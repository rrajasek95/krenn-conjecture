#!/usr/bin/env python3
"""Map the transverse-column 2I+2R+2Z potential boundary.

The two rank-one endpoint matrices miss opposite selected columns.  After
covariant normalization their source factors are e_0 and e_1, so every core
numerator is nonzero and has one of the exact forms

    J, e_1 e_0^T, or e_0 e_0^T.

Signed potential partitions give 39 zero-sum support envelopes.  The 38
non-dense envelopes have at most 52 active differential columns.  The sole
dense envelope has potential (1,1,1,1,-1,-1); an exact normalized packet on
that ray has differential rank 55 and literal R2 witnesses at all roots.

Standard library only; checks remain live under python -O and python -I -S.
"""

from collections import Counter
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
boundary = run_path(str(
    HERE / "verify_level_two_two_invertible_same_column_potential_boundary.py"
))
rank_core = run_path(str(
    HERE / "verify_level_two_one_sided_overlap_collapse.py"
))
dense_core = run_path(str(
    HERE / "verify_level_two_two_invertible_same_column_dense_ray_closure.py"
))

SITES = boundary["SITES"]
COLOURS = boundary["COLOURS"]
INVERTIBLE = boundary["INVERTIBLE"]
RANK_ONE = boundary["RANK_ONE"]
ZERO = boundary["ZERO"]
EDGES = boundary["EDGES"]
CELLS = boundary["CELLS"]
COMPLEMENT_MATCHINGS = boundary["COMPLEMENT_MATCHINGS"]
J = dense_core["J"]
IDENTITY = dense_core["IDENTITY"]
E00 = dense_core["E00"]
E10 = dense_core["E10"]
ZERO_MATRIX = dense_core["ZERO_MATRIX"]

X = {
    0: IDENTITY,
    1: IDENTITY,
    2: E00,
    3: ((0, 1), (0, 0)),
    4: ZERO_MATRIX,
    5: ZERO_MATRIX,
}

CORE_BLOCKS = {
    (0, 1): J,
    (0, 2): E10,
    (1, 2): E10,
    (0, 3): E00,
    (1, 3): E00,
    (2, 3): E00,
}


def audit_covariant_core_normal_form():
    checks = 0
    for pair in EDGES:
        numerator = dense_core["matrix_product"](
            dense_core["matrix_product"](X[pair[0]], J),
            dense_core["transpose"](X[pair[1]]),
        )
        expected = CORE_BLOCKS.get(pair, ZERO_MATRIX)
        require(numerator == expected,
                ("transverse core numerator changed", pair, numerator))
        for a, b in product(COLOURS, repeat=2):
            require((numerator[a][b] != 0) == (expected[a][b] != 0),
                    ("core support scalar changed", pair, a, b))
            checks += 1
    require(checks == 60, "normal-form scalar census changed")
    return checks


def support_value(optional, pair, colours):
    a, b = colours
    if pair == (0, 1):
        return (a, b) in ((0, 1), (1, 0))
    if pair in ((0, 2), (1, 2)):
        return (a, b) == (1, 0)
    if pair in ((0, 3), (1, 3), (2, 3)):
        return (a, b) == (0, 0)
    return pair in optional


def cofactor_may_live(optional, pair, word):
    return any(
        all(
            support_value(
                optional,
                matching_edge,
                (word[matching_edge[0]], word[matching_edge[1]]),
            )
            for matching_edge in matching
        )
        for matching in COMPLEMENT_MATCHINGS[pair]
    )


def active_cells(optional):
    answer = set()
    for cell in CELLS:
        u, v, a, b = cell
        if any(
            word[u] == a
            and word[v] == b
            and cofactor_may_live(optional, (u, v), word)
            for word in product(COLOURS, repeat=6)
        ):
            answer.add(cell)
    return frozenset(answer)


EXPECTED_ACTIVE_HISTOGRAM = {
    4: 1,
    16: 2,
    20: 6,
    28: 3,
    32: 3,
    40: 9,
    44: 8,
    48: 2,
    52: 4,
    60: 1,
}


def audit_potential_support_map():
    admissible_count, envelopes = boundary["support_envelopes"]()
    require(admissible_count == 1574,
            ("admissible potential census changed", admissible_count))
    require(len(envelopes) == 39,
            ("transverse support census changed", len(envelopes)))

    counts = {optional: len(active_cells(optional)) for optional in envelopes}
    histogram = dict(sorted(Counter(counts.values()).items()))
    require(histogram == EXPECTED_ACTIVE_HISTOGRAM,
            ("transverse active-cell histogram changed", histogram))

    # The canonical quotient includes exchanging the two rank-one sites,
    # accompanied by the global selected-column exchange.  Audit directly
    # that every labelled support in a quotient class has the same exact
    # local-colour count.
    raw_counts = {}
    for potential in boundary["signed_partitions"](len(SITES)):
        if not boundary["admissible"](potential):
            continue
        optional = boundary["optional_edges"](potential)
        if optional not in raw_counts:
            raw_counts[optional] = len(active_cells(optional))
        canonical = boundary["canonical_optional_edges"](optional)
        require(raw_counts[optional] == counts[canonical],
                ("transverse quotient changed the cell count",
                 potential, raw_counts[optional], counts[canonical]))
    require(len(raw_counts) == 131,
            ("labelled transverse support census changed", len(raw_counts)))

    dense_optional = boundary["canonical_optional_edges"](
        boundary["DENSE_OPTIONAL"]
    )
    require(counts[dense_optional] == 60,
            ("dense transverse active count changed", counts[dense_optional]))
    non_dense = {
        optional: count for optional, count in counts.items()
        if optional != dense_optional
    }
    require(max(non_dense.values()) == 52,
            ("non-dense transverse bound changed", max(non_dense.values())))

    dense_representatives = tuple(
        potential
        for potential in boundary["signed_partitions"](len(SITES))
        if boundary["admissible"](potential)
        and boundary["optional_edges"](potential)
        == boundary["DENSE_OPTIONAL"]
    )
    require(dense_representatives == (boundary["DENSE_POTENTIAL"],),
            ("dense transverse potential lost uniqueness",
             dense_representatives))
    return envelopes, histogram, len(raw_counts)


DENSE_POTENTIAL = (Q(1, 2),) * 4 + (Q(-1, 2),) * 2


def dense_free_value(edge_index, pair, a, b):
    if pair in ((0, 4), (1, 4)) and b == 0:
        return 0
    return 1 + (
        17 * edge_index + 7 * a + 11 * b
        + 3 * edge_index * edge_index
    ) % 29


def build_dense_guard_blocks():
    blocks = {}
    for edge_index, pair in enumerate(EDGES):
        if pair in CORE_BLOCKS:
            blocks[pair] = CORE_BLOCKS[pair]
        elif pair == (4, 5):
            blocks[pair] = ZERO_MATRIX
        else:
            blocks[pair] = tuple(
                tuple(
                    dense_free_value(edge_index, pair, a, b)
                    for b in COLOURS
                )
                for a in COLOURS
            )
    return blocks


BLOCKS = build_dense_guard_blocks()
PACKET = {
    (u, v, a, b): BLOCKS[u, v][a][b]
    for u, v in EDGES
    for a, b in product(COLOURS, repeat=2)
}


def audit_dense_generic_kernel():
    checks = 0
    for pair in EDGES:
        numerator = dense_core["matrix_product"](
            dense_core["matrix_product"](X[pair[0]], J),
            dense_core["transpose"](X[pair[1]]),
        )
        multiplier = DENSE_POTENTIAL[pair[0]] + DENSE_POTENTIAL[pair[1]]
        for a, b in product(COLOURS, repeat=2):
            require(
                numerator[a][b] == multiplier * BLOCKS[pair][a][b],
                ("dense generic-kernel equation failed", pair, a, b),
            )
            checks += 1
    require(checks == 60, "dense generic-kernel scalar census changed")
    return checks


def audit_dense_selected_rows():
    derivative = rank_core["differential"](PACKET)
    numerator = []
    for u, v, a, b in CELLS:
        block = dense_core["matrix_product"](
            dense_core["matrix_product"](X[u], J),
            dense_core["transpose"](X[v]),
        )
        numerator.append(block[a][b])
    tangent = rank_core["matrix_vector_product"](derivative, numerator)
    slope = [
        rank_core["hafnian"](PACKET, SITES, word)
        for word in rank_core["WORDS"]
    ]
    direct_value = -sum(DENSE_POTENTIAL)
    require(direct_value == -1,
            ("dense direct selected value changed", direct_value))
    require(all(
        direct_value * slope_value + tangent_value == 0
        for slope_value, tangent_value in zip(slope, tangent)
    ), "a dense selected level-two row failed")
    return len(slope), sum(value != 0 for value in slope)


def gauge_tangent(mu):
    return [
        (mu[u] + mu[v]) * PACKET[u, v, a, b]
        for u, v, a, b in CELLS
    ]


def audit_dense_rank():
    derivative = rank_core["differential"](PACKET)
    ranks = (
        dense_core["rational_rank"](derivative),
        rank_core["rank_mod"](derivative, 101),
        rank_core["rank_mod"](derivative, 1_000_003),
    )
    require(ranks == (55, 55, 55),
            ("dense transverse rank changed", ranks))

    gauges = []
    for basis in range(5):
        mu = [0] * 6
        mu[basis] = 1
        mu[5] = -1
        tangent = gauge_tangent(mu)
        require(not any(rank_core["matrix_vector_product"](
            derivative, tangent
        )), ("dense vertex gauge left the kernel", basis))
        gauges.append(tangent)
    require(dense_core["rational_rank"](gauges) == 5,
            "dense transverse gauges became dependent")
    return ranks


def orient_block(root, neighbour):
    if root < neighbour:
        return BLOCKS[root, neighbour]
    return dense_core["transpose"](BLOCKS[neighbour, root])


def pure_column(block, output):
    width = len(block[0])
    return (
        any(block[row][output] for row in COLOURS)
        and all(
            block[row][column] == 0
            for row in COLOURS
            for column in range(width)
            if column != output
        )
    )


def endpoint_blocks(root):
    if root <= 2:
        return (
            tuple((0, 0, X[root][row][0]) for row in COLOURS),
            tuple((0, 0, X[root][row][1]) for row in COLOURS),
        )
    if root == 3:
        # P_3=0 supplies a physical selected-output witness, while Q_3=e_0
        # retains its nonzero outside-column entries.
        return (
            ((0, 1, 0), (0, 2, 0)),
            ((0, 0, 1), (0, 0, 0)),
        )
    scale = root - 2
    return (
        ((scale, 0, 0), (scale + 1, 0, 0)),
        ((0, scale + 2, 0), (0, scale + 3, 0)),
    )


EXPECTED_WITNESSES = {
    0: ((2, 0), (4, 1)),
    1: ((2, 0), (4, 1)),
    2: ((3, 0), (0, 1)),
    3: ((0, 0), ("p", 1)),
    4: (("p", 0), ("q", 1)),
    5: (("p", 0), ("q", 1)),
}


def audit_dense_r2():
    tables = {}
    for root in SITES:
        p_block, q_block = endpoint_blocks(root)
        require(
            tuple(p_block[row][2] for row in COLOURS)
            == tuple(X[root][row][0] for row in COLOURS),
            ("dense P selected star mismatch", root),
        )
        require(
            tuple(q_block[row][2] for row in COLOURS)
            == tuple(X[root][row][1] for row in COLOURS),
            ("dense Q selected star mismatch", root),
        )

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
                if pure_column(block, output)
            )
            for output in COLOURS
        }
        require(pure[0] and pure[1],
                ("dense R2 lacks a witness colour", root, pure))
        require(any(left != right for left in pure[0] for right in pure[1]),
                ("dense R2 witnesses are not distinct", root, pure))
        for label, output in EXPECTED_WITNESSES[root]:
            require(label in pure[output],
                    ("planned dense R2 witness vanished",
                     root, label, output, pure))
        tables[root] = pure
    return tables


def determinant(block):
    return block[0][0] * block[1][1] - block[0][1] * block[1][0]


def audit_dense_spokes():
    # The displayed R2 guard lies in the invertible-spoke interior at both
    # zero sites, although singular-spoke degenerations remain unclassified.
    witnesses = {}
    for zero in ZERO:
        choices = {
            core: determinant(BLOCKS[core, zero])
            for core in (2, 3)
        }
        require(any(value for value in choices.values()),
                ("dense zero site lost every invertible core spoke",
                 zero, choices))
        witnesses[zero] = choices
    return witnesses


def main():
    normal = audit_covariant_core_normal_form()
    envelopes, histogram, labelled = audit_potential_support_map()
    generic = audit_dense_generic_kernel()
    selected = audit_dense_selected_rows()
    ranks = audit_dense_rank()
    r2 = audit_dense_r2()
    spokes = audit_dense_spokes()
    print("2I+2R+2Z transverse-column boundary: all checks passed")
    print(f"  normalized numerator scalars : {normal}/60")
    print(f"  potential support envelopes  : {len(envelopes)}")
    print(f"  labelled support graphs      : {labelled}")
    print(f"  active-cell histogram        : {histogram}")
    print(f"  non-dense maximum rank bound : 52")
    print(f"  dense generic-kernel scalars : {generic}/60")
    print(f"  dense selected rows/support  : {selected}")
    print(f"  dense exact ranks            : {ranks}")
    print(f"  dense R2 roots               : {len(r2)}/6")
    print(f"  dense invertible spokes      : {spokes}")


if __name__ == "__main__":
    main()
