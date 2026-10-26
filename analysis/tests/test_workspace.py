"""Portable packaging: public allowlist, repeatability and failure isolation."""
import importlib.util
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import zipfile

spec = importlib.util.spec_from_file_location('workspace', Path(__file__).resolve().parents[2] / 'scripts/workspace.py')
workspace = importlib.util.module_from_spec(spec)
spec.loader.exec_module(workspace)


class WorkspaceTests(unittest.TestCase):
    def prepare(self, root):
        for name in workspace.PUBLIC:
            target = root / 'web/dist' / name
            target.parent.mkdir(parents=True, exist_ok=True)
            data = {'schema_version': '0.4.0', 'output_type': 'recorded_temperature_year_catalog',
                    'selection_status': 'candidate', 'data_mode': 'recorded_offline_replay', 'inference_performed': False}
            target.write_text(json.dumps(data) if name.endswith('.json') else 'public fixture', encoding='utf-8')
        monthly=(root/'web/dist/data/results.json').read_bytes()
        (root/'web/dist/data/annual.json').write_text(json.dumps({
            'schema_version':'0.1.0','output_type':'recorded_annual_weighting_web_preview',
            'selection_status':'candidate','data_mode':'recorded_offline_replay','inference_performed':False,
            'source_catalog_sha256':hashlib.sha256(monthly).hexdigest(),'status':'not_available','regions':[]}),encoding='utf-8')
        (root / '.env').write_text('PRIVATE_FIXTURE_NOT_A_TOKEN', encoding='utf-8')
        (root / 'web/dist/.env').write_text('PRIVATE_EXTRA', encoding='utf-8')

    def test_only_seven_public_assets_and_manifest_are_packaged_repeatably(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(workspace, 'ROOT', Path(temp)), patch.object(workspace, 'build'):
            root = Path(temp)
            self.prepare(root)
            workspace.package()
            package = root / 'web/artifacts/expedition73-preview.zip'
            original = package.read_bytes()
            self.assertEqual(workspace.verify_package(package)['status'], 'verified')
            with zipfile.ZipFile(package) as archive:
                self.assertEqual(set(archive.namelist()), workspace.ARCHIVE_NAMES)
                self.assertFalse(any(b'PRIVATE' in archive.read(name) for name in archive.namelist()))
            workspace.package()
            self.assertEqual(original, package.read_bytes())

    def test_tampered_assets_or_manifest_cannot_pass_integrity_check(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(workspace, 'ROOT', Path(temp)), patch.object(workspace, 'build'):
            root = Path(temp)
            self.prepare(root)
            workspace.package()
            path = root / 'web/artifacts/expedition73-preview.zip'
            with zipfile.ZipFile(path) as archive:
                files = {name: archive.read(name) for name in archive.namelist()}
            for name in ('app.js', 'manifest.json'):
                with self.subTest(name=name):
                    altered = {**files, name: b'{}'}
                    with zipfile.ZipFile(path, 'w') as archive:
                        for key, raw in altered.items(): archive.writestr(key, raw)
                    with self.assertRaises(ValueError): workspace.verify_package(path)

    def test_previous_manifest_and_web_contract_remain_verifiable(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'previous.zip'
            data = {'schema_version': '0.2.0', 'output_type': 'recorded_temperature_web_preview',
                    'selection_status': 'candidate', 'data_mode': 'recorded_offline_replay', 'inference_performed': False}
            files = {name: json.dumps(data).encode() if name.endswith('.json') else b'previous asset'
                     for name in workspace.LEGACY_PUBLIC}
            manifest = workspace._manifest(files, '0.1.0')
            with zipfile.ZipFile(path, 'w') as archive:
                for name, raw in files.items(): archive.writestr(name, raw)
                archive.writestr('manifest.json', json.dumps(manifest))
            self.assertEqual(workspace.verify_package(path)['public_files'], 5)

    def test_previous_six_file_year_catalog_manifest_remains_verifiable(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); self.prepare(root); path=root/'previous.zip'
            files={name:(root/'web/dist'/name).read_bytes() for name in workspace.PRIOR_PUBLIC}
            with zipfile.ZipFile(path,'w') as archive:
                for name,raw in files.items(): archive.writestr(name,raw)
                archive.writestr('manifest.json',json.dumps(workspace._manifest(files,'0.3.0')))
            self.assertEqual(workspace.verify_package(path)['public_files'],6)

    def test_resealed_annual_catalog_mismatch_preserves_previous_demo(self):
        with tempfile.TemporaryDirectory() as temp,patch.object(workspace,'ROOT',Path(temp)),patch.object(workspace,'build'):
            root=Path(temp); self.prepare(root); workspace.package()
            package=root/'web/artifacts/expedition73-preview.zip'; before=package.read_bytes()
            path=root/'web/dist/data/annual.json'; data=json.loads(path.read_bytes()); data['source_catalog_sha256']='0'*64
            path.write_text(json.dumps(data),encoding='utf-8')
            with self.assertRaises(ValueError): workspace.package()
            self.assertEqual(package.read_bytes(),before)

    def test_new_manifest_cannot_omit_trace_asset_or_claim_previous_web_contract(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(workspace, 'ROOT', Path(temp)), patch.object(workspace, 'build'):
            root = Path(temp)
            self.prepare(root)
            (root / 'web/dist/data/results.json').write_text(json.dumps({
                'schema_version': '0.2.0', 'output_type': 'recorded_temperature_web_preview',
                'selection_status': 'candidate', 'data_mode': 'recorded_offline_replay', 'inference_performed': False}))
            with self.assertRaises(ValueError): workspace.package()

    def test_duplicate_or_traversal_archive_entries_are_rejected_without_extracting(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'bad.zip'
            for names in (['../.env'], ['manifest.json'] * 2):
                with self.subTest(names=names), zipfile.ZipFile(path, 'w') as archive:
                    for name in names: archive.writestr(name, '{}')
                with self.assertRaises(ValueError): workspace.verify_package(path)
            self.assertEqual(sorted(p.name for p in Path(temp).iterdir()), ['bad.zip'])

    def test_destination_outside_public_artifacts_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(workspace, 'ROOT', Path(temp)), patch.object(workspace, 'build'):
            root = Path(temp)
            self.prepare(root)
            with self.assertRaises(ValueError): workspace.package(root / 'accidental.zip')
            self.assertFalse((root / 'accidental.zip').exists())

    def test_failed_rebuild_preserves_previous_demo(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(workspace, 'ROOT', Path(temp)), patch.object(workspace, 'build') as build:
            root = Path(temp)
            self.prepare(root)
            workspace.package()
            path = root / 'web/artifacts/expedition73-preview.zip'
            original = path.read_bytes()
            build.side_effect = subprocess.CalledProcessError(1, 'fixture')
            with self.assertRaises(subprocess.CalledProcessError): workspace.package()
            self.assertEqual(original, path.read_bytes())

    def test_full_checks_stop_on_first_failure(self):
        with patch.object(workspace.shutil, 'which', return_value='node'), \
                patch.object(workspace, 'run', side_effect=subprocess.CalledProcessError(1, 'fixture')) as run, \
                patch.object(workspace, 'build') as build:
            with self.assertRaises(subprocess.CalledProcessError): workspace.checks()
            self.assertEqual(run.call_count, 1)
            build.assert_not_called()

    def test_missing_node_does_not_claim_a_partial_full_check_pass(self):
        with patch.object(workspace.shutil, 'which', return_value=None), patch.object(workspace, 'run') as run:
            with self.assertRaises(ValueError): workspace.checks()
            run.assert_not_called()
