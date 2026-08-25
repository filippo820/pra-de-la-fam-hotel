# -*- coding: utf-8 -*-
"""Rigenera faq.html — testo visibile e JSON-LD dalla STESSA fonte.

Le domande e le risposte stanno in faq_dati.py: qui si costruisce la pagina e
il blocco FAQPage leggendo quell'unico file, cosi' non possono dire due cose
diverse. E' il difetto tipico dei dati strutturati scritti a mano: si cambia la
risposta in pagina e ci si dimentica del JSON, e la versione che le IA ripetono
resta quella vecchia.

Le chiavi data-i18n si calcolano qui come le calcola marca.py — impronta sha1
del testo italiano, primi 10 caratteri — perche' marca.py NON marca dentro un
<summary>, e le domande stanno tutte li'.

Dopo averlo lanciato: raccogli.py e poi costruisci.py, altrimenti le traduzioni
delle frasi nuove non entrano in i18n.js.
"""
import sys, json, hashlib, re, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from faq_dati import GRUPPI

BASE = pathlib.Path.home() / "Documents/Fam_S.r.l./Sito Prà/pradelafam"
SITO = "https://alpradelafam.com"
BOOK = "https://www.secure-reservation.cloud/booking-engine/?portal=pradelafam-tignale&lang=it"

def k(t):
    return "t" + hashlib.sha1(re.sub(r'\s+', ' ', t).strip().encode()).hexdigest()[:10]

def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

TITOLO = "Domande frequenti — Prà de la Fam · Hotel sul Lago di Garda · Tignale"
DESCR = ("Le domande che ci fanno ogni giorno alla reception: come si arriva sulla Gardesana, "
         "il parcheggio, la spiaggia, i cani, gli orari, la limonaia storica del Prà de la Fam.")

# ── JSON-LD: FAQPage + il filo verso la struttura e le briciole
faq_nodi = []
for _, _, domande in GRUPPI:
    for d, risposte in domande:
        faq_nodi.append({
            "@type": "Question",
            "name": d,
            "acceptedAnswer": {"@type": "Answer", "text": " ".join(risposte)},
        })

grafo = {"@context": "https://schema.org", "@graph": [
    {"@type": "FAQPage", "@id": f"{SITO}/faq#faq", "url": f"{SITO}/faq",
     "name": TITOLO, "inLanguage": "it",
     "description": DESCR,
     "about": {"@id": f"{SITO}/#struttura"},
     "isPartOf": {"@id": f"{SITO}/#sito"},
     "publisher": {"@id": f"{SITO}/#azienda"},
     "mainEntity": faq_nodi},
    {"@type": "BreadcrumbList", "@id": f"{SITO}/faq#briciole", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Prà de la Fam", "item": f"{SITO}/"},
        {"@type": "ListItem", "position": 2, "name": "Domande frequenti", "item": f"{SITO}/faq"},
    ]},
]}
jsonld = json.dumps(grafo, ensure_ascii=False, indent=2)

# ── il corpo della pagina: stesse domande, stesse risposte
corpo = []
for i, (gruppo, sottotitolo, domande) in enumerate(GRUPPI):
    corpo.append('  <section class="faq-gruppo r d1">')
    corpo.append(f'    <p data-i18n="{k(gruppo)}" class="faq-gruppo-idx">0{i+1} — {esc(gruppo)}</p>'
                 .replace(f'>0{i+1} — ', f'>0{i+1} — ', 1))
    corpo.append(f'    <h2 data-i18n="{k(sottotitolo)}" class="faq-gruppo-tit">{esc(sottotitolo)}</h2>')
    for d, risposte in domande:
        corpo.append(f'    <details class="faq-voce" id="d-{k(d)[1:]}">')
        corpo.append('      <summary class="faq-testa">')
        corpo.append(f'        <h3 data-i18n="{k(d)}" class="faq-dom">{esc(d)}</h3>')
        corpo.append('        <svg class="faq-chev" width="15" height="15" viewBox="0 0 24 24" fill="none"'
                     ' stroke="currentColor" stroke-width="2.2" stroke-linecap="round"'
                     ' stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>')
        corpo.append('      </summary>')
        corpo.append('      <div class="faq-risp">')
        for r in risposte:
            corpo.append(f'        <p data-i18n="{k(r)}">{esc(r)}</p>')
        corpo.append('      </div>')
        corpo.append('    </details>')
    corpo.append('  </section>')
CORPO = "\n".join(corpo)

INTRO = ("Queste sono le domande che ci arrivano davvero al telefono e al banco, con la "
         "risposta per esteso — la stessa che daremmo di persona. Se quello che cercate non "
         "c'è, chiamateci: rispondiamo noi, non un centralino.")
OCCHIELLO = "Prà de la Fam · Informazioni"
H1A, H1B = "Domande", "dalla reception."
CHIUSA_T = "Non avete trovato la risposta?"
CHIUSA_P = ("Il telefono lo alza la famiglia che gestisce la struttura. Chiamate o scrivete: "
            "vi diciamo com'è davvero, anche quando la risposta è «quella settimana siamo pieni».")

PAGINA = f'''<!DOCTYPE html>
<html lang="it">
<head>
<!-- ══ pdlf-analytics ══ consenso PRIMA del tag: si nega di default e si concede solo se l'utente accetta -->
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('consent', 'default', {{
    'analytics_storage': 'denied',
    'ad_storage': 'denied',
    'wait_for_update': 500
  }});
</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-M29PYB9NDX"></script>
<script>
  gtag('js', new Date());
  (function(){{
    var lang = 'it';
    try {{ lang = localStorage.getItem('pdlf_lang') || document.documentElement.lang || 'it'; }} catch(e){{}}
    var slug = location.pathname.replace(/\\/+$/,'').split('/').pop() || 'home';
    slug = slug.replace(/\\.html$/,'') || 'home';
    gtag('config', 'G-M29PYB9NDX', {{ pdlf_lang: lang, pdlf_pagina: slug }});
    window.__pdlf = {{ lang: lang, slug: slug }};
  }})();
</script>

<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>{TITOLO}</title>
<meta property="og:type" content="website" />
<meta property="og:site_name" content="Prà de la Fam" />
<meta property="og:locale" content="it_IT" />
<meta property="og:title" content="{TITOLO}" />
<meta property="og:description" content="{DESCR}" />
<meta property="og:url" content="{SITO}/faq" />
<meta property="og:image" content="{SITO}/og/index.jpg" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:image:alt" content="Prà de la Fam — Hotel e Appartamenti sul Lago di Garda · Tignale" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{TITOLO}" />
<meta name="twitter:description" content="{DESCR}" />
<meta name="twitter:image" content="{SITO}/og/index.jpg" />
<link rel="canonical" href="{SITO}/faq" />

<meta name="description" content="{DESCR}"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400;1,600&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet"/>

<!-- ══ pdlf-dati ══ le stesse domande e le stesse risposte che si leggono qui sotto,
     in una forma che una macchina prende senza doverle ritagliare dalla pagina.
     Le une e le altre escono dallo STESSO file (strumenti/faq_dati.py): non possono
     divergere, che e' il difetto tipico di questi blocchi scritti a mano.

     ⚠️ Se si cambia una risposta nella pagina, va cambiata anche qui — o meglio, si
     rigenera la pagina con strumenti/faq_costruisci.py. -->
<script type="application/ld+json">
{jsonld}
</script>

<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --ink:#0b1520;--mid:#2e4a62;--steel:#4a6580;
  --bone:#f7f4ef;--warm:#ede8df;
  --gold:#b8934a;--gold2:#d4b06a;--gold3:#f0d898;
  --gold-testo:#7d6331;    /* 5.17 su crema · 4.65 sul fondo caldo · 5.67 su bianco */
  --gold-titolo:#9a7a3c;   /* 3.66:1 su crema — solo per il corsivo grande dei titoli */
  --white:#ffffff;
  --ease:cubic-bezier(.22,.68,0,1.2);
  --shadow-float:0 20px 60px rgba(11,21,32,.18),0 4px 16px rgba(11,21,32,.1);
}}
html{{scroll-behavior:smooth}}
body{{font-family:'DM Sans',sans-serif;background:var(--bone);color:var(--ink);overflow-x:hidden}}

/* NAV — identica alle pagine di camere e appartamenti */
nav{{position:fixed;top:0;left:0;right:0;z-index:500;display:flex;align-items:center;justify-content:space-between;padding:0 clamp(1.5rem,4vw,4rem);height:68px;background:rgba(247,244,239,.96);backdrop-filter:blur(24px) saturate(1.5);border-bottom:1px solid rgba(11,21,32,.08)}}
.nav-logo-img{{height:44px;width:auto;display:block}}
.nav-logo{{display:flex;align-items:center;gap:.75rem;text-decoration:none}}
.nav-back{{margin-left:1.5rem;font-size:.68rem;font-weight:400;letter-spacing:.12em;text-transform:uppercase;color:var(--steel);text-decoration:none;transition:color .2s;display:flex;align-items:center;gap:.5rem}}
.nav-back:hover{{color:var(--ink)}}
.nav-back::before{{content:'←';font-size:.8rem}}
.nav-cta{{display:inline-flex;align-items:center;gap:.4rem;background:var(--ink);color:var(--bone);font-size:.68rem;font-weight:500;letter-spacing:.1em;text-transform:uppercase;padding:.5rem 1.3rem;border-radius:2px;text-decoration:none;transition:background .2s}}
.nav-cta:hover{{background:var(--mid)}}

/* APERTURA — piu' bassa di quella delle camere: qui si viene a leggere, non a guardare */
.faq-hero{{position:relative;height:46vh;min-height:320px;overflow:hidden;display:grid;place-items:end}}
.faq-hbg{{position:absolute;inset:0;background:var(--ink) center/cover no-repeat}}
.faq-hov{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(11,21,32,.15) 0%,rgba(11,21,32,.35) 45%,rgba(11,21,32,.82) 100%)}}
.faq-hc{{position:relative;z-index:2;width:100%;padding:0 clamp(1.5rem,5vw,5rem) clamp(2.2rem,5vh,4rem)}}
.faq-eyebrow{{font-size:.6rem;letter-spacing:.22em;text-transform:uppercase;color:rgba(247,244,239,.6);margin-bottom:.8rem;display:flex;align-items:center;gap:.6rem}}
.faq-eyebrow::before{{content:'';display:block;width:22px;height:1px;background:var(--gold2)}}
.faq-h1{{font-family:'Cormorant Garamond',serif;font-size:clamp(2.4rem,6.5vw,5rem);font-weight:300;line-height:.95;color:var(--white);letter-spacing:-.015em}}
.faq-h1 em{{font-style:italic;color:var(--gold3)}}

/* CORPO */
.faq-body{{max-width:900px;margin:0 auto;padding:clamp(3rem,7vw,6rem) clamp(1.5rem,5vw,4rem) 0}}
.faq-intro{{font-size:1rem;font-weight:300;line-height:2;color:var(--steel);margin-bottom:clamp(2.5rem,6vw,4rem);border-left:2px solid var(--gold-testo);padding-left:1.2rem}}
.faq-gruppo{{margin-bottom:clamp(2.8rem,6vw,4.5rem)}}
.faq-gruppo-idx{{font-size:.6rem;letter-spacing:.2em;text-transform:uppercase;color:var(--gold-testo);margin-bottom:.6rem}}
.faq-gruppo-tit{{font-family:'Cormorant Garamond',serif;font-size:clamp(1.5rem,3vw,2.1rem);font-weight:300;line-height:1.2;color:var(--ink);margin-bottom:1.8rem;padding-bottom:1.2rem;border-bottom:1px solid rgba(11,21,32,.1)}}

/* OGNI DOMANDA E' UN <details>, come «Come arrivare» in home: si apre col dito e
   col tasto Invio, funziona senza JavaScript, e la risposta RESTA nel documento
   anche a scheda chiusa — quindi Google e gli assistenti la leggono lo stesso. */
.faq-voce{{border-bottom:1px solid rgba(11,21,32,.09);scroll-margin-top:88px}}
.faq-testa{{display:flex;align-items:flex-start;justify-content:space-between;gap:1.2rem;cursor:pointer;list-style:none;padding:1.15rem 0;user-select:none}}
.faq-testa::-webkit-details-marker{{display:none}}
.faq-dom{{font-family:'Cormorant Garamond',serif;font-size:clamp(1.1rem,2.2vw,1.35rem);font-weight:400;line-height:1.45;color:var(--ink);transition:color .2s}}
.faq-testa:hover .faq-dom,.faq-testa:focus-visible .faq-dom{{color:var(--gold-testo)}}
.faq-chev{{color:var(--gold-testo);flex-shrink:0;margin-top:.35rem;transition:transform .22s}}
.faq-voce[open] .faq-chev{{transform:rotate(180deg)}}
.faq-risp{{padding:0 0 1.5rem;max-width:70ch}}
.faq-risp p{{font-size:.9rem;font-weight:300;line-height:1.95;color:var(--steel);margin-bottom:.9rem}}
.faq-risp p:last-child{{margin-bottom:0}}
.faq-risp a{{color:var(--gold-testo)}}

/* CHIUSA */
.faq-chiusa{{background:var(--white);box-shadow:var(--shadow-float);border-radius:2px;padding:clamp(1.8rem,4vw,2.6rem);margin:1rem 0 clamp(3rem,6vw,5rem);display:flex;flex-wrap:wrap;gap:1.5rem;align-items:center;justify-content:space-between}}
.faq-chiusa-tit{{font-family:'Cormorant Garamond',serif;font-size:1.5rem;font-weight:300;color:var(--ink);margin-bottom:.5rem}}
.faq-chiusa-txt{{font-size:.85rem;font-weight:300;line-height:1.9;color:var(--steel);max-width:52ch}}
.faq-azioni{{display:flex;flex-direction:column;gap:.6rem;min-width:220px}}
.faq-btn{{display:flex;align-items:center;justify-content:center;gap:.5rem;background:var(--gold);color:var(--ink);font-size:.75rem;font-weight:500;letter-spacing:.12em;text-transform:uppercase;padding:.9rem 1.5rem;text-decoration:none;border-radius:2px;transition:background .25s,transform .2s;box-shadow:0 6px 28px rgba(184,147,74,.38)}}
.faq-btn:hover{{background:var(--gold2);transform:translateY(-2px)}}
.faq-btn2{{display:flex;align-items:center;justify-content:center;gap:.5rem;color:var(--steel);font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;padding:.75rem 1.5rem;text-decoration:none;border-radius:2px;border:1px solid rgba(11,21,32,.15);transition:border-color .2s,color .2s}}
.faq-btn2:hover{{border-color:var(--ink);color:var(--ink)}}

/* SCROLL REVEAL */
.r{{opacity:0;transform:translateY(24px);transition:opacity .7s var(--ease),transform .7s var(--ease)}}
.r.d1{{transition-delay:.1s}}.r.d2{{transition-delay:.2s}}
.r.in{{opacity:1;transform:none}}

/* PIEDE — la striscia delle sottopagine, da cui menu.js legge le voci del telefono */
.room-footer-strip{{background:var(--ink);padding:clamp(2rem,5vw,4rem) clamp(1.5rem,5vw,5rem);display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:2rem}}
.rfs-text{{font-family:'Cormorant Garamond',serif;font-size:clamp(1.2rem,2.5vw,1.8rem);font-weight:300;color:var(--white)}}
.rfs-text em{{font-style:italic;color:var(--gold3)}}
.rfs-links{{display:flex;gap:1rem;flex-wrap:wrap}}
.rfs-link{{font-size:.68rem;letter-spacing:.12em;text-transform:uppercase;color:rgba(247,244,239,.45);text-decoration:none;transition:color .2s}}
.rfs-link:hover{{color:var(--gold2)}}
.rfs-book{{display:inline-flex;align-items:center;gap:.4rem;background:var(--gold);color:var(--ink);font-size:.72rem;font-weight:500;letter-spacing:.1em;text-transform:uppercase;padding:.65rem 1.6rem;border-radius:2px;text-decoration:none;transition:background .2s}}
.rfs-book:hover{{background:var(--gold2)}}
@media(max-width:700px){{.faq-chiusa{{flex-direction:column;align-items:stretch}}.faq-azioni{{width:100%}}}}
</style>
</head>
<body>

<nav>
  <a href="index.html" class="nav-logo">
    <img class="nav-logo-img" src="img/logo.png" alt="Prà de la Fam"/>
  </a>
  <a data-i18n="{k('Home')}" href="index.html" class="nav-back">Home</a>
  <div class="lang-switcher" style="display:flex;align-items:center;gap:.1rem;margin-left:auto;margin-right:1rem"><button class="lang-btn active" onclick="setLang('it')" style="background:none;border:none;font:inherit;font-size:.62rem;letter-spacing:.08em;color:var(--steel,#4a6580);cursor:pointer;padding:2px 5px">IT</button><span style="opacity:.35">|</span><button class="lang-btn" onclick="setLang('en')" style="background:none;border:none;font:inherit;font-size:.62rem;letter-spacing:.08em;color:var(--steel,#4a6580);cursor:pointer;padding:2px 5px">EN</button><span style="opacity:.35">|</span><button class="lang-btn" onclick="setLang('de')" style="background:none;border:none;font:inherit;font-size:.62rem;letter-spacing:.08em;color:var(--steel,#4a6580);cursor:pointer;padding:2px 5px">DE</button><span style="opacity:.35">|</span><button class="lang-btn" onclick="setLang('fr')" style="background:none;border:none;font:inherit;font-size:.62rem;letter-spacing:.08em;color:var(--steel,#4a6580);cursor:pointer;padding:2px 5px">FR</button><span style="opacity:.35">|</span><button class="lang-btn" onclick="setLang('es')" style="background:none;border:none;font:inherit;font-size:.62rem;letter-spacing:.08em;color:var(--steel,#4a6580);cursor:pointer;padding:2px 5px">ES</button></div>
  <a data-i18n="{k('Prenota →')}" href="{BOOK}" target="_blank" class="nav-cta">Prenota →</a>
</nav>

<section class="faq-hero">
  <div class="faq-hbg" style="background-image:url(img/limonaia-aerea.jpg)"></div>
  <div class="faq-hov"></div>
  <div class="faq-hc">
    <p data-i18n="{k(OCCHIELLO)}" class="faq-eyebrow">{OCCHIELLO}</p>
    <h1 class="faq-h1"><span data-i18n="{k(H1A)}">{H1A}</span><br><em data-i18n="{k(H1B)}">{H1B}</em></h1>
  </div>
</section>

<div class="faq-body">
  <p data-i18n="{k(INTRO)}" class="faq-intro r">{esc(INTRO)}</p>

{CORPO}

  <div class="faq-chiusa r d1">
    <div>
      <h2 data-i18n="{k(CHIUSA_T)}" class="faq-chiusa-tit">{esc(CHIUSA_T)}</h2>
      <p data-i18n="{k(CHIUSA_P)}" class="faq-chiusa-txt">{esc(CHIUSA_P)}</p>
    </div>
    <div class="faq-azioni">
      <a data-i18n="{k('📞 Chiama: 0365 799890')}" href="tel:+390365799890" class="faq-btn">📞 Chiama: 0365 799890</a>
      <a data-i18n="{k('✉ info@alpradelafam.com')}" href="mailto:info@alpradelafam.com" class="faq-btn2">✉ info@alpradelafam.com</a>
    </div>
  </div>
</div>

<div class="room-footer-strip">
  <p data-i18n="{k('Prà de la Fam —<br><em>Lago di Garda</em>')}" class="rfs-text">Prà de la Fam —<br><em>Lago di Garda</em></p>
  <div class="rfs-links">
    <a data-i18n="{k('Camere')}" href="index.html#hotel" class="rfs-link">Camere</a>
    <a data-i18n="{k('Appartamenti')}" href="index.html#appartamenti" class="rfs-link">Appartamenti</a>
    <a data-i18n="{k('La Limonaia')}" href="index.html#limonaia" class="rfs-link">La Limonaia</a>
    <a data-i18n="{k('Contatti')}" href="index.html#contatti" class="rfs-link">Contatti</a>
    <a href="faq.html" class="rfs-link">FAQ</a>
  </div>
  <a data-i18n="{k('Prenota ora →')}" href="{BOOK}" target="_blank" class="rfs-book">Prenota ora →</a>
</div>

<script>
/* Le schede si aprono da sole se si arriva con l'ancora nella barra
   dell'indirizzo — un link mandato per mail a «/faq#d-…» deve mostrare
   la risposta, non una riga chiusa. */
(function(){{
  function apri(){{
    var id = location.hash.slice(1);
    if (!id) return;
    var el = document.getElementById(id);
    if (el && el.tagName === 'DETAILS') {{ el.open = true; el.scrollIntoView(); }}
  }}
  window.addEventListener('hashchange', apri); apri();
}})();

const io=new IntersectionObserver(entries=>{{
  entries.forEach(e=>{{ if(e.isIntersecting){{ e.target.classList.add('in'); io.unobserve(e.target); }} }});
}},{{threshold:.12,rootMargin:'0px 0px -60px 0px'}});
document.querySelectorAll('.r').forEach(el=>io.observe(el));
</script>

<script src="i18n.js" defer></script>
<script src="menu.js" defer></script>
<script src="chat.js" defer></script>
</body>
</html>
'''

(BASE / "faq.html").write_text(PAGINA, encoding="utf-8")
print("faq.html scritto:", len(PAGINA), "caratteri ·", len(faq_nodi), "domande nel JSON-LD")
