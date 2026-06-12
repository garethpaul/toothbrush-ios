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
- Keep timer accessibility labels and values synchronized with visible state
- Keep shared timer resets synchronized with countdown state
- Keep prompt animation state deterministic after shared timer resets
- Keep repeating countdown timers tolerant enough for efficient scheduling
- Keep countdown ticks active during normal UI tracking interactions
- Keep the two-minute interval accurate when timer callbacks are delayed
- Keep custom navigation views tied to controller appearance, disappearance,
  and teardown
- Keep the custom navigation logo centered after layout changes
- Stop active countdown timers when the view leaves screen
- Maintain the app GIF as behavior context
- Keep completed maintenance plans under `docs/plans`
- Keep GitHub Actions aligned with both portable contracts and Xcode compilation
- Keep the Swift 5, Xcode 16.4, and iOS 12 baseline explicit
- Compile the app and XCTest target before merging

Next priorities:

- Add a completion state that is testable without waiting two minutes
- Add a shared scheme for hosted XCTest execution
- Add simulator-backed accessibility assertions when Xcode is available

Contribution rules:

- One PR = one focused timer, UI, accessibility, test, or documentation change.
- Keep the app local and offline.
- Include simulator notes for behavior changes.
- Avoid expanding scope beyond brushing guidance without a product note.

## Security And Responsible Use

Canonical security policy and reporting:

- [`SECURITY.md`](SECURITY.md)

The app should remain a local timer. It should not collect health, habit, or
device data unless an explicit privacy model is added.

## What We Will Not Merge (For Now)

- Hidden analytics
- Network-backed habit tracking
- Health data collection
- Countdown timers that retain dismissed controllers
- Prompt animation state that survives timer reset
- Custom navigation views with stale layout after size changes
- Broad redesigns that obscure the simple timer purpose

This list is a roadmap guardrail, not a permanent rule.
Strong user demand and strong technical rationale can change it.
