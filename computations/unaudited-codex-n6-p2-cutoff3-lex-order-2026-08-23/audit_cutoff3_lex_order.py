#!/usr/bin/env python3
"""Exact lex-monovariant audit of the frozen N6 cutoff-three DFS ledger."""

from __future__ import annotations

import argparse
import collections
import hashlib
import itertools
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "computations"))
VENV_SITE = (Path(sys.executable).absolute().parents[1] / "lib" /
             f"python{sys.version_info.major}.{sys.version_info.minor}" /
             "site-packages")
if VENV_SITE.is_dir():
    sys.path.append(str(VENV_SITE))

import lift_power2_offdiag2 as L  # noqa: E402


CERT = (ROOT / "computations" /
        "unaudited-codex-p2-k6-global-2026-08-23" / "cutoff3_dfs.txt")
OUT = HERE / "results_cutoff3_lex_order.json"
EXPECTED_CERT = "4985027e5f91bb462960f3e3dcd3c77edd181bc9e8ace1d938c7b506ff974222"
FEATURES = ("off_degree", "off_multiset", "diagonal_graph_code")


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def sha256_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decode_word(code):
    word = [0] * 6
    for index in range(5, -1, -1):
        word[index] = code % 3
        code //= 3
    return tuple(word)


def parse_packed(text):
    off_text, graph_text = text.split(" | ")
    fields = tuple(map(int, off_text.split()))
    degree = fields[0]
    require(len(fields) == degree + 1, "bad packed off degree")
    graphs = tuple(map(int, graph_text.split()))
    require(len(graphs) == 3, "bad packed graph triple")
    return fields[1:], graphs


def parse_certificate():
    require(sha256_file(CERT) == EXPECTED_CERT, "certificate hash changed")
    pivots = []
    with CERT.open(encoding="ascii") as stream:
        require(stream.readline().split() ==
                ["KRENN_P2_TRUNCATED_DFS_V1", "3", "663", "9528"],
                "certificate header changed")
        for line in stream:
            row_text, column_text, diagonal_text = line.rstrip().split(" || ")
            row = parse_packed(row_text.removeprefix("PIVOT "))
            word_text, multiplier_text = column_text.split(" ", 1)
            column = (decode_word(int(word_text)), *parse_packed(multiplier_text))
            pivots.append((row, column, int(diagonal_text)))
    require(len(pivots) == 9528, "pivot count changed")
    return pivots


def truncated_outputs(column, cutoff=3):
    word, off, graphs = column
    answer = []
    for matching in L.PM:
        term = L.term_variables(word, matching)
        row = L.canonical_row(*L.add_term(off, graphs, term))
        if len(row[0]) <= cutoff:
            answer.append(row)
    return tuple(answer)


def compare(left, right):
    return (left > right) - (left < right)


def row_features(row):
    off, graphs = row
    return {
        "off_degree": len(off),
        "off_multiset": off,
        "diagonal_graph_code": graphs,
    }


def render_row(row):
    return [list(row[0]), list(row[1])]


def render_column(column):
    return [list(column[0]), list(column[1]), list(column[2])]


def candidate_name(order, orientations):
    signs = {feature: ("+" if orientation == 1 else "-")
             for feature, orientation in zip(order, orientations)}
    return ">".join(signs[feature] + feature for feature in order)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    parser.add_argument("--mutate", action="store_true")
    args = parser.parse_args()

    pivots = parse_certificate()
    row_index = {row: index for index, (row, _column, _diagonal) in
                 enumerate(pivots)}
    require(len(row_index) == len(pivots), "pivot row repeated")
    edges = []
    pattern_count = collections.Counter()
    pattern_first = {}
    diagonal_count = collections.Counter()
    word_profiles = collections.Counter()
    for pivot_index, (pivot, column, diagonal) in enumerate(pivots):
        outputs = collections.Counter(truncated_outputs(column))
        require(outputs[pivot] == diagonal, "pivot diagonal replay changed")
        diagonal_count[diagonal] += 1
        profile = tuple(sorted(collections.Counter(column[0]).values(),
                               reverse=True))
        word_profiles[profile] += 1
        pivot_features = row_features(pivot)
        for dependency in sorted(outputs):
            if dependency == pivot:
                continue
            require(dependency in row_index, "dependency absent from ledger")
            dependency_index = row_index[dependency]
            require(dependency_index < pivot_index,
                    "certificate order stopped being well founded")
            dependency_features = row_features(dependency)
            pattern = tuple(compare(dependency_features[feature],
                                    pivot_features[feature])
                            for feature in FEATURES)
            edge = {
                "pivot_index": pivot_index,
                "dependency_index": dependency_index,
                "pivot": render_row(pivot),
                "dependency": render_row(dependency),
                "column": render_column(column),
                "column_word_profile": list(profile),
                "feature_sign_dependency_vs_pivot": dict(zip(FEATURES, pattern)),
            }
            edges.append(edge)
            pattern_count[pattern] += 1
            pattern_first.setdefault(pattern, edge)

    candidates = []
    for order in itertools.permutations(FEATURES):
        for orientations in itertools.product((-1, 1), repeat=len(FEATURES)):
            candidates.append((order, orientations))
    require(len(candidates) == 48, "candidate census changed")
    all_mask = (1 << len(candidates)) - 1
    satisfaction = {}
    violations = [0] * len(candidates)
    for pattern, count in pattern_count.items():
        mask = 0
        for index, (order, orientations) in enumerate(candidates):
            orientation = dict(zip(order, orientations))
            for feature in order:
                sign = pattern[FEATURES.index(feature)]
                if sign:
                    if sign * orientation[feature] < 0:
                        mask |= 1 << index
                    break
        satisfaction[pattern] = mask
        for index in range(len(candidates)):
            if not (mask >> index) & 1:
                violations[index] += count

    passing = [candidate_name(*candidate) for index, candidate in
               enumerate(candidates) if violations[index] == 0]
    ranked = sorted((count, candidate_name(*candidates[index]))
                    for index, count in enumerate(violations))

    # Find the minimum pattern witness whose violated-candidate masks cover
    # every tested lex order.  One or two patterns suffice in the frozen data.
    pattern_items = sorted(pattern_count)
    witness_patterns = None
    for pattern in pattern_items:
        if (all_mask ^ satisfaction[pattern]) == all_mask:
            witness_patterns = (pattern,)
            break
    if witness_patterns is None:
        choices = []
        for left_index, left in enumerate(pattern_items):
            left_bad = all_mask ^ satisfaction[left]
            for right in pattern_items[left_index:]:
                if left_bad | (all_mask ^ satisfaction[right]) == all_mask:
                    score = max(pattern_first[left]["pivot_index"],
                                pattern_first[right]["pivot_index"])
                    choices.append((score, left, right))
        if choices:
            _score, left, right = min(choices)
            witness_patterns = (left, right)
    require(witness_patterns is not None,
            "three-feature counterwitness grew beyond two edges")
    witness = [pattern_first[pattern] for pattern in witness_patterns]

    if args.mutate:
        require(passing, "hostile assertion that a lex monovariant exists survived")

    result = {
        "verdict": "NO_FIXED_LEX_MONOVARIANT_FROM_OFF_DEGREE_OFF_MULTISET_AND_DIAGONAL_GRAPH_CODE",
        "scope": "all dependency edges in the exact frozen cutoff3 DFS ledger",
        "certificate_sha256": EXPECTED_CERT,
        "pivots": len(pivots),
        "dependency_edges": len(edges),
        "pivot_diagonal_coefficients": dict(sorted(diagonal_count.items())),
        "pivot_word_profiles": {str(key): value for key, value in
                                sorted(word_profiles.items())},
        "tested_family": {
            "features": list(FEATURES),
            "priority_orders": 6,
            "independent_orientations": 8,
            "total_lex_orders": len(candidates),
            "word_profile_note": (
                "the source-word profile is constant between a pivot and "
                "every output dependency of its column, so inserting it at "
                "any lex priority cannot distinguish an edge"
            ),
        },
        "passing_orders": passing,
        "best_orders_by_violation_count": [
            {"violations": count, "order": name} for count, name in ranked[:8]
        ],
        "feature_sign_pattern_counts": {
            str(pattern): pattern_count[pattern] for pattern in pattern_items
        },
        "minimum_comparison_counterwitness": {
            "edges": len(witness),
            "interpretation": (
                "these dependency comparisons jointly force incompatible "
                "orientations on the first distinguishing feature for every "
                "tested priority order; this is a comparison cycle, not a "
                "cycle in the already-acyclic DFS dependency graph"
            ),
            "witness": witness,
        },
        "positive_order": {
            "name": "certificate collapse height",
            "definition": "the pivot index in cutoff3_dfs.txt",
            "strict_on_every_dependency": True,
            "human_readable_closed_formula_found": False,
        },
        "cutoff4_guard": (
            "not tested until a literal cutoff-four failing target/component "
            "artifact is exported; no extrapolation from cutoff three"
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = hashlib.sha256(logical.encode()).hexdigest()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_results:
        OUT.write_text(rendered, encoding="utf-8")
    if args.check_results:
        require(OUT.read_text(encoding="utf-8") == rendered,
                "frozen result differs")
    print(json.dumps({
        "dependency_edges": len(edges),
        "passing_orders": len(passing),
        "minimum_witness_edges": len(witness),
        "best_order": ranked[0],
        "logical_sha256": result["logical_sha256"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
