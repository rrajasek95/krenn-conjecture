#!/usr/bin/env python3
"""Quotient diagonal C6 terminals and chase endpoint-coloured repairs.

The deterministic diagonal repair closure has 46,702 terminal supports.
Canonicalize them under the order-eight stabilizer of the labelled guard,
then process all eighteen equivalence classes at minimum support size 15.
Every class's cardinality-minimum endpoint-coloured repair exports a new
mixed singleton under complete 729-row replay.

On the most favourable class (six old singleton rows), the first genuinely
singleton-free endpoint-coloured extension occurs at sixteen new cells.
Its fifty mixed fibres are all binomials.  Three of them--the parent row
111001 and two of the thirteen S-chain exit geometries--have exponent
differences d1-d2+d3=0 but each ratio is -1.  Hence 1=-1 in the source
torus.  The occurrence recurrence is not an exact full-row counterguard.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
from hashlib import sha256
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_c6_oriented_complementary_face_naturality.py":
        "7d0fb2cc5d1a722eddfdafaa155f2346fc62c531fe0a33c28abaf8a537b6e980",
    "computations/verify_c6_three_direct_all_diagonal_repair_closure.py":
        "08945a657c7b39c3182e93adebfe465974582768c21fb461b6a2c9db2b542815",
    "computations/verify_c6_three_direct_minimum_offdiagonal_repair_unit.py":
        "7396af7a1bd8d128e3df2f26db89e5467f686c510eabc2b9f03d14db17139a12",
    "computations/verify_c6_unspecialized_eqsystem_parent_antidiagonal_spair.py":
        "584c36d076224fcc437b70998a43091ffa0f19b35bfbe73fea0caf1d7ae9865a",
}
EXPECTED_LEDGER_SHA256 = (
    "6da72ee0f61c61f5bb69c199d709059025b99649b2e8b55678c2ce4c2e0cda72"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def diagonal_terminal_census(base, diagonal):
    compatible = diagonal.compatible_rows(base)
    cap = base.edge(3, 4)
    _guard, residual, _cap_avoiding, initial = (
        diagonal.initial_witness_supports(base, cap)
    )
    actions = diagonal.guard_stabilizer(base, cap, residual)
    queue = deque(sorted(initial,
                         key=lambda item: (len(item), tuple(sorted(item)))))
    seen = set(initial)
    terminals = []
    while queue:
        support = queue.popleft()
        selected = diagonal.first_mixed_singleton(base, compatible, support)
        require(selected is not None, ("diagonal survivor", support))
        word = tuple(map(int, selected["word"]))
        fine = selected["fine"].removeprefix("fine:")
        alternatives = []
        for matching, cells in compatible[word]:
            if base.matching_name(matching) == fine:
                continue
            missing = cells - support
            if missing:
                alternatives.append(missing)
        if not alternatives:
            require(selected["profile"] == (2, 2, 2), selected)
            terminals.append(support)
            continue
        for missing in alternatives:
            child = support | missing
            if child not in seen:
                seen.add(child)
                queue.append(child)

    size_histogram = Counter(map(len, terminals))
    require(len(terminals) == 46702, len(terminals))
    require(size_histogram == Counter({
        15: 68, 16: 76, 17: 127, 18: 293, 19: 626,
        20: 1118, 21: 1655, 22: 2882, 23: 4330, 24: 6482,
        25: 8679, 26: 9093, 27: 6730, 28: 3164, 29: 1199,
        30: 169, 31: 11,
    }), size_histogram)

    # The deterministic "first singleton" terminal list is not invariant
    # under the guard action: another image can be terminal but reached by a
    # different repair order.  Quotient its elements by their canonical
    # full guard orbit key rather than requiring every image to be listed.
    groups = defaultdict(list)
    for support in terminals:
        key = min(
            (diagonal.transform_support(base, support, action)
             for action in actions),
            key=lambda item: tuple(sorted(item)),
        )
        groups[key].append(support)
    representatives = tuple(sorted(
        groups, key=lambda item: (len(item), tuple(sorted(item)))
    ))
    class_size_histogram = Counter(map(len, representatives))
    require(len(representatives) == 21483, len(representatives))
    require(class_size_histogram == Counter({
        15: 18, 16: 32, 17: 58, 18: 117, 19: 257,
        20: 430, 21: 611, 22: 1087, 23: 1770, 24: 2688,
        25: 3686, 26: 4395, 27: 3613, 28: 1846, 29: 740,
        30: 124, 31: 11,
    }), class_size_histogram)
    minimum = tuple(item for item in representatives if len(item) == 15)
    require(len(minimum) == 18, len(minimum))
    return compatible, actions, terminals, groups, representatives, minimum


def minimum_class_repairs(base, diagonal, offdiagonal, compatible, minimum):
    ledgers = []
    for index, support in enumerate(minimum):
        diagonal_rows = {
            word: diagonal.supported_occurrences(compatible, support, word)
            for word in compatible
        }
        old_singletons = tuple(
            offdiagonal.singleton_record(
                base, word,
                (matching,
                 frozenset((endpoints, word[endpoints[0]],
                            word[endpoints[1]])
                           for endpoints in matching)),
            )
            for word, occurrences in sorted(diagonal_rows.items())
            if len(set(word)) > 1 and len(occurrences) == 1
            for matching, _cells in occurrences
        )
        full_support = frozenset(
            (endpoints, colour, colour) for endpoints, colour in support
        )
        candidate_rows = tuple(
            offdiagonal.repair_candidates(base, full_support, singleton)[0]
            for singleton in old_singletons
        )
        budget, packets, search = offdiagonal.solve_minimum_union(candidate_rows)
        packet_audit = offdiagonal.packet_ledger(
            base, full_support, old_singletons, packets
        )
        require(packet_audit["minimum_new_singletons"] > 0,
                (index, support, packet_audit))
        support_names = tuple(
            offdiagonal.diagonal_name(item) for item in sorted(support)
        )
        ledgers.append({
            "class": index,
            "support_sha256": sha256(
                json.dumps(support_names, separators=(",", ":")).encode()
            ).hexdigest(),
            "old_singletons": len(old_singletons),
            "old_profile": tuple(sorted(Counter(
                tuple(item["profile"]) for item in old_singletons
            ).items())),
            "minimum_repair_cells": budget,
            "minimum_packets": len(packets),
            "minimum_new_singletons": packet_audit["minimum_new_singletons"],
            "new_singleton_histogram":
                packet_audit["new_singleton_count_histogram"],
            "search_certificate": search,
        })

    require(tuple(item["minimum_repair_cells"] for item in ledgers) == (
        7, 7, 9, 8, 8, 8, 5, 5, 8, 8, 8, 8, 8, 8, 7, 9, 8, 7,
    ), ledgers)
    require(tuple(item["minimum_packets"] for item in ledgers) == (
        8, 2, 48, 24, 6, 24, 2, 2, 8,
        8, 6, 24, 168, 168, 8, 48, 24, 2,
    ), ledgers)
    require(tuple(item["minimum_new_singletons"] for item in ledgers) == (
        9, 20, 10, 18, 21, 18, 12, 12, 23,
        23, 21, 18, 18, 18, 9, 10, 18, 20,
    ), ledgers)
    return tuple(ledgers)


def parse_full_cell(value):
    endpoints, colours = value.split(";")
    return (int(endpoints[0]), int(endpoints[1])), int(colours[0]), int(colours[1])


RECURRENT_ADDITIONS = (
    "13;02", "13;10", "13;12", "13;21",
    "14;01", "14;20",
    "15;00", "15;10", "15;22",
    "23;11", "34;02", "34;20",
    "35;02", "35;10", "45;12", "45;20",
)


def occurrence_pair(base, rows, word):
    occurrences = rows[word]
    require(len(occurrences) == 2, (word, occurrences))
    records = []
    for matching, cells in occurrences:
        records.append({
            "matching": base.matching_name(matching),
            "cells": tuple(
                f"{left}{right};{left_colour}{right_colour}"
                for (left, right), left_colour, right_colour in sorted(cells)
            ),
            "cell_set": cells,
        })
    return tuple(records)


def exponent_difference(first, second):
    answer = Counter(first)
    answer.subtract(second)
    return Counter({cell: coefficient for cell, coefficient in answer.items()
                    if coefficient})


def bipartite_permutation(matching, left_part, right_part):
    right_index = {vertex: index for index, vertex in enumerate(right_part)}
    neighbours = {}
    for first, second in matching:
        if first in left_part and second in right_part:
            neighbours[first] = second
        elif second in left_part and first in right_part:
            neighbours[second] = first
        else:
            raise RuntimeError(("not a bipartite matching", matching,
                                left_part, right_part))
    require(set(neighbours) == set(left_part), (matching, neighbours))
    return tuple(right_index[neighbours[vertex]] for vertex in left_part)


def permutation_parity(permutation):
    inversions = sum(
        permutation[left] > permutation[right]
        for left in range(len(permutation))
        for right in range(left + 1, len(permutation))
    )
    return inversions % 2


def recurrent_signed_exit_audit(base, offdiagonal, spair, minimum):
    seed = minimum[6]
    expected_seed = (
        "01;1", "02;0", "02;2", "03;1", "05;1",
        "12;1", "13;0", "14;1", "14;2", "25;1",
        "34;0", "34;1", "34;2", "35;2", "45;0",
    )
    require(tuple(offdiagonal.diagonal_name(item) for item in sorted(seed)) ==
            expected_seed, seed)
    full_seed = frozenset(
        (endpoints, colour, colour) for endpoints, colour in seed
    )
    additions = frozenset(map(parse_full_cell, RECURRENT_ADDITIONS))
    require(len(additions) == 16 and additions.isdisjoint(full_seed), additions)
    support = full_seed | additions
    rows = offdiagonal.full_rows(base, support)
    singletons = offdiagonal.mixed_singletons(base, rows)
    require(not singletons, singletons)
    occurrence_histogram = Counter()
    for word, occurrences in rows.items():
        occurrence_histogram[("pure" if len(set(word)) == 1 else "mixed",
                              len(occurrences))] += 1
    require(occurrence_histogram == Counter({
        ("mixed", 2): 50, ("pure", 2): 2, ("pure", 4): 1,
    }), occurrence_histogram)

    relation_words = (
        tuple(map(int, "101111")),
        tuple(map(int, "111001")),
        tuple(map(int, "111100")),
    )
    relation_coefficients = (1, -1, 1)
    pairs = tuple(occurrence_pair(base, rows, word)
                  for word in relation_words)
    expected_matchings = (
        ("03|14|25", "05|14|23"),
        ("01|25|34", "05|12|34"),
        ("01|23|45", "03|12|45"),
    )
    require(tuple(tuple(item["matching"] for item in pair) for pair in pairs) ==
            expected_matchings, pairs)
    total_difference = Counter()
    row_records = []
    for word, coefficient, pair in zip(
            relation_words, relation_coefficients, pairs, strict=True):
        difference = exponent_difference(
            pair[0]["cell_set"], pair[1]["cell_set"]
        )
        for cell, exponent in difference.items():
            total_difference[cell] += coefficient * exponent
        row_records.append({
            "word": base.word_name(word),
            "relation_coefficient": coefficient,
            "first_matching": pair[0]["matching"],
            "first_cells": pair[0]["cells"],
            "second_matching": pair[1]["matching"],
            "second_cells": pair[1]["cells"],
            "typed_face": "parent anti-diagonal" if word == relation_words[1]
                          else "C4 exit binomial",
        })
    require(not +total_difference, total_difference)
    require(sum(relation_coefficients) % 2 == 1,
            relation_coefficients)

    exit_names = {
        spair.matching_name(matching) for matching in spair.MATCHINGS
        if matching not in (spair.M0, spair.M1)
    }
    used_exit_names = set(expected_matchings[0] + expected_matchings[2])
    require(used_exit_names <= exit_names,
            (used_exit_names, exit_names))
    spectator_tails = []
    for pair in (pairs[0], pairs[2]):
        first = next(matching for matching in base.MATCHINGS
                     if base.matching_name(matching) == pair[0]["matching"])
        second = next(matching for matching in base.MATCHINGS
                      if base.matching_name(matching) == pair[1]["matching"])
        common = set(first) & set(second)
        require(len(common) == 1 and len(set(first) ^ set(second)) == 4,
                (first, second, common))
        tail_left, tail_right = next(iter(common))
        spectator_tails.append(f"{tail_left}{tail_right}")
    require(tuple(spectator_tails) == ("14", "45"), spectator_tails)

    # With the middle row inverted by its relation coefficient, the positive
    # and negative fines are the two parity classes of all six permutation
    # matchings of one K3,3.  Their products therefore use every edge once.
    matching_by_name = {
        base.matching_name(matching): matching for matching in base.MATCHINGS
    }
    positive_names = (
        expected_matchings[0][0], expected_matchings[1][1],
        expected_matchings[2][0],
    )
    negative_names = (
        expected_matchings[0][1], expected_matchings[1][0],
        expected_matchings[2][1],
    )
    left_part = (0, 2, 4)
    right_part = (1, 3, 5)
    positive_permutations = tuple(
        bipartite_permutation(matching_by_name[name], left_part, right_part)
        for name in positive_names
    )
    negative_permutations = tuple(
        bipartite_permutation(matching_by_name[name], left_part, right_part)
        for name in negative_names
    )
    require(tuple(map(permutation_parity, positive_permutations)) == (0, 0, 0),
            positive_permutations)
    require(tuple(map(permutation_parity, negative_permutations)) == (1, 1, 1),
            negative_permutations)
    all_cross_edges = {
        base.edge(left, right) for left in left_part for right in right_part
    }
    require(Counter(edge for name in positive_names
                    for edge in matching_by_name[name]) ==
            Counter(all_cross_edges), positive_names)
    require(Counter(edge for name in negative_names
                    for edge in matching_by_name[name]) ==
            Counter(all_cross_edges), negative_names)

    return {
        "seed_minimum_class": 6,
        "seed_cells": len(seed),
        "added_endpoint_cells": len(additions),
        "added_cells": RECURRENT_ADDITIONS,
        "total_cells": len(support),
        "singleton_free": True,
        "complete_row_occurrence_histogram": tuple(
            sorted(occurrence_histogram.items())
        ),
        "signed_relation_rows": tuple(row_records),
        "exponent_identity": "d_101111-d_111001+d_111100=0",
        "ratio_identity": "(-1)*(-1)^(-1)*(-1)=-1, but monomials give 1",
        "thirteen_exit_geometries_used": tuple(sorted(used_exit_names)),
        "c4_exit_spectator_tails": tuple(spectator_tails),
        "permanent_triangle": {
            "bipartition": (left_part, right_part),
            "even_fines": positive_names,
            "even_permutations": positive_permutations,
            "odd_fines": negative_names,
            "odd_permutations": negative_permutations,
            "edge_product_identity": (
                "product(even permutation fines)="
                "product(odd permutation fines)"
            ),
        },
        "uniform_tail_scope": (
            "a single row-independent nonzero perfect-matching spectator "
            "tail tensors through and cancels; changing tails are not covered"
        ),
        "source_verdict": "Laurent unit 1=-1; not an exact source packet",
    }


def cell_universe(base):
    edges = tuple(combinations(base.VERTICES, 2))
    cells = tuple((edge, left_colour, right_colour)
                  for edge in edges
                  for left_colour, right_colour in product(base.COLOURS,
                                                            repeat=2))
    return edges, cells, {cell: index for index, cell in enumerate(cells)}


def singleton_free_smt(base, seed, relation, exact):
    _edges, cells, cell_index = cell_universe(base)
    base_cells = frozenset(
        (endpoints, colour, colour) for endpoints, colour in seed
    )
    free = tuple(index for index, cell in enumerate(cells)
                 if cell not in base_cells)
    lines = [
        "(set-option :produce-models true)",
        "(declare-const cost Int)",
    ]
    lines.extend(f"(declare-const x{index} Bool)"
                 for index in range(len(cells)))
    lines.extend(f"(assert x{cell_index[cell]})" for cell in sorted(base_cells))
    lines.append("(assert (= cost (+ " + " ".join(
        f"(ite x{index} 1 0)" for index in free
    ) + ")))")
    for word in product(base.COLOURS, repeat=len(base.VERTICES)):
        if len(set(word)) == 1:
            continue
        occurrence_names = []
        word_label = base.word_name(word)
        for matching_index, matching in enumerate(base.MATCHINGS):
            variables = []
            for endpoints in matching:
                left, right = endpoints
                variables.append(
                    f"x{cell_index[(endpoints, word[left], word[right])]}"
                )
            name = f"y{word_label}_{matching_index}"
            lines.append(f"(declare-const {name} Bool)")
            lines.append(f"(assert (= {name} (and {' '.join(variables)})))")
            occurrence_names.append(name)
        for index, name in enumerate(occurrence_names):
            others = " ".join(item for offset, item
                               in enumerate(occurrence_names)
                               if offset != index)
            lines.append(f"(assert (or (not {name}) {others}))")
    operator = "=" if exact else "<="
    lines.extend((f"(assert ({operator} cost {relation}))", "(check-sat)"))
    return "\n".join(lines) + "\n"


def exhaustive_minimality_check(base, seed):
    records = []
    for relation, exact in ((14, False), (15, True)):
        program = singleton_free_smt(base, seed, relation, exact)
        result = subprocess.run(
            ("z3", "-in"), input=program, text=True,
            capture_output=True, timeout=60, check=False,
        )
        require(result.returncode == 0 and result.stdout.strip() == "unsat",
                (relation, exact, result.returncode,
                 result.stdout[-1000:], result.stderr[-1000:]))
        records.append({
            "constraint": f"cost {'=' if exact else '<='} {relation}",
            "result": "unsat",
            "smt_sha256": sha256(program.encode()).hexdigest(),
        })
    return tuple(records)


def build_ledger(base, diagonal, offdiagonal, spair):
    compatible, actions, terminals, groups, representatives, minimum = (
        diagonal_terminal_census(base, diagonal)
    )
    first_layer = minimum_class_repairs(
        base, diagonal, offdiagonal, compatible, minimum
    )
    recurrent = recurrent_signed_exit_audit(
        base, offdiagonal, spair, minimum
    )
    smt_programs = (
        ("cost<=14", sha256(singleton_free_smt(
            base, minimum[6], 14, False
        ).encode()).hexdigest()),
        ("cost=15", sha256(singleton_free_smt(
            base, minimum[6], 15, True
        ).encode()).hexdigest()),
    )
    return {
        "terminal_quotient": {
            "guard_stabilizer_order": len(actions),
            "deterministic_terminal_states": len(terminals),
            "terminal_size_histogram": tuple(sorted(Counter(
                map(len, terminals)
            ).items())),
            "canonical_equivalence_classes": len(representatives),
            "class_size_histogram": tuple(sorted(Counter(
                map(len, representatives)
            ).items())),
            "minimum_terminal_cells": 15,
            "minimum_classes": len(minimum),
            "deterministic_list_is_guard_invariant": False,
            "quotient_definition": (
                "canonical full guard-orbit key on each listed terminal; "
                "observed class fibres may be proper subsets of an orbit"
            ),
        },
        "all_minimum_class_first_repairs": first_layer,
        "all_minimum_classes_export_singletons": True,
        "minimum_occurrence_recurrence": {
            **recurrent,
            "exact_minimum_added_cells": 16,
            "minimality_smt_program_hashes": smt_programs,
            "minimality_certificate": (
                "cost<=14 UNSAT and cost=15 UNSAT; displayed cost16 packet"
            ),
        },
        "scope": (
            "all eighteen minimum-size diagonal terminal equivalence classes "
            "through their cardinality-minimum endpoint-coloured repair; "
            "one exact-minimum recurrent repair DAG seed through its signed "
            "thirteen-exit Laurent closure. Larger terminal classes and "
            "nonminimum repairs of the other seventeen classes are not closed."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="structural")
    parser.add_argument("--dump-ledger", action="store_true")
    arguments = parser.parse_args()
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    base = load(
        "computations/verify_uniform_c6_oriented_complementary_face_naturality.py",
        "c6_terminal_orbit_base",
    )
    diagonal = load(
        "computations/verify_c6_three_direct_all_diagonal_repair_closure.py",
        "c6_terminal_orbit_diagonal",
    )
    offdiagonal = load(
        "computations/verify_c6_three_direct_minimum_offdiagonal_repair_unit.py",
        "c6_terminal_orbit_offdiagonal",
    )
    spair = load(
        "computations/verify_c6_unspecialized_eqsystem_parent_antidiagonal_spair.py",
        "c6_terminal_orbit_spair",
    )
    ledger = {
        "mode_independent": True,
        "dependencies": PINS,
        "audit": build_ledger(base, diagonal, offdiagonal, spair),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger changed", digest, EXPECTED_LEDGER_SHA256))
    solver_records = ()
    if arguments.mode == "exhaustive":
        _, _, _, _, _, minimum = diagonal_terminal_census(base, diagonal)
        solver_records = exhaustive_minimality_check(base, minimum[6])
    if arguments.dump_ledger:
        print(json.dumps(ledger, indent=2, sort_keys=True))

    audit = ledger["audit"]
    quotient = audit["terminal_quotient"]
    recurrence = audit["minimum_occurrence_recurrence"]
    print("C6 terminal orbit/offdiagonal signed-exit gate: PASS")
    print("mode", arguments.mode)
    print("terminal states / canonical classes / minimum classes",
          quotient["deterministic_terminal_states"],
          quotient["canonical_equivalence_classes"],
          quotient["minimum_classes"])
    print("minimum classes with singleton-exporting first repairs",
          len(audit["all_minimum_class_first_repairs"]))
    print("first occurrence recurrence / signed source verdict",
          recurrence["exact_minimum_added_cells"],
          recurrence["source_verdict"])
    if solver_records:
        print("exhaustive z3 minimality replay", solver_records)
    print("sha256:", digest)


if __name__ == "__main__":
    main()
