#!/usr/bin/env python3
"""W27 T1d -- THE BACKGROUND SEARCH FOR AN X_4 POINT AT N = 8.

By W27-R1 the whole question is: is there a source B on the seven sites
V - {z} for which all three colour systems at z are consistent?  The blocks AT
z are then free (they are the unknowns), so the search space is exactly a
source on K_7 -- 21 blocks, 189 coordinates.

Three searches:
  S1  EXHAUSTIVE-ish over DIAGONAL K_7 backgrounds (three disjoint edge sets of
      K_7 with generic weights) -- a family strictly larger than the
      restrictions of Delta^3_8, because 7 is odd and no perfect-matching
      condition constrains it;
  S2  LOCAL SEARCH from the best backgrounds found (score = 10 * #feasible
      colour systems + sum of the mixed-kernel dimensions), perturbing the
      background block by block;
  S3  structured degenerate backgrounds (rank-1 blocks, sparse supports,
      two-block splits).

Every 3-of-3 hit is solved exactly and checked against the raw word test.
"""
from __future__ import annotations

import json
import random
import sys
import time
from fractions import Fraction
from itertools import combinations

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-penult-w27-2026-08-18")
W25BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
           "unaudited-x3core-w25-2026-08-15")
sys.path.insert(0, BASE)
sys.path.insert(0, W25BASE)
import w27_core as W                                              # noqa: E402
import w27_x4 as X                                                # noqa: E402
import w25_walk as WK                                             # noqa: E402
C = W.C

N = 8
Z = 7                                    # the free site (WLOG by relabelling)
REST = tuple(range(7))
E7 = list(combinations(REST, 2))
RES = {}
RAN = []
HITS = []
OUT = f"{BASE}/results_t1d_bgsearch.json"
WORDS4 = None


def control(name):
    if name not in RAN:
        RAN.append(name)


def ck(tag=""):
    RES["ran"] = RAN
    RES["hits"] = HITS
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    if tag:
        print(f"      [checkpoint {tag}]", flush=True)


def score(src, z=Z):
    """(#feasible colour systems, [kernel dims], [feasible flags])."""
    try:
        sm = X.src_mod(src, X.P1)
    except ValueError:
        return None
    tabs = X.cof_tables(sm, X.P1, sites=[z])
    fl, kd, rk = [], [], []
    for c in range(3):
        rows, rhs, tags, cols = X.build_rows(tabs, WORDS4, z, c)
        ok, rmix, rall = X.feasible_mod(rows, rhs, len(cols), X.P1)
        fl.append(ok)
        kd.append(len(cols) - rmix)
        rk.append(rmix)
    return {"n_feasible": sum(fl), "feasible": fl, "mixed_kernel": kd,
            "rank_mixed": rk,
            "score": 100 * sum(fl) + sum(kd)}


def diag_k7(rng, sizes=None):
    """A diagonal K_7 background: three disjoint edge sets with weights."""
    pool = list(E7)
    rng.shuffle(pool)
    if sizes is None:
        sizes = [rng.randint(2, 6) for _ in range(3)]
    src = C.zero_source(N)
    i = 0
    Ls = []
    for c in range(3):
        L = pool[i:i + sizes[c]]
        i += sizes[c]
        Ls.append(sorted(L))
        for e in L:
            src[e][c][c] = Fraction(rng.choice([1, -1, 2, -2, 3, 5]))
    return src, Ls


def verify(src, z, tag, note):
    print(f"      >>> HIT {tag} at site {z} -- exact solve", flush=True)
    cur, dims = WK.site_solve(src, z, N, 4, keep_particular=True,
                              words=tuple(WORDS4))
    rec = {"tag": tag, "note": note, "site": z, "exact_feasible": cur is not None}
    if cur is None:
        print("      ... exact says INFEASIBLE (mod-p false positive)",
              flush=True)
        return rec
    ok4, bad = C.in_Xk(cur, N, 4)
    rec.update({"kernel_dims": dims, "in_X4_raw": ok4,
                "in_X3_raw": C.in_Xk(cur, N, 3)[0],
                "first_failure": list(bad) if bad else None,
                "pures": [str(x) for x in C.pures(cur, N).values()],
                "n_mixed_defects": len(C.mixed_defects(cur, N)),
                "blocks": {f"{a},{b}": [[str(x) for x in row]
                                        for row in cur[(a, b)]]
                           for a, b in combinations(range(N), 2)}})
    print(f"      ... EXACT in_X4 {ok4}; kernels {dims}; defects "
          f"{rec['n_mixed_defects']}", flush=True)
    return rec


def perturb_bg(src, rng, k=1, vals=(-2, -1, 1, 2)):
    out = C.copy_source(src)
    for _ in range(k):
        e = E7[rng.randrange(len(E7))]
        i, j = rng.randrange(3), rng.randrange(3)
        if rng.random() < 0.35:
            out[e][i][j] = Fraction(0)
        else:
            out[e][i][j] = out[e][i][j] + Fraction(rng.choice(vals))
    return out


def main():
    global WORDS4
    t0 = time.time()
    rng = random.Random(9091)
    WORDS4 = list(C.near_constant_words(N, 3, 4))

    print("=" * 74)
    print("(S1) DIAGONAL K_7 BACKGROUNDS")
    print("=" * 74)
    best = None
    hist = {}
    rows = []
    for t in range(700):
        src, Ls = diag_k7(rng)
        s = score(src)
        if s is None:
            continue
        hist[s["n_feasible"]] = hist.get(s["n_feasible"], 0) + 1
        rows.append({"sizes": [len(L) for L in Ls], **{k: v for k, v in s.items()
                                                       if k != "feasible"},
                     "feasible": s["feasible"]})
        if best is None or s["score"] > best[0]["score"]:
            best = (s, src, {"family": "diag_k7",
                             "classes": [[list(e) for e in L] for L in Ls]})
            print(f"   t={t}: new best score {s['score']} "
                  f"(feasible {s['feasible']}, kernels {s['mixed_kernel']})",
                  flush=True)
        if s["n_feasible"] == 3:
            HITS.append(verify(src, Z, f"S1_{t}", {"classes": [[list(e)
                                                                for e in L]
                                                               for L in Ls]}))
            ck(f"S1hit_{t}")
        if t % 100 == 99:
            RES["S1"] = {"histogram": hist, "n": len(rows),
                         "best": best[0] if best else None,
                         "best_note": best[2] if best else None}
            ck(f"S1_{t}")
    print(f"   {len(rows)} diagonal K_7 backgrounds; histogram of "
          f"#feasible colour systems at site 7: {hist}")
    RES["S1"] = {"histogram": hist, "n": len(rows),
                 "best": best[0] if best else None,
                 "best_note": best[2] if best else None,
                 "sample": rows[:40]}
    control("T1d_S1_diag_k7")
    ck("S1")

    print("=" * 74)
    print("(S2) LOCAL SEARCH from the best backgrounds")
    print("=" * 74)
    starts = []
    for _ in range(14):
        src, Ls = diag_k7(rng)
        s = score(src)
        if s:
            starts.append((s["score"], src))
    starts.sort(key=lambda x: -x[0])
    if best is not None:
        starts.insert(0, (best[0]["score"], best[1]))
    runs = []
    for si, (sc0, src0) in enumerate(starts[:6]):
        cur = src0
        cs = score(cur)
        traj = [cs["score"]]
        for step in range(260):
            cand = perturb_bg(cur, rng, k=rng.choice([1, 1, 2]))
            s2 = score(cand)
            if s2 is None:
                continue
            if s2["score"] >= cs["score"]:
                cur, cs = cand, s2
            if cs["n_feasible"] == 3:
                HITS.append(verify(cur, Z, f"S2_{si}_{step}",
                                   {"from": "local search"}))
                ck(f"S2hit_{si}_{step}")
                break
            traj.append(cs["score"])
        runs.append({"start": sc0, "end": cs["score"],
                     "feasible": cs["feasible"],
                     "kernels": cs["mixed_kernel"],
                     "n_feasible": cs["n_feasible"]})
        print(f"   run {si}: score {sc0} -> {cs['score']}; feasible "
              f"{cs['feasible']}; kernels {cs['mixed_kernel']}", flush=True)
        RES["S2"] = runs
        ck(f"S2_{si}")
    control("T1d_S2_local_search")

    print("=" * 74)
    print("(S3) STRUCTURED DEGENERATE BACKGROUNDS")
    print("=" * 74)
    fams = {}

    def famrun(name, mk, k=60):
        h = {}
        bst = 0
        for t in range(k):
            src = mk()
            s = score(src)
            if s is None:
                continue
            h[s["n_feasible"]] = h.get(s["n_feasible"], 0) + 1
            bst = max(bst, s["n_feasible"])
            if s["n_feasible"] == 3:
                HITS.append(verify(src, Z, f"S3_{name}_{t}", {"family": name}))
                ck(f"S3hit_{name}_{t}")
        fams[name] = {"histogram": h, "best": bst}
        print(f"   {name:26s}: histogram {h}", flush=True)

    def rank1_blocks():
        src = C.zero_source(N)
        for e in E7:
            if rng.random() < 0.6:
                u = [Fraction(rng.choice([0, 1, -1, 2])) for _ in range(3)]
                v = [Fraction(rng.choice([0, 1, -1, 2])) for _ in range(3)]
                src[e] = [[u[i] * v[j] for j in range(3)] for i in range(3)]
        return src

    def sparse_general():
        src = C.zero_source(N)
        for e in E7:
            for i in range(3):
                for j in range(3):
                    if rng.random() < 0.12:
                        src[e][i][j] = Fraction(rng.choice([1, -1, 2, -2]))
        return src

    def two_block():
        """K_7 split 4 + 3, only inside-group blocks live."""
        src = C.zero_source(N)
        A = set(rng.sample(REST, 4))
        for e in E7:
            if (e[0] in A) == (e[1] in A):
                for i in range(3):
                    src[e][i][i] = Fraction(rng.choice([1, -1, 2]))
        return src

    def diag_plus_one_offdiag():
        src, Ls = diag_k7(rng)
        for _ in range(rng.randint(1, 3)):
            e = E7[rng.randrange(len(E7))]
            i, j = rng.randrange(3), rng.randrange(3)
            if i != j:
                src[e][i][j] = Fraction(rng.choice([1, -1]))
        return src

    def diag_k7_small():
        return diag_k7(rng, sizes=[rng.randint(1, 3) for _ in range(3)])[0]

    def diag_k7_big():
        return diag_k7(rng, sizes=[rng.randint(5, 7) for _ in range(3)])[0]

    famrun("rank1_blocks", rank1_blocks)
    famrun("sparse_general", sparse_general)
    famrun("two_block_4_3", two_block)
    famrun("diag_plus_offdiag", diag_plus_one_offdiag)
    famrun("diag_k7_small", diag_k7_small, 150)
    famrun("diag_k7_big", diag_k7_big, 150)
    RES["S3"] = fams
    control("T1d_S3_structured")
    ck("S3")

    RES["n_hits"] = len(HITS)
    print(f"TOTAL 3-of-3 HITS: {len(HITS)}")
    declared = ["T1d_S1_diag_k7", "T1d_S2_local_search", "T1d_S3_structured"]
    missing = [x for x in declared if x not in RAN]
    RES["manifest"] = {"declared": declared, "ran": RAN, "missing": missing}
    RES["seconds"] = round(time.time() - t0, 1)
    print(f"CONTROL MANIFEST: declared {len(declared)}, ran {len(RAN)}, "
          f"missing {missing}")
    assert not missing
    ck("final")
    print(f"wrote {OUT} ({RES['seconds']}s)")


if __name__ == "__main__":
    main()
