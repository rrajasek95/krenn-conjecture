#!/usr/bin/env python3
"""Finite audit of the 31 matching-triple geometries against the three-copy
alternating invariant.

This is deliberately a support/rank audit, not a coefficient solve.  For each
S8 x S3 orbit it constructs the canonical diagonal rank-respecting decorated
triple, enumerates its rainbow determinant terms and its supported coloured
perfect matchings, and records exactly which conclusions disappear after an
arbitrary source completion is allowed.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import product
import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ORBIT_PATH = ROOT / "computations" / "analyze_n8_full_s8s3_pure_product_membership.py"
SAT_BAND_PATH = (ROOT / "computations" /
                 "unaudited-template-kill-w8-2026-08-15" / "w8_band.py")
SAT_ENCODING_PATH = (ROOT / "computations" /
                     "unaudited-template-kill-w8-2026-08-15" / "w8_sat.py")
SUPPORT6_PATH = (ROOT / "computations" /
                 "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20" /
                 "results_support6_component_pairwise_obstruction.json")
SUPPORT8_PATH = (ROOT / "computations" /
                 "unaudited-codex-orbit0-t2-radical-2026-08-20" /
                 "results_forced_one_y_mate_unit_identity.json")
OUT = HERE / "results_three_copy_matching_orbits.json"
EXPECTED_LOGICAL_SHA256 = (
    "0987c5f409fb1e1d98ee446910ce89b69ce64e8f71e72914e1ffd9ac8c11c0c0"
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


SOURCE = load("three_copy_orbit_source", ORBIT_PATH)


def file_sha(path):
    return sha256(path.read_bytes()).hexdigest()


def logical_sha(value):
    return sha256(json.dumps(value, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def edge(u, v):
    return (u, v) if u < v else (v, u)


def matchings_from_row(row):
    mate = SOURCE.decode_key(row)
    answer = []
    for colour in range(3):
        matching = []
        for vertex in range(8):
            other = mate[3 * vertex + colour]
            require(other >= 0 and other % 3 == colour,
                    "pure triple row changed colour on an edge")
            other_vertex = other // 3
            if vertex < other_vertex:
                matching.append((vertex, other_vertex))
        require(len(matching) == 4, "decoded layer is not a perfect matching")
        answer.append(tuple(sorted(matching)))
    return tuple(answer)


def membership(matchings):
    answer = {}
    for colour, matching in enumerate(matchings):
        for item in matching:
            answer.setdefault(item, []).append(colour)
    return {item: tuple(colours) for item, colours in answer.items()}


def permutation_sign(values):
    require(tuple(sorted(values)) == (0, 1, 2),
            "local factor vectors are not a basis")
    inversions = sum(values[i] > values[j]
                     for i in range(3) for j in range(i + 1, 3))
    return -1 if inversions % 2 else 1


def rainbow_terms(matchings, member):
    """Evaluate Phi on the canonical diagonal rank witness.

    Each occurrence (slot, physical edge) can select any diagonal rank factor
    available on that physical edge.  The endpoint basis condition says the
    three selected colours at every vertex are distinct.  Integer +/- counts
    are the exact determinant expansion at unit factor weights.
    """

    occurrences = []
    for slot, matching in enumerate(matchings):
        for item in matching:
            occurrences.append((slot, item, member[item]))
    occurrences.sort(key=lambda item: (len(item[2]), item[0], item[1]))
    at_vertex = [[None, None, None] for _ in range(8)]
    positive = negative = 0

    def visit(index):
        nonlocal positive, negative
        if index == len(occurrences):
            sign = 1
            for values in at_vertex:
                sign *= permutation_sign(tuple(values))
            if sign == 1:
                positive += 1
            else:
                negative += 1
            return
        slot, (u, v), colours = occurrences[index]
        for colour in colours:
            if colour in at_vertex[u] or colour in at_vertex[v]:
                continue
            at_vertex[u][slot] = colour
            at_vertex[v][slot] = colour
            visit(index + 1)
            at_vertex[u][slot] = None
            at_vertex[v][slot] = None

    visit(0)
    require(positive + negative > 0,
            "canonical rank witness lost its original rainbow term")
    return positive, negative


def coloured_matching_fibres(member):
    fibres = Counter()
    supported_physical = []
    for matching in SOURCE.VERTEX_MATCHINGS:
        matching = tuple(sorted(edge(*item) for item in matching))
        if not all(item in member for item in matching):
            continue
        supported_physical.append(matching)
        for colours in product(*(member[item] for item in matching)):
            word = [None] * 8
            for (u, v), colour in zip(matching, colours):
                word[u] = colour
                word[v] = colour
            fibres[tuple(word)] += 1
    return tuple(sorted(set(supported_physical))), fibres


def component_partition(member):
    adjacency = [set() for _ in range(8)]
    for u, v in member:
        adjacency[u].add(v)
        adjacency[v].add(u)
    unseen = set(range(8))
    sizes = []
    while unseen:
        root = min(unseen)
        seen = {root}
        todo = [root]
        while todo:
            u = todo.pop()
            for v in adjacency[u]:
                if v not in seen:
                    seen.add(v)
                    todo.append(v)
        unseen -= seen
        sizes.append(len(seen))
    return tuple(sorted(sizes, reverse=True))


def record(row, index):
    matchings = matchings_from_row(row)
    member = membership(matchings)
    multiplicities = Counter(map(len, member.values()))
    # On edge e set A_e=sum_{c:e in M_c} e_c e_c^T.  Its rank is exactly the
    # multiplicity and the selected principal minor is the identity.
    require(all(len(colours) == len(set(colours)) for colours in member.values()),
            "an edge repeats a matching colour")
    positive, negative = rainbow_terms(matchings, member)
    require(positive - negative != 0,
            "canonical diagonal rank witness has vanishing Phi")

    physical, fibres = coloured_matching_fibres(member)
    pure_words = {(colour,) * 8 for colour in range(3)}
    require(all(fibres[word] == 1 for word in pure_words),
            "canonical diagonal witness changed a pure fibre")
    mixed = {word: count for word, count in fibres.items()
             if word not in pure_words}
    singleton = tuple(sorted(word for word, count in mixed.items() if count == 1))
    chosen_physical = set(matchings)
    alternatives = tuple(item for item in physical if item not in chosen_physical)
    stabilizer = SOURCE.stabilizer_order(row)
    require(SOURCE.GROUP_ORDER % stabilizer == 0,
            "stabilizer does not divide S8 x S3")
    return {
        "chart": index,
        "matchings": [[list(item) for item in matching] for matching in matchings],
        "orbit_size": SOURCE.GROUP_ORDER // stabilizer,
        "stabilizer": stabilizer,
        "simple_support_edges": len(member),
        "edge_multiplicity_histogram": {str(k): multiplicities[k]
                                         for k in sorted(multiplicities)},
        "component_partition": list(component_partition(member)),
        "rank_witness": {
            "edge_blocks": "A_e=diag(1_{e in M0},1_{e in M1},1_{e in M2})",
            "every_edge_rank_equals_multiplicity": True,
            "every_selected_repeated_edge_minor": 1,
            "every_vertex_local_vectors": ["e0", "e1", "e2"],
            "rainbow_terms_positive_negative": [positive, negative],
            "Phi_at_unit_diagonal_witness": positive - negative,
        },
        "supported_physical_matchings": len(physical),
        "fourth_physical_matchings": len(alternatives),
        "coloured_mixed_terms": sum(mixed.values()),
        "mixed_word_fibres": len(mixed),
        "mixed_singleton_words": len(singleton),
        "minimum_mixed_fibre": min(mixed.values()),
        "maximum_mixed_fibre": max(mixed.values()),
        "first_singleton_word": "".join(map(str, singleton[0])),
        "completion_scope": {
            "singleton_is_only_inside_12_cell_diagonal_subsupport": True,
            "arbitrary_extra_source_cells_can_add_terms_to_that_word": True,
            "forced_full_source_contradiction": False,
            "forced_literal_support6_support8_or_cap_signature": False,
        },
    }


def audit_sat_scope():
    band = SAT_BAND_PATH.read_text()
    encoding = SAT_ENCODING_PATH.read_text()
    require("enc.add([enc.cell_lit" in band,
            "SAT orbit case split no longer forces diagonal cell literals")
    require("self.cell = [[self.pool.id((\"c\", e, k))" in encoding,
            "SAT cell variables changed")
    require("rank>=m" not in band and "determinant" not in band,
            "SAT band unexpectedly claims a rank/minor constraint")
    return {
        "encoded": [
            "Boolean presence of every selected (c,c) cell",
            "existence of one diagonal perfect matching per colour",
            "support/FIE/no-singleton clauses",
        ],
        "not_encoded": [
            "the alternating invariant's factor-decorated witness triple",
            "linear independence of the three local factor vectors",
            "nonvanishing 2x2 or 3x3 minors on repeated edges",
            "identification of the invariant witness with the chosen pure triple",
        ],
        "reason": (
            "Cell-presence variables carry no coefficient values.  In particular, "
            "nonzero selected diagonal entries do not force their minor nonzero "
            "when off-diagonal entries are present."),
    }


def main():
    rows = tuple(sorted(SOURCE.target_orbit_rows()))
    require(len(rows) == 31, "matching-triple census is no longer 31")
    records = tuple(record(row, i) for i, row in enumerate(rows, 1))
    require(sum(item["orbit_size"] for item in records) == 105 ** 3,
            "the 31 orbit sizes do not exhaust ordered triples")
    require(all(item["rank_witness"]["Phi_at_unit_diagonal_witness"] != 0
                for item in records), "a rank-respecting orbit lost Phi")
    require(all(item["mixed_singleton_words"] > 0 for item in records),
            "a bare diagonal orbit ceased to have a mixed singleton")
    require(all(not item["completion_scope"]["forced_full_source_contradiction"]
                for item in records), "a local singleton was promoted globally")

    support6 = json.loads(SUPPORT6_PATH.read_text())
    support8 = json.loads(SUPPORT8_PATH.read_text())
    require((len(support6["x_support"]), len(support6["cofactor_support"]),
             len(support6["q_support"])) == (12, 4, 6),
            "frozen support6 signature changed")
    left8 = support8["fixed_left"]
    require((len(left8["entry_live_cells"]),
             len(left8["cofactor_live_cells"]), len(left8["Q_support"]))
            == (18, 8, 8), "frozen support8 signature changed")

    aggregates = {
        "orbits": len(records),
        "labelled_ordered_triples": sum(item["orbit_size"] for item in records),
        "rank_respecting_orbits": sum(
            item["rank_witness"]["every_edge_rank_equals_multiplicity"]
            for item in records),
        "bare_diagonal_orbits_with_mixed_singleton": sum(
            item["mixed_singleton_words"] > 0 for item in records),
        "bare_diagonal_orbits_with_every_mixed_term_singleton": sum(
            item["maximum_mixed_fibre"] == 1 for item in records),
        "orbits_with_a_fourth_physical_matching": sum(
            item["fourth_physical_matchings"] > 0 for item in records),
        "orbits_without_a_fourth_physical_matching": sum(
            item["fourth_physical_matchings"] == 0 for item in records),
        "orbits_with_repeated_edges": sum(
            item["simple_support_edges"] < 12 for item in records),
        "pairwise_edge_disjoint_orbits": sum(
            item["simple_support_edges"] == 12 for item in records),
        "pairwise_edge_disjoint_orbits_with_fourth_matching": sum(
            item["simple_support_edges"] == 12
            and item["fourth_physical_matchings"] > 0 for item in records),
        "edge_multiplicity_profile_histogram": {
            ";".join(f"m{k}:{v}" for k, v in
                     profile): count
            for profile, count in Counter(
                tuple(sorted(row["edge_multiplicity_histogram"].items()))
                for row in records).items()
        },
        "Phi_value_histogram": dict(sorted(Counter(
            item["rank_witness"]["Phi_at_unit_diagonal_witness"]
            for item in records).items())),
        "mixed_singleton_histogram": dict(sorted(Counter(
            item["mixed_singleton_words"] for item in records).items())),
        "fourth_matching_histogram": dict(sorted(Counter(
            item["fourth_physical_matchings"] for item in records).items())),
        "surviving_orbits_after_sound_full_source_consequences": 31,
    }
    result = {
        "status": "PASS exact 31-orbit rank-respecting rainbow audit",
        "sat_scope_audit": audit_sat_scope(),
        "aggregates": aggregates,
        "records": records,
        "literal_signature_audit": {
            "support6_X_C_Q_sizes": [12, 4, 6],
            "support8_X_C_Q_sizes": [18, 8, 8],
            "matching_geometry_forces_only": [
                "selected cells/minors nonzero",
                "no source cell, cofactor, Q, or H zero pattern",
            ],
            "unconditional_matches": 0,
            "explanation": (
                "The frozen mate units require full literal (X,C,Q,H) "
                "signatures.  A rank-respecting decorated triple is an open "
                "nonvanishing condition and forces none of their zero equations. "
                "Likewise a clean cap is not a graph-only consequence."),
        },
        "terminal_scope": {
            "surviving_matching_geometry_orbits": 31,
            "countermodel_to_orbit_exclusion": (
                "For every orbit set A_e=diag(1_{e in M0},1_{e in M1},"
                "1_{e in M2}) on the union and zero elsewhere.  It is exactly "
                "rank-respecting and its selected Phi is nonzero, so no graph "
                "orbit is excluded by the strengthened local consequence.  "
                "This is not a GHZ-source counterexample: its mixed singleton "
                "proves that the sparse completion is not GHZ.  Extra source "
                "edges can populate and cancel the same fibre."),
            "missing_bridge": (
                "A source-faithful localization theorem tying the invariant's "
                "decorated triple to a coefficient fibre or to a complete "
                "(X,C,Q,H) signature."),
        },
        "source_hashes": {str(path.relative_to(ROOT)): file_sha(path)
                          for path in (ORBIT_PATH, SAT_BAND_PATH,
                                       SAT_ENCODING_PATH, SUPPORT6_PATH,
                                       SUPPORT8_PATH)},
    }
    result["logical_sha256"] = logical_sha(result)
    if EXPECTED_LOGICAL_SHA256 != "TO_BE_FROZEN":
        require(result["logical_sha256"] == EXPECTED_LOGICAL_SHA256,
                "logical ledger digest changed")

    if "--mutate-drop-orbit" in sys.argv:
        require(len(records[:-1]) == 31, "mutation survived: dropped orbit")
    if "--mutate-promote-singleton" in sys.argv:
        require(any(item["completion_scope"]["forced_full_source_contradiction"]
                    for item in records),
                "mutation survived: local singleton promoted globally")
    if "--mutate-sat-has-rank" in sys.argv:
        require("determinant" in SAT_BAND_PATH.read_text(),
                "mutation survived: SAT falsely credited with minors")

    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if "--write-results" in sys.argv:
        OUT.write_text(text)
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
