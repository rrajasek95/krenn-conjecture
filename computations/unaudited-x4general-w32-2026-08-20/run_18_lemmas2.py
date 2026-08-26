#!/usr/bin/env python3
"""W32 / T18 -- lemma-survival, part 2 (SYM / DEC / FREE).  Part 1 (W27-R2 on
general blocks) landed in log_t10.txt: 13,476 sigma-symmetric GENERAL
backgrounds, k=4 score 0 throughout, rung histogram {0: 13468, 2: 1, 3: 7} --
the slice carries X_3 (informative, ledger 18) and is X_4-silent.

run_10's SYM task aborted with 0/0 tested: it only sampled at k in {2,3} where
random sigma backgrounds are almost never feasible, so the control never
exercised its target (ledger 27).  Repaired here by sampling at k in {1,2}
and requiring a minimum number of genuinely feasible cases."""
import itertools, json, os, random, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction
import w32_bg as BG
from w32_core import (Manifest, all_words, haf_word, offcount, profile,
                      require, zero_source)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "results_t18.json")
rng = random.Random(818181)
R = {}
MAN = Manifest(["SYM_general", "DEC_fails_general", "FREE_forcing_census"])
SIG = {0: 1, 1: 2, 2: 0, 3: 4, 4: 5, 5: 3, 6: 6}
RHO = {0: 1, 1: 2, 2: 0}
PR = (13, 31)


def orbits():
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
                    su, sv = SIG[u], SIG[v]
                    na, nb = RHO[aa], RHO[bb]
                    cur = ((BG.EIDX[(su, sv)], na, nb) if su < sv
                           else (BG.EIDX[(sv, su)], nb, na))
                k = len(reps); reps.append((i, a, b))
                for t in orb:
                    seen[t] = k
    return reps, seen


REPS, ORB = orbits()
DIAG = sorted({ORB[(i, a, a)] for i in range(len(BG.EDGES)) for a in range(3)})


def sigma_F(p, vals):
    F = [[[0] * 3 for _ in range(3)] for _ in BG.EDGES]
    for (i, a, b), k in ORB.items():
        F[i][a][b] = vals[k]
    return F


def reduced_feasible(F, p, k, c=0):
    oid, reps = {}, []
    for y in range(7):
        for d in range(3):
            if (y, d) in oid:
                continue
            t, orb = (y, d), []
            for _ in range(3):
                orb.append(t); t = (SIG[t[0]], RHO[t[1]])
            kk = len(reps); reps.append((y, d))
            for q in orb:
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


def task_SYM():
    ok = tested = feas = 0
    t0 = time.time()
    while tested < 200 and time.time() - t0 < 900:
        p = PR[rng.randrange(2)]
        vals = [0] * len(REPS)
        for k in DIAG:
            if rng.random() < rng.choice([0.4, 0.7, 1.0]):
                vals[k] = rng.randrange(1, p)
        for _ in range(rng.randrange(0, 5)):
            vals[rng.randrange(len(REPS))] = rng.randrange(1, p)
        F = sigma_F(p, vals)
        for kk in (1, 2):
            full = BG.feasible_colours(F, p, k=kk)[0]
            red = reduced_feasible(F, p, kk, 0)
            tested += 1
            feas += 1 if full else 0
            ok += 1 if red == full else 0
    require(tested > 0 and ok == tested,
            f"W28-SYM FAILS on general blocks: {ok}/{tested}")
    require(feas >= 20,
            f"only {feas} feasible cases -- the control never exercised its "
            f"target (ledger 27)")
    MAN.mark("SYM_general")
    R["SYM"] = {"tested": tested, "agree": ok, "feasible_cases": feas}
    print(f"W28-SYM on GENERAL blocks: {ok}/{tested} agreements between the "
          f"21-unknown and the 7-orbit systems ({feas} genuinely feasible) "
          f"=> averaging is slice-INDEPENDENT")


def task_DEC():
    tot = nz = 0
    for _ in range(4):
        src = zero_source(8)
        for e in src:
            for a in range(3):
                for b in range(3):
                    src[e][a][b] = Fraction(rng.randint(-4, 4))
        for w in all_words(8):
            if offcount(w) > 4 or len(set(w)) < 2:
                continue
            if all(x % 2 == 0 for x in profile(w)):
                continue
            tot += 1
            if haf_word(src, w) != 0:
                nz += 1
    require(nz > 0, "DEC control did not fire")
    MAN.mark("DEC_fails_general")
    R["DEC"] = {"odd_class_words_tested": tot, "nonzero": nz,
                "fraction": nz / tot}
    print(f"W28-DEC: {nz}/{tot} ({100*nz/tot:.1f}%) odd-colour-class imposed "
          f"words have H_w != 0 on general sources => parity decoupling is "
          f"diagonal-only")


def task_FREE():
    res, p = {}, 31
    for label in ("diagonal", "general_dense", "general_sparse"):
        forced = []
        for _ in range(8):
            if label == "diagonal":
                F = [[[rng.randrange(p) if a == b else 0 for b in range(3)]
                      for a in range(3)] for _ in BG.EDGES]
            elif label == "general_dense":
                F = [[[rng.randrange(p) for _ in range(3)] for _ in range(3)]
                     for _ in BG.EDGES]
            else:
                F = [[[rng.randrange(p) if rng.random() < .35 else 0
                       for _ in range(3)] for _ in range(3)]
                     for _ in BG.EDGES]
            rows = BG.rows_of(F, p)
            zs = {r[0][0] for i, r in enumerate(rows)
                  if len(r) == 1 and i not in BG.DROP[(0, 4)]
                  and i != BG.CONSTROW[0]}
            forced.append(len(zs))
        res[label] = {"mean_forced_of_21": sum(forced) / len(forced),
                      "samples": forced}
        print(f"  W28-FREE, {label}: mean {sum(forced)/len(forced):.1f} of 21 "
              f"star variables forced to zero by single-entry rows")
    require(res["general_dense"]["mean_forced_of_21"] == 0, "unexpected")
    MAN.mark("FREE_forcing_census")
    R["FREE"] = res


task_SYM(); task_DEC(); print("W28-FREE forcing census:"); task_FREE()
R["manifest"] = MAN.assert_complete()
R["R2_from_run10"] = {"n_sigma_backgrounds": 13476,
                      "k4_score_hist": {"0": 13476},
                      "rung_hist": {"0": 13468, "2": 1, "3": 7},
                      "carries_X3": True}
with open(OUT, "w") as fh:
    json.dump(R, fh, indent=1, sort_keys=True)
print("wrote", OUT)
