# Changes

## 2026-06-08

- Removed the custom navigation logo during controller teardown and tightened
  the static deinit lifecycle check.
- Ignored Python bytecode caches produced by local checker syntax validation.
- Added timer/start/prompt accessibility labels and static checks that keep the
  timer accessibility value synchronized with visible countdown text.
- Added `make check` as the shared repository verification alias.
- Hardened the hex color helper so invalid or partially parsed color strings
  fall back to gray instead of silently becoming black.
- Extended `make test` with a source check for hex color parser validation.
- Added a Makefile verification gate for project metadata and timer lifecycle
  source checks.
- Fixed repeated Start taps so an existing countdown timer is invalidated before
  scheduling a new one.
- Clamped countdown completion at zero and stopped repeating brush-text
  animations when the timer finishes.
- Invalidated the timer when the view controller is deallocated.
- Added canonical `docs/plans` coverage and made project checks require
  completed plans.
