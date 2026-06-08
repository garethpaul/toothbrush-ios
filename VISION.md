## Toothbrush iOS Vision

Toothbrush iOS is a small Swift app that runs a two-minute brushing timer with
simple branding and animated prompt text.

The repository is useful as a focused iOS timer prototype with one primary
interaction: start the timer, count down, and reveal the start button again at
completion.

The goal is to preserve the simple timer behavior while making the app easier
to build and verify on modern iOS tooling.

The current focus is:

Priority:

- Preserve the 120-second countdown flow
- Keep the start/reset visual state obvious
- Maintain the app GIF as behavior context
- Treat Swift and Xcode versions as legacy until documented

Next priorities:

- Add README setup notes for Xcode and simulator versions
- Add a completion state that is testable without waiting two minutes
- Modernize timer APIs and Swift syntax in a dedicated pass
- Add accessibility labels for the timer and start button

Contribution rules:

- One PR = one focused timer, UI, accessibility, test, or documentation change.
- Keep the app local and offline.
- Include simulator notes for behavior changes.
- Avoid expanding scope beyond brushing guidance without a product note.

## Security And Responsible Use

The app should remain a local timer. It should not collect health, habit, or
device data unless an explicit privacy model is added.

## What We Will Not Merge (For Now)

- Hidden analytics
- Network-backed habit tracking
- Health data collection
- Broad redesigns that obscure the simple timer purpose
