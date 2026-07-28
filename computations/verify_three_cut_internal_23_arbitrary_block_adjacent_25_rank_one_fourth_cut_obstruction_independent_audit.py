#!/usr/bin/env python3
"""Clean-room exact audit of the adjacent rank-one (E10, E20) fourth-cut theorem.

Audits notes/three-cut-internal-23-arbitrary-block-adjacent-25-rank-one-
fourth-cut-obstruction.md.  This checker imports no project module and
consumes no matrix, basis, minor, locus, or Singular program emitted by the
primary implementation.  Everything is rebuilt from the note's statement
alone, with deliberately different orderings:

* perfect matchings by a greatest-vertex recursion (mates scanned downward);
* reverse lexicographic word order for every row system;
* cylinder columns enumerated hole-descending, colours descending;
* this audit's own Gauss pivot scans (three row priority fallbacks);
* the three literal C2 duplicates resolved by keeping the FIRST member seen
  in the reversed enumeration (the E22 audit kept the last);
* independently designed 43x43 minor anchors of [C4|D] (42 signature words
  plus one obstruction word) whose determinants come out as the D_full
  generators up to sign, corroborated by seeded off-locus Gauss scans;
* Singular rings with reversed variable order and reversed generator order.

The audited family keeps the seven endpoint-ordered cells 01:E00, 45:E00,
02:E11, 14:E11, 04:E22, 13:E22, 35:E10, lets A23 = X in Mat3(C) be
arbitrary, and moves A25 = E00 + t*Ec0 for the direction colour c in {1,2}.
All nine x_ab and t stay exact symbols over Q throughout; numerical spot
checks use Fractions only.

AUDIT OUTCOME.  Every geometric claim of the primary note (sections 2-5
and equation (12)) is confirmed, as are the eight radical certificates and
the four line packets.  The section-6 claim that the two D_full plane
packets (target colours {0,1}, scalar families for H and D) have reduced
Groebner basis [1] is FALSE: on the sublocus {X = a0*E00, a0 != 0, t = 0}
of D_full the tail identity gives H - D = a0*[0^6], the pure colour-0
target lies inside the normal <H,D>, and an explicit rational star witness
satisfies every packet generator.  This script proves that witness
symbolically, corroborates it with a fast specialized Singular run, runs
the note's own programs to record their non-unit Groebner bases, and
exits nonzero because a note claim fails.  The supplementary
colours-(1,2) plane packets are reported informationally; they are NOT a
complete repair either (the E10 one is non-unit, e.g. satisfiable at
X = E21, i.e. a=0, w=0, u=1, for both t=0 and t=1).
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from fractions import Fraction
from functools import lru_cache
import hashlib
from itertools import product
import random
import shutil
import subprocess
import sys
import time

import sympy as sp


Q = Fraction
COLOURS = (0, 1, 2)
SIX = tuple(range(6))
EIGHT = tuple(range(8))
CELLS = tuple(product(COLOURS, repeat=2))
ACTIVE = (0, 1)
DIRECTIONS = (1, 2)
FINAL_CUTS = (5, 0, 1)

# Every cell is endpoint ordered: the first colour belongs to the smaller
# endpoint.  In particular 35:E10 is not silently transposed, and the moving
# block sits on the ordered pair (2,5): A25 = E00 + t*Ec0 places colour c at
# site 2 and colour 0 at site 5.
BASE_SOURCES = (
    (0, 1, 0, 0),
    (4, 5, 0, 0),
    (0, 2, 1, 1),
    (1, 4, 1, 1),
    (0, 4, 2, 2),
    (1, 3, 2, 2),
    (3, 5, 1, 0),
    (2, 5, 0, 0),
)


def moving_source(direction):
    return (2, 5, direction, 0)


X_SYMBOLS = sp.symbols("x00 x01 x02 x10 x11 x12 x20 x21 x22")
T = sp.Symbol("t")
X_OF_CELL = dict(zip(CELLS, X_SYMBOLS))

E_WORDS = tuple((0, 0, a, b, 0, 0) for a, b in CELLS)
READOUT_WORDS = E_WORDS + (
    (0, 0, 0, 1, 1, 0), (0, 0, 0, 1, 2, 0), (1, 2, 1, 2, 0, 0),
)
FORBIDDEN_W_WORDS = ((1, 2, 1, 2, 1, 0), (1, 2, 1, 2, 2, 0))

# Frozen after the first fully independent exact replay of this audit's own
# differently ordered certificates.  Empty strings skip the comparison.
EXPECTED_RANK_LEDGER_SHA256 = ""
EXPECTED_IDEAL_LEDGER_SHA256 = ""


def add(vector, key, value):
    """Sparse addition valid for both Fractions and SymPy expressions."""
    if value == 0:
        return
    total = vector.get(key, 0) + value
    total = sp.expand(total) if isinstance(total, sp.Basic) else total
    if total == 0:
        vector.pop(key, None)
    else:
        vector[key] = total


def linear_combination(terms):
    answer = {}
    for vector, scalar in terms:
        for key, value in vector.items():
            add(answer, key, scalar * value)
    return answer


@lru_cache(maxsize=None)
def perfect_matchings(vertices):
    """Pair the greatest remaining vertex; returned edges are ordered."""
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    greatest = vertices[-1]
    answer = []
    for index in range(len(vertices) - 2, -1, -1):
        mate = vertices[index]
        remainder = vertices[:index] + vertices[index + 1:-1]
        for tail in perfect_matchings(remainder):
            answer.append(tail + ((mate, greatest),))
    return tuple(answer)


def internal_blocks(x_values, t_value, direction):
    blocks = defaultdict(dict)
    for left, right, left_colour, right_colour in BASE_SOURCES:
        blocks[left, right][left_colour, right_colour] = 1
    if t_value != 0:
        left, right, left_colour, right_colour = moving_source(direction)
        blocks[left, right][left_colour, right_colour] = t_value
    for index, value in enumerate(x_values):
        if value != 0:
            blocks[2, 3][CELLS[index]] = value
    return {edge: dict(cells) for edge, cells in blocks.items()}


def matching_tensor(vertices, blocks):
    vertices = tuple(vertices)
    position = {site: index for index, site in enumerate(vertices)}
    answer = {}
    for matching in perfect_matchings(vertices):
        choices = [tuple(blocks.get(edge, {}).items()) for edge in matching]
        if any(not options for options in choices):
            continue
        for selected in product(*choices):
            word = [-1] * len(vertices)
            coefficient = 1
            for (left, right), ((left_colour, right_colour), value) in zip(
                matching, selected
            ):
                word[position[left]] = left_colour
                word[position[right]] = right_colour
                coefficient = coefficient * value
            add(answer, tuple(word), coefficient)
    return answer


def raw_columns(cut, blocks):
    """Return the 45 raw cylinder columns in reversed independent order."""
    remaining = tuple(site for site in SIX if site != cut)
    columns = []
    labels = []
    for hole in reversed(remaining):
        rest = tuple(site for site in remaining if site != hole)
        cofactor = matching_tensor(rest, blocks)
        for hole_colour in reversed(COLOURS):
            for cut_colour in reversed(COLOURS):
                vector = {}
                for rest_word, coefficient in cofactor.items():
                    assignment = dict(zip(rest, rest_word))
                    assignment[hole] = hole_colour
                    assignment[cut] = cut_colour
                    add(
                        vector,
                        tuple(assignment[site] for site in SIX),
                        coefficient,
                    )
                columns.append(vector)
                labels.append((hole, hole_colour, cut_colour))
    assert len(columns) == len(labels) == 45
    return tuple(columns), tuple(labels)


def direct_representation(cut, blocks, columns, labels):
    """Expand the direct tensor along the internal edges incident to cut."""
    answer = {}
    for column, (hole, hole_colour, cut_colour) in zip(columns, labels):
        edge = tuple(sorted((cut, hole)))
        cell = ((cut_colour, hole_colour) if cut < hole
                else (hole_colour, cut_colour))
        coefficient = blocks.get(edge, {}).get(cell, 0)
        if coefficient != 0:
            for word, value in column.items():
                add(answer, word, coefficient * value)
    return answer


def word_terms(blocks):
    """Endpoint-inserted cofactor atoms grouped by their six-site word."""
    grouped = defaultdict(list)
    for right in reversed(SIX):
        for left in reversed(tuple(site for site in SIX if site < right)):
            rest = tuple(site for site in SIX if site not in (left, right))
            cofactor = matching_tensor(rest, blocks)
            for rest_word, coefficient in cofactor.items():
                for right_colour in reversed(COLOURS):
                    for left_colour in reversed(COLOURS):
                        assignment = dict(zip(rest, rest_word))
                        assignment[left] = left_colour
                        assignment[right] = right_colour
                        word = tuple(assignment[site] for site in SIX)
                        grouped[word].append((
                            left, left_colour, right, right_colour, coefficient
                        ))
    return {word: tuple(terms) for word, terms in grouped.items()}


# --------------------------------------------------------------------------
# W members, explicit representations, degenerate locus definitions.
# --------------------------------------------------------------------------

def d_member(direction):
    return {
        (1, 1, 1, 1, 1, 0): sp.Integer(1),
        (1, 2, 1, 2, 0, 0): sp.Integer(1),
        (2, 2, 0, 2, 2, 0): sp.Integer(1),
        (2, 2, direction, 2, 2, 0): T,
    }


def w_members(direction):
    members = []
    for (a, b), word in zip(CELLS, E_WORDS):
        members.append((f"e{a}{b}", {word: sp.Integer(1)}))
    members.append(("sigma1", {
        (0, 0, 0, 1, 1, 0): sp.Integer(1),
        (0, 0, direction, 1, 1, 0): T,
    }))
    members.append(("sigma2", {
        (0, 0, 0, 1, 2, 0): sp.Integer(1),
        (0, 0, direction, 1, 2, 0): T,
    }))
    members.append(("D", d_member(direction)))
    return tuple(members)


def w_representations(direction):
    """This audit's own exact column representations, derived by hand from
    the reconstructed cofactor structure (labels are (hole, hcol, ccol))."""
    c = direction
    reps_c2 = {}
    reps_c3 = {}
    for a, b in CELLS:
        reps_c2[f"e{a}{b}"] = (((3, b, a), sp.Integer(1)),)
        reps_c3[f"e{a}{b}"] = (((2, a, b), sp.Integer(1)),)
    reps_c2["sigma1"] = (((4, 1, 0), sp.Integer(1)), ((4, 1, c), T))
    reps_c2["sigma2"] = (((4, 2, 0), sp.Integer(1)), ((4, 2, c), T))
    reps_c2["D"] = (
        ((0, 1, 1), sp.Integer(1)),
        ((5, 0, 0), sp.Integer(1)),
        ((5, 0, c), T),
    )
    reps_c3["sigma1"] = (((4, 1, 1), sp.Integer(1)),)
    reps_c3["sigma2"] = (((4, 2, 1), sp.Integer(1)),)
    reps_c3["D"] = (((1, 2, 2), sp.Integer(1)), ((5, 0, 1), sp.Integer(1)))
    return reps_c2, reps_c3


def d_boundary_representations():
    """Two-column representations of D inside C0 and C1 (audit's own)."""
    return {
        0: (((2, 1, 1), sp.Integer(1)), ((4, 2, 2), sp.Integer(1))),
        1: (((3, 2, 2), sp.Integer(1)), ((4, 1, 1), sp.Integer(1))),
    }


def locus_generators(direction):
    other = 3 - direction
    return (
        sp.expand(T * X_OF_CELL[0, 0] - X_OF_CELL[direction, 0]),
        sp.expand(T * X_OF_CELL[0, 2] - X_OF_CELL[direction, 2]),
        X_OF_CELL[other, 0],
        X_OF_CELL[other, 2],
    )


def locus_x_values(direction, a0, a1, a2, w, u, t_value):
    """X = (e0 + t*ec) (x) (a0,a1,a2)  +  (0,w,u) (x) e1."""
    m = {1: w, 2: u}
    other = 3 - direction
    values = {(0, 0): a0, (0, 1): a1, (0, 2): a2}
    values[direction, 0] = t_value * a0
    values[direction, 1] = t_value * a1 + m[direction]
    values[direction, 2] = t_value * a2
    values[other, 0] = 0
    values[other, 1] = m[other]
    values[other, 2] = 0
    return tuple(sp.expand(values[cell]) for cell in CELLS)


# --------------------------------------------------------------------------
# Exact rational sparse linear algebra (greatest-coordinate elimination).
# --------------------------------------------------------------------------

def rref_basis(vectors, coordinates=None):
    rows = [
        {key: Q(value) for key, value in vector.items() if value}
        for vector in vectors
    ]
    rows = [row for row in rows if row]
    if coordinates is None:
        coordinates = sorted(
            set().union(*(set(row) for row in rows)) if rows else (),
            reverse=True,
        )
    else:
        coordinates = tuple(coordinates)
    active = 0
    pivots = []
    for coordinate in coordinates:
        found = next((index for index in range(active, len(rows))
                      if rows[index].get(coordinate, 0)), None)
        if found is None:
            continue
        rows[active], rows[found] = rows[found], rows[active]
        pivot_value = rows[active][coordinate]
        rows[active] = {
            key: value / pivot_value for key, value in rows[active].items()
        }
        for index, row in enumerate(rows):
            if index == active:
                continue
            multiple = row.get(coordinate, Q(0))
            if multiple == 0:
                continue
            for key, value in rows[active].items():
                add(row, key, -multiple * value)
        pivots.append(coordinate)
        active += 1
        if active == len(rows):
            break
    assert all(not row for row in rows[active:])
    return tuple(rows[:active]), tuple(pivots)


def rank(vectors):
    return len(rref_basis(vectors)[0])


def annihilator(vectors, coordinates):
    coordinates = tuple(coordinates)
    rows, pivots = rref_basis(vectors, coordinates)
    pivot_set = set(pivots)
    result = []
    for free in coordinates:
        if free in pivot_set:
            continue
        functional = {free: Q(1)}
        for row, pivot in zip(rows, pivots):
            coefficient = -row.get(free, Q(0))
            if coefficient:
                functional[pivot] = coefficient
        result.append(functional)
    for vector in vectors:
        for functional in result:
            assert sum(value * functional.get(key, 0)
                       for key, value in vector.items()) == 0
    return tuple(result)


def intersection_two(left, right):
    left = rref_basis(left)[0]
    right = rref_basis(right)[0]
    if not left or not right:
        return ()
    coordinates = tuple(sorted(set().union(
        *(set(row) for row in left + right)
    ), reverse=True))
    dual = annihilator(left, coordinates) + annihilator(right, coordinates)
    return rref_basis(annihilator(dual, coordinates), coordinates)[0]


def intersection_many(spaces):
    result = rref_basis(spaces[0])[0]
    for space in spaces[1:]:
        result = intersection_two(result, space)
    return result


def in_span(vector, space):
    return rank(tuple(space) + (vector,)) == rank(space)


def same_span(left, right):
    return rank(left) == rank(right) and all(in_span(row, right) for row in left)


# --------------------------------------------------------------------------
# Dense Fraction Gauss for pivot selection.
# --------------------------------------------------------------------------

def to_rational(expression, substitution):
    value = sp.expand(expression)
    if substitution:
        value = value.subs(substitution)
    value = sp.nsimplify(value) if not isinstance(value, sp.Basic) else value
    assert value.is_Rational, value
    return Q(int(value.p), int(value.q))


def gauss_pivot_pairs(dense_rows, column_count, row_priority):
    work = [list(row) for row in dense_rows]
    chosen = []
    used = set()
    for column in range(column_count):
        pivot = next(
            (row for row in row_priority
             if row not in used and work[row][column] != 0),
            None,
        )
        if pivot is None:
            continue
        chosen.append((pivot, column))
        used.add(pivot)
        pivot_value = work[pivot][column]
        pivot_row = work[pivot]
        for row in range(len(work)):
            if row == pivot:
                continue
            factor = work[row][column]
            if factor:
                factor = factor / pivot_value
                target = work[row]
                for index in range(column, column_count):
                    if pivot_row[index]:
                        target[index] -= factor * pivot_row[index]
    return chosen


# --------------------------------------------------------------------------
# Phase 1: endpoint-order literal eight-site boundary fibre identity.
# --------------------------------------------------------------------------

def audit_eight_site(direction):
    pool = [Q(1201 + 7 * index, 9973) for index in range(127)]
    assert len(set(pool)) == 127
    values = iter(pool)
    x_values = tuple(next(values) for _ in range(9))
    t_value = next(values)
    p = {(a, site, colour): next(values)
         for a in COLOURS for site in SIX for colour in COLOURS}
    q = {(b, site, colour): next(values)
         for b in COLOURS for site in SIX for colour in COLOURS}
    r = {(a, b): next(values) for a in COLOURS for b in COLOURS}
    interior = internal_blocks(x_values, t_value, direction)
    blocks = {edge: dict(cells) for edge, cells in interior.items()}
    for site in SIX:
        blocks[site, 6] = {(colour, a): p[a, site, colour]
                           for colour in COLOURS for a in COLOURS}
        blocks[site, 7] = {(colour, b): q[b, site, colour]
                           for colour in COLOURS for b in COLOURS}
    blocks[6, 7] = dict(r)
    observed_full = matching_tensor(EIGHT, blocks)
    hs = matching_tensor(SIX, interior)
    atoms = word_terms(interior)
    for a, b in product(COLOURS, repeat=2):
        observed = {word[:6]: value for word, value in observed_full.items()
                    if word[6:] == (a, b)}
        expected = {}
        for word, value in hs.items():
            add(expected, word, r[a, b] * value)
        for word, terms in atoms.items():
            total = Q(0)
            for left, lc, right, rc, coefficient in terms:
                total += coefficient * (
                    p[a, left, lc] * q[b, right, rc]
                    + p[a, right, rc] * q[b, left, lc]
                )
            add(expected, word, total)
        assert observed == expected, (direction, a, b)


# --------------------------------------------------------------------------
# Phase 2: no matching term mixes X and t (site 2 is shared by 23 and 25).
# --------------------------------------------------------------------------

def multilinear_degree_ok(expression):
    poly = sp.Poly(sp.expand(expression), *X_SYMBOLS, T)
    return poly.total_degree() <= 1


def audit_no_mixing(direction):
    blocks = internal_blocks(X_SYMBOLS, T, direction)
    hs = matching_tensor(SIX, blocks)
    assert all(multilinear_degree_ok(value) for value in hs.values())
    for right in SIX:
        for left in range(right):
            rest = tuple(site for site in SIX if site not in (left, right))
            cofactor = matching_tensor(rest, blocks)
            assert all(multilinear_degree_ok(value)
                       for value in cofactor.values())
    for cut in SIX:
        columns, _labels = raw_columns(cut, blocks)
        for column in columns:
            assert all(multilinear_degree_ok(value)
                       for value in column.values())


# --------------------------------------------------------------------------
# Phase 3: the two-cylinder space W = C2 cap C3.
# --------------------------------------------------------------------------

def duplicate_free_c2(columns, labels):
    def key(vector):
        return tuple(sorted(
            (word, sp.srepr(sp.expand(sp.sympify(value))))
            for word, value in vector.items()
        ))

    classes = defaultdict(list)
    for index, vector in enumerate(columns):
        classes[key(vector)].append(index)
    sizes = sorted(len(indices) for indices in classes.values())
    assert sizes.count(2) == 3 and set(sizes) <= {1, 2}
    duplicate_pairs = tuple(sorted(
        tuple(sorted(labels[index] for index in indices))
        for indices in classes.values() if len(indices) == 2
    ))
    keep = tuple(sorted(indices[0] for indices in classes.values()))
    assert len(keep) == 42
    return keep, duplicate_pairs


def symbolic_matrix_det(entries_matrix):
    return sp.factor(sp.Matrix(entries_matrix).det(method="domain-ge"))


def constant_unit_minor(words, column_vectors, parameters, expected_rank):
    zero_subs = {parameter: 0 for parameter in parameters}
    dense = []
    word_index = {word: index for index, word in enumerate(words)}
    for word in words:
        dense.append([Q(0)] * len(column_vectors))
    for column, vector in enumerate(column_vectors):
        for word, value in vector.items():
            dense[word_index[word]][column] = to_rational(
                sp.sympify(value), zero_subs
            )
    orders = {
        "reverse_lex": list(range(len(words))),
        "site2_constant_first": sorted(
            range(len(words)),
            key=lambda index: (words[index][2] in (1, 2), index),
        ),
        "lex": list(range(len(words) - 1, -1, -1)),
    }
    last_error = None
    for name, priority in orders.items():
        chosen = gauss_pivot_pairs(dense, len(column_vectors), priority)
        if len(chosen) != expected_rank:
            last_error = (name, len(chosen))
            continue
        rows = [row for row, _column in chosen]
        cols = [column for _row, column in chosen]
        minor = [
            [sp.expand(sp.sympify(column_vectors[c].get(words[r], 0)))
             for c in cols]
            for r in rows
        ]
        determinant = symbolic_matrix_det(minor)
        nonzeros = sum(1 for row in minor for value in row if value != 0)
        if determinant in (1, -1):
            return name, tuple(rows), tuple(cols), determinant, nonzeros
        last_error = (name, str(determinant))
    raise AssertionError(f"no constant unit minor found: {last_error}")


def audit_w_structure(direction):
    blocks = internal_blocks(X_SYMBOLS, T, direction)
    data = {cut: raw_columns(cut, blocks) for cut in SIX}
    c2_columns, c2_labels = data[2]
    c3_columns, c3_labels = data[3]
    c4_columns, c4_labels = data[4]
    x_set = set(X_SYMBOLS)

    # C2 involves neither X nor t; C3 involves t but not X.
    for column in c2_columns:
        for value in column.values():
            assert not (sp.sympify(value).free_symbols & (x_set | {T}))
    for column in c3_columns:
        for value in column.values():
            assert not (sp.sympify(value).free_symbols & x_set)

    # Duplicates and the simultaneous representation matrix [C3 | -C2].
    keep, duplicate_pairs = duplicate_free_c2(c2_columns, c2_labels)
    assert duplicate_pairs == tuple(sorted(
        tuple(sorted(((4, 0, k), (3, 1, k)))) for k in COLOURS
    ))
    column_vectors = list(c3_columns)
    column_names = [("C3",) + label for label in c3_labels]
    for index in keep:
        column_vectors.append(linear_combination(((c2_columns[index], -1),)))
        column_names.append(("C2",) + c2_labels[index])
    assert len(column_vectors) == 87
    words = sorted(set().union(*(set(v) for v in column_vectors)),
                   reverse=True)
    order_name, rows, cols, determinant, nonzeros = constant_unit_minor(
        words, column_vectors, (T,), 72
    )

    # C2 injectivity: the 42 kept columns are constant with rank 42.
    assert rank(tuple(
        {word: Q(int(sp.Integer(value))) for word, value in
         c2_columns[index].items()}
        for index in keep
    )) == 42

    # Rank-one kernel relations, one per cut-colour block.
    c3_by_label = dict(zip(c3_labels, c3_columns))
    c4_by_label = dict(zip(c4_labels, c4_columns))
    for k in COLOURS:
        relation3 = linear_combination((
            (c3_by_label[2, 0, k], sp.Integer(1)),
            (c3_by_label[2, direction, k], T),
            (c3_by_label[4, 0, k], sp.Integer(-1)),
        ))
        assert not relation3, (direction, k, relation3)
        relation4 = linear_combination((
            (c4_by_label[2, 0, k], sp.Integer(1)),
            (c4_by_label[2, direction, k], T),
            (c4_by_label[3, 1, k], sp.Integer(-1)),
        ))
        assert not relation4, (direction, k, relation4)
    # The three relations touch disjoint cut-colour blocks and restrict to
    # -identity on the columns (4,0,k) resp. (3,1,k): independent for all t.

    # Twelve members with exact representations in both cylinders.
    members = w_members(direction)
    reps_c2, reps_c3 = w_representations(direction)
    c2_by_label = dict(zip(c2_labels, c2_columns))
    for name, member in members:
        for reps, by_label in ((reps_c2, c2_by_label), (reps_c3, c3_by_label)):
            combination = linear_combination(tuple(
                (by_label[label], coefficient)
                for label, coefficient in reps[name]
            ))
            difference = linear_combination(
                ((combination, 1), (member, -1))
            )
            assert not difference, (direction, name)
    for (a, b), word in zip(CELLS, E_WORDS):
        assert c2_by_label[3, b, a] == {word: 1}
        assert c3_by_label[2, a, b] == {word: 1}

    # Identity readout on the twelve probe words: independence and exact
    # coefficient readout, uniformly in t.
    for row_index, (name, member) in enumerate(members):
        for column_index, word in enumerate(READOUT_WORDS):
            expected = sp.Integer(1 if row_index == column_index else 0)
            assert sp.expand(sp.sympify(member.get(word, 0)) - expected) == 0
        for word in FORBIDDEN_W_WORDS:
            assert word not in member

    # Tail identity H = sum x_ab e_ab + D and H in all six cylinders.
    hs = matching_tensor(SIX, blocks)
    tail_expected = {word: X_OF_CELL[cell]
                     for cell, word in zip(CELLS, E_WORDS)}
    for word, value in d_member(direction).items():
        add(tail_expected, word, value)
    assert not linear_combination(((hs, 1), (tail_expected, -1)))
    for cut in SIX:
        columns, labels = data[cut]
        direct = direct_representation(cut, blocks, columns, labels)
        assert not linear_combination(((direct, 1), (hs, -1))), cut

    return {
        "matrix_shape": (len(words), 87),
        "duplicate_pairs": duplicate_pairs,
        "minor_order": order_name,
        "minor_rows": rows,
        "minor_cols": cols,
        "minor_det": str(determinant),
        "minor_nonzeros": nonzeros,
        "column_names": tuple(column_names),
        "words": tuple(words),
    }


# --------------------------------------------------------------------------
# Phase 4: probe identities for cuts 5, 0, 1.
# --------------------------------------------------------------------------

def restriction(vector, probe_words):
    return {word: sp.expand(sp.sympify(vector[word]))
            for word in probe_words if word in vector}


def audit_probes(direction):
    c = direction
    blocks = internal_blocks(X_SYMBOLS, T, direction)
    sigma_words = (
        (0, 0, 0, 1, 1, 0), (0, 0, c, 1, 1, 0),
        (0, 0, 0, 1, 2, 0), (0, 0, c, 1, 2, 0),
    )
    records = {}

    columns5, labels5 = raw_columns(5, blocks)
    probe5 = E_WORDS + sigma_words + (
        (1, 2, 1, 2, 0, 0), (1, 2, 1, 2, 1, 0), (1, 2, 1, 2, 2, 0),
    )
    assert len(probe5) == 16
    full_pattern = {word: X_OF_CELL[cell]
                    for cell, word in zip(CELLS, E_WORDS)}
    full_pattern[(1, 2, 1, 2, 0, 0)] = sp.Integer(1)
    expected5 = {
        (4, 0, 0): full_pattern,
        (4, 1, 0): {
            (0, 0, 0, 1, 1, 0): X_OF_CELL[0, 1],
            (0, 0, c, 1, 1, 0): X_OF_CELL[c, 1],
            (1, 2, 1, 2, 1, 0): sp.Integer(1),
        },
        (4, 2, 0): {
            (0, 0, 0, 1, 2, 0): X_OF_CELL[0, 1],
            (0, 0, c, 1, 2, 0): X_OF_CELL[c, 1],
            (1, 2, 1, 2, 2, 0): sp.Integer(1),
        },
    }
    survivors5 = {}
    for column, label in zip(columns5, labels5):
        restricted = restriction(column, probe5)
        if restricted:
            survivors5[label] = restricted
    assert set(survivors5) == set(expected5), (direction, sorted(survivors5))
    for label, expected in expected5.items():
        difference = linear_combination(
            ((survivors5[label], 1), (expected, -1))
        )
        assert not difference, (direction, label, difference)
    records[5] = tuple(sorted(survivors5))

    probe01 = E_WORDS + sigma_words
    expected_pattern = {word: X_OF_CELL[cell]
                        for cell, word in zip(CELLS, E_WORDS)}
    survivor_label = {0: (1, 0, 0), 1: (0, 0, 0)}
    d_reps = d_boundary_representations()
    for cut in (0, 1):
        columns, labels = raw_columns(cut, blocks)
        survivors = {}
        for column, label in zip(columns, labels):
            restricted = restriction(column, probe01)
            if restricted:
                survivors[label] = restricted
        assert set(survivors) == {survivor_label[cut]}, (direction, cut,
                                                         sorted(survivors))
        difference = linear_combination((
            (survivors[survivor_label[cut]], 1), (expected_pattern, -1),
        ))
        assert not difference, (direction, cut, difference)
        by_label = dict(zip(labels, columns))
        combination = linear_combination(tuple(
            (by_label[label], coefficient)
            for label, coefficient in d_reps[cut]
        ))
        difference = linear_combination(
            ((combination, 1), (d_member(direction), -1))
        )
        assert not difference, (direction, cut, "D representation")
        records[cut] = (survivor_label[cut], tuple(
            label for label, _ in d_reps[cut]
        ))
    return records


# --------------------------------------------------------------------------
# Phase 5: the degenerate locus D_full and the [C4|D] minors.
# --------------------------------------------------------------------------

LOCUS_PARAMETERS = sp.symbols("a0 a1 a2 w u")


def audit_locus_parameterization(direction):
    a0, a1, a2, w, u = LOCUS_PARAMETERS
    generators = locus_generators(direction)
    values = locus_x_values(direction, a0, a1, a2, w, u, T)
    x_substitution = dict(zip(X_SYMBOLS, values))
    for generator in generators:
        assert sp.expand(generator.subs(x_substitution)) == 0

    # Backward: reconstruct parameters from an arbitrary X on the locus.
    other = 3 - direction
    m = {direction: X_OF_CELL[direction, 1] - T * X_OF_CELL[0, 1],
         other: X_OF_CELL[other, 1]}
    back = {1: m[1], 2: m[2]}
    rebuilt = locus_x_values(
        direction,
        X_OF_CELL[0, 0], X_OF_CELL[0, 1], X_OF_CELL[0, 2],
        back[1], back[2], T,
    )
    allowed = set()
    for generator in generators:
        allowed.add(sp.expand(generator))
        allowed.add(sp.expand(-generator))
    allowed.add(sp.Integer(0))
    for cell, value in zip(CELLS, rebuilt):
        difference = sp.expand(value - X_OF_CELL[cell])
        assert difference in allowed, (direction, cell, difference)


def audit_locus_membership(direction):
    """On D_full the tensor D is an explicit eight-column member of C4."""
    a0, a1, a2, w, u = LOCUS_PARAMETERS
    c = direction
    other = 3 - direction
    m = {1: w, 2: u}
    values = locus_x_values(direction, a0, a1, a2, w, u, T)
    blocks = internal_blocks(values, T, direction)
    columns, labels = raw_columns(4, blocks)
    by_label = dict(zip(labels, columns))
    representation = (
        ((1, 1, 1), sp.Integer(1)),
        ((0, 2, 2), sp.Integer(1)),
        ((5, 0, 0), sp.Integer(1)),
        ((3, 0, 0), -a0),
        ((3, 1, 0), -a1),
        ((3, 2, 0), -a2),
        ((2, c, 0), -m[c]),
        ((2, other, 0), -m[other]),
    )
    combination = linear_combination(tuple(
        (by_label[label], coefficient) for label, coefficient in representation
    ))
    difference = linear_combination(
        ((combination, 1), (d_member(direction), -1))
    )
    assert not difference, (direction, difference)
    return tuple(label for label, _ in representation)


def c4_minor_certificates(direction):
    """Four designed 43x43 minors of [C4|D] whose determinants come out as
    (up to sign) exactly the four generators of D_full, plus two seeded
    random-anchor minors as corroboration.

    The designed anchors are this audit's own: each kept C4 column has a
    signature word ((1,h,1,1,k,0), (0,0,h,1,k,0), (h,2,0,2,k,0),
    (1,2,1,2,k,h), (0,0,0,h,k,0) for h in {0,2}), and one obstruction word
    (0,0,e,b,0,0) with e in {c, 3-c}, b in {0,2} is appended.
    """
    other = 3 - direction
    blocks = internal_blocks(X_SYMBOLS, T, direction)
    columns, labels = raw_columns(4, blocks)
    dropped = {(3, 1, k) for k in COLOURS}
    kept = [(column, label) for column, label in zip(columns, labels)
            if label not in dropped]
    assert len(kept) == 42
    augmented = [d_member(direction)] + [column for column, _ in kept]
    words = sorted(set().union(*(set(v) for v in augmented)), reverse=True)
    word_index = {word: index for index, word in enumerate(words)}
    generators = locus_generators(direction)
    parameter_substitution = dict(zip(
        X_SYMBOLS,
        locus_x_values(direction, *LOCUS_PARAMETERS, T),
    ))

    base_rows = set()
    for h, k in product(COLOURS, repeat=2):
        base_rows |= {(1, h, 1, 1, k, 0), (0, 0, h, 1, k, 0),
                      (h, 2, 0, 2, k, 0), (1, 2, 1, 2, k, h)}
    for h in (0, 2):
        for k in COLOURS:
            base_rows.add((0, 0, 0, h, k, 0))
    assert len(base_rows) == 42 and base_rows <= set(words)
    obstruction_words = (
        ("x_other_0", (0, 0, other, 0, 0, 0)),
        ("x_other_2", (0, 0, other, 2, 0, 0)),
        ("t_line_0", (0, 0, direction, 0, 0, 0)),
        ("t_line_2", (0, 0, direction, 2, 0, 0)),
    )
    determinants = []
    records = []
    for name, obstruction in obstruction_words:
        rows = tuple(sorted(base_rows | {obstruction}, reverse=True))
        assert len(rows) == 43
        minor = [
            [sp.expand(sp.sympify(vector.get(word, 0)))
             for vector in augmented]
            for word in rows
        ]
        determinant = symbolic_matrix_det(minor)
        assert determinant != 0
        assert sp.expand(
            sp.expand(determinant).subs(parameter_substitution)
        ) == 0, (direction, name)
        determinants.append(determinant)
        records.append((name, obstruction, str(determinant)))
    signed = {sp.expand(det) for det in determinants}
    signed |= {sp.expand(-det) for det in determinants}
    for generator in generators:
        assert sp.expand(generator) in signed, (direction, generator)

    seen = {min(sp.srepr(det), sp.srepr(sp.expand(-det)))
            for det in determinants}
    for regime_index, regime in enumerate(("generic", "t_zero")):
        for seed in range(16):
            rng = random.Random(
                20260727 + 1000 * direction + 100 * regime_index + seed
            )
            substitution = {
                symbol: Q(rng.randint(-45, 45) or 7, rng.randint(2, 29))
                for symbol in X_SYMBOLS
            }
            substitution[T] = (Q(0) if regime == "t_zero"
                               else Q(rng.randint(-45, 45) or 3,
                                      rng.randint(2, 29)))
            if all(generator.subs(substitution) == 0
                   for generator in generators):
                continue
            dense = [[Q(0)] * 43 for _ in words]
            for column, vector in enumerate(augmented):
                for word, value in vector.items():
                    dense[word_index[word]][column] = to_rational(
                        sp.sympify(value), substitution
                    )
            priority = list(range(len(words)))
            rng.shuffle(priority)
            chosen = gauss_pivot_pairs(dense, 43, priority)
            if len(chosen) != 43:
                continue
            rows = tuple(sorted(row for row, _column in chosen))
            minor = [
                [sp.expand(sp.sympify(augmented[c].get(words[r], 0)))
                 for c in range(43)]
                for r in rows
            ]
            determinant = symbolic_matrix_det(minor)
            assert determinant != 0
            assert sp.expand(
                sp.expand(determinant).subs(parameter_substitution)
            ) == 0, (direction, regime, seed)
            key = min(sp.srepr(determinant), sp.srepr(sp.expand(-determinant)))
            if key not in seen:
                seen.add(key)
                determinants.append(determinant)
                records.append((f"seeded_{regime}_{seed}", rows,
                                str(determinant)))
                break
    assert len(determinants) == 6, (direction, len(determinants))
    return tuple(determinants), tuple(records)


# --------------------------------------------------------------------------
# Phase 6: numeric spot checks of equation (12), exact rationals only.
# --------------------------------------------------------------------------

def numeric_columns(cut, blocks):
    columns, _labels = raw_columns(cut, blocks)
    return tuple(
        {word: Q(value) for word, value in column.items()}
        for column in columns
    )


def numeric_member(member, t_value):
    return {word: Q(sp.Rational(sp.sympify(value).subs({T: t_value})))
            for word, value in member.items()
            if sp.sympify(value).subs({T: t_value}) != 0}


def spot_check_point(direction, tag, x_values, t_value, expected_dims):
    blocks = internal_blocks(x_values, t_value, direction)
    bases = {cut: rref_basis(numeric_columns(cut, blocks))[0]
             for cut in SIX}
    hs = matching_tensor(SIX, blocks)
    hs = {word: Q(value) for word, value in hs.items()}
    d_numeric = numeric_member(d_member(direction), t_value)
    members = tuple(
        numeric_member(member, t_value) for _name, member in w_members(direction)
    )
    for cut in SIX:
        assert in_span(hs, bases[cut]), (tag, cut)
    w_space = intersection_two(bases[2], bases[3])
    assert len(w_space) == 12, (tag, len(w_space))
    assert same_span(w_space, members), tag
    observed = {}
    for cut in FINAL_CUTS:
        normal = intersection_many(
            (bases[2], bases[3], bases[4], bases[cut])
        )
        observed[cut] = len(normal)
        assert len(normal) == expected_dims[cut], (tag, cut, len(normal))
        if expected_dims[cut] == 1:
            assert same_span(normal, (hs,)), (tag, cut)
        else:
            assert same_span(normal, (hs, d_numeric)), (tag, cut)
    return observed


def audit_spot_checks(direction):
    other = 3 - direction
    generic_x = (Q(2, 3), Q(-3, 7), Q(5, 11), Q(7, 13), Q(-1, 2),
                 Q(3, 5), Q(4, 9), Q(-5, 8), Q(9, 14))
    generators = locus_generators(direction)
    observed = {}

    def off_locus(x_values, t_value):
        substitution = dict(zip(X_SYMBOLS, x_values))
        substitution[T] = t_value
        return all(generator.subs(substitution) != 0
                   for generator in generators)

    assert off_locus(generic_x, Q(5, 7))
    observed["generic"] = spot_check_point(
        direction, "generic", generic_x, Q(5, 7), {5: 1, 0: 1, 1: 1}
    )
    locus_x = tuple(
        Q(sp.Rational(value))
        for value in locus_x_values(
            direction, Q(2, 3), Q(-3, 5), Q(5, 7), Q(7, 4), Q(-2, 9), Q(4, 9)
        )
    )
    observed["on_locus"] = spot_check_point(
        direction, "on_locus", locus_x, Q(4, 9), {5: 1, 0: 2, 1: 2}
    )
    observed["x_zero"] = spot_check_point(
        direction, "x_zero", (Q(0),) * 9, Q(3, 2), {5: 1, 0: 1, 1: 1}
    )
    assert off_locus(generic_x, Q(0))
    observed["t_zero_generic"] = spot_check_point(
        direction, "t_zero_generic", generic_x, Q(0), {5: 1, 0: 1, 1: 1}
    )
    locus_x_t0 = tuple(
        Q(sp.Rational(value))
        for value in locus_x_values(
            direction, Q(2, 3), Q(-3, 5), Q(5, 7), Q(7, 4), Q(-2, 9), Q(0)
        )
    )
    observed["t_zero_on_locus"] = spot_check_point(
        direction, "t_zero_on_locus", locus_x_t0, Q(0), {5: 1, 0: 2, 1: 2}
    )
    return observed


# --------------------------------------------------------------------------
# Phase 7: Singular certificates (radical membership and star packets).
# --------------------------------------------------------------------------

def singular_text(value):
    value = sp.expand(sp.sympify(value))
    return str(value).replace("**", "^")


def star_name(kind, boundary, site, colour):
    return f"{kind}{boundary}_{site}_{colour}"


def star_variables(active=ACTIVE):
    return tuple(
        star_name(kind, boundary, site, colour)
        for kind in ("q", "p")
        for boundary in reversed(active)
        for site in reversed(SIX)
        for colour in reversed(COLOURS)
    )


def beta_text(terms, a, b):
    pieces = []
    for left, lc, right, rc, coefficient in terms:
        factor = singular_text(coefficient)
        pieces.append(
            f"({factor})*{star_name('p', a, left, lc)}*"
            f"{star_name('q', b, right, rc)}"
        )
        pieces.append(
            f"({factor})*{star_name('p', a, right, rc)}*"
            f"{star_name('q', b, left, lc)}"
        )
    return "+".join(pieces) if pieces else "0"


def fibre_order(active):
    return tuple(reversed(tuple(product(active, repeat=2))))


def packet_generators(blocks, normal_members, active=ACTIVE):
    """normal_members: tuple of (scalar name prefix, tensor) pairs."""
    hs = matching_tensor(SIX, blocks)
    atoms = word_terms(blocks)
    coordinates = set(atoms) | set(hs) | {(colour,) * 6 for colour in active}
    for _prefix, tensor in normal_members:
        coordinates |= set(tensor)
    coordinates = tuple(sorted(coordinates, reverse=True))
    generators = []
    for a, b in fibre_order(active):
        for word in coordinates:
            pieces = []
            beta = beta_text(atoms.get(word, ()), a, b)
            if beta != "0":
                pieces.append(beta)
            if a == b and word == (a,) * 6:
                pieces.append("-1")
            for prefix, tensor in normal_members:
                value = tensor.get(word, 0)
                if value != 0:
                    pieces.append(f"-({singular_text(value)})*{prefix}{a}{b}")
            if pieces:
                generators.append("+".join(pieces))
    generators = list(dict.fromkeys(reversed(generators)))
    return generators, len(coordinates)


def assemble_program(names, generators):
    program = "ring R=0,(" + ",".join(names) + "),dp;\n"
    program += "option(redSB);\n"
    program += "ideal I=" + ",".join(generators) + ";\n"
    program += "ideal G=slimgb(I);\n"
    program += 'print("AUDIT_UNIT"); if(reduce(1,G)==0){1;}else{0;}\n'
    program += 'print("AUDIT_SIZE"); size(G);\n'
    return program


def line_packet_job(direction, invert_x00):
    if invert_x00:
        x_values = X_SYMBOLS
        parameter_names = tuple(
            str(symbol) for symbol in reversed(X_SYMBOLS)
        )
        prefix_names = ("y", "t")
    else:
        x_values = (sp.Integer(0),) + tuple(X_SYMBOLS[1:])
        parameter_names = tuple(
            str(symbol) for symbol in reversed(X_SYMBOLS[1:])
        )
        prefix_names = ("t",)
    blocks = internal_blocks(x_values, T, direction)
    hs = matching_tensor(SIX, blocks)
    generators, coordinates = packet_generators(blocks, (("s", hs),))
    if invert_x00:
        generators.append("1-y*x00")
    names = prefix_names + parameter_names + star_variables() + tuple(
        f"s{a}{b}" for a, b in fibre_order(ACTIVE)
    )
    program = assemble_program(names, generators)
    return {
        "name": f"line_c{direction}_" + ("x00_unit" if invert_x00
                                         else "x00_zero"),
        "coverage": "normals <H>: cut 5 always; cuts 0,1 off D_full",
        "claim": "note_unit",
        "variables": len(names),
        "coordinates": coordinates,
        "generators": len(generators),
        "program": program,
        "sha256": hashlib.sha256(program.encode()).hexdigest(),
    }


def plane_packet_job(direction, active=ACTIVE, point=None):
    """The D_full plane packet over target colours `active`.

    With point=None the six locus parameters stay polynomial variables (the
    note's program shape); a point dict {a: (...), w: .., u: .., t: ..}
    specializes the packet at exact rationals (used to corroborate the
    witness locus with a fast Singular run).
    """
    fibres = fibre_order(active)
    if point is None:
        a0, a1, a2, w, u = LOCUS_PARAMETERS
        t_value = T
        parameter_names = ("t", "u", "w", "a2", "a1", "a0")
        d_tensor = d_member(direction)
        tag = "dfull"
    else:
        a0, a1, a2 = (Q(value) for value in point["a"])
        w, u, t_value = Q(point["w"]), Q(point["u"]), Q(point["t"])
        parameter_names = ()
        d_tensor = {
            word: value
            for word, value in (
                (word, Q(sp.Rational(sp.sympify(coeff).subs({T: t_value}))))
                for word, coeff in d_member(direction).items()
            )
            if value != 0
        }
        tag = "witness_point"
    values = locus_x_values(direction, a0, a1, a2, w, u, t_value)
    blocks = internal_blocks(values, t_value, direction)
    hs = matching_tensor(SIX, blocks)
    generators, coordinates = packet_generators(
        blocks, (("g", hs), ("k", d_tensor)), active
    )
    names = parameter_names + star_variables(active) + tuple(
        f"g{a}{b}" for a, b in fibres
    ) + tuple(f"k{a}{b}" for a, b in fibres)
    program = assemble_program(names, generators)
    colour_tag = "".join(map(str, active))
    return {
        "name": f"plane_c{direction}_{tag}_colours{colour_tag}",
        "coverage": ("normals <H,D>: cuts 0,1 on D_full, "
                     f"target colours {active}"),
        "claim": ("note_unit" if point is None and active == ACTIVE
                  else "audit_nonunit" if point is not None
                  else "info"),
        "variables": len(names),
        "coordinates": coordinates,
        "generators": len(generators),
        "program": program,
        "sha256": hashlib.sha256(program.encode()).hexdigest(),
    }


WITNESS_POINT = {"a": (1, 0, 0), "w": 0, "u": 0, "t": 0}


def audit_plane_witness(direction):
    """Machine-check the explicit star witness proving the note's plane
    packet is NOT the unit ideal.

    On the sublocus {X = a0*E00, a0 != 0, t = 0} of D_full the tail
    identity gives H - D = a0*[0^6], so the pure colour-0 target lies in
    the normal <H,D>.  The assignment p^1_{3,1} = q^1_{5,1} = 1 (all other
    70 stars zero) with scalars g00 = -1/a0, k00 = 1/a0 (others zero) then
    satisfies every packet generator identically in a0."""
    a0 = sp.Symbol("a0")
    values = locus_x_values(direction, a0, 0, 0, 0, 0, 0)
    for generator in locus_generators(direction):
        substitution = dict(zip(X_SYMBOLS, values))
        substitution[T] = sp.Integer(0)
        assert sp.expand(generator.subs(substitution)) == 0
    blocks = internal_blocks(values, 0, direction)
    hs = matching_tensor(SIX, blocks)
    d_tensor = {word: sp.sympify(value).subs({T: 0})
                for word, value in d_member(direction).items()}
    d_tensor = {word: value for word, value in d_tensor.items() if value != 0}
    difference = linear_combination((
        (hs, 1), (d_tensor, -1), ({(0,) * 6: a0}, -1),
    ))
    assert not difference, difference
    atoms = word_terms(blocks)
    coordinates = sorted(
        set(atoms) | set(hs) | set(d_tensor)
        | {(colour,) * 6 for colour in ACTIVE},
        reverse=True,
    )
    p = {(boundary, site, colour): 0
         for boundary in ACTIVE for site in SIX for colour in COLOURS}
    q = dict(p)
    p[1, 3, 1] = 1
    q[1, 5, 1] = 1
    g = {(0, 0): -1 / a0, (0, 1): 0, (1, 0): 0, (1, 1): 0}
    k = {(0, 0): 1 / a0, (0, 1): 0, (1, 0): 0, (1, 1): 0}
    checked = 0
    for a, b in product(ACTIVE, repeat=2):
        for word in coordinates:
            beta = 0
            for left, lc, right, rc, coefficient in atoms.get(word, ()):
                beta += coefficient * (
                    p[a, left, lc] * q[b, right, rc]
                    + p[a, right, rc] * q[b, left, lc]
                )
            target = 1 if (a == b and word == (a,) * 6) else 0
            residual = sp.simplify(
                beta - target - g[a, b] * hs.get(word, 0)
                - k[a, b] * d_tensor.get(word, 0)
            )
            assert residual == 0, (direction, (a, b), word, residual)
            checked += 1
    return checked


def radical_jobs(direction, determinants):
    names = ("y", "t") + tuple(str(symbol) for symbol in reversed(X_SYMBOLS))
    jobs = []
    for index, generator in enumerate(locus_generators(direction)):
        generators = [singular_text(det) for det in determinants]
        generators.append(f"1-y*({singular_text(generator)})")
        program = assemble_program(names, generators)
        jobs.append({
            "name": f"radical_c{direction}_g{index}",
            "coverage": f"V(minors) inside V({singular_text(generator)})",
            "claim": "audit_unit",
            "variables": len(names),
            "coordinates": 0,
            "generators": len(generators),
            "program": program,
            "sha256": hashlib.sha256(program.encode()).hexdigest(),
        })
    return jobs


def marker(output, name):
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    return int(lines[lines.index(name) + 1])


def run_singular(program, timeout):
    """Run one Singular program; return (unit, gb_size, seconds)."""
    executable = shutil.which("Singular")
    if executable is None:
        raise SystemExit("Singular is required")
    started = time.monotonic()
    completed = subprocess.run(
        [executable, "-q"], input=program, text=True,
        capture_output=True, check=True, timeout=timeout,
    )
    if completed.stderr.strip():
        raise AssertionError(completed.stderr)
    unit = marker(completed.stdout, "AUDIT_UNIT")
    size = marker(completed.stdout, "AUDIT_SIZE")
    return unit, size, time.monotonic() - started


# --------------------------------------------------------------------------
# Ledgers and main.
# --------------------------------------------------------------------------

def ledger_hash(rows):
    return hashlib.sha256("\n".join(map(repr, rows)).encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--directions", default="1,2")
    parser.add_argument("--skip-numeric", action="store_true")
    parser.add_argument("--skip-singular", action="store_true")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--timeout", type=int, default=21600)
    args = parser.parse_args()
    directions = tuple(int(piece) for piece in args.directions.split(","))

    started_all = time.monotonic()
    rank_records = []
    minor_ledgers = {}

    for direction in directions:
        audit_eight_site(direction)
        print(f"PASS direction {direction}: literal eight-site "
              "endpoint-order identity (127 distinct rationals)", flush=True)
        audit_no_mixing(direction)
        print(f"PASS direction {direction}: no matching term mixes X and t "
              "(total degree <= 1 in all tensors, cofactors, 270 columns)",
              flush=True)

        w_record = audit_w_structure(direction)
        print(
            f"PASS direction {direction}: W structure -- "
            f"matrix {w_record['matrix_shape']}, "
            f"order {w_record['minor_order']}, "
            f"72x72 minor det {w_record['minor_det']} "
            f"({w_record['minor_nonzeros']} nonzeros), "
            "C2 rank 42, ker M3 >= 3, ker M4 >= 3, twelve members, "
            "identity readout, tail identity, H in all six cylinders",
            flush=True,
        )

        probe_records = audit_probes(direction)
        print(
            f"PASS direction {direction}: probes -- cut5 survivors "
            f"{probe_records[5]}, cut0 {probe_records[0]}, "
            f"cut1 {probe_records[1]}",
            flush=True,
        )

        audit_locus_parameterization(direction)
        locus_rep = audit_locus_membership(direction)
        determinants, minor_records = c4_minor_certificates(direction)
        minor_ledgers[direction] = determinants
        print(
            f"PASS direction {direction}: D_full parameterization both ways, "
            f"on-locus D in C4 via {locus_rep}, "
            f"{len(determinants)} distinct 43x43 minors of [C4|D] "
            "(four designed dets equal the D_full generators up to sign):",
            flush=True,
        )
        for name, anchor, determinant in minor_records:
            print(f"    {name} @ {anchor}: det = {determinant}", flush=True)

        rank_records.append((
            direction,
            w_record["matrix_shape"],
            w_record["duplicate_pairs"],
            w_record["minor_order"],
            w_record["minor_det"],
            w_record["minor_nonzeros"],
            tuple(w_record["column_names"][index]
                  for index in w_record["minor_cols"]),
            tuple(w_record["words"][index]
                  for index in w_record["minor_rows"]),
            probe_records[5], probe_records[0], probe_records[1],
            locus_rep,
            tuple(str(det) for det in determinants),
        ))

        if not args.skip_numeric:
            observed = audit_spot_checks(direction)
            print(
                f"PASS direction {direction}: exact rational spot checks of "
                f"equation (12): {observed}",
                flush=True,
            )
            rank_records.append((direction, "spot", tuple(sorted(
                (tag, tuple(sorted(dims.items())))
                for tag, dims in observed.items()
            ))))

        checked = audit_plane_witness(direction)
        print(
            f"FINDING direction {direction}: on the D_full sublocus "
            "{X = a0*E00, a0 != 0, t = 0} the tail identity gives "
            "H - D = a0*[0^6], the pure colour-0 target lies inside the "
            "normal <H,D>, and the explicit stars p1_3_1 = q1_5_1 = 1 "
            "(all 70 others 0) with scalars g00 = -1/a0, k00 = 1/a0 satisfy "
            f"every generator of the note's plane packet ({checked} "
            "equations verified symbolically in a0).  The note's claim "
            "that this program has reduced Groebner basis [1] is false.",
            flush=True,
        )
        rank_records.append((direction, "plane_witness", checked))

    full_configuration = (set(directions) == {1, 2}
                          and not args.skip_numeric)
    rank_digest = ledger_hash(rank_records)
    if EXPECTED_RANK_LEDGER_SHA256 and full_configuration:
        assert rank_digest == EXPECTED_RANK_LEDGER_SHA256, rank_digest
    print("RANK_LEDGER_SHA256", rank_digest, flush=True)

    jobs = []
    for direction in directions:
        jobs.extend(radical_jobs(direction, minor_ledgers[direction]))
        jobs.append(line_packet_job(direction, invert_x00=True))
        jobs.append(line_packet_job(direction, invert_x00=False))
        jobs.append(plane_packet_job(direction))
        jobs.append(plane_packet_job(direction, point=WITNESS_POINT))
        jobs.append(plane_packet_job(direction, active=(1, 2)))
    ideal_rows = tuple(
        (job["name"], job["coverage"], job["claim"], job["variables"],
         job["coordinates"], job["generators"], job["sha256"])
        for job in jobs
    )
    ideal_digest = ledger_hash(ideal_rows)
    if EXPECTED_IDEAL_LEDGER_SHA256 and full_configuration:
        assert ideal_digest == EXPECTED_IDEAL_LEDGER_SHA256, ideal_digest
    for row in ideal_rows:
        print("IDEAL", *row, flush=True)
    print("IDEAL_LEDGER_SHA256", ideal_digest, flush=True)

    if args.skip_singular:
        print("Singular phase skipped by request; audit incomplete "
              "(geometry PASS, plane-packet FINDING already established "
              "by the symbolic witness).", flush=True)
        sys.exit(2)

    jobs_by_name = {job["name"]: job for job in jobs}
    assert len(jobs_by_name) == len(jobs)

    def run_job(job):
        try:
            return run_singular(job["program"], args.timeout)
        except subprocess.TimeoutExpired:
            return None, None, float(args.timeout)

    started_exact = time.monotonic()
    results = {}
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(run_job, job): job["name"] for job in jobs
        }
        for future in as_completed(futures):
            name = futures[future]
            unit, size, seconds = future.result()
            results[name] = (unit, size, seconds)
            state = ("TIMEOUT" if unit is None
                     else f"unit={unit} gbsize={size}")
            print(f"UNIT {name} {state} seconds={seconds:.3f}", flush=True)
    exact_wall = time.monotonic() - started_exact

    findings = []
    for job in jobs:
        unit, size, _seconds = results[job["name"]]
        claim = job["claim"]
        if claim == "audit_unit":
            assert (unit, size) == (1, 1), (job["name"], unit, size)
        elif claim == "audit_nonunit":
            assert unit == 0, (job["name"], unit, size)
        elif claim == "note_unit" and (unit, size) != (1, 1):
            observed = ("no reduced basis within the time budget"
                        if unit is None
                        else f"observed unit={unit}, gbsize={size}")
            findings.append(
                f"{job['name']}: note claims reduced Groebner basis [1], "
                f"{observed}"
            )

    print("independent adjacent rank-one (E10,E20) geometry audit "
          "(sections 2-5, equation (12)): PASS")
    print("eight-site endpoint order, X/t separation, kernel relations: PASS")
    print("W = <e_ab, sigma1, sigma2, D> via constant unit 72-minors: PASS")
    print("probe tables for cuts 5,0,1 and D in C0,C1: PASS")
    print("D_full parameterization, on-locus D in C4, [C4|D] minors: PASS")
    print("exact rational spot checks of equation (12): PASS")
    print("8 radical certificates and 4 line packets, all unit: PASS")
    repair = [name for name, (unit, size, _s) in results.items()
              if name.endswith("colours12") and (unit, size) == (1, 1)]
    print(f"supplementary colours-(1,2) plane packets unit: {sorted(repair)}")
    print(f"rank ledger SHA256: {rank_digest}")
    print(f"ideal ledger SHA256: {ideal_digest}")
    print(f"maximum Singular time: "
          f"{max(seconds for _u, _g, seconds in results.values()):.3f}s")
    print(f"parallel Singular wall time: {exact_wall:.3f}s")
    print(f"independent total wall time: {time.monotonic()-started_all:.3f}s")
    if findings:
        for finding in findings:
            print("FINDING", finding, flush=True)
        print("AUDIT VERDICT: geometry claims confirmed; the section-6 "
              "plane-packet unit claim of the note FAILS (explicit witness "
              "above).  Exiting nonzero.", flush=True)
        sys.exit(2)
    print("AUDIT VERDICT: all note claims confirmed.")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as error:
        print(f"AUDIT FAIL: {error!r}", flush=True)
        sys.exit(1)
