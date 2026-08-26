#!/usr/bin/env python3
"""A7 -- TARGET 1(b) part 1: the m=25 effectively-clean word set and its box
structure, verified independently.

Checks
  (B1) |effectively-clean| = 2624 (mixed words) and none is constant;
  (B2) for EVERY L-word x the clean y-set is a product box S4 x S5 x S6 x S7
       (exhaustive, all 81 x);
  (B3) the number of L-words with S4 = {0,1,2}, split by x1;
  (B4) which L-words have ALL FOUR alphabets full (the words where the
       two-line hand proof of case 2 can be run at a single word);
  (B5) same for m = 24, 26, 27, 28 and for the C_8 member (product box?);
  (B6) MUTATION control: a corrupted template must break the box property or
       the counts.
"""
from __future__ import annotations
import os, sys, json, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a7_core import (W8_IMMUNE, WORDS, MIXED, CONSTS, F_gamma, k_of,
                     word_clean, single_cells)

HERE = os.path.dirname(os.path.abspath(__file__))


def boxes(T):
    Fg = F_gamma(T)
    out = {}
    nonbox = []
    for x in itertools.product(range(3), repeat=4):
        ys = [y for y in itertools.product(range(3), repeat=4)
              if k_of(T, tuple(x) + tuple(y), Fg) == 0]
        proj = [sorted({y[k] for y in ys}) for k in range(4)] if ys else \
            [[], [], [], []]
        n = 1
        for p in proj:
            n *= len(p)
        if n != len(ys):
            nonbox.append((x, len(ys), n))
        out[x] = (proj, len(ys))
    return out, nonbox


def analyse(T, label):
    bx, nonbox = boxes(T)
    total = sum(v[1] for v in bx.values())
    Fg = F_gamma(T)
    n_const_clean = sum(1 for w in CONSTS if k_of(T, w, Fg) == 0)
    fullS4 = {}
    all_full = []
    for x, (proj, cnt) in bx.items():
        if proj[0] == [0, 1, 2]:
            fullS4.setdefault(x[1], []).append(x)
        if all(p == [0, 1, 2] for p in proj):
            all_full.append(x)
    # word-clean comparison
    sc = single_cells(T)
    wc_total = sum(1 for w in MIXED if word_clean(T, w, sc))
    return dict(label=label, total_eff_clean=total,
                nonbox_Lwords=[[list(a), b, c] for a, b, c in nonbox],
                constants_eff_clean=n_const_clean,
                word_clean_total=wc_total,
                n_full_S4_by_x1={k: len(v) for k, v in sorted(fullS4.items())},
                n_full_S4=sum(len(v) for v in fullS4.values()),
                all_full_Lwords=[list(x) for x in all_full],
                distinct_box_shapes=sorted({str([len(p) for p in v[0]])
                                            for v in bx.values()}))


def main():
    res = {}
    for m in range(24, 29):
        r = analyse(W8_IMMUNE[m], "m=%d" % m)
        res["m%d" % m] = r
        print("m=%d: eff-clean=%d word-clean=%d nonbox=%d fullS4=%s allfull=%s"
              % (m, r["total_eff_clean"], r["word_clean_total"],
                 len(r["nonbox_Lwords"]), r["n_full_S4_by_x1"],
                 r["all_full_Lwords"]))
    # mutation control
    T = list(W8_IMMUNE[25])
    T[3] = 3          # widen a single-cell block 0-4 from 1 cell to 2
    r = analyse(T, "m=25 MUTATED")
    res["mutation"] = r
    print("MUTATION: eff-clean=%d (was 2624) nonbox=%d -> fired=%s"
          % (r["total_eff_clean"], len(r["nonbox_Lwords"]),
             r["total_eff_clean"] != 2624 or r["nonbox_Lwords"]))
    json.dump(res, open(os.path.join(HERE, "results_boxes.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
