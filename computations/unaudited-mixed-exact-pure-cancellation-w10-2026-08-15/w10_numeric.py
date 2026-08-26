#!/usr/bin/env python3
"""W10 -- FLOAT SEARCH ONLY (explicitly labelled).  Nothing here decides
anything: every candidate produced here is re-verified in exact arithmetic by
the calling script before it is reported.

Vectorised residuals + ANALYTIC Jacobian for the N-site d-colour hafnian
system, so scipy.optimize.least_squares can be pointed at:
    * all mixed words          H_w = 0
    * chosen pure words        H_{c^N} = target_c
    * chosen "fibre anchors"   prod_{e in M} A_e[c][c] = 1
      (an anchor forces the colour-c pure FIBRE to be nonempty, since it makes
       every cell (c,c) along the matching M nonzero).

H_w = sum over perfect matchings M of prod_{uv in M} x[idx(uv, w_u, w_v)], so
with IDX[w] the (n_matchings, N/2) index array,
    H  = x[IDX].prod(axis=2).sum(axis=1)
    dH/dx_k = sum over (M,p) with IDX[w,M,p]==k of the leave-one-out product.
"""
from __future__ import annotations

from itertools import combinations, product

import numpy as np


def _pm(vertices):
    if not vertices:
        return ((),)
    head = vertices[0]
    out = []
    for i in range(1, len(vertices)):
        rest = vertices[1:i] + vertices[i + 1:]
        for tail in _pm(rest):
            out.append(((head, vertices[i]),) + tail)
    return tuple(out)


class System:
    """Only words with a NONEMPTY template fibre are kept: the others are
    identically zero and carry no information."""

    def __init__(self, N, d=3, template=None):
        self.N = N
        self.d = d
        self.half = N // 2
        self.edges = tuple(combinations(range(N), 2))
        self.matchings = _pm(tuple(range(N)))
        if template is None:
            template = {e: frozenset((i, j) for i in range(d) for j in range(d))
                        for e in self.edges}
        self.template = template
        self.vars = []
        self.vidx = {}
        for e in self.edges:
            for (i, j) in sorted(template[e]):
                self.vidx[(e, i, j)] = len(self.vars)
                self.vars.append((e, i, j))
        self.nv = len(self.vars)

        def rows_for(w):
            rows = []
            for M in self.matchings:
                idx = []
                ok = True
                for (u, v) in M:
                    key = ((u, v), w[u], w[v])
                    if key not in self.vidx:
                        ok = False
                        break
                    idx.append(self.vidx[key])
                if ok:
                    rows.append(idx)
            return rows

        self.mixed = []
        mixed_rows = []
        for w in product(range(d), repeat=N):
            if len(set(w)) == 1:
                continue
            r = rows_for(w)
            if r:
                self.mixed.append(w)
                mixed_rows.append(r)
        self.mixed_idx = _pack(mixed_rows, self.half)
        self.pure_rows = {c: rows_for((c,) * N) for c in range(d)}

    # ---------------------------------------------------------------- eval
    def _hafs(self, x, packed):
        idx, mask = packed
        if idx.shape[0] == 0:
            return np.zeros(0), None
        vals = np.where(mask, x[idx], 1.0)
        prods = vals.prod(axis=2)
        prods = np.where(mask.any(axis=2), prods, 0.0)
        return prods.sum(axis=1), (idx, mask, vals, prods)

    def residual(self, x, pure_targets=None, anchors=()):
        parts = [self._hafs(x, self.mixed_idx)[0]]
        if pure_targets:
            for c in sorted(pure_targets):
                h = 0.0
                for row in self.pure_rows[c]:
                    p = 1.0
                    for k in row:
                        p *= x[k]
                    h += p
                parts.append(np.array([h - pure_targets[c]]))
        for (c, M) in anchors:
            p = 1.0
            for (u, v) in M:
                p *= x[self.vidx[((u, v), c, c)]]
            parts.append(np.array([p - 1.0]))
        return np.concatenate(parts)

    def jacobian(self, x, pure_targets=None, anchors=()):
        idx, mask = self.mixed_idx
        nrow = idx.shape[0]
        extra = (len(pure_targets) if pure_targets else 0) + len(anchors)
        J = np.zeros((nrow + extra, self.nv))
        vals = np.where(mask, x[idx], 1.0)
        for p in range(self.half):
            loo = np.ones_like(vals[:, :, 0])
            for q in range(self.half):
                if q != p:
                    loo = loo * vals[:, :, q]
            loo = np.where(mask[:, :, p], loo, 0.0)
            rows = np.repeat(np.arange(nrow)[:, None], idx.shape[1], axis=1)
            np.add.at(J, (rows.ravel(), idx[:, :, p].ravel()), loo.ravel())
        r = nrow
        if pure_targets:
            for c in sorted(pure_targets):
                for row in self.pure_rows[c]:
                    for a, k in enumerate(row):
                        pr = 1.0
                        for b, k2 in enumerate(row):
                            if b != a:
                                pr *= x[k2]
                        J[r, k] += pr
                r += 1
        for (c, M) in anchors:
            ks = [self.vidx[((u, v), c, c)] for (u, v) in M]
            for a, k in enumerate(ks):
                pr = 1.0
                for b, k2 in enumerate(ks):
                    if b != a:
                        pr *= x[k2]
                J[r, k] += pr
            r += 1
        return J


def _pack(rows_list, half):
    """(n_words, max_matchings, half) index array + validity mask."""
    if not rows_list:
        return (np.zeros((0, 1, half), dtype=np.int64),
                np.zeros((0, 1, half), dtype=bool))
    width = max(len(r) for r in rows_list)
    idx = np.zeros((len(rows_list), width, half), dtype=np.int64)
    mask = np.zeros((len(rows_list), width, half), dtype=bool)
    for n, rows in enumerate(rows_list):
        for k, row in enumerate(rows):
            idx[n, k] = row
            mask[n, k] = True
    return idx, mask
