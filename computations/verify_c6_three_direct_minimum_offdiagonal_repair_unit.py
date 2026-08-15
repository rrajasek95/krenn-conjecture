#!/usr/bin/env python3
"""Classify the first endpoint-offdiagonal repairs of a terminal C6 fibre.

Regenerate the 68 smallest (15-cell) terminal states from the diagonal
repair closure and choose the canonical labelled support.  It has eight
mixed singleton rows.  For each row enumerate all fourteen alternative
perfect matchings with literal endpoint-colour cells, then solve the exact
minimum-union problem for a packet supplying at least one mate per row.

The unrestricted endpoint-coloured minimum has seven cells: five genuinely
offdiagonal and two diagonal.  There are eight packets.  If every added cell
is required to be endpoint-offdiagonal, the minimum is eight and there are
twenty-four packets.  Complete expansion of all 729 output words shows that
every minimum packet exports new literal mixed singleton rows.
"""

from __future__ import annotations

import argparse
from collections import Counter, deque
from hashlib import sha256
import importlib.util
from itertools import permutations, product
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_c6_oriented_complementary_face_naturality.py":
        "7d0fb2cc5d1a722eddfdafaa155f2346fc62c531fe0a33c28abaf8a537b6e980",
    "computations/verify_c6_three_direct_all_diagonal_repair_closure.py":
        "08945a657c7b39c3182e93adebfe465974582768c21fb461b6a2c9db2b542815",
}
EXPECTED_LEDGER_SHA256 = (
    "a17084a3c8d72febc289ff16dcfe3f5c48dc25a3c26c81cd9c2b8db3e30333c7"
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


def cell_name(selected):
    (left, right), left_colour, right_colour = selected
    return f"{left}{right};{left_colour}{right_colour}"


def diagonal_name(selected):
    (left, right), colour = selected
    return f"{left}{right};{colour}"


def full_cell(endpoints, word):
    left, right = endpoints
    return endpoints, word[left], word[right]


def smallest_terminal_states(base, diagonal):
    compatible = diagonal.compatible_rows(base)
    cap = base.edge(3, 4)
    _guard, _residual, _cap_avoiding, initial = (
        diagonal.initial_witness_supports(base, cap)
    )
    queue = deque(sorted(
        (support for support in initial if len(support) <= 15),
        key=lambda support: (len(support), tuple(sorted(support))),
    ))
    seen = set(queue)
    terminals = []
    while queue:
        support = queue.popleft()
        selected = diagonal.first_mixed_singleton(base, compatible, support)
        require(selected is not None,
                ("unexpected singleton-free state at <=15 cells", support))
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
            if len(child) <= 15 and child not in seen:
                seen.add(child)
                queue.append(child)

    require(len(terminals) == 68 and {len(item) for item in terminals} == {15},
            (len(terminals), Counter(map(len, terminals))))
    canonical = min(terminals, key=lambda item: tuple(sorted(item)))
    expected = (
        "01;1", "01;2", "02;0", "03;1", "05;1",
        "12;1", "13;0", "14;1", "23;1", "25;1",
        "25;2", "34;0", "34;1", "34;2", "45;0",
    )
    require(tuple(diagonal_name(item) for item in sorted(canonical)) == expected,
            tuple(diagonal_name(item) for item in sorted(canonical)))
    return compatible, tuple(sorted(terminals,
                                    key=lambda item: tuple(sorted(item)))), canonical


def full_rows(base, support):
    rows = {}
    for word in product(base.COLOURS, repeat=len(base.VERTICES)):
        occurrences = []
        for matching in base.MATCHINGS:
            cells = frozenset(full_cell(endpoints, word)
                              for endpoints in matching)
            if cells <= support:
                occurrences.append((matching, cells))
        if occurrences:
            rows[word] = tuple(occurrences)
    return rows


def singleton_record(base, word, occurrence):
    matching, cells = occurrence
    return {
        "word": base.word_name(word),
        "profile": tuple(sorted(Counter(word).values(), reverse=True)),
        "fine": f"fine:{base.matching_name(matching)}",
        "operation": f"coefficient:{base.word_name(word)}",
        "cells": tuple(cell_name(item) for item in sorted(cells)),
        "parent_cap": "34",
        "parent_window": "0125",
        "tail": "tail:T",
    }


def mixed_singletons(base, rows):
    return tuple(
        singleton_record(base, word, occurrences[0])
        for word, occurrences in sorted(rows.items())
        if len(set(word)) > 1 and len(occurrences) == 1
    )


def repair_candidates(base, diagonal_support, singleton):
    word = tuple(map(int, singleton["word"]))
    selected_fine = singleton["fine"].removeprefix("fine:")
    candidates = []
    for matching in base.MATCHINGS:
        if base.matching_name(matching) == selected_fine:
            continue
        occurrence = frozenset(full_cell(endpoints, word)
                               for endpoints in matching)
        missing = occurrence - diagonal_support
        require(missing, (singleton, matching, occurrence))
        candidates.append((missing, matching))
    require(len(candidates) == 14, (singleton, candidates))

    # A strict superset can be omitted in a cardinality-minimum union: its
    # smaller candidate already repairs this row, and any useful extra cell
    # must also occur in a candidate selected for another row.
    minimal = tuple(
        (missing, matching) for missing, matching in candidates
        if not any(other < missing for other, _ in candidates)
    )
    offdiagonal = tuple(
        (missing, matching) for missing, matching in minimal
        if all(left_colour != right_colour
               for _endpoints, left_colour, right_colour in missing)
    )
    require(offdiagonal, singleton)
    return minimal, offdiagonal


def solve_minimum_union(candidate_rows):
    candidates = tuple(tuple(sorted(
        {missing for missing, _matching in row},
        key=lambda item: (len(item), tuple(sorted(item))),
    )) for row in candidate_rows)

    def satisfied(selected):
        return frozenset(
            index for index, row in enumerate(candidates)
            if any(candidate <= selected for candidate in row)
        )

    # Deterministic greedy bound; exact depth-limited search below proves
    # every smaller cardinality impossible.
    selected = frozenset()
    while len(satisfied(selected)) < len(candidates):
        done = satisfied(selected)
        choices = []
        for index in set(range(len(candidates))) - set(done):
            for candidate in candidates[index]:
                child = selected | candidate
                gain = len(satisfied(child) - done)
                choices.append((-gain, len(child - selected),
                                tuple(sorted(candidate)), child))
        selected = min(choices)[3]
    upper_bound = len(selected)
    lower_bound = max(min(len(item) for item in row) for row in candidates)

    budget_audit = []
    for budget in range(lower_bound, upper_bound + 1):
        memo = set()
        solutions = set()
        calls = 0

        def search(current):
            nonlocal calls
            calls += 1
            if len(current) > budget or current in memo:
                return
            memo.add(current)
            done = satisfied(current)
            if len(done) == len(candidates):
                solutions.add(current)
                return
            choices = []
            for index in set(range(len(candidates))) - set(done):
                viable = tuple(
                    item for item in candidates[index]
                    if len(current | item) <= budget
                )
                if not viable:
                    return
                score = (len(viable),
                         -min(len(item - current) for item in viable), index)
                choices.append((score, index, viable))
            _score, _index, viable = min(choices)
            for item in sorted(viable,
                               key=lambda value: (
                                   len(value - current), tuple(sorted(value))
                               )):
                search(current | item)

        search(frozenset())
        budget_audit.append((budget, calls, len(memo), len(solutions)))
        if solutions:
            ordered = tuple(sorted(solutions,
                                   key=lambda item: tuple(sorted(item))))
            require(all(len(item) == budget for item in ordered), ordered)
            return budget, ordered, tuple(budget_audit)
    raise RuntimeError(("greedy upper bound failed", upper_bound, budget_audit))


def packet_ledger(base, diagonal_support, old_singletons, packets):
    old_words = {tuple(map(int, item["word"])) for item in old_singletons}
    count_histogram = Counter()
    type_histogram = Counter()
    ledgers = []
    for packet in packets:
        support = diagonal_support | packet
        rows = full_rows(base, support)
        require(all(word in rows and len(rows[word]) >= 2
                    for word in old_words), (packet, old_words, rows))
        new_singletons = mixed_singletons(base, rows)
        require(new_singletons, packet)
        count_histogram[len(new_singletons)] += 1
        cell_type = (
            sum(left_colour != right_colour
                for _endpoints, left_colour, right_colour in packet),
            sum(left_colour == right_colour
                for _endpoints, left_colour, right_colour in packet),
        )
        type_histogram[cell_type] += 1
        ledgers.append({
            "packet": tuple(cell_name(item) for item in sorted(packet)),
            "offdiagonal_diagonal_cells": cell_type,
            "old_singletons_all_mated": True,
            "new_singletons": len(new_singletons),
            "first_new_singleton": new_singletons[0],
        })
    best = min(ledgers, key=lambda item: (
        item["new_singletons"], item["packet"]
    ))
    return {
        "packets": len(packets),
        "cell_type_histogram": tuple(sorted(type_histogram.items())),
        "new_singleton_count_histogram": tuple(sorted(count_histogram.items())),
        "minimum_new_singletons": best["new_singletons"],
        "sharp_packet": best,
        "packet_registry": tuple(ledgers),
    }


def audit(base, diagonal):
    compatible, terminal_states, canonical = smallest_terminal_states(
        base, diagonal
    )
    stabilizer = tuple(
        action for action in permutations(base.VERTICES)
        if frozenset(
            (base.edge(action[left], action[right]), colour)
            for (left, right), colour in canonical
        ) == canonical
    )
    require(stabilizer == (tuple(base.VERTICES),), stabilizer)
    diagonal_rows = {
        word: diagonal.supported_occurrences(compatible, canonical, word)
        for word in compatible
    }
    old_singletons = tuple(
        singleton_record(
            base, word,
            (matching,
             frozenset((endpoints, word[endpoints[0]], word[endpoints[1]])
                       for endpoints in matching)),
        )
        for word, occurrences in sorted(diagonal_rows.items())
        if len(set(word)) > 1 and len(occurrences) == 1
        for matching, _cells in occurrences
    )
    require(len(old_singletons) == 8, old_singletons)
    require(Counter(tuple(item["profile"]) for item in old_singletons) ==
            Counter({(4, 2): 5, (2, 2, 2): 3}), old_singletons)

    full_diagonal_support = frozenset(
        (endpoints, colour, colour) for endpoints, colour in canonical
    )
    candidate_rows = tuple(
        repair_candidates(base, full_diagonal_support, singleton)
        for singleton in old_singletons
    )
    candidate_profile = tuple({
        "word": singleton["word"],
        "minimal_candidates": len(candidates[0]),
        "offdiagonal_only_candidates": len(candidates[1]),
        "minimal_missing_cell_histogram": tuple(sorted(Counter(
            len(missing) for missing, _matching in candidates[0]
        ).items())),
    } for singleton, candidates in zip(old_singletons, candidate_rows,
                                        strict=True))

    all_budget, all_packets, all_search = solve_minimum_union(
        tuple(item[0] for item in candidate_rows)
    )
    off_budget, off_packets, off_search = solve_minimum_union(
        tuple(item[1] for item in candidate_rows)
    )
    require((all_budget, len(all_packets), off_budget, len(off_packets)) ==
            (7, 8, 8, 24),
            (all_budget, len(all_packets), off_budget, len(off_packets)))
    require(all(sum(left_colour != right_colour
                    for _endpoints, left_colour, right_colour in packet) == 5
                and sum(left_colour == right_colour
                        for _endpoints, left_colour, right_colour in packet) == 2
                for packet in all_packets), all_packets)
    require(all(all(left_colour != right_colour
                    for _endpoints, left_colour, right_colour in packet)
                for packet in off_packets), off_packets)

    all_ledger = packet_ledger(
        base, full_diagonal_support, old_singletons, all_packets
    )
    off_ledger = packet_ledger(
        base, full_diagonal_support, old_singletons, off_packets
    )
    require(all_ledger["new_singleton_count_histogram"] == (
        (9, 1), (20, 1), (22, 1), (23, 1),
        (25, 2), (33, 1), (38, 1),
    ), all_ledger)
    require(off_ledger["new_singleton_count_histogram"] == (
        (16, 1), (17, 1), (18, 2), (19, 2), (20, 4), (21, 4),
        (22, 2), (23, 1), (24, 1), (25, 1), (26, 1), (27, 1),
        (29, 1), (30, 1), (33, 1),
    ), off_ledger)
    sharp = all_ledger["sharp_packet"]
    require(sharp["packet"] == (
        "02;12", "02;21", "05;22", "12;22",
        "13;21", "15;12", "15;21",
    ), sharp)
    require(sharp["first_new_singleton"] == {
        "word": "010002",
        "profile": (4, 1, 1),
        "fine": "fine:02|15|34",
        "operation": "coefficient:010002",
        "cells": ("02;00", "15;12", "34;00"),
        "parent_cap": "34",
        "parent_window": "0125",
        "tail": "tail:T",
    }, sharp)

    return {
        "terminal_states_at_minimum_size": len(terminal_states),
        "canonical_labelled_stabilizer_order": len(stabilizer),
        "canonical_terminal_support": tuple(
            diagonal_name(item) for item in sorted(canonical)
        ),
        "canonical_terminal_mixed_singletons": old_singletons,
        "candidate_profile": candidate_profile,
        "minimum_general_endpoint_packet": {
            "cells": all_budget,
            "packets": len(all_packets),
            "search_certificate": all_search,
            "full_row_audit": all_ledger,
        },
        "minimum_strictly_offdiagonal_packet": {
            "cells": off_budget,
            "packets": len(off_packets),
            "search_certificate": off_search,
            "full_row_audit": off_ledger,
        },
        "theorem": (
            "every minimum endpoint-coloured repair of the canonical "
            "smallest terminal diagonal state exports a literal mixed "
            "singleton under complete 729-row replay"
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
        "c6_minimum_offdiagonal_base",
    )
    diagonal = load(
        "computations/verify_c6_three_direct_all_diagonal_repair_closure.py",
        "c6_minimum_offdiagonal_diagonal_closure",
    )
    ledger = {
        "mode_independent": True,
        "dependencies": PINS,
        "audit": audit(base, diagonal),
        "scope": (
            "minimum endpoint-coloured packets mating every mixed singleton "
            "of the canonical one among 68 smallest diagonal terminal states; "
            "larger packets and the other 67 terminal states are not closed"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger changed", digest, EXPECTED_LEDGER_SHA256))
    if arguments.dump_ledger:
        print(json.dumps(ledger, indent=2, sort_keys=True))

    result = ledger["audit"]
    general = result["minimum_general_endpoint_packet"]
    strict = result["minimum_strictly_offdiagonal_packet"]
    print("C6 minimum endpoint-offdiagonal repair unit gate: PASS")
    print("mode", arguments.mode)
    print("smallest terminal states / old singletons",
          result["terminal_states_at_minimum_size"],
          len(result["canonical_terminal_mixed_singletons"]))
    print("general minimum cells / packets / min new singletons",
          general["cells"], general["packets"],
          general["full_row_audit"]["minimum_new_singletons"])
    print("strict offdiagonal cells / packets / min new singletons",
          strict["cells"], strict["packets"],
          strict["full_row_audit"]["minimum_new_singletons"])
    print("sha256:", digest)


if __name__ == "__main__":
    main()
