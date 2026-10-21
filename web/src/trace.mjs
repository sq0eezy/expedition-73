// A public projection of a build-time execution, never a live scheduler.
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
