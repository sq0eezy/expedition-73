"""Read public NASA CMR metadata for proposed regions; no science files or login."""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://cmr.earthdata.nasa.gov/search/"
REGIONS = [
    {"id": "candidate-a", "name": "Colorado Plateau study window",
     "bbox_west_south_east_north": [-113, 36, -109, 39]},
    {"id": "candidate-b", "name": "Northern Alaska study window",
     "bbox_west_south_east_north": [-156, 68, -150, 70]},
]
PRODUCTS = [
    {"short_name": "M2TMNXSLV", "version": "5.12.4", "provider": "GES_DISC"},
    {"short_name": "MOD13A3", "version": "061", "provider": "LPCLOUD"},
    {"short_name": "MOD10CM", "version": "61", "provider": "NSIDC_CPRD"},
]
PERIODS = {
    "proposed_2001_2024": "2001-01-01T00:00:00Z,2024-12-31T23:59:59Z",
    "sample_july_2001": "2001-07-01T00:00:00Z,2001-07-31T23:59:59Z",
    "sample_july_2024": "2024-07-01T00:00:00Z,2024-07-31T23:59:59Z",
}


def query(endpoint: str, params: dict) -> tuple[dict, int | None, str]:
    url = BASE + endpoint + "?" + urlencode(params)
    request = Request(url, headers={"User-Agent": "Expedition73-RegionCatalogResearch/1.0",
                                    "Accept": "application/json"})
    with urlopen(request, timeout=40) as response:
        payload = json.load(response)
        hits = response.headers.get("CMR-Hits")
    return payload, int(hits) if hits is not None else None, url


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--as-of", required=True, type=date.fromisoformat)
    options = parser.parse_args()
    result = {
        "as_of": options.as_of.isoformat(),
        "kind": "public_metadata_probe_not_scientific_analysis",
        "regions": REGIONS,
        "limits": [
            "Rectangles are proposed sampling windows, not official NASA region boundaries.",
            "A spatial granule match does not establish valid pixels within the rectangle.",
            "Full-period hit counts and two sampled months do not prove all-month coverage.",
            "No science file, QA mask, authentication or trend was tested.",
        ],
        "products": [],
    }
    for product in PRODUCTS:
        payload, _, url = query("collections.json", {**product, "page_size": 10})
        entries = payload["feed"]["entry"]
        if len(entries) != 1:
            raise RuntimeError(f"Expected one explicit collection for {product}: {len(entries)}")
        entry = entries[0]
        record = {
            **product, "collection_id": entry["id"], "title": entry["title"],
            "time_start": entry.get("time_start"), "time_end": entry.get("time_end"),
            "collection_query": url, "spatial_queries": [],
        }
        for region in REGIONS:
            for label, temporal in PERIODS.items():
                data, hits, granule_url = query("granules.json", {
                    "collection_concept_id": entry["id"],
                    "bounding_box": ",".join(map(str, region["bbox_west_south_east_north"])),
                    "temporal": temporal, "page_size": 1,
                })
                granules = data["feed"]["entry"]
                example = granules[0] if granules else {}
                record["spatial_queries"].append({
                    "region_id": region["id"], "period": label, "query_url": granule_url,
                    "matching_granules": hits, "example_id": example.get("id"),
                    "example_title": example.get("title"),
                    "example_time_start": example.get("time_start"),
                    "example_time_end": example.get("time_end"),
                })
                print(f"{product['short_name']} {region['id']} {label}: "
                      f"hits={hits}, example={'yes' if granules else 'no'}", flush=True)
        result["products"].append(record)
    output = ROOT / "docs/research/REGION_CATALOG_CHECK.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Saved docs/research/REGION_CATALOG_CHECK.json", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
