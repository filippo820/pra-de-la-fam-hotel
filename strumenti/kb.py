#!/usr/bin/env python3
"""kb.json — quello che il sito dice davvero, per l'assistente.

ESTRATTO DALLE PAGINE, non riscritto a mano: una base di conoscenza copiata
diverge al primo cambio di prezzo o di descrizione, e diverge in silenzio.
Rigenerando dopo una modifica torna tutto in riga.

Il testo si prende con il JAVASCRIPT SPENTO, altrimenti si cattura la lingua
che il browser ha scelto invece dell'italiano — errore gia' fatto una volta
costruendo il dizionario delle traduzioni.
"""
import json, re, pathlib, subprocess, sys

BASE = pathlib.Path.home() / "Documents/Fam_S.r.l./Sito Prà/pradelafam"
S = pathlib.Path(__file__).parent

JS = r"""
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
"""
(S / "_kb.mjs").write_text(JS, encoding="utf-8")
r = subprocess.run([ "node", str(S / "_kb.mjs") ], capture_output=True, text=True, cwd=S)
if r.returncode != 0:
    print(r.stderr[:800]); sys.exit(1)
pagine = json.loads(r.stdout)

# fatti che non stanno nel testo delle pagine ma servono per rispondere
FATTI = {
    "contatti": "Telefono +39 0365 799890 · email info@alpradelafam.com · "
                "Via Gardesana 7, Porto di Tignale, 25080 Tignale (BS), sponda bresciana del Lago di Garda.",
    "come si prenota": "Dal tasto «Prenota» del sito, che apre il motore di prenotazione con "
                       "disponibilità in tempo reale e conferma immediata. In alternativa si può "
                       "telefonare o scrivere una mail.",
    "lingue": "Il sito e lo staff parlano italiano, inglese, tedesco, francese e spagnolo.",
    "parcheggio": "Parcheggio privato gratuito riservato ai clienti, chiuso — comodo anche per le moto.",
    "bottega": "La Bottega del Prà (pradelafam.shop) vende olio extravergine biologico, limoni sotto sale, "
               "limoncino, sciroppo di limone, olio agrumato, marmellate e articoli con il logo del Prà. "
               "I prodotti si acquistano in hotel durante il soggiorno.",
    "limonaia": "La Limonaia del Prà de la Fam è la più grande e la più a nord d'Europa, con 80 piante adulte. "
                "È visitabile da Pasqua a ottobre con visita guidata e degustazione. "
                "Sito dedicato: ecomuseopradelafam.com",
}

kb = {"pagine": pagine, "fatti": FATTI}
(BASE / "kb.json").write_text(json.dumps(kb, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
n = len(json.dumps(kb, ensure_ascii=False))
print(f"  kb.json: {n//1024} KB · ~{n//4} parole-macchina per richiesta")
for k, v in pagine.items():
    print(f"    {k:<26} {len(v.split()):>4} parole")
