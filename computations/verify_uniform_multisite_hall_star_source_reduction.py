#!/usr/bin/env python3
"""Source reduction of the common-centre Hall-star obstruction.

Let the pure diagonal hole families for colours 1 and 2 both lie in the
same physical star with centre c.  Split each pure target coefficient by
which deleted endpoint occupies c.  If the two colours have a common
nonzero side, the corresponding two crossed zero rows have nonzero centre
pivots.  Their cancellation terms necessarily contain off-diagonal star
cells away from c.  Two different cancellation sites are precisely the
distinct-head four-good wedge of the pinned lock theorem.

The exact residuals are (i) both crossed debts concentrated at one common
off-centre site, or (ii) disjoint effective centre sides.  In the latter
case the selected unary and diagonal matchings contain the physical
triangle P-S-c.  This is a symbolic family theorem, not a subset census.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import itertools
import json
from math import prod
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_multisite_endpoint_affine_hall_concentration_boundary.py":
        "f24e9bd69ec4baef96104557571c154b399f87f34074edffda27e551f33c2205",
    "notes/uniform-multisite-endpoint-affine-hall-concentration-boundary.md":
        "241b46d9ecede656aa59f2be6d74bc288fbada2aa4843103a950441066763df2",
    "computations/verify_uniform_five_lock_wedge_or_switch.py":
        "c2541a60db1f8e7a661bc698d2bd1f1a1f396a0f0bfde389ea89bea17fac175e",
    "notes/uniform-five-lock-wedge-or-switch.md":
        "0871d5151a0fdb46fee0c9b15797a864e579a85c360a2638d458583479426914",
    "computations/verify_uniform_one_bad_nonanchor_offdiagonal_good_pair.py":
        "64e85cd84112b5160efe4f43ce1208da3c49f5e58b3e4a4d6192e6a9c229c306",
    "notes/uniform-one-bad-nonanchor-offdiagonal-good-pair.md":
        "4516c5ff02f130e1ad25b4fde395c81557e58ba0c83f7f98969d95df17fd6409",
    "computations/verify_uniform_target_augmented_private_site_active_minor.py":
        "c53ba30dd8b7084cc27e05f11aa6066354fdec45ff2cf72ebdfb85bb8517169b",
    "notes/uniform-target-augmented-private-site-active-minor.md":
        "d7b16ecbb867524615ecf3034e0911e0add34825a7f9088f369f3a11e1c61f0d",
}
EXPECTED_LEDGER_SHA256 = "bc484624f80803e7df024c0a727128d79c8516aebde56fec8eca5ae3e802b4f7"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


# Sparse polynomials over Q, indexed by sorted tuples of variable labels.
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


def audit_star_orientation_dichotomy():
    """Nonempty effective side sets either meet or are opposite singletons."""
    sides = frozenset(("P", "S"))
    nonempty = (frozenset(("P",)), frozenset(("S",)), sides)
    histogram = Counter()
    for first, second in itertools.product(nonempty, repeat=2):
        common = first & second
        if common:
            histogram["common_effective_side"] += 1
            continue
        require(len(first) == len(second) == 1 and first | second == sides,
                "disjoint effective orientations stopped being opposite")
        histogram["opposite_singletons"] += 1
    require(histogram == Counter({
        "common_effective_side": 7,
        "opposite_singletons": 2,
    }), f"the effective-orientation split changed: {histogram}")
    return dict(histogram)


def audit_crossed_source_identities():
    """Verify the two ordinary target-augmented identities on a pure side."""
    a1, a2 = variable("a1"), variable("a2")
    u1, u2 = variable("U1"), variable("U2")
    tails12 = [multiply(variable(f"x12_{site}"),
                        variable(f"C12_{site}")) for site in range(3)]
    tails21 = [multiply(variable(f"x21_{site}"),
                        variable(f"C21_{site}")) for site in range(3)]
    g11 = add(multiply(a1, u1), constant(-1))
    g22 = add(multiply(a2, u2), constant(-1))
    g12 = add(multiply(a1, u2), *tails12)
    g21 = add(multiply(a2, u1), *tails21)

    identity12 = add(multiply(a2, g12), scale(multiply(a1, g22), -1))
    expected12 = add(a1, *(multiply(a2, tail) for tail in tails12))
    require(identity12 == expected12,
            "the 12 target-augmented star identity changed")
    identity21 = add(multiply(a1, g21), scale(multiply(a2, g11), -1))
    expected21 = add(a2, *(multiply(a1, tail) for tail in tails21))
    require(identity21 == expected21,
            "the 21 target-augmented star identity changed")

    # The co-located guard satisfies both diagonal targets and both crossed
    # zero coefficients, showing that these scalar identities alone do not
    # separate the two active sites.  It is deliberately not a full packet.
    values = {
        "a1": Q(1), "a2": Q(1), "U1": Q(1), "U2": Q(1),
        "x12_0": Q(1), "C12_0": Q(-1),
        "x21_0": Q(1), "C21_0": Q(-1),
    }

    def evaluate(polynomial):
        return sum(coefficient * prod(values.get(name, Q(0))
                                      for name in term)
                   for term, coefficient in polynomial.items())

    require(all(evaluate(generator) == 0
                for generator in (g11, g22, g12, g21)),
            "the co-located crossed-debt guard changed")
    return {
        "ordinary_identity_12":
            "a2*g12-a1*g22=a1+a2*sum_u(x12_u*C12_u)",
        "ordinary_identity_21":
            "a1*g21-a2*g11=a2+a1*sum_u(x21_u*C21_u)",
        "domain_consequence": (
            "on a common effective P side, both off-centre active sets "
            "{u:x12_u*C12_u!=0} and {u:x21_u*C21_u!=0} are nonempty"
        ),
        "s_side": "the identical formulas hold after P<->S",
        "sharp_scalar_guard":
            "both active sums may be supported at one common site",
    }


def perfect_matching(*edges):
    flattened = [site for edge in edges for site in edge]
    require(len(flattened) == len(set(flattened)),
            f"not a physical matching: {edges}")
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


def endpoint_anchor_rank(matchings, deleted_pair, endpoint):
    """Rank of the three selected matching columns after deleting a pair."""
    other = deleted_pair[0] if endpoint == deleted_pair[1] else deleted_pair[1]
    labels = []
    for colour, matching in enumerate(matchings):
        require(tuple(sorted(deleted_pair)) not in matching,
                "a claimed off-anchor pair lies in a selected matching")
        neighbour = partner(matching, endpoint)
        require(neighbour != other, "the selected column was deleted")
        labels.append((neighbour, colour))
    basis = {label: index for index, label in enumerate(sorted(set(labels)))}
    matrix = [[Q(1) if basis[label] == row else Q(0)
               for label in labels] for row in range(len(basis))]
    return rank(matrix)


def audit_free_wedge_and_triangle():
    # The rank argument is independent of the matching geometry beyond
    # avoidance of the reselected pair.  At either endpoint the three
    # surviving columns have labels (neighbour_0,0), (neighbour_1,1),
    # (neighbour_2,2).  They remain distinct even when neighbours repeat.
    for neighbours in itertools.product(range(3), repeat=3):
        labels = tuple((neighbours[colour], colour) for colour in range(3))
        require(len(set(labels)) == 3,
                "distinct colours stopped separating anchor columns")
        require(rank([[Q(row == column) for column in range(3)]
                      for row in range(3)]) == 3,
                "the uniform three-colour endpoint rank changed")

    # P=6, S=7, common residual centre c=0.  In the same-P orientation,
    # Q1 and Q2 both use P-c; Q0 uses the normalized unary direct P-S.
    q0 = perfect_matching((6, 7), (0, 1), (2, 3), (4, 5))
    q1_same = perfect_matching((6, 0), (7, 1), (2, 4), (3, 5))
    q2_same = perfect_matching((6, 0), (7, 2), (1, 3), (4, 5))
    same_matchings = (q0, q1_same, q2_same)
    first_pair, second_pair = (6, 3), (6, 4)
    ranks = tuple(endpoint_anchor_rank(same_matchings, pair, endpoint)
                  for pair in (first_pair, second_pair)
                  for endpoint in pair)
    require(ranks == (3, 3, 3, 3),
            f"the off-anchor four-good ranks changed: {ranks}")

    # Opposite effective sides select P-c in colour 1 and S-c in colour 2;
    # with the unary direct edge this is the literal three-colour triangle.
    q2_opposite = perfect_matching((7, 0), (6, 2), (1, 4), (3, 5))
    triangle = {
        tuple(sorted((6, 7))): 0,
        tuple(sorted((6, 0))): 1,
        tuple(sorted((7, 0))): 2,
    }
    require(all(edge in matching
                for edge, matching in zip(triangle, (q0, q1_same, q2_opposite),
                                          strict=True)),
            "the opposite-side selected-anchor triangle changed")
    return {
        "distinct_active_sites": {
            "pairs": ["P-u", "P-v"],
            "deleted_star_ranks": list(ranks),
            "centre_heads": ["e1", "e2"],
            "landing": "pinned distinct-head four-good wedge",
            "uniform_rank_reason": (
                "at either endpoint of any off-anchor pair, Q_c contributes "
                "the undeleted column (neighbour_c,c); the colour labels "
                "c=0,1,2 make these three columns independent even when "
                "physical neighbours repeat"
            ),
        },
        "coincident_active_sites":
            "one off-anchor pair P-u carries both ordered off-diagonal debts",
        "opposite_effective_sides": {
            "selected_anchor_edges": ["P-S:0", "P-c:1", "S-c:2"],
            "normal_form": "three-colour outer-centre triangle",
        },
    }


def main():
    pin_dependencies()
    ledger = {
        "effective_orientation_dichotomy":
            audit_star_orientation_dichotomy(),
        "crossed_source_identities": audit_crossed_source_identities(),
        "physical_landing": audit_free_wedge_and_triangle(),
        "theorem": (
            "for a common-centre Hall star, a common effective endpoint "
            "side forces nonempty active 12 and 21 off-centre carrier "
            "sets.  Distinct carrier sites give the certified four-good "
            "wedge without modifying coefficients"
        ),
        "representative_dichotomy": (
            "for nonempty active-site sets A12,A21, either choose u in A12 "
            "and v in A21 with u!=v, or every cross-pair is equal; in the "
            "latter case A12=A21={u}"
        ),
        "sharp_residuals": [
            "both ordered active carrier sets are concentrated at one "
            "common off-centre site (a co-located bidirectional C4 lock)",
            "the effective centre sides are opposite, so the three selected "
            "pure anchors contain P-S-c with colours 0,1,2",
        ],
        "source_inputs": (
            "the diagonal rows certify nonzero effective centre factors; "
            "both crossed zero rows force the two active debts; the unary "
            "top supplies Q0 and makes every off-centre P-u (or S-u) pair "
            "off the selected anchor union"
        ),
        "scope": (
            "uniform source-labelled family reduction, not a full one-bad "
            "counterexample and not line-hitting in the two residual normal "
            "forms; triangle and K2,2 Hall families remain separate"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"Hall-star source ledger changed: {digest}")
    print("uniform multisite Hall-star source reduction: PASS")
    print("common effective side -> two nonempty off-anchor active sets")
    print("distinct active sites -> ranks (3,3,3,3), distinct heads")
    print("residuals: co-located bidirectional lock or anchor triangle")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
