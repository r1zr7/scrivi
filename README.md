# AR Scrittura

Author and designer: **Alessandro Resch**.

AR Scrittura is an original, upright monoline handwriting typeface for names,
headings and short messages. It uses simple separated letters, compact spacing
and minimal flourishes. One style: Regular (400), visually light.

The font family name **AR Scrittura** was approved by its author on 27 October
2026. The AR-Scrittura spelling may still be used in project branding. This package
contains only the approved technical family, not the earlier hyphenated alternative.

## Status

Public release **1.003** raises the accents on ĥ, ȟ and ǩ above their ascenders.
Only these three encoded outlines changed from 1.002. All advances are retained;
GPOS now places combining accents above tall lowercase h/k, consistently with l.
See `specimen/accenti-alti-prima-dopo.png`. The author approved the corrected samples at large and small sizes. The corrected long s and kra from 1.002 passed the author's visual review.

Corrections retained from the 1.001 contour review:
- l acute (ĺ): separated the acute from the ascender, with matching GPOS positioning.
- Romanian comma below: separated it from Ș/ș; the same combining mark correction
  applies to Ț/ț and decomposed sequences.
- Dotted circle: twelve larger, distinct dots for better small-size visibility.
All advance widths and the previously approved side-caron outlines are unchanged.
The comparison image is in `specimen/contorni-prima-dopo.png`. FontBakery 1.1.0 results:

| Profile | PASS | FAIL | WARN | INFO | SKIP |
|---|---:|---:|---:|---:|---:|
| Universal | 80 | 0 | 3 | 3 | 41 |
| Google Fonts | 109 | 0 | 7 | 8 | 112 |

No local exceptions or disabled checks were used. These results are not catalog
admission. Author initials and the naming of a light single-weight family still
need review by Google Fonts. See `PUBBLICAZIONE.md` for all remaining steps.

392 encoded characters, including complete GF Latin Core, ASCII, Latin-1 Supplement
and Latin Extended-A. Combining marks, mark-to-mark positioning, dotless alternates
and 21 kerning pairs are included. No Greek, Cyrillic or Arabic coverage is claimed.

## Install and use

Desktop: install `fonts/ARScrittura-Regular.ttf`. Remove the older preview if it
is already installed, then restart applications that cache font information.

Web: copy `web/` and include `web/ar-scrittura.css`.
Use `font-family: 'AR Scrittura'; font-weight: 400; font-synthesis: none;`.
The CSS class `.ar-scrittura` is provided. The web font remains fully self-hosted.
Open `Anteprima.html` to test it offline.

## Open sources and build

The original stroke drawings are in `sources/glyphs.json`. The editable generated
outline source is `sources/AR-Scrittura-Regular.ufo`. Its filename is a source path;
the family inside it is AR Scrittura. The pipeline expands original strokes,
exports UFO, compiles through Fontmake and generates TTF/WOFF2 with release metadata.
No external font is copied or embedded.

Use Python 3.12 in a virtual environment:

```sh
python -m pip install -r sources/requirements-qa.txt
python sources/build_font.py
python sources/verify_and_preview.py
python sources/release_checks.py
python sources/contour_review.py
python sources/special_forms_review.py
python sources/tall_accents_review.py
python -m fontbakery check-googlefonts fonts/ARScrittura-Regular.ttf --json qa/fontbakery-googlefonts.json --html qa/fontbakery-googlefonts.html
```

The build regenerates and overwrites the included UFO. Preserve manual editor
changes in a separate working copy. Build timestamps are fixed to 2026-10-27 UTC.
604 additional assertions pass, including byte-identical rebuilds in the tested
Linux environment. No Windows or macOS execution is claimed by these reports.
Specimen captions use a system font or Pillow fallback; no UI font is bundled.

## License

SIL Open Font License 1.1, no Reserved Font Name. See `OFL.txt`.
Personal and commercial use, embedding and redistribution are allowed under the OFL.
Copyright holder: Alessandro Resch. The font, drawings, UFO, scripts and specimens
in this package are OFL-licensed. The separately reserved AR brand monogram is not
included. All third-party build tools retain their own licenses.

Project presentation: https://ar-scrittura.workspace-833185.chatgpt.site/
The public upstream repository URL will be added after authorized account access.

## Direct distribution

This package can be hosted on the author's own website. The complete TTF and
WOFF2 retain all 392 encoded characters. No Google Fonts service is needed.
See `USO-WEB.txt` for local hosting and `TESTO-PRESENTAZIONE.txt` for the Italian
release description. Google Fonts submission remains pending; the working
materials in `submission/` are drafts, not an accepted catalog entry.
Author: Alessandro Resch. Public package prepared on 29 October 2026.

## Public upstream repository

https://github.com/r1zr7/ar-scrittura

The repository was created on 1 November 2026. This initial import preserves
version 1.003 binaries and their matching OFL copyright line. Updating the font
copyright URL for catalog onboarding requires a subsequent binary revision.

## AI assistance

ChatGPT/Codex assisted drawing construction, font engineering, build scripts,
testing, documentation and release preparation. Alessandro Resch directed the
design decisions and reviewed the visual specimens. Google Fonts naming policy,
CLA, residual warnings and editorial approval remain open; a preliminary review request was published at
https://github.com/google/fonts/issues/11207 on 1 November 2026. The font is
not admitted to Google Fonts.
