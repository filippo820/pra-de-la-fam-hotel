#!/usr/bin/env python3
"""Mette una chiave data-i18n su ogni elemento traducibile.

COME SI SCEGLIE L'ELEMENTO
· se contiene solo testo → la chiave va li';
· se contiene solo formattazione in linea (em, strong, br, span, b, i) →
  la chiave va comunque li' e la traduzione conterra' anche il markup. E'
  cosi' che si traduce «Un albergo con <em>posizione ideale.</em>» senza
  perdere il corsivo;
· se contiene blocchi (div, p, section...) → NON si tocca: la sua chiave
  sta piu' in basso, sui figli.

LA CHIAVE E' L'IMPRONTA DEL TESTO ITALIANO, non un progressivo: lo stesso
testo su pagine diverse (menu, piede) prende la stessa chiave e si traduce
una volta sola. E se domani si aggiunge una pagina con una frase gia' vista,
si traduce da sola.

NON RIORDINA E NON RISCRIVE L'HTML: inserisce solo un attributo, calcolando
la posizione esatta con un parser. Serializzare la pagina con un browser
l'avrebbe normalizzata tutta, ed e' esattamente il tipo di riscrittura che
su questo sito ha gia' fatto danni.
"""
import re, json, hashlib, pathlib
from html.parser import HTMLParser

BASE = pathlib.Path.home() / "Documents/Fam_S.r.l./Sito Prà/pradelafam"
INLINE = {"em", "strong", "b", "i", "br", "span", "small", "sup", "sub", "u"}
SALTA  = {"script", "style", "title", "noscript", "head", "meta", "link"}
NON_TRADURRE = re.compile(
    r'^(?:[\d\s.,:;€%°/–—-]+|IT|EN|DE|FR|ES|\||·|→|←|✕|✓|™|®|'
    r'Pr[àa] de la Fam|AlPraDeLaFam\.com|P\.IVA.*|.*@.*\..*|\+?\d[\d\s./-]*)$', re.I)

def chiave(testo):
    t = re.sub(r'\s+', ' ', testo).strip()
    return "t" + hashlib.sha1(t.encode()).hexdigest()[:10]

class Analizza(HTMLParser):
    """Trova gli elementi traducibili e la posizione dove infilare l'attributo."""
    def __init__(self, src):
        super().__init__(convert_charrefs=False)
        self.src = src
        self.righe = [0]
        for r in src.split("\n")[:-1]:
            self.righe.append(self.righe[-1] + len(r) + 1)
        self.pila = []          # (tag, pos_fine_tag_apertura, pos_inizio_tag, ha_gia_chiave)
        self.trovati = []       # (pos_inserimento, chiave, testo)
        self.dentro_salta = 0
    def off(self):
        r, c = self.getpos()
        return self.righe[r-1] + c
    def handle_starttag(self, tag, attrs):
        if tag in SALTA: self.dentro_salta += 1
        d = dict(attrs)
        # posizione subito dopo il nome del tag, dove infilare l'attributo
        inizio = self.off()
        dopo_nome = inizio + 1 + len(tag)
        self.pila.append([tag, None, inizio, dopo_nome, "data-i18n" in d, len(self.trovati)])
        # segna dove finisce il tag d'apertura
        fine = self.src.find(">", inizio) + 1
        self.pila[-1][1] = fine
    def handle_endtag(self, tag):
        if tag in SALTA and self.dentro_salta: self.dentro_salta -= 1
        while self.pila:
            t = self.pila.pop()
            if t[0] == tag:
                self.chiudi(t, self.off())
                break
    def handle_startendtag(self, tag, attrs):
        pass
    def chiudi(self, t, pos_chiusura):
        tag, apre_fine, apre_inizio, dopo_nome, ha_chiave, _ = t
        if self.dentro_salta or ha_chiave or tag in SALTA or tag in INLINE: return
        inner = self.src[apre_fine:pos_chiusura]
        if not inner.strip(): return
        # solo formattazione in linea dentro?
        tag_dentro = set(re.findall(r'<\s*/?\s*([a-zA-Z][\w-]*)', inner))
        if tag_dentro - INLINE: return          # contiene blocchi: la chiave sta piu' giu'
        testo = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', inner)).strip()
        if len(testo) < 2 or not re.search(r'[A-Za-zÀ-ÿ]', testo): return
        if NON_TRADURRE.match(testo): return
        self.trovati.append((dopo_nome, chiave(inner.strip()), inner.strip()))

def marca(f):
    src = f.read_text(encoding="utf-8")
    a = Analizza(src); a.feed(src)
    if not a.trovati: return 0, {}
    voci = {}
    fuori = sorted(a.trovati, key=lambda x: -x[0])   # dal fondo, cosi' gli offset restano validi
    out = src
    for pos, k, inner in fuori:
        out = out[:pos] + f' data-i18n="{k}"' + out[pos:]
        voci[k] = re.sub(r'\s+', ' ', inner).strip()
    f.write_text(out, encoding="utf-8")
    return len(fuori), voci

tutte = {}
tot = 0
for f in sorted(BASE.glob("*.html")):
    n, voci = marca(f)
    tutte.update(voci)
    tot += n
    print(f"  {f.name:<32} {n:>3} chiavi")
print(f"\n  {tot} elementi marcati · {len(tutte)} testi DISTINTI da tradurre")
print(f"  {sum(len(re.sub(r'<[^>]+>','',v).split()) for v in tutte.values())} parole")
(pathlib.Path(__file__).parent / "it.json").write_text(
    json.dumps(tutte, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")
print("  testi italiani salvati in it.json")
