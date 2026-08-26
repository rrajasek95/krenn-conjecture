#!/usr/bin/env python3
"""Exact source-labelled low-rank/carrier proof for full-family representative 3."""

from __future__ import annotations

import hashlib
import json
import os
from fractions import Fraction
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FULL_DIR = ROOT / "computations/unaudited-codex-n8-x5-seven-block-guard-dual-gate-2026-08-25"
SANDWICH_DIR = ROOT / "computations/unaudited-codex-n8-x5-seven-block-two-sandwich-reduction-2026-08-25"
PINS = {
    FULL_DIR / "MANIFEST.sha256": "21f351085e1650dcf64889103813c869853f47b74a432596a9147d3324536acf",
    FULL_DIR / "results_full_family_obligation.json": "22b471512c6ac6a6ff86bb65fbd4f1fec094208a1c99d338865dfee89c0cb3a0",
    SANDWICH_DIR / "MANIFEST.sha256": "056d73cd56818a18e2976707815f902cc433839ce69b192a88b118b7a9a5d707",
    SANDWICH_DIR / "results_two_sandwich_reduction.json": "1d94711066e002f9f827ce4ce392526d0cb46c5b5c0f5eaba584af571561d19c",
}
EXPECTED_ADDED = ["06", "14", "17", "25", "26", "36", "37"]
EXPECTED_VARIABLE = ["04", "12", "35", "67"]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def transpose(a):
    return tuple(zip(*a))


def matmul(a, b):
    bt = transpose(b)
    return tuple(tuple(sum(x * y for x, y in zip(row, col)) for col in bt) for row in a)


def add(a, b):
    return tuple(tuple(x + y for x, y in zip(ra, rb)) for ra, rb in zip(a, b))


def neg(a):
    return tuple(tuple(-x for x in row) for row in a)


def rank(a) -> int:
    rows = [list(map(Fraction, row)) for row in a]
    answer = 0
    for column in range(len(rows[0])):
        pivot = next((i for i in range(answer, len(rows)) if rows[i][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        scale = rows[answer][column]
        rows[answer] = [x / scale for x in rows[answer]]
        for i in range(len(rows)):
            if i != answer and rows[i][column]:
                scale = rows[i][column]
                rows[i] = [x - scale * y for x, y in zip(rows[i], rows[answer])]
        answer += 1
    return answer


def main() -> None:
    for path, expected in PINS.items():
        assert sha256(path) == expected, (path, sha256(path), expected)

    full = json.loads((FULL_DIR / "results_full_family_obligation.json").read_text())
    sandwich = json.loads((SANDWICH_DIR / "results_two_sandwich_reduction.json").read_text())
    representatives = full["six_full_family_representatives"]
    rep = representatives[3]
    assert rep["representative_id"] == 3
    assert rep["added"] == EXPECTED_ADDED
    assert rep["supported_perfect_matchings"] == 12
    assert rep["candidate_count"] == 10

    # Objective selection among the four untouched full-family representatives.
    open_reps = [representatives[i] for i in (1, 3, 4, 5)]
    assert {r["supported_perfect_matchings"] for r in open_reps} == {12}
    assert {len(s["supported_forbidden_terms"]) for r in open_reps for s in r["two_sandwich_stars"]} == {2}
    total_terms = {
        r["representative_id"]: sum(int(k) * v for k, v in r["full_x5_term_count_census"].items())
        for r in open_reps
    }
    assert total_terms == {1: 38718, 3: 37260, 4: 40176, 5: 41634}
    assert min(total_terms, key=total_terms.get) == 3

    guard = rep["guard"]
    assert guard["outside_site"] == 3
    assert guard["fixed_identity_substitution"] == [
        "A06*A37^T=0",
        "A37^T+A17*A36^T=0",
        "A26*A37^T+A36^T=0",
    ]
    star = next(
        item for item in rep["two_sandwich_stars"]
        if item["cap"] == "03" and item["star_center"] == 4 and item["common_block"] == "06"
    )
    assert star["factorization_up_to_output_permutation"] == "A06^T*K*[A35|A37]"
    assert star["P"] == "Row(A06^T)"
    assert star["Q"] == "ColSpan(A35,A37)"
    assert star["supported_forbidden_terms"] == [
        {"left_block": "06", "orientation": "switched", "response_pair": "56", "right_block": "35"},
        {"left_block": "06", "orientation": "direct", "response_pair": "67", "right_block": "37"},
    ]
    full_reduction = next(
        item for item in sandwich["reductions"]
        if item["added"] == EXPECTED_ADDED
        and item["nonzero_variable_blocks"] == EXPECTED_VARIABLE
        and item["cap"] == "03"
        and item["star_center"] == 4
        and item["common_block"] == "06"
    )
    assert full_reduction["common_side"] == "left"
    assert full_reduction["factorization"] == "U*K*[B1|B2]"
    assert full_reduction["partner_blocks"] == ["35", "37"]

    # Exact Q witness for the nonzero rank-one branch.  It is illustrative,
    # while the dimension argument below is uniform in all coefficients/ranks.
    z = Fraction(0)
    o = Fraction(1)
    eye = ((o, z, z), (z, o, z), (z, z, o))
    e00 = ((o, z, z), (z, z, z), (z, z, z))
    a37 = e00
    a26 = eye
    a17 = eye
    a06 = ((z, z, z), (z, o, z), (z, z, o))
    a36 = neg(e00)
    zero = ((z, z, z), (z, z, z), (z, z, z))
    assert matmul(a06, transpose(a37)) == zero
    assert add(transpose(a37), matmul(a17, transpose(a36))) == zero
    assert add(matmul(a26, transpose(a37)), transpose(a36)) == zero
    assert rank(a37) == 1 and rank(a06) == 2
    k = e00
    assert matmul(matmul(transpose(a06), k), eye) == zero
    assert matmul(matmul(transpose(a06), k), a37) == zero
    assert sum(k[i][i] for i in range(3)) == 1

    # Negative control for the load-bearing diagonal condition: the same guard
    # allows P=span(e0) and Q containing e0.  Then E00 is in P tensor Q even
    # though I is not, so pairing activity does not imply K00 activity.
    e11 = ((z, z, z), (z, o, z), (z, z, z))
    assert matmul(e00, transpose(e11)) == zero
    assert add(transpose(e11), matmul(eye, transpose(neg(e11)))) == zero
    assert add(matmul(eye, transpose(e11)), transpose(neg(e11))) == zero
    assert matmul(matmul(transpose(e00), e00), e00) == e00

    result = {
        "schema": "KRENN_X5_SEVEN_BLOCK_REP3_LOW_RANK_CARRIER_V1",
        "status": "PAIRING_ONLY_INCOMPLETE_NONZERO_RANKS",
        "representative_id": 3,
        "support": {
            "fixed": ["03", "16", "27", "45"],
            "variable_nonzero": EXPECTED_VARIABLE,
            "added_nonzero": EXPECTED_ADDED,
        },
        "selection": {
            "open_representatives_compared": [1, 3, 4, 5],
            "supported_perfect_matchings": {str(i): representatives[i]["supported_perfect_matchings"] for i in (1, 3, 4, 5)},
            "minimum_star_terms": {str(i): min(len(s["supported_forbidden_terms"]) for s in representatives[i]["two_sandwich_stars"]) for i in (1, 3, 4, 5)},
            "full_x5_total_term_tiebreak": {str(k): v for k, v in total_terms.items()},
            "selected": 3,
        },
        "exact_guard": guard["fixed_identity_substitution"],
        "carrier": star,
        "proof": {
            "rank_zero": [
                "A37=0 and A26*A37^T+A36^T=0 force A36=0.",
                "Every cap67/triangle012 response term contains A36 or A37, so L67=0.",
                "A67 is nonzero on the full-family stratum, hence its Frobenius functional is live on ker(L67)=Mat_3 and cap67 is active.",
            ],
            "nonzero_rank_pairing_only": [
                "Write A37=u*v^T with u,v nonzero. The guard A06*A37^T=0 is A06*v*u^T=0, hence A06*v=0.",
                "Thus P=Row(A06^T)=Col(A06) is proper.",
                "The cap03/star4 response row space is P tensor ColSpan(A35,A37). Since A03=I, the cap pairing is live.",
                "This does not make all three Kii functionals live: each additionally needs not(e_i in P and e_i in Q).",
            ],
            "all_nonzero_ranks_pairing_scope": "The same argument proves pairing activity for ranks 1, 2, and 3, but no all-rank carrier closure.",
            "missing_diagonal_lemma": "For every i=0,1,2 prove not(e_i in Col(A06) and e_i in ColSpan(A35,A37)).",
            "field": "characteristic zero (indeed any field)",
        },
        "exact_local_countermodel_to_closure": {"A37": "E11", "A36": "-E11", "A06": "E00", "A17": "I", "A26": "I", "A35": "E00", "pairing_live": True, "K00_functional_in_response_rowspace": "E00=A06^T*E00*A35"},
        "exact_Q_rank1_witness": {
            "A37": "E00",
            "A36": "-E00",
            "A26": "I",
            "A17": "I",
            "A06": "diag(0,1,1)",
            "kernel_K": "E00",
            "carrier_responses": "A06^T*K*A35=A06^T*K*A37=0 for A35=I",
            "cap03_pairing": "trace(K)=1",
        },
        "pins": {str(path.relative_to(ROOT)): digest for path, digest in PINS.items()},
        "scope": {
            "rep3_closed": False,
            "rank_zero_closed": True,
            "nonzero_ranks_pairing_only": True,
            "rep0_transport_used": False,
            "rep2_transport_used": False,
            "other_representatives_claimed": [],
            "full_X5_equations_used": False,
        },
    }
    atomic_json(HERE / "results_rep3_low_rank_carrier.json", result)
    print(json.dumps({"status": result["status"], "representative": 3, "all_ranks": False}, sort_keys=True))


if __name__ == "__main__":
    main()
