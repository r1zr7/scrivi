#!/usr/bin/env python3
"""Copyright (c) 2026 Alessandro Resch. SIL Open Font License 1.1."""
from pathlib import Path
import json,hashlib,unicodedata,subprocess,sys
from fontTools.ttLib import TTFont
from ufoLib2 import Font
import glyphsets
from verify_and_preview import shape

R=Path(__file__).resolve().parents[1]
p=R/'fonts/ttf/Scrivi-Regular.ttf'
f=TTFont(p);c=f.getBestCmap();data=p.read_bytes();checks=[]
def check(ok,text):
	if not ok:raise AssertionError(text)
	checks.append(text)
base=json.loads((R/'qa/preview-baseline.json').read_text())
check(set(map(int,base['advances'])).issubset(c),'All 344 previous codepoints retained')
maths=set(map(ord,'+−÷×=<>¬'))
check(all(f['hmtx'][c[int(cp)]][0]==advance for cp,advance in base['advances'].items() if int(cp) not in maths and int(cp) not in map(ord,'ďĽľť')),'Previous advances retained except documented math operators and side-caron glyphs')
check(set(glyphsets.unicodes_per_glyphset('GF_Latin_Core')).issubset(c),'Complete GF Latin Core coverage')
check(f['name'].getDebugName(0)==(R/'OFL.txt').read_text().splitlines()[0],'Copyright in font and OFL matches exactly')
check(f['name'].getDebugName(5)=='Version 1.004','Release version 1.004 in name table')
check(round(f['head'].fontRevision,3)==1.004,'Version matches head.fontRevision')
check(f['name'].getDebugName(9)=='Alessandro Resch','Designer retained')
check(f['OS/2'].fsType==0,'Installable embedding allowed')
check('mkmk' in [r.FeatureTag for r in f['GPOS'].table.FeatureList.FeatureRecord],'Mark-to-mark positioning compiled')
for ch in c:
	check(all(g[0]!=0 for g in shape(data,chr(ch))),f'Shapes U+{ch:04X} without .notdef')
for cp in c:
	text=chr(cp);nfd=unicodedata.normalize('NFD',text)
	if len(nfd)>1 and all(ord(t) in c for t in nfd):
		check(shape(data,text)==shape(data,nfd),f'NFC/NFD equivalent U+{cp:04X}')
for text in ['ȘșȚț','ẀẁẂẃẄẅỲỳ','ďĽľť','ĢģĶķĻļŅņŖŗ','Ą́ Ę̃ Į̇́ Ų̃ Ū́','ą́ ę̃ į́ ų̃ ū́','◌́ ◌̦']:
	check(all(g[0]!=0 for g in shape(data,text)),f'Language sample: {text}')
for text in ['į́','į̀','í̦','j̧́']:
	out=shape(data,text)
	check(f.getGlyphID('uni0069') not in [g[0] for g in out] and f.getGlyphID('uni006A') not in [g[0] for g in out],f'Dotless contextual substitution: {text}')
u=Font.open(R/'sources/Scrivi-Regular.ufo',validate=True)
check(set(f.getGlyphOrder())==set(u.keys()),'Editable UFO contains every compiled glyph')
check(len(u)==394,'394 editable glyphs, including unencoded dotless alternate')
# The binary assembly, including WOFF2 compression, must be byte-identical twice.
paths=[p,R/'fonts/webfonts/Scrivi-Regular.woff2']
before={x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in paths}
subprocess.run([sys.executable,str(R/'sources/build_font.py')],check=True,capture_output=True)
after={x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in paths}
check(before==after,'Rebuild from original drawings produces byte-identical TTF and WOFF2')
result={'result':'PASS','checks_count':len(checks),'checks':checks,'sha256':after,'googlefonts_status':'Not admitted. Catalog review and author CLA remain open; Scrivi naming and public repository are documented.'}
(R/'qa/release-validation.json').write_text(json.dumps(result,indent='\t',ensure_ascii=False)+'\n')
print(f"PASS: {len(checks)} release assertions, including reproducibility")
