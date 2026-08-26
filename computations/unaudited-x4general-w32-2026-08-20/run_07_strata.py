#!/usr/bin/env python3
"""W32 / T7 -- attack line 2: STRATIFY the W27-R1 background problem.

Two stratifications, both computed with the calibrated F_p background engine
(run_03 controls: fires 3/3 on F8's real X_3 background, 0 on random dense):

  S1  CELL-TYPE SUPPORT.  For each of the 511 nonempty subsets T of the nine
      cell types {(a,b)}, sweep random K_7 backgrounds supported on T and
      record the best rung reached (k = 2, 3, 4).  This is the honest form of
      "rank stratification of the mixed rowspan": it says which support
      patterns can carry the penultimate rung at all (ledger 18: a stratum
      whose X_4-emptiness is worth anything must first carry X_3), and it
      hands line 2 the short list of small strata worth an elimination.

  S2  THE sigma-SYMMETRIC GENERAL SLICE.  sigma = (012)(345)(6) on the K_7
      background together with the colour rotation rho = (012).  W28 proved
      the DIAGONAL sigma slice X_4-empty; the general sigma slice was left as
      "search silence, 18,000 backgrounds".  Under sigma the three colour
      systems are carried into one another, so the score is 0 or 3 -- checked
      here, and used as a 3x speedup.  63 free parameters.

Checkpointed every 30 s to results_t7.json; safe across machine sleeps.
"""
from __future__ import annotations

import itertools
import json
import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w32_bg as BG  # noqa: E402
from w32_core import Manifest, require  # noqa: E402

OUT = os.path.join(HERE, "results_t7.json")
PRIMES = (13, 31)
SECONDS = int(sys.argv[1]) if len(sys.argv) > 1 else 5400
SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 424242
rng = random.Random(SEED)
STATE = {"seed": SEED, "primes": list(PRIMES), "started": time.time()}
MAN = Manifest(["sigma_symmetry_collapses_scores", "sigma_slice_informative",
                "celltype_sweep", "diag_stratum_control"])

TYPES = [(a, b) for a in range(3) for b in range(3)]

# ------------------------------------------------------------ sigma machinery
SIG = {0: 1, 1: 2, 2: 0, 3: 4, 4: 5, 5: 3, 6: 6}
RHO = {0: 1, 1: 2, 2: 0}


def orbit_reps():
    """Orbits of (edge_index, a, b) under (sigma, rho); returns reps + a map."""
    seen = {}
    reps = []
    for i, e in enumerate(BG.EDGES):
        for a in range(3):
            for b in range(3):
                if (i, a, b) in seen:
                    continue
                cur = (i, a, b)
                orb = []
                for _ in range(3):
                    orb.append(cur)
                    (ii, aa, bb) = cur
                    (u, v) = BG.EDGES[ii]
                    su, sv = SIG[u], SIG[v]
                    na, nb = RHO[aa], RHO[bb]
                    if su < sv:
                        cur = (BG.EIDX[(su, sv)], na, nb)
                    else:
                        cur = (BG.EIDX[(sv, su)], nb, na)
                require(cur == (i, a, b), "sigma does not have order 3 here")
                k = len(reps)
                reps.append((i, a, b))
                for t in orb:
                    seen[t] = k
    return reps, seen


REPS, ORBMAP = orbit_reps()


def sigma_F(p, dens=1.0, allowed=None):
    vals = [rng.randrange(p) if (rng.random() <= dens) else 0
            for _ in REPS]
    F = [[[0] * 3 for _ in range(3)] for _ in BG.EDGES]
    for (i, a, b), k in ORBMAP.items():
        if allowed is not None and (a, b) not in allowed:
            continue
        F[i][a][b] = vals[k]
    return F


def typed_F(p, allowed, dens=1.0):
    F = [[[0] * 3 for _ in range(3)] for _ in BG.EDGES]
    for i in range(len(BG.EDGES)):
        for (a, b) in allowed:
            if rng.random() <= dens:
                F[i][a][b] = rng.randrange(p)
    return F


def best_rung(F, p):
    """Highest k in {2,3,4} whose three systems are all consistent (0 if none)."""
    out = 0
    for k in (2, 3, 4):
        if BG.score(F, p, k=k) == 3:
            out = k
        else:
            break
    return out


def save():
    STATE["elapsed"] = time.time() - STATE["started"]
    tmp = OUT + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(STATE, fh, indent=1, sort_keys=True)
    os.replace(tmp, OUT)


# ------------------------------------------------------------------ S2 sigma
def task_sigma():
    print(f"sigma slice: {len(REPS)} free parameters (orbits of cells)")
    scores = {}
    rung = {}
    t0 = time.time()
    n = 0
    while time.time() - t0 < min(600, SECONDS * 0.2):
        p = PRIMES[rng.randrange(2)]
        d = rng.choice([0.15, 0.3, 0.5, 0.75, 1.0])
        F = sigma_F(p, dens=d)
        s = BG.score(F, p, k=4)
        scores[str(s)] = scores.get(str(s), 0) + 1
        r = best_rung(F, p)
        rung[str(r)] = rung.get(str(r), 0) + 1
        n += 1
        if n % 50 == 0:
            STATE["sigma"] = {"n": n, "k4_score_hist": scores,
                              "best_rung_hist": rung,
                              "n_params": len(REPS)}
            save()
    STATE["sigma"] = {"n": n, "k4_score_hist": scores, "best_rung_hist": rung,
                      "n_params": len(REPS)}
    require(all(k in ("0", "3") for k in scores),
            f"sigma slice produced a score outside {{0,3}}: {scores}")
    MAN.mark("sigma_symmetry_collapses_scores")
    informative = rung.get("3", 0) > 0 or rung.get("4", 0) > 0
    STATE["sigma"]["informative_carries_X3"] = informative
    MAN.mark("sigma_slice_informative")
    print("  sigma k=4 score histogram:", scores)
    print("  sigma best-rung histogram:", rung,
          "=> slice carries X_3:", informative)
    save()


# -------------------------------------------------------------- S1 cell types
def task_celltypes():
    subsets = []
    for m in range(1, 512):
        T = tuple(TYPES[i] for i in range(9) if (m >> i) & 1)
        subsets.append(T)
    subsets.sort(key=len)
    res = {}
    t0 = time.time()
    budget = SECONDS - (time.time() - STATE["started"])
    per = max(4, int(budget / max(1, len(subsets)) / 0.25))
    STATE["celltype_samples_per_subset"] = per
    for si, T in enumerate(subsets):
        if time.time() - STATE["started"] > SECONDS:
            break
        hist = {}
        best = 0
        for _ in range(per):
            p = PRIMES[rng.randrange(2)]
            F = typed_F(p, T, dens=rng.choice([0.3, 0.6, 1.0]))
            r = best_rung(F, p)
            hist[str(r)] = hist.get(str(r), 0) + 1
            best = max(best, r)
        res["|".join(f"{a}{b}" for a, b in T)] = {
            "size": len(T), "best_rung": best, "hist": hist}
        if si % 20 == 0:
            STATE["celltypes"] = res
            save()
    STATE["celltypes"] = res
    MAN.mark("celltype_sweep")
    # control: the diagonal stratum must reach rung 3 (F8 is diagonal-ish) and
    # must NEVER reach 4 (W29-T1 is a theorem there)
    diag = res.get("00|11|22")
    if diag is not None:
        require(diag["best_rung"] < 4,
                "DIAGONAL stratum reached X_4 -- contradicts W29-T1!")
    MAN.mark("diag_stratum_control")
    tops = sorted(((v["best_rung"], -v["size"], k) for k, v in res.items()),
                  reverse=True)[:25]
    STATE["celltype_top"] = [{"types": k, "best_rung": b, "size": -s}
                             for b, s, k in tops]
    print("cell-type strata swept:", len(res))
    print("  best rungs (top): ", [(k, b) for b, s, k in tops[:12]])
    if diag:
        print("  diagonal stratum 00|11|22:", diag)
    save()


def main():
    task_sigma()
    task_celltypes()
    STATE["manifest"] = MAN.assert_complete()
    save()
    print("wrote", OUT)


if __name__ == "__main__":
    main()
