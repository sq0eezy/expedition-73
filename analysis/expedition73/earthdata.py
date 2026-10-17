"""A single, fixed-host metadata probe. Tokens are supplied only in memory."""
from __future__ import annotations

import hashlib
import re
import warnings
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from getpass import GetPassWarning, getpass
from http.client import HTTPException
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener

from .masking import COMPONENTS
from .power import PilotError

METADATA_URL = ("https://opendap.earthdata.nasa.gov/collections/C1276812819-GES_DISC/granules/"
                "M2C0NXASM.5.12.4%3AMERRA2_101.const_2d_asm_Nx.00000000.nc4.dmr.xml")
MAX_METADATA_BYTES = 1_000_000


def valid_token(token):
    return isinstance(token, str) and len(token) <= 16384 and re.fullmatch(r"[A-Za-z0-9\-._~+/]+=*", token) is not None


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # Hyrax supports direct bearer access. Never forward the token to an
        # identity provider, a signed storage URL, HTTP or an unexpected host.
        raise PilotError("Earthdata redirected the request; no token was forwarded. Check application authorization.")


def read_token():
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", GetPassWarning)
            token = getpass("Earthdata token (hidden; not saved): ")
    except (GetPassWarning, EOFError, KeyboardInterrupt) as exc:
        raise PilotError("Token entry cancelled or hidden input unavailable; run in an interactive terminal.") from exc
    token = token.strip()
    if not valid_token(token):
        raise PilotError("Token must be a single nonempty ASCII value; no request was made.")
    return token


def probe(token):
    if not valid_token(token):
        raise PilotError("Invalid token format; no request was made.")
    request = Request(METADATA_URL, headers={"Authorization": "Bearer " + token,
                                          "User-Agent": "Expedition73/0.1 metadata-probe"})
    try:
        with build_opener(NoRedirect()).open(request, timeout=40) as response:
            if response.status != 200:
                raise PilotError("Unexpected metadata status; no result was saved.")
            raw = response.read(MAX_METADATA_BYTES + 1)
    except HTTPError as exc:
        if exc.code == 401:
            message = "Earthdata HTTP 401: check token validity and application authorization."
        elif exc.code == 403:
            message = "Earthdata HTTP 403: check authorization for the NASA Hyrax data application."
        else:
            message = f"Earthdata HTTP {exc.code}; metadata was not saved."
        raise PilotError(message) from None
    except (URLError, TimeoutError, OSError, HTTPException, ValueError):
        # Do not expose response bodies, cookies, request headers or exception
        # text which could reflect a credential. No automatic retry.
        raise PilotError("Earthdata network request failed or timed out; metadata was not saved.") from None
    if len(raw) > MAX_METADATA_BYTES:
        raise PilotError("Metadata exceeds the size limit; no result was saved.")
    if token.encode("ascii") in raw:
        raise PilotError("Unexpected credential reflection in response; no result was saved.")
    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        raise PilotError("Response is not valid DMR XML; no result was saved.") from None
    if root.tag.rsplit("}", 1)[-1] != "Dataset":
        raise PilotError("Response is not a DMR Dataset; no result was saved.")
    variables = []
    for element in root.iter():
        kind = element.tag.rsplit("}", 1)[-1]
        if element.attrib.get("name") in COMPONENTS and kind in {"Float32", "Float64", "Int16", "Int32", "Int64", "UInt16", "UInt32", "UInt64", "Byte", "Int8", "UInt8"}:
            variables.append({"name": element.attrib["name"], "type": kind,
                              "dimensions": [dict(child.attrib) for child in element
                                             if child.tag.rsplit("}", 1)[-1] == "Dim"]})
    found = {v["name"] for v in variables}
    report = {"schema_version": "0.1.0", "status": "metadata_received", "http_status": 200,
              "request_url": METADATA_URL, "retrieved_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
              "response_sha256": hashlib.sha256(raw).hexdigest(), "response_bytes": len(raw),
              "surface_variables_found": variables,
              "surface_variables_missing": [name for name in COMPONENTS if name not in found],
              "mask_values_retrieved": False, "credentials_persisted": False,
              "scope": "metadata_access_only_not_scientific_validation"}
    return raw, report
