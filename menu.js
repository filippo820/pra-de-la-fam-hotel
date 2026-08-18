/* ══════════════════════════════════════════════════════════════════════
   Il menu del telefono.

   COSA MANCAVA. Sotto i 900px il menu (otto voci) è nascosto, e non c'era
   nessun pulsante per riaprirlo: sul telefono la barra aveva solo il
   marchio e «Prenota». Sotto i 560px sparivano anche le cinque lingue —
   un ospite tedesco col telefono in mano poteva cambiare lingua solo
   scorrendo fino in fondo a una pagina di quindicimila pixel.

   IL PANNELLO SI COSTRUISCE ALL'APERTURA leggendo i link veri della barra,
   non copiandoli una volta per tutte. Cosi' e' sempre nella lingua giusta
   senza dipendere dall'ordine in cui partono gli script, e se domani una
   voce cambia nell'HTML cambia anche qui.
   ══════════════════════════════════════════════════════════════════════ */
(function () {
  var nav = document.getElementById('nav') || document.querySelector('nav');
  if (!nav) return;
  /* Da dove vengono le voci: in home dal menu nascosto, nelle pagine di
     camere e appartamenti dalla striscia in fondo — che ha gli stessi
     quattro link. Cosi' il pannello non inventa niente. */
  var fonte = nav.querySelector('.nav-center') ? '#nav .nav-center a' : '.rfs-links a';
  if (!document.querySelector(fonte)) return;

  var L = ['it', 'en', 'de', 'fr', 'es'];
  var T = {
    apri:   ['Menu', 'Menu', 'Menü', 'Menu', 'Menú'],
    chiudi: ['Chiudi il menu', 'Close menu', 'Menü schließen', 'Fermer le menu', 'Cerrar el menú'],
    lingua: ['Lingua', 'Language', 'Sprache', 'Langue', 'Idioma']
  };
  function d(k) { var i = L.indexOf(document.documentElement.lang || 'it'); return T[k][i < 0 ? 0 : i]; }

  var css = document.createElement('style');
  css.textContent = [
    '#pdlf-menu-btn{display:none;background:none;border:0;padding:0;margin-left:auto;margin-right:.7rem;',
    'width:40px;height:40px;flex-direction:column;align-items:center;justify-content:center;',
    'cursor:pointer;color:var(--ink);flex-shrink:0}',
    '#pdlf-menu-btn span{display:block;width:20px;height:1.6px;background:currentColor;border-radius:2px;',
    'transition:transform .24s,opacity .18s}',
    '#pdlf-menu-btn span+span{margin-top:5px}',
    'body.menu-aperto #pdlf-menu-btn span:nth-child(1){transform:translateY(6.6px) rotate(45deg)}',
    'body.menu-aperto #pdlf-menu-btn span:nth-child(2){opacity:0}',
    'body.menu-aperto #pdlf-menu-btn span:nth-child(3){transform:translateY(-6.6px) rotate(-45deg)}',
    '#pdlf-menu{position:fixed;inset:0;height:100dvh;max-height:none;min-height:0;box-sizing:border-box;',
    'z-index:499;background:var(--bone,#f7f4ef);margin:0;',
    'display:none;flex-direction:column;padding:88px 0 28px;overflow-y:auto;overscroll-behavior:contain}',
    '#pdlf-menu.aperto{display:flex}',
    '#pdlf-menu a.voce{display:block;padding:.85rem clamp(1.5rem,6vw,2.5rem);text-decoration:none;',
    "font-family:'Cormorant Garamond',serif;font-size:1.55rem;font-weight:300;color:var(--ink,#0b1520);",
    'border-bottom:1px solid rgba(11,21,32,.07)}',
    '#pdlf-menu a.voce:active{background:rgba(11,21,32,.04)}',
    '.pm-lingue{padding:1.5rem clamp(1.5rem,6vw,2.5rem) .4rem}',
    '.pm-tit{font-size:.7rem;letter-spacing:.18em;text-transform:uppercase;color:var(--gold-testo,#846934);margin-bottom:.9rem}',
    '.pm-riga{display:flex;flex-wrap:wrap;gap:.5rem}',
    '.pm-l{font:inherit;font-size:.8rem;letter-spacing:.1em;padding:.55rem 1rem;cursor:pointer;',
    'background:none;border:1px solid rgba(11,21,32,.18);color:var(--ink,#0b1520);border-radius:2px}',
    '.pm-l[aria-current="true"]{background:var(--ink,#0b1520);color:var(--bone,#f7f4ef);border-color:var(--ink,#0b1520)}',
    '.pm-contatti{padding:1.6rem clamp(1.5rem,6vw,2.5rem) 0;display:flex;flex-direction:column;gap:.55rem}',
    '.pm-contatti a{color:var(--gold-testo,#846934);text-decoration:none;font-size:.95rem}',
    '@media(max-width:1300px){#pdlf-menu-btn{display:flex}}',
    /* Nelle sottopagine le lingue stanno in linea e rubano lo spazio al
       ritorno indietro: sotto i 700px passano nel pannello.
       !important perche' quel div ha lo style scritto SUL TAG, che batte
       qualunque regola del foglio — trappola gia' incontrata due volte. */
    '@media(max-width:700px){nav .lang-switcher{display:none !important}}',
    'body.menu-aperto{overflow:hidden}'
  ].join('');
  document.head.appendChild(css);

  var btn = document.createElement('button');
  btn.id = 'pdlf-menu-btn'; btn.type = 'button';
  btn.setAttribute('aria-expanded', 'false');
  btn.setAttribute('aria-controls', 'pdlf-menu');
  btn.innerHTML = '<span></span><span></span><span></span>';
  var cta = nav.querySelector('.nav-right') || nav.lastElementChild;
  nav.insertBefore(btn, cta);

  /* UN DIV, NON UN <nav>. Nel sito c'e' una regola sull'ELEMENTO — 
     nav{position:fixed;height:68px} — e un pannello a tutto schermo scritto
     come <nav> se la prende: la prima versione era alta 117px invece di 844,
     cioe' solo il suo stesso margine interno. E' la stessa trappola del
     pannello della chat, che era un <section> e si prendeva
     section{padding:120px}. L'altezza e' dichiarata, non lasciata a inset. */
  var pan = document.createElement('div');
  pan.id = 'pdlf-menu';
  pan.setAttribute('role', 'navigation');
  pan.setAttribute('aria-label', 'Menu');
  document.body.appendChild(pan);

  function riempi() {
    var voci = [...document.querySelectorAll(fonte)].map(function (a) {
      return '<a class="voce" href="' + a.getAttribute('href') + '">' +
             a.textContent.trim().replace(/[<>&]/g, '') + '</a>';
    }).join('');
    var attuale = document.documentElement.lang || 'it';
    var lingue = L.map(function (l) {
      return '<button type="button" class="pm-l" data-l="' + l + '"' +
             (l === attuale ? ' aria-current="true"' : '') + '>' + l.toUpperCase() + '</button>';
    }).join('');
    pan.innerHTML = voci +
      '<div class="pm-lingue"><p class="pm-tit">' + d('lingua') + '</p><div class="pm-riga">' + lingue + '</div></div>' +
      '<div class="pm-contatti"><a href="tel:+390365799890">(+39) 0365 799890</a>' +
      '<a href="mailto:info@alpradelafam.com">info@alpradelafam.com</a></div>';
  }

  function apri() {
    riempi();
    pan.classList.add('aperto');
    document.body.classList.add('menu-aperto');
    btn.setAttribute('aria-expanded', 'true');
    btn.setAttribute('aria-label', d('chiudi'));
  }
  function chiudi() {
    pan.classList.remove('aperto');
    document.body.classList.remove('menu-aperto');
    btn.setAttribute('aria-expanded', 'false');
    btn.setAttribute('aria-label', d('apri'));
  }
  btn.setAttribute('aria-label', d('apri'));

  btn.addEventListener('click', function () {
    pan.classList.contains('aperto') ? chiudi() : apri();
  });
  pan.addEventListener('click', function (e) {
    var l = e.target.closest('.pm-l');
    if (l) {
      // la lingua si cambia e il menu resta aperto: si vede il cambio,
      // e chi ha sbagliato lingua non deve riaprire tutto
      if (typeof window.setLang === 'function') window.setLang(l.dataset.l);
      riempi();
      return;
    }
    if (e.target.closest('a')) chiudi();     // scelta una voce, via il pannello
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && pan.classList.contains('aperto')) { chiudi(); btn.focus(); }
  });
  // tornando a schermo grande il menu vero riappare: il pannello non serve piu'
  window.addEventListener('resize', function () {
    if (window.innerWidth > 1300 && pan.classList.contains('aperto')) chiudi();
  });
})();
