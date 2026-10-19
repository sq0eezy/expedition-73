const $ = (id) => document.getElementById(id);
const months = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"];
const shortMonths = ["Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"];
const colors = ["#c77543", "#247c78", "#7466a1", "#777c39", "#a3536b", "#3878a6", "#8c6238", "#626c6a"];
const labels = { unmasked: "Bütün pencere · maskesiz", land: "Kara oranı · FRLAND (aday)", land_and_ice: "Kara + kara buzu (aday)" };
const state = { data: null, selected: new Set(), month: 0, policy: "unmasked" };
const number = (value, digits = 2) => value === null ? "Veri yok" : value.toLocaleString("tr-TR", { minimumFractionDigits: digits, maximumFractionDigits: digits });
const el = (tag, text, className) => { const node = document.createElement(tag); if (text !== undefined) node.textContent = text; if (className) node.className = className; return node; };
const color = (region) => colors[state.data.regions.indexOf(region) % colors.length];
const named = (region) => region.display_name;
const active = () => state.data.regions.filter((region) => state.selected.has(region.id));
const value = (region, index) => region.series[index][state.policy];
const svg = (tag, attributes, text) => { const node = document.createElementNS("http://www.w3.org/2000/svg", tag); for (const [key, v] of Object.entries(attributes)) node.setAttribute(key, v); if (text !== undefined) node.textContent = text; return node; };

function validate(data) {
  if (data.schema_version !== "0.1.0" || data.output_type !== "recorded_temperature_web_preview" || data.data_mode !== "recorded_offline_replay" || data.selection_status !== "candidate" || data.inference_performed !== false) throw Error("Unsupported preview contract");
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
    for (const key of ["land", "land_and_ice"]) {
      const support = region.support.policies[key];
      if (![support.lower_fraction_of_window, support.uniform_fraction_of_window, support.upper_fraction_of_window].every((v) => typeof v === "number" && Number.isFinite(v) && v >= 0 && v <= 1)) throw Error("Invalid area support");
      if (support.lower_fraction_of_window > support.uniform_fraction_of_window || support.uniform_fraction_of_window > support.upper_fraction_of_window) throw Error("Invalid area bounds");
    }
  }
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

function render() {
  const regions = active();
  $("month-label").textContent = months[state.month]; $("month").setAttribute("aria-valuetext", `${months[state.month]} ${state.data.dates[0].slice(0, 4)}`);
  renderMetrics(regions); renderChart(regions); renderSupport(regions); renderSources(regions); renderTable(regions);
  $("download").disabled = !regions.length;
}

async function load() {
  $("loading").hidden = false; $("results").hidden = true; $("error").hidden = true;
  try {
    const response = await fetch("./data/results.json", { cache: "no-store" }); if (!response.ok) throw Error("Data unavailable");
    const data = await response.json(); validate(data); state.data = data; state.selected = new Set(data.regions.map((r) => r.id));
    state.month = 0; state.policy = "unmasked"; $("policy").value = state.policy; $("month").value = "0";
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
$("retry").addEventListener("click", load);
window.matchMedia("(max-width:740px)").addEventListener("change", () => { if (state.data) renderChart(active()); });
$("download").addEventListener("click", () => {
  const selected = { schema_version: "0.1.0", selection_status: "candidate", data_mode: state.data.data_mode, inference_performed: false, selected_policy: state.policy, selected_month: state.data.dates[state.month], regions: active() };
  const url = URL.createObjectURL(new Blob([JSON.stringify(selected, null, 2)], { type: "application/json" }));
  const link = el("a"); link.href = url; link.download = "expedition73-temperature-preview.json"; document.body.append(link); link.click(); link.remove(); setTimeout(() => URL.revokeObjectURL(url), 1000);
});
load();
