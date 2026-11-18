// Render poster.html to entry.png at exactly 1024 x 1024, device scale 1.
// Usage: NODE_PATH=/data/motion/node_modules PLAYWRIGHT_BROWSERS_PATH=/data/motion/pw-browsers node render.mjs
import { createRequire } from "node:module";
import { readFileSync, writeFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { fileURLToPath, pathToFileURL } from "node:url";
import path from "node:path";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright");

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const GEO = path.join(ROOT, "tmp", "geo", "land-110m.json");
const GEO_URL = "https://cdn.jsdelivr.net/npm/world-atlas@2.0.2/land-110m.json";
const OUT = path.join(ROOT, "entry.png");
const LIMIT = 1048576;

async function landData() {
  if (!existsSync(GEO)) {
    mkdirSync(path.dirname(GEO), { recursive: true });
    const res = await fetch(GEO_URL);
    if (!res.ok) throw new Error(`download failed: ${res.status}`);
    writeFileSync(GEO, Buffer.from(await res.arrayBuffer()));
  }
  return JSON.parse(readFileSync(GEO, "utf8"));
}

const land = await landData();
const browser = await chromium.launch();
try {
  const page = await browser.newPage({ viewport: { width: 1024, height: 1024 }, deviceScaleFactor: 1 });
  await page.addInitScript(t => { window.LAND = t; }, land);
  await page.goto(pathToFileURL(path.join(ROOT, "poster.html")).href);
  await page.waitForSelector("body[data-ready='1']");
  await page.evaluate(() => document.fonts.ready);

  // Layout check: overflowing/clipped text boxes and anything under 15 px.
  const problems = await page.evaluate(() => {
    const out = [];
    for (const el of document.querySelectorAll(".card, .txt, .hl, .dt, .tag, header, .date, footer")) {
      if (el.scrollWidth > el.clientWidth + 1 || el.scrollHeight > el.clientHeight + 1)
        out.push(`overflow: ${el.className || el.tagName} "${el.textContent.trim().slice(0, 40)}"`);
    }
    for (const el of document.querySelectorAll("body *")) {
      if (!el.childNodes.length || ![...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) continue;
      const fs = parseFloat(getComputedStyle(el).fontSize);
      if (fs < 15) out.push(`small text ${fs}px: "${el.textContent.trim().slice(0, 30)}"`);
    }
    const r = document.getElementById("cards").getBoundingClientRect();
    const f = document.querySelector("footer").getBoundingClientRect();
    if (r.bottom > f.top) out.push("cards overlap footer");
    if (f.bottom > 1024) out.push("footer clipped");
    return out;
  });
  console.log(problems.length ? "LAYOUT PROBLEMS:\n  " + problems.join("\n  ") : "layout check: ok");

  let buf = await page.screenshot({ type: "png", clip: { x: 0, y: 0, width: 1024, height: 1024 } });
  if (buf.length > LIMIT) {
    console.log(`png ${buf.length} bytes > limit, falling back to jpeg`);
    buf = await page.screenshot({ type: "jpeg", quality: 90, clip: { x: 0, y: 0, width: 1024, height: 1024 } });
  }
  writeFileSync(OUT, buf);
  console.log(`wrote ${OUT}: ${statSync(OUT).size} bytes`);
} finally {
  await browser.close();
}
