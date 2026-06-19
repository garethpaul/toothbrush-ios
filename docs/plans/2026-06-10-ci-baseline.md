# Toothbrush iOS Static Contract Gate

## Status: Completed

## Context

The app has an SDK-free `make check` baseline for project metadata, timer
lifecycle, color parsing, accessibility, documentation, and completed plans.
Full compilation and runtime verification require macOS, Xcode, a simulator,
or a device, but the portable contracts previously had no hosted gate.

## Objectives

- Run all portable contracts on pushes and pull requests.
- Keep the workflow least-privilege, immutable, and bounded.
- Preserve a manual trigger for maintenance verification.
- State clearly that Linux does not validate the iOS build or runtime.

## Work Completed

- Added `.github/workflows/check.yml` for pushes to `master`, pull requests,
  and manual runs.
- Granted only read access to repository contents, disabled persisted checkout
  credentials, and bounded both hosted jobs with timeouts.
- Pinned checkout and Python setup actions to immutable Node 24 commits.
- Ran the existing `make check` entry point with Python 3.12.
- Added an Xcode 16.4 simulator compilation job for the app and XCTest target.
- Extended the project checker to enforce the workflow contract.
- Updated README, SECURITY, VISION, and CHANGES with the hosted baseline.

## Verification

- `python3 -m py_compile scripts/check-toothbrush-source.py`
- `python3 scripts/check-toothbrush-source.py --mode project`
- `python3 scripts/check-toothbrush-source.py --mode timer`
- `python3 scripts/check-toothbrush-source.py --mode color`
- `python3 scripts/check-toothbrush-source.py --mode accessibility`
- `make check`
- `git diff --check`

The Linux job validates portable source and repository contracts only. The
macOS job compiles Swift and XCTest sources but does not launch a simulator or
exercise device lifecycle behavior.
