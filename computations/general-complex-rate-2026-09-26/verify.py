#!/usr/bin/env python3
"""Exact supporting checks for the general complex rate argument.

Uses the preceding package's Gaussian-rational arithmetic, but evaluates
new literal off-color matching responses directly. No floating-point tests.
Complex norm checks use |Re|+|Im| upper bounds, labeled as such in the output.
The analytic arbitrary-size proof remains in the accompanying research note.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product, combinations
from math import factorial, ceil
from pathlib import Path
import hashlib
import importlib.util
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PREVIOUS = ROOT / 'computations/quantitative-proof-identities-2026-09-26'
spec = importlib.util.spec_from_file_location('previous_rate_arithmetic', PREVIOUS / 'verify.py')
previous = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = previous
spec.loader.exec_module(previous)
C, ZERO, ONE = previous.C, previous.ZERO, previous.ONE


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def clean(p):
    return {e: c for e, c in p.items() if c}


def add(p, q):
    out = dict(p)
    for e, c in q.items():
        out[e] = out.get(e, ZERO) + c
    return clean(out)


def scale(c, p):
    return clean({e: c*v for e, v in p.items()})


def mul(p, q):
    out = {}
    for a, x in p.items():
        for b, y in q.items():
            e = tuple(i+j for i, j in zip(a, b))
            out[e] = out.get(e, ZERO) + x*y
    return clean(out)


def homogeneous(p, degree):
    return {e: c for e, c in p.items() if sum(e) == degree}


def rect(c):
    return abs(c.re) + abs(c.im)


def norm(p):
    return sum((rect(c) for c in p.values()), F(0))


def var(index, count=3):
    return {tuple(int(i == index) for i in range(count)): ONE}


def power(p, degree, count):
    out = {(0,)*count: ONE}
    for _ in range(degree):
        out = mul(out, p)
    return out


def embed(p, slot):
    return {(e + (0,)*3 if slot == 0 else (0,)*3 + e): c for e, c in p.items()}


def rotate(p, slot, odd=False):
    """g((s+t)/sqrt(2)) or g((-s+t)/sqrt(2)); odd case returns sqrt(2)*Psi."""
    out = {}
    bases = [add(var(i, 6), var(i+3, 6)) if slot == 0 else
             add(scale(-1, var(i, 6)), var(i+3, 6)) for i in range(3)]
    cache = {}
    for e, c in p.items():
        degree = sum(e)
        require(degree % 2 == int(odd), 'Parity before 45-degree rotation')
        term = {(0,)*6: c / C(2**((degree-int(odd))//2))}
        for i, k in enumerate(e):
            if (i, k) not in cache:
                cache[i, k] = power(bases[i], k, 6)
            term = mul(term, cache[i, k])
        out = add(out, term)
    return out


def pair(first, second, palette):
    out = {}
    a, b = palette
    for word, p in first.items():
        complement = tuple(b if color == a else a for color in word)
        out = add(out, scale((-1)**word.count(b), mul(p, second[complement])))
    return out


def involutions(n):
    a, b = 1, 1
    for j in range(2, n+1):
        a, b = b, b+(j-1)*a
    return b


def constants(n):
    m, D, N = n//2, n//2-1, n-1
    P = factorial(n)//(2**m*factorial(m))
    M = 3**N*involutions(N)
    U, V = 2**N*M, 2*(P+M)
    T = (4*D+1)*(1+2**N)*(P+U)*(U+V)
    Z = F(T, 4*M*M)
    K3 = 2**N*M*(1+12*max(F(1), F(64, 7)*factorial(m)*Z))
    H0 = 2**(N-1)*involutions(N-1)
    G = n*(2*H0*(K3+9*P)+P*P)
    return dict(m=m, D=D, N=N, P=P, M=M, T=T, Z=Z, K3=K3, G=G, L=24*m*P*G)


class Source:
    def __init__(self, n):
        self.n, self.cells = n, {}

    def put(self, p, q, i, j, value):
        if p > q:
            p, q, i, j = q, p, j, i
        self.cells[p, q, i, j] = C.cast(value)

    def edge(self, p, q, i, j):
        if p == q:
            return ZERO
        if p > q:
            p, q, i, j = q, p, j, i
        return self.cells.get((p, q, i, j), ZERO)

    def output(self, word):
        @lru_cache(None)
        def rec(vertices):
            if not vertices:
                return ONE
            p, rest = vertices[0], vertices[1:]
            return sum((self.edge(p, q, word[p], word[q]) *
                        rec(tuple(v for v in rest if v != q)) for q in rest), ZERO)
        return rec(tuple(range(self.n)))

    def response(self, root, vertices, word):
        @lru_cache(None)
        def rec(indices):
            if not indices:
                return {(0, 0, 0): ONE}
            i, rest = indices[0], indices[1:]
            mean = {tuple(int(c == j) for c in range(3)):
                    self.edge(root, vertices[i], j, word[i]) for j in range(3)}
            out = mul(clean(mean), rec(rest))
            for j in rest:
                weight = self.edge(vertices[i], vertices[j], word[i], word[j])
                if weight:
                    out = add(out, scale(weight, rec(tuple(k for k in rest if k != j))))
            return out
        return rec(tuple(range(len(vertices))))

    @lru_cache(None)
    def cofactor(self, color, p, q):
        vertices = tuple(i for i in range(self.n) if i not in (p, q))
        @lru_cache(None)
        def rec(vs):
            if not vs:
                return ONE
            i, rest = vs[0], vs[1:]
            return sum((self.edge(i, j, color, color)*rec(tuple(v for v in rest if v != j))
                        for j in rest), ZERO)
        return rec(vertices)


def sources():
    a = Source(4)
    for h, edges in enumerate([[(0, 1), (2, 3)], [(0, 2), (1, 3)], [(0, 3), (1, 2)]]):
        for p, q in edges:
            a.put(p, q, h, h, F(1, 4))
    a.put(0, 1, 0, 1, F(1, 2**180))
    yield 'allowed_four_site_with_tiny_off_color', a, True
    b = Source(4)
    b.cells = dict(a.cells)
    b.put(0, 1, 0, 1, C(F(1, 128), F(1, 128)))
    b.put(1, 3, 2, 0, C(0, F(-1, 64)))
    b.put(2, 3, 1, 2, F(-1, 128))
    yield 'complex_off_color_four_site', b, True
    c, t = Source(6), F(1, 10)
    for h, edges in enumerate([[(0, 1, 1), (3, 4, 1), (2, 5, t), (0, 2, t*t)],
                              [(1, 2, 1), (4, 5, 1), (0, 3, t)],
                              [(0, 2, 1), (3, 5, 1), (1, 4, t)]]):
        for p, q, w in edges:
            c.put(p, q, h, h, w*F(1, 4))
    c.put(0, 1, 0, 2, C(0, t**3/4))
    c.put(3, 4, 1, 0, -t**3/8)
    yield 'six_site_prism_with_diagonal_and_off_color_errors', c, True
    d = Source(6)
    for p in range(6):
        for q in range(p+1, 6):
            for i, j in product(range(3), repeat=2):
                d.put(p, q, i, j, F(1, 20) if i == j else
                      C(F((p+2*q+i-j) % 5-2, 100), F((2*p+q-i+j) % 3-1, 100)))
    yield 'dense_complex_six_site', d, False


def literal_source_checks():
    results = []
    for name, source, full_rotation in sources():
        n = source.n
        cs = constants(n)
        m, N, P, M, T, K3, G = (cs[k] for k in ['m', 'N', 'P', 'M', 'T', 'K3', 'G'])
        require(sum(c.abs2() for c in source.cells.values()) <= 1, 'Total source norm bound')
        require(all(rect(c) <= 1 for c in source.cells.values()), 'Rectangular cell norm bound')
        top = {w: source.output(w) for w in product(range(3), repeat=n)}
        lam = sum((top[(h,)*n] for h in range(3)), ZERO)/C(3)
        require(not lam.im and lam.re > 0, 'Chosen examples have positive rational pure average')
        ell = lam.re
        error = {w: value-(lam if len(set(w)) == 1 else ZERO) for w, value in top.items()}
        xi = sum((rect(c) for c in error.values()), F(0))
        x = xi/ell
        counts = dict(linear_response=0, pure_scalar_residual=0, binary_mixed_residual=0,
                      cubic_omission=0, cofactor_polarization=0, two_copy_rotation=0)
        roots = range(n) if n == 4 else [0]
        for root in roots:
            omega = tuple(i for i in range(n) if i != root)
            psi = {w: source.response(root, omega, w) for w in product(range(3), repeat=N)}
            for word, polynomial in psi.items():
                for h in range(3):
                    full_word = list(word)
                    full_word.insert(root, h)
                    key = tuple(int(j == h) for j in range(3))
                    require(polynomial.get(key, ZERO) == top[tuple(full_word)], 'Literal linear response')
                    counts['linear_response'] += 1
            high = {w: {e: c for e, c in p.items() if sum(e) >= 3} for w, p in psi.items()}
            g = {(0, 0, 0): ONE}
            for e, c in high[(0,)*N].items():
                if e[0]:
                    key = (e[0]-1, e[1], e[2])
                    g[key] = g.get(key, ZERO) + c/lam
            tail = add(g, {(0, 0, 0): -ONE})
            for h in range(3):
                residual = add(high[(h,)*N], scale(-lam, mul(var(h), tail)))
                require(norm(residual) <= M*x, 'Approximate common scalar on pure words')
                counts['pure_scalar_residual'] += 1
            for w, polynomial in high.items():
                if len(set(w)) == 2:
                    require(norm(polynomial) <= M*x, 'Binary mixed higher response')
                    counts['binary_mixed_residual'] += 1
            half = {e: c/C(2**(sum(e)//2)) for e, c in g.items()}
            residual = add(mul(half, half), scale(-1, g))
            require(norm(residual) <= T*xi/ell**3, 'General scalar scaling residual')
            require(not homogeneous(residual, 0) and not homogeneous(residual, 2),
                    'Scaling residual begins at degree four')
            rho2 = ell/(2*M)
            scaled = {e: c*rho2**(sum(e)//2) for e, c in g.items()}
            require(norm(add(scaled, {(0, 0, 0): -ONE})) <= F(1, 2), 'Auxiliary normalization')
            scaled_residual = {e: c*rho2**(sum(e)//2) for e, c in residual.items()}
            require(norm(scaled_residual) <= cs['Z']*x, 'Improved normalized residual budget')
            if x <= 1:
                for palette in [(0, 1), (0, 2), (1, 2)]:
                    observed = sum((norm(homogeneous(psi[w], 3))
                                    for w in product(palette, repeat=N)), F(0))
                    require((observed/K3)**m <= x, 'Cubic response norm bound')
            if full_rotation and root == 0:
                for palette in [(0, 1), (0, 2), (1, 2)]:
                    binary = {w: psi[w] for w in product(palette, repeat=N)}
                    original = pair({w: embed(p, 0) for w, p in binary.items()},
                                    {w: embed(p, 1) for w, p in binary.items()}, palette)
                    rotated = scale(F(1, 2), pair({w: rotate(p, 0, True) for w, p in binary.items()},
                                                   {w: rotate(p, 1, True) for w, p in binary.items()}, palette))
                    require(original == rotated, 'Universal full polynomial two-copy rotation')
                    counts['two_copy_rotation'] += 1
            for omitted in omega:
                core = tuple(v for v in omega if v != omitted)
                core_responses = {}
                def response(w):
                    if w not in core_responses:
                        core_responses[w] = source.response(root, core, w)
                    return core_responses[w]
                for h, k in product(range(3), repeat=2):
                    if h == k:
                        continue
                    palette = (k, h)
                    f, even2, b1, b3 = {}, {}, {}, {}
                    for w in product(palette, repeat=n-2):
                        ev = response(w)
                        f[w], even2[w] = homogeneous(ev, 0), homogeneous(ev, 2)
                        by_site = dict(zip(core, w))
                        by_site[omitted] = h
                        root_word = tuple(by_site[v] for v in omega)
                        b1[w] = homogeneous(psi[root_word], 1)
                        if w == (h,)*(n-2):
                            b1[w] = add(b1[w], scale(-lam, var(h)))
                        b3[w] = homogeneous(psi[root_word], 3)
                    lhs = scale(lam, mul(var(h), even2[(k,)*(n-2)]))
                    rhs = add(pair(f, b3, palette), scale(-1, pair(even2, b1, palette)))
                    require(lhs == rhs, 'Literal cubic omission identity')
                    counts['cubic_omission'] += 1
                for i, h in product(range(3), repeat=2):
                    observed = sum((source.edge(root, r, i, h)*source.cofactor(h, r, omitted)
                                    for r in range(n) if r != omitted), ZERO)
                    key = tuple(int(c == i)+int(c == h) for c in range(3))
                    target = response((h,)*(n-2)).get(key, ZERO)*(2 if i == h else 1)
                    require(observed == target, 'Cofactor polarization and factor two')
                    counts['cofactor_polarization'] += 1
                    if x <= 1:
                        require((rect(observed)*ell*n/G)**m <= x, 'Cofactor residual entry bound')
        inverse_condition = x <= 1 and x <= (ell*ell/(2*G))**m
        if inverse_condition:
            off_upper = sum((rect(v) for (p, q, i, j), v in source.cells.items() if i != j), F(0))
            require((off_upper*ell*ell/(8*G))**m <= x, 'Approximate diagonal reduction on an actual source')
        if name == 'allowed_four_site_with_tiny_off_color':
            require(inverse_condition, 'Positive test exercises the cofactor inverse regime')
        results.append({'case': name, 'sites': n, 'roots_checked': len(roots),
                        'pure_average': str(lam), 'error_coefficient_norm_upper_bound': str(xi),
                        'norm_convention': 'Exact |Re|+|Im| upper bounds; complex identities exact in Q(i).',
                        'checks': counts, 'inverse_condition_satisfied': inverse_condition})
    return results


def determinant_division_checks():
    first, second = (1, 0, 0, 0, 1, 0), (0, 1, 0, 1, 0, 0)
    determinant = {first: ONE, second: -ONE}
    def divide(p):
        remaining, quotient = dict(p), {}
        while remaining:
            lead = max(remaining)
            require(all(a >= b for a, b in zip(lead, first)), 'Exact determinant divisibility')
            exponent = tuple(a-b for a, b in zip(lead, first))
            value = remaining[lead]
            quotient[exponent] = quotient.get(exponent, ZERO)+value
            remaining = add(remaining, scale(-value, mul({exponent: ONE}, determinant)))
        return clean(quotient)
    cases = 0
    for D in range(1, 5):
        for degree in range(0, 4*D+1):
            # A whole coefficient chain, with both flat and oscillating controls.
            for mode in range(3):
                q = {}
                for j in range(degree//2+1):
                    e = (j, degree//2-j, 0, degree//2-j, j, degree % 2)
                    q[e] = C(1 if mode == 0 else (-1)**j,
                             F(j+1, 7) if mode == 2 else 0)
                r = mul(determinant, q)
                require(divide(r) == q, 'Exact finite binomial division')
                require(norm(q) <= (4*D+1)*norm(r), 'Coefficient division norm bound')
                cases += 1
    return {'cases': cases, 'maximum_quotient_degree': 16, 'complex_controls': True}


def general_rate_constants():
    prior = json.loads((PREVIOUS / 'results.json').read_text())
    for rel, expected in prior['sha256'].items():
        p = PREVIOUS / rel if rel == 'verify.py' else ROOT / 'notes' / rel
        require(hashlib.sha256(p.read_bytes()).hexdigest() == expected, 'Pinned diagonal dependency')
    out = []
    for row in prior['global_diagonal_rate_constants']:
        n = row['sites']
        cs = constants(n)
        m, D, P, G, L = (cs[k] for k in ['m', 'D', 'P', 'G', 'L'])
        cn = F(row['amplitude_lower_bound_c'])
        k = F(3)+F(3*D, 2)
        b = min(cn, F(1, 2*P**ceil(k-1)))
        q = m*(k+2)+1
        candidates = [F(1, 3**m*P**ceil(q-1)), (1/(6*G*P**ceil(k)))**m,
                      b/(4*P**ceil(q-k)), (b/(4*L))**m]
        c = min(candidates)
        require(q.denominator == 1, 'Integral amplitude exponent')
        require(1/(q-1) == F(8, n*(3*n+14)), 'General complex rate exponent')
        require(3**m*c*P**ceil(q-1) <= 1, 'Small coefficient error budget')
        require(c*(6*G*P**ceil(k))**m <= 1, 'Cofactor inverse budget')
        require(4*c*P**ceil(q-k) <= b, 'Original error budget after projection')
        require(c*(4*L)**m <= b**m, 'Projection error budget')
        require(2*b*P**ceil(k-1) <= 1, 'Projected fidelity budget')
        out.append({'sites': n, 'amplitude_power': str(q), 'rate_exponent': str(1/(q-1)),
                    'cubic_response_constant': str(cs['K3']), 'cofactor_constant_G': str(G),
                    'output_projection_constant_L': str(L), 'diagonal_constant_c': str(cn),
                    'general_constant_c': str(c), 'minimum_selected_term': candidates.index(c)+1,
                    'all_budget_inequalities_verified': True})
    return out


def palette_projection_checks():
    counts = 0
    for d in range(3, 13):
        for mode in range(3):
            values = [C(F((j+1)*(-1 if mode == 1 and j % 2 else 1), 7),
                        F((j*j+mode) % 5-2, 11)) for j in range(d)]
            mean = sum(values, ZERO)/C(d)
            means = []
            for subset in combinations(range(d), 3):
                local_mean = sum((values[j] for j in subset), ZERO)/C(3)
                means.append(local_mean)
                local_error = sum((values[j]-local_mean).abs2() for j in subset)
                old_error = sum((values[j]-mean).abs2() for j in subset)
                require(local_error + 3*(local_mean-mean).abs2() == old_error,
                        'Exact orthogonal projection of a three-color subset')
                counts += 1
            require(sum(means, ZERO)/C(len(means)) == mean, 'Average of all triple means')
            require(max(c.abs2() for c in means) >= mean.abs2(), 'A triple retains the target amplitude')
    return {'target_dimensions': list(range(3, 13)), 'subset_projection_checks': counts,
            'complex_pure_amplitudes': True}


def main():
    result = {'status': 'PASS',
              'scope': 'Supporting exact checks; arbitrary-size proof is in the research note. Not an independent audit.',
              'coefficient_division': determinant_division_checks(),
              'target_palette_projection': palette_projection_checks(),
              'literal_off_color_sources': literal_source_checks(),
              'general_complex_rate_constants': general_rate_constants()}
    dependencies = [HERE / 'verify.py', ROOT / 'notes/general-complex-rate-bound-2026-09-26.md',
                    PREVIOUS / 'verify.py', PREVIOUS / 'results.json',
                    ROOT / 'notes/quantitative-proof-identities-2026-09-26.md',
                    ROOT / 'proofs/krenn-gu-all-orders-two-replica-proof.md']
    result['sha256'] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in dependencies}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
