#!/usr/bin/env python3
"""adv2 -- the JACOBIAN / TANGENT SPACE of the solution variety.

UNAUDITED.  Exact integer arithmetic mod p (a HEURISTIC: the mod-p
tangent space can only be LARGER than the rational one when p divides a
minor, so a mod-p "dead" coordinate is genuinely dead over Q, while a
mod-p live coordinate still has to be realised exactly).

At a point with H_w = 0 for all mixed w, the tangent space is
   ker DH,   DH[w][cell of e=(u,v)] = [w hits that cell] * haf(M-u-v)(w)
             DH[w][z_e]             = [e active at w]   * haf(M-p-j)(w)
so a z-coordinate that is identically zero on ker DH cannot be switched
on by ANY first-order deformation of the point.
"""
from __future__ import annotations

import os
import random
import sys
from fractions import Fraction

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import a2lib as A                                                 # noqa: E402
import a2fp as FP                                                 # noqa: E402
import w26_core as C                                              # noqa: E402

F = Fraction


def to_fp_flat(m, bl, z, p):
    G = A.Geo(m)
    gam = list(G.gam)
    base = {e: 9 * k for k, e in enumerate(gam)}
    P = [0] * (9 * len(gam))
    for e in gam:
        for a in range(3):
            for b in range(3):
                x = Fraction(bl[e][a][b])
                P[base[e] + 3 * a + b] = (x.numerator
                                          * pow(x.denominator, p - 2, p)) % p
    zz = {}
    for e in G.live:
        x = Fraction(z.get(e, 0))
        zz[e] = (x.numerator * pow(x.denominator, p - 2, p)) % p
    return gam, base, P, zz


def hafM_p(m, gs, sing, P, base, zz, w, verts, p):
    if not verts:
        return 1
    a = verts[0]
    tot = 0
    for i in range(1, len(verts)):
        b = verts[i]
        e = (a, b) if a < b else (b, a)
        if e in gs:
            c = P[base[e] + 3 * w[e[0]] + w[e[1]]]
        elif e in sing and (w[e[0]], w[e[1]]) == sing[e]:
            c = zz.get(e, 0)
        else:
            continue
        if c == 0:
            continue
        tot += c * hafM_p(m, gs, sing, P, base, zz, w,
                          verts[1:i] + verts[i + 1:], p)
    return tot % p


def jac_rows(m, bl, z, p, words=None):
    """returns (colnames, rows) with rows = gradient of H_w."""
    G = A.Geo(m)
    gam, base, P, zz = to_fp_flat(m, bl, z, p)
    gs, sing = G.gs, G.sing
    live = list(G.live)
    ncell = 9 * len(gam)
    n = ncell + len(live)
    names = ["%s[%d][%d]" % (e, a, b) for e in gam
             for a in range(3) for b in range(3)] + \
            ["z%s" % (e,) for e in live]
    words = list(C.MIXED) if words is None else list(words)
    rows = []
    V = tuple(range(8))
    for w in words:
        r = [0] * n
        for e in gam:
            u, v = e
            K = hafM_p(m, gs, sing, P, base, zz, w,
                       tuple(x for x in V if x != u and x != v), p)
            if K:
                r[base[e] + 3 * w[u] + w[v]] = (r[base[e] + 3 * w[u]
                                                  + w[v]] + K) % p
        for i, e in enumerate(live):
            if (w[e[0]], w[e[1]]) != sing[e]:
                continue
            K = hafM_p(m, gs, sing, P, base, zz, w,
                       tuple(x for x in V if x not in e), p)
            r[ncell + i] = K % p
        if any(r):
            rows.append(r)
    return names, rows, n, ncell, live


def tangent(m, bl, z, p, sample=None, rng=None):
    """kernel of DH; returns (names, kerdim, dead-coordinate list)."""
    names, rows, n, ncell, live = jac_rows(m, bl, z, p)
    use = rows
    if sample and len(rows) > sample:
        rng = rng or random.Random(1)
        use = rng.sample(rows, sample)
    K = FP.kernel_p(use, n, p)
    # tighten against ALL rows
    for r in rows:
        if not K:
            break
        vals = [sum(r[i] * v[i] for i in range(n)) % p for v in K]
        if any(vals):
            j = next(i for i, x in enumerate(vals) if x)
            pv = pow(vals[j], p - 2, p)
            base = [(x * pv) % p for x in K[j]]
            K = [[(K[i][t] - vals[i] * base[t]) % p for t in range(n)]
                 for i in range(len(K)) if i != j]
    dead = [names[i] for i in range(n) if all(v[i] == 0 for v in K)]
    zlive = [str(live[i]) for i in range(len(live))
             if any(v[ncell + i] != 0 for v in K)]
    return dict(n_unknowns=n, n_rows=len(rows), ker_dim=len(K),
                n_dead=len(dead), z_live=zlive,
                z_dead=[str(e) for e in live if str(e) not in zlive],
                dead_cells=[d for d in dead if not d.startswith("z")][:20])
