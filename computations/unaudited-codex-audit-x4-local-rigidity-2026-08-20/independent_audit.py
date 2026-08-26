#!/usr/bin/env python3
"""Independent audit of the W40 X4 local-rigidity claim.

This script deliberately imports no code from the producer directory.  It
reconstructs the endpoint-ordered integral W40 point from its 20 nonzero
cells, checks that reconstruction against a pinned historical JSON file, and
builds the raw X4 Jacobian in two different ways:

  * differentiation term-by-term through all 105 perfect matchings of K8;
  * six-site hafnian cofactors obtained by a subset recurrence.

All arithmetic is exact and uses only the Python standard library.  The
output is deterministic so the script can be run under python, python -O,
and python -I -S without weakening any assertion.

UNAUDITED audit artifact.  Writes only beside itself.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PINNED = (ROOT / "computations/unaudited-x4general-w40-2026-08-20/"
          "results_t3.json")
PINNED_SHA256 = "30ad242d62b5cb905858842ce4e8255b105862dc21a65c73c080557fa8c1617f"

N = 8
SITES = tuple(range(N))
COLORS = tuple(range(3))
EDGES = tuple(combinations(SITES, 2))
COORDS = tuple((u, v, a, b) for u, v in EDGES
               for a in COLORS for b in COLORS)
COORD_INDEX = {coordinate: i for i, coordinate in enumerate(COORDS)}

# This is the endpoint-ordered source itself, not a generated parametrization.
# The other 232 endpoint-ordered cells are zero.
W40_NONZERO = {
    (0, 1, 0, 0): 1,
    (0, 3, 1, 1): 1,
    (0, 4, 0, 1): 1,
    (0, 4, 2, 2): 1,
    (0, 5, 1, 0): 1,
    (0, 6, 0, 2): 1,
    (1, 2, 0, 2): 1,
    (1, 2, 1, 1): 1,
    (1, 3, 2, 2): 1,
    (1, 7, 0, 1): -1,
    (2, 3, 0, 0): 1,
    (2, 4, 2, 1): 1,
    (2, 6, 2, 2): -1,
    (3, 4, 1, 0): -1,
    (4, 5, 0, 0): 1,
    (4, 7, 1, 1): 1,
    (5, 6, 1, 1): 1,
    (5, 7, 2, 2): -1,
    (6, 7, 0, 0): 1,
    (6, 7, 2, 1): 1,
}

DECLARED_CONTROLS = {
    "pinned_file_hash",
    "hardcoded_source_equals_pinned_source",
    "matching_count_105",
    "x4_point_and_three_level5_defects",
    "two_independent_jacobians",
    "mutation_breaks_x4",
    "jacobian_minor_nonzero",
    "zero_transversal_minor_nonzero",
    "gauge_minor_nonzero",
    "jacobian_annihilates_gauge",
    "corrupt_gauge_must_fail",
    "pair67_active_clean_cap",
    "cap_gauge_covariance",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def file_sha256(path):
    return sha256(path.read_bytes()).hexdigest()


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        remainder = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(remainder):
            yield ((first, second),) + tail


PM8 = tuple(perfect_matchings(SITES))
PM6 = tuple(perfect_matchings(tuple(range(6))))


def source_from_nonzero(entries=W40_NONZERO):
    return {coordinate: Fraction(entries.get(coordinate, 0))
            for coordinate in COORDS}


def parse_pinned_source():
    record = json.loads(PINNED.read_text())
    raw = record["engine_audit"]["witness_B_integral"]["source"]
    source = {}
    for edge_text, matrix in raw.items():
        u, v = (int(piece.strip())
                for piece in edge_text.strip("()").split(","))
        for a in COLORS:
            for b in COLORS:
                source[(u, v, a, b)] = Fraction(matrix[a][b])
    require(set(source) == set(COORDS), "pinned source has wrong coordinates")
    return source


def cell(source, u, v, a, b):
    if u < v:
        return source[(u, v, a, b)]
    return source[(v, u, b, a)]


def off_count(word):
    return N - max(word.count(c) for c in COLORS)


def amplitude_matching(source, word):
    total = Fraction(0)
    for matching in PM8:
        term = Fraction(1)
        for u, v in matching:
            term *= cell(source, u, v, word[u], word[v])
            if not term:
                break
        total += term
    return total


def six_hafnian_subset(source, word, omitted):
    """Six-site cofactor via a subset recurrence, not PM differentiation."""
    mask = (1 << N) - 1
    for site in omitted:
        mask &= ~(1 << site)
    memo = {0: Fraction(1)}

    def rec(current):
        if current in memo:
            return memo[current]
        u = (current & -current).bit_length() - 1
        remainder = current & ~(1 << u)
        answer = Fraction(0)
        scan = remainder
        while scan:
            v = (scan & -scan).bit_length() - 1
            scan &= ~(1 << v)
            answer += cell(source, u, v, word[u], word[v]) * rec(
                remainder & ~(1 << v)
            )
        memo[current] = answer
        return answer

    return rec(mask)


def direct_matching_value_and_gradient(source, word):
    """Differentiate the 105 matching monomials term by term."""
    value = Fraction(0)
    gradient = {}
    for matching in PM8:
        weights = [cell(source, u, v, word[u], word[v])
                   for u, v in matching]
        term = Fraction(1)
        for weight in weights:
            term *= weight
        value += term
        for selected, (u, v) in enumerate(matching):
            derivative = Fraction(1)
            for index, weight in enumerate(weights):
                if index != selected:
                    derivative *= weight
            if derivative:
                coordinate = COORD_INDEX[(u, v, word[u], word[v])]
                gradient[coordinate] = gradient.get(
                    coordinate, Fraction(0)
                ) + derivative
    return value, {c: x for c, x in gradient.items() if x}


def cofactor_gradient(source, word):
    row = {}
    for u, v in EDGES:
        coefficient = six_hafnian_subset(source, word, (u, v))
        if coefficient:
            row[COORD_INDEX[(u, v, word[u], word[v])]] = coefficient
    return row


def build_x4_jacobians(source):
    direct_rows = []
    cofactor_rows = []
    row_words = []
    values = {}
    defects = []
    for word in product(COLORS, repeat=N):
        value, direct = direct_matching_value_and_gradient(source, word)
        target = Fraction(1) if len(set(word)) == 1 else Fraction(0)
        values[word] = value
        if value != target:
            defects.append((word, off_count(word), value))
        if off_count(word) <= 4:
            cofactor = cofactor_gradient(source, word)
            require(direct == cofactor,
                    ("Jacobian disagreement", word, direct, cofactor))
            direct_rows.append(direct)
            cofactor_rows.append(cofactor)
            row_words.append("".join(map(str, word)))
    require(direct_rows == cofactor_rows, "Jacobian arrays differ")
    return direct_rows, row_words, values, defects


def sparse_rank_and_minor(rows, ncols, prime=1_000_003):
    """Row-echelon rank over F_p, retaining one certified square minor."""
    pivots = {}
    chosen_rows = []
    for row_index, original in enumerate(rows):
        row = {column: int(value) % prime
               for column, value in original.items()
               if int(value) % prime}
        while row:
            pivot_column = min(row)
            previous = pivots.get(pivot_column)
            if previous is None:
                inverse = pow(row[pivot_column], prime - 2, prime)
                pivots[pivot_column] = {
                    column: value * inverse % prime
                    for column, value in row.items() if value % prime
                }
                chosen_rows.append(row_index)
                break
            multiplier = row[pivot_column]
            for column, value in previous.items():
                reduced = (row.get(column, 0) - multiplier * value) % prime
                if reduced:
                    row[column] = reduced
                else:
                    row.pop(column, None)
    return len(pivots), chosen_rows, sorted(pivots)


def dense_minor(rows, selected_rows, selected_columns):
    position = {column: index
                for index, column in enumerate(selected_columns)}
    matrix = [[0] * len(selected_columns) for _ in selected_rows]
    for i, row_index in enumerate(selected_rows):
        for column, value in rows[row_index].items():
            if column in position:
                require(value.denominator == 1, (row_index, column, value))
                matrix[i][position[column]] = value.numerator
    return matrix


def bareiss_determinant(matrix):
    """Exact fraction-free determinant with row pivoting."""
    a = [row[:] for row in matrix]
    size = len(a)
    require(all(len(row) == size for row in a), "minor is not square")
    if size == 0:
        return 1
    sign = 1
    previous_pivot = 1
    for k in range(size - 1):
        pivot_row = next((r for r in range(k, size) if a[r][k]), None)
        require(pivot_row is not None, ("singular selected minor", k))
        if pivot_row != k:
            a[k], a[pivot_row] = a[pivot_row], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k + 1, size):
            left = a[i][k]
            row_i = a[i]
            row_k = a[k]
            for j in range(k + 1, size):
                numerator = row_i[j] * pivot - left * row_k[j]
                quotient, remainder = divmod(numerator, previous_pivot)
                require(remainder == 0,
                        ("non-exact Bareiss division", k, i, j))
                row_i[j] = quotient
            row_i[k] = 0
        previous_pivot = pivot
    return sign * a[-1][-1]


def matmul_sparse(left_rows, right_rows):
    """Multiply sparse row matrices, with right indexed by its rows."""
    answer = []
    for row in left_rows:
        image = {}
        for middle, left_value in row.items():
            for column, right_value in right_rows[middle].items():
                image[column] = image.get(column, Fraction(0)) + (
                    left_value * right_value
                )
        answer.append({c: x for c, x in image.items() if x})
    return answer


def normalized_gauge_tangent(source):
    """252-by-21 differential of product-one diagonal site/color gauge."""
    tangent = []
    for u, v, a, b in COORDS:
        value = source[(u, v, a, b)]
        row = {}
        if value:
            # Parameters are eta_(site,color), site=0,...,6.  The product-one
            # constraint sets eta_(7,color)=-sum_{site<7} eta_(site,color).
            row[3 * u + a] = row.get(3 * u + a, Fraction(0)) + value
            if v < 7:
                row[3 * v + b] = row.get(
                    3 * v + b, Fraction(0)
                ) + value
            else:
                for site in range(7):
                    row[3 * site + b] = row.get(
                        3 * site + b, Fraction(0)
                    ) - value
        tangent.append({c: x for c, x in row.items() if x})
    return tangent


def corrupted_gauge_tangent(source):
    """Negative control: incorrectly freeze all site-7 gauge parameters."""
    tangent = []
    for u, v, a, b in COORDS:
        value = source[(u, v, a, b)]
        row = {}
        if value:
            row[3 * u + a] = row.get(3 * u + a, Fraction(0)) + value
            if v < 7:
                row[3 * v + b] = row.get(
                    3 * v + b, Fraction(0)
                ) + value
        tangent.append({c: x for c, x in row.items() if x})
    return tangent


def response(source, cap, K):
    p, q = cap
    residual = tuple(site for site in SITES if site not in cap)
    answer = {}
    for a, b in combinations(residual, 2):
        for alpha in COLORS:
            for beta in COLORS:
                total = Fraction(0)
                for i in COLORS:
                    for j in COLORS:
                        total += K[i][j] * (
                            cell(source, p, a, i, alpha)
                            * cell(source, q, b, j, beta)
                            + cell(source, p, b, i, beta)
                            * cell(source, q, a, j, alpha)
                        )
                answer[(a, b, alpha, beta)] = total
    return answer


def cap_scalar(source, cap, K):
    p, q = cap
    return sum((cell(source, p, q, i, j) * K[i][j]
                for i in COLORS for j in COLORS), Fraction(0))


def response_cell(response_data, u, v, a, b):
    if u < v:
        return response_data[(u, v, a, b)]
    return response_data[(v, u, b, a)]


def cap_error_values(source, cap, K):
    """Coefficients of s*r^2*x/2 + r^3/6 on the six residual sites."""
    residual = tuple(site for site in SITES if site not in cap)
    scalar = cap_scalar(source, cap, K)
    rdata = response(source, cap, K)
    errors = {}
    for local_word in product(COLORS, repeat=6):
        word = dict(zip(residual, local_word))
        total = Fraction(0)
        for matching_local in PM6:
            matching = tuple((residual[i], residual[j])
                             for i, j in matching_local)
            # r^3/6: one contribution for each perfect matching.
            r_product = Fraction(1)
            for u, v in matching:
                r_product *= response_cell(rdata, u, v, word[u], word[v])
            total += r_product
            # s*r^2*x/2: choose the unique x edge in the matching.
            for x_index, (x_u, x_v) in enumerate(matching):
                term = scalar * cell(
                    source, x_u, x_v, word[x_u], word[x_v]
                )
                for r_index, (u, v) in enumerate(matching):
                    if r_index != x_index:
                        term *= response_cell(rdata, u, v,
                                              word[u], word[v])
                total += term
        errors[local_word] = total
    return scalar, rdata, errors


def scaled_source_and_dual_cap(source, K, lambdas):
    scaled = {}
    for u, v, a, b in COORDS:
        scaled[(u, v, a, b)] = (
            lambdas[u][a] * lambdas[v][b] * source[(u, v, a, b)]
        )
    p, q = (6, 7)
    dual = tuple(tuple(K[i][j] / (lambdas[p][i] * lambdas[q][j])
                       for j in COLORS) for i in COLORS)
    return scaled, dual


def audit_cap_gauge_covariance(source):
    cap = (6, 7)
    identity = tuple(tuple(Fraction(int(i == j)) for j in COLORS)
                     for i in COLORS)
    scalar, rdata, errors = cap_error_values(source, cap, identity)
    activity = scalar
    for color in COLORS:
        activity *= identity[color][color]
    require(activity == 1, ("pair67 activity", activity))
    require(not any(errors.values()), "pair67 error is not zero")

    # Seven freely chosen values per color, followed by the product-one value
    # at site 7.  Signs are included to ensure covariance is not an artifact
    # of positive or uniform scalings.
    seeds = (
        (Fraction(2), Fraction(3), Fraction(-1), Fraction(1, 2),
         Fraction(5), Fraction(1, 3), Fraction(-2)),
        (Fraction(-1), Fraction(2), Fraction(1, 2), Fraction(3),
         Fraction(-3), Fraction(1, 3), Fraction(4)),
        (Fraction(3), Fraction(-2), Fraction(5), Fraction(1, 5),
         Fraction(2), Fraction(-1, 2), Fraction(7)),
    )
    lambdas = [[Fraction(0) for _ in COLORS] for _ in SITES]
    for color in COLORS:
        running = Fraction(1)
        for site in range(7):
            lambdas[site][color] = seeds[color][site]
            running *= seeds[color][site]
        lambdas[7][color] = 1 / running
        require(product_fraction(lambdas[site][color]
                                 for site in SITES) == 1,
                ("bad product-one gauge", color))

    scaled, dual = scaled_source_and_dual_cap(source, identity, lambdas)
    scalar2, rdata2, errors2 = cap_error_values(scaled, cap, dual)
    require(scalar2 == scalar, (scalar, scalar2))
    residual = tuple(site for site in SITES if site not in cap)
    for a, b in combinations(residual, 2):
        for alpha in COLORS:
            for beta in COLORS:
                expected = (lambdas[a][alpha] * lambdas[b][beta]
                            * rdata[(a, b, alpha, beta)])
                require(rdata2[(a, b, alpha, beta)] == expected,
                        ("response covariance", a, b, alpha, beta))
    for local_word, value in errors.items():
        factor = product_fraction(
            lambdas[site][color]
            for site, color in zip(residual, local_word)
        )
        require(errors2[local_word] == factor * value,
                ("error covariance", local_word))
    activity2 = scalar2
    for color in COLORS:
        activity2 *= dual[color][color]
    require(activity2 != 0 and not any(errors2.values()),
            ("scaled cap lost activity or cleanness", activity2))
    return {
        "cap": "67",
        "original_activity_product": str(activity),
        "scaled_activity_product": str(activity2),
        "residual_error_coefficients_checked_twice": len(errors),
        "response_coefficients_checked": len(rdata),
        "scalar_invariant": True,
        "response_covariance": True,
        "clean_error_covariance": True,
        "active_nonvanishing_invariant": True,
    }


def product_fraction(values):
    answer = Fraction(1)
    for value in values:
        answer *= value
    return answer


def main():
    controls = set()
    require(file_sha256(PINNED) == PINNED_SHA256,
            ("pinned file hash mismatch", file_sha256(PINNED)))
    controls.add("pinned_file_hash")
    source = source_from_nonzero()
    require(source == parse_pinned_source(),
            "hardcoded W40 reconstruction differs from pinned source")
    controls.add("hardcoded_source_equals_pinned_source")
    require(len(PM8) == 105 and len(PM6) == 15, (len(PM8), len(PM6)))
    controls.add("matching_count_105")

    rows, words, values, defects = build_x4_jacobians(source)
    x4_words = sum(off_count(word) <= 4 for word in values)
    require(x4_words == 4881 and len(rows) == 4881, x4_words)
    require(all(values[tuple([c] * N)] == 1 for c in COLORS),
            "pure target failure")
    defect_ledger = [("".join(map(str, word)), off, str(value))
                     for word, off, value in defects]
    require(defect_ledger == [
        ("01110222", 5, "1"),
        ("12221000", 5, "1"),
        ("20002111", 5, "-1"),
    ], defect_ledger)
    controls.add("x4_point_and_three_level5_defects")
    controls.add("two_independent_jacobians")

    mutated = dict(source)
    require(mutated[(2, 6, 2, 2)] == -1, "mutation source cell moved")
    mutated[(2, 6, 2, 2)] = 1
    mutation_failures = []
    for word_tuple in product(COLORS, repeat=N):
        if off_count(word_tuple) <= 4:
            target = Fraction(1) if len(set(word_tuple)) == 1 else Fraction(0)
            value = amplitude_matching(mutated, word_tuple)
            if value != target:
                mutation_failures.append(
                    ("".join(map(str, word_tuple)), str(value - target))
                )
    require(len(mutation_failures) == 4, mutation_failures)
    controls.add("mutation_breaks_x4")

    rank_p1, selected_rows, selected_columns = sparse_rank_and_minor(
        rows, len(COORDS), 1_000_003
    )
    rank_p2, _, _ = sparse_rank_and_minor(rows, len(COORDS), 1_000_033)
    full_minor = dense_minor(rows, selected_rows, selected_columns)
    full_det = bareiss_determinant(full_minor)
    require(rank_p1 == rank_p2 == 240, (rank_p1, rank_p2))
    require(abs(full_det) == 2 ** 33, full_det)
    controls.add("jacobian_minor_nonzero")

    zero_columns = [index for index, coordinate in enumerate(COORDS)
                    if not source[coordinate]]
    zero_position = {column: index
                     for index, column in enumerate(zero_columns)}
    zero_rows = [
        {zero_position[column]: value for column, value in row.items()
         if column in zero_position}
        for row in rows
    ]
    zero_rank, zero_selected_rows, zero_selected_columns = (
        sparse_rank_and_minor(zero_rows, len(zero_columns), 1_000_003)
    )
    zero_det = bareiss_determinant(dense_minor(
        zero_rows, zero_selected_rows, zero_selected_columns
    ))
    require(zero_rank == 232 and abs(zero_det) == 2 ** 33,
            (zero_rank, zero_det))
    controls.add("zero_transversal_minor_nonzero")

    gauge = normalized_gauge_tangent(source)
    gauge_rank, gauge_selected_rows, gauge_selected_columns = (
        sparse_rank_and_minor(gauge, 21, 1_000_003)
    )
    gauge_det = bareiss_determinant(dense_minor(
        gauge, gauge_selected_rows, gauge_selected_columns
    ))
    require(gauge_rank == 12 and abs(gauge_det) == 1,
            (gauge_rank, gauge_det))
    controls.add("gauge_minor_nonzero")
    composed = matmul_sparse(rows, gauge)
    require(not any(composed), "X4 Jacobian does not annihilate gauge")
    controls.add("jacobian_annihilates_gauge")
    corrupted_composed = matmul_sparse(rows, corrupted_gauge_tangent(source))
    corrupt_nonzero = sum(bool(row) for row in corrupted_composed)
    require(corrupt_nonzero > 0, "corrupted gauge control did not fire")
    controls.add("corrupt_gauge_must_fail")

    cap_audit = audit_cap_gauge_covariance(source)
    controls.add("pair67_active_clean_cap")
    controls.add("cap_gauge_covariance")

    # The determinant gives rank(J)>=240 over Q.  A 12-dimensional subspace
    # in ker(J) gives rank(J)<=240, so this is an exact rank proof independent
    # of trusting modular rank as an upper bound.
    require(full_det and gauge_rank == 12 and not any(composed),
            "exact rank sandwich failed")
    require(controls == DECLARED_CONTROLS,
            {"declared": sorted(DECLARED_CONTROLS),
             "executed": sorted(controls)})

    omitted = [str(COORDS[index]) for index in range(len(COORDS))
               if index not in selected_columns]
    result = {
        "status": "PASS",
        "classification": "INDEPENDENT PROMOTION-STYLE AUDIT",
        "source": {
            "pinned_file": str(PINNED.relative_to(ROOT)),
            "pinned_sha256": PINNED_SHA256,
            "nonzero_endpoint_ordered_cells": len(W40_NONZERO),
            "zero_endpoint_ordered_cells": 252 - len(W40_NONZERO),
            "hardcoded_reconstruction_equals_pinned_source": True,
        },
        "x4": {
            "raw_equations": x4_words,
            "jacobian_rows": len(rows),
            "ambient_coordinates": len(COORDS),
            "jacobian_nonzero_entries": sum(len(row) for row in rows),
            "two_derivative_engines_agree": True,
            "rank_mod_1000003": rank_p1,
            "rank_mod_1000033": rank_p2,
            "rank_over_Q_by_exact_sandwich": 240,
            "tangent_dimension_over_Q": 12,
            "rank_minor_size": len(selected_rows),
            "rank_minor_determinant": str(full_det),
            "rank_minor_factorization": "2^33 up to sign",
            "rank_minor_word_sha256": sha256(
                "\n".join(words[index] for index in selected_rows).encode()
            ).hexdigest(),
            "rank_minor_omitted_coordinates": omitted,
            "non_X4_defects": defect_ledger,
        },
        "fixed_nonzero_cell_transversal": {
            "coordinates": len(zero_columns),
            "rank": zero_rank,
            "minor_determinant": str(zero_det),
            "minor_factorization": "2^33 up to sign",
        },
        "gauge": {
            "target_preserving_torus_dimension": 21,
            "orbit_tangent_rank": gauge_rank,
            "gauge_rank_minor_determinant": str(gauge_det),
            "jacobian_times_gauge_is_zero": True,
            "corrupt_unnormalized_gauge_nonzero_rows": corrupt_nonzero,
            "active_cap_gauge_covariance": cap_audit,
        },
        "field_scope": {
            "rank_minor": (
                "nonzero in characteristic zero and every odd characteristic"
            ),
            "local_germ_conclusion_audited_here": "characteristic zero",
            "characteristic_2": "not decided",
        },
        "local_theorem": (
            "Over a characteristic-zero field, the raw X4 scheme is smooth "
            "of local dimension 12 at the integral W40 point.  Its scheme-"
            "theoretic Zariski local germ there equals the germ of the "
            "target-preserving diagonal-gauge orbit.  Hence over C there is "
            "a Zariski (and therefore analytic) neighborhood in X4 on which "
            "the active clean cap property persists."
        ),
        "logical_inference": [
            "The nonzero 240x240 Jacobian minor gives tangent dimension at most 12.",
            "The target-preserving torus orbit lies in X4 and has tangent rank 12, so local dimension is at least 12.",
            "Local dimension and tangent dimension are both 12; therefore W40 is a smooth point of X4.",
            "The orbit closure is an irreducible 12-dimensional closed subvariety through W40.  At the regular local ring of the unique local component, its height-zero prime is zero, so the scheme germs agree.",
            "The orbit is open in its closure.  Active clean caps transform by the inverse cap gauge and their nonvanishing/zero conditions are invariant."
        ],
        "limits": [
            "This is local at W40; it gives no universal X4-to-cap theorem.",
            "It does not exclude remote points, other components, or singular loci.",
            "It does not decide characteristic 2."
        ],
        "negative_control": {
            "mutation": "A_(2,6)[2,2] changes from -1 to +1",
            "x4_failures": mutation_failures,
        },
        "controls": {
            "declared": sorted(DECLARED_CONTROLS),
            "executed": sorted(controls),
            "all_ran": True,
        },
    }
    (HERE / "results.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps({
        "status": result["status"],
        "rank": result["x4"]["rank_over_Q_by_exact_sandwich"],
        "tangent_dimension": result["x4"]["tangent_dimension_over_Q"],
        "gauge_rank": result["gauge"]["orbit_tangent_rank"],
        "rank_minor_determinant": result["x4"]["rank_minor_determinant"],
        "zero_minor_determinant": result["fixed_nonzero_cell_transversal"]["minor_determinant"],
        "controls_all_ran": result["controls"]["all_ran"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
