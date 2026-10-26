"""Python-owned annual results bind to the exact, unchanged monthly catalog."""
import copy
import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from expedition73 import annual_weighting, history, regional, web_preview
from expedition73.power import PilotError, loads

ROOT=Path(__file__).resolve().parents[1]
WEB=ROOT.parent/'web'


class AnnualWebTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry=loads((WEB/'history-regions.json').read_bytes())
        cls.data=web_preview.catalog(ROOT,cls.registry)
        cls.raw=history.encoded(cls.data)
        cls.annual=web_preview.annual_payload(ROOT,cls.registry,cls.data,cls.raw)

    def test_actual_annual_results_bind_to_the_original_catalog_and_stored_audits(self):
        self.assertEqual(hashlib.sha256(self.raw).hexdigest(),'58cbad9e6951c648501a33a9f0bda71e589d09dd6bfb38f3de1727498ed75fdb')
        self.assertEqual(self.annual['source_catalog_sha256'],hashlib.sha256(self.raw).hexdigest())
        self.assertEqual(self.annual['status'],'available')
        for entry in self.annual['regions']:
            saved=loads((ROOT/f"examples/{entry['id'].lower()}-annual-weighting-audit.json").read_bytes())
            self.assertTrue(regional._same_result(entry['audit'],saved))
            self.assertEqual(len(entry['audit']['series']),24)

    def test_mixed_annual_source_identity_years_or_region_cannot_export(self):
        for mutate in [lambda a:a['provenance']['annual_sources'][0]['files_sha256'].update({'result.json':'0'*64}),
                       lambda a:a['series'].pop(),lambda a:a['region'].update(id='C')]:
            audit=copy.deepcopy(self.annual['regions'][0]['audit']); mutate(audit)
            with patch.object(annual_weighting,'run',return_value=audit),self.assertRaises(PilotError):
                web_preview.annual_payload(ROOT,self.registry,self.data,self.raw)

    def test_legacy_source_explicitly_reports_no_annual_history(self):
        with patch.object(annual_weighting,'run',side_effect=AssertionError('No history available')):
            result=web_preview.annual_payload(ROOT,None,{},b'legacy fixture')
        self.assertEqual(result['status'],'not_available'); self.assertEqual(result['regions'],[])
        self.assertEqual(result['source_catalog_sha256'],hashlib.sha256(b'legacy fixture').hexdigest())

    def test_failed_annual_source_preserves_previous_generated_files(self):
        with tempfile.TemporaryDirectory() as temp:
            output=Path(temp)/'dist'; output.mkdir(); (output/'index.html').write_bytes(b'previous build')
            with patch.object(web_preview,'catalog',return_value=self.data),patch.object(web_preview,'annual_payload',side_effect=PilotError('source changed')):
                with self.assertRaises(PilotError): web_preview.build(ROOT,WEB,output)
            self.assertEqual((output/'index.html').read_bytes(),b'previous build')
            self.assertEqual([p.name for p in output.iterdir()],['index.html'])
