#!/usr/bin/env python3
"""Exact first-order minimum-norm/conormal controls for the Krenn map."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_blockwise_minimum_norm.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


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


def oriented(cell_values, u, v, a, b):
    if u < v:
        return cell_values.get((u, v, a, b), Fraction(0))
    return cell_values.get((v, u, b, a), Fraction(0))


def edge_choices(source, u, v):
    answer = []
    for a in range(3):
        for b in range(3):
            value = oriented(source, u, v, a, b)
            if value:
                answer.append((a, b, value))
    return answer


def amplitudes(source, n):
    answer = Counter()
    for matching in perfect_matchings(range(n)):
        choices = [edge_choices(source, u, v) for u, v in matching]
        if any(not row for row in choices):
            continue
        for selected in product(*choices):
            word = [None] * n
            coefficient = Fraction(1)
            for (u, v), (a, b, value) in zip(matching, selected):
                word[u], word[v] = a, b
                coefficient *= value
            answer[tuple(word)] += coefficient
    return +answer


def residual_amplitudes(source, n, p, q):
    remaining = tuple(v for v in range(n) if v not in (p, q))
    answer = Counter()
    for matching in perfect_matchings(remaining):
        choices = [edge_choices(source, u, v) for u, v in matching]
        if any(not row for row in choices):
            continue
        for selected in product(*choices):
            word = {}
            coefficient = Fraction(1)
            for (u, v), (a, b, value) in zip(matching, selected):
                word[u], word[v] = a, b
                coefficient *= value
            answer[tuple(word[v] for v in remaining)] += coefficient
    return remaining, +answer


def derivative_columns(source, n):
    """Literal J columns, labelled by endpoint-ordered source cells."""
    columns = {}
    for p, q in combinations(range(n), 2):
        remaining, residual = residual_amplitudes(source, n, p, q)
        for i in range(3):
            for j in range(3):
                column = {}
                for residual_word, coefficient in residual.items():
                    word = [None] * n
                    word[p], word[q] = i, j
                    for site, colour in zip(remaining, residual_word):
                        word[site] = colour
                    column[tuple(word)] = coefficient
                columns[p, q, i, j] = column
    return columns


def jacobian_rows(columns, n):
    labels = sorted(columns)
    index = {label: position for position, label in enumerate(labels)}
    rows = defaultdict(dict)
    for label, column in columns.items():
        for word, value in column.items():
            rows[word][index[label]] = value
    return labels, [rows[word] for word in product(range(3), repeat=n)]


def sparse_row_basis(rows):
    basis = {}
    for raw in rows:
        row = {index: Fraction(value) for index, value in raw.items() if value}
        while row:
            pivot = min(row)
            if pivot not in basis:
                scalar = row[pivot]
                row = {index: value / scalar for index, value in row.items()}
                basis[pivot] = row
                break
            scalar = row[pivot]
            base = basis[pivot]
            for index, value in base.items():
                row[index] = row.get(index, 0) - scalar * value
                if not row[index]:
                    del row[index]
    return basis


def in_sparse_rowspan(basis, raw):
    row = {index: Fraction(value) for index, value in raw.items() if value}
    while row:
        pivot = min(row)
        if pivot not in basis:
            return False
        scalar = row[pivot]
        for index, value in basis[pivot].items():
            row[index] = row.get(index, 0) - scalar * value
            if not row[index]:
                del row[index]
    return True


def nullspace_from_echelon(basis, ncols):
    pivots = set(basis)
    free = [index for index in range(ncols) if index not in pivots]
    answer = []
    for free_index in free:
        vector = [Fraction(0)] * ncols
        vector[free_index] = 1
        for pivot in sorted(basis, reverse=True):
            row = basis[pivot]
            vector[pivot] = -sum(value * vector[index]
                                 for index, value in row.items()
                                 if index != pivot)
        answer.append(vector)
    return answer


def source_row(source, labels):
    return {index: source.get(label, 0)
            for index, label in enumerate(labels) if source.get(label, 0)}


def dense_rank(rows, ncols=9):
    sparse = [{index: value for index, value in enumerate(row) if value}
              for row in rows]
    return len(sparse_row_basis(sparse))


def response_row(source, p, q, a, b, alpha, beta):
    return [
        oriented(source, p, a, i, alpha) * oriented(source, q, b, j, beta)
        + oriented(source, p, b, i, beta) * oriented(source, q, a, j, alpha)
        for i in range(3) for j in range(3)]


def n8_stationary_blocker_counterguard():
    layers = {
        0: ((0, 1), (2, 3), (4, 5), (6, 7)),
        1: ((0, 2), (1, 3), (4, 6), (5, 7)),
        2: ((0, 3), (1, 4), (2, 7), (5, 6)),
    }
    source = {edge + (colour, colour): Fraction(1)
              for colour, matching in layers.items() for edge in matching}
    columns = derivative_columns(source, 8)
    labels, rows = jacobian_rows(columns, 8)
    basis = sparse_row_basis(rows)
    stationary = in_sparse_rowspan(basis, source_row(source, labels))
    require(stationary and len(basis) == 226, (stationary, len(basis)))

    # Literal lex-first blocked response star: pair 01, residual centre 2.
    p, q, centre = 0, 1, 2
    residual = tuple(v for v in range(8) if v not in (p, q))
    carrier_rows = [response_row(source, p, q, a, b, alpha, beta)
                    for a, b in combinations(residual, 2)
                    if centre not in (a, b)
                    for alpha in range(3) for beta in range(3)]
    activity = []
    for colour in range(3):
        row = [Fraction(0)] * 9
        row[3 * colour + colour] = 1
        activity.append(row)
    activity.append([oriented(source, p, q, i, j)
                     for i in range(3) for j in range(3)])
    rank = dense_rank(carrier_rows)
    memberships = [dense_rank(carrier_rows + [row]) == rank
                   for row in activity]
    require(rank == 1 and memberships == [False, False, True, False],
            (rank, memberships))
    output = amplitudes(source, 8)
    require(len(output) == 5, output)
    return {
        "source": "canonical (4+4,8,8) diagonal P=2 source",
        "output_support": ["".join(map(str, word)) for word in sorted(output)],
        "is_GHZ_fibre_point": False,
        "jacobian_rank": len(basis),
        "rank_after_adjoining_source_norm_row": len(basis),
        "A_perpendicular_to_ker_J": True,
        "blocked_carrier": {"pair": [p, q], "kind": "star",
                            "centre": centre, "response_rank": rank,
                            "activity_memberships_diag0_diag1_diag2_direct":
                                memberships},
        "counterguard": (
            "Stationarity plus one literal blocker membership has an exact "
            "source realization and supplies no first-order lowering vector: "
            "A perpendicular ker(J) forbids one tautologically. The GHZ "
            "target equations and a genuine K-to-(v,w) second-order lift are "
            "therefore load-bearing."
        ),
    }


def block_least_norm_check(source, target, n):
    columns = derivative_columns(source, n)
    current = amplitudes(source, n)
    checks = []
    for p, q in combinations(range(n), 2):
        # Remove all terms using pq. Multi-affinity makes this exact.
        without = dict(source)
        for i in range(3):
            for j in range(3):
                without.pop((p, q, i, j), None)
        base = amplitudes(without, n)
        required = Counter(target)
        required.subtract(base)
        required = +required
        for i in range(3):
            for j in range(3):
                column = columns[p, q, i, j]
                norm = sum(value * value for value in column.values())
                numerator = sum(value * required.get(word, 0)
                                for word, value in column.items())
                expected = numerator / norm if norm else Fraction(0)
                actual = source.get((p, q, i, j), Fraction(0))
                require(actual == expected, ((p, q, i, j), actual,
                                              expected, norm, numerator))
        checks.append({"edge": [p, q],
                       "nonzero_columns": sum(bool(columns[p, q, i, j])
                                              for i in range(3) for j in range(3)),
                       "column_supports_pairwise_disjoint": all(
                           not (set(columns[p, q, i, j]) &
                                set(columns[p, q, k, ell]))
                           for (i, j), (k, ell) in combinations(
                               product(range(3), repeat=2), 2))})
    require(current == target, (current, target))
    return columns, checks


def n4_control():
    source = {}
    layers = {
        0: ((0, 1), (2, 3)),
        1: ((0, 2), (1, 3)),
        2: ((0, 3), (1, 2)),
    }
    for colour, matching in layers.items():
        for u, v in matching:
            source[u, v, colour, colour] = Fraction(1)
    target = Counter({(0,) * 4: Fraction(1),
                      (1,) * 4: Fraction(1),
                      (2,) * 4: Fraction(1)})
    columns, block_checks = block_least_norm_check(source, target, 4)
    labels, rows = jacobian_rows(columns, 4)
    basis = sparse_row_basis(rows)
    stationarity = in_sparse_rowspan(basis, source_row(source, labels))
    require(stationarity, "n4 norm row not in Jacobian rowspace")
    require(len(basis) == 51, len(basis))
    kernel = nullspace_from_echelon(basis, len(labels))
    require(len(kernel) == 3, len(kernel))

    # lambda has value one on each pure output and zero elsewhere, so J*lambda=A.
    # The constrained Hessian is <v,w>-<lambda,D2F(v,w)>.
    label_index = {label: index for index, label in enumerate(labels)}

    def constrained_hessian(left, right):
        value = sum(x * y for x, y in zip(left, right))
        for colour, matching in layers.items():
            (e1, e2) = matching
            i1 = label_index[e1 + (colour, colour)]
            i2 = label_index[e2 + (colour, colour)]
            value -= left[i1] * right[i2] + right[i1] * left[i2]
        return value

    bordered = [[constrained_hessian(left, right) for right in kernel]
                for left in kernel]
    require(bordered == [[4 if i == j else 0 for j in range(3)]
                         for i in range(3)], bordered)
    # Global minimum: for each colour, |xy+uv+zw| <= sum six squares / 2.
    # The three pure coordinate sets are disjoint, so norm^2 >= 2+2+2.
    norm_squared = sum(value * value for value in source.values())
    require(norm_squared == 6, norm_squared)
    return {
        "source_cells": [list(cell) + [str(value)]
                         for cell, value in sorted(source.items())],
        "output": {"".join(map(str, word)): str(value)
                   for word, value in sorted(target.items())},
        "global_minimum_norm_squared": "6",
        "global_minimum_proof": (
            "For each pure colour, Cauchy gives |a01*a23+a02*a13+"
            "a03*a12| <= (sum of its six diagonal-cell squares)/2. "
            "Three unit pure amplitudes therefore force norm^2>=6; the "
            "displayed source attains equality."
        ),
        "jacobian_rank": len(basis),
        "rank_after_adjoining_source_norm_row": len(basis),
        "source_norm_row_in_J_rowspace": stationarity,
        "kernel_dimension": len(kernel),
        "constrained_hessian_on_kernel_basis":
            [[int(value) for value in row] for row in bordered],
        "constrained_hessian_verdict": "positive definite (4*I3)",
        "exact_second_order_arcs": (
            "Each kernel basis vector scales one live opposite-edge pair as "
            "(exp(t),exp(-t)). In A+t*v+t^2*w notation, w has 1/2 on "
            "both cells and satisfies Jw+(1/2)D2F(v,v)=0 exactly."
        ),
        "block_checks": block_checks,
    }


def invisible_chord_control():
    base = {
        (0, 1, 0, 0): Fraction(1),
        (2, 3, 0, 0): Fraction(1),
        (4, 5, 0, 0): Fraction(1),
        (6, 7, 0, 0): Fraction(1),
    }
    chord = (0, 2, 0, 0)
    source = dict(base)
    source[chord] = Fraction(1)
    require(amplitudes(source, 8) == amplitudes(base, 8), "chord became visible")
    columns = derivative_columns(source, 8)
    require(not columns[chord], columns[chord])
    labels, rows = jacobian_rows(columns, 8)
    basis = sparse_row_basis(rows)
    augmented = dict(source_row(source, labels))
    stationarity = in_sparse_rowspan(basis, augmented)
    require(not stationarity, "nonminimal invisible chord passed stationarity")
    chord_index = labels.index(chord)
    kernel_witness = {chord_index: Fraction(1)}
    require(all(row.get(chord_index, 0) == 0 for row in rows),
            "chord coordinate not in kernel")
    pairing = augmented[chord_index]
    require(pairing == 1, pairing)
    return {
        "base_matching": [[0, 1], [2, 3], [4, 5], [6, 7]],
        "chord": list(chord),
        "top_output_unchanged": True,
        "all_residual_six_site_hafnians_for_chord": 0,
        "T_chord_rank": 0,
        "jacobian_rank": len(basis),
        "rank_after_adjoining_source_norm_row": len(basis) + 1,
        "source_norm_row_in_J_rowspace": False,
        "kernel_witness_pairing_with_source": str(pairing),
        "minimum_norm_conclusion": "the chord coefficient must be zero",
    }


def logical_sha(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--mutate-invisible", action="store_true")
    args = parser.parse_args()
    n4 = n4_control()
    invisible = invisible_chord_control()
    blocker_guard = n8_stationary_blocker_counterguard()
    if args.mutate_invisible:
        invisible["T_chord_rank"] = 1
    require(invisible["T_chord_rank"] == 0, invisible)
    payload = {
        "status": "PASS exact blockwise minimum-norm/conormal controls",
        "blockwise_theorem": (
            "Fix all blocks except A_e. Multi-affinity gives F=T_e(A_e)+b. "
            "At a global fibre norm minimizer every u in ker(T_e) is an "
            "exact affine fibre direction, so A_e is orthogonal to ker(T_e), "
            "equivalently A_e lies in im(T_e^*). For minimization on a fixed "
            "no-cap incidence/rank stratum, this deletion argument applies "
            "only when the affine cell variation preserves that stratum."
        ),
        "source_labelled_Te": (
            "The column for (e=pq;i,j) is supported exactly on output words "
            "with w_p=i,w_q=j and has coefficient the residual (n-2)-site "
            "Hafnian. The nine endpoint labels give pairwise-disjoint word "
            "supports. Therefore a cell whose every residual Hafnian vanishes "
            "must itself vanish at a minimum-norm point."
        ),
        "global_regular_stationarity": (
            "At a regular fibre minimum, rank([J_A;A*])=rank(J_A), or "
            "A orthogonal to ker(J_A). At a singular point retain the separate "
            "Fritz-John branch alpha*A=J_A^*lambda, including alpha=0. "
            "A full-fibre minimizer may be an active-cap source and therefore "
            "need not represent a hypothetical no-cap point."
        ),
        "carrier_order_guard": (
            "No carrier L_C is identified with T_e. Literal T_e rows are "
            "residual-Hafnian multiples of coordinate rows; rho is degree two "
            "and belongs only to the complementary second-derivative split."
        ),
        "n4_exact_GHZ": n4,
        "k8_invisible_chord": invisible,
        "one_blocker_stationarity_counterguard": blocker_guard,
        "next_exact_target": (
            "On an attained interior chart of a fixed no-cap incidence/rank "
            "stratum, add the incidence-normal multipliers and test the KKT "
            "system for inconsistency. Treat finite active-cap/rank-drop "
            "boundary and infinity separately; do not retry a carrier-as-"
            "Jacobian rank argument."
        ),
    }
    payload["logical_sha256"] = logical_sha(payload)
    if args.write_results:
        OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("n4 rank/augmentation", n4["jacobian_rank"],
          n4["rank_after_adjoining_source_norm_row"])
    print("invisible rank/augmentation", invisible["jacobian_rank"],
          invisible["rank_after_adjoining_source_norm_row"])
    print("logical sha256", payload["logical_sha256"])


if __name__ == "__main__":
    main()
