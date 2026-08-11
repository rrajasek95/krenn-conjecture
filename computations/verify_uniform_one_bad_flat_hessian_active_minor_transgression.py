#!/usr/bin/env python3
"""Route the k=2 flat Hessian circuit to an active physical minor.

The flat response debt is

    gY = D*(Q0*C + Q1*E) = 0,
    S  = Q0*Q1.

Here C=q_12(1,0) is an off-diagonal physical cell.  The genuine unary pure
and one-site mixed rows give the target-augmented private-site identity

    sum_s Delta_2s*K_s = -C.

The exact composition is

    D*E*S = D*Q0^2*sum_s Delta_2s*K_s       modulo gY.

Thus over a domain, after localizing D,E,Q0, every nonzero flat self-square
forces a nonzero determinant/cofactor product.  No Hessian-only inference is
used: the nonzero constant in the unary pure target is indispensable.

The checker also enumerates the genuine eight-site companion word
21000121.  Its pivot is 06:22|12:10|34:00|57:11.  Exactly six of 105
matchings keep both outer endpoint arms axis-purified; besides the pivot,
each of the other five contains a displayed internal off-diagonal cell.
Every one of the remaining 99 contains an off-diagonal outer arm.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_one_bad_axis_hessian_carrier_circuit_boundary.py":
        "1594dcac16bb77bb929c18edda224e215ea99697bfd36edabc4230a0d341b5c8",
    "notes/uniform-one-bad-axis-hessian-carrier-circuit-boundary.md":
        "d784f8d25461ffcdafcc3fb9a39ccc776f770fb63359f722bead4fe7c965e73e",
    "computations/verify_uniform_target_augmented_private_site_active_minor.py":
        "c53ba30dd8b7084cc27e05f11aa6066354fdec45ff2cf72ebdfb85bb8517169b",
    "notes/uniform-target-augmented-private-site-active-minor.md":
        "d7b16ecbb867524615ecf3034e0911e0add34825a7f9088f369f3a11e1c61f0d",
    "computations/verify_h3_one_bad_second_principal_parts_companion_closure.py":
        "3612f9d7c03a3e265792543cd602f27ebf64830390f95b5bddb8d953d238c3f5",
    "computations/verify_h3_one_bad_companion_quadratic_mate_partition.py":
        "b8047fd1e610052fc47fcc0a5e11dd99d582f3ae638ad18825af46d036bc52cb",
}
EXPECTED_LEDGER_SHA256 = (
    "55dd1c7376c370c347353c58b66775f6f9f315b456a9c805b64ef28d4cf2c1ba"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


# Sparse polynomials are Counters indexed by sorted tuples of variable names.
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


def audit_composed_source_identity():
    D, E, S = map(variable, ("D", "E", "S"))
    Q0, Q1, C = map(variable, ("Q0", "Q1", "C"))

    # The literal mixed debt coefficient in the flat C4 packet.  D is the
    # shared q_34(0,0) carrier.  Q0*C and Q1*E are the two matching terms.
    g_y = multiply(D, add(multiply(Q0, C), multiply(Q1, E)))
    square_definition = add(S, scale(multiply(Q0, Q1), -1))

    # Exact source polynomial identity:
    # Q0*gY = D*(E*S+Q0^2*C) - D*E*(S-Q0*Q1).
    left = multiply(Q0, g_y)
    right = add(
        multiply(D, add(multiply(E, S), multiply(Q0, Q0, C))),
        scale(multiply(D, E, square_definition), -1),
    )
    require(left == right,
            "the flat debt/self-square source identity changed")

    # Independently verify the unary private-site identity with four
    # symbolic neighbour columns.  The reference neighbour is 2 and q_2=C.
    neighbours = (2, 3, 4, 5)
    p = {site: variable(f"p{site}") for site in neighbours}
    q = {site: (C if site == 2 else variable(f"q{site}"))
         for site in neighbours}
    k = {site: variable(f"K{site}") for site in neighbours}
    g_pure = add(*(multiply(p[site], k[site]) for site in neighbours),
                 constant(-1))
    g_mixed = add(*(multiply(q[site], k[site]) for site in neighbours))
    private_left = add(multiply(p[2], g_mixed),
                       scale(multiply(C, g_pure), -1))
    active_terms = []
    for site in neighbours:
        delta = add(multiply(p[2], q[site]),
                    scale(multiply(C, p[site]), -1))
        active_terms.append(multiply(delta, k[site]))
    private_right = add(C, *active_terms)
    require(private_left == private_right,
            "the target-augmented private-site identity changed")

    # Modulo gY=0, S=Q0*Q1, and the two exact unary rows, substitute
    # sum(active)=-C into E*S+Q0^2*C=0.
    active_sum = variable("ACTIVE_SUM")
    transgression = add(multiply(D, E, S),
                        scale(multiply(D, Q0, Q0, active_sum), -1))
    expected = add(
        multiply(Q0, g_y),
        multiply(D, E, square_definition),
        scale(multiply(D, Q0, Q0,
                       add(C, active_sum)), -1),
    )
    require(transgression == expected,
            "the composed flat-to-active transgression changed")

    return {
        "flat_mixed_row": "gY=D*(Q0*C+Q1*E)",
        "self_square": "S=Q0*Q1",
        "unary_private_row": "sum_s Delta_2s*K_s=-C",
        "composed_identity": (
            "D*E*S=D*Q0^2*sum_s(Delta_2s*K_s) modulo source rows"
        ),
        "localized_units": ["D", "E", "Q0"],
        "field_consequence": (
            "S!=0 implies some Delta_2s*K_s!=0; S=0 is the concentrated "
            "flat alternative"
        ),
        "source_input_not_hessian": (
            "the +C term comes from the constant -1 in the unary pure "
            "target equation"
        ),
    }


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        remainder = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remainder):
            yield tuple(sorted(((first, second),) + tail))


def partner(matching, site):
    for left, right in matching:
        if left == site:
            return right
        if right == site:
            return left
    raise RuntimeError((matching, site))


def cell_label(edge, word):
    left, right = edge
    return f"{left}{right}:{word[left]}{word[right]}"


def audit_companion_matching_partition():
    word = tuple(map(int, "21000121"))
    matchings = tuple(perfect_matchings(range(8)))
    require(len(matchings) == 105,
            "the eight-site perfect-matching count changed")
    pivot = tuple(sorted(((0, 6), (1, 2), (3, 4), (5, 7))))
    require(pivot in matchings,
            "the physical companion pivot disappeared")

    axis = tuple(matching for matching in matchings
                 if word[partner(matching, 6)] == word[6]
                 and word[partner(matching, 7)] == word[7])
    expected_axis = (
        ((0, 6), (1, 2), (3, 4), (5, 7)),
        ((0, 6), (1, 3), (2, 4), (5, 7)),
        ((0, 6), (1, 4), (2, 3), (5, 7)),
        ((0, 6), (1, 7), (2, 3), (4, 5)),
        ((0, 6), (1, 7), (2, 4), (3, 5)),
        ((0, 6), (1, 7), (2, 5), (3, 4)),
    )
    require(axis == expected_axis,
            f"the axis-preserving companion matchings changed: {axis}")

    axis_mates = []
    for matching in axis:
        off_diagonal = tuple(cell_label(edge, word) for edge in matching
                             if word[edge[0]] != word[edge[1]])
        require(len(off_diagonal) == 1,
                f"an axis matching changed off-diagonal count: {matching}")
        axis_mates.append({
            "matching": [f"{left}{right}" for left, right in matching],
            "off_diagonal_cell": off_diagonal[0],
            "role": "pivot" if matching == pivot else "axis mate",
        })
    require([entry["off_diagonal_cell"] for entry in axis_mates] == [
        "12:10", "13:10", "14:10", "45:01", "35:01", "25:01"
    ], "the six axis off-diagonal cells changed")

    off_axis = tuple(matching for matching in matchings
                     if matching not in set(axis))
    require(len(off_axis) == 99,
            "the off-axis companion count changed")
    for matching in off_axis:
        outer_off_diagonal = []
        for site in (6, 7):
            other = partner(matching, site)
            if word[site] != word[other]:
                outer_off_diagonal.append(cell_label(
                    tuple(sorted((site, other))), word
                ))
        require(outer_off_diagonal,
                f"an off-axis matching lacks an off-diagonal outer arm: {matching}")

    return {
        "word": "21000121",
        "all_matchings": len(matchings),
        "pivot": ["06:22", "12:10", "34:00", "57:11"],
        "axis_preserving_matchings": len(axis),
        "axis_mate_ledger": axis_mates,
        "off_axis_matchings": len(off_axis),
        "off_axis_property": (
            "every matching has an off-diagonal cell incident with site 6 "
            "or 7"
        ),
        "exact_row_consequence": (
            "if the localized pivot is nonzero, the mixed zero coefficient "
            "forces at least one nonzero mate; every mate exposes either an "
            "off-diagonal outer arm or one of five displayed internal "
            "off-diagonal cells"
        ),
    }


def main():
    pin_dependencies()
    ledger = {
        "pins": PINS,
        "flat_to_active_source_identity": audit_composed_source_identity(),
        "physical_companion_partition": audit_companion_matching_partition(),
        "theorem": (
            "in the k=2 axis-flat Hessian normal form, genuine unary target "
            "provenance gives the exact dichotomy: the diagonal-star "
            "self-square vanishes, or a literal determinant/cofactor product "
            "is active; this remains valid after imposing the independent "
            "colour-2 diagonal target and both crossed-zero rows"
        ),
        "colour2_role": (
            "the independent colour-2 target localizes the 06:22 outer "
            "factor in the eight-site companion pivot; the crossed rows make "
            "21000121 a genuine mixed zero row.  The flat-to-active identity "
            "is stronger and already follows before using those extra rows"
        ),
        "remaining_gate": (
            "an active off-diagonal determinant/cofactor product is not yet "
            "a doubly-good curved OO pair; upgrading active-minor incidence "
            "to the certified clean/curved descent remains separate"
        ),
        "scope": (
            "source-polynomial identity and complete matching partition, not "
            "a support-cardinality census; assumes the localized k=2 flat "
            "normal-form factors and does not claim arbitrary k concentration"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"flat Hessian active-minor ledger changed: {digest}")
    print("uniform one-bad flat-Hessian active-minor transgression: PASS")
    print("source identity: D*E*S = D*Q0^2*sum(Delta_2s*K_s)")
    print("companion 21000121: 1 pivot + 5 axis mates + 99 off-axis mates")
    print("every mate contains a literal off-diagonal physical cell")
    print("remaining gate: active determinant/cofactor -> clean/curved OO")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
