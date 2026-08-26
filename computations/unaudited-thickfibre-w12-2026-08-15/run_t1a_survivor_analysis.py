#!/usr/bin/env python3
"""UNAUDITED PROBE (W12) -- TASK 1(a): anatomy of the m=20 CEGAR survivor."""

from __future__ import annotations

import json
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w12_core as C          # noqa: E402
import w12_lattice as LAT     # noqa: E402
from run_t4_calibration import load_survivor  # noqa: E402


def main():
    geo = C.geometry()
    T = load_survivor()
    sysv = C.ValueSystem(geo, T)
    out = {"nvars": sysv.nvars,
           "vars": [sysv.varname(n) for n in range(sysv.nvars)]}
    print(f"variables: {sysv.nvars}")
    print(f"mixed live words: {len(sysv.mixed_eqs)}")
    sizes = Counter(len(v) for v in sysv.mixed_eqs.values())
    print(f"mixed fibre sizes: {dict(sorted(sizes.items()))}")
    out["mixed_live"] = len(sysv.mixed_eqs)
    out["mixed_sizes"] = {int(k): v for k, v in sorted(sizes.items())}
    for w, monos in sysv.const_eqs.items():
        print(f"constant {w[0]}: fibre size {len(monos)}")
    out["const_sizes"] = {str(w[0]): len(v) for w, v in sysv.const_eqs.items()}

    # which variables occur at all?
    occurring = set()
    for monos in list(sysv.mixed_eqs.values()) + list(sysv.const_eqs.values()):
        for mono in monos:
            occurring.update(mono)
    dead = [sysv.varname(n) for n in range(sysv.nvars) if n not in occurring]
    print(f"variables occurring in NO live equation: {len(dead)} -> {dead}")
    out["vars_in_no_equation"] = dead

    only_const = set()
    mixedvars = set()
    for monos in sysv.mixed_eqs.values():
        for mono in monos:
            mixedvars.update(mono)
    out["vars_in_mixed_equations"] = len(mixedvars)
    print(f"variables occurring in some MIXED equation: {len(mixedvars)}")

    # lattices
    diff = LAT.difference_lattice(sysv)
    out["difference_lattice_rows"] = len(diff)
    out["difference_lattice_rank"] = LAT.rank_z(diff)
    gauge = LAT.gauge_matrix(sysv)
    out["gauge_rank"] = LAT.rank_q(gauge)
    bino = LAT.binomial_lattice(sysv)
    out["binomial_rows"] = len(bino)
    out["binomial_rank"] = LAT.rank_z(bino)
    out["binomial_consistency"] = LAT.binomial_consistency(sysv)
    print(f"difference lattice: {len(diff)} rows, rank "
          f"{out['difference_lattice_rank']}")
    print(f"gauge rank r(T) = {out['gauge_rank']}  "
          f"(so gauge-invariant dimension = {sysv.nvars - out['gauge_rank']})")
    print(f"binomial sublattice: {len(bino)} rows, rank "
          f"{out['binomial_rank']}, consistency "
          f"{out['binomial_consistency']}")

    # per-equation listing (small ones)
    listing = []
    for w, monos in sorted(sysv.mixed_eqs.items()):
        listing.append({"word": "".join(map(str, w)), "size": len(monos),
                        "monomials": [[sysv.varname(v) for v in mono]
                                      for mono in monos]})
    out["mixed_equations"] = listing
    out["const_equations"] = {
        str(w[0]): [[sysv.varname(v) for v in mono] for mono in monos]
        for w, monos in sysv.const_eqs.items()}

    with open(os.path.join(HERE, "results_t1a_survivor.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print("wrote results_t1a_survivor.json")

    # show the two-term equations, they are the binomial relations
    print("\nfirst 6 two-term equations:")
    for row in listing:
        if row["size"] == 2:
            print("  ", row["word"], row["monomials"])
    print("\nthree-term equations (first 8):")
    k = 0
    for row in listing:
        if row["size"] == 3:
            print("  ", row["word"], row["monomials"])
            k += 1
            if k == 8:
                break


if __name__ == "__main__":
    main()
