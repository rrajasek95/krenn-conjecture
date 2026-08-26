#!/usr/bin/env python3
"""W21 MOVE 1 -- diagnostics at the explicit non-factoring clean points.
UNAUDITED.  Exact only."""
import json, os, random, sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction
import w21_core as K, w21_site as SI
from w21_pf import load_w20_points

res = {"_header": "UNAUDITED W21 move-1 site diagnostics. Exact only."}
pts = load_w20_points()
for m in (26, 27, 28):
    T = K.W8_IMMUNE[m]; gam = K.gamma_edges(T); clean = K.clean_words(T)
    entry = []
    for tag, bl in pts[m][:1]:
        assert all(K.phi_value(bl, gam, w) == 0 for w in clean)
        rep = [SI.site_report(bl, gam, t, clean) for t in range(8)]
        entry.append(dict(tag=tag, sites=rep))
        print("=== m=%d  %s   factoring sites %s" % (m, tag, [r["site"] for r in rep if r["factors"]]))
        for r in rep:
            print("  site %d deg=%d common=%d dimW=%2d Kcap=%2d factors=%-5s pats=%2d reg=%2d "
                  "mergecomp=%d colclasses=%s blockranks=%s"
                  % (r["site"], r["deg"], r["n_common"], r["dimW"], r["dim_Kcap"],
                     r["factors"], r["n_patterns"], r["n_regular"], r["regular_merge_components"],
                     r["column_class_sizes"], sorted(r["block_ranks"].values())))
        for r in rep:
            if not r["factors"]:
                print("    site %d NON-FACTORING: column classes %s" % (r["site"], r["column_classes"]))
                print("      nonregular patterns (%d): %s" % (r["n_nonregular"], r["nonregular"][:20]))
    res["m%d" % m] = entry
json.dump(res, open("results_diag.json", "w"), indent=1, default=str)
