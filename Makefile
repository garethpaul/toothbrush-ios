.PHONY: build check lint test verify

ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
PYTHON ?= python3
XCODEBUILD ?= xcodebuild

lint:
	$(PYTHON) "$(ROOT)/scripts/check-toothbrush-source.py" --mode project

test:
	$(PYTHON) "$(ROOT)/scripts/check-toothbrush-source.py" --mode timer
	$(PYTHON) "$(ROOT)/scripts/check-toothbrush-source.py" --mode color
	$(PYTHON) "$(ROOT)/scripts/check-toothbrush-source.py" --mode accessibility

build: lint
	@if command -v "$(XCODEBUILD)" >/dev/null 2>&1; then \
		"$(XCODEBUILD)" -project "$(ROOT)/toothbrush.xcodeproj" -target toothbrushTests -sdk iphonesimulator -configuration Debug CODE_SIGNING_ALLOWED=NO build; \
	else \
		echo "xcodebuild not found; static project checks completed"; \
	fi

verify: lint test build

check: verify
