#!/usr/bin/env python3
"""Finite exact/modular audit of the T0-equivariant differential-rank idea."""

from __future__ import annotations

from fractions import Fraction
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
from math import gcd, lcm
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "results_x5_equivariant_differential_rank.json"
W40 = ROOT / "computations/unaudited-x4general-w40-2026-08-20/results_t3.json"
W25 = ROOT / "computations/unaudited-x3core-w25-2026-08-15/OBJECT_W25-F8_n8_allblocked_X3.json"
PINS = {
    W40: "30ad242d62b5cb905858842ce4e8255b105862dc21a65c73c080557fa8c1617f",
    W25: "46d6e207e392deaa7e0bfc4221c7f5cc6735f11a2a14cc388292ca6850dd33f6",
}
SITES = tuple(range(8))
COLOURS = tuple(range(3))
EDGES = tuple(combinations(SITES, 2))
COORDS = tuple((u, v, a, b) for u, v in EDGES
               for a in COLOURS for b in COLOURS)
COORD_INDEX = {coordinate: index for index, coordinate in enumerate(COORDS)}
PRIMES = (1000003, 1000033)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


PM6 = {vertices: perfect_matchings(vertices)
       for vertices in (tuple(site for site in SITES if site not in edge)
                        for edge in EDGES)}
PM8 = perfect_matchings(SITES)


def file_sha(path):
    return sha256(path.read_bytes()).hexdigest()


def parse_source(path, kind):
    record = json.loads(path.read_text())
    raw = (record["engine_audit"]["witness_B_integral"]["source"]
           if kind == "W40" else record["blocks"])
    source = {}
    for key, matrix in raw.items():
        pieces = key.strip("()").split(",")
        u, v = (int(piece.strip()) for piece in pieces)
        source[u, v] = tuple(tuple(Fraction(value) for value in row)
                             for row in matrix)
    require(set(source) == set(EDGES), (kind, len(source)))
    return source


def cell(source, u, v, a, b):
    if u < v:
        return source[u, v][a][b]
    return source[v, u][b][a]


def source_mod(source, prime):
    return {edge: tuple(tuple((value.numerator % prime)
                                   * pow(value.denominator, prime - 2, prime)
                                   % prime for value in row)
                               for row in matrix)
            for edge, matrix in source.items()}


def haf_mod(mod_source, word, vertices, prime):
    total = 0
    for matching in PM6[vertices] if len(vertices) == 6 else PM8:
        term = 1
        for u, v in matching:
            term = term * mod_source[u, v][word[u]][word[v]] % prime
            if not term:
                break
        total = (total + term) % prime
    return total


def haf_q(source, word, vertices):
    total = Fraction(0)
    matchings = PM6[vertices] if len(vertices) == 6 else PM8
    for matching in matchings:
        term = Fraction(1)
        for u, v in matching:
            term *= cell(source, u, v, word[u], word[v])
            if not term:
                break
        total += term
    return total


def carrier_rows_q(source, p, q, kind, label):
    residual = tuple(site for site in SITES if site not in (p, q))
    if kind == "star":
        allowed = {edge for edge in combinations(residual, 2)
                   if label in edge}
    else:
        allowed = set(combinations(label, 2))
    rows = []
    for a, b in combinations(residual, 2):
        if (a, b) in allowed:
            continue
        for alpha, beta in product(COLOURS, repeat=2):
            row = []
            for i, j in product(COLOURS, repeat=2):
                row.append(
                    cell(source, p, a, i, alpha)
                    * cell(source, q, b, j, beta)
                    + cell(source, p, b, i, beta)
                    * cell(source, q, a, j, alpha)
                )
            rows.append(row)
    expected = 90 if kind == "star" else 108
    require(len(rows) == expected, (p, q, kind, label, len(rows)))
    return rows


def hessian_carrier_controls(w40_source, w25_source):
    identity = tuple(Fraction(int(i == j))
                     for i, j in product(COLOURS, repeat=2))
    w40_rows = carrier_rows_q(w40_source, 6, 7, "star", 5)
    require(all(sum(left * right for left, right in zip(row, identity,
                                                        strict=True)) == 0
                for row in w40_rows), "W40 identity K left carrier kernel")
    w40_s = sum(identity[3 * i + j] * cell(w40_source, 6, 7, i, j)
                for i, j in product(COLOURS, repeat=2))
    require(w40_s == 1, w40_s)
    w40_h6 = haf_q(w40_source, (0,) * 8, tuple(range(6)))
    require(w40_h6 == 1, w40_h6)

    w25_rows = carrier_rows_q(w25_source, 0, 1, "star", 2)
    w25_rank = rational_rank(w25_rows, 9)
    require(w25_rank == 9, w25_rank)
    w25_h6 = haf_q(w25_source, (0,) * 8, tuple(range(2, 8)))
    require(w25_h6 == Fraction(1, 2), w25_h6)
    return {
        "W40_active_control": {
            "carrier": "pair 67, star centre 5",
            "K": "I3",
            "L_times_K": "zero in all 90 forbidden response rows",
            "activity_s": str(w40_s),
            "pure0_direct_Jacobian_cofactor_H6": str(w40_h6),
            "conormal_test": (
                "FAIL: the slice covector K has nonzero contraction with "
                "the true pair-67 Jacobian block because H6=1."
            ),
        },
        "W25_blocked_control": {
            "carrier": "pair 01, star centre 2",
            "carrier_rank": w25_rank,
            "blockers": "all four activity rows lie in the full rowspace",
            "chosen_blocker": "ell_0=K00",
            "pure0_direct_Jacobian_cofactor_H6": str(w25_h6),
            "conormal_test": (
                "FAIL: ell_0 contracted with the true pair-01 Jacobian "
                "column A_01[00] is H6=1/2, not zero. Thus even an exact "
                "carrier blocker is not a conormal/radical element for II."
            ),
        },
    }


def pair_grade_active_indices(word):
    """ANOVA basis of functions of at most two sites: dimension 129."""
    indices = [0]
    for site, colour in enumerate(word):
        if colour < 2:
            indices.append(1 + 2 * site + colour)
    pair_start = 17
    for edge_index, (u, v) in enumerate(EDGES):
        if word[u] < 2 and word[v] < 2:
            indices.append(pair_start + 4 * edge_index
                           + 2 * word[u] + word[v])
    require(len(set(indices)) == len(indices), (word, indices))
    return indices


def pair_grade_conormal_test(source):
    """Compress J^T on the full 129-dimensional pairwise word-function grade."""
    width = 1 + 8 * 2 + 28 * 4
    require(width == 129, width)
    compressed = [[Fraction(0)] * width for _ in range(252)]
    for word in product(COLOURS, repeat=8):
        active = pair_grade_active_indices(word)
        for u, v in EDGES:
            residual = tuple(site for site in SITES if site not in (u, v))
            coefficient = haf_q(source, word, residual)
            if not coefficient:
                continue
            row = compressed[COORD_INDEX[u, v, word[u], word[v]]]
            for basis_index in active:
                row[basis_index] += coefficient
    rank = rational_rank(compressed, width)
    return {
        "pairwise_word_function_dimension": width,
        "compressed_J_transpose_rank_over_Q": rank,
        "pairwise_conormal_dimension": width - rank,
        "matrix_shape": [252, width],
    }


def conormal_overlap_test(w40_source, w25_source):
    w40 = pair_grade_conormal_test(w40_source)
    w25 = pair_grade_conormal_test(w25_source)
    return {
        "strict_restriction_overlap_lemma": {
            "intersection_dimension": 1,
            "proof": (
                "If one global lambda restricts to a function only of "
                "(w_p,w_q) for every pair pq, choose two disjoint pairs. "
                "Varying the second while holding the first shows both "
                "pair functions, and hence lambda, are constant."
            ),
            "consequence": (
                "Literal equality of all 28 pair-slice restrictions can "
                "glue only the constant covector. Diagonal blockers K00, "
                "K11, K22 are nonconstant, so arbitrary per-carrier blocker "
                "choices have no global mixed covector with those exact "
                "restrictions."
            ),
        },
        "sum_of_pair_slices_grade": {
            "description": (
                "Allow the most generous linear gluing lambda(w)="
                "sum_(p<q)K_pq[w_p,w_q]. Pair-slice parameter space has "
                "dimension 252 but its image is the degree-at-most-two "
                "ANOVA word-function space of dimension 129; the overlap "
                "gauge kernel has dimension 123."
            ),
            "W40_full_J": w40,
            "W25_full_J": w25,
        },
        "bounded_verdict": (
            "On both sharp controls the compressed map J^T is injective on "
            "the entire 129-dimensional pairwise grade, so there is no "
            "nonzero conormal assembled from pair-flattening covectors at "
            "all—not merely no blocker-compatible one. A conormal lift at a "
            "hypothetical X5 point would require a rank drop forced by the "
            "full equations or word degree at least three; it is not a "
            "formal consequence of carrier overlap."
        ),
    }


def off_count(word):
    return 8 - max(word.count(colour) for colour in COLOURS)


def jacobian_rows_mod(source, prime, level=None):
    mod_source = source_mod(source, prime)
    rows = []
    outputs = []
    defects = []
    for word in product(COLOURS, repeat=8):
        if level is not None and off_count(word) > level:
            continue
        value = haf_mod(mod_source, word, SITES, prime)
        target = 1 if len(set(word)) == 1 else 0
        if value != target:
            defects.append("".join(map(str, word)))
        row = {}
        for u, v in EDGES:
            residual = tuple(site for site in SITES if site not in (u, v))
            coefficient = haf_mod(mod_source, word, residual, prime)
            if coefficient:
                row[COORD_INDEX[u, v, word[u], word[v]]] = coefficient
        rows.append(row)
        outputs.append(value)
    return rows, outputs, defects


def sparse_rank_mod(rows, prime):
    pivots = {}
    for original in rows:
        row = dict(original)
        while row:
            column = min(row)
            if column not in pivots:
                inverse = pow(row[column], prime - 2, prime)
                pivots[column] = {key: value * inverse % prime
                                  for key, value in row.items() if value}
                break
            factor = row[column]
            for key, value in pivots[column].items():
                new = (row.get(key, 0) - factor * value) % prime
                if new:
                    row[key] = new
                else:
                    row.pop(key, None)
    return len(pivots)


def sparse_rank_q(rows):
    """Exact sparse Gaussian rank over Q; only 252 columns can pivot."""
    pivots = {}
    for original in rows:
        row = {column: Fraction(value) for column, value in original.items()
               if value}
        while row:
            column = min(row)
            if column not in pivots:
                scale = row[column]
                pivots[column] = {key: value / scale
                                  for key, value in row.items() if value}
                break
            factor = row[column]
            for key, value in pivots[column].items():
                new = row.get(key, Fraction(0)) - factor * value
                if new:
                    row[key] = new
                else:
                    row.pop(key, None)
    return len(pivots)


def structural_column_row_matching(rows, columns=252):
    """Maximum bipartite matching using the evaluated nonzero entry pattern."""
    adjacency = [[] for _ in range(columns)]
    for row_index, row in enumerate(rows):
        for column in row:
            adjacency[column].append(row_index)
    row_to_column = {}

    def augment(column, seen):
        for row_index in adjacency[column]:
            if row_index in seen:
                continue
            seen.add(row_index)
            previous = row_to_column.get(row_index)
            if previous is None or augment(previous, seen):
                row_to_column[row_index] = column
                return True
        return False

    matched = sum(augment(column, set()) for column in range(columns))
    return matched


def jacobian_rows_q(source, level=None):
    rows = []
    for word in product(COLOURS, repeat=8):
        if level is not None and off_count(word) > level:
            continue
        row = {}
        for u, v in EDGES:
            residual = tuple(site for site in SITES if site not in (u, v))
            total = Fraction(0)
            for matching in PM6[residual]:
                term = Fraction(1)
                for a, b in matching:
                    term *= cell(source, a, b, word[a], word[b])
                    if not term:
                        break
                total += term
            if total:
                row[COORD_INDEX[u, v, word[u], word[v]]] = total
        rows.append(row)
    return rows


def rational_rank(rows, columns):
    matrix = [[Fraction(value) for value in row] for row in rows]
    rank = 0
    for column in range(columns):
        pivot = next((index for index in range(rank, len(matrix))
                      if matrix[index][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale = matrix[rank][column]
        matrix[rank] = [value / scale for value in matrix[rank]]
        for index in range(len(matrix)):
            if index == rank or not matrix[index][column]:
                continue
            factor = matrix[index][column]
            matrix[index] = [left - factor * right
                             for left, right in zip(matrix[index],
                                                    matrix[rank], strict=True)]
        rank += 1
    return rank


def rational_nullspace(rows, columns):
    matrix = [[Fraction(value) for value in row] for row in rows]
    pivot_columns = []
    rank = 0
    for column in range(columns):
        pivot = next((index for index in range(rank, len(matrix))
                      if matrix[index][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale = matrix[rank][column]
        matrix[rank] = [value / scale for value in matrix[rank]]
        for index in range(len(matrix)):
            if index == rank or not matrix[index][column]:
                continue
            factor = matrix[index][column]
            matrix[index] = [left - factor * right
                             for left, right in zip(matrix[index],
                                                    matrix[rank], strict=True)]
        pivot_columns.append(column)
        rank += 1
    free_columns = [column for column in range(columns)
                    if column not in pivot_columns]
    basis = []
    for free in free_columns:
        vector = [Fraction(0)] * columns
        vector[free] = 1
        for row, pivot in zip(matrix[:rank], pivot_columns, strict=True):
            vector[pivot] = -row[free]
        denominator = lcm(*(value.denominator for value in vector))
        integers = [int(value * denominator) for value in vector]
        divisor = gcd(*(abs(value) for value in integers if value))
        integers = [value // divisor for value in integers]
        first = next(value for value in integers if value)
        if first < 0:
            integers = [-value for value in integers]
        basis.append(integers)
    return basis


def t0_stabilizer(source):
    # Coordinates u_(site,colour), followed by the three pure-character
    # equations and one support equation u_(i,a)+u_(j,b)=0 per live cell.
    rows = []
    for colour in COLOURS:
        row = [0] * 24
        for site in SITES:
            row[3 * site + colour] = 1
        rows.append(row)
    live_cells = 0
    for u, v, a, b in COORDS:
        if not cell(source, u, v, a, b):
            continue
        live_cells += 1
        row = [0] * 24
        row[3 * u + a] += 1
        row[3 * v + b] += 1
        rows.append(row)
    rank = rational_rank(rows, 24)
    basis = rational_nullspace(rows, 24)
    stabilizer = 24 - rank
    require(len(basis) == stabilizer, (rank, stabilizer, basis))
    orbit = 21 - stabilizer
    return {
        "live_cells": live_cells,
        "constraint_rank": rank,
        "T0_dimension": 21,
        "source_T0_stabilizer_dimension": stabilizer,
        "primitive_stabilizer_basis_site_major": basis,
        "T0_orbit_dimension": orbit,
        "equivariant_rank_upper_bound_at_exact_target": 252 - orbit,
    }


def carrier_response_interface():
    """Literal matching partition distinguishing carrier rows from dF."""
    # Fix p,q and the six residual vertices.  A matching either uses pq,
    # leaving one of 15 residual matchings, or sends p,q to an unordered
    # residual pair a,b in either order and matches the remaining four sites.
    through_pair = len(perfect_matchings(range(6)))
    residual_pairs = len(tuple(combinations(range(6), 2)))
    arm_orders = 2
    residual_four_matchings = len(perfect_matchings(range(4)))
    avoiding_pair = residual_pairs * arm_orders * residual_four_matchings
    require((through_pair, avoiding_pair, through_pair + avoiding_pair) ==
            (15, 90, 105),
            (through_pair, avoiding_pair))
    star_forbidden = 15 - 5
    triangle_forbidden = 15 - 3
    require((9 * star_forbidden, 9 * triangle_forbidden) == (90, 108),
            (star_forbidden, triangle_forbidden))

    def literal_cell(u, v, a, b):
        return (u, v, a, b) if u < v else (v, u, b, a)

    def monomial(cells):
        return tuple(sorted(cells))

    # Canonical-pair exact source-label replay. Site symmetry transports it
    # to all 28 physical pairs. This verifies the formula, not just its count.
    p, q = 0, 1
    residual = tuple(range(2, 8))
    labelled_terms_checked = 0
    for endpoint_colours in product(COLOURS, repeat=2):
        for residual_colours in product(COLOURS, repeat=6):
            word = list(endpoint_colours + residual_colours)
            direct = Counter()
            for matching in PM8:
                direct[monomial(literal_cell(u, v, word[u], word[v])
                                for u, v in matching)] += 1
            sliced = Counter()
            for tail in perfect_matchings(residual):
                cells = [literal_cell(p, q, *endpoint_colours)]
                cells.extend(literal_cell(u, v, word[u], word[v])
                             for u, v in tail)
                sliced[monomial(cells)] += 1
            for a, b in combinations(residual, 2):
                rest = tuple(site for site in residual if site not in (a, b))
                for tail in perfect_matchings(rest):
                    tail_cells = [literal_cell(u, v, word[u], word[v])
                                  for u, v in tail]
                    sliced[monomial(tail_cells + [
                        literal_cell(p, a, endpoint_colours[0], word[a]),
                        literal_cell(q, b, endpoint_colours[1], word[b]),
                    ])] += 1
                    sliced[monomial(tail_cells + [
                        literal_cell(p, b, endpoint_colours[0], word[b]),
                        literal_cell(q, a, endpoint_colours[1], word[a]),
                    ])] += 1
            require(direct == sliced,
                    (endpoint_colours, residual_colours, direct - sliced,
                     sliced - direct))
            labelled_terms_checked += sum(direct.values())
    require(labelled_terms_checked == 6561 * 105, labelled_terms_checked)

    # Exact second-derivative identification on canonical labels. Fix
    # p,q,a,b=0,1,2,3 and differentiate by the complementary matching
    # 45|67. The remaining four-site Hafnian has precisely the direct
    # pq|ab term and the two arm-order terms making rho.
    hessian_terms_checked = 0
    differentiated_edges = {(4, 5), (6, 7)}
    for word in product(COLOURS, repeat=8):
        observed = Counter()
        for matching in PM8:
            if not differentiated_edges <= set(matching):
                continue
            remainder = [literal_cell(u, v, word[u], word[v])
                         for u, v in matching if (u, v) not in differentiated_edges]
            observed[monomial(remainder)] += 1
        expected = Counter({
            monomial((literal_cell(0, 1, word[0], word[1]),
                      literal_cell(2, 3, word[2], word[3]))): 1,
            monomial((literal_cell(0, 2, word[0], word[2]),
                      literal_cell(1, 3, word[1], word[3]))): 1,
            monomial((literal_cell(0, 3, word[0], word[3]),
                      literal_cell(1, 2, word[1], word[2]))): 1,
        })
        require(observed == expected, (word, observed, expected))
        hessian_terms_checked += sum(observed.values())
    require(hessian_terms_checked == 6561 * 3, hessian_terms_checked)
    return {
        "fixed_pair_slice": (
            "For residual word z, Phi_(pq,z)[i,j]=F_(i,j,z). Literal "
            "matching partition gives Phi=H6(z)*s_pq + "
            "sum_(a<b in U) H4(z without a,b)*rho_ab^(z_a,z_b)."
        ),
        "matching_partition": {
            "matchings_using_pq": through_pair,
            "matchings_avoiding_pq": avoiding_pair,
            "avoiding_factorization": "15 residual pairs * 2 arm orders * 3 four-site matchings",
            "total": through_pair + avoiding_pair,
            "canonical_pair_source_label_terms_checked": labelled_terms_checked,
            "transport_to_all_pairs": "S8 site relabelling",
        },
        "global_first_jacobian_pair_block": (
            "For rows (i,j,z) and columns A_pq[k,l], "
            "dF/dA_pq = delta_((i,j),(k,l))*H6(z). Thus each fixed-z "
            "9x9 Jacobian slice is H6(z)*I9, of source degree 3."
        ),
        "carrier_matrix": (
            "rho_ab^(alpha,beta)[i,j]="
            "A_pa[i,alpha]A_qb[j,beta]+A_pb[i,beta]A_qa[j,alpha]. "
            "It has source degree 2. Stacking forbidden rows gives 90x9 "
            "for a star and 108x9 for a triangle."
        ),
        "radial_relation": (
            "Only H6(z)*s_pq is the radial contraction of the true "
            "Jacobian pair block with the existing pair block A_pq."
        ),
        "quotient_scope": (
            "The quotient C*/W_C kills the span of forbidden quadratic "
            "rho rows inside the nine-dimensional cap dual. It is not a "
            "quotient of the 6561-dimensional codomain of dF and supplies "
            "no first-Jacobian rank additivity across carriers."
        ),
        "degree_guard": {
            "dF_entries_source_degree": 3,
            "carrier_response_entries_source_degree": 2,
            "identical_as_polynomial_blocks": False,
        },
        "second_derivative_identification": {
            "formula": (
                "For any perfect matching M of U minus {a,b}, and the word "
                "with colours (i,j,alpha,beta,z), differentiating F_w by "
                "the two source cells of M gives Haf_4(p,q,a,b)="
                "A_pq[i,j]A_ab[alpha,beta]+rho_ab^(alpha,beta)[i,j]."
            ),
            "canonical_source_label_terms_checked": hessian_terms_checked,
            "consequence": (
                "rho is a literal Hessian block after subtracting the direct "
                "rank-one A_pq tensor A_ab term. The carrier machinery belongs "
                "to the second fundamental form, not to first-Jacobian rank."
            ),
        },
    }


def control_audit(name, source, satisfied_level):
    stabilizer = t0_stabilizer(source)
    profiles = {}
    for label, level in (("X3", 3), ("X4", 4), ("full_F", None)):
        prime_records = []
        for prime in PRIMES:
            rows, outputs, defects = jacobian_rows_mod(source, prime, level)
            prime_records.append({
                "prime": prime,
                "rank": sparse_rank_mod(rows, prime),
                "rows": len(rows),
                "defects": len(defects),
            })
        require(len({record["rank"] for record in prime_records}) == 1,
                (name, label, prime_records))
        require(len({record["defects"] for record in prime_records}) == 1,
                (name, label, prime_records))
        q_rows = jacobian_rows_q(source, level)
        exact_rank = sparse_rank_q(q_rows)
        require(exact_rank == prime_records[0]["rank"],
                (name, label, exact_rank, prime_records))
        zero_columns = {index for index, (u, v, a, b) in enumerate(COORDS)
                        if not cell(source, u, v, a, b)}
        live_columns = set(range(252)) - zero_columns
        zero_rank = sparse_rank_q([
            {column: value for column, value in row.items()
             if column in zero_columns} for row in q_rows])
        live_rank = sparse_rank_q([
            {column: value for column, value in row.items()
             if column in live_columns} for row in q_rows])
        structural_matching = structural_column_row_matching(q_rows)
        require(structural_matching >= exact_rank,
                (name, label, structural_matching, exact_rank))
        profiles[label] = {
            "prime_records": prime_records,
            "common_modular_rank": prime_records[0]["rank"],
            "exact_Q_rank": exact_rank,
            "zero_source_coordinate_columns": len(zero_columns),
            "zero_coordinate_submatrix_exact_Q_rank": zero_rank,
            "live_source_coordinate_columns": len(live_columns),
            "live_coordinate_submatrix_exact_Q_rank": live_rank,
            "evaluated_nonzero_pattern_maximum_matching": structural_matching,
            "common_defect_count": prime_records[0]["defects"],
        }
    bound = stabilizer["equivariant_rank_upper_bound_at_exact_target"]
    satisfied_rank = profiles[f"X{satisfied_level}"]["common_modular_rank"]
    require(profiles[f"X{satisfied_level}"]["common_defect_count"] == 0,
            (name, profiles[f"X{satisfied_level}"]))
    require(satisfied_rank <= bound, (name, satisfied_rank, bound))
    profiles[f"X{satisfied_level}"]["rank_231_plus_s_consistency"] = {
        "upper_bound": bound,
        "modular_lower_bound": satisfied_rank,
        "equality_proves_exact_rank": satisfied_rank == bound,
    }
    for profile in profiles.values():
        profile["exact_rank_minus_stabilizer_dimension"] = (
            profile["exact_Q_rank"]
            - stabilizer["source_T0_stabilizer_dimension"]
        )
    return {"stabilizer": stabilizer, "jacobian_profiles": profiles}


def build_result():
    for path, digest in PINS.items():
        require(file_sha(path) == digest, (str(path), file_sha(path), digest))
    w40_source = parse_source(W40, "W40")
    w25_source = parse_source(W25, "W25")
    w40 = control_audit("W40", w40_source, 4)
    w25 = control_audit("W25", w25_source, 3)
    return {
        "status": "PASS exact/modular equivariant differential-rank controls",
        "theorem_interface": {
            "identity": (
                "For X in Lie(T0), dF_A(X.A)=X.F(A). At F(A)=GHZ the "
                "right side is zero because sum_i X_(i,c)=0 for each c."
            ),
            "rank_bound": "rank(dF_A) <= 252-(21-s)=231+s",
            "sharp_contradiction_target": (
                "X5 plus simultaneous no-cap implies rank(dF_A)-s >= 232; "
                "equivariance gives rank(dF_A)-s <= 231."
            ),
            "torus_complex": (
                "For basis cocharacter e_(i,c)-e_(7,c), the tangent column "
                "G has entry A_uv[a,b]*(delta_(u,a),(i,c)+"
                "delta_(v,b),(i,c)-delta_(u,a),(7,c)-"
                "delta_(v,b),(7,c)). Semi-invariance gives "
                "J*G=(1_(w_i=c)-1_(w_7=c))*F_w, hence J*G=0 at GHZ."
            ),
            "equivalent_kernel_target": (
                "dim ker(J_A) <= 20-s, whereas the T0 orbit already has "
                "dimension 21-s. Infinitesimal rigidity modulo T0 alone "
                "only gives equality rank(J)=231+s and is not a contradiction."
            ),
            "scope": "The bound applies only where every audited output row equals its T0-fixed target.",
        },
        "carrier_response_vs_global_jacobian": carrier_response_interface(),
        "second_fundamental_form": {
            "definition": (
                "At an exact point put V=ker(J_A), O=im(G_A), and "
                "N=coker(J_A). Then II_A:Sym^2(V/O)->N sends "
                "([v],[w]) to [D^2F_A(v,w)]."
            ),
            "descent_identity": (
                "Equivariance gives D^2F_A(G_X A,v)+"
                "J_A(G_X v)=X.J_A(v). For v in ker(J_A), the first term "
                "lies in im(J_A), so II descends modulo the T0 orbit."
            ),
            "dual_normal_requirement": (
                "A scalar Hessian form is induced only by a conormal "
                "lambda in ker(J_A^T). A carrier K is merely a covector on "
                "one nine-output slice; L_C K=0 or ell in rowspan(L_C) "
                "does not imply lambda J_A=0."
            ),
            "GHZ_normal_direction_guard": (
                "Euler homogeneity gives J_A(A)=4F(A)=4GHZ. Therefore the "
                "GHZ output direction is zero in coker(J_A); it cannot be "
                "a nonzero normal obstruction. Any II obstruction must use "
                "a genuinely mixed conormal direction."
            ),
            "bounded_controls": hessian_carrier_controls(w40_source,
                                                           w25_source),
            "verdict": (
                "One blocker is not isotropy/radical membership, and the "
                "728 blocked-carrier conditions do not by themselves define "
                "conormals of II. A missing source identity must first lift "
                "a compatible family of carrier slice covectors into "
                "ker(J_A^T)."
            ),
        },
        "bounded_pairwise_conormal_lift": conormal_overlap_test(w40_source,
                                                                 w25_source),
        "controls": {"W40": w40, "W25": w25},
        "support6_support8_scope": {
            "rank_evaluation_available": False,
            "reason": (
                "The frozen support6, support8, and positive-dimensional "
                "branch-1 charts are one-colour diagonal components/support "
                "records, not 252-coordinate three-colour X5 points. Their "
                "fixed-left mate units exclude assembling the required "
                "partner colours. A global dF rank on those records is "
                "therefore undefined rather than an omitted computation."
            ),
            "available_exact_stabilizer_control": (
                "Across the 310 three-colour minimal support records, the "
                "frozen support-weight audit has stabilizer dimensions "
                "0,1,2,3 with representative counts 187,91,26,6; those are "
                "support records, not coefficient-realizable X5 points."
            ),
        },
        "rank_attack_verdict": {
            "rank_minus_s_target_is_sharp": True,
            "carrier_matrices_directly_prove_rank_lower_bound": False,
            "rational_non_X5_guard": (
                "W25 is all-blocked with s=1 and rank(dF_X3)-s=209, so "
                "no-cap does not force a free T0 orbit or rank threshold at "
                "the lower rung. Its full rank-minus-s is 244 only after "
                "including 103 violated output rows."
            ),
            "smallest_missing_lemma": (
                "Derive 232+s independent cubic cofactor rows from the "
                "X5 equations on each fixed carrier rank/membership branch. "
                "The existing quadratic rho rowspaces do not furnish them."
            ),
            "hall_obstruction": (
                "W40 X4 has exact rank 240 and s=9, but its evaluated "
                "nonzero-entry graph has a column-row matching of size 244. "
                "Thus Hall can select more than the forbidden target 241; "
                "torus/source identities cancel every such determinant. A "
                "support-only or nonzero-cofactor selection cannot prove the minor."
            ),
            "next_derivative_order": (
                "Use the Hessian-induced second fundamental form on "
                "ker(J)/im(G). Carrier rho rows occur there exactly after "
                "subtracting A_pq tensor A_ab. Test whether fixed no-cap "
                "membership makes every non-torus first-order deformation "
                "second-order obstructed."
            ),
        },
        "pinned_inputs": {str(path.relative_to(ROOT)): digest
                          for path, digest in PINS.items()},
    }


def main(write_results=False):
    result = build_result()
    logical = sha256(json.dumps(result, sort_keys=True,
                                separators=(",", ":")).encode()).hexdigest()
    result["logical_sha256"] = logical
    if write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "logical_sha256": logical,
        "controls": {
            name: {
                "s": row["stabilizer"]["source_T0_stabilizer_dimension"],
                "bound": row["stabilizer"]["equivariant_rank_upper_bound_at_exact_target"],
                "satisfied_rank": row["jacobian_profiles"][
                    "X4" if name == "W40" else "X3"]["common_modular_rank"],
                "full_rank": row["jacobian_profiles"]["full_F"]["common_modular_rank"],
            } for name, row in result["controls"].items()
        },
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    main(args.write_results)
