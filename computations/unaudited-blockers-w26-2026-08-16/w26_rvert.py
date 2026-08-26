#!/usr/bin/env python3
"""W26 -- THE R-VERTEX DECOMPOSITION (new here).  UNAUDITED.  Exact only.

Motivation.  Group the twelve singles by their R-endpoint j (not by their
L-endpoint i as W24 did).  The three singles into j are (i,j), i in
L \\ {sigma^-1 j}, and they all switch on the SAME coordinate y_j.  Phi is
LINEAR in the y_j-slice data, so the whole j-system becomes a 3-vector
equation over the three letters of y_j:

    M(.)  (Ahat, Bhat, Chat, Dhat)^T  =  kappa

with M the 3x4 matrix whose columns are the y_j-slices of the four blocks
that touch j, and kappa the single-contribution vector supported on the
letters at which a single into j fires.

j = 6 (the case used below):  the four blocks touching 6 in Gamma are
A_36 (sigma), A_46, A_56, A_67; the singles are (0,6) cell (0,2),
(1,6) cell (1,1), (2,6) cell (2,1).  So kappa has the (2,6)- and
(1,6)-contributions in slot y6 = 1 and the (0,6)-contribution in slot
y6 = 2.

j-ISOLATED WORD: a mixed word all of whose active LIVE singles have
R-endpoint j.  The j-system is the residual system on those words in the
<= 3 unknowns z_(i,j).
"""
from __future__ import annotations

import os
import sys
from fractions import Fraction
from itertools import product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w26_core as C                                              # noqa: E402

_ISO = {}


def rvert_words(m, j):
    """all mixed words whose active live singles all have R-endpoint j
    (at least one active), grouped as (word, tuple of active singles)."""
    key = (m, j)
    if key in _ISO:
        return _ISO[key]
    T = C.TEMPLATES[m]
    sing = C.single_edges(T)
    lv = set(C.live_singles(m))
    out = []
    for w in C.MIXED:
        act = tuple(f for f in lv
                    if w[f[0]] == sing[f][0] and w[f[1]] == sing[f][1])
        if act and all(f[1] == j for f in act):
            out.append((w, act))
    _ISO[key] = tuple(out)
    return _ISO[key]


def rvert_targets(m, j):
    return tuple(sorted(e for e in C.live_singles(m) if e[1] == j))


def rvert_verdict(m, bl, j):
    """residual sub-system on the j-isolated words, unknowns z_(i,j)."""
    gs = set(C.gamma_edges(C.TEMPLATES[m]))
    tg = rvert_targets(m, j)
    idx = {e: k for k, e in enumerate(tg)}
    n = len(tg)
    rows = []
    for w, act in rvert_words(m, j):
        v = [Fraction(0)] * n
        for f in act:
            v[idx[f]] = C.coeff(bl, gs, f, w)
        cst = C.phi(bl, gs, w)
        if any(v) or cst != 0:
            rows.append(v + [-cst])
    if not rows:
        return dict(j=j, n_rows=0, killed=False, inconsistent=False,
                    forced=[], targets=[str(e) for e in tg])
    Rw, piv = C.rref(rows, n + 1)
    if n in piv:
        return dict(j=j, n_rows=len(rows), rank=len(piv), inconsistent=True,
                    forced=[], killed=True, targets=[str(e) for e in tg])
    sol = [Fraction(0)] * n
    for k, pc in enumerate(piv):
        if pc < n:
            sol[pc] = Rw[k][n]
    ker = C.kernel_basis([r[:n] for r in rows], n)
    forced = [str(tg[k]) for k in range(n)
              if sol[k] == 0 and all(b[k] == 0 for b in ker)]
    return dict(j=j, n_rows=len(rows), rank=len(piv), inconsistent=False,
                solution_dim=len(ker), forced=forced, killed=bool(forced),
                targets=[str(e) for e in tg])


def all_rvert(m, bl):
    return {j: rvert_verdict(m, bl, j) for j in (4, 5, 6, 7)}


# ------------------------------------------------ the 3x3 matrix G at j=6
def Gmat(bl, m, x3, y5, y7):
    """columns  g_{x3} = A36[x3][.],  V[.][y7] = A67[.][y7],
                U[y5][.] = A56[y5][.]  (rows indexed by y6).
    A_36 absent at m=25 -> first column is 0."""
    gs = set(C.gamma_edges(C.TEMPLATES[m]))
    g = [bl[(3, 6)][x3][t] if (3, 6) in gs else Fraction(0) for t in range(3)]
    V = [bl[(6, 7)][t][y7] for t in range(3)]
    U = [bl[(5, 6)][y5][t] for t in range(3)]
    return [[g[t], V[t], U[t]] for t in range(3)]


def det3(M):
    return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
            - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
            + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))


def detG_table(bl, m):
    """{(x3,y5,y7): det G} -- the branch discriminant of the j=6 system."""
    return {(x3, y5, y7): det3(Gmat(bl, m, x3, y5, y7))
            for x3 in range(3) for y5 in range(3) for y7 in range(3)}


def main():
    import json
    import w26_pts as PT
    out = {"_header": "UNAUDITED W26 R-vertex (j) sub-systems."}
    print("j-isolated word counts and target sets:")
    for m in (25, 26, 27, 28):
        print("  m=%d" % m, {j: (len(rvert_words(m, j)),
                                 [str(e) for e in rvert_targets(m, j)])
                             for j in (4, 5, 6, 7)})
        out["m%d_sizes" % m] = {str(j): len(rvert_words(m, j))
                                for j in (4, 5, 6, 7)}
    recs = []
    print("=" * 78)
    for m, tag, bl in PT.stored_points():
        rv = all_rvert(m, bl)
        dt = detG_table(bl, m)
        nz = sum(1 for v in dt.values() if v != 0)
        rec = dict(m=m, tag=tag,
                   rvert={str(j): rv[j]["killed"] for j in (4, 5, 6, 7)},
                   rvert_detail={str(j): rv[j] for j in (4, 5, 6, 7)},
                   n_detG_nonzero=nz,
                   van=PT.vanishing_stratum(m, bl))
        recs.append(rec)
        print("  m=%d %-24s van=%-5s rvert=%s  #detG!=0 %2d/27"
              % (m, tag[:24], rec["van"],
                 "".join("K" if rv[j]["killed"] else "." for j in (4, 5, 6, 7)),
                 nz), flush=True)
    out["records"] = recs
    nk = sum(1 for r in recs if all(r["rvert"].values()))
    n6 = sum(1 for r in recs if r["rvert"]["6"])
    print("all four R-vertex systems kill: %d/%d ; j=6 alone kills: %d/%d"
          % (nk, len(recs), n6, len(recs)))
    out["tally"] = dict(n=len(recs), all_four=nk, j6=n6)
    json.dump(out, open(os.path.join(HERE, "results_rvert.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
