#!/usr/bin/env python3
"""Replay exact support for cofactor rigidity and local scalar W optimality."""

from collections import Counter
from fractions import Fraction as Q
from itertools import combinations
from math import comb
from pathlib import Path
import hashlib
import importlib.util
import json
import ground_hessian
from exact import ONE, E, matchings, require

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
spec = importlib.util.spec_from_file_location(
    "w_factor_support", ROOT/"computations/w-universal-factor-two-2026-09-27/verify.py")
factor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(factor)


def cycle_constants(n):
    A = Q(3, 2*n*(n-1))
    B = Q(3*(n-2), n*(n-1))
    C = Q(n*n-7*n+9, n*(n-1))
    L = Q(3*(n-2)*(n-3), 2*n*(n-1))
    require(min(A, B, C) > 0 and 4*A+4*B+2*C == 2,
            "Positive cycle AM-GM allocation")
    require(A*(n-2)*(n-3) == L, "Fourth-power coefficient")
    require(B*(n-3) == 2*L, "Adjacent edge-pair coefficient")
    require(1+2*C == 2*L, "Disjoint edge-pair coefficient")
    require(L == Q(9*comb(n, 4), comb(n, 2)**2), "Subhafnian normalization")
    require(A*comb(n, 2)/2 == Q(3, 8), "Magnitude-variance slack coefficient")
    kappa = Q(comb(n, 2)**2, 24*comb(n, 4))
    require(kappa == Q(n*(n-1), 4*(n-2)*(n-3)), "Full-hafnian slack normalization")
    return A, B, C, L, kappa


def cycle_census(n):
    edge_counts, pair_counts = Counter(), Counter()
    count = 0
    for vertices in combinations(range(n), 4):
        perfect = list(matchings(vertices))
        for a, b in combinations(perfect, 2):
            cycle = tuple(sorted((*a, *b)))
            edge_counts.update(cycle)
            pair_counts.update(combinations(cycle, 2))
            count += 1
    edges = list(combinations(range(n), 2))
    require(count == 3*comb(n, 4), "All four-cycles enumerated")
    require(set(edge_counts.values()) == {(n-2)*(n-3)}, "Every edge incidence count")
    for e, f in combinations(edges, 2):
        require(pair_counts[e, f] == (n-3 if set(e) & set(f) else 2),
                "Every edge-pair incidence count")
    return dict(sites=n, cycles=count, edge_incidences=(n-2)*(n-3),
                adjacent_pair_incidences=n-3, disjoint_pair_incidences=2)


def matching_transversals(n):
    edges = list(combinations(range(n), 2))
    index = {e: i for i, e in enumerate(edges)}
    perfect = [sum(1 << index[e] for e in p) for p in matchings(tuple(range(n)))]
    survivors = {mask for mask in range(1 << len(edges))
                 if all((mask & p).bit_count() == 1 for p in perfect)}
    stars = {sum(1 << i for i, e in enumerate(edges) if v in e) for v in range(n)}
    expected = stars
    if n == 4:
        expected = stars | {((1 << len(edges))-1) ^ mask for mask in stars}
    require(survivors == expected, "All exact-one matching transversals have the stated form")
    return dict(sites=n, edge_sets_checked=1 << len(edges),
                survivors=len(survivors), stars=len(stars),
                complement_stars_allowed=(n == 4))


def scalar_slack():
    records = []
    for n in (6, 8, 10, 12):
        A, allocation, C, L, kappa = cycle_constants(n)
        q, m, M = n//2-1, n//2, comb(n, 2)
        for name, D, sharp in factor.fixtures(n):
            value, cofactors = factor.coefficients(D, n)
            a = sum(z.abs2() for z in D.values())
            T = sum(z.abs2() for z in cofactors.values())
            B, K, lower_rate, upper_rate = factor.constants(n)
            haf = factor.hafnian_polynomial(D, {}, n)
            Q4 = sum(haf(U)[0].abs2() for U in combinations(range(n), 4))
            edges = list(combinations(range(n), 2))
            variance = sum((D.get(e, E()).abs2()-a/M)**2 for e in edges)
            require(L*a*a-Q4 >= Q(3, 8)*variance, "Quartet magnitude-slack estimate")
            require(B*a**m-value.abs2() >= B*kappa*a**(m-2)*variance,
                    "Full scalar hafnian magnitude slack")
            eta = T/(K*a**q)
            u = {e: D.get(e, E()).abs2()/a for e in edges}
            p = {e: cofactors[e].abs2()/T for e in edges}
            diagnostic = (sum((u[e]+p[e]/q-Q(m, q*M))**2 for e in edges)
                          + Q(2, q)*sum(u[e]*p[e] for e in edges))
            require(diagnostic <= Q(m*m, q*q)/kappa*(1-eta),
                    "Quantitative ground/cofactor complementarity")
            if sharp:
                require(eta == 1 and diagnostic == 0,
                        "Sharp sources have disjoint and uniformly complementary strengths")
            records.append(dict(sites=n, fixture=name, complementarity_slack=str(diagnostic),
                                cofactor_efficiency=str(eta)))
        complete = {e: ONE for e in combinations(range(n), 2)}
        value, _ = factor.coefficients(complete, n)
        require(value.abs2() == factor.constants(n)[0]*Q(M)**m,
                "Complete coherent source attains the scalar norm bound")
    require(len(records) == 11, "All eleven complementarity fixtures")
    return records


def all_even_checks():
    for n in range(6, 82, 2):
        cycle_constants(n)
        N = n-1
        numerators = (N**3-N*N+N-3, N-3, N-1, (N-4)*N*N+N-2)
        require(min(numerators) > 0, "Every transverse Hessian coefficient is positive")
    N = 5
    require(Q(2*(N**3-N*N+N-3), N*(N*N+1)) == Q(102, 65), "Six-site core coefficient")
    require(Q((N-4)*N*N+N-2, N*(N-2)*(N*N+1)) == Q(14, 195),
            "Six-site root coefficient")
    N = 3
    require(Q((N-4)*N*N+N-2, N*(N-2)*(N*N+1)) == Q(-4, 15),
            "Four-site scalar relaxation has a negative root mode")
    return dict(even_sizes=list(range(6, 82, 2)), four_site_root_coefficient="-4/15")


def main():
    dependencies = json.loads((HERE/"dependencies.json").read_text())
    for name, digest in dependencies.items():
        require(hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest,
                "Pinned dependency: "+name)
    result = dict(status="PASS",
                  evidence_status="Written proofs with exact supporting checks; independent audit pending",
                  cycle_incidences=[cycle_census(n) for n in (6, 8, 10, 12)],
                  matching_transversals=[matching_transversals(n) for n in (4, 6)],
                  cofactor_diagnostics=scalar_slack(),
                  constrained_hessians=ground_hessian.check(),
                  all_even_constants=all_even_checks(), dependencies=dependencies,
                  conclusions=["Unique maximum-response ground family for every even n >= 6",
                               "Sharp scalar W response inequality near that family",
                               "No better W design has sufficiently near-maximal response efficiency"],
                  limitations=["Exact global W optimum remains open",
                               "No explicit efficiency-neighborhood radius",
                               "The analytic rigidity and compactness arguments require the written proof"])
    paths = [p for p in HERE.iterdir() if p.suffix in (".py", ".md", ".json")
             and p.name != "results.json"]
    paths += [ROOT/"notes/w-cofactor-rigidity-2026-09-27.md"]
    result["sha256"] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in sorted(paths)}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
