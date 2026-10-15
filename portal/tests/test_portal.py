"""Real toolkit tests. No claims about a user's application or LLM obedience."""
import argparse
import hashlib
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import portal
from portal_core import check_content, load_state, local_target, nav_targets, render_tokens, strip_fences

STATE = '---\nstatus: Proposed\nupdated: "2026-10-05"\nphase: Awaiting context\n---\n# State\n'


class StateTests(unittest.TestCase):
    def test_valid_date_and_shared_state(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "CURRENT_STATE.md"
            path.write_text(STATE, encoding="utf-8")
            state = load_state(path)
            self.assertEqual(state["updated"], "2026-10-05")
            config = {"site_name": "Sample", "site_description": "Example"}
            self.assertEqual(render_tokens("{{ current_status }} / {{ current_phase }}", config, state),
                             "Proposed / Awaiting context")
            path.write_text(STATE.replace("Proposed", "Verified"), encoding="utf-8")
            self.assertEqual(load_state(path)["status"], "Verified")

    def test_invalid_metadata_is_rejected(self):
        variants = [
            STATE.replace("---\n", "", 1), STATE.replace("Proposed", "Done"),
            STATE.replace("2026-10-05", "2026-02-30"),
            STATE.replace("2026-10-05", "yesterday"),
            STATE.replace("Awaiting context", ""),
            STATE.replace("status: Proposed", "status: [Proposed]"),
            "---\nstatus: Proposed\n",
        ]
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "state.md"
            for text in variants:
                with self.subTest(text=text):
                    path.write_text(text, encoding="utf-8")
                    with self.assertRaises(ValueError):
                        load_state(path)

    def test_dynamic_text_is_escaped(self):
        state = {"status": "Proposed", "updated": "2026-10-05", "phase": "<script>alert(1)</script>"}
        rendered = render_tokens("{{ project_name }} / {{ current_phase }}",
                                 {"site_name": '<img src=x onerror="bad">'}, state)
        self.assertNotIn("<script>", rendered)
        self.assertNotIn("<img", rendered)
        self.assertIn("&lt;script&gt;", rendered)

    def test_unknown_token_is_not_silently_kept(self):
        with self.assertRaises(ValueError):
            render_tokens("{{ nonexistent }}", {"site_name": "Example"},
                          {"status": "Proposed", "updated": "2026-10-05", "phase": "Setup"})


class LinkTests(unittest.TestCase):
    def test_nav_parses_nested_structure(self):
        self.assertEqual(nav_targets("site_name: X\nnav:\n  - Home: index.md\n  - Group:\n      - State: CURRENT_STATE.md\n"),
                         ["index.md", "CURRENT_STATE.md"])

    def test_invalid_navigation_rejected(self):
        for text in ("site_name: X", "nav:\n  - 123\n"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                nav_targets(text)

    def test_internal_routes_and_external_links(self):
        with tempfile.TemporaryDirectory() as temp:
            docs = Path(temp) / "docs"
            (docs / "product").mkdir(parents=True)
            (docs / "product/index.md").write_text("# Product", encoding="utf-8")
            source = docs / "index.md"
            self.assertEqual(local_target(source, "product/", docs), docs / "product/index.md")
            self.assertEqual(local_target(source, "CURRENT_STATE/#next", docs), docs / "CURRENT_STATE.md")
            for raw in ("https://example.com", "mailto:test@example.com", "#section", "//example.com"):
                self.assertIsNone(local_target(source, raw, docs))

    def test_private_paths_and_script_links_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            docs = Path(temp) / "docs"
            docs.mkdir()
            for raw in ("../.portal/preferences.md", "%2e%2e/.portal/x", "javascript:alert(1)", "file:///private.txt"):
                with self.subTest(raw=raw), self.assertRaises(ValueError):
                    local_target(docs / "index.md", raw, docs)

    def test_fenced_examples_are_not_links(self):
        text = "# Real\n~~~sh\n[example](missing.md)\n~~~\n[real](index.md)\n"
        self.assertNotIn("missing.md", strip_fences(text))
        self.assertIn("[real](index.md)", strip_fences(text))


class ContentTests(unittest.TestCase):
    def create_fixture(self, root):
        docs = root / "docs"
        docs.mkdir()
        (docs / "CURRENT_STATE.md").write_text(STATE, encoding="utf-8")
        for name in ("index.md", "PROJECT_CONTEXT.md", "DOCUMENTATION_MAP.md"):
            (docs / name).write_text("# Example\n[State](CURRENT_STATE.md)\n", encoding="utf-8")
        (root / "mkdocs.yml").write_text("site_name: Test\nnav:\n  - Home: index.md\n", encoding="utf-8")
        return docs

    def test_known_good_content_and_read_only(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.create_fixture(root)
            before = {str(p): p.read_bytes() for p in root.rglob("*") if p.is_file()}
            self.assertEqual(check_content(root), [])
            after = {str(p): p.read_bytes() for p in root.rglob("*") if p.is_file()}
            self.assertEqual(before, after)

    def test_broken_markdown_html_nav_token_and_private_link(self):
        variants = {
            "markdown": "[Broken](missing.md)",
            "html": '<a href="missing/">Broken</a>',
            "image": '<img src="assets/missing.png">',
            "token": "{{ unknown_field }}",
            "private": "[Private](../.portal/user-preferences.local.md)",
        }
        for label, text in variants.items():
            with self.subTest(label=label), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                docs = self.create_fixture(root)
                (docs / "index.md").write_text(text, encoding="utf-8")
                self.assertTrue(check_content(root))
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.create_fixture(root)
            (root / "mkdocs.yml").write_text("nav:\n  - Missing: missing.md\n", encoding="utf-8")
            self.assertTrue(any("nav target" in e for e in check_content(root)))

    def test_missing_canonical_document(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            docs = self.create_fixture(root)
            (docs / "PROJECT_CONTEXT.md").unlink()
            self.assertTrue(any("PROJECT_CONTEXT" in e for e in check_content(root)))

    def test_actual_template_passes_without_mutation(self):
        before = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT / "docs").rglob("*") if p.is_file()}
        self.assertEqual(check_content(ROOT), [])
        after = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT / "docs").rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_private_preferences_stay_outside_docs(self):
        self.assertIn(".portal/", (ROOT / ".gitignore").read_text(encoding="utf-8"))
        self.assertIn("@AGENTS.md", (ROOT / "CLAUDE.md").read_text(encoding="utf-8"))
        self.assertIn("user-preferences.local.md", (ROOT / "AGENTS.md").read_text(encoding="utf-8"))
        self.assertFalse(any("user-preferences" in str(p).lower() for p in (ROOT / "docs").rglob("*")))


class CliTests(unittest.TestCase):
    def test_windows_and_posix_environment_paths(self):
        root = Path("sample")
        self.assertEqual(portal.environment_python(root, "win32"), root / ".venv/Scripts/python.exe")
        self.assertEqual(portal.environment_python(root, "linux"), root / ".venv/bin/python")
        self.assertEqual(portal.environment_python(root, "darwin"), root / ".venv/bin/python")

    def test_missing_environment_has_actionable_error(self):
        with tempfile.TemporaryDirectory() as temp, self.assertRaises(portal.PortalError):
            portal.require_environment(Path(temp))

    def test_invalid_port_rejected(self):
        for value in ("0", "1023", "65536", "abc"):
            with self.subTest(value=value), self.assertRaises(argparse.ArgumentTypeError):
                portal.port_number(value)
        self.assertEqual(portal.port_number("8001"), 8001)

    def test_server_is_loopback_and_no_shell_interpolation(self):
        args = portal.mkdocs_command(Path("folder with spaces/python"), "serve", 8001, True)
        self.assertIn("127.0.0.1:8001", args)
        self.assertIn("--strict", args)
        self.assertIn("--open", args)
        self.assertEqual(args[0], str(Path("folder with spaces/python")))

    def test_failed_commands_raise(self):
        with patch("portal.subprocess.run") as run:
            run.return_value.returncode = 7
            with self.assertRaises(portal.PortalError):
                portal.run_command(["python", "-m", "mkdocs"], ROOT)
            self.assertFalse(run.call_args.kwargs.get("shell", False))


if __name__ == "__main__":
    unittest.main()
