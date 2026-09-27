#!/usr/bin/env python3
"""Exact checks for quantitative polynomial rigidity and endpoint diagnostics.

Standard library only. No imported proof/checker code, numerical fitting, or
floating-point assertions. Run normally or with -O; require() remains active.
The arbitrary-size conclusions are proved in the accompanying research note.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import factorial
from pathlib import Path
import hashlib
import json


def require(condition, message):
    if not condition:
        raise AssertionError(message)


@dataclass(frozen=True, eq=False)
class C:
    """A Gaussian rational, with exact arithmetic in Q(i)."""
    re: F = F(0)
    im: F = F(0)

    def __post_init__(self):
        object.__setattr__(self, "re", F(self.re))
        object.__setattr__(self, "im", F(self.im))

    @staticmethod
    def cast(value):
        return value if isinstance(value, C) else C(value)

    def __add__(self, other):
        other = C.cast(other)
        return C(self.re + other.re, self.im + other.im)

    __radd__ = __add__

    def __neg__(self):
        return C(-self.re, -self.im)

    def __sub__(self, other):
        return self + (-C.cast(other))

    def __rsub__(self, other):
        return C.cast(other) - self

    def __mul__(self, other):
        other = C.cast(other)
        return C(self.re * other.re - self.im * other.im,
                 self.re * other.im + self.im * other.re)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = C.cast(other)
        den = other.abs2()
        return self * C(other.re / den, -other.im / den)

    def __pow__(self, exponent):
        if exponent < 0:
            return (C(1) / self) ** (-exponent)
        result, base = C(1), self
        while exponent:
            if exponent % 2:
                result = result * base
            base = base * base
            exponent //= 2
        return result

    def __bool__(self):
        return bool(self.re or self.im)

    def __eq__(self, other):
        other = C.cast(other)
        return self.re == other.re and self.im == other.im

    def abs2(self):
        return self.re * self.re + self.im * self.im

    def __str__(self):
        return str(self.re) if not self.im else f"({self.re})+({self.im})i"


ZERO, ONE, I = C(), C(1), C(0, 1)


def poly(values):
    values = list(map(C.cast, values)) or [ZERO]
    while len(values) > 1 and not values[-1]:
        values.pop()
    return tuple(values)


P0, P1 = poly([0]), poly([1])


def add(p, q):
    return poly((p[j] if j < len(p) else ZERO) +
                (q[j] if j < len(q) else ZERO)
                for j in range(max(len(p), len(q))))


def scale(c, p):
    return poly(C.cast(c) * x for x in p)


def sub(p, q):
    return add(p, scale(-1, q))


def mul(p, q):
    out = [ZERO] * (len(p) + len(q) - 1)
    for j, x in enumerate(p):
        for k, y in enumerate(q):
            out[j + k] = out[j + k] + x * y
    return poly(out)


def deriv(p):
    return poly(j * p[j] for j in range(1, len(p)))


def truncate(p, order):
    return poly(p[:order + 1])


def log_series(p, order):
    u = sub(p, P1)
    power, answer = P1, P0
    for j in range(1, order + 1):
        power = truncate(mul(power, u), order)
        answer = add(answer, scale(F((-1) ** (j + 1), j), power))
    return truncate(answer, order)


def exp_series(p, order):
    power, answer = P1, P1
    for j in range(1, order + 1):
        power = truncate(mul(power, p), order)
        answer = add(answer, scale(F(1, factorial(j)), power))
    return truncate(answer, order)


def norm1_real(p):
    require(all(not x.im for x in p), "Expected real rational coefficients")
    return sum(abs(x.re) for x in p)


def ode_inverse(r, d, degree):
    answer, current = P0, r
    for j in range(degree + 1):
        answer = add(answer, scale(C((-1) ** j) / d ** (j + 1), current))
        current = deriv(current)
    return answer


def ode_checks():
    count, sharp, functional = 0, 0, 0
    for degree in range(10):
        for d in [C(1), C(-2), C(F(1, 3)), C(1, 2)]:
            b = poly(C(F((-1) ** j * (j + 1), j + 2), F(j % 3, j + 3))
                     for j in range(degree + 1))
            r = add(deriv(b), scale(d, b))
            require(ode_inverse(r, d, degree) == b, "ODE inverse")
            cleared = P0
            current = r
            for j in range(degree + 1):
                cleared = add(cleared, scale((-1) ** j * d ** (degree - j), current))
                current = deriv(current)
            require(cleared == scale(d ** (degree + 1), b), "Cleared ODE certificate")
            count += 1
        for d in [C(F(1, 10)), C(1), C(3)]:
            r = poly([0] * degree + [1])
            b = ode_inverse(r, d, degree)
            sharp_norm = sum(F(factorial(degree), factorial(degree - j))
                             / abs(d.re) ** (j + 1) for j in range(degree + 1))
            require(norm1_real(b) == sharp_norm, "Sharp coefficient norm")
            sharp += 1
            endpoint_norm = max(F(factorial(j)) / abs(d.re) ** j
                                for j in range(degree + 1))
            require(endpoint_norm == max(F(1), F(factorial(degree)) / abs(d.re) ** degree),
                    "Sharp endpoint functional norm")
            functional += 1
    degree, d = 3, C(F(1, 100))
    b = poly((-d) ** j / C(factorial(j)) for j in range(degree + 1))
    r = add(deriv(b), scale(d, b))
    require(r == poly([0] * degree + [(-1) ** degree * d ** (degree + 1) / C(factorial(degree))]),
            "Small-edge negative control")
    return {
        "exact_complex_inverse_cases": count,
        "sharp_operator_norm_cases": sharp,
        "sharp_endpoint_functional_norm_cases": functional,
        "small_edge_control": {"degree": degree, "d": str(d),
                               "polynomial_norm": str(norm1_real(b)),
                               "residual_norm": str(norm1_real(r)),
                               "inverse_norm": str(norm1_real(b) / norm1_real(r))},
    }


def multivariate_scaling_checks():
    def plus(p, q):
        out = dict(p)
        for key, value in q.items():
            out[key] = out.get(key, ZERO) + value
        return {key: value for key, value in out.items() if value}

    def times(p, q):
        out = {}
        for a, x in p.items():
            for b, y in q.items():
                key = tuple(u + v for u, v in zip(a, b))
                out[key] = out.get(key, ZERO) + x * y
        return {key: value for key, value in out.items() if value}

    def scaled(c, p):
        return {key: C.cast(c) * value for key, value in p.items() if c * value}

    count = 0
    for degree in range(1, 5):
        for cross in [C(F(1, 100)), C(0, F(1, 100))]:
            q = {(2, 0): C(F(1, 100)), (1, 1): cross, (0, 2): C(F(-1, 100))}
            power = {(0, 0): ONE}
            g = dict(power)
            for j in range(1, degree + 1):
                power = times(power, q)
                g = plus(g, scaled(F(1, factorial(j)), power))
            gs = {key: value / C(2 ** (sum(key) // 2)) for key, value in g.items()}
            residual = plus(times(gs, gs), scaled(-1, g))
            require(all(sum(key) > 2 * degree for key in residual), "Multivariate low-degree cancellation")
            leading = {key: value for key, value in residual.items() if sum(key) == 2 * degree + 2}
            predicted = scaled((1 - F(1, 2 ** degree)) / factorial(degree + 1), times(power, q))
            require(leading == predicted, "Multivariate complex leading residual")
            count += 1
    return count


def scaling_checks():
    cases, logarithms, examples = 0, 0, []
    constant = F(64, 7)
    for degree in range(1, 9):
        for t in [F(1, 4), F(1, 10), F(1, 100)]:
            # u denotes the square of the original mean parameter.
            g = poly(t ** j / factorial(j) for j in range(degree + 1))
            gs = poly(x / C(2 ** j) for j, x in enumerate(g))
            r = sub(mul(gs, gs), g)
            require(r[:degree + 1] == (ZERO,) * (degree + 1), "Truncated exponential low terms")
            leading = (1 - F(1, 2 ** degree)) * t ** (degree + 1) / factorial(degree + 1)
            require(r[degree + 1] == leading, "Sharpness leading coefficient")
            epsilon = norm1_real(r)
            require(t ** (degree + 1) <= constant * factorial(degree + 1) * epsilon,
                    "Quadratic coefficient stability")
            cases += 1
            if degree in (1, 2, 3) and t == F(1, 100):
                examples.append({"half_degree": degree, "t": str(t),
                                 "response_distance": str(norm1_real(sub(g, P1))),
                                 "scaling_residual": str(epsilon),
                                 "optimal_holder_exponent": f"1/{degree + 1}"})
        # Signed coefficients, with norm(g-1) at most 1/4.
        g = poly([1] + [F((-1) ** j, 4 * degree * (j + 1)) for j in range(1, degree + 1)])
        order = degree + 1
        h = log_series(g, order)
        q = poly([0, g[1]])
        gs = poly(x / C(2 ** j) for j, x in enumerate(g))
        r = sub(mul(gs, gs), g)
        hs = poly(x / C(2 ** j) for j, x in enumerate(h))
        log_difference = sub(log_series(mul(gs, gs), order), h)
        require(log_difference == sub(scale(2, hs), h), "Formal logarithm/scaling identity")
        require(exp_series(h, order) == g, "Formal logarithm/exponential inverse")
        require(norm1_real(sub(h, q)) <= F(32, 7) * norm1_real(r), "Logarithm error bound")
        require(norm1_real(sub(g, exp_series(q, order))) <= constant * norm1_real(r),
                "Truncated exponential error bound")
        logarithms += 1
    return {"truncated_exponential_cases": cases, "signed_logarithm_cases": logarithms,
            "multivariate_real_and_complex_cases": multivariate_scaling_checks(),
            "constant": "64/7", "sharpness_examples": examples}


D0, D1 = (P0,) * 4, (P1, P0, P0, P0)


def dual_add(a, b):
    return tuple(add(x, y) for x, y in zip(a, b))


def dual_mul(a, b):
    return (mul(a[0], b[0]),
            add(mul(a[0], b[1]), mul(a[1], b[0])),
            add(mul(a[0], b[2]), mul(a[2], b[0])),
            add(add(mul(a[0], b[3]), mul(a[3], b[0])),
                add(mul(a[1], b[2]), mul(a[2], b[1]))))


def tensor(b, h, means, u=None, v=None):
    """Direct sums over partial matchings, with polynomial singleton weights.

    Dual coefficients give E, E_u, E_v, E_uv without differentiating any
    assumed source constraint. Each retained site is used exactly once.
    """
    n = len(b)
    u = u or [ZERO] * n
    v = v or [ZERO] * n
    answer = []
    for word in product((0, 1), repeat=n):
        @lru_cache(None)
        def rec(mask):
            if not mask:
                return D1
            i = (mask & -mask).bit_length() - 1
            rest = mask ^ (1 << i)
            mono = ((means[i], P0, P0, P0) if word[i] == 0 else
                    (P0, poly([u[i]]), poly([v[i]]), P0))
            total = dual_mul(mono, rec(rest))
            for j in range(i + 1, n):
                if rest & (1 << j) and word[i] == word[j]:
                    weight = b[i][j] if word[i] == 0 else h[i][j]
                    paired = tuple(scale(weight, p) for p in rec(rest ^ (1 << j)))
                    total = dual_add(total, paired)
            return total
        answer.append((word, rec((1 << n) - 1)))
    return tuple({w: values[j] for w, values in answer} for j in range(4))


def pairing(a, b):
    result = P0
    for word, p in a.items():
        sign = (-1) ** word.count(0)
        result = add(result, scale(sign, mul(p, b[tuple(1 - i for i in word)])))
    return result


def haf(matrix):
    @lru_cache(None)
    def rec(vertices):
        if not vertices:
            return ONE
        p, rest = vertices[0], vertices[1:]
        return sum((matrix[p][q] * rec(tuple(v for v in rest if v != q))
                    for q in rest), ZERO)
    return rec(tuple(range(len(matrix))))


def zero_matrix(n):
    return [[ZERO for _ in range(n)] for _ in range(n)]


def matrix(n, edges):
    out = zero_matrix(n)
    for p, q, weight in edges:
        out[p][q] = out[q][p] = C.cast(weight)
    return out


def diagnostic(b, h, p, q):
    n = len(b)
    keep = [v for v in range(n) if v not in (p, q)]
    cb = [[b[i][j] for j in keep] for i in keep]
    ch = [[h[i][j] for j in keep] for i in keep]
    x, y = [b[p][i] for i in keep], [b[q][i] for i in keep]
    u, v = [h[p][i] for i in keep], [h[q][i] for i in keep]
    d, e = b[p][q], h[p][q]
    first = tensor(cb, ch, [poly([xx, yy / C(2)]) for xx, yy in zip(x, y)], u, v)
    second = tensor(cb, ch, [poly([I * xx, -I * yy / C(2)]) for xx, yy in zip(x, y)], u, v)
    f = pairing(first[0], second[0])
    m11, m22 = pairing(first[3], second[0]), pairing(first[0], second[3])
    m12, m21 = pairing(first[1], second[2]), pairing(first[2], second[1])
    a = scale(F(1, 2), add(add(m11, m22), add(scale(2 * e, f), scale(-I, sub(m12, m21)))))
    degree = (n - 2) // 2
    require(len(a) - 1 <= degree, "Isotropic kernel degree bound")
    beta, eta, alpha = haf(b), haf(h), haf(cb)
    r = sub(add(deriv(a), scale(d, a)), poly([beta * eta]))
    zero = tensor(cb, ch, [P0] * len(keep), u, v)
    retained, uv = zero[0], zero[3]
    z0 = {w: add(uv[w], scale(e, retained[w])) for w in retained}
    origin = pairing(retained, z0)
    require(origin == poly([a[0]]), "Kernel origin evaluation")
    w = dict(z0)
    w[(1,) * len(keep)] = sub(w[(1,) * len(keep)], poly([eta]))
    origin_defect = a[0] - eta * alpha
    require(pairing(retained, w) == poly([origin_defect]), "Origin defect slice")
    norm_f2 = sum(values[0].abs2() for values in retained.values())
    norm_w2 = sum(values[0].abs2() for values in w.values())
    require(origin_defect.abs2() <= norm_f2 * norm_w2, "Origin Cauchy bound")
    core_norm2 = sum(cb[i][j].abs2() + ch[i][j].abs2()
                     for i in range(len(keep)) for j in range(i + 1, len(keep)))
    matching_count = factorial(2 * degree) // (2 ** degree * factorial(degree))
    require(norm_f2 <= matching_count ** 2 * (core_norm2 / degree) ** degree,
            "Explicit retained-tensor norm bound")

    # Compare the boundary tensor to the literal full-source HH output slice.
    top = tensor(b, h, [P0] * n)[0]
    for word, value in z0.items():
        full_word = [1] * n
        for i, color in zip(keep, word):
            full_word[i] = color
        require(value == top[tuple(full_word)], "Literal HH slice")
    rhs = sum(((-1) ** j * d ** (degree - j) * factorial(j)
               * (r[j] if j < len(r) else ZERO) for j in range(degree + 1)), ZERO)
    rhs = rhs - d ** (degree + 1) * origin_defect
    lhs = d ** degree * eta * (d * alpha - beta)
    require(lhs == rhs, "Cleared endpoint certificate")
    return {"sites": n, "root_pair": [p, q], "degree_bound": degree,
            "actual_degree": len(a) - 1, "d": str(d), "beta": str(beta), "eta": str(eta),
            "alpha": str(alpha), "kernel_coefficients": list(map(str, a)),
            "ode_residual_coefficients": list(map(str, r)),
            "origin_defect": str(origin_defect),
            "endpoint_defect_beta_minus_d_alpha": str(beta - d * alpha),
            "mixed_slice_norm_squared": str(norm_w2),
            "certificate_value": str(lhs)}


def kernel_checks():
    results = []
    b = matrix(4, [(0, 1, 2), (2, 3, 3)])
    h = matrix(4, [(0, 2, 5), (1, 3, 7)])
    for p, q in [(0, 1), (1, 0), (0, 2)]:
        result = diagnostic(b, h, p, q)
        require(result["ode_residual_coefficients"] == ["0"], "Allowed K4 residual")
        results.append({"case": "weighted_K4", **result})
    b = matrix(4, [(0, 2, 1), (0, 3, 1), (1, 2, 1), (1, 3, 1)])
    h = matrix(4, [(0, 1, 1), (2, 3, 1)])
    result = diagnostic(b, h, 0, 2)
    require(result["kernel_coefficients"] == ["1", "1"], "Binary control kernel 1+z")
    require(result["ode_residual_coefficients"] == ["0", "1"], "Binary control residual z")
    require(result["mixed_slice_norm_squared"] == "0", "Binary control exact pure top slice")
    require(result["endpoint_defect_beta_minus_d_alpha"] == "1", "Binary endpoint control")
    results.append({"case": "binary_only_negative_control", **result})
    for n in (4, 6, 8):
        b, h = zero_matrix(n), zero_matrix(n)
        for p in range(n):
            for q in range(p + 1, n):
                b[p][q] = b[q][p] = C(F(((p + 2) * (q + 3)) % 7 - 3, 3),
                                      F((p + q) % 3 - 1, 5))
                h[p][q] = h[q][p] = C(F(((p + 3) * (q + 1)) % 9 - 4, 4),
                                      F((p + 2 * q) % 3 - 1, 7))
        results.append({"case": "generic_complex", **diagnostic(b, h, 0, 1)})
        if n == 6:
            results.append({"case": "generic_complex_imaginary_edge", **diagnostic(b, h, 0, 2)})
        beta = haf(b)
        for p in range(n):
            defects = []
            for q in range(n):
                if not b[p][q]:
                    continue
                keep = [v for v in range(n) if v not in (p, q)]
                minor = [[b[i][j] for j in keep] for i in keep]
                defects.append(beta - b[p][q] * haf(minor))
            require(sum(defects, ZERO) == (len(defects) - 1) * beta, "Degree-counting identity")
            if len(defects) >= 2:
                require(max(x.abs2() for x in defects) >=
                        F((len(defects) - 1) ** 2, len(defects) ** 2) * beta.abs2(),
                        "Quantitative degree-counting bound")
    return results


def root_response_checks():
    """Independent three-color partial-matchings check of physical error bounds."""
    cases = []
    for n in (4, 6):
        colors = [matrix(n, [(i, j, F(((i + 2*c + 2)*(j + c + 3)) % 11 - 5, 6))
                             for i in range(n) for j in range(i + 1, n)])
                  for c in range(3)]
        cases.append((f"signed_diagonal_{n}", colors))
    t = F(1, 10)
    colors = [matrix(6, edges) for edges in [
        [(0, 1, 1), (3, 4, 1), (2, 5, t), (0, 2, t*t)],
        [(1, 2, 1), (4, 5, 1), (0, 3, t)],
        [(0, 2, 1), (3, 5, 1), (1, 4, t)],
    ]]
    cases.append(("perturbed_prism", colors))
    results = []
    for name, colors in cases:
        n, origin = len(colors[0]), (0, 0, 0)
        N = n - 1
        values = [[[entry.re for entry in row] for row in color] for color in colors]
        require(all(not entry.im and entry.abs2() <= 1
                    for color in colors for row in color for entry in row),
                "Root-response edge bound")

        @lru_cache(None)
        def full(word, mask):
            if not mask:
                return F(1)
            i = (mask & -mask).bit_length() - 1
            rest = mask ^ (1 << i)
            return sum(values[word[i]][i][j] * full(word, rest ^ (1 << j))
                       for j in range(i + 1, n)
                       if rest & (1 << j) and word[i] == word[j])

        top = {w: full(w, (1 << n) - 1) for w in product(range(3), repeat=n)}
        amplitudes = [top[(c,) * n] for c in range(3)]
        tau = min(abs(x) for x in amplitudes)
        require(tau > 0, "Nonzero three-color pure amplitudes")
        xi = sum(abs(value) for word, value in top.items() if len(set(word)) > 1)
        inv0, inv1 = 1, 1
        for j in range(2, N + 1):
            inv0, inv1 = inv1, inv1 + (j - 1) * inv0
        involutions = inv1
        bound = involutions * xi / tau
        responses = {}
        worst, checked, absolute_partial_bound = F(0), 0, F(0)
        for word in product(range(3), repeat=N):
            @lru_cache(None)
            def rec(mask):
                if not mask:
                    return {origin: F(1)}
                i = (mask & -mask).bit_length() - 1
                rest = mask ^ (1 << i)
                out = {}
                for exponent, value in rec(rest).items():
                    shifted = list(exponent)
                    shifted[word[i]] += 1
                    key = tuple(shifted)
                    out[key] = out.get(key, F(0)) + values[word[i]][0][i+1] * value
                for j in range(i + 1, N):
                    if rest & (1 << j) and word[i] == word[j]:
                        weight = values[word[i]][i+1][j+1]
                        for key, value in rec(rest ^ (1 << j)).items():
                            out[key] = out.get(key, F(0)) + weight * value
                return {key: value for key, value in out.items() if value}
            response = rec((1 << N) - 1)
            responses[word] = response
            @lru_cache(None)
            def absolute_by_singletons(mask):
                if not mask:
                    return (F(1),) + (F(0),) * N
                i = (mask & -mask).bit_length() - 1
                rest = mask ^ (1 << i)
                tail = absolute_by_singletons(rest)
                out = [F(0)] + [abs(values[word[i]][0][i+1]) * tail[k-1]
                                for k in range(1, N+1)]
                for j in range(i + 1, N):
                    if rest & (1 << j) and word[i] == word[j]:
                        weight = abs(values[word[i]][i+1][j+1])
                        paired = absolute_by_singletons(rest ^ (1 << j))
                        out = [a + weight * b for a, b in zip(out, paired)]
                return tuple(out)
            absolute_partial_bound = max(
                absolute_partial_bound, sum(absolute_by_singletons((1 << N)-1)[3:]))
            for c in range(3):
                exponent = tuple(int(j == c) for j in range(3))
                require(response.get(exponent, F(0)) == top[(c,) + word],
                        "Linear response is literal full output")
            high_norm = sum(abs(value) for exponent, value in response.items()
                            if sum(exponent) >= 3)
            if len(set(word)) <= 2:
                require(high_norm <= bound, "Physical-to-higher-response bound")
                worst = max(worst, high_norm)
                checked += 1
        specific_bound = absolute_partial_bound * xi / tau
        require(worst <= specific_bound, "Source-specific higher-response bound")
        require(absolute_partial_bound <= involutions, "Partial matching count bound")
        boundary_checks = 0
        boundary_bound = xi * (1 + F(2 ** (n - 2) * involutions, 1) / tau)
        for palette in [(0, 1), (0, 2), (1, 2)]:
            for omitted in range(N):
                for color_at_q in palette:
                    residual_norm = F(0)
                    for word, response in responses.items():
                        if word[omitted] != color_at_q or not set(word).issubset(palette):
                            continue
                        residual = dict(response)
                        if len(set(word)) == 1:
                            c = word[0]
                            key = tuple(int(j == c) for j in range(3))
                            residual[key] = residual.get(key, F(0)) - amplitudes[c]
                        residual_norm += sum(abs(value) for exponent, value in residual.items()
                                             if all(exponent[j] == 0 for j in range(3) if j not in palette))
                    require(residual_norm <= boundary_bound, "Physical-to-root-boundary bound")
                    boundary_checks += 1
        results.append({"case": name, "sites": n, "pure_amplitudes": list(map(str, amplitudes)),
                        "mixed_output_coefficient_norm": str(xi),
                        "minimum_pure_amplitude": str(tau), "partial_matching_count": involutions,
                        "binary_word_checks": checked, "root_boundary_checks": boundary_checks,
                        "largest_binary_higher_response_norm": str(worst),
                        "absolute_partial_matching_bound": str(absolute_partial_bound),
                        "per_word_source_specific_bound": str(specific_bound),
                        "per_word_upper_bound": str(bound)})
    return results


def covariance_projection_checks():
    """Exact right inverses for the axis map on every covariant generator.

    Variables are P1,P2,Q1,Q2. O(2) covariance is spanned by I, PP^T,
    QQ^T, PQ^T, QP^T times monomials in sigma,rho,z. The projection
    reproduces both axis restrictions; its remainder has the exact
    special matrix form. The norm certificate is computed on the full
    coefficient operator, not estimated by random sampling.
    """
    unit = (0, 0, 0, 0)
    basis = [tuple(int(i == j) for i in range(4)) for j in range(4)]

    def plus(p, q):
        out = dict(p)
        for key, value in q.items():
            out[key] = out.get(key, F(0)) + value
        return {key: value for key, value in out.items() if value}

    def times(p, q):
        out = {}
        for a, x in p.items():
            for b, y in q.items():
                key = tuple(u + v for u, v in zip(a, b))
                out[key] = out.get(key, F(0)) + x*y
        return out

    variables = [{key: F(1)} for key in basis]
    sigma = plus(times(variables[0], variables[0]), times(variables[1], variables[1]))
    rho = plus(times(variables[2], variables[2]), times(variables[3], variables[3]))
    z = plus(times(variables[0], variables[2]), times(variables[1], variables[3]))

    def gram(a, b, c):
        out = {unit: F(1)}
        for base, power in [(sigma, a), (rho, b), (z, c)]:
            for _ in range(power):
                out = times(out, base)
        return out

    def indices(degree):
        for total in range(degree + 1):
            for a in range(total + 1):
                for b in range(total - a + 1):
                    yield a, b, total - a - b

    def axis(col):
        out = {}
        for (i, j, exp), value in col.items():
            if (i, j) != (0, 1):
                continue
            if exp[0] == 0:
                out[(0, exp[1:])] = value
            if exp[3] == 0:
                out[(1, exp[:3])] = value
        return out

    def invert(a):
        size = len(a)
        rows = [list(row) + [F(int(i == j)) for j in range(size)]
                for i, row in enumerate(a)]
        for j in range(size):
            p = next(i for i in range(j, size) if rows[i][j])
            rows[j], rows[p] = rows[p], rows[j]
            scale_factor = rows[j][j]
            rows[j] = [x / scale_factor for x in rows[j]]
            for i in range(size):
                if i != j and rows[i][j]:
                    scale_factor = rows[i][j]
                    rows[i] = [x - scale_factor*y for x, y in zip(rows[i], rows[j])]
        return [row[size:] for row in rows]

    def scalar_of(col):
        signs = {(0, 0): ONE, (1, 1): ONE, (0, 1): -I, (1, 0): I}
        out = P0
        for (i, j, exp), value in col.items():
            power = exp[2] + exp[3]
            coefficient = (C(value) * signs[i, j] * I ** exp[1] * (-I) ** exp[3]
                           / C(2 ** (power + 1)))
            out = add(out, poly([0] * power + [coefficient]))
        return out

    def axis_ode(col, entry, d, target=F(0)):
        out = {}
        for (i, j, exp), value in col.items():
            if (i, j) != entry:
                continue
            if exp[2] == 1:
                key = (exp[0], exp[1], exp[3])
                out[key] = out.get(key, F(0)) + value
            if exp[2] == 0:
                key = (exp[0] + 1, exp[1], exp[3])
                out[key] = out.get(key, F(0)) + d*value
        if target:
            out[(1, 0, 0)] = out.get((1, 0, 0), F(0)) - target
        return {key: value for key, value in out.items() if value}

    def extract_ode(col, d, target=F(0)):
        r3, r4 = axis_ode(col, (0, 1), d), axis_ode(col, (1, 1), d, target)
        answer = P0
        for residual, shift, sign in [(r3, 0, ONE), (r4, 1, -ONE)]:
            for (a, b, c), value in residual.items():
                if a + b + 1 == c + 2:
                    answer = add(answer, poly([0] * c + [sign * I ** (a + shift) * value]))
        return answer

    results = []
    for degree in range(1, 5):
        columns = []
        for powers in indices(degree):
            scalar = gram(*powers)
            columns.append({(i, i, exp): value for i in range(2) for exp, value in scalar.items()})
        for left, right in [(0, 0), (2, 2), (0, 2), (2, 0)]:
            for powers in indices(degree - 1):
                scalar = gram(*powers)
                columns.append({(i, j, exp): value for i in range(2) for j in range(2)
                                for exp, value in times(scalar,
                                  times(variables[left+i], variables[right+j])).items()})
        axes = list(map(axis, columns))
        pivots, selected, selected_rows = [], [], []
        for index, col in enumerate(axes):
            remainder = dict(col)
            for pivot, reduced in pivots:
                factor = remainder.get(pivot, F(0))
                if factor:
                    remainder = plus(remainder, {key: -factor*value for key, value in reduced.items()})
            if remainder:
                pivot = min(remainder)
                factor = remainder[pivot]
                reduced = {key: value / factor for key, value in remainder.items()}
                pivots.append((pivot, reduced))
                selected.append(index)
                selected_rows.append(pivot)
        matrix_a = [[axes[j].get(key, F(0)) for j in selected] for key in selected_rows]
        inverse = invert(matrix_a)
        projection_columns = []
        for j in range(len(selected)):
            out = {}
            for k, index in enumerate(selected):
                factor = inverse[k][j]
                if factor:
                    out = plus(out, {key: factor*value for key, value in columns[index].items()})
            projection_columns.append(out)
        norm = max(sum(abs(value) for value in col.values()) for col in projection_columns)
        for col, measured in zip(columns, axes):
            correction = {}
            for key, proj in zip(selected_rows, projection_columns):
                factor = measured.get(key, F(0))
                if factor:
                    correction = plus(correction, {row: factor*value for row, value in proj.items()})
            require(axis(correction) == measured, "Axis projection on every covariant generator")
            remainder = plus(col, {key: -value for key, value in correction.items()})
            a = scalar_of(remainder)
            require(len(a)-1 <= degree, "Invariant scalar degree on full generator basis")
            # All expressions are affine in d, so 0 and 1 check the
            # coefficient identity for every complex d, not only samples.
            for d in (F(0), F(1)):
                require(extract_ode(remainder, d) == add(deriv(a), scale(d, a)),
                        "Scalar ODE extraction on the whole covariant generator space")
        require(extract_ode({}, F(1), F(1)) == poly([-1]), "Target constant in ODE extraction")
        R = 3 * (degree * (degree + 1) * (degree + 2) // 6)
        general_bound = 4 * factorial(R) * 2 ** ((degree - 1) * R)
        require(norm <= general_bound, "General finite projection bound")
        results.append({"half_degree_D": degree, "sites": 2*degree + 2,
                        "covariant_generator_count": len(columns), "axis_rank": len(selected),
                        "certified_projection_norm": str(norm),
                        "scalar_ode_extraction_verified": True,
                        "all_generator_identities_verified": True})
    return results


def diagonal_rate_constants(projections):
    results = []
    for row in projections:
        D = row["half_degree_D"]
        if D < 2:
            continue
        n, m, N = 2*D + 2, D + 1, 2*D
        def involutions(size):
            a, b = 1, 1
            for j in range(2, size + 1):
                a, b = b, b + (j-1)*a
            return b
        P = factorial(n) // (2 ** m * factorial(m))
        Pcore = factorial(N) // (2 ** D * factorial(D))
        Cproj = F(row["certified_projection_norm"])
        W = 4 ** N * involutions(N)
        B = W * (N*N + 1 + N*(D+5)*Cproj)
        A = 2 ** (n-2) * involutions(n-1)
        K = B * 3 ** m * (P + 2*A)
        endpoint_constant = 2 * (K * factorial(D) + Pcore * P)
        c = F(1) / (256 * (1 + endpoint_constant) * (64*P*P) ** D)
        power = F(3) + F(3*D, 2)
        exponent = 1 / (power - 1)
        require(exponent == F(4, 3*n+2), "Global diagonal rate exponent")
        require(endpoint_constant * c * (64*P*P) ** D <= F(1, 256),
                "Heavy-edge endpoint error budget")
        require(c * P ** (2*D) <= F(1, 256), "Mixed-output contradiction budget")
        for lam in [F(1, 10000), F(1, 100), F(1), F(P)]:
            cutoff_squared = lam ** 3 / (64*P*P) ** 2
            require(P*P*cutoff_squared <= lam*lam/F(64*64), "Small-edge expansion budget")
            require(P*cutoff_squared <= lam/F(4096), "Pure heavy-matching amplitude budget")
            require(P*cutoff_squared <= lam**3/F(4096), "Mixed light-matching cancellation budget")
        results.append({"sites": n, "covariance_projection_C": str(Cproj),
                        "boundary_to_kernel_B": str(B), "endpoint_constant": str(endpoint_constant),
                        "amplitude_power": str(power), "amplitude_lower_bound_c": str(c),
                        "rate_exponent": str(exponent), "fidelity_floor": "12/13",
                        "scope": "All diagonal complex three-color sources; no minimum edge-weight assumption."})
    return results


def main():
    projections = covariance_projection_checks()
    result = {"status": "PASS", "scope": "Supporting exact checks; analytic proofs are in the research note.",
              "finite_ode": ode_checks(), "finite_scaling": scaling_checks(),
              "literal_source_endpoint_diagnostics": kernel_checks(),
              "physical_to_diagonal_response": root_response_checks(),
              "finite_covariance_projections": projections,
              "global_diagonal_rate_constants": diagonal_rate_constants(projections)}
    here = Path(__file__).resolve()
    note = here.parents[2] / "notes/quantitative-proof-identities-2026-09-26.md"
    result["sha256"] = {"verify.py": hashlib.sha256(here.read_bytes()).hexdigest()}
    if note.exists():
        result["sha256"][note.name] = hashlib.sha256(note.read_bytes()).hexdigest()
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
