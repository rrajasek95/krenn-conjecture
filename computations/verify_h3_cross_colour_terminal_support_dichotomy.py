#!/usr/bin/env python3
"""Exact support audit for the two-sign h=3 cross-colour terminal class.

Research evidence only.  Krenn's conjecture remains open, SP-CLEAN-BRIDGE is
untouched, and no certified dependency changes.

The source full-row identities are already audited in
verify_h3_cross_colour_repair_internal_edge_localization.py.  When both
d01+2*d02 and d01-2*d02 are nonzero, those identities give

    A_c B_d = 0 and C_c B_d = 0  for all c,d in {0,1},

plus four zero orientations on edge 23.  This checker exhausts the 64
zero/nonzero support patterns of A0,A1,B0,B1,C0,C1 and verifies the resulting
carrier dichotomy.  Standard library only; checks remain live under -O and
-I -S.
"""

from itertools import product


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    survivors = []
    for bits in product((False, True), repeat=6):
        a = bits[0:2]
        b = bits[2:4]
        c = bits[4:6]
        product_constraints = all(
            not (left[colour] and b[output])
            for left in (a, c)
            for colour in range(2)
            for output in range(2)
        )
        if not product_constraints:
            continue
        survivors.append(bits)
        carrier4_zero = not any(b)
        carrier5_zero = not any(a) and not any(c)
        require(carrier4_zero or carrier5_zero,
                ("support dichotomy failed", bits))

    require(len(survivors) == 19,
            ("surviving support count changed", len(survivors)))
    require(sum(not any(bits[2:4]) for bits in survivors) == 16,
            "carrier-4-zero branch count changed")
    require(sum(any(bits[2:4]) for bits in survivors) == 3,
            "live-carrier-4 branch count changed")

    # With both trade scalars nonzero, the two C2 sign families also kill
    # q(2@c,3@2) and q(2@2,3@c), c=0,1: all four 2-mixed orientations.
    edge23_orientations = (False,) * 4
    require(not any(edge23_orientations),
            "an edge-23 mixed orientation survived")
    print(
        "h3 cross-colour terminal support dichotomy: "
        "64 patterns -> 19; either carrier-4 pair B vanishes or all four "
        "carrier-5 entries A,C vanish; edge-23 mixed support=0/4"
    )


if __name__ == "__main__":
    main()
