"""Bounded M2C0NXASM subset conversion. Live access is a separate local step.

No regridding, automatic land/ice choice, annual statistic or scientific acceptance.
"""
from __future__ import annotations

import hashlib
import math
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

from . import earthdata, masking, regional
from .power import PilotError, loads

MAX_SUBSET_BYTES = 2_000_000
DATASET_NAME = "MERRA2_101.const_2d_asm_Nx.00000000.nc4"
CONVERTER_VERSION = "0.1.0"


def dependencies():
    try:
        import netCDF4
        import numpy
    except ImportError:
        raise PilotError("Install analysis/requirements-mask.txt in the analysis virtual environment first.") from None
    return netCDF4, numpy


def request_url(config):
    plan = masking.request_plan(config)
    indices = plan["zero_based_inclusive_indices"]
    x0, x1 = indices["longitude"]
    y0, y1 = indices["latitude"]
    # DAP4 uses semicolon-separated projections and inclusive [start:stride:stop].
    projections = [f"/lon[{x0}:1:{x1}]", f"/lat[{y0}:1:{y1}]", "/time[0:1:0]"]
    projections += [f"/{name}[0:1:0][{y0}:1:{y1}][{x0}:1:{x1}]" for name in masking.COMPONENTS]
    return earthdata.SUBSET_PREFIX + quote(";".join(projections), safe="")


def metadata_spec(raw):
    """Fail closed if the observed source's dimensions/packing have changed."""
    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        raise PilotError("Invalid source DMR XML.") from None
    local = lambda element: element.tag.rsplit("}", 1)[-1]
    if local(root) != "Dataset" or root.attrib.get("name") != DATASET_NAME:
        raise PilotError("Unexpected source Dataset identity.")
    dimensions = {e.attrib.get("name"): e.attrib.get("size") for e in root if local(e) == "Dimension"}
    if dimensions != {"time": "1", "lat": "361", "lon": "576"}:
        raise PilotError("Unexpected source grid dimensions.")
    specs = {}
    for name in ("lon", "lat", "time", *masking.COMPONENTS):
        elements = [e for e in root if e.attrib.get("name") == name and local(e) != "Dimension"]
        if len(elements) != 1:
            raise PilotError("Missing or duplicate DMR variable.")
        element = elements[0]
        dims = [e.attrib.get("name") for e in element if local(e) == "Dim"]
        wanted = ["/time", "/lat", "/lon"] if name in masking.COMPONENTS else ["/" + name]
        dtype = "Float32" if name in masking.COMPONENTS else "Int32" if name == "time" else "Float64"
        if dims != wanted or local(element) != dtype:
            raise PilotError("Unexpected source variable dimension order/type.")
        attrs = {e.attrib.get("name"): [v.text for v in e if local(v) == "Value"]
                 for e in element if local(e) == "Attribute"}
        unit = "1" if name in masking.COMPONENTS else {"lon": "degrees_east", "lat": "degrees_north",
                                                    "time": "minutes since 1992-01-02 03:00:00"}[name]
        if attrs.get("units") != [unit]:
            raise PilotError("Unexpected source variable units.")
        if name in masking.COMPONENTS:
            try:
                if (float(attrs["scale_factor"][0]) != 1 or float(attrs["add_offset"][0]) != 0
                        or not math.isfinite(float(attrs["_FillValue"][0]))
                        or float(attrs["_FillValue"][0]) <= 1
                        or attrs["missing_value"] != attrs["_FillValue"]):
                    raise ValueError()
            except (KeyError, ValueError, TypeError, IndexError):
                raise PilotError("Unsupported source packing or missing-value metadata.") from None
        specs[name] = attrs
    return specs


def fetch_subset(token, config):
    url = request_url(config)
    raw = earthdata._read(token, url, MAX_SUBSET_BYTES)
    return raw, datetime.now(timezone.utc).isoformat(timespec="seconds")


def area_capability(metadata_raw):
    """Audit the selected granule declaration, never infer/download AREA values.

    The 2015 file specification lists AREA; actual observed DMR does not.
    Even a future AREA declaration is only metadata, not validated numeric data.
    """
    if len(metadata_raw) > earthdata.MAX_METADATA_BYTES:
        raise PilotError("Source metadata exceeds the supported size limit.")
    metadata_spec(metadata_raw)  # Existing strict product/grid/fraction checks.
    root = ET.fromstring(metadata_raw)
    local = lambda element: element.tag.rsplit("}", 1)[-1]
    if any(local(element) == "Group" for element in root):
        raise PilotError("Grouped source metadata requires explicit variable mapping.")
    numeric = {"Float32", "Float64", "Int8", "UInt8", "Byte", "Int16", "UInt16",
               "Int32", "UInt32", "Int64", "UInt64"}
    variables = []
    for element in root:
        if local(element) not in numeric:
            continue
        name = element.attrib.get("name")
        if not name or any(record["name"] == name for record in variables):
            raise PilotError("Missing or duplicate numeric variable declaration in source metadata.")
        units = [value.text for attribute in element if local(attribute) == "Attribute"
                 and attribute.attrib.get("name") == "units"
                 for value in attribute if local(value) == "Value"]
        variables.append({"name": name, "type": local(element), "units": units,
                          "dimensions": [item.attrib.get("name") for item in element if local(item) == "Dim"]})
    variables.sort(key=lambda item: item["name"])
    area = next((variable for variable in variables if variable["name"] == "AREA"), None)
    return {"schema_version": "0.1.0", "output_type": "source_area_capability_check",
            "scope": "selected_granule_metadata_only",
            "source": {"dataset": "M2C0NXASM", "version": "5.12.4", "granule": DATASET_NAME,
                       "metadata_uri": earthdata.METADATA_URL,
                       "metadata_sha256": hashlib.sha256(metadata_raw).hexdigest()},
            "available_numeric_variables": variables,
            "area": {"numeric_declaration_present": area is not None, "declaration": area,
                     "comparison_status": "metadata_present_values_not_validated" if area is not None
                     else "not_available_in_selected_granule",
                     "numeric_values_retrieved": False, "comparison_performed": False},
            "automatic_product_or_geometry_substitution": False,
            "scientific_profile_accepted": False}


def convert(raw, metadata_raw, config, retrieved_at):
    """Read local bytes only; the NetCDF library never receives a URL or token."""
    plan = masking.request_plan(config)
    spec = metadata_spec(metadata_raw)
    if len(raw) > MAX_SUBSET_BYTES or not raw.startswith((b"\x89HDF\r\n\x1a\n", b"CDF\x01", b"CDF\x02")):
        raise PilotError("Expected a bounded NetCDF subset response.")
    netcdf, np = dependencies()
    xs = sorted({c["longitude"] for c in plan["cells"]})
    ys = sorted({c["latitude"] for c in plan["cells"]})
    arrays = {}
    try:
        with netcdf.Dataset("surface-subset", memory=raw) as ds:
            ds.set_auto_maskandscale(False)
            if ds.groups:
                raise PilotError("Grouped source variables require explicit mapping; no implicit conversion.")
            for name in ("lon", "lat", "time", *masking.COMPONENTS):
                if name not in ds.variables:
                    raise PilotError("Required subset variable is absent.")
                var = ds.variables[name]
                dims = ("time", "lat", "lon") if name in masking.COMPONENTS else (name,)
                shape = (1, len(ys), len(xs)) if name in masking.COMPONENTS else (
                    len(xs) if name == "lon" else len(ys) if name == "lat" else 1,)
                dtype = np.dtype("float32" if name in masking.COMPONENTS else "int32" if name == "time" else "float64")
                if var.dimensions != dims or var.shape != shape or var.dtype != dtype:
                    raise PilotError("Subset shape, dimension order or numeric type differs from the plan.")
                attrs = {attr: var.getncattr(attr) for attr in var.ncattrs()}
                if attrs.get("units") != spec[name]["units"][0] or "_Unsigned" in attrs:
                    raise PilotError("Unexpected subset units or encoding.")
                if float(attrs.get("scale_factor", 1)) != 1 or float(attrs.get("add_offset", 0)) != 0:
                    raise PilotError("Nonidentity packing requires an explicit converter version.")
                values = var[:]
                if not np.isfinite(values).all():
                    raise PilotError("Subset contains nonfinite values.")
                for attr in ("_FillValue", "missing_value", "fmissing_value"):
                    if attr in attrs and np.isin(values, attrs[attr]).any():
                        raise PilotError("Subset contains source missing/fill values; no zero filling.")
                if name in masking.COMPONENTS:
                    for attr in ("_FillValue", "missing_value"):
                        if attr not in attrs or not math.isclose(float(attrs[attr]), float(spec[name][attr][0]), rel_tol=1e-7):
                            raise PilotError("Subset fill metadata differs from source DMR.")
                    if ((values < 0) | (values > 1)).any():
                        raise PilotError("Surface fractions must lie in [0, 1]; no clipping.")
                arrays[name] = values
    except (OSError, RuntimeError, ValueError, TypeError, IndexError) as exc:
        if isinstance(exc, PilotError):
            raise
        raise PilotError("Unable to decode the expected local NetCDF subset.") from None
    if arrays["lon"].tolist() != xs or arrays["lat"].tolist() != ys:
        raise PilotError("Actual subset coordinates differ from native grid plan; no regridding or reversal.")
    cells = [{"longitude": lon, "latitude": lat,
              "fractions": {name: float(arrays[name][0, j, i]) for name in masking.COMPONENTS}}
             for j, lat in enumerate(ys) for i, lon in enumerate(xs)]
    result = {"schema_version": "0.1.0", "output_type": "source_cell_surface_fractions",
              "data_origin": "provider_subset", "grid_id": plan["grid"]["id"],
              "spatial_support": "whole_source_cell", "unit": "1",
              "source": {"dataset": "M2C0NXASM", "version": "5.12.4", "uri": request_url(config),
                         "retrieved_at": retrieved_at, "response_sha256": hashlib.sha256(raw).hexdigest()},
              "cells": cells}
    masking.validate_mask(result, config)
    return result


def replay(directory):
    """Reconvert fixed local filenames; equality is not independent source authentication."""
    directory = Path(directory)
    config = loads((directory / "request.json").read_bytes())
    report = loads((directory / "conversion-report.json").read_bytes())
    metadata = (directory / "metadata.dmr.xml").read_bytes()
    saved = loads((directory / "fractions.json").read_bytes())
    raw = (directory / "response.nc4").read_bytes()
    return replay_data(config, report, metadata, raw, saved)


def replay_data(config, report, metadata, raw, saved):
    """Replay an already captured snapshot without reading mutable files again."""
    if (report.get("converter_version") != CONVERTER_VERSION or
            report.get("metadata_sha256") != hashlib.sha256(metadata).hexdigest()):
        raise PilotError("Conversion version or saved metadata hash disagrees.")
    masking.validate_mask(saved, config)
    if (report.get("response_sha256") != hashlib.sha256(raw).hexdigest()
            or report.get("response_bytes") != len(raw) or report.get("cells") != len(saved["cells"])):
        raise PilotError("Saved subset report disagrees with raw response or cell count.")
    result = convert(raw, metadata, config, saved["source"]["retrieved_at"])
    if not regional._same_result(result, saved):
        raise PilotError("Saved fractions differ from conversion replay.")
    return result
