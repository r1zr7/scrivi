# Pubblicazione di Scrivi

Autore: Alessandro Resch. 2 novembre 2026. Versione font 1.004.

Nome famiglia/menu/CSS: **Scrivi**. PostScript: **Scrivi-Regular**.
Repository: https://github.com/r1zr7/scrivi
Richiesta esistente: https://github.com/google/fonts/issues/11207

Il repository è stato rinominato da ar-scrittura. Il copyright del font e la prima
riga di OFL.txt ora contengono l’URL reale del repository. File TTF/WOFF2, UFO,
script, anteprima e pagina di download usano Scrivi. I materiali storici sono
isolati in documentation/history, e la cronologia Git conserva le vecchie release.

## Controlli completati

- make check: 604 asserzioni di rilascio e ricompilazione riproducibile passate.
- Confronto binario con 1.003: contorni, cmap, larghezze, metriche, GPOS, GSUB,
  GDEF e programma di hinting invariati. Rinominati metadati e URL.
- FontBakery Google Fonts: 113 PASS, 0 FAIL/ERROR/FATAL, 6 WARN, 7 INFO, 110 SKIP.
- FontBakery Universal: 80 PASS, 0 FAIL/ERROR/FATAL, 3 WARN, 3 INFO, 41 SKIP.
- Articolo, immagine e relativo controllo passati. Report integrali in qa/.
- Nome Scrivi verificato su fontdata: nessuna corrispondenza esatta il 2 novembre.
- Layout essenziale upstream: fonts/ttf, fonts/webfonts, sources/UFO/build.sh,
  documentazione e articolo, requirements alla radice, autori e licenza.

La guida ammette build.sh in alternativa a config.yaml e non impone i workflow
esatti del project-template. Il Makefile è incluso come comodo ingresso.

## Punti ancora aperti

I sei WARN sono riportati integralmente e commentati in qa/WARN-REVIEW.txt.
Non sono stati soppressi. SKIP non significa PASS. L’ammissione richiede ancora
la valutazione del team, l’accordo sui sottoinsiemi e le decisioni editoriali,
compresa la convenzione per una famiglia a singolo peso. Nessun suffisso One è
stato aggiunto al nome approvato senza indicazioni del team.

La checklist ufficiale è ripristinata integralmente in submission/CHECKLIST.md.
Tutte le dichiarazioni personali della checklist sono state confermate
esplicitamente da Alessandro Resch il 2 novembre 2026: assenza di versioni retail
più grandi, titolarità, lettura e adesione ai requisiti e impegno alla manutenzione. Il CLA va letto e firmato personalmente; nessuna firma è stata
eseguita né dichiarata da questo lavoro.

## Licenze

Font e software sorgente: OFL 1.1 senza Reserved Font Name.
Nuova immagine promozionale: CC BY-SA 4.0, dettagli in documentation/image-license.txt.
Nessun monogramma AR riservato incluso. Assistenza AI dichiarata nel README.

## Sito proprio

Scrivi.html incorpora il WOFF2 e contiene il link a Scrivi-1.004-Pubblico.zip.
Caricare i due file nella stessa cartella del sito. Il pacchetto non è un tema
WordPress. Il vecchio AR-Tema non viene aggiornato da questa release del font.

Fonti ufficiali:
https://googlefonts.github.io/gf-guide/upstream.html
https://googlefonts.github.io/gf-guide/onboarding.html
https://googlefonts.github.io/gf-guide/article.html
https://namecheck.fontdata.com/?q=Scrivi

Aggiornamento del 2 novembre 2026: checklist ufficiale interamente confermata dall’autore. CLA personale in compilazione; firma non ancora confermata. Restano la revisione Google e i WARN tecnici già documentati.
