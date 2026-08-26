#!/usr/bin/env python3
"""Claim (E): the TRUE arc.  Solve the newest bend from the M30 row at each
order and check that all 38 other mixed rows and both pure rows H0, H1
vanish for free.

Independent of the prototype: the newest bend is obtained by exact affine
interpolation from three samples (which VERIFIES affineness rather than
assuming it), the graph state is carried incrementally, and the monicity
slope is checked against C*u at every order rather than asserted once.
"""
from fractions import Fraction as QQ
import argparse
import copy
import random
import time

from myarc import Arc, load_base, affine_fit
from setup import Point, committed_values


def run_point(p, tag, max_bend):
    print(f"\n================ {tag} ================")
    print("z0,z30,z52 =", p.z(0), p.z(30), p.z(52),
          " C*u =", p.C * p.u, " units:",
          {k: str(v) for k, v in p.units.items()})
    order = max_bend + 3
    normal, transverse, targets = p.rows()
    arc = Arc(p.data, p.point, order)
    bends = [p.z(46), p.s, p.t, p.r3] + [QQ(0)] * (order - 3)
    arc.set_bends(bends)
    history = {}
    for m in range(1, 4):
        history[m] = arc.step(m, normal, transverse, targets)
        assert not any(history[m]), f"order {m} did not vanish"
    committed_state = copy.deepcopy(arc.series)

    naive = list(bends[:4])
    t0 = time.time()
    for k in range(4, max_bend + 1):
        top = k + 3
        samples = []
        for trial in (QQ(0), QQ(1), QQ(-3, 2)):
            arc.series = copy.deepcopy(committed_state)
            bends[k] = trial
            arc.set_bends(bends[:order + 1])
            values = None
            for m in range(k, top + 1):
                values = arc.step(m, normal, transverse, targets)
            samples.append((trial, values[29]))
        slope, constant = affine_fit(samples)
        assert slope == p.C * p.u, (
            f"newest-bend M30 slope at k={k} is {slope}, not C*u={p.C*p.u}")
        root = -constant / slope
        bends[k] = root
        arc.series = copy.deepcopy(committed_state)
        arc.set_bends(bends[:order + 1])
        rows_nonzero = {}
        for m in range(k, top + 1):
            values = arc.step(m, normal, transverse, targets)
            nz = [i + 1 for i, x in enumerate(values) if x]
            if nz:
                rows_nonzero[m] = nz
            if m == k:
                committed_state = copy.deepcopy(arc.series)
        naive.append(-(p.e1 * naive[-1] + p.e2 * naive[-2] + p.e3 * naive[-3]))
        label = {40: "H0", 41: "H1"}
        pretty = {m: [label.get(i, i) for i in v]
                  for m, v in rows_nonzero.items()}
        print(f"  k={k:2d} [{time.time()-t0:6.1f}s] r{k} = {root}  "
              f"({'SAME as' if root == naive[-1] else 'DIFFERS from'} "
              f"three-step)   nonzero rows at orders {k}..{top}: "
              f"{pretty if pretty else 'NONE'}")
        assert not rows_nonzero, (
            f"a row survived at k={k}: {rows_nonzero}")
    print("  denominators of the true bends:",
          [bends[i].denominator for i in range(4, max_bend + 1)])
    return bends


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-bend", type=int, default=13)
    parser.add_argument("--seed", type=int, default=811)
    parser.add_argument("--which", default="both")
    args = parser.parse_args()
    data = load_base()
    if args.which in ("both", "committed"):
        run_point(Point(data, committed_values(data)),
                  "COMMITTED POINT z_p = p+2", args.max_bend)
    if args.which in ("both", "third"):
        rng = random.Random(args.seed)
        while True:
            values = {q: QQ(rng.randint(-30, 30) or 5)
                      for q in data["layout_a"]}
            try:
                third = Point(data, values)
            except AssertionError:
                continue
            if all(v for v in third.units.values()):
                break
        run_point(third, f"THIRD AUDIT POINT (seed {args.seed})",
                  args.max_bend)


if __name__ == "__main__":
    main()
