#!/usr/bin/env python3
"""A11 -- independent adversarial audit of W30's post-A10 additions.

UNAUDITED AUDIT LANE.  Nothing here is a proved claim of the repository.
Pinned repository HEAD: see PINNED_HEAD.txt.

FROM SCRATCH.  Standard library only.  ZERO imports from any w26_*/w30_*/
a10_* module.  The only thing taken from outside is (i) the nine 28-entry
template masks, which are combinatorial DATA embedded below and re-derived
against the census independently, and (ii) stored point corpora, read as
JSON DATA.

Every definition below is written from the COMMITTED spine document
`proofs/slice-master-relations.md` (dependency SLICE-MASTER):

  * the model and Phi                        -> spine (0)
  * the sigma-count decomposition            -> spine (1), Lemma 1.1
  * the master relation (M) / (M*)           -> spine Thm 2.1 / 2.2
  * the augmented slice matrix S'            -> spine Def 3.1
  * the cofactor vector Q and identity (C)   -> spine Thm 4.1
  * the delivery predicate FAIL_primary      -> spine 5.0

House rule: every check goes through the raising `need()`, never a bare
`assert`, so `python3 -O` cannot strip it.
"""
from __future__ import annotations

import json
import os
import random
from fractions import Fraction
from itertools import combinations, product

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))


class A11Error(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise A11Error(msg)
    return True


# ------------------------------------------------------------------- model
NSITE = 8
ALPHA = 3
FULLMASK = 511
EDGES = tuple(combinations(range(NSITE), 2))
LS = (0, 1, 2, 3)
RS = (4, 5, 6, 7)
SIG = {0: 7, 1: 4, 2: 5, 3: 6}
SIGINV = {v: k for k, v in SIG.items()}

# The nine 28-entry template masks (combinatorial data; identical copies live
# in the committed checker computations/verify_slice_master_relations.py and
# in eight lane engines).  511 = Gamma edge, 0 = absent, one-bit = a single.
TMPL = {
    25: (511, 511, 511, 1, 2, 4, 511, 511, 511, 511, 8, 16, 4, 511,
         8, 511, 128, 32, 64, 128, 0, 256, 511, 0, 511, 511, 0, 511),
    26: (511, 511, 511, 1, 2, 4, 511, 511, 511, 511, 8, 16, 4, 511,
         8, 511, 128, 32, 64, 128, 511, 256, 511, 0, 511, 511, 0, 511),
    27: (511, 511, 511, 1, 2, 4, 511, 511, 511, 511, 8, 16, 4, 511,
         8, 511, 128, 32, 64, 128, 511, 256, 511, 511, 511, 511, 0, 511),
    28: (511, 511, 511, 1, 2, 4, 511, 511, 511, 511, 8, 16, 4, 511,
         8, 511, 128, 32, 64, 128, 511, 256, 511, 511, 511, 511, 511, 511),
}

VLAB = ("R4", "R5", "R6", "R7", "L0", "L1", "L2", "L3")


def vsplit(lab):
    return lab[0], int(lab[1:])


def matchings(vs):
    """every perfect matching of the complete graph on the tuple vs"""
    if not vs:
        yield ()
        return
    head, rest = vs[0], vs[1:]
    for i in range(len(rest)):
        e = (head, rest[i]) if head < rest[i] else (rest[i], head)
        for tail in matchings(rest[:i] + rest[i + 1:]):
            yield (e,) + tail


PM_ALL = tuple(matchings(tuple(range(NSITE))))
WORDS = tuple(product(range(ALPHA), repeat=NSITE))
MIXED = tuple(w for w in WORDS if len(set(w)) > 1)


class Tmpl(object):
    """template combinatorics rebuilt from the mask tuple alone"""

    def __init__(self, m):
        msk = TMPL[m]
        need(len(msk) == 28, "mask length")
        self.m = m
        self.gamma = frozenset(e for e, t in zip(EDGES, msk) if t == FULLMASK)
        self.absent = frozenset(e for e, t in zip(EDGES, msk) if t == 0)
        self.single = {}
        for e, t in zip(EDGES, msk):
            if t in (0, FULLMASK):
                continue
            bits = [i for i in range(9) if (t >> i) & 1]
            need(len(bits) == 1, "single mask %s not one bit" % (e,))
            self.single[e] = (bits[0] // 3, bits[0] % 3)
        need(len(self.gamma) + len(self.absent) + len(self.single) == 28,
             "partition")
        self.live = frozenset(
            e for e in self.single
            if self._gamma_pm_exists(tuple(v for v in range(NSITE)
                                           if v not in e)))
        self.gamma_pms = tuple(M for M in PM_ALL
                               if all(e in self.gamma for e in M))
        self.nbr = {v: tuple(s for s in range(NSITE)
                             if (min(s, v), max(s, v)) in self.gamma)
                    for v in range(NSITE)}
        self.clean_words = tuple(w for w in MIXED if not self.fired(w))

    def _gamma_pm_exists(self, vs):
        if not vs:
            return True
        a, rest = vs[0], vs[1:]
        for i in range(len(rest)):
            e = (a, rest[i]) if a < rest[i] else (rest[i], a)
            if e in self.gamma and self._gamma_pm_exists(
                    rest[:i] + rest[i + 1:]):
                return True
        return False

    def fired(self, w):
        """the LIVE singles active on w"""
        return tuple(e for e in sorted(self.live)
                     if (w[e[0]], w[e[1]]) == self.single[e])

    def deg(self, v):
        return len(self.nbr[v])


_T = {}


def T(m):
    if m not in _T:
        _T[m] = Tmpl(m)
    return _T[m]


# ------------------------------------------------------------------- fields
class Rat(object):
    tag = "Q"
    p = 0
    zero = Fraction(0)
    one = Fraction(1)

    @staticmethod
    def of(a):
        return Fraction(a)

    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def sub(a, b):
        return a - b

    @staticmethod
    def mul(a, b):
        return a * b

    @staticmethod
    def iszero(a):
        return a == 0

    @staticmethod
    def inv(a):
        return 1 / a


class Modp(object):
    def __init__(self, p):
        self.p = p
        self.tag = "F_%d" % p
        self.zero = 0
        self.one = 1 % p

    def of(self, a):
        if isinstance(a, Fraction):
            return (a.numerator % self.p) * pow(a.denominator, -1,
                                                self.p) % self.p
        return int(a) % self.p

    def add(self, a, b):
        return (a + b) % self.p

    def sub(self, a, b):
        return (a - b) % self.p

    def mul(self, a, b):
        return (a * b) % self.p

    def iszero(self, a):
        return a % self.p == 0

    def inv(self, a):
        return pow(a, -1, self.p)


# ------------------------------------------------------- linear algebra
def rank(rows, K):
    """rank by fraction-free-ish Gaussian elimination over a field"""
    mat = [list(r) for r in rows]
    if not mat:
        return 0
    nc = len(mat[0])
    r = 0
    for c in range(nc):
        piv = None
        for i in range(r, len(mat)):
            if not K.iszero(mat[i][c]):
                piv = i
                break
        if piv is None:
            continue
        mat[r], mat[piv] = mat[piv], mat[r]
        iv = K.inv(mat[r][c])
        mat[r] = [K.mul(x, iv) for x in mat[r]]
        for i in range(len(mat)):
            if i != r and not K.iszero(mat[i][c]):
                f = mat[i][c]
                mat[i] = [K.sub(x, K.mul(f, y)) for x, y in zip(mat[i], mat[r])]
        r += 1
        if r == len(mat):
            break
    return r


def in_span(vec, basis, K):
    return rank(list(basis) + [list(vec)], K) == rank(list(basis), K)


# ------------------------------------------------------------ point access
def cell(bl, tm, u, v, a, b, K):
    """A_{uv}[a][b] with the spine convention: 0 off Gamma."""
    if u > v:
        u, v, a, b = v, u, b, a
    if (u, v) not in tm.gamma:
        return K.zero
    return bl[(u, v)][a][b]


def phi_raw(tm, bl, w, K):
    """Phi(w) by RAW enumeration of the 105 perfect matchings of K_8
    (spine (0)); a matching contributes 0 unless every edge is a Gamma edge."""
    tot = K.zero
    for M in PM_ALL:
        pr = K.one
        ok = True
        for (u, v) in M:
            if (u, v) not in tm.gamma:
                ok = False
                break
            pr = K.mul(pr, bl[(u, v)][w[u]][w[v]])
        if ok:
            tot = K.add(tot, pr)
    return tot


def phi_gpm(tm, bl, w, K):
    """Phi(w) summed over the PRE-FILTERED Gamma perfect matchings.  Same
    number as phi_raw; used only in bulk loops and always cross-checked
    against phi_raw by a control in the calling script."""
    tot = K.zero
    for M in tm.gamma_pms:
        pr = K.one
        for (u, v) in M:
            pr = K.mul(pr, bl[(u, v)][w[u]][w[v]])
        tot = K.add(tot, pr)
    return tot


def phi_decomp(tm, bl, w, K):
    """Phi(w) by the sigma-count decomposition, spine (1)."""
    def c(u, v):
        return cell(bl, tm, u, v, w[u], w[v], K)
    ll = {(i, j): c(i, j) for i, j in combinations(LS, 2)}
    rr = {(a, b): c(a, b) for a, b in combinations(RS, 2)}
    dd = {i: c(i, SIG[i]) for i in LS}
    hafl = K.add(K.add(K.mul(ll[(0, 1)], ll[(2, 3)]),
                       K.mul(ll[(0, 2)], ll[(1, 3)])),
                 K.mul(ll[(0, 3)], ll[(1, 2)]))
    hafr = K.add(K.add(K.mul(rr[(4, 5)], rr[(6, 7)]),
                       K.mul(rr[(4, 6)], rr[(5, 7)])),
                 K.mul(rr[(4, 7)], rr[(5, 6)]))
    tot = K.mul(hafl, hafr)
    for i, j in combinations(LS, 2):
        p, q = [t for t in LS if t not in (i, j)]
        si, sj = min(SIG[i], SIG[j]), max(SIG[i], SIG[j])
        tot = K.add(tot, K.mul(ll[(i, j)],
                               K.mul(rr[(si, sj)], K.mul(dd[p], dd[q]))))
    tot = K.add(tot, K.mul(K.mul(dd[0], dd[1]), K.mul(dd[2], dd[3])))
    return tot


def hafL(tm, bl, x, K):
    def c(u, v):
        return cell(bl, tm, u, v, x[u], x[v], K)
    return K.add(K.add(K.mul(c(0, 1), c(2, 3)), K.mul(c(0, 2), c(1, 3))),
                 K.mul(c(0, 3), c(1, 2)))


def hafR(tm, bl, w, K):
    def c(u, v):
        return cell(bl, tm, u, v, w[u], w[v], K)
    return K.add(K.add(K.mul(c(4, 5), c(6, 7)), K.mul(c(4, 6), c(5, 7))),
                 K.mul(c(4, 7), c(5, 6)))


# -------------------------------------------------- the master relation (M)
def master_rows(tm, bl, kind, v, w, K):
    """ROWS[t][idx] of spine Thm 2.1 (R-site) / 2.2 (L-site), together with
    the coefficient vector B (resp X) and the scale.  w[v] is ignored."""
    def c(u, uu, a, b):
        return cell(bl, tm, u, uu, a, b, K)

    ll = {(i, j): c(i, j, w[i], w[j]) for i, j in combinations(LS, 2)}
    rr = {(a, b): c(a, b, w[a], w[b]) for a, b in combinations(RS, 2)}
    dd = {i: c(i, SIG[i], w[i], w[SIG[i]]) for i in LS}
    hl = K.add(K.add(K.mul(ll[(0, 1)], ll[(2, 3)]),
                     K.mul(ll[(0, 2)], ll[(1, 3)])),
               K.mul(ll[(0, 3)], ll[(1, 2)]))
    hr = K.add(K.add(K.mul(rr[(4, 5)], rr[(6, 7)]),
                     K.mul(rr[(4, 6)], rr[(5, 7)])),
               K.mul(rr[(4, 7)], rr[(5, 6)]))
    rows = [[K.zero] * 3 for _ in range(3)]
    coef = []
    if kind == 'R':
        p = SIGINV[v]
        scale = hl
        cols = [q for q in LS if q != p]
        for jc, q in enumerate(cols):
            i, j = [t for t in LS if t not in (p, q)]
            si, sj = min(SIG[i], SIG[j]), max(SIG[i], SIG[j])
            coef.append(K.add(K.mul(hl, rr[(si, sj)]),
                              K.mul(ll[(min(p, q), max(p, q))],
                                    K.mul(dd[i], dd[j]))))
            for t in range(3):
                term1 = K.mul(c(p, v, w[p], t),
                              K.mul(dd[q], ll[(min(i, j), max(i, j))]))
                term2 = K.mul(hl, c(v, SIG[q], t, w[SIG[q]]))
                rows[t][jc] = K.add(term1, term2)
    else:
        p = v
        scale = hr
        cols = [a for a in LS if a != p]
        for jc, a in enumerate(cols):
            b, cc = [t for t in LS if t not in (p, a)]
            sb, sc = min(SIG[b], SIG[cc]), max(SIG[b], SIG[cc])
            coef.append(K.add(K.mul(hr, ll[(min(b, cc), max(b, cc))]),
                              K.mul(c(SIG[p], SIG[a], w[SIG[p]], w[SIG[a]]),
                                    K.mul(dd[b], dd[cc]))))
            for s in range(3):
                term1 = K.mul(c(p, SIG[p], s, w[SIG[p]]),
                              K.mul(dd[a], rr[(sb, sc)]))
                term2 = K.mul(hr, c(p, a, s, w[a]))
                rows[s][jc] = K.add(term1, term2)
    return rows, coef, scale, cols


# ------------------------------------------- augmented slice matrix + Q
def nbrs(tm, v):
    return tm.nbr[v]


def slice_S(tm, bl, v, tau, K):
    """spine Def 3.1: S'(tau)[t][j] = A_{v,s_j}[t][tau_j], columns = ALL
    Gamma neighbours of v in increasing order."""
    ns = tm.nbr[v]
    return [[cell(bl, tm, v, s, t, tau[j], K) for j, s in enumerate(ns)]
            for t in range(3)]


def gamma_haf_minus(tm, bl, w, drop, K):
    """haf_{Gamma - drop}(w): Gamma-hafnian over the sites not in drop."""
    vs = tuple(u for u in range(NSITE) if u not in drop)
    tot = K.zero
    for M in matchings(vs):
        pr = K.one
        ok = True
        for (u, uu) in M:
            if (u, uu) not in tm.gamma:
                ok = False
                break
            pr = K.mul(pr, bl[(u, uu)][w[u]][w[uu]])
        if ok:
            tot = K.add(tot, pr)
    return tot


def cofactorQ(tm, bl, v, w, K):
    """spine Thm 4.1: Q(w)_j = haf_{Gamma-{v,s_j}}(w)."""
    return [gamma_haf_minus(tm, bl, w, (v, s), K) for s in tm.nbr[v]]


# ---------------------------------------------------- delivery predicate
def singles_into(tm, kind, v):
    """[(edge, trigger site, trigger letter, letter at v)] over LIVE singles"""
    out = []
    for e in sorted(tm.live):
        a, b = tm.single[e]
        if kind == 'R' and e[1] == v:
            out.append((e, e[0], a, b))
        elif kind == 'L' and e[0] == v:
            out.append((e, e[1], b, a))
    return out


def admissible(tm, kind, v):
    """STRICT admissible index choices (spine 5.0 bookkeeping):
    letters on the 7 sites != v; some live single into v fires; every
    non-firing completion is a non-constant CLEAN word; every firing
    completion is non-constant and all its active live singles are into v.
    -> [(w7 as a full word with w[v]=0, T_f, T_c)]"""
    mine = singles_into(tm, kind, v)
    other = [u for u in range(NSITE) if u != v]
    out = []
    for vals in product(range(ALPHA), repeat=7):
        w = [0] * NSITE
        for u, a in zip(other, vals):
            w[u] = a
        fire = set()
        for (e, trig, tv, letter) in mine:
            if w[trig] == tv:
                fire.add(letter)
        if not fire:
            continue
        Tf, Tc, ok = [], [], True
        for t in range(ALPHA):
            ww = tuple(w[:v] + [t] + w[v + 1:])
            const = len(set(ww)) == 1
            act = tm.fired(ww)
            if t in fire:
                good = (not const) and all(
                    (e[1] if kind == 'R' else e[0]) == v for e in act)
                if good:
                    Tf.append(t)
                else:
                    ok = False
            else:
                good = (not const) and (not act)
                if good:
                    Tc.append(t)
                else:
                    ok = False
            if not ok:
                break
        if ok and Tf:
            out.append((tuple(w), tuple(Tf), tuple(Tc)))
    return out


_ADM = {}


def admissible_cached(m, kind, v):
    k = (m, kind, v)
    if k not in _ADM:
        _ADM[k] = admissible(T(m), kind, v)
    return _ADM[k]


def verdict(tm, bl, lab, K, detail=False):
    """FAIL_primary (spine 5.0): v DELIVERS at an index choice iff every
    firing ROW lies in span{clean ROWS}; it FAILS iff no admissible index
    choice delivers.  Index choices of zero scale carry no information from
    the master relation and are skipped (they are the (H2) of spine 2.1)."""
    kind, v = vsplit(lab)
    idx = admissible_cached(tm.m, kind, v)
    ndeliver = 0
    nlive = 0
    recs = []
    for (w, Tf, Tc) in idx:
        rows, coef, scale, cols = master_rows(tm, bl, kind, v, w, K)
        if K.iszero(scale):
            continue
        nlive += 1
        base = [rows[t] for t in Tc]
        rb = rank(base, K)
        ok = all(rank(base + [rows[t]], K) == rb for t in Tf)
        if ok:
            ndeliver += 1
        if detail:
            recs.append((w, Tf, Tc, ok))
    out = dict(vertex=lab, n_idx=nlive, n_deliver=ndeliver,
               DELIVERS=ndeliver > 0)
    if detail:
        out['recs'] = recs
    return out


def full_verdict(tm, bl, K):
    res = {}
    for lab in VLAB:
        res[lab] = verdict(tm, bl, lab, K)
    res['fails'] = [l for l in VLAB if not res[l]['DELIVERS']]
    return res


# ---------------------------------------------------------- point hygiene
def is_clean_point(tm, bl, K):
    """Phi = 0 at EVERY clean mixed word, by the RAW 105-matching route."""
    for w in tm.clean_words:
        if not K.iszero(phi_raw(tm, bl, w, K)):
            return False
    return True


def clean_violations(tm, bl, K):
    return [w for w in tm.clean_words if not K.iszero(phi_raw(tm, bl, w, K))]


def all_cells_nonzero(tm, bl, K):
    for e in sorted(tm.gamma):
        for a in range(3):
            for b in range(3):
                if K.iszero(bl[e][a][b]):
                    return False
    return True


def n_phi_nonzero(tm, bl, K):
    return sum(1 for w in WORDS if not K.iszero(phi_raw(tm, bl, w, K)))


def off_stratum(tm, bl, K):
    """off the vanishing stratum: Phi is not identically zero on all words"""
    for w in WORDS:
        if not K.iszero(phi_raw(tm, bl, w, K)):
            return True
    return False


# ------------------------------------------------------------- untriggered
def untriggered_words(tm, bl, v, K):
    """all 7-coordinate assignments w (w[v] free) with Phi(w|v=t) = 0 for
    every letter t -- spine Cor 4.2."""
    other = [u for u in range(NSITE) if u != v]
    out = []
    for vals in product(range(ALPHA), repeat=7):
        w = [0] * NSITE
        for u, a in zip(other, vals):
            w[u] = a
        if all(K.iszero(phi_raw(tm, bl, tuple(w[:v] + [t] + w[v + 1:]), K))
               for t in range(ALPHA)):
            out.append(tuple(w))
    return out


# ------------------------------------------------------------ point I/O
def load_point(d, K):
    """stored point: {"(u, v)": [[str,str,str],...]} -> {(u,v): 3x3}"""
    bl = {}
    for k, mat in d.items():
        e = tuple(int(x) for x in k.strip("()").split(","))
        bl[(e[0], e[1])] = [[K.of(Fraction(str(z))) for z in row]
                            for row in mat]
    return bl


def random_blocks(tm, K, rng, allow_zero=True, full=False):
    """random blocks on every Gamma edge (and, if full, on every edge)"""
    bl = {}
    src = EDGES if full else sorted(tm.gamma)
    for e in src:
        bl[e] = [[K.of(rng.randrange(1, 1000)) if not allow_zero
                  else K.of(rng.randrange(0, 1000)) for _ in range(3)]
                 for _ in range(3)]
    return bl


# ------------------------------------------------------------- manifests
class Manifest(object):
    """ledger item 21: a control file must fail loudly if a control never
    runs.  Declare up front, record on execution, assert at the end."""

    def __init__(self, declared):
        self.declared = list(declared)
        self.run = []
        self.out = {"_controls_declared": list(declared), "_controls_run": []}

    def record(self, name, payload):
        need(name in self.declared, "undeclared control %s" % name)
        need(name not in self.run, "control %s run twice" % name)
        self.run.append(name)
        self.out["_controls_run"].append(name)
        self.out[name] = payload

    def finish(self, path, extra=None):
        need(sorted(self.run) == sorted(self.declared),
             "control manifest mismatch: declared %s ran %s"
             % (sorted(self.declared), sorted(self.run)))
        if extra:
            self.out.update(extra)
        self.out["_manifest_ok"] = True
        self.out["done"] = True
        with open(path, "w") as fh:
            json.dump(self.out, fh, indent=1, default=str)
        return self.out
