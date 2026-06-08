# Changes

## 2026-06-08

- Added a Makefile verification gate for project metadata and timer lifecycle
  source checks.
- Fixed repeated Start taps so an existing countdown timer is invalidated before
  scheduling a new one.
- Clamped countdown completion at zero and stopped repeating brush-text
  animations when the timer finishes.
- Invalidated the timer when the view controller is deallocated.
