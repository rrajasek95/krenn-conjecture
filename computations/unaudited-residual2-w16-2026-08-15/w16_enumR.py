#!/usr/bin/env python3
"""W16 T4 -- ENUMERATING the residual family (R) at N = 8.

DEFINITION USED (the brief's, verbatim):
  (R1) (SC)-admissible: for every vertex p and colour r there is an incident
       edge pj with S_pj nonempty and EVERY cell of S_pj carrying colour r
       at the far endpoint j;
  (R2) all three constant fibres nonempty;
  (R3) no mixed word has fibre exactly 1;
  (R4) EVERY mixed fibre has size >= 3   (thickness; implies (R3));
  (R5) Gamma(T) = the graph of FULL nine-cell blocks is spanning
       2-connected.

BLOCK TAXONOMY (A2/W8): a nonempty block is
  SINGLE (1 cell)  -> serves the demand (u, j) and the demand (v, i);
  THIN   (>=2 cells, all in one row OR all in one column, i.e. a single far
          colour at exactly one endpoint) -> serves exactly ONE demand;
  FAT    (everything else, in particular every FULL block) -> serves NONE.
Counting the 24 demands:  2*beta + h >= 24,  m = |Gamma| + phi + beta + h,
where phi = #fat-but-not-full blocks.  With m <= 28 this gives

        beta + h >= 12   and   |Gamma| + phi <= 16          (Lemma W16-C)

and, since a spanning 2-connected graph on 8 vertices has >= 8 edges,
8 <= |Gamma| <= 16.

THE THICKNESS SHORTCUT (Lemma W16-D).  Every matching of FULL blocks is
supported on EVERY word, so fibre(w) contains F(Gamma) for all w.  Hence

        |F(Gamma)| >= 3   =>   (R2), (R3) and (R4) hold automatically.

So (R) contains EVERY (SC)-admissible template whose Gamma is spanning
2-connected with at least three perfect matchings.
"""
from __future__ import annotations
import os, sys, json, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w16_core import (EDGES, EIDX, FULL, N, W8_IMMUNE, audit, support,
                      gamma_edges, spanning_2conn, pms_of_graph, MIXED,
                      CONSTS, WORDS, full_pm_indices, extras_at)

HERE = os.path.dirname(os.path.abspath(__file__))


# --------------------------------------------------------- block taxonomy
def cells_of(mask):
    return [(c // 3, c % 3) for c in range(9) if (mask >> c) & 1]


def block_class(mask):
    if mask == 0:
        return "zero"
    cs = cells_of(mask)
    if len(cs) == 1:
        return "single"
    rows = set(i for i, j in cs)
    cols = set(j for i, j in cs)
    if len(rows) == 1 or len(cols) == 1:
        return "thin"
    return "fat"


def far_thin_colour(mask, at_second):
    """the unique far colour if the block is thin at that endpoint, else None"""
    if not mask:
        return None
    seen = set(j if at_second else i for i, j in cells_of(mask))
    return seen.pop() if len(seen) == 1 else None


def sc_demands(T):
    out = {}
    for p in range(N):
        for r in range(3):
            servers = []
            for ei, (u, v) in enumerate(EDGES):
                if p not in (u, v):
                    continue
                col = far_thin_colour(T[ei], at_second=(u == p))
                if col == r:
                    servers.append(ei)
            out[(p, r)] = servers
    return out


def sc_ok(T):
    return all(v for v in sc_demands(T).values())


def audit_R(T):
    fullm = full_pm_indices(T)
    fib = {}
    for w in MIXED:
        fib[w] = len(support(T, w))
    minmix = min(fib.values())
    consts = [len(support(T, w)) for w in CONSTS]
    ge = gamma_edges(T)
    return dict(m=sum(1 for t in T if t),
                sigma=sum(bin(t).count("1") for t in T),
                sc=sc_ok(T), consts_nonzero=all(c > 0 for c in consts),
                min_mixed_fibre=minmix, thick=(minmix >= 3),
                gamma=[list(e) for e in ge], n_gamma=len(ge),
                gamma_pms=len(fullm),
                gamma_span2conn=spanning_2conn(ge),
                classes={c: sum(1 for t in T if block_class(t) == c)
                         for c in ("single", "thin", "fat", "zero")},
                in_R=(sc_ok(T) and all(c > 0 for c in consts)
                      and minmix >= 3 and spanning_2conn(ge)))


# -------------------------------------------- cubic single-cell skeletons
CUBIC_NAMED = {
 "cube_K44_minus_PM (W8's CUBE)":
   [(0,4),(1,5),(2,6),(3,7),(0,5),(1,6),(2,7),(3,4),(0,6),(1,7),(2,4),(3,5)],
 "K4 + K4 (disconnected)":
   [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3),(4,5),(4,6),(4,7),(5,6),(5,7),(6,7)],
 "Wagner V8 = C8 + diameters":
   [(i,(i+1)%8) for i in range(8)] + [(0,4),(1,5),(2,6),(3,7)],
 "Q3 hypercube":
   [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)],
 "C8 + short chords":
   [(i,(i+1)%8) for i in range(8)] + [(0,2),(1,3),(4,6),(5,7)],
 "twisted C8 + chords":
   [(i,(i+1)%8) for i in range(8)] + [(0,3),(1,6),(2,5),(4,7)],
 "Mobius-Kantor-ish C8 + 3-chords":
   [(i,(i+1)%8) for i in range(8)] + [(0,5),(1,4),(2,7),(3,6)],
}


def cubic_graphs():
    """all 3-regular graphs on 8 labelled vertices, up to isomorphism."""
    seen = {}
    verts = list(range(N))
    alledges = list(EDGES)
    out = []
    # backtracking over degrees
    def rec(i, deg, chosen):
        if i == len(alledges):
            if all(d == 3 for d in deg):
                key = canon(chosen)
                if key not in seen:
                    seen[key] = chosen[:]
                    out.append(chosen[:])
            return
        u, v = alledges[i]
        rem = len(alledges) - i
        if sum(3 - d for d in deg) > 2 * rem:
            return
        if deg[u] < 3 and deg[v] < 3:
            deg[u] += 1; deg[v] += 1
            chosen.append((u, v))
            rec(i + 1, deg, chosen)
            chosen.pop(); deg[u] -= 1; deg[v] -= 1
        rec(i + 1, deg, chosen)
    def canon(edges):
        best = None
        es = set(edges)
        for perm in itertools.permutations(range(N)):
            mask = 0
            for (a, b) in es:
                x, y = perm[a], perm[b]
                mask |= 1 << EIDX[(min(x, y), max(x, y))]
            if best is None or mask < best:
                best = mask
        return best
    rec(0, [0] * N, [])
    return out


def proper_3_edge_colourings(edges):
    """proper 3-edge-colourings chi (each vertex sees all three colours)."""
    edges = list(edges)
    inc = {v: [i for i, e in enumerate(edges) if v in e] for v in range(N)}
    col = [None] * len(edges)
    outs = []
    def rec(i):
        if i == len(edges):
            outs.append(col[:])
            return
        u, v = edges[i]
        used = set()
        for j in inc[u] + inc[v]:
            if col[j] is not None:
                used.add(col[j])
        for c in range(3):
            if c in used:
                continue
            col[i] = c
            rec(i + 1)
            col[i] = None
        if len(outs) > 200:
            return
    rec(0)
    return outs


def template_from(cubic, chi, gamma):
    T = [0] * 28
    for i, (u, v) in enumerate(cubic):
        T[EIDX[(u, v)]] = 1 << (3 * chi[i] + chi[i])
    for (u, v) in gamma:
        T[EIDX[(min(u, v), max(u, v))]] = FULL
    return T


def main():
    res = {}
    # ---- 0. the W8 family, re-audited with the (R) predicate
    res["W8_family"] = {m: audit_R(W8_IMMUNE[m]) for m in range(20, 29)}
    for m in range(20, 29):
        a = res["W8_family"][m]
        print("W8 m=%d: in_R=%s  |Gamma|=%d PMs=%d minfib=%d classes=%s"
              % (m, a["in_R"], a["n_gamma"], a["gamma_pms"],
                 a["min_mixed_fibre"], a["classes"]))
    # ---- 1. named cubic skeletons (the single-cell graphs)
    named = []
    for nm, C in CUBIC_NAMED.items():
        C = [(min(u, v), max(u, v)) for (u, v) in C]
        deg = [0] * 8
        for u, v in C:
            deg[u] += 1; deg[v] += 1
        assert len(set(C)) == 12 and all(d == 3 for d in deg), nm
        named.append((nm, C))
    res["n_cubic_named"] = len(named)
    # ---- 2. NEW (R) members: single cells on a cubic C, Gamma = K8 \ C
    found = []
    for ci, (nm, C) in enumerate(named):
        chis = proper_3_edge_colourings(C)
        if not chis:
            continue
        gamma = [e for e in EDGES if e not in set(map(
            lambda t: (min(t), max(t)), C))]
        T = template_from(C, chis[0], gamma)
        a = audit_R(T)
        found.append(dict(name=nm, template=list(T),
                          cubic=[list(e) for e in C], n_colourings=len(chis),
                          **{k: a[k] for k in ("m", "sigma", "sc",
                                               "min_mixed_fibre", "n_gamma",
                                               "gamma_pms",
                                               "gamma_span2conn", "in_R")}))
        print("  %-34s |chi|=%d m=%d Sig=%d SC=%s minfib=%d "
              "|G|=%d PMs=%d 2conn=%s  IN (R): %s"
              % (nm, len(chis), a["m"], a["sigma"], a["sc"],
                 a["min_mixed_fibre"], a["n_gamma"], a["gamma_pms"],
                 a["gamma_span2conn"], a["in_R"]))
    res["complement_family"] = found
    json.dump(res, open(os.path.join(HERE, "results_enumR.json"), "w"),
              indent=1)


if __name__ == "__main__":
    main()
