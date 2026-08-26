#!/usr/bin/env python3
"""Exact character, Hankel, and one-step module audit of the 44-dual."""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
AUDIT13 = ROOT / "unaudited-codex-carrier-minor-pure-amplitude-degree13-x5-2026-08-23" / "audit_pure_amplitude_carrier_minor_separator.py"
SHELL = ROOT / "unaudited-codex-carrier-minor-pure-square-degree17-x5-2026-08-23" / "screen_exact_separator_prolongation_shell.py"
RESULT13 = AUDIT13.parent / "results_pure_amplitude_carrier_minor_separator_exact.json"
RESULT17 = SHELL.parent / "results_exact_separator_prolongation_shell_p32003.json"
OUT = HERE / "results_pure_separator_inverse_system.json"
EXPECTED = {
    AUDIT13: "5774cdbc880cb89ecaaf8b6b7482026c79c2a6622a467ad5389ce729142b379c",
    SHELL: "d6ccb454b1a78a98776ebe0c11d8f7c8eb8b512f7b96a24ba5b849a22e88a643",
    RESULT13: "d21c0d84b42d99b102fbce4a093963c2e23eff941d3775956732701228d1d707",
    RESULT17: "a3de4d144aa39e7d352a84333f0a6bed268f187f87f4d65739983e27f9f7c440",
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


A = load(AUDIT13, "audit13")
S = load(SHELL, "shell17")
C = A.C
D9 = A.D9


def separator(mutate=False):
    record = json.loads(RESULT13.read_text())
    answer = [
        [A.parse_monomial(entry["monomial"]), entry["coefficient"]]
        for entry in record["exact_separator"]["entries"]
    ]
    require(len(answer) == 44, len(answer))
    if mutate:
        answer[0][1] += 1
    return tuple((monomial, coefficient) for monomial, coefficient in answer)


def character_circuit(values):
    seen = {}
    for left in range(len(values)):
        for right in range(left, len(values)):
            exponent_sum = tuple(sorted(values[left][0] + values[right][0]))
            product = values[left][1] * values[right][1]
            if exponent_sum in seen:
                old_left, old_right, old_product = seen[exponent_sum]
                if old_product != product:
                    return {
                        "pair_indices": [left, right, old_left, old_right],
                        "coefficient_products": [product, old_product],
                        "monomials": [
                            D9.monomial_text(values[index][0])
                            for index in (left, right, old_left, old_right)
                        ],
                        "coefficients": [
                            values[index][1]
                            for index in (left, right, old_left, old_right)
                        ],
                        "equal_exponent_sums": True,
                    }
            else:
                seen[exponent_sum] = (left, right, product)
    return None


def exact_sparse_rank(rows):
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
    return len(basis), tuple(pivots)


def determinant(matrix):
    work = [[Fraction(value) for value in row] for row in matrix]
    answer = Fraction(1)
    for column in range(len(work)):
        pivot = next((row for row in range(column, len(work))
                      if work[row][column]), None)
        require(pivot is not None, (column, work))
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


def pure_hankel(values):
    functional = dict(values)
    pure = tuple(D9.amplitude((0,) * 8))
    live = []
    for matching_index, matching in enumerate(pure):
        row = {
            quotient: coefficient
            for monomial, coefficient in values
            if (quotient := C.divides(monomial, matching)) is not None
        }
        if row:
            live.append((matching_index, matching, row))
    rank, pivots = exact_sparse_rank([row for _, _, row in live])
    require(rank == len(live) == len(pivots) == 5,
            (rank, len(live), len(pivots)))
    minor = [[row.get(pivot, 0) for pivot in pivots]
             for _, _, row in live]
    minor_determinant = determinant(minor)

    delta = D9.target_minor()
    target_contributions = []
    for matching_index, matching, _ in live:
        contribution = sum(
            coefficient * functional.get(tuple(sorted(monomial + matching)), 0)
            for monomial, coefficient in delta.items()
        )
        target_contributions.append({
            "matching_index": matching_index,
            "matching": D9.monomial_text(matching),
            "contribution_to_lambda_F0_Delta": contribution,
        })
    require(sum(item["contribution_to_lambda_F0_Delta"]
                for item in target_contributions) == 2,
            target_contributions)
    return {
        "row_count_all_pure_matchings": len(pure),
        "zero_rows": len(pure) - len(live),
        "live_rows": len(live),
        "live_matching_indices": [index for index, _, _ in live],
        "live_matching_support_sizes": [len(row) for _, _, row in live],
        "quotient_columns": len(set().union(*(set(row) for _, _, row in live))),
        "rank_over_Q": rank,
        "minor_columns": [D9.monomial_text(pivot) for pivot in pivots],
        "minor_matrix": minor,
        "minor_determinant": int(minor_determinant),
        "target_contributions": target_contributions,
    }


def parse_fraction(text):
    return Fraction(text)


def replay_shell_obstruction():
    record = json.loads(RESULT17.read_text())
    certificate = record["exact_Q_contradiction"]
    separator17, pure, _, shell, equations, _ = S.build_system()
    combined = Counter()
    combined_rhs = Fraction(0)
    sources = set()
    for entry in certificate["entries"]:
        source = entry["equation_index"]
        coefficient = parse_fraction(entry["coefficient"])
        sources.add(source)
        kind, label, row, rhs = equations[source]
        require(kind == "contraction", kind)
        for monomial, value in row.items():
            combined[monomial] += coefficient * value
            if not combined[monomial]:
                del combined[monomial]
        combined_rhs += coefficient * rhs
    require(not combined and combined_rhs == 2, (len(combined), combined_rhs))
    repair_outside = set()
    repair_inside = set()
    for source in sources:
        quotient = equations[source][1]
        for matching in pure:
            column = tuple(sorted(quotient + matching))
            if column in shell:
                repair_inside.add(column)
            else:
                repair_outside.add(column)
    require((len(shell), len(repair_inside), len(repair_outside),
             len(shell | repair_outside)) == (4559, 105, 5949, 10508),
            (len(shell), len(repair_inside), len(repair_outside),
             len(shell | repair_outside)))
    return {
        "minimal_shell_variables": len(shell),
        "certificate_rows": len(sources),
        "certificate_coefficient_set": sorted({
            entry["coefficient"] for entry in certificate["entries"]
        }),
        "combined_lhs_terms": len(combined),
        "combined_rhs": int(combined_rhs),
        "certificate_sha256": certificate["sha256"],
        "inside_variables_in_certificate": len(repair_inside),
        "mandatory_outside_repair_candidates": len(repair_outside),
        "shell_plus_all_repairs": len(shell | repair_outside),
    }


def audit(mutate=False):
    values = separator(mutate)
    circuit = character_circuit(values)
    require(circuit is not None, "unexpected character-consistent support")
    require(circuit["pair_indices"] == [1, 6, 0, 7], circuit)
    require(circuit["coefficient_products"] == [2, 4], circuit)
    hankel = pure_hankel(values)
    require(hankel["minor_determinant"] == 32, hankel["minor_determinant"])
    shell = replay_shell_obstruction()
    result = {
        "status": "PASS exact inverse-system structure of 44-term separator",
        "separator_support": len(values),
        "active_source_atoms": len(set(
            atom for monomial, _ in values for atom in monomial
        )),
        "character_test": {
            "is_single_monomial_character": False,
            "four_monomial_countercircuit": circuit,
            "reason": (
                "Equal exponent sums would force equal coefficient products "
                "for a scalar multiple of a monoid character."
            ),
        },
        "pure_matching_hankel": hankel,
        "one_step_cyclic_module_test": {
            "extends_inside_supp_lambda_times_supp_F0": False,
            **shell,
            "interpretation": (
                "No degree-17 functional supported on the one-step product "
                "shell contracts by F0 to lambda. Any k=2 continuation needs "
                "genuinely new monomials outside that shell."
            ),
        },
        "verdict": (
            "The separator is neither evaluation-like nor a rank-one pure "
            "moment functional. Its pure Hankel rank is exactly 5. There is no "
            "source-faithful all-k extension obtained by cyclically multiplying "
            "its support by F0: the first k=2 lift is already exactly obstructed."
        ),
        "scope_guard": (
            "This does not rule out a higher-rank finitely generated inverse "
            "module after adjoining the 5,949 outside repair variables, and does "
            "not decide global F0^2*Delta membership."
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
    parser.add_argument("--mutate-separator", action="store_true")
    args = parser.parse_args()
    result = audit(args.mutate_separator)
    if args.check_results:
        require(OUT.exists() and json.loads(OUT.read_text()) == result,
                "stored result drift")
    if args.write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(result["status"])
    print("character products",
          result["character_test"]["four_monomial_countercircuit"]["coefficient_products"])
    print("pure Hankel rank/minor",
          result["pure_matching_hankel"]["rank_over_Q"],
          result["pure_matching_hankel"]["minor_determinant"])
    print("shell/repairs",
          result["one_step_cyclic_module_test"]["minimal_shell_variables"],
          result["one_step_cyclic_module_test"]["mandatory_outside_repair_candidates"])
    print("logical", result["logical_sha256"])


if __name__ == "__main__":
    main()
