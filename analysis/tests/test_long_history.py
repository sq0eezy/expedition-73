"""The real 24-year candidate period, offline replay and old report identities."""
import hashlib
from pathlib import Path
import unittest

from expedition73 import history, web_preview
from expedition73.power import loads

ROOT = Path(__file__).resolve().parents[1]


class LongHistoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results = {r: history.validate_run(ROOT / f'examples/{r}-history-2001-2024') for r in ('a', 'b')}
        cls.catalog = web_preview.catalog(ROOT, loads((ROOT.parent / 'web/history-regions.json').read_bytes()))

    def test_full_calendar_and_all_intersecting_cells_are_present(self):
        for region, cells in [('a', 56), ('b', 55)]:
            result = self.results[region]
            self.assertEqual(result['time']['start'], '2001-01')
            self.assertEqual(result['time']['end'], '2024-12')
            self.assertEqual(result['quality']['complete_months'], 288)
            self.assertEqual(result['quality']['missing_months'], [])
            self.assertEqual(len(result['provenance']['annual_sources']), 24)
            self.assertTrue(all(row['valid_cells'] == cells and row['valid_area_fraction'] == 1 for row in result['series']))

    def test_old_source_snapshots_remain_byte_identical(self):
        for r in ('a', 'b'):
            for year in (2023, 2024):
                old = history.capture(ROOT / f'examples/{r}-history-2023-2024/year-{year}')
                new = history.capture(ROOT / f'examples/{r}-history-2001-2024/year-{year}')
                self.assertEqual(old, new)

    def test_catalog_spans_all_years_without_changing_old_report_identities(self):
        self.assertEqual([s['year'] for s in self.catalog['snapshots']], list(range(2001, 2025)))
        self.assertEqual(self.catalog['default_year'], 2024)
        expected = {2023: 'f4c23871f99661d75e99102208ac9cb15b17f33e373c1ee18bc75a14d941fa5b',
                    2024: 'd4ce2e87783af79ccee855a6a8040845cfd19776a405b52dc829c88c766e7169'}
        for row in self.catalog['snapshots']:
            self.assertEqual(hashlib.sha256(row['data_json'].encode()).hexdigest(), row['sha256'])
            if row['year'] in expected: self.assertEqual(row['sha256'], expected[row['year']])
        self.assertLess(len(history.encoded(self.catalog)), 8_000_000)

    def test_every_exported_unmasked_month_equals_its_source_replay(self):
        for snapshot in self.catalog['snapshots']:
            annual = loads(snapshot['data_json'])
            for region in annual['regions']:
                source = self.results[region['id'].lower()]
                expected = [row['value'] for row in source['series'] if row['date'].startswith(str(snapshot['year']))]
                self.assertEqual([row['unmasked'] for row in region['series']], expected)
