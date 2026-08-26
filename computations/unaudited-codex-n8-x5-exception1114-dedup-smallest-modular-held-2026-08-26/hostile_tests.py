#!/usr/bin/env python3
"""In-memory hostile mutations for the held package validator."""

import copy
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("held_validator", HERE / "validate.py")
if spec is None or spec.loader is None:
    raise RuntimeError("cannot import validator")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)
base = validator.load_values()


def mutation(component, function):
    values = list(copy.deepcopy(base))
    replacement = function(values[component])
    if replacement is not None:
        values[component] = replacement
    return values


tests = {
    "held_status": mutation(0, lambda x: x.__setitem__("status", "READY")),
    "lane_count": mutation(0, lambda x: x["execution"].__setitem__("maximum_lane_count", 2)),
    "native_wall": mutation(0, lambda x: x["execution"].__setitem__("native_wall_seconds", 301)),
    "rss": mutation(0, lambda x: x["execution"].__setitem__("rss_cap_bytes", 9 * 1024**3)),
    "attempts": mutation(0, lambda x: x["scope"].__setitem__("attempts", 1)),
    "authorization": mutation(0, lambda x: x["authorization"].__setitem__("exact_Q_authorized", True)),
    "acceptance_source": mutation(1, lambda x: x.__setitem__("source_sha256", "0" * 64)),
    "clearance_relaunch": mutation(2, lambda x: x.__setitem__("automatic_relaunch_authorized", True)),
    "clearance_overlap": mutation(2, lambda x: x.__setitem__("expected_census_match_count", 1)),
    "q_dependency": mutation(3, lambda x: x["required_future_dependencies"].__setitem__("modular_terminal_manifest_sha256", "f" * 64)),
    "q_authorization": mutation(3, lambda x: x["authorization"].__setitem__("exact_Q_authorized", True)),
    "refusal_missing": mutation(4, lambda x: x.__setitem__("missing_by_design", [])),
    "source_prime": mutation(5, lambda x: x.replace(b"ring r=32003,(", b"ring r=32009,(", 1)),
    "source_epilogue": mutation(5, lambda x: x.replace(b"ideal G=slimgb(I);", b"ideal G=I;", 1)),
    "derivation_run": mutation(6, lambda x: x["scope"].__setitem__("solver_runs", 1)),
    "runner_resource": mutation(7, lambda x: x.replace(b"NATIVE = 300", b"NATIVE = 301", 1)),
}
rejected = []
for name, values in tests.items():
    try:
        validator.validate_values(*values)
    except Exception:
        rejected.append(name)
if len(rejected) != len(tests):
    raise RuntimeError(("hostile accepted", sorted(set(tests) - set(rejected))))
result = {"schema": "KRENN_X5_EXCEPTION1114_DEDUP_MODULAR_HOSTILES_V1", "status": "PASS_ALL_REJECTED", "count": len(tests), "rejected": sorted(rejected), "solver_runs": 0}
(HERE / "results_hostiles.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, sort_keys=True))
