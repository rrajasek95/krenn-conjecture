#!/usr/bin/env python3
"""Claim (A): pipeline validity at the committed exact generic-L point.

Independently reconstructs the centre bends s, t, r3 from the committed
relations F1, F2, G, then checks
  * Q_1..Q_8 all vanish on the centre arc built by the three-step recurrence,
  * dQ_7/dr_4 = C*u = 6791850 exactly (by interpolation, not dual numbers),
  * Q_7^{M30} : Q_7^{M33} = u : v = 75 : -18.
"""
from fractions import Fraction as QQ
import time

from myarc import Arc, collapse, committed_point, load_base, affine_fit


def solve_linear(row, point, variable):
    """Solve a committed relation, affine in `variable`, at the point."""
    slope = QQ(0)
    constant = QQ(0)
    for monomial, coefficient in row.items():
        degree = monomial.count(variable)
        assert degree <= 1, "relation is not affine in the bend"
        value = QQ(coefficient)
        for other in monomial:
            if other != variable:
                value *= point[other]
        if degree:
            slope += value
        else:
            constant += value
    assert slope, "relation has zero slope at the point"
    return -constant / slope


def g_relation(data, point, s, t):
    """The committed generic-L third-bend centre G, monic in r3, evaluated."""
    a = data["layout_a"]

    def z(index):
        return point[a[index]]

    # G = ... - s*z0*z52 + s*z7*z54 - t*z0 - t*z52 - r3   (committed formula,
    # verify_n8_p5_schur_generic_L_g_center.py lines 431-446)
    value = (
        z(0) * z(26) * z(30) * z(54)
        - z(26) * z(30) ** 2 * z(54)
        + z(0) * z(7) * z(46) * z(54)
        - z(7) * z(24) * z(46) * z(54)
        - z(7) * z(30) * z(46) * z(54)
        - z(0) * z(26) * z(52) * z(54)
        + z(26) * z(30) * z(52) * z(54)
        + z(7) * z(46) * z(52) * z(54)
        + z(7) * z(26) * z(54) ** 2
        - s * z(0) * z(52)
        + s * z(7) * z(54)
        - t * z(0)
        - t * z(52)
    )
    return value  # r3 = value, since the r3 coefficient is -1


def main():
    t0 = time.time()
    data = load_base()
    point = committed_point(data)
    a = data["layout_a"]

    def z(index):
        return point[a[index]]

    # centre: L = z9*z25 - z11*z46
    assert z(9) * z(25) - z(11) * z(46) == 0, "point left L=0"
    s = solve_linear(data["first_relation"], point, data["first_bend"])
    point[data["first_bend"]] = s
    t = solve_linear(data["second_relation"], point, data["second_bend"])
    r3 = g_relation(data, point, s, t)
    print(f"z46={z(46)}  s={s}  t={t}  r3={r3}")

    e1 = z(0) + z(30) + z(52)
    e2 = z(0) * z(30) + z(0) * z(52) + z(30) * z(52)
    e3 = z(0) * z(30) * z(52)
    C = QQ(1, 2) * z(11) * z(16) ** 2 * z(41)
    u = z(26) + z(45)
    v = z(26) - z(44)
    b = z(44) + z(45)
    print(f"e=({e1},{e2},{e3})  C={C}  u={u}  v={v}  b={b}  C*u={C*u}")
    assert u == z(26) + b - z(44)

    dynamic = set(data["local_variables"]) | {a[46]}
    normal = [collapse(r, point, dynamic) for r in data["normal"]]
    transverse = [collapse(r, point, dynamic) for r in data["transverse"]]
    targets = [collapse(r, point, dynamic)
               for r in list(data["obstruction"]) + list(data["pure"])]
    print(f"[{time.time()-t0:.1f}s] rows collapsed")

    order = 8

    def run(bends):
        arc = Arc(data, point, order)
        arc.set_bends(bends)
        out = []
        for m in range(1, order + 1):
            out.append(arc.step(m, normal, transverse, targets))
        return out

    def recurrence_bends(r4=None):
        bends = [z(46), s, t, r3]
        if r4 is not None:
            bends.append(QQ(r4))
        while len(bends) <= order:
            bends.append(-(e1 * bends[-1] + e2 * bends[-2] + e3 * bends[-3]))
        return bends

    base_bends = recurrence_bends()
    print("recurrence bends:", [str(x) for x in base_bends])
    history = run(base_bends)
    for m in range(1, order + 1):
        nonzero = [(i + 1, val) for i, val in enumerate(history[m - 1]) if val]
        print(f"  order {m}: nonzero rows = {[i for i, _ in nonzero]}"
              f"   [{time.time()-t0:.1f}s]")
    assert all(not any(row) for row in history), \
        "Q_1..Q_8 did not all vanish on the recurrence arc"
    print("CLAIM A part 1: Q_1..Q_8 = 0 on the centre arc  -> reproduced")

    # dQ7/dr4 by exact interpolation over three samples of r4
    samples30 = []
    samples33 = []
    for trial in (QQ(0), QQ(1), QQ(-3, 7)):
        bends = recurrence_bends(r4=trial)
        out = run(bends)
        samples30.append((trial, out[6][29]))
        samples33.append((trial, out[6][32]))
    slope30, const30 = affine_fit(samples30)
    slope33, const33 = affine_fit(samples33)
    print(f"dQ7^M30/dr4 = {slope30}   (C*u = {C*u})")
    print(f"dQ7^M33/dr4 = {slope33}   (C*v = {C*v})")
    assert slope30 == C * u, "dQ7/dr4 != C*u"
    assert slope33 == C * v, "dQ7^M33/dr4 != C*v"
    print("CLAIM A part 2: monicity slope C*u reproduced (M33 gives C*v)")

    # M30:M33 = u:v as functions of r4
    print(f"Q7^M30(r4=0) = {const30}   Q7^M33(r4=0) = {const33}")
    assert const30 * v == const33 * u, "M30:M33 != u:v at r4=0"
    ratio = QQ(slope30, 1) / slope33
    print(f"slope ratio M30:M33 = {ratio}  u/v = {QQ(u, v)}")
    assert ratio == QQ(u, v)
    print("CLAIM A part 3: M30:M33 = u:v = 75:-18 reproduced")
    print(f"total {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
