"""Rational certificates for W sources with two uniform ground groups."""

from fractions import Fraction as Q
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from math import comb, factorial

BASE = Path(__file__).resolve().parents[1] / "w-equal-split-legendre-2026-09-27/algebra.py"
SPEC = spec_from_file_location("equal_split_polynomials", BASE)
P = module_from_spec(SPEC)
SPEC.loader.exec_module(P)
require = P.require


def bp(p):
    return [P.trim(c) for c in p]


def btrim(p):
    p = bp(p)
    while len(p) > 1 and p[-1] == [Q(0)]:
        p.pop()
    return p


def badd(p, q):
    return btrim([P.add(p[i] if i < len(p) else [0],
                        q[i] if i < len(q) else [0])
                  for i in range(max(len(p), len(q)))])


def bscale(p, c):
    return btrim([P.mul(a, c) for a in p])


def bmul(p, q):
    out = [[Q(0)] for _ in range(len(p)+len(q)-1)]
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i+j] = P.add(out[i+j], P.mul(a, b))
    return btrim(out)


def bpower(p, n):
    out = [[Q(1)]]
    for _ in range(n):
        out = bmul(out, p)
    return out


def bderivative(p):
    return btrim([P.scale(p[i], i) for i in range(1, len(p))] or [[0]])


def ground_polynomial(p, q):
    """H(a,b,c) = b^d sum_j G_j (ab)^j c^(p-2j)."""
    require(2 <= p <= q and (q-p) % 2 == 0, "Admissible group sizes")
    d = (q-p)//2
    return [Q(factorial(p)*factorial(q),
              factorial(p-2*j)*2**(2*j+d)*factorial(j)*factorial(j+d))
            for j in range(p//2+1)]


def cancellation_polynomial(p, q):
    return [a*(-1)**j for j, a in enumerate(ground_polynomial(p, q))]


def cost_parts(p, q):
    """Bivariate polynomials: outer variable x=|c|^2, inner variable k."""
    r = (p+q-2)//2
    s = bp([[comb(q, 2)], [p*q], [0, 0, comb(p, 2)]])
    a = bp([[q], [0, 0, p-1]])
    b = bp([[q-1], [p]])
    h = badd(bscale([[0]]+b, [0, 0, p*p*(p-1)]),
             bscale(a, [q*q*(q-1)]))
    g = [j*c*(-1)**(j-1) for j, c in enumerate(ground_polynomial(p, q)) if j]
    return r, s, a, b, h, g


def gap_polynomial(p, q, factor=Q(81, 80)):
    r, s, a, b, h, g = cost_parts(p, q)
    left = bscale(bmul(bpower(s, r), h), [p*q])
    norm = P.scale([0, 0]+P.power(g, 2), 4*factor*P.star_cost(r+1))
    right = bscale([[0]]*(p-1)+bmul(a, b), norm)
    return badd(left, bscale(right, [-1]))


def stationary_polynomial(p, q):
    r, s, a, b, h, _ = cost_parts(p, q)
    d = bmul(a, b)
    first = bscale([[0]]+bmul(bmul(bderivative(s), h), d), [r])
    second = [[0]]+bmul(bmul(s, bderivative(h)), d)
    third = bscale(bmul(bmul(s, h), d), [-(p-1)])
    fourth = bscale([[0]]+bmul(bmul(s, h), bderivative(d)), [-1])
    return badd(badd(first, second), badd(third, fourth))


def positive_normalize(p):
    p = P.trim(p)
    if p != [Q(0)]:
        p = P.scale(p, 1/abs(p[-1]))
    return p


def sturm(p):
    seq = [positive_normalize(p), positive_normalize(P.derivative(p))]
    while seq[-1] != [Q(0)]:
        nxt = P.scale(P.remainder(seq[-2], seq[-1]), -1)
        if nxt == [Q(0)]:
            break
        seq.append(positive_normalize(nxt))
    return seq


def variation(seq, x):
    signs = []
    for p in seq:
        v = p[-1] if x is None else P.value(p, x)
        if v:
            signs.append(1 if v > 0 else -1)
    return sum(a != b for a, b in zip(signs, signs[1:]))


def safe_cut(poly, lo, hi):
    denominator = 2
    while True:
        mid = ((denominator-1)*lo+hi)/denominator
        if P.value(poly, mid):
            return mid
        denominator += 1


def root_intervals(poly, bits=26):
    seq = sturm(poly)
    degree = len(poly)-1
    require(variation(seq, 0)-variation(seq, None) == degree,
            "All cancellation roots simple and positive")
    hi = Q(1)
    while not P.value(poly, hi) or variation(seq, 0)-variation(seq, hi) != degree:
        hi = 2*hi+1
    pending = [(Q(0), hi, degree)]
    isolated = []
    while pending:
        lo, hi, count = pending.pop()
        if not count:
            continue
        if count == 1 and hi-lo <= max(Q(1), lo)/2**bits:
            isolated.append((lo, hi))
            continue
        mid = safe_cut(poly, lo, hi)
        left = variation(seq, lo)-variation(seq, mid)
        pending.append((mid, hi, count-left))
        pending.append((lo, mid, left))
    return sorted(isolated)


def lower_coefficients(poly, lo, hi):
    require(0 <= lo < hi, "Positive root interval")
    return [sum(c*(lo if c >= 0 else hi)**j for j, c in enumerate(a))
            for a in poly]


def bernstein_positive(poly, max_depth=16):
    """Cover x>=0 via t=x/(1+x), using exact de Casteljau subdivision."""
    poly = P.trim(poly)
    degree = len(poly)-1
    initial = [c/Q(comb(degree, i)) for i, c in enumerate(poly)]
    pending = [(initial, 0, 0)]
    cells, deepest = [], 0
    while pending:
        coefficients, depth, index = pending.pop()
        if min(coefficients) > 0:
            cells.append([index, depth])
            deepest = max(deepest, depth)
            continue
        if max(coefficients) <= 0 or depth == max_depth:
            return None
        left, right = [coefficients[0]], [coefficients[-1]]
        while len(coefficients) > 1:
            coefficients = [(a+b)/2 for a, b in zip(coefficients, coefficients[1:])]
            left.append(coefficients[0])
            right.append(coefficients[-1])
        pending.append((left, depth+1, 2*index))
        pending.append((right[::-1], depth+1, 2*index+1))
    return {"positive_intervals": len(cells), "maximum_depth": deepest,
            "dyadic_cells": sorted(cells, key=lambda c: Q(c[0], 2**c[1]))}


def disconnected_cost(p, q):
    require(p % 2 and q % 2, "Odd disconnected groups")
    alpha, beta = (p-1)//2, (q-1)//2
    r = alpha+beta
    return (Q(p*p+q*q, p*q)*r**r*p**alpha*q**beta
            / (P.odd_double(p-2)*P.odd_double(q-2))**2)


def finite_catalog(max_m=20):
    catalog = []
    for m in range(3, max_m+1):
        for p in range(2, m):
            q = 2*m-p
            poly = cancellation_polynomial(p, q)
            gap = gap_polynomial(p, q)
            intervals = root_intervals(poly)
            branches = []
            for lo, hi in intervals:
                certificate = bernstein_positive(lower_coefficients(gap, lo, hi))
                require(certificate is not None,
                        f"Positive scalar gap p={p}, q={q}, k in {(lo,hi)}")
                branches.append(dict(k_interval=[str(lo), str(hi)],
                                     **certificate))
            row = dict(p=p, q=q, branches=branches)
            if p % 2:
                ratio = disconnected_cost(p, q)/P.star_cost(m)
                require(ratio > Q(81, 80), "Disconnected finite-catalog gap")
                row["disconnected_cost_ratio"] = str(ratio)
            catalog.append(row)
    return catalog


def normalized_gegenbauer(p, d):
    """Three-term recurrence, then normalize the value at 1."""
    lam = Q(2*d+1, 2)
    prev, current = [Q(1)], [Q(0), 2*lam]
    if not p:
        return prev
    for j in range(1, p):
        nxt = P.scale(P.add(P.scale([0]+current, 2*(j+lam)),
                            P.scale(prev, -(j+2*lam-1))), Q(1, j+1))
        prev, current = current, nxt
    return P.scale(current, 1/P.value(current, 1))


def check_reductions():
    pairs = 0
    for m in range(3, 13):
        for p in range(2, m+1):
            q, d = 2*m-p, m-p
            g = ground_polynomial(p, q)
            counted = P.group_haf(p, q)
            expected = {(j, j+d, p-2*j): number for j, number in enumerate(g)}
            require(counted == expected, "Unequal-group matching count")
            transformed = [Q(0)]
            for j, number in enumerate(g):
                term = [Q(0)]*(p-2*j)+P.power([-1, 0, 1], j)
                transformed = P.add(transformed, P.scale(term, number/g[0]))
            require(transformed == normalized_gegenbauer(p, d),
                    "Gegenbauer identity from independent recurrence")
            cancellation = cancellation_polynomial(p, q)
            derivative = [j*c*(-1)**(j-1) for j, c in enumerate(g) if j]
            for sizes, target in (
                    ((p-2, q), P.scale(derivative, Q(1, comb(p, 2)))),
                    ((p, q-2), P.scale([0]+derivative, Q(-1, comb(q, 2)))),
                    ((p-1, q-1), P.scale([0]+derivative, Q(2, p*q)))):
                minor = P.group_haf(*sizes)
                coefficients = [Q(0)]*(max(a for a, _, _ in minor)+1)
                for (a, _, c), number in minor.items():
                    coefficients[a] += number*(-1)**a
                    require(2*a+c == sizes[0], "Homogeneous cross-weight scaling")
                require(P.remainder(P.add(coefficients, P.scale(target, -1)),
                                    cancellation) == [Q(0)],
                        "Individual cofactor on every cancellation branch")
            r, s, a, b, h, _ = cost_parts(p, q)
            stationary = stationary_polynomial(p, q)
            require(len(stationary) == 7, "Stationary polynomial has degree six")
            negative_constant = P.scale(P.mul(P.mul(s[0], h[0]), P.mul(a[0], b[0])),
                                        -(p-1))
            positive_leading = P.scale(P.mul(P.mul(s[-1], h[-1]),
                                             P.mul(a[-1], b[-1])), q-1)
            require(stationary[0] == negative_constant
                    and stationary[-1] == positive_leading,
                    "Nonvanishing stationary polynomial and endpoint signs")
            for k in (Q(1, 2), Q(1), Q(3)):
                for x in (Q(1, 4), Q(1), Q(4)):
                    # Cofactor factor g is set to 1 on both sides.
                    row_a = 4*x**(p-2)/p**2*(Q(1, p-1)+k*k*x/q)
                    row_b = 4*k*k*x**(p-1)/q**2*(Q(1, p)+x/(q-1))
                    direct = p/row_a+q/row_b
                    ev = lambda z: P.value([P.value(c, k) for c in z], x)
                    formula = Q(p*q)/(4*k*k)*ev(h)/(x**(p-1)*ev(a)*ev(b))
                    require(direct == formula, "Scalar reciprocal response formula")
            pairs += 1
    return {"half_sizes": [3, 12], "group_splits": pairs,
            "stationary_degree": 6, "exact_row_examples": 9*pairs}


def shifted(p, a):
    out = [Q(0)]
    for j, c in enumerate(p):
        out = P.add(out, P.scale(P.power([a, 1], j), c))
    return out


def check_two_site_tail():
    small = {
        4: ([27, -27, -522, 576, 1280, 1088, 128], Q(20)),
        6: ([1875, 2300, -46480, 102480, 196000, 305536, 209664,
             179712, 6912], Q(14)),
        8: ([168070, 557417, -5246082, 15805536, 30515520, 64431360,
             64335360, 88350720, 44974080, 39649280, 655360], Q(36, 5)),
    }
    rows = []
    for q, (expected, multiple) in small.items():
        u = [q*(q-1), (q-1)*(q*q+4), 8]
        d = P.scale(P.mul([0, q-1, 2], [1, q]), 2)
        polynomial = P.add(
            P.scale(P.mul(P.power([q-1, 4, 2*q], q//2), u), q+1),
            P.scale(d, -Q(6, 5)*(q+1)**(q//2)*((q+1)**2+1)))
        require(polynomial == P.scale(expected, multiple),
                "Small two-site-tail certificate polynomial")
        general = [P.value(c, q) for c in gap_polynomial(2, q, Q(6, 5))]
        require(general == P.scale(polynomial, general[-1]/polynomial[-1]),
                "Specialized two-site formula matches general cost")
        certificate = bernstein_positive(expected)
        require(certificate is not None, "Positive small two-site-tail certificate")
        rows.append(dict(q=q, **certificate))
    # Common-denominator check for 4*a*c-b^2 in the written tail proof.
    m = [0, -1, 0, 1]  # q(q-1)(q+1)
    b_num = P.scale([-20, 0, 7, 7], -6)
    c_num = P.scale([-80, -80, -40, 3, 3], 3)
    small_m = [2, 2, 1]  # (q+1)^2+1
    require(b_num == P.add([0, 0, 18, 18], P.scale(P.mul([-1, 1], small_m), -60)),
            "Linear coefficient of the Bernoulli lower quadratic")
    require(c_num == P.add([0, 0, 0, 9, 9], P.scale(small_m, -120)),
            "Quadratic coefficient of the Bernoulli lower quadratic")
    numerator = P.add(P.scale(P.mul(c_num, m), 36), P.scale(P.power(b_num, 2), -1))
    n = [-400, 240, 520, 160, -298, -227, -40, 9]
    require(numerator == P.scale(n, 36), "Tail discriminant factorization")
    coefficients = shifted(n, 10)
    require(coefficients == list(map(Q, [
        24534000, 26516640, 10456520, 2111240, 243352, 16273, 590, 9])),
        "Exact tail shift coefficients")
    require(all(c > 0 for c in coefficients), "Positive tail at every q>=10")
    require(Q(3, 5)**2 == Q(9, 25), "Monotone prefactor base case q=4")
    for q in range(4, 42, 2):
        require(cancellation_polynomial(2, q)[0]
                /ground_polynomial(2, q)[1] == q,
                "Unique two-site cancellation root")
    return {"small_core_sizes": rows, "tail_core_size": 10,
            "scalar_cost_ratio": "6/5", "strict_rate_ratio": "5/6",
            "positive_shift_coefficients": list(map(str, coefficients)),
            "all_size_argument": "Written monotone prefactor, Bernoulli inequality, and positive quadratic"}


def certificate_catalog(max_m=20):
    result = finite_catalog(max_m)
    return {"maximum_sites": 2*max_m,
            "splits": len(result),
            "branches": sum(len(a["branches"]) for a in result),
            "maximum_bernstein_depth": max(b["maximum_depth"]
                for a in result for b in a["branches"]),
            "catalog": result}


if __name__ == "__main__":
    import argparse
    import json
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-sites", type=int, default=40)
    args = parser.parse_args()
    require(args.max_sites >= 6 and not args.max_sites % 2, "Even maximum site count >=6")
    print(json.dumps(certificate_catalog(args.max_sites//2), indent=2, sort_keys=True))
