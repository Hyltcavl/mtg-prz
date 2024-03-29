.PHONY: venv
VERSION_PYTHON=python3.10
VENV_ACTIVATE = . .venv/bin/activate
BIN_ECHO=/bin/echo

venv:
	$(VERSION_PYTHON) -m venv .venv
	$(VENV_ACTIVATE)
	.venv/bin/$(VERSION_PYTHON) -m pip install --upgrade pip
	.venv/bin/$(VERSION_PYTHON) -m pip install -r requirements.txt

dl_scan:
	$(VENV_ACTIVATE)
	echo "" > log.txt
	DEBUG="yes" .venv/bin/$(VERSION_PYTHON) -m src.dl_scan.main | tee log.json

alpha_scan:
	$(VENV_ACTIVATE)
	echo "" > log.txt
	DEBUG="yes" .venv/bin/$(VERSION_PYTHON) -m src.alpha_scan.main

price_check:
	$(VENV_ACTIVATE)
	echo "" > log.txt
	DEBUG="yes" .venv/bin/$(VERSION_PYTHON) -m src.scryfall_price_compare.main | tee log.json