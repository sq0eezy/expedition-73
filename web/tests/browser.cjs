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
    await page.screenshot({ path: path.join(screenshots, 'desktop.png'), fullPage: true });
    await page.locator('#month').fill('6'); await checkMetrics('unmasked', 6);
    assert.equal(await page.locator('#month-label').innerText(), 'Temmuz');
    await page.locator('#policy').selectOption('land'); await checkMetrics('land', 6);
    assert.match(await page.locator('#support-note').innerText(), /güven aralığı veya sıcaklık hata payı değildir/); checks++;
    const pendingDownload = page.waitForEvent('download'); await page.locator('#download').click();
    const download = await pendingDownload;
    const exported = JSON.parse(await fs.readFile(await download.path(), 'utf-8'));
    assert.equal(exported.selected_policy, 'land'); assert.equal(exported.selected_month, '2024-07');
    assert.equal(exported.inference_performed, false); assert.deepEqual(exported.regions, data.regions); checks++;
    await page.getByRole('checkbox', { name: 'A · Colorado çevresi', exact: true }).uncheck();
    assert.equal(await page.locator('.chart-path').count(), 1);
    assert.equal(await page.locator('#metrics .metric').count(), 1);
    await page.getByRole('checkbox', { name: 'B · Kuzey Alaska', exact: true }).uncheck();
    assert.equal(await page.locator('#empty').isVisible(), true); assert.equal(await page.locator('#download').isDisabled(), true);
    assert.match(await page.locator('#area-state').innerText(), /Pencere seçin/); checks++;
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
    const missing = await browser.newPage();
    await missing.route('**/data/results.json', async (route) => {
      const modified = structuredClone(data); modified.regions[0].series[5].unmasked = null;
      await route.fulfill({ json: modified });
    });
    await missing.goto(base); await missing.locator('#results').waitFor({ state: 'visible' });
    await missing.locator('#month').fill('5');
    assert.equal(await missing.locator('#metrics .metric > strong').first().innerText(), 'Veri yok');
    assert.equal(await missing.locator('#metrics .difference > strong').innerText(), 'Veri yok');
    assert.equal((await missing.locator('.chart-path').first().getAttribute('d')).match(/M/g).length, 2); checks++;
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
    console.log(JSON.stringify({ status: 'passed', browser: 'Chrome headless', checks, javascript_errors: errors,
      external_runtime_requests: requests.filter((url) => new URL(url).origin !== new URL(base).origin).length,
      screenshots: ['web/artifacts/desktop.png', 'web/artifacts/mobile.png'] }));
  } finally { await browser.close(); }
})().catch((error) => { console.error(error); process.exitCode = 1; });
