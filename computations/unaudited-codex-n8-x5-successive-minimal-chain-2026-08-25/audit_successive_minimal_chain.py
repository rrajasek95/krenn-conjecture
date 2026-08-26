#!/usr/bin/env python3
"""Classify the first non-one-cell X5 repair layer after A45 escalation."""

from __future__ import annotations

from collections import Counter
import hashlib
import importlib.util
import itertools
import json
import os
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
PARENT_DIR = HERE.parent / "unaudited-codex-n8-x5-four-cell-colour-escalation-2026-08-25"
PARENT_MANIFEST = PARENT_DIR / "MANIFEST.sha256"
PARENT_MANIFEST_SHA256 = "adff4a4a49f5493a542b5042fabdcd3871777bfa91c88ab4f721b1cc3842ee02"
CORE = HERE.parent / "unaudited-codex-n8-x5-two-cell-escape-dichotomy-2026-08-25/audit_two_cell_dichotomy.py"
CORE_SHA256 = "f8305d4b514ac6dc0a2b28b359dbca62929667248596beee48804eb43109e876"

F1 = (0, 0, 1, 0, 0, 0, 0, 1)
F2 = (0, 0, 2, 0, 0, 0, 0, 2)
NEXT = (0, 1, 0, 0, 0, 0, 1, 0)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


assert sha256(PARENT_MANIFEST) == PARENT_MANIFEST_SHA256
assert sha256(CORE) == CORE_SHA256
spec = importlib.util.spec_from_file_location("x5_core", CORE)
assert spec is not None and spec.loader is not None
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)


def six_cell_source():
    source = core.base_source()
    for colour in (1, 2):
        core.put(source, 0, 4, 0, colour, 1)
        core.put(source, 3, 5, 0, colour, -1)
    core.put(source, 4, 5, 1, 2, 1)
    core.put(source, 4, 5, 2, 1, 1)
    return source


def missing_cells(source, matching, word):
    return tuple(sorted(
        core.key(u, v, word[u], word[v])
        for u, v in matching
        if core.get(source, u, v, word[u], word[v]) == 0
    ))


def pure_amplitudes(source):
    return [core.amplitude(source, (colour,) * 8) for colour in core.COLORS]


def cell_string(cell):
    u, v, a, b = cell
    return f"A{u}{v}[{a},{b}]"


def minimal_two_cell_patterns(source, target):
    assert core.amplitude_terms(source, target) == [(core.M0, 1)]
    minimum = min(
        len(missing_cells(source, matching, target))
        for matching in core.PM8 if matching != core.M0
    )
    assert minimum == 2
    all_patterns = []
    accepted = []
    for matching in core.PM8:
        cells = missing_cells(source, matching, target)
        if len(cells) != minimum:
            continue
        trial = dict(source)
        trial[cells[0]] = 1
        trial[cells[1]] = -1
        terms = core.amplitude_terms(trial, target)
        assert terms == [(matching, -1), (core.M0, 1)] or terms == [(core.M0, 1), (matching, -1)]
        assert core.amplitude(trial, target) == 0
        preserves = pure_amplitudes(trial) == [1, 1, 1]
        assert preserves == all(a != b for _u, _v, a, b in cells)
        record = {
            "matching": core.matching_string(matching),
            "new_cells": [cell_string(cell) for cell in cells],
            "cell_tuples": cells,
            "coefficient_constraint": "product=-1",
            "pure_preserving": preserves,
        }
        all_patterns.append(record)
        if preserves:
            accepted.append((record, trial))
    assert len(all_patterns) == 12 and len(accepted) == 6
    return all_patterns, accepted


def enabled_alternatives(source, target):
    return [
        matching for matching in core.PM8
        if matching != core.M0 and not missing_cells(source, matching, target)
    ]


def main():
    source6 = six_cell_source()
    assert pure_amplitudes(source6) == [1, 1, 1]
    assert core.outside_response_count(source6) == 0
    assert core.amplitude_terms(source6, F1) == [(core.M0, 1)]
    assert core.amplitude_terms(source6, F2) == [(core.M0, 1)]

    all_f1, accepted_f1 = minimal_two_cell_patterns(source6, F1)
    f1_names = [item[0]["matching"] for item in accepted_f1]
    assert f1_names == [
        "02|16|37|45", "03|12|45|67", "03|16|24|57",
        "03|16|25|47", "03|17|26|45", "07|16|23|45",
    ]

    combined = []
    f2_pattern_names = None
    for f1_record, source8 in accepted_f1:
        # Colour-1 additions cannot occur in the colour-2 word.
        assert core.amplitude_terms(source8, F2) == [(core.M0, 1)]
        all_f2, accepted_f2 = minimal_two_cell_patterns(source8, F2)
        names = [item[0]["matching"] for item in accepted_f2]
        assert names == f1_names
        if f2_pattern_names is None:
            f2_pattern_names = names
        for f2_record, source10 in accepted_f2:
            assert len(source10) - len(core.base_source()) == 10
            assert pure_amplitudes(source10) == [1, 1, 1]
            assert core.amplitude(source10, F1) == core.amplitude(source10, F2) == 0
            assert core.amplitude_terms(source10, NEXT) == [(core.M0, 1)]
            assert min(
                len(missing_cells(source10, matching, NEXT))
                for matching in core.PM8 if matching != core.M0
            ) == 2
            combined.append((f1_record, f2_record, source10))
    assert len(combined) == 36

    # Prove that fewer than four additional cells cannot cancel both F1/F2.
    # If a source with <=3 new cells did so, choose one nonzero alternative
    # matching for each target.  Exhaust every such matching pair.
    choices = []
    for target in (F1, F2):
        target_choices = []
        for matching in core.PM8:
            cells = frozenset(missing_cells(source6, matching, target))
            if cells:
                target_choices.append((matching, cells))
        choices.append(target_choices)
    lower_bound_pairs = []
    for left, right in itertools.product(*choices):
        union = left[1] | right[1]
        if len(union) <= 3:
            lower_bound_pairs.append((left, right, union))
    assert len(lower_bound_pairs) == 14
    assert Counter(len(item[2]) for item in lower_bound_pairs) == {2: 6, 3: 8}
    assert len({tuple(sorted(item[2])) for item in lower_bound_pairs}) == 14
    for left, right, union in lower_bound_pairs:
        # Both words use exactly the same diagonal alternative matching.
        assert left[0] == right[0]
        assert all(a == b == 0 for _u, _v, a, b in union)
        trial = dict(source6)
        ordered = sorted(union)
        for cell in ordered[:-1]:
            trial[cell] = 1
        trial[ordered[-1]] = -1
        assert enabled_alternatives(trial, F1) == [left[0]]
        assert enabled_alternatives(trial, F2) == [right[0]]
        assert core.amplitude(trial, F1) == core.amplitude(trial, F2) == 0
        # The identical diagonal matching occurs on 0^8 with coefficient -1.
        assert pure_amplitudes(trial) == [0, 1, 1]

    outside_census = Counter(core.outside_response_count(source) for _a, _b, source in combined)
    assert outside_census == {0: 9, 1: 21, 2: 6}

    # A concrete guard-preserving smallest continuation.
    example = next(
        (a, b, source) for a, b, source in combined
        if a["matching"] == b["matching"] == "03|12|45|67"
    )
    assert core.outside_response_count(example[2]) == 0
    example_new_cells = [
        "A04[0,1]=+1", "A35[0,1]=-1", "A04[0,2]=+1", "A35[0,2]=-1",
        "A45[1,2]=+1", "A45[2,1]=+1",
        "A12[0,1]=+1", "A67[0,1]=-1", "A12[0,2]=+1", "A67[0,2]=-1",
    ]

    result = {
        "schema": "KRENN_X5_SUCCESSIVE_MINIMAL_CHAIN_AUDIT_V1",
        "status": "PASS_NONTERMINAL_MINIMAL_LAYER_CLASSIFIED",
        "parent_manifest_sha256": PARENT_MANIFEST_SHA256,
        "core_sha256": CORE_SHA256,
        "six_cell_input": {
            "forced_colour_one_word": "00100001",
            "forced_colour_two_word": "00200002",
            "both_amplitudes": 1,
            "both_unique_matching": "03|16|27|45",
            "one_cell_repair_exists": False,
        },
        "colour_one_minimal_repairs": {
            "two_missing_cell_matchings": len(all_f1),
            "pure_preserving_patterns": len(accepted_f1),
            "accepted_matching_names": f1_names,
            "patterns": [record for record, _source in accepted_f1],
        },
        "colour_two_layer": {
            "minimum_new_cells_after_any_colour_one_repair": 2,
            "pure_preserving_patterns_per_colour_one_branch": 6,
            "matching_names": f2_pattern_names,
            "source_label_separation": "colour-1 repair cells do not occur in 00200002",
        },
        "four_cell_lower_bound": {
            "matching_pairs_with_union_at_most_three": len(lower_bound_pairs),
            "union_size_census": {str(key): value for key, value in sorted(Counter(len(item[2]) for item in lower_bound_pairs).items())},
            "all_use_same_diagonal_matching_for_both_colours": True,
            "forced_pure_amplitudes": [0, 1, 1],
            "conclusion": "at least four additional source cells are required to cancel both colour words under pure normalization",
        },
        "smallest_nonminimal_continuations": {
            "additional_cells": 4,
            "total_new_cells_over_base_physical_source": 10,
            "branch_count": len(combined),
            "outside_response_census": {str(key): value for key, value in sorted(outside_census.items())},
            "guard_preserving_branches": outside_census[0],
            "branches_with_outside_response": len(combined) - outside_census[0],
            "common_forced_word": "01000010",
            "common_forced_amplitude": 1,
            "common_forced_matching": "03|16|27|45",
            "minimum_cells_for_next_repair": 2,
            "guard_preserving_example": example_new_cells,
        },
        "finite_colour_layer_monovariant": {
            "definition": "number of unrepaired nonzero colours on the 27 matching pair",
            "values": [2, 1, 0],
            "branch_independence": "six minimal supports at each colour; colour labels are disjoint",
            "terminal_for_this_layer": "after value zero, 01000010 is unique-base",
            "global_all_minimal_repairs_proved": False,
        },
        "scope": {
            "terminality_at_six_cells": False,
            "first_nonminimal_layer_exhaustive": True,
            "general_successive_minimal_chain_terminal": False,
            "active_clean_cap_proved": False,
            "degree_twelve_read": False,
            "broad_cegar": False,
            "full_conjecture_claim": False,
        },
    }
    temporary = HERE / "results_successive_minimal_chain.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_successive_minimal_chain.json")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
