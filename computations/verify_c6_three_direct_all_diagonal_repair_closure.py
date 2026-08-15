#!/usr/bin/env python3
"""Close every diagonal repair above the C6 three-direct seven-cell guard.

An exact diagonal six-site source containing the guard and a forced
cap-avoiding colour-one escape must contain one pure perfect matching in
each colour.  Enumerate all 15*12*15 labelled choices of such witnesses.
Every initial union has a mixed singleton.  A 4+2 singleton can only be
repaired by one of the other two pairings of its four equal-colour sites;
adjoin each possible mate and repeat.  A 2+2+2 singleton has no alternative
diagonal occurrence and is terminal.

The resulting finite monotone repair DAG has no singleton-free vertex:
every branch ends at a literal 2+2+2 Laurent unit.  Thus arbitrary
simultaneous diagonal mate additions do not evade the minimum-completion
gate.  This is stronger than support minimality in the declared diagonal
universe; the tight-cut derivative theorem is retained as the correct
fallback for any physical dependence, but is not needed to delete a cell.
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
    "computations/verify_c6_three_direct_minimal_pure_escape_unit_gate.py":
        "b6d27b3ecb69e1bc62f23d583c97cd026b1b2ec2d3050f1ed5ecba2cd32df263",
    "computations/verify_uniform_tight_cut_minimal_derivative_independence_gate.py":
        "69c0a995092c4cad6ffadbd82f00332ff27719b24b1f73d23583ac28245c14d2",
}
EXPECTED_LEDGER_SHA256 = (
    "a0bf20492be06f1e7dbc4b137d2b4129024a11783c0aeabad85ac1d4e002ef06"
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


def compatible_rows(base):
    rows = {}
    for word in product(base.COLOURS, repeat=len(base.VERTICES)):
        occurrences = []
        for matching in base.MATCHINGS:
            cells = base.occurrence_cells(matching, word)
            if cells is not None:
                occurrences.append((matching, cells))
        rows[word] = tuple(occurrences)
    return rows


def supported_occurrences(compatible, support, word):
    return tuple((matching, cells)
                 for matching, cells in compatible[word]
                 if cells <= support)


def word_profile(word):
    return tuple(sorted(Counter(word).values(), reverse=True))


def mixed_singletons(base, compatible, support):
    records = []
    for word in sorted(compatible):
        if len(set(word)) == 1:
            continue
        occurrences = supported_occurrences(compatible, support, word)
        if len(occurrences) != 1:
            continue
        matching, cells = occurrences[0]
        records.append({
            "word": base.word_name(word),
            "profile": word_profile(word),
            "fine": f"fine:{base.matching_name(matching)}",
            "operation": f"coefficient:{base.word_name(word)}",
            "decorated_cells": tuple(sorted(cells)),
            "cap": "34",
            "window": "0125",
            "tail": "tail:T",
        })
    return tuple(records)


def first_mixed_singleton(base, compatible, support):
    """Return the first record without materializing every later row."""
    for word in sorted(compatible):
        if len(set(word)) == 1:
            continue
        occurrences = supported_occurrences(compatible, support, word)
        if len(occurrences) != 1:
            continue
        matching, cells = occurrences[0]
        return {
            "word": base.word_name(word),
            "profile": word_profile(word),
            "fine": f"fine:{base.matching_name(matching)}",
            "operation": f"coefficient:{base.word_name(word)}",
            "decorated_cells": tuple(sorted(cells)),
            "cap": "34",
            "window": "0125",
            "tail": "tail:T",
        }
    return None


def initial_witness_supports(base, cap):
    residual = frozenset((
        base.edge(0, 5), base.edge(1, 2),
        base.edge(0, 1), base.edge(2, 5),
    ))
    guard = (frozenset((cap, colour) for colour in base.COLOURS)
             | frozenset((endpoints, 1) for endpoints in residual))
    cap_avoiding = tuple(matching for matching in base.MATCHINGS
                         if cap not in matching)
    require(len(guard) == 7 and len(cap_avoiding) == 12,
            (guard, cap_avoiding))

    supports = {}
    for zero, one, two in product(base.MATCHINGS, cap_avoiding,
                                  base.MATCHINGS):
        support = (guard
                   | frozenset((endpoints, 0) for endpoints in zero)
                   | frozenset((endpoints, 1) for endpoints in one)
                   | frozenset((endpoints, 2) for endpoints in two))
        witness = (zero, one, two)
        require(support not in supports, (support, supports.get(support), witness))
        supports[support] = witness
    require(len(supports) == 15 * 12 * 15, len(supports))
    return guard, residual, cap_avoiding, supports


def transform_support(base, support, vertex_action):
    return frozenset(
        (base.edge(vertex_action[left], vertex_action[right]), colour)
        for (left, right), colour in support
    )


def guard_stabilizer(base, cap, residual):
    core = {base.edge(0, 5), base.edge(1, 2)}
    mate = {base.edge(0, 1), base.edge(2, 5)}
    require(core | mate == residual, (core, mate, residual))
    actions = []
    for action in permutations(base.VERTICES):
        if (base.edge(action[cap[0]], action[cap[1]]) == cap
                and {base.edge(action[left], action[right])
                     for left, right in core} == core
                and {base.edge(action[left], action[right])
                     for left, right in mate} == mate):
            actions.append(action)
    require(len(actions) == 8, len(actions))
    return tuple(actions)


def orbit_ledger(base, supports, actions):
    universe = set(supports)
    unseen = set(supports)
    representatives = []
    histogram = Counter()
    while unseen:
        representative = min(unseen, key=lambda item: tuple(sorted(item)))
        orbit = {transform_support(base, representative, action)
                 for action in actions}
        require(orbit <= universe, (representative, orbit - universe))
        representatives.append(representative)
        histogram[len(orbit)] += 1
        unseen.difference_update(orbit)
    return {
        "orbits": len(representatives),
        "orbit_size_histogram": tuple(sorted(histogram.items())),
        "representatives": tuple(
            tuple(f"{left}{right};{colour}"
                  for (left, right), colour in sorted(support))
            for support in representatives
        ),
    }


def repair_closure(base, compatible, initial_supports):
    queue = deque(sorted(initial_supports,
                         key=lambda item: (len(item), tuple(sorted(item)))))
    seen = set(initial_supports)
    generated_by_size = Counter(map(len, initial_supports))
    terminal_by_size = Counter()
    branch_missing_size = Counter()
    unique_children = 0
    singleton_free = []
    terminal_example = None

    while queue:
        support = queue.popleft()
        selected = first_mixed_singleton(base, compatible, support)
        if selected is None:
            singleton_free.append(support)
            continue
        word = tuple(map(int, selected["word"]))
        selected_fine = selected["fine"].removeprefix("fine:")
        alternatives = []
        for matching, cells in compatible[word]:
            if base.matching_name(matching) == selected_fine:
                continue
            missing = cells - support
            if missing:
                alternatives.append(missing)

        if not alternatives:
            require(selected["profile"] == (2, 2, 2), selected)
            require(len(compatible[word]) == 1, (selected, compatible[word]))
            terminal_by_size[len(support)] += 1
            if terminal_example is None:
                terminal_example = selected
            continue

        require(selected["profile"] == (4, 2), selected)
        require(len(compatible[word]) == 3 and len(alternatives) == 2,
                (selected, compatible[word], alternatives))
        for missing in alternatives:
            require(len(missing) in (1, 2), (selected, missing))
            branch_missing_size[len(missing)] += 1
            child = support | missing
            if child in seen:
                continue
            seen.add(child)
            queue.append(child)
            generated_by_size[len(child)] += 1
            unique_children += 1

    require(not singleton_free, singleton_free)
    require(terminal_example is not None, terminal_example)
    require(sum(terminal_by_size.values()) > 0, terminal_by_size)
    return {
        "states": len(seen),
        "state_size_histogram": tuple(sorted(generated_by_size.items())),
        "maximum_state_cells": max(generated_by_size),
        "unique_children": unique_children,
        "repair_face_missing_cell_histogram": tuple(
            sorted(branch_missing_size.items())
        ),
        "terminal_rainbow_states": sum(terminal_by_size.values()),
        "terminal_size_histogram": tuple(sorted(terminal_by_size.items())),
        "singleton_free_states": 0,
        "terminal_example": terminal_example,
    }


def audit(base):
    cap = base.edge(3, 4)
    compatible = compatible_rows(base)
    guard, residual, cap_avoiding, initial = initial_witness_supports(base, cap)

    initial_size_histogram = Counter(map(len, initial))
    mixed_histogram = Counter()
    rainbow_histogram = Counter()
    no_rainbow = []
    for support in initial:
        singletons = mixed_singletons(base, compatible, support)
        require(singletons, support)
        mixed_histogram[len(singletons)] += 1
        rainbow_count = sum(record["profile"] == (2, 2, 2)
                            for record in singletons)
        rainbow_histogram[rainbow_count] += 1
        if not rainbow_count:
            no_rainbow.append(support)

    require(initial_size_histogram == Counter({
        13: 72, 14: 612, 15: 1440, 16: 576,
    }), initial_size_histogram)
    require(rainbow_histogram == Counter({
        0: 16, 1: 144, 2: 716, 3: 864,
        4: 572, 5: 304, 6: 76, 8: 8,
    }), rainbow_histogram)
    require(len(no_rainbow) == 16 and {len(item) for item in no_rainbow} == {15},
            (len(no_rainbow), Counter(map(len, no_rainbow))))

    actions = guard_stabilizer(base, cap, residual)
    exceptional_orbits = orbit_ledger(base, no_rainbow, actions)
    require((exceptional_orbits["orbits"],
             exceptional_orbits["orbit_size_histogram"]) == (2, ((8, 2),)),
            exceptional_orbits)
    for support in no_rainbow:
        records = mixed_singletons(base, compatible, support)
        require(records and all(record["profile"] == (4, 2)
                                for record in records), records)

    # Recover exactly the 3d78125 minimum subcensus: the colour-one witness
    # shares one old residual edge, and both other witnesses avoid the cap.
    minimum_subcensus = []
    for support, (zero, one, two) in initial.items():
        if (cap not in zero and cap not in two
                and len(set(one) & residual) == 1):
            minimum_subcensus.append(support)
    require(len(minimum_subcensus) == 1152
            and {len(item) for item in minimum_subcensus} == {15},
            (len(minimum_subcensus), Counter(map(len, minimum_subcensus))))
    require(all(mixed_singletons(base, compatible, support)
                for support in minimum_subcensus), "minimum packet lost unit")

    closure = repair_closure(base, compatible, initial)
    return {
        "fixed_labels": {
            "cap": "34",
            "window": "0125",
            "tail": "tail:T",
            "core_fine": "fine:05|12|34",
            "mate_fine": "fine:01|25|34",
            "operation": "literal diagonal coefficient row",
        },
        "guard_cells": len(guard),
        "pure_witness_choices": (15, 12, 15),
        "labelled_initial_witness_unions": len(initial),
        "initial_size_histogram": tuple(sorted(initial_size_histogram.items())),
        "initial_mixed_singleton_histogram": tuple(sorted(mixed_histogram.items())),
        "initial_rainbow_singleton_histogram": tuple(
            sorted(rainbow_histogram.items())
        ),
        "minimum_subcensus_from_3d78125": len(minimum_subcensus),
        "no_immediate_rainbow_packets": len(no_rainbow),
        "no_immediate_rainbow_orbits": exceptional_orbits,
        "all_no_rainbow_packets_have_4_plus_2_unit": True,
        "repair_closure": closure,
        "well_founded_potential": (
            "for a hypothetical singleton-free completion T and partial "
            "repair S subset T, rho_T(S)=|T\\S|; following a required "
            "4+2 mate strictly lowers rho until an unrepairable 2+2+2 row"
        ),
        "derivative_minimality_interface": (
            "if a live tight-cut physical derivative relation occurs, "
            "c8bc02f deletes a cell; the diagonal repair closure is stronger "
            "because its independent alternative also terminates in a unit"
        ),
        "theorem": (
            "no diagonal exact source, support-minimal or otherwise, can "
            "contain the seven-cell guard together with its forced "
            "cap-avoiding colour-one escape"
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
        "c6_all_diagonal_repair_base",
    )
    ledger = {
        "mode_independent": True,
        "dependencies": PINS,
        "audit": audit(base),
        "scope": (
            "all diagonal-cell supersets of the labelled seven-cell C6 "
            "guard after a cap-avoiding colour-one escape; arbitrary "
            "endpoint-offdiagonal repair cells are not enumerated"
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
    closure = result["repair_closure"]
    print("C6 three-direct all-diagonal repair closure: PASS")
    print("mode", arguments.mode)
    print("initial witness unions / minimum subcensus",
          result["labelled_initial_witness_unions"],
          result["minimum_subcensus_from_3d78125"])
    print("no-rainbow exceptional packets / orbits",
          result["no_immediate_rainbow_packets"],
          result["no_immediate_rainbow_orbits"]["orbits"])
    print("repair states / terminal rainbow states",
          closure["states"], closure["terminal_rainbow_states"])
    print("singleton-free diagonal completions",
          closure["singleton_free_states"])
    print("sha256:", digest)


if __name__ == "__main__":
    main()
