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

### 1 · Pubblicare l'archivio (nessun rischio: è tutto nuovo)

1. Netlify → **Add new site → Deploy manually** → trascina la cartella
   `~/Documents/Fam_S.r.l./Sito Prà/vecchio-congelato` (35 MB).
2. Netlify assegna un nome a caso, tipo `sereno-pastello-12345.netlify.app`.
   **Annotalo**, serve al punto 3.
3. Nel sito appena creato: **Domain management → Add a domain** →
   `vecchio.alpradelafam.com`. Netlify dirà che il DNS non punta ancora a lui:
   è normale, lo sistemiamo subito.
4. Aruba → pannello del dominio → **Gestione DNS** → aggiungi un record:

   | | |
   |---|---|
   | Tipo | **CNAME** |
   | Nome / Host | `vecchio` |
   | Valore | `sereno-pastello-12345.netlify.app.` *(il nome del punto 2)* |

   È un nome che oggi non esiste: **non può rompere niente.**
5. Aspetta qualche minuto e prova `https://vecchio.alpradelafam.com`.
   Deve aprirsi il vecchio sito con la striscia scura in cima.

**A questo punto l'archivio è al sicuro e il sito vero non è stato toccato.**

### 2 · Dichiarare il dominio sul sito nuovo (ancora nessun effetto)

Netlify → sito `pradelafam` → **Domain management → Add a domain** →
`alpradelafam.com`. Netlify aggiunge da sé anche `www.alpradelafam.com`.

Dirà «Awaiting external DNS» o simile. **È giusto così**: gli stiamo dicendo in
anticipo «fra poco arriveranno visite per questo nome, preparati». Il traffico
continua ad andare sul vecchio finché non tocchiamo Aruba.

### 3 · Le due righe da cambiare su Aruba

Aruba → dominio `alpradelafam.com` → **Gestione DNS**. Cambiano **due** record:

| nome | prima | dopo |
|---|---|---|
| `alpradelafam.com` (lascia il campo Nome **vuoto**, o `@`) | A `89.46.109.26` | **A `75.2.60.5`** |
| `www` | A `89.46.109.26` | **CNAME `pradelafam.netlify.app.`** |

Due note su cosa sono quei valori:

- **`75.2.60.5`** è l'indirizzo d'ingresso di Netlify. Non è «il nostro server»:
  è la porta da cui Netlify smista, e riconosce il sito dal nome che il
  visitatore ha chiesto — ecco perché il punto 2 va fatto prima.
  ⓘ Sul nome nudo, senza `www`, le regole del DNS non permettono un CNAME: si
  è costretti a scrivere un indirizzo numerico. È lo stesso che hai già fatto
  per `colgo.app`, che infatti punta a `75.2.60.5`.
- **`pradelafam.netlify.app.`** con il punto finale, se Aruba lo richiede. Per
  `www` si usa il nome e non il numero: se domani Netlify cambia indirizzo, il
  nome continua a funzionare da solo.

**Non toccare nient'altro.** MX, `mx`, `mail`, `webmail`, `ftp`, TXT/SPF
restano esattamente come sono.

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
