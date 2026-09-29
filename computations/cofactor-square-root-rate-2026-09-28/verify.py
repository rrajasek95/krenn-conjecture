#!/usr/bin/env python3
"""Exact checks for residual coercivity and the cofactor square-root test."""

from fractions import Fraction as Q
from itertools import combinations, product
from math import ceil, comb, factorial, isqrt
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


G0 = module("cofactor_general", "computations/general-complex-rate-2026-09-26/verify.py")
EX = module("cofactor_exact", "computations/boundary-structure-2026-09-26/exact.py")
C, ZERO, ONE = G0.C, G0.ZERO, G0.ONE


def exact_norm(polynomial):
    total = Q(0)
    for c in polynomial.values():
        squared = c.abs2()
        a, b = isqrt(squared.numerator), isqrt(squared.denominator)
        require(a*a == squared.numerator and b*b == squared.denominator,
                "Fixture has rational coefficient moduli")
        total += Q(a, b)
    return total


def half(polynomial):
    return {e: c / 2**(sum(e)//2) for e, c in polynomial.items()}


def residual(g):
    return G0.add(G0.mul(half(g), half(g)), G0.scale(-1, g))


def constants(n):
    cs = G0.constants(n)
    m, D, N, P, M, T = (cs[k] for k in ("m", "D", "N", "P", "M", "T"))
    K = comb(2*D+3, 3)
    B = 2**D*K*(3+2**D)
    QD = 12*B*max(Q(1), Q(64, 7)*factorial(m))
    U = 2**N*M
    H0 = 2**(N-1)*G0.involutions(N-1)
    J = 2*QD+(P+U)*P
    G = n*(2*H0*(J+9*P*P)+P**3)
    Cparity = 2**m*P
    Kglobal = 576*Cparity*G*G*T
    return dict(n=n, m=m, D=D, N=N, P=P, K=K, B=B, QD=QD, T=T,
                H0=H0, J=J, G=G, Kglobal=Kglobal)


def polynomial_checks():
    records = []
    for D in range(1, 6):
        cs = constants(2*D+2)
        tests = []
        # Real coefficients with a torus phase substitution keep exact moduli.
        for scale in (Q(1, 16), Q(1, 2), Q(4, 5)):
            base = {(2, 0, 0): C(scale)}
            power = {(0, 0, 0): ONE}
            g = dict(power)
            for j in range(1, D+1):
                power = G0.mul(power, base)
                g = G0.add(g, G0.scale(Q(1, factorial(j)), power))
            tests.append(g)
        for seed in range(6):
            tail = {}
            for j in range(1, D+1):
                for k, e in enumerate(((2*j, 0, 0), (j, j, 0), (0, j, j))):
                    value = Q((seed+2*k+j) % 7 - 3, 200*D)
                    tail[e] = tail.get(e, ZERO) + C(0, 1)**e[0]*value
            tests.append(G0.add({(0, 0, 0): ONE}, tail))
        large = G0.add({(0, 0, 0): ONE}, {(2*D, 0, 0): C(100)})
        require(exact_norm(residual(large)) > 1, "Large-tail negative control")
        checks = 0
        for g in tests:
            tail = G0.add(g, {(0, 0, 0): -ONE})
            u = half(tail)
            u2 = G0.mul(u, u)
            rpoly = residual(g)
            r = exact_norm(rpoly)
            require(r <= 1, "Small-residual fixture")
            lower = sum(c.abs2() for c in u.values())
            require(exact_norm(u2) >= lower, "Polynomial-square lower bound")
            b = exact_norm(u)
            require(lower*cs["K"] >= b*b, "Coefficient Cauchy-Schwarz bound")
            require(b*b <= cs["K"]*(r+(2+2**D)*b), "Coercive quadratic inequality")
            require(exact_norm(tail) <= cs["B"], "Uniform tail bound")
            rho2 = Q(1, 2*cs["B"])
            scaled_tail = {e: c*rho2**(sum(e)//2) for e, c in tail.items()}
            require(exact_norm(scaled_tail) <= Q(1, 2), "Fixed normalization radius")
            scaled_r = {e: c*rho2**(sum(e)//2) for e, c in rpoly.items()}
            require(exact_norm(scaled_r) <= rho2*rho2*r, "Residual starts in degree four")
            quad = exact_norm(G0.homogeneous(g, 2))
            require(quad**(D+1) <= cs["QD"]**(D+1)*r, "Quadratic coefficient bound")
            checks += 1
        if D >= 2:
            require(exact_norm(G0.add(tests[2], {(0, 0, 0): -ONE})) > Q(1, 2),
                    "No inherited small-tail hypothesis")
        # Truncating to the input degree loses the obstruction.
        truncated = {e: c for e, c in residual(tests[0]).items() if sum(e) <= 2*D}
        require(not truncated and residual(tests[0]), "Truncated residual is insufficient")
        records.append(dict(sites=2*D+2, polynomials_checked=checks,
                            QD=str(cs["QD"]), fixed_radius_squared=str(Q(1, 2*cs["B"]))))
    return records


def source_output(source):
    out = {w: source.output(w) for w in product(range(3), repeat=source.n)}
    lam = sum((out[(h,)*source.n] for h in range(3)), ZERO)/3
    error = {w: z-(lam if len(set(w)) == 1 else ZERO) for w, z in out.items()}
    return out, lam, error


def defects(source, lam=ZERO):
    n = source.n
    rows = {}
    for i, h in product(range(3), repeat=2):
        cof = [[source.cofactor(h, r, q) if r != q else ZERO for q in range(n)]
               for r in range(n)]
        matrix = [[sum((source.edge(p, r, i, h)*cof[r][q] for r in range(n)), ZERO)
                   -(lam if i == h and p == q else ZERO)
                   for q in range(n)] for p in range(n)]
        rows[i, h] = matrix
    return rows


def norm2(matrix):
    return sum(c.abs2() for row in matrix for c in row)


def scalar_rank(source):
    return EX.rank([[EX.E(source.edge(p, q, 0, 0).re) for q in range(source.n)]
                    for p in range(source.n)])


def triangle_rank():
    rows = []
    for word in product(range(3), repeat=3):
        row = []
        for i, h in product(range(3), repeat=2):
            j, k = [v for v in range(3) if v != i]
            row.append(EX.ONE if word[i] == h and word[j] == word[k] == 0 else EX.ZERO)
        rows.append(row)
    return EX.rank(rows)


def boundary_examples():
    tri = G0.Source(6)
    for block in ((0, 1, 2), (3, 4, 5)):
        for p, q in combinations(block, 2):
            tri.put(p, q, 0, 0, ONE)
    octa = G0.Source(6)
    blocks = (((1, 1), (1, -1)), ((1, 1), (1, -1)), ((1, 1), (-1, 1)))
    for (g, h), block in zip(combinations(range(3), 2), blocks):
        for i, j in product(range(2), repeat=2):
            octa.put(2*g+i, 2*h+j, 0, 0, block[i][j])
    prism = G0.Source(6)
    for color, edges in enumerate((((0, 1), (3, 4)), ((1, 2), (4, 5)), ((0, 2), (3, 5)))):
        for p, q in edges:
            prism.put(p, q, color, color, ONE)
    result = []
    for name, source, expected in (("singular_two_triangles", tri, 72),
                                   ("signed_octahedron", octa, 192),
                                   ("canonical_prism", prism, 0)):
        output, lam, error = source_output(source)
        require(all(not c for c in output.values()), "Exact zero output")
        S = sum(c.abs2() for c in source.cells.values())
        degrees = [sum(source.edge(p, q, i, h).abs2()
                       for q in range(6) for i, h in product(range(3), repeat=2))
                   for p in range(6)]
        require(all(d == S/3 for d in degrees), "Balanced source")
        d2 = max(norm2(mat) for mat in defects(source).values())
        require(d2 == expected, "Exact nonzero cofactor test or prism control")
        # Each example passes the previous support test.
        for p in range(6):
            for palette in combinations(range(3), 2):
                require(any(all(not source.edge(p, q, i, h)
                                for i in range(3) for h in palette)
                            for q in range(6) if q != p), "Necessary two-column zeros")
        if name != "canonical_prism":
            # Pure ground is the only nonzero receiving word.
            for p in range(6):
                vertices = tuple(i for i in range(6) if i != p)
                response = source.response(p, vertices, (0,)*5)
                require(not response, "All root response degrees vanish")
            require(scalar_rank(source) == 6, "Scalar source matrix rank")
        else:
            for p in range(6):
                neighbors = [q for q in range(6) if q != p and
                             any(source.edge(p, q, i, h)
                                 for i, h in product(range(3), repeat=2))]
                require(len(neighbors) == 2,
                        "Prism root means cannot occupy three distinct receiving sites")
        row = dict(name=name, squared_source_norm=str(S),
                   cofactor_defect_squared=str(d2), normalized_defect_squared=str(d2/S**3),
                   all_higher_binary_responses_vanish=True)
        if name == "singular_two_triangles":
            require(triangle_rank() == 7, "Singular triangle response rank")
            row.update(triangle_response_ranks=[7, 7], output_derivative_rank=49)
            expected_matrix = [[C(2 if (p < 3) != (q < 3) else 0) for q in range(6)]
                               for p in range(6)]
            require(defects(source)[0, 0] == expected_matrix, "Explicit two-triangle product")
        result.append(row)
    return result


def small_error_checks():
    # Four sites permit exact GHZ, so arbitrarily small cube-relative
    # residuals can be tested without assuming a six-site near-counterexample.
    name, source, _ = next(G0.sources())
    out, lam, error = source_output(source)
    require(lam and not lam.im and lam.re > 0, "Real positive pure mean in fixture")
    ell = lam.re
    xi_upper = sum(G0.rect(c) for c in error.values())
    cs = constants(4)
    t_upper = cs["T"]*xi_upper/ell**3
    require(0 < t_upper <= 1, "Nonzero small cube-relative error")
    d2 = max(norm2(mat) for mat in defects(source, lam).values())
    require(d2 > 0 and d2**cs["m"] <= cs["G"]**(2*cs["m"])*t_upper*t_upper,
            "Improved endpoint estimate on an actual off-color source")
    for root in range(4):
        vertices = tuple(i for i in range(4) if i != root)
        for palette in combinations(range(3), 2):
            cubic_upper = sum(G0.norm(G0.homogeneous(source.response(root, vertices, w), 3))
                              for w in product(palette, repeat=3))
            require(cubic_upper**cs["m"] <= (cs["J"]*ell)**cs["m"]*t_upper,
                    "Improved cubic response bound")
    require(cs["G"]**cs["m"]*t_upper <= (ell/2)**cs["m"], "Cofactor inverse condition")
    off2 = sum(c.abs2() for (_, _, i, h), c in source.cells.items() if i != h)
    require(off2**cs["m"]*ell**(2*cs["m"])
            <= (8*cs["G"])**(2*cs["m"])*t_upper*t_upper, "Improved diagonal reduction")
    return dict(source=name, cube_relative_error_upper=str(t_upper),
                nonzero_defect=True, all_roots_and_palettes_checked=True,
                rectangular_norm_upper_bounds_used=True)


def budget_checks():
    prior = json.loads((ROOT / "computations/quantitative-proof-identities-2026-09-26/results.json").read_text())
    records = []
    for row in prior["global_diagonal_rate_constants"]:
        n = row["sites"]
        cs = constants(n)
        m, D, P, T, G, Kg = (cs[k] for k in ("m", "D", "P", "T", "G", "Kglobal"))
        k = Q(3)+Q(3*D, 2)
        q = 3+Q(m, 2)*(k+2)
        cn = Q(row["amplitude_lower_bound_c"])
        b = min(cn, Q(1, 2*P**ceil(k-1)))
        candidates = [Q(1, 3**(2*m)*T*T*P**(2*ceil(q-3))),
                      1/(T*T*(6*G*P**ceil(k/2))**(2*m)),
                      (b/(4*P**ceil(q-k)))**2,
                      (b/(4*Kg))**m]
        gamma = min(candidates)
        require(gamma*3**(2*m)*T*T*P**(2*ceil(q-3)) <= 1, "Residual at most one")
        require(gamma*T*T*(6*G*P**ceil(k/2))**(2*m) <= 1, "Inverse budget")
        require(gamma*16*P**(2*ceil(q-k)) <= b*b, "Original error budget")
        require(gamma*(4*Kg)**m <= b**m, "Projected quadratic error budget")
        require(2*b*P**ceil(k-1) <= 1, "Projected fidelity threshold")
        require(T**2 <= T**m, "Rational bound on T to power 2/m")
        require((q-3)/m-1 == k/2 and 2*q/m-2-Q(6, m) == k,
                "Two exponent balances")
        require(1/(q-1) == Q(16, 3*n*n+14*n+32), "Universal rate exponent")
        records.append(dict(sites=n, amplitude_power=str(q), rate_exponent=str(1/(q-1)),
                            gamma=str(gamma), G=str(G), T=str(T),
                            diagonal_constant=str(cn), selected_budget=candidates.index(gamma)+1))
    for n in range(6, 102, 2):
        m = n//2
        k = 3+Q(3*(m-1), 2)
        q = 3+Q(m, 2)*(k+2)
        require(q-k >= 0 and q-3 >= 0 and k >= 6, "Nonnegative normalization powers")
        require(1/(q-1) == Q(16, 3*n*n+14*n+32), "All-size exponent algebra")
        require(q < 1+Q(m, 2)*(k+4), "Strict improvement of previous power")
    return records


def scalar_matching_certificate():
    """Rebuild the inputs and replay an ideal-membership DAG over Q[x_1,...,x_12]."""
    certificate = json.loads((HERE / "scalar-matching-certificate.json").read_text())
    matching = ((0, 1), (2, 3), (4, 5))
    edges = [e for e in combinations(range(6), 2) if e not in matching]
    require(certificate["variables"] == [list(e) for e in edges], "Certificate variables")
    require(certificate["normalized_matching"] == [list(e) for e in matching],
            "Certificate normalizes one whole perfect matching")
    z = (0,)*12
    one = {z: Q(1)}

    def plus(p, q):
        out = dict(p)
        for e, c in q.items():
            out[e] = out.get(e, Q(0))+c
        return {e: c for e, c in out.items() if c}

    def times(p, q):
        out = {}
        for e, c in p.items():
            for f, d in q.items():
                key = tuple(a+b for a, b in zip(e, f))
                out[key] = out.get(key, Q(0))+c*d
        return {e: c for e, c in out.items() if c}

    def decode(rows):
        out = {}
        for powers, coefficient in rows:
            require(len(powers) == 12 and all(isinstance(v, int) and v >= 0 for v in powers),
                    "Ordinary polynomial multiplier")
            key = tuple(powers)
            require(key not in out, "No duplicate multiplier monomial")
            out[key] = Q(coefficient)
        return out

    D = [[{} for _ in range(6)] for _ in range(6)]
    for j, (p, q) in enumerate(edges):
        D[p][q] = D[q][p] = {tuple(int(i == j) for i in range(12)): Q(1)}
    for p, q in matching:
        D[p][q] = D[q][p] = one
    cof = [[{} for _ in range(6)] for _ in range(6)]
    for i, j in combinations(range(6), 2):
        a, b, c, d = [k for k in range(6) if k not in (i, j)]
        cof[i][j] = cof[j][i] = plus(plus(times(D[a][b], D[c][d]),
                                             times(D[a][c], D[b][d])),
                                       times(D[a][d], D[b][c]))
    equations = [[{} for _ in range(6)] for _ in range(6)]
    for p, q in product(range(6), repeat=2):
        for r in range(6):
            equations[p][q] = plus(equations[p][q], times(D[p][r], cof[r][q]))
    values = []
    input_positions = []
    for index, node in enumerate(certificate["nodes"]):
        if "input_position" in node:
            p, q = node["input_position"]
            require(p in range(6) and q in range(6), "Valid cofactor-product input")
            value = equations[p][q]
            input_positions.append((p, q))
        else:
            value = {}
            for earlier, multiplier in node["terms"]:
                require(isinstance(earlier, int) and 0 <= earlier < index,
                        "Acyclic polynomial derivation")
                value = plus(value, times(decode(multiplier), values[earlier]))
        require(value, "Every retained node is nonzero")
        values.append(value)
    last = certificate["final_node"]
    require(last == len(values)-1 and values[last] == one,
            "Exact derivation of 1 from the normalized D C entries")
    # Altering one final multiplier adds a nonzero polynomial, which must fail.
    earlier, multiplier = certificate["nodes"][last]["terms"][0]
    corrupt = plus(values[last], values[earlier])
    require(corrupt != one, "Corrupted final multiplier rejected")
    return dict(arithmetic_nodes=len(values), cofactor_inputs=len(input_positions),
                maximum_intermediate_monomials=max(map(len, values)),
                maximum_intermediate_degree=max(sum(e) for p in values for e in p),
                final_polynomial="1",
                conclusion="D C = 0 is impossible when the scalar six-site support has a perfect matching",
                sympy_required_for_replay=False)


def matching_gauge_check():
    source = G0.Source(6)
    for p, q in combinations(range(6), 2):
        source.put(p, q, 0, 0, C(p+q+1, p-q))
    scales = [ONE]*6
    for p, q in ((0, 1), (2, 3), (4, 5)):
        scales[q] = ONE/source.edge(p, q, 0, 0)
    total_scale = ONE
    for s in scales:
        total_scale *= s
    transformed = G0.Source(6)
    for (p, q, i, h), c in source.cells.items():
        transformed.put(p, q, i, h, scales[p]*scales[q]*c)
    before, after = defects(source)[0, 0], defects(transformed)[0, 0]
    for p, q in product(range(6), repeat=2):
        require(after[p][q] == total_scale*scales[p]/scales[q]*before[p][q],
                "Complex diagonal gauge preserves cofactor-product vanishing")
    require(all(transformed.edge(p, q, 0, 0) == ONE for p, q in ((0, 1), (2, 3), (4, 5))),
            "Every nonzero perfect matching can be normalized")
    return dict(matrix_entries=36, normalized_matching_edges=3)


def main():
    dependencies = json.loads((HERE / "dependencies.json").read_text())
    for name, digest in dependencies.items():
        require(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest,
                "Pinned dependency: " + name)
    result = dict(status="PASS",
                  evidence_status="Written proof with exact supporting checks; independent audit pending",
                  polynomial_coercivity=polynomial_checks(),
                  boundary_examples=boundary_examples(),
                  actual_small_error_source=small_error_checks(),
                  global_constants=budget_checks(),
                  scalar_perfect_matching_certificate=scalar_matching_certificate(),
                  complex_matching_normalization=matching_gauge_check(),
                  negative_controls=["Large polynomial tail produces a large residual",
                                     "Truncating the residual to the input degree loses the obstruction",
                                     "Prism has zero defect despite its known square-root law"],
                  conclusions=["Nonzero cofactor products at a zero imply a local square-root rate bound",
                               "Every balanced single-color six-site zero has a local square-root rate bound",
                               "An exact polynomial certificate excludes D C = 0 on scalar supports with a perfect matching",
                               "Unrestricted six-site exponent improves from 1/15 to 1/14",
                               "Possible square-root violations must limit to zero cofactor products"],
                  limitations=["Unrestricted square-root law remains open",
                               "Zero defect is not a counterexample",
                               "Universal inequalities use the written proof",
                               "Independent audit is pending"],
                  dependencies=dependencies)
    paths = [p for p in HERE.iterdir() if p.suffix in (".py", ".md", ".json")
             and p.name != "results.json"]
    paths.append(ROOT / "notes/cofactor-square-root-rate-2026-09-28.md")
    result["sha256"] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in sorted(paths)}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
