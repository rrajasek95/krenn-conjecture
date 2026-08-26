"""UNAUDITED STRESS TEST (2026-08-13): matching flip graph + spanning-tree
transport library.

Pinned HEAD: see PINNED_HEAD.txt in this directory.

Everything is exact: coefficients are fractions.Fraction, Laurent monomials
are frozen dicts cell -> integer exponent, signs are +-1 integers.

Vocabulary
----------
matching   : tuple of sorted 2-tuples, a perfect matching of K_{2n}
occurrence : (chi, M) with chi a colouring word; the physical monomial is
             m_chi(M) = prod_{uv in M} a_uv(chi_u, chi_v)
cell       : (u, v, chi_u, chi_v) with u < v   -- a variable of the problem
flip edge  : (M, M') with |M sym-diff M'| = 4  (a 2-switch / alternating
             4-cycle exchange).  Optionally general alternating-cycle
             exchanges (any symmetric difference that is a single cycle).
"""
from __future__ import annotations

from collections import defaultdict, deque
from fractions import Fraction as Q
from itertools import combinations
import heapq


# ------------------------------------------------------------------ matchings

def perfect_matchings(sites):
    """All perfect matchings of the complete graph on `sites` (a sorted tuple)."""
    sites = tuple(sorted(sites))
    if not sites:
        yield ()
        return
    a = sites[0]
    for i in range(1, len(sites)):
        b = sites[i]
        rest = sites[1:i] + sites[i + 1:]
        for sub in perfect_matchings(rest):
            yield tuple(sorted(((a, b),) + sub))


def all_matchings(n2):
    """Perfect matchings of K_{n2}, lexicographically sorted."""
    return sorted(perfect_matchings(tuple(range(n2))))


# ---------------------------------------------------------------- flip graph

def two_switch_neighbours(M):
    """All matchings obtained from M by one 2-switch (alternating 4-cycle)."""
    out = set()
    pairs = list(M)
    for i, j in combinations(range(len(pairs)), 2):
        (a, b), (c, d) = pairs[i], pairs[j]
        rest = tuple(p for k, p in enumerate(pairs) if k not in (i, j))
        for new in (((min(a, c), max(a, c)), (min(b, d), max(b, d))),
                    ((min(a, d), max(a, d)), (min(b, c), max(b, c)))):
            cand = tuple(sorted(rest + new))
            if cand != M:
                out.add(cand)
    return out


def alternating_cycle_neighbours(M, allow_pairs=None):
    """All matchings M' with M sym-diff M' a SINGLE alternating cycle.

    (2-switch is the length-4 case.)  `allow_pairs`, if given, is the set of
    pairs permitted in M'.
    """
    out = set()
    verts = sorted(x for p in M for x in p)
    partner = {}
    for a, b in M:
        partner[a] = b
        partner[b] = a
    # a symmetric difference that is a single cycle uses k pairs of M and k
    # new pairs on the same 2k vertices; enumerate by choosing the subset of
    # M-pairs and re-matching their vertex set with no shared pair.
    pairs = list(M)
    for k in range(2, len(pairs) + 1):
        for sub in combinations(range(len(pairs)), k):
            vs = tuple(sorted(x for i in sub for x in pairs[i]))
            rest = tuple(pairs[i] for i in range(len(pairs)) if i not in sub)
            old = set(pairs[i] for i in sub)
            for new in perfect_matchings(vs):
                if set(new) & old:
                    continue      # not a full exchange on this subset
                if allow_pairs is not None and any(
                        p not in allow_pairs for p in new):
                    continue
                cand = tuple(sorted(rest + new))
                # single-cycle test: the union old|new must be connected
                adj = defaultdict(set)
                for a, b in old | set(new):
                    adj[a].add(b)
                    adj[b].add(a)
                seen = {vs[0]}
                stack = [vs[0]]
                while stack:
                    x = stack.pop()
                    for y in adj[x]:
                        if y not in seen:
                            seen.add(y)
                            stack.append(y)
                if len(seen) != len(vs):
                    continue
                out.add(cand)
    out.discard(M)
    return out


def flip_graph(matchings, neighbour_fn=two_switch_neighbours):
    """adjacency dict M -> sorted list of neighbours (restricted to `matchings`)."""
    mset = set(matchings)
    adj = {M: [] for M in matchings}
    for M in matchings:
        for N in neighbour_fn(M):
            if N in mset:
                adj[M].append(N)
    for M in adj:
        adj[M] = sorted(adj[M])
    return adj


def undirected_edges(adj):
    E = set()
    for M, ns in adj.items():
        for N in ns:
            E.add((M, N) if M < N else (N, M))
    return sorted(E)


def is_connected(adj):
    if not adj:
        return True
    start = min(adj)
    seen = {start}
    dq = deque([start])
    while dq:
        x = dq.popleft()
        for y in adj[x]:
            if y not in seen:
                seen.add(y)
                dq.append(y)
    return len(seen) == len(adj)


def components(adj):
    seen = set()
    comps = []
    for start in sorted(adj):
        if start in seen:
            continue
        comp = {start}
        dq = deque([start])
        seen.add(start)
        while dq:
            x = dq.popleft()
            for y in adj[x]:
                if y not in seen:
                    seen.add(y)
                    comp.add(y)
                    dq.append(y)
        comps.append(sorted(comp))
    return comps


# ------------------------------------------------------- rooted spanning tree

def bfs_tree(adj, root, key=lambda M: M):
    """BFS spanning tree rooted at `root`, neighbours visited in `key` order.

    Returns (parent, depth, order).  parent[root] is None.
    Deterministic: FIFO queue, neighbours sorted by `key`.
    """
    parent = {root: None}
    depth = {root: 0}
    order = [root]
    dq = deque([root])
    while dq:
        x = dq.popleft()
        for y in sorted(adj[x], key=key):
            if y not in parent:
                parent[y] = x
                depth[y] = depth[x] + 1
                order.append(y)
                dq.append(y)
    return parent, depth, order


def dijkstra_tree(adj, root, key=lambda M: M):
    """Shortest-path tree with `key` as the deterministic tie-break (a second,
    genuinely different, canonical tree rule)."""
    parent = {root: None}
    depth = {root: 0}
    order = []
    heap = [(0, key(root), root)]
    done = set()
    while heap:
        d, _k, x = heapq.heappop(heap)
        if x in done:
            continue
        done.add(x)
        order.append(x)
        for y in sorted(adj[x], key=key):
            if y not in done and (y not in depth or d + 1 < depth[y]):
                depth[y] = d + 1
                parent[y] = x
                heapq.heappush(heap, (d + 1, key(y), y))
    return parent, depth, order


def dfs_tree(adj, root, key=lambda M: M):
    """Depth-first spanning tree (a THIRD tree rule; deliberately not BFS)."""
    parent = {root: None}
    depth = {root: 0}
    order = [root]
    stack = [(root, iter(sorted(adj[root], key=key)))]
    while stack:
        x, it = stack[-1]
        advanced = False
        for y in it:
            if y not in parent:
                parent[y] = x
                depth[y] = depth[x] + 1
                order.append(y)
                stack.append((y, iter(sorted(adj[y], key=key))))
                advanced = True
                break
        if not advanced:
            stack.pop()
    return parent, depth, order


def tree_edges(parent):
    return sorted((min(v, p), max(v, p)) for v, p in parent.items()
                  if p is not None)


def path_to_root(parent, M):
    """[M, ..., root] vertex list along tree edges."""
    out = [M]
    while parent[out[-1]] is not None:
        out.append(parent[out[-1]])
    return out


def tree_path(parent, depth, A, B):
    """Vertex list A ... B through the tree (via their meet)."""
    up, down = [A], [B]
    a, b = A, B
    while depth[a] > depth[b]:
        a = parent[a]
        up.append(a)
    while depth[b] > depth[a]:
        b = parent[b]
        down.append(b)
    while a != b:
        a = parent[a]
        up.append(a)
        b = parent[b]
        down.append(b)
    return up + down[-2::-1]


# ------------------------------------------------- Laurent monomials / signs

def cell(u, v, chi):
    """The variable a_uv(chi_u, chi_v) as a canonical 4-tuple, u < v."""
    if u > v:
        u, v = v, u
    return (u, v, chi[u], chi[v])


def monomial_of(M, chi):
    """m_chi(M): frozenset of cells (squarefree), as a sorted tuple."""
    return tuple(sorted(cell(u, v, chi) for u, v in M))


def laurent_ratio(M, N, chi):
    """m_chi(N)/m_chi(M) as a dict cell -> exponent (nonzero entries only)."""
    e = defaultdict(int)
    for c in monomial_of(N, chi):
        e[c] += 1
    for c in monomial_of(M, chi):
        e[c] -= 1
    return {c: k for c, k in e.items() if k}


def ratio_mul(a, b):
    e = defaultdict(int)
    for c, k in a.items():
        e[c] += k
    for c, k in b.items():
        e[c] += k
    return {c: k for c, k in e.items() if k}


def ratio_inv(a):
    return {c: -k for c, k in a.items()}


# ----------------------------------------------- exact sparse linear algebra

def rref(vectors):
    """Row-reduce sparse dict vectors over Q.  Returns pivot -> reduced row."""
    basis = {}
    for vec in vectors:
        v = {k: Q(x) for k, x in vec.items() if x}
        while v:
            p = min(v, key=repr)
            if p not in basis:
                inv = Q(1) / v[p]
                basis[p] = {k: x * inv for k, x in v.items()}
                break
            c = v[p]
            row = basis[p]
            for k, x in row.items():
                r = v.get(k, Q(0)) - c * x
                if r:
                    v[k] = r
                else:
                    v.pop(k, None)
    return basis


def rank(vectors):
    return len(rref(vectors))


def reduce_against(basis, vec):
    """Fully reduce `vec` against a rref basis; returns the residual."""
    v = {k: Q(x) for k, x in vec.items() if x}
    changed = True
    while changed:
        changed = False
        common = set(v) & set(basis)
        if not common:
            break
        p = min(common, key=repr)
        c = v[p]
        for k, x in basis[p].items():
            r = v.get(k, Q(0)) - c * x
            if r:
                v[k] = r
            else:
                v.pop(k, None)
        changed = True
    return v


def in_span(vectors_basis, vec):
    return not reduce_against(vectors_basis, vec)


# ----------------------------------------------------------- chain utilities

def clean(d):
    return {k: v for k, v in d.items() if v}


def sub(a, b):
    out = dict(a)
    for k, v in b.items():
        out[k] = out.get(k, Q(0)) - v
    return clean(out)


def add(a, b):
    out = dict(a)
    for k, v in b.items():
        out[k] = out.get(k, Q(0)) + v
    return clean(out)


def scale(a, c):
    return clean({k: v * c for k, v in a.items()})
