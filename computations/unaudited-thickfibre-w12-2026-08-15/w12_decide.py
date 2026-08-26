#!/usr/bin/env python3
"""UNAUDITED PROBE (W12) -- the full exact decision pipeline for a template.

    template  ->  ValueSystem  ->  ReducedSystem (lossless torus reduction)
              ->  binomial sublattice solved by Smith normal form
              ->  Laurent system in f free variables  ->  Singular over Q.

VERDICTS
  'support-dead'   some constant word has an EMPTY fibre (no exact source can
                   have this template; committed (T4)).
  'killed-mixed'   the MIXED system alone has no solution with all cells
                   nonzero  ->  no exact source, a fortiori.
  'killed-const'   the mixed system is solvable but never with all three
                   constant fibre sums nonzero  ->  no exact source.
  'feasible'       a point of the exact locus exists over C (Nullstellensatz);
                   ESCALATE.
  'undecided'      Singular did not finish / a nontrivial elementary divisor
                   forced a case split that was not taken.
"""

from __future__ import annotations

from fractions import Fraction
import random

import w12_core as C
import w12_reduce as RED
import w12_torus as TOR


def decide(template, geo=None, timeout=1800, characteristic=0,
           want_scripts=False, mixed_only=False):
    """`mixed_only=True` skips the support/constant conditions entirely and
    asks only whether the MIXED system is solvable with all cells nonzero.
    That is the mode the negative control needs."""
    geo = geo or C.geometry()
    out = {"m": C.support(template), "sigma": C.sigma(template)}
    fib = C.all_fibres(geo, template)
    missing = [w[0] for w in geo.constant_words if w not in fib]
    if missing and not mixed_only:
        out["verdict"] = "support-dead"
        out["empty_constant_fibres"] = missing
        return out
    sing = [w for w, ms in fib.items() if geo.is_mixed(w) and len(ms) == 1]
    if sing:
        out["verdict"] = "killed-mixed"
        out["reason"] = "mixed singleton fibre"
        out["singleton_example"] = "".join(map(str, sing[0]))
        return out
    sysv = C.ValueSystem(geo, template)
    red = RED.ReducedSystem(sysv)
    out["reduced"] = red.summary()
    phi = RED.MonomialValues(red.d)
    for vec, val in red.binomial_rows():
        if phi.learn(vec, val) == "contradiction":
            out["verdict"] = "killed-mixed"
            out["reason"] = "binomial lattice inconsistent"
            out["contradiction"] = [str(x) for x in phi.contradiction]
            return out
    sol = TOR.TorusSolution(red.d, phi.rows, phi.vals)
    out["torus"] = sol.summary()
    if any(x != 1 for x in sol.divisors):
        out["verdict"] = "undecided"
        out["reason"] = "nontrivial elementary divisor"
        return out
    if sol.free == 0:
        # every coordinate is pinned to an exact rational: evaluate directly
        bad = []
        for w, terms in TOR.laurent_forms(red, sol, "mixed"):
            if sum(c for c, _ in terms) != 0:
                bad.append("".join(map(str, w)))
        if bad:
            out["verdict"] = "killed-mixed"
            out["reason"] = "pinned point violates a mixed equation"
            out["violated_example"] = bad[0]
            out["violated_count"] = len(bad)
            return out
        if mixed_only:
            out["verdict"] = "mixed-feasible"
            return out
        zeros = [str(w[0]) for w, terms in TOR.laurent_forms(red, sol, "const")
                 if sum(c for c, _ in terms) == 0]
        if zeros:
            out["verdict"] = "killed-const"
            out["reason"] = "pinned point forces a constant fibre sum to zero"
            out["zero_constants"] = zeros
            return out
        out["verdict"] = "feasible"
        out["reason"] = "fully pinned point satisfies everything"
        return out
    names = [f"w{k}" for k in range(sol.free)]
    mixed = TOR.laurent_forms(red, sol, "mixed")
    const = TOR.laurent_forms(red, sol, "const")
    gens = [TOR.singular_polynomial(t, names)[0] for _, t in mixed]
    cpolys = [TOR.singular_polynomial(t, names)[0] for _, t in const]
    prod = "*".join(names)
    script_m = "\n".join([
        f'ring RM={characteristic},({",".join(names)},t),dp;',
        "ideal I=" + ",".join(gens) + ";",
        f"ideal J=I,t*({prod})-1;",
        "ideal G=std(J);",
        '"ONEM "+string(reduce(1,G)==0);'])
    prod_c = prod + "*" + "*".join(f"({p})" for p in cpolys)
    script_f = "\n".join([
        f'ring RF={characteristic},({",".join(names)},t),dp;',
        "ideal I=" + ",".join(gens) + ";",
        f"ideal J=I,t*({prod_c})-1;",
        "ideal G=std(J);",
        '"ONEF "+string(reduce(1,G)==0);'])
    if want_scripts:
        out["script_mixed"] = script_m
        out["script_full"] = script_f
    try:
        rm = C.run_singular(script_m, timeout=timeout)
    except Exception as exc:                              # noqa: BLE001
        out["verdict"] = "undecided"
        out["reason"] = f"singular(mixed): {type(exc).__name__}"
        return out
    one_m = "ONEM 1" in rm
    out["mixed_unit_ideal"] = one_m
    if one_m:
        out["verdict"] = "killed-mixed"
        out["reason"] = "mixed system infeasible on the torus"
        return out
    if mixed_only:
        out["verdict"] = "mixed-feasible"
        return out
    try:
        rf = C.run_singular(script_f, timeout=timeout)
    except Exception as exc:                              # noqa: BLE001
        out["verdict"] = "undecided"
        out["reason"] = f"singular(full): {type(exc).__name__}"
        return out
    one_f = "ONEF 1" in rf
    out["full_unit_ideal"] = one_f
    out["verdict"] = "killed-const" if one_f else "feasible"
    return out


# ------------------------------------------------------------- controls


def roundtrip_control(template, geo=None, trials=2, seed=11):
    """CONTROL C1.  The torus reduction must reproduce every fibre sum.

    For random nonzero rational cell values x, check
        F_w(x)  ==  x^{a_1} * (1 + sum_k z^{c_k})
    for every live word, with z^{c} evaluated through the reduced basis."""
    geo = geo or C.geometry()
    rng = random.Random(seed)
    sysv = C.ValueSystem(geo, template)
    red = RED.ReducedSystem(sysv)
    bad = 0
    checked = 0
    for _ in range(trials):
        vals = [Fraction(rng.randint(1, 40), rng.randint(1, 12))
                * (1 if rng.random() < 0.5 else -1)
                for _ in range(sysv.nvars)]
        for src, rsrc in ((sysv.mixed_eqs, red.mixed),
                          (sysv.const_eqs, red.const)):
            for w, monos in src.items():
                direct = sysv.evaluate(vals, w)
                lead = Fraction(1)
                for v in monos[0]:
                    lead *= vals[v]
                total = Fraction(1)
                for row in rsrc[w]:
                    total += red.character(vals, row)
                checked += 1
                if direct != lead * total:
                    bad += 1
    return {"checked": checked, "mismatches": bad}


def smith_control(template, geo=None, seed=5, trials=2):
    """CONTROL C2.  The Smith substitution must satisfy the binomial system.

    Sample free w-coordinates at random, reconstruct z = w^{V^T}, and verify
    every binomial relation z^{c_i} = eps_i holds exactly."""
    geo = geo or C.geometry()
    sysv = C.ValueSystem(geo, template)
    red = RED.ReducedSystem(sysv)
    phi = RED.MonomialValues(red.d)
    for vec, val in red.binomial_rows():
        phi.learn(vec, val)
    if not phi.rows:
        return {"skipped": "no binomial relations"}
    sol = TOR.TorusSolution(red.d, phi.rows, phi.vals)
    if any(x != 1 for x in sol.divisors):
        return {"skipped": "nontrivial divisors"}
    rng = random.Random(seed)
    bad = 0
    checked = 0
    for _ in range(trials):
        w = [Fraction(1)] * sol.rank + \
            [Fraction(rng.randint(1, 30), rng.randint(1, 7))
             for _ in range(sol.free)]
        for j in range(sol.rank):
            w[j] = sol.eps[j]
        # z_j = prod_k w_k^{V[j][k]}
        z = []
        for j in range(sol.d):
            v = Fraction(1)
            for k in range(sol.d):
                e = sol.V[j][k]
                if e:
                    v *= w[k] ** e
            z.append(v)
        for row, val in zip(phi.rows, phi.vals):
            got = Fraction(1)
            for j, e in enumerate(row):
                if e:
                    got *= z[j] ** e
            checked += 1
            if got != val:
                bad += 1
    return {"checked": checked, "mismatches": bad}
