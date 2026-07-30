#!/usr/bin/env python3
"""Audit the uniform one-site polarization obstruction.

This intentionally reuses the exact packet constructor in
verify_full_27_colon_cycle_guard.py. It adds no third-party dependency and
keeps the new audit focused on the 27-by-(2h+7) local coefficient map.
"""

from fractions import Fraction
import importlib.util
from pathlib import Path


Q = Fraction
LABELS = range(3)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def load_guard_module():
    path = Path(__file__).with_name("verify_full_27_colon_cycle_guard.py")
    spec = importlib.util.spec_from_file_location("full_27_guard", path)
    require(spec is not None and spec.loader is not None, "guard module spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


GUARD = load_guard_module()


def rref(matrix):
    work = [[Q(value) for value in row] for row in matrix]
    if not work:
        return work, []
    row = 0
    pivots = []
    for column in range(len(work[0])):
        pivot = next(
            (index for index in range(row, len(work))
             if work[index][column]),
            None,
        )
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        pivot_value = work[row][column]
        work[row] = [value / pivot_value for value in work[row]]
        for index in range(len(work)):
            if index == row or not work[index][column]:
                continue
            scalar = work[index][column]
            work[index] = [
                work[index][j] - scalar * work[row][j]
                for j in range(len(work[0]))
            ]
        pivots.append(column)
        row += 1
        if row == len(work):
            break
    return work, pivots


def nullspace(matrix):
    reduced, pivots = rref(matrix)
    width = len(matrix[0])
    free = [column for column in range(width) if column not in pivots]
    basis = []
    for free_column in free:
        vector = [Q(0)] * width
        vector[free_column] = Q(1)
        for row, pivot in reversed(list(enumerate(pivots))):
            vector[pivot] = -sum(
                reduced[row][column] * vector[column]
                for column in free
            )
        basis.append(vector)
    return basis


def row_index(i, j, k):
    return 9 * i + 3 * j + k


def one_site_map(h, data=None):
    """Return the u0-polarized top-row map and its column labels."""
    if data is None:
        data = GUARD.packet(h)
    site_count = 2 * h - 1
    top_mask = (1 << site_count) - 1

    star_base = {
        name: [
            {mask: value for mask, value in form.items() if mask != 1}
            for form in data[name]
        ]
        for name in ("x", "y", "t")
    }
    z_base = {
        mask: value for mask, value in data["z"].items()
        if not (mask & 1)
    }
    columns = [
        ("star", name, label)
        for name in ("x", "y", "t")
        for label in LABELS
    ] + [
        ("z", site) for site in range(1, site_count)
    ]

    values = []
    for column in columns:
        lifted = dict(data)
        for name in ("x", "y", "t"):
            lifted[name] = [dict(form) for form in star_base[name]]
        lifted["z"] = dict(z_base)

        if column[0] == "star":
            _, name, label = column
            lifted[name][label][1] = Q(1)
        else:
            _, site = column
            lifted["z"][1 | (1 << site)] = Q(1)

        lifted["z_h_minus_1"] = GUARD.divided_power(
            lifted["z"], h - 1
        )
        lifted["z_h_minus_2"] = GUARD.divided_power(
            lifted["z"], h - 2
        )

        column_values = []
        for i in LABELS:
            for j in LABELS:
                for k in LABELS:
                    residual = GUARD.row_residual(lifted, i, j, k)
                    # row_residual subtracts the scalar target. Add it
                    # back: this map contains only the source-side vector.
                    if i == j == k:
                        residual = GUARD.add(
                            residual, lifted["targets"][i]
                        )
                    column_values.append(residual.get(top_mask, Q(0)))
        values.append(column_values)

    matrix = [
        [values[column][row] for column in range(len(columns))]
        for row in range(27)
    ]
    return matrix, columns


def audit_one_site_maps():
    summaries = []
    base_matrix = None
    base_columns = None
    certificate = {
        row_index(0, 0, 0): Q(1),
        row_index(0, 1, 1): Q(-8, 3),
        row_index(1, 0, 0): Q(3, 8),
        row_index(1, 1, 1): Q(-1),
    }
    target_coefficients = [
        certificate.get(row_index(i, i, i), Q(0))
        for i in LABELS
    ]
    require(target_coefficients == [Q(1), Q(-1), Q(0)],
            "four-row target functional is X0-X1")

    for h in range(3, 9):
        data = GUARD.packet(h)
        # Fail closed if the imported scalar packet ceases to have its
        # advertised normalization, literal rows, or contracted rows.
        GUARD.check_linear_data(data)
        GUARD.check_all_rows(data)
        GUARD.check_contractions(data)

        matrix, columns = one_site_map(h, data)
        off_rows = [
            row_index(i, j, k)
            for i in LABELS for j in LABELS for k in LABELS
            if not (i == j == k)
        ]
        off_matrix = [matrix[row] for row in off_rows]
        full_rank = GUARD.matrix_rank(matrix)
        off_rank = GUARD.matrix_rank(off_matrix)
        require(full_rank == 13, f"full local rank at h={h}")
        require(off_rank == 12, f"off-diagonal local rank at h={h}")

        certificate_values = [
            sum(
                coefficient * matrix[row][column]
                for row, coefficient in certificate.items()
            )
            for column in range(len(columns))
        ]
        require(not any(certificate_values),
                f"four-row certificate at h={h}")

        kernel = nullspace(off_matrix)
        diagonal_image = []
        for vector in kernel:
            output = [
                sum(
                    matrix[row_index(i, i, i)][column] * vector[column]
                    for column in range(len(columns))
                )
                for i in LABELS
            ]
            diagonal_image.append(output)
            require(output == [0, 0, 0]
                    or output[0] == output[1] == output[2],
                    f"diagonal image line at h={h}")
        require(GUARD.matrix_rank(diagonal_image) == 1,
                f"nonzero diagonal line at h={h}")

        if h == 3:
            base_matrix = matrix
            base_columns = columns
            require(len(kernel) == 1, "base off-diagonal nullity")
            expected = [Q(0)] * len(columns)
            expected[1] = Q(1, 3)  # x_1 at u0
            expected[3] = Q(-1)    # y_0 at u0
            expected[8] = Q(1)     # t_2 at u0
            require(kernel[0] == expected, "explicit base kernel line")
            require(diagonal_image == [[-1, -1, -1]],
                    "explicit base diagonal output")
        else:
            require(columns[:len(base_columns)] == base_columns,
                    f"base local columns retained at h={h}")
            require(all(row[:len(base_columns)] == base_matrix[index]
                        for index, row in enumerate(matrix)),
                    f"uniform suspension of base columns at h={h}")
            # New incident edges from u0 to a suspended pair strand its
            # mate; their complete top-row columns are identically zero.
            for column, label in enumerate(columns):
                if label[0] == "z" and label[1] >= 5:
                    require(not any(row[column] for row in matrix),
                            f"stranded suspension edge {label} at h={h}")

        summaries.append((h, len(columns), full_rank, off_rank))
    return summaries


def multiply_terms(left, right):
    result = {}
    for word_left, coefficient_left in left.items():
        sites_left = {site for site, _ in word_left}
        for word_right, coefficient_right in right.items():
            if sites_left & {site for site, _ in word_right}:
                continue
            word = tuple(sorted(word_left + word_right))
            result[word] = result.get(word, Q(0)) + (
                coefficient_left * coefficient_right
            )
    return {word: value for word, value in result.items() if value}


def audit_two_site_collision():
    for site_count in range(2, 9):
        target = {
            colour: {
                tuple((site, colour) for site in range(site_count)): Q(1)
            }
            for colour in LABELS
        }
        left = {((0, 0),): Q(1), ((1, 1),): Q(1)}
        companion = {((0, 0),): Q(1), ((1, 2),): Q(1)}

        def pure_hole(colour, missing):
            return {
                tuple((site, colour) for site in range(site_count)
                      if site != missing): Q(1)
            }

        require(multiply_terms(left, pure_hole(0, 0)) == target[0],
                "left e anchor")
        require(multiply_terms(left, pure_hole(1, 1)) == target[1],
                "left a anchor")
        require(multiply_terms(companion, pure_hole(0, 0)) == target[0],
                "right e anchor")
        require(multiply_terms(companion, pure_hole(2, 1)) == target[2],
                "right b anchor")


def main():
    summaries = audit_one_site_maps()
    audit_two_site_collision()
    print("pure-target one-site polarization obstruction: PASS")
    print("  h, columns, full rank, off-diagonal rank:", summaries)
    print("  diagonal target image: Q*(1,1,1)")
    print("  sparse ordered-row certificate: X0-X1=0")
    print("  scalar dependency: normalized and 27/27 rows checked")
    print("  suspension: base columns fixed; new incident columns zero")
    print("  two-site/four-anchor collision guard: m=2,...,8")


if __name__ == "__main__":
    main()
