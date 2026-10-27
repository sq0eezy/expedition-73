"""Frozen recorded history -> annual candidates through the dependency engine."""
from __future__ import annotations

import copy
from pathlib import Path

from . import annual_weighting, history, regional, surface_workflow
from .power import PilotError, loads, validate_schema
from .workflow import Operation, execute

VERSION = "0.1.0"
HISTORY = {"type": "verified_annual_weighting_inputs", "schema_version": VERSION, "unit": "degC"}
ANNUAL = {"type": "candidate_annual_weighting_audit", "schema_version": VERSION, "unit": "degC"}


def build(directory):
    """Capture fixed files once. Callbacks neither reopen files nor use NASA/token."""
    directory = Path(directory)
    parent = {name: surface_workflow._read(directory, name, limit=8_000_000 if name == "result.json" else 2_000_000)
              for name in ("request.json", "history.json", "result.json")}
    config = loads(parent["request.json"])
    requests = history.plan(config)
    sources = [history.capture(directory / f"year-{request['start_year']}") for request in requests]
    parent_hashes = surface_workflow._hashes(parent)
    entries = [{"year": request["start_year"], "files_sha256": surface_workflow._hashes(files)}
               for request, files in zip(requests, sources, strict=True)]
    context = {"scope": "candidate_annual_weighting", "region": surface_workflow._identity(config),
               "period": {"start_year": config["start_year"], "end_year": config["end_year"]},
               "source_files_sha256": {"history": parent_hashes, "annual_sources": entries}}

    def check_context(actual):
        # Declared source hashes/periods cannot be relabelled after build().
        if actual != context:
            raise PilotError("Annual workflow context differs from its captured sources.")

    def frozen_annual_inputs():
        # Interpret result payloads only after assemble has validated every source.
        return [annual_weighting._annual_input(request["start_year"], loads(files["result.json"]))
                for request, files in zip(requests, sources, strict=True)]

    def replay(inputs, parameters, actual):
        check_context(actual)
        if inputs or parameters:
            raise PilotError("History replay has no configurable input overrides.")
        manifest, verified = history.assemble(config, sources)
        if loads(parent["history.json"]) != manifest:
            raise PilotError("History manifest differs from frozen annual source hashes.")
        stored = loads(parent["result.json"])
        validate_schema(stored, "window-history.schema.json")
        if not regional._same_result(stored, verified):
            raise PilotError("History differs from frozen raw-source replay.")
        return {"history": verified, "annual_inputs": frozen_annual_inputs(),
                "source_history_result_sha256": parent_hashes["result.json"]}

    def validate_history(value, actual):
        check_context(actual)
        validate_schema(value["history"], "window-history.schema.json")
        if (set(value) != {"history", "annual_inputs", "source_history_result_sha256"}
                or value["source_history_result_sha256"] != parent_hashes["result.json"]
                or value["history"]["provenance"]["annual_sources"] != entries
                or not regional._same_result(value["history"], loads(parent["result.json"]))
                or value["annual_inputs"] != frozen_annual_inputs()):
            raise PilotError("History output is not bound to the captured annual inputs.")
        support = value["history"]["spatial_support"]
        if support["kind"] != "unmasked_rectangular_window" or support["mask"] != "none":
            raise PilotError("Annual workflow supports only unmasked candidate windows.")

    def summarize(inputs, parameters, actual):
        check_context(actual)
        if parameters or set(inputs) != {"history"}:
            raise PilotError("Annual candidates require exactly the declared history input.")
        value = inputs["history"]["value"]
        validate_history(value, actual)
        return annual_weighting._summarize_verified(
            value["history"], value["annual_inputs"], value["source_history_result_sha256"])

    def validate_annual(value, actual):
        check_context(actual)
        validate_schema(value, "annual-weighting.schema.json")
        if (value["method"] != annual_weighting.METHOD
                or value["weighting_definitions"] != annual_weighting.DEFINITIONS
                or value["provenance"]["source_history_result_sha256"] != parent_hashes["result.json"]
                or value["provenance"]["annual_sources"] != entries
                or value["region"]["id"] != config["region_id"]
                or [row["year"] for row in value["series"]] != [r["start_year"] for r in requests]):
            raise PilotError("Annual output differs from source identity, candidate methods or period.")

    nodes = [
        {"id": "History", "operation": "ReplayRecordedHistory", "version": VERSION, "parameters": {},
         "inputs": {}, "output_contract": dict(HISTORY)},
        {"id": "AnnualWeighting", "operation": "CompareAnnualWeighting", "version": VERSION, "parameters": {},
         "inputs": {"history": {"node": "History", "output": "result", "contract": dict(HISTORY)}},
         "output_contract": dict(ANNUAL)},
    ]
    registry = {"ReplayRecordedHistory": Operation(VERSION, dict(HISTORY), replay, validate_history),
                "CompareAnnualWeighting": Operation(VERSION, dict(ANNUAL), summarize, validate_annual)}
    return {"schema_version": VERSION, "context": copy.deepcopy(context), "nodes": nodes}, registry


def run(directory):
    spec, registry = build(directory)
    return spec, execute(spec, "AnnualWeighting", registry)
