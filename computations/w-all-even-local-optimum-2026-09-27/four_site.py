"""Exact higher-output obstructions for the exceptional four-site tangent modes."""

from fractions import Fraction as Q
from itertools import combinations, product
from derivatives import require
from exact import E, ZERO, ONE, OMEGA, cell, outputs, matchings


def plus(*polys):
    result = {}
    for p in polys:
        for key, value in p.items():
            result[key] = result.get(key, Q(0))+value
    return {k: v for k, v in result.items() if v}


def scale(p, a):
    return {k: a*v for k, v in p.items() if a*v}


def times(p, q):
    result = {}
    for a, x in p.items():
        for b, y in q.items():
            key = tuple(i+j for i, j in zip(a, b))
            result[key] = result.get(key, Q(0))+x*y
    return {k: v for k, v in result.items() if v}


def formal_identities():
    x, y, tau = [{tuple(int(j == i) for j in range(3)): Q(1)} for i in range(3)]
    s = [x, y, scale(plus(x, y), -1)]
    K = {(0, 1): tau, (1, 2): tau, (2, 0): tau}
    K.update({(j, i): scale(p, -1) for (i, j), p in list(K.items())})
    U = {(i, j): plus(scale(s[i], Q(2, 3)), scale(s[j], Q(1, 3)), K[i, j])
         for i in range(3) for j in range(3) if i != j}
    Y = {(i, j): plus(times(s[i], U[j, k]), times(s[j], U[i, k]))
         for i, j in combinations(range(3), 2) for k in range(3) if k not in (i, j)}
    quadratic = plus(*Y.values(), *(times(z, z) for z in s))
    cubic = plus(*(times(s[k], p) for (i, j), p in Y.items()
                   for k in range(3) if k not in (i, j)),
                 scale(times(times(s[0], s[1]), s[2]), -3))
    require(not quadratic, "Sum of induced bb entries equals minus sum of row squares")
    require(not cubic, "All-excited obstruction is three times the row product")
    return dict(quadratic_remainder_terms=len(quadratic), cubic_remainder_terms=len(cubic))


def jet_coefficient(jets, order):
    result = {}
    for word in product(range(2), repeat=4):
        value = ZERO
        for matching in matchings(tuple(range(4))):
            (i, j), (k, l) = matching
            for p in range(len(jets)):
                q = order-p
                if 0 <= q < len(jets):
                    value += jets[p].get((i, j, word[i], word[j]), ZERO)*jets[q].get(
                        (k, l, word[k], word[l]), ZERO)
        if value:
            result[word] = value
    return result


def check(data):
    identities = formal_identities()
    require(data["N"] == 3, "Four-site certificate uses the four-site derivatives")
    base = {key: E(z) for key, z in zip(data["cells"], data["base"]) if z}
    s = {1: ONE, 2: OMEGA, 3: OMEGA*OMEGA}
    T = {}
    for i in range(1, 4):
        T[0, i, 0, 0] = -3*s[i].conjugate()
        T[0, i, 1, 1] = -s[i]
        for j in range(1, 4):
            if i != j:
                T[cell(i, j, 1, 0)] = (2*s[i]+s[j])/3
    require(not jet_coefficient([base, T], 1), "The negative direction is in the full linear kernel")
    v = [T.get(key, ZERO) for key in data["cells"]]
    metric_norm = sum(g*z.abs2() for g, z in zip(data["metric"], v))
    B = sum((2*b*v[i]*v[j] for (i, j), b in data["hessian"].items()), ZERO)
    lagrangian = metric_norm-(B.a-B.b/2)
    require(lagrangian == -4, "A negative complex tangent direction really exists")
    second = outputs(T, n=4, colors=2)
    V = {}
    for i, j in combinations(range(1, 4), 2):
        word = tuple(int(k in (0, i, j)) for k in range(4))
        V[i, j, 1, 1] = -second.get(word, ZERO)
    for i in range(1, 4):
        word = tuple(int(k == i) for k in range(4))
        V[0, i, 0, 1] = -second.get(word, ZERO)
    require(not jet_coefficient([base, T, V], 2), "This direction can cancel all second-order outputs")
    third = jet_coefficient([base, T, V], 3)
    require(third.get((1, 1, 1, 1), ZERO) == E(-3),
            "A nonzero cubic all-excited obstruction remains")
    require((1, 1, 1, 1) not in data["jacobian"],
            "No third source jet can change that output at first order")
    return dict(symbolic_identities=identities, negative_tangent_lagrangian=str(lagrangian),
                second_order_extension="all output errors canceled",
                third_order_all_excited=["-3", "0"],
                implication="Negative linear-kernel directions do not establish a better exact W design")
