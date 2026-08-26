#!/usr/bin/env python3
"""Exact quotient and smallest cycle in the X5 successive-minimal support walk."""

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
PARENT_DIR = HERE.parent / "unaudited-codex-n8-x5-successive-minimal-chain-2026-08-25"
PARENT_MANIFEST = PARENT_DIR / "MANIFEST.sha256"
PARENT_MANIFEST_SHA256 = "6d77153968c4386cd56ab01650c53882efafc15cb9d00cba55d5877ad9dc3717"
CORE = HERE.parent / "unaudited-codex-n8-x5-two-cell-escape-dichotomy-2026-08-25/audit_two_cell_dichotomy.py"
CORE_SHA256 = "f8305d4b514ac6dc0a2b28b359dbca62929667248596beee48804eb43109e876"

P45_1 = (0, 0, 0, 0, 1, 1, 0, 0)
P27_1 = (0, 0, 1, 0, 0, 0, 0, 1)
P27_2 = (0, 0, 2, 0, 0, 0, 0, 2)
P16_1 = (0, 1, 0, 0, 0, 0, 1, 0)
P16_2 = (0, 2, 0, 0, 0, 0, 2, 0)
P03_1 = (1, 0, 0, 1, 0, 0, 0, 0)
P03_2 = (2, 0, 0, 2, 0, 0, 0, 0)
RETURN_1 = (1, 1, 1, 1, 0, 0, 1, 1)
ZERO_FREE = (1, 1, 1, 1, 2, 2, 1, 1)


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


def missing_cells(source, matching, word):
    return tuple(sorted(
        core.key(u, v, word[u], word[v])
        for u, v in matching
        if core.get(source, u, v, word[u], word[v]) == 0
    ))


def pures(source):
    return [core.amplitude(source, (colour,) * 8) for colour in core.COLORS]


def cell_string(cell):
    u, v, a, b = cell
    return f"A{u}{v}[{a},{b}]"


def add_pair(source, cells):
    trial = dict(source)
    trial[cells[0]] = 1
    trial[cells[1]] = -1
    return trial


def admissible_patterns(source, target):
    assert core.amplitude_terms(source, target) == [(core.M0, 1)]
    raw_minimum = min(
        len(missing_cells(source, matching, target))
        for matching in core.PM8 if matching != core.M0
    )
    rejected_at_raw = 0
    for size in range(raw_minimum, 5):
        accepted = []
        for matching in core.PM8:
            cells = missing_cells(source, matching, target)
            if len(cells) != size:
                continue
            existing_product = 1
            for u, v in matching:
                value = core.get(source, u, v, target[u], target[v])
                if value:
                    existing_product *= value
            assert existing_product in (-1, 1)
            trial = dict(source)
            for cell in cells[:-1]:
                trial[cell] = 1
            trial[cells[-1]] = -1 // existing_product
            if core.amplitude(trial, target) != 0:
                continue
            if pures(trial) != [1, 1, 1]:
                if size == raw_minimum:
                    rejected_at_raw += 1
                continue
            accepted.append((core.matching_string(matching), cells, trial))
        if accepted:
            return raw_minimum, size, rejected_at_raw, accepted
    raise AssertionError("no admissible repair through four cells")


def signature(patterns):
    return tuple((name, cells) for name, cells, _source in patterns)


def six_cell_source():
    source = core.base_source()
    for colour in (1, 2):
        core.put(source, 0, 4, 0, colour, 1)
        core.put(source, 3, 5, 0, colour, -1)
    core.put(source, 4, 5, 1, 2, 1)
    core.put(source, 4, 5, 2, 1, 1)
    return source


def pair_record(patterns):
    return [
        {"matching": name, "new_cells": [cell_string(cell) for cell in cells], "coefficient_constraint": "product=-1"}
        for name, cells, _source in patterns
    ]


def main():
    source6 = six_cell_source()
    raw27, minimum27, rejected27, repairs27_1 = admissible_patterns(source6, P27_1)
    assert (raw27, minimum27, rejected27, len(repairs27_1)) == (2, 2, 6, 6)
    repairs27_2 = admissible_patterns(source6, P27_2)[3]
    assert tuple(name for name, _cells, _source in repairs27_1) == tuple(name for name, _cells, _source in repairs27_2)

    ten_cell_sources = []
    for _name1, _cells1, source8 in repairs27_1:
        _raw, _minimum, _rejected, colour2 = admissible_patterns(source8, P27_2)
        assert (_raw, _minimum, _rejected, len(colour2)) == (2, 2, 6, 6)
        for _name2, _cells2, source10 in colour2:
            ten_cell_sources.append(source10)
    assert len(ten_cell_sources) == 36

    # Exact quotient of the requested Phi(01000010) repairs.
    quotient16 = Counter()
    sources14 = []
    canonical16_1 = None
    canonical16_2 = None
    for source10 in ten_cell_sources:
        raw, minimum, rejected, repairs16_1 = admissible_patterns(source10, P16_1)
        quotient16[(raw, minimum, rejected, signature(repairs16_1))] += 1
        assert (raw, minimum, rejected, len(repairs16_1)) == (2, 2, 6, 6)
        if canonical16_1 is None:
            canonical16_1 = repairs16_1
        assert signature(repairs16_1) == signature(canonical16_1)
        assert all(all(cell not in source10 for cell in cells) for _name, cells, _trial in repairs16_1)
        for _name1, _cells1, source12 in repairs16_1:
            raw2, minimum2, rejected2, repairs16_2 = admissible_patterns(source12, P16_2)
            assert (raw2, minimum2, rejected2, len(repairs16_2)) == (2, 2, 6, 6)
            if canonical16_2 is None:
                canonical16_2 = repairs16_2
            assert signature(repairs16_2) == signature(canonical16_2)
            assert all(all(cell not in source12 for cell in cells) for _name, cells, _trial in repairs16_2)
            for _name2, _cells2, source14 in repairs16_2:
                sources14.append(source14)
    assert len(quotient16) == 1 and next(iter(quotient16.values())) == 36
    assert len(sources14) == 1296

    # Pair03 is the only change of local geometry: raw one-cell matchings all
    # destroy a pure row, and the admissible minimum is two cells with 8 types.
    quotient03_1 = Counter()
    quotient03_2 = Counter()
    canonical03_1 = None
    canonical03_2 = None
    for source14 in sources14:
        raw1, minimum1, rejected1, repairs03_1 = admissible_patterns(source14, P03_1)
        raw2, minimum2, rejected2, repairs03_2 = admissible_patterns(source14, P03_2)
        assert (raw1, minimum1, rejected1, len(repairs03_1)) == (1, 2, 1, 8)
        assert (raw2, minimum2, rejected2, len(repairs03_2)) == (1, 2, 1, 8)
        quotient03_1[(raw1, minimum1, rejected1, signature(repairs03_1))] += 1
        quotient03_2[(raw2, minimum2, rejected2, signature(repairs03_2))] += 1
        if canonical03_1 is None:
            canonical03_1 = repairs03_1
            canonical03_2 = repairs03_2
        assert signature(repairs03_1) == signature(canonical03_1)
        assert signature(repairs03_2) == signature(canonical03_2)
        assert all(all(cell not in source14 for cell in cells) for _name, cells, _trial in repairs03_1 + repairs03_2)
    assert len(quotient03_1) == len(quotient03_2) == 1
    assert next(iter(quotient03_1.values())) == next(iter(quotient03_2.values())) == 1296

    # Coordinate-level no-reuse across the colour-1 pair walk.
    pair45_cells = {(0, 4, 0, 1), (3, 5, 0, 1)}
    unions = [
        pair45_cells,
        {cell for _name, cells, _source in repairs27_1 for cell in cells},
        {cell for _name, cells, _source in canonical16_1 for cell in cells},
        {cell for _name, cells, _source in canonical03_1 for cell in cells},
    ]
    assert all(not left & right for index, left in enumerate(unions) for right in unions[index + 1:])
    edge_unions = [{cell[:2] for cell in layer} for layer in unions]
    assert edge_unions[0] & edge_unions[3] == {(0, 4), (3, 5)}

    # Quotient all colour-1 branch triples and expose the edge-level cycle.
    cycle_base = core.base_source()
    core.put(cycle_base, 0, 4, 0, 1, 1)
    core.put(cycle_base, 3, 5, 0, 1, -1)
    return_amplitudes = Counter()
    amplitude_outside = Counter()
    cycles = []
    for f_index, (_f_name, f_cells, _f_source) in enumerate(repairs27_1):
        for h_index, (_h_name, h_cells, _h_source) in enumerate(canonical16_1):
            for j_index, (_j_name, j_cells, _j_source) in enumerate(canonical03_1):
                source = cycle_base
                for cells in (f_cells, h_cells, j_cells):
                    source = add_pair(source, cells)
                assert pures(source) == [1, 1, 1]
                assert all(core.amplitude(source, word) == 0 for word in (P45_1, P27_1, P16_1, P03_1))
                value = core.amplitude(source, RETURN_1)
                outside = core.outside_response_count(source)
                return_amplitudes[value] += 1
                amplitude_outside[(value, outside)] += 1
                if value == 0:
                    cycles.append((f_index, h_index, j_index, outside, source))
    assert return_amplitudes == {0: 140, 1: 96, -1: 48, -2: 4}
    assert len(cycles) == 140
    assert sum(outside == 0 for _f, _h, _j, outside, _source in cycles) == 18

    # Canonical smallest guard-preserving cycle: branch indices (1,1,4).
    canonical_cycle = next(item for item in cycles if item[:4] == (1, 1, 4, 0))
    cycle_source = canonical_cycle[4]
    assert len(cycle_source) - len(core.base_source()) == 8
    cycle_cells = [
        "A04[0,1]=+1", "A35[0,1]=-1",
        "A12[0,1]=+1", "A67[0,1]=-1",
        "A12[1,0]=+1", "A67[1,0]=-1",
        "A04[1,0]=+1", "A35[1,0]=-1",
    ]
    cycle_terms = {
        "00001100": [(core.matching_string(matching), value) for matching, value in core.amplitude_terms(cycle_source, P45_1)],
        "00100001": [(core.matching_string(matching), value) for matching, value in core.amplitude_terms(cycle_source, P27_1)],
        "01000010": [(core.matching_string(matching), value) for matching, value in core.amplitude_terms(cycle_source, P16_1)],
        "10010000": [(core.matching_string(matching), value) for matching, value in core.amplitude_terms(cycle_source, P03_1)],
        "11110011": [(core.matching_string(matching), value) for matching, value in core.amplitude_terms(cycle_source, RETURN_1)],
    }
    assert all(sum(value for _matching, value in terms) == 0 for terms in cycle_terms.values())
    violations = core.violation_census(cycle_source)
    assert len(violations) == 132
    assert core.word_string(violations[0][0]) == "00002200" and violations[0][1] == 1
    assert core.amplitude_terms(cycle_source, (0, 0, 0, 0, 2, 2, 0, 0)) == [(core.M0, 1)]

    completed_reference_zero_paths = 6 ** 4 * 8 ** 2
    # Every repair cell after A45 contains the reference colour 0.  The only
    # zero-free added cells are A45[12]/A45[21], neither used by ZERO_FREE.
    assert all(0 in cell[2:] for layer in unions[1:] for cell in layer)
    canonical_full = canonical03_1[0][2]
    canonical_full = add_pair(canonical_full, canonical03_2[0][1])
    assert core.amplitude_terms(canonical_full, ZERO_FREE) == [(core.M0, 1)]

    result = {
        "schema": "KRENN_X5_SUPPORT_WALK_CYCLE_AUDIT_V1",
        "status": "PASS_CELL_NO_REUSE_EDGE_CYCLE_FOUND",
        "parent_manifest_sha256": PARENT_MANIFEST_SHA256,
        "core_sha256": CORE_SHA256,
        "pair16_quotient": {
            "ten_cell_sources_checked": len(ten_cell_sources),
            "quotient_classes": len(quotient16),
            "raw_minimum_cells": 2,
            "admissible_minimum_cells": 2,
            "pure_preserving_patterns_per_colour": 6,
            "colour_one_patterns": pair_record(canonical16_1),
            "colour_two_is_exact_colour_lift": True,
            "resulting_sources_after_both_colours": len(sources14),
        },
        "pair03_quotient": {
            "input_sources_checked": len(sources14),
            "quotient_classes_per_colour": 1,
            "raw_minimum_cells": 1,
            "raw_patterns_rejected_by_pure_normalization": 1,
            "admissible_minimum_cells": 2,
            "pure_preserving_patterns_per_colour": 8,
            "colour_one_patterns": pair_record(canonical03_1),
            "colour_two_is_exact_colour_lift": True,
            "completed_reference_zero_path_count": completed_reference_zero_paths,
            "common_zero_free_residual": "Phi(11112211)=+1 from unique 03|16|27|45",
        },
        "no_reuse_and_cycle": {
            "source_coordinate_reuse_across_pair45_27_16_03": False,
            "coordinate_layer_intersections_empty": True,
            "edge_reuse": ["04", "35"],
            "edge_level_no_cycle_lemma": False,
            "walk": "45 -> 27 -> 16 -> 03 -> 45",
            "successive_minimal_cell_lower_bound": 8,
            "reason_for_lower_bound": "four layers, two admissible cells each, disjoint coordinate layers",
        },
        "cycle_quotient": {
            "branch_triples": 288,
            "return_amplitude_census": {str(key): value for key, value in sorted(return_amplitudes.items())},
            "cycles": len(cycles),
            "guard_preserving_cycles": 18,
            "amplitude_outside_census": {f"amplitude={a},outside={o}": value for (a, o), value in sorted(amplitude_outside.items())},
        },
        "smallest_guard_preserving_cycle": {
            "new_cells": cycle_cells,
            "new_cell_count": 8,
            "pure_amplitudes": [1, 1, 1],
            "formal_triangle_guard_preserved": True,
            "outside_response_count_for_K_I": 0,
            "same_source_reciprocity_compatible": True,
            "cancelled_walk_terms": cycle_terms,
            "remaining_mixed_violations": len(violations),
            "first_residual_word": "00002200",
            "first_residual_amplitude": 1,
            "first_residual_unique_matching": "03|16|27|45",
        },
        "scope": {
            "cell_coordinate_no_reuse_for_reference_zero_walk": True,
            "edge_level_no_cycle": False,
            "smallest_cycle_within_successive_minimal_policy": True,
            "global_arbitrary_source_cycle_minimality": False,
            "active_clean_cap_proved": False,
            "degree_twelve_read": False,
            "broad_cegar": False,
            "full_conjecture_claim": False,
        },
    }
    temporary = HERE / "results_support_walk_cycle.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_support_walk_cycle.json")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
