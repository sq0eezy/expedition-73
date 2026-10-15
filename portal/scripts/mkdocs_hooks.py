"""Reuse one state source for Home and Control Center; never rewrite docs."""
from pathlib import Path

from mkdocs.exceptions import PluginError

from portal_core import load_state, render_tokens


def on_page_markdown(markdown, page, config, **kwargs):
    try:
        state = load_state(Path(config["docs_dir"]) / "CURRENT_STATE.md")
        return render_tokens(markdown, config, state)
    except (ValueError, OSError) as exc:
        raise PluginError(str(exc)) from exc
