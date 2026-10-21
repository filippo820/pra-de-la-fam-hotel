// Controlla le regole SEO di base su TUTTE le pagine, come le legge un motore
// (JavaScript spento), e poi apre alcune pagine con il JavaScript acceso per
// vedere gli errori in console.
//
// Uso (con il sito servito in locale, vedi STATO.md):
//   NODE_PLAYWRIGHT=/cartella/con/node_modules node strumenti/controlla_seo.mjs [http://localhost:8911]
// Per i moduli ES conta dove sta il file, non da dove lo lanci: Playwright si
// cerca nella cartella NODE_PLAYWRIGHT (come per kb.py).
// Esce con codice 1 se qualcosa non va.
import { createRequire } from "module";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const BASE = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const req = createRequire(path.join(process.env.NODE_PLAYWRIGHT || process.cwd(), "x.js"));
const { chromium } = req("playwright");
const SITO = process.argv[2] || "http://localhost:8911";

const pagine = fs.readdirSync(BASE).filter(f => f.endsWith(".html")).sort();
const b = await chromium.launch();
const ctx = await b.newContext({ javaScriptEnabled: false });
let guai = 0;
const male = (pg, msg) => { guai++; console.log(`  ✗ ${pg}: ${msg}`); };

console.log("Pagine (JavaScript spento):");
for (const f of pagine) {
  const p = await ctx.newPage();
  const url = SITO + "/" + (f === "index.html" ? "" : f.replace(/\.html$/, ""));
  await p.goto(url, { waitUntil: "domcontentloaded" });
  const d = await p.evaluate(() => {
    const m = n => document.querySelector(`meta[name="${n}"],meta[property="${n}"]`)?.content;
    return {
      title: document.title, desc: m("description"), robots: m("robots") || "",
      canon: document.querySelector('link[rel=canonical]')?.getAttribute("href"),
      ogImg: m("og:image"), ogAlt: m("og:image:alt"), tw: m("twitter:card"),
      main: document.querySelectorAll("main").length, header: document.querySelectorAll("header").length,
      h1: document.querySelectorAll("h1").length,
      salti: (() => { let prima = 1, s = []; for (const h of document.querySelectorAll("main h1,main h2,main h3,main h4,main h5,main h6")) { const n = +h.tagName[1]; if (n > prima + 1) s.push(h.tagName + " «" + h.textContent.trim().slice(0, 30) + "»"); prima = n; } return s; })(),
      ld: [...document.querySelectorAll('script[type="application/ld+json"]')].map(s => { try { const j = JSON.parse(s.textContent); return (j["@graph"] || [j]).map(x => [].concat(x["@type"]).join("+")).join(","); } catch (e) { return "ERRORE " + e.message; } }),
      gfont: [...document.querySelectorAll("link[href],style")].some(e => /fonts\.(googleapis|gstatic)\.com/.test(e.getAttribute("href") || e.textContent)),
      img: [...document.querySelectorAll("img")].filter(i => i.getAttribute("src")).map(i => ({ src: i.getAttribute("src"), w: i.getAttribute("width"), h: i.getAttribute("height"), alt: i.getAttribute("alt") })),
      linkHtml: [...document.querySelectorAll("a[href],[data-href]")].map(a => a.getAttribute("href") || a.dataset.href).filter(h => /^(?!https?:)[^#?]*\.html/.test(h)),
    };
  });
  await p.close();
  const pg = f, nonIndicizzata = /noindex/.test(d.robots);
  if (d.title.length > 60) male(pg, `title di ${d.title.length} caratteri`);
  if (!nonIndicizzata) {
    if (!d.desc || d.desc.length < 120 || d.desc.length > 160) male(pg, `description di ${(d.desc || "").length} caratteri`);
    if (!d.canon || /\.html/.test(d.canon) || !d.canon.startsWith("https://alpradelafam.com/")) male(pg, `canonical «${d.canon}»`);
    if (!d.ogImg || !d.ogAlt || d.tw !== "summary_large_image") male(pg, "anteprima social incompleta");
    if (!d.ld.length) male(pg, "nessun JSON-LD");
    if (/\d\s*€|€\s*\d/.test(d.title + " " + d.desc)) male(pg, "prezzo nel title o nella description");
  }
  if (d.main !== 1) male(pg, `${d.main} <main>`);
  if (d.header !== 1) male(pg, `${d.header} <header>`);
  if (d.h1 !== 1) male(pg, `${d.h1} H1`);
  if (d.salti.length) male(pg, `titoli che saltano un livello: ${d.salti.join(", ")}`);
  d.ld.filter(x => x.startsWith("ERRORE")).forEach(x => male(pg, "JSON-LD non valido: " + x));
  if (d.gfont) male(pg, "carica ancora Google Fonts");
  d.img.filter(i => !i.w || !i.h).forEach(i => male(pg, `immagine senza misure: ${i.src}`));
  d.img.filter(i => !i.alt || i.alt.trim().toLowerCase() === "foto").forEach(i => male(pg, `immagine senza alt descrittivo: ${i.src}`));
  if (d.linkHtml.length) male(pg, `link interni con .html: ${[...new Set(d.linkHtml)].join(", ")}`);
  console.log(`  ${pg.padEnd(30)} T${String(d.title.length).padStart(3)} D${String((d.desc || "").length).padStart(4)}  ${nonIndicizzata ? "noindex " : ""}${d.ld.join(" · ")}`);
}

// sitemap: tutte e sole le pagine indicizzabili, senza .html, uguali ai canonical
const sm = fs.readFileSync(path.join(BASE, "sitemap.xml"), "utf8");
const locs = [...sm.matchAll(/<loc>([^<]+)<\/loc>/g)].map(m => m[1]);
if (locs.some(l => l.includes(".html"))) male("sitemap.xml", "contiene indirizzi .html");
const attesi = pagine.filter(f => f !== "404.html").map(f => "https://alpradelafam.com/" + (f === "index.html" ? "" : f.replace(/\.html$/, "")));
attesi.filter(a => !locs.includes(a)).forEach(a => male("sitemap.xml", "manca " + a));
locs.filter(l => !attesi.includes(l)).forEach(l => male("sitemap.xml", "in più " + l));
if (!/Sitemap: https:\/\/alpradelafam\.com\/sitemap\.xml/.test(fs.readFileSync(path.join(BASE, "robots.txt"), "utf8"))) male("robots.txt", "non dichiara la sitemap");

console.log("\nConsole (JavaScript acceso):");
const viva = await b.newContext({ viewport: { width: 1280, height: 860 } });
for (const pg of ["/", "/camera-doppia", "/appartamento-pomelo", "/faq", "/pagina-che-non-esiste"]) {
  const p = await viva.newPage(); const err = [];
  p.on("pageerror", e => err.push("eccezione: " + e.message));
  p.on("console", m => { if (m.type() === "error" && !/status of 404/.test(m.text())) err.push(m.text()); });
  p.on("response", r => { if (r.status() >= 400 && !r.request().isNavigationRequest() && r.url().startsWith(SITO)) err.push(`${r.status()} ${r.url()}`); });
  const r = await p.goto(SITO + pg, { waitUntil: "networkidle" });
  await p.evaluate(() => window.setLang && setLang("de")); await p.waitForTimeout(300);
  const h1 = await p.evaluate(() => document.querySelector("h1")?.textContent.trim().slice(0, 50));
  await p.evaluate(() => window.setLang && setLang("it"));
  if (err.length) err.forEach(e => male(pg, e));
  console.log(`  ${pg.padEnd(24)} ${r.status()}  errori: ${err.length}  H1 in tedesco: «${h1}»`);
  await p.close();
}
await b.close();
console.log("\n  " + (guai ? `✗ ${guai} problemi` : "✓ tutto in regola"));
process.exit(guai ? 1 : 0);
