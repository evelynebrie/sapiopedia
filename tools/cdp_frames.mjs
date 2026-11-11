// Records a page frame by frame through the Chrome DevTools protocol.
// The page defines window.__ready (true once set up) and window.__step(i) (async: moves its own clock to frame i).
// Usage: node tools/cdp_frames.mjs <url> <outdir> <frames> [width height]
import { spawn } from "node:child_process";
import { mkdirSync, writeFileSync, mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const [url, outdir, nStr, wStr = "1000", hStr = "1500"] = process.argv.slice(2);
const N = +nStr, W = +wStr, H = +hStr, PORT = 9300 + Math.floor(Math.random() * 600);
mkdirSync(outdir, { recursive: true });
const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const chrome = spawn(CHROME, ["--headless=new", "--hide-scrollbars", `--remote-debugging-port=${PORT}`, `--window-size=${W},${H}`,
  "--force-device-scale-factor=1", "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--autoplay-policy=no-user-gesture-required",
  `--user-data-dir=${mkdtempSync(join(tmpdir(), "cdp-"))}`, "about:blank"], { stdio: "ignore" });
const sleep = ms => new Promise(r => setTimeout(r, ms));

let targets;
for (let i = 0; i < 100; i++) { try { targets = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json(); if (targets.some(t => t.type === "page")) break; } catch (_) {} await sleep(150); }
const ws = new WebSocket(targets.find(t => t.type === "page").webSocketDebuggerUrl);
await new Promise(r => ws.addEventListener("open", r, { once: true }));
let id = 0; const waiting = new Map();
ws.addEventListener("message", e => { const m = JSON.parse(e.data); if (m.id && waiting.has(m.id)) { waiting.get(m.id)(m); waiting.delete(m.id); } });
const send = (method, params = {}) => new Promise((res, rej) => { const i = ++id; waiting.set(i, m => m.error ? rej(new Error(method + ": " + m.error.message)) : res(m.result)); ws.send(JSON.stringify({ id: i, method, params })); });
const evaluate = async expr => { const r = await send("Runtime.evaluate", { expression: expr, awaitPromise: true, returnByValue: true });
  if (r.exceptionDetails) throw new Error(r.exceptionDetails.exception?.description || r.exceptionDetails.text); return r.result.value; };

try {
  await send("Emulation.setDeviceMetricsOverride", { width: W, height: H, deviceScaleFactor: 1, mobile: false });
  await send("Page.enable"); await send("Page.navigate", { url });
  for (let i = 0; ; i++) { if (await evaluate("!!window.__ready").catch(() => false)) break; if (i > 300) throw new Error("page never ready"); await sleep(100); }
  for (let i = 0; i < N; i++) {
    await evaluate(`window.__step(${i})`);
    const { data } = await send("Page.captureScreenshot", { format: "png", clip: { x: 0, y: 0, width: W, height: H, scale: 1 }, captureBeyondViewport: false });
    writeFileSync(join(outdir, `f_${String(i).padStart(4, "0")}.png`), Buffer.from(data, "base64"));
    if (i % 60 === 0) process.stderr.write(`frame ${i}/${N}\n`);
  }
} finally { ws.close(); chrome.kill(); }
