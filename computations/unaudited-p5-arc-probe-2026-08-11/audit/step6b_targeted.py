#!/usr/bin/env python3
"""Targeted (non-inert) mutation tests.

step6 showed that many single-coefficient perturbations are invisible below
order 9 simply because the mutated monomial's series contribution starts
later.  These mutations are constructed so that they cannot be inert.
"""
from fractions import Fraction as QQ
import time

from myarc import Arc, collapse, load_base
from setup import Point, committed_values


def main():
    t0 = time.time()
    data = load_base()
    p = Point(data, committed_values(data))
    order = 10
    tau = data["tau"]
    dynamic = set(data["local_variables"]) | {p.a[46]}
    bends = p.recurrence_bends(order)

    def run(normal_rows, transverse_rows, obstruction_rows):
        arc = Arc(data, p.point, order)
        arc.set_bends(bends)
        return [arc.step(m, normal_rows, transverse_rows, obstruction_rows)
                for m in range(1, order + 1)]

    normal = [collapse(r, p.point, dynamic) for r in data["normal"]]
    transverse = [collapse(r, p.point, dynamic) for r in data["transverse"]]
    obstruction = [collapse(r, p.point, dynamic)
                   for r in list(data["obstruction"]) + list(data["pure"])]
    clean = run(normal, transverse, obstruction)
    print("clean: Q10^M30 =", clean[9][29], " Q10^M33 =", clean[9][32])

    print("\n(a) scale the committed M30 obstruction row by 2")
    mutated = list(obstruction)
    mutated[29] = {k: 2 * v for k, v in obstruction[29].items()}
    out = run(normal, transverse, mutated)
    print("    Q10^M30 =", out[9][29],
          " doubled =", out[9][29] == 2 * clean[9][29],
          " other rows unchanged =", all(
              out[m][i] == clean[m][i]
              for m in range(order) for i in range(41) if i != 29))

    print("\n(b) add tau^7 to the committed M30 obstruction row")
    mutated = list(obstruction)
    row = dict(obstruction[29])
    key = tuple([tau] * 7)
    row[key] = row.get(key, QQ(0)) + QQ(1)
    mutated[29] = row
    out = run(normal, transverse, mutated)
    print("    Q7^M30 =", out[6][29], "(clean", clean[6][29], ")")
    assert out[6][29] == clean[6][29] + 1

    print("\n(c) add tau^3 to committed normal row 0 (propagates through the "
          "whole graph)")
    mutated = list(normal)
    row = dict(normal[0])
    key = (tau, tau, tau)
    row[key] = row.get(key, QQ(0)) + QQ(1)
    mutated[0] = row
    out = run(mutated, transverse, obstruction)
    profile = [[i + 1 for i, x in enumerate(v) if x] for v in out]
    print("    nonzero rows per order:", profile)
    assert any(profile[:9]), "normal-row mutation stayed invisible"

    print("\n(d) add tau^3 to committed transverse row 0")
    mutated = list(transverse)
    row = dict(transverse[0])
    row[key] = row.get(key, QQ(0)) + QQ(1)
    mutated[0] = row
    out = run(normal, mutated, obstruction)
    profile = [[i + 1 for i, x in enumerate(v) if x] for v in out]
    print("    nonzero rows per order:", profile)
    assert any(profile[:9]), "transverse-row mutation stayed invisible"

    print("\n(e) why some single-coefficient mutations were inert: minimal "
          "contributing order of the monomials step6 picked")
    for group, table in (("normal", data["normal"]),
                         ("obstruction", data["obstruction"])):
        for index in ((0, 100) if group == "normal" else (29,)):
            src = table[index]
            keys = sorted(src)
            for which in (0, 1, 7, 33, 101, 555):
                monomial = keys[which % len(keys)]
                dyn = [w for w in monomial if w in dynamic]
                base = [w for w in monomial if w not in dynamic]
                base_value = 1
                for w in base:
                    base_value *= p.point[w]
                # minimal tau-order: tau counts 1, z46 counts 0, y/n count >=1
                minimal = 0
                for w in dyn:
                    if w == tau:
                        minimal += 1
                    elif w == p.a[46]:
                        minimal += 0
                    else:
                        minimal += 1
                print(f"    {group}[{index}] #{which}: dyn-degree "
                      f"{len(dyn)}, min order >= {minimal}, "
                      f"base factor {'0' if base_value == 0 else 'nonzero'}")
    print(f"\ntotal {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
