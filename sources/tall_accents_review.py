#!/usr/bin/env python3
"""Copyright (c) 2026 Alessandro Resch. SIL Open Font License 1.1."""
from pathlib import Path
import argparse,json,hashlib
from fontTools.ttLib import TTFont
from contour_review import contours

ROOT=Path(__file__).resolve().parents[1]

def main():
	parser=argparse.ArgumentParser();parser.add_argument('--baseline',type=Path);args=parser.parse_args()
	path=ROOT/'fonts/ARScrittura-Regular.ttf';f=TTFont(path);cmap=f.getBestCmap();checks=[]
	for ch in 'ĥȟǩ':
		parts=contours(f,ch);assert len(parts)==2,(ch,len(parts))
		parts.sort(key=lambda p:p.bounds[1]);base,mark=parts
		gap=mark.bounds[1]-base.bounds[3]
		assert gap>=35,(ch,gap)
		checks.append({'character':ch,'vertical_gap_font_units':gap})
	# Inspect compiled mark-to-base positioning, independent of HarfBuzz recomposition.
	for ch in 'hklĥȟǩ':
		y_values=[]
		for lookup in f['GPOS'].table.LookupList.Lookup:
			if lookup.LookupType!=4:continue
			for sub in lookup.SubTable:
				if cmap[ord(ch)] not in sub.BaseCoverage.glyphs:continue
				i=sub.BaseCoverage.glyphs.index(cmap[ord(ch)])
				y_values.extend(a.YCoordinate for a in sub.BaseArray.BaseRecord[i].BaseAnchor[:11] if a)
		expected=700 if ch in 'hkl' else 910
		assert y_values and set(y_values)=={expected},(ch,y_values)
	result={'result':'PASS','author':'Alessandro Resch','version':f['name'].getDebugName(5),'checks':checks,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
	if args.baseline:
		old=TTFont(args.baseline);assert cmap==old.getBestCmap()
		changed=[chr(cp) for cp,gn in cmap.items() if f['glyf'][gn].compile(f['glyf'])!=old['glyf'][gn].compile(old['glyf'])]
		assert set(changed)==set('ĥȟǩ'),changed
		assert all(f['hmtx'][gn][0]==old['hmtx'][gn][0] for gn in f.getGlyphOrder())
		for table in ['GSUB','GDEF']:assert f.getTableData(table)==old.getTableData(table),table
		assert f.getTableData('GPOS')!=old.getTableData('GPOS')
		result['baseline']={'version':'1.002','changed_encoded_outlines':changed,'all_advances_unchanged':True,'GSUB_GDEF_unchanged':True,'GPOS_updated_for_tall_lowercase_accents':True}
	(ROOT/'qa/tall-accents-review.json').write_text(json.dumps(result,indent='\t',ensure_ascii=False)+'\n')
	print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
