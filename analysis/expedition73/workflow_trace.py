"""Validated public execution trace, with stable definition ids rather than run ids."""
from . import workflow
from .power import PilotError


def project(spec, report):
    """Inspect actual artifacts before exporting a small, credential-free view.

    Definition fingerprints identify the declared calculation and source snapshot;
    they are not artifact identities or a claim of scientific correctness.
    """
    snapshot = workflow.plan(spec, report.get("target"))
    order = snapshot["order"]
    context_hash = workflow._hash(snapshot["context"])
    expected_events = [{"node": name, "status": "waiting"} for name in order]
    expected_events += [{"node": name, "status": status} for name in order
                        for status in ("running", "completed")]
    if (report.get("status") != "completed" or report.get("order") != order
            or report.get("context") != snapshot["context"]
            or report.get("scientific_validation") != "not_performed"
            or set(report.get("nodes", {})) != set(order)
            or report.get("events") != expected_events):
        raise PilotError("Public trace requires one complete, consistent execution.")
    rows = []
    for name in order:
        node, record = snapshot["nodes"][name], report["nodes"][name]
        if record.get("status") != "completed" or record.get("fingerprint") != snapshot["fingerprints"][name]:
            raise PilotError("Trace definition and executed node differ.")
        body = workflow.validate_artifact(record["artifact"])
        inputs = {alias: report["nodes"][link["node"]]["artifact"] for alias, link in node["inputs"].items()}
        expected = {"schema_version": workflow.VERSION, "producer_run_id": report["run_id"],
                    "node_id": name, "operation": node["operation"], "operation_version": node["version"],
                    "context_sha256": context_hash, "parameters": node["parameters"],
                    "contract": node["output_contract"],
                    "inputs": {alias: artifact["artifact_id"] for alias, artifact in inputs.items()},
                    "lineage": workflow.input_lineage(inputs, context_hash)}
        if any(body.get(key) != value for key, value in expected.items()):
            raise PilotError("Trace artifact does not belong to the declared execution and lineage.")
        # Never copy arbitrary context, parameters, payloads, paths or run ids.
        rows.append({"id": name, "operation": node["operation"], "operation_version": node["version"],
                     "status": "completed", "executions": 1,
                     "definition_fingerprint": snapshot["fingerprints"][name],
                     "output_contract": dict(node["output_contract"]),
                     "inputs": [{"alias": alias, "node": link["node"], "output": "result",
                                 "definition_fingerprint": snapshot["fingerprints"][link["node"]]}
                                for alias, link in sorted(node["inputs"].items())]})
    return {"schema_version": "0.1.0", "output_type": "recorded_workflow_trace",
            "execution_status": "completed", "scientific_validation": "not_performed",
            "identity_kind": "workflow_plan_fingerprint", "context_sha256": context_hash,
            "target": report["target"], "nodes": rows}
