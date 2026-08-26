#!/usr/bin/env python3
"""W23 T2b -- THE LADDER: at which word-depth does ALL-BLOCKED die?

STRATUM D6(1) [stated explicitly, per ledger item 12].  N = 6 DIAGONAL sources
with every nonzero weight equal to 1:  A_uv = diag(w_0(u,v), w_1(u,v),
w_2(u,v)) with w_c(u,v) in {0,1}.  Such a source IS a triple (G_0, G_1, G_2) of
subgraphs of K_6 (colours may share an edge).  For a diagonal source

    H_B(A)_w = prod_c haf(w_c | S_c),      S_c = w^{-1}(c),

so every equation is combinatorial, and (PROVED HERE):

  * PURE:  haf(w_c) = #PM(G_c) = 1, i.e. G_c has EXACTLY ONE perfect matching.
  * L1 (one-off words): AUTOMATIC on the diagonal stratum -- the off-colour
    star components A_au[d][c] (d != c) all vanish, so L1 reduces to the pure
    equations.  Hence X_1 = X_0 here.
  * L2 (two-off words): reduces to      w_d(a,b) * C^(c)_ab = 0  for d != c,
    i.e.   E(G_d)  disjoint from  cof(G_g)  for every g != d,
    where cof(G) = { pairs {a,b} : G - {a,b} has a perfect matching }.
    (The (c,c) entry of L2 is the pure equation; the off-diagonal entries are
    0 = 0.)  This is the FIRST rung that is not automatic.
  * BALANCED words (the (2,2,2) partitions, the only remaining shape at N = 6):
    no partition of B into three pairs (S_0,S_1,S_2) with S_c in G_c.

THE LADDER at N = 6 on D6(1) is therefore  X_0 = X_1  <  X_2  <  EXACT, and it
has exactly three rungs.  This runner decides, EXHAUSTIVELY:

  (a) |X_2 cap D6(1)| and whether any of its points is ALL-BLOCKED;
  (b) |EXACT cap D6(1)| (must be 0: the six-site theorem, re-derived here on a
      strictly larger stratum than W22's 76^3 matching-triple sweep);
  (c) that ALL-BLOCKED points DO exist one rung lower (X_0), so L2 -- the
      object built in T1 -- is exactly the load-bearing rung.

All verdicts exact (integers + Singular over Q with Rabinowitsch).
"""
from __future__ import annotations

import json
import random
import sys
from fractions import Fraction
from itertools import combinations, permutations, product

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-pure-core-w23-2026-08-15")
sys.path.insert(0, BASE)
sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/"
                   "unaudited-induction2-w22-2026-08-15")
import w23_core as C                                          # noqa: E402
import w22_n6 as N6                                           # noqa: E402

N = 6
EDGES = list(combinations(range(N), 2))
EIDX = {e: i for i, e in enumerate(EDGES)}
RES = {}


def banner(t):
    print("\n" + "=" * 72)
    print(t)
    print("=" * 72)


def emask_edges(mask):
    return [EDGES[i] for i in range(len(EDGES)) if mask >> i & 1]


def build_tables():
    PMfull = [sum(1 << EIDX[C.ekey(*e)] for e in M)
              for M in C.perfect_matchings(tuple(range(N)))]
    PM4 = {}
    for T in combinations(range(N), 4):
        PM4[T] = [sum(1 << EIDX[C.ekey(*e)] for e in M)
                  for M in C.perfect_matchings(T)]
    return PMfull, PM4


def unique_pm_subgraphs(PMfull):
    out = []
    for S in range(1 << len(EDGES)):
        k = 0
        for pm in PMfull:
            if pm & ~S == 0:
                k += 1
                if k > 1:
                    break
        if k == 1:
            out.append(S)
    return out


def cof_mask(S, PM4):
    m = 0
    for a, b in EDGES:
        T = tuple(x for x in range(N) if x not in (a, b))
        if any(pm & ~S == 0 for pm in PM4[T]):
            m |= 1 << EIDX[(a, b)]
    return m


def source_of(triple):
    src = C.zero_source(N)
    for c, G in enumerate(triple):
        for e in emask_edges(G):
            src[e][c][c] = 1
    return src


def balanced_ok(triple):
    """No partition of B into three pairs with S_c an edge of G_c."""
    for M in C.perfect_matchings(tuple(range(N))):
        es = [C.ekey(*e) for e in M]
        for pi in permutations(range(3)):
            if all(triple[pi[k]] >> EIDX[es[k]] & 1 for k in range(3)):
                return False
    return True


def canon(triple, perms):
    best = None
    for p in perms:
        img = []
        for G in triple:
            out = 0
            for a, b in EDGES:
                if G >> EIDX[(a, b)] & 1:
                    out |= 1 << EIDX[C.ekey(p[a], p[b])]
            img.append(out)
        for pi in permutations(range(3)):
            t = (img[pi[0]], img[pi[1]], img[pi[2]])
            if best is None or t < best:
                best = t
    return best


CACHE = {}


def blocking_profile(triple, perms, use_singular=True):
    """Exact witness/blocked verdict at every LIVE pair.  Cached by the
    S_6 x S_3 canonical form."""
    key = canon(triple, perms)
    if key in CACHE:
        return CACHE[key]
    src = source_of(triple)
    rows = []
    for p, q in EDGES:
        if not N6.live(src, p, q):
            rows.append({"pair": [p, q], "live": False})
            continue
        U = tuple(x for x in range(N) if x not in (p, q))
        # detached sites (the detachment law's statistic)
        det_p = sum(1 for a in U
                    if all(x == 0 for r in C.oriented(src, p, a) for x in r))
        det_q = sum(1 for a in U
                    if all(x == 0 for r in C.oriented(src, q, a) for x in r))
        row = {"pair": [p, q], "live": True, "det_p": det_p, "det_q": det_q}
        # cheap sufficient test (W22-X2): on a DIAGONAL source A_py^T u = 0 for
        # a torus u iff A_py = 0, so W(u) is u-independent.
        nz_p = sum(1 for y in range(N) if y != p
                   and any(x != 0 for r in C.oriented(src, p, y) for x in r))
        nz_q = sum(1 for y in range(N) if y != q
                   and any(x != 0 for r in C.oriented(src, q, y) for x in r))
        row["cheap_witness"] = (nz_p <= 2) or (nz_q <= 2)
        if use_singular:
            v, d = N6.decide_pair_general(src, p, q, U, f"D{p}{q}")
            row["verdict"] = v
        else:
            row["verdict"] = "WITNESS" if row["cheap_witness"] else "?"
        rows.append(row)
    live = [r for r in rows if r["live"]]
    prof = {"rows": rows, "n_live": len(live),
            "n_witness": sum(1 for r in live if r.get("verdict") == "WITNESS"),
            "n_blocked": sum(1 for r in live if r.get("verdict") == "BLOCKED")}
    prof["all_blocked"] = prof["n_live"] > 0 and prof["n_witness"] == 0
    CACHE[key] = prof
    return prof


def main():
    rng = random.Random(23081523)
    perms = list(permutations(range(N)))

    banner("(0) build the stratum D6(1)")
    PMfull, PM4 = build_tables()
    U = unique_pm_subgraphs(PMfull)
    COF = {S: cof_mask(S, PM4) for S in U}
    print(f"   subgraphs of K_6 with exactly one perfect matching: {len(U)}")
    # S_6 orbit representatives
    seen, reps = set(), []
    for S in U:
        if S in seen:
            continue
        orb = set()
        for p in perms:
            out = 0
            for a, b in EDGES:
                if S >> EIDX[(a, b)] & 1:
                    out |= 1 << EIDX[C.ekey(p[a], p[b])]
            orb.add(out)
        seen |= orb
        reps.append((S, len(orb)))
    print(f"   S_6-orbits: {len(reps)}  (orbit sizes {[o for _, o in reps]})")
    RES["stratum"] = {"unique_pm_subgraphs": len(U), "orbits": len(reps)}

    # ------------------------------------------------------------------ (1)
    banner("(1) EXHAUSTIVE enumeration of X_2 cap D6(1)")

    def compat(S1, S2):
        return (S1 & COF[S2]) == 0 and (S2 & COF[S1]) == 0

    triples = []
    weighted = 0
    for S0, orbsz in reps:
        cand = [S for S in U if compat(S0, S)]
        for S1 in cand:
            for S2 in cand:
                if compat(S1, S2):
                    triples.append((S0, S1, S2))
                    weighted += orbsz
    print(f"   ordered triples with G_0 an S_6-representative: {len(triples)}")
    print(f"   => |X_2 cap D6(1)| (ordered, all of K_6) = {weighted}")
    canons = {}
    for t in triples:
        canons.setdefault(canon(t, perms), t)
    print(f"   distinct S_6 x S_3 isomorphism classes: {len(canons)}")
    RES["X2_enumeration"] = {"rep_triples": len(triples),
                             "ordered_total": weighted,
                             "iso_classes": len(canons)}

    # independent re-verification: each survivor really is in X_2
    words2 = [w for w in product(range(3), repeat=N)
              if max(sum(1 for x in w if x == g) for g in range(3)) >= N - 2]
    bad = 0
    for t in list(canons.values()):
        src = source_of(t)
        for w in words2:
            tgt = 1 if len(set(w)) == 1 else 0
            if C.H(src, w, N) != tgt:
                bad += 1
                break
    print(f"   [re-verification] survivors failing a 2-near-constant word: "
          f"{bad}/{len(canons)}")
    # and a NEGATIVE control: triples that fail the L2 test must fail a word
    ncheck = nfail = 0
    for _ in range(400):
        t = (rng.choice(U), rng.choice(U), rng.choice(U))
        if compat(t[0], t[1]) and compat(t[0], t[2]) and compat(t[1], t[2]):
            continue
        ncheck += 1
        src = source_of(t)
        if any(C.H(src, w, N) != (1 if len(set(w)) == 1 else 0) for w in words2):
            nfail += 1
    print(f"   [negative control] L2-incompatible triples that DO fail a "
          f"2-near-constant word: {nfail}/{ncheck}")
    RES["X2_enumeration"]["reverify_bad"] = bad
    RES["X2_enumeration"]["negctrl_checked"] = ncheck
    RES["X2_enumeration"]["negctrl_failed"] = nfail

    # ------------------------------------------------------------------ (2)
    banner("(2) the top rung: EXACT cap D6(1)  (the six-site theorem)")
    exact = [t for t in canons.values() if balanced_ok(t)]
    print(f"   isomorphism classes of X_2 that ALSO satisfy every balanced "
          f"word: {len(exact)}")
    print("   (0 = an independent exhaustive re-derivation of the six-site "
          "theorem\n    on the whole all-1 diagonal stratum -- strictly larger "
          "than W22's\n    76^3 matching-triple sweep, which only allowed "
          "MATCHINGS as colour classes)")
    # confirm by the direct definition on a sample
    scheck = 0
    for t in list(canons.values())[:200]:
        src = source_of(t)
        if C.exact_defects(src, N) == []:
            scheck += 1
    print(f"   [cross-check by direct exactness test] exact sources found: "
          f"{scheck}/200 sampled classes")
    RES["exact_rung"] = {"classes_exact": len(exact), "direct_check": scheck}

    # ------------------------------------------------------------------ (3)
    banner("(3) IS ANY POINT OF X_2 cap D6(1) ALL-BLOCKED?  (exact decisions)")
    prof_rows = []
    allb = []
    for i, t in enumerate(canons.values()):
        prof = blocking_profile(t, perms)
        prof_rows.append({"triple": [t[0], t[1], t[2]],
                          "n_live": prof["n_live"],
                          "n_witness": prof["n_witness"],
                          "n_blocked": prof["n_blocked"],
                          "all_blocked": prof["all_blocked"]})
        if prof["all_blocked"]:
            allb.append(t)
        if (i + 1) % 25 == 0:
            print(f"   ... {i+1}/{len(canons)} classes decided, "
                  f"{len(allb)} all-blocked so far")
    nlive0 = sum(1 for r in prof_rows if r["n_live"] == 0)
    print(f"   classes decided: {len(prof_rows)}  (with no live pair at all: "
          f"{nlive0})")
    print(f"   >>> ALL-BLOCKED classes in X_2 cap D6(1): {len(allb)}")
    print(f"   witness counts per class: min "
          f"{min(r['n_witness'] for r in prof_rows)}, max "
          f"{max(r['n_witness'] for r in prof_rows)}")
    RES["X2_blocking"] = {"classes": len(prof_rows), "all_blocked": len(allb),
                          "no_live_pair": nlive0,
                          "min_witness": min(r["n_witness"] for r in prof_rows),
                          "rows": prof_rows[:400]}

    # ------------------------------------------------------------------ (4)
    banner("(4) one rung DOWN: does ALL-BLOCKED exist in X_0 cap D6(1)?")
    found = []
    tested = 0
    seenc = set()
    while tested < 3000 and len(found) < 12:
        t = (rng.choice(U), rng.choice(U), rng.choice(U))
        k = canon(t, perms)
        if k in seenc:
            continue
        seenc.add(k)
        tested += 1
        prof = blocking_profile(t, perms)
        if prof["all_blocked"]:
            found.append({"triple": list(t), "n_live": prof["n_live"],
                          "n_blocked": prof["n_blocked"]})
    print(f"   sampled {tested} X_0 classes (pures only, L2 NOT imposed)")
    print(f"   >>> ALL-BLOCKED classes found in X_0: {len(found)}")
    for f in found[:5]:
        print(f"      e.g. G = {f['triple']}  live={f['n_live']} "
              f"blocked={f['n_blocked']}")
    # explicit-point control: verify one of them from scratch
    if found:
        t = tuple(found[0]["triple"])
        src = source_of(t)
        pu = C.pures(src, N)
        chk = []
        for p, q in EDGES:
            if not N6.live(src, p, q):
                continue
            Uu = tuple(x for x in range(N) if x not in (p, q))
            v, d = N6.decide_pair_general(src, p, q, Uu, f"X{p}{q}")
            chk.append((p, q, v))
        print(f"   [explicit point] pures {[str(pu[c]) for c in range(3)]}; "
              f"per-pair verdicts {chk}")
        RES["X0_explicit_point"] = {"triple": list(t),
                                    "pures": [str(pu[c]) for c in range(3)],
                                    "verdicts": [[a, b, v] for a, b, v in chk]}
    RES["X0_blocking"] = {"sampled": tested, "all_blocked_found": len(found),
                          "examples": found}

    # ------------------------------------------------------------------ (5)
    banner("(5) detachment-law statistics on the exhaustive X_2 stratum")
    tally = {}
    for t in canons.values():
        prof = CACHE[canon(t, perms)]
        for r in prof["rows"]:
            if not r["live"]:
                continue
            key = (r["verdict"], r["det_p"], r["det_q"])
            tally[key] = tally.get(key, 0) + 1
    print("   (verdict, #sites of U detached from p, from q) -> count")
    for k in sorted(tally, key=lambda x: (-tally[x], str(x))):
        print(f"      {k} -> {tally[k]}")
    RES["detachment_stats_X2"] = {str(k): v for k, v in tally.items()}

    with open(f"{BASE}/results_t2b_diag6.json", "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    print("\nwrote results_t2b_diag6.json")


if __name__ == "__main__":
    main()
