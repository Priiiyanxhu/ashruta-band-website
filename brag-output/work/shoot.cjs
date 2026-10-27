const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const mode = process.argv[2] || 'stills';
  const outDir = process.argv[3];
  const times = process.argv.slice(4).map(Number);
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport:{width:1920,height:1080}, deviceScaleFactor:1 });
  await pg.goto('file://' + path.resolve('scene.html'));
  await pg.waitForFunction('window.__ready === true', null, {timeout:30000});
  if (mode === 'stills') {
    for (const t of times) {
      await pg.evaluate(t => window.__setT(t), t);
      await pg.evaluate(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))));
      await pg.screenshot({ path: `${outDir}/t${t.toFixed(2)}.png` });
    }
  } else {
    const fps = 30, dur = 20.0, n = Math.round(fps*dur);
    for (let i=0;i<n;i++){
      await pg.evaluate(t => window.__setT(t), i/fps);
      await pg.evaluate(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))));
      await pg.screenshot({ path: `${outDir}/f${String(i).padStart(4,'0')}.png` });
      if (i%60===0) console.log('frame', i, '/', n);
    }
    console.log('done', n);
  }
  await b.close();
})();
