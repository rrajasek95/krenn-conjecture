#!/usr/bin/env python3
"""adv2 step 0 -- geometry dump + validation of my independent engine
against w26_core's from-the-definition engine.  UNAUDITED.  EXACT ONLY."""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import a2lib as A                                                 # noqa: E402
import w26_core as C                                              # noqa: E402

F = Fraction
OUT = {"_header": "UNAUDITED adv2 -- geometry + engine validation"}
RAN = []


def main():
    rng = random.Random(20260817)
    for m in (25, 26, 27, 28):
        G = A.Geo(m)
        rec = dict(m=m, gamma=[str(e) for e in G.gam], n_gamma=len(G.gam),
                   singles={str(e): list(c) for e, c in
                            sorted(G.sing.items())},
                   live=[str(e) for e in G.live],
                   n_clean=len(G.clean),
                   n_solo={str(e): len(G.solo[e]) for e in G.live})
        print("=" * 74)
        print("m=%d  Gamma(%d)=%s" % (m, len(G.gam),
                                      " ".join(str(e) for e in G.gam)))
        print("  singles: %s" % "  ".join(
            "%s@x%d=%d,y%d=%d" % (e, e[0], c[0], e[1], c[1])
            for e, c in sorted(G.sing.items())))
        print("  live=%d  clean words=%d" % (len(G.live), len(G.clean)))
        print("  solo sizes: %s" % {str(e): len(G.solo[e]) for e in G.live})
        # ---- engine validation on 3 random (non-clean) points
        RAN.append("engine_val_m%d" % m)
        nmis_phi = nmis_c = nmis_raw = 0
        for t in range(3):
            bl = {e: [[F(rng.randint(-9, 9) or 4, rng.randint(1, 4))
                       for _ in range(3)] for _ in range(3)] for e in G.gam}
            for w in C.WORDS[::37]:
                a = A.phi2(bl, G, w)
                b = C.phi(bl, G.gs, w)
                c = AL_phi_raw(m, bl, w)
                if a != b:
                    nmis_phi += 1
                if a != c:
                    nmis_raw += 1
                for e in G.live:
                    if A.coef2(bl, G, e, w) != C.coeff(bl, G.gs, e, w):
                        nmis_c += 1
        print("  ENGINE CHECK: phi2 vs C.phi mismatches=%d ; phi2 vs raw "
              "H_word mismatches=%d ; coef2 vs C.coeff mismatches=%d"
              % (nmis_phi, nmis_raw, nmis_c))
        assert nmis_phi == 0 and nmis_c == 0 and nmis_raw == 0
        rec["engine_mismatches"] = [nmis_phi, nmis_raw, nmis_c]
        OUT["m%d" % m] = rec
    declared = ["engine_val_m%d" % m for m in (25, 26, 27, 28)]
    missing = [d for d in declared if d not in RAN]
    print("\nCONTROL MANIFEST declared=%s ran=%s" % (declared, RAN))
    assert not missing, "CONTROL DID NOT RUN: %s" % missing
    OUT["control_manifest"] = dict(declared=declared, ran=RAN)
    json.dump(OUT, open(os.path.join(HERE, "results_setup.json"), "w"),
              indent=1, default=str)
    print("wrote results_setup.json")


def AL_phi_raw(m, bl, w):
    T = C.TEMPLATES[m]
    z = {e: F(0) for e in C.single_edges(T)}
    return C.H_word(bl, T, z, w)


if __name__ == "__main__":
    main()
