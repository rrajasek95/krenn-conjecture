#!/usr/bin/env python3
"""W24 -- MINIMAL kill certificates.  For every stored exact clean point and
every row-isolating sub-system, find the SMALLEST set of words whose rows
already kill (inconsistent, or force one of the sub-system's cells to zero).
UNAUDITED.  Exact only."""
from __future__ import annotations

import json
import os
import sys
from fractions import Fraction
from itertools import combinations, product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w24_core as C                                              # noqa: E402
import w24_pts as P                                               # noqa: E402
import w24_ident as ID                                            # noqa: E402


def sub_rows(m, bl, xwords, targets):
    T = C.TEMPLATES[m]
    gam_set = set(C.gamma_edges(T))
    sing = C.single_edges(T)
    live = {e for e in sing
            if C.has_pm(gam_set, tuple(v for v in range(8) if v not in e))}
    idx = {e: k for k, e in enumerate(targets)}
    n = len(targets)
    rows = []
    for x in xwords:
        for y in product(range(3), repeat=4):
            w = tuple(x) + tuple(y)
            if len(set(w)) == 1:
                continue
            act = [e for e in sing if e in live
                   and w[e[0]] == sing[e][0] and w[e[1]] == sing[e][1]]
            if any(e not in idx for e in act):
                return None
            v = [Fraction(0)] * n
            for e in act:
                v[idx[e]] = ID.coeff(bl, gam_set, e, w)
            cst = C.phi(bl, gam_set, w)
            if any(v) or cst != 0:
                rows.append((w, v, cst))
    return rows


def kills(rows, n):
    aug = [list(v) + [-c] for _, v, c in rows]
    R, piv = C.rref(aug, n + 1)
    if n in piv:
        return "inconsistent"
    sol = [Fraction(0)] * n
    for k, pc in enumerate(piv):
        if pc < n:
            sol[pc] = R[k][n]
    ker = C.kernel_basis([list(v) for _, v, _ in rows], n)
    f = [k for k in range(n) if sol[k] == 0 and all(b[k] == 0 for b in ker)]
    return ("forced:%s" % f) if f else None


def minimal_cert(rows, n, maxk=3):
    for k in range(1, maxk + 1):
        for S in combinations(range(len(rows)), k):
            r = [rows[i] for i in S]
            v = kills(r, n)
            if v:
                return k, [(list(rows[i][0]), [str(z) for z in rows[i][1]],
                            str(rows[i][2])) for i in S], v
    return None, None, None


def main():
    out = {"_header": "UNAUDITED W24 minimal kill certificates."}
    recs = []
    for m, tag, bl in P.stored_points():
        iso, live = ID.isolating_words(m)
        rec = dict(m=m, tag=tag, certs={})
        for i in (0, 1, 2, 3):
            grp = {}
            for x, can in iso[i]:
                grp.setdefault(can, []).append(x)
            for can, xs in grp.items():
                rows = sub_rows(m, bl, xs, list(can))
                if rows is None:
                    continue
                n = len(can)
                k, cert, kind = minimal_cert(rows, n, maxk=2)
                lab = "%d|%s" % (i, ",".join(str(e) for e in can))
                rec["certs"][lab] = dict(size=k, kind=kind,
                                         words=[c[0] for c in cert] if cert
                                         else None)
        recs.append(rec)
        print("m=%d %-26s %s" % (m, tag[:26],
                                 {k: (v["size"], v["kind"], v["words"])
                                  for k, v in rec["certs"].items()}),
              flush=True)
    out["records"] = recs
    json.dump(out, open(os.path.join(HERE, "results_cert.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
