.PHONY: build check lint test verify

override ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
PYTHON ?= python3
XCODEBUILD ?= xcodebuild

lint:
	$(PYTHON) "$(ROOT)/scripts/check-toothbrush-source.py" --mode project

test:
	$(PYTHON) "$(ROOT)/scripts/check-toothbrush-source.py" --mode timer
	$(PYTHON) "$(ROOT)/scripts/check-toothbrush-source.py" --mode color
	$(PYTHON) "$(ROOT)/scripts/check-toothbrush-source.py" --mode accessibility
	@if command -v "$(XCODEBUILD)" >/dev/null 2>&1; then \
		"$(XCODEBUILD)" -project "$(ROOT)/toothbrush.xcodeproj" -scheme toothbrush -destination 'platform=iOS Simulator,name=iPhone 16 Pro,OS=18.5' -configuration Debug CODE_SIGNING_ALLOWED=NO test; \
	else \
		echo "xcodebuild not found; static XCTest contracts completed"; \
	fi

build: lint
	@if command -v "$(XCODEBUILD)" >/dev/null 2>&1; then \
		"$(XCODEBUILD)" -project "$(ROOT)/toothbrush.xcodeproj" -target toothbrushTests -sdk iphonesimulator -configuration Debug CODE_SIGNING_ALLOWED=NO ONLY_ACTIVE_ARCH=NO DISABLE_MANUAL_TARGET_ORDER_BUILD_WARNING=YES build; \
	else \
		echo "xcodebuild not found; static project checks completed"; \
	fi

verify: lint test build

check: verify
