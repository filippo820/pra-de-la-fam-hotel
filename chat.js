/* ══════════════════════════════════════════════════════════════════════
   Assistente del Prà — la parte che si vede.

   Nel sito c'era un pannello a meta': l'HTML era troncato (mancava il
   pulsante e il <div> che apre il riquadro, e cinque </div> restavano
   spaiati) e le funzioni toggleChat/chatKey/sendChat/autoResize non
   esistevano. Qui e' rifatto intero.

   LE ETICHETTE STANNO QUI, non nel dizionario del sito: sono di questo
   componente e cosi' si aggiorna da solo senza rigenerare i18n.js.

   IL TESTO DELLE RISPOSTE VA IN textContent, MAI IN innerHTML: la risposta
   la scrive un modello, e non deve poter iniettare markup nella pagina.
   ══════════════════════════════════════════════════════════════════════ */
(function () {
  var API = '/api/chat';
  var L = ['it', 'en', 'de', 'fr', 'es'];
  var T = {
    titolo:  ['Assistente Prà de la Fam', 'Prà de la Fam assistant', 'Prà de la Fam Assistent', 'Assistant Prà de la Fam', 'Asistente Prà de la Fam'],
    apri:    ['Fai una domanda', 'Ask a question', 'Eine Frage stellen', 'Poser une question', 'Hacer una pregunta'],
    chiudi:  ['Chiudi', 'Close', 'Schließen', 'Fermer', 'Cerrar'],
    invia:   ['Invia', 'Send', 'Senden', 'Envoyer', 'Enviar'],
    scrivi:  ['Scrivi la tua domanda…', 'Type your question…', 'Ihre Frage…', 'Écrivez votre question…', 'Escribe tu pregunta…'],
    benv:    ['Buongiorno. Chiedimi quello che vuoi sapere sul Prà: le camere, gli appartamenti, la limonaia, cosa si fa qui intorno.',
              'Hello. Ask me anything about Prà: the rooms, the apartments, the lemon house, what to do nearby.',
              'Guten Tag. Fragen Sie mich alles über das Prà: Zimmer, Apartments, die Limonaia, was man hier unternehmen kann.',
              'Bonjour. Demandez-moi ce que vous voulez savoir sur le Prà : les chambres, les appartements, la limonaia, que faire aux alentours.',
              'Buenos días. Pregúntame lo que quieras sobre el Prà: las habitaciones, los apartamentos, la limonaia, qué hacer por aquí.'],
    nota:    ['Risponde in base a quello che c’è sul sito. Per disponibilità e prezzi: il tasto Prenota, o +39 0365 799890.',
              'It answers from what’s on this site. For availability and rates: the Book button, or +39 0365 799890.',
              'Antwortet anhand dessen, was auf dieser Seite steht. Für Verfügbarkeit und Preise: Buchen-Taste oder +39 0365 799890.',
              'Il répond à partir de ce qui est sur ce site. Pour les disponibilités et les tarifs : le bouton Réserver, ou +39 0365 799890.',
              'Responde según lo que hay en este sitio. Para disponibilidad y precios: el botón Reservar, o +39 0365 799890.'],
    err:     ['Non riesco a rispondere adesso. Scrivici a info@alpradelafam.com.',
              'I can’t answer right now. Write to info@alpradelafam.com.',
              'Ich kann gerade nicht antworten. Schreiben Sie an info@alpradelafam.com.',
              'Je ne peux pas répondre maintenant. Écrivez à info@alpradelafam.com.',
              'No puedo responder ahora. Escríbenos a info@alpradelafam.com.'],
    sp1:     ['Che camere avete?', 'What rooms do you have?', 'Welche Zimmer haben Sie?', 'Quelles chambres avez-vous ?', '¿Qué habitaciones tenéis?'],
    sp2:     ['Cosa si fa qui intorno?', 'What is there to do nearby?', 'Was kann man hier unternehmen?', 'Que faire aux alentours ?', '¿Qué se puede hacer cerca?'],
    sp3:     ['Si può visitare la limonaia?', 'Can we visit the lemon house?', 'Kann man die Limonaia besichtigen?', 'Peut-on visiter la limonaia ?', '¿Se puede visitar la limonaia?']
  };
  function idx() { var i = L.indexOf(document.documentElement.lang || 'it'); return i < 0 ? 0 : i; }
  function d(k) { return T[k][idx()]; }

  var css = document.createElement('style');
  css.textContent = [
    // il pulsante non deve finire sopra la barra «Verifica disponibilita»:
    // --barra la dichiara la home, altrove var() ripiega su 0
    '#pdlf-chat-btn{position:fixed;right:24px;bottom:calc(24px + var(--barra, 0px));z-index:400;width:56px;height:56px;border-radius:50%;',
    'display:flex;align-items:center;justify-content:center;cursor:pointer;border:none;',
    // ⚠️ L'ANELLO CHIARO NON E' UN ORNAMENTO. Il cerchio scuro su una foto
    // scura si staccava solo 1.84:1 — sotto il minimo di 3:1 per un comando —
    // e sull'apertura spariva. Con corpo scuro E anello chiaro almeno uno dei
    // due stacca sempre: l'anello sui fondi scuri, il corpo su quelli chiari.
    'background:#0b1520;color:#f0d898;border:2.5px solid rgba(247,244,239,.94);',
    'box-shadow:0 6px 22px rgba(11,21,32,.5);transition:transform .18s}',
    '#pdlf-chat-btn:hover{transform:translateY(-2px)}',
    // padding:0 e' una difesa, non un vezzo: nel sito c'e' section{padding:120px 32px}
    // e un riquadro con 120px di vuoto in cima e' gia' successo una volta
    '#pdlf-chat{padding:0;margin:0;position:fixed;right:24px;bottom:calc(96px + var(--barra, 0px));z-index:401;width:376px;max-width:calc(100vw - 32px);',
    'height:auto;min-height:270px;max-height:calc(100vh - 150px);display:none;flex-direction:column;',
    'background:#f7f4ef;border-radius:4px;box-shadow:0 24px 70px rgba(11,21,32,.34);overflow:hidden;',
    'font-family:\'DM Sans\',\'Josefin Sans\',system-ui,sans-serif}',
    '#pdlf-chat.aperta{display:flex}',
    '.pc-testa{display:flex;align-items:center;justify-content:space-between;padding:15px 18px;',
    'background:#0b1520;color:#f7f4ef;flex-shrink:0}',
    '.pc-testa strong{font-family:\'Cormorant Garamond\',Georgia,serif;font-weight:400;font-size:1.05rem}',
    '.pc-x{background:none;border:none;color:rgba(247,244,239,.65);cursor:pointer;font-size:1.05rem;padding:2px 6px;line-height:1}',
    '.pc-x:hover{color:#f7f4ef}',
    '.pc-corpo{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:11px}',
    '.pc-m{max-width:86%;font-size:.9rem;line-height:1.62;padding:10px 13px;border-radius:3px;white-space:pre-wrap;overflow-wrap:anywhere}',
    '.pc-lui{align-self:flex-start;background:#fff;color:#243447;box-shadow:0 1px 4px rgba(11,21,32,.07)}',
    '.pc-te{align-self:flex-end;background:#0b1520;color:#f7f4ef}',
    '.pc-att{align-self:flex-start;display:flex;gap:5px;padding:13px}',
    '.pc-att i{width:6px;height:6px;border-radius:50%;background:#b8934a;opacity:.4;animation:pcP 1.1s infinite}',
    '.pc-att i:nth-child(2){animation-delay:.18s}.pc-att i:nth-child(3){animation-delay:.36s}',
    '@keyframes pcP{0%,60%,100%{opacity:.25;transform:translateY(0)}30%{opacity:1;transform:translateY(-3px)}}',
    '.pc-sp{display:flex;flex-wrap:wrap;gap:7px;padding:0 16px 12px}',
    '.pc-spb{font:inherit;font-size:.74rem;color:#b8934a;background:none;border:1px solid rgba(184,147,74,.4);',
    'padding:6px 11px;border-radius:3px;cursor:pointer}',
    '.pc-spb:hover{background:rgba(184,147,74,.1)}',
    '.pc-piede{border-top:1px solid rgba(11,21,32,.09);padding:11px 13px 9px;flex-shrink:0}',
    '.pc-form{display:flex;gap:7px;align-items:center}',
    '.pc-in{flex:1;font:inherit;font-size:.92rem;color:#0b1520;background:#fff;border:1px solid rgba(11,21,32,.14);',
    'border-radius:3px;padding:10px 11px;outline:none;min-width:0;resize:none;max-height:88px;line-height:1.45}',
    '.pc-in:focus{border-color:rgba(184,147,74,.65)}',
    '.pc-inv{background:#b8934a;border:none;color:#0b1520;cursor:pointer;width:40px;height:40px;border-radius:3px;',
    'display:flex;align-items:center;justify-content:center;flex-shrink:0}',
    '.pc-inv:disabled{opacity:.4;cursor:default}',
    '.pc-nota{font-size:.66rem;line-height:1.5;color:rgba(11,21,32,.42);margin-top:8px;text-align:center}',
    '@media(max-width:760px){#pdlf-chat{right:12px;left:12px;bottom:calc(88px + var(--barra, 0px));width:auto;max-width:none;max-height:calc(100vh - 150px)}',
    '#pdlf-chat-btn{right:16px;bottom:calc(16px + var(--barra, 0px));width:50px;height:50px}}'
  ].join('');
  document.head.appendChild(css);

  var wrap = document.createElement('div');
  wrap.innerHTML =
    '<button id="pdlf-chat-btn" type="button" aria-expanded="false">' +
      '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" ' +
      'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
      '<path d="M20.5 15.5a2 2 0 0 1-2 2H8l-4.5 3.5v-15a2 2 0 0 1 2-2h13a2 2 0 0 1 2 2z"/>' +
      '<path d="M8 9h8"/><path d="M8 12.5h5"/></svg></button>' +
    '<section id="pdlf-chat" role="dialog" aria-labelledby="pc-tit">' +
      '<div class="pc-testa"><strong id="pc-tit"></strong><button class="pc-x" type="button">&#10005;</button></div>' +
      '<div class="pc-corpo" aria-live="polite"></div>' +
      '<div class="pc-sp"></div>' +
      '<div class="pc-piede"><form class="pc-form">' +
        '<textarea class="pc-in" rows="1" maxlength="500"></textarea>' +
        '<button class="pc-inv" type="submit">' +
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">' +
        '<path d="M2 21l21-9L2 3v7l15 2-15 2v7z"/></svg></button>' +
      '</form><p class="pc-nota"></p></div>' +
    '</section>';
  document.body.appendChild(wrap);

  var btn = document.getElementById('pdlf-chat-btn'),
      pan = document.getElementById('pdlf-chat'),
      corpo = pan.querySelector('.pc-corpo'),
      spunti = pan.querySelector('.pc-sp'),
      form = pan.querySelector('.pc-form'),
      input = pan.querySelector('.pc-in'),
      inv = pan.querySelector('.pc-inv');

  var storia = [], occupato = false;

  function etichette() {
    document.getElementById('pc-tit').textContent = d('titolo');
    input.placeholder = d('scrivi');
    btn.setAttribute('aria-label', d('apri'));
    inv.setAttribute('aria-label', d('invia'));
    pan.querySelector('.pc-x').setAttribute('aria-label', d('chiudi'));
    pan.querySelector('.pc-nota').textContent = d('nota');
    spunti.innerHTML = '';
    ['sp1', 'sp2', 'sp3'].forEach(function (k) {
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'pc-spb'; b.textContent = d(k);
      spunti.appendChild(b);
    });
    // il saluto e' un'etichetta, non un messaggio scambiato: finche' non si
    // e' chiesto nulla segue la lingua. I messaggi veri no — riscrivere
    // quello che qualcuno ha gia' letto sarebbe peggio.
    if (!storia.length && corpo.firstChild) corpo.firstChild.textContent = d('benv');
  }

  function riga(cls, testo) {
    var e = document.createElement('div');
    e.className = 'pc-m ' + cls;
    e.textContent = testo;              // testo, MAI innerHTML
    corpo.appendChild(e);
    corpo.scrollTop = corpo.scrollHeight;
    return e;
  }

  function chiedi(testo) {
    testo = (testo || '').trim();
    if (occupato || !testo) return;
    occupato = true; inv.disabled = true; spunti.style.display = 'none';
    riga('pc-te', testo);
    storia.push({ ruolo: 'persona', testo: testo });
    var att = document.createElement('div');
    att.className = 'pc-att'; att.innerHTML = '<i></i><i></i><i></i>';
    corpo.appendChild(att); corpo.scrollTop = corpo.scrollHeight;

    fetch(API, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ lingua: document.documentElement.lang || 'it', messaggi: storia.slice(-12) })
    })
      .then(function (r) { return r.json(); })
      .then(function (x) {
        att.remove();
        var t = (x && x.risposta) ? x.risposta : d('err');
        riga('pc-lui', t);
        storia.push({ ruolo: 'assistente', testo: t });
        try { if (typeof gtag === 'function') gtag('event', 'assistente_risposta', {}); } catch (e) {}
      })
      .catch(function () { att.remove(); riga('pc-lui', d('err')); })
      .then(function () { occupato = false; inv.disabled = false; input.focus(); });
  }

  function apri() {
    pan.classList.add('aperta');
    btn.setAttribute('aria-expanded', 'true');
    if (!corpo.children.length) riga('pc-lui', d('benv'));
    try { if (typeof gtag === 'function') gtag('event', 'apre_assistente', {}); } catch (e) {}
    setTimeout(function () { input.focus(); }, 60);
  }
  function chiudi() { pan.classList.remove('aperta'); btn.setAttribute('aria-expanded', 'false'); }

  btn.addEventListener('click', function () { pan.classList.contains('aperta') ? chiudi() : apri(); });
  pan.querySelector('.pc-x').addEventListener('click', chiudi);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && pan.classList.contains('aperta')) { chiudi(); btn.focus(); }
  });
  form.addEventListener('submit', function (e) { e.preventDefault(); var v = input.value; input.value = ''; input.style.height = 'auto'; chiedi(v); });
  input.addEventListener('input', function () { this.style.height = 'auto'; this.style.height = Math.min(this.scrollHeight, 88) + 'px'; });
  input.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); form.dispatchEvent(new Event('submit')); }
  });
  spunti.addEventListener('click', function (e) {
    var b = e.target.closest('.pc-spb'); if (b) chiedi(b.textContent);
  });

  var vecchio = window.setLang;
  if (typeof vecchio === 'function') {
    window.setLang = function () { var r = vecchio.apply(this, arguments); etichette(); return r; };
  }
  etichette();
})();
