import puppeteer from 'puppeteer';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUT_DIR = path.join(__dirname, 'temporary screenshots');

const [, , url, label] = process.argv;

if (!url) {
  console.error('Usage: node screenshot.mjs <url> [label]');
  process.exit(1);
}

fs.mkdirSync(OUT_DIR, { recursive: true });

function nextIndex() {
  const existing = fs.readdirSync(OUT_DIR).filter((f) => f.startsWith('screenshot-'));
  const nums = existing.map((f) => parseInt(f.match(/screenshot-(\d+)/)?.[1] ?? '0', 10));
  return (nums.length ? Math.max(...nums) : 0) + 1;
}

const index = nextIndex();
const filename = label ? `screenshot-${index}-${label}.png` : `screenshot-${index}.png`;
const outPath = path.join(OUT_DIR, filename);

const browser = await puppeteer.launch();
try {
  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900 });
  await page.goto(url, { waitUntil: 'networkidle0' });
  await page.screenshot({ path: outPath, fullPage: true });
  console.log(`Saved ${outPath}`);
} finally {
  await browser.close();
}
