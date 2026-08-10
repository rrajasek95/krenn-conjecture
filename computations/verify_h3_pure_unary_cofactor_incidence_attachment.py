#!/usr/bin/env python3
r"""Pure-unary cofactor filtration at the h=3 conormal gate.

For the universal six-site scalar quadratic q, put H=q^[3], F0=H-u,
and retain the genuine source-labelled cofactors

    H_e       (first, degree 2),
    G_{e,f}   (second, degree 1),
    J_{e,f,g} (third, degree 0, equal to 1 on a perfect matching).

The exact Euler layers give

    3 F0 - sum_e q_e H_e                         = -3u,
    3 F0 - sum_{e<f disjoint} q_e q_f G_{e,f}   = -3u,
      F0 - sum_M q_M J_M                        = -u.

The internal-edge quotient detects every first/second expression by its
nonzero u residue.  A third cofactor is the first polynomial source-labelled
cofactor capable of cancelling it:

    3 F0 - sum_e q_e H_e + 3u J_M = 0.

This is an exact polynomial identity, not by itself a physical lower-face
chain.  A positive source proof must realize u J_M with zero w/target/ores;
declaring that chain would assume the remaining attachment.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_one_bad_semisimple_cofactor_tower_boundary.py":
        "5b6ae90480611c6b1f87d049f404d1e61bde4a93a3af3779c42d749de453c1fe",
    "notes/uniform-one-bad-semisimple-cofactor-tower-boundary.md":
        "43402aa2051086aedacfd04cfc5f9d3e155471946beffafaddc4617f33d59283",
    "computations/verify_h3_signed_circuit_conormal_transport_no_go.py":
        "fdcc5c663e5ad8c9680838301957e03db2ff124fd0d1d4b5a8bc1f7395a922a0",
    "notes/h3-signed-circuit-conormal-transport-no-go.md":
        "bb9ee5c4e63da79a49e27d2b6e2cc4819641b3f52efdd9f9749a747bfcb5544f",
    "computations/verify_h3_source_base_change_conormal_obstruction.py":
        "1a921671ab378f68355c2a6196d1951cad30244d78a9e90ec2715ce47ef12bf0",
    "notes/h3-source-base-change-conormal-obstruction.md":
        "550d1fdea1127d1771191057207b6b2bb6cb97edd3309c90f230d87631f401cd",
}
EXPECTED_LEDGER_SHA256 = "428935f1f9b4f084710a5e6bc6f3f69b2baf873b82b79669cfe30e5bd170001a"

SITES = tuple(range(6))
EDGES = tuple(combinations(SITES, 2))
U = "u"
ZERO = Q(0)

Polynomial = Counter[tuple[str, ...]]


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def add(*polynomials: Polynomial) -> Polynomial:
    answer: Polynomial = Counter()
    for polynomial in polynomials:
        answer.update(polynomial)
    return Counter({monomial: coefficient
                    for monomial, coefficient in answer.items()
                    if coefficient})


def scale(value, polynomial: Polynomial) -> Polynomial:
    value = Q(value)
    return Counter({monomial: value * coefficient
                    for monomial, coefficient in polynomial.items()
                    if value * coefficient})


def multiply(*polynomials: Polynomial) -> Polynomial:
    answer: Polynomial = Counter({(): Q(1)})
    for polynomial in polynomials:
        output: Polynomial = Counter()
        for left, left_coefficient in answer.items():
            for right, right_coefficient in polynomial.items():
                output[tuple(sorted(left + right))] += (
                    left_coefficient * right_coefficient
                )
        answer = Counter({monomial: coefficient
                          for monomial, coefficient in output.items()
                          if coefficient})
    return answer


def variable(name: str) -> Polynomial:
    return Counter({(name,): Q(1)})


def edge_name(edge: tuple[int, int]) -> str:
    return f"q{edge[0]}{edge[1]}"


def q_edge(edge: tuple[int, int]) -> Polynomial:
    return variable(edge_name(edge))


def perfect_matchings(vertices) -> tuple[tuple[tuple[int, int], ...], ...]:
    vertices = tuple(sorted(vertices))
    if not vertices:
        return ((),)
    first = vertices[0]
    result = []
    for second in vertices[1:]:
        remainder = tuple(site for site in vertices
                          if site not in (first, second))
        edge = tuple(sorted((first, second)))
        for tail in perfect_matchings(remainder):
            result.append((edge,) + tail)
    return tuple(result)


def hafnian(vertices) -> Polynomial:
    output: Polynomial = Counter()
    for matching in perfect_matchings(vertices):
        output = add(output, multiply(*(q_edge(edge) for edge in matching)))
    return output


def disjoint(first, second) -> bool:
    return not (set(first) & set(second))


def internal_edge_quotient(polynomial: Polynomial) -> Polynomial:
    return Counter({monomial: coefficient
                    for monomial, coefficient in polynomial.items()
                    if all(item == U for item in monomial)})


def u_coefficient(polynomial: Polynomial) -> Q:
    return polynomial.get((U,), ZERO)


def degree_set(polynomial: Polynomial):
    return {sum(item != U for item in monomial)
            for monomial in polynomial}


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"pinned dependency changed: {relative}")


def cofactor_tower_audit():
    top = hafnian(SITES)
    matchings = perfect_matchings(SITES)
    require(len(matchings) == 15 and len(top) == 15
            and degree_set(top) == {3},
            "six-site unary hafnian changed")
    first = {
        edge: hafnian(site for site in SITES if site not in edge)
        for edge in EDGES
    }
    second = {}
    third = {}
    for edge_index, edge in enumerate(EDGES):
        for other in EDGES[edge_index + 1:]:
            if not disjoint(edge, other):
                continue
            pair = tuple(sorted((edge, other)))
            remaining = tuple(site for site in SITES
                              if site not in set(edge) | set(other))
            second[pair] = hafnian(remaining)
            complement = tuple(sorted(remaining))
            triple = tuple(sorted((edge, other, complement)))
            third[triple] = Counter({(): Q(1)})
    require(len(first) == 15 and all(degree_set(value) == {2}
                                     for value in first.values()),
            "first cofactors lost degree two")
    require(len(second) == 45 and all(degree_set(value) == {1}
                                      for value in second.values()),
            "second cofactors lost degree one")
    require(len(third) == 15 and all(value == Counter({(): Q(1)})
                                     for value in third.values()),
            "third cofactors stopped being matching units")

    first_euler: Polynomial = Counter()
    for edge, cofactor in first.items():
        first_euler = add(first_euler, multiply(q_edge(edge), cofactor))
    require(first_euler == scale(3, top),
            "first-cofactor Euler recurrence changed")

    second_euler: Polynomial = Counter()
    for (edge, other), cofactor in second.items():
        second_euler = add(
            second_euler,
            multiply(q_edge(edge), q_edge(other), cofactor),
        )
    require(second_euler == scale(3, top),
            "second-cofactor Euler recurrence changed")

    third_euler: Polynomial = Counter()
    for matching in matchings:
        triple = tuple(sorted(matching))
        third_euler = add(
            third_euler,
            multiply(*(q_edge(edge) for edge in matching), third[triple]),
        )
    require(third_euler == top,
            "third-cofactor matching recurrence changed")

    f0 = add(top, scale(-1, variable(U)))
    first_residual = add(scale(3, f0), scale(-1, first_euler))
    second_residual = add(scale(3, f0), scale(-1, second_euler))
    third_residual = add(f0, scale(-1, third_euler))
    require(first_residual == second_residual
            == Counter({(U,): Q(-3)}),
            "first/second Euler residue stopped being -3u")
    require(third_residual == Counter({(U,): Q(-1)}),
            "third matching residue stopped being -u")

    selected_matching = tuple(sorted(matchings[0]))
    unit_third = third[selected_matching]
    first_closed = add(first_residual,
                       scale(3, multiply(variable(U), unit_third)))
    second_closed = add(second_residual,
                        scale(3, multiply(variable(U), unit_third)))
    third_closed = add(third_residual,
                       multiply(variable(U), unit_third))
    require(not first_closed and not second_closed and not third_closed,
            "third cofactor failed to close an Euler residue")

    # The internal-edge quotient is the exact separator.  It kills H and
    # every first/second cofactor with arbitrary polynomial multipliers that
    # do not invert an internal edge, but sees u*J_M=u.
    require(not internal_edge_quotient(top)
            and all(not internal_edge_quotient(value)
                    for value in first.values())
            and all(not internal_edge_quotient(value)
                    for value in second.values()),
            "a lower cofactor escaped the internal-edge ideal")
    require(internal_edge_quotient(unit_third) == unit_third,
            "third unit vanished in the internal-edge quotient")
    require(u_coefficient(first_residual) == -3
            and u_coefficient(second_residual) == -3,
            "u-incidence separator changed")

    # Conditional localization guard: at a live matching, G_{e,f}=q_g.
    # Inverting q_g makes the second cofactor a unit.  This is algebraically
    # sufficient but is not a polynomial lower-face construction.
    edge, other, complement = selected_matching
    pair = tuple(sorted((edge, other)))
    require(second[pair] == q_edge(complement),
            "selected second cofactor is not its complementary cell")

    return {
        "top_matching_terms": len(top),
        "first_cofactors": len(first),
        "second_cofactors": len(second),
        "third_cofactors": len(third),
        "edge_degrees": {"H": 3, "H_e": 2, "G_ef": 1, "J_efg": 0},
        "first_Euler": "sum_e q_e H_e=3H",
        "second_Euler": "sum_{e<f disjoint}q_e q_f G_ef=3H",
        "third_matching": "sum_M q_M J_M=H",
        "first_residual": "3F0-sum_e q_e H_e=-3u",
        "second_residual": "3F0-sum_ef q_e q_f G_ef=-3u",
        "closed_identity": (
            "3F0-sum_e q_e H_e+3u J_M=0 for every perfect matching M"
        ),
        "first_polynomially_capable_order": 3,
        "selected_matching": [list(edge) for edge in selected_matching],
        "localized_second_guard": (
            "G_ef=q_g; after inverting the complementary live cell q_g, "
            "q_g^-1 G_ef=1, but no polynomial/source lower face is created"
        ),
    }


def two_chart_euler_audit():
    # Coordinates are the two u-incidence residuals and the desired
    # normalized attachment.  Each first/second Euler packet has residual
    # (-3u) on its chart; a Bianchi difference is (-1,+1,0).  Normalizing by
    # -3 gives exactly the anchor-number module of e96482a.
    chart_d = (Q(1), Q(0), Q(1))
    chart_l = (Q(0), Q(1), Q(1))
    bianchi = (Q(-1), Q(1), Q(0))
    separator = (Q(1), Q(1), Q(-1))
    desired = (Q(0), Q(0), Q(1))
    require(all(sum(x * y for x, y in zip(separator, row, strict=True)) == 0
                for row in (chart_d, chart_l, bianchi)),
            "cofactor Euler/Bianchi separator changed")
    require(sum(x * y for x, y in zip(separator, desired, strict=True)) == -1,
            "desired attachment entered the lower-cofactor Bianchi span")
    return {
        "normalized_chart_D": ["1", "0", "1"],
        "normalized_chart_L": ["0", "1", "1"],
        "Bianchi_L_minus_D": ["-1", "1", "0"],
        "separator": ["1", "1", "-1"],
        "desired_pairing": "-1",
    }


def main() -> None:
    pin_dependencies()
    tower = cofactor_tower_audit()
    bianchi = two_chart_euler_audit()
    ledger = {
        "pins": PINS,
        "pure_unary_cofactor_tower": tower,
        "two_chart_Euler_Bianchi": bianchi,
        "physical_scope": {
            "proved_identity": (
                "the third matching cofactor supplies the first exact "
                "degree-zero coefficient capable of cancelling [F0]"
            ),
            "not_constructed": (
                "a chain realizing u*J_M with zero w, target, and ordinary "
                "residue in the underived full-nine/two-chart module"
            ),
            "first_and_second_rows": (
                "remain separated by internal-edge degree; their physical "
                "response companions are target-zero and contain no u"
            ),
        },
        "verdict": (
            "first/second pure cofactors do not supply the polynomial "
            "incidence attachment; the genuine third cofactor J_M=1 is "
            "the first capable source coefficient and names the minimal "
            "new lower-face type"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"pure-unary cofactor ledger changed: {digest}")
    print("h=3 pure-unary cofactor incidence audit: PASS")
    print("first/second Euler residual: -3u")
    print("internal-edge quotient separates all first/second cofactors")
    print("third cofactor J_M=1 closes the exact Euler identity")
    print("first polynomially capable cofactor order: 3")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
