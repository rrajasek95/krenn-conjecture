#!/usr/bin/env python3
"""Exact lightweight checks for the double-zero common-label repair.

This script has no third-party dependencies.  It checks:

* every two-missing-label grid and {-1,0,1} coefficient pattern;
* the explicit rank-one singleton detectors and hook repairs;
* the extended-detector opposite-diagonal exception; and
* the exact eight-site disjoint-detector guard.

It deliberately does not run the heavier bounded SAT/CEGAR searches.
"""

from fractions import Fraction
from itertools import product


if not __debug__:
    raise RuntimeError("run this exact checker without Python -O")


MISSING = (1, 2)
COORDINATES = tuple(product(MISSING, repeat=2))
VALUES = (-1, 0, 1)


def matrix_rank(rows):
    """Rank over Q for a possibly empty rectangular matrix."""
    rows = [list(map(Fraction, row)) for row in rows]
    if not rows:
        return 0
    column_count = len(rows[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, len(rows)) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        scale = rows[pivot_row][column]
        rows[pivot_row] = [value / scale for value in rows[pivot_row]]
        for row in range(len(rows)):
            if row == pivot_row or not rows[row][column]:
                continue
            scale = rows[row][column]
            rows[row] = [
                value - scale * pivot_value
                for value, pivot_value in zip(rows[row], rows[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return pivot_row


def nonempty_subsets(values):
    values = tuple(values)
    return tuple(
        frozenset(value for bit, value in enumerate(values) if mask & (1 << bit))
        for mask in range(1, 1 << len(values))
    )


def embedded_vector(matrix):
    return tuple(Fraction(matrix.get(coordinate, 0)) for coordinate in COORDINATES)


def unit_vector(label):
    return tuple(Fraction(int(coordinate == (label, label))) for coordinate in COORDINATES)


def pairing(functional, matrix):
    return sum(
        Fraction(functional.get(coordinate, 0)) * Fraction(matrix.get(coordinate, 0))
        for coordinate in COORDINATES
    )


def functional_rank(functional):
    return matrix_rank(
        [[functional.get((row, column), 0) for column in MISSING] for row in MISSING]
    )


def pure_diagonal_label(matrix):
    support = {coordinate for coordinate, value in matrix.items() if value}
    for label in MISSING:
        if support == {(label, label)}:
            return label
    return None


def detector_set(rows, columns, matrix):
    """Compute detector existence by exact rank separation."""
    result = set()
    direct = embedded_vector(matrix)
    for label in MISSING:
        if label not in rows or label not in columns:
            continue
        diagonal = unit_vector(label)
        if matrix_rank([direct, diagonal]) > matrix_rank([direct]):
            result.add(label)
    return frozenset(result)


def predicted_detector_set(rows, columns, matrix):
    result = set()
    pure_label = pure_diagonal_label(matrix)
    for label in MISSING:
        if label in rows and label in columns and pure_label != label:
            result.add(label)
    return frozenset(result)


def singleton_detector(rows, columns, matrix, target):
    """The explicit functional in equation (5)."""
    other = next(label for label in MISSING if label != target)
    if rows == frozenset((target,)) and columns == frozenset(MISSING):
        denominator = Fraction(matrix[(target, other)])
        assert denominator
        return {
            (target, target): Fraction(1),
            (target, other): -Fraction(matrix.get((target, target), 0)) / denominator,
        }
    if rows == frozenset(MISSING) and columns == frozenset((target,)):
        denominator = Fraction(matrix[(other, target)])
        assert denominator
        return {
            (target, target): Fraction(1),
            (other, target): -Fraction(matrix.get((target, target), 0)) / denominator,
        }
    assert rows == columns == frozenset(MISSING)
    assert pure_diagonal_label(matrix) == other
    return {(target, target): Fraction(1)}


def singleton_shape_holds(rows, columns, matrix, target):
    other = next(label for label in MISSING if label != target)
    row_hook = (
        rows == frozenset((target,))
        and columns == frozenset(MISSING)
        and bool(matrix.get((target, other), 0))
    )
    column_hook = (
        rows == frozenset(MISSING)
        and columns == frozenset((target,))
        and bool(matrix.get((other, target), 0))
    )
    opposite_diagonal = (
        rows == columns == frozenset(MISSING)
        and pure_diagonal_label(matrix) == other
    )
    return sum(map(bool, (row_hook, column_hook, opposite_diagonal))) == 1


def empty_boundary_holds(rows, columns, matrix):
    intersection = rows & columns
    if not intersection:
        return len(rows) == len(columns) == 1
    if len(intersection) == 1:
        label = next(iter(intersection))
        return pure_diagonal_label(matrix) == label
    return False


def matrices_on_grid(rows, columns):
    grid = tuple(product(sorted(rows), sorted(columns)))
    for values in product(VALUES, repeat=len(grid)):
        if not any(values):
            continue
        yield {coordinate: value for coordinate, value in zip(grid, values) if value}


def verify_detector_classification():
    packet_count = 0
    singleton_count = 0
    hook_repair_count = 0
    subsets = nonempty_subsets(MISSING)
    for rows in subsets:
        for columns in subsets:
            for matrix in matrices_on_grid(rows, columns):
                packet_count += 1
                detected = detector_set(rows, columns, matrix)
                assert detected == predicted_detector_set(rows, columns, matrix)
                assert (not detected) == empty_boundary_holds(rows, columns, matrix)
                if len(detected) == 1:
                    singleton_count += 1
                    target = next(iter(detected))
                    assert singleton_shape_holds(rows, columns, matrix, target)
                    functional = singleton_detector(rows, columns, matrix, target)
                    other = next(label for label in MISSING if label != target)
                    assert pairing(functional, matrix) == 0
                    assert functional[(target, target)] == 1
                    assert functional.get((other, other), 0) == 0
                    assert functional_rank(functional) == 1
                    is_row_hook = rows == frozenset((target,))
                    is_column_hook = columns == frozenset((target,))
                    if is_row_hook or is_column_hook:
                        requested = other
                        mandatory = (
                            (target, requested)
                            if is_row_hook
                            else (requested, target)
                        )
                        denominator = Fraction(matrix[mandatory])
                        for outside_diagonal in (-2, -1, 0, 1, 2):
                            full_direct = dict(matrix)
                            if outside_diagonal:
                                full_direct[(requested, requested)] = outside_diagonal
                            repaired = {
                                (requested, requested): Fraction(1),
                                mandatory: -Fraction(outside_diagonal) / denominator,
                            }
                            repaired = {
                                key: value for key, value in repaired.items() if value
                            }
                            assert pairing(repaired, full_direct) == 0
                            assert repaired.get((requested, requested), 0) == 1
                            assert repaired.get((target, target), 0) == 0
                            assert functional_rank(repaired) == 1
                            hook_repair_count += 1
    assert packet_count == 120
    assert singleton_count == 28
    assert hook_repair_count == 120
    return packet_count, singleton_count, hook_repair_count


def all_missing_matrices():
    for values in product(VALUES, repeat=len(COORDINATES)):
        if not any(values):
            continue
        yield {
            coordinate: value
            for coordinate, value in zip(COORDINATES, values)
            if value
        }


def extended_detector_set(matrix):
    pure_label = pure_diagonal_label(matrix)
    return frozenset(label for label in MISSING if label != pure_label)


def two_coordinate_repair(matrix, target):
    assert target in extended_detector_set(matrix)
    candidates = [
        coordinate
        for coordinate, value in matrix.items()
        if value and coordinate != (target, target)
    ]
    # Prefer an off-diagonal cell: on two labels this makes the repair rank one.
    coordinate = next(
        (item for item in candidates if item[0] != item[1]),
        candidates[0],
    )
    functional = {
        (target, target): Fraction(1),
        coordinate: -Fraction(matrix.get((target, target), 0))
        / Fraction(matrix[coordinate]),
    }
    return coordinate, {key: value for key, value in functional.items() if value}


def verify_extended_repairs():
    matrices = tuple(all_missing_matrices())
    repair_count = 0
    for matrix in matrices:
        for target in extended_detector_set(matrix):
            coordinate, functional = two_coordinate_repair(matrix, target)
            assert pairing(functional, matrix) == 0
            assert functional.get((target, target), 0) == 1
            if coordinate[0] != coordinate[1]:
                assert functional_rank(functional) == 1
                other = next(label for label in MISSING if label != target)
                assert functional.get((other, other), 0) == 0
            repair_count += 1

    pair_count = 0
    exceptional_count = 0
    for left in matrices:
        for right in matrices:
            pair_count += 1
            disjoint = not (extended_detector_set(left) & extended_detector_set(right))
            left_label = pure_diagonal_label(left)
            right_label = pure_diagonal_label(right)
            expected = (
                left_label is not None
                and right_label is not None
                and left_label != right_label
            )
            assert disjoint == expected
            exceptional_count += int(disjoint)
    assert len(matrices) == 80
    # Two ordered projective patterns, with two nonzero test scalars on each
    # side, give eight concrete instances in the {-1,0,1} census.
    assert exceptional_count == 8
    return repair_count, pair_count, exceptional_count


P_SITE, Q_SITE, R_SITE, A_SITE, B_SITE, C_SITE, D_SITE, E_SITE = range(8)
SITES = tuple(range(8))
COLORS = tuple(range(3))
COMMON = (A_SITE, B_SITE, C_SITE, D_SITE, E_SITE)


def zero_block():
    return [[0 for _ in COLORS] for _ in COLORS]


def build_guard_blocks():
    blocks = {}

    def add(left, right, left_color, right_color, value=1):
        if left > right:
            left, right = right, left
            left_color, right_color = right_color, left_color
        block = blocks.setdefault((left, right), zero_block())
        block[left_color][right_color] += value

    cells = (
        (P_SITE, A_SITE, 0, 0),
        (Q_SITE, B_SITE, 0, 0),
        (R_SITE, C_SITE, 0, 0),
        (D_SITE, E_SITE, 0, 0),
        (Q_SITE, R_SITE, 1, 1),
        (P_SITE, E_SITE, 1, 1),
        (A_SITE, B_SITE, 1, 1),
        (C_SITE, D_SITE, 1, 1),
        (Q_SITE, R_SITE, 2, 2),
        (P_SITE, D_SITE, 2, 2),
        (A_SITE, C_SITE, 2, 2),
        (B_SITE, E_SITE, 2, 2),
        (P_SITE, Q_SITE, 1, 2),
        (P_SITE, Q_SITE, 1, 0),
        (P_SITE, R_SITE, 2, 1),
        (P_SITE, R_SITE, 2, 0),
    )
    for cell in cells:
        add(*cell)
    return blocks


BLOCKS = build_guard_blocks()


def entry(left, right, left_color, right_color):
    if left < right:
        block = BLOCKS.get((left, right))
        return 0 if block is None else block[left_color][right_color]
    block = BLOCKS.get((right, left))
    return 0 if block is None else block[right_color][left_color]


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for matching in perfect_matchings(rest):
            yield ((first, second),) + matching


def matching_tensor(vertices):
    vertices = tuple(vertices)
    tensor = {}
    for matching in perfect_matchings(vertices):
        choices = []
        for left, right in matching:
            decorated = [
                (left_color, right_color, entry(left, right, left_color, right_color))
                for left_color in COLORS
                for right_color in COLORS
                if entry(left, right, left_color, right_color)
            ]
            if not decorated:
                break
            choices.append((left, right, decorated))
        else:
            for selected in product(*(decorated for _, _, decorated in choices)):
                word = {}
                coefficient = 1
                for (left, right, _), (left_color, right_color, value) in zip(
                    choices, selected
                ):
                    word[left] = left_color
                    word[right] = right_color
                    coefficient *= value
                key = tuple(word[site] for site in vertices)
                tensor[key] = tensor.get(key, 0) + coefficient
    return {word: coefficient for word, coefficient in tensor.items() if coefficient}


def channel(endpoint, deleted, pure_color=0):
    residual = [site for site in SITES if site not in (endpoint, deleted)]
    return frozenset(
        endpoint_color
        for endpoint_color in COLORS
        if any(
            entry(endpoint, site, endpoint_color, pure_color)
            for site in residual
        )
    )


def star_rank(endpoint, deleted):
    residual = [site for site in SITES if site not in (endpoint, deleted)]
    rows = [
        [
            entry(endpoint, site, endpoint_color, residual_color)
            for site in residual
            for residual_color in COLORS
        ]
        for endpoint_color in COLORS
    ]
    return matrix_rank(rows)


def gamma(i, j, k):
    total = 0
    for p_site in COMMON:
        for q_site in COMMON:
            if q_site == p_site:
                continue
            for r_site in COMMON:
                if r_site in (p_site, q_site):
                    continue
                residual = [
                    site for site in COMMON if site not in (p_site, q_site, r_site)
                ]
                total += (
                    entry(P_SITE, p_site, i, 0)
                    * entry(Q_SITE, q_site, j, 0)
                    * entry(R_SITE, r_site, k, 0)
                    * entry(residual[0], residual[1], 0, 0)
                )
    return total


def verify_guard():
    expected_words = {
        tuple(map(int, word)): 1
        for word in (
            "00000000",
            "11111111",
            "22222222",
            "01102112",
            "02202112",
            "10011000",
            "12011000",
            "12211111",
            "20020200",
            "20120200",
            "21122222",
        )
    }
    tensor = matching_tensor(SITES)
    assert tensor == expected_words

    pq_channels = (
        channel(P_SITE, Q_SITE),
        channel(Q_SITE, P_SITE),
    )
    pr_channels = (
        channel(P_SITE, R_SITE),
        channel(R_SITE, P_SITE),
    )
    assert pq_channels == (frozenset((0, 2)), frozenset((0,)))
    assert pr_channels == (frozenset((0, 1)), frozenset((0,)))

    p_block = BLOCKS[(P_SITE, Q_SITE)]
    r_block = BLOCKS[(P_SITE, R_SITE)]
    p_compression = {(1, 1): p_block[1][1], (1, 2): p_block[1][2]}
    r_compression = {(2, 1): r_block[2][1], (2, 2): r_block[2][2]}
    p_compression = {key: value for key, value in p_compression.items() if value}
    r_compression = {key: value for key, value in r_compression.items() if value}
    assert detector_set(frozenset((1,)), frozenset((1, 2)), p_compression) == frozenset((1,))
    assert detector_set(frozenset((2,)), frozenset((1, 2)), r_compression) == frozenset((2,))

    for endpoint, deleted in (
        (P_SITE, Q_SITE),
        (Q_SITE, P_SITE),
        (P_SITE, R_SITE),
        (R_SITE, P_SITE),
    ):
        assert star_rank(endpoint, deleted) == 3

    for left, right in ((P_SITE, Q_SITE), (P_SITE, R_SITE)):
        for color in COLORS:
            fiber = {
                word: coefficient
                for word, coefficient in tensor.items()
                if word[left] == word[right] == color
            }
            assert fiber == {(color,) * len(SITES): 1}
        for left_color in COLORS:
            for right_color in COLORS:
                if left_color == right_color:
                    continue
                assert any(
                    word[left] == left_color and word[right] == right_color
                    for word in tensor
                )

    pq_residual = tuple(site for site in SITES if site not in (P_SITE, Q_SITE))
    pr_residual = tuple(site for site in SITES if site not in (P_SITE, R_SITE))
    for residual in (pq_residual, pr_residual):
        internal = matching_tensor(residual)
        assert (0,) * len(residual) not in internal
        for defect_site in range(len(residual)):
            for defect_color in (1, 2):
                word = [0] * len(residual)
                word[defect_site] = defect_color
                assert tuple(word) not in internal

    for i in COLORS:
        for j in COLORS:
            for k in COLORS:
                assert gamma(i, j, k) == int(i == j == k == 0)

    direct_a = entry(P_SITE, Q_SITE, 1, 2)
    direct_b = entry(P_SITE, R_SITE, 1, 0)
    direct_f = entry(Q_SITE, C_SITE, 2, 0)
    direct_u = entry(R_SITE, C_SITE, 0, 0)
    assert direct_a == direct_u == 1
    assert direct_b == direct_f == 0
    assert direct_a * direct_u - direct_b * direct_f == 1
    return len(tensor)


def main():
    packet_count, singleton_count, hook_repair_count = verify_detector_classification()
    repair_count, pair_count, exceptional_count = verify_extended_repairs()
    word_count = verify_guard()
    print(
        "detector classification: PASS "
        f"({packet_count} packets, {singleton_count} singleton packets, "
        f"{hook_repair_count} hook repairs)"
    )
    print(
        "one-coordinate repairs: PASS "
        f"({repair_count} repairs, {pair_count} chart pairs, "
        f"{exceptional_count} ordered opposite-diagonal exceptions)"
    )
    print(f"eight-site disjoint-detector guard: PASS ({word_count} words)")


if __name__ == "__main__":
    main()
