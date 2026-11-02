#!/usr/bin/env python3
"""Copyright (c) 2026 Alessandro Resch. SIL OFL 1.1."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from verify_and_preview import ui_font
r=Path(__file__).resolve().parents[1]
f=ImageFont.truetype(str(r/'fonts/ttf/Scrivi-Regular.ttf'),85)
# System UI font for captions; not copied into the font distribution.
ui=ui_font(23)
im=Image.new('RGB',(1600,1600),'#f6f4ef');d=ImageDraw.Draw(im)
rows=[('NUOVI SEGNI / RUMENO E GALLESE','Ș ș Ț ț   Ẁ ẁ Ẃ ẃ Ẅ ẅ Ỳ ỳ'),('CARON LATERALE / VIRGOLE','ď Ľ ľ ť    Ģ ģ Ķ ķ Ļ ļ Ņ ņ Ŗ ŗ'),('DOTLESS / OGONEK','i į į́ į̀    j j̦́    Ą́ ą́ Ę̃ ę̃'),('POSIZIONAMENTO SU ACCENTI','Į̇́ į̇́   Ų̃ ų̃   Ū́ ū́   ◌́ ◌̦'),('ALTRE LETTERE LATINE','Ǎ ǎ Ǔ ǔ Ǧ ǧ Ǩ ǩ Ȟ ȟ Ǿ ǿ'),('ALTRE LETTERE E SEGNI','Ʒ ʒ Ǯ ǯ Ẽ ẽ    ‹ › ‚ „ ™'),('LETTURA','Știință · Dobrý deň · Ŵyl · æ œ')]
for n,(label,text) in enumerate(rows):
	y=50+n*215;d.text((70,y),label,font=ui,fill='#5a5e60');d.text((70,y+44),text,font=f,fill='#172d3a')
im.save(r/'specimen/lingue-e-accenti.png')
