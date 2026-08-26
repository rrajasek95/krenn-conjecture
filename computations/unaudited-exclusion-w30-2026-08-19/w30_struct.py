#!/usr/bin/env python3
"""W30 STRUCTURE OF THE FAILURE LOCUS.  UNAUDITED.  Pure combinatorics.

For each support m and each of the eight vertices this reports the data that
decides the SHAPE of "vertex v fails":

 1. FIRING LETTERS.  T_f is the set of letters carried by the live singles
    at v that are triggered.  A vertex whose live singles carry ONE letter
    can only ever constrain ONE row pair of the slice matrix; a vertex whose
    singles carry TWO letters constrains TWO row pairs -- and two row pairs
    sharing a row force RANK 1 of the whole slice matrix.

 2. STRUCTURE TYPE of ROWS = d u^T + sc*M:
      (a) some column of ROWS vanishes identically (u_q = 0 AND M-column
          absent)               -> rank ROWS <= 2 automatically, and collapse
                                   is ONE 2x2 minor;
      (b) an M-column is absent but u_q != 0 (all Gamma cells nonzero)
                                -> det ROWS == 0 automatically, and collapse
                                   on a clean pair {t1,t2} is exactly
                                   "rank of the 2x3 slice block = 1";
      (c)/(d) no absent column  -> det ROWS = 0 is a real condition.

 3. REACHABILITY: for each vertex, which (slice-index tuple, clean pair)
    combinations are realised by an admissible index choice, and whether the
    TWO clean pairs of a two-letter vertex are realised at a COMMON slice
    index tuple (which is what upgrades "two 2x2 minors" to "rank 1").

The consequence, stated for the record and tested numerically in
w30_rank1.py:

  LEMMA W30-S (type (b) + two firing letters).  Let v be an R-vertex whose
  slice matrix has an absent R-R column q0 with u_{q0} != 0, and whose live
  singles carry two distinct firing letters, and suppose both clean pairs
  are realised at a common slice index tuple by index choices with
  hafL != 0.  If v FAILS then the 3x3 slice matrix
        S_v = [ d(.) | c_a(.) | c_b(.) ]
  has RANK 1 at that slice index tuple.  Ranging over all reachable tuples,
  the three blocks involved are simultaneously rank one with a COMMON
  direction vector.
"""
from __future__ import annotations

import json
import os
import sys
from collections import Counter, defaultdict

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
W26 = os.path.join(os.path.dirname(HERE), "unaudited-blockers-w26-2026-08-16")
for _p in (HERE, W26):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import w30_lib as L                                               # noqa: E402
import w26_core as C                                              # noqa: E402

RES = os.path.join(HERE, "results_struct.json")


def slice_index(m, kind, v, w):
    """the coordinates the SLICE matrix at (kind,v) actually depends on --
    the trigger-free ones."""
    if kind == 'R':
        p = C.SIGINV[v]
        keys = [('x', p)] + [('y', u) for u in range(4, 8) if u != v]
        return tuple((k, i, w[i] if k == 'x' else w[i]) for k, i in keys)
    p = v
    keys = [('y', C.SIG[p])] + [('x', a) for a in range(4) if a != p]
    return tuple((k, i, w[i]) for k, i in keys)


def main():
    OUT = {"_header": "UNAUDITED W30 structure of the failure locus",
           "per_m": {}}
    for m in (25, 26, 27, 28):
        T = C.TEMPLATES[m]
        gs = set(C.gamma_edges(T))
        sing = C.single_edges(T)
        lv = set(C.live_singles(m))
        rec = {}
        for lab in L.VERTS:
            kind, v = L.vkey(lab)
            # ---- 1. firing letters carried by the LIVE singles at v
            letters = []
            for e, (a, b) in sing.items():
                if e not in lv:
                    continue
                if kind == 'R' and e[1] == v:
                    letters.append(b)
                if kind == 'L' and e[0] == v:
                    letters.append(a)
            # ---- 2. structure type
            if kind == 'R':
                p = C.SIGINV[v]
                cols = []
                for q in [q for q in range(4) if q != p]:
                    u2 = C.SIG[q]
                    e2 = (min(v, u2), max(v, u2))
                    i, j = [t for t in range(4) if t not in (p, q)]
                    u_zero = ((q, C.SIG[q]) not in gs)      # D_q absent
                    cols.append(dict(q=q, Mcol_present=(e2 in gs),
                                     u_identically_zero=u_zero))
                d_present = ((p, v) in gs)
            else:
                p = v
                cols = []
                for a in [a for a in range(4) if a != p]:
                    b, c = [t for t in range(4) if t not in (p, a)]
                    sb, sc2 = min(C.SIG[b], C.SIG[c]), max(C.SIG[b], C.SIG[c])
                    u_zero = ((sb, sc2) not in gs) or \
                             ((a, C.SIG[a]) not in gs)
                    e2 = (min(p, a), max(p, a))
                    cols.append(dict(q=a, Mcol_present=(e2 in gs),
                                     u_identically_zero=u_zero))
                d_present = ((p, C.SIG[p]) in gs)
            nzero_col = sum(1 for c2 in cols
                            if not c2['Mcol_present']
                            and c2['u_identically_zero'])
            nb = sum(1 for c2 in cols
                     if not c2['Mcol_present']
                     and not c2['u_identically_zero'])
            typ = ('a' if nzero_col else ('b' if nb else 'd'))
            # ---- 3. reachability
            idx = L.index_choices_cached(m, kind, v)
            pairs_at = defaultdict(set)
            fire_sizes = Counter()
            for (w, fire) in idx:
                fire_sizes[len(fire)] += 1
                if len(fire) != 1:
                    continue
                ct = tuple(sorted(t for t in range(3) if t not in fire))
                pairs_at[slice_index(m, kind, v, w)].add(ct)
            distinct_pairs = set()
            for s in pairs_at.values():
                distinct_pairs |= s
            n_common = sum(1 for s in pairs_at.values() if len(s) >= 2)
            rec[lab] = dict(
                live_single_letters=sorted(set(letters)),
                n_distinct_firing_letters=len(set(letters)),
                d_column_present=d_present,
                columns=cols, structure_type=typ,
                n_index_choices=len(idx),
                fire_size_hist=dict(fire_sizes),
                clean_pairs_realised=sorted(str(p2)
                                            for p2 in distinct_pairs),
                n_slice_tuples=len(pairs_at),
                n_slice_tuples_with_two_pairs=n_common,
                RANK1_FORCED_IF_FAILS=(typ == 'b' and n_common > 0))
        OUT["per_m"][m] = rec
        print("=== m=%d" % m, flush=True)
        for lab in L.VERTS:
            r = rec[lab]
            print("  %-3s type=%s letters=%-9s pairs=%-22s "
                  "tuples=%3d  two-pair tuples=%3d  RANK1_FORCED=%s"
                  % (lab, r['structure_type'],
                     r['live_single_letters'],
                     ",".join(r['clean_pairs_realised']),
                     r['n_slice_tuples'], r['n_slice_tuples_with_two_pairs'],
                     r['RANK1_FORCED_IF_FAILS']), flush=True)
    json.dump(OUT, open(RES, "w"), indent=1, default=str)
    print("STRUCT DONE -> results_struct.json", flush=True)


if __name__ == "__main__":
    main()
