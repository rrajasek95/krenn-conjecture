#!/usr/bin/env python3
"""Exact local algebra behind the source-labelled gluing dichotomy.

This checker deliberately proves only the pointwise finite-dimensional
alternative.  It does not declare the missing physical comparison map, an
exhaustive physical C1 registry, or a global X5-to-cap theorem.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from functools import reduce
from hashlib import sha256
from itertools import combinations, product
import json
from math import gcd
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PINS = {
    "computations/verify_overlap_complex_common_factor_countermodel.py":
        "236e001e6b6793694804e448625ff1cc296bde3ce5e63b0a77186d7be65f1128",
    "computations/verify_derived_base_change_relative_cap_obstruction.py":
        "19c38d42710de2df403aa5cdf8513b6c03a758ab01eb281ce9da21564ca907d3",
    "computations/verify_h3_primitive_attaching_universal_module.py":
        "9116553a78b231898355f17ed1f6ccada816d9954ad037a71c8318cfb391a927",
    "computations/verify_h3_component_iv_physical_definability_gate.py":
        "d2753b9e885464243a471387f168531484edafa8aa4bb34d160308a128237c00",
    "computations/verify_h3_kappa_lambda_literal_mapping_cone_normalization_gate.py":
        "b60538f9db5b8c2984bbee95e0a05f383408e9ab7c13680216adf56386682522",
    "computations/verify_h3_gamma_star_source_derived_free_closure_census.py":
        "a479ac8759bf7a18b43ee91d8b1ab7d0b432c48a7787b065cac68403ace3df3a",
    "computations/verify_h3_gamma_star_physical_c1_registry_counterguard.py":
        "549c60c9613dff00ea2e29038970fd5a26715ba3f64dca5dd22980c8baab99ce",
    "computations/verify_h3_eqsystem_augp2_actual_presentation_underdetermination_gate.py":
        "2c112bffeef2c6adb00029077b6b231de396ace76c78756ab0e11e20078a557b",
    "computations/verify_h3_psi_source_grade_macaulay_exhaustiveness_terminal_gate.py":
        "2ae3d0fe36ca6ab92ee506b4a4441d6476ecb09567a1441c66f54793e304980d",
    "computations/verify_h3_actual_source_primitive_terminal_reduction_gate.py":
        "5754c85f7ae4b714777cdbb0f941672ade1977c5568f332a0dc8e317e4952927",
    "computations/verify_h3_canonical_principal_parts_gammajet_enrichment_gate.py":
        "0163890e3ec1a7fd115e93f34f68c37a5c82eaf984b36c5b72531c39e5769a0f",
    "notes/h3-canonical-principal-parts-gammajet-enrichment-gate.md":
        "35e459d65a8252b7ad6bd930094e587b989f2ee3ee146870fa86b14f99218e83",
}

EXPECTED_LEDGER_SHA256 = "b55e8c400663a4b7a8477a21bda4a13234f51757dfe0b6f18e635486efa502fc"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def file_sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def determinant(matrix: list[list[Q]]) -> Q:
    a = [row[:] for row in matrix]
    n = len(a)
    det = Q(1)
    for col in range(n):
        pivot = next((row for row in range(col, n) if a[row][col]), None)
        if pivot is None:
            return Q(0)
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            det = -det
        value = a[col][col]
        det *= value
        a[col] = [x / value for x in a[col]]
        for row in range(col + 1, n):
            factor = a[row][col]
            if factor:
                a[row] = [x - factor * y for x, y in zip(a[row], a[col])]
    return det


def rank(columns: list[tuple[Q, ...]]) -> int:
    if not columns:
        return 0
    matrix = [[columns[col][row] for col in range(len(columns))]
              for row in range(len(columns[0]))]
    a = [row[:] for row in matrix]
    r = 0
    for col in range(len(columns)):
        pivot = next((row for row in range(r, len(a)) if a[row][col]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        value = a[r][col]
        a[r] = [x / value for x in a[r]]
        for row in range(len(a)):
            if row != r and a[row][col]:
                factor = a[row][col]
                a[row] = [x - factor * y for x, y in zip(a[row], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def dot(x: tuple[Q, ...], y: tuple[Q, ...]) -> Q:
    return sum((a * b for a, b in zip(x, y)), Q(0))


def add(x: tuple[Q, ...], y: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(a + b for a, b in zip(x, y))


def scale(a: Q, x: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(a * b for b in x)


def sub(x: tuple[Q, ...], y: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(a - b for a, b in zip(x, y))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="std")
    args = parser.parse_args()

    observed = {name: file_sha256(ROOT / name) for name in PINS}
    require(observed == PINS, "pinned dependency hash changed")

    # Physical readout coordinates are (E,W,T,R).
    r0 = tuple(map(Q, (-1, 0, 1, 0)))
    cap_t = tuple(map(Q, (0, -1, 1, 0)))
    yrho = tuple(map(Q, (0, 1, 0, 1)))
    old = [r0, cap_t, yrho]
    separator = tuple(map(Q, (1, 1, 1, -1)))
    missing = tuple(map(Q, (0, 1, 0, 0)))

    require(all(dot(separator, c) == 0 for c in old),
            "separator does not kill old image")
    require(dot(separator, missing) == 1,
            "separator does not normalize missing direction")
    require(rank(old) == 3, "old image rank changed")
    require(rank(old + [missing]) == 4, "missing direction no longer fills")

    # The physical image is saturated: its maximal-minor gcd is one.
    row_matrix = [[c[row] for c in old] for row in range(4)]
    minors = []
    for rows in combinations(range(4), 3):
        minors.append(int(determinant([[row_matrix[i][j] for j in range(3)]
                                       for i in rows])))
    require(reduce(gcd, (abs(x) for x in minors)) == 1,
            "old image is not saturated")
    full_det = determinant([[c[row] for c in old + [missing]]
                            for row in range(4)])
    require(abs(full_det) == 1, "augmented lattice is not unimodular")

    # Exhaustively replay the pointwise Fredholm alternative for eight
    # quotient coefficients over the test alphabet {-1,0,1}.  The old part
    # of kappa_i is irrelevant in V/W; deterministic representatives keep
    # the reconstruction literal here.
    cases = 0
    dark_cases = 0
    filler_cases = 0
    for lambdas in product((-1, 0, 1), repeat=8):
        kappas = [add(old[i % len(old)], scale(Q(lam), missing))
                  for i, lam in enumerate(lambdas)]
        cases += 1
        if not any(lambdas):
            dark_cases += 1
            require(all(dot(separator, c) == 0 for c in kappas),
                    "all-dark pattern escaped separator")
            require(rank(old + kappas) == 3,
                    "all-dark pattern enlarged image")
        else:
            filler_cases += 1
            i = next(j for j, lam in enumerate(lambdas) if lam)
            recovered = scale(Q(1, lambdas[i]),
                              sub(kappas[i], old[i % len(old)]))
            require(recovered == missing, "bright column failed to recover filler")
            require(rank(old + kappas) == 4, "bright pattern failed to fill image")
    require((cases, dark_cases, filler_cases) == (6561, 1, 6560),
            "eight-column alternative census changed")

    # In the 8-dimensional (B,Eq) occurrence block, strict multiplication
    # gives equal faces and hence zero charge.  A bright twist is measured
    # exactly by its scalar lambda.
    delta = tuple(map(Q, (1, 1, -1, -1)))
    occurrence_vectors = [
        tuple(Q(1 if j == i % 4 else 0) for j in range(4))
        for i in range(8)
    ]
    strict_charges = []
    twisted_charges = []
    for i, v in enumerate(occurrence_vectors):
        strict = v + v
        chi = dot(delta, strict[:4]) - dot(delta, strict[4:])
        strict_charges.append(chi / 4)
        lam = Q((i % 3) - 1)
        twisted_b = add(v, scale(lam, delta))
        twisted = twisted_b + v
        twisted_chi = dot(delta, twisted[:4]) - dot(delta, twisted[4:])
        twisted_charges.append(twisted_chi / 4)
        require(twisted_charges[-1] == lam, "bright twist charge changed")
    require(strict_charges == [0] * 8,
            "strict multiplicative comparison acquired a charge")

    ledger = {
        "theorem": "pointwise local source-labelled singular gluing dichotomy",
        "mode": args.mode,
        "pins": observed,
        "physical_readout": {
            "coordinates": ["E", "W", "T", "R"],
            "old_columns": [list(map(int, c)) for c in old],
            "separator": list(map(int, separator)),
            "missing_direction": list(map(int, missing)),
            "old_rank": rank(old),
            "augmented_rank": rank(old + [missing]),
            "maximal_minor_gcd": reduce(gcd, (abs(x) for x in minors)),
            "augmented_determinant_abs": int(abs(full_det)),
        },
        "pointwise_eight_column_alternative": {
            "enumerated_test_patterns": cases,
            "all_dark_patterns": dark_cases,
            "filler_patterns": filler_cases,
            "statement": (
                "over a residue field, either every quotient coefficient "
                "lambda_i is zero and the separator extends, or a nonzero "
                "lambda_i reconstructs the missing direction after localization"
            ),
        },
        "strict_product": {
            "charges": [int(x) for x in strict_charges],
            "bright_twist_test_charges": [int(x) for x in twisted_charges],
            "conclusion": "strict physical Leibniz/mapping-cone product forces all lambda_i=0",
        },
        "bounded_direct_literal_attempt": {
            "official_order_six_columns": 8580,
            "fine_word_histogram": {"11111111": 6381, "11211211": 2199},
            "required_cap_word": "01211222",
            "columns_in_required_cap_word": 0,
            "site_repeating_projection_coordinates": 159,
            "site_repeating_projection_rank_two_primes": [153, 153],
            "minimal_response_P3_coordinates": 148,
            "minimal_response_P3_rank": 146,
            "canonical_operation_endpoint": "response -> response",
            "desired_operation_endpoint": "response -> AugP2 cap",
            "literal_cross_word_map_constructed": False,
            "first_missing_homogenized_face": "-u*e_Eq",
            "conclusion": (
                "literal EqSystem/principal-parts data do not construct the "
                "cross-word map; a decorated stabilization-invariant "
                "principal-parts comparison would be genuinely new input"
            ),
        },
        "status": {
            "proved": "exact local pointwise alternative and primitive integral separator",
            "not_proved": [
                "essential surjectivity of the actual physical Gamma_* C1 registry",
                "existence of the source-valid cross-word Phi_KS,r0 comparison",
                "identification of this h=3 local packet with an exhaustive slice of the 560 X5 triangle blockers",
                "strict degeneration inside the exact X5 fibre",
            ],
            "bounded_attempt_verdict": (
                "negative: the complete canonical principal-parts candidate "
                "remains response-valued and misses the cap word and operation"
            ),
        },
    }
    logical = dict(ledger)
    logical.pop("mode")
    digest = sha256(json.dumps(logical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256, "logical ledger changed")
    print("local singular gluing dichotomy: PASS")
    print("physical image rank 3 saturated; missing class primitive rank 4")
    print("pointwise alternative: all dark => separator; some bright => filler")
    print("strict multiplicative comparison => lambda_0=...=lambda_7=0")
    print("global X5 descent/cap theorem: NOT PROVED")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
