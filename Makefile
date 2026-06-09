.PHONY: build check lint test verify

PYTHON ?= python3
XCODEBUILD ?= xcodebuild

lint:
	$(PYTHON) scripts/check-toothbrush-source.py --mode project

test:
	$(PYTHON) scripts/check-toothbrush-source.py --mode timer
	$(PYTHON) scripts/check-toothbrush-source.py --mode color
	$(PYTHON) scripts/check-toothbrush-source.py --mode accessibility

build: lint
	@if command -v "$(XCODEBUILD)" >/dev/null 2>&1; then \
		"$(XCODEBUILD)" -project toothbrush.xcodeproj -target toothbrush -sdk iphonesimulator CODE_SIGNING_ALLOWED=NO build; \
	else \
		echo "xcodebuild not found; static project checks completed"; \
	fi

verify: lint test build

check: verify
