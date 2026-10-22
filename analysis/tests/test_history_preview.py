"""Annual catalogs retain existing contracts and exact annual report identities."""
import copy
import hashlib
from pathlib import Path
import unittest
from unittest.mock import patch

from expedition73 import history, web_preview
from expedition73.power import PilotError, loads

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT.parent / 'web'


class HistoryPreviewTests(unittest.TestCase):
    def registry(self):
        return loads((WEB / 'history-regions.json').read_bytes())

    def test_actual_catalog_has_both_years_and_original_2024_snapshot_bytes(self):
        catalog = web_preview.catalog(ROOT, self.registry())
        self.assertEqual(catalog['schema_version'], '0.4.0')
        self.assertEqual([s['year'] for s in catalog['snapshots']], [2023, 2024])
        for row in catalog['snapshots']:
            self.assertEqual(hashlib.sha256(row['data_json'].encode()).hexdigest(), row['sha256'])
            data = loads(row['data_json'])
            self.assertEqual(data['dates'], [f"{row['year']}-{m:02d}" for m in range(1, 13)])
            self.assertEqual([len(r['spatial']['cells']) for r in data['regions']], [56, 55])
        legacy = web_preview.payload(ROOT, loads((WEB / 'regions.json').read_bytes()))
        self.assertEqual(catalog['snapshots'][1]['data_json'].encode(), history.encoded(legacy))

    def test_bad_registry_or_default_does_not_export_partial_catalog(self):
        registry = self.registry()
        for change in [{**registry, 'default_year': 2025}, {**registry, 'private': True},
                       {**registry, 'regions': []}, {**registry, 'default_year': True}]:
            with self.assertRaises(PilotError): web_preview.catalog(ROOT, change)

    def test_different_year_ranges_cannot_silently_drop_a_region_year(self):
        registry = self.registry()
        results = [history.validate_run(ROOT / e['history']) for e in registry['regions']]
        results[1] = copy.deepcopy(results[1]); results[1]['time']['start'] = '2024-01'
        with patch.object(history, 'validate_run', side_effect=results), self.assertRaises(PilotError):
            web_preview.catalog(ROOT, registry)

    def test_existing_year_data_matches_replayed_annual_sensitivity(self):
        catalog = web_preview.catalog(ROOT, self.registry())
        for row in catalog['snapshots']:
            for region in loads(row['data_json'])['regions']:
                original = history.validate_run(ROOT / f"examples/{region['id'].lower()}-history-2023-2024")
                expected = [r['value'] for r in original['series'] if r['date'].startswith(str(row['year']))]
                self.assertEqual([r['unmasked'] for r in region['series']], expected)
