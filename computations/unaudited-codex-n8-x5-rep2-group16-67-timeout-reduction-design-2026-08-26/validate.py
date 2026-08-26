#!/usr/bin/env python3
"""Fail-closed validation of the design-only rep2 group16 reduction package."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def split_top(text: str) -> list[str]:
    out, depth, start = [], 0, 0
    for i, char in enumerate(text):
        if char == "(": depth += 1
        elif char == ")": depth -= 1
        elif char == "," and depth == 0:
            out.append(text[start:i]); start = i + 1
    out.append(text[start:])
    assert depth == 0
    return out


def main() -> None:
    result_path = HERE / "results_design.json"
    result = json.loads(result_path.read_text())
    assert result["status"] == "PASS_DESIGN_ONLY_NO_SOLVE"
    assert result["solver_run"] is False and result["unit_certificate"] is False
    assert result["minimal_literal_unit_subset"] is None
    assert result["source"]["sha256"] == "2403105f5c6bf4860525220d0d2d036099b79ace67297c864767ae71b9e97339"
    assert result["terminal_referee"]["sha256"] == "d0f48380558bb663567083c744667f76fad18cb85cc47e0e93b857dc05cac68f"
    ranks = result["ranks"]["exact_Q"]
    assert ranks == {
        "amplitude_affine_linear_part_Q": 19,
        "amplitude_coefficient_span_Q": 6561,
        "amplitude_variable_support_incidence_Q": 47,
        "monomial_exponent_incidence_Q": 67,
    }
    assert result["amplitude_structure"]["all_67_coordinates_active"] is True
    assert result["amplitude_structure"]["monic_graph_candidates_all_generators"] == []
    assert result["amplitude_structure"]["exact_linear_redundancy"] == 0
    expected = {
        "Dt1": (64, 6569),
        "Vt1_Dt2": (63, 6569),
        "Vt1_Vt2_Dt0": (64, 6569),
        "Vt0_Vt1_Vt2": (62, 6568),
    }
    strata = result["exact_stratified_cover"]["strata"]
    assert len(strata) == 4 and {s["name"] for s in strata} == set(expected)
    for stratum in strata:
        path = HERE / stratum["source"]
        assert sha256(path) == stratum["sha256"]
        text = path.read_text()
        assert "slimgb" not in text and "std(" not in text and "reduce(" not in text
        variables = text.split("ring r=0,(", 1)[1].split("),dp;", 1)[0].split(",")
        generators = split_top(text.split("ideal I=", 1)[1].split(";\n", 1)[0])
        assert (len(variables), len(generators)) == expected[stratum["name"]]
        assert len(generators) == len(set(generators))
        for removed in stratum["removed_variables"]:
            assert removed not in variables
    canonical = result["canonical_expanded_reference"]
    assert sha256(HERE / canonical["path"]) == canonical["sha256"]
    tail = result["tail_expansion"]
    assert sha256(HERE / tail["path"]) == tail["sha256"]
    terminal = json.loads((ROOT / result["terminal_referee"]["path"]).read_text())
    assert terminal["status"] == "PASS_FAIL_CLOSED_NATIVE_WALL_ZERO_COVERAGE"
    assert terminal["mathematical_coverage"] is False
    assert terminal["automatic_relaunch"] is False
    print("PASS_DESIGN_ONLY_NO_SOLVE")


if __name__ == "__main__":
    main()
