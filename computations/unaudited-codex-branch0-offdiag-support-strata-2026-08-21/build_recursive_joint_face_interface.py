#!/usr/bin/env python3
"""Build the symmetry-complete recursive permanent-face interface.

A state is (B,T,D): the cofactor branch mask B, the selected permanent-term
mask T, and the edge support D on which both permanent terms remain live.
For a full edge e in D, setting the opposite entry to zero replaces the live
term on e and gives the boundary transition

    (B,T,D) -> (B,T xor {e},D minus {e}).

The full B4=C2^4 semidirect S4 action acts on B and T by the same endpoint
switches, while D is merely permuted.  Starting with B=0 gives 3^6 labelled
states but 66 joint B4 orbits.  This file is combinatorial routing only; it
does not assert that a boundary node is empty.
"""

from __future__ import annotations

from collections import Counter, deque
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_recursive_joint_face_interface.json"
EDGES = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
ACTIONS = tuple((switches, permutation)
                for switches in product((0, 1), repeat=4)
                for permutation in permutations(range(4)))
HARD_STARTS = (15, 30, 31, 63)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def act_mask(mask, switches, permutation, toggle):
    answer = 0
    for index, (left, right) in enumerate(EDGES):
        bit = (mask >> index) & 1
        if toggle:
            bit ^= switches[left] ^ switches[right]
        target = EDGE_INDEX[tuple(sorted((permutation[left],
                                          permutation[right])))]
        answer |= bit << target
    return answer


def act_state(state, action):
    branch, term, full = state
    switches, permutation = action
    return (act_mask(branch, switches, permutation, True),
            act_mask(term, switches, permutation, True),
            act_mask(full, switches, permutation, False))


def canonical(state):
    return min(act_state(state, action) for action in ACTIONS)


def state_key(state):
    return ":".join(str(value) for value in state)


def edge_list(mask):
    return [index for index in range(6) if mask >> index & 1]


def all_initial_states():
    # Type 0: offdiagonal only; 1: both terms; 2: diagonal only.
    states = []
    for types in product(range(3), repeat=6):
        term = sum((kind != 2) << edge for edge, kind in enumerate(types))
        full = sum((kind == 1) << edge for edge, kind in enumerate(types))
        states.append((0, term, full))
    require(len(states) == 3 ** 6, "labelled ternary state count changed")
    return tuple(states)


def transitions(state):
    branch, term, full = state
    return tuple(sorted({
        canonical((branch, term ^ (1 << edge), full ^ (1 << edge)))
        for edge in edge_list(full)
    }))


def reachable(start):
    seen = {start}
    queue = deque([start])
    while queue:
        current = queue.popleft()
        for target in transitions(current):
            if target not in seen:
                seen.add(target)
                queue.append(target)
    return frozenset(seen)


def main():
    require(len(ACTIONS) == 384, "B4 action count changed")
    labelled = all_initial_states()
    representatives = sorted({canonical(state) for state in labelled},
                             key=lambda state: (state[2].bit_count(), state))
    require(len(representatives) == 66,
            "recursive joint-face orbit count changed")
    require(Counter(state[2].bit_count() for state in representatives)
            == {0: 11, 1: 14, 2: 18, 3: 14, 4: 6, 5: 2, 6: 1},
            "recursive full-edge degree histogram changed")

    hard_reachable = {
        start: reachable(canonical((0, 63, start)))
        for start in HARD_STARTS
    }
    hard_union = frozenset().union(*hard_reachable.values())
    require([len(hard_reachable[start]) for start in HARD_STARTS]
            == [12, 6, 14, 11], "hard-start face counts changed")
    require(len(hard_union) == 43,
            "hard-start recursive union count changed")

    records = []
    for state in representatives:
        branch, term, full = state
        orbit = {act_state(state, action) for action in ACTIONS}
        record = {
            "key": state_key(state),
            "branch_mask": branch,
            "selected_term_mask": term,
            "both_live_edge_mask": full,
            "selected_term_edges": edge_list(term),
            "both_live_edges": edge_list(full),
            "both_live_degree": full.bit_count(),
            "orbit_size": len(orbit),
            "terminal_aligned": full == 0,
            "boundary_targets": [state_key(target)
                                 for target in transitions(state)],
            "reachable_from_hard_starts": [
                start for start in HARD_STARTS
                if state in hard_reachable[start]
            ],
        }
        records.append(record)

    result = {
        "status": "UNAUDITED exact recursive joint-face orbit interface",
        "edge_order": ["".join(map(str, edge)) for edge in EDGES],
        "group": "B4=C2^4 semidirect S4",
        "action_count": len(ACTIONS),
        "labelled_state_count": len(labelled),
        "joint_orbit_count": len(representatives),
        "both_live_degree_histogram": {
            str(degree): count for degree, count in sorted(
                Counter(state[2].bit_count()
                        for state in representatives).items())
        },
        "boundary_transition": "(B,T,D)->(B,T xor e,D minus e)",
        "hard_start_masks": list(HARD_STARTS),
        "hard_start_reachable_counts_including_start": {
            str(start): len(hard_reachable[start]) for start in HARD_STARTS
        },
        "hard_start_union_count_including_starts": len(hard_union),
        "terminal_aligned_orbit_count": sum(state[2] == 0
                                             for state in representatives),
        "records": records,
        "scope_guard": (
            "This is an exact symmetry/routing census only.  A partial "
            "c_e=0 face generally has D nonempty and is not covered merely "
            "because every D=0 terminal chart was previously classified."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("recursive branch/term/full-face interface: PASS")
    print("labelled / orbits / hard union:", len(labelled),
          len(representatives), len(hard_union))
    print("degree histogram:", result["both_live_degree_histogram"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
