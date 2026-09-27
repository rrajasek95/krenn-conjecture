#!/usr/bin/env python3
"""Exact support for the zero-hafnian response and universal W-rate bounds."""

from fractions import Fraction as Q
from functools import lru_cache
from itertools import combinations
from math import comb, prod
from pathlib import Path
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.append(str(ROOT/"computations/boundary-structure-2026-09-26"))
from exact import E, ZERO, ONE, OMEGA, require


def constants(n):
    m, q, N = n//2, n//2-1, n-1
    B = Q(prod(range(1, n, 2))**2, comb(n, 2)**m)
    return B, B*Q(m**m, q**q), Q(n)*B/(N*N+1), 2*B/n


def hafnian_polynomial(ground, direction, n):
    """Independently enumerate all coefficients of haf(D+sV) by recursion."""
    @lru_cache(None)
    def recurse(vertices):
        if not vertices:
            return (ONE,)
        result = [ZERO]*(len(vertices)//2+1)
        i = vertices[0]
        for j in vertices[1:]:
            lower = recurse(tuple(k for k in vertices if k not in (i, j)))
            d, v = ground.get((i, j), ZERO), direction.get((i, j), ZERO)
            for k, z in enumerate(lower):
                result[k] += d*z
                result[k+1] += v*z
        return tuple(result)
    return recurse


def coefficients(ground, n):
    haf = hafnian_polynomial(ground, {}, n)
    return haf(tuple(range(n)))[0], {
        e: haf(tuple(v for v in range(n) if v not in e))[0]
        for e in combinations(range(n), 2)}


def fixtures(n):
    phases = [ONE, OMEGA, OMEGA*OMEGA]
    sharp = {(i, j): phases[i % 3]*phases[j % 3]
             for i, j in combinations(range(1, n), 2)}
    dense = {e: ONE for e in combinations(range(n), 2)}
    dense[n-2, n-1] = E(-(n-2))
    result = [("sharp_odd_core", sharp, True), ("dense_real_cancellation", dense, False)]
    if n <= 10:
        general = {(i, j): E(1+(2*i+j) % 3, (i+2*j) % 3-1)
                   for i, j in combinations(range(n), 2)}
        e = (n-2, n-1)
        general[e] = ZERO
        value, C = coefficients(general, n)
        require(bool(C[e]), "Selected edge has a nonzero coefficient")
        general[e] = -value/C[e]
        result.append(("nonuniform_complex_cancellation", general, False))
    return result


def check_fixture(n, name, D, sharp):
    m, q = n//2, n//2-1
    value, C = coefficients(D, n)
    a = sum(z.abs2() for z in D.values())
    T = sum(z.abs2() for z in C.values())
    require(not value and a > 0 and T > 0, "Nontrivial zero-hafnian fixture")
    require(sum((D.get(e, ZERO)*z for e, z in C.items()), ZERO) == m*value,
            "Euler identity in independent unordered edge coordinates")
    direction = {e: z.conjugate() for e, z in C.items()}
    require(not sum((D.get(e, ZERO).conjugate()*z for e, z in direction.items()), ZERO),
            "The derivative direction is Hermitian-orthogonal to the source")
    polynomial = hafnian_polynomial(D, direction, n)(tuple(range(n)))
    require(not polynomial[0] and polynomial[1] == E(T),
            "The first circle coefficient is the total squared response")
    B, K, attained, upper = constants(n)
    correction = sum(polynomial[j].abs2()*a**(j-1)/Q(q**(j-1)*T**j)
                     for j in range(2, m+1))
    require(T+correction <= K*a**q, "Refined Parseval response inequality")
    radius2 = a/(q*T)
    average = sum(z.abs2()*radius2**j for j, z in enumerate(polynomial))
    require(average <= B*(a+radius2*T)**m, "Circle average obeys the scalar norm bound")
    require((T+correction)*(a/q) == average, "Correct normalization of the higher coefficients")
    # Exact Fourier orthogonality: m+1 equally spaced phases distinguish all powers.
    require(all((j-k) % (m+1) != 0 for j in range(m+1) for k in range(m+1) if j != k),
            "No aliasing in the finite Fourier average")
    rows = [sum(z.abs2() for e, z in C.items() if i in e) for i in range(n)]
    require(all(rows) and sum(rows) == 2*T, "Every unordered cofactor appears in two rows")
    beta = sum(Q(1, r) for r in rows)
    eta, xi = T/(K*a**q), 2*T*beta/(n*n)-1
    imbalance = sum((rows[i]-rows[j])**2/(rows[i]*rows[j])
                    for i, j in combinations(range(n), 2))/(n*n)
    require(xi == imbalance >= 0 and 0 < eta <= 1, "Efficiency and row-imbalance identities")
    response_bound = Q(n*q**q, m**m)/(a**q*beta)
    require(response_bound == upper*eta/(1+xi) <= upper,
            "The refined formula reproduces the unrestricted response relaxation")
    if sharp:
        require(eta == 1 and correction == 0, "Sharp cofactor norm bound at every tested order")
        require(xi == Q((n-2)**2, n*n), "Exact row imbalance of the one-root design")
        require(response_bound == attained, "The refined bound retains the attained rate")
    # Weighted Cauchy-Schwarz, including zero target weights.
    weights = [Q((i % 4)) for i in range(n)]
    beta_w = sum(w*w/r for w, r in zip(weights, rows))
    require(beta_w*2*T >= sum(weights)**2, "Weighted response inequality")
    weighted_bound = Q(q**q, m**m)*sum(w*w for w in weights)/(a**q*beta_w)
    require(weighted_bound <= 2*B*sum(w*w for w in weights)/sum(weights)**2,
            "Weighted W global bound")
    return dict(sites=n, fixture=name, efficiency=str(eta), row_imbalance=str(xi),
                higher_coefficient_defect_fraction=str(correction/(K*a**q)),
                circle_degree=m, response_upper_bound=str(response_bound),
                universal_upper_bound=str(upper), sharp=sharp)


def check_all_even_algebra():
    records = []
    for n in range(4, 82, 2):
        m, q, N = n//2, n//2-1, n-1
        B, K, attained, upper = constants(n)
        c = prod(range(1, n-2, 2))
        require(K*(N*q)**q == N*c*c, "Sharp cofactor constant at the isolated-root source")
        require(Q(2*q**q, n*m**m)*K == upper, "Cancellation of universal rate constants")
        ratio = upper/attained
        require(ratio == Q(2*(N*N+1), n*n) < 2, "Global factor strictly smaller than two")
        require(ratio-1 == Q((n-2)**2, n*n), "Threshold for response-row imbalance")
        # Sharpness of the general polynomial lemma: P=z_1^q z_2.
        monomial_sup = Q(q**q, m**m)
        require(monomial_sup*Q(m**m, q**q) == 1, "Sharp polynomial-gradient constant")
        require(Q(q, m)**q*Q(1, m) == monomial_sup, "Unit-sphere maximizer for the monomial")
        old = B*Q(q, m)**q
        require(upper <= old and (upper < old or n == 4), "Comparison with the previous global bound")
        records.append(dict(sites=n, attained_rate=str(attained), upper_bound=str(upper),
                            upper_to_attained_ratio=str(ratio), construction_guarantee=str(1/ratio)))
    return records


def check_scope():
    # The zero-hafnian hypothesis cannot be dropped from the sharp response theorem.
    D = {e: ONE for e in combinations(range(6), 2)}
    value, C = coefficients(D, 6)
    a, T = Q(15), sum(z.abs2() for z in C.values())
    require(bool(value) and T > constants(6)[1]*a*a,
            "Nonzero ground output is an actual counterexample to dropping the hypothesis")
    require(constants(6)[3] == Q(1, 45) and constants(6)[2] == Q(1, 65),
            "Six-site global interval")
    require(constants(6)[3]/(Q(4, 135)) == Q(3, 4), "Twenty-five percent improvement")
    return dict(zero_hafnian_hypothesis="necessary", nonzero_ground_counterexample_response=str(T),
                six_site_rate_interval=["1/65", "1/45"], exact_global_optimum="OPEN")


def main():
    dependencies = json.loads((HERE/"dependencies.json").read_text())
    for name, digest in dependencies.items():
        require(hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest,
                "Pinned dependency: "+name)
    records = [check_fixture(n, *fixture) for n in range(4, 14, 2) for fixture in fixtures(n)]
    require(len(records) == 14, "Advertised exact fixture count")
    result = dict(status="PASS",
                  evidence_status="Written proof with exact supporting checks; independent audit pending",
                  cofactor_fixtures=records, all_even_algebra=check_all_even_algebra(),
                  scope=check_scope(), dependencies=dependencies,
                  external_input="Roos, arXiv:1906.06176, Theorem 2.3 and equations (40), (42)",
                  universal_conclusion="Every even-size unrestricted exact W rate is at most 2 B_n/n")
    paths = [p for p in HERE.iterdir() if p.suffix in (".py", ".md", ".json")
             and p.name != "results.json"]
    paths += [ROOT/"notes/w-state-universal-factor-two-2026-09-27.md"]
    result["sha256"] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in sorted(paths)}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
