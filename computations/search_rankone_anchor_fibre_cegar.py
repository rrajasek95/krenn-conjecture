#!/usr/bin/env python3
"""CEGAR search for a rank-one K6 support escaping elementary fibre obstructions.

This is a discovery tool, not a proof certificate.  It imposes the exact
one-centre coordinate anchors, the unique-anchor mutuality theorem, and the
absence of singleton mixed fibres.  A refinement forbids a binomial fibre
whose two terms recur (with unchanged ratio) inside a trinomial fibre.
"""

from __future__ import annotations

import argparse
from itertools import product

from pysat.solvers import Solver


VERTICES = tuple(range(6))


def perfect_matchings(vertices=VERTICES):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(rest):
            yield tuple(sorted(((first, second),) + tail))


MATCHINGS = tuple(perfect_matchings())
MIXED_WORDS = tuple(word for word in product(range(3), repeat=6)
                    if len(set(word)) > 1)
PURE_WORDS = tuple((colour,) * 6 for colour in range(3))


class Formula:
    def __init__(self):
        self.top = 0
        self.clauses: list[list[int]] = []

    def variable(self):
        self.top += 1
        return self.top

    def add(self, *literals):
        self.clauses.append(list(literals))


def build_formula():
    formula = Formula()
    incidence = {
        (u, v, colour): formula.variable()
        for u in VERTICES for v in VERTICES if u != v
        for colour in range(3)
    }
    singleton = {
        (u, v, colour): formula.variable()
        for u in VERTICES for v in VERTICES if u != v
        for colour in range(3)
    }
    presence = {
        (u, v): formula.variable()
        for u in VERTICES for v in VERTICES if u < v
    }

    for u in VERTICES:
        for v in VERTICES:
            if u == v:
                continue
            edge = presence[tuple(sorted((u, v)))]
            # A rank-one aggregate block is either absent at both ends or
            # has a nonzero factor at both ends.
            formula.add(-edge, *(incidence[u, v, colour]
                                 for colour in range(3)))
            for colour in range(3):
                formula.add(-incidence[u, v, colour], edge)
            for colour in range(3):
                other = tuple(c for c in range(3) if c != colour)
                exact = singleton[u, v, colour]
                formula.add(-exact, incidence[u, v, colour])
                formula.add(-exact, -incidence[u, v, other[0]])
                formula.add(-exact, -incidence[u, v, other[1]])
                formula.add(
                    -incidence[u, v, colour],
                    incidence[u, v, other[0]],
                    incidence[u, v, other[1]],
                    exact,
                )

    # For each centre and colour there is an incoming exact-coordinate
    # anchor.  If it is unique, the one-hole identity makes it mutual.
    for centre in VERTICES:
        for colour in range(3):
            formula.add(*(singleton[u, centre, colour]
                          for u in VERTICES if u != centre))
            for unique_tail in VERTICES:
                if unique_tail == centre:
                    continue
                formula.add(
                    -singleton[unique_tail, centre, colour],
                    *(singleton[u, centre, colour]
                      for u in VERTICES if u not in (centre, unique_tail)),
                    singleton[centre, unique_tail, colour],
                )

    compatible = {}
    for word in PURE_WORDS + MIXED_WORDS:
        terms = []
        for matching_index, matching in enumerate(MATCHINGS):
            term = formula.variable()
            compatible[word, matching_index] = term
            entries = []
            for u, v in matching:
                entries.append(incidence[u, v, word[u]])
                entries.append(incidence[v, u, word[v]])
            for entry in entries:
                formula.add(-term, entry)
            formula.add(*(-entry for entry in entries), term)
            terms.append(term)
        if word in PURE_WORDS:
            formula.add(*terms)
        else:
            # A mixed fibre may be empty, but may not be a singleton.
            for index, term in enumerate(terms):
                formula.add(-term, *(terms[j] for j in range(15) if j != index))

    return formula, incidence, compatible


def supported_fibres(model, compatible):
    positive = {literal for literal in model if literal > 0}
    return {
        word: tuple(index for index in range(15)
                    if compatible[word, index] in positive)
        for word in MIXED_WORDS
    }


def common_vertices(first, second):
    common = set(first) & set(second)
    return {vertex for edge in common for vertex in edge}


def nested_witness(fibres):
    binomials = [(word, terms) for word, terms in fibres.items()
                 if len(terms) == 2]
    trinomials = [(word, terms) for word, terms in fibres.items()
                  if len(terms) == 3]
    for lower_word, pair in binomials:
        fixed_vertices = common_vertices(
            MATCHINGS[pair[0]], MATCHINGS[pair[1]]
        )
        pair_set = set(pair)
        for upper_word, triple in trinomials:
            if not pair_set.issubset(triple):
                continue
            changed = {v for v in VERTICES
                       if lower_word[v] != upper_word[v]}
            if changed.issubset(fixed_vertices):
                return lower_word, pair, upper_word, triple
    return None


def exponent(word, matching):
    result = [0] * 90
    for u, v in matching:
        result[(5 * u + (v if v < u else v - 1)) * 3 + word[u]] += 1
        result[(5 * v + (u if u < v else u - 1)) * 3 + word[v]] += 1
    return tuple(result)


def difference(word, first, second):
    left = exponent(word, MATCHINGS[first])
    right = exponent(word, MATCHINGS[second])
    return tuple(a - b for a, b in zip(left, right))


def rectangle_witness(fibres):
    """Find R(t)R(e)=R(b)R(d) with b,d,e binomial and t trinomial."""
    by_pair = {}
    for word, terms in fibres.items():
        if len(terms) == 2:
            pair = tuple(sorted(terms))
            by_pair.setdefault(pair, []).append((word, difference(word, *pair)))
    for target_word, triple in fibres.items():
        if len(triple) != 3:
            continue
        for first_index in range(3):
            for second_index in range(first_index + 1, 3):
                pair = tuple(sorted((triple[first_index], triple[second_index])))
                rows = by_pair.get(pair, ())
                if len(rows) < 3:
                    continue
                target = difference(target_word, *pair)
                pair_sums = {}
                for b_word, b_row in rows:
                    for d_word, d_row in rows:
                        total = tuple(a + b for a, b in zip(b_row, d_row))
                        pair_sums.setdefault(total, (b_word, d_word))
                for e_word, e_row in rows:
                    wanted = tuple(a + b for a, b in zip(target, e_row))
                    if wanted in pair_sums:
                        b_word, d_word = pair_sums[wanted]
                        return target_word, triple, pair, b_word, d_word, e_word
    return None


def exact_fibre_clause(compatible, word, expected):
    expected = set(expected)
    return [
        -compatible[word, index] if index in expected
        else compatible[word, index]
        for index in range(15)
    ]


def block_nested_witness(solver, compatible, witness):
    lower_word, pair, upper_word, triple = witness
    clause = []
    clause.extend(exact_fibre_clause(compatible, lower_word, pair))
    clause.extend(exact_fibre_clause(compatible, upper_word, triple))
    solver.add_clause(clause)


def block_rectangle_witness(solver, compatible, witness):
    target_word, triple, pair, b_word, d_word, e_word = witness
    clause = []
    patterns = {
        target_word: triple,
        b_word: pair,
        d_word: pair,
        e_word: pair,
    }
    for word, expected in patterns.items():
        clause.extend(exact_fibre_clause(compatible, word, expected))
    solver.add_clause(clause)


def show_support(model, incidence):
    positive = {literal for literal in model if literal > 0}
    for u in VERTICES:
        row = []
        for v in VERTICES:
            if u == v:
                continue
            mask = "".join(str(c) for c in range(3)
                           if incidence[u, v, c] in positive)
            row.append(f"{v}:{mask}")
        print(u, " ".join(row), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rounds", type=int, default=10000)
    args = parser.parse_args()
    formula, incidence, compatible = build_formula()
    print(f"variables={formula.top} clauses={len(formula.clauses)}", flush=True)
    with Solver(name="cadical195", bootstrap_with=formula.clauses) as solver:
        for round_index in range(args.rounds):
            if not solver.solve():
                print(f"UNSAT after {round_index} nested-fibre refinements")
                return
            model = solver.get_model()
            fibres = supported_fibres(model, compatible)
            witness = nested_witness(fibres)
            rectangle = None if witness is not None else rectangle_witness(fibres)
            if witness is None and rectangle is None:
                histogram = {
                    size: sum(len(terms) == size for terms in fibres.values())
                    for size in range(16)
                    if any(len(terms) == size for terms in fibres.values())
                }
                print(f"SURVIVOR round={round_index} fibres={histogram}")
                show_support(model, incidence)
                return
            if witness is not None:
                block_nested_witness(solver, compatible, witness)
                kind = "nested"
                lower, pair, upper, triple = witness
                detail = (
                    f"{''.join(map(str, lower))}:{pair} -> "
                    f"{''.join(map(str, upper))}:{triple}"
                )
            else:
                block_rectangle_witness(solver, compatible, rectangle)
                kind = "rectangle"
                target, triple, pair, b_word, d_word, e_word = rectangle
                detail = (
                    f"{''.join(map(str, target))}:{triple} via {pair} and "
                    f"{''.join(map(str, b_word))},"
                    f"{''.join(map(str, d_word))},"
                    f"{''.join(map(str, e_word))}"
                )
            if round_index < 10 or (round_index + 1) % 100 == 0:
                print(
                    f"refine {round_index + 1} ({kind}): {detail}",
                    flush=True,
                )
        print(f"ROUND LIMIT {args.rounds}")


if __name__ == "__main__":
    main()
