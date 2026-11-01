# Pubblicazione di AR Scrittura

Autore: Alessandro Resch. Aggiornato il 29 ottobre 2026.

Nome definitivo della famiglia approvato dall'autore: **AR Scrittura**.
File desktop canonico: `fonts/ARScrittura-Regular.ttf`.
Nome CSS: `'AR Scrittura'`. La presentazione del progetto può usare AR-Scrittura.

Questo pacchetto 1.003 corregge gli accenti sopra le aste di ĥ, ȟ e ǩ,
con posizionamento coerente degli accenti combinanti su h/k/l.
Non rappresenta un'ammissione ai cataloghi.
Le verifiche sono documentate in README.md e nei report completi in qa/.
I binari conservano le correzioni a ĺ, Ș/ș, Ț/ț, virgola combinante e cerchio puntinato
e aggiungono le nuove forme di ſ e ĸ, senza modificarne le larghezze.
Spaziature e caron laterali approvati restano invariati. Vedere qa/REVISIONE-VISIVA.md.

## Passaggi rimasti per Google Fonts

1. Il connettore GitHub ha verificato l'account `r1zr7`. La creazione del
   repository è rimasta sospesa: non è stata verificata una sessione browser
   autenticata e non esiste ancora un repository pubblico confermato.
2. Creare un repository pubblico, nome suggerito `ar-scrittura`, verificando che
   non esista già. Il contenuto di questo pacchetto è predisposto come sua radice.
3. Sostituire il sito di presentazione nel copyright/OFL/sorgente con l'URL reale
   del repository, come richiesto da Google. Ricompilare, incrementare la versione
   font se si pubblica una nuova revisione e rigenerare i report.
4. Alessandro Resch deve leggere e sottoscrivere personalmente il Google CLA.
   Nessuna firma o dichiarazione di avvenuta sottoscrizione è stata generata.
5. Presentare la proposta tramite il modulo ufficiale collegato dalla guida,
   discutendo iniziali AR, eventuale suffisso One per il singolo peso sottile,
   sottoinsiemi e metadati del catalogo. FontBakery include AR fra le eccezioni
   generiche agli acronimi; ciò non è una specifica approvazione di questo progetto.
6. Completare la revisione editoriale e tipografica richiesta dalla piattaforma.

## Avvisi residui di FontBakery

- alt_caron: i quattro glifi sono contorni autonomi, perciò il controllo automatico
  non li valuta; la tavola specimen/lingue-e-accenti.png mostra il caron laterale.
- contour_count: dopo le correzioni rimangono @, § e U+00AD. Le forme di @ e §
  non mostrano anomalie evidenti nei campioni esaminati; U+00AD è stato verificato nelle prove del browser inviate dall’autore, senza
  anomalie; il WARN sulla presenza del carattere rimane. Il WARN complessivo rimane, ma non segnala più ĺ, Ș/ș o ◌.
- soft_hyphen: U+00AD è conservato per compatibilità con il font già distribuito.
- outline_semi_vertical: lievi inclinazioni del disegno manoscritto conservate.
- metadata/unreachable_subsetting: concordare inclusioni e METADATA.pb con Google.
- vendor_id: ARSC è un ID tecnico proposto e non registrato presso Microsoft.
- article/images: bozza testuale in submission/article/ARTICLE.en_us.html; manca
  ancora il link al repository pubblico e il materiale deve essere valutato dal team.

I risultati SKIP non sono controlli superati. Alcuni richiedono metadati del
catalogo non ancora presenti o tecnologie non usate da questo font statico.
I report finali sono stati eseguiti senza --skip-network, con timeout di 5 secondi.

## Altre piattaforme

TTF, OFL, descrizione inglese e specimen sono pronti per FontSpace, dafont e per
la valutazione redazionale di Font Squirrel. Occorrono accesso autore, invio e
revisione previsti dalle singole piattaforme. Non è stato eseguito alcun invio.
L'OFL consente uso personale e commerciale: non presentare il font come riservato
all'uso personale. Il sito proprio e AR-Tema dovranno adottare coerentemente il
nome CSS AR Scrittura quando si aggiornerà il font distribuito.

## Fonti

https://googlefonts.github.io/gf-guide/onboarding.html
https://googlefonts.github.io/gf-guide/requirements.html
https://googlefonts.github.io/gf-guide/statics.html
https://googlefonts.github.io/gf-guide/license-file.html
https://cla.developers.google.com/

## Distribuzione autonoma

Il pacchetto pubblico 1.003 del 29 ottobre conserva i binari già verificati.
I materiali della candidatura sono bozze, separati in submission/; non sono
necessari per usare o ospitare il font completo. Le immagini finali grandi e
piccole della 1.003 hanno completato il controllo delle correzioni h/k.
Per i 15 codepoint esclusi dai sottoinsiemi consultare submission/SOTTOINSIEMI.txt.
La revisione visiva documentata riguarda i campioni esaminati, non ogni possibile
sequenza o applicazione. Non sono dichiarati risolti tutti i WARN.

## Aggiornamento 1 novembre 2026

Autore: Alessandro Resch.
Repository pubblico creato: https://github.com/r1zr7/ar-scrittura
Le indicazioni precedenti sulla creazione sospesa descrivono lo stato storico.
Importazione iniziale della 1.003, senza cambiare i binari. Il copyright/OFL
conserva quindi l’URL del sito già presente nella release. La modifica all’URL
richiederà una nuova versione del font, compilazione e verifica.
Non risultano ancora firmati il CLA o inviata la candidatura da questo progetto.
Il modello di candidatura attuale richiede di dichiarare l’assistenza AI.
Il nome AR Scrittura richiede discussione perché AR sono iniziali dell’autore.
