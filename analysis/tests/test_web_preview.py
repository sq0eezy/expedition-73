"""Real recorded-source export, coherent snapshots and isolated public outputs."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from expedition73 import earthdata, surface_source, surface_workflow, web_preview
from expedition73.power import PilotError, loads

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT.parent / 'web'
try:
    import netCDF4
except ImportError:
    netCDF4 = None


@unittest.skipIf(netCDF4 is None, 'optional requirements-mask.txt not installed')
class WebPreviewTests(unittest.TestCase):
    def setUp(self):
        self.registry = loads((WEB / 'regions.json').read_bytes())

    def test_real_export_matches_existing_series_and_source_hashes_exactly(self):
        result = web_preview.payload(ROOT, self.registry)
        self.assertFalse(result['inference_performed'])
        self.assertEqual(result['selection_status'], 'candidate')
        self.assertEqual(result['dates'], [f'2024-{m:02d}' for m in range(1, 13)])
        for region in result['regions']:
            saved = loads((ROOT / f"examples/{region['id'].lower()}-surface-sensitivity.json").read_bytes())
            self.assertEqual(region['series'], saved['series'])
            self.assertEqual(region['provenance'], saved['provenance'])
            self.assertEqual(region['source_area']['comparison_status'], 'not_available_in_selected_granule')

    def test_single_region_registry_needs_no_frontend_or_source_algorithm_change(self):
        result = web_preview.payload(ROOT, [self.registry[1]])
        self.assertEqual([r['id'] for r in result['regions']], ['B'])
        self.assertEqual(result['regions'][0]['display_name'], 'Kuzey Alaska')

    def test_registry_rejects_duplicate_wrong_identity_extra_fields_and_empty_names(self):
        for registry in [[], self.registry * 2, [{**self.registry[0], 'id': 'wrong'}],
                         [{**self.registry[0], 'display_name': ''}], [{**self.registry[0], 'token': 'not-allowed'}]]:
            with self.subTest(registry=registry), self.assertRaises(PilotError):
                web_preview.payload(ROOT, registry)

    def test_input_paths_cannot_traverse_to_credentials_or_private_directories(self):
        for value in ['', '../.env', '.env', 'private-notes/source', '/tmp/source',
                      'examples/../../.env', 'C:\\secrets', 'examples\\source']:
            with self.subTest(value=value), self.assertRaises(PilotError):
                web_preview.payload(ROOT, [{**self.registry[0], 'window': value}])

    def test_export_does_not_access_network_or_credential_reader(self):
        with patch.object(earthdata, 'get_token', side_effect=AssertionError('No token')), \
                patch.object(earthdata, '_read', side_effect=AssertionError('No network')), \
                patch.object(surface_source, 'fetch_subset', side_effect=AssertionError('No subset')):
            result = web_preview.payload(ROOT, self.registry)
        self.assertEqual(result['data_mode'], 'recorded_offline_replay')

    def test_metadata_replacement_after_replay_is_rejected(self):
        spec, report = surface_workflow.run(ROOT / self.registry[0]['window'], ROOT / self.registry[0]['fractions'])
        report = copy.deepcopy(report)
        report['nodes']['Sensitivity']['artifact']['value']['provenance']['source_files_sha256']['fractions']['metadata.dmr.xml'] = '0' * 64
        with patch.object(surface_workflow, 'run', return_value=(spec, report)), self.assertRaises(PilotError):
            web_preview.payload(ROOT, [self.registry[0]])

    def test_different_time_standard_or_provider_version_cannot_be_paired(self):
        runs = [surface_workflow.run(ROOT / entry['window'], ROOT / entry['fractions']) for entry in self.registry]
        for field in ['provider_time_standard', 'api_version']:
            changed = copy.deepcopy(runs)
            summary = changed[1][1]['nodes']['Sensitivity']['artifact']['value']
            if field == 'provider_time_standard':
                summary['time'][field] = 'UTC'
            else:
                summary['provenance']['temperature'][field] = 'other-version'
            with self.subTest(field=field), patch.object(surface_workflow, 'run', side_effect=changed), self.assertRaises(PilotError):
                web_preview.payload(ROOT, self.registry)

    def test_failed_source_or_unsupported_period_produces_no_partial_output(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / 'dist'
            with patch.object(surface_workflow, 'run', return_value=({}, {'status': 'incomplete'})), self.assertRaises(PilotError):
                web_preview.build(ROOT, WEB, output)
            self.assertFalse(output.exists())
        spec, report = surface_workflow.run(ROOT / self.registry[0]['window'], ROOT / self.registry[0]['fractions'])
        report['nodes']['Sensitivity']['artifact']['value']['series'].pop()
        with patch.object(surface_workflow, 'run', return_value=(spec, report)), self.assertRaises(PilotError):
            web_preview.payload(ROOT, [self.registry[0]])

    def test_output_contains_only_enumerated_assets_and_is_repeatable(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / 'dist'
            result = web_preview.build(ROOT, WEB, output)
            files = {p.relative_to(output).as_posix(): p.read_bytes() for p in output.rglob('*') if p.is_file()}
            self.assertEqual(set(files), {'index.html', 'styles.css', 'app.js', 'data/results.json'})
            self.assertFalse(result['live_nasa_request'])
            web_preview.build(ROOT, WEB, output)
            self.assertEqual(files, {p.relative_to(output).as_posix(): p.read_bytes() for p in output.rglob('*') if p.is_file()})
            (output / '.env').write_text('private local fixture', encoding='utf-8')
            with self.assertRaises(PilotError):
                web_preview.build(ROOT, WEB, output)
        with self.assertRaises(PilotError):
            web_preview.build(ROOT, WEB, WEB / 'src')
