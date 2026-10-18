"""Real recorded subset integration; temp mutations are artificial error cases."""
import copy
import io
import json
import shutil
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path
from unittest.mock import patch

from expedition73 import earthdata, masking, regional, surface_source, surface_workflow
from expedition73.__main__ import main
from expedition73.power import loads
from expedition73.workflow import compare_snapshot, execute, validate_artifact

ROOT = Path(__file__).resolve().parents[1]
try:
    import numpy as np
    import netCDF4
except ImportError:
    netCDF4 = None


@unittest.skipIf(netCDF4 is None, 'optional requirements-mask.txt not installed')
class SurfaceWorkflowTests(unittest.TestCase):
    def directories(self, region='a'):
        return ROOT / f'examples/{region}-window-2024', ROOT / f'examples/{region}-surface-fractions'

    def test_both_real_regions_replay_once_and_share_the_same_upstream_ids(self):
        for region, count in [('a', 56), ('b', 55)]:
            with patch.object(surface_workflow, '_window_replay', wraps=surface_workflow._window_replay) as replay, \
                    patch.object(surface_source, 'replay_data', wraps=surface_source.replay_data) as fractions:
                spec, report = surface_workflow.run(*self.directories(region))
            with self.subTest(region=region):
                replay.assert_called_once()
                fractions.assert_called_once()
                self.assertEqual(report['status'], 'completed')
                self.assertEqual(report['order'], ['Temperature', 'Fractions', 'Land', 'LandIce', 'Sensitivity'])
                nodes = report['nodes']
                temperature = nodes['Temperature']['artifact']
                mask = nodes['Fractions']['artifact']
                self.assertEqual(mask['inputs']['temperature'], temperature['artifact_id'])
                self.assertEqual(len(mask['value']['result']['cells']), count)
                for name in ['Land', 'LandIce']:
                    self.assertEqual(nodes[name]['artifact']['inputs']['temperature'], temperature['artifact_id'])
                    self.assertEqual(nodes[name]['artifact']['inputs']['fractions'], mask['artifact_id'])
                for record in nodes.values():
                    validate_artifact(record['artifact'])
                result = nodes['Sensitivity']['artifact']['value']
                self.assertEqual(result['diagnostics']['complete_paired_months'], 12)
                self.assertFalse(result['method']['mask_policy_accepted'])
                self.assertIn('FRACTION_ASSUMED_UNIFORM_WITHIN_SOURCE_CELL', result['warnings'])

    def test_independent_numpy_january_reference_matches_both_policies(self):
        for region in ['a', 'b']:
            _, report = surface_workflow.run(*self.directories(region))
            window = report['nodes']['Temperature']['artifact']['value']['result']
            mask = report['nodes']['Fractions']['artifact']['value']['result']
            by_coordinate = {(c['longitude'], c['latitude']): c['fractions'] for c in mask['cells']}
            cells = window['module_details']['cells']
            temperatures = np.array([cell['series'][0]['value'] for cell in cells])
            areas = np.array([cell['area_m2'] for cell in cells])
            for node, components in [('Land', ['FRLAND']), ('LandIce', ['FRLAND', 'FRLANDICE'])]:
                factors = np.array([sum(by_coordinate[(cell['longitude'], cell['latitude'])][component]
                                        for component in components) for cell in cells])
                reference = float(np.average(temperatures, weights=areas * factors))
                actual = report['nodes'][node]['artifact']['value']['series'][0]['value']
                self.assertAlmostEqual(actual, reference, places=11)

    def test_saved_candidate_examples_recompute_with_identical_source_provenance(self):
        for region in ['a', 'b']:
            _, report = surface_workflow.run(*self.directories(region))
            actual = report['nodes']['Sensitivity']['artifact']['value']
            expected = loads((ROOT / f'examples/{region}-surface-sensitivity.json').read_bytes())
            with self.subTest(region=region):
                self.assertEqual(actual['provenance']['source_files_sha256'],
                                 expected['provenance']['source_files_sha256'])
                self.assertTrue(regional._same_result(actual, expected))
                self.assertEqual(actual['provenance']['surface_fractions']['dataset'], 'M2C0NXASM')

    def test_no_network_or_credential_reader_is_used(self):
        with patch.object(earthdata, 'get_token', side_effect=AssertionError('No credentials permitted')), \
                patch.object(surface_source, 'fetch_subset', side_effect=AssertionError('No fetch permitted')), \
                patch('expedition73.power.urlopen', side_effect=AssertionError('No network permitted')):
            _, report = surface_workflow.run(*self.directories())
        self.assertEqual(report['status'], 'completed')

    def test_mismatched_candidate_regions_block_fraction_and_consumers(self):
        window, _ = self.directories('a')
        _, mask = self.directories('b')
        _, report = surface_workflow.run(window, mask)
        self.assertEqual(report['nodes']['Temperature']['status'], 'completed')
        self.assertEqual(report['nodes']['Fractions']['status'], 'failed')
        for name in ['Land', 'LandIce', 'Sensitivity']:
            self.assertEqual(report['nodes'][name]['status'], 'blocked')

    def test_corrupt_fraction_bytes_block_both_previews_without_fake_result(self):
        with tempfile.TemporaryDirectory() as temp:
            window, original = self.directories()
            mask = Path(temp) / 'mask'
            shutil.copytree(original, mask)
            (mask / 'response.nc4').write_bytes(b'corrupt artificial response')
            _, report = surface_workflow.run(window, mask)
            self.assertEqual(report['nodes']['Temperature']['status'], 'completed')
            self.assertEqual(report['nodes']['Fractions']['reason'], 'COMPUTE_FAILED')
            self.assertEqual(report['status'], 'incomplete')
            self.assertNotIn('artifact', report['nodes']['Sensitivity'])

    def test_corrupt_saved_temperature_result_blocks_all_downstream(self):
        with tempfile.TemporaryDirectory() as temp:
            original, mask = self.directories()
            window = Path(temp) / 'window'
            shutil.copytree(original, window)
            saved = loads((window / 'result.json').read_bytes())
            saved['series'][0]['value'] += 1
            (window / 'result.json').write_text(json.dumps(saved), encoding='utf-8')
            _, report = surface_workflow.run(window, mask)
            self.assertEqual(report['nodes']['Temperature']['status'], 'failed')
            self.assertTrue(all(report['nodes'][name]['status'] == 'blocked' for name in
                                ['Fractions', 'Land', 'LandIce', 'Sensitivity']))

    def test_sources_are_frozen_and_a_new_source_hash_marks_old_work_stale(self):
        with tempfile.TemporaryDirectory() as temp:
            window, original = self.directories()
            mask = Path(temp) / 'mask'
            shutil.copytree(original, mask)
            spec, registry = surface_workflow.build(window, mask)
            (mask / 'response.nc4').write_bytes(b'changed after snapshot capture')
            report = execute(spec, 'Sensitivity', registry)
            self.assertEqual(report['status'], 'completed')
            new_spec, new_registry = surface_workflow.build(window, mask)
            self.assertEqual(set(compare_snapshot(report, new_spec, 'Sensitivity').values()), {'stale'})
            self.assertEqual(execute(new_spec, 'Sensitivity', new_registry)['status'], 'incomplete')
            self.assertNotIn(str(Path(temp)), json.dumps(spec))

    def test_preview_policy_cannot_be_relabelled(self):
        spec, registry = surface_workflow.build(*self.directories('b'))
        spec['nodes'][2]['parameters']['components'] = ['FRLAND', 'FRLANDICE']
        report = execute(spec, 'Sensitivity', registry)
        self.assertEqual(report['nodes']['Land']['reason'], 'OUTPUT_INVALID')
        self.assertEqual(report['nodes']['LandIce']['status'], 'completed')
        self.assertEqual(report['nodes']['Sensitivity']['status'], 'blocked')

    def test_complete_case_zero_ice_in_a_has_identical_two_policies(self):
        _, report = surface_workflow.run(*self.directories('a'))
        result = report['nodes']['Sensitivity']['artifact']['value']
        self.assertEqual(result['diagnostics']['max_abs_land_ice_minus_land_degC'], 0)
        self.assertTrue(all(row['land'] == row['land_and_ice'] for row in result['series']))

    def test_missing_temperature_month_stays_null_in_all_candidate_outputs(self):
        with tempfile.TemporaryDirectory() as temp:
            original, mask = self.directories()
            window = Path(temp) / 'window'
            shutil.copytree(original, window)
            request = loads((window / 'request.json').read_bytes())
            stored = loads((window / 'result.json').read_bytes())
            raw = loads((window / 'response.json').read_bytes())
            raw['features'][0]['properties']['parameter']['T2M']['202401'] = -999
            encoded = json.dumps(raw).encode()
            replayed = regional.normalize(encoded, request, stored['provenance']['retrieved_at'])
            (window / 'response.json').write_bytes(encoded)
            (window / 'result.json').write_text(json.dumps(replayed), encoding='utf-8')
            _, report = surface_workflow.run(window, mask)
            self.assertEqual(report['status'], 'completed')
            result = report['nodes']['Sensitivity']['artifact']['value']
            self.assertEqual(result['diagnostics']['complete_paired_months'], 11)
            self.assertTrue(all(result['series'][0][key] is None for key in
                                ['unmasked', 'land', 'land_and_ice', 'land_minus_unmasked', 'land_ice_minus_land']))

    def test_cli_saves_complete_report_and_never_overwrites(self):
        with tempfile.TemporaryDirectory() as temp:
            window, mask = self.directories()
            output = Path(temp) / 'run'
            args = ['run-surface-workflow', '--window-run', str(window), '--fraction-run', str(mask),
                    '--output-dir', str(output)]
            with redirect_stdout(io.StringIO()):
                self.assertEqual(main(args), 0)
            self.assertEqual(sorted(p.name for p in output.iterdir()),
                             ['request.workflow.json', 'sensitivity.json', 'workflow.json'])
            before = (output / 'workflow.json').read_bytes()
            with patch.object(surface_workflow, 'run') as runner, redirect_stderr(io.StringIO()):
                self.assertEqual(main(args), 1)
            runner.assert_not_called()
            self.assertEqual((output / 'workflow.json').read_bytes(), before)

    def test_cli_failed_run_retains_status_but_writes_no_sensitivity(self):
        with tempfile.TemporaryDirectory() as temp:
            window, _ = self.directories('a')
            _, wrong_mask = self.directories('b')
            output = Path(temp) / 'failed'
            with redirect_stdout(io.StringIO()):
                self.assertEqual(main(['run-surface-workflow', '--window-run', str(window),
                                       '--fraction-run', str(wrong_mask), '--output-dir', str(output)]), 2)
            self.assertTrue((output / 'workflow.json').is_file())
            self.assertFalse((output / 'sensitivity.json').exists())


if __name__ == '__main__':
    unittest.main()
