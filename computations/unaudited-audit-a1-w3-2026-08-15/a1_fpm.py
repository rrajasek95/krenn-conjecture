"""AUDIT A1 -- fractional perfect matchings, INDEPENDENT route.

W3 decides "edge e lies in some fractional perfect matching" by the
fractional Tutte condition i(H-S) <= |S| applied to H - {u,v} plus a scan
over odd cycles through e.  I instead ENUMERATE ALL VERTICES of the
fractional perfect matching polytope directly: by half-integrality every
vertex is (a set of vertex-disjoint odd cycles at value 1/2) + (a perfect
matching of the rest at value 1).  The union of their supports is exactly
the set of edges lying in some fpm, and the polytope is nonempty iff at
least one such structure exists.

Cross-checked against an exact rational LP (a1_lp) on random graphs.
"""

from __future__ import annotations

import itertools


def _adj(edges, verts):
    a = {v: set() for v in verts}
    for u, v in edges:
        a[u].add(v)
        a[v].add(u)
    return a


def odd_cycles_from(adj, start, allowed):
    """All simple odd cycles (>=3) through `start` inside `allowed`, as
    frozensets of edges."""
    out = set()
    stack = [(start, [start], {start})]
    while stack:
        cur, path, seen = stack.pop()
        for nxt in adj[cur]:
            if nxt not in allowed:
                continue
            if nxt == start:
                if len(path) >= 3 and len(path) % 2 == 1:
                    es = frozenset(
                        tuple(sorted((path[i], path[(i + 1) % len(path)])))
                        for i in range(len(path))
                    )
                    out.add(es)
                continue
            if nxt in seen or nxt < start:
                continue
            stack.append((nxt, path + [nxt], seen | {nxt}))
    return out


def fpm_vertices(edges, verts):
    """Yield the edge sets of all vertices of the fpm polytope."""
    edges = [tuple(sorted(e)) for e in edges]
    adj = _adj(edges, verts)
    verts = tuple(sorted(verts))
    res = []

    def rec(remaining, acc):
        if not remaining:
            res.append(frozenset(acc))
            return
        v = min(remaining)
        rest = remaining - {v}
        for u in adj[v]:
            if u in rest:
                rec(rest - {u}, acc | {tuple(sorted((v, u)))})
        for cyc in odd_cycles_from(adj, v, remaining):
            used = set()
            for (a, b) in cyc:
                used.add(a)
                used.add(b)
            rec(remaining - used, acc | set(cyc))

    rec(set(verts), set())
    return res


def fpm_exists(edges, verts):
    return len(fpm_vertices(edges, verts)) > 0


def fpm_support(edges, verts):
    out = set()
    for es in fpm_vertices(edges, verts):
        out |= es
    return out


def failing_edges(edges, verts):
    edges = {tuple(sorted(e)) for e in edges}
    return sorted(edges - fpm_support(edges, verts))


# ------------------------------------------------------------- LP crosscheck


def edge_in_fpm_lp(edges, verts, e):
    """Exact rational LP: max x_e over {x >= 0, sum_{f ~ v} x_f = 1}."""
    from a1_lp import solve
    from fractions import Fraction

    edges = [tuple(sorted(f)) for f in edges]
    verts = sorted(verts)
    A = [[Fraction(1) if v in f else Fraction(0) for f in edges] for v in verts]
    b = [Fraction(1)] * len(verts)
    c = [Fraction(0)] * len(edges)
    c[edges.index(tuple(sorted(e)))] = Fraction(-1)
    st, x, obj = solve(A, b, c)
    if st == "infeasible":
        return False
    if st == "unbounded":
        return True
    return -obj > 0
