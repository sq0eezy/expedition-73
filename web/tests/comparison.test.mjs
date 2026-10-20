import assert from 'node:assert/strict';
import { test } from 'node:test';
import { readFileSync } from 'node:fs';
import { summarizePolicyDifferences } from '../src/comparison.mjs';

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
