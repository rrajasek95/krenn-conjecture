#!/usr/bin/env python3
"""W25 T1b -- THE ADVERSARIAL BUILDER (ledger 20): try to BUILD an ALL-BLOCKED
point of X_3 at N = 6.

W23 walked X_3 from ONE seed (the committed near-exact source) and reported
that the walk sees a single component (kernel dims (0,0,0) at three sites).
This runner attacks the same question with a genuinely diverse seed set, made
possible by W25-D1 (diagonal X_2 = diagonal X_3): EVERY point of EVERY one of
the 24 exhaustively enumerated diagonal skeleton classes is an X_3 point, and
the X_3 site systems there have POSITIVE kernel dimension, so the walk leaves
the diagonal stratum.

Seeds
  S1  the committed near-exact source (W23's seed -- reproduction control);
  S2  the four all-blocked X_2 objects of W23, pushed into X_3 by the unique
      site-2 solve (this is the sharpest possible starting point: it is the
      nearest X_3 point to a known all-blocked X_2 point);
  S3  the 24 diagonal classes, several exact weight points each;
  S4  Q(omega) points of the same classes (omega is structural, ledger 19/20).

Each walked object is re-verified in X_3 against the RAW 639-word definition,
then screened: live pairs are decided in Singular until a WITNESS appears; an
object with no witness at any live pair gets the FULL battery (both deciders,
three primes) and is reported as an ESCALATION.
"""
from __future__ import annotations

import json
import random
import sys
import time
from collections import Counter
from fractions import Fraction
from itertools import combinations

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-x3core-w25-2026-08-15")
W23BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
           "unaudited-pure-core-w23-2026-08-15")
sys.path.insert(0, BASE)
sys.path.insert(0, W23BASE)
import w25_core as C                                            # noqa: E402
import w25_walk as WK                                           # noqa: E402
import w25_decide as D                                          # noqa: E402
import w23_decide as W23D                                       # noqa: E402
import run_t1d_diagonal as T1D                                  # noqa: E402
import run_t1e_diagonal_uniform as T1E                          # noqa: E402

N = 6
RES = {}
RAN = []
ESCALATIONS = []


def control(name):
    RAN.append(name)


def profile(src):
    ranks = sorted(C.matrix_rank(C.oriented(src, a, b))
                   for a, b in combinations(range(N), 2))
    md = C.mixed_defects(src, N)
    shapes = Counter(tuple(sorted(Counter(w).values())) for w in md)
    diag = all(len([(i, j) for i in range(3) for j in range(3)
                    if src[e][i][j] != 0]) <= 1 for e in src)
    return {"ranks": ranks, "n_defects": len(md),
            "defect_shapes": {str(k): v for k, v in shapes.items()},
            "diagonal": diag,
            "n_live": sum(1 for a, b in combinations(range(N), 2)
                          if C.live(src, a, b))}


def screen(src, tag):
    """Decide live pairs until a WITNESS appears.  Returns (verdict_summary)."""
    live = [(p, q) for p, q in combinations(range(N), 2) if C.live(src, p, q)]
    order = sorted(live, key=lambda pq: -C.matrix_rank(C.oriented(src, *pq)))
    decided = []
    for (p, q) in order:
        U = tuple(x for x in range(N) if x not in (p, q))
        v, d, _ = D.decide_pair(src, p, q, U, f"{tag}_{p}{q}", primes=())
        decided.append(((p, q), v))
        if v == "WITNESS":
            return {"n_live": len(live), "witness_found": [p, q],
                    "decided": len(decided), "all_blocked": False}
    return {"n_live": len(live), "witness_found": None,
            "decided": len(decided), "all_blocked": bool(live),
            "verdicts": [[list(pq), v] for pq, v in decided]}


def full_battery(src, tag):
    rows = []
    for p, q in combinations(range(N), 2):
        lv = C.live(src, p, q)
        row = {"pair": [p, q], "live": lv,
               "rank": C.matrix_rank(C.oriented(src, p, q))}
        if lv:
            U = tuple(x for x in range(N) if x not in (p, q))
            v1, d1, mp = D.decide_pair(src, p, q, U, f"{tag}A{p}{q}")
            isrc, _ = C.clear_denominators(src)
            v2, d2, _ = W23D.decide_pair(isrc, p, q, U, f"{tag}B{p}{q}",
                                         primes=(32003, 1000003))
            row.update({"w25": v1, "dimQ": d1, "modp": mp, "w23": v2,
                        "agree": v1 == v2})
        rows.append(row)
    lv = [r for r in rows if r["live"]]
    return {"in_X3_raw": C.in_Xk(src, N, 3)[0],
            "pures": [str(x) for x in C.pures(src, N).values()],
            "n_live": len(lv),
            "n_witness": sum(1 for r in lv if r["w25"] == "WITNESS"),
            "all_blocked": bool(lv) and all(r["w25"] == "BLOCKED" for r in lv),
            "disagreements": sum(1 for r in lv if not r["agree"]),
            "modp_mismatch": sum(1 for r in lv for ch, dd in r["modp"].items()
                                 if (dd == -1) != (r["dimQ"] == -1)),
            "rows": rows}


def record(src, tag, stats, seedname):
    ok, badw = C.in_Xk(src, N, 3)
    assert ok, (tag, "walk left X_3", badw)
    pr = profile(src)
    if pr["n_live"] == 0:
        stats.append({"tag": tag, "seed": seedname, "skip": "no live pair"})
        return
    sc = screen(src, tag)
    rec = {"tag": tag, "seed": seedname, **pr, **sc}
    stats.append(rec)
    if sc["all_blocked"]:
        bat = full_battery(src, tag + "F")
        blocks = {f"{a},{b}": [[str(x) for x in row] for row in src[(a, b)]]
                  for a, b in combinations(range(N), 2)}
        ESCALATIONS.append({"tag": tag, "seed": seedname, "profile": pr,
                            "battery": {k: v for k, v in bat.items()
                                        if k != "rows"},
                            "rows": bat["rows"], "blocks": blocks})
        print(f"\n   *** ESCALATION: ALL-BLOCKED X_3 CANDIDATE {tag} "
              f"(seed {seedname}) -- full battery: {bat['all_blocked']}, "
              f"disagreements {bat['disagreements']}, mod-p "
              f"{bat['modp_mismatch']}\n", flush=True)


def main():
    t0 = time.time()
    rng = random.Random(31415926)
    stats = []

    print("=" * 74)
    print("SEED S1: the committed near-exact source (W23's seed)")
    print("=" * 74)
    ne = C.near_exact_six_site()
    record(ne, "S1base", stats, "near_exact")
    for k in range(12):
        src = ne
        ok = True
        for t in range(rng.randint(2, 8)):
            nxt, dims = WK.site_solve(src, rng.randrange(N), N, 3, rng,
                                      spread=rng.choice([1, 2, 3, 5]))
            if nxt is None:
                ok = False
                break
            src = nxt
        if ok:
            record(src, f"S1w{k}", stats, "near_exact")
    print(f"   objects so far: {len(stats)}; all-blocked "
          f"{sum(1 for s in stats if s.get('all_blocked'))}")
    control("S1_near_exact_walk")

    print("=" * 74)
    print("SEED S2: W23's four ALL-BLOCKED X_2 objects, pushed into X_3")
    print("=" * 74)
    for i, ab in enumerate(C.w23_allblocked_x2()):
        pushed, dims = WK.site_solve(ab, 2, N, 3, keep_particular=True)
        assert pushed is not None
        record(pushed, f"S2p{i}", stats, "allblocked_x2_pushed")
        for k in range(6):
            src = pushed
            ok = True
            for t in range(rng.randint(1, 6)):
                nxt, dd = WK.site_solve(src, rng.randrange(N), N, 3, rng,
                                        spread=rng.choice([1, 2, 3]))
                if nxt is None:
                    ok = False
                    break
                src = nxt
            if ok:
                record(src, f"S2w{i}_{k}", stats, "allblocked_x2_pushed")
    print(f"   objects so far: {len(stats)}; all-blocked "
          f"{sum(1 for s in stats if s.get('all_blocked'))}")
    control("S2_allblocked_x2_pushed")

    print("=" * 74)
    print("SEED S3: the 24 diagonal classes, walked off the diagonal in X_3")
    print("=" * 74)
    classes = sorted(set(T1D.canonical(Ls) for Ls in T1E._survivors()))
    for i, cn in enumerate(classes):
        pts = T1E.sample_points(cn, rng, k=3)
        for j, w in enumerate(pts):
            base = T1D.build_source(cn, w)
            record(base, f"S3b{i}_{j}", stats, f"diag{i}")
            for k in range(3):
                src = base
                ok = True
                for t in range(rng.randint(1, 6)):
                    nxt, dd = WK.site_solve(src, rng.randrange(N), N, 3, rng,
                                            spread=rng.choice([1, 2, 3, 4]))
                    if nxt is None:
                        ok = False
                        break
                    src = nxt
                if ok:
                    record(src, f"S3w{i}_{j}_{k}", stats, f"diag{i}")
        print(f"   class {i}: cumulative objects {len(stats)}; all-blocked "
              f"{sum(1 for s in stats if s.get('all_blocked'))}", flush=True)
    control("S3_diagonal_walk")

    print("=" * 74)
    print("SEED S4: Q(omega) walks (ledger 19/20 -- omega is structural)")
    print("=" * 74)
    for i, cn in enumerate(classes):
        pts = T1E.sample_points(cn, rng, k=1)
        for j, w in enumerate(pts):
            wo = {e: C.Om(v, 0) for e, v in w.items()}
            base = T1D.build_source(cn, wo)
            for k in range(2):
                src = base
                ok = True
                for t in range(rng.randint(1, 5)):
                    z = rng.randrange(N)
                    sysd = WK.site_systems(src, z, N, 3)
                    sol, dims, good = {}, [], True
                    for c in range(3):
                        rows, rhs, tags, cols = sysd[c]
                        part, kern = C.solve_linear(rows, rhs, len(cols))
                        if part is None:
                            good = False
                            break
                        vec = list(part)
                        for kv in kern:
                            lam = C.Om(rng.randint(-2, 2), rng.randint(-2, 2))
                            if lam != 0:
                                vec = [a + lam * b for a, b in zip(vec, kv)]
                        sol[c] = vec
                    if not good:
                        ok = False
                        break
                    src = WK.apply_site_solution(src, z, sol, sysd[0][3], N)
                if ok:
                    record(src, f"S4w{i}_{k}", stats, f"omega_diag{i}")
        if i % 6 == 0:
            print(f"   omega class {i}: cumulative objects {len(stats)}; "
                  f"all-blocked {sum(1 for s in stats if s.get('all_blocked'))}",
                  flush=True)
    control("S4_omega_walk")

    n = len(stats)
    ab = sum(1 for s in stats if s.get("all_blocked"))
    print("=" * 74)
    print(f"TOTAL X_3 objects built and screened: {n}")
    print(f"ALL-BLOCKED X_3 objects: {ab}")
    live = Counter(s.get("n_live") for s in stats if "n_live" in s)
    print(f"live-pair distribution: {dict(sorted(live.items()))}")
    diagc = Counter(s.get("diagonal") for s in stats if "diagonal" in s)
    print(f"diagonal vs non-diagonal objects: {dict(diagc)}")
    rk = Counter(tuple(s["ranks"]) for s in stats if "ranks" in s)
    print(f"distinct rank profiles seen: {len(rk)}")
    print(f"max block rank seen: "
          f"{max(max(s['ranks']) for s in stats if 'ranks' in s)}")
    dshapes = Counter()
    for s in stats:
        for k, v in s.get("defect_shapes", {}).items():
            dshapes[k] += v
    print(f"defect colour-multiset shapes over all objects: {dict(dshapes)}")
    RES["stats"] = stats
    RES["summary"] = {"objects": n, "all_blocked": ab,
                      "live_distribution": {str(k): v
                                            for k, v in live.items()},
                      "diagonal_counts": {str(k): v for k, v in diagc.items()},
                      "rank_profiles": len(rk),
                      "defect_shapes": dict(dshapes),
                      "seconds": round(time.time() - t0, 1)}
    RES["escalations"] = ESCALATIONS

    declared = ["S1_near_exact_walk", "S2_allblocked_x2_pushed",
                "S3_diagonal_walk", "S4_omega_walk"]
    missing = [x for x in declared if x not in RAN]
    print(f"CONTROL MANIFEST: declared {len(declared)}, ran {len(RAN)}, "
          f"missing {missing}")
    RES["manifest"] = {"declared": declared, "ran": RAN, "missing": missing}
    assert not missing
    with open(f"{BASE}/results_t1b_builder.json", "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    print("wrote results_t1b_builder.json")


if __name__ == "__main__":
    main()
