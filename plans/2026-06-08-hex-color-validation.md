# Hex Color Validation Gate

## Problem

The app uses a helper to convert branded hex strings into `UIColor` values.
Before this pass, the helper ignored `scanHexInt` failures, so a malformed
six-character string could silently resolve as black instead of the existing
gray fallback used for invalid lengths.

## TDD Evidence

1. Extended `scripts/check-toothbrush-source.py` and `make test` with a color
   parser validation mode.
2. Ran `make test` before changing `Hex.swift` and confirmed the new color
   checks failed against the ignored scanner result.
3. Updated the parser to validate scanner success and full-string consumption,
   then reran the full verification gate.

## Verification

- `make lint`
- `make test`
- `make build`
- `make verify`
- `git diff --check`
