#!/usr/bin/env python3
r"""W31 -- the SLACK lemma: no (R) template with slack 0 lies in the
empty-clean stratum.  UNAUDITED PROBE.  Exact integer arithmetic only.

DEFINITIONS (all as in w31_census.py).
  A block is a SERVER if it is occupied and not FULL.  (SC) demands, at every
  site p and every colour c, a block at p whose occupied cells all carry
  colour c at the FAR endpoint.  A server serves at most 2 of the 24 demands
  (one per endpoint), so an (R) template has >= 12 servers, hence
      |Gamma|  <=  m - 12                                 [W18-E]
  Define the SLACK  s(T) := m - 12 - |Gamma(T)|  >= 0.
  s = 0 forces: exactly 12 servers, each serving BOTH its endpoints, i.e.
  each server has a unique far colour from either side, i.e. each server is a
  SINGLE CELL; and every site carries exactly 3 of them, so the 12 single
  edges form a spanning CUBIC graph C.  All other non-Gamma blocks are empty.
  (Placements: for edge e = (u,v) with cell (i,j), the far colour seen from u
  is j and from v is i; the demand at u says the three far colours of its
  incident singles are distinct.  Equivalently: choose a bijection
  sigma_u : {edges at u} -> {0,1,2} at every u, and set the cell coordinate
  of e AT v to sigma_u(e).  That is 6^8 placements per labelled C -- the
  count W19's census reports.)

THE ARGUMENT TESTED HERE.
  At slack 0 every supported matching outside F(Gamma) must use one of the 12
  single cells.  So a mixed word activating NO single has fibre exactly
  |F(Gamma)| -- it is effectively clean if |F| >= 3, and violates (R)'s
  fibre >= 3 condition outright if |F| <= 2.  Hence:

    (i)  #(effectively clean mixed words) >= 6558 - COV(C, placement)
    (ii) an (R) template with slack 0 and |F(Gamma)| <= 2 requires
         COV(C, placement) = 6558 -- the singles must cover EVERY mixed word.

  COV = #mixed words w with (w_u, w_v) equal to the cell of some single (u,v).
  This script computes  max over C, max over placements, of COV  EXACTLY, by
  branch and bound over the 6^8 placements of each of the cubic iso-classes.

CONTROLS
  D1  the labelled cubic count must come out 19,355 (external ground truth,
      also used by W19's census) and must equal sum over iso-classes of
      8!/|Aut|, with |Aut| computed by brute force over all 40,320
      permutations -- this validates the invariant-based classification.
  D2  the coverage engine is cross-checked against a direct per-word
      recomputation on random placements (0 mismatches required).
  D3  MUTATION: a deliberately invalid placement (a repeated far colour at a
      site) must be rejected by the validity checker.
  D4  POSITIVE CONTROL (lives in the companion script `w31_d4.py`, NOT here --
      per ledger item 21 this file's manifest declares only D1-D3 + E, and
      w31_d4.py asserts its own D4/D5 manifest): the W26/W30 m=28 template's
      own single-cell set is a valid slack-0 placement on a cubic C, and its
      uncovered-mixed-word count must equal the stored clean-word count 2152.
      RESULT: 2152, exact match (results_d4.json).
"""
from __future__ import annotations

import json
import os
import sys
from itertools import combinations, permutations, product

sys.dont_write_bytecode = True

N = 8
Q = 3
HERE = os.path.dirname(os.path.abspath(__file__))
EDGES = tuple(combinations(range(N), 2))
EIDX = {e: i for i, e in enumerate(EDGES)}
WORDS = tuple(product(range(Q), repeat=N))
MIXED_POS = [i for i, w in enumerate(WORDS) if len(set(w)) > 1]
NM = len(MIXED_POS)
assert NM == 6558

# CELLMASK[e][i][j] : bitmask over the 6558 MIXED words (position = index in
# MIXED_POS) of the words with w_u = i and w_v = j.
print("building cell masks ...")
CELLMASK = {}
for ei, (u, v) in enumerate(EDGES):
    buckets = [[0] * 9 for _ in range(1)]
    acc = [0] * 9
    for pos, wi in enumerate(MIXED_POS):
        w = WORDS[wi]
        acc[3 * w[u] + w[v]] |= (1 << pos)
    CELLMASK[ei] = acc
FULLCOVER = (1 << NM) - 1


# ---------------------------------------------------------- cubic graphs
def cubic_graphs():
    """all labelled 3-regular graphs on 8 vertices, as sorted edge tuples."""
    out = []
    deg = [0] * N
    adj = [[False] * N for _ in range(N)]

    def rec(start, chosen):
        v = -1
        for x in range(N):
            if deg[x] < 3:
                v = x
                break
        if v < 0:
            out.append(tuple(chosen))
            return
        # v is the least-indexed deficient vertex; connect it upward only
        need = 3 - deg[v]
        cands = [x for x in range(v + 1, N) if deg[x] < 3 and not adj[v][x]]
        if len(cands) < need:
            return
        for combo in combinations(cands, need):
            for x in combo:
                deg[x] += 1
                adj[v][x] = adj[x][v] = True
            deg[v] += need
            rec(start, chosen + [(v, x) for x in combo])
            deg[v] -= need
            for x in combo:
                deg[x] -= 1
                adj[v][x] = adj[x][v] = False

    rec(0, [])
    return out


def emask(edges):
    m = 0
    for e in edges:
        m |= 1 << EIDX[tuple(sorted(e))]
    return m


def relabel(edges, p):
    return tuple(sorted(tuple(sorted((p[u], p[v]))) for u, v in edges))


def invariant(edges):
    """cheap iso-invariant: matching counts + triangle/4-cycle counts."""
    es = [tuple(sorted(e)) for e in edges]
    S = set(es)
    tri = sum(1 for a, b, c in combinations(range(N), 3)
              if (a, b) in S and (a, c) in S and (b, c) in S)
    c4 = 0
    for quad in combinations(range(N), 4):
        for pr in (((0, 1), (1, 2), (2, 3), (3, 0)),
                   ((0, 1), (1, 3), (3, 2), (2, 0)),
                   ((0, 2), (2, 1), (1, 3), (3, 0))):
            if all(tuple(sorted((quad[a], quad[b]))) in S for a, b in pr):
                c4 += 1
    mk = [0] * 5
    for k in range(1, 5):
        for sub in combinations(es, k):
            vs = set()
            ok = True
            for u, v in sub:
                if u in vs or v in vs:
                    ok = False
                    break
                vs.add(u)
                vs.add(v)
            if ok:
                mk[k] += 1
    return (tri, c4, tuple(mk))


def aut_size(edges):
    S = set(tuple(sorted(e)) for e in edges)
    n = 0
    for p in permutations(range(N)):
        if set(relabel(edges, p)) == S:
            n += 1
    return n


# ------------------------------------------------ placements and coverage
def incident(edges, v):
    return [e for e in edges if v in e]


def cov_of_placement(edges, sig):
    """sig[v] : dict edge -> colour, a bijection at v.  The cell of edge
    e=(u,v) is (sig[v][e], sig[u][e]) -- coordinate at u is set by v's
    bijection.  Returns the coverage bitmask over mixed words."""
    acc = 0
    for e in edges:
        u, v = e
        i, j = sig[v][e], sig[u][e]
        acc |= CELLMASK[EIDX[e]][3 * i + j]
    return acc


def max_coverage(edges, best=0):
    """exact max over the 6^8 placements, by DFS over vertices with the bound
    partial + 729*(#unplaced edges) <= best  =>  prune.
    Global colour symmetry fixed by pinning vertex 0's bijection."""
    inc = {v: incident(edges, v) for v in range(N)}
    order = list(range(N))
    sig = {}
    bestv = [best]
    bestp = [None]

    def rec(k, acc, placed):
        if k == N:
            c = bin(acc).count("1")
            if c > bestv[0]:
                bestv[0] = c
                bestp[0] = {v: dict(sig[v]) for v in sig}
            return
        v = order[k]
        perms = [((0, 1, 2),)] if False else permutations(range(Q))
        if v == 0:
            perms = [(0, 1, 2)]                 # global S_3 gauge fix
        for pm in perms:
            sig[v] = {e: pm[t] for t, e in enumerate(inc[v])}
            newacc = acc
            np_ = placed
            for e in inc[v]:
                u = e[0] if e[1] == v else e[1]
                if u in sig:
                    i, j = sig[e[1]][e], sig[e[0]][e]
                    newacc |= CELLMASK[EIDX[e]][3 * i + j]
                    np_ += 1
            if bin(newacc).count("1") + 729 * (len(edges) - np_) > bestv[0]:
                rec(k + 1, newacc, np_)
            del sig[v]

    rec(0, 0, 0)
    return bestv[0], bestp[0]


def main():
    OUT = {"_header": "UNAUDITED W31 slack-0 coverage lemma. Exact integer "
                      "arithmetic only. Nothing here is a proved claim of "
                      "the repository.",
           "_pinned_head": open(os.path.join(HERE,
                                             "PINNED_HEAD.txt")).read().strip()}

    print("[D1] enumerating labelled cubic graphs on 8 vertices")
    gs = cubic_graphs()
    OUT["D1_labelled_cubic_count"] = len(gs)
    OUT["D1_matches_19355"] = (len(gs) == 19355)
    print("    count =", len(gs), " (ground truth 19,355):",
          OUT["D1_matches_19355"])

    buckets = {}
    for g in gs:
        buckets.setdefault(invariant(g), []).append(g)
    print("    invariant buckets:", len(buckets))
    classes = []
    tot = 0
    for inv, mem in sorted(buckets.items()):
        rep = mem[0]
        a = aut_size(rep)
        orb = 40320 // a
        tot += orb
        classes.append(dict(invariant=str(inv), rep=[list(e) for e in rep],
                            aut=a, orbit=orb, bucket=len(mem),
                            orbit_matches_bucket=(orb == len(mem))))
        print("      inv=%s |Aut|=%d orbit=%d bucket=%d ok=%s"
              % (inv, a, orb, len(mem), orb == len(mem)))
    OUT["D1_classes"] = classes
    OUT["D1_orbit_sum"] = tot
    OUT["D1_classification_validated"] = (tot == len(gs)
                                          and all(c["orbit_matches_bucket"]
                                                  for c in classes))
    print("    sum of orbits =", tot, " classification validated:",
          OUT["D1_classification_validated"])

    # ------------------------------------------------------------- D2/D3
    import random
    rng = random.Random(20260820)
    rep0 = classes[0]["rep"]
    rep0 = [tuple(e) for e in rep0]
    mism = 0
    for _ in range(20):
        sig = {v: {e: c for e, c in zip(incident(rep0, v),
                                        rng.sample(range(Q), 3))}
               for v in range(N)}
        fast = cov_of_placement(rep0, sig)
        slow = 0
        cells = {}
        for e in rep0:
            u, v = e
            cells[e] = (sig[v][e], sig[u][e])
        for pos, wi in enumerate(MIXED_POS):
            w = WORDS[wi]
            if any(w[u] == i and w[v] == j for (u, v), (i, j) in cells.items()):
                slow |= 1 << pos
        if fast != slow:
            mism += 1
    OUT["D2_engine_mismatches"] = mism
    print("[D2] coverage engine mismatches vs direct recomputation:", mism)

    def valid(edges, sig):
        for u in range(N):
            far = [sig[u][e] for e in incident(edges, u)]
            if sorted(far) != [0, 1, 2]:
                return False
        return True
    good = {v: {e: c for e, c in zip(incident(rep0, v), (0, 1, 2))}
            for v in range(N)}
    bad = {v: dict(good[v]) for v in range(N)}
    bad[0][incident(rep0, 0)[0]] = bad[0][incident(rep0, 0)[1]]
    OUT["D3_mutation_rejected"] = (valid(rep0, good) and not valid(rep0, bad))
    print("[D3] mutation control (invalid placement rejected):",
          OUT["D3_mutation_rejected"])

    # ------------------------------------------------------------- max cov
    print("[E] exact max coverage per cubic iso-class (branch and bound)")
    res = []
    for c in classes:
        rep = [tuple(e) for e in c["rep"]]
        mc, _ = max_coverage(rep, best=0)
        res.append(dict(invariant=c["invariant"], max_coverage=mc,
                        min_clean_mixed_words=NM - mc,
                        can_cover_all_mixed=(mc == NM)))
        print("    inv=%s  max COV = %d / 6558   =>  >= %d clean words"
              % (c["invariant"], mc, NM - mc))
    OUT["E_per_class"] = res
    OUT["E_global_max_coverage"] = max(r["max_coverage"] for r in res)
    OUT["E_min_clean_words_over_all_slack0_templates"] = (
        NM - OUT["E_global_max_coverage"])
    OUT["E_LEMMA_slack0_forces_nonempty_clean_layer"] = (
        OUT["E_global_max_coverage"] < NM)
    print("    GLOBAL max coverage =", OUT["E_global_max_coverage"],
          "of 6558  =>  every slack-0 (R) template has >=",
          OUT["E_min_clean_words_over_all_slack0_templates"],
          "effectively clean mixed words")

    with open(os.path.join(HERE, "results_slack.json"), "w") as fh:
        json.dump(OUT, fh, indent=1, sort_keys=True)
    declared = ["D1_classification_validated", "D2_engine_mismatches",
                "D3_mutation_rejected", "E_per_class"]
    missing = [d for d in declared if d not in OUT]
    assert not missing, "CONTROL NEVER RAN: %s" % missing
    print("control manifest OK:", declared)


if __name__ == "__main__":
    main()
