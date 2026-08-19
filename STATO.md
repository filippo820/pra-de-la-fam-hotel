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


### Carte appartamenti: stessa misura, meno bianco — e un guasto mio riparato
🔴 **La descrizione degli appartamenti era invisibile: 1,10:1.** L'avevo
"corretta" io il giorno prima, credendo che quelle carte fossero su fondo scuro.
**Sono bianche.** La misura era sbagliata perché le carte scorrono di lato e lo
strumento leggeva la sezione scura dietro invece della carta. Ripristinato
`--steel`: **6,06:1**.
📐 **Regola:** un elemento che scorre fuori dallo schermo non si misura da fermo.
E una correzione di contrasto va confermata guardando il fondo **dichiarato**
dell'elemento, non solo il numero che esce dallo strumento.

**Tutte della stessa misura.** Clementina e Bergamotto erano `wide`: più larghe
(640 contro 420) e con la foto **panoramica** (`aspect-ratio:16/7` → 184px contro
315). Ora larghezza unica e proporzione unica 4/3. Scarto misurato: **0px sul
telefono**, 4px su computer (arrotondamento). I bottoni «Prenota» sono allineati
fra le carte (`margin-top:auto`).

⚠️ La foto doveva anche essere bloccata (`flex:none`): nelle carte con la
descrizione più lunga l'immagine **cedeva spazio al testo** e tornava diversa.

**Meno bianco sul telefono:** margini interni da 1,4/1,6/1,7rem a 1/1,05/1,15, e
spazi fra nome, descrizione e etichette accorciati. Carta da 489 a 474px con la
stessa foto.


### Le prime righe sotto l'header: riprodotto e chiuso
Segnalato «home, telefono, sopra il meteo» — cioè la riga dell'indirizzo. Alle
altezze di prova non succedeva mai; **succede alle altezze vere di Safari**, che
si mangia un centinaio di pixel con le sue barre. Riprodotto a **375×553** e
**360×640**: l'indirizzo finiva **8px sotto la barra**.

**Causa.** L'apertura era alta *esattamente* quanto lo schermo, con il contenuto
ancorato in basso. Se il blocco cresce — ed è cresciuto quando il meteo è
entrato nel flusso — il testo esce **dall'alto** e scivola sotto la barra di
navigazione. Non c'era nessun limite a impedirlo.

**Correzione strutturale:** l'apertura ora **cresce** (`height:auto` +
`min-height:100svh`) e il contenuto tiene sempre libera la fascia della barra
(`padding-top`). Così è il layout a garantirlo, non l'altezza dello schermo.
Provato su otto formati — da 553 a 844px di altezza: nessuno copre più niente.

Sotto i 620px di altezza l'apertura **non ci sta comunque** e scorre: meglio
scorrere che nascondere. Lì il titolo si stringe ancora, così il primo bottone
resta visibile senza scorrere.

📐 **Quinta volta con la stessa trappola.** Il blocco «schermi molto bassi»,
scritto *prima* di quello «schermi corti», non faceva niente: i due si
sovrappongono e a parità di peso vince l'ultimo. Il titolo misurava 46,4px dove
ne avevo chiesti 38,4. **Se una regola sembra non fare effetto, misurare il
valore calcolato — non guardare la schermata.**


### Contenuto rialzato · campi data induriti per iOS
**Rialzato.** La guardia contro la barra, messa sul *contenuto*, faceva scendere
il testo di un centinaio di pixel — e la mia `height:100svh` **sovrascriveva** la
regola che accorcia l'apertura sui telefoni alti (86svh). Ora la guardia sta
sull'**apertura** (`padding-top:72px`, border-box) e la misura è `min-height:86svh`:
il testo torna esattamente dov'era (89px su iPhone 14 pieno) e l'apertura può
comunque crescere quando serve. Otto formati: l'indirizzo sta sempre fra 72 e
89px, mai sotto i 68 della barra.

**Campi data.** I riquadri Arrivo/Partenza che si sovrappongono **non si
riproducono su Chromium**: i contenitori non si toccano a nessuna delle sette
larghezze provate, e il testo non deborda in nessuna delle tre lingue provate.
La causa nota su iOS è che `<input type="date"><` ha una **larghezza minima
imposta dal sistema**, e sia le caselle della griglia sia i campi partono da
`min-width:auto`: senza `min-width:0` non possono rimpicciolire e sbordano.
Applicato `min-width:0` alle caselle **e ai campi**, più `max-width:100%` e un
corpo leggermente più piccolo.
⚠️ **Non è verificato sul dispositivo:** è la correzione giusta per quella
causa, ma la conferma può darla solo un iPhone vero.


### I campi data che «si sovrapponevano»: era un traboccamento
Chiuso grazie a una **foto di uno schermo vero** (iPhone Pro Max), dopo che due
motori, cinque profili, sette larghezze, tre lingue, cinque dimensioni di testo e
l'orientamento orizzontale non l'avevano riprodotto.

**Misurato dalla foto:** il campo era largo **212px dove la colonna ne dava 197**.
Non si sovrapponevano: **«Partenza» usciva dallo schermo a destra**, e il bordo di
«Arrivo» gli finiva addosso. È la larghezza minima che iOS impone a
`<input type="date">` — e che nessun motore da scrivania riproduce, perché
disegna quel controllo in un altro modo.

⚠️ **La foto era di una pagina in cache:** lo stacco misurato era 9px, cioè quello
di prima delle correzioni pubblicate 19 minuti prima. Su iPhone conviene sempre
chiedere una **finestra privata** prima di dare per buono un difetto.

**Fermo duro:** `overflow:hidden` sul riquadro. Provato forzando il campo a
pretendere 212 e 260px: i riquadri restano nella loro colonna, allineati con
«Ospiti» e «Cerca» sotto, e **niente esce dallo schermo**. Al massimo si perde il
bordo destro del campo — molto meglio di un campo fuori pagina.
Aggiunti anche `-webkit-appearance:none` e margini interni più stretti, perché
iOS scrive la data come «21 ago 2026», più larga di «21/08/2026».

📐 **Regola:** quando un difetto non si riproduce in nessun motore, la foto dello
schermo vero non è un ripiego — è **la misura**. Da quella sono usciti i 15px di
troppo in due minuti, dopo un'ora di prove al buio.


### L'assistente: due problemi diversi
**«Non si fa vedere».** Misurato: sull'apertura il pulsante si staccava dallo
sfondo **1,84:1** — cerchio scuro su foto scura, sotto il minimo di **3:1** per un
comando. Aggiunto un **anello chiaro**: corpo scuro *e* anello chiaro, così almeno
uno dei due stacca sempre. Provato a sette punti di scorrimento: il peggiore ora
è **6,12:1**.

📐 **La prima misura era falsa** perché mediava anello e corpo insieme e su fondo
grigio dava 1,45. Un comando a due colori si misura **un colore alla volta**:
basta che uno stacchi.

🔑 **«Non fa domande».** Non è un difetto del sito: la chiave Anthropic su Netlify
è **ancora rifiutata**. La funzione risponde `guasto: authentication_error` —
significa che una variabile c'è ma Anthropic non la accetta (se mancasse direbbe
`chiave assente`). Il riquadro si apre, mostra il benvenuto e i tre spunti, ma a
ogni domanda risponde «Qualcosa non ha funzionato».
**Netlify → `pradelafam` → Site configuration → Environment variables →
`ANTHROPIC_API_KEY`.** È l'unica cosa che manca per farlo parlare.


### Le cinque schede appartamento sono link veri
Erano `<article onclick="location.href=…">`: col mouse funzionavano, ma **Google
non le seguiva** — cinque pagine con foto e descrizioni invisibili ai motori — il
**Tab non ci arrivava** e il tasto destro non apriva niente.

**Non si poteva avvolgere la scheda in un `<a>`:** dentro c'è già il link
«Prenota», e un link dentro un link è HTML non valido. Usato il **link esteso**:
il nome è un `<a>` vero e il suo `::after` copre tutta la scheda; «Prenota» sta
sopra e continua a portare al motore.

⚠️ **`data-i18n` è andato sull'`<a>`, non sull'`<h3>`.** La traduzione sostituisce
l'`innerHTML` dell'elemento marcato: lasciandolo sull'`h3` avrebbe **cancellato il
link** al primo cambio di lingua. Verificato passando a tedesco e tornando: i
cinque link restano.

Sistemati anche i cinque link del piè di pagina, che dicevano «App. Bergamotto» e
portavano alla sezione generica.

⬜ Restano i punti della **mappa della proprietà**, che usano `data-href`: per un
visitatore funzionano, per Google no. Le schede e il piede ora danno comunque una
strada seguibile a tutte e cinque le pagine.


### «Come arrivare» — il primo pezzo recuperato dal vecchio sito
Era la mancanza più grossa per chi sta per prenotare: sul vecchio WordPress c'è
una pagina intera, qui non c'era nulla. Ora è una sezione dentro **Contatti**:
auto, treno, aereo, più la nota sulla Gardesana e le coordinate GPS.

**Riscritta, non copiata.** L'originale era tutto in maiuscolo e conteneva
errori che non aveva senso propagare:
- «Riva di Trento» **non esiste** → Riva del Garda;
- sull'A22 **non c'è un'uscita «Rovereto Est»**: per Riva si esce a Rovereto Sud;
- refusi: «AUTOSTADA», «LINATE EMALPENSA», «OGNI LES 20 MIN».

⚠️ **Tolte le distanze in chilometri degli aeroporti.** Il vecchio sito dava
Verona 60, Montichiari 45, Milano 100: sono misure che non ho potuto verificare
e che mi sembrano ottimistiche (Malpensa a 100 km è quasi certamente sbagliato).
Gli aeroporti sono elencati **dal più vicino al più lontano**, senza numeri.
Meglio nessun numero che uno sbagliato a chi sta prenotando un transfer.
Se servono i km, vanno misurati e me li si passa.

Tolte anche le frequenze delle navette aeroportuali: erano di quindici anni fa.

✅ Le coordinate GPS del vecchio sito sono state **verificate**: cadono a 492 m
da quelle usate per il meteo, cioè lo stesso posto.

Tradotta in tutte e cinque le lingue (15 frammenti nuovi).

### 🔴 Rifacendo il dizionario l'ho azzerato — e come non succeda più
`marca.py` scrive in `it.json` **solo gli elementi che ha marcato in quella
passata**. Rilanciandolo su un sito già marcato, `it.json` è sceso da 341 testi a
89; poi `costruisci.py` l'ha letto e ha riscritto `i18n.js` **da 96 KB a 3** —
cioè il sito senza traduzioni. Ripristinato da git.

📐 **La fonte di verità non è l'ultima passata di marca.py: è l'HTML.** Scritto
`strumenti/raccogli.py`, che ricostruisce `it.json` leggendo tutti gli elementi
`[data-i18n]` delle pagine. **Va lanciato sempre fra `marca.py` e
`costruisci.py`.** (`it.json` non è mai stato in git: adesso c'è lo strumento che
lo rigenera, che è meglio.)

⚠️ **Seconda trappola, dentro la prima:** `raccogli.py` normalizza gli spazi, e
`\s` in Python **comprende lo spazio unificatore**. Quindi nelle chiavi dei
frammenti lo spazio unificatore diventa normale. Le chiavi delle traduzioni
devono avere lo spazio **normale**, i valori quello **unificatore** — altrimenti
o non combaciano, o la freccia torna a staccarsi nelle quattro lingue. Sistemato
in entrambi i file, verificato: 0 valori con lo spazio sbagliato.

Dizionario finale: **104 KB, en 247 · de 248 · fr 242 · es 231** testi tradotti
(prima 235 · 237 · 231 · 219). Verificato che nessuna traduzione preesistente sia
andata persa: le uniche tre sparite erano del pannello chat rimosso.


### «I sentieri dimenticati» — il Territorio recuperato
Sul sito era ridotto a mezza riga dentro la scheda Trekking: «percorsi militari
storici panoramici». Sul vecchio sito c'è il racconto per intero, ed è la cosa
più caratteristica del posto: la rete di sentieri militari **dimenticati dalla
cartografia**, la batteria di artiglieria sul Monte Castello, le linee difensive
lungo il Dosso Piemp fino al Passo della Puria, e come ci si arriva.

Nessun altro hotel del Garda ha una rete di trincee dietro casa.

⚠️ **Non ho aggiunto una data.** Sono con ogni probabilità opere della Grande
Guerra, ma il vecchio sito non lo dice e non volevo mettere in bocca alla
struttura una cosa che nessuno ha scritto. Se la data è certa, si aggiunge in
una riga.

### «Come arrivare» è una scheda che si apre
Chiusa occupa **56px sul telefono invece di 1137**, e 67 invece di 569 su
computer. Si apre col dito e **col tasto Invio**.

📐 È un `<details>`, non un finto accordion in JavaScript: funziona da tastiera
di suo, funziona anche senza JavaScript, e **il testo resta nel documento** —
quindi Google lo legge lo stesso. Verificato: a scheda chiusa, «Rovereto Sud» è
comunque dentro la pagina.

⚠️ **`marca.py` non marca dentro un `<summary>`**: la riga «In auto, in treno,
in aereo» sarebbe rimasta in italiano nelle altre quattro lingue. Impronta messa
a mano (`sha1` del testo italiano, primi 10 caratteri) e traduzione aggiunta.


### I nomi degli agrumi e la spiaggia
**Ogni appartamento spiega il proprio nome.** Sul vecchio sito ogni pagina
apriva con l'agrume fra parentesi; qui non c'era. Ora una riga in corsivo sotto
la posizione, su tutte e cinque le pagine — e dice anche **perché** si chiamano
così: «Gli appartamenti portano il nome di un agrume della limonaia.» È il filo
che li lega alla limonaia, e si era perso del tutto.

**La spiaggia a meno di venti metri** è entrata nella storia dell'hotel in home,
insieme alla colazione in veranda e al giardino. È il dato più concreto che il
vecchio sito aveva e questo non diceva.

Le visite per scolaresche restano fuori, per scelta.

⚠️ **`--gold-testo` era tarato su UN solo fondo.** #846934 passa su crema (4,72)
ma **non** sul fondo caldo della sezione Territorio (**4,25**), dove è finito «I
sentieri dimenticati». Portato a **#7d6331**: 5,17 su crema · 4,65 sul caldo ·
5,67 su bianco. E la barra in alto da `rgba(…,.92)` a `.97`, perché la foto che
traspariva scuriva il pulsante della lingua attiva (4,39).

📐 **Stessa lezione del 06/08, in un'altra veste:** un colore va misurato su
**tutti** i fondi su cui compare davvero, non su quello principale.


### «Come arrivare» trovabile davvero, e le carte in cima attivate
Nasce dalla domanda «dove l'hai messa?»: se la chiede chi l'ha commissionata,
un ospite non la trova mai. Era al **94% della pagina**, in fondo a Contatti.

1. **Risalita** dentro Contatti: ora è la prima cosa della sezione, sopra
   l'indirizzo e la mappa. **88%** invece di 94 — sempre in fondo alla pagina,
   ma ora è il primo elemento della sezione anziché l'ultimo.
2. **Nel menu**, nona voce dopo Contatti — e quindi anche nel pannello del
   telefono, che legge le voci da lì.
3. **Su tutte e nove le pagine** di camere e appartamenti, in fondo alla colonna
   del testo: chiusa 67px, aperta 569. Nessuna traduzione nuova: i frammenti
   sono identici, e l'impronta è la stessa.
4. **Le carte in cima alla sezione sono attive**: 📍 Dove siamo apre la mappa,
   🚗 Come arrivare porta alla scheda, 📞 Contatti ha il numero che si chiama e
   la mail che si apre. Erano quattro riquadri di sola lettura.

⚠️ **Nove voci nel menu non ci stavano:** chiedono **1517px** di barra, e fra
1000 e 1280 andavano a capo spingendo «Prenota» **fuori dallo schermo**.
Sotto i **1300** si passa al pulsante del menu (prima era 900); fra 1300 e 1500
la barra si stringe. Provato a 390, 900, 1200, 1299, 1301, 1366, 1440, 1500,
1600: una riga sola, niente che esce.

📐 **Due regole morte scoperte e tolte**, invece di lasciarle a mentire: quella
che nascondeva la scritta accanto al marchio (battuta dallo `style` sul tag) e
`.cinfo-label` che nelle pagine camera **non esiste** — la targhetta usciva in
grande, come un titolo qualunque. Copiata la regola vera dalla home. ⚠️ La prima
estrazione aveva preso per sbaglio una regola di `:hover` con lo stesso nome.


### Le tre contraddizioni, chiuse
Risposte del gestore, applicate in tutte e cinque le lingue.

| | prima | ora |
|---|---|---|
| camere | il testo diceva «minibar», i servizi «frigo vuoto» | **frigo vuoto** ovunque |
| Clementina | scheda «vista lago», pagina «vista sulle montagne» | **il lago e le montagne** |
| Bergamotto | «4 ospiti max», ma il testo descrive 3 posti letto | **3** (scheda, capienza, mappa) |

⚠️ **Trovato mentre correggevo:** Pomelo era l'unico appartamento con la
targhetta «🍷 Minibar» — ma ha la cucina, come gli altri quattro che dicono
«Frigorifero». Allineato.

📐 **Cambiare un testo italiano scollega la sua traduzione**: l'impronta è
calcolata sul testo, quindi cambiarlo crea una chiave nuova e le quattro lingue
restano sulla vecchia. Vanno riagganciate a mano. ⚠️ Due volte ho corretto la
**chiave sbagliata**: nel dizionario convivevano vecchia e nuova versione, e
`[0]` era quella morta. Il segnale è che il sito non cambia pur dicendo
«sostituita».

⚠️ **E il materiale dell'assistente va rigenerato**: `kb.json` continuava a dire
«minibar» dopo che il sito non lo diceva più — l'assistente avrebbe ripetuto
l'errore appena corretto. `strumenti/kb.py` ora accetta `NODE_PLAYWRIGHT` per
trovare Playwright (per i moduli ES conta **dove sta il file**, non da dove lo
lanci: `NODE_PATH` non serve a niente).

**Dopo aver toccato un testo del sito, l'ordine è:**
`marca.py` → `raccogli.py` → riaggancio traduzioni → `costruisci.py` → `kb.py`.


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
