#!/usr/bin/env python3
"""UNAUDITED PROBE (W2) -- the monomial regime with rank >= 2 blocks.

Pinned HEAD: 26ba69f7e643694c6a58464af6e9e1de9ec92f01

The one-cell-per-edge stratum is exhausted by w2_hunt8.py.  This module lifts
the same exact machinery to blocks with SEVERAL cells, which is where the
candidate regime of task A puts its rank >= 2 blocks:

  cell support of an edge uv = the set of (a, b) with A_uv[a][b] != 0.

  'injection'  every block is a MONOMIAL MATRIX (at most one cell per row and
               per column, i.e. a scaled partial permutation).  This is the
               regime forced by two distinct s*kappa blockings (w2_regime.py
               Claim C), and it FORCES every rank-one block to be a single
               coordinate cell.
  'cross'      every block is supported in row c U column c for some c (the
               regime forced by one s*kappa_c blocking).
  'free'       arbitrary cell supports (the general support problem; included
               only as a control).

Structure used throughout (the reformulation that makes the census cheap):

    fibre(colouring) = PM(G_colouring),
    G_colouring = { uv : (colouring_u, colouring_v) is a cell of A_uv },

so a mixed singleton is a colouring whose compatibility graph has a UNIQUE
perfect matching.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
import random

from w2_monomial import (Character, Q, class_decomposition, geometry,
                         is_mixed)

INJECTION_PATTERNS = None


def all_partial_injections():
    """34 partial injections of {0,1,2} into {0,1,2}, as frozensets of cells."""
    global INJECTION_PATTERNS
    if INJECTION_PATTERNS is not None:
        return INJECTION_PATTERNS
    out = set()
    for size in range(4):
        for rows in combinations(range(Q), size):
            for columns in product(range(Q), repeat=size):
                if len(set(columns)) != size:
                    continue
                out.add(frozenset(zip(rows, columns)))
    INJECTION_PATTERNS = tuple(sorted(out, key=lambda s: (len(s), sorted(s))))
    return INJECTION_PATTERNS


def cross_patterns():
    out = set()
    for colour in range(Q):
        full = [(i, j) for i in range(Q) for j in range(Q)
                if i == colour or j == colour]
        for size in range(len(full) + 1):
            for subset in combinations(full, size):
                out.add(frozenset(subset))
    return tuple(sorted(out, key=lambda s: (len(s), sorted(s))))


def cell_index(geo, edge, a, b):
    return 9 * edge + 3 * a + b


def cell_fibres(geo, cells):
    """cells[e] is a set of (a, b).  Returns {colouring: [matching numbers]}."""
    table: dict[tuple[int, ...], list[int]] = {}
    for number, matching in enumerate(geo.matchings):
        options = []
        ok = True
        for u, v in matching:
            choices = cells[geo.index[(u, v)]]
            if not choices:
                ok = False
                break
            options.append(((u, v), tuple(sorted(choices))))
        if not ok:
            continue
        for combination in product(*[choices for _edge, choices in options]):
            colouring = [-1] * geo.size
            for ((u, v), _all), (a, b) in zip(options, combination):
                colouring[u], colouring[v] = a, b
            table.setdefault(tuple(colouring), []).append(number)
    return table


def cell_exponent(geo, number, colouring):
    row = [0] * (9 * len(geo.edges))
    for u, v in geo.matchings[number]:
        row[cell_index(geo, geo.index[(u, v)], colouring[u], colouring[v])] += 1
    return tuple(row)


def analyse_cells(geo, cells, max_rounds=40, table=None):
    """Exactly w2_monomial.analyse, over cell supports instead of labels."""
    if table is None:
        table = cell_fibres(geo, cells)
    mixed = {c: m for c, m in table.items() if is_mixed(c)}
    for colour in range(Q):
        if not table.get(tuple([colour] * geo.size)):
            return {"verdict": "missing-constant", "colour": colour}
    singles = [c for c, m in mixed.items() if len(m) == 1]
    if singles:
        return {"verdict": "O2-literal-singleton", "singletons": len(singles),
                "words": [list(w) for w in singles[:5]]}

    width = 9 * len(geo.edges)
    character = Character(width)
    exponents = {(number, colouring): cell_exponent(geo, number, colouring)
                 for colouring, members in table.items() for number in members}
    binomials = [(c, m) for c, m in sorted(mixed.items()) if len(m) == 2]
    for colouring, (first, second) in binomials:
        difference = [a - b for a, b in zip(exponents[(first, colouring)],
                                            exponents[(second, colouring)])]
        character.add(difference, Fraction(-1))
    relation = character.odd_relation()
    if relation is not None:
        return {"verdict": "O1-odd-holonomy",
                "coefficients": [x for x in relation if x],
                "binomials": len(binomials)}

    for _ in range(max_rounds):
        changed = False
        for colouring, members in sorted(mixed.items()):
            if len(members) == 2:
                continue
            vectors = [exponents[(number, colouring)] for number in members]
            classes = class_decomposition(character, vectors)
            live = [entry for entry in classes if entry[1] != 0]
            if len(live) == 1:
                return {"verdict": "O2-one-live-class", "word": list(colouring),
                        "terms": len(members)}
            if len(live) == 2:
                (i, ci), (j, cj) = live
                difference = [a - b for a, b in zip(vectors[i], vectors[j])]
                character.add(difference, Fraction(-1) * cj / ci)
                if character.odd_relation() is not None:
                    return {"verdict": "O1-odd-holonomy",
                            "detail": "after class propagation"}
                changed = True
        if not changed:
            break

    for colour in range(Q):
        colouring = tuple([colour] * geo.size)
        vectors = [exponents[(number, colouring)]
                   for number in table[colouring]]
        classes = class_decomposition(character, vectors)
        if all(entry[1] == 0 for entry in classes):
            return {"verdict": "K3-pure-vanishing", "colour": colour}

    return {"verdict": "survivor", "relations": len(character.rows)}


def mixed_singletons(table):
    return sum(1 for c, m in table.items() if is_mixed(c) and len(m) == 1)


def support_cells(cells):
    return sum(len(entry) for entry in cells)


def random_monomial(geo, targets, rng, pattern, budget):
    """Random template: three constant matchings + a cell budget."""
    patterns = (all_partial_injections() if pattern == "injection"
                else cross_patterns())
    cells = [set() for _ in geo.edges]
    fixed = set()
    for colour, matching in enumerate(targets):
        for edge in matching:
            cells[geo.index[edge]].add((colour, colour))
            fixed.add(geo.index[edge])
    slots = list(range(len(geo.edges)))
    rng.shuffle(slots)
    for index in slots:
        if support_cells(cells) >= budget:
            break
        wanted = rng.choice(patterns)
        merged = set(cells[index]) | set(wanted)
        if pattern == "injection":
            rows = [a for a, _ in merged]
            columns = [b for _, b in merged]
            if len(set(rows)) != len(rows) or len(set(columns)) != len(columns):
                continue
        if support_cells(cells) - len(cells[index]) + len(merged) > budget:
            continue
        cells[index] = merged
    return [frozenset(entry) for entry in cells]


def neighbours(geo, cells, targets, pattern, rng, budget):
    """One local move: add or drop a single cell, keeping the pattern class."""
    fixed = {(geo.index[edge], (colour, colour))
             for colour, matching in enumerate(targets) for edge in matching}
    candidates = []
    for index in range(len(geo.edges)):
        current = set(cells[index])
        for a in range(Q):
            for b in range(Q):
                cell = (a, b)
                if cell in current:
                    if (index, cell) in fixed:
                        continue
                    candidates.append((index, cell, "drop"))
                else:
                    merged = current | {cell}
                    if pattern == "injection":
                        rows = [x for x, _ in merged]
                        columns = [y for _, y in merged]
                        if (len(set(rows)) != len(rows)
                                or len(set(columns)) != len(columns)):
                            continue
                    if support_cells(cells) + 1 > budget:
                        continue
                    candidates.append((index, cell, "add"))
    if not candidates:
        return None
    index, cell, move = rng.choice(candidates)
    out = [set(entry) for entry in cells]
    if move == "add":
        out[index].add(cell)
    else:
        out[index].discard(cell)
    return [frozenset(entry) for entry in out]
