#!/usr/bin/env python3
"""Determine the exact SCOPE of the committed identities Q7 = C*u*W4 and
Q8 = C*u*W5.

The committed checker eliminates r4 via W4 before comparing Q8, so from the
ledger alone one cannot tell whether

  (V1)  Q8 - C*u*W5  vanishes modulo (L,F1,F2,G)                 -- or
  (V2)  Q8 - C*u*W5  vanishes only modulo (L,F1,F2,G,W4).

This matters for claim (D): the impulse-response argument dQ_{k+4}/dr_k =
C*u*e1 is only forced by the conjecture under (V1).

Test: put the centre bends at their forced values but leave r4, r5 FREE
(generic rationals) and compare Q7, Q8 against C*u*W4, C*u*W5 numerically.
"""
from fractions import Fraction as QQ
import time

from myarc import Arc, collapse, committed_point, load_base
from step1_claimA import solve_linear, g_relation


def main():
    t0 = time.time()
    data = load_base()
    point = committed_point(data)
    a = data["layout_a"]
    z = lambda i: point[a[i]]
    s = solve_linear(data["first_relation"], point, data["first_bend"])
    point[data["first_bend"]] = s
    t = solve_linear(data["second_relation"], point, data["second_bend"])
    r3 = g_relation(data, point, s, t)
    e1 = z(0) + z(30) + z(52)
    e2 = z(0) * z(30) + z(0) * z(52) + z(30) * z(52)
    e3 = z(0) * z(30) * z(52)
    C = QQ(1, 2) * z(11) * z(16) ** 2 * z(41)
    u = z(26) + z(45)
    v = z(26) - z(44)

    dynamic = set(data["local_variables"]) | {a[46]}
    normal = [collapse(r, point, dynamic) for r in data["normal"]]
    transverse = [collapse(r, point, dynamic) for r in data["transverse"]]
    targets = [collapse(r, point, dynamic) for r in data["obstruction"]]

    order = 9

    def run(bends):
        arc = Arc(data, point, order)
        arc.set_bends(bends)
        return [arc.step(m, normal, transverse, targets)
                for m in range(1, order + 1)]

    # generic free r4, r5, r6 -- deliberately NOT satisfying W4, W5, W6
    for r4, r5, r6 in ((QQ(3), QQ(-5, 2), QQ(11, 4)),
                       (QQ(-7, 3), QQ(1), QQ(0))):
        bends = [z(46), s, t, r3, r4, r5, r6]
        out = run(bends)
        w4 = r4 + e1 * r3 + e2 * t + e3 * s
        w5 = r5 + e1 * r4 + e2 * r3 + e3 * t
        w6 = r6 + e1 * r5 + e2 * r4 + e3 * r3
        q7_30, q7_33 = out[6][29], out[6][32]
        q8_30, q8_33 = out[7][29], out[7][32]
        q9_30, q9_33 = out[8][29], out[8][32]
        print(f"\nr4={r4} r5={r5} r6={r6}")
        print(f"  Q7^M30 = {q7_30}    C*u*W4 = {C*u*w4}   "
              f"equal={q7_30 == C*u*w4}")
        print(f"  Q7^M33 = {q7_33}    C*v*W4 = {C*v*w4}   "
              f"equal={q7_33 == C*v*w4}")
        print(f"  Q8^M30 = {q8_30}    C*u*W5 = {C*u*w5}   "
              f"equal={q8_30 == C*u*w5}")
        print(f"  Q8^M33 = {q8_33}    C*v*W5 = {C*v*w5}   "
              f"equal={q8_33 == C*v*w5}")
        print(f"  Q9^M30 = {q9_30}    C*u*W6 = {C*u*w6}   "
              f"equal={q9_30 == C*u*w6}")
        print(f"  Q9^M33 = {q9_33}    C*v*W6 = {C*v*w6}   "
              f"equal={q9_33 == C*v*w6}")
        others7 = [i + 1 for i, x in enumerate(out[6]) if x and i not in (29, 32)]
        others8 = [i + 1 for i, x in enumerate(out[7]) if x and i not in (29, 32)]
        others9 = [i + 1 for i, x in enumerate(out[8]) if x and i not in (29, 32)]
        print(f"  other nonzero rows: order7={others7} order8={others8} "
              f"order9={others9}")
    print(f"\ntotal {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
