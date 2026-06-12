# Toothbrush iOS CI Baseline

Status: Completed

## Context

The app has an SDK-free `make check` baseline for project metadata, timer
lifecycle, color parsing, accessibility, docs, and plan coverage. Full app
verification still requires macOS and Xcode. The missing guard was hosted CI for
the static baseline.

## Changes

- Added `.github/workflows/check.yml` for GitHub Actions.
- Ran the Python static baseline on Ubuntu with Python 3.12.
- Kept full simulator/device verification documented as a macOS toolchain task.
- Extended the checker and docs so hosted CI stays visible.

## Verification

- `make check`
- `git diff --check`
