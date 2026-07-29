#!/usr/bin/env python3
"""Exact audits for ``notes/simultaneous-star-syzygy-boundary.md``.

There are two independent checks.

1.  A seven-site, three-colour common-cofactor module has three pure target
    tensors in its image, an injective cofactor map, and unique two-centre
    preimages.  Hence its least-norm star has six scalar cells and cannot be
    replaced by three one-centre rows.  This module is deliberately *not*
    asserted to be a power of a quadratic matching source.
2.  A genuine six-vertex binary matching source has ``H_6 = GHZ_2``.  At
    every vertex its displayed star is the exact least-Frobenius-norm
    solution for the common internal quadratic, although four of the stars
    use two colour-zero neighbours.  All arithmetic is rational.
"""

from __future__ import annotations

import itertools
from collections import defaultdict

import sympy as sp


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        edge = tuple(sorted((first, second)))
        for matching in perfect_matchings(rest):
            yield (edge,) + matching


def audit_common_cofactor_module() -> None:
    sites = tuple(range(7))
    centres = {0: (0, 1), 1: (2, 3), 2: (4, 5)}
    transfer_colours = {
        0: {2: 1, 3: 2, 4: 0, 5: 1, 6: 2},
        1: {0: 2, 1: 0, 4: 1, 5: 2, 6: 0},
        2: {0: 0, 1: 1, 2: 2, 3: 0, 6: 1},
    }

    # C[j] is stored in the standard basis as partial colourings with None
    # in the missing slot j.
    cofactors: dict[int, dict[tuple[int | None, ...], int]] = {
        j: {} for j in sites
    }

    def add(j: int, colouring: list[int | None], coefficient: int) -> None:
        key = tuple(colouring)
        cofactors[j][key] = cofactors[j].get(key, 0) + coefficient
        if cofactors[j][key] == 0:
            del cofactors[j][key]

    for colour, (a, b) in centres.items():
        other_colour = (colour + 1) % 3
        remainder = tuple(j for j in sites if j not in (a, b))

        baseline: list[int | None] = [None] * 7
        baseline[b] = colour
        for j in remainder:
            baseline[j] = colour
        add(a, baseline, 1)

        transfer: list[int | None] = [None] * 7
        transfer[b] = other_colour
        for j in remainder:
            transfer[j] = transfer_colours[colour][j]
        add(a, transfer, -1)

        mate: list[int | None] = [None] * 7
        mate[a] = colour
        for j in remainder:
            mate[j] = transfer_colours[colour][j]
        add(b, mate, 1)

    # A harmless seventh active cofactor makes the full map injective.
    # Its nonconstant pattern is absent from every preceding support.
    add(6, [0, 0, 0, 0, 0, 1, None], 1)

    columns: list[dict[tuple[int, ...], int]] = []
    labels: list[tuple[int, int]] = []
    for j in range(7):
        for endpoint_colour in range(3):
            column: dict[tuple[int, ...], int] = {}
            for partial, coefficient in cofactors[j].items():
                full = list(partial)
                full[j] = endpoint_colour
                key = tuple(int(value) for value in full)
                column[key] = column.get(key, 0) + coefficient
            columns.append(column)
            labels.append((j, endpoint_colour))

    support = sorted(set().union(*(set(column) for column in columns)))
    matrix = sp.Matrix(
        [[column.get(colouring, 0) for column in columns] for colouring in support]
    )
    assert matrix.rank() == 21 == len(columns)

    # The unique preimage of g_r has entries (a_r,r) and
    # (b_r,r+1 mod 3), both equal to one.
    for colour, (a, b) in centres.items():
        target = sp.Matrix(
            [int(colouring == (colour,) * 7) for colouring in support]
        )
        expected = sp.zeros(21, 1)
        expected[labels.index((a, colour))] = 1
        expected[labels.index((b, (colour + 1) % 3))] = 1
        assert matrix * expected == target
        solution = sp.linsolve((matrix, target))
        assert solution == sp.FiniteSet(tuple(expected))

    # A one-centre preimage of a nonzero constant tensor would require its
    # cofactor to be a pure constant tensor.  No active C_j has that form.
    for j in range(7):
        assert cofactors[j]
        for colour in range(3):
            desired = tuple(None if k == j else colour for k in sites)
            assert not (
                len(cofactors[j]) == 1
                and desired in cofactors[j]
                and cofactors[j][desired] != 0
            )


def binary_source():
    c = sp.Rational(3, 5)
    s = sp.Rational(4, 5)
    cells: dict[tuple[tuple[int, int], int, int], sp.Rational] = {}

    def put(u: int, v: int, colour: int, weight) -> None:
        edge = tuple(sorted((u, v)))
        cells[edge, colour, colour] = sp.Rational(weight)

    for u, v, weight in (
        (0, 1, c),
        (2, 3, c),
        (0, 2, s),
        (1, 3, s),
        (4, 5, 1),
    ):
        put(u, v, 0, weight)
    for u, v in ((1, 2), (3, 4), (0, 5)):
        put(u, v, 1, 1)
    return cells


def matching_tensor(
    vertices: tuple[int, ...],
    cells: dict[tuple[tuple[int, int], int, int], sp.Rational],
):
    answer: defaultdict[tuple[int, ...], sp.Expr] = defaultdict(lambda: sp.S.Zero)
    for matching in perfect_matchings(vertices):
        choices = []
        for edge in matching:
            edge_choices = [
                (left, right, weight)
                for (candidate, left, right), weight in cells.items()
                if candidate == edge
            ]
            if not edge_choices:
                break
            choices.append(edge_choices)
        else:
            for selected in itertools.product(*choices):
                colouring: dict[int, int] = {}
                value = sp.S.One
                for edge, (left, right, weight) in zip(matching, selected):
                    colouring[edge[0]] = left
                    colouring[edge[1]] = right
                    value *= weight
                key = tuple(colouring[v] for v in vertices)
                answer[key] += value
    return {key: sp.simplify(value) for key, value in answer.items() if value != 0}


def audit_binary_shared_power_least_stars() -> None:
    cells = binary_source()
    vertices = tuple(range(6))
    output = matching_tensor(vertices, cells)
    assert output == {(0,) * 6: 1, (1,) * 6: 1}

    # The source has the Hamilton norm 6 and eight scalar cells.
    assert sp.simplify(sum(abs(value) ** 2 for value in cells.values())) == 6
    assert len(cells) == 8

    duplicate_zero_stars = 0
    for centre in vertices:
        remaining = tuple(v for v in vertices if v != centre)
        output_basis = tuple(itertools.product(range(2), repeat=5))
        labels: list[tuple[int, int]] = []
        columns: list[sp.Matrix] = []

        for neighbour in remaining:
            cofactor_sites = tuple(
                v for v in remaining if v != neighbour
            )
            cofactor = matching_tensor(cofactor_sites, cells)
            for neighbour_colour in range(2):
                labels.append((neighbour, neighbour_colour))
                entries = []
                for colouring in output_basis:
                    if colouring[remaining.index(neighbour)] != neighbour_colour:
                        entries.append(0)
                        continue
                    restricted = tuple(
                        colouring[remaining.index(v)] for v in cofactor_sites
                    )
                    entries.append(cofactor.get(restricted, 0))
                columns.append(sp.Matrix(entries))

        cofactor_map = sp.Matrix.hstack(*columns)
        kernel = cofactor_map.nullspace()

        for centre_colour in range(2):
            current = sp.zeros(len(labels), 1)
            for index, (neighbour, neighbour_colour) in enumerate(labels):
                if neighbour_colour != centre_colour:
                    continue
                edge = tuple(sorted((centre, neighbour)))
                current[index] = cells.get(
                    (edge, centre_colour, centre_colour), sp.S.Zero
                )

            target = sp.Matrix(
                [
                    int(colouring == (centre_colour,) * 5)
                    for colouring in output_basis
                ]
            )
            assert cofactor_map * current == target

            # For a consistent affine system, x is the unique least-norm
            # point exactly when it is orthogonal to ker(F).
            assert all((direction.T * current)[0] == 0 for direction in kernel)

            support_size = sum(value != 0 for value in current)
            if centre_colour == 0 and support_size == 2:
                duplicate_zero_stars += 1

    assert duplicate_zero_stars == 4

    # At centre 0 the least star has two colour-zero neighbours and one
    # colour-one neighbour, hence three cells rather than the binary cubic
    # normal form's two.  Its squared star norm is exactly 2.
    centre_zero_cells = [
        (edge, left, right, value)
        for (edge, left, right), value in cells.items()
        if 0 in edge
    ]
    assert len(centre_zero_cells) == 3
    assert sp.simplify(sum(value**2 for *_, value in centre_zero_cells)) == 2


def main() -> None:
    audit_common_cofactor_module()
    audit_binary_shared_power_least_stars()
    print("verified injective seven-site three-colour common-cofactor module")
    print("verified unique six-cell simultaneous star and no one-centre rows")
    print("verified exact rational GHZ_2 source and least-norm shared-power stars")


if __name__ == "__main__":
    main()
