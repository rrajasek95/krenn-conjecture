#!/usr/bin/env python3
"""Independent raw classification of X4 on the 20-cell W40 support.

All X4 coefficients are rebuilt from endpoint-ordered cells and all 105
perfect matchings.  The intended output is an exact Laurent-lattice
description on the open torus where all twenty displayed cells are nonzero.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import product
from itertools import combinations
import json
from pathlib import Path


SITES = tuple(range(8))
COLORS = tuple(range(3))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for k in range(1, len(vertices)):
        v = vertices[k]
        rest = vertices[1:k] + vertices[k + 1:]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


PMS = tuple(perfect_matchings(SITES))

# Endpoint order is literal: (u,v,colour-at-u,colour-at-v), u<v.
SUPPORT = (
    (0, 1, 0, 0), (2, 3, 0, 0), (4, 5, 0, 0), (6, 7, 0, 0),
    (0, 3, 1, 1), (1, 2, 1, 1), (4, 7, 1, 1), (5, 6, 1, 1),
    (0, 4, 0, 1), (0, 5, 1, 0), (1, 7, 0, 1), (3, 4, 1, 0),
    (0, 6, 0, 2), (1, 2, 0, 2), (2, 4, 2, 1), (6, 7, 2, 1),
    (0, 4, 2, 2), (1, 3, 2, 2), (2, 6, 2, 2), (5, 7, 2, 2),
)

# W40-B integral point, used only as a positive control.
POINT = (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, -1,
         1, 1, 1, 1, 1, 1, -1, -1)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


INDEX = {cell: k for k, cell in enumerate(SUPPORT)}
require(len(INDEX) == 20, "support contains duplicate cells")
HERE = Path(__file__).resolve().parent
CERTIFICATE_PATH = HERE / "certificate.json"
ZERO_EXPONENT = (0,) * len(SUPPORT)


def lookup(u, v, cu, cv):
    if u > v:
        u, v, cu, cv = v, u, cv, cu
    return INDEX.get((u, v, cu, cv))


def off_count(word):
    return 8 - max(word.count(c) for c in COLORS)


def polynomial(word):
    """Sparse polynomial dict exponent-vector -> integer coefficient."""
    ans = Counter()
    for matching in PMS:
        factors = []
        for u, v in matching:
            k = lookup(u, v, word[u], word[v])
            if k is None:
                break
            factors.append(k)
        else:
            exponent = [0] * len(SUPPORT)
            for k in factors:
                exponent[k] += 1
            ans[tuple(exponent)] += 1
    if len(set(word)) == 1:
        ans[(0,) * len(SUPPORT)] -= 1
    return {m: c for m, c in ans.items() if c}


def poly_add(left, right):
    answer = Counter(left)
    answer.update(right)
    return {m: c for m, c in answer.items() if c}


def poly_scale(poly, coefficient):
    return {m: coefficient * c for m, c in poly.items() if coefficient * c}


def poly_mul(left, right):
    answer = Counter()
    for a, ca in left.items():
        for b, cb in right.items():
            answer[tuple(x + y for x, y in zip(a, b))] += ca * cb
    return {m: c for m, c in answer.items() if c}


def variable_poly(index):
    exponent = [0] * len(SUPPORT)
    exponent[index] = 1
    return {tuple(exponent): 1}


def source_cell_poly(u, v, cu, cv):
    index = lookup(u, v, cu, cv)
    return {} if index is None else variable_poly(index)


def recursive_hafnian(word, vertices):
    """Second raw engine: recursive polynomial hafnian, no PM table."""
    vertices = tuple(vertices)
    if not vertices:
        return {ZERO_EXPONENT: 1}
    u = vertices[0]
    total = {}
    for position in range(1, len(vertices)):
        v = vertices[position]
        edge = source_cell_poly(u, v, word[u], word[v])
        if not edge:
            continue
        rest = vertices[1:position] + vertices[position + 1:]
        total = poly_add(total, poly_mul(edge, recursive_hafnian(word, rest)))
    return total


def recursive_x4_polynomial(word):
    answer = recursive_hafnian(word, SITES)
    if len(set(word)) == 1:
        answer = poly_add(answer, {ZERO_EXPONENT: -1})
    return answer


def evaluate(poly, point):
    total = Fraction(0)
    for exponent, coefficient in poly.items():
        term = Fraction(coefficient)
        for x, e in zip(point, exponent):
            term *= Fraction(x) ** e
        total += term
    return total


def primitive_relation(poly):
    """Convert a binomial or monomial-minus-constant to d and rhs x^d=rhs."""
    require(len(poly) == 2, poly)
    terms = sorted(poly.items())
    (a, ca), (b, cb) = terms
    d = tuple(x - y for x, y in zip(a, b))
    rhs = Fraction(-cb, ca)
    # Canonicalize orientation.
    for z in d:
        if z:
            if z < 0:
                d = tuple(-x for x in d)
                rhs = 1 / rhs
            break
    return d, rhs


def rational_rank(rows):
    rows = [[Fraction(x) for x in row] for row in rows]
    if not rows:
        return 0
    rank = 0
    width = len(rows[0])
    for col in range(width):
        pivot = next((r for r in range(rank, len(rows)) if rows[r][col]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        q = rows[rank][col]
        rows[rank] = [x / q for x in rows[rank]]
        for r in range(len(rows)):
            if r != rank and rows[r][col]:
                q = rows[r][col]
                rows[r] = [x - q*y for x, y in zip(rows[r], rows[rank])]
        rank += 1
        if rank == len(rows):
            break
    return rank


def determinant(matrix):
    """Exact integer determinant by fraction-free Bareiss elimination."""
    a = [list(row) for row in matrix]
    n = len(a)
    if n == 0:
        return 1
    sign = 1
    previous = 1
    for k in range(n - 1):
        pivot = next((i for i in range(k, n) if a[i][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            sign = -sign
        p = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                a[i][j] = (a[i][j] * p - a[i][k] * a[k][j]) // previous
        for i in range(k + 1, n):
            a[i][k] = 0
        previous = p
    return sign * a[-1][-1]


def unimodular_minor(rows):
    """Find independent rows and an explicit determinant-one column minor."""
    basis = []
    basis_indices = []
    for i, row in enumerate(rows):
        if rational_rank(basis + [row]) > len(basis):
            basis.append(row)
            basis_indices.append(i)
    require(len(basis) == 8, ("relation rank", len(basis)))
    for columns in combinations(range(len(SUPPORT)), 8):
        minor = [[row[j] for j in columns] for row in basis]
        det = determinant(minor)
        if abs(det) == 1:
            return basis_indices, columns, det
    raise RuntimeError("no unimodular rank minor")


def invert(matrix):
    n = len(matrix)
    aug = [[Fraction(x) for x in row] +
           [Fraction(i == j) for j in range(n)]
           for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next(i for i in range(col, n) if aug[i][col])
        aug[col], aug[pivot] = aug[pivot], aug[col]
        q = aug[col][col]
        aug[col] = [x / q for x in aug[col]]
        for i in range(n):
            if i != col and aug[i][col]:
                q = aug[i][col]
                aug[i] = [x - q*y for x, y in zip(aug[i], aug[col])]
    return [row[n:] for row in aug]


def matmul(left, right):
    return [[sum((left[i][k] * right[k][j]
                  for k in range(len(right))), Fraction(0))
             for j in range(len(right[0]))]
            for i in range(len(left))]


def gauge_matrix():
    """20x21 exponent matrix for target-preserving diagonal gauge.

    Coordinates are d[u,c], u=0..6; d[7,c] is the inverse product for its
    colour, enforcing product_u d[u,c]=1.
    """
    answer = []
    for u, v, cu, cv in SUPPORT:
        row = [0] * 21
        for site, colour in ((u, cu), (v, cv)):
            if site < 7:
                row[3 * site + colour] += 1
            else:
                for w in range(7):
                    row[3 * w + colour] -= 1
        answer.append(row)
    return answer


def greedy_rank_minor(matrix):
    rank = rational_rank(matrix)
    row_ids = []
    chosen = []
    for i, row in enumerate(matrix):
        if rational_rank(chosen + [row]) > len(chosen):
            chosen.append(row)
            row_ids.append(i)
    transposed = [[chosen[i][j] for i in range(rank)]
                  for j in range(len(chosen[0]))]
    column_ids = []
    selected_columns = []
    for j, column in enumerate(transposed):
        if rational_rank(selected_columns + [column]) > len(selected_columns):
            selected_columns.append(column)
            column_ids.append(j)
    minor = [[matrix[i][j] for j in column_ids] for i in row_ids]
    return rank, row_ids, column_ids, determinant(minor)


def relation_from_record(record, name_to_index):
    exponent = [0] * len(SUPPORT)
    for name, power in record["exponents"].items():
        exponent[name_to_index[name]] = power
    return tuple(exponent), Fraction(record["rhs"])


def monomial_from_names(names, name_to_index):
    exponent = [0] * len(SUPPORT)
    for name in names:
        exponent[name_to_index[name]] += 1
    return {tuple(exponent): 1}


def cap67_response():
    response = {}
    for a in range(6):
        for b in range(a + 1, 6):
            for alpha in COLORS:
                for beta in COLORS:
                    total = {}
                    for i in COLORS:  # K=I, hence the same colour i.
                        left = poly_mul(source_cell_poly(6, a, i, alpha),
                                        source_cell_poly(7, b, i, beta))
                        right = poly_mul(source_cell_poly(6, b, i, beta),
                                         source_cell_poly(7, a, i, alpha))
                        total = poly_add(total, poly_add(left, right))
                    if total:
                        response[(a, b, alpha, beta)] = total
    scalar = {}
    for i in COLORS:
        scalar = poly_add(scalar, source_cell_poly(6, 7, i, i))
    return scalar, response


def response_cell(response, u, v, cu, cv):
    if u > v:
        u, v, cu, cv = v, u, cv, cu
    return response.get((u, v, cu, cv), {})


def clean_cap_errors(scalar, response):
    """Raw cleared clean-error polynomial on all 729 residual words."""
    errors = {}
    residual = tuple(range(6))
    for colors in product(COLORS, repeat=6):
        word = dict(zip(residual, colors))
        total = {}
        for matching in perfect_matchings(residual):
            rs = [response_cell(response, u, v, word[u], word[v])
                  for u, v in matching]
            xs = [source_cell_poly(u, v, word[u], word[v])
                  for u, v in matching]
            total = poly_add(total, poly_mul(rs[0], poly_mul(rs[1], rs[2])))
            for original in range(3):
                term = poly_mul(scalar, xs[original])
                for k in range(3):
                    if k != original:
                        term = poly_mul(term, rs[k])
                total = poly_add(total, term)
        if total:
            errors["".join(map(str, colors))] = total
    return errors


def main():
    certificate = json.loads(CERTIFICATE_PATH.read_text())
    controls = set()
    declared_controls = {
        "certificate_support_exact",
        "two_raw_engines_all_x4_rows",
        "integral_point_positive",
        "q26_sign_mutation_must_fire",
        "laurent_generators_exact",
        "unimodular_saturation_and_parameterization",
        "gauge_lattice_equality",
        "cap67_raw_response",
        "cap67_all_729_clean_errors",
    }

    certified_support = tuple(tuple(item["cell"])
                              for item in certificate["support"])
    names = tuple(item["name"] for item in certificate["support"])
    name_to_index = {name: i for i, name in enumerate(names)}
    require(certified_support == SUPPORT, "certificate support mismatch")
    require(tuple(certificate["integral_point"]) == POINT,
            "integral point mismatch")
    require([item["index"] for item in certificate["support"]] == list(range(20)),
            "support indices mismatch")
    controls.add("certificate_support_exact")

    raw_rows = {}
    term_counts = Counter()
    mutation_failures = []
    mutant = list(POINT)
    mutant[name_to_index["x26_22"]] *= -1
    for word in product(COLORS, repeat=8):
        if off_count(word) > 4:
            continue
        first = polynomial(word)
        second = recursive_x4_polynomial(word)
        require(first == second, ("raw engines disagree", word))
        term_counts[len(first)] += 1
        require(evaluate(first, POINT) == 0, ("positive point failed", word))
        if evaluate(first, mutant):
            mutation_failures.append("".join(map(str, word)))
        if first:
            raw_rows["".join(map(str, word))] = first
    require(sum(term_counts.values()) == 4881, term_counts)
    require(term_counts == Counter({0: 4869, 2: 12}), term_counts)
    controls.add("two_raw_engines_all_x4_rows")
    controls.add("integral_point_positive")
    require(len(mutation_failures) == 4, mutation_failures)
    controls.add("q26_sign_mutation_must_fire")

    relation_records = certificate["laurent_relations"]
    relation_by_id = {item["id"]: relation_from_record(item, name_to_index)
                      for item in relation_records}
    expected_word_map = certificate["raw_x4"]["nonzero_word_to_relation"]
    require(set(raw_rows) == set(expected_word_map),
            (set(raw_rows), set(expected_word_map)))
    for word, poly in raw_rows.items():
        require(primitive_relation(poly) == relation_by_id[expected_word_map[word]],
                ("relation mismatch", word))
    require(certificate["raw_x4"]["row_count"] == 4881, "row count certificate")
    require(certificate["raw_x4"]["identically_zero_rows"] == 4869,
            "zero row certificate")
    controls.add("laurent_generators_exact")

    lattice = certificate["lattice_certificate"]
    basis_ids = lattice["basis"]
    pivot_names = lattice["pivot_variables"]
    basis = [relation_by_id[name] for name in basis_ids]
    pivot_indices = [name_to_index[name] for name in pivot_names]
    pivot_matrix = [[row[0][j] for j in pivot_indices] for row in basis]
    require(determinant(pivot_matrix) == lattice["pivot_determinant"] == 1,
            "non-unimodular lattice certificate")
    require(rational_rank([row[0] for row in relation_by_id.values()]) == 8,
            "wrong relation rank")
    for target_id, combination in lattice["dependencies"].items():
        exponent = [0] * 20
        rhs = Fraction(1)
        for basis_id, coefficient in combination.items():
            row, row_rhs = relation_by_id[basis_id]
            exponent = [x + coefficient*y for x, y in zip(exponent, row)]
            rhs *= row_rhs ** coefficient
        require((tuple(exponent), rhs) == relation_by_id[target_id],
                ("dependency failed", target_id))

    parameterization = certificate["parameterization"]
    free_names = parameterization["free_variables"]
    require(set(free_names).isdisjoint(pivot_names), "free/pivot overlap")
    require(set(free_names) | set(pivot_names) == set(names),
            "free/pivot variables do not partition support")
    substitutions = {}
    for free_index, name in enumerate(free_names):
        exponent = [0] * len(free_names)
        exponent[free_index] = 1
        substitutions[name] = (Fraction(1), tuple(exponent))
    for name, record in parameterization["solved"].items():
        exponent = [0] * len(free_names)
        for free_name, power in record["exponents"].items():
            exponent[free_names.index(free_name)] = power
        substitutions[name] = (Fraction(record["coefficient"]), tuple(exponent))
    require(set(substitutions) == set(names), "parameterization domain mismatch")
    for row, rhs in relation_by_id.values():
        coefficient = Fraction(1)
        exponent = [0] * len(free_names)
        for variable, power in zip(names, row):
            if not power:
                continue
            c, e = substitutions[variable]
            coefficient *= c ** power
            exponent = [x + power*y for x, y in zip(exponent, e)]
        require(coefficient == rhs and not any(exponent),
                ("parameterized relation failed", row, rhs))

    # Re-derive the displayed parameterization from the determinant-one basis.
    inverse = invert(pivot_matrix)
    require(all(x.denominator == 1 for row in inverse for x in row),
            "pivot inverse not integral")
    free_indices = [name_to_index[name] for name in free_names]
    free_matrix = [[row[0][j] for j in free_indices] for row in basis]
    derived_exponents = matmul(inverse,
                               [[-x for x in row] for row in free_matrix])
    for i, pivot_name in enumerate(pivot_names):
        derived_coefficient = Fraction(1)
        for eq, (_, rhs) in enumerate(basis):
            derived_coefficient *= rhs ** int(inverse[i][eq])
        require(substitutions[pivot_name] == (
            derived_coefficient, tuple(int(x) for x in derived_exponents[i])),
            ("parameter formula not derived", pivot_name))
    controls.add("unimodular_saturation_and_parameterization")

    gauge = gauge_matrix()
    gauge_record = certificate["gauge_certificate"]
    rank, row_ids, column_ids, minor_det = greedy_rank_minor(gauge)
    require((rank, row_ids, column_ids, minor_det) == (
        gauge_record["rank"], gauge_record["unimodular_row_indices"],
        gauge_record["unimodular_column_indices"],
        gauge_record["minor_determinant"]), "gauge minor mismatch")
    for row, rhs in relation_by_id.values():
        require(all(sum(row[k] * gauge[k][j] for k in range(20)) == 0
                    for j in range(21)), "relation not gauge invariant")
        point_value = Fraction(1)
        for value, power in zip(POINT, row):
            point_value *= Fraction(value) ** power
        require(point_value == rhs, "relation coset misses W40 point")
    # rank(L)=8=20-rank(gauge), and the determinant-one L minor makes L
    # primitive.  Hence L equals ker(gauge^T); the gauge minor also splits
    # the cocharacter image over every field.
    require(rank + rational_rank([row[0] for row in relation_by_id.values()]) == 20,
            "gauge/relation ranks not complementary")
    controls.add("gauge_lattice_equality")

    scalar, response = cap67_response()
    cap_record = certificate["cap_certificate"]
    require(scalar == variable_poly(name_to_index[cap_record["direct_scalar"]]),
            "cap direct scalar mismatch")
    expected_response = {}
    for item in cap_record["nonzero_response_cells"]:
        key = tuple(item["edge"] + item["colors"])
        expected_response[key] = monomial_from_names(item["factors"], name_to_index)
    require(response == expected_response, ("cap response mismatch", response))
    center = cap_record["star_center"]
    require(all(center in key[:2] for key in response), "response is not a star")
    response_edges = {key[:2] for key in response}
    require(all(set(a) & set(b) for a in response_edges for b in response_edges),
            "response contains disjoint edges")
    controls.add("cap67_raw_response")
    require(clean_cap_errors(scalar, response) == {}, "clean cap error nonzero")
    controls.add("cap67_all_729_clean_errors")

    require(controls == declared_controls, (controls, declared_controls))
    digest = sha256(CERTIFICATE_PATH.read_bytes()).hexdigest()
    print("PASS W40 fixed-support global X4 classification")
    print("rows=4881 zero=4869 binomial=12 normalized_relations=10 rank=8")
    print("split_parameter_torus_dimension=12 gauge_orbit_dimension=12")
    print("cap67_K=I response_star_center=5 clean_errors=0 activity=x67_00!=0")
    print("mutation_failures=" + ",".join(mutation_failures))
    print("certificate_sha256=" + digest)
    print("controls=" + str(len(controls)) + "/" + str(len(declared_controls)))


if __name__ == "__main__":
    main()
