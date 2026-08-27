/* ══════════════════════════════════════════════════════════════════════
   La barra «Verifica disponibilità» — collegata al motore di prenotazione.

   PRIMA NON FACEVA NIENTE: <a href="#"> senza una riga di codice dietro.
   Chi metteva le date credeva di aver iniziato a prenotare, premeva, e la
   pagina restava ferma.

   I NOMI DEI PARAMETRI NON SONO INDOVINATI. Sono presi dal codice del
   motore stesso (secure-reservation.cloud, main.*.js) e poi verificati a
   schermo su un browser vero:

     fromDate / toDate   formato yyyy-MM-dd — la funzione interna e'
                         dateToQueryParam(d) = d.toFormat("yyyy-MM-dd"),
                         cioe' esattamente quello che <input type="date">
                         restituisce gia' in .value: nessuna conversione
     rooms               camere separate da ";", ospiti separati da ","
                         "A" = un adulto, un numero = un bambino di
                         quell'eta'.  "A,A" = una camera, due adulti
                         (massimo 5 camere: il motore taglia le altre)
     portal / lang       gia' in uso nei tasti «Prenota»

   Prova fatta: ...&fromDate=2026-10-02&toDate=2026-10-05&rooms=A,A,A
   apre il motore su «02 Ven → 05 Lun · 1 Camera 3». Anche in tedesco.

   IL BOTTONE RESTA UN LINK VERO, con un indirizzo valido gia' nell'HTML:
   funziona col tasto destro, con «apri in nuova scheda», e anche se
   questo file non venisse caricato (in quel caso porta al motore senza
   date — cioe' quello che fanno tutti gli altri tasti Prenota).
   ══════════════════════════════════════════════════════════════════════ */
(function () {
  var MOTORE = 'https://www.secure-reservation.cloud/booking-engine/?portal=pradelafam-tignale';

  var go = document.getElementById('avail-go');
  var dal = document.getElementById('avail-in');
  var al = document.getElementById('avail-out');
  var ospiti = document.getElementById('avail-guests');
  if (!go || !dal || !al) return;

  function giorno(d) {                       // Date → "2026-09-10", ora locale
    return new Date(d.getTime() - d.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
  }
  function piu(iso, n) {
    var d = new Date(iso + 'T12:00:00');
    d.setDate(d.getDate() + n);
    return giorno(d);
  }

  // Non si puo' piu' chiedere una disponibilita' per ieri: prima si poteva,
  // e il motore rispondeva com'era prevedibile.
  var oggi = giorno(new Date());
  dal.min = oggi;
  al.min = piu(oggi, 1);

  /* DATE PROPOSTE. I campi vuoti costringono a due passaggi di calendario
     prima ancora di sapere se c'e' posto. Si propone il primo fine settimana
     utile — venerdi'→domenica, il soggiorno piu' comune qui — e restano
     modificabili come prima: e' un punto di partenza, non una scelta fatta
     al posto dell'ospite. Se qualcuno ha gia' scritto qualcosa non si tocca
     niente. */
  function primoVenerdi() {
    var d = new Date(); d.setHours(12, 0, 0, 0);
    d.setDate(d.getDate() + 1);                       // mai oggi
    while (d.getDay() !== 5) d.setDate(d.getDate() + 1);
    return giorno(d);
  }
  if (!dal.value && !al.value) {
    var v = primoVenerdi();
    dal.value = v;
    al.value = piu(v, 2);                             // due notti
  }

  function aggiorna() {
    // la partenza non puo' precedere o coincidere con l'arrivo: invece di
    // rifiutare, si sposta al giorno dopo — e' quello che l'ospite intende
    if (dal.value) {
      al.min = piu(dal.value, 1);
      if (al.value && al.value <= dal.value) al.value = piu(dal.value, 1);
    }
    var u = MOTORE + '&lang=' + (document.documentElement.lang || 'it');
    if (dal.value && al.value && al.value > dal.value) {
      var n = Math.max(1, Math.min(5, parseInt(ospiti && ospiti.value, 10) || 2));
      u += '&fromDate=' + dal.value + '&toDate=' + al.value +
           '&rooms=' + new Array(n + 1).join('A,').slice(0, -1);
    }
    go.href = u;
  }

  [dal, al, ospiti].forEach(function (e) {
    if (!e) return;
    e.addEventListener('change', aggiorna);
    e.addEventListener('input', aggiorna);
  });

  go.addEventListener('click', function () {
    try {
      if (typeof gtag === 'function') gtag('event', 'cerca_disponibilita', {
        con_date: !!(dal.value && al.value), ospiti: ospiti ? ospiti.value : ''
      });
    } catch (e) {}
  });

  // il cambio lingua deve arrivare anche qui: setLang riscrive lang= su
  // tutti i link del motore, ma questo indirizzo lo ricostruiamo noi
  var vecchio = window.setLang;
  if (typeof vecchio === 'function') {
    window.setLang = function () { var r = vecchio.apply(this, arguments); aggiorna(); return r; };
  }
  aggiorna();
})();

/* ══════════════════════════════════════════════════════════════════════
   Chi arriva con il link «Come arrivare» deve TROVARE le indicazioni, non
   una riga chiusa da premere. La scheda sta al 94% della pagina: se dopo
   tutto quello scorrimento chiedesse un altro tocco sarebbe una presa in
   giro. Aperta anche quando il link e' gia' nell'indirizzo al caricamento.
   ══════════════════════════════════════════════════════════════════════ */
(function () {
  function apri() {
    if (location.hash !== '#come-arrivare') return;
    var d = document.getElementById('come-arrivare');
    if (d) { d.open = true; d.scrollIntoView({ block: 'start' }); }
  }
  window.addEventListener('hashchange', apri);
  // due volte: subito, e di nuovo a immagini caricate — altrimenti la pagina
  // cresce sotto i piedi e lo scorrimento finisce nel posto sbagliato
  window.addEventListener('load', apri);
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', apri);
  else apri();
})();

/* ══════════════════════════════════════════════════════════════════════
   IL CALENDARIO CHE SI APRE VERSO L'ALTO.

   La barra «Verifica disponibilita» e' position:fixed;bottom:0. Misurato
   sul sito pubblicato, finestra da 848px: il campo Arrivo finisce a 836,
   cioe' DODICI pixel dal fondo. Il calendario di sistema si apre sotto il
   campo che lo chiama e ne chiede circa 330: usciva dalla finestra e non
   si vedeva. Col mouse non c'era modo di scegliere una data — restava
   solo scriverla a mano.

   La posizione del calendario di sistema non e' governabile da qui, quindi
   ce n'e' uno nostro, disegnato nella pagina, ancorato SOPRA il campo.

   SOLO SU COMPUTER (hover:hover e pointer:fine). Sul telefono il
   calendario di sistema e' un pannello che copre mezzo schermo, si vede
   benissimo, ed e' fatto per il dito: sostituirlo sarebbe un
   peggioramento. Li' non cambia niente.

   L'<input type="date"> RESTA. Continua a tenere il valore in yyyy-mm-dd,
   continua a rispettare min, si compila ancora da tastiera, e cerca.js
   piu' sopra continua a leggerlo senza sapere che esistiamo: quando si
   sceglie un giorno gli si manda un evento 'change' come farebbe l'utente.
   Se questo blocco non partisse, tornerebbe il calendario di sistema.

   I nomi dei mesi e dei giorni arrivano da Intl nella lingua di
   <html lang>: nessun testo italiano nuovo nella pagina, quindi nessuna
   chiave data-i18n e nessuna traduzione da rifare. Vale per tutte e
   cinque le lingue, compreso il cambio lingua a pagina aperta.
   ══════════════════════════════════════════════════════════════════════ */
(function () {
  if (!window.matchMedia || !matchMedia('(hover:hover) and (pointer:fine)').matches) return;

  var campi = [document.getElementById('avail-in'), document.getElementById('avail-out')]
              .filter(function (c) { return c; });
  if (!campi.length) return;

  var pop = document.createElement('div');
  pop.className = 'cal-pop';
  pop.setAttribute('role', 'dialog');
  document.body.appendChild(pop);

  var attivo = null;    // il campo aperto in questo momento
  var mese = null;      // il primo del mese mostrato

  function iso(d) { return new Date(d.getTime() - d.getTimezoneOffset() * 60000).toISOString().slice(0, 10); }
  function daIso(s) {
    var p = String(s || '').split('-');
    return p.length === 3 && p[0] ? new Date(+p[0], +p[1] - 1, +p[2], 12) : null;
  }
  function primoDel(d) { return new Date(d.getFullYear(), d.getMonth(), 1, 12); }
  function lingua() { return document.documentElement.lang || 'it'; }

  function disegna() {
    var L = lingua(), i;

    // le iniziali dei giorni, da lunedi': il 1° gennaio 2024 era un lunedi'
    var gg = new Intl.DateTimeFormat(L, { weekday: 'short' }), teste = '';
    for (i = 0; i < 7; i++) {
      teste += '<div class="cal-gg">' + gg.format(new Date(2024, 0, 1 + i)).slice(0, 2) + '</div>';
    }

    var quanti = new Date(mese.getFullYear(), mese.getMonth() + 1, 0).getDate();
    var vuote = (mese.getDay() + 6) % 7;                 // lunedi' = prima colonna
    var min = attivo.min || '', max = attivo.max || '', scelto = attivo.value || '', oggi = iso(new Date());
    var celle = '';
    for (i = 0; i < vuote; i++) celle += '<div></div>';
    for (i = 1; i <= quanti; i++) {
      var g = iso(new Date(mese.getFullYear(), mese.getMonth(), i, 12));
      var no = (min && g < min) || (max && g > max);
      celle += '<button type="button" class="cal-d' + (g === scelto ? ' scelto' : '') +
               (g === oggi ? ' oggi' : '') + '" data-giorno="' + g + '"' +
               (no ? ' disabled' : '') + '>' + i + '</button>';
    }

    // niente frecce verso mesi interamente fuori dai limiti
    var finePrec = iso(new Date(mese.getFullYear(), mese.getMonth(), 0, 12));
    var inizioSucc = iso(new Date(mese.getFullYear(), mese.getMonth() + 1, 1, 12));

    pop.innerHTML =
      '<div class="cal-testa">' +
        '<button type="button" class="cal-nav" data-vai="-1"' +
          (min && finePrec < min ? ' disabled' : '') + ' aria-label="&larr;">&lsaquo;</button>' +
        '<span class="cal-mese">' +
          new Intl.DateTimeFormat(L, { month: 'long', year: 'numeric' }).format(mese) +
        '</span>' +
        '<button type="button" class="cal-nav" data-vai="1"' +
          (max && inizioSucc > max ? ' disabled' : '') + ' aria-label="&rarr;">&rsaquo;</button>' +
      '</div>' +
      '<div class="cal-griglia">' + teste + celle + '</div>';

    posiziona();   // cinque righe o sei cambiano l'altezza, e l'ancoraggio e' in basso
  }

  /* Ancorato SOPRA il campo: e' tutto il punto di questo blocco. Se un
     giorno la barra non fosse piu' in fondo e sopra non ci stesse, si
     torna sotto invece di uscire dallo schermo. */
  function posiziona() {
    var r = attivo.getBoundingClientRect(), h = pop.offsetHeight, w = pop.offsetWidth;
    pop.style.left = Math.max(8, Math.min(r.left, window.innerWidth - w - 8)) + 'px';
    pop.style.top = (r.top - h - 8 >= 8 ? r.top - h - 8
                                        : Math.min(r.bottom + 8, window.innerHeight - h - 8)) + 'px';
  }

  function apri(campo) {
    attivo = campo;
    mese = primoDel(daIso(campo.value) || daIso(campo.min) || new Date());
    pop.classList.add('aperto');
    disegna();
  }
  function chiudi() { pop.classList.remove('aperto'); attivo = null; }

  pop.addEventListener('mousedown', function (e) { e.preventDefault(); });   // il fuoco resta al campo
  pop.addEventListener('click', function (e) {
    var b = e.target.closest ? e.target.closest('button') : null;
    if (!b || !attivo) return;
    if (b.dataset.vai) {
      mese = new Date(mese.getFullYear(), mese.getMonth() + (+b.dataset.vai), 1, 12);
      disegna();
    } else if (b.dataset.giorno) {
      attivo.value = b.dataset.giorno;
      // come se l'avesse scritta l'ospite: cosi' aggiorna() rifa' il link
      attivo.dispatchEvent(new Event('change', { bubbles: true }));
      chiudi();
    }
  });

  campi.forEach(function (c) {
    /* ⚠️ LO SCUDO. Il primo tentativo era preventDefault sul mousedown del
       campo: NON BASTA. Chrome apre il calendario di sistema al clic, e il
       clic parte lo stesso. Si vedevano due calendari insieme — il nostro
       verso l'alto e quello bianco di sistema verso il basso, mezzo fuori
       dallo schermo. L'unico fermo certo e' non far arrivare il clic al
       campo: un velo trasparente sopra la casella se lo prende tutto.
       Il fuoco lo diamo noi, cosi' la data si scrive ancora da tastiera. */
    var casella = c.parentNode;
    casella.classList.add('con-scudo');
    var scudo = document.createElement('div');
    scudo.className = 'cal-scudo';
    scudo.setAttribute('aria-hidden', 'true');
    casella.appendChild(scudo);
    scudo.addEventListener('mousedown', function (e) {
      e.preventDefault();
      var eraAperto = (attivo === c);
      c.focus();
      if (eraAperto) chiudi(); else apri(c);
    });
    c.addEventListener('keydown', function (e) {
      if (e.key === 'F4' || (e.altKey && (e.key === 'ArrowDown' || e.key === 'ArrowUp'))) {
        e.preventDefault();
        apri(c);
      }
    });
    // se si esce dal campo con Tab il calendario non deve restare appeso
    c.addEventListener('blur', function () { setTimeout(function () {
      if (attivo === c && document.activeElement !== c) chiudi();
    }, 0); });
  });

  document.addEventListener('mousedown', function (e) {
    // gli scudi si arrangiano da soli (aprono, chiudono, passano da un campo
    // all'altro): se chiudessimo anche di qui riaprirebbero subito dopo
    var suUnoScudo = e.target.closest && e.target.closest('.cal-scudo');
    if (attivo && !pop.contains(e.target) && !suUnoScudo) chiudi();
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && attivo) chiudi(); });
  window.addEventListener('resize', function () { if (attivo) posiziona(); });
})();
