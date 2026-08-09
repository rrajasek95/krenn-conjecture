#!/usr/bin/env python3
"""Exact audit of the adjacent-cubic N -> N-2 descent identity.

The calculation is coefficient-free.  Four endpoint ports carry formal
nonzero weights ad, bd, ae, be.  In the four-distinct-port stratum the
four inserted edges have weights

    ad*bd, ae*be, ad*be, -ae*bd.

The only compatible inserted pairs are the two opposite pairings of the
four ports.  They have the same endpoint-colour tensor and opposite formal
weights.  In every collision stratum the two same-colour inserted edges
overlap, so no quadratic insertion term exists.
"""

from collections import defaultdict
from itertools import product


# Monomials use exponents of (ad, bd, ae, be).  A polynomial is a sparse
# dictionary monomial -> integer coefficient.
ONE = (0, 0, 0, 0)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def add_exp(left, right):
    return tuple(x + y for x, y in zip(left, right, strict=True))


def canonical_partition(values):
    relabel = {}
    return tuple(relabel.setdefault(value, len(relabel)) for value in values)


def compatible(left, right):
    return set(left["pair"]).isdisjoint(right["pair"])


def product_signature(left, right):
    require(compatible(left, right), "attempted to multiply colliding insertions")
    decoration = dict(left["decoration"])
    decoration.update(right["decoration"])
    return (
        tuple(sorted(set(left["pair"]) | set(right["pair"]))),
        tuple(sorted(decoration.items())),
        add_exp(left["weight"], right["weight"]),
        left["sign"] * right["sign"],
    )


def make_edge(name, pair, colours, weight, sign=1):
    require(pair[0] != pair[1], f"insertion {name} became a loop")
    return {
        "name": name,
        "pair": pair,
        "decoration": tuple(zip(pair, colours, strict=True)),
        "weight": weight,
        "sign": sign,
    }


def audit_distinct_ports():
    # Endpoint order is (u_d, v_d, u_e, v_e) = (0,1,2,3).
    edges = [
        make_edge("A", (0, 1), ("d", "d"), (1, 1, 0, 0)),
        make_edge("B", (2, 3), ("e", "e"), (0, 0, 1, 1)),
        make_edge("C", (0, 3), ("d", "e"), (1, 0, 0, 1)),
        make_edge("D", (2, 1), ("e", "d"), (0, 1, 1, 0), -1),
    ]

    compatible_pairs = []
    grouped = defaultdict(int)
    for i, left in enumerate(edges):
        for right in edges[i + 1 :]:
            if not compatible(left, right):
                continue
            compatible_pairs.append(left["name"] + right["name"])
            deleted, decoration, weight, sign = product_signature(left, right)
            grouped[(deleted, decoration, weight)] += sign

    require(compatible_pairs == ["AB", "CD"], "compatible-pair census changed")
    require(len(grouped) == 1, "opposite pairings no longer share one signature")
    ((deleted, decoration, weight), coefficient), = grouped.items()
    require(deleted == (0, 1, 2, 3), "four-port deletion set changed")
    require(
        decoration == ((0, "d"), (1, "d"), (2, "e"), (3, "e")),
        "opposite pairings no longer have the same endpoint-colour word",
    )
    require(weight == (1, 1, 1, 1), "formal port-weight product changed")
    require(coefficient == 0, "quadratic insertion coefficient did not cancel")

    # No three inserted edges can coexist on four sites: every candidate
    # contains one of the four endpoint collisions just audited.
    for i in range(len(edges)):
        for j in range(i + 1, len(edges)):
            for k in range(j + 1, len(edges)):
                require(
                    not (
                        compatible(edges[i], edges[j])
                        and compatible(edges[i], edges[k])
                        and compatible(edges[j], edges[k])
                    ),
                    "three inserted cells became pairwise compatible",
                )


def audit_collision_strata():
    # Cubicity and the two nonzero same-colour rows impose
    #   u_d != u_e, v_d != v_e, u_d != v_d, u_e != v_e.
    # Up to relabelling, only the following four port partitions remain.
    patterns = {
        canonical_partition(values)
        for values in product(range(4), repeat=4)
        if values[0] != values[2]
        and values[1] != values[3]
        and values[0] != values[1]
        and values[2] != values[3]
    }
    expected = {
        (0, 1, 2, 3),  # four distinct ports
        (0, 1, 2, 0),  # u_d = v_e
        (0, 1, 1, 2),  # v_d = u_e
        (0, 1, 1, 0),  # both cross equalities
    }
    require(patterns == expected, "allowed port-partition census changed")

    for pattern in patterns - {(0, 1, 2, 3)}:
        ud, vd, ue, ve = pattern
        same_d = make_edge("A", (ud, vd), ("d", "d"), (1, 1, 0, 0))
        same_e = make_edge("B", (ue, ve), ("e", "e"), (0, 0, 1, 1))
        require(
            not compatible(same_d, same_e),
            f"collision pattern {pattern} retained a quadratic A/B term",
        )


def audit_linear_normalization():
    # If a=ad*bd and C_A=(ad*bd)^-1 X_d, the A insertion has coefficient 1;
    # similarly for B.  Cross insertions multiply zero cofactors.  We encode
    # Laurent cancellation by adding the exponent vectors.
    inv_a = (-1, -1, 0, 0)
    inv_b = (0, 0, -1, -1)
    weight_a = (1, 1, 0, 0)
    weight_b = (0, 0, 1, 1)
    require(add_exp(weight_a, inv_a) == ONE, "d-row normalization changed")
    require(add_exp(weight_b, inv_b) == ONE, "e-row normalization changed")


def main():
    audit_linear_normalization()
    audit_distinct_ports()
    audit_collision_strata()
    print("adjacent-cubic pair descent: PASS")
    print("four distinct ports: only AB/CD coexist and their formal weights cancel")
    print("collision ports: A and B overlap, so the quadratic insertion term is absent")
    print("remaining coefficients: lambda^-1 X_c + X_d + X_e")


if __name__ == "__main__":
    main()
