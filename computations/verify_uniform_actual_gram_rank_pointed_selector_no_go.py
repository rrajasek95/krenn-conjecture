#!/usr/bin/env python3
"""Rank the actual insertion Gram packet and exhibit its pointed cokernel.

The literal occurrence set at order h+1 consists of an ordered endpoint
pair (p,s) and a perfect matching F of the remaining 2h sites.  The actual
Gram entry is

    |F intersect R| + C((p,s),(p',s')),

with the endpoint constants pinned in the uniform projector audit.  The
matrix factors through endpoint indicators and physical-edge incidence.
This checker verifies the resulting rank formula and an explicit uniform
eight-matching covector which kills the whole Gram image but detects one
marked occurrence.
"""

from __future__ import annotations

import argparse
import json
from hashlib import sha256
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = (
    "c668d82dddfdabc2bf09d9fbf9610271924ade2eace804e9c97deb3784fb2b37"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted(((first, second),) + tail))


def occurrences(h: int):
    n = 2 * h + 2
    answer = []
    for p in range(n):
        for s in range(n):
            if p == s:
                continue
            residual = tuple(site for site in range(n) if site not in (p, s))
            for matching in perfect_matchings(residual):
                answer.append((p, s, frozenset(matching)))
    return tuple(answer)


def rank_mod(rows, prime: int = 1_000_003) -> int:
    work = [[value % prime for value in row] for row in rows]
    if not work:
        return 0
    height = len(work)
    width = len(work[0])
    pivot_row = 0
    for column in range(width):
        pivot = next((row for row in range(pivot_row, height)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        inverse = pow(work[pivot_row][column], prime - 2, prime)
        work[pivot_row] = [value * inverse % prime
                           for value in work[pivot_row]]
        for row in range(height):
            if row == pivot_row or not work[row][column]:
                continue
            scalar = work[row][column]
            work[row] = [
                (left - scalar * right) % prime
                for left, right in zip(work[row], work[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == height:
            break
    return pivot_row


def feature_rank_audit(h: int) -> dict[str, int]:
    n = 2 * h + 2
    occ = occurrences(h)
    endpoint_pairs = tuple((p, s) for p in range(n) for s in range(n)
                           if p != s)
    edges = tuple(combinations(range(n), 2))

    # Transpose of the feature matrix: endpoint-fibre indicators followed
    # by residual-edge incidence rows.  Its rational rank is at least its
    # rank modulo the good prime, while the exact additive-weight relations
    # give the matching upper bound used in the note.
    feature_rows = []
    for endpoint in endpoint_pairs:
        feature_rows.append(tuple(int((p, s) == endpoint)
                                  for p, s, _matching in occ))
    for edge in edges:
        feature_rows.append(tuple(int(edge in matching)
                                  for _p, _s, matching in occ))

    actual_rank = rank_mod(feature_rows)
    expected_rank = n * (3 * n - 5) // 2
    require(actual_rank == expected_rank,
            (h, actual_rank, expected_rank))
    return {
        "h": h,
        "sites": n,
        "occurrences": len(occ),
        "endpoint_features": len(endpoint_pairs),
        "edge_features": len(edges),
        "feature_relations": n,
        "actual_gram_rank": actual_rank,
        "actual_gram_nullity": len(occ) - actual_rank,
    }


# An integral zero-edge-marginal relation on the fifteen matchings of K6.
# The first matching is the marked occurrence and has coefficient -1.
K6_RELATION = {
    ((0, 1), (2, 3), (4, 5)): -1,
    ((0, 1), (2, 5), (3, 4)): 1,
    ((0, 2), (1, 4), (3, 5)): 1,
    ((0, 2), (1, 5), (3, 4)): -1,
    ((0, 3), (1, 2), (4, 5)): 1,
    ((0, 3), (1, 4), (2, 5)): -1,
    ((0, 4), (1, 2), (3, 5)): -1,
    ((0, 4), (1, 5), (2, 3)): 1,
}


def endpoint_constant(h: int, marked, other) -> int:
    pf, sf = marked
    p, s = other
    if (p, s) == (pf, sf):
        return 4 * h * h + 4 * h
    if (p == pf) ^ (s == sf):
        return 2 * h - 1
    return 0


def pointed_cokernel_audit(h: int) -> dict[str, object]:
    require(h >= 3, h)
    n = 2 * h + 2
    marked_endpoints = (n - 2, n - 1)
    extra_vertices = tuple(range(6, n - 2))
    require(len(extra_vertices) % 2 == 0, extra_vertices)
    fixed_tail = tuple((extra_vertices[index], extra_vertices[index + 1])
                       for index in range(0, len(extra_vertices), 2))

    relation = {}
    for core, coefficient in K6_RELATION.items():
        matching = frozenset(tuple(sorted(core + fixed_tail)))
        relation[matching] = coefficient

    require(sum(relation.values()) == 0, relation)
    for edge in combinations(range(n), 2):
        marginal = sum(coefficient for matching, coefficient in relation.items()
                       if edge in matching)
        require(marginal == 0, (h, edge, marginal))

    marked_matching = frozenset(
        tuple(sorted(((0, 1), (2, 3), (4, 5)) + fixed_tail))
    )
    require(relation[marked_matching] == -1, marked_matching)

    # Directly annihilate every literal Gram column, including columns in
    # other endpoint fibres.  The endpoint contribution is constant across
    # the eight relation rows and the intersection contribution has zero
    # edge marginals.
    all_occurrences = occurrences(h)
    for p, s, other_matching in all_occurrences:
        pairing = 0
        for matching, coefficient in relation.items():
            gram = len(matching & other_matching) + endpoint_constant(
                h, marked_endpoints, (p, s)
            )
            pairing += coefficient * gram
        require(pairing == 0,
                (h, p, s, tuple(sorted(other_matching)), pairing))

    return {
        "h": h,
        "marked_endpoints": list(marked_endpoints),
        "fixed_spectator_tail": [list(edge) for edge in fixed_tail],
        "relation_support": len(relation),
        "coefficient_sum": sum(relation.values()),
        "all_edge_marginals": 0,
        "gram_columns_annihilated": len(all_occurrences),
        "value_on_marked_occurrence": relation[marked_matching],
    }


def audit() -> tuple[dict[str, object], str]:
    ranks = [feature_rank_audit(h) for h in (2, 3, 4)]
    cokernels = [pointed_cokernel_audit(h) for h in (3, 4)]
    ledger = {
        "rank_formula": "n*(3*n-5)/2, n=2h+2",
        "rank_derivation": {
            "endpoint_fibre_dimension": "n*(n-1)",
            "physical_edge_dimension": "n*(n-1)/2",
            "intersection_dimension": "n additive vertex weights",
            "endpoint_gram_positive_definite": (
                "c*I+b*(first_endpoint_blocks+second_endpoint_blocks), c>0"
            ),
        },
        "bounded_exact_rank_checks": ranks,
        "uniform_pointed_cokernel_embedding": cokernels,
        "conclusion": (
            "The actual insertion Gram correspondence reaches only endpoint "
            "aggregates plus edge-additive matching functions.  For every "
            "h>=3 an embedded K6 eight-matching covector kills its full image "
            "and detects a marked occurrence, so the nonzero projector "
            "composite cannot construct the pointed occurrence selector."
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                (digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("all", "rank", "pointed"),
                        default="all")
    args = parser.parse_args()
    ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    if args.mode in ("all", "rank"):
        print("actual Gram ranks h=2,3,4:",
              [row["actual_gram_rank"]
               for row in ledger["bounded_exact_rank_checks"]])
    if args.mode in ("all", "pointed"):
        print("uniform h>=3 pointed selector: OUTSIDE GRAM IMAGE")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
