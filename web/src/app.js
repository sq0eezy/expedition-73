import { summarizePolicyDifferences } from "./comparison.mjs";
import { traceGraph } from "./trace.mjs";

const $ = (id) => document.getElementById(id);
const months = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"];
const shortMonths = ["Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"];
const colors = ["#c77543", "#247c78", "#7466a1", "#777c39", "#a3536b", "#3878a6", "#8c6238", "#626c6a"];
const labels = { unmasked: "Bütün pencere · maskesiz", land: "Kara oranı · FRLAND (aday)", land_and_ice: "Kara + kara buzu (aday)" };
const state = { data: null, selected: new Set(), month: 0, policy: "unmasked", spatialRegion: null, cell: 0, traceRegion: null, traceNode: null };
const number = (value, digits = 2) => value === null ? "Veri yok" : value.toLocaleString("tr-TR", { minimumFractionDigits: digits, maximumFractionDigits: digits });
const el = (tag, text, className) => { const node = document.createElement(tag); if (text !== undefined) node.textContent = text; if (className) node.className = className; return node; };
const color = (region) => colors[state.data.regions.indexOf(region) % colors.length];
const named = (region) => region.display_name;
const active = () => state.data.regions.filter((region) => state.selected.has(region.id));
const value = (region, index) => region.series[index][state.policy];
const svg = (tag, attributes, text) => { const node = document.createElementNS("http://www.w3.org/2000/svg", tag); for (const [key, v] of Object.entries(attributes)) node.setAttribute(key, v); if (text !== undefined) node.textContent = text; return node; };

function validate(data) {
  if (data.schema_version !== "0.3.0" || data.output_type !== "recorded_temperature_web_preview" || data.data_mode !== "recorded_offline_replay" || data.selection_status !== "candidate" || data.inference_performed !== false) throw Error("Unsupported preview contract");
  if (!Array.isArray(data.dates) || data.dates.length !== 12 || !data.dates.every((d, i) => d === `${data.dates[0].slice(0, 4)}-${String(i + 1).padStart(2, "0")}`)) throw Error("Unsupported period");
  if (!Array.isArray(data.regions) || !data.regions.length || data.regions.length > 8 || new Set(data.regions.map((r) => r.id)).size !== data.regions.length) throw Error("Unsupported regions");
  let context;
  for (const region of data.regions) {
    if (typeof region.id !== "string" || typeof region.display_name !== "string" || !region.display_name.trim() || region.region.id !== region.id || region.region.selection_status !== "candidate" || region.variable.unit !== "degC" || region.variable.height_m !== 2 || region.variable.id !== "air_temperature_2m") throw Error("Unsupported indicator");
    if (region.series.length !== 12 || !region.series.every((row, i) => row.date === data.dates[i] && Object.keys(labels).every((key) => row[key] === null || typeof row[key] === "number" && Number.isFinite(row[key])))) throw Error("Invalid series");
    if (region.source_area.comparison_performed !== false || region.source_area.numeric_values_retrieved !== false) throw Error("Unexpected AREA claim");
    const provider = region.provenance.temperature;
    const signature = JSON.stringify([region.variable.id, region.variable.unit, region.variable.height_m, ...["frequency", "start", "end", "calendar", "provider_time_standard"].map((key) => region.time[key]), provider.provider, provider.product, provider.api_version, [...provider.sources].sort()]);
    if (context !== undefined && signature !== context) throw Error("Incompatible comparison context");
    context = signature;
    summarizePolicyDifferences(region.series);
    validateSpatial(region, data.dates);
    traceGraph(region.workflow_trace);
    for (const key of ["land", "land_and_ice"]) {
      const support = region.support.policies[key];
      if (![support.lower_fraction_of_window, support.uniform_fraction_of_window, support.upper_fraction_of_window].every((v) => typeof v === "number" && Number.isFinite(v) && v >= 0 && v <= 1)) throw Error("Invalid area support");
      if (support.lower_fraction_of_window > support.uniform_fraction_of_window || support.uniform_fraction_of_window > support.upper_fraction_of_window) throw Error("Invalid area bounds");
    }
  }
}

function validateSpatial(region, dates) {
  const s = region.spatial, bbox = region.region.candidate_bbox;
  const finite = (v) => typeof v === "number" && Number.isFinite(v);
  const bounds = (b) => Array.isArray(b) && b.length === 4 && b.every(finite) && b[0] < b[2] && b[1] < b[3] && b[0] >= -180 && b[2] <= 180 && b[1] >= -90 && b[3] <= 90;
  const close = (a, b) => Math.abs(a - b) <= Math.max(1, Math.abs(b)) * 1e-9;
  if (!s || s.geometry !== "reconstructed_midpoint_rectangles" || s.fraction_placement !== "uniform_within_full_cell_assumption" || s.longitude_step_deg !== 0.625 || s.latitude_step_deg !== 0.5 || s.area_radius_m !== 6371008.8 || !bounds(bbox) || !Array.isArray(s.cells) || !s.cells.length || s.cells.length !== region.support.cell_count) throw Error("Invalid spatial context");
  const keys = new Set(), sums = { unmasked: 0, land: 0, land_and_ice: 0 };
  for (const c of s.cells) {
    const key = `${c.longitude},${c.latitude}`, f = c.fractions, part = c.intersection_bbox;
    if (!finite(c.longitude) || !finite(c.latitude) || keys.has(key) || !bounds(c.full_cell_bbox) || !bounds(part)) throw Error("Invalid cell geometry");
    keys.add(key);
    const full = [c.longitude - 0.3125, c.latitude - 0.25, c.longitude + 0.3125, c.latitude + 0.25];
    const intersection = [Math.max(full[0], bbox[0]), Math.max(full[1], bbox[1]), Math.min(full[2], bbox[2]), Math.min(full[3], bbox[3])];
    if (!full.every((v, i) => close(v, c.full_cell_bbox[i])) || !intersection.every((v, i) => close(v, part[i])) || c.clipped !== full.some((v, i) => !close(v, part[i]))) throw Error("Invalid cell intersection");
    const area = s.area_radius_m ** 2 * (part[2] - part[0]) * Math.PI / 180 * (Math.sin(part[3] * Math.PI / 180) - Math.sin(part[1] * Math.PI / 180));
    if (!finite(c.intersection_area_m2) || !close(c.intersection_area_m2, area) || !f || !["FRLAND", "FRLANDICE", "FRLAKE", "FROCEAN"].every((k) => finite(f[k]) && f[k] >= 0 && f[k] <= 1) || Math.abs(f.FRLAND + f.FRLANDICE + f.FRLAKE + f.FROCEAN - 1) > 1e-6) throw Error("Invalid cell fractions or area");
    const factors = { unmasked: 1, land: f.FRLAND, land_and_ice: f.FRLAND + f.FRLANDICE };
    for (const policy of Object.keys(labels)) {
      if (!finite(c.weights_m2[policy]) || !close(c.weights_m2[policy], c.intersection_area_m2 * factors[policy])) throw Error("Invalid cell weight");
      sums[policy] += c.weights_m2[policy];
    }
    if (!Array.isArray(c.series) || c.series.length !== 12 || !c.series.every((r, i) => r.date === dates[i] && (r.value === null || finite(r.value)))) throw Error("Invalid cell series");
  }
  if (!close(sums.unmasked, region.support.window_area_m2) || !["land", "land_and_ice"].every((p) => close(sums[p], region.support.policies[p].uniform_estimate_m2))) throw Error("Cell coverage disagrees with aggregate");
}

function metric(title, temperature, note, region, difference = false) {
  const box = el("article", undefined, `metric${difference ? " difference" : ""}`);
  const head = el("div", undefined, "metric-head");
  if (region) { const dot = el("span", undefined, "swatch"); dot.style.setProperty("--region-color", color(region)); head.append(dot); }
  head.append(el("span", title));
  const big = el("strong", number(temperature)); if (temperature !== null) big.append(el("span", "°C"));
  box.append(head, big, el("small", note)); return box;
}

function renderMetrics(regions) {
  const fragment = document.createDocumentFragment();
  for (const region of regions) fragment.append(metric(`${region.id} · ${named(region)}`, value(region, state.month), `${months[state.month]} · aday pencere`, region));
  if (regions.length === 2) {
    const a = value(regions[0], state.month), b = value(regions[1], state.month);
    fragment.append(metric(`${regions[0].id} − ${regions[1].id} · seçili ay farkı`, a === null || b === null ? null : a - b, "Mekânsal fark · iklim eğilimi değildir", null, true));
  }
  $("metrics").replaceChildren(fragment);
  $("metrics").style.gridTemplateColumns = `repeat(${Math.min(3, regions.length === 2 ? 3 : Math.max(1, regions.length))},minmax(0,1fr))`;
}

function renderChart(regions) {
  const chart = $("chart"); chart.replaceChildren(svg("title", { id: "chart-title" }, `${state.data.dates[0].slice(0, 4)} aylık 2 metre hava sıcaklığı`), svg("desc", { id: "chart-desc" }, "Seçili aday pencerelerin aylık serileri. Sayısal değerler aşağıdaki erişilebilir tabloda da bulunur. Eksik aylar birleştirilmez."));
  $("empty").hidden = regions.length > 0; $("chart-wrap").hidden = regions.length === 0;
  const values = regions.flatMap((r) => r.series.map((_, i) => value(r, i))).filter((v) => v !== null);
  const min = Math.floor((Math.min(0, ...values) - 2) / 10) * 10;
  const max = Math.ceil((Math.max(0, ...values) + 2) / 10) * 10;
  const compact = window.matchMedia("(max-width:740px)").matches;
  const width = compact ? 400 : 920;
  const left = compact ? 34 : 45, right = width - (compact ? 14 : 25), top = 18, bottom = compact ? 220 : 251;
  chart.setAttribute("viewBox", `0 0 ${width} ${bottom + 39}`);
  const x = (i) => left + i / 11 * (right - left), y = (v) => bottom - (v - min) / (max - min) * (bottom - top);
  for (let tick = min; tick <= max; tick += 10) {
    chart.append(svg("line", { x1: left, y1: y(tick), x2: right, y2: y(tick), class: tick === 0 ? "chart-grid chart-zero" : "chart-grid" }), svg("text", { x: left - 13, y: y(tick) + 3, "text-anchor": "end", class: "chart-text" }, String(tick)));
  }
  for (let i = 0; i < 12; i++) if (!compact || [0, 2, 4, 6, 8, 11].includes(i)) chart.append(svg("text", { x: x(i), y: bottom + 24, "text-anchor": "middle", class: "chart-text" }, shortMonths[i]));
  chart.append(svg("line", { x1: x(state.month), y1: top, x2: x(state.month), y2: bottom, class: "chart-focus" }));
  for (const region of regions) {
    let path = "", connected = false;
    region.series.forEach((_, i) => { const v = value(region, i); if (v === null) { connected = false; return; } path += `${connected ? "L" : "M"}${x(i)},${y(v)} `; connected = true; });
    const line = svg("path", { d: path, class: "chart-path", "data-region": region.id }); line.style.setProperty("--region-color", color(region)); chart.append(line);
    const current = value(region, state.month);
    if (current !== null) { const point = svg("circle", { cx: x(state.month), cy: y(current), r: 5, class: "chart-point" }); point.style.setProperty("--region-color", color(region)); point.append(svg("title", {}, `${region.id} · ${months[state.month]}: ${number(current)} °C`)); chart.append(point); }
  }
  $("legend").replaceChildren(...regions.map((r) => { const item = el("span", undefined, "legend-item"); item.style.setProperty("--region-color", color(r)); item.append(el("span", undefined, "legend-line"), el("span", `${r.id} · ${named(r)}`)); return item; }));
  $("chart-caption").textContent = `${labels[state.policy]}. Kayıtlı aylık grid sıcaklıkları; eksik aylar boş bırakılır. Dikey ölçek, görünür serilere göre değişir.`;
}

function renderSupport(regions) {
  $("support").replaceChildren(...regions.map((region) => {
    const row = el("div", undefined, "support-row"); row.style.setProperty("--region-color", color(region));
    const estimate = state.policy === "unmasked" ? 1 : region.support.policies[state.policy].uniform_fraction_of_window;
    const top = el("div", undefined, "support-top"); top.append(el("span", `${region.id} · ${named(region)}`), el("strong", state.policy === "unmasked" ? "Bütün pencere" : `%${number(estimate * 100, 3)}`));
    const bar = el("div", undefined, "support-bar"); const fill = el("span"); fill.style.setProperty("--coverage", `${Math.min(100, Math.max(0, estimate * 100))}%`); bar.append(fill);
    let caption = `${region.support.cell_count} hücre · ${region.support.clipped_cells} sınırdan kesilmiş hücre`;
    if (state.policy !== "unmasked") { const p = region.support.policies[state.policy]; caption = `Koşullu alan aralığı: %${number(p.lower_fraction_of_window * 100, 3)}–%${number(p.upper_fraction_of_window * 100, 3)}`; }
    row.append(top, bar, el("p", caption, "support-caption")); return row;
  }));
  $("support-note").textContent = state.policy === "unmasked" ? "Alan, aday dikdörtgen ile grid hücrelerinin kesişiminden hesaplanır. Kara, göl, buz ve okyanus ayrımı uygulanmaz." : "Oran, tam hücredeki fraksiyonun kesilen parçada da aynı olduğu varsayımına dayanır. Aralık, bu yerleşim varsayımının koşullu sınırıdır; güven aralığı veya sıcaklık hata payı değildir.";
}

function renderSources(regions) {
  if (!regions.length) { $("area-state").replaceChildren(el("span", "Kaynak AREA karşılaştırması"), el("strong", "Pencere seçin")); $("provenance-content").replaceChildren(); return; }
  const anyArea = regions.some((r) => r.source_area.numeric_declaration_present);
  $("area-state").replaceChildren(el("span", "Kaynak AREA karşılaştırması"), el("strong", anyArea ? "Değerler doğrulanmadı" : "AREA metaveride bulunmuyor"));
  $("provenance-content").replaceChildren(...regions.map((region) => {
    const p = region.provenance, box = el("div", undefined, "provenance-block");
    box.append(el("strong", `${region.id} · ${named(region)} / aday`), el("p", region.region.label), el("p", `Sınır [batı, güney, doğu, kuzey]: ${region.region.candidate_bbox.join(", ")}°`), el("p", `Zaman: ${region.time.provider_time_standard} · ${region.time.calendar}`), el("p", `T2M kaydı: ${p.temperature.retrieved_at}`), el("p", `Fraksiyon kaydı: ${p.surface_fractions.retrieved_at}`));
    const link = el("a", "NASA fraksiyon kaynak sorgusu ↗"); const uri = new URL(p.surface_fractions.uri); if (uri.protocol === "https:") { link.href = uri.href; link.target = "_blank"; link.rel = "noopener noreferrer"; box.append(link); }
    const sha = p.surface_fractions.response_sha256; box.append(el("p", `Ham fraksiyon SHA-256: ${sha}`, "hash")); return box;
  }));
}

function renderTable(regions) {
  const head = el("thead"), header = el("tr"); header.append(el("th", "Ay"));
  for (const region of regions) header.append(el("th", `${region.id} · °C`)); head.append(header);
  const body = el("tbody");
  state.data.dates.forEach((date, i) => { const tr = el("tr"); tr.append(el("td", `${months[i]} ${date.slice(0, 4)}`)); for (const r of regions) tr.append(el("td", number(value(r, i), 6))); body.append(tr); });
  $("data-table").replaceChildren(el("caption", `${labels[state.policy]} · kayıtlı aylık sıcaklıklar`), head, body);
}

function renderComparison(regions) {
  $("comparison-month").textContent = `${months[state.month]} ${state.data.dates[state.month].slice(0, 4)}`;
  $("comparison-empty").hidden = regions.length > 0;
  const signed = (v) => v === null ? "Veri yok" : `${v >= 0.0000005 ? "+" : ""}${number(Math.abs(v) < 0.0000005 ? 0 : v, 6)} °C`;
  $("comparison-cards").replaceChildren(...regions.map((region) => {
    const box = el("article", undefined, "comparison-card"); box.dataset.region = region.id;
    const head = el("h3", `${region.id} · ${named(region)}`); head.style.setProperty("--region-color", color(region));
    const table = el("table"); table.append(el("caption", "Seçili ay · üç ağırlık seçeneği"));
    const body = el("tbody");
    for (const [policy, label] of Object.entries(labels)) {
      const row = el("tr"); row.dataset.policy = policy; if (policy === state.policy) row.className = "chosen-policy";
      const th = el("th", label); th.scope = "row"; if (policy === state.policy) th.append(el("span", "Grafikte", "comparison-tag"));
      const temperature = region.series[state.month][policy];
      row.append(th, el("td", temperature === null ? "Veri yok" : `${number(temperature, 6)} °C`)); body.append(row);
    }
    table.append(body); box.append(head, table);
    for (const contrast of summarizePolicyDifferences(region.series)) {
      const row = el("div", undefined, "contrast-row"); row.dataset.contrast = contrast.id;
      const top = el("div", undefined, "contrast-top"); top.append(el("span", contrast.label), el("strong", signed(contrast.values[state.month].delta), "contrast-value"));
      let peak = "En büyük |fark|: veri yok";
      if (contrast.max_abs_delta_degC !== null) {
        const dates = contrast.max_abs_dates.length === 12 ? "12 ay eşit" : contrast.max_abs_dates.map((date) => months[Number(date.slice(-2)) - 1]).join(", ");
        peak = `En büyük |fark|: ${number(contrast.max_abs_delta_degC, 6)} °C · ${dates}`;
      }
      row.append(top, el("p", peak, "contrast-peak"), el("p", `${contrast.valid_months}/12 eşleşen ay · yalnız bu iki seri için`, "detail-note")); box.append(row);
    }
    return box;
  }));
}

function renderSpatial(regions) {
  $("spatial-empty").hidden = regions.length > 0;
  $("spatial-content").hidden = regions.length === 0;
  $("spatial-region").disabled = !regions.length;
  $("spatial-region").replaceChildren(...regions.map((r) => { const option = el("option", `${r.id} · ${named(r)}`); option.value = r.id; return option; }));
  if (!regions.length) { state.spatialRegion = null; $("cell-grid").replaceChildren(); $("cell-detail").replaceChildren(); return; }
  if (!regions.some((r) => r.id === state.spatialRegion)) { state.spatialRegion = regions[0].id; state.cell = 0; }
  $("spatial-region").value = state.spatialRegion;
  const region = regions.find((r) => r.id === state.spatialRegion), cells = region.spatial.cells;
  state.cell = Math.min(state.cell, cells.length - 1);
  const temperatures = state.data.regions.flatMap((r) => r.spatial.cells.flatMap((c) => c.series.map((row) => row.value))).filter((v) => v !== null);
  const low = temperatures.length ? Math.floor(Math.min(...temperatures) / 10) * 10 : 0;
  const high = temperatures.length ? Math.max(low + 10, Math.ceil(Math.max(...temperatures) / 10) * 10) : 10;
  const fill = (v) => {
    if (v === null) return "#d7dcd4";
    const t = (v - low) / (high - low), a = t < .5 ? [53, 110, 159] : [244, 245, 239], b = t < .5 ? [244, 245, 239] : [199, 117, 67], f = t < .5 ? t * 2 : (t - .5) * 2;
    return `rgb(${a.map((n, i) => Math.round(n + (b[i] - n) * f)).join(",")})`;
  };
  $("scale-low").textContent = number(low, 0); $("scale-high").textContent = number(high, 0);
  $("spatial-context").textContent = `${region.id} · ${months[state.month]} ${state.data.dates[0].slice(0, 4)} · ${cells.length} hücre · 0,625° boylam × 0,5° enlem. Sınır [B, G, D, K]: ${region.region.candidate_bbox.join(", ")}°.`;
  const minX = Math.min(...cells.map((c) => c.full_cell_bbox[0])), maxX = Math.max(...cells.map((c) => c.full_cell_bbox[2]));
  const minY = Math.min(...cells.map((c) => c.full_cell_bbox[1])), maxY = Math.max(...cells.map((c) => c.full_cell_bbox[3]));
  const x = (lon) => 57 + (lon - minX) / (maxX - minX) * 440, y = (lat) => 290 - (lat - minY) / (maxY - minY) * 267;
  const box = (b) => ({ x: x(b[0]), y: y(b[3]), width: x(b[2]) - x(b[0]), height: y(b[1]) - y(b[3]) });
  const grid = $("cell-grid"); grid.replaceChildren(svg("title", {}, `${named(region)} · kayıtlı grid hücreleri`));
  cells.forEach((c, i) => {
    grid.append(svg("rect", { ...box(c.full_cell_bbox), class: "full-cell", "aria-hidden": "true" }));
    const v = c.series[state.month].value, selected = i === state.cell;
    const rect = svg("rect", { ...box(c.intersection_bbox), fill: fill(v), class: "grid-cell", role: "button", tabindex: selected ? "0" : "-1", "aria-pressed": String(selected), "data-cell": i, "aria-label": `Hücre merkezi ${c.longitude}°, ${c.latitude}°; ${months[state.month]}: ${v === null ? "veri yok" : number(v) + " °C"}` });
    const select = (index, focus) => { state.cell = index; renderSpatial(regions); if (focus) grid.querySelector(`[data-cell="${index}"]`).focus({ preventScroll: true }); };
    rect.addEventListener("click", () => select(i, true));
    rect.addEventListener("keydown", (event) => {
      if (["Enter", " "].includes(event.key)) { event.preventDefault(); select(i, true); return; }
      const offset = { ArrowRight: [0.625, 0], ArrowLeft: [-0.625, 0], ArrowUp: [0, 0.5], ArrowDown: [0, -0.5] }[event.key];
      if (!offset) return; event.preventDefault();
      const next = cells.findIndex((other) => other.longitude === c.longitude + offset[0] && other.latitude === c.latitude + offset[1]);
      if (next >= 0) select(next, true);
    });
    rect.append(svg("title", {}, rect.getAttribute("aria-label"))); grid.append(rect);
  });
  grid.append(svg("rect", { ...box(region.region.candidate_bbox), class: "candidate-outline", "aria-hidden": "true" }));
  const chosen = cells[state.cell], center = [(chosen.intersection_bbox[0] + chosen.intersection_bbox[2]) / 2, (chosen.intersection_bbox[1] + chosen.intersection_bbox[3]) / 2];
  grid.append(svg("circle", { cx: x(center[0]), cy: y(center[1]), r: 5, class: "selected-cell-mark", "aria-hidden": "true" }));
  for (const lon of [minX, maxX]) grid.append(svg("text", { x: x(lon), y: 310, "text-anchor": lon === minX ? "start" : "end", class: "spatial-axis" }, `${number(lon, 3)}°`));
  for (const lat of [minY, maxY]) grid.append(svg("text", { x: 50, y: y(lat) + 4, "text-anchor": "end", class: "spatial-axis" }, `${number(lat, 2)}°`));
  grid.append(svg("text", { x: 277, y: 333, "text-anchor": "middle", class: "spatial-axis" }, "Boylam → · Enlem ↑"));
  const detail = $("cell-detail"), temperature = chosen.series[state.month].value;
  const total = cells.reduce((sum, c) => sum + (c.series[state.month].value === null ? 0 : c.weights_m2[state.policy]), 0);
  const effective = temperature === null ? 0 : chosen.weights_m2[state.policy];
  const table = el("dl", undefined, "cell-facts");
  const fact = (name, text) => table.append(el("dt", name), el("dd", text));
  fact("Hücre merkezi (boylam, enlem)", `${chosen.longitude}°, ${chosen.latitude}°`);
  fact("Sınır kesişimi", chosen.clipped ? "Tam hücrenin bir parçası" : "Tam hücre");
  fact("Kesişim alanı · pilot küresi", `${number(chosen.intersection_area_m2 / 1e6, 3)} km²`);
  fact("Seçili ağırlığın etkin alanı", `${number(effective / 1e6, 3)} km²${temperature === null ? " · sıcaklık eksik" : ""}`);
  fact("Bu ayın geçerli alanındaki payı", total > 0 ? `%${number(effective / total * 100, 3)}` : "Veri yok");
  for (const [key, label] of Object.entries({ FRLAND: "Kara", FRLANDICE: "Kara buzu", FRLAKE: "Göl", FROCEAN: "Okyanus" })) fact(`${label} · tam hücre oranı`, `%${number(chosen.fractions[key] * 100, 4)}`);
  detail.replaceChildren(el("span", "SEÇİLİ HÜCRE", "section-label"), el("h3", temperature === null ? "Veri yok" : `${number(temperature)} °C`), el("p", `${months[state.month]} · grid T2M · ${labels[state.policy]}`, "detail-note"), table);
}

const traceLabels = { Temperature: "Sıcaklık girdisi", Fractions: "Fraksiyon kontrolü", Land: "Kara ağırlığı", LandIce: "Kara + buz ağırlığı", Sensitivity: "Karşılaştırma" };
function renderTrace(regions) {
  const select = $("trace-region"), graph = $("trace-graph"), detail = $("trace-detail");
  select.replaceChildren(...regions.map((r) => { const option = el("option", `${r.id} · ${named(r)}`); option.value = r.id; return option; }));
  const region = regions.find((r) => r.id === state.traceRegion) || regions[0];
  $("trace-empty").hidden = !!region; $("trace-content").hidden = !region; select.disabled = !region;
  graph.replaceChildren(); detail.replaceChildren();
  if (!region) { state.traceRegion = null; state.traceNode = null; return; }
  state.traceRegion = region.id; select.value = region.id;
  const compact = window.matchMedia("(max-width:740px)").matches;
  const trace = region.workflow_trace, layout = traceGraph(trace, compact);
  const selected = layout.nodes.find((n) => n.id === state.traceNode) || layout.nodes.at(-1);
  state.traceNode = selected.id;
  $("trace-summary").textContent = `${region.id} · ${layout.nodes.length} adım · ${layout.edges.length} veri bağlantısı · her adım 1 kez çalıştı`;
  graph.setAttribute("viewBox", `0 0 ${layout.width} ${layout.height}`);
  const marker = svg("marker", { id: "trace-arrow", viewBox: "0 0 10 10", refX: 9, refY: 5, markerWidth: 6, markerHeight: 6, orient: "auto-start-reverse" }); marker.append(svg("path", { d: "M0,0 L10,5 L0,10 Z" }));
  const defs = svg("defs", {}); defs.append(marker); graph.append(defs);
  layout.edges.forEach((edge, i) => {
    const a = layout.nodes.find((n) => n.id === edge.from), b = layout.nodes.find((n) => n.id === edge.to);
    const x1 = a.x + 160, x2 = b.x, y1 = a.y, y2 = b.y;
    const d = compact ? (b.y - a.y > 160 ? `M${a.x + 80},${a.y + 33} L${a.x + 80},${a.y + 48} L${8 + i * 3},${a.y + 48} L${8 + i * 3},${b.y - 48} L${b.x + 80},${b.y - 48} L${b.x + 80},${b.y - 33}` : `M${a.x + 80},${a.y + 33} C${a.x + 80},${a.y + 80} ${b.x + 80},${b.y - 80} ${b.x + 80},${b.y - 33}`) : x2 - x1 > 100 ? `M${x1},${y1} L${x1 + 12},${y1} L${x1 + 12},${20 + i * 8} L${x2 - 14},${20 + i * 8} L${x2 - 14},${y2} L${x2},${y2}` : `M${x1},${y1} C${x1 + 25},${y1} ${x2 - 25},${y2} ${x2},${y2}`;
    const path = svg("path", { d, class: "trace-edge", "marker-end": "url(#trace-arrow)", "data-from": edge.from, "data-to": edge.to }); path.append(svg("title", {}, `${edge.from} → ${edge.to} · ${edge.alias}`)); graph.append(path);
  });
  for (const node of layout.nodes) {
    const group = svg("g", { transform: `translate(${node.x},${node.y - 33})`, class: "trace-node", role: "button", tabindex: "0", "aria-pressed": String(node.id === selected.id), "aria-label": `${traceLabels[node.id] || node.id} · tamamlandı · 1 çalıştırma`, "data-node": node.id });
    group.append(svg("rect", { width: 160, height: 66, rx: 10 }), svg("text", { x: 12, y: 25, class: "trace-label" }, traceLabels[node.id] || node.id), svg("text", { x: 12, y: 47, class: "trace-status" }, "✓ Tamamlandı · 1 kez"));
    const choose = () => { state.traceNode = node.id; renderTrace(regions); graph.querySelector(`[data-node="${node.id}"]`).focus({ preventScroll: true }); };
    group.addEventListener("click", choose); group.addEventListener("keydown", (event) => { if (["Enter", " "].includes(event.key)) { event.preventDefault(); choose(); } }); graph.append(group);
  }
  const dl = el("dl", undefined, "trace-facts");
  const fact = (label, value) => dl.append(el("dt", label), el("dd", value));
  fact("İşlem / sürüm", `${selected.operation} / ${selected.operation_version}`);
  fact("Çıktı sözleşmesi", `${selected.output_contract.type} · ${selected.output_contract.schema_version} · ${selected.output_contract.unit}`);
  fact("Aldığı girdiler", selected.inputs.length ? selected.inputs.map((i) => `${i.alias} ← ${traceLabels[i.node] || i.node}`).join("; ") : "Üst modül girdisi yok; kayıtlı kaynaklar doğrulanır.");
  fact("İş tanımı kimliği · SHA-256", selected.definition_fingerprint);
  detail.append(el("span", "SEÇİLİ ADIM", "section-label"), el("h3", traceLabels[selected.id] || selected.id), dl);
}

function render() {
  const regions = active();
  $("month-label").textContent = months[state.month]; $("month").setAttribute("aria-valuetext", `${months[state.month]} ${state.data.dates[0].slice(0, 4)}`);
  renderTrace(regions); renderMetrics(regions); renderChart(regions); renderComparison(regions); renderSpatial(regions); renderSupport(regions); renderSources(regions); renderTable(regions);
  $("download").disabled = !regions.length;
}

async function load() {
  $("loading").hidden = false; $("results").hidden = true; $("error").hidden = true;
  try {
    const response = await fetch("./data/results.json", { cache: "no-store" }); if (!response.ok) throw Error("Data unavailable");
    const data = await response.json(); validate(data); state.data = data; state.selected = new Set(data.regions.map((r) => r.id));
    state.month = 0; state.policy = "unmasked"; state.spatialRegion = null; state.cell = 0; state.traceRegion = null; state.traceNode = null; $("policy").value = state.policy; $("month").value = "0";
    const year = data.dates[0].slice(0, 4); $("scope-year").textContent = `${year} · 12 ay`; $("year-mark").textContent = year;
    $("dataset-note").textContent = `Kayıtlı ${year} örnekleri · Aday sınırlar · Bilimsel profil incelemede`;
    $("region-options").replaceChildren(...data.regions.map((region) => {
      const label = el("label", undefined, "region-option"), checkbox = el("input"); checkbox.type = "checkbox"; checkbox.checked = true; checkbox.value = region.id; checkbox.setAttribute("aria-label", `${region.id} · ${named(region)}`);
      checkbox.addEventListener("change", () => { if (checkbox.checked) state.selected.add(region.id); else state.selected.delete(region.id); render(); });
      const dot = el("span", undefined, "swatch"); dot.style.setProperty("--region-color", color(region)); label.append(checkbox, dot, el("span", `${region.id} · ${named(region)}`)); return label;
    }));
    render(); $("results").hidden = false;
  } catch { $("error").hidden = false; }
  finally { $("loading").hidden = true; }
}

$("policy").addEventListener("change", () => { state.policy = $("policy").value; render(); });
$("month").addEventListener("input", () => { state.month = Number($("month").value); render(); });
$("trace-region").addEventListener("change", () => { state.traceRegion = $("trace-region").value; state.traceNode = null; renderTrace(active()); });
$("retry").addEventListener("click", load);
$("spatial-region").addEventListener("change", () => { state.spatialRegion = $("spatial-region").value; state.cell = 0; renderSpatial(active()); });
window.matchMedia("(max-width:740px)").addEventListener("change", () => { if (state.data) { renderChart(active()); renderTrace(active()); } });
$("download").addEventListener("click", () => {
  const selected = { schema_version: state.data.schema_version, selection_status: "candidate", data_mode: state.data.data_mode, inference_performed: false, selected_policy: state.policy, selected_month: state.data.dates[state.month], regions: active() };
  const url = URL.createObjectURL(new Blob([JSON.stringify(selected, null, 2)], { type: "application/json" }));
  const link = el("a"); link.href = url; link.download = "expedition73-temperature-preview.json"; document.body.append(link); link.click(); link.remove(); setTimeout(() => URL.revokeObjectURL(url), 1000);
});
load();
