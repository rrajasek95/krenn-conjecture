#!/usr/bin/env python3
"""Exact obstruction audit for the n=8 block-diagonal ansatz.

The four canonical pairs are 01,23,45,67 and their binary-block matrices
vanish.  On the four edges between two canonical pairs, the zero four-site
hafnian has five maximal strata:

* ``D``: all four matrices are nonzero (the crossing-Segre component);
* one of four two-edge stars.

An exact layer support is empty, a singleton, one of the four two-edge
stars, or ``D``.  The script enumerates all ``10^6`` exact support patterns,
not merely their maximal star extensions.  It rejects a proper pair-union
with exactly one supported perfect matching and quotients the remaining
matching products by transported four- and six-site identities.  Exact
rational row reduction proves that most full tensors are zero or factor
across a nontrivial vertex cut.

For the remaining patterns it applies three proved local consequences:

* a two-term six-site identity promotes all residual edge matrices to rank
  one and identifies their endpoint lines;
* a four-term identity containing a dense layer promotes every supported
  edge to rank one and forces two explicit coherent block corners;
* an eight-term all-dense identity forces at least two of its three block
  corners to be coherent.

An exhaustive union-find audit then finds a physical vertex whose full
tensor has mode rank at most one.  Two sparse cycle patterns require separate
small core-tensor rank arguments, also checked exactly below.  Thus every
exact support orbit is obstructed.
"""

from __future__ import annotations

import itertools
from collections import Counter
from fractions import Fraction


BLOCKS = tuple(range(4))
VERTICES = tuple(range(8))
BLOCK_PAIRS = tuple(itertools.combinations(BLOCKS, 2))
CANONICAL_EDGES = {(0, 1), (2, 3), (4, 5), (6, 7)}
CROSS_EDGES = set(itertools.combinations(VERTICES, 2)) - CANONICAL_EDGES

# Bit order 00,01,10,11.  D=15; the four two-edge masks are stars.
EXACT_TYPES = (0, 1, 2, 4, 8, 3, 5, 10, 12, 15)


def perfect_matchings(vertices, allowed=CROSS_EDGES):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for second in vertices[1:]:
        edge = (first, second)
        if edge not in allowed:
            continue
        rest = tuple(v for v in vertices if v not in edge)
        for tail in perfect_matchings(rest, allowed):
            yield tuple(sorted((edge,) + tail))


MATCHING_CACHE = {
    frozenset(subset): tuple(perfect_matchings(subset))
    for size in range(0, 9, 2)
    for subset in itertools.combinations(VERTICES, size)
}


def edge_support(pattern):
    support = set()
    for (left, right), mask in zip(BLOCK_PAIRS, pattern, strict=True):
        for bit, (a, b) in enumerate(itertools.product(range(2), repeat=2)):
            if mask & (1 << bit):
                support.add((2 * left + a, 2 * right + b))
    return support


def transform_pattern(pattern, block_permutation, flips):
    transformed_edges = set()
    for u, v in edge_support(pattern):
        block_u, bit_u = divmod(u, 2)
        block_v, bit_v = divmod(v, 2)
        new_u = 2 * block_permutation[block_u] + (bit_u ^ flips[block_u])
        new_v = 2 * block_permutation[block_v] + (bit_v ^ flips[block_v])
        transformed_edges.add(tuple(sorted((new_u, new_v))))

    answer = []
    for left, right in BLOCK_PAIRS:
        mask = 0
        for bit, (a, b) in enumerate(itertools.product(range(2), repeat=2)):
            if (2 * left + a, 2 * right + b) in transformed_edges:
                mask |= 1 << bit
        answer.append(mask)
    return tuple(answer)


GROUP = tuple(
    (permutation, flips)
    for permutation in itertools.permutations(BLOCKS)
    for flips in itertools.product(range(2), repeat=4)
)


def canonical_pattern(pattern):
    return min(transform_pattern(pattern, *element) for element in GROUP)


def proper_matching_data(support):
    """Return proper block-union matching lists, or None for a singleton."""
    answer = []
    for mask in range(1, 15):
        vertices = frozenset(
            vertex
            for block in BLOCKS
            if mask & (1 << block)
            for vertex in (2 * block, 2 * block + 1)
        )
        matchings = tuple(
            matching
            for matching in MATCHING_CACHE[vertices]
            if set(matching) <= support
        )
        if len(matchings) == 1:
            return None
        answer.append((vertices, matchings))
    return tuple(answer)


def inherited_relations(support, full_matchings, proper_data):
    """Transport factored proper-subset identities to the full vertex set.

    If every term of a zero identity contains a common matching C, cancel
    the nonzero tensor product on C.  The residual zero relation may then be
    multiplied by any matching product on the complementary vertices.
    """
    full_index = {matching: index for index, matching in enumerate(full_matchings)}
    relations = []
    for _, matchings in proper_data:
        if len(matchings) < 2:
            continue
        common = set.intersection(*(set(matching) for matching in matchings))
        residual = tuple(
            tuple(edge for edge in matching if edge not in common)
            for matching in matchings
        )
        residual_vertices = {
            vertex for matching in residual for edge in matching for vertex in edge
        }
        complement = frozenset(set(VERTICES) - residual_vertices)
        for extension in MATCHING_CACHE[complement]:
            extended = tuple(
                tuple(sorted(matching + extension)) for matching in residual
            )
            if not all(matching in full_index for matching in extended):
                continue
            row = [Fraction(0) for _ in full_matchings]
            for matching in extended:
                row[full_index[matching]] += 1
            relations.append(row)
    return relations


def rref(rows, width):
    basis = []
    pivots = []
    for original in rows:
        row = list(original)
        for pivot, basis_row in zip(pivots, basis, strict=True):
            if row[pivot]:
                coefficient = row[pivot]
                row = [
                    value - coefficient * other
                    for value, other in zip(row, basis_row, strict=True)
                ]
        pivot = next((index for index, value in enumerate(row) if value), None)
        if pivot is None:
            continue
        scale = row[pivot]
        row = [value / scale for value in row]
        for index, basis_row in enumerate(basis):
            if basis_row[pivot]:
                coefficient = basis_row[pivot]
                basis[index] = [
                    value - coefficient * other
                    for value, other in zip(basis_row, row, strict=True)
                ]
        insertion = next(
            (index for index, old_pivot in enumerate(pivots) if old_pivot > pivot),
            len(pivots),
        )
        pivots.insert(insertion, pivot)
        basis.insert(insertion, row)
    return tuple(pivots), tuple(tuple(row) for row in basis)


def reduce_vector(vector, pivots, basis):
    answer = list(vector)
    for pivot, row in zip(pivots, basis, strict=True):
        if answer[pivot]:
            coefficient = answer[pivot]
            answer = [
                value - coefficient * other
                for value, other in zip(answer, row, strict=True)
            ]
    return tuple(answer)


def product_cut(vector, full_matchings):
    """Find a cut across which the represented full tensor is decomposable."""
    support_indices = [index for index, value in enumerate(vector) if value]
    for size in (2, 4):
        for subset_tuple in itertools.combinations(VERTICES, size):
            # Avoid checking both sides of a 4|4 cut.
            if size == 4 and 0 not in subset_tuple:
                continue
            subset = set(subset_tuple)
            complement = set(VERTICES) - subset
            if any(
                any((u in subset) != (v in subset) for u, v in full_matchings[index])
                for index in support_indices
            ):
                continue

            left_matchings = sorted(
                {
                    tuple(edge for edge in full_matchings[index] if set(edge) <= subset)
                    for index in support_indices
                }
            )
            right_matchings = sorted(
                {
                    tuple(
                        edge
                        for edge in full_matchings[index]
                        if set(edge) <= complement
                    )
                    for index in support_indices
                }
            )
            left_index = {matching: index for index, matching in enumerate(left_matchings)}
            right_index = {
                matching: index for index, matching in enumerate(right_matchings)
            }
            matrix = [
                [Fraction(0) for _ in right_matchings] for _ in left_matchings
            ]
            for matching, coefficient in zip(full_matchings, vector, strict=True):
                if not coefficient:
                    continue
                left = tuple(edge for edge in matching if set(edge) <= subset)
                right = tuple(edge for edge in matching if set(edge) <= complement)
                matrix[left_index[left]][right_index[right]] = coefficient

            # All 2x2 minors vanish exactly iff this nonzero matrix has rank one.
            rank_one = all(
                matrix[i][j] * matrix[k][ell]
                == matrix[i][ell] * matrix[k][j]
                for i, k in itertools.combinations(range(len(matrix)), 2)
                for j, ell in itertools.combinations(range(len(matrix[0])), 2)
            )
            if rank_one:
                return tuple(sorted(subset))
    return None


def classify_pattern(pattern):
    support = edge_support(pattern)
    full_matchings = tuple(
        matching
        for matching in MATCHING_CACHE[frozenset(VERTICES)]
        if set(matching) <= support
    )
    if len(full_matchings) < 2:
        return "support", len(full_matchings), None
    proper_data = proper_matching_data(support)
    if proper_data is None:
        return "singleton", len(full_matchings), None
    relations = inherited_relations(support, full_matchings, proper_data)
    pivots, basis = rref(relations, len(full_matchings))
    reduced = reduce_vector(
        tuple(Fraction(1) for _ in full_matchings), pivots, basis
    )
    if not any(reduced):
        return "zero", len(full_matchings), len(basis)
    cut = product_cut(reduced, full_matchings)
    if cut is not None:
        return "product", len(full_matchings), cut
    return "open", len(full_matchings), len(basis)


class UnionFind:
    """Equivalence classes of endpoint factor lines."""

    def __init__(self, parents=None):
        self.parents = {} if parents is None else dict(parents)

    def find(self, item):
        self.parents.setdefault(item, item)
        if self.parents[item] != item:
            self.parents[item] = self.find(self.parents[item])
        return self.parents[item]

    def union(self, first, second):
        first = self.find(first)
        second = self.find(second)
        if first != second:
            self.parents[second] = first

    def clone(self):
        return UnionFind(self.parents)


def layer_edges(support, block_pair):
    return tuple(
        edge
        for edge in support
        if {edge[0] // 2, edge[1] // 2} == set(block_pair)
    )


def star_center(support, block_pair):
    edges = layer_edges(support, block_pair)
    assert len(edges) == 2
    common = set(edges[0]) & set(edges[1])
    assert len(common) == 1
    return next(iter(common))


def incidences_toward(support, vertex, other_block):
    return tuple(
        (edge, vertex)
        for edge in support
        if vertex in edge
        and next(endpoint for endpoint in edge if endpoint != vertex) // 2
        == other_block
    )


def impose_corner(union_find, support, block, first_neighbor, second_neighbor):
    """Identify both endpoint lines toward the two indicated neighbors."""
    for vertex in (2 * block, 2 * block + 1):
        first = incidences_toward(support, vertex, first_neighbor)
        second = incidences_toward(support, vertex, second_neighbor)
        assert first and second
        incidences = first + second
        for incidence in incidences[1:]:
            union_find.union(incidences[0], incidence)


def triangle_matchings(support, triangle):
    vertices = frozenset(
        vertex for block in triangle for vertex in (2 * block, 2 * block + 1)
    )
    return tuple(
        matching
        for matching in MATCHING_CACHE[vertices]
        if set(matching) <= support
    )


def exact_support_representatives():
    """Enumerate all admissible exact supports and quotient by 384 symmetries."""
    admissible = []
    for pattern in itertools.product(EXACT_TYPES, repeat=len(BLOCK_PAIRS)):
        support = edge_support(pattern)
        full_count = sum(
            set(matching) <= support
            for matching in MATCHING_CACHE[frozenset(VERTICES)]
        )
        if full_count < 2:
            continue
        if any(
            len(triangle_matchings(support, triangle)) == 1
            for triangle in itertools.combinations(BLOCKS, 3)
        ):
            continue
        admissible.append(pattern)

    seen = set()
    representatives = []
    for pattern in admissible:
        if pattern in seen:
            continue
        orbit = {transform_pattern(pattern, *element) for element in GROUP}
        seen.update(orbit)
        representatives.append(min(orbit))

    # The two-block identities have zero or two terms for every EXACT_TYPE;
    # hence the triangle test above is equivalent to testing every proper
    # union of canonical pairs.  Check that assertion generically on orbits.
    assert all(
        proper_matching_data(edge_support(pattern)) is not None
        for pattern in representatives
    )
    return tuple(admissible), tuple(sorted(representatives))


def promotion_audit(pattern):
    """Apply the exact local rank-one/coherence consequences.

    Return the number of all-dense corner choices for which no physical
    vertex is forced to have a common rank-one endpoint line in every full
    matching, together with the number of as-yet-unpromoted full edges.
    """
    support = edge_support(pattern)
    pair_type = dict(zip(BLOCK_PAIRS, pattern, strict=True))
    rank_one = set()
    union_find = UnionFind()
    all_dense_triangles = []

    # Dense K2,2 components are crossing-Segre tensors.  Their four edge
    # matrices have rank one and the two incidences at each vertex agree.
    for block_pair, mask in pair_type.items():
        if mask != 15:
            continue
        edges = layer_edges(support, block_pair)
        assert len(edges) == 4
        rank_one.update(edges)
        for block in block_pair:
            for vertex in (2 * block, 2 * block + 1):
                incidences = tuple((edge, vertex) for edge in edges if vertex in edge)
                assert len(incidences) == 2
                union_find.union(*incidences)

    for triangle in itertools.combinations(BLOCKS, 3):
        pairs = tuple(itertools.combinations(triangle, 2))
        dense_pairs = tuple(pair for pair in pairs if pair_type[pair] == 15)
        matchings = triangle_matchings(support, triangle)

        if len(matchings) == 0:
            continue

        if len(matchings) == 2:
            # Cancel the common nonzero matching tensor.  Equality of the
            # two residual crossing products makes every residual edge
            # rank one and identifies the two endpoint factors at each
            # residual vertex.
            common = set(matchings[0]) & set(matchings[1])
            residual = tuple(
                tuple(edge for edge in matching if edge not in common)
                for matching in matchings
            )
            assert len(residual[0]) == len(residual[1]) >= 2
            rank_one.update(edge for matching in residual for edge in matching)
            residual_vertices = {
                vertex
                for matching in residual
                for edge in matching
                for vertex in edge
            }
            for vertex in residual_vertices:
                first = next(edge for edge in residual[0] if vertex in edge)
                second = next(edge for edge in residual[1] if vertex in edge)
                union_find.union((first, vertex), (second, vertex))
            continue

        if len(matchings) == 4:
            # The four-term promotion lemma has two cases: two dense layers
            # and one star, or one dense layer and two stars centered at the
            # two different vertices of the third block.
            assert len(dense_pairs) in (1, 2)
            used_edges = {edge for matching in matchings for edge in matching}
            rank_one.update(used_edges)
            for pair in pairs:
                if pair_type[pair] == 15:
                    continue
                assert pair_type[pair] in (3, 5, 10, 12)
                center = star_center(support, pair)
                incidences = tuple(
                    (edge, center)
                    for edge in used_edges
                    if edge in layer_edges(support, pair) and center in edge
                )
                assert len(incidences) == 2
                union_find.union(*incidences)

            if len(dense_pairs) == 2:
                common_block = next(iter(set(dense_pairs[0]) & set(dense_pairs[1])))
                star_pair = next(pair for pair in pairs if pair not in dense_pairs)
                center_block = star_center(support, star_pair) // 2
                noncenter_block = next(
                    block for block in star_pair if block != center_block
                )
                forced_blocks = (common_block, noncenter_block)
            else:
                forced_blocks = dense_pairs[0]

            for block in forced_blocks:
                neighbors = tuple(other for other in triangle if other != block)
                impose_corner(union_find, support, block, *neighbors)
            continue

        if len(matchings) == 8:
            assert len(dense_pairs) == 3
            all_dense_triangles.append(triangle)
            continue

        raise AssertionError((pattern, triangle, len(matchings)))

    full_matchings = tuple(
        matching
        for matching in MATCHING_CACHE[frozenset(VERTICES)]
        if set(matching) <= support
    )
    full_edges = {edge for matching in full_matchings for edge in matching}
    choices = tuple(
        tuple(
            subset
            for size in (2, 3)
            for subset in itertools.combinations(triangle, size)
        )
        for triangle in all_dense_triangles
    )

    bad_choices = 0
    selections = itertools.product(*choices) if choices else ((),)
    for selection in selections:
        selected_union_find = union_find.clone()
        for triangle, coherent_blocks in zip(
            all_dense_triangles, selection, strict=True
        ):
            for block in coherent_blocks:
                neighbors = tuple(other for other in triangle if other != block)
                impose_corner(
                    selected_union_find, support, block, *neighbors
                )

        has_rank_one_mode = False
        for vertex in VERTICES:
            incidences = tuple(
                (edge, vertex) for edge in full_edges if vertex in edge
            )
            if (
                incidences
                and all(edge in rank_one for edge, _ in incidences)
                and len(
                    {
                        selected_union_find.find(incidence)
                        for incidence in incidences
                    }
                )
                == 1
            ):
                has_rank_one_mode = True
                break
        if not has_rank_one_mode:
            bad_choices += 1

    return bad_choices, len(full_edges - rank_one)


def matrix_rank(matrix):
    if not matrix:
        return 0
    rows = [[Fraction(value) for value in row] for row in matrix]
    return len(rref(rows, len(rows[0]))[0])


def verify_local_core_ranks():
    """Check the sign-rank facts used in the four/eight-term lemmas."""

    def hadamard(row, column):
        return -1 if row == column == 1 else 1

    assert matrix_rank(((1, 1), (1, -1))) == 2

    # With dense layers AB and AC and a BC-star centered at B0, grouping by
    # the two star choices gives the coefficient rows -(X+Y) and X-Y.
    assert matrix_rank(((-1, -1), (1, -1))) == 2

    # Canonical all-dense triangle core, using increasing neighbor order at
    # every block.  Each of its three mode flattenings has rank two.
    neighbor_order = {0: (1, 2), 1: (0, 2), 2: (0, 1)}

    def endpoint(block, neighbor, state):
        return state[block] if neighbor_order[block][0] == neighbor else 1 - state[block]

    core = {}
    for bits in itertools.product(range(2), repeat=3):
        state = dict(zip(range(3), bits, strict=True))
        core[bits] = 1
        for left, right in ((0, 1), (0, 2), (1, 2)):
            core[bits] *= hadamard(
                endpoint(left, right, state), endpoint(right, left, state)
            )

    for mode in range(3):
        others = tuple(index for index in range(3) if index != mode)
        flattening = []
        for bit in range(2):
            row = []
            for other_bits in itertools.product(range(2), repeat=2):
                index = [None, None, None]
                index[mode] = bit
                for other, value in zip(others, other_bits, strict=True):
                    index[other] = value
                row.append(core[tuple(index)])
            flattening.append(row)
        assert matrix_rank(flattening) == 2


def verify_sparse_core_obstructions():
    """Check the two core tensors used for the exceptional sparse cycles."""

    def hadamard(row, column):
        return -1 if row == column == 1 else 1

    # (0,3,12,15,15,0): variables are the two star choices c,d and
    # which vertex a of block 1 goes to block 2.  All eight core entries
    # are nonzero and every mode flattening has rank two.
    three_core = {
        (a, c, d): hadamard(a, 1 - c) * hadamard(1 - a, 1 - d)
        for a, c, d in itertools.product(range(2), repeat=3)
    }
    assert all(three_core.values())
    for mode in range(3):
        others = tuple(index for index in range(3) if index != mode)
        matrix = []
        for bit in range(2):
            row = []
            for other_bits in itertools.product(range(2), repeat=2):
                index = [None, None, None]
                index[mode] = bit
                for other, value in zip(others, other_bits, strict=True):
                    index[other] = value
                row.append(three_core[tuple(index)])
            matrix.append(row)
        assert matrix_rank(matrix) == 2

    # (0,15,15,15,15,0): after the two doubled-layer contributions vanish,
    # the remaining block graph is the cycle 0-2-1-3-0.  Its Hadamard core
    # has Schmidt rank four across the adjacent-block cut {0,2}|{1,3}.
    neighbor_order = {0: (2, 3), 2: (0, 1), 1: (2, 3), 3: (1, 0)}

    def endpoint(block, neighbor, state):
        return state[block] if neighbor_order[block][0] == neighbor else 1 - state[block]

    four_core = {}
    for bits in itertools.product(range(2), repeat=4):
        state = dict(zip(BLOCKS, bits, strict=True))
        four_core[bits] = 1
        for left, right in ((0, 2), (1, 2), (1, 3), (0, 3)):
            four_core[bits] *= hadamard(
                endpoint(left, right, state), endpoint(right, left, state)
            )

    left_blocks = (0, 2)
    right_blocks = (1, 3)
    flattening = []
    for left_bits in itertools.product(range(2), repeat=2):
        row = []
        for right_bits in itertools.product(range(2), repeat=2):
            state = dict(zip(left_blocks, left_bits, strict=True))
            state.update(zip(right_blocks, right_bits, strict=True))
            row.append(four_core[tuple(state[block] for block in BLOCKS)])
        flattening.append(row)
    assert matrix_rank(flattening) == 4


def main():
    verify_local_core_ranks()
    admissible, representatives = exact_support_representatives()
    outcomes = {pattern: classify_pattern(pattern) for pattern in representatives}
    counts = Counter(outcome[0] for outcome in outcomes.values())

    assert len(admissible) == 73749
    assert len(representatives) == 501
    assert counts == Counter({"product": 318, "zero": 123, "open": 60})

    exceptional = {}
    coherence_closed = 0
    for pattern, outcome in outcomes.items():
        if outcome[0] != "open":
            continue
        audit = promotion_audit(pattern)
        if audit[0] == 0:
            coherence_closed += 1
        else:
            exceptional[pattern] = audit

    sparse_three_core = (0, 3, 12, 15, 15, 0)
    sparse_four_core = (0, 15, 15, 15, 15, 0)
    assert coherence_closed == 58
    assert exceptional == {
        sparse_three_core: (1, 4),
        sparse_four_core: (1, 0),
    }
    verify_sparse_core_obstructions()

    print(
        "exact supports: "
        f"admissible={len(admissible)}, orbits={len(representatives)}, "
        f"formal_outcomes={dict(sorted(counts.items()))}"
    )
    print("promotion/coherence audit closes 58 of the 60 formal open orbits")
    print("two sparse cycle cores close the final 2 orbits")
    print("all 501 admissible exact-support orbits are obstructed")


if __name__ == "__main__":
    main()
