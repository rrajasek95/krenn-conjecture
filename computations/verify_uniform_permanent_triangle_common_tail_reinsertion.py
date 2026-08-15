#!/usr/bin/env python3
"""Uniform common-tail and terminal-ear audit for permanent triangles.

This checker verifies three exact layers:

1. the three-row Laurent identity remains valid with a symbolic arbitrary
   common cofactor tail;
2. restriction/reinsertion by a terminal odd ear has exactly two matching
   channels, so a row-independent rank-one channel factor preserves the
   common tail; and
3. a labelled tight C6 cut is a smallest counterguard to deriving that
   rank-one factor from tightness alone.
"""

from __future__ import annotations

from collections import Counter
import importlib.util
from itertools import combinations
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_local(name, filename):
    path = HERE / filename
    specification = importlib.util.spec_from_file_location(name, path)
    require(specification is not None
            and specification.loader is not None, path)
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


POLY = load_local(
    "n8_permanent_triangle_polynomial_primitives",
    "audit_n8_support28_cube_cut_permanent_triangle_unit_independent.py",
)


def edge(left, right):
    return tuple(sorted((left, right)))


def perfect_matchings(vertices, allowed_edges=None):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        selected = edge(first, second)
        if allowed_edges is not None and selected not in allowed_edges:
            continue
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest, allowed_edges):
            yield (selected,) + tail


def formal_common_tail_identity():
    a, b, c, d, e, f = (f"local_{name}" for name in "abcdef")
    u, v, w = (f"pair_{name}" for name in "uvw")
    tail = "arbitrary_common_tail"
    first = POLY.multiply(
        POLY.monomial(u, tail),
        POLY.add(POLY.monomial(a, e), POLY.monomial(b, d)),
    )
    second = POLY.multiply(
        POLY.monomial(v, tail),
        POLY.add(POLY.monomial(a, f), POLY.monomial(c, d)),
    )
    third = POLY.multiply(
        POLY.monomial(w, tail),
        POLY.add(POLY.monomial(b, f), POLY.monomial(c, e)),
    )
    lhs = POLY.add(
        POLY.multiply(POLY.monomial(c, v, w), first),
        POLY.multiply(POLY.monomial(b, u, w), second),
        POLY.scale(-1, POLY.multiply(POLY.monomial(a, u, v), third)),
    )
    rhs = POLY.scale(2, POLY.monomial(b, c, d, u, v, w, tail))
    require(lhs == rhs and len(rhs) == 1, (lhs, rhs))

    # The terminal-ear update has two channels.  Treating their cofactors as
    # independent symbols shows that it merely substitutes a new arbitrary
    # common tail A*T0+B*T2 into the already checked identity.
    updated_tail = POLY.add(
        POLY.monomial("ear_internal", "tail_state_0"),
        POLY.monomial("ear_through", "tail_state_2"),
    )
    updated_rows = tuple(POLY.multiply(row, updated_tail)
                         for row in (POLY.add(
                             POLY.monomial(u, a, e),
                             POLY.monomial(u, b, d)),
                             POLY.add(POLY.monomial(v, a, f),
                                      POLY.monomial(v, c, d)),
                             POLY.add(POLY.monomial(w, b, f),
                                      POLY.monomial(w, c, e))))
    updated_lhs = POLY.add(
        POLY.multiply(POLY.monomial(c, v, w), updated_rows[0]),
        POLY.multiply(POLY.monomial(b, u, w), updated_rows[1]),
        POLY.scale(-1, POLY.multiply(
            POLY.monomial(a, u, v), updated_rows[2])),
    )
    updated_rhs = POLY.multiply(
        POLY.scale(2, POLY.monomial(b, c, d, u, v, w)),
        updated_tail,
    )
    require(updated_lhs == updated_rhs, (updated_lhs, updated_rhs))
    return {
        "common_tail_identity_terms": (len(lhs), len(rhs)),
        "ear_tail_terms": len(updated_tail),
        "updated_rhs_terms": len(updated_rhs),
    }


def coefficient(vertices, word, support):
    answer = Counter()
    for matching in perfect_matchings(vertices):
        variables = []
        for endpoints in matching:
            left, right = endpoints
            if word[left] != word[right]:
                break
            key = (endpoints, word[left])
            if key not in support:
                break
            variables.append(support[key])
        else:
            answer[tuple(sorted(variables))] += 1
    return dict(answer)


def literal_nonmonomial_tail_reinsertion():
    """A 12-site cofactor face with a three-term arbitrary common tail."""
    local_support = {
        (endpoints, colour): POLY.variable(colour, endpoints)
        for endpoints, colours in POLY.SUPPORT.items()
        for colour in colours
    }
    tail_vertices = (8, 9, 10, 11)
    tail_support = {
        (endpoints, 2): f"tail2_{endpoints[0]}{endpoints[1]}"
        for endpoints in combinations(tail_vertices, 2)
    }
    support = {**local_support, **tail_support}
    tail_word = (2, 2, 2, 2)
    tail_word_global = (None,) * 8 + tail_word
    tail_coefficient = coefficient(
        tail_vertices, tail_word_global, tail_support
    )
    require(len(tail_coefficient) == 3, tail_coefficient)
    local_words = (
        (0, 0, 1, 1, 0, 0, 2, 2),
        (0, 0, 2, 1, 0, 1, 0, 2),
        (0, 0, 1, 1, 2, 0, 0, 2),
    )
    for local_word in local_words:
        global_word = local_word + tail_word
        local_coefficient = coefficient(range(8), local_word, local_support)
        global_coefficient = coefficient(range(12), global_word, support)
        require(global_coefficient == POLY.multiply(
            local_coefficient, tail_coefficient
        ), (local_word, global_coefficient, local_coefficient,
            tail_coefficient))
    return len(tail_coefficient), tuple(map(len, (
        coefficient(range(12), word + tail_word, support)
        for word in local_words
    )))


def terminal_ear_edges(outside_vertices, internal_count):
    require(internal_count >= 2 and internal_count % 2 == 0, internal_count)
    first_endpoint, second_endpoint = outside_vertices[:2]
    first_internal = max(outside_vertices) + 1
    internal = tuple(range(first_internal, first_internal + internal_count))
    path = (first_endpoint,) + internal + (second_endpoint,)
    return internal, tuple(edge(path[index], path[index + 1])
                           for index in range(len(path) - 1))


def terminal_ear_channel_census():
    """Exhaust all four-vertex outside graphs for ears of length 3,5,7."""
    outside = (0, 1, 2, 3)
    outside_edges = tuple(combinations(outside, 2))
    tested = 0
    for mask in range(1 << len(outside_edges)):
        old_edges = {edge(*endpoints)
                     for index, endpoints in enumerate(outside_edges)
                     if mask & (1 << index)}
        old_matchings = set(perfect_matchings(outside, old_edges))
        deleted_matchings = set(perfect_matchings((2, 3), old_edges))
        for internal_count in (2, 4, 6):
            internal, ear_edges = terminal_ear_edges(
                outside, internal_count
            )
            graph_edges = old_edges | set(ear_edges)
            full_vertices = outside + internal
            actual = set(perfect_matchings(full_vertices, graph_edges))

            internal_mode = tuple(edge(internal[index], internal[index + 1])
                                  for index in range(0, internal_count, 2))
            through_mode = (
                edge(0, internal[0]),
                *(edge(internal[index], internal[index + 1])
                  for index in range(1, internal_count - 1, 2)),
                edge(internal[-1], 1),
            )
            expected_internal = {
                tuple(sorted(matching + internal_mode))
                for matching in old_matchings
            }
            expected_through = {
                tuple(sorted(matching + through_mode))
                for matching in deleted_matchings
            }
            require(actual == expected_internal | expected_through,
                    (mask, internal_count, actual,
                     expected_internal, expected_through))
            require(not (expected_internal & expected_through),
                    (mask, internal_count))
            tested += 1
    require(tested == 64 * 3, tested)
    return tested


def tight_c6_counterguard():
    """Tightness with a rank-two boundary transfer and no common shore tail."""
    cycle_edges = {
        edge(0, 1), edge(1, 2), edge(2, 3),
        edge(3, 4), edge(4, 5), edge(5, 0),
    }
    matchings = tuple(perfect_matchings(range(6), cycle_edges))
    require(len(matchings) == 2, matchings)
    shore = {0, 1, 2}
    cut = {endpoints for endpoints in cycle_edges
           if (endpoints[0] in shore) != (endpoints[1] in shore)}
    require(cut == {edge(2, 3), edge(0, 5)}, cut)
    require(all(sum(endpoints in cut for endpoints in matching) == 1
                for matching in matchings), matchings)

    support = {}
    for endpoints in (edge(0, 1), edge(1, 2), edge(2, 3), edge(0, 5)):
        support[endpoints, 0] = f"c6_0_{endpoints[0]}{endpoints[1]}"
    for endpoints in (edge(3, 4), edge(4, 5)):
        for colour in (0, 1):
            support[endpoints, colour] = (
                f"c6_{colour}_{endpoints[0]}{endpoints[1]}"
            )

    words = (
        (0, 0, 0, 0, 1, 1),
        (0, 0, 0, 1, 1, 0),
        (0, 0, 0, 0, 0, 0),
    )
    rows = tuple(coefficient(range(6), word, support) for word in words)
    expected = (
        POLY.monomial("c6_0_01", "c6_0_23", "c6_1_45"),
        POLY.monomial("c6_0_12", "c6_1_34", "c6_0_05"),
        POLY.add(
            POLY.monomial("c6_0_01", "c6_0_23", "c6_0_45"),
            POLY.monomial("c6_0_12", "c6_0_34", "c6_0_05"),
        ),
    )
    require(rows == expected, (rows, expected))
    require(all(word[:3] == (0, 0, 0) for word in words), words)

    # The two boundary channels expose different shore near-perfect factors:
    # q01 when crossing 23, and q12 when crossing 05.  Already the first two
    # rows are coprime monomials, so no positive-degree common shore cofactor
    # can divide all three rows.
    first_variables = set(next(iter(rows[0])))
    second_variables = set(next(iter(rows[1])))
    require(not (first_variables & second_variables),
            (first_variables, second_variables))
    return {
        "perfect_matchings": len(matchings),
        "cut_edges": tuple(sorted(cut)),
        "crossings_per_matching": (1, 1),
        "common_left_word": "000",
        "boundary_channel_rank": 2,
        "row_term_counts": tuple(map(len, rows)),
        "common_nonconstant_monomial_factor": False,
    }


def main():
    formal = formal_common_tail_identity()
    literal_tail = literal_nonmonomial_tail_reinsertion()
    ears = terminal_ear_channel_census()
    counterguard = tight_c6_counterguard()
    print("uniform permanent-triangle common-tail lemma: PASS")
    print("formal arbitrary-tail identity", formal)
    print("literal 12-site tail terms / row terms", literal_tail)
    print("terminal-ear graphs checked", ears)
    print("tight C6 rank-two counterguard", counterguard)
    print("terminal criterion: nonzero rank-one common boundary transfer")


if __name__ == "__main__":
    main()
