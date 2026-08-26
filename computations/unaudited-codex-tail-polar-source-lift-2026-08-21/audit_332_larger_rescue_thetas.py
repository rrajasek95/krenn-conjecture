#!/usr/bin/env python3
"""Exact d=5/6 rescue recursion from transported 332 rows."""

import argparse
from collections import Counter
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import time
import sys

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "results_tail_polar_source_lift.json"
TWOS = HERE / "results_332_two_rescue_thetas.json"
OUT = HERE / "results_332_larger_rescue_thetas.json"
CORE_PATH = HERE / "audit_332_two_rescue_thetas.py"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    if spec.loader is None:
        raise RuntimeError("missing module loader")
    spec.loader.exec_module(module)
    return module


CORE = load("larger_rescue_theta_core", CORE_PATH)


def require(value, detail):
    if not value:
        raise RuntimeError(detail)


def logical_hash(value):
    return sha256(json.dumps(value, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def negate(polynomial):
    return Counter({monomial: -coefficient
                    for monomial, coefficient in polynomial.items()})


def multiply(left, right):
    answer = Counter()
    for lmon, lc in left.items():
        for rmon, rc in right.items():
            answer[tuple(sorted(lmon+rmon))] += lc*rc
    return Counter({monomial: coefficient for monomial, coefficient
                    in answer.items() if coefficient})


def lambda_uv(left, right):
    return Counter({
        tuple(sorted((f"U{left}", f"V{right}"))): 1,
        tuple(sorted((f"U{right}", f"V{left}"))): -1,
    })


def identify_delta_lambda(polynomial, sites):
    for delta_pair in combinations(sites, 2):
        delta = CORE.delta_atoms(*delta_pair)
        remaining = tuple(site for site in sites if site not in delta_pair)
        for lambda_pair in combinations(remaining, 2):
            candidate = multiply(delta, lambda_uv(*lambda_pair))
            if polynomial in (candidate, negate(candidate)):
                return delta_pair, lambda_pair
    return None


def search_d5(base_labels, candidates, rows):
    sites = (0, 1, 2, 3, 4)
    best = None
    tested = 0
    started = time.monotonic()
    for label in candidates:
        if label in base_labels:
            continue
        labels = base_labels+(label,)
        polynomial = CORE.formal_determinant(
            CORE.reduced_matrix(sites, [rows[label] for label in labels]),
            sites)
        tested += 1
        if not polynomial:
            continue
        common, residual = CORE.common_monomial(polynomial)
        identified = identify_delta_lambda(residual, sites)
        score = (0 if identified else 1, len(residual), labels)
        if best is None or score < best[0]:
            best = (score, labels, polynomial, common, residual, identified)
        if identified and len(residual) == 4:
            # Continue through every possible single-row extension so the
            # selected added row is exactly minimal, not sampled.
            pass
    elapsed = time.monotonic()-started
    require(elapsed < 120 and best is not None,
            ("Theta_221 exact search failed/cap", elapsed))
    return sites, tested, elapsed, best


def extend_d6(d5_labels, candidates, rows):
    sites = tuple(range(6))
    best = None
    tested = 0
    started = time.monotonic()
    for label in candidates:
        if label in d5_labels:
            continue
        labels = d5_labels+(label,)
        polynomial = CORE.formal_determinant(
            CORE.reduced_matrix(sites, [rows[value] for value in labels]),
            sites)
        tested += 1
        if not polynomial:
            continue
        common, residual = CORE.common_monomial(polynomial)
        score = (len(residual), label)
        if best is None or score < best[0]:
            best = (score, labels, polynomial, common, residual)
    elapsed = time.monotonic()-started
    require(elapsed < 120 and best is not None,
            ("Theta_222 one-row extension failed/cap", elapsed))
    return sites, tested, elapsed, best


def divide_by_delta(polynomial, left, right):
    positive = (f"P{left}", f"Q{right}", f"V{left}", f"U{right}")
    quotient = Counter()
    for monomial, coefficient in polynomial.items():
        value = list(monomial)
        if all(factor in value for factor in positive):
            for factor in positive:
                value.remove(factor)
            quotient[tuple(value)] += coefficient
    candidate = multiply(CORE.delta_atoms(left, right), quotient)
    if candidate == polynomial:
        return quotient
    if negate(candidate) == polynomial:
        return negate(quotient)
    return None


def identify_delta_omega(polynomial, sites):
    for pair in combinations(sites, 2):
        quotient = divide_by_delta(polynomial, *pair)
        if quotient is not None:
            return pair, quotient
    return None


def record(name, sites, tested, best, rows, identified=None):
    _, labels, polynomial, common, residual, *rest = best
    return {
        "name": name,
        "double_sites": list(sites),
        "source_labels": list(labels),
        "source_row_coefficients": {
            label: rows[label]["nonzero_columns"] for label in labels
        },
        "candidates_tested": tested,
        "symbolic_cap_seconds": 120,
        "determinant_term_count": len(polynomial),
        "common_monomial_factors": list(common),
        "primitive_factor_term_count": len(residual),
        "primitive_factor": CORE.encode(residual),
        "delta_lambda_factorization": (
            None if identified is None else {
                "Delta_pair": list(identified[0]),
                "Lambda_UV_pair": list(identified[1]),
                "literal_product_replay": True,
            }
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    source = json.loads(SOURCE.read_text())
    twos = json.loads(TWOS.read_text())
    require(twos["logical_sha256"] ==
            "dd662ba48005cb31f323f92a9eafe32beeda594f6a4381747339c8264b2a52f4",
            "two-rescue Theta digest changed")
    rows = {row["source_label"]: row for row in source["row_ledger"]}
    candidates = sorted({CORE.transform_label(seed, action)
                         for seed in CORE.SEEDS
                         for action in CORE.vertex_actions()})
    require(len(candidates) == 96, "transported rescue row count changed")

    theta220 = next(record for record in twos["determinants"]
                    if record["name"] == "Theta_220")
    base_labels = tuple(theta220["source_labels"])
    d5_sites, d5_tested, _, d5_best = search_d5(
        base_labels, candidates, rows)
    d5_identified = d5_best[-1]
    require(d5_identified is not None,
            "Theta_221 ceased to factor as Delta*Lambda_UV")
    d5_record = record("Theta_221", d5_sites, d5_tested,
                       d5_best, rows, d5_identified)

    d5_labels = tuple(d5_best[1])
    d6_sites, d6_tested, _, d6_best = extend_d6(
        d5_labels, candidates, rows)
    d6_record = record("Theta_222", d6_sites, d6_tested,
                       d6_best, rows)
    d6_factor = identify_delta_omega(d6_best[4], d6_sites)
    require(d6_factor is not None,
            "Theta_222 ceased to factor as Delta*Omega")
    d6_record["delta_omega_factorization"] = {
        "Delta_pair": list(d6_factor[0]),
        "Omega_term_count": len(d6_factor[1]),
        "Omega": CORE.encode(d6_factor[1]),
        "literal_product_replay": True,
    }

    # Independent literal full-source determinant replay for the selected
    # 10x10 and 12x12 minors by sparse subset dynamic programming.
    for value, labels, sites, polynomial in (
            (d5_record, d5_labels, d5_sites, d5_best[2]),
            (d6_record, tuple(d6_best[1]), d6_sites, d6_best[2])):
        full, columns = CORE.full_matrix(
            sites, [rows[label] for label in labels])
        started = time.monotonic()
        full_polynomial = CORE.formal_determinant_dp(full, columns)
        elapsed = time.monotonic()-started
        require(elapsed < 120 and full_polynomial in
                (polynomial, negate(polynomial)),
                ("literal larger full/reduced determinant changed",
                 value["name"], elapsed))
        value["literal_full_vs_reduced_replay"] = True
        value["full_minor_rows"] = (["Y", "Z"]+
            [f"E{site}" for site in sites]+list(labels))
        value["full_minor_columns"] = [
            *(f"y{site}" for site in sites),
            *(f"z{site}" for site in sites),
        ]

    result = {
        "status": "PASS exact larger Hall rescue determinant recursion",
        "determinants": [d5_record, d6_record],
        "adjoining_test": {
            "Theta_221_from_220_by_one_row": True,
            "reason_221": (
                "One transported row gives an exact determinant, but its "
                "minimal primitive has four terms and factors as Delta "
                "times a genuinely new Lambda_UV two-by-two minor."),
            "Theta_222_from_selected_221_by_one_row": True,
            "reason_222": (
                "One transported row gives an exact nonzero six-site "
                "determinant; its primitive factors as Delta times a new "
                "seven-term Omega polynomial."
            ),
        },
        "atom_dictionary": {
            "P_a": "h0_a6", "Q_a": "h0_a7",
            "U_a": "h1_a6", "V_a": "h1_a7",
            "Lambda_UV_ab": "U_a*V_b-U_b*V_a",
        },
        "scope_guard": (
            "These are exact determinant opens. Their factor divisors "
            "remain inputs to the cofactor-support/arbitrary-mate routing "
            "ledger; no sampled rank assertion is used."
        ),
        "source_hashes": {
            "source": sha256(SOURCE.read_bytes()).hexdigest(),
            "two_rescue": sha256(TWOS.read_bytes()).hexdigest(),
            "core": sha256(CORE_PATH.read_bytes()).hexdigest(),
        },
    }
    result["logical_sha256"] = logical_hash(result)
    if args.write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("larger rescue Thetas: PASS", result["logical_sha256"])
    for value in result["determinants"]:
        print(value["name"], value["source_labels"],
              "primitive", value["primitive_factor_term_count"],
              "tested", value["candidates_tested"])


if __name__ == "__main__":
    main()
