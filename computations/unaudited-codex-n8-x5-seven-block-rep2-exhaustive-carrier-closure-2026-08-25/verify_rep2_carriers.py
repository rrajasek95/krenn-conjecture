#!/usr/bin/env python3
"""Exhaustive 90-carrier census and exact closure of full-family rep2."""

from __future__ import annotations

import collections
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
ADDED = frozenset(((0, 6), (1, 4), (1, 7), (2, 3), (2, 6), (5, 6), (5, 7)))
SUPPORT = FIXED | VARIABLE | ADDED


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def label(edge):
    return f"{edge[0]}{edge[1]}"


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


def star_terms(cap, center):
    p, q = cap
    residual = tuple(site for site in range(8) if site not in cap)
    terms = []
    for a, b in itertools.combinations(residual, 2):
        if center in (a, b):
            continue
        pa, qb = tuple(sorted((p, a))), tuple(sorted((q, b)))
        if pa in SUPPORT and qb in SUPPORT:
            terms.append({
                "left_block": label(pa), "orientation": "direct",
                "response_pair": f"{a}{b}", "right_block": label(qb),
            })
        pb, qa = tuple(sorted((p, b))), tuple(sorted((q, a)))
        if pb in SUPPORT and qa in SUPPORT:
            terms.append({
                "left_block": label(pb), "orientation": "switched",
                "response_pair": f"{a}{b}", "right_block": label(qa),
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


def rank(a):
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


def literal_factor_entries():
    entries = []
    for response, right, transposed in (("26", "A23", True), ("56", "A35", False)):
        for i, j in itertools.product(range(3), repeat=2):
            terms = []
            for x, y in itertools.product(range(3), repeat=2):
                right_entry = f"{right}[{j},{y}]" if transposed else f"{right}[{y},{j}]"
                terms.append(f"A06[{x},{i}]*K[{x},{y}]*{right_entry}")
            entries.append({"response": response, "entry": [i, j], "polynomial": "+".join(terms)})
    return entries


def atomic_json(path: Path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def main():
    for path, expected in PINS.items():
        assert sha256(path) == expected, (path, sha256(path), expected)
    full = json.loads((FULL_DIR / "results_full_family_obligation.json").read_text())
    sandwich = json.loads((SANDWICH_DIR / "results_two_sandwich_reduction.json").read_text())
    rep = full["six_full_family_representatives"][2]
    assert rep["representative_id"] == 2
    assert rep["added"] == ["06", "14", "17", "23", "26", "56", "57"]

    all_matchings = tuple(sorted(matchings(tuple(range(8)))))
    supported = tuple(matching for matching in all_matchings if set(matching) <= SUPPORT)
    assert len(all_matchings) == 105 and len(supported) == 13

    carriers = []
    histogram = collections.Counter()
    for cap in sorted(SUPPORT):
        for center in range(8):
            if center in cap:
                continue
            terms = star_terms(cap, center)
            histogram[len(terms)] += 1
            carriers.append({"cap": label(cap), "star_center": center, "term_count": len(terms), "terms": terms})
    assert len(carriers) == len(SUPPORT) * 6 == 90
    assert dict(sorted(histogram.items())) == {2: 8, 3: 14, 4: 28, 5: 8, 6: 12, 7: 12, 8: 4, 9: 2, 10: 2}
    two_term = [item for item in carriers if item["term_count"] == 2]
    assert len(two_term) == 8

    expanded = rep["two_sandwich_stars"]
    assert len(expanded) == 8
    for candidate in two_term:
        matches = [
            item for item in expanded
            if item["cap"] == candidate["cap"]
            and item["star_center"] == candidate["star_center"]
            and item["supported_forbidden_terms"] == candidate["terms"]
        ]
        assert len(matches) == 1
        candidate["expanded_ledger_factor"] = matches[0]["factorization_up_to_output_permutation"]
        candidate["P"] = matches[0]["P"]
        candidate["Q"] = matches[0]["Q"]
        candidate["common_block"] = matches[0]["common_block"]

    target = next(item for item in two_term if item["cap"] == "03" and item["star_center"] == 4)
    assert target == {
        "cap": "03",
        "star_center": 4,
        "term_count": 2,
        "terms": [
            {"left_block": "06", "orientation": "switched", "response_pair": "26", "right_block": "23"},
            {"left_block": "06", "orientation": "switched", "response_pair": "56", "right_block": "35"},
        ],
        "expanded_ledger_factor": "A06^T*K*[A23^T|A35]",
        "P": "Row(A06^T)",
        "Q": "ColSpan(A23^T,A35)",
        "common_block": "06",
    }
    reduction = next(
        item for item in sandwich["reductions"]
        if item["added"] == rep["added"] and item["nonzero_variable_blocks"] == ["04", "12", "35", "67"]
    )
    assert reduction["cap"] == "03" and reduction["star_center"] == 2 and reduction["common_block"] == "35"
    assert not (reduction["star_center"] == 4 and reduction["common_block"] == "06")

    literal_entries = literal_factor_entries()
    assert len(literal_entries) == 18
    literal_sha = hashlib.sha256(json.dumps(literal_entries, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

    # Exact rational rank-one replay of both source-labelled response matrices.
    z, o = Fraction(0), Fraction(1)
    eye = ((o, z, z), (z, o, z), (z, z, o))
    e00 = ((o, z, z), (z, z, z), (z, z, z))
    zero = ((z, z, z), (z, z, z), (z, z, z))
    a57, a56 = e00, neg(e00)
    a06 = ((z, z, z), (z, o, z), (z, z, o))
    assert matmul(a06, transpose(a57)) == zero
    assert add(transpose(a57), matmul(eye, transpose(a56))) == zero
    assert add(matmul(eye, transpose(a57)), transpose(a56)) == zero
    assert rank(a57) == 1 and rank(a06) == 2
    k = e00
    assert matmul(matmul(transpose(a06), k), transpose(eye)) == zero
    assert matmul(matmul(transpose(a06), k), eye) == zero
    assert sum(k[i][i] for i in range(3)) == 1

    result = {
        "schema": "KRENN_X5_SEVEN_BLOCK_REP2_EXHAUSTIVE_CARRIER_V1",
        "status": "PAIRING_ONLY_INCOMPLETE_REP2_NONZERO_RANKS",
        "representative_id": 2,
        "support": {"fixed": ["03", "16", "27", "45"], "variable_nonzero": ["04", "12", "35", "67"], "added_nonzero": rep["added"]},
        "exhaustive_census": {
            "perfect_matchings_total": 105,
            "perfect_matchings_supported": 13,
            "supported_caps": len(SUPPORT),
            "centers_per_cap": 6,
            "carrier_configurations": len(carriers),
            "term_count_histogram": {str(k): v for k, v in sorted(histogram.items())},
            "minimum_term_count": 2,
            "minimum_carriers": two_term,
        },
        "frozen_best_record_obstruction": {
            "record": reduction,
            "why_not_used": "its P=RowSpan(A04^T,A06^T) is not forced proper merely because A06 is singular",
        },
        "closing_carrier": target,
        "literal_source_factorization": {
            "response_matrices": {"R26": "A06^T*K*A23^T", "R56": "A06^T*K*A35"},
            "distinct_response_outputs": ["26", "56"],
            "coordinate_expansions": literal_entries,
            "canonical_sha256": literal_sha,
        },
        "exact_guard": ["A06*A57^T=0", "A57^T+A17*A56^T=0", "A26*A57^T+A56^T=0"],
        "proof": {
            "zero_A57": ["A57=0 forces A56=0 by A26*A57^T+A56^T=0.", "Then the full cap67 response map L67 is zero; nonzero full-family A67 makes cap67/triangle012 active."],
            "nonzero_A57_pairing_only": ["A06*A57^T=0 with A57 nonzero gives a nonzero vector in ker(A06), hence P=Row(A06^T)=Col(A06) is proper.", "The cap03/star4 response row space is P tensor ColSpan(A23^T,A35).", "Since fixed A03=I has full column space, its pairing is live, but each Kii additionally requires not(e_i in P and e_i in Q)."],
            "closed_rank_scope": [0],
            "pairing_only_rank_scope": [1, 2, 3],
            "missing_diagonal_lemma": "For every i=0,1,2 prove not(e_i in Col(A06) and e_i in ColSpan(A23^T,A35)).",
        },
        "exact_local_countermodel_to_nonzero_rank_closure": {"A57": "E11", "A56": "-E11", "A06": "E00", "A17": "I", "A26": "I", "A23": "E00", "A35": "E00", "pairing_live": True, "K00_functional_in_response_rowspace": "E00=A06^T*E00*A35"},
        "exact_Q_rank1_local_replay": {"A57": "E00", "A56": "-E00", "A06": "diag(0,1,1)", "A17": "I", "A26": "I", "A23": "I", "A35": "I", "kernel_K": "E00", "cap03_pairing": "trace(K)=1"},
        "pins": {str(path.relative_to(ROOT)): digest for path, digest in PINS.items()},
        "scope": {"rep2_full_family_closed": False, "rank_zero_closed": True, "nonzero_ranks_pairing_only": True, "groebner_used": False, "transport_used": False, "non_full_family_claimed": False},
    }
    atomic_json(HERE / "results_rep2_exhaustive_carrier.json", result)
    print(json.dumps({"status": result["status"], "carriers": 90, "two_term": 8}, sort_keys=True))


if __name__ == "__main__":
    main()
