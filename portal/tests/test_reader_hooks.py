"""Reader catalog contracts; these are not application/model tests."""
import importlib.util
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('reader_hooks', ROOT / 'scripts/reader_hooks.py')
reader = importlib.util.module_from_spec(spec); spec.loader.exec_module(reader)


class ReaderCatalogTests(unittest.TestCase):
    def entry(self, **meta):
        return reader.page_entry('guide/a.md', 'guide/a/', 'A', '<h1>A</h1><p>Hello <strong>reader</strong>.</p>', meta)

    def test_plain_intro_and_authored_change_note(self):
        e = self.entry(change_summary='Added review controls')
        self.assertEqual(e['summary'], 'Hello reader .')
        self.assertEqual(e['change_summary'], 'Added review controls')

    def test_real_heading_distinguishes_repeated_overview_nav_labels(self):
        e = reader.page_entry('architecture/index.md', 'architecture/', 'Overview',
                              '<h1>Architecture<a href="#architecture">¶</a></h1><p>Design notes</p>', {})
        self.assertEqual(e['title'], 'Architecture')

    def test_content_and_dependency_changes_change_hash(self):
        args = ('a.md', 'a/', 'A', '<p>Same page</p>', {})
        a = reader.page_entry(*args, [b'old JSON'])
        b = reader.page_entry(*args, [b'new JSON'])
        self.assertNotEqual(a['content_hash'], b['content_hash'])
        self.assertNotEqual(self.entry()['content_hash'], self.entry(review_summary='New introduction')['content_hash'])

    def test_catalog_revision_is_order_independent_and_deterministic(self):
        a = self.entry(); b = dict(a, id='guide/b.md', url='guide/b/')
        one = reader.catalog_payload('sample', [a,b])
        self.assertEqual(one, reader.catalog_payload('sample', [b,a]))
        with self.assertRaises(ValueError): reader.catalog_payload('sample', [a,a])

    def test_invalid_settings_and_unsafe_paths_rejected(self):
        for ref in ('../private.md', '/absolute.md', 'https://host/file.md', 'C:\\private.md', 'a.md#x'):
            with self.subTest(ref=ref), self.assertRaises(ValueError): reader.safe_path(ref)
        for settings in ({}, {'project_id':'Name With Spaces'}, {'project_id':'x','dependencies':{'a.md':'wrong'}}):
            with self.subTest(settings=settings), self.assertRaises(ValueError): reader.validate_settings(settings)
        self.assertEqual(reader.validate_settings({'project_id':'my-project'})['project_id'], 'my-project')

    def test_invalid_summary_type_rejected(self):
        with self.assertRaises(ValueError): self.entry(review_summary=['not','text'])
        with self.assertRaises(ValueError): self.entry(change_summary={'bad':'type'})

    def test_center_uses_inline_slot_without_rewriting_source(self):
        reader.SETTINGS = {'project_id':'test'}; reader.REVIEW_URL = 'review/'
        page = SimpleNamespace(file=SimpleNamespace(src_uri='review/index.md',url='review/'),title='Review',meta={})
        html = '<p>Introduction</p><!-- READER:CENTER --><details>Help</details>'
        output = reader.on_page_content(html,page,{'theme':{'language':'en'}},[])
        self.assertLess(output.index('data-reader-center'),output.index('<details>'))
        self.assertNotIn('<!-- READER:CENTER -->',output)
        self.assertIn('<!-- READER:CENTER -->',html)

    def test_deep_urls_and_attributes_are_escaped(self):
        reader.REVIEW_URL = 'review/'
        page = SimpleNamespace(file=SimpleNamespace(src_uri='guide/a"b.md',url='guide/a/'))
        markup = reader.widget(page, 'en')
        self.assertIn('../../assets/reader/catalog.json', markup)
        self.assertIn('../../review/', markup)
        self.assertIn('a&quot;b.md', markup)

    def test_missing_dependency_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            reader.DOCS = Path(temp); reader.SETTINGS={'project_id':'test','dependencies':{'a.md':['missing.json']}}
            files = [SimpleNamespace(src_uri='review/index.md',url='review/'),SimpleNamespace(src_uri='a.md',url='a/')]
            with self.assertRaises(ValueError): reader.on_files(files,{})

    def test_post_build_writes_only_catalog_and_does_not_change_sources(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); docs = root / 'docs'; docs.mkdir()
            source = docs / 'a.md'; source.write_text('# Untouched',encoding='utf-8')
            reader.SETTINGS={'project_id':'test'};reader.CATALOG={'guide/a.md':self.entry()}
            reader.on_post_build({'site_dir':str(root / 'site')})
            self.assertEqual(source.read_text(encoding='utf-8'),'# Untouched')
            self.assertTrue((root / 'site/assets/reader/catalog.json').is_file())


if __name__ == '__main__': unittest.main()
