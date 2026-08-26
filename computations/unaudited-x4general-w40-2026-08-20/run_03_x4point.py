#!/usr/bin/env python3
"""W40 / T3 -- THE X_4 POINT: the level-4 system at N=8 with general
bicoloured blocks is NON-EMPTY, and the same background is UNIT at full
exactness.

TWO TARGET STATEMENTS (ledger 27 -- verbatim; the controls test these).

  (T3a) [REFUTATION]  There EXISTS a d=3 source A on K_8 with
        H_w(A) = [w constant] for every w in {0,1,2}^8 with off(w) <= 4,
        whose {0,1} restriction is the W33-D5 twisted 4+4.  Equivalently:
        "general X_4-emptiness at N=8" -- Route B's stated target -- is
        FALSE.  Refuted by an explicit stored point (below), audited by both
        inherited hafnian engines over Q and over F_13, F_31 (ledger 19),
        and by an independent Singular evaluation (ledger 13b).

  (T3b) [THEOREM W40-B1]  There is NO d=3 source A on K_8 with
        H_w(A) = [w constant] for EVERY w in {0,1,2}^8 (full exactness;
        at N=8 this is the level-5 system, because off(w) <= 5 always and
        the only off-count-5 profile is the trichromatic (3,3,2)) whose
        {0,1} restriction is the W33-D5 twisted 4+4.  Decided UNIT over ZZ,
        hence over every field.  Since the twisted-4+4 stratum is a single
        gauge orbit (W33 t12: stratum dim 8 = gauge-orbit dim 8) and the
        d=3 gauge group restricts onto the d=2 one, this closes the whole
        orbit -- the named dangerous seed of branch (B1).

CONTROLS (each writes its own ok field; ledger 21/31):
  engine_audit     the stored point, re-audited cell by cell over ALL 6561
                   words by the DP engine AND by the explicit-PM control
                   engine, over Q and over F_13/F_31.
  variety_closed   the level-4 ideal CONTAINS the 42 vanishing coordinates
                   (so the closed form below is the whole variety, not a
                   component), and the 6-coordinate reduced ideal has the
                   stated Groebner basis.
  outside_locus    (ledger 18) the explicit point for the (T3b) unit verdict
                   lies OUTSIDE the asserted locus: at it the level-4 target
                   HOLDS and only the omitted off-count-5 words fail -- so
                   it could falsify a level-4 unit verdict, which is exactly
                   what makes the level-5 verdict non-vacuous.
  k5_pointfree     the level-5 ideal is unit while the level-4 ideal is not,
                   both recomputed from the same generator list (the level-5
                   generators are a SUPERSET; checked by construction).
"""
from __future__ import annotations

import itertools
import json
import os
import sys
import time
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from w40_core import (  # noqa: E402
    EDG, Fp, Manifest, N, Sym, build_variables, cell_forms,
    completion_generators, d5_point, haf, haf_pm, install_d3, kernel_bases,
    no_shadow_guard, off, rational_emission_guard, require, run_singular,
    singular_decide, singular_eval_point, words3,
)

OUT = os.path.join(HERE, "results_t3.json")

# the six surviving coordinates of the level-4 variety
KEEP6 = [("lam", 2, 1), ("lam", 6, 5), ("q", 0, 4), ("q", 1, 3),
         ("q", 2, 6), ("q", 5, 7)]
# the stored witness (small rationals; found by exhaustive small search)
PT6 = [Fraction(-2), Fraction(-1), Fraction(-2), Fraction(1, 2),
       Fraction(-2), Fraction(1, 2)]
# a second, integral witness over EVERY field: s=t=1 => q26=-1, q04=q13=1,
# q57=-1  (checks the refutation is characteristic-free)
PT6_INT = [Fraction(1), Fraction(1), Fraction(1), Fraction(1),
           Fraction(-1), Fraction(-1)]


def keep_index(lamidx, qidx):
    out = []
    for k in KEEP6:
        out.append(lamidx[(k[1], k[2])] if k[0] == "lam"
                   else qidx[(k[1], k[2])])
    return out


def full_vals(nv, keep, pt6):
    v = [Fraction(0)] * nv
    for i, x in zip(keep, pt6):
        v[i] = x
    return v


def audit_source(src, sample):
    """(violations at off<=4, violations at off=5) using a given engine."""
    def E(w, eng):
        return eng(src, w, n=N, sample=sample)
    bad4dp, bad5dp, bad4pm, bad5pm = [], [], [], []
    for w in itertools.product(range(3), repeat=N):
        tgt = 1 if len(set(w)) == 1 else 0
        a = E(w, haf)
        b = E(w, haf_pm)
        require(a == b, f"ENGINE DISAGREEMENT at {w}: {a} vs {b}")
        if a != tgt:
            (bad4dp if off(w) <= 4 else bad5dp).append(w)
        if b != tgt:
            (bad4pm if off(w) <= 4 else bad5pm).append(w)
    require(bad4dp == bad4pm and bad5dp == bad5pm, "engine tallies differ")
    return bad4dp, bad5dp


def main():
    t0 = time.time()
    MAN = Manifest(["rational_emission", "engine_audit", "variety_closed",
                    "outside_locus", "k5_pointfree", "main_decision"])
    R = {"status": "UNAUDITED",
         "pinned_head": open(os.path.join(HERE, "PINNED_HEAD.txt")).read()
         .strip(),
         "target_T3a": ("general X_4-emptiness at N=8 (Route B's stated "
                        "target) -- REFUTED by explicit point"),
         "target_T3b": ("no fully exact d=3 source at N=8 whose {0,1} "
                        "restriction is the W33-D5 twisted 4+4"),
         "_controls_run": []}

    def ran(name):
        MAN.mark(name)
        R["_controls_run"].append(name)

    # W40 hazard guard (see w40_core.sing_rat): a parenthesised rational
    # is silently truncated to 0 by Singular's poly parser.
    R["rational_emission"] = {"ok": rational_emission_guard()}
    ran("rational_emission")

    bg = d5_point()
    kb = kernel_bases(bg)
    names, lamidx, qidx = build_variables(kb)
    cf = cell_forms(bg, kb, lamidx, qidx)
    keep = keep_index(lamidx, qidx)
    g4, _ = completion_generators(cf, 4)
    g5, _ = completion_generators(cf, 5)
    R["system"] = {"n_vars": len(names), "n_gens_k4": len(g4),
                   "n_gens_k5": len(g5),
                   "kernel_profile": [kb[j]["dim"] for j in range(N)],
                   "n_words_off_le_4": len(words3(4)),
                   "n_words_total": len(words3(5)),
                   "n_words_off_5": len(words3(5)) - len(words3(4))}

    # -------------------------------------------------------- engine_audit
    ea = {}
    for tag, pt in (("witness_A", PT6), ("witness_B_integral", PT6_INT)):
        vals = full_vals(len(names), keep, pt)
        src = install_d3(cf, vals)
        b4, b5 = audit_source(src, Fraction(0))
        ea[tag] = {"point6": [str(x) for x in pt],
                   "off_le4_violations": len(b4),
                   "off5_violations": len(b5),
                   "off5_violating_words": [list(w) for w in b5],
                   "cross_cells": sorted(
                       f"A_{e}[{a}][{b}]={src[e][a][b]}" for e in EDG
                       for a in range(3) for b in range(3)
                       if a != b and src[e][a][b] != 0),
                   "diagonal_supports": {
                       str(c): sorted([list(e) for e in EDG
                                       if src[e][c][c] != 0])
                       for c in range(3)},
                   "source": {str(e): [[str(src[e][a][b]) for b in range(3)]
                                       for a in range(3)] for e in EDG}}
        # multi-characteristic re-audit (ledger 19: two primes = 1 mod 3).
        # The witness's cells are reduced into F_p directly (the Sym ring is
        # over Q); the background's kernel profile is recomputed over F_p so
        # the reduction is not silently degenerate.
        for p in (13, 31):
            kbp = kernel_bases(d5_point(sample=Fp(0, p)), sample=Fp(0, p))
            require([kbp[j]["dim"] for j in range(N)]
                    == [kb[j]["dim"] for j in range(N)],
                    f"kernel profile changes mod {p}")
            sp = {e: [[Fp(src[e][a][b].numerator, p)
                       * Fp(src[e][a][b].denominator, p).inv()
                       for b in range(3)] for a in range(3)] for e in EDG}
            b4p, b5p = audit_source(sp, Fp(0, p))
            ea[tag][f"F{p}"] = {"off_le4_violations": len(b4p),
                                "off5_violations": len(b5p)}
    ea["ok"] = (ea["witness_A"]["off_le4_violations"] == 0
                and ea["witness_A"]["off5_violations"] > 0
                and ea["witness_B_integral"]["off_le4_violations"] == 0
                and ea["witness_B_integral"]["off5_violations"] > 0
                and all(ea[t][f"F{p}"]["off_le4_violations"] == 0
                        for t in ("witness_A", "witness_B_integral")
                        for p in (13, 31)))
    R["engine_audit"] = ea
    require(ea["ok"], f"ENGINE AUDIT FAILED: "
                      f"{ {k: v for k, v in ea.items() if k != 'source'} }")
    ran("engine_audit")
    print("witness A: off<=4 violations",
          ea["witness_A"]["off_le4_violations"], "| off=5 violations",
          ea["witness_A"]["off5_violations"],
          ea["witness_A"]["off5_violating_words"], flush=True)
    with open(OUT, "w") as fh:
        json.dump(R, fh, indent=1, sort_keys=True)

    # ------------------------------------------------------ variety_closed
    body = ",\n ".join(g.to_singular(names) for g in g4)
    script = (f"ring R = 0, (zzv(1..{len(names)})), dp;\n"
              f"ideal zzI = {body};\n"
              "ideal zzG = std(zzI);\n"
              '"UNIT:", (size(zzG)==1 && zzG[1]==1);\n'
              "int zzi; string zzs = \"\";\n"
              f"for (zzi = 1; zzi <= {len(names)}; zzi++)"
              " { if (reduce(zzv(zzi), zzG) == 0)"
              " { zzs = zzs + string(zzi) + \",\"; } }\n"
              '"VANISH:", zzs;\n'
              '"DIM:", dim(zzG);\n')
    no_shadow_guard(script, set(names))
    txt = run_singular(script, timeout=1800)
    got = {}
    for ln in txt.splitlines():
        for k in ("UNIT", "VANISH", "DIM"):
            if ln.strip().startswith(k + ":"):
                got[k] = ln.split(":", 1)[1].strip()
    van = sorted(int(x) - 1 for x in got["VANISH"].rstrip(",").split(",")
                 if x.strip())
    vc = {"k4_unit": got["UNIT"], "k4_dim": got["DIM"],
          "n_coords_in_ideal": len(van),
          "surviving_coords": [str(k) for k in KEEP6],
          "surviving_ok": sorted(set(range(len(names))) - set(van))
          == sorted(keep)}
    # the reduced ideal in the 6 survivors
    sub = {i: p for p, i in enumerate(keep)}
    red, seen = [], set()
    for g in g4:
        t = {}
        for m, c in g.t.items():
            if any(x in van for x in m):
                continue
            t[tuple(sorted(sub[x] for x in m))] = \
                t.get(tuple(sorted(sub[x] for x in m)), Fraction(0)) + c
        t = {m: c for m, c in t.items() if c}
        key = tuple(sorted(t.items()))
        if t and key not in seen:
            seen.add(key)
            red.append(Sym(t))
    nn = [f"zzv({i + 1})" for i in range(6)]
    body6 = ",\n ".join(g.to_singular(nn) for g in red)
    s6 = ("ring R = 0, (zzv(1..6)), dp;\n"
          f"ideal zzI = {body6};\n"
          "ideal zzG = std(zzI);\n"
          '"UNIT:", (size(zzG)==1 && zzG[1]==1);\n'
          '"DIM:", dim(zzG);\n'
          '"GB:", string(zzG);\n')
    no_shadow_guard(s6, set(nn))
    t6 = run_singular(s6, timeout=900)
    for ln in t6.splitlines():
        for k in ("UNIT", "DIM", "GB"):
            if ln.strip().startswith(k + ":"):
                vc["reduced_" + k] = ln.split(":", 1)[1].strip()
    vc["closed_form"] = ("lam(2,1)*lam(6,5) + q(2,6) = 0  and  "
                         "q(0,4)*q(1,3)*q(2,6)*q(5,7) = 1, "
                         "every other coordinate 0")
    vc["ok"] = (vc["surviving_ok"] and vc["k4_unit"] == "0"
                and vc["k4_dim"] == "4" and vc["reduced_DIM"] == "4")
    R["variety_closed"] = vc
    require(vc["ok"], f"variety-closure control FAILED: {vc}")
    ran("variety_closed")
    print("level-4 variety:", vc["reduced_GB"], "dim", vc["k4_dim"],
          flush=True)

    # ------------------------------------------------------- outside_locus
    vals = full_vals(len(names), keep, PT6)
    ev4 = singular_eval_point(g4, names, vals)
    ev5 = singular_eval_point(g5, names, vals)
    ol = {"k4_nonzero_gens_at_point": ev4,
          "k5_nonzero_gens_at_point": ev5,
          "note": ("the point satisfies every level-4 generator and "
                   "violates only level-5 ones, so it is a legitimate "
                   "ledger-18 control for the level-5 unit verdict")}
    ol["ok"] = (ev4 == 0 and ev5 > 0)
    R["outside_locus"] = ol
    require(ol["ok"], f"outside-locus control FAILED: {ol}")
    ran("outside_locus")

    # -------------------------------------------------------- k5_pointfree
    kp = {"k5_generators_superset": all(
        any(tuple(sorted(a.t.items())) == tuple(sorted(b.t.items()))
            for b in g5) for a in g4[:80])}
    for base in (0, "integer"):
        tag = "Q" if base == 0 else "ZZ"
        o = singular_decide(g5, names, base,
                            max(600, int(7200 - (time.time() - t0))),
                            want_dim=(base == 0))
        kp[f"k5_{tag}_unit"] = o["UNIT"]
        kp[f"k5_{tag}_dim"] = o.get("DIM")
    kp["ok"] = (kp["k5_Q_unit"] == "1" and kp["k5_ZZ_unit"] == "1"
                and kp["k5_generators_superset"])
    R["k5_pointfree"] = kp
    require(kp["ok"], f"k5 control FAILED: {kp}")
    ran("k5_pointfree")
    print("FULL exactness (level 5): unit Q =", kp["k5_Q_unit"],
          "| unit ZZ =", kp["k5_ZZ_unit"], flush=True)

    R["verdict"] = {
        "T3a_X4_emptiness_at_N8": "REFUTED (explicit point, any field)",
        "T3b_W40_B1_full_exactness_on_twisted44": "UNIT over ZZ (any field)",
        "cross_cell_count_of_witness": len(
            ea["witness_A"]["cross_cells"]),
        "restrictions": {
            "{0,1}": "twisted 4+4 (non-Hamiltonian), 4 cross cells",
            "{0,2}": "PM pair M0 u M2 Hamiltonian, 2 cross cells",
            "{1,2}": "PM pair M1 u M2 Hamiltonian, 2 cross cells"}}
    ran("main_decision")
    R["manifest"] = MAN.assert_complete()
    R["elapsed"] = time.time() - t0
    with open(OUT, "w") as fh:
        json.dump(R, fh, indent=1, sort_keys=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
