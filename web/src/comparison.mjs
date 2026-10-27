/* Descriptive, paired differences of recorded policy series. No inference. */
import { traceGraph } from "./trace.mjs";
export const contrasts = [
  { id: "land_minus_unmasked", left: "land", right: "unmasked", label: "Kara − maskesiz" },
  { id: "land_ice_minus_land", left: "land_and_ice", right: "land", label: "Kara + kara buzu − kara" },
];

export function summarizePolicyDifferences(series) {
  if (!Array.isArray(series) || series.length !== 12) throw Error("Expected twelve monthly policy records");
  const year = typeof series[0]?.date === "string" ? series[0].date.slice(0, 4) : "";
  if (!/^\d{4}$/.test(year) || !series.every((row, i) => row?.date === `${year}-${String(i + 1).padStart(2, "0")}` &&
      ["unmasked", "land", "land_and_ice"].every((key) => row[key] === null || typeof row[key] === "number" && Number.isFinite(row[key])))) throw Error("Invalid monthly policy series");
  return contrasts.map((contrast) => {
    const values = series.map((row) => ({ date: row.date,
      delta: row[contrast.left] === null || row[contrast.right] === null ? null : row[contrast.left] - row[contrast.right] }));
    if (values.some((row) => row.delta !== null && !Number.isFinite(row.delta))) throw Error("Non-finite policy difference");
    const valid = values.filter((row) => row.delta !== null);
    const maximum = valid.length ? Math.max(...valid.map((row) => Math.abs(row.delta))) : null;
    return { ...contrast, values, valid_months: valid.length,
      max_abs_delta_degC: maximum,
      max_abs_dates: valid.filter((row) => Math.abs(row.delta) === maximum).map((row) => row.date) };
  });
}

// This gate permits a descriptive subtraction, never a scientific acceptance.
export function summarizeRegionDifferences(left, right, policy) {
  if (!["unmasked", "land", "land_and_ice"].includes(policy)) throw Error("Unknown pair policy");
  for (const region of [left, right]) summarizePolicyDifferences(region.series);
  const checks = [];
  const nonempty = (s) => typeof s === "string" && !!s.trim();
  const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);
  const check = (id, label, a, b, valid, detail) => checks.push({ id, label,
    status: valid && same(a, b) ? "matched" : "mismatch", detail });
  checks.push({ id: "identity", label: "Farklı iki pencere", status: nonempty(left.id) && nonempty(right.id) && left.id !== right.id ? "matched" : "mismatch", detail: `${left.id} − ${right.id}` });
  const quantity = (r) => [r.variable?.id, r.variable?.height_m, r.variable?.unit];
  check("quantity", "Gösterge / yükseklik / birim", quantity(left), quantity(right),
    same(quantity(left), ["air_temperature_2m", 2, "degC"]), "2 m hava sıcaklığı · °C");
  const calendar = (r) => [r.time?.frequency, r.time?.calendar, r.time?.provider_time_standard, r.time?.start, r.time?.end, r.series.map((row) => row.date)];
  const timeValid = (r) => r.time?.frequency === "monthly" && r.time?.calendar === "gregorian" && nonempty(r.time?.provider_time_standard) && r.time.start === r.series[0].date && r.time.end === r.series.at(-1).date;
  check("time", "Takvim / dönem / zaman standardı", calendar(left), calendar(right), timeValid(left) && timeValid(right), `${left.time?.start}–${left.time?.end} · ${left.time?.provider_time_standard}`);
  const source = (r) => { const p = r.provenance?.temperature; return [p?.provider, p?.product, p?.api_version, Array.isArray(p?.sources) ? [...p.sources].sort() : null]; };
  const sourceValid = (r) => { const p = source(r); return p.slice(0, 3).every(nonempty) && Array.isArray(p[3]) && p[3].length > 0 && p[3].every(nonempty) && new Set(p[3]).size === p[3].length; };
  check("provider", "Sıcaklık kaynağı / API sürümü", source(left), source(right), sourceValid(left) && sourceValid(right), `${source(left)[0]} · ${source(left)[2]}`);
  const geometry = (r) => [r.spatial?.geometry, r.spatial?.longitude_step_deg, r.spatial?.latitude_step_deg, r.spatial?.area_radius_m];
  check("geometry", "Grid / alan yaklaşımı", geometry(left), geometry(right), same(geometry(left), ["reconstructed_midpoint_rectangles", 0.625, 0.5, 6371008.8]), "0,625° × 0,5° · aynı pilot küresi");
  const names = policy === "unmasked" ? ["Temperature"] : ["Temperature", "Fractions", policy === "land" ? "Land" : "LandIce"];
  const recipe = (r) => names.map((id) => {
    const n = r.workflow_trace?.nodes?.find((node) => node.id === id);
    return [n?.operation, n?.operation_version, n?.output_contract?.type, n?.output_contract?.schema_version, n?.output_contract?.unit];
  });
  check("recipe", "Kullanılan işlem / sözleşme sürümleri", recipe(left), recipe(right),
    [left, right].every((r) => recipe(r).every((row, i) => row[0] === names[i] && row.every(nonempty))), names.join(" + "));
  if (policy === "unmasked") checks.push({ id: "surface", label: "Fraksiyon kaynağı", status: "not_used", detail: "Maskesiz farkta fraksiyon ağırlığı kullanılmaz." });
  else {
    const fractions = (r) => [r.provenance?.surface_fractions?.dataset, r.provenance?.surface_fractions?.version,
      r.provenance?.source_files_sha256?.fractions?.["metadata.dmr.xml"], r.spatial?.fraction_placement];
    const valid = (r) => { const f = fractions(r); return f.slice(0, 2).every(nonempty) && /^[a-f0-9]{64}$/.test(f[2]) && f[3] === "uniform_within_full_cell_assumption"; };
    check("surface", "Fraksiyon ürünü / metaveri / yerleşim", fractions(left), fractions(right), valid(left) && valid(right), `${fractions(left)[0]} · ${fractions(left)[1]} · homojen yerleşim varsayımı`);
  }
  const compatible = checks.every((c) => c.status !== "mismatch");
  const values = compatible ? left.series.map((row, i) => ({ date: row.date,
    left: row[policy], right: right.series[i][policy],
    delta: row[policy] === null || right.series[i][policy] === null ? null : row[policy] - right.series[i][policy] })) : [];
  if (values.some((r) => r.delta !== null && !Number.isFinite(r.delta))) throw Error("Non-finite regional difference");
  const valid = values.filter((r) => r.delta !== null);
  const maximum = valid.length ? Math.max(...valid.map((r) => Math.abs(r.delta))) : null;
  return { left_id: left.id, right_id: right.id, policy, checks, compatible, inference_performed: false,
    scope: "descriptive_spatial_difference_only", values, valid_months: valid.length,
    max_abs_delta_degC: maximum, max_abs_dates: valid.filter((r) => Math.abs(r.delta) === maximum).map((r) => r.date) };
}

function canonical(value) {
  if (value === null || typeof value === "string" || typeof value === "boolean") return JSON.stringify(value);
  if (typeof value === "number" && Number.isFinite(value)) return JSON.stringify(value);
  if (Array.isArray(value)) return `[${value.map(canonical).join(",")}]`;
  if (value && typeof value === "object" && Object.getPrototypeOf(value) === Object.prototype)
    return `{${Object.keys(value).sort().map((k) => `${JSON.stringify(k)}:${canonical(value[k])}`).join(",")}}`;
  throw Error("Expected finite JSON review fields");
}

// Concatenate recorded months only. Check each region across years; do not
// equate the spatial support of different regions or compute any statistic.
export function recordedMonthlyHistory(snapshots, ids, policy) {
  const nonempty = (v) => typeof v === "string" && !!v.trim();
  const finite = (v) => typeof v === "number" && Number.isFinite(v);
  const bounds = (v) => Array.isArray(v) && v.length === 4 && v.every(finite) && v[0] < v[2] && v[1] < v[3];
  if (!Array.isArray(snapshots) || !snapshots.length || snapshots.length > 50 ||
      !Array.isArray(ids) || !ids.length || ids.length > 8 || !ids.every(nonempty) || new Set(ids).size !== ids.length ||
      !["unmasked", "land", "land_and_ice"].includes(policy)) throw Error("Geçersiz uzun dönem seçimi.");
  const context = (r, dates) => {
    summarizePolicyDifferences(r.series);
    const t = r.time, p = r.provenance?.temperature, s = r.spatial, g = r.region;
    if (!nonempty(r.id) || g?.id !== r.id || g.selection_status !== "candidate" || !bounds(g.candidate_bbox) || !nonempty(g.candidate_window_version) ||
        canonical(r.variable) !== canonical({ id: "air_temperature_2m", height_m: 2, unit: "degC" }) ||
        t?.frequency !== "monthly" || t.calendar !== "gregorian" || !nonempty(t.provider_time_standard) || t.start !== dates[0] || t.end !== dates.at(-1) ||
        !r.series.every((row, i) => row.date === dates[i]) ||
        ![p?.provider, p?.product, p?.api_version].every(nonempty) || !Array.isArray(p.sources) || !p.sources.length || !p.sources.every(nonempty) || new Set(p.sources).size !== p.sources.length ||
        s?.geometry !== "reconstructed_midpoint_rectangles" || s.longitude_step_deg !== 0.625 || s.latitude_step_deg !== 0.5 || s.area_radius_m !== 6371008.8 ||
        !Array.isArray(s.cells) || !s.cells.length || s.cells.length !== r.support?.cell_count || !finite(r.support.window_area_m2) || r.support.window_area_m2 <= 0) throw Error("Uzun dönem kaynak bağlamı eksik veya geçersiz.");
    const names = policy === "unmasked" ? ["Temperature"] : ["Temperature", "Fractions", policy === "land" ? "Land" : "LandIce"];
    const recipe = names.map((id) => {
      const matches = r.workflow_trace?.nodes?.filter((n) => n.id === id);
      const n = matches?.length === 1 ? matches[0] : null;
      const row = [n?.operation, n?.operation_version, n?.output_contract?.type, n?.output_contract?.schema_version, n?.output_contract?.unit];
      if (row[0] !== id || !row.every(nonempty) || row[4] !== (id === "Fractions" ? "1" : "degC")) throw Error("Uzun dönem işlem sözleşmesi geçersiz.");
      return row;
    });
    const coordinates = new Set();
    const cells = s.cells.map((c) => {
      const key = `${c.longitude},${c.latitude}`;
      if (!finite(c.longitude) || !finite(c.latitude) || coordinates.has(key) || !bounds(c.full_cell_bbox) || !bounds(c.intersection_bbox) ||
          !finite(c.intersection_area_m2) || c.intersection_area_m2 <= 0 || !finite(c.weights_m2?.[policy]) || c.weights_m2[policy] < 0) throw Error("Uzun dönem hücre desteği geçersiz.");
      coordinates.add(key);
      return [c.longitude, c.latitude, c.full_cell_bbox, c.intersection_bbox, c.intersection_area_m2, c.weights_m2[policy]];
    }).sort((a, b) => a[1] - b[1] || a[0] - b[0]);
    let surface = null;
    if (policy !== "unmasked") {
      const f = r.provenance?.surface_fractions, hashes = r.provenance?.source_files_sha256?.fractions;
      if (!nonempty(f?.dataset) || !nonempty(f?.version) || s.fraction_placement !== "uniform_within_full_cell_assumption" ||
          !hashes || !Object.keys(hashes).length || !/^[a-f0-9]{64}$/.test(hashes["metadata.dmr.xml"]) || !Object.values(hashes).every((v) => /^[a-f0-9]{64}$/.test(v))) throw Error("Uzun dönem fraksiyon kaydı geçersiz.");
      surface = [f.dataset, f.version, hashes, s.fraction_placement];
    }
    return canonical([g.id, g.candidate_bbox, g.candidate_window_version, r.variable,
      t.frequency, t.calendar, t.provider_time_standard, p.provider, p.product, p.api_version, [...p.sources].sort(),
      s.geometry, s.longitude_step_deg, s.latitude_step_deg, s.area_radius_m, r.support.window_area_m2, cells, recipe, surface]);
  };
  const dates = [], baselines = new Map(), years = [];
  const series = ids.map((id) => ({ id, values: [], valid_months: 0 }));
  for (const data of snapshots) {
    if (data?.schema_version !== "0.3.0" || data.output_type !== "recorded_temperature_web_preview" || data.data_mode !== "recorded_offline_replay" || data.selection_status !== "candidate" || data.inference_performed !== false ||
        !Array.isArray(data.dates) || data.dates.length !== 12 || !Array.isArray(data.regions) || !data.regions.length || data.regions.length > 8 || new Set(data.regions.map((r) => r.id)).size !== data.regions.length) throw Error("Geçersiz yıllık kaynak kaydı.");
    const year = Number(data.dates[0]?.slice(0, 4));
    if (!Number.isInteger(year) || year < 1981 || year > 9999 || years.length && year !== years.at(-1) + 1 ||
        !data.dates.every((date, i) => date === `${year}-${String(i + 1).padStart(2, "0")}`)) throw Error("Uzun dönemde eksik, yinelenen veya sırasız yıl var.");
    for (const row of series) {
      const region = data.regions.find((r) => r.id === row.id);
      if (!region) throw Error(`${row.id} için ${year} kaydı yok; yıllar atlanmadı.`);
      const signature = context(region, data.dates);
      if (baselines.has(row.id) && signature !== baselines.get(row.id)) throw Error(`${row.id} · ${year}: kaynak, sınır, grid, ağırlık veya kullanılan işlem sürümü değişiyor.`);
      baselines.set(row.id, signature);
      for (const month of region.series) {
        row.values.push({ date: month.date, value: month[policy] });
        if (month[policy] !== null) row.valid_months++;
      }
    }
    dates.push(...data.dates); years.push(year);
  }
  return { scope: "recorded_months_only", inference_performed: false, policy, dates, years, series };
}

export async function datasetDigest(bytes) {
  if (!(bytes instanceof Uint8Array) || !bytes.length || bytes.length > 8_000_000) throw Error("Invalid dataset byte size");
  const digest = await globalThis.crypto.subtle.digest("SHA-256", bytes);
  return [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

// Validate the result adapter and its source binding. Python owns the annual
// temperature calculation; this adapter never re-averages monthly temperatures.
export function validateAnnualPreview(payload, catalogSha256, snapshots) {
  const finite = (v) => typeof v === "number" && Number.isFinite(v);
  const close = (a, b) => finite(a) && finite(b) && Math.abs(a - b) <= 1e-9 * Math.max(1, Math.abs(b));
  const same = (a, b) => canonical(a) === canonical(b);
  const fail = () => { throw Error("Yıllık aday kayıt aylık kaynakla veya hesap sözleşmesiyle eşleşmiyor."); };
  if (!/^[a-f0-9]{64}$/.test(catalogSha256) || !["0.1.0","0.2.0"].includes(payload?.schema_version) || payload.output_type !== "recorded_annual_weighting_web_preview" ||
      payload.data_mode !== "recorded_offline_replay" || payload.selection_status !== "candidate" || payload.inference_performed !== false || payload.source_catalog_sha256 !== catalogSha256 ||
      !["available", "not_available"].includes(payload.status) || !Array.isArray(payload.regions) || payload.regions.length > 8 || (payload.status === "available") !== !!payload.regions.length) fail();
  if (payload.status === "not_available") return payload;
  if (!Array.isArray(snapshots) || !snapshots.length) fail();
  const ids = snapshots[0].regions.map((r) => r.id);
  if (!same([...ids].sort(), payload.regions.map((r) => r.id).sort())) fail();
  const history = recordedMonthlyHistory(snapshots, ids, "unmasked");
  for (const entry of payload.regions) {
    const a = entry.audit, first = snapshots[0].regions.find((r) => r.id === entry.id);
    if (!a || !same(Object.keys(a).sort(), ["schema_version","output_type","selection_status","inference_performed","scientific_acceptance","module","region","variable","spatial_support","time","method","weighting_definitions","provenance","series","quality","sensitivity"].sort()) ||
        a.schema_version !== "0.1.0" || a.output_type !== "candidate_annual_weighting_audit" || a.selection_status !== "candidate" || a.inference_performed !== false || a.scientific_acceptance !== "not_performed" ||
        !same(a.module, {id:"air_temperature_2m_annual_weighting",version:"0.1.0"}) || !same(a.region, first.region) || !same(a.variable, first.variable) ||
        a.spatial_support?.kind !== "unmasked_rectangular_window" || a.spatial_support.mask !== "none" || a.spatial_support.cell_count !== first.support.cell_count || !close(a.spatial_support.window_area_m2,first.support.window_area_m2) ||
        !same(a.time,{frequency:"annual",input_frequency:"monthly",calendar:"gregorian",provider_time_standard:first.time.provider_time_standard,start:String(history.years[0]),end:String(history.years.at(-1))}) ||
        !same(a.method,{id:"compare_annual_temperature_weighting",version:"0.1.0",selection_status:"candidate",selected_weighting:null,missing_policy:"require_12_complete_months",inference:"not_performed",provider_value_role:"comparison_only"}) ||
        !same(a.weighting_definitions,[{id:"equal_months",formula:"sum(T_m / 12)",target:"mean_of_twelve_monthly_values"},{id:"calendar_days",formula:"sum(T_m * days_m / days_year)",target:"calendar_day_weighted_monthly_values"}]) ||
        a.provenance?.source_history_schema_version !== "0.1.0" || !/^[a-f0-9]{64}$/.test(a.provenance.source_history_result_sha256) ||
        !Array.isArray(a.series) || a.series.length !== snapshots.length || !Array.isArray(a.provenance.annual_sources) || a.provenance.annual_sources.length !== snapshots.length) fail();
    const provider = first.provenance.temperature;
    for (const key of ["provider","product","api_version"]) if (a.provenance[key] !== provider[key]) fail();
    if (!same([...a.provenance.sources].sort(),[...provider.sources].sort())) fail();
    for (const [i,row] of a.series.entries()) {
      const monthly = snapshots[i].regions.find((r) => r.id === entry.id), year = history.years[i], source = a.provenance.annual_sources[i];
      if (!monthly || source.year !== year || !same(source.files_sha256,monthly.provenance.source_files_sha256.temperature) || row.year !== year) fail();
      const missing = monthly.series.filter((r) => r.unmasked === null).map((r) => r.date);
      const days = monthly.series.map((_,m) => new Date(Date.UTC(year,m+1,0)).getUTCDate()), total = days.reduce((s,d) => s+d,0);
      const complete = missing.length === 0;
      if (row.status !== (complete?"complete":"incomplete") || row.valid_months !== 12-missing.length || !same(row.missing_months,missing) || row.calendar_days !== total ||
          row.valid_calendar_days !== days.reduce((s,d,m) => s+(missing.includes(monthly.series[m].date)?0:d),0) || !Array.isArray(row.weights) || row.weights.length !== 12) fail();
      row.weights.forEach((w,m) => { if (w.date !== monthly.series[m].date || w.days !== days[m] || !close(w.equal_month_weight,1/12) || !close(w.calendar_day_weight,days[m]/total)) fail(); });
      const e = row.equal_month_mean_degC, c = row.calendar_day_mean_degC, d = row.calendar_minus_equal_degC, p = row.provider_annual;
      if (complete ? !finite(e) || !finite(c) || !close(d,c-e) : e !== null || c !== null || d !== null) fail();
      if (!p || p.expected_cells !== monthly.support.cell_count || !Number.isInteger(p.valid_cells) || p.valid_cells < 0 || p.valid_cells > p.expected_cells ||
          p.status !== (p.valid_cells===p.expected_cells?"complete":"incomplete") ||
          (p.status === "complete" ? !finite(p.area_weighted_mean_degC) : p.area_weighted_mean_degC !== null)) fail();
      for (const [key,v] of [["provider_minus_equal_degC",e],["provider_minus_calendar_degC",c]]) {
        if (v === null || p.area_weighted_mean_degC === null ? p[key] !== null : !close(p[key],p.area_weighted_mean_degC-v)) fail();
      }
    }
    const valid = a.series.filter((r) => r.status === "complete"), max = valid.length ? Math.max(...valid.map((r) => Math.abs(r.calendar_minus_equal_degC))) : null;
    if (a.quality?.expected_years !== a.series.length || a.quality.complete_years !== valid.length || !same(a.quality.incomplete_years,a.series.filter((r) => r.status !== "complete").map((r) => r.year)) ||
        a.quality.provider_complete_years !== a.series.filter((r) => r.provider_annual.status === "complete").length ||
        a.sensitivity?.valid_years !== valid.length || (max === null ? a.sensitivity.max_abs_calendar_minus_equal_degC !== null : !close(a.sensitivity.max_abs_calendar_minus_equal_degC,max)) ||
        !same(a.sensitivity.years_at_maximum,valid.filter((r) => Math.abs(r.calendar_minus_equal_degC) === max).map((r) => r.year))) fail();
  }
  return payload;
}

export function createComparisonReview(data, datasetSha256, selection) {
  if (!/^[a-f0-9]{64}$/.test(datasetSha256) || data?.schema_version !== "0.3.0" || data.output_type !== "recorded_temperature_web_preview" || data.data_mode !== "recorded_offline_replay" || data.selection_status !== "candidate" || data.inference_performed !== false || !Array.isArray(data.regions) || !data.regions.length || data.regions.length > 8 || new Set(data.regions.map((r) => r.id)).size !== data.regions.length) throw Error("Unsupported review source snapshot");
  if (!selection || canonical(Object.keys(selection).sort()) !== canonical(["left_id", "month", "policy", "right_id"]) || !Object.values(selection).every((v) => typeof v === "string")) throw Error("Invalid review selection");
  const regions = [selection.left_id, selection.right_id].map((id) => data.regions.find((r) => r.id === id));
  if (regions.some((r) => !r)) throw Error("Review refers to an unavailable region");
  const result = summarizeRegionDifferences(...regions, selection.policy);
  if (!result.compatible || !result.values.some((r) => r.date === selection.month) || canonical(data.dates) !== canonical(result.values.map((r) => r.date))) throw Error("Review selection cannot be compared in this snapshot");
  const definitions = regions.map((r) => {
    traceGraph(r.workflow_trace);
    if (r.workflow_trace.target !== "Sensitivity") throw Error("Unsupported review calculation target");
    return { region_id: r.id, context_sha256: r.workflow_trace.context_sha256,
      definition_fingerprint: r.workflow_trace.nodes.find((n) => n.id === "Sensitivity").definition_fingerprint };
  });
  return { schema_version: "0.1.0", output_type: "recorded_comparison_review", comparison_version: "0.1.0",
    selection_status: "candidate", data_mode: "recorded_offline_replay", inference_performed: false,
    dataset: { schema_version: data.schema_version, sha256: datasetSha256 },
    selection: { left_id: selection.left_id, right_id: selection.right_id, policy: selection.policy, month: selection.month },
    source_definitions: definitions, result,
    selected_month: result.values.find((r) => r.date === selection.month),
    scientific_acceptance: "not_performed", identity_authentication: "not_performed" };
}

export function verifyComparisonReview(report, data, datasetSha256) {
  if (report?.dataset?.sha256 !== datasetSha256) throw Error("Review uses a different dataset snapshot");
  const expected = createComparisonReview(data, datasetSha256, report.selection);
  if (canonical(report) !== canonical(expected)) throw Error("Review content differs from recomputed comparison");
  return expected;
}
