#!/usr/bin/env python3
"""Audit the triangle-local cross-word observation module for N=8.

For T={0,1,2}, fix the colours on T.  Every perfect matching uses either
zero or one internal T-edge.  The 243 equations indexed by the colours on
O={3,4,5,6,7} are consequently affine-linear in exactly three source
cells, one on each internal T-edge.  This checker reconstructs that split
from literal perfect matchings, verifies its source labels, and profiles the
three-column systems on the frozen W40 and W25 controls.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path


sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "results_triangle_crossword_observation.json"
W40_PATH = ROOT / "computations/unaudited-x4general-w40-2026-08-20/results_t3.json"
W25_PATH = (ROOT / "computations/unaudited-x3core-w25-2026-08-15"
            / "OBJECT_W25-F8_n8_allblocked_X3.json")
W40_SHA = "30ad242d62b5cb905858842ce4e8255b105862dc21a65c73c080557fa8c1617f"
W25_SHA = "46d6e207e392deaa7e0bfc4221c7f5cc6735f11a2a14cc388292ca6850dd33f6"

SITES = tuple(range(8))
COLORS = tuple(range(3))
T = (0, 1, 2)
O = (3, 4, 5, 6, 7)
T_EDGES = ((0, 1), (0, 2), (1, 2))
CAP_PAIR = (6, 7)
TRIANGLE_OUTSIDE_EDGES = tuple(
    edge for edge in itertools.combinations(range(6), 2)
    if edge not in T_EDGES
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for index in range(1, len(vertices)):
        v = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for matching in perfect_matchings(rest):
            yield ((u, v),) + matching


MATCHINGS = tuple(perfect_matchings(SITES))
require(len(MATCHINGS) == 105, len(MATCHINGS))


def stored_cell(u: int, v: int, a: int, b: int) -> str:
    if u < v:
        return f"A_{u}{v}[{a},{b}]"
    return f"A_{v}{u}[{b},{a}]"


def monomial(matching, word):
    return tuple(sorted(stored_cell(u, v, word[u], word[v]) for u, v in matching))


def internal_edge(matching):
    edges = [tuple(sorted(edge)) for edge in matching if edge[0] in T and edge[1] in T]
    require(len(edges) <= 1, (matching, edges))
    return edges[0] if edges else None


def rank(rows, width):
    work = [list(row) for row in rows if any(row)]
    pivot_row = 0
    for column in range(width):
        pivot = next((r for r in range(pivot_row, len(work))
                      if work[r][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for r in range(len(work)):
            if r == pivot_row or not work[r][column]:
                continue
            value = work[r][column]
            work[r] = [a - value * b for a, b in zip(work[r], work[pivot_row])]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def det3(matrix):
    return (
        matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )


def abstract_incidence_slice(h01, h02, h12):
    """Return the exact 27x27 slice from its three cofactor vectors."""
    columns = [
        (edge, a, b)
        for edge in T_EDGES
        for a in COLORS
        for b in COLORS
    ]
    index = {label: column for column, label in enumerate(columns)}
    rows = []
    for a, b, c in itertools.product(COLORS, repeat=3):
        row = [Fraction(0) for _ in columns]
        row[index[((0, 1), a, b)]] = h01[c]
        row[index[((0, 2), a, c)]] = h02[b]
        row[index[((1, 2), b, c)]] = h12[a]
        rows.append(tuple(row))
    return tuple(rows), tuple(columns)


def exact_three_word_model():
    """Audit the generic 19 -> 26 -> 27 holonomy formula over Q."""
    triples = (
        ((1, 2, 3), (4, 5, 7), (8, 11, 13)),
        ((2, 5, 11), (3, 7, 17), (19, 23, 29)),
        ((31, 37, 41), (43, 47, 53), (59, 61, 67)),
    )
    triples = tuple(tuple(tuple(Fraction(x) for x in vector) for vector in packet)
                    for packet in triples)
    slices = [abstract_incidence_slice(*packet)[0] for packet in triples]
    ladder = [
        rank(slices[0], 27),
        rank(slices[0] + slices[1], 27),
        rank(slices[0] + slices[1] + slices[2], 27),
    ]
    require(ladder == [19, 26, 27], ladder)

    u0, v0, w0 = triples[0]
    u1, v1, w1 = triples[1]
    alpha = tuple(u1[c] / u0[c] for c in COLORS)
    beta = tuple(v1[b] / v0[b] for b in COLORS)
    gamma = tuple(w1[a] / w0[a] for a in COLORS)
    kernel = {}
    for a, b in itertools.product(COLORS, repeat=2):
        kernel[((0, 1), a, b)] = v0[b] * w0[a] * (gamma[a] - beta[b])
    for a, c in itertools.product(COLORS, repeat=2):
        kernel[((0, 2), a, c)] = u0[c] * w0[a] * (alpha[c] - gamma[a])
    for b, c in itertools.product(COLORS, repeat=2):
        kernel[((1, 2), b, c)] = u0[c] * v0[b] * (beta[b] - alpha[c])
    columns = abstract_incidence_slice(*triples[0])[1]
    vector = tuple(kernel[column] for column in columns)
    require(any(vector), vector)
    require(all(sum(x * y for x, y in zip(row, vector)) == 0
                for row in slices[0] + slices[1]), "two-word kernel formula")

    delta = tuple(triples[2][0][c] / u0[c] for c in COLORS)
    epsilon = tuple(triples[2][1][b] / v0[b] for b in COLORS)
    zeta = tuple(triples[2][2][a] / w0[a] for a in COLORS)
    witness = None
    for a, b, c in itertools.product(COLORS, repeat=3):
        normalized = det3((
            (Fraction(1), Fraction(1), Fraction(1)),
            (alpha[c], beta[b], gamma[a]),
            (delta[c], epsilon[b], zeta[a]),
        ))
        cleared = det3((
            (u0[c], v0[b], w0[a]),
            (u1[c], v1[b], w1[a]),
            (triples[2][0][c], triples[2][1][b], triples[2][2][a]),
        ))
        require(cleared == u0[c] * v0[b] * w0[a] * normalized,
                (a, b, c, cleared, normalized))
        row_index = a * 9 + b * 3 + c
        evaluation = sum(slices[2][row_index][j] * vector[j] for j in range(27))
        require(evaluation == u0[c] * v0[b] * w0[a] * normalized,
                (a, b, c, evaluation, normalized))
        if cleared and witness is None:
            witness = {"triangle_word": f"{a}{b}{c}", "determinant": str(cleared)}
    require(witness is not None, "generic holonomy must be nonzero")

    # An affine third packet has zero holonomy and leaves the common kernel.
    affine = tuple(tuple(2 * x + 3 * y for x, y in zip(v0p, v1p))
                   for v0p, v1p in zip(triples[0], triples[1]))
    affine_slice = abstract_incidence_slice(*affine)[0]
    require(rank(slices[0] + slices[1] + affine_slice, 27) == 26,
            "affine dark branch")
    require(all(det3((
        (u0[c], v0[b], w0[a]),
        (u1[c], v1[b], w1[a]),
        (affine[0][c], affine[1][b], affine[2][a]),
    )) == 0 for a, b, c in itertools.product(COLORS, repeat=3)),
            "affine holonomy must vanish")
    return {
        "generic_rank_ladder": ladder,
        "two_word_kernel_dimension": 1,
        "holonomy_witness": witness,
        "dark_affine_rank": 26,
    }


def poly_add(left, right, scale=Fraction(1)):
    out = dict(left)
    for monomial_key, coefficient in right.items():
        out[monomial_key] = out.get(monomial_key, Fraction(0)) + scale * coefficient
        if not out[monomial_key]:
            del out[monomial_key]
    return out


def poly_mul(left, right):
    out = {}
    for x, cx in left.items():
        for y, cy in right.items():
            key = tuple(sorted(x + y))
            out[key] = out.get(key, Fraction(0)) + cx * cy
            if not out[key]:
                del out[key]
    return out


def poly_var(name):
    return {(name,): Fraction(1)}


def formal_det3(rows):
    terms = {}
    for permutation in itertools.permutations(range(3)):
        inversions = sum(permutation[i] > permutation[j]
                         for i in range(3) for j in range(i + 1, 3))
        term = {(): Fraction(-1 if inversions % 2 else 1)}
        for i, j in enumerate(permutation):
            term = poly_mul(term, rows[i][j])
        terms = poly_add(terms, term)
    return terms


def exact_four_word_cramer_syzygy(mutate_sign=False):
    """Verify the universal source-word-changing 4x3 Cramer identity."""
    coefficient_rows = [
        [poly_var(f"c{s}{j}") for j in range(3)] for s in range(4)
    ]
    lambdas = []
    for omitted in range(4):
        minor = formal_det3([
            coefficient_rows[s] for s in range(4) if s != omitted
        ])
        lambdas.append({key: ((-1) ** omitted) * value
                        for key, value in minor.items()})
    if mutate_sign:
        lambdas[0] = {key: -value for key, value in lambdas[0].items()}

    equations = []
    remainders = []
    for s in range(4):
        equation = poly_add(poly_var(f"b{s}"), poly_var(f"t{s}"), scale=-1)
        for j in range(3):
            equation = poly_add(
                equation,
                poly_mul(coefficient_rows[s][j], poly_var(f"x{j}")),
            )
        equations.append(equation)
        remainders.append(poly_add(poly_var(f"b{s}"), poly_var(f"t{s}"), scale=-1))

    lhs = {}
    rhs = {}
    for s in range(4):
        lhs = poly_add(lhs, poly_mul(lambdas[s], equations[s]))
        rhs = poly_add(rhs, poly_mul(lambdas[s], remainders[s]))
    require(lhs == rhs, poly_add(lhs, rhs, scale=-1))
    require(not any(any(variable.startswith("x") for variable in monomial_key)
                    for monomial_key in lhs), "internal cells did not cancel")

    base_minor = formal_det3(coefficient_rows[:3])
    require(lambdas[3] == {key: -value for key, value in base_minor.items()},
            "fourth cofactor sign")
    # With rows 0,1,2 mixed and row 3 pure, -sum lambda_s*t_s is
    # -lambda_3*u = det(C_0,C_1,C_2)*u.
    target_part = poly_mul(base_minor, poly_var("u_pure"))
    require(target_part, "pure target holonomy vanished formally")
    return {
        "row_count": 4,
        "internal_cell_columns": 3,
        "signed_cofactor_terms_per_multiplier": 6,
        "internal_cell_terms_cancel": True,
        "pure_target_term": "det(C0,C1,C2)*u_pure",
        "remaining_source_sector": (
            "signed sum of the four 60-term triangle-avoiding packets"
        ),
    }


def cap_word_cramer_profile(outside_slice_rows, variable_index):
    """Specialize the four rows so their labels are one cap matrix K.

    Sites 0,1,2,3,4,5 have the common pure colour c.  Only the ordered
    colours (i,j) on cap endpoints 6,7 vary.  Three mixed cap words and the
    pure cap word (c,c) therefore give four rows whose signed Cramer
    cofactors are literally four entries of a single 3x3 cap matrix.
    """
    records = []
    mixed_pairs_by_colour = {
        c: tuple(pair for pair in itertools.product(COLORS, repeat=2)
                 if pair != (c, c))
        for c in COLORS
    }
    for c in COLORS:
        tword = (c, c, c)
        row_index = c * 9 + c * 3 + c
        columns = [
            variable_index[((0, 1), c, c)],
            variable_index[((0, 2), c, c)],
            variable_index[((1, 2), c, c)],
        ]

        def coefficient_row(pair):
            outside_word = f"{c}{c}{c}{pair[0]}{pair[1]}"
            return tuple(outside_slice_rows[outside_word][row_index][column]
                         for column in columns)

        witness = None
        nonzero_triples = 0
        for triple in itertools.combinations(mixed_pairs_by_colour[c], 3):
            mixed_rows = tuple(coefficient_row(pair) for pair in triple)
            determinant = det3(mixed_rows)
            if not determinant:
                continue
            nonzero_triples += 1
            if witness is None:
                all_pairs = triple + ((c, c),)
                all_rows = mixed_rows + (coefficient_row((c, c)),)
                lambdas = []
                for omitted in range(4):
                    minor = tuple(all_rows[index] for index in range(4)
                                  if index != omitted)
                    lambdas.append(Fraction((-1) ** omitted) * det3(minor))
                require(lambdas[3] == -determinant,
                        (c, triple, determinant, lambdas))
                require(all(
                    sum(lambdas[s] * all_rows[s][j] for s in range(4)) == 0
                    for j in range(3)
                ), (c, triple, all_rows, lambdas))
                cap_matrix = [
                    [Fraction(0) for _ in COLORS] for _ in COLORS
                ]
                for pair, value in zip(all_pairs, lambdas, strict=True):
                    cap_matrix[pair[0]][pair[1]] = value
                witness = {
                    "mixed_cap_pairs": [f"{i}{j}" for i, j in triple],
                    "pure_cap_pair": f"{c}{c}",
                    "mixed_minor": str(determinant),
                    "pure_row_multiplier": str(lambdas[3]),
                    "cap_matrix": [[str(value) for value in row]
                                   for row in cap_matrix],
                    "cap_matrix_support": [
                        f"{i}{j}" for i, j in all_pairs
                        if cap_matrix[i][j]
                    ],
                }
        records.append({
            "pure_colour": c,
            "mixed_cap_triples_tested": 56,
            "nonzero_mixed_minors": nonzero_triples,
            "witness": witness,
        })
    return {
        "records": records,
        "colours_with_open_chart": sum(record["witness"] is not None
                                       for record in records),
        "interpretation": (
            "On each displayed open chart, the four signed row cofactors "
            "are entries of one literal cap matrix K supported on three "
            "mixed cap colours and the pure diagonal colour.  The pure "
            "target occurs with coefficient minus the nonzero mixed minor."
        ),
    }


def canonical_line_multi_anchor_profile(outside_slice_rows, variable_index):
    """Keep the curvature-line labels E_ab, E_00, E_11, E_22 together.

    Unlike ``cap_word_cramer_profile``, this comparison does not discard two
    of the three pure target anchors.  Its four Cramer cofactors are one
    off-diagonal coefficient and the three separately labelled diagonal
    coefficients of a single cap matrix.
    """
    records = []
    for residual_colour in COLORS:
        row_index = 13 * residual_colour  # (c,c,c) in lexicographic order
        columns = [
            variable_index[((0, 1), residual_colour, residual_colour)],
            variable_index[((0, 2), residual_colour, residual_colour)],
            variable_index[((1, 2), residual_colour, residual_colour)],
        ]

        def coefficient_row(pair):
            outside_word = (
                f"{residual_colour}{residual_colour}{residual_colour}"
                f"{pair[0]}{pair[1]}"
            )
            return tuple(
                outside_slice_rows[outside_word][row_index][column]
                for column in columns
            )

        for a, b in itertools.product(COLORS, repeat=2):
            if a == b:
                continue
            pairs = ((a, b), (0, 0), (1, 1), (2, 2))
            rows = tuple(coefficient_row(pair) for pair in pairs)
            lambdas = []
            for omitted in range(4):
                minor = tuple(rows[index] for index in range(4) if index != omitted)
                lambdas.append(Fraction((-1) ** omitted) * det3(minor))
            require(all(
                sum(lambdas[s] * rows[s][j] for s in range(4)) == 0
                for j in range(3)
            ), (residual_colour, a, b, rows, lambdas))
            records.append({
                "residual_colour": residual_colour,
                "selected_offdiagonal": f"{a}{b}",
                "multipliers": {
                    f"{i}{j}": str(value)
                    for (i, j), value in zip(pairs, lambdas, strict=True)
                },
                "offdiagonal_nonzero": bool(lambdas[0]),
                "nonzero_diagonal_anchors": sum(bool(value) for value in lambdas[1:]),
            })
    return {
        "records": records,
        "comparisons": len(records),
        "offdiagonal_nonzero": sum(row["offdiagonal_nonzero"] for row in records),
        "three_anchor_support": sum(
            row["nonzero_diagonal_anchors"] == 3 for row in records
        ),
        "interpretation": (
            "Each record is one literal four-row relation supported on "
            "E_ab plus the three separately labelled diagonal anchors."
        ),
    }


def parse_source(payload):
    source = {}
    for key, matrix in payload.items():
        u, v = (int(piece.strip())
                for piece in key.strip().strip("()").split(","))
        source[u, v] = tuple(
            tuple(Fraction(str(value)) for value in row) for row in matrix
        )
    require(len(source) == 28, len(source))
    return source


def source_cell(source, u, v, a, b):
    if u < v:
        return source[u, v][a][b]
    return source[v, u][b][a]


def matching_value(source, matching, word):
    value = Fraction(1)
    for u, v in matching:
        value *= source_cell(source, u, v, word[u], word[v])
        if not value:
            break
    return value


def dense_rational_source(seed=1):
    source = {}
    for u, v in itertools.combinations(SITES, 2):
        matrix = []
        for a in COLORS:
            row = []
            for b in COLORS:
                flat = (((u * 8 + v) * 3 + a) * 3 + b) + 1
                row.append(Fraction(
                    1 + (seed * flat * flat + 7 * flat
                         + 11 * (u + 1) * (b + 1)
                         + 13 * (v + 1) * (a + 1)) % 23
                ))
            matrix.append(tuple(row))
        source[u, v] = tuple(matrix)
    return source


def generic_cap_word_nonvanishing_model():
    """Exhibit that the restricted cap-word minors are honest polynomials.

    The model is not an X5 point.  Its sole purpose is to prove that the
    determinant-open chart used by the argument is nonempty in source
    space, rather than an identically vanishing formal chart.
    """
    for seed in range(1, 32):
        source = dense_rational_source(seed)

        colour_records = []
        all_colours_open = True
        multi_anchor_records = []
        for c in COLORS:
            coefficient_rows = {}
            for i, j in itertools.product(COLORS, repeat=2):
                word = {site: c for site in range(6)}
                word[6] = i
                word[7] = j
                row = []
                for selected_edge in T_EDGES:
                    coefficient = Fraction(0)
                    for matching in MATCHINGS:
                        if internal_edge(matching) != selected_edge:
                            continue
                        term = Fraction(1)
                        for u, v in matching:
                            if tuple(sorted((u, v))) == selected_edge:
                                continue
                            term *= source_cell(source, u, v, word[u], word[v])
                        coefficient += term
                    row.append(coefficient)
                coefficient_rows[i, j] = tuple(row)

            mixed_pairs = tuple(pair for pair in coefficient_rows
                                if pair != (c, c))
            witness = None
            for triple in itertools.combinations(mixed_pairs, 3):
                determinant = det3(tuple(coefficient_rows[pair]
                                         for pair in triple))
                if determinant:
                    witness = {
                        "mixed_cap_pairs": [f"{i}{j}" for i, j in triple],
                        "determinant": str(determinant),
                    }
                    break
            colour_records.append({"pure_colour": c, "witness": witness})
            all_colours_open &= witness is not None
            for a, b in itertools.product(COLORS, repeat=2):
                if a == b:
                    continue
                pairs = ((a, b), (0, 0), (1, 1), (2, 2))
                rows = tuple(coefficient_rows[pair] for pair in pairs)
                lambdas = []
                for omitted in range(4):
                    minor = tuple(rows[index] for index in range(4)
                                  if index != omitted)
                    lambdas.append(Fraction((-1) ** omitted) * det3(minor))
                require(all(
                    sum(lambdas[s] * rows[s][j] for s in range(4)) == 0
                    for j in range(3)
                ), (seed, c, a, b, rows, lambdas))
                multi_anchor_records.append({
                    "residual_colour": c,
                    "selected_offdiagonal": f"{a}{b}",
                    "all_four_multipliers_nonzero": all(lambdas),
                })
        if all_colours_open:
            return {
                "seed": seed,
                "value_rule_modulus": 23,
                "colours": colour_records,
                "multi_anchor_comparisons": len(multi_anchor_records),
                "multi_anchor_all_four_nonzero": sum(
                    row["all_four_multipliers_nonzero"]
                    for row in multi_anchor_records
                ),
                "scope": "exact dense rational source, not an X5 solution",
            }
    raise RuntimeError("failed to exhibit a nonzero cap-word minor")


def solve_basis_coordinates(basis_rows, target):
    """Solve target=sum_i coefficient_i*basis_rows[i] over Q."""
    size = len(basis_rows)
    require(size == len(target) and all(len(row) == size for row in basis_rows),
            "basis must be square")
    work = [
        [basis_rows[column][row] for column in range(size)] + [target[row]]
        for row in range(size)
    ]
    for column in range(size):
        pivot = next((row for row in range(column, size)
                      if work[row][column]), None)
        require(pivot is not None, ("singular basis", column))
        work[column], work[pivot] = work[pivot], work[column]
        value = work[column][column]
        work[column] = [entry / value for entry in work[column]]
        for row in range(size):
            if row == column or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[column], strict=True)]
    return tuple(work[row][-1] for row in range(size))


def determinant(matrix):
    work = [list(row) for row in matrix]
    size = len(work)
    require(all(len(row) == size for row in work), "determinant square")
    value = Fraction(1)
    sign = 1
    for column in range(size):
        pivot = next((row for row in range(column, size)
                      if work[row][column]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            sign = -sign
        head = work[column][column]
        value *= head
        for row in range(column + 1, size):
            if not work[row][column]:
                continue
            factor = work[row][column] / head
            for index in range(column + 1, size):
                work[row][index] -= factor * work[column][index]
            work[row][column] = Fraction(0)
    return sign * value


def global_multi_anchor_dependency_profile(source):
    """Find one literal dependency crossing rootless and three pure words.

    The 6,561 triangle observation rows share 27 physical internal cells.
    A common 27-row basis lets the four mandatory rows be compared without
    changing source coordinates.  Summing their four fundamental relations
    is stronger than a four-row relation confined to one triangle word, but
    need not itself be a deletion-minimal matroid circuit.
    """
    labels = [
        (edge, a, b)
        for edge in T_EDGES
        for a in COLORS
        for b in COLORS
    ]
    variable_index = {label: index for index, label in enumerate(labels)}

    def coefficient_row(word_string):
        word = tuple(int(value) for value in word_string)
        require(len(word) == 8, word_string)
        row = [Fraction(0) for _ in labels]
        for edge in T_EDGES:
            coefficient = Fraction(0)
            for matching in MATCHINGS:
                if internal_edge(matching) != edge:
                    continue
                term = Fraction(1)
                for u, v in matching:
                    if tuple(sorted((u, v))) == edge:
                        continue
                    term *= source_cell(source, u, v, word[u], word[v])
                coefficient += term
            row[variable_index[(edge, word[edge[0]], word[edge[1]])]] = coefficient
        return tuple(row)

    mandatory = ("01211222", "00000000", "11111111", "22222222")
    all_words = tuple("".join(map(str, word))
                      for word in itertools.product(COLORS, repeat=8))
    rows = {word: coefficient_row(word) for word in all_words}
    comparison_suffixes = ("11222", "00000", "11111", "22222")
    comparison_words = tuple(
        "".join(map(str, tword)) + suffix
        for suffix in comparison_suffixes
        for tword in itertools.product(COLORS, repeat=3)
    )
    basis_words = []
    basis_rows = []
    for word in comparison_words:
        if word in mandatory:
            continue
        candidate = rows[word]
        if rank(basis_rows + [candidate], 27) > len(basis_rows):
            basis_words.append(word)
            basis_rows.append(candidate)
            if len(basis_rows) == 27:
                break
    require(len(basis_rows) == 27 and rank(basis_rows, 27) == 27,
            (len(basis_rows), rank(basis_rows, 27)))
    basis_determinant = determinant(basis_rows)
    require(basis_determinant, "comparison basis determinant vanished")

    weights = tuple(map(Fraction, (1, 2, 4, 8)))
    coordinates = tuple(
        solve_basis_coordinates(basis_rows, rows[word]) for word in mandatory
    )
    basis_multipliers = tuple(
        -sum(weights[index] * coordinates[index][column]
             for index in range(len(mandatory)))
        for column in range(27)
    )
    require(all(
        sum(weights[index] * rows[mandatory[index]][column]
            for index in range(len(mandatory)))
        + sum(basis_multipliers[index] * basis_rows[index][column]
              for index in range(27)) == 0
        for column in range(27)
    ), "global multi-anchor dependency replay")
    witness = {
        "basis_words": basis_words,
        "comparison_outside_words": list(comparison_suffixes),
        "basis_determinant_sign": 1 if basis_determinant > 0 else -1,
        "basis_determinant_numerator_bits": abs(
            basis_determinant.numerator
        ).bit_length(),
        "basis_determinant_denominator": str(basis_determinant.denominator),
        "basis_determinant_sha256": hashlib.sha256(
            str(basis_determinant).encode()
        ).hexdigest(),
        "mandatory_multipliers": {
            label: str(weights[index])
            for index, label in enumerate(mandatory)
        },
        "nonzero_basis_multipliers": sum(bool(value)
                                          for value in basis_multipliers),
        "dependency_support": len(mandatory) + sum(
            bool(value) for value in basis_multipliers
        ),
        "all_four_mandatory_nonzero": True,
    }
    return {
        "mandatory_words": list(mandatory),
        "global_internal_cell_columns": 27,
        "comparison_basis_rows": 27,
        "pure_target_scalar_after_weights": str(sum(weights[1:])),
        "witness": witness,
        "scope": (
            "Exact rational dense-source witness that the literal global "
            "triangle observation map has a bounded dependency containing "
            "the rootless word and all three pure anchors; not necessarily "
            "a deletion-minimal circuit, not an X5 point, and not yet a "
            "source-independent divisor-evaluation identity."
        ),
    }


def load_controls():
    require(sha256(W40_PATH) == W40_SHA, "W40 pin changed")
    require(sha256(W25_PATH) == W25_SHA, "W25 pin changed")
    w40_raw = json.loads(W40_PATH.read_text())["engine_audit"]["witness_B_integral"]["source"]
    w25_raw = json.loads(W25_PATH.read_text())["blocks"]
    return {"W40_X4": parse_source(w40_raw), "W25_X3": parse_source(w25_raw)}


def block_numeric(source, tword):
    rows = []
    defects = []
    for oword in itertools.product(COLORS, repeat=len(O)):
        word = dict(zip(T, tword, strict=True))
        word.update(zip(O, oword, strict=True))
        columns = []
        for edge in T_EDGES:
            x = source_cell(source, *edge, word[edge[0]], word[edge[1]])
            require(x is not None, edge)
            coefficient = Fraction(0)
            for matching in MATCHINGS:
                if internal_edge(matching) == edge:
                    term = matching_value(source, matching, word)
                    if x:
                        # Every such term contains the selected cell once.
                        coefficient += term / x
                    else:
                        # Recompute the remaining six-site product without
                        # dividing by a zero specialization.
                        term = Fraction(1)
                        for u, v in matching:
                            if tuple(sorted((u, v))) == edge:
                                continue
                            term *= source_cell(source, u, v, word[u], word[v])
                        coefficient += term
            columns.append(coefficient)
        avoiding = sum(
            (matching_value(source, matching, word) for matching in MATCHINGS
             if internal_edge(matching) is None),
            Fraction(0),
        )
        target = Fraction(1) if len(set(word.values())) == 1 else Fraction(0)
        rhs = target - avoiding
        rows.append(tuple(columns) + (rhs,))
        total = avoiding + sum(
            columns[index] * source_cell(
                source, *edge, word[edge[0]], word[edge[1]]
            )
            for index, edge in enumerate(T_EDGES)
        )
        if total != target:
            defects.append("".join(map(str, tword + oword)))
    column_rank = rank((row[:3] for row in rows), 3)
    augmented_rank = rank(rows, 4)
    return column_rank, augmented_rank, defects


def control_profile(source):
    records = []
    for tword in itertools.product(COLORS, repeat=3):
        rank_c, rank_aug, defects = block_numeric(source, tword)
        records.append({
            "triangle_word": "".join(map(str, tword)),
            "column_rank": rank_c,
            "augmented_rank": rank_aug,
            "defect_count": len(defects),
            "defect_words": defects,
        })
    # Global system: the 27 word blocks share the same 27 physical cells.
    # A cell A_01[i,j], for example, appears in the three blocks (i,j,k).
    variable_labels = [
        (edge, a, b)
        for edge in T_EDGES
        for a in COLORS
        for b in COLORS
    ]
    variable_index = {label: index for index, label in enumerate(variable_labels)}
    global_rows = []
    for tword in itertools.product(COLORS, repeat=3):
        for oword in itertools.product(COLORS, repeat=len(O)):
            word = dict(zip(T, tword, strict=True))
            word.update(zip(O, oword, strict=True))
            row = [Fraction(0) for _ in range(28)]
            for edge in T_EDGES:
                coefficient = Fraction(0)
                for matching in MATCHINGS:
                    if internal_edge(matching) != edge:
                        continue
                    term = Fraction(1)
                    for u, v in matching:
                        if tuple(sorted((u, v))) == edge:
                            continue
                        term *= source_cell(source, u, v, word[u], word[v])
                    coefficient += term
                label = (edge, word[edge[0]], word[edge[1]])
                row[variable_index[label]] = coefficient
            avoiding = sum(
                (matching_value(source, matching, word) for matching in MATCHINGS
                 if internal_edge(matching) is None),
                Fraction(0),
            )
            target = Fraction(1) if len(set(word.values())) == 1 else Fraction(0)
            row[27] = target - avoiding
            global_rows.append(tuple(row))
    global_column_rank = rank((row[:27] for row in global_rows), 27)
    global_augmented_rank = rank(global_rows, 28)

    # Regroup the same literal equations by the five outside colours.  For a
    # fixed outside word, the 27 triangle words give a square 27x27 weighted
    # triangle-incidence matrix in the 27 physical cells.  A nonsingular
    # slice is therefore a literal Cramer chart for all internal triangle
    # cells; comparing two slices is an actual cross-word elimination, not a
    # declared word-reset operation.
    outside_slices = []
    outside_slice_rows = {}
    for oword in itertools.product(COLORS, repeat=len(O)):
        rows = []
        for tword in itertools.product(COLORS, repeat=len(T)):
            word = dict(zip(T, tword, strict=True))
            word.update(zip(O, oword, strict=True))
            row = [Fraction(0) for _ in range(28)]
            for edge in T_EDGES:
                coefficient = Fraction(0)
                for matching in MATCHINGS:
                    if internal_edge(matching) != edge:
                        continue
                    term = Fraction(1)
                    for u, v in matching:
                        if tuple(sorted((u, v))) == edge:
                            continue
                        term *= source_cell(source, u, v, word[u], word[v])
                    coefficient += term
                label = (edge, word[edge[0]], word[edge[1]])
                row[variable_index[label]] = coefficient
            avoiding = sum(
                (matching_value(source, matching, word) for matching in MATCHINGS
                 if internal_edge(matching) is None),
                Fraction(0),
            )
            target = Fraction(1) if len(set(word.values())) == 1 else Fraction(0)
            row[27] = target - avoiding
            rows.append(tuple(row))
        column_rank = rank((row[:27] for row in rows), 27)
        augmented_rank = rank(rows, 28)
        outside_slices.append({
            "outside_word": "".join(map(str, oword)),
            "column_rank": column_rank,
            "augmented_rank": augmented_rank,
        })
        outside_slice_rows["".join(map(str, oword))] = tuple(rows)

    # Greedily expose the exact 19 -> 26 -> 27 cross-word ladder.  This is
    # only a profiling choice: the rank statements are recomputed from the
    # literal slice rows, and no randomization or modular inference is used.
    chosen = []
    accumulated = []
    ladder = []
    remaining = sorted(outside_slice_rows)
    while remaining and (not ladder or ladder[-1] < global_column_rank):
        scored = []
        for word in remaining:
            candidate_rank = rank(accumulated + list(outside_slice_rows[word]), 27)
            scored.append((candidate_rank, word))
        best_rank = max(score for score, _ in scored)
        best_word = min(word for score, word in scored if score == best_rank)
        chosen.append(best_word)
        accumulated.extend(outside_slice_rows[best_word])
        ladder.append(best_rank)
        remaining.remove(best_word)
        require(len(chosen) <= 27, (chosen, ladder))

    determinant_witness = None
    if len(chosen) >= 3 and ladder[2] == 27:
        for a, b, c in itertools.product(COLORS, repeat=3):
            row_index = a * 9 + b * 3 + c
            columns = [
                variable_index[((0, 1), a, b)],
                variable_index[((0, 2), a, c)],
                variable_index[((1, 2), b, c)],
            ]
            matrix = [
                [outside_slice_rows[word][row_index][column] for column in columns]
                for word in chosen[:3]
            ]
            value = det3(matrix)
            if value:
                determinant_witness = {
                    "triangle_word": f"{a}{b}{c}",
                    "value": str(value),
                }
                break
        require(determinant_witness is not None, (chosen, ladder))
    return {
        "column_rank_histogram": dict(sorted(Counter(r["column_rank"] for r in records).items())),
        "rank_jump_blocks": sum(r["augmented_rank"] > r["column_rank"] for r in records),
        "defect_count": sum(r["defect_count"] for r in records),
        "global_column_rank": global_column_rank,
        "global_augmented_rank": global_augmented_rank,
        "global_rank_jump": global_augmented_rank - global_column_rank,
        "outside_slice_rank_histogram": dict(sorted(Counter(
            record["column_rank"] for record in outside_slices
        ).items())),
        "outside_slice_rank_jumps": sum(
            record["augmented_rank"] > record["column_rank"]
            for record in outside_slices
        ),
        "invertible_outside_slices": [
            record["outside_word"] for record in outside_slices
            if record["column_rank"] == 27
        ],
        "greedy_crossword_words": chosen,
        "greedy_crossword_rank_ladder": ladder,
        "three_word_cofactor_determinant_witness": determinant_witness,
        "cap_word_cramer_profile": cap_word_cramer_profile(
            outside_slice_rows, variable_index
        ),
        "canonical_line_multi_anchor_profile": canonical_line_multi_anchor_profile(
            outside_slice_rows, variable_index
        ),
        "records": records,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--mutate-cramer-sign", action="store_true")
    args = parser.parse_args()

    matching_partition = Counter(internal_edge(matching) for matching in MATCHINGS)
    require(matching_partition[None] == 60, matching_partition)
    require(all(matching_partition[edge] == 15 for edge in T_EDGES), matching_partition)

    literal_occurrences = 0
    coefficient_occurrences = Counter()
    avoiding_occurrences = 0
    hostile_transpose_mismatches = 0
    y0 = "A_06[0,1]"
    y0_profile = Counter()
    source_variable_blocks = {}

    for tword in itertools.product(COLORS, repeat=3):
        selected_cells = tuple(
            stored_cell(*edge, tword[edge[0]], tword[edge[1]]) for edge in T_EDGES
        )
        source_variable_blocks["".join(map(str, tword))] = selected_cells
        for oword in itertools.product(COLORS, repeat=5):
            word = dict(zip(T, tword, strict=True))
            word.update(zip(O, oword, strict=True))
            reconstructed = []
            for matching in MATCHINGS:
                edge = internal_edge(matching)
                term = monomial(matching, word)
                literal_occurrences += 1
                if edge is None:
                    avoiding_occurrences += 1
                    reconstructed.append(("b", term))
                    if y0 in term:
                        y0_profile["avoiding"] += 1
                else:
                    index = T_EDGES.index(edge)
                    selected = selected_cells[index]
                    require(selected in term, (edge, selected, term))
                    cofactor = list(term)
                    cofactor.remove(selected)
                    coefficient_occurrences[edge] += 1
                    reconstructed.append((f"c{edge[0]}{edge[1]}", (selected, *cofactor)))
                    if y0 in cofactor:
                        y0_profile[f"cofactor_{edge[0]}{edge[1]}"] += 1
                # Hostile endpoint-order guard: A_06[0,1] must not be
                # silently rewritten as A_06[1,0].
                if y0 in term and "A_06[1,0]" not in term:
                    hostile_transpose_mismatches += 1
            require(len(reconstructed) == 105, len(reconstructed))

    require(literal_occurrences == 3**8 * 105, literal_occurrences)
    require(avoiding_occurrences == 3**8 * 60, avoiding_occurrences)
    require(set(coefficient_occurrences.values()) == {3**8 * 15}, coefficient_occurrences)
    require(hostile_transpose_mismatches > 0, "orientation hostile guard did not fire")

    # Refine the 60 triangle-avoiding matchings relative to the canonical
    # cap pair 67.  This is the exact remainder sector of the four-word
    # Cramer identity.  After contraction by a triangle-carrier kernel, the
    # 36 outside-triangle response terms vanish; only the six direct terms
    # and eighteen internal-triangle response terms remain.
    remainder_sectors = Counter()
    outside_residual = {3, 4, 5}
    cap_pair = {6, 7}
    for matching in MATCHINGS:
        if internal_edge(matching) is not None:
            continue
        internal_o = [set(edge) for edge in matching if set(edge) <= set(O)]
        require(len(internal_o) == 1, (matching, internal_o))
        edge = internal_o[0]
        if edge == cap_pair:
            remainder_sectors["direct_A67"] += 1
        elif edge <= outside_residual:
            remainder_sectors["internal_triangle_response"] += 1
        else:
            require(len(edge & cap_pair) == 1 and len(edge & outside_residual) == 1,
                    (matching, edge))
            remainder_sectors["outside_triangle_response"] += 1
    require(remainder_sectors == {
        "direct_A67": 6,
        "internal_triangle_response": 18,
        "outside_triangle_response": 36,
    }, remainder_sectors)

    # The 27 selected variable triples are disjoint and cover all 27 cells
    # on the three internal triangle blocks.
    all_selected = [cell for block in source_variable_blocks.values() for cell in block]
    require(len(all_selected) == 81, len(all_selected))
    require(len(set(all_selected)) == 27, len(set(all_selected)))
    selected_multiplicity = Counter(all_selected)
    require(set(selected_multiplicity.values()) == {3}, selected_multiplicity)

    # Correct statement: each physical cell belongs to three fixed-word
    # systems because the colour on the third triangle vertex is free.
    # Within each system, however, only the three displayed cells occur as
    # affine unknowns.

    # Triangle-word orbits under site permutations and global colour
    # permutations are the equality patterns 3, 2+1, and 1+1+1.
    orbit_hist = Counter(tuple(sorted(Counter(tword).values(), reverse=True))
                         for tword in itertools.product(COLORS, repeat=3))
    require(orbit_hist == {(3,): 3, (2, 1): 18, (1, 1, 1): 6}, orbit_hist)

    # Untwisted incidence shadow.  Rows are triangle-colour triples and
    # columns are colour-labelled cells on the three triangle edges.
    incidence_columns = [
        (edge, a, b)
        for edge in T_EDGES
        for a in COLORS
        for b in COLORS
    ]
    incidence_index = {label: index for index, label in enumerate(incidence_columns)}
    incidence_rows = []
    for tword in itertools.product(COLORS, repeat=3):
        row = [Fraction(0) for _ in incidence_columns]
        for edge in T_EDGES:
            row[incidence_index[(edge, tword[edge[0]], tword[edge[1]])]] = Fraction(1)
        incidence_rows.append(tuple(row))
    incidence_rank = rank(incidence_rows, 27)
    require(incidence_rank == 19, incidence_rank)

    # The canonical triangle membership matrix uses only response edges
    # outside T, so no A_01/A_02/A_12 source cell can occur in it.
    membership_source_cells = set()
    for a, b in TRIANGLE_OUTSIDE_EDGES:
        for alpha, beta in itertools.product(COLORS, repeat=2):
            for i, j in itertools.product(COLORS, repeat=2):
                membership_source_cells.add(stored_cell(6, a, i, alpha))
                membership_source_cells.add(stored_cell(7, b, j, beta))
                membership_source_cells.add(stored_cell(6, b, i, beta))
                membership_source_cells.add(stored_cell(7, a, j, alpha))
    require(not set(all_selected) & membership_source_cells,
            set(all_selected) & membership_source_cells)
    require(y0 in membership_source_cells, "live tail cell must enter outside responses")

    controls = {name: control_profile(source) for name, source in load_controls().items()}
    require(controls["W40_X4"]["defect_count"] == 3, controls["W40_X4"])
    require(controls["W25_X3"]["defect_count"] == 103, controls["W25_X3"])
    require(controls["W40_X4"]["rank_jump_blocks"] > 0,
            controls["W40_X4"]["rank_jump_blocks"])
    require(controls["W25_X3"]["rank_jump_blocks"] > 0,
            controls["W25_X3"]["rank_jump_blocks"])
    require(controls["W40_X4"]["global_rank_jump"] == 1,
            controls["W40_X4"])
    require(controls["W25_X3"]["global_rank_jump"] == 1,
            controls["W25_X3"])

    payload = {
        "status": "PASS",
        "scope": (
            "Literal triangle-local affine decomposition and exact rational "
            "control ranks; no emptiness or cap theorem is claimed."
        ),
        "triangle": list(T),
        "outside": list(O),
        "matching_partition": {
            "avoids_triangle": matching_partition[None],
            "per_internal_edge": matching_partition[T_EDGES[0]],
            "total": len(MATCHINGS),
        },
        "observation_blocks": {
            "count": 27,
            "rows_per_block": 243,
            "affine_unknowns_per_block": 3,
            "triangle_word_orbits": {
                "3": orbit_hist[(3,)],
                "2+1": orbit_hist[(2, 1)],
                "1+1+1": orbit_hist[(1, 1, 1)],
            },
            "criterion": (
                "For each fixed triangle word g, X5 is equivalent to "
                "rank(C_g)=rank([C_g|target_g-b_g]); equivalently the "
                "class of target_g-b_g vanishes in k^243/im(C_g)."
            ),
            "rank_three_chart": (
                "One nonzero 3x3 row minor solves the three internal-edge "
                "cells and leaves 240 denominator-cleared compatibility rows."
            ),
        },
        "global_observation_map": {
            "rows": 6561,
            "physical_internal_triangle_cells": 27,
            "nonzero_columns_per_row": 3,
            "shared_cell_incidence_rank": incidence_rank,
            "shared_cell_incidence_kernel_dimension": 27 - incidence_rank,
            "criterion": (
                "All 27 word blocks glue to one 6561x27 coefficient matrix D_T; "
                "X5 is exactly target-b in im(D_T).  The rank-19 untwisted "
                "shadow has an 8-dimensional vertex-potential gauge, while "
                "the physical cofactor weights may raise the rank to 27."
            ),
            "outside_slice_ladder": (
                "For each of the 243 outside words o, the 27 triangle-word "
                "rows form a square weighted triangle-incidence matrix D_o. "
                "One generic word has rank 19, two have rank 26, and a third "
                "reaches 27 exactly when a 3x3 determinant of their six-site "
                "cofactor triples is nonzero.  This is the literal three-word "
                "holonomy/comparison packet."
            ),
        },
        "exact_three_word_model": exact_three_word_model(),
        "exact_four_word_cramer_syzygy": exact_four_word_cramer_syzygy(
            mutate_sign=args.mutate_cramer_sign
        ),
        "generic_cap_word_nonvanishing_model": (
            generic_cap_word_nonvanishing_model()
        ),
        "global_rootless_three_pure_dependency": (
            global_multi_anchor_dependency_profile(dense_rational_source(1))
        ),
        "cramer_remainder_cap_partition": {
            **dict(sorted(remainder_sectors.items())),
            "triangle_kernel_consequence": (
                "The 36 outside-triangle response terms vanish on ker(L_T); "
                "the unresolved remainder is exactly 6 direct-A67 plus 18 "
                "internal-triangle-response matchings."
            ),
        },
        "literal_occurrences_checked": literal_occurrences,
        "coefficient_occurrences_per_internal_edge": {
            f"{edge[0]}{edge[1]}": coefficient_occurrences[edge]
            for edge in T_EDGES
        },
        "avoiding_occurrences": avoiding_occurrences,
        "selected_physical_cells": {
            "distinct": len(set(all_selected)),
            "fixed_word_occurrences": len(all_selected),
            "systems_per_physical_cell": 3,
        },
        "triangle_membership_disjointness": {
            "internal_cells_in_membership_matrix": 0,
            "live_A_06_01_enters_membership_matrix": True,
            "consequence": (
                "The 27 internal triangle cells can be eliminated from X5 "
                "without changing any of the four canonical blocker "
                "membership equations."
            ),
        },
        "live_cell_occurrence_profile": dict(sorted(y0_profile.items())),
        "controls": controls,
        "pins": {str(W40_PATH.relative_to(ROOT)): W40_SHA,
                 str(W25_PATH.relative_to(ROOT)): W25_SHA},
    }
    logical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["logical_sha256"] = hashlib.sha256(logical.encode()).hexdigest()
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.write_results:
        OUT.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
