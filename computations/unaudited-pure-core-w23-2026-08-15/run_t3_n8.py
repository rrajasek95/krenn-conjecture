#!/usr/bin/env python3
"""W23 T3-extension -- the ladder at N = 8 (the first inductive boundary).

STRUCTURE THEOREM (all-1 diagonal stratum, every even N) [PROVED-HERE].
Let A be an all-1 diagonal source in X_2 with colour graphs G_c.
  * pures  <=>  each G_c has EXACTLY ONE perfect matching M_c;
  * L_c := {e : w_c(e) C^(c)_e != 0} = M_c EXACTLY.  [If e in G_c and G_c - e
    has a PM M', then M' + e is a PM of G_c, so M' + e = M_c and e in M_c.]
  * L2  <=>  E(G_d) cap cof(G_c) = {} for every d != c.  Since M_c subset
    cof(G_c), the M_c are pairwise DISJOINT and G_d avoids M_c, so

        G_c = M_c u S_c,      S_c subset F := E(K_N) \\ (M_0 u M_1 u M_2),

    and every edge of S_c is DEAD: all three of its colour cofactors vanish.

At N = 8, |F| = 16.  This gives a complete generator of X_2 cap D8(1):
1,884 ordered bases with M_0 fixed to the standard matching (exhaustive up to
S_8), and per base 10^5-10^6 valid (S_0,S_1,S_2) triples -- of order 10^9
points in all, far beyond exact per-object decision.  So this runner:

  (a) verifies the generator against the raw word definition;
  (b) samples the family broadly and applies the SOUND cheap witness test
      (an explicit admissible cap K with E_pq(K) = 0 IS a witness -- validated
      against the exhaustive N = 6 ground truth at 510 hits / 0 unsound);
  (c) falls back to the exact Singular decision (h = 3 cubics) for any live
      pair the cheap test cannot settle;
  (d) verifies THEOREM W23-DR at N = 8 on every sampled point.
"""
from __future__ import annotations

import json
import random
import sys
import time
from itertools import combinations, product

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-pure-core-w23-2026-08-15")
sys.path.insert(0, BASE)
import w23_core as C                                          # noqa: E402
import w23_walk as WK                                         # noqa: E402
import w23_decide as DEC                                      # noqa: E402

N = 8
E8 = list(combinations(range(N), 2))
IDX = {e: i for i, e in enumerate(E8)}
RES = {}


def banner(t):
    print("\n" + "=" * 72)
    print(t, flush=True)
    print("=" * 72, flush=True)


PM8 = [sum(1 << IDX[C.ekey(*e)] for e in M)
       for M in C.perfect_matchings(tuple(range(N)))]
PM6 = {T: [sum(1 << IDX[C.ekey(*e)] for e in M)
           for M in C.perfect_matchings(T)]
       for T in combinations(range(N), 6)}


def cofmask(G):
    m = 0
    for i, (a, b) in enumerate(E8):
        T = tuple(x for x in range(N) if x not in (a, b))
        if any(pm & ~G == 0 for pm in PM6[T]):
            m |= 1 << i
    return m


def source_of(masks):
    src = C.zero_source(N)
    for c, G in enumerate(masks):
        for i, e in enumerate(E8):
            if G >> i & 1:
                src[e][c][c] = 1
    return src


CAPS = None


def caps():
    global CAPS
    if CAPS is None:
        out = []
        for a in range(3):
            for b in range(3):
                if a == b:
                    continue
                K = [[1 if i == j else 0 for j in range(3)] for i in range(3)]
                K[a][b] = 1
                K[b][a] = -1
                out.append(K)
        for d in product([1, -1, 2], repeat=3):
            out.append([[d[i] if i == j else 0 for j in range(3)]
                        for i in range(3)])
        CAPS = out
    return CAPS


def cheap_witness(src, p, q):
    U = tuple(x for x in range(N) if x not in (p, q))
    for K in caps():
        if not C.is_admissible(src, p, q, K):
            continue
        if not C.cap_error(src, p, q, K, U):
            return K
    return None


def main():
    rng = random.Random(80808)
    M0 = sum(1 << IDX[e] for e in [(0, 1), (2, 3), (4, 5), (6, 7)])
    d0 = [m for m in PM8 if not (m & M0)]
    bases = [(M0, m1, m2) for m1 in d0 for m2 in d0 if not (m1 & m2)]
    print(f"   perfect matchings of K_8: {len(PM8)}; disjoint from the "
          f"standard one: {len(d0)}")
    print(f"   ordered bases (M_0 fixed; exhaustive up to S_8): {len(bases)}")
    RES["bases"] = len(bases)

    def valid_S(b, c):
        F = ((1 << 28) - 1) & ~(b[0] | b[1] | b[2])
        Mc = b[c]
        oth = b[(c + 1) % 3] | b[(c + 2) % 3]
        forb = [(m & F) for m in PM8 if m != Mc and (m & ~(Mc | F)) == 0]
        out = []
        sub = F
        while True:
            if all((f & ~sub) != 0 for f in forb):
                R = cofmask(Mc | sub)
                if not (R & oth):
                    out.append((sub, R & F))
            if sub == 0:
                break
            sub = (sub - 1) & F
        return out

    # ---------------- (a) generator size + verification --------------------
    banner("(a) the X_2 generator at N = 8, verified against the raw words")
    words2 = WK.near_constant_words(N, 3, 2)
    print(f"   2-near-constant words at N=8: {len(words2)}", flush=True)
    sizes = []
    for bi in rng.sample(range(len(bases)), 8):
        b = bases[bi]
        V = [valid_S(b, c) for c in range(3)]
        sizes.append([len(v) for v in V])
    print(f"   |valid S_c| on 8 random bases: {sizes}", flush=True)
    RES["valid_S_sizes"] = sizes

    # sample points and verify membership exactly
    pts = []
    t0 = time.time()
    while len(pts) < 60 and time.time() - t0 < 600:
        b = bases[rng.randrange(len(bases))]
        V = [valid_S(b, c) for c in range(3)]
        for _ in range(40):
            S0, R0 = V[0][rng.randrange(len(V[0]))]
            S1, R1 = V[1][rng.randrange(len(V[1]))]
            S2, R2 = V[2][rng.randrange(len(V[2]))]
            if (S1 & R0) or (S0 & R1) or (S2 & R0) or (S2 & R1) \
               or (S0 & R2) or (S1 & R2):
                continue
            pts.append((b[0] | S0, b[1] | S1, b[2] | S2))
            break
    bad = 0
    extra = []
    for g in pts:
        src = source_of(g)
        ok, w = WK.in_Xk(src, N, words2)
        if not ok:
            bad += 1
        extra.append(sum(bin(g[c]).count("1") for c in range(3)) - 12)
    print(f"   sampled {len(pts)} X_2 points; failing a 2-near-constant word: "
          f"{bad}; extra (dead) edges per point: min {min(extra)} max "
          f"{max(extra)}", flush=True)
    RES["sampled_points"] = {"n": len(pts), "membership_failures": bad,
                             "extra_edges_min": min(extra),
                             "extra_edges_max": max(extra)}

    # negative control: break L2 on purpose
    nc = ncf = 0
    for _ in range(60):
        b = bases[rng.randrange(len(bases))]
        F = ((1 << 28) - 1) & ~(b[0] | b[1] | b[2])
        g = list(b)
        c = rng.randrange(3)
        # add an edge that IS in another colour's cofactor support
        R = cofmask(b[(c + 1) % 3])
        cand = [i for i in range(28) if (R >> i & 1) and not (g[c] >> i & 1)]
        if not cand:
            continue
        g[c] |= 1 << rng.choice(cand)
        nc += 1
        if not WK.in_Xk(source_of(tuple(g)), N, words2)[0]:
            ncf += 1
    print(f"   [negative control] adding an edge inside another colour's "
          f"cofactor support breaks X_2: {ncf}/{nc}", flush=True)
    RES["neg_control"] = {"checked": nc, "fired": ncf}

    # ---------------- (b) THEOREM W23-DR at N = 8 --------------------------
    banner("(b) THEOREM W23-DR verified on every sampled N = 8 point")
    drbad = 0
    for g in pts:
        src = source_of(g)
        Ls = []
        for c in range(3):
            w = C.colour_slice(src, c, N)
            Ls.append(set(e for e in E8
                          if w[e] != 0 and C.cofactor(w, N, e) != 0))
        okc = all(len(set(x for e in L for x in e)) == N for L in Ls)
        okd = all(not (Ls[i] & Ls[j]) for i, j in combinations(range(3), 2))
        okr = all(C.matrix_rank(C.oriented(src, *e)) == 1 for L in Ls for e in L)
        oksz = all(len(L) == N // 2 for L in Ls)
        if not (okc and okd and okr and oksz):
            drbad += 1
    print(f"   {len(pts)} points: L_c covers B, pairwise disjoint, rank-one, "
          f"|L_c| = N/2 -- violations {drbad}", flush=True)
    RES["DR_n8"] = {"points": len(pts), "violations": drbad}

    # ---------------- (c) witnesses ---------------------------------------
    banner("(c) does every sampled N = 8 X_2 point carry a witness?")
    rows = []
    t0 = time.time()
    for k, g in enumerate(pts):
        src = source_of(g)
        nlive = ncheap = nsing_w = nsing_b = nund = 0
        for p, q in E8:
            if not DEC.live(src, p, q):
                continue
            nlive += 1
            K = cheap_witness(src, p, q)
            if K is not None:
                ncheap += 1
                continue
            U = tuple(x for x in range(N) if x not in (p, q))
            try:
                v, d, mp = DEC.decide_pair(src, p, q, U, f"E{k}{p}{q}",
                                           timeout=240)
                nsing_w += int(v == "WITNESS")
                nsing_b += int(v == "BLOCKED")
            except Exception:
                nund += 1
        rows.append({"point": k, "live": nlive, "cheap_witness": ncheap,
                     "singular_witness": nsing_w, "singular_blocked": nsing_b,
                     "undecided": nund,
                     "all_blocked": nlive > 0 and (ncheap + nsing_w) == 0})
        if (k + 1) % 10 == 0:
            print(f"   ... {k+1}/{len(pts)} points, "
                  f"{sum(1 for r in rows if r['all_blocked'])} all-blocked so "
                  f"far ({time.time()-t0:.0f}s)", flush=True)
        if time.time() - t0 > 2400:
            print("   [time budget reached]", flush=True)
            break
    nb = sum(1 for r in rows if r["all_blocked"])
    wmin = min((r["cheap_witness"] + r["singular_witness"]) for r in rows)
    print(f"   {len(rows)} N=8 X_2 points decided; ALL-BLOCKED: {nb}")
    print(f"   witness pairs per point: min {wmin}, "
          f"live pairs per point {sorted(set(r['live'] for r in rows))}")
    print(f"   pairs needing Singular: "
          f"{sum(r['singular_witness'] + r['singular_blocked'] for r in rows)}; "
          f"undecided {sum(r['undecided'] for r in rows)}")
    RES["n8_witnesses"] = {"points": len(rows), "all_blocked": nb,
                           "min_witnesses": wmin, "rows": rows}

    with open(f"{BASE}/results_t3_n8.json", "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    print("\nwrote results_t3_n8.json")


if __name__ == "__main__":
    main()
