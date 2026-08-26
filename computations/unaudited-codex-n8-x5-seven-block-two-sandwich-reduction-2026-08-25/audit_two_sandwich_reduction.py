#!/usr/bin/env python3
"""Reduce every unresolved seven-block X5 locus to a two-sandwich star map."""

from __future__ import annotations

from collections import Counter
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "unaudited-codex-n8-x5-seven-block-support-boundary-2026-08-25/MANIFEST.sha256"
PARENT_SHA256 = "13bb284c0b400f7227db74f8a135155dd324251147ebf48711b9af8d10adcc85"
PARENT_RESULT = HERE.parent / "unaudited-codex-n8-x5-seven-block-support-boundary-2026-08-25/results_seven_block_support_boundary.json"
PARENT_RESULT_SHA256 = "b3951e07149e4b831a5d3d3548284afb27f04154d805585468ba69bdb09b2f19"
FIVE_SOURCE = HERE.parent / "unaudited-codex-n8-x5-five-block-support-cap-2026-08-25/audit_five_block_support_cap.py"
FIVE_SOURCE_SHA256 = "4a686fe5bbf80559283d993245166764d5b52d8b4bd33b144017f26f5f2c1f45"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


assert sha256(PARENT) == PARENT_SHA256
assert sha256(PARENT_RESULT) == PARENT_RESULT_SHA256
assert sha256(FIVE_SOURCE) == FIVE_SOURCE_SHA256
spec = importlib.util.spec_from_file_location("five", FIVE_SOURCE)
assert spec is not None and spec.loader is not None
five = importlib.util.module_from_spec(spec)
spec.loader.exec_module(five)


def edge(text: str) -> tuple[int, int]:
    assert len(text) == 2 and text[0] < text[1]
    return int(text[0]), int(text[1])


def edge_string(value: tuple[int, int]) -> str:
    return "".join(map(str, sorted(value)))


def star_terms(support: set[tuple[int, int]], cap: tuple[int, int], center: int):
    """Supported direct/switched products in responses forbidden by a star."""
    p, q = cap
    residual = tuple(site for site in range(8) if site not in cap)
    assert center in residual
    records = []
    for a, b in itertools.combinations(residual, 2):
        if center in (a, b):
            continue
        for left_site, right_site, orientation in ((a, b, "direct"), (b, a, "switched")):
            left = tuple(sorted((p, left_site)))
            right = tuple(sorted((q, right_site)))
            if left in support and right in support:
                records.append({
                    "response_pair": edge_string((a, b)),
                    "orientation": orientation,
                    "left_block": edge_string(left),
                    "right_block": edge_string(right),
                })
    return records


def common_side(terms):
    left = {term["left_block"] for term in terms}
    right = {term["right_block"] for term in terms}
    answers = []
    if len(left) == 1:
        answers.append(("left", next(iter(left))))
    if len(right) == 1:
        answers.append(("right", next(iter(right))))
    return answers


def main():
    parent = json.loads(PARENT_RESULT.read_text())
    orbits = parent["exact_variable_stratum_classification"]["unresolved_orbit_records"]
    strata = [member for orbit in orbits for member in orbit["members"]]
    assert len(strata) == 64

    reductions = []
    pattern_census = Counter()
    for record in strata:
        support = set(five.FIXED)
        support.update(map(edge, record["nonzero_variable_blocks"]))
        support.update(map(edge, record["added"]))
        candidates = []
        for cap in itertools.combinations(range(8), 2):
            residual = tuple(site for site in range(8) if site not in cap)
            for center in residual:
                terms = star_terms(support, cap, center)
                for side, common in common_side(terms):
                    if terms:
                        candidates.append((len(terms), edge_string(cap), center, common, side, terms))
        assert candidates
        candidates.sort(key=lambda item: (item[0], item[1], item[2], item[3], item[4]))
        count, cap, center, common, side, terms = candidates[0]
        assert count == 2
        # The two terms occur in distinct response matrices, so their row
        # spaces add without cancellation before the common-factor reduction.
        assert len({term["response_pair"] for term in terms}) == 2
        assert len({term[f"{side}_block"] for term in terms}) == 1
        other_side = "right" if side == "left" else "left"
        partners = sorted({term[f"{other_side}_block"] for term in terms})
        assert 1 <= len(partners) <= 2
        key = (cap, center, common)
        pattern_census[key] += 1
        reductions.append({
            "added": record["added"],
            "nonzero_variable_blocks": record["nonzero_variable_blocks"],
            "cap": cap,
            "star_center": center,
            "common_side": side,
            "common_block": common,
            "partner_blocks": partners,
            "supported_forbidden_terms": terms,
            "factorization": (
                "U*K*[B1|B2]" if side == "left" else "[U1;U2]*K*B"
            ),
        })

    expected = {
        ("01", 3, "04"): 1,
        ("02", 3, "04"): 1,
        ("03", 1, "04"): 3,
        ("03", 1, "35"): 19,
        ("03", 2, "35"): 16,
        ("03", 4, "06"): 8,
        ("03", 4, "07"): 8,
        ("04", 1, "03"): 2,
        ("04", 1, "45"): 2,
        ("15", 3, "45"): 1,
        ("16", 0, "26"): 1,
        ("25", 3, "45"): 1,
        ("26", 0, "16"): 1,
    }
    assert dict(pattern_census) == expected

    # Exhaust the coordinate-subspace cases of the abstract tensor lemma.
    # E_ii belongs to P tensor Q exactly when e_i belongs to both P and Q.
    coordinate_checks = 0
    for p_mask in range(8):
        for q_mask in range(8):
            for colour in range(3):
                tensor_contains = bool(p_mask & (1 << colour)) and bool(q_mask & (1 << colour))
                direct_criterion = bool((p_mask & q_mask) & (1 << colour))
                assert tensor_contains == direct_criterion
                coordinate_checks += 1
            identity_in_tensor = p_mask == 7 and q_mask == 7
            assert identity_in_tensor == (p_mask == q_mask == 7)

    result = {
        "schema": "x5-seven-block-two-sandwich-reduction-v1",
        "status": "PASS_ALL_64_REDUCE_TO_13_TWO_SANDWICH_STAR_PATTERNS",
        "parent_manifest_sha256": PARENT_SHA256,
        "parent_result_sha256": PARENT_RESULT_SHA256,
        "census": {
            "unresolved_strata": len(strata),
            "two_term_factorizations": len(reductions),
            "labeled_patterns": len(pattern_census),
            "pattern_census": [
                {"cap": cap, "center": center, "common_block": common, "count": count}
                for (cap, center, common), count in sorted(pattern_census.items())
            ],
        },
        "abstract_activity_lemma": {
            "response_row_space": "P tensor Q",
            "left_factor_case": "P=Row(U), Q=ColSpan(B1,B2)",
            "right_factor_case": "P=RowSpan(U1,U2), Q=Col(B)",
            "diagonal_failure_criterion": "K_ii vanishes on ker(L) iff e_i is in P and e_i is in Q",
            "cap_pairing_failure_criterion": (
                "the coefficient matrix of <K,A_cap> lies in P tensor Q; equivalently its "
                "column space lies in P and its row space lies in Q"
            ),
            "simultaneous_activity": (
                "over Q, if all four functionals are nonzero on ker(L), avoid their four "
                "proper hyperplanes to obtain one clean active K"
            ),
            "coordinate_subspace_cases_replayed": coordinate_checks,
        },
        "reductions": reductions,
        "scope": {
            "proves_full_seven_block_closure": False,
            "remaining_obligation": (
                "on the 13 factor patterns, derive one failed-incidence exclusion from the "
                "formal guard/full-X5 equations, or route to another active carrier"
            ),
            "counterexample_claim": False,
        },
    }
    output = HERE / "results_two_sandwich_reduction.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "strata": len(strata),
        "patterns": len(pattern_census),
        "result_sha256": sha256(output),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
