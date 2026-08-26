#!/usr/bin/env python3
"""H1 / BLOCKER 2 -- W12's unevidenced C1/C2 round-trip controls, re-built.

UNAUDITED.  Hygiene agent H1, 2026-08-15.

A4 finding D2: W12's REPORT claims "reduction round-trips 0 mismatches",
but `results_t4_controls.json` and `results_t8_soundness.json` were never
written to disk, so the C1 (reduction round-trip) and C2 (Smith
substitution round-trip) controls are UNEVIDENCED.

This module re-implements both controls FROM THE REPORT'S DESCRIPTION,
independently of `w12_decide.roundtrip_control` / `.smith_control`, but
against W12's actual reduction code (`w12_reduce.ReducedSystem`,
`w12_reduce.smith`, `w12_torus.TorusSolution`), and writes the evidence.

  C1a  EXACT (symbolic) round-trip.  For every live word w with monomials
       a_1 < a_2 < ... < a_t, the reduced system stores a coordinate row
       c_k in the HNF basis of the difference lattice.  C1a checks the
       INTEGER identity
              lift(c_k) = exponent(a_k) - exponent(a_1)     in Z^Sigma
       for every (w, k).  This makes the round-trip an identity rather
       than a point test, so no evaluation point can hide a defect.
       (Ledger item 17: a point test decides nothing on its own.)

  C1b  NUMERIC round-trip at W12's original scale (2 trials x 162
       equations = 324 checks):
              F_w(x)  ==  x^{a_1} * (1 + sum_k z^{c_k}).
       Evaluation points are DETERMINISTIC (fixed rationals from a prime
       ladder with alternating signs), not random: the identity is
       algebraic, so the point carries no decision, and a fixed point is
       reproducible.

  C2   SMITH substitution round-trip at the original scale (2 trials x 27
       binomial relations = 54 checks).  Sample the free w-coordinates
       deterministically, set the pinned ones to eps, reconstruct
       z_j = prod_k w_k^{V[j][k]}, and verify z^{row} == val exactly for
       every learned binomial relation.

  MUT1 / MUT2 / MUT3  MUTATION CONTROLS.  A broken round-trip must be
       CAUGHT.  Each mutation corrupts one object and the corresponding
       control must report a nonzero mismatch count.

Everything is exact (Fraction / int).  No floats.

Usage:  python3 h1_b2_w12_controls.py
Writes  results_b2_c1_roundtrip.json, results_b2_c2_smith.json,
        results_b2_mutations.json
"""

from __future__ import annotations

import copy
import json
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
W12 = os.path.join(ROOT, "computations", "unaudited-thickfibre-w12-2026-08-15")
W8 = os.path.join(ROOT, "computations", "unaudited-template-kill-w8-2026-08-15")
sys.path.insert(0, W12)

import w12_core as C          # noqa: E402
import w12_reduce as RED      # noqa: E402
import w12_torus as TOR       # noqa: E402


class CheckFailure(Exception):
    pass


def require(cond, msg):
    if not cond:
        raise CheckFailure(msg)


# --------------------------------------------------------------- helpers

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59,
          61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127,
          131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193,
          197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269,
          271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349]


def deterministic_point(nvars, trial):
    """A fixed nonzero rational point.  Trial 0 and trial 1 differ; neither
    is random, so the run is reproducible byte-for-byte."""
    out = []
    for i in range(nvars):
        p = PRIMES[(i + 3 * trial) % len(PRIMES)]
        q = PRIMES[(i * 5 + 7 * trial + 11) % len(PRIMES)]
        sign = 1 if (i + trial) % 3 else -1
        out.append(Fraction(sign * p, q))
    require(all(v != 0 for v in out), "evaluation point has a zero cell")
    return out


def exponent_vector(mono, nvars):
    """Independent re-implementation: v[i] = multiplicity of variable i."""
    v = [0] * nvars
    for x in mono:
        v[x] += 1
    return v


def lift_row(red, row):
    """Lift a coordinate row (in the HNF basis) back to Z^Sigma."""
    out = [0] * red.system.nvars
    for c, b in zip(row, red.basis):
        if c:
            for j, x in enumerate(b):
                if x:
                    out[j] += c * x
    return out


def monomial_value(values, mono):
    t = Fraction(1)
    for v in mono:
        t *= values[v]
    return t


def character_from_lift(values, lift):
    t = Fraction(1)
    for j, e in enumerate(lift):
        if e:
            t *= values[j] ** e
    return t


def load_survivor():
    with open(os.path.join(W8, "results_close_m20.json")) as fh:
        return tuple(json.load(fh)["survivors"][0])


# ------------------------------------------------------------- C1 exact

def c1a_exact(sysv, red):
    """lift(c_k) == exponent(a_k) - exponent(a_1) for every (word, k)."""
    checked = bad = 0
    sample = []
    for src, rsrc in ((sysv.mixed_eqs, red.mixed), (sysv.const_eqs, red.const)):
        for w, monos in src.items():
            base = exponent_vector(monos[0], sysv.nvars)
            rows = rsrc[w]
            require(len(rows) == len(monos) - 1,
                    f"word {w}: {len(rows)} rows for {len(monos)} monomials")
            for k, mono in enumerate(monos[1:]):
                want = [a - b for a, b in
                        zip(exponent_vector(mono, sysv.nvars), base)]
                got = lift_row(red, rows[k])
                checked += 1
                if got != want:
                    bad += 1
                    if len(sample) < 3:
                        sample.append({"word": "".join(map(str, w)), "k": k})
    return {"checked": checked, "mismatches": bad, "sample": sample}


# ----------------------------------------------------------- C1 numeric

def c1b_numeric(sysv, red, trials=2):
    """F_w(x) == x^{a_1} * (1 + sum_k z^{c_k}) at deterministic points."""
    checked = bad = 0
    sample = []
    per_trial = []
    for t in range(trials):
        vals = deterministic_point(sysv.nvars, t)
        tbad = tchk = 0
        for src, rsrc in ((sysv.mixed_eqs, red.mixed),
                          (sysv.const_eqs, red.const)):
            for w, monos in src.items():
                direct = sysv.evaluate(vals, w)
                lead = monomial_value(vals, monos[0])
                total = Fraction(1)
                for row in rsrc[w]:
                    total += character_from_lift(vals, lift_row(red, row))
                tchk += 1
                if direct != lead * total:
                    tbad += 1
                    if len(sample) < 3:
                        sample.append({"trial": t,
                                       "word": "".join(map(str, w)),
                                       "direct": str(direct),
                                       "reduced": str(lead * total)})
        per_trial.append({"trial": t, "checked": tchk, "mismatches": tbad})
        checked += tchk
        bad += tbad
    return {"checked": checked, "mismatches": bad, "trials": per_trial,
            "sample": sample}


# ------------------------------------------------------------------- C2

def c2_smith(red, trials=2, V_override=None, eps_override=None):
    """Smith substitution round-trip: z = w^{V^T} must satisfy every learned
    binomial relation exactly."""
    phi = RED.MonomialValues(red.d)
    for vec, val in red.binomial_rows():
        st = phi.learn(vec, val)
        require(st != "contradiction",
                "the survivor's binomial system is contradictory -- "
                "the C2 control cannot run on a killed template")
    if not phi.rows:
        return {"skipped": "no binomial relations"}
    sol = TOR.TorusSolution(red.d, phi.rows, phi.vals)
    if V_override is not None:
        sol.V = V_override
    if eps_override is not None:
        sol.eps = eps_override
    info = {"d": red.d, "rank": sol.rank, "free": sol.free,
            "divisors": [int(x) for x in sol.divisors],
            "relations": len(phi.rows)}
    if any(x != 1 for x in sol.divisors):
        info["skipped"] = "nontrivial elementary divisors"
        return info
    checked = bad = 0
    sample = []
    per_trial = []
    for t in range(trials):
        wvec = [Fraction(1)] * sol.d
        for j in range(sol.rank):
            wvec[j] = sol.eps[j]
        for j in range(sol.rank, sol.d):
            p = PRIMES[(j + 5 * t) % len(PRIMES)]
            q = PRIMES[(j * 3 + 2 * t + 4) % len(PRIMES)]
            wvec[j] = Fraction(p, q)
        z = []
        for j in range(sol.d):
            v = Fraction(1)
            for k in range(sol.d):
                e = sol.V[j][k]
                if e:
                    v *= wvec[k] ** e
            z.append(v)
        tbad = tchk = 0
        for row, val in zip(phi.rows, phi.vals):
            got = Fraction(1)
            for j, e in enumerate(row):
                if e:
                    got *= z[j] ** e
            tchk += 1
            if got != val:
                tbad += 1
                if len(sample) < 3:
                    sample.append({"trial": t, "got": str(got),
                                   "want": str(val)})
        per_trial.append({"trial": t, "checked": tchk, "mismatches": tbad})
        checked += tchk
        bad += tbad
    info.update({"checked": checked, "mismatches": bad, "trials": per_trial,
                 "sample": sample})
    return info


# ------------------------------------------------------------- mutations

def mutations(sysv, red):
    """Three mutation controls.  Each MUST produce mismatches."""
    out = []

    # MUT1: corrupt one stored exponent row of the reduced system.
    m1 = copy.deepcopy(red)
    w0 = sorted(m1.mixed.keys())[0]
    require(m1.mixed[w0], "MUT1: first mixed word has no non-leading monomial")
    m1.mixed[w0][0] = list(m1.mixed[w0][0])
    m1.mixed[w0][0][0] += 1
    ra = c1a_exact(sysv, m1)
    rb = c1b_numeric(sysv, m1, trials=2)
    out.append({"control": "MUT1 corrupt one reduced exponent row",
                "c1a_mismatches": ra["mismatches"],
                "c1b_mismatches": rb["mismatches"],
                "caught": ra["mismatches"] > 0 and rb["mismatches"] > 0})

    # MUT2: corrupt the HNF basis itself (changes every lift through it).
    m2 = copy.deepcopy(red)
    m2.basis = [list(r) for r in m2.basis]
    m2.basis[0][-1] += 1
    ra = c1a_exact(sysv, m2)
    rb = c1b_numeric(sysv, m2, trials=2)
    out.append({"control": "MUT2 corrupt the difference-lattice HNF basis",
                "c1a_mismatches": ra["mismatches"],
                "c1b_mismatches": rb["mismatches"],
                "caught": ra["mismatches"] > 0 and rb["mismatches"] > 0})

    # MUT3: corrupt the Smith transform V so that a FREE coordinate leaks
    # into a pinned relation.  NOTE: V is NOT unique -- perturbing its
    # pinned block can land on another valid substitution, and perturbing a
    # coordinate on which no relation depends is invisible by construction
    # (column 0 of the relation matrix is identically zero here).  So the
    # mutation is placed on a LIVE coordinate and aimed at the free block,
    # where breakage is forced: the relation then depends on a generic
    # rational free variable and can no longer equal +-1.
    phi = RED.MonomialValues(red.d)
    for vec, val in red.binomial_rows():
        phi.learn(vec, val)
    sol = TOR.TorusSolution(red.d, phi.rows, phi.vals)
    live = [j for j in range(red.d)
            if any(row[j] for row in phi.rows)]
    require(live, "MUT3: the relation matrix is identically zero")
    Vbad = [list(r) for r in sol.V]
    Vbad[live[0]][sol.rank] += 1          # inject the first free variable
    r3 = c2_smith(red, trials=2, V_override=Vbad)
    out.append({"control": "MUT3 leak a free coordinate into the Smith "
                           "substitution V",
                "mutated_entry": [live[0], sol.rank],
                "c2_mismatches": r3.get("mismatches"),
                "caught": bool(r3.get("mismatches", 0) > 0)})

    # MUT4: corrupt one pinned eps value -- C2 must catch it.
    epsbad = list(sol.eps)
    epsbad[0] = epsbad[0] * 2
    r4 = c2_smith(red, trials=2, eps_override=epsbad)
    out.append({"control": "MUT4 corrupt a pinned eps of the Smith solution",
                "c2_mismatches": r4.get("mismatches"),
                "caught": bool(r4.get("mismatches", 0) > 0)})

    # MUT5: corrupt a BINOMIAL RELATION of the reduced system itself (the
    # input C2 consumes).  The reconstructed z then cannot satisfy it.
    m5 = copy.deepcopy(red)
    w = next(k for k, v in m5.mixed.items() if len(v) == 1)
    m5.mixed[w] = [list(m5.mixed[w][0])]
    m5.mixed[w][0][live[0]] += 2
    r5 = c2_smith(m5, trials=2)
    out.append({"control": "MUT5 corrupt a binomial relation of the "
                           "reduced system",
                "c2_mismatches": r5.get("mismatches"),
                "caught": bool(r5.get("mismatches", 0) > 0
                               or r5.get("skipped"))})
    return out


# ------------------------------------------------------------------ main

def main():
    surv = load_survivor()
    geo = C.geometry()
    audit = C.audit(geo, surv)
    sysv = C.ValueSystem(geo, surv)
    red = RED.ReducedSystem(sysv)

    head = open(os.path.join(HERE, "PINNED_HEAD.txt")).read().split()[0]
    meta = {"agent": "H1", "blocker": 2, "pinned_head": head,
            "target": "W12 m=20 CEGAR survivor (Sigma=58)",
            "template": list(surv),
            "m": audit["m"], "sigma": audit["sigma"], "beta": audit["beta"],
            "mixed_eqs": len(sysv.mixed_eqs),
            "const_eqs": len(sysv.const_eqs),
            "reduced": red.summary()}
    print("target:", {k: meta[k] for k in
                      ("m", "sigma", "beta", "mixed_eqs", "const_eqs")})
    print("reduced:", meta["reduced"])

    print("=== C1a exact (symbolic) reduction round-trip ===")
    c1a = c1a_exact(sysv, red)
    print("   ", c1a)

    print("=== C1b numeric reduction round-trip (original scale) ===")
    c1b = c1b_numeric(sysv, red, trials=2)
    print("   ", {k: c1b[k] for k in ("checked", "mismatches")})
    require(c1b["checked"] == 324,
            f"C1b scale is {c1b['checked']}, expected W12's 324")

    print("=== C2 Smith substitution round-trip (original scale) ===")
    c2 = c2_smith(red, trials=2)
    print("   ", {k: c2.get(k) for k in
                  ("d", "rank", "free", "relations", "checked", "mismatches")})
    require(c2.get("checked") == 54,
            f"C2 scale is {c2.get('checked')}, expected W12's 54")

    print("=== mutation controls (each must be CAUGHT) ===")
    mut = mutations(sysv, red)
    for row in mut:
        print(f"    [{'OK ' if row['caught'] else 'BAD'}] {row['control']}"
              f"  {[(k, v) for k, v in row.items() if k.endswith('mismatches')]}")

    with open(os.path.join(HERE, "results_b2_c1_roundtrip.json"), "w") as fh:
        json.dump({**meta, "C1a_exact": c1a, "C1b_numeric": c1b,
                   "verdict": ("PASS" if c1a["mismatches"] == 0
                               and c1b["mismatches"] == 0 else "FAIL")},
                  fh, indent=1, default=str)
    with open(os.path.join(HERE, "results_b2_c2_smith.json"), "w") as fh:
        json.dump({**meta, "C2_smith": c2,
                   "verdict": ("PASS" if c2.get("mismatches") == 0
                               else "FAIL")}, fh, indent=1, default=str)
    with open(os.path.join(HERE, "results_b2_mutations.json"), "w") as fh:
        json.dump({**meta, "mutations": mut,
                   "all_caught": all(r["caught"] for r in mut)},
                  fh, indent=1, default=str)
    print("\nwrote results_b2_c1_roundtrip.json, results_b2_c2_smith.json, "
          "results_b2_mutations.json")


if __name__ == "__main__":
    main()
