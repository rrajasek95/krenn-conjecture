#!/usr/bin/env python3
"""Robustness control: repeat the true-arc construction at a RANDOM exact
generic-L rational point, not the committed arithmetic-progression point
z_p = p+2 (which has many accidental coincidences).

Same conclusion structure as true_arc_point.py:
  * solve the newest bend from the M30 compatibility row,
  * check the other 38 mixed rows and the two pure rows H0,H1 vanish,
  * compare the true bend against the conjectured three-step recurrence.
"""

from fractions import Fraction as QQ
import argparse
import random
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from impulse_response_point import Dual, evaluate_row, load_module  # noqa: E402
from true_arc_point import Graph  # noqa: E402


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20260810)
    parser.add_argument("--max-bend", type=int, default=9)
    arguments = parser.parse_args()
    rng = random.Random(arguments.seed)

    t0 = time.time()
    R4 = load_module("p5_r4_rand", "verify_n8_p5_generic_L_koszul_ward_r4.py")
    G = R4.G
    F2 = R4.F2
    P5 = G.P5
    base = F2.audit(return_data=True)
    POINTMOD = load_module("p5_point_rand",
                           "analyze_n8_p5_full_point_weierstrass.py")
    layout = base["layout"]
    a = layout["a"]

    point = {variable: QQ(rng.randint(-40, 40) or 7)
             for variable in a.values()}
    point[a[46]] = point[a[9]] * point[a[25]] / point[a[11]]
    assert point[a[44]] + point[a[45]], "random point left the b chart"
    first_at_point = POINTMOD.partial_evaluate(
        base["first_relation"], point, {base["first_bend"]})
    point[base["first_bend"]] = POINTMOD.affine_root(
        first_at_point, base["first_bend"])
    second_at_point = POINTMOD.partial_evaluate(
        base["second_relation"], point, {base["second_bend"]})
    point[base["second_bend"]] = POINTMOD.affine_root(
        second_at_point, base["second_bend"])
    s = point[base["first_bend"]]
    t = point[base["second_bend"]]
    r3 = POINTMOD.third_bend_root(layout, point, s, t)
    z = lambda parameter: point[a[parameter]]
    e1 = z(0) + z(30) + z(52)
    e2 = z(0) * z(30) + z(0) * z(52) + z(30) * z(52)
    e3 = z(0) * z(30) * z(52)
    unit = QQ(1, 2) * z(11) * z(16) ** 2 * z(41)
    u = z(26) + z(45)
    print(f"[{time.time()-t0:.1f}s] random point: z0={z(0)} z30={z(30)} "
          f"z52={z(52)} C*u={unit*u}", flush=True)

    PURE = G.F2.SCHUR.audit(return_data=True)["pure_stricts"]
    dynamic = set(base["local_variables"]) | {a[46]}
    rows = (
        [evaluate_row(x, point, dynamic) for x in base["normal"]],
        [evaluate_row(x, point, dynamic) for x in base["transverse"]],
        [evaluate_row(x, point, dynamic)
         for x in list(base["obstruction"]) + list(PURE)],
    )

    bends = [z(46), s, t, r3]
    naive = list(bends)
    for k in range(4, arguments.max_bend + 1):
        start = time.time()
        maximum_order = k + 3
        trial = [Dual(value) for value in bends] + [Dual(0, 1)]
        graph = Graph(base, point, P5, maximum_order, trial, rows)
        history = [graph.step(order) for order in range(1, maximum_order + 1)]
        terminal = history[-1]
        slope = terminal[29].b
        assert slope == unit * u, f"M30 slope changed at k={k}: {slope}"
        value = -terminal[29].a / slope
        bends.append(value)
        naive.append(-(e1 * naive[-1] + e2 * naive[-2] + e3 * naive[-3]))
        residual = [row + 1 for row, item in enumerate(terminal)
                    if item.a + item.b * value]
        earlier = [(order + 1, row + 1)
                   for order, values in enumerate(history[:-1])
                   for row, item in enumerate(values)
                   if item.a + item.b * value]
        agree = "SAME as three-step" if value == naive[-1] else "DIFFERS"
        print(f"k={k:2d} [{time.time()-start:5.1f}s] {agree}; other rows "
              f"nonzero: {residual}; earlier violations: {earlier[:4]}",
              flush=True)


if __name__ == "__main__":
    main()
