"""Exact graph gates for signed edge sums and cancellation constraints."""
from itertools import combinations
from fractions import Fraction as Q
from exact import require, matchings, rank


def components(n, edges):
    neighbors = [set() for _ in range(n)]
    for i, j in edges:
        neighbors[i].add(j)
        neighbors[j].add(i)
    seen, out = set(), []
    for start in range(n):
        if start in seen:
            continue
        signs, stack, bipartite = {start: 1}, [start], True
        seen.add(start)
        while stack:
            i = stack.pop()
            for j in sorted(neighbors[i]):
                if j not in signs:
                    signs[j] = -signs[i]
                    stack.append(j)
                    seen.add(j)
                elif signs[j] == signs[i]:
                    bipartite = False
        out.append(dict(vertices=sorted(signs), signs=signs, bipartite=bipartite,
                        imbalance=sum(signs.values())))
    return out


def cover(n, supported):
    """Return p with sum p=1 and p_i+p_j=0 off supported, or None."""
    supported = set(supported)
    missing = set(combinations(range(n), 2))-supported
    for comp in components(n, missing):
        if comp['bipartite'] and comp['imbalance']:
            p = [Q(comp['signs'].get(i, 0), comp['imbalance']) for i in range(n)]
            weights = {(i, j): p[i]+p[j] for i, j in combinations(range(n), 2)}
            require(sum(p) == 1 and all(not weights[e] for e in missing), 'Supported vertex potential')
            return p, {e: z for e, z in weights.items() if z}
    return None


def census(n=6):
    require(n == 6, 'This exhaustive census and minor bound are for six sites')
    edges = tuple(combinations(range(n), 2))
    pm = tuple(matchings(tuple(range(n))))
    incidence = [[int(e in matching) for e in edges] for matching in pm]
    require(rank(incidence) == len(edges)-n+1, 'Constant matching-sum affine space has vertex-potential dimension')
    accepted, by_edges = 0, {}
    for bits in range(1 << len(edges)):
        support = {e for j, e in enumerate(edges) if bits & (1 << j)}
        certificate = cover(n, support)
        # Independent linear consistency check. For n=6, Hadamard bounds
        # every relevant integer minor by sqrt(6)*2^(5/2) < 16 < 101;
        # hence reduction modulo 101 preserves these ranks exactly.
        equations = [[int(k in e) for k in range(n)] for e in edges if e not in support]
        linear_feasible = modular_rank(equations+[([1]*n)]) > modular_rank(equations)
        require(linear_feasible == (certificate is not None), 'Independent exact linear feasibility agrees with graph gate')
        if certificate is None:
            continue
        _, weights = certificate
        require(all(sum(weights.get(e, 0) for e in matching) == 1 for matching in pm),
                'Every perfect matching receives total weight one')
        accepted += 1
        by_edges[len(support)] = by_edges.get(len(support), 0)+1
    return dict(sites=n, supports=1 << len(edges), excluded_supports=accepted,
                unresolved_supports=(1 << len(edges))-accepted,
                excluded_by_edge_count=by_edges, matching_incidence_rank=rank(incidence),
                independent_consistency_checks=1 << len(edges), rank_prime=101,
                integer_minor_absolute_upper='16')


def modular_rank(matrix):
    a = [row[:] for row in matrix]
    if not a:
        return 0
    row = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(row, len(a)) if a[i][col] % 101), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        inv = pow(a[row][col], -1, 101)
        a[row] = [x*inv % 101 for x in a[row]]
        for i in range(row+1, len(a)):
            d = a[i][col]
            if d:
                a[i] = [(x-d*y) % 101 for x, y in zip(a[i], a[row])]
        row += 1
        if row == len(a):
            break
    return row
