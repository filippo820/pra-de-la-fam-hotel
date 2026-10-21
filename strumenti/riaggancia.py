#!/usr/bin/env python3
"""Riaggancia le chiavi data-i18n degli elementi il cui testo e' cambiato.

PERCHE' ESISTE. La chiave e' l'impronta del testo italiano (marca.py). Se si
cambia il testo di un elemento gia' marcato, la chiave resta quella vecchia:
marca.py salta gli elementi che hanno gia' un data-i18n, e la traduzione
continua a cercare il testo di prima. Qui si ricalcola l'impronta e si
sostituisce l'attributo, toccando SOLO quel valore.

NON TOCCA LE CHIAVI STORICHE. Nel sito ci sono chiavi che non coincidono con
l'impronta del loro testo da prima (correzioni di refusi tenute apposta sulla
chiave vecchia, impronte messe a mano). Si riconoscono perche' non
coincidevano gia' nell'ultima versione salvata in git: quelle restano.
Si riagganciano solo gli elementi che coincidevano e ora non piu'.

Ordine: marca.py → raccogli.py → riaggancia.py → raccogli.py → costruisci.py → kb.py
(la seconda passata di raccogli.py riscrive it.json con le chiavi nuove).
Le traduzioni si ricostruiscono da sole se i frammenti di testo sono gia' in
trad_*.json; i frammenti nuovi vanno aggiunti li'.
"""
import re, hashlib, pathlib, subprocess
from html.parser import HTMLParser

BASE = pathlib.Path(__file__).resolve().parent.parent

def chiave(testo):
    return "t" + hashlib.sha1(re.sub(r'\s+', ' ', testo).strip().encode()).hexdigest()[:10]

class Elementi(HTMLParser):
    """(chiave, testo interno, inizio del tag d'apertura) di ogni [data-i18n]."""
    def __init__(self, src):
        super().__init__(convert_charrefs=False)
        self.src = src; self.righe = [0]
        for r in src.split("\n")[:-1]:
            self.righe.append(self.righe[-1] + len(r) + 1)
        self.pila = []; self.out = []
    def off(self):
        r, c = self.getpos(); return self.righe[r-1] + c
    def handle_starttag(self, tag, attrs):
        inizio = self.off()
        self.pila.append((tag, inizio, self.src.find(">", inizio) + 1, dict(attrs).get("data-i18n")))
    def handle_startendtag(self, tag, attrs):
        pass
    def handle_endtag(self, tag):
        while self.pila:
            t = self.pila.pop()
            if t[0] == tag:
                if t[3]:
                    self.out.append((t[3], self.src[t[2]:self.off()].strip(), t[1], t[2]))
                break

def elementi(src):
    e = Elementi(src); e.feed(src); return e.out

def storiche(nome):
    """Chiavi che gia' nell'ultima versione in git non erano l'impronta del loro testo."""
    r = subprocess.run(["git", "show", f"HEAD:{nome}"], cwd=BASE, capture_output=True, text=True)
    if r.returncode != 0:
        return set()
    return {k for k, testo, _, _ in elementi(r.stdout) if chiave(testo) != k}

tot = 0
for f in sorted(BASE.glob("*.html")):
    src = f.read_text(encoding="utf-8")
    vecchie = storiche(f.name)
    cambi = []
    for k, testo, inizio, fine in elementi(src):
        nuova = chiave(testo)
        if nuova != k and k not in vecchie:
            cambi.append((inizio, fine, k, nuova, testo))
    for inizio, fine, k, nuova, testo in sorted(cambi, reverse=True):
        tag = src[inizio:fine].replace(f'data-i18n="{k}"', f'data-i18n="{nuova}"', 1)
        src = src[:inizio] + tag + src[fine:]
        print(f"  {f.name:<30} {k} → {nuova}  {re.sub(r'<[^>]+>', '', testo)[:60]}")
    if cambi:
        f.write_text(src, encoding="utf-8")
        tot += len(cambi)
print(f"\n  {tot} chiavi riagganciate")
