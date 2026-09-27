#!/usr/bin/env python3
"""Exact support for the star fidelity certificate and boundary support test."""

from fractions import Fraction as Q
from itertools import combinations, product
from math import factorial
from pathlib import Path
import hashlib
import importlib.util
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    value = importlib.util.module_from_spec(spec)
    sys.modules[name] = value
    spec.loader.exec_module(value)
    return value


G = module("star_general_rate", "computations/general-complex-rate-2026-09-26/verify.py")
E = module("star_eisenstein", "computations/boundary-structure-2026-09-26/exact.py")
C, ZERO, ONE = G.C, G.ZERO, G.ONE


def coefficient_power(h, degree):
    return tuple(degree if i == h else 0 for i in range(3))


def star(source, root, color):
    result = ONE
    for i in range(source.n):
        if i != root:
            result *= source.edge(root, i, color, color)
    return result


def constant(n):
    m, N, D = n // 2, n - 1, n // 2 - 1
    involutions = [1, 1]
    for j in range(2, N + 1):
        involutions.append(involutions[-1] + (j - 1) * involutions[-2])
    P = factorial(n) // (2**m * factorial(m))
    M = 3**N * involutions[N]
    U, V = 2**N * M, 2 * (P + M)
    T = (4 * D + 1) * (1 + 2**N) * (P + U) * (U + V)
    require(T == G.constants(n)["T"], "Independent inherited constant formula")
    return Q(1, 3**m * 2**(2 * D) * T)


def scalar_checks():
    records = []
    for D in range(1, 6):
        W = {}
        for j in range(1, D + 1):
            for k, exponent in enumerate(((2*j, 0, 0), (0, 2*j, 0),
                                         (j, j, 0), (0, j, j), (1, 0, 2*j-1))):
                W[exponent] = W.get(exponent, ZERO) + C(j + k + 1, j - 2*k)
        lam = C(Q(2, 3), Q(1, 5))
        g = G.add({(0, 0, 0): ONE}, G.scale(ONE / lam, W))
        half = {e: c / 2**(sum(e)//2) for e, c in g.items()}
        residual = G.add(G.mul(half, half), G.scale(-1, g))
        top = G.homogeneous(W, 2*D)
        expected = G.scale(ONE / (2**(2*D) * lam * lam), G.mul(top, top))
        require(G.homogeneous(residual, 4*D) == expected, "Full highest homogeneous identity")
        require(not G.homogeneous(residual, 0) and not G.homogeneous(residual, 2),
                "Residual starts at degree four")
        w = top[2*D, 0, 0]
        actual = residual[4*D, 0, 0]
        require(actual == w*w / (2**(2*D)*lam*lam), "Pure highest coefficient")
        require(actual.abs2() == w.abs2()**2 / (2**(4*D)*lam.abs2()**2),
                "Complex modulus is handled after squaring")
        require(actual != w*w / (2**D*lam*lam), "Wrong rotation scale rejected")
        require(actual != w*w / (2**(2*D)*lam.abs2()), "Wrong complex denominator rejected")
        records.append(dict(sites=2*(D+1), highest_degree=4*D,
                            highest_monomials=len(expected)))
    return records


def dense_source(n):
    source = G.Source(n)
    for p, q in combinations(range(n), 2):
        for h, k in product(range(3), repeat=2):
            source.put(p, q, h, k, C(Q(1+p+2*q+h+k, 1000),
                                     Q(1+2*p+q+2*h-k, 1000)))
    return source


def literal_star_checks():
    records = []
    for n in (4, 6, 8):
        source = dense_source(n)
        count = 0
        for root in range(n):
            vertices = tuple(i for i in range(n) if i != root)
            for h in range(3):
                response = source.response(root, vertices, (h,)*(n-1))
                coefficient = response.get(coefficient_power(h, n-1), ZERO)
                expected = star(source, root, h)
                require(coefficient == expected and expected, "Literal divided star coefficient")
                require(coefficient != factorial(n-1)*expected, "Uncanceled factorial rejected")
                count += 1
        records.append(dict(sites=n, root_color_checks=count))
    return records


def ground_fixture():
    w, one = E.OMEGA, E.ONE
    ground = {(0, 1): one, (2, 3): one, (0, 2): w, (1, 3): w,
              (0, 3): w*w, (1, 2): w*w,
              **{(i, j): one for i in range(4) for j in (4, 5)}, (4, 5): E.E(-2)}
    require(len(ground) == 15 and all(ground.values()), "Full support fixture")
    require(not E.hafnian(ground, tuple(range(6))), "Ground output is zero")
    stars = []
    for p in range(6):
        value = one
        for i in range(6):
            if i != p:
                value *= ground[tuple(sorted((p, i)))]
        stars.append(value)
    require(stars == [one]*4 + [E.E(-2)]*2, "Six exact star products")
    require(sum(z.abs2() for z in ground.values()) == 18, "Ground normalization")
    return dict(star_products=[1, 1, 1, 1, -2, -2],
                squared_source_norm=18, normalized_max_squared_star=str(Q(4, 18**5)))


def binary_product(source, root, palette):
    """Build the terminal response using only singleton factors."""
    vertices = tuple(i for i in range(source.n) if i != root)
    result = {}
    for word in product(palette, repeat=source.n-1):
        polynomial = {(0, 0, 0): ONE}
        for i, color in zip(vertices, word):
            mean = {coefficient_power(h, 1): source.edge(root, i, h, color)
                    for h in range(3)}
            polynomial = G.mul(polynomial, G.clean(mean))
        if polynomial:
            result[word] = polynomial
        actual = source.response(root, vertices, word)
        require(G.homogeneous(actual, source.n-1) == polynomial,
                "Singleton product equals highest response")
    return result


def witnesses(source, root, palette):
    return [i for i in range(source.n) if i != root and
            all(not source.edge(root, i, h, k)
                for h in range(3) for k in palette)]


def support_checks():
    perfect = G.Source(4)
    for h, edges in enumerate((((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))):
        for p, q in edges:
            perfect.put(p, q, h, h, Q(1, 4))
    out = {w: perfect.output(w) for w in product(range(3), repeat=4)}
    require(all(z == (C(Q(1, 16)) if len(set(w)) == 1 else ZERO)
                for w, z in out.items()), "Allowed four-site GHZ is not excluded")

    off = G.Source(6)
    for i in range(1, 6):
        for h, k in product(range(3), repeat=2):
            if h != k:
                off.put(0, i, h, k, C(Q(1, 20), Q(h-k, 100)))
    require(all(not star(off, p, h) for p in range(6) for h in range(3)),
            "Off-color control has no same-color star")
    require(all(not off.output(w) for w in product(range(3), repeat=6)),
            "Off-color star is a zero-output limit candidate")
    require(all(not witnesses(off, 0, B) for B in combinations(range(3), 2)),
            "Stronger column test excludes the off-color star")

    missing = G.Source(6)
    missing.cells = {cell: z for cell, z in off.cells.items() if cell[1] != 5}
    checks = 0
    for source, roots in ((perfect, range(4)), (off, (0,)), (missing, (0,)),
                          (dense_source(6), (0,))):
        for root in roots:
            for palette in combinations(range(3), 2):
                tensor = binary_product(source, root, palette)
                require(bool(tensor) == (not witnesses(source, root, palette)),
                        "Product vanishing iff a two-column block vanishes")
                checks += 1
    return dict(binary_palette_checks=checks, allowed_four_site_perfect_GHZ="PASSES",
                off_color_star_with_all_diagonal_cells_zero="EXCLUDED_BY_COLUMN_TEST",
                absent_edge_control="PASSES_NECESSARY_TEST",
                sufficiency_claim=False)


def certificate_checks():
    records = []
    for name, source, _ in G.sources():
        output = {w: source.output(w) for w in product(range(3), repeat=source.n)}
        lam = sum((output[(h,)*source.n] for h in range(3)), ZERO) / 3
        error2 = sum((z-(lam if len(set(w)) == 1 else ZERO)).abs2()
                     for w, z in output.items())
        total2 = sum(z.abs2() for z in output.values())
        S = sum(z.abs2() for z in source.cells.values())
        eta = max(star(source, p, h).abs2() for p in range(source.n)
                  for h in range(3)) / S**(source.n-1)
        kappa = constant(source.n)
        require(error2 >= kappa*kappa*eta*eta*lam.abs2(), "Squared amplitude certificate")
        require(3*lam.abs2()+error2 == total2, "Orthogonal target split")
        fidelity = 3*lam.abs2()/total2
        require(fidelity <= 3/(3+kappa*kappa*eta*eta), "Fidelity ceiling")
        scale = C(Q(2, 3), Q(1, 7))
        scaled = G.Source(source.n)
        scaled.cells = {cell: scale*z for cell, z in source.cells.items()}
        scaled_S = sum(z.abs2() for z in scaled.cells.values())
        scaled_eta = max(star(scaled, p, h).abs2() for p in range(source.n)
                         for h in range(3)) / scaled_S**(source.n-1)
        require(scaled_eta == eta, "Complex source rescaling invariance")
        records.append(dict(name=name, nonzero_star=bool(eta)))
    return records


def main():
    dependencies = json.loads((HERE / "dependencies.json").read_text())
    for name, digest in dependencies.items():
        require(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest,
                "Pinned dependency: " + name)
    result = dict(
        status="PASS",
        evidence_status="Written proof with exact supporting checks; independent audit pending",
        scalar_highest_degree=scalar_checks(),
        literal_star_coefficients=literal_star_checks(),
        full_support_rank25_ground=ground_fixture(),
        support_tests=support_checks(),
        exact_source_inequalities=certificate_checks(),
        constants={str(n): str(constant(n)) for n in (4, 6, 8, 10, 12)},
        negative_controls=["Wrong rotation factor rejected",
                           "Wrong complex denominator rejected",
                           "Uncanceled singleton factorial rejected",
                           "Diagonal-only test misses an off-color star"],
        conclusions=["A nonzero same-color star forces a local GHZ fidelity ceiling",
                     "All full-support single-color zeros are excluded at every even size at least four",
                     "High-fidelity limits require a zero two-column block at every root and palette"],
        limitations=["Unrestricted square-root rate law remains open",
                     "Necessary support conditions are not sufficient",
                     "Arbitrary-size inequalities and limiting arguments rely on the written proof",
                     "Constants are conservative; no practical fidelity guarantee is claimed",
                     "Independent audit is pending"],
        dependencies=dependencies)
    paths = [p for p in HERE.iterdir() if p.suffix in (".py", ".md", ".json")
             and p.name != "results.json"]
    paths.append(ROOT / "notes/ghz-star-fidelity-gap-2026-09-27.md")
    result["sha256"] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in sorted(paths)}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
