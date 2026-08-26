#!/usr/bin/env python3
"""Exact colour escalation from the minimal four-cell X5 escape."""

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
PARENT_DIR = HERE.parent / "unaudited-codex-n8-x5-two-cell-escape-dichotomy-2026-08-25"
PARENT_MANIFEST = PARENT_DIR / "MANIFEST.sha256"
PARENT_MANIFEST_SHA256 = "dca3d614af5203d5dc2e1b6adb4c2c3f1621d3b0cf368f68d079a376f979f779"
CORE_PATH = PARENT_DIR / "audit_two_cell_dichotomy.py"
CORE_SHA256 = "f8305d4b514ac6dc0a2b28b359dbca62929667248596beee48804eb43109e876"

T12 = (0, 0, 0, 0, 1, 2, 0, 0)
T21 = (0, 0, 0, 0, 2, 1, 0, 0)
SIX_FORCED = (0, 0, 1, 0, 0, 0, 0, 1)
COMMON_NEXT = (0, 0, 2, 0, 0, 0, 0, 2)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def load_core():
    assert sha256(PARENT_MANIFEST) == PARENT_MANIFEST_SHA256
    assert sha256(CORE_PATH) == CORE_SHA256
    spec = importlib.util.spec_from_file_location("two_cell_core", CORE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


core = load_core()


def four_cell_source():
    source = core.base_source()
    for colour in (1, 2):
        core.put(source, 0, 4, 0, colour, 1)
        core.put(source, 3, 5, 0, colour, -1)
    return source


def pure_amplitudes(source):
    return [core.amplitude(source, (colour,) * 8) for colour in core.COLORS]


def cell_string(cell):
    u, v, a, b = cell
    return f"A{u}{v}[{a},{b}]"


def word_string(word):
    return "".join(map(str, word))


def relevant_absent_cells(source, target):
    return tuple(sorted({
        core.key(u, v, target[u], target[v])
        for u, v in itertools.combinations(core.SITES, 2)
        if core.get(source, u, v, target[u], target[v]) == 0
    }))


def exact_one_cell_repairs(source, target):
    """All one-coordinate values which zero the target amplitude."""
    base = core.amplitude(source, target)
    repairs = []
    for cell in relevant_absent_cells(source, target):
        trial = dict(source)
        trial[cell] = 1
        delta = core.amplitude(trial, target) - base
        if delta == 0:
            continue
        value = Fraction(-base, delta)
        trial[cell] = value
        assert core.amplitude(trial, target) == 0
        pures = pure_amplitudes(trial)
        repairs.append({
            "cell": cell_string(cell),
            "cell_tuple": cell,
            "required_value": int(value) if value.denominator == 1 else str(value),
            "pure_amplitudes": [int(item) for item in pures],
            "pure_preserving": pures == [1, 1, 1],
            "formal_triangle_guard_preserved": core.outside_response_count(trial) == 0,
        })
    return repairs


def missing_cells(source, matching, word):
    return frozenset(
        core.key(u, v, word[u], word[v])
        for u, v in matching
        if core.get(source, u, v, word[u], word[v]) == 0
    )


def mixed_census(source):
    violations = core.violation_census(source)
    return {
        "count": len(violations),
        "first_word": word_string(violations[0][0]),
        "first_amplitude": violations[0][1],
        "profiles": dict(sorted(Counter(core.profile(word) for word, _value, _terms in violations).items())),
    }


def main():
    source4 = four_cell_source()
    assert pure_amplitudes(source4) == [1, 1, 1]
    assert core.outside_response_count(source4) == 0
    assert core.amplitude_terms(source4, T12) == [(((0, 4), (1, 6), (2, 7), (3, 5)), -1)]
    assert core.amplitude_terms(source4, T21) == [(((0, 4), (1, 6), (2, 7), (3, 5)), -1)]
    census4 = mixed_census(source4)
    assert census4["count"] == 78 and census4["first_word"] == "00001200"

    repairs12 = exact_one_cell_repairs(source4, T12)
    assert len(repairs12) == 2
    assert [(item["cell"], item["required_value"], item["pure_preserving"]) for item in repairs12] == [
        ("A12[0,0]", -1, False),
        ("A45[1,2]", 1, True),
    ]

    source5 = dict(source4)
    core.put(source5, 4, 5, 1, 2, 1)
    assert pure_amplitudes(source5) == [1, 1, 1]
    assert core.outside_response_count(source5) == 0
    assert core.amplitude(source5, T12) == 0
    assert core.amplitude_terms(source5, T21) == [(((0, 4), (1, 6), (2, 7), (3, 5)), -1)]
    census5 = mixed_census(source5)
    assert census5["count"] == 87 and census5["first_word"] == "00002100"
    repairs21 = exact_one_cell_repairs(source5, T21)
    assert len(repairs21) == 2
    assert [(item["cell"], item["required_value"], item["pure_preserving"]) for item in repairs21] == [
        ("A12[0,0]", -1, False),
        ("A45[2,1]", 1, True),
    ]

    # Exact simultaneous two-cell support classification.  Pair every
    # correction matching for T12 with every correction matching for T21 and
    # retain unions containing at most two new coordinates.
    correction_matchings = []
    for target in (T12, T21):
        choices = []
        for matching in core.PM8:
            missing = missing_cells(source4, matching, target)
            if 0 < len(missing) <= 2:
                choices.append((matching, missing))
        correction_matchings.append(choices)
    small_unions = []
    for left, right in itertools.product(*correction_matchings):
        union = left[1] | right[1]
        if len(union) <= 2:
            small_unions.append((left, right, union))
    assert len(small_unions) == 7
    distinct_unions = {tuple(sorted(item[2])) for item in small_unions}
    assert len(distinct_unions) == 5
    cross_pair = tuple(sorted(((4, 5, 1, 2), (4, 5, 2, 1))))
    assert cross_pair in distinct_unions
    # Every competing union contains A12[00], or is the diagonal A17/A26
    # pair.  A12 changes Phi(0^8) linearly; A17*A26 changes it by the same
    # product needed for cancellation.  Hence only the cross pair can retain
    # the normalized pure row.
    for union in distinct_unions - {cross_pair}:
        assert (1, 2, 0, 0) in union or set(union) == {(1, 7, 0, 0), (2, 6, 0, 0)}

    source6 = dict(source5)
    core.put(source6, 4, 5, 2, 1, 1)
    assert pure_amplitudes(source6) == [1, 1, 1]
    assert core.outside_response_count(source6) == 0
    assert core.amplitude(source6, T12) == core.amplitude(source6, T21) == 0
    census6 = mixed_census(source6)
    assert census6["count"] == 96 and census6["first_word"] == "00100001"
    assert core.amplitude_terms(source6, SIX_FORCED) == [(core.M0, 1)]
    assert exact_one_cell_repairs(source6, SIX_FORCED) == []
    assert min(
        len(missing_cells(source6, matching, SIX_FORCED))
        for matching in core.PM8 if matching != core.M0
    ) == 2

    # Classify the next minimal two-cell boundary without following it.
    next_patterns = []
    all_two_missing = []
    for matching in core.PM8:
        cells = tuple(sorted(missing_cells(source6, matching, SIX_FORCED)))
        if len(cells) != 2:
            continue
        all_two_missing.append((matching, cells))
        trial = dict(source6)
        trial[cells[0]] = 1
        trial[cells[1]] = -1
        assert core.amplitude(trial, SIX_FORCED) == 0
        preserves = pure_amplitudes(trial) == [1, 1, 1]
        assert preserves == all(a != b for _u, _v, a, b in cells)
        if not preserves:
            continue
        outside = core.outside_response_count(trial)
        assert core.amplitude_terms(trial, COMMON_NEXT) == [(core.M0, 1)]
        next_patterns.append({
            "matching": core.matching_string(matching),
            "new_cells": [cell_string(cell) for cell in cells],
            "coefficient_constraint": "product=-1",
            "formal_triangle_guard_preserved": outside == 0,
            "outside_response_count_for_K_I": outside,
            "common_forced_word": word_string(COMMON_NEXT),
            "common_forced_amplitude": 1,
        })
    assert len(all_two_missing) == 12
    assert len(next_patterns) == 6
    assert sum(item["formal_triangle_guard_preserved"] for item in next_patterns) == 3
    assert sum(item["outside_response_count_for_K_I"] == 1 for item in next_patterns) == 3

    result = {
        "schema": "KRENN_X5_FOUR_CELL_COLOUR_ESCALATION_AUDIT_V1",
        "status": "PASS_MINIMAL_FOUR_TO_SIX_CELL_ESCALATION",
        "parent_manifest_sha256": PARENT_MANIFEST_SHA256,
        "core_sha256": CORE_SHA256,
        "four_cell_boundary": {
            "new_cells": ["A04[0,1]=+1", "A35[0,1]=-1", "A04[0,2]=+1", "A35[0,2]=-1"],
            "pure_amplitudes": [1, 1, 1],
            "formal_triangle_guard_preserved": True,
            "forced_word": "00001200",
            "forced_amplitude": -1,
            "mixed_census": census4,
        },
        "exact_first_escalation": {
            "all_one_cell_repairs": repairs12,
            "unique_pure_preserving_repair": "A45[1,2]=+1",
            "monovariant_missing_ordered_colour_entries": "2 -> 1",
            "five_cell_mixed_census": census5,
            "next_forced_word": "00002100",
            "next_forced_amplitude": -1,
        },
        "exact_second_escalation": {
            "all_one_cell_repairs": repairs21,
            "unique_pure_preserving_repair": "A45[2,1]=+1",
            "simultaneous_matching_pairs_checked": len(small_unions),
            "distinct_at_most_two_cell_supports": len(distinct_unions),
            "unique_pure_preserving_two_cell_support": ["A45[1,2]", "A45[2,1]"],
            "monovariant_missing_ordered_colour_entries": "1 -> 0",
        },
        "smallest_surviving_six_cell_support": {
            "new_cells": [
                "A04[0,1]=+1", "A35[0,1]=-1", "A04[0,2]=+1", "A35[0,2]=-1",
                "A45[1,2]=+1", "A45[2,1]=+1",
            ],
            "pure_amplitudes": [1, 1, 1],
            "formal_triangle_guard_preserved": True,
            "cleaned_cross_words": ["00001200", "00002100"],
            "mixed_census": census6,
            "unique_base_forced_word": "00100001",
            "unique_base_forced_amplitude": 1,
            "one_cell_repairs": 0,
        },
        "next_minimal_boundary": {
            "two_missing_cell_matchings": len(all_two_missing),
            "pure_preserving_patterns": len(next_patterns),
            "response_branch_patterns": 3,
            "guard_preserving_patterns": 3,
            "patterns": next_patterns,
            "common_unique_base_word": "00200002",
            "common_unique_base_amplitude": 1,
        },
        "restricted_monovariant": {
            "definition": "missing ordered off-diagonal entries of A45 on colours {1,2}",
            "values": [2, 1, 0],
            "scope": "successive minimal one-cell pure-preserving repairs of the residual cross-colour sector",
            "terminal_fact": "at zero, 00100001 is unique-base and has no one-cell repair",
            "general_nonminimal_chain_proved": False,
        },
        "scope": {
            "minimal_four_to_six_cell_chain_proved": True,
            "smallest_surviving_six_cell_support_is_X5": False,
            "general_off_support_monovariant_proved": False,
            "active_clean_cap_proved": False,
            "broad_cegar": False,
            "degree_twelve_read": False,
            "full_conjecture_claim": False,
        },
    }
    temporary = HERE / "results_four_cell_escalation.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_four_cell_escalation.json")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
