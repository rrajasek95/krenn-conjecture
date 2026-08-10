#!/usr/bin/env python3
"""Exact h=3 cofactor tower and the semisimple one-bad boundary.

This checker separates three statements which must not be conflated.

1. For a universal labelled scalar quadratic on six sites, it constructs the
   genuine third/second/first hafnian cofactors and checks every source-labelled
   recurrence J -> G -> H -> q^[3].
2. The four one-bad rows give a perfect C+ C-valued pairing on P x S.  This
   makes P and S dual but gives no nonzero joint-kernel direction inside
   either two-plane.  A site deletion must therefore come from the ambient
   site-filtered kernels, not semisimplicity.
3. Two exact guards pin the missing interaction.  The independent-target
   minimum-response guard has spread p rows but no common q.  Conversely a
   genuine q with q^[3] nonzero and the complete cofactor tower has spread
   p and s rows and a nonzero standard cap tail, but its two target tensors
   collapse to the same scalar top word.  Thus neither half alone proves
   concentration/cleanliness; endpoint-coloured carrier exchange is essential.

No support search and no declared cofactor variables are used.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_one_bad_minimal_response_counterguard.py":
        "57d0a980a26f50bc236f2dcf0b468584a801be049e3cc8cc9418ab0e08ed3b04",
    "notes/uniform-one-bad-minimal-response-counterguard.md":
        "b053f949eef97957c1d53f0c4d4bf1287ca5773a60fd09cbd04fd04c70887dd2",
    "computations/verify_uniform_one_bad_third_cofactor_pure_carrier_gate.py":
        "9f346fd63964802c1286d76a27d6f9dfa2d1382545b44f31f976054310cbcaaf",
    "notes/uniform-one-bad-third-cofactor-pure-carrier-gate.md":
        "9c775dce662938a761f7970b7a7db0cbd7ef401f17045b0b559cf859c5e0a0f1",
}
EXPECTED_LEDGER_SHA256 = (
    "c4ffdc88380b806eff6a913f60cefc360bf0cb3ce1c2655b6ef3cd8c075a762a"
)

SITES = tuple(range(6))
EDGES = tuple(combinations(SITES, 2))
TOP = frozenset(SITES)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def load_module(relative: str, name: str):
    path = ROOT / relative
    specification = importlib.util.spec_from_file_location(name, path)
    require(specification is not None and specification.loader is not None,
            f"cannot load {relative}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"pinned dependency changed: {relative}: {actual}")


# ---------------------------------------------------------------------------
# Universal source-labelled scalar cofactor tower on six sites.
# Polynomials are Counters whose monomials are sorted tuples of q-edge labels.
# ---------------------------------------------------------------------------


def poly_add(*polynomials: Counter) -> Counter:
    answer = Counter()
    for polynomial in polynomials:
        answer.update(polynomial)
    return Counter({term: coefficient for term, coefficient in answer.items()
                    if coefficient})


def poly_scale(polynomial: Counter, scalar: int) -> Counter:
    return Counter({term: scalar * coefficient
                    for term, coefficient in polynomial.items()
                    if scalar * coefficient})


def poly_multiply(left: Counter, right: Counter) -> Counter:
    answer = Counter()
    for left_term, left_coefficient in left.items():
        for right_term, right_coefficient in right.items():
            answer[tuple(sorted(left_term + right_term))] += (
                left_coefficient * right_coefficient
            )
    return Counter({term: coefficient for term, coefficient in answer.items()
                    if coefficient})


def q_variable(edge: tuple[int, int]) -> Counter:
    return Counter({(f"q{edge[0]}{edge[1]}",): 1})


def perfect_matchings(vertices) -> tuple[tuple[tuple[int, int], ...], ...]:
    vertices = tuple(sorted(vertices))
    if not vertices:
        return ((),)
    first = vertices[0]
    output = []
    for second in vertices[1:]:
        remainder = tuple(site for site in vertices if site not in (first, second))
        edge = tuple(sorted((first, second)))
        for tail in perfect_matchings(remainder):
            output.append((edge,) + tail)
    return tuple(output)


def hafnian_polynomial(vertices) -> Counter:
    output = Counter()
    for matching in perfect_matchings(vertices):
        term = Counter({(): 1})
        for edge in matching:
            term = poly_multiply(term, q_variable(edge))
        output = poly_add(output, term)
    return output


def disjoint(first, second) -> bool:
    return not (set(first) & set(second))


def audit_universal_cofactor_tower() -> dict[str, object]:
    top = hafnian_polynomial(SITES)
    require(len(top) == 15 and all(value == 1 for value in top.values()),
            "six-site universal hafnian changed")

    first = {
        edge: hafnian_polynomial(site for site in SITES if site not in edge)
        for edge in EDGES
    }
    second = {}
    third = {}
    for index, edge in enumerate(EDGES):
        for other in EDGES[index + 1:]:
            if not disjoint(edge, other):
                continue
            pair = tuple(sorted((edge, other)))
            complement = tuple(site for site in SITES
                               if site not in set(edge) | set(other))
            second[pair] = hafnian_polynomial(complement)
            remaining_edge = tuple(sorted(complement))
            triple = tuple(sorted((edge, other, remaining_edge)))
            third[triple] = Counter({(): 1})

    require(len(first) == 15 and all(len(value) == 3 for value in first.values()),
            "first-cofactor census changed")
    require(len(second) == 45
            and all(len(value) == 1 for value in second.values()),
            "second-cofactor census changed")
    require(len(third) == 15 and all(value == Counter({(): 1})
                                     for value in third.values()),
            "genuine third cofactors are not the 15 matching units")

    # G_{e,f}=sum_g q_g J_{e,f,g}; at h=3 the complement has exactly one g.
    third_checks = 0
    for pair, g_value in second.items():
        removed = set(pair[0]) | set(pair[1])
        candidates = [edge for edge in EDGES
                      if not (set(edge) & removed)]
        require(len(candidates) == 1, "third-cofactor complement is not unique")
        edge = candidates[0]
        triple = tuple(sorted(pair + (edge,)))
        left = poly_multiply(q_variable(edge), third[triple])
        require(left == g_value, f"third recurrence failed at {pair}")
        third_checks += 1

    # 2H_e=sum_f q_f G_{e,f}; each complementary matching is selected by
    # either of its two edges, hence the exact factor two.
    second_checks = 0
    for edge, h_value in first.items():
        left = Counter()
        for other in EDGES:
            if not disjoint(edge, other):
                continue
            pair = tuple(sorted((edge, other)))
            left = poly_add(left,
                            poly_multiply(q_variable(other), second[pair]))
        require(left == poly_scale(h_value, 2),
                f"second recurrence failed at {edge}")
        second_checks += 1

    # 3q^[3]=sum_e q_e H_e; each perfect matching is marked at one of its
    # three source edges.
    top_left = Counter()
    for edge in EDGES:
        top_left = poly_add(top_left,
                            poly_multiply(q_variable(edge), first[edge]))
    require(top_left == poly_scale(top, 3), "top Euler recurrence failed")

    return {
        "sites": 6,
        "q_cells": len(EDGES),
        "first_cofactors_H": len(first),
        "second_cofactors_G": len(second),
        "third_cofactors_J": len(third),
        "third_recurrence_checks": third_checks,
        "second_recurrence_checks": second_checks,
        "top_recurrence": "sum_e q_e H_e = 3 q^[3]",
        "source_labels_retained": True,
    }


# ---------------------------------------------------------------------------
# Site-square-zero algebra for the sharp genuine scalar counterguard.
# ---------------------------------------------------------------------------


def add_tensors(*tensors: dict[frozenset[int], Q]):
    output = Counter()
    for tensor in tensors:
        output.update(tensor)
    return {support: coefficient for support, coefficient in output.items()
            if coefficient}


def scale_tensor(tensor, scalar):
    return {support: Q(scalar) * coefficient
            for support, coefficient in tensor.items()
            if Q(scalar) * coefficient}


def multiply_tensors(left, right):
    output = Counter()
    for left_support, left_coefficient in left.items():
        for right_support, right_coefficient in right.items():
            if left_support & right_support:
                continue
            output[left_support | right_support] += (
                left_coefficient * right_coefficient
            )
    return {support: coefficient for support, coefficient in output.items()
            if coefficient}


def divided_power(tensor, exponent: int):
    output = {frozenset(): Q(1)}
    for _ in range(exponent):
        output = multiply_tensors(output, tensor)
    denominator = 1
    for value in range(2, exponent + 1):
        denominator *= value
    return scale_tensor(output, Q(1, denominator))


def linear_form(entries):
    return {frozenset((site,)): Q(value)
            for site, value in entries.items() if value}


def bilinear_value(left, cofactor, right):
    return multiply_tensors(multiply_tensors(left, right), cofactor).get(TOP, Q(0))


def audit_genuine_scalar_counterguard() -> dict[str, object]:
    # The perfect-matching quadratic has q^[3]=TOP and its first cofactor
    # pairing is the invertible permutation matrix 0<->1, 2<->3, 4<->5.
    q = {frozenset(edge): Q(1) for edge in ((0, 1), (2, 3), (4, 5))}
    h = divided_power(q, 2)
    require(divided_power(q, 3) == {TOP: Q(1)},
            "genuine scalar q lost its nonzero unary top")

    p1 = linear_form({0: 1, 2: 1})
    p2 = linear_form({1: 1, 4: 1})
    s1 = linear_form({1: 1, 0: 1, 5: -1})
    s2 = linear_form({1: 1, 3: -1, 0: 1})
    p = (p1, p2)
    s = (s1, s2)
    pairing = tuple(tuple(bilinear_value(p_i, h, s_j) for s_j in s)
                    for p_i in p)
    require(pairing == ((Q(1), Q(0)), (Q(0), Q(1))),
            f"semisimple scalar pairing changed: {pairing}")

    squares = {
        "p1^[2]": divided_power(p1, 2),
        "p2^[2]": divided_power(p2, 2),
        "s1^[2]": divided_power(s1, 2),
        "s2^[2]": divided_power(s2, 2),
    }
    require(all(squares.values()), "a spread scalar star became square-zero")

    # Standard permanent-null one-bad response.  The first-order response is
    # diagonal, but the genuine higher cap tail is nonzero.
    response = add_tensors(
        multiply_tensors(p1, s1),
        multiply_tensors(p1, s2),
        scale_tensor(multiply_tensors(p2, s1), -1),
        multiply_tensors(p2, s2),
    )
    r2 = divided_power(response, 2)
    r3 = divided_power(response, 3)
    q_r2 = multiply_tensors(q, r2)
    tail = add_tensors(q_r2, r3)
    require(q_r2 == {TOP: Q(-4)} and r3 == {TOP: Q(-4)}
            and tail == {TOP: Q(-8)},
            "the scalar standard-cap tail changed")

    return {
        "q": ["01", "23", "45"],
        "q^[3]": "TOP",
        "cofactor_pairing": [[str(value) for value in row] for row in pairing],
        "spread_squares": {label: len(value) for label, value in squares.items()},
        "standard_cap_qR2": "-4*TOP",
        "standard_cap_R3": "-4*TOP",
        "standard_cap_tail": "-8*TOP",
        "scope_guard": (
            "both diagonal targets are the same scalar TOP word; this is not "
            "the endpoint-coloured X1/X2 one-bad packet"
        ),
    }


def audit_independent_target_guard() -> dict[str, object]:
    minimal = load_module(
        "computations/verify_uniform_one_bad_minimal_response_counterguard.py",
        "minimal_response_semisimple_boundary",
    )
    audit = minimal.audit_order(3)
    require(audit["response_rows"] == {
        "11": "X1", "12": "0", "21": "0", "22": "X2"
    }, "independent-target response pairing changed")
    require(audit["joint_kernel_columns"] == {
        "p1": ["X1+Y", "-Y"], "p2": ["X2+Z", "-Z"]
    }, "site-component cancellation guard changed")
    require(audit["nonzero_self_squares"] == ["p1^[2]", "p2^[2]"],
            "independent-target guard became concentrated")
    return {
        "pairing": "diag(X1,X2)",
        "p1_site_columns": ["X1+Y", "-Y"],
        "p2_site_columns": ["X2+Z", "-Z"],
        "component_column_rank": 4,
        "nonzero_self_squares": audit["nonzero_self_squares"],
        "scope_guard": "F is formal and is not q^[2] for a common q",
    }


def audit_semisimple_quotient() -> dict[str, object]:
    # In the bases p1,p2 and s1,s2, the maps P -> Hom_A(S,A) and
    # S -> Hom_A(P,A) are represented by the identity.  Their kernels are
    # zero.  Hence semisimplicity supplies duality, not a deletion vector.
    identity = ((Q(1), Q(0)), (Q(0), Q(1)))
    determinant = identity[0][0] * identity[1][1] - identity[0][1] * identity[1][0]
    require(determinant == 1, "semisimple pairing stopped being perfect")

    # Exact four-column site cancellation module of the independent-target
    # guard, on coordinates X1,Y,X2,Z.  Each colour pair has rank two; its
    # target is obtained only by summing both nondeletable columns.
    columns = (
        (1, 1, 0, 0), (0, -1, 0, 0),
        (0, 0, 1, 1), (0, 0, 0, -1),
    )
    matrix = [[Q(column[row]) for column in columns] for row in range(4)]
    determinant_columns = Q(1)
    for pivot_index in range(4):
        pivot = next((row for row in range(pivot_index, 4)
                      if matrix[row][pivot_index]), None)
        require(pivot is not None, "site component matrix lost full rank")
        if pivot != pivot_index:
            matrix[pivot_index], matrix[pivot] = matrix[pivot], matrix[pivot_index]
            determinant_columns = -determinant_columns
        pivot_value = matrix[pivot_index][pivot_index]
        determinant_columns *= pivot_value
        for row in range(pivot_index + 1, 4):
            if not matrix[row][pivot_index]:
                continue
            scalar = matrix[row][pivot_index] / pivot_value
            matrix[row] = [left - scalar * right for left, right in
                           zip(matrix[row], matrix[pivot_index], strict=True)]
    require(abs(determinant_columns) == 1
            and tuple(sum(column[row] for column in columns)
                      for row in range(4)) == (1, 0, 1, 0),
            "site cancellation presentation changed")
    require(all(column != (0, 0, 0, 0) for column in columns),
            "a site component became a joint-kernel deletion")

    return {
        "algebra": "A=C*X1 direct_sum C*X2",
        "pairing_matrix": [[1, 0], [0, 1]],
        "P_to_HomA_S_A_kernel_dimension": 0,
        "S_to_HomA_P_A_kernel_dimension": 0,
        "site_component_presentation_determinant": str(determinant_columns),
        "concentration_criterion": (
            "requires a nonzero ambient site component in N_S={l:l*S*F=0} "
            "or N_P={l:P*l*F=0}; no such vector lies in P or S"
        ),
    }


def main() -> None:
    pin_dependencies()
    ledger = {
        "genuine_h3_cofactor_tower": audit_universal_cofactor_tower(),
        "coordinate_free_semisimple_theorem": audit_semisimple_quotient(),
        "independent_target_formal_guard": audit_independent_target_guard(),
        "genuine_tower_scalar_target_guard": audit_genuine_scalar_counterguard(),
        "verdict": (
            "the h=3 genuine cofactor recurrences plus abstract semisimplicity "
            "do not force one-sided square-zero rows or the standard clean cap; "
            "a proof must use the shared endpoint-coloured word provenance "
            "linking q^[3]=X0 to the distinct X1/X2 carrier fibres"
        ),
        "exact_remaining_map": (
            "carrier exchange must put a nonzero site component into the "
            "ambient joint kernel N_S or N_P, or prove R^[2]=0 directly"
        ),
        "scope": (
            "coordinate-free no-go and complementary sharp guards; not an "
            "endpoint-coloured one-bad source and not a Krenn counterexample"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"semisimple cofactor ledger changed: {digest}")

    print("uniform one-bad semisimple/cofactor boundary: PASS")
    print("h=3 universal tower: 15 H, 45 G, 15 unit J; all recurrences exact")
    print("diag(X1,X2) pairing: perfect; internal joint-kernel dimensions 0/0")
    print("independent targets without common q: spread p rows")
    print("genuine q/top/tower with collapsed target: four spread rows, cap tail -8")
    print("remaining input: endpoint-coloured carrier exchange into ambient joint kernels")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
