import assert from 'node:assert/strict';
import { test } from 'node:test';
import { readFileSync } from 'node:fs';
import { summarizePolicyDifferences, summarizeRegionDifferences, datasetDigest, createComparisonReview, verifyComparisonReview } from '../src/comparison.mjs';

const series = () => Array.from({ length: 12 }, (_, i) => ({ date: `2024-${String(i + 1).padStart(2, '0')}`, unmasked: 10, land: 10, land_and_ice: 10 }));

test('signed pairs use their own reference; maximum uses absolute size', () => {
  const rows = series(); rows[0] = { ...rows[0], unmasked: -20, land: -22, land_and_ice: -21.5 };
  const [land, ice] = summarizePolicyDifferences(rows);
  assert.equal(land.values[0].delta, -2); assert.equal(ice.values[0].delta, 0.5);
  assert.equal(land.max_abs_delta_degC, 2); assert.deepEqual(land.max_abs_dates, ['2024-01']);
  assert.equal(ice.max_abs_delta_degC, 0.5); assert.equal(land.valid_months, 12);
});
test('missing values exclude only affected pairs, and zero remains a valid value', () => {
  const rows = series(); rows[0].unmasked = null; rows[1].land_and_ice = null;
  const [land, ice] = summarizePolicyDifferences(rows);
  assert.equal(land.values[0].delta, null); assert.equal(land.values[1].delta, 0);
  assert.equal(ice.values[0].delta, 0); assert.equal(ice.values[1].delta, null);
  assert.equal(land.valid_months, 11); assert.equal(ice.valid_months, 11);
});
test('all missing pairs have no maximum, never an artificial zero', () => {
  const rows = series().map((row) => ({ ...row, land: null }));
  for (const summary of summarizePolicyDifferences(rows)) {
    assert.equal(summary.valid_months, 0); assert.equal(summary.max_abs_delta_degC, null);
    assert.deepEqual(summary.max_abs_dates, []);
  }
});
test('all exact ties including zero are retained without mutating inputs', () => {
  const rows = series(), before = structuredClone(rows);
  for (const summary of summarizePolicyDifferences(rows)) assert.deepEqual(summary.max_abs_dates, rows.map((r) => r.date));
  assert.deepEqual(rows, before);
  rows[0].land = 12; rows[5].land = 8;
  assert.deepEqual(summarizePolicyDifferences(rows)[0].max_abs_dates, ['2024-01', '2024-06']);
});
test('sub-millidegree differences are not rounded before aggregation', () => {
  const rows = series(); rows[9].land_and_ice += 0.000576977;
  const ice = summarizePolicyDifferences(rows)[1];
  assert.ok(ice.max_abs_delta_degC > 0.0005769 && ice.max_abs_delta_degC < 0.0005770);
  assert.deepEqual(ice.max_abs_dates, ['2024-10']);
});
test('wrong calendars, duplicates, incomplete years and invalid numeric values fail closed', () => {
  const variants = [series().slice(1), series().reverse(), series(), series(), series(), series()];
  variants[2][1].date = '2024-01'; variants[3][0].land = NaN;
  variants[4][0].land = '10'; variants[5][0].land = undefined;
  for (const rows of variants) assert.throws(() => summarizePolicyDifferences(rows));
});
test('overflow cannot become an infinite displayed statistic', () => {
  const rows = series(); rows[0].land = Number.MAX_VALUE; rows[0].unmasked = -Number.MAX_VALUE;
  assert.throws(() => summarizePolicyDifferences(rows));
});

test('both recorded windows reproduce all existing workflow differences and maxima exactly', () => {
  for (const id of ['a', 'b']) {
    const recorded = JSON.parse(readFileSync(new URL(`../../analysis/examples/${id}-surface-sensitivity.json`, import.meta.url), 'utf8'));
    for (const summary of summarizePolicyDifferences(recorded.series)) {
      assert.equal(summary.max_abs_delta_degC, recorded.diagnostics[`max_abs_${summary.id}_degC`]);
      assert.deepEqual(summary.values.map((r) => r.delta), recorded.series.map((r) => r[summary.id]));
      assert.equal(summary.valid_months, 12);
    }
  }
});


// Minimal technical metadata fixture; scientific values are tested separately
// against both recorded surface sensitivity files below.
function region(id = 'A') {
  const nodes = ['Temperature', 'Fractions', 'Land', 'LandIce'].map((id) => ({ id, operation: id, operation_version: '0.1.0', output_contract: { type: id === 'Fractions' ? 'verified_surface_fractions' : 'temperature_fixture', schema_version: '0.1.0', unit: id === 'Fractions' ? '1' : 'degC' } }));
  return { id, variable: { id: 'air_temperature_2m', height_m: 2, unit: 'degC' },
    time: { frequency: 'monthly', calendar: 'gregorian', provider_time_standard: 'LST', start: '2024-01', end: '2024-12' },
    provenance: { temperature: { provider: 'NASA POWER', product: 'POWER Monthly and Annual API', api_version: 'v2.10.0', sources: ['MERRA2'] }, surface_fractions: { dataset: 'M2C0NXASM', version: '5.12.4' }, source_files_sha256: { fractions: { 'metadata.dmr.xml': 'a'.repeat(64) } } },
    spatial: { geometry: 'reconstructed_midpoint_rectangles', longitude_step_deg: 0.625, latitude_step_deg: 0.5, area_radius_m: 6371008.8, fraction_placement: 'uniform_within_full_cell_assumption' },
    workflow_trace: { nodes }, series: series() };
}

test('regional subtraction preserves direction, all tied maxima and inputs', () => {
  const a = region('A'), b = region('B'); b.series[0].unmasked = 8; b.series[1].unmasked = 12;
  const before = structuredClone([a, b]), ab = summarizeRegionDifferences(a, b, 'unmasked'), ba = summarizeRegionDifferences(b, a, 'unmasked');
  assert.equal(ab.compatible, true); assert.equal(ab.inference_performed, false); assert.equal(ab.scope, 'descriptive_spatial_difference_only');
  assert.equal(ab.values[0].delta, 2); assert.equal(ab.values[1].delta, -2);
  assert.deepEqual(ab.max_abs_dates, ['2024-01', '2024-02']); assert.equal(ab.max_abs_delta_degC, 2);
  assert.equal(ba.max_abs_delta_degC, 2); assert.deepEqual(ba.max_abs_dates, ab.max_abs_dates);
  ab.values.forEach((r, i) => assert.equal(ba.values[i].delta || 0, -r.delta || 0)); assert.deepEqual([a, b], before);
});
test('pair gate blocks different identity, quantity, time, provider and geometry metadata', () => {
  for (const [id, mutate] of [
    ['identity', (b) => b.id = 'A'], ['quantity', (b) => b.variable.height_m = 10], ['quantity', (b) => b.variable.unit = 'K'],
    ['time', (b) => b.time.provider_time_standard = 'UTC'], ['time', (b) => b.time.end = '2025-12'],
    ['provider', (b) => b.provenance.temperature.api_version = 'other'], ['provider', (b) => delete b.provenance.temperature.sources],
    ['geometry', (b) => b.spatial.area_radius_m = 6371000], ['geometry', (b) => delete b.spatial.geometry],
  ]) { const b = region('B'); mutate(b); const result = summarizeRegionDifferences(region(), b, 'unmasked');
    assert.equal(result.compatible, false); assert.equal(result.checks.find((c) => c.id === id).status, 'mismatch');
    assert.deepEqual(result.values, []); assert.equal(result.max_abs_delta_degC, null);
  }
});
test('recipe versions and contracts are checked only for consumed operations', () => {
  const a = region(), b = region('B'); b.workflow_trace.nodes.find((n) => n.id === 'LandIce').operation_version = '0.2.0';
  assert.equal(summarizeRegionDifferences(a, b, 'unmasked').compatible, true);
  assert.equal(summarizeRegionDifferences(a, b, 'land').compatible, true);
  assert.equal(summarizeRegionDifferences(a, b, 'land_and_ice').compatible, false);
  b.workflow_trace.nodes.find((n) => n.id === 'Temperature').output_contract.unit = 'K';
  assert.equal(summarizeRegionDifferences(a, b, 'unmasked').compatible, false);
});
test('surface source, metadata and placement gate masked policies without blocking unmasked', () => {
  for (const mutate of [(b) => b.provenance.surface_fractions.version = 'other', (b) => b.provenance.source_files_sha256.fractions['metadata.dmr.xml'] = 'b'.repeat(64), (b) => b.spatial.fraction_placement = 'unknown']) {
    const b = region('B'); mutate(b);
    assert.equal(summarizeRegionDifferences(region(), b, 'unmasked').checks.find((c) => c.id === 'surface').status, 'not_used');
    for (const policy of ['land', 'land_and_ice']) assert.equal(summarizeRegionDifferences(region(), b, policy).compatible, false);
  }
});
test('regional missing pairs are policy-specific, zero remains a value', () => {
  const a = region(), b = region('B'); a.series[0].land = null; b.series[1].land = null;
  a.series[2].land = 0; b.series[2].land = 0;
  const land = summarizeRegionDifferences(a, b, 'land');
  assert.equal(land.valid_months, 10); assert.equal(land.values[0].delta, null); assert.equal(land.values[1].delta, null); assert.equal(land.values[2].delta, 0);
  assert.equal(summarizeRegionDifferences(a, b, 'unmasked').valid_months, 12);
});
test('no valid regional pairs cannot acquire an artificial zero maximum', () => {
  const a = region(), b = region('B'); b.series.forEach((r) => r.land = null);
  const result = summarizeRegionDifferences(a, b, 'land'); assert.equal(result.valid_months, 0); assert.equal(result.max_abs_delta_degC, null); assert.deepEqual(result.max_abs_dates, []);
});
test('invalid pair calendars, invalid policy and arithmetic overflow are rejected', () => {
  const a = region(), b = region('B'); assert.throws(() => summarizeRegionDifferences(a, b, 'other'));
  const wrong = region('B'); wrong.series.reverse(); assert.throws(() => summarizeRegionDifferences(a, wrong, 'unmasked'));
  for (const r of a.series) r.unmasked = r.land = r.land_and_ice = Number.MAX_VALUE;
  for (const r of b.series) r.unmasked = r.land = r.land_and_ice = -Number.MAX_VALUE;
  assert.throws(() => summarizeRegionDifferences(a, b, 'unmasked'));
});
test('source order and transport strategy do not change pairing; source membership does', () => {
  const a = region(), b = region('B'); a.provenance.temperature.sources = ['MERRA2', 'fixture']; b.provenance.temperature.sources = ['fixture', 'MERRA2'];
  a.provenance.temperature.request_url = 'single'; b.provenance.temperature.requests = [{ id: 'tile' }];
  assert.equal(summarizeRegionDifferences(a, b, 'unmasked').compatible, true);
  b.provenance.temperature.sources = ['MERRA2']; assert.equal(summarizeRegionDifferences(a, b, 'unmasked').compatible, false);
});
test('recorded A/B monthly pair differences match independent direct subtraction for all policies', () => {
  const [a, b] = ['a', 'b'].map((id) => { const saved = JSON.parse(readFileSync(new URL(`../../analysis/examples/${id}-surface-sensitivity.json`, import.meta.url), 'utf8')); return { ...region(id.toUpperCase()), series: saved.series, variable: saved.variable, time: saved.time, provenance: saved.provenance }; });
  for (const policy of ['unmasked', 'land', 'land_and_ice']) {
    const result = summarizeRegionDifferences(a, b, policy);
    assert.equal(result.compatible, true); assert.equal(result.valid_months, 12);
    const independent = a.series.map((row, i) => row[policy] - b.series[i][policy]);
    assert.deepEqual(result.values.map((r) => r.delta), independent);
    assert.equal(result.max_abs_delta_degC, Math.max(...independent.map(Math.abs)));
    assert.deepEqual(result.max_abs_dates, independent.flatMap((v, i) => Math.abs(v) === result.max_abs_delta_degC ? [a.series[i].date] : []));
  }
});


function reviewData() {
  const regions = [region('A'), region('B')];
  for (const r of regions) {
    const ids = ['Temperature', 'Fractions', 'Land', 'LandIce', 'Sensitivity'];
    const links = [[], ['Temperature'], ['Temperature', 'Fractions'], ['Temperature', 'Fractions'], ['Temperature', 'Land', 'LandIce']];
    r.workflow_trace = { schema_version: '0.1.0', output_type: 'recorded_workflow_trace', execution_status: 'completed', scientific_validation: 'not_performed', identity_kind: 'workflow_plan_fingerprint', context_sha256: 'a'.repeat(64), target: 'Sensitivity', nodes: ids.map((id, i) => ({ id, operation: id, operation_version: '0.1.0', status: 'completed', executions: 1, definition_fingerprint: String(i).repeat(64), output_contract: { type: id === 'Fractions' ? 'verified_surface_fractions' : 'temperature_fixture', schema_version: '0.1.0', unit: id === 'Fractions' ? '1' : 'degC' }, inputs: links[i].map((node) => ({ alias: node.toLowerCase(), node, output: 'result', definition_fingerprint: String(ids.indexOf(node)).repeat(64) })) })) };
  }
  return { schema_version: '0.3.0', output_type: 'recorded_temperature_web_preview', data_mode: 'recorded_offline_replay', selection_status: 'candidate', inference_performed: false, dates: series().map((r) => r.date), regions };
}
const reviewSelection = () => ({ left_id: 'B', right_id: 'A', policy: 'land', month: '2024-07' });
const reviewHash = 'c'.repeat(64);

test('dataset digest hashes exact bytes using standard SHA-256', async () => {
  assert.equal(await datasetDigest(new TextEncoder().encode('abc')), 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad');
  assert.notEqual(await datasetDigest(new TextEncoder().encode('abc')), await datasetDigest(new TextEncoder().encode('abc\n')));
  await assert.rejects(datasetDigest(new Uint8Array()));
  await assert.rejects(datasetDigest(new Uint8Array(8_000_001)));
});
test('review round trip binds direction, policy, month and definition identities without mutating inputs', () => {
  const data = reviewData(), before = structuredClone(data), selection = reviewSelection();
  const report = createComparisonReview(data, reviewHash, selection);
  assert.deepEqual(verifyComparisonReview(JSON.parse(JSON.stringify(report)), data, reviewHash), report);
  assert.deepEqual(report.selection, selection); assert.equal(report.selected_month.date, '2024-07');
  assert.deepEqual(report.result, summarizeRegionDifferences(data.regions[1], data.regions[0], 'land'));
  assert.equal(report.scientific_acceptance, 'not_performed'); assert.equal(report.identity_authentication, 'not_performed');
  assert.deepEqual(data, before);
});
test('result, source identity, policy, schema, extra fields and scientific claims cannot be silently changed', () => {
  const data = reviewData(), original = createComparisonReview(data, reviewHash, reviewSelection());
  for (const mutate of [(r) => r.result.values[0].delta = 99, (r) => r.selected_month.delta = 99, (r) => r.source_definitions[0].definition_fingerprint = '9'.repeat(64), (r) => r.selection.policy = 'unmasked', (r) => r.schema_version = '9.0.0', (r) => r.inference_performed = true, (r) => r.extra = 'private', (r) => r.scientific_acceptance = 'approved']) {
    const report = structuredClone(original); mutate(report); assert.throws(() => verifyComparisonReview(report, data, reviewHash));
  }
});
test('different source snapshots are rejected even when the selected numerical values match', () => {
  const data = reviewData(), report = createComparisonReview(data, reviewHash, reviewSelection());
  assert.throws(() => verifyComparisonReview(report, data, 'd'.repeat(64)));
  const changed = structuredClone(data); changed.regions[0].workflow_trace.context_sha256 = 'd'.repeat(64);
  assert.throws(() => verifyComparisonReview(report, changed, reviewHash));
});
test('reordered JSON keys verify semantically; serialization order is not a signature', () => {
  const data = reviewData(), report = createComparisonReview(data, reviewHash, reviewSelection());
  const reordered = Object.fromEntries(Object.entries(report).reverse());
  reordered.selection = Object.fromEntries(Object.entries(report.selection).reverse());
  assert.deepEqual(verifyComparisonReview(reordered, data, reviewHash), report);
});
test('unsupported source, unavailable pair, invalid month and uncomparable calculations cannot generate reviews', () => {
  const data = reviewData();
  for (const selection of [{ ...reviewSelection(), left_id: 'Missing' }, { ...reviewSelection(), left_id: 'A' }, { ...reviewSelection(), month: '2023-01' }, { ...reviewSelection(), extra: 'private' }]) assert.throws(() => createComparisonReview(data, reviewHash, selection));
  assert.throws(() => createComparisonReview({ ...data, schema_version: '0.2.0' }, reviewHash, reviewSelection()));
  assert.throws(() => createComparisonReview(data, 'bad hash', reviewSelection()));
  data.regions[0].workflow_trace.nodes.find((n) => n.id === 'Land').operation_version = '0.2.0';
  assert.throws(() => createComparisonReview(data, reviewHash, reviewSelection()));
});
test('reviews retain missing pairs and null maximum instead of manufacturing zero evidence', () => {
  const data = reviewData(); data.regions[0].series.forEach((r) => r.land = null);
  const report = createComparisonReview(data, reviewHash, reviewSelection());
  assert.equal(report.result.valid_months, 0); assert.equal(report.result.max_abs_delta_degC, null); assert.equal(report.selected_month.delta, null);
  assert.deepEqual(verifyComparisonReview(report, data, reviewHash), report);
});
test('arbitrary private source fields are not copied into a review', () => {
  const data = reviewData(); data.private = 'PRIVATE_CONTEXT'; data.regions[0].provenance.private = 'PRIVATE_PATH';
  data.regions[0].workflow_trace.nodes[0].private = 'PRIVATE_PARAMETER';
  assert.ok(!JSON.stringify(createComparisonReview(data, reviewHash, reviewSelection())).includes('PRIVATE_'));
});
