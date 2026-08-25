# -*- coding: utf-8 -*-
"""Le domande della reception. UNA fonte sola: da qui nascono sia il testo
   visibile sia il JSON-LD, cosi' non possono dire due cose diverse."""

GRUPPI = [
 ("La strada e l'arrivo", "Dove siamo davvero, e come ci si arriva senza sorprese.", [

  ("Dove si trova esattamente il Prà de la Fam?",
   ["Siamo in Via Gardesana 7, al Porto di Tignale, 25080 Tignale (BS): sponda bresciana del Lago di Garda, sulla strada che collega Gargnano a Riva del Garda. La struttura è direttamente a lago — la spiaggia è a meno di venti metri dal giardino.",
    "C'è una cosa che confonde quasi tutti, ed è meglio saperla prima di partire: il paese di Tignale sta in alto, sulla montagna, a qualche chilometro di tornanti dalla riva. Noi siamo giù, sul lago, sulla Gardesana. Le coordinate esatte sono 45°43.684′N · 10°43.176′E."]),

  ("Che cosa devo scrivere nel navigatore per arrivare?",
   ["Scrivete «Prà de la Fam» oppure «Porto di Tignale». Non scrivete solo «Tignale»: il navigatore vi porta in paese, in cima alla montagna, e da lì dovete riscendere.",
    "Se preferite andare sul sicuro, impostate direttamente le coordinate 45°43.684′N · 10°43.176′E, o aprite la nostra posizione su Google Maps dalla pagina dei contatti."]),

  ("Come si arriva in auto?",
   ["Da est: autostrada A4, uscita Desenzano, direzione Salò, circa 15 km. Da Salò si prosegue verso Riva del Garda sulla Gardesana, la SS 45 bis; passata Gargnano, ancora 4 km fino al Porto di Tignale.",
    "Da ovest: autostrada A4, uscita Brescia Est, direzione Salò, circa 20 km, e poi come sopra.",
    "Da nord: autostrada del Brennero A22, uscita Rovereto Sud, direzione Riva del Garda, quindi Gardesana verso Brescia per una ventina di chilometri. L'ingresso è sulla Gardesana stessa, con il parcheggio davanti: non c'è nessuna strada di montagna da fare all'ultimo momento."]),

  ("Com'è la strada? Ho letto che è stretta e piena di gallerie.",
   ["È vero, ed è anche il motivo per cui vale il viaggio. La Gardesana Occidentale è scavata nella roccia a picco sul lago: stretta, con molte gallerie, alcune delle quali si aprono sull'acqua. È una delle strade più panoramiche d'Italia.",
    "Si percorre normalmente in auto, in moto e in camper — ci passano i pullman di linea tutti i giorni — a patto di andare piano e di non avere fretta negli incroci in galleria. Il consiglio che diamo a tutti è di calcolare mezz'ora in più e di fermarsi in una delle piazzole: dall'alto si vede tutto il lago.",
    "L'ultimo tratto prima di noi è in galleria: l'ingresso del Prà de la Fam arriva subito dopo, sulla destra se venite da Gargnano."]),

  ("C'è il parcheggio? Si paga?",
   ["Sì, il parcheggio è privato, gratuito e riservato a chi soggiorna, subito davanti alla struttura. È chiuso, quindi va bene anche per le moto — è una delle cose che i motociclisti ci scrivono più spesso nelle recensioni.",
    "Non serve prenotarlo né segnalarlo in anticipo: c'è posto per tutti gli ospiti."]),

  ("Si può arrivare senza auto, in treno o in aereo?",
   ["Sì. Le stazioni comode sono Brescia e Desenzano–Sirmione, sulla linea Milano–Venezia; da lì partono gli autobus che percorrono la Gardesana, più frequenti da Brescia e più radi da Desenzano. Si scende alla fermata «Porto di Tignale», che è davanti a noi.",
    "Arrivando da nord: stazione di Rovereto, autobus fino a Riva del Garda e da lì la linea per Gargnano.",
    "Gli aeroporti, dal più vicino al più lontano: Brescia Montichiari, Verona Villafranca, Bergamo Orio al Serio, Milano Linate, Venezia e Milano Malpensa, tutti collegati in treno o in autobus con Brescia, Desenzano e Verona.",
    "Una volta qui si sta benissimo anche senza macchina: spiaggia, limonaia e sentieri partono dalla porta. Per girare gli altri paesi del lago, però, l'auto o il battello aiutano."]),
 ]),

 ("La posizione e la limonaia", "Che cosa si vede da qui, e che cos'è quella limonaia.", [

  ("Che cos'è la Limonaia del Prà de la Fam? Si può visitare?",
   ["È la limonaia più grande e la più a nord d'Europa, e sta dentro la nostra proprietà: dalla camera ci si arriva a piedi in un minuto. Non è un rudere e non è una ricostruzione — le ottanta piante adulte sono vive e in produzione.",
    "Fu restaurata nel 1985 con l'intervento della Comunità Montana del Parco Alto Garda Bresciano e oggi è un Ecomuseo, visitabile da Pasqua a ottobre. La proprietà è rimasta della famiglia Parisini, la stessa che gestisce l'albergo.",
    "La visita è guidata e racconta come funzionavano le limonaie del Garda: i pilastri di pietra, le assi che d'inverno chiudevano la serra, il commercio dei limoni verso il Nord Europa. Alla fine c'è la degustazione dei prodotti che nascono qui: limoni sotto sale, limoncino, sciroppo di limone e olio agrumato. Orari e informazioni sul sito dedicato, ecomuseopradelafam.com."]),

  ("Che differenza c'è fra la vostra limonaia e le altre del Lago di Garda?",
   ["Sul Garda le limonaie storiche sono molte, ma quasi tutte sono strutture vuote: restano i pilastri e i muri, non le piante. La nostra è ancora coltivata, ed è la più grande e la più settentrionale d'Europa — cresce esattamente al limite climatico oltre il quale un limone all'aperto non ce la fa più.",
    "Per chi soggiorna qui la differenza pratica è semplice: la limonaia non è una gita da programmare, è il giardino di fianco alla camera. E i cinque appartamenti sono ricavati proprio nella vecchia limonaia, tanto che portano il nome di un agrume: Clementina, Calamondino, Kumquat, Pomelo, Bergamotto."]),

  ("Si può fare il bagno? Com'è la spiaggia?",
   ["Sì. La spiaggia è a meno di venti metri dal giardino, si attraversa il prato e si è in acqua. È una piccola spiaggia libera, non un lido attrezzato: niente file di ombrelloni, niente cancelli.",
    "Il lago qui è pulito e profondo; la stagione del bagno va indicativamente da giugno a settembre. La mattina l'acqua è uno specchio, nel pomeriggio si alza il vento — è per questo che il tratto davanti a noi è frequentato da chi fa windsurf e kitesurf.",
    "Non abbiamo piscina, e non ci è mai mancata: qui si nuota nel lago."]),

  ("Che cosa si vede dalla struttura?",
   ["Davanti, il lago aperto e il Monte Baldo sulla sponda veronese: nelle giornate limpide la vista corre da Malcesine fino a Sirmione. Dietro, a pochi metri, si alza un muro di roccia con una cascata.",
    "Le camere hanno vista lago o vista montagna a seconda della posizione nella struttura; gli appartamenti guardano tutti il lago. La colazione si serve in veranda, all'ombra degli ulivi, con il lago davanti."]),

  ("Che cosa si può fare in zona?",
   ["Windsurf, kitesurf e vela: il vento del Garda è costante e regolare, e il Circolo Vela Gargnano organizza regate per tutta la stagione, compresa la storica Centomiglia.",
    "A piedi e in mountain bike si parte direttamente da qui: siamo dentro il Parco Alto Garda Bresciano, e oltre ai sentieri del parco c'è una rete fittissima di sentieri militari — trincee, ricoveri, gallerie e casematte — ormai spariti dalle carte, quasi sempre nei punti più panoramici.",
    "Poi canyoning nelle forre del Garda e della Valle di Ledro, arrampicata sulla parete dietro l'albergo, e il Golf Bogliaco, fondato nel 1912, terzo golf club d'Italia, fra Gargnano e Toscolano Maderno.",
    "Per le giornate tranquille: Gargnano a pochi chilometri, Limone sul Garda e Riva del Garda verso nord, il santuario di Montecastello sopra Tignale."]),
 ]),

 ("Camere, appartamenti e servizi", "Quello che si chiede al banco prima di prenotare.", [

  ("Meglio una camera d'albergo o un appartamento?",
   ["Dipende da quanto vi fermate e da quanto volete cucinare. Le camere sono dieci: Doppia Standard (18 m²), Doppia Economy (16 m²), Tripla (23 m²) e Familiare (29 m²), tutte con bagno privato, aria condizionata, Wi-Fi e colazione inclusa servita in veranda. È la scelta più semplice per due o tre notti.",
    "Gli appartamenti sono ricavati nella vecchia limonaia: Clementina, Calamondino, Kumquat e Pomelo sono da circa 35 m² per due persone, con cucina attrezzata o angolo cottura, spazio esterno e vista lago; Bergamotto è su due livelli, 65 m², ma al momento non è disponibile.",
    "In pratica: camera per un soggiorno breve e senza pensieri, appartamento per una settimana, per chi viaggia con bambini o per chi vuole farsi la spesa e cucinare."]),

  ("La colazione è inclusa?",
   ["Per chi dorme in camera sì, ed è compresa nel prezzo: si serve in veranda, all'ombra degli ulivi, con la vista sul lago.",
    "Per gli appartamenti no, perché hanno la cucina: chi vuole può però aggiungerla a pagamento. Basta dirlo quando si prenota, o anche il giorno prima alla reception."]),

  ("Si possono portare i cani?",
   ["Sì, i cani sono i benvenuti, sia nelle camere sia negli appartamenti. Il supplemento è di 10 € a notte per animale in albergo e di 50 € a soggiorno per animale negli appartamenti — non a notte: per l'intero soggiorno.",
    "Vi chiediamo solo di segnalarlo quando prenotate, così sappiamo assegnarvi la sistemazione più comoda. Intorno c'è il giardino, la spiaggia è libera e i sentieri del parco partono dalla porta: per un cane è un posto facile."]),

  ("A che ora si fa il check-in e il check-out?",
   ["Il check-in è dalle 14:00 alle 20:00, il check-out entro le 10:30.",
    "Se arrivate più tardi delle 20:00, chiamateci: la struttura è a gestione familiare e ci si organizza, basta saperlo prima. E se arrivate in anticipo, di solito potete già lasciare la macchina nel parcheggio e usare giardino e spiaggia mentre finiamo di preparare la camera."]),

  ("Che cosa c'è in camera?",
   ["Bagno privato con doccia, asciugacapelli, set di asciugamani, bagnoschiuma e kit cortesia; aria condizionata, Wi-Fi gratuito, televisione e un frigo vuoto a disposizione.",
    "Le finestre sono state rifatte tutte: dalla Gardesana, che passa qui davanti, in camera non entra rumore — è una delle cose che gli ospiti citano più spesso. La struttura è per non fumatori."]),

  ("Che lingue parlate?",
   ["Italiano, inglese, tedesco, francese e spagnolo, sia al banco sia su tutto il sito. La famiglia gestisce la struttura di persona: chi risponde al telefono è chi vi accoglierà all'arrivo."]),

  ("Come si prenota? Conviene prenotare dal sito?",
   ["Dal tasto «Prenota» del sito si apre il nostro motore di prenotazione, con la disponibilità in tempo reale e la conferma immediata. In alternativa si può telefonare allo (+39) 0365 799890 o scrivere a info@alpradelafam.com.",
    "Prenotando direttamente parlate con noi e non con un intermediario: le richieste particolari — il cane, la colazione in appartamento, l'arrivo tardi, la camera vicino al giardino — si risolvono in due righe di mail."]),

  ("Si possono comprare i vostri prodotti?",
   ["Sì. Olio extravergine biologico di spremitura a freddo, olio agrumato, limoni sotto sale con peperoncino o pepe, limoncino senza coloranti né conservanti, sciroppo di limone e marmellate biologiche di limone e arance amare, insieme all'abbigliamento e agli accessori con il logo del Prà.",
    "Si acquistano in hotel durante il soggiorno; la vetrina con tutti i prodotti è su pradelafam.shop."]),
 ]),
]
