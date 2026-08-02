#!/usr/bin/env python3
"""Audit the gauge-boundary closure in the 3I+1R+2Z normal form.

The forced live core is a triangle on 0,1,2 joined to rank-one site 3.
At rank 55, zero sites 4 and 5 cannot be isolated because an isolated site
leaves at most its twenty incident cell columns in the differential.  Once
both zero sites have a live core spoke, the live graph is connected and
nonbipartite, so all five trace-zero vertex gauges are independent.

Standard library only; assertions remain live under -O and -I -S.
"""

from fractions import Fraction as Q
from itertools import combinations


SITES = tuple(range(6))
INNER = (0, 1, 2)
RANK_ONE = 3
CORE = INNER + (RANK_ONE,)
ZEROS = (4, 5)
EDGES = tuple(combinations(SITES, 2))
CORE_EDGES = frozenset(combinations(INNER, 2)) | {
    (i, RANK_ONE) for i in INNER
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def rational_rank(matrix):
    rows = [[Q(entry) for entry in row] for row in matrix]
    height = len(rows)
    width = len(rows[0]) if rows else 0
    rank = 0
    for column in range(width):
        pivot = next(
            (row for row in range(rank, height) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = rows[rank][column]
        rows[rank] = [entry / scale for entry in rows[rank]]
        for row in range(height):
            if row == rank or not rows[row][column]:
                continue
            multiple = rows[row][column]
            rows[row] = [
                left - multiple * right
                for left, right in zip(rows[row], rows[rank])
            ]
        rank += 1
    return rank


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def connected(live_edges):
    reached = {0}
    changed = True
    while changed:
        changed = False
        for u, v in live_edges:
            if u in reached and v not in reached:
                reached.add(v)
                changed = True
            elif v in reached and u not in reached:
                reached.add(u)
                changed = True
    return reached == set(SITES)


def gauge_matrix(live_edges):
    """Map five free mu coordinates (mu_5=-sum_0^4 mu_i) to edge sums."""

    matrix = []
    for u, v in sorted(live_edges):
        row = [0] * 5
        for endpoint in (u, v):
            if endpoint < 5:
                row[endpoint] += 1
            else:
                for index in range(5):
                    row[index] -= 1
        matrix.append(row)
    return matrix


def audit_live_graphs_and_gauges():
    core_spokes = tuple((r, z) for r in CORE for z in ZEROS)
    choices = tuple(
        frozenset(CORE[index] for index in range(len(CORE)) if mask >> index & 1)
        for mask in range(1, 1 << len(CORE))
    )
    checked = 0
    for left in choices:
        for right in choices:
            live = set(CORE_EDGES)
            live.update((r, 4) for r in left)
            live.update((r, 5) for r in right)
            require((4, 5) not in live, "the forced zero edge 45 became live")
            require(live <= set(EDGES), "a live edge left K6")
            require(connected(live), ("live graph disconnected", left, right))
            require(set(combinations(INNER, 2)) <= live,
                    "the forced odd triangle disappeared")
            require(rational_rank(gauge_matrix(live)) == 5,
                    ("trace-zero gauges became dependent", left, right))
            checked += 1
    require(checked == 225, "nonempty zero-spoke census changed")
    require(len(core_spokes) == 8, "zero-spoke edge count changed")
    return checked


def audit_isolated_site_column_bound():
    isolated = 5
    incident_edges = tuple(edge for edge in EDGES if isolated in edge)
    other_edges = tuple(edge for edge in EDGES if isolated not in edge)
    require(len(incident_edges) == 5 and len(other_edges) == 10,
            "isolated-site edge split changed")

    # A derivative column on uv uses perfect matchings of the four vertices
    # complementary to u,v.  If uv avoids the isolated site, every such
    # matching contains one edge incident with it and therefore vanishes.
    checked_matchings = 0
    for u, v in other_edges:
        remaining = tuple(r for r in SITES if r not in (u, v))
        matchings = perfect_matchings(remaining)
        require(len(matchings) == 3, "four-site matching count changed")
        require(all(any(isolated in edge for edge in matching)
                    for matching in matchings),
                ("a cofactor matching avoided the isolated site", u, v))
        checked_matchings += len(matchings)

    possible_columns = 4 * len(incident_edges)
    require(possible_columns == 20, "isolated-site column bound changed")
    require(checked_matchings == 30, "isolated cofactor audit changed")
    return possible_columns, checked_matchings


def main():
    graphs = audit_live_graphs_and_gauges()
    columns, matchings = audit_isolated_site_column_bound()
    print("three-invertible gauge-boundary closure: all checks passed")
    print(f"  attached-spoke graphs : {graphs}/225")
    print("  trace-zero gauge rank : 5 in every graph")
    print(f"  isolated-site columns : {columns}, hence rank <= {columns}")
    print(f"  vanished cofactors    : {matchings}/30 matching terms")


if __name__ == "__main__":
    main()
