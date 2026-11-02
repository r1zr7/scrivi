#!/usr/bin/env bash
# Author: Alessandro Resch. SIL OFL 1.1.
set -euo pipefail
scrivi_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
"${PYTHON:-python3}" "$scrivi_root/sources/build_font.py"
mkdir -p "$scrivi_root/fonts/ttf/article"
cp "$scrivi_root/documentation/article/ARTICLE.en_us.html" "$scrivi_root/fonts/ttf/article/ARTICLE.en_us.html"
cp "$scrivi_root/documentation/article/scrivi-specimen.png" "$scrivi_root/fonts/ttf/article/scrivi-specimen.png"
