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
  · il motore di prenotazione riceve lang= della pagina;
  · ogni pagina, italiana compresa, dichiara le sue cinque versioni
    (hreflang, piu' x-default verso l'italiano) in un blocco fra i segnaposto
    pdlf-lingue, scritto anche nella pagina italiana. Canonical, og:url,
    og:locale e gli indirizzi del JSON-LD puntano alla pagina nella sua
    lingua;
  · il selettore IT/EN/DE/FR/ES sono link veri (<a hreflang>): qui se ne
    scrivono gli href — la stessa pagina nell'altra lingua — e si segna
    quella attiva. Questo e il blocco hreflang sono le sole cose che lo
    script scrive anche nelle sorgenti italiane;
  · _redirects: fra i segnaposto «lingue» le regole delle pagine nuove — il
    301! da /de/faq.html a /de/faq, le vecchie URL del WordPress
    (/de_DE/clementina/) verso la pagina nella lingua giusta, il resto del
    vecchio sito verso la home della lingua, e la 404 per lingua. Nessuna
    regola per la barra finale: Netlify la toglie da solo, e una regola
    «/de/:pagina/» faceva un giro infinito sulle pagine che non esistono. Le vecchie
    pagine si leggono dalle regole «/:lingua/<pagina>» gia' nel file: la
    mappa resta una sola;
  · sitemap.xml: tutte le pagine indicizzabili nelle cinque lingue, ognuna
    con le sue alternative. lastmod resta quello di prima finche' la pagina
    non cambia: una data che si sposta a ogni passata non dice niente a
    nessuno, e Google smette di crederci;
  · cio' che il dizionario non copre — <title>, description, anteprime
    social, alt, aria-label e i testi del JSON-LD — si traduce da
    trad_meta.json; se li' non c'e', da un frammento gia' tradotto
    (trad_corti/trad_lunghi) o da un testo visibile identico. Le risposte
    della FAQ nel JSON-LD sono i paragrafi visibili uniti da uno spazio
    (faq_costruisci.py): si ricompongono dai paragrafi tradotti.
    Un testo che non si trova da nessuna parte resta in italiano, e lo
    script lo elenca ed esce con errore: meglio saperlo che pubblicarlo;
  · cookie e privacy tradotte: in cima la riga «fa fede la versione
    italiana», che la pagina italiana non ha (vedi LEGALI).

Ordine della procedura: marca.py → raccogli.py → riaggancia.py → raccogli.py
→ costruisci.py → lingue.py → kb.py
"""
import json, re, sys, datetime, pathlib, html as H
from html.parser import HTMLParser

BASE = pathlib.Path(__file__).resolve().parent.parent
S = BASE / "strumenti"
LINGUE = ["en", "de", "fr", "es"]
TUTTE = ["it"] + LINGUE
SITO = "https://alpradelafam.com"
LOCALE = {"it": "it_IT", "en": "en_GB", "de": "de_DE", "fr": "fr_FR", "es": "es_ES"}

DIZ = json.loads((S / "dizionario.json").read_text(encoding="utf-8"))
PAGINE = sorted(p.stem for p in BASE.glob("*.html"))          # index, faq, 404, ...
INTERNE = {p for p in PAGINE if p not in ("index", "404")}      # indirizzi /<pagina>

# ── le traduzioni fuori dal dizionario
def piano(t):
    """Il testo come lo legge chi guarda: senza tag, entita' risolte, spazi normali."""
    return re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]+>', ' ', t))).strip()

_meta = json.loads((S / "trad_meta.json").read_text(encoding="utf-8"))
INVARIATI = set(_meta.get("_invariati", []))
META = {piano(k): v for k, v in _meta.items() if not k.startswith("_")}
FRAMMENTI = {}
for _f in ("trad_corti.json", "trad_lunghi.json"):
    for k, v in json.loads((S / _f).read_text(encoding="utf-8")).items():
        if not k.startswith("_"):
            FRAMMENTI[piano(k)] = {l: piano(t) for l, t in v.items()}
_it = json.loads((S / "it.json").read_text(encoding="utf-8"))
VISIBILI = {l: {} for l in LINGUE}          # testo italiano visibile → tradotto
for k, v in _it.items():
    for l in LINGUE:
        if k in DIZ[l]:
            VISIBILI[l].setdefault(piano(v), piano(DIZ[l][k]))
MANCANTI = {}                               # (testo, lingua) → dove


def traduci(testo, lingua, dove=""):
    """Il testo tradotto (piano), o None se non c'e' — e allora lo si annota."""
    n = piano(testo)
    if not re.search(r'[A-Za-zÀ-ÿ]', n) or n in INVARIATI:
        return n
    for fonte in (META, FRAMMENTI):
        if lingua in fonte.get(n, {}):
            return fonte[n][lingua]
    if n in VISIBILI[lingua]:
        return VISIBILI[lingua][n]
    composto = ricomponi(n, lingua)
    if composto:
        return composto
    MANCANTI.setdefault((n, lingua), dove)
    return None


def ricomponi(n, lingua):
    """«par1 par2 par3» → i tre paragrafi tradotti, se ognuno e' un testo visibile."""
    v = VISIBILI[lingua]
    tagli = [0] + [m.end() for m in re.finditer(r' ', n)] + [len(n) + 1]
    migliore = {0: []}
    for i in tagli:
        if i not in migliore:
            continue
        for j in tagli:
            if j > i and j - 1 > i and (n[i:j - 1] in v) and j not in migliore:
                migliore[j] = migliore[i] + [v[n[i:j - 1]]]
    fine = len(n) + 1
    return " ".join(migliore[fine]) if fine in migliore and len(migliore[fine]) > 1 else None


# chiavi del JSON-LD che non sono testo da leggere
NON_TESTO = {"@id", "@type", "@context", "url", "item", "image", "logo", "telephone", "email",
             "sameAs", "streetAddress", "postalCode", "addressRegion", "addressCountry",
             "addressLocality", "latitude", "longitude", "priceCurrency", "unitCode", "hasMap",
             "urlTemplate", "checkinTime", "checkoutTime", "inLanguage", "actionPlatform",
             "additionalType", "contentUrl", "encodingFormat", "currenciesAccepted",
             "paymentAccepted", "openingHours", "vatID", "taxID", "foundingDate", "areaServed"}


def dati(src, lingua, nome):
    """Traduce i testi dentro i blocchi JSON-LD."""
    def giro(o, chiave=None):
        if isinstance(o, dict):
            return {k: (lingua if k == "inLanguage" else
                        nella_lingua(v, lingua) if k in ("url", "item") else
                        v if k in NON_TESTO else giro(v, k))
                    for k, v in o.items()}
        if isinstance(o, list):
            return [giro(v, chiave) for v in o]
        if isinstance(o, str):
            t = traduci(o, lingua, f"{nome}: JSON-LD «{chiave}»")
            return t if t is not None else o
        return o
    def blocco(m):
        g = giro(json.loads(m.group(2).replace("<\\/", "</")))
        corpo = json.dumps(g, ensure_ascii=False, indent=2).replace("</", "<\\/")
        return f"{m.group(1)}\n{corpo}\n{m.group(3)}"
    return re.sub(r'(<script type="application/ld\+json">)\s*(.*?)\s*(</script>)', blocco, src, flags=re.S)


def attributi(src, lingua, nome):
    """<title>, meta delle anteprime, alt, aria-label e le etichette della mappa."""
    def sost(t, dove, quote):
        if not t.strip():
            return None
        r = traduci(t, lingua, f"{nome}: {dove}")
        return None if r is None else H.escape(r, quote=quote)
    m = re.search(r'<title>(.*?)</title>', src, re.S)
    r = sost(m.group(1), "title", False)
    if r is not None:
        src = src[:m.start(1)] + r + src[m.end(1):]
    def meta(m):
        r = sost(m.group(3), m.group(2), True)
        return m.group(0) if r is None else f'{m.group(1)}{r}"'
    src = re.sub(r'(<meta (?:name|property)="(description|og:title|og:description|og:image:alt|'
                 r'twitter:title|twitter:description|twitter:image:alt)" content=")([^"]*)"', meta, src)
    def attr(m):
        r = sost(m.group(3), m.group(2), True)
        return m.group(0) if r is None else f'{m.group(1)}{r}"'
    # data-name/-detail/-cta: le etichette dei punti sulla mappa della home,
    # che lo script della mappa mostra al passaggio
    return re.sub(r'(\b(alt|aria-label|placeholder|data-name|data-detail|data-cta)=")([^"]*)"', attr, src)


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


def nella_lingua(url, lingua):
    """https://alpradelafam.com/faq → https://alpradelafam.com/de/faq (solo le pagine)."""
    if not isinstance(url, str) or not url.startswith(SITO + "/"):
        return url
    nuovo = indirizzo(lingua, url[len(SITO):])
    return SITO + nuovo if nuovo else url


def assoluto(nome, lingua):
    """L'indirizzo canonico della pagina nella lingua, senza .html."""
    percorso = "" if nome == "index" else nome
    return f"{SITO}/{percorso}" if lingua == "it" else f"{SITO}/{lingua}/{percorso}"


INIZIO_ALT = "<!-- ══ pdlf-lingue ══"
FINE_ALT = "<!-- ══ /pdlf-lingue ══ -->"


def alternative(src, nome):
    """Il blocco hreflang (uguale in tutte e cinque le versioni) subito dopo il canonical."""
    righe = [f'<link rel="alternate" hreflang="{l}" href="{assoluto(nome, l)}" />' for l in TUTTE]
    righe.append(f'<link rel="alternate" hreflang="x-default" href="{assoluto(nome, "it")}" />')
    blocco = (f"{INIZIO_ALT} la stessa pagina nelle cinque lingue: lo scrive strumenti/lingue.py -->\n"
              + "\n".join(righe) + f"\n{FINE_ALT}\n")
    if INIZIO_ALT in src:
        i = src.index(INIZIO_ALT); j = src.index(FINE_ALT, i) + len(FINE_ALT) + 1
        return src[:i] + blocco + src[j:]
    m = re.search(r'<link rel="canonical"[^>]*>\n', src)
    return src[:m.end()] + blocco + src[m.end():]


def percorso(nome, lingua):
    """Come assoluto(), ma dalla radice del sito: vale anche su un'anteprima Netlify."""
    return assoluto(nome, lingua)[len(SITO):]


def selettore(src, nome, lingua):
    """I link del selettore di lingua: href giusto, e la lingua della pagina attiva."""
    def sost(m):
        tag, l = m.group(0), m.group(1)
        tag = re.sub(r' href="[^"]*"', f' href="{percorso(nome, l)}"', tag)
        tag = re.sub(r' aria-current="true"', '', tag)
        tag = re.sub(r'class="([\w-]+)(?: active)?"',
                     lambda c: f'class="{c.group(1)} active"' if l == lingua else f'class="{c.group(1)}"', tag)
        if l == lingua:
            tag = tag.replace(f' lang="{l}"', f' lang="{l}" aria-current="true"', 1)
        return tag
    return re.sub(r'<a\b[^>]*\bhreflang="(\w\w)"[^>]*>', sost, src)


def indirizzi(src, nome, lingua):
    """canonical, og:url e og:locale della pagina nella sua lingua."""
    qui = assoluto(nome, lingua)
    src = re.sub(r'(<link rel="canonical" href=")[^"]*"', rf'\g<1>{qui}"', src)
    src = re.sub(r'(<meta property="og:url" content=")[^"]*"', rf'\g<1>{qui}"', src)
    altre = "".join(f'<meta property="og:locale:alternate" content="{LOCALE[l]}" />\n'
                    for l in TUTTE if l != lingua)
    return re.sub(r'<meta property="og:locale" content="[^"]*" />\n'
                  r'(?:<meta property="og:locale:alternate" content="[^"]*" />\n)*',
                  f'<meta property="og:locale" content="{LOCALE[lingua]}" />\n{altre}', src)


def collegamenti(src, lingua):
    def sost(m):
        nuovo = indirizzo(lingua, m.group(2))
        return f'{m.group(1)}="{nuovo}"' if nuovo else m.group(0)
    src = re.sub(r'\b(href|data-href)="(/[^"]*)"', sost, src)
    # il motore di prenotazione nella lingua della pagina (anche dentro il JSON-LD)
    src = re.sub(r'(secure-reservation[^"\s<]*?[?&](?:amp;)?lang=)it\b', rf'\g<1>{lingua}', src)
    return src


# Le pagine legali tradotte dicono in cima che vale il testo italiano (decisione
# di Filippo, 23/10/2026). Sulla pagina italiana non serve, quindi la riga non
# sta nella sorgente: la aggiunge solo questo script, prima della data. La
# traduzione e' in trad_meta.json come le altre.
LEGALI = ("cookie", "privacy")
FA_FEDE = "In caso di difformità fa fede la versione italiana."


def fa_fede(src, lingua, nome):
    riga = traduci(FA_FEDE, lingua, f"{lingua}/{nome}")
    if riga is None:
        return src
    src, n = re.subn(r'(\n *)(<p data-i18n="[^"]+" class="agg">)',
                     lambda m: (f'{m.group(1)}<p class="fede" style="font-size:.85rem;font-style:italic;'
                                f'color:var(--steel);margin-bottom:6px">{H.escape(riga, quote=False)}</p>'
                                f'{m.group(1)}{m.group(2)}'), src, count=1)
    if n != 1:
        sys.exit(f"lingue.py: in {nome}.html manca la data (class=\"agg\") sotto cui va «{FA_FEDE}»")
    return src


def pagina(nome, lingua):
    src = (BASE / f"{nome}.html").read_text(encoding="utf-8")
    src, n = testi(src, lingua)
    if nome in LEGALI:
        src = fa_fede(src, lingua, nome)
    src = collegamenti(src, lingua)
    src = attributi(src, lingua, f"{lingua}/{nome}")
    src = dati(src, lingua, f"{lingua}/{nome}")
    src = indirizzi(src, nome, lingua)
    src = selettore(src, nome, lingua)
    src = src.replace('<html lang="it">', f'<html lang="{lingua}">', 1)
    src = src.replace("<!DOCTYPE html>\n", "<!DOCTYPE html>\n" + AVVISO, 1)
    return src, n


# i prefissi del vecchio WordPress e la lingua nuova che gli corrisponde. Il
# vecchio sito non aveva lo spagnolo: es_ES non esisteva, ma se qualcuno lo
# scrive a mano arriva comunque alle pagine in spagnolo.
VECCHI = {"it_IT": "it", "en_GB": "en", "en_US": "en", "de_DE": "de", "fr_FR": "fr",
          "es_ES": "es", "wp": "it"}
INIZIO_RED = "# ══ lingue: generato da strumenti/lingue.py — non modificare a mano ══"
FINE_RED = "# ══ /lingue ══"


def reindirizzi():
    """Riscrive il blocco delle lingue in _redirects; ne restituisce le righe."""
    f = BASE / "_redirects"
    src = f.read_text(encoding="utf-8")
    vecchie = []                                   # (pagina vecchia, destinazione italiana)
    for m in re.finditer(r'^/:lingua/(\S+?)\s+(\S+)\s+301\s*$', src, re.M):
        if (m.group(1), m.group(2)) not in vecchie:
            vecchie.append((m.group(1), m.group(2)))
    w = max(len(f"/{v}/{p}") for v in VECCHI for p, _ in vecchie) + 2
    def riga(da, a, codice):
        return f"{da:<{w}}{a:<{w}}{codice}"
    out = [INIZIO_RED, "#",
           "# Ogni lingua ha le sue pagine: /de/faq e' la FAQ in tedesco. Qui, nell'ordine:",
           "#  1. un indirizzo solo anche nelle lingue nuove: /de/faq.html → /de/faq",
           "#     (il ! serve perche' il file esiste, come per l'italiano qui sopra);",
           "#  2. le vecchie URL del WordPress verso la pagina nella LORO lingua:",
           "#     /de_DE/clementina/ → /de/appartamento-clementina, non piu' l'italiano;",
           "#  3. il resto del vecchio sito alla home della lingua, non alla 404;",
           "#  4. un indirizzo che non esiste sotto /de/ → la 404 in tedesco, con stato",
           "#     404. Senza «!»: Netlify la applica solo se il file NON esiste.",
           "# /de/pagina/ con la barra finale lo porta Netlify da solo a /de/pagina.",
           "# NON aggiungere una regola «/de/:pagina/ → /de/:pagina»: Netlify confronta",
           "# le regole ignorando la barra finale, e per una pagina che non esiste",
           "# rimandava a se' stessa all'infinito (visto sull'anteprima del 22/10).",
           "# Stanno PRIMA delle regole «/:lingua/...» qui sotto: Netlify applica la",
           "# prima che corrisponde, e quelle manderebbero /de_DE/... all'italiano.", ""]
    for l in LINGUE:
        out.append(riga(f"/{l}/index.html", f"/{l}/", "301!"))
        out += [riga(f"/{l}/{p}.html", percorso(p, l), "301!") for p in PAGINE if p in INTERNE]
        out.append("")
    for v, l in VECCHI.items():
        for p, a in vecchie:
            dest = a if l == "it" else (indirizzo(l, a) or f"/{l}/")
            out.append(riga(f"/{v}/{p}", dest, "301"))
        out.append(riga(f"/{v}/*", "/" if l == "it" else f"/{l}/", "301"))
        out.append("")
    for l in LINGUE:
        out.append(riga(f"/{l}/*", f"/{l}/404.html", "404"))
    out.append(FINE_RED)
    blocco = "\n".join(out) + "\n"
    if INIZIO_RED in src:
        i = src.index(INIZIO_RED); j = src.index(FINE_RED, i) + len(FINE_RED) + 1
        src = src[:i] + blocco + src[j:]
    else:
        i = src.index("\n/hotel ") + 1
        src = src[:i] + blocco + "\n" + src[i:]
    f.write_text(src, encoding="utf-8")
    return sum(1 for r in out if r and not r.startswith("#"))


PRIORITA = {"index": "1.0", "faq": "0.8", "cookie": "0.3", "privacy": "0.3"}   # le altre 0.9


def sitemap(cambiate):
    """Riscrive sitemap.xml. `cambiate`: le (pagina, lingua) riscritte in questa passata."""
    f = BASE / "sitemap.xml"
    prima = dict(re.findall(r'<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>', f.read_text(encoding="utf-8")))
    oggi = datetime.date.today().isoformat()
    righe = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<!-- Scritta da strumenti/lingue.py: ogni pagina nelle cinque lingue, con le sue alternative. -->',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for nome in ["index"] + [p for p in PAGINE if p != "index"]:
        if nome == "404":
            continue
        # se cambia una traduzione, e' cambiata la pagina in tutte le lingue:
        # la sorgente e' una sola
        toccata = any((nome, l) in cambiate for l in TUTTE)
        for lingua in TUTTE:
            loc = assoluto(nome, lingua)
            righe += ["  <url>", f"    <loc>{loc}</loc>",
                      f"    <lastmod>{oggi if toccata or loc not in prima else prima[loc]}</lastmod>",
                      f"    <priority>{PRIORITA.get(nome, '0.9')}</priority>"]
            righe += [f'    <xhtml:link rel="alternate" hreflang="{l}" href="{assoluto(nome, l)}"/>' for l in TUTTE]
            righe += [f'    <xhtml:link rel="alternate" hreflang="x-default" href="{assoluto(nome, "it")}"/>',
                      "  </url>"]
    righe.append("</urlset>")
    f.write_text("\n".join(righe) + "\n", encoding="utf-8")
    return sum(1 for r in righe if r == "  <url>")


if __name__ == "__main__":
    cambiate = set()
    # prima le sorgenti italiane: il blocco hreflang (la 404 non ha versioni da
    # dichiarare: non e' indicizzata e non ha un indirizzo suo)
    for nome in PAGINE:
        if nome == "404":
            continue
        f = BASE / f"{nome}.html"
        prima = f.read_text(encoding="utf-8")
        dopo = selettore(alternative(prima, nome), nome, "it")
        if dopo != prima:
            f.write_text(dopo, encoding="utf-8")
            cambiate.add((nome, "it"))
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
            dove = cartella / f"{nome}.html"
            if not dove.exists() or dove.read_text(encoding="utf-8") != src:
                dove.write_text(src, encoding="utf-8")
                cambiate.add((nome, lingua))
            totale += n
        print(f"  /{lingua}/  {len(PAGINE)} pagine, {totale} testi tradotti")
    print(f"  sitemap.xml: {sitemap(cambiate)} indirizzi; pagine riscritte in questa passata: {len(cambiate)}")
    print(f"  _redirects: {reindirizzi()} regole delle lingue")
    if MANCANTI:
        print(f"\n  ✗ {len(MANCANTI)} testi senza traduzione (restano in italiano):")
        for (t, l), dove in sorted(MANCANTI.items(), key=lambda x: (x[1], x[0][1])):
            print(f"    {l} · {dove} · {t[:90]}")
        sys.exit(1)
