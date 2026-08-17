# Sito Prà de la Fam — a che punto siamo

Aggiornato: **17 agosto 2026** (notte)

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

### Anteprime social
Un'immagine **1200×630 per ogni pagina** (chi condivide la Tripla deve vedere la
Tripla), più `og:title`, `og:description` e `canonical` — che mancavano ovunque.
Verificato **con il JavaScript spento**, che è come lo vedono WhatsApp e Facebook.

⚠️ **L'anteprima resta in italiano** anche per chi vede il sito in tedesco: chi la
genera non esegue il JavaScript. Tradurla richiederebbe una pagina per lingua.

### Privacy e cookie
Quattro pagine nuove (due per sito). **Ogni cookie elencato è stato osservato in un
browser**, non copiato da un modello: prima del consenso nessun cookie, dopo
«Accetta» `_ga` e `_ga_M29PYB9NDX` a 400 giorni, dopo «Solo necessari» nessuno.

Scritte anche due cose che un modello tacerebbe: **Google viene contattato anche
prima del consenso** (ping senza cookie del Consent Mode: nessun dato sul
dispositivo, ma l'IP arriva comunque) e **i caratteri tipografici sono caricati dai
server di Google**, il che espone l'IP.

Titolare: **FAM S.r.l.**, confermata dall'utente.

I link all'informativa stanno **fuori** dal testo tradotto del banner: dentro
sarebbero spariti al primo cambio lingua.

### Meteo
In alto a destra nell'hero: oggi e i quattro giorni dopo, da Open-Meteo (gratuita,
senza chiave).

⚠️ **Le coordinate sono la cosa importante di quel file.** Tignale paese sta in
montagna, il Prà sta sul lago: chiedendo il meteo per «Tignale» l'API risponde con
un punto a **1147 m** — alla prova 21,6° contro i 28,0° della riva. Le coordinate
finali (`45.7250, 10.7150`) sono state trovate provandone una decina finché la
quota risposta non è stata da riva (70 m). Se un giorno mostrasse temperature
stranamente basse, il primo sospettato è quella riga.

La richiesta parte **127 ms dopo** il caricamento della pagina. Se l'API non
risponde il riquadro non compare: un buco visibile è peggio di un'assenza. I nomi
dei giorni seguono la lingua senza traduzioni nuove.


### Assistente
Un riquadro in basso a destra, su tutte e dieci le pagine. Risponde in cinque
lingue, **solo con quello che il sito dice**: il materiale è `kb.json`, estratto
dalle pagine stesse (non riscritto a mano — una copia diverge al primo cambio di
prezzo, e diverge in silenzio).

⚠️ **La regola che conta: non sa se c'è posto.** Disponibilità e tariffe stanno nel
motore di prenotazione. Un assistente che stima la disponibilità di una camera fa
un danno vero — qualcuno prenota un viaggio su una frase falsa. Rimanda al tasto
Prenota o al telefono, sempre.

Il pannello che c'era **era troncato**: mancavano il pulsante e il `<div>` che
apre il riquadro, e le funzioni `toggleChat`/`chatKey`/`sendChat`/`autoResize`
non esistevano. **Cinque dei sette `</div>` di troppo erano suoi:** rifacendolo
intero l'HTML è passato da 7 a 2.

Il costo massimo di una domanda è noto in partenza: istruzioni ~7.900 gettoni
(marcate come riutilizzabili, quindi si pagano per intero solo la prima volta),
storia al massimo 4.000 caratteri, risposta 380 gettoni. La chiave sta in una
funzione Netlify, mai nel sito.

⚠️ **Il tetto d'uso qui è parziale.** Le funzioni Netlify sono senza stato e
replicate: il contatore vede solo le richieste capitate sulla stessa istanza.
Tengono davvero i tetti su lunghezza e risposta. Se il sito prendesse traffico
vero, il tetto solido si fa nel database — su Colgo la funzione esiste già.


---

## ⬜ Aperto

### Da fare, in ordine di quanto pesa
1. 🔑 **La chiave dell'assistente, da mettere a mano.** Netlify →
   `pradelafam` → Site configuration → Environment variables →
   `ANTHROPIC_API_KEY`. **Finché non c'è, il riquadro si apre ma risponde
   «Qualcosa non ha funzionato».** È l'unica cosa che manca per farlo parlare.
2. **Ospitare i caratteri tipografici sul nostro server.** Oggi arrivano da
   Google e questo espone l'indirizzo IP dei visitatori — è scritto nella cookie
   policy come miglioramento in programma.
3. **Il link della bottega «← Torna al sito principale»** punta ad
   `alpradelafam.com`. Da cambiare **il giorno del passaggio**, non prima.

### Difetti noti, non ancora risolti
- **`index.html` ha 2 `</div>` di troppo** (erano 7: cinque erano del pannello
  chat troncato, spariti rifacendolo). Non introdotti da noi: verificato contro
  il commit di partenza.
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
