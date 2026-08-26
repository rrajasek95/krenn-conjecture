#!/usr/bin/env python3
"""Exact residual-amplitude ledger for the 140 X5 support cycles."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import hashlib
import importlib.util
import itertools
import json
import os
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
PARENT_DIR = HERE.parent / "unaudited-codex-n8-x5-support-walk-2026-08-25"
PARENT_MANIFEST = PARENT_DIR / "MANIFEST.sha256"
PARENT_MANIFEST_SHA256 = "45e9e0de636bba080efc34b4005ed4a8a62b5c0fc37f15419d670275dfa4df1f"
PARENT_AUDIT = PARENT_DIR / "audit_support_walk_cycle.py"
PARENT_AUDIT_SHA256 = "d3b474dc29a9f47931b69fee4eefad9f4b54a7eb1f8aa9cbba725183c815ba8c"
TARGET2 = (0, 0, 0, 0, 2, 2, 0, 0)
NEXT2 = (0, 0, 2, 0, 0, 0, 0, 2)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


assert sha256(PARENT_MANIFEST) == PARENT_MANIFEST_SHA256
assert sha256(PARENT_AUDIT) == PARENT_AUDIT_SHA256
spec = importlib.util.spec_from_file_location("support_cycle", PARENT_AUDIT)
assert spec is not None and spec.loader is not None
walk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(walk)
core = walk.core


def pair_words():
    for a, b, c, d in itertools.product(core.COLORS, repeat=4):
        yield (a, b, c, d), (a, b, c, a, d, d, b, c)


def matrix_rank(matrix):
    rows = [[Fraction(value) for value in row] for row in matrix]
    rank = 0
    for column in range(len(rows[0])):
        pivot = next((index for index in range(rank, len(rows)) if rows[index][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        divisor = rows[rank][column]
        rows[rank] = [value / divisor for value in rows[rank]]
        for index in range(len(rows)):
            if index == rank or not rows[index][column]:
                continue
            factor = rows[index][column]
            rows[index] = [value - factor * pivot_value for value, pivot_value in zip(rows[index], rows[rank])]
        rank += 1
    return rank


def amplitude_ledger(source):
    values = {}
    unique_base_words = []
    for coordinates, word in pair_words():
        value = core.amplitude(source, word)
        values[coordinates] = value
        if len(set(word)) > 1 and core.amplitude_terms(source, word) == [(core.M0, 1)]:
            unique_base_words.append(core.word_string(word))
    mixed = [value for coordinates, value in values.items() if len(set(coordinates)) > 1]
    matrix = [
        [values[(a, b, c, d)] for b in core.COLORS for c in core.COLORS]
        for a in core.COLORS for d in core.COLORS
    ]
    vector = [values[coordinates] for coordinates, _word in pair_words()]
    vector_hash = hashlib.sha256(json.dumps(vector, separators=(",", ":")).encode()).hexdigest()
    return {
        "nonzero_mixed": sum(value != 0 for value in mixed),
        "signed_sum": sum(mixed),
        "absolute_sum": sum(abs(value) for value in mixed),
        "unique_base_count": len(unique_base_words),
        "unique_base_parity": len(unique_base_words) % 2,
        "flattening_rank": matrix_rank(matrix),
        "amplitude_vector_sha256": vector_hash,
    }


def ledger_key(ledger):
    return (
        ledger["nonzero_mixed"], ledger["signed_sum"], ledger["absolute_sum"],
        ledger["unique_base_count"], ledger["unique_base_parity"], ledger["flattening_rank"],
    )


def counter_json(counter):
    return {"|".join(map(str, key)): value for key, value in sorted(counter.items())}


def build_cycles():
    source6 = walk.six_cell_source()
    repairs27 = walk.admissible_patterns(source6, walk.P27_1)[3]
    source8 = repairs27[0][2]
    repairs27_colour2 = walk.admissible_patterns(source8, walk.P27_2)[3]
    source10 = repairs27_colour2[0][2]
    repairs16 = walk.admissible_patterns(source10, walk.P16_1)[3]
    source12 = repairs16[0][2]
    repairs16_colour2 = walk.admissible_patterns(source12, walk.P16_2)[3]
    source14 = repairs16_colour2[0][2]
    repairs03 = walk.admissible_patterns(source14, walk.P03_1)[3]
    cycle_base = core.base_source()
    core.put(cycle_base, 0, 4, 0, 1, 1)
    core.put(cycle_base, 3, 5, 0, 1, -1)
    cycles = []
    for f_index, (_name_f, cells_f, _source_f) in enumerate(repairs27):
        for h_index, (_name_h, cells_h, _source_h) in enumerate(repairs16):
            for j_index, (_name_j, cells_j, _source_j) in enumerate(repairs03):
                source = cycle_base
                for cells in (cells_f, cells_h, cells_j):
                    source = walk.add_pair(source, cells)
                if core.amplitude(source, walk.RETURN_1) == 0:
                    cycles.append((f_index, h_index, j_index, core.outside_response_count(source), source))
    assert len(cycles) == 140
    return cycles


def main():
    cycles = build_cycles()
    cycle_records = []
    cycle_distribution = Counter()
    guard_distribution = Counter()
    repair_distribution = Counter()
    repair_signature = None
    component_change_witnesses = {}
    repaired_sources_checked = 0
    for f_index, h_index, j_index, outside, source in cycles:
        before = amplitude_ledger(source)
        cycle_distribution[ledger_key(before)] += 1
        if outside == 0:
            guard_distribution[ledger_key(before)] += 1
        cycle_records.append({
            "branch": [f_index, h_index, j_index],
            "outside_response_count": outside,
            "ledger": before,
        })
        raw, minimum, rejected, repairs = walk.admissible_patterns(source, TARGET2)
        assert (raw, minimum, rejected, len(repairs)) == (1, 2, 1, 8)
        signature = tuple((name, cells) for name, cells, _trial in repairs)
        if repair_signature is None:
            repair_signature = signature
        assert signature == repair_signature
        for repair_index, (name, cells, repaired) in enumerate(repairs):
            after = amplitude_ledger(repaired)
            repair_distribution[ledger_key(after)] += 1
            repaired_sources_checked += 1
            assert core.amplitude_terms(repaired, NEXT2) == [(core.M0, 1)]
            for field in ("nonzero_mixed", "signed_sum", "unique_base_count", "unique_base_parity", "flattening_rank"):
                if before[field] != after[field] and field not in component_change_witnesses:
                    component_change_witnesses[field] = {
                        "cycle_branch": [f_index, h_index, j_index],
                        "repair_index": repair_index,
                        "repair_matching": name,
                        "new_cells": [walk.cell_string(cell) for cell in cells],
                        "before": before[field],
                        "after": after[field],
                    }
    assert repaired_sources_checked == 140 * 8 == 1120
    assert set(component_change_witnesses) == {
        "nonzero_mixed", "signed_sum", "unique_base_count", "unique_base_parity", "flattening_rank"
    }
    assert len(cycle_distribution) == 12
    assert len(guard_distribution) == 3

    canonical = next(source for f, h, j, outside, source in cycles if (f, h, j, outside) == (1, 1, 4, 0))
    canonical_before = amplitude_ledger(canonical)
    assert ledger_key(canonical_before) == (46, 46, 46, 46, 0, 1)
    raw, minimum, rejected, canonical_repairs = walk.admissible_patterns(canonical, TARGET2)
    canonical_repair_records = []
    first_residual_census = Counter()
    for name, cells, repaired in canonical_repairs:
        violations = core.violation_census(repaired)
        first = (core.word_string(violations[0][0]), violations[0][1])
        first_residual_census[first] += 1
        canonical_repair_records.append({
            "matching": name,
            "new_cells": [walk.cell_string(cell) for cell in cells],
            "coefficient_constraint": "product=-1",
            "ledger": amplitude_ledger(repaired),
            "mixed_violations": len(violations),
            "first_residual_word": first[0],
            "first_residual_amplitude": first[1],
            "outside_response_count": core.outside_response_count(repaired),
        })
    assert first_residual_census == {("00002201", 1): 2, ("00011000", -1): 5, ("00001200", -1): 1}

    # Saturate the same guard-preserving 4-edge cycle for all six ordered
    # colour pairs.  Inclusion-exclusion cancels the two elementary pair
    # defects, but leaves six zero-free unique-base words exactly.
    saturated = core.base_source()
    for u, v, sign in ((0, 4, 1), (1, 2, 1), (3, 5, -1), (6, 7, -1)):
        for left, right in itertools.permutations(core.COLORS, 2):
            core.put(saturated, u, v, left, right, sign)
    assert core.outside_response_count(saturated) == 0
    pures = [core.amplitude(saturated, (colour,) * 8) for colour in core.COLORS]
    assert pures == [1, 1, 1]
    saturated_unique = []
    for _coordinates, word in pair_words():
        if len(set(word)) > 1 and core.amplitude_terms(saturated, word) == [(core.M0, 1)]:
            saturated_unique.append(core.word_string(word))
    assert saturated_unique == [
        "01100011", "02200022", "10011100",
        "12211122", "20022200", "21122211",
    ]
    saturated_violations = core.violation_census(saturated)
    assert len(saturated_violations) == 1680
    assert core.word_string(saturated_violations[0][0]) == "00001200"
    assert saturated_violations[0][1] == -1
    saturated_ledger = amplitude_ledger(saturated)
    assert ledger_key(saturated_ledger) == (6, 6, 6, 6, 0, 1)

    result = {
        "schema": "KRENN_X5_CYCLE_RESIDUAL_LEDGER_AUDIT_V1",
        "status": "PASS_SCALAR_INVARIANTS_REFUTED_RESIDUAL_NONVANISHING_PROVED",
        "parent_manifest_sha256": PARENT_MANIFEST_SHA256,
        "parent_audit_sha256": PARENT_AUDIT_SHA256,
        "ledger_definition": {
            "sector": "81 words (a,b,c,a,d,d,b,c), with 78 mixed words",
            "fields": [
                "nonzero_mixed", "signed_sum", "absolute_sum", "unique_base_count",
                "unique_base_parity", "9x9 flattening rank", "amplitude vector SHA256"
            ],
            "flattening": "rows=(a,d), columns=(b,c), exact rational rank",
        },
        "cycle_ledger": {
            "cycles": len(cycles),
            "guard_preserving_cycles": sum(record["outside_response_count"] == 0 for record in cycle_records),
            "records": cycle_records,
            "distribution": counter_json(cycle_distribution),
            "distribution_classes": len(cycle_distribution),
            "guard_distribution": counter_json(guard_distribution),
            "guard_distribution_classes": len(guard_distribution),
        },
        "invariant_verdict": {
            "nonzero_count_invariant": False,
            "signed_sum_invariant": False,
            "unique_base_count_invariant": False,
            "unique_base_parity_invariant": False,
            "flattening_rank_invariant": False,
            "change_witnesses": component_change_witnesses,
            "repaired_sources_checked": repaired_sources_checked,
            "repair_ledger_distribution": counter_json(repair_distribution),
        },
        "canonical_first_residual_repairs": {
            "target": "Phi(00002200)=+1",
            "raw_minimum_cells": raw,
            "raw_patterns_rejected_by_pure_normalization": rejected,
            "admissible_minimum_cells": minimum,
            "repair_patterns": canonical_repair_records,
            "all_cycle_repair_quotient_classes": 1,
            "all_cycle_repair_moves": repaired_sources_checked,
            "common_unique_base_residual": "Phi(00200002)=+1 from 03|16|27|45",
            "zero_residual_sources": 0,
        },
        "colour_saturated_cycle": {
            "offdiagonal_new_cells": 24,
            "pure_amplitudes": pures,
            "formal_triangle_guard_preserved": True,
            "outside_response_count": 0,
            "ledger": saturated_ledger,
            "unique_base_residual_words": saturated_unique,
            "identity": "Phi(a,b,b,a,a,a,b,b)=1 for all a!=b",
            "mixed_violations": len(saturated_violations),
            "first_residual_word": "00001200",
            "first_residual_amplitude": -1,
            "normalized_X5": False,
        },
        "scope": {
            "simple_scalar_ledger_invariant_found": False,
            "first_residual_minimal_repairs_exhaustive_for_all_140_cycles": True,
            "residual_nonvanishing_after_every_classified_move": True,
            "zero_residual_cycle_found": False,
            "arbitrary_nonminimal_repairs_exhausted": False,
            "active_clean_cap_proved": False,
            "degree_twelve_read": False,
            "broad_cegar": False,
            "full_conjecture_claim": False,
        },
    }
    temporary = HERE / "results_cycle_residual_ledger.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_cycle_residual_ledger.json")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
