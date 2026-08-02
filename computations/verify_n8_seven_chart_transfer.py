#!/usr/bin/env python3
"""Exact transfer audit for the seven lex-critical n=8 chart types.

The frozen 31 by 31 support-incidence matrix has rank 24.  This checker
reconstructs its lexicographic contraction over QQ, including the source
kernel inclusion Sigma, target quotient pi, and contracting homotopy h.

The incidence matrix itself transfers to the zero map on the seven critical
source and target spaces.  More importantly, the incidence data contain no
higher filtered perturbation delta.  We certify this underdetermination by
constructing, for every 7 by 7 rational matrix B, a formal filtration-one
perturbation delta_B with the same leading incidence and transferred map

                 pi delta_B (I + h delta_B)^(-1) Sigma = B.

Thus the five extra target types 27--31 may all cancel, none may cancel, or
any intermediate rank may occur without changing the audited incidence.
"""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE_PATH = HERE / "verify_n8_target_triple_localization_orbits.py"
SPEC = importlib.util.spec_from_file_location("n8_target_charts", SOURCE_PATH)
CHARTS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHARTS)

SOURCE = CHARTS.SOURCE
QQ = Fraction

EXPECTED_LEDGER_SHA256 = (
    "66cb22aa359d67831e4bad5bc6e0cbf4c8fbf4ad1b96648374229200e8db6a06"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add_scaled(target, source, scale):
    for index, coefficient in source.items():
        value = target.get(index, QQ(0)) + scale * coefficient
        if value:
            target[index] = value
        else:
            target.pop(index, None)


def apply_columns(columns, vector):
    output = {}
    for index, coefficient in vector.items():
        add_scaled(output, columns[index], coefficient)
    return output


def unit(index):
    return {index: QQ(1)}


def rational_record(vector):
    return tuple(
        (index + 1, value.numerator, value.denominator)
        for index, value in sorted(vector.items())
    )


def matrix_rank(columns, row_count):
    """Exact sparse column rank over QQ."""
    pivots = {}
    for source in columns:
        vector = dict(source)
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            if pivot not in pivots:
                pivots[pivot] = {
                    row: coefficient / value
                    for row, coefficient in vector.items()
                }
                break
            add_scaled(vector, pivots[pivot], -value)
    require(all(0 <= pivot < row_count for pivot in pivots),
            "rank elimination produced an invalid row")
    return len(pivots)


def construct_incidence():
    rows = tuple(sorted(SOURCE.target_orbit_rows()))
    require(len(rows) == 31, "target chart count changed")
    row_index = {row: index for index, row in enumerate(rows)}
    support_columns = tuple(sorted(set().union(*(
        SOURCE.incident_columns(row) for row in rows
    ))))
    require(len(support_columns) == 31,
            "support-column orbit count changed")

    columns = []
    for support_column in support_columns:
        entries = Counter(
            row_index[output]
            for output in SOURCE.column_outputs(support_column)
            if output in row_index
        )
        columns.append({row: QQ(value) for row, value in entries.items()})
    require(matrix_rank(columns, 31) == 24,
            "support-incidence rank changed")
    return rows, support_columns, tuple(columns)


def lex_contraction(columns):
    """Return exact pivot images and a triangular source basis.

    Each processed original column produces one transformed source vector:
    either a normalized pivot representative or a zero representative.  The
    resulting 31 vectors are triangular in original-column order and form a
    basis.  This makes the kernel projection as explicit as the row
    contraction.
    """
    pivot_images = {}
    pivot_sources = {}
    zero_sources = {}
    transformed_by_column = {}

    for column_number, source in enumerate(columns):
        vector = dict(source)
        representative = unit(column_number)
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            if pivot not in pivot_images:
                image = {
                    row: coefficient / value
                    for row, coefficient in vector.items()
                }
                transformed = {
                    column: coefficient / value
                    for column, coefficient in representative.items()
                }
                require(apply_columns(columns, transformed) == image,
                        "pivot source provenance failed")
                require(image[pivot] == 1, "pivot did not normalize")
                require(all(row >= pivot for row in image),
                        "pivot image is not lex triangular")
                pivot_images[pivot] = image
                pivot_sources[pivot] = transformed
                transformed_by_column[column_number] = transformed
                break
            add_scaled(vector, pivot_images[pivot], -value)
            add_scaled(representative, pivot_sources[pivot], -value)
        if not vector:
            require(not apply_columns(columns, representative),
                    "zero representative is not a source syzygy")
            zero_sources[column_number] = representative
            transformed_by_column[column_number] = representative

    require(len(pivot_images) == 24, "lex pivot count changed")
    require(tuple(row + 1 for row in range(31) if row not in pivot_images)
            == (25, 26, 27, 28, 29, 30, 31),
            "critical target rows changed")
    require(tuple(column + 1 for column in sorted(zero_sources))
            == (18, 19, 21, 23, 26, 29, 31),
            "critical source columns changed")
    require(set(transformed_by_column) == set(range(31)),
            "triangular source basis is incomplete")
    for column_number, transformed in transformed_by_column.items():
        require(transformed.get(column_number, 0) != 0,
                "triangular source basis lost its diagonal")
        require(all(index <= column_number for index in transformed),
                "source transform is not triangular")
    return (pivot_images, pivot_sources, zero_sources,
            transformed_by_column)


class Contraction:
    def __init__(self, columns, pivot_images, pivot_sources, zero_sources,
                 transformed_by_column):
        self.columns = columns
        self.pivot_images = pivot_images
        self.pivot_sources = pivot_sources
        self.zero_sources = zero_sources
        self.transformed_by_column = transformed_by_column
        self.pivot_rows = tuple(sorted(pivot_images))
        self.critical_rows = tuple(
            row for row in range(31) if row not in pivot_images
        )
        self.critical_source_columns = tuple(sorted(zero_sources))

    def sigma(self, critical_vector):
        """Critical-source inclusion Sigma: QQ^7 -> QQ^31."""
        output = {}
        for index, coefficient in critical_vector.items():
            add_scaled(
                output,
                self.zero_sources[self.critical_source_columns[index]],
                coefficient,
            )
        return output

    def include_target(self, critical_vector):
        """Chosen target-section i_H: QQ^7 -> QQ^31."""
        return {
            self.critical_rows[index]: coefficient
            for index, coefficient in critical_vector.items()
            if coefficient
        }

    def h_and_pi(self, row_vector):
        """Lex row reduction y = D h(y) + i_H pi(y)."""
        work = dict(row_vector)
        source = {}
        for pivot in self.pivot_rows:
            coefficient = work.get(pivot, QQ(0))
            if not coefficient:
                continue
            add_scaled(source, self.pivot_sources[pivot], coefficient)
            add_scaled(work, self.pivot_images[pivot], -coefficient)
        require(all(row in self.critical_rows for row in work),
                "row reduction retained a pivot row")
        quotient = {
            self.critical_rows.index(row): coefficient
            for row, coefficient in work.items()
        }
        return source, quotient

    def h(self, row_vector):
        return self.h_and_pi(row_vector)[0]

    def pi(self, row_vector):
        return self.h_and_pi(row_vector)[1]

    def source_coordinates(self, source_vector):
        """Coordinates in the triangular transformed source basis."""
        work = dict(source_vector)
        coordinates = {}
        for column_number in reversed(range(31)):
            transformed = self.transformed_by_column[column_number]
            diagonal = transformed[column_number]
            coefficient = work.get(column_number, QQ(0)) / diagonal
            if coefficient:
                coordinates[column_number] = coefficient
                add_scaled(work, transformed, -coefficient)
        require(not work, "triangular source-coordinate solve failed")
        return coordinates

    def p_source(self, source_vector):
        coordinates = self.source_coordinates(source_vector)
        return {
            index: coordinates.get(column, QQ(0))
            for index, column in enumerate(self.critical_source_columns)
            if coordinates.get(column, QQ(0))
        }

    def audit_identities(self):
        # D h + i_H pi = identity on target rows.
        for row in range(31):
            target = unit(row)
            h_target, pi_target = self.h_and_pi(target)
            replay = apply_columns(self.columns, h_target)
            add_scaled(replay, self.include_target(pi_target), QQ(1))
            require(replay == target,
                    f"target contraction identity failed at row {row + 1}")

        # h D + Sigma p_K = identity on source columns.
        for column in range(31):
            source = unit(column)
            replay = self.h(self.columns[column])
            add_scaled(replay, self.sigma(self.p_source(source)), QQ(1))
            require(replay == source,
                    f"source contraction identity failed at column {column + 1}")

        for index in range(7):
            critical = unit(index)
            require(not apply_columns(self.columns, self.sigma(critical)),
                    "D Sigma is nonzero")
            require(self.p_source(self.sigma(critical)) == critical,
                    "p_K Sigma is not the identity")
            included = self.include_target(critical)
            require(not self.h(included), "h i_H is nonzero")
            require(self.pi(included) == critical,
                    "pi i_H is not the identity")
        for column in self.columns:
            require(not self.pi(column), "pi D is nonzero")


def apply_matrix(matrix_columns, vector):
    return apply_columns(matrix_columns, vector)


def elementary_matrix(row, column, size=7):
    return tuple(unit(row) if index == column else {} for index in range(size))


def diagonal_matrix(rank, size=7, start_row=0):
    columns = []
    for column in range(size):
        row = start_row + column
        columns.append(unit(row) if column < rank and row < size else {})
    return tuple(columns)


def delta_from_critical_matrix(contraction, matrix_columns, source_vector):
    """delta_B = i_H B p_K, viewed as filtration-one data."""
    critical_source = contraction.p_source(source_vector)
    critical_target = apply_matrix(matrix_columns, critical_source)
    return contraction.include_target(critical_target)


def transferred_matrix(contraction, matrix_columns):
    """Evaluate pi delta_B (I+h delta_B)^-1 Sigma exactly.

    Here h delta_B vanishes identically because delta_B lands in the chosen
    critical target section.  The inverse therefore terminates at order zero.
    """
    for column in range(31):
        delta_value = delta_from_critical_matrix(
            contraction, matrix_columns, unit(column)
        )
        require(not contraction.h(delta_value),
                "constructed h delta_B should vanish")
    output = []
    for critical_column in range(7):
        lifted = contraction.sigma(unit(critical_column))
        delta_value = delta_from_critical_matrix(
            contraction, matrix_columns, lifted
        )
        output.append(contraction.pi(delta_value))
    return tuple(output)


def coefficient_statistics(vectors):
    values = [coefficient for vector in vectors for coefficient in vector.values()]
    return {
        "nonzeros": len(values),
        "max_numerator_abs": max((abs(value.numerator) for value in values),
                                 default=0),
        "max_denominator": max((value.denominator for value in values),
                               default=1),
    }


def audit():
    rows, support_columns, incidence = construct_incidence()
    (pivot_images, pivot_sources, zero_sources,
     transformed_by_column) = lex_contraction(incidence)
    contraction = Contraction(
        incidence, pivot_images, pivot_sources, zero_sources,
        transformed_by_column,
    )
    contraction.audit_identities()

    sigma_columns = tuple(contraction.sigma(unit(index)) for index in range(7))
    pi_columns = tuple(contraction.pi(unit(index)) for index in range(31))
    h_columns = tuple(contraction.h(unit(index)) for index in range(31))
    p_source_columns = tuple(
        contraction.p_source(unit(index)) for index in range(31)
    )

    # The only differential supplied by the incidence ledger is D itself,
    # and its induced map from ker D to coker D is exactly zero.
    incidence_transfer = tuple(
        contraction.pi(apply_columns(incidence, sigma_column))
        for sigma_column in sigma_columns
    )
    require(incidence_transfer == ({},) * 7,
            "leading incidence has a nonzero critical transfer")

    # The map B -> transferred(delta_B) is the identity on all 49 matrix
    # units.  Hence leading incidence alone imposes no condition at all on a
    # later seven-by-seven differential.
    for row in range(7):
        for column in range(7):
            matrix = elementary_matrix(row, column)
            require(transferred_matrix(contraction, matrix) == matrix,
                    f"elementary transfer E_{row + 1},{column + 1} failed")

    possible_ranks = []
    for rank in range(8):
        matrix = diagonal_matrix(rank)
        transfer = transferred_matrix(contraction, matrix)
        possible_ranks.append(matrix_rank(transfer, 7))
    require(possible_ranks == list(range(8)),
            "not every critical transfer rank was realized")

    # An explicit rank-five perturbation kills target chart rows 27--31 and
    # leaves precisely rows 25 and 26 in the critical cokernel.
    reduce_to_25_26 = tuple(
        unit(column + 2) if column < 5 else {} for column in range(7)
    )
    require(matrix_rank(reduce_to_25_26, 7) == 5,
            "two-chart reduction witness lost rank")
    require(transferred_matrix(contraction, reduce_to_25_26)
            == reduce_to_25_26,
            "two-chart reduction transfer replay failed")
    perturbed_columns = []
    for column in range(31):
        output = dict(incidence[column])
        add_scaled(
            output,
            delta_from_critical_matrix(
                contraction, reduce_to_25_26, unit(column)
            ),
            QQ(1),
        )
        perturbed_columns.append(output)
    require(matrix_rank(perturbed_columns, 31) == 29,
            "rank-five formal perturbation did not raise total rank to 29")

    contraction_record = {
        "sigma": [rational_record(column) for column in sigma_columns],
        "pi": [rational_record(column) for column in pi_columns],
        "h": [rational_record(column) for column in h_columns],
        "p_source": [
            rational_record(column) for column in p_source_columns
        ],
    }
    contraction_digest = sha256(json.dumps(
        contraction_record, separators=(",", ":"), sort_keys=True
    ).encode()).hexdigest()

    return {
        "leading_incidence_shape": [31, 31],
        "leading_incidence_rank": 24,
        "critical_target_charts": [25, 26, 27, 28, 29, 30, 31],
        "critical_source_column_types": [18, 19, 21, 23, 26, 29, 31],
        "critical_dimensions": [7, 7],
        "incidence_transferred_rank": 0,
        "incidence_transferred_nonzeros": 0,
        "sigma_statistics": coefficient_statistics(sigma_columns),
        "pi_statistics": coefficient_statistics(pi_columns),
        "h_statistics": coefficient_statistics(h_columns),
        "source_projection_statistics": coefficient_statistics(
            p_source_columns
        ),
        "contraction_sha256": contraction_digest,
        "formal_higher_transfer_dimension": 49,
        "formal_higher_transfer_possible_ranks": possible_ranks,
        "rank_five_witness_pairs": [
            [18, 27], [19, 28], [21, 29], [23, 30], [26, 31]
        ],
        "rank_five_witness_total_rank": 29,
        "rank_five_witness_surviving_target_charts": [25, 26],
        "delta_determined_by_incidence": False,
        "minimal_first_order_extra_data": (
            "the 7x7 compressed block pi*delta_r*Sigma (49 rational "
            "coefficients) at the first nonzero filtration r"
        ),
        "minimal_all_orders_extra_data": (
            "source-labelled higher-filter column outputs, with exact "
            "coefficients/orbit normalizations and filtration degrees, on "
            "every matched source reached by repeated h*delta"
        ),
    }


def main():
    ledger = audit()
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                "frozen seven-chart transfer ledger changed")
    print(
        "n=8 seven-chart transfer: PASS; incidence transfer is zero; "
        "higher delta absent and all critical ranks 0..7 are compatible"
    )
    print(json.dumps(ledger, sort_keys=True))
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
