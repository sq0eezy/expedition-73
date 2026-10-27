// A public projection of a build-time execution, never a live scheduler.
const canonical = (value) => JSON.stringify(value && typeof value === "object" ?
  Array.isArray(value) ? value.map((v) => JSON.parse(canonical(v))) : Object.fromEntries(Object.keys(value).sort().map((key) => [key,JSON.parse(canonical(value[key]))])) : value);
const sha256 = async (text) => [...new Uint8Array(await crypto.subtle.digest("SHA-256",new TextEncoder().encode(text)))].map((n)=>n.toString(16).padStart(2,"0")).join("");

// Call after validating the annual audit against the monthly catalog.
export async function validateAnnualWorkflow(entry) {
  const a = entry?.audit, w = entry?.workflow;
  const fail = () => { throw Error("Annual execution does not match its recorded sources or definitions"); };
  if (!w || Object.keys(w).sort().join() !== "context_json,trace" || typeof w.context_json !== "string" || w.context_json.length > 100_000) fail();
  const context = JSON.parse(w.context_json), parent = context?.source_files_sha256?.history;
  if (!parent || Object.keys(parent).sort().join() !== "history.json,request.json,result.json" ||
      Object.values(parent).some((v)=>typeof v !== "string" || !/^[a-f0-9]{64}$/.test(v)) || parent["result.json"] !== a.provenance.source_history_result_sha256) fail();
  const expected = { scope:"candidate_annual_weighting", region:{region_id:entry.id,candidate_bbox:a.region.candidate_bbox,candidate_window_version:a.region.candidate_window_version},
    period:{start_year:Number(a.time.start),end_year:Number(a.time.end)},source_files_sha256:{history:parent,annual_sources:a.provenance.annual_sources} };
  if (a.region.id !== entry.id || canonical(context) !== canonical(expected)) fail();
  const trace = w.trace, graph = traceGraph(trace);
  if (trace.context_sha256 !== await sha256(w.context_json) || trace.target !== "AnnualWeighting" || graph.nodes.length !== 2 || graph.edges.length !== 1) fail();
  const historyContract = {type:"verified_annual_weighting_inputs",schema_version:"0.1.0",unit:"degC"};
  const annualContract = {type:"candidate_annual_weighting_audit",schema_version:"0.1.0",unit:"degC"};
  const definitions = [
    {id:"History",operation:"ReplayRecordedHistory",version:"0.1.0",parameters:{},inputs:{},output_contract:historyContract},
    {id:"AnnualWeighting",operation:"CompareAnnualWeighting",version:"0.1.0",parameters:{},inputs:{history:{node:"History",output:"result",contract:historyContract}},output_contract:annualContract},
  ];
  const fingerprints = [];
  for (const [i,definition] of definitions.entries()) {
    const dependencies = i ? {history:fingerprints[0]} : {};
    // Keep Python's exact context number spelling; known node definitions contain no floats.
    const fingerprint = await sha256(`{"context":${w.context_json},"dependencies":${canonical(dependencies)},"node":${canonical(definition)}}`);
    const node = trace.nodes[i], inputs = i ? [{alias:"history",node:"History",output:"result",definition_fingerprint:fingerprints[0]}] : [];
    if (node.id !== definition.id || node.operation !== definition.operation || node.operation_version !== definition.version ||
        node.definition_fingerprint !== fingerprint || canonical(node.output_contract) !== canonical(definition.output_contract) || canonical(node.inputs) !== canonical(inputs)) fail();
    fingerprints.push(fingerprint);
  }
  return trace;
}

export function traceGraph(trace, compact = false) {
  const hash = (s) => typeof s === "string" && /^[a-f0-9]{64}$/.test(s);
  const id = (s) => typeof s === "string" && /^[A-Za-z][A-Za-z0-9_-]{0,63}$/.test(s);
  const version = (s) => typeof s === "string" && /^\d+\.\d+\.\d+$/.test(s);
  if (!trace || trace.schema_version !== "0.1.0" || trace.output_type !== "recorded_workflow_trace" || trace.execution_status !== "completed" || trace.scientific_validation !== "not_performed" || trace.identity_kind !== "workflow_plan_fingerprint" || !hash(trace.context_sha256) || !Array.isArray(trace.nodes) || !trace.nodes.length || trace.nodes.length > 64) throw Error("Invalid execution trace");
  const seen = new Map(), edges = [], levels = new Map();
  for (const node of trace.nodes) {
    const c = node.output_contract;
    if (!id(node.id) || seen.has(node.id) || !id(node.operation) || !version(node.operation_version) || node.status !== "completed" || node.executions !== 1 || !hash(node.definition_fingerprint) || !c || typeof c.type !== "string" || !c.type || typeof c.unit !== "string" || !c.unit || !version(c.schema_version) || !Array.isArray(node.inputs) || node.inputs.length > 32) throw Error("Invalid executed node");
    let level = 0; const aliases = new Set();
    for (const input of node.inputs) {
      const producer = seen.get(input.node);
      if (!producer || input.output !== "result" || !id(input.alias) || aliases.has(input.alias) || input.definition_fingerprint !== producer.definition_fingerprint) throw Error("Invalid execution dependency");
      aliases.add(input.alias); level = Math.max(level, levels.get(input.node) + 1);
      edges.push({ from: input.node, to: node.id, alias: input.alias });
    }
    seen.set(node.id, node); levels.set(node.id, level);
  }
  if (!seen.has(trace.target) || trace.nodes.at(-1).id !== trace.target) throw Error("Invalid trace target");
  const closure = new Set();
  const visit = (name) => { if (closure.has(name)) return; closure.add(name); for (const input of seen.get(name).inputs) visit(input.node); };
  visit(trace.target);
  if (closure.size !== seen.size) throw Error("Unrelated execution nodes");
  const maxLevel = Math.max(...levels.values());
  const nodes = trace.nodes.map((node) => {
    const peers = trace.nodes.filter((other) => levels.get(other.id) === levels.get(node.id));
    const index = peers.indexOf(node), level = levels.get(node.id);
    return { ...node, x: compact ? 20 + (index + 0.5) * 360 / peers.length - 80 : 20 + level * 210,
      y: compact ? 50 + level * 150 : 110 + (index + 0.5) * 200 / peers.length };
  });
  return { nodes, edges, width: compact ? 400 : 200 + maxLevel * 210, height: compact ? 100 + maxLevel * 150 : 360 };
}
