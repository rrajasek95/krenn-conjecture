#!/usr/bin/env python3
"""Exact linear-L0 incidence survivor on the dense transverse ray.

Keep the determined transverse core and replace only the eight zero-sum
core-to-zero blocks.  The resulting packet has differential rank 55,
mixed-row rank 53, and both pure coordinate targets in its tangent image
over Q and three prime fields.  It retains invertible zero-site spokes but
fails literal R2 at exactly root 0.

Standard library only; checks remain live under python -O and python -I -S.
"""

from itertools import product
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
guard = run_path(str(
    HERE / "verify_level_two_two_invertible_transverse_column_potential_boundary.py"
))
old_survivor = run_path(str(
    HERE / "verify_level_two_two_invertible_l0_incidence_survivor.py"
))
l0_core = run_path(str(
    HERE / "verify_level_two_three_invertible_l0_obstruction.py"
))

rank_core = guard["rank_core"]
dense_core = guard["dense_core"]
SITES = guard["SITES"]
COLOURS = guard["COLOURS"]
EDGES = guard["EDGES"]
CELLS = guard["CELLS"]
WORDS = rank_core["WORDS"]
X = guard["X"]
POTENTIAL = guard["DENSE_POTENTIAL"]
J = guard["J"]
ZERO_MATRIX = guard["ZERO_MATRIX"]
FREE_EDGES = frozenset(old_survivor["FREE_EDGES"])
PRIMES = (101, 32_003, 1_000_003)

REPLACEMENT = dict(old_survivor["REPLACEMENT"])
REPLACEMENT[0, 4] = ((1, 85), (0, 87))

BLOCKS = dict(guard["CORE_BLOCKS"])
BLOCKS.update(REPLACEMENT)
BLOCKS[4, 5] = ZERO_MATRIX
PACKET = {
    (u, v, a, b): BLOCKS[u, v][a][b]
    for u, v in EDGES
    for a, b in product(COLOURS, repeat=2)
}


def append_columns(matrix, *columns):
    return [
        row[:] + [column[index] for column in columns]
        for index, row in enumerate(matrix)
    ]


def ranks_over_fields(matrix):
    return (
        dense_core["rational_rank"](matrix),
        *(rank_core["rank_mod"](matrix, prime) for prime in PRIMES),
    )


def audit_replacement_scope():
    require(frozenset(REPLACEMENT) == FREE_EDGES,
            "transverse replacement does not cover the eight free blocks")
    require(all(
        POTENTIAL[u] + POTENTIAL[v] == 0
        for u, v in REPLACEMENT
    ), "a transverse replacement block has nonzero multiplier")

    changed_from_old = {
        pair: BLOCKS[pair]
        for pair in FREE_EDGES
        if BLOCKS[pair] != old_survivor["REPLACEMENT"][pair]
    }
    require(changed_from_old == {
        (0, 4): ((1, 85), (0, 87)),
    }, ("the one-cell incidence lift changed", changed_from_old))
    return changed_from_old


def audit_generic_kernel_and_selected_rows():
    numerator = {}
    checks = 0
    for pair in EDGES:
        block = dense_core["matrix_product"](
            dense_core["matrix_product"](X[pair[0]], J),
            dense_core["transpose"](X[pair[1]]),
        )
        numerator[pair] = block
        multiplier = POTENTIAL[pair[0]] + POTENTIAL[pair[1]]
        for a, b in product(COLOURS, repeat=2):
            require(
                block[a][b] == multiplier * BLOCKS[pair][a][b],
                ("transverse survivor generic-kernel equation failed",
                 pair, a, b),
            )
            checks += 1

    derivative = rank_core["differential"](PACKET)
    numerator_vector = [
        numerator[u, v][a][b]
        for u, v, a, b in CELLS
    ]
    tangent = rank_core["matrix_vector_product"](
        derivative, numerator_vector
    )
    slope = [
        rank_core["hafnian"](PACKET, SITES, word)
        for word in WORDS
    ]
    direct_value = -sum(POTENTIAL)
    require(direct_value == -1,
            ("transverse survivor direct value changed", direct_value))
    require(all(
        direct_value * slope_value + tangent_value == 0
        for slope_value, tangent_value in zip(slope, tangent)
    ), "a transverse survivor selected row failed")
    return checks, slope


def gauge_tangent(mu):
    return [
        (mu[u] + mu[v]) * PACKET[u, v, a, b]
        for u, v, a, b in CELLS
    ]


def audit_rank_and_kernel():
    derivative = rank_core["differential"](PACKET)
    ranks = ranks_over_fields(derivative)
    require(ranks == (55, 55, 55, 55),
            ("transverse survivor rank changed", ranks))

    gauges = []
    for basis in range(5):
        mu = [0] * 6
        mu[basis] = 1
        mu[5] = -1
        tangent = gauge_tangent(mu)
        require(not any(rank_core["matrix_vector_product"](
            derivative, tangent
        )), ("transverse survivor gauge left the kernel", basis))
        gauges.append(tangent)
    require(dense_core["rational_rank"](gauges) == 5,
            "transverse survivor gauges became dependent")
    return derivative, ranks


def audit_l0_incidence(derivative):
    formal_slices = l0_core["audit_matching_partition_and_slice_formula"]()
    require(formal_slices == 256, "formal L0 slice count changed")

    slope = [
        rank_core["hafnian"](PACKET, SITES, word)
        for word in WORDS
    ]
    radial = [PACKET[cell] for cell in CELLS]
    require(
        rank_core["matrix_vector_product"](derivative, radial)
        == [3 * value for value in slope],
        "transverse survivor Euler identity failed",
    )

    pure_zero = [int(word == (0,) * 6) for word in WORDS]
    pure_one = [int(word == (1,) * 6) for word in WORDS]
    mixed = [
        row
        for row, word in zip(derivative, WORDS)
        if word not in ((0,) * 6, (1,) * 6)
    ]
    ranks = {
        "D": ranks_over_fields(derivative),
        "D_mixed": ranks_over_fields(mixed),
        "D|e0": ranks_over_fields(
            append_columns(derivative, pure_zero)
        ),
        "D|e1": ranks_over_fields(
            append_columns(derivative, pure_one)
        ),
        "D|e0,e1": ranks_over_fields(
            append_columns(derivative, pure_zero, pure_one)
        ),
    }
    require(ranks == {
        "D": (55, 55, 55, 55),
        "D_mixed": (53, 53, 53, 53),
        "D|e0": (55, 55, 55, 55),
        "D|e1": (55, 55, 55, 55),
        "D|e0,e1": (55, 55, 55, 55),
    }, ("transverse survivor L0 ranks changed", ranks))
    return formal_slices, ranks


def orient_block(root, neighbour):
    if root < neighbour:
        return BLOCKS[root, neighbour]
    return dense_core["transpose"](BLOCKS[neighbour, root])


def audit_r2_boundary():
    tables = {}
    passing = []
    failing = []
    for root in SITES:
        p_block, q_block = guard["endpoint_blocks"](root)
        incident = {
            neighbour: orient_block(root, neighbour)
            for neighbour in SITES
            if neighbour != root
        }
        incident["p"] = p_block
        incident["q"] = q_block
        pure = {
            output: tuple(
                label
                for label, block in incident.items()
                if guard["pure_column"](block, output)
            )
            for output in COLOURS
        }
        has_exit = (
            pure[0]
            and pure[1]
            and any(left != right for left in pure[0] for right in pure[1])
        )
        (passing if has_exit else failing).append(root)
        tables[root] = pure

    require(passing == [1, 2, 3, 4, 5] and failing == [0],
            ("transverse survivor R2 boundary changed", passing, failing))
    require(tables[0][0] and not tables[0][1],
            ("root 0 did not fail in exactly output one", tables[0]))
    require(dense_core["rational_rank"](X[0]) == 2,
            "the failing R2 root is no longer invertible")
    return tables, tuple(passing), tuple(failing)


def determinant(block):
    return block[0][0] * block[1][1] - block[0][1] * block[1][0]


def audit_invertible_spokes():
    determinants = {
        zero: {
            core: determinant(BLOCKS[core, zero])
            for core in (0, 1, 2, 3)
        }
        for zero in (4, 5)
    }
    require(all(
        any(value for value in choices.values())
        for choices in determinants.values()
    ), ("a transverse survivor zero lost invertible spokes", determinants))
    return determinants


def main():
    changed = audit_replacement_scope()
    generic, slope = audit_generic_kernel_and_selected_rows()
    derivative, differential_ranks = audit_rank_and_kernel()
    formal, incidence = audit_l0_incidence(derivative)
    r2, passing, failing = audit_r2_boundary()
    spokes = audit_invertible_spokes()
    print("dense transverse L0 incidence survivor: all checks passed")
    print(f"  one-cell lift                  : {changed}")
    print(f"  generic scalars/selected rows : {generic}/64")
    print(f"  slope support                 : {sum(value != 0 for value in slope)}/64")
    print(f"  differential ranks           : {differential_ranks}")
    print(f"  formal slices/L0 ranks       : {formal}, {incidence}")
    print(f"  R2 passing/failing roots      : {passing}/{failing}")
    print(f"  invertible-spoke determinants : {spokes}")


if __name__ == "__main__":
    main()
