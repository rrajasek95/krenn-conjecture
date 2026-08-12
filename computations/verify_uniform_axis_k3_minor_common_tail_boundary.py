#!/usr/bin/env python3
"""Physical boundary of the first nonzero minor in a minimum k=3 circuit.

Three independent complete response columns summing with nonzero weights to
one target have quotient rank two.  Hence two literal mixed coefficient rows
have a nonzero 2 by 2 minor.  Expanding that minor in genuine common-q
matching tails gives pairs of perfect matchings on the augmented eight-site
set.

If a selected pair differs by one C4, has the same decorated tail, and the
opposite determinant orientation supplies the switched pairing with those
same decorations, its contribution is the common-tail alternating-C4
minor.  Independently, whenever one of its cells is a typed off-diagonal
reference cell, the target-augmented pure/mixed source rows give the ordinary
identity

    p_u G_mixed - q_u G_pure
      = q_u + (p_u q_s-q_u p_s) C_s.

Thus an off-diagonal reference cell q_u forces a literal active carrier
Delta_us C_s.  The first topology not covered is an unequal determinant
tail: C6, C8, two independent C4 components, or absence of the switched
cross orientation with the same decorated tail.  Even on a complete single
C4, a coordinate-diagonal label change is a separate diagonal-web boundary.
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
    "computations/verify_uniform_one_bad_axis_hessian_carrier_circuit_boundary.py":
        "1594dcac16bb77bb929c18edda224e215ea99697bfd36edabc4230a0d341b5c8",
    "notes/uniform-one-bad-axis-hessian-carrier-circuit-boundary.md":
        "d784f8d25461ffcdafcc3fb9a39ccc776f770fb63359f722bead4fe7c965e73e",
    "computations/verify_uniform_target_augmented_private_site_active_minor.py":
        "c53ba30dd8b7084cc27e05f11aa6066354fdec45ff2cf72ebdfb85bb8517169b",
    "notes/uniform-target-augmented-private-site-active-minor.md":
        "d7b16ecbb867524615ecf3034e0911e0add34825a7f9088f369f3a11e1c61f0d",
    "computations/verify_uniform_multisite_endpoint_affine_hall_concentration_boundary.py":
        "f24e9bd69ec4baef96104557571c154b399f87f34074edffda27e551f33c2205",
    "notes/uniform-multisite-endpoint-affine-hall-concentration-boundary.md":
        "241b46d9ecede656aa59f2be6d74bc288fbada2aa4843103a950441066763df2",
}
EXPECTED_LEDGER_SHA256 = (
    "b946af6d2769f985fe04926039399e61f3a692f12fc923824df0b4f2c9ef2cb9"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def rank(matrix):
    work = [[Q(value) for value in row] for row in matrix]
    if not work:
        return 0
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next((row for row in range(pivot_row, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [entry - value * pivot_entry
                         for entry, pivot_entry
                         in zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def audit_k3_normal_form():
    # After a change of output basis and rescaling the three occupied
    # components, every minimum k=3 circuit has this response-column form.
    # The first row is the target coordinate; the last two are literal mixed
    # coefficient coordinates chosen from a nonzero quotient minor.
    columns = (
        (Q(1), Q(1), Q(0)),
        (Q(0), Q(-1), Q(1)),
        (Q(0), Q(0), Q(-1)),
    )
    target = (Q(1), Q(0), Q(0))
    summed = tuple(sum(column[row] for column in columns)
                   for row in range(3))
    require(summed == target, "the canonical k3 columns stopped summing")
    matrix = [[column[row] for column in columns] for row in range(3)]
    require(rank(matrix) == 3, "the canonical k3 columns lost independence")
    quotient = matrix[1:]
    require(rank(quotient) == 2, "the target quotient stopped having rank 2")
    minors = {
        (left, right): (quotient[0][left] * quotient[1][right]
                        - quotient[0][right] * quotient[1][left])
        for left, right in combinations(range(3), 2)
    }
    require(any(minors.values()), "every literal mixed 2 by 2 minor vanished")
    require(not any(
        all(column[row] == 0 for row in (1, 2)) for column in columns
    ), "an occupied minimum-circuit column entered the target line")
    return {
        "complete_column_rank": 3,
        "target_quotient_rank": 2,
        "occupied_target_line_columns": 0,
        "mixed_row_minors": {
            f"{left}{right}": str(value)
            for (left, right), value in sorted(minors.items())
        },
        "general_reason": (
            "span(C0,C1,C2)/<T> has dimension 2; the nonzero star weights "
            "give its unique full-support relation, so no occupied column "
            "projects to zero and some two literal coefficient rows have a "
            "nonzero 2 by 2 minor"
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


def alternating_components(first, second):
    edges = set(first) ^ set(second)
    adjacency = {}
    for left, right in edges:
        adjacency.setdefault(left, []).append(right)
        adjacency.setdefault(right, []).append(left)
    unseen = set(adjacency)
    lengths = []
    while unseen:
        start = next(iter(unseen))
        previous = None
        current = start
        length = 0
        while True:
            unseen.discard(current)
            length += 1
            neighbours = adjacency[current]
            require(len(neighbours) == 2,
                    "a perfect-matching difference stopped being cycles")
            following = (neighbours[0] if neighbours[0] != previous
                         else neighbours[1])
            previous, current = current, following
            if current == start:
                break
        lengths.append(length)
    return tuple(sorted(lengths))


def audit_matching_tail_topology():
    matchings = tuple(perfect_matchings(range(8)))
    require(len(matchings) == 105, "the eight-site matching count changed")
    histogram = Counter(
        alternating_components(first, second)
        for first, second in combinations(matchings, 2)
    )
    expected = Counter({
        (4,): 630,
        (6,): 1680,
        (8,): 2520,
        (4, 4): 630,
    })
    require(histogram == expected,
            f"the alternating-tail histogram changed: {histogram}")

    # A single C4 is exactly the common-physical-tail case: the matchings
    # share the other two edges.  Longer cycles and C4+C4 have no common
    # four-site cofactor tail on which the private-site determinant can be
    # read without another source exchange.
    for first, second in combinations(matchings, 2):
        components = alternating_components(first, second)
        shared = set(first) & set(second)
        if components == (4,):
            require(len(shared) == 2,
                    "a one-C4 pair lost its two-edge common tail")
        else:
            require(len(shared) < 2,
                    "an unequal-tail pair acquired a full common tail")
    return {
        "perfect_matchings": len(matchings),
        "unordered_distinct_pairs": sum(histogram.values()),
        "alternating_component_histogram": {
            "+".join(map(str, key)): value
            for key, value in sorted(histogram.items())
        },
        "single_c4_common_tail_pairs": histogram[(4,)],
        "first_unequal_tail_pairs": (
            histogram[(6,)] + histogram[(8,)] + histogram[(4, 4)]
        ),
    }


# Sparse commutative polynomials used only to expand the ordinary source
# identity.  A monomial is a sorted tuple of variable names.
def variable(name):
    return Counter({(name,): Q(1)})


def constant(value):
    return Counter({(): Q(value)}) if value else Counter()


def add(*terms):
    answer = Counter()
    for polynomial, scalar in terms:
        for monomial, coefficient in polynomial.items():
            answer[monomial] += Q(scalar) * coefficient
    return Counter({monomial: coefficient for monomial, coefficient
                    in answer.items() if coefficient})


def multiply(*polynomials):
    answer = constant(1)
    for polynomial in polynomials:
        updated = Counter()
        for left, left_coefficient in answer.items():
            for right, right_coefficient in polynomial.items():
                updated[tuple(sorted(left + right))] += (
                    left_coefficient * right_coefficient
                )
        answer = Counter({monomial: coefficient for monomial, coefficient
                          in updated.items() if coefficient})
    return answer


def audit_typed_common_tail_identity():
    p_u, p_s, q_u, q_s, c_u, c_s = map(
        variable, ("p_u", "p_s", "q_u", "q_s", "C_u", "C_s")
    )
    g_pure = add((multiply(p_u, c_u), 1),
                 (multiply(p_s, c_s), 1),
                 (constant(1), -1))
    g_mixed = add((multiply(q_u, c_u), 1),
                  (multiply(q_s, c_s), 1))
    left = add((multiply(p_u, g_mixed), 1),
               (multiply(q_u, g_pure), -1))
    delta = add((multiply(p_u, q_s), 1),
                (multiply(q_u, p_s), -1))
    right = add((q_u, 1), (multiply(delta, c_s), 1))
    require(left == right,
            "the target-augmented common-tail identity changed")

    # This factorization is available only if the opposite determinant
    # orientation contains the switched pairing with the same decorations.
    tail, x_ab, x_cd, x_ac, x_bd = map(
        variable, ("TAIL", "x_ab", "x_cd", "x_ac", "x_bd")
    )
    c4_minor = multiply(tail, add(
        (multiply(x_ab, x_cd), 1),
        (multiply(x_ac, x_bd), -1),
    ))
    expanded = add(
        (multiply(tail, x_ab, x_cd), 1),
        (multiply(tail, x_ac, x_bd), -1),
    )
    require(c4_minor == expanded,
            "the common-tail alternating-C4 factorization changed")

    label_types = Counter(
        "typed_offdiagonal" if pure != mixed else "diagonal_web"
        for pure in range(3) for mixed in range(3)
    )
    require(label_types == Counter({
        "typed_offdiagonal": 6, "diagonal_web": 3,
    }), "the ternary common-tail typing split changed")
    return {
        "source_rows": [
            "G_pure=p_u*C_u+p_s*C_s-1",
            "G_mixed=q_u*C_u+q_s*C_s",
        ],
        "ordinary_identity": (
            "p_u*G_mixed-q_u*G_pure="
            "q_u+(p_u*q_s-q_u*p_s)*C_s"
        ),
        "source_consequence": (
            "q_u!=0 forces the literal active carrier "
            "(p_u*q_s-q_u*p_s)*C_s!=0"
        ),
        "alternating_c4_factorization": (
            "TAIL*(x_ab*x_cd-x_ac*x_bd), conditional on the switched "
            "determinant orientation having the same decorated TAIL"
        ),
        "ternary_label_split": dict(label_types),
        "first_label_obstruction": (
            "the cycle is coordinate-diagonal, so the two full words do "
            "not give a typed pure/mixed private-site comparison"
        ),
    }


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def main():
    pin_dependencies()
    ledger = {
        "pins": PINS,
        "minimum_k3_minor": audit_k3_normal_form(),
        "physical_matching_tail_topology": audit_matching_tail_topology(),
        "typed_common_tail_source_route": audit_typed_common_tail_identity(),
        "theorem": (
            "the first nonzero mixed 2 by 2 minor of a minimum k3 complete-"
            "column circuit has a source-valid active-minor landing whenever "
            "one selected common-q monomial pair and its opposite determinant "
            "orientation form a typed single-C4 with one common decorated "
            "tail"
        ),
        "first_exact_obstruction": (
            "every selected nonzero determinant product has unequal tails "
            "(a C6, C8, or C4+C4), the switched determinant orientation "
            "does not retain the same decorated tail, or the resulting "
            "single-C4 is coordinate-diagonal; these are respectively the "
            "matching-exchange/Hall boundary and the diagonal cycle-web "
            "boundary"
        ),
        "scope": (
            "ordinary source identity plus complete topology of two literal "
            "eight-site matching tails; it does not assert that a general "
            "minor contains a single-C4 term, nor that the unequal-tail or "
            "diagonal-web alternatives are already empty"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"k3 common-tail boundary ledger changed: {digest}")
    print("uniform k3 minor/common-tail physical boundary: PASS")
    print("minimum columns/quotient ranks: 3/2; nonzero mixed minor forced")
    print("matching pairs C4/C6/C8/C4+C4: 630/1680/2520/630")
    print("typed single-C4 -> ordinary private-site active carrier")
    print("first obstruction: unequal tails or coordinate-diagonal cycle web")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
