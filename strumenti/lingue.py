#!/usr/bin/env python3
"""Scrive le pagine vere per lingua: /en/, /de/, /fr/, /es/.

PERCHE' ESISTE. Fino alla fase SEO 1 le altre quattro lingue esistevano solo
nel browser: i18n.js sostituiva l'innerHTML dopo il caricamento. Google, chi
genera le anteprime social e chiunque legga l'HTML vedeva solo l'italiano.
Qui ogni pagina italiana diventa quattro pagine statiche, una per lingua.

LA SORGENTE RESTA L'ITALIANO. Le pagine in /en/ ecc. non si modificano mai a
mano: si cambia la pagina italiana (e le traduzioni in trad_*.json), si
rilancia la procedura, e questo script le riscrive tutte. Un ritocco fatto a
mano in /de/faq.html sparirebbe alla passata seguente, in silenzio.

COSA FA, pagina per pagina e lingua per lingua:
  · il testo: ogni elemento [data-i18n] riceve la sua traduzione da
    dizionario.json (lo scrive costruisci.py), la stessa che prima applicava
    il browser. Senza traduzione resta l'italiano, come prima: nomi propri,
    misure, la riga legale;
  · <html lang> della lingua;
  · i link interni restano nella stessa lingua: «/faq» → «/de/faq»,
    «/#hotel» → «/de/#hotel». Le risorse (/img, /fonts, /i18n.js) hanno gia'
    percorsi assoluti nelle pagine italiane, e valgono da qualsiasi cartella;
  · il motore di prenotazione riceve lang= della pagina.

Ordine della procedura: marca.py → raccogli.py → riaggancia.py → raccogli.py
→ costruisci.py → lingue.py → kb.py
"""
import json, re, pathlib
from html.parser import HTMLParser

BASE = pathlib.Path(__file__).resolve().parent.parent
S = BASE / "strumenti"
LINGUE = ["en", "de", "fr", "es"]

DIZ = json.loads((S / "dizionario.json").read_text(encoding="utf-8"))
PAGINE = sorted(p.stem for p in BASE.glob("*.html"))          # index, faq, 404, ...
INTERNE = {p for p in PAGINE if p not in ("index", "404")}      # indirizzi /<pagina>

AVVISO = ("<!-- Generata da strumenti/lingue.py dalla pagina italiana: NON modificarla qui,\n"
          "     cambia la pagina italiana o le traduzioni e rilancia la procedura (STATO.md). -->\n")


class Elementi(HTMLParser):
    """(inizio, fine, chiave) del contenuto di ogni [data-i18n], come raccogli.py."""
    def __init__(self, src):
        super().__init__(convert_charrefs=False)
        self.src = src; self.righe = [0]
        for r in src.split("\n")[:-1]:
            self.righe.append(self.righe[-1] + len(r) + 1)
        self.pila = []; self.out = []
    def off(self):
        r, c = self.getpos(); return self.righe[r - 1] + c
    def handle_starttag(self, tag, attrs):
        self.pila.append((tag, self.src.find(">", self.off()) + 1, dict(attrs).get("data-i18n")))
    def handle_startendtag(self, tag, attrs):
        pass
    def handle_endtag(self, tag):
        while self.pila:
            t = self.pila.pop()
            if t[0] == tag:
                if t[2]:
                    self.out.append((t[1], self.off(), t[2]))
                break


def testi(src, lingua):
    """Sostituisce il contenuto degli elementi tradotti.

    Se un elemento tradotto ne contiene altri, vale il piu' esterno: la sua
    traduzione comprende gia' quelli dentro (costruisci.py traduce i pezzi di
    testo e lascia i tag dove sono)."""
    e = Elementi(src); e.feed(src)
    d = DIZ[lingua]
    scelti, fine = [], -1
    for inizio, fi, k in sorted(e.out):
        if inizio < fine or k not in d:
            continue
        scelti.append((inizio, fi, d[k])); fine = fi
    for inizio, fi, t in reversed(scelti):
        src = src[:inizio] + t + src[fi:]
    return src, len(scelti)


def indirizzo(lingua, percorso):
    """«/faq#x» nella lingua: «/de/faq#x». Solo le pagine del sito, non le risorse."""
    m = re.match(r'/([^/?#]*)([?#].*)?$', percorso)
    if not m:
        return None
    nome, resto = m.group(1), m.group(2) or ""
    if nome == "":
        return f"/{lingua}/{resto}"
    if nome in INTERNE:
        return f"/{lingua}/{nome}{resto}"
    return None


def collegamenti(src, lingua):
    def sost(m):
        nuovo = indirizzo(lingua, m.group(2))
        return f'{m.group(1)}="{nuovo}"' if nuovo else m.group(0)
    src = re.sub(r'\b(href|data-href)="(/[^"]*)"', sost, src)
    # il motore di prenotazione nella lingua della pagina (anche dentro il JSON-LD)
    src = re.sub(r'(secure-reservation[^"\s<]*?[?&](?:amp;)?lang=)it\b', rf'\g<1>{lingua}', src)
    return src


def pagina(nome, lingua):
    src = (BASE / f"{nome}.html").read_text(encoding="utf-8")
    src, n = testi(src, lingua)
    src = collegamenti(src, lingua)
    src = src.replace('<html lang="it">', f'<html lang="{lingua}">', 1)
    src = src.replace("<!DOCTYPE html>\n", "<!DOCTYPE html>\n" + AVVISO, 1)
    return src, n


if __name__ == "__main__":
    for lingua in LINGUE:
        cartella = BASE / lingua
        cartella.mkdir(exist_ok=True)
        # una pagina tolta dall'italiano sparisce anche qui
        for vecchia in cartella.glob("*.html"):
            if vecchia.stem not in PAGINE:
                vecchia.unlink()
        totale = 0
        for nome in PAGINE:
            src, n = pagina(nome, lingua)
            (cartella / f"{nome}.html").write_text(src, encoding="utf-8")
            totale += n
        print(f"  /{lingua}/  {len(PAGINE)} pagine, {totale} testi tradotti")
