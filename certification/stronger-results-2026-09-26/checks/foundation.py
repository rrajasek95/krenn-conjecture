"""Independent finite convention checks; these are not all-order certificates."""

from fractions import Fraction
from functools import lru_cache
from itertools import product
import hashlib
import json
from pathlib import Path
import random


class MatchingMoments:
    """First-site recursion, indexed by labeled colored sites and mean degree."""

    def __init__(self, covariance, means, direction=None):
        self.covariance = covariance
        self.means = means
        self.direction = direction or {}

    @lru_cache(None)
    def moment(self, word):
        if not word:
            return (1,), (0,)
        x, rest = word[0], word[1:]
        n = len(word)
        values = [0] * (n + 1)
        derivatives = [0] * (n + 1)
        sub, der = self.moment(rest)
        mu = self.means.get(x, 0)
        nu = self.direction.get(x, 0)
        for d, value in enumerate(sub):
            values[d + 1] += mu * value
            derivatives[d + 1] += nu * value + mu * der[d]
        for j, y in enumerate(rest):
            cov = self.covariance.get((x, y), self.covariance.get((y, x), 0))
            if cov:
                sub, der = self.moment(rest[:j] + rest[j + 1 :])
                for d, value in enumerate(sub):
                    values[d] += cov * value
                    derivatives[d] += cov * der[d]
        return tuple(values), tuple(derivatives)


def input_data(n, seed):
    rng = random.Random(seed)
    cov = {
        ((i, a), (j, b)): rng.randrange(-4, 5)
        for i in range(n)
        for j in range(i + 1, n)
        for a in range(3)
        for b in range(3)
    }
    rows = [
        {(i, a): rng.randrange(-3, 4) for i in range(n) for a in range(3)}
        for _ in range(3)
    ]
    return cov, rows


def words_for_pairs(pairs):
    for bits in product((0, 1), repeat=len(pairs)):
        w = tuple((i, pairs[i][bits[i]]) for i in range(len(pairs)))
        z = tuple((i, pairs[i][1 - bits[i]]) for i in range(len(pairs)))
        yield (-1) ** sum(bits), w, z


def contraction(left, right, pairs, ld=None, rd=None, derivative=False):
    answer = 0
    for sign, w, z in words_for_pairs(pairs):
        lv = left.moment(w)[0]
        rv = right.moment(z)[int(derivative)]
        answer += sign * (sum(lv) if ld is None else lv[ld]) * (
            sum(rv) if rd is None else rv[rd]
        )
    return answer


def reflection_checks():
    cases = []
    for n in (3, 5, 7):
        cov, (row, _, _) = input_data(n, 920000 + n)
        moments = MatchingMoments(cov, row)
        for pairs in ([(0, 1)] * n, [(i % 3, (i + 1) % 3) for i in range(n)]):
            for p in range(1, n + 1, 2):
                for q in range(1, n + 1, 2):
                    assert contraction(moments, moments, pairs, p, q) == 0
                    cases.append((n, p, q, pairs != [(0, 1)] * n))
    return {"tested_contractions": len(cases), "odd_orders": [3, 5, 7]}


def covariance_checks():
    cases = []
    homogeneous_checks = 0
    for n in (2, 4, 6):
        cov, (row, other, direction) = input_data(n, 920100 + n)
        moments = MatchingMoments(cov, row, direction)
        others = MatchingMoments(cov, other)
        zero = MatchingMoments(cov, {})
        turned_row = {x: Fraction(3 * row[x] + 4 * other[x], 5) for x in row}
        turned_other = {x: Fraction(-4 * row[x] + 3 * other[x], 5) for x in row}
        turned_a = MatchingMoments(cov, turned_row)
        turned_b = MatchingMoments(cov, turned_other)
        for pairs in ([(0, 1)] * n, [(i % 3, (i + 1) % 3) for i in range(n)]):
            before = contraction(moments, others, pairs)
            after = contraction(turned_a, turned_b, pairs)
            assert before == after
            for degree in range(0, 2 * n + 1, 2):
                lhs = sum(
                    contraction(moments, moments, pairs, d, degree - d)
                    for d in range(0, n + 1, 2)
                    if 0 <= degree - d <= n
                )
                rhs = (
                    2 ** (degree // 2) * contraction(moments, zero, pairs, degree, 0)
                    if degree <= n
                    else 0
                )
                assert lhs == rhs
                homogeneous_checks += 1
            for degree in range(1, 2 * n, 2):
                lhs = sum(
                    contraction(moments, moments, pairs, d, degree + 1 - d, True)
                    for d in range(0, n + 1, 2)
                    if 2 <= degree + 1 - d <= n
                )
                rhs = (
                    2 ** ((degree - 1) // 2)
                    * contraction(zero, moments, pairs, 0, degree + 1, True)
                    if degree + 1 <= n
                    else 0
                )
                assert lhs == rhs
                homogeneous_checks += 1
            cases.append({"n": n, "site_dependent": pairs != [(0, 1)] * n,
                          "pairing": str(before)})
    return {"rational_rotations": cases, "homogeneous_checks": homogeneous_checks}


def matrix_checks():
    off_diagonal_checks = diagonal_checks = 0
    for n in (4, 6, 8):
        cov, _ = input_data(n, 920200 + n)
        zero = MatchingMoments(cov, {})
        edge = lambda p, i, r, h: cov.get(((p, i), (r, h)), cov.get(((r, h), (p, i)), 0))
        for h in range(3):
            cofactor = {
                (r, q): zero.moment(tuple((v, h) for v in range(n) if v not in (r, q)))[0][0]
                if r != q else 0
                for r in range(n) for q in range(n)
            }
            for p in range(n):
                for i in range(3):
                    for q in range(n):
                        actual = sum(edge(p, i, r, h) * cofactor[r, q] for r in range(n))
                        if p == q:
                            word = tuple((v, i if v == p else h) for v in range(n))
                            assert actual == zero.moment(word)[0][0]
                            diagonal_checks += 1
                        else:
                            word = tuple((v, h) for v in range(n) if v not in (p, q))
                            u = {(v, h): edge(p, i, v, h) for v in range(n) if v not in (p, q)}
                            v = {(x, h): edge(p, h, x, h) for x in range(n) if x not in (p, q)}
                            both = {x: u[x] + v[x] for x in u}
                            extracted = (MatchingMoments(cov, both).moment(word)[0][2]
                                         - MatchingMoments(cov, u).moment(word)[0][2]
                                         - MatchingMoments(cov, v).moment(word)[0][2])
                            assert actual == extracted
                            off_diagonal_checks += 1
    return {"arbitrary_source_orders": [4, 6, 8], "off_diagonal_checks": off_diagonal_checks,
            "diagonal_checks": diagonal_checks}


def boundary_controls():
    cov = {((0, 0), (1, 0)): 2, ((2, 0), (3, 0)): 3,
           ((0, 1), (2, 1)): 5, ((1, 1), (3, 1)): 7,
           ((0, 2), (3, 2)): 11, ((1, 2), (2, 2)): 13}
    zero = MatchingMoments(cov, {})
    targets = {0: 6, 1: 35, 2: 143}
    for colors in product(range(3), repeat=4):
        value = zero.moment(tuple(enumerate(colors)))[0][0]
        assert value == (targets[colors[0]] if len(set(colors)) == 1 else 0)
    tested = 0
    edge = lambda p, i, r, h: cov.get(((p, i), (r, h)), cov.get(((r, h), (p, i)), 0))
    for p in range(4):
        for q in range(4):
            if p == q:
                continue
            for i, j, h in product(range(3), repeat=3):
                sites = [v for v in range(4) if v not in (p, q)]
                value = sum(edge(p, i, r, h) * edge(p, j, s, h)
                            for r in sites for s in sites if r != s)
                assert value == 0
                tested += 1
    binary = {((0, 1), (1, 1)): 1, ((1, 0), (2, 0)): 1, ((0, 1), (2, 0)): 1}
    row = {(0, 0): 2, (2, 1): 3, (1, 0): 5, (0, 1): -5,
           (1, 1): 7, (2, 0): -7}
    moments = MatchingMoments(binary, row)
    pure = [moments.moment(tuple((v, h) for v in range(3)))[0] for h in range(3)]
    assert [p[1] for p in pure] == [2, 3, 0]
    assert [6 * p[3] for p in pure] == [-420, -630, 0]
    return {"weighted_K4_tensor_coefficients": 81, "weighted_K4_EV1_coefficients": tested,
            "binary_only_negative_control_H3": [-420, -630, 0]}


if __name__ == "__main__":
    results = {"status": "PASS", "scope": "Finite exact convention checks only",
               "reflection": reflection_checks(), "covariance": covariance_checks(),
               "matrix_expansion": matrix_checks(), "boundary_controls": boundary_controls(),
               "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    output = Path(__file__).with_name("global_foundation_exact_checks.json")
    output.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))
