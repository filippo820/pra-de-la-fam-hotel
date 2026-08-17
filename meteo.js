/* ══════════════════════════════════════════════════════════════════════
   Meteo del Prà — oggi e i quattro giorni dopo.

   FONTE: Open-Meteo. Gratuita, senza registrazione e senza chiave da
   nascondere: si puo' chiamare direttamente dal browser, quindi non serve
   nessun pezzo di server.

   ⚠️ LE COORDINATE SONO LA COSA PIU' IMPORTANTE DI QUESTO FILE.
   Tignale paese sta in montagna, il Pra' sta sul lago. Chiedendo il meteo
   per «Tignale» l'API restituisce un punto a 1147 m di quota: alla prova
   dava 21,6° mentre sulla riva erano 28,0°. Sei gradi e mezzo di
   differenza — un meteo cosi' sarebbe peggio di nessun meteo. Queste
   coordinate sono state scelte provandole una per una finche' l'API non ha
   risposto con una quota da riva (70 m; il lago sta a 65).
   Se un giorno il riquadro mostrasse temperature stranamente basse, il
   primo sospettato e' questa riga.

   QUANDO PARTE: dopo che la pagina ha finito di caricare. La home pesa gia'
   abbastanza, e il meteo non deve rubarle un millisecondo.

   SE NON RISPONDE: il riquadro non compare e basta. Nessun messaggio
   d'errore, nessuna cornice vuota — un buco visibile e' peggio di
   un'assenza.
   ══════════════════════════════════════════════════════════════════════ */
(function () {
  var LAT = 45.7250, LON = 10.7150;          // riva del lago, quota 70 m
  var CACHE = 'pdlf_meteo', VALIDO = 30 * 60 * 1000;   // mezz'ora

  /* Codici WMO → un disegno e una parola. Le icone sono disegnate, non
     emoji: un'emoji la disegna il sistema operativo, cambia fra iPhone e
     Android e non si puo' colorare. */
  function tipo(c) {
    if (c === 0) return 'sereno';
    if (c <= 2) return 'poco-nuvoloso';
    if (c === 3) return 'nuvoloso';
    if (c === 45 || c === 48) return 'nebbia';
    if (c >= 51 && c <= 57) return 'pioviggine';
    if (c >= 61 && c <= 67) return 'pioggia';
    if (c >= 71 && c <= 77) return 'neve';
    if (c >= 80 && c <= 82) return 'rovesci';
    if (c === 85 || c === 86) return 'neve';
    if (c >= 95) return 'temporale';
    return 'nuvoloso';
  }
  var D = {
    'sereno':        '<circle cx="12" cy="12" r="4.6"/><path d="M12 2.6v2M12 19.4v2M2.6 12h2M19.4 12h2M5.3 5.3l1.4 1.4M17.3 17.3l1.4 1.4M18.7 5.3l-1.4 1.4M6.7 17.3l-1.4 1.4"/>',
    'poco-nuvoloso': '<circle cx="9" cy="9.5" r="3.4"/><path d="M9 3.6v1.6M3.6 9.5h1.6M5.2 5.7l1.1 1.1"/><path d="M17.5 20H8.6a3.6 3.6 0 0 1 0-7.2 5 5 0 0 1 9.5 1.2 3 3 0 0 1-.6 6z"/>',
    'nuvoloso':      '<path d="M17.5 19H7.6a4 4 0 0 1 0-8 5.5 5.5 0 0 1 10.5 1.3 3.4 3.4 0 0 1-.6 6.7z"/>',
    'nebbia':        '<path d="M17.5 15H7.6a4 4 0 0 1 0-8 5.5 5.5 0 0 1 10.5 1.3 3.4 3.4 0 0 1-.6 6.7z"/><path d="M4.5 18.5h15M7 21.5h11"/>',
    'pioviggine':    '<path d="M17.5 15H7.6a4 4 0 0 1 0-8 5.5 5.5 0 0 1 10.5 1.3 3.4 3.4 0 0 1-.6 6.7z"/><path d="M9 18.5v1.6M13 18.5v1.6M17 18.5v1.6"/>',
    'pioggia':       '<path d="M17.5 14H7.6a4 4 0 0 1 0-8 5.5 5.5 0 0 1 10.5 1.3 3.4 3.4 0 0 1-.6 6.7z"/><path d="M8.6 17.5l-1 3.4M12.6 17.5l-1 3.4M16.6 17.5l-1 3.4"/>',
    'rovesci':       '<path d="M17.5 13.5H7.6a4 4 0 0 1 0-8 5.5 5.5 0 0 1 10.5 1.3 3.4 3.4 0 0 1-.6 6.7z"/><path d="M8.4 16.6l-1.2 4M12.6 16.6l-1.2 4M16.8 16.6l-1.2 4"/>',
    'neve':          '<path d="M17.5 14H7.6a4 4 0 0 1 0-8 5.5 5.5 0 0 1 10.5 1.3 3.4 3.4 0 0 1-.6 6.7z"/><path d="M9 18v.01M9 21v.01M12.5 19.5v.01M16 18v.01M16 21v.01"/>',
    'temporale':     '<path d="M17.5 13.5H7.6a4 4 0 0 1 0-8 5.5 5.5 0 0 1 10.5 1.3 3.4 3.4 0 0 1-.6 6.7z"/><path d="M13 15.5l-2.6 4h3.2l-2.4 3.6"/>'
  };
  function icona(c, dim) {
    return '<svg class="mt-ico" width="' + dim + '" height="' + dim + '" viewBox="0 0 24 24" fill="none" ' +
           'stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" ' +
           'aria-hidden="true">' + (D[tipo(c)] || D['nuvoloso']) + '</svg>';
  }

  /* SUL TELEFONO le previsioni dei giorni successivi sono nascoste e resta
     solo il numero: senza una parola accanto non si capisce se sia la
     temperatura di adesso, la massima di oggi o quella di domani. */
  var ORA = { it: 'adesso', en: 'now', de: 'jetzt', fr: 'maintenant', es: 'ahora' };

  function lingua() {
    var l = document.documentElement.lang || 'it';
    return { it: 'it-IT', en: 'en-GB', de: 'de-DE', fr: 'fr-FR', es: 'es-ES' }[l] || 'it-IT';
  }

  function disegna(dati) {
    var box = document.getElementById('pdlf-meteo');
    if (!box) return;
    var giorno = new Intl.DateTimeFormat(lingua(), { weekday: 'short' });
    var righe = '';
    for (var i = 1; i < Math.min(dati.daily.time.length, 5); i++) {
      var d = new Date(dati.daily.time[i] + 'T12:00:00');
      righe += '<div class="mt-g">' +
        '<span class="mt-gn">' + giorno.format(d).replace('.', '') + '</span>' +
        icona(dati.daily.weather_code[i], 15) +
        '<span class="mt-gt">' + Math.round(dati.daily.temperature_2m_max[i]) + '°' +
        '<i>' + Math.round(dati.daily.temperature_2m_min[i]) + '°</i></span></div>';
    }
    box.innerHTML =
      '<div class="mt-ora">' + icona(dati.current.weather_code, 26) +
      '<span class="mt-t">' + Math.round(dati.current.temperature_2m) + '°</span>' +
      '<span class="mt-ora-et">' + (ORA[document.documentElement.lang] || ORA.it) + '</span></div>' +
      '<div class="mt-gg">' + righe + '</div>';
    box.hidden = false;
    box.setAttribute('aria-label',
      'Meteo a Prà de la Fam: ' + Math.round(dati.current.temperature_2m) + " gradi adesso");
  }

  function carica() {
    try {
      var c = JSON.parse(sessionStorage.getItem(CACHE) || 'null');
      if (c && Date.now() - c.q < VALIDO) { disegna(c.d); return; }
    } catch (e) {}
    fetch('https://api.open-meteo.com/v1/forecast?latitude=' + LAT + '&longitude=' + LON +
          '&current=temperature_2m,weather_code' +
          '&daily=weather_code,temperature_2m_max,temperature_2m_min' +
          '&timezone=Europe%2FRome&forecast_days=6')
      .then(function (r) { return r.ok ? r.json() : Promise.reject(r.status); })
      .then(function (d) {
        if (!d || !d.current || !d.daily) return;
        try { sessionStorage.setItem(CACHE, JSON.stringify({ q: Date.now(), d: d })); } catch (e) {}
        disegna(d);
      })
      .catch(function () { /* silenzio: meglio niente che una cornice vuota */ });
  }

  // dopo il caricamento della pagina, e con calma
  function avvia() {
    if (window.requestIdleCallback) requestIdleCallback(carica, { timeout: 2500 });
    else setTimeout(carica, 1200);
  }
  if (document.readyState === 'complete') avvia();
  else window.addEventListener('load', avvia);

  // se cambia la lingua, cambiano i nomi dei giorni
  var vecchio = window.setLang;
  if (typeof vecchio === 'function') {
    window.setLang = function () {
      var r = vecchio.apply(this, arguments);
      try {
        var c = JSON.parse(sessionStorage.getItem(CACHE) || 'null');
        if (c) disegna(c.d);
      } catch (e) {}
      return r;
    };
  }
})();
