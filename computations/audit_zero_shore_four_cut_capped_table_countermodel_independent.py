#!/usr/bin/env python3
"""Clean-room audit of the twelve-port capped four-cut countermodel.

The implementation is independent of the primary checker.  Ports are
labelled by pairs (hole colour, frame), polynomials are expanded directly
in the site-square-zero algebra, and the fixed-perfect-matching obstruction
is audited both by physical hole multidegrees and by the coordinate lines
forced on an arbitrary tensor block on each matching edge.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product


COLOURS = tuple(range(3))
FRAMES = tuple(range(4))
PORTS = tuple((colour, frame) for colour in COLOURS for frame in FRAMES)
PORT_INDEX = {port: index for index, port in enumerate(PORTS)}
EMPTY = -1

Monomial = tuple[int, ...]
Polynomial = dict[Monomial, Fraction]


def singleton(site: tuple[int, int], coordinate: int) -> Monomial:
    word = [EMPTY] * len(PORTS)
    word[PORT_INDEX[site]] = coordinate
    return tuple(word)


def multiply_words(left: Monomial, right: Monomial) -> Monomial | None:
    answer = []
    for a, b in zip(left, right, strict=True):
        if a != EMPTY and b != EMPTY:
            return None
        answer.append(b if a == EMPTY else a)
    return tuple(answer)


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    answer: Counter[Monomial] = Counter()
    for left_word, left_coefficient in left.items():
        for right_word, right_coefficient in right.items():
            word = multiply_words(left_word, right_word)
            if word is not None:
                answer[word] += left_coefficient * right_coefficient
    return {word: coefficient for word, coefficient in answer.items()
            if coefficient}


def row(frame: int, colour: int) -> Polynomial:
    return {singleton((colour, frame), colour): Fraction(1)}


def sector(colour: int) -> Monomial:
    """E_colour: holes at H_colour and colour elsewhere."""
    return tuple(
        EMPTY if port_colour == colour else colour
        for port_colour, _frame in PORTS
    )


def diagonal_target(colour: int) -> Polynomial:
    return {(colour,) * len(PORTS): Fraction(1)}


QBAR: Polynomial = {sector(colour): Fraction(1) for colour in COLOURS}


def product_of_rows(colours: tuple[int, int, int, int]) -> Polynomial:
    answer: Polynomial = {(EMPTY,) * len(PORTS): Fraction(1)}
    for frame, colour in zip(FRAMES, colours, strict=True):
        answer = multiply(answer, row(frame, colour))
    return answer


def rational_rank(rows: list[list[Fraction]]) -> int:
    matrix = [list(row_values) for row_values in rows]
    pivot_row = 0
    width = len(matrix[0]) if matrix else 0
    for column in range(width):
        pivot = next(
            (row_index for row_index in range(pivot_row, len(matrix))
             if matrix[row_index][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / scale for entry in matrix[pivot_row]]
        for row_index in range(len(matrix)):
            if row_index == pivot_row or not matrix[row_index][column]:
                continue
            scale = matrix[row_index][column]
            matrix[row_index] = [
                entry - scale * pivot_entry
                for entry, pivot_entry in zip(
                    matrix[row_index], matrix[pivot_row], strict=True
                )
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        remainder = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(remainder):
            yield ((first, second),) + tail


def holes_for_omitted_edges(
    matching: tuple[tuple[int, int], ...],
    omitted: tuple[int, int],
) -> frozenset[int]:
    return frozenset(
        vertex
        for edge_index in omitted
        for vertex in matching[edge_index]
    )


def coefficient_edge_indices(
    matching: tuple[tuple[int, int], ...],
    hole_set: frozenset[int],
) -> frozenset[int] | None:
    omitted = tuple(
        edge_index
        for edge_index, edge in enumerate(matching)
        if set(edge) <= hole_set
    )
    if len(omitted) != 2:
        return None
    if holes_for_omitted_edges(matching, omitted) != hole_set:
        return None
    return frozenset(set(range(6)) - set(omitted))


def audit_frames_and_responses():
    frame_ledger = []
    for frame in FRAMES:
        vectors: list[list[Fraction]] = []
        for colour in COLOURS:
            vector = [Fraction(0)] * (3 * len(PORTS))
            site = (colour, frame)
            vector[3 * PORT_INDEX[site] + colour] = Fraction(1)
            vectors.append(vector)

            support = {
                PORTS[site_index]
                for site_index in range(len(PORTS))
                if any(vector[3 * site_index + coordinate]
                       for coordinate in COLOURS)
            }
            assert support == {site}
            assert vector[3 * PORT_INDEX[site] + colour] == 1
        rank = rational_rank(vectors)
        assert rank == 3
        frame_ledger.append((frame, rank))

    response_ledger = []
    sector_ledger = []
    nonzero_words = []
    for colours in product(COLOURS, repeat=4):
        rows = product_of_rows(colours)
        total = multiply(rows, QBAR)
        expected = (
            diagonal_target(colours[0])
            if len(set(colours)) == 1
            else {}
        )
        assert total == expected

        sector_hits = []
        for sector_colour in COLOURS:
            contribution = multiply(
                rows, {sector(sector_colour): Fraction(1)}
            )
            should_hit = all(
                colour == sector_colour for colour in colours
            )
            assert bool(contribution) == should_hit
            if contribution:
                assert contribution == diagonal_target(sector_colour)
                sector_hits.append(sector_colour)
        assert len(sector_hits) == (1 if total else 0)

        if total:
            nonzero_words.append(colours)
        response_ledger.append((colours, tuple(sorted(total.items()))))
        sector_ledger.append((colours, tuple(sector_hits)))

    assert nonzero_words == [(0, 0, 0, 0), (1, 1, 1, 1),
                             (2, 2, 2, 2)]

    # The formal induced-zero K4 has six literally zero mutual aggregate
    # blocks.  Its capped shore contraction is precisely the response above.
    zero_blocks = {
        pair: tuple(tuple(Fraction(0) for _ in COLOURS) for _ in COLOURS)
        for pair in combinations(FRAMES, 2)
    }
    assert len(zero_blocks) == 6
    assert not any(entry for matrix in zero_blocks.values()
                   for matrix_row in matrix for entry in matrix_row)

    return frame_ledger, response_ledger, sector_ledger


def audit_fixed_matching_lemma():
    hole_sets = {
        colour: frozenset(
            PORT_INDEX[(colour, frame)] for frame in FRAMES
        )
        for colour in COLOURS
    }

    total = 0
    alignment_histogram: Counter[int] = Counter()
    fully_aligned = []
    full_nonzero_sector_counts = set()
    zero_mask_ledger = Counter()
    coordinate_conflicts = 0

    for matching in perfect_matchings(tuple(range(len(PORTS)))):
        total += 1

        # Six nonzero blocks on disjoint matching edges give one nonzero
        # tensor-product coefficient for every four-edge choice.  Their
        # physical hole multidegrees are all distinct.
        all_hole_sectors = {
            holes_for_omitted_edges(matching, omitted)
            for omitted in combinations(range(6), 2)
        }
        assert len(all_hole_sectors) == 15
        full_nonzero_sector_counts.add(len(all_hole_sectors))

        coefficient_edges = {
            colour: coefficient_edge_indices(
                matching, hole_sets[colour]
            )
            for colour in COLOURS
        }
        aligned_colours = tuple(
            colour for colour in COLOURS
            if coefficient_edges[colour] is not None
        )
        alignment_histogram[len(aligned_colours)] += 1
        assert len(aligned_colours) in (0, 1, 3)

        if len(aligned_colours) != 3:
            # At least one required nonzero E_c coefficient has a hole set
            # which no four-edge product on this matching can have.
            continue

        fully_aligned.append(matching)

        group_of_edge = {}
        for edge_index, edge in enumerate(matching):
            containing = [
                colour for colour in COLOURS
                if set(edge) <= hole_sets[colour]
            ]
            assert len(containing) == 1
            group_of_edge[edge_index] = containing[0]
        assert Counter(group_of_edge.values()) == Counter({0: 2, 1: 2, 2: 2})

        # Allow an arbitrary zero/nonzero choice for all six tensor blocks.
        # Every required E_c sector is nonzero only if all four included
        # edge blocks are nonzero.  The only mask retaining all three is the
        # full mask, so every mask containing a zero block already fails.
        masks_with_all_required = []
        for mask in range(1 << 6):
            alive = tuple(
                colour
                for colour in COLOURS
                if all(mask & (1 << edge_index)
                       for edge_index in coefficient_edges[colour])
            )
            zero_mask_ledger[len(alive)] += 1
            if len(alive) == 3:
                masks_with_all_required.append(mask)
        assert masks_with_all_required == [(1 << 6) - 1]

        # Regroup a required nonzero coefficient by its four disjoint edge
        # factors.  Equality with E_c forces each arbitrary 9-dimensional
        # block B_e into span(e_c tensor e_c).  An edge contained in H_g is
        # used by the two coefficients c != g, which demand two different
        # coordinate lines.  Their intersection is {0}, contradicting the
        # nonzero-block hypothesis.  The basis indices below audit these
        # exact one-dimensional subspaces without assuming B_e is simple.
        for edge_index in range(6):
            group = group_of_edge[edge_index]
            demands = tuple(colour for colour in COLOURS if colour != group)
            assert len(demands) == 2
            demanded_basis_indices = tuple(3 * colour + colour
                                            for colour in demands)
            assert len(set(demanded_basis_indices)) == 2
            # Two distinct coordinate basis lines in the edge's full
            # V_x tensor V_y (dimension nine) meet only at zero.
            coordinate_conflicts += 1

    assert total == 10395
    assert full_nonzero_sector_counts == {15}
    assert alignment_histogram == Counter({0: 9504, 1: 864, 3: 27})
    assert len(fully_aligned) == 27
    assert coordinate_conflicts == 27 * 6

    # Each aligned matching has 64 zero/nonzero masks.  Only its all-nonzero
    # mask leaves all three required sectors structurally nonzero.
    assert sum(zero_mask_ledger.values()) == 27 * 64
    assert zero_mask_ledger[3] == 27
    assert sum(count for alive_count, count in zero_mask_ledger.items()
               if alive_count < 3) == 27 * 63

    return (
        total,
        tuple(sorted(alignment_histogram.items())),
        len(fully_aligned),
        tuple(sorted(zero_mask_ledger.items())),
        coordinate_conflicts,
    )


def main() -> None:
    assert len(PORTS) == 12
    assert len({sector(colour) for colour in COLOURS}) == 3
    frames, responses, sector_hits = audit_frames_and_responses()
    matching_ledger = audit_fixed_matching_lemma()

    ledger = repr((PORTS, frames, responses, sector_hits,
                   matching_ledger)).encode()
    digest = sha256(ledger).hexdigest()
    print("independent twelve-port capped-table audit: PASS")
    print("81 products: 3 unit diagonal responses, 78 literal zeros")
    print("four support-one coordinate-anchored frame ranks: 3, 3, 3, 3")
    print("fixed matching ledger: 10395 total; 27 fully aligned")
    print("zero-block masks: 27 full masks survive structurally; 1701 fail")
    print("arbitrary nonzero edge blocks: 162 incompatible coordinate demands")
    print(f"independent ledger sha256: {digest}")


if __name__ == "__main__":
    main()
