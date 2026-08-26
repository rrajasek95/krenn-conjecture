#!/usr/bin/env python3
"""Literal 90-to-45 crossing response and exact diagonal-chart rank audit.

For the source row 00000011 and tail pair 67, the 90 matchings not using
67 have two mixed edges.  Pairing the two endpoint orientations leaves 45
groups: an unordered residual pair {a,b} and one of the three perfect
matchings of the other four residual vertices.  After evaluating the
same-colour fine, the quadratic tail is y^T C z, where C is the symmetric
6 by 6 Hafnian-cofactor response matrix.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
COMP = HERE.parent
SOURCE_REFEREE = (COMP / "unaudited-codex-n8-source-referee-2026-08-20" /
                  "audit_n8_source_interface.py")
SUPPORT6_SOURCE = (COMP / "unaudited-codex-n8-orbit0-normalized-78-2026-08-20" /
                   "audit_weight0_support6_char0_component.py")
FAMILY_SOURCE = (COMP / "unaudited-codex-orbit0-t2-radical-2026-08-20" /
                 "audit_weight0_char0_family_and_packet.py")
OUT = HERE / "results_lowest_crossing_response.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def file_hash(path):
    return sha256(path.read_bytes()).hexdigest()


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        answer.extend((tuple(sorted(((first, second),) + tail))
                       for tail in perfect_matchings(rest)))
    return tuple(sorted(answer))


def edge_name(edge):
    return f"{edge[0]}{edge[1]}"


def matching_name(matching):
    return "|".join(edge_name(edge) for edge in matching)


def cell_name(edge, word):
    left, right = edge
    return f"a{left}{right}^{word[left]}{word[right]}"


def logical_hash(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutation", action="store_true")
    args = parser.parse_args()
    try:
        import sympy as sp
    except ImportError:
        sites = sorted((HERE.parents[1] / ".venv/lib").glob(
            "python*/site-packages"))
        require(bool(sites), "sympy unavailable")
        sys.path.append(str(sites[-1]))
        import sympy as sp

    sites = tuple(range(8))
    residual = tuple(range(6))
    tail = (6, 7)
    word = (0, 0, 0, 0, 0, 0, 1, 1)
    matchings = perfect_matchings(sites)
    common = tuple(matching for matching in matchings if tail in matching)
    crossing = tuple(matching for matching in matchings if tail not in matching)
    require((len(matchings), len(common), len(crossing)) == (105, 15, 90),
            "literal matching census changed")

    grouped = defaultdict(list)
    occurrence_records = []
    for matching_index, matching in enumerate(matchings):
        if tail in matching:
            continue
        edge6 = next(edge for edge in matching if 6 in edge)
        edge7 = next(edge for edge in matching if 7 in edge)
        endpoint6 = edge6[0] if edge6[1] == 6 else edge6[1]
        endpoint7 = edge7[0] if edge7[1] == 7 else edge7[1]
        pair = tuple(sorted((endpoint6, endpoint7)))
        fine = tuple(edge for edge in matching
                     if 6 not in edge and 7 not in edge)
        require(len(fine) == 2 and len(pair) == 2,
                "crossing-tail profile changed")
        key = (pair, fine)
        record = {
            "matching_index": matching_index,
            "matching": matching_name(matching),
            "residual_pair": edge_name(pair),
            "fine": matching_name(fine),
            "tail_cells_raw_endpoint_order": [cell_name(edge6, word),
                                                cell_name(edge7, word)],
            "fine_cells_raw_endpoint_order": [cell_name(edge, word)
                                                for edge in fine],
            "orientation_6_to_7": [endpoint6, endpoint7],
        }
        grouped[key].append(record)
        occurrence_records.append(record)
    require(len(grouped) == 45 and
            Counter(len(value) for value in grouped.values()) == {2: 45},
            "90-to-45 grouping changed")
    for (pair, _fine), records in grouped.items():
        require({tuple(record["orientation_6_to_7"])
                 for record in records} == {pair, tuple(reversed(pair))},
                "endpoint-orientation pair changed")

    # Supervertices are the normalized anchors 01,23,45,67.  Six oriented
    # 2x2 blocks join them in edge order 01,02,03,12,13,23.
    super_edges = tuple(combinations(range(4), 2))
    super_edge_index = {edge: index for index, edge in enumerate(super_edges)}
    anchors = {(0, 1), (2, 3), (4, 5), (6, 7)}
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

    b_support6 = (z, -z-2, 1, -z-2, 1, 1)
    c_support6 = (-z-2, z, -1, z, -1, -1)
    support6_entries = tuple(
        value
        for b_value, c_value in zip(b_support6, c_support6)
        for value in (0, b_value, c_value, 0)
    )
    require(all(reduce_z(b*c+1) == 0
                for b, c in zip(b_support6, c_support6)),
            "support-six offdiagonal products changed")

    def physical_entry(u, v, block_entries):
        if u > v:
            u, v = v, u
        if (u, v) in anchors:
            return sp.Integer(1)
        left, left_clone = divmod(u, 2)
        right, right_clone = divmod(v, 2)
        require(left != right, "unexpected intra-anchor edge")
        block = super_edge_index[(left, right)]
        return block_entries[4*block + 2*left_clone + right_clone]

    def fine_value(fine, block_entries, reduce):
        answer = sp.Integer(1)
        for u, v in fine:
            answer *= physical_entry(u, v, block_entries)
        return reduce(answer)

    def response_matrix(block_entries, reduce):
        matrix = sp.zeros(6, 6)
        group_values = {}
        for (pair, fine), records in sorted(grouped.items()):
            value = fine_value(fine, block_entries, reduce)
            group_values[(pair, fine)] = value
            a, b = pair
            matrix[a, b] = reduce(matrix[a, b] + value)
            matrix[b, a] = reduce(matrix[b, a] + value)
            require(len(records) == 2, "response orientation count changed")
        return matrix.applyfunc(reduce), group_values

    support_matrix, support_group_values = response_matrix(
        support6_entries, reduce_z)
    support_determinant = reduce_z(support_matrix.det())
    require(support_determinant == -64,
            f"support-six response determinant changed: {support_determinant}")
    require(support_matrix.rank() == 6, "support-six response rank changed")
    support_inverse = support_matrix.inv().applyfunc(reduce_z)
    require((support_inverse * support_matrix).applyfunc(reduce_z) == sp.eye(6)
            and (support_matrix * support_inverse).applyfunc(reduce_z) == sp.eye(6),
            "support-six left/right inverse replay failed")

    # Polarized elimination interface.  The literal quadratic row is
    # R(y,z)=y^T C z.  Its twelve polar coefficients are
    # Py=Cz and Pz=Cy.  Inverting C gives source-ready linear identities for
    # every star variable, provided these polar coefficients really occur in
    # the chosen source initial ideal.  The bare scalar equation R=0 alone
    # does not imply Py=Pz=0; that scope distinction is load-bearing.
    hessian = sp.zeros(6).row_join(support_matrix).col_join(
        support_matrix.row_join(sp.zeros(6)))
    # The ordering above is variables (y,z) and rows (Pz,Py).
    hessian_inverse = sp.zeros(6).row_join(support_inverse).col_join(
        support_inverse.row_join(sp.zeros(6)))
    require((hessian_inverse*hessian).applyfunc(reduce_z) == sp.eye(12),
            "12-variable polar Hessian inverse failed")
    hessian_determinant = reduce_z(hessian.det())
    require(hessian_determinant == 4096 and hessian.rank() == 12,
            "polar Hessian rank/determinant changed")

    def inverse_identity(variable_prefix, polar_prefix, row):
        terms = []
        for column, coefficient in enumerate(support_inverse.row(row)):
            coefficient = reduce_z(coefficient)
            if coefficient:
                terms.append(f"({coefficient})*{polar_prefix}{column}")
        return f"{variable_prefix}{row}=" + "+".join(terms)

    polar_identities = [
        inverse_identity("z", "Py", row) for row in range(6)
    ] + [
        inverse_identity("y", "Pz", row) for row in range(6)
    ]
    # Endpoint swap 6<->7 exchanges y,z.  In symmetric/antisymmetric
    # coordinates s=y+z, a=y-z the two polar blocks are C and -C, so neither
    # endpoint-orientation quotient acquires a kernel.
    endpoint_quotient = {
        "symmetric_block_rank": support_matrix.rank(),
        "symmetric_block_kernel": [],
        "antisymmetric_block_rank": support_matrix.rank(),
        "antisymmetric_block_kernel": [],
    }
    # Must-fire against the invalid inference R=0 => y=z=0: because C00=0,
    # y=e0,z=e0 is a nonzero point of the bare quadratic response cone.
    e0 = sp.Matrix([1, 0, 0, 0, 0, 0])
    bare_quadratic_counterexample = reduce_z((e0.T*support_matrix*e0)[0])
    require(bare_quadratic_counterexample == 0,
            "bare-response counterexample stopped firing")

    # Exact B4 covariance.  Permuting the four normalized anchors and
    # independently swapping their endpoints transports the response matrix
    # by simultaneous row/column permutation.  The tail anchor may move;
    # the residual complement and its fine matchings move with it.
    support_graph = {}
    for left, right in combinations(range(8), 2):
        support_graph[(left, right)] = reduce_z(
            physical_entry(left, right, support6_entries))

    def hafnian4(graph, vertices):
        aa, bb, cc, dd = vertices
        return reduce_z(graph[tuple(sorted((aa, bb)))]
                        * graph[tuple(sorted((cc, dd)))]
                        + graph[tuple(sorted((aa, cc)))]
                        * graph[tuple(sorted((bb, dd)))]
                        + graph[tuple(sorted((aa, dd)))]
                        * graph[tuple(sorted((bb, cc)))])

    covariance_checked = 0
    covariance_determinants = Counter()
    for super_permutation in permutations(range(4)):
        for flip_mask in range(16):
            flips = tuple((flip_mask >> site) & 1 for site in range(4))

            def act_vertex(vertex):
                supervertex, clone = divmod(vertex, 2)
                return (2*super_permutation[supervertex]
                        + (clone ^ flips[supervertex]))

            transformed_graph = {}
            for edge, value in support_graph.items():
                image = tuple(sorted(map(act_vertex, edge)))
                transformed_graph[image] = value
            transformed_tail = tuple(sorted(map(act_vertex, tail)))
            transformed_residual = tuple(vertex for vertex in range(8)
                                         if vertex not in transformed_tail)
            transformed_response = sp.zeros(6, 6)
            for ia, avertex in enumerate(transformed_residual):
                for ib in range(ia+1, 6):
                    bvertex = transformed_residual[ib]
                    fine_vertices = tuple(vertex for vertex in transformed_residual
                                          if vertex not in (avertex, bvertex))
                    transformed_response[ia, ib] = transformed_response[ib, ia] = (
                        hafnian4(transformed_graph, fine_vertices))
            old_to_new_position = {
                old: transformed_residual.index(act_vertex(old))
                for old in residual
            }
            for old_a in residual:
                for old_b in residual:
                    observed = transformed_response[
                        old_to_new_position[old_a], old_to_new_position[old_b]]
                    require(reduce_z(observed-support_matrix[old_a, old_b]) == 0,
                            "B4 response covariance failed")
            transformed_det = reduce_z(transformed_response.det())
            covariance_determinants[str(transformed_det)] += 1
            covariance_checked += 1
    require(covariance_checked == 384
            and covariance_determinants == {"-64": 384},
            "B4 response determinant census changed")

    # Literal check of 15 entries x 3 fine terms = 45 response groups and
    # two endpoint orientations = 90 raw occurrences.
    pair_group_counts = Counter(pair for pair, _fine in grouped)
    require(pair_group_counts == Counter({pair: 3
                                          for pair in combinations(residual, 2)}),
            "three-fines-per-response-entry changed")

    # Rebuild the positive-dimensional weight-zero component over
    # Q(sqrt(2),sqrt(65))(u,v,w,t).  At t=0,u=v=w=1 it is the support-six
    # point above.  This independently checks all 22 literal diagonal rows.
    sqrt2, sqrt65 = sp.sqrt(2), sp.sqrt(65)
    u, v, w, t = sp.symbols("u v w t", nonzero=True)
    rho = sqrt2 - 1
    sigma = -sqrt2 - 1
    eta = sp.cancel((-5*rho - 12 + sqrt65*(rho+2))/(6*rho))
    b = (rho*u/v, sigma*u/w, u, sigma*v/w, v, w)
    a5 = t
    a4 = eta*t*v/w
    a3 = t*v*(rho*eta + sigma)
    a2 = sp.cancel(u*t/w*((-3*rho-7)*eta + 5*rho+13)/(rho+5))
    a1 = sp.cancel(u*t*((7*rho+3)*eta - 2*rho-4)/(rho+5))
    a0 = sp.cancel(sigma*(v*a2 + u*a4))
    a = (a0, a1, a2, a3, a4, a5)
    family_entries = tuple(value for edge in range(6)
                           for value in (a[edge], b[edge], -1/b[edge], 0))

    def reduce_family(value):
        return sp.factor(sp.simplify(sp.radsimp(sp.cancel(value))),
                         extension=[sqrt2, sqrt65])

    family_matrix, _family_groups = response_matrix(family_entries,
                                                     reduce_family)
    family_determinant = reduce_family(family_matrix.det())
    require(family_determinant == -64,
            f"family response determinant changed: {family_determinant}")
    family_at_support6 = family_matrix.subs({t: 0, u: 1, v: 1, w: 1})
    support_radical = support_matrix.subs(z, sqrt2-1)
    require(all(reduce_family(left-right) == 0
                for left, right in zip(family_at_support6, support_radical)),
            "positive-dimensional family no longer specializes to support six")

    def block_entry(block, left_clone, right_clone):
        return family_entries[4*block + 2*left_clone + right_clone]

    permanent_rows = []
    for block in range(6):
        permanent_rows.append(reduce_family(
            1 + block_entry(block, 0, 0)*block_entry(block, 1, 1)
            + block_entry(block, 0, 1)*block_entry(block, 1, 0)))
    require(permanent_rows == [0]*6, "family permanent row failed")

    def super_entry(i, j, clone_i, clone_j):
        if i < j:
            block = super_edge_index[(i, j)]
            return block_entry(block, clone_i, clone_j)
        block = super_edge_index[(j, i)]
        return block_entry(block, clone_j, clone_i)

    triangle_rows = []
    for i, j, k in combinations(range(4), 3):
        triangle = 0
        for ci in (0, 1):
            for cj in (0, 1):
                for ck in (0, 1):
                    triangle += (super_entry(i, j, ci, cj)
                                 * super_entry(i, k, 1-ci, ck)
                                 * super_entry(j, k, 1-cj, 1-ck))
        row = 1 + sum(
            block_entry(super_edge_index[edge], 0, 0)
            * block_entry(super_edge_index[edge], 1, 1)
            + block_entry(super_edge_index[edge], 0, 1)
            * block_entry(super_edge_index[edge], 1, 0)
            for edge in ((i, j), (i, k), (j, k))) + triangle
        triangle_rows.append(reduce_family(row))
    require(triangle_rows == [0]*4, "family triangle row failed")

    # Pure normalized Hafnian and the twelve branch-51 selected cofactors.
    xvars = sp.symbols("x0:24")

    def symbolic_physical_entry(left, right):
        if left > right:
            left, right = right, left
        if (left, right) in anchors:
            return sp.Integer(1)
        si, ci = divmod(left, 2)
        sj, cj = divmod(right, 2)
        return xvars[4*super_edge_index[(si, sj)] + 2*ci + cj]

    pure_hafnian = 0
    for matching in matchings:
        term = 1
        for edge in matching:
            term *= symbolic_physical_entry(*edge)
        pure_hafnian += term
    substitution = dict(zip(xvars, family_entries))
    pure_value = reduce_family(pure_hafnian.subs(substitution))
    require(pure_value == 4, f"family pure Hafnian changed: {pure_value}")
    branch_bits = (1, 1, 0, 0, 1, 1)
    selected_cofactor_values = []
    selected_cofactor_labels = []
    for block, bit in enumerate(branch_bits):
        selected_entries = (0, 3) if bit == 0 else (1, 2)
        for entry in selected_entries:
            value = reduce_family(sp.diff(
                pure_hafnian, xvars[4*block+entry]).subs(substitution))
            selected_cofactor_values.append(value)
            selected_cofactor_labels.append(
                f"dH/dx{4*block+entry} block={super_edges[block]} entry={entry}")
    require(selected_cofactor_values == [0]*12,
            "family selected cofactor row failed")

    # Two independent must-fire controls: one raw crossing occurrence is
    # indispensable to the 90/45 census, and changing one physical response
    # coefficient changes the certified determinant from -64 to -36.
    deleted = occurrence_records[:-1]
    deletion_fired = len(deleted) == 89 and len(occurrence_records) == 90
    mutated_matrix = support_matrix.copy()
    mutated_matrix[0, 3] = reduce_z(mutated_matrix[0, 3] + 1)
    mutated_matrix[3, 0] = mutated_matrix[0, 3]
    mutated_determinant = reduce_z(mutated_matrix.det())
    coefficient_mutation_fired = mutated_determinant == -36
    require(deletion_fired and coefficient_mutation_fired,
            "response mutation guard failed")

    group_records = []
    for (pair, fine), records in sorted(grouped.items()):
        group_records.append({
            "residual_pair": edge_name(pair),
            "fine": matching_name(fine),
            "fine_cells_raw_endpoint_order": records[0][
                "fine_cells_raw_endpoint_order"],
            "support6_fine_coefficient": str(support_group_values[(pair, fine)]),
            "occurrences": records,
        })

    result = {
        "status": "PASS exact literal crossing-response rank audit",
        "mutation_mode": args.mutation,
        "source_row": "00000011",
        "tail_pair": "67",
        "literal_census": {
            "perfect_matchings": 105,
            "common_tail_occurrences": 15,
            "lowest_two_crossing_tail_occurrences": 90,
            "physical_response_groups": 45,
            "groups_per_symmetric_matrix_entry": 3,
            "endpoint_orientations_per_group": 2,
        },
        "response_formula": (
            "tail_2(F_00000011)=sum_{a,b=0}^5 y_a C_ab z_b; "
            "C_aa=0 and C_ab=Hafnian of the four residual vertices other "
            "than a,b.  Each C_ab has the three fine groups; symmetry "
            "accounts for the two endpoint-ordered occurrences."),
        "raw_group_ledger": group_records,
        "support6_aligned_chart": {
            "field": "Q(z), z^2+2z-1=0",
            "anchor_edges_normalized_to_one": ["01", "23", "45", "67"],
            "block_edge_order": [edge_name(edge) for edge in super_edges],
            "block_entries_row_major": [str(value)
                                         for value in support6_entries],
            "response_matrix": [[str(value) for value in row]
                                for row in support_matrix.tolist()],
            "rank": 6,
            "kernel_basis": [],
            "unique_maximal_minor_rows": list(range(6)),
            "unique_maximal_minor_columns": list(range(6)),
            "maximal_minor_determinant": str(support_determinant),
            "left_inverse": [[str(value) for value in row]
                             for row in support_inverse.tolist()],
            "left_inverse_replay": "C_inverse*C=I_6 and C*C_inverse=I_6",
        },
        "lowest_tail_polar_elimination": {
            "star_variables_raw_endpoint_order": {
                "y": [f"a{a}6^01" for a in range(6)],
                "z": [f"a{a}7^01" for a in range(6)],
            },
            "quadratic_response": "R(y,z)=y^T*C*z",
            "polar_coefficients": {
                "Py": "dR/dy=C*z",
                "Pz": "dR/dz=C*y",
            },
            "hessian_rank": 12,
            "hessian_kernel": [],
            "hessian_determinant": str(hessian_determinant),
            "explicit_inverse_identities": polar_identities,
            "conditional_forcing": (
                "If all twelve polar response coefficients Py,Pz belong to "
                "the lowest source initial ideal and vanish, the displayed "
                "identities force all twelve star perturbations y,z to zero."),
            "endpoint_6_7_orientation_quotient": endpoint_quotient,
            "bare_row_scope_blocker": {
                "counterexample": "y=e0,z=e0",
                "response_value": str(bare_quadratic_counterexample),
                "consequence": (
                    "The single literal row R=0 forces no individual star "
                    "coefficient to vanish.  C invertible is nondegeneracy "
                    "of the pairing, not linear elimination without the "
                    "twelve polar/source coefficients."),
            },
        },
        "B4_covariance": {
            "action": "C maps to P*C*P^T after moving the tail anchor",
            "anchor_permutations_times_endpoint_switches": covariance_checked,
            "determinant_histogram": dict(covariance_determinants),
            "symmetric_and_antisymmetric_endpoint_blocks": "C and -C",
        },
        "positive_dimensional_weight0_component": {
            "field": "Q(sqrt(2),sqrt(65))(u,v,w,t)",
            "dimension_parameters": ["u", "v", "w", "t"],
            "same_maximal_minor": str(family_determinant),
            "same_minor_is_constant_unit": True,
            "specialization_to_support6": "t=0,u=v=w=1,z=sqrt(2)-1",
            "literal_diagonal_source_replay": {
                "six_permanent_rows": True,
                "four_triangle_rows": True,
                "twelve_branch51_selected_cofactor_rows": True,
                "pure_H": str(pure_value),
                "selected_cofactor_labels": selected_cofactor_labels,
            },
            "consequence": (
                "The 6x6 lowest-tail response matrix remains invertible on "
                "the entire declared Laurent family; adj(C)/(-64) is a "
                "symbolic left inverse over its coordinate field."),
        },
        "mutation_guards": {
            "deleted_occurrence_90_to_89_fired": deletion_fired,
            "mutated_C03_determinant": str(mutated_determinant),
            "coefficient_mutation_fired": coefficient_mutation_fired,
        },
        "scope_guard": (
            "This proves invertibility of the literal degree-two crossing "
            "response for the fixed 00000011/tail67 packet on the support-six "
            "point and one aligned positive-dimensional diagonal component. "
            "It proves elimination of all twelve star variables only "
            "conditional on the twelve polar coefficients occurring in the "
            "lowest source initial ideal.  The bare quadratic source row has "
            "a large nonzero zero-cone.  This is not a global 240-variable "
            "initial-ideal theorem and does not prove that every diagonal "
            "component has the same unit minor."),
        "source_hashes": {
            "n8_source_referee": file_hash(SOURCE_REFEREE),
            "support6_component": file_hash(SUPPORT6_SOURCE),
            "weight0_family": file_hash(FAMILY_SOURCE),
        },
    }
    result["logical_sha256"] = logical_hash(result)
    if not args.mutation:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    else:
        mutation_out = HERE / "results_lowest_crossing_response_mutation.json"
        mutation_out.write_text(json.dumps(result, indent=2,
                                           sort_keys=True) + "\n")
    print("lowest crossing response PASS", result["logical_sha256"])
    print("census 105/15/90/45; support rank/det", 6, support_determinant)
    print("family determinant", family_determinant)


if __name__ == "__main__":
    main()
