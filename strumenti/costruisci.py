#!/usr/bin/env python3
"""Costruisce il dizionario per lingua e lo scrive in i18n.js.

COME FUNZIONA. Ogni elemento traducibile ha gia' un data-i18n con l'impronta
del suo testo italiano. Qui, per ciascuna chiave, si ricostruisce l'HTML
tradotto sostituendo SOLO i pezzi di testo e lasciando intatto il markup —
cosi' «Un albergo con <em>posizione ideale.</em>» diventa «A hotel with
<em>the perfect location.</em>» e il corsivo resta dov'e'.

E' il motivo per cui ho tradotto FRAMMENTI e non stringhe HTML intere:
riscrivere 256 stringhe con dentro i tag a mano avrebbe significato prima o
poi sbagliare una virgoletta e rompere una pagina.

QUELLO CHE RESTA IN ITALIANO. Se un frammento non ha traduzione (nomi propri,
misure, indirizzi, i nomi degli ospiti, le due recensioni gia' scritte in
inglese e in polacco) resta com'e'. Meglio una parola in italiano dentro una
frase tedesca che una parola inventata.
"""
import json, re, pathlib, html as H

S = pathlib.Path(__file__).parent
BASE = pathlib.Path.home() / "Documents/Fam_S.r.l./Sito Prà/pradelafam"
LINGUE = ["en", "de", "fr", "es"]

it = json.load(open(S / "it.json"))
trad = {}
for f in ("trad_corti.json", "trad_lunghi.json"):
    for k, v in json.load(open(S / f)).items():
        if not k.startswith("_"):
            trad[k] = v

def traduci(html, lingua):
    """Sostituisce i pezzi di TESTO, lascia i tag dove sono."""
    fuori = []
    for pezzo in re.split(r'(<[^>]+>)', html):
        if pezzo.startswith('<'):
            fuori.append(pezzo); continue
        nudo = pezzo.strip()
        if not nudo:
            fuori.append(pezzo); continue
        # &amp; nell'HTML vs & nelle traduzioni: si confronta il testo decodificato
        voce = trad.get(nudo) or trad.get(H.unescape(nudo))
        t = (voce or {}).get(lingua)
        if t and "&amp;" in nudo: t = t.replace("&", "&amp;")
        fuori.append(pezzo.replace(nudo, t) if t else pezzo)
    return "".join(fuori)

diz = {l: {} for l in LINGUE}
non_tradotti = set()
for k, v in it.items():
    for l in LINGUE:
        nuovo = traduci(v, l)
        if nuovo != v:
            diz[l][k] = nuovo
    # traccia i frammenti senza traduzione, per dirlo onestamente
    for pezzo in re.split(r'(<[^>]+>)', v):
        if pezzo.startswith('<'): continue
        n = pezzo.strip()
        if n and re.search(r'[A-Za-zÀ-ÿ]', n) and n not in trad and H.unescape(n) not in trad:
            non_tradotti.add(n)

for l in LINGUE:
    print(f"  {l}: {len(diz[l])}/{len(it)} testi tradotti")
print(f"\n  frammenti lasciati in italiano: {len(non_tradotti)}")
for n in sorted(non_tradotti)[:24]:
    print(f"    · {n[:78]}")

JS = """/* ══════════════════════════════════════════════════════════════════════
   Prà de la Fam — cinque lingue.

   Fino a oggi i dieci pulsanti IT/EN/DE/FR/ES non facevano niente: setLang
   non era definita da nessuna parte e la console diceva «setLang is not
   defined». Non era codice rotto, era una funzione mai costruita — non
   c'era un solo marcatore di traduzione in tutto il sito.

   Ogni elemento traducibile ha un data-i18n con l'impronta del suo testo
   italiano. L'italiano non sta qui: sta nell'HTML, ed e' la sorgente. Qui
   ci sono solo le altre quattro lingue, e quello che manca resta in
   italiano — meglio una parola non tradotta che una inventata.
   ══════════════════════════════════════════════════════════════════════ */
window.PDLF_T = __DIZ__;

(function () {
  var LINGUE = ['it', 'en', 'de', 'fr', 'es'];
  var originale = null;            // l'italiano com'era al caricamento

  function raccogliOriginale() {
    if (originale) return;
    originale = {};
    document.querySelectorAll('[data-i18n]').forEach(function (el) {
      originale[el.getAttribute('data-i18n')] = el.innerHTML;
    });
  }

  window.setLang = function (l) {
    if (LINGUE.indexOf(l) < 0) l = 'it';
    raccogliOriginale();
    var d = (l === 'it') ? null : (window.PDLF_T[l] || {});
    document.querySelectorAll('[data-i18n]').forEach(function (el) {
      var k = el.getAttribute('data-i18n');
      var t = d ? d[k] : originale[k];
      // senza traduzione si torna all'italiano: mai una casella vuota
      el.innerHTML = (t !== undefined && t !== null) ? t : originale[k];
    });
    document.documentElement.lang = l;
    document.querySelectorAll('.lang-btn, .flb').forEach(function (b) {
      var suo = (b.getAttribute('onclick') || '').match(/setLang\\('(\\w+)'\\)/);
      b.classList.toggle('active', !!suo && suo[1] === l);
    });
    try { localStorage.setItem('pdlf_lang', l); } catch (e) {}
    // il motore di prenotazione riceve la stessa lingua del sito: era
    // fisso su 'it', quindi un tedesco atterrava in italiano proprio nel
    // momento in cui non deve esitare
    document.querySelectorAll('a[href*="secure-reservation"]').forEach(function (a) {
      a.href = a.href.replace(/([?&]lang=)\\w+/, '$1' + l);
    });
    try { if (typeof gtag === 'function') gtag('event', 'cambio_lingua', { nuova: l }); } catch (e) {}
  };

  function iniziale() {
    var l = null;
    try { l = localStorage.getItem('pdlf_lang'); } catch (e) {}
    if (!l) {
      var b = (navigator.languages && navigator.languages[0]) || navigator.language || 'it';
      b = b.slice(0, 2).toLowerCase();
      l = LINGUE.indexOf(b) > -1 ? b : 'it';
    }
    raccogliOriginale();
    if (l !== 'it') window.setLang(l);
    else document.documentElement.lang = 'it';
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', iniziale);
  else iniziale();
})();
"""
(BASE / "i18n.js").write_text(
    JS.replace("__DIZ__", json.dumps(diz, ensure_ascii=False, separators=(",", ":"))),
    encoding="utf-8")
kb = (BASE / "i18n.js").stat().st_size // 1024
print(f"\n  i18n.js scritto ({kb} KB)")
