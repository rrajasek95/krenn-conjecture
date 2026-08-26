#!/usr/bin/env python3
"""W30 FAILURE-MECHANISM ANALYSER.  UNAUDITED.  Exact only.

For every index choice at a vertex, classify the non-delivery mode:

  ROWS = d u^T + sc * M   (3x3; sc = hafL for R-vertices, hafR for L)
  |T_f| = 1, T_c = {t1,t2}:
      DELIVER : row_f in span{clean rows}
      N1      : rank{clean} = 2 and det ROWS != 0        (no collapse at all)
      N2      : rank{clean} <= 1 and row_f outside       (LETTER COLLAPSE)
  |T_f| = 2 : T_c is a single row; |T_f| = 3 : span is 0.

Also records the rank of the SLICE MATRIX  [d | c_1 | c_2 | c_3]  (3x4, the
Gamma-edge slices at the vertex) -- the trigger-free object of W26-K -- and
tests the structural prediction

  PREDICTION P: at a vertex whose singles carry TWO distinct firing letters,
  failure via N2 at both firing letters forces rank(slice matrix) = 1.

usage: w30_mech.py <pointfile.json> [outsuffix]
"""
from __future__ import annotations

import json
import os
import sys
import time
from collections import Counter
from fractions import Fraction

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
W26 = os.path.join(os.path.dirname(HERE), "unaudited-blockers-w26-2026-08-16")
for _p in (HERE, W26):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import w30_lib as L                                               # noqa: E402
import w26_core as C                                              # noqa: E402

F = Fraction


def det3(M, K):
    return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
            - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
            + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))


def slice_matrix(m, bl, kind, v, w, K):
    """the 3x(1+3) matrix of Gamma-edge slices at the vertex: the sigma
    column d and the three cross-slices (absent edge -> zero column).
    TRIGGER-FREE: depends only on the letter at v's partner and on the
    letters at v's Gamma-neighbours, not on the trigger coordinates."""
    sd = L.slice_data(m, bl, kind, v, w, K)
    if sd is None:
        return None
    d, uu, MM, sc = sd
    return [[d[t]] + [MM[t][j] for j in range(3)] for t in range(3)]


def analyse_vertex(m, bl, lab, K):
    kind, v = L.vkey(lab)
    idx = L.index_choices_cached(m, kind, v)
    modes = Counter()
    slice_ranks = Counter()
    sub_ranks = {}
    collapse_by_fire = {}
    rowsp_seen = {}
    n_del = 0
    for (w, fire) in idx:
        sd = L.slice_data(m, bl, kind, v, w, K)
        if sd is None:
            modes['zero_scale'] += 1
            continue
        d, uu, MM, sc = sd
        rows = [[d[t] * uu[j] + sc * MM[t][j] for j in range(3)]
                for t in range(3)]
        clean_ts = [t for t in range(3) if t not in fire]
        cleanrows = [rows[t] for t in clean_ts]
        rc = L.rank_rows(cleanrows, K)
        ok = all(L.rank_rows(cleanrows + [rows[t]], K) == rc for t in fire)
        dt = det3(rows, K)
        S = [[d[t]] + [MM[t][j] for j in range(3)] for t in range(3)]
        slice_ranks[L.rank_rows(S, K)] += 1
        key = tuple(sorted(fire))
        # rank of the SLICE rows restricted to the CLEAN letters (the
        # structural prediction: N2 collapse <=> this 2x4 block is rank 1)
        srk = L.rank_rows([S[t] for t in clean_ts], K)
        sub_ranks[(len(clean_ts), srk)] = sub_ranks.get((len(clean_ts),
                                                         srk), 0) + 1
        if ok:
            n_del += 1
            modes['DELIVER'] += 1
        elif len(fire) == 1 and rc == 2 and not K.iszero(dt):
            modes['N1_det_nonzero'] += 1
        elif len(fire) == 1 and rc <= 1:
            modes['N2_collapse'] += 1
            collapse_by_fire[key] = collapse_by_fire.get(key, 0) + 1
        elif len(fire) == 1:
            modes['N3_other'] += 1
        else:
            modes['multi_fire'] += 1
        rowsp_seen.setdefault(key, [0, 0])
        rowsp_seen[key][0] += 1
        if ok:
            rowsp_seen[key][1] += 1
    return dict(modes=dict(modes), slice_ranks=dict(slice_ranks),
                clean_sub_ranks={str(k): v2 for k, v2 in sub_ranks.items()},
                n_deliver=n_del, DELIVERS=n_del > 0,
                collapse_by_fire={str(k): v2
                                  for k, v2 in collapse_by_fire.items()},
                by_fire={str(k): v2 for k, v2 in rowsp_seen.items()})


def main():
    src = sys.argv[1]
    suf = sys.argv[2] if len(sys.argv) > 2 else ""
    d = json.load(open(os.path.join(HERE, src)))
    res = os.path.join(HERE, "results_mech%s.json" % suf)
    OUT = {"_header": "UNAUDITED W30 failure-mechanism analysis",
           "source": src, "recs": []}
    pts = d.get("points") or d.get("hits") or []
    t0 = time.time()
    for i, rec in enumerate(pts):
        if rec.get("van"):
            continue
        m = rec.get("m") or d.get("m")
        pp = int(rec.get("p") or d.get("p") or 0)
        if pp:
            bl = {eval(k): [[int(z) % pp for z in row] for row in v]
                  for k, v in rec["point"].items()}
            K = L.FP(pp)
        else:
            bl = {eval(k): [[F(z) for z in row] for row in v]
                  for k, v in rec["point"].items()}
            K = L.QF
        out = dict(m=m, tag=rec.get("tag", rec.get("seed", i)), vert={})
        for lab in L.VERTS:
            out["vert"][lab] = analyse_vertex(m, bl, lab, K)
        out["fails"] = [l for l in L.VERTS if not out["vert"][l]["DELIVERS"]]
        OUT["recs"].append(out)
        json.dump(OUT, open(res, "w"), indent=1, default=str)
        print("[%2d] m=%d %-26s fails=%-22s %s (%.0fs)"
              % (i, m, str(out["tag"])[:26], ",".join(out["fails"]) or "-",
                 {l: (out["vert"][l]["modes"], out["vert"][l]["slice_ranks"])
                  for l in out["fails"]}, time.time() - t0), flush=True)
    OUT["done"] = True
    json.dump(OUT, open(res, "w"), indent=1, default=str)
    print("MECH DONE %d recs %.0fs" % (len(OUT["recs"]), time.time() - t0),
          flush=True)


if __name__ == "__main__":
    main()
