#!/usr/bin/env python3
"""Clean-room exact audit of the adjacent E22 fourth-cut obstruction.

This checker imports no project module and consumes no matrix, normal, chart
program, or certificate emitted by the primary E22 implementation.  It
reconstructs endpoint-ordered matchings by a greatest-vertex recursion,
orders every cylinder column in reverse lexicographic endpoint order, uses
greatest-coordinate sparse elimination for numerical intersections, and
uses a reversed Singular variable/generator order.

The audited local family is

    A23 = arbitrary X,       A25 = E00 + t E22,

with the other seven displayed six-site cells fixed.  For t != 0 the script
checks the complete 512-support torus cover, uniform full-cylinder line
minors away from the exceptional {x01,x11,x21} locus, the eight exact true
normals on that locus, the all-X cut-5 ten-space/probe argument, literal
eight-site boundary fibres, and every characteristic-zero unit ideal.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from fractions import Fraction
from functools import lru_cache
import hashlib
from itertools import combinations, product
import shutil
import subprocess
import time

import sympy as sp


Q = Fraction
COLOURS = (0, 1, 2)
SIX = tuple(range(6))
EIGHT = tuple(range(8))
CELLS = tuple(product(COLOURS, repeat=2))
CELL_NAMES = tuple(f"x{a}{b}" for a, b in CELLS)
X00, X01, X02, X10, X11, X12, X20, X21, X22 = range(9)
ACTIVE = (0, 1)
FINAL_CUTS = (0, 1, 5)
OFF_ORDER = (X02, X10, X12, X20, X22)
EXCEPTIONAL = (X01, X11, X21)

# Every cell is endpoint ordered: the first colour belongs to the smaller
# endpoint.  In particular 35:E10 is not silently transposed.
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
MOVING_SOURCE = (2, 5, 2, 2)

E_WORDS = tuple((0, 0, a, b, 0, 0) for a, b in CELLS)
TAIL_PROBE = (1, 2, 1, 2, 0, 0)

# Filled after the first fully independent exact replay.  These constants
# freeze this audit's own differently ordered certificate ledgers.
EXPECTED_RANK_LEDGER_SHA256 = (
    "57277268d226e1b7b6b0469f2bacdda63700ed693d7c439d618ac2cf6543b84b"
)
EXPECTED_IDEAL_LEDGER_SHA256 = (
    "57bca13bbcf440d4b1a3425e0fe52988aa037a9a08ed1138eeb734454d646d36"
)


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


def subtract(left, right):
    return linear_combination(((left, 1), (right, -1)))


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


def internal_blocks(x_values, t_value):
    blocks = defaultdict(dict)
    for left, right, left_colour, right_colour in BASE_SOURCES:
        blocks[left, right][left_colour, right_colour] = 1
    if t_value != 0:
        left, right, left_colour, right_colour = MOVING_SOURCE
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
                coefficient *= value
            add(answer, tuple(word), coefficient)
    return answer


def raw_columns(cut, blocks):
    """Return 45 full cylinder columns in a reversed independent order."""
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
    """Expand the direct tensor along the internal edge incident to cut."""
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


def vector_key(vector):
    return tuple(
        (word, sp.srepr(sp.expand(value)))
        for word, value in sorted(vector.items(), reverse=True)
    )


def independent_c2_columns(columns, labels):
    """Drop the earlier member of each literal duplicate pair."""
    latest = {}
    for index, vector in enumerate(columns):
        latest[vector_key(vector)] = index
    selected = tuple(sorted(latest.values(), reverse=True))
    assert len(selected) == 42
    duplicate_classes = defaultdict(list)
    for index, vector in enumerate(columns):
        duplicate_classes[vector_key(vector)].append(index)
    assert sorted(len(indices) for indices in duplicate_classes.values()).count(2) == 3
    assert all(len(indices) in (1, 2) for indices in duplicate_classes.values())
    return selected, tuple(labels[index] for index in selected)


def symbolic_values(assignments):
    return tuple(assignments.get(index, 0) for index in range(9))


def simultaneous_matrix(blocks, final_cut):
    cut_order = (final_cut, 4, 3)
    data = {cut: raw_columns(cut, blocks) for cut in (2,) + cut_order}
    selected2, _selected_labels = independent_c2_columns(*data[2])
    column_labels = tuple((2, data[2][1][index]) for index in selected2)
    for cut in cut_order:
        column_labels += tuple(
            (cut, data[cut][1][index]) for index in range(44, -1, -1)
        )
    row_labels = []
    for comparison in cut_order:
        coordinates = set().union(
            *(set(column) for column in data[2][0]),
            *(set(column) for column in data[comparison][0]),
        )
        row_labels.extend((comparison, word) for word in sorted(coordinates, reverse=True))
    row_labels = tuple(row_labels)
    row_index = {label: index for index, label in enumerate(row_labels)}
    matrix = sp.MutableSparseMatrix(len(row_labels), len(column_labels), {})
    for column_index, (cut, label) in enumerate(column_labels):
        columns, labels = data[cut]
        local_index = labels.index(label)
        vector = columns[local_index]
        if cut == 2:
            for comparison in cut_order:
                for word, coefficient in vector.items():
                    matrix[row_index[comparison, word], column_index] = -coefficient
        else:
            for word, coefficient in vector.items():
                matrix[row_index[cut, word], column_index] = coefficient
    assert matrix.shape[1] == 177
    return sp.ImmutableSparseMatrix(matrix), row_labels, column_labels, data


def two_cylinder_matrix(blocks):
    data = {cut: raw_columns(cut, blocks) for cut in (2, 3)}
    selected2, _selected_labels = independent_c2_columns(*data[2])
    column_labels = tuple((3, data[3][1][index]) for index in range(44, -1, -1))
    column_labels += tuple((2, data[2][1][index]) for index in selected2)
    coordinates = sorted(set().union(
        *(set(column) for column in data[2][0] + data[3][0])
    ), reverse=True)
    row_index = {word: index for index, word in enumerate(coordinates)}
    matrix = sp.MutableSparseMatrix(len(coordinates), len(column_labels), {})
    for column_index, (cut, label) in enumerate(column_labels):
        columns, labels = data[cut]
        local_index = labels.index(label)
        sign = 1 if cut == 3 else -1
        for word, coefficient in columns[local_index].items():
            matrix[row_index[word], column_index] = sign * coefficient
    assert matrix.shape == (108, 87)
    return sp.ImmutableSparseMatrix(matrix), tuple(coordinates), column_labels, data


def select_constant_minor(matrix, parameters, expected_rank):
    numeric = matrix.subs({parameter: 0 for parameter in parameters})
    _rref, columns = numeric.rref()
    assert len(columns) == expected_rank, len(columns)
    restricted = numeric[:, columns]
    _rref_t, rows = restricted.T.rref()
    assert len(rows) == expected_rank, len(rows)
    symbolic_minor = matrix.extract(rows, columns)
    determinant = sp.factor(symbolic_minor.det(method="domain-ge"))
    assert determinant in (1, -1), determinant
    return tuple(rows), tuple(columns), symbolic_minor, determinant


def certificate_hash(row_labels, column_labels, rows, columns):
    payload = repr((
        tuple(row_labels[index] for index in rows),
        tuple(column_labels[index] for index in columns),
    ))
    return hashlib.sha256(payload.encode()).hexdigest()


def rref_basis(vectors, coordinates=None):
    """Greatest-coordinate exact sparse Gauss--Jordan basis."""
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


def cylinder_basis(cut, blocks):
    columns, _labels = raw_columns(cut, blocks)
    return rref_basis(columns)[0]


def normal_for(blocks, final_cut):
    return intersection_many(tuple(
        cylinder_basis(cut, blocks) for cut in (2, 3, 4, final_cut)
    ))


def rational_matrix_rank(rows):
    return rank(tuple(
        {index: Q(value) for index, value in enumerate(row) if value}
        for row in rows
    ))


def rational_nullspace(rows, width):
    sparse = tuple(
        {index: Q(value) for index, value in enumerate(row) if value}
        for row in rows
    )
    dual = annihilator(sparse, tuple(range(width - 1, -1, -1)))
    return tuple(tuple(vector.get(index, Q(0)) for index in range(width))
                 for vector in dual)


def character_data():
    coordinate = {(site, colour): 3 * site + colour
                  for site in SIX for colour in COLOURS}
    fixed_rows = []
    for left, right, left_colour, right_colour in BASE_SOURCES:
        row = [0] * 18
        row[coordinate[left, left_colour]] = 1
        row[coordinate[right, right_colour]] = 1
        fixed_rows.append(tuple(row))
    assert rational_matrix_rank(fixed_rows) == 8
    kernel = rational_nullspace(fixed_rows, 18)
    assert len(kernel) == 10

    def character(source):
        left, right, left_colour, right_colour = source
        return tuple(
            vector[coordinate[left, left_colour]]
            + vector[coordinate[right, right_colour]]
            for vector in kernel
        )

    x_rows = tuple(character((2, 3, a, b)) for a, b in CELLS)
    t_row = character(MOVING_SOURCE)
    assert rational_matrix_rank(x_rows) == 5
    assert rational_matrix_rank(x_rows + (t_row,)) == 6
    for mask in range(1 << 9):
        selected = tuple(x_rows[index] for index in range(9)
                         if mask & (1 << index))
        assert rational_matrix_rank(selected + (t_row,)) == \
            rational_matrix_rank(selected) + 1
    return x_rows, t_row


def audit_torus_cover():
    x_rows, t_row = character_data()
    counts = defaultdict(int)
    representatives = []
    for mask in range(1 << 9):
        if mask & (1 << X00):
            counts["x00_open"] += 1
            chart = "x00_open"
        else:
            pivot = next((bit for bit in OFF_ORDER if mask & (1 << bit)), None)
            if pivot is None:
                counts["exceptional"] += 1
                chart = "exceptional"
            else:
                counts[CELL_NAMES[pivot]] += 1
                chart = CELL_NAMES[pivot]
        representatives.append((mask, chart))
    expected = {
        "x00_open": 256,
        "x02": 128,
        "x10": 64,
        "x12": 32,
        "x20": 16,
        "x22": 8,
        "exceptional": 8,
    }
    assert dict(counts) == expected
    assert rational_matrix_rank((x_rows[X00], t_row)) == 2
    for pivot in OFF_ORDER:
        assert rational_matrix_rank((x_rows[pivot], t_row)) == 2
    for mask in range(1 << len(EXCEPTIONAL)):
        support = tuple(EXCEPTIONAL[index] for index in range(3)
                        if mask & (1 << index))
        rows = tuple(x_rows[index] for index in support) + (t_row,)
        assert rational_matrix_rank(rows) == len(rows)
    return expected, tuple(representatives)


def delta_map(one, zero):
    return {key: value for key in set(one) | set(zero)
            if (value := one.get(key, 0) - zero.get(key, 0)) != 0}


def audit_affinity():
    zero = (0,) * 9
    base00 = internal_blocks(zero, 0)
    for index in range(9):
        one = tuple(1 if bit == index else 0 for bit in range(9))
        for vertices in (SIX,) + tuple(
            tuple(site for site in SIX if site not in pair)
            for pair in combinations(SIX, 2)
        ):
            f11 = matching_tensor(vertices, internal_blocks(one, 1))
            f10 = matching_tensor(vertices, internal_blocks(one, 0))
            f01 = matching_tensor(vertices, internal_blocks(zero, 1))
            f00 = matching_tensor(vertices, base00)
            assert not delta_map(delta_map(f11, f10), delta_map(f01, f00))
        for cut in SIX:
            c11, _ = raw_columns(cut, internal_blocks(one, 1))
            c10, _ = raw_columns(cut, internal_blocks(one, 0))
            c01, _ = raw_columns(cut, internal_blocks(zero, 1))
            c00, _ = raw_columns(cut, base00)
            for vectors in zip(c11, c10, c01, c00):
                assert not delta_map(
                    delta_map(vectors[0], vectors[1]),
                    delta_map(vectors[2], vectors[3]),
                )
    dense = tuple(Q(index + 2, index + 3) for index in range(9))
    for vertices in (SIX,) + tuple(
        tuple(site for site in SIX if site not in pair)
        for pair in combinations(SIX, 2)
    ):
        f0 = matching_tensor(vertices, internal_blocks(dense, Q(0)))
        f1 = matching_tensor(vertices, internal_blocks(dense, Q(1)))
        f2 = matching_tensor(vertices, internal_blocks(dense, Q(2)))
        assert f2 == linear_combination(((f1, 2), (f0, -1)))


def audit_literal_eight_site_identity():
    x_values = tuple(Q(101 + index, 103 + index) for index in range(9))
    t_value = Q(17, 19)
    interior = internal_blocks(x_values, t_value)
    p = {(a, site, colour): Q(1001 + 100 * a + 10 * site + colour, 997)
         for a in COLOURS for site in SIX for colour in COLOURS}
    q = {(b, site, colour): Q(2003 + 100 * b + 10 * site + colour, 991)
         for b in COLOURS for site in SIX for colour in COLOURS}
    r = {(a, b): Q(3001 + 10 * a + b, 983)
         for a in COLOURS for b in COLOURS}
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
        assert observed == expected


def x00_chart():
    parameters = sp.symbols("u22 u21 u20 u12 u11 u10 u02 u01")
    # Names are deliberately assigned in reverse cell order.
    bits = (X22, X21, X20, X12, X11, X10, X02, X01)
    assignments = {X00: sp.Integer(1)}
    assignments.update(zip(bits, parameters))
    return "x00_open", (), bits, parameters, internal_blocks(
        symbolic_values(assignments), sp.Integer(1)
    )


def off_chart(pivot):
    position = OFF_ORDER.index(pivot)
    forced_zero = (X00,) + OFF_ORDER[:position]
    parameter_bits = tuple(bit for bit in range(8, 0, -1)
                           if bit != pivot and bit not in forced_zero)
    parameters = sp.symbols(" ".join("u" + CELL_NAMES[bit][1:]
                                      for bit in parameter_bits))
    if not isinstance(parameters, tuple):
        parameters = (parameters,)
    assignments = {pivot: sp.Integer(1)}
    assignments.update(zip(parameter_bits, parameters))
    return CELL_NAMES[pivot], forced_zero, parameter_bits, parameters, internal_blocks(
        symbolic_values(assignments), sp.Integer(1)
    )


def audit_line_rank_certificates():
    records = []
    charts = [x00_chart()] + [off_chart(pivot) for pivot in OFF_ORDER]
    for chart_index, chart in enumerate(charts):
        name, _zero_bits, _parameter_bits, parameters, blocks = chart
        cuts = FINAL_CUTS if chart_index == 0 else (0, 1)
        hs = matching_tensor(SIX, blocks)
        assert hs.get(TAIL_PROBE) == 1
        for cut in cuts:
            matrix, row_labels, column_labels, data = simultaneous_matrix(blocks, cut)
            rows, columns, minor, determinant = select_constant_minor(
                matrix, parameters, 176
            )
            for cylinder_cut, (raw, labels) in data.items():
                assert direct_representation(cylinder_cut, blocks, raw, labels) == hs
            record = (
                name,
                cut,
                matrix.shape,
                minor.shape,
                len(minor.todok()),
                str(determinant),
                certificate_hash(row_labels, column_labels, rows, columns),
            )
            records.append(record)
    digest = hashlib.sha256("\n".join(map(repr, records)).encode()).hexdigest()
    return tuple(records), digest, tuple(charts)


def audit_cut5_uniform():
    parameters = sp.symbols("v22 v21 v20 v12 v11 v10 v02 v01 v00")
    bits = (X22, X21, X20, X12, X11, X10, X02, X01, X00)
    assignments = dict(zip(bits, parameters))
    blocks = internal_blocks(symbolic_values(assignments), sp.Integer(1))
    hs = matching_tensor(SIX, blocks)
    zero_blocks = internal_blocks((0,) * 9, sp.Integer(1))
    tail = matching_tensor(SIX, zero_blocks)
    expected_hs = dict(tail)
    for bit, word in enumerate(E_WORDS):
        add(expected_hs, word, assignments[bit])
    assert hs == expected_hs
    assert tail.get(TAIL_PROBE) == 1
    assert set(E_WORDS).isdisjoint(tail)

    matrix, row_labels, column_labels, data = two_cylinder_matrix(blocks)
    rows, columns, minor, determinant = select_constant_minor(matrix, parameters, 77)
    for cut, (raw, labels) in data.items():
        assert direct_representation(cut, blocks, raw, labels) == hs
        for word in E_WORDS:
            assert any(column == {word: 1} for column in raw)

    # The ten displayed vectors are independent and lie in C2 cap C3.  The
    # relation kernel has dimension at most 87-77=10, so this is the whole
    # intersection, even on parameter rank-jump loci.
    w_basis = tuple({word: 1} for word in E_WORDS) + (tail,)
    assert rank(w_basis) == 10

    columns5, labels5 = raw_columns(5, blocks)
    assert direct_representation(5, blocks, columns5, labels5) == hs
    probe = E_WORDS + (TAIL_PROBE,)
    restrictions = tuple(
        {word: vector[word] for word in probe if word in vector}
        for vector in columns5
    )
    nonzero = tuple(index for index, vector in enumerate(restrictions) if vector)
    assert len(nonzero) == 1
    expected_probe = {TAIL_PROBE: 1}
    for bit, word in enumerate(E_WORDS):
        expected_probe[word] = assignments[bit]
    assert restrictions[nonzero[0]] == expected_probe

    record = (
        "cut5_all_X",
        matrix.shape,
        minor.shape,
        len(minor.todok()),
        str(determinant),
        certificate_hash(row_labels, column_labels, rows, columns),
        nonzero,
        labels5[nonzero[0]],
    )
    return record


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


def singular_text(value):
    value = sp.cancel(value)
    if value == 0:
        return "0"
    return str(value).replace("**", "^")


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


def line_program(blocks, parameters):
    hs = matching_tensor(SIX, blocks)
    atoms = word_terms(blocks)
    coordinates = tuple(sorted(
        set(atoms) | set(hs) | {(colour,) * 6 for colour in ACTIVE},
        reverse=True,
    ))
    generators = []
    fibres = tuple(reversed(tuple(product(ACTIVE, repeat=2))))
    for a, b in fibres:
        scalar = f"s{a}{b}"
        for word in coordinates:
            pieces = []
            beta = beta_text(atoms.get(word, ()), a, b)
            if beta != "0":
                pieces.append(beta)
            if a == b and word == (a,) * 6:
                pieces.append("-1")
            if word in hs:
                pieces.append(f"-({singular_text(hs[word])})*{scalar}")
            if pieces:
                generators.append("+".join(pieces))
    generators = list(dict.fromkeys(reversed(generators)))
    names = tuple(str(parameter) for parameter in reversed(parameters))
    names += star_variables()
    names += tuple(f"s{a}{b}" for a, b in fibres)
    program = "ring R=0,(" + ",".join(names) + "),dp;\n"
    program += "option(redSB);\n"
    program += "ideal I=" + ",".join(generators) + ";\n"
    program += "ideal G=slimgb(I);\n"
    program += 'print("AUDIT_UNIT"); if(reduce(1,G)==0){1;}else{0;}\n'
    program += 'print("AUDIT_SIZE"); size(G);\n'
    return program, len(generators), len(names), len(coordinates)


def numeric_beta_terms(atoms, a, b, functional):
    pieces = []
    constant = Q(0)
    for word, multiplier in functional.items():
        for left, lc, right, rc, coefficient in atoms.get(word, ()):
            factor = multiplier * coefficient
            pieces.append(
                f"({singular_text(factor)})*{star_name('p', a, left, lc)}*"
                f"{star_name('q', b, right, rc)}"
            )
            pieces.append(
                f"({singular_text(factor)})*{star_name('p', a, right, rc)}*"
                f"{star_name('q', b, left, lc)}"
            )
        if a == b and word == (a,) * 6:
            constant -= multiplier
    if constant:
        pieces.append(singular_text(constant))
    return "+".join(pieces) if pieces else "0"


def normal_program(blocks, normal):
    atoms = word_terms(blocks)
    coordinates = tuple(sorted(
        set(atoms) | set().union(*(set(row) for row in normal))
        | {(colour,) * 6 for colour in ACTIVE},
        reverse=True,
    ))
    dual = annihilator(normal, coordinates)
    generators = []
    fibres = tuple(reversed(tuple(product(ACTIVE, repeat=2))))
    for a, b in fibres:
        for functional in reversed(dual):
            expression = numeric_beta_terms(atoms, a, b, functional)
            if expression != "0":
                generators.append(expression)
    generators = list(dict.fromkeys(reversed(generators)))
    names = star_variables()
    program = "ring R=0,(" + ",".join(names) + "),dp;\n"
    program += "option(redSB);\n"
    program += "ideal I=" + ",".join(generators) + ";\n"
    program += "ideal G=slimgb(I);\n"
    program += 'print("AUDIT_UNIT"); if(reduce(1,G)==0){1;}else{0;}\n'
    program += 'print("AUDIT_SIZE"); size(G);\n'
    return program, len(generators), len(names), len(coordinates), len(dual)


def exceptional_supports():
    for mask in range(1 << len(EXCEPTIONAL)):
        yield tuple(EXCEPTIONAL[index] for index in range(3)
                    if mask & (1 << index))


def audit_exceptional_normals_and_jobs():
    jobs = []
    records = []
    for support in exceptional_supports():
        x_values = tuple(Q(1) if index in support else Q(0) for index in range(9))
        blocks = internal_blocks(x_values, Q(1))
        hs = matching_tensor(SIX, blocks)
        normals = {cut: normal_for(blocks, cut) for cut in FINAL_CUTS}
        expected01 = 2 if support else 1
        assert len(normals[0]) == len(normals[1]) == expected01
        assert len(normals[5]) == 1
        assert same_span(normals[0], normals[1])
        assert all(in_span(hs, normal) for normal in normals.values())
        assert all(
            not in_span({(colour,) * 6: Q(1)}, normal)
            for normal in normals.values() for colour in ACTIVE
        )
        assert same_span(normals[5], (hs,))
        for cut in FINAL_CUTS:
            program, generators, variables, coordinates, dual_dimension = \
                normal_program(blocks, normals[cut])
            name = "exceptional_" + (
                "zero" if not support else "_".join(CELL_NAMES[bit] for bit in support)
            )
            job = {
                "name": name,
                "coverage": f"cut_{cut}",
                "support": support,
                "cut": cut,
                "normal_dimension": len(normals[cut]),
                "dual_dimension": dual_dimension,
                "generators": generators,
                "variables": variables,
                "coordinates": coordinates,
                "program": program,
                "sha256": hashlib.sha256(program.encode()).hexdigest(),
            }
            jobs.append(job)
            records.append((support, cut, len(normals[cut]), coordinates,
                            dual_dimension, generators, job["sha256"]))
    assert len(jobs) == 24
    return tuple(records), tuple(jobs)


def build_all_ideal_jobs(charts):
    jobs = []
    for name, _zero_bits, _parameter_bits, parameters, blocks in charts:
        program, generators, variables, coordinates = line_program(blocks, parameters)
        jobs.append({
            "name": name,
            "coverage": "cuts_0_1_5",
            "normal_dimension": 1,
            "generators": generators,
            "variables": variables,
            "coordinates": coordinates,
            "program": program,
            "sha256": hashlib.sha256(program.encode()).hexdigest(),
        })
    exceptional_records, exceptional_jobs = audit_exceptional_normals_and_jobs()
    jobs.extend(exceptional_jobs)
    assert len(jobs) == 30
    return tuple(jobs), exceptional_records


def ideal_ledger_hash(jobs):
    rows = tuple((
        job["name"], job["coverage"], job["normal_dimension"],
        job["variables"], job["coordinates"], job["generators"], job["sha256"],
    ) for job in jobs)
    return hashlib.sha256("\n".join(map(repr, rows)).encode()).hexdigest()


def marker(output, name):
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    return int(lines[lines.index(name) + 1])


def run_singular(program, timeout):
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
    assert (unit, size) == (1, 1), (unit, size, completed.stdout[-1000:])
    return time.monotonic() - started


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--geometry-only", action="store_true")
    parser.add_argument("--skip-ranks", action="store_true")
    parser.add_argument("--skip-singular", action="store_true")
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--timeout", type=int, default=3600)
    args = parser.parse_args()

    started_all = time.monotonic()
    counts, representatives = audit_torus_cover()
    assert len(representatives) == 512
    audit_affinity()
    audit_literal_eight_site_identity()
    print("GEOMETRY", "pass=1", "support_counts=" + repr(counts), flush=True)
    if args.geometry_only:
        return

    rank_records = ()
    rank_digest = "skipped"
    charts = tuple([x00_chart()] + [off_chart(pivot) for pivot in OFF_ORDER])
    if not args.skip_ranks:
        rank_records, rank_digest, charts = audit_line_rank_certificates()
        cut5_record = audit_cut5_uniform()
        combined = rank_records + (cut5_record,)
        rank_digest = hashlib.sha256("\n".join(map(repr, combined)).encode()).hexdigest()
        if EXPECTED_RANK_LEDGER_SHA256:
            assert rank_digest == EXPECTED_RANK_LEDGER_SHA256, rank_digest
        for record in combined:
            print("RANK", repr(record), flush=True)
        print("RANK_LEDGER_SHA256", rank_digest, flush=True)

    jobs, exceptional_records = build_all_ideal_jobs(charts)
    ideal_digest = ideal_ledger_hash(jobs)
    if EXPECTED_IDEAL_LEDGER_SHA256:
        assert ideal_digest == EXPECTED_IDEAL_LEDGER_SHA256, ideal_digest
    programs = {}
    for job in jobs:
        programs.setdefault(job["sha256"], job["program"])
    assert len(programs) == 21, len(programs)
    print("EXCEPTIONAL_NORMALS", repr(exceptional_records), flush=True)
    print("IDEAL_LEDGER", f"jobs={len(jobs)}", f"unique={len(programs)}",
          f"sha256={ideal_digest}", flush=True)
    for job in jobs:
        print(
            "IDEAL", job["name"], job["coverage"],
            f"N={job['normal_dimension']}", f"variables={job['variables']}",
            f"coordinates={job['coordinates']}",
            f"generators={job['generators']}", f"sha256={job['sha256']}",
            flush=True,
        )
    if args.skip_singular:
        return

    started_exact = time.monotonic()
    elapsed = {}
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(run_singular, program, args.timeout): digest
            for digest, program in programs.items()
        }
        for future in as_completed(futures):
            digest = futures[future]
            elapsed[digest] = future.result()
            print("UNIT", digest, f"seconds={elapsed[digest]:.3f}", flush=True)
    exact_wall = time.monotonic() - started_exact
    print("independent adjacent-E22 full-cylinder audit: PASS")
    print("t=0 inherited literally; t!=0 normalized without an X modulus: PASS")
    print("512 supports covered exactly as 256+128+64+32+16+8+8: PASS")
    print("13 constant rank-176 minors and all-X cut-5 rank-77/probe: PASS")
    print("eight true exceptional normals for cuts 0,1,5: PASS")
    print("all nine literal boundary fibres, shared stars, arbitrary A67: PASS")
    print("30 chart/cut jobs and 21 exact characteristic-zero units: PASS")
    print(f"rank ledger SHA256: {rank_digest}")
    print(f"ideal ledger SHA256: {ideal_digest}")
    print(f"maximum Singular time: {max(elapsed.values()):.3f}s")
    print(f"parallel Singular wall time: {exact_wall:.3f}s")
    print(f"independent total wall time: {time.monotonic()-started_all:.3f}s")


if __name__ == "__main__":
    main()
