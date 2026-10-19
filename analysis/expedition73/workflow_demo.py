"""Synthetic A -> B, A+B -> C experiment. No NASA data or credentials."""
from __future__ import annotations

from .power import PilotError, finite
from .workflow import Operation, compare_snapshot, execute

CONTRACT = {"type": "synthetic_scalar", "schema_version": "0.1.0", "unit": "1"}


def request(value=4):
    def link(name):
        return {"node": name, "output": "result", "contract": dict(CONTRACT)}
    def node(name, operation, inputs, parameters):
        return {"id": name, "operation": operation, "version": "0.1.0", "inputs": inputs,
                "parameters": parameters, "output_contract": dict(CONTRACT)}
    return {"schema_version": "0.1.0",
            "context": {"region_id": "synthetic-region", "boundary_version": "demo-1",
                        "period": "synthetic-step-1", "source_revision": "fabricated-1"},
            "nodes": [node("A", "constant", {}, {"value": value}),
                      node("B", "double", {"base": link("A")}, {}),
                      node("C", "combine", {"base": link("A"), "derived": link("B")}, {})]}


def registry(calls):
    def compute_a(inputs, parameters, context):
        calls.append("A")
        return {"value": parameters["value"]}
    def compute_b(inputs, parameters, context):
        calls.append("B")
        return {"value": 2 * inputs["base"]["value"]["value"]}
    def compute_c(inputs, parameters, context):
        calls.append("C")
        return {"value": inputs["base"]["value"]["value"] + inputs["derived"]["value"]["value"]}
    def validate(value, context):
        if not isinstance(value, dict) or set(value) != {"value"}:
            raise PilotError("Synthetic demo needs exactly one scalar.")
        finite(value["value"], "synthetic scalar")
    return {name: Operation("0.1.0", dict(CONTRACT), callback, validate)
            for name, callback in [("constant", compute_a), ("double", compute_b), ("combine", compute_c)]}


def run():
    calls = []
    original = request()
    first = execute(original, "C", registry(calls))
    changed = request(value=7)
    stale = compare_snapshot(first, changed, "C")
    second_calls = []
    second = execute(changed, "C", registry(second_calls))
    return {"schema_version": "0.1.0", "data_origin": "synthetic_fixture",
            "scope": "dependency_engine_experiment_not_scientific_result",
            "first_call_order": calls, "first_run": first,
            "after_A_parameter_change": stale, "second_call_order": second_calls, "second_run": second}
