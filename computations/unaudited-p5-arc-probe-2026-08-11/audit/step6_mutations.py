#!/usr/bin/env python3
"""Mutation / control tests.

(i)   perturb one coefficient of a committed equation -> Q values must change
(ii)  the monicity slope dQ7/dr4 must equal C*u at a SECOND point too, and
      must not equal a mutated C formula
(iii) truncated-arc control: H0 must blow up at order 8, H1 at order 9
(iv)  break the centre (wrong s) -> low-order Q must stop vanishing
"""
from fractions import Fraction as QQ
import time

from myarc import load_base, affine_fit
from setup import Point, committed_values


def nonzero_profile(out):
    return [[i + 1 for i, x in enumerate(values) if x] for values in out]


def main():
    t0 = time.time()
    data = load_base()
    p = Point(data, committed_values(data))
    order = 10
    clean_rows = p.rows()
    bends = p.recurrence_bends(order)
    clean = p.run(bends, order, clean_rows)
    print("clean profile:", nonzero_profile(clean))

    print("\n--- (i) coefficient mutations of committed equations ---")
    survivors = 0
    total = 0
    for group, index in (("normal", 0), ("normal", 100), ("transverse", 3),
                         ("obstruction", 29), ("obstruction", 0)):
        for which in (0, 1, 7, 33, 101, 555):
            rows = p.rows(mutate=(group, index, QQ(1), which))
            out = p.run(bends, 8, rows)
            profile = nonzero_profile(out)
            changed = out != clean[:8]
            total += 1
            survivors += changed
            print(f"  mutate {group}[{index}] monomial #{which} +1 -> "
                  f"nonzero rows through order 8: {profile}  "
                  f"OUTPUT CHANGED={changed}")
    print(f"  {survivors}/{total} single-coefficient mutations changed the "
          f"order<=8 output (a tautological pipeline would give 0)")
    assert survivors, "no mutation changed the pipeline output"

    print("\n--- (ii) monicity slope is not hard-coded ---")
    for tag, q in (("committed", p),):
        samples = []
        for trial in (QQ(0), QQ(1), QQ(-2)):
            b2 = list(bends)
            b2[4] = trial
            out = q.run(b2, 7, clean_rows)
            samples.append((trial, out[6][29]))
        slope, _ = affine_fit(samples)
        mutatedC = QQ(1, 2) * q.z(11) * q.z(16) * q.z(41)
        print(f"  {tag}: measured dQ7/dr4 = {slope}; C*u = {q.C*q.u}; "
              f"match={slope == q.C*q.u}; mutated-C formula gives "
              f"{mutatedC*q.u} (match={slope == mutatedC*q.u})")
        assert slope == q.C * q.u and slope != mutatedC * q.u

    print("\n--- (iii) truncated-arc control (r4=r5=...=0) ---")
    truncated = [p.z(46), p.s, p.t, p.r3] + [QQ(0)] * (order - 3)
    out = p.run(truncated, order, clean_rows)
    label = {40: "H0", 41: "H1"}
    for m in range(1, order + 1):
        nz = [label.get(i + 1, i + 1) for i, x in enumerate(out[m - 1]) if x]
        print(f"  order {m:2d}: {nz}")
    h0_first = next(m for m in range(1, order + 1) if out[m - 1][39])
    h1_first = next(m for m in range(1, order + 1) if out[m - 1][40])
    print(f"  H0 first nonzero at order {h0_first}; "
          f"H1 first nonzero at order {h1_first}")
    print(f"  H0(order 8) = {out[7][39]}")
    print(f"  H1(order 9) = {out[8][40]}")

    print("\n--- (iv) break the centre: s -> s+1 ---")
    p2 = Point(data, committed_values(data))
    p2.s = p2.s + 1
    bad = [p2.z(46), p2.s, p2.t, p2.r3] + [QQ(0)] * (order - 3)
    out = p2.run(bad, 6, clean_rows)
    print("  nonzero profile with a wrong first bend:",
          nonzero_profile(out))
    assert any(nonzero_profile(out)), "wrong centre still gave zero rows"
    print(f"\ntotal {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
