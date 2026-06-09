# toothbrush-ios

<!-- README-OVERVIEW-IMAGE -->
![Project overview](docs/readme-overview.svg)

## Overview

`garethpaul/toothbrush-ios` is an Apple platform application or Swift sample. A toothbrush companion app. 

This README is based on the checked-in source, manifests, scripts, and repository metadata on the `master` branch. The project language mix found during review was: Swift (4).

## Repository Contents

- `README.md` - project overview and local usage notes
- `CHANGES.md` - maintenance history for timer and color checks
- `Makefile` - local verification entry points
- `docs/plans` - completed maintenance plans for the current baseline
- `img` - GIF behavior reference
- `plans` - historical implementation notes
- `scripts` - static project, timer, and color validators
- `SECURITY.md` - security reporting and disclosure guidance
- `toothbrush` - source or example code
- `toothbrush.xcodeproj` - Xcode project file
- `toothbrushTests` - source or example code
- `VISION.md` - project direction and maintenance guardrails

Additional scan context:

- Source directories: toothbrush, toothbrushTests
- Dependency and build manifests: none detected
- Entry points or build surfaces: toothbrush.xcodeproj
- Test-looking files: toothbrushTests/Info.plist, toothbrushTests/toothbrushTests.swift

## Getting Started

### Prerequisites

- Git
- macOS with Xcode for building Apple platform projects
- Python 3 for repository source checks

### Setup

```bash
git clone https://github.com/garethpaul/toothbrush-ios.git
cd toothbrush-ios
```

The setup commands above are derived from repository files. Legacy mobile, Python, or JavaScript samples may require older SDKs or package versions than a modern workstation uses by default.

## Running or Using the Project

- Open `toothbrush.xcodeproj` in Xcode, choose the app or sample scheme, and run it on the matching simulator/device.

## Testing and Verification

- `make check` runs static project checks, timer lifecycle checks, hex color
  parser checks, and timer accessibility checks. When `xcodebuild` is
  installed, the `build` target also attempts an iOS simulator build with code
  signing disabled.
- Timer lifecycle checks also require teardown to invalidate timers and remove
  the custom navigation logo view. They also require view disappearance to stop
  an active timer through the shared reset path.
- Static project checks also require completed canonical plans under `docs/plans`.
- Xcode's test action or `xcodebuild test` with the appropriate scheme and
  destination can be used on macOS for deeper verification.

When the required SDK or runtime is unavailable, use static checks and source review first, then verify on a machine that has the matching platform toolchain.

## Configuration and Secrets

- No required secret or credential file was identified in the repository scan. If you add integrations later, keep secrets out of git.

## Security and Privacy Notes

- Review changes touching network requests, sockets, or service endpoints; examples from the scan include toothbrush/Info.plist, toothbrushTests/Info.plist.
- Review changes touching file, media, JSON, XML, CSV, OCR, or data parsing; examples from the scan include toothbrush/Info.plist, toothbrush/ViewController.swift, toothbrushTests/Info.plist.

## Maintenance Notes

- This looks like an Apple platform project or sample. Xcode, Swift, CocoaPods, and deployment target versions may need to match the original project era.
- See `SECURITY.md` for vulnerability reporting and safe research guidance.
- See `VISION.md` for project direction and contribution guardrails.
- See `docs/plans/2026-06-08-toothbrush-ios-baseline.md` for the canonical
  timer and color validation baseline.
- See `docs/plans/2026-06-08-timer-accessibility.md` for timer accessibility
  label coverage.
- See `docs/plans/2026-06-08-navigation-logo-teardown.md` for navigation logo
  teardown coverage.
- See `docs/plans/2026-06-09-view-disappear-timer-reset.md` for the
  view-disappear timer reset guard.

## Contributing

Keep changes small and tied to the project that is already present in this repository. For code changes, document the toolchain used, avoid committing generated dependency directories or local configuration, and update this README when setup or verification steps change.
