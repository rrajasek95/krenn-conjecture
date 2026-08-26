#!/usr/bin/env python3
"""Exact finite support ledger for the tail-response monomial boundaries.

This audit stays in the four-anchor diagonal chart.  It enumerates the exact
cross-block supports compatible with the six permanent and four reduced
triangle equations, quotients their inclusion-minimal members by the
order-96 fixed-tail group, and evaluates the literal 611+71+332 source-row
support matrix.  It deliberately does not infer coefficient existence from
support compatibility.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache, reduce
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_tail_support_boundary_orbits.json"
NONMONOMIAL = HERE / "results_tail_nonmonomial_boundary_closure.json"
SINGLE = HERE / "results_single_cofactor_boundary.json"
PRIMES = HERE / "results_single_boundary_monomial_primes.json"
FILTER = HERE / "results_prime_support_filter.json"
SUPPORT6 = (HERE.parent /
            "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20" /
            "results_support6_component_pairwise_obstruction.json")

VERTICES = tuple(range(8))
RESIDUAL = tuple(range(6))
TAILS = (6, 7)
SUPER_EDGES = tuple(combinations(range(4), 2))
PHYSICAL_EDGES = tuple(combinations(range(8), 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(PHYSICAL_EDGES)}
ANCHORS = frozenset(((0, 1), (2, 3), (4, 5), (6, 7)))
COLUMNS = tuple((site, tail) for tail in TAILS for site in RESIDUAL)
COLUMN_NAMES = tuple((f"y{site}" if tail == 6 else f"z{site}")
                     for site, tail in COLUMNS)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def logical_hash(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def file_hash(path):
    return sha256(path.read_bytes()).hexdigest()


def physical_edge(i, j, clone_i, clone_j):
    return tuple(sorted((2*i + clone_i, 2*j + clone_j)))


def block_cells(i, j):
    return tuple(physical_edge(i, j, ci, cj)
                 for ci, cj in product((0, 1), repeat=2))


CROSS_EDGES = tuple(edge for ij in SUPER_EDGES for edge in block_cells(*ij))
CROSS_INDEX = {edge: index for index, edge in enumerate(CROSS_EDGES)}


def edge_mask(edges):
    return sum(1 << EDGE_INDEX[tuple(sorted(edge))] for edge in edges)


ANCHOR_MASK = edge_mask(ANCHORS)


def support_edges(cross_mask):
    return frozenset(ANCHORS | {
        edge for index, edge in enumerate(CROSS_EDGES)
        if (cross_mask >> index) & 1
    })


def triangle_terms(i, j, k):
    return tuple(frozenset((
        physical_edge(i, j, ci, cj),
        physical_edge(i, k, 1-ci, ck),
        physical_edge(j, k, 1-cj, 1-ck),
    )) for ci, cj, ck in product((0, 1), repeat=3))


TRIANGLE_TERMS = tuple(triangle_terms(*triple)
                       for triple in combinations(range(4), 3))


def cross_supports():
    """All exact supports compatible at support level, and their minima."""
    # Each permanent has the live normalized anchor term.  Hence at least
    # one of the diagonal/off-diagonal cross products must also be live.
    allowed_blocks = (0b1001, 0b0110, 0b1011, 0b1101,
                      0b0111, 0b1110, 0b1111)
    accepted = []
    for block_masks in product(allowed_blocks, repeat=6):
        cross = sum(block_masks[index] << (4*index)
                    for index in range(6))
        edges = support_edges(cross)
        if all(any(term <= edges for term in terms)
               for terms in TRIANGLE_TERMS):
            accepted.append(cross)
    accepted_set = set(accepted)
    minima = []
    for mask in sorted(accepted, key=lambda value: (value.bit_count(), value)):
        # Deleting any live cell is sufficient because accepted supports are
        # upward closed.
        if not any((mask ^ (1 << bit)) in accepted_set
                   for bit in range(24) if (mask >> bit) & 1):
            minima.append(mask)
    return tuple(accepted), tuple(minima)


def fixed_tail_vertex_actions():
    answer = set()
    for block_permutation in permutations(range(3)):
        for flips in product((0, 1), repeat=4):
            action = []
            for vertex in VERTICES:
                block, clone = divmod(vertex, 2)
                image_block = (block_permutation[block]
                               if block < 3 else 3)
                action.append(2*image_block + (clone ^ flips[block]))
            answer.add(tuple(action))
    require(len(answer) == 96, "fixed-tail group order changed")
    return tuple(sorted(answer))


def full_b4_vertex_actions():
    answer = set()
    for block_permutation in permutations(range(4)):
        for flips in product((0, 1), repeat=4):
            action = []
            for vertex in VERTICES:
                block, clone = divmod(vertex, 2)
                action.append(2*block_permutation[block]
                              + (clone ^ flips[block]))
            answer.add(tuple(action))
    require(len(answer) == 384, "B4 order changed")
    return tuple(sorted(answer))


def act_cross_mask(mask, action):
    answer = 0
    for index, edge in enumerate(CROSS_EDGES):
        if not ((mask >> index) & 1):
            continue
        image = tuple(sorted((action[edge[0]], action[edge[1]])))
        answer |= 1 << CROSS_INDEX[image]
    return answer


def quotient_masks(masks, actions):
    universe = set(masks)
    unseen = set(masks)
    records = []
    while unseen:
        representative = min(unseen)
        orbit = {act_cross_mask(representative, action)
                 for action in actions}
        orbit &= universe
        require(orbit, "empty support orbit")
        unseen -= orbit
        records.append({
            "representative": representative,
            "orbit_size": len(orbit),
            "support_size": representative.bit_count(),
        })
    return tuple(records)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index+1:]
        answer.extend((((first, second),) + tail
                       for tail in perfect_matchings(rest)))
    return tuple(answer)


@lru_cache(None)
def has_matching(support_mask, subset):
    return any(all((support_mask >> EDGE_INDEX[tuple(sorted(edge))]) & 1
                       for edge in matching)
               for matching in perfect_matchings(subset))


def profile(word):
    return tuple(sorted(Counter(word).values(), reverse=True))


def source_term(word, column):
    """Coefficient support datum for one literal source row entry.

    A 332 entry is a product of three named edges.  A 611/71 entry contains
    one six-vertex Hafnian; the latter is recorded by its colour and subset.
    """
    site, tail = column
    if word[site] != 0 or word[tail] != 1:
        return None
    remaining = tuple(v for v in VERTICES if v not in (site, tail))
    counts = Counter(word)
    counts[0] -= 1
    counts[1] -= 1
    if any(counts[colour] % 2 for colour in range(3)):
        return None
    factors = []
    for colour in range(3):
        subset = tuple(v for v in remaining if word[v] == colour)
        if len(subset) == 2:
            factors.append(("edge", colour, tuple(sorted(subset))))
        elif len(subset) == 6:
            factors.append(("hafnian6", colour, subset))
        elif subset:
            raise RuntimeError(("unexpected coefficient subset", word,
                                column, colour, subset))
    return tuple(factors)


def source_rows():
    wanted = {(7, 1), (6, 1, 1), (3, 3, 2)}
    rows = []
    for word in product(range(3), repeat=8):
        kind = profile(word)
        if kind not in wanted:
            continue
        entries = tuple(source_term(word, column) for column in COLUMNS)
        if any(entry is not None for entry in entries):
            rows.append((word, kind, entries))
    require(Counter(kind for _, kind, _ in rows) == {
        (7, 1): 8, (6, 1, 1): 12, (3, 3, 2): 360,
    }, "literal source-row census changed")
    return tuple(rows)


def entry_live(entry, graph_masks):
    if entry is None:
        return False
    for kind, colour, datum in entry:
        if kind == "edge":
            if not ((graph_masks[colour] >> EDGE_INDEX[datum]) & 1):
                return False
        else:
            require(kind == "hafnian6", ("unknown factor kind", kind))
            if not has_matching(graph_masks[colour], datum):
                return False
    return True


def row_masks(graph_masks, rows):
    answer = []
    identities = []
    for word, kind, entries in rows:
        mask = sum(1 << column for column, entry in enumerate(entries)
                   if entry_live(entry, graph_masks))
        if mask:
            answer.append(mask)
            identities.append((word, kind))
    return tuple(answer), tuple(identities)


def matching_rank(row_supports):
    """Maximum bipartite matching of source rows into the 12 columns."""
    matched_row = {}

    def augment(row, seen):
        mask = row_supports[row]
        while mask:
            bit = mask & -mask
            column = bit.bit_length()-1
            mask ^= bit
            if column in seen:
                continue
            seen.add(column)
            if column not in matched_row or augment(matched_row[column], seen):
                matched_row[column] = row
                return True
        return False

    rank = 0
    for row in range(len(row_supports)):
        rank += augment(row, set())
        if rank == 12:
            break
    witness = tuple(sorted((column, row)
                           for column, row in matched_row.items()))
    return rank, witness


def triangular_rank(row_supports):
    """Greedy unique-matching minor: each new row has one future column."""
    used_columns = 0
    witness = []
    while True:
        selected = None
        for row, support in enumerate(row_supports):
            remaining = support & ~used_columns
            if remaining and not (remaining & (remaining-1)):
                selected = row, remaining.bit_length()-1
                break
        if selected is None:
            break
        row, column = selected
        used_columns |= 1 << column
        witness.append((column, row))
        if used_columns == (1 << 12)-1:
            break
    return used_columns.bit_count(), tuple(sorted(witness))


def full_graph_mask(cross_mask):
    return ANCHOR_MASK | edge_mask(
        edge for index, edge in enumerate(CROSS_EDGES)
        if (cross_mask >> index) & 1)


def mask_edges(mask):
    return ["%d%d" % edge for index, edge in enumerate(CROSS_EDGES)
            if (mask >> index) & 1]


@dataclass(frozen=True)
class K:
    """a+b*r in Q[r]/(r^2-2r-1)."""

    a: Fraction = Fraction(0)
    b: Fraction = Fraction(0)

    def __add__(self, other):
        other = as_k(other)
        return K(self.a+other.a, self.b+other.b)

    __radd__ = __add__

    def __neg__(self):
        return K(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-as_k(other))

    def __rsub__(self, other):
        return as_k(other) - self

    def __mul__(self, other):
        other = as_k(other)
        return K(self.a*other.a + self.b*other.b,
                 self.a*other.b + self.b*other.a
                 + 2*self.b*other.b)

    __rmul__ = __mul__

    def inverse(self):
        norm = self.a*self.a + 2*self.a*self.b - self.b*self.b
        require(norm != 0, ("division by zero in K", self))
        return K((self.a+2*self.b)/norm, -self.b/norm)

    def __truediv__(self, other):
        return self * as_k(other).inverse()

    def __pow__(self, exponent):
        if exponent < 0:
            return (self.inverse()) ** (-exponent)
        answer = K(Fraction(1))
        base = self
        while exponent:
            if exponent & 1:
                answer *= base
            base *= base
            exponent //= 2
        return answer

    def __bool__(self):
        return bool(self.a or self.b)

    def encode(self):
        return [[self.a.numerator, self.a.denominator],
                [self.b.numerator, self.b.denominator]]


def as_k(value):
    return value if isinstance(value, K) else K(Fraction(value))


KZERO = K()
KONE = K(Fraction(1))
R = K(Fraction(0), Fraction(1))
RCONJ = K(Fraction(2), Fraction(-1))


def determinant_integer(matrix):
    """Small exact determinant."""
    matrix = [list(map(Fraction, row)) for row in matrix]
    answer = Fraction(1)
    for column in range(len(matrix)):
        pivot = next((row for row in range(column, len(matrix))
                      if matrix[row][column]), None)
        if pivot is None:
            return 0
        if pivot != column:
            matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
            answer = -answer
        value = matrix[column][column]
        answer *= value
        matrix[column] = [entry/value for entry in matrix[column]]
        for row in range(column+1, len(matrix)):
            scale = matrix[row][column]
            if scale:
                matrix[row] = [left-scale*right
                               for left, right in zip(matrix[row],
                                                      matrix[column])]
    require(answer.denominator == 1, ("nonintegral determinant", answer))
    return answer.numerator


def solve_integer_matrix(matrix, values):
    """Solve a unimodular square log system multiplicatively in K*."""
    size = len(matrix)
    augmented = [[Fraction(value) for value in row]
                 + [Fraction(1 if i == j else 0) for j in range(size)]
                 for i, row in enumerate(matrix)]
    for column in range(size):
        pivot = next(row for row in range(column, size)
                     if augmented[row][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [entry/scale for entry in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            scale = augmented[row][column]
            if scale:
                augmented[row] = [left-scale*right for left, right in
                                  zip(augmented[row], augmented[column])]
    inverse = [row[size:] for row in augmented]
    require(all(entry.denominator == 1 for row in inverse for entry in row),
            "chosen exponent minor was not unimodular")
    answer = []
    for row in inverse:
        value = KONE
        for factor, exponent in zip(values, row):
            value *= factor ** int(exponent)
        answer.append(value)
    return tuple(answer)


def size12_triangle_data(cross_mask):
    """Return c_t,v_t for triangle_t = c X^v-c X^-v."""
    edge_position = {edge: index for index, edge in enumerate(SUPER_EDGES)}

    def entry(i, j, ci, cj):
        if i > j:
            i, j, ci, cj = j, i, cj, ci
        block = edge_position[(i, j)]
        position = 2*ci+cj
        block_mask = (cross_mask >> (4*block)) & 15
        if not ((block_mask >> position) & 1):
            return None
        first = 1 if block_mask == 0b0110 else 0
        return ((1 if position == first else -1),
                (1 if position == first else -1), block)

    records = []
    for i, j, k in combinations(range(4), 3):
        terms = []
        for ci, cj, ck in product((0, 1), repeat=3):
            factors = (entry(i, j, ci, cj),
                       entry(i, k, 1-ci, ck),
                       entry(j, k, 1-cj, 1-ck))
            if all(factors):
                coefficient = 1
                exponent = [0]*6
                for sign, power, block in factors:
                    coefficient *= sign
                    exponent[block] += power
                terms.append((coefficient, tuple(exponent)))
        require(len(terms) == 2 and terms[1] ==
                (-terms[0][0], tuple(-value for value in terms[0][1])),
                ("size-12 triangle ceased to be reciprocal binomial",
                 cross_mask, (i, j, k), terms))
        records.append(terms[0])
    return tuple(records)


def relation_four(vectors):
    candidates = []
    for relation in product((-1, 1), repeat=4):
        if relation[0] != 1:
            continue
        if all(sum(relation[row]*vectors[row][column]
                   for row in range(4)) == 0 for column in range(6)):
            candidates.append(relation)
    require(len(candidates) == 1, ("triangle relation changed", vectors))
    return candidates[0]


def graph_from_size12_branch(cross_mask, root_bits):
    data = size12_triangle_data(cross_mask)
    vectors = tuple(vector for _coefficient, vector in data)
    relation = relation_four(vectors)
    roots = tuple(RCONJ if (root_bits >> row) & 1 else R
                  for row in range(4))
    target = tuple(root/as_k(coefficient)
                   for root, (coefficient, _vector) in zip(roots, data))
    relation_left = KONE
    relation_right = KONE
    for exponent, root, (coefficient, _vector) in zip(
            relation, roots, data):
        relation_left *= root ** exponent
        relation_right *= as_k(coefficient) ** exponent
    if relation_left != relation_right:
        return None

    # Use three independent triangle rows and any unimodular 3-column minor;
    # the remaining three block variables are fixed to one.  This is a gauge
    # representative of the three-dimensional anchor-preserving site torus.
    pivot_columns = None
    for columns in combinations(range(6), 3):
        matrix = [[vectors[row][column] for column in columns]
                  for row in range(3)]
        if abs(determinant_integer(matrix)) == 1:
            pivot_columns = columns
            break
    require(pivot_columns is not None, "no unimodular triangle exponent minor")
    matrix = [[vectors[row][column] for column in pivot_columns]
              for row in range(3)]
    solved = solve_integer_matrix(matrix, target[:3])
    block_values = [KONE]*6
    for column, value in zip(pivot_columns, solved):
        block_values[column] = value
    require(all(as_k(coefficient) * reduce(
                    lambda left, pair: left*(block_values[pair[0]]**pair[1]),
                    enumerate(vector), KONE) == root
                for root, (coefficient, vector) in zip(roots, data)),
            "fourth triangle equation failed after exponent solve")

    graph = {edge: KONE for edge in ANCHORS}
    for block, (i, j) in enumerate(SUPER_EDGES):
        block_mask = (cross_mask >> (4*block)) & 15
        first = 1 if block_mask == 0b0110 else 0
        cells = block_cells(i, j)
        graph[cells[first]] = block_values[block]
        other = 2 if first == 1 else 3
        graph[cells[other]] = -KONE/block_values[block]
    return graph


def hafnian_value(graph, vertices):
    answer = KZERO
    for matching in perfect_matchings(tuple(vertices)):
        term = KONE
        for edge in matching:
            term *= graph.get(tuple(sorted(edge)), KZERO)
        answer += term
    return answer


def graph_signature(graph):
    x_support = frozenset(index for index, edge in enumerate(CROSS_EDGES)
                          if graph.get(edge, KZERO))
    cofactors = tuple(hafnian_value(graph, tuple(
        vertex for vertex in VERTICES if vertex not in edge))
        for edge in CROSS_EDGES)
    q_values = []
    for value in range(16):
        bits = tuple((value >> (3-site)) & 1 for site in range(4))
        answer = KZERO
        for (i, j), (k, l) in (((0, 1), (2, 3)),
                               ((0, 2), (1, 3)),
                               ((0, 3), (1, 2))):
            answer += (graph.get(physical_edge(i, j, bits[i], bits[j]), KZERO)
                       * graph.get(physical_edge(k, l, bits[k], bits[l]), KZERO))
        q_values.append(answer)
    h_value = hafnian_value(graph, VERTICES)
    return (x_support,
            frozenset(index for index, value in enumerate(cofactors) if value),
            frozenset(index for index, value in enumerate(q_values) if value),
            h_value)


def raw_action_index(raw_index, action):
    edge = CROSS_EDGES[raw_index]
    image = tuple(sorted((action[edge[0]], action[edge[1]])))
    return CROSS_INDEX[image]


def q_action_index(value, action):
    old = tuple((value >> (3-site)) & 1 for site in range(4))
    new = [0]*4
    for site in range(4):
        old_vertex = 2*site + old[site]
        image_vertex = action[old_vertex]
        image_site, image_clone = divmod(image_vertex, 2)
        new[image_site] = image_clone
    return sum(new[site] << (3-site) for site in range(4))


def support6_joint_orbit(actions, payload):
    base = (frozenset(payload["x_support"]),
            frozenset(payload["cofactor_support"]),
            frozenset(payload["q_support"]))
    return frozenset((
        frozenset(raw_action_index(index, action) for index in base[0]),
        frozenset(raw_action_index(index, action) for index in base[1]),
        frozenset(q_action_index(index, action) for index in base[2]),
    ) for action in actions)


def canonical_support6_graph():
    """Frozen support6 point, translated by z=r-2."""
    z = R-as_k(2)
    b_values = (z, -z-as_k(2), KONE, -z-as_k(2), KONE, KONE)
    c_values = (-z-as_k(2), z, -KONE, z, -KONE, -KONE)
    require(all(left*right == -KONE
                for left, right in zip(b_values, c_values)),
            "canonical support6 permanent products changed")
    graph = {edge: KONE for edge in ANCHORS}
    for block, (i, j) in enumerate(SUPER_EDGES):
        cells = block_cells(i, j)
        graph[cells[1]] = b_values[block]
        graph[cells[2]] = c_values[block]
    return graph


def act_graph(graph, action):
    return {tuple(sorted((action[edge[0]], action[edge[1]]))): value
            for edge, value in graph.items()}


def support6_gauge_witness(graph, actions):
    """Find B4 action and anchor-preserving clone scalings to canonical."""
    target = canonical_support6_graph()
    target_support = frozenset(target)
    for action in actions:
        moved = act_graph(graph, action)
        if frozenset(moved) != target_support:
            continue
        ratios = {}
        for i, j in SUPER_EDGES:
            edge = physical_edge(i, j, 0, 1)
            ratios[i, j] = target[edge]/moved[edge]
        lambdas = [KONE]
        lambdas.extend(KONE/ratios[0, site] for site in (1, 2, 3))
        if all(ratios[i, j] == lambdas[i]/lambdas[j]
               for i, j in SUPER_EDGES):
            # Check every cell, including anchors, rather than only b_ij.
            scaled = {}
            for edge, value in moved.items():
                i, ci = divmod(edge[0], 2)
                j, cj = divmod(edge[1], 2)
                factor_i = lambdas[i] if ci == 0 else KONE/lambdas[i]
                factor_j = lambdas[j] if cj == 0 else KONE/lambdas[j]
                scaled[edge] = value*factor_i*factor_j
            require(scaled == target,
                    "claimed support6 gauge witness failed literal cells")
            return action, tuple(lambdas)
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--rank-scan", choices=("none", "diagonal", "joint"),
                        default="diagonal")
    args = parser.parse_args()

    nonmonomial = json.loads(NONMONOMIAL.read_text())
    single = json.loads(SINGLE.read_text())
    primes = json.loads(PRIMES.read_text())
    support_filter = json.loads(FILTER.read_text())
    support6 = json.loads(SUPPORT6.read_text())
    require(nonmonomial["logical_sha256"] ==
            "66e8fd767c2872383dda79de63a880eef67ff01e5ab86dcc791bdacf7b5f10bc",
            "nonmonomial closure changed")
    require(single["logical_sha256"] ==
            "e98ff441ead785676089d2986ef62704467f0bd93a9db117836524e9d42639fe",
            "single-cofactor closure changed")
    require(primes["logical_sha256"] ==
            "af23ec140df2b126af7195b65aff62f9f489805e4509328794438c98a80efc8c",
            "single-boundary prime census changed")

    accepted, minima = cross_supports()
    require(len(accepted) == 112473, "accepted cross-support census changed")
    require(Counter(mask.bit_count() for mask in minima) ==
            {12: 8, 13: 96, 14: 864, 15: 256},
            "minimal support-size census changed")
    fixed_actions = fixed_tail_vertex_actions()
    b4_actions = full_b4_vertex_actions()
    fixed_orbits = quotient_masks(minima, fixed_actions)
    b4_orbits = quotient_masks(minima, b4_actions)
    require(len(minima) == 1224 and len(fixed_orbits) == 19
            and len(b4_orbits) == 9,
            "minimal support orbit census changed")

    rows = source_rows()

    # Solve the only structurally deficient one-colour support orbit exactly.
    # Every block has precisely one live permanent product.  The four reduced
    # triangles become reciprocal Laurent binomials Y-Y^-1=2.
    small_supports = tuple(mask for mask in minima if mask.bit_count() == 12)
    support6_orbit = support6_joint_orbit(b4_actions, support6)
    require(len(support6_orbit) == 24, "support6 joint orbit changed")
    laurent_records = []
    for cross in small_supports:
        orientation = sum(
            (((cross >> (4*block)) & 15) == 0b1001) << block
            for block in range(6))
        data = size12_triangle_data(cross)
        relation = relation_four(tuple(vector for _, vector in data))
        valid_bits = []
        signatures = set()
        h_values = set()
        branch_records = []
        for root_bits in range(16):
            graph = graph_from_size12_branch(cross, root_bits)
            if graph is None:
                continue
            valid_bits.append(root_bits)
            x_support, c_support, q_support, h_value = graph_signature(graph)
            signatures.add((x_support, c_support, q_support))
            h_values.add(h_value)
            require((x_support, c_support, q_support) in support6_orbit,
                    ("Laurent branch left support6 joint orbit",
                     orientation, root_bits, x_support, c_support, q_support))
            require(h_value == as_k(4),
                    ("Laurent branch pure H changed", orientation,
                     root_bits, h_value))
            gauge_witness = support6_gauge_witness(graph, b4_actions)
            require(gauge_witness is not None,
                    ("Laurent branch is not gauge/B4-equivalent to frozen "
                     "support6", orientation, root_bits))
            action, lambdas = gauge_witness
            branch_records.append({
                "root_bit_mask": root_bits,
                "X_support": sorted(x_support),
                "C_support": sorted(c_support),
                "Q_support": sorted(q_support),
                "H": h_value.encode(),
                "B4_vertex_map_to_canonical": list(action),
                "anchor_preserving_clone_scalings": [
                    value.encode() for value in lambdas],
            })
        laurent_records.append({
            "cross_support": cross,
            "orientation_mask": orientation,
            "triangle_exponent_relation": list(relation),
            "valid_root_bit_masks": valid_bits,
            "valid_branch_count": len(valid_bits),
            "joint_signature_count": len(signatures),
            "all_signatures_in_support6_B4_orbit": True,
            "all_branches_B4_gauge_equivalent_to_frozen_support6": True,
            "pure_H_values": [value.encode() for value in sorted(
                h_values, key=lambda value: (value.a, value.b))],
            "branches": branch_records,
        })
    require(Counter(record["valid_branch_count"]
                    for record in laurent_records) == {6: 8},
            "size-12 Laurent branch census changed")
    require(sum(record["valid_branch_count"]
                for record in laurent_records) == 48,
            "size-12 Laurent total changed")

    # This labelled 8^3 census is deliberately kept separate from the larger
    # simultaneous quotient below: it proves the exact alignment assertion.
    small_triple_ranks = Counter()
    small_triple_deficient = []
    for support0, support1, support2 in product(small_supports, repeat=3):
        graph_masks = tuple(full_graph_mask(support)
                            for support in (support0, support1, support2))
        supports, _identities = row_masks(graph_masks, rows)
        rank, _witness = triangular_rank(supports)
        small_triple_ranks[rank] += 1
        if rank < 12:
            small_triple_deficient.append((support0, support1, support2,
                                           rank))
    require(small_triple_ranks == {12: 504, 6: 8}
            and all(support0 == support1 == support2 and rank == 6
                    for support0, support1, support2, rank
                    in small_triple_deficient),
            "size-12 three-colour triangular-rank census changed")
    diagonal_ranks = Counter()
    deficient_diagonal = []
    if args.rank_scan in ("diagonal", "joint"):
        for support in minima:
            graph = full_graph_mask(support)
            supports, profiles = row_masks((graph, graph, graph), rows)
            rank, witness = triangular_rank(supports)
            diagonal_ranks[rank] += 1
            if rank < 12:
                deficient_diagonal.append({
                    "cross_support": support,
                    "cross_edges": mask_edges(support),
                    "support_size": support.bit_count(),
                    "rank": rank,
                    "live_row_count": len(supports),
                })

    joint_ranks = Counter()
    joint_deficient = []
    joint_representatives = 0
    joint_witness_counts = Counter()
    joint_ledger_hasher = sha256()
    if args.rank_scan == "joint":
        # If G2 has >=13 cells, all twelve literal 611 pivots are support-
        # live (verified below), so only its unique size-12 fixed-tail orbit
        # needs a joint G0,G1 analysis.  Fixing its representative leaves a
        # group of order 12.  Quotient G0 by that group and then G1 by the
        # stabilizer of the pair; this is the exact simultaneous quotient.
        canonical2 = min(mask for mask in minima if mask.bit_count() == 12)
        stabilizer2 = tuple(action for action in fixed_actions
                            if act_cross_mask(canonical2, action) == canonical2)
        require(len(stabilizer2) == 12, "size-12 stabilizer changed")
        unseen0 = set(minima)
        representatives0 = []
        while unseen0:
            support0 = min(unseen0)
            orbit0 = {act_cross_mask(support0, action)
                      for action in stabilizer2}
            unseen0 -= orbit0
            representatives0.append(support0)
        graph2 = full_graph_mask(canonical2)
        for support0 in representatives0:
            stabilizer20 = tuple(
                action for action in stabilizer2
                if act_cross_mask(support0, action) == support0)
            unseen1 = set(minima)
            while unseen1:
                support1 = min(unseen1)
                orbit1 = {act_cross_mask(support1, action)
                          for action in stabilizer20}
                unseen1 -= orbit1
                graph_masks = (full_graph_mask(support0),
                               full_graph_mask(support1), graph2)
                supports, identities = row_masks(graph_masks, rows)
                rank, witness = triangular_rank(supports)
                joint_representatives += 1
                joint_ranks[rank] += 1
                witness_key = tuple(
                    (COLUMN_NAMES[column],
                     "F_"+"".join(map(str, identities[row][0])))
                    for column, row in witness)
                if rank == 12:
                    joint_witness_counts[witness_key] += 1
                joint_ledger_hasher.update(json.dumps(
                    [support0, support1, canonical2, rank, witness_key],
                    separators=(",", ":")).encode())
                if rank < 12:
                    joint_deficient.append({
                        "G0_cross_support": support0,
                        "G1_cross_support": support1,
                        "G2_cross_support": canonical2,
                        "support_sizes": [support0.bit_count(),
                                          support1.bit_count(), 12],
                        "rank": rank,
                    })
        require(diagonal_ranks == {12: 1216, 6: 8},
                "one-colour triangular rank census changed")
        require(joint_representatives == 125956
                and joint_ranks == {12: 125955, 6: 1}
                and len(joint_deficient) == 1,
                "simultaneous triangular rank census changed")
        require(joint_deficient[0]["G0_cross_support"]
                == joint_deficient[0]["G1_cross_support"]
                == joint_deficient[0]["G2_cross_support"]
                and joint_deficient[0]["rank"] == 6,
                "the unique simultaneous survivor ceased to be aligned")
        require(len(joint_witness_counts) == 10222,
                "triangular witness-pattern census changed")
        require(joint_ledger_hasher.hexdigest() ==
                "9fd83c462cee829fac3c8d6854448491216e0621a34548f6bb80e49d7823c311",
                "simultaneous matching ledger digest changed")

    result = {
        "status": "PASS exhaustive four-orbit tail support-boundary theorem",
        "four_support_factor_orbits": [
            {
                "name": "h_residual_tail",
                "representative_zero": "h2_06",
                "labelled_count_with_sound_colour_permutations": 36,
                "route": "closed by exact single-cofactor monomial-prime chain",
                "terminal_localized_survivors": 0,
            },
            {
                "name": "g_residual_same_block",
                "representative_zero": "g0_01",
                "labelled_count_with_sound_colour_permutations": 9,
                "route": "empty in the four-anchor chart because g0_01=1",
                "terminal_localized_survivors": 0,
            },
            {
                "name": "g_residual_distinct_blocks",
                "representative_zero": "g0_02",
                "labelled_count_with_sound_colour_permutations": 36,
                "route": "finite cross-support/source-rank ledger below",
            },
            {
                "name": "g_residual_tail",
                "representative_zero": "g0_06",
                "labelled_count_with_sound_colour_permutations": 36,
                "route": "same finite cross-support/source-rank ledger below",
            },
        ],
        "one_colour_cross_support_census": {
            "block_support_options": 7,
            "raw_block_tuples": 7**6,
            "permanent_and_reduced_triangle_support_compatible": len(accepted),
            "inclusion_minimal_count": len(minima),
            "minimal_size_histogram": dict(sorted(
                Counter(mask.bit_count() for mask in minima).items())),
            "fixed_tail_orbits": len(fixed_orbits),
            "fixed_tail_orbits_by_size": dict(sorted(Counter(
                row["support_size"] for row in fixed_orbits).items())),
            "full_B4_orbits": len(b4_orbits),
            "fixed_tail_orbit_ledger": fixed_orbits,
        },
        "size12_exact_Laurent_classification": {
            "equations": (
                "Each block has entries x_e,-x_e^-1. Each reduced triangle "
                "is Y_t-Y_t^-1=2, so Y_t is r or 2-r in "
                "Q(r), r^2-2r-1=0."),
            "support_count": len(small_supports),
            "records": laurent_records,
            "coefficient_compatible_support_count": sum(
                bool(record["valid_branch_count"])
                for record in laurent_records),
            "normalized_branch_count": sum(
                record["valid_branch_count"] for record in laurent_records),
            "old_24_branch_mutation_fired": (
                sum(record["valid_branch_count"]
                    for record in laurent_records) != 24),
            "anchor_preserving_gauge": (
                "The three free block variables are the residual quotient "
                "of the four clone scalings lambda_i,lambda_i^-1 preserving "
                "the four anchors; setting them to one loses no orbit."),
            "support6_route": (
                "Every coefficient-compatible normalized branch has H=4 "
                "and literal (X,C,Q) signature in the frozen 24-record B4 "
                "orbit, so the fixed-left arbitrary-mate unit applies."),
        },
        "size12_three_colour_alignment_census": {
            "labelled_triples": len(small_supports)**3,
            "unique_triangular_minor_rank_histogram": dict(sorted(
                small_triple_ranks.items())),
            "full_rank_nonaligned": small_triple_ranks[12],
            "deficient_aligned": len(small_triple_deficient),
            "deficient_iff_all_three_supports_equal": True,
            "aligned_route": (
                "Every aligned support has six exact Laurent branches per "
                "colour, all B4/gauge-equivalent to frozen support6; any "
                "ordered pair is excluded by its arbitrary-mate unit."),
        },
        "diagonal_three_colour_structural_scan": {
            "scope": "G0=G1=G2 support; exact support matching only",
            "rank_histogram": dict(sorted(diagonal_ranks.items())),
            "deficient": deficient_diagonal,
        },
        "simultaneous_three_colour_structural_scan": {
            "scope": (
                "all inclusion-minimal G0,G1 supports modulo the stabilizer "
                "of the unique size-12 fixed-tail orbit for G2"),
            "G2_size_ge_13_closed_by_611": (
                args.rank_scan in ("diagonal", "joint")
                and diagonal_ranks.get(12, 0) == 1216),
            "simultaneous_orbit_representatives": joint_representatives,
            "rank_histogram": dict(sorted(joint_ranks.items())),
            "rank_kind": (
                "unique triangular structural minor; its determinant is "
                "the product of the twelve displayed diagonal entries"),
            "deficient_count": len(joint_deficient),
            "deficient": joint_deficient,
            "structural_witness_pattern_count": len(joint_witness_counts),
            "structural_witness_pattern_histogram": dict(sorted(Counter(
                joint_witness_counts.values()).items())),
            "structural_matching_ledger_sha256": (
                joint_ledger_hasher.hexdigest() if joint_representatives else None),
        },
        "support6_route": {
            "existing_result_sha256": support6["result_sha256"],
            "guard": "fires only after literal (X,C,Q,H) orbit match",
        },
        "single_cofactor_route": {
            "minimal_prime_count": primes["minimal_primes"]["count"],
            "site_orbit_count": primes["site_stabilizer_quotient"]["orbit_count"],
            "packet_survivors": support_filter[
                "packet_survivor_orbit_count_before_Dhat"],
            "localized_survivors": support_filter[
                "survivor_orbit_count_on_declared_chart"],
        },
        "terminal_tail_boundary_theorem": (
            "On the anchor-normalized diagonal packet every support factor "
            "face is closed: h-faces by the frozen exact monomial-prime "
            "chain, same-block g-faces by anchor localization, nonaligned "
            "cross-edge faces by a unique triangular literal source minor, "
            "and aligned size-12 faces by the support6 arbitrary-mate unit. "
            "Thus the chartwise tail-rank recursion has no survivor."),
        "remaining_global_work": (
            "No tail-response divisor remains on this diagonal chart. The "
            "remaining proof obligation is the global carrier/idempotent "
            "lift that transports the completed chart theorem to the full "
            "conjecture."),
        "scope_guard": (
            "A triangular witness gives a literal product determinant on "
            "the open where its displayed edge monomials and residual-tail "
            "cofactors are nonzero. Vanishing cofactor factors route to the "
            "frozen h_residual_tail boundary; no cancellation-generic rank "
            "or coefficient-existence inference is used."),
        "source_hashes": {
            "nonmonomial": file_hash(NONMONOMIAL),
            "single_cofactor": file_hash(SINGLE),
            "single_boundary_primes": file_hash(PRIMES),
            "prime_support_filter": file_hash(FILTER),
            "support6": file_hash(SUPPORT6),
        },
    }
    result["logical_sha256"] = logical_hash(result)
    if args.write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("accepted/minimal/fixed-tail/B4:", len(accepted), len(minima),
          len(fixed_orbits), len(b4_orbits))
    print("minimal sizes:", Counter(mask.bit_count() for mask in minima))
    print("diagonal structural ranks:", diagonal_ranks)
    print("deficient diagonal:", len(deficient_diagonal))
    print("joint representatives/ranks/deficient:", joint_representatives,
          joint_ranks, len(joint_deficient))
    print("logical sha256:", result["logical_sha256"])


if __name__ == "__main__":
    main()
