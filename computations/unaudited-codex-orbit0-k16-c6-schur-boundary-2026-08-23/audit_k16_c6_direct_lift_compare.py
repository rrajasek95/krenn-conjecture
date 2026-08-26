#!/usr/bin/env python3
"""Lift the exact 18-column C6 certificate and compare frozen exterior pages."""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import argparse
import importlib.util
import json
from math import lcm
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROVIDER = HERE / "audit_k16_c6_schur_boundary.py"
SEED = HERE / "results_k16_c6_schur_boundary.json"
SCHUR = HERE / "boundary_schur_interface.json"
DIRECT = HERE / "results_k16_c6_signed_projection.json"
CYCLE = ROOT / "computations/unaudited-codex-orbit0-k16-coloured-necklace-referee-2026-08-23"
CYCLE_RESULT = CYCLE / "results_c6_boundary_schur_lift.json"
CYCLE_LEDGER = CYCLE / "c6_boundary_schur_lift_coefficients.tsv"
C7_RESULT = CYCLE / "results_unpivotable_c7_boundary.json"
C7_PAIR = CYCLE / "results_c7_pair_schur_lift.json"
C7_LEDGER = CYCLE / "c7_pair_schur_lift_coefficients.tsv"
C7_CERTIFIED = CYCLE / "results_c7_certified_reduction.json"
C7_CERTIFIED_LEDGER = CYCLE / "c7_certified_reduction_coefficients.tsv"
OUT = HERE / "results_k16_c6_direct_lift_compare.json"
DIRECT_RESIDUAL = HERE / "k16_c6_direct_lift_residual.tsv"
DIRECT_CERTIFIED_RESIDUAL = HERE / "k16_c6_direct_certified_residual.tsv"

def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)

def load_provider():
    spec = importlib.util.spec_from_file_location("k16_c6_compare_provider", PROVIDER)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, PROVIDER)
    spec.loader.exec_module(module)
    return module

def retain(counter):
    return Counter({key: value for key, value in counter.items() if value})

def add_scaled(left, right, scale):
    for key, value in right.items():
        updated = left.get(key, 0) + scale * value
        if updated: left[key] = updated
        else: left.pop(key, None)

def parse_column(key):
    word, multiplier = key.split(":", 1)
    return tuple(map(int, word)), bytes.fromhex(multiplier)

def residual_text(residual):
    return "\n".join(f"{row.hex()}\t{coefficient}"
                     for row, coefficient in sorted(residual.items())) + "\n"

def profile(provider, residual):
    answer = Counter()
    for row in residual:
        answer[(provider.D24.row_k_degree(row), len(provider.graph_data(row)[0]))] += 1
    return {f"{degree},{cycles}": count for (degree, cycles), count in sorted(answer.items())}

def build(mutate=False):
    provider = load_provider()
    seed = json.loads(SEED.read_text())
    schur = json.loads(SCHUR.read_text())
    direct = json.loads(DIRECT.read_text())
    cycle_result = json.loads(CYCLE_RESULT.read_text())
    c7_result = json.loads(C7_RESULT.read_text())
    c7_pair = json.loads(C7_PAIR.read_text())
    c7_certified = json.loads(C7_CERTIFIED.read_text())
    require(direct["logical_sha256"] == "e1361165b89d59fb5426e79a26061baf49a28eee88f2dc18ec738f15e0ab981a", direct["logical_sha256"])
    require(cycle_result["logical_sha256"] == "d53aad470b3db200ee0c9311548e237b7a748bfd9e5f25dd501ac902a75b73ff", cycle_result["logical_sha256"])
    blockers = [provider.HQ.canonical_row(bytes.fromhex(record["row"]))
                for record in seed["blockers"]]
    target = Counter({row: Fraction(*record["target_mass"])
                      for row, record in zip(blockers, seed["blockers"], strict=True)})

    direct_residual = Counter(target)
    for record in direct["target_solution"]:
        coefficient = Fraction(*record["coefficient"])
        column = schur["columns"][record["column_index"]]
        require(column["key"] == record["column"], record)
        add_scaled(direct_residual,
                   {bytes.fromhex(row): Fraction(value) for row, value in column["entries"]},
                   -coefficient)
    direct_residual = retain(direct_residual)
    require(all(row not in direct_residual for row in blockers), "direct lift retained C6 blocker")

    column_cache = {}
    def literal_projection(key):
        found = column_cache.get(key)
        if found is not None:
            return found
        vector = Counter()
        for row in provider.D24.degree24_column_rows(parse_column(key)):
            if provider.D24.row_k_degree(row) <= 16:
                vector[provider.HQ.canonical_row(row)] += 1
        vector = retain(vector)
        column_cache[key] = vector
        return vector

    cycle_residual = Counter(target)
    ledger_lines = CYCLE_LEDGER.read_text().splitlines()
    for line in ledger_lines[1:]:
        kind, coefficient_text, key = line.split("\t")
        require(kind in ("pair-left", "pair-right", "c>=7-pivot"), kind)
        add_scaled(cycle_residual, literal_projection(key), -Fraction(coefficient_text))
    cycle_residual = retain(cycle_residual)
    cycle_payload = residual_text(cycle_residual)
    require(len(cycle_residual) == 3713, len(cycle_residual))
    require(sha256(cycle_payload.encode()).hexdigest() == cycle_result["remaining_residual_sha256"],
            "Cycle residual literal replay mismatch")

    if mutate:
        row = min(direct_residual)
        direct_residual[row] += 1

    intersection = set(direct_residual) & set(cycle_residual)
    equal = {row for row in intersection if direct_residual[row] == cycle_residual[row]}
    opposite = {row for row in intersection if direct_residual[row] == -cycle_residual[row]}
    difference = Counter(cycle_residual)
    add_scaled(difference, direct_residual, -1)
    difference = retain(difference)
    proportional = False
    if intersection:
        first = min(intersection)
        ratio = cycle_residual[first] / direct_residual[first]
        proportional = (set(direct_residual) == set(cycle_residual)
                        and all(cycle_residual[row] == ratio * direct_residual[row]
                                for row in direct_residual))

    c7_seed = {bytes.fromhex(record["row"]) for record in c7_result["failure_profiles"]}
    c7_frontier = {bytes.fromhex(record["row"]) for record in c7_pair["frontier_rows"]}
    c7_residual = Counter({bytes.fromhex(record["row"]): Fraction(record["coefficient"])
                           for record in cycle_result["uncertified_high_rows"]})
    for line in C7_LEDGER.read_text().splitlines()[1:]:
        kind, coefficient_text, key = line.split("\t")
        require(kind in ("pair-left", "pair-right", "c>7-pivot"), kind)
        add_scaled(c7_residual, literal_projection(key), -Fraction(coefficient_text))
    c7_residual = retain(c7_residual)
    c7_payload = residual_text(c7_residual)
    require(len(c7_residual) == 308, len(c7_residual))
    require(sha256(c7_payload.encode()).hexdigest() == c7_pair["remaining_residual_sha256"],
            "C7 residual literal replay mismatch")
    certified_residual = Counter({bytes.fromhex(record["row"]): Fraction(record["coefficient"])
                                  for record in cycle_result["uncertified_high_rows"]})
    for line in C7_CERTIFIED_LEDGER.read_text().splitlines()[1:]:
        kind, coefficient_text, key = line.split("\t")
        require(kind in ("pair-left", "pair-right", "c>7-pivot"), kind)
        add_scaled(certified_residual, literal_projection(key), -Fraction(coefficient_text))
    certified_residual = retain(certified_residual)
    certified_payload = residual_text(certified_residual)
    require(len(certified_residual) == 884, len(certified_residual))
    require(sha256(certified_payload.encode()).hexdigest() == c7_certified["remaining_residual_sha256"],
            "certified C7 reduction literal replay mismatch")
    direct_certified = Counter(direct_residual)
    direct_pivot_columns = Counter()
    blocked_high = set()
    direct_pivot_uses = 0
    while True:
        candidates = []
        for row, coefficient in direct_certified.items():
            cycles = len(provider.graph_data(row)[0])
            if cycles >= 7 and row not in blocked_high:
                candidates.append((cycles, row, coefficient))
        if not candidates:
            break
        cycles, row, coefficient = max(candidates, key=lambda item: (item[0], item[1]))
        witness = provider.eligible_pivot(row)
        if witness is None:
            blocked_high.add(row)
            continue
        word, selected = witness
        multiplier = list(row)
        for cell in selected:
            multiplier.remove(cell)
        key = provider.HQ.column_key((word, bytes(sorted(multiplier))))
        vector = literal_projection(key)
        parent_coefficient = vector.get(row, 0)
        require(parent_coefficient > 0, (row.hex(), key, parent_coefficient))
        require(all(len(provider.graph_data(child)[0]) < cycles
                    for child, value in vector.items() if child != row and value),
                ("nontriangular direct pivot", row.hex(), cycles))
        factor = coefficient / parent_coefficient
        add_scaled(direct_certified, vector, -factor)
        direct_pivot_columns[key] += factor
        direct_pivot_uses += 1
        require(len(direct_certified) <= 100_000, len(direct_certified))
    direct_certified = retain(direct_certified)
    direct_certified_payload = residual_text(direct_certified)
    DIRECT_CERTIFIED_RESIDUAL.write_text(direct_certified_payload)

    certified_intersection = set(direct_certified) & set(certified_residual)
    affine_candidates = Counter()
    for row in certified_intersection:
        left, right = direct_certified[row], certified_residual[row]
        if left != right:
            affine_candidates[-right / (left - right)] += 1
    best_lambda = max(affine_candidates, key=lambda value: (affine_candidates[value],
                                                             -abs(value.numerator),
                                                             -value.denominator), default=Fraction(0))
    affine_residual = Counter()
    add_scaled(affine_residual, direct_certified, best_lambda)
    add_scaled(affine_residual, certified_residual, 1 - best_lambda)
    affine_residual = retain(affine_residual)
    direct_payload = residual_text(direct_residual)
    require(sha256(direct_payload.encode()).hexdigest() ==
            "561ded7e50164d42ab7baf78395e638664322ac6546461b42a24bd46be4e699d",
            "direct residual hostile mutation or drift")
    DIRECT_RESIDUAL.write_text(direct_payload)
    payload = {
        "schema": "orbit0-k16-c6-direct-lift-comparison-v1",
        "status": "EXACT_BOUNDED_EXTERIOR_COMPARISON",
        "direct_18_column_lift": {
            "support": len(direct_residual),
            "profile_K_degree_cycle_count": profile(provider, direct_residual),
            "coefficient_l1": str(sum(abs(value) for value in direct_residual.values())),
            "max_numerator": max(abs(value.numerator) for value in direct_residual.values()),
            "lcm_denominator": lcm(*(value.denominator for value in direct_residual.values())),
            "residual_sha256": sha256(direct_payload.encode()).hexdigest(),
        },
        "cycle_26_pair_lift": {
            "support": len(cycle_residual),
            "profile_K_degree_cycle_count": profile(provider, cycle_residual),
            "residual_sha256": sha256(cycle_payload.encode()).hexdigest(),
            "literal_columns_replayed": len(column_cache),
        },
        "comparison": {
            "support_intersection": len(intersection),
            "equal_coefficients_on_intersection": len(equal),
            "opposite_coefficients_on_intersection": len(opposite),
            "support_union": len(set(direct_residual) | set(cycle_residual)),
            "difference_support": len(difference),
            "residual_vectors_proportional": proportional,
            "direct_support_strictly_smaller": len(direct_residual) < len(cycle_residual),
        },
        "later_c7_pages": {
            "eight_seed_rows_in_direct_support": len(c7_seed & set(direct_residual)),
            "eight_seed_rows_in_cycle_support": len(c7_seed & set(cycle_residual)),
            "twenty_four_frontier_rows_in_direct_support": len(c7_frontier & set(direct_residual)),
            "twenty_four_frontier_rows_in_cycle_support": len(c7_frontier & set(cycle_residual)),
            "c7_pair_full_residual_support": len(c7_residual),
            "direct_overlap_with_c7_pair_full_residual": len(set(direct_residual) & set(c7_residual)),
            "cycle_overlap_with_c7_pair_full_residual": len(set(cycle_residual) & set(c7_residual)),
            "c7_pair_full_residual_sha256": sha256(c7_payload.encode()).hexdigest(),
            "certified_c_le_6_residual_support": len(certified_residual),
            "certified_c_le_6_residual_sha256": sha256(certified_payload.encode()).hexdigest(),
            "direct_overlap_with_certified_c_le_6_residual": len(set(direct_residual) & set(certified_residual)),
            "cycle_certified_path_smaller_than_direct": len(certified_residual) < len(direct_residual),
            "support_advantage_over_direct": len(direct_residual) - len(certified_residual),
            "direct_coefficients_on_eight_seed": {row.hex(): str(direct_residual[row])
                                                   for row in sorted(c7_seed & set(direct_residual))},
            "direct_coefficients_on_twenty_four_frontier": {row.hex(): str(direct_residual[row])
                                                              for row in sorted(c7_frontier & set(direct_residual))},
        },
        "direct_general_cycle_reduction": {
            "certified_pivot_uses": direct_pivot_uses,
            "distinct_pivot_columns": sum(bool(value) for value in direct_pivot_columns.values()),
            "blocked_c_ge_7_rows": len(blocked_high),
            "remaining_support": len(direct_certified),
            "remaining_profile_K_degree_cycle_count": profile(provider, direct_certified),
            "residual_sha256": sha256(direct_certified_payload.encode()).hexdigest(),
            "comparison_with_cycle_884": {
                "support_intersection": len(certified_intersection),
                "support_union": len(set(direct_certified) | set(certified_residual)),
                "equal_coefficients": sum(direct_certified[row] == certified_residual[row]
                                          for row in certified_intersection),
                "opposite_coefficients": sum(direct_certified[row] == -certified_residual[row]
                                             for row in certified_intersection),
                "direct_smaller_than_cycle_884": len(direct_certified) < len(certified_residual),
            },
            "best_affine_combination": {
                "lambda_on_direct": [best_lambda.numerator, best_lambda.denominator],
                "one_minus_lambda_on_cycle": [(1-best_lambda).numerator,
                                                (1-best_lambda).denominator],
                "shared_rows_cancelled": affine_candidates.get(best_lambda, 0),
                "resulting_support": len(affine_residual),
                "improves_on_both": len(affine_residual) < min(len(direct_certified),
                                                               len(certified_residual)),
            },
        },
        "scope_guard": "Comparison of two frozen finite lifts only; no new incidence closure or rank inference.",
        "pinned": {"direct_projection_logical": direct["logical_sha256"],
                   "cycle_lift_logical": cycle_result["logical_sha256"],
                   "c7_boundary_logical": c7_result["logical_sha256"],
                   "c7_pair_logical": c7_pair["logical_sha256"],
                   "c7_certified_logical": c7_certified["logical_sha256"]},
    }
    payload["logical_sha256"] = sha256(json.dumps(payload, sort_keys=True,
                                                   separators=(",", ":")).encode()).hexdigest()
    return payload

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutate", action="store_true")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    payload = build(args.mutate)
    if not args.verify:
        OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": payload["status"],
                      "direct_support": payload["direct_18_column_lift"]["support"],
                      "cycle_support": payload["cycle_26_pair_lift"]["support"],
                      "comparison": payload["comparison"],
                      "later_c7_pages": payload["later_c7_pages"],
                      "direct_general_cycle_reduction": payload["direct_general_cycle_reduction"],
                      "logical_sha256": payload["logical_sha256"]}, sort_keys=True))

if __name__ == "__main__":
    main()
