#!/usr/bin/env python3
"""Assemble the complete exact D0=0 theorem inside the Delta-open cycle chart."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def require(condition, message):
    if not condition: raise RuntimeError(message)


def logical_hash(value):
    return sha256(json.dumps(value, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def read_logical(path):
    value = json.loads(path.read_text()); frozen = value.pop("logical_sha256")
    require(logical_hash(value) == frozen, f"logical mismatch: {path}")
    return value, frozen


def main():
    c0_path = (ROOT / "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20" /
               "results_branch0_cycle_d0_cramer_exception.json")
    c0 = json.loads(c0_path.read_text())
    require(c0["result_sha256"] ==
            "a8b5f3480b137580b6cd6751171afdc2cec5cc6505239e6cd62ba47fa776e6d0",
            "C0=0 closure changed")
    old_ledger, old_hash = read_logical(HERE / "results_d0_theorem_ledger.json")
    require(old_hash ==
            "cd25ef17331e546dad33d8c85bb024acef66406cd03bebf4c8e73152772eb883" and
            old_ledger["open"] == ["D0=0,C0!=0,selected-pivot=0"],
            "pre-pivot ledger changed")
    delta, delta_hash = read_logical(HERE / "results_d0_pivot_zero_delta_scope.json")
    o1, o1_hash = read_logical(HERE / "results_d0_pivot_zero_R0_R1_gate_audit.json")
    o2, o2_hash = read_logical(HERE / "results_d0_pivot_zero_R0_S42_gate_audit.json")
    o3, o3_hash = read_logical(HERE / "results_d0_pivot_zero_R1_S256_gate_audit.json")
    require(delta_hash ==
            "c694d0d8676452be54dc6f529f93a8edd6ac84d9229f4aafde2802ccd5dac9c9",
            "Delta correction changed")
    require(o1_hash ==
            "843442aa0e1f82d6bdc367f03e8de300c01e97bb2fc07cd3a7ef8942dc630479",
            "O1 closure changed")
    require(o2_hash ==
            "e505d4627acb06602ec3e9fe29a731807e5d01a1d6b3c1bfe1ae3570690953bf",
            "O2 closure changed")
    require(o3_hash ==
            "ddfaef7abe057df82b59ec69cab3c41563f403ace017d95ef492308db61669a8",
            "O3 closure changed")
    require(delta["source_admissible_pair_count"] == 5 and
            delta["source_admissible_orbit_count"] == 3,
            "pivot-zero admissible cover changed")
    require("R0=R2" in o1["symmetry_consequence"] and
            "R2=S256" in o3["symmetry_consequence"],
            "involutive mate coverage changed")
    require("O3 is untouched" in o2["scope_guard"] and
            "all three" in o3["combined_pivot_zero_conclusion"],
            "sequential orbit scope changed")

    result = {
        "status": "complete exact D0=0 theorem inside Delta-open cycle chart PASS",
        "ambient_assumptions": ["branch-0 four-cycle interior",
                                "Delta!=0", "declared Laurent/selected factors live"],
        "C0_split": {
            "C0=0": {"closed": True, "digest": c0["result_sha256"]},
            "C0!=0": {
                "selected_pivot!=0": {"closed": True,
                                      "ledger_digest": old_hash},
                "selected_pivot=0": {
                    "closed": True,
                    "cover": ["O1: R0R1 or R0R2", "O2: R0S42",
                              "O3: R1S256 or R2S256"],
                    "digests": [delta_hash, o1_hash, o2_hash, o3_hash],
                },
            },
        },
        "theorem": ("Under the declared Delta-open branch-0 four-cycle interior "
                    "assumptions, the complete D0=0 source scheme is empty over Q."),
        "scope_guards": [
            "This is the complete D0=0 branch, not the complete four-cycle.",
            "The separately analyzed Delta=0 subtree is not inferred from this ledger.",
            "D0!=0 generic residuals and recursive term-boundary faces are not covered.",
        ],
        "mutation_control": ("Removing any O1/O2/O3 orbit restores one of the five "
                             "source-admissible pivot-zero factor pairs."),
    }
    result["logical_sha256"] = logical_hash(result)
    (HERE / "results_d0_complete_theorem_ledger.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("complete D0 theorem ledger PASS", result["logical_sha256"])


if __name__ == "__main__": main()
