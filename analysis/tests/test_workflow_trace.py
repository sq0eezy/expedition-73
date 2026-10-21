"""Public trace must be derived from one actual, validated execution."""
import copy
import json
from pathlib import Path
import unittest

from expedition73 import surface_workflow, workflow, workflow_trace
from expedition73.power import PilotError
from expedition73.workflow_demo import request, registry


class WorkflowTraceTests(unittest.TestCase):
    def setUp(self):
        self.spec = request()
        self.report = workflow.execute(self.spec, 'C', registry([]))

    def resign(self, report, name):
        artifact = report['nodes'][name]['artifact']
        artifact.pop('artifact_id')
        artifact['artifact_id'] = 'sha256:' + workflow._hash(artifact)

    def test_repeated_execution_has_same_public_identity_but_distinct_artifacts(self):
        other = workflow.execute(self.spec, 'C', registry([]))
        self.assertNotEqual(self.report['run_id'], other['run_id'])
        self.assertEqual(workflow_trace.project(self.spec, self.report), workflow_trace.project(self.spec, other))

    def test_arbitrary_private_parameters_context_and_payloads_are_not_exported(self):
        self.spec['context']['local_path'] = 'PRIVATE_LOCAL_PATH'
        self.spec['nodes'][0]['parameters']['credential'] = 'PRIVATE_PARAMETER'
        report = workflow.execute(self.spec, 'C', registry([]))
        raw = json.dumps(workflow_trace.project(self.spec, report))
        for private in ['PRIVATE_', report['run_id'], 'artifact_id', 'value_sha256']:
            self.assertNotIn(private, raw)

    def test_stale_fingerprint_incomplete_duplicate_execution_or_bad_context_is_rejected(self):
        for kind in ['fingerprint', 'status', 'events', 'context', 'order', 'extra']:
            report = copy.deepcopy(self.report)
            if kind == 'fingerprint': report['nodes']['B']['fingerprint'] = '0' * 64
            if kind == 'status': report['status'] = 'incomplete'
            if kind == 'events': report['events'].append({'node': 'A', 'status': 'completed'})
            if kind == 'context': report['context']['other'] = True
            if kind == 'order': report['order'].reverse()
            if kind == 'extra': report['nodes']['Unrelated'] = {}
            with self.subTest(kind=kind), self.assertRaises(PilotError):
                workflow_trace.project(self.spec, report)

    def test_payload_tampering_is_rejected(self):
        self.report['nodes']['C']['artifact']['value']['value'] = -123
        with self.assertRaises(PilotError): workflow_trace.project(self.spec, self.report)

    def test_old_run_input_is_rejected_even_after_consumer_is_resigned(self):
        old = workflow.execute(self.spec, 'C', registry([]))
        self.report['nodes']['C']['artifact']['inputs']['base'] = old['nodes']['A']['artifact']['artifact_id']
        self.resign(self.report, 'C')
        with self.assertRaises(PilotError): workflow_trace.project(self.spec, self.report)

    def test_wrong_lineage_or_run_or_contract_cannot_be_hidden_by_new_artifact_hash(self):
        for field, value in [('lineage', {}), ('producer_run_id', 'old-run'), ('contract', {}), ('parameters', {'extra': 1})]:
            report = copy.deepcopy(self.report)
            report['nodes']['C']['artifact'][field] = value
            self.resign(report, 'C')
            with self.subTest(field=field), self.assertRaises(PilotError): workflow_trace.project(self.spec, report)

    def test_actual_a_and_b_traces_preserve_eight_links_and_single_shared_temperature(self):
        root = Path(__file__).resolve().parents[1]
        for region in ('a', 'b'):
            spec, report = surface_workflow.run(root / f'examples/{region}-window-2024', root / f'examples/{region}-surface-fractions')
            trace = workflow_trace.project(spec, report)
            self.assertEqual(len(trace['nodes']), 5)
            self.assertEqual(sum(len(n['inputs']) for n in trace['nodes']), 8)
            self.assertTrue(all(n['executions'] == 1 for n in trace['nodes']))
            nodes = {n['id']: n for n in trace['nodes']}
            for name in ['Fractions', 'Land', 'LandIce', 'Sensitivity']:
                link = next(i for i in nodes[name]['inputs'] if i['node'] == 'Temperature')
                self.assertEqual(link['definition_fingerprint'], nodes['Temperature']['definition_fingerprint'])
