"""Synthetic dependency scheduling, isolation and invalidation; no NASA claims."""
import copy
import io
import json
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from expedition73.__main__ import main
from expedition73.power import PilotError
from expedition73.workflow import Operation, compare_snapshot, execute, input_lineage, plan, validate_artifact
from expedition73.workflow_demo import request, registry


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.spec = request()
        self.calls = []
        self.operations = registry(self.calls)

    def run_graph(self):
        return execute(self.spec, "C", self.operations)

    def test_diamond_runs_a_once_and_c_uses_the_same_a_as_b(self):
        report = self.run_graph()
        a, b, c = [report['nodes'][name]['artifact'] for name in 'ABC']
        self.assertEqual(self.calls, ['A', 'B', 'C'])
        self.assertEqual(report['status'], 'completed')
        self.assertEqual(c['value']['value'], 12)
        self.assertEqual(b['inputs']['base'], a['artifact_id'])
        self.assertEqual(c['inputs']['base'], a['artifact_id'])
        self.assertEqual(c['lineage'], {'A': a['artifact_id'], 'B': b['artifact_id']})
        for artifact in (a, b, c):
            validate_artifact(artifact)
        self.assertEqual([e['status'] for e in report['events'] if e['node'] == 'C'],
                         ['waiting', 'running', 'completed'])

    def test_only_target_dependencies_run_and_node_declaration_order_is_irrelevant(self):
        self.spec['nodes'].reverse()
        unused = copy.deepcopy(self.spec['nodes'][-1])
        unused['id'] = 'Unused'
        self.spec['nodes'].append(unused)
        report = self.run_graph()
        self.assertEqual(report['order'], ['A', 'B', 'C'])
        self.assertEqual(self.calls, ['A', 'B', 'C'])

    def assert_preflight_error(self):
        with self.assertRaises(PilotError):
            self.run_graph()
        self.assertEqual(self.calls, [])

    def test_cycle_rejected_before_any_callback(self):
        self.spec['nodes'][0]['inputs']['cycle'] = copy.deepcopy(self.spec['nodes'][2]['inputs']['base'])
        self.spec['nodes'][0]['inputs']['cycle']['node'] = 'C'
        self.assert_preflight_error()

    def test_self_dependency_rejected(self):
        self.spec['nodes'][1]['inputs']['base']['node'] = 'B'
        self.assert_preflight_error()

    def test_missing_producer_duplicate_ids_and_unknown_target_rejected(self):
        original = copy.deepcopy(self.spec)
        self.spec['nodes'][1]['inputs']['base']['node'] = 'Absent'
        self.assert_preflight_error()
        self.spec = original
        self.spec['nodes'].append(copy.deepcopy(self.spec['nodes'][0]))
        self.assert_preflight_error()
        with self.assertRaises(PilotError):
            plan(original, 'Absent')

    def test_wrong_input_type_unit_version_or_port_rejected_before_a_runs(self):
        for field, value in [('type', 'different_type'), ('unit', 'degC'), ('schema_version', '0.2.0')]:
            self.spec = request()
            self.spec['nodes'][2]['inputs']['derived']['contract'][field] = value
            with self.subTest(field=field):
                self.assert_preflight_error()
        self.spec = request()
        self.spec['nodes'][1]['inputs']['base']['output'] = 'absent_port'
        self.assert_preflight_error()

    def test_missing_registry_operation_and_wrong_version_rejected_upfront(self):
        self.operations.pop('double')
        self.assert_preflight_error()
        self.operations = registry(self.calls)
        self.spec['nodes'][1]['version'] = '0.2.0'
        self.assert_preflight_error()

    def test_b_failure_keeps_a_and_blocks_c_without_exception_text(self):
        def fail(inputs, parameters, context):
            self.calls.append('B')
            raise RuntimeError('private debug string must not appear in output')
        old = self.operations['double']
        self.operations['double'] = Operation(old.version, old.contract, fail, old.validate)
        report = self.run_graph()
        self.assertEqual(self.calls, ['A', 'B'])
        self.assertEqual(report['nodes']['A']['status'], 'completed')
        self.assertEqual(report['nodes']['B']['reason'], 'COMPUTE_FAILED')
        self.assertEqual(report['nodes']['C']['blocked_by'], ['B'])
        self.assertEqual(report['status'], 'incomplete')
        self.assertNotIn('private debug', json.dumps(report))

    def test_failed_a_blocks_b_and_c(self):
        def fail(inputs, parameters, context):
            self.calls.append('A')
            raise PilotError('deliberate failure')
        old = self.operations['constant']
        self.operations['constant'] = Operation(old.version, old.contract, fail, old.validate)
        report = self.run_graph()
        self.assertEqual(self.calls, ['A'])
        self.assertEqual(report['nodes']['B']['status'], 'blocked')
        self.assertEqual(report['nodes']['C']['status'], 'blocked')

    def test_independent_sibling_completes_after_another_sibling_fails(self):
        sibling = copy.deepcopy(self.spec['nodes'][0])
        sibling['id'] = 'D'
        self.spec['nodes'].append(sibling)
        link = copy.deepcopy(self.spec['nodes'][2]['inputs']['base'])
        link['node'] = 'D'
        self.spec['nodes'][2]['inputs']['independent'] = link
        old = self.operations['double']
        def fail(*args):
            raise RuntimeError('deliberate B failure')
        self.operations['double'] = Operation(old.version, old.contract, fail, old.validate)
        report = self.run_graph()
        self.assertEqual(report['nodes']['D']['status'], 'completed')
        self.assertEqual(report['nodes']['C']['status'], 'blocked')

    def test_output_validator_and_nonfinite_output_block_consumers(self):
        for value in ({'wrong': 4}, {'value': float('nan')}, {'value': True}, {1: 4}):
            old = self.operations['constant']
            self.operations['constant'] = Operation(old.version, old.contract, lambda *args: value, old.validate)
            report = self.run_graph()
            with self.subTest(value=value):
                self.assertEqual(report['nodes']['A']['reason'], 'OUTPUT_INVALID')
                self.assertEqual(report['nodes']['C']['status'], 'blocked')

    def test_consumers_cannot_mutate_upstream_artifacts_or_snapshot(self):
        old = self.operations['double']
        def mutate(inputs, parameters, context):
            value = inputs['base']['value']['value']
            inputs['base']['value']['value'] = -999
            context['region_id'] = 'wrong-region'
            self.spec['nodes'][0]['parameters']['value'] = 99
            return {'value': 2 * value}
        self.operations['double'] = Operation(old.version, old.contract, mutate, old.validate)
        report = self.run_graph()
        self.assertEqual(report['nodes']['A']['artifact']['value']['value'], 4)
        self.assertEqual(report['nodes']['C']['artifact']['value']['value'], 12)
        self.assertEqual(report['context']['region_id'], 'synthetic-region')

    def test_changed_a_marks_a_b_c_stale_and_preserves_old_snapshot(self):
        first = self.run_graph()
        old_copy = copy.deepcopy(first)
        self.spec['nodes'][0]['parameters']['value'] = 7
        self.assertEqual(compare_snapshot(first, self.spec, 'C'), {'A': 'stale', 'B': 'stale', 'C': 'stale'})
        second = self.run_graph()
        self.assertEqual(first, old_copy)
        self.assertEqual(second['nodes']['C']['artifact']['value']['value'], 21)
        self.assertNotEqual(first['run_id'], second['run_id'])
        self.assertNotEqual(first['nodes']['A']['artifact']['artifact_id'], second['nodes']['A']['artifact']['artifact_id'])

    def test_unchanged_and_independent_configuration_changes_have_correct_staleness(self):
        first = self.run_graph()
        self.assertEqual(set(compare_snapshot(first, self.spec, 'C').values()), {'current'})
        self.spec['nodes'][1]['parameters']['declared_method_revision'] = 'demo-2'
        self.assertEqual(compare_snapshot(first, self.spec, 'C'), {'A': 'current', 'B': 'stale', 'C': 'stale'})

    def test_region_period_or_source_revision_changes_do_not_reuse_old_scope(self):
        first = self.run_graph()
        for field in ['region_id', 'period', 'source_revision']:
            self.spec = request()
            self.spec['context'][field] = 'different'
            with self.subTest(field=field):
                self.assertEqual(set(compare_snapshot(first, self.spec, 'C').values()), {'stale'})
        second = self.run_graph()
        with self.assertRaises(PilotError):
            input_lineage({'old': first['nodes']['A']['artifact']}, second['nodes']['A']['artifact']['context_sha256'])

    def test_old_a_and_new_b_cannot_be_combined_even_in_the_same_context(self):
        first = self.run_graph()
        self.spec['nodes'][0]['parameters']['value'] = 7
        second = self.run_graph()
        old_a, new_b = first['nodes']['A']['artifact'], second['nodes']['B']['artifact']
        with self.assertRaises(PilotError):
            input_lineage({'base': old_a, 'derived': new_b}, old_a['context_sha256'])

    def test_tampered_artifact_is_rejected_by_id(self):
        artifact = self.run_graph()['nodes']['A']['artifact']
        artifact['value']['value'] = 123
        with self.assertRaises(PilotError):
            validate_artifact(artifact)

    def test_graph_is_data_not_arbitrary_python_or_shell_code(self):
        self.spec['nodes'][0]['operation'] = '__import__(os).system'
        self.assert_preflight_error()

    def test_cli_demo_is_synthetic_and_shows_two_consistent_generations(self):
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(['demo-workflow']), 0)
        report = json.loads(output.getvalue())
        self.assertEqual(report['data_origin'], 'synthetic_fixture')
        self.assertEqual(report['first_call_order'], ['A', 'B', 'C'])
        self.assertEqual(report['first_run']['nodes']['C']['artifact']['value']['value'], 12)
        self.assertEqual(report['second_run']['nodes']['C']['artifact']['value']['value'], 21)
        self.assertEqual(set(report['after_A_parameter_change'].values()), {'stale'})

    def test_saved_demo_artifacts_retain_consistent_input_ids(self):
        path = Path(__file__).resolve().parents[1] / 'examples/workflow-demo.json'
        report = json.loads(path.read_text(encoding='utf-8'))
        self.assertEqual(report['data_origin'], 'synthetic_fixture')
        for run_name, expected in [('first_run', 12), ('second_run', 21)]:
            saved = report[run_name]
            a, b, c = [saved['nodes'][name]['artifact'] for name in 'ABC']
            self.assertEqual(c['value']['value'], expected)
            self.assertEqual(input_lineage({'a': a, 'b': b}, a['context_sha256']), c['lineage'])
            for artifact in (a, b, c):
                validate_artifact(artifact)


if __name__ == '__main__':
    unittest.main()
