# Timer Generation Deep Review Implementation Plan

## Status: Completed

> **For Claude:** REQUIRED SUB-SKILL: Use test-driven-development to implement this plan task-by-task.

**Goal:** Make the brushing countdown robust against extreme time values, stale timer callbacks, and duplicate terminal reconciliation while preserving the two-minute UI.

**Architecture:** Keep deadline arithmetic in pure helpers, but make conversion total by clamping invalid or unrepresentable intervals. Keep timer ownership in `ViewController`; assign each run a generation and ignore callbacks from previous or cancelled runs. Treat an absent deadline as an inactive session rather than another completion event.

**Tech Stack:** Swift 5, UIKit, Foundation `Timer`, XCTest, Python static contracts, GitHub Actions Xcode 16.4.

---

### Task 1: Prove arithmetic and terminal failures

**Files:**
- Modify: `toothbrushTests/toothbrushTests.swift`

1. Add a failing test showing an extreme finite interval must clamp instead of trapping during `Int` conversion.
2. Add a failing controller test showing repeated reconciliation after completion must not execute the shared reset twice.
3. Run the focused XCTest cases and record the expected failures.

### Task 2: Harden deadline conversion

**Files:**
- Modify: `toothbrush/ViewController.swift`
- Modify: `toothbrushTests/toothbrushTests.swift`

1. Reject non-finite inputs as completed.
2. Clamp positive intervals larger than `Int.max`.
3. Run the arithmetic XCTest cases until green.

### Task 3: Own timer generations

**Files:**
- Modify: `toothbrush/ViewController.swift`
- Modify: `toothbrushTests/toothbrushTests.swift`
- Modify: `scripts/check-toothbrush-source.py`

1. Add a monotonically changing generation for every start and reset.
2. Capture the generation in the timer callback and ignore stale callbacks.
3. Return immediately when reconciliation has no active deadline.
4. Add restart, cancellation, and exactly-once completion tests.
5. Extend static contracts so generation checks cannot be removed silently.

### Task 4: Verify and land the stack

**Files:**
- Modify: `CHANGES.md`

1. Run focused XCTest, all XCTest, static contracts, and external-directory `make check` where feasible.
2. Run hostile mutations against arithmetic clamping, inactive reconciliation, and generation checks.
3. Scan the current tree and full history for credentials without printing values.
4. Push one consolidation branch, wait for hosted Check and CodeQL, merge, and close superseded PRs.

## Verification

- Focused red/green XCTest reproduced duplicate terminal reset and an extreme
  interval conversion trap before the fixes.
- All native XCTest cases passed on an iPhone 16 Pro simulator with Xcode 26.
- Repository-root and external-directory `make check` passed with native Xcode
  execution covered separately.
- Hostile mutations covering interval clamping, inactive reconciliation, and
  timer generation ownership were rejected by XCTest or static contracts.
- Current-tree and full-history credential scans completed without printing
  candidate values.
