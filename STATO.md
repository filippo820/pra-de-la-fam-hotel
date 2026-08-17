# Sito Prà de la Fam — a che punto siamo

Aggiornato: **17 agosto 2026**

---

## In una riga

Il sito nuovo (costruito a maggio, mai andato online) è ora **collegato a GitHub
e pubblicato in automatico su `pradelafam.netlify.app`**. Non è ancora il sito
ufficiale: `alpradelafam.com` resta il vecchio WordPress, e da lì passano le
prenotazioni.

| | |
|---|---|
| repo | `github.com/filippo820/pra-de-la-fam-hotel` |
| pubblicato su | `pradelafam.netlify.app` (deploy automatico a ogni push) |
| sito ufficiale | `alpradelafam.com` — **vecchio WordPress, non toccato** |
| bottega | `github.com/filippo820/pradelafam-shop` → `pradelafam.shop` (già online) |

---

## ✅ Fatto

### Foto
- **18 immagini davano 404**: undici scelte dall'archivio `04_Foto_Video`
  guardandole una per una (dal nome non si sceglie: si chiamano
  `PHOTO-2025-05-05-14-50-00`). Le altre sette erano una galleria doppione
  sulla pagina Pomelo che puntava a una cartella mai esistita.
- **Clementina e Bergamotto** mostravano la copertina due volte: la galleria
  c'era ma era vuota. Ora 7 e 5 foto.
- **Sezioni senza immagini**: `#hotel` aveva un riquadro grigio vuoto, la
  Limonaia mostrava la facciata di un altro edificio, il Territorio non aveva
  nessuna foto. Ora l'albergo vero, le terrazze della limonaia dall'alto e il
  promontorio dal drone.
- Due sostituzioni: i limoni della Doppia ora hanno il lago dietro; nella
  Familiare via un doppione, dentro la stanza intera.

### Peso
- **Sito hotel: da 52,7 MB a 21,4 MB.** Home da 8,9 a 3,9. Nessuna riga di HTML
  toccata: solo dimensione e compressione. Le copertine erano servite a 1920px
  ed erano mostrate a 342px sul telefono.
- **Bottega: da 21,7 MB a 3,4.** Otto foto prodotto erano in PNG e da sole
  facevano 18 dei 19 MB. Il logo pesava 2,36 MB per essere mostrato a 69 pixel.

### Cinque lingue
Prima i dieci pulsanti IT/EN/DE/FR/ES **non facevano niente** — `setLang is not
defined`, e non c'era un solo marcatore di traduzione. Ora:
- 575 elementi marcati, dizionario in `i18n.js`
- copertura misurata: **en 93% · de 93% · fr 92% · es 89%** (il resto sono
  misure, indirizzi e nomi propri, che restano in italiano di proposito)
- selettore lingua aggiunto alle 9 sottopagine, che non l'avevano
- la lingua si ricorda, e al primo arrivo si prende da quella del browser
- i 36 pulsanti Prenota passano al motore la lingua del sito (era fisso su `it`)

### Analytics
GA4 `G-M29PYB9NDX` — **la stessa proprietà della bottega**, perché hotel e
bottega sono un viaggio solo. Consenso negato di default, banner Accetta /
Solo necessari.

Si misura: lettura (25→100%), tempo (10s→5min), sezioni davvero guardate, clic
verso bottega/ecomuseo/telefono/mail, e soprattutto **Prenota con il punto di
partenza** (barra, hero, sezione hotel, sezione appartamenti, piede, scheda
camera).

### Piccole cose
- refuso «Appartamentoi» → «Appartamenti» (5 pagine) e «Camerai» → «Camere» (4)
- `camera-doppia-economy-02 .jpg` aveva uno spazio nel nome: dava 404
- il punto Pomelo sulla mappa diceva ancora «Matrimoniale»: da quest'anno è
  appartamento

---

## ⬜ Aperto

### Da fare, in ordine di quanto pesa
1. **`og:image` su tutte le pagine** (hotel e bottega). Oggi un link condiviso
   su WhatsApp arriva nudo, senza anteprima. Per un hotel, dove il link lo gira
   l'ospite agli amici, è il canale più naturale che c'è.
2. **Pagine privacy e cookie.** Il banner della bottega rimanda a
   `/privacy.html` e `/cookie.html` che **danno 404**; sul sito hotel non
   esistono affatto. Il consenso viene raccolto davvero, ma l'informativa è
   incompleta.
3. **Meteo** in alto a destra — nel codice della home c'è già un segnaposto
   `<!-- weather widget -->`. Open-Meteo è gratuito e non chiede registrazione.
   Va caricato dopo il resto, per non aggiungere attesa.
4. **Chatbot.** Il pannello esiste già nell'HTML (`Assistente Prà de la Fam`,
   campo di scrittura, messaggio di benvenuto) ma **mancano le funzioni**
   `toggleChat`, `chatKey`, `sendChat`, `autoResize`. Deve anche rispondere su
   cosa fare nei dintorni e portare al tasto Prenota.
5. **Il link della bottega «← Torna al sito principale»** punta ad
   `alpradelafam.com`. Da cambiare **il giorno del passaggio**, non prima.

### Difetti noti, non ancora risolti
- **`index.html` ha 7 `</div>` di troppo.** Non introdotti da noi: verificato
  contro il commit di partenza. Probabilmente lo stesso troncamento che ha
  portato via il blocco JavaScript.
- **`closeLb` è chiamata ma non esiste**, per un lightbox che in home non c'è:
  residuo di codice tolto.
- **Immagini senza descrizione** (`alt`) nelle gallerie delle sottopagine: 7 per
  pagina. Accessibilità e Google.
- **Netlify riscrive l'HTML** in fase di pubblicazione: gli attributi
  `onmouseover` arrivano con le virgolette rotte. Da guardare.
- **Le date della barra prenotazione** mostrano `mm/dd/yyyy`, formato americano
  su un sito italiano.

---

## ⚠️ Cose da sapere prima di lavorarci

**Le tre copie che divergevano.** Fino a ieri esistevano tre versioni del sito:
la cartella locale, il repo GitHub e quello che era pubblicato. **Nove foto —
le copertine delle card in home, quelle che vendono — esistevano solo online.**
Ripubblicare dalla cartella le avrebbe cancellate tutte e nove. Adesso il repo
è collegato a Netlify e quel disallineamento non può più succedere: quello che
sta qui è quello che è online.

**Verificare che una pagina si APRA, non solo che le immagini carichino.** Una
modifica aveva lasciato una `<section>` aperta e la pagina Pomelo era collassata
a 900px — tutte le immagini intatte, e la pagina illeggibile. Da allora il
controllo include altezza e scorrimento, oltre ai 404.

**Il ripristino da backup toglie anche le correzioni buone.** Ripristinando
Pomelo per riparare la sezione, è tornato indietro anche il refuso già corretto.

**L'archivio foto giusto è `04_Foto_Video`**, non `FAM_BACKUP_20260421`. Dentro,
`Foto_sito_claude_edit` è una selezione già fatta per il sito. Le riprese da
drone (`Esterni_Struttura/Foto drone pra`, 18 foto) sono le migliori
dell'archivio.

---

## Come si lavora

```bash
cd ~/Documents/Fam_S.r.l./Sito\ Prà/pradelafam
python3 -m http.server 8911        # anteprima su http://localhost:8911
git add -A && git commit -m "…" && git push
```

Il push pubblica da solo su `pradelafam.netlify.app` in meno di un minuto.

**Dopo aver cambiato un testo italiano** in una pagina, la sua chiave `data-i18n`
cambia e la traduzione va rifatta: gli script sono in
`scratchpad/` (`marca.py` per le chiavi, `costruisci.py` per `i18n.js`).
