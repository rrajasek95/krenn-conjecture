"""W37 / A3 -- THE DEGENERATION PROFILE OF THE BLOCKAGE (UNAUDITED).

A witness needs FOUR nonvanishing conditions at once:
    s = <K,A_pq> != 0,   kappa_0 != 0,  kappa_1 != 0,  kappa_2 != 0.
"BLOCKED" only says the conjunction is unreachable.  A3 decides, for
every live pair of an object, the whole lattice of sub-conditions:

    for every subset S of {s, k00, k11, k22}, is V(E) intersect
    {every form in S nonzero} nonempty?

The MAXIMAL reachable subsets say exactly WHICH nondegeneracy the cap
system destroys -- the precise 'Gamma-degeneration' the descent hits.
Also runs the same lattice on the AS-IF-EXACT system (all defects zeroed).
"""
from __future__ import annotations

import json
import os
import sys
import time
from fractions import Fraction
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "unaudited-x3core-w25-2026-08-15"))

import w37_core as C
import w37_decide as D
from run_a1_falsifier import sym_cap_system_cleaned

OUT = os.path.join(HERE, "results_a3_degeneration.json")
RES = {"lane": "W37", "task": "A3 degeneration profile", "unaudited": True}
RAN, DECLARED = [], ["control_positive", "F8_true", "F8_asifexact"]
FORMS = ["s", "k00", "k11", "k22"]


def decide_with(src, p, q, sites, Z, keep, char=0, timeout=300):
    """keep: subset of FORMS required nonzero."""
    polys, s = sym_cap_system_cleaned(src, p, q, sites, Z)
    polys = D.clear_denoms(polys)
    sden = 1
    for c in s.values():
        fr = Fraction(c)
        sden = sden * fr.denominator // D._gcd(sden, fr.denominator)
    sint = {e: int(Fraction(c) * sden) for e, c in s.items()}
    gens = [D._poly_txt(f) for _, f in polys if f]
    prod = []
    for f in keep:
        if f == "s":
            gens_s = D._poly_txt(sint)
            prod.append("(" + gens_s + ")")
        else:
            prod.append({"k00": D.KV[0], "k11": D.KV[4],
                         "k22": D.KV[8]}[f])
    if prod:
        gens.append("zzt*" + "*".join(prod) + "-1")
    if not gens:
        gens = ["0"]            # E vanishes identically: every cap works
    ringvars = D.KV + ["zzt"]
    script = "\n".join([
        f"ring zzR = {char},({','.join(ringvars)}),dp;",
        "ideal zzI = " + ",\n  ".join(gens) + ";",
        "ideal zzG = std(zzI);",
        'if (dim(zzG) == -1) { "V:EMPTY"; } else { "V:NONEMPTY"; }',
    ])
    D.no_shadow_guard(script, set(ringvars))
    out, st = D.run_singular(script, timeout)
    if st == "TIMEOUT":
        return "UNCHECKED"
    return "EMPTY" if "V:EMPTY" in out else "NONEMPTY"


def profile(src, p, q, Z, n=8):
    U = tuple(x for x in range(n) if x not in (p, q))
    res = {}
    for r in range(len(FORMS) + 1):
        for S in combinations(FORMS, r):
            res["|".join(S) if S else "-"] = decide_with(src, p, q, U, Z,
                                                         list(S))
    maximal = []
    keys = [k for k, v in res.items() if v == "NONEMPTY"]
    for k in keys:
        ks = set(k.split("|")) - {"-"}
        if not any(ks < (set(o.split("|")) - {"-"}) for o in keys):
            maximal.append(k)
    return res, sorted(maximal)


def main():
    t0 = time.time()
    import w25_core as W25
    print("=== A3.0 positive control (Delta^3_8, has witnesses) ===",
          flush=True)
    d3 = {k: [[Fraction(x) for x in r] for r in v]
          for k, v in W25.delta3_N(8).items()}
    r, m = profile(d3, 0, 1, [])
    print("   Delta^3_8 (0,1) full conjunction:",
          r.get("s|k00|k11|k22"), " maximal:", m, flush=True)
    assert r.get("s|k00|k11|k22") == "NONEMPTY", "control failed"
    RES["control_positive"] = {"pair": [0, 1], "lattice": r, "maximal": m}
    RAN.append("control_positive"); C.ckpt(OUT, RES)

    f8 = C.parse_source(json.load(open(os.path.join(
        HERE, "..", "unaudited-x3core-w25-2026-08-15",
        "OBJECT_W25-F8_n8_allblocked_X3.json")))["blocks"], 8)
    _, bad = C.defects(f8, 8)
    allZ = sorted(bad)
    live = [(p, q) for p, q in combinations(range(8), 2)
            if C.is_live(f8, p, q)]

    for tag, Z in (("F8_true", []), ("F8_asifexact", allZ)):
        print(f"\n=== A3 {tag} ===", flush=True)
        rows = []
        for (p, q) in live:
            r, m = profile(f8, p, q, Z)
            rows.append({"pair": [p, q], "maximal": m,
                         "full": r["s|k00|k11|k22"], "lattice": r})
            print(f"   {p},{q}: maximal reachable {m}", flush=True)
            RES[tag] = rows
            C.ckpt(OUT, RES)
        RAN.append(tag)

    RES["seconds"] = round(time.time() - t0, 1)
    RES["manifest"] = {"declared": DECLARED, "ran": RAN,
                       "missing": [x for x in DECLARED if x not in RAN]}
    C.ckpt(OUT, RES)
    print("\nMANIFEST", RES["manifest"])


if __name__ == "__main__":
    main()
