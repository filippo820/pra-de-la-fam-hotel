#!/bin/bash
# Prova un'anteprima Netlify (Deploy Preview) PRIMA di pubblicare la fase SEO.
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
prova "/de_DE/clementina/ → 301 appartamento-clementina" "[[ \"\$(dove /de_DE/clementina/)\" == */appartamento-clementina ]]"
prova "/it_IT/xyz → 301 /" "[ \"\$(stato /it_IT/xyz)\" = 301 ]"
prova "/domande-frequenti → 301 /faq" "[[ \"\$(dove /domande-frequenti)\" == */faq ]]"
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
