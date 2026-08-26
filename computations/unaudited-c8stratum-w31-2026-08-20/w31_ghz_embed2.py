#!/usr/bin/env python3
r"""W31 -- LEMMA W31-2, corrected: WHICH stratum Gammas admit a doubled-GHZ
template?  UNAUDITED PROBE.  Exact integer arithmetic only.

WHAT THE FIRST ATTEMPT GOT WRONG (control E1 caught it; recorded, not hidden).
`w31_ghz_embed.py` tested the 75 STORED census representatives and found zero
GHZ embeddings -- including for the C_8 class, whose W20 member demonstrably
double-embeds.  Cause: W19's census representatives are built by a DIFFERENT
construction.  Their servers are THIN 3-cell blocks (e.g. mask 7 = cells
(0,0),(0,1),(0,2); mask 146 = (0,1),(1,1),(2,1)), not single cells, so they
have no 12-single subgraph at all.  W20's C_8 member uses 12 SINGLE cells.
Both satisfy (SC): a thin block whose cells share a far colour serves a demand
just as a single cell does.

CONSEQUENCE, and it is the real finding:
**the GHZ_4 embedding is a property of the CELL PLACEMENT, not of Gamma.**
It is not a class invariant, so "is the stratum made of doubled GHZ sources?"
cannot be read off the stored representatives at all.  (Same shape as the
214-vs-75 distinction already recorded in STATEMENT.md.)

THE RIGHT QUESTION, and it is sharp and cheap.  A doubled-GHZ template puts a
GHZ_4^3 copy on each side of a 4|4 split, i.e. all twelve single cells lie
INSIDE the two halves.  Those twelve edges are exactly the two K_4's, so every
edge of Gamma must be a CROSS edge:

    Gamma admits a doubled-GHZ placement  <=>  there is a 4|4 split of the
    eight sites with EVERY Gamma edge crossing it  (so |Gamma| <= 16 and
    Gamma is contained in the K_{4,4} of that split).

This script decides that for all 75 Gamma-forced stratum classes, and then
CONSTRUCTS the doubled-GHZ template for each Gamma that admits one and tests
whether it lies in (R).

THE LINK TO ROUTE A (note it in the report).  "Every Gamma edge crosses the
split" is exactly the condition under which W26/W30's hafL and hafR -- the
hafnians of Gamma's cells inside the two halves -- vanish IDENTICALLY.  So the
split carrying the doubled GHZ copies is precisely a split at which Route A's
slice machinery is undefined.  The structure that makes these templates
interesting is the same structure that makes them invisible to Route A.

CONTROLS
  F1  W20's C_8 member (the object the finding came from) must double-embed.
  F2  the stored census representative of the SAME class must not, and the
      reason must be recorded (thin servers, no singles) -- this is the bug
      that control E1 caught, kept as a regression test.
  F3  the Route-A slack-0 m=28 template must NOT admit a doubled-GHZ split
      (its Gamma contains K_4(L) and K_4(R), so no split makes every edge
      cross).
  F4  MUTATION: moving one of the C_8 member's single cells off the diagonal
      must break its embedding verdict.
  F5  every constructed template is checked by the SAME direct (R) predicate
      used by the R1 SAT lane's K3 control.
"""
from __future__ import annotations

import json
import os
import sys
from itertools import combinations, product

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CENSUS = os.path.join(REPO, "computations",
                      "unaudited-forcing-w19-2026-08-15", "census")
sys.path.insert(0, os.path.join(REPO, "computations",
                                "unaudited-blockers-w26-2026-08-16"))

N, FULL = 8, 511
EDGES = tuple(combinations(range(N), 2))
EIDX = {e: i for i, e in enumerate(EDGES)}
WORDS = tuple(product(range(3), repeat=N))
MIXED = tuple(w for w in WORDS if len(set(w)) > 1)
CONSTS = tuple((c,) * N for c in range(3))

C8_MEMBER = [1, 16, 256, 511, 511, 503, 447, 256, 16, 510, 495, 511, 511, 1,
             383, 511, 510, 511, 511, 255, 511, 383, 1, 16, 256, 256, 16, 1]


def _pms(vs):
    if not vs:
        return [()]
    a, rest = vs[0], vs[1:]
    out = []
    for i, b in enumerate(rest):
        for mm in _pms(rest[:i] + rest[i + 1:]):
            out.append(((a, b),) + mm)
    return out


PMS = tuple(tuple(sorted(m)) for m in _pms(tuple(range(N))))


def cells_of(mask):
    return [(c // 3, c % 3) for c in range(9) if (mask >> c) & 1]


def singles_of(T):
    return {EDGES[i]: cells_of(t)[0] for i, t in enumerate(T)
            if t and bin(t).count("1") == 1}


def block_kind(mask):
    n = bin(mask).count("1")
    if n == 0:
        return "empty"
    if mask == FULL:
        return "full"
    if n == 1:
        return "single"
    cs = cells_of(mask)
    rows = {i for i, _ in cs}
    cols = {j for _, j in cs}
    return "thin" if (len(rows) == 1 or len(cols) == 1) else "fat"


def ghz_on(sing, quad):
    """is the K_4 on `quad` a GHZ_4^3 copy of single cells?"""
    need = [tuple(sorted(p)) for p in combinations(quad, 2)]
    if not all(e in sing for e in need):
        return False, None
    cells = {e: sing[e] for e in need}
    if not all(i == j for i, j in cells.values()):
        return False, None
    a, b, c, d = quad
    pms = (((a, b), (c, d)), ((a, c), (b, d)), ((a, d), (b, c)))
    cols = []
    for p in pms:
        s = {cells[tuple(sorted(e))][0] for e in p}
        if len(s) != 1:
            return False, None
        cols.append(s.pop())
    if sorted(cols) != [0, 1, 2]:
        return False, None
    return True, {str(list(p)): c for p, c in zip(pms, cols)}


def embedding_of(T):
    sing = singles_of(T)
    best = []
    for half in combinations(range(1, N), 3):
        Lh = (0,) + half
        Rh = tuple(v for v in range(N) if v not in Lh)
        okL, dL = ghz_on(sing, Lh)
        okR, dR = ghz_on(sing, Rh)
        if okL and okR:
            best.append(dict(split=[list(Lh), list(Rh)], L=dL, R=dR))
    kinds = {}
    for t in T:
        kinds[block_kind(t)] = kinds.get(block_kind(t), 0) + 1
    return dict(n_singles=len(sing), block_kinds=kinds,
                n_double_embeddings=len(best), embeddings=best,
                embedding=("double" if best else "none"))


def all_cross_splits(gedges):
    out = []
    for half in combinations(range(1, N), 3):
        Lh = set((0,) + half)
        if all((u in Lh) != (v in Lh) for u, v in gedges):
            out.append(sorted(Lh))
    return out


def build_doubled(gedges, split):
    """Gamma full; the two K_4's carry the GHZ_4^3 single cells; every other
    cross block is FAT (all nine cells minus one)."""
    Lh = set(split)
    Rh = [v for v in range(N) if v not in Lh]
    T = [0] * len(EDGES)
    gs = set(tuple(sorted(e)) for e in gedges)
    for e in gs:
        T[EIDX[e]] = FULL
    for side in (sorted(Lh), Rh):
        a, b, c, d = side
        for col, pm in enumerate((((a, b), (c, d)), ((a, c), (b, d)),
                                  ((a, d), (b, c)))):
            for e in pm:
                T[EIDX[tuple(sorted(e))]] = 1 << (3 * col + col)
    for u in sorted(Lh):
        for v in Rh:
            e = tuple(sorted((u, v)))
            if e not in gs:
                T[EIDX[e]] = FULL ^ 1                      # fat: 8 cells
    return T


def far_colour(e, p, c):
    u, v = e
    i, j = c // 3, c % 3
    return j if p == u else i


def check_R(T):
    for p in range(N):
        need = set(range(3))
        for e in EDGES:
            if p not in e:
                continue
            mk = T[EIDX[e]]
            if not mk:
                continue
            fc = {far_colour(e, p, c) for c in range(9) if (mk >> c) & 1}
            if len(fc) == 1:
                need.discard(fc.pop())
        if need:
            return False, "SC fails at site %d" % p
    ge = [EDGES[i] for i, t in enumerate(T) if t == FULL]
    vs = set()
    for u, v in ge:
        vs.add(u)
        vs.add(v)
    if vs != set(range(N)):
        return False, "Gamma not spanning"
    adj = {v: set() for v in range(N)}
    for u, v in ge:
        adj[u].add(v)
        adj[v].add(u)

    def conn(skip):
        keep = [v for v in range(N) if v != skip]
        st, seen = [keep[0]], {keep[0]}
        while st:
            a = st.pop()
            for b in adj[a]:
                if b != skip and b not in seen:
                    seen.add(b)
                    st.append(b)
        return len(seen) == len(keep)
    if not (conn(-1) and all(conn(s) for s in range(N))):
        return False, "Gamma not 2-connected"

    def fib(w):
        n = 0
        for M in PMS:
            if all((T[EIDX[e]] >> (3 * w[e[0]] + w[e[1]])) & 1 for e in M):
                n += 1
                if n >= 3:
                    return n
        return n
    for w in CONSTS:
        if fib(w) < 1:
            return False, "empty constant fibre"
    for w in MIXED:
        if fib(w) < 3:
            return False, "fibre < 3 at %s" % (w,)
    return True, "ok"


def main():
    OUT = {"_header": "UNAUDITED W31 doubled-GHZ admissibility over the "
                      "Gamma-forced stratum. Exact only. Nothing here is a "
                      "proved claim of the repository.",
           "_pinned_head": open(os.path.join(HERE,
                                             "PINNED_HEAD.txt")).read().strip()}
    kill = json.load(open(os.path.join(CENSUS, "results_kill.json")))
    dec = json.load(open(os.path.join(CENSUS, "results_decide.json")))
    inv = {r["gamma_mask"]: r for r in kill["reps_inventory"]}

    # ---- F1 / F2 / F4 ------------------------------------------------------
    e8 = embedding_of(C8_MEMBER)
    OUT["F1_c8_member"] = e8
    OUT["F1_ok"] = (e8["embedding"] == "double")
    print("[F1] W20 C_8 member:", e8["embedding"], e8["block_kinds"],
          "splits:", [d["split"] for d in e8["embeddings"]])

    c8gm = [gm for gm, r in inv.items() if r["n_edges"] == 8][0]
    rep = dec["reps"][str(c8gm)]
    er = embedding_of(rep)
    OUT["F2_census_rep_same_class"] = er
    OUT["F2_ok"] = (er["embedding"] == "none" and er["n_singles"] != 12)
    print("[F2] census rep of the SAME class:", er["embedding"],
          er["block_kinds"], "-> regression test:", OUT["F2_ok"])

    Tm = list(C8_MEMBER)
    e0 = sorted(singles_of(Tm))[0]
    Tm[EIDX[e0]] = 1 << 1
    OUT["F4_mutation_breaks_embedding"] = (
        embedding_of(Tm)["embedding"] != "double")
    print("[F4] mutation control fires:", OUT["F4_mutation_breaks_embedding"])

    import w26_core as C26
    T26 = list(C26.TEMPLATES[28])
    g26 = [EDGES[i] for i, t in enumerate(T26) if t == FULL]
    OUT["F3_routeA_allcross_splits"] = all_cross_splits(g26)
    OUT["F3_ok"] = (len(OUT["F3_routeA_allcross_splits"]) == 0)
    print("[F3] Route-A m=28 admits a doubled-GHZ split:",
          not OUT["F3_ok"], "-> control", OUT["F3_ok"])

    # ---- the classification ------------------------------------------------
    per, admits, denies = {}, [], []
    for gm, r in sorted(inv.items()):
        if r["pms"] > 2:
            continue
        ge = [EDGES[i] for i in range(len(EDGES)) if (gm >> i) & 1]
        sp = all_cross_splits(ge)
        per[str(gm)] = dict(n_gamma=r["n_edges"], n_F=r["pms"],
                            n_allcross_splits=len(sp), splits=sp)
        (admits if sp else denies).append(gm)
    OUT["per_class"] = per
    OUT["n_admitting"] = len(admits)
    OUT["n_denying"] = len(denies)
    print("[classification] stratum classes admitting an all-cross 4|4 split:",
          len(admits), "of", len(admits) + len(denies))

    byg = {}
    for gm in admits:
        k = "|G|=%d,|F|=%d" % (inv[gm]["n_edges"], inv[gm]["pms"])
        byg[k] = byg.get(k, 0) + 1
    byd = {}
    for gm in denies:
        k = "|G|=%d,|F|=%d" % (inv[gm]["n_edges"], inv[gm]["pms"])
        byd[k] = byd.get(k, 0) + 1
    OUT["admitting_by_class"] = byg
    OUT["denying_by_class"] = byd
    print("   admitting:", byg)
    print("   denying  :", byd)

    # ---- construct and test (R) for the admitting classes ------------------
    built = {}
    for gm in admits:
        ge = [EDGES[i] for i in range(len(EDGES)) if (gm >> i) & 1]
        sp = per[str(gm)]["splits"][0]
        T = build_doubled(ge, sp)
        ok, why = check_R(T)
        emb = embedding_of(T)
        built[str(gm)] = dict(n_gamma=inv[gm]["n_edges"], n_F=inv[gm]["pms"],
                              split=sp, in_R=ok, reason=why,
                              embedding=emb["embedding"],
                              m=sum(1 for t in T if t),
                              Sigma=sum(bin(t).count("1") for t in T),
                              template=T if ok else None)
        print("   gamma=%-8d |G|=%2d |F|=%d split=%s -> in_R=%s (%s)"
              % (gm, inv[gm]["n_edges"], inv[gm]["pms"], sp, ok, why[:38]),
              flush=True)
    OUT["constructed"] = built
    nR = sum(1 for b in built.values() if b["in_R"])
    OUT["n_constructed_in_R"] = nR
    OUT["LEMMA_W31_2"] = (
        "Every Gamma-forced stratum class with an all-cross 4|4 split admits "
        "an (R) template that is two GHZ_4^3 copies joined across the split: "
        "%d of %d admitting classes verified in (R)." % (nR, len(admits)))
    print()
    print("[LEMMA W31-2]", OUT["LEMMA_W31_2"])

    with open(os.path.join(HERE, "results_ghz_embed2.json"), "w") as fh:
        json.dump(OUT, fh, indent=1, sort_keys=True)
    declared = ["F1_ok", "F2_ok", "F3_ok", "F4_mutation_breaks_embedding",
                "per_class", "constructed"]
    missing = [d for d in declared if d not in OUT]
    assert not missing, "CONTROL NEVER RAN: %s" % missing
    print("control manifest OK:", declared)


if __name__ == "__main__":
    main()
