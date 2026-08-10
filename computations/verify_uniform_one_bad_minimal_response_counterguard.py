#!/usr/bin/env python3
"""Uniform minimum-support response guard without top/cofactor provenance.

For every h>=3 this constructs formal four-hole tensors F_uv on 2h sites
and four endpoint stars with

    p_i*s_j*F = delta_ij X_i,  i,j in {1,2},

minimum total star-site support six, but p1^[2],p2^[2] nonzero.  The guard is
not asserted to equal F=q^[h-1] for a common q.  Indeed its pure-zero Euler
row is 0=h, so exact q^[h]=X0 provenance kills it immediately.  This isolates
the additional source row which a valid concentration theorem must use.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "notes/centered-rank-one-two-star-pure-response-obstruction.md":
        "685d76abf57ed21249196e5c22d20875460f6fdb6793c688ee54b4c6dedc21ee",
    "computations/verify_uniform_one_bad_square_zero_clean_cap.py":
        "a943fffdc3ce86aa5506e6774ec3a6a8ff10c70491225417152a1298e2754883",
    "notes/full-nine-type3-annihilator-plane-closure.md":
        "c555baf00004a2738ad85ff77f8b76f62aa71ae8cb2c37733be7c13d5d5bde0d",
}
EXPECTED_LEDGER_SHA256 = (
    "ea721127daa4254db9eefbf5f7b062da24e5118f564fc0de2d0c1a1d0f7c0939"
)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def restrict_word(word, holes):
    return tuple(colour for site, colour in enumerate(word)
                 if site not in holes)


def build_formal_cofactors(h):
    sites = tuple(range(2 * h))
    x1 = (1,) * len(sites)
    x2 = (2,) * len(sites)
    y = list(x1)
    y[2] = 0
    y = tuple(y)
    z = list(x2)
    z[0] = 0
    z = tuple(z)

    cofactors = {}

    def put(holes, full_word, coefficient):
        holes = frozenset(holes)
        cofactors.setdefault(holes, Counter())[
            restrict_word(full_word, holes)
        ] += Fraction(coefficient)

    put((0, 5), x1, 1)
    put((0, 5), y, 1)
    put((1, 5), y, -1)
    put((2, 4), x2, 1)
    put((2, 4), z, 1)
    put((3, 4), z, -1)
    cofactors = {
        holes: Counter({word: coefficient for word, coefficient
                        in tensor.items() if coefficient})
        for holes, tensor in cofactors.items()
    }
    return sites, cofactors, {"X1": x1, "X2": x2, "Y": y, "Z": z}


def response(sites, cofactors, left, right):
    output = Counter()
    for left_site, left_colour, left_coefficient in left:
        for right_site, right_colour, right_coefficient in right:
            if left_site == right_site:
                continue
            holes = frozenset((left_site, right_site))
            complement = tuple(site for site in sites if site not in holes)
            for cofactor_word, coefficient in cofactors.get(holes, {}).items():
                word = [-1] * len(sites)
                word[left_site] = left_colour
                word[right_site] = right_colour
                for site, colour in zip(complement, cofactor_word, strict=True):
                    word[site] = colour
                output[tuple(word)] += (
                    Fraction(left_coefficient)
                    * Fraction(right_coefficient) * coefficient
                )
    return Counter({word: coefficient for word, coefficient in output.items()
                    if coefficient})


def audit_order(h):
    sites, cofactors, words = build_formal_cofactors(h)
    p1 = ((0, 1, 1), (1, 1, 1))
    s1 = ((5, 1, 1),)
    p2 = ((2, 2, 1), (3, 2, 1))
    s2 = ((4, 2, 1),)
    rows = {
        "11": response(sites, cofactors, p1, s1),
        "12": response(sites, cofactors, p1, s2),
        "21": response(sites, cofactors, p2, s1),
        "22": response(sites, cofactors, p2, s2),
    }
    require(rows == {
        "11": Counter({words["X1"]: Fraction(1)}),
        "12": Counter(),
        "21": Counter(),
        "22": Counter({words["X2"]: Fraction(1)}),
    }, f"the formal four-response packet changed at h={h}")

    # Exact joint-kernel columns with the opposite rows fixed.  The two
    # occupied p1 components are X1+Y and -Y; the p2 components are X2+Z
    # and -Z.  They are independent, so neither occupied component can be
    # removed by a joint-kernel first variation.
    p1_columns = (
        response(sites, cofactors, ((0, 1, 1),), s1),
        response(sites, cofactors, ((1, 1, 1),), s1),
    )
    p2_columns = (
        response(sites, cofactors, ((2, 2, 1),), s2),
        response(sites, cofactors, ((3, 2, 1),), s2),
    )
    require(p1_columns == (
        Counter({words["X1"]: 1, words["Y"]: 1}),
        Counter({words["Y"]: -1}),
    ), f"the p1 joint-kernel columns changed at h={h}")
    require(p2_columns == (
        Counter({words["X2"]: 1, words["Z"]: 1}),
        Counter({words["Z"]: -1}),
    ), f"the p2 joint-kernel columns changed at h={h}")

    # Minimum-support proof: X1 occurs in only F_05 and brings Y with the
    # same coefficient; cancelling Y requires F_15.  Thus the p1,s1 support
    # union must realize both edges 05 and 15, costing at least three total
    # site occurrences.  The disjoint colour-2 argument uses 24 and 34.
    pure_holes = {1: frozenset((0, 5)), 2: frozenset((2, 4))}
    cancellation_holes = {1: frozenset((1, 5)), 2: frozenset((3, 4))}
    require(all(len(pure_holes[colour] | cancellation_holes[colour]) == 3
                for colour in (1, 2)),
            "the minimum-support edge unions changed")
    displayed_support = len(p1) + len(s1) + len(p2) + len(s2)
    require(displayed_support == 6,
            "the displayed minimum star support changed")

    # Exact top-provenance failure.  If F_uv=q^[h-1]_{delete uv}, Euler's
    # matching identity at the pure-zero word is
    #   sum q_uv(00) F_uv(0...0) = h q^[h](0...0) = h.
    # Every formal F_uv pure-zero coefficient here is zero, so the left side
    # is identically zero for arbitrary q_uv(00).
    pure_zero_cofactor_coefficients = {
        "".join(map(str, sorted(holes))): tensor.get(
            (0,) * (len(sites) - 2), Fraction(0)
        )
        for holes, tensor in cofactors.items()
    }
    require(not any(pure_zero_cofactor_coefficients.values()),
            "the guard unexpectedly acquired pure-zero top provenance")
    return {
        "h": h,
        "residual_sites": len(sites),
        "nonzero_cofactor_holes": [
            list(sorted(holes)) for holes in sorted(
                cofactors, key=lambda holes: tuple(sorted(holes))
            )
        ],
        "response_rows": {"11": "X1", "12": "0", "21": "0", "22": "X2"},
        "star_supports": {
            "p1": [0, 1], "s1": [5], "p2": [2, 3], "s2": [4],
        },
        "minimum_total_site_support": 6,
        "nonzero_self_squares": ["p1^[2]", "p2^[2]"],
        "joint_kernel_columns": {
            "p1": ["X1+Y", "-Y"],
            "p2": ["X2+Z", "-Z"],
        },
        "pure_zero_euler_row": f"0={h}",
    }


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"pinned dependency changed: {relative}")


def main():
    pin_dependencies()
    # The construction and proof are formula-uniform.  These representatives
    # guard the first six orders without pretending finite replay proves the
    # quantified statement.
    audits = [audit_order(h) for h in range(3, 9)]
    ledger = {
        "pins": PINS,
        "uniform_construction": (
            "for every h>=3, use holes 05/15 for X1+Y/-Y and holes "
            "24/34 for X2+Z/-Z; extend Y,Z by pure factors on all extra sites"
        ),
        "representative_order_audits": audits,
        "verdict": (
            "the four binary response tensors plus minimum total star-site "
            "support do not force square-zero rows at the formal common-"
            "cofactor level"
        ),
        "missing_source_provenance": (
            "there is no common q with q^[h]=X0 asserted; the pure-zero "
            "Euler row sum q_uv(00)F_uv(0...0)=h is already 0=h"
        ),
        "extra_row_needed": (
            "the first-variation proof must use the unary top together with "
            "the exact derivative identity F_uv=q^[h-1]_{delete uv}; response "
            "joint kernels alone cannot prove concentration"
        ),
        "scope": (
            "uniform formal counterguard, not an ordinary source packet, "
            "not a Krenn counterexample, and not a refutation of the full "
            "top-provenant concentration theorem; this concerns only the "
            "projection-degenerate one-bad branch, not the generic rootless "
            "type-3 packet where the pinned annihilator-plane theorem "
            "excludes endpoint-star support at most two"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"uniform minimum-response guard ledger changed: {digest}")
    print("uniform one-bad minimum-response counterguard: PASS")
    print("orders audited: h=3..8; formula valid for every h>=3")
    print("all four binary responses: exact")
    print("minimum total star-site support: 6")
    print("nonzero self-squares: p1^[2], p2^[2]")
    print("missing top provenance: pure-zero Euler row is 0=h")
    print("full top-provenant concentration theorem: OPEN")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
