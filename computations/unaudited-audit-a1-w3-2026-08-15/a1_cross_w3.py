"""AUDIT A1 -- cross-implementation comparison against W3's own classifier.

My verdicts come from a1_dichotomy (exact simplex).  W3's classify() uses
scipy float LP + exact re-check.  Disagreements are reported; a
disagreement where W3 says '?' or 'D?' is a W3 completeness gap, and a
disagreement of substance is a bug in one of the two.
"""

from __future__ import annotations

import random
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "unaudited-git-moment-w3-2026-08-15"))

from a1_core import COLS, all_cells                     # noqa: E402
from a1_dichotomy import classify, kempf_ness, random_support   # noqa: E402


def w3_key_to_mine(n, s_index):
    """W3 indexes cells by a flat integer; translate to my (u,v,i,j) key."""
    import itertools

    E = list(itertools.combinations(range(n), 2))
    k, r = divmod(s_index, 9)
    i, j = divmod(r, 3)
    u, v = E[k]
    return (u, v, i, j)


def mine_to_w3(n, key):
    import itertools

    E = list(itertools.combinations(range(n), 2))
    u, v, i, j = key
    k = E.index((u, v))
    return 9 * k + 3 * i + j


def run(n, trials, density, seed):
    from w3_balance import classify as w3classify

    rng = random.Random(seed)
    agree = dis = 0
    rows = []
    for _ in range(trials):
        S = random_support(n, rng, density)
        if not S:
            continue
        mine, _ = classify(n, S)
        Sw = frozenset(mine_to_w3(n, k) for k in S)
        try:
            theirs, _ = w3classify(n, Sw)
        except Exception as exc:                       # noqa: BLE001
            theirs = "EXC:" + type(exc).__name__
        kn_r, kn_def = kempf_ness(n, S)
        same = (mine == theirs)
        agree += same
        dis += (not same)
        rows.append((mine, theirs, len(S), kn_r, kn_def, same))
    return agree, dis, rows


if __name__ == "__main__":
    print("AUDIT A1 -- cross-check of the A.1 classifier vs W3's")
    print("=" * 78)
    for n, dens, tr in ((6, 0.20, 30), (6, 0.35, 20), (8, 0.08, 10)):
        agree, dis, rows = run(n, tr, dens, seed=2000 + n)
        print(f"n={n} density={dens}: agree={agree} disagree={dis}")
        for mine, theirs, ls, r, d, same in rows:
            if not same:
                print(f"    DISAGREE mine={mine} w3={theirs} |S|={ls}")
        # triangulate with the numeric Kempf-Ness route
        bad = 0
        for mine, theirs, ls, r, d, same in rows:
            if mine == "P" and (d > 1e-4 or r > 50):
                bad += 1
            if mine == "D" and (d < 1e-6 and r < 20):
                bad += 1
        print(f"    Kempf-Ness numeric triangulation mismatches: {bad}/{len(rows)}")
