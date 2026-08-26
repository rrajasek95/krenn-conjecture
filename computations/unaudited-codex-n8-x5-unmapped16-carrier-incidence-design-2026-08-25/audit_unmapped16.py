#!/usr/bin/env python3
"""Exact support/guard/carrier census for the 16 unmapped seven-block records."""

from __future__ import annotations

import collections
import copy
import hashlib
import itertools
import json
import os
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BOUNDARY = ROOT / "computations/unaudited-codex-n8-x5-seven-block-support-boundary-2026-08-25/results_seven_block_support_boundary.json"
COVERAGE = ROOT / "computations/unaudited-codex-n8-x5-seven-block-64-carrier-coverage-2026-08-25/results_64_carrier_coverage.json"
PINS = {
    ROOT / "computations/unaudited-codex-n8-x5-seven-block-support-boundary-2026-08-25/MANIFEST.sha256": "13bb284c0b400f7227db74f8a135155dd324251147ebf48711b9af8d10adcc85",
    BOUNDARY: "b3951e07149e4b831a5d3d3548284afb27f04154d805585468ba69bdb09b2f19",
    ROOT / "computations/unaudited-codex-n8-x5-seven-block-64-carrier-coverage-2026-08-25/MANIFEST.sha256": "944d1ec0df599056d4cadfe689093f621bfa9c939475efbd7158b7414443d578",
        COVERAGE: "e38dbd6f67c988da80bfbe0f5663a31a042daf8d7e29a9376f473b22325ab691",
}
FIXED = frozenset(((0, 3), (1, 6), (2, 7), (4, 5)))
TRIANGLE = frozenset((0, 1, 2))
INTERNAL_GUARD = frozenset(itertools.combinations(TRIANGLE, 2))


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def edge(label):
    return int(label[0]), int(label[1])


def label(value):
    return f"{value[0]}{value[1]}"


def A(value):
    return f"A{label(value)}"


def oriented(cap_site, residual_site):
    value = tuple(sorted((cap_site, residual_site)))
    return A(value) + ("^T" if cap_site < residual_site else "")


def transposed(expression):
    """Render the literal transpose, cancelling a stored-orientation transpose."""
    return expression[:-2] if expression.endswith("^T") else expression + "^T"


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


PM8 = tuple(sorted(matchings(tuple(range(8)))))
assert len(PM8) == 105


def response_terms(support, cap, pair):
    p, q = cap
    a, b = pair
    pa, qb = tuple(sorted((p, a))), tuple(sorted((q, b)))
    pb, qa = tuple(sorted((p, b))), tuple(sorted((q, a)))
    terms = []
    if pa in support and qb in support:
        terms.append({
            "orientation": "direct", "left_block": label(pa), "right_block": label(qb),
            "formula": f"{oriented(p,a)}*K*{transposed(oriented(q,b))}",
        })
    if pb in support and qa in support:
        terms.append({
            "orientation": "switched", "left_block": label(pb), "right_block": label(qa),
            "formula": f"{oriented(q,a)}*K^T*{transposed(oriented(p,b))}",
        })
    return terms


def carrier_terms(support, cap, kind, defining):
    residual = tuple(site for site in range(8) if site not in cap)
    if kind == "triangle":
        internal = set(itertools.combinations(defining, 2))
    else:
        center = defining[0]
        internal = {tuple(sorted((center, other))) for other in residual if other != center}
    terms = []
    for pair in itertools.combinations(residual, 2):
        if pair in internal:
            continue
        for term in response_terms(support, cap, pair):
            terms.append({"response_pair": label(pair), **term})
    return terms


def two_sandwich_record(cap, kind, defining, terms):
    if len(terms) != 2 or len({term["response_pair"] for term in terms}) != 2:
        return None
    left = {term["left_block"] for term in terms}
    right = {term["right_block"] for term in terms}
    if (len(left) == 1) == (len(right) == 1):
        return None
    common_side = "p" if len(left) == 1 else "q"
    common = next(iter(left if common_side == "p" else right))
    p, q = cap
    common_factor = oriented(p if common_side == "p" else q, next(site for site in range(8) if label(tuple(sorted(((p if common_side == 'p' else q), site)))) == common))
    partners = []
    for term in terms:
        pair = edge(term["response_pair"])
        a, b = pair
        if common_side == "p":
            partners.append(oriented(q, b if term["orientation"] == "direct" else a))
        else:
            partners.append(oriented(p, a if term["orientation"] == "direct" else b))
    factorization = (
        f"{common_factor}*K*[{'|'.join(partners)}]^T"
        if common_side == "p" else
        f"[{'|'.join(partners)}]*K*{common_factor}^T"
    )
    return {
        "kind": kind, "cap": label(cap), "defining_sites": list(defining),
        "identity_cap": cap in FIXED, "common_side": common_side,
        "common_block": common, "factorization_up_to_response_transposes": factorization,
        "terms": terms,
    }


def all_two_sandwich(support):
    records = []
    scanned = {"triangle": 0, "star": 0}
    for cap in itertools.combinations(range(8), 2):
        residual = tuple(site for site in range(8) if site not in cap)
        for defining in itertools.combinations(residual, 3):
            scanned["triangle"] += 1
            terms = carrier_terms(support, cap, "triangle", defining)
            record = two_sandwich_record(cap, "triangle", defining, terms)
            if record:
                records.append(record)
        for center in residual:
            scanned["star"] += 1
            terms = carrier_terms(support, cap, "star", (center,))
            record = two_sandwich_record(cap, "star", (center,), terms)
            if record:
                records.append(record)
    assert scanned == {"triangle": 560, "star": 168}
    return records, scanned


def guard_equations(support):
    records = []
    for pair in itertools.combinations(range(6), 2):
        if pair in INTERNAL_GUARD:
            continue
        terms = response_terms(support, (6, 7), pair)
        if terms:
            records.append({
                "response_pair": label(pair), "terms": terms,
                "matrix_equation_at_K_equals_I": "+".join(term["formula"].replace("K", "I") for term in terms) + "=0",
            })
    return records


def validate(result):
    assert result["schema"] == "KRENN_X5_UNMAPPED16_CARRIER_INCIDENCE_DESIGN_V1"
    assert result["status"] == "PASS_RECONSTRUCTION_AND_SINGULAR_BRANCH_REDUCTION"
    assert result["census"] == {"records": 16, "orbit_ids": 8, "matchings_per_record": 8, "no_anchor_records": 12, "no_rectangle_records": 4, "mathematically_closed_records": 0}
    assert result["selected_reduction"]["status"] == "PASS_EXACT_DESIGN_NO_SOLVE"
    assert result["scope"] == {"large_groebner_runs": 0, "mathematically_closed_records": 0, "full_conjecture": False}


def hostile(result, mutation):
    candidate = copy.deepcopy(result)
    mutation(candidate)
    try:
        validate(candidate)
    except (AssertionError, KeyError, TypeError):
        return True
    return False


def main():
    for path, expected in PINS.items():
        assert sha256(path) == expected, (path, sha256(path), expected)
    coverage = json.loads(COVERAGE.read_text())
    uncovered = coverage["uncovered"]
    assert len(uncovered) == 16 and sorted({item["orbit_id"] for item in uncovered}) == list(range(8))
    records = []
    for index, item in enumerate(uncovered):
        support = FIXED | {edge(value) for value in item["added"] + item["nonzero_variable_blocks"]}
        supported = [matching for matching in PM8 if set(matching) <= support]
        assert len(supported) == item["supported_perfect_matchings"] == 8
        guards = guard_equations(support)
        carriers, scanned = all_two_sandwich(support)
        expected_count = 24 if "12" in item["nonzero_variable_blocks"] else 40
        assert len(carriers) == expected_count
        assert collections.Counter(record["kind"] for record in carriers) == {"triangle": expected_count // 2, "star": expected_count // 2}
        if item["classification"] == "NO_GUARD_ANCHOR_06_OR_07":
            assert len(guards) == 2 and all(len(record["terms"]) == 2 for record in guards)
        else:
            assert guards == []
        records.append({
            "record_index": index, "orbit_id": item["orbit_id"], "added": item["added"],
            "nonzero_variable_blocks": item["nonzero_variable_blocks"],
            "classification": item["classification"], "support": list(map(label, sorted(support))),
            "supported_matchings": ["|".join(map(label, matching)) for matching in supported],
            "guard_equations": guards, "carrier_scan": scanned,
            "two_sandwich_census": {
                "total": len(carriers), "triangle": expected_count // 2, "star": expected_count // 2,
                "identity_cap": sum(record["identity_cap"] for record in carriers),
            },
            "two_sandwich_carriers": carriers,
        })

    selected_support = ("01", "15", "17", "23", "26", "46", "47")
    selected_records = [record for record in records if tuple(record["added"]) == selected_support]
    assert len(selected_records) == 2 and {"12" in record["nonzero_variable_blocks"] for record in selected_records} == {False, True}
    for record in selected_records:
        assert [item["response_pair"] for item in record["guard_equations"]] == ["14", "24"]
    selected_carrier = next(
        carrier for carrier in selected_records[0]["two_sandwich_carriers"]
        if carrier["kind"] == "star" and carrier["cap"] == "27" and carrier["defining_sites"] == [1]
    )
    assert selected_carrier["identity_cap"] is True and selected_carrier["common_block"] == "47" and selected_carrier["common_side"] == "q"
    assert [term["response_pair"] for term in selected_carrier["terms"]] == ["34", "46"]
    assert selected_carrier["terms"][0]["formula"] == "A23^T*K*A47^T"
    assert selected_carrier["terms"][1]["formula"] == "A47*K^T*A26"
    selected = {
        "status": "PASS_EXACT_DESIGN_NO_SOLVE",
        "records_covered_by_same_design": [record["record_index"] for record in selected_records],
        "support": list(selected_support),
        "A12_states": ["absent", "present"],
        "guard": {
            "equations": ["A47^T+A17*A46^T=0", "A26*A47^T+A46^T=0"],
            "elimination": "A46=-A47*A26^T",
            "reduced": "(I-A17*A26)*A47^T=0",
            "rank_consequence": "rank(A46)=rank(A47); if rank=3 then A17*A26=I and all A17,A26,A46,A47 are invertible",
        },
        "carrier": {
            "cap": "27", "cap_block": "A27=I", "kind": "star", "center": 1,
            "responses": ["R34=A23^T*K*A47^T", "R46^T=A26^T*K*A47^T"],
            "factorization": "[A23^T|A26^T]*K*A47^T (up to transposing R46)",
            "P": "ColSpan(A23,A26)", "Q": "Col(A47^T)=Row(A47)",
        },
        "singular_branch": {
            "ranks": [1, 2], "pairing_live_reason": "Q is proper and A27=I",
            "only_remaining_activity_failure": "exists i with e_i in P intersection Q",
            "rank_factorization": "A47=U*V^T with U,V full column rank r; then Q=Col(V)",
            "substitutions": ["A46=-U*V^T*A26^T", "(I-A17*A26)*V=0"],
            "incidence_equations": ["V*z=e_i", "A23*u+A26*w=e_i"],
            "rank_chart_census": {"raw_per_rank": 27, "S3_orbits_per_rank": 5},
            "A12_present_counts": {"rank1_variables": 86, "rank1_generators": 6571, "rank2_variables": 93, "rank2_generators": 6574},
            "A12_absent_counts": {"rank1_variables": 77, "rank1_generators": 6571, "rank2_variables": 84, "rank2_generators": 6574},
            "saturation": "one selected nonzero r-minor of U times one of V times sat = 1",
        },
        "invertible_branch_obstruction": "rank(A47)=3 forces A17*A26=I; no enumerated two-sandwich carrier has a guard-forced proper factor on this branch, so a full-X5 residual identity or different carrier is still required",
    }

    result = {
        "schema": "KRENN_X5_UNMAPPED16_CARRIER_INCIDENCE_DESIGN_V1",
        "status": "PASS_RECONSTRUCTION_AND_SINGULAR_BRANCH_REDUCTION",
        "census": {"records": 16, "orbit_ids": 8, "matchings_per_record": 8, "no_anchor_records": 12, "no_rectangle_records": 4, "mathematically_closed_records": 0},
        "records": records,
        "selected_reduction": selected,
        "pins": {str(path.relative_to(ROOT)): digest for path, digest in PINS.items()},
        "scope": {"large_groebner_runs": 0, "mathematically_closed_records": 0, "full_conjecture": False},
    }
    validate(result)
    tests = {
        "closure_overclaim": hostile(result, lambda value: value["census"].__setitem__("mathematically_closed_records", 2)),
        "solve_injection": hostile(result, lambda value: value["scope"].__setitem__("large_groebner_runs", 1)),
        "selected_status_mutation": hostile(result, lambda value: value["selected_reduction"].__setitem__("status", "PASS_CLOSED")),
        "conjecture_overclaim": hostile(result, lambda value: value["scope"].__setitem__("full_conjecture", True)),
    }
    assert all(tests.values())
    result["hostile_tests"] = tests
    temporary = HERE / "results_unmapped16_design.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_unmapped16_design.json")
    print(json.dumps({"status": result["status"], "records": 16, "selected_records": 2, "large_runs": 0}, sort_keys=True))


if __name__ == "__main__":
    main()
