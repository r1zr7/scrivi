#!/usr/bin/env python3
"""Copyright (c) 2026 Alessandro Resch. SIL Open Font License 1.1."""
from pathlib import Path
import argparse,json,hashlib
from fontTools.ttLib import TTFont
from shapely.geometry import Polygon, LineString

ROOT=Path(__file__).resolve().parents[1]

def main():
	parser=argparse.ArgumentParser();parser.add_argument('--baseline',type=Path);args=parser.parse_args()
	path=ROOT/'fonts/ARScrittura-Regular.ttf';f=TTFont(path);cmap=f.getBestCmap();glyf=f['glyf']
	longs=glyf[cmap[ord('ſ')]];letter_f=glyf[cmap[ord('f')]]
	kra=glyf[cmap[ord('ĸ')]];letter_k=glyf[cmap[ord('k')]]
	assert longs.compile(glyf)!=letter_f.compile(glyf),'Long s must not duplicate f'
	assert kra.compile(glyf)!=letter_k.compile(glyf),'Kra must not duplicate k'
	assert abs(kra.yMax-f['OS/2'].sxHeight)<=5,(kra.yMax,f['OS/2'].sxHeight)
	assert letter_k.yMax-kra.yMax>=250
	assert abs(longs.yMax-letter_f.yMax)<=2 and abs(longs.yMin-letter_f.yMin)<=2
	# Absence of the f crossbar: in its horizontal band, long s is a narrow stem.
	points,_,_=longs.getCoordinates(glyf)
	section=Polygon(points).intersection(LineString([(-1000,385),(2000,385)]))
	assert not section.is_empty and section.bounds[2]-section.bounds[0]<=30,section
	result={'result':'PASS','version':'1.003','author':'Alessandro Resch','sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'long_s':{'distinct_from_f':True,'crossbar_absent':True},'kra':{'distinct_from_k':True,'top_font_units':kra.yMax,'x_height_font_units':f['OS/2'].sxHeight}}
	if args.baseline:
		old=TTFont(args.baseline);assert cmap==old.getBestCmap()
		changed=[chr(cp) for cp,gn in cmap.items() if glyf[gn].compile(glyf)!=old['glyf'][gn].compile(old['glyf'])]
		assert set(changed)==set('ſĸ'),changed
		assert all(f['hmtx'][gn][0]==old['hmtx'][gn][0] for gn in f.getGlyphOrder())
		for table in ['GPOS','GSUB','GDEF']:
			assert f.getTableData(table)==old.getTableData(table),table
		result['baseline']={'version':'1.001','changed_encoded_outlines':changed,'all_advances_unchanged':True,'positioning_and_substitutions_unchanged':True,'other_outlines_unchanged':True}
	(ROOT/'qa/special-forms-review.json').write_text(json.dumps(result,ensure_ascii=False,indent='\t')+'\n')
	print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
