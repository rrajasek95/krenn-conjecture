#!/usr/bin/env python3
"""Audit the same-column 2I+2R+2Z potential boundary.

Assume endpoint ranks (2,2,1,1,0,0).  The two rank-one source factors
occupy the same selected coordinate line, and their potential sum is
nonzero.  Their mutual numerator and residual block therefore vanish.
After independent covariant shore normalizations, the four invertible-to-
rank-one blocks occupy one column at each rank-one shore.

Signed set partitions enumerate every possible zero-sum support graph.
There are 39 envelopes modulo the natural I-, R-, and Z-site swaps.  Except
for the equal-core/opposite-zero envelope, every envelope has at most 52
potentially nonzero cell columns in the matching differential.

Standard library only; checks remain live under python -O and python -I -S.
"""

from collections import Counter
from itertools import combinations, product
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


SITES = tuple(range(6))
COLOURS = (0, 1)
INVERTIBLE = (0, 1)
RANK_ONE = (2, 3)
ZERO = (4, 5)
EDGES = tuple(combinations(SITES, 2))
CORE_EDGES = frozenset(combinations(INVERTIBLE + RANK_ONE, 2))
CELLS = tuple(
    (u, v, a, b)
    for u, v in EDGES
    for a, b in product(COLOURS, repeat=2)
)


def edge(u, v):
    return tuple(sorted((u, v)))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    head = vertices[0]
    answer = []
    for position in range(1, len(vertices)):
        partner = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            answer.append(((head, partner),) + tail)
    return tuple(answer)


COMPLEMENT_MATCHINGS = {
    pair: perfect_matchings(site for site in SITES if site not in pair)
    for pair in EDGES
}


def signed_partitions(length):
    """Canonical values modulo relabeling nonzero negation orbits.

    Zero is literal zero.  A first occurrence of a new orbit {lambda,-lambda}
    is positive; later occurrences may use either sign.  Thus zero-sum
    relations are enumerated exactly without choosing numerical values.
    """

    answer = []

    def visit(prefix, classes):
        if len(prefix) == length:
            answer.append(tuple(prefix))
            return
        visit(prefix + [0], classes)
        for orbit in range(1, classes + 1):
            visit(prefix + [orbit], classes)
            visit(prefix + [-orbit], classes)
        visit(prefix + [classes + 1], classes + 1)

    visit([], 0)
    return tuple(answer)


def zero_sum(left, right):
    return (left == right == 0) or (left != 0 and left == -right)


def admissible(potential):
    # The I-I and all I-R numerators are nonzero.  The same-column theorem
    # additionally assumes the R-R potential sum is nonzero, so no pair of
    # the four core potentials may sum to zero.
    return all(
        not zero_sum(potential[u], potential[v])
        for u, v in CORE_EDGES
    )


def optional_edges(potential):
    return frozenset(
        pair for pair in EDGES
        if pair not in CORE_EDGES
        and zero_sum(potential[pair[0]], potential[pair[1]])
    )


def swap_maps():
    answer = []
    for swap_i, swap_r, swap_z in product((False, True), repeat=3):
        mapping = list(SITES)
        if swap_i:
            mapping[0], mapping[1] = mapping[1], mapping[0]
        if swap_r:
            mapping[2], mapping[3] = mapping[3], mapping[2]
        if swap_z:
            mapping[4], mapping[5] = mapping[5], mapping[4]
        answer.append(tuple(mapping))
    return tuple(answer)


SWAP_MAPS = swap_maps()


def canonical_optional_edges(live):
    variants = []
    for mapping in SWAP_MAPS:
        variants.append(tuple(sorted(
            edge(mapping[u], mapping[v]) for u, v in live
        )))
    return min(variants)


def support_value(optional, pair, colours):
    u, v = pair
    _, colour_at_v = colours
    if pair == (0, 1):
        return True
    if u in INVERTIBLE and v in RANK_ONE:
        # A separate local basis change at each rank-one shore sends its
        # nonzero target factor to e_0.  This is only a covariant rank audit.
        return colour_at_v == 0
    if pair == (2, 3):
        # Equal missing selected columns make b_2^T J b_3 zero, while the
        # assumed nonzero potential sum forces the residual block to zero.
        return False
    return pair in optional


def cofactor_may_live(optional, pair, word):
    return any(
        all(
            support_value(
                optional,
                matching_edge,
                (word[matching_edge[0]], word[matching_edge[1]]),
            )
            for matching_edge in matching
        )
        for matching in COMPLEMENT_MATCHINGS[pair]
    )


def active_cells(optional):
    answer = set()
    for cell in CELLS:
        u, v, a, b = cell
        if any(
            word[u] == a
            and word[v] == b
            and cofactor_may_live(optional, (u, v), word)
            for word in product(COLOURS, repeat=6)
        ):
            answer.add(cell)
    return frozenset(answer)


def support_envelopes():
    envelopes = {}
    admissible_count = 0
    for potential in signed_partitions(len(SITES)):
        if not admissible(potential):
            continue
        admissible_count += 1
        optional = canonical_optional_edges(optional_edges(potential))
        envelopes.setdefault(optional, potential)
    return admissible_count, envelopes


DENSE_OPTIONAL = frozenset(
    edge(core, zero) for core in INVERTIBLE + RANK_ONE for zero in ZERO
)
DENSE_POTENTIAL = (1, 1, 1, 1, -1, -1)


def audit_support_map():
    signed_count = len(signed_partitions(len(SITES)))
    admissible_count, envelopes = support_envelopes()
    require(signed_count == 4088,
            ("signed partition census changed", signed_count))
    require(admissible_count == 1574,
            ("admissible potential census changed", admissible_count))
    require(len(envelopes) == 39,
            ("support-envelope census changed", len(envelopes)))

    dense_key = canonical_optional_edges(DENSE_OPTIONAL)
    require(dense_key in envelopes, "dense guard envelope disappeared")
    require(optional_edges(DENSE_POTENTIAL) == DENSE_OPTIONAL,
            "dense potential no longer realizes all core-zero edges")

    # Conversely, all eight core-zero sums force a single nonzero core
    # potential and its opposite on both zero sites.
    dense_representatives = tuple(
        potential for potential in signed_partitions(len(SITES))
        if admissible(potential)
        and optional_edges(potential) == DENSE_OPTIONAL
    )
    require(dense_representatives == (DENSE_POTENTIAL,),
            ("dense envelope lost uniqueness", dense_representatives))
    return envelopes, dense_key


EXPECTED_ACTIVE_HISTOGRAM = {
    # Filled from the exact local-colour enumeration below.  Keeping the
    # whole histogram live catches both support-map and cofactor regressions.
    4: 1,
    12: 2,
    16: 1,
    20: 6,
    24: 3,
    28: 2,
    32: 4,
    36: 3,
    40: 10,
    44: 2,
    48: 3,
    52: 1,
    60: 1,
}


def audit_cofactor_bounds(envelopes, dense_key):
    counts = {optional: len(active_cells(optional)) for optional in envelopes}
    histogram = dict(sorted(Counter(counts.values()).items()))
    require(histogram == EXPECTED_ACTIVE_HISTOGRAM,
            ("active-cell histogram changed", histogram))
    require(counts[dense_key] == 60,
            ("dense envelope active count changed", counts[dense_key]))
    non_dense = {
        optional: count for optional, count in counts.items()
        if optional != dense_key
    }
    require(max(non_dense.values()) == 52,
            ("non-dense rank bound changed", max(non_dense.values())))
    return counts, histogram


def build_numeric_packet(optional):
    packet = {}
    for edge_index, pair in enumerate(EDGES):
        for a, b in product(COLOURS, repeat=2):
            if support_value(optional, pair, (a, b)):
                value = 1 + (
                    17 * edge_index + 7 * a + 11 * b
                    + 3 * edge_index * edge_index
                ) % 29
            else:
                value = 0
            packet[pair[0], pair[1], a, b] = value
    return packet


def audit_modular_calibration(envelopes, dense_key, counts):
    core = run_path(str(Path(__file__).with_name(
        "verify_level_two_one_sided_overlap_collapse.py"
    )))
    ranks = {}
    for optional in envelopes:
        derivative = core["differential"](build_numeric_packet(optional))
        pair = tuple(
            core["rank_mod"](derivative, prime)
            for prime in (101, 1_000_003)
        )
        require(pair[0] == pair[1],
                ("calibration primes disagreed", optional, pair))
        require(pair[0] <= counts[optional],
                ("calibration exceeded support bound", optional, pair))
        ranks[optional] = pair[0]
    require(ranks[dense_key] == 55,
            ("dense envelope lost rank-55 calibration", ranks[dense_key]))
    require(max(rank for key, rank in ranks.items() if key != dense_key) <= 52,
            ("non-dense calibration exceeded theorem", ranks))
    return dict(sorted(Counter(ranks.values()).items()))


def main():
    envelopes, dense_key = audit_support_map()
    counts, histogram = audit_cofactor_bounds(envelopes, dense_key)
    rank_histogram = audit_modular_calibration(envelopes, dense_key, counts)
    print("2I+2R+2Z same-column potential boundary: all checks passed")
    print(f"  support envelopes              : {len(envelopes)}")
    print(f"  active-cell histogram          : {histogram}")
    print(f"  calibration-rank histogram     : {rank_histogram}")
    print(f"  non-dense maximum rank bound   : 52")
    print(f"  enlarged dense active/rank     : 60/55")
    print(f"  dense exceptional potential    : {DENSE_POTENTIAL}")


if __name__ == "__main__":
    main()
