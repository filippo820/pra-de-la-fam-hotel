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
  "faq": "/faq.html",
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
# ⚠️ Per i moduli ES conta DOVE STA IL FILE, non da dove lo lanci: NODE_PATH
# non serve a niente. Lo script va quindi scritto accanto a node_modules.
import os
np = os.environ.get("NODE_PLAYWRIGHT")
DOVE = pathlib.Path(np) if np else S
(DOVE / "_kb.mjs").write_text(JS, encoding="utf-8")
r = subprocess.run(["node", str(DOVE / "_kb.mjs")], capture_output=True, text=True, cwd=DOVE)
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
    "orari": "Check-in dalle 14:00 alle 20:00, check-out entro le 10:30. Chi arriva più tardi "
             "avvisa per telefono: la gestione è familiare e ci si organizza.",
    "animali": "I cani sono ammessi sia nelle camere sia negli appartamenti. Supplemento: 10 € a "
               "notte per animale in albergo, 50 € a soggiorno per animale negli appartamenti "
               "(non a notte). Va segnalato al momento della prenotazione.",
    "spiaggia": "La spiaggia è a meno di venti metri dal giardino, piccola e libera, non un lido "
                "attrezzato. Non c'è piscina: si fa il bagno nel lago.",
    "colazione": "Inclusa per chi dorme in camera, servita in veranda all'ombra degli ulivi. Per gli "
                 "appartamenti, che hanno la cucina, si può aggiungere a pagamento.",
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
