#!/usr/bin/env python3
"""W15 TASK 3 -- survey of the whole (R) family (and the killed m=20..23
calibration band): which words are 'effectively clean', i.e. have fibre
contained in the set of matchings all of whose blocks are FULL.

Exact / combinatorial only.
"""

import json
import os
import sys
from itertools import product

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w15_core import (W8_IMMUNE, EDGES, EIDX, MATCHINGS, CONST_WORDS,
                      MIXED_WORDS, WORDS, FULL, is_clean,
                      single_cell_activity, supported_matchings)

HERE = os.path.dirname(os.path.abspath(__file__))
out = {}
LOG = []


def say(s=""):
    print(s)
    LOG.append(s)


for m, T in sorted(W8_IMMUNE.items()):
    act = single_cell_activity(T)
    fullm = set(mi for mi, mm in enumerate(MATCHINGS)
                if all(T[EIDX[e]] == FULL for e in mm))
    n_clean = n_effclean = 0
    n_clean_mixed = n_effclean_mixed = 0
    for w in WORDS:
        sup = supported_matchings(T, w)
        eff = set(sup) <= fullm
        cl = is_clean(T, w, act)
        assert (not cl) or eff, "clean must imply effectively clean"
        mixed = len(set(w)) > 1
        if cl:
            n_clean += 1
            n_clean_mixed += mixed
        if eff:
            n_effclean += 1
            n_effclean_mixed += mixed
    const_eff = []
    for c, w in enumerate(CONST_WORDS):
        sup = supported_matchings(T, w)
        const_eff.append({"colour": c, "fibre": len(sup),
                          "effectively_clean": bool(set(sup) <= fullm),
                          "extra_matchings":
                          [MATCHINGS[i] for i in sup if i not in fullm]})
    out[m] = {
        "n_full_matchings": len(fullm),
        "n_clean_words": n_clean, "n_clean_mixed": n_clean_mixed,
        "n_effectively_clean_words": n_effclean,
        "n_effectively_clean_mixed": n_effclean_mixed,
        "constants": const_eff,
    }
    ec = [c["colour"] for c in const_eff if c["effectively_clean"]]
    say(f"m={m:2d}  |F|={len(fullm):2d}  clean={n_clean:5d} "
        f"effclean={n_effclean:5d} (mixed {n_effclean_mixed:5d})  "
        f"constant fibres={[c['fibre'] for c in const_eff]}  "
        f"EFFECTIVELY-CLEAN CONSTANTS={ec}")

json.dump(out, open(os.path.join(HERE, "results_task3_survey.json"), "w"),
          indent=1, default=str)
open(os.path.join(HERE, "log_task3_survey.txt"), "w").write("\n".join(LOG)
                                                            + "\n")
