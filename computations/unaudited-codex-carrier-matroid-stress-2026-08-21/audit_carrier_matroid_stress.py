#!/usr/bin/env python3
"""Bounded exact algebraic-matroid/rigidity-stress screen.

The carrier part is an exact rational vector-matroid calculation on all 728
star/triangle response matrices.  The tail part records what the frozen
380-by-12 full-rank theorem means matroidally and replays the smallest exact
remote-component counterexample.  No polynomial ideal is solved.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CORE_PATH = (ROOT / "computations" /
    "unaudited-codex-response-star-2026-08-20" /
    "response_star_core.py")
TAIL_PATH = (ROOT / "computations" /
    "unaudited-codex-tail-polar-source-lift-2026-08-21" /
    "results_611_71_sdr_and_332_rescue.json")
OUT = HERE / "results_carrier_matroid_stress.json"
EXPECTED_TAIL_LOGICAL = \
    "6d55fe4a761cc60665268e1ebfa61215390b6994134749b7fa6fe5610f2b4ad2"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None,
            ("cannot load", str(path)))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def logical_sha(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def dense_source():
    edges = tuple(combinations(range(8), 2))
    return {
        edge: [[Fraction(1 + ((index+i+2*j+i*j) % 13))
                for j in range(3)] for i in range(3)]
        for index, edge in enumerate(edges)
    }


def pure_normalize(core, source):
    """A rational site-colour torus normalization at site zero."""
    pure = [core.hafnian(source, (colour,)*8) for colour in range(3)]
    require(all(value for value in pure), "dense pure Hafnian vanished")
    lambdas = {(site, colour): Fraction(1)
               for site in range(8) for colour in range(3)}
    for colour in range(3):
        lambdas[0, colour] = 1/pure[colour]
    normalized = {}
    for (u, v), matrix in source.items():
        normalized[u, v] = [
            [matrix[i][j]*lambdas[u, i]*lambdas[v, j]
             for j in range(3)]
            for i in range(3)
        ]
    require([core.hafnian(normalized, (colour,)*8)
             for colour in range(3)] == [1, 1, 1],
            "rational torus normalization failed")
    return normalized, pure, lambdas


def independent_row_indices(core, rows):
    indices = []
    basis = []
    rank = 0
    for index, row in enumerate(rows):
        new_rank = core.rank(basis+[row])
        if new_rank > rank:
            indices.append(index)
            basis.append(row)
            rank = new_rank
            if rank == 9:
                break
    return indices


def solve_basis_coefficients(basis_rows, right_sides):
    """Solve sum_i c_i*basis_i=ell for several ell, exactly over Q."""
    n = len(basis_rows)
    require(n == 9, "expected a nine-row basis")
    # Columns are coefficients c_i; equations are ambient coordinates.
    matrix = [
        [Fraction(basis_rows[column][row]) for column in range(n)]
        + [Fraction(rhs[row]) for rhs in right_sides]
        for row in range(n)
    ]
    for column in range(n):
        pivot = next((row for row in range(column, n)
                      if matrix[row][column]), None)
        require(pivot is not None, "carrier basis became singular")
        matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
        scale = matrix[column][column]
        matrix[column] = [value/scale for value in matrix[column]]
        for row in range(n):
            if row == column or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [left-scale*right for left, right
                           in zip(matrix[row], matrix[column])]
    return tuple(tuple(matrix[row][n+rhs]
                       for row in range(n))
                 for rhs in range(len(right_sides)))


def add_scaled(rows, coefficients):
    return tuple(sum((coefficient*row[column]
                      for coefficient, row in zip(coefficients, rows)),
                     Fraction(0))
                 for column in range(9))


def circuit_audit(core, source):
    detailed = []
    rank_histogram = Counter()
    circuit_size_histogram = Counter()
    stress_dimension_histogram = Counter()
    first_certificate = None
    edges = tuple(combinations(range(8), 2))
    for p, q in edges:
        residual = tuple(site for site in range(8) if site not in (p, q))
        carriers = [
            ("star", (centre,), *core.response_star_matrix(
                source, p, q, centre))
            for centre in residual
        ]
        carriers += [
            ("triangle", triangle, *core.response_triangle_matrix(
                source, p, q, triangle))
            for triangle in combinations(residual, 3)
        ]
        require(len(carriers) == 26, "carrier count per pair changed")
        blockers = core.activity_rows(source, p, q)
        for kind, carrier_label, row_labels, rows in carriers:
            indices = independent_row_indices(core, rows)
            rank = len(indices)
            rank_histogram[kind, rank] += 1
            require(rank == 9, ("dense carrier lost full rank", p, q,
                                kind, carrier_label, rank))
            basis = [rows[index] for index in indices]
            coefficients = solve_basis_coefficients(basis, blockers)
            circuit_records = []
            for blocker_index, (ell, coeffs) in enumerate(
                    zip(blockers, coefficients)):
                require(add_scaled(basis, coeffs) == tuple(ell),
                        ("fundamental circuit failed", p, q, kind,
                         carrier_label, blocker_index))
                support = [position for position, value in enumerate(coeffs)
                           if value]
                # Independence of the basis makes this the unique expression;
                # after zero coefficients are removed it is a minimal circuit.
                circuit_size = len(support)+1
                circuit_size_histogram[kind, blocker_index, circuit_size] += 1
                record = {
                    "blocker": blocker_index,
                    "response_basis_positions": support,
                    "coefficients": [str(coeffs[position])
                                     for position in support],
                    "circuit_size_including_blocker": circuit_size,
                }
                circuit_records.append(record)
            stress_dimension = len(rows)-rank
            stress_dimension_histogram[kind, stress_dimension] += 1
            carrier_record = {
                "pair": [p, q],
                "kind": kind,
                "carrier_label": list(carrier_label),
                "response_rows": len(rows),
                "rank": rank,
                "kernel_flex_dimension": 9-rank,
                "ordinary_response_stress_dimension": stress_dimension,
                "basis_row_labels": [row_labels[index] for index in indices],
                "blocker_fundamental_circuits": circuit_records,
            }
            detailed.append(carrier_record)
            if first_certificate is None:
                first_certificate = carrier_record
    require(len(detailed) == 728, "global carrier count changed")
    require(sum(count for (kind, rank), count in rank_histogram.items()
                if rank == 9) == 728, "not every dense carrier has rank nine")
    return {
        "records": detailed,
        "records_logical_sha256": logical_sha(detailed),
        "rank_histogram": {
            f"{kind}:rank{rank}": count
            for (kind, rank), count in sorted(rank_histogram.items())},
        "circuit_size_histogram": {
            f"{kind}:blocker{blocker}:size{size}": count
            for (kind, blocker, size), count
            in sorted(circuit_size_histogram.items())},
        "stress_dimension_histogram": {
            f"{kind}:dimension{dimension}": count
            for (kind, dimension), count
            in sorted(stress_dimension_histogram.items())},
        "first_exact_fundamental_circuit_certificate": first_certificate,
    }


def cyclic_remote_audit():
    points = []
    for x, y, z in product(range(-2, 3), repeat=3):
        equations = (x-y*z, y-x*z, z-x*y)
        if equations == (0, 0, 0):
            points.append((x, y, z))
        require(x**3-x == (x*x-1)*equations[0]
                - z*equations[1]-x*z*equations[2],
                ("cyclic x-cubic identity failed", x, y, z))
    require(points == [(-1, -1, 1), (-1, 1, -1), (0, 0, 0),
                       (1, -1, -1), (1, 1, 1)],
            ("cyclic point census changed", points))
    return points


def main():
    core = load_module("carrier_matroid_response_core", CORE_PATH)
    tail = json.loads(TAIL_PATH.read_text())
    require(tail["logical_sha256"] == EXPECTED_TAIL_LOGICAL,
            "tail-response theorem digest changed")

    source, pre_normalization_h, lambdas = pure_normalize(
        core, dense_source())
    require(all(entry for matrix in source.values()
                for row in matrix for entry in row),
            "dense witness acquired a zero cell")
    circuits = circuit_audit(core, source)
    cyclic_points = cyclic_remote_audit()

    # A single positive mixed amplitude is enough to guard the scope: this
    # rational witness is a response-interface counterexample, not X5.
    mixed_word = tuple(map(int, "00000001"))
    mixed_value = core.hafnian(source, mixed_word)
    require(mixed_value > 0, "dense witness accidentally entered X5")

    payload = {
        "status": "PASS bounded exact carrier matroid/stress screen",
        "scope": {
            "carrier_computation": "all 728 carriers over exact Q",
            "polynomial_solve": False,
            "dense_witness_satisfies_X5": False,
            "purpose": "test whether response/tail matroid data alone force a cap or zero-tail descent",
        },
        "matroid_formulation": {
            "carrier_vector_matroid": (
                "M_C is the row-vector matroid on the response rows R_C "
                "together with blockers b_0,b_1,b_2,b_3 in Q^9."),
            "blocker_equivalence": (
                "b_i lies in cl(R_C) iff R_C union {b_i} has a circuit "
                "containing b_i; its coefficients are a fundamental stress."),
            "active_cap_equivalence": (
                "C is active iff every b_i is outside cl(R_C), equivalently "
                "b_i is a coloop in M_C restricted to R_C union {b_i} for all i."),
            "no_cap_equivalence": (
                "For every C choose at least one i with a blocker circuit. "
                "Thus local circuit language is exactly the original 728 "
                "four-way disjunction, not a compression of it."),
            "rigidity_dictionary": {
                "cap_flex_space": "ker(L_C), dimension 9-rank(L_C)",
                "response_stress_space": "ker(L_C^T), dimension |R_C|-rank(L_C)",
                "warning": "Maximal response rigidity rank(L_C)=9 kills cap flexes and makes every blocker dependent; stresses favour blockedness, not activity.",
            },
            "cross_carrier_limitation": (
                "Different cap pairs have different nine-dimensional K spaces. "
                "Their direct-sum matroid has no circuit elimination across pairs; "
                "the shared polynomial source parametrization is lost after evaluation."),
        },
        "exact_pure_normalized_dense_counterexample": {
            "construction": (
                "A_uv[i,j]=1+((edge_index+i+2j+ij) mod 13), followed by "
                "the rational site-colour torus scaling lambda_(0,c)=1/H_c."),
            "pre_normalization_pure_H": [str(value)
                                          for value in pre_normalization_h],
            "normalizing_lambda_at_site0": [str(lambdas[0, colour])
                                              for colour in range(3)],
            "post_normalization_pure_H": [1, 1, 1],
            "all_252_source_cells_nonzero": True,
            "all_168_cross_colour_tail_cells_nonzero": True,
            "carrier_rank_histogram": circuits["rank_histogram"],
            "every_carrier_blocked_by_every_blocker": True,
            "all_2912_blocker_memberships_have_exact_circuits": True,
            "circuit_size_histogram": circuits["circuit_size_histogram"],
            "ordinary_stress_dimension_histogram":
                circuits["stress_dimension_histogram"],
            "fundamental_circuit_ledger_logical_sha256":
                circuits["records_logical_sha256"],
            "first_exact_fundamental_circuit_certificate":
                circuits["first_exact_fundamental_circuit_certificate"],
            "selected_nonzero_mixed_X5_row": {
                "word": "00000001", "value": str(mixed_value)},
            "scope_guard": (
                "This witnesses failure of a response-matroid-only theorem. "
                "It is not a source solution because the displayed mixed amplitude is nonzero."),
        },
        "tail_response_matroid": {
            "frozen_matrix_shape": [380, 12],
            "generic_rank": 12,
            "selected_column_matroid": "free rank-12 matroid; it has no column circuit",
            "generic_row_stress_dimension": 368,
            "meaning": (
                "The row stresses are syzygies of the lowest linear layer. "
                "They do not encode the undeleted equal/lower columns or nonlinear remainder."),
            "remote_counterexample": {
                "equations": ["x-y*z", "y-x*z", "z-x*y"],
                "initial_matrix": "I_3",
                "initial_column_matroid": "free rank 3",
                "exact_points": [list(point) for point in cyclic_points],
                "nonzero_remote_points": len(cyclic_points)-1,
                "consequence": "Even full initial rigidity does not imply global zero-tail descent."},
            "frozen_tail_digest": EXPECTED_TAIL_LOGICAL,
        },
        "verdict": {
            "stress_duality_replaces_728_casework": False,
            "stress_duality_forces_clean_cap": False,
            "tail_matroid_rank_forces_zero_tail": False,
            "reason": (
                "The carrier matroid restates each blocker membership and "
                "forgets cross-carrier source coupling; the tail matroid "
                "forgets nonlinear/remote components."),
            "smallest_plausible_upgrade": (
                "Construct a source-identity map from tail Fitting minors to "
                "carrier augmented minors, or compute an algebraic matroid/Jacobian "
                "of the joint X5 incidence. Either upgrade reintroduces the "
                "missing coefficient-level coupling rather than eliminating it."),
        },
    }
    payload["logical_sha256"] = logical_sha(payload)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True)+"\n")
    print(json.dumps({
        "logical_sha256": payload["logical_sha256"],
        "carrier_rank_histogram": circuits["rank_histogram"],
        "fundamental_circuit_ledger_logical_sha256":
            circuits["records_logical_sha256"],
        "remote_points": len(cyclic_points)-1,
        "verdict": payload["verdict"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
