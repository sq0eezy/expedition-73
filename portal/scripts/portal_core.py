"""Small, read-only content checks and shared state-token rendering."""
from __future__ import annotations

import datetime as dt
import html
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

STATUSES = {"Proposed", "Validating", "Implemented", "Verified", "Deferred", "Rejected"}
TOKEN = re.compile(r"\{\{\s*([a-zA-Z_][a-zA-Z_0-9]*)\s*\}\}")
TOKENS = {"project_name", "project_description", "current_status", "current_updated", "current_phase"}


def load_state(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("CURRENT_STATE.md needs YAML front matter.")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError("Unclosed state front matter.") from exc
    data = yaml.safe_load("\n".join(lines[1:end]))
    if not isinstance(data, dict):
        raise ValueError("State metadata must be a mapping.")
    if not isinstance(data.get("status"), str) or data["status"] not in STATUSES:
        raise ValueError("Unsupported current status.")
    phase = data.get("phase")
    if not isinstance(phase, str) or not phase.strip() or "\n" in phase or len(phase) > 180:
        raise ValueError("State phase must be a non-empty single line, at most 180 characters.")
    updated = str(data.get("updated", ""))
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", updated):
        raise ValueError("State updated must be an ISO YYYY-MM-DD date.")
    dt.date.fromisoformat(updated)
    return {"status": data["status"], "updated": updated, "phase": phase.strip()}


def render_tokens(markdown: str, config: dict, state: dict[str, str]) -> str:
    values = {
        "project_name": config["site_name"],
        "project_description": config.get("site_description") or "",
        "current_status": state["status"],
        "current_updated": state["updated"],
        "current_phase": state["phase"],
    }

    def replace(match: re.Match) -> str:
        key = match.group(1)
        if key not in values:
            raise ValueError("Unknown portal token: " + key)
        value = html.escape(str(values[key]).replace("\r", " ").replace("\n", " "), quote=True)
        # Escape Markdown operators as well as HTML when values enter prose.
        return re.sub(r"([\\*_{}\[\]#!|])", r"\\\1", value)

    return TOKEN.sub(replace, markdown)


def strip_fences(text: str) -> str:
    out, active, width = [], None, 0
    for line in text.splitlines():
        marker = re.match(r"^\s*([~]{3,}|[`]{3,})", line)
        if marker:
            current = marker.group(1)
            if active is None:
                active, width = current[0], len(current)
            elif current[0] == active and len(current) >= width:
                active = None
            continue
        if active is None:
            out.append(line)
    return "\n".join(out)


def local_target(source: Path, raw: str, docs: Path) -> Path | None:
    parsed = urlsplit(raw)
    if parsed.scheme in {"http", "https", "mailto"} or raw.startswith("//") or not parsed.path:
        return None
    if parsed.scheme:
        raise ValueError("Unsupported link scheme: " + parsed.scheme)
    target = (source.parent / unquote(parsed.path)).resolve()
    try:
        target.relative_to(docs.resolve())
    except ValueError as exc:
        raise ValueError("Link leaves published docs: " + raw) from exc
    if target.is_dir():
        target = target / "index.md"
    elif not target.suffix:
        target = target.with_suffix(".md")
    return target


def nav_targets(config_text: str) -> list[str]:
    # Parse only the ordinary nav block, not MkDocs' Python extension tags.
    match = re.search(r"(?ms)^nav:\s*\n(.*?)(?=^\S|\Z)", config_text)
    if not match:
        raise ValueError("mkdocs.yml needs an explicit nav block.")
    data = yaml.safe_load(match.group(1))
    targets: list[str] = []

    def visit(value: object) -> None:
        if isinstance(value, str):
            targets.append(value)
        elif isinstance(value, list):
            for entry in value:
                visit(entry)
        elif isinstance(value, dict):
            for entry in value.values():
                visit(entry)
        else:
            raise ValueError("Unsupported navigation entry.")

    visit(data)
    return targets


def check_content(root: Path) -> list[str]:
    docs = root / "docs"
    errors: list[str] = []
    for name in ("index.md", "CURRENT_STATE.md", "PROJECT_CONTEXT.md", "DOCUMENTATION_MAP.md"):
        if not (docs / name).is_file():
            errors.append("Missing canonical document: " + name)
    if (docs / "CURRENT_STATE.md").is_file():
        try:
            load_state(docs / "CURRENT_STATE.md")
        except (ValueError, yaml.YAMLError) as exc:
            errors.append(str(exc))
    config = root / "mkdocs.yml"
    if not config.is_file():
        errors.append("Missing mkdocs.yml")
    else:
        try:
            for raw in nav_targets(config.read_text(encoding="utf-8")):
                target = local_target(docs / "index.md", raw, docs)
                if target is not None and not target.is_file():
                    errors.append("Missing nav target: " + raw)
        except (ValueError, yaml.YAMLError) as exc:
            errors.append(str(exc))
    for source in sorted(docs.rglob("*.md")):
        if not source.resolve().is_relative_to(docs.resolve()):
            errors.append("Document leaves docs through a symlink: " + str(source))
            continue
        text = strip_fences(source.read_text(encoding="utf-8"))
        for key in TOKEN.findall(text):
            if key not in TOKENS:
                errors.append(source.name + ": unknown token " + key)
        markdown_links = re.findall(r'!?\[[^\]]*\]\(\s*(?:<([^>]+)>|([^\s)]+))', text)
        raw_links = [a or b for a, b in markdown_links]
        raw_links += re.findall(r'(?:href|src)\s*=\s*["\x27]([^"\x27]+)["\x27]', text)
        for raw in raw_links:
            try:
                target = local_target(source, raw, docs)
                if target is not None and not target.is_file():
                    errors.append(str(source.relative_to(docs)) + ": missing link " + raw)
            except ValueError as exc:
                errors.append(str(source.relative_to(docs)) + ": " + str(exc))
    return errors
