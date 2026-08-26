#!/usr/bin/env python3
"""Classify every minimal pure-preserving cancellation of 00001100."""

from __future__ import annotations

from collections import Counter
import hashlib
import itertools
import json
import os
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PARENT = REPO / "computations/unaudited-codex-n8-x5-reciprocity-pure-row-guard-2026-08-25/MANIFEST.sha256"
PARENT_SHA256 = "0c6c164e7c1e6a37a369dfe509ec4145ae8d610a80a17d8b6ff0bb0a98a6d65b"
SITES = tuple(range(8))
COLORS = tuple(range(3))
TARGET1 = (0, 0, 0, 0, 1, 1, 0, 0)
TARGET2 = (0, 0, 0, 0, 2, 2, 0, 0)
M0 = ((0, 3), (1, 6), (2, 7), (4, 5))
BASE_EDGES = frozenset(M0 + ((6, 7),))
TRIANGLE = frozenset((0, 1, 2))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def matchings(vertices):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in matchings(rest):
            yield tuple(sorted(((first, second),) + tail))


PM8 = tuple(sorted(matchings(SITES)))
assert len(PM8) == 105 and M0 in PM8


def key(u, v, cu, cv):
    if u > v:
        u, v, cu, cv = v, u, cv, cu
    return u, v, cu, cv


def put(source, u, v, cu, cv, value):
    source[key(u, v, cu, cv)] = value


def get(source, u, v, cu, cv):
    return source.get(key(u, v, cu, cv), 0)


def base_source():
    source = {}
    for u, v in BASE_EDGES:
        for colour in COLORS:
            put(source, u, v, colour, colour, 1)
    return source


def amplitude_terms(source, word):
    terms = []
    for matching in PM8:
        value = 1
        for u, v in matching:
            value *= get(source, u, v, word[u], word[v])
        if value:
            terms.append((matching, value))
    return terms


def amplitude(source, word):
    return sum(value for _matching, value in amplitude_terms(source, word))


def identity():
    return [[int(i == j) for j in COLORS] for i in COLORS]


def zero_matrix():
    return [[0 for _ in COLORS] for _ in COLORS]


def response(source, p, q, a, b, covector):
    answer = zero_matrix()
    for alpha in COLORS:
        for beta in COLORS:
            answer[alpha][beta] = sum(
                covector[i][j] * (
                    get(source, p, a, i, alpha) * get(source, q, b, j, beta)
                    + get(source, p, b, i, beta) * get(source, q, a, j, alpha)
                )
                for i in COLORS for j in COLORS
            )
    return answer


def missing_cells(matching, word):
    source = base_source()
    return tuple(
        key(u, v, word[u], word[v])
        for u, v in matching
        if get(source, u, v, word[u], word[v]) == 0
    )


def pattern_class(matching):
    edges = set(matching)
    if (6, 7) in edges:
        return "direct_edge_six_cycle"
    if (1, 6) in edges and (2, 7) in edges:
        return "residual_four_cycle"
    return "cap_star_four_cycle"


def word_string(word):
    return "".join(map(str, word))


def matching_string(matching):
    return "|".join(f"{u}{v}" for u, v in matching)


def profile(word):
    return "+".join(map(str, sorted(Counter(word).values(), reverse=True)))


def make_candidate(matching, cells):
    source = base_source()
    put(source, *cells[0], 1)
    put(source, *cells[1], -1)
    assert amplitude(source, TARGET1) == 0
    assert [amplitude(source, (c,) * 8) for c in COLORS] == [1, 1, 1]
    return source


def outside_response_count(source):
    K = identity()
    outside = [
        edge for edge in itertools.combinations(range(6), 2)
        if not set(edge) <= TRIANGLE
    ]
    return sum(response(source, 6, 7, *edge, K) != zero_matrix() for edge in outside)


def violation_census(source):
    records = []
    for word in itertools.product(COLORS, repeat=8):
        value = amplitude(source, word)
        if value and len(set(word)) > 1:
            records.append((word, value, amplitude_terms(source, word)))
    return records


def main() -> None:
    assert sha256(PARENT) == PARENT_SHA256
    base = base_source()
    assert [amplitude(base, (c,) * 8) for c in COLORS] == [1, 1, 1]
    assert amplitude_terms(base, TARGET1) == [(M0, 1)]

    # Enumerate every alternative matching needing exactly two newly nonzero
    # source cells.  Pure preservation forces both new cells to be off-diagonal.
    all_two_cell = []
    pure_preserving = []
    for matching in PM8:
        if matching == M0:
            continue
        cells = missing_cells(matching, TARGET1)
        if len(cells) == 2:
            all_two_cell.append((matching, cells))
            trial = base_source()
            put(trial, *cells[0], 1)
            put(trial, *cells[1], -1)
            assert amplitude(trial, TARGET1) == 0
            preserves_pures = [amplitude(trial, (c,) * 8) for c in COLORS] == [1, 1, 1]
            # This computation independently proves that the seven diagonal
            # alternatives destroy Phi(0^8), while exactly the eight
            # off-diagonal alternatives preserve every pure row.
            assert preserves_pures == all(cu != cv for _u, _v, cu, cv in cells)
            if preserves_pures:
                pure_preserving.append((matching, cells))
    assert len(all_two_cell) == 15 and len(pure_preserving) == 8

    patterns = []
    class_counts = Counter()
    valid_guard_count = 0
    for matching, cells in pure_preserving:
        source = make_candidate(matching, cells)
        kind = pattern_class(matching)
        class_counts[kind] += 1
        outside_count = outside_response_count(source)
        guard_preserved = outside_count == 0
        valid_guard_count += guard_preserved
        violations = violation_census(source)
        profile_counts = Counter(profile(word) for word, _value, _terms in violations)
        # A direct-edge six-cycle cancels three base words but creates three
        # words outside the base matching support; hence its mixed count stays
        # 81.  The two four-cycle classes cancel a nine-word slice and create
        # no new words outside the base support.
        expected_count = 81 if kind == "direct_edge_six_cycle" else 69
        expected_profiles = (
            {"6+2": 24, "4+4": 18, "4+2+2": 39}
            if kind == "direct_edge_six_cycle"
            else {"6+2": 22, "4+4": 16, "4+2+2": 31}
        )
        assert len(violations) == expected_count
        assert dict(profile_counts) == expected_profiles
        assert amplitude(source, TARGET2) == 1
        assert amplitude_terms(source, TARGET2) == [(M0, 1)]
        patterns.append({
            "matching": matching_string(matching),
            "new_cells": [
                {"edge": [u, v], "colours": [cu, cv]}
                for u, v, cu, cv in cells
            ],
            "coefficient_constraint": "product=-1",
            "source_class": kind,
            "formal_triangle_guard_preserved": guard_preserved,
            "outside_response_count_for_K_I": outside_count,
            "remaining_mixed_violations": len(violations),
            "profile_census": dict(profile_counts),
            "forced_next_word": "00002200",
            "forced_next_amplitude": 1,
        })
    assert class_counts == {
        "direct_edge_six_cycle": 2,
        "cap_star_four_cycle": 4,
        "residual_four_cycle": 2,
    }
    assert valid_guard_count == 4
    assert sum(item["formal_triangle_guard_preserved"] for item in patterns
               if item["source_class"] == "cap_star_four_cycle") == 0

    # Exact source/symmetry census for the parent's A04/A35 boundary record.
    boundary_matching = ((0, 4), (1, 6), (2, 7), (3, 5))
    boundary_cells = missing_cells(boundary_matching, TARGET1)
    assert boundary_cells == ((0, 4, 0, 1), (3, 5, 0, 1))
    boundary = make_candidate(boundary_matching, boundary_cells)
    boundary_violations = violation_census(boundary)
    boundary_cancelled = []
    for a, b, c, d in itertools.product(COLORS, repeat=4):
        word = (a, b, c, a, d, d, b, c)
        terms = amplitude_terms(boundary, word)
        if len(terms) == 2 and sum(value for _matching, value in terms) == 0:
            boundary_cancelled.append(word)
    assert len(boundary_cancelled) == 9
    assert all(word[0] == word[3] == 0 and word[4] == word[5] == 1
               for word in boundary_cancelled)
    profile_counts = Counter(profile(word) for word, _value, _terms in boundary_violations)
    assert profile_counts == {"6+2": 22, "4+4": 16, "4+2+2": 31}
    # Swapping the two shared cap-star pair colours b,c is an exact word-level
    # symmetry of this source sector.
    encoded = {
        (word[0], word[1], word[2], word[4])
        for word, _value, _terms in boundary_violations
    }
    assert all((a, c, b, d) in encoded for a, b, c, d in encoded)
    symmetry_orbits = {
        min((a, b, c, d), (a, c, b, d)) for a, b, c, d in encoded
    }
    assert len(symmetry_orbits) == 45

    # The smallest next guard cancels both d=1 and d=2 slices.  The two colour
    # pairs require disjoint source-cell labels, so four new cells are minimal.
    next_source = base_source()
    for colour in (1, 2):
        put(next_source, 0, 4, 0, colour, 1)
        put(next_source, 3, 5, 0, colour, -1)
    assert amplitude(next_source, TARGET1) == amplitude(next_source, TARGET2) == 0
    assert [amplitude(next_source, (c,) * 8) for c in COLORS] == [1, 1, 1]
    assert outside_response_count(next_source) == 0
    next_violations = violation_census(next_source)
    # The two cancelled nine-word base slices are replaced by 18 cross-colour
    # words (differing 1/2 endpoint colours), so the total mixed count is 78.
    assert len(next_violations) == 78
    assert word_string(next_violations[0][0]) == "00001200"

    result = {
        "schema": "KRENN_X5_TWO_CELL_ESCAPE_DICHOTOMY_AUDIT_V1",
        "status": "PASS_ALL_MINIMAL_TWO_CELL_ESCAPES_FORCE_SECOND_X5_VIOLATION",
        "parent_manifest_sha256": PARENT_SHA256,
        "minimality_and_classification": {
            "all_two_new_cell_matchings": len(all_two_cell),
            "diagonal_patterns_rejected_by_pure_normalization": len(all_two_cell) - len(pure_preserving),
            "pure_preserving_two_cell_patterns": len(pure_preserving),
            "source_class_counts": dict(class_counts),
            "triangle_flag_symmetry_classes": [
                "residual_four_cycle",
                "cap_star_four_cycle (cap endpoints exchanged)",
                "direct_edge_six_cycle",
            ],
            "formal_guard_preserving_patterns": valid_guard_count,
            "patterns": patterns,
        },
        "proved_dichotomy_minimal_case": {
            "antecedent": (
                "three pure amplitudes are one and two newly nonzero source cells "
                "cancel Phi(00001100)=1"
            ),
            "classification_fact": (
                "pure preservation forces both cells to carry endpoint colours 0/1 "
                "on one of the eight listed alternative matchings"
            ),
            "conclusion": "Phi(00002200)=1 from the unique base matching 03|16|27|45",
            "active_cap_branch_needed": False,
            "mathematical_scope": "all minimal two-cell source-labelled escapes",
        },
        "boundary_69_violation_census": {
            "source": "A04[0,1]=+1, A35[0,1]=-1",
            "only_physical_matchings": ["03|16|27|45", "04|16|27|35"],
            "cancelled_slice": "edge-pair colours (a,b,c,d) with a=0,d=1; b,c arbitrary",
            "cancelled_words": [word_string(word) for word in boundary_cancelled],
            "cancelled_word_count": len(boundary_cancelled),
            "nonzero_mixed_count": len(boundary_violations),
            "profile_census": dict(profile_counts),
            "word_symmetry": "swap the colours on matching pairs16 and27",
            "word_symmetry_orbits": len(symmetry_orbits),
            "all_nonzero_amplitudes": 1,
        },
        "next_minimal_surviving_pattern": {
            "new_cells": [
                "A04[0,1]=+1", "A35[0,1]=-1",
                "A04[0,2]=+1", "A35[0,2]=-1",
            ],
            "minimal_new_cell_count_to_cancel_both_colour_words": 4,
            "pure_amplitudes": [1, 1, 1],
            "formal_triangle_guard_preserved": True,
            "cancelled_words": ["00001100", "00002200"],
            "remaining_mixed_violations": len(next_violations),
            "first_remaining": word_string(next_violations[0][0]),
            "normalized_X5": False,
        },
        "scope": {
            "general_off_support_dichotomy_proved": False,
            "minimal_two_cell_dichotomy_proved": True,
            "active_clean_cap_constructed": False,
            "degree_twelve_read": False,
            "broad_cegar": False,
            "full_conjecture_claim": False,
        },
    }
    temporary = HERE / "results_two_cell_dichotomy.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_two_cell_dichotomy.json")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
