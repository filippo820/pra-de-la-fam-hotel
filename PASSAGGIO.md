# Il giorno dello scambio — istruzioni per esteso

Scritto il 19 agosto 2026. Riguarda solo il momento in cui `alpradelafam.com`
smette di puntare al vecchio WordPress e comincia a puntare al sito nuovo.

---

## Prima di tutto: cos'è il DNS, e perché è l'unica cosa che conta qui

Il **dominio** (`alpradelafam.com`) e il **sito** sono due cose separate. Il
dominio è solo un elenco di indicazioni: «chi cerca `www.alpradelafam.com`
vada a questo indirizzo», «chi manda una mail a `@alpradelafam.com` la
consegni a quest'altro». Quelle indicazioni si chiamano **record DNS** e oggi
stanno tutte su Aruba.

Cambiare sito **non** vuol dire spostare il dominio: vuol dire cambiare **una
sola indicazione** dentro quell'elenco, lasciando ferme tutte le altre.
È per questo che il passaggio è reversibile in un'ora.

## Cosa c'è oggi, davvero

Letto dai server di Aruba il 19 agosto 2026:

| nome | tipo | valore | a cosa serve |
|---|---|---|---|
| `alpradelafam.com` | A | `89.46.109.26` | **il sito** (hosting Aruba) — TTL 3600 |
| `www.alpradelafam.com` | A | `89.46.109.26` | **il sito** con il www — TTL ~900 |
| `alpradelafam.com` | MX | `10 mx.alpradelafam.com` | **dove vanno le mail in arrivo** |
| `mx` | A | 8 indirizzi `62.149.128.x` | i server di posta Aruba |
| `mail` | A | 7 indirizzi `62.149.128.x` | posta in uscita |
| `webmail` | A | `62.149.158.91/92` | la webmail |
| `ftp` | A | `89.46.104.211/218` | l'accesso ai file |
| `alpradelafam.com` | TXT | `v=spf1 include:_spf.aruba.it ~all` | dice al mondo che le mail partono da Aruba: **senza, finiscono nello spam** |

**Le prime due righe sono il sito. Tutto il resto è la posta e i servizi.**
Del sito ci occupiamo; il resto non si tocca.

## ⚠️ Perché NON si spostano i nameserver

Netlify propone anche di gestire lui il dominio («Netlify DNS»): si cambiano i
**nameserver** e si consegna a Netlify l'elenco intero.

**Non farlo.** Consegnare l'elenco vuol dire ricominciarlo da zero: quelle otto
righe di posta là sopra — MX, `mx`, `mail`, `webmail`, SPF — non si copiano da
sole. Se manca l'MX, `info@alpradelafam.com` **smette di ricevere** e chi
scrive si prende un errore di consegna; se manca l'SPF, quello che mandi tu
finisce nello spam. Sono guasti che si notano ore dopo, quando una prenotazione
è già andata persa.

Restando su Aruba si cambiano **due righe su nove** e le altre sette non le
sfiora nessuno.

---

## Le mosse, nell'ordine

L'ordine non è estetico: ogni passo prepara il seguente. In particolare
**il sito va dichiarato su Netlify PRIMA di cambiare il DNS**, altrimenti nel
frattempo il certificato HTTPS non esiste e chi arriva vede l'avviso rosso
«sito non sicuro».

### 1 · Pubblicare l'archivio

Questo passo **non può rompere niente**: crea un sito nuovo su un indirizzo che
oggi non esiste. Il sito vero non viene sfiorato. Sono cinque minuti.

#### 1.1 — Cosa si carica

Non la cartella: **il file `vecchio-congelato.zip`**, in
`~/Documents/Fam_S.r.l./Sito Prà/` (28 MB, 617 file).

⚠️ **Non trascinare la cartella.** Dentro c'è `.git`, cioè la cronologia
completa del repository: caricandola finirebbe su un server pubblico. Lo zip
contiene solo il sito — l'ho fatto togliendo `.git`, `README.md` e i
`.DS_Store`, e verificato che dentro non ci sia nessun file nascosto.

Netlify accetta lo zip esattamente come una cartella, e i file stanno alla
radice (`_redirects`, `it_IT/`, `de_DE/`, `fr_FR/`, `en_GB/`) — che è la
condizione perché funzioni.

#### 1.2 — Caricarlo

Netlify → **Add new site** → **Deploy manually** → trascina lo zip nel
riquadro. Finito il caricamento il sito è già online.

#### 1.3 — Dargli un nome sensato

Netlify gliene assegna uno a caso (`sereno-pastello-12345`). Cambialo:
**Site configuration → Site details → Change site name** → `pradelafam-archivio`.

Non è pignoleria: quel nome diventa il valore da scrivere su Aruba al passo
1.5, e fra sei mesi `pradelafam-archivio.netlify.app` si capisce da solo,
mentre `sereno-pastello-12345` no.

#### 1.4 — Provarlo PRIMA di toccare il DNS

Apri `https://pradelafam-archivio.netlify.app`. Devi vedere:

- la **striscia scura in cima**: «Questa è una copia d'archivio del sito
  precedente. → Vai al sito di Prà de la Fam»;
- sotto, il vecchio sito com'era, con le foto;
- in fondo alla pagina Contatti, al posto del modulo, l'indirizzo mail e il
  telefono.

Se qui è tutto a posto, il resto è solo indirizzamento. Se qualcosa manca,
si sistema adesso, con calma, senza che nessuno stia guardando.

#### 1.5 — Collegargli l'indirizzo definitivo

Nel sito appena creato: **Domain management → Add a domain** →
`vecchio.alpradelafam.com`.

Netlify dirà che il DNS non punta ancora a lui. È **giusto**: gli stiamo
dicendo in anticipo «fra poco arriveranno visite per questo nome». Senza
questo avviso non emetterebbe il certificato HTTPS.

Poi Aruba → dominio `alpradelafam.com` → **Gestione DNS** → **aggiungi** un
record (non modificarne nessuno):

| campo | valore |
|---|---|
| Tipo | **CNAME** |
| Nome / Host | `vecchio` |
| Valore / Destinazione | `pradelafam-archivio.netlify.app.` |
| TTL | quello proposto va bene |

Il punto finale dopo `.app` mettilo se Aruba lo accetta; se lo rifiuta,
scrivilo senza.

#### 1.6 — Verificare

Dopo qualche minuto:

```bash
dig +short vecchio.alpradelafam.com     # deve arrivare a Netlify
curl -sI https://vecchio.alpradelafam.com | head -3
```

e apri `https://vecchio.alpradelafam.com` nel browser: stessa pagina del punto
1.4, ma con il lucchetto e l'indirizzo giusto.

#### 1.7 — Se qualcosa non torna

| cosa vedi | cosa vuol dire |
|---|---|
| Aruba rifiuta il punto finale | scrivilo senza: `pradelafam-archivio.netlify.app` |
| Aruba non fa scegliere «CNAME» | sei nella pagina sbagliata: serve **Gestione DNS / Record DNS**, non «Nameserver» |
| `dig` non risponde ancora | è presto: i record nuovi si vedono in pochi minuti, ma possono volerci fino a un'ora |
| il browser dice «non sicuro» | il certificato non è ancora emesso: aspetta, poi Netlify → Domain management → **Verify DNS configuration** |
| Netlify dice «check DNS configuration» | il CNAME non è arrivato o è scritto storto: ricontrolla che il Nome sia `vecchio` e non `vecchio.alpradelafam.com` (alcuni pannelli aggiungono il dominio da soli, e verrebbe `vecchio.alpradelafam.com.alpradelafam.com`) |

⚠️ **Il record si AGGIUNGE, non si modifica.** Se ti trovi a cambiare il valore
di una riga che c'era già, fermati: quella è la riga di qualcos'altro.

**Da qui in poi l'archivio è al sicuro**, indipendentemente da quello che
succede al vecchio hosting. Solo adesso ha senso passare al punto 2.

### 2 · Dichiarare il dominio sul sito nuovo (ancora nessun effetto)

Netlify → sito `pradelafam` → **Domain management → Add a domain** →
`alpradelafam.com`. Netlify aggiunge da sé anche `www.alpradelafam.com`.

Dirà «Awaiting external DNS» o simile. **È giusto così**: gli stiamo dicendo in
anticipo «fra poco arriveranno visite per questo nome, preparati». Il traffico
continua ad andare sul vecchio finché non tocchiamo Aruba.

### 3 · Le due righe da cambiare su Aruba

#### Dove si va

**La stessa pagina dove hai aggiunto `vecchio`.** Da lì è uscita la riga di
storico «19/08/2026 20:44:30 — Aggiunta record CNAME — vecchio».

Il percorso, se serve rifarlo da zero:
`admin.aruba.it` → accedi → **Domini** / «I tuoi domini» → `alpradelafam.com`
→ **Gestione DNS** (a volte «DNS e Server DNS» → «Gestione record DNS»).

⚠️ **Non** la pagina dei **Server DNS / Nameserver**: lì si cambia *chi* tiene
l'elenco, ed è la cosa che non va toccata mai. Se la pagina giusta è aperta,
vedi una **tabella di righe** con Tipo / Nome / Valore / TTL.

#### Cosa vedrai nella tabella, e cosa NON si tocca

| nome | tipo | oggi | |
|---|---|---|---|
| *(vuoto o `@`)* | A | `89.46.109.26` | ← **da cambiare** |
| `www` | A | `89.46.109.26` | ← **da cambiare** |
| `vecchio` | CNAME | `pradelafam-archivio.netlify.app.` | fatto ieri, lascia |
| `mx` `mail` `smtp` `pop3` `imap` `webmail` `autoconfig` | A / CNAME | server Aruba | **la posta — non toccare** |
| `ftp` | A | `89.46.104.x` | non toccare |
| *(dominio)* | MX | `10 mx.alpradelafam.com` | **non toccare** |
| *(dominio)* | TXT | `v=spf1 include:_spf.aruba.it ~all` | **non toccare** |

**Undici righe: due si cambiano, nove restano.** Se ti ritrovi a modificare una
riga che contiene `62.149.` o `mx`, fermati: quella è la posta.

#### Le due modifiche

**Riga 1 — il dominio nudo.** Nella tabella il campo Nome è **vuoto** oppure `@`
oppure mostra `alpradelafam.com`. Si modifica **solo il valore**:

```
tipo A   ·   89.46.109.26   →   75.2.60.5
```

Il tipo resta `A`. ⓘ Sul nome nudo le regole del DNS non permettono un CNAME:
per forza un numero. È l'indirizzo d'ingresso di Netlify — lo stesso che hai
già su `colgo.app`.

**Riga 2 — `www`.** Qui cambia anche il **tipo**, da `A` a `CNAME`:

```
tipo A      · www · 89.46.109.26
tipo CNAME  · www · pradelafam.netlify.app.
```

⚠️ **Molti pannelli non lasciano cambiare il tipo di una riga esistente.** In
quel caso: **elimina** la riga `www` di tipo A e **aggiungine** una nuova di
tipo CNAME. Non è pericoloso — è il nome che stiamo comunque spostando.

Se il pannello complica troppo la vita, **c'è un ripiego che funziona**:
lasciare `www` di tipo **A** e cambiargli solo il valore in `75.2.60.5`, come
il nome nudo. Netlify risponde lo stesso, perché riconosce il sito dal nome
chiesto e non dall'indirizzo. È meno elegante — il giorno che Netlify cambia
numero, il CNAME si aggiornerebbe da solo e l'A no — ma è corretto.

#### Salva, e poi aspetta

Salva **tutte e due** nella stessa sessione. Nel mezzo, per qualche minuto, uno
dei due nomi può mostrare il sito nuovo e l'altro il vecchio: nessun danno,
sono due nomi indipendenti.

⏱️ **Aruba mette in coda.** Ieri sera ci ha messo **58 minuti**: mettili in
conto e non rifare il record perché «non si vede» — creeresti un doppione.
Il TTL minimo che il pannello concede è 1 ora, quindi anche il ritorno
indietro, se serve, richiede fino a un'ora.

### 4 · Aspettare, e guardare

I TTL misurati sono **3600 secondi sul nome nudo** e **~900 sul www**: in
pratica entro un'ora tutti vedono il nuovo, molti nel giro di minuti.

Da terminale, per vedere dove punta adesso:

```bash
dig +short alpradelafam.com A          # deve dire 75.2.60.5
dig +short www.alpradelafam.com        # deve arrivare a Netlify
curl -sI https://alpradelafam.com | grep -i server   # deve dire Netlify
```

Il **certificato HTTPS** lo emette Netlify da solo quando vede il DNS
arrivato: di solito pochi minuti. Se dopo mezz'ora il lucchetto non c'è,
Domain management → **Verify DNS configuration / Renew certificate**.

### 5 · Solo adesso: togliere il `noindex` e correggere i `canonical`

Questi due sono dentro le pagine, non nel DNS. Oggi dicono a Google due cose
che dal momento dello scambio diventano sbagliate e dannose:

- **`noindex`** = «non mettermi nei risultati». Ce l'ho messo io il 19 agosto
  perché finché il sito ufficiale è il vecchio, un secondo sito con lo stesso
  contenuto gli ruba posizioni. **Dopo lo scambio, lasciarlo vuol dire che il
  sito ufficiale sparisce da Google.** È il danno peggiore di tutta l'operazione,
  ed è silenzioso: il sito funziona benissimo, semplicemente nessuno lo trova.
- **`canonical`** = «l'indirizzo buono di questa pagina è quello lì». Oggi
  puntano a `pradelafam.netlify.app`. Se restano così, Google consolida tutto
  su un indirizzo che nessuno digita — e che porta il `noindex`.

Sono due sostituzioni meccaniche su 12 file: `pdlf-passaggio` trova i primi,
`rel="canonical"` i secondi. **Dimmelo e li faccio io in cinque minuti**, così
sono verificati e pubblicati in un colpo solo.

Fatto questo, `pradelafam.netlify.app` resta raggiungibile ma i `canonical`
diranno che l'originale è `alpradelafam.com`: è esattamente il meccanismo
inventato per due indirizzi che mostrano la stessa cosa.

### 6 · Le rifiniture, in giornata o nei giorni dopo

- **Google Search Console**: aggiungi `alpradelafam.com`, manda la sitemap.
- Il link «← Torna al sito principale» della **bottega**.
- Un rimando discreto all'archivio nel piede del sito nuovo.
- La striscia dell'archivio punta già a `www.alpradelafam.com`, che da adesso
  **è** il sito nuovo: **non va toccata**, è già giusta.
- **Solo alla fine, e senza fretta**: disdire l'hosting WordPress su Aruba.
  ⚠️ Attenzione: su Aruba **posta e hosting sono servizi distinti** — verifica
  di disdire l'hosting e non la casella, o perdi `info@alpradelafam.com`.

---

## Se qualcosa va storto

**Si torna indietro rimettendo le due righe com'erano**: A `89.46.109.26` sul
nome nudo e su `www`. Entro un'ora si è di nuovo sul vecchio, che nel frattempo
è rimasto acceso e intatto. Niente di questo passaggio cancella qualcosa.

**Le mail non c'entrano mai.** Se dopo lo scambio una mail non arriva, il
problema non è lo scambio: quei record non sono stati toccati. Controlla prima
il pannello della posta.
