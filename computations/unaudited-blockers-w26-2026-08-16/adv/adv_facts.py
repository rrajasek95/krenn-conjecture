#!/usr/bin/env python3
"""W26 ADVERSARIAL LANE -- combinatorial facts of the templates.
UNAUDITED probe.  EXACT ONLY (no floats anywhere in this directory)."""
from __future__ import annotations

import json
import os
import sys
from itertools import product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
UP = os.path.dirname(HERE)
sys.path.insert(0, UP)
sys.path.insert(0, HERE)
import w26_core as C                                              # noqa: E402
import w26_sub as SB                                              # noqa: E402

OUT = {"_header": "UNAUDITED W26 adversarial lane -- template facts."}


def main():
    for m in (25, 26, 27, 28):
        T = C.TEMPLATES[m]
        gam = C.gamma_edges(T)
        sing = C.single_edges(T)
        lv = C.live_singles(m)
        dead = sorted(set(sing) - set(lv))
        rec = dict(gamma=[str(e) for e in gam], n_gamma=len(gam),
                   n_cells=9 * len(gam),
                   singles={str(e): list(c) for e, c in sorted(sing.items())},
                   live=[str(e) for e in lv], dead=[str(e) for e in dead],
                   n_clean=len(C.clean_words(m)))
        print("=" * 78)
        print("m=%d  |Gamma|=%d (%d cells)  clean words=%d"
              % (m, len(gam), 9 * len(gam), len(C.clean_words(m))))
        print("  Gamma:", [str(e) for e in gam])
        print("  singles (edge -> cell):",
              {str(e): c for e, c in sorted(sing.items())})
        print("  live:", [str(e) for e in lv])
        print("  dead:", [str(e) for e in dead])
        # solo counts
        solo = {}
        for e in lv:
            sw = SB.solo_words(m, e)
            solo[str(e)] = len(sw)
        print("  solo-word counts:", solo)
        rec["solo_counts"] = solo
        # iso groups
        grp = SB.iso_groups(m)
        gr = {}
        for can, xs in sorted(grp.items()):
            lab = "%d|%s" % (can[0][0], ",".join(str(e) for e in can))
            gr[lab] = len(xs)
        print("  iso groups (label -> #L-words):", gr)
        rec["iso_groups"] = gr
        # per-vertex-6 analysis: which y6 letters are excluded, per x
        if m in (25, 26, 27):
            excl = {}
            for x in product(range(3), repeat=4):
                bad = set()
                for e, cell in sing.items():
                    if e[1] == 6 and e in set(lv) and x[e[0]] == cell[0]:
                        bad.add(cell[1])
                excl.setdefault(tuple(sorted(bad)), []).append(x)
            print("  y6-exclusion classes:",
                  {str(k): len(v) for k, v in sorted(excl.items())})
            rec["y6_excl"] = {str(k): len(v) for k, v in sorted(excl.items())}
        OUT["m%d" % m] = rec
    # detailed (2,6) solo x-sets at m=26,27
    for m in (26, 27):
        sw = SB.solo_words(m, (2, 6))
        xs = sorted({w[:4] for w in sw})
        print("m=%d (2,6)-solo: %d words; distinct x: %d ; y6 values %s"
              % (m, len(sw), len(xs), sorted({w[6] for w in sw})))
        print("   x-set:", [".".join(map(str, x)) for x in xs])
        OUT["m%d_26solo_x" % m] = [list(x) for x in xs]
    json.dump(OUT, open(os.path.join(HERE, "results_facts.json"), "w"),
              indent=1, default=str)
    print("wrote results_facts.json")


if __name__ == "__main__":
    main()
