#!/usr/bin/env python3
r"""AUDIT A6-B10 -- independent re-implementation of the h=2 six-site cap
error, the general witness decision and the RANK-ONE witness decision.

Nothing here imports W14 or P2 code (except b10_verify_sources.py, which
cross-checks my source generator against theirs one time).

Conventions (from the audit spec, re-derived here):
  sites 0..5, colours 0..2, blocks A_{uv} for u<v, row index = colour at u.
  block(u,v,cu,cv) = A_{uv}[cu][cv] if u<v else A_{vu}[cv][cu].
  cap K = 3x3, variable k_{3i+j} = K_ij.
  For pair (p,q), U = the other four sites, word w: U -> {0,1,2}.
      s(K)    = sum_ij K_ij A_pq[i][j]
      P_a[i]  = block(p,a,i,w_a),  Q_a[j] = block(q,a,j,w_a)
      R_ab(K) = sum_ij K_ij (P_a[i] Q_b[j] + P_b[i] Q_a[j])
      x_ab    = block(a,b,w_a,w_b)
      E_w(K)  = sum_{M perfect matching of U}
                  sum_{J subset M, |J| <= h-2} s^|J| prod_{J} x_e prod_{M\J} R_f
  At h = 2 only J = {} survives:  E_w = sum_M R_e1 R_e2.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
import os
import random
import subprocess
import tempfile
import time

SITES = tuple(range(6))
ALLPAIRS = tuple(combinations(SITES, 2))
NK = 9                       # cap coordinates k0..k8, k_{3i+j} = K_ij
KAPPA = (0, 4, 8)            # k0,k4,k8  =  K_00,K_11,K_22
SINGULAR = "/usr/local/bin/Singular"


# ------------------------------------------------------------ my source gen
# Re-implementation of the P2 generator (seed + mode -> blocks) as a pure
# replay of a documented sequence of random.Random calls.  Order of the calls
# below is dictated by Python evaluation order in P2's comprehensions and is
# verified against P2's own build_source in b10_verify_sources.py.

def _mat_dense(rng, lo=-4, hi=4, density=1.0):
    out = []
    for _ in range(3):
        row = []
        for _ in range(3):
            # `X if C else Y` evaluates C first
            keep = rng.random() < density
            row.append(Fraction(rng.randint(lo, hi)) if keep else Fraction(0))
        out.append(row)
    return out


def _mat_rank(rng, rank, lo=-4, hi=4):
    while True:
        left = [[rng.randint(lo, hi) for _ in range(rank)] for _ in range(3)]
        right = [[rng.randint(lo, hi) for _ in range(3)] for _ in range(rank)]
        mat = [[Fraction(sum(left[i][t] * right[t][j] for t in range(rank)))
                for j in range(3)] for i in range(3)]
        if rank == 0 or _rank_of(mat) == rank:
            return mat


def _rank_of(mat):
    rows = [[Fraction(x) for x in row] for row in mat]
    rank = 0
    for col in range(len(rows[0])):
        piv = next((r for r in range(rank, len(rows)) if rows[r][col] != 0),
                   None)
        if piv is None:
            continue
        rows[rank], rows[piv] = rows[piv], rows[rank]
        head = rows[rank]
        for r in range(len(rows)):
            if r != rank and rows[r][col] != 0:
                f = rows[r][col] / head[col]
                rows[r] = [a - f * b for a, b in zip(rows[r], head)]
        rank += 1
    return rank


def _mat_diag(rng):
    mat = [[Fraction(0)] * 3 for _ in range(3)]
    for c in range(3):
        mat[c][c] = Fraction(rng.randint(-4, 4))
    return mat


def gen_source(seed, mode):
    """blocks[(u,v)] for u<v, exact Fractions."""
    rng = random.Random(seed)
    blocks = {}
    for pair in ALLPAIRS:
        if mode == "generic":
            blocks[pair] = _mat_dense(rng)
        elif mode == "sparse":
            blocks[pair] = _mat_dense(rng, density=0.35)
        elif mode == "lowrank":
            rk = rng.choice([0, 1, 1, 2])
            blocks[pair] = _mat_rank(rng, rk)
        elif mode == "diagonal":
            blocks[pair] = _mat_diag(rng)
        elif mode == "binary":
            blocks[pair] = [[Fraction(rng.randint(0, 1)) for _ in range(3)]
                            for _ in range(3)]
        elif mode == "mixed":
            pick = rng.choice(["generic", "sparse", "rank1", "rank2", "zero",
                               "diagonal"])
            if pick == "generic":
                blocks[pair] = _mat_dense(rng)
            elif pick == "sparse":
                blocks[pair] = _mat_dense(rng, density=0.4)
            elif pick == "rank1":
                blocks[pair] = _mat_rank(rng, 1)
            elif pick == "rank2":
                blocks[pair] = _mat_rank(rng, 2)
            elif pick == "zero":
                blocks[pair] = [[Fraction(0)] * 3 for _ in range(3)]
            else:
                blocks[pair] = _mat_diag(rng)
        else:
            raise ValueError(mode)
    return blocks


def block(blocks, u, v, cu, cv):
    if u < v:
        return blocks[(u, v)][cu][cv]
    return blocks[(v, u)][cv][cu]


# --------------------------------------------------------------- linear alg

def lin0():
    return [Fraction(0)] * NK


def lin_zero(a):
    return all(x == 0 for x in a)


def lin_prod(a, b):
    """(sum a_m k_m)(sum b_n k_n) -> {(m,n): coeff} with m<=n."""
    out = {}
    for m in range(NK):
        if a[m] == 0:
            continue
        for n in range(NK):
            if b[n] == 0:
                continue
            key = (m, n) if m <= n else (n, m)
            out[key] = out.get(key, Fraction(0)) + a[m] * b[n]
    return {k: v for k, v in out.items() if v != 0}


def quad_add(dst, src, scale=Fraction(1)):
    for k, v in src.items():
        nv = dst.get(k, Fraction(0)) + scale * v
        if nv == 0:
            dst.pop(k, None)
        else:
            dst[k] = nv


def matchings_of(four):
    a, b, c, d = four
    return (((a, b), (c, d)), ((a, c), (b, d)), ((a, d), (b, c)))


# ------------------------------------------------------------------ pair

class Pair:
    """s, R, x and the 81 cap-error quadrics of one pair, built from spec."""

    def __init__(self, blocks, p, q, h=2):
        self.blocks, self.p, self.q, self.h = blocks, p, q, h
        self.U = tuple(t for t in SITES if t not in (p, q))
        self.s = [block(blocks, p, q, i, j) for i in range(3)
                  for j in range(3)]           # s vector in k-coordinates
        self.words = [(w0, w1, w2, w3) for w0 in range(3) for w1 in range(3)
                      for w2 in range(3) for w3 in range(3)]
        self.pos = {t: n for n, t in enumerate(self.U)}
        self.quadrics = [self.E_word(w) for w in self.words]
        self.quadrics = [Q for Q in self.quadrics if Q]

    def R_lin(self, a, b, word):
        """R_ab(K) as a length-9 vector of coefficients of k_{3i+j}."""
        wa, wb = word[self.pos[a]], word[self.pos[b]]
        P_a = [block(self.blocks, self.p, a, i, wa) for i in range(3)]
        Q_a = [block(self.blocks, self.q, a, j, wa) for j in range(3)]
        P_b = [block(self.blocks, self.p, b, i, wb) for i in range(3)]
        Q_b = [block(self.blocks, self.q, b, j, wb) for j in range(3)]
        form = lin0()
        for i in range(3):
            for j in range(3):
                form[3 * i + j] = P_a[i] * Q_b[j] + P_b[i] * Q_a[j]
        return form

    def x_edge(self, a, b, word):
        return block(self.blocks, a, b, word[self.pos[a]], word[self.pos[b]])

    def E_word(self, word):
        """h=2 specialisation: sum over the 3 matchings of R_e1*R_e2."""
        quad = {}
        for e1_, e2_ in matchings_of(self.U):
            f1 = self.R_lin(e1_[0], e1_[1], word)
            f2 = self.R_lin(e2_[0], e2_[1], word)
            if lin_zero(f1) or lin_zero(f2):
                continue
            quad_add(quad, lin_prod(f1, f2))
        return quad

    def E_word_general(self, word):
        """General formula, |J| <= h-2 subsets.  Only valid as a *check* at
        h = 2 where every J must be empty (returns the same dict)."""
        quad = {}
        for match in matchings_of(self.U):
            for jmask in range(4):
                J = [match[t] for t in range(2) if (jmask >> t) & 1]
                if len(J) > self.h - 2:
                    continue
                rest = [e for e in match if e not in J]
                coeff = Fraction(1)
                for e in J:
                    coeff *= self.x_edge(e[0], e[1], word)
                # s^{|J|} is a *linear form*; at h=2, |J|=0 so it never appears
                if len(J) != 0:
                    raise AssertionError("h=2 must force J empty")
                if coeff == 0:
                    continue
                forms = [self.R_lin(e[0], e[1], word) for e in rest]
                assert len(forms) == 2
                if lin_zero(forms[0]) or lin_zero(forms[1]):
                    continue
                quad_add(quad, lin_prod(forms[0], forms[1]), coeff)
        return quad

    def live(self):
        return not lin_zero(self.s)

    def span_rank(self):
        """rank of the span of the quadrics inside the 45-dim quadratic space"""
        keys = sorted({k for Q in self.quadrics for k in Q})
        idx = {k: n for n, k in enumerate(keys)}
        basis, pivots = [], []
        for Q in self.quadrics:
            row = [Fraction(0)] * len(keys)
            for k, v in Q.items():
                row[idx[k]] = v
            for piv, brow in zip(pivots, basis):
                if row[piv] != 0:
                    f = row[piv] / brow[piv]
                    row = [a - f * b for a, b in zip(row, brow)]
            piv = next((n for n, v in enumerate(row) if v != 0), None)
            if piv is None:
                continue
            basis.append(row)
            pivots.append(piv)
        return len(basis)


# ------------------------------------------------------------- Singular I/O

KV = [f"k{n}" for n in range(NK)]


def _fr(v):
    return f"({v.numerator}/{v.denominator})"


def quad_str_k(Q):
    """key None (used only by the mutation controls) = constant term."""
    parts = [f"{_fr(v)}*{KV[m]}*{KV[n]}"
             for (m, n), v in sorted((k, v) for k, v in Q.items()
                                     if k is not None)]
    if None in Q:
        parts.append(_fr(Q[None]))
    return "+".join(parts) if parts else "0"


def lin_str_k(form):
    parts = [f"{_fr(v)}*{KV[m]}" for m, v in enumerate(form) if v != 0]
    return "+".join(parts) if parts else "0"


def quad_str_uv(Q):
    """substitute K_ij -> u_i v_j into a quadric in k."""
    parts = []
    for (m, n), v in sorted((k, v) for k, v in Q.items() if k is not None):
        a, b = divmod(m, 3)
        c, d = divmod(n, 3)
        parts.append(f"{_fr(v)}*u{a}*v{b}*u{c}*v{d}")
    if None in Q:
        parts.append(_fr(Q[None]))
    return "+".join(parts) if parts else "0"


def lin_str_uv(form):
    parts = []
    for m, v in enumerate(form):
        if v != 0:
            a, b = divmod(m, 3)
            parts.append(f"{_fr(v)}*u{a}*v{b}")
    return "+".join(parts) if parts else "0"


def query_general(pair, tag, saturate=True, quadrics=None, char=0):
    """witness over the full 9-dim cap space; dim != -1  <=>  witness."""
    qs = pair.quadrics if quadrics is None else quadrics
    gens = ",".join(quad_str_k(Q) for Q in qs) if qs else "0"
    sat = f"t*({lin_str_k(pair.s)})*k0*k4*k8-1"
    lines = [f'ring RB={char},({",".join(KV)},t),dp;',
             f"ideal gI={gens};"]
    if saturate:
        lines.append(f"ideal gJ=gI,{sat};")
    else:
        lines.append("ideal gJ=gI;")
    lines.append(f'"B10GEN {tag} "+string(dim(std(gJ)));')
    return "\n".join(lines)


def query_rankone(pair, tag, saturate=True, quadrics=None, char=0):
    """witness among rank-one caps K = u (x) v;  dim != -1  <=>  witness."""
    qs = pair.quadrics if quadrics is None else quadrics
    gens = ",".join(quad_str_uv(Q) for Q in qs) if qs else "0"
    sat = (f"t*({lin_str_uv(pair.s)})*u0*u1*u2*v0*v1*v2-1")
    lines = [f"ring RB={char},(u0,u1,u2,v0,v1,v2,t),dp;",
             f"ideal gI={gens};"]
    if saturate:
        lines.append(f"ideal gJ=gI,{sat};")
    else:
        lines.append("ideal gJ=gI;")
    lines.append(f'"B10RK1 {tag} "+string(dim(std(gJ)));')
    return "\n".join(lines)


def run_singular(script, timeout=120):
    """-> (stdout, elapsed_seconds, status) ; status in ok/timeout/error"""
    with tempfile.NamedTemporaryFile("w", suffix=".sing", delete=False) as fh:
        fh.write(script + "\nquit;\n")
        path = fh.name
    t0 = time.time()
    try:
        proc = subprocess.run([SINGULAR, "-q", "--no-warn", path],
                              capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return "", time.time() - t0, "timeout"
    finally:
        os.unlink(path)
    dt = time.time() - t0
    if proc.returncode != 0:
        return proc.stderr[:800], dt, "error"
    return proc.stdout, dt, "ok"


def parse_dim(out, key):
    val = None
    for line in out.splitlines():
        f = line.split()
        if f and f[0] == key:
            val = int(f[-1])
    return val


def decide(pair, tag, kind, saturate=True, quadrics=None, timeout=120,
           char=0):
    """-> (verdict True/False/None, dim, seconds, status)"""
    if kind == "gen":
        script = query_general(pair, tag, saturate, quadrics, char)
        key = "B10GEN"
    else:
        script = query_rankone(pair, tag, saturate, quadrics, char)
        key = "B10RK1"
    out, dt, status = run_singular(script, timeout=timeout)
    if status != "ok":
        return None, None, dt, status
    dim = parse_dim(out, key)
    if dim is None:
        return None, None, dt, "noparse"
    return (dim != -1), dim, dt, "ok"
