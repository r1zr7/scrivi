#!/usr/bin/env python3
"""Copyright (c) 2026 Alessandro Resch. SIL Open Font License 1.1."""
from pathlib import Path
import argparse
from PIL import Image, ImageDraw, ImageFont
from verify_and_preview import ui_font

ROOT=Path(__file__).resolve().parents[1]

def main():
	parser=argparse.ArgumentParser();parser.add_argument('--baseline',type=Path);args=parser.parse_args()
	current=ROOT/'fonts/ttf/Scrivi-Regular.ttf'
	columns=[('1.000 · prima',args.baseline),('1.001 · correzione',current)] if args.baseline else [('1.001 · correzione',current)]
	width=620*len(columns)
	im=Image.new('RGB',(width,950),'#f6f4ef');d=ImageDraw.Draw(im)
	for n,(title,path) in enumerate(columns):
		x=30+n*620
		d.text((x,25),title,font=ui_font(24),fill='#172d3a')
		d.text((x,65),'GRANDE · 120 px',font=ui_font(18),fill='#5a5e60')
		f=ImageFont.truetype(str(path),120)
		for y,text in [(100,'l ĺ  Ș ș'),(275,'Ț ț'),(450,'◌ ◌́ ◌̀ ◌̈')]:d.text((x,y),text,font=f,fill='#172d3a')
		d.line((x,635,x+550,635),fill='#c6cccb',width=1)
		d.text((x,660),'PICCOLO · 24 px',font=ui_font(18),fill='#5a5e60')
		f=ImageFont.truetype(str(path),24)
		for y,text in [(710,'l ĺ  ĺa ĺe ĺi ĺo ĺu'),(755,'S Ș  s ș  Șa Șe Și Șo Șu'),(800,'Ț ț  ța țe ți țo țu'),(845,'◌ ◌́ ◌̀ ◌̈')]:d.text((x,y),text,font=f,fill='#172d3a')
	d.text((30,915),'Alessandro Resch · verifica contorni · 27 ottobre 2026',font=ui_font(16),fill='#5a5e60')
	im.save(ROOT/'specimen/contorni-prima-dopo.png')

if __name__=='__main__':main()
