"""A successful metadata fetch is not proof of a usable AREA variable."""
import io
import json
import tempfile
import unittest
import xml.etree.ElementTree as ET
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path
from unittest.mock import patch

from expedition73 import earthdata, surface_source
from expedition73.__main__ import main
from expedition73.power import PilotError, loads

ROOT = Path(__file__).resolve().parents[1]
METADATA = ROOT / 'examples/a-surface-fractions/metadata.dmr.xml'


class SourceAreaTests(unittest.TestCase):
    def add(self, snippet):
        root = ET.fromstring(METADATA.read_bytes())
        root.append(ET.fromstring(snippet))
        return ET.tostring(root)

    def test_recorded_source_and_committed_summary_show_absence_not_a_zero_area(self):
        expected = loads((ROOT / 'examples/source-area-capability.json').read_bytes())
        for region in ['a', 'b']:
            raw = (ROOT / f'examples/{region}-surface-fractions/metadata.dmr.xml').read_bytes()
            result = surface_source.area_capability(raw)
            self.assertEqual(result, expected)
            self.assertIsNone(result['area']['declaration'])
            self.assertEqual(result['area']['comparison_status'], 'not_available_in_selected_granule')
            self.assertFalse(result['area']['comparison_performed'])
            self.assertFalse(result['scientific_profile_accepted'])
            self.assertEqual(len(result['available_numeric_variables']), 9)

    def test_future_numeric_area_declaration_still_does_not_verify_any_values_or_units(self):
        for unit in ['m+2', 'unexpected-unit']:
            raw = self.add('<Float32 name="AREA"><Dim name="/time"/><Dim name="/lat"/><Dim name="/lon"/>'
                           '<Attribute name="units"><Value>' + unit + '</Value></Attribute></Float32>')
            result = surface_source.area_capability(raw)
            self.assertEqual(result['area']['comparison_status'], 'metadata_present_values_not_validated')
            self.assertEqual(result['area']['declaration']['units'], [unit])
            self.assertFalse(result['area']['numeric_values_retrieved'])
            self.assertFalse(result['area']['comparison_performed'])
            self.assertFalse(result['automatic_product_or_geometry_substitution'])

    def test_attribute_text_is_not_mistaken_for_numeric_area(self):
        raw = self.add('<Attribute name="AREA" type="String"><Value>documentation only</Value></Attribute>')
        self.assertFalse(surface_source.area_capability(raw)['area']['numeric_declaration_present'])

    def test_ambiguous_duplicates_or_grouped_variables_fail_instead_of_claiming_absence(self):
        root = ET.fromstring(self.add('<Float32 name="AREA"/>'))
        root.append(ET.fromstring('<Float32 name="AREA"/>'))
        for raw in [ET.tostring(root), self.add('<Group name="nested"><Float32 name="AREA"/></Group>')]:
            with self.assertRaises(PilotError):
                surface_source.area_capability(raw)

    def test_wrong_product_grid_invalid_or_oversize_metadata_fail(self):
        raw = METADATA.read_bytes()
        for invalid in [b'<html>not metadata</html>', b'not xml', raw.replace(b'361', b'360', 1),
                        raw.replace(surface_source.DATASET_NAME.encode(), b'other-product.nc4'),
                        b'x' * (earthdata.MAX_METADATA_BYTES + 1)]:
            with self.assertRaises(PilotError):
                surface_source.area_capability(invalid)

    def test_cli_is_offline_and_absence_is_an_explicit_valid_report(self):
        with patch.object(earthdata, 'get_token', side_effect=AssertionError('No credentials')), \
                patch.object(earthdata, '_read', side_effect=AssertionError('No network')), \
                patch.object(surface_source, 'fetch_subset', side_effect=AssertionError('No subset')), \
                redirect_stdout(io.StringIO()) as output:
            code = main(['check-source-area', '--metadata', str(METADATA)])
        self.assertEqual(code, 0)  # Check completed; status in JSON says AREA unavailable.
        self.assertEqual(json.loads(output.getvalue()), surface_source.area_capability(METADATA.read_bytes()))

    def test_cli_invalid_input_writes_no_partial_success_report(self):
        with tempfile.TemporaryDirectory() as temp:
            metadata = Path(temp) / 'invalid.xml'
            metadata.write_bytes(b'<html/>')
            with redirect_stdout(io.StringIO()) as output, redirect_stderr(io.StringIO()):
                code = main(['check-source-area', '--metadata', str(metadata)])
            self.assertEqual(code, 1)
            self.assertEqual(output.getvalue(), '')
