#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


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


def project_checks():
    errors = require_paths()
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("project", "timer"), required=True)
    args = parser.parse_args()

    errors = project_checks() if args.mode == "project" else timer_checks()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(f"{args.mode} checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
