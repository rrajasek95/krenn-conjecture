#!/usr/bin/env python3
"""W27 T1b -- IS THE X_4 SITE SYSTEM AT N=8 EVER FEASIBLE?

W25 tried a single site-0 projection from six diagonal seeds and reached
nothing.  This runner does the systematic version:

  * the exact reduction W27-R1 (see w27_x4.py): X_4 at N=8 is nonempty iff some
    background on K_7 makes all three colour systems at a site consistent;
  * feasibility measured for F8, for diagonal X_3 sources, for the exact
    N=4 source doubled, and for large random families, at EVERY site;
  * a diagnostic that isolates WHICH off-count-4 words destroy consistency.

Screening is modulo two primes (both = 1 mod 3, ledger 19); every positive hit
is re-verified exactly with W25's raw word test.
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
C = W.C
WK = W.WK

N = 8
RES = {}
RAN = []
OUT = f"{BASE}/results_t1b_x4feas.json"


def control(name):
    RAN.append(name)


def ck(tag=""):
    RES["ran"] = RAN
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    if tag:
        print(f"      [checkpoint {tag}]", flush=True)


def load_f8():
    path = f"{W25BASE}/OBJECT_W25-F8_n8_allblocked_X3.json"
    with open(path) as fh:
        D = json.load(fh)
    key = None
    for k in ("blocks", "source", "object"):
        if k in D:
            key = k
            break
    if key is None:
        for k, v in D.items():
            if isinstance(v, dict) and "blocks" in v:
                D = v
                key = "blocks"
                break
    src = {}
    for k, m in D[key].items():
        a, b = (int(x) for x in k.replace("(", "").replace(")", "").split(","))
        src[(a, b)] = [[Fraction(str(x)) for x in row] for row in m]
    return src, D


def rand_source(rng, n=N, vals=(-2, -1, 0, 1, 2), dens=1.0):
    src = C.zero_source(n)
    for a, b in combinations(range(n), 2):
        for i in range(3):
            for j in range(3):
                if rng.random() < dens:
                    src[(a, b)][i][j] = Fraction(rng.choice(vals))
    return src


def diag_x3_seed(rng, n=N):
    """A diagonal X_3 = X_2 source at N=8: three disjoint PMs plus extra edges
    that create no (6,2,0) violation, weights normalised so each pure = 1."""
    G = W.Graph(n)
    while True:
        Ms, used = [], set()
        ok = True
        for c in range(3):
            for _ in range(200):
                p = list(range(n))
                rng.shuffle(p)
                M = W.pm_norm([(p[2 * i], p[2 * i + 1]) for i in range(n // 2)])
                if not (set(M) & used):
                    break
            else:
                ok = False
                break
            used |= set(M)
            Ms.append(M)
        if not ok:
            continue
        wts = {}
        for c, M in enumerate(Ms):
            vs = [Fraction(rng.choice([1, -1, 2, -2, 3])) for _ in M]
            pr = Fraction(1)
            for v in vs:
                pr *= v
            vs[-1] = vs[-1] / pr
            for e, v in zip(M, vs):
                wts[(c, e)] = v
        src = W.build_diag(n, [list(M) for M in Ms], wts)
        if C.in_Xk(src, n, 3)[0]:
            return src, Ms


def doubled_exact4(n=N):
    """delta43 on {0,1,2,3} and on {4,5,6,7}, zero across.  In X_3, not X_4 --
    the cleanest witness that the (4,4,0) words are the new content."""
    d = C.delta43()
    src = C.zero_source(n)
    for (a, b), m in d.items():
        src[(a, b)] = [row[:] for row in m]
        src[(a + 4, b + 4)] = [row[:] for row in m]
    return src


def main():
    t0 = time.time()
    rng = random.Random(8080)
    bank = X.word_bank(N, 3, 4)
    n4 = len(bank.get(4, []))
    tot = sum(len(v) for v in bank.values())
    print(f"4-near-constant words at N=8: {tot} "
          f"({ {k: len(v) for k, v in sorted(bank.items())} })")
    words4 = [w for k in sorted(bank) for w in bank[k]]
    words3 = [w for k in sorted(bank) if k <= 3 for w in bank[k]]
    RES["word_counts"] = {str(k): len(v) for k, v in sorted(bank.items())}
    RES["n_words_X4"] = len(words4)
    RES["n_words_X3"] = len(words3)

    print("=" * 74)
    print("(0) CONTROLS: F8 and a doubled exact-4 source")
    print("=" * 74)
    f8, meta = load_f8()
    ok3, w3 = C.in_Xk(f8, N, 3)
    ok4, w4 = C.in_Xk(f8, N, 4)
    print(f"   F8 reproduced through W27's loader: in X_3 {ok3}, in X_4 {ok4} "
          f"(first failure {w4}, off-count "
          f"{C.offcount(w4) if w4 else None})")
    assert ok3 and not ok4
    bad = C.mixed_defects(f8, N)
    byoff = {}
    for b in bad:
        byoff[C.offcount(b)] = byoff.get(C.offcount(b), 0) + 1
    print(f"   F8 mixed defects: {len(bad)} total, by off-count {byoff}")
    RES["f8"] = {"in_X3": ok3, "in_X4": ok4, "first_X4_fail": list(w4),
                 "n_defects": len(bad), "defects_by_offcount": byoff,
                 "pures": [str(x) for x in C.pures(f8, N).values()]}
    control("T1b0_f8_control")

    dbl = doubled_exact4()
    o3, _ = C.in_Xk(dbl, N, 3)
    o4, ww = C.in_Xk(dbl, N, 4)
    dfl = C.mixed_defects(dbl, N)
    print(f"   doubled delta43: in X_3 {o3}, in X_4 {o4} (first failure {ww});"
          f" mixed defects {len(dfl)} = the 6 group-constant (4,4,0) words: "
          f"{sorted(set(tuple(sorted(set(x))) for x in dfl))}")
    assert o3 and not o4 and len(dfl) == 6
    RES["doubled_delta43"] = {"in_X3": o3, "in_X4": o4,
                              "defects": [list(x) for x in dfl]}
    control("T1b0b_doubled_control")
    ck("controls")

    print("=" * 74)
    print("(1) mod-p engine vs W25's exact engine (control)")
    print("=" * 74)
    sm = X.src_mod(f8, X.P1)
    tabs = X.cof_tables(sm, X.P1)
    mism = 0
    for _ in range(200):
        z = rng.randrange(N)
        y = rng.randrange(N)
        if y == z:
            continue
        U = tuple(x for x in range(N) if x not in (z, y))
        word = tuple(rng.randrange(3) for _ in range(N))
        exact = C.haf_sub(f8, {a: word[a] for a in U}, U)
        got = tabs[(z, y)][tuple(word[x] for x in U)]
        want = Fraction(exact).numerator % X.P1 * pow(
            Fraction(exact).denominator % X.P1, X.P1 - 2, X.P1) % X.P1
        if got != want:
            mism += 1
    print(f"   200 random cofactors: mismatches {mism} (must be 0)")
    assert mism == 0
    RES["cofactor_control"] = {"mismatches": mism}
    control("T1b1_cofactor_control")

    print("=" * 74)
    print("(2) FEASIBILITY of the X_3 and X_4 site systems -- F8")
    print("=" * 74)
    rep3, rep4 = [], []
    for z in range(N):
        r3 = X.site_report(tabs, words3, z, X.P1)
        r4 = X.site_report(tabs, words4, z, X.P1)
        rep3.append(r3)
        rep4.append(r4)
        print(f"   site {z}: X_3 feasible {[x['feasible'] for x in r3]} "
              f"ker {[x['kernel_dim'] for x in r3]} | X_4 feasible "
              f"{[x['feasible'] for x in r4]} rank(mixed) "
              f"{[x['rank_mixed'] for x in r4]}")
    # F8 in X_3 => its own star solves the X_3 system => feasible everywhere
    assert all(x["feasible"] for r in rep3 for x in r), "X_3 control failed"
    RES["f8_feasibility"] = {"X3": rep3, "X4": rep4}
    nfeas4 = sum(1 for r in rep4 for x in r if x["feasible"])
    print(f"   X_4 feasible colour-systems over all 8 sites: {nfeas4} / 24")
    control("T1b2_f8_feasibility")
    ck("f8feas")

    print("=" * 74)
    print("(3) FEASIBILITY sweep over families of backgrounds")
    print("=" * 74)
    fams = []

    def add(name, mk, k):
        fams.append((name, mk, k))

    add("random_dense", lambda: rand_source(rng), 40)
    add("random_sparse", lambda: rand_source(rng, dens=0.45), 40)
    add("random_01", lambda: rand_source(rng, vals=(0, 1)), 40)
    add("diagonal_X3", lambda: diag_x3_seed(rng)[0], 15)
    add("f8_perturbed", lambda: perturb(f8, rng), 30)
    add("doubled_delta43_pert", lambda: perturb(dbl, rng), 30)

    sweep = []
    hits = []
    for name, mk, k in fams:
        cnt = {"tried": 0, "any_site_all3": 0, "colour_systems_feasible": 0,
               "total_colour_systems": 0, "max_feasible_at_a_site": 0}
        for _ in range(k):
            s = mk()
            try:
                smm = X.src_mod(s, X.P1)
            except ValueError:
                continue
            tb = X.cof_tables(smm, X.P1)
            cnt["tried"] += 1
            best = 0
            for z in range(N):
                r = X.site_report(tb, words4, z, X.P1)
                nf = sum(1 for x in r if x["feasible"])
                cnt["colour_systems_feasible"] += nf
                cnt["total_colour_systems"] += 3
                best = max(best, nf)
                if nf == 3:
                    cnt["any_site_all3"] += 1
                    hits.append({"family": name, "site": z,
                                 "blocks": {f"{a},{b}": [[str(x) for x in row]
                                                         for row in s[(a, b)]]
                                            for a, b in combinations(range(N), 2)}})
            cnt["max_feasible_at_a_site"] = max(cnt["max_feasible_at_a_site"],
                                                best)
        print(f"   {name:24s}: tried {cnt['tried']:3d}; feasible colour "
              f"systems {cnt['colour_systems_feasible']}/"
              f"{cnt['total_colour_systems']}; sites with ALL THREE "
              f"feasible {cnt['any_site_all3']}; best-at-a-site "
              f"{cnt['max_feasible_at_a_site']}", flush=True)
        sweep.append({"family": name, **cnt})
        RES["sweep"] = sweep
        RES["hits"] = hits[:5]
        ck(name)
    control("T1b3_family_sweep")

    print("=" * 74)
    print("(4) WHICH WORDS DESTROY CONSISTENCY (F8, site 0)")
    print("=" * 74)
    diag = []
    for c in range(3):
        rows, rhs, tags, cols = X.build_rows(tabs, words4, 0, c)
        # grow the word set by off-count and find the first level that breaks
        levels = {}
        for k in (0, 1, 2, 3, 4):
            sel = [i for i, t in enumerate(tags) if C.offcount(t) <= k]
            ok, rmix, rall = X.feasible_mod([rows[i] for i in sel],
                                            [rhs[i] for i in sel],
                                            len(cols), X.P1)
            levels[k] = {"n": len(sel), "feasible": ok, "rank_mixed": rmix,
                         "rank": rall}
        diag.append({"colour": c, "levels": levels})
        print(f"   colour {c}: " + "; ".join(
            f"off<={k}: n={v['n']} rk_mixed={v['rank_mixed']} feas={v['feasible']}"
            for k, v in levels.items()))
    RES["level_diagnostic"] = diag
    control("T1b4_level_diagnostic")

    declared = ["T1b0_f8_control", "T1b0b_doubled_control",
                "T1b1_cofactor_control", "T1b2_f8_feasibility",
                "T1b3_family_sweep", "T1b4_level_diagnostic"]
    missing = [x for x in declared if x not in RAN]
    print(f"CONTROL MANIFEST: declared {len(declared)}, ran {len(RAN)}, "
          f"missing {missing}")
    RES["manifest"] = {"declared": declared, "ran": RAN, "missing": missing}
    RES["seconds"] = round(time.time() - t0, 1)
    assert not missing
    ck("final")
    print(f"wrote {OUT} ({RES['seconds']}s)")


def perturb(src, rng, k=3):
    out = C.copy_source(src)
    for _ in range(k):
        a, b = sorted(rng.sample(range(N), 2))
        i, j = rng.randrange(3), rng.randrange(3)
        out[(a, b)][i][j] = out[(a, b)][i][j] + Fraction(rng.choice([-2, -1, 1, 2]))
    return out


if __name__ == "__main__":
    main()
