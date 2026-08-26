#!/usr/bin/env python3
"""A12 STEP 0 -- engine calibration.  UNAUDITED.

Before any W36 claim is touched, this establishes that the A12 engine is a
faithful, independent implementation of the COMMITTED spine:

  E0_structure  -- Gamma edges/degrees/perfect-matching counts and the live
                   singles rebuilt from the masks, matched against the
                   committed census in proofs/slice-master-relations.md
                   (Remark 3.2: m=25 degrees (4,4,4,3,3,3,2,3), m=28 all 4;
                   m=27 has 12 Gamma perfect matchings)
  E1_phi        -- Phi by RAW 105-matching enumeration vs the decomposition
                   (1), at RANDOM (non-clean) blocks, three fields
  E2_cofactor   -- the cofactor identity (C) Phi(w|v=t) = <S'(tau)_t, Q(w)>
                   at RANDOM blocks, every site, every letter
  E3_master     -- the master relations (M)/(M*) at RANDOM blocks
  E4_mutation   -- MUT-A: one perturbed cell must break (C) and (M) against
                   the unperturbed Phi; MUT-B: a shuffled cofactor vector
                   must break (C)
  E5_rowsBC     -- at m=25/R6 the hand-derived closed forms
                   B = hafL*r45 + l03*d1*d2, C = hafL*r47 + l23*d0*d1 must
                   equal the 6-vertex cofactor hafnians (RANDOM blocks)
"""
from __future__ import annotations

import json
import os
import random
import sys
import time
from itertools import product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import a12_lib as A  # noqa: E402

DECL = ["E0_structure", "E1_phi", "E2_cofactor", "E3_master", "E4_mutation",
        "E5_rowsBC"]
HDR = "UNAUDITED A12 (independent audit of lane W36 round 2)"


class Manifest:
    def __init__(self, decl):
        self.decl = list(decl)
        self.out = {"_header": HDR, "_controls_declared": list(decl),
                    "_controls_run": []}

    def record(self, name, rec):
        if name not in self.decl:
            raise ValueError("undeclared control %s" % name)
        rec = dict(rec)
        rec["executed"] = True
        self.out[name] = rec
        self.out["_controls_run"].append(name)

    def finish(self, path, extra=None):
        self.out.update(extra or {})
        missing = [c for c in self.decl if c not in self.out["_controls_run"]]
        self.out["_manifest_ok"] = (missing == [])
        for k, v in self.out.items():
            if isinstance(v, dict) and "ok" in v and not v.get("executed"):
                raise ValueError("ok without executed: %s" % k)
        self.out["done"] = True
        json.dump(self.out, open(path, "w"), indent=1, default=str)
        if missing:
            raise SystemExit("CONTROL MANIFEST FAILURE %s" % missing)
        return self.out


def rnd_blocks(tm, K, rng, nonzero=True):
    lo = 1 if nonzero else 0
    hi = (K.p - 1) if K.p else 40
    return {e: [[K.of(rng.randint(lo, hi)) for _ in range(3)]
                for _ in range(3)] for e in sorted(tm.gamma)}


def main():
    t0 = time.time()
    man = Manifest(DECL)
    rng = random.Random(20260821)
    fields = [A.Rat, A.Fp(13), A.Fp(31)]

    # ------------------------------------------------------ E0 structure
    st = {}
    for m in (25, 26, 27, 28):
        tm = A.T(m)
        st["m%d" % m] = dict(
            n_gamma=len(tm.gamma), degrees=list(tm.deg),
            n_gamma_pms=len(tm.gamma_pms),
            n_singles=len(tm.singles), n_live=len(tm.live),
            live=[list(e) for e in tm.live],
            n_clean_words=len(tm.clean_words),
            nbr={str(v): list(tm.nbr[v]) for v in range(8)})
    ok0 = (st["m25"]["degrees"] == [4, 4, 4, 3, 3, 3, 2, 3]
           and st["m28"]["degrees"] == [4] * 8
           and st["m27"]["n_gamma_pms"] == 12
           and A.T(25).nbr[6] == (5, 7))
    man.record("E0_structure", dict(
        per_support=st, ok=ok0,
        note="matched against the committed census (Remark 3.2 degrees; "
             "m=27 Gamma perfect matchings = 12, the value the committed "
             "checker's step 1 caught)"))
    print("E0:", json.dumps({k: (v["degrees"], v["n_gamma_pms"], v["n_live"],
                                 v["n_clean_words"])
                             for k, v in st.items()}), flush=True)

    # ---------------------------------------------------------- E1 phi
    n1 = b1 = 0
    for m in (25, 26, 27, 28):
        tm = A.T(m)
        for K in fields:
            for _ in range(3):
                bl = rnd_blocks(tm, K, rng, nonzero=False)
                for w in [tuple(rng.randrange(3) for _ in range(8))
                          for _ in range(6)]:
                    n1 += 1
                    if not K.iszero(A.norm(K, tm.phi_raw(bl, w, K)
                                           - tm.phi_decomp(bl, w, K))):
                        b1 += 1
    man.record("E1_phi", dict(tests=n1, mismatches=b1, ok=(b1 == 0),
                              note="RANDOM, non-clean blocks: an identity, "
                                   "not a property of the solution locus"))
    print("E1: phi two routes %d tests %d mismatches" % (n1, b1), flush=True)

    # ------------------------------------------------------- E2 cofactor
    n2 = b2 = 0
    for m in (25, 26, 27, 28):
        tm = A.T(m)
        for K in fields:
            bl = rnd_blocks(tm, K, rng, nonzero=False)
            for v in range(8):
                for _ in range(2):
                    w = tuple(rng.randrange(3) for _ in range(8))
                    Q = tm.cofactorQ(bl, v, w, K)
                    S = tm.Sprime(bl, v, tm.tau_of(v, w), K)
                    for t in range(3):
                        ww = tuple(w[:v] + (t,) + w[v + 1:])
                        lhs = tm.phi_raw(bl, ww, K)
                        rhs = A.norm(K, sum(A.norm(K, S[t][j] * Q[j])
                                            for j in range(len(Q))))
                        n2 += 1
                        b2 += (not K.iszero(A.norm(K, lhs - rhs)))
    man.record("E2_cofactor", dict(tests=n2, violations=b2, ok=(b2 == 0),
                                   note="(C) at RANDOM blocks, all four "
                                        "supports, all eight sites"))
    print("E2: cofactor identity %d tests %d violations" % (n2, b2),
          flush=True)

    # --------------------------------------------------------- E3 master
    n3 = b3 = 0
    for m in (25, 26, 27, 28):
        tm = A.T(m)
        for K in fields:
            bl = rnd_blocks(tm, K, rng, nonzero=False)
            for (kind, v) in [('R', 4), ('R', 5), ('R', 6), ('R', 7),
                              ('L', 0), ('L', 1), ('L', 2), ('L', 3)]:
                w = tuple(rng.randrange(3) for _ in range(8))
                lhs, rhs = tm.master_lhs_rhs(bl, kind, v, w, K)
                for a, b in zip(lhs, rhs):
                    n3 += 1
                    b3 += (not K.iszero(A.norm(K, a - b)))
    man.record("E3_master", dict(tests=n3, violations=b3, ok=(b3 == 0),
                                 note="(M)/(M*) at RANDOM blocks"))
    print("E3: master relations %d tests %d violations" % (n3, b3), flush=True)

    # ------------------------------------------------------- E4 mutation
    fired_a = fired_b = tot_a = tot_b = 0
    for m in (25, 28):
        tm = A.T(m)
        for K in fields:
            for _ in range(4):
                bl = rnd_blocks(tm, K, rng)
                w = tuple(rng.randrange(3) for _ in range(8))
                v = rng.randrange(8)
                Q = tm.cofactorQ(bl, v, w, K)
                base = [tm.phi_raw(bl, tuple(w[:v] + (t,) + w[v + 1:]), K)
                        for t in range(3)]
                # MUT-A: perturb the cell this word actually reads, on an
                # edge NOT incident to v (so Q moves and S' does not)
                cand = [e for e in sorted(tm.gamma) if v not in e]
                e = cand[rng.randrange(len(cand))]
                i, j = w[e[0]], w[e[1]]
                old = bl[e][i][j]
                bl[e][i][j] = A.norm(K, old + K.one)
                S2 = tm.Sprime(bl, v, tm.tau_of(v, w), K)
                Q2 = tm.cofactorQ(bl, v, w, K)
                tot_a += 1
                if any(not K.iszero(A.norm(
                        K, base[t] - sum(A.norm(K, S2[t][jj] * Q2[jj])
                                         for jj in range(len(Q2)))))
                       for t in range(3)):
                    fired_a += 1
                bl[e][i][j] = old
                # MUT-B: shuffle the cofactor vector
                if len(Q) > 1:
                    Qs = Q[1:] + Q[:1]
                    S = tm.Sprime(bl, v, tm.tau_of(v, w), K)
                    tot_b += 1
                    if any(not K.iszero(A.norm(
                            K, base[t] - sum(A.norm(K, S[t][jj] * Qs[jj])
                                             for jj in range(len(Qs)))))
                           for t in range(3)):
                        fired_b += 1
    man.record("E4_mutation", dict(
        MUT_A_fired=fired_a, MUT_A_tests=tot_a,
        MUT_B_fired=fired_b, MUT_B_tests=tot_b,
        ok=(fired_a == tot_a and fired_b >= tot_b - 1),
        note="a one-cell perturbation and a rotated cofactor vector must "
             "both break (C); a checker that cannot fail proves nothing"))
    print("E4: MUT-A %d/%d  MUT-B %d/%d" % (fired_a, tot_a, fired_b, tot_b),
          flush=True)

    # ---------------------------------------------------------- E5 B, C
    tm = A.T(25)
    n5 = b5 = 0
    for K in fields:
        for _ in range(4):
            bl = rnd_blocks(tm, K, rng, nonzero=False)
            for _ in range(8):
                w = tuple(rng.randrange(3) for _ in range(8))
                x, y = w[:4], w[4:]
                c = tm.cell
                hl = tm.hafL(bl, x, K)
                Bcl = A.norm(K, hl * c(bl, 4, 5, y[0], y[1], K)
                             + c(bl, 0, 3, x[0], x[3], K)
                             * c(bl, 1, 4, x[1], y[0], K)
                             * c(bl, 2, 5, x[2], y[1], K))
                Ccl = A.norm(K, hl * c(bl, 4, 7, y[0], y[3], K)
                             + c(bl, 2, 3, x[2], x[3], K)
                             * c(bl, 0, 7, x[0], y[3], K)
                             * c(bl, 1, 4, x[1], y[0], K))
                Bh = tm.haf_on(bl, [0, 1, 2, 3, 4, 5], w, K)
                Ch = tm.haf_on(bl, [0, 1, 2, 3, 4, 7], w, K)
                n5 += 1
                if not (K.iszero(A.norm(K, Bcl - Bh))
                        and K.iszero(A.norm(K, Ccl - Ch))):
                    b5 += 1
    man.record("E5_rowsBC", dict(
        tests=n5, mismatches=b5, ok=(b5 == 0),
        note="the closed forms of the two m=25/R6 cofactors, hand-derived "
             "here from the sigma-count decomposition, at RANDOM blocks"))
    print("E5: B/C closed form %d tests %d mismatches" % (n5, b5), flush=True)

    man.finish(os.path.join(HERE, "results_t0.json"),
               extra={"elapsed_s": round(time.time() - t0, 1)})
    print("T0 DONE in %.1fs" % (time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
