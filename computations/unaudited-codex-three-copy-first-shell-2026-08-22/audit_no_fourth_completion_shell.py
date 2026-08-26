#!/usr/bin/env python3
"""Exact one-/two-cell completion shell for the 12 no-fourth matching charts.

The base source has only the twelve diagonal cells selected by its matching
triple.  Every mixed output term is then a literal singleton.  For each such
word this checker enumerates every other perfect matching and records the
one- or two-cell deficits that would supply a cancellation mate.  It then
exhausts every off-support singleton/pair addition and asks whether all base
singleton fibres can be repaired simultaneously.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations
import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PREV_SCRIPT = (ROOT / "computations" /
    "unaudited-codex-three-copy-31-rank-audit-2026-08-22" /
    "audit_three_copy_matching_orbits.py")
PREV_RESULT = PREV_SCRIPT.parent / "results_three_copy_matching_orbits.json"
OUT = HERE / "results_no_fourth_completion_shell.json"
EXPECTED_LOGICAL_SHA256 = (
    "717b6c79c51c1ea396641d425253316a4c649be70281a8319c5fcbea6014c12f"
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


BASE = load("three_copy_base_audit", PREV_SCRIPT)
SOURCE = BASE.SOURCE
EDGES = tuple(combinations(range(8), 2))
EDGE_INDEX = {item: i for i, item in enumerate(EDGES)}
ALL_CELLS = frozenset(range(28 * 9))


def file_sha(path):
    return sha256(path.read_bytes()).hexdigest()


def logical_sha(value):
    return sha256(json.dumps(value, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def cell(u, v, a, b):
    if u > v:
        u, v, a, b = v, u, b, a
    return 9 * EDGE_INDEX[(u, v)] + 3 * a + b


def decode_cell(value):
    edge_index, entry = divmod(value, 9)
    a, b = divmod(entry, 3)
    u, v = EDGES[edge_index]
    return u, v, a, b


def base_support(matchings):
    return frozenset(cell(u, v, colour, colour)
                     for colour, matching in enumerate(matchings)
                     for u, v in matching)


def term_support(word, matching):
    return frozenset(cell(u, v, word[u], word[v]) for u, v in matching)


def base_fibres(support):
    fibres = Counter()
    for word_number in range(3 ** 8):
        value = word_number
        word = []
        for _ in range(8):
            word.append(value % 3)
            value //= 3
        word = tuple(word)
        for matching in SOURCE.VERTEX_MATCHINGS:
            if term_support(word, matching) <= support:
                fibres[word] += 1
    return fibres


def transform_cell(value, vertex_permutation, colour_permutation):
    u, v, a, b = decode_cell(value)
    return cell(vertex_permutation[u], vertex_permutation[v],
                colour_permutation[a], colour_permutation[b])


def stabilizer_actions(support):
    actions = []
    for sigma in permutations(range(3)):
        for vertex_permutation in permutations(range(8)):
            image = frozenset(transform_cell(value, vertex_permutation, sigma)
                              for value in support)
            if image == support:
                actions.append((vertex_permutation, sigma))
    return tuple(actions)


def orbit_count(sets, actions):
    unseen = set(sets)
    count = 0
    while unseen:
        seed = unseen.pop()
        orbit = {
            frozenset(transform_cell(value, vertex_permutation, sigma)
                      for value in seed)
            for vertex_permutation, sigma in actions
        }
        unseen -= orbit
        count += 1
    return count


def chart_audit(row, old_record):
    matchings = BASE.matchings_from_row(row)
    support = base_support(matchings)
    require(len(support) == 12, "selected diagonal occurrence cells collided")
    fibres = base_fibres(support)
    pure = {(c,) * 8 for c in range(3)}
    singleton_words = tuple(sorted(word for word, count in fibres.items()
                                   if word not in pure and count == 1))
    require(len(singleton_words) == old_record["mixed_singleton_words"],
            "base singleton count disagrees with 31-orbit ledger")
    require(old_record["fourth_physical_matchings"] == 0,
            "first-shell audit received a fourth-matching chart")

    chosen_physical = set(matchings)
    interfaces = {}
    direction_to_words = {}
    direction_to_matchings = {}
    for word in singleton_words:
        existing = tuple(matching for matching in SOURCE.VERTEX_MATCHINGS
                         if term_support(word, matching) <= support)
        require(len(existing) == 1, "base word is not a literal singleton")
        deficits = set()
        for matching in SOURCE.VERTEX_MATCHINGS:
            if matching == existing[0]:
                continue
            missing = term_support(word, matching) - support
            if 1 <= len(missing) <= 2:
                deficits.add(missing)
                direction_to_words.setdefault(missing, set()).add(word)
                direction_to_matchings.setdefault(missing, set()).add(matching)
                # Completing a distinct word-matching term necessarily makes
                # its physical perfect matching live.  In these 12 charts it
                # cannot already be a fourth matching of the simple union.
                physical = tuple(sorted(matching))
                if physical not in chosen_physical:
                    pass
                else:
                    # A chosen physical layer can carry a mixed word only via
                    # repeated-edge colours.  It is still a new coloured term,
                    # while its support is not a new physical fourth matching.
                    # Record this sharp exception rather than overclaiming.
                    pass
        interfaces[word] = deficits

    off = tuple(sorted(ALL_CELLS - support))
    single_hits = {value: set() for value in off}
    pair_hits = {}
    for direction, words in direction_to_words.items():
        if len(direction) == 1:
            single_hits[next(iter(direction))].update(words)
        else:
            pair_hits[direction] = set(words)
    best_one = len(singleton_words) - max(map(len, single_hits.values()))
    best_two_cancelled = 0
    for a, b in combinations(off, 2):
        direction = frozenset((a, b))
        hits = single_hits[a] | single_hits[b] | pair_hits.get(direction, set())
        best_two_cancelled = max(best_two_cancelled, len(hits))
    best_two = len(singleton_words) - best_two_cancelled
    require(best_one > 0 and best_two > 0,
            "a <=2-cell completion repaired every literal singleton")

    actual_directions = tuple(direction_to_words)
    actions = stabilizer_actions(support)
    require(len(actions) == old_record["stabilizer"],
            "literal cell stabilizer disagrees with orbit ledger")

    directions_new_physical = 0
    directions_only_chosen_physical = 0
    for direction, matching_set in direction_to_matchings.items():
        if any(tuple(sorted(matching)) not in chosen_physical
               for matching in matching_set):
            directions_new_physical += 1
        else:
            directions_only_chosen_physical += 1

    one_interfaces = tuple(item for item in actual_directions if len(item) == 1)
    two_interfaces = tuple(item for item in actual_directions if len(item) == 2)
    return {
        "chart": old_record["chart"],
        "base_singleton_words": len(singleton_words),
        "off_support_cells": len(off),
        "linear_interfaces": len(one_interfaces),
        "quadratic_interfaces": len(two_interfaces),
        "linear_interface_orbits": orbit_count(one_interfaces, actions),
        "quadratic_interface_orbits": orbit_count(two_interfaces, actions),
        "stabilizer": len(actions),
        "directions_completing_a_new_physical_matching": directions_new_physical,
        "directions_using_only_a_chosen_physical_layer":
            directions_only_chosen_physical,
        "best_remaining_base_singletons_after_one_cell": best_one,
        "best_remaining_base_singletons_after_two_cells": best_two,
        "maximum_base_singletons_cancelled_by_one_cell":
            len(singleton_words) - best_one,
        "maximum_base_singletons_cancelled_by_two_cells":
            len(singleton_words) - best_two,
        "all_linear_and_quadratic_additions_retain_a_literal_singleton": True,
        "cap_audit_needed_for_shell_exclusion": False,
        "cap_scope": (
            "Clean-cap activity depends on coefficient equations, not only "
            "cell support.  It is not inferred: the retained literal singleton "
            "already excludes every <=2-cell shell completion."),
    }


def main():
    previous = json.loads(PREV_RESULT.read_text())
    require(previous["logical_sha256"] ==
            "0987c5f409fb1e1d98ee446910ce89b69ce64e8f71e72914e1ffd9ac8c11c0c0",
            "31-orbit parent ledger changed")
    rows = tuple(sorted(SOURCE.target_orbit_rows()))
    old_records = tuple(previous["records"])
    selected = tuple((row, record) for row, record in zip(rows, old_records)
                     if record["fourth_physical_matchings"] == 0)
    require(len(selected) == 12, "no-fourth residual is no longer 12 charts")
    records = tuple(chart_audit(row, record) for row, record in selected)
    require(all(item["all_linear_and_quadratic_additions_retain_a_literal_singleton"]
                for item in records), "a first-shell residual survived")

    result = {
        "status": "PASS exact no-fourth one-/two-cell completion shell",
        "charts": [item["chart"] for item in records],
        "records": records,
        "aggregates": {
            "no_fourth_charts": len(records),
            "linear_interfaces": sum(item["linear_interfaces"] for item in records),
            "quadratic_interfaces": sum(item["quadratic_interfaces"]
                                         for item in records),
            "linear_interface_orbits": sum(item["linear_interface_orbits"]
                                            for item in records),
            "quadratic_interface_orbits": sum(item["quadratic_interface_orbits"]
                                               for item in records),
            "quadratic_interfaces_completing_new_physical_matching": sum(
                item["directions_completing_a_new_physical_matching"]
                for item in records),
            "quadratic_interfaces_using_chosen_physical_layer": sum(
                item["directions_using_only_a_chosen_physical_layer"]
                for item in records),
            "minimum_remaining_literal_singletons_after_two_cells": min(
                item["best_remaining_base_singletons_after_two_cells"]
                for item in records),
            "charts_closed_through_first_quadratic_shell_by_literal_singleton":
                sum(item["all_linear_and_quadratic_additions_retain_a_literal_singleton"]
                    for item in records),
        },
        "exact_structural_statement": (
            "For a fixed word and matching, a monomial is determined by its "
            "four source cells.  Therefore the listed one-/two-cell deficits "
            "are the exhaustive linear/quadratic mate interfaces.  Across "
            "every off-support addition of size at most two, at least one "
            "original literal mixed singleton remains.  Whenever an interface "
            "uses a new physical matching, completing it explicitly supplies "
            "the fourth matching; chosen-layer colour alternatives are counted "
            "separately and still leave another singleton."),
        "scope_guard": (
            "This closes only the one-cell and first two-cell support shells "
            "around the twelve canonical diagonal witnesses.  It does not "
            "exclude larger completions, does not identify the invariant "
            "witness with a pure localization chart, and does not infer cap "
            "activity from support."),
        "source_hashes": {
            str(PREV_SCRIPT.relative_to(ROOT)): file_sha(PREV_SCRIPT),
            str(PREV_RESULT.relative_to(ROOT)): file_sha(PREV_RESULT),
        },
    }
    result["logical_sha256"] = logical_sha(result)
    if EXPECTED_LOGICAL_SHA256 != "TO_BE_FROZEN":
        require(result["logical_sha256"] == EXPECTED_LOGICAL_SHA256,
                "logical first-shell ledger changed")

    if "--mutate-drop-chart" in sys.argv:
        require(len(records[:-1]) == 12, "mutation survived: dropped chart")
    if "--mutate-promote-fourth" in sys.argv:
        require(all(item["directions_using_only_a_chosen_physical_layer"] == 0
                    for item in records),
                "mutation survived: every interface called a physical fourth")
    if "--mutate-ignore-singleton" in sys.argv:
        require(any(item["best_remaining_base_singletons_after_two_cells"] == 0
                    for item in records),
                "mutation survived: retained singleton ignored")

    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if "--write-results" in sys.argv:
        OUT.write_text(text)
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
