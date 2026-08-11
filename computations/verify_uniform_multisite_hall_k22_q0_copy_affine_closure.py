#!/usr/bin/env python3
"""Route the exact Q0-copy affine residual of the strict Hall K2,2 core.

Normalize the bridge unary matching Q0=01|24|35, whose K4 core edge 01
belongs to the colour-1 matching M1.  If Q0 also occurs in colour 2, the
mixed colour-1 diagonal response with holes 01 contains the complete
colour-2 cofactor H01.  In the absence of an endpoint-star mate this forces
H01=0.  Expanding the pure-2 unary row along edge 01 then removes all three
matchings using 01.  The selected nonzero M2 term must be cancelled by M3
or by one of ten bridge matchings.  M3 is the crossed route and every such
bridge is free relative to the selected anchor web.

The crossed route may still have an off-axis cancellation mate, so this is
a routing theorem rather than a proof that every downstream lock packet is
empty.

If the mixed response has an endpoint-star mate, it is either the reverse
pure orientation (common-side/affine witness reselection) or contains an
off-diagonal endpoint cell (active/lock route).  Witness reselection alone
does not construct a target-coordinate point in the affine fibre.  The
other K4-core cases follow by exchanging colours or by the crossed-row
argument.
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
    "computations/verify_uniform_multisite_hall_k22_unary_mate_routing.py":
        "543e73ff1ed4eeefb6bbd33a603137f99381c7ad2e7eb28cee5ec55c4ae1956a",
    "notes/uniform-multisite-hall-k22-unary-mate-routing.md":
        "11625211e28d1fd0971f39a05e7da77d66aa4d8c17c357a688b3ec90100c4fec",
    "computations/verify_uniform_multisite_hall_star_source_reduction.py":
        "65ccab6e5830efd9f0dfa084c0d98391e89bad083fa7a41743b2fec7dde15bd5",
    "notes/uniform-multisite-hall-star-source-reduction.md":
        "a0efe068a25423f16d0e24f8d943fd09c4c6911d1dbcdd231d45e66ae37868e0",
    "computations/verify_uniform_five_lock_wedge_or_switch.py":
        "c2541a60db1f8e7a661bc698d2bd1f1a1f396a0f0bfde389ea89bea17fac175e",
    "notes/uniform-five-lock-wedge-or-switch.md":
        "0871d5151a0fdb46fee0c9b15797a864e579a85c360a2638d458583479426914",
}
EXPECTED_LEDGER_SHA256 = "586a44e9293e903aa4c025a08c0fb5869f127bd4450910bb262da099e2294027"


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


def audit_matching_partition_after_cofactor_kill():
    matchings = tuple(perfect_matchings(range(6)))
    using_01 = tuple(matching for matching in matchings
                     if edge(0, 1) in matching)
    avoiding_01 = tuple(matching for matching in matchings
                        if edge(0, 1) not in matching)
    require(len(using_01) == 3 and len(avoiding_01) == 12,
            "the edge-01 expansion split changed")
    require(set(using_01) == {
        M1, Q0, tuple(sorted((edge(0, 1), edge(2, 5), edge(3, 4))))
    }, "the H01 cofactor matchings changed")
    require(M2 in avoiding_01 and M3 in avoiding_01,
            "the two non-01 K4 matchings moved")

    bridges = tuple(matching for matching in avoiding_01
                    if edge(4, 5) not in matching)
    require(len(bridges) == 10,
            "the bridge count after removing edge01 changed")
    anchor_edges = set(M1) | set(M2) | set(M3) | set(Q0)
    for matching in bridges:
        require(set(matching) - anchor_edges,
                f"an avoiding bridge stayed in the selected web: {matching}")
    require(set(avoiding_01) == set(bridges) | {M2, M3},
            "the avoiding matching classification changed")
    return {
        "using_core_edge_01": using_01,
        "avoiding_core_edge_01": {
            "selected_M2": M2,
            "crossed_M3": M3,
            "free_bridges": bridges,
        },
        "counts": {"using_01": 3, "avoiding_01": 12,
                   "free_bridges": 10},
    }


# Sparse commutative polynomials.
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


def audit_literal_row_factorization():
    q23, q45, q24, q35, q25, q34 = (
        variable(name) for name in
        ("q23_22", "q45_22", "q24_22", "q35_22",
         "q25_22", "q34_22")
    )
    h01 = add(multiply(q23, q45), multiply(q24, q35),
              multiply(q25, q34))
    require(set(h01) == {
        ("q23_22", "q45_22"),
        ("q24_22", "q35_22"),
        ("q25_22", "q34_22"),
    }, "the colour-2 H01 cofactor changed")

    p10, s11 = variable("p1_0"), variable("s1_1")
    diagonal_mixed = multiply(p10, s11, h01)
    q01 = variable("q01_22")
    unary_using_01 = multiply(q01, h01)
    require(len(diagonal_mixed) == len(unary_using_01) == 3,
            "the common H01 factorization changed")

    # The pure-2 unary coefficient is q01*H01 plus the twelve matchings
    # avoiding 01.  Record a separate symbol for each avoiding matching and
    # verify that the selected M2 pivot is one of them.
    avoiding = tuple(matching for matching in perfect_matchings(range(6))
                     if edge(0, 1) not in matching)
    remainder_terms = tuple(variable(f"T{index}")
                            for index in range(len(avoiding)))
    pure2 = add(unary_using_01, *remainder_terms)
    require(len(pure2) == 15 and avoiding.index(M2) >= 0,
            "the pure-2 edge expansion changed")

    return {
        "mixed_diagonal_word": "112222",
        "mixed_diagonal_axis_row": "p1_0*s1_1*H01_22",
        "H01_22": (
            "q23_22*q45_22+q24_22*q35_22+q25_22*q34_22"
        ),
        "pure2_unary_factorization":
            "[222222]q^[3]=q01_22*H01_22+sum_{R not containing 01} T_R",
        "selected_nonzero_avoiding_term": "T_M2=q02_22*q13_22*q45_22",
        "consequence_without_endpoint_mate": (
            "the mixed diagonal zero row gives H01_22=0; the pure-2 "
            "unary zero row then forces another avoiding-01 matching "
            "besides the selected nonzero M2"
        ),
    }


def audit_endpoint_mate_types():
    # Output word 112222: a pure diagonal p1/s1 star cell can occur only at
    # sites 0 or 1.  Besides selected orientation (0,1), the only distinct
    # pure-axis orientation is (1,0).  Every star use at 2..5 has residual
    # colour 2 while its outer colour is 1, hence is off-diagonal.
    word = (1, 1, 2, 2, 2, 2)
    ordered_holes = tuple((left, right) for left in range(6)
                          for right in range(6) if left != right)
    pure_axis = tuple(pair for pair in ordered_holes
                      if word[pair[0]] == word[pair[1]] == 1)
    off_axis = tuple(pair for pair in ordered_holes
                     if pair not in pure_axis)
    require(pure_axis == ((0, 1), (1, 0)),
            f"the reverse-axis mate classification changed: {pure_axis}")
    require(len(off_axis) == 28,
            "the off-axis ordered-hole count changed")
    return {
        "selected_orientation": [0, 1],
        "only_pure_axis_mate": [1, 0],
        "off_axis_ordered_holes": len(off_axis),
        "routing": {
            "reverse_axis": (
                "with no off-axis terms the mixed row is "
                "(p1_0*s1_1+p1_1*s1_0)*H01_22=0.  If H01_22 is nonzero, "
                "the star factor vanishes; the same factor multiplies the "
                "pure H01_11 response, so hole01 is ineffective and the "
                "nonzero target sum permits source-preserving witness "
                "reselection to another affine contribution"
            ),
            "other_hole": (
                "at least one endpoint star cell has outer colour1 and "
                "residual colour2, so it is an off-diagonal active/lock mate"
            ),
        },
    }


def audit_three_core_edge_cases():
    # Every bridge matching has exactly one K4-core edge.  The six K4 edges
    # split into M1, M2, M3, so the two-copy argument is uniform: the copy
    # in the other diagonal colour supplies the mixed diagonal row for M1
    # or M2, while an M3 core edge is crossed for both colours.
    core_edges = set(itertools.combinations(range(4), 2))
    partition = {"M1": set(M1) & core_edges,
                 "M2": set(M2) & core_edges,
                 "M3": set(M3) & core_edges}
    require(set().union(*partition.values()) == core_edges
            and sum(map(len, partition.values())) == 6,
            "the K4 core-edge colour partition changed")
    return {
        "core_edge_partition": {
            name: sorted(edges) for name, edges in partition.items()
        },
        "M1_core": "use the colour-2 Q0 copy in the colour-1 diagonal row",
        "M2_core": "use the colour-1 Q0 copy in the colour-2 diagonal row",
        "M3_core": "either copy enters a crossed row",
    }


def main():
    pin_dependencies()
    ledger = {
        "matching_partition": audit_matching_partition_after_cofactor_kill(),
        "literal_row_factorization": audit_literal_row_factorization(),
        "endpoint_mate_types": audit_endpoint_mate_types(),
        "three_core_edge_cases": audit_three_core_edge_cases(),
        "theorem": (
            "the exact Q0 physical-copy affine residual is not a separate "
            "packet after both colour copies.  For a core edge of M1 or M2, the other "
            "colour copy gives a mixed diagonal coefficient.  An endpoint "
            "mate routes to affine witness-reselection/lock alternatives; "
            "without one the complete cofactor vanishes, and the other "
            "pure-colour unary row forces M3 or a free bridge.  A core edge "
            "of M3 is already crossed"
        ),
        "full_closure_requires": [
            (
                "every M3/off-axis mate must exit the active/lock interface "
                "to a proved unit or curved/free branch, excluding the "
                "currently named trapped-lock residual"
            ),
            (
                "reverse-axis witness reselection must either produce an "
                "anchor-safe joint-kernel target-coordinate point or "
                "strictly decrease a well-founded selected-support measure"
            ),
        ],
        "scope": (
            "uniform complete-cofactor factorization and endpoint-word "
            "classification, not a support census or affine-fibre closure.  "
            "The ten avoiding bridges always enter the certified free/active "
            "route; M3 and reverse-axis mates retain the two explicitly named "
            "interfaces above.  The conclusion routes "
            "to existing Hall-star, free-carrier, lock-kernel, or crossed "
            "branches; it does not reprove their downstream closures"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"Hall K2,2 Q0-copy ledger changed: {digest}")
    print("uniform strict Hall K2,2 Q0-copy affine routing: PASS")
    print("M1 core: other-colour copy -> mixed diagonal H01")
    print("H01=0 -> pure unary forces M3 or one of ten free bridges")
    print("endpoint mate -> witness reselection or off-diagonal lock route")
    print("full closure still requires trapped-lock exit and terminating/anchor-safe reselection")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
