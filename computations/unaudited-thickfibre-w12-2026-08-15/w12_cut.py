#!/usr/bin/env python3
"""UNAUDITED PROBE (W12) -- THE CUT EXTRACTION.  This is the mechanism that
beats W8's thick-fibre immunity.

    LEMMA W12-3 (cut extraction).  Let B = L u R with |L|, |R| both EVEN, and
    call a word w CLEAN (for this cut) if no T-supported perfect matching of B
    uses a crossing edge.  Because a supported matching using k crossing edges
    leaves |L| - k vertices of L to be matched inside L, k is always even; so
    w is clean as soon as the ACTIVE crossing edges on w (those whose cell
    (w_p,w_q) is occupied) contain no two vertex-disjoint edges.  For a clean
    word,

            F_w  =  F^L_{w|L} . F^R_{w|R},

    where F^L_u is the sum over perfect matchings of L supported on u.

    Say a sub-word u on L is PINNED if F^L_u is forced nonzero.  Two free
    sources of pinning:
        (P1) L has exactly ONE supported perfect matching at u -- then F^L_u
             is a single product of nonzero cells;
        (P2) u = c^L and the constant word c^B is clean -- then
             F^L_c . F^R_c = F_{c^B} != 0.
    Now for every PINNED u on L and every sub-word y on R with (u,y) clean and
    (u,y) MIXED, exactness forces

            F^R_y = 0.

    That is a value system on the R-cells ALONE.  Its fibres are perfect
    matchings of R, so for |R| = 4 they have at most THREE terms and very
    often two -- the binomial relations that the full thick-fibre system does
    not have.  THIS is why the cut beats the immunity proposition: thickness
    of the fibres of B says nothing about the fibres of R.

    KILL: the extracted R-system (equations F^R_y = 0, non-vanishing
    F^R_y != 0 for every PINNED y on R, all R-cells nonzero) is infeasible.
"""

from __future__ import annotations

from itertools import combinations, product

import w12_core as C


class HalfSystem:
    """The value system of a sub-site set: same interface as ValueSystem."""

    def __init__(self, geo, template, sites):
        self.geo = geo
        self.template = tuple(template)
        self.sites = tuple(sorted(sites))
        self.pms = C.perfect_matchings(self.sites)
        self.vars = []
        self.varindex = {}
        internal = [geo.eindex[e] for e in combinations(self.sites, 2)]
        for e in internal:
            for (i, j) in C.cells(template[e]):
                self.varindex[(e, i, j)] = len(self.vars)
                self.vars.append((e, i, j))
        self.nvars = len(self.vars)
        self.mixed_eqs = {}      # sub-word -> monomials  (must vanish)
        self.const_eqs = {}      # sub-word -> monomials  (must NOT vanish)

    def fibre(self, sub):
        """Monomials (tuples of variable indices) for the sub-word `sub`."""
        colour = dict(zip(self.sites, sub))
        out = []
        for pm in self.pms:
            mono = []
            ok = True
            for (u, v) in pm:
                e = self.geo.eindex[(u, v)]
                key = (e, colour[u], colour[v])
                if key not in self.varindex:
                    ok = False
                    break
                mono.append(self.varindex[key])
            if ok:
                out.append(tuple(sorted(mono)))
        out.sort()
        return out

    def add_zero(self, sub):
        mono = self.fibre(sub)
        if mono:
            self.mixed_eqs[tuple(sub)] = mono
        return len(mono)

    def add_nonzero(self, sub):
        mono = self.fibre(sub)
        self.const_eqs[tuple(sub)] = mono
        return len(mono)

    def evaluate(self, values, sub):
        total = 0
        for mono in (self.mixed_eqs.get(tuple(sub))
                     or self.const_eqs.get(tuple(sub)) or []):
            term = 1
            for v in mono:
                term *= values[v]
            total += term
        return total

    def varname(self, n):
        e, i, j = self.vars[n]
        u, v = self.geo.edges[e]
        return f"x_{u}{v}_{i}{j}"


def crossing_edges(geo, template, L):
    inL = [v in L for v in range(geo.size)]
    return [e for e, mask in enumerate(template)
            if mask and inL[geo.edges[e][0]] != inL[geo.edges[e][1]]]


def active_crossing_on(geo, template, word, cross):
    out = []
    for e in cross:
        u, v = geo.edges[e]
        if (template[e] >> (3 * word[u] + word[v])) & 1:
            out.append((u, v))
    return out


def no_two_disjoint(edges):
    for (a, b), (c, d) in combinations(edges, 2):
        if len({a, b, c, d}) == 4:
            return False
    return True


def clean(geo, template, word, L, cross):
    return no_two_disjoint(active_crossing_on(geo, template, word, cross))


def supported_pms(geo, template, sites, sub):
    colour = dict(zip(sorted(sites), sub))
    n = 0
    for pm in C.perfect_matchings(tuple(sorted(sites))):
        if all((template[geo.eindex[(u, v)]] >> (3 * colour[u] + colour[v])) & 1
               for (u, v) in pm):
            n += 1
    return n


def pinned_subwords(geo, template, sites, other, cross):
    """PINNED sub-words on `sites`: (P1) unique supported PM, or (P2) c^sites
    with the constant word c^B clean."""
    sites = tuple(sorted(sites))
    other = tuple(sorted(other))
    out = set()
    for sub in product(range(C.Q), repeat=len(sites)):
        if supported_pms(geo, template, sites, sub) == 1:
            out.add(sub)
    for c in range(C.Q):
        w = (c,) * geo.size
        if clean(geo, template, w, set(sites), cross):
            if C.fibre(geo, template, w):
                out.add((c,) * len(sites))
    return out


def extract(geo, template, L, R):
    """Build both extracted half-systems for the cut (L,R).

    Returns {'R': (HalfSystem, stats), 'L': (...)} with zero/nonzero words
    already installed."""
    cross = crossing_edges(geo, template, L)
    result = {}
    for tag, side, other in (("R", R, L), ("L", L, R)):
        side = tuple(sorted(side))
        other = tuple(sorted(other))
        pinned_other = pinned_subwords(geo, template, other, side, cross)
        hs = HalfSystem(geo, template, side)
        zeros = set()
        for u in pinned_other:
            for y in product(range(C.Q), repeat=len(side)):
                word = [0] * geo.size
                for k, v in enumerate(other):
                    word[v] = u[k]
                for k, v in enumerate(side):
                    word[v] = y[k]
                word = tuple(word)
                if not geo.is_mixed(word):
                    continue
                if clean(geo, template, word, set(L), cross):
                    zeros.add(y)
        pinned_side = pinned_subwords(geo, template, side, other, cross)
        for y in sorted(zeros):
            hs.add_zero(y)
        for y in sorted(pinned_side):
            hs.add_nonzero(y)
        stats = {"pinned_other": len(pinned_other),
                 "forced_zero_words": len(zeros),
                 "live_zero_equations": len(hs.mixed_eqs),
                 "pinned_side": len(pinned_side),
                 "nvars": hs.nvars,
                 "immediate_contradiction":
                     sorted(set(zeros) & set(pinned_side))}
        result[tag] = (hs, stats)
    return result


def even_cuts(size):
    seen = set()
    out = []
    for k in range(2, size - 1, 2):
        for L in combinations(range(size), k):
            Ls = frozenset(L)
            Rs = frozenset(range(size)) - Ls
            key = frozenset((Ls, Rs))
            if key in seen:
                continue
            seen.add(key)
            out.append((Ls, Rs))
    return out
