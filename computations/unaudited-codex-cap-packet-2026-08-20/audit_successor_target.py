#!/usr/bin/env python3
"""Adversarial calibration for the proposed N=8 X4-to-clean-cap theorem.

This script does not search an unbounded source space.  It audits the three
named existing calibration families:

* W25-F8: exact all-blocked X3 point (near-falsifier, but not X4);
* W37: counterfactual modifications of F8's cap equations (not new sources);
* W40: an actual four-dimensional X4 torus with an explicit clean cap.

For W25-F8 it independently rebuilds every raw coefficient and re-decides
all live pairs with exact Qbar Rabinowitsch saturation using this lane's cap
encoder.  A negative theorem is not inferred from the bounded census.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import audit_cap_packet as CAP  # noqa: E402


W25_OBJECT = (ROOT / "computations/unaudited-x3core-w25-2026-08-15/"
              "OBJECT_W25-F8_n8_allblocked_X3.json")
W25_OLD_RESULTS = (ROOT / "computations/unaudited-x3core-w25-2026-08-15/"
                   "results_t3c_n8_rungs.json")
W37_RUN = (ROOT / "computations/unaudited-witness-w37-2026-08-20/"
           "run_a2_counterfactual.py")
W37_ENCODER = (ROOT / "computations/unaudited-witness-w37-2026-08-20/"
               "run_a1_falsifier.py")
W37_RESULTS = (ROOT / "computations/unaudited-witness-w37-2026-08-20/"
               "results_a2_counterfactual.json")
W40_TORUS = HERE / "results_w40_torus_cap.json"
PINS = {
    W25_OBJECT: "46d6e207e392deaa7e0bfc4221c7f5cc6735f11a2a14cc388292ca6850dd33f6",
    W25_OLD_RESULTS: "194d3d2fdcb49b0b41ecab63a50e7a7abb0cb2bed68a2ddb9f2644999cb91c58",
    W37_RUN: "c2b258c3327da3efb5a89db6ca5f47248660e6923ba862184b9f8cd5c4e2c9f3",
    W37_ENCODER: "fa779b32ac1a12a3d653578a29eeb7ef5c6291b4afade3dd576988fca2833651",
    W37_RESULTS: "711f6425d92d89750252e0fbabebd3616b7f0d8cb6d8ee195baece04d3784445",
}
DECLARED_CONTROLS = {
    "pinned_inputs",
    "w25_raw_word_replay",
    "w25_old_decider_agreement",
    "w40_positive_saturation_control",
    "w37_source_scope_guard",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_w25():
    obj = json.loads(W25_OBJECT.read_text())
    source = {}
    for key, matrix in obj["blocks"].items():
        u, v = (int(piece) for piece in key.split(","))
        source[(u, v)] = tuple(tuple(Fraction(value) for value in row)
                               for row in matrix)
    require(set(source) == set(combinations(CAP.SITES, 2)), len(source))
    return source


def replay_words(source):
    defects = []
    for word in product(CAP.COLOURS, repeat=CAP.N):
        value = CAP.hafnian_word(source, word)
        target = Fraction(1) if len(set(word)) == 1 else Fraction(0)
        if value != target:
            defects.append({
                "word": "".join(map(str, word)),
                "off": CAP.N - max(word.count(c) for c in CAP.COLOURS),
                "value": str(value),
            })
    return defects


def main():
    controls_run = set()
    for path, expected in PINS.items():
        require(sha256(path.read_bytes()).hexdigest() == expected,
                (str(path), "pin changed"))
    controls_run.add("pinned_inputs")

    source = load_w25()
    defects = replay_words(source)
    profile = Counter(entry["off"] for entry in defects)
    require(profile == {4: 78, 5: 25}, profile)
    require(all(entry["off"] >= 4 for entry in defects), profile)
    controls_run.add("w25_raw_word_replay")

    live_pairs = tuple(edge for edge in combinations(CAP.SITES, 2)
                       if any(CAP.cell(source, *edge, i, j)
                              for i in CAP.COLOURS for j in CAP.COLOURS))
    require(len(live_pairs) == 21, live_pairs)
    cap_records = {}
    for edge in live_pairs:
        _, scalar, _, words, polynomials = CAP.error_polynomials(source, edge)
        decision = CAP.singular_decision(polynomials, scalar, timeout=120)
        require(decision["status"] != "UNCHECKED_TIMEOUT", (edge, decision))
        cap_records[CAP.edge_name(edge)] = {
            "nonzero_error_polynomials": len(polynomials),
            "decision": decision,
        }
    require(all(record["decision"]["rabinowitsch_unit"]
                for record in cap_records.values()), cap_records)
    old = json.loads(W25_OLD_RESULTS.read_text())
    old_rows = old["third_route"]["rows"]
    require(len(old_rows) == 21 and
            all(row["sat_verdict"] == "BLOCKED" for row in old_rows),
            old_rows)
    controls_run.add("w25_old_decider_agreement")

    # Positive control through the exact same polynomial and saturation path:
    # W40's integral X4 point must have non-unit cap ideal at pair 67.
    w40raw = json.loads(CAP.W40_RESULT.read_text())
    w40source = CAP.parse_source(
        w40raw["engine_audit"]["witness_B_integral"]["source"]
    )
    _, scalar67, _, _, polynomials67 = CAP.error_polynomials(w40source, (6, 7))
    positive = CAP.singular_decision(polynomials67, scalar67, timeout=120)
    explicit = CAP.find_small_rational_cap(polynomials67, scalar67)
    require(not positive["rabinowitsch_unit"] and explicit is not None,
            (positive, explicit))
    controls_run.add("w40_positive_saturation_control")

    # W37's E_X4/E_X5 rows modify the cap polynomials by adding selected
    # H_B defect values from the fixed F8 blocks.  They never alter `src` or
    # verify the modified blocks against X4.  Pin and assert the semantic
    # markers so a future rewrite cannot silently change this scope audit.
    w37_text = W37_RUN.read_text()
    w37_encoder = W37_ENCODER.read_text()
    require("src = load_f8()" in w37_text and
            "decide_cleaned(src" in w37_text and
            "def sym_cap_system_cleaned(src" in w37_encoder and
            "table[w] = C._padd" in w37_encoder,
            "W37 counterfactual semantics changed")
    w37 = json.loads(W37_RESULTS.read_text())
    require(w37["summary"] == {
        "E_X5": {"BLOCKED": 21},
        "E_X4": {"BLOCKED": 21},
        "E0": {"BLOCKED": 21},
        "E_o5": {"BLOCKED": 21},
    }, w37["summary"])
    controls_run.add("w37_source_scope_guard")

    require(W40_TORUS.exists(), "run audit_w40_torus_cap.py first")
    torus = json.loads(W40_TORUS.read_text())
    require(torus["status"] == "PASS" and
            torus["cap67"]["activity_product"] == "1" and
            not torus["cap67"]["error_nonzero_coefficients"], torus)

    require(controls_run == DECLARED_CONTROLS,
            {"declared": sorted(DECLARED_CONTROLS),
             "executed": sorted(controls_run)})
    result = {
        "status": "PASS",
        "classification": "UNAUDITED BOUNDED ADVERSARIAL AUDIT",
        "target": (
            "Every N=8 ternary level-4 X4 source with nonzero pure "
            "amplitudes has an active clean cap"
        ),
        "w25_F8": {
            "raw_membership": "X3_NOT_X4",
            "raw_defects_by_off_count": {str(k): v
                                          for k, v in sorted(profile.items())},
            "live_pairs": len(live_pairs),
            "exact_saturation": "21/21 BLOCKED over Qbar",
            "new_decisions": cap_records,
            "verdict_for_target": (
                "near-falsifier excluded by 78 nonzero level-4 rows"
            ),
        },
        "w37": {
            "stored_counterfactual_summary": w37["summary"],
            "verdict_for_target": (
                "not a source construction: selected H_B defect values are "
                "zeroed inside E while the fixed W25-F8 blocks are retained"
            ),
        },
        "w40": {
            "raw_membership": "FOUR_DIMENSIONAL_X4_LAURENT_TORUS",
            "cap67": "K=I, activity=1, E=0 identically",
            "integral_point_live_pair_census": (
                "7 active-cap pairs and 10 blocked pairs by exact saturation"
            ),
            "verdict_for_target": "positive four-dimensional stratum",
        },
        "bounded_search_verdict": (
            "NO ALL-BLOCKED X4 FALSIFIER IN THE NAMED W25/W37/W40 INPUTS; "
            "this is not evidence of the universal theorem"
        ),
        "sharp_sublemma": (
            "At N=8, if an active pair has response support of matching "
            "number at most one, then r^2=0 and hence E=0.  The W40 torus "
            "realizes this at pair 67: its four nonzero response cells form "
            "a star centered at residual site 5."
        ),
        "controls": {
            "declared": sorted(DECLARED_CONTROLS),
            "executed": sorted(controls_run),
            "all_ran": True,
        },
    }
    output = HERE / "results_successor_target.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
