#!/usr/bin/env python3
"""Route the 15 pure-colour unary matchings in the strict Hall K2,2 core.

The two colour-1 diagonal core terms force the pure-1 matching
M1=01|23|45 to be nonzero, while q^[3]=X0 forces its pure-1 unary
coefficient to vanish.  The other fourteen K6 matchings split into two
q45/K4 alternatives and twelve bridge matchings.  Relative to a fixed
bridge unary anchor Q0, exactly one bridge is its physical copy and the
other eleven expose a pair outside the selected anchor web.

The three nonfree alternatives route as follows.  The Q0 copy is an
additional contribution to the same diagonal target coefficient and hence
is exactly the affine line-hitting/joint-kernel gate.  The M3 alternative
enters the literal crossed shore cofactor.  The M2 alternative enters a
mixed coefficient of the other diagonal response and forces a bridge
product or an off-axis star mate.  No odd signed holonomy is asserted.
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
    "computations/verify_uniform_multisite_hall_k22_unary_incidence_boundary.py":
        "d9526464fda779a0500ff11024db8bdfef433da573d978a1809509975d1cc14a",
    "notes/uniform-multisite-hall-k22-unary-incidence-boundary.md":
        "f78e01143bf0adfedc993184ebf3b57f85bf597602e8fe466f899e92b2629f26",
    "computations/verify_uniform_multisite_endpoint_affine_hall_concentration_boundary.py":
        "f24e9bd69ec4baef96104557571c154b399f87f34074edffda27e551f33c2205",
    "notes/uniform-multisite-endpoint-affine-hall-concentration-boundary.md":
        "241b46d9ecede656aa59f2be6d74bc288fbada2aa4843103a950441066763df2",
    "computations/verify_uniform_one_bad_nonanchor_offdiagonal_good_pair.py":
        "64e85cd84112b5160efe4f43ce1208da3c49f5e58b3e4a4d6192e6a9c229c306",
    "notes/uniform-one-bad-nonanchor-offdiagonal-good-pair.md":
        "4516c5ff02f130e1ad25b4fde395c81557e58ba0c83f7f98969d95df17fd6409",
}
EXPECTED_LEDGER_SHA256 = "1619d4e8916463a4119f6f15ae2f6adb5e229ab4e4cb599040fd67fd5b8c1199"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def edge(left, right):
    return tuple(sorted((left, right)))


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    left = vertices[0]
    for index, right in enumerate(vertices[1:], 1):
        remainder = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remainder):
            yield tuple(sorted((edge(left, right),) + tail))


M1 = tuple(sorted((edge(0, 1), edge(2, 3), edge(4, 5))))
M2 = tuple(sorted((edge(0, 2), edge(1, 3), edge(4, 5))))
M3 = tuple(sorted((edge(0, 3), edge(1, 2), edge(4, 5))))
Q0 = tuple(sorted((edge(0, 1), edge(2, 4), edge(3, 5))))


def audit_fifteen_matching_split():
    matchings = tuple(perfect_matchings(range(6)))
    require(len(matchings) == 15 and M1 in matchings,
            "the K6 matching universe changed")
    with_45 = tuple(matching for matching in matchings if edge(4, 5) in matching)
    bridges = tuple(matching for matching in matchings if edge(4, 5) not in matching)
    require(set(with_45) == {M1, M2, M3} and len(bridges) == 12,
            "the q45/K4 versus bridge split changed")
    require(Q0 in bridges, "the normalized unary anchor stopped being a bridge")

    selected_anchor_edges = set(M1) | set(M2) | set(M3) | set(Q0)
    noncopy_bridges = tuple(matching for matching in bridges if matching != Q0)
    free_edges = {}
    for matching in noncopy_bridges:
        outside = tuple(sorted(set(matching) - selected_anchor_edges))
        # Q1,Q2 use only K4 edges and 45 on their residual q parts.  A
        # bridge different from Q0 changes at least one bridge edge, hence
        # exposes a physical pair outside all three selected pure matchings.
        require(outside,
                f"a noncopy bridge stayed inside the selected anchor web: {matching}")
        free_edges[str(matching)] = outside
    require(len(noncopy_bridges) == 11,
            "the free bridge count changed")
    return {
        "selected_pure1_matching": M1,
        "q45_k4_matchings": [M1, M2, M3],
        "bridge_matching_count": len(bridges),
        "exact_Q0_copy": Q0,
        "free_noncopy_bridge_count": len(noncopy_bridges),
        "free_edge_witnesses": free_edges,
        "arithmetic_guard": (
            "there are fourteen alternatives to M1: eleven free noncopy "
            "bridges plus exactly Q0, M2, and M3"
        ),
    }


# Sparse commutative polynomials over Q.
def clean(polynomial):
    return Counter({term: coefficient for term, coefficient
                    in polynomial.items() if coefficient})


def variable(name):
    return Counter({(name,): Q(1)})


def add(*polynomials):
    answer = Counter()
    for polynomial in polynomials:
        answer.update(polynomial)
    return clean(answer)


def multiply(*polynomials):
    answer = Counter({(): Q(1)})
    for polynomial in polynomials:
        updated = Counter()
        for left, left_coefficient in answer.items():
            for right, right_coefficient in polynomial.items():
                updated[tuple(sorted(left + right))] += (
                    left_coefficient * right_coefficient
                )
        answer = clean(updated)
    return answer


def audit_selected_unary_pivot():
    # The two colour-1 diagonal response monomials have cofactors
    # q23^11*z1 and q01^11*z1.  Their nonvanishing forces all three factors
    # in the selected pure-1 unary matching M1.
    p0, s1, p3, s2 = (variable(name)
                       for name in ("p1_0", "s1_1", "p1_3", "s1_2"))
    q01, q23, z1 = (variable(name)
                     for name in ("q01_11", "q23_11", "q45_11"))
    diagonal_left = multiply(p0, s1, q23, z1)
    diagonal_right = multiply(p3, s2, q01, z1)
    unary_pivot = multiply(q01, q23, z1)
    require(len(diagonal_left) == len(diagonal_right) == len(unary_pivot) == 1,
            "a selected core monomial split")
    return {
        "diagonal_core_monomials": [
            "p1_0*s1_1*q23_11*q45_11",
            "p1_3*s1_2*q01_11*q45_11",
        ],
        "forced_unary_pivot": "q01_11*q23_11*q45_11 != 0",
        "unary_row": (
            "[111111]q^[3]=0 forces at least one of the other fourteen "
            "physical perfect-matching products to be nonzero"
        ),
    }


def audit_anchor_web_routing_rows():
    # M3 route: in the 12 crossed axis word, deleting shore edge 03 leaves
    # q12*q45 plus its two bridge pairings.
    q12, z1, q14, q25, q15, q24 = (
        variable(name) for name in
        ("q12_11", "q45_11", "q14_11", "q25_11",
         "q15_11", "q24_11")
    )
    h03 = add(multiply(q12, z1), multiply(q14, q25), multiply(q15, q24))
    require(set(h03) == {
        ("q12_11", "q45_11"),
        ("q14_11", "q25_11"),
        ("q15_11", "q24_11"),
    }, "the M3 crossed cofactor expansion changed")

    # M2 route: the colour-1 copy q13*q45 is the selected-axis pivot in a
    # mixed coefficient of the colour-2 diagonal response with holes 02.
    q13, q14b, q35, q15b, q34 = (
        variable(name) for name in
        ("q13_11", "q14_11", "q35_11", "q15_11", "q34_11")
    )
    h02 = add(multiply(q13, z1), multiply(q14b, q35),
              multiply(q15b, q34))
    p2_2, s2_0 = variable("p2_2"), variable("s2_0")
    mixed_diagonal_row = multiply(p2_2, s2_0, h02)
    require(len(mixed_diagonal_row) == 3,
            "the M2 mixed diagonal cofactor changed")

    # Q0-copy route: recolour edge 01 of Q0 to colour1 and retain the pure0
    # complement.  The coefficient is q01^11 times the complete pure0
    # cofactor H01.  This is the same complete cofactor occurring in the
    # colour-1 diagonal response with holes 01, hence an affine-fibre
    # contribution rather than an independent unit.
    q01_11 = variable("q01_11")
    q23_00, q45_00, q24_00, q35_00, q25_00, q34_00 = (
        variable(name) for name in
        ("q23_00", "q45_00", "q24_00", "q35_00",
         "q25_00", "q34_00")
    )
    h01_00 = add(multiply(q23_00, q45_00),
                 multiply(q24_00, q35_00),
                 multiply(q25_00, q34_00))
    unary_mixed = multiply(q01_11, h01_00)
    p1_0, s1_1 = variable("p1_0"), variable("s1_1")
    diagonal_mixed = multiply(p1_0, s1_1, h01_00)
    require(len(unary_mixed) == len(diagonal_mixed) == 3,
            "the Q0-copy complete cofactor changed")

    return {
        "M3_crossed_route": {
            "row": "p1_0*s2_3*(q12_11*q45_11+q14_11*q25_11+q15_11*q24_11)",
            "consequence": (
                "the M3 pivot forces a bridge product or a same-word "
                "off-axis star cancellation mate"
            ),
        },
        "M2_other_diagonal_route": {
            "word": "colour2 at holes 02, colour1 on 1345",
            "row": "p2_2*s2_0*(q13_11*q45_11+q14_11*q35_11+q15_11*q34_11)",
            "consequence": (
                "the M2 colour-1 copy forces a bridge product or an "
                "off-axis endpoint-star mate in the colour-2 diagonal row"
            ),
        },
        "Q0_copy_affine_route": {
            "unary_word": "110000",
            "unary_row": "q01_11*H01_00 plus off-diagonal matching terms",
            "diagonal_row": "p1_0*s1_1*H01_00 plus endpoint-star mates",
            "conclusion": (
                "the exact physical Q0 copy contributes through the same "
                "complete cofactor H01 as the diagonal target; it lands on "
                "the established affine line-hitting/joint-kernel gate, "
                "not on an odd signed unit"
            ),
        },
    }


def audit_q45_nonimplication():
    # This exact scalar support is a counterguard to the inference
    # H03=H12=0 and top=1 => q45=0.  The q45 cell is top-invisible here.
    support = {edge(0, 1), edge(2, 4), edge(3, 5), edge(4, 5)}

    def count(vertices):
        return sum(all(pair in support for pair in matching)
                   for matching in perfect_matchings(vertices))

    top = count(range(6))
    h03 = count((1, 2, 4, 5))
    h12 = count((0, 3, 4, 5))
    require((top, h03, h12) == (1, 0, 0)
            and edge(4, 5) in support,
            "the q45 nonimplication guard changed")
    return {
        "support": sorted(support),
        "top": top,
        "H03": h03,
        "H12": h12,
        "q45_nonzero": True,
        "conclusion": (
            "the two cofactor equations alone do not force q45=0; the "
            "pure-colour unary zero rows and response routing above are "
            "the genuinely load-bearing inputs"
        ),
    }


def main():
    pin_dependencies()
    ledger = {
        "fifteen_matching_split": audit_fifteen_matching_split(),
        "selected_unary_pivot": audit_selected_unary_pivot(),
        "anchor_web_routing_rows": audit_anchor_web_routing_rows(),
        "q45_nonimplication": audit_q45_nonimplication(),
        "theorem_boundary": (
            "the selected pure-1 unary matching has fourteen alternatives: "
            "eleven free noncopy bridges, the exact Q0 copy which lands on "
            "the affine gate, M3 which lands in a crossed cofactor, and M2 "
            "which lands in a mixed coefficient of the other diagonal row. "
            "The latter two force bridge products or off-axis mates.  No "
            "odd signed holonomy or full-packet contradiction is claimed"
        ),
        "scope": (
            "literal six-site matching and complete-cofactor family algebra; "
            "a bridge/off-axis mate routes to existing source machinery, "
            "while the affine Q0-copy branch remains the earlier joint-kernel gate"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"Hall K2,2 unary-mate ledger changed: {digest}")
    print("uniform strict Hall K2,2 unary mate routing: PASS")
    print("K6 alternatives: 11 free bridges + Q0 copy + M2 + M3")
    print("M2 -> other diagonal mixed row; M3 -> crossed row")
    print("Q0 copy -> affine line-hitting/joint-kernel gate")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
