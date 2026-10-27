"""Python-owned annual results bind to the exact, unchanged monthly catalog."""
import copy
import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from expedition73 import annual_workflow, history, regional, web_preview, workflow_trace
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
        cls.execution=annual_workflow.run(ROOT/'examples/a-history-2001-2024')

    def test_actual_annual_results_bind_to_the_original_catalog_and_stored_audits(self):
        self.assertEqual(hashlib.sha256(self.raw).hexdigest(),'58cbad9e6951c648501a33a9f0bda71e589d09dd6bfb38f3de1727498ed75fdb')
        self.assertEqual(self.annual['source_catalog_sha256'],hashlib.sha256(self.raw).hexdigest())
        self.assertEqual(self.annual['status'],'available')
        self.assertEqual(self.annual['schema_version'],'0.2.0')
        for entry in self.annual['regions']:
            saved=loads((ROOT/f"examples/{entry['id'].lower()}-annual-weighting-audit.json").read_bytes())
            self.assertTrue(regional._same_result(entry['audit'],saved))
            self.assertEqual(len(entry['audit']['series']),24)
            workflow=entry['workflow']; context=loads(workflow['context_json'].encode('utf-8'))
            self.assertEqual(workflow['trace']['context_sha256'],hashlib.sha256(workflow['context_json'].encode('utf-8')).hexdigest())
            self.assertEqual(workflow['trace']['target'],'AnnualWeighting')
            self.assertEqual(context['source_files_sha256']['history']['result.json'],saved['provenance']['source_history_result_sha256'])
            self.assertEqual(context['source_files_sha256']['annual_sources'],saved['provenance']['annual_sources'])

    def test_mixed_annual_source_identity_years_or_region_cannot_export(self):
        for mutate in [lambda a:a['provenance']['annual_sources'][0]['files_sha256'].update({'result.json':'0'*64}),
                       lambda a:a['series'].pop(),lambda a:a['region'].update(id='C')]:
            spec,run=copy.deepcopy(self.execution); mutate(run['nodes']['AnnualWeighting']['artifact']['value'])
            with patch.object(annual_workflow,'run',return_value=(spec,run)),self.assertRaises(PilotError):
                web_preview.annual_payload(ROOT,self.registry,self.data,self.raw)

    def test_legacy_source_explicitly_reports_no_annual_history(self):
        with patch.object(annual_workflow,'run',side_effect=AssertionError('No history available')):
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

    def test_incomplete_execution_and_foreign_artifacts_cannot_export_a_trace(self):
        for mutate in [lambda s,r:r.update(status='incomplete'),
                       lambda s,r:r['nodes']['History']['artifact'].update(producer_run_id='foreign')]:
            spec,run=copy.deepcopy(self.execution); mutate(spec,run)
            with patch.object(annual_workflow,'run',return_value=(spec,run)),self.assertRaises(PilotError):
                web_preview.annual_payload(ROOT,self.registry,self.data,self.raw)

    def test_private_context_cannot_be_projected_even_when_graph_claims_completion(self):
        spec,run=copy.deepcopy(self.execution); spec['context']['private_note']='must not export'
        trace=workflow_trace.project(*self.execution)
        with patch.object(annual_workflow,'run',return_value=(spec,run)),patch.object(workflow_trace,'project',return_value=trace),self.assertRaises(PilotError):
            web_preview.annual_payload(ROOT,self.registry,self.data,self.raw)
