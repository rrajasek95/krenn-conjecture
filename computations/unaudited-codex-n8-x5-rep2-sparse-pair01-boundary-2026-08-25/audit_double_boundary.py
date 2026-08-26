#!/usr/bin/env python3
"""Independent exact audit of the base/single/double sparse pair01 boundary."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import os
import subprocess
import tempfile
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PINS = {
    ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep2-tensor-flattening-2026-08-25/MANIFEST.sha256":
        "16d459603ae0107e0da21ded47b67de62dd289c128667b67bad83bdd36deae1b",
    ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep2-tensor-flattening-2026-08-25/results_tensor_core_audit.json":
        "b164264e31b6b3c9341409db79df81cabb3b843db7aae7cf6615715656a16a00",
    ROOT / "computations/unaudited-codex-n8-x5-seven-block-rank1-incidence-gate-2026-08-25/generate_rank1_gate.py":
        "1fc2a1a62e4092f75cbb330009bbb9649e83e559167f251217a26b7eb3bc7c14",
    Path("/usr/local/bin/Singular"):
        "9436b32ff7565719240230de8a6fb1d27af5e65f0ca4c9c5b756a77e82409b88",
}


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(text):
    return hashlib.sha256(text.encode()).hexdigest()


def load(name):
    path = HERE / name
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def singular_status(path):
    process = subprocess.run(
        ["gtimeout", "2", "Singular", str(path)], capture_output=True, text=True,
        timeout=4,
    )
    stdout = process.stdout + process.stderr
    assert process.returncode == 0, (path, process.returncode, stdout[:500])
    if "STATUS=UNIT_IDEAL" in stdout:
        return "UNIT_IDEAL"
    if "STATUS=NONUNIT" in stdout:
        return "NONUNIT"
    raise AssertionError((path, stdout[-500:]))


def main():
    assert __debug__
    for path, digest in PINS.items():
        assert sha256(path) == digest, path
    generator = load("generate_sparse_pair01.py")
    single_normalizer = load("enumerate_single_relaxations.py")
    double_normalizer = load("enumerate_double_relaxations.py")
    core = generator.load_core()
    amplitude_variables = set(core.SOURCE.values()) | set(core.U) | set(core.V)
    zero = sorted(amplitude_variables - generator.BASE_LIVE)
    assert len(amplitude_variables) == 87 and len(generator.BASE_LIVE) == 17 and len(zero) == 70

    base_metadata = json.loads((HERE / "metadata_base17.json").read_text())
    assert base_metadata["input"]["live_variables"] == sorted(generator.BASE_LIVE)
    assert base_metadata["input"]["emitted_equation_count"] == 59
    assert singular_status(HERE / base_metadata["input"]["path"]) == "UNIT_IDEAL"

    single = json.loads((HERE / "single_relaxation_ledger.json").read_text())
    single_run = json.loads((HERE / "results_single_relaxations.json").read_text())
    assert single["zero_coordinate_count"] == 70
    assert {item["extra"] for item in single["records"]} == set(zero)
    assert single["normalized_group_count"] == 28
    assert single_run["status"] == "PASS_TERMINAL_ALL_NORMALIZED_SINGLE_COORDINATE_GROUPS"
    assert single_run["group_count"] == 28 and single_run["unit_group_count"] == 28
    assert single_run["nonunit_group_count"] == 0
    assert sum(len(item["members"]) for item in single["normalized_polynomial_groups"]) == 70
    for group in single_run["groups"]:
        assert group["status"] == "UNIT_IDEAL"
        assert sha256(HERE / group["input"]) == group["input_sha256"]
        assert sha256(HERE / group["stdout"]) == group["stdout_sha256"]
        assert singular_status(HERE / group["input"]) == "UNIT_IDEAL"

    double = json.loads((HERE / "double_relaxation_ledger.json").read_text())
    double_run = json.loads((HERE / "results_double_search.json").read_text())
    all_pairs = {tuple(pair) for pair in itertools.combinations(zero, 2)}
    recorded_pairs = {tuple(item["pair"]) for item in double["pair_records"]}
    grouped_pairs = {
        tuple(pair) for group in double["groups"] for pair in group["members"]
    }
    assert len(all_pairs) == 2415 and recorded_pairs == all_pairs == grouped_pairs
    assert double["normalized_group_count"] == 381
    assert sum(len(group["members"]) for group in double["groups"]) == 2415
    assert double_run["status"] == "PASS_ALL_DOUBLE_GROUPS_UNIT"
    assert double_run["attempt_count"] == 381
    assert double_run["exact_lower_bound_on_extra_coordinates"] == 3
    assert all(item["status"] == "UNIT_IDEAL" for item in double_run["attempts"])
    assert sum(item["member_count"] for item in double_run["attempts"]) == 2415
    group_by_digest = {item["normalized_sha256"]: item for item in double["groups"]}
    assert len(group_by_digest) == 381
    for attempt in double_run["attempts"]:
        group = group_by_digest[attempt["normalized_sha256"]]
        assert attempt["representative"] == group["representative"]
        assert attempt["member_count"] == len(group["members"])
        assert sha256(HERE / attempt["input"]) == attempt["input_sha256"]
        assert sha256(HERE / attempt["stdout"]) == attempt["stdout_sha256"]
        assert singular_status(HERE / attempt["input"]) == "UNIT_IDEAL"

    # Independently regenerate every raw chart in a temporary directory and
    # recheck its canonical normalized-program digest against the ledger.
    single_digest = {item["extra"]: item["normalized_sha256"] for item in single["records"]}
    double_digest = {tuple(item["pair"]): item["normalized_sha256"] for item in double["pair_records"]}
    with tempfile.TemporaryDirectory(prefix="rep2_boundary_audit_") as temporary_directory:
        original_here = generator.HERE
        generator.HERE = Path(temporary_directory)
        try:
            for index, extra in enumerate(zero):
                generated = generator.build(generator.BASE_LIVE | {extra}, f"audit_s{index}")
                text = (generator.HERE / generated["path"]).read_text()
                normalized = single_normalizer.normalized_input(text, extra, generator.BASE_LIVE)
                assert sha256_text(normalized) == single_digest[extra]
            for index, pair in enumerate(itertools.combinations(zero, 2)):
                generated = generator.build(generator.BASE_LIVE | set(pair), f"audit_d{index}")
                text = (generator.HERE / generated["path"]).read_text()
                normalized = min(
                    double_normalizer.normalize(text, pair[0], pair[1], generator.BASE_LIVE),
                    double_normalizer.normalize(text, pair[1], pair[0], generator.BASE_LIVE),
                )
                assert sha256_text(normalized) == double_digest[pair]
        finally:
            generator.HERE = original_here

    # Scope guard: the parent 17-coordinate core point is not a full-pair01
    # point and also fails the rank-one guard and cap45 inactivity incidence.
    parent = json.loads((PINS.keys().__iter__().__next__().parent / "results_tensor_core_audit.json").read_text())
    point = {name: Fraction(value) for name, value in parent["rational_lift_test"]["point"].items()}
    guard_a06v_row1 = point["a06_10"] * point["v0"]
    assert guard_a06v_row1 == Fraction(-1, 2) != 0
    # A04 has only entry (0,1), so Row(A04)=span(e1), excluding e0.
    assert set(name for name in point if name.startswith("a04_")) == {"a04_01"}
    assert parent["rational_lift_test"]["other_pair01_violation_count"] == 13

    result = {
        "schema": "KRENN_X5_REP2_SPARSE_PAIR01_DOUBLE_BOUNDARY_AUDIT_V1",
        "status": "PASS_EXACT_NO_FULL_PAIR01_POINT_WITH_AT_MOST_TWO_EXTRA_COORDINATES",
        "pins": {str(path): digest for path, digest in PINS.items()},
        "coordinate_counts": {"amplitude": 87, "base_live": 17, "zero": 70},
        "base": {"charts": 1, "unit": 1, "nonunit": 0},
        "single": {"raw_charts": 70, "normalized_groups": 28, "unit_groups": 28, "nonunit": 0},
        "double": {"raw_charts": 2415, "normalized_groups": 381, "unit_groups": 381, "nonunit": 0},
        "exact_minimum_extra_coordinate_lower_bound": 3,
        "regenerated_normalization_checks": 70 + 2415,
        "independent_singular_unit_replays": 1 + 28 + 381,
        "parent_core_point_scope": {
            "full_pair01": False,
            "violated_pair01_equations": 13,
            "rank1_guard_A06v": False,
            "A06v_nonzero_witness": str(guard_a06v_row1),
            "cap45_inactivity_incidence": False,
            "incidence_reason": "Row(A04)=span(e1), so e0 is absent",
        },
        "logical_scope": {
            "included": "257 full pair01 amplitude equations on base17 plus <=2 amplitude coordinates",
            "excluded": "guard, cap67 adjoint, cap45/cap03 incidence, rank nonzero, and all remaining source coordinates",
            "consequence": "no Q or algebraic-closure point exists on any enumerated <=2-extra coordinate chart",
        },
        "hostile_checks": [
            "exact 70-coordinate singleton set equality",
            "exact C(70,2)=2415 pair set equality",
            "every raw chart regenerated to the sealed normalized digest",
            "all 409 representative ideals replay UNIT",
            "parent core43 point rejected as full-pair01/guard/incidence point",
        ],
    }
    output = HERE / "results_double_boundary_audit.json"
    temporary = output.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, output)
    print(json.dumps({
        "status": result["status"],
        "raw_charts": 1 + 70 + 2415,
        "unit_groups": 1 + 28 + 381,
        "lower_bound": 3,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
