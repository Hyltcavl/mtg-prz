.PHONY: venv dl_scan dl_scan_short alpha_scan alpha_scan_short price
VERSION_PYTHON=python3.12
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
	.venv/bin/$(VERSION_PYTHON) -m src.dl_scan.main

dl_scan_short:
	$(VENV_ACTIVATE)
	echo "" > log.txt
	SHORT=true .venv/bin/$(VERSION_PYTHON) -m src.dl_scan.main

alpha_scan:
	$(VENV_ACTIVATE)
	echo "" > log.txt
	.venv/bin/$(VERSION_PYTHON) -m src.alpha_scan.main

alpha_scan_short:
	$(VENV_ACTIVATE)
	echo "" > log.txt
	SHORT=true .venv/bin/$(VERSION_PYTHON) -m src.alpha_scan.main

price:
	$(VENV_ACTIVATE)
	echo "" > log.txt
	.venv/bin/$(VERSION_PYTHON) -m src.price_compare.main

test:
	$(VENV_ACTIVATE)
	.venv/bin/pytest -c ./pytest.ini
