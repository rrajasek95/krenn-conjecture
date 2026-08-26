#!/usr/bin/env python3
"""UNAUDITED PROBE (W12) -- decide an extracted half-system (see w12_cut)."""

from __future__ import annotations

import w12_core as C
import w12_cut as CUT
import w12_reduce as RED
import w12_torus as TOR


def decide_half(hs, stats, timeout=600, characteristic=0):
    """Verdict for one extracted half-system."""
    out = dict(stats)
    if stats["immediate_contradiction"]:
        out["verdict"] = "killed"
        out["reason"] = "a pinned sub-word is forced to vanish"
        return out
    singles = [w for w, m in hs.mixed_eqs.items() if len(m) == 1]
    if singles:
        out["verdict"] = "killed"
        out["reason"] = "single-monomial equation forced to vanish"
        out["example"] = "".join(map(str, singles[0]))
        return out
    if not hs.mixed_eqs:
        out["verdict"] = "no-content"
        return out
    if not hs.const_eqs:
        out["verdict"] = "no-nonvanishing-anchor"
        return out
    red = RED.ReducedSystem(hs)
    out["d"] = red.d
    phi = RED.MonomialValues(red.d)
    for vec, val in red.binomial_rows():
        if phi.learn(vec, val) == "contradiction":
            out["verdict"] = "killed"
            out["reason"] = "binomial lattice inconsistent"
            out["contradiction"] = [str(x) for x in phi.contradiction]
            return out
    sol = TOR.TorusSolution(red.d, phi.rows, phi.vals)
    out["binomial_rank"] = sol.rank
    out["free"] = sol.free
    if any(x != 1 for x in sol.divisors):
        out["verdict"] = "undecided"
        out["reason"] = "nontrivial elementary divisor"
        return out
    if sol.free == 0:
        bad = [w for w, terms in TOR.laurent_forms(red, sol, "mixed")
               if sum(c for c, _ in terms) != 0]
        if bad:
            out["verdict"] = "killed"
            out["reason"] = "pinned point violates an extracted equation"
            out["example"] = "".join(map(str, bad[0]))
            return out
        zeros = [w for w, terms in TOR.laurent_forms(red, sol, "const")
                 if sum(c for c, _ in terms) == 0]
        if zeros:
            out["verdict"] = "killed"
            out["reason"] = "pinned point kills a required non-vanishing"
            out["example"] = "".join(map(str, zeros[0]))
            return out
        out["verdict"] = "feasible"
        return out
    if timeout <= 0:
        out["verdict"] = "needs-groebner"
        return out
    names = [f"u{k}" for k in range(sol.free)]
    gens = [TOR.singular_polynomial(t, names)[0]
            for _, t in TOR.laurent_forms(red, sol, "mixed")]
    cpolys = [TOR.singular_polynomial(t, names)[0]
              for _, t in TOR.laurent_forms(red, sol, "const")]
    prod = "*".join(names) + "*" + "*".join(f"({p})" for p in cpolys)
    script = "\n".join([
        f'ring RH={characteristic},({",".join(names)},t),dp;',
        "ideal I=" + ",".join(gens) + ";",
        f"ideal J=I,t*({prod})-1;",
        "ideal G=std(J);",
        '"ONEH "+string(reduce(1,G)==0);'])
    try:
        res = C.run_singular(script, timeout=timeout)
    except Exception as exc:                              # noqa: BLE001
        out["verdict"] = "undecided"
        out["reason"] = f"singular: {type(exc).__name__}"
        return out
    if "ONEH 1" in res:
        out["verdict"] = "killed"
        out["reason"] = "extracted half-system infeasible (Groebner)"
    else:
        out["verdict"] = "feasible"
    return out


def cut_kill(geo, template, timeout=60, want_all=False, max_cuts=None,
             cheap_only=False):
    """Search all even cuts for a kill.

    Two staged passes: first every cut with the CHEAP tests only (no
    Groebner), then -- if nothing fired -- the Groebner test, smallest half
    first.  Returns (verdict, records)."""
    cuts = CUT.even_cuts(geo.size)
    if max_cuts:
        cuts = cuts[:max_cuts]
    halves = []
    for (L, R) in cuts:
        for tag, (hs, stats) in CUT.extract(geo, template, L, R).items():
            if not stats["forced_zero_words"] and not \
                    stats["immediate_contradiction"]:
                continue
            halves.append((sorted(L), sorted(R), tag, hs, stats))
    records = []
    for L, R, tag, hs, stats in halves:
        v = decide_half(hs, stats, timeout=0)      # timeout 0 => cheap only
        v.update({"cut_L": L, "cut_R": R, "side": tag})
        records.append(v)
        if v["verdict"] == "killed" and not want_all:
            return "killed", records
    if cheap_only:
        verdicts = {r["verdict"] for r in records}
        return ("killed" if "killed" in verdicts else "no-kill"), records
    order = sorted(range(len(halves)), key=lambda n: len(halves[n][3].sites))
    for n in order:
        if records[n]["verdict"] != "needs-groebner":
            continue
        L, R, tag, hs, stats = halves[n]
        v = decide_half(hs, stats, timeout=timeout)
        v.update({"cut_L": L, "cut_R": R, "side": tag})
        records[n] = v
        if v["verdict"] == "killed" and not want_all:
            return "killed", records
    verdicts = {r["verdict"] for r in records}
    return ("killed" if "killed" in verdicts else "no-kill"), records
