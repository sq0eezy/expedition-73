"""Real annual source replay and temporal completeness, without network."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from expedition73 import history, regional, surface_workflow, tiled
from expedition73.power import PilotError, loads

ROOT = Path(__file__).resolve().parents[1]


class HistoryTests(unittest.TestCase):
    def inputs(self, region='a'):
        directory = ROOT / f'examples/{region}-history-2023-2024'
        config = loads((directory / 'request.json').read_bytes())
        files = [history.capture(directory / f'year-{year}') for year in (2023, 2024)]
        return config, files

    def test_actual_two_year_histories_have_24_ordered_months_and_preserve_annual_values(self):
        for region, cells in [('a', 56), ('b', 55)]:
            config, files = self.inputs(region)
            _, result = history.assemble(config, files)
            self.assertEqual(result['quality']['complete_months'], 24)
            self.assertEqual(result['quality']['missing_months'], [])
            self.assertEqual(result['spatial_support']['cell_count'], cells)
            self.assertEqual(result['time']['start'], '2023-01')
            expected = [row for f in files for row in loads(f['result.json'])['series']]
            self.assertEqual(result['series'], expected)
            self.assertTrue(regional._same_result(result, history.validate_run(ROOT / f'examples/{region}-history-2023-2024')))

    def test_original_2024_source_bytes_are_preserved_exactly(self):
        for r in ('a', 'b'):
            source = ROOT / f'examples/{r}-window-2024'
            copy_dir = ROOT / f'examples/{r}-history-2023-2024/year-2024'
            for name, raw in history.capture(source).items():
                self.assertEqual(raw, (copy_dir / name).read_bytes())

    def test_24_year_plan_is_annual_bounded_and_does_not_fetch(self):
        config, _ = self.inputs(); config.update(start_year=2001, end_year=2024)
        with patch.object(regional, 'fetch', side_effect=AssertionError('No network')):
            planned = history.plan(config)
        self.assertEqual(len(planned), 24)
        self.assertTrue(all(c['start_year'] == c['end_year'] for c in planned))
        self.assertEqual(sum(12 for _ in planned), 288)
        planned[0]['candidate_bbox'][0] = -100
        self.assertEqual(config['candidate_bbox'][0], -113)

    def test_invalid_ranges_and_integer_types_fail_before_network(self):
        config, _ = self.inputs()
        for start, end in [(2024, 2023), (1981, 2031), (2023.0, 2024), (2023, True), (2023, 9999)]:
            with self.subTest(start=start, end=end), self.assertRaises(PilotError):
                history.plan({**config, 'start_year': start, 'end_year': end})

    def test_missing_duplicate_reversed_years_and_extra_files_are_rejected(self):
        config, files = self.inputs()
        variants = [files[:1], files[::-1], [files[0], files[0]], [{**files[0], '../private': b'ignored'}, files[1]]]
        for variant in variants:
            with self.assertRaises(PilotError): history.assemble(config, variant)

    def test_raw_tampering_cannot_hide_behind_a_plausible_annual_result(self):
        config, files = self.inputs()
        raw = loads(files[0]['response.json'])
        raw['features'][0]['properties']['parameter']['T2M']['202301'] += 1
        files[0]['response.json'] = history.encoded(raw)
        with self.assertRaises(PilotError): history.assemble(config, files)

    def test_equivalent_single_and_tiled_annual_contracts_share_the_same_support(self):
        config, files = self.inputs()
        request = loads(files[0]['request.json'])
        raw = files[0]['response.json']
        stamp = loads(files[0]['result.json'])['provenance']['retrieved_at']
        tile = tiled.plan(request)[0]
        manifest = {'schema_version': '0.1.0', 'format': 'power_tiled_run',
                    'tiles': [tiled.manifest_entry(tile, raw, stamp)]}
        converted = {'request.json': files[0]['request.json'], 'tile-001.json': raw,
                     'manifest.json': history.encoded(manifest),
                     'result.json': history.encoded(tiled.normalize([raw], request, manifest))}
        _, result = history.assemble(config, [converted, files[1]])
        self.assertEqual(result['quality']['complete_months'], 24)

    def test_individually_valid_api_revision_cannot_be_silently_mixed_across_years(self):
        config, files = self.inputs()
        request = loads(files[0]['request.json']); stored = loads(files[0]['result.json'])
        raw = loads(files[0]['response.json']); raw['header']['api']['version'] = 'changed-version'
        files[0]['response.json'] = history.encoded(raw)
        files[0]['result.json'] = history.encoded(regional.normalize(files[0]['response.json'], request, stored['provenance']['retrieved_at']))
        surface_workflow._window_replay(files[0])
        with self.assertRaises(PilotError): history.assemble(config, files)

    def test_missing_provider_month_stays_null_and_is_counted(self):
        config, files = self.inputs()
        request = loads(files[0]['request.json']); stored = loads(files[0]['result.json'])
        raw = loads(files[0]['response.json'])
        for feature in raw['features']: feature['properties']['parameter']['T2M'].pop('202301')
        files[0]['response.json'] = history.encoded(raw)
        files[0]['result.json'] = history.encoded(regional.normalize(files[0]['response.json'], request, stored['provenance']['retrieved_at']))
        _, result = history.assemble(config, files)
        self.assertEqual(result['series'][0]['value'], None)
        self.assertEqual(result['quality']['complete_months'], 23)
        self.assertEqual(result['quality']['missing_months'], ['2023-01'])

    def test_offline_assembly_rejects_missing_seeds_without_creating_output(self):
        config, _ = self.inputs()
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / 'history'
            with self.assertRaises(PilotError): history.collect(config, target, [])
            self.assertFalse(target.exists())

    def test_duplicate_or_incompatible_seeds_are_checked_before_fetch(self):
        config, _ = self.inputs()
        seed = ROOT / 'examples/a-window-2024'
        with tempfile.TemporaryDirectory() as temp, patch.object(regional, 'fetch') as fetch:
            with self.assertRaises(PilotError): history.collect(config, Path(temp) / 'history', [seed, seed], fetch_missing=True)
            fetch.assert_not_called()

    def test_failed_fetch_publishes_no_partial_history_and_cleans_owned_stage(self):
        config, _ = self.inputs()
        with tempfile.TemporaryDirectory() as temp, patch.object(regional, 'fetch', side_effect=PilotError('offline')):
            with self.assertRaises(PilotError): history.collect(config, Path(temp) / 'history', fetch_missing=True)
            self.assertEqual(list(Path(temp).iterdir()), [])

    def test_normal_output_is_readable_replayable_and_existing_run_is_preserved(self):
        config, _ = self.inputs('b')
        source = ROOT / 'examples/b-history-2023-2024'
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / 'history'
            history.collect(config, target, [source / 'year-2024', source / 'year-2023'])
            self.assertEqual(history.validate_run(target)['quality']['complete_months'], 24)
            before = (target / 'result.json').read_bytes()
            with self.assertRaises(PilotError): history.collect(config, target, [])
            self.assertEqual(before, (target / 'result.json').read_bytes())
            damaged = loads(before); damaged['series'][0]['value'] += 1
            (target / 'result.json').write_bytes(history.encoded(damaged))
            with self.assertRaises(PilotError): history.validate_run(target)
