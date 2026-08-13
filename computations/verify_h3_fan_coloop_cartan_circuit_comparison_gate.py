#!/usr/bin/env python3
"""Audit the Cartan/circuit gate after the fan-coloop complete-row pivot.

The scalar identity alpha*U-d*V=alpha is only one evaluated response
coordinate.  On its own it is not a target-containing circuit of the full
protected source map.  A two-root Cartan comparison would have to transport
the complete V packet to U first.

The local c<->i Weyl swap at the coloop endpoints has four-word target
defect

    m_(c|i) + m_(i|c) - p_i - p_c.

All four words are fixed by the endpoint transposition.  Hence the odd
Cartan prism kills the defect while the signless prism doubles it.  A pure-c
coloop normalization, even together with both pure target rows, cannot
cancel the two mixed directions.  Global colour permutation only relabels
the same four-dimensional support.

Once a complete protected comparison is separately constructed, the exact
remaining rectangular condition is h_phys(k)!=0 on its target circuit k,
equivalently after normalization h_phys-e_tau lies in row(A_D).  A sharp
linear packet shows that the scalar pivot and an external Cartan column do
not decide this row congruence.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_active_fan_coloop_complete_row_pivot.py":
        "d62fd630abac6e4d25bd6ffb0c1a2070311ec1c5d3c7764f56793283f78aa94a",
    "computations/verify_target_augmented_affine_circuit_cartan_guard.py":
        "7c72b58101cc77a0ca3e3c688b5de0742b4f118777f450f235d578691954d08f",
    "computations/verify_augmented_cartan_full_column_separator_guard.py":
        "0710f16230a1c656bb3ec24843a60c18b668fd499e81652970c41706d6d9f41e",
    "computations/verify_uniform_physical_cartan_source_prism.py":
        "4f23c4645574d619fac4667eba50567435b2f85ff2583b5b3708a565de400cca",
    "computations/verify_protected_physical_comparison_first_source_cell.py":
        "0c93a7e67f1f48d114e343a282820477fe5a86649502500c5b00ee5e560b0245",
    "computations/verify_dark_cartan_physical_q_protected_quotient_comparison.py":
        "eb56cdb4ab1915f8ce35ab3acf0398b4f526c52a17c9c8ebafcc7a5ad4f86bcc",
}
EXPECTED_LEDGER_SHA256 = (
    "3448a7fd4d50a437574e718dd804f173bb25763fa2894c6d4c739c5ba0a49da5"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def rref(matrix):
    work = [list(map(Q, row)) for row in matrix]
    if not work:
        return (), ()
    rows = len(work)
    columns = len(work[0])
    pivot_row = 0
    pivots = []
    for column in range(columns):
        pivot = next((row for row in range(pivot_row, rows)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == rows:
            break
    return tuple(tuple(row) for row in work), tuple(pivots)


def rank(matrix):
    return len(rref(matrix)[1])


def dot(left, right):
    return sum(Q(a) * Q(b) for a, b in zip(left, right, strict=True))


def mat_vec(matrix, vector):
    return tuple(dot(row, vector) for row in matrix)


def append_row(matrix, row):
    return tuple(tuple(map(Q, old)) for old in matrix) + (tuple(map(Q, row)),)


def append_column(matrix, column):
    return tuple(tuple(map(Q, row)) + (Q(value),)
                 for row, value in zip(matrix, column, strict=True))


def border(matrix, column, row, corner=0):
    return append_row(append_column(matrix, column),
                      tuple(map(Q, row)) + (Q(corner),))


def in_row_space(row, matrix):
    return rank(tuple(matrix) + (tuple(map(Q, row)),)) == rank(matrix)


def pure_word(size, colour):
    return (colour,) * size


def mixed_endpoint_word(size, endpoint_colour, interior_colour):
    return (endpoint_colour, endpoint_colour) + (interior_colour,) * (size - 2)


def local_swap(word, first_colour=0, second_colour=1):
    answer = list(word)
    for site in (0, 1):
        if answer[site] == first_colour:
            answer[site] = second_colour
        elif answer[site] == second_colour:
            answer[site] = first_colour
    return tuple(answer)


def transpose_endpoints(word):
    answer = list(word)
    # The orientation transposition is disjoint from the two local root
    # sites 0,1.  In the endpoint-response chart it exchanges P,S, placed
    # here at the last two sites.
    answer[-2], answer[-1] = answer[-1], answer[-2]
    return tuple(answer)


def colour_permute(word, permutation):
    return tuple(permutation[colour] for colour in word)


def audit_four_word_target_defect():
    records = []
    for size in (6, 8, 10):
        pure_c = pure_word(size, 0)
        pure_i = pure_word(size, 1)
        mixed_c_i = mixed_endpoint_word(size, 0, 1)
        mixed_i_c = mixed_endpoint_word(size, 1, 0)
        support = (mixed_c_i, mixed_i_c, pure_i, pure_c)
        coefficients = (1, 1, -1, -1)
        require(len(set(support)) == 4
                and local_swap(pure_i) == mixed_c_i
                and local_swap(pure_c) == mixed_i_c,
                "the two-root Weyl defect support changed")
        require(all(transpose_endpoints(word) == word for word in support),
                "the endpoint transposition stopped fixing the defect")

        # In the free word module, corrections supported only on the two
        # pure target directions can never cancel either mixed coefficient.
        index = {word: position for position, word in enumerate(support)}
        defect = tuple(Q(value) for value in coefficients)
        pure_span = (
            tuple(Q(int(position == index[pure_i])) for position in range(4)),
            tuple(Q(int(position == index[pure_c])) for position in range(4)),
        )
        for left, right in product(range(-3, 4), repeat=2):
            candidate = tuple(defect[position]
                              + left * pure_span[0][position]
                              + right * pure_span[1][position]
                              for position in range(4))
            require(candidate != (Q(0),) * 4,
                    "pure target corrections cancelled the mixed defect")

        # A common global colour permutation preserves four distinct word
        # directions and simply relabels the same coefficient pattern.
        for permutation in permutations(range(3)):
            image = tuple(colour_permute(word, permutation)
                          for word in support)
            require(len(set(image)) == 4,
                    "global colour relabelling collapsed the defect")

        odd = tuple(value - value for value in defect)
        signless = tuple(value + value for value in defect)
        require(not any(odd)
                and signless == tuple(2 * value for value in defect),
                "the odd/signless endpoint parity changed")
        records.append({
            "order": size,
            "defect_words": ["".join(map(str, word)) for word in support],
            "coefficients": list(coefficients),
            "endpoint_odd_defect": list(map(int, odd)),
            "endpoint_signless_defect": list(map(int, signless)),
        })
    return {
        "orders": records,
        "uniform_defect": "m_(c|i)+m_(i|c)-p_i-p_c",
        "pure_coloop_row_target_correction_sufficient": False,
        "both_pure_target_rows_sufficient": False,
        "global_colour_permutation_changes_verdict": False,
        "parity": (
            "the endpoint-odd prism kills the target defect; the signless "
            "prism doubles all four word directions"
        ),
    }


def audit_scalar_pivot_not_a_full_circuit():
    alpha, diagonal, mixed_omit = Q(2), Q(3), Q(2)
    pure_omit = (alpha + diagonal * mixed_omit) / alpha
    require(alpha * pure_omit - diagonal * mixed_omit == alpha,
            "the numerical complete-row pivot changed")
    scalar_augmented = ((pure_omit, -mixed_omit, Q(-1)),)
    displayed_relation = (alpha, diagonal, alpha)
    require(mat_vec(scalar_augmented, displayed_relation) == (Q(0),)
            and rank(scalar_augmented) == 1
            and len(displayed_relation) - rank(scalar_augmented) == 2,
            "the scalar pivot/circuit rank guard changed")

    # Every nonzero scalar old column individually spans the scalar target;
    # the apparent two-column affine relation is not support-minimal.
    coordinate_solutions = {
        "U_only": str(Q(1) / pure_omit),
        "V_only": str(Q(-1) / mixed_omit),
    }
    return {
        "values": {
            "alpha": str(alpha), "d": str(diagonal),
            "U": str(pure_omit), "V": str(mixed_omit),
        },
        "scalar_augmented_row": [str(value)
                                  for value in scalar_augmented[0]],
        "displayed_kernel_relation": [str(value)
                                        for value in displayed_relation],
        "scalar_kernel_dimension": 2,
        "single_coordinate_scalar_target_solutions": coordinate_solutions,
        "consequence": (
            "alpha*U-d*V=alpha is one evaluated coordinate, not a "
            "target-containing circuit of the complete protected map"
        ),
    }


def audit_exact_physical_row_congruence():
    # Complete a target-augmented circuit whose first row is exactly the
    # numerical scalar pivot.  The two independent protected rows have
    # one-dimensional kernel generated by k=(2,3,2).
    circuit = (Q(2), Q(3), Q(2))
    first = (Q(4), Q(-2), Q(-1))
    second = (Q(3), Q(-2), Q(0))
    matrix = (first, second, (Q(0), Q(0), Q(0)))
    require(rank(matrix) == 2
            and mat_vec(matrix, circuit) == (Q(0), Q(0), Q(0)),
            "the completed target circuit changed")

    target_selector = (Q(0), Q(0), Q(1))
    physical_dark = first
    physical_bright = target_selector
    require(dot(target_selector, circuit) == 2
            and dot(physical_dark, circuit) == 0
            and dot(physical_bright, circuit) == 2,
            "the physical row visibility split changed")

    # The external Cartan column raises column rank in both cases.  Only a
    # physical row seeing the circuit supplies the second rank gain.
    cartan = (Q(0), Q(0), Q(1))
    base_rank = rank(matrix)
    dark_rank = rank(border(matrix, cartan, physical_dark))
    bright_rank = rank(border(matrix, cartan, physical_bright))
    require((base_rank, dark_rank, bright_rank) == (2, 3, 4),
            "the anchor/Cartan rectangular rank split changed")

    difference = tuple(left - right for left, right in
                       zip(physical_bright, target_selector, strict=True))
    require(in_row_space(difference, matrix)
            and not in_row_space(
                tuple(left - right for left, right in
                      zip(physical_dark, target_selector, strict=True)),
                matrix),
            "the h_phys/e_tau row-space congruence changed")
    return {
        "protected_matrix": [[str(value) for value in row] for row in matrix],
        "target_circuit": [str(value) for value in circuit],
        "external_cartan_column": [str(value) for value in cartan],
        "rank_A_D": base_rank,
        "rank_with_cartan_and_dark_physical_row": dark_rank,
        "rank_with_cartan_and_bright_physical_row": bright_rank,
        "criterion": (
            "h_phys(k)!=0; after scaling to h_phys(k)=e_tau(k), "
            "h_phys-e_tau lies in row(A_D)"
        ),
        "sharp_guard": (
            "the same scalar pivot, completed target circuit, and external "
            "Cartan column admit a target-bearing row in row(A_D) which "
            "kills the circuit and gives only one rank gain"
        ),
    }


def audit_odd_cartan_plus_physical_signless_workaround():
    # Order: U_plus,U_minus,V_plus,V_minus,target.  The complete-row pivot
    # supplies the physical signless row S.  If the endpoint-odd Cartan
    # projection lands on the *same complete weighted packet*, D splits S
    # into two target-bearing oriented rows.  No signless homotopy is used.
    alpha, diagonal = Q(2), Q(3)
    signless = (alpha, alpha, -diagonal, -diagonal, -alpha)
    odd = (alpha, -alpha, -diagonal, diagonal, Q(0))
    plus = tuple((left + right) / 2
                 for left, right in zip(signless, odd, strict=True))
    minus = tuple((left - right) / 2
                  for left, right in zip(signless, odd, strict=True))
    require(plus == (alpha, 0, -diagonal, 0, -alpha / 2)
            and minus == (0, alpha, 0, -diagonal, -alpha / 2),
            "the S/D oriented pivot split changed")
    require(rank((signless, odd)) == 2
            and rank((plus, minus)) == 2,
            "the S/D endpoint quotient rank changed")

    # Mere nonzero occurrence placement of an odd prism is weaker.  An odd
    # row with the right marked coefficient but one extra protected feature
    # cannot be combined with S to give the desired oriented comparison.
    # The extra coordinate models a complementary Cartan corner retained in
    # the same component or a mismatched fine/terminal readout.
    signless_extended = signless + (Q(0),)
    desired_odd_extended = odd + (Q(0),)
    contaminated_odd = odd + (Q(1),)
    require(rank((signless_extended, desired_odd_extended,
                  contaminated_odd)) == 3
            and not in_row_space(desired_odd_extended,
                                 (signless_extended, contaminated_odd)),
            "the protected-packet mismatch guard changed")
    return {
        "feature_order": [
            "U_plus", "U_minus", "V_plus", "V_minus", "target"
        ],
        "physical_signless_pivot_S": [str(value) for value in signless],
        "target_safe_odd_Cartan_D": [str(value) for value in odd],
        "oriented_E_plus=(S+D)/2": [str(value) for value in plus],
        "oriented_E_minus=(S-D)/2": [str(value) for value in minus],
        "positive_consequence": (
            "if D is the odd projection of the same complete weighted "
            "U/V packet as S, the two oriented affine rows are physical "
            "and each carries target alpha/2; no signless Cartan homotopy "
            "or target correction is needed"
        ),
        "remaining_packet_identity": (
            "the ambient Cartan placement theorem only gives a nonzero "
            "marked odd occurrence.  One must still prove that every "
            "retained Cartan corner, fine label, protected readout, and "
            "coefficient multiplier agrees with the complete pivot packet, "
            "or that a mismatch is a typed saturated exit"
        ),
        "protected_contaminant_blocks_split": True,
    }


def main():
    pin_dependencies()
    ledger = {
        "pins": PINS,
        "two_root_target_defect": audit_four_word_target_defect(),
        "scalar_pivot_typing_guard": audit_scalar_pivot_not_a_full_circuit(),
        "odd_Cartan_plus_physical_signless_workaround":
            audit_odd_cartan_plus_physical_signless_workaround(),
        "physical_row_congruence": audit_exact_physical_row_congruence(),
        "conditional_positive_composition": (
            "after a source-valid complete protected two-root comparison "
            "lifts the V packet to U and produces a minimum target circuit, "
            "the target-augmented Cartan theorem applies.  An internal "
            "Cartan column gives normalized affine exchange or homogeneous "
            "unit-Cartan connector; an external column gives a target-dark "
            "separator.  The constructive rank-two landing additionally "
            "requires the displayed h_phys/e_tau row congruence"
        ),
        "gate_identification": (
            "the fan-coloop trapped-carrier gate has the same source type "
            "as the protected two-root comparison and separate physical-"
            "anchor law in the determinant-dark collision gate.  The "
            "ambient Cartan prism supplies the word-changing column, but "
            "the pure-c coloop normalization supplies neither a target-safe "
            "signless comparison nor visibility of the physical anchor row"
        ),
        "canonical_workaround": (
            "do not construct a signless Cartan homotopy.  Use the already "
            "physical complete signless pivot S and a target-safe odd "
            "Cartan D.  Once their complete protected packets agree, "
            "(S+D)/2 and (S-D)/2 give the two oriented target-bearing rows. "
            "The remaining source theorem is precisely packet agreement "
            "modulo protected rows or a typed saturated exit, followed by "
            "the independent h_phys circuit congruence"
        ),
        "remaining_obstruction": (
            "construct the target-corrected complete two-root mapping-cone "
            "comparison in the fan-coloop fine grade (or transport the "
            "canonical comparison there), then prove h_phys(k)!=0 or type "
            "the dual failure as the already saturated Hall/Fitting exit"
        ),
        "scope": (
            "exact target-word and linear-algebra obstruction, not a full "
            "one-bad source counterexample and not construction of the "
            "protected two-root comparison"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"fan-coloop Cartan/circuit ledger changed: {digest}")
    print("h3 fan-coloop Cartan/circuit comparison: SHARP GATE")
    print("pure coloop row cannot target-correct signless two-root prism")
    print("rectangular landing requires complete Phi plus h_phys visibility")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
