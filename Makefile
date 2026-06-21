.DEFAULT_GOAL := check
.PHONY: __repository-make-authority build check contract-test lint root-test test verify
.SECONDEXPANSION:

PYTHON ?= python3
XCODEBUILD ?= xcodebuild
override PYTHON := $(value PYTHON)
override XCODEBUILD := $(value XCODEBUILD)
export PYTHON XCODEBUILD
override REPOSITORY_MAKE_DOLLAR := $$
override REPOSITORY_MAKE_OPEN := (
ifneq ($(findstring $(REPOSITORY_MAKE_DOLLAR)$(REPOSITORY_MAKE_OPEN),$(value PYTHON)),)
$(error PYTHON must be a literal executable path, not Make syntax)
endif
ifneq ($(findstring $(REPOSITORY_MAKE_DOLLAR)$(REPOSITORY_MAKE_OPEN),$(value XCODEBUILD)),)
$(error XCODEBUILD must be a literal executable path, not Make syntax)
endif
override SHELL := /bin/sh
override .SHELLFLAGS := -c

ifneq ($(filter command line,$(origin MAKEFLAGS)),)
$(error MAKEFLAGS must not be overridden for repository verification)
endif
override REPOSITORY_MAKE_FIRST_FLAGS := $(firstword $(MAKEFLAGS))
ifneq ($(filter -%,$(REPOSITORY_MAKE_FIRST_FLAGS)),)
override REPOSITORY_MAKE_FIRST_FLAGS :=
endif
override REPOSITORY_MAKE_SHORT_FLAGS := $(REPOSITORY_MAKE_FIRST_FLAGS) $(filter-out --%,$(filter -%,$(MAKEFLAGS)))
ifneq ($(findstring n,$(REPOSITORY_MAKE_SHORT_FLAGS)),)
$(error non-executing or error-ignoring MAKEFLAGS are not supported for repository verification)
endif
ifneq ($(findstring t,$(REPOSITORY_MAKE_SHORT_FLAGS)),)
$(error non-executing or error-ignoring MAKEFLAGS are not supported for repository verification)
endif
ifneq ($(findstring q,$(REPOSITORY_MAKE_SHORT_FLAGS)),)
$(error non-executing or error-ignoring MAKEFLAGS are not supported for repository verification)
endif
ifneq ($(findstring i,$(REPOSITORY_MAKE_SHORT_FLAGS)),)
$(error non-executing or error-ignoring MAKEFLAGS are not supported for repository verification)
endif
ifneq ($(filter --just-print --dry-run --recon --touch --question --ignore-errors,$(MAKEFLAGS)),)
$(error non-executing or error-ignoring MAKEFLAGS are not supported for repository verification)
endif
ifneq ($(strip $(MAKEFILES)),)
$(error MAKEFILES must be empty; repository verification requires this Makefile to be loaded alone)
endif
override MAKEFILES :=
ifneq ($(origin MAKEFILE_LIST),file)
$(error MAKEFILE_LIST must not be overridden)
endif
override ROOT := $(shell path='$(subst ','"'"',$(value MAKEFILE_LIST))'; path=$$(printf '%s' "$$path" | /usr/bin/sed 's/^ //'); [ -f "$$path" ] || exit 1; directory=$$(/usr/bin/dirname -- "$$path"); CDPATH= cd -- "$$directory" && /bin/pwd -P)
export ROOT
ifeq ($(strip $(ROOT)),)
$(error repository Makefile path could not be resolved)
endif

build check contract-test lint root-test test verify: $$(if $$(filter file,$$(origin MAKEFILE_LIST)),,$$(error MAKEFILE_LIST must not be overridden))
build check contract-test lint root-test test verify: $$(if $$(shell path=$$$$(/usr/bin/printf '%s' '$$(subst ','"'"',$$(MAKEFILE_LIST))' | /usr/bin/sed 's/^ //') && [ -f "$$$$path" ] && /usr/bin/printf '%s' ok),,$$(error repository Makefile must be loaded alone))
build check contract-test lint root-test test verify: __repository-make-authority

__repository-make-authority::
	@:

lint:
	"$$PYTHON" "$$ROOT/scripts/check-toothbrush-source.py" --mode project

test:
	"$$PYTHON" "$$ROOT/scripts/check-toothbrush-source.py" --mode timer
	"$$PYTHON" "$$ROOT/scripts/check-toothbrush-source.py" --mode color
	"$$PYTHON" "$$ROOT/scripts/check-toothbrush-source.py" --mode accessibility
	@if command -v "$$XCODEBUILD" >/dev/null 2>&1; then \
		"$$XCODEBUILD" -project "$$ROOT/toothbrush.xcodeproj" -scheme toothbrush -destination 'platform=iOS Simulator,name=iPhone 16 Pro,OS=18.5' -configuration Debug CODE_SIGNING_ALLOWED=NO test; \
	else \
		echo "xcodebuild not found; static XCTest contracts completed"; \
	fi

contract-test:
	"$$PYTHON" "$$ROOT/scripts/test_workflow_contract.py"

build: lint
	@if command -v "$$XCODEBUILD" >/dev/null 2>&1; then \
		"$$XCODEBUILD" -project "$$ROOT/toothbrush.xcodeproj" -target toothbrushTests -sdk iphonesimulator -configuration Debug CODE_SIGNING_ALLOWED=NO ONLY_ACTIVE_ARCH=NO DISABLE_MANUAL_TARGET_ORDER_BUILD_WARNING=YES build; \
	else \
		echo "xcodebuild not found; static project checks completed"; \
	fi

root-test:
	/bin/sh "$$ROOT/scripts/test-makefile-root.sh"

verify: root-test lint contract-test test build

check: verify
