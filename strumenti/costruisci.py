#!/usr/bin/env python3
"""Costruisce il dizionario per lingua e lo scrive in strumenti/dizionario.json.

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
        # una traduzione puo' essere scritta con «&» o gia' con «&amp;»: si
        # codifica una volta sola (prima il banner diceva «Cookies &amp;amp;»)
        if t and "&amp;" in nudo: t = t.replace("&amp;", "&").replace("&", "&amp;")
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

# Il dizionario lo legge strumenti/lingue.py, che scrive le pagine vere per
# lingua (/en/, /de/, /fr/, /es/). Fino alla fase SEO 2 finiva anche in
# i18n.js e il browser lo applicava dopo il caricamento: non serve piu', e il
# file pesava 165 KB su ogni pagina.
(S / "dizionario.json").write_text(
    json.dumps(diz, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")
print("\n  strumenti/dizionario.json scritto")
