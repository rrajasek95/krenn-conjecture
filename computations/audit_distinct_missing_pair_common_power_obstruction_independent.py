#!/usr/bin/env python3
"""Independent finite audit for the distinct-missing-pair obstruction.

This script deliberately imports no project module and does not use the
primary checker.  It audits the finite bookkeeping surrounding the hand
proof:

* the five isomorphism types of three distinct edges on six vertices;
* separation of the three full-support colour-word spaces in q q^[2];
* the complete Boolean support propagation in the P4 case;
* the K3 common-spoke-support lemma and its odd-characteristic scalar
  contradictions over two sample prime fields;
* formal, coefficient-by-coefficient syzygies behind the star elimination;
* the final two-colour marking argument in the all-zero star branch.

The arbitrary-tensor crossing and rank arguments remain mathematical proofs;
finite support tests below are corroboration, not substitutes for them.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, product


VERTICES = tuple(range(6))
EDGES = tuple(combinations(VERTICES, 2))


def connected_degree_signature(edges: tuple[tuple[int, int], ...]):
    """Classify through connected components, not a canned graph table."""
    adjacency = {v: set() for v in VERTICES}
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    unseen = {v for v in VERTICES if adjacency[v]}
    components = []
    while unseen:
        seed = min(unseen)
        stack = [seed]
        component = set()
        while stack:
            v = stack.pop()
            if v in component:
                continue
            component.add(v)
            stack.extend(adjacency[v] - component)
        unseen -= component
        components.append(tuple(sorted(len(adjacency[v]) for v in component)))
    return tuple(sorted(components))


GRAPH_NAMES = {
    ((1, 1), (1, 1), (1, 1)): "3K2",
    ((1, 1), (1, 1, 2)): "P3+K2",
    ((1, 1, 2, 2),): "P4",
    ((1, 1, 1, 3),): "K1,3",
    ((2, 2, 2),): "K3",
}


def graph_and_word_audit():
    counts = Counter()
    for triple in combinations(EDGES, 3):
        signature = connected_degree_signature(triple)
        assert signature in GRAPH_NAMES, (triple, signature)
        counts[GRAPH_NAMES[signature]] += 1

        # The i-th term has arbitrary colours on P_i and fixed colour i
        # everywhere else.  Reconstruct all nine possible full words.
        word_spaces = []
        for colour, omitted_pair in enumerate(triple):
            words = set()
            for endpoint_colours in product(range(3), repeat=2):
                word = [colour] * 6
                for site, endpoint_colour in zip(omitted_pair, endpoint_colours):
                    word[site] = endpoint_colour
                words.add(tuple(word))
            assert len(words) == 9
            word_spaces.append(words)
        assert all(
            word_spaces[i].isdisjoint(word_spaces[j])
            for i, j in combinations(range(3), 2)
        )

    expected = Counter({"P3+K2": 180, "P4": 180, "K1,3": 60,
                        "K3": 20, "3K2": 15})
    assert counts == expected
    assert sum(counts.values()) == 455
    return dict(counts)


def perfect_matchings(sites: tuple[int, ...]):
    """Generate unordered perfect matchings recursively."""
    if not sites:
        return ((),)
    first = sites[0]
    answer = []
    for position in range(1, len(sites)):
        mate = sites[position]
        rest = sites[1:position] + sites[position + 1:]
        for tail in perfect_matchings(rest):
            answer.append((((min(first, mate), max(first, mate))),) + tail)
    return tuple(answer)


def p4_support_audit():
    # a,b,c,d,e,f = 0,...,5; targets are complements of ab, bc, cd.
    forbidden_edges = {(0, 1), (1, 2), (2, 3)}
    targets = {
        tuple(sorted(set(VERTICES) - set(pair))) for pair in forbidden_edges
    }
    edge_position = {edge: position for position, edge in enumerate(EDGES)}
    survivors = []
    for bits in range(1 << len(EDGES)):
        present = lambda edge: bool(bits & (1 << edge_position[edge]))
        if any(present(edge) for edge in forbidden_edges):
            continue
        viable = True
        for four_set in combinations(VERTICES, 4):
            live_terms = sum(
                all(present(edge) for edge in matching)
                for matching in perfect_matchings(four_set)
            )
            if four_set in targets and live_terms == 0:
                viable = False
                break
            if four_set not in targets and live_terms == 1:
                viable = False
                break
        if viable:
            survivors.append(bits)

    assert len(survivors) == 2
    core_edges = tuple(combinations(range(4), 2))
    spoke_edges = tuple((x, y) for x in range(4) for y in (4, 5))
    for bits in survivors:
        present = lambda edge: bool(bits & (1 << edge_position[edge]))
        assert not any(present(edge) for edge in core_edges)
        assert all(present(edge) for edge in spoke_edges)
    assert {
        bool(bits & (1 << edge_position[(4, 5)])) for bits in survivors
    } == {False, True}

    # E-only, G-only, or both.  Zero brackets are ac, bc, bd; target
    # brackets are ab, ad, cd.
    states = ((1, 0), (0, 1), (1, 1))
    zero_edges = ((0, 2), (1, 2), (1, 3))
    target_edges = ((0, 1), (0, 3), (2, 3))
    surviving_states = []
    for rows in product(states, repeat=4):
        if any(
            not (rows[x][0] * rows[y][1] or rows[x][1] * rows[y][0])
            for x, y in target_edges
        ):
            continue
        if any(
            rows[x][0] * rows[y][1] != rows[x][1] * rows[y][0]
            for x, y in zero_edges
        ):
            continue
        surviving_states.append(rows)
    assert surviving_states == [((1, 1),) * 4]
    return len(survivors), len(surviving_states)


def k3_support_and_scalar_audit():
    columns = frozenset(range(3))
    nonempty = tuple(
        frozenset(subset)
        for size in range(1, 4)
        for subset in combinations(columns, size)
    )
    allowed_pairs = []
    for left, right in product(nonempty, repeat=2):
        condition = all(
            ((u in left and v in right) == (v in left and u in right))
            for u, v in combinations(columns, 2)
        )
        if condition:
            allowed_pairs.append((left, right))
    assert len(allowed_pairs) == 7
    assert all(left == right for left, right in allowed_pairs)

    # Independent finite-field corroboration of the scalar arguments.  For
    # three supported columns even two rows cannot obey all crossings; for
    # two columns no three full-support rows are pairwise hyperbolic-orthogonal.
    for prime in (3, 5):
        full_three = tuple(product(range(1, prime), repeat=3))
        assert not any(
            all(
                (x[u] * y[v] + x[v] * y[u]) % prime == 0
                for u, v in combinations(range(3), 2)
            )
            for x, y in product(full_three, repeat=2)
        )

        full_two = tuple(product(range(1, prime), repeat=2))
        orthogonal = lambda x, y: (x[0] * y[1] + x[1] * y[0]) % prime == 0
        assert not any(
            orthogonal(x, y) and orthogonal(x, z) and orthogonal(y, z)
            for x, y, z in product(full_two, repeat=3)
        )
    return len(allowed_pairs)


# A tiny formal commutative-expression engine.  A monomial is a sorted tuple
# of atom names and an expression is an integer linear combination of them.
def atom(*names: str):
    return {tuple(sorted(names)): 1}


def add(*expressions):
    result = Counter()
    for expression in expressions:
        result.update(expression)
    return {monomial: coefficient for monomial, coefficient in result.items()
            if coefficient}


def scale(coefficient: int, expression):
    return {monomial: coefficient * value for monomial, value in expression.items()
            if coefficient * value}


def multiply_atom(expression, name: str):
    return {
        tuple(sorted(monomial + (name,))): coefficient
        for monomial, coefficient in expression.items()
    }


def star_syzygy_audit():
    # Formal versions of (21)--(22); X*Y denotes an outer product and H a
    # matrix atom.  These identities hold entrywise for arbitrary vectors.
    lx = add(atom("A", "Xb"), atom("B", "Xc"), atom("C", "Xd"))
    ly = add(atom("A", "Yb"), atom("B", "Yc"), atom("C", "Yd"))
    m = add(atom("Xc", "Yd"), atom("Xd", "Yc"))
    t0 = add(atom("A", "H"), m)
    t1 = add(atom("B", "H"), atom("Xb", "Yd"), atom("Xd", "Yb"))
    t2 = add(atom("C", "H"), atom("Xb", "Yc"), atom("Xc", "Yb"))

    first_left = add(
        multiply_atom(t0, "B"),
        scale(-1, multiply_atom(t1, "A")),
        scale(-2, multiply_atom(m, "B")),
        scale(-2, atom("C", "Xd", "Yd")),
    )
    first_certificate = add(
        scale(-1, multiply_atom(lx, "Yd")),
        scale(-1, multiply_atom(ly, "Xd")),
    )
    assert first_left == first_certificate

    second_left = add(
        multiply_atom(t0, "C"),
        scale(-1, multiply_atom(t2, "A")),
        scale(-2, multiply_atom(m, "C")),
        scale(-2, atom("B", "Xc", "Yc")),
    )
    second_certificate = add(
        scale(-1, multiply_atom(lx, "Yc")),
        scale(-1, multiply_atom(ly, "Xc")),
    )
    assert second_left == second_certificate

    # A=0 branch, with Lx0=B Xc+C Xd and Ly0=B Yc+C Yd.
    lx0 = add(atom("B", "Xc"), atom("C", "Xd"))
    ly0 = add(atom("B", "Yc"), atom("C", "Yd"))
    n = add(atom("Xb", "Yc"), atom("Xc", "Yb"))
    one_zero_left = add(
        multiply_atom(t2, "B"),
        scale(-1, multiply_atom(t1, "C")),
        scale(-2, multiply_atom(n, "B")),
    )
    one_zero_certificate = add(
        scale(-1, multiply_atom(ly0, "Xb")),
        scale(-1, multiply_atom(lx0, "Yb")),
    )
    assert one_zero_left == one_zero_certificate

    # The all-zero branch needs only the fact that every two-colouring of a
    # triangle repeats a colour on two incident edges.
    triangle = ((0, 1), (0, 2), (1, 2))
    for marks in product(("column", "row"), repeat=3):
        assert any(
            marks[i] == marks[j] and set(triangle[i]) & set(triangle[j])
            for i, j in combinations(range(3), 2)
        )

    # Exhaust the zero/nonzero patterns of A,B,C and make the branch split
    # explicit: 1 all-nonzero, 3 one-zero, 3 two-zero, 1 all-zero.
    branch_counts = Counter(sum(pattern) for pattern in product((0, 1), repeat=3))
    assert branch_counts == Counter({0: 1, 1: 3, 2: 3, 3: 1})
    return 3, dict(branch_counts)


def main():
    graph_counts = graph_and_word_audit()
    p4 = p4_support_audit()
    k3 = k3_support_and_scalar_audit()
    syzygies, star_branches = star_syzygy_audit()
    print("independent distinct-missing-pair audit: PASS")
    print("unlabelled support-graph census:", graph_counts)
    print("P4 support/state survivors:", p4)
    print("K3 allowed support pairs:", k3, "(equal subsets only)")
    print("star formal syzygies checked:", syzygies)
    print("star scalar nonzero-count branches:", star_branches)
    print("scope: finite bookkeeping plus exact syzygies; tensor arguments audited by hand")


if __name__ == "__main__":
    main()
