"""Analytic conservation bounds and real recorded-source integration."""
import copy
import io
import itertools
import json
import math
import shutil
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path
from unittest.mock import patch

from expedition73 import earthdata, regional, surface_source, surface_support, surface_workflow
from expedition73.__main__ import main
from expedition73.power import PilotError, loads

ROOT = Path(__file__).resolve().parents[1]
try:
    import netCDF4
except ImportError:
    netCDF4 = None


class AreaBoundsTests(unittest.TestCase):
    def test_known_partial_cell_conserves_available_selected_and_unselected_area(self):
        self.assertEqual(surface_support.area_bounds(100, 40, .7),
                         {'lower_m2': 10, 'uniform_estimate_m2': 28, 'upper_m2': 40})
        self.assertEqual(surface_support.area_bounds(100, 40, .2),
                         {'lower_m2': 0, 'uniform_estimate_m2': 8, 'upper_m2': 20})

    def test_exhaustive_subcell_placements_reach_both_bounds(self):
        # Eight equal-area subcells; first k are inside the window. Enumerate
        # all placements with s selected subcells, independently of the formula.
        for k in range(9):
            for s in range(9):
                placements = [len(set(choice).intersection(range(k)))
                              for choice in itertools.combinations(range(8), s)]
                result = surface_support.area_bounds(8, k, s / 8)
                self.assertEqual(result['lower_m2'], min(placements))
                self.assertEqual(result['upper_m2'], max(placements))
                self.assertLessEqual(result['lower_m2'], result['uniform_estimate_m2'])
                self.assertLessEqual(result['uniform_estimate_m2'], result['upper_m2'])

    def test_full_empty_and_pure_cells_have_no_placement_ambiguity(self):
        for full, part, f, selected in [(100, 100, .7, 70), (100, 0, .7, 0),
                                         (100, 40, 0, 0), (100, 40, 1, 40)]:
            self.assertEqual(list(surface_support.area_bounds(full, part, f).values()), [selected] * 3)

    def test_complementary_component_bounds_follow_area_conservation(self):
        for f in [0, .001, .2, .6, 1]:
            left = surface_support.area_bounds(100, 37, f)
            right = surface_support.area_bounds(100, 37, 1 - f)
            self.assertAlmostEqual(left['lower_m2'] + right['upper_m2'], 37)
            self.assertAlmostEqual(left['uniform_estimate_m2'] + right['uniform_estimate_m2'], 37)

    def test_invalid_nonfinite_or_out_of_range_values_rejected(self):
        for args in [(0, 0, 0), (100, -1, .5), (100, 101, .5), (100, 50, -1e-8),
                     (100, 50, 1.000001), (100, 50, math.nan), (math.inf, 50, .5), (100, True, .5)]:
            with self.subTest(args=args), self.assertRaises(PilotError):
                surface_support.area_bounds(*args)


@unittest.skipIf(netCDF4 is None, 'optional requirements-mask.txt not installed')
class SupportIntegrationTests(unittest.TestCase):
    def directories(self, region='a'):
        return ROOT / f'examples/{region}-window-2024', ROOT / f'examples/{region}-surface-fractions'

    def test_real_regions_cover_window_and_match_existing_uniform_weight_preview(self):
        for region, count in [('a', 56), ('b', 55)]:
            result = surface_support.run(*self.directories(region))
            reference = loads((ROOT / f'examples/{region}-surface-sensitivity.json').read_bytes())
            with self.subTest(region=region):
                self.assertEqual(result['cell_count'], count)
                self.assertEqual(result['selection_status'], 'candidate')
                self.assertFalse(result['method']['mask_policy_accepted'])
                self.assertEqual(result['method']['inference'], 'not_performed')
                self.assertGreater(result['clipped_cells'], 0)
                for policy in surface_support.POLICIES:
                    value = result['policies'][policy]
                    self.assertAlmostEqual(value['uniform_estimate_m2'],
                                           reference['spatial_support'][policy]['effective_area_m2'], places=4)
                    self.assertLessEqual(value['lower_m2'], value['uniform_estimate_m2'])
                    self.assertLessEqual(value['uniform_estimate_m2'], value['upper_m2'])
                    self.assertLessEqual(value['upper_m2'], result['window_area_m2'])
                self.assertEqual(result['provenance'], reference['provenance'])

    def test_unclipped_cells_have_equal_endpoints_and_only_clipped_cells_can_be_ambiguous(self):
        result = surface_support.run(*self.directories('b'))
        for cell in result['cells']:
            for values in cell['policies'].values():
                if not cell['clipped']:
                    self.assertEqual(values['lower_m2'], values['upper_m2'])
                self.assertLessEqual(values['upper_m2'], cell['intersection_area_m2'])

    def test_committed_support_summary_recomputes_with_exact_source_hashes(self):
        saved = loads((ROOT / 'examples/surface-support-summary.json').read_bytes())
        for region in ['a', 'b']:
            actual = surface_support.run(*self.directories(region))
            actual.pop('cells')
            self.assertEqual(actual['provenance'], saved[region]['provenance'])
            self.assertTrue(regional._same_result(actual, saved[region]))

    def test_repeated_audit_is_deterministic_and_does_not_change_existing_examples(self):
        paths = list((ROOT / 'examples/a-surface-fractions').iterdir())
        before = {p.name: p.read_bytes() for p in paths}
        self.assertEqual(surface_support.run(*self.directories()), surface_support.run(*self.directories()))
        self.assertEqual(before, {p.name: p.read_bytes() for p in paths})

    def test_no_credentials_or_network_and_sources_replayed_once(self):
        with patch.object(earthdata, 'get_token', side_effect=AssertionError('No credentials')), \
                patch.object(surface_source, 'fetch_subset', side_effect=AssertionError('No network')), \
                patch('expedition73.power.urlopen', side_effect=AssertionError('No network')), \
                patch.object(surface_source, 'replay_data', wraps=surface_source.replay_data) as replay:
            result = surface_support.run(*self.directories())
        replay.assert_called_once()
        self.assertIn('CONDITIONAL_AREA_BOUNDS_NOT_CONFIDENCE_INTERVALS', result['warnings'])

    def test_cli_json_matches_calculation_and_failure_writes_no_success_output(self):
        window, fractions = self.directories()
        with redirect_stdout(io.StringIO()) as output:
            code = main(['audit-surface-support', '--window-run', str(window), '--fraction-run', str(fractions)])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output.getvalue()), surface_support.run(window, fractions))
        with tempfile.TemporaryDirectory() as temporary:
            corrupt = Path(temporary) / 'corrupt'
            shutil.copytree(fractions, corrupt)
            (corrupt / 'response.nc4').write_bytes(b'corrupt')
            with redirect_stdout(io.StringIO()) as output, redirect_stderr(io.StringIO()):
                code = main(['audit-surface-support', '--window-run', str(window), '--fraction-run', str(corrupt)])
            self.assertEqual(code, 1)
            self.assertEqual(output.getvalue(), '')

    def test_mismatched_regions_and_changed_cell_geometry_rejected(self):
        with self.assertRaises(PilotError):
            surface_support.run(self.directories('a')[0], self.directories('b')[1])
        _, report = surface_workflow.run(*self.directories())
        temperature = copy.deepcopy(report['nodes']['Temperature']['artifact']['value'])
        mask = report['nodes']['Fractions']['artifact']['value']['result']
        temperature['result']['module_details']['cells'][0]['area_m2'] *= .9
        with self.assertRaises(PilotError):
            surface_support._summarize(temperature['result'], mask, temperature['request'])
