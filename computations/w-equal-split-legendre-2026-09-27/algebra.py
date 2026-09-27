"""Exact polynomial checks for the equal-split W cancellation theorem."""

from fractions import Fraction as Q
from functools import lru_cache
from math import comb, factorial, prod


def require(condition, message):
    if not condition:
        raise ValueError(message)


def trim(p):
    p = list(map(Q, p))
    while len(p) > 1 and not p[-1]:
        p.pop()
    return p or [Q(0)]


def add(p, q):
    return trim([(p[i] if i < len(p) else 0)
                 + (q[i] if i < len(q) else 0)
                 for i in range(max(len(p), len(q)))])


def scale(p, c):
    return trim([c * a for a in p])


def mul(p, q):
    out = [Q(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return trim(out)


def power(p, n):
    out = [Q(1)]
    for _ in range(n):
        out = mul(out, p)
    return out


def derivative(p):
    return trim([i * p[i] for i in range(1, len(p))])


def value(p, x):
    out = Q(0)
    for a in reversed(p):
        out = out * x + a
    return out


def remainder(p, q):
    p, q = trim(p), trim(q)
    require(q != [Q(0)], "Nonzero polynomial divisor")
    while len(p) >= len(q) and p != [Q(0)]:
        shift = len(p) - len(q)
        p = add(p, [Q(0)] * shift + scale(q, -p[-1] / q[-1]))
    return p


def even_variable(p):
    require(all(not p[i] for i in range(1, len(p), 2)),
            "Polynomial is even")
    return trim(p[::2])


def legendre(m):
    """Rodrigues coefficients, independently of the recurrence below."""
    out = [Q(0)] * (m + 1)
    for j in range(m // 2 + 1):
        out[m - 2*j] = Q(
            (-1)**j * factorial(2*m - 2*j),
            2**m * factorial(j) * factorial(m-j) * factorial(m-2*j))
    return trim(out)


def kernel(m):
    out = [Q(0)]
    for j in range(m):
        out = add(out, scale(power(legendre(j), 2), Q(2*j+1, 2)))
    return out


def root_polynomial(m):
    return even_variable(legendre(m)[m % 2:])


def odd_double(k):
    return prod(range(1, k + 1, 2))


def star_cost(m):
    n = 2*m - 1
    return Q((n*(m-1))**(m-1) * (n*n+1),
             n * odd_double(2*m-3)**2)


def cost_factor(m):
    return Q(m**(m+1), (m-1)*factorial(m-2)**2)


def lower_cost(m):
    return Q(2*m**(m-1)*(m-1)**(m-3), factorial(m-2)**2)


def tail_ratio(m):
    return Q(2*m**(m-1)*odd_double(2*m-3)**2,
             factorial(m-1)**2*(2*m-1)**(m-2)*((2*m-1)**2+1))


@lru_cache(None)
def group_haf(p, q):
    """Enumerate matching monomials by expanding at one labeled vertex."""
    if p < 0 or q < 0 or (p+q) % 2:
        return {}
    if p == q == 0:
        return {(0, 0, 0): 1}
    choices = ([(p-1, (1, 0, 0), p-2, q),
                (q, (0, 0, 1), p-1, q-1)] if p else
               [(q-1, (0, 1, 0), 0, q-2)])
    out = {}
    for count, edge, r, s in choices:
        if count <= 0:
            continue
        for powers, coefficient in group_haf(r, s).items():
            key = tuple(a+b for a, b in zip(powers, edge))
            out[key] = out.get(key, 0) + count*coefficient
    return out


def multi_derivative(p, variable):
    out = {}
    for powers, coefficient in p.items():
        exponent = powers[variable]
        if exponent:
            key = list(powers)
            key[variable] -= 1
            out[tuple(key)] = coefficient * exponent
    return out


def check_matching_counts():
    for m in range(2, 13):
        counted = group_haf(m, m)
        formula = {}
        for j in range(m//2 + 1):
            c = Q(factorial(m)**2,
                  factorial(m-2*j)*4**j*factorial(j)**2)
            require(c.denominator == 1, "Integral matching count")
            formula[(j, j, m-2*j)] = int(c)
        require(counted == formula, f"Matching polynomial m={m}")
        for variable, minor, count in (
                (0, group_haf(m-2, m), comb(m, 2)),
                (1, group_haf(m, m-2), comb(m, 2)),
                (2, group_haf(m-1, m-1), m*m)):
            require(multi_derivative(counted, variable)
                    == {k: count*v for k, v in minor.items()},
                    f"Individual cofactor polynomial m={m}, variable={variable}")
    return {"half_sizes": [2, 12], "cofactor_classes_per_size": 3}


def check_classical_identities():
    for m in range(17):
        p = legendre(m)
        laplace = [Q(0)]
        for j in range(m//2 + 1):
            term = [Q(0)]*(m-2*j) + power([-1, 0, 1], j)
            laplace = add(laplace, scale(
                term, Q(factorial(m), factorial(m-2*j)*4**j*factorial(j)**2)))
        require(p == laplace, f"Integral expansion m={m}")
        require(value(p, 1) == 1, f"Endpoint normalization m={m}")
        for k in range(m):
            integral = sum(Q(2)*a/Q(i+k+1)
                           for i, a in enumerate(p) if (i+k) % 2 == 0)
            require(integral == 0, f"Orthogonality m={m}, monomial={k}")
        if not m:
            continue
        prev = legendre(m-1)
        recurrence = add(scale(mul([0, 1], p), 2*m+1),
                         scale(prev, -m))
        require(recurrence == scale(legendre(m+1), m+1),
                f"Three-term recurrence m={m}")
        require(mul([1, 0, -1], derivative(p))
                == scale(add(prev, scale(mul([0, 1], p), -1)), m),
                f"Derivative recurrence m={m}")
        cd = scale(add(mul(derivative(p), prev),
                       scale(mul(p, derivative(prev)), -1)), m)
        require(scale(kernel(m), 2) == cd,
                f"Christoffel-Darboux identity m={m}")
        derivative_weight = mul([1, 0, -1], power(derivative(p), 2))
        require(remainder(add(scale(kernel(m), 2),
                              scale(derivative_weight, -1)), p) == [Q(0)],
                f"Quadrature weight identity at roots m={m}")
    return {"degrees": [0, 16], "arithmetic": "Fractions only"}


def check_cost_identity():
    for m in range(2, 13):
        # Read L from the independently counted cofactor polynomial:
        # C_A = b*L(ab), and substitute ab=-k.
        within = group_haf(m-2, m)
        coefficients = {}
        for (a, b, c), number in within.items():
            require(b == a+1 and c == m-2-2*a, "Internal cofactor monomial")
            coefficients[a] = Q(number * (-1)**a)
        d = m//2-1
        ell = [coefficients.get(j, Q(0)) for j in range(d+1)]
        # Ltilde(y) = y^d L((1-y)/y).
        transformed = [Q(0)]
        for j, coefficient in enumerate(ell):
            transformed = add(transformed, scale(
                [Q(0)]*(d-j) + power([1, -1], j), coefficient))
        lhs = scale(even_variable(kernel(m)), 2*factorial(m-2)**2)
        if not m % 2:
            lhs = [Q(0)] + lhs
        rhs = mul([1, -1], power(transformed, 2))
        require(remainder(add(lhs, scale(rhs, -1)), root_polynomial(m)) == [Q(0)],
                f"Counted-cofactor versus kernel cost m={m}")
        if m % 2:
            disc = Q(2*(m*(m-1))**(m-1), odd_double(m-2)**4)
            at_zero = cost_factor(m)*Q((m-1)**(m-2))/value(kernel(m), 0)
            require(disc == at_zero, f"Disconnected zero-root cost m={m}")
    return {"half_sizes": [2, 12], "method": "Polynomial remainder at every positive root"}


# Polynomials below are in y; all denominators are positive.
REMAINDERS = {
    3: ([0], 1),
    4: ([105829, -14765], 280),
    5: ([15158361426, 3212873471], 2857680),
    6: ([35532440345, 43983028502, -18859616167], 758912),
    7: ([324694581459728736, 450239037543590565,
         -123689938153268938], 757954454400),
}


def check_finite_degrees():
    rows = []
    for m, (coefficients, denominator) in REMAINDERS.items():
        h = add(scale(power([m-1, 1], m-2), cost_factor(m)),
                scale(even_variable(kernel(m)), -Q(81, 80)*star_cost(m)))
        actual = remainder(h, root_polynomial(m))
        expected = scale(coefficients, Q(1, denominator))
        require(actual == expected, f"Finite-degree certificate m={m}")
        if m == 3:
            require(actual == [Q(0)], "Six-site scalar equality")
            require(value(root_polynomial(m), Q(3, 5)) == 0, "Six-site root")
            cost = cost_factor(m)*Q(2+Q(3, 5)) / value(even_variable(kernel(m)), Q(3, 5))
            require(cost == Q(117, 2), "Six-site cost")
        elif len(actual) == 2:
            # A linear polynomial lies between its endpoint values.
            require(value(actual, 0) > 0 and value(actual, 1) > 0,
                    f"Positive linear remainder on [0,1], m={m}")
        else:
            # a+b*y-c*y^2 = a+(b-c)*y+c*y*(1-y).
            a, b, negative_c = actual
            require(a > 0 and b+negative_c > 0 and negative_c < 0,
                    f"Positive quadratic remainder on [0,1], m={m}")
        row = {"m": m, "remainder": list(map(str, actual))}
        if m % 2:
            disc_ratio = Q(2*(m*(m-1))**(m-1), odd_double(m-2)**4)/star_cost(m)
            require(disc_ratio > Q(81, 80), f"Disconnected finite degree m={m}")
            row["disconnected_cost_ratio"] = str(disc_ratio)
        rows.append(row)
    return rows


def check_tail():
    for m in range(3, 41):
        q = tail_ratio(m)
        require(q == lower_cost(m)/star_cost(m), f"Tail normalization m={m}")
        ratio = (Q(2*m+1, m) * (1-Q(1, m*(2*m+1)))**m
                 * Q(2*m*m-2*m+1, 2*m*m+2*m+1))
        require(tail_ratio(m+1)/q == ratio, f"Tail ratio identity m={m}")
    base = tail_ratio(8)
    require(base == Q(167518208, 143015625) and base > Q(7, 6) > Q(81, 80),
            "Exact infinite-tail base case")
    # This coefficient identity, together with Bernoulli's inequality,
    # proves the induction for ALL m=8+h, h>=0, in the written argument.
    shifted = add(add(scale(power([8, 1], 2), 2), scale([8, 1], -14)), [1])
    require(shifted == list(map(Q, [17, 18, 2])) and all(a > 0 for a in shifted),
            "Positive all-size tail polynomial")
    return {"base_half_size": 8, "Q8": str(base),
            "ratio_lower_bound": "3/2", "positive_shifted_coefficients": [17, 18, 2],
            "finite_ratio_identity_checks": [3, 40],
            "all_size_argument": "Written Bernoulli induction; not a finite extrapolation"}


def check_imbalance_formula():
    count = 0
    for m in range(3, 13):
        for k in (Q(1, 4), Q(2, 3), Q(1), Q(2), Q(10)):
            d = Q(m-1, m)*k*k
            for t in (Q(1, 4), Q(1), Q(3)):
                u, v = k*t, k/t
                z = u+v
                rows = Q(m, m-1)*(1/(u+d)+1/(v+d))
                combined = Q(m, m-1)*(z+2*d)/(k*k+d*z+d*d)
                require(rows == combined, "Combined reciprocal row formula, L=1")
                log_derivative = (Q(m-1)/(z+Q(2*m, m-1))
                                  +1/(z+2*d)-d/(k*k+d*z+d*d))
                combined_derivative = (Q(m-1)/(z+Q(2*m, m-1))
                    +(k*k-d*d)/((z+2*d)*(k*k+d*z+d*d)))
                require(log_derivative == combined_derivative and log_derivative > 0,
                        "Imbalance algebra sample; all-parameter proof is written")
                count += 1
    return {"exact_formula_examples": count,
            "general_monotonicity": "Written two-case inequality for all m>=3, k>0"}


def check():
    return dict(matching_counts=check_matching_counts(),
                classical_identities=check_classical_identities(),
                cost_identity=check_cost_identity(),
                finite_degrees=check_finite_degrees(),
                tail=check_tail(),
                imbalance=check_imbalance_formula())
