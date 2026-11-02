#!/usr/bin/env python3
"""Copyright 2026 Alessandro Resch. SIL OFL 1.1."""
from pathlib import Path
import argparse,json,hashlib
from fontTools.ttLib import TTFont
ROOT=Path(__file__).resolve().parents[1]

def main():
	parser=argparse.ArgumentParser();parser.add_argument('--baseline',type=Path);args=parser.parse_args()
	p=ROOT/'fonts/ttf/Scrivi-Regular.ttf';f=TTFont(p)
	assert f['name'].getDebugName(1)=='Scrivi'
	assert f['name'].getDebugName(4)=='Scrivi Regular'
	assert f['name'].getDebugName(6)=='Scrivi-Regular'
	assert f['name'].getDebugName(5)=='Version 1.004'
	assert f['name'].getDebugName(0)==(ROOT/'OFL.txt').read_text().splitlines()[0]
	assert 'https://github.com/r1zr7/scrivi' in f['name'].getDebugName(0)
	assert not any('AR Scrittura' in n.toUnicode() or 'ARScrittura' in n.toUnicode() for n in f['name'].names)
	result={'result':'PASS','author':'Alessandro Resch','family':'Scrivi','version':'1.004','sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
	if args.baseline:
		old=TTFont(args.baseline)
		for table in ['glyf','hmtx','hhea','cmap','GSUB','GPOS','GDEF','prep','gasp']:
			assert f.getTableData(table)==old.getTableData(table),table
		result['unchanged_from_previous_release']=['outlines','character_coverage','widths','vertical_metrics','kerning','mark_positioning','substitutions','hinting_program']
	(ROOT/'qa/rename-review.json').write_text(json.dumps(result,indent='\t',ensure_ascii=False)+'\n')
	print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
