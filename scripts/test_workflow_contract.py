#!/usr/bin/env python3
import importlib.util
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "scripts" / "check-toothbrush-source.py"
EXPECTED_ERROR = "GitHub Actions workflow must match the reviewed Toothbrush validation contract"


def load_checker():
    spec = importlib.util.spec_from_file_location("toothbrush_source_checker", CHECKER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load Toothbrush source checker")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def replace_once(source, old, new):
    if old not in source:
        raise AssertionError(f"workflow fixture did not contain {old!r}")
    return source.replace(old, new, 1)


def main():
    checker = load_checker()
    workflow = checker.CI_WORKFLOW.read_text(encoding="utf-8")
    if workflow != checker.EXPECTED_WORKFLOW:
        raise AssertionError("checked-in workflow does not match the source checker contract")
    mutations = (
        ("permissions", "contents: read", "contents: write"),
        ("credential persistence", "persist-credentials: false", "persist-credentials: true"),
        ("checkout pin", "actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10", "actions/checkout@main"),
        ("Python action pin", "actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405", "actions/setup-python@v6"),
        ("Ubuntu runner", "runs-on: ubuntu-24.04", "runs-on: ubuntu-latest"),
        ("macOS runner", "runs-on: macos-15", "runs-on: macos-latest"),
        ("static timeout", "timeout-minutes: 5", "timeout-minutes: 30"),
        ("Xcode timeout", "timeout-minutes: 15", "timeout-minutes: 30"),
        ("concurrency cancellation", "cancel-in-progress: true", "cancel-in-progress: false"),
        ("Python version", 'python-version: "3.12"', 'python-version: "3.11"'),
        ("Xcode version", "Xcode_16.4.app", "Xcode_16.3.app"),
        ("static unqualified Make", "run: /usr/bin/make check", "run: make check"),
        ("XCTest unqualified Make", "run: /usr/bin/make test", "run: make test"),
        ("pull request target", "  pull_request:\n", "  pull_request_target:\n"),
        ("secret environment", "    timeout-minutes: 5\n", "    timeout-minutes: 5\n    env:\n      TOKEN: ${{ secrets.TOKEN }}\n"),
        ("checkout token", "          persist-credentials: false\n", "          persist-credentials: false\n          token: ${{ github.token }}\n"),
        ("XCTest shell wrapper", "run: /usr/bin/make test", "run: /bin/sh -c '/usr/bin/make test'"),
    )
    original = checker.CI_WORKFLOW
    with tempfile.TemporaryDirectory(prefix="toothbrush-workflow-contract-") as temp_dir:
        for name, old, new in mutations:
            path = Path(temp_dir) / "check.yml"
            path.write_text(replace_once(workflow, old, new), encoding="utf-8")
            checker.CI_WORKFLOW = path
            errors = checker.project_checks()
            if EXPECTED_ERROR not in errors:
                raise AssertionError(f"workflow mutation was not rejected: {name}")
    checker.CI_WORKFLOW = original
    print(f"workflow contract passed ({len(mutations)} mutations rejected)")


if __name__ == "__main__":
    main()
