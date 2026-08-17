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


### Il marchio in alto a sinistra
C'era **solo in home**. Le nove sottopagine mostravano un **orologio** — un'icona
generica, non il logo — e privacy e cookie non avevano niente in cima. Ora il
logo vero è su tutte e dodici le pagine, e porta alla home.

In home stava **incollato dentro l'HTML come base64, due volte**: viaggiava a
ogni visita e non poteva finire in cache. Diventato un file, `index.html` è
passato da **330 KB a 84 KB**. Il file è ritagliato sull'inchiostro (la tela
originale aveva un quinto di vuoto) e sta a 266×132 — tre volte i 44px a cui si
vede, quindi nitido anche sui telefoni migliori.

⚠️ **Sul telefono la barra traboccava, e non per colpa nostra**: a 390px il tasto
Prenota usciva dallo schermo di 63px già prima. Sotto i 640px ora sparisce il
link «← Camere» (è un doppione — il marchio porta alla stessa pagina) e il
marchio si stringe a 36px. Misurato: rientra sia a 390 che a 360.

📐 **Trappola trovata qui:** `style="height:44px"` scritto sul tag **batte
qualsiasi regola del foglio**, media query compresi. La prima versione della
regola per il telefono era codice morto e sembrava funzionare. Le misure stanno
nel CSS, non in linea.



**Una misura sola, e lo stesso file.** I marchi si vedevano di grandezze diverse
e la causa non era il numero nel CSS: erano **due file diversi**. Quello della
bottega ha molto vuoto attorno alla scritta — l'inchiostro riempiva il **60,3%**
dell'altezza contro il **90,9%** di quello dell'hotel — quindi a parità di
riquadro (46px contro 44) il marchio si vedeva **31% più piccolo**. Ora un file
solo su entrambi i siti, **44px su computer e 36px sul telefono**, tutte e
quindici le pagine. La bottega ci guadagna anche in peso: 110 → 49 KB.

⚠️ **La cartella `pradelafam-shop` in `Sito Prà` è una copia vecchia e non è un
repo git**: il suo `logo.png` pesa 2,4 MB mentre quello pubblicato ne pesa 110
di KB, e l'`index.html` è diverso. Modificarla non pubblica niente. Il sito vero
è `github.com/filippo820/pradelafam-shop` — è la stessa trappola delle tre copie
che divergevano, ancora aperta sulla bottega.


### La barra «Verifica disponibilità» ora funziona
Era **finta**: `<a href="#">` senza una riga di codice dietro. Chi metteva le
date credeva di aver iniziato a prenotare, premeva, e la pagina restava ferma.

📐 **I nomi dei parametri non sono indovinati.** Sono letti nel codice del motore
(`secure-reservation.cloud`, il bundle Angular) e poi **verificati a schermo**:

| parametro | cosa vuole |
|---|---|
| `fromDate` / `toDate` | `yyyy-MM-dd` — la funzione interna è `dateToQueryParam(d) = d.toFormat("yyyy-MM-dd")`, cioè esattamente quello che `<input type="date">.value` restituisce già |
| `rooms` | camere separate da `;`, ospiti da `,` · `A` = adulto, un numero = bambino di quell'età · `A,A` = una camera due adulti · massimo 5 camere |
| `portal` / `lang` | già in uso nei tasti Prenota |

Prova: `…&fromDate=2026-10-02&toDate=2026-10-05&rooms=A,A,A` apre il motore su
**«02 Ven → 05 Lun · 1 Camera 3»**. Funziona anche in tedesco.

Aggiunto anche: **non si può più chiedere una data passata** (`min` = oggi) e se
la partenza precede l'arrivo si sposta da sola al giorno dopo, invece di
rifiutare. Evento `cerca_disponibilita` in Analytics, con o senza date.

⚠️ **Il bottone resta un link vero**, con l'indirizzo già scritto nell'HTML:
funziona col tasto destro e con «apri in nuova scheda», e se `cerca.js` non si
caricasse porterebbe comunque al motore — senza date, cioè come fanno tutti gli
altri tasti Prenota. Non torna a essere un bottone morto.

⬜ Resta il formato `mm/dd/yyyy` nei campi: **non è un difetto dell'HTML**, lo
decide la lingua del sistema operativo del visitatore. Cambiarlo richiede un
calendario scritto da noi.


### Il telefono: la barra si mangiava un terzo dello schermo
Segnalato guardando il sito dal telefono. Misurato, era peggio di come si
vedeva: la barra «Verifica disponibilità» è **fissa in fondo allo schermo** e il
corpo della pagina non le lasciava spazio.

| | prima | dopo |
|---|---|---|
| altezza della barra sul telefono | **225px** (quattro righe) — il 34% di un iPhone SE, sempre | **121px**, griglia 2×2 |
| «Prenota ora» e «Scopri gli appartamenti» | **coperti dalla barra** | visibili |
| piè di pagina | telefono, email, «Come arrivare» **sotto la barra** — anche su computer | libero |
| meteo sul telefono | solo «24°», senza dire di cosa | «24° **adesso**» ×5 lingue |
| apertura | quasi tutta cielo sui telefoni alti | accorciata a 86svh **solo sopra i 750px di schermo** |

L'etichetta «VERIFICA DISPONIBILITÀ» sparisce sul telefono: i campi hanno già la
propria. Il pulsante della chat si alza sopra la barra (`var(--barra, 0px)`, che
sulle altre pagine ripiega a zero perché la barra non c'è).

📐 **Trappola, presa due volte nella stessa sessione:** a parità di peso, nei
fogli di stile **vince l'ultima regola scritta**. Il blocco per il telefono stava
più in alto di `.hero`, `.hc`, `.htag` e `.hdesc` e non faceva niente — pur
sembrando applicato. Ora sta **in fondo al foglio**, con un commento che spiega
perché. Stessa famiglia dello `style="height:44px"` in linea che batteva il
media query: **se una regola sembra non fare effetto, misurare, non guardare.**

📐 **E una scoperta contro-intuitiva:** accorciare l'apertura *peggiorava* le
cose su uno schermo corto — il testo finiva sotto la barra di navigazione. Il
blocco misurava 630px su 667 di schermo. Per questo l'accorciamento vale solo
sopra i 750px di altezza, e sugli schermi corti si recuperano ~50px stringendo
gli spazi vuoti (non i testi).


### Contrasti e corpi del testo — misurati, non guardati
Nasce da una segnalazione precisa: «le scritte bianche su quella foto azzurra
non si leggono». Era vero, e molto peggio del previsto.

**Come sono stati misurati.** Per il testo sopra una foto non esiste uno sfondo
da leggere nel CSS: lo sfondo è l'immagine. La pagina viene fotografata **due
volte alla stessa altezza — con il testo e senza** — e il contrasto si calcola
fra il colore della scritta e i pixel che stanno esattamente sotto le lettere.
Strumento in scratchpad (`misura.mjs`), non versionato.

📐 **Ci sono voluti tre tentativi falliti, e ognuno insegna qualcosa:**
1. prendere il pixel peggiore di **tutto il riquadro** includeva gli angoli
   arrotondati, cioè pixel FUORI dal bottone → «1:1» su un bottone dorato con
   testo scuro, impossibile;
2. fotografare a fette richiede coordinate, e le coordinate sbagliano con lo
   scorrimento morbido, la parallasse e le immagini pigre che arrivano fra uno
   scatto e l'altro;
3. la versione buona **ritaglia ogni elemento con la fotocamera del browser**:
   niente coordinate, niente errori.
**Quando un numero è impossibile, il primo sospettato è lo strumento.**

**Trovato e corretto:**

| | prima | dopo |
|---|---|---|
| titolo dell'apertura, telefono | **1,52:1** | 5,60 |
| «Al Prà» in oro, telefono | **1,19:1** | 4,27 |
| riga d'indirizzo sotto il titolo | **1,86:1** | 5,13 |
| descrizione dell'apertura | **2,67:1** | 7,64 |
| riquadro meteo sul cielo | 3,29:1 | 9,22 |
| **oro del marchio su crema** | **2,62:1** ovunque | 4,72 / 3,66 |
| testo schede appartamento | 3,03:1 | 6,92 |
| piè di pagina (38% di chiaro) | 3,37:1 | 5,7 |

L'oro `#b8934a` su crema dà **2,62:1**: sotto il minimo per un testo (4,5), e
sotto anche quello per il testo grande (3). Era usato per i numeri di sezione,
**il corsivo dentro ogni titolo**, le etichette dei contatti, i link di privacy
e cookie. Due nuovi colori, entrambi scelti dal calcolo e non a occhio:
`--gold-testo:#846934` (4,72 su crema) e `--gold-titolo:#9a7a3c` (3,66, solo per
il corsivo grande). **`--gold` resta invariato dove sta su fondo scuro**, dove
dà 6,40:1 e va benissimo.

**Corpi del testo.** Il testo che si legge davvero stava a **13px**, contro i 16
di riferimento: portato a 15. Restano sotto i 12px le etichette in maiuscoletto
(«SCORRI», «CAMERA», i numeri di sezione) — è una scelta editoriale diffusa e non
sono testo di lettura, ma **sono ancora il 52% delle scritte** e vale la pena
decidere se tenerle così.

⚠️ **Un falso allarme dichiarato:** `.book-cta-title` risulta 2,87:1 anche dopo i
fix. Verificato a mano: è bianco su fondo scuro, **16,76:1**. È lo strumento che
sbaglia su quell'elemento, non la pagina.

### Il meteo si apre al tocco
Sul telefono i giorni non ci stanno in fila e restava un numero solo. Ora il
riquadro si apre toccandolo. **Le previsioni partivano già da domani** — oggi non
è mai stato mostrato: verificato contro i dati dell'API.


### Menu del telefono, ritorno indietro, date proposte
Tre segnalazioni in fila, e la prima era grossa.

**Sul telefono non c'era né il menu né le lingue.** Sotto i 900px le otto voci
sono nascoste e **non esisteva nessun pulsante per riaprirle**: la barra aveva
solo marchio e «Prenota». Sotto i 560px sparivano anche le cinque lingue — un
ospite tedesco poteva cambiare lingua solo scorrendo fino in fondo a una pagina
di quindicimila pixel. Ora c'è un pannello a tutto schermo: le voci, le lingue e
i contatti.

**Il ritorno indietro dalle sottopagine: difetto introdotto da noi.** Per far
stare la barra sul telefono avevamo nascosto «← Camere», e restava solo il
marchio — che nessuno legge come «indietro». Ora le lingue stanno nel pannello e
lo spazio c'è: il ritorno è di nuovo visibile. Il pannello nelle sottopagine
prende le voci dalla striscia in fondo (Camere · Appartamenti · Limonaia ·
Contatti), che ha già gli stessi link: **non inventa niente**.

**La ricerca propone le date.** I campi vuoti costringevano a due passaggi di
calendario prima di sapere se c'era posto. Ora propone il **primo venerdì utile →
domenica**, due notti, restando modificabili.

📐 **Il pannello è un `<div>`, non un `<nav>` — e la prima versione lo era.**
Nel foglio c'è `nav{position:fixed;height:68px}` scritto sull'**elemento**, e un
pannello a tutto schermo chiamato `<nav>` se la prende: era alto **117px invece
di 844**, cioè solo il suo stesso margine interno. È la stessa trappola del
pannello della chat, che era un `<section>` e si prendeva
`section{padding:120px}`. **Terza volta in questo sito che una regola su un nome
di elemento morde un componente nuovo.**

📐 **E la terza volta dello `style` sul tag:** le lingue delle sottopagine non
sparivano perché quel contenitore ha `style="display:flex"` scritto sul tag, che
batte il foglio. Serve `!important`.


### Meteo più basso · lingua verificata · la freccia non va più a capo
**Meteo.** Su computer da 104 a 128px. Sul telefono lo spazio è quasi nullo — la
barra finisce a 68 e la riga d'indirizzo comincia a 130 — quindi scende solo a
84 e si stringe (padding 6→4) per non toccarla: restano 2px.

**Lingua del browser — provata, non dedotta.** Dieci browser diversi:
`it-IT en-GB en-US de-DE de-AT fr-FR es-ES es-MX pl-PL nl-NL`. Tutti corretti:
le varianti regionali (`de-AT`, `es-MX`) prendono la lingua base, le lingue non
gestite (`pl`, `nl`) tornano all'italiano invece di restare vuote, e in ogni
caso viaggiano insieme **i testi, i nomi dei giorni del meteo e il `lang=` del
motore di prenotazione**. Verificato anche che **una scelta salvata batte il
browser**: browser tedesco + scelta «fr» → dopo il ricaricamento resta francese.

**La freccia.** «Prenota →» andava a capo sul telefono, lasciando la freccia da
sola sotto. Le **106 frecce** del sito (HTML + dizionario delle traduzioni) ora
sono legate all'ultima parola con uno **spazio unificatore**: non si spezza mai.
Meglio di `white-space:nowrap`, che avrebbe fatto traboccare i bottoni lunghi
(«Controlla disponibilità →») sugli schermi stretti — quelli vanno ancora a
capo, ma **con la freccia attaccata alla parola**. Vale in tutte e cinque le
lingue senza altro lavoro.


### Il meteo sotto la riga dell'indirizzo
Richiesto due volte, e la seconda ha richiesto di cambiare approccio.

**Appoggiarlo lì non si poteva.** Subito sotto quella riga comincia il titolo:
misurando il riquadro contro l'inchiostro vero delle righe, urtava in **quattro
lingue su cinque** (il tedesco «Willkommen» arriva a 322px). Provato anche in
fondo all'apertura: lì urtava i bottoni in francese e spagnolo. Su un telefono
l'apertura è **una colonna sola** — non esiste una fascia destra libera, e
qualunque riquadro appoggiato prima o poi tocca qualcosa.

**Soluzione: nel flusso.** Il riquadro è un blocco allineato a destra fra
l'indirizzo e il titolo. Così non può urtare niente, in nessuna lingua e a
nessuna larghezza — è il layout a garantirlo, non una misura fortunata.

Due conseguenze da gestire, entrambe trovate misurando:
- **costa una cinquantina di pixel** e sugli schermi corti il blocco finiva
  sotto la barra di navigazione → sotto i 760px di altezza il titolo scende a
  2,9rem e gli spazi si accorciano;
- **aprendolo spingeva il titolo** e l'indirizzo finiva sotto la barra → i
  giorni ora **scendono sopra** il titolo invece di spingerlo.

📐 **Lo spostamento lo fa il codice, non il foglio di stile** (`meteo.js`,
`sistema()`): un elemento assoluto si ancora al primo antenato posizionato, e
`.hc` lo è — lasciandolo dentro il flusso del testo, su computer finiva a metà
pagina invece che in alto a destra. Su schermo grande torna figlio
dell'apertura.

📐 **Quarta volta con la stessa trappola:** la regola che rimpicciolisce il
titolo sugli schermi corti, scritta sopra la regola base `.hh1`, **non faceva
niente**. A parità di peso vince l'ultima. Ora sta nel blocco in fondo al
foglio, dove ho già imparato che devono stare.


---

## ⬜ Aperto

### Da fare, in ordine di quanto pesa
1. 🔑 **La chiave dell'assistente è rifiutata.** Netlify → `pradelafam` → Site
   configuration → Environment variables → `ANTHROPIC_API_KEY`. Una variabile
   **c'è già**, ma Anthropic la respinge: chiedendo al sito pubblicato, la
   funzione risponde `guasto: authentication_error` (se mancasse del tutto
   direbbe `chiave assente` — sono due cose diverse). Probabile chiave vecchia,
   revocata, o incollata con uno spazio. **Finché non è valida il riquadro si
   apre ma dice «Qualcosa non ha funzionato».** È l'unica cosa che manca.

   Per rileggere la diagnosi dopo averla cambiata, senza aprire il sito:
   ```bash
   curl -s -X POST https://pradelafam.netlify.app/api/chat \
     -H 'content-type: application/json' \
     -H 'origin: https://pradelafam.netlify.app' \
     -d '{"messaggi":[{"ruolo":"persona","testo":"Che camere avete?"}]}'
   ```
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
- **Le date mostrano `mm/dd/yyyy`** su un dispositivo in inglese e `gg/mm/aaaa`
  su uno in italiano: lo decide la lingua del sistema operativo di chi guarda,
  non l'HTML. Per imporre il formato italiano a tutti serve un calendario
  scritto da noi.

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
