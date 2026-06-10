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
CI_WORKFLOW = ROOT / ".github/workflows/check.yml"


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
        "timeout-minutes: 5",
        "actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10",
        "actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405",
        'python-version: "3.12"',
        "run: make check",
    ):
        if fragment not in workflow:
            errors.append(f"GitHub Actions workflow is missing expected setting: {fragment}")

    docs = "\n".join(read_text(path) for path in ("README.md", "VISION.md", "SECURITY.md", "CHANGES.md"))
    if "GitHub Actions" not in docs:
        errors.append("project docs must mention the GitHub Actions static baseline")

    project = read_text("toothbrush.xcodeproj/project.pbxproj")
    for fragment in (
        "toothbrushTests",
        "IPHONEOS_DEPLOYMENT_TARGET = 8.3;",
    ):
        if fragment not in project:
            errors.append(f"project is missing expected setting: {fragment}")
    return errors


def timer_checks():
    errors = require_paths()
    if errors:
        return errors

    source = read_text("toothbrush/ViewController.swift")
    setup = re.search(r"func setupTimer\(\).*?func subtractTime", source, re.S)
    setup_body = setup.group(0) if setup else ""
    subtract = re.search(r"func subtractTime\(\).*?override func viewWillDisappear", source, re.S)
    subtract_body = subtract.group(0) if subtract else ""
    appear = re.search(r"override func viewWillAppear\(animated: Bool\).*?override func didReceiveMemoryWarning", source, re.S)
    appear_body = appear.group(0) if appear else ""
    layout = re.search(r"override func viewDidLayoutSubviews\(\).*?override func didReceiveMemoryWarning", source, re.S)
    layout_body = layout.group(0) if layout else ""
    disappear = re.search(r"override func viewWillDisappear\(animated: Bool\).*?func setupAccessibility", source, re.S)
    disappear_body = disappear.group(0) if disappear else ""
    reset = re.search(r"func stopTimerAndResetPrompt\(\)\s*\{(?P<body>.*?)\n\s*\}", source, re.S)
    reset_body = reset.group("body") if reset else ""
    deinit = re.search(r"deinit\s*\{(?P<body>.*?)\n\s*\}", source, re.S)
    deinit_body = deinit.group("body") if deinit else ""
    if "timer.invalidate()" not in setup_body:
        errors.append("setupTimer must invalidate any existing timer before scheduling")
    if "timer.tolerance = 0.1" not in setup_body:
        errors.append("setupTimer must set a small tolerance on the repeating timer")
    if "NSRunLoop.mainRunLoop().addTimer(timer, forMode: NSRunLoopCommonModes)" not in setup_body:
        errors.append("setupTimer must add the countdown timer to common run-loop modes")
    if 'if(second == 0)' in source:
        errors.append("countdown completion must handle zero and negative values")
    if "if(second <= 0)" not in source:
        errors.append("countdown completion must use second <= 0")
    if "stopTimerAndResetPrompt()" not in subtract_body:
        errors.append("countdown completion must stop the timer through the shared reset path")
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
        "timer.invalidate()",
        "second = 0",
        "updateTimerLabel()",
        "brushText.layer.removeAllAnimations()",
        "brushText.alpha = 0",
        "brushBtn.hidden = false",
        "brushText.hidden = true",
    ):
        if fragment not in reset_body:
            errors.append(f"shared timer reset path is missing: {fragment}")
    if "timer.invalidate()" not in deinit_body:
        errors.append("ViewController must invalidate its timer during deinit")
    if "removeNavigationLogo()" not in deinit_body:
        errors.append("ViewController must remove the navigation logo during deinit")
    for fragment in (
        "func showNavigationLogo()",
        "if let logoView = logoView",
        "func updateNavigationLogoFrame()",
        "logoView.frame.origin.x = (self.view.frame.size.width - logoView.frame.size.width) / 2",
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

    return errors


def color_checks():
    errors = require_paths()
    if errors:
        return errors

    source = read_text("toothbrush/Hex.swift")
    if "NSScanner(string: cString).scanHexInt(&rgbValue)" in source:
        errors.append("hex parser must not ignore the scanHexInt return value")
    if "let scanner = NSScanner(string: cString)" not in source:
        errors.append("hex parser must keep an NSScanner reference for validation")
    if "scanner.scanHexInt(&rgbValue)" not in source:
        errors.append("hex parser must scan the hex value through the validator")
    if "scanner.scanLocation != cString.characters.count" not in source:
        errors.append("hex parser must reject partially parsed hex strings")

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
