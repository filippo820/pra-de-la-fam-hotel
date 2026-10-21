#!/usr/bin/env python3
"""Scrive il JSON-LD delle pagine interne a partire da quello della home.

LA FONTE E' UNA SOLA: il blocco pdlf-dati di index.html. Li' ogni camera e
appartamento e' gia' descritto (HotelRoom / Apartment, metri quadri,
capienza, servizi). Qui quel nodo viene copiato nella pagina dell'alloggio,
con accanto le briciole (BreadcrumbList). Se si cambia un dato, lo si cambia
in home e si rilancia questo script: le pagine non vanno toccate a mano,
altrimenti le due versioni divergono in silenzio.

Bergamotto non ha il nodo perche' in home e' fuori dal JSON-LD finche' e'
«Non disponibile» (vedi STATO.md): la sua pagina riceve solo le briciole.
La FAQ ha gia' le sue briciole, scritte da faq_costruisci.py.

Idempotente: il blocco sta fra i due segnaposto pdlf-dati e viene
sostituito a ogni passata.
"""
import json, re, pathlib

BASE = pathlib.Path(__file__).resolve().parent.parent
SITO = "https://alpradelafam.com"
INIZIO = "<!-- ══ pdlf-dati ══"
FINE = "<!-- ══ /pdlf-dati ══ -->"

PAGINE = {
    "camera-doppia": "Camera Doppia",
    "camera-doppia-economy": "Camera Doppia Economy",
    "camera-tripla": "Camera Tripla",
    "camera-familiare": "Camera Familiare",
    "appartamento-pomelo": "Appartamento Pomelo",
    "appartamento-clementina": "Appartamento Clementina",
    "appartamento-calamondino": "Appartamento Calamondino",
    "appartamento-kumquat": "Appartamento Kumquat",
    "appartamento-bergamotto": "Appartamento Bergamotto",
    "cookie": "Cookie policy",
    "privacy": "Informativa privacy",
}

home = (BASE / "index.html").read_text(encoding="utf-8")
grafo = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', home, re.S).group(1))
struttura = next(n for n in grafo["@graph"] if n.get("@id") == f"{SITO}/#struttura")
alloggi = {n["@id"]: n for n in struttura["containsPlace"] if n.get("@type") in ("HotelRoom", "Apartment")}

# la struttura, ridotta all'essenziale: chi legge solo questa pagina deve
# sapere dove sta l'alloggio senza dover seguire l'@id fino alla home
dove = {k: struttura[k] for k in ("@type", "additionalType", "@id", "name", "url", "telephone", "address", "geo")}

for slug, nome in PAGINE.items():
    f = BASE / f"{slug}.html"
    src = f.read_text(encoding="utf-8")
    nodi = []
    alloggio = alloggi.get(f"{SITO}/{slug}#alloggio")
    if alloggio:
        nodi.append(dict(alloggio, containedInPlace=dove))
    nodi.append({
        "@type": "BreadcrumbList", "@id": f"{SITO}/{slug}#briciole",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Prà de la Fam", "item": f"{SITO}/"},
            {"@type": "ListItem", "position": 2, "name": nome, "item": f"{SITO}/{slug}"},
        ]})
    corpo = json.dumps({"@context": "https://schema.org", "@graph": nodi}, ensure_ascii=False, indent=2)
    corpo = corpo.replace("</", "<\\/")       # mai un </script> dentro il JSON
    blocco = (f"{INIZIO} generato da strumenti/dati_strutturati.py dal JSON-LD della home:\n"
              f"     non modificarlo qui, cambia la home e rilancia lo script. -->\n"
              f'<script type="application/ld+json">\n{corpo}\n</script>\n{FINE}\n')
    if INIZIO in src:
        i = src.index(INIZIO); j = src.index(FINE, i) + len(FINE) + 1
        src = src[:i] + blocco + src[j:]
    else:
        m = re.search(r'<link rel="canonical"[^>]*>\n', src)
        src = src[:m.end()] + blocco + src[m.end():]
    f.write_text(src, encoding="utf-8")
    print(f"  {slug:<26} {' + '.join(n['@type'] for n in nodi)}")
