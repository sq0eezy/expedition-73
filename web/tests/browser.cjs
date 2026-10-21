/* Optional browser QA: Playwright + installed Chrome. Application needs neither. */
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const path = require('node:path');
const { chromium } = require(process.env.EXPEDITION73_PLAYWRIGHT || 'playwright');
const base = process.env.EXPEDITION73_PREVIEW_URL || 'http://127.0.0.1:8873/';
const format = (v) => v.toLocaleString('tr-TR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });

(async () => {
  const browser = await chromium.launch({ headless: true, channel: process.env.EXPEDITION73_BROWSER || 'chrome' });
  let checks = 0;
  const screenshots = path.join(__dirname, '../artifacts');
  await fs.mkdir(screenshots, { recursive: true });
  try {
    const page = await browser.newPage({ viewport: { width: 1440, height: 1100 }, acceptDownloads: true });
    const errors = [], requests = [];
    page.on('pageerror', (error) => errors.push(error.message));
    page.on('request', (request) => requests.push(request.url()));
    const response = await page.goto(base); assert.equal(response.status(), 200);
    const moduleResponse = await page.request.get(new URL('comparison.mjs', base).href);
    assert.equal(moduleResponse.status(), 200); assert.match(moduleResponse.headers()['content-type'], /javascript/);
    await page.locator('#results').waitFor({ state: 'visible' });
    const data = await (await page.request.get(new URL('data/results.json', base).href)).json();
    assert.equal(data.regions.length, 2);
    const checkMetrics = async (policy, month) => {
      const actual = await page.locator('#metrics .metric > strong').allTextContents();
      const a = data.regions[0].series[month][policy], b = data.regions[1].series[month][policy];
      assert.deepEqual(actual, [a, b, a - b].map((v) => format(v) + '°C'));
    };
    await checkMetrics('unmasked', 0); assert.equal(await page.locator('.chart-path').count(), 2);
    assert.equal(await page.locator('#data-table tbody tr').count(), 12); checks++;
    const comparisonCard = (id) => page.locator(`.comparison-card[data-region="${id}"]`);
    const six = (v) => v.toLocaleString('tr-TR', { minimumFractionDigits: 6, maximumFractionDigits: 6 });
    for (const region of data.regions) {
      const card = comparisonCard(region.id);
      for (const key of ['unmasked', 'land', 'land_and_ice']) assert.equal(await card.locator(`[data-policy="${key}"] td`).innerText(), six(region.series[0][key]) + ' °C');
      for (const id of ['land_minus_unmasked', 'land_ice_minus_land']) {
        const expected = region.diagnostics[`max_abs_${id}_degC`];
        assert.ok((await card.locator(`[data-contrast="${id}"] .contrast-peak`).innerText()).includes(six(expected) + ' °C'));
        assert.match(await card.locator(`[data-contrast="${id}"]`).innerText(), /12\/12 eşleşen ay/);
      }
    }
    assert.match(await comparisonCard('B').locator('[data-contrast="land_minus_unmasked"] .contrast-peak').innerText(), /Kasım/);
    assert.match(await comparisonCard('B').locator('[data-contrast="land_ice_minus_land"] .contrast-peak').innerText(), /Ekim/); checks++;
    assert.equal(data.schema_version, '0.3.0');
    assert.equal(await page.locator('#trace-graph .trace-node').count(), 5);
    assert.equal(await page.locator('#trace-graph .trace-edge').count(), 8);
    await page.locator('#trace-graph [data-node="Fractions"]').click();
    assert.match(await page.locator('#trace-detail').innerText(), /temperature ← Sıcaklık girdisi/);
    assert.ok((await page.locator('#trace-detail').innerText()).includes(data.regions[0].workflow_trace.nodes.find((n) => n.id === 'Fractions').definition_fingerprint)); checks++;
    await page.locator('#trace-region').selectOption('B');
    const summaryNode = page.locator('#trace-graph [data-node="Sensitivity"]');
    await summaryNode.focus(); await page.keyboard.press('Enter');
    assert.match(await page.locator('#trace-detail').innerText(), /land_and_ice ← Kara \+ buz ağırlığı/);
    assert.equal(await summaryNode.getAttribute('aria-pressed'), 'true'); checks++;
    const definitionText = await page.locator('#trace-detail').innerText();
    await page.locator('#month').fill('8'); await page.locator('#policy').selectOption('land');
    assert.equal(await page.locator('#trace-detail').innerText(), definitionText);
    await page.locator('#month').fill('0'); await page.locator('#policy').selectOption('unmasked');
    await page.locator('.trace-panel').screenshot({ path: path.join(screenshots, 'trace-desktop.png') }); checks++;

    assert.equal(await page.locator('#cell-grid [data-cell]').count(), 56);
    const aCell = data.regions[0].spatial.cells[9];
    await page.locator('#cell-grid [data-cell="9"]').click();
    assert.equal(await page.locator('#cell-detail h3').innerText(), format(aCell.series[0].value) + ' °C');
    assert.match(await page.locator('#cell-detail').innerText(), new RegExp(String(aCell.longitude).replace('.', '\\.')));
    assert.equal(await page.locator('#cell-grid [data-cell="9"]').getAttribute('aria-pressed'), 'true');
    await page.keyboard.press('ArrowRight');
    const nextIndex = data.regions[0].spatial.cells.findIndex((c) => c.longitude === aCell.longitude + 0.625 && c.latitude === aCell.latitude);
    assert.equal(await page.locator('#cell-grid [tabindex="0"]').getAttribute('data-cell'), String(nextIndex));
    assert.equal(await page.locator('#cell-grid [tabindex="0"]').evaluate((node) => node === document.activeElement), true); checks++;
    await page.locator('#spatial-region').selectOption('B');
    assert.equal(await page.locator('#cell-grid [data-cell]').count(), 55);
    const bCell = data.regions[1].spatial.cells[0];
    const originalFill = await page.locator('#cell-grid [data-cell="0"]').getAttribute('fill');
    await page.locator('#policy').selectOption('land_and_ice');
    await page.locator('.spatial-panel').screenshot({ path: path.join(screenshots, 'spatial-b.png') });
    assert.equal(await page.locator('#cell-grid [data-cell="0"]').getAttribute('fill'), originalFill);
    const areaText = (bCell.weights_m2.land_and_ice / 1e6).toLocaleString('tr-TR', { minimumFractionDigits: 3, maximumFractionDigits: 3 });
    assert.ok((await page.locator('#cell-detail').innerText()).includes(areaText + ' km²'));
    await page.locator('#month').fill('11');
    assert.equal(await page.locator('#cell-detail h3').innerText(), format(bCell.series[11].value) + ' °C');
    await page.locator('#spatial-region').selectOption('A'); await page.locator('#policy').selectOption('unmasked'); await page.locator('#month').fill('0'); checks++;
    await page.screenshot({ path: path.join(screenshots, 'desktop.png'), fullPage: true });
    await page.locator('.comparison-panel').screenshot({ path: path.join(screenshots, 'comparison-desktop.png') });
    await page.locator('.spatial-panel').screenshot({ path: path.join(screenshots, 'spatial-a.png') });
    await page.locator('#month').fill('6'); await checkMetrics('unmasked', 6);
    assert.equal(await page.locator('#month-label').innerText(), 'Temmuz');
    await page.locator('#policy').selectOption('land'); await checkMetrics('land', 6);
    assert.match(await page.locator('#comparison-month').innerText(), /Temmuz 2024/);
    assert.equal(await comparisonCard('B').locator('.chosen-policy').getAttribute('data-policy'), 'land');
    assert.equal(await comparisonCard('B').locator('[data-policy="land"] td').innerText(), six(data.regions[1].series[6].land) + ' °C'); checks++;
    assert.match(await page.locator('#support-note').innerText(), /güven aralığı veya sıcaklık hata payı değildir/); checks++;
    const pendingDownload = page.waitForEvent('download'); await page.locator('#download').click();
    const download = await pendingDownload;
    const exported = JSON.parse(await fs.readFile(await download.path(), 'utf-8'));
    assert.equal(exported.selected_policy, 'land'); assert.equal(exported.selected_month, '2024-07');
    assert.equal(exported.inference_performed, false); assert.deepEqual(exported.regions, data.regions); checks++;
    await page.getByRole('checkbox', { name: 'A · Colorado çevresi', exact: true }).uncheck();
    assert.equal(await page.locator('#spatial-region').inputValue(), 'B');
    assert.equal(await page.locator('#cell-grid [data-cell]').count(), 55);
    assert.equal(await page.locator('.chart-path').count(), 1);
    assert.equal(await page.locator('#metrics .metric').count(), 1);
    await page.getByRole('checkbox', { name: 'B · Kuzey Alaska', exact: true }).uncheck();
    assert.equal(await page.locator('#empty').isVisible(), true); assert.equal(await page.locator('#download').isDisabled(), true);
    assert.equal(await page.locator('#trace-graph .trace-node').count(), 0);
    assert.equal(await page.locator('#trace-detail').innerText(), '');
    assert.equal(await page.locator('#trace-region').isDisabled(), true); checks++;
    assert.match(await page.locator('#area-state').innerText(), /Pencere seçin/); checks++;
    assert.equal(await page.locator('#spatial-empty').isVisible(), true);
    assert.equal(await page.locator('#spatial-region').isDisabled(), true);
    assert.equal(await page.locator('#cell-grid [data-cell]').count(), 0);
    assert.equal(await page.locator('#comparison-empty').isVisible(), true);
    assert.equal(await page.locator('.comparison-card').count(), 0);
    await page.getByRole('checkbox', { name: 'A · Colorado çevresi', exact: true }).check();
    await page.getByRole('checkbox', { name: 'B · Kuzey Alaska', exact: true }).check();
    await page.locator('#provenance summary').click();
    assert.match(await page.locator('#provenance-content').innerText(), /62cccbedac8849e2a5e8de79c44dc37bed3757eb701ec74ce126def1ca5f4584/);
    assert.ok(requests.every((url) => new URL(url).origin === new URL(base).origin));
    assert.deepEqual(errors, []); checks++;
    await page.locator('#provenance summary').click();
    await page.setViewportSize({ width: 390, height: 844 });
    await page.waitForFunction(() => document.getElementById('chart').getAttribute('viewBox').startsWith('0 0 400'));
    assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.screenshot({ path: path.join(screenshots, 'mobile.png'), fullPage: true }); checks++;
    await page.locator('.comparison-panel').screenshot({ path: path.join(screenshots, 'comparison-mobile.png') });
    assert.equal(await page.locator('#trace-graph').getAttribute('viewBox'), '0 0 400 550');
    await page.locator('#trace-graph [data-node=LandIce]').click();
    assert.equal(await page.locator('#trace-detail h3').innerText(), 'Kara + buz ağırlığı');
    await page.locator('.trace-panel').screenshot({ path: path.join(screenshots, 'trace-mobile.png') }); checks++;
    const missing = await browser.newPage();
    await missing.route('**/data/results.json', async (route) => {
      const modified = structuredClone(data); modified.regions[0].series[5].unmasked = null;
      modified.regions[0].spatial.cells[0].series[5].value = null;
      await route.fulfill({ json: modified });
    });
    await missing.goto(base); await missing.locator('#results').waitFor({ state: 'visible' });
    await missing.locator('#month').fill('5');
    assert.equal(await missing.locator('#metrics .metric > strong').first().innerText(), 'Veri yok');
    assert.equal(await missing.locator('#metrics .difference > strong').innerText(), 'Veri yok');
    assert.equal((await missing.locator('.chart-path').first().getAttribute('d')).match(/M/g).length, 2); checks++;
    assert.equal(await missing.locator('#cell-detail h3').innerText(), 'Veri yok');
    assert.equal(await missing.locator('#cell-grid [data-cell="0"]').getAttribute('fill'), '#d7dcd4');
    assert.match(await missing.locator('#cell-detail').innerText(), /0,000 km² · sıcaklık eksik/); checks++;
    const missingComparison = missing.locator('.comparison-card[data-region="A"]');
    assert.equal(await missingComparison.locator('[data-contrast="land_minus_unmasked"] .contrast-value').innerText(), 'Veri yok');
    assert.match(await missingComparison.locator('[data-contrast="land_minus_unmasked"]').innerText(), /11\/12 eşleşen ay/);
    assert.match(await missingComparison.locator('[data-contrast="land_ice_minus_land"]').innerText(), /12\/12 eşleşen ay/); checks++;
    const allMissing = await browser.newPage();
    await allMissing.route('**/data/results.json', (route) => {
      const modified = structuredClone(data); modified.regions[0].series.forEach((r) => { r.land = null; });
      return route.fulfill({ json: modified });
    });
    await allMissing.goto(base); await allMissing.locator('#results').waitFor({ state: 'visible' });
    for (const id of ['land_minus_unmasked', 'land_ice_minus_land']) {
      const row = allMissing.locator(`.comparison-card[data-region="A"] [data-contrast="${id}"]`);
      assert.match(await row.innerText(), /En büyük \|fark\|: veri yok/);
      assert.match(await row.innerText(), /0\/12 eşleşen ay/);
    }
    await allMissing.close(); checks++;
    const failure = await browser.newPage();
    await failure.route('**/data/results.json', (route) => route.fulfill({ status: 503, body: 'unavailable' }));
    await failure.goto(base); await failure.locator('#error').waitFor({ state: 'visible' });
    assert.equal(await failure.locator('#results').isVisible(), false);
    await failure.unroute('**/data/results.json'); await failure.locator('#retry').click();
    await failure.locator('#results').waitFor({ state: 'visible' }); checks++;
    const invalid = await browser.newPage();
    await invalid.route('**/data/results.json', (route) => {
      const modified = structuredClone(data); modified.regions[0].variable.unit = 'K';
      return route.fulfill({ json: modified });
    });
    await invalid.goto(base); await invalid.locator('#error').waitFor({ state: 'visible' });
    assert.equal(await invalid.locator('#results').isVisible(), false); checks++;
    const incompatible = await browser.newPage();
    await incompatible.route('**/data/results.json', (route) => {
      const modified = structuredClone(data); modified.regions[1].time.provider_time_standard = 'UTC';
      return route.fulfill({ json: modified });
    });
    await incompatible.goto(base); await incompatible.locator('#error').waitFor({ state: 'visible' });
    assert.equal(await incompatible.locator('#results').isVisible(), false); checks++;
    for (const kind of ['weight', 'geometry', 'coverage', 'date', 'old-contract', 'trace-lineage', 'trace-missing', 'trace-cycle']) {
      const broken = await browser.newPage();
      await broken.route('**/data/results.json', (route) => {
        const modified = structuredClone(data), c = modified.regions[0].spatial.cells[0];
        if (kind === 'weight') c.weights_m2.land *= 0.5;
        if (kind === 'geometry') c.intersection_bbox[0] += 0.01;
        if (kind === 'coverage') modified.regions[0].spatial.cells.pop();
        if (kind === 'date') c.series[0].date = '2023-01';
        if (kind === 'old-contract') modified.schema_version = '0.2.0';
        if (kind === 'trace-lineage') modified.regions[0].workflow_trace.nodes[1].inputs[0].definition_fingerprint = '0'.repeat(64);
        if (kind === 'trace-missing') delete modified.regions[0].workflow_trace;
        if (kind === 'trace-cycle') modified.regions[0].workflow_trace.nodes.reverse();
        return route.fulfill({ json: modified });
      });
      await broken.goto(base); await broken.locator('#error').waitFor({ state: 'visible' });
      assert.equal(await broken.locator('#results').isVisible(), false); await broken.close(); checks++;
    }
    assert.deepEqual(errors, []);
    console.log(JSON.stringify({ status: 'passed', browser: 'Chrome headless', checks, javascript_errors: errors,
      external_runtime_requests: requests.filter((url) => new URL(url).origin !== new URL(base).origin).length,
      screenshots: ['web/artifacts/desktop.png', 'web/artifacts/mobile.png', 'web/artifacts/comparison-desktop.png', 'web/artifacts/comparison-mobile.png', 'web/artifacts/spatial-a.png', 'web/artifacts/spatial-b.png', 'web/artifacts/trace-desktop.png', 'web/artifacts/trace-mobile.png'] }));
  } finally { await browser.close(); }
})().catch((error) => { console.error(error); process.exitCode = 1; });
