#!/usr/bin/env python3
"""A12 -- independent audit engine for lane W36 round 2.  UNAUDITED.

FROM SCRATCH.  Standard library only.  ZERO imports from w26/w30/w36/a11
code.  The only inputs taken from the repository are the 28-entry template
masks, which are committed (computations/verify_slice_master_relations.py,
frozen SHA 8b8385c1...), re-typed here by hand and cross-checked against the
committed structural census (Gamma degrees, Gamma perfect-matching counts).

Everything else -- Phi by raw 105-matching enumeration, the decomposition
(1), the cofactor hafnians, live singles, clean words, admissible index
choices, the ROWS matrix of the master relation (M), the augmented slice
S'(tau), the DELIVERS predicate -- is re-derived here.

Exact arithmetic only: Fraction over Q, int mod p over F_p.
"""
from __future__ import annotations

import sys
from fractions import Fraction
from itertools import combinations, product

sys.dont_write_bytecode = True

N = 8
FULL = 511
EDGES = tuple(combinations(range(N), 2))
EIDX = {e: i for i, e in enumerate(EDGES)}
LSIDE = (0, 1, 2, 3)
RSIDE = (4, 5, 6, 7)
SIG = {0: 7, 1: 4, 2: 5, 3: 6}
SIGINV = {v: k for k, v in SIG.items()}

# 28-entry masks, re-typed from the committed checker.  511 = Gamma edge,
# 0 = absent, 2^c = single at cell (c//3, c%3).
MASKS = {
    25: (511, 511, 511, 1, 2, 4, 511, 511, 511, 511, 8, 16, 4, 511,
         8, 511, 128, 32, 64, 128, 0, 256, 511, 0, 511, 511, 0, 511),
    26: (511, 511, 511, 1, 2, 4, 511, 511, 511, 511, 8, 16, 4, 511,
         8, 511, 128, 32, 64, 128, 511, 256, 511, 0, 511, 511, 0, 511),
    27: (511, 511, 511, 1, 2, 4, 511, 511, 511, 511, 8, 16, 4, 511,
         8, 511, 128, 32, 64, 128, 511, 256, 511, 511, 511, 511, 0, 511),
    28: (511, 511, 511, 1, 2, 4, 511, 511, 511, 511, 8, 16, 4, 511,
         8, 511, 128, 32, 64, 128, 511, 256, 511, 511, 511, 511, 511, 511),
}


# ------------------------------------------------------------------ fields
class Rat:
    p = 0
    zero = Fraction(0)
    one = Fraction(1)

    @staticmethod
    def of(x):
        return Fraction(x)

    @staticmethod
    def iszero(x):
        return x == 0

    @staticmethod
    def inv(x):
        return Fraction(1) / x

    @staticmethod
    def name():
        return 'Q'


class Fp:
    def __init__(self, p):
        self.p = p
        self.zero = 0
        self.one = 1 % p

    def of(self, x):
        return int(x) % self.p

    def iszero(self, x):
        return x % self.p == 0

    def inv(self, x):
        return pow(int(x) % self.p, self.p - 2, self.p)

    def name(self):
        return str(self.p)


def K_of(fld):
    return Rat if str(fld) in ('Q', '0') else Fp(int(fld))


def norm(K, x):
    return x % K.p if K.p else x


# ---------------------------------------------------- perfect matchings
def _pms(vs):
    if not vs:
        return [()]
    a, rest = vs[0], vs[1:]
    out = []
    for i, b in enumerate(rest):
        for mm in _pms(rest[:i] + rest[i + 1:]):
            out.append(((a, b),) + mm)
    return out


PMS = tuple(tuple(sorted(m)) for m in _pms(tuple(range(N))))
assert len(PMS) == 105
WORDS = tuple(product(range(3), repeat=N))
MIXED = tuple(w for w in WORDS if len(set(w)) > 1)
assert len(MIXED) == 6558


# ------------------------------------------------------------- structure
class Tmpl:
    """all combinatorics of one support, computed here."""

    def __init__(self, m):
        self.m = m
        msk = MASKS[m]
        self.gamma = frozenset(EDGES[i] for i, t in enumerate(msk)
                               if t == FULL)
        sing = {}
        for i, t in enumerate(msk):
            if t in (0, FULL):
                continue
            cs = [c for c in range(9) if (t >> c) & 1]
            if len(cs) != 1:
                raise ValueError("bad mask %r at %r" % (t, EDGES[i]))
            sing[EDGES[i]] = (cs[0] // 3, cs[0] % 3)
        self.singles = sing
        self.absent = frozenset(EDGES[i] for i, t in enumerate(msk) if t == 0)
        self.nbr = {v: tuple(sorted(u for u in range(N)
                                    if self._ed(u, v) in self.gamma))
                    for v in range(N)}
        self.deg = tuple(len(self.nbr[v]) for v in range(N))
        self.gamma_pms = tuple(M for M in PMS
                               if all(e in self.gamma for e in M))
        self.live = tuple(sorted(e for e in sing
                                 if self._has_pm(tuple(v for v in range(N)
                                                       if v not in e))))
        self.liveset = frozenset(self.live)
        self.clean_words = tuple(w for w in MIXED if not self.fired(w))

    @staticmethod
    def _ed(u, v):
        return (u, v) if u < v else (v, u)

    def _has_pm(self, verts):
        verts = tuple(sorted(verts))
        if not verts:
            return True
        a = verts[0]
        for i in range(1, len(verts)):
            b = verts[i]
            if self._ed(a, b) in self.gamma and \
               self._has_pm(verts[1:i] + verts[i + 1:]):
                return True
        return False

    def active(self, w):
        """the LIVE singles active at word w."""
        return tuple(e for e in self.live
                     if w[e[0]] == self.singles[e][0]
                     and w[e[1]] == self.singles[e][1])

    def fired(self, w):
        return bool(self.active(w))

    def cell(self, bl, u, v, a, b, K):
        e = self._ed(u, v)
        if e not in self.gamma:
            return K.zero
        return bl[e][a][b] if u < v else bl[e][b][a]

    # ------------------------------------------------------------ hafnians
    def phi_raw(self, bl, w, K):
        """z-free part of H_w by RAW enumeration of the 105 matchings."""
        tot = K.zero
        for M in PMS:
            pr = K.one
            for (u, v) in M:
                if (u, v) not in self.gamma:
                    pr = K.zero
                    break
                pr = norm(K, pr * bl[(u, v)][w[u]][w[v]])
            tot = norm(K, tot + pr)
        return tot

    def phi(self, bl, w, K):
        """same value as phi_raw, summing only over the matchings that lie
        inside Gamma (the others contribute 0).  Calibrated against phi_raw
        and against the decomposition (1) in a12_t0."""
        tot = K.zero
        for M in self.gamma_pms:
            pr = K.one
            for (u, v) in M:
                pr = norm(K, pr * bl[(u, v)][w[u]][w[v]])
            tot = norm(K, tot + pr)
        return tot

    def haf_on(self, bl, verts, w, K):
        """Gamma-hafnian restricted to `verts`."""
        verts = tuple(sorted(verts))
        if not verts:
            return K.one
        a = verts[0]
        tot = K.zero
        for i in range(1, len(verts)):
            b = verts[i]
            e = self._ed(a, b)
            if e not in self.gamma:
                continue
            c = bl[e][w[e[0]]][w[e[1]]]
            tot = norm(K, tot + norm(K, c * self.haf_on(
                bl, verts[1:i] + verts[i + 1:], w, K)))
        return tot

    def phi_decomp(self, bl, w, K):
        """Phi by the sigma-count decomposition (1) of the committed spine."""
        x, y = w[:4], w[4:]

        def cl(u, v, a, b):
            return self.cell(bl, u, v, a, b, K)

        ll = {(a, b): cl(a, b, x[a], x[b])
              for a, b in combinations(range(4), 2)}
        rr = {(a, b): cl(a, b, y[a - 4], y[b - 4])
              for a, b in combinations(range(4, 8), 2)}
        d = {a: cl(a, SIG[a], x[a], y[SIG[a] - 4]) for a in range(4)}
        hL = norm(K, ll[(0, 1)] * ll[(2, 3)] + ll[(0, 2)] * ll[(1, 3)]
                  + ll[(0, 3)] * ll[(1, 2)])
        hR = norm(K, rr[(4, 5)] * rr[(6, 7)] + rr[(4, 6)] * rr[(5, 7)]
                  + rr[(4, 7)] * rr[(5, 6)])
        tot = norm(K, hL * hR)
        for i, j in combinations(range(4), 2):
            p, q = [t for t in range(4) if t not in (i, j)]
            si, sj = min(SIG[i], SIG[j]), max(SIG[i], SIG[j])
            tot = norm(K, tot + norm(K, ll[(i, j)] * rr[(si, sj)]
                                     * d[p] * d[q]))
        return norm(K, tot + d[0] * d[1] * d[2] * d[3])

    def hafL(self, bl, x, K):
        c = self.cell
        return norm(K, c(bl, 0, 1, x[0], x[1], K) * c(bl, 2, 3, x[2], x[3], K)
                    + c(bl, 0, 2, x[0], x[2], K) * c(bl, 1, 3, x[1], x[3], K)
                    + c(bl, 0, 3, x[0], x[3], K) * c(bl, 1, 2, x[1], x[2], K))

    def hafR(self, bl, y, K):
        c = self.cell
        return norm(K, c(bl, 4, 5, y[0], y[1], K) * c(bl, 6, 7, y[2], y[3], K)
                    + c(bl, 4, 6, y[0], y[2], K) * c(bl, 5, 7, y[1], y[3], K)
                    + c(bl, 4, 7, y[0], y[3], K) * c(bl, 5, 6, y[1], y[2], K))

    def cofactorQ(self, bl, v, w, K):
        """Q(w)_j = haf_{Gamma - {v, s_j}}(w) for s_j in N(v), in order."""
        return [self.haf_on(bl, [u for u in range(N) if u not in (v, s)],
                            w, K) for s in self.nbr[v]]

    def Sprime(self, bl, v, tau, K):
        """S'(tau)[t][j] = A_{v,s_j}[t][tau_j], s_j in N(v) in order."""
        return [[self.cell(bl, v, s, t, tau[j], K)
                 for j, s in enumerate(self.nbr[v])] for t in range(3)]

    def tau_of(self, v, w):
        return tuple(w[s] for s in self.nbr[v])

    # ------------------------------------------------------- index choices
    def singles_at(self, kind, v):
        """live singles into v, as (edge, trigger site, trigger value,
        letter at v)."""
        out = []
        for e in self.live:
            a, b = self.singles[e]
            if kind == 'R' and e[1] == v:
                out.append((e, e[0], a, b))
            elif kind == 'L' and e[0] == v:
                out.append((e, e[1], b, a))
        return out

    def index_choices(self, kind, v):
        """ALL admissible index choices at vertex (kind, v).  An index choice
        is an assignment of letters to the seven sites != v.  T_f = letters
        at v at which some live single into v fires; T_c the rest.  Admissible
        iff T_f nonempty, every completion is a mixed word, the completions at
        T_c letters are CLEAN, and the completions at T_f letters have no
        active live single other than ones at v."""
        mine = self.singles_at(kind, v)
        out = []
        others = [c for c in range(N) if c != v]
        for vals in product(range(3), repeat=7):
            w = [0] * N
            for c, a in zip(others, vals):
                w[c] = a
            fire = {let for (e, trig, tv, let) in mine if w[trig] == tv}
            if not fire:
                continue
            ok = True
            for t in range(3):
                ww = tuple(w[:v] + [t] + w[v + 1:])
                if len(set(ww)) == 1:
                    ok = False
                    break
                act = self.active(ww)
                if t not in fire:
                    if act:
                        ok = False
                        break
                else:
                    if any((e[1] if kind == 'R' else e[0]) != v for e in act):
                        ok = False
                        break
            if ok:
                out.append((tuple(w), frozenset(fire)))
        return out

    # ------------------------------------------------ the ROWS of (M)/(M*)
    def rows_and_scale(self, bl, kind, v, w, K):
        """ROWS(t)[q] of the master relation, plus the scale.  For an R-site
        v with p = sigma^{-1}(v):
            ROW(t)[q] = d_p(t) * (d_q * l_ij) + hafL * r_{v, sigma q}(t)
        with {i,j} = L - {p,q}; q runs over L - {p}.  For an L-site the dual.
        Returns (ROWS, scale, ucoef, Mcols) or (None, 0, ..) if scale = 0."""
        x, y = w[:4], w[4:]
        c = self.cell
        if kind == 'R':
            sc = self.hafL(bl, x, K)
            p = SIGINV[v]
            dv = [c(bl, p, v, x[p], t, K) for t in range(3)]
            qs = [q for q in range(4) if q != p]
            uu, MM = [], [[None] * 3 for _ in range(3)]
            for jc, q in enumerate(qs):
                i, j = [t for t in range(4) if t not in (p, q)]
                lij = c(bl, i, j, x[i], x[j], K)
                dq = c(bl, q, SIG[q], x[q], y[SIG[q] - 4], K)
                uu.append(norm(K, dq * lij))
                s2 = SIG[q]
                for t in range(3):
                    MM[t][jc] = c(bl, v, s2, t, y[s2 - 4], K)
        else:
            sc = self.hafR(bl, y, K)
            p = v
            dv = [c(bl, p, SIG[p], s, y[SIG[p] - 4], K) for s in range(3)]
            qs = [a for a in range(4) if a != p]
            uu, MM = [], [[None] * 3 for _ in range(3)]
            for jc, a in enumerate(qs):
                b, cc = [t for t in range(4) if t not in (p, a)]
                rbc = c(bl, SIG[b], SIG[cc], y[SIG[b] - 4], y[SIG[cc] - 4], K)
                da = c(bl, a, SIG[a], x[a], y[SIG[a] - 4], K)
                uu.append(norm(K, da * rbc))
                for s in range(3):
                    MM[s][jc] = c(bl, p, a, s, x[a], K)
        if K.iszero(sc):
            return None, sc, uu, MM
        ROWS = [[norm(K, dv[t] * uu[j] + sc * MM[t][j]) for j in range(3)]
                for t in range(3)]
        return ROWS, sc, uu, MM

    def master_lhs_rhs(self, bl, kind, v, w, K):
        """(M): scale * Phi(w|v=t) =?= sum_q B_q ROW(t)[q].  Returns the two
        sides for t = 0,1,2 (own derivation of the B_q)."""
        x, y = w[:4], w[4:]
        c = self.cell
        if kind == 'R':
            sc = self.hafL(bl, x, K)
            p = SIGINV[v]
            qs = [q for q in range(4) if q != p]
            Bq = []
            for q in qs:
                i, j = [t for t in range(4) if t not in (p, q)]
                si, sj = min(SIG[i], SIG[j]), max(SIG[i], SIG[j])
                rij = c(bl, si, sj, y[si - 4], y[sj - 4], K)
                lpq = c(bl, p, q, x[p], x[q], K)
                di = c(bl, i, SIG[i], x[i], y[SIG[i] - 4], K)
                dj = c(bl, j, SIG[j], x[j], y[SIG[j] - 4], K)
                Bq.append(norm(K, sc * rij + lpq * di * dj))
        else:
            sc = self.hafR(bl, y, K)
            p = v
            qs = [a for a in range(4) if a != p]
            Bq = []
            for a in qs:
                b, cc = [t for t in range(4) if t not in (p, a)]
                lbc = c(bl, b, cc, x[b], x[cc], K)
                rpa = c(bl, SIG[p], SIG[a], y[SIG[p] - 4], y[SIG[a] - 4], K)
                db = c(bl, b, SIG[b], x[b], y[SIG[b] - 4], K)
                dc = c(bl, cc, SIG[cc], x[cc], y[SIG[cc] - 4], K)
                Bq.append(norm(K, sc * lbc + rpa * db * dc))
        R, sc2, uu, MM = self.rows_and_scale(bl, kind, v, w, K)
        if R is None:
            dv = ([c(bl, SIGINV[v], v, x[SIGINV[v]], t, K) for t in range(3)]
                  if kind == 'R'
                  else [c(bl, v, SIG[v], s, y[SIG[v] - 4], K)
                        for s in range(3)])
            R = [[norm(K, dv[t] * uu[j] + sc * MM[t][j]) for j in range(3)]
                 for t in range(3)]
        lhs, rhs = [], []
        for t in range(3):
            ww = tuple(w[:v] + (t,) + w[v + 1:])
            lhs.append(norm(K, sc * self.phi_raw(bl, ww, K)))
            rhs.append(norm(K, sum(norm(K, Bq[j] * R[t][j])
                                   for j in range(3))))
        return lhs, rhs

    # -------------------------------------------------------- the predicate
    def vertex_report(self, bl, kind, v, K, choices=None, detail=False):
        """EXHAUSTIVE delivery test at one vertex.  A choice SURVIVES iff its
        scale is nonzero; it DELIVERS iff ROW(t_f) lies in the span of the
        clean ROWS for every firing letter t_f."""
        idx = choices if choices is not None else self.index_choices(kind, v)
        n_idx = n_zero = n_del = 0
        det = []
        for (w, fire) in idx:
            R, sc, uu, MM = self.rows_and_scale(bl, kind, v, w, K)
            if R is None:
                n_zero += 1
                continue
            n_idx += 1
            cts = [t for t in range(3) if t not in fire]
            crows = [R[t] for t in cts]
            rc = rank(crows, K)
            ok = all(rank(crows + [R[t]], K) == rc for t in sorted(fire))
            if ok:
                n_del += 1
                if detail:
                    det.append((w, tuple(sorted(fire))))
        return dict(n_idx_total=len(idx), n_idx=n_idx, n_zero_scale=n_zero,
                    n_deliver=n_del, DELIVERS=n_del > 0, detail=det)

    # ---------------------------------------------------------- point tests
    def is_clean(self, bl, K):
        return all(K.iszero(self.phi(bl, w, K)) for w in self.clean_words)

    def all_nonzero(self, bl, K):
        return all(not K.iszero(bl[e][i][j]) for e in self.gamma
                   for i in range(3) for j in range(3))

    def n_phi_nonzero(self, bl, K):
        return sum(1 for w in WORDS if not K.iszero(self.phi(bl, w, K)))

    def off_stratum(self, bl, K):
        for w in WORDS:
            if not K.iszero(self.phi(bl, w, K)):
                return True
        return False


def rank(rows, K):
    if not rows:
        return 0
    M = [list(r) for r in rows]
    ncol = len(M[0])
    r = 0
    for c in range(ncol):
        sel = None
        for i in range(r, len(M)):
            if not K.iszero(M[i][c]):
                sel = i
                break
        if sel is None:
            continue
        M[r], M[sel] = M[sel], M[r]
        iv = K.inv(M[r][c])
        M[r] = [norm(K, z * iv) for z in M[r]]
        for i in range(len(M)):
            if i != r and not K.iszero(M[i][c]):
                f = M[i][c]
                M[i] = [norm(K, a - f * b) for a, b in zip(M[i], M[r])]
        r += 1
        if r == len(M):
            break
    return r


def kernel_basis(rows, K, n):
    M = [list(r) for r in rows] or [[K.zero] * n]
    piv = {}
    r = 0
    for c in range(n):
        sel = None
        for i in range(r, len(M)):
            if not K.iszero(M[i][c]):
                sel = i
                break
        if sel is None:
            continue
        M[r], M[sel] = M[sel], M[r]
        iv = K.inv(M[r][c])
        M[r] = [norm(K, z * iv) for z in M[r]]
        for i in range(len(M)):
            if i != r and not K.iszero(M[i][c]):
                f = M[i][c]
                M[i] = [norm(K, a - f * b) for a, b in zip(M[i], M[r])]
        piv[c] = r
        r += 1
    out = []
    for fc in [c for c in range(n) if c not in piv]:
        vec = [K.zero] * n
        vec[fc] = K.one
        for c, rr in piv.items():
            vec[c] = norm(K, -M[rr][fc])
        out.append(vec)
    return out


_T = {}


def T(m):
    if m not in _T:
        _T[m] = Tmpl(m)
    return _T[m]


# ------------------------------------------------------------------- IO
def _to_field(z, K):
    f = Fraction(z)
    if K.p == 0:
        return f
    den = f.denominator % K.p
    if den == 0:
        raise ValueError("denominator divisible by p")
    return (f.numerator % K.p) * pow(den, K.p - 2, K.p) % K.p


def load_point(ptj, K):
    out = {}
    for k, v in ptj.items():
        e = tuple(eval(k)) if isinstance(k, str) else tuple(k)
        out[e] = [[_to_field(z, K) for z in row] for row in v]
    return out


def dump_point(bl):
    return {str(k): [[str(z) for z in row] for row in v]
            for k, v in sorted(bl.items())}
