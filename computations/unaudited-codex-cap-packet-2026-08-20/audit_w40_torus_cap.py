#!/usr/bin/env python3
"""Exact Laurent audit of the W40 four-torus and its cap at pair 67.

The source is written explicitly below in endpoint order.  All coefficient
rows, the cap partition, and the N=8 clean error are rebuilt from raw perfect
matchings over Q[s^+-1,t^+-1,a^+-1,b^+-1].

UNAUDITED: this is a new same-lane encoding, not an independent audit.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
W40_RESULT = (ROOT / "computations/unaudited-x4general-w40-2026-08-20/"
              "results_t3.json")
PINNED_W40_SHA256 = (
    "30ad242d62b5cb905858842ce4e8255b105862dc21a65c73c080557fa8c1617f"
)
SITES = tuple(range(8))
COLOURS = range(3)
PARAMETERS = ("s", "t", "a", "b")
DECLARED_CONTROLS = {
    "integral_point_matches_pin",
    "raw_x4_all_rows",
    "q26_sign_mutation_must_fire",
    "cap_partition_all_rows",
    "response_deletion_mutation_must_fire",
    "clean_error_all_rows",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


class Laurent:
    """Sparse Laurent polynomial in (s,t,a,b) over Q."""

    __slots__ = ("terms",)

    def __init__(self, terms=None):
        self.terms = {tuple(exponent): Fraction(coefficient)
                      for exponent, coefficient in (terms or {}).items()
                      if coefficient}

    @staticmethod
    def constant(value):
        value = Fraction(value)
        return Laurent({(0, 0, 0, 0): value}) if value else Laurent()

    @staticmethod
    def monomial(exponent, coefficient=1):
        coefficient = Fraction(coefficient)
        return Laurent({tuple(exponent): coefficient}) if coefficient else Laurent()

    def __bool__(self):
        return bool(self.terms)

    def __eq__(self, other):
        if not isinstance(other, Laurent):
            other = Laurent.constant(other)
        return self.terms == other.terms

    def __add__(self, other):
        if not isinstance(other, Laurent):
            other = Laurent.constant(other)
        answer = dict(self.terms)
        for exponent, coefficient in other.terms.items():
            new = answer.get(exponent, Fraction(0)) + coefficient
            if new:
                answer[exponent] = new
            else:
                answer.pop(exponent, None)
        return Laurent(answer)

    def __neg__(self):
        return Laurent({exponent: -coefficient
                        for exponent, coefficient in self.terms.items()})

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        if not isinstance(other, Laurent):
            other = Laurent.constant(other)
        answer = {}
        for left, lc in self.terms.items():
            for right, rc in other.terms.items():
                exponent = tuple(a + b for a, b in zip(left, right))
                new = answer.get(exponent, Fraction(0)) + lc * rc
                if new:
                    answer[exponent] = new
                else:
                    answer.pop(exponent, None)
        return Laurent(answer)

    def evaluate(self, values):
        total = Fraction(0)
        for exponent, coefficient in self.terms.items():
            term = coefficient
            for value, power in zip(values, exponent):
                if power >= 0:
                    term *= value ** power
                else:
                    term /= value ** (-power)
            total += term
        return total

    def text(self):
        if not self.terms:
            return "0"
        pieces = []
        for exponent, coefficient in sorted(self.terms.items()):
            factors = []
            for name, power in zip(PARAMETERS, exponent):
                if power == 1:
                    factors.append(name)
                elif power:
                    factors.append(f"{name}^{power}")
            monomial = "*".join(factors)
            if not monomial:
                piece = str(coefficient)
            elif coefficient == 1:
                piece = monomial
            elif coefficient == -1:
                piece = "-" + monomial
            else:
                piece = f"{coefficient}*{monomial}"
            pieces.append(piece)
        answer = pieces[0]
        for piece in pieces[1:]:
            answer += piece if piece.startswith("-") else "+" + piece
        return answer


ZERO = Laurent()
ONE = Laurent.constant(1)
S = Laurent.monomial((1, 0, 0, 0))
T = Laurent.monomial((0, 1, 0, 0))
A = Laurent.monomial((0, 0, 1, 0))
B = Laurent.monomial((0, 0, 0, 1))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted(((first, second),) + tail))


def empty_source():
    return {(u, v): [[ZERO for _ in COLOURS] for _ in COLOURS]
            for u in SITES for v in SITES if u < v}


def put(source, u, v, cu, cv, value):
    require(u < v, (u, v))
    source[(u, v)][cu][cv] = value


def torus_source(q26_sign=-1):
    """The W40 closed four-torus, with all unlisted cells zero."""
    source = empty_source()
    for u, v, colour in (
        (0, 1, 0), (2, 3, 0), (4, 5, 0), (6, 7, 0),
        (0, 3, 1), (1, 2, 1), (4, 7, 1), (5, 6, 1),
    ):
        put(source, u, v, colour, colour, ONE)
    for u, v, cu, cv, value in (
        (0, 4, 0, 1, ONE),
        (0, 5, 1, 0, ONE),
        (1, 7, 0, 1, -ONE),
        (3, 4, 1, 0, -ONE),
        (0, 6, 0, 2, T),
        (1, 2, 0, 2, S),
        (2, 4, 2, 1, S),
        (6, 7, 2, 1, T),
    ):
        put(source, u, v, cu, cv, value)
    put(source, 0, 4, 2, 2, A)
    put(source, 1, 3, 2, 2, B)
    put(source, 2, 6, 2, 2, Laurent.constant(q26_sign) * S * T)
    put(source, 5, 7, 2, 2,
        Laurent.monomial((-1, -1, -1, -1), -1))
    return source


def cell(source, u, v, cu, cv):
    if u < v:
        return source[(u, v)][cu][cv]
    return source[(v, u)][cv][cu]


def hafnian(source, word, vertices=SITES):
    total = ZERO
    for matching in perfect_matchings(vertices):
        term = ONE
        for u, v in matching:
            term = term * cell(source, u, v, word[u], word[v])
            if not term:
                break
        total = total + term
    return total


def off(word):
    return 8 - max(word.count(colour) for colour in COLOURS)


def cap67_response(source):
    """K=I_3, so contraction sums equal cap endpoint colours i=j."""
    response = {}
    residual = tuple(range(6))
    for a in residual:
        for b in residual:
            if a >= b:
                continue
            matrix = [[ZERO for _ in COLOURS] for _ in COLOURS]
            for alpha in COLOURS:
                for beta in COLOURS:
                    total = ZERO
                    for i in COLOURS:
                        total = total + (
                            cell(source, 6, a, i, alpha) *
                            cell(source, 7, b, i, beta) +
                            cell(source, 6, b, i, beta) *
                            cell(source, 7, a, i, alpha)
                        )
                    matrix[alpha][beta] = total
            response[(a, b)] = matrix
    scalar = sum((cell(source, 6, 7, c, c) for c in COLOURS), ZERO)
    return residual, scalar, response


def clean_error(source, residual, scalar, response):
    errors = {}
    for colours in product(COLOURS, repeat=6):
        word = dict(zip(residual, colours))
        total = ZERO
        for matching in perfect_matchings(residual):
            rs = [response[edge][word[edge[0]]][word[edge[1]]]
                  for edge in matching]
            xs = [cell(source, edge[0], edge[1],
                       word[edge[0]], word[edge[1]])
                  for edge in matching]
            total = total + rs[0] * rs[1] * rs[2]
            for original_index in range(3):
                term = scalar * xs[original_index]
                for index in range(3):
                    if index != original_index:
                        term = term * rs[index]
                total = total + term
        if total:
            errors["".join(map(str, colours))] = total.text()
    return errors


def main():
    require(sha256(W40_RESULT.read_bytes()).hexdigest() == PINNED_W40_SHA256,
            "pinned W40 result changed")
    pinned = json.loads(W40_RESULT.read_text())
    source = torus_source()
    controls_run = set()

    # Compare the explicit Laurent family at s=t=a=b=1 with the pinned
    # integral witness, cell by cell and with endpoint order retained.
    expected = pinned["engine_audit"]["witness_B_integral"]["source"]
    for key, matrix in expected.items():
        u, v = (int(piece.strip()) for piece in key.strip("()").split(","))
        for i in COLOURS:
            for j in COLOURS:
                require(cell(source, u, v, i, j).evaluate((1, 1, 1, 1)) ==
                        Fraction(matrix[i][j]), (key, i, j))
    controls_run.add("integral_point_matches_pin")

    defects = {}
    x4_checked = 0
    for word in product(COLOURS, repeat=8):
        value = hafnian(source, word)
        target = ONE if len(set(word)) == 1 else ZERO
        if off(word) <= 4:
            require(value == target, (word, value.text(), target.text()))
            x4_checked += 1
        elif value != target:
            defects["".join(map(str, word))] = (value - target).text()
    require(x4_checked == 4881 and len(defects) == 3,
            (x4_checked, defects))
    controls_run.add("raw_x4_all_rows")

    # Must-fire negative control: reversing the forced sign q26=-st breaks
    # the exact level-4 equations in the raw matching engine.
    mutant = torus_source(q26_sign=1)
    mutant_failures = []
    for word in product(COLOURS, repeat=8):
        if off(word) > 4:
            continue
        target = ONE if len(set(word)) == 1 else ZERO
        if hafnian(mutant, word) != target:
            mutant_failures.append("".join(map(str, word)))
    require(mutant_failures, "q26 sign mutation did not break X4")
    controls_run.add("q26_sign_mutation_must_fire")

    residual, scalar, response = cap67_response(source)
    require(scalar == ONE, scalar.text())
    response_support = {
        f"{a}{b}:{alpha}{beta}": entry.text()
        for (a, b), matrix in response.items()
        for alpha, row in enumerate(matrix)
        for beta, entry in enumerate(row) if entry
    }

    # Raw cap contraction versus the independently partitioned direct plus
    # response formula on all 729 residual words.
    deleted_one_response = False
    for colours in product(COLOURS, repeat=6):
        word = dict(enumerate(colours))
        left = ZERO
        for cap_colour in COLOURS:
            full = tuple(colours) + (cap_colour, cap_colour)
            left = left + hafnian(source, full)
        right = scalar * hafnian(source, tuple(colours) + (0, 0), residual)
        response_terms = []
        for a in residual:
            for b in residual:
                if a >= b:
                    continue
                remaining = tuple(site for site in residual if site not in (a, b))
                term = (response[(a, b)][word[a]][word[b]] *
                        hafnian(source, tuple(colours) + (0, 0), remaining))
                response_terms.append(term)
                right = right + term
        require(left == right, (colours, left.text(), right.text()))
        nonzero_terms = [term for term in response_terms if term]
        if nonzero_terms and left != right - nonzero_terms[0]:
            deleted_one_response = True
    controls_run.add("cap_partition_all_rows")
    require(deleted_one_response,
            "response-deletion mutation was not detected")
    controls_run.add("response_deletion_mutation_must_fire")

    errors = clean_error(source, residual, scalar, response)
    require(not errors, errors)
    controls_run.add("clean_error_all_rows")
    require(controls_run == DECLARED_CONTROLS,
            {"declared": sorted(DECLARED_CONTROLS),
             "executed": sorted(controls_run)})

    result = {
        "status": "PASS",
        "classification": "UNAUDITED EXACT LAURENT COMPUTATION",
        "family": {
            "base_ring": "Q[s^+-1,t^+-1,a^+-1,b^+-1]",
            "domain": "(C*)^4",
            "relations": ["q26=-s*t", "q57=-1/(a*b*s*t)"],
            "raw_level4_rows_checked": x4_checked,
            "off_count5_defects": defects,
        },
        "cap67": {
            "K": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            "s_direct": scalar.text(),
            "kappa": [1, 1, 1],
            "activity_product": "1",
            "response_support": response_support,
            "error_nonzero_coefficients": errors,
            "error_ledger_sha256": sha256(
                json.dumps(errors, sort_keys=True).encode()
            ).hexdigest(),
            "conclusion": (
                "K=I is an active clean physical cap at pair 67 on every "
                "point of the four-dimensional Laurent X4 stratum"
            ),
        },
        "negative_controls": {
            "q26_sign_mutant_level4_failures": mutant_failures,
            "response_deletion_caught": deleted_one_response,
        },
        "controls": {
            "declared": sorted(DECLARED_CONTROLS),
            "executed": sorted(controls_run),
            "all_ran": True,
        },
    }
    output = HERE / "results_w40_torus_cap.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
