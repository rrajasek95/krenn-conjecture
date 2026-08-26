#!/usr/bin/env python3
"""Claims (B) and (C): does the three-step bend recurrence kill Q7..Q9 and
leave Q10 nonzero?  Run at the committed point and at a THIRD generic-L
point chosen by this audit (not the prototype's z0=1,z30=35,z52=9).
"""
from fractions import Fraction as QQ
import argparse
import random
import time

from myarc import load_base
from setup import Point, committed_values


def report(tag, p, order):
    print(f"\n================ {tag} ================")
    print("z0,z30,z52 =", p.z(0), p.z(30), p.z(52))
    print("localized units:",
          {k: str(v) for k, v in p.units.items()})
    for name, value in p.units.items():
        assert value != 0, f"unit {name} vanishes at this point"
    print("z46,s,t,r3 =", p.z(46), p.s, p.t, p.r3)
    print("e =", p.e1, p.e2, p.e3)
    rows = p.rows()
    bends = p.recurrence_bends(order)
    print("recurrence bends r4..:", [str(x) for x in bends[4:]])
    out = p.run(bends, order, rows)
    first_bad = None
    for m in range(1, order + 1):
        nonzero = [i + 1 for i, x in enumerate(out[m - 1]) if x]
        label = {40: "H0", 41: "H1"}
        print(f"  order {m:2d}: nonzero rows = "
              f"{[label.get(i, i) for i in nonzero]}")
        if nonzero and first_bad is None:
            first_bad = m
    print(f"first order with a nonzero compatibility row: {first_bad}")
    if first_bad is not None:
        row30 = out[first_bad - 1][29]
        row33 = out[first_bad - 1][32]
        print(f"  Q_{first_bad}^M30 = {row30}")
        print(f"  Q_{first_bad}^M33 = {row33}")
        if row33:
            print(f"  ratio M30/M33 = {QQ(row30, 1)/row33}"
                  f"   u/v = {QQ(p.u, p.v)}"
                  f"   equal={QQ(row30,1)/row33 == QQ(p.u, p.v)}")
    return out, first_bad


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, default=10)
    parser.add_argument("--seed", type=int, default=811)
    args = parser.parse_args()
    t0 = time.time()
    data = load_base()

    committed = Point(data, committed_values(data))
    report("COMMITTED POINT z_p = p+2", committed, args.order)
    print(f"[{time.time()-t0:.1f}s]")

    rng = random.Random(args.seed)
    while True:
        values = {p: QQ(rng.randint(-30, 30) or 5) for p in data["layout_a"]}
        try:
            third = Point(data, values)
        except AssertionError as error:
            print("rejected candidate point:", error)
            continue
        if all(v for v in third.units.values()) and \
                len({third.z(0), third.z(30), third.z(52)}) == 3 and \
                (third.z(0), third.z(30), third.z(52)) != (1, 35, 9):
            break
    report(f"THIRD AUDIT POINT (seed {args.seed})", third, args.order)
    print(f"[{time.time()-t0:.1f}s] done")


if __name__ == "__main__":
    main()
