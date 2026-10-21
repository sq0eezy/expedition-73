"""Check only a caller-selected local preview; never contact NASA."""
import argparse
import json
import urllib.error
import urllib.parse
import urllib.request


def check(base):
    url = urllib.parse.urlsplit(base)
    if url.scheme != 'http' or url.hostname not in ('127.0.0.1', 'localhost') or url.username or url.password:
        raise ValueError('Smoke checks require a local HTTP preview URL.')
    base = base.rstrip('/') + '/'
    for name in ('index.html', 'styles.css', 'app.js', 'comparison.mjs', 'trace.mjs', 'data/results.json'):
        with urllib.request.urlopen(base + name, timeout=5) as response:
            raw = response.read(8_000_001)
            if response.status != 200 or len(raw) > 8_000_000:
                raise ValueError('Public file missing or unexpectedly large.')
            if name.endswith('.mjs') and 'javascript' not in response.headers.get('Content-Type', ''):
                raise ValueError('ES module is not served with a JavaScript MIME type.')
            if name.endswith('.json'):
                data = json.loads(raw)
                if data['data_mode'] != 'recorded_offline_replay' or data['inference_performed'] is not False:
                    raise ValueError('Unexpected preview data mode.')
    for name in ('.env', 'analysis/expedition73/power.py', 'web/serve.py'):
        try:
            urllib.request.urlopen(base + name, timeout=5).close()
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                continue
            raise
        raise ValueError('A private/source path is accessible through the public server.')
    print('Local HTTP smoke passed: six public files, ES module MIME, recorded data and absent source/private paths.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('url', nargs='?', default='http://127.0.0.1:8873/')
    args = parser.parse_args()
    try:
        check(args.url)
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, f'ERROR: {exc}\n')
