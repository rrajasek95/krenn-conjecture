#!/usr/bin/env python3
"""UNAUDITED PROBE (W12) -- TASK 1(b)/(c): decide the m=20 survivor exactly.

Pipeline (every step exact):
  ValueSystem  ->  ReducedSystem (torus of dim d, lossless)
               ->  binomial sublattice solved by Smith normal form
               ->  Laurent system in f = d - rank free variables
               ->  Singular: Rabinowitsch decision over Q.

A Groebner basis equal to <1> is a KILL certificate for the template.
"""

from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w12_core as C          # noqa: E402
import w12_reduce as RED      # noqa: E402
import w12_torus as TOR       # noqa: E402
from run_t4_calibration import load_survivor  # noqa: E402


def build(geo, template):
    sysv = C.ValueSystem(geo, template)
    red = RED.ReducedSystem(sysv)
    phi = RED.MonomialValues(red.d)
    for vec, val in red.binomial_rows():
        st = phi.learn(vec, val)
        if st == "contradiction":
            return sysv, red, None, None, "binomial-contradiction"
    sol = TOR.TorusSolution(red.d, phi.rows, phi.vals)
    return sysv, red, phi, sol, "ok"


def singular_script(red, sol, saturate_constants=True, characteristic=0):
    names = [f"w{k}" for k in range(sol.free)]
    mixed = TOR.laurent_forms(red, sol, "mixed")
    const = TOR.laurent_forms(red, sol, "const")
    gens = []
    for w, terms in mixed:
        poly, _ = TOR.singular_polynomial(terms, names)
        gens.append(poly)
    cpolys = []
    for w, terms in const:
        poly, _ = TOR.singular_polynomial(terms, names)
        cpolys.append(poly)
    allnames = names + ["t"]
    prod = "*".join(names)
    if saturate_constants:
        prod += "*" + "*".join(f"({p})" for p in cpolys)
    lines = [f'ring RR={characteristic},({",".join(allnames)}),dp;',
             "ideal I=" + ",".join(gens) + ";",
             f"ideal J=I,t*({prod})-1;",
             "ideal G=std(J);",
             '"DIMJ "+string(dim(G));',
             '"ONEJ "+string(reduce(1,G)==0);',
             # also the mixed-only question (no constant saturation)
             ]
    return "\n".join(lines), names, len(gens)


def singular_mixed_only(red, sol, characteristic=0):
    names = [f"w{k}" for k in range(sol.free)]
    mixed = TOR.laurent_forms(red, sol, "mixed")
    gens = [TOR.singular_polynomial(terms, names)[0] for _, terms in mixed]
    prod = "*".join(names)
    lines = [f'ring RM={characteristic},({",".join(names)},t),dp;',
             "ideal I=" + ",".join(gens) + ";",
             f"ideal J=I,t*({prod})-1;",
             "ideal G=std(J);",
             '"DIMM "+string(dim(G));',
             '"ONEM "+string(reduce(1,G)==0);']
    return "\n".join(lines)


def main():
    geo = C.geometry()
    T = load_survivor()
    sysv, red, phi, sol, status = build(geo, T)
    out = {"status": status, "reduced": red.summary()}
    print("reduced:", red.summary())
    if sol is None:
        print("KILLED by binomial inconsistency")
        json.dump(out, open(os.path.join(HERE, "results_t1c.json"), "w"),
                  indent=1)
        return
    print("torus:", sol.summary())
    out["torus"] = sol.summary()

    script_m = singular_mixed_only(red, sol)
    with open(os.path.join(HERE, "survivor_mixed_only.sing"), "w") as fh:
        fh.write(script_m + "\nquit;\n")
    print("\n--- Singular: MIXED-ONLY feasibility on the torus ---")
    res_m = C.run_singular(script_m, timeout=3600)
    print(res_m.strip())
    out["mixed_only"] = res_m.strip()

    script_f, names, ng = singular_script(red, sol)
    with open(os.path.join(HERE, "survivor_full.sing"), "w") as fh:
        fh.write(script_f + "\nquit;\n")
    print(f"\n--- Singular: FULL decision ({ng} generators, "
          f"{sol.free} free variables) ---")
    res_f = C.run_singular(script_f, timeout=3600)
    print(res_f.strip())
    out["full"] = res_f.strip()

    json.dump(out, open(os.path.join(HERE, "results_t1c.json"), "w"), indent=1)
    print("wrote results_t1c.json")


if __name__ == "__main__":
    main()
