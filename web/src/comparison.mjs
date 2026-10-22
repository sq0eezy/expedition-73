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

export async function datasetDigest(bytes) {
  if (!(bytes instanceof Uint8Array) || !bytes.length || bytes.length > 8_000_000) throw Error("Invalid dataset byte size");
  const digest = await globalThis.crypto.subtle.digest("SHA-256", bytes);
  return [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, "0")).join("");
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
