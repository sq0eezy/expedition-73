"""Local dependency experiment; no NASA operations, persistence or parallel jobs.

Graph declarations are data. Only explicitly registered Python callbacks run.
Each node produces one result port. Every execution starts a fresh snapshot.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from uuid import uuid4

from .power import PilotError, validate_schema

VERSION = "0.1.0"


def _clone(value):
    try:
        encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
        copied = json.loads(encoded)
        if copied != value:
            raise ValueError()
        return copied
    except (ValueError, TypeError, RecursionError):
        raise PilotError("Workflow values must be finite JSON with string object keys.") from None


def _hash(value):
    return hashlib.sha256(json.dumps(_clone(value), sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=False, allow_nan=False).encode()).hexdigest()


@dataclass(frozen=True)
class Operation:
    version: str
    contract: dict
    compute: object
    validate: object


def plan(spec, target):
    spec = _clone(spec)
    validate_schema(spec, "workflow-request.schema.json")
    nodes = {node["id"]: node for node in spec["nodes"]}
    if len(nodes) != len(spec["nodes"]):
        raise PilotError("Workflow node ids must be unique.")
    if target not in nodes:
        raise PilotError("Workflow target is absent.")
    for node in nodes.values():
        for link in node["inputs"].values():
            producer = nodes.get(link["node"])
            if producer is None:
                raise PilotError("Workflow refers to a missing producer.")
            if link["contract"] != producer["output_contract"]:
                raise PilotError("Input and output type/version/unit contracts differ; conversion is not implicit.")
    order, state = [], {}

    def visit(name):
        if state.get(name) == "active":
            raise PilotError("Workflow dependency cycle detected; no computation started.")
        if state.get(name) == "done":
            return
        state[name] = "active"
        for dependency in sorted({link["node"] for link in nodes[name]["inputs"].values()}):
            visit(dependency)
        state[name] = "done"
        order.append(name)

    # Reject invalid cycles even in unused declarations, then select the closure.
    for name in sorted(nodes):
        visit(name)
    order.clear()
    state.clear()
    visit(target)
    fingerprints = {}
    for name in order:
        node = nodes[name]
        fingerprints[name] = _hash({"context": spec["context"], "node": node,
                                   "dependencies": {alias: fingerprints[link["node"]]
                                                    for alias, link in node["inputs"].items()}})
    return {"context": spec["context"], "nodes": nodes, "order": order, "fingerprints": fingerprints}


def validate_artifact(artifact):
    copied = _clone(artifact)
    identifier = copied.pop("artifact_id", None)
    if identifier != "sha256:" + _hash(copied):
        raise PilotError("Workflow artifact content does not match its immutable id.")
    if copied.get("value_sha256") != _hash(copied.get("value")):
        raise PilotError("Workflow payload hash mismatch.")
    return copied


def input_lineage(inputs, context_sha256):
    """Merge ancestor identities, rejecting old/new versions of shared producers."""
    lineage = {}
    for artifact in inputs.values():
        body = validate_artifact(artifact)
        if body["context_sha256"] != context_sha256:
            raise PilotError("Input belongs to a different context snapshot.")
        ancestors = dict(body["lineage"])
        if body["node_id"] in ancestors:
            raise PilotError("An artifact cannot list itself as an ancestor.")
        ancestors[body["node_id"]] = artifact["artifact_id"]
        for node_id, identifier in ancestors.items():
            if node_id in lineage and lineage[node_id] != identifier:
                raise PilotError("Conflicting versions of a shared upstream artifact.")
            lineage[node_id] = identifier
    return lineage


def execute(spec, target, registry):
    snapshot = plan(spec, target)
    # Validate and capture executable definitions before any callback can run.
    operations = {}
    for name in snapshot["order"]:
        node = snapshot["nodes"][name]
        operation = registry.get(node["operation"])
        if (not isinstance(operation, Operation) or operation.version != node["version"]
                or operation.contract != node["output_contract"]
                or not callable(operation.compute) or not callable(operation.validate)):
            raise PilotError("Missing operation or incompatible registered version/contract.")
        operations[name] = operation
    run_id = str(uuid4())
    context_hash = _hash(snapshot["context"])
    results, events = {}, []
    for name in snapshot["order"]:
        results[name] = {"status": "waiting", "fingerprint": snapshot["fingerprints"][name]}
        events.append({"node": name, "status": "waiting"})
    for name in snapshot["order"]:
        node = snapshot["nodes"][name]
        failed_inputs = sorted({link["node"] for link in node["inputs"].values()
                                if results[link["node"]]["status"] != "completed"})
        if failed_inputs:
            results[name].update(status="blocked", reason="UPSTREAM_UNAVAILABLE", blocked_by=failed_inputs)
            events.append({"node": name, "status": "blocked"})
            continue
        inputs = {alias: results[link["node"]]["artifact"] for alias, link in node["inputs"].items()}
        lineage = input_lineage(inputs, context_hash)
        operation = operations[name]
        results[name]["status"] = "running"
        events.append({"node": name, "status": "running"})
        try:
            # All callback arguments are independent copies: mutating a consumer
            # cannot alter another consumer's artifact, context or parameters.
            value = operation.compute(_clone(inputs), _clone(node["parameters"]), _clone(snapshot["context"]))
        except Exception:
            results[name].update(status="failed", reason="COMPUTE_FAILED")
            events.append({"node": name, "status": "failed"})
            continue
        try:
            value = _clone(value)
            operation.validate(_clone(value), _clone(snapshot["context"]))
        except Exception:
            results[name].update(status="failed", reason="OUTPUT_INVALID")
            events.append({"node": name, "status": "failed"})
            continue
        body = {"schema_version": VERSION, "producer_run_id": run_id, "node_id": name,
                "operation": node["operation"], "operation_version": node["version"],
                "context_sha256": context_hash, "parameters": _clone(node["parameters"]),
                "contract": _clone(node["output_contract"]),
                "inputs": {alias: artifact["artifact_id"] for alias, artifact in inputs.items()},
                "lineage": lineage, "value": value, "value_sha256": _hash(value)}
        artifact = {**body, "artifact_id": "sha256:" + _hash(body)}
        results[name].update(status="completed", artifact=artifact)
        events.append({"node": name, "status": "completed"})
    return {"schema_version": VERSION, "output_type": "technical_workflow_run", "run_id": run_id,
            "target": target, "context": snapshot["context"], "order": snapshot["order"],
            "status": "completed" if results[target]["status"] == "completed" else "incomplete",
            "nodes": results, "events": events, "scientific_validation": "not_performed"}


def compare_snapshot(previous, spec, target):
    """Explicit comparison of declarations; no live monitor/cache or source probing."""
    current = plan(spec, target)
    return {name: "removed" if name not in current["fingerprints"] else
            "unavailable" if record["status"] != "completed" else
            "current" if record["fingerprint"] == current["fingerprints"][name] else "stale"
            for name, record in previous["nodes"].items()}
