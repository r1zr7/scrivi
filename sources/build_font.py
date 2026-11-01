#!/usr/bin/env python3
"""AR-Scrittura. Copyright (c) 2026 Alessandro Resch. SIL OFL 1.1.
Original monoline drawings; no external font is copied or embedded.
"""
from pathlib import Path
import json
import unicodedata as ud
import math
from datetime import datetime, timezone
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.basePen import BasePen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.svgLib.path import parse_path
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from fontTools.ttLib import TTFont
from shapely.geometry import LineString, Polygon, box
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
from shapely.affinity import translate, scale

ROOT=Path(__file__).resolve().parents[1]
SOURCES=Path(__file__).resolve().parent
DATA=json.loads((SOURCES/'glyphs.json').read_text())
FAMILY='AR Scrittura'
VERSION='1.003'

class FlattenPen(BasePen):
	def __init__(self):
		super().__init__(None)
		self.lines=[]
		self.points=[]
	def _moveTo(self,p):
		self._endPath()
		self.points=[p]
	def _lineTo(self,p): self.points.append(p)
	def _curveToOne(self,p1,p2,p3):
		p0=self.points[-1]
		steps=max(8,int(sum(math.dist(a,b) for a,b in [(p0,p1),(p1,p2),(p2,p3)])/2))
		for i in range(1,steps+1):
			t=i/steps;u=1-t
			self.points.append(tuple(u**3*p0[j]+3*u*u*t*p1[j]+3*u*t*t*p2[j]+t**3*p3[j] for j in (0,1)))
	def _qCurveToOne(self,p1,p2):
		p0=self.points[-1]
		steps=max(8,int((math.dist(p0,p1)+math.dist(p1,p2))/2))
		for i in range(1,steps+1):
			t=i/steps;u=1-t
			self.points.append(tuple(u*u*p0[j]+2*u*t*p1[j]+t*t*p2[j] for j in (0,1)))
	def _closePath(self):
		if self.points:self.points.append(self.points[0])
		self._endPath()
	def _endPath(self):
		if len(self.points)>1:self.lines.append(self.points)
		self.points=[]

def stroke(path):
	pen=FlattenPen();parse_path(path,pen);pen._endPath()
	return unary_union([LineString(x).buffer(1.8,quad_segs=6,cap_style='round',join_style='round') for x in pen.lines]) if pen.lines else Polygon()

BASE={ch:(v['width'],stroke(v['path'])) for ch,v in DATA.items()}
ACCENTS={
	'\u0300':'M-10 -22 L4 -11',
	'\u0301':'M-3 -11 L10 -23',
	'\u0302':'M-11 -11 L0 -23 L11 -11',
	'\u0303':'M-14 -14 Q-7 -24 0 -17 Q7 -10 14 -20',
	'\u0304':'M-13 -16 H13',
	'\u0306':'M-13 -24 Q0 -6 13 -24',
	'\u0307':'M0 -18 L0 -17.5',
	'\u0308':'M-9 -18 L-9 -17.5 M9 -18 L9 -17.5',
	'\u030a':'M-7 -17 C-7 -27 7 -27 7 -17 C7 -7 -7 -7 -7 -17 Z',
	'\u030b':'M-12 -10 L-3 -23 M2 -10 L11 -23',
	'\u030c':'M-11 -23 L0 -11 L11 -23',
	'\u0326':'M0 114 L-5 128',
	'\u0327':'M0 100 Q10 107 1 116 Q-3 119 -9 115',
	'\u0328':'M0 98 Q-13 111 -7 116 Q-1 121 5 115',
}

def attachment_x(geo,width):
	baseline=geo.intersection(box(-100,96,200,103))
	return baseline.bounds[2]-1.8 if not baseline.is_empty else width/2

def accent(mark,width,upper,base_geo=None):
	geo=stroke(ACCENTS[mark])
	return translate(geo,attachment_x(base_geo,width) if mark=='\u0328' and base_geo is not None else width/2,0 if upper or mark in '\u0326\u0327\u0328' else 36)

def build_shape(ch):
	if ch in BASE:return BASE[ch]
	spacing_marks={'ˆ':'\u0302','ˇ':'\u030c','˘':'\u0306','˙':'\u0307','˚':'\u030a','˛':'\u0328','˜':'\u0303','˝':'\u030b'}
	if ch in spacing_marks:return 36,translate(stroke(ACCENTS[spacing_marks[ch]]),18,0)
	extra={'‚':(22,'M13 95 Q18 108 6 118'),'„':(36,'M11 95 Q16 108 4 118 M29 95 Q34 108 22 118'),'‹':(27,'M21 49 L7 66 L21 83'),'›':(27,'M6 49 L20 66 L6 83'),'™':(78,'M0 0 H31 M15 0 V35 M40 35 V0 L55 23 L70 0 V35')}
	if ch in extra:
		w,p=extra[ch];return w,stroke(p)
	# Stroke variants which have no canonical Unicode decomposition.
	variants={'Đ':('D','M-3 49 H54'),'đ':('d','M12 22 H47'),'Ħ':('H','M-3 22 H63'),'ħ':('h','M-2 23 H27'),'Ł':('L','M-4 66 L43 37'),'ł':('l','M-5 61 L22 37'),'Ŧ':('T','M7 39 H53'),'ŧ':('t','M-2 70 H34'),'Ø':('O','M-2 102 L65 -2'),'ø':('o','M-2 104 L48 39'),'Ŀ':('L','M48 55 L48 55.5'),'ŀ':('l','M22 62 L22 62.5'),'Ŋ':('N','M63 90 Q65 128 43 121'),'ŋ':('n','M43 90 Q49 130 27 123')}
	if ch in variants:
		b,p=variants[ch];w,g=BASE[b]
		return max(w,26 if ch=='ŀ' else w),unary_union([g,stroke(p)])
	if ch in 'Ʒʒ':
		return (52,stroke('M2 0 H49 L17 43 C68 29 65 102 20 103 Q8 104 0 97')) if ch=='Ʒ' else (40,stroke('M2 44 H36 L13 75 C48 58 52 125 17 129 Q7 131 0 122'))
	if ch=='ʻ':return 20,stroke('M13 2 Q1 7 6 23')
	if ch in 'Ǥǥ':
		w,g=BASE['G' if ch.isupper() else 'g'];return w,unary_union([g,stroke('M0 44 H32' if ch.isupper() else 'M0 62 H29')])
	if ch=='œ':return 82,stroke('M39 60 C27 30 3 45 2 73 C0 99 23 111 36 94 C43 83 43 70 39 60 M40 72 C57 75 80 51 68 44 C55 34 37 57 39 78 C41 103 61 109 80 95')
	# Slovak/Czech caron has an apostrophe form beside tall letters.
	if ch in 'ďĽľť':
		b={'ď':'d','Ľ':'L','ľ':'l','ť':'t'}[ch];w,g=BASE[b]
		x={'ď':49,'Ľ':23,'ľ':19,'ť':23}[ch]
		return max(w,x+9),unary_union([g,translate(stroke('M0 0 Q4 8 -3 15'),x,0)])
	if ch in 'ĢģĶķĻļŅņŖŗ':
		b=ud.normalize('NFD',ch)[0];w,g=BASE[b]
		p=stroke('M2 -11 Q-4 -19 3 -27') if ch=='ģ' else translate(stroke('M0 109 Q7 116 -3 123'),w/2,0)
		if ch=='ģ':p=translate(p,w/2,36)
		return w,unary_union([g,p])
	if ch in ['Æ','æ','Œ','Ĳ','ĳ']:
		pair={'Æ':'AE','æ':'ae','Œ':'OE','œ':'oe','Ĳ':'IJ','ĳ':'ij'}[ch]
		w1,g1=BASE[pair[0]];w2,g2=BASE[pair[1]]
		return w1+w2-7,unary_union([g1,translate(g2,w1-7,0)])
	# Kra has a lowercase-height stem; it is not an ascender k.
	if ch=='ĸ':
		w,_=BASE['k']
		return w,stroke('M3 42 L3 100 M41 45 L4 76 M19 64 L44 100')
	# Long s retains the original f's curved ascender, without its crossbar.
	if ch=='ſ':
		w,_=BASE['f']
		return w,stroke('M9 100 L10 25 Q12 -6 30 4')
	if ch=='◌':
		parts=[]
		for a in range(0,360,30):
			t=math.radians(a);x=25+23*math.cos(t);y=71+29*math.sin(t)
			parts.append(LineString([(x,y),(x,y+0.1)]).buffer(3.2,quad_segs=8,cap_style='round',join_style='round'))
		return 50,unary_union(parts)
	decomp=ud.normalize('NFD',ch)
	if len(decomp)>1 and decomp[0]!=ch and all(m in ACCENTS for m in decomp[1:]):
		base=decomp[0]
		w,g=build_shape({'i':'ı','j':'ȷ'}.get(base,base) if any(m not in '\u0326\u0327\u0328' for m in decomp[1:]) else base)
		return w,unary_union([g]+[accent(m,w,base.isupper() or base in 'hkl',g) for m in decomp[1:]])
	if ch in ACCENTS:
		return 0,stroke(ACCENTS[ch])
	return None

def name(ch):return f'uni{ord(ch):04X}'

CHARS=sorted(set(chr(i) for i in list(range(32,127))+list(range(160,384))+[0x237,0x1e9e,0x20ac,0x2013,0x2014,0x2018,0x2019,0x201c,0x201d,0x2022,0x2026,0x2212,0x218,0x219,0x21a,0x21b,0x2c6,0x2c7,0x2d8,0x2d9,0x2da,0x2db,0x2dc,0x2dd,0x1e80,0x1e81,0x1e82,0x1e83,0x1e84,0x1e85,0x1ef2,0x1ef3,0x201a,0x201e,0x2039,0x203a,0x2122,0x25cc,0x1fe,0x1ff,0x2bb,0x1e6,0x1e7,0x1e4,0x1e5,0x21e,0x21f,0x1e8,0x1e9,0x1b7,0x292,0x1ee,0x1ef,0x1d3,0x1d4,0x1ebc,0x1ebd,0x1cd,0x1ce])|set(ACCENTS),key=ord)
SHAPES={}
for ch in CHARS:
	shape=build_shape(ch)
	if shape is None:raise ValueError(f'Undrawn character U+{ord(ch):04X} {ch}')
	SHAPES[ch]=shape

def glyph_from_shape(geo,width,combining=False):
	# All drawing coordinates use a 100-unit cap-height grid, y down.
	geo=scale(geo,xfact=7,yfact=-7,origin=(0,0))
	geo=translate(geo,xoff=0 if combining else 28,yoff=700)
	geo=geo.simplify(0.6,preserve_topology=True)
	pen=TTGlyphPen(None)
	polys=list(geo.geoms) if geo.geom_type=='MultiPolygon' else ([geo] if not geo.is_empty else [])
	for poly in polys:
		poly=orient(poly,sign=-1)
		for ring in [poly.exterior]+list(poly.interiors):
			pts=[(round(x),round(y)) for x,y in ring.coords[:-1]]
			pts=list(dict.fromkeys(pts))
			if len(pts)<3:continue
			pen.moveTo(pts[0])
			for p in pts[1:]:pen.lineTo(p)
			pen.closePath()
	glyph=pen.glyph()
	if glyph.numberOfContours:glyph.recalcBounds(None)
	lsb=glyph.xMin if glyph.numberOfContours else 0
	advance=0 if combining else round(width*7+56)
	return glyph,(advance,lsb)

def main():
	order=['.notdef']+[name(ch) for ch in CHARS]+['iogonek.nodot']
	glyphs={};metrics={}
	glyphs['.notdef'],metrics['.notdef']=glyph_from_shape(stroke('M3 0 H45 V100 H3 Z M3 0 L45 100'),48)
	for ch,(w,g) in SHAPES.items():
		if ch in '+−÷×=<>¬':
			g=translate(g,(49-w)/2,0);w=49
		glyphs[name(ch)],metrics[name(ch)]=glyph_from_shape(g,w,ch in ACCENTS)
	w,g=BASE['ı']
	g=unary_union([g,accent('\u0328',w,False,g)])
	glyphs['iogonek.nodot'],metrics['iogonek.nodot']=glyph_from_shape(g,w)
	fb=FontBuilder(1000,isTTF=True)
	fb.setupGlyphOrder(order)
	fb.setupCharacterMap({ord(ch):name(ch) for ch in CHARS})
	fb.setupGlyf(glyphs)
	fb.setupHorizontalMetrics(metrics)
	fb.setupHorizontalHeader(ascent=1030,descent=-310,lineGap=0)
	fb.setupNameTable({'familyName':FAMILY,'styleName':'Regular','uniqueFontIdentifier':VERSION+';ARSC;ARScrittura-Regular','fullName':FAMILY+' Regular','psName':'ARScrittura-Regular','version':'Version '+VERSION,'copyright':'Copyright 2026 The AR Scrittura Project Authors (https://ar-scrittura.workspace-833185.chatgpt.site/)','designer':'Alessandro Resch','manufacturer':'Alessandro Resch','description':'Original monoline handwriting by Alessandro Resch. Separated letters with simple strokes for names, headings and short messages.','licenseDescription':'This Font Software is licensed under the SIL Open Font License, Version 1.1. This license is available with a FAQ at: https://openfontlicense.org','licenseInfoURL':'https://openfontlicense.org'})
	fb.setupOS2(version=4,sTypoAscender=1030,sTypoDescender=-310,sTypoLineGap=0,usWinAscent=1030,usWinDescent=310,sxHeight=420,sCapHeight=700,usWeightClass=400,usWidthClass=5,fsType=0,fsSelection=0xC0,ulCodePageRange1=0x00000093,ulCodePageRange2=0,achVendID='ARSC')
	fb.setupPost(keepGlyphNames=True,underlinePosition=-160,underlineThickness=25)
	fb.setupMaxp()
	fb.font['head'].fontRevision=float(VERSION)
	# Reproducible timestamps: 26 October 2026, 00:00 UTC, in Mac epoch.
	fb.font['head'].created=int(datetime(2026,10,26,tzinfo=timezone.utc).timestamp())+2082844800
	fb.font['head'].modified=fb.font['head'].created
	fb.font.recalcTimestamp=False
	fea=['languagesystem DFLT dflt;','languagesystem latn dflt;','feature kern {']
	pairs={'Ta':-18,'Te':-20,'To':-26,'Tu':-18,'Ty':-20,'Va':-25,'Ve':-22,'Vo':-28,'Wa':-18,'Wo':-18,'Ya':-25,'Yo':-30,'AT':-20,'AV':-22,'AW':-15,'AY':-22,'LT':-15,'LV':-15,'PA':-16,'FA':-17,'Pe':-10}
	for pair,value in pairs.items():
		fea.append(f'pos {name(pair[0])} {name(pair[1])} {value};')
	fea.append('} kern;')
	# Mark positioning for decomposed Latin accents, equivalent to precomposed forms.
	for m in ACCENTS:
		anchor_y=0 if m in '\u0326\u0327\u0328' else 700
		fea.append(f'markClass {name(m)} <anchor 0 {anchor_y}> @MARK{ord(m):04X};')
	fea.append('@ABOVE = ['+' '.join(name(m) for m in ACCENTS if m not in '\u0326\u0327\u0328')+'];')
	fea.append('@BELOW = ['+' '.join(name(m) for m in '\u0326\u0327\u0328')+'];')
	fea.append('feature ccmp {')
	for src,dst in [(name('i'),name('ı')),(name('j'),name('ȷ')),(name('į'),'iogonek.nodot')]:
		fea.append(f'sub {src}\' @ABOVE by {dst};')
		fea.append(f'sub {src}\' @BELOW @ABOVE by {dst};')
	fea.append('} ccmp;')
	fea.append('feature mark {')
	for base in [ch for ch in CHARS if ch.isalpha() and ch not in ACCENTS]+['◌']:
		w,_=SHAPES[base]
		for m in ACCENTS:
			x=round((attachment_x(SHAPES[base][1],w) if m=='\u0328' else w/2)*7+28)
			y=0 if m in '\u0326\u0327\u0328' else (700 if base.isupper() or ud.normalize('NFD',base)[0] in 'hkl' else 448)
			decomp=ud.normalize('NFD',base)
			if any(a in ACCENTS and a not in '\u0326\u0327\u0328' for a in decomp[1:]):y+=210
			if base=='◌':y=448 if m not in '\u0326\u0327\u0328' else 0
			fea.append(f'pos base {name(base)} <anchor {x} {y}> mark @MARK{ord(m):04X};')
	for m in ACCENTS:
		w,g=BASE['ı'];x=round((attachment_x(g,w) if m=='\u0328' else w/2)*7+28);y=0 if m in '\u0326\u0327\u0328' else 448
		fea.append(f'pos base iogonek.nodot <anchor {x} {y}> mark @MARK{ord(m):04X};')
	fea.append('} mark;')
	fea.append('feature mkmk {')
	for first in ACCENTS:
		for second in ACCENTS:
			if first in '\u0326\u0327\u0328' or second in '\u0326\u0327\u0328':continue
			fea.append(f'pos mark {name(first)} <anchor 0 910> mark @MARK{ord(second):04X};')
	fea.append('} mkmk;')
	features='\n'.join(fea)
	(SOURCES/'features.fea').write_text(features,encoding='utf-8')
	addOpenTypeFeaturesFromString(fb.font,features)
	# UFO is the editable outline source. Compile it with fontmake.
	from ufoLib2 import Font
	from fontTools.pens.pointPen import SegmentToPointPen
	from fontmake.font_project import FontProject
	ufo=Font()
	i=ufo.info
	i.familyName=FAMILY;i.styleName='Regular';i.unitsPerEm=1000
	i.ascender=1030;i.descender=-310;i.xHeight=420;i.capHeight=700
	i.versionMajor=int(VERSION.split('.')[0]);i.versionMinor=int(VERSION.split('.')[1])
	i.copyright='Copyright 2026 The AR Scrittura Project Authors (https://ar-scrittura.workspace-833185.chatgpt.site/)'
	i.openTypeNameDesigner='Alessandro Resch';i.openTypeNameManufacturer='Alessandro Resch'
	i.openTypeNameDescription=fb.font['name'].getDebugName(10)
	i.openTypeNameLicense=fb.font['name'].getDebugName(13)
	i.openTypeNameLicenseURL='https://openfontlicense.org'
	i.openTypeOS2VendorID='ARSC';i.openTypeOS2WeightClass=400;i.openTypeOS2WidthClass=5
	i.openTypeOS2Selection=[7];i.openTypeOS2Type=[]
	i.openTypeOS2CodePageRanges=[0,1,4,7]
	i.openTypeOS2TypoAscender=1030;i.openTypeOS2TypoDescender=-310;i.openTypeOS2TypoLineGap=0
	i.openTypeOS2WinAscent=1030;i.openTypeOS2WinDescent=310
	i.openTypeHheaAscender=1030;i.openTypeHheaDescender=-310;i.openTypeHheaLineGap=0
	i.postscriptUnderlinePosition=-160;i.postscriptUnderlineThickness=25
	i.postscriptFontName='ARScrittura-Regular'
	for gn in order:
		g=ufo.newGlyph(gn);g.width=metrics[gn][0]
		if gn.startswith('uni'):g.unicodes=[int(gn[3:],16)]
		glyphs[gn].draw(SegmentToPointPen(g.getPointPen()),glyphs)
	ufo.glyphOrder=order;ufo.features.text=features
	ufo.save(SOURCES/'AR-Scrittura-Regular.ufo',overwrite=True)
	out=ROOT/'fonts'/'ARScrittura-Regular.ttf'
	names=fb.font['name']
	FontProject().run_from_ufos([ufo],output=['ttf'],output_path=str(out),use_production_names=False)
	fb.font=TTFont(out)
	fb.font.recalcTimestamp=False
	fb.font['head'].created=int(datetime(2026,10,27,tzinfo=timezone.utc).timestamp())+2082844800
	fb.font['head'].modified=fb.font['head'].created
	fb.font['name']=names
	fb.font['name'].names=[n for n in names.names if n.platformID!=1]
	from fontTools.ttLib import newTable
	fb.font['gasp']=newTable('gasp');fb.font['gasp'].gaspRange={65535:15}
	fb.font['OS/2'].sFamilyClass=10<<8
	fb.font['OS/2'].panose.bFamilyType=3
	fb.font['OS/2'].panose.bWeight=4
	fb.font['OS/2'].panose.bProportion=2
	fb.font['OS/2'].sxHeight=420;fb.font['OS/2'].sCapHeight=700
	fb.font['meta']=newTable('meta');fb.font['meta'].data={'dlng':'Latn','slng':'Latn'}
	# Recommended unhinted TrueType smart dropout program (gftools).
	from fontTools.ttLib.tables.ttProgram import Program
	fb.font['prep']=newTable('prep');fb.font['prep'].program=Program()
	fb.font['prep'].program.fromBytecode([0xB8,0x01,0xFF,0x85,0xB0,0x04,0x8D])
	fb.save(out)
	font=TTFont(out);font.recalcTimestamp=False;font.flavor='woff2';font.save(ROOT/'web'/'AR-Scrittura-Regular.woff2')
	(ROOT/'qa'/'coverage.json').write_text(json.dumps({'family':FAMILY,'version':VERSION,'author':'Alessandro Resch','encoded_characters':len(CHARS),'glyphs':len(order),'characters':''.join(CHARS),'kerning_pairs':len(pairs)},indent='\t',ensure_ascii=False),encoding='utf-8')
	print(f'{len(CHARS)} characters / {len(order)} glyphs; TTF and WOFF2 built.')

if __name__=='__main__':main()
