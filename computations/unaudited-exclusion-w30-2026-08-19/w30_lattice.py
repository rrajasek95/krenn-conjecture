#!/usr/bin/env python3
"""W30 BINOMIAL/LATTICE CERTIFICATES.  UNAUDITED.  Exact integer arithmetic.

The m=25 collapse system is BINOMIAL: every generator is  M1 - M2  (a
collapse minor) or  M1 + M2  (the reduced clean equation (RED) valid on the
locus hafL = 0).  With every Gamma cell NONZERO the system lives in the
torus, where each generator says

        z^{a_i} = c_i ,     a_i = exp(M1) - exp(M2) in Z^n,  c_i in {+1,-1}.

INFEASIBILITY CERTIFICATE.  If there is an integer vector lambda with

        sum_i lambda_i a_i = 0        and        prod_i c_i^{lambda_i} = -1

then the system has NO solution with all coordinates nonzero, over ANY
field of characteristic != 2 -- and lambda is a short, independently
checkable certificate (this is the Farkas-style object for the torus).
The test is SOUND in the direction we need (a certificate proves
infeasibility); absence of a certificate is reported as such, never as
feasibility.

Characteristic 2 is excluded explicitly (+1 = -1 there); our primes are
13 and 31.
"""
from __future__ import annotations

import json
import os
import sys
from fractions import Fraction
from itertools import combinations

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))


def parse_binomial(g, varidx):
    """'a*b*c - d*e*f' or 'a*b + c*d'  ->  (exponent vector, sign)."""
    g = g.replace(" ", "")
    if "+" in g:
        left, right, c = g.split("+")[0], g.split("+")[1], -1
    elif "-" in g:
        left, right, c = g.split("-")[0], g.split("-")[1], +1
    else:
        raise ValueError("not a binomial: %s" % g)
    a = [0] * len(varidx)
    for v in left.split("*"):
        a[varidx[v]] += 1
    for v in right.split("*"):
        a[varidx[v]] -= 1
    return a, c


def rational_nullspace(rows, k):
    """left kernel: {lambda in Q^k : sum_i lambda_i rows[i] = 0}.
    rows is a list of k integer vectors of length n.  Exact."""
    n = len(rows[0])
    # build the n x k matrix M with M[j][i] = rows[i][j]; solve M lambda = 0
    M = [[Fraction(rows[i][j]) for i in range(k)] for j in range(n)]
    piv = []
    r = 0
    for c in range(k):
        sel = None
        for i in range(r, len(M)):
            if M[i][c] != 0:
                sel = i
                break
        if sel is None:
            continue
        M[r], M[sel] = M[sel], M[r]
        pv = M[r][c]
        M[r] = [x / pv for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        piv.append(c)
        r += 1
        if r == len(M):
            break
    free = [c for c in range(k) if c not in piv]
    basis = []
    for f in free:
        v = [Fraction(0)] * k
        v[f] = Fraction(1)
        for i, p in enumerate(piv):
            v[p] = -M[i][f]
        basis.append(v)
    return basis


def primitive(v):
    from math import gcd
    den = 1
    for x in v:
        den = den * x.denominator // gcd(den, x.denominator)
    w = [int(x * den) for x in v]
    g = 0
    for x in w:
        g = gcd(g, abs(x))
    if g:
        w = [x // g for x in w]
    return w


def find_certificate(gens, varnames, max_subsets=200000):
    """search the saturated kernel lattice for lambda with an ODD number of
    sign-(-1) generators."""
    varidx = {v: i for i, v in enumerate(varnames)}
    A, S = [], []
    for g in gens:
        a, c = parse_binomial(g, varidx)
        A.append(a)
        S.append(0 if c == 1 else 1)          # parity of the (-1) exponent
    k = len(A)
    basis = [primitive(b) for b in rational_nullspace(A, k)]
    # each primitive kernel vector IS a lattice element; check its parity
    for b in basis:
        par = sum(b[i] * S[i] for i in range(k)) % 2
        if par == 1:
            return dict(found=True, certificate=b,
                        n_generators_used=sum(1 for x in b if x),
                        parity=par)
    # F_2 combinations of the basis
    m = len(basis)
    if m and m <= 20:
        for rsz in range(2, min(m, 6) + 1):
            for comb in combinations(range(m), rsz):
                v = [0] * k
                for j in comb:
                    v = [x + y for x, y in zip(v, basis[j])]
                if any(v) and all(
                        sum(v[i] * A[i][j] for i in range(k)) == 0
                        for j in range(len(A[0]))):
                    par = sum(v[i] * S[i] for i in range(k)) % 2
                    if par == 1:
                        return dict(found=True, certificate=v,
                                    n_generators_used=sum(1 for x in v if x),
                                    parity=par)
    return dict(found=False, kernel_rank=len(basis), n_generators=k,
                note="NO certificate found -- this is NOT a feasibility "
                     "claim (ledger 18): the search is sound only in the "
                     "infeasibility direction")


def verify_certificate(gens, varnames, lam):
    """independent re-check of a certificate."""
    varidx = {v: i for i, v in enumerate(varnames)}
    A, S = [], []
    for g in gens:
        a, c = parse_binomial(g, varidx)
        A.append(a)
        S.append(0 if c == 1 else 1)
    n = len(varnames)
    tot = [sum(lam[i] * A[i][j] for i in range(len(A))) for j in range(n)]
    return dict(exponent_sum_is_zero=all(t == 0 for t in tot),
                sign_parity=sum(lam[i] * S[i] for i in range(len(A))) % 2)


def selftest():
    """controls: a KNOWN-infeasible binomial system must yield a
    certificate; a KNOWN-feasible one must not."""
    vs = ["zzx", "zzy"]
    # x*x - y*y = 0 and x*x + y*y = 0  ->  (x/y)^2 = 1 and = -1  : infeasible
    bad = ["zzx*zzx - zzy*zzy", "zzx*zzx + zzy*zzy"]
    r1 = find_certificate(bad, vs)
    # feasible: x*x - y*y = 0 alone
    r2 = find_certificate(["zzx*zzx - zzy*zzy"], vs)
    ok1 = r1["found"] and verify_certificate(
        bad, vs, r1["certificate"])["exponent_sum_is_zero"] and \
        verify_certificate(bad, vs, r1["certificate"])["sign_parity"] == 1
    return dict(infeasible_detected=bool(ok1),
                feasible_not_flagged=(not r2["found"]),
                certificate=r1.get("certificate"))


if __name__ == "__main__":
    print(json.dumps(selftest(), indent=1))
