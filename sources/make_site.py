#!/usr/bin/env python3
"""Author: Alessandro Resch. SIL OFL 1.1. Build the offline public demo."""
from pathlib import Path
import base64,html,re
ROOT=Path(__file__).resolve().parents[1]
def main():
	s=(ROOT/'Anteprima.html').read_text()
	css=(ROOT/'web/scrivi.css').read_text()
	css=css.replace("url('../fonts/webfonts/Scrivi-Regular.woff2')","url('data:font/woff2;base64,"+base64.b64encode((ROOT/'fonts/webfonts/Scrivi-Regular.woff2').read_bytes()).decode()+"')")
	s=s.replace('<link rel="stylesheet" href="web/scrivi.css">','<style>\n'+css+'\n</style>')
	s=s.replace('<title>Scrivi · anteprima 1.004</title>','<title>Scrivi — Alessandro Resch</title>\n\t<meta name="author" content="Alessandro Resch">\n\t<meta name="description" content="Scrivi: un carattere manoscritto essenziale di Alessandro Resch. Provalo e scarica il font completo con licenza SIL Open Font License 1.1.">')
	s=s.replace('Un carattere sottile, semplice e con lettere separate. Famiglia approvata dall’autore: Scrivi. Candidato 1.004 con sorgenti UFO e compilazione riproducibile.','Un carattere manoscritto essenziale: lettere separate, tratto sottile e pochi riccioli. Per nomi, titoli e messaggi brevi, quando serve un segno personale senza appesantire la pagina.')
	s=s.replace('<section aria-labelledby="try-heading">','''<p class="download-row"><a class="download" href="Scrivi-1.004-Pubblico.zip" download>Scarica Scrivi 1.004</a><span>TTF, WOFF2, sorgenti e istruzioni · ZIP</span></p>
		<p>Un solo stile Regular, 392 caratteri, lettere latine accentate e segni combinanti. Font distribuito con licenza <a href="#licenza">SIL Open Font License 1.1</a>.</p>
		<section aria-labelledby="try-heading">''')
	a=s.index('<section aria-labelledby="brand-heading">');b=s.index('<footer>',a)
	s=s[:a]+'''<section aria-labelledby="about-heading"><h2 id="about-heading">Pochi segni, una voce personale</h2>
			<p>Scrivi nasce dal lavoro di Alessandro Resch su una scrittura semplice e personale. Le lettere usano pochi segni e decorazioni essenziali. Il tratto leggero è pensato per testi brevi; per interfacce e letture lunghe è preferibile un carattere adatto a quegli usi.</p>
			<p>Il download comprende il TTF da installare sul computer, il WOFF2 per il web, i sorgenti modificabili e un’anteprima utilizzabile anche offline.</p></section>
		<section id="licenza" aria-labelledby="license-heading"><h2 id="license-heading">Licenza e attribuzione</h2>
			<p>Autore e designer: <strong>Alessandro Resch</strong>. Font distribuito con licenza SIL Open Font License 1.1, senza Reserved Font Name.</p>
			<details><summary>Leggi la licenza completa</summary><pre class="license-text">'''+html.escape((ROOT/'OFL.txt').read_text())+'''</pre></details></section>
		'''+s[b:]
	a=s.index('<footer>');b=s.index('</footer>',a)+len('</footer>')
	s=s[:a]+'''<footer><p>Scrivi 1.004 · Alessandro Resch · 2026</p>
		<p>Il font è incorporato nella pagina. La prova non usa servizi esterni e il testo digitato non viene inviato a un server dalla pagina.</p>
		<p><a href="https://github.com/r1zr7/scrivi">Sorgenti su GitHub</a> · La candidatura a Google Fonts è in corso: il font non è ancora presente nel catalogo.</p></footer>'''+s[b:]
	s=s.replace('.meta {','''a {color:inherit;text-underline-offset:.18em;}
		.download-row {display:flex;align-items:center;gap:1rem;flex-wrap:wrap;margin:2rem 0 1rem;}
		.download {display:inline-block;padding:.8rem 1.2rem;background:var(--ink);color:var(--paper);border:1px solid var(--ink);border-radius:.3rem;text-decoration:none;font-weight:600;}
		.download:hover {text-decoration:underline;}
		.download-row span {font-size:.9rem;}
		summary {cursor:pointer;padding:.6rem 0;}
		.license-text {white-space:pre-wrap;overflow-wrap:anywhere;font:.85rem/1.6 ui-monospace,monospace;max-height:28rem;overflow:auto;padding:1rem;border:1px solid var(--border);}
		.meta {''')
	(ROOT/'Scrivi.html').write_text(s)
	print('Standalone Scrivi.html generated')
if __name__=='__main__':main()
