"""Provider/project-neutral, read-only MkDocs reader catalog and widgets.

Only the built site is written. Review marks belong to the reader's browser,
never to source documents. This module is shared with project-context-portal.
"""
from __future__ import annotations

from hashlib import sha256
from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path, PurePosixPath
import posixpath
import re

CATALOG = {}
SETTINGS = {}
DOCS = None
REVIEW_URL = None


class PlainText(HTMLParser):
    def __init__(self, value):
        super().__init__(); self.parts = []; self.feed(value)

    def handle_data(self, text):
        self.parts.append(text)

    def text(self):
        return re.sub(r'\s+', ' ', ' '.join(self.parts)).strip()


def safe_path(value):
    if not isinstance(value, str) or not value or '\\' in value or ':' in value:
        raise ValueError('Reader references must be relative documentation paths')
    path = PurePosixPath(value)
    if path.is_absolute() or '..' in path.parts or '#' in value or '?' in value:
        raise ValueError('Unsafe reader reference')
    return value


def validate_settings(settings):
    if not isinstance(settings, dict) or not re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,79}', settings.get('project_id', '')):
        raise ValueError('Set a stable, unique extra.portal_reader.project_id')
    safe_path(settings.get('review_page', 'review/index.md'))
    dependencies = settings.get('dependencies', {})
    if not isinstance(dependencies, dict):
        raise ValueError('Reader dependencies must be a path-to-list mapping')
    for source, paths in dependencies.items():
        safe_path(source)
        if not isinstance(paths, list):
            raise ValueError('Reader dependencies must be lists')
        for path in paths: safe_path(path)
    return settings


def page_entry(source, url, title, content, meta, dependencies=()):
    safe_path(source)
    heading = re.search(r'<h1\b[^>]*>(.*?)</h1>', content, flags=re.S)
    if heading:
        title = PlainText(heading.group(1)).text().rstrip('¶').strip() or title
    summary = meta.get('review_summary')
    change = meta.get('change_summary', '')
    if summary is not None and not isinstance(summary, str) or not isinstance(change, str):
        raise ValueError('Reader summaries must be plain strings')
    if summary is None:
        paragraphs = [PlainText(value).text() for value in re.findall(r'<p\b[^>]*>(.*?)</p>', content, flags=re.S)]
        summary = next((text for text in paragraphs if len(text) >= 40), paragraphs[0] if paragraphs else '')
    digest = sha256()
    for value in (title.encode('utf-8'), content.encode('utf-8'), summary.encode('utf-8'), change.encode('utf-8'), *dependencies):
        digest.update(len(value).to_bytes(8, 'big')); digest.update(value)
    return {'id': source, 'url': url, 'title': title, 'summary': summary[:400],
            'change_summary': change[:600], 'topic': source.split('/')[0] if '/' in source else 'overview',
            'content_hash': digest.hexdigest()}


def catalog_payload(project_id, pages):
    pages = sorted(pages, key=lambda entry: entry['id'])
    if len({p['id'] for p in pages}) != len(pages):
        raise ValueError('Duplicate reader page id')
    revision = sha256(json.dumps(pages, sort_keys=True, ensure_ascii=False).encode('utf-8')).hexdigest()
    return {'schema_version': '1.0', 'artifact_kind': 'portal_reader_catalog',
            'project_id': project_id, 'revision': revision, 'pages': pages}


def relative_root(page):
    url = page.file.url
    base = url if url.endswith('/') else posixpath.dirname(url)
    return posixpath.relpath('.', base or '.') + '/'


def widget(page, language, center=False):
    root = relative_root(page)
    attributes = f'data-reader-catalog="{escape(root, quote=True)}assets/reader/catalog.json" data-reader-root="{escape(root, quote=True)}" data-reader-lang="{language}"'
    if center:
        return f'<section class="reader-center" data-reader-center {attributes}><p role="status">' + ('İnceleme kataloğu yükleniyor…' if language == 'tr' else 'Loading review catalog…') + '</p></section>'
    review = root + REVIEW_URL
    return f'<section class="reader-toolbar" data-reader-toolbar data-reader-page="{escape(page.file.src_uri, quote=True)}" {attributes}><label>' + ('Bu sayfanın inceleme durumu' if language == 'tr' else 'Your review status for this page') + f'<select data-reader-mark disabled></select></label><a href="{escape(review, quote=True)}">' + ('Değişiklikler ve inceleme listem' if language == 'tr' else 'Changes & my review list') + '</a><p data-reader-message role="status" aria-live="polite"></p></section>'


def on_config(config):
    global CATALOG, SETTINGS, DOCS, REVIEW_URL
    CATALOG = {}; REVIEW_URL = None
    SETTINGS = validate_settings(config.get('extra', {}).get('portal_reader', {}))
    DOCS = Path(config['docs_dir']).resolve()
    return config


def on_files(files, config):
    global REVIEW_URL
    source = SETTINGS.get('review_page', 'review/index.md')
    review = next((file for file in files if file.src_uri == source), None)
    if review is None: raise ValueError('Reader center page is missing')
    REVIEW_URL = review.url
    sources = {file.src_uri for file in files}
    for page, paths in SETTINGS.get('dependencies', {}).items():
        if page not in sources: raise ValueError('Reader dependency owner page is missing')
        for path in paths:
            target = (DOCS / path).resolve()
            if not target.is_relative_to(DOCS) or not target.is_file():
                raise ValueError('Reader dependency missing or outside public docs')
    return files


def on_page_content(html, page, config, files):
    source = page.file.src_uri
    dependencies = [(DOCS / path).read_bytes() for path in SETTINGS.get('dependencies', {}).get(source, [])]
    CATALOG[source] = page_entry(source, page.file.url, page.title, html, page.meta, dependencies)
    language = 'tr' if config['theme'].get('language') == 'tr' else 'en'
    if source == SETTINGS.get('review_page', 'review/index.md'):
        center = widget(page, language, center=True)
        return html.replace('<!-- READER:CENTER -->', center) if '<!-- READER:CENTER -->' in html else html + center
    return widget(page, language) + html


def on_post_build(config):
    output = Path(config['site_dir']) / 'assets/reader/catalog.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = catalog_payload(SETTINGS['project_id'], CATALOG.values())
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
