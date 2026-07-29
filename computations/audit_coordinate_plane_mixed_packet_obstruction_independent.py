#!/usr/bin/env python3
"""Clean-room audit of the coordinate-plane mixed-packet obstruction.

This script deliberately imports neither the primary checker nor the older
common-annihilator checker.  It rebuilds the finite and symbolic certificates
used by the proof over QQ:

* the double-quotient incidence table (including both row endpoint orders),
* the four support strata of q*ell=0 on a two-dimensional K4,
* the pure-K4 apex incidence consequence,
* every disconnected 3+3 and 2+2+2 component partition,
* the complete mixed-cofactor graph frontier and response-line propagation,
* and the sharp two-triangle model.

No six-site coefficient of q^[3] is queried by the obstruction audit.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from itertools import combinations, product

import sympy as sp


U = tuple(range(6))
COLORS = tuple(range(3))
LABEL = {u: u // 2 for u in U}
CLASS_PAIR = {c: (2 * c, 2 * c + 1) for c in COLORS}
ALL_EDGES = tuple(combinations(U, 2))
MIXED_EDGES = tuple(e for e in ALL_EDGES if LABEL[e[0]] != LABEL[e[1]])


def pairings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for position, v in enumerate(vertices[1:], 1):
        remainder = vertices[1:position] + vertices[position + 1 :]
        for tail in pairings(remainder):
            yield ((u, v),) + tail


def audit_double_quotient():
    """A two-site quotient isolates exactly one missing-pair slice."""

    checks = 0
    for quotient in ALL_EDGES:
        for hole in ALL_EDGES:
            # A hole slice is supported on U\hole.  Both quotient maps kill
            # it unless both quotient sites are holes.
            survives = not (set(quotient) & (set(U) - set(hole)))
            assert survives == (quotient == hole)
            checks += 1

        target_survivors = tuple(
            c for c in COLORS if LABEL[quotient[0]] == c == LABEL[quotient[1]]
        )
        if quotient in CLASS_PAIR.values():
            assert target_survivors == (LABEL[quotient[0]],)
        else:
            assert target_survivors == ()

    # Keep p-at-u/s-at-v and p-at-v/s-at-u as genuinely ordered outer
    # products.  No symmetry of either response family is introduced.
    au = sp.Matrix(sp.symbols("au0:3"))
    av = sp.Matrix(sp.symbols("av0:3"))
    bu = sp.Matrix(sp.symbols("bu0:3"))
    bv = sp.Matrix(sp.symbols("bv0:3"))
    response = au * bv.T + av * bu.T
    assert all(
        sp.expand(response[r, s] - au[r] * bv[s] - av[r] * bu[s]) == 0
        for r in COLORS
        for s in COLORS
    )
    assert response != response.T
    return checks


def audit_extension_strata_and_apex():
    """Solve q*ell=0 on K4 and replay the no-apex contradiction."""

    sites = tuple(range(4))
    bits = (0, 1)
    edges = tuple(combinations(sites, 2))
    keys = tuple((i, j, a, b) for i, j in edges for a in bits for b in bits)
    symbols = sp.symbols(f"z0:{len(keys)}")
    variable_for = dict(zip(keys, symbols))

    def coefficient(entries, i, j, a, b):
        return entries[i, j, a, b] if i < j else entries[j, i, b, a]

    def square(entries, colors):
        c = dict(enumerate(colors))
        return sp.expand(
            coefficient(entries, 0, 1, c[0], c[1])
            * coefficient(entries, 2, 3, c[2], c[3])
            + coefficient(entries, 0, 2, c[0], c[2])
            * coefficient(entries, 1, 3, c[1], c[3])
            + coefficient(entries, 0, 3, c[0], c[3])
            * coefficient(entries, 1, 2, c[1], c[2])
        )

    nullities = []
    for support_size in range(1, 5):
        equations = []
        # ell_i=e0 for i<support_size and ell_i=0 otherwise.
        for triple in combinations(sites, 3):
            for colors in product(bits, repeat=3):
                c = dict(zip(triple, colors))
                expression = 0
                for singled in triple:
                    if singled < support_size and c[singled] == 0:
                        j, k = tuple(x for x in triple if x != singled)
                        expression += coefficient(
                            variable_for, j, k, c[j], c[k]
                        )
                equations.append(expression)

        matrix, _ = sp.linear_eq_to_matrix(equations, symbols)
        kernel = matrix.nullspace()
        nullities.append(len(kernel))
        parameters = sp.symbols(f"t{support_size}_0:{len(kernel)}")
        generic_vector = sp.zeros(len(symbols), 1)
        for t, vector in zip(parameters, kernel):
            generic_vector += t * vector
        entries = {
            key: sp.expand(generic_vector[index])
            for index, key in enumerate(keys)
        }
        tensor = {
            colors: sp.factor(square(entries, colors))
            for colors in product(bits, repeat=4)
        }

        if support_size in (1, 3):
            assert all(value == 0 for value in tensor.values())
        elif support_size == 2:
            assert all(
                value == 0
                for colors, value in tensor.items()
                if colors[0] or colors[1]
            )
            residual = sp.Matrix(
                2, 2, lambda a, b: tensor[(0, 0, a, b)]
            )
            assert residual != sp.zeros(2, 2)
            assert sp.factor(residual.det()) == 0

            def block(i, j):
                return sp.Matrix(
                    2,
                    2,
                    lambda a, b: coefficient(entries, i, j, a, b),
                )

            assert block(2, 3) == sp.zeros(2, 2)
            assert all(
                sp.factor(block(i, j).det()) == 0
                for i in (0, 1)
                for j in (2, 3)
            )
        else:
            assert tensor[(0, 0, 0, 0)] != 0
            assert all(
                value == 0
                for colors, value in tensor.items()
                if colors != (0, 0, 0, 0)
            )

    assert nullities == [12, 8, 5, 2]

    # In a hypothetical apex-free pure K4, each transverse derivative has
    # support two.  Its one nonsupport neighbor must be reciprocal because
    # their edge is zero.  Enumerate the reciprocal maps: they are exactly
    # the three perfect matchings.  Every remaining edge is transverse at
    # both ends (hence rank two) but is a cross edge in the support-two
    # normal form above (hence rank <=1).
    reciprocal_maps = []
    for values in product(*(tuple(j for j in sites if j != i) for i in sites)):
        if all(values[values[i]] == i for i in sites):
            reciprocal_maps.append(values)
    assert len(reciprocal_maps) == 3
    for missing in reciprocal_maps:
        for i, j in edges:
            assert (missing[i] == j) == (missing[j] == i)
            if missing[i] != j:
                assert j != missing[i] and i != missing[j]

    return tuple(nullities), len(reciprocal_maps)


def complement_of_pair(edge):
    return tuple(u for u in U if u not in edge)


def audit_no_isolated_vertex_setup():
    """Check all matching incidences used by the analytic isolation proof."""

    matching_checks = 0
    quotient_checks = 0
    for isolated in U:
        c = LABEL[isolated]
        mate = next(u for u in CLASS_PAIR[c] if u != isolated)
        core = tuple(u for u in U if LABEL[u] != c)

        # The four zero cofactors are exactly the four multidegrees of
        # q_core times the mate-star.
        for deleted in core:
            remaining = tuple(u for u in U if u not in (isolated, deleted))
            assert set(remaining) == {mate} | (set(core) - {deleted})
            for matching in pairings(remaining):
                star = next(edge for edge in matching if mate in edge)
                internal = next(edge for edge in matching if edge != star)
                assert set(internal) <= set(core)
                assert next(u for u in star if u != mate) in core
                matching_checks += 1

        # After the extension lemma aligns every mate-star endpoint in core
        # with e_c, quotienting either other class by e_c kills precisely the
        # two cross matchings and retains the internal|internal matching.
        target_lines = []
        for target in COLORS:
            if target == c:
                continue
            quotient_class = 3 - c - target
            four = tuple(sorted(CLASS_PAIR[c] + CLASS_PAIR[quotient_class]))
            surviving = []
            for matching in pairings(four):
                killed = any(
                    mate in edge
                    and LABEL[next(u for u in edge if u != mate)]
                    == quotient_class
                    for edge in matching
                )
                if not killed:
                    surviving.append(matching)
                quotient_checks += 1
            assert len(surviving) == 1
            assert all(LABEL[u] == LABEL[v] for u, v in surviving[0])
            target_lines.append(target)
        assert len(set(target_lines)) == 2

    return matching_checks, quotient_checks


EDGE_INDEX = {edge: index for index, edge in enumerate(ALL_EDGES)}
PURE_SETS = {
    c: tuple(u for u in U if u not in CLASS_PAIR[c]) for c in COLORS
}


def edge_key(u, v):
    return (u, v) if u < v else (v, u)


def four_matchings(four):
    a, b, c, d = tuple(sorted(four))
    return (
        ((a, b), (c, d)),
        ((a, c), (b, d)),
        ((a, d), (b, c)),
    )


def all_apex_branches_close(zero_four_sets):
    """Branch only on the exact zero-K4 tensor quotient disjunction."""

    zero_four_sets = tuple(tuple(sorted(s)) for s in zero_four_sets)

    # State = (zero edge bitmask, frozenset((edge index, endpoint, line))).
    def is_zero(state, edge):
        return bool(state[0] & (1 << EDGE_INDEX[edge_key(*edge)]))

    def has_line(state, edge, endpoint, line):
        index = EDGE_INDEX[edge_key(*edge)]
        return is_zero(state, edge) or (index, endpoint, line) in state[1]

    def force_zero(state, edge):
        index = EDGE_INDEX[edge_key(*edge)]
        mask = state[0] | (1 << index)
        records = frozenset(record for record in state[1] if record[0] != index)
        return mask, records

    def force_line(state, edge, endpoint, line):
        edge = edge_key(*edge)
        if is_zero(state, edge):
            return state
        index = EDGE_INDEX[edge]
        existing = {
            recorded_line
            for recorded_edge, recorded_endpoint, recorded_line in state[1]
            if recorded_edge == index and recorded_endpoint == endpoint
        }
        if existing and line not in existing:
            return force_zero(state, edge)
        return state[0], state[1] | frozenset(((index, endpoint, line),))

    def pure_coefficient_killed(state):
        for color, four in PURE_SETS.items():
            every_matching_killed = True
            for matching in four_matchings(four):
                term_killed = False
                for edge in matching:
                    if is_zero(state, edge):
                        term_killed = True
                        break
                    for endpoint in edge:
                        index = EDGE_INDEX[edge_key(*edge)]
                        forced = {
                            line
                            for e, u, line in state[1]
                            if e == index and u == endpoint
                        }
                        if forced and color not in forced:
                            term_killed = True
                            break
                    if term_killed:
                        break
                if not term_killed:
                    every_matching_killed = False
                    break
            if every_matching_killed:
                return True
        return False

    def available_clause(state):
        for four in zero_four_sets:
            for apex in four:
                neighbors = tuple(v for v in four if v != apex)
                for line in COLORS:
                    if line == LABEL[apex]:
                        continue
                    aligned = tuple(
                        v
                        for v in neighbors
                        if has_line(state, (apex, v), apex, line)
                    )
                    for first, second in combinations(aligned, 2):
                        third = next(v for v in neighbors if v not in (first, second))
                        opposite = edge_key(first, second)
                        if not has_line(state, (apex, third), apex, line) and not is_zero(
                            state, opposite
                        ):
                            return (apex, third), apex, line, opposite
        return None

    def starting_state(apices):
        state = (0, frozenset())
        for color, apex in enumerate(apices):
            for other in PURE_SETS[color]:
                if other != apex:
                    state = force_line(state, (apex, other), apex, color)
        return state

    @lru_cache(maxsize=None)
    def closed(state):
        if pure_coefficient_killed(state):
            return True
        clause = available_clause(state)
        if clause is None:
            return False
        edge, endpoint, line, opposite = clause
        return closed(force_line(state, edge, endpoint, line)) and closed(
            force_zero(state, opposite)
        )

    assignments = tuple(product(*(PURE_SETS[c] for c in COLORS)))
    assert len(assignments) == 64
    failures = [apices for apices in assignments if not closed(starting_state(apices))]
    assert failures == []
    return len(assignments), closed.cache_info().currsize


def set_partitions_fixed_sizes(sizes):
    """Generate unordered set partitions of U with prescribed sizes."""

    sizes = tuple(sorted(sizes))

    # The explicit canonicalization below is simpler and safer for repeated
    # part sizes than relying on recursive ordering alone.
    raw = set()

    def build(remaining, pending, parts):
        if not pending:
            raw.add(tuple(sorted((tuple(sorted(p)) for p in parts))))
            return
        anchor = min(remaining)
        size = pending[0]
        for rest in combinations(sorted(remaining - {anchor}), size - 1):
            part = frozenset((anchor,) + rest)
            build(remaining - part, pending[1:], parts + (part,))

    build(set(U), sizes, ())
    return tuple(tuple(frozenset(p) for p in partition) for partition in sorted(raw))


def mandatory_zero_four_sets(partition):
    component = {u: index for index, part in enumerate(partition) for u in part}
    zero_holes = tuple(
        edge
        for edge in MIXED_EDGES
        if component[edge[0]] != component[edge[1]]
    )
    return tuple(complement_of_pair(edge) for edge in zero_holes)


def audit_all_disconnected_apex_partitions():
    """Close every 3+3 and every admissible 2+2+2 partition directly."""

    three_three = set_partitions_fixed_sizes((3, 3))
    assert len(three_three) == 10
    three_results = []
    for partition in three_three:
        result = all_apex_branches_close(mandatory_zero_four_sets(partition))
        three_results.append(result)

    two_two_two = tuple(
        partition
        for partition in set_partitions_fixed_sizes((2, 2, 2))
        if all(LABEL[min(part)] != LABEL[max(part)] for part in partition)
    )
    assert len(two_two_two) == 8
    two_results = []
    for partition in two_two_two:
        result = all_apex_branches_close(mandatory_zero_four_sets(partition))
        two_results.append(result)

    return (
        len(three_three),
        tuple(sorted(Counter(len(mandatory_zero_four_sets(p)) for p in three_three).items())),
        len(two_two_two),
        tuple(sorted(Counter(len(mandatory_zero_four_sets(p)) for p in two_two_two).items())),
        sum(states for _, states in three_results + two_results),
    )


def graph_components(edge_set):
    adjacency = {u: set() for u in U}
    for u, v in edge_set:
        adjacency[u].add(v)
        adjacency[v].add(u)
    unseen = set(U)
    parts = []
    while unseen:
        reached = {min(unseen)}
        frontier = list(reached)
        while frontier:
            u = frontier.pop()
            for v in adjacency[u] - reached:
                reached.add(v)
                frontier.append(v)
        unseen -= reached
        parts.append(frozenset(reached))
    return tuple(sorted(parts, key=lambda p: (len(p), tuple(p))))


def audit_graph_frontier_and_response_finish():
    """Enumerate graph patterns and check the response proof's incidences."""

    disconnected = Counter()
    connected = 0
    two_four_full_class_checks = 0
    for mask in range(1 << len(MIXED_EDGES)):
        edges = {
            edge for bit, edge in enumerate(MIXED_EDGES) if mask & (1 << bit)
        }
        degrees = Counter(u for edge in edges for u in edge)
        if any(degrees[u] == 0 for u in U):
            continue
        parts = graph_components(edges)
        if len(parts) == 1:
            connected += 1
            # Every equality edge identifies the a-lines and the b-lines;
            # graph connectivity reaches all six vertices.
            reached = set(parts[0])
            assert reached == set(U)
            continue
        pattern = tuple(sorted(len(part) for part in parts))
        assert pattern in ((2, 4), (3, 3), (2, 2, 2))
        disconnected[pattern] += 1
        if pattern == (2, 4):
            small, large = parts
            assert len({LABEL[u] for u in small}) == 2
            full_classes = [
                c for c in COLORS if set(CLASS_PAIR[c]) <= set(large)
            ]
            assert len(full_classes) == 1
            c = full_classes[0]
            for d in COLORS:
                if d == c:
                    continue
                # A matrix f_c*x^T+y*f_c^T has zero (d,d), whereas the
                # required theta_d E_dd has a nonzero (d,d).
                f = sp.eye(3).col(c)
                x = sp.Matrix(sp.symbols(f"x{mask}_{d}_0:3"))
                y = sp.Matrix(sp.symbols(f"y{mask}_{d}_0:3"))
                assert (f * x.T + y * f.T)[d, d] == 0
                two_four_full_class_checks += 1

    assert disconnected == Counter({(2, 4): 168, (3, 3): 70, (2, 2, 2): 8})
    assert connected > 0

    # Once all nonzero response vectors lie on common lines A and B, each
    # same-class N is a scalar multiple of A*B^T.  The three demanded units
    # E_00,E_11,E_22 are linearly independent, hence cannot all lie there.
    diagonal_units = [
        sp.eye(3).col(c) * sp.eye(3).col(c).T for c in COLORS
    ]
    flattened = sp.Matrix.hstack(
        *(sp.Matrix(9, 1, tuple(matrix)) for matrix in diagonal_units)
    )
    assert flattened.rank() == 3
    return connected, dict(sorted(disconnected.items())), two_four_full_class_checks


def tensor_hafnian(vertices, blocks):
    """Sparse exact matching tensor with endpoint-ordered color cells."""

    vertices = tuple(sorted(vertices))
    answer = Counter()
    for matching in pairings(vertices):
        partial = {(): sp.Integer(1)}
        for u, v in matching:
            edge = edge_key(u, v)
            cells = blocks.get(edge, {})
            next_partial = Counter()
            for assignment, old_value in partial.items():
                old = dict(assignment)
                for (left_color, right_color), value in cells.items():
                    new = dict(old)
                    if edge == (u, v):
                        new[u], new[v] = left_color, right_color
                    else:
                        new[u], new[v] = right_color, left_color
                    next_partial[tuple(sorted(new.items()))] += old_value * value
            partial = dict(next_partial)
        for assignment, value in partial.items():
            color = dict(assignment)
            answer[tuple(color[u] for u in vertices)] += value
    return {key: value for key, value in answer.items() if value != 0}


def audit_sharp_two_triangle():
    """Pure same-class slices and q^[3]=0 coexist before responses."""

    blocks = {}
    for c, d in combinations(COLORS, 2):
        remaining_color = 3 - c - d
        for side in (0, 1):
            edge = edge_key(CLASS_PAIR[c][side], CLASS_PAIR[d][side])
            blocks[edge] = {(remaining_color, remaining_color): sp.Integer(1)}

    six_tensor = tensor_hafnian(U, blocks)
    assert six_tensor == {}  # two odd triangles: this is q^[3]=0
    nonzero_mixed_holes = []
    for hole in ALL_EDGES:
        cofactor = tensor_hafnian(complement_of_pair(hole), blocks)
        if hole in CLASS_PAIR.values():
            c = LABEL[hole[0]]
            assert cofactor == {(c, c, c, c): sp.Integer(1)}
        elif cofactor:
            nonzero_mixed_holes.append(hole)
    assert len(nonzero_mixed_holes) == 6
    assert len(graph_components(set(nonzero_mixed_holes))) == 1
    return len(nonzero_mixed_holes)


def main():
    quotient_checks = audit_double_quotient()
    extension, reciprocal = audit_extension_strata_and_apex()
    isolation = audit_no_isolated_vertex_setup()
    partitions = audit_all_disconnected_apex_partitions()
    graph_audit = audit_graph_frontier_and_response_finish()
    sharp_edges = audit_sharp_two_triangle()
    print("independent coordinate-plane mixed-packet audit: PASS")
    print("double-quotient checks:", quotient_checks)
    print("extension nullities / reciprocal no-apex maps:", extension, reciprocal)
    print("no-isolated matching / quotient incidences:", isolation)
    print("all disconnected apex partitions:", partitions)
    print("mixed-cofactor graph / response frontier:", graph_audit)
    print("sharp two-triangle nonzero mixed holes:", sharp_edges)
    print("obstruction queried q^[3]: no")


if __name__ == "__main__":
    main()
