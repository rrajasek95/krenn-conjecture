"""Exact algebra behind the two-anchor dichotomy for coherent GHZ arms."""

from fractions import Fraction as Q
from itertools import combinations, permutations, product
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]
                       / "transverse-two-arm-ghz-2026-09-27"))
import transverse_arms as T
from transverse_arms import E, ZERO, ONE, cell, outputs, four_outputs, hafnian, require

K, L = (0, 1, 2), (3, 4, 5)


class Poly:
    """Small exact commutative polynomials for inequality certificates."""

    def __init__(self, value=0):
        self.terms = ({key: Q(v) for key, v in value.items() if v}
                      if isinstance(value, dict) else ({(): Q(value)} if value else {}))

    @staticmethod
    def variable(name):
        return Poly({(name,): 1})

    def __add__(self, other):
        other = other if isinstance(other, Poly) else Poly(other)
        result = dict(self.terms)
        for key, value in other.terms.items():
            result[key] = result.get(key, Q(0)) + value
        return Poly(result)

    __radd__ = __add__

    def __neg__(self):
        return Poly({key: -value for key, value in self.terms.items()})

    def __sub__(self, other):
        return self + (-other if isinstance(other, Poly) else -Poly(other))

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        other = other if isinstance(other, Poly) else Poly(other)
        result = {}
        for left, a in self.terms.items():
            for right, b in other.terms.items():
                key = tuple(sorted(left + right))
                result[key] = result.get(key, Q(0)) + a*b
        return Poly(result)

    __rmul__ = __mul__


def check_scalar_certificates():
    M, a, t, d, theta, hr, hs, hu, wu, beta, k = [
        Poly.variable(name) for name in
        ("M", "a", "t", "d", "theta", "hr", "hs", "hu", "wu", "beta", "k")]
    certificates = []

    def record(name, left, right, assumptions):
        require(left.terms == right.terms, "Polynomial certificate: " + name)
        certificates.append(dict(name=name, monomials=len(left.terms),
                                 nonnegative_factors=assumptions))

    record("refined bracket envelope",
           3*M*(t*d+theta*hr*hs)
           - (M*(t*d+theta*hr*hs) + hr*M*(d+theta*hs) + hs*M*(d+theta*hr)),
           M*d*((t-hr)+(t-hs)),
           ["M,d >= 0", "hr,hs <= t"])

    center_constant = M*(1+a)+a
    record("center anchor controls the hidden cross product",
           center_constant*t*d - (M*t*d+M*theta*hr*hu+hr*wu),
           M*((a*d-hr)*theta*hu+a*d*((t-hu)+(1-theta)*hu))
           + (a*d-hr)*wu+a*d*(t-wu),
           ["M,a,d,hu,wu >= 0", "hr <= a*d",
            "hu,wu <= t", "0 <= theta <= 1"])

    record("leaf anchor envelope with beta = theta*t",
           (M+a)*t*d+(M+a)*theta*t*hr
           - (M*t*d+M*theta*hr*hu+hu*a*(d+theta*hr)),
           (a*d+(M+a)*theta*hr)*(t-hu),
           ["M,a,d,theta,hr >= 0", "hu <= t"])

    record("large hidden attachment absorption",
           2*k*t*d-hr*wu,
           2*(k*t*d+k*beta*hr-hr*wu)+hr*(wu-2*k*beta),
           ["hr >= 0", "hr*wu <= k*t*d+k*beta*hr", "wu >= 2*k*beta"])

    record("absorbed arm gives a small rescaled attachment",
           t*wu*d-beta*hr*wu,
           t*d*(wu-2*k*beta)+beta*(2*k*t*d-hr*wu),
           ["t,d,beta >= 0", "wu >= 2*k*beta", "hr*wu <= 2*k*t*d"])

    # The threshold is essential for the absorption argument.
    kval, tv, dv, bv, hv, wv = Q(2), Q(1), Q(1, 100), Q(1, 10), Q(1), Q(1, 5)
    require(hv*wv <= kval*tv*dv+kval*bv*hv, "Negative control satisfies pair envelope")
    require(hv > 2*kval*tv*dv/wv and wv < 2*kval*bv,
            "Dropping the large-hidden threshold invalidates the arm conclusion")
    return dict(certificates=certificates, missing_threshold_negative_control=True)


def check_tensor_identities():
    q = 2
    u = (E(1, 1), E(2, -1))
    vectors = {1: (E(1, 2), E(2)), 2: (E(-1, 1), E(3, -1))}
    scale = E(7)
    source = {(0, i, a, b): scale*sign*u[a]*vectors[i][b]
              for i, sign in ((1, 1), (2, -1))
              for a, b in product(range(q), repeat=2)}
    closing = {(a, b): E(2+a-b, 1+a+b) for a, b in product(range(q), repeat=2)}
    source.update({(1, 2, a, b): z for (a, b), z in closing.items()})
    h = {(r, a, b): E(r+a+2*b, 1+a-b)
         for r in L for a, b in product(range(q), repeat=2)}
    w = {r: (E(r, 1), E(1-r, 2)) for r in L}
    error = {(i, r, a, b): E(1+i-r+a, b-i)
             for i in (1, 2) for r in L for a, b in product(range(q), repeat=2)}
    z = {(r, s, a, b): E(r-s+a, 1+r+a-b)
         for r, s in combinations(L, 2) for a, b in product(range(q), repeat=2)}
    cross = {(0, r, a, b): value for (r, a, b), value in h.items()}
    cross.update({(i, r, a, b): vectors[i][a]*w[r][b]+error[i, r, a, b]
                  for i in (1, 2) for r in L for a, b in product(range(q), repeat=2)})
    source.update(cross)
    source.update({(r, s, a, b): value for (r, s, a, b), value in z.items()})
    response = four_outputs(source, n=6, q=q)
    single_count, pair_count = 0, 0
    for r in L:
        for a0, a1, a2, ar in product(range(q), repeat=4):
            rhs = (source[0, 1, a0, a1]*error[2, r, a2, ar]
                   + source[0, 2, a0, a2]*error[1, r, a1, ar]
                   + h[r, a0, ar]*closing[a1, a2])
            require(response.get(((0, 1, 2, r), (a0, a1, a2, ar)), ZERO) == rhs,
                    "Single response after coherent-kernel decomposition")
            single_count += 1
    for r, s in combinations(L, 2):
        for i in (1, 2):
            for a0, ai, ar, ass in product(range(q), repeat=4):
                symmetric = h[r, a0, ar]*w[s][ass]+h[s, a0, ass]*w[r][ar]
                rhs = (source[0, i, a0, ai]*z[r, s, ar, ass]
                       + vectors[i][ai]*symmetric
                       + h[r, a0, ar]*error[i, s, ai, ass]
                       + h[s, a0, ass]*error[i, r, ai, ar])
                require(response.get(((0, i, r, s), (a0, ai, ar, ass)), ZERO) == rhs,
                        "Complementary pair response including each error term")
                pair_count += 1
    full = outputs(source, n=6, colors=q)
    permanent = outputs(cross, n=6, colors=q)
    projected_rhs = {}
    for word in product(range(q), repeat=6):
        outside = ZERO
        projected = ZERO
        for r, s in combinations(L, 2):
            other = next(v for v in L if v not in (r, s))
            outside += z[r, s, word[r], word[s]]*response.get(
                ((0, 1, 2, other), (word[0], word[1], word[2], word[other])), ZERO)
            bracket = (h[r, word[0], word[r]]*cross[2, s, word[2], word[s]]
                       + h[s, word[0], word[s]]*cross[2, r, word[2], word[r]])
            projected += error[1, other, word[1], word[other]]*bracket
        require(full.get(word, ZERO) == outside+permanent.get(word, ZERO),
                "Complete six-site matching split")
        if projected:
            projected_rhs[word] = projected
    require(T.project(permanent, vectors[1], 1) == T.project(projected_rhs, vectors[1], 1),
            "Projected permanent is the sum of error times complementary bracket")
    ghz = {(0,)*6: ONE, (1,)*6: ONE}
    require(T.norm2(T.project(ghz, vectors[1], 1)) == 1,
            "Projection retains unit binary GHZ norm")
    return dict(single_response_coordinates=single_count, pair_response_coordinates=pair_count,
                matching_split_coordinates=64, projected_permanent_coordinates=64)


def check_formal_tensor_identities():
    """Compare coefficients with every free block entry an indeterminate."""
    variable = lambda *name: Poly.variable("_".join(map(str, name)))
    v = {i: [variable("v", i, a) for a in range(2)] for i in (1, 2)}
    h = {(r, a, b): variable("h", r, a, b)
         for r in L for a, b in product(range(2), repeat=2)}
    w = {(r, a): variable("w", r, a) for r in L for a in range(2)}
    error = {(i, r, a, b): variable("e", i, r, a, b)
             for i in (1, 2) for r in L for a, b in product(range(2), repeat=2)}
    source = {(0, i, a, b): variable("g", i, a, b)
              for i in (1, 2)
              for a, b in product(range(2), repeat=2)}
    source.update({(1, 2, a, b): variable("closing", a, b)
                   for a, b in product(range(2), repeat=2)})
    source.update({(0, r, a, b): value for (r, a, b), value in h.items()})
    source.update({(i, r, a, b): v[i][a]*w[r, b]+error[i, r, a, b]
                   for i in (1, 2) for r in L for a, b in product(range(2), repeat=2)})
    source.update({(r, s, a, b): variable("z", r, s, a, b)
                   for r, s in combinations(L, 2) for a, b in product(range(2), repeat=2)})

    def matching_output(vertices, word):
        result = Poly()
        for matching in T.matchings(vertices):
            term = Poly(1)
            for i, j in matching:
                term *= source[i, j, word[i], word[j]]
            result += term
        return result

    for r in L:
        for colors in product(range(2), repeat=4):
            a0, a1, a2, ar = colors
            word = dict(zip((0, 1, 2, r), colors))
            left = matching_output((0, 1, 2, r), word)
            right = ((source[0, 1, a0, a1]*v[2][a2]
                      + source[0, 2, a0, a2]*v[1][a1])*w[r, ar]
                     + source[0, 1, a0, a1]*error[2, r, a2, ar]
                     + source[0, 2, a0, a2]*error[1, r, a1, ar]
                     + h[r, a0, ar]*source[1, 2, a1, a2])
            require(left.terms == right.terms, "Formal single-response identity")
    for r, s in combinations(L, 2):
        for i in (1, 2):
            for colors in product(range(2), repeat=4):
                a0, ai, ar, ass = colors
                word = dict(zip((0, i, r, s), colors))
                symmetric = h[r, a0, ar]*w[s, ass]+h[s, a0, ass]*w[r, ar]
                right = (source[0, i, a0, ai]*source[r, s, ar, ass]
                         + v[i][ai]*symmetric
                         + h[r, a0, ar]*error[i, s, ai, ass]
                         + h[s, a0, ass]*error[i, r, ai, ar])
                require(matching_output((0, i, r, s), word).terms == right.terms,
                        "Formal complementary pair response")
    monomials = 0
    for word in product(range(2), repeat=6):
        full = matching_output(tuple(range(6)), word)
        permanent = Poly()
        for r, s, other in permutations(L):
            permanent += (h[r, word[0], word[r]]*source[1, s, word[1], word[s]]
                          * source[2, other, word[2], word[other]])
        outside, remainder, killed = Poly(), Poly(), Poly()
        for r, s in combinations(L, 2):
            other = next(a for a in L if a not in (r, s))
            outside += source[r, s, word[r], word[s]]*matching_output((0, 1, 2, other), word)
            bracket = (h[r, word[0], word[r]]*source[2, s, word[2], word[s]]
                       + h[s, word[0], word[s]]*source[2, r, word[2], word[r]])
            remainder += error[1, other, word[1], word[other]]*bracket
            killed += v[1][word[1]]*w[other, word[other]]*bracket
        require(full.terms == (outside+permanent).terms, "Formal full matching split")
        require(permanent.terms == (remainder+killed).terms,
                "Formal removed term has the fixed local factor v1")
        monomials += len(full.terms)
    return dict(single_response_identities=48, pair_response_identities=96,
                matching_split_identities=64, local_factor_identities=64,
                expanded_output_monomials=monomials,
                scope="Coefficient identities with arbitrary arms, including a nonzero Phi(v)")


def check_anchor_cases():
    ground = T.original_ground()
    cofactor = {e: hafnian(ground, tuple(v for v in range(6) if v not in e))
                for e in combinations(range(6), 2)}
    cases = {"center": 0, "leaf": 0}
    leaf_permutations = 0
    for core in combinations(range(6), 3):
        if any(cofactor[e] for e in combinations(core, 2)):
            continue
        outside = [v for v in range(6) if v not in core]
        for center in core:
            choices = {i: [(r, s) for r, s in combinations(outside, 2)
                           if cofactor[tuple(sorted((i, r)))]
                           and cofactor[tuple(sorted((i, s)))]]
                       for i in core}
            if choices[center]:
                cases["center"] += 1
            else:
                leaves = [i for i in core if i != center and choices[i]]
                require(leaves, "A leaf supplies two anchors when the center does not")
                cases["leaf"] += 1
                leaf_permutations += len(leaves)
    require(cases == {"center": 12, "leaf": 12}, "All 24 core-center choices")
    return dict(cases=cases, available_leaf_selections=leaf_permutations)


def check_single_edge_frontier():
    edges = list(combinations(range(6), 2))
    pair_count, triple_count, single_count = 0, 0, 0
    for count in (1, 2, 3):
        for chosen in combinations(edges, count):
            if len({v for edge in chosen for v in edge}) != 2*count:
                continue
            palettes = (1, 2) if count == 1 else (1,)
            for matrix_rank in palettes:
                source = {(*edge, a, a): E(1+sum(edge)+a, a)
                          for edge in chosen for a in range(matrix_rank)}
                response = four_outputs(source, n=6, q=2)
                if count == 1:
                    require(not response, "Single edges of either binary rank are flat")
                    single_count += 1
                else:
                    require(len(response) == count*(count-1)//2,
                            "Each disjoint edge pair has one uncancelled quartet")
                    require(all(response.values()), "No matching-support cancellation")
                    pair_count += count == 2
                    triple_count += count == 3
    require((single_count, pair_count, triple_count) == (30, 45, 15),
            "All disjoint supports and both single-edge ranks")
    return dict(single_edge_fixtures=single_count, disjoint_pair_fixtures=pair_count,
                disjoint_triple_fixtures=triple_count)


def check():
    return dict(scalar_certificates=check_scalar_certificates(),
                formal_tensor_identities=check_formal_tensor_identities(),
                tensor_identities=check_tensor_identities(),
                ground_anchor_cases=check_anchor_cases(),
                single_edge_frontier=check_single_edge_frontier())
