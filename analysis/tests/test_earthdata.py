"""No live tokens or requests. Authentication handling and metadata boundaries."""
import io
import unittest
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError, URLError

from expedition73.earthdata import METADATA_URL, NoRedirect, probe, read_token
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


if __name__ == "__main__":
    unittest.main()
