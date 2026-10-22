// Controlla le regole SEO su TUTTE le pagine, in tutte e cinque le lingue,
// come le legge un motore (JavaScript spento), e poi apre alcune pagine per
// lingua con il JavaScript acceso: errori in console, selettore di lingua,
// assistente.
//
// Uso (con il sito servito in locale, vedi STATO.md — serve un server che
// risponda agli indirizzi senza .html e dia la 404 con stato 404):
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
const DOMINIO = "https://alpradelafam.com";
const LINGUE = ["it", "en", "de", "fr", "es"];

// le pagine: l'italiano alla radice, le altre lingue nelle cartelle
const nomi = fs.readdirSync(BASE).filter(f => f.endsWith(".html")).map(f => f.replace(/\.html$/, "")).sort();
const pagine = LINGUE.flatMap(l => nomi.map(n => ({ l, n, file: (l === "it" ? "" : l + "/") + n + ".html" })))
  .filter(p => fs.existsSync(path.join(BASE, p.file)));
const percorso = (n, l) => (l === "it" ? "" : "/" + l) + "/" + (n === "index" ? "" : n);
const assoluto = (n, l) => DOMINIO + percorso(n, l);

// cosa puo' restare identico all'italiano in una pagina tradotta: i testi
// dichiarati invariati, quelli la cui traduzione e' uguale (Superficie in
// francese), e cio' che non e' una parola (numeri, indirizzi mail, codici)
const leggi = f => JSON.parse(fs.readFileSync(path.join(BASE, "strumenti", f), "utf8"));
const norm = t => t.replace(/\s+/g, " ").trim();
const meta = leggi("trad_meta.json");
const INVARIATI = new Set((meta._invariati || []).map(norm));
const UGUALI = Object.fromEntries(LINGUE.map(l => [l, new Set()]));
for (const f of [leggi("trad_corti.json"), leggi("trad_lunghi.json"), meta])
  for (const [k, v] of Object.entries(f)) if (!k.startsWith("_") && typeof v === "object")
    for (const l of LINGUE) if (v[l] && norm(v[l].replace(/ /g, " ")) === norm(k)) UGUALI[l].add(norm(k));
const NON_PAROLA = /^(?:[\d\s.,:;€%°/–—\-+()×′″²m]*|.*@.*\..*|[\w.-]+\.(?:com|it|cloud|shop)(?:\/\S*)?|GPS .*|P\.IVA.*|.*P\.IVA \d+|© \d{4} .*|\S*[\p{Extended_Pictographic}\p{Regional_Indicator}].*|App\. \w+)$/u;

// Su un'anteprima Netlify, dopo una raffica di richieste da un browser
// automatico, arriva un 403 con la pagina di protezione di Netlify (in
// inglese, senza niente del sito): non e' un errore del sito. Si aspetta e si
// riprova, con pause sempre piu' lunghe.
async function vai(p, url, opz) {
  let r;
  for (const pausa of [0, 5000, 15000, 30000, 60000]) {
    if (pausa) await p.waitForTimeout(pausa);
    r = await p.goto(url, opz);
    if (![403, 429].includes(r.status())) return r;
  }
  return r;
}

const b = await chromium.launch();
const ctx = await b.newContext({ javaScriptEnabled: false });
let guai = 0;
const male = (pg, msg) => { guai++; console.log(`  ✗ ${pg}: ${msg}`); };
const visti = { title: {}, desc: {} };
const testiIt = {};

console.log("Pagine (JavaScript spento):");
for (const { l, n, file } of pagine) {
  const p = await ctx.newPage();
  const url = SITO + (n === "404" ? "/" + file : percorso(n, l));
  await vai(p, url, { waitUntil: "domcontentloaded" });
  const d = await p.evaluate(() => {
    const m = n => document.querySelector(`meta[name="${n}"],meta[property="${n}"]`)?.content;
    const testi = [];
    // (con il JavaScript della pagina spento un TreeWalker non accetta un filtro-funzione)
    const giro = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    while (giro.nextNode()) {
      if (giro.currentNode.parentElement.closest("script,style,noscript,svg")) continue;
      const t = giro.currentNode.textContent.replace(/\s+/g, " ").trim(); if (t) testi.push(t);
    }
    return {
      lang: document.documentElement.lang,
      title: document.title, desc: m("description"), robots: m("robots") || "",
      canon: document.querySelector('link[rel=canonical]')?.getAttribute("href"),
      ogUrl: m("og:url"), ogLocale: m("og:locale"),
      ogAlt: [...document.querySelectorAll('meta[property="og:locale:alternate"]')].map(e => e.content).sort().join(","),
      alt: Object.fromEntries([...document.querySelectorAll('link[rel=alternate][hreflang]')].map(e => [e.hreflang, e.getAttribute("href")])),
      ogImg: m("og:image"), ogImgAlt: m("og:image:alt"), tw: m("twitter:card"),
      main: document.querySelectorAll("main").length, header: document.querySelectorAll("header").length,
      h1: document.querySelectorAll("h1").length,
      salti: (() => { let prima = 1, s = []; for (const h of document.querySelectorAll("main h1,main h2,main h3,main h4,main h5,main h6")) { const n = +h.tagName[1]; if (n > prima + 1) s.push(h.tagName + " «" + h.textContent.trim().slice(0, 30) + "»"); prima = n; } return s; })(),
      ld: [...document.querySelectorAll('script[type="application/ld+json"]')].map(s => { try { return JSON.parse(s.textContent); } catch (e) { return { errore: e.message }; } }),
      gfont: [...document.querySelectorAll("link[href],style")].some(e => /fonts\.(googleapis|gstatic)\.com/.test(e.getAttribute("href") || e.textContent)),
      img: [...document.querySelectorAll("img")].filter(i => i.getAttribute("src")).map(i => ({ src: i.getAttribute("src"), w: i.getAttribute("width"), h: i.getAttribute("height"), alt: i.getAttribute("alt") })),
      link: [...document.querySelectorAll("a[href],[data-href]")].map(a => ({ h: a.getAttribute("href") || a.dataset.href, sel: a.hasAttribute("hreflang") })),
      i18n: !!document.querySelector('script[src*="i18n.js"]'),
      testi,
    };
  });
  await p.close();
  const pg = file, noindex = /noindex/.test(d.robots);
  if (d.lang !== l) male(pg, `<html lang="${d.lang}">`);
  if (d.title.length > 60) male(pg, `title di ${d.title.length} caratteri`);
  (visti.title[d.title] ||= []).push(pg);
  if (!noindex) {
    if (!d.desc || d.desc.length < 120 || d.desc.length > 160) male(pg, `description di ${(d.desc || "").length} caratteri`);
    (visti.desc[d.desc] ||= []).push(pg);
    if (d.canon !== assoluto(n, l)) male(pg, `canonical «${d.canon}» invece di ${assoluto(n, l)}`);
    if (d.ogUrl !== d.canon) male(pg, `og:url «${d.ogUrl}» diverso dal canonical`);
    const loc = { it: "it_IT", en: "en_GB", de: "de_DE", fr: "fr_FR", es: "es_ES" };
    if (d.ogLocale !== loc[l] || d.ogAlt !== LINGUE.filter(x => x !== l).map(x => loc[x]).sort().join(",")) male(pg, `og:locale ${d.ogLocale} / ${d.ogAlt}`);
    // hreflang: le cinque versioni piu' x-default, uguali in tutte le versioni
    const attese = Object.fromEntries([...LINGUE.map(x => [x, assoluto(n, x)]), ["x-default", assoluto(n, "it")]]);
    if (JSON.stringify(Object.entries(d.alt).sort()) !== JSON.stringify(Object.entries(attese).sort())) male(pg, `hreflang ${JSON.stringify(d.alt)}`);
    if (!d.ogImg || !d.ogImgAlt || d.tw !== "summary_large_image") male(pg, "anteprima social incompleta");
    if (!d.ld.length) male(pg, "nessun JSON-LD");
    if (/\d\s*€|€\s*\d/.test(d.title + " " + d.desc)) male(pg, "prezzo nel title o nella description");
  }
  // JSON-LD: valido, nella lingua della pagina, indirizzi nella stessa lingua, immagini che esistono
  for (const j of d.ld) {
    if (j.errore) { male(pg, "JSON-LD non valido: " + j.errore); continue; }
    const s = JSON.stringify(j);
    for (const m of s.matchAll(/"inLanguage":"(\w+)"/g)) if (m[1] !== l) male(pg, `JSON-LD inLanguage ${m[1]}`);
    for (const m of s.matchAll(/"(?:url|item)":"(https:\/\/alpradelafam\.com\/[^"]*)"/g)) {
      const altra = (m[1].match(/^https:\/\/alpradelafam\.com\/(en|de|fr|es)(?:\/|$)/) || [, "it"])[1];
      if (altra !== l) male(pg, `JSON-LD punta a un'altra lingua: ${m[1]}`);
    }
    for (const m of s.matchAll(/"(https:\/\/alpradelafam\.com\/(?:img|og)\/[^"]+)"/g))
      if (!fs.existsSync(path.join(BASE, m[1].slice(DOMINIO.length)))) male(pg, `JSON-LD: immagine che non esiste ${m[1]}`);
  }
  if (d.main !== 1) male(pg, `${d.main} <main>`);
  if (d.header !== 1) male(pg, `${d.header} <header>`);
  if (d.h1 !== 1) male(pg, `${d.h1} H1`);
  if (d.salti.length) male(pg, `titoli che saltano un livello: ${d.salti.join(", ")}`);
  if (d.gfont) male(pg, "carica ancora Google Fonts");
  if (d.i18n) male(pg, "carica ancora i18n.js");
  d.img.filter(i => !i.w || !i.h).forEach(i => male(pg, `immagine senza misure: ${i.src}`));
  d.img.filter(i => !i.alt || i.alt.trim().toLowerCase() === "foto").forEach(i => male(pg, `immagine senza alt descrittivo: ${i.src}`));
  d.img.filter(i => !i.src.startsWith("/") && !/^https?:/.test(i.src)).forEach(i => male(pg, `immagine con percorso relativo: ${i.src}`));
  const conHtml = d.link.map(x => x.h).filter(h => /^(?!https?:)[^#?]*\.html/.test(h));
  if (conHtml.length) male(pg, `link interni con .html: ${[...new Set(conHtml)].join(", ")}`);
  // nessun link che porta per sbaglio a un'altra lingua (il selettore si')
  const RISORSA = /^\/(?:img|og|fonts|api)\//;
  const fuori = d.link.filter(x => !x.sel && x.h && x.h.startsWith("/") && !RISORSA.test(x.h))
    .filter(x => { const m = x.h.match(/^\/(en|de|fr|es)(?:\/|$)/); return (m ? m[1] : "it") !== l; }).map(x => x.h);
  if (fuori.length) male(pg, `link verso un'altra lingua: ${[...new Set(fuori)].join(", ")}`);
  if (l === "it") testiIt[n] = new Set(d.testi);
  else {
    const rimasti = [...new Set(d.testi.filter(t => testiIt[n]?.has(t) && /\p{L}{3}/u.test(t)
      && !INVARIATI.has(t) && !UGUALI[l].has(t) && !NON_PAROLA.test(t)))];
    if (rimasti.length) male(pg, `testo rimasto in italiano: ${rimasti.map(t => "«" + t.slice(0, 50) + "»").join(", ")}`);
  }
  if (n === "index" || n === "camera-doppia" || n === "404")
    console.log(`  ${pg.padEnd(32)} T${String(d.title.length).padStart(3)} D${String((d.desc || "").length).padStart(4)}  ${noindex ? "noindex " : ""}${d.ld.map(j => (j["@graph"] || [j]).map(x => [].concat(x["@type"]).join("+")).join(",")).join(" · ")}`);
}
console.log(`  … ${pagine.length} pagine in tutto`);
for (const [k, v] of Object.entries(visti.title)) if (v.length > 1) male(v.join(" "), `stesso title «${k}»`);
for (const [k, v] of Object.entries(visti.desc)) if (v.length > 1) male(v.join(" "), `stessa description «${k.slice(0, 50)}…»`);

// sitemap: tutte e sole le pagine indicizzabili in tutte le lingue, con le alternative giuste
const sm = fs.readFileSync(path.join(BASE, "sitemap.xml"), "utf8");
const voci = [...sm.matchAll(/<url>([\s\S]*?)<\/url>/g)].map(m => ({
  loc: m[1].match(/<loc>([^<]+)<\/loc>/)[1],
  alt: Object.fromEntries([...m[1].matchAll(/hreflang="([^"]+)" href="([^"]+)"/g)].map(x => [x[1], x[2]])) }));
const indicizzabili = pagine.filter(p => p.n !== "404");
const attesi = indicizzabili.map(p => assoluto(p.n, p.l));
if (voci.some(v => v.loc.includes(".html"))) male("sitemap.xml", "contiene indirizzi .html");
attesi.filter(a => !voci.some(v => v.loc === a)).forEach(a => male("sitemap.xml", "manca " + a));
voci.filter(v => !attesi.includes(v.loc)).forEach(v => male("sitemap.xml", "in più " + v.loc));
for (const v of voci) {
  const p = indicizzabili.find(p => assoluto(p.n, p.l) === v.loc); if (!p) continue;
  if (Object.keys(v.alt).length !== 6 || LINGUE.some(x => v.alt[x] !== assoluto(p.n, x)) || v.alt["x-default"] !== assoluto(p.n, "it"))
    male("sitemap.xml", `alternative sbagliate per ${v.loc}`);
}
if (!/Sitemap: https:\/\/alpradelafam\.com\/sitemap\.xml/.test(fs.readFileSync(path.join(BASE, "robots.txt"), "utf8"))) male("robots.txt", "non dichiara la sitemap");
console.log(`  sitemap.xml: ${voci.length} indirizzi`);

console.log("\nUna pagina per lingua (JavaScript acceso): console, selettore, assistente");
const viva = await b.newContext({ viewport: { width: 1280, height: 860 } });
// il banner dei cookie come se la scelta fosse gia' fatta: qui non lo si prova
await viva.addInitScript(() => { try { localStorage.setItem("pdlf_consent", "false"); } catch (e) {} });
await viva.route(/open-meteo|googletagmanager/, r => r.abort());
for (const l of LINGUE) for (const n of ["index", "camera-doppia", "faq", "pagina-che-non-esiste"]) {
  const pg = percorso(n, l);
  const p = await viva.newPage(); const err = [];
  p.on("pageerror", e => err.push("eccezione: " + e.message));
  p.on("console", m => { if (m.type() === "error" && !/status of 404|ERR_FAILED/.test(m.text())) err.push(m.text()); });
  p.on("response", r => { if (r.status() >= 400 && !r.request().isNavigationRequest() && r.url().startsWith(SITO)) err.push(`${r.status()} ${r.url()}`); });
  const r = await vai(p, SITO + pg, { waitUntil: "networkidle" });
  const info = await p.evaluate(() => ({ lang: document.documentElement.lang, h1: document.querySelector("h1")?.textContent.replace(/\s+/g, " ").trim().slice(0, 44) }));
  if (info.lang !== l) err.push(`lang della pagina ${info.lang}`);
  if (n === "pagina-che-non-esiste" && r.status() !== 404) err.push(`stato ${r.status()} invece di 404`);
  let extra = "";
  if (n === "camera-doppia") {
    // il selettore porta alla stessa pagina nell'altra lingua
    const altra = l === "de" ? "fr" : "de";
    await Promise.all([p.waitForNavigation(), p.click(`nav a[hreflang=${altra}]`)]);
    const arrivo = new URL(p.url()).pathname;
    if (arrivo !== percorso(n, altra)) err.push(`il selettore porta a ${arrivo} invece di ${percorso(n, altra)}`);
    extra = ` → ${altra}: ${arrivo}`;
    await vai(p, SITO + pg, { waitUntil: "networkidle" });
    // l'assistente si apre, nella lingua della pagina
    await p.click("#pdlf-chat-btn");
    const chat = await p.evaluate(() => { const x = [...document.querySelectorAll("[id^=pdlf-chat]")].find(e => e.id !== "pdlf-chat-btn" && e.offsetHeight > 100); return x ? x.innerText.replace(/\s+/g, " ").slice(0, 34) : null; });
    if (!chat) err.push("l'assistente non si apre");
    extra += `  assistente: «${chat}»`;
  }
  if (err.length) err.forEach(e => male(pg, e));
  console.log(`  ${pg.padEnd(28)} ${r.status()}  errori: ${err.length}  H1 «${info.h1}»${extra}`);
  await p.close();
}
await b.close();
console.log("\n  " + (guai ? `✗ ${guai} problemi` : "✓ tutto in regola"));
process.exit(guai ? 1 : 0);
