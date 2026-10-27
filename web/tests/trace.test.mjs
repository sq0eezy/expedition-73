import { test } from 'node:test';
import assert from 'node:assert/strict';
import { traceGraph, validateAnnualWorkflow } from '../src/trace.mjs';
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';

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

const canonical = (x) => JSON.stringify(x && typeof x === 'object' ? Array.isArray(x) ? x.map((v)=>JSON.parse(canonical(v))) : Object.fromEntries(Object.keys(x).sort().map((k)=>[k,JSON.parse(canonical(x[k]))])) : x);
const digest = (s) => createHash('sha256').update(s).digest('hex');
function annualFixture(id='a') {
  const audit=JSON.parse(readFileSync(new URL(`../../analysis/examples/${id}-annual-weighting-audit.json`,import.meta.url),'utf8'));
  const directory=new URL(`../../analysis/examples/${id}-history-2001-2024/`,import.meta.url);
  const parent=Object.fromEntries(['history.json','request.json','result.json'].map((name)=>[name,digest(readFileSync(new URL(name,directory)))]));
  const context={scope:'candidate_annual_weighting',region:{region_id:audit.region.id,candidate_bbox:audit.region.candidate_bbox,candidate_window_version:audit.region.candidate_window_version},period:{start_year:2001,end_year:2024},source_files_sha256:{history:parent,annual_sources:audit.provenance.annual_sources}};
  const context_json=canonical(context), historyContract={type:'verified_annual_weighting_inputs',schema_version:'0.1.0',unit:'degC'}, annualContract={type:'candidate_annual_weighting_audit',schema_version:'0.1.0',unit:'degC'};
  const definitions=[{id:'History',operation:'ReplayRecordedHistory',version:'0.1.0',parameters:{},inputs:{},output_contract:historyContract},{id:'AnnualWeighting',operation:'CompareAnnualWeighting',version:'0.1.0',parameters:{},inputs:{history:{node:'History',output:'result',contract:historyContract}},output_contract:annualContract}];
  const nodes=[];
  for(const [i,d] of definitions.entries()) {
    const fingerprint=digest(`{"context":${context_json},"dependencies":${canonical(i?{history:nodes[0].definition_fingerprint}:{})},"node":${canonical(d)}}`);
    nodes.push({id:d.id,operation:d.operation,operation_version:d.version,status:'completed',executions:1,definition_fingerprint:fingerprint,output_contract:d.output_contract,inputs:i?[{alias:'history',node:'History',output:'result',definition_fingerprint:nodes[0].definition_fingerprint}]:[]});
  }
  return {id:audit.region.id,audit,workflow:{context_json,trace:{schema_version:'0.1.0',output_type:'recorded_workflow_trace',execution_status:'completed',scientific_validation:'not_performed',identity_kind:'workflow_plan_fingerprint',context_sha256:digest(context_json),target:'AnnualWeighting',nodes}}};
}

test('annual trace binds two known operations to actual region and annual source identities',async()=>{
  for(const id of ['a','b']) {const entry=annualFixture(id); assert.equal(await validateAnnualWorkflow(entry),entry.workflow.trace); assert.equal(traceGraph(entry.workflow.trace).edges.length,1);}
});
test('annual trace cannot be swapped between regions or shifted to another source period',async()=>{
  const a=annualFixture(), b=annualFixture('b'); a.workflow=b.workflow; await assert.rejects(validateAnnualWorkflow(a));
  const entry=annualFixture(); const c=JSON.parse(entry.workflow.context_json); c.period.start_year=2002; entry.workflow.context_json=canonical(c); entry.workflow.trace.context_sha256=digest(entry.workflow.context_json); await assert.rejects(validateAnnualWorkflow(entry));
});
test('annual trace rejects changed source hash, private context and unsupported wrappers',async()=>{
  for(const mutate of [(e)=>{const c=JSON.parse(e.workflow.context_json);c.source_files_sha256.history['result.json']='f'.repeat(64);e.workflow.context_json=canonical(c);},(e)=>{const c=JSON.parse(e.workflow.context_json);c.private_note='do not export';e.workflow.context_json=canonical(c);},(e)=>e.workflow.extra='private',(e)=>e.workflow.context_json='x'.repeat(100001)]) {
    const entry=annualFixture();mutate(entry);await assert.rejects(validateAnnualWorkflow(entry));
  }
});
test('annual operation contract, version, fingerprint, edge and completion are all checked',async()=>{
  for(const mutate of [(t)=>t.nodes[1].operation_version='0.2.0',(t)=>t.nodes[0].definition_fingerprint='f'.repeat(64),(t)=>t.nodes[1].inputs[0].alias='other',(t)=>t.nodes[1].output_contract.unit='K',(t)=>t.nodes[1].operation='DifferentAnnualMethod',(t)=>t.execution_status='incomplete']) {
    const entry=annualFixture();mutate(entry.workflow.trace);await assert.rejects(validateAnnualWorkflow(entry));
  }
});
test('missing annual execution metadata never becomes a completed trace',async()=>{
  for(const entry of [{}, {id:'A',audit:annualFixture().audit}, {...annualFixture(),workflow:null}]) await assert.rejects(validateAnnualWorkflow(entry));
});
