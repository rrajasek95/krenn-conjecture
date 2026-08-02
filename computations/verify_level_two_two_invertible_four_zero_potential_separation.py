#!/usr/bin/env python3
"""Audit the separated-potential 2I+4Z differential-rank bound.

Research evidence only.  Krenn's conjecture remains open, SP-CLEAN-BRIDGE
is untouched, and no certified dependency changes.
"""

from itertools import combinations


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


SITES = tuple(range(6))
ZERO = frozenset((2, 3, 4, 5))
EDGES = tuple(combinations(SITES, 2))


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


MATCHINGS4 = {
    vertices: perfect_matchings(vertices)
    for vertices in combinations(SITES, 4)
}


def edge(u, v):
    return tuple(sorted((u, v)))


def r2_partitions():
    """Each distinct-potential witness set has size exactly two."""

    partitions = set()
    zero_subsets = tuple(
        frozenset(subset)
        for size in range(2, 5)
        for subset in combinations(ZERO, size)
    )
    for left in zero_subsets:
        for right in zero_subsets:
            if left & right:
                continue
            require(len(left) == len(right) == 2,
                    ("disjoint R2 witness sets did not partition four sites",
                     left, right))
            require(left | right == ZERO, ("incomplete partition", left, right))
            partitions.add((left, right))
    require(len(partitions) == 6, ("wrong ordered partition count", partitions))
    return partitions


def multiplier_support(nu):
    """Zero-endpoint numerators permit exactly the zero-sum edges."""

    require(nu[0] != nu[1], "invertible potentials must be separated")
    require(nu[0] + nu[1] != 0, "invertible core numerator needs nonzero sum")
    live = {edge(0, 1)}
    for u, v in EDGES:
        if (u, v) == (0, 1):
            continue
        # Every remaining edge has at least one zero endpoint, so its
        # generic-kernel numerator is zero and the whole block is forced
        # to vanish unless the multiplier sum is zero.
        if nu[u] + nu[v] == 0:
            live.add((u, v))
    return frozenset(live)


def expected_envelope(a_pair, b_pair, zero_side):
    live = {edge(0, 1)}
    live.update(edge(0, site) for site in a_pair)
    live.update(edge(1, site) for site in b_pair)
    if zero_side == 0:
        live.add(edge(*tuple(sorted(a_pair))))
    elif zero_side == 1:
        live.add(edge(*tuple(sorted(b_pair))))
    return frozenset(live)


def active_cofactor_edges(live):
    active = set()
    for varied in EDGES:
        complement = tuple(site for site in SITES if site not in varied)
        if any(
            all(edge(*pair) in live for pair in matching)
            for matching in MATCHINGS4[complement]
        ):
            active.add(varied)
    return frozenset(active)


def audit_envelopes():
    a_pair = frozenset((2, 3))
    b_pair = frozenset((4, 5))
    cases = (
        ((1, 2, -1, -1, -2, -2), None, 4, 16),
        ((0, 1, 0, 0, -1, -1), 0, 7, 28),
        ((1, 0, -1, -1, 0, 0), 1, 7, 28),
    )
    results = []
    for nu, zero_side, edge_count, column_count in cases:
        actual = multiplier_support(nu)
        expected = expected_envelope(a_pair, b_pair, zero_side)
        require(actual == expected,
                ("zero-multiplier envelope mismatch", nu, actual, expected))
        active = active_cofactor_edges(actual)
        require(len(active) == edge_count,
                ("cofactor-edge count mismatch", nu, active))
        require(4 * len(active) == column_count,
                ("cell-column bound mismatch", nu, active))
        results.append((zero_side, tuple(sorted(active)), column_count))
    return tuple(results)


def main():
    partitions = r2_partitions()
    results = audit_envelopes()
    require(max(result[2] for result in results) == 28,
            "separated-potential bound is not 28")
    print("2I+4Z separated-potential closure: all checks passed")
    print(f"  ordered R2 partitions : {len(partitions)}")
    print(f"  cofactor envelopes    : {[len(item[1]) for item in results]}")
    print(f"  cell-column bounds    : {[item[2] for item in results]}")
    print("  maximum rank bound    : 28")
    print("  remaining boundary    : equal invertible-site potentials")


if __name__ == "__main__":
    main()
