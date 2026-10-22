#!/usr/bin/env python3
"""Server di prova in locale, che si comporta come Netlify dove conta.

PERCHE' NON BASTA `python3 -m http.server`. Le pagine si chiamano senza .html
(/faq, /de/camera-doppia) e un indirizzo che non esiste deve dare la 404 con
stato 404 — nella sua lingua sotto /en/ /de/ /fr/ /es/, come dicono le regole
«/de/*  /de/404.html  404» di _redirects. http.server non fa nessuna delle due
cose, e controlla_seo.mjs e kb.py fallirebbero su tutte le sottopagine.

NON prova i redirect di _redirects (i 301 dalle vecchie URL, i 301! dai .html):
quelli li applica solo Netlify, e si provano su una Deploy Preview con
strumenti/prova_anteprima.sh.

Uso:  python3 strumenti/servi.py      → http://localhost:8911
"""
import http.server, io, os, pathlib, re, sys

R = str(pathlib.Path(__file__).resolve().parent.parent)
PORTA = int(sys.argv[1]) if len(sys.argv) > 1 else 8911


class Netlify(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=R, **k)

    def log_message(self, *a):
        pass

    def send_head(self):
        p = self.path.split("?")[0].split("#")[0]
        dove = os.path.join(R, p.lstrip("/"))
        if p != "/" and not p.endswith("/") and not os.path.exists(dove) and os.path.exists(dove + ".html"):
            self.path = p + ".html"
        elif not os.path.exists(dove) or (p.endswith("/") and not os.path.exists(os.path.join(dove, "index.html"))):
            m = re.match(r"/(en|de|fr|es)/", p)
            corpo = open(os.path.join(R, (m.group(1) + "/" if m else "") + "404.html"), "rb").read()
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(corpo)))
            self.end_headers()
            return io.BytesIO(corpo)
        return super().send_head()

    def copyfile(self, src, dst):
        try:
            super().copyfile(src, dst)
        except (BrokenPipeError, ConnectionResetError):
            pass      # il browser ha chiuso prima della fine: normale


if __name__ == "__main__":
    print(f"  http://localhost:{PORTA}  (Ctrl-C per fermare)")
    http.server.ThreadingHTTPServer(("127.0.0.1", PORTA), Netlify).serve_forever()
