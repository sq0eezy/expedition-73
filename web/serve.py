"""Serve only the generated public preview on this machine."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


class PreviewHandler(SimpleHTTPRequestHandler):
    # Windows may register .mjs as text/plain; browsers require a JS MIME type.
    extensions_map = {**SimpleHTTPRequestHandler.extensions_map, '.mjs': 'text/javascript'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8873)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent / 'dist'
    if not (root / 'index.html').is_file():
        parser.error('Build the preview first: analysis/scripts/build_web_preview.py')
    if not 1024 <= args.port <= 65535:
        parser.error('Choose a port between 1024 and 65535.')
    try:
        server = ThreadingHTTPServer(('127.0.0.1', args.port), partial(PreviewHandler, directory=str(root)))
    except OSError:
        parser.error('Could not bind the local port; stop the previous preview or choose --port.')
    print(f'Local preview: http://127.0.0.1:{args.port}/\nStop: Ctrl+C', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
