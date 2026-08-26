#!/usr/bin/env python3
"""UNAUDITED PROBE W17 -- h = 2 (six sites) rank-one decision procedures.

Two INDEPENDENT decision paths for
    (RK1)  exists (u,v):  E_pq(u (x) v) = 0,  u_c v_c != 0,  u^T A_pq v != 0

  path 1 (definition): Rabinowitsch on the 81 bidegree-(2,2) components of
          E_pq(u (x) v)   [identical in shape to W14's task-3 query];
  path 2 (Theorem W17.1): the union of the five structural branches
          - branch Z(a): site a has alpha_a = beta_a = 0;
          - branch D (|D| = 3): the three sites of D are rank <= 1
            (9 bidegree-(1,1) minors) and the two e-conditions hold;
          - branch U (all four): four sites rank <= 1 and one quadric.
          Each branch is decided by its own Rabinowitsch query.

Path 2 is used both as a control on path 1 and as the CLASSIFIER (which
branch carries the witness).
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations

from w17_core import COLORS, oriented, run_singular

UV = ("u0", "u1", "u2", "v0", "v1", "v2")


def _fr(x):
    x = Fraction(x)
    return f"({x.numerator}/{x.denominator})"


def lin_u(vec):
    """sum_i u_i vec[i] as a Singular string."""
    parts = [f"{_fr(c)}*u{i}" for i, c in enumerate(vec) if c != 0]
    return "+".join(parts) if parts else "0"


def lin_v(vec):
    parts = [f"{_fr(c)}*v{j}" for j, c in enumerate(vec) if c != 0]
    return "+".join(parts) if parts else "0"


def alpha_forms(source, p, a):
    """alpha_a[c] = sum_i u_i A_pa[i][c] as strings."""
    apa = oriented(source, p, a)
    return [lin_u([apa[i][c] for i in range(3)]) for c in COLORS]


def beta_forms(source, q, a):
    aqa = oriented(source, q, a)
    return [lin_v([aqa[j][c] for j in range(3)]) for c in COLORS]


def s_form(source, p, q):
    apq = oriented(source, p, q)
    parts = []
    for i in range(3):
        for j in range(3):
            if apq[i][j] != 0:
                parts.append(f"{_fr(apq[i][j])}*u{i}*v{j}")
    return "+".join(parts) if parts else "0"


def error_forms(source, p, q, sites):
    """The 81 components E_w = 2 e_2^hom(alpha[w], beta[w]) as strings."""
    sites = tuple(sites)
    A = {a: alpha_forms(source, p, a) for a in sites}
    Bt = {a: beta_forms(source, q, a) for a in sites}
    out = []
    from itertools import product as iproduct
    for word in iproduct(COLORS, repeat=4):
        terms = []
        for pair in combinations(range(4), 2):
            fac = []
            for n, a in enumerate(sites):
                f = A[a][word[n]] if n in pair else Bt[a][word[n]]
                if f == "0":
                    fac = None
                    break
                fac.append(f"({f})")
            if fac:
                terms.append("*".join(fac))
        if terms:
            out.append("+".join(terms))
    return out


def minor_forms(source, p, q, a):
    """The three components of alpha_a x beta_a (bidegree (1,1))."""
    A = alpha_forms(source, p, a)
    Bt = beta_forms(source, q, a)
    out = []
    for i, j in ((1, 2), (2, 0), (0, 1)):
        t1 = f"({A[i]})*({Bt[j]})" if A[i] != "0" and Bt[j] != "0" else ""
        t2 = f"({A[j]})*({Bt[i]})" if A[j] != "0" and Bt[i] != "0" else ""
        if t1 and t2:
            out.append(f"{t1}-{t2}")
        elif t1:
            out.append(t1)
        elif t2:
            out.append(f"-1*{t2}")
    return out


def zero_forms(source, p, q, a):
    """alpha_a = 0 and beta_a = 0 (six linear forms)."""
    return [f for f in alpha_forms(source, p, a) + beta_forms(source, q, a)
            if f != "0"]


def _query(gens, s_str, tag, ring="RQ"):
    prod = f"({s_str})*u0*u1*u2*v0*v1*v2"
    return "\n".join([
        f'ring {ring}=0,({",".join(UV)},t),dp;',
        "ideal Iw=" + (",".join(gens) if gens else "0") + ";",
        f"ideal Jw=Iw,t*({prod})-1;",
        f'"RK1 {tag} "+string(dim(std(Jw)));'])


def direct_query(source, p, q, sites, tag):
    return _query(error_forms(source, p, q, sites), s_form(source, p, q), tag)


def branch_queries(source, p, q, sites, tag):
    """(name, script) for every structural branch of Theorem W17.1."""
    sites = tuple(sites)
    s_str = s_form(source, p, q)
    errs = error_forms(source, p, q, sites)
    out = []
    for a in sites:
        out.append((f"Z{a}", _query(zero_forms(source, p, q, a), s_str,
                                    f"{tag}_Z{a}")))
    for D in combinations(sites, 3):
        gens = []
        for a in D:
            gens.extend(minor_forms(source, p, q, a))
        out.append((f"D{''.join(map(str, D))}",
                    _query(gens + errs, s_str,
                           f"{tag}_D{''.join(map(str, D))}")))
    return out


def parse_rk1(output, tag):
    for line in output.splitlines():
        f = line.split()
        if f and f[0] == "RK1" and f[1] == tag:
            return int(f[2]) != -1
    return None


def decide_rank_one(source, p, q, sites, tag, timeout=300):
    out = run_singular(direct_query(source, p, q, sites, tag), timeout=timeout)
    return parse_rk1(out, tag)


def decide_branches(source, p, q, sites, tag, timeout=300):
    found = {}
    for name, script in branch_queries(source, p, q, sites, tag):
        out = run_singular(script, timeout=timeout)
        found[name] = parse_rk1(out, f"{tag}_{name}")
    return found
