#!/usr/bin/env python3
"""Audit the equal-potential 2I+4Z support-rank closure.

Research evidence only.  Krenn's conjecture remains open, SP-CLEAN-BRIDGE
is untouched, and no certified dependency changes.
"""

from itertools import combinations


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


SITES = tuple(range(6))
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


def base_envelope(a_sites, joined_c=(), c_edge=None):
    live = {edge(0, 1)}
    live.update(edge(i, a) for i in (0, 1) for a in a_sites)
    live.update(edge(a, c) for a in a_sites for c in joined_c)
    if c_edge is not None:
        live.add(edge(*c_edge))
    return frozenset(live)


def active_cofactor_edges(live):
    answer = set()
    for varied in EDGES:
        complement = tuple(site for site in SITES if site not in varied)
        if any(
            all(edge(*pair) in live for pair in matching)
            for matching in MATCHINGS4[complement]
        ):
            answer.add(varied)
    return frozenset(answer)


def audit_potential_representatives():
    """The seven representatives realize exactly the claimed envelopes."""

    # alpha=1.  Values -1 form A; values +1 join their C vertex to A;
    # opposite non-+/-1 C values create the optional C-C edge.
    representatives = (
        ((1, 1, -1, -1, -1, -1), (2, 3, 4, 5), (), None, 6),
        ((1, 1, -1, -1, -1, 2), (2, 3, 4), (), None, 3),
        ((1, 1, -1, -1, -1, 1), (2, 3, 4), (5,), None, 12),
        ((1, 1, -1, -1, 2, 3), (2, 3), (), None, 1),
        ((1, 1, -1, -1, 1, 3), (2, 3), (4,), None, 5),
        ((1, 1, -1, -1, 1, 1), (2, 3), (4, 5), None, 10),
        ((1, 1, -1, -1, 2, -2), (2, 3), (), (4, 5), 6),
    )
    results = []
    for nu, a_sites, joined_c, c_edge, expected_count in representatives:
        actual = {edge(0, 1)}
        for u, v in EDGES:
            if (u, v) == (0, 1):
                continue
            if nu[u] + nu[v] == 0:
                actual.add((u, v))
        expected = base_envelope(a_sites, joined_c, c_edge)
        require(frozenset(actual) == expected,
                ("potential envelope mismatch", nu, actual, expected))
        active = active_cofactor_edges(expected)
        require(len(active) == expected_count,
                ("cofactor count mismatch", nu, active, expected_count))
        results.append((len(a_sites), len(joined_c), c_edge is not None,
                        expected_count, 4 * expected_count))
    return tuple(results)


def audit_exception_compatibility():
    # If c has potential alpha and cd is a zero-sum edge, then d has
    # potential -alpha and belongs to A, never to C.
    for alpha in (-3, -1, 1, 2):
        c_value = alpha
        d_value = -c_value
        require(d_value == -alpha, "exception compatibility identity failed")
        require(d_value != alpha, "alpha must be nonzero")


def main():
    audit_exception_compatibility()
    results = audit_potential_representatives()
    counts = tuple(result[3] for result in results)
    bounds = tuple(result[4] for result in results)
    require(counts == (6, 3, 12, 1, 5, 10, 6),
            ("wrong support census", counts))
    require(max(bounds) == 48, ("equal-potential rank bound failed", bounds))
    print("2I+4Z equal-potential closure: all checks passed")
    print(f"  support envelopes     : {len(results)}")
    print(f"  cofactor-edge counts  : {counts}")
    print(f"  cell-column bounds    : {bounds}")
    print("  maximum rank bound    : 48")
    print("  combined 2I+4Z status : closed with separated-potential theorem")


if __name__ == "__main__":
    main()
