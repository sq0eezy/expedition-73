"""Portable offline checks, preview and a bounded, verifiable demo archive."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
LEGACY_PUBLIC = ('app.js', 'comparison.mjs', 'data/results.json', 'index.html', 'styles.css')
PRIOR_PUBLIC = (*LEGACY_PUBLIC, 'trace.mjs')
PUBLIC = (*PRIOR_PUBLIC, 'data/annual.json')
PACKAGE_CONTRACTS = {'0.1.0': (LEGACY_PUBLIC, '0.2.0'), '0.2.0': (PRIOR_PUBLIC, '0.3.0'), '0.3.0': (PRIOR_PUBLIC, '0.4.0'), '0.4.0': (PUBLIC, '0.4.0'), '0.5.0': (PUBLIC, '0.4.0')}
ARCHIVE_NAMES = {*PUBLIC, 'manifest.json'}
LIMIT = 8_000_000


def run(arguments, cwd=ROOT):
    subprocess.run([str(a) for a in arguments], cwd=cwd, check=True)


def setup():
    env = ROOT / 'analysis/.venv'
    python = env / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    if env.is_symlink() or not env.resolve().is_relative_to((ROOT / 'analysis').resolve()):
        raise ValueError('Analysis environment must stay inside this checkout.')
    if not python.exists():
        if env.exists():
            raise ValueError('Existing analysis/.venv is incomplete; preserve it and inspect it before setup.')
        run([sys.executable, '-m', 'venv', env])
    run([python, '-m', 'pip', 'install', '--disable-pip-version-check', '-r', ROOT / 'docker/requirements.lock'])


def build():
    run([sys.executable, ROOT / 'analysis/scripts/build_web_preview.py'])


def checks():
    analysis = ROOT / 'analysis'
    node = shutil.which('node')
    if not node:
        raise ValueError('Full checks require Node.js 22+ for the JS tests; preview itself needs only Python.')
    # Missing optional source dependencies must fail, not silently skip all NetCDF tests.
    run([sys.executable, '-c', 'import jsonschema, netCDF4, numpy'])
    run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests'], analysis)
    for args in [
        ['validate', 'examples/a-point-2024/result.json'],
        ['validate', 'examples/b-point-2024/result.json'],
        ['check-alignment', 'examples/a-point-2024/result.json', 'examples/b-point-2024/result.json'],
        ['validate-window', 'examples/a-window-2024'],
        ['validate-tiled-window', 'examples/b-window-2024'],
    ]:
        run([sys.executable, '-m', 'expedition73', *args], analysis)
    for region in ('a', 'b'):
        run([sys.executable, '-m', 'expedition73', 'validate-window-history', f'examples/{region}-history-2023-2024'], analysis)
        run([sys.executable, '-m', 'expedition73', 'validate-window-history', f'examples/{region}-history-2001-2024'], analysis)
        run([sys.executable, '-m', 'expedition73', 'validate-annual-weighting', '--run', f'examples/{region}-history-2001-2024', '--input', f'examples/{region}-annual-weighting-audit.json'], analysis)
        run([sys.executable, 'scripts/fetch_surface_fractions.py', '--replay', f'examples/{region}-surface-fractions'], analysis)
    artifacts = analysis / 'artifacts'
    if artifacts.is_symlink() or not artifacts.resolve().is_relative_to(analysis.resolve()):
        raise ValueError('Check artifacts must stay inside analysis.')
    artifacts.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='workspace-check-', dir=artifacts) as temp:
        # Verify this owned temporary target before its recursive context cleanup.
        if not Path(temp).resolve().is_relative_to(artifacts.resolve()):
            raise ValueError('Unexpected temporary check directory.')
        for region in ('a', 'b'):
            run([sys.executable, '-m', 'expedition73', 'run-surface-workflow',
                 '--window-run', f'examples/{region}-window-2024',
                 '--fraction-run', f'examples/{region}-surface-fractions',
                 '--output-dir', Path(temp) / region], analysis)
            run([sys.executable, '-m', 'expedition73', 'run-annual-workflow',
                 '--run', f'examples/{region}-history-2001-2024',
                 '--output-dir', Path(temp) / f'{region}-annual'], analysis)
    run([node, '--test', 'web/tests/comparison.test.mjs', 'web/tests/trace.test.mjs'])
    for name in ('app.js', 'comparison.mjs', 'trace.mjs'):
        run([node, '--check', f'web/src/{name}'])
    build()
    print('Offline analysis, A/B replay, JS checks and preview build passed.', flush=True)


def _manifest(files, version='0.5.0'):
    return {'format': 'expedition73-static-preview', 'version': version,
            'selection_status': 'candidate', 'data_mode': 'recorded_offline_replay',
            'inference_performed': False,
            'files': {name: {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
                      for name, raw in sorted(files.items())}}


def verify_package(path):
    with zipfile.ZipFile(path) as archive:
        infos = archive.infolist()
        names = [i.filename for i in infos]
        if len(names) != len(set(names)) or 'manifest.json' not in names or len(names) > len(ARCHIVE_NAMES):
            raise ValueError('Duplicate, missing or excessive archive entries.')
        if any(i.file_size > LIMIT or i.is_dir() or i.flag_bits & 1 for i in infos):
            raise ValueError('Unexpected archive size, directory or encrypted entry.')
        # Read the enumerated entries only; never extract an archive into the checkout.
        raw_manifest = archive.read('manifest.json')
        manifest = json.loads(raw_manifest)
        contract = PACKAGE_CONTRACTS.get(manifest.get('version')) if isinstance(manifest, dict) else None
        if contract is None:
            raise ValueError('Unsupported package manifest version.')
        public, schema_version = contract
        if set(names) != {*public, 'manifest.json'}:
            raise ValueError('Demo archive must contain exactly the versioned public allowlist and manifest.')
        files = {name: archive.read(name) for name in public}
        if manifest != _manifest(files, manifest['version']):
            raise ValueError('Demo archive manifest or SHA-256 integrity check failed.')
        data = json.loads(files['data/results.json'])
        if (data.get('schema_version') != schema_version or data.get('output_type') != ('recorded_temperature_year_catalog' if schema_version == '0.4.0' else 'recorded_temperature_web_preview')
                or data.get('selection_status') != 'candidate' or data.get('inference_performed') is not False
                or data.get('data_mode') != 'recorded_offline_replay'):
            raise ValueError('Demo archive has an unsupported result contract.')
        if manifest['version'] in {'0.4.0', '0.5.0'}:
            annual = json.loads(files['data/annual.json'])
            if (annual.get('schema_version') != ('0.2.0' if manifest['version'] == '0.5.0' else '0.1.0') or annual.get('output_type') != 'recorded_annual_weighting_web_preview'
                    or annual.get('selection_status') != 'candidate' or annual.get('inference_performed') is not False
                    or annual.get('data_mode') != 'recorded_offline_replay'
                    or annual.get('source_catalog_sha256') != hashlib.sha256(files['data/results.json']).hexdigest()
                    or annual.get('status') not in {'available', 'not_available'} or not isinstance(annual.get('regions'), list)
                    or not 0 <= len(annual['regions']) <= 8 or (annual['status'] == 'available') != bool(annual['regions'])):
                raise ValueError('Annual preview does not match the exact packaged monthly catalog.')
            if manifest['version'] == '0.5.0':
                for entry in annual['regions']:
                    if not isinstance(entry, dict) or not isinstance(entry.get('workflow'), dict):
                        raise ValueError('Annual workflow identity is missing or inconsistent.')
                    workflow = entry.get('workflow', {})
                    context = workflow.get('context_json')
                    trace = workflow.get('trace', {})
                    if (not isinstance(trace, dict) or not isinstance(context, str) or len(context) > 100_000
                            or hashlib.sha256(context.encode('utf-8')).hexdigest() != trace.get('context_sha256')
                            or trace.get('target') != 'AnnualWeighting' or trace.get('execution_status') != 'completed'
                            or trace.get('scientific_validation') != 'not_performed'):
                        raise ValueError('Annual workflow identity is missing or inconsistent.')
    return {'status': 'verified', 'public_files': len(public), 'selection_status': 'candidate'}


def package(output=None):
    build()
    dist = ROOT / 'web/dist'
    files = {}
    for name in PUBLIC:
        path = dist / name
        if path.is_symlink() or not path.resolve().is_relative_to(dist.resolve()):
            raise ValueError('Public assets must resolve inside web/dist.')
        raw = path.read_bytes()
        if len(raw) > LIMIT:
            raise ValueError('Preview asset exceeds the bounded demo size.')
        files[name] = raw
    files['manifest.json'] = (json.dumps(_manifest(files), ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode('utf-8')
    destination = Path(output) if output else ROOT / 'web/artifacts/expedition73-preview.zip'
    allowed = ROOT / 'web/artifacts'
    if (destination.suffix != '.zip' or destination.is_symlink()
            or not destination.resolve().is_relative_to(allowed.resolve())
            or not allowed.resolve().is_relative_to((ROOT / 'web').resolve())):
        raise ValueError('Demo output must be a .zip file inside web/artifacts.')
    destination.parent.mkdir(parents=True, exist_ok=True)
    # Deterministic stored ZIP: fixed dates, permissions, order; no local paths/timestamps.
    handle, temp = tempfile.mkstemp(prefix='.demo-', suffix='.tmp', dir=destination.parent)
    os.close(handle)
    try:
        with zipfile.ZipFile(temp, 'w', compression=zipfile.ZIP_STORED) as archive:
            for name, raw in sorted(files.items()):
                info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                archive.writestr(info, raw)
        result = verify_package(temp)
        os.replace(temp, destination)
    finally:
        Path(temp).unlink(missing_ok=True)
    return {**result, 'archive': str(destination),
            'sha256': hashlib.sha256(destination.read_bytes()).hexdigest()}


def doctor():
    print(f'Python: {sys.version.split()[0]}')
    for name in ('jsonschema', 'netCDF4', 'numpy'):
        from importlib.metadata import PackageNotFoundError, version
        try:
            print(f'{name}: {version(name)}')
        except PackageNotFoundError:
            print(f'{name}: missing (run setup; then use analysis/.venv Python)')
    for name in ('node', 'docker'):
        print(f'{name}: {"available" if shutil.which(name) else "not installed"}')
    print('No NASA requests or token reads were performed. Docker engine readiness is a separate check.')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest='command', required=True)
    for command in ('doctor', 'setup', 'check', 'build'):
        subs.add_parser(command)
    preview = subs.add_parser('preview')
    preview.add_argument('--port', type=int, default=8873)
    pack = subs.add_parser('package')
    pack.add_argument('--output', type=Path)
    verify = subs.add_parser('verify-package')
    verify.add_argument('archive', type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == 'doctor': doctor()
        elif args.command == 'setup': setup()
        elif args.command == 'check': checks()
        elif args.command == 'build': build()
        elif args.command == 'package': print(json.dumps(package(args.output)))
        elif args.command == 'verify-package': print(json.dumps(verify_package(args.archive)))
        elif args.command == 'preview':
            build()
            run([sys.executable, ROOT / 'web/serve.py', '--port', args.port])
    except subprocess.CalledProcessError as exc:
        print(f'ERROR: workspace step failed (exit {exc.returncode}).', file=sys.stderr)
        return 1
    except (OSError, ValueError, zipfile.BadZipFile, KeyError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
