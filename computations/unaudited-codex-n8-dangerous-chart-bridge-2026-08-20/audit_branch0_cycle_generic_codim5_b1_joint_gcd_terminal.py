#!/usr/bin/env python3
"""Freeze the live-normalized terminal joint-gcd compression."""

from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
STATE = HERE / "results_branch0_cycle_generic_codim5_b1_joint_gcd_state.json"
EXPORT = HERE / "results_branch0_cycle_generic_qrs_codim3_export.json"
RESULT = HERE / "results_branch0_cycle_generic_codim5_b1_joint_gcd_terminal.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> None:
    state = json.loads(STATE.read_text())
    export = json.loads(EXPORT.read_text())
    require(state["processed_rows"] == ["P1846"]
            and len(state["steps"]) == 1,
            "joint-gcd did not stop after P1846")
    step = state["steps"][0]
    require(state["accumulator"] == "d4"
            and step["accumulator_after"] == {
                "terms": 1, "degree": 1,
                "sha256": "af327a6478537246e0d9f0c589986d5f067d2e2351a1ca5a0a4962424da0e408"},
            "P1846 accumulator is no longer literal d4")
    require("d4" in export["live_factors"],
            "d4 ceased to be an audited live chart factor")
    require(step["gcd_accumulator_after_J"]["degree"] == 0,
            "d4 unexpectedly acquired a common factor with J")
    result = {
        "status": "UNAUDITED exact live-normalized joint-gcd terminal",
        "state": STATE.name,
        "state_sha256": sha256(STATE.read_bytes()).hexdigest(),
        "processed_rows": ["P1846"],
        "initial_accumulator_profile": state["initial_K_over_A_profile"],
        "P1846_fraction_free_numerator_profile":
            step["fraction_free_numerator_profile"],
        "exact_gcd_before_live_normalization": "d4",
        "audited_live_factor": "d4",
        "normalized_accumulator": "1",
        "remaining_rows_not_needed_for_hypersurface_compression":
            ["Q4098", "R4885", "S4331", "T4750", "U3217"],
        "theorem": (
            "On the A*d4-open generic PRS branch, the P324/P851/P1342/"
            "P1846 common-root projection has no common hypersurface factor."),
        "nonclaim": (
            "A unit multivariate gcd is not a Bezout identity in four "
            "parameter variables and does not by itself prove the common "
            "zero set empty or D10 radical containment."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("live-normalized joint-gcd terminal: PASS")
    print("gcd -> d4 -> 1 on d4-open chart")
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
