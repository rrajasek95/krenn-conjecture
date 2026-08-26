#!/usr/bin/env python3
"""Materialize the independently approved rep5 guard-pivot k0 modular pilot."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DESIGN = ROOT / "computations/unaudited-codex-n8-x5-rep5-post-timeout-guard-pivot-quotient-design-2026-08-25"
REFEREE = ROOT / "computations/unaudited-codex-n8-x5-rep5-post-timeout-guard-pivot-quotient-design-referee-2026-08-25"
TEMPLATE = ROOT / "computations/unaudited-codex-n8-x5-rep5-all-equal-y-modular-held-v2-2026-08-25"
Q_SOURCE = DESIGN / "rep5_p00_guardpivot_k0_Q.sing"
SOURCE = HERE / "rep5_p00_guardpivot_k0_p32003.sing"
RUNNER = HERE / "run_one_lane.py"
PINS = {
    DESIGN / "MANIFEST.sha256": "00ac8c2a1bea2b958644b0e6b1851d26535c83cc715d92b28335157b219da3f9",
    Q_SOURCE: "d4204428cab5f3b5dd4ac321dd1ae04ce9b79c8f1197b8e1e863c6c186cc74f1",
    REFEREE / "FINAL_MANIFEST.sha256": "af4bee0ca8db5391aac9f59cb1e52051d32e66fdb2974a126468b054ca3f5a4b",
    REFEREE / "HELD_DIAGNOSTIC_PLAN.json": "acf0923735e96633389f8df6a74a0a35c3700fd9fd77ee28e1deffd1d8bac796",
    TEMPLATE / "run_one_lane.py": "9eaef175601f51dcd7a50321fc80d02dc71ec81b91a8f13f02116d3b76cdadb9",
    Path("/usr/local/bin/Singular"): "9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88",
    Path("/usr/local/bin/gtimeout"): "1e26c50fa8c439fe1f4e6c6edd106e95030e16582c1c8c32e73d8a889cdf5b95",
}
SOURCE_SHA = "dc04c72252144d1a8ff798f49aa1130b1742fff342f21eaf02146b889e3370c1"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


for path, expected in PINS.items():
    assert sha256(path) == expected, (path, sha256(path), expected)

raw = Q_SOURCE.read_bytes()
assert raw.count(b"ring r=0,") == 1
assert raw.count(b"ideal G=slimgb(I);") == 1
assert raw.count(b"poly remainder=reduce(1,G);") == 1
modular = raw.replace(b"ring r=0,", b"ring r=32003,")
assert sha256(Q_SOURCE) == PINS[Q_SOURCE]
assert hashlib.sha256(modular).hexdigest() == SOURCE_SHA
SOURCE.write_bytes(modular)

runner = (TEMPLATE / "run_one_lane.py").read_text()
runner = runner.replace(
    '"""Single-use, refusal-by-default rep5 runner with internal wrapper enforcement."""',
    '"""Single-use fail-closed runner for the rep5 guard-pivot k0 modular pilot."""',
)
runner = runner.replace(
    'SOURCE = HERE / "rep5_all_equal_y_i0_p00_x0_y0_d01_p32003.sing"',
    'SOURCE = HERE / "rep5_p00_guardpivot_k0_p32003.sing"',
)
old_constants_start = runner.index('DESIGN = ROOT / "computations/unaudited-codex-n8-x5-rep5-guard-minor-contraction-design-2026-08-25"')
old_constants_end = runner.index("NATIVE_WALL = 180")
new_constants = '''DESIGN = ROOT / "computations/unaudited-codex-n8-x5-rep5-post-timeout-guard-pivot-quotient-design-2026-08-25"
REFEREE = ROOT / "computations/unaudited-codex-n8-x5-rep5-post-timeout-guard-pivot-quotient-design-referee-2026-08-25"
TEMPLATE = ROOT / "computations/unaudited-codex-n8-x5-rep5-all-equal-y-modular-held-v2-2026-08-25"
PINS = {
    DESIGN / "MANIFEST.sha256": "00ac8c2a1bea2b958644b0e6b1851d26535c83cc715d92b28335157b219da3f9",
    DESIGN / "rep5_p00_guardpivot_k0_Q.sing": "d4204428cab5f3b5dd4ac321dd1ae04ce9b79c8f1197b8e1e863c6c186cc74f1",
    REFEREE / "FINAL_MANIFEST.sha256": "af4bee0ca8db5391aac9f59cb1e52051d32e66fdb2974a126468b054ca3f5a4b",
    REFEREE / "HELD_DIAGNOSTIC_PLAN.json": "acf0923735e96633389f8df6a74a0a35c3700fd9fd77ee28e1deffd1d8bac796",
    TEMPLATE / "run_one_lane.py": "9eaef175601f51dcd7a50321fc80d02dc71ec81b91a8f13f02116d3b76cdadb9",
    SINGULAR: "9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88",
    GTIMEOUT: "1e26c50fa8c439fe1f4e6c6edd106e95030e16582c1c8c32e73d8a889cdf5b95",
}
'''
runner = runner[:old_constants_start] + new_constants + runner[old_constants_end:]
runner = runner.replace("NATIVE_WALL = 180", "NATIVE_WALL = 240")
runner = runner.replace("WRAPPER_WALL = 195", "WRAPPER_WALL = 250")
runner = runner.replace(
    'SOURCE_SHA = "33716adb0c1e2e9064e8c68e8cd60df305fe88781153c195853dba8131838c97"',
    f'SOURCE_SHA = "{SOURCE_SHA}"',
)
old_acceptance_start = runner.index("    assert acceptance == {")
old_acceptance_end = runner.index("    clearance = json.loads", old_acceptance_start)
new_acceptance = '''    assert acceptance == {
        "schema": "KRENN_X5_REP5_GUARD_PIVOT_K0_INDEPENDENT_ACCEPTANCE_V1",
        "status": "PASS_APPROVE_ONE_GUARD_PIVOT_K0_MODULAR_DIAGNOSTIC_ONLY",
        "held_manifest_sha256": manifest_sha,
        "source_sha256": source_sha,
        "runner_sha256": runner_sha,
        "design_manifest_sha256": PINS[DESIGN / "MANIFEST.sha256"],
        "source_Q_sha256": PINS[DESIGN / "rep5_p00_guardpivot_k0_Q.sing"],
        "design_referee_manifest_sha256": PINS[REFEREE / "FINAL_MANIFEST.sha256"],
        "held_plan_sha256": PINS[REFEREE / "HELD_DIAGNOSTIC_PLAN.json"],
        "singular_sha256": PINS[SINGULAR],
        "gtimeout_sha256": PINS[GTIMEOUT],
        "field": 32003, "pivot_k": 0, "variables": 88, "generators": 6574,
        "maximum_lane_count": 1, "exact_Q_authorized": False,
        "other_k_authorized": False, "automatic_relaunch_authorized": False,
    }
'''
runner = runner[:old_acceptance_start] + new_acceptance + runner[old_acceptance_end:]
runner = runner.replace(
    '"exact_Q_authorized",\n        "second_lane_authorized", "automatic_relaunch_authorized",',
    '"exact_Q_authorized",\n        "other_k_authorized", "automatic_relaunch_authorized",',
)
runner = runner.replace(
    '"KRENN_X5_REP5_ALL_EQUAL_Y_V2_EXPLICIT_LAUNCH_CLEARANCE_V1"',
    '"KRENN_X5_REP5_GUARD_PIVOT_K0_EXPLICIT_LAUNCH_CLEARANCE_V1"',
)
runner = runner.replace(
    '"CLEARED_ONE_HARDENED_MODULAR_DIAGNOSTIC_ONLY"',
    '"CLEARED_ONE_GUARD_PIVOT_K0_MODULAR_DIAGNOSTIC_ONLY"',
)
runner = runner.replace(
    'assert clearance["exact_Q_authorized"] is False and clearance["second_lane_authorized"] is False',
    'assert clearance["exact_Q_authorized"] is False and clearance["other_k_authorized"] is False',
)
runner = runner.replace("KRENN_X5_REP5_ALL_EQUAL_Y_V2", "KRENN_X5_REP5_GUARD_PIVOT_K0")
runner = runner.replace('"variables": 91, "generators": 6577', '"variables": 88, "generators": 6574')
runner = runner.replace('"NATIVE_WALL_CAP_180"', '"NATIVE_WALL_CAP_240"')
runner = runner.replace('"second_lane_launched": False', '"other_k_launched": False')
runner = runner.replace('"rep2_equivalence_used": False,', '"pivot_k": 0,')
runner = runner.replace('"second_lane_authorized"', '"other_k_authorized"')
assert "ALL_EQUAL_Y" not in runner
assert "SOURCE_REFEREE" not in runner and "REJECTION" not in runner and "PRIOR_HELD" not in runner
assert "second_lane" not in runner and "180" not in runner and "195" not in runner
compile(runner, str(RUNNER), "exec")
RUNNER.write_text(runner)

result = {
    "schema": "KRENN_X5_REP5_GUARD_PIVOT_K0_HELD_PACKAGE_BUILD_V1",
    "status": "PASS_MATERIALIZED_ZERO_RUN",
    "source_Q_sha256": sha256(Q_SOURCE),
    "source_modular_sha256": sha256(SOURCE),
    "runner_sha256": sha256(RUNNER),
    "field": 32003,
    "pivot_k": 0,
    "variables": 88,
    "generators": 6574,
    "solver_runs": 0,
}
(HERE / "build_result.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, sort_keys=True))
