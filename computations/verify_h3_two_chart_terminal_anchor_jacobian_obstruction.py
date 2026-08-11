#!/usr/bin/env python3
"""Exact Jacobian obstruction at the physical terminal separator.

At the zero-target packet of b72402c, compute the complete 6561 by 252
Jacobian of the eight-site matching tensor.  The two pure target words 0^8
and 1^8 are absent from its row support, so Delta is not a tangent value.
"""

from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import importlib.util
import json


EXPECTED_BASE_SHA256 = "0d108f53014a52751b61f459ac9ea8a017e09a153fec5c9d8cbd970a7553d9ef"
EXPECTED_DIGEST = "7338d531a873d299c7f7fa130655e0d9b923918f5f9d4469af34a9182ee30c29"
COLORS = tuple(range(3))
SITES = tuple(range(8))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_base():
    path = Path(__file__).with_name(
        "verify_h3_two_chart_terminal_zero_target_counterguard.py")
    digest = sha256(path.read_bytes()).hexdigest()
    require(digest == EXPECTED_BASE_SHA256,
            f"base terminal guard changed: {digest}")
    spec = importlib.util.spec_from_file_location("terminal_zero_guard", path)
    require(spec is not None and spec.loader is not None, "cannot load base guard")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def word_index(word):
    return sum(colour * 3 ** (7 - site) for site, colour in enumerate(word))


def exact_rank(vectors):
    """Sparse column rank over Q, returning normalized pivot columns."""
    basis = {}
    for original in vectors:
        vector = {key: F(value) for key, value in original.items() if value}
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            if pivot not in basis:
                vector = {key: entry / value for key, entry in vector.items()}
                basis[pivot] = vector
                break
            row = basis[pivot]
            for key, entry in row.items():
                new_value = vector.get(key, F(0)) - value * entry
                if new_value:
                    vector[key] = new_value
                elif key in vector:
                    del vector[key]
    return len(basis), basis


def jacobian_columns(base, cells):
    coordinates = [
        (x, y, a, b)
        for x in SITES for y in SITES if x < y
        for a in COLORS for b in COLORS
    ]
    columns = []
    for x, y, a, b in coordinates:
        residual = tuple(site for site in SITES if site not in (x, y))
        column = {}
        for residual_word in product(COLORS, repeat=6):
            partial = dict(zip(residual, residual_word))
            value = base.tensor_coefficient(cells, residual, partial)
            if not value:
                continue
            word = [0] * 8
            word[x], word[y] = a, b
            for site, colour in partial.items():
                word[site] = colour
            column[word_index(word)] = value
        columns.append(column)
    return coordinates, columns


def maximum_base_edges(base, cells, colour):
    best = 0
    for matching in base.matchings(SITES):
        count = sum(
            1 for x, y in matching
            if base.cell(cells, x, y, colour, colour)
        )
        best = max(best, count)
    return best


def main():
    base = load_base()
    cells, *_ = base.make_cells()
    coordinates, columns = jacobian_columns(base, cells)

    require(len(coordinates) == 252, "wrong physical coordinate count")
    support = set().union(*(column.keys() for column in columns))
    nonzeros = sum(len(column) for column in columns)
    require(len(support) == 501, f"Jacobian row support moved: {len(support)}")
    require(nonzeros == 999, f"Jacobian nonzero count moved: {nonzeros}")

    jacobian_rank, _ = exact_rank(columns)
    require(jacobian_rank == 131, f"Jacobian rank moved: {jacobian_rank}")

    pure_indices = [word_index([colour] * 8) for colour in COLORS]
    require(pure_indices == [0, 3280, 6560], "pure word indices moved")
    pure_support = [index in support for index in pure_indices]
    require(pure_support == [False, False, True],
            f"pure Jacobian support moved: {pure_support}")

    delta = {index: F(1) for index in pure_indices}
    augmented_rank, _ = exact_rank(columns + [delta])
    require(augmented_rank == 132,
            f"Delta did not raise Jacobian rank: {augmented_rank}")

    individual_augmented = [
        exact_rank(columns + [{index: F(1)}])[0]
        for index in pure_indices
    ]
    require(individual_augmented == [132, 132, 131],
            f"individual pure ranks moved: {individual_augmented}")

    # The primitive integral separator is simply evaluation at 0^8 (and,
    # independently, at 1^8): every Jacobian column has value zero there,
    # while Delta has value one.
    require(all(column.get(pure_indices[0], F(0)) == 0 for column in columns),
            "0^8 is not a left Jacobian covector")
    require(delta[pure_indices[0]] == 1, "0^8 does not detect Delta")

    # Explain the failure by the pure support at the base point.  Colour 0
    # has only the disjoint base edges 01 and 67, so a pure-0 anchor first
    # appears at perturbation order two.  Colour 1 has only 67 and first
    # appears at order three.  Colour 2 has a cancelling order-zero tensor
    # but a nonzero first derivative.
    max_base = [maximum_base_edges(base, cells, colour) for colour in COLORS]
    require(max_base[:2] == [2, 1], f"pure base matchings moved: {max_base}")
    first_possible_orders = [4 - max_base[0], 4 - max_base[1], 1]
    require(first_possible_orders == [2, 3, 1],
            "pure anchor onset orders moved")

    pure_two_columns = [
        (coordinates[index], column[pure_indices[2]])
        for index, column in enumerate(columns)
        if pure_indices[2] in column
    ]
    require(len(pure_two_columns) == 9,
            f"pure-2 derivative support moved: {len(pure_two_columns)}")

    ledger = {
        "scope": "complete H8 Jacobian at b72402c physical zero-target packet",
        "shape": [6561, 252],
        "row_support": len(support),
        "nonzeros": nonzeros,
        "rank_Q": jacobian_rank,
        "rank_with_Delta": augmented_rank,
        "pure_word_in_support": pure_support,
        "pure_individual_augmented_ranks": individual_augmented,
        "primitive_left_separator": "coefficient_at_0^8",
        "pure_anchor_first_possible_orders": first_possible_orders,
        "pure_2_derivative_columns": len(pure_two_columns),
        "verdict": "Delta_not_in_complete_matching_tensor_tangent_image",
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST, f"ledger changed: {digest}")

    print("h=3 terminal anchor Jacobian obstruction: PASS")
    print(f"Jacobian rank {jacobian_rank}/252; augmented rank {augmented_rank}")
    print("primitive left separator: coefficient at 0^8")
    print(f"pure anchor onset orders: {first_possible_orders}")
    print(f"ledger sha256: {digest}")


if __name__ == "__main__":
    main()
