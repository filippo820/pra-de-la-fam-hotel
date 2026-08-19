
import { chromium } from "playwright";
const PAG = {
  "home": "/", "camera doppia": "/camera-doppia.html",
  "camera doppia economy": "/camera-doppia-economy.html",
  "camera tripla": "/camera-tripla.html", "camera familiare": "/camera-familiare.html",
  "appartamento Pomelo": "/appartamento-pomelo.html",
  "appartamento Clementina": "/appartamento-clementina.html",
  "appartamento Calamondino": "/appartamento-calamondino.html",
  "appartamento Kumquat": "/appartamento-kumquat.html",
  "appartamento Bergamotto": "/appartamento-bergamotto.html",
  "privacy": "/privacy.html", "cookie": "/cookie.html",
};
const b = await chromium.launch();
// JavaScript SPENTO: cosi' il testo e' l'italiano del file, non la lingua
// che il browser avrebbe scelto da solo
const c = await b.newContext({ javaScriptEnabled: false, locale: "it-IT" });
const out = {};
for (const [nome, url] of Object.entries(PAG)) {
  const p = await c.newPage();
  await p.goto("http://localhost:8911" + url, { waitUntil: "domcontentloaded" });
  out[nome] = await p.evaluate(() => {
    document.querySelectorAll("script,style,#pdlf-overlay,nav,footer").forEach(e => e.remove());
    return document.body.innerText.replace(/\s+/g, " ").trim();
  });
  await p.close();
}
console.log(JSON.stringify(out));
await b.close();
