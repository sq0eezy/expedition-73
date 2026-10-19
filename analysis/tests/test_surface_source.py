"""Fabricated NetCDF bytes only: parser/provenance checks, never NASA data proof."""
import hashlib
import importlib.util
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch
from urllib.parse import unquote

from expedition73 import earthdata, masking, surface_source as source
from expedition73.power import PilotError, loads

ROOT = Path(__file__).resolve().parents[1]
STAMP = "2026-10-18T00:00:00Z"
try:
    import netCDF4
    import numpy as np
except ImportError:
    netCDF4 = None


def fake_dmr():
    variables = []
    for name in ("lon", "lat", "time", *masking.COMPONENTS):
        fraction = name in masking.COMPONENTS
        kind = "Float32" if fraction else "Int32" if name == "time" else "Float64"
        dims = ("time", "lat", "lon") if fraction else (name,)
        attrs = {"units": "1" if fraction else {"lon": "degrees_east", "lat": "degrees_north",
                                               "time": "minutes since 1992-01-02 03:00:00"}[name]}
        if fraction:
            attrs.update({"_FillValue": "9.99999987e+14", "missing_value": "9.99999987e+14",
                          "scale_factor": "1.", "add_offset": "0."})
        children = ''.join(f'<Dim name="/{dim}"/>' for dim in dims)
        children += ''.join(f'<Attribute name="{a}"><Value>{v}</Value></Attribute>' for a, v in attrs.items())
        variables.append(f'<{kind} name="{name}">{children}</{kind}>')
    dimensions = '<Dimension name="time" size="1"/><Dimension name="lat" size="361"/><Dimension name="lon" size="576"/>'
    return (f'<Dataset name="{source.DATASET_NAME}">' + dimensions + ''.join(variables) + '</Dataset>').encode()


@unittest.skipIf(netCDF4 is None, "optional requirements-mask.txt not installed")
class SurfaceSourceTests(unittest.TestCase):
    def setUp(self):
        self.config = loads((ROOT / "examples/a-window-2024.config.json").read_bytes())
        self.metadata = fake_dmr()

    def fabricate(self, config=None, mutate=None):
        plan = masking.request_plan(config or self.config)
        xs = sorted({c['longitude'] for c in plan['cells']})
        ys = sorted({c['latitude'] for c in plan['cells']})
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "synthetic-not-nasa.nc4"
            with netCDF4.Dataset(path, "w") as ds:
                for name, size in [("time", 1), ("lat", len(ys)), ("lon", len(xs))]:
                    ds.createDimension(name, size)
                for name, values, unit in [("lon", xs, "degrees_east"), ("lat", ys, "degrees_north"),
                                           ("time", [0], "minutes since 1992-01-02 03:00:00")]:
                    var = ds.createVariable(name, "i4" if name == "time" else "f8", (name,))
                    var.units = unit
                    var[:] = values
                for name, value in zip(masking.COMPONENTS, (0.5, 0.125, 0.125, 0.25)):
                    var = ds.createVariable(name, "f4", ("time", "lat", "lon"), fill_value=np.float32(9.99999987e14))
                    var.units = "1"
                    var.missing_value = np.float32(9.99999987e14)
                    var.scale_factor = np.float32(1)
                    var.add_offset = np.float32(0)
                    var[:] = value
                if mutate:
                    mutate(ds)
            return path.read_bytes()

    def test_both_geometries_and_known_fraction_values(self):
        for name, count in [("a", 56), ("b", 55)]:
            config = loads((ROOT / f"examples/{name}-window-2024.config.json").read_bytes())
            raw = self.fabricate(config)
            result = source.convert(raw, self.metadata, config, STAMP)
            self.assertEqual(len(result['cells']), count)
            self.assertEqual(result['cells'][0]['fractions']['FRLANDICE'], .125)
            self.assertEqual(result['source']['response_sha256'], hashlib.sha256(raw).hexdigest())
            self.assertNotIn('selected_components', result)

    def test_constraint_is_subset_of_each_axis_not_full_globe(self):
        query = unquote(source.request_url(self.config))
        self.assertIn('/FRLAND[0:1:0][252:1:258][107:1:114]', query)
        self.assertIn('/lon[107:1:114];/lat[252:1:258];/time[0:1:0];', query)
        self.assertNotIn('361', query)

    def test_metadata_changes_rejected_before_decoding(self):
        for before, after in [(b'size="576"', b'size="575"'), (b'<Dim name="/lat"/>', b'<Dim name="/lon"/>'),
                              (b'<Value>1.</Value>', b'<Value>0.5</Value>'), (b'Float32', b'Float64'),
                              (b'degrees_east', b'degrees_west')]:
            with self.subTest(before=before), self.assertRaises(PilotError):
                source.convert(self.fabricate(), self.metadata.replace(before, after), self.config, STAMP)

    def test_coordinate_shift_reversal_and_duplicate_rejected(self):
        for values in [lambda v: v + .125, lambda v: v[::-1], lambda v: np.zeros_like(v)]:
            def mutate(ds):
                ds.variables['lon'][:] = values(ds.variables['lon'][:])
            with self.subTest(values=values), self.assertRaises(PilotError):
                source.convert(self.fabricate(mutate=mutate), self.metadata, self.config, STAMP)

    def test_fill_nan_out_of_range_and_bad_partition_rejected(self):
        for value in (np.float32(9.99999987e14), float('nan'), float('inf'), -0.01, 1.01, .25):
            def mutate(ds):
                ds.variables['FRLAND'][0, 0, 0] = value
            with self.subTest(value=value), self.assertRaises(PilotError):
                source.convert(self.fabricate(mutate=mutate), self.metadata, self.config, STAMP)

    def test_zero_land_is_retained_not_missing(self):
        def mutate(ds):
            ds.variables['FRLAND'][0, 0, 0] = 0
            ds.variables['FROCEAN'][0, 0, 0] = .75
        result = source.convert(self.fabricate(mutate=mutate), self.metadata, self.config, STAMP)
        self.assertEqual(result['cells'][0]['fractions']['FRLAND'], 0)
        self.assertEqual(len(result['cells']), 56)

    def test_units_packing_fill_metadata_and_dimension_order_rejected(self):
        def packing(ds):
            ds.variables['FRLAND'].scale_factor = .5
        def unit(ds):
            ds.variables['FRLAND'].units = '%'
        def fill(ds):
            ds.variables['FRLAND'].missing_value = -999.
        def dim(ds):
            ds.renameDimension('lat', 'wrong_dimension')
        def missing(ds):
            ds.renameVariable('FRLAKE', 'not_FRLAKE')
        for mutate in (packing, unit, fill, dim, missing):
            with self.subTest(mutate=mutate), self.assertRaises(PilotError):
                source.convert(self.fabricate(mutate=mutate), self.metadata, self.config, STAMP)

    def test_html_corrupt_and_oversized_are_not_netcdf(self):
        for raw in (b'<html>login</html>', b'CDF\x01broken', b'x' * (source.MAX_SUBSET_BYTES + 1)):
            with self.subTest(size=len(raw)), self.assertRaises(PilotError):
                source.convert(raw, self.metadata, self.config, STAMP)

    def test_timestamp_is_required_and_timezone_aware(self):
        for stamp in ('2026-10-18T00:00:00', 'invalid'):
            with self.subTest(stamp=stamp), self.assertRaises(PilotError):
                source.convert(self.fabricate(), self.metadata, self.config, stamp)

    def test_fixed_url_transport_limit_and_no_token_in_result(self):
        token = 'fabricated-test-token-not-live'
        raw = self.fabricate()
        with patch('expedition73.earthdata._read', return_value=raw) as request:
            saved, stamp = source.fetch_subset(token, self.config)
        request.assert_called_once_with(token, source.request_url(self.config), source.MAX_SUBSET_BYTES)
        self.assertNotIn(token, json.dumps(source.convert(saved, self.metadata, self.config, stamp)))
        for url in ('https://evil.example/data', earthdata.SUBSET_PREFIX + 'x&token=oops'):
            with patch('expedition73.earthdata.build_opener') as opener, self.assertRaises(PilotError):
                earthdata._read(token, url, 100)
            opener.assert_not_called()

    def test_local_replay_detects_tampering(self):
        raw = self.fabricate()
        result = source.convert(raw, self.metadata, self.config, STAMP)
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            (directory / 'response.nc4').write_bytes(raw)
            (directory / 'metadata.dmr.xml').write_bytes(self.metadata)
            for name, value in [('request.json', self.config), ('fractions.json', result),
                                ('conversion-report.json', {'converter_version': source.CONVERTER_VERSION,
                                 'metadata_sha256': hashlib.sha256(self.metadata).hexdigest(),
                                 'response_sha256': hashlib.sha256(raw).hexdigest(),
                                 'response_bytes': len(raw), 'cells': len(result['cells'])})]:
                (directory / name).write_text(json.dumps(value), encoding='utf-8')
            self.assertEqual(source.replay(directory), result)
            result['cells'][0]['fractions']['FRLAND'] = .4
            (directory / 'fractions.json').write_text(json.dumps(result), encoding='utf-8')
            with self.assertRaises(PilotError):
                source.replay(directory)

    def test_helper_saves_and_replays_both_regions_without_token(self):
        spec = importlib.util.spec_from_file_location('surface_helper_success', ROOT / 'scripts/fetch_surface_fractions.py')
        helper = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(helper)
        token = 'fabricated-local-test-token-only'
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'examples').mkdir()
            for name in ('a', 'b'):
                (root / f'examples/{name}-window-2024.config.json').write_bytes(
                    (ROOT / f'examples/{name}-window-2024.config.json').read_bytes())
            log = io.StringIO()
            def fetch(supplied, config):
                self.assertEqual(supplied, token)
                return self.fabricate(config), STAMP
            with patch.object(helper, 'ROOT', root), patch.object(earthdata, 'get_token', return_value=(token, False)) as prompt, \
                    patch.object(earthdata, 'probe', return_value=(self.metadata, {})), \
                    patch.object(source, 'fetch_subset', side_effect=fetch), redirect_stdout(log):
                self.assertEqual(helper.main([]), 0)
            prompt.assert_called_once_with(env_path=root.parent / '.env', save=False)
            output = next((root / 'artifacts').iterdir())
            for name, count in [('a', 56), ('b', 55)]:
                self.assertEqual(len(source.replay(output / name)['cells']), count)
            for file in output.rglob('*'):
                if file.is_file():
                    self.assertNotIn(token.encode(), file.read_bytes())
            self.assertNotIn(token, log.getvalue())

    def test_helper_failure_saves_no_success_directory_or_credential(self):
        spec = importlib.util.spec_from_file_location('surface_helper', ROOT / 'scripts/fetch_surface_fractions.py')
        helper = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(helper)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'examples').mkdir()
            for name in ('a', 'b'):
                (root / f'examples/{name}-window-2024.config.json').write_bytes(
                    (ROOT / f'examples/{name}-window-2024.config.json').read_bytes())
            with patch.object(helper, 'ROOT', root), patch.object(earthdata, 'get_token', return_value=('fake-token', False)), \
                    patch.object(earthdata, 'probe', side_effect=PilotError('HTTP 401')), \
                    redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                self.assertEqual(helper.main([]), 1)
            self.assertFalse((root / 'artifacts').exists())
