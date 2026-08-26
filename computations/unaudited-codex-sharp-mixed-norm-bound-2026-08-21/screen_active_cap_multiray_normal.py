#!/usr/bin/env python3
"""Gaussian-phase quadratic guard on minimal 2-/3-ray no-carrier supports."""

from __future__ import annotations

from collections import defaultdict
from itertools import combinations, product
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import integrate_negative_multiray_family as family  # noqa: E402
import certify_active_cap_normal_cone as normal  # noqa: E402
from certify_eight_cell_global_branch import source_box  # noqa: E402
from certify_negative_family_global_min import I  # noqa: E402


PHASES = (1, -1, 1j, -1j)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def carrier_mask(ray):
    row = {"cells": tuple(normal.BOUNDARY_LEAK) + ray}
    mask = 0
    for index, cap in enumerate(normal.CAPS):
        if not normal.support_separated_identity_cap(row, *cap):
            mask |= 1 << index
    return mask


def full_blocker(indices, rays):
    source = {cell: None for cell in normal.BASE}
    source.update({cell: None for cell in normal.BOUNDARY_LEAK})
    for index in indices:
        source.update({cell: None for cell in rays[index]})
    try:
        stars, triangles = family.carrier_witnesses(source)
    except RuntimeError:
        return False
    return len(stars) == 168 and len(triangles) == 560


def minimal_supports(rays):
    masks = [carrier_mask(ray) for ray in rays]
    pairs = [indices for indices in combinations(range(len(rays)), 2)
             if masks[indices[0]] != 63 and masks[indices[1]] != 63
             and (masks[indices[0]] | masks[indices[1]]) == 63
             and full_blocker(indices, rays)]
    triples = []
    for indices in combinations(range(len(rays)), 3):
        if (masks[indices[0]] | masks[indices[1]] | masks[indices[2]]) != 63:
            continue
        if any((masks[left] | masks[right]) == 63
               for left, right in combinations(indices, 2)):
            continue
        if full_blocker(indices, rays):
            triples.append(indices)
    return pairs, triples


def term_ledger(active_cells):
    support = set(normal.BASE) | set(normal.BOUNDARY_LEAK) | set(active_cells)
    edge_cells = defaultdict(list)
    for cell in support:
        edge_cells[cell[:2]].append(cell)
    answer = defaultdict(list)
    for matching in family.PM8:
        choices = [edge_cells[edge] for edge in matching]
        if any(not choice for choice in choices):
            continue
        for picked in product(*choices):
            word = [None] * 8
            for u, v, a, b in picked:
                word[u], word[v] = a, b
            answer[tuple(word)].append(tuple(picked))
    return answer


VLO, VHI = normal.minimizer_v_interval()
BASE_INTERVAL = source_box(I(0), I(VLO, VHI))
BASE_SOURCE = {cell: (value.lo + value.hi) / 2
               for cell, value in BASE_INTERVAL.items()
               if cell in normal.BASE or cell in normal.BOUNDARY_LEAK}


def q_complex(direction, ledger):
    degree = defaultdict(float)
    for (u, v, a, b), value in direction.items():
        square = abs(value) ** 2
        degree[u, a] += square
        degree[v, b] += square
    source_w = {}
    for colour, layer in family.LAYERS.items():
        gaps = [BASE_SOURCE[edge + (colour, colour)] ** 2 for edge in layer]
        values = []
        for u, v in layer:
            require(abs(degree[u, colour] - degree[v, colour]) < 1e-12,
                    (direction, colour, u, v, degree))
            values.append(degree[u, colour])
        rho_w = sum(value / gap for value, gap in zip(values, gaps))
        rho_w /= sum(1 / gap for gap in gaps)
        for edge, value in zip(layer, values):
            diagonal = BASE_SOURCE[edge + (colour, colour)]
            source_w[edge + (colour, colour)] = (rho_w - value) / (2 * diagonal)
    for cell in normal.BOUNDARY_LEAK:
        source_w[cell] = 0.0

    q = 0.0
    for word, monomials in ledger.items():
        if len(set(word)) == 1:
            continue
        f0 = 0j
        linear = 0j
        quadratic = 0j
        for monomial in monomials:
            count = sum(cell in direction for cell in monomial)
            if count == 0:
                value = 1.0
                for cell in monomial:
                    value *= BASE_SOURCE[cell]
                f0 += value
                derivative = 0.0
                for index, cell in enumerate(monomial):
                    piece = source_w[cell]
                    for other, other_cell in enumerate(monomial):
                        if other != index:
                            piece *= BASE_SOURCE[other_cell]
                    derivative += piece
                quadratic += derivative
            elif count in (1, 2):
                value = 1 + 0j
                for cell in monomial:
                    value *= direction[cell] if cell in direction else BASE_SOURCE[cell]
                if count == 1:
                    linear += value
                else:
                    quadratic += value
        q += abs(linear) ** 2 + 2 * (f0.conjugate() * quadratic).real
    return q


def phase_states(ray):
    return tuple({ray[0]: left, ray[1]: right}
                 for left, right in product(PHASES, repeat=2))


def add_directions(*directions):
    answer = {}
    for direction in directions:
        for cell, value in direction.items():
            answer[cell] = answer.get(cell, 0) + value
    return {cell: value for cell, value in answer.items() if value}


def matrix(indices, states, rays, ledgers, diagonal_cache, cross_cache):
    size = len(indices)
    answer = [[0.0] * size for _ in range(size)]
    for place, (index, state_index) in enumerate(zip(indices, states)):
        key = index, state_index
        if key not in diagonal_cache:
            direction = phase_states(rays[index])[state_index]
            diagonal_cache[key] = q_complex(direction, ledgers[(index,)])
        answer[place][place] = diagonal_cache[key]
    for left, right in combinations(range(size), 2):
        i, si = indices[left], states[left]
        j, sj = indices[right], states[right]
        key = (i, si, j, sj) if i < j else (j, sj, i, si)
        if key not in cross_cache:
            di = phase_states(rays[i])[si]
            dj = phase_states(rays[j])[sj]
            total = q_complex(add_directions(di, dj), ledgers[tuple(sorted((i, j)))])
            cross_cache[key] = (total - answer[left][left] - answer[right][right]) / 2
        answer[left][right] = answer[right][left] = cross_cache[key]
    return answer


def det2(matrix, i, j):
    return matrix[i][i] * matrix[j][j] - matrix[i][j] ** 2


def det3(matrix):
    return (matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] ** 2)
            - matrix[0][1] * (matrix[0][1] * matrix[2][2]
                              - matrix[0][2] * matrix[1][2])
            + matrix[0][2] * (matrix[0][1] * matrix[1][2]
                              - matrix[0][2] * matrix[1][1]))


def structural_cross_zero(left, right, ledger):
    left_cells, right_cells = set(left), set(right)
    base_words, left_words, right_words, quadratic_words = set(), set(), set(), set()
    for word, monomials in ledger.items():
        if len(set(word)) == 1:
            continue
        for monomial in monomials:
            left_count = sum(cell in left_cells for cell in monomial)
            right_count = sum(cell in right_cells for cell in monomial)
            if left_count == right_count == 0:
                base_words.add(word)
            elif left_count == 1 and right_count == 0:
                left_words.add(word)
            elif left_count == 0 and right_count == 1:
                right_words.add(word)
            elif left_count == right_count == 1:
                quadratic_words.add(word)
    return not (left_words & right_words or quadratic_words & base_words)


def main():
    rays, _ = normal.star_hitting_rays()
    pairs, triples = minimal_supports(rays)
    used_singletons = {(index,) for support in pairs + triples for index in support}
    used_pairs = {tuple(sorted(pair)) for support in pairs + triples
                  for pair in combinations(support, 2)}
    ledgers = {key: term_ledger(sum((rays[index] for index in key), ()))
               for key in used_singletons | used_pairs}
    require(all(structural_cross_zero(rays[left], rays[right], ledgers[left, right])
                for left, right in used_pairs),
            "a cross-ray Hermitian or holomorphic word overlap survived")
    # With exact cross terms absent, positivity reduces to the one-ray phase
    # minima.  The Hermitian overlap of the two cells in every used ray also
    # vanishes structurally, so a real relative sign realizes the Gaussian
    # phase minimum; certify those values outward at the exact boundary root.
    exact_minima = []
    for (index,) in sorted(used_singletons):
        values = [normal.coefficient(rays[index], signs, VLO, VHI)
                  for signs in product((-1, 1), repeat=2)]
        exact_minima.append((min(value.lo for value in values), index, values))
    exact_minimum = min(exact_minima)
    require(exact_minimum[0] > 0, exact_minimum)
    diagonal_cache = {}
    cross_cache = {}
    minimum = None
    nonpositive = []
    for supports, size in ((pairs, 2), (triples, 3)):
        for indices in supports:
            for states in product(range(16), repeat=size):
                value = matrix(indices, states, rays, ledgers,
                               diagonal_cache, cross_cache)
                minors = [value[index][index] for index in range(size)]
                minors.extend(det2(value, i, j) for i, j in combinations(range(size), 2))
                if size == 3:
                    minors.append(det3(value))
                score = min(minors)
                record = (score, indices, states, value, minors)
                if minimum is None or score < minimum[0]:
                    minimum = record
                if score <= -1e-10:
                    nonpositive.append(record)
                    print("NONPOSITIVE", record)
                    return
    print("minimal supports", len(pairs), len(triples))
    print("Gaussian phase states", len(pairs) * 16 ** 2,
          len(triples) * 16 ** 3)
    print("minimum principal guard", minimum)
    print("structural zero cross-ray pairs", len(used_pairs))
    print("certified exact phase minimum", exact_minimum[0],
          "ray", exact_minimum[1], rays[exact_minimum[1]])
    print("nonpositive", len(nonpositive))
    require(not nonpositive, nonpositive)


if __name__ == "__main__":
    main()
