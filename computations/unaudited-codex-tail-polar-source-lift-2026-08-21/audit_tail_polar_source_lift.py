#!/usr/bin/env python3
"""Exact lowest-tail source-row audit for one ordered 01 endpoint star.

The retained columns are

    y_a = a_{a6}^{01}, z_a = a_{a7}^{01}, 0 <= a < 6.

All other off-diagonal cells are killed only for the purpose of taking this
literal associated-graded column slice.  Three independent diagonal graphs
G0,G1,G2 are retained symbolically.  No compatible three-colour point is
assumed.
"""

from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
UPSTREAM = (HERE.parent /
            "unaudited-codex-diagonal-full-response-lift-2026-08-21" /
            "audit_lowest_crossing_response.py")
OUT = HERE / "results_tail_polar_source_lift.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def logical_hash(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def file_hash(path):
    return sha256(path.read_bytes()).hexdigest()


def word_name(word):
    return "".join(map(str, word))


def profile(word):
    return tuple(sorted(Counter(word).values(), reverse=True))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        answer.extend((((first, second),) + tail
                       for tail in perfect_matchings(rest)))
    return tuple(answer)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    try:
        import sympy as sp
    except ImportError:
        sites = sorted((ROOT / ".venv/lib").glob("python*/site-packages"))
        require(bool(sites), "sympy unavailable")
        sys.path.append(str(sites[-1]))
        import sympy as sp

    vertices = tuple(range(8))
    residual = tuple(range(6))
    tails = (6, 7)
    columns = tuple((a, tail) for tail in tails for a in residual)
    column_names = tuple((f"y{a}" if tail == 6 else f"z{a}")
                         for a, tail in columns)
    edges = tuple(combinations(vertices, 2))
    diagonal = {
        (colour, edge): sp.symbols(f"g{colour}_{edge[0]}{edge[1]}")
        for colour in range(3) for edge in edges
    }

    @lru_cache(None)
    def hafnian(colour, subset):
        subset = tuple(subset)
        if not subset:
            return sp.Integer(1)
        first = subset[0]
        answer = 0
        for index in range(1, len(subset)):
            second = subset[index]
            rest = subset[1:index] + subset[index + 1:]
            answer += diagonal[colour, tuple(sorted((first, second)))] * \
                hafnian(colour, rest)
        return sp.expand(answer)

    def coefficient(word, a, tail):
        # The retained ordered cell has residual colour 0 and tail colour 1.
        if word[a] != 0 or word[tail] != 1:
            return sp.Integer(0)
        remaining = tuple(v for v in vertices if v not in (a, tail))
        counts = Counter(word)
        counts[0] -= 1
        counts[1] -= 1
        if any(counts[colour] % 2 for colour in range(3)):
            return sp.Integer(0)
        answer = sp.Integer(1)
        for colour in range(3):
            subset = tuple(v for v in remaining if word[v] == colour)
            answer *= hafnian(colour, subset)
        return sp.expand(answer)

    wanted_profiles = ((7, 1), (6, 1, 1), (3, 3, 2))
    rows = []
    row_by_word = {}
    for word in product(range(3), repeat=8):
        row_profile = profile(word)
        if row_profile not in wanted_profiles:
            continue
        values = tuple(coefficient(word, a, tail) for a, tail in columns)
        if not any(values):
            continue
        record = (word, row_profile, values)
        rows.append(record)
        row_by_word[word] = record
    row_counts = Counter(record[1] for record in rows)
    require(row_counts == {(7, 1): 8, (6, 1, 1): 12,
                           (3, 3, 2): 360}, row_counts)
    require(len(rows) == 380, "lowest-tail row census changed")

    # Independent raw 105-matching replay of every retained coefficient.
    # This guards both the word labels and the endpoint orientation in the
    # compact product-of-hafnians formula above.
    matchings = perfect_matchings(vertices)
    require(len(matchings) == 105, "K8 matching census changed")
    raw_linear_occurrences = 0
    column_index = {edge: index for index, edge in enumerate(columns)}
    for word, _row_profile, values in rows:
        raw_values = [sp.Integer(0)] * 12
        for matching in matchings:
            cross_edges = tuple(edge for edge in matching
                                if word[edge[0]] != word[edge[1]])
            if len(cross_edges) != 1:
                continue
            cross_edge = cross_edges[0]
            index = column_index.get(cross_edge)
            if index is None:
                continue
            a, tail = cross_edge
            if word[a] != 0 or word[tail] != 1:
                continue
            term = sp.Integer(1)
            for edge in matching:
                if edge == cross_edge:
                    continue
                require(word[edge[0]] == word[edge[1]],
                        "raw lowest-tail fine ceased to be diagonal")
                term *= diagonal[word[edge[0]], edge]
            raw_values[index] += term
            raw_linear_occurrences += 1
        require(all(sp.expand(left-right) == 0
                    for left, right in zip(raw_values, values)),
                ("raw 105-matching source replay failed", word_name(word)))

    # The twelve 6+1+1 rows are diagonal in the twelve retained columns.
    # Their multiplier is the six-site cofactor of the independent third
    # diagonal graph G2.
    rows_611 = []
    cofactors_611 = []
    for column_index, (a, tail) in enumerate(columns):
        word = [2] * 8
        word[a] = 0
        word[tail] = 1
        word = tuple(word)
        values = row_by_word[word][2]
        cofactor = hafnian(2, tuple(v for v in vertices
                                    if v not in (a, tail)))
        expected = [sp.Integer(0)] * 12
        expected[column_index] = cofactor
        require(values == tuple(expected),
                ("6+1+1 diagonal row changed", word_name(word)))
        rows_611.append({
            "source_label": "F_" + word_name(word),
            "column": column_names[column_index],
            "multiplier": str(cofactor),
            "identity": (f"in_1(F_{word_name(word)})="
                         f"({cofactor})*{column_names[column_index]}"),
        })
        cofactors_611.append(cofactor)
    determinant_611 = sp.prod(cofactors_611)
    require(determinant_611 != 0,
            "6+1+1 determinant ceased to be a nonzero polynomial")

    # One explicit 332 redundancy minor.  For each endpoint block use two
    # disjoint residual triangles; the coefficient matrix on a triangle has
    # determinant 2*d0*d1*d2, hence the six-row block has determinant
    # 4*prod(d_a).  Fine factors are retained literally.
    selected_partitions = (
        ((0, 1), (2, 3), (4, 5)),
        ((0, 2), (1, 3), (4, 5)),
        ((1, 2), (0, 3), (4, 5)),
        ((3, 4), (0, 1), (2, 5)),
        ((3, 5), (0, 1), (2, 4)),
        ((4, 5), (0, 1), (2, 3)),
    )

    selected_332 = []
    selected_labels = []
    fine_product = sp.Integer(1)
    for tail, other_tail in ((6, 7), (7, 6)):
        for zero_pair, one_pair, two_pair in selected_partitions:
            word = [None] * 8
            word[tail] = 1
            word[other_tail] = 0
            for v in zero_pair:
                word[v] = 0
            for v in one_pair:
                word[v] = 1
            for v in two_pair:
                word[v] = 2
            word = tuple(word)
            require(profile(word) == (3, 3, 2), "selected 332 label changed")
            selected_332.append(row_by_word[word][2])
            selected_labels.append("F_" + word_name(word))
            fine_product *= (diagonal[1, tuple(sorted(one_pair))]
                             * diagonal[2, tuple(sorted(two_pair))])
    selected_332_matrix = sp.Matrix(selected_332)
    determinant_332 = sp.factor(selected_332_matrix.det())
    # fine_product contains both identical endpoint blocks, so the expected
    # expression uses it directly rather than squaring once more.
    endpoint_product = sp.prod(
        diagonal[0, tuple(sorted((a, tail)))]
        for a in residual for tail in tails)
    expected_332 = sp.factor(16 * endpoint_product * fine_product)
    require(sp.expand(determinant_332 - expected_332) == 0,
            "selected 332 determinant factorization changed")

    # Generic ranks are proved by the displayed nonzero polynomial minors;
    # modular evaluation is only an independent must-fire control.
    def modular_rank(matrix, modulus, substitution):
        values = [[int(value.subs(substitution)) % modulus
                   for value in row] for row in matrix.tolist()]
        rank = 0
        for column in range(len(values[0])):
            pivot = next((row for row in range(rank, len(values))
                          if values[row][column]), None)
            if pivot is None:
                continue
            values[rank], values[pivot] = values[pivot], values[rank]
            inverse = pow(values[rank][column], -1, modulus)
            values[rank] = [(entry * inverse) % modulus
                            for entry in values[rank]]
            for row in range(len(values)):
                if row == rank or not values[row][column]:
                    continue
                scale = values[row][column]
                values[row] = [
                    (left - scale * right) % modulus
                    for left, right in zip(values[row], values[rank])
                ]
            rank += 1
        return rank

    rank_controls = {}
    all_symbols = tuple(diagonal.values())
    matrix_611 = sp.Matrix([
        row_by_word[tuple(0 if v == a else 1 if v == tail else 2
                          for v in vertices)][2]
        for a, tail in columns
    ])
    matrix_332 = sp.Matrix([record[2] for record in rows
                            if record[1] == (3, 3, 2)])
    for modulus in (1009, 1013):
        substitution = {
            symbol: (1 + 37 * (index + 1) + 11 * (index + 3) ** 2) % modulus
            for index, symbol in enumerate(all_symbols)
        }
        ranks = {
            "6+1+1": modular_rank(matrix_611, modulus, substitution),
            "3+3+2": modular_rank(matrix_332, modulus, substitution),
            "selected_3+3+2_minor": modular_rank(
                selected_332_matrix, modulus, substitution),
        }
        require(ranks == {"6+1+1": 12, "3+3+2": 12,
                          "selected_3+3+2_minor": 12},
                ("generic rank control changed", modulus, ranks))
        rank_controls[str(modulus)] = ranks

    # Rebuild the support-six C and the two genuinely available 7+1 rows.
    z = sp.symbols("z")
    z_modulus = sp.Poly(z**2 + 2*z - 1, z, domain=sp.QQ)

    def reduce_z_polynomial(value):
        return sp.rem(sp.Poly(sp.expand(value), z, domain=sp.QQ),
                      z_modulus).as_expr()

    def reduce_z(value):
        numerator, denominator = sp.cancel(value).as_numer_denom()
        numerator = reduce_z_polynomial(numerator)
        denominator = reduce_z_polynomial(denominator)
        inverse = sp.invert(sp.Poly(denominator, z, domain=sp.QQ),
                            z_modulus).as_expr()
        return reduce_z_polynomial(numerator * inverse)

    super_edges = tuple(combinations(range(4), 2))
    super_edge_index = {edge: index for index, edge in enumerate(super_edges)}
    anchors = {(0, 1), (2, 3), (4, 5), (6, 7)}
    b = (z, -z-2, 1, -z-2, 1, 1)
    c = (-z-2, z, -1, z, -1, -1)
    support_entries = tuple(value for bv, cv in zip(b, c)
                            for value in (0, bv, cv, 0))

    def support_edge(u, v):
        if u > v:
            u, v = v, u
        if (u, v) in anchors:
            return sp.Integer(1)
        left, left_clone = divmod(u, 2)
        right, right_clone = divmod(v, 2)
        block = super_edge_index[(left, right)]
        return support_entries[4*block + 2*left_clone + right_clone]

    @lru_cache(None)
    def support_hafnian(subset):
        subset = tuple(subset)
        if not subset:
            return sp.Integer(1)
        first = subset[0]
        answer = 0
        for index in range(1, len(subset)):
            second = subset[index]
            rest = subset[1:index] + subset[index + 1:]
            answer += support_edge(first, second) * support_hafnian(rest)
        return reduce_z(answer)

    response = sp.Matrix(6, 6, lambda a, bb:
                         0 if a == bb else support_hafnian(tuple(
                             v for v in residual if v not in (a, bb))))
    response = response.applyfunc(reduce_z)
    response_inverse = response.inv().applyfunc(reduce_z)
    require(reduce_z(response.det()) == -64,
            "support response determinant changed")
    d6 = sp.Matrix([support_edge(a, 6) for a in residual])
    d7 = sp.Matrix([support_edge(a, 7) for a in residual])
    h6 = sp.Matrix([support_hafnian(tuple(v for v in vertices
                                          if v not in (a, 6)))
                    for a in residual])
    h7 = sp.Matrix([support_hafnian(tuple(v for v in vertices
                                          if v not in (a, 7)))
                    for a in residual])
    require((response*d7-h6).applyfunc(reduce_z) == sp.zeros(6, 1)
            and (response*d6-h7).applyfunc(reduce_z) == sp.zeros(6, 1),
            "7+1 response-direction containment changed")
    require(list(map(reduce_z, d6)) == [0, -1, 0, -1, 0, -1]
            and list(map(reduce_z, d7)) == [1, 0, 1, 0, 1, 0]
            and list(map(reduce_z, h6)) == [0, -4, 0, 0, 0, 0]
            and list(map(reduce_z, h7)) == [4, 0, 0, 0, 0, 0],
            "support 7+1 vectors changed")
    h67 = support_hafnian(residual)
    require(h67 == 0, "seventh tail-edge contaminant no longer vanishes")

    # Polar coordinate ordering is (Pz0..Pz5,Py0..Py5), where Pz=C*y and
    # Py=C*z.  The two literal 7+1 rows span exactly d7^T Pz and d6^T Py.
    fixed_71_polar = sp.zeros(2, 12)
    for a in residual:
        fixed_71_polar[0, a] = d7[a]
        fixed_71_polar[1, 6+a] = d6[a]
    require(fixed_71_polar.rank() == 2
            and len(fixed_71_polar.nullspace()) == 10,
            "fixed 7+1 polar rank/kernel changed")

    hessian = sp.zeros(6).row_join(response).col_join(
        response.row_join(sp.zeros(6)))
    require(hessian.rank() == 12 and len(hessian.nullspace()) == 0
            and reduce_z(hessian.det()) == 4096,
            "paired-orientation Hessian changed")

    def inverse_identity(variable_prefix, polar_prefix, row):
        terms = []
        for column, coefficient_value in enumerate(response_inverse.row(row)):
            coefficient_value = reduce_z(coefficient_value)
            if coefficient_value:
                terms.append(f"({coefficient_value})*{polar_prefix}{column}")
        return f"{variable_prefix}{row}=" + "+".join(terms)

    inverse_identities = [
        inverse_identity("z", "Py", row) for row in residual
    ] + [inverse_identity("y", "Pz", row) for row in residual]

    # Full B4 covariance of C, allowing the tail anchor to move.
    support_graph = {edge: reduce_z(support_edge(*edge)) for edge in edges}
    covariance_determinants = Counter()
    covariance_checked = 0
    for super_permutation in permutations(range(4)):
        for flip_mask in range(16):
            flips = tuple((flip_mask >> site) & 1 for site in range(4))

            def act_vertex(vertex):
                supervertex, clone = divmod(vertex, 2)
                return 2*super_permutation[supervertex] + \
                    (clone ^ flips[supervertex])

            transformed_graph = {}
            for edge, value in support_graph.items():
                transformed_graph[tuple(sorted(map(act_vertex, edge)))] = value
            transformed_tail = tuple(sorted(map(act_vertex, tails)))
            transformed_residual = tuple(v for v in vertices
                                         if v not in transformed_tail)
            transformed = sp.zeros(6, 6)
            for ia, av in enumerate(transformed_residual):
                for ib in range(ia+1, 6):
                    bv = transformed_residual[ib]
                    fine = tuple(v for v in transformed_residual
                                 if v not in (av, bv))
                    aa, bb, cc, dd = fine
                    value = (
                        transformed_graph[tuple(sorted((aa, bb)))]
                        * transformed_graph[tuple(sorted((cc, dd)))]
                        + transformed_graph[tuple(sorted((aa, cc)))]
                        * transformed_graph[tuple(sorted((bb, dd)))]
                        + transformed_graph[tuple(sorted((aa, dd)))]
                        * transformed_graph[tuple(sorted((bb, cc)))]
                    )
                    transformed[ia, ib] = transformed[ib, ia] = reduce_z(value)
            old_to_new_position = {
                old: transformed_residual.index(act_vertex(old))
                for old in residual
            }
            for old_a in residual:
                for old_b in residual:
                    observed = transformed[
                        old_to_new_position[old_a],
                        old_to_new_position[old_b]
                    ]
                    require(reduce_z(observed-response[old_a, old_b]) == 0,
                            "B4 response entry covariance changed")
            determinant = reduce_z(transformed.det())
            covariance_determinants[str(determinant)] += 1
            covariance_checked += 1
    require(covariance_checked == 384
            and covariance_determinants == {"-64": 384},
            "B4 determinant covariance changed")

    # Must-fire mutations.
    mutated_h6 = h6.copy()
    mutated_h6[0] = reduce_z(mutated_h6[0] + 1)
    direction_mutation_fired = (
        (response*d7-mutated_h6).applyfunc(reduce_z) != sp.zeros(6, 1))
    deleted_611 = matrix_611.copy()
    deleted_611.row_del(0)
    deletion_mutation_fired = deleted_611.rank() <= 11
    mutated_332 = selected_332_matrix.copy()
    mutated_332[0, 0] = sp.expand(mutated_332[0, 0] + 1)
    coefficient_mutation_fired = (
        sp.expand(mutated_332.det()-determinant_332) != 0)
    mutated_response = response.copy()
    mutated_response[0, 3] = reduce_z(mutated_response[0, 3]+1)
    mutated_response[3, 0] = mutated_response[0, 3]
    covariance_mutation_determinant = reduce_z(mutated_response.det())
    require(direction_mutation_fired and deletion_mutation_fired
            and coefficient_mutation_fired
            and covariance_mutation_determinant == -36,
            "source/rank/covariance mutation failed")

    # Compact row ledger: every row label and every nonzero retained column
    # is frozen.  This is source provenance, not a claim that the quotient is
    # itself a full-source solution.
    row_ledger = []
    for word, row_profile, values in rows:
        row_ledger.append({
            "source_label": "F_" + word_name(word),
            "profile": "+".join(map(str, row_profile)),
            "nonzero_columns": {
                column_names[index]: str(value)
                for index, value in enumerate(values) if value != 0
            },
        })

    result = {
        "status": "PASS exact source-faithful lowest-tail linear rank audit",
        "retained_star_columns": list(column_names),
        "independent_diagonal_graphs": ["G0", "G1", "G2"],
        "source_row_census": {
            "7+1": 8,
            "6+1+1": 12,
            "3+3+2": 360,
            "total_rows": 380,
            "columns": 12,
            "literal_linear_matching_occurrences": raw_linear_occurrences,
            "raw_105_matching_replay": True,
        },
        "row_ledger": row_ledger,
        "generic_rank_theorem": {
            "combined_rank_over_Q_G0_G1_G2": 12,
            "proof": (
                "the 12 profile-6+1+1 rows form the displayed diagonal "
                "minor, a nonzero polynomial in the independent diagonal "
                "coordinate ring"),
            "modular_controls": rank_controls,
        },
        "source_faithful_6+1+1_elimination": {
            "rows": rows_611,
            "maximal_minor": str(determinant_611),
            "factor_count": 12,
            "rank_drop_locus_for_this_subpacket": (
                "union_{a=0..5,t=6,7} V(Haf(G2 on "
                "{0,...,7}\\{a,t}))"),
            "principal_open_lemma": (
                "On D611=product_{a,t} Haf(G2\\{a,t}) != 0, each "
                "retained star cell equals its labelled 6+1+1 source "
                "initial divided by the displayed cofactor; hence all "
                "twelve cells lie in the localized lowest source ideal."),
        },
        "selected_3+3+2_redundancy_minor": {
            "source_labels_in_row_order": selected_labels,
            "columns_in_order": list(column_names),
            "determinant": str(determinant_332),
            "role": (
                "explicit generic redundancy/control only; its vanishing "
                "does not imply rank drop of the full 360-row 332 matrix"),
        },
        "support6_fixed_7+1_interface": {
            "source_rows": {
                "F_00000010_initial": "-4*y1=d7^T*Pz=Pz0+Pz2+Pz4",
                "F_00000001_initial": "4*z0=d6^T*Py=-Py1-Py3-Py5",
            },
            "seventh_tail_edge_coefficient": str(h67),
            "seventh_tail_edge_contamination": False,
            "polar_row_rank": 2,
            "polar_kernel_dimension": 10,
            "missing_polar_directions": 10,
            "consequence": (
                "The fixed two 7+1 rows are source-faithful but do not "
                "supply the twelve polar rows assumed by bare C-inversion."),
        },
        "response_inverse": {
            "source_row": "F_00000011",
            "tail_pair": "67",
            "determinant": "-64",
            "inverse": [[str(reduce_z(value)) for value in row]
                        for row in response_inverse.tolist()],
            "conditional_polar_identities": inverse_identities,
            "paired_orientation_hessian_rank": 12,
            "paired_orientation_hessian_determinant": "4096",
            "paired_orientation_kernel": [],
            "scope": (
                "These twelve identities become source elimination only "
                "where source rows span all twelve polar coefficients; "
                "the 6+1+1 principal open is one exact such locus."),
        },
        "B4_covariance": {
            "group": "C2^4 semidirect S4",
            "elements_checked": covariance_checked,
            "determinant_histogram": dict(covariance_determinants),
            "response_transport": "C maps to P*C*P^T",
            "cofactor_divisors": (
                "the twelve star cofactors are one orbit under the "
                "fixed-tail stabilizer and under full B4 transport"),
        },
        "boundary_map": {
            "covered_open": "D611 != 0",
            "support6_intersection": (
                "D611=0 (ten of the twelve fixed-tail cofactors vanish); "
                "the frozen support6 arbitrary-mate unit separately "
                "excludes a compatible diagonal mate"),
            "generic_single_cofactor_divisor": (
                "not covered by an existing all-chart theorem; B4 reduces "
                "the twelve named divisors to one representative, but the "
                "full 332/7+1 rank on that divisor still depends on the "
                "other two independent diagonal graphs"),
            "no_numeric_triple_screen": (
                "there is no frozen compatible diagonal triple on which "
                "to specialize G0,G1,G2; setting all three to support6 "
                "would be unsound because support6 has no mate"),
        },
        "mutation_guards": {
            "7+1_direction_coefficient_mutation": direction_mutation_fired,
            "delete_one_6+1+1_row": deletion_mutation_fired,
            "3+3+2_minor_coefficient_mutation": coefficient_mutation_fired,
            "mutated_C03_determinant": str(covariance_mutation_determinant),
        },
        "scope_guard": (
            "This is an exact associated-graded row theorem for one ordered "
            "01 endpoint-star quotient. It proves tail elimination on the "
            "principal cofactor-open D611, and generic rank over three "
            "independent diagonal graphs. It does not prove that the "
            "diagonal packet forces D611 nonzero, nor close the union of "
            "cofactor-zero divisors, nor prove the full 240-variable lift."),
        "source_hashes": {
            "upstream_response_checker": file_hash(UPSTREAM),
        },
    }
    result["logical_sha256"] = logical_hash(result)
    if args.write_results:
        HERE.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("tail polar source lift: PASS", result["logical_sha256"])
    print("rows/columns", len(rows), len(columns), "generic rank 12")
    print("profile rows", dict(sorted(("+".join(map(str, key)), value)
                                           for key, value in row_counts.items())))
    print("fixed 7+1 polar rank/kernel", 2, 10)


if __name__ == "__main__":
    main()
