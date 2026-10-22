#!/usr/bin/env python3
"""Controlla che le traduzioni non si siano staccate.

Due domande, contro una versione di riferimento in git (di solito origin/main):

1. CHIAVI ORFANE. Ogni chiave del dizionario deve stare ancora in
   qualche pagina, e ogni data-i18n delle pagine deve stare in it.json. Una
   chiave del dizionario senza pagina e' una traduzione che non verra' mai
   mostrata; un data-i18n senza voce in it.json e' un testo che costruisci.py
   non ha mai visto.
2. TESTI TORNATI IN ITALIANO. Ogni testo italiano che nel riferimento aveva
   una traduzione deve averla ancora — cercato per TESTO, non per chiave,
   cosi' un riaggancio di chiave non nasconde una traduzione persa.

Uso:  python3 strumenti/controlla_traduzioni.py [riferimento]
Esce con codice 1 se trova qualcosa.
"""
import json, re, sys, subprocess, pathlib

BASE = pathlib.Path(__file__).resolve().parent.parent
RIF = sys.argv[1] if len(sys.argv) > 1 else "origin/main"
LINGUE = ["en", "de", "fr", "es"]

def dizionario(js):
    m = re.search(r'window\.PDLF_T = (\{.*?\});\n', js, re.S)
    return json.loads(m.group(1))

def dizionario_in(leggi):
    """Dalla fase SEO 2 il dizionario sta in strumenti/dizionario.json (lo legge
    lingue.py); prima stava dentro i18n.js. Il riferimento puo' essere l'uno o l'altro."""
    try:
        return json.loads(leggi("strumenti/dizionario.json"))
    except (FileNotFoundError, subprocess.CalledProcessError):
        return dizionario(leggi("i18n.js"))

def git(percorso):
    return subprocess.run(["git", "show", f"{RIF}:{percorso}"], cwd=BASE,
                          capture_output=True, text=True, check=True).stdout

it = json.loads((BASE / "strumenti/it.json").read_text(encoding="utf-8"))
diz = dizionario_in(lambda p: (BASE / p).read_text(encoding="utf-8"))
it_rif = json.loads(git("strumenti/it.json"))
diz_rif = dizionario_in(git)

pagine = set()
for f in BASE.glob("*.html"):
    pagine |= set(re.findall(r'data-i18n="(t[0-9a-f]{10})"', f.read_text(encoding="utf-8")))

guai = 0
senza_it = pagine - set(it)
if senza_it:
    guai += len(senza_it); print(f"  ✗ data-i18n senza voce in it.json: {sorted(senza_it)}")
for l in LINGUE:
    orfane = set(diz[l]) - pagine
    if orfane:
        guai += len(orfane); print(f"  ✗ {l}: chiavi tradotte che nessuna pagina usa: {sorted(orfane)}")

norm = lambda t: re.sub(r'\s+', ' ', t).strip()
per_testo = {norm(v): k for k, v in it.items()}
for l in LINGUE:
    persi = []
    for k_rif, testo in it_rif.items():
        if k_rif not in diz_rif[l]:
            continue                       # gia' in italiano nel riferimento
        k = per_testo.get(norm(testo))
        if k is None:
            continue                       # testo tolto o cambiato apposta
        if k not in diz[l]:
            persi.append(testo)
    if persi:
        guai += len(persi)
        print(f"  ✗ {l}: {len(persi)} testi tornati in italiano")
        for t in persi[:10]:
            print(f"      · {re.sub(r'<[^>]+>', '', t)[:80]}")
    print(f"  {l}: {len(diz[l])} testi tradotti (riferimento {RIF}: {len(diz_rif[l])})")

cambiati = sorted(set(it_rif.values()) - set(it.values()))
nuovi = sorted(set(it.values()) - set(it_rif.values()))
print(f"\n  testi italiani tolti o cambiati rispetto a {RIF}: {len(cambiati)} · nuovi: {len(nuovi)}")
for t in nuovi:
    k = per_testo[norm(t)]
    mancano = [l for l in LINGUE if k not in diz[l]]
    stato = "tradotto in tutte le lingue" if not mancano else f"⚠️ in italiano in: {', '.join(mancano)}"
    print(f"    + {re.sub(r'<[^>]+>', '', t)[:70]}  — {stato}")
print("\n  " + ("✓ nessuna chiave orfana, nessun testo tornato in italiano" if not guai else f"✗ {guai} problemi"))
sys.exit(1 if guai else 0)
