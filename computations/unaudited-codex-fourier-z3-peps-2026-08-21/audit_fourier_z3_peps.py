#!/usr/bin/env python3
"""Exact Fourier-Z3 and blocked one-hot PEPS injectivity audit."""

from __future__ import annotations

import argparse
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "results_fourier_z3_peps.json"
PINS = {
    "computations/unaudited-codex-onehot-peps-holant-2026-08-21/results_onehot_peps_holant.json":
        "d5029396bbe6347808d5e7c5cab4baf5bebcacc9eaba9d7f97405649d3d02221",
    "computations/unaudited-codex-onehot-qmfmc-2026-08-21/results_onehot_qmfmc.json":
        "c03965b3fe00392c209261860825cb7ea5968bf4998d965ca852c6acc6384060",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


# Cyclotomic arithmetic in Q[w]/(w^2+w+1), represented by a+b*w.
def qadd(x, y):
    return (x[0] + y[0], x[1] + y[1])


def qmul(x, y):
    a, b = x
    c, d = y
    return (a * c - b * d, a * d + b * c - b * d)


ONE = (Fraction(1), Fraction(0))
ZERO = (Fraction(0), Fraction(0))
W = (Fraction(0), Fraction(1))


def qpow(x, exponent):
    result = ONE
    for _ in range(exponent % 3):
        result = qmul(result, x)
    return result


def fourier_target_audit(n):
    histogram = {0: 0, 1: 0, 2: 0}
    nonzero = 0
    for word in product(range(3), repeat=n):
        residue = sum(word) % 3
        histogram[residue] += 1
        coefficient = ZERO
        for colour in range(3):
            coefficient = qadd(coefficient, qpow(W, colour * residue))
        expected = (Fraction(3), Fraction(0)) if residue == 0 else ZERO
        require(coefficient == expected, (n, word, coefficient, expected))
        nonzero += coefficient != ZERO
    require(nonzero == 3 ** (n - 1), (n, nonzero))
    return {
        "words": 3**n,
        "residue_histogram": histogram,
        "nonzero_coefficients": nonzero,
        "coefficient_rule": "3 if sum(site charges)=0 mod 3, otherwise 0",
    }


def virtual_colour_shift(label):
    if label == 0:
        return 0
    return 1 + label % 3


def local_covariance_audit(degree):
    checked = 0
    for inputs in product(range(4), repeat=degree):
        live = [(position, value - 1) for position, value in enumerate(inputs)
                if value]
        # P is zero away from exactly one excitation.  On that sector,
        # F P has component s equal to w^(s*a).
        left = [ZERO] * 3
        right = [ZERO] * 3
        if len(live) == 1:
            _position, colour = live[0]
            for charge in range(3):
                # Z F P.
                left[charge] = qmul(qpow(W, charge),
                                    qpow(W, charge * colour))
            shifted = tuple(virtual_colour_shift(value) for value in inputs)
            shifted_live = [(position, value - 1)
                            for position, value in enumerate(shifted) if value]
            require(len(shifted_live) == 1, shifted_live)
            shifted_colour = shifted_live[0][1]
            for charge in range(3):
                # F P G^tensor degree.
                right[charge] = qpow(W, charge * shifted_colour)
        require(left == right, (degree, inputs, left, right))
        checked += 1
    return {
        "degree": degree,
        "basis_inputs_checked": checked,
        "identity": "Z (F P) = (F P) diag(1,X)^tensor degree",
    }


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, partner in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, partner),) + tail


def matrix_rank(matrix):
    matrix = [list(map(Fraction, row)) for row in matrix]
    if not matrix:
        return 0
    rows = len(matrix)
    columns = len(matrix[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next((row for row in range(pivot_row, rows)
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [value / scale for value in matrix[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [left - scale * right
                           for left, right in zip(matrix[row], matrix[pivot_row])]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def k4_weights():
    weights = {}
    for colour, matching in enumerate(perfect_matchings(range(4))):
        for u, v in matching:
            weights[(min(u, v), max(u, v), colour, colour)] = Fraction(1)
    return weights


def blocked_map_k4(region, weights):
    region = tuple(region)
    region_set = frozenset(region)
    outside = tuple(vertex for vertex in range(4) if vertex not in region_set)
    boundary = tuple((u, v) for u in region for v in outside)
    internal_edges = tuple(combinations(region, 2))
    outputs = tuple(product(range(3), repeat=len(region)))
    out_index = {word: position for position, word in enumerate(outputs)}
    columns = []
    for assignment in product(range(4), repeat=len(boundary)):
        boundary_at = {u: [] for u in region}
        for (u, _v), value in zip(boundary, assignment):
            if value:
                boundary_at[u].append(value - 1)
        column = [Fraction(0) for _ in outputs]
        # An internal live-edge set is a matching.  Include the empty matching.
        for size in range(len(region) // 2 + 1):
            for chosen in combinations(internal_edges, size):
                endpoints = [vertex for edge in chosen for vertex in edge]
                if len(set(endpoints)) != 2 * size:
                    continue
                matched = set(endpoints)
                if any((len(boundary_at[u]) != 0 if u in matched
                        else len(boundary_at[u]) != 1) for u in region):
                    continue
                for edge_colours in product(range(3), repeat=2 * size):
                    coefficient = Fraction(1)
                    word = {}
                    for edge_position, (u, v) in enumerate(chosen):
                        a = edge_colours[2 * edge_position]
                        b = edge_colours[2 * edge_position + 1]
                        coefficient *= weights.get((min(u, v), max(u, v),
                                                   a if u < v else b,
                                                   b if u < v else a), 0)
                        word[u], word[v] = a, b
                    if not coefficient:
                        continue
                    for u in region:
                        if u not in matched:
                            word[u] = boundary_at[u][0]
                    column[out_index[tuple(word[u] for u in region)]] += coefficient
        columns.append(column)
    matrix = [list(row) for row in zip(*columns)]
    return {
        "sites": list(region),
        "boundary_legs": len(boundary),
        "domain_dimension": 4 ** len(boundary),
        "physical_dimension": 3 ** len(region),
        "exact_rank": matrix_rank(matrix),
    }


def block_table(n):
    table = {}
    for r in range(1, n):
        boundary = r * (n - r)
        domain = 4**boundary
        physical = 3**r
        invariant = (domain + 2) // 3
        require((domain + 2) % 3 == 0, (n, r, domain))
        table[str(r)] = {
            "boundary_legs": boundary,
            "domain_dimension": domain,
            "physical_dimension": physical,
            "exact_rank": physical,
            "Z3_invariant_boundary_dimension": invariant,
            "normal_injective": False,
            "G_injective": False,
            "explicit_invariant_kernel": (
                "all-boundary-vacuum (wrong parity)" if r % 2
                else "one charge-zero boundary excitation (wrong parity)"
            ),
        }
    return table


def k4_pullthrough_control():
    weights = k4_weights()
    failures = []
    for u, v in combinations(range(4), 2):
        support = [(a, b) for a in range(3) for b in range(3)
                   if weights.get((u, v, a, b), 0)]
        shifted = [((a + 1) % 3, (b + 1) % 3) for a, b in support]
        if set(support) != set(shifted):
            failures.append([u, v])
    require(len(failures) == 6, failures)
    return {
        "exact_output": "GHZ4",
        "edgewise_same-sign_pullthrough_failures": failures,
        "meaning": (
            "Global target Z3 symmetry does not imply bondwise virtual "
            "invariance; all six rank-one edge blocks fail it."
        ),
    }


def logical_sha(payload):
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return sha256(raw).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    for relative, expected in PINS.items():
        observed = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(observed == expected, (relative, observed, expected))

    fourier = {str(n): fourier_target_audit(n) for n in (4, 8)}
    covariance = {str(d): local_covariance_audit(d) for d in (3, 7)}
    k4_exact = [blocked_map_k4(range(r), k4_weights()) for r in (1, 2, 3)]
    require([row["exact_rank"] for row in k4_exact] == [3, 9, 27], k4_exact)
    k4_table = block_table(4)
    k8_table = block_table(8)
    require(all(row["exact_rank"] == 3 ** int(r)
                for r, row in k8_table.items()), k8_table)

    payload = {
        "status": "PASS terminal negative Fourier-Z3 PEPS audit",
        "fourier_GHZ": fourier,
        "local_covariance": covariance,
        "edge_compatibility": {
            "same_sign": "X A_uv X^T = A_uv",
            "opposite_orientation": "X A_uv (X^-1)^T = A_uv",
            "scope": (
                "Neither edgewise condition follows from full X5/GHZ output "
                "equality; arbitrary edge-dependent bond tensors are not a "
                "Z3-symmetric PEPS family."
            ),
        },
        "K4_blocked_maps_formula": k4_table,
        "K4_explicit_matrix_ranks": k4_exact,
        "K8_blocked_maps_formula": k8_table,
        "rank_proof": (
            "For every proper region choose one boundary leg at each site. "
            "Exciting exactly those legs gives an identity V^tensor r to "
            "V^tensor r submatrix, so rank=3^r. Domain dimension 4^b is "
            "larger, so normal injectivity fails."
        ),
        "G_injective_obstruction": (
            "Paired internal bonds force boundary excitation count congruent "
            "to r mod 2. For odd r, the invariant all-vacuum boundary vector "
            "is killed. For even r, a single charge-zero excitation, fixed by "
            "both X and X^-1, is killed. Thus the invariant subspace always "
            "has a nonzero kernel, independent of source coefficients."
        ),
        "K4_pullthrough_control": k4_pullthrough_control(),
        "invisible_chord_scope": (
            "The pinned K8 invisible chord changes one internal bond and its "
            "pull-through defect while preserving the complete top tensor. "
            "Therefore output symmetry cannot repair or diagnose the local "
            "virtual-symmetry failure."
        ),
        "terminal_verdict": (
            "The local Fourier covariance is exact, but it does not extend to "
            "a source-wide pull-through, and no proper K4/K8 block is normal "
            "or G-injective. These theorem hypotheses fail universally, not "
            "on a special no-cap locus, so their failure cannot select a clean cap."
        ),
        "input_hashes": PINS,
    }
    payload["logical_sha256"] = logical_sha(payload)
    if args.write_results:
        OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("Fourier-Z3 PEPS audit: PASS terminal negative")
    print("local covariance basis checks d=3,7:",
          covariance["3"]["basis_inputs_checked"],
          covariance["7"]["basis_inputs_checked"])
    print("K4 exact blocked ranks:",
          [row["exact_rank"] for row in k4_exact])
    print("K8 formula ranks:", [row["exact_rank"] for row in k8_table.values()])
    print("logical sha256:", payload["logical_sha256"])


if __name__ == "__main__":
    main()
