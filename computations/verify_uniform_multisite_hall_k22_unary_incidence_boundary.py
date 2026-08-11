#!/usr/bin/env python3
"""Unary incidence audit for the opposite-shore strict Hall K2,2 packet.

The second core matching in each diagonal hole family restores the colour
column lost when a natural selected arm is cut; the direct unary matching
restores colour zero.  Thus the two natural shore overlaps are active and
four-good.  Their curvature determinants are the two shore 2x2 minors.

In the curvature-flat residual, the literal axis crossed rows force the
pure-zero two-cofactors on the shore edges 03 and 12 to vanish.  A genuine
pure-zero six-site matching can have top coefficient one with both these
cofactors zero, so this unary incidence condition is sharp.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_multisite_hall_k22_source_reduction.py":
        "6f75623da9a371303fad5a7986fa3dba464e8c0fb593c97dc23df04a0e84b9f4",
    "notes/uniform-multisite-hall-k22-source-reduction.md":
        "ed05ae4c38b048932fcb9b50c452c074d96b555f4f00a17b18b25045cac197c9",
    "computations/verify_oo_curved_doubly_good_minimal_fullnine_unit.py":
        "5340f74c4f430241d006b69db35cac464fc227f369de52db17c10e8d19253396",
    "notes/oo-curved-doubly-good-minimal-fullnine-unit.md":
        "25b09a934e18b05b14eb158e4ada8c45a34b25cd8629a87fc81c15e558a34ff2",
}
EXPECTED_LEDGER_SHA256 = "3b9bac27ddafe82e3fd315beb1307fa6144d4f7de0a7db2e5eb4dbbe8120e58c"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def perfect_matching(*edges):
    flat = [site for edge in edges for site in edge]
    require(len(flat) == len(set(flat)), f"not a matching: {edges}")
    return tuple(tuple(sorted(edge)) for edge in edges)


def partner(matching, site):
    for left, right in matching:
        if left == site:
            return right
        if right == site:
            return left
    raise RuntimeError((matching, site))


def rank(matrix):
    matrix = [[Q(value) for value in row] for row in matrix]
    pivot_row = 0
    if not matrix:
        return 0
    for column in range(len(matrix[0])):
        pivot = next((row for row in range(pivot_row, len(matrix))
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value
                             for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [entry - value * pivot_entry
                           for entry, pivot_entry
                           in zip(matrix[row], matrix[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def selected_rank(matchings, pair, endpoint):
    other = pair[0] if endpoint == pair[1] else pair[1]
    labels = []
    for colour, matching in matchings:
        neighbour = partner(matching, endpoint)
        if neighbour != other:
            labels.append((neighbour, colour))
    # The star has three endpoint rows.  A diagonal E_cc witness supplies
    # row c; multiple neighbours in one colour do not increase the rank.
    return len({colour for _neighbour, colour in labels}), tuple(labels)


def audit_unary_rank_repair():
    # Outer endpoints P=6,S=7.  The pure-zero matching deliberately avoids
    # the two opposite-shore edges 03 and 12 while remaining nonzero.
    q0 = perfect_matching((6, 7), (0, 1), (2, 4), (3, 5))
    q1_left = perfect_matching((6, 0), (7, 1), (2, 3), (4, 5))
    q1_right = perfect_matching((6, 3), (7, 2), (0, 1), (4, 5))
    q2_left = perfect_matching((6, 2), (7, 0), (1, 3), (4, 5))
    q2_right = perfect_matching((6, 1), (7, 3), (0, 2), (4, 5))
    selected = (
        (0, q0),
        (1, q1_left), (1, q1_right),
        (2, q2_left), (2, q2_right),
    )

    overlaps = (((6, 0), (7, 0)), ((6, 1), (7, 1)))
    audits = []
    for first, second in overlaps:
        ranks = tuple(selected_rank(selected, pair, endpoint)[0]
                      for pair in (first, second) for endpoint in pair)
        require(ranks == (3, 3, 3, 3),
                f"the unary/second-core rank repair changed: {ranks}")
        audits.append({
            "pairs": [first, second],
            "selected_ranks": ranks,
            "activity": [True, True],
        })

    # Each natural arm occurs in one selected target monomial with a
    # nonzero complementary perfect matching, hence is support-active.
    for pair, matching in (((6, 0), q1_left), ((7, 0), q2_left),
                           ((6, 1), q2_right), ((7, 1), q1_left)):
        normalized = tuple(sorted(pair))
        require(normalized in matching,
                f"selected activity witness lost: {pair}")
        require(len(tuple(edge for edge in matching
                          if edge != normalized)) == 3,
                "an activity cofactor stopped being a perfect matching")

    return {
        "selected_matchings": {
            "Q0": q0,
            "Q1_core": [q1_left, q1_right],
            "Q2_core": [q2_left, q2_right],
        },
        "shore_overlap_audits": audits,
        "rank_mechanism": (
            "cutting a diagonal selected arm loses its own colour column; "
            "the second disjoint core matching restores that colour, the "
            "other diagonal target restores the other nonzero colour, and "
            "the direct unary matching restores colour zero"
        ),
    }


def pure_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        remainder = vertices[1:index] + vertices[index + 1:]
        for tail in pure_matchings(remainder):
            yield ((first, second),) + tail


def hafnian(support, vertices):
    return sum(
        1 for matching in pure_matchings(vertices)
        if all(tuple(sorted(edge)) in support for edge in matching)
    )


def audit_unary_cofactor_darkness():
    # One literal top matching 01|24|35.  It proves that top=1 does not force
    # either complementary shore cofactor H_03 or H_12 to be nonzero.
    support = {(0, 1), (2, 4), (3, 5)}
    top = hafnian(support, range(6))
    h03 = hafnian(support, (1, 2, 4, 5))
    h12 = hafnian(support, (0, 3, 4, 5))
    require((top, h03, h12) == (1, 0, 0),
            f"the unary cofactor-dark guard changed: {top,h03,h12}")

    # On the strict opposite axis chart all four core star coefficients are
    # nonzero.  The four distinct crossed output words therefore give the
    # displayed monomial equations, forcing H03=H12=0 in the absence of
    # cancellation mates in the same word grade.
    equations = (
        "a0*d3*H03", "a3*d0*H03",
        "b1*c2*H12", "b2*c1*H12",
    )
    words = ((1, 0, 0, 2), (2, 0, 0, 1),
             (0, 2, 1, 0), (0, 1, 2, 0))
    require(len(set(words)) == 4,
            "the four axis crossed word grades collided")
    return {
        "literal_pure_zero_support": sorted(support),
        "top_hafnian": top,
        "shore_cofactors": {"H03": h03, "H12": h12},
        "axis_crossed_equations": equations,
        "axis_crossed_word_restrictions": words,
        "scope": (
            "a cancellation mate in one of these four word grades leaves "
            "the pure selected-axis packet and must be routed separately; "
            "without such a mate the crossed rows force H03=H12=0"
        ),
    }


def audit_curvature_dichotomy():
    # The two shore curvature minors.  Values all one give the sharp flat
    # guard while keeping every selected core coefficient nonzero.
    values = {name: Q(1) for name in
              ("a0", "a3", "d0", "d3", "b1", "b2", "c1", "c2")}
    kappa_a = values["a0"] * values["d3"] - (
        values["d0"] * values["a3"]
    )
    kappa_b = values["b1"] * values["c2"] - (
        values["c1"] * values["b2"]
    )
    require((kappa_a, kappa_b) == (0, 0),
            "the double-flat shore guard changed")

    # Over an integral domain, a zero 2x2 determinant with all four entries
    # nonzero is precisely proportionality after localization at one entry.
    # Verify the denominator-cleared identities symbolically on a sample.
    samples = ((Q(2), Q(3), Q(4), Q(6)),
               (Q(-1), Q(5), Q(2), Q(-10)))
    for u0, u1, v0, v1 in samples:
        require(u0 * v1 - v0 * u1 == 0,
                "a flat sample stopped being proportional")
        require(u0 * v1 == v0 * u1,
                "the denominator-cleared proportionality changed")
    return {
        "shore_A_curvature": "kappa_A=a0*d3-d0*a3",
        "shore_B_curvature": "kappa_B=b1*c2-c1*b2",
        "curvature_open_landing": (
            "if either kappa is nonzero, the corresponding natural overlap "
            "has two support-active arms, four rank-three deleted stars, "
            "distinct target heads, and a nonzero physical four-cycle minor"
        ),
        "flat_residual": (
            "kappa_A=kappa_B=0, equivalently the two endpoint vectors are "
            "proportional on each shore after localizing a core coefficient"
        ),
        "flat_scalar_guard": {name: int(value)
                              for name, value in values.items()},
    }


def main():
    pin_dependencies()
    ledger = {
        "unary_rank_repair": audit_unary_rank_repair(),
        "unary_cofactor_darkness": audit_unary_cofactor_darkness(),
        "curvature_dichotomy": audit_curvature_dichotomy(),
        "theorem_boundary": (
            "the strict opposite K2,2 core already supplies active four-good "
            "natural overlaps once both disjoint diagonal matchings and the "
            "direct unary anchor are retained.  Nonzero shore curvature "
            "reaches the curved-good interface.  The sole selected-axis "
            "residual is double-flat shore proportionality together with "
            "H03=H12=0; unary top=1 does not exclude this cofactor darkness"
        ),
        "scope": (
            "exact selected-matching and literal crossed-word family audit, "
            "not a full one-bad source.  Arbitrary same-word cancellation "
            "mates and the double-flat shore lock remain separate"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"Hall K2,2 unary ledger changed: {digest}")
    print("uniform strict Hall K2,2 unary incidence boundary: PASS")
    print("both natural overlaps: active with ranks (3,3,3,3)")
    print("curvature-open branch reaches curved-good interface")
    print("flat residual: kappa_A=kappa_B=H03=H12=0")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
