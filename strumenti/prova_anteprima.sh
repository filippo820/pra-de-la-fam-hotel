#!/bin/bash
# Prova un'anteprima Netlify (Deploy Preview) PRIMA di pubblicare la fase SEO
# (dalla fase 2: anche le pagine per lingua e le vecchie URL per lingua).
# Le cose che in locale non si possono provare: i redirect «301!», la 404
# servita da Netlify, le intestazioni di cache, e che Netlify non riscriva
# l'HTML rompendo il JSON-LD.
#
# Uso:  bash strumenti/prova_anteprima.sh https://deploy-preview-12--pradelafam.netlify.app
A="${1%/}"; [ -z "$A" ] && { echo "manca l'indirizzo dell'anteprima"; exit 2; }
guai=0
prova() {  # descrizione, comando che deve dare «vero»
  if eval "$2" >/dev/null 2>&1; then echo "  ✓ $1"; else echo "  ✗ $1"; guai=$((guai+1)); fi
}
stato() { curl -s -o /dev/null -w "%{http_code}" "$A$1"; }
dove()  { curl -s -o /dev/null -w "%{redirect_url}" "$A$1"; }

echo "Pagine senza .html: 200, nessun giro"
for p in / /faq /camera-doppia /appartamento-pomelo /cookie /privacy; do
  prova "$p → 200" "[ \"\$(stato $p)\" = 200 ]"
done
echo "Pagine con .html: un solo 301 verso l'indirizzo pulito"
for p in faq camera-doppia appartamento-pomelo cookie; do
  prova "/$p.html → 301 /$p" "[ \"\$(stato /$p.html)\" = 301 ] && [[ \"\$(dove /$p.html)\" == */$p ]]"
done
prova "/index.html → 301 /" "[ \"\$(stato /index.html)\" = 301 ] && [[ \"\$(dove /index.html)\" == */ ]]"
prova "nessun giro: /faq.html arriva a 200 in un passo" "[ \"\$(curl -sL -o /dev/null -w '%{http_code} %{num_redirects}' $A/faq.html)\" = '200 1' ]"
echo "Vecchie URL (regole esistenti)"
prova "/hotel/ → 301" "[ \"\$(stato /hotel/)\" = 301 ]"
prova "/it_IT/clementina/ → 301 /appartamento-clementina" "[[ \"\$(dove /it_IT/clementina/)\" == */appartamento-clementina && \"\$(dove /it_IT/clementina/)\" != */de/* ]]"
prova "/it_IT/xyz → 301 /" "[ \"\$(stato /it_IT/xyz)\" = 301 ]"
prova "/domande-frequenti → 301 /faq" "[[ \"\$(dove /domande-frequenti)\" == */faq ]]"
echo "Le lingue: /en/ /de/ /fr/ /es/"
for l in en de fr es; do
  prova "/$l/ → 200, html lang=$l" "[ \"\$(stato /$l/)\" = 200 ] && curl -s $A/$l/ | grep -q '<html lang=\"$l\">'"
  prova "/$l/faq → 200 (non mandata all'italiano)" "[ \"\$(curl -s -o /dev/null -w '%{http_code} %{num_redirects}' $A/$l/faq)\" = '200 0' ]"
  prova "/$l/camera-doppia → 200" "[ \"\$(stato /$l/camera-doppia)\" = 200 ]"
  prova "/$l/camera-doppia.html → 301 /$l/camera-doppia, un passo" "[ \"\$(stato /$l/camera-doppia.html)\" = 301 ] && [[ \"\$(dove /$l/camera-doppia.html)\" == */$l/camera-doppia ]] && [ \"\$(curl -sL -o /dev/null -w '%{http_code} %{num_redirects}' $A/$l/camera-doppia.html)\" = '200 1' ]"
  prova "/$l/index.html → 301 /$l/" "[ \"\$(stato /$l/index.html)\" = 301 ] && [[ \"\$(dove /$l/index.html)\" == */$l/ ]]"
  prova "/$l/faq/ → 301 /$l/faq" "[[ \"\$(dove /$l/faq/)\" == */$l/faq ]]"
  prova "/$l/pagina-inesistente → 404 nella lingua" "[ \"\$(stato /$l/pagina-inesistente)\" = 404 ] && curl -s $A/$l/pagina-inesistente | grep -q '<html lang=\"$l\">'"
  prova "/$l/404.html con X-Robots-Tag noindex" "curl -sI $A/$l/404.html | grep -qi 'x-robots-tag: noindex'"
done
prova "hreflang serviti: /de/faq dichiara /en/faq e x-default" "curl -s $A/de/faq | grep -q 'hreflang=\"en\" href=\"https://alpradelafam.com/en/faq\"' && curl -s $A/de/faq | grep -q 'hreflang=\"x-default\" href=\"https://alpradelafam.com/faq\"'"
prova "canonical di /fr/cookie è /fr/cookie" "curl -s $A/fr/cookie | grep -q 'rel=\"canonical\" href=\"https://alpradelafam.com/fr/cookie\"'"
prova "il selettore di /es/faq porta a /de/faq" "curl -s $A/es/faq | grep -q 'href=\"/de/faq\" hreflang=\"de\"'"
prova "nessuna pagina carica più i18n.js" "! curl -s $A/ | grep -q i18n.js && ! curl -s $A/en/ | grep -q i18n.js"
prova "sitemap con /es/faq e le sue alternative" "curl -s $A/sitemap.xml | grep -q '<loc>https://alpradelafam.com/es/faq</loc>' && curl -s $A/sitemap.xml | grep -q 'xhtml:link'"
echo "Vecchie URL nella lingua giusta, in un passo"
uno() { curl -sL -o /dev/null -w '%{http_code} %{num_redirects}' "$A$1"; }
prova "/de_DE/clementina/ → /de/appartamento-clementina" "[[ \"\$(dove /de_DE/clementina/)\" == */de/appartamento-clementina ]] && [ \"\$(uno /de_DE/clementina/)\" = '200 1' ]"
prova "/en_GB/pomelo → /en/appartamento-pomelo" "[[ \"\$(dove /en_GB/pomelo)\" == */en/appartamento-pomelo ]] && [ \"\$(uno /en_GB/pomelo)\" = '200 1' ]"
prova "/fr_FR/hotel/ → /fr/#hotel" "[[ \"\$(dove /fr_FR/hotel/)\" == */fr/#hotel ]]"
prova "/en_US/cookie-policy/ → /en/cookie" "[[ \"\$(dove /en_US/cookie-policy/)\" == */en/cookie ]]"
prova "/de_DE/pagina-sparita/ → /de/ (non la 404)" "[[ \"\$(dove /de_DE/pagina-sparita/)\" == */de/ ]] && [ \"\$(uno /de_DE/pagina-sparita/)\" = '200 1' ]"
prova "/es_ES/qualcosa → /es/" "[[ \"\$(dove /es_ES/qualcosa)\" == */es/ ]]"
prova "/wp/kumquat/ → /appartamento-kumquat (italiano)" "[[ \"\$(dove /wp/kumquat/)\" == */appartamento-kumquat && \"\$(dove /wp/kumquat/)\" != */en/* ]]"
echo "404"
prova "/pagina-inesistente → 404 con la nostra pagina" "[ \"\$(stato /pagina-inesistente)\" = 404 ] && curl -s $A/pagina-inesistente | grep -q 'Questa pagina'"
prova "404 profonda: il logo si carica" "[ \"\$(stato /img/logo.png)\" = 200 ]"
prova "404 con X-Robots-Tag noindex" "curl -sI $A/404.html | grep -qi 'x-robots-tag: noindex'"
echo "Funzione dell'assistente non intercettata"
prova "/api/chat risponde la funzione (non 404)" "[ \"\$(stato /api/chat)\" != 404 ]"
echo "Font"
prova "/fonts/caratteri-v1.css → 200" "[ \"\$(stato /fonts/caratteri-v1.css)\" = 200 ]"
prova "woff2 → 200 e cache immutable" "curl -sI $A/fonts/dm-sans-v17-normal-latin.woff2 | grep -qi 'immutable'"
prova "nessun fonts.googleapis.com nella home" "! curl -s $A/ | grep -q fonts.googleapis.com"
echo "Immagini e dati strutturati"
prova "/img/hero-bg.webp → 200" "[ \"\$(stato /img/hero-bg.webp)\" = 200 ]"
prova "JSON-LD della home ancora valido dopo il deploy" "curl -s $A/ | python3 -c 'import sys,re,json; [json.loads(b) for b in re.findall(r\"<script type=\\\"application/ld\\+json\\\">(.*?)</script>\", sys.stdin.read(), re.S)]'"
prova "JSON-LD di una camera valido" "curl -s $A/camera-tripla | python3 -c 'import sys,re,json; b=re.findall(r\"<script type=\\\"application/ld\\+json\\\">(.*?)</script>\", sys.stdin.read(), re.S); assert b; [json.loads(x) for x in b]'"
echo
[ $guai = 0 ] && echo "  ✓ anteprima in regola" || echo "  ✗ $guai problemi: non pubblicare"
exit $guai
