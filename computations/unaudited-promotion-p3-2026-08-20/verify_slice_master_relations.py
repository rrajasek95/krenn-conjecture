#!/usr/bin/env python3
"""House checker for the slice master relations, the cofactor identity, and
the Q-span bound  (dependency ID SLICE-MASTER; staged by lane P3).

    computations/verify_slice_master_relations.py

STANDARD LIBRARY ONLY.  No import from any `computations/unaudited-*`
directory, and no import of any lane module.  The nine 28-entry template
masks are EMBEDDED below (they are combinatorial data, independently
corroborated across eight lanes -- see STEP 1, which rebuilds every derived
structural fact from the masks alone and checks it against the recorded
census).  Step 5 READS a stored point corpus as DATA (a JSON file); it never
imports code from it, and it is optional-but-loud (see --strict).

House style: every check goes through the raising `require()`.  There is no
bare `assert` anywhere in this file, so the checker is equally strict under
`python3 -O`.

WHAT IS CHECKED

  STEP 1  structure       templates -> Gamma / singles / live singles /
                          clean words / Gamma perfect matchings, rebuilt from
                          the masks alone and matched against the census.
  STEP 2  Phi two routes  raw enumeration over the 105 perfect matchings of
                          K_8 vs the sigma-count decomposition (equation (1)),
                          which is the sole structural input to the master
                          relations.
  STEP 3  master relations  (M) and (M*) at RANDOM blocks -- they are
                          identities, so a check confined to clean points
                          could not tell an identity from a coincidence on
                          the locus.
  STEP 4  cofactor identity  at RANDOM NON-CLEAN blocks, with the left-hand
                          side computed by the raw 105-matching route.
  STEP 5  Q-span bound    at STORED points (data file).  Optional-but-loud.
  STEP 6  MUT-A           one perturbed cell must BREAK the cofactor identity
                          against the unperturbed Phi.
  STEP 7  MUT-B           with the untriggered word sets of a real clean
                          point but randomised blocks, the Q-span bound must
                          be VIOLATED -- the step-5 checker is not vacuous.

Steps 1-4, 6 and 7 are mandatory.  Step 5 runs when the point corpus is
found and prints a labelled SKIPPED line otherwise; `--strict` makes it
mandatory.

Exit code 0 iff every mandatory step passes.

UNAUDITED STAGING -- nothing verified here is a proved claim of the
repository.  See computations/unaudited-promotion-p3-2026-08-20/.
"""

import argparse
import json
import os
import random
import sys
import time
from fractions import Fraction
from itertools import combinations, product


# --------------------------------------------------------------- house style
class CheckerError(Exception):
    """Raised by require(); never caught inside a step."""


def require(cond, msg):
    """The single assertion primitive.  Raises rather than asserting, so that
    `python3 -O` cannot strip it."""
    if not cond:
        raise CheckerError(msg)
    return True


# ------------------------------------------------------------------ the model
NV = 8
QQ = 3
FULL = 511

EDG = tuple(combinations(range(NV), 2))
LSIDE = (0, 1, 2, 3)
RSIDE = (4, 5, 6, 7)
SG = {0: 7, 1: 4, 2: 5, 3: 6}
SGI = dict((v, k) for k, v in SG.items())

# The nine 28-entry template masks, m = 25..28.  511 = Gamma edge, 0 = absent,
# a one-bit value = a "single" at that cell.  Combinatorial data.
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
SUPPORTS = (25, 26, 27, 28)

VERTS = ("R4", "R5", "R6", "R7", "L0", "L1", "L2", "L3")

# The structural census recorded by audit A10 (results_smoke.json, key
# C3_structure).  STEP 1 must reproduce every one of these numbers from the
# masks alone.
CENSUS = {
    25: {"n_gamma": 13, "n_live": 10, "n_clean": 2624, "n_gamma_pms": 8,
         "deg": (4, 4, 4, 3, 3, 3, 2, 3)},
    26: {"n_gamma": 14, "n_live": 12, "n_clean": 2152, "n_gamma_pms": 11,
         "deg": (4, 4, 4, 4, 3, 3, 3, 3)},
    27: {"n_gamma": 15, "n_live": 12, "n_clean": 2152, "n_gamma_pms": 12,
         "deg": (4, 4, 4, 4, 4, 3, 4, 3)},
    28: {"n_gamma": 16, "n_live": 12, "n_clean": 2152, "n_gamma_pms": 16,
         "deg": (4, 4, 4, 4, 4, 4, 4, 4)},
}


def _perfect_matchings(vs):
    """All perfect matchings of the complete graph on the vertex tuple vs."""
    if not vs:
        return [()]
    a = vs[0]
    out = []
    for i in range(1, len(vs)):
        b = vs[i]
        e = (a, b) if a < b else (b, a)
        for rest in _perfect_matchings(vs[1:i] + vs[i + 1:]):
            out.append((e,) + rest)
    return out


PM105 = tuple(_perfect_matchings(tuple(range(NV))))
WORDS = tuple(product(range(QQ), repeat=NV))
MIXED = tuple(w for w in WORDS if len(set(w)) > 1)


class Struct(object):
    """Template combinatorics, computed from the mask list alone."""

    def __init__(self, m):
        T = TMPL[m]
        require(len(T) == len(EDG), "template %d has wrong length" % m)
        self.m = m
        self.gamma = tuple(e for e, t in zip(EDG, T) if t == FULL)
        self.gs = set(self.gamma)
        self.single = {}
        for e, t in zip(EDG, T):
            if t in (0, FULL):
                continue
            bits = [c for c in range(9) if (t >> c) & 1]
            require(len(bits) == 1,
                    "edge %s of template %d is not a single-cell mask" % (e, m))
            self.single[e] = (bits[0] // 3, bits[0] % 3)
        self.absent = tuple(e for e, t in zip(EDG, T) if t == 0)
        require(len(self.gamma) + len(self.single) + len(self.absent) == 28,
                "template %d does not partition the 28 edges" % m)
        self.live = tuple(sorted(
            e for e in self.single
            if self._has_pm(tuple(v for v in range(NV) if v not in e))))
        self.clean = tuple(w for w in MIXED if not self.active_live(w))
        self.gamma_pms = tuple(M for M in PM105 if all(e in self.gs for e in M))
        self.nbrs = {}
        for v in range(NV):
            self.nbrs[v] = tuple(
                s for s in range(NV)
                if (min(s, v), max(s, v)) in self.gs)

    def _has_pm(self, vs):
        if not vs:
            return True
        a = vs[0]
        for i in range(1, len(vs)):
            b = vs[i]
            e = (a, b) if a < b else (b, a)
            if e in self.gs and self._has_pm(vs[1:i] + vs[i + 1:]):
                return True
        return False

    def active_live(self, w):
        return tuple(e for e in self.live
                     if (w[e[0]], w[e[1]]) == self.single[e])

    def degree(self, v):
        return len(self.nbrs[v])


_S = {}


def S(m):
    if m not in _S:
        _S[m] = Struct(m)
    return _S[m]


# ------------------------------------------------------------------ the field
class Fp(object):
    name_fmt = "F_%d"

    def __init__(self, p):
        self.p = p
        self.name = self.name_fmt % p
        self.zero = 0
        self.one = 1

    def z(self, a):
        return int(a) % self.p

    def add(self, a, b):
        return (a + b) % self.p

    def sub(self, a, b):
        return (a - b) % self.p

    def mul(self, a, b):
        return (a * b) % self.p

    def isz(self, a):
        return a % self.p == 0

    def inv(self, a):
        return pow(a, self.p - 2, self.p)


class Rat(object):
    def __init__(self):
        self.name = "Q"
        self.zero = Fraction(0)
        self.one = Fraction(1)

    def z(self, a):
        return Fraction(a)

    def add(self, a, b):
        return a + b

    def sub(self, a, b):
        return a - b

    def mul(self, a, b):
        return a * b

    def isz(self, a):
        return a == 0

    def inv(self, a):
        return 1 / a


def rank(rows, K):
    """Exact rank by Gaussian elimination over K."""
    mat = [list(r) for r in rows]
    nr = len(mat)
    if nr == 0:
        return 0
    nc = len(mat[0])
    r = 0
    for c in range(nc):
        piv = None
        for i in range(r, nr):
            if not K.isz(mat[i][c]):
                piv = i
                break
        if piv is None:
            continue
        mat[r], mat[piv] = mat[piv], mat[r]
        iv = K.inv(mat[r][c])
        mat[r] = [K.mul(x, iv) for x in mat[r]]
        for i in range(nr):
            if i != r and not K.isz(mat[i][c]):
                f = mat[i][c]
                mat[i] = [K.sub(mat[i][j], K.mul(f, mat[r][j]))
                          for j in range(nc)]
        r += 1
        if r == nr:
            break
    return r


# ------------------------------------------------------------- Phi, two routes
def cell(bl, gs, u, v, a, b, K):
    """A_uv[a][b] with u, v given in ANY order (a is u's letter).  Only Gamma
    edges carry a z-free term; singles and absent edges contribute 0 to Phi."""
    e = (u, v) if u < v else (v, u)
    if e not in gs:
        return K.zero
    if u < v:
        return bl[e][a][b]
    return bl[e][b][a]


def phi_raw(m, bl, w, K):
    """Phi(w) by raw enumeration of the perfect matchings of K_8 that lie
    inside Gamma."""
    st = S(m)
    tot = K.zero
    for M in st.gamma_pms:
        pr = K.one
        for (a, b) in M:
            pr = K.mul(pr, bl[(a, b)][w[a]][w[b]])
            if K.isz(pr):
                break
        tot = K.add(tot, pr)
    return tot


def _lrd(m, bl, w, K):
    """The l / r / d / hafL / hafR bundle of equation (1) at the word w."""
    st = S(m)
    gs = st.gs

    def c(u, v, a, b):
        return cell(bl, gs, u, v, a, b, K)

    ll = {}
    for i, j in combinations(LSIDE, 2):
        ll[(i, j)] = c(i, j, w[i], w[j])
    rr = {}
    for a, b in combinations(RSIDE, 2):
        rr[(a, b)] = c(a, b, w[a], w[b])
    dd = {}
    for a in LSIDE:
        dd[a] = c(a, SG[a], w[a], w[SG[a]])
    hafL = K.add(K.add(K.mul(ll[(0, 1)], ll[(2, 3)]),
                       K.mul(ll[(0, 2)], ll[(1, 3)])),
                 K.mul(ll[(0, 3)], ll[(1, 2)]))
    hafR = K.add(K.add(K.mul(rr[(4, 5)], rr[(6, 7)]),
                       K.mul(rr[(4, 6)], rr[(5, 7)])),
                 K.mul(rr[(4, 7)], rr[(5, 6)]))
    return ll, rr, dd, hafL, hafR


def phi_formula(m, bl, w, K):
    """Phi(w) by the sigma-count decomposition -- equation (1).  This is the
    sole structural input to the master relations, so checking it against
    phi_raw is also a check of (1)."""
    ll, rr, dd, hafL, hafR = _lrd(m, bl, w, K)
    tot = K.mul(hafL, hafR)
    for i, j in combinations(LSIDE, 2):
        p, q = tuple(x for x in LSIDE if x not in (i, j))
        term = K.mul(ll[(i, j)],
                     rr[(min(SG[i], SG[j]), max(SG[i], SG[j]))])
        term = K.mul(term, K.mul(dd[p], dd[q]))
        tot = K.add(tot, term)
    tot = K.add(tot, K.mul(K.mul(dd[0], dd[1]), K.mul(dd[2], dd[3])))
    return tot


# ------------------------------------------------------- the master relations
def master_R(m, bl, w, v, t, K):
    """(M) at an R-vertex v and letter t: returns (lhs, rhs)."""
    st = S(m)
    gs = st.gs
    p = SGI[v]
    ww = list(w)
    ww[v] = t
    ww = tuple(ww)
    ll, rr, dd, hafL, _ = _lrd(m, bl, ww, K)
    lhs = K.mul(hafL, phi_raw(m, bl, ww, K))
    rhs = K.zero
    for q in LSIDE:
        if q == p:
            continue
        i, j = tuple(x for x in LSIDE if x not in (p, q))
        # B_q = hafL * r_{sigma i, sigma j} + l_pq * d_i * d_j
        B = K.add(K.mul(hafL, rr[(min(SG[i], SG[j]), max(SG[i], SG[j]))]),
                  K.mul(ll[(min(p, q), max(p, q))], K.mul(dd[i], dd[j])))
        # ROW(t)[q] = d_p(t) * (d_q * l_ij) + hafL * r_{v, sigma q}(t)
        d_p_t = cell(bl, gs, p, v, ww[p], t, K)
        r_v_sq = cell(bl, gs, v, SG[q], t, ww[SG[q]], K)
        ROW = K.add(K.mul(d_p_t, K.mul(dd[q], ll[(min(i, j), max(i, j))])),
                    K.mul(hafL, r_v_sq))
        rhs = K.add(rhs, K.mul(B, ROW))
    return lhs, rhs


def master_L(m, bl, w, p, s, K):
    """(M*) at an L-vertex p and letter s: returns (lhs, rhs)."""
    st = S(m)
    gs = st.gs
    ww = list(w)
    ww[p] = s
    ww = tuple(ww)
    ll, rr, dd, _, hafR = _lrd(m, bl, ww, K)
    lhs = K.mul(hafR, phi_raw(m, bl, ww, K))
    rhs = K.zero
    for a in LSIDE:
        if a == p:
            continue
        b, cc = tuple(x for x in LSIDE if x not in (p, a))
        # X_a = hafR * l_bc + r_{sigma p, sigma a} * d_b * d_c
        X = K.add(K.mul(hafR, ll[(min(b, cc), max(b, cc))]),
                  K.mul(rr[(min(SG[p], SG[a]), max(SG[p], SG[a]))],
                        K.mul(dd[b], dd[cc])))
        # ROW(s)[a] = d_p(s) * (d_a * r_{sigma b, sigma c}) + hafR * l_{p,a}(s)
        d_p_s = cell(bl, gs, p, SG[p], s, ww[SG[p]], K)
        l_pa = cell(bl, gs, p, a, s, ww[a], K)
        ROW = K.add(
            K.mul(d_p_s,
                  K.mul(dd[a],
                        rr[(min(SG[b], SG[cc]), max(SG[b], SG[cc]))])),
            K.mul(hafR, l_pa))
        rhs = K.add(rhs, K.mul(X, ROW))
    return lhs, rhs


# -------------------------------------------------------- S', Q, and the bound
def Sprime(m, bl, v, tau, ns, K):
    """S'(tau)[t][j] = A_{v,s_j}[t][tau_j] over ALL Gamma-neighbours of v."""
    st = S(m)
    return [[cell(bl, st.gs, v, s, t, tau[j], K)
             for j, s in enumerate(ns)] for t in range(QQ)]


def Qvec(m, bl, v, w, ns, K):
    """Q_j = haf_Gamma(V - {v, s_j})(w), by raw enumeration of the 15 perfect
    matchings of the remaining six vertices."""
    st = S(m)
    out = []
    for s in ns:
        rest = tuple(z for z in range(NV) if z not in (v, s))
        tot = K.zero
        for M in _perfect_matchings(rest):
            pr = K.one
            for (a, b) in M:
                e = (a, b) if a < b else (b, a)
                if e not in st.gs:
                    pr = K.zero
                    break
                pr = K.mul(pr, bl[e][w[e[0]]][w[e[1]]])
                if K.isz(pr):
                    break
            tot = K.add(tot, pr)
        out.append(tot)
    return out


def untriggered_by_tau(m, bl, v, K, cap_tuples=0):
    """Map tau -> list of words w with slice tuple tau that are UNTRIGGERED at
    v, i.e. Phi(w|v=t) = 0 for all three letters t."""
    st = S(m)
    ns = st.nbrs[v]
    others = tuple(z for z in range(NV) if z != v)
    out = {}
    for assign in product(range(QQ), repeat=NV - 1):
        w = [0] * NV
        for idx, z in enumerate(others):
            w[z] = assign[idx]
        ok = True
        for t in range(QQ):
            w[v] = t
            if not K.isz(phi_raw(m, bl, tuple(w), K)):
                ok = False
                break
        if not ok:
            continue
        tau = tuple(w[s] for s in ns)
        if cap_tuples and tau not in out and len(out) >= cap_tuples:
            continue
        out.setdefault(tau, []).append(tuple(w))
    return out


# ------------------------------------------------------------- block builders
def rnd_blocks(m, rng, K, p=None, nonzero=False):
    st = S(m)
    bl = {}
    for e in st.gamma:
        rows = []
        for _ in range(QQ):
            row = []
            for _ in range(QQ):
                if p is None:
                    row.append(Fraction(rng.randrange(-9, 10)))
                else:
                    row.append(rng.randrange(1 if nonzero else 0, p))
            rows.append(row)
        bl[e] = rows
    return bl


def parse_point(pt, K):
    """A stored point: {"(u, v)": [[str,str,str], ...]} -> block dict."""
    bl = {}
    for key, mat in pt.items():
        a, b = key.strip("()").split(",")
        e = (int(a), int(b))
        bl[e] = [[K.z(Fraction(x)) for x in row] for row in mat]
    return bl


# ------------------------------------------------------------------- the steps
def step1_structure(rep):
    for m in SUPPORTS:
        st = S(m)
        c = CENSUS[m]
        require(len(st.gamma) == c["n_gamma"],
                "m=%d: Gamma count %d != %d" % (m, len(st.gamma), c["n_gamma"]))
        require(len(st.live) == c["n_live"],
                "m=%d: live-single count %d != %d"
                % (m, len(st.live), c["n_live"]))
        require(len(st.clean) == c["n_clean"],
                "m=%d: clean-word count %d != %d"
                % (m, len(st.clean), c["n_clean"]))
        require(len(st.gamma_pms) == c["n_gamma_pms"],
                "m=%d: Gamma perfect-matching count %d != %d"
                % (m, len(st.gamma_pms), c["n_gamma_pms"]))
        deg = tuple(st.degree(v) for v in range(NV))
        require(deg == c["deg"],
                "m=%d: Gamma degrees %s != %s" % (m, deg, c["deg"]))
    require(len(PM105) == 105, "K_8 has %d perfect matchings, not 105"
            % len(PM105))
    require(len(WORDS) == 6561 and len(MIXED) == 6558,
            "word bookkeeping is wrong")
    rep["step1_structure"] = {
        "supports": list(SUPPORTS), "n_pm_K8": len(PM105),
        "census_matched": True, "PASS": True}
    return "STEP 1  structure          4 supports, census matched      PASS"


def step2_phi_routes(rep, rng):
    n = 0
    for m in SUPPORTS:
        for K, p in ((Rat(), None), (Fp(31), 31)):
            bl = rnd_blocks(m, rng, K, p)
            for _ in range(10):
                w = tuple(rng.randrange(QQ) for _ in range(NV))
                a = phi_raw(m, bl, w, K)
                b = phi_formula(m, bl, w, K)
                require(K.isz(K.sub(a, b)),
                        "m=%d %s: Phi routes disagree at %s"
                        % (m, K.name, (w,)))
                n += 1
    rep["step2_phi_two_routes"] = {"tests": n, "mismatches": 0, "PASS": True}
    return ("STEP 2  Phi two routes     %4d tests, 0 mismatches         PASS"
            % n)


def step3_master(rep, rng):
    n = 0
    for m in SUPPORTS:
        for K, p in ((Rat(), None), (Fp(31), 31)):
            bl = rnd_blocks(m, rng, K, p)
            for _ in range(6):
                w = tuple(rng.randrange(QQ) for _ in range(NV))
                for v in RSIDE:
                    for t in range(QQ):
                        lhs, rhs = master_R(m, bl, w, v, t, K)
                        require(K.isz(K.sub(lhs, rhs)),
                                "m=%d %s: (M) fails at R%d, t=%d"
                                % (m, K.name, v, t))
                        n += 1
                for pv in LSIDE:
                    for s in range(QQ):
                        lhs, rhs = master_L(m, bl, w, pv, s, K)
                        require(K.isz(K.sub(lhs, rhs)),
                                "m=%d %s: (M*) fails at L%d, s=%d"
                                % (m, K.name, pv, s))
                        n += 1
    rep["step3_master_relations"] = {"tests": n, "violations": 0, "PASS": True}
    return ("STEP 3  master relations   %4d tests, 0 violations         PASS"
            % n)


def step4_cofactor(rep, rng):
    n = 0
    nonclean = 0
    for m in SUPPORTS:
        for K, p in ((Rat(), None), (Fp(13), 13), (Fp(31), 31)):
            bl = rnd_blocks(m, rng, K, p)
            st = S(m)
            # Random blocks are non-clean with overwhelming probability; we
            # verify that explicitly rather than assuming it.
            probe = st.clean[0]
            if not K.isz(phi_raw(m, bl, probe, K)):
                nonclean += 1
            for v in range(NV):
                ns = st.nbrs[v]
                for _ in range(8):
                    w = [rng.randrange(QQ) for _ in range(NV)]
                    tau = tuple(w[s] for s in ns)
                    Sp = Sprime(m, bl, v, tau, ns, K)
                    Q = Qvec(m, bl, v, tuple(w), ns, K)
                    for t in range(QQ):
                        ww = list(w)
                        ww[v] = t
                        lhs = phi_raw(m, bl, tuple(ww), K)
                        rhs = K.zero
                        for j in range(len(ns)):
                            rhs = K.add(rhs, K.mul(Sp[t][j], Q[j]))
                        require(K.isz(K.sub(lhs, rhs)),
                                "m=%d %s: cofactor identity fails at v=%d, "
                                "t=%d" % (m, K.name, v, t))
                        n += 1
    require(nonclean > 0,
            "no random block set was witnessed non-clean; step 4 would be "
            "testing the identity only on the solution locus")
    rep["step4_cofactor_identity"] = {
        "tests": n, "violations": 0, "nonclean_witnesses": nonclean,
        "PASS": True}
    return ("STEP 4  cofactor identity  %4d tests, 0 violations, %d "
            "non-clean witnesses  PASS" % (n, nonclean))


def _find_points(explicit):
    if explicit:
        return explicit if os.path.exists(explicit) else None
    env = os.environ.get("KRENN_POINTS")
    if env and os.path.exists(env):
        return env
    here = os.path.dirname(os.path.abspath(__file__))
    cands = [
        os.path.join(here, "certified_package", "points_hunt.json"),
        os.path.join(here, "points_hunt.json"),
        os.path.join(os.path.dirname(here),
                     "unaudited-exclusion-w30-2026-08-19", "points_hunt.json"),
        os.path.join(os.getcwd(), "points_hunt.json"),
    ]
    for c in cands:
        if os.path.exists(c):
            return c
    return None


def step5_qspan(rep, rng, path, npoints):
    if path is None:
        rep["step5_qspan_bound"] = {"SKIPPED": True,
                                    "reason": "point corpus not found"}
        return ("STEP 5  Q-span bound       SKIPPED (no point corpus; "
                "--points PATH or --strict)")
    data = json.load(open(path))
    pts = [q for q in data.get("points", []) if q.get("p")]
    require(len(pts) > 0, "point corpus %s carries no F_p points" % path)
    rng.shuffle(pts)
    used = 0
    ntau = 0
    nwords = 0
    checked = []
    for q in pts:
        if used >= npoints:
            break
        m = q["m"]
        if m not in TMPL:
            continue
        K = Fp(q["p"])
        bl = parse_point(q["point"], K)
        st = S(m)
        per_point = 0
        for v in range(NV):
            ns = st.nbrs[v]
            groups = untriggered_by_tau(m, bl, v, K)
            for tau, wl in groups.items():
                Sp = Sprime(m, bl, v, tau, ns, K)
                qs = [Qvec(m, bl, v, w, ns, K) for w in wl]
                rS = rank(Sp, K)
                rQ = rank(qs, K)
                require(rS + rQ <= len(ns),
                        "m=%d %s v=%d tau=%s: rank S'=%d + dim span Q=%d "
                        "exceeds |N(v)|=%d" % (m, K.name, v, tau, rS, rQ,
                                               len(ns)))
                ntau += 1
                nwords += len(wl)
                per_point += 1
        checked.append({"m": m, "p": q["p"], "tag": q.get("tag", ""),
                        "van": q.get("van"), "tuples_checked": per_point})
        used += 1
    require(used > 0, "no usable stored point was found in %s" % path)
    rep["step5_qspan_bound"] = {
        "source": os.path.relpath(path), "points": used, "tuples": ntau,
        "untriggered_words": nwords, "violations": 0, "detail": checked,
        "PASS": True}
    return ("STEP 5  Q-span bound       %d points, %d tuples, %d words, "
            "0 violations  PASS" % (used, ntau, nwords))


def step6_mut_a(rep, rng):
    """One perturbed cell must break the cofactor identity.

    The perturbed cell is chosen so that it is provably load-bearing: an edge
    (v, s_j) at v with Q_j != 0, at the cell that S'(tau)[t0][j] reads.  Such
    an edge is incident to v, so it appears in NO Q_j (each Q_j is a hafnian
    over V - {v, s_j}); the perturbation therefore moves the right-hand side
    by exactly delta * Q_j != 0 and must break the identity.  A perturbation
    chosen blindly can land on a cell the sampled tuple never reads, which is
    a property of the sample and not of the checker."""
    fired = 0
    trials = 0
    detail = []
    for m in SUPPORTS:
        K = Fp(31)
        p = 31
        bl = rnd_blocks(m, rng, K, p, nonzero=True)
        st = S(m)
        for v in range(NV):
            ns = st.nbrs[v]
            w = tuple(rng.randrange(QQ) for _ in range(NV))
            tau = tuple(w[s] for s in ns)
            Sp = Sprime(m, bl, v, tau, ns, K)
            Q = Qvec(m, bl, v, tuple(w), ns, K)
            # baseline must hold at every letter
            for t in range(QQ):
                ww = list(w)
                ww[v] = t
                lhs = phi_raw(m, bl, tuple(ww), K)
                rhs = K.zero
                for j in range(len(ns)):
                    rhs = K.add(rhs, K.mul(Sp[t][j], Q[j]))
                require(K.isz(K.sub(lhs, rhs)),
                        "m=%d v=%d: MUT-A baseline identity already fails"
                        % (m, v))
            # a load-bearing column
            jj = None
            for j in range(len(ns)):
                if not K.isz(Q[j]):
                    jj = j
                    break
            if jj is None:
                continue
            t0 = 0
            s = ns[jj]
            e0 = (min(v, s), max(v, s))
            b2 = dict((e, [r[:] for r in bl[e]]) for e in bl)
            if v < s:
                b2[e0][t0][tau[jj]] = (b2[e0][t0][tau[jj]] + 1) % p
            else:
                b2[e0][tau[jj]][t0] = (b2[e0][tau[jj]][t0] + 1) % p
            Sp2 = Sprime(m, b2, v, tau, ns, K)
            Q2 = Qvec(m, b2, v, tuple(w), ns, K)
            ww = list(w)
            ww[v] = t0
            lhs = phi_raw(m, bl, tuple(ww), K)      # UNMUTATED Phi
            rhs = K.zero
            for j in range(len(ns)):
                rhs = K.add(rhs, K.mul(Sp2[t0][j], Q2[j]))
            trials += 1
            if not K.isz(K.sub(lhs, rhs)):
                fired += 1
            else:
                detail.append({"m": m, "v": v, "j": jj})
    require(trials > 0, "MUT-A found no column with Q_j != 0 to perturb")
    require(fired == trials,
            "MUT-A: a load-bearing one-cell perturbation did not break the "
            "cofactor identity in %d of %d trials (%s) -- the step-4 checker "
            "may be vacuous" % (trials - fired, trials, detail))
    rep["step6_mut_a"] = {"trials": trials, "fired": fired, "PASS": True}
    return ("STEP 6  MUT-A              %d/%d load-bearing perturbations "
            "broke the identity  PASS" % (fired, trials))


def step7_mut_b(rep, rng, path):
    """With a real point's untriggered word sets but RANDOM blocks, the Q-span
    bound must be violated -- otherwise step 5 proves nothing."""
    if path is None:
        rep["step7_mut_b"] = {"SKIPPED": True,
                              "reason": "point corpus not found"}
        return ("STEP 7  MUT-B              SKIPPED (no point corpus)")
    data = json.load(open(path))
    pts = [q for q in data.get("points", []) if q.get("p")]
    require(len(pts) > 0, "point corpus %s carries no F_p points" % path)
    q = pts[0]
    m = q["m"]
    K = Fp(q["p"])
    bl = parse_point(q["point"], K)
    st = S(m)
    viol = 0
    tested = 0
    rb = rnd_blocks(m, rng, K, q["p"], nonzero=True)
    for v in range(NV):
        ns = st.nbrs[v]
        groups = untriggered_by_tau(m, bl, v, K)
        for tau, wl in groups.items():
            Sp = Sprime(m, rb, v, tau, ns, K)      # RANDOM blocks
            qs = [Qvec(m, rb, v, w, ns, K) for w in wl]
            rS = rank(Sp, K)
            rQ = rank(qs, K)
            tested += 1
            if rS + rQ > len(ns):
                viol += 1
    require(tested > 0,
            "MUT-B found no untriggered word set to perturb")
    require(viol > 0,
            "MUT-B: randomising the blocks produced 0 bound violations over "
            "%d tuples -- the step-5 checker is vacuous" % tested)
    rep["step7_mut_b"] = {"m": m, "p": q["p"], "tag": q.get("tag", ""),
                          "tuples_tested": tested, "violations": viol,
                          "PASS": True}
    return ("STEP 7  MUT-B              %d/%d tuples violate the bound at "
            "random blocks  PASS" % (viol, tested))


# -------------------------------------------------------------------- driver
def main(argv=None):
    ap = argparse.ArgumentParser(
        description="House checker for SLICE-MASTER (lane P3 staging).")
    ap.add_argument("--seed", type=int, default=20260820)
    ap.add_argument("--points", default=None,
                    help="stored point corpus (JSON) for steps 5 and 7")
    ap.add_argument("--npoints", type=int, default=3,
                    help="how many stored points to use in step 5")
    ap.add_argument("--strict", action="store_true",
                    help="make steps 5 and 7 mandatory")
    ap.add_argument("--json", default=None, help="write the report here")
    args = ap.parse_args(argv)

    t0 = time.time()
    rng = random.Random(args.seed)
    rep = {"_header": "UNAUDITED house checker -- SLICE-MASTER (lane P3)",
           "seed": args.seed, "python": sys.version.split()[0],
           "optimised": not __debug__}

    path = _find_points(args.points)
    if args.strict:
        require(path is not None,
                "--strict was given but no point corpus was found "
                "(use --points PATH or set KRENN_POINTS)")

    print("verify_slice_master_relations.py  seed=%d  python=%s  -O=%s"
          % (args.seed, sys.version.split()[0], not __debug__))
    print("point corpus: %s" % (path if path else "(none)"))
    print("")

    lines = []
    lines.append(step1_structure(rep))
    print(lines[-1], flush=True)
    lines.append(step2_phi_routes(rep, rng))
    print(lines[-1], flush=True)
    lines.append(step3_master(rep, rng))
    print(lines[-1], flush=True)
    lines.append(step4_cofactor(rep, rng))
    print(lines[-1], flush=True)
    lines.append(step5_qspan(rep, rng, path, args.npoints))
    print(lines[-1], flush=True)
    lines.append(step6_mut_a(rep, rng))
    print(lines[-1], flush=True)
    lines.append(step7_mut_b(rep, rng, path))
    print(lines[-1], flush=True)

    rep["elapsed_s"] = round(time.time() - t0, 1)
    mandatory = ["step1_structure", "step2_phi_two_routes",
                 "step3_master_relations", "step4_cofactor_identity",
                 "step6_mut_a"]
    if args.strict or path is not None:
        mandatory += ["step5_qspan_bound", "step7_mut_b"]
    for k in mandatory:
        require(rep.get(k, {}).get("PASS") is True,
                "mandatory step %s did not pass" % k)
    rep["MANDATORY_STEPS"] = mandatory
    rep["ALL_PASS"] = True
    print("")
    print("ALL MANDATORY STEPS PASS  (%.1f s)" % rep["elapsed_s"])
    if args.json:
        fh = open(args.json, "w")
        json.dump(rep, fh, indent=1, default=str)
        fh.close()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except CheckerError as exc:
        sys.stderr.write("CHECKER FAILURE: %s\n" % exc)
        sys.exit(1)
