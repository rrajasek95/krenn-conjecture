#!/usr/bin/env python3
"""Reduce equal-partition zero-Fitting two-cycles to one diagonal C4 switch.

The spectator factorization theorem writes a literal zero-Fitting rectangle

    A=G*U, B=G*V, C=H*U, D=H*V.

The two full output words agree on the alternating core U,V and can differ
only on the spectator sites supporting G,H.  If their colour multiplicity
partitions are equal, enumerate those spectator decorations at N=8.

* a six-site core has two spectator sites; every distinct equal-partition
  pair is a transposition and its unique spectator cell is off-diagonal;
* an eight-site core has no spectator sites, so two literal rows cannot be
  distinct;
* a four-site core has four spectator sites.  Unless one spectator factor
  contains an off-diagonal cell, the two words have type 2+2.  Either G,H
  are two different same-colour pairings (one physical C4), or they have
  the same skeleton and the two diagonal colours exchange between its
  edges.  Every other K4 matching is off-diagonal in both words.

Thus the only equal-partition two-row geometry not already entering the
bidirectional off-diagonal fan theorem is one diagonal 2+2 switch family.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COLOURS = tuple(range(3))
PINS = {
    "computations/verify_oo_zero_fitting_spectator_factorization.py":
        "bd6899602e428b2037372d22efe0ec5552b220ed71bfff1a7b1a81718dea6049",
    "notes/oo-zero-fitting-spectator-factorization.md":
        "5500856374ee4cfc4c369d28b0c2e43a3bf8938f55d3570e08da0d145dcd3b94",
    "computations/verify_uniform_bidirectional_private_site_fan_rank_boundary.py":
        "c4e175ca053cd98e788cca1a38a1851e708e7e47a9ea5745ef4ac6e303ddfd40",
    "notes/uniform-bidirectional-private-site-fan-rank-boundary.md":
        "7d0f04d22fe11d1ba797a29507fd43915dc98e9d89bdc4085f1c8561deaa1402",
    "computations/verify_uniform_bidirectional_five_lock_relative_homotopy_boundary.py":
        "aeed58d596f931602dcb77b44aa3bd11a27b8e2d26435cc328b325ce91b0e1bb",
    "notes/uniform-bidirectional-five-lock-relative-homotopy-boundary.md":
        "c9ce579dcbd6333060527872425c63cfb45ab3fbbc40401c345360ceeb767ad1",
}
EXPECTED_LEDGER_SHA256 = (
    "21c0911170844030c7585dae964e5a5456685a87b65911b5e0ed54f508293d62"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        return ((),)
    first = vertices[0]
    output = []
    for second in vertices[1:]:
        rest = tuple(site for site in vertices
                     if site not in (first, second))
        for tail in perfect_matchings(rest):
            output.append((tuple(sorted((first, second))),) + tail)
    return tuple(output)


def same_colour_matching(word, matching):
    return all(word[left] == word[right] for left, right in matching)


def word_type(word):
    return tuple(sorted(Counter(word).values(), reverse=True))


def third_k4_matching(first, second):
    matchings = perfect_matchings(range(4))
    remaining = tuple(item for item in matchings
                      if item not in (first, second))
    require(len(remaining) == 1,
            ("two distinct K4 matchings lost their third route", first, second))
    return remaining[0]


def audit_spectator_size(size):
    words = tuple(product(COLOURS, repeat=size))
    matchings = perfect_matchings(range(size))
    counts = Counter()
    diagonal_subtypes = Counter()
    type_counts = Counter()
    examples = {}
    for left in words:
        for right in words:
            if left == right or Counter(left) != Counter(right):
                continue
            for G in matchings:
                for H in matchings:
                    diagonal = (same_colour_matching(left, G)
                                and same_colour_matching(right, H))
                    branch = ("all_diagonal" if diagonal
                              else "contains_offdiagonal_spectator_cell")
                    counts[branch] += 1
                    type_counts[(branch, word_type(left))] += 1
                    examples.setdefault(branch, {
                        "left_word": list(left),
                        "right_word": list(right),
                        "G": [list(edge) for edge in G],
                        "H": [list(edge) for edge in H],
                    })

                    if size == 2:
                        require(not diagonal,
                                "a distinct two-site equal-multiset pair became diagonal")
                        require(right == left[::-1] and left[0] != left[1],
                                "two-site branch stopped being a colour transposition")

                    if size == 4 and diagonal:
                        require(word_type(left) == (2, 2),
                                "all-diagonal four-site branch is not 2+2")
                        if G == H:
                            diagonal_subtypes["same_skeleton_colour_swap"] += 1
                            for K in matchings:
                                if K == G:
                                    continue
                                require(not same_colour_matching(left, K)
                                        and not same_colour_matching(right, K),
                                        "same-skeleton alternative stopped being off-diagonal")
                        else:
                            diagonal_subtypes["physical_C4_switch"] += 1
                            K = third_k4_matching(G, H)
                            require(not same_colour_matching(left, K)
                                    and not same_colour_matching(right, K),
                                    "third K4 route stopped being off-diagonal in both words")
                            require(len(set(G) ^ set(H)) == 4,
                                    "the two diagonal pairings stopped forming one C4")

    return {
        "spectator_sites": size,
        "perfect_matchings": len(matchings),
        "distinct_equal_multiset_decorated_pairs": sum(counts.values()),
        "branches": dict(sorted(counts.items())),
        "diagonal_subtypes": dict(sorted(diagonal_subtypes.items())),
        "word_types": [
            {"branch": branch, "word_type": list(kind), "count": count}
            for (branch, kind), count in sorted(type_counts.items())
        ],
        "examples": examples,
    }


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    core8 = audit_spectator_size(0)
    core6 = audit_spectator_size(2)
    core4 = audit_spectator_size(4)
    require(core8["branches"] == {},
            ("eight-site literal core gained distinct rows", core8))
    require(core6["branches"] == {
        "contains_offdiagonal_spectator_cell": 6,
    }, ("six-site equal-partition split changed", core6))
    require(core4["branches"] == {
        "all_diagonal": 90,
        "contains_offdiagonal_spectator_cell": 4932,
    }, ("four-site equal-partition split changed", core4))
    require(core4["diagonal_subtypes"] == {
        "physical_C4_switch": 72,
        "same_skeleton_colour_swap": 18,
    }, ("four-site diagonal subtype split changed", core4))

    return {
        "theorem": "equal-partition zero-holonomy two-cycle reduction",
        "factorization_input": (
            "AD=BC gives A=G*U,B=G*V,C=H*U,D=H*V; the two literal "
            "source words agree on the alternating core and differ only on "
            "the spectator sites"
        ),
        "N8_core_cases": {
            "core8_spectator0": core8,
            "core6_spectator2": core6,
            "core4_spectator4": core4,
        },
        "offdiagonal_route": (
            "every nonzero off-diagonal spectator cell enters the pinned "
            "bidirectional private-site fan theorem: an off-anchor fan is a "
            "distinct-head four-good overlap, while an anchor-contained fan "
            "is the common five-lock endpoint-holonomy interface"
        ),
        "sole_new_geometry": (
            "a four-site 2+2 diagonal switch: either 72 physical-C4 switches "
            "or 18 same-skeleton colour swaps.  Every unused K4 matching is "
            "off-diagonal in both words"
        ),
        "scope": (
            "this classifies literal zero-Fitting two-row blocks after "
            "spectator factorization.  It does not close the diagonal 2+2 "
            "switch, higher critical SCCs, or prove that arbitrary reductions "
            "remain binomial"
        ),
    }


def main():
    ledger = audit()
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))
    print("OO equal-partition zero-holonomy reduction: PASS")
    print("core6: 6/6 distinct pairs contain an off-diagonal spectator cell")
    print("core4: 4932 off-diagonal routes; 72 diagonal C4 switches; 18 same-skeleton colour swaps")
    print("core8: no distinct literal-row pair")
    print("sha256:", digest)


if __name__ == "__main__":
    main()
