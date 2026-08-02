#!/usr/bin/env python3
"""Independent exact audit of the h=3 denominator Tor/Fitting gate.

No code or computed data are imported from the primary checker.  The
243-by-15 denominator matrices are rebuilt from raw universal or sparse
internal q-cells.  Exact rational elimination verifies universal
injectivity, specialized kernels, Tor dimensions, transgression ranks,
membership defects, and maximal augmented-minor witnesses.

The audit also freezes a two-dimensional counterexample to the primary
note's local augmented-minor statement when its displayed unit r-minor is
not assumed maximal/constant-rank.
"""

import argparse
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import product
import json


Q = Fraction
ZERO = Q(0)
ONE = Q(1)
COLOURS = (0, 1, 2)
VERTICES = (1, 2, 3, 4, 5)
WORDS = tuple(product(COLOURS, repeat=5))
COLUMNS = tuple((vertex, colour) for vertex in VERTICES for colour in COLOURS)
RESET_WORD = (1, 2, 1, 1, 2)
SELECTED_LABELS = tuple(zip(VERTICES, RESET_WORD))
EXPECTED_DIGEST = "d7c63abd5affe86433ba3a3c0efc3b28c96f7996acad14a2e06c78250a37f0cc"


def insist(condition, message):
    if not condition:
        raise AssertionError(message)


@lru_cache(maxsize=None)
def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    head = vertices[0]
    answer = []
    for offset, mate in enumerate(vertices[1:]):
        tail = vertices[1 : offset + 1] + vertices[offset + 2 :]
        for matching in perfect_matchings(tail):
            answer.append(((head, mate),) + matching)
    return tuple(answer)


def canonical_edge(left, right, left_colour, right_colour):
    if left < right:
        return left, right, left_colour, right_colour
    return right, left, right_colour, left_colour


def make_sparse_value(raw_cells):
    cells = {}
    for left, right, left_colour, right_colour, numerator, denominator in raw_cells:
        key = canonical_edge(left, right, left_colour, right_colour)
        insist(key not in cells, f"duplicate raw q-cell {key}")
        cells[key] = Q(numerator, denominator)

    def value(left, right, left_colour, right_colour):
        key = canonical_edge(left, right, left_colour, right_colour)
        return cells.get(key, ZERO)

    return value


def make_denominator(value):
    """Build rows indexed by words and columns indexed by (site, colour)."""
    matrix = []
    for word in WORDS:
        row = []
        colouring = dict(zip(VERTICES, word))
        for deleted, linear_colour in COLUMNS:
            if colouring[deleted] != linear_colour:
                row.append(ZERO)
                continue
            remaining = tuple(vertex for vertex in VERTICES if vertex != deleted)
            coefficient = ZERO
            for matching in perfect_matchings(remaining):
                term = ONE
                for left, right in matching:
                    term *= value(left, right, colouring[left], colouring[right])
                coefficient += term
            row.append(coefficient)
        matrix.append(row)
    return matrix


def transpose(matrix):
    return [list(column) for column in zip(*matrix)] if matrix else []


def rref(matrix):
    work = [[Q(entry) for entry in row] for row in matrix]
    pivots = []
    pivot_row = 0
    width = len(work[0]) if work else 0
    for column in range(width):
        found = next(
            (row for row in range(pivot_row, len(work)) if work[row][column]),
            None,
        )
        if found is None:
            continue
        work[pivot_row], work[found] = work[found], work[pivot_row]
        pivot = work[pivot_row][column]
        work[pivot_row] = [entry / pivot for entry in work[pivot_row]]
        for row in range(len(work)):
            if row != pivot_row and work[row][column]:
                multiplier = work[row][column]
                work[row] = [
                    entry - multiplier * pivot_entry
                    for entry, pivot_entry in zip(work[row], work[pivot_row])
                ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(work):
            break
    return work, tuple(pivots)


def rank(matrix):
    return len(rref(matrix)[1])


def kernel(matrix):
    reduced, pivots = rref(matrix)
    width = len(matrix[0]) if matrix else 0
    free = [column for column in range(width) if column not in pivots]
    answer = []
    for free_column in free:
        vector = [ZERO] * width
        vector[free_column] = ONE
        for row, pivot_column in enumerate(pivots):
            vector[pivot_column] = -reduced[row][free_column]
        answer.append(tuple(vector))
    return tuple(answer)


def determinant(matrix):
    insist(all(len(row) == len(matrix) for row in matrix), "nonsquare determinant")
    work = [[Q(entry) for entry in row] for row in matrix]
    result = ONE
    for column in range(len(work)):
        pivot_row = next(
            (row for row in range(column, len(work)) if work[row][column]),
            None,
        )
        if pivot_row is None:
            return ZERO
        if pivot_row != column:
            work[column], work[pivot_row] = work[pivot_row], work[column]
            result = -result
        pivot = work[column][column]
        result *= pivot
        for row in range(column + 1, len(work)):
            if work[row][column]:
                multiplier = work[row][column] / pivot
                work[row] = [
                    entry - multiplier * pivot_entry
                    for entry, pivot_entry in zip(work[row], work[column])
                ]
    return result


def section(matrix, row_indices, column_indices):
    return [
        [matrix[row][column] for column in column_indices]
        for row in row_indices
    ]


def independent_rows(matrix):
    """Return original row indices supporting a maximal nonzero minor."""
    return rref(transpose(matrix))[1]


def column_index(label):
    return COLUMNS.index(label)


def word_index(word):
    if isinstance(word, str):
        word = tuple(map(int, word))
    return WORDS.index(tuple(word))


def audit_generic_value(left, right, left_colour, right_colour):
    if left > right:
        left, right = right, left
        left_colour, right_colour = right_colour, left_colour
    # Deliberately different from the primary checker's specialization.
    return Q(2 + 131 * left + 29 * right + 11 * left_colour + 5 * right_colour)


# Raw internal q-cells, copied from the packet definitions as mathematical
# input.  The denominator matrix is reconstructed below from the divided
# matching formula rather than imported from any previous executable.
DIRECT_FREE_Q = (
    (1, 2, 1, 2, 1, 1),
    (1, 3, 1, 2, 1, 1),
    (1, 4, 1, 1, 1, 1),
    (2, 3, 2, 0, 1, 1),
    (3, 4, 0, 1, 1, 1),
    (3, 5, 0, 2, 1, 1),
)

TILTED_Q = (
    (1, 2, 1, 2, 1, 1),
    (1, 3, 0, 0, 1, 1),
    (1, 4, 1, 1, 1, 1),
    (1, 5, 2, 2, 1, 1),
    (2, 3, 2, 0, 1, 1),
    (3, 4, 0, 1, 1, 1),
    (3, 5, 0, 2, 1, 1),
)


PACKETS = {
    "direct_free": {"raw": DIRECT_FREE_Q, "kappa": Q(-1, 4)},
    "tilted": {"raw": TILTED_Q, "kappa": Q(-5, 2)},
}


def universal_check():
    matrix = make_denominator(audit_generic_value)
    full_rank = rank(matrix)
    full_rows = independent_rows(matrix)
    insist(full_rank == 15 and len(full_rows) == 15, "generic full rank changed")
    full_minor = determinant(section(matrix, full_rows, range(15)))
    insist(full_minor, "independent generic 15-minor vanished")

    selected = tuple(column_index(label) for label in SELECTED_LABELS)
    other = tuple(column for column in range(15) if column not in selected)
    other_matrix = section(matrix, range(243), other)
    other_rank = rank(other_matrix)
    other_rows = independent_rows(other_matrix)
    insist(other_rank == 10 and len(other_rows) == 10, "generic other rank changed")
    other_minor = determinant(section(matrix, other_rows, other))
    insist(other_minor, "independent generic other minor vanished")

    return {
        "rank": full_rank,
        "rows": ["".join(map(str, WORDS[row])) for row in full_rows],
        "minor": str(full_minor),
        "other_rank": other_rank,
        "other_rows": ["".join(map(str, WORDS[row])) for row in other_rows],
        "other_minor": str(other_minor),
    }


def projection_to_selected(vector, selected):
    return tuple(vector[column] for column in selected)


def unit_vector(width, position):
    return tuple(ONE if index == position else ZERO for index in range(width))


def find_maximal_augmented_minor(matrix, other, selected):
    """Choose a maximal independent other block, then selected increments."""
    other_matrix = section(matrix, range(len(matrix)), other)
    _, local_pivots = rref(other_matrix)
    chosen = [other[index] for index in local_pivots]
    current_rank = rank(section(matrix, range(len(matrix)), chosen))
    for column in selected:
        candidate = chosen + [column]
        candidate_rank = rank(section(matrix, range(len(matrix)), candidate))
        if candidate_rank > current_rank:
            chosen.append(column)
            current_rank = candidate_rank
    full_rank = rank(matrix)
    insist(current_rank == full_rank, "augmented column search did not reach full rank")
    chosen_matrix = section(matrix, range(len(matrix)), chosen)
    rows = independent_rows(chosen_matrix)
    insist(len(rows) == len(chosen) == full_rank, "maximal minor is not square")
    value = determinant(section(matrix, rows, chosen))
    insist(value, "maximal augmented minor vanished")
    return tuple(chosen), tuple(rows), value


def packet_check(name):
    metadata = PACKETS[name]
    matrix = make_denominator(make_sparse_value(metadata["raw"]))
    selected = tuple(column_index(label) for label in SELECTED_LABELS)
    other = tuple(column for column in range(15) if column not in selected)

    full_rank = rank(matrix)
    other_rank = rank(section(matrix, range(243), other))
    null_basis = kernel(matrix)
    insist(len(null_basis) == 15 - full_rank, f"{name}: kernel/rank-nullity failure")
    for vector in null_basis:
        insist(
            all(sum(entry * coefficient for entry, coefficient in zip(row, vector)) == 0
                for row in matrix),
            f"{name}: computed kernel vector is not a relation",
        )

    projected = tuple(projection_to_selected(vector, selected) for vector in null_basis)
    tau_rank = rank(projected)
    expected_from_rank_formula = 5 - (full_rank - other_rank)
    insist(tau_rank == expected_from_rank_formula, f"{name}: transgression rank formula failed")
    cokernel_dual = kernel(projected)
    insist(len(cokernel_dual) == 5 - tau_rank, f"{name}: cokernel dual changed")

    individual_hits = []
    for position in range(5):
        basis_vector = unit_vector(5, position)
        individual_hits.append(
            rank(list(projected) + [basis_vector]) == tau_rank
        )

    # All five selected entries in the reset-word row vanish, despite the
    # whole-column membership obstruction.
    reset_row = matrix[word_index(RESET_WORD)]
    h_values = tuple(reset_row[column] for column in selected)
    insist(h_values == (ZERO,) * 5, f"{name}: reset defects do not vanish")

    witness_columns, witness_rows, witness_value = find_maximal_augmented_minor(
        matrix, other, selected
    )
    selected_increment = len(witness_columns) - other_rank
    insist(selected_increment == full_rank - other_rank, f"{name}: bad augmented increment")

    # The coarse I_11(b)=0 necessary condition holds automatically here,
    # yet tau is not onto.  This independently demonstrates that I_11 alone
    # is not sufficient even over these reduced fields on lower-rank strata.
    fitting_i11_vanishes = full_rank < 11
    insist(fitting_i11_vanishes and tau_rank < 5, f"{name}: Fitting counterguard changed")

    return {
        "kappa_external_packet_metadata": str(metadata["kappa"]),
        "rank": full_rank,
        "other_rank": other_rank,
        "tor_dimension": len(null_basis),
        "tau_rank": tau_rank,
        "tau_cokernel_dimension": 5 - tau_rank,
        "rank_formula": expected_from_rank_formula,
        "individual_hits": individual_hits,
        "h_values": [str(value) for value in h_values],
        "kernel": [[str(value) for value in vector] for vector in null_basis],
        "tau_rows": [[str(value) for value in vector] for vector in projected],
        "cokernel_dual": [[str(value) for value in vector] for vector in cokernel_dual],
        "i11_vanishes_but_tau_not_onto": True,
        "augmented_columns": [f"d{COLUMNS[column][0]}{COLUMNS[column][1]}"
                              for column in witness_columns],
        "augmented_rows": ["".join(map(str, WORDS[row])) for row in witness_rows],
        "augmented_minor": str(witness_value),
    }


def local_minor_scope_counterexample():
    # Over the local field Q, B=I_2 and y=e_2.  The 1x1 upper-left minor is
    # a unit and y belongs to im(B), but adjoining y to the first pivot
    # column has nonzero 2x2 determinant.  Thus the primary note's statement
    # is false for an arbitrary unit r-minor.  It becomes correct when r is
    # the local maximal/constant rank (or, here, when the full 2x2 pivot is
    # used).
    b_other = [[ONE, ZERO], [ZERO, ONE]]
    selected = [ZERO, ONE]
    unit_r_minor = b_other[0][0]
    augmented_minor = determinant([
        [b_other[0][0], selected[0]],
        [b_other[1][0], selected[1]],
    ])
    selected_in_image = True
    insist(unit_r_minor == ONE and selected_in_image and augmented_minor == ONE,
            "local-minor scope counterexample changed")
    return {
        "ring": "Q",
        "chosen_r": 1,
        "unit_minor": str(unit_r_minor),
        "selected_in_other_image": selected_in_image,
        "augmented_minor": str(augmented_minor),
        "required_correction": "r maximal/constant rank, or use the full 10-column unit pivot",
    }


def execute(mode):
    ledger = {"local_minor_scope": local_minor_scope_counterexample()}
    if mode in ("all", "universal"):
        ledger["universal"] = universal_check()
    if mode in ("all", "direct_free"):
        ledger["direct_free"] = packet_check("direct_free")
    if mode in ("all", "tilted"):
        ledger["tilted"] = packet_check("tilted")
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    if mode == "all":
        insist(digest == EXPECTED_DIGEST, f"audit digest changed: {digest}")
    print(f"independent h=3 denominator Tor/Fitting audit ({mode}): PASS")
    if mode in ("all", "universal"):
        print("independent universal specialization: ranks 15 and 10")
    if mode in ("all", "direct_free"):
        print("direct-free: Tor dimension 8; tau rank 4")
    if mode in ("all", "tilted"):
        print("tilted: Tor dimension 7; tau rank 3")
    print("scope correction: a unit r-minor must be maximal/constant-rank")
    print(f"sha256: {digest}")
    return digest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("all", "universal", "direct_free", "tilted"),
        default="all",
    )
    arguments = parser.parse_args()
    execute(arguments.mode)


if __name__ == "__main__":
    main()
