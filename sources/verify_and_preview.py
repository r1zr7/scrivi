#!/usr/bin/env python3
"""Copyright (c) 2026 Alessandro Resch. SIL OFL 1.1."""
from pathlib import Path
import json
import os
import hashlib
import unicodedata
from fontTools.ttLib import TTFont
import uharfbuzz as hb
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
TTF=ROOT/'fonts/ARScrittura-Regular.ttf'
WOFF=ROOT/'web/AR-Scrittura-Regular.woff2'

def shape(data,text,features=None):
	font=hb.Font(hb.Face(data));font.scale=(1000,1000)
	buf=hb.Buffer();buf.add_str(text);buf.guess_segment_properties()
	hb.shape(font,buf,features or {})
	return [(g.codepoint,p.x_advance,p.y_advance,p.x_offset,p.y_offset) for g,p in zip(buf.glyph_infos,buf.glyph_positions)]

def ui_font(size):
	for candidate in [os.environ.get('AR_SCRITTURA_UI_FONT',''),'DejaVuSans.ttf','C:/Windows/Fonts/segoeui.ttf','/System/Library/Fonts/Supplemental/Arial.ttf']:
		if not candidate:continue
		try:return ImageFont.truetype(candidate,size)
		except OSError:pass
	return ImageFont.load_default(size=size)

def main():
	font=TTFont(TTF,checkChecksums=2);web=TTFont(WOFF,checkChecksums=2)
	cmap=font.getBestCmap();data=TTF.read_bytes()
	assert cmap==web.getBestCmap()
	assert font['OS/2'].fsType==0
	assert font['OS/2'].version>=4
	assert len(cmap)==392
	assert all(i in cmap for i in range(32,127))
	assert all(i in cmap for i in range(160,384))
	assert font['name'].getDebugName(1)=='AR Scrittura'
	assert font['name'].getDebugName(9)=='Alessandro Resch'
	assert 'Open Font License' in font['name'].getDebugName(13)
	for table in ['glyf','hmtx','cmap','GSUB','GPOS','GDEF']:
		assert font.getTableData(table)==web.getTableData(table),table
	for glyph in font['glyf'].glyphs.values():
		glyph.expand(font['glyf'])
		if glyph.numberOfContours:
			assert glyph.yMax<=1030 and glyph.yMin>=-310
	for ch in cmap:
		assert all(g[0]!=0 for g in shape(data,chr(ch))),f'Missing {ch}'
	accented='ÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜÝàáâãäåçèéêëìíîïñòóôõöùúûüýÿĜĝĴĵŠšŽž'
	for ch in accented:
		assert shape(data,ch)==shape(data,unicodedata.normalize('NFD',ch)),ch
	assert sum(x[1] for x in shape(data,'To'))<sum(x[1] for x in shape(data,'To',{'kern':False}))
	assert shape(data,'i\u030b',{'ccmp':True})[0][0]==font.getGlyphID('uni0131')
	assert shape(data,'j\u030b',{'ccmp':True})[0][0]==font.getGlyphID('uni0237')
	checks={'result':'PASS','encoded_characters':len(cmap),'glyphs':font['maxp'].numGlyphs,'checks':['TTF and WOFF2 load and relevant tables match','ASCII, Latin-1 Supplement and Latin Extended-A complete','All mapped characters shape without .notdef','Glyph bounds within vertical metrics','Precomposed/decomposed accent samples equivalent','Kerning changes the To pair','Dotless i and j substitutions before unsupported precomposed accents','License, author, family and embedding metadata checked'],'limitations':['Author approved AR Scrittura; Google Fonts admission and naming review pending','Only Regular; review covers selected supported languages, not every possible text','Combining marks and above-mark stacking provided; arbitrary stacks can exceed normal line height'],'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [TTF,WOFF]}}
	(ROOT/'qa/validation.json').write_text(json.dumps(checks,indent='\t',ensure_ascii=False)+'\n')
	image=Image.new('RGB',(1600,1750),'#f6f4ef');draw=ImageDraw.Draw(image)
	# Use an installed UI font, with a portable Pillow fallback.
	def label(text,y,size=22):draw.text((90,y),text,font=ui_font(size),fill='#5a5e60')
	def sample(text,y,size=70):draw.text((90,y),text,font=ImageFont.truetype(str(TTF),size),fill='#172d3a')
	label('AR / STUDIO DEL CARATTERE',65,20)
	sample('AR-Scrittura',110,140)
	label('1.003 · candidato per pubblicazione · Regular · SIL Open Font License 1.1',310)
	draw.line((90,365,1510,365),fill='#c6cccb',width=2)
	label('FIRMA SEMPLICE, LETTERE SEPARATE',410)
	sample('Tema   Club   Personal',455,105)
	label('ALFABETO',625)
	sample('ABCDEFGHIJKLMNOPQRSTUVWXYZ',660,65)
	sample('abcdefghijklmnopqrstuvwxyz',760,75)
	sample('0123456789   & @ € % + − = ? !',875,70)
	label('ACCENTI E SEGNI',1015)
	sample('à è é ì ò ù  Ä Ö Ü ß  ç ñ  ø æ œ',1050,65)
	label('PROVE DI LETTURA',1190)
	sample('Pochi segni, spazio alle idee.',1230,60)
	sample('Simple letters. Clear intentions.',1335,45)
	sample('Un carattere per nomi, titoli e brevi messaggi.',1420,32)
	draw.line((90,1545,1510,1545),fill='#c6cccb',width=2)
	label('Disegni originali · Alessandro Resch · 2026',1590)
	label('Disegno monolineare originale · sorgenti UFO · TTF e WOFF2',1640,20)
	image.save(ROOT/'specimen/anteprima.png')
	print(json.dumps(checks,ensure_ascii=False))

if __name__=='__main__':main()
