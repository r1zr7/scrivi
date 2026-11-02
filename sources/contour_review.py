#!/usr/bin/env python3
"""Copyright (c) 2026 Alessandro Resch. SIL Open Font License 1.1."""
from pathlib import Path
import argparse,json,hashlib
from fontTools.ttLib import TTFont
from shapely.geometry import Polygon

ROOT=Path(__file__).resolve().parents[1]

def contours(font,ch):
	name=font.getBestCmap()[ord(ch)]
	glyph=font['glyf'][name]
	points,endpoints,_=glyph.getCoordinates(font['glyf'])
	start=0;out=[]
	for end in endpoints:
		out.append(Polygon(points[start:end+1]));start=end+1
	return out

def main():
	parser=argparse.ArgumentParser();parser.add_argument('--baseline',type=Path);args=parser.parse_args()
	path=ROOT/'fonts/ttf/Scrivi-Regular.ttf';font=TTFont(path);checks=[]
	for ch in 'ĺȘșȚț':
		parts=contours(font,ch)
		assert len(parts)==2,(ch,len(parts))
		gap=parts[0].distance(parts[1]);assert gap>=35,(ch,gap)
		checks.append({'character':ch,'contours':len(parts),'minimum_separation_font_units':round(gap,2)})
	parts=contours(font,'◌');assert len(parts)==12
	assert all(p.is_valid for p in parts)
	assert min(min(p.bounds[2]-p.bounds[0],p.bounds[3]-p.bounds[1]) for p in parts)>=43
	assert all(a.distance(b)>0 for i,a in enumerate(parts) for b in parts[i+1:])
	checks.append({'character':'◌','separate_dots':12,'minimum_dot_diameter_font_units':min(min(p.bounds[2]-p.bounds[0],p.bounds[3]-p.bounds[1]) for p in parts)})
	result={'result':'PASS','version':'1.004','author':'Alessandro Resch','checks':checks,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
	if args.baseline:
		old=TTFont(args.baseline);old_cmap=old.getBestCmap();cmap=font.getBestCmap()
		assert cmap==old_cmap
		assert all(old['hmtx'][gn][0]==font['hmtx'][gn][0] for gn in old.getGlyphOrder())
		changed=[chr(cp) for cp,gn in cmap.items() if old['glyf'][gn].compile(old['glyf'])!=font['glyf'][gn].compile(font['glyf'])]
		assert set(changed)==set('ĺȘșȚț\u0326◌'),changed
		for table in ['hhea','GSUB']:
			assert old.getTableData(table)==font.getTableData(table),table
		result['baseline']={'version':'1.000','sha256':hashlib.sha256(args.baseline.read_bytes()).hexdigest(),'changed_encoded_outlines':changed,'all_advances_unchanged':True,'cmap_unchanged':True,'approved_side_carons_unchanged':True}
	(ROOT/'qa/contour-review.json').write_text(json.dumps(result,indent='\t',ensure_ascii=False)+'\n')
	print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
