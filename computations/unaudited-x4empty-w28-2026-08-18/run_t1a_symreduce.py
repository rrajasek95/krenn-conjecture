#!/usr/bin/env python3
"""W28 T1a -- the site reduction re-derived, the AVERAGING LEMMA (W28-SYM),
and exhaustive sweeps over the F_21 / Z_7 symmetric slices.

Stages (argv[1]): all | ctrl | sweepf21 | sweepf21om | sweepz7 | sigma
Every stage checkpoints its own JSON immediately.
"""
from __future__ import annotations

import json
import random
import sys
import time
from fractions import Fraction
from itertools import combinations, product

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-x4empty-w28-2026-08-18")
sys.path.insert(0, BASE)
import w28_core as K                                              # noqa: E402
import w28_sym as S                                               # noqa: E402

N, Z, NS = 8, 7, 7
RES = {}
RAN = []
OUT = f"{BASE}/results_t1a_symreduce.json"


def control(name):
    if name not in RAN:
        RAN.append(name)


def ck(tag=""):
    RES["ran"] = RAN
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    if tag:
        print(f"      [checkpoint {tag}]", flush=True)


def rand_block(rng, lo=-3, hi=3, om=False):
    if om:
        return [[K.Cyc(rng.randint(lo, hi), rng.randint(lo, hi))
                 for _ in range(3)] for _ in range(3)]
    return [[Fraction(rng.randint(lo, hi)) for _ in range(3)] for _ in range(3)]


# ------------------------------------------------------------------- (0)

def stage_ctrl(rng):
    print("=" * 74)
    print("(0) CONTROL: site linearity  H_w = sum_y A_zy[w_z][w_y] C_y(w)")
    print("=" * 74)
    bad = tested = 0
    for t in range(4):
        src = {e: rand_block(rng) for e in K.zero_source(N)}
        for _ in range(40):
            w = tuple(rng.randrange(3) for _ in range(N))
            lhs = K.H_word(src, w, N)
            rhs = Fraction(0)
            for y in range(N):
                if y == Z:
                    continue
                U = tuple(x for x in range(N) if x not in (Z, y))
                cof = K.haf_on(src, {a: w[a] for a in U}, U)
                rhs += K.oriented(src, Z, y)[w[Z]][w[y]] * cof
            tested += 1
            bad += (lhs != rhs)
    print(f"   {tested} random words: {bad} mismatches (must be 0)")
    assert bad == 0
    RES["site_linearity"] = {"tested": tested, "mismatches": bad}
    control("T1a0_site_linearity")

    print("=" * 74)
    print("(0b) CONTROL: a feasible site solve LANDS the source in X_k "
          "(ledger 18: the control lives where the conclusion is nontrivial)")
    print("=" * 74)
    rows = []
    # backgrounds taken from KNOWN X_k points (Delta^3_8 in X_3, F8 in X_3)
    # so that the control is guaranteed non-vacuous, plus sparse diagonal ones
    bgs = [K.delta3_source(N), K.load_F8()]
    for t in range(6):
        s = K.zero_source(N)
        es = list(s)
        rng.shuffle(es)
        for c in range(3):
            for e in es[6 * c:6 * c + 5]:
                s[e][c][c] = Fraction(rng.choice([1, -1, 2]))
        bgs.append(s)
    for k in (2, 3):
        hits = 0
        for src in bgs:
            ok = True
            sols, cols = {}, None
            for c in range(3):
                r, rhs, tags, cols = K.site_rows_exact(src, Z, c, N, k)
                part, kern = K.rref_solve(r, rhs, len(cols))
                if part is None:
                    ok = False
                    break
                sols[c] = part
            if not ok:
                continue
            hits += 1
            new = K.apply_star(src, Z, sols, cols, N)
            inn, w = K.in_Xk(new, N, k)
            rows.append({"k": k, "in_Xk_raw": inn, "witness": None if inn
                         else list(w)})
            assert inn, ("site solve did not land in X_k", k, w)
        print(f"   k={k}: {hits} feasible backgrounds, all landed in X_{k} "
              f"by the RAW word test")
        assert hits > 0, "vacuous control"
    RES["site_solve_lands"] = rows
    control("T1a0b_site_solve_lands")
    ck("ctrl0")

    print("=" * 74)
    print("(1) W28-SYM: the averaging lemma on Z_7-symmetric backgrounds")
    print("=" * 74)
    z7 = S.slice_z7()
    f21 = S.slice_f21()
    recs = []
    agree = disagree = 0
    nfeas = {1: 0, 2: 0, 3: 0, 4: 0}

    def cell(i, j, v=1):
        M = [[Fraction(0)] * 3 for _ in range(3)]
        M[i][j] = Fraction(v)
        return M

    zero = [[Fraction(0)] * 3 for _ in range(3)]
    # STRUCTURED backgrounds that ARE feasible at k = 4 for some colour, so
    # that the lemma is tested on both verdicts at the rung that matters
    fam = [(z7, [cell(0, 0), zero, zero]),
           (z7, [cell(0, 0), cell(1, 1), zero]),
           (z7, [cell(0, 0) , zero, cell(1, 1)]),
           (f21, [cell(0, 0)]),
           (f21, [cell(0, 1)]),
           (f21, [[[Fraction(1)] * 3 for _ in range(3)]])]
    for sl, ntr in ((z7, 4), (f21, 4)):
        for t in range(ntr):
            fam.append((sl, [rand_block(rng, -2, 2)
                             for _ in range(sl.nblocks)]))
    for sl, blocks in fam:
        if True:
            src7 = sl.build(blocks)
            assert sl.check(src7) == 0
            src8 = S.lift(src7)
            for k in (1, 2, 3, 4):
                for c in range(3):
                    fu, dim = S.full_feasible(src8, c, k)
                    fa, rk, rc = S.averaged_feasible(src7, c, k)
                    recs.append({"slice": sl.name, "k": k,
                                 "colour": c, "full": fu, "avg": fa,
                                 "kernel_dim": dim, "rank_mixed3": rk})
                    if fu == fa:
                        agree += 1
                    else:
                        disagree += 1
                    if fu:
                        nfeas[k] += 1
            print(f"   {sl.name}: k=4 verdicts "
                  f"{[(r['colour'], r['full'], r['avg']) for r in recs[-3:]]}",
                  flush=True)
    print(f"   agreement full(21 unknowns) vs averaged(3 unknowns): "
          f"{agree} agree / {disagree} disagree")
    print(f"   feasible counts by rung (non-vacuity): {nfeas}")
    assert disagree == 0, "AVERAGING LEMMA FAILS"
    assert nfeas[1] > 0 and nfeas[4] > 0, "vacuous control (nothing feasible)"
    RES["averaging_lemma"] = {"agree": agree, "disagree": disagree,
                              "feasible_by_k": nfeas, "records": recs}
    control("T1a1_averaging_lemma")
    ck("avg")

    print("=" * 74)
    print("(2) W27-R2 on F_21 backgrounds: the three colour systems agree; "
          "plus a ledger-18 negative control")
    print("=" * 74)
    same = 0
    tot = 0
    for t in range(40):
        blocks = [rand_block(rng, -2, 2) for _ in range(f21.nblocks)]
        src7 = f21.build(blocks)
        v = [S.averaged_feasible(src7, c, 4)[:2] for c in range(3)]
        tot += 1
        same += (len(set(x[0] for x in v)) == 1 and len(set(x[1] for x in v)) == 1)
    print(f"   {tot} F_21 backgrounds: {same} had all three colour systems "
          f"identical (feasibility AND rank)")
    assert same == tot
    dis = 0
    tot2 = 0
    neg = [[cell(0, 0), zero, zero], [cell(0, 0), cell(1, 1), zero],
           [cell(0, 0), cell(0, 0), zero], [cell(0, 1), zero, zero],
           [cell(0, 0), cell(1, 1), cell(1, 1)]]
    for t in range(300):
        neg.append([[[Fraction(rng.choice([0, 0, 0, 0, 0, 1, -1]))
                      for _ in range(3)] for _ in range(3)] for _ in range(3)])
    for blocks in neg:
        src7 = z7.build(blocks)
        v = [S.averaged_feasible(src7, c, 4)[:2] for c in range(3)]
        tot2 += 1
        if len(set(x[1] for x in v)) > 1:
            dis += 1
    print(f"   negative control: {tot2} Z_7-only backgrounds, {dis} had "
          f"DIFFERENT ranks across colours (control not vacuous)")
    assert dis > 0
    RES["R2_check"] = {"f21_same": same, "f21_total": tot,
                       "z7_rank_disagree": dis, "z7_total": tot2}
    control("T1a2_R2")
    ck("r2")


# ------------------------------------------------------------- sweeps

def sweep(sl, gen, label, colours=(0,), k=4, limit=None, report=200000):
    """Exhaustive/enumerated sweep; returns (n, hits, rank_hist)."""
    uord = {c: S.constrained_u(c, k) for c in colours}
    n = 0
    hits = []
    hist = {}
    t0 = time.time()
    for blocks in gen:
        src7 = sl.build(blocks)
        okall = True
        info = []
        for c in colours:
            ok, rk, rc = S.averaged_feasible(src7, c, k, uord[c])
            info.append((ok, rk))
            if not ok:
                okall = False
                break
        hist[str(info[-1][1])] = hist.get(str(info[-1][1]), 0) + 1
        n += 1
        if okall:
            hits.append({"blocks": [[[str(x) for x in r] for r in B]
                                    for B in blocks], "info": str(info)})
            print(f"      *** FEASIBLE {label} at #{n}: {blocks}", flush=True)
        if limit and n >= limit:
            break
        if n % report == 0:
            print(f"      ... {label} {n} done ({round(time.time()-t0,1)}s), "
                  f"hits {len(hits)}", flush=True)
    return n, hits, hist


def gen_entries(vals, nblocks, om=False):
    cells = list(product(vals, repeat=9))
    for combo in product(cells, repeat=nblocks):
        yield [[[c[3 * i + j] for j in range(3)] for i in range(3)]
               for c in combo]


def stage_sweepf21(rng):
    f21 = S.slice_f21()
    print("=" * 74)
    print("(3) F_21 SLICE (9 parameters): EXHAUSTIVE over {-1,0,1}^9 = 19683")
    print("=" * 74)
    vals = [Fraction(-1), Fraction(0), Fraction(1)]
    n, hits, hist = sweep(f21, gen_entries(vals, 1), "F21{-1,0,1}",
                          colours=(0,), report=2000)
    print(f"   {n} backgrounds, feasible {len(hits)}; mixed-rank histogram "
          f"{hist}")
    RES["f21_pm1"] = {"n": n, "hits": hits, "rank_hist": hist}
    control("T1a3_f21_pm1")
    ck("f21pm1")


def stage_sweepf21om(rng):
    f21 = S.slice_f21()
    print("=" * 74)
    print("(3b) F_21 SLICE over Q(omega): EXHAUSTIVE over {0,1,omega}^9 "
          "(ledger 19/20: the cube root of unity is structural here)")
    print("=" * 74)
    vals = [K.Cyc(0, 0), K.Cyc(1, 0), K.Cyc(0, 1)]
    n, hits, hist = sweep(f21, gen_entries(vals, 1), "F21{0,1,w}",
                          colours=(0,), report=2000)
    print(f"   {n} backgrounds, feasible {len(hits)}; rank histogram {hist}")
    RES["f21_omega"] = {"n": n, "hits": hits, "rank_hist": hist}
    control("T1a3b_f21_omega")
    ck("f21om")

    print("   ... plus {0,1,-1,omega,-omega,1+omega}^9 random exact sample")
    pool = [K.Cyc(0, 0), K.Cyc(1, 0), K.Cyc(-1, 0), K.Cyc(0, 1), K.Cyc(0, -1),
            K.Cyc(1, 1), K.Cyc(2, -1), K.Cyc(-2, 3)]
    hits2 = 0
    for t in range(20000):
        B = [[[pool[rng.randrange(len(pool))] for _ in range(3)]
              for _ in range(3)]]
        ok, rk, rc = S.averaged_feasible(f21.build(B), 0, 4)
        if ok:
            hits2 += 1
            print(f"      *** FEASIBLE random-omega: {B}", flush=True)
    print(f"   20000 random Q(omega) F_21 backgrounds: {hits2} feasible")
    RES["f21_omega_random"] = {"n": 20000, "hits": hits2}
    control("T1a3c_f21_omega_random")
    ck("f21omr")


def stage_sweepz7(rng):
    z7 = S.slice_z7()
    print("=" * 74)
    print("(4) Z_7 SLICE (27 parameters, colour-asymmetric): structured "
          "exhaustive strata + random exact sweeps")
    print("=" * 74)
    out = {}
    # (a) single-cell blocks with weights in {1,-1}: 19 options per block
    cells = [[[Fraction(0)] * 3 for _ in range(3)]]
    for i in range(3):
        for j in range(3):
            for s in (1, -1):
                M = [[Fraction(0)] * 3 for _ in range(3)]
                M[i][j] = Fraction(s)
                cells.append(M)

    def gen_cells():
        for c in product(range(len(cells)), repeat=3):
            yield [cells[c[0]], cells[c[1]], cells[c[2]]]

    n, hits, hist = sweep(z7, gen_cells(), "Z7 single-cell",
                          colours=(0, 1, 2), report=2000)
    print(f"   single-cell: {n} backgrounds ({len(cells)}^3), feasible "
          f"{len(hits)}; rank hist {hist}")
    out["single_cell"] = {"n": n, "hits": hits, "rank_hist": hist}
    RES["z7"] = out
    ck("z7cell")

    # (b) diagonal blocks (the monochrome family) with weights in {1,-1,2}
    dia = [[[Fraction(0)] * 3 for _ in range(3)]]
    for c in range(3):
        for s in (1, -1, 2):
            M = [[Fraction(0)] * 3 for _ in range(3)]
            M[c][c] = Fraction(s)
            dia.append(M)

    def gen_dia():
        for c in product(range(len(dia)), repeat=3):
            yield [dia[c[0]], dia[c[1]], dia[c[2]]]

    n, hits, hist = sweep(z7, gen_dia(), "Z7 diagonal", colours=(0, 1, 2),
                          report=2000)
    print(f"   diagonal: {n} backgrounds, feasible {len(hits)}; hist {hist}")
    out["diagonal"] = {"n": n, "hits": hits, "rank_hist": hist}
    RES["z7"] = out
    ck("z7dia")

    # (c) {-1,0,1} in each of the three blocks -- 3^27 is impossible, so:
    #     exhaustive over 0/1 SUPPORTS with all-ones weights (2^27 = too many)
    #     -> exhaustive over supports of size <= 2 per block, then random.
    tot = 0
    hits3 = 0
    hist3 = {}
    uord = {c: S.constrained_u(c, 4) for c in range(3)}
    t0 = time.time()
    for t in range(120000):
        B = [[[Fraction(rng.choice([0, 0, 1, -1, 2, -2])) for _ in range(3)]
              for _ in range(3)] for _ in range(3)]
        src7 = z7.build(B)
        ok = True
        rk = None
        for c in range(3):
            f, rk, rc = S.averaged_feasible(src7, c, 4, uord[c])
            if not f:
                ok = False
                break
        hist3[str(rk)] = hist3.get(str(rk), 0) + 1
        tot += 1
        if ok:
            hits3 += 1
            print(f"      *** FEASIBLE Z7 random: {B}", flush=True)
        if tot % 20000 == 0:
            print(f"      ... z7 random {tot} ({round(time.time()-t0,1)}s)",
                  flush=True)
            out["random"] = {"n": tot, "hits": hits3, "rank_hist": hist3}
            RES["z7"] = out
            ck(f"z7rand{tot}")
    print(f"   random sparse-integer: {tot} backgrounds, feasible {hits3}")
    out["random"] = {"n": tot, "hits": hits3, "rank_hist": hist3}
    RES["z7"] = out
    control("T1a4_z7")
    ck("z7")


def main():
    t0 = time.time()
    rng = random.Random(280818)
    stage = sys.argv[1] if len(sys.argv) > 1 else "all"
    global OUT
    OUT = f"{BASE}/results_t1a_{stage}.json"
    if stage in ("all", "ctrl"):
        stage_ctrl(rng)
    if stage in ("all", "sweepf21"):
        stage_sweepf21(rng)
    if stage in ("all", "sweepf21om"):
        stage_sweepf21om(rng)
    if stage in ("all", "sweepz7"):
        stage_sweepz7(rng)
    RES["stage"] = stage
    RES["seconds"] = round(time.time() - t0, 1)
    declared = {"ctrl": ["T1a0_site_linearity", "T1a0b_site_solve_lands",
                         "T1a1_averaging_lemma", "T1a2_R2"],
                "sweepf21": ["T1a3_f21_pm1"],
                "sweepf21om": ["T1a3b_f21_omega", "T1a3c_f21_omega_random"],
                "sweepz7": ["T1a4_z7"]}
    need = []
    for s, d in declared.items():
        if stage in ("all", s):
            need += d
    missing = [x for x in need if x not in RAN]
    RES["manifest"] = {"declared": need, "ran": RAN, "missing": missing}
    print(f"CONTROL MANIFEST ({stage}): declared {len(need)}, ran {len(RAN)}, "
          f"missing {missing}")
    assert not missing, missing
    ck("final")
    print(f"wrote {OUT} ({RES['seconds']}s)")


if __name__ == "__main__":
    main()
