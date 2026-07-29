#!/usr/bin/env python3
"""Exact audit for wedge-equality-coordinate-oriented-obstruction.md.

The arbitrary-tensor crossing-factorization step is a mathematical proof.
This checker independently reconstructs the matching ledger, the cubic
Bianchi identity, the coordinate-row pair census, the final symbolic
Segre minor, and the quotient visibility of the path and triangle types.
"""

from __future__ import annotations

from itertools import combinations, product

import sympy as sp


SITES = tuple("abcdef")
EDGES = tuple("".join(pair) for pair in combinations(SITES, 2))
EDGE_SYMBOLS = sp.symbols(" ".join(EDGES))
Q = dict(zip(EDGES, EDGE_SYMBOLS, strict=True))


def edge(u: str, v: str) -> str:
    return "".join(sorted((u, v)))


def perfect_matchings(vertices: tuple[str, ...]):
    """Return unordered perfect matchings in canonical recursive order."""
    if not vertices:
        return ((),)
    first = vertices[0]
    result = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for matching in perfect_matchings(rest):
            result.append(((first, second),) + matching)
    return tuple(result)


def matching_power(vertices: tuple[str, ...]):
    return sp.expand(
        sum(
            sp.prod(Q[edge(u, v)] for u, v in matching)
            for matching in perfect_matchings(vertices)
        )
    )


def cofactor(missing: str):
    complement = tuple(site for site in SITES if site not in missing)
    return matching_power(complement)


def audit_coordinate_rows():
    p_sites = ("a", "b", "d")
    s_sites = ("b", "c", "e")
    diagonal = tuple(edge(p_sites[i], s_sites[i]) for i in range(3))
    off_diagonal = []
    collisions = []
    for i in range(3):
        for j in range(3):
            if i == j:
                continue
            if p_sites[i] == s_sites[j]:
                collisions.append((i, j, p_sites[i]))
            else:
                off_diagonal.append(edge(p_sites[i], s_sites[j]))
    assert diagonal == ("ab", "bc", "de")
    assert sorted(off_diagonal) == ["ac", "ae", "bd", "be", "cd"]
    assert collisions == [(1, 0, "b")]
    return diagonal, tuple(sorted(off_diagonal)), tuple(collisions)


def audit_matching_ledger():
    assert len(perfect_matchings(SITES)) == 15
    for missing in EDGES:
        assert len(perfect_matchings(tuple(s for s in SITES if s not in missing))) == 3

    hole_zero = {Q["ab"]: 0, Q["bc"]: 0, Q["de"]: 0}
    expected_targets = {
        "ab": Q["cd"] * Q["ef"] + Q["ce"] * Q["df"],
        "bc": Q["ad"] * Q["ef"] + Q["ae"] * Q["df"],
        "de": Q["ac"] * Q["bf"],
    }
    for missing, expected in expected_targets.items():
        actual = sp.expand(cofactor(missing).subs(hole_zero))
        assert sp.expand(actual - expected) == 0

    expected_zeros = {
        "ac": Q["bd"] * Q["ef"] + Q["be"] * Q["df"],
        "ae": Q["bd"] * Q["cf"] + Q["bf"] * Q["cd"],
        "be": Q["ac"] * Q["df"] + Q["ad"] * Q["cf"] + Q["af"] * Q["cd"],
        "bd": Q["ac"] * Q["ef"] + Q["ae"] * Q["cf"] + Q["af"] * Q["ce"],
        "cd": Q["ae"] * Q["bf"] + Q["af"] * Q["be"],
    }
    for missing, expected in expected_zeros.items():
        actual = sp.expand(cofactor(missing).subs(hole_zero))
        assert sp.expand(actual - expected) == 0

    cubic = sp.expand(matching_power(SITES).subs(hole_zero))
    crossing = Q["bf"] * (Q["ad"] * Q["ce"] + Q["ae"] * Q["cd"])
    bianchi = Q["be"] * cofactor("be") + Q["bd"] * cofactor("bd") + crossing
    assert sp.expand(cubic - bianchi.subs(hole_zero)) == 0

    # The eight surviving matchings are also checked without simplification.
    surviving = tuple(
        matching
        for matching in perfect_matchings(SITES)
        if all(edge(u, v) not in {"ab", "bc", "de"} for u, v in matching)
    )
    assert len(surviving) == 8
    return expected_targets, expected_zeros, surviving


def audit_segre_minor():
    xd, xe, yd = sp.symbols("x_d x_e y_d", nonzero=True)
    ye = -xe * yd / xd
    determinant = sp.factor(yd * xe - ye * xd)
    assert sp.factor(determinant - 2 * yd * xe) == 0

    mu0, mu1 = sp.symbols("mu_0 mu_1", nonzero=True)
    coefficient_u0 = sp.factor(xe * mu0 / determinant)
    coefficient_u1 = sp.factor(-ye * mu1 / determinant)
    assert coefficient_u0 != 0
    assert coefficient_u1 != 0

    # Across d | ef, alpha*U0 + beta*U1 has this 2-by-2 diagonal minor.
    flattening_minor = sp.factor(coefficient_u0 * coefficient_u1)
    expected = sp.factor(mu0 * mu1 / (4 * yd * xd))
    assert sp.factor(flattening_minor - expected) == 0
    assert flattening_minor != 0
    return determinant, flattening_minor


def pure_type_solutions(points, target_pairs, zero_pairs):
    """Enumerate P/S purity types after the crossed-target lemma applies."""
    answer = []
    for bits in product(("P", "S"), repeat=len(points)):
        assignment = dict(zip(points, bits, strict=True))
        if any(assignment[left] == assignment[right] for left, right in target_pairs):
            continue
        if any(assignment[left] != assignment[right] for left, right in zero_pairs):
            continue
        answer.append(assignment)
    return answer


def audit_typed_grid_closure():
    triangle_points = ("A0", "A2", "B0", "B1", "C1", "C2")
    triangle_targets = (("A0", "B0"), ("B1", "C1"), ("C2", "A2"))
    triangle_zeros = (
        ("A0", "B1"), ("A2", "B0"), ("A2", "B1"),
        ("B0", "C1"), ("B0", "C2"), ("B1", "C2"),
        ("C1", "A2"), ("C1", "A0"), ("C2", "A0"),
    )
    assert pure_type_solutions(
        triangle_points, triangle_targets, triangle_zeros
    ) == []

    path_points = ("A0", "B0", "B1", "C1", "C2", "D2")
    path_targets = (("A0", "B0"), ("B1", "C1"), ("C2", "D2"))
    path_zeros = (
        ("A0", "B1"),
        ("B0", "C1"), ("B0", "C2"), ("B1", "C2"),
        ("C1", "D2"),
    )
    assert pure_type_solutions(path_points, path_targets, path_zeros) == []

    wedge_points = ("A0", "B0", "B1", "C1")
    wedge_targets = (("A0", "B0"), ("B1", "C1"))
    wedge_zeros = (("A0", "B1"), ("B0", "C1"))
    wedge_solutions = pure_type_solutions(
        wedge_points, wedge_targets, wedge_zeros
    )
    assert len(wedge_solutions) == 2
    for assignment in wedge_solutions:
        assert assignment["A0"] == assignment["B1"]
        assert assignment["B0"] == assignment["C1"]
        assert assignment["A0"] != assignment["C1"]

    # A nonzero point cannot have zero Phi with nonzero P-pure and S-pure
    # points simultaneously.  This is the finite purity consequence used
    # to force F_BD and F_BE to vanish.
    for assignment in wedge_solutions:
        assert {assignment["B0"], assignment["B1"]} == {"P", "S"}
    return len(wedge_solutions)


def main():
    diagonal, zeros, collisions = audit_coordinate_rows()
    targets, zero_expansions, surviving = audit_matching_ledger()
    determinant, minor = audit_segre_minor()
    wedge_type_solutions = audit_typed_grid_closure()
    print("coordinate diagonal pairs:", diagonal)
    print("five literal no-rerouting pairs:", zeros, "collision:", collisions)
    print("surviving cubic matchings:", len(surviving))
    print("target cofactors audited:", tuple(targets))
    print("zero cofactors audited:", tuple(zero_expansions))
    print("coefficient determinant:", determinant)
    print("Segre flattening minor:", minor)
    print("triangle typed-grid purity assignments: 0")
    print("path typed-grid purity assignments: 0")
    print("wedge core purity assignments:", wedge_type_solutions)
    print("conditional wedge coordinate-oriented obstruction: PASS")


if __name__ == "__main__":
    main()
