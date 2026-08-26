#!/usr/bin/env python3
"""W32 / T20 -- lemma survival, corrected.

run_18 found the (sigma, rho)-orbit reduction DISAGREEING with the full system
on 100 of 200 general-block cases.  That is not a failure of W28-SYM: it is an
independent reproduction, on GENERAL blocks, of W28's own mid-run soundness
catch -- the colour rotation rho carries the colour-0 system to the colour-1
system, so the combined group does NOT stabilise a single colour system and
the invariant ansatz is unsound.  W28-SYM's hypothesis is a site group with
TRIVIAL colour action; that version is tested here and does survive.

  SYMa  tau = (012)(345)(6) on sites, TRIVIAL colour action: background
        tau-invariant  =>  colour-c system feasible  <=>  the 9-unknown
        tau-invariant reduced system feasible.   [W28-SYM proper]
  SYMb  the same with the colour rotation switched on: must DISAGREE
        somewhere (the ledger-13-style unsoundness control must FIRE).
  DEC   diagonal parity decoupling has no general analogue.
  FREE  the single-entry-row forcing census.
"""
import itertools, json, os, random, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction
import w32_bg as BG
from w32_core import (Manifest, all_words, haf_word, offcount, profile,
                      require, zero_source)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "results_t20.json")
rng = random.Random(202020)
R, PR = {}, (13, 31)
MAN = Manifest(["SYM_trivial_colour_survives", "SYM_colour_rotation_unsound",
                "DEC_fails_general", "FREE_forcing_census"])
TAU = {0: 1, 1: 2, 2: 0, 3: 4, 4: 5, 5: 3, 6: 6}
RHO = {0: 1, 1: 2, 2: 0}
IDC = {0: 0, 1: 1, 2: 2}


def orbits(rho):
    seen, reps = {}, []
    for i, e in enumerate(BG.EDGES):
        for a in range(3):
            for b in range(3):
                if (i, a, b) in seen:
                    continue
                cur, orb = (i, a, b), []
                for _ in range(3):
                    orb.append(cur)
                    (ii, aa, bb) = cur
                    (u, v) = BG.EDGES[ii]
                    su, sv = TAU[u], TAU[v]
                    na, nb = rho[aa], rho[bb]
                    cur = ((BG.EIDX[(su, sv)], na, nb) if su < sv
                           else (BG.EIDX[(sv, su)], nb, na))
                k = len(reps); reps.append((i, a, b))
                for t in orb:
                    seen[t] = k
    return reps, seen


def mk(p, reps, orb, diagheavy=True):
    vals = [0] * len(reps)
    diag = sorted({orb[(i, a, a)] for i in range(len(BG.EDGES))
                   for a in range(3)})
    for k in (diag if diagheavy else range(len(reps))):
        if rng.random() < rng.choice([0.4, 0.7, 1.0]):
            vals[k] = rng.randrange(1, p)
    for _ in range(rng.randrange(0, 5)):
        vals[rng.randrange(len(reps))] = rng.randrange(1, p)
    F = [[[0] * 3 for _ in range(3)] for _ in BG.EDGES]
    for (i, a, b), k in orb.items():
        F[i][a][b] = vals[k]
    return F


def reduced_feasible(F, p, k, rho, c=0):
    oid, reps = {}, []
    for y in range(7):
        for d in range(3):
            if (y, d) in oid:
                continue
            t, o = (y, d), []
            for _ in range(3):
                o.append(t); t = (TAU[t[0]], rho[t[1]])
            kk = len(reps); reps.append((y, d))
            for q in o:
                oid[q] = kk
    rows = BG.rows_of(F, p)
    drop, ci = BG.DROP[(c, k)], BG.CONSTROW[c]
    aug = []
    for i, r in enumerate(rows):
        if i in drop:
            continue
        v = [0] * len(reps)
        for (j, val) in r:
            v[oid[(j // 3, j % 3)]] = (v[oid[(j // 3, j % 3)]] + val) % p
        aug.append(v + [1 if i == ci else 0])
    r0 = 0
    for col in range(len(reps)):
        pr = None
        for i in range(r0, len(aug)):
            if aug[i][col]:
                pr = i; break
        if pr is None:
            continue
        aug[r0], aug[pr] = aug[pr], aug[r0]
        inv = pow(aug[r0][col], p - 2, p)
        aug[r0] = [x * inv % p for x in aug[r0]]
        for i in range(len(aug)):
            if i != r0 and aug[i][col]:
                f = aug[i][col]
                aug[i] = [(x - f * y) % p for x, y in zip(aug[i], aug[r0])]
        r0 += 1
    return not any(aug[i][len(reps)] and not any(aug[i][:len(reps)])
                   for i in range(len(aug)))


def run(rho, label, n_target=200):
    reps, orb = orbits(rho)
    ok = tested = feas = 0
    t0 = time.time()
    while tested < n_target and time.time() - t0 < 700:
        p = PR[rng.randrange(2)]
        F = mk(p, reps, orb)
        for kk in (1, 2):
            full = BG.feasible_colours(F, p, k=kk)[0]
            red = reduced_feasible(F, p, kk, rho, 0)
            tested += 1
            feas += 1 if full else 0
            ok += 1 if red == full else 0
    return {"tested": tested, "agree": ok, "feasible": feas,
            "n_params": len(reps), "label": label}


a = run(IDC, "trivial colour action")
require(a["feasible"] >= 20, f"control never exercised its target: {a}")
require(a["agree"] == a["tested"],
        f"W28-SYM FAILS with trivial colour action: {a}")
MAN.mark("SYM_trivial_colour_survives")
print("SYMa (W28-SYM proper, trivial colour action) on GENERAL blocks:",
      f"{a['agree']}/{a['tested']} agree ({a['feasible']} feasible)"
      " => averaging is slice-INDEPENDENT")
b = run(RHO, "with colour rotation")
require(b["agree"] < b["tested"],
        "the unsoundness control did NOT fire -- expected disagreements")
MAN.mark("SYM_colour_rotation_unsound")
print("SYMb (colour rotation switched on):",
      f"{b['agree']}/{b['tested']} agree => the invariant ansatz is UNSOUND"
      " on general blocks too (independent reproduction of W28's catch)")
R["SYM"] = {"trivial_colour": a, "colour_rotation": b}

tot = nz = 0
for _ in range(4):
    src = zero_source(8)
    for e in src:
        for x in range(3):
            for y in range(3):
                src[e][x][y] = Fraction(rng.randint(-4, 4))
    for w in all_words(8):
        if offcount(w) > 4 or len(set(w)) < 2:
            continue
        if all(t % 2 == 0 for t in profile(w)):
            continue
        tot += 1
        if haf_word(src, w) != 0:
            nz += 1
require(nz > 0, "DEC control did not fire")
MAN.mark("DEC_fails_general")
R["DEC"] = {"tested": tot, "nonzero": nz, "fraction": nz / tot}
print(f"W28-DEC: {nz}/{tot} ({100*nz/tot:.1f}%) odd-colour-class imposed words"
      f" have H_w != 0 on general sources => parity decoupling is diagonal-only")

res, p = {}, 31
for label in ("diagonal", "general_dense", "general_sparse"):
    forced = []
    for _ in range(8):
        if label == "diagonal":
            F = [[[rng.randrange(p) if x == y else 0 for y in range(3)]
                  for x in range(3)] for _ in BG.EDGES]
        elif label == "general_dense":
            F = [[[rng.randrange(p) for _ in range(3)] for _ in range(3)]
                 for _ in BG.EDGES]
        else:
            F = [[[rng.randrange(p) if rng.random() < .35 else 0
                   for _ in range(3)] for _ in range(3)] for _ in BG.EDGES]
        rows = BG.rows_of(F, p)
        zs = {r[0][0] for i, r in enumerate(rows) if len(r) == 1
              and i not in BG.DROP[(0, 4)] and i != BG.CONSTROW[0]}
        forced.append(len(zs))
    res[label] = {"mean_forced_of_21": sum(forced) / len(forced),
                  "samples": forced}
    print(f"  W28-FREE, {label}: mean {sum(forced)/len(forced):.1f} of 21 star"
          f" variables forced to zero by single-entry rows")
require(res["general_dense"]["mean_forced_of_21"] == 0, "unexpected")
MAN.mark("FREE_forcing_census")
R["FREE"] = res
R["manifest"] = MAN.assert_complete()
R["R2_from_run10"] = {"n_sigma_backgrounds": 13476, "k4_scores": {"0": 13476},
                      "rung_hist": {"0": 13468, "2": 1, "3": 7},
                      "carries_X3": True}
with open(OUT, "w") as fh:
    json.dump(R, fh, indent=1, sort_keys=True)
print("wrote", OUT)
