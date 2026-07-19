#!/usr/bin/env python3
"""Vendor-neutral validator for model-routing observability v0.1.

Validates that metric and event contracts are vendor-neutral and receipt-driven,
alert semantics distinguish informational/warning/blocking/incident, no private
content is required, cost and quality remain joined, promotion expiry and
benchmark staleness are first-class signals, and silent paid fallback is
detectable.

Stdlib-only. No third-party dependencies.

Usage:
    python validate.py            # validate all fixtures in valid/ and invalid/
    python validate.py <path>     # validate a single file, print errors
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

SCHEMA_DIR = Path(__file__).parent.parent.parent / "schemas"
OBS_SCHEMA_PATH = SCHEMA_DIR / "model-routing-observability-v0.1.json"
DASHBOARD_SCHEMA_PATH = SCHEMA_DIR / "model-routing-dashboard-v0.1.json"
VALID_DIR = Path(__file__).parent / "valid"
INVALID_DIR = Path(__file__).parent / "invalid"

_PRIVATE_MARKERS = ("prompt_content", "output_content", "user_message", "raw_prompt", "raw_output")
_VENDOR_API_MARKERS = ("datadog", "newrelic", "grafana_api", "splunk_api", "honeycomb_api", "dynatrace_api")
_REQUIRED_ALERT_NAMES = {
    "budget-ceiling-breach",
    "premium-model-outside-scope",
    "promoted-route-evidence-expired",
    "failure-rate-exceeds-threshold",
    "provider-concentration-breach",
    "route-decision-missing-metadata",
    "observed-model-differs-from-selected",
    "cost-arithmetic-reconciliation-failure",
    "silent-paid-fallback",
    "high-consequence-no-review",
}
_REQUIRED_METRIC_ECONOMICS = {
    "spend-by-provider-model-runtime",
    "cost-per-accepted-governed-outcome",
    "rejected-failed-attempt-cost",
    "reviewer-human-correction-burden",
    "batch-cache-local-utilization",
    "premium-route-frequency",
}
_REQUIRED_METRIC_GOVERNANCE = {
    "privacy-authority-gate-failures",
    "missing-independent-review",
    "stale-benchmark-evidence",
    "route-promotion-expiry",
    "alias-version-drift",
    "provider-concentration",
    "routing-policy-version-drift",
    "unexpected-production-default-changes",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Minimal stdlib JSON Schema validator (subset of Draft 2020-12)
# ---------------------------------------------------------------------------

_TYPE_MAP = {
    "string": (str,),
    "number": (int, float),
    "integer": (int,),
    "boolean": (bool,),
    "array": (list,),
    "object": (dict,),
    "null": (type(None),),
}


def _check_type(instance: Any, type_name: str | list[str]) -> str | None:
    if isinstance(type_name, list):
        expected = tuple(t for name in type_name for t in _TYPE_MAP.get(name, ()))
    else:
        expected = _TYPE_MAP.get(type_name, ())
    if expected and not isinstance(instance, expected):
        return f"expected type {type_name!r}, got {type(instance).__name__}"
    return None


def _validate_schema(instance: Any, schema: dict[str, Any], path: str = "") -> list[str]:
    if not isinstance(schema, dict):
        return [f"{path}: schema must be an object"]

    if "const" in schema and instance != schema["const"]:
        return [f"{path}: expected const {schema['const']!r}, got {instance!r}"]

    if "type" in schema:
        type_err = _check_type(instance, schema["type"])
        if type_err:
            return [f"{path}: {type_err}"]

    errors: list[str] = []

    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: {instance!r} not in enum {schema['enum']}")

    if isinstance(instance, str):
        if "minLength" in schema and len(instance) < schema["minLength"]:
            errors.append(f"{path}: string length {len(instance)} < minLength {schema['minLength']}")
        if "maxLength" in schema and len(instance) > schema["maxLength"]:
            errors.append(f"{path}: string length {len(instance)} > maxLength {schema['maxLength']}")
        if "pattern" in schema:
            try:
                if not re.search(schema["pattern"], instance):
                    errors.append(f"{path}: {instance!r} does not match pattern {schema['pattern']!r}")
            except re.error as exc:
                errors.append(f"{path}: invalid regex pattern: {exc}")

    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            errors.append(f"{path}: {instance} < minimum {schema['minimum']}")
        if "maximum" in schema and instance > schema["maximum"]:
            errors.append(f"{path}: {instance} > maximum {schema['maximum']}")

    if isinstance(instance, dict):
        for req in schema.get("required", []):
            if req not in instance:
                errors.append(f"{path}: missing required property {req!r}")
        props = schema.get("properties", {})
        for key, prop_schema in props.items():
            if key in instance:
                sub = f"{path}.{key}" if path else key
                errors.extend(_validate_schema(instance[key], prop_schema, sub))
        if "additionalProperties" in schema:
            ap = schema["additionalProperties"]
            for key in instance:
                if key not in props:
                    if ap is False:
                        errors.append(f"{path}: unexpected property {key!r}")
                    elif isinstance(ap, dict):
                        sub = f"{path}.{key}" if path else key
                        errors.extend(_validate_schema(instance[key], ap, sub))

    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            errors.append(f"{path}: array length {len(instance)} < minItems {schema['minItems']}")
        if "maxItems" in schema and len(instance) > schema["maxItems"]:
            errors.append(f"{path}: array length {len(instance)} > maxItems {schema['maxItems']}")
        if "items" in schema:
            for i, item in enumerate(instance):
                errors.extend(_validate_schema(item, schema["items"], f"{path}[{i}]"))

    return errors


# ---------------------------------------------------------------------------
# Semantic validation
# ---------------------------------------------------------------------------

def validate_semantic(data: dict[str, Any]) -> list[str]:
    """Run vendor-neutral semantic checks. Returns list of error messages."""
    errors: list[str] = []

    # Check 1: All metrics must be receipt-driven (vendor-neutral).
    metrics = data.get("metrics", {})
    for category in ("economics", "qualityReliability", "governanceLifecycle"):
        for metric in metrics.get(category, []):
            if not metric.get("receiptDriven", False):
                errors.append(
                    f"metrics.{category}.{metric.get('name', '?')}: must be receiptDriven (vendor-neutral)"
                )

    # Check 2: All alerts must be receipt-driven.
    for alert in data.get("alerts", []):
        if not alert.get("receiptDriven", False):
            errors.append(
                f"alerts.{alert.get('name', '?')}: must be receiptDriven (vendor-neutral)"
            )

    # Check 3: No private content markers in the document.
    doc_text = json.dumps(data).lower()
    for marker in _PRIVATE_MARKERS:
        if marker in doc_text:
            errors.append(f"document contains private content marker: {marker!r}")
            break

    # Check 4: No vendor-specific API markers.
    for marker in _VENDOR_API_MARKERS:
        if marker in doc_text:
            errors.append(f"document contains vendor-specific API marker: {marker!r}")
            break

    # Check 5: Alert severities must distinguish informational/warning/blocking/incident.
    severities = {alert.get("severity") for alert in data.get("alerts", [])}
    required_severities = {"informational", "warning", "blocking", "incident"}
    if not severities.intersection(required_severities):
        errors.append("alerts must include at least one of: informational, warning, blocking, incident")

    # Check 6: Required alert names must be present.
    alert_names = {alert.get("name") for alert in data.get("alerts", [])}
    missing_alerts = _REQUIRED_ALERT_NAMES - alert_names
    if missing_alerts:
        errors.append(f"missing required alert contracts: {sorted(missing_alerts)}")

    # Check 7: Required economics metrics must be present.
    econ_metrics = {m.get("name") for m in metrics.get("economics", [])}
    missing_econ = _REQUIRED_METRIC_ECONOMICS - econ_metrics
    if missing_econ:
        errors.append(f"missing required economics metrics: {sorted(missing_econ)}")

    # Check 8: Required governance metrics must be present.
    gov_metrics = {m.get("name") for m in metrics.get("governanceLifecycle", [])}
    missing_gov = _REQUIRED_METRIC_GOVERNANCE - gov_metrics
    if missing_gov:
        errors.append(f"missing required governance metrics: {sorted(missing_gov)}")

    # Check 9: Promotion expiry and benchmark staleness must be first-class signals.
    gov_names = {m.get("name") for m in metrics.get("governanceLifecycle", [])}
    if "route-promotion-expiry" not in gov_names:
        errors.append("route-promotion-expiry must be a first-class governance metric")
    if "stale-benchmark-evidence" not in gov_names:
        errors.append("stale-benchmark-evidence must be a first-class governance metric")

    # Check 10: Silent paid fallback must be detectable.
    if "silent-paid-fallback" not in alert_names:
        errors.append("silent-paid-fallback alert must be present (silent paid fallback must be detectable)")

    # Check 11: Cost and quality must remain joined (at least one quality metric required).
    quality_metrics = metrics.get("qualityReliability", [])
    if not quality_metrics:
        errors.append("qualityReliability metrics must be present (cost and quality must remain joined)")

    # Check 12: Dimensions must declare no private content where required.
    dims = data.get("dimensions", {})
    for dim_name in ("taskClass", "productConsumer"):
        dim = dims.get(dim_name, {})
        if dim.get("noPrivateContent") is not True:
            errors.append(f"dimensions.{dim_name}: noPrivateContent must be true")

    return errors


def validate(data: dict[str, Any], schema: dict[str, Any] | None = None) -> list[str]:
    """Full validation: schema + semantic."""
    if schema is None:
        schema = load_json(OBS_SCHEMA_PATH)
    data = {k: v for k, v in data.items() if not k.startswith("_")}
    errors = _validate_schema(data, schema)
    if errors:
        return errors
    return validate_semantic(data)


def validate_file(path: Path) -> list[str]:
    data = load_json(path)
    schema = load_json(OBS_SCHEMA_PATH)
    return validate(data, schema)


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]

    if args:
        path = Path(args[0])
        errors = validate_file(path)
        if errors:
            print(f"INVALID: {path.name}")
            for e in errors:
                print(f"  - {e}")
            return 1
        print(f"VALID: {path.name}")
        return 0

    failures = 0
    total = 0

    for path in sorted(VALID_DIR.glob("*.json")):
        total += 1
        errors = validate_file(path)
        if errors:
            print(f"FAIL (valid): {path.name}")
            for e in errors:
                print(f"  - {e}")
            failures += 1
        else:
            print(f"PASS (valid): {path.name}")

    for path in sorted(INVALID_DIR.glob("*.json")):
        total += 1
        errors = validate_file(path)
        if errors:
            print(f"PASS (invalid): {path.name}")
        else:
            print(f"FAIL (invalid): {path.name} - no errors found")
            failures += 1

    print(f"\n{total - failures}/{total} fixtures passed validation")
    return 1 if failures > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
