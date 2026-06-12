#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS_PLANS = ROOT / "docs" / "plans"
CANONICAL_PLAN = DOCS_PLANS / "2026-06-08-toothbrush-ios-baseline.md"
NAVIGATION_LOGO_LIFECYCLE_PLAN = DOCS_PLANS / "2026-06-09-navigation-logo-lifecycle.md"
TIMER_RUN_LOOP_PLAN = DOCS_PLANS / "2026-06-09-timer-run-loop-modes.md"
NAVIGATION_LOGO_LAYOUT_PLAN = DOCS_PLANS / "2026-06-09-navigation-logo-layout.md"
CI_PLAN = DOCS_PLANS / "2026-06-10-ci-baseline.md"
MODERNIZATION_PLAN = DOCS_PLANS / "2026-06-10-swift-5-xcode-build.md"
DEADLINE_TIMER_PLAN = DOCS_PLANS / "2026-06-10-deadline-countdown.md"
CI_WORKFLOW = ROOT / ".github/workflows/check.yml"
CHECKOUT_ACTION = "actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10"
SETUP_PYTHON_ACTION = "actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405"
ALLOWED_ACTIONS = {"actions/checkout", "actions/setup-python"}


def read_text(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8")


def require_paths():
    errors = []
    for relative_path in (
        "toothbrush.xcodeproj/project.pbxproj",
        "toothbrush/ViewController.swift",
        "toothbrush/Hex.swift",
        "toothbrush/Info.plist",
        "toothbrushTests/toothbrushTests.swift",
        "toothbrush/Images.xcassets/AppIcon.appiconset/Icon-83.5@2x.png",
        "toothbrush/Images.xcassets/AppIcon.appiconset/Icon-AppStore-1024.png",
    ):
        if not (ROOT / relative_path).exists():
            errors.append(f"missing required file: {relative_path}")
    return errors


def docs_plan_checks():
    errors = []
    if not CANONICAL_PLAN.exists():
        errors.append("docs/plans/2026-06-08-toothbrush-ios-baseline.md is missing")
    if not NAVIGATION_LOGO_LIFECYCLE_PLAN.exists():
        errors.append("docs/plans/2026-06-09-navigation-logo-lifecycle.md is missing")
    if not TIMER_RUN_LOOP_PLAN.exists():
        errors.append("docs/plans/2026-06-09-timer-run-loop-modes.md is missing")
    if not NAVIGATION_LOGO_LAYOUT_PLAN.exists():
        errors.append("docs/plans/2026-06-09-navigation-logo-layout.md is missing")
    if not CI_PLAN.exists():
        errors.append("docs/plans/2026-06-10-ci-baseline.md is missing")
    if not MODERNIZATION_PLAN.exists():
        errors.append("docs/plans/2026-06-10-swift-5-xcode-build.md is missing")
    if not DEADLINE_TIMER_PLAN.exists():
        errors.append("docs/plans/2026-06-10-deadline-countdown.md is missing")
    if not CI_WORKFLOW.exists():
        errors.append(".github/workflows/check.yml is missing")

    plans = sorted(DOCS_PLANS.glob("*.md")) if DOCS_PLANS.exists() else []
    if not plans:
        errors.append("docs/plans must contain at least one completed plan")

    for plan_path in plans:
        plan = plan_path.read_text(encoding="utf-8")
        if "Status: Completed" not in plan or "make check" not in plan:
            errors.append(f"{plan_path.relative_to(ROOT)} must record completed status and make check verification")

    return errors


def project_checks():
    errors = docs_plan_checks() + require_paths()
    if errors:
        return errors

    workflow = read_text(".github/workflows/check.yml")
    for fragment in (
        "permissions:",
        "contents: read",
        "workflow_dispatch:",
        "concurrency:",
        "cancel-in-progress: true",
        "runs-on: ubuntu-24.04",
        "runs-on: macos-15",
        "timeout-minutes: 5",
        "timeout-minutes: 15",
        "DEVELOPER_DIR: /Applications/Xcode_16.4.app/Contents/Developer",
        f"{CHECKOUT_ACTION} # v6.0.3",
        f"{SETUP_PYTHON_ACTION} # v6.2.0",
        "persist-credentials: false",
        'python-version: "3.12"',
        "run: make check",
        "run: make build",
    ):
        if fragment not in workflow:
            errors.append(f"GitHub Actions workflow is missing expected setting: {fragment}")
    if workflow.count(f"uses: {CHECKOUT_ACTION}") != 2:
        errors.append("GitHub Actions workflow must use the approved checkout action twice")
    if workflow.count(f"uses: {SETUP_PYTHON_ACTION}") != 1:
        errors.append("GitHub Actions workflow must use the approved Python setup action once")
    if workflow.count("persist-credentials: false") != 2:
        errors.append("GitHub Actions checkout steps must not persist credentials")
    if not re.search(r"(?m)^permissions:\n  contents: read\n\nconcurrency:", workflow):
        errors.append("GitHub Actions workflow must keep exact read-only top-level permissions")
    if "pull_request_target:" in workflow:
        errors.append("GitHub Actions workflow must not use pull_request_target")
    for action, revision in re.findall(
        r"^\s*(?:-\s*)?uses:\s*([^@\s]+)@([^\s#]+)", workflow, flags=re.MULTILINE
    ):
        if action not in ALLOWED_ACTIONS:
            errors.append(f"GitHub Actions action {action} is not approved")
        if not re.fullmatch(r"[a-f0-9]{40}", revision):
            errors.append(f"GitHub Actions action {action} must be pinned to a full commit SHA")

    for docs_path in ("README.md", "VISION.md", "SECURITY.md", "CHANGES.md"):
        if "GitHub Actions" not in read_text(docs_path):
            errors.append(f"{docs_path} must mention the GitHub Actions baseline")

    project = read_text("toothbrush.xcodeproj/project.pbxproj")
    for fragment in (
        "toothbrushTests",
        "IPHONEOS_DEPLOYMENT_TARGET = 12.0;",
        "SWIFT_VERSION = 5.0;",
        "PRODUCT_BUNDLE_IDENTIFIER = com.garethpaul.toothbrush;",
        "PRODUCT_BUNDLE_IDENTIFIER = com.garethpaul.toothbrushTests;",
    ):
        if fragment not in project:
            errors.append(f"project is missing expected setting: {fragment}")
    if "IPHONEOS_DEPLOYMENT_TARGET = 8.3;" in project:
        errors.append("project must not retain the unsupported iOS 8.3 deployment target")

    makefile = read_text("Makefile")
    for fragment in (
        "ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))",
        "-target toothbrushTests",
        "-sdk iphonesimulator",
        "CODE_SIGNING_ALLOWED=NO",
        "ONLY_ACTIVE_ARCH=NO",
        "DISABLE_MANUAL_TARGET_ORDER_BUILD_WARNING=YES",
    ):
        if fragment not in makefile:
            errors.append(f"Makefile is missing expected build setting: {fragment}")

    app_delegate = read_text("toothbrush/AppDelegate.swift")
    if "@main" not in app_delegate or "UIApplication.LaunchOptionsKey" not in app_delegate:
        errors.append("AppDelegate must use the modern Swift application entry point")

    view_controller = read_text("toothbrush/ViewController.swift")
    legacy_fragments = (
        "@UIApplicationMain",
        "NSTimer",
        "NSRunLoop",
        "CGRectMake",
        "imageWithRenderingMode",
        "animateWithDuration",
        ".hidden =",
        "second--",
    )
    combined_source = app_delegate + view_controller
    for fragment in legacy_fragments:
        if fragment in combined_source:
            errors.append(f"Swift 2-era API must not return: {fragment}")

    app_plist = read_text("toothbrush/Info.plist")
    if "<string>armv7</string>" in app_plist:
        errors.append("app plist must not require the obsolete armv7 capability")
    if "$(PRODUCT_BUNDLE_IDENTIFIER)" not in app_plist:
        errors.append("app plist must use the target product bundle identifier")

    app_icons = read_text("toothbrush/Images.xcassets/AppIcon.appiconset/Contents.json")
    for filename in ("Icon-83.5@2x.png", "Icon-AppStore-1024.png"):
        if f'"filename" : "{filename}"' not in app_icons:
            errors.append(f"app icon catalog is missing modern size: {filename}")

    tests = read_text("toothbrushTests/toothbrushTests.swift")
    for fragment in (
        "import UIKit",
        "@testable import toothbrush",
        "testHexColorParsesTrimmedHashValue",
        "testHexColorRejectsPartialInput",
        "testRemainingSecondsUsesDeadlineInsteadOfTickCount",
    ):
        if fragment not in tests:
            errors.append(f"XCTest coverage is missing: {fragment}")
    if "func testExample()" in tests or "func testPerformanceExample()" in tests:
        errors.append("placeholder XCTest methods must not replace behavior coverage")
    return errors


def timer_checks():
    errors = require_paths()
    if errors:
        return errors

    source = read_text("toothbrush/ViewController.swift")
    setup = re.search(r"func setupTimer\(\).*?@objc func subtractTime", source, re.S)
    setup_body = setup.group(0) if setup else ""
    subtract = re.search(r"@objc func subtractTime\(\).*?override func viewWillDisappear", source, re.S)
    subtract_body = subtract.group(0) if subtract else ""
    appear = re.search(r"override func viewWillAppear\(_ animated: Bool\).*?override func viewDidLayoutSubviews", source, re.S)
    appear_body = appear.group(0) if appear else ""
    layout = re.search(r"override func viewDidLayoutSubviews\(\).*?func setupTimer", source, re.S)
    layout_body = layout.group(0) if layout else ""
    disappear = re.search(r"override func viewWillDisappear\(_ animated: Bool\).*?func showNavigationLogo", source, re.S)
    disappear_body = disappear.group(0) if disappear else ""
    reset = re.search(r"func stopTimerAndResetPrompt\(\)\s*\{(?P<body>.*?)\n\s*\}", source, re.S)
    reset_body = reset.group("body") if reset else ""
    deinit = re.search(r"deinit\s*\{(?P<body>.*?)\n\s*\}", source, re.S)
    deinit_body = deinit.group("body") if deinit else ""
    if "timer?.invalidate()" not in setup_body:
        errors.append("setupTimer must invalidate any existing timer before scheduling")
    if "timerEndDate = Date().addingTimeInterval(TimeInterval(second))" not in setup_body:
        errors.append("setupTimer must establish a real-time countdown deadline")
    if "timer?.tolerance = 0.1" not in setup_body:
        errors.append("setupTimer must set a small tolerance on the repeating timer")
    if "RunLoop.main.add(timer, forMode: .common)" not in setup_body:
        errors.append("setupTimer must add the countdown timer to common run-loop modes")
    if "if second == 0" in source:
        errors.append("countdown completion must handle zero and negative values")
    if "if second <= 0" not in source:
        errors.append("countdown completion must use second <= 0")
    if "stopTimerAndResetPrompt()" not in subtract_body:
        errors.append("countdown completion must stop the timer through the shared reset path")
    if "second -= 1" in subtract_body:
        errors.append("countdown ticks must not assume every timer callback is exactly one second apart")
    if "second = remainingWholeSeconds(until: timerEndDate)" not in subtract_body:
        errors.append("countdown ticks must derive remaining time from the deadline")
    if "stopTimerAndResetPrompt()" not in disappear_body:
        errors.append("view disappearance must stop the timer through the shared reset path")
    if "showNavigationLogo()" not in appear_body:
        errors.append("view appearance must reattach the navigation logo")
    if "super.viewDidLayoutSubviews()" not in layout_body:
        errors.append("layout updates must call super.viewDidLayoutSubviews()")
    if "updateNavigationLogoFrame()" not in layout_body:
        errors.append("layout updates must recenter the navigation logo")
    if "removeNavigationLogo()" not in disappear_body:
        errors.append("view disappearance must remove the navigation logo")
    for fragment in (
        "timer?.invalidate()",
        "timer = nil",
        "timerEndDate = nil",
        "second = 0",
        "updateTimerLabel()",
        "brushText.layer.removeAllAnimations()",
        "brushText.alpha = 0",
        "brushBtn.isHidden = false",
        "brushText.isHidden = true",
    ):
        if fragment not in reset_body:
            errors.append(f"shared timer reset path is missing: {fragment}")
    if "timer?.invalidate()" not in deinit_body:
        errors.append("ViewController must invalidate its timer during deinit")
    if "removeNavigationLogo()" not in deinit_body:
        errors.append("ViewController must remove the navigation logo during deinit")
    for fragment in (
        "func showNavigationLogo()",
        "if let logoView = logoView",
        "func updateNavigationLogoFrame()",
        "logoView.frame.origin.x = (view.bounds.width - logoView.frame.width) / 2",
        "logoView.frame.origin.y = 20",
        "logoView.superview == nil",
        "addSubview(logoView)",
        "bringSubviewToFront(logoView)",
        "func removeNavigationLogo()",
        "logoView?.removeFromSuperview()",
    ):
        if fragment not in source:
            errors.append(f"navigation logo lifecycle is missing: {fragment}")
    if source.count("updateNavigationLogoFrame()") < 4:
        errors.append("navigation logo frame must be refreshed during setup, layout, and reattachment")
    for fragment in (
        "func remainingWholeSeconds(until endDate: Date, now: Date = Date()) -> Int",
        "max(0, Int(ceil(endDate.timeIntervalSince(now))))",
    ):
        if fragment not in source:
            errors.append(f"deadline countdown helper is missing: {fragment}")

    return errors


def color_checks():
    errors = require_paths()
    if errors:
        return errors

    source = read_text("toothbrush/Hex.swift")
    for fragment in (
        "hex.trimmingCharacters(in: .whitespacesAndNewlines).uppercased()",
        "cString.removeFirst()",
        "let scanner = Scanner(string: cString)",
        "scanner.scanHexInt64(&rgbValue)",
        "!scanner.isAtEnd",
    ):
        if fragment not in source:
            errors.append(f"modern hex parser is missing: {fragment}")

    return errors


def accessibility_checks():
    errors = require_paths()
    if errors:
        return errors

    source = read_text("toothbrush/ViewController.swift")
    for fragment in (
        "setupAccessibility()",
        'seconds.accessibilityLabel = "Brushing timer"',
        "seconds.accessibilityValue = seconds.text",
        'brushBtn.accessibilityLabel = "Start brushing timer"',
        'brushBtn.accessibilityHint = "Starts a two minute brushing countdown"',
        'brushText.accessibilityLabel = "Brushing reminder"',
        "func updateTimerLabel()",
        "seconds.accessibilityValue = labelText",
    ):
        if fragment not in source:
            errors.append(f"accessibility setup is missing: {fragment}")
    if source.count("updateTimerLabel()") < 3:
        errors.append("timer updates must keep visible text and accessibility value in sync")

    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("project", "timer", "color", "accessibility"), required=True)
    args = parser.parse_args()

    checks = {
        "project": project_checks,
        "timer": timer_checks,
        "color": color_checks,
        "accessibility": accessibility_checks,
    }
    errors = checks[args.mode]()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(f"{args.mode} checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
