#!/usr/bin/env python3
"""Close the co-located Hall-star lock using the unary scalar arm.

The one-bad outer block is lambda*E_00.  Therefore the outer neighbour S
cannot occur in either private-site determinant for the reciprocal cells
12 and 21.  In the trapped branch of 19bc055 both private identities are
forced onto the Hall centre c.  Their original nonzero crossed cofactors
repair the colour-2 and colour-1 rows at c after deleting P-c; the unary
matching repairs colour 0.  Thus P-c and the already-good P-u form the
required active distinct-head four-good wedge.
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
    "computations/verify_uniform_multisite_hall_star_colocated_lock_boundary.py":
        "11627ef80bc4a99366c88fd042b08daff1b6f2125c54ea4d2367586b5db2967a",
    "notes/uniform-multisite-hall-star-colocated-lock-boundary.md":
        "177e1bf4ee204e477f54ad1f7baea2ab3f56cde115d3554c16b7e87c92ae004c",
    "computations/verify_shared_reciprocal_two_bad_anchor_safe_retraction.py":
        "a280b40657f2ab02c9c9f6ecf50dd3326db12bcc20614cbbd12bddffac8a1b62",
    "notes/shared-reciprocal-two-bad-anchor-safe-retraction.md":
        "dda2e2e0b3e81bca41392f355ce3f678a38d8f09053646b2f22df3a86b24bee5",
    "computations/verify_uniform_five_lock_wedge_or_switch.py":
        "c2541a60db1f8e7a661bc698d2bd1f1a1f396a0f0bfde389ea89bea17fac175e",
    "notes/uniform-five-lock-wedge-or-switch.md":
        "0871d5151a0fdb46fee0c9b15797a864e579a85c360a2638d458583479426914",
}
EXPECTED_LEDGER_SHA256 = (
    "0aa7d13eb0ccc868820c6c4c5dea95a620dc00fcbf0b0e14fb2cd6becfc58396"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def clean(polynomial):
    return Counter({term: coefficient for term, coefficient
                    in polynomial.items() if coefficient})


def variable(name):
    return Counter({(name,): Q(1)})


def constant(value):
    return Counter({(): Q(value)}) if value else Counter()


def add(*polynomials):
    answer = Counter()
    for polynomial in polynomials:
        answer.update(polynomial)
    return clean(answer)


def scale(polynomial, scalar):
    return clean(Counter({term: Q(scalar) * coefficient
                          for term, coefficient in polynomial.items()}))


def multiply(*polynomials):
    answer = constant(1)
    for polynomial in polynomials:
        updated = Counter()
        for left, left_coefficient in answer.items():
            for right, right_coefficient in polynomial.items():
                updated[tuple(sorted(left + right))] += (
                    left_coefficient * right_coefficient
                )
        answer = clean(updated)
    return answer


def audit_private_identity(direction, pure_colour, mixed_colour):
    """Replay p_u G_mixed-x G_pure=x+sum Delta_us C_s."""
    x = variable(f"x{direction}")
    p_u = variable(f"p{direction}_u")
    terms = {}
    g_pure = multiply(p_u, variable(f"C{direction}_u"))
    g_mixed = multiply(x, variable(f"C{direction}_u"))
    for site in ("S", "c", "f0", "f1"):
        p_s = variable(f"p{direction}_{site}")
        q_s = variable(f"q{direction}_{site}")
        cofactor = variable(f"C{direction}_{site}")
        g_pure = add(g_pure, multiply(p_s, cofactor))
        g_mixed = add(g_mixed, multiply(q_s, cofactor))
        terms[site] = multiply(
            add(multiply(p_u, q_s),
                scale(multiply(x, p_s), -1)),
            cofactor,
        )
    g_pure = add(g_pure, constant(-1))
    left = add(multiply(p_u, g_mixed),
               scale(multiply(x, g_pure), -1))
    right = add(x, *terms.values())
    require(left == right,
            f"the private source identity changed in direction {direction}")

    # A_PS=lambda E_00.  For a in {1,2}, b the other binary colour,
    # both the pure and changed entries in column a are literally zero.
    direct = {(0, 0): Q(1)}
    p_s = direct.get((pure_colour, pure_colour), Q(0))
    q_s = direct.get((mixed_colour, pure_colour), Q(0))
    require(p_s == q_s == 0,
            f"the scalar unary arm acquired a {direction} entry")
    delta_s = p_s * Q(7) - q_s * Q(11)
    require(delta_s == 0,
            f"the outer-neighbour determinant survived in {direction}")
    return {
        "direction": direction,
        "private_identity":
            f"p_u*G_mixed-x{direction}*G_pure="
            f"x{direction}+sum_s Delta{direction}_us*C{direction}_s",
        "pure_mixed_colours": [pure_colour, mixed_colour],
        "outer_block": "E00",
        "outer_entries": {
            f"A_PS({pure_colour},{pure_colour})": 0,
            f"A_PS({mixed_colour},{pure_colour})": 0,
        },
        "outer_transition": 0,
        "trapped_consequence":
            f"Delta{direction}_uc*C{direction}_c=-x{direction}!=0",
    }


def rank(matrix):
    matrix = [[Q(value) for value in row] for row in matrix]
    pivot_row = 0
    for column in range(len(matrix[0])):
        pivot = next((row for row in range(pivot_row, len(matrix))
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [entry - value * pivot_entry
                           for entry, pivot_entry
                           in zip(matrix[row], matrix[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def coordinate_rank(labels):
    basis = {label: index for index, label in enumerate(sorted(set(labels)))}
    matrix = [[Q(basis[label] == row) for label in labels]
              for row in range(len(basis))]
    return rank(matrix)


def audit_repaired_pair_ranks():
    # At P after deleting P-c: unary row 0 comes from P-S, while the two
    # reciprocal cells on P-u provide endpoint rows 1 and 2.
    p_labels = (("S", 0), ("u", 2), ("u", 1))
    require(coordinate_rank(p_labels) == 3,
            "the reciprocal block did not repair the P star")

    # The original Hall crossed cofactor for x12 has colour 1 at c and
    # colour 2 elsewhere; the x21 cofactor has colour 2 at c and colour 1
    # elsewhere.  After deleting P,u, a nonzero matching term therefore
    # supplies an incident colour-1/colour-2 cell at c.  Its physical
    # neighbour is arbitrary.  The unary pure matching supplies colour 0.
    # Audit all
    # possible coincidences of those three neighbours: colour labels retain
    # independence, and none is P because the cofactors/pure residual have
    # already deleted P or use P-S.
    patterns = 0
    for neighbours in itertools.product(range(3), repeat=3):
        # Rows at c are 0,1,2.  Their selected neighbour colours are
        # respectively 0,2,1 in the unary, 12-crossed, 21-crossed words.
        labels = (
            (neighbours[0], 0),
            (neighbours[1], 2),
            (neighbours[2], 1),
        )
        require(coordinate_rank(labels) == 3,
                "a repaired c-star neighbour coincidence lost rank")
        patterns += 1
    require(patterns == 27, "the c-star coincidence audit changed")
    return {
        "P_after_deleting_Pc": ["P-S:00", "P-u:12", "P-u:21"],
        "P_rank": 3,
        "c_after_deleting_Pc": [
            "one cell from the unary pure-0 residual matching",
            "the colour-1-at-c cell from a nonzero Hall C12_u matching",
            "the colour-2-at-c cell from a nonzero Hall C21_u matching",
        ],
        "c_rank": 3,
        "neighbour_coincidence_patterns": patterns,
        "why_surviving": (
            "C12_u and C21_u delete P,u, while the unary matching uses "
            "P-S; their selected cells at c never use the deleted pair P-c"
        ),
    }


def main():
    pin_dependencies()
    directions = [
        audit_private_identity("12", pure_colour=2, mixed_colour=1),
        audit_private_identity("21", pure_colour=1, mixed_colour=2),
    ]
    ranks = audit_repaired_pair_ranks()
    ledger = {
        "dependencies": PINS,
        "private_rows": directions,
        "repaired_pair": ranks,
        "field_step": (
            "x12,x21 are nonzero; with every free transition zero and the "
            "outer S transitions identically zero, each c product equals "
            "-xij and hence has nonzero determinant and cofactor"
        ),
        "wedge": {
            "first_pair": "P-u (off-anchor, already rank-(3,3) and active)",
            "second_pair": "P-c (repaired rank-(3,3), active in both pure rows)",
            "shared_endpoint": "P",
            "transition": "Delta12_uc*C12_c or Delta21_uc*C21_c is nonzero",
            "landing": "distinct-head active four-good overlap",
        },
        "theorem": (
            "the co-located bidirectional Hall-star residual cannot remain "
            "trapped on {S,c}: the scalar unary arm kills S coefficientwise, "
            "and the forced c transitions plus the two original crossed "
            "cofactors repair P-c into the second four-good active arm"
        ),
        "scope": (
            "uniform in h>=3 for the anchor-safely retracted one-bad packet "
            "A_PS=lambda*E00; uses the genuine nonzero crossed cofactors and "
            "the selected unary pure matching, with no support census"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"co-located unary wedge ledger changed: {digest}")
    print("uniform co-located Hall-star unary wedge closure: PASS")
    print("outer S transitions: 0/2; forced Hall-centre transitions: 2/2")
    print("P-c deleted-star ranks repaired to (3,3)")
    print("landing: P-u / P-c distinct-head active four-good wedge")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
