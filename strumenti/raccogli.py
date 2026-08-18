#!/usr/bin/env python3
"""Ricostruisce it.json leggendo TUTTI gli elementi [data-i18n] dell'HTML.

PERCHE' ESISTE. marca.py scrive in it.json soltanto gli elementi che ha
marcato LUI in quella passata: rilanciandolo su un sito gia' marcato, it.json
si riduce ai pochi elementi nuovi. Poi costruisci.py legge quel file e
riscrive i18n.js — che da 96 KB e' sceso a 3, cioe' il sito senza traduzioni.
E' successo davvero.

La fonte di verita' non e' quello che marca.py ha appena fatto: e' l'HTML.
Da lanciare SEMPRE fra marca.py e costruisci.py.
"""
import json, re, pathlib, glob
from html.parser import HTMLParser

BASE = pathlib.Path.home() / "Documents/Fam_S.r.l./Sito Prà/pradelafam"

class Raccogli(HTMLParser):
    def __init__(self, src):
        super().__init__(convert_charrefs=False)
        self.src = src; self.righe = [0]
        for r in src.split("\n")[:-1]:
            self.righe.append(self.righe[-1] + len(r) + 1)
        self.pila = []; self.out = {}
    def off(self):
        r, c = self.getpos(); return self.righe[r-1] + c
    def handle_starttag(self, tag, attrs):
        self.pila.append((tag, self.src.find(">", self.off()) + 1, dict(attrs).get("data-i18n")))
    def handle_startendtag(self, tag, attrs):
        pass
    def handle_endtag(self, tag):
        while self.pila:
            t = self.pila.pop()
            if t[0] == tag:
                if t[2]:
                    self.out[t[2]] = re.sub(r'\s+', ' ', self.src[t[1]:self.off()]).strip()
                break

tutte = {}
for f in sorted(BASE.glob("*.html")):
    src = f.read_text(encoding="utf-8")
    r = Raccogli(src); r.feed(src)
    print(f"  {f.name:<32} {len(r.out):>3} marcatori")
    tutte.update(r.out)
(pathlib.Path(__file__).parent / "it.json").write_text(
    json.dumps(tutte, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")
print(f"\n  it.json: {len(tutte)} testi (dall'HTML, non dall'ultima passata di marca.py)")
