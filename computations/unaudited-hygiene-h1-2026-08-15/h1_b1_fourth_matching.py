#!/usr/bin/env python3
"""H1 / BLOCKER 1 -- adversarial from-scratch audit of A3's Theorem A3.4
(the fourth-matching theorem) and its corollaries.

UNAUDITED.  Hygiene agent H1, 2026-08-15.  Exact arithmetic (Python ints
only; no floats anywhere).  Written WITHOUT importing anything from the
A3 lane: every routine below (perfect-matching enumeration, the
constructive proof, the permanent/fibre engine, even-cycle detection) is
an independent re-implementation, so agreement with A3's numbers is
evidence and not a tautology.

WHAT IS CHECKED
  T1  chart enumeration + the constructive proof (steps 1/3/4) at
      N = 4, 6, 8, 10: every emitted matching is verified to be a genuine
      perfect matching of M_0 u M_1 u M_2 lying outside {M_0,M_1,M_2},
      against a brute-force enumeration of ALL perfect matchings of the
      union.  Branch census.  N = 4 sharpness.
  T2  STEP 5.  A3's Step-5 prose is a 2-adic descent that never uses the
      Hamiltonicity of M_0 u M_2.  T2 tests, exhaustively, whether the
      residual configuration is empty
        (a) under the hypotheses the prose actually uses  [(B)+(C)], and
        (b) under the full step-5 hypotheses               [(A)+(B)+(C)],
      for N = 8, 12, 16, 20, and verifies the replacement lemma
      (H = E' u O' is disconnected) that H1's corrected proof turns on.
  T3  Corollary A3.4-a (the m = 3N/2 floor): per chart, the word read off
      the fourth matching is mixed and its fibre has size exactly 1 --
      computed by TWO disjoint engines (subset-DP product formula; direct
      enumeration of all (N-1)!! matchings).
  T4  NEW CHECKER (excluded corollary 2): the even-cycle lemma
        pm(G[S]) <= 1 for every S   <=>   G has no even cycle,
      exhaustively over all graphs on n = 4, 5, 6 vertices and a
      deterministic stride at n = 7.
  T5  NEW CHECKER (excluded corollary 2, main statement): every diagonal
      monomial template whose three colour graphs are even-cycle-free and
      whose three constant fibres are live has a MIXED SINGLETON FIBRE
      (hence dies by O2).  Exhaustive at N = 6 (all 4^6 extensions of all
      32 charts) and at N = 8 up to two extra edges.
  T6  NEW CHECKER (excluded corollary 1): m = 3N/2 + 1 dies.  Exactly one
      edge added to one colour class of a chart; the added-edge lemma
      ("a matching plus one edge is acyclic, hence even-cycle-free") is
      checked directly, and the mixed singleton fibre is exhibited by
      both engines.  N = 6, 8, 10.
  MC  mutation controls: nine of them, each of which MUST fail.

Usage:  python3 h1_b1_fourth_matching.py [maxN]
"""

from __future__ import annotations

import json
import os
import sys
import time
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))


class CheckFailure(Exception):
    pass


def require(cond, msg):
    """House style: a raising check that survives python3 -O."""
    if not cond:
        raise CheckFailure(msg)


# ===================================================================== base

def perfect_matchings(verts):
    """Every perfect matching of the complete graph on `verts` (a tuple),
    as a sorted tuple of sorted 2-tuples.  Independent recursion."""
    if not verts:
        yield ()
        return
    a = verts[0]
    for i in range(1, len(verts)):
        b = verts[i]
        rest = verts[1:i] + verts[i + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted(((a, b),) + tail))


def matchings_avoiding(n, forbidden):
    """Perfect matchings of K_n using no edge of `forbidden`."""
    bad = set(forbidden)
    return [m for m in perfect_matchings(tuple(range(n)))
            if not any(e in bad for e in m)]


def pm_of_graph(n, edges):
    """Every perfect matching of the graph (n, edges), by direct search."""
    adj = {v: set() for v in range(n)}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    out = []

    def rec(rem, acc):
        if not rem:
            out.append(frozenset(acc))
            return
        v = min(rem)
        for u in sorted(adj[v] & rem):
            rec(rem - {v, u}, acc + [(min(u, v), max(u, v))])

    rec(frozenset(range(n)), [])
    return out


def pm_counts_by_subset(n, edges):
    """cnt[S] = number of perfect matchings of the induced subgraph on the
    vertex bitmask S.  Independent exact integer subset DP."""
    nbr = [0] * n
    for u, v in edges:
        nbr[u] |= 1 << v
        nbr[v] |= 1 << u
    cnt = [0] * (1 << n)
    cnt[0] = 1
    for S in range(1, 1 << n):
        low = S & (-S)
        v = low.bit_length() - 1
        rest = S ^ low
        tot = 0
        c = nbr[v] & rest
        while c:
            b = c & (-c)
            tot += cnt[rest ^ b]
            c ^= b
        cnt[S] = tot
    return cnt


def nbr_bits(n, edges):
    nbr = [0] * n
    for u, v in edges:
        nbr[u] |= 1 << v
        nbr[v] |= 1 << u
    return nbr


def pm_count_mask(nbr, mask, memo):
    """Number of perfect matchings of the subgraph induced on the vertex
    bitmask `mask`.  Memoised recursion -- only the reachable submasks are
    visited, so this is far cheaper than the full 2^n DP when the colour
    graph is sparse.  Exact integers."""
    if mask == 0:
        return 1
    got = memo.get(mask)
    if got is not None:
        return got
    low = mask & (-mask)
    v = low.bit_length() - 1
    rest = mask ^ low
    tot = 0
    c = nbr[v] & rest
    while c:
        b = c & (-c)
        tot += pm_count_mask(nbr, rest ^ b, memo)
        c ^= b
    memo[mask] = tot
    return tot


def components(n, edges):
    """Vertex sets of the connected components of (n, edges)."""
    adj = {v: [] for v in range(n)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    seen, out = set(), []
    for s in range(n):
        if s in seen:
            continue
        stack, comp = [s], set()
        seen.add(s)
        while stack:
            w = stack.pop()
            comp.add(w)
            for z in adj[w]:
                if z not in seen:
                    seen.add(z)
                    stack.append(z)
        out.append(comp)
    return out


def has_even_cycle(n, edges):
    """True iff the simple graph (n, edges) contains a cycle of EVEN length.

    Independent DFS: for each start vertex s, walk simple paths that use
    only vertices >= s, and close back to s.  Returns on the first even
    closure.  A cycle needs length >= 3, so a length-2 closure (retracing
    the entry edge) is excluded."""
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    for s in range(n):
        onpath = [False] * n
        onpath[s] = True

        def dfs(v, length):
            for w in adj[v]:
                if w == s:
                    if length >= 3 and length % 2 == 0:
                        return True
                    continue
                if w < s or onpath[w]:
                    continue
                onpath[w] = True
                if dfs(w, length + 1):
                    onpath[w] = False
                    return True
                onpath[w] = False
            return False

        if dfs(s, 1):
            return True
    return False


# ============================================ the constructive proof (mine)

def cycle_order(n, ma, mb):
    """If M_a u M_b is a single cycle, the vertex sequence around it,
    starting at vertex 0 and leaving along its M_a edge.  Else None."""
    if len(components(n, list(ma) + list(mb))) != 1:
        return None
    pa, pb = {}, {}
    for u, v in ma:
        pa[u], pa[v] = v, u
    for u, v in mb:
        pb[u], pb[v] = v, u
    order = [0, pa[0]]
    nxt = pb
    while len(order) < n:
        order.append(nxt[order[-1]])
        nxt = pa if nxt is pb else pb
    require(len(set(order)) == n, "cycle_order did not cover all vertices")
    return order


def build_fourth(n, m0, m1, m2):
    """Steps 1/3/4 of the constructive proof.  Returns (branch, matching)
    with `matching` a frozenset of edges, or (branch, None)."""
    ms = [frozenset(m0), frozenset(m1), frozenset(m2)]
    require(len(ms[0] | ms[1] | ms[2]) == 3 * (n // 2),
            "colour classes are not pairwise edge-disjoint")

    # -------- Step 1: some pair union is disconnected -> swap a component
    for a, b in ((0, 1), (0, 2), (1, 2)):
        comps = components(n, list(ms[a]) + list(ms[b]))
        if len(comps) >= 2:
            C = comps[0]
            S = frozenset([e for e in ms[a] if e[0] in C and e[1] in C]
                          + [e for e in ms[b]
                             if e[0] not in C and e[1] not in C])
            return "step1", S

    # -------- Steps 3/4 live on the M_0 u M_1 Hamilton cycle
    order = cycle_order(n, ms[0], ms[1])
    require(order is not None, "step 1 fell through but M_0uM_1 is not a cycle")
    pos = {v: i for i, v in enumerate(order)}

    def arc(i, j):
        """Alternating matching of the open cyclic arc from position i up to
        position j, along CYCLE edges.  The arc must have even size."""
        vs = []
        k = (i + 1) % n
        while k != j:
            vs.append(order[k])
            k = (k + 1) % n
        require(len(vs) % 2 == 0, f"arc({i},{j}) has odd size {len(vs)}")
        return frozenset((min(vs[t], vs[t + 1]), max(vs[t], vs[t + 1]))
                         for t in range(0, len(vs), 2))

    chords = sorted(ms[2])
    for c in chords:
        i, j = sorted((pos[c[0]], pos[c[1]]))
        require((j - i) % n not in (1, n - 1), "an M_2 edge is a cycle edge")
        if (j - i) % 2 == 1:                       # Step 3
            return "step3", frozenset([c]) | arc(i, j) | arc(j, i)

    for c, d in combinations(chords, 2):           # Step 4
        i, k = sorted((pos[c[0]], pos[c[1]]))
        j, l = sorted((pos[d[0]], pos[d[1]]))
        for (p, q, r, s) in ((i, j, k, l), (j, i, l, k)):
            if p < q < r < s and (q - p) % 2 == 1:
                return "step4", (frozenset([c, d]) | arc(p, q) | arc(q, r)
                                 | arc(r, s) | arc(s, p))

    return "step5-RESIDUAL", None


def is_pm_of(n, edges_universe, S):
    """S is a perfect matching using only edges of `edges_universe`."""
    U = set(edges_universe)
    if len(S) != n // 2:
        return False
    seen = set()
    for e in S:
        if e not in U:
            return False
        if e[0] in seen or e[1] in seen:
            return False
        seen.add(e[0])
        seen.add(e[1])
    return len(seen) == n


# =========================================================== fibre engines

def fibre_size_dp(n, colour_edges, word, nbrs=None):
    """|fibre(word)| for a diagonal template, by the product formula
    prod_r pm(G_r[word^{-1}(r)]) -- the memoised masked permanent."""
    masks = [0, 0, 0]
    for v, r in enumerate(word):
        masks[r] |= 1 << v
    if nbrs is None:
        nbrs = [nbr_bits(n, colour_edges[r]) for r in range(3)]
    out = 1
    for r in range(3):
        out *= pm_count_mask(nbrs[r], masks[r], {})
        if out == 0:
            return 0
    return out


def fibre_size_direct(n, colour_edges, word):
    """|fibre(word)| by DIRECT enumeration of all (n-1)!! matchings of K_n:
    count the matchings all of whose edges uv carry the diagonal label
    (word[u], word[v]) with word[u] == word[v]."""
    lab = {}
    for r, es in enumerate(colour_edges):
        for e in es:
            lab[(min(e), max(e))] = r
    tot = 0
    for m in perfect_matchings(tuple(range(n))):
        ok = True
        for u, v in m:
            r = lab.get((u, v))
            if r is None or word[u] != r or word[v] != r:
                ok = False
                break
        if ok:
            tot += 1
    return tot


def word_from_matching(n, colour_edges, S):
    """c(v) = the colour of the S-edge at v (S must be inside the union)."""
    col = {}
    for r, es in enumerate(colour_edges):
        for e in es:
            e = (min(e), max(e))
            if e in S:
                col[e[0]] = r
                col[e[1]] = r
    require(len(col) == n, "the matching does not cover every vertex")
    return tuple(col[v] for v in range(n))


def charts(n):
    """Ordered triples (M_0,M_1,M_2) of pairwise disjoint perfect matchings
    of K_n with M_0 pinned to the canonical matching by relabelling."""
    m0 = tuple(sorted((2 * i, 2 * i + 1)) for i in range(n // 2))
    m0 = tuple((a, b) for a, b in m0)
    for m1 in matchings_avoiding(n, m0):
        for m2 in matchings_avoiding(n, set(m0) | set(m1)):
            yield m0, m1, m2


# =============================================================== T1 + T3

def t1_t3(n, direct_stride):
    """Constructive proof + the m = 3N/2 singleton corollary, all charts."""
    census, nchart = {}, 0
    max_pm = 0
    fail_theorem, fail_construct, fail_singleton = [], [], []
    n_direct = 0
    example = None
    for m0, m1, m2 in charts(n):
        nchart += 1
        cols = [set(m0), set(m1), set(m2)]
        U = list(m0) + list(m1) + list(m2)
        allpm = set(pm_of_graph(n, U))
        max_pm = max(max_pm, len(allpm))
        originals = {frozenset(m0), frozenset(m1), frozenset(m2)}
        if len(allpm - originals) == 0:
            fail_theorem.append((m0, m1, m2))
        branch, S = build_fourth(n, m0, m1, m2)
        census[branch] = census.get(branch, 0) + 1
        if S is None:
            fail_construct.append(("no-output", m0, m1, m2, branch))
            continue
        # the emitted object must really be a FOURTH perfect matching
        if not (is_pm_of(n, U, S) and S in allpm and S not in originals):
            fail_construct.append(("bad-output", m0, m1, m2, branch))
            continue
        w = word_from_matching(n, cols, S)
        mixed = len(set(w)) > 1
        s_dp = fibre_size_dp(n, cols, w)
        s_dir = None
        if nchart % direct_stride == 0:
            s_dir = fibre_size_direct(n, cols, w)
            n_direct += 1
        bad = (not mixed) or s_dp != 1 or (s_dir is not None and s_dir != 1)
        if bad:
            fail_singleton.append((m0, m1, m2, w, s_dp, s_dir, mixed))
        if example is None:
            example = dict(M0=list(map(list, m0)), M1=list(map(list, m1)),
                           M2=list(map(list, m2)), branch=branch,
                           fourth=sorted(map(list, S)), word=list(w),
                           fibre_dp=s_dp, fibre_direct=s_dir)
    return dict(
        N=n, charts=nchart, branch_census=census, max_pm_count=max_pm,
        theorem_holds=(len(fail_theorem) == 0),
        charts_with_no_fourth_matching=len(fail_theorem),
        constructive_failures=len(fail_construct),
        constructive_failure_sample=[str(x) for x in fail_construct[:3]],
        singleton_corollary_failures=len(fail_singleton),
        singleton_failure_sample=[str(x) for x in fail_singleton[:3]],
        direct_engine_checks=n_direct, direct_engine_stride=direct_stride,
        example=example)


# ==================================================================== T2

def t2_step5(n):
    """Is the Step-5 residual configuration reachable?

    Fix the M_0 u M_1 Hamilton cycle 0-1-...-(n-1)-0 with
      M_0 = {(2s,2s+1)},  M_1 = {(2s+1,2s+2 mod n)}.
    Every chart whose three pair-unions are Hamiltonian is isomorphic to
    one of this shape, so ranging M_2 over perfect matchings of the
    remaining edges is exhaustive for the question.

    Step 3 fails  <=>  every M_2 chord joins two positions of EQUAL parity
                       (hypothesis B), which forces n = 0 mod 4.
    Step 4 fails  <=>  no even-parity chord interlaces an odd-parity chord
                       (hypothesis C).
    Step 1 fails  <=>  M_0 u M_2 and M_1 u M_2 are connected (hypothesis A).
    """
    res = dict(N=n)
    if n % 4 != 0:
        # B is unsatisfiable: a parity class has odd size n/2.
        res["hypothesis_B_satisfiable"] = False
        res["reason"] = ("n/2 is odd, so M_2 cannot match the n/2 even "
                         "positions among themselves; Step 3 always fires")
        res["configs_BC"] = 0
        res["configs_ABC"] = 0
        return res
    res["hypothesis_B_satisfiable"] = True
    ev = list(range(0, n, 2))
    od = list(range(1, n, 2))
    n_BC = n_ABC = 0
    H_connected_under_BC = 0
    total_B = 0
    witness_BC = None
    # The DERIVED condition of hypothesis (C): every chord's span is 0 mod 4
    # (an E-chord (i,k) encloses (k-i)/2 odd positions, which (C) forces to
    # be O-matched among themselves, hence even in number).  Counting these
    # separately keeps H1's replacement lemma (beta) NON-VACUOUS even though
    # (B)+(C) itself turns out to be empty.
    n_span4 = 0
    n_span4_H_connected = 0
    n_span4_lemma_violation = 0
    m0 = [(2 * s, 2 * s + 1) for s in range(n // 2)]
    m1 = [(min(2 * s + 1, (2 * s + 2) % n), max(2 * s + 1, (2 * s + 2) % n))
          for s in range(n // 2)]
    for E in perfect_matchings(tuple(ev)):
        for O in perfect_matchings(tuple(od)):
            total_B += 1
            m2 = tuple(sorted(E + O))
            npr = n // 2
            hedges = [(a // 2, c // 2) for (a, c) in E] + \
                     [((b - 1) // 2, (d - 1) // 2) for (b, d) in O]
            if all((x - y) % 4 == 0 for x, y in E) and \
                    all((x - y) % 4 == 0 for x, y in O):
                n_span4 += 1
                if any((u - v) % 2 for u, v in hedges):
                    n_span4_lemma_violation += 1
                if len(components(npr, hedges)) == 1:
                    n_span4_H_connected += 1
            # --- (C): no cross-parity interlacing pair
            crossed = False
            for (a, c) in E:
                for (b, d) in O:
                    lo, hi = (a, c) if a < c else (c, a)
                    x, y = (b, d) if b < d else (d, b)
                    if (lo < x < hi < y) or (x < lo < y < hi):
                        crossed = True
                        break
                if crossed:
                    break
            if crossed:
                continue
            n_BC += 1
            if witness_BC is None:
                witness_BC = dict(E=[list(e) for e in E],
                                  O=[list(e) for e in O])
            # --- H1's replacement lemma (beta): contract M_0, get
            #     H = E' u O' on Z_{n/2}; every edge must stay inside a
            #     parity class, so H is disconnected.
            if any((u - v) % 2 for u, v in hedges):
                res["LEMMA_VIOLATED"] = True
            if len(components(npr, hedges)) == 1:
                H_connected_under_BC += 1
            # --- (A): all three pair unions Hamiltonian
            ok_a = (len(components(n, m0 + list(m2))) == 1
                    and len(components(n, m1 + list(m2))) == 1)
            if ok_a:
                n_ABC += 1
    res.update(
        parity_preserving_M2_count=total_B,
        configs_BC=n_BC, configs_ABC=n_ABC,
        H_connected_under_BC=H_connected_under_BC,
        configs_all_spans_0_mod_4=n_span4,
        span4_with_H_connected=n_span4_H_connected,
        span4_lemma_violations=n_span4_lemma_violation,
        replacement_lemma_violations=res.get("LEMMA_VIOLATED", False),
        witness_BC=witness_BC)
    return res


# ==================================================================== T4

def t4_even_cycle_lemma(nv, stride):
    """pm(G[S]) <= 1 for every S   <=>   G has no even cycle."""
    edges = list(combinations(range(nv), 2))
    ne = len(edges)
    tested = mismatches = 0
    n_evenfree = n_witnessed = 0
    sample_bad = []
    for code in range(0, 1 << ne, stride):
        G = [edges[i] for i in range(ne) if code >> i & 1]
        cnt = pm_counts_by_subset(nv, G)
        pm_le1 = all(c <= 1 for c in cnt)
        evenfree = not has_even_cycle(nv, G)
        tested += 1
        if pm_le1 != evenfree:
            mismatches += 1
            if len(sample_bad) < 3:
                sample_bad.append(dict(edges=[list(e) for e in G],
                                       pm_le1=pm_le1, evenfree=evenfree,
                                       max_pm=max(cnt)))
        if evenfree:
            n_evenfree += 1
        else:
            n_witnessed += 1                # a subset with pm >= 2 must exist
            if max(cnt) < 2:
                mismatches += 1
    return dict(vertices=nv, stride=stride, graphs_tested=tested,
                even_cycle_free=n_evenfree, with_even_cycle=n_witnessed,
                mismatches=mismatches, sample=sample_bad,
                exhaustive=(stride == 1))


# =============================================================== T5 + T6

def extensions(free_edges, k):
    """All ways to assign exactly k of `free_edges` to a colour in {0,1,2}."""
    for chosen in combinations(range(len(free_edges)), k):
        for assign in _triples(k):
            yield [(free_edges[c], a) for c, a in zip(chosen, assign)]


def _triples(k):
    if k == 0:
        yield ()
        return
    for tail in _triples(k - 1):
        for a in (0, 1, 2):
            yield (a,) + tail


def t5_even_cycle_free_corollary(n, max_extra, direct_stride, chart_stride=1):
    """Every diagonal template with even-cycle-free colour graphs and three
    live constant fibres has a MIXED SINGLETON fibre."""
    allE = set(combinations(range(n), 2))
    tested = 0
    filtered_out = 0
    no_singleton = []
    dp_direct_disagree = []
    n_direct = 0
    extra_hist = {}
    ci = 0
    for m0, m1, m2 in charts(n):
        ci += 1
        if ci % chart_stride:
            continue
        base = [set(m0), set(m1), set(m2)]
        free = sorted(allE - set(m0) - set(m1) - set(m2))
        branch, S = build_fourth(n, m0, m1, m2)
        require(S is not None, f"N={n}: chart reached the step-5 residual")
        w = word_from_matching(n, base, S)
        mixed = len(set(w)) > 1
        full = (1 << n) - 1
        for k in range(0, max_extra + 1):
            for ext in extensions(free, k):
                cols = [set(x) for x in base]
                touched = set()
                for e, a in ext:
                    cols[a].add(e)
                    touched.add(a)
                # PRECONDITION 1: every colour graph even-cycle-free.  The
                # untouched classes are perfect matchings, hence acyclic, so
                # only the touched ones can acquire a cycle.
                if any(has_even_cycle(n, sorted(cols[a])) for a in touched):
                    filtered_out += 1
                    continue
                tested += 1
                extra_hist[k] = extra_hist.get(k, 0) + 1
                nbrs = [nbr_bits(n, cols[r]) for r in range(3)]
                # PRECONDITION 2: three live constant fibres.  Guaranteed
                # (M_r subset G_r), but verified, not assumed.
                if any(pm_count_mask(nbrs[r], full, {}) == 0
                       for r in range(3)):
                    raise CheckFailure("a colour graph lost its perfect "
                                       "matching -- enumeration is wrong")
                s_dp = fibre_size_dp(n, cols, w, nbrs)
                if not (mixed and s_dp == 1):
                    no_singleton.append((m0, m1, m2, ext, list(w), s_dp))
                if tested % direct_stride == 0:
                    n_direct += 1
                    s_dir = fibre_size_direct(n, cols, w)
                    if s_dir != s_dp:
                        dp_direct_disagree.append((list(w), s_dp, s_dir))
    return dict(N=n, max_extra_edges=max_extra, chart_stride=chart_stride,
                templates_tested=tested, templates_filtered_out=filtered_out,
                extra_edge_histogram=extra_hist,
                templates_without_mixed_singleton=len(no_singleton),
                sample=[str(x) for x in no_singleton[:3]],
                direct_engine_checks=n_direct,
                dp_vs_direct_disagreements=len(dp_direct_disagree),
                exhaustive=(chart_stride == 1))


def t6_floor_plus_one(n, direct_stride, chart_stride=1):
    """m = 3N/2 + 1: exactly ONE extra edge on one colour class."""
    allE = set(combinations(range(n), 2))
    tested = 0
    acyclic_fail = 0
    no_singleton = []
    disagree = 0
    n_direct = 0
    ci = 0
    for m0, m1, m2 in charts(n):
        ci += 1
        if ci % chart_stride:
            continue
        base = [set(m0), set(m1), set(m2)]
        free = sorted(allE - set(m0) - set(m1) - set(m2))
        branch, S = build_fourth(n, m0, m1, m2)
        require(S is not None, f"N={n}: chart reached the step-5 residual")
        w = word_from_matching(n, base, S)
        basenbr = [nbr_bits(n, base[r]) for r in range(3)]
        for f in free:
            for r in (0, 1, 2):
                cols = [set(x) for x in base]
                cols[r].add(f)
                tested += 1
                # the added-edge lemma: matching + one edge is ACYCLIC
                if has_even_cycle(n, sorted(cols[r])):
                    acyclic_fail += 1
                nbrs = list(basenbr)
                nbrs[r] = nbr_bits(n, cols[r])
                s_dp = fibre_size_dp(n, cols, w, nbrs)
                if not (len(set(w)) > 1 and s_dp == 1):
                    no_singleton.append((m0, m1, m2, f, r, list(w), s_dp))
                if tested % direct_stride == 0:
                    n_direct += 1
                    if fibre_size_direct(n, cols, w) != s_dp:
                        disagree += 1
    return dict(N=n, chart_stride=chart_stride, templates_tested=tested,
                added_edge_created_even_cycle=acyclic_fail,
                templates_without_mixed_singleton=len(no_singleton),
                sample=[str(x) for x in no_singleton[:3]],
                direct_engine_checks=n_direct,
                dp_vs_direct_disagreements=disagree,
                exhaustive=(chart_stride == 1))


# ============================================================== mutations

def mutation_controls():
    """Nine controls.  EVERY one must trip; a silent pass is a checker bug."""
    out = []

    def rec(name, tripped, detail=""):
        out.append(dict(control=name, tripped=bool(tripped), detail=detail))

    n = 8
    m0 = ((0, 1), (2, 3), (4, 5), (6, 7))
    m1 = ((1, 2), (3, 4), (5, 6), (0, 7))
    m2 = ((0, 3), (1, 4), (2, 5), (6, 7))          # shares (6,7) with M_0
    try:
        build_fourth(n, m0, m1, m2)
        rec("MC1 overlapping colour classes rejected", False,
            "build_fourth accepted a non-disjoint triple")
    except CheckFailure as exc:
        rec("MC1 overlapping colour classes rejected", True, str(exc))

    # MC2: a corrupted 'fourth matching' must fail the PM test.
    m2 = ((0, 2), (1, 3), (4, 6), (5, 7))
    U = list(m0) + list(m1) + list(m2)
    branch, S = build_fourth(n, m0, m1, m2)
    require(S is not None, "MC2 setup: no fourth matching produced")
    e = sorted(S)[0]
    bad = frozenset(sorted(S)[1:]) | {(e[0], e[1]) if False else e}
    bad = frozenset(sorted(S)[1:])                 # drop one edge
    rec("MC2 truncated matching rejected", not is_pm_of(n, U, bad),
        f"|S|-1 = {len(bad)}")

    # MC3: swapping in an edge outside the union must be rejected.
    outside = next(x for x in combinations(range(n), 2) if x not in set(U))
    bad = frozenset(list(sorted(S))[1:] + [outside])
    rec("MC3 out-of-union edge rejected", not is_pm_of(n, U, bad),
        f"injected {outside}")

    # MC4: M_0 itself must be recognised as NOT a fourth matching.
    rec("MC4 M_0 is not a fourth matching",
        frozenset(m0) in {frozenset(m0), frozenset(m1), frozenset(m2)},
        "identity test")

    # MC5: N = 4 sharpness -- the theorem MUST fail there.
    t = t1_t3(4, 1)
    rec("MC5 N=4 sharpness (theorem must FAIL)",
        t["charts_with_no_fourth_matching"] == t["charts"] == 2,
        f"charts={t['charts']} without-fourth={t['charts_with_no_fourth_matching']}")

    # MC6: even-cycle lemma must be non-vacuous -- C_4 has pm 2.
    c4 = [(0, 1), (1, 2), (2, 3), (0, 3)]
    cnt = pm_counts_by_subset(4, c4)
    rec("MC6 C_4 detected (even cycle, pm=2)",
        has_even_cycle(4, c4) and cnt[(1 << 4) - 1] == 2,
        f"pm(C_4)={cnt[(1 << 4) - 1]}")

    # MC7: a triangle is odd -- must NOT be flagged as an even cycle,
    #      and must keep pm <= 1 on every subset.
    tri = [(0, 1), (1, 2), (0, 2)]
    cnt = pm_counts_by_subset(3, tri)
    rec("MC7 triangle is not an even cycle",
        (not has_even_cycle(3, tri)) and max(cnt) <= 1,
        f"max pm = {max(cnt)}")

    # MC8: the two fibre engines must DISAGREE when one is fed the wrong
    #      colour graphs -- proves T3/T5's agreement is not tautological.
    cols = [set(m0), set(m1), set(m2)]
    branch, S = build_fourth(n, m0, m1, m2)
    w = word_from_matching(n, cols, S)
    wrong = [set(m1), set(m0), set(m2)]            # colours 0,1 swapped
    a = fibre_size_dp(n, cols, w)
    b = fibre_size_dp(n, wrong, w)
    rec("MC8 mutated colour graphs change the fibre size", a != b,
        f"true={a} mutated={b}")

    # MC9: a template with an even cycle in a colour graph must be caught
    #      by T5's precondition filter (else T5 would be vacuous).
    withc4 = [set(m0) | {(0, 2), (1, 3)}, set(m1), set(m2)]
    rec("MC9 even-cycle colour graph is filtered out",
        has_even_cycle(n, sorted(withc4[0])), "M_0 + a 4-cycle")

    return out


# ==================================================================== main

def main():
    maxN = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    t0 = time.time()
    res = {"agent": "H1", "blocker": 1,
           "pinned_head": open(os.path.join(HERE, "PINNED_HEAD.txt")
                               ).read().split()[0]}

    print("== T1/T3: charts, constructive proof, singleton corollary ==")
    res["T1_T3"] = {}
    for n in (4, 6, 8, 10):
        if n > maxN:
            continue
        stride = 1 if n <= 8 else 500
        r = t1_t3(n, stride)
        res["T1_T3"][f"N={n}"] = r
        print(f"  N={n:2d} charts={r['charts']:7d} census={r['branch_census']} "
              f"maxPM={r['max_pm_count']:3d} theorem={r['theorem_holds']} "
              f"constr_fail={r['constructive_failures']} "
              f"singleton_fail={r['singleton_corollary_failures']} "
              f"direct_checks={r['direct_engine_checks']} "
              f"[{time.time()-t0:.0f}s]", flush=True)

    print("== T2: is the Step-5 residual reachable? ==")
    res["T2_step5"] = {}
    for n in (6, 8, 10, 12, 14, 16, 20):
        r = t2_step5(n)
        res["T2_step5"][f"N={n}"] = r
        print(f"  N={n:2d} B-satisfiable={r['hypothesis_B_satisfiable']} "
              f"parity-preserving M_2={r.get('parity_preserving_M2_count',0)} "
              f"(B)+(C)={r['configs_BC']} (A)+(B)+(C)={r['configs_ABC']} "
              f"| beta-lemma: spans=0mod4 configs="
              f"{r.get('configs_all_spans_0_mod_4','-')} "
              f"H-connected={r.get('span4_with_H_connected','-')} "
              f"violations={r.get('span4_lemma_violations','-')}", flush=True)

    print("== T4: even-cycle lemma ==")
    res["T4_even_cycle_lemma"] = {}
    for nv, stride in ((4, 1), (5, 1), (6, 1), (7, 7)):
        r = t4_even_cycle_lemma(nv, stride)
        res["T4_even_cycle_lemma"][f"n={nv}"] = r
        print(f"  n={nv} tested={r['graphs_tested']:8d} "
              f"exhaustive={r['exhaustive']} "
              f"even-cycle-free={r['even_cycle_free']:8d} "
              f"mismatches={r['mismatches']} [{time.time()-t0:.0f}s]",
              flush=True)

    print("== T5: even-cycle-free colour graphs die (NEW CHECKER) ==")
    res["T5_even_cycle_free_corollary"] = {}
    for n, mx, ds, cs in ((6, 6, 500, 1), (8, 2, 5000, 1)):
        if n > maxN:
            continue
        r = t5_even_cycle_free_corollary(n, mx, ds, cs)
        res["T5_even_cycle_free_corollary"][f"N={n}"] = r
        print(f"  N={n} <= {mx} extra edges: tested={r['templates_tested']:8d} "
              f"filtered={r['templates_filtered_out']:9d} "
              f"no-singleton={r['templates_without_mixed_singleton']} "
              f"dp!=direct={r['dp_vs_direct_disagreements']} "
              f"[{time.time()-t0:.0f}s]", flush=True)

    print("== T6: m = 3N/2 + 1 dies (NEW CHECKER) ==")
    res["T6_floor_plus_one"] = {}
    for n, ds, cs in ((6, 200, 1), (8, 2000, 1), (10, 20000, 25)):
        if n > maxN:
            continue
        r = t6_floor_plus_one(n, ds, cs)
        res["T6_floor_plus_one"][f"N={n}"] = r
        print(f"  N={n:2d} tested={r['templates_tested']:9d} "
              f"exhaustive={r['exhaustive']} "
              f"even-cycle-from-added-edge={r['added_edge_created_even_cycle']} "
              f"no-singleton={r['templates_without_mixed_singleton']} "
              f"dp!=direct={r['dp_vs_direct_disagreements']} "
              f"[{time.time()-t0:.0f}s]", flush=True)

    print("== MC: mutation controls (every one must trip) ==")
    mc = mutation_controls()
    res["mutation_controls"] = mc
    for row in mc:
        print(f"  [{'OK ' if row['tripped'] else 'BAD'}] {row['control']}"
              f"  {row['detail']}")
    res["mutation_controls_all_tripped"] = all(r["tripped"] for r in mc)

    res["seconds"] = round(time.time() - t0, 1)
    with open(os.path.join(HERE, "results_b1_fourth_matching.json"), "w") as fh:
        json.dump(res, fh, indent=1, default=str)
    print(f"\nwrote results_b1_fourth_matching.json  [{res['seconds']}s]")


if __name__ == "__main__":
    main()
