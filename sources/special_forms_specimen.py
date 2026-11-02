#!/usr/bin/env python3
"""Copyright (c) 2026 Alessandro Resch. SIL Open Font License 1.1."""
from pathlib import Path
import argparse
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
from verify_and_preview import ui_font

ROOT=Path(__file__).resolve().parents[1]

def version(path):
	with TTFont(path) as f:return f['name'].getDebugName(5).removeprefix('Version ')

def main():
	parser=argparse.ArgumentParser();parser.add_argument('--baseline',type=Path);args=parser.parse_args()
	current=ROOT/'fonts/ttf/Scrivi-Regular.ttf'
	columns=[(version(args.baseline)+' · prima',args.baseline),(version(current)+' · correzione',current)] if args.baseline else [(version(current),current)]
	im=Image.new('RGB',(660*len(columns),1180),'#f6f4ef');d=ImageDraw.Draw(im)
	for n,(title,path) in enumerate(columns):
		x=30+n*660
		d.text((x,25),title,font=ui_font(24),fill='#172d3a')
		d.text((x,65),'GRANDE · 120 px',font=ui_font(18),fill='#5a5e60')
		f=ImageFont.truetype(str(path),120)
		for y,text in [(100,'f ſ s    k ĸ x'),(285,'ſa ſe ſi ſo ſu'),(470,'ĸa ĸe ĸi ĸo ĸu')]:d.text((x,y),text,font=f,fill='#172d3a')
		d.line((x,675,x+590,675),fill='#c6cccb',width=1)
		d.text((x,700),'PICCOLO · 24 px',font=ui_font(18),fill='#5a5e60')
		f=ImageFont.truetype(str(path),24)
		for y,text in [(750,'f ſ s    k ĸ x'),(805,'ſa ſe ſi ſo ſu'),(860,'ĸa ĸe ĸi ĸo ĸu')]:d.text((x,y),text,font=f,fill='#172d3a')
		d.text((x,950),'CONTROLLO · 48 px',font=ui_font(18),fill='#5a5e60')
		f=ImageFont.truetype(str(path),48)
		d.text((x,1000),'fſ  ſf   kĸ  ĸk',font=f,fill='#172d3a')
	d.text((30,1130),'Alessandro Resch · s lunga e kra · 27 ottobre 2026',font=ui_font(16),fill='#5a5e60')
	im.save(ROOT/'specimen/speciali-prima-dopo.png')

if __name__=='__main__':main()
