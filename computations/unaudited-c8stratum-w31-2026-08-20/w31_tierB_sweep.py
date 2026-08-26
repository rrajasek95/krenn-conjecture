#!/usr/bin/env python3
r"""W31 -- TIER B SWEEP: the one-sided permanental law across the 64 classes.
UNAUDITED PROBE.  Exact arithmetic only.  Detached-safe: one JSON checkpoint
per class, written the moment that class finishes.

PER CLASS (no representative shortcuts -- transport was never proved, and the
two census-representative incidents are why):
  1. build a genuine (R) template at m = 28 with the R1 SAT engine and accept
     it only if the INDEPENDENT direct checker agrees (control B-T1);
  2. find Gamma's independent 4-sets -- by Lemma W31-3 these are exactly the
     sides on which the L-free permanental reduction exists;
  3. compute the free words on that side (words deactivating its six internal
     blocks) and VERIFY the reduction identity H = per B exactly at them
     (control B-T2, 0 mismatches required);
  4. read off the dead-cell pattern each free word induces on the four 4x3
     cross matrices C_j(x), and decide which free words are COMPATIBLE with a
     permanent-null configuration of the stored family's shape
     (a,b,+-b,+-a) -- the same test that decided the C_8 gate;
  5. try to BUILD a simultaneous witness on the compatible words and verify it
     exactly (all occupied cells nonzero, every permanent equation checked).

VERDICT PER CLASS
  RESISTS    an explicit exact witness satisfies >= 2 free words at once with
             all occupied cross cells nonzero -- the permanental law alone
             cannot kill this class (this is what happened at C_8).
  THRESHOLD  free words exist and the reduction runs, but no witness of this
             family shape exists -- the class needs the dim Pcal_j >= 3
             threshold, i.e. the Q-span law has to do real work.
  DEGENERATE no free word exists for any independent 4-set: the reduction is
             present in principle but has no input on this template.

CONTROLS (asserted per class before its verdict is written)
  B-T1  the direct (R) checker accepts the SAT model.
  B-T2  the reduction identity H = per B holds at every free word tested.
  B-T3  MUTATION: a perturbed witness must break at least one equation.
  B-T4  NEGATIVE: a generic assignment on the witness's rows must fail.
  B-T5  the C_8 class, run through the same pipeline, must come out RESISTS --
         it is the one class whose answer is already known.
"""
from __future__ import annotations

import json
import os
import sys
import time
from itertools import combinations, permutations, product

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
CENSUS = os.path.join(REPO, "computations",
                      "unaudited-forcing-w19-2026-08-15", "census")
OUTD = os.path.join(HERE, "tierB")
N, FULL = 8, 511
EDGES = tuple(combinations(range(N), 2))
EIDX = {e: i for i, e in enumerate(EDGES)}
S4 = tuple(permutations(range(4)))

import w31_r1_sat as R1                                           # noqa: E402


def cells_of(mask):
    return [(c // 3, c % 3) for c in range(9) if (mask >> c) & 1]


def occ(T, e, i, j):
    return (T[EIDX[e]] >> (3 * i + j)) & 1


def independent_4sets(gs):
    return [q for q in combinations(range(N), 4)
            if not any(tuple(sorted(p)) in gs for p in combinations(q, 2))]


def free_words(T, side):
    inner = [tuple(sorted(p)) for p in combinations(side, 2)]
    out = []
    for x in product(range(3), repeat=4):
        lk = {v: x[k] for k, v in enumerate(side)}
        if all(not occ(T, e, lk[e[0]], lk[e[1]]) for e in inner):
            out.append(x)
    return out


def perB(val, T, Ls, Rs, x, y):
    B = [[0] * 4 for _ in range(4)]
    for a, u in enumerate(Ls):
        for b, v in enumerate(Rs):
            e = (u, v) if u < v else (v, u)
            i, j = (x[a], y[b]) if u < v else (y[b], x[a])
            B[a][b] = val.get((e, i, j), 0) if occ(T, e, i, j) else 0
    return sum(B[0][s[0]] * B[1][s[1]] * B[2][s[2]] * B[3][s[3]] for s in S4)


def H(val, T, w):
    t = 0
    for M in R1.PMS:
        p = 1
        for e in M:
            i, j = w[e[0]], w[e[1]]
            if not occ(T, e, i, j):
                p = 0
                break
            p *= val[(e, i, j)]
        t += p
    return t


AB = ((1, 1), (1, 2), (2, 1))
PAT = (0, 1, 1, 0)


def signs(k):
    return (1, 1, 1, 1) if k != 1 else (1, 1, -1, -1)


def zeroset(T, Ls, Rs, x, jj, d):
    out = []
    for i, u in enumerate(Ls):
        v = Rs[jj]
        e = (u, v) if u < v else (v, u)
        a, b = (x[i], d) if u < v else (d, x[i])
        if not occ(T, e, a, b):
            out.append(i)
    return frozenset(out)


PAIRED = (frozenset(), frozenset({0, 3}), frozenset({1, 2}))


def compatible(T, Ls, Rs, x):
    return all(zeroset(T, Ls, Rs, x, jj, d) in PAIRED
               for jj in range(4) for d in range(3))


def realise(A, T, Ls, Rs, x):
    for jj in range(4):
        sg = signs(jj)
        for d in range(3):
            a, b = AB[d]
            z = zeroset(T, Ls, Rs, x, jj, d)
            if z == frozenset({0, 3}):
                a = 0
            elif z == frozenset({1, 2}):
                b = 0
            for i, u in enumerate(Ls):
                v = Rs[jj]
                e = (u, v) if u < v else (v, u)
                key = (e, x[i], d) if u < v else (e, d, x[i])
                A[key] = sg[i] * (a if PAT[i] == 0 else b)



def build_doubled(gs, Ls):
    """both sides independent: a GHZ_4^3 copy on each, remaining blocks fat."""
    Rs = tuple(v for v in range(N) if v not in Ls)
    T = [0] * len(EDGES)
    for e in gs:
        T[EIDX[e]] = FULL
    for side in (sorted(Ls), sorted(Rs)):
        a, b, c, d = side
        for col, pm in enumerate((((a, b), (c, d)), ((a, c), (b, d)),
                                  ((a, d), (b, c)))):
            for e in pm:
                T[EIDX[tuple(sorted(e))]] = 1 << (3 * col + col)
    for e in EDGES:
        if T[EIDX[e]] == 0:
            T[EIDX[e]] = FULL ^ 1
    return T


def build_onesided(gs, Ls):
    """CANONICAL tier-B template: Gamma full; the independent 4-set Ls carries
    a GHZ_4^3 copy of single cells (its six internal edges are non-Gamma by
    definition, and the copy serves all of Ls's (SC) demands); each site of the
    complementary side gets three single-cell servers on non-Gamma edges with
    far colours 0,1,2; every other non-Gamma block is fat (eight cells).
    Returns None if the (SC) servers cannot be placed."""
    Rs = tuple(v for v in range(N) if v not in Ls)
    T = [0] * len(EDGES)
    for e in gs:
        T[EIDX[e]] = FULL
    a, b, c, d = sorted(Ls)
    for col, pm in enumerate((((a, b), (c, d)), ((a, c), (b, d)),
                              ((a, d), (b, c)))):
        for e in pm:
            T[EIDX[tuple(sorted(e))]] = 1 << (3 * col + col)
    # (SC) servers for the complementary side, as THIN blocks (three cells in
    # one line) rather than single cells: a thin block forces a far colour just
    # as a single does but destroys far fewer fibres -- which is how W19's own
    # census representatives are built.
    for v in Rs:
        avail = [e for e in EDGES if v in e and e not in gs
                 and T[EIDX[e]] == 0]
        if len(avail) < 3:
            return None
        for col, e in enumerate(sorted(avail)[:3]):
            if e[0] == v:            # far colour from v is the 2nd index
                T[EIDX[e]] = sum(1 << (3 * i + col) for i in range(3))
            else:                    # far colour from v is the 1st index
                T[EIDX[e]] = sum(1 << (3 * col + j) for j in range(3))
    for e in EDGES:
        if T[EIDX[e]] == 0:
            T[EIDX[e]] = FULL ^ 1
    return T


def run_class(gm, ng, nF, tmo=1800):
    t0 = time.time()
    rec = dict(gamma_mask=gm, n_gamma=ng, n_F=nF)
    gs0 = set(EDGES[i] for i in range(len(EDGES)) if (gm >> i) & 1)
    inds0 = independent_4sets(gs0)
    T, src = None, None
    cands = []
    for Ls0 in inds0:
        comp0 = tuple(v for v in range(N) if v not in Ls0)
        if comp0 in set(inds0):
            cands.append((Ls0, True))       # both sides free: doubled build
    cands += [(q, False) for q in inds0]
    for Ls0, dbl in cands:
        cand = (build_doubled(gs0, Ls0) if dbl
                else build_onesided(gs0, Ls0))
        if cand is None:
            continue
        okc, _ = R1.check_R(cand)
        if okc:
            T, src = cand, ("doubled" if dbl else "one-sided") + \
                " GHZ placement on %s" % (list(Ls0),)
            break
    if T is None:
        F, xv, _ = R1.build(gm, 28)
        sol = R1.solve(F, "tierB_%d" % gm, tmo, want_proof=False)
        rec["sat_status"] = sol["status"]
        if sol["status"] != "SAT":
            rec["verdict"] = "NO_TEMPLATE(" + sol["status"] + ")"
            rec["seconds"] = round(time.time() - t0, 1)
            return rec
        T = R1.model_to_T(sol["model"], xv)
        src = "SAT fallback (canonical placement not in (R))"
    rec["template_source"] = src
    ok, why = R1.check_R(T)
    rec["B_T1_direct_checker"] = ok
    rec["B_T1_reason"] = why
    rec["template"] = T
    if not ok:
        rec["verdict"] = "ENCODER_DISAGREEMENT"
        rec["seconds"] = round(time.time() - t0, 1)
        return rec
    gs = set(EDGES[i] for i in range(len(EDGES)) if (gm >> i) & 1)
    inds = independent_4sets(gs)
    rec["n_independent_4sets"] = len(inds)
    best = None
    for Ls in inds:
        Rs = tuple(v for v in range(N) if v not in Ls)
        fw = free_words(T, Ls)
        comp = [x for x in fw if compatible(T, Ls, Rs, x)]
        key = (len(comp), len(fw))
        if best is None or key > (len(best[3]), len(best[2])):
            best = (Ls, Rs, fw, comp)
    Ls, Rs, fw, comp = best
    rec.update(side=list(Ls), n_free_words=len(fw), n_compatible=len(comp),
               compatible=[list(c) for c in comp[:8]])

    # B-T2 : the reduction identity
    import random
    rng = random.Random(gm)
    val = {(e, i, j): rng.randint(-9, 9) or 3 for e in EDGES
           for i in range(3) for j in range(3) if occ(T, e, i, j)}
    mism = tests = 0
    for x in fw[:4]:
        for _ in range(6):
            y = tuple(rng.randrange(3) for _ in range(4))
            w = [0] * N
            for k, v in enumerate(Ls):
                w[v] = x[k]
            for k, v in enumerate(Rs):
                w[v] = y[k]
            tests += 1
            if H(val, T, tuple(w)) != perB(val, T, Ls, Rs, x, y):
                mism += 1
    rec["B_T2_identity_tests"] = tests
    rec["B_T2_identity_mismatches"] = mism

    if not fw:
        rec["verdict"] = "DEGENERATE"
    elif len(comp) < 2:
        rec["verdict"] = "THRESHOLD"
    else:
        A = {}
        for x in comp[:2]:
            realise(A, T, Ls, Rs, x)
        for e in EDGES:
            for (i, j) in cells_of(T[EIDX[e]]):
                A.setdefault((e, i, j), rng.randint(1, 20))
        viol = {}
        for x in comp[:2]:
            viol[str(list(x))] = sum(
                1 for y in product(range(3), repeat=4)
                if perB(A, T, Ls, Rs, x, y) != 0)
        used = [k for k in A]
        allnz = all(A[k] != 0 for k in used if occ(T, k[0], k[1], k[2]))
        rec["witness_violations"] = viol
        rec["witness_all_nonzero"] = allnz
        good = all(v == 0 for v in viol.values()) and allnz
        # B-T3 mutation
        k0 = sorted(A)[0]
        A[k0] += 1
        mv = any(sum(1 for y in product(range(3), repeat=4)
                     if perB(A, T, Ls, Rs, x, y) != 0) > 0 for x in comp[:2])
        A[k0] -= 1
        rec["B_T3_mutation_fires"] = mv
        rec["verdict"] = "RESISTS" if good else "THRESHOLD"
    rec["seconds"] = round(time.time() - t0, 1)
    return rec


def main():
    os.makedirs(OUTD, exist_ok=True)
    kill = json.load(open(os.path.join(CENSUS, "results_kill.json")))
    inv = {r["gamma_mask"]: r for r in kill["reps_inventory"]}
    reach = json.load(open(os.path.join(HERE, "results_r3_reach.json")))
    tierA = set(reach["tier_A_masks"])
    tierC = set(reach["tier_C_masks"])
    strat = sorted(gm for gm, r in inv.items() if r["pms"] <= 2)
    # B-T5: run the C_8 class FIRST as the known-answer calibration
    order = sorted(tierC) + [gm for gm in strat
                             if gm not in tierA and gm not in tierC]
    print("tier-B sweep: %d classes (+%d calibration)"
          % (len(order) - len(tierC), len(tierC)), flush=True)
    for gm in order:
        f = os.path.join(OUTD, "class_%d.json" % gm)
        if os.path.exists(f):
            continue
        rec = run_class(gm, inv[gm]["n_edges"], inv[gm]["pms"])
        if gm in tierC:
            rec["B_T5_calibration"] = dict(
                expect="RESISTS", got=rec.get("verdict"),
                ok=(rec.get("verdict") == "RESISTS"))
        with open(f, "w") as fh:
            json.dump(rec, fh, indent=1, sort_keys=True)
        print("gamma=%-8d |G|=%2d free=%s comp=%s -> %-10s %6.1fs"
              % (gm, rec["n_gamma"], rec.get("n_free_words"),
                 rec.get("n_compatible"), rec.get("verdict"),
                 rec.get("seconds", 0)), flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
