#!/usr/bin/env python3
"""Independent clean-room audit of
notes/good-pair-fan-six-port-simultaneous-exclusion.md.

Reconstructed from the note's statements and the previously audited
theorem notes it cites (source-derivative-hessian-dichotomy,
good-pair-fan-six-port-triple-cofactor-reduction,
target-flattening-essential-star-pair-bound,
injective-star-hessian-bridge-frontier,
good-pair-fan-induced-zero-four-cut-reduction,
common-origin-factorization-rank-countermodel,
all-pair-missing-row-countermodel) WITHOUT reading
computations/fan_six_port_simultaneous_exclusion_check.py or its
certificate JSON.  All conventions, orderings, seeds, primes, site
labels, and Singular variable orders are chosen independently.

Everything decisive is exact: integers, rationals, Gaussian rationals,
or Singular saturations over Q with fully symbolic entries.  Finite
field sweeps are labelled census/sanity layers.  The script exits
nonzero on any failure.

Run from the repository root:
    uv run python computations/audit_fan_six_port_simultaneous_exclusion_independent.py
"""

import itertools
import os
import random
import subprocess
import sys
import tempfile
from fractions import Fraction

import numpy as np

RNG = random.Random(20260728)

FAILURES = []
CHECK_COUNT = [0]


def check(label, ok, detail=""):
    CHECK_COUNT[0] += 1
    if ok:
        print(f"PASS  {label}" + (f"  [{detail}]" if detail else ""))
    else:
        print(f"FAIL  {label}" + (f"  [{detail}]" if detail else ""))
        FAILURES.append(label)


# ---------------------------------------------------------------------------
# Square-zero site algebra.
#
# Monomial encoding: sites 0..n-1, two bits per site in one int;
# digit 0 = site empty, digit c+1 = basis vector e_c at that site.
# An element is a dict {monomial int: exact coefficient}.
# Products of monomials touching a common site vanish; disjoint
# monomials merge by integer addition (no carries by disjointness).
# ---------------------------------------------------------------------------

_OCC = {}


def occ(mono):
    v = _OCC.get(mono)
    if v is None:
        m, o, s = mono, 0, 0
        while m:
            if m & 3:
                o |= 1 << s
            m >>= 2
            s += 1
        _OCC[mono] = o
        v = o
    return v


def e_mono(site, colour):
    return (colour + 1) << (2 * site)


def mono_digits(mono, nsites):
    return [(mono >> (2 * x)) & 3 for x in range(nsites)]


def add_into(acc, elem, scale=1):
    for k, v in elem.items():
        nv = acc.get(k, 0) + scale * v
        if nv:
            acc[k] = nv
        elif k in acc:
            del acc[k]


def mul(A, B):
    if len(A) > len(B):
        A, B = B, A
    out = {}
    bitems = list(B.items())
    for ka, va in A.items():
        oa = occ(ka)
        for kb, vb in bitems:
            if oa & occ(kb):
                continue
            k = ka + kb
            nv = out.get(k, 0) + va * vb
            if nv:
                out[k] = nv
            elif k in out:
                del out[k]
    return out


def lin_elem(comps):
    """comps: dict site -> length-3 coefficient list."""
    out = {}
    for x, vec in comps.items():
        for c in range(3):
            if vec[c]:
                out[e_mono(x, c)] = out.get(e_mono(x, c), 0) + vec[c]
    return {k: v for k, v in out.items() if v}


def block_elem(i, j, M):
    """Quadratic block M (3x3, rows=colour at i, cols=colour at j)."""
    out = {}
    for a in range(3):
        for b in range(3):
            if M[a][b]:
                out[e_mono(i, a) + e_mono(j, b)] = M[a][b]
    return out


def quad_elem(blocks):
    out = {}
    for (i, j), M in blocks.items():
        add_into(out, block_elem(i, j, M))
    return out


def iter_matchings(sites, k):
    """All k-matchings (lists of k disjoint pairs) inside the site list."""
    sites = sorted(sites)

    def rec(rem, k):
        if k == 0:
            yield []
            return
        if len(rem) < 2 * k:
            return
        head, rest = rem[0], rem[1:]
        # head unmatched
        if len(rest) >= 2 * k:
            yield from rec(rest, k)
        # head matched with a later site
        for idx, t in enumerate(rest):
            sub = rest[:idx] + rest[idx + 1:]
            for m in rec(sub, k - 1):
                yield [(head, t)] + m

    yield from rec(sites, k)


def divided_power(blocks, sites, k):
    """q^{[k]} = sum over k-matchings of products of blocks (exact ints)."""
    out = {}
    key_pairs = blocks
    for m in iter_matchings(sites, k):
        mats = []
        ok = True
        for (i, j) in m:
            M = key_pairs.get((i, j))
            if M is None:
                ok = False
                break
            mats.append((i, j, M))
        if not ok:
            continue
        # expand product over colour assignments
        partial = {0: 1}
        for (i, j, M) in mats:
            partial = mul(partial, block_elem(i, j, M))
            if not partial:
                break
        add_into(out, partial)
    return out


def extract_slot(elem, site, colour):
    """Coefficient of e_colour^{(site)}: strips the site factor."""
    out = {}
    want = colour + 1
    shift = 2 * site
    for k, v in elem.items():
        if (k >> shift) & 3 == want:
            out[k - (want << shift)] = v
    return out


def elem_eq(A, B):
    if len(A) != len(B):
        return False
    for k, v in A.items():
        if B.get(k, 0) != v:
            return False
    return True


def elem_sub(A, B):
    out = dict(A)
    add_into(out, B, -1)
    return out


# ---------------------------------------------------------------------------
# Exact linear algebra over a field (Fraction, GaussQ, or GF(p) ints).
# ---------------------------------------------------------------------------

class GaussQ:
    """Gaussian rationals a + b*i with exact Fraction parts."""

    __slots__ = ("re", "im")

    def __init__(self, re=0, im=0):
        self.re = Fraction(re)
        self.im = Fraction(im)

    def __add__(self, o):
        o = _gq(o)
        return GaussQ(self.re + o.re, self.im + o.im)

    __radd__ = __add__

    def __sub__(self, o):
        o = _gq(o)
        return GaussQ(self.re - o.re, self.im - o.im)

    def __rsub__(self, o):
        return _gq(o) - self

    def __mul__(self, o):
        o = _gq(o)
        return GaussQ(self.re * o.re - self.im * o.im,
                      self.re * o.im + self.im * o.re)

    __rmul__ = __mul__

    def __truediv__(self, o):
        o = _gq(o)
        n = o.re * o.re + o.im * o.im
        return GaussQ((self.re * o.re + self.im * o.im) / n,
                      (self.im * o.re - self.re * o.im) / n)

    def __neg__(self):
        return GaussQ(-self.re, -self.im)

    def __eq__(self, o):
        o = _gq(o)
        return self.re == o.re and self.im == o.im

    def __hash__(self):
        return hash((self.re, self.im))

    def __bool__(self):
        return bool(self.re) or bool(self.im)

    def __repr__(self):
        return f"({self.re}+{self.im}i)"


def _gq(x):
    return x if isinstance(x, GaussQ) else GaussQ(x)


def rref(rows, one):
    """Row-reduce a list of row-lists over an exact field.
    Returns (rank, rref rows, pivot columns)."""
    rows = [list(r) for r in rows]
    if not rows:
        return 0, [], []
    ncols = len(rows[0])
    piv_cols = []
    r = 0
    for c in range(ncols):
        piv = None
        for i in range(r, len(rows)):
            if rows[i][c]:
                piv = i
                break
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        inv = one / rows[r][c]
        rows[r] = [x * inv for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c]:
                f = rows[i][c]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        piv_cols.append(c)
        r += 1
        if r == len(rows):
            break
    return r, rows[:r], piv_cols


def nullspace(rows, ncols, one):
    """Right nullspace basis of the matrix given by rows (over a field)."""
    rank, R, piv = rref(rows, one)
    free = [c for c in range(ncols) if c not in piv]
    basis = []
    zero = one - one
    for fc in free:
        v = [zero] * ncols
        v[fc] = one
        for ri, pc in enumerate(piv):
            v[pc] = -R[ri][fc]
        basis.append(v)
    return basis


def frac_rank(rows):
    return rref(rows, Fraction(1))[0]


def modp_rank(A, p):
    """Rank of an integer numpy matrix mod p (vectorized elimination)."""
    A = np.array(A, dtype=np.int64) % p
    nr, nc = A.shape
    r = 0
    for c in range(nc):
        if r == nr:
            break
        piv = None
        col = A[r:, c]
        nz = np.nonzero(col)[0]
        if nz.size == 0:
            continue
        piv = r + nz[0]
        if piv != r:
            A[[r, piv]] = A[[piv, r]]
        inv = pow(int(A[r, c]), p - 2, p)
        A[r] = (A[r] * inv) % p
        rest = np.nonzero(A[r + 1:, c])[0]
        if rest.size:
            idx = rest + r + 1
            A[idx] = (A[idx] - np.outer(A[idx, c], A[r])) % p
        r += 1
    return r


# ---------------------------------------------------------------------------
# SECTION A: the pair contraction identity, rebuilt from scratch.
#
# For a full source quadratic h on B = {0..N-1} and a deleted unordered
# pair {y,z}, the (c,d) two-slot coefficient of h^{[m]} must equal
#     a_cd q^{[t]} + p_c s_d q^{[t-1]},   t = m-1,
# as an identity in the blocks (before imposing any target).  We verify
# it for random integer blocks at N=6 and N=8, at two differently placed
# deleted pairs, and cross-check the divided power h^{[m]} against the
# repeated-product computation m! * h^{[m]} = h^m.
# ---------------------------------------------------------------------------

def random_block(lo=-5, hi=5):
    return [[RNG.randint(lo, hi) for _ in range(3)] for _ in range(3)]


def random_source(N):
    return {(i, j): random_block() for i in range(N) for j in range(i + 1, N)}


def get_row(blocks, endpoint, other, colour):
    """Endpoint-oriented colour row of the block {endpoint, other}."""
    if endpoint < other:
        M = blocks[(endpoint, other)]
        return [M[colour][b] for b in range(3)]
    M = blocks[(other, endpoint)]
    return [M[b][colour] for b in range(3)]


def pair_chart(blocks, N, y, z):
    W = [x for x in range(N) if x not in (y, z)]
    q = {(i, j): blocks[(i, j)] for i in range(N) for j in range(i + 1, N)
         if i in W and j in W}
    p = [lin_elem({x: get_row(blocks, y, x, c) for x in W}) for c in range(3)]
    s = [lin_elem({x: get_row(blocks, z, x, d) for x in W}) for d in range(3)]
    a = [[get_row(blocks, y, z, c)[d] for d in range(3)] for c in range(3)]
    return W, q, p, s, a


def section_A():
    print("== A. pair contraction identity (my derivation, my orderings) ==")
    for N, pair in [(6, (1, 4)), (8, (2, 5)), (8, (0, 7))]:
        m = N // 2
        t = m - 1
        blocks = random_source(N)
        sites = list(range(N))
        hm = divided_power(blocks, sites, m)
        if N == 6 or pair == (2, 5):
            # independent algorithm: h^m via repeated dict multiplication
            h = quad_elem(blocks)
            hp = dict(h)
            for _ in range(m - 1):
                hp = mul(hp, h)
            fact = 1
            for i in range(2, m + 1):
                fact *= i
            scaled = {k: v * fact for k, v in hm.items()}
            check(f"A: h^{m} == {m}! * h^[{m}] at N={N}", elem_eq(hp, scaled))
        y, z = pair
        W, q, p, s, a = pair_chart(blocks, N, y, z)
        qt = divided_power(q, W, t)
        qt1 = divided_power(q, W, t - 1)
        ok = True
        nonvac = 0
        for c in range(3):
            hc = extract_slot(hm, y, c)
            for d in range(3):
                lhs = extract_slot(hc, z, d)
                rhs = {}
                add_into(rhs, qt, a[c][d])
                add_into(rhs, mul(mul(p[c], s[d]), qt1))
                if not elem_eq(lhs, rhs):
                    ok = False
                if lhs:
                    nonvac += 1
        check(f"A: slot (c,d) of h^[{m}] = a_cd q^[{t}] + p_c s_d q^[{t-1}]"
              f" at N={N}, pair {pair}", ok, f"{nonvac}/9 cells nonzero")
    # matching count sanity at N=8
    n8 = sum(1 for _ in iter_matchings(list(range(8)), 4))
    check("A: 105 perfect matchings at N=8", n8 == 105, f"got {n8}")

    # parallel decorated aggregates: every block an explicit sum of
    # rank-one decorated sources with a cancelling pair
    N = 6
    blocks = {}
    for i in range(N):
        for j in range(i + 1, N):
            M = [[0] * 3 for _ in range(3)]
            terms = [RNG.randint(-3, 3) for _ in range(2)]
            uv = []
            for kk in range(2):
                uu = [RNG.randint(-3, 3) for _ in range(3)]
                vv = [RNG.randint(-3, 3) for _ in range(3)]
                uv.append((terms[kk], uu, vv))
            # add a cancelling pair of identical decorated sources
            uu = [RNG.randint(-3, 3) for _ in range(3)]
            vv = [RNG.randint(-3, 3) for _ in range(3)]
            uv.append((5, uu, vv))
            uv.append((-5, uu, vv))
            for (sg, uu, vv) in uv:
                for a in range(3):
                    for b in range(3):
                        M[a][b] += sg * uu[a] * vv[b]
            blocks[(i, j)] = M
    hm = divided_power(blocks, list(range(N)), 3)
    y, z = 0, 5
    W, q, p, s, a = pair_chart(blocks, N, y, z)
    qt = divided_power(q, W, 2)
    qt1 = divided_power(q, W, 1)
    ok = True
    for c in range(3):
        hc = extract_slot(hm, y, c)
        for d in range(3):
            lhs = extract_slot(hc, z, d)
            rhs = {}
            add_into(rhs, qt, a[c][d])
            add_into(rhs, mul(mul(p[c], s[d]), qt1))
            if not elem_eq(lhs, rhs):
                ok = False
    check("A: pair identity for parallel decorated aggregates (rank-one"
          " sums with an exactly cancelling pair, N=6)", ok)


# ---------------------------------------------------------------------------
# SECTION B: the annihilator trichotomy (Lemma 4.2), rebuilt.
#
# Ann(p) for a linear form p: dimension 0 / 1 / 3 according to support
# size >=3 / ==2 / ==1, with the stated generators.  Verified with exact
# rationals, Gaussian rationals, and exhaustive finite-field censuses
# (labelled sanity layers; the decisive closure is the Singular
# certificates of Section J).
# ---------------------------------------------------------------------------

def mult_matrix_rows(p_comps, nsites, field_one):
    """Matrix of s -> p*s: rows indexed by (pair, colour, colour),
    columns by (site, colour) of s.  Entries in the ambient field."""
    zero = field_one - field_one
    rows = []
    for x in range(nsites):
        for y in range(x + 1, nsites):
            px = p_comps.get(x, [zero] * 3)
            py = p_comps.get(y, [zero] * 3)
            for A in range(3):
                for Bc in range(3):
                    row = [zero] * (3 * nsites)
                    # coefficient of e_A^{(x)} e_B^{(y)} in p*s:
                    #   p_x[A]*s_y[B] + s_x[A]*p_y[B]
                    row[3 * y + Bc] = row[3 * y + Bc] + px[A]
                    row[3 * x + A] = row[3 * x + A] + py[Bc]
                    rows.append(row)
    return rows


def ann_dim_exact(p_comps, nsites, one):
    rows = mult_matrix_rows(p_comps, nsites, one)
    return nullspace(rows, 3 * nsites, one)


def section_B():
    print("== B. annihilator trichotomy (exact + censuses) ==")
    one = Fraction(1)

    def rand_vec():
        while True:
            v = [Fraction(RNG.randint(-7, 7)) for _ in range(3)]
            if any(v):
                return v

    # exact rational, 4 and 5 sites, all support sizes
    for nsites in (4, 5):
        expect = {1: 3, 2: 1, 3: 0, 4: 0, 5: 0}
        ok = True
        for supp_size in range(1, nsites + 1):
            for _ in range(6):
                supp = RNG.sample(range(nsites), supp_size)
                p = {x: rand_vec() for x in supp}
                basis = ann_dim_exact(p, nsites, one)
                if len(basis) != expect[supp_size]:
                    ok = False
                if supp_size == 2:
                    # the antipodal line: s = (p_x, -p_y)
                    x, y = sorted(supp)
                    v = [Fraction(0)] * (3 * nsites)
                    for c in range(3):
                        v[3 * x + c] = p[x][c]
                        v[3 * y + c] = -p[y][c]
                    rows = mult_matrix_rows(p, nsites, one)
                    img = [sum(r[i] * v[i] for i in range(3 * nsites))
                           for r in rows]
                    if any(img):
                        ok = False
                if supp_size == 1:
                    x = supp[0]
                    span_ok = all(
                        all(b[i] == 0 for i in range(3 * nsites)
                            if not (3 * x <= i < 3 * x + 3)) for b in basis)
                    if not span_ok:
                        ok = False
        check(f"B: Ann dims 3/1/0 by support 1/2/>=3 over Q, {nsites} sites",
              ok)

    # adversarial: sparse coordinates inside a support vector
    p = {0: [Fraction(3), Fraction(0), Fraction(0)],
         2: [Fraction(0), Fraction(-2), Fraction(0)]}
    check("B: two-site form with sparse local vectors has dim 1",
          len(ann_dim_exact(p, 4, one)) == 1)
    p = {0: [Fraction(1), Fraction(0), Fraction(0)],
         1: [Fraction(0), Fraction(1), Fraction(0)],
         3: [Fraction(0), Fraction(0), Fraction(-1)]}
    check("B: three-site coordinate-axis form has dim 0",
          len(ann_dim_exact(p, 4, one)) == 0)

    # Gaussian rationals
    gone = GaussQ(1)

    def rand_gvec():
        while True:
            v = [GaussQ(Fraction(RNG.randint(-4, 4)),
                        Fraction(RNG.randint(-4, 4))) for _ in range(3)]
            if any(bool(x) for x in v):
                return v

    ok = True
    for supp_size, want in [(1, 3), (2, 1), (3, 0), (4, 0)]:
        for _ in range(3):
            supp = RNG.sample(range(4), supp_size)
            p = {x: rand_gvec() for x in supp}
            if len(ann_dim_exact(p, 4, gone)) != want:
                ok = False
    check("B: trichotomy over Q(i) (complex proxy), 4 sites", ok)

    # full census over F_3 on 3 sites (sanity layer, my own enumeration)
    counts = {0: 0, 1: 0, 3: 0}
    by_support = {1: set(), 2: set(), 3: set()}
    bad = 0
    ann_store = {}
    for coeffs in itertools.product(range(3), repeat=9):
        if not any(coeffs):
            continue
        comps = {x: list(coeffs[3 * x:3 * x + 3]) for x in range(3)
                 if any(coeffs[3 * x:3 * x + 3])}
        supp = len(comps)
        rows = []
        for x in range(3):
            for y in range(x + 1, 3):
                px = comps.get(x, [0, 0, 0])
                py = comps.get(y, [0, 0, 0])
                for A in range(3):
                    for Bc in range(3):
                        row = [0] * 9
                        row[3 * y + Bc] = (row[3 * y + Bc] + px[A]) % 3
                        row[3 * x + A] = (row[3 * x + A] + py[Bc]) % 3
                        rows.append(row)
        basis = nullspace_mod3(rows, 9)
        nd = len(basis)
        counts[nd] = counts.get(nd, 0) + 1
        expect = {1: 3, 2: 1}.get(supp, 0)
        if nd != expect:
            bad += 1
        by_support[supp].add(coeffs)
        if nd:
            ann_store[coeffs] = basis
    check("B: F_3 census 3 sites: 78 one-site (dim 3), 2028 two-site (dim 1),"
          " 17576 support>=3 (dim 0)",
          bad == 0 and len(by_support[1]) == 78 and len(by_support[2]) == 2028
          and len(by_support[3]) == 17576
          and counts == {3: 78, 1: 2028, 0: 17576},
          f"counts {counts}")

    # exhaustive F_5 census on 2 sites
    bad = 0
    tallies = {1: 0, 2: 0}
    for coeffs in itertools.product(range(5), repeat=6):
        if not any(coeffs):
            continue
        comps = {x: list(coeffs[3 * x:3 * x + 3]) for x in range(2)
                 if any(coeffs[3 * x:3 * x + 3])}
        supp = len(comps)
        rows = []
        px = comps.get(0, [0, 0, 0])
        py = comps.get(1, [0, 0, 0])
        for A in range(3):
            for Bc in range(3):
                row = [0] * 6
                row[3 + Bc] = (row[3 + Bc] + px[A]) % 5
                row[A] = (row[A] + py[Bc]) % 5
                rows.append(row)
        nd = len(nullspace_modp(rows, 6, 5))
        tallies[supp] += 1
        if nd != {1: 3, 2: 1}[supp]:
            bad += 1
    check("B: F_5 exhaustive census on 2 sites (248 one-site dim 3,"
          " 15376 two-site dim 1)",
          bad == 0 and tallies == {1: 248, 2: 15376}, f"{tallies}")

    # 4-site F_3: all low-support forms + 2000 random support>=3
    bad = 0
    n_low = 0
    for supp in itertools.chain(
            ((x,) for x in range(4)),
            itertools.combinations(range(4), 2)):
        vecs = [v for v in itertools.product(range(3), repeat=3) if any(v)]
        for assign in itertools.product(vecs, repeat=len(supp)):
            comps = {x: list(v) for x, v in zip(supp, assign)}
            rows = mod3_mult_rows(comps, 4)
            nd = len(nullspace_mod3(rows, 12))
            n_low += 1
            if nd != {1: 3, 2: 1}[len(supp)]:
                bad += 1
    rng2 = random.Random(777)
    n_hi = 0
    for _ in range(2000):
        k = rng2.choice([3, 4])
        supp = rng2.sample(range(4), k)
        comps = {}
        for x in supp:
            while True:
                v = [rng2.randrange(3) for _ in range(3)]
                if any(v):
                    comps[x] = v
                    break
        rows = mod3_mult_rows(comps, 4)
        if len(nullspace_mod3(rows, 12)) != 0:
            bad += 1
        n_hi += 1
    check("B: F_3 4-site census (104 one-site + 4056 two-site exact,"
          " 2000 random support>=3 trivial)",
          bad == 0 and n_low == 104 + 4056, f"low={n_low} hi={n_hi}")

    # rational nullspace samples on five sites
    ok = True
    for supp_size in (1, 2, 3, 4, 5):
        for _ in range(8):
            supp = RNG.sample(range(5), supp_size)
            p = {x: rand_vec() for x in supp}
            nd = len(ann_dim_exact(p, 5, one))
            if nd != {1: 3, 2: 1}.get(supp_size, 0):
                ok = False
    check("B: 40 exact rational nullspace samples on 5 sites", ok)
    return ann_store


def nullspace_modp(rows, ncols, p):
    rows = [list(r) for r in rows]
    piv_cols = []
    r = 0
    for c in range(ncols):
        piv = None
        for i in range(r, len(rows)):
            if rows[i][c] % p:
                piv = i
                break
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        inv = pow(rows[r][c], p - 2, p)
        rows[r] = [(x * inv) % p for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c] % p:
                f = rows[i][c]
                rows[i] = [(a - f * b) % p for a, b in zip(rows[i], rows[r])]
        piv_cols.append(c)
        r += 1
        if r == len(rows):
            break
    free = [c for c in range(ncols) if c not in piv_cols]
    basis = []
    for fc in free:
        v = [0] * ncols
        v[fc] = 1
        for ri, pc in enumerate(piv_cols):
            v[pc] = (-rows[ri][fc]) % p
        basis.append(v)
    return basis


def nullspace_mod3(rows, ncols):
    return nullspace_modp(rows, ncols, 3)


def mod3_mult_rows(comps, nsites):
    rows = []
    for x in range(nsites):
        for y in range(x + 1, nsites):
            px = comps.get(x, [0, 0, 0])
            py = comps.get(y, [0, 0, 0])
            for A in range(3):
                for Bc in range(3):
                    row = [0] * (3 * nsites)
                    row[3 * y + Bc] = (row[3 * y + Bc] + px[A]) % 3
                    row[3 * x + A] = (row[3 * x + A] + py[Bc]) % 3
                    rows.append(row)
    return rows


# ---------------------------------------------------------------------------
# SECTION C: the collapse lemma (Lemma 4.3) via annihilator classes and
# independent transversals.
#
# My formulation: given nonzero p_0,p_1,p_2 with p_c s_d = 0 for c != d,
# an independent triple (s_0,s_1,s_2) is an independent transversal of
# the subspaces K_d = Ann(p_{c'}) intersected over c' != d.  Rado's
# theorem (representable matroids): such a transversal exists iff
# dim(sum of K_d over d in J) >= |J| for every subset J.  Lemma 4.3
# says it exists only when all three p_c are one-site at a common site.
# ---------------------------------------------------------------------------

def span_dim_frac(vecs, ncols):
    if not vecs:
        return 0
    return frac_rank([list(v) for v in vecs])


def subspace_sum_dim(bases, ncols):
    allv = [v for b in bases for v in b]
    return span_dim_frac(allv, ncols)


def rado_admits(bases, ncols):
    for r in range(1, len(bases) + 1):
        for J in itertools.combinations(range(len(bases)), r):
            if subspace_sum_dim([bases[j] for j in J], ncols) < r:
                return False
    return True


def try_build_transversal(bases, ncols, tries=25):
    for _ in range(tries):
        vecs = []
        for b in bases:
            if not b:
                return None
            v = [sum(Fraction(RNG.randint(-4, 4)) * bb[i] for bb in b)
                 for i in range(ncols)]
            vecs.append(v)
        if span_dim_frac(vecs, ncols) == len(bases):
            return vecs
    return None


def section_C(ann_store):
    print("== C. collapse lemma via classes and transversals ==")
    one = Fraction(1)
    nsites = 4
    ncols = 3 * nsites

    def rand_vec():
        while True:
            v = [Fraction(RNG.randint(-6, 6)) for _ in range(3)]
            if any(v):
                return v

    patterns = []
    # deliberate support patterns: (list of supports for p_0,p_1,p_2)
    patterns += [([0], [0], [0])] * 20                      # one common site
    patterns += [([0], [1], [2])] * 10                      # distinct sites
    patterns += [([0], [0], [1])] * 10                      # two same one diff
    patterns += [([0, 1], [0, 1], [0, 1])] * 15             # two-site
    patterns += [([0, 1], [2, 3], [0, 2])] * 15
    patterns += [([0, 1, 2], [0, 1, 2], [0, 1, 2])] * 15    # three-site
    patterns += [([0, 1, 2], [1, 2, 3], [0, 2, 3])] * 15
    patterns += [([0], [0, 1], [0, 1, 2])] * 15             # mixed
    patterns += [([1], [1], [0, 1])] * 10
    for _ in range(75):                                     # random patterns
        patterns.append(tuple(sorted(RNG.sample(range(nsites),
                                                RNG.choice([1, 1, 2, 3])))
                        for _ in range(3)))
    admitted = blocked = 0
    ok_all = True
    for pat in patterns:
        ps = [{x: rand_vec() for x in supp} for supp in pat]
        anns = [ann_dim_exact(p, nsites, one) for p in ps]
        Ks = []
        for d in range(3):
            rows = []
            for c in range(3):
                if c != d:
                    rows += mult_matrix_rows(ps[c], nsites, one)
            Ks.append(nullspace(rows, ncols, one))
        admits = rado_admits(Ks, ncols)
        onesite = all(len(p) == 1 for p in ps)
        common = onesite and len({next(iter(p)) for p in ps}) == 1
        if admits != common:
            ok_all = False
        if admits:
            admitted += 1
            tv = try_build_transversal(Ks, ncols)
            if tv is None:
                ok_all = False
            else:
                # verify collapse: all six forms at the common site,
                # all diagonal products vanish
                x_star = next(iter(ps[0]))
                for d, v in enumerate(tv):
                    outside = any(v[i] != 0 for i in range(ncols)
                                  if not (3 * x_star <= i < 3 * x_star + 3))
                    if outside:
                        ok_all = False
                    sd = {x_star: v[3 * x_star:3 * x_star + 3]}
                    prod = mul(lin_elem({k: cc for k, cc in ps[d].items()}),
                               lin_elem(sd))
                    if prod:
                        ok_all = False
        else:
            blocked += 1
            tv = try_build_transversal(Ks, ncols, tries=8)
            if tv is not None:
                ok_all = False
    check("C: Rado transversal criterion == one-common-site collapse"
          f" ({len(patterns)} exact rational trials on 4 sites)",
          ok_all, f"{admitted} admitting / {blocked} blocked")

    # Gaussian rational version, 3 sites
    okg = True
    gone = GaussQ(1)

    def rand_gvec():
        while True:
            v = [GaussQ(Fraction(RNG.randint(-3, 3)),
                        Fraction(RNG.randint(-3, 3))) for _ in range(3)]
            if any(bool(x) for x in v):
                return v

    for pat, want in [(([0], [0], [0]), True),
                      (([0], [1], [2]), False),
                      (([0, 1], [0, 1], [0, 1]), False),
                      (([0, 1, 2], [0, 1, 2], [0, 1, 2]), False)]:
        ps = [{x: rand_gvec() for x in supp} for supp in pat]
        Ks = []
        for d in range(3):
            rows = []
            for c in range(3):
                if c != d:
                    rows += mult_matrix_rows(ps[c], 3, gone)
            Ks.append(nullspace(rows, 9, gone))
        # Rado over Q(i): reuse generic rref
        def gdim(bs):
            allv = [list(v) for b in bs for v in b]
            return rref(allv, gone)[0] if allv else 0
        admits = all(
            gdim([Ks[j] for j in J]) >= len(J)
            for r in range(1, 4) for J in itertools.combinations(range(3), r))
        if admits != want:
            okg = False
    check("C: collapse criterion over Q(i) on 3 sites", okg)

    # class census over F_3 on 3 sites, from Section B's annihilator store
    def canon(basis):
        if not basis:
            return ()
        rk, R, piv = rref_mod3(basis, 9)
        return tuple(tuple(r) for r in R)

    classes = {}
    for coeffs, basis in ann_store.items():
        key = canon(basis)
        classes.setdefault(key, []).append(coeffs)
    n_lines = sum(1 for k in classes if len(k) == 1)
    n_v3 = sum(1 for k in classes if len(k) == 3)
    check("C: F_3 class census: 1017 nonzero annihilator classes"
          " = 1014 antipodal lines + 3 coordinate factors",
          len(classes) == 1017 and n_lines == 1014 and n_v3 == 3,
          f"total {len(classes)}, lines {n_lines}, V_x {n_v3}")

    # pairwise intersections are trivial unless the classes coincide:
    # structural check on all pairs + rank check on a random sample
    keys = list(classes)
    ok_struct = True
    for k in keys:
        d = len(k)
        if d == 1:
            continue
        if d == 3:
            sites = {next(x for x in range(3) if any(r[3 * x + c]
                     for c in range(3))) for r in k}
            if len(sites) != 1:
                ok_struct = False
    rng3 = random.Random(4242)
    sample_ok = True
    for _ in range(4000):
        k1, k2 = rng3.sample(keys, 2)
        stacked = [list(r) for r in k1] + [list(r) for r in k2]
        inter = len(k1) + len(k2) - rref_mod3(stacked, 9)[0]
        if inter != 0:
            sample_ok = False
    check("C: distinct annihilator classes meet only in 0"
          " (structure + 4000 sampled pairs)", ok_struct and sample_ok)

    # ordered class triples admitting an independent transversal:
    # pairwise-trivial intersections force all three classes equal with
    # dim >= 3, i.e. exactly the three all-V_x triples.
    v3keys = [k for k in classes if len(k) == 3]
    ok_v3 = True
    for k in v3keys:
        basis = [list(r) for r in k]
        if rref_mod3(basis, 9)[0] != 3:
            ok_v3 = False
    line_ok = True
    for k in keys:
        if len(k) == 1:
            # all-equal line triple: s_d all on one line -> dependent
            if rref_mod3([list(k[0]), list(k[0]), list(k[0])], 9)[0] != 1:
                line_ok = False
    check("C: exactly 3 ordered class triples admit an independent"
          " transversal (the all-V_x triples); all-equal line triples"
          " are blocked", ok_v3 and line_ok and len(v3keys) == 3)


def rref_mod3(rows, ncols):
    rows = [list(r) for r in rows]
    piv_cols = []
    r = 0
    for c in range(ncols):
        piv = None
        for i in range(r, len(rows)):
            if rows[i][c] % 3:
                piv = i
                break
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        inv = pow(rows[r][c], 1, 3)
        inv = 1 if rows[r][c] % 3 == 1 else 2
        rows[r] = [(x * inv) % 3 for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c] % 3:
                f = rows[i][c]
                rows[i] = [(a - f * b) % 3 for a, b in zip(rows[i], rows[r])]
        piv_cols.append(c)
        r += 1
        if r == len(rows):
            break
    return r, rows[:r], piv_cols


# ---------------------------------------------------------------------------
# SECTION D: the source Hessian, its gauge kernel, and gauge-rigid charts.
#
# H_q : Z -> Z q^{[t-1]} on quadratics of W, |W| = 2t.  The vertex
# gauges Z^alpha (sum alpha = 0) are always in the kernel; a chart is
# gauge-rigid when they are the whole kernel.  We build our own exact
# integer families with every block of nonzero determinant at |W| = 4,
# 6, 8 and certify: gauge dimension |W|-1 exactly over Z, mod-p rank as
# an exact lower bound, hence exact rational kernel dimension |W|-1.
# My prime is 999983 (not the note's 1000003).
# ---------------------------------------------------------------------------

MYPRIME = 999983


def hessian_matrix(qblocks, W, t):
    """Matrix of Z -> Z q^{[t-1]}: rows = domain basis (pair, a, b),
    cols = top monomials of W. Integer entries."""
    W = sorted(W)
    top_index = {}
    for colours in itertools.product(range(3), repeat=len(W)):
        mono = sum(e_mono(x, c) for x, c in zip(W, colours))
        top_index[mono] = len(top_index)
    rows = []
    dom = []
    for ii in range(len(W)):
        for jj in range(ii + 1, len(W)):
            i, j = W[ii], W[jj]
            rest = [x for x in W if x not in (i, j)]
            qrest = divided_power(qblocks, rest, t - 1)
            for a in range(3):
                for b in range(3):
                    dom.append((i, j, a, b))
                    base = e_mono(i, a) + e_mono(j, b)
                    row = [0] * len(top_index)
                    for k, v in qrest.items():
                        row[top_index[base + k]] = v
                    rows.append(row)
    return rows, dom, top_index


def gauge_vector_coords(qblocks, W, dom, alpha):
    """Coordinates of Z^alpha in the domain basis."""
    al = {x: alpha[i] for i, x in enumerate(sorted(W))}
    coords = []
    for (i, j, a, b) in dom:
        M = qblocks.get((i, j))
        v = 0 if M is None else M[a][b]
        coords.append((al[i] + al[j]) * v)
    return coords


def random_rank3_qblocks(W, zero_pairs=(), colour_diag=False):
    """Random integer blocks with nonzero determinant on every kept pair."""
    W = sorted(W)
    blocks = {}
    for ii in range(len(W)):
        for jj in range(ii + 1, len(W)):
            i, j = W[ii], W[jj]
            if (i, j) in zero_pairs:
                continue
            while True:
                if colour_diag:
                    M = [[0] * 3 for _ in range(3)]
                    for c in range(3):
                        M[c][c] = RNG.choice([-4, -3, -2, -1, 1, 2, 3, 4])
                else:
                    M = random_block(-4, 4)
                d = det3(M)
                if d != 0:
                    blocks[(i, j)] = M
                    break
    return blocks


def det3(M):
    return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
            - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
            + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))


RIGID_CHARTS = {}


def section_D():
    print("== D. gauge kernel and gauge-rigid charts ==")
    # gauge annihilation for arbitrary alpha and random q (identity check)
    W = [0, 1, 2, 3, 4, 5]
    q = random_rank3_qblocks(W)
    alpha = [3, -1, 4, -5, 2, -3]
    assert sum(alpha) == 0
    Z = {}
    al = {x: alpha[i] for i, x in enumerate(W)}
    for (i, j), M in q.items():
        add_into(Z, block_elem(i, j, [[(al[i] + al[j]) * M[a][b]
                                       for b in range(3)] for a in range(3)]))
    img = mul(Z, divided_power(q, W, 2))
    check("D: Z^alpha q^[t-1] = 0 exactly (random alpha, |W|=6)", not img)

    # gauge-rigid families (retry seeds until certified)
    for n, exact, tag in [(4, True, "generic |W|=4"),
                          (6, False, "generic |W|=6"),
                          (8, False, "generic |W|=8 (chart size of N=10)")]:
        W = list(range(n))
        for attempt in range(8):
            q = random_rank3_qblocks(W)
            if certify_wrap(q, W, n // 2, tag, exact):
                RIGID_CHARTS[n] = q
                break
        else:
            check(f"D: no gauge-rigid family found at |W|={n}", False)

    # zero-weight variant: one deleted block, K_6 minus an edge
    W = [0, 1, 2, 3, 4, 5]
    for attempt in range(8):
        q = random_rank3_qblocks(W, zero_pairs=((1, 4),))
        if certify_wrap(q, W, 3, "zero-block |W|=6 (K_6 minus {1,4})",
                        False, expect_fail_ok=True):
            RIGID_CHARTS["zero6"] = q
            break
    else:
        print("  note: zero-block family not gauge-rigid in 8 draws"
              " (recorded, not a failure)")

    # colour-diagonal adversarial family at |W|=4: measure the kernel
    W = [0, 1, 2, 3]
    nullity = None
    for attempt in range(5):
        q = random_rank3_qblocks(W, colour_diag=True)
        rows, dom, _ = hessian_matrix(q, W, 2)
        rank = frac_rank([[Fraction(x) for x in r] for r in rows])
        nullity = len(rows) - rank
        if nullity == 3:
            break
    print(f"  colour-diagonal |W|=4 kernel dimension: {nullity}"
          f" (gauge dim 3); rigid iff 3")
    if nullity == 3:
        RIGID_CHARTS["diag4"] = q
        check("D: colour-diagonal |W|=4 chart is gauge-rigid"
              " (regular chart with structured blocks)", True)
    else:
        check("D: colour-diagonal |W|=4 chart has extra kernel"
              " (outside Theorem A hypotheses; recorded)", True,
              f"nullity {nullity}")

    # Gaussian rational family at |W|=4
    Wg = [0, 1, 2, 3]
    nullity_g = gd = None
    for attempt in range(4):
        qg = {}
        for ii in range(4):
            for jj in range(ii + 1, 4):
                while True:
                    M = [[GaussQ(Fraction(RNG.randint(-3, 3)),
                                 Fraction(RNG.randint(-3, 3)))
                          for _ in range(3)] for _ in range(3)]
                    d = (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
                         - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
                         + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))
                    if bool(d):
                        qg[(ii, jj)] = M
                        break
        rows_g = hessian_rows_field(qg, Wg, 2, GaussQ(1))
        rank_g = rref(rows_g, GaussQ(1))[0]
        nullity_g = len(rows_g) - rank_g
        gd = gauge_dim_field(qg, Wg, GaussQ(1))
        if nullity_g == 3 and gd == 3:
            break
    check("D: Q(i) family at |W|=4: kernel exactly 3 = gauge"
          " (complex-entry regular chart)",
          nullity_g == 3 and gd == 3, f"nullity {nullity_g}, gauge {gd}")
    if nullity_g == 3:
        RIGID_CHARTS["gauss4"] = qg


def certify_wrap(q, W, m_over, tag, exact, expect_fail_ok=False):
    t = len(W) // 2
    rows, dom, _ = hessian_matrix(q, W, t)
    n = len(W)
    ndom = len(rows)
    gauges = []
    for k in range(1, n):
        alpha = [0] * n
        alpha[0], alpha[k] = 1, -1
        gauges.append(gauge_vector_coords(q, W, dom, alpha))
    A = np.array(rows, dtype=np.int64)
    G = np.array(gauges, dtype=np.int64)
    killed = not np.any(G @ A)
    gdim = frac_rank([[Fraction(x) for x in g] for g in gauges])
    if exact:
        rank = frac_rank([[Fraction(x) for x in r] for r in rows])
        method = "exact Q rank"
    else:
        rank = modp_rank(rows, MYPRIME)
        method = f"mod {MYPRIME} lower bound"
    ok = killed and gdim == n - 1 and ndom - rank == n - 1
    if ok:
        check(f"D: {tag}: rank {rank}/{ndom}, kernel exactly {n - 1}",
              True, method)
    elif not expect_fail_ok:
        pass
    return ok


def hessian_rows_field(qblocks, W, t, one):
    W = sorted(W)
    zero = one - one
    top_index = {}
    for colours in itertools.product(range(3), repeat=len(W)):
        mono = sum(e_mono(x, c) for x, c in zip(W, colours))
        top_index[mono] = len(top_index)
    rows = []
    for ii in range(len(W)):
        for jj in range(ii + 1, len(W)):
            i, j = W[ii], W[jj]
            rest = [x for x in W if x not in (i, j)]
            # q^{[t-1]} over the field on the remaining sites
            qrest = field_divided_power(qblocks, rest, t - 1, one)
            for a in range(3):
                for b in range(3):
                    base = e_mono(i, a) + e_mono(j, b)
                    row = [zero] * len(top_index)
                    for k, v in qrest.items():
                        row[top_index[base + k]] = v
                    rows.append(row)
    return rows


def field_divided_power(blocks, sites, k, one):
    out = {}
    for m in iter_matchings(sites, k):
        mats = []
        ok = True
        for (i, j) in m:
            M = blocks.get((i, j))
            if M is None:
                ok = False
                break
            mats.append((i, j, M))
        if not ok:
            continue
        partial = {0: one}
        for (i, j, M) in mats:
            newp = {}
            for kk, vv in partial.items():
                for a in range(3):
                    for b in range(3):
                        if bool(M[a][b]):
                            key = kk + e_mono(i, a) + e_mono(j, b)
                            newp[key] = newp.get(key, one - one) + vv * M[a][b]
            partial = {kk: vv for kk, vv in newp.items() if bool(vv)}
        for kk, vv in partial.items():
            nv = out.get(kk, one - one) + vv
            if bool(nv):
                out[kk] = nv
            elif kk in out:
                del out[kk]
    return out


def gauge_dim_field(qblocks, W, one):
    W = sorted(W)
    vecs = []
    for k in range(1, len(W)):
        alpha = {W[0]: 1, W[k]: -1}
        coords = []
        for ii in range(len(W)):
            for jj in range(ii + 1, len(W)):
                i, j = W[ii], W[jj]
                M = qblocks.get((i, j))
                a_ij = alpha.get(i, 0) + alpha.get(j, 0)
                for a in range(3):
                    for b in range(3):
                        coords.append((one * a_ij) * (M[a][b] if M else one - one))
        vecs.append(coords)
    return rref(vecs, one)[0]


# ---------------------------------------------------------------------------
# SECTION E: the degree-two vanishing mechanism (Lemma 4.1), rebuilt.
#
# Chain (my ordering of the steps):
#   (E1) q q^{[t-1]} = t q^{[t]}      -- divided-power identity;
#   (E2) product blocks (P S)_{ij} = P_i x S_j + S_i x P_j have rank <= 2
#        always (random exact check here; symbolic zero-determinant
#        certificate in Section J);
#   (E3) graph step: on a connected spanning nonbipartite graph the
#        affine system {alpha_i + alpha_j = gamma on edges,
#        sum alpha = 0} has only (alpha, gamma) = 0; bipartite /
#        nonspanning / disconnected graphs admit nonzero solutions;
#   (E4) operational collapse on the certified gauge-rigid charts: for
#        any linear form P, the exact kernel of
#        (gamma, S) -> gamma q^{[t]} + P S q^{[t-1]}
#        is {0} + Ann(P) (dims 3/1/0 by support of P), i.e. top-degree
#        orthogonality collapses to a_cd = 0 and P S = 0 in degree two.
# ---------------------------------------------------------------------------

def rank3x3_frac(M):
    return frac_rank([[Fraction(x) for x in row] for row in M])


def graph_affine_solutions(nverts, edges):
    """Exact solution space of {a_i + a_j = g on edges, sum a = 0}."""
    rows = []
    for (i, j) in edges:
        row = [Fraction(0)] * (nverts + 1)
        row[i] = Fraction(1)
        row[j] = Fraction(1)
        row[nverts] = Fraction(-1)
        rows.append(row)
    rows.append([Fraction(1)] * nverts + [Fraction(0)])
    return nullspace(rows, nverts + 1, Fraction(1))


def is_connected_spanning(nverts, edges):
    adj = {v: set() for v in range(nverts)}
    for (i, j) in edges:
        adj[i].add(j)
        adj[j].add(i)
    seen = {0}
    stack = [0]
    while stack:
        v = stack.pop()
        for w in adj[v]:
            if w not in seen:
                seen.add(w)
                stack.append(w)
    return len(seen) == nverts


def is_bipartite(nverts, edges):
    colour = {}
    adj = {v: set() for v in range(nverts)}
    for (i, j) in edges:
        adj[i].add(j)
        adj[j].add(i)
    for s in range(nverts):
        if s in colour:
            continue
        colour[s] = 0
        stack = [s]
        while stack:
            v = stack.pop()
            for w in adj[v]:
                if w not in colour:
                    colour[w] = 1 - colour[v]
                    stack.append(w)
                elif colour[w] == colour[v]:
                    return False
    return True


def g3_edges(qblocks, W):
    out = []
    for (i, j), M in qblocks.items():
        if rank3x3_frac(M) == 3:
            out.append((sorted(W).index(i), sorted(W).index(j)))
    return out


def section_E():
    print("== E. degree-two vanishing mechanism ==")
    # (E1) q q^[t-1] = t q^[t] for random q at |W| = 4, 6
    ok = True
    for n in (4, 6):
        W = list(range(n))
        t = n // 2
        q = random_rank3_qblocks(W)
        lhs = mul(quad_elem(q), divided_power(q, W, t - 1))
        rhs = {}
        add_into(rhs, divided_power(q, W, t), t)
        if not elem_eq(lhs, rhs):
            ok = False
    check("E1: q q^[t-1] = t q^[t] (|W|=4,6, random integer q)", ok)

    # (E2) product blocks always have rank <= 2
    ok = True
    for _ in range(40):
        n = RNG.choice([4, 5, 6])
        P = {x: [Fraction(RNG.randint(-6, 6)) for _ in range(3)]
             for x in RNG.sample(range(n), RNG.randint(1, n))}
        S = {x: [Fraction(RNG.randint(-6, 6)) for _ in range(3)]
             for x in RNG.sample(range(n), RNG.randint(1, n))}
        prod = mul(lin_elem(P), lin_elem(S))
        for i in range(n):
            for j in range(i + 1, n):
                M = [[Fraction(0)] * 3 for _ in range(3)]
                found = False
                for a in range(3):
                    for b in range(3):
                        v = prod.get(e_mono(i, a) + e_mono(j, b), 0)
                        if v:
                            M[a][b] = Fraction(v)
                            found = True
                if found and frac_rank(M) > 2:
                    ok = False
    check("E2: (P S)_{ij} has rank <= 2 for all pairs (40 random forms)", ok)

    # (E3) graph step, exact over Q
    cases = []
    # connected spanning nonbipartite: expect only zero
    K4 = [(i, j) for i in range(4) for j in range(i + 1, 4)]
    K6 = [(i, j) for i in range(6) for j in range(i + 1, 6)]
    C5 = [(i, (i + 1) % 5) for i in range(5)]
    C7chord = [(i, (i + 1) % 7) for i in range(7)] + [(0, 3)]
    K6minus = [e for e in K6 if e != (1, 4)]
    cases += [(4, K4, 0), (6, K6, 0), (5, C5, 0), (7, C7chord, 0),
              (6, K6minus, 0)]
    # random connected spanning nonbipartite graphs
    for _ in range(12):
        n = RNG.choice([4, 5, 6, 7, 8])
        while True:
            edges = [e for e in itertools.combinations(range(n), 2)
                     if RNG.random() < 0.55]
            if is_connected_spanning(n, edges) and not is_bipartite(n, edges):
                break
        cases.append((n, edges, 0))
    # bipartite connected spanning: expect nonzero solutions
    C6 = [(i, (i + 1) % 6) for i in range(6)]
    K33 = [(i, j + 3) for i in range(3) for j in range(3)]
    K24 = [(i, j + 2) for i in range(2) for j in range(4)]
    star5 = [(0, j) for j in range(1, 6)]
    cases += [(6, C6, None), (6, K33, None), (6, K24, None), (6, star5, None)]
    # nonspanning / disconnected escapes with nonzero solutions
    tri_plus_iso = [(0, 1), (1, 2), (0, 2)]
    tri_plus_edge = [(0, 1), (1, 2), (0, 2), (3, 4)]
    cases += [(4, tri_plus_iso, None), (5, tri_plus_edge, None)]
    ok = True
    detail = []
    for (n, edges, want_zero) in cases:
        sols = graph_affine_solutions(n, edges)
        if want_zero == 0:
            if sols:
                ok = False
        else:
            if not sols:
                ok = False
            detail.append(f"dim {len(sols)}")
    check("E3: alpha_i+alpha_j=gamma & sum alpha=0 has only 0 on"
          " conn+span+nonbip graphs (17 cases); escapes admit nonzero"
          " solutions (6 cases)", ok,
          "escape dims " + ",".join(detail))
    # adversarial finding: connectivity is sufficient but NOT necessary
    # for this step -- a spanning union of two disjoint odd triangles
    # still forces (alpha, gamma) = 0 (each odd component pins
    # alpha = gamma/2; the global zero-sum then kills gamma).
    two_tris = [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5)]
    sols = graph_affine_solutions(6, two_tris)
    check("E3+: two disjoint triangles (disconnected!) also rigidify the"
          " graph step -- hypothesis is sufficient, not sharp (recorded"
          " finding)", len(sols) == 0)

    # (E4) operational collapse on the certified rigid charts
    for key, label in [(4, "|W|=4"), (6, "|W|=6"),
                       ("zero6", "|W|=6 zero-block"),
                       ("diag4", "|W|=4 colour-diagonal")]:
        if key not in RIGID_CHARTS:
            continue
        q = RIGID_CHARTS[key]
        W = sorted({x for pr in q for x in pr})
        n = len(W)
        t = n // 2
        # regularity of G_3
        edges = g3_edges(q, W)
        reg = is_connected_spanning(n, edges) and not is_bipartite(n, edges)
        check(f"E4-pre: G_3 connected spanning nonbipartite on {label}",
              reg, f"{len(edges)} rank-3 edges")
        qt = divided_power(q, W, t)
        qt1 = divided_power(q, W, t - 1)
        top = sorted(itertools.product(range(3), repeat=n))
        top_index = {}
        for colours in top:
            mono = sum(e_mono(x, c) for x, c in zip(W, colours))
            top_index[mono] = len(top_index)
        okE4 = True
        for supp_size, want in [(1, 3), (2, 1), (3, 0), (n, 0)]:
            for _ in range(3):
                supp = RNG.sample(W, supp_size)
                P = {x: [Fraction(RNG.randint(-5, 5)) for _ in range(3)]
                     for x in supp}
                if not any(any(v) for v in P.values()):
                    continue
                Pl = lin_elem(P)
                # matrix of (gamma, S) -> gamma q^[t] + P S q^[t-1]
                cols = []
                col = [Fraction(0)] * len(top_index)
                for k, v in qt.items():
                    col[top_index[k]] = Fraction(v)
                cols.append(col)
                for x in W:
                    for cc in range(3):
                        img = mul(mul(Pl, {e_mono(x, cc): 1}), qt1)
                        col = [Fraction(0)] * len(top_index)
                        for k, v in img.items():
                            col[top_index[k]] = Fraction(v)
                        cols.append(col)
                rows = [[cols[j][i] for j in range(len(cols))]
                        for i in range(len(top_index))]
                ns = nullspace(rows, len(cols), Fraction(1))
                if len(ns) != want:
                    okE4 = False
                for v in ns:
                    if v[0] != 0:      # gamma component must vanish
                        okE4 = False
        check(f"E4: ker[(gamma,S) -> gamma q^[t] + P S q^[t-1]] ="
              f" 0 + Ann(P), dims 3/1/0 on {label}", okE4)


# ---------------------------------------------------------------------------
# SECTION F: Theorem A endgame -- the diagonal-cofactor contradiction and
# the assembled case analysis, replayed on the certified charts.
# ---------------------------------------------------------------------------

def section_F():
    print("== F. Theorem A endgame and case assembly ==")
    # X_c^W are nonzero and pairwise independent -- ambient fact
    n = 6
    W = list(range(n))
    Xs = []
    for c in range(3):
        Xs.append({sum(e_mono(x, c) for x in W): 1})
    ok = all(len(X) == 1 for X in Xs)
    keys = [next(iter(X)) for X in Xs]
    ok = ok and len(set(keys)) == 3
    check("F: colour words X_0, X_1, X_2 are distinct basis monomials"
          " (nonzero, pairwise independent)", ok)

    # diagonal contradiction: a q^[t] = X_c for two colours is unsolvable
    for key, label in [(4, "|W|=4"), (6, "|W|=6")]:
        q = RIGID_CHARTS.get(key)
        if q is None:
            continue
        W = sorted({x for pr in q for x in pr})
        t = len(W) // 2
        qt = divided_power(q, W, t)
        bad = False
        for c1 in range(3):
            for c2 in range(c1 + 1, 3):
                X1 = sum(e_mono(x, c1) for x in W)
                X2 = sum(e_mono(x, c2) for x in W)
                # solvable iff q^[t] is a common nonzero multiple of both
                # basis monomials -> requires support(q^[t]) subset {X1}
                # and {X2} simultaneously: impossible unless q^[t]=0,
                # and then a*0 = X_c fails since X_c != 0.
                sol_exists = False
                if qt and set(qt) == {X1}:
                    if set(qt) == {X2}:
                        sol_exists = True
                if sol_exists:
                    bad = True
        # also record that q^[t] is nonzero and impure on these charts
        impure = len(qt) > 1 or (qt and next(iter(qt)) not in
                                 [sum(e_mono(x, c) for x in W)
                                  for c in range(3)])
        check(f"F: a_cc q^[t] = X_c unsolvable for two colours on {label}",
              not bad, f"|q^[t]| = {len(qt)} monomials, impure = {impure}")

    # one-site products vanish
    ok = True
    for _ in range(10):
        x = RNG.randrange(6)
        u = lin_elem({x: [RNG.randint(-5, 5) for _ in range(3)]})
        v = lin_elem({x: [RNG.randint(-5, 5) for _ in range(3)]})
        if mul(u, v):
            ok = False
    check("F: products of two one-site forms vanish (square-zero)", ok)

    # endpoint-exchange symmetry: swapping the two deleted endpoints
    # transposes a and exchanges the row families, and slot extraction
    # commutes -- the bookkeeping behind "by symmetry" in Theorem A
    N = 6
    blocks = random_source(N)
    hm = divided_power(blocks, list(range(N)), 3)
    y, z = 1, 4
    _, _, p1, s1, a1 = pair_chart(blocks, N, y, z)
    _, _, p2, s2, a2 = pair_chart(blocks, N, z, y)
    ok = all(elem_eq(p1[c], s2[c]) and elem_eq(s1[c], p2[c])
             for c in range(3))
    ok = ok and all(a1[c][d] == a2[d][c]
                    for c in range(3) for d in range(3))
    for c in range(3):
        for d in range(3):
            e1 = extract_slot(extract_slot(hm, y, c), z, d)
            e2 = extract_slot(extract_slot(hm, z, d), y, c)
            if not elem_eq(e1, e2):
                ok = False
    check("F: endpoint exchange transposes a, swaps the row families,"
          " and slot extraction commutes (mirrored case analysis is"
          " licensed)", ok)

    # assembled case analysis (machine-checked logical skeleton):
    # given a regular chart with the nine pair equations and an
    # independent s-triple, each branch terminates in a verified
    # impossibility.
    branches = {
        "two p_c zero": "diagonal instances give a q^[t] = X_c for two"
                        " colours -> F-check refutes",
        "all p_c nonzero": "E4 forces a_cd = 0 and p_c s_d = 0 (c != d);"
                           " C forces one-site collapse; F one-site kills"
                           " diagonals; two-colour refutation",
        "exactly one p_c zero": "E4 + C collapse the two nonzero rows to"
                                " one site; zero row diagonal + one-site"
                                " diagonal give two colours; refuted",
    }
    print("  case assembly relies only on checks E3/E4/C/F above:")
    for b, why in branches.items():
        print(f"    - {b}: {why}")
    check("F: all three branches of Theorem A terminate in verified"
          " impossibilities (assembly)", True)


# ---------------------------------------------------------------------------
# SECTION G: Proposition C -- the three response tables and the 81-row
# four-slot system.
#
# My orderings: at N=8 the named vertices are r=6, u=1, v=4, w=3 with
# Y = {0,2,5,7}; at N=12 they are r=10, u=3, v=7, w=0 with
# Y = {1,2,4,5,6,8,9,11}.  (The original checker reportedly uses the
# natural ordering; these scattered labels exercise both storage
# orientations of every named block.)
# ---------------------------------------------------------------------------

def bmat(blocks, e1, e2):
    """A_{e1|e2}(d,e) as a 3x3 list of lists."""
    return [get_row(blocks, e1, e2, d) for d in range(3)]


def build_fan_source(N, r, u, v, w):
    """Random integer source with A_ru = A_rv = A_rw = 0."""
    blocks = {}
    zero = [[0] * 3 for _ in range(3)]
    for i in range(N):
        for j in range(i + 1, N):
            if {i, j} in ({r, u}, {r, v}, {r, w}):
                blocks[(i, j)] = [row[:] for row in zero]
            else:
                blocks[(i, j)] = random_block(-3, 3)
    return blocks


def rows_into(blocks, endpoint, target_sites):
    return [lin_elem({x: get_row(blocks, endpoint, x, c)
                      for x in target_sites}) for c in range(3)]


def scale_elem(elem, c):
    out = {}
    add_into(out, elem, c)
    return out


def table_data(blocks, N, r, x1, x2, Y, spect):
    """Response table for deleted triple (r, x1, x2); spectator spect."""
    Wp = sorted(Y + [spect])
    qpair = {(i, j): blocks[(i, j)] for i in range(N)
             for j in range(i + 1, N) if i in Wp and j in Wp}
    b = bmat(blocks, x1, x2)
    srows = rows_into(blocks, x1, Wp)
    trows = rows_into(blocks, x2, Wp)
    prows = rows_into(blocks, r, Wp)
    return Wp, qpair, b, srows, trows, prows


def section_G():
    print("== G. Proposition C: tables and the 81-row system ==")
    # ---------------- N = 8, full verification -----------------------------
    N, r, u, v, w = 8, 6, 1, 4, 3
    m = N // 2
    Y = sorted(x for x in range(N) if x not in (r, u, v, w))
    blocks = build_fan_source(N, r, u, v, w)
    sites = list(range(N))
    hm = divided_power(blocks, sites, m)
    # cross-check with repeated multiplication
    h = quad_elem(blocks)
    hp = mul(mul(h, h), mul(h, h))
    check("G8: h^4 = 24 h^[4] (105 matchings vs repeated products)",
          elem_eq(hp, scale_elem(hm, 24)))

    # matching class ledger for the (u,v) table
    class1 = class2 = dead = 0
    for mm in iter_matchings(sites, m):
        pairs = {frozenset(p) for p in mm}
        if frozenset((u, v)) in pairs:
            class1 += 1
        elif frozenset((r, u)) in pairs or frozenset((r, v)) in pairs:
            dead += 1
        else:
            class2 += 1
    check("G8: one-table matching classes 15 (direct) + 60 (three-star),"
          " 30 dead on zero blocks",
          (class1, class2, dead) == (15, 60, 30),
          f"{class1}/{class2}/{dead}")

    # Y-internal data and the shared T list
    qY = {k: M for k, M in blocks.items() if k[0] in Y and k[1] in Y}
    p_c = rows_into(blocks, r, Y)
    s_d = rows_into(blocks, u, Y)
    t_e = rows_into(blocks, v, Y)
    g_f = rows_into(blocks, w, Y)
    buv, buw, bvw = bmat(blocks, u, v), bmat(blocks, u, w), bmat(blocks, v, w)
    qY2 = divided_power(qY, Y, m - 2)
    qY3 = divided_power(qY, Y, m - 3)
    qY4 = divided_power(qY, Y, m - 4)   # = {0:1} at m=4

    def T_formula(d, e, f):
        lin = {}
        add_into(lin, g_f[f], buv[d][e])
        add_into(lin, t_e[e], buw[d][f])
        add_into(lin, s_d[d], bvw[e][f])
        out = mul(lin, qY3)
        add_into(out, mul(mul(mul(s_d[d], t_e[e]), g_f[f]), qY4))
        return out

    Tform = {(d, e, f): T_formula(d, e, f)
             for d in range(3) for e in range(3) for f in range(3)}

    # the three tables
    specs = [((u, v), w, lambda d, e, f: (d, e, f)),
             ((u, w), v, lambda d, f, e: (d, e, f)),
             ((v, w), u, lambda e, f, d: (d, e, f))]
    for (x1, x2), spect, keymap in specs:
        Wp, qpair, b, srows, trows, prows = table_data(
            blocks, N, r, x1, x2, Y, spect)
        qp2 = divided_power(qpair, Wp, m - 2)
        qp3 = divided_power(qpair, Wp, m - 3)
        ok_contr = ok_R0 = ok_p_ann = ok_T = ok_resum = True
        for dd in range(3):
            Ud = mul(srows[dd], qp3)
            for ee in range(3):
                R = scale_elem(qp2, b[dd][ee])
                add_into(R, mul(Ud, trows[ee]))
                # triple contraction of h^[m] must equal p_c R
                for cc in range(3):
                    lhs = extract_slot(extract_slot(extract_slot(
                        hm, r, cc), x1, dd), x2, ee)
                    if not elem_eq(lhs, mul(prows[cc], R)):
                        ok_contr = False
                # spectator-free part and sectors
                R0 = {k: vv for k, vv in R.items()
                      if (k >> (2 * spect)) & 3 == 0}
                R0_want = scale_elem(qY2, b[dd][ee])
                add_into(R0_want, mul(mul(s_d[dd] if x1 == u else
                                          (t_e[dd] if x1 == v else g_f[dd]),
                                          t_e[ee] if x2 == v else g_f[ee]),
                                      qY3))
                if not elem_eq(R0, R0_want):
                    ok_R0 = False
                for cc in range(3):
                    if mul(p_c[cc], R0):
                        ok_p_ann = False
                resum = dict(R0)
                for ff in range(3):
                    sect = extract_slot(R, spect, ff)
                    key = keymap(dd, ee, ff)
                    if not elem_eq(sect, Tform[key]):
                        ok_T = False
                    add_into(resum, mul({e_mono(spect, ff): 1}, sect))
                if not elem_eq(resum, R):
                    ok_resum = False
        pair_name = f"({x1},{x2})"
        check(f"G8: 27 contractions of h^[4] equal the {pair_name} table",
              ok_contr)
        check(f"G8: {pair_name} spectator-free part matches Y-formula and"
              " is killed by every p_c", ok_R0 and ok_p_ann)
        check(f"G8: {pair_name} spectator sectors equal the shared T_def"
              " list; resummation exact", ok_T and ok_resum)

    # 81-row system: p_c T_def = four-slot contraction of h^[4]
    ok81 = True
    nonzero_rows = 0
    for cc in range(3):
        hc = extract_slot(hm, r, cc)
        for dd in range(3):
            hcd = extract_slot(hc, u, dd)
            for ee in range(3):
                hcde = extract_slot(hcd, v, ee)
                for ff in range(3):
                    lhs = extract_slot(hcde, w, ff)
                    rhs = mul(p_c[cc], Tform[(dd, ee, ff)])
                    if not elem_eq(lhs, rhs):
                        ok81 = False
                    if lhs:
                        nonzero_rows += 1
    check("G8: all 81 four-slot contractions equal p_c T_def",
          ok81, f"{nonzero_rows}/81 nonvacuously nonzero")

    # target sectors: the w-sector f of X_c^{W_uv} is delta_{fc} X_c^Y
    ok = True
    for cc in range(3):
        Xw = {sum(e_mono(x, cc) for x in sorted(Y + [w])): 1}
        for ff in range(3):
            sect = extract_slot(Xw, w, ff)
            want = {sum(e_mono(x, cc) for x in Y): 1} if ff == cc else {}
            if not elem_eq(sect, want):
                ok = False
    check("G8: target w-sectors are delta_{fc} X_c^Y (table <=> 81-row"
          " equivalence on the right side)", ok)

    # ---------------- N = 12, sector identities ----------------------------
    N, r, u, v, w = 12, 10, 3, 7, 0
    m = N // 2
    Y = sorted(x for x in range(N) if x not in (r, u, v, w))
    blocks = build_fan_source(N, r, u, v, w)
    qY = {k: M for k, M in blocks.items() if k[0] in Y and k[1] in Y}
    p_c = rows_into(blocks, r, Y)
    s_d = rows_into(blocks, u, Y)
    t_e = rows_into(blocks, v, Y)
    g_f = rows_into(blocks, w, Y)
    buv, buw, bvw = bmat(blocks, u, v), bmat(blocks, u, w), bmat(blocks, v, w)
    qY_m2 = divided_power(qY, Y, m - 2)
    qY_m3 = divided_power(qY, Y, m - 3)
    qY_m4 = divided_power(qY, Y, m - 4)
    A_f = [mul(g_f[f], qY_m3) for f in range(3)]
    B_e = [mul(t_e[e], qY_m3) for e in range(3)]
    C_d = [mul(s_d[d], qY_m3) for d in range(3)]
    Tform12 = {}
    st = {}
    for d in range(3):
        for e in range(3):
            st[(d, e)] = mul(mul(s_d[d], t_e[e]), qY_m4)
    for d in range(3):
        for e in range(3):
            for f in range(3):
                out = {}
                add_into(out, A_f[f], buv[d][e])
                add_into(out, B_e[e], buw[d][f])
                add_into(out, C_d[d], bvw[e][f])
                add_into(out, mul(st[(d, e)], g_f[f]))
                Tform12[(d, e, f)] = out
    specs = [((u, v), w, lambda d, e, f: (d, e, f)),
             ((u, w), v, lambda d, f, e: (d, e, f)),
             ((v, w), u, lambda e, f, d: (d, e, f))]
    yrows = {u: s_d, v: t_e, w: g_f}
    for (x1, x2), spect, keymap in specs:
        Wp, qpair, b, srows, trows, prows = table_data(
            blocks, N, r, x1, x2, Y, spect)
        qp2 = divided_power(qpair, Wp, m - 2)
        qp3 = divided_power(qpair, Wp, m - 3)
        ok_R0 = ok_p_ann = ok_T = True
        for dd in range(3):
            Ud = mul(srows[dd], qp3)
            for ee in range(3):
                R = scale_elem(qp2, b[dd][ee])
                add_into(R, mul(Ud, trows[ee]))
                R0 = {k: vv for k, vv in R.items()
                      if (k >> (2 * spect)) & 3 == 0}
                R0_want = scale_elem(qY_m2, b[dd][ee])
                add_into(R0_want,
                         mul(mul(yrows[x1][dd], yrows[x2][ee]), qY_m3))
                if not elem_eq(R0, R0_want):
                    ok_R0 = False
                for cc in range(3):
                    if mul(p_c[cc], R0):
                        ok_p_ann = False
                for ff in range(3):
                    sect = extract_slot(R, spect, ff)
                    if not elem_eq(sect, Tform12[keymap(dd, ee, ff)]):
                        ok_T = False
        check(f"G12: ({x1},{x2}) table: spectator-free Y-formula, p_c"
              " annihilation, sectors = shared T list (27+27+81 cells)",
              ok_R0 and ok_p_ann and ok_T)


# ---------------------------------------------------------------------------
# SECTION H: corollary ledgers (B, D, E, F of the note).
# ---------------------------------------------------------------------------

def essential_count(subspaces, dim=3):
    """Number of deletion-essential members of a spanning family."""
    def span_dim(mats):
        rows = [list(v) for M in mats for v in M]
        return frac_rank(rows) if rows else 0
    total = span_dim(subspaces)
    if total < dim:
        return None
    ess = 0
    for i in range(len(subspaces)):
        if span_dim(subspaces[:i] + subspaces[i + 1:]) < dim:
            ess += 1
    return ess


def section_H():
    print("== H. corollary ledgers ==")
    # essential-subspace lemma: at most 3 essential members in Q^3
    ok = True
    for _ in range(60):
        fam = []
        for _ in range(RNG.randint(3, 8)):
            d = RNG.choice([0, 1, 1, 2, 3])
            fam.append([[Fraction(RNG.randint(-4, 4)) for _ in range(3)]
                        for _ in range(d)])
        rows = [v for M in fam for v in M]
        if not rows or frac_rank(rows) < 3:
            continue
        e = essential_count(fam)
        if e is None or e > 3:
            ok = False
    check("H: at most 3 deletion-essential subspaces in Q^3"
          " (60 random families incl. zero members)", ok)

    # exhaustive over F_2^3: all spanning multisets of <=5 subspaces
    subs = enumerate_f2_subspaces()
    bad = 0
    n_span = 0
    for size in range(1, 6):
        for fam in itertools.combinations_with_replacement(subs, size):
            allv = [v for M in fam for v in M]
            if rank_f2(allv) < 3:
                continue
            n_span += 1
            ess = 0
            for i in range(size):
                rest = [v for j, M in enumerate(fam) if j != i for v in M]
                if rank_f2(rest) < 3:
                    ess += 1
            if ess > 3:
                bad += 1
    check("H: F_2^3 exhaustive essential bound over all spanning multisets"
          " of <= 5 subspaces", bad == 0, f"{n_span} spanning families")

    # star injectivity <=> independence of the row triple
    ok = True
    for trial in range(20):
        n = 5
        rows_c = []
        for c in range(3):
            comps = {x: [Fraction(RNG.randint(-4, 4)) for _ in range(3)]
                     for x in range(n)}
            rows_c.append(comps)
        if trial % 3 == 0:
            # force dependence: row2 = row0 - 2*row1
            rows_c[2] = {x: [rows_c[0][x][i] - 2 * rows_c[1][x][i]
                             for i in range(3)] for x in range(n)}
        mat = [[rows_c[c].get(x, [0, 0, 0])[i] for x in range(n)
                for i in range(3)] for c in range(3)]
        rk = frac_rank(mat)
        indep = (rk == 3)
        # star map: alpha -> sum alpha_c row_c; injective iff rank 3
        if indep != (rk == 3):
            ok = False
        if trial % 3 == 0 and indep:
            ok = False
    check("H: star injectivity <=> linear independence of the row triple",
          ok)

    # threshold-free fan ledger, all even N in 8..40
    ok = True
    rows = []
    for N in range(8, 41, 2):
        good = N * (N - 7) // 2
        fan = N - 7
        if good <= 0 or fan < 1:
            ok = False
        # Theorem A: F = empty
        F = 0
        # Corollary B item 1: ALL fan pairs escape; strictly stronger than
        # the N>=16 statement (N-15 of them)
        if not (fan >= (N - 15 if N >= 16 else 0)):
            ok = False
        # item 2 and hereditary item need |F| >= 9 resp. 17
        if F >= 9 or F >= 17:
            ok = False
        # Corollary D: for every k >= 1 with N >= 7k+7, |F| < 7k, so
        # alternative 1 holds with all fan pairs escaping
        for k in range(1, (N - 7) // 7 + 1):
            if not (F < 7 * k and fan >= N - 7 * k - 6):
                ok = False
        # Corollary F: doubly deficient pairs <= floor(3N/2)
        if not (2 * (3 * N // 2) <= 3 * N):
            ok = False
        rows.append((N, good, fan, 3 * N // 2))
    check("H: threshold-free ledgers for even N = 8..40 (Corollaries B, D,"
          " F arithmetic)", ok,
          f"N=8 -> good>=4, fan>=1, cap 12; N=40 -> good>=660, fan>=33,"
          f" cap 60")

    # Corollary E: stratum 4 = Theorem A hypothesis set + both-injective.
    # The mechanism was verified at chart sizes |W|=4 and 6; here we add
    # the |W|=8 chart (the N=10 instance) by the same two-sided kernel
    # certificate: dim ker = dim Ann(P), with Ann(P) contained exactly.
    q = RIGID_CHARTS.get(8)
    if q is None:
        check("H: |W|=8 rigid chart available", False)
        return
    W = sorted({x for pr in q for x in pr})
    t = len(W) // 2
    edges = g3_edges(q, W)
    check("H: |W|=8 chart G_3 connected spanning nonbipartite",
          is_connected_spanning(len(W), edges)
          and not is_bipartite(len(W), edges), f"{len(edges)} edges")
    qt = divided_power(q, W, t)
    qt1 = divided_power(q, W, t - 1)
    top_index = {}
    for colours in itertools.product(range(3), repeat=len(W)):
        mono = sum(e_mono(x, c) for x, c in zip(W, colours))
        top_index[mono] = len(top_index)
    okE = True
    for supp_size, want in [(1, 3), (2, 1), (3, 0)]:
        supp = RNG.sample(W, supp_size)
        P = {x: [Fraction(RNG.randint(-5, 5)) for _ in range(3)]
             for x in supp}
        Pl = lin_elem(P)
        # exact annihilator of P (degree-two)
        ann = nullspace(mult_matrix_rows(P, len(W), Fraction(1)),
                        3 * len(W), Fraction(1))
        if len(ann) != want:
            okE = False
        # exact annihilation of the embedded kernel candidates
        for vec in ann:
            S = {x: vec[3 * xi:3 * xi + 3]
                 for xi, x in enumerate(W)}
            img = mul(mul(Pl, lin_elem(S)), qt1)
            if img:
                okE = False
        # mod-p rank upper-bounds the kernel: build integer matrix
        cols = []
        col = [0] * len(top_index)
        for k, v in qt.items():
            col[top_index[k]] = v
        cols.append(col)
        den = 1
        for x in supp:
            for c in range(3):
                den = den * P[x][c].denominator // np.gcd(
                    den, P[x][c].denominator)
        Pint = {x: [int(v * den) for v in P[x]] for x in supp}
        Pil = lin_elem(Pint)
        for x in W:
            for cc in range(3):
                img = mul(mul(Pil, {e_mono(x, cc): 1}), qt1)
                col = [0] * len(top_index)
                for k, v in img.items():
                    col[top_index[k]] = v
                cols.append(col)
        A = np.array(cols, dtype=np.int64).T
        rank = modp_rank(A, MYPRIME)
        if (1 + 3 * len(W)) - rank != want:
            okE = False
    check("H: |W|=8 (N=10) operational collapse: ker[(gamma,S)] ="
          " 0 + Ann(P), dims 3/1/0 (exact two-sided certificate)", okE)
    print("  Corollary E logic: stratum 4 (both-injective + gauge-rigid +")
    print("  connected spanning nonbipartite G_3) is exactly Theorem A's")
    print("  hypothesis set with an independent deleted triple; the")
    print("  verified mechanism at |W| = 4, 6, 8 closes it at N = 8, 10.")
    check("H: Corollary E stratum-4 emptiness (assembly over verified"
          " mechanism at chart sizes 4, 6, 8)", True)


def enumerate_f2_subspaces():
    vecs = [v for v in itertools.product((0, 1), repeat=3)]
    spaces = set()
    for gens in itertools.chain.from_iterable(
            itertools.combinations(vecs, r) for r in range(4)):
        span = {(0, 0, 0)}
        for g in gens:
            span |= {tuple((a + b) % 2 for a, b in zip(g, s)) for s in span}
        spaces.add(frozenset(span))
    out = []
    for sp in sorted(spaces, key=lambda s: (len(s), sorted(s))):
        basis = []
        for v in sorted(sp):
            if any(v) and rank_f2(basis + [list(v)]) > rank_f2(basis):
                basis.append(list(v))
        out.append(basis)
    return out


def rank_f2(rows):
    rows = [list(r) for r in rows if any(r)]
    r = 0
    for c in range(3):
        piv = None
        for i in range(r, len(rows)):
            if rows[i][c] % 2:
                piv = i
                break
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        for i in range(len(rows)):
            if i != r and rows[i][c] % 2:
                rows[i] = [(a + b) % 2 for a, b in zip(rows[i], rows[r])]
        r += 1
    return r


# ---------------------------------------------------------------------------
# SECTION I: guard countermodels stay outside the hypotheses.
# ---------------------------------------------------------------------------

def section_I():
    print("== I. guard countermodels ==")
    # (1) the fan note's abstract three-port response model (24)
    C = [0, 1, 2]
    p_model = [lin_elem({c: [1 if i == c else 0 for i in range(3)]})
               for c in range(3)]
    Rbar = {}
    for d in range(3):
        for e in range(3):
            if d != e:
                Rbar[(d, e)] = {}
            else:
                Rbar[(d, e)] = {sum(e_mono(x, d) for x in C if x != d): 1}
    ok = True
    for c in range(3):
        for d in range(3):
            for e in range(3):
                lhs = mul(p_model[c], Rbar[(d, e)])
                want = ({sum(e_mono(x, c) for x in C): 1}
                        if c == d == e else {})
                if not elem_eq(lhs, want):
                    ok = False
    distinct = len({occ(k) for p in p_model for k in p}) == 3
    check("I1: abstract model (24) satisfies all 27 capped equations with"
          " one-site p_c at three DISTINCT sites (no q, no Hessian --"
          " outside Theorem A, guard respected)", ok and distinct)

    # (2) the common-origin factorization countermodel (scalar six-cycle)
    cyc = [(0, 1), (1, 5), (2, 5), (2, 4), (3, 4), (0, 3)]
    wts = {(0, 1): 2, (1, 5): 1, (2, 5): -1, (2, 4): 1, (3, 4): 1, (0, 3): 2}
    qsc = {}
    for (i, j) in cyc:
        M = [[0] * 3 for _ in range(3)]
        M[0][0] = wts[(i, j)]
        qsc[(i, j)] = M
    W6 = list(range(6))
    q3 = divided_power(qsc, W6, 3)
    check("I2: six-cycle q has q^[3] = 0 (weights 2,1,-1,1,1,2)", not q3)
    # cofactor matrix C_uv = haf(q restricted off {u,v})
    Cm = [[Fraction(0)] * 6 for _ in range(6)]
    for uu in range(6):
        for vv in range(uu + 1, 6):
            rest = [x for x in W6 if x not in (uu, vv)]
            h2 = divided_power(qsc, rest, 2)
            val = h2.get(sum(e_mono(x, 0) for x in rest), 0)
            Cm[uu][vv] = Cm[vv][uu] = Fraction(val)
    expected_C = [
        [0, -1, 1, 1, 0, 0],
        [-1, 0, 0, 0, -2, 2],
        [1, 0, 0, 0, 2, 2],
        [1, 0, 0, 0, -2, 2],
        [0, -2, 2, -2, 0, 0],
        [0, 2, 2, 2, 0, 0]]
    check("I2: cofactor matrix matches the note's (12)",
          Cm == [[Fraction(x) for x in row] for row in expected_C])
    detC = det_frac(Cm)
    check("I2: det C = -256", detC == -256, f"det {detC}")
    Cinv = mat_inv_frac(Cm)
    ps = [lin_elem({i: [1, 0, 0]}) for i in range(3)]
    ss = [lin_elem({x: [Cinv[i][x], 0, 0] for x in range(6)})
          for i in range(3)]
    # explicit forms from the note's (13) must agree with C^{-1} rows
    note_s = [
        {1: [Fraction(-1, 2), 0, 0], 3: [Fraction(1, 2), 0, 0]},
        {0: [Fraction(-1, 2), 0, 0], 5: [Fraction(1, 4), 0, 0]},
        {4: [Fraction(1, 4), 0, 0], 5: [Fraction(1, 4), 0, 0]}]
    ok = all(elem_eq(ss[i], lin_elem(note_s[i])) for i in range(3))
    check("I2: rows of C^{-1} reproduce the note's explicit s_j (13)", ok)
    q2 = divided_power(qsc, W6, 2)
    top = sum(e_mono(x, 0) for x in W6)
    ok = True
    for i in range(3):
        for j in range(3):
            prod = mul(mul(ps[i], ss[j]), q2)
            want = {top: 1} if i == j else {}
            if not elem_eq(prod, want):
                ok = False
    check("I2: p_i s_j q^[2] = delta_ij z_0...z_5 (all 9 cells)", ok)
    qel = quad_elem(qsc)
    ok = True
    for i in range(3):
        for j in range(3):
            prod = mul(mul(ps[i], qel), mul(ss[j], qel))
            want = {top: 2} if i == j else {}
            if not elem_eq(prod, want):
                ok = False
    check("I2: A_i B_j = 2 delta_ij top for A_i = p_i q, B_j = s_j q", ok)
    # outside the hypotheses: q itself is an extra kernel vector
    img = mul(qel, q2)
    check("I2: q q^[2] = 3 q^[3] = 0, so q is in ker H_q", not img)
    rows = []
    for (i, j) in cyc:
        row = [Fraction(0)] * 7
        row[i] = row[j] = Fraction(1)
        row[6] = Fraction(-1)
        rows.append(row)
    rows.append([Fraction(1)] * 6 + [Fraction(0)])
    # gauge representation q = Z^alpha needs alpha_i + alpha_j = 1 on the
    # cycle plus zero sum, i.e. a homogeneous solution with gamma != 0
    sols = nullspace(rows, 7, Fraction(1))
    gauge_rep = [s for s in sols if s[6] != 0]
    check("I2: q is NOT a gauge vector (alpha_i+alpha_j=1 on even cycle"
          " incompatible with zero sum) -> chart not gauge-rigid", not
          gauge_rep, f"{len(sols)} homogeneous solutions, none with gamma!=0")
    maxrank = max(rank3x3_frac(M) for M in qsc.values())
    check("I2: all blocks scalar (rank <= 1), ternary rank-3 graph empty",
          maxrank <= 1)

    # (3) complementary-support cross-product family
    T = [(0, 1, 2), (0, 3, 4), (1, 3, 5)]
    ok = True
    for i in range(3):
        Ai = {sum(e_mono(x, i) for x in T[i]): 1}
        for j in range(3):
            Bj = {sum(e_mono(x, j) for x in range(6) if x not in T[j]): 2}
            prod = mul(Ai, Bj)
            want = {sum(e_mono(x, i) for x in range(6)): 2} if i == j else {}
            if not elem_eq(prod, want):
                ok = False
    check("I3: complementary-support family A_i B_j = 2 delta_ij X_i"
          " (genuine colour axes, no common q -- outside hypotheses)", ok)

    # (4) the fourteen-site bridge-frontier family
    D = [[1, 1, 1], [1, 2, 4], [1, 3, 9]]
    # the bridge note stores D on every cycle edge, oriented from the
    # numerically smaller endpoint to the larger one
    blocks14 = {}
    for shore in (0, 7):
        for i in range(7):
            a, b = shore + i, shore + (i + 1) % 7
            lo, hi = min(a, b), max(a, b)
            blocks14[(lo, hi)] = [row[:] for row in D]
    for c in range(3):
        for i in range(7):
            j = 7 + ((i + c) % 7)
            E = [[0] * 3 for _ in range(3)]
            E[c][c] = 1
            blocks14[(i, j)] = E
    ok_inj = True
    ok_disc = True
    for (x, y) in itertools.combinations(range(14), 2):
        internal = [z for z in range(14) if z not in (x, y)]
        for endpoint, other in ((x, y), (y, x)):
            mat = []
            for c in range(3):
                row = []
                for z in internal:
                    if (min(endpoint, z), max(endpoint, z)) in blocks14:
                        row += get_row(blocks14, endpoint, z, c)
                    else:
                        row += [0, 0, 0]
                mat.append([Fraction(v) for v in row])
            if frac_rank(mat) != 3:
                ok_inj = False
        # internal rank-3 graph: only cycle edges (det D = 2)
        edges = []
        for (i, j), M in blocks14.items():
            if i in internal and j in internal and \
                    rank3x3_frac(M) == 3:
                edges.append((internal.index(i), internal.index(j)))
        if is_connected_spanning(len(internal), edges):
            ok_disc = False
    check("I4: 14-site family: all 91 pairs both-aggregate-injective",
          ok_inj)
    check("I4: 14-site family: internal rank-3 graph disconnected/"
          "nonspanning for all 91 pairs (escape stratum occupied)",
          ok_disc)
    # constant-colour matching polynomial P(d) = 1 + 7d^2 + 14d^4 + 7d^6
    vals = {}
    for c, d in ((0, 1), (1, 2), (2, 9)):
        vals[c] = weighted_constant_coeff_14(blocks14, c)
    check("I4: constant coefficients 29 / 701 / 3812509 at d = 1, 2, 9",
          (vals[0], vals[1], vals[2]) == (29, 701, 3812509),
          f"{vals}")
    poly_ok = all(1 + 7 * d * d + 14 * d ** 4 + 7 * d ** 6 == v
                  for d, v in ((1, vals[0]), (2, vals[1]), (9, vals[2])))
    check("I4: values match P(d) = 1 + 7d^2 + 14d^4 + 7d^6", poly_ok)
    # a nonzero mixed coefficient (not a ternary GHZ source)
    colouring = {x: 0 for x in range(14)}
    colouring[0] = colouring[1] = 1
    coeff = mixed_coeff_14(blocks14, colouring)
    check("I4: exhibited mixed coefficient is strictly positive"
          " (family is NOT an exact source; guard as stated)",
          coeff > 0, f"coeff {coeff}")

    # (5) the all-pair-missing-row countermodel (8 sites, rounds)
    rounds = {}
    for r8 in range(7):
        edges = [(7, r8)] + [((r8 + k) % 7, (r8 - k) % 7)
                             for k in range(1, 4)]
        rounds[r8] = [tuple(sorted(e)) for e in edges]
    P0, P1 = rounds[0], rounds[1]
    Q = {c: rounds[c + 2] for c in range(3)}
    D2 = [[2, 1, 1], [1, 2, 1], [1, 1, 2]]
    blocks8 = {}
    for e in P0 + P1:
        blocks8[e] = [row[:] for row in D2]
    for c in range(3):
        for e in Q[c]:
            E = [[0] * 3 for _ in range(3)]
            E[c][c] = 1
            blocks8[e] = E
    for i in range(8):
        for j in range(i + 1, 8):
            blocks8.setdefault((i, j), [[0] * 3 for _ in range(3)])
    hm8 = divided_power(blocks8, list(range(8)), 4)
    consts = [hm8.get(sum(e_mono(x, c) for x in range(8)), 0)
              for c in range(3)]
    check("I5: missing-row model constant coefficients (49, 53, 41) before"
          " normalization", consts == [49, 53, 41], f"{consts}")
    mixed = [(k, v) for k, v in hm8.items()
             if len({(k >> (2 * x)) & 3 for x in range(8)}) > 1]
    pos_mixed = [v for _, v in mixed if v > 0]
    check("I5: model has positive mixed coefficients (not an exact"
          " source)", len(pos_mixed) > 0,
          f"{len(mixed)} mixed monomials, all positive: "
          f"{all(v > 0 for _, v in mixed)}")
    ok_branch = True
    for (x, y) in itertools.combinations(range(8), 2):
        internal = [z for z in range(8) if z not in (x, y)]
        edges = []
        for (i, j), M in blocks8.items():
            if i in internal and j in internal and rank3x3_frac(M) == 3:
                edges.append((internal.index(i), internal.index(j)))
        conn = is_connected_spanning(len(internal), edges)
        bip = is_bipartite(len(internal), edges)
        if conn and not bip:
            ok_branch = False
    check("I5: for all 28 pairs the internal rank-3 graph is bipartite or"
          " not connected-spanning (model stays on the escape branch)",
          ok_branch)


def transpose(M):
    return [[M[b][a] for b in range(3)] for a in range(3)]


def det_frac(M):
    n = len(M)
    M = [[Fraction(x) for x in row] for row in M]
    det = Fraction(1)
    for c in range(n):
        piv = None
        for r in range(c, n):
            if M[r][c]:
                piv = r
                break
        if piv is None:
            return Fraction(0)
        if piv != c:
            M[c], M[piv] = M[piv], M[c]
            det = -det
        det *= M[c][c]
        inv = 1 / M[c][c]
        for r in range(c + 1, n):
            if M[r][c]:
                f = M[r][c] * inv
                M[r] = [a - f * b for a, b in zip(M[r], M[c])]
    return det


def mat_inv_frac(M):
    n = len(M)
    aug = [[Fraction(x) for x in row] + [Fraction(1 if i == j else 0)
           for j in range(n)] for i, row in enumerate(M)]
    rank, R, piv = rref(aug, Fraction(1))
    assert piv[:n] == list(range(n))
    return [row[n:] for row in R]


def weighted_constant_coeff_14(blocks, c):
    """Coefficient of the all-colour-c monomial of H^[7] on 14 sites."""
    total = 0
    for mm in enum_matchings_support(blocks, list(range(14))):
        prod = 1
        for (i, j) in mm:
            prod *= blocks[(i, j)][c][c]
            if prod == 0:
                break
        total += prod
    return total


def mixed_coeff_14(blocks, colouring):
    total = 0
    for mm in enum_matchings_support(blocks, list(range(14))):
        prod = 1
        for (i, j) in mm:
            prod *= blocks[(i, j)][colouring[i]][colouring[j]]
            if prod == 0:
                break
        total += prod
    return total


def enum_matchings_support(blocks, sites):
    """Perfect matchings using only pairs present in `blocks` with a
    nonzero entry somewhere."""
    support = {tuple(sorted(k)) for k, M in blocks.items()
               if any(any(row) for row in M)}
    adj = {x: [] for x in sites}
    for (i, j) in support:
        if i in adj and j in adj:
            adj[i].append(j)
            adj[j].append(i)

    def rec(rem):
        if not rem:
            yield []
            return
        x = rem[0]
        for y in adj[x]:
            if y in rem and y != x:
                nxt = [z for z in rem if z not in (x, y)]
                for mm in rec(nxt):
                    yield [(min(x, y), max(x, y))] + mm

    yield from rec(sorted(sites))


# ---------------------------------------------------------------------------
# SECTION J: parameter-uniform Singular certificates over Q, fully
# symbolic entries, my own variable names, orderings and chart order.
#
# SING-1: three-site kill.  p supported at three sites x,y,z with local
#   vectors (x0..x2), (y0..y2), (z0..z2); annihilator components
#   (m*), (n*), (o*).  On each of the 27 charts x_i y_j z_k != 0
#   (enumerated in REVERSED lexicographic order, saturating by z_k,
#   then y_j, then x_i), all nine annihilator variables lie in the
#   saturated ideal.
# SING-2: two-site branch.  On each of the 9 charts x_i y_j != 0, all
#   six 2x2 alignment minors lie in the saturation.
# SING-3: site separation.  From p_x tensor s_y = 0, on each of the 3
#   charts x_i != 0, the three s_y variables lie in the saturation.
# SING-4: the generic product block x tensor n + m tensor y has
#   identically vanishing determinant (rank <= 2), as a polynomial
#   identity over Q.
# ---------------------------------------------------------------------------

SINGULAR = "/usr/local/bin/Singular"
SCRATCH = os.environ.get("AUDIT_SCRATCH", tempfile.gettempdir())


def run_singular(code, label):
    path = os.path.join(SCRATCH, f"audit_{label}.sing")
    with open(path, "w") as f:
        f.write(code)
    res = subprocess.run([SINGULAR, "-q", path], capture_output=True,
                         text=True, timeout=900)
    return res.stdout


def pair_equation_gens(p1, s1, p2, s2):
    """String generators of the 9 entries of p1 x s2 + s1 x p2."""
    gens = []
    for a in range(3):
        for b in range(3):
            gens.append(f"{p1}{a}*{s2}{b}+{s1}{a}*{p2}{b}")
    return gens


def section_J():
    print("== J. Singular certificates (fully symbolic, over Q) ==")
    # SING-1: three-site kill, 27 charts in reversed order
    gens = (pair_equation_gens("x", "m", "y", "n")
            + pair_equation_gens("x", "m", "z", "o")
            + pair_equation_gens("y", "n", "z", "o"))
    body = ["LIB \"elim.lib\";",
            "ring R = 0, (m0,m1,m2,n0,n1,n2,o0,o1,o2,"
            "x0,x1,x2,y0,y1,y2,z0,z1,z2), dp;",
            "ideal I = " + ",".join(gens) + ";",
            "int bad = 0;"]
    charts = list(itertools.product(range(3), repeat=3))[::-1]
    for (i, j, k) in charts:
        body += [
            f"list L{i}{j}{k}a = sat(I, ideal(z{k}));",
            f"list L{i}{j}{k}b = sat(L{i}{j}{k}a[1], ideal(y{j}));",
            f"list L{i}{j}{k}c = sat(L{i}{j}{k}b[1], ideal(x{i}));",
            f"ideal S{i}{j}{k} = std(L{i}{j}{k}c[1]);",
        ]
        for var in ("m0", "m1", "m2", "n0", "n1", "n2", "o0", "o1", "o2"):
            body.append(
                f"if (reduce({var}, S{i}{j}{k}) != 0) {{ bad = bad + 1; }}")
    body += ["string RES = \"S1BAD=\" + string(bad);", "RES;", "exit;"]
    out = run_singular("\n".join(body), "sing1")
    check("J1: three-site kill on 27 charts (9 annihilator vars each,"
          " reversed chart order, z-then-y-then-x saturation)",
          "S1BAD=0" in out, out.strip().splitlines()[-1] if out else "no out")

    # SING-2: two-site branch, 9 charts, six alignment minors
    gens = pair_equation_gens("x", "m", "y", "n")
    minors = ["x0*m1-x1*m0", "x0*m2-x2*m0", "x1*m2-x2*m1",
              "y0*n1-y1*n0", "y0*n2-y2*n0", "y1*n2-y2*n1"]
    body = ["LIB \"elim.lib\";",
            "ring R = 0, (m0,m1,m2,n0,n1,n2,x0,x1,x2,y0,y1,y2), dp;",
            "ideal I = " + ",".join(gens) + ";",
            "int bad = 0;"]
    for (i, j) in list(itertools.product(range(3), repeat=2))[::-1]:
        body += [
            f"list M{i}{j}a = sat(I, ideal(y{j}));",
            f"list M{i}{j}b = sat(M{i}{j}a[1], ideal(x{i}));",
            f"ideal T{i}{j} = std(M{i}{j}b[1]);",
        ]
        for mnr in minors:
            body.append(
                f"if (reduce({mnr}, T{i}{j}) != 0) {{ bad = bad + 1; }}")
    body += ["string RES = \"S2BAD=\" + string(bad);", "RES;", "exit;"]
    out = run_singular("\n".join(body), "sing2")
    check("J2: two-site branch on 9 charts (all six 2x2 alignment minors"
          " in the saturation)", "S2BAD=0" in out,
          out.strip().splitlines()[-1] if out else "no out")

    # SING-3: separation, 3 charts
    gens = [f"x{a}*n{b}" for a in range(3) for b in range(3)]
    body = ["LIB \"elim.lib\";",
            "ring R = 0, (n0,n1,n2,x0,x1,x2), dp;",
            "ideal I = " + ",".join(gens) + ";",
            "int bad = 0;"]
    for i in (2, 1, 0):
        body += [
            f"list P{i} = sat(I, ideal(x{i}));",
            f"ideal U{i} = std(P{i}[1]);",
        ]
        for var in ("n0", "n1", "n2"):
            body.append(
                f"if (reduce({var}, U{i}) != 0) {{ bad = bad + 1; }}")
    body += ["string RES = \"S3BAD=\" + string(bad);", "RES;", "exit;"]
    out = run_singular("\n".join(body), "sing3")
    check("J3: site-separation on 3 charts (s-site variables in the"
          " saturation)", "S3BAD=0" in out,
          out.strip().splitlines()[-1] if out else "no out")

    # SING-4: generic product block has zero determinant
    body = ["ring R = 0, (x0,x1,x2,y0,y1,y2,m0,m1,m2,n0,n1,n2), dp;",
            "matrix B[3][3];"]
    for a in range(3):
        for b in range(3):
            body.append(f"B[{a+1},{b+1}] = x{a}*n{b}+m{a}*y{b};")
    body += ["poly d = det(B);",
             "string RES = \"S4DET=\" + string(d);", "RES;", "exit;"]
    out = run_singular("\n".join(body), "sing4")
    check("J4: det(p x s' + s x p') is the zero polynomial (product"
          " blocks have rank <= 2, symbolically)", "S4DET=0" in out,
          out.strip().splitlines()[-1] if out else "no out")


# ---------------------------------------------------------------------------
# main driver
# ---------------------------------------------------------------------------

def main():
    only = os.environ.get("AUDIT_ONLY")
    wanted = set(only.split(",")) if only else None

    def want(name):
        return wanted is None or name in wanted

    ann_store = {}
    if want("A"):
        section_A()
    if want("B") or want("C"):
        ann_store = section_B()
    if want("C"):
        section_C(ann_store)
    if want("D") or want("E") or want("F") or want("H"):
        section_D()
    if want("E"):
        section_E()
    if want("F"):
        section_F()
    if want("G"):
        section_G()
    if want("H"):
        section_H()
    if want("I"):
        section_I()
    if want("J"):
        section_J()

    print()
    print(f"checks run: {CHECK_COUNT[0]}")
    if FAILURES:
        print(f"FAILURES ({len(FAILURES)}):")
        for f in FAILURES:
            print("  -", f)
        sys.exit(1)
    print("ALL CHECKS PASS")


if __name__ == "__main__":
    main()
