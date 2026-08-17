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
