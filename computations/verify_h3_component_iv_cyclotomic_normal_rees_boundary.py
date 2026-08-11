#!/usr/bin/env python3
"""First normal/Rees correction of the cyclotomic five-Schur composition.

The five chord directions give an invertible Jacobian for the five face
hafnians at the cyclotomic point.  Dividing the tagged Schur tails by the
Rees parameter therefore gives five independent chart-odd boundaries.
Their complete words are mixed (target zero), and the two old ordinary-
residue sector readings cancel.  After localizing kappa the boundary matrix
remains invertible.

This is an exact first-normal associated-graded result.  It does not prove
that the Rees classes lift to an all-order physical attaching chain.
"""

from fractions import Fraction as Q
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path

import verify_h3_component_iv_cyclotomic_hamming_two_boundary as H2
import verify_h3_component_iv_cyclotomic_schur_face_composition as SC


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_DIGEST = "d2ed8773582c6a945f500571f58c8c9eb09990d626b7db3ee90c57fc05e8d529"
PINS = {
    "computations/verify_h3_component_iv_cyclotomic_schur_face_composition.py":
        "66086a7a67e5ca05864394933d37e36b6b92b990b91169eef19b275e7c02181d",
    "computations/verify_h3_component_iv_cyclotomic_word_change_relation.py":
        "335c82b382dcb3b8d69cd57a4fa54185a0db96368b5413b218b7c0f8bf303dae",
    "computations/verify_h3_component_iv_cyclotomic_hamming_two_boundary.py":
        "aa225b9c59c22a104957b61da6ad2a365577876fe3fd74de6f119d4b42241c76",
    "computations/verify_h3_gl3_normalized_bar_word_change_obstruction.py":
        "ed3c1baafd7d83819c1b6842857611b5b540c57ef95c8ca8a450de357312670a",
}

D = H2.SITES
CHORDS = ((1, 3), (1, 4), (2, 4), (2, 5), (3, 5))
ZERO = H2.ZERO
ONE = H2.ONE


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def inverse(value):
    norm = value.a * value.a - value.a * value.b + value.b * value.b
    require(norm, "attempted to invert zero in Q(zeta)")
    return H2.K((value.a - value.b) / norm, -value.b / norm)


def determinant(matrix):
    work = [[H2.K(value) for value in row] for row in matrix]
    answer = ONE
    for column in range(len(work)):
        pivot = next((row for row in range(column, len(work))
                      if work[row][column]), None)
        if pivot is None:
            return ZERO
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            answer = -answer
        value = work[column][column]
        answer *= value
        scale = inverse(value)
        work[column] = [scale * entry for entry in work[column]]
        for row in range(column + 1, len(work)):
            if not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [left - scale * right for left, right in
                         zip(work[row], work[column], strict=True)]
    return answer


def inverse_matrix(matrix):
    size = len(matrix)
    work = [
        [H2.K(value) for value in row]
        + [ONE if row_index == column else ZERO for column in range(size)]
        for row_index, row in enumerate(matrix)
    ]
    for column in range(size):
        pivot = next((row for row in range(column, size) if work[row][column]), None)
        require(pivot is not None, "normal Jacobian is singular")
        work[column], work[pivot] = work[pivot], work[column]
        scale = inverse(work[column][column])
        work[column] = [scale * entry for entry in work[column]]
        for row in range(size):
            if row == column or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [left - scale * right for left, right in
                         zip(work[row], work[column], strict=True)]
    return [row[size:] for row in work]


def matmul(left, right):
    return [
        [sum((left[i][k] * right[k][j] for k in range(len(right))), ZERO)
         for j in range(len(right[0]))]
        for i in range(len(left))
    ]


def parity(permutation):
    inversions = sum(permutation[i] > permutation[j]
                     for i in range(len(permutation))
                     for j in range(i + 1, len(permutation)))
    return -1 if inversions % 2 else 1


def determinant_definition(matrix):
    return sum((H2.K(parity(permutation))
                * product(matrix[row][permutation[row]]
                          for row in range(len(matrix)))
                for permutation in permutations(range(len(matrix)))), ZERO)


def product(values):
    answer = ONE
    for value in values:
        answer *= value
    return answer


def tau_multiply(left, right):
    """Multiply degree-at-most-two tau polynomials."""
    output = [ZERO, ZERO, ZERO]
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            if i + j <= 2:
                output[i + j] += a * b
    return tuple(output)


def edge_tau(edge, normal):
    edge = tuple(sorted(edge))
    base = H2.q_edge(*edge)
    direction = normal.get(edge, ZERO)
    return base, direction, ZERO


def face_tau(deleted, normal):
    vertices = tuple(site for site in D if site != deleted)
    total = [ZERO, ZERO, ZERO]
    a, b, c, d = vertices
    pairings = (((a, b), (c, d)), ((a, c), (b, d)), ((a, d), (b, c)))
    for left, right in pairings:
        term = tau_multiply(edge_tau(left, normal), edge_tau(right, normal))
        total = [old + new for old, new in zip(total, term, strict=True)]
    return tuple(total)


def jacobian():
    columns = []
    for chord in CHORDS:
        normal = {tuple(sorted(chord)): ONE}
        column = []
        for deleted in D:
            constant, linear, _quadratic = face_tau(deleted, normal)
            require(constant == ZERO, "cyclotomic face constant became nonzero")
            column.append(linear)
        columns.append(column)
    return [[columns[column][row] for column in range(5)] for row in range(5)]


def identity(size):
    return [[ONE if row == column else ZERO for column in range(size)]
            for row in range(size)]


def main():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"pinned dependency changed: {relative}: {actual}")

    j = jacobian()
    expected_j = [
        [ZERO, ZERO, H2.ZETA, ONE, H2.ZETA],
        [ONE, H2.ZETA, ZERO, ZERO, H2.ZETA],
        [ZERO, H2.ZETA, ONE, H2.ZETA, ZERO],
        [H2.ZETA, ZERO, ZERO, H2.ZETA, ONE],
        [H2.ZETA, ONE, H2.ZETA, ZERO, ZERO],
    ]
    require(j == expected_j, "normal Jacobian entries changed")
    det = determinant(j)
    require(det == H2.K(-4, -8), f"normal determinant changed: {det.text()}")
    require(determinant_definition(j) == det,
            "elimination and permutation determinants disagree")

    j_inverse = inverse_matrix(j)
    require(matmul(j, j_inverse) == identity(5), "normal inverse is not right inverse")
    require(matmul(j_inverse, j) == identity(5), "normal inverse is not left inverse")

    face_words = []
    for deleted in D:
        word = list(SC.BASE_WORD)
        word[deleted] = 0
        word = tuple(word)
        require(len(set(word)) > 1,
                f"face {deleted}: normal deformation acquired a pure target word")
        face_words.append("".join(map(str, word)))

    # Columns of J^-1 are normal chord directions n^(v) with dh_w(n^(v))
    # equal to delta_wv.  Verify the actual tau expansion, including the
    # quadratic remainder that is discarded only after the honest Rees
    # division by tau.
    normal_records = []
    tagged_columns = []
    for face in range(5):
        direction = {
            CHORDS[chord]: j_inverse[chord][face]
            for chord in range(5)
        }
        linear_values = []
        quadratic_values = []
        for deleted in D:
            constant, linear, quadratic = face_tau(deleted, direction)
            require(constant == ZERO, "normal arc left V(h) at order zero")
            linear_values.append(linear)
            quadratic_values.append(quadratic)
        expected_linear = [ONE if row == face else ZERO for row in range(5)]
        require(linear_values == expected_linear,
                f"normal direction {face + 1} is not dual to dh")

        # After h/tau and tau=0, the pq/pr tagged sectors are (+e_v,-e_v).
        tagged = []
        for value in linear_values:
            tagged.extend((value, -value))
        tagged_columns.append(tagged)
        normal_records.append({
            "face": face + 1,
            "chord_direction": {
                f"{left}{right}": direction[(left, right)].text()
                for left, right in CHORDS
            },
            "dh": [value.text() for value in linear_values],
            "tau2_remainder": [value.text() for value in quadratic_values],
        })

    # Boundary reads the chart-odd half-difference; old ores reads the sum.
    boundary = []
    old_ores = []
    for tagged in tagged_columns:
        boundary.append([(tagged[2 * face] - tagged[2 * face + 1]) / 2
                         for face in range(5)])
        old_ores.append([tagged[2 * face] + tagged[2 * face + 1]
                         for face in range(5)])
    require(boundary == identity(5), "first normal boundary is not I5")
    require(old_ores == [[ZERO] * 5 for _ in range(5)],
            "first normal old-ores value is nonzero")
    require(H2.rank_over_k(boundary) == 5,
            "first normal boundary lost rank")

    # Every face word is mixed, so target is identically zero.  Localizing
    # kappa scales the boundary by a unit and cannot create a separator.
    kappa_records = []
    for kappa in (H2.K(1), H2.K(2), H2.K(Q(-3, 2))):
        scaled = [[kappa * value for value in row] for row in boundary]
        scaled_det = determinant(scaled)
        require(scaled_det == kappa * kappa * kappa * kappa * kappa,
                "kappa-scaled boundary determinant changed")
        require(H2.rank_over_k(scaled) == 5,
                "kappa localization lost normal boundary rank")
        kappa_records.append({
            "kappa": kappa.text(),
            "boundary_rank": 5,
            "boundary_det": scaled_det.text(),
        })

    ledger = {
        "scope": "first normal/Rees correction transverse to cyclotomic V(h)",
        "normal_coordinates": [f"q_{left}{right}" for left, right in CHORDS],
        "face_coordinates": [f"h_{face}" for face in D],
        "literal_mixed_face_words": face_words,
        "Jacobian": [[value.text() for value in row] for row in j],
        "Jacobian_det": det.text(),
        "Jacobian_rank": 5,
        "normal_directions": normal_records,
        "Rees_operation": "q=q0+tau*n; divide tagged (h,-h) by tau; set tau=0",
        "chart_odd_boundary_matrix": "I5",
        "boundary_rank": 5,
        "target_rank": 0,
        "old_ores_rank": 0,
        "kappa_localized_probes": kappa_records,
        "primitive_normal_separator_dimension": 0,
        "verdict": (
            "the first normal/Rees correction gives five independent nonzero "
            "kappa-localized chart-odd boundaries with target=old-ores=0"
        ),
        "scope_guard": (
            "this is the exact associated-graded normal bundle; an all-order "
            "source-provenant lift and the physical identification of this "
            "chart-odd boundary with the final cap w-coordinate remain to prove"
        ),
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    digest = sha256(encoded).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST, f"ledger digest changed: {digest}")

    print("h=3 Component-IV cyclotomic normal/Rees boundary: PASS")
    print("normal Jacobian det = -4-8*zeta; rank 5")
    print("Rees chart-odd boundary = I5; target rank 0; old-ores rank 0")
    print("kappa localization preserves boundary rank 5")
    print("all-order/physical cap identification: OPEN")
    print(f"ledger sha256: {digest}")


if __name__ == "__main__":
    main()
