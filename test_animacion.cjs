// Ejecutar con Playwright disponible: NODE_PATH=/ruta/node_modules node test_animacion.cjs
const {chromium} = require('playwright');
const assert = require('node:assert/strict');
const {execFileSync} = require('node:child_process');
const {mkdtempSync, rmSync, mkdirSync} = require('node:fs');
const {tmpdir} = require('node:os');
const {join} = require('node:path');
const {pathToFileURL} = require('node:url');

(async () => {
  const dir = mkdtempSync(join(tmpdir(), 'transformer-'));
  const file = join(dir, 'preview.html');
  execFileSync(process.env.PYTHON || 'python3', ['-c', `
import sys
from pathlib import Path
from proceso_transformer import crear_diagrama
sample = dict(muestra_texto='Hola mundo', muestra_tokens=['▁Hola','▁mundo'], muestra_ids=[123,456],
    salida_tokens=['<pad>','▁Hello','▁world','</s>'], salida_ids=[65000,78,91,0], especiales=[65000,0],
    capas_encoder=6, capas_decoder=6, cabezas=8, dimension=512, traduccion='Hello world')
Path(sys.argv[1]).write_text(crear_diagrama('Hola mundo', sample))
`, file], {cwd:__dirname});
  const browser = await chromium.launch({channel:'chrome', headless:true, args:['--no-sandbox']});
  try {
    const page = await browser.newPage({viewport:{width:1440, height:1120}});
    const errors = []; page.on('pageerror', e => errors.push(e.message));
    await page.goto(pathToFileURL(file).href);
    await page.waitForFunction(() => document.getElementById('motion-status').textContent === 'Resultado visible');
    if (process.env.SCREENSHOT_DIR) mkdirSync(process.env.SCREENSHOT_DIR, {recursive:true});
    for (let i = 0; i < 20; i++) {
      assert.equal(await page.locator('#counter').innerText(), `${i + 1} / 20`);
      assert.equal(await page.locator('#scene [data-phase]').count(), 3);
      assert.ok((await page.locator('#scene-note').innerText()).length > 20);
      assert.equal(await page.locator('.node.active').getAttribute('data-step'), String(i));
      await page.evaluate(() => animations.forEach(a => a.finish()));
      await page.waitForFunction(() => document.getElementById('motion-status').textContent === 'Resultado visible');
      await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
      if (process.env.SCREENSHOT_DIR) await page.locator('.detail').screenshot({path:join(process.env.SCREENSHOT_DIR, `paso-${i + 1}.png`)});
      if (i !== 19) await page.locator('#next').click();
    }
    assert.ok(await page.locator('#next').isDisabled());
    await page.locator('#prev').click();
    await page.locator('#replay').click();
    await page.locator('#play').click();
    assert.ok(await page.evaluate(() => animations.every(a => a.playState === 'paused')));
    await page.locator('#speed').selectOption('2');
    await page.locator('#play').click();
    await page.evaluate(() => animations.forEach(a => a.finish()));
    await page.locator('#replay').click();
    assert.ok(await page.evaluate(() => animations.every(a => a.playbackRate === 2)));
    await page.locator('body').click({position:{x:5,y:5}});
    await page.keyboard.press('ArrowLeft');
    assert.equal(await page.locator('#counter').innerText(), '18 / 20');
    await page.setViewportSize({width:390,height:844});
    assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
    const map = await page.locator('.map').boundingBox(), detail = await page.locator('.detail').boundingBox();
    assert.ok(detail.y >= map.y + map.height);
    await page.emulateMedia({reducedMotion:'reduce'});
    await page.locator('#next').click();
    assert.ok(await page.evaluate(() => animations.every(a => a.playState === 'finished')));
    if (process.env.SCREENSHOT_DIR) await page.screenshot({path:join(process.env.SCREENSHOT_DIR, 'mobile.png'), fullPage:true});
    await page.evaluate(() => {
      sample.splice(0, sample.length, ...Array.from({length:6}, (_,i) => ({token:'<img onerror=alert(1)>'.repeat(5),id:i})));
      step=1; render();
    });
    assert.ok((await page.locator('#scene-note').innerText()).includes('4 de 6'));
    assert.equal(await page.locator('#scene img').count(),0);
    assert.deepEqual(errors, []);
    console.log('OK: 20 escenas, navegación, pausa, repetición, velocidad, móvil, movimiento reducido y texto largo seguro');
  } finally {
    await browser.close(); rmSync(dir, {recursive:true, force:true});
  }
})();
