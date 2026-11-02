#!/usr/bin/env python3
"""Copyright (c) 2026 Alessandro Resch. SIL Open Font License 1.1."""
from pathlib import Path
import argparse
from PIL import Image,ImageDraw,ImageFont
from verify_and_preview import ui_font

ROOT=Path(__file__).resolve().parents[1]
def main():
	parser=argparse.ArgumentParser();parser.add_argument('--baseline',type=Path,required=True);args=parser.parse_args()
	im=Image.new('RGB',(1240,890),'#faf9f6');d=ImageDraw.Draw(im)
	d.text((36,25),'Scrivi · accenti sulle aste alte',font=ui_font(26),fill='#293747')
	d.text((36,65),'Alessandro Resch · 28 ottobre 2026 · confronto 1.002 / 1.004',font=ui_font(18),fill='#53616c')
	for x,label,path in [(36,'Prima · 1.002',args.baseline),(650,'Dopo · 1.004',ROOT/'fonts/ttf/Scrivi-Regular.ttf')]:
		d.text((x,120),label,font=ui_font(22),fill='#293747')
		for y,size,text in [(175,120,'h ĥ ȟ'),(360,120,'k ķ ǩ'),(555,24,'h ĥ ȟ   k ķ ǩ   l ĺ'),(650,48,'ĥa ȟe ǩi ĺo'),(750,48,'h\u0302 h\u030c k\u030c')]:
			d.text((x,y),text,font=ImageFont.truetype(str(path),size),fill='#203642')
	im.save(ROOT/'specimen/accenti-alti-prima-dopo.png')
if __name__=='__main__':main()
