#!/usr/bin/env python3
"""Independent Laurent replay of the W40 response-star stratum.

This script uses a tiny local Laurent implementation and the raw matching
definition.  It proves six literal (pair,centre,K=I) response-star choices on
the entire (C*)^4 family, including the requested (67,5,I) control.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
W40_PATH = (
    ROOT / "computations/unaudited-x4general-w40-2026-08-20/results_t3.json"
)
PINNED_W40_SHA256 = (
    "30ad242d62b5cb905858842ce4e8255b105862dc21a65c73c080557fa8c1617f"
)
SITES = tuple(range(8))
COLOURS = tuple(range(3))
PARAMETERS = ("s", "t", "a", "b")
DECLARED_CONTROLS = {
    "integral_point_matches_pinned_w40",
    "raw_laurent_x4_4881",
    "q26_sign_mutation_must_fire",
    "six_identity_caps",
    "pair67_centre5_exact_support",
    "endpoint_reversal",
    "support_separated_six",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


class Laurent:
    __slots__ = ("terms",)

    def __init__(self, terms=None):
        self.terms = {
            tuple(exponent): Fraction(coefficient)
            for exponent, coefficient in (terms or {}).items()
            if coefficient
        }

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

    __radd__ = __add__

    def __neg__(self):
        return Laurent({key: -value for key, value in self.terms.items()})

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return Laurent.constant(other) - self

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

    __rmul__ = __mul__

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

    def at_ones(self):
        return sum(self.terms.values(), Fraction(0))


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
    return {
        (u, v): [[ZERO for _ in COLOURS] for _ in COLOURS]
        for u, v in combinations(SITES, 2)
    }


def put(source, u, v, cu, cv, value):
    require(u < v, (u, v))
    source[(u, v)][cu][cv] = value


def torus_source(q26_sign=-1):
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
    put(source, 5, 7, 2, 2, Laurent.monomial((-1, -1, -1, -1), -1))
    return source


def cell(source, u, v, cu, cv):
    if u < v:
        return source[(u, v)][cu][cv]
    return source[(v, u)][cv][cu]


def hafnian(source, word):
    total = ZERO
    for matching in perfect_matchings(SITES):
        term = ONE
        for u, v in matching:
            term = term * cell(source, u, v, word[u], word[v])
            if not term:
                break
        total = total + term
    return total


def off_count(word):
    return 8 - max(word.count(colour) for colour in COLOURS)


def response_entry(source, p, q, a, b, alpha, beta, cap):
    total = ZERO
    for i in COLOURS:
        for j in COLOURS:
            total = total + cap[i][j] * (
                cell(source, p, a, i, alpha) * cell(source, q, b, j, beta)
                + cell(source, p, b, i, beta) * cell(source, q, a, j, alpha)
            )
    return total


def response_support(source, p, q, cap):
    residual = tuple(site for site in SITES if site not in (p, q))
    support = []
    for a, b in combinations(residual, 2):
        for alpha in COLOURS:
            for beta in COLOURS:
                value = response_entry(source, p, q, a, b, alpha, beta, cap)
                if value:
                    support.append({
                        "edge": [a, b], "cell": [alpha, beta],
                        "value": value.text(),
                    })
    return support


def identity_support_separated(source, p, q, centre):
    """Support-only sufficient condition for R_ab(I)=0 off a star.

    For every cap colour i and distinct non-centre residual sites a,b, no
    endpoint-p row-i cell at a may coexist with an endpoint-q row-i cell at
    b (and vice versa).  This kills each summand before cancellation.
    """
    residual = tuple(site for site in SITES if site not in (p, q, centre))
    violations = []
    neighbour_rows = []
    for i in COLOURS:
        p_neighbours = [
            a for a in residual
            if any(cell(source, p, a, i, alpha) for alpha in COLOURS)
        ]
        q_neighbours = [
            a for a in residual
            if any(cell(source, q, a, i, alpha) for alpha in COLOURS)
        ]
        neighbour_rows.append({
            "cap_colour": i,
            "p_noncentre_neighbours": p_neighbours,
            "q_noncentre_neighbours": q_neighbours,
        })
        for a in p_neighbours:
            for b in q_neighbours:
                if a != b:
                    violations.append([i, a, b])
    return not violations, neighbour_rows, violations


def main():
    controls_run = set()
    source = torus_source()
    require(sha256(W40_PATH.read_bytes()).hexdigest() == PINNED_W40_SHA256,
            "pinned W40 result changed")
    pinned = json.loads(W40_PATH.read_text())
    expected = pinned["engine_audit"]["witness_B_integral"]["source"]
    for key, matrix in expected.items():
        u, v = (int(piece.strip()) for piece in key.strip("()").split(","))
        for i in COLOURS:
            for j in COLOURS:
                require(
                    cell(source, u, v, i, j).at_ones() == Fraction(matrix[i][j]),
                    (key, i, j),
                )
    controls_run.add("integral_point_matches_pinned_w40")
    raw_rows = []
    x4_count = 0
    for word in product(COLOURS, repeat=8):
        if off_count(word) > 4:
            continue
        value = hafnian(source, word)
        target = ONE if len(set(word)) == 1 else ZERO
        require(value == target, (word, value.text(), target.text()))
        raw_rows.append({
            "word": "".join(map(str, word)),
            "off_count": off_count(word),
            "amplitude": value.text(),
            "target": target.text(),
            "defect": (value - target).text(),
        })
        x4_count += 1
    require(x4_count == 4881, x4_count)
    with (HERE / "raw_x4_rows_w40_laurent.jsonl").open("w") as handle:
        for row in raw_rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")
    controls_run.add("raw_laurent_x4_4881")

    mutant = torus_source(q26_sign=1)
    mutation_failures = []
    for word in product(COLOURS, repeat=8):
        if off_count(word) <= 4:
            target = ONE if len(set(word)) == 1 else ZERO
            if hafnian(mutant, word) != target:
                mutation_failures.append("".join(map(str, word)))
    require(mutation_failures, "q26 mutation did not fire")
    controls_run.add("q26_sign_mutation_must_fire")

    identity = [
        [ONE if i == j else ZERO for j in COLOURS] for i in COLOURS
    ]
    choices = (
        (1, 2, 3), (1, 3, 2), (2, 3, 1),
        (5, 6, 7), (5, 7, 6), (6, 7, 5),
    )
    choice_records = []
    for p, q, centre in choices:
        support = response_support(source, p, q, identity)
        require(support, (p, q, centre, "zero response"))
        require(all(centre in item["edge"] for item in support), (p, q, centre, support))
        kappas = [identity[c][c] for c in COLOURS]
        scalar = sum(
            (identity[i][j] * cell(source, p, q, i, j)
             for i in COLOURS for j in COLOURS),
            ZERO,
        )
        require(all(kappas) and scalar, (p, q, centre, scalar.text()))
        separated, neighbour_rows, violations = identity_support_separated(
            source, p, q, centre
        )
        require(separated and not violations, (p, q, centre, violations))
        choice_records.append({
            "pair": [p, q], "centre": centre, "K": "I_3",
            "scalar": scalar.text(), "kappas": [item.text() for item in kappas],
            "response_support": support,
            "support_separation": neighbour_rows,
        })
    controls_run.add("six_identity_caps")
    controls_run.add("support_separated_six")
    target = next(row for row in choice_records if row["pair"] == [6, 7])
    require(target["centre"] == 5 and len(target["response_support"]) == 4, target)
    controls_run.add("pair67_centre5_exact_support")

    # The raw ordered formula must be equivariant under p<->q, K<->K^T.
    for p, q, centre in choices:
        residual = tuple(site for site in SITES if site not in (p, q))
        for a, b in combinations(residual, 2):
            for alpha in COLOURS:
                for beta in COLOURS:
                    left = response_entry(source, p, q, a, b, alpha, beta, identity)
                    right = response_entry(source, q, p, a, b, alpha, beta, identity)
                    require(left == right, (p, q, a, b, alpha, beta))
    controls_run.add("endpoint_reversal")

    require(controls_run == DECLARED_CONTROLS, {
        "declared": sorted(DECLARED_CONTROLS),
        "executed": sorted(controls_run),
    })
    raw_path = HERE / "raw_x4_rows_w40_laurent.jsonl"
    result = {
        "status": "PASS",
        "classification": "UNAUDITED EXACT LAURENT STRUCTURAL STRATUM",
        "base_ring": "Q[s^+-1,t^+-1,a^+-1,b^+-1]",
        "raw_x4_rows": {
            "path": raw_path.name,
            "count": x4_count,
            "sha256": sha256(raw_path.read_bytes()).hexdigest(),
        },
        "theorem_on_stratum": (
            "Every point of the W40 four-torus has each of the six listed "
            "active response-star caps K=I_3; hence each point has E_pq=0"
        ),
        "support_only_lemma": (
            "If, for every cap colour i, endpoint p's and endpoint q's "
            "row-i noncentre neighbour sets have no distinct cross-pair, "
            "then every off-star response cell for K=I vanishes termwise. "
            "If trace(A_pq) is nonzero, this is an active clean cap."
        ),
        "choices": choice_records,
        "negative_controls": {
            "q26_sign_mutant_x4_failures": mutation_failures,
        },
        "controls": {
            "declared": sorted(DECLARED_CONTROLS),
            "executed": sorted(controls_run),
            "all_ran": True,
        },
    }
    output = HERE / "results_w40_laurent_response_star.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "raw_x4_rows": x4_count,
        "active_response_star_choices": len(choice_records),
        "controls": result["controls"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
