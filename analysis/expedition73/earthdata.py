"""Fixed NASA access; hidden entry or explicitly saved local .env credential."""
from __future__ import annotations

import hashlib
import os
import re
import tempfile
import warnings
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from getpass import GetPassWarning, getpass
from http.client import HTTPException
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener

from .masking import COMPONENTS
from .power import PilotError

METADATA_URL = ("https://opendap.earthdata.nasa.gov/collections/C1276812819-GES_DISC/granules/"
                "M2C0NXASM.5.12.4%3AMERRA2_101.const_2d_asm_Nx.00000000.nc4.dmr.xml")
MAX_METADATA_BYTES = 1_000_000
SUBSET_PREFIX = METADATA_URL.removesuffix(".dmr.xml") + ".dap.nc4?dap4.ce="
TOKEN_KEY = "EARTHDATA_TOKEN"
MAX_ENV_BYTES = 65_536


def valid_token(token):
    return isinstance(token, str) and len(token) <= 16384 and re.fullmatch(r"[A-Za-z0-9\-._~+/]+=*", token) is not None


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # Hyrax supports direct bearer access. Never forward the token to an
        # identity provider, a signed storage URL, HTTP or an unexpected host.
        raise PilotError("Earthdata redirected the request; no token was forwarded. Check application authorization.")


def read_token(*, persist=False):
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", GetPassWarning)
            token = getpass("Earthdata token (hidden; save to local .env): " if persist else
                            "Earthdata token (hidden; not saved): ")
    except (GetPassWarning, EOFError, KeyboardInterrupt) as exc:
        raise PilotError("Token entry cancelled or hidden input unavailable; run in an interactive terminal.") from exc
    token = token.strip()
    if not valid_token(token):
        raise PilotError("Token must be a single nonempty ASCII value; no request was made.")
    return token


def _env_lines(path):
    # Only the explicitly named project .env, never profile files or a search
    # through parent directories. Do not print file contents on any failure.
    try:
        if path.is_symlink():
            raise PilotError("Project .env must be a regular local file, not a symlink.")
        if not path.exists():
            return []
        with path.open("rb") as stream:
            raw = stream.read(MAX_ENV_BYTES + 1)
        if len(raw) > MAX_ENV_BYTES:
            raise PilotError("Project .env exceeds the size limit.")
        return raw.decode("utf-8-sig").splitlines(keepends=True)
    except (OSError, UnicodeError):
        raise PilotError("Could not read project .env as UTF-8; no contents were displayed.") from None


def _token_lines(lines):
    positions = [i for i, line in enumerate(lines)
                 if re.match(r"^\s*(?:export\s+)?EARTHDATA_TOKEN\s*=", line)]
    if len(positions) > 1:
        raise PilotError("Duplicate EARTHDATA_TOKEN entries in project .env; keep a single entry.")
    return positions


def load_saved_token(path):
    lines = _env_lines(Path(path))
    positions = _token_lines(lines)
    if not positions:
        return None
    value = lines[positions[0]].split("=", 1)[1].strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    if not value:
        return None
    if not valid_token(value):
        raise PilotError("Invalid EARTHDATA_TOKEN in project .env; replace it with --save-token.")
    return value


def save_token(path, token):
    """Replace only our key; unrelated settings survive. Never echo the value."""
    if not valid_token(token):
        raise PilotError("Invalid token format; project .env was not changed.")
    path = Path(path)
    lines = _env_lines(path)
    positions = _token_lines(lines)
    entry = TOKEN_KEY + "=" + token + "\n"
    if positions:
        lines[positions[0]] = entry
    else:
        if lines and not lines[-1].endswith(("\r", "\n")):
            lines[-1] += "\n"
        lines.append(entry)
    temporary = None
    try:
        # mkstemp uses mode 0600 on POSIX. Windows uses the user's directory ACL.
        descriptor, name = tempfile.mkstemp(prefix=".earthdata-", suffix=".tmp", dir=path.parent)
        temporary = Path(name)
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as stream:
            stream.write("".join(lines))
        os.replace(temporary, path)
    except OSError:
        raise PilotError("Could not save token to project .env; no credential was displayed.") from None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def get_token(*, env_path, save=False):
    """Return (token, stored_locally); saving needs the explicit CLI flag."""
    if save:
        token = read_token(persist=True)
        save_token(env_path, token)
        return token, True
    saved = load_saved_token(env_path)
    return (saved, True) if saved is not None else (read_token(), False)


def _read(token, url, max_bytes):
    """Only this product's metadata or encoded subset query; never arbitrary URLs."""
    if not valid_token(token):
        raise PilotError("Invalid token format; no request was made.")
    if url != METADATA_URL and not (url.startswith(SUBSET_PREFIX) and
            re.fullmatch(r"[A-Za-z0-9%_.~-]+", url[len(SUBSET_PREFIX):])):
        raise PilotError("Unsupported Earthdata endpoint; no request was made.")
    request = Request(url, headers={"Authorization": "Bearer " + token,
                                          "User-Agent": "Expedition73/0.1 metadata-probe"})
    try:
        with build_opener(NoRedirect()).open(request, timeout=40) as response:
            if response.status != 200:
                raise PilotError("Unexpected metadata status; no result was saved.")
            raw = response.read(max_bytes + 1)
    except HTTPError as exc:
        if exc.code == 401:
            message = "Earthdata HTTP 401: check token validity and application authorization."
        elif exc.code == 403:
            message = ("Earthdata HTTP 403: request forbidden. Check token validity and Earthdata "
                       "Applications > Authorized Apps > Hyrax in the cloud; this status alone does not identify the cause.")
        else:
            message = f"Earthdata HTTP {exc.code}; response was not saved."
        raise PilotError(message) from None
    except (URLError, TimeoutError, OSError, HTTPException, ValueError):
        # Do not expose response bodies, cookies, request headers or exception
        # text which could reflect a credential. No automatic retry.
        raise PilotError("Earthdata network request failed or timed out; response was not saved.") from None
    if len(raw) > max_bytes:
        raise PilotError("Response exceeds the size limit; no result was saved.")
    if token.encode("ascii") in raw:
        raise PilotError("Unexpected credential reflection in response; no result was saved.")
    return raw


def probe(token):
    raw = _read(token, METADATA_URL, MAX_METADATA_BYTES)
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
