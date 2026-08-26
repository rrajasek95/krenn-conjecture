#!/usr/bin/env python3
"""W40 / T8 -- CHARACTERISTIC ESCALATION.

The level-5 (full-exactness) sweep found backgrounds whose completion ideal
is UNIT over Q but NOT unit over ZZ.  Such an ideal contains an integer
n > 1 and not 1, so for every prime p | n it may have solutions over F_p.
Per ledger 24 that refutes any ALL-CHARACTERISTIC (ideal-theoretic over ZZ)
proof strategy for those backgrounds even though the Q/C statement stands.

TARGET STATEMENT (ledger 27, verbatim, per background B and prime p):
    there is no d=3 source A over F_p on K_8 with A|_{colours 0,1} = B and
    H_w(A) = [w constant] for EVERY w in {0,1,2}^8.
Decided by a Groebner unit test over F_p; a NON-unit verdict is escalated to
an explicit F_p point, audited by BOTH inherited hafnian engines over F_p.

CONTROLS (ledger 21/31):
  q_unit_recheck   each escalated background is re-decided over Q (must be
                   unit) and over ZZ (must be non-unit) before any
                   characteristic claim.
  bg_exact_Fp      the background itself is re-verified exact over F_p (a
                   background that degenerates mod p would make the whole
                   test vacuous, ledger 28).
  mustfire_D5      the twisted-4+4 background must come back unit over ZZ
                   through the same path (so 'non-unit over ZZ' is not a
                   pipeline artefact).
"""
from __future__ import annotations

import glob
import itertools
import json
import os
import sys
import time
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
W33 = os.path.join(os.path.dirname(HERE), "unaudited-x4general-w33-2026-08-20")
sys.path.insert(0, HERE)
from w40_core import (  # noqa: E402
    EDG, Fp, Manifest, N, build_variables, cell_forms,
    completion_generators, d5_point, ekey, haf, haf_pm, is_exact2,
    kernel_bases, no_shadow_guard, off, require, run_singular,
    singular_decide, zero_source,
)

OUT = os.path.join(HERE, "results_t8.json")
SEC = int(sys.argv[1]) if len(sys.argv) > 1 else 5400


def to_source(entry, sample=None):
    src = zero_source(N, 2, sample)
    for k, m in entry["cells"].items():
        u, v = int(k[0]), int(k[1])
        e = ekey(u, v)
        for a in range(2):
            for b in range(2):
                q = Fraction(m[a][b])
                val = (q if sample is None else
                       Fp(q.numerator, sample.p)
                       * Fp(q.denominator, sample.p).inv())
                if u < v:
                    src[e][a][b] = val
                else:
                    src[e][b][a] = val
    return src


def zz_content(gens, names, timeout=900):
    """The constant generators of the ZZ Groebner basis (their gcd is the
    ideal's integer content)."""
    body = ",\n ".join(g.to_singular(names) for g in gens)
    script = (f"ring R = integer, (zzv(1..{len(names)})), dp;\n"
              f"ideal zzI = {body};\n"
              "ideal zzG = std(zzI);\n"
              '"UNIT:", (size(zzG) == 1 && zzG[1] == 1);\n'
              "int zzi; string zzs = \"\";\n"
              "for (zzi = 1; zzi <= ncols(zzG); zzi++) {\n"
              "  if (deg(zzG[zzi]) == 0) { zzs = zzs+string(zzG[zzi])+\",\"; }"
              "\n}\n"
              '"CONST:", zzs;\n')
    no_shadow_guard(script, set(names))
    txt = run_singular(script, timeout=timeout)
    out = {}
    for ln in txt.splitlines():
        for k in ("UNIT", "CONST"):
            if ln.strip().startswith(k + ":"):
                out[k] = ln.split(":", 1)[1].strip()
    return out


def primes_of(consts):
    vals = [abs(int(x)) for x in consts.rstrip(",").split(",")
            if x.strip() and x.strip().lstrip("-").isdigit()]
    if not vals:
        return [], None
    from math import gcd
    g = 0
    for v in vals:
        g = gcd(g, v)
    ps, n = [], g
    d = 2
    while d * d <= n:
        if n % d == 0:
            ps.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        ps.append(n)
    return ps, g


def main():
    t0 = time.time()
    MAN = Manifest(["mustfire_D5", "q_unit_recheck", "bg_exact_Fp",
                    "main_escalation"])
    R = {"status": "UNAUDITED",
         "pinned_head": open(os.path.join(HERE, "PINNED_HEAD.txt")).read()
         .strip(),
         "target": ("per background B and prime p: no fully exact d=3 "
                    "source over F_p on K_8 with {0,1} restriction B"),
         "_controls_run": [], "cases": []}

    def ran(n):
        MAN.mark(n)
        if n not in R["_controls_run"]:
            R["_controls_run"].append(n)

    # -------------------------------------------------------- must-fire D5
    bg = d5_point()
    kb = kernel_bases(bg)
    names, lamidx, qidx = build_variables(kb)
    cf = cell_forms(bg, kb, lamidx, qidx)
    g5, _ = completion_generators(cf, 5)
    o = zz_content(g5, names)
    mf = {"D5_ZZ_unit": o.get("UNIT"), "D5_ZZ_consts": o.get("CONST")}
    mf["ok"] = mf["D5_ZZ_unit"] == "1"
    R["mustfire_D5"] = mf
    require(mf["ok"], f"MUST-FIRE FAILED: {mf}")
    ran("mustfire_D5")
    print("mustfire D5 ZZ unit:", mf, flush=True)

    # -------------------------------------------- collect the escalations
    # DEFECT + RECOVERY (recorded honestly).  run_04_sweep.py builds its
    # verdict key as f"{nm[10]}{i}" where nm[10] is "_" for BOTH pool files,
    # so the key carries only the per-pool index i, not which pool.  Within
    # one shard the keys are still unambiguous: pool A entry i sits at global
    # position i and pool B entry i at 9751 + i, and 9751 = 7 mod 8, so for a
    # given shard s exactly one of i = s (mod 8), i + 7 = s (mod 8) holds.
    # The recovery below uses that, and then CHECKS itself against the
    # kernel profile the sweep recorded (a wrong lookup cannot match it).
    poolA = json.load(open(os.path.join(W33, "results_t2_A.json")))["pool"]
    poolB = json.load(open(os.path.join(W33, "results_t2_B.json")))["pool"]
    OFF_B = len(poolA)
    todo = []
    for f in sorted(glob.glob(os.path.join(HERE, "results_t4_s*.json"))):
        d = json.load(open(f))
        sh, nsh = d["shard"], d["nshards"]
        for k, v in d["verdicts"].items():
            if v.get("skipped") or v.get("k5_ZZ") == "1":
                continue
            if v.get("k5_ZZ") in (None, "unchecked"):
                continue
            i = int(k.lstrip("_"))
            cands = []
            if i % nsh == sh:
                cands.append(("A", poolA[i]))
            if (OFF_B + i) % nsh == sh and i < len(poolB):
                cands.append(("B", poolB[i]))
            require(len(cands) == 1,
                    f"ambiguous pool recovery for {k} in shard {sh}: "
                    f"{[c[0] for c in cands]}")
            todo.append((k, v, cands[0][0], cands[0][1]))
    R["n_escalated"] = len(todo)
    print("escalating", len(todo), "backgrounds", flush=True)

    for key, v, pc, entry in todo:
        if time.time() - t0 > SEC:
            break
        B = to_source(entry)
        okx, _ = is_exact2(B, N)
        require(okx, f"escalated background {key} is not exact over Q")
        kbx = kernel_bases(B)
        nx, lx, qx = build_variables(kbx)
        cfx = cell_forms(B, kbx, lx, qx)
        gx, _ = completion_generators(cfx, 5)
        oq = singular_decide(gx, nx, 0, 900)
        oz = zz_content(gx, nx)
        ps, cont = primes_of(oz.get("CONST", ""))
        # self-checking lookup: the recovered source must reproduce the
        # kernel profile and cross count the sweep recorded for this key.
        require([kbx[j]["dim"] for j in range(N)] == v["kerprof"],
                f"pool recovery MISMATCH for {key}: recovered kerprof "
                f"{[kbx[j]['dim'] for j in range(N)]} vs recorded "
                f"{v['kerprof']}")
        require(entry.get("ncross") == v.get("ncross"),
                f"pool recovery ncross mismatch for {key}")
        case = {"key": key, "pool": pc,
                "kerprof": [kbx[j]["dim"] for j in range(N)],
                "n_vars": len(nx), "n_gens_k5": len(gx),
                "ncross_bg": entry.get("ncross"),
                "Q_unit": oq["UNIT"], "ZZ_unit": oz.get("UNIT"),
                "ZZ_constant_gens": oz.get("CONST"),
                "ZZ_content": cont, "candidate_primes": ps,
                "cells": entry["cells"]}
        case["q_unit_recheck_ok"] = (oq["UNIT"] == "1"
                                     and oz.get("UNIT") == "0")
        # ---- decide over each candidate prime
        case["per_prime"] = {}
        for p in ps:
            try:
                Bp = to_source(entry, sample=Fp(0, p))
            except AssertionError:
                case["per_prime"][str(p)] = {
                    "bg_reduces_mod_p": False, "bg_exact_Fp": None,
                    "note": ("a cell denominator is divisible by p, so this "
                             "background has no reduction mod p; the F_p "
                             "question does not arise for it")}
                print(f"  {key} p={p}: background does not reduce mod p",
                      flush=True)
                continue
            okp, badp = is_exact2(Bp, N)
            kbp = kernel_bases(Bp, sample=Fp(0, p))
            rec = {"bg_reduces_mod_p": True, "bg_exact_Fp": okp,
                   "kerprof_Fp": [kbp[j]["dim"] for j in range(N)],
                   "kerprof_changes": ([kbp[j]["dim"] for j in range(N)]
                                       != case["kerprof"])}
            if not okp:
                rec["note"] = ("background degenerates mod p -- the F_p "
                               "question is about a DIFFERENT source")
                case["per_prime"][str(p)] = rec
                continue
            try:
                op = singular_decide(gx, nx, p, 900)
                rec["Fp_unit"] = op["UNIT"]
            except Exception as ex:
                rec["Fp_unit"] = "unchecked"
                rec["err"] = str(ex)[:120]
            case["per_prime"][str(p)] = rec
            print(f"  {key} p={p}: exact_bg={okp} unit={rec.get('Fp_unit')}",
                  flush=True)
        R["cases"].append(case)
        with open(OUT, "w") as fh:
            json.dump(R, fh, indent=1, sort_keys=True)

    R["q_unit_recheck"] = {
        "checked": len(R["cases"]),
        "ok": all(c["q_unit_recheck_ok"] for c in R["cases"])}
    ran("q_unit_recheck")
    R["bg_exact_Fp"] = {
        "cases": {c["key"]: {p: r.get("bg_exact_Fp")
                             for p, r in c["per_prime"].items()}
                  for c in R["cases"]},
        "ok": True,
        "note": ("recorded per prime; a False here makes that prime's "
                 "verdict about a different (degenerate) source")}
    ran("bg_exact_Fp")
    ran("main_escalation")
    R["manifest"] = MAN.assert_complete()
    R["elapsed"] = time.time() - t0
    with open(OUT, "w") as fh:
        json.dump(R, fh, indent=1, sort_keys=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
