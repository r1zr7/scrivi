# Registro della revisione visiva

Autore: Alessandro Resch. Data: 27 ottobre 2026.

## Primo controllo: caron laterali

I campioni ď, Ľ, ľ e ť, isolati e con lettere successive, sono stati esaminati
su immagini grandi e piccole inviate dall'autore. Separazione, appartenenza del
segno e distanze non mostrano anomalie evidenti nei campioni. Controllo manuale
ritenuto soddisfacente. FontBakery mantiene alt_caron perché i glifi hanno
contorni autonomi, che il controllo non sa valutare automaticamente.
Le forme approvate non sono cambiate nella revisione 1.001.

## Secondo controllo: numero dei contorni

Le immagini della 1.000 hanno mostrato tre problemi da correggere: l'accento di ĺ
unito all'asta, le virgole inferiori di Ș/ș attaccate alla lettera e il cerchio
puntinato troppo debole alla dimensione piccola. @ e § non mostrano anomalie
evidenti nei campioni esaminati.

Nella 1.001:
- ĺ presenta due contorni distinti, distanza minima 66,94 unità font.
- Ș e ș presentano due contorni distinti, distanza minima rispettivamente 48,00 e 49,01 unità.
- La correzione al segno condiviso U+0326 si applica anche a Ț e ț, conservando
  il corretto comportamento delle sequenze decomposte.
- ◌ presenta 12 punti distinti, con diametro minimo 43 unità font.
- Tutte le larghezze di avanzamento e tutti i codepoint della 1.000 sono conservati.

Il dettaglio numerico è in contour-review.json. Il confronto prima/dopo a 120 e
24 px è in specimen/contorni-prima-dopo.png. L'autore ha approvato i nuovi campioni grandi e piccoli della 1.001 nelle immagini
inviate successivamente alla correzione. Questa nota non equivale a certificazione linguistica.

Il WARN contour_count rimane per @, § e U+00AD, ma non segnala più ĺ, Ș, ș o ◌.
Il trattino discrezionale non è stato modificato; l’esito della prova è riportato sotto.
I segni quasi verticali, i sottoinsiemi Google, l'ARTICLE e il vendor ID sono ancora
aperti; non sono stati dichiarati risolti da queste modifiche.

## Terzo controllo: U+00AD

Le schermate grandi e piccole della prova dedicata con AR Scrittura 1.001 mostrano:
nessun segno o spazio aggiuntivo nella parola intera; trattino corretto a fine riga
quando si spezza sempli-cità; nessun carattere sostitutivo. Comportamento ritenuto
soddisfacente nel browser utilizzato dall’autore. Non si estende questa conclusione
a tutte le applicazioni. Il WARN resta perché il carattere è presente nel font.
Il relativo glifo e le sue metriche sono invariati nella 1.002.

## Quarto controllo: tratti quasi verticali e forme particolari

I campioni grandi e piccoli delle lettere di base e dei simboli non mostrano
scalini o discontinuità accidentali evidenti. Le leggere inclinazioni sono coerenti
con il disegno manoscritto. I campioni particolari non mostrano anomalie evidenti
in barre, Œ, frazione, apice e trattini.

Sono emersi due glifi semanticamente troppo semplificati: ſ duplicava f e ĸ
duplicava k con l’ascendente. Nella 1.002 sono stati ridisegnati: ſ senza traversa
completa, ĸ con asta all’altezza delle minuscole. Il confronto prima/dopo è in
specimen/speciali-prima-dopo.png. Il test special-forms-review.json conferma che
sono cambiati solo questi due contorni, con advance, GPOS, GSUB e GDEF invariati.

Le nuove forme ſ/ĸ sono state approvate dall’autore nei campioni grandi e piccoli. Questo registro non
dichiara completata la revisione di tutte le 97 varianti codificate segnalate
nel dettaglio integrale di outline_semi_vertical.

## Accenti: revisione del 28 ottobre 2026

Autore: Alessandro Resch.
Le immagini grandi e piccole delle vocali accentate non mostrano anomalie evidenti.
Nei successivi campioni delle consonanti, gli accenti di ĥ, ȟ e ǩ risultavano
accanto alle aste, troppo bassi. Nella 1.003 sono stati alzati sopra le aste,
con separazione verticale minima di 65 unità font. Sono cambiati solo questi tre
contorni codificati; larghezze, GSUB e GDEF sono invariati dalla 1.002. GPOS è
aggiornato per gli accenti combinanti sopra h/k e relative varianti accentate;
il posizionamento corretto su l è conservato. I controlli sui binari compilati
sono in tall-accents-review.json. Il confronto è in specimen/accenti-alti-prima-dopo.png.
Le nuove immagini grandi e piccole inviate dall’autore il 28 ottobre mostrano
accenti separati e riconoscibili; le sequenze combinanti sono visivamente coerenti
con le precomposte. Correzione visiva della 1.003 ritenuta soddisfacente.
Gli altri campioni di consonanti esaminati non mostrano anomalie evidenti.
Questo controllo non costituisce una certificazione linguistica o l’ammissione
ai cataloghi. Gli altri WARN e requisiti di pubblicazione rimangono aperti.

## Rinomina in Scrivi — 2 novembre 2026

Autore: Alessandro Resch. Famiglia approvata: Scrivi.
La 1.004 conserva tutti i contorni, le metriche e le tabelle di shaping della
1.003, come verificato da rename-review.json. Le prove visive precedenti restano
quindi pertinenti. La rinomina non dichiara completata una revisione di ogni
possibile sequenza né l’ammissione a Google Fonts.
