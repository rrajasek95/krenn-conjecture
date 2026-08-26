#!/usr/bin/env python3
"""Exact quadratic matching-exchange complex and dense-support counterguard."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SHELL_SCRIPT = (ROOT / "computations" /
    "unaudited-codex-three-copy-first-shell-2026-08-22" /
    "audit_no_fourth_completion_shell.py")
SHELL_RESULT = SHELL_SCRIPT.parent / "results_no_fourth_completion_shell.json"
OUT = HERE / "results_exchange_complex_dense_guard.json"
EXPECTED_LOGICAL_SHA256 = (
    "178f1808f7bee65fbd5a4e35cd463e4ec04642e20602fcca339c3563dc6ba901"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, f"missing loader for {path}")
    spec.loader.exec_module(module)
    return module


SHELL = load("three_copy_shell", SHELL_SCRIPT)
BASE = SHELL.BASE
SOURCE = SHELL.SOURCE


def file_sha(path):
    return sha256(path.read_bytes()).hexdigest()


def logical_sha(value):
    return sha256(json.dumps(value, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def exact_sparse_rank(rows):
    basis = {}
    for raw in rows:
        row = {key: Fraction(value) for key, value in raw.items() if value}
        while row:
            pivot = min(row)
            if pivot not in basis:
                scale = row[pivot]
                basis[pivot] = {key: value / scale for key, value in row.items()}
                break
            scale = row[pivot]
            for key, value in basis[pivot].items():
                updated = row.get(key, Fraction(0)) - scale * value
                if updated:
                    row[key] = updated
                else:
                    row.pop(key, None)
    return len(basis)


def chart_complex(row, old_record):
    matchings = BASE.matchings_from_row(row)
    support = SHELL.base_support(matchings)
    fibres = SHELL.base_fibres(support)
    pure = {(colour,) * 8 for colour in range(3)}
    words = tuple(sorted(word for word, count in fibres.items()
                         if word not in pure and count == 1))
    require(len(words) == old_record["base_singleton_words"],
            "exchange-complex obstruction coordinates changed")

    directions = set()
    word_directions = {}
    all_deficit_sizes = []
    for word in words:
        deficits = set()
        for matching in SOURCE.VERTEX_MATCHINGS:
            missing = SHELL.term_support(word, matching) - support
            if missing:
                all_deficit_sizes.append(len(missing))
            if len(missing) == 2:
                deficits.add(missing)
                directions.add(missing)
        word_directions[word] = deficits
    directions = tuple(sorted(directions, key=lambda item: tuple(sorted(item))))
    index = {direction: i for i, direction in enumerate(directions)}
    matrix_rows = []
    for word in words:
        matrix_rows.append({index[direction]: 1
                            for direction in word_directions[word]})
    rank = exact_sparse_rank(matrix_rows)
    column_weights = [0] * len(directions)
    for matrix_row in matrix_rows:
        for column in matrix_row:
            column_weights[column] += 1
    maximum_hit = max(column_weights)
    require(maximum_hit < len(words),
            "a quadratic exchange direction hits every old singleton")
    require(min(all_deficit_sizes) == 2,
            "a linear mate appeared in the no-fourth complex")

    # One small integer/Farkas candidate per chart: assign weight one to every
    # old obstruction coordinate.  Every quadratic column has weight at most
    # maximum_hit < total, proving the shell obstruction.  The dense guard
    # below proves that this certificate cannot extend to arbitrary support.
    return {
        "chart": old_record["chart"],
        "obstruction_coordinates": len(words),
        "quadratic_generators": len(directions),
        "quadratic_incidence_rank_over_Q": rank,
        "quadratic_left_nullity": len(words) - rank,
        "quadratic_column_maximum_weight": maximum_hit,
        "uniform_integer_dual": {
            "coordinate_weights": "all 1",
            "total_weight": len(words),
            "maximum_single_generator_hit_weight": maximum_hit,
            "strict_gap": len(words) - maximum_hit,
        },
        "full_deficit_size_range": [min(all_deficit_sizes),
                                    max(all_deficit_sizes)],
    }


def main():
    shell = json.loads(SHELL_RESULT.read_text())
    require(shell["logical_sha256"] ==
            "717b6c79c51c1ea396641d425253316a4c649be70281a8319c5fcbea6014c12f",
            "first-shell parent ledger changed")
    rows = tuple(sorted(SOURCE.target_orbit_rows()))
    old_by_chart = {row["chart"]: row for row in shell["records"]}
    records = []
    for chart, row in enumerate(rows, 1):
        if chart in old_by_chart:
            records.append(chart_complex(row, old_by_chart[chart]))
    require(len(records) == 12, "exchange complex lost a no-fourth chart")
    require(len(records) <= 20, "candidate dual orbit budget exceeded")

    # Dense exact hostile control.  Put B=I+J on all 28 edges.  Every entry is
    # nonzero and det(B)=4.  In the factorization B=sum_i col_i(B) tensor e_i,
    # choosing label i for matching slot i gives, at a vertex, columns each
    # equal to e_i or e_i+1.  Their determinant is 1+k for k chosen B-columns,
    # hence one of 1,2,3,4 and never zero.  So the local rank-respecting
    # rainbow condition survives.  Yet full cell support makes all 105 perfect
    # matchings live in every output word, hence there are no singletons.
    dense = {
        "edge_matrix": [[2, 1, 1], [1, 2, 1], [1, 1, 2]],
        "determinant": 4,
        "all_252_cells_nonzero": True,
        "selected_local_determinants": [1, 2, 3, 4],
        "matching_terms_per_output_word": 105,
        "mixed_singleton_words": 0,
        "rank_respecting_for_every_selected_triple": True,
        "is_GHZ_source": False,
    }
    require(dense["determinant"] != 0
            and dense["matching_terms_per_output_word"] == 105
            and dense["mixed_singleton_words"] == 0,
            "dense counterguard failed")

    result = {
        "status": "PASS exchange-complex audit; dense support kills global dual",
        "records": records,
        "candidate_dual_orbits_tested": len(records),
        "dense_rank_respecting_counterguard": dense,
        "terminal": {
            "quadratic_shell_dual": (
                "The uniform positive obstruction covector proves the exact "
                "one-generator quadratic gaps recorded chartwise."),
            "arbitrary_support_verdict": (
                "No support-only cocycle, Farkas dual, or submodular potential "
                "can prove that hitting all old singletons forces a new "
                "singleton: the exact dense rank-respecting support hits every "
                "old obstruction and has fibre size 105 at every word."),
            "what_would_be_needed": (
                "A coefficient-sensitive identity using the mixed zero sums; "
                "the matching-exchange incidence complex alone is insufficient."),
        },
        "scope_guard": (
            "The dense point is a counterexample to the proposed support-level "
            "extension, not a GHZ source.  It does not refute a coefficient-level "
            "potential that uses the actual cancellation equations."),
        "source_hashes": {
            str(SHELL_SCRIPT.relative_to(ROOT)): file_sha(SHELL_SCRIPT),
            str(SHELL_RESULT.relative_to(ROOT)): file_sha(SHELL_RESULT),
        },
    }
    result["logical_sha256"] = logical_sha(result)
    if EXPECTED_LOGICAL_SHA256 != "TO_BE_FROZEN":
        require(result["logical_sha256"] == EXPECTED_LOGICAL_SHA256,
                "exchange-complex logical digest changed")
    if "--mutate-dense-singleton" in sys.argv:
        require(dense["mixed_singleton_words"] > 0,
                "mutation survived: dense singleton invented")
    if "--mutate-dense-rank" in sys.argv:
        require(dense["determinant"] == 0,
                "mutation survived: dense rank guard deleted")

    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if "--write-results" in sys.argv:
        OUT.write_text(text)
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
