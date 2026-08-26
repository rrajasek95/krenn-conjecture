#!/usr/bin/env python3
"""Exact contraction/Hankel transfer audit for lambda_1 and lambda_2."""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import permutations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
A1_PATH = ROOT / "unaudited-codex-carrier-minor-pure-amplitude-degree13-x5-2026-08-23" / "audit_pure_amplitude_carrier_minor_separator.py"
R1_PATH = A1_PATH.parent / "results_pure_amplitude_carrier_minor_separator_exact.json"
A2_PATH = ROOT / "unaudited-codex-carrier-minor-pure-square-degree17-rust-2026-08-23" / "audit_pure_square_separator_exact.py"
R2_PATH = A2_PATH.parent / "results_pure_square_separator_exact.json"
RUST_PATH = A2_PATH.parent / "results_pure_square_cegar_rust_p32003.json"
OUT = HERE / "results_pure_separator_transfer.json"
EXPECTED = {
    A1_PATH: "5774cdbc880cb89ecaaf8b6b7482026c79c2a6622a467ad5389ce729142b379c",
    R1_PATH: "d21c0d84b42d99b102fbce4a093963c2e23eff941d3775956732701228d1d707",
    A2_PATH: "ec2eba8b16c76790d6b65788ab3f5530af964d8ffc31146b61a984a0c137c6ae",
    R2_PATH: "1a508cc4cbfa2eae130a7a986a4a0632402cc76de70d1a8aa97e5db4b56c4d56",
    RUST_PATH: "9354f742bec952d3ed03da3e2f80291bd03224d1181f2d03e1906e50bf41a510",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(path, name):
    require(sha256(path.read_bytes()).hexdigest() == EXPECTED[path],
            f"source drift: {path}")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, path)
    spec.loader.exec_module(module)
    return module


A1 = load(A1_PATH, "audit_lambda1")
A2 = load(A2_PATH, "audit_lambda2")
C = A1.C
D9 = A1.D9


def functionals(mutate=False):
    record1 = json.loads(R1_PATH.read_text())
    record2 = json.loads(R2_PATH.read_text())
    lambda1 = {
        A1.parse_monomial(entry["monomial"]): entry["coefficient"]
        for entry in record1["exact_separator"]["entries"]
    }
    lambda2 = {
        A1.parse_monomial(entry["monomial"]): entry["coefficient"]
        for entry in record2["exact_separator"]["entries"]
    }
    require((len(lambda1), len(lambda2)) == (44, 102),
            (len(lambda1), len(lambda2)))
    if mutate:
        lambda2[min(lambda2)] += 1
    return lambda1, lambda2


def sparse_basis(rows):
    basis = {}
    pivots = []
    for raw in rows:
        row = {column: Fraction(value) for column, value in raw.items() if value}
        while row:
            pivot = min(row)
            coefficient = row[pivot]
            if pivot not in basis:
                basis[pivot] = {
                    column: value / coefficient for column, value in row.items()
                }
                pivots.append(pivot)
                break
            for column, value in basis[pivot].items():
                updated = row.get(column, Fraction(0)) - coefficient * value
                if updated:
                    row[column] = updated
                else:
                    row.pop(column, None)
    return basis, tuple(pivots)


def reduce_row(raw, basis):
    row = {column: Fraction(value) for column, value in raw.items() if value}
    while row and min(row) in basis:
        pivot = min(row)
        coefficient = row[pivot]
        for column, value in basis[pivot].items():
            updated = row.get(column, Fraction(0)) - coefficient * value
            if updated:
                row[column] = updated
            else:
                row.pop(column, None)
    return row


def add_to_basis(raw, basis):
    row = reduce_row(raw, basis)
    if not row:
        return False
    pivot = min(row)
    coefficient = row[pivot]
    basis[pivot] = {column: value / coefficient for column, value in row.items()}
    return True


def determinant(matrix):
    work = [[Fraction(value) for value in row] for row in matrix]
    answer = Fraction(1)
    for column in range(len(work)):
        pivot = next(row for row in range(column, len(work))
                     if work[row][column])
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            answer = -answer
        value = work[column][column]
        answer *= value
        for later in range(column, len(work)):
            work[column][later] /= value
        for row in range(column + 1, len(work)):
            value = work[row][column]
            for later in range(column, len(work)):
                work[row][later] -= value * work[column][later]
    return answer


def pure_hankel(functional):
    pure = tuple(D9.amplitude((0,) * 8))
    live = []
    for matching_index, matching in enumerate(pure):
        row = {
            quotient: coefficient
            for monomial, coefficient in functional.items()
            if (quotient := C.divides(monomial, matching)) is not None
        }
        if row:
            live.append((matching_index, matching, row))
    basis, pivots = sparse_basis([row for _, _, row in live])
    require(len(basis) == len(live), (len(basis), len(live)))
    minor = [[row.get(pivot, 0) for pivot in pivots]
             for _, _, row in live]
    return {
        "live_rows": len(live),
        "zero_rows": len(pure) - len(live),
        "live_matching_indices": [index for index, _, _ in live],
        "live_matchings": [D9.monomial_text(matching) for _, matching, _ in live],
        "live_support_sizes": [len(row) for _, _, row in live],
        "quotient_columns": len(set().union(*(set(row) for _, _, row in live))),
        "rank": len(basis),
        "minor_columns": [D9.monomial_text(pivot) for pivot in pivots],
        "minor_matrix": minor,
        "minor_determinant": int(determinant(minor)),
        "rows": [row for _, _, row in live],
    }


def contract_sum(hankel):
    total = Counter()
    for row in hankel["rows"]:
        total.update(row)
    return {monomial: coefficient for monomial, coefficient in total.items()
            if coefficient}


def permute_monomial(monomial, site_permutation):
    return tuple(sorted(
        D9.cell(site_permutation[u], site_permutation[v], a, b)
        for u, v, a, b in monomial
    ))


def stabilizer_orbit(functional):
    orbit = []
    for first in permutations(range(3)):
        for second in permutations(range(3, 6)):
            site_permutation = tuple(first) + tuple(second) + (6, 7)
            orbit.append({
                permute_monomial(monomial, site_permutation): coefficient
                for monomial, coefficient in functional.items()
            })
    distinct = {tuple(sorted(row.items())) for row in orbit}
    basis, _ = sparse_basis(orbit)
    require(len(orbit) == len(distinct) == len(basis) == 36,
            (len(orbit), len(distinct), len(basis)))
    return orbit, basis


def audit(mutate=False):
    lambda1, lambda2 = functionals(mutate)
    hankel1 = pure_hankel(lambda1)
    hankel2 = pure_hankel(lambda2)
    require((hankel1["rank"], hankel1["minor_determinant"])
            == (5, 32), hankel1)
    require((hankel2["rank"], hankel2["minor_determinant"])
            == (6, -64), hankel2)

    contraction2 = contract_sum(hankel2)
    common = set(contraction2) & set(lambda1)
    private_contraction = set(contraction2) - set(lambda1)
    private_lambda1 = set(lambda1) - set(contraction2)
    scalar_candidate = 14  # forced by target pairings 28/2.
    scalar_residual = Counter(contraction2)
    scalar_residual.subtract({
        monomial: scalar_candidate * coefficient
        for monomial, coefficient in lambda1.items()
    })
    scalar_residual = {monomial: coefficient
                       for monomial, coefficient in scalar_residual.items()
                       if coefficient}
    require((len(contraction2), len(common), len(private_contraction),
             len(private_lambda1), len(scalar_residual))
            == (108, 7, 101, 37, 145),
            (len(contraction2), len(common), len(private_contraction),
             len(private_lambda1), len(scalar_residual)))

    orbit, orbit_basis = stabilizer_orbit(lambda1)
    independent_remainders = [
        len(reduce_row(row, orbit_basis)) for row in hankel2["rows"]
    ]
    require(independent_remainders == [121, 64, 45, 56, 6, 73],
            independent_remainders)
    enlarged_basis = {pivot: dict(row) for pivot, row in orbit_basis.items()}
    increments = [add_to_basis(row, enlarged_basis) for row in hankel2["rows"]]
    require(increments == [True] * 6 and len(enlarged_basis) == 42,
            (increments, len(enlarged_basis)))

    # Recheck the two target pairings that force the scalar candidate 14.
    require(json.loads(R1_PATH.read_text())["exact_separator"]["target_pairing"] == 2,
            "lambda1 pairing drift")
    require(json.loads(R2_PATH.read_text())["exact_separator"]["target_pairing"] == 28,
            "lambda2 pairing drift")

    for hankel in (hankel1, hankel2):
        del hankel["rows"]
    result = {
        "status": "PASS exact pure-transfer obstruction between lambda_1 and lambda_2",
        "levels": {
            "lambda_1": {"degree": 13, "support": len(lambda1),
                         "target": "F0*Delta", "target_pairing": 2},
            "lambda_2": {"degree": 17, "support": len(lambda2),
                         "target": "F0^2*Delta", "target_pairing": 28},
        },
        "pure_hankel": {"lambda_1": hankel1, "lambda_2": hankel2},
        "full_pure_contraction": {
            "support": len(contraction2),
            "intersection_with_lambda_1": len(common),
            "private_to_contraction": len(private_contraction),
            "private_to_lambda_1": len(private_lambda1),
            "scalar_candidate_forced_by_target_pairings": scalar_candidate,
            "nonzero_terms_after_subtracting_14_lambda_1": len(scalar_residual),
            "is_scalar_multiple_of_lambda_1": False,
        },
        "fine_grade_stabilizer_transfer": {
            "group": "S3({0,1,2}) x S3({3,4,5}), fixing 6,7",
            "orbit_size": len(orbit),
            "orbit_span_rank": len(orbit_basis),
            "lambda_2_channel_remainder_sizes": independent_remainders,
            "all_six_channels_independent_mod_orbit_span": all(increments),
            "rank_after_adjoining_six_channels": len(enlarged_basis),
        },
        "verdict": (
            "There is no scalar/eigenfunctional recurrence F0.lambda_2 = c lambda_1, "
            "and no closure inside the full 36-dimensional fine-grade stabilizer "
            "orbit module of lambda_1. The pure Hankel rank grows 5 to 6, and "
            "the six lambda_2 contraction channels add six independent directions."
        ),
        "scope_guard": (
            "Two levels do not rule out a larger transfer module chosen with new "
            "generators. An all-k theorem would need at least those six new degree-13 "
            "directions and a proved closure rule at the next level; no k=3 solve "
            "is performed here."
        ),
        "source_sha256": {str(path.relative_to(ROOT.parent)): digest
                          for path, digest in EXPECTED.items()},
    }
    result["logical_sha256"] = sha256(json.dumps(
        result, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    parser.add_argument("--mutate-lambda2", action="store_true")
    args = parser.parse_args()
    result = audit(args.mutate_lambda2)
    if args.check_results:
        require(OUT.exists() and json.loads(OUT.read_text()) == result,
                "stored result drift")
    if args.write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(result["status"])
    print("Hankel ranks/determinants",
          result["pure_hankel"]["lambda_1"]["rank"],
          result["pure_hankel"]["lambda_1"]["minor_determinant"],
          result["pure_hankel"]["lambda_2"]["rank"],
          result["pure_hankel"]["lambda_2"]["minor_determinant"])
    print("contraction/common/private",
          result["full_pure_contraction"]["support"],
          result["full_pure_contraction"]["intersection_with_lambda_1"],
          result["full_pure_contraction"]["private_to_contraction"])
    print("orbit/enlarged rank",
          result["fine_grade_stabilizer_transfer"]["orbit_span_rank"],
          result["fine_grade_stabilizer_transfer"]["rank_after_adjoining_six_channels"])
    print("logical", result["logical_sha256"])


if __name__ == "__main__":
    main()
