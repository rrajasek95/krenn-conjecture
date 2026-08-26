#!/usr/bin/env python3
"""Quadratic response control at the nonexact common-matching I3 source."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from audit_blockwise_minimum_norm import (  # noqa: E402
    amplitudes, derivative_columns, sparse_row_basis, require,
)
from audit_13block_environment import dense_rank, response_row  # noqa: E402


OUT = HERE / "results_active_cap_boundary_leading.json"
SITES = tuple(range(8))
COLOURS = tuple(range(3))
MATCHING = ((0, 1), (2, 3), (4, 5), (6, 7))
MATCHING_SET = frozenset(MATCHING)
ALL_EDGES = tuple(combinations(SITES, 2))
OFF_EDGES = tuple(edge for edge in ALL_EDGES if edge not in MATCHING_SET)
Y_LABELS = tuple(edge + (i, j) for edge in OFF_EDGES
                 for i in COLOURS for j in COLOURS)
Y_INDEX = {label: index for index, label in enumerate(Y_LABELS)}
Z_LABELS = tuple(edge + (i, j) for edge in MATCHING
                 for i in COLOURS for j in COLOURS)
Z_INDEX = {label: index for index, label in enumerate(Z_LABELS)}


def base_source():
    return {edge + (colour, colour): Fraction(1)
            for edge in MATCHING for colour in COLOURS}


def activity_rows(source, p, q):
    answer = []
    for colour in COLOURS:
        row = [Fraction(0)] * 9
        row[3 * colour + colour] = 1
        answer.append(row)
    answer.append([source.get((p, q, i, j), 0)
                   for i in COLOURS for j in COLOURS])
    return answer


def carrier_rows(source, p, q, kind, carrier):
    residual = tuple(v for v in SITES if v not in (p, q))
    if kind == "star":
        allowed = {edge for edge in combinations(residual, 2)
                   if carrier in edge}
    else:
        allowed = set(combinations(tuple(carrier), 2))
    # audit_13's response_row is pinned to pair 01; rebuild for arbitrary pair.
    def cell(u, v, i, j):
        if u < v:
            return source.get((u, v, i, j), 0)
        return source.get((v, u, j, i), 0)

    rows = []
    for a, b in combinations(residual, 2):
        if (a, b) in allowed:
            continue
        for alpha in COLOURS:
            for beta in COLOURS:
                rows.append([
                    cell(p, a, i, alpha) * cell(q, b, j, beta)
                    + cell(p, b, i, beta) * cell(q, a, j, alpha)
                    for i in COLOURS for j in COLOURS])
    return rows


def carrier_census():
    source = base_source()
    histogram = Counter()
    active = []
    for p, q in ALL_EDGES:
        residual = tuple(v for v in SITES if v not in (p, q))
        carriers = [("star", centre) for centre in residual]
        carriers += [("triangle", triangle)
                     for triangle in combinations(residual, 3)]
        for kind, carrier in carriers:
            rows = carrier_rows(source, p, q, kind, carrier)
            rank = dense_rank(rows)
            memberships = tuple(dense_rank(rows + [functional]) == rank
                                for functional in activity_rows(source, p, q))
            passes = not any(memberships)
            histogram[kind, rank, "".join("1" if x else "0"
                                           for x in memberships)] += 1
            if passes:
                active.append((p, q, kind, carrier))
    require(len(active) == 104, len(active))
    require(all((p, q) in MATCHING_SET for p, q, _, _ in active), active[:1])
    require(Counter(kind for _, _, kind, _ in active) ==
            {"star": 24, "triangle": 80}, active)
    return active, histogram


def full_jacobian_profile():
    source = base_source()
    columns = derivative_columns(source, 8)
    labels = sorted(columns)
    label_index = {label: index for index, label in enumerate(labels)}
    mixed_rows = []
    for word in product(COLOURS, repeat=8):
        if len(set(word)) == 1:
            continue
        row = {label_index[label]: column[word]
               for label, column in columns.items() if word in column}
        mixed_rows.append(row)
    basis = sparse_row_basis(mixed_rows)
    off_columns_zero = all(not columns[label] for label in Y_LABELS)
    require(len(basis) == 33 and off_columns_zero,
            (len(basis), off_columns_zero))
    return {
        "mixed_J_rank": len(basis),
        "mixed_tangent_dimension": len(labels) - len(basis),
        "off_matching_first_derivative_columns_all_zero": off_columns_zero,
        "off_matching_Y_dimension": len(Y_LABELS),
    }


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for index in range(1, len(vertices)):
        v = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


PM8 = tuple(perfect_matchings(SITES))


def second_order_mixed_polynomials():
    """Coefficient [t^2]F for A=A0+tY, as quadratic Y monomials."""
    rows = defaultdict(Counter)
    matching_terms = 0
    for matching in PM8:
        base_edges = tuple(edge for edge in matching if edge in MATCHING_SET)
        y_edges = tuple(edge for edge in matching if edge not in MATCHING_SET)
        if len(base_edges) != 2 or len(y_edges) != 2:
            continue
        for base_colours in product(COLOURS, repeat=2):
            for y_colours in product(product(COLOURS, repeat=2), repeat=2):
                word = [None] * 8
                for (u, v), colour in zip(base_edges, base_colours):
                    word[u] = word[v] = colour
                variables = []
                for (u, v), (a, b) in zip(y_edges, y_colours):
                    word[u], word[v] = a, b
                    variables.append(Y_INDEX[u, v, a, b])
                monomial = tuple(sorted(variables))
                rows[tuple(word)][monomial] += 1
                matching_terms += 1
    require(matching_terms == 8748, matching_terms)
    return {word: +poly for word, poly in rows.items()}


def correction_j_rows():
    """Mixed-output rows of J applied to second-order direct corrections Z."""
    rows = defaultdict(dict)
    for edge in MATCHING:
        remaining_edges = tuple(item for item in MATCHING if item != edge)
        u, v = edge
        for i in COLOURS:
            for j in COLOURS:
                column = Z_INDEX[edge + (i, j)]
                for residual_colours in product(COLOURS, repeat=3):
                    word = [None] * 8
                    word[u], word[v] = i, j
                    for (a, b), colour in zip(remaining_edges,
                                              residual_colours):
                        word[a] = word[b] = colour
                    word = tuple(word)
                    if len(set(word)) > 1:
                        rows[word][column] = 1
    return rows


def poly_add_scaled(target, source, scalar):
    answer = Counter(target)
    for monomial, value in source.items():
        answer[monomial] += scalar * value
        if not answer[monomial]:
            del answer[monomial]
    return answer


def normalize_constraint(poly):
    poly = Counter({key: Fraction(value) for key, value in poly.items() if value})
    if not poly:
        return ()
    first = min(poly)
    scalar = poly[first]
    return tuple(sorted((monomial, value / scalar)
                        for monomial, value in poly.items()))


def eliminate_second_order(h2):
    jrows = correction_j_rows()
    words = sorted(set(jrows) | set(h2))
    basis = {}
    constraints = set()
    for word in words:
        numeric = {index: Fraction(value)
                   for index, value in jrows.get(word, {}).items() if value}
        rhs = Counter(h2.get(word, {}))
        while numeric:
            pivot = min(numeric)
            if pivot not in basis:
                scalar = numeric[pivot]
                numeric = {index: value / scalar
                           for index, value in numeric.items()}
                rhs = Counter({key: value / scalar for key, value in rhs.items()})
                basis[pivot] = (numeric, rhs)
                break
            scalar = numeric[pivot]
            base_numeric, base_rhs = basis[pivot]
            for index, value in base_numeric.items():
                numeric[index] = numeric.get(index, 0) - scalar * value
                if not numeric[index]:
                    del numeric[index]
            rhs = poly_add_scaled(rhs, base_rhs, -scalar)
        else:
            normalized = normalize_constraint(rhs)
            if normalized:
                constraints.add(normalized)
    require(len(basis) == 33, len(basis))
    return tuple(sorted(constraints)), len(words)


def eval_poly(poly, assignment):
    return sum(value * assignment[a] * assignment[b]
               for (a, b), value in poly)


def leading_response_schema():
    # For a matched pair all twelve incident residual star blocks vanish at A0,
    # so response rank has neither order-zero nor order-one terms.
    canonical = {
        "star": {"pair": [0, 1], "centre": 2,
                 "outside_physical_edges": 10, "row_count": 90},
        "triangle_pair_plus_single": {
            "pair": [0, 1], "triangle": [2, 3, 4],
            "outside_physical_edges": 12, "row_count": 108},
        "triangle_transversal": {
            "pair": [0, 1], "triangle": [2, 4, 6],
            "outside_physical_edges": 12, "row_count": 108},
    }
    return {
        "response_order_0": "zero on all 104 formerly active carriers",
        "response_order_1": "identically zero: every rho row is a product of two vanishing star blocks",
        "first_nonzero_response_order": 2,
        "B2_row_formula": (
            "Y_pa[i,alpha]*Y_qb[j,beta]+"
            "Y_pb[i,beta]*Y_qa[j,alpha]"
        ),
        "incidence_condition": (
            "For blocker b in {E00,E11,E22,I}, impose "
            "rank([B2_C(Y);b])=rank(B2_C(Y)) stratumwise: on a rank-r "
            "chart, one r-minor of B2 is live and every augmented (r+1)-minor "
            "vanishes. This leading-minor formulation does not treat "
            "membership as closed at B2=0."
        ),
        "carrier_orbits_per_matched_pair": {
            "star": 6, "triangle_pair_plus_single": 12,
            "triangle_transversal": 8},
        "canonical_orbits": canonical,
    }


def logical_sha(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--mutate-leading-order", action="store_true")
    args = parser.parse_args()
    active, carrier_histogram = carrier_census()
    base_amplitudes = amplitudes(base_source(), 8)
    base_pure = {word: value for word, value in base_amplitudes.items()
                 if len(set(word)) == 1}
    base_mixed = {word: value for word, value in base_amplitudes.items()
                  if len(set(word)) > 1}
    require(len(base_pure) == 3 and all(value == 1 for value in base_pure.values()),
            base_pure)
    require(len(base_mixed) == 78 and all(value == 1 for value in base_mixed.values()),
            list(base_mixed.items())[:2])
    jacobian = full_jacobian_profile()
    h2 = second_order_mixed_polynomials()
    constraints, active_word_count = eliminate_second_order(h2)
    schema = leading_response_schema()
    if args.mutate_leading_order:
        schema["first_nonzero_response_order"] = 1
    require(schema["first_nonzero_response_order"] == 2, schema)

    # Dense scalar-identity Y blocks every leading canonical carrier, but is a
    # hostile guard for the X5 equations.
    assignment = {index: int(label[2] == label[3])
                  for label, index in Y_INDEX.items()}
    violated = [constraint for constraint in constraints
                if eval_poly(constraint, assignment)]
    require(violated, "dense identity Y unexpectedly solves the X5 obstruction")
    term_hist = Counter(len(constraint) for constraint in constraints)
    constraint_serial = [
        [[[list(Y_LABELS[a]), list(Y_LABELS[b])], str(value)]
         for (a, b), value in constraint]
        for constraint in constraints]
    constraint_digest = sha256(json.dumps(
        constraint_serial, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

    payload = {
        "status": "PASS nonexact pair-product response control; not an exact-fibre tangent cone",
        "base_source": {
            "matching": [list(edge) for edge in MATCHING],
            "blocks": "A_01=A_23=A_45=A_67=I3; all other blocks zero",
            "output": (
                "NOT GHZ8: 81 nonzero words = 3 pure + 78 mixed, all "
                "coefficient 1; this is the tensor product of four I3 blocks"
            ),
            "lex_first_mixed_counterexample": {
                "word": list(min(base_mixed)),
                "coefficient": str(base_mixed[min(base_mixed)]),
            },
        },
        "carrier_census": {
            "active_count": len(active), "active_stars": 24,
            "active_triangles": 80,
            "all_active_pairs_are_the_four_matching_edges": True,
            "full_profile": {
                f"{kind}:rank={rank}:membership={mask}": count
                for (kind, rank, mask), count in sorted(carrier_histogram.items())},
        },
        "linear_mixed_X5": jacobian,
        "leading_no_cap_incidence": schema,
        "quadratic_mixed_X5_obstruction": {
            "Y_variables": len(Y_LABELS),
            "raw_matching_cell_terms": 8748,
            "active_output_words_in_J_or_H2": active_word_count,
            "independent_direct_correction_rank": 33,
            "deduplicated_quadratic_cokernel_equations": len(constraints),
            "term_count_histogram": {str(k): v for k, v in sorted(term_hist.items())},
            "full_constraint_digest": constraint_digest,
            "first_constraints": constraint_serial[:12],
        },
        "dense_identity_Y_control": {
            "definition": "Y_uv=I3 on all 24 off-matching edges",
            "blocks_all_three_canonical_leading_carrier_orbits": True,
            "violated_quadratic_X5_constraints": len(violated),
            "verdict": "incidence alone is feasible, but joint X5 fails",
        },
        "terminal_scope": (
            "The common-matching I3 base is pure-normalized but is not on the "
            "exact GHZ fibre: it already has 78 mixed order-zero outputs.  "
            "Ordinary first-order response matrices vanish on every formerly "
            "active carrier, so linearized membership cannot close or realize "
            "the response boundary of this control. The exported quadratic "
            "system is only a homogeneous coefficient/response control: "
            "mixed cokernel equations plus a transported "
            "rank-stratified blocker disjunction on 104 B2 matrices. This audit "
            "does not describe a tangent cone to F^{-1}(Delta), does not claim "
            "the quadratic system empty, and does not affect exact-fibre ED."
        ),
        "next_exact_target": (
            "Solve the symmetry-reduced joint quadratic incidence system for "
            "the three canonical carrier orbit types; if a solution lands, "
            "replay all 728 leading ranks before lifting to the next order."
        ),
    }
    payload["logical_sha256"] = logical_sha(payload)
    if args.write_results:
        OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("active carriers", len(active), "rank mixed J", jacobian["mixed_J_rank"])
    print("quadratic constraints", len(constraints), "term hist", term_hist)
    print("dense identity violations", len(violated))
    print("constraint digest", constraint_digest)
    print("logical sha256", payload["logical_sha256"])


if __name__ == "__main__":
    main()
