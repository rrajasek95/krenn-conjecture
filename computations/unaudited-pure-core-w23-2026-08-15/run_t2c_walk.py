#!/usr/bin/env python3
"""W23 T2c -- the ladder for GENERAL (non-diagonal) N = 6 sources.

The exhaustive result of T2b lives on the all-1 DIAGONAL stratum.  This runner
tests the same ladder on general sources, by walking the varieties

    X_0 (pures) subset X_1 (pures + L1) subset X_2 (pures + L1 + L2)

exactly, using site linearity: with every block away from a site z fixed, the
condition "every k-near-constant word is exact" is THREE inhomogeneous linear
systems in the 3(N-1) star unknowns at z.  Solving them and resampling the
kernel is an exact walk that never leaves X_k.

Questions decided here:
  (a) is X_2 nonempty away from the diagonal stratum, and how big is it?
  (b) do the walked X_0 / X_1 objects contain ALL-BLOCKED points? (expected:
      yes, matching T2b)
  (c) do the walked X_2 objects? (the general-source form of the ladder)
  (d) the DETACHMENT LAW (W22, one object): witness pairs have exactly 2 sites
      of U detached from p, blocked pairs exactly 1.

All verdicts exact.
"""
from __future__ import annotations

import json
import random
import sys
import time
from fractions import Fraction
from itertools import combinations, product

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-pure-core-w23-2026-08-15")
sys.path.insert(0, BASE)
sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/"
                   "unaudited-induction2-w22-2026-08-15")
import w23_core as C                                          # noqa: E402
import w23_walk as WK                                         # noqa: E402
import w23_decide as DEC                                      # noqa: E402
import w22_n6 as N6                                           # noqa: E402

N = 6
PAIRS = list(combinations(range(N), 2))
RES = {}


def banner(t):
    print("\n" + "=" * 72)
    print(t)
    print("=" * 72)


CHEAP_CAPS = None


def cheap_caps():
    """A small exact library of caps used as a SUFFICIENT witness test."""
    global CHEAP_CAPS
    if CHEAP_CAPS is not None:
        return CHEAP_CAPS
    out = []
    # antisymmetric caps I + E_ab - E_ba  (the W23-U2 family)
    for a in range(3):
        for b in range(3):
            if a == b:
                continue
            K = [[1 if i == j else 0 for j in range(3)] for i in range(3)]
            K[a][b] = 1
            K[b][a] = -1
            out.append(K)
    # diagonal caps
    for d in product([1, -1, 2, -2], repeat=3):
        out.append([[d[i] if i == j else 0 for j in range(3)] for i in range(3)])
    # rank-one caps u (x) v with small torus entries
    small = [(1, 1, 1), (1, -1, 1), (1, 1, -1), (1, -1, -1),
             (2, 1, 1), (1, 2, 1), (1, 1, 2), (1, 1, -2)]
    for u in small:
        for v in small:
            out.append([[u[i] * v[j] for j in range(3)] for i in range(3)])
    CHEAP_CAPS = out
    return out


def cheap_witness(src, p, q, n=6):
    """SUFFICIENT test: returns a witness cap or None.  Never claims BLOCKED.
    Denominators are cleared first (verdict-invariant; see w23_decide)."""
    src = DEC.clear_denominators(src)[0]
    U = tuple(x for x in range(n) if x not in (p, q))
    # (a) detachment (W22-X2 at the source-support level)
    det = [a for a in U if all(x == 0 for r in C.oriented(src, p, a) for x in r)]
    det_q = [a for a in U if all(x == 0 for r in C.oriented(src, q, a) for x in r)]
    # (b) explicit cap library
    for K in cheap_caps():
        if not C.is_admissible(src, p, q, K):
            continue
        if not C.cap_error(src, p, q, K, U):
            return K
    return None


def profile(src, tag, decide=True, timeout=180, n=6):
    """Cheap SOUND witness test at every live pair; Singular is escalated to
    ONLY when the cheap test finds no witness anywhere (i.e. only for genuine
    all-blocked candidates).  n_witness is therefore a LOWER bound unless the
    escalation ran, which is exactly what the all-blocked question needs."""
    rows = []
    modp_mismatch = 0
    undecided = 0
    for p, q in PAIRS:
        if not DEC.live(src, p, q):
            rows.append({"pair": [p, q], "live": False})
            continue
        U = tuple(x for x in range(N) if x not in (p, q))
        det_p = sum(1 for a in U
                    if all(x == 0 for r in C.oriented(src, p, a) for x in r))
        det_q = sum(1 for a in U
                    if all(x == 0 for r in C.oriented(src, q, a) for x in r))
        row = {"pair": [p, q], "live": True, "det_p": det_p, "det_q": det_q,
               "rank_pq": C.matrix_rank(C.oriented(src, p, q))}
        row["verdict"] = ("WITNESS" if cheap_witness(src, p, q, N) is not None
                          else "?")
        row["how"] = "cheap"
        rows.append(row)
    live = [r for r in rows if r["live"]]
    nw = sum(1 for r in live if r["verdict"] == "WITNESS")
    escalated = False
    if decide and live and nw == 0:
        escalated = True
        for r in live:
            p, q = r["pair"]
            U = tuple(x for x in range(N) if x not in (p, q))
            try:
                v, d, mp = DEC.decide_pair(src, p, q, U, f"{tag}{p}{q}",
                                           timeout=timeout)
                r["verdict"] = v
                r["how"] = "singular"
                for ch, dd in mp.items():
                    if (dd == -1) != (d == -1):
                        modp_mismatch += 1
            except Exception as exc:
                r["verdict"] = "UNDECIDED"
                r["how"] = f"timeout/{type(exc).__name__}"
                undecided += 1
    return {"rows": rows, "n_live": len(live), "modp_mismatch": modp_mismatch,
            "undecided": undecided, "escalated": escalated,
            "n_witness": sum(1 for r in live if r["verdict"] == "WITNESS"),
            "n_blocked": sum(1 for r in live if r["verdict"] == "BLOCKED"),
            "all_blocked": bool(live) and
                           all(r["verdict"] == "BLOCKED" for r in live)}


def walk(src0, n, words, rng, steps, spread=3):
    """Round-robin exact site-linear walk on X_k.  Returns the final source or
    None if some site system is infeasible."""
    src = src0
    for t in range(steps):
        z = t % n
        new, dims = WK.walk_step(src, z, n, words, rng, spread=spread)
        if new is None:
            return None, f"infeasible at site {z} (step {t})"
        src = new
    ok, w = WK.in_Xk(src, n, words)
    if not ok:
        return None, f"walk left the variety at word {w}"
    return src, "ok"


def main():
    rng = random.Random(556677)
    WORDS = {k: WK.near_constant_words(N, 3, k) for k in (0, 1, 2)}
    for k in (0, 1, 2):
        print(f"   X_{k}: {len(WORDS[k])} near-constant words imposed")
    RES["word_counts"] = {str(k): len(WORDS[k]) for k in WORDS}

    # ------------------------------------------------------------------ (0)
    banner("(0) VALIDATION of the cheap sufficient witness test against the "
           "exhaustive\n    T2b ground truth (643 live pairs, all decided by "
           "Singular)")
    import run_t2b_diag6 as D6
    from itertools import permutations as _perm
    PERMS6 = list(_perm(range(6)))
    with open(f"{BASE}/results_t2b_diag6.json") as fh:
        T2B = json.load(fh)
    unsound = miss = hit = tot = 0
    for r in T2B["X2_blocking"]["rows"]:
        t = tuple(r["triple"])
        src = D6.source_of(t)
        prof = D6.blocking_profile(t, PERMS6)
        for row in prof["rows"]:
            if not row["live"]:
                continue
            p, q = row["pair"]
            tot += 1
            K = cheap_witness(src, p, q, N)
            if K is not None:
                if row["verdict"] != "WITNESS":
                    unsound += 1
                else:
                    hit += 1
            else:
                if row["verdict"] == "WITNESS":
                    miss += 1
    print(f"   {tot} live pairs with exact ground truth: cheap test claims "
          f"WITNESS {hit} times,\n   UNSOUND claims (cheap says witness, "
          f"Singular says blocked) {unsound},\n   missed witnesses (cheap "
          f"silent, Singular says witness) {miss}")
    RES["cheap_test_validation"] = {"pairs": tot, "cheap_hits": hit,
                                    "unsound": unsound, "missed": miss}

    # ------------------------------------------------------------------ (1)
    banner("(1) the walk is exact: dimensions of the site systems")
    ne = C.near_exact_six_site()
    dimrows = []
    for k in (0, 1, 2):
        for z in range(N):
            sysd = WK.site_systems(ne, z, N, WORDS[k])
            ds = []
            feas = True
            for c in range(3):
                rows, rhs, tags, cols = sysd[c]
                part, kern = WK.solve_linear(rows, rhs)
                if part is None:
                    feas = False
                    ds.append(None)
                else:
                    ds.append(len(kern))
            dimrows.append({"level": k, "site": z, "feasible": feas,
                            "kernel_dims": ds,
                            "rows": [len(sysd[c][0]) for c in range(3)]})
        print(f"   X_{k} at the near-exact source: kernel dims per site "
              f"{[d['kernel_dims'] for d in dimrows if d['level'] == k]}")
    RES["site_system_dims"] = dimrows

    # ------------------------------------------------------------------ (2)
    banner("(2) walking X_0, X_1, X_2 from the near-exact source")
    out = {}
    for k in (0, 1, 2):
        objs = []
        t0 = time.time()
        tries = 0
        while len(objs) < 6 and tries < 30:
            tries += 1
            s, msg = walk(ne, N, WORDS[k], rng, steps=6, spread=2)
            if s is None:
                continue
            # keep only genuinely new / nondegenerate objects
            objs.append(s)
        print(f"   X_{k}: built {len(objs)} walked objects in "
              f"{time.time()-t0:.1f}s ({tries} attempts)")
        rowsk = []
        allb = 0
        for i, s in enumerate(objs):
            pr = profile(s, f"W{k}{i}", decide=(k == 2), timeout=90)
            ranks = sorted(C.matrix_rank(C.oriented(s, a, b)) for a, b in PAIRS)
            pu = C.pures(s, N)
            rowsk.append({"obj": i, "n_live": pr["n_live"],
                          "n_witness": pr["n_witness"],
                          "n_blocked": pr["n_blocked"],
                          "all_blocked": pr["all_blocked"],
                          "ranks": ranks,
                          "n_fullrank": sum(1 for r in ranks if r == 3),
                          "pures": [str(pu[c]) for c in range(3)],
                          "det": [[r.get("det_p"), r.get("det_q"),
                                   r.get("verdict")]
                                  for r in pr["rows"] if r["live"]]})
            allb += int(pr["all_blocked"])
        wc = [r["n_witness"] for r in rowsk]
        if k != 2:
            print(f"   X_{k}: (cheap sufficient test only -- witness counts are "
                  f"LOWER bounds; no Singular escalation at this level)")
        print(f"   X_{k}: ALL-BLOCKED objects {allb}/{len(rowsk)}; witness "
              f"counts min {min(wc) if wc else '-'} max {max(wc) if wc else '-'}"
              f"; full-rank blocks per object "
              f"{[r['n_fullrank'] for r in rowsk]}")
        out[str(k)] = {"objects": len(rowsk), "all_blocked": allb,
                       "rows": rowsk}
    RES["walk_from_near_exact"] = out

    # ------------------------------------------------------------------ (3)
    banner("(3) projecting OTHER start points into X_k")
    starts = {}
    # (a) W22-1's constant-block mixed-exact falsifier (pures = 0)
    def const_block_mixed_exact():
        while True:
            t = {e: rng.randint(-5, 5) for e in PAIRS}
            t[(0, 1)] = 0
            b0 = C.haf_scalar(t, tuple(range(N)))
            t[(0, 1)] = 1
            c0 = C.haf_scalar(t, tuple(range(N))) - b0
            if c0 == 0:
                continue
            v = Fraction(-b0, c0)
            d = v.denominator
            tt = {e: (int(v * d) if e == (0, 1) else int(val * d))
                  for e, val in t.items()}
            if any(x == 0 for x in tt.values()):
                continue
            if C.haf_scalar(tt, tuple(range(N))) != 0:
                continue
            return {e: [[tt[e]] * 3 for _ in range(3)] for e in PAIRS}

    starts["W22-1 falsifier"] = const_block_mixed_exact()
    starts["random dense"] = C.random_source(rng, N)
    s = C.zero_source(N)
    for e in s:
        for i in range(3):
            for j in range(3):
                if rng.random() < 0.4:
                    s[e][i][j] = rng.randint(-3, 3)
    starts["random sparse"] = s

    proj = {}
    for name, s0 in starts.items():
        row = {}
        for k in (0, 1, 2):
            got, msg = walk(s0, N, WORDS[k], rng, steps=6, spread=2)
            row[str(k)] = {"reachable": got is not None, "msg": msg}
            if got is not None:
                pr = profile(got, f"P{k}", decide=(k == 2), timeout=90)
                ranks = sorted(C.matrix_rank(C.oriented(got, a, b))
                               for a, b in PAIRS)
                row[str(k)].update({"n_live": pr["n_live"],
                                    "n_witness": pr["n_witness"],
                                    "all_blocked": pr["all_blocked"],
                                    "n_fullrank": sum(1 for r in ranks if r == 3),
                                    "pures": [str(x) for x in
                                              C.pures(got, N).values()]})
        proj[name] = row
        print(f"   {name}:")
        for k in (0, 1, 2):
            r = row[str(k)]
            if r["reachable"]:
                print(f"      X_{k}: reached; live {r['n_live']} witness "
                      f"{r['n_witness']} ALL_BLOCKED {r['all_blocked']} "
                      f"full-rank blocks {r['n_fullrank']}")
            else:
                print(f"      X_{k}: NOT reachable from this start ({r['msg']})")
    RES["projections"] = proj

    # ------------------------------------------------------------------ (4)
    banner("(4) targeted hunt for an ALL-BLOCKED point of X_2 (general blocks)")
    best = None
    trials = 0
    t0 = time.time()
    hits = 0
    while trials < 20 and time.time() - t0 < 1200:
        trials += 1
        base = rng.choice([ne, starts["random dense"], starts["random sparse"]])
        s, msg = walk(base, N, WORDS[2], rng, steps=rng.randint(3, 10),
                      spread=rng.choice([1, 2, 4]))
        if s is None:
            continue
        pr = profile(s, f"H{trials}", decide=True, timeout=90)
        if pr["n_live"] == 0:
            continue
        frac = pr["n_blocked"] / pr["n_live"]
        if best is None or frac > best[0]:
            best = (frac, pr["n_blocked"], pr["n_live"],
                    sorted(C.matrix_rank(C.oriented(s, a, b)) for a, b in PAIRS))
        hits += int(pr["all_blocked"])
    print(f"   {trials} walked X_2 objects; ALL-BLOCKED found: {hits}")
    if best:
        print(f"   best blocked fraction {best[1]}/{best[2]} = {best[0]:.3f}; "
              f"block ranks {best[3]}")
    RES["x2_hunt"] = {"trials": trials, "all_blocked": hits,
                      "best_blocked_fraction": None if not best else
                      [best[1], best[2]], "best_ranks": None if not best
                      else best[3]}

    # ------------------------------------------------------------------ (5)
    banner("(5) DETACHMENT LAW (T3): aggregate over every object built here")
    tally = {}
    for k, blk in RES["walk_from_near_exact"].items():
        for r in blk["rows"]:
            for dp, dq, v in r["det"]:
                tally[(v, dp, dq)] = tally.get((v, dp, dq), 0) + 1
    print("   (verdict, det_p, det_q) -> count   [general-source walks]")
    for key in sorted(tally, key=lambda x: (-tally[x], str(x))):
        print(f"      {key} -> {tally[key]}")
    RES["detachment_walk"] = {str(k): v for k, v in tally.items()}

    with open(f"{BASE}/results_t2c_walk.json", "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    print("\nwrote results_t2c_walk.json")


if __name__ == "__main__":
    main()
