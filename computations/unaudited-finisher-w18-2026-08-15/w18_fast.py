#!/usr/bin/env python3
"""UNAUDITED PROBE (W18) -- vectorised search for Lemma W18-A kills.

Pinned HEAD: see PINNED_HEAD.txt.  Probe output; not a proved project claim.

Same lemma as w18_kill.find_kill_A, but (a) with the general SPLIT test
("no supported perfect matching of B at w uses a crossing edge", which is the
real hypothesis; the star condition on the active crossing edges is only a
sufficient special case) and (b) organised so that the whole search is a
handful of numpy reductions per template.

The search space is pruned by an exact observation, not by a heuristic:

    for a zero-singleton template the (P1, P1) combination can never fire,
    because a split word with a unique supported matching on each side has a
    fibre of size 1, i.e. it IS a singleton.

so every kill must use (P2) -- a constant word that is split for the cut -- on
at least one side.  Moreover a (P2, P1) kill needs the (P2) side to have at
least TWO supported matchings at its constant sub-word (otherwise the
contradiction word is again a singleton), which is impossible on a two-site
side.  Both facts are re-derived in `find` and used only to skip work.

Every kill this module reports is handed to w18_kill.verify_certificate, which
re-proves it from scratch; this module is a search accelerator, not an oracle.
"""

from __future__ import annotations

from itertools import combinations, product

import numpy as np

import w18_core as C
import w18_kill as K

_WORDS = np.array(C.WORDS, dtype=np.int8)
_CELLIDX = np.zeros((C.NE, len(C.WORDS)), dtype=np.int64)
for _e, (_u, _v) in enumerate(C.EDGES):
    _CELLIDX[_e] = 3 * _WORDS[:, _u].astype(np.int64) + _WORDS[:, _v]
_MIXED = np.array([len(set(w)) > 1 for w in C.WORDS], dtype=bool)
_PMEDGES = np.array(C.PM_EIDX, dtype=np.int64)                # (105, 4)


class Side:
    """Sub-word bookkeeping for one subset of the sites."""

    def __init__(self, sites):
        self.sites = tuple(sorted(sites))
        k = len(self.sites)
        self.subwords = np.array(list(product(range(3), repeat=k)),
                                 dtype=np.int8)                 # (3^k, k)
        self.n = len(self.subwords)
        self.pms = C._pms(self.sites)
        self.pm_cells = []          # per PM: list of (edge, cellindex array)
        for pm in self.pms:
            row = []
            for (u, v) in pm:
                e = C.EIDX[(u, v)]
                iu = self.sites.index(u)
                iv = self.sites.index(v)
                row.append((e, 3 * self.subwords[:, iu].astype(np.int64)
                            + self.subwords[:, iv]))
            self.pm_cells.append(row)
        # sub-word index -> full word index, when the complement is constant c
        self.fullidx = []
        for c in range(3):
            full = np.full((self.n, C.N), c, dtype=np.int8)
            for a, p in enumerate(self.sites):
                full[:, p] = self.subwords[:, a]
            idx = np.zeros(self.n, dtype=np.int64)
            for p in range(C.N):
                idx = idx * 3 + full[:, p]
            self.fullidx.append(idx)
        self.const_index = [int(np.ravel_multi_index(
            tuple([c] * k), (3,) * k)) for c in range(3)]

    def pm_counts(self, occ):
        out = np.zeros(self.n, dtype=np.int16)
        for row in self.pm_cells:
            acc = np.ones(self.n, dtype=bool)
            for (e, cellidx) in row:
                acc &= occ[e][cellidx]
            out += acc
        return out


_SIDES = {}


def side(sites):
    key = tuple(sorted(sites))
    if key not in _SIDES:
        _SIDES[key] = Side(key)
    return _SIDES[key]


class Cut:
    def __init__(self, L, R):
        self.L = tuple(sorted(L))
        self.R = tuple(sorted(R))
        self.sideL = side(self.L)
        self.sideR = side(self.R)
        inL = [p in set(self.L) for p in range(C.N)]
        self.cross_edges = [e for e, (u, v) in enumerate(C.EDGES)
                            if inL[u] != inL[v]]
        cs = set(self.cross_edges)
        self.crossing_pms = np.array(
            [n for n, M in enumerate(C.PM_EIDX) if cs & set(M)], dtype=np.int64)
        # pairidx[iu, iy] = index of the full word with sub-word iu on L, iy on R
        a = np.zeros(self.sideL.n, dtype=np.int64)
        for k, p in enumerate(self.sideL.sites):
            a += self.sideL.subwords[:, k].astype(np.int64) * 3 ** (C.N - 1 - p)
        b = np.zeros(self.sideR.n, dtype=np.int64)
        for k, p in enumerate(self.sideR.sites):
            b += self.sideR.subwords[:, k].astype(np.int64) * 3 ** (C.N - 1 - p)
        self.pairidx = a[:, None] + b[None, :]


CUTS = [Cut(L, R) for (L, R) in K.even_cuts()]
CONST_WORD_IDX = [C.WIDX[(c,) * C.N] for c in range(3)]


def occupancy(T):
    occ = np.zeros((C.NE, 9), dtype=bool)
    for e, mask in enumerate(T):
        for k in range(9):
            if (mask >> k) & 1:
                occ[e, k] = True
    return occ


def support_matrix(occ):
    """(105, 6561) bool: is matching n supported at word w?"""
    per = np.empty((C.NE, len(C.WORDS)), dtype=bool)
    for e in range(C.NE):
        per[e] = occ[e][_CELLIDX[e]]
    out = np.empty((len(C.PM_EIDX), len(C.WORDS)), dtype=bool)
    for n, M in enumerate(C.PM_EIDX):
        out[n] = per[M[0]] & per[M[1]] & per[M[2]] & per[M[3]]
    return out


def find(T, compat=None):
    """First Lemma W18-A kill found, as (cut_L, cut_R, u, y, pinL, pinR)."""
    occ = occupancy(T)
    if compat is None:
        compat = support_matrix(occ)
    for cut in CUTS:
        if len(cut.crossing_pms) == 0:
            continue
        crossing_used = compat[cut.crossing_pms].any(axis=0)
        split = ~crossing_used
        cl = [c for c in range(3) if split[CONST_WORD_IDX[c]]]
        if not cl:
            continue                     # (P1,P1) cannot fire: see the header
        cntL = cut.sideL.pm_counts(occ)
        cntR = cut.sideR.pm_counts(occ)
        # (P2, P2)
        for c in cl:
            for cp in cl:
                if c == cp:
                    continue
                widx = int(cut.sideR.fullidx[c][cut.sideR.const_index[cp]])
                if split[widx] and _MIXED[widx]:
                    return (cut.L, cut.R, (c,) * len(cut.L),
                            (cp,) * len(cut.R), "P2", "P2")
        # (P2 on L, P1 on R)
        for c in cl:
            if cntL[cut.sideL.const_index[c]] < 2:
                continue
            cand = np.nonzero(cntR == 1)[0]
            if len(cand):
                widx = cut.sideR.fullidx[c][cand]
                good = np.nonzero(split[widx] & _MIXED[widx])[0]
                if len(good):
                    y = tuple(int(x) for x in cut.sideR.subwords[cand[good[0]]])
                    return (cut.L, cut.R, (c,) * len(cut.L), y, "P2", "P1")
        # (P1 on L, P2 on R)
        for c in cl:
            if cntR[cut.sideR.const_index[c]] < 2:
                continue
            cand = np.nonzero(cntL == 1)[0]
            if len(cand):
                widx = cut.sideL.fullidx[c][cand]
                good = np.nonzero(split[widx] & _MIXED[widx])[0]
                if len(good):
                    u = tuple(int(x) for x in cut.sideL.subwords[cand[good[0]]])
                    return (cut.L, cut.R, u, (c,) * len(cut.R), "P1", "P2")
    return None


def certificate(T, hit):
    """Turn a `find` hit into a full Lemma W18-A certificate with a reason."""
    L, R, u, y, pinL, pinR = hit
    cross = K.crossing_edges(L, R)
    w = K.join(L, R, u, y)
    reason = []
    reason += K.split_reason(T, w, L, R)
    for tag, sites, sub, kind in (("L", L, u, pinL), ("R", R, y, pinR)):
        if kind == "P1":
            r = K.p1_reason(T, sites, sub)
            assert r is not None, "P1 reason failed"
            reason += r
        else:
            reason += K.split_reason(T, (sub[0],) * C.N, L, R)
    return {"lemma": "W18-A", "cut_L": list(L), "cut_R": list(R),
            "word": list(w), "u": list(u), "y": list(y),
            "pinL": pinL, "pinR": pinR, "reason": K._dedupe(reason)}
