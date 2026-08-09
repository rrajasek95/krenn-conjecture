#!/usr/bin/env python3
"""Refine the 16 shared-reciprocal low-rank forms by head labels and ranks.

The omission pair is combined with the four reciprocal head labels
    A_pq = lambda E_{b,a},  A_pr = mu E_{d,c},  a != c.
The checker quotients simultaneous colour relabelling and q<->r exchange,
audits the exact diagonal-routing masks, and constructs every endpoint-star
rank pattern not ruled out by equality of the two shared-p endpoint lines.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path

import verify_shared_reciprocal_fourcover_overlap as overlap


ROOT = Path(__file__).resolve().parents[1]
COLORS = (0, 1, 2)
PINS = {
    "computations/verify_shared_reciprocal_fourcover_overlap.py":
        "03c70295b5c72393dda96de0987d88978de768110d0484955e90d983bd1d6851",
    "computations/verify_n8_rankone_good_curvature_selection.py":
        "f66f3acf359ee24fe96b7bb61c91f5d75f3c76d14075cb818bd8562bc72547ac",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency drift: {relative}")


def transform_packet(packet, color_permutation, exchange):
    state, a, c, b, d = packet
    state = overlap.transform_state(state, color_permutation, exchange)
    a, c, b, d = (color_permutation[a], color_permutation[c],
                  color_permutation[b], color_permutation[d])
    if exchange:
        a, c, b, d = c, a, d, b
    return state, a, c, b, d


def canonical_packet(packet):
    return min(
        transform_packet(packet, color_permutation, exchange)
        for color_permutation in permutations(COLORS)
        for exchange in (False, True)
    )


def combined_packets():
    maps = overlap.balanced_omission_maps()
    states = {
        overlap.state_from_maps(left, right)
        for left in maps for right in maps
    }
    raw = (
        (state, a, c, b, d)
        for state in states
        for a in COLORS for c in COLORS if a != c
        for b in COLORS for d in COLORS
    )
    packets = tuple(sorted({canonical_packet(packet) for packet in raw}))
    require(len(packets) == 477,
            "combined omission/head-label orbit count changed")
    require(all(a != c for _state, a, c, _b, _d in packets),
            "shared endpoint repeated an outgoing target colour")
    return packets


def required_chord_diagonals(packet):
    state, a, c, b, d = packet
    omitted_r, omitted_q = state[:2]
    required = set()
    if not (a == b == omitted_q):
        required.add(omitted_q)
    if not (c == d == omitted_r):
        required.add(omitted_r)
    return frozenset(required)


def endpoint_rank(lines, deleted_index):
    full = len(set(lines))
    deleted = len(set(lines[:deleted_index] + lines[deleted_index + 1:]))
    require(full == 3, "endpoint star lost target-flattening rank three")
    return deleted


def realize_shared_endpoint_ranks(b, d, desired_pq, desired_pr):
    """Construct seven coordinate lines at p with the requested deletions."""

    require(desired_pq in (2, 3) and desired_pr in (2, 3),
            "invalid deleted-star rank")
    if b == d:
        require((desired_pq, desired_pr) == (3, 3),
                "equal shared lines cannot be deletion-essential")
        other = [color for color in COLORS if color != b]
        lines = [b, d, other[0], other[1], b, b, b]
    else:
        third = (set(COLORS) - {b, d}).pop()
        lines = [b, d]
        lines += [b] * (desired_pq == 3)
        lines += [d] * (desired_pr == 3)
        lines.append(third)
        lines += [third] * (7 - len(lines))
    require(endpoint_rank(lines, 0) == desired_pq,
            "pq deletion-rank realization failed")
    require(endpoint_rank(lines, 1) == desired_pr,
            "pr deletion-rank realization failed")
    return tuple(lines)


def realize_outer_endpoint_rank(direct_axis, omitted, desired, chord_forced):
    """Realize the coordinate-plane core plus its opposite chord.

    The five common-core blocks span the plane omitting `omitted`.  A forced
    chord diagonal in that colour is transverse and makes the deleted star
    rank three.  If it is not forced, the direct reciprocal block is itself
    diagonal in `omitted`, and the chord may lie in or outside the plane.
    """

    plane = [color for color in COLORS if color != omitted]
    require(not chord_forced or desired == 3,
            "forced chord diagonal failed to make outer star injective")
    if desired == 2:
        require(direct_axis == omitted and not chord_forced,
                "rank-two outer star lacks its direct missing-axis factor")
        chord_axis = plane[0]
    else:
        require(desired == 3, "invalid outer deleted-star rank")
        chord_axis = omitted
    lines = [direct_axis, chord_axis,
             plane[0], plane[1], plane[0], plane[1], plane[0]]
    require(endpoint_rank(lines, 0) == desired,
            "outer deletion-rank realization failed")
    return tuple(lines)


def rank_pattern_audit(packets):
    incoming_equal = 0
    branch_rows = 0
    curved_rows = 0
    residual_rows = 0
    for _state, a, c, b, d in packets:
        if b == d:
            incoming_equal += 1
            p_patterns = ((3, 3),)
        else:
            p_patterns = tuple(product((2, 3), repeat=2))
        for rank_pq_p, rank_pr_p in p_patterns:
            realize_shared_endpoint_ranks(
                b, d, rank_pq_p, rank_pr_p
            )
            required = required_chord_diagonals((_state, a, c, b, d))
            omitted_r, omitted_q = _state[:2]
            q_patterns = (3,) if omitted_q in required else (2, 3)
            r_patterns = (3,) if omitted_r in required else (2, 3)
            for rank_pq_q, rank_pr_r in product(q_patterns, r_patterns):
                realize_outer_endpoint_rank(
                    a, omitted_q, rank_pq_q, omitted_q in required
                )
                realize_outer_endpoint_rank(
                    c, omitted_r, rank_pr_r, omitted_r in required
                )
                minimum_chord_rank = int(bool(required))
                for chord_rank in range(minimum_chord_rank, 4):
                    branch_rows += 1
                    both_good = (
                        rank_pq_p == rank_pq_q == 3
                        and rank_pr_p == rank_pr_r == 3
                    )
                    # Pinned flat-wedge theorem: if the shared p-lines are
                    # proportional (b=d), flatness needs chord rank>=2; if
                    # independent, it needs chord rank=3.
                    flat_rank_threshold = 2 if b == d else 3
                    forced_curved = both_good and chord_rank < flat_rank_threshold
                    if forced_curved:
                        curved_rows += 1
                    else:
                        residual_rows += 1
    require(incoming_equal == 159,
            "equal shared-head-label orbit count changed")
    expected = (5223, 804, 4419)
    require((branch_rows, curved_rows, residual_rows) == expected,
            f"rank/chord branch census changed: "
            f"{(branch_rows, curved_rows, residual_rows)}")
    return incoming_equal, branch_rows, curved_rows, residual_rows


def packet_census(packets):
    chord_histogram = Counter(len(required_chord_diagonals(packet))
                              for packet in packets)
    require(chord_histogram == {0: 9, 1: 214, 2: 254},
            f"opposite-chord routing census changed: {chord_histogram}")
    mismatch_histogram = Counter(
        (overlap.mismatch_count(state), state[0] == state[1])
        for state, _a, _c, _b, _d in packets
    )
    expected_mismatch = {
        (0, True): 15,
        (1, False): 30,
        (2, False): 30, (2, True): 42,
        (3, False): 84, (3, True): 30,
        (4, False): 114, (4, True): 42,
        (5, False): 60, (5, True): 30,
    }
    require(mismatch_histogram == expected_mismatch,
            f"head-labelled mismatch census changed: {mismatch_histogram}")

    zero = tuple(packet for packet in packets
                 if overlap.mismatch_count(packet[0]) == 0)
    require(len(zero) == 15,
            "zero-mismatch head-label packet count changed")
    zero_incoming_equal = sum(b == d for _state, _a, _c, b, d in zero)
    zero_one_direct = sum(
        int(a == b == state[1]) + int(c == d == state[0]) == 1
        for state, a, c, b, d in zero
    )
    require((zero_incoming_equal, zero_one_direct) == (5, 3),
            "aligned-orbit endpoint-label refinement changed")
    require(all(required_chord_diagonals(packet) == {packet[0][0]}
                for packet in zero),
            "aligned orbit lost its forced opposite-chord diagonal")
    return chord_histogram, mismatch_histogram, len(zero), (
        zero_incoming_equal, zero_one_direct
    )


def main():
    pin_dependencies()
    packets = combined_packets()
    chord_histogram, mismatch_histogram, zero_count, zero_flags = (
        packet_census(packets)
    )
    incoming_equal, branch_rows, curved_rows, residual_rows = (
        rank_pattern_audit(packets)
    )
    ledger = {
        "combined_orbits": len(packets),
        "incoming_equal_orbits": incoming_equal,
        "required_chord_diagonal_histogram": dict(sorted(chord_histogram.items())),
        "mismatch_exception_histogram": {
            f"{mismatch},{int(same)}": count
            for (mismatch, same), count in sorted(mismatch_histogram.items())
        },
        "zero_mismatch_orbits": zero_count,
        "zero_mismatch_incoming_equal": zero_flags[0],
        "zero_mismatch_one_direct_aligned": zero_flags[1],
        "rank_chord_branch_rows": branch_rows,
        "forced_curved_rows": curved_rows,
        "finite_residual_rows": residual_rows,
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    expected = "2b1bfdbc2dc543ef1118dbc4bedf69b478471535adae10c341f3b06f35f649f8"
    require(digest == expected,
            f"shared reciprocal head-label ledger changed: {digest}")
    print("shared reciprocal low-rank head-label refinement: PASS")
    print("combined omission/head-label orbits:", len(packets))
    print("opposite-chord diagonal requirements:",
          dict(sorted(chord_histogram.items())))
    print("zero-mismatch endpoint packets:", zero_count)
    print("rank/chord rows: curved", curved_rows,
          "finite residual", residual_rows)
    print("sha256:", digest)


if __name__ == "__main__":
    main()
