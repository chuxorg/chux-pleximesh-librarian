#!/usr/bin/env python3
"""Read-path smoke tests for Librarian API (LIB-005)."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple
from urllib import error, request

DEFAULT_BASE_URL = os.environ.get("LIBRARIAN_BASE_URL", "http://localhost:8000")


@dataclass
class TestResult:
    name: str
    passed: bool
    details: str


def now_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fetch_json(url: str, timeout: float) -> Tuple[int, str, Optional[Dict[str, Any]]]:
    try:
        with request.urlopen(url, timeout=timeout) as response:
            body = response.read().decode("utf-8")
            return response.getcode(), body, json.loads(body)
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8")
        payload = None
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            payload = None
        return exc.code, body, payload


def assert_equal(actual: Any, expected: Any, message: str) -> Optional[str]:
    if actual != expected:
        return f"{message}: expected {expected!r}, got {actual!r}"
    return None


def assert_error(payload: Optional[Dict[str, Any]], expected: str) -> Optional[str]:
    if not isinstance(payload, dict):
        return "error response is not JSON"
    error_value = payload.get("error")
    if error_value != expected:
        return f"error message mismatch: expected {expected!r}, got {error_value!r}"
    return None


def check_sorted(artifacts: List[Dict[str, Any]]) -> Optional[str]:
    def version_key(value: str) -> int:
        if not value.startswith("v"):
            return -1
        try:
            return int(value[1:])
        except ValueError:
            return -1

    keys = [(item.get("artifact_id"), version_key(item.get("version", ""))) for item in artifacts]
    if keys != sorted(keys):
        return f"artifacts not ordered deterministically: {keys}"
    return None


def run_tests(base_url: str, timeout: float, wait_seconds: float) -> List[TestResult]:
    if wait_seconds:
        time.sleep(wait_seconds)

    results: List[TestResult] = []

    def record(name: str, passed: bool, details: str) -> None:
        results.append(TestResult(name=name, passed=passed, details=details))

    status, _, payload = fetch_json(f"{base_url}/artifacts/LIB-003", timeout)
    if status != 200:
        record("latest artifact", False, f"expected 200, got {status}")
    else:
        errors = [
            assert_equal(payload.get("artifact_id"), "LIB-003", "artifact_id"),
            assert_equal(payload.get("kind"), "task", "kind"),
            assert_equal(payload.get("domain"), "librarian", "domain"),
            assert_equal(payload.get("version"), "v0", "version"),
        ]
        error = next((err for err in errors if err), None)
        record("latest artifact", error is None, error or "ok")

    status, _, payload = fetch_json(f"{base_url}/artifacts/LIB-003?version=v0", timeout)
    if status != 200:
        record("versioned artifact", False, f"expected 200, got {status}")
    else:
        error = assert_equal(payload.get("artifact_id"), "LIB-003", "artifact_id")
        record("versioned artifact", error is None, error or "ok")

    status, _, payload = fetch_json(f"{base_url}/tasks/LIB-003", timeout)
    if status != 200:
        record("task alias", False, f"expected 200, got {status}")
    else:
        errors = [
            assert_equal(payload.get("kind"), "task", "kind"),
            assert_equal(payload.get("domain"), "librarian", "domain"),
        ]
        error = next((err for err in errors if err), None)
        record("task alias", error is None, error or "ok")

    status, _, payload = fetch_json(f"{base_url}/policies/pr-policy", timeout)
    if status != 200:
        record("policy alias", False, f"expected 200, got {status}")
    else:
        error = assert_equal(payload.get("kind"), "policy", "kind")
        record("policy alias", error is None, error or "ok")

    status, _, payload = fetch_json(f"{base_url}/phases/PHASE-LIBRARY-HARDENING", timeout)
    if status != 200:
        record("phase alias", False, f"expected 200, got {status}")
    else:
        error = assert_equal(payload.get("kind"), "phase", "kind")
        record("phase alias", error is None, error or "ok")

    status, _, payload = fetch_json(
        f"{base_url}/artifacts?kind=task&domain=librarian&status=active", timeout
    )
    if status != 200:
        record("list artifacts", False, f"expected 200, got {status}")
    else:
        artifacts = payload.get("artifacts") if isinstance(payload, dict) else None
        if not isinstance(artifacts, list):
            record("list artifacts", False, "missing artifacts list")
        else:
            ordering_error = check_sorted(artifacts)
            record("list artifacts", ordering_error is None, ordering_error or "ok")

    status, _, payload = fetch_json(f"{base_url}/artifacts/LIB-003?version=bad", timeout)
    if status != 400:
        record("invalid version", False, f"expected 400, got {status}")
    else:
        error = assert_error(payload, "version must match vN")
        record("invalid version", error is None, error or "ok")

    status, _, payload = fetch_json(f"{base_url}/health", timeout)
    if status != 404:
        record("unknown path", False, f"expected 404, got {status}")
    else:
        error = assert_error(payload, "Unknown path")
        record("unknown path", error is None, error or "ok")

    status, _, payload = fetch_json(f"{base_url}/artifacts?kind=unknown", timeout)
    if status != 400:
        record("invalid filter", False, f"expected 400, got {status}")
    else:
        error = assert_error(payload, "Invalid kind filter")
        record("invalid filter", error is None, error or "ok")

    status, _, payload = fetch_json(f"{base_url}/artifacts/NO-SUCH-ARTIFACT", timeout)
    if status != 404:
        record("not found", False, f"expected 404, got {status}")
    else:
        error = assert_error(payload, "Artifact not found")
        record("not found", error is None, error or "ok")

    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="LIB-005 Librarian read-path smoke tests")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="Base URL for the API")
    parser.add_argument("--timeout", type=float, default=5.0, help="HTTP timeout seconds")
    parser.add_argument("--wait", type=float, default=0.0, help="Optional startup delay")
    parser.add_argument("--output", help="Write JSON report to this path")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    results = run_tests(args.base_url, args.timeout, args.wait)
    passed = all(result.passed for result in results)

    report = {
        "report": {
            "name": "lib-005-smoke-tests",
            "version": "v0",
            "generated_at": now_timestamp(),
            "base_url": args.base_url,
            "passed": passed,
        },
        "results": [
            {
                "name": result.name,
                "passed": result.passed,
                "details": result.details,
            }
            for result in results
        ],
    }

    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(json.dumps(report, ensure_ascii=True, indent=2) + "\n")

    summary = "PASS" if passed else "FAIL"
    print(f"Smoke tests: {summary}")
    for result in results:
        status = "PASS" if result.passed else "FAIL"
        print(f"- {result.name}: {status} ({result.details})")

    if not passed:
        sys.exit(1)


if __name__ == "__main__":
    main()
