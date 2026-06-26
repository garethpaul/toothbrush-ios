# Toothbrush Timer Roadmap Reconciliation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use executing-plans to implement this plan task-by-task.

**Goal:** Reconcile Toothbrush iOS timer roadmap items that are already implemented and document the existing simulator-backed countdown and accessibility evidence.

**Architecture:** Preserve the Swift app, project, tests, workflow, Makefile, and timer behavior. Add fail-closed documentation contracts for pure completion, singular/plural grammar, controller/accessibility synchronization, stale-generation/reset coverage, hosted Xcode authority, roadmap history, and plan completion; then remove only the proven stale next-priority entries.

**Tech Stack:** Markdown, Python 3 static contracts, Swift 5, XCTest, GNU Make, GitHub Actions

---

## Status: Completed

### Task 1: Add The Documentation Contract

**Files:**
- Modify: `scripts/check-toothbrush-source.py`
- Test: `scripts/check-toothbrush-source.py`

**Step 1: Write the failing test**

Require a timer XCTest coverage section, exact maintained evidence, roadmap maintenance boundary, change-history record, and completed plan.

**Step 2: Run test to verify it fails**

Run: `python3 scripts/check-toothbrush-source.py --mode project`

Expected: FAIL because the README does not yet summarize the completed simulator-backed priorities and VISION still lists them as next work.

### Task 2: Reconcile Documentation

**Files:**
- Modify: `README.md`
- Modify: `VISION.md`
- Modify: `CHANGES.md`

**Step 1: Write minimal documentation**

Document the 15-test suite, pure completion and grammar boundaries, visible/accessibility synchronization, exactly-once reset and generation coverage, and hosted Xcode 16.4 authority. Remove the three completed next priorities and keep one explicit synchronization priority.

**Step 2: Run focused contracts**

Run: `python3 scripts/check-toothbrush-source.py --mode project`

Expected: PASS.

### Task 3: Prove Drift Fails Closed

**Files:**
- Test: `scripts/check-toothbrush-source.py`

**Step 1: Apply hostile mutations**

Mutate the coverage heading, test count, completion, grammar, accessibility, reset/generation, hosted authority, roadmap, change history, and plan status.

**Step 2: Verify each mutation fails**

Run the project source checker after each mutation.

Expected: every mutation is rejected.

### Task 4: Run The Full Gate

**Files:**
- Verify: `Makefile`

**Step 1: Run repository and external gates**

Run: `/usr/bin/make check`

Run: `cd "$(mktemp -d)" && /usr/bin/make -f /absolute/path/to/Makefile check`

Expected: portable source, timer, color, accessibility, workflow, and Make authority gates pass; hosted macOS supplies native XCTest evidence.

### Task 5: Commit And Ship

**Files:**
- Modify: `CHANGES.md`
- Modify: `docs/plans/2026-06-26-toothbrush-roadmap-reconciliation.md`

**Step 1: Record exact validation**

Add mutation, local gate, hosted XCTest, review, and blocker evidence.

**Step 2: Commit**

```bash
git add README.md VISION.md CHANGES.md scripts/check-toothbrush-source.py docs/plans/2026-06-26-toothbrush-roadmap-reconciliation.md
git commit -m "docs: reconcile toothbrush timer roadmap"
```

## Results

- Reconciled three stale next-priority entries against completed plans, source
  integration, static contracts, the 15-test shared XCTest suite, and hosted
  Xcode coverage.
- Added maintained guidance for pure completion, singular/plural grammar,
  visible/accessibility synchronization, exactly-once reset, stale generations,
  activation, prompt state, and weak timer ownership.
- Rejected 11 hostile documentation mutations.
- Passed `/usr/bin/make check` from the checkout and an external working
  directory; Linux ran all portable contracts and reported the documented
  native Xcode skip. Hosted Xcode 16.4 remains the XCTest authority.
