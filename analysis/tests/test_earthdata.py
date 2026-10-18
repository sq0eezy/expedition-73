"""No live tokens or requests. Authentication handling and metadata boundaries."""
import io
import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError, URLError

from expedition73.earthdata import METADATA_URL, NoRedirect, probe, read_token
from expedition73 import earthdata
from expedition73.power import PilotError

TOKEN = "synthetic-test-token-not-a-live-secret"
XML = b'<Dataset xmlns="http://xml.opendap.org/ns/DAP/4.0#"><Float32 name="FRLAND"><Dim size="1"/><Dim size="361"/><Dim size="576"/></Float32></Dataset>'


class EarthdataTests(unittest.TestCase):
    def response(self, raw):
        response = MagicMock();response.status = 200;response.read.return_value = raw
        response.__enter__.return_value = response
        opener = MagicMock();opener.open.return_value = response
        return opener

    def test_direct_metadata_request_and_sanitized_report(self):
        opener = self.response(XML)
        with patch("expedition73.earthdata.build_opener", return_value=opener):
            raw, report = probe(TOKEN)
        request = opener.open.call_args.args[0]
        self.assertEqual(request.full_url, METADATA_URL)
        self.assertEqual(request.get_header("Authorization"), "Bearer " + TOKEN)
        self.assertEqual(raw, XML)
        self.assertFalse(report["mask_values_retrieved"])
        self.assertFalse(report["credentials_persisted"])
        self.assertNotIn(TOKEN, str(report))
        self.assertEqual(report["surface_variables_found"][0]["dimensions"][1], {"size": "361"})

    def test_no_token_is_forwarded_on_redirect_even_to_same_host(self):
        for url in ("https://evil.example/", "http://opendap.earthdata.nasa.gov/", "https://opendap.earthdata.nasa.gov/other"):
            with self.subTest(url=url), self.assertRaises(PilotError):
                NoRedirect().redirect_request(None, None, 302, "redirect", {}, url)

    def test_auth_and_network_errors_do_not_expose_reflected_credentials(self):
        for failure in [HTTPError(METADATA_URL, 401, TOKEN, {}, io.BytesIO(TOKEN.encode())),
                        HTTPError(METADATA_URL, 403, TOKEN, {}, None), URLError(TOKEN), TimeoutError(TOKEN)]:
            opener = MagicMock();opener.open.side_effect = failure
            with patch("expedition73.earthdata.build_opener", return_value=opener), self.assertRaises(PilotError) as caught:
                probe(TOKEN)
            self.assertNotIn(TOKEN, str(caught.exception))

    def test_html_wrong_xml_oversize_or_reflected_token_are_not_saved(self):
        for raw in [b'<html>Login</html>', b'not xml', b'x' * 1000001, XML.replace(b'FRLAND', TOKEN.encode())]:
            with patch("expedition73.earthdata.build_opener", return_value=self.response(raw)), self.assertRaises(PilotError):
                probe(TOKEN)

    def test_token_must_not_contain_header_whitespace(self):
        for token in ("", "bad\r\nHeader", "bad token", "é", "bad\x7f", "x" * 16385):
            with patch("expedition73.earthdata.build_opener") as network, self.assertRaises(PilotError):
                probe(token)
            network.assert_not_called()

    def test_hidden_prompt_has_no_echo_fallback(self):
        from getpass import GetPassWarning
        with patch("expedition73.earthdata.getpass", return_value=TOKEN):
            self.assertEqual(read_token(), TOKEN)
        for error in (GetPassWarning("no hidden input"), EOFError(), KeyboardInterrupt()):
            with patch("expedition73.earthdata.getpass", side_effect=error), self.assertRaises(PilotError):
                read_token()

    def test_attributes_are_not_mistaken_for_numeric_surface_arrays(self):
        xml = b'<Dataset><Attribute name="FRLAND" type="String"><Value>description</Value></Attribute></Dataset>'
        with patch("expedition73.earthdata.build_opener", return_value=self.response(xml)):
            _, report = probe(TOKEN)
        self.assertEqual(report["surface_variables_found"], [])
        self.assertIn("FRLAND", report["surface_variables_missing"])

    def test_saved_token_loads_without_prompt_or_changing_process_environment(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / '.env'
            path.write_text('# local\nEARTHDATA_TOKEN="' + TOKEN + '"\nOTHER_SETTING=leave-alone\n', encoding='utf-8')
            before = dict(os.environ)
            with patch.object(earthdata, 'read_token') as prompt:
                self.assertEqual(earthdata.get_token(env_path=path), (TOKEN, True))
            prompt.assert_not_called()
            self.assertEqual(dict(os.environ), before)

    def test_no_saved_token_uses_hidden_entry_without_creating_file(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / '.env'
            with patch.object(earthdata, 'read_token', return_value=TOKEN):
                self.assertEqual(earthdata.get_token(env_path=path), (TOKEN, False))
            self.assertFalse(path.exists())

    def test_explicit_save_and_replacement_preserve_unrelated_settings(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / '.env'
            original = '# keep comment\nOTHER_SETTING=keep-value\nexport EARTHDATA_TOKEN=old-test-token\n'
            path.write_text(original, encoding='utf-8')
            with patch.object(earthdata, 'read_token', return_value=TOKEN) as prompt:
                self.assertEqual(earthdata.get_token(env_path=path, save=True), (TOKEN, True))
            prompt.assert_called_once_with(persist=True)
            self.assertEqual(path.read_text(encoding='utf-8'), '# keep comment\nOTHER_SETTING=keep-value\nEARTHDATA_TOKEN=' + TOKEN + '\n')
            self.assertEqual(list(Path(temp).iterdir()), [path])

    def test_create_token_file_and_keep_final_unterminated_setting(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / '.env'
            earthdata.save_token(path, TOKEN)
            self.assertEqual(earthdata.load_saved_token(path), TOKEN)
            path.write_text('UNRELATED=keep', encoding='utf-8')
            earthdata.save_token(path, TOKEN)
            self.assertTrue(path.read_text(encoding='utf-8').startswith('UNRELATED=keep\n'))
            path.write_text('EARTHDATA_TOKEN=\n', encoding='utf-8')
            self.assertIsNone(earthdata.load_saved_token(path))

    def test_invalid_or_duplicate_env_entry_never_echoes_contents_or_prompts(self):
        for content in ('EARTHDATA_TOKEN=bad secret value\n', 'EARTHDATA_TOKEN=a\nEARTHDATA_TOKEN=b\n'):
            with self.subTest(content=content), tempfile.TemporaryDirectory() as temp:
                path = Path(temp) / '.env'
                path.write_text(content, encoding='utf-8')
                with patch.object(earthdata, 'read_token') as prompt, self.assertRaises(PilotError) as caught:
                    earthdata.get_token(env_path=path)
                self.assertNotIn(content, str(caught.exception))
                self.assertNotIn('bad secret value', str(caught.exception))
                prompt.assert_not_called()
                self.assertEqual(path.read_text(encoding='utf-8'), content)

    def test_failed_atomic_replace_preserves_original_and_cleans_temp_file(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / '.env'
            path.write_text('UNRELATED=keep\n', encoding='utf-8')
            with patch.object(earthdata.os, 'replace', side_effect=OSError(TOKEN)), self.assertRaises(PilotError) as caught:
                earthdata.save_token(path, TOKEN)
            self.assertNotIn(TOKEN, str(caught.exception))
            self.assertEqual(path.read_text(encoding='utf-8'), 'UNRELATED=keep\n')
            self.assertEqual(list(Path(temp).iterdir()), [path])

    def test_oversized_or_non_utf8_env_rejected_without_contents(self):
        for raw in (b'x' * (earthdata.MAX_ENV_BYTES + 1), b'\xff\xfe'):
            with tempfile.TemporaryDirectory() as temp:
                path = Path(temp) / '.env'
                path.write_bytes(raw)
                with self.assertRaises(PilotError):
                    earthdata.load_saved_token(path)

    def test_symlink_env_does_not_read_or_overwrite_target(self):
        # Mock the link check: Windows may require privileges to create symlinks.
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / '.env'
            with patch.object(Path, 'is_symlink', return_value=True):
                with self.assertRaises(PilotError):
                    earthdata.load_saved_token(path)
                with self.assertRaises(PilotError):
                    earthdata.save_token(path, TOKEN)
            self.assertFalse(path.exists())

    def test_cli_saves_before_403_and_next_run_reuses_file_with_honest_report(self):
        script = Path(__file__).resolve().parents[1] / 'scripts/check_earthdata_access.py'
        spec = importlib.util.spec_from_file_location('metadata_env_test', script)
        helper = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(helper)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / 'analysis'
            root.mkdir()
            log, error = io.StringIO(), io.StringIO()
            with patch.object(helper, 'ROOT', root), patch.object(earthdata, 'read_token', return_value=TOKEN), \
                    patch.object(helper, 'probe', side_effect=PilotError('Earthdata HTTP 403')), \
                    redirect_stdout(log), redirect_stderr(error):
                self.assertEqual(helper.main(['--save-token']), 1)
            self.assertEqual(earthdata.load_saved_token(root.parent / '.env'), TOKEN)
            self.assertFalse((root / 'artifacts').exists())
            report = {'credentials_persisted': False, 'surface_variables_found': []}
            with patch.object(helper, 'ROOT', root), patch.object(earthdata, 'read_token') as prompt, \
                    patch.object(helper, 'probe', return_value=(XML, report)), redirect_stdout(log):
                self.assertEqual(helper.main([]), 0)
            prompt.assert_not_called()
            output = next((root / 'artifacts').iterdir())
            saved = json.loads((output / 'access-report.json').read_text(encoding='utf-8'))
            self.assertTrue(saved['credentials_persisted'])
            self.assertNotIn(TOKEN, log.getvalue() + error.getvalue())
            self.assertNotIn(TOKEN, json.dumps(saved))


if __name__ == "__main__":
    unittest.main()
