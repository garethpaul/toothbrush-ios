#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS_PLANS = ROOT / "docs" / "plans"
CANONICAL_PLAN = DOCS_PLANS / "2026-06-08-toothbrush-ios-baseline.md"


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
    if "timer.invalidate()" not in setup_body:
        errors.append("setupTimer must invalidate any existing timer before scheduling")
    if 'if(second == 0)' in source:
        errors.append("countdown completion must handle zero and negative values")
    if "if(second <= 0)" not in source:
        errors.append("countdown completion must use second <= 0")
    if "brushText.layer.removeAllAnimations()" not in source:
        errors.append("countdown completion must stop the repeating brush-text animation")
    if "deinit" not in source or "timer.invalidate()" not in source.split("deinit", 1)[-1]:
        errors.append("ViewController must invalidate its timer during deinit")

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
