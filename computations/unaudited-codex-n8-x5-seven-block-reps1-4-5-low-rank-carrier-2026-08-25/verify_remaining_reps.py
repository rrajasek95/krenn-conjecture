#!/usr/bin/env python3
"""Independent low-rank/carrier closures for full-family reps 1, 4, and 5."""

from __future__ import annotations

import hashlib
import itertools
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
FIXED = frozenset(((0, 3), (1, 6), (2, 7), (4, 5)))
VARIABLE = frozenset(((0, 4), (1, 2), (3, 5), (6, 7)))
EXPECTED = {
    1: {
        "added": ["06", "13", "17", "25", "26", "46", "47"],
        "outside": 4,
        "partner_blocks": ["13", "35"],
        "factor": "A06^T*K*[A13^T|A35]",
        "total_terms": 38718,
        "ledger_best": {"cap": "03", "star_center": 1, "common_block": "35", "common_side": "right", "partner_blocks": ["04", "06"]},
        "terms": [
            {"left_block": "06", "orientation": "switched", "response_pair": "16", "right_block": "13"},
            {"left_block": "06", "orientation": "switched", "response_pair": "56", "right_block": "35"},
        ],
    },
    4: {
        "added": ["06", "15", "17", "23", "26", "46", "47"],
        "outside": 4,
        "partner_blocks": ["23", "35"],
        "factor": "A06^T*K*[A23^T|A35]",
        "total_terms": 40176,
        "ledger_best": {"cap": "03", "star_center": 2, "common_block": "35", "common_side": "right", "partner_blocks": ["04", "06"]},
        "terms": [
            {"left_block": "06", "orientation": "switched", "response_pair": "26", "right_block": "23"},
            {"left_block": "06", "orientation": "switched", "response_pair": "56", "right_block": "35"},
        ],
    },
    5: {
        "added": ["06", "15", "17", "24", "26", "36", "37"],
        "outside": 3,
        "partner_blocks": ["35", "37"],
        "factor": "A06^T*K*[A35|A37]",
        "total_terms": 41634,
        "ledger_best": {"cap": "03", "star_center": 4, "common_block": "06", "common_side": "left", "partner_blocks": ["35", "37"]},
        "terms": [
            {"left_block": "06", "orientation": "switched", "response_pair": "56", "right_block": "35"},
            {"left_block": "06", "orientation": "direct", "response_pair": "67", "right_block": "37"},
        ],
    },
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def edge(label: str) -> tuple[int, int]:
    assert len(label) == 2 and label[0] < label[1]
    return int(label[0]), int(label[1])


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


def supported_star_terms(support, cap=(0, 3), center=4):
    p, q = cap
    residual = tuple(site for site in range(8) if site not in cap)
    terms = []
    for a, b in itertools.combinations(residual, 2):
        if center in (a, b):
            continue
        pa, qb = tuple(sorted((p, a))), tuple(sorted((q, b)))
        if pa in support and qb in support:
            terms.append({
                "left_block": f"{pa[0]}{pa[1]}",
                "orientation": "direct",
                "response_pair": f"{a}{b}",
                "right_block": f"{qb[0]}{qb[1]}",
            })
        pb, qa = tuple(sorted((p, b))), tuple(sorted((q, a)))
        if pb in support and qa in support:
            terms.append({
                "left_block": f"{pb[0]}{pb[1]}",
                "orientation": "switched",
                "response_pair": f"{a}{b}",
                "right_block": f"{qa[0]}{qa[1]}",
            })
    return terms


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
        divisor = rows[answer][column]
        rows[answer] = [x / divisor for x in rows[answer]]
        for i in range(len(rows)):
            if i != answer and rows[i][column]:
                factor = rows[i][column]
                rows[i] = [x - factor * y for x, y in zip(rows[i], rows[answer])]
        answer += 1
    return answer


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def main() -> None:
    for path, expected in PINS.items():
        assert sha256(path) == expected, (path, sha256(path), expected)
    full = json.loads((FULL_DIR / "results_full_family_obligation.json").read_text())
    sandwich = json.loads((SANDWICH_DIR / "results_two_sandwich_reduction.json").read_text())
    representatives = {item["representative_id"]: item for item in full["six_full_family_representatives"]}
    all_matchings = tuple(sorted(matchings(tuple(range(8)))))
    assert len(all_matchings) == 105

    records = []
    # Rep5 is first because its frozen 64-to-13 best record already has the
    # guard-controlled common A06 factor.  Reps1/4 are then treated separately:
    # their frozen best record does not suffice, but independent source
    # enumeration supplies another exact two-term common-A06 carrier.
    for representative_id in (5, 1, 4):
        expected = EXPECTED[representative_id]
        rep = representatives[representative_id]
        assert rep["added"] == expected["added"]
        support = FIXED | VARIABLE | {edge(label) for label in expected["added"]}
        supported = tuple(matching for matching in all_matchings if set(matching) <= support)
        assert len(supported) == rep["supported_perfect_matchings"] == 12
        terms = supported_star_terms(support)
        assert terms == expected["terms"]
        total_terms = sum(int(k) * v for k, v in rep["full_x5_term_count_census"].items())
        assert total_terms == expected["total_terms"]

        r = expected["outside"]
        outside6, outside7 = f"{r}6", f"{r}7"
        guard = rep["guard"]
        exact_guard = [
            f"A06*A{outside7}^T=0",
            f"A{outside7}^T+A17*A{outside6}^T=0",
            f"A26*A{outside7}^T+A{outside6}^T=0",
        ]
        assert guard["outside_site"] == r
        assert guard["fixed_identity_substitution"] == exact_guard
        star = next(
            item for item in rep["two_sandwich_stars"]
            if item["cap"] == "03" and item["star_center"] == 4 and item["common_block"] == "06"
        )
        assert star["factorization_up_to_output_permutation"] == expected["factor"]
        assert star["P"] == "Row(A06^T)"
        assert star["partner_blocks"] == expected["partner_blocks"]
        assert star["supported_forbidden_terms"] == terms
        reductions = [
            item for item in sandwich["reductions"]
            if item["added"] == expected["added"]
            and item["nonzero_variable_blocks"] == ["04", "12", "35", "67"]
        ]
        assert len(reductions) == 1
        reduction = reductions[0]
        assert reduction["factorization"] == ("U*K*[B1|B2]" if reduction["common_side"] == "left" else "[U1;U2]*K*B")
        assert {key: reduction[key] for key in expected["ledger_best"]} == expected["ledger_best"]
        ledger_best_suffices = reduction["common_block"] == "06" and reduction["common_side"] == "left"
        assert ledger_best_suffices == (representative_id == 5)
        if ledger_best_suffices:
            assert reduction["partner_blocks"] == expected["partner_blocks"]
            assert reduction["supported_forbidden_terms"] == terms

        # A literal exact-Q rank-one local replay for this distinct support.
        z, o = Fraction(0), Fraction(1)
        eye = ((o, z, z), (z, o, z), (z, z, o))
        e00 = ((o, z, z), (z, z, z), (z, z, z))
        ar7, ar6 = e00, neg(e00)
        a06 = ((z, z, z), (z, o, z), (z, z, o))
        zero = ((z, z, z), (z, z, z), (z, z, z))
        assert matmul(a06, transpose(ar7)) == zero
        assert add(transpose(ar7), matmul(eye, transpose(ar6))) == zero
        assert add(matmul(eye, transpose(ar7)), transpose(ar6)) == zero
        assert rank(ar7) == 1 and rank(a06) == 2
        assert matmul(transpose(a06), e00) == zero
        assert sum(e00[i][i] for i in range(3)) == 1

        records.append({
            "representative_id": representative_id,
            "support": {"fixed": ["03", "16", "27", "45"], "variable_nonzero": ["04", "12", "35", "67"], "added_nonzero": expected["added"]},
            "independent_regeneration": {
                "all_perfect_matchings": len(all_matchings),
                "supported_perfect_matchings": len(supported),
                "carrier_terms": terms,
                "frozen_64_to_13_best_record": reduction,
                "best_record_directly_supports_guard_dichotomy": ledger_best_suffices,
                "best_record_obstruction": None if ledger_best_suffices else "P=RowSpan(A04^T,A06^T); guard makes A06 singular but does not force this larger P proper",
                "source_labelled_factorization": expected["factor"],
                "full_x5_total_term_load": total_terms,
            },
            "exact_guard": exact_guard,
            "outside_pair": outside7,
            "companion_pair": outside6,
            "carrier": star,
            "proof": {
                "zero_outside_factor": f"A{outside7}=0 forces A{outside6}=0 by the third guard equation; then L67=0 and nonzero A67 makes cap67/triangle012 active.",
                "nonzero_outside_factor": f"A{outside7}!=0 and A06*A{outside7}^T=0 force ker(A06)!=0, so P=Row(A06^T)=Col(A06) is proper.",
                "identity_cap_pairing_only": "The cap03/star4 row space is P tensor Q. Since A03=I, this proves the cap pairing live, but not all three Kii functionals.",
                "missing_diagonal_lemma": "For every i=0,1,2 prove not(e_i in P and e_i in Q).",
                "closed_rank_scope": [0],
                "pairing_only_rank_scope": [1, 2, 3],
            },
            "exact_Q_rank1_local_replay": {f"A{outside7}": "E00", f"A{outside6}": "-E00", "A06": "diag(0,1,1)", "A17": "I", "A26": "I", "kernel_K": "E00", "cap03_pairing": "trace(K)=1"},
            "exact_local_countermodel_to_nonzero_rank_closure": {f"A{outside7}": "E11", f"A{outside6}": "-E11", "A06": "E00", "A17": "I", "A26": "I", "partner_block_for_e0": "E00", "K00_functional_in_response_rowspace": True},
        })

    result = {
        "schema": "KRENN_X5_SEVEN_BLOCK_REPS1_4_5_LOW_RANK_CARRIER_V1",
        "status": "PAIRING_ONLY_INCOMPLETE_REPS1_4_5_NONZERO_RANKS",
        "sequential_order": [5, 1, 4],
        "selection_basis": {
            "all_supported_matchings": 12,
            "all_minimum_carrier_terms": 2,
            "term_loads": {"1": 38718, "4": 40176, "5": 41634},
            "first_direct_frozen_best_record_with_guard_controlled_common_factor": 5,
        },
        "representatives": records,
        "pins": {str(path.relative_to(ROOT)): digest for path, digest in PINS.items()},
        "scope": {
            "closed_representatives": [],
            "rank_zero_closed_representatives": [1, 4, 5],
            "nonzero_ranks_pairing_only": [1, 4, 5],
            "transport_from_rep0_rep2_rep3_used": False,
            "each_support_and_carrier_regenerated": True,
            "non_full_family_claimed": False,
            "full_x5_equations_used": False,
        },
    }
    atomic_json(HERE / "results_remaining_reps_low_rank_carrier.json", result)
    print(json.dumps({"status": result["status"], "closed": [], "rank_zero_closed": [1, 4, 5]}, sort_keys=True))


if __name__ == "__main__":
    main()
