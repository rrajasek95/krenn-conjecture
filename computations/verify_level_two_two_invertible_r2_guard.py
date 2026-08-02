#!/usr/bin/env python3
"""Exact 2I+2R+2Z rank-55 guard for the generic kernel and R2."""

from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
core = run_path(str(HERE / "verify_level_two_three_invertible_r2_guard.py"))

SITES = tuple(range(6))
COLOURS = (0, 1)
EDGES = tuple(combinations(SITES, 2))
CELLS = tuple(
    (u, v, a, b)
    for u, v in EDGES
    for a, b in product(COLOURS, repeat=2)
)
J = ((0, 1), (1, 0))
RHO = (1, 1, 1, 1, -1, -1)
Z_VALUE = Q(-1)

X = {
    0: ((1, 0), (0, 1)),
    1: ((1, 0), (0, 1)),
    2: ((1, 2), (0, 0)),
    3: ((2, 5), (0, 0)),
    4: ((0, 0), (0, 0)),
    5: ((0, 0), (0, 0)),
}

BLOCKS = {
    (0, 1): ((0, 1), (1, 0)),
    (0, 2): ((2, 0), (1, 0)),
    (0, 3): ((5, 0), (2, 0)),
    (0, 4): ((0, 3), (0, 10)),
    (0, 5): ((1, 12), (8, 19)),
    (1, 2): ((2, 0), (1, 0)),
    (1, 3): ((5, 0), (2, 0)),
    (1, 4): ((0, 17), (0, 24)),
    (1, 5): ((10, 21), (17, 28)),
    (2, 3): ((9, 0), (0, 0)),
    (2, 4): ((0, 18), (0, 25)),
    (2, 5): ((29, 11), (7, 18)),
    (3, 4): ((28, 10), (6, 17)),
    (3, 5): ((0, 15), (0, 22)),
    (4, 5): ((0, 0), (0, 0)),
}


def packet_from_blocks(blocks):
    return {
        (u, v, a, b): blocks[u, v][a][b]
        for u, v in EDGES
        for a, b in product(COLOURS, repeat=2)
    }


M = packet_from_blocks(BLOCKS)


def audit_generic_kernel_and_selected_rows():
    ranks = [core["matrix_rank"](X[site]) for site in SITES]
    require(ranks == [2, 2, 1, 1, 0, 0],
            ("endpoint rank pattern changed", ranks))
    require(sum(Q(value, 2) for value in RHO) == 1,
            "gauge parameters no longer sum to one")
    require(Z_VALUE == -sum(Q(value, 2) for value in RHO),
            "direct rare cell is not minus the multiplier sum")

    n_blocks = {}
    checked = 0
    for u, v in EDGES:
        n_block = core["matrix_product"](
            core["matrix_product"](X[u], J),
            core["transpose"](X[v]),
        )
        n_blocks[u, v] = n_block
        for a, b in product(COLOURS, repeat=2):
            require(
                2 * n_block[a][b]
                == (RHO[u] + RHO[v]) * BLOCKS[u, v][a][b],
                ("generic-kernel equation failed", u, v, a, b),
            )
            checked += 1

    n_packet = packet_from_blocks(n_blocks)
    slope = core["matching_tensor"](M)
    d_n = core["apply_differential"](M, n_packet)
    require(all(
        Z_VALUE * slope_value + tangent_value == 0
        for slope_value, tangent_value in zip(slope, d_n)
    ), "a selected level-two row failed")
    return checked, slope


def gauge_tangent(mu):
    return {
        (u, v, a, b): (mu[u] + mu[v]) * M[u, v, a, b]
        for u, v, a, b in CELLS
    }


def audit_rank_and_kernel():
    derivative = core["differential_matrix"](M)
    ranks = (
        core["rational_rank"](derivative),
        core["modular_rank"](derivative, 101),
        core["modular_rank"](derivative, 1_000_003),
    )
    require(ranks == (55, 55, 55), ("differential rank changed", ranks))

    gauges = []
    for basis in range(5):
        mu = [0] * 6
        mu[basis] = 1
        mu[5] = -1
        tangent = gauge_tangent(mu)
        require(not any(core["apply_differential"](M, tangent)),
                ("gauge left the kernel", basis))
        gauges.append([tangent[cell] for cell in CELLS])
    require(core["rational_rank"](gauges) == 5,
            "the five gauge directions became dependent")
    return ranks


def orient_block(root, neighbour):
    if root < neighbour:
        return BLOCKS[root, neighbour]
    return core["transpose"](BLOCKS[neighbour, root])


def pure_column(block, output):
    return (
        any(block[row][output] for row in COLOURS)
        and all(
            block[row][column] == 0
            for row in COLOURS
            for column in COLOURS
            if column != output
        )
    )


def endpoint_blocks(root):
    if root <= 3:
        p_block = tuple((0, 0, X[root][row][0]) for row in COLOURS)
        q_block = tuple((0, 0, X[root][row][1]) for row in COLOURS)
        return p_block, q_block
    scale = root - 2
    return (
        ((scale, 0, 0), (scale + 1, 0, 0)),
        ((0, scale + 2, 0), (0, scale + 3, 0)),
    )


EXPECTED = {
    0: ((2, 0), (4, 1)),
    1: ((2, 0), (4, 1)),
    2: ((3, 0), (4, 1)),
    3: ((2, 0), (5, 1)),
}


def audit_r2():
    tables = {}
    for root in SITES:
        p_block, q_block = endpoint_blocks(root)
        require(tuple(p_block[row][2] for row in COLOURS)
                == tuple(X[root][row][0] for row in COLOURS),
                ("p selected star mismatch", root))
        require(tuple(q_block[row][2] for row in COLOURS)
                == tuple(X[root][row][1] for row in COLOURS),
                ("q selected star mismatch", root))

        incident = {
            neighbour: orient_block(root, neighbour)
            for neighbour in SITES if neighbour != root
        }
        incident["p"] = p_block
        incident["q"] = q_block
        pure = {
            output: tuple(
                label for label, block in incident.items()
                if pure_column(block, output)
            )
            for output in COLOURS
        }
        require(pure[0] and pure[1],
                ("R2 lacks a witness colour", root, pure))
        require(any(left != right for left in pure[0] for right in pure[1]),
                ("R2 witnesses are not distinct", root, pure))
        if root in EXPECTED:
            for neighbour, output in EXPECTED[root]:
                require(neighbour in pure[output],
                        ("planned internal witness vanished",
                         root, neighbour, output, pure))
        else:
            require("p" in pure[0] and "q" in pure[1],
                    ("zero-star endpoint witnesses vanished", root, pure))
        tables[root] = pure
    return tables


def main():
    checked, slope = audit_generic_kernel_and_selected_rows()
    ranks = audit_rank_and_kernel()
    tables = audit_r2()
    print(
        "two-invertible R2 guard: "
        f"{checked} generic-kernel scalars, 64 selected rows; "
        f"ranks Q/mod101/mod1000003={ranks}; "
        f"slope support {sum(value != 0 for value in slope)}/64; "
        f"R2 roots {len(tables)}/6"
    )


if __name__ == "__main__":
    main()
