import { test } from 'node:test';
import assert from 'node:assert/strict';
import { traceGraph } from '../src/trace.mjs';

const fingerprint = (n) => String(n).repeat(64);
function fixture() {
  const node = (id, n, inputs = []) => ({ id, operation: id, operation_version: '0.1.0', status: 'completed', executions: 1, definition_fingerprint: fingerprint(n), output_contract: { type: 'test_result', schema_version: '0.1.0', unit: 'degC' }, inputs: inputs.map(([alias, node, n]) => ({ alias, node, output: 'result', definition_fingerprint: fingerprint(n) })) });
  return { schema_version: '0.1.0', output_type: 'recorded_workflow_trace', execution_status: 'completed', scientific_validation: 'not_performed', identity_kind: 'workflow_plan_fingerprint', context_sha256: fingerprint(0), target: 'C', nodes: [node('A', 1), node('B', 2, [['base', 'A', 1]]), node('C', 3, [['base', 'A', 1], ['derived', 'B', 2]])] };
}
test('shared producer is one selectable node with all actual links', () => {
  const graph = traceGraph(fixture()); assert.equal(graph.nodes.length, 3); assert.equal(graph.edges.length, 3);
  assert.deepEqual(graph.edges, [{ from: 'A', to: 'B', alias: 'base' }, { from: 'A', to: 'C', alias: 'base' }, { from: 'B', to: 'C', alias: 'derived' }]);
  assert.ok(graph.nodes[0].x < graph.nodes[1].x && graph.nodes[1].x < graph.nodes[2].x);
});
test('old identities, missing producer, bad port and duplicate aliases fail closed', () => {
  for (const mutate of [(t) => t.nodes[2].inputs[0].definition_fingerprint = fingerprint(9), (t) => t.nodes[2].inputs[0].node = 'Missing', (t) => t.nodes[2].inputs[0].output = 'other', (t) => t.nodes[2].inputs[1].alias = 'base']) {
    const t = fixture(); mutate(t); assert.throws(() => traceGraph(t));
  }
});
test('cycles, wrong order and duplicate nodes fail closed', () => {
  const cycle = fixture(); cycle.nodes[0].inputs.push(cycle.nodes[2].inputs[1]); assert.throws(() => traceGraph(cycle));
  const order = fixture(); order.nodes.reverse(); assert.throws(() => traceGraph(order));
  const duplicate = fixture(); duplicate.nodes.push(duplicate.nodes[0]); assert.throws(() => traceGraph(duplicate));
});
test('incomplete or repeated execution and scientific claims are rejected', () => {
  for (const mutate of [(t) => t.execution_status = 'incomplete', (t) => t.nodes[0].executions = 2, (t) => t.scientific_validation = 'approved', (t) => t.identity_kind = 'artifact_id', (t) => t.nodes[0].output_contract.unit = '']) {
    const t = fixture(); mutate(t); assert.throws(() => traceGraph(t));
  }
});
test('only the target dependency closure is displayed', () => {
  const t = fixture(); t.target = 'B'; assert.throws(() => traceGraph(t));
});
