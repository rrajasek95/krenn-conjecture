#!/usr/bin/env python3
"""Exact factored-pure boundary on the all-zero-potential 1I+5Z chart.

Rebind the integral SHARP_M residual packet to X_0=I and X_1=...=X_5=0.
It has rank(dPsi)=55, mixed-row rank 53, literal preimages of both pure
targets, and selected residual R2.  More strongly, each literal preimage is
realized by an actual pair of endpoint stars.  Keeping the other endpoint
colour rows zero also makes both mixed slices vanish.

The pure-zero and pure-one constructions are two separate endpoint-star
assignments.  This checker does not assert a simultaneous four-slice L0
completion; the committed sharp-factor obstruction excludes that for this
packet.  Standard library only; checks stay live under -O and -I -S.
"""

from itertools import combinations, product
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
SHARP = run_path(str(
    HERE / "verify_level_two_three_invertible_l0_obstruction.py"
))
OLD = run_path(str(
    HERE / "verify_level_two_one_invertible_five_zero_l0_incidence_survivor.py"
))

SITES = tuple(range(6))
ENDPOINTS = (6, 7)
COLOURS = (0, 1)
RARE = 2
EDGES = tuple(combinations(SITES, 2))
WORDS = tuple(product(COLOURS, repeat=6))
CELLS = SHARP["CELLS"]
MATCHINGS8 = SHARP["MATCHINGS8"]
M = SHARP["SHARP_M"]
BLOCKS = SHARP["SHARP_BLOCKS"]
X = {
    site: ((1, 0), (0, 1)) if site == 0 else ((0, 0), (0, 0))
    for site in SITES
}
POTENTIALS = (0,) * 6


def append_columns(matrix, *columns):
    return [
        row[:] + [column[index] for column in columns]
        for index, row in enumerate(matrix)
    ]


def ranks_over_fields(matrix):
    return (
        SHARP["rational_rank"](matrix),
        SHARP["modular_rank"](matrix, 101),
        SHARP["modular_rank"](matrix, 32_003),
        SHARP["modular_rank"](matrix, 1_000_003),
    )


def audit_residual_rank_and_kernel():
    require(M != OLD["M"], "the sharp packet equals the old incidence packet")
    changed = sum(M[cell] != OLD["M"][cell] for cell in CELLS)
    require(changed == 47, ("sharp/old cell-difference census changed", changed))

    derivative = SHARP["differential_matrix"](M)
    mixed = [
        row for row, word in zip(derivative, WORDS)
        if word not in ((0,) * 6, (1,) * 6)
    ]
    pure_zero = [int(word == (0,) * 6) for word in WORDS]
    pure_one = [int(word == (1,) * 6) for word in WORDS]
    ranks = {
        "D": ranks_over_fields(derivative),
        "D_mixed": ranks_over_fields(mixed),
        "D|e0": ranks_over_fields(append_columns(derivative, pure_zero)),
        "D|e1": ranks_over_fields(append_columns(derivative, pure_one)),
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
    }, ("sharp one-invertible ranks changed", ranks))

    zero_column = CELLS.index((0, 1, 0, 0))
    one_column = CELLS.index((4, 5, 1, 1))
    require([row[zero_column] for row in derivative] == pure_zero,
            "the literal pure-zero column changed")
    require([row[one_column] for row in derivative] == pure_one,
            "the literal pure-one column changed")

    gauge_rows = []
    for basis in range(5):
        mu = [0] * 6
        mu[basis] = 1
        mu[5] = -1
        tangent = {
            (u, v, a, b): (mu[u] + mu[v]) * M[u, v, a, b]
            for u, v, a, b in CELLS
        }
        require(not any(SHARP["apply_differential"](M, tangent)),
                ("a vertex gauge left the kernel", basis))
        gauge_rows.append([tangent[cell] for cell in CELLS])
    require(SHARP["rational_rank"](gauge_rows) == 5,
            "the five vertex gauges are dependent")
    require(len(CELLS) - ranks["D"][0] == 5,
            "the differential kernel is larger than the gauges")

    slope = SHARP["matching_tensor"](M)
    require(
        SHARP["apply_differential"](M, M)
        == [3 * value for value in slope],
        "Euler's differential identity failed",
    )
    return derivative, ranks, changed


def audit_one_invertible_selected_block():
    endpoint_ranks = tuple(SHARP["rational_rank"](X[site]) for site in SITES)
    require(endpoint_ranks == (2, 0, 0, 0, 0, 0),
            ("one-invertible endpoint ranks changed", endpoint_ranks))

    checked = 0
    for u, v in EDGES:
        for a, b in product(COLOURS, repeat=2):
            numerator = sum(
                X[u][a][i] * X[v][b][1 - i]
                for i in COLOURS
            )
            require(
                numerator == (POTENTIALS[u] + POTENTIALS[v]) * M[u, v, a, b],
                ("generic-kernel identity failed", u, v, a, b),
            )
            checked += 1
    require(checked == 60, "generic-kernel scalar census changed")

    selected_tangent = {
        (u, v, a, b): sum(
            X[u][a][i] * X[v][b][1 - i]
            for i in COLOURS
        )
        for u, v in EDGES
        for a, b in product(COLOURS, repeat=2)
    }
    require(not any(selected_tangent.values()),
            "the selected tangent is nonzero")
    require(SHARP["apply_differential"](M, selected_tangent) == [0] * 64,
            "a selected level-two row survived")
    return endpoint_ranks, checked


def oriented_value(packet, root, neighbour, root_colour, neighbour_colour):
    if root < neighbour:
        return packet.get(
            (root, neighbour, root_colour, neighbour_colour), 0
        )
    return packet.get(
        (neighbour, root, neighbour_colour, root_colour), 0
    )


def pure_column(packet, root, neighbour, output):
    return (
        any(oriented_value(packet, root, neighbour, row, output)
            for row in COLOURS)
        and all(
            oriented_value(packet, root, neighbour, row, column) == 0
            for row in COLOURS
            for column in (0, 1, 2)
            if column != output
        )
    )


def endpoint_stars(target):
    require(target in COLOURS, ("invalid pure target", target))
    u = {(s, r, a): 0 for s in COLOURS for r in SITES for a in COLOURS}
    v = dict(u)
    if target == 0:
        u[0, 0, 0] = 1
        v[0, 1, 0] = 1
    else:
        u[1, 4, 1] = 1
        v[1, 5, 1] = 1
    w = {(s, t): 0 for s, t in product(COLOURS, repeat=2)}
    return u, v, w


def factored_tangent(u_star, v_star, s, t):
    return {
        (r, u, a, b): (
            u_star[s, r, a] * v_star[t, u, b]
            + v_star[t, r, a] * u_star[s, u, b]
        )
        for r, u in EDGES
        for a, b in product(COLOURS, repeat=2)
    }


def full_edge_value(u_star, v_star, direct, edge, colours):
    r, u = edge
    a, b = colours
    if u < ENDPOINTS[0]:
        return M[r, u, a, b]
    if u == ENDPOINTS[0] and r < ENDPOINTS[0]:
        if b in COLOURS:
            return u_star[b, r, a]
        if b == RARE:
            return X[r][a][0]
        return 0
    if u == ENDPOINTS[1] and r < ENDPOINTS[0]:
        if b in COLOURS:
            return v_star[b, r, a]
        if b == RARE:
            return X[r][a][1]
        return 0
    if (r, u) == ENDPOINTS:
        return direct.get((a, b), 0)
    raise RuntimeError(("unclassified eight-site edge", edge, colours))


def eight_site_value(u_star, v_star, direct, word):
    require(len(word) == 8, ("wrong eight-site word length", len(word)))
    total = 0
    for matching in MATCHINGS8:
        term = 1
        for edge in matching:
            term *= full_edge_value(
                u_star, v_star, direct, edge,
                (word[edge[0]], word[edge[1]]),
            )
        total += term
    return total


def audit_factored_three_slice_completion(target):
    u_star, v_star, direct = endpoint_stars(target)
    tangents = {
        (s, t): factored_tangent(u_star, v_star, s, t)
        for s, t in product(COLOURS, repeat=2)
    }
    live_cell = (0, 1, 0, 0) if target == 0 else (4, 5, 1, 1)
    require(
        tuple(cell for cell in CELLS if tangents[target, target][cell])
        == (live_cell,),
        ("the pure factored tangent is not localized", target),
    )
    require(tangents[target, target][live_cell] == 1,
            ("the pure factored tangent coefficient changed", target))
    require(all(
        not any(tangents[s, t].values())
        for s, t in product(COLOURS, repeat=2)
        if (s, t) != (target, target)
    ), ("a nominally zero endpoint slice became live", target))

    pure = [int(word == (target,) * 6) for word in WORDS]
    require(SHARP["apply_differential"](
        M, tangents[target, target]
    ) == pure, ("the factored tangent misses its pure target", target))

    checked = 0
    for s, t in product(COLOURS, repeat=2):
        formula = SHARP["apply_differential"](M, tangents[s, t])
        literal = [
            eight_site_value(u_star, v_star, direct, word + (s, t))
            for word in WORDS
        ]
        expected = pure if (s, t) == (target, target) else [0] * 64
        require(formula == literal == expected,
                ("literal/formula endpoint slice mismatch", target, s, t))
        checked += len(WORDS)
    require(checked == 256, "the endpoint-slice census changed")

    # With only X_0 nonzero, the selected rare/rare endpoint slice vanishes
    # literally for the same assignment: the two endpoint edges cannot meet
    # the same residual vertex in a perfect matching.
    selected = [
        eight_site_value(u_star, v_star, direct, word + (RARE, RARE))
        for word in WORDS
    ]
    require(selected == [0] * 64,
            ("the selected rare/rare slice became live", target))
    return checked, live_cell


def audit_selected_residual_r2():
    # Either binary endpoint-star completion may be used: R2 preservation is
    # controlled by the selected rare columns X and the residual packet.
    u_star, v_star, direct = endpoint_stars(0)
    packet = dict(M)
    for site in SITES:
        for colour in COLOURS:
            for endpoint, star, x_column in (
                (ENDPOINTS[0], u_star, 0),
                (ENDPOINTS[1], v_star, 1),
            ):
                for endpoint_colour in COLOURS:
                    packet[site, endpoint, colour, endpoint_colour] = (
                        star[endpoint_colour, site, colour]
                    )
                packet[site, endpoint, colour, RARE] = X[site][colour][x_column]
    for a, b in product((0, 1, 2), repeat=2):
        packet[ENDPOINTS[0], ENDPOINTS[1], a, b] = direct.get((a, b), 0)

    tables = {}
    for root in SITES:
        preserves = all(
            oriented_value(packet, root, neighbour, row, RARE) == 0
            for neighbour in range(8)
            if neighbour != root
            for row in COLOURS
        )
        pure = {
            output: tuple(
                neighbour
                for neighbour in range(8)
                if neighbour != root
                and pure_column(packet, root, neighbour, output)
            )
            for output in COLOURS
        }
        if root == 0:
            require(not preserves, "the invertible root unexpectedly preserves")
            require(3 in pure[0] and 2 in pure[1],
                    ("root-zero pure witnesses changed", pure))
        else:
            require(preserves, ("a zero endpoint root does not preserve", root))
        tables[root] = (preserves, pure)

    for neighbour in (2, 3):
        complement = tuple(
            site for site in SITES if site not in (0, neighbour)
        )
        nonzero = tuple(
            SHARP["hafnian"](M, complement, word)
            for word in WORDS
            if SHARP["hafnian"](M, complement, word) != 0
        )
        require(nonzero, ("an R2 witness has zero cofactor", neighbour))
    return tables


def audit_sharp_factor_obstruction_scope():
    expected = {
        (0, 1): ((2, 3), (4, 6)),
        (0, 4): ((5, 6), (11, 8)),
        (0, 5): ((6, 7), (13, 9)),
        (4, 5): ((1, 0), (0, 0)),
    }
    require({edge: BLOCKS[edge] for edge in expected} == expected,
            "the sharp-factor obstruction core changed")
    return len(expected)


def main():
    _derivative, ranks, changed = audit_residual_rank_and_kernel()
    endpoint_ranks, generic = audit_one_invertible_selected_block()
    zero_slices, zero_cell = audit_factored_three_slice_completion(0)
    one_slices, one_cell = audit_factored_three_slice_completion(1)
    r2 = audit_selected_residual_r2()
    obstruction_edges = audit_sharp_factor_obstruction_scope()
    print("one-invertible factored-pure boundary: all checks passed")
    print(f"  residual differs from old packet : {changed}/60 cells")
    print(f"  endpoint ranks                   : {endpoint_ranks}")
    print(f"  generic-kernel scalars           : {generic}/60")
    print(f"  selected residual R2 roots       : {len(r2)}/6")
    print(f"  differential ranks               : {ranks}")
    print(f"  pure-zero factored tangent       : {zero_cell}; {zero_slices}/256 slices")
    print(f"  pure-one factored tangent        : {one_cell}; {one_slices}/256 slices")
    print(f"  simultaneous-obstruction core    : {obstruction_edges} edges")
    print("  scope                             : two separate three-slice completions")


if __name__ == "__main__":
    main()
