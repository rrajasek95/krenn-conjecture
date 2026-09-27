#!/usr/bin/env python3
"""Exact support for the all-even uniform-odd-core W theorem."""

from functools import lru_cache
from fractions import Fraction as Q
from itertools import combinations
from math import comb, prod
from pathlib import Path
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "computations/boundary-structure-2026-09-26"))
from exact import E, ONE, ZERO, OMEGA, require, outputs, cell
import octahedral


def power(z, n):
    result = ONE
    for _ in range(n):
        result *= z
    return result


def double_factorial(k):
    return prod(range(1, k + 1, 2))


def matching_sums(ground):
    @lru_cache(None)
    def haf(vertices):
        if not vertices:
            return ONE
        i = vertices[0]
        return sum((ground.get(tuple(sorted((i, j))), ZERO)
                    * haf(tuple(v for v in vertices if v not in (i, j)))
                    for j in vertices[1:]), ZERO)
    return haf


def ground_source(n, w, z):
    N = n - 1
    require(len(z) == N, "One root coupling for each core site")
    return {(i, j): w for i, j in combinations(range(1, n), 2)} | {
        (0, i + 1): v for i, v in enumerate(z)}


def check_fixture(n, w, z):
    N, m = n - 1, n // 2
    require(bool(w) and not sum(z, ZERO), "Nonzero core and zero-sum root couplings")
    ground = ground_source(n, w, z)
    haf = matching_sums(ground)
    require(not haf(tuple(range(n))), "Ground matching terms cancel")
    c = double_factorial(N - 2) * power(w, m - 1)
    d = double_factorial(N - 4) * power(w, m - 2)
    require(c == (N - 2) * w * d, "Adjacent double-factorial relation")
    cofactors = {}
    for i, j in combinations(range(n), 2):
        actual = haf(tuple(v for v in range(n) if v not in (i, j)))
        expected = c if i == 0 else -d * (z[i - 1] + z[j - 1])
        require(actual == expected, "Every complementary matching sum")
        cofactors[i, j] = actual
    rows = [sum(v.abs2() for edge, v in cofactors.items() if i in edge)
            for i in range(n)]
    b = sum(v.abs2() for v in z)
    expected = [N * c.abs2()] + [
        c.abs2() + d.abs2() * (b + (N - 4) * v.abs2()) for v in z]
    require(rows == expected, "All response row norms")
    require(all(rows), "All response rows are nonzero")
    a = sum(v.abs2() for v in ground.values())
    x = b / (comb(N, 2) * w.abs2())
    kappa = Q(N - 1, N - 2)
    beta = sum(Q(1, r) for r in rows)
    beta_lower = (Q(1, N) + N / (1 + kappa * x)) / c.abs2()
    require(beta >= beta_lower, "Core-row Cauchy-Schwarz lower bound")
    q = m - 1
    sharp = Q(n * double_factorial(N)**2, comb(n, 2)**m * (N*N + 1))
    ratio = Q(N*N + 1) * (1 + kappa*x) / ((1+x)**q * (N*N+1+kappa*x))
    bound = Q(n * q**q, m**m) / (a**q * beta)
    require(bound <= sharp * ratio, "Universal response bound implies the new rate curve")
    if n >= 6:
        require(ratio <= 1 and (ratio < 1 or b == 0), "Strict gap for nonzero root ground strength")
    return dict(sites=n, ground_strength=str(a), root_strength=str(b),
                cofactor_count=len(cofactors), harmonic_sum=str(beta),
                response_rate_bound=str(bound), theorem_rate_bound=str(sharp*ratio),
                loss_factor=str(ratio))


def check_constants():
    records = []
    for n in range(6, 82, 2):
        N, m = n-1, n//2
        q, kappa = m-1, Q(N-1, N-2)
        sharp = Q(n * double_factorial(N)**2, comb(n, 2)**m * (N*N+1))
        L0 = Q((N*q)**q, double_factorial(N-2)**2) * (Q(1, N)+N)
        require(Q(n*q**q, m**m)/L0 == sharp, "Zero-root rate is exactly R_*")
        require(q-kappa == Q((N-1)*(N-4), 2*(N-2)) > 0,
                "Positive constant term in the derivative numerator")
        require(kappa*(q-1) > 0, "Positive linear term in the derivative numerator")
        # Squared amplitudes suffice to check the normalized equality source.
        lam2 = Q(N*N*double_factorial(N-2)**2, N*N+1)
        require(n*lam2/Q(N*m)**m == sharp, "Attaining source rate")
        records.append(dict(sites=n, optimum=str(sharp),
                            derivative_constant=str(q-kappa),
                            derivative_linear=str(kappa*(q-1))))
    return records


def check_outputs_and_scope():
    n, N = 6, 5
    source = {(i, j, 0, 0): ONE for i, j in combinations(range(1, n), 2)}
    for i in range(1, n):
        source[0, i, 0, 1] = E(N)
        source[0, i, 1, 0] = ONE
    expected = {tuple(int(v == i) for v in range(n)): E(N*double_factorial(N-2))
                for i in range(n)}
    require(outputs(source, n=n, colors=2) == expected, "Only equal W words survive at the one-root source")
    z = [E(1, 1), E(2, -1), E(3, 1), E(-1, 2)]
    z.append(-sum(z, ZERO))
    require(all(z), "The cancellation completion has complete ground support")
    source.update({(0, i+1, 0, 0): value for i, value in enumerate(z)})
    require(outputs(source, n=n, colors=2) == expected,
            "Adding zero-sum root ground couplings preserves the exact W output")

    z = [ONE, OMEGA, OMEGA*OMEGA]
    ground = ground_source(4, ONE, z)
    haf = matching_sums(ground)
    require(not haf(tuple(range(4))), "Four-site negative control has zero ground output")
    C = {(i, j): haf(tuple(v for v in range(4) if v not in (i, j)))
         for i, j in combinations(range(4), 2)}
    rows = [sum(v.abs2() for edge, v in C.items() if i in edge) for i in range(4)]
    a, beta = sum(v.abs2() for v in ground.values()), sum(Q(1, r) for r in rows)
    require(a*beta == 8, "Four-site response threshold is 8, not 10")
    source = {(i, j, 0, 0): v for (i, j), v in ground.items()}
    for i in range(4):
        for j in range(4):
            if i != j:
                source[cell(i, j, 1, 0)] = C[tuple(sorted((i, j)))].conjugate()/rows[i]
    actual = outputs(source, n=4, colors=2)
    W = {tuple(int(v == i) for v in range(4)): ONE for i in range(4)}
    require(all(actual.get(word, ZERO) == value for word, value in W.items()),
            "Minimum response completion produces all W coefficients")
    extras = {word: value for word, value in actual.items() if word not in W}
    require(bool(extras), "Four-site relaxed response is not an exact W design")

    for x in (Q(0), Q(1, 2), Q(1), Q(2), Q(10)):
        f = (1+x)*(Q(1, 3)+Q(3)/(1+2*x))
        require(f-Q(8, 3) == 2*(x-1)**2/(3*(1+2*x)), "Four-site minimum identity")

    bad_z = [ONE] * 5
    rejected = False
    try:
        check_fixture(6, ONE, bad_z)
    except ValueError:
        rejected = True
    require(rejected, "Nonzero root sum must be rejected")
    require(bool(matching_sums(ground_source(6, ONE, bad_z))(tuple(range(6)))),
            "Violating the zero-sum condition really produces ground output")
    require(C[1, 2] != z[0]+z[1], "Wrong sign in an internal cofactor is rejected")
    return dict(one_root_output="exact W", complete_ground_support_output="exact W",
                four_site_relaxed_rate="1/8",
                four_site_unwanted_outputs=len(extras), zero_sum_mutation="REJECTED",
                cofactor_sign_mutation="REJECTED")


def main():
    dependencies = json.loads((HERE/"dependencies.json").read_text())
    for path, digest in dependencies.items():
        require(hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == digest,
                "Pinned dependency: "+path)
    fixtures = []
    for n in range(4, 14, 2):
        z = [E(i+1, (i % 3)+1) for i in range(n-2)]
        z.append(-sum(z, ZERO))
        fixtures.append(check_fixture(n, E(2, 1), z))
        fixtures.append(check_fixture(n, E(1, -1), [ZERO]*(n-1)))
    result = dict(status="PASS",
                  evidence_status="Written proof with exact supporting checks; independent audit pending",
                  fixtures=fixtures, rate_constants=check_constants(),
                  scope_checks=check_outputs_and_scope(),
                  octahedral=octahedral.check(matching_sums), dependencies=dependencies,
                  unresolved="Nonuniform cores and unrestricted all-even W optimality")
    files = [p for p in HERE.iterdir() if p.suffix in (".py", ".md", ".json")
             and p.name != "results.json"]
    files.append(ROOT/"notes/w-state-coherent-odd-core-2026-09-27.md")
    files.append(ROOT/"notes/w-state-octahedral-ground-gap-2026-09-27.md")
    result["sha256"] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in sorted(files)}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
