# Author: Alessandro Resch. SIL OFL 1.1.
PYTHON ?= python3
.PHONY: build check
build:
	PYTHON="$(PYTHON)" bash sources/build.sh
check: build
	$(PYTHON) sources/verify_and_preview.py
	$(PYTHON) sources/release_checks.py
	$(PYTHON) sources/contour_review.py
	$(PYTHON) sources/special_forms_review.py
	$(PYTHON) sources/tall_accents_review.py
	$(PYTHON) sources/rename_review.py
