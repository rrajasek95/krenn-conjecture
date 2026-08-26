#!/usr/bin/env python3
"""Exact 64-record coverage audit for the six full-family carrier theorems."""

from __future__ import annotations

import collections
import hashlib
import itertools
import json
import os
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BOUNDARY = ROOT / "computations/unaudited-codex-n8-x5-seven-block-support-boundary-2026-08-25"
SANDWICH = ROOT / "computations/unaudited-codex-n8-x5-seven-block-two-sandwich-reduction-2026-08-25"
PINS = {
    BOUNDARY / "MANIFEST.sha256": "13bb284c0b400f7227db74f8a135155dd324251147ebf48711b9af8d10adcc85",
    BOUNDARY / "results_seven_block_support_boundary.json": "b3951e07149e4b831a5d3d3548284afb27f04154d805585468ba69bdb09b2f19",
    SANDWICH / "MANIFEST.sha256": "056d73cd56818a18e2976707815f902cc433839ce69b192a88b118b7a9a5d707",
    SANDWICH / "results_two_sandwich_reduction.json": "1d94711066e002f9f827ce4ce392526d0cb46c5b5c0f5eaba584af571561d19c",
    ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep3-low-rank-carrier-2026-08-25/MANIFEST.sha256": "050dd75b8de30bc05bec61c9da1b8df2720a5a2e88741b49ff19e3de69d861c0",
    ROOT / "computations/unaudited-codex-n8-x5-seven-block-reps1-4-5-low-rank-carrier-2026-08-25/MANIFEST.sha256": "63f5f18c7740cb73d4832e2bff477a43d160ea5db9370b2ce64c3188de87bf68",
    ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep2-exhaustive-carrier-closure-2026-08-25/MANIFEST.sha256": "006512d367abfe79d554ce1f1ad3d2db897abc03659b642d9b7a2c148654681a",
}
FIXED = frozenset(((0, 3), (1, 6), (2, 7), (4, 5)))
REP_SUPPORTS = {
    0: ("06", "13", "17", "24", "26", "56", "57"),
    1: ("06", "13", "17", "25", "26", "46", "47"),
    2: ("06", "14", "17", "23", "26", "56", "57"),
    3: ("06", "14", "17", "25", "26", "36", "37"),
    4: ("06", "15", "17", "23", "26", "46", "47"),
    5: ("06", "15", "17", "24", "26", "36", "37"),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def edge(label: str):
    return int(label[0]), int(label[1])


def label(edge_value):
    return f"{edge_value[0]}{edge_value[1]}"


def matchings(vertices):
    if not vertices:
        yield ()
        return

    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in matchings(rest):
            yield tuple(sorted(((first, second),) + tail))


def star_terms(support, cap=(0, 3), center=4):
    p, q = cap
    residual = tuple(site for site in range(8) if site not in cap)
    terms = []
    for a, b in itertools.combinations(residual, 2):
        if center in (a, b):
            continue
        pa, qb = tuple(sorted((p, a))), tuple(sorted((q, b)))
        if pa in support and qb in support:
            terms.append({"left_block": label(pa), "orientation": "direct", "response_pair": f"{a}{b}", "right_block": label(qb)})
        pb, qa = tuple(sorted((p, b))), tuple(sorted((q, a)))
        if pb in support and qa in support:
            terms.append({"left_block": label(pb), "orientation": "switched", "response_pair": f"{a}{b}", "right_block": label(qa)})
    return terms


def cap67_guard_terms(support, outside):
    terms = []
    direct = ((0, 6), (outside, 7))
    switched = ((0, 7), (outside, 6))
    if all(block in support for block in direct):
        terms.append({"orientation": "direct", "left_block": "06", "right_block": f"{outside}7", "response_pair": f"0{outside}"})
    if all(block in support for block in switched):
        terms.append({"orientation": "switched", "left_block": "07", "right_block": f"{outside}6", "response_pair": f"0{outside}"})
    return terms


def atomic_json(path: Path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def main():
    for path, expected in PINS.items():
        assert sha256(path) == expected, (path, sha256(path), expected)
    boundary = json.loads((BOUNDARY / "results_seven_block_support_boundary.json").read_text())
    sandwich = json.loads((SANDWICH / "results_two_sandwich_reduction.json").read_text())
    orbit_records = boundary["exact_variable_stratum_classification"]["unresolved_orbit_records"]
    assert len(orbit_records) == 32
    records = []
    for orbit in orbit_records:
        assert len(orbit["members"]) == 2
        for member in orbit["members"]:
            records.append({"orbit_id": orbit["orbit_id"], **member})
    assert len(records) == 64
    keys = {(tuple(r["added"]), tuple(r["nonzero_variable_blocks"])) for r in records}
    assert len(keys) == 64
    reduction_keys = {(tuple(r["added"]), tuple(r["nonzero_variable_blocks"])) for r in sandwich["reductions"]}
    assert keys == reduction_keys

    # The second member of each full-family orbit is the exact guard mate.
    rep_by_support = {support: representative_id for representative_id, support in REP_SUPPORTS.items()}
    mate_by_support = {}
    for representative_id, first_orbit in zip(range(6), (8, 12, 16, 20, 24, 28)):
        group = [orbit for orbit in orbit_records if orbit["orbit_id"] == first_orbit]
        assert len(group) == 1
        first, mate = group[0]["members"]
        assert tuple(first["added"]) == REP_SUPPORTS[representative_id]
        mate_by_support[tuple(mate["added"])] = representative_id
    assert len(mate_by_support) == 6

    all_matchings = tuple(sorted(matchings(tuple(range(8)))))
    assert len(all_matchings) == 105
    covered = []
    uncovered = []
    for record in records:
        added_tuple = tuple(record["added"])
        representative_id = rep_by_support.get(added_tuple, mate_by_support.get(added_tuple))
        is_mate = added_tuple in mate_by_support
        support = FIXED | {edge(item) for item in record["added"] + record["nonzero_variable_blocks"]}
        supported_matching_count = sum(set(matching) <= support for matching in all_matchings)
        if representative_id is None:
            anchors = [item for item in ("06", "07") if edge(item) in support]
            rectangles = [r for r in (3, 4, 5) if (r, 6) in support and (r, 7) in support]
            if not anchors:
                reason = "NO_GUARD_ANCHOR_06_OR_07"
                missing = "the cap67 guard has no R0r product whose zero forces the common block of an identity-cap carrier proper"
            else:
                assert anchors == ["06", "07"] and not rectangles
                reason = "NO_OUTSIDE_R6_R7_RECTANGLE"
                missing = "the support has both anchors but no outside r with both r6 and r7, so the cap67 guard supplies no one-product singularity implication"
            uncovered.append({
                "orbit_id": record["orbit_id"],
                "added": record["added"],
                "nonzero_variable_blocks": record["nonzero_variable_blocks"],
                "supported_perfect_matchings": supported_matching_count,
                "classification": reason,
                "first_missing_rank_implication": missing,
            })
            continue

        outside_rectangles = [r for r in (3, 4, 5) if (r, 6) in support and (r, 7) in support]
        assert len(outside_rectangles) == 1
        outside = outside_rectangles[0]
        anchor = "07" if is_mate else "06"
        outside_factor = f"{outside}6" if is_mate else f"{outside}7"
        assert edge(anchor) in support and edge(outside_factor) in support
        guard_terms = cap67_guard_terms(support, outside)
        assert len(guard_terms) == 1
        assert guard_terms[0]["left_block"] == anchor and guard_terms[0]["right_block"] == outside_factor
        carrier_terms = star_terms(support)
        anchor_terms = [term for term in carrier_terms if term["left_block"] == anchor]
        assert len(carrier_terms) == len(anchor_terms) == 2
        assert len({term["response_pair"] for term in carrier_terms}) == 2
        assert (0, 3) in FIXED
        # Every recorded coefficient boundary retains A04 and A35, but the
        # P-proper/I-cap argument is independent of partner rank or variable zeros.
        assert "04" in record["nonzero_variable_blocks"] and "35" in record["nonzero_variable_blocks"]
        covered.append({
            "orbit_id": record["orbit_id"],
            "representative_id": representative_id,
            "guard_mate": is_mate,
            "added": record["added"],
            "nonzero_variable_blocks": record["nonzero_variable_blocks"],
            "supported_perfect_matchings": supported_matching_count,
            "guard_response_pair": f"0{outside}",
            "guard_single_product": guard_terms[0],
            "nonzero_outside_factor": outside_factor,
            "forced_proper_space": f"Col(A{anchor})",
            "identity_cap": "A03=I",
            "carrier": {"cap": "03", "star_center": 4, "common_block": anchor, "terms": carrier_terms},
            "variable_zero_boundaries_safe": "the activity proof only uses proper P and A03=I; Q may have arbitrary rank and absent variable blocks are set literally to zero",
        })

    assert len(covered) == 48 and len(uncovered) == 16
    assert collections.Counter(item["classification"] for item in uncovered) == {"NO_GUARD_ANCHOR_06_OR_07": 12, "NO_OUTSIDE_R6_R7_RECTANGLE": 4}
    assert sorted({item["orbit_id"] for item in uncovered}) == list(range(8))
    assert sorted({item["orbit_id"] for item in covered}) == list(range(8, 32))
    assert collections.Counter(item["representative_id"] for item in covered) == {i: 8 for i in range(6)}
    assert collections.Counter((item["representative_id"], item["guard_mate"]) for item in covered) == {(i, mate): 4 for i in range(6) for mate in (False, True)}

    result = {
        "schema": "KRENN_X5_SEVEN_BLOCK_64_CARRIER_COVERAGE_V1",
        "status": "PASS_MAPPING_48_PAIRING_ONLY_ZERO_CLOSURE",
        "census": {"records": 64, "symmetry_orbits": 32, "pairing_only_records": 48, "pairing_only_orbits": 24, "mathematically_closed_records": 0, "unmapped_records": 16, "unmapped_orbits": 8},
        "coverage": covered,
        "uncovered": uncovered,
        "pairing_only_reduction": {
            "statement": "Every record in orbit 8..31 has exactly one guard anchor (06 for the representative, 07 for its mate) and one complete outside rectangle. Its sole R0r guard product has a nonzero outside factor, forcing the anchor singular. The independently enumerated cap03/star4 carrier has that anchor as common left factor; A03=I proves pairing activity only.",
            "zero_coefficient_scope": "all four recorded variable subsets, including A12=0 and/or A67=0, are covered; the proof does not use either block",
            "full_family_nonzero_A67_not_needed_for_pairing": True,
            "missing_diagonal_lemma": "For each record and i=0,1,2 prove not(e_i in P and e_i in Q). P proper alone is insufficient.",
            "abstract_countermodel": "P=Q=span(e0): I is outside P tensor Q but E00 is inside",
        },
        "no_go": {
            "all_64_closed": False,
            "previous_48_closure_claim_retracted": True,
            "first_six_orbits": "no 06/07 guard anchor",
            "orbits_six_and_seven": "both 06/07 but no outside rectangle",
            "smallest_missing_lemma": "For each of the eight non-full-family support orbits, derive a different guard-forced proper response subspace (or a literal amplitude contradiction); the six full-family anchor-singularity theorems supply neither.",
        },
        "eight_block_extension": {"attempted": False, "reason": "zero of 64 records are closed by the six pairing-only theorems; no monotone extension is claimed"},
        "pins": {str(path.relative_to(ROOT)): digest for path, digest in PINS.items()},
        "scope": {"complete_seven_block_theorem": False, "full_conjecture": False, "broad_computation": False},
    }
    atomic_json(HERE / "results_64_carrier_coverage.json", result)
    print(json.dumps({"status": result["status"], "pairing_only": 48, "closed": 0, "unmapped": 16}, sort_keys=True))


if __name__ == "__main__":
    main()
