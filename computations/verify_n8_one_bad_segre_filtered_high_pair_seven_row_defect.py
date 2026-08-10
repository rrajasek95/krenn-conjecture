#!/usr/bin/env python3
"""Audit the canonical seven-row lift on the maximal filtered envelope."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEPENDENCY = "computations/verify_n8_one_bad_segre_24cell_response_filtration.py"
DEPENDENCY_SHA256 = (
    "1dddc71dcc3dc81ecebe29498a0f5b5d708e1f9db510899a49ea5003db6c7691"
)
EXPECTED_LEDGER_SHA256 = (
    "8b6b54618177488b399180146a4a88e02f99679c496d7cb56a5ea6d2682df17a"
)
HIGH_PAIR = ("23:10", "25:10")


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_dependency():
    path = ROOT / DEPENDENCY
    actual = sha256(path.read_bytes()).hexdigest()
    require(actual == DEPENDENCY_SHA256,
            f"dependency changed: {DEPENDENCY}: {actual}")
    spec = spec_from_file_location("filtration", path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def add_term(poly, monomial, coefficient=1):
    poly[tuple(sorted(monomial))] += Fraction(coefficient)


def add(*terms):
    result = Counter()
    for scale, poly in terms:
        for monomial, coefficient in poly.items():
            result[monomial] += scale * coefficient
    return Counter({m: c for m, c in result.items() if c})


def multiply(poly, monomial):
    return Counter({tuple(sorted(term + tuple(monomial))): coefficient
                    for term, coefficient in poly.items()})


def polynomial_payload(poly):
    return [[list(monomial), coefficient.numerator, coefficient.denominator]
            for monomial, coefficient in sorted(poly.items())]


def build_rows(anchor, support_h, weights_h):
    face = {anchor.parse_cell(label) for label in anchor.LARGE_ZERO_CLASS}
    diagonal = {(edge, (colour, colour))
                for edge in anchor.EDGES for colour in anchor.COLOURS}
    high = {anchor.parse_cell(label) for label in HIGH_PAIR}
    optional = face | diagonal | high
    q_variables = {
        cell: f"x{cell[0][0]}{cell[0][1]}_{cell[1][0]}{cell[1][1]}"
        for cell in sorted(optional)
    }
    q = {cell: (None, Fraction(value))
         for cell, value in weights_h.items()}
    q.update({cell: (name, Fraction(1))
              for cell, name in q_variables.items()})

    top = {}
    for word in itertools.product(anchor.COLOURS, repeat=6):
        poly = Counter()
        for matching in anchor.MATCHINGS:
            monomial = []
            coefficient = Fraction(1)
            for edge in matching:
                cell = (edge, (word[edge[0]], word[edge[1]]))
                if cell not in q:
                    break
                variable, value = q[cell]
                coefficient *= value
                if variable:
                    monomial.append(variable)
            else:
                add_term(poly, monomial, coefficient)
        if word == (0,) * 6:
            add_term(poly, (), -1)
        poly = Counter({m: c for m, c in poly.items() if c})
        if poly:
            top["".join(map(str, word))] = poly

    response = {}
    for word in itertools.product(anchor.COLOURS, repeat=6):
        poly = Counter()
        for p_site in anchor.SITES:
            if word[p_site] != 2:
                continue
            for s_site in anchor.SITES:
                if s_site == p_site or word[s_site] != 2:
                    continue
                residual = tuple(site for site in anchor.SITES
                                 if site not in (p_site, s_site))
                for matching in anchor.perfect_matchings(residual):
                    monomial = [f"p2_{p_site}", f"s2_{s_site}"]
                    coefficient = Fraction(1)
                    for edge in matching:
                        cell = (edge, (word[edge[0]], word[edge[1]]))
                        if cell not in q:
                            break
                        variable, value = q[cell]
                        coefficient *= value
                        if variable:
                            monomial.append(variable)
                    else:
                        add_term(poly, monomial, coefficient)
        if word == (2,) * 6:
            add_term(poly, (), -1)
        poly = Counter({m: c for m, c in poly.items() if c})
        if poly:
            response["".join(map(str, word))] = poly
    return q_variables, top, response


def reduce_over_q(vector, basis):
    vector = {m: Fraction(c) for m, c in vector.items() if c}
    while vector:
        pivot = max(vector)
        if pivot not in basis:
            return vector
        factor = vector[pivot]
        for monomial, coefficient in basis[pivot].items():
            value = vector.get(monomial, 0) - factor * coefficient
            if value:
                vector[monomial] = value
            else:
                vector.pop(monomial, None)
    return vector


def main():
    filtration = load_dependency()
    anchor = filtration.load_dependency()
    four = anchor.load_dependency()
    one = four.load_dependency()
    first = one.load_dependency()
    diagonal = first.load_dependency()
    pure = diagonal.load_dependency()
    source = pure.load_dependency()
    support_h, weights_h = pure.build_top_null_H(source)
    q_variables, top, response = build_rows(anchor, support_h, weights_h)

    symmetric_01 = Counter({("p2_1", "s2_0"): 1,
                            ("p2_0", "s2_1"): 1})
    symmetric_24 = Counter({("p2_4", "s2_2"): 1,
                            ("p2_2", "s2_4"): 1})
    defect = add(
        (-1, add(*[(coefficient, multiply(top["102222"], monomial))
                   for monomial, coefficient in symmetric_01.items()])),
        (-1, add(*[(coefficient, multiply(top["222202"], monomial))
                   for monomial, coefficient in symmetric_24.items()])),
        (1, multiply(response["220122"], ("x23_22",))),
        (1, multiply(response["220221"], ("x25_22",))),
        (-1, multiply(response["222102"], ("x34_22",))),
        (1, multiply(response["222201"], ("x45_22",))),
        (-1, response["222222"]),
        (-1, Counter({(): Fraction(1)})),
    )
    require(len(defect) == 66 and () not in defect,
            "the seven-row defect term count changed")

    grouped = {}
    for monomial, coefficient in defect.items():
        p = next(variable for variable in monomial
                 if variable.startswith("p2_"))
        s = next(variable for variable in monomial
                 if variable.startswith("s2_"))
        i, j = int(p[-1]), int(s[-1])
        q_part = tuple(variable for variable in monomial
                       if variable not in (p, s))
        grouped.setdefault((i, j), Counter())[q_part] += coefficient
    factors = {}
    for i in range(6):
        require((i, i) not in grouped, "a diagonal-star defect appeared")
        for j in range(i + 1, 6):
            require(grouped[(i, j)] == grouped[(j, i)],
                    f"the ({i},{j}) defect stopped being symmetric")
            factors[f"{i}{j}"] = polynomial_payload(grouped[(i, j)])
    require(len(factors) == 15, "the symmetric factor count changed")

    # Exact, source-provenant degree bound.  These are every mixed top row
    # multiplied by an ordered p2/s2 star pair and every mixed response row
    # multiplied by either 1 or one q coordinate.  They are precisely the
    # natural rows at the bidegrees occurring in the seven-row defect.
    candidates = []
    seen = set()
    for word, poly in sorted(response.items()):
        if word == "222222":
            continue
        for multiplier in [()] + [(variable,) for variable in q_variables.values()]:
            candidate = multiply(poly, multiplier)
            key = tuple(sorted(candidate.items()))
            if key not in seen:
                seen.add(key)
                candidates.append(candidate)
    for word, poly in sorted(top.items()):
        if word == "000000":
            continue
        for i in range(6):
            for j in range(6):
                candidate = multiply(poly, (f"p2_{i}", f"s2_{j}"))
                key = tuple(sorted(candidate.items()))
                if key not in seen:
                    seen.add(key)
                    candidates.append(candidate)
    require(len(candidates) == 48756,
            f"the bounded source-row family changed: {len(candidates)}")
    basis = {}
    for candidate in candidates:
        remainder = reduce_over_q(candidate, basis)
        if remainder:
            pivot = max(remainder)
            inverse = 1 / remainder[pivot]
            basis[pivot] = {m: c * inverse for m, c in remainder.items()}
    remainder = reduce_over_q(defect, basis)
    require(len(basis) == 48426, "the exact source-row rank changed")
    require(remainder == defect,
            "the defect unexpectedly entered the bounded source-row span")

    ledger = {
        "dependency": {"path": DEPENDENCY, "sha256": DEPENDENCY_SHA256},
        "high_pair": HIGH_PAIR,
        "maximal_envelope": {
            "q_variables": len(q_variables),
            "top_rows": len(top),
            "p2s2_rows": len(response),
        },
        "seven_row_defect": {
            "terms": len(defect),
            "symmetric_offdiagonal_factors": factors,
            "factor_count": len(factors),
            "diagonal_star_terms": 0,
        },
        "bounded_source_span": {
            "candidate_multiples": len(candidates),
            "rank_over_Q": len(basis),
            "remainder_terms": len(remainder),
            "remainder_is_full_defect": True,
        },
        "verdict": (
            "the frozen seven-row unit lifts to 1 plus a nonzero symmetric "
            "offdiagonal-star defect on the maximal grade-zero envelope; the "
            "defect is not in the exact degree-compatible span of the obvious "
            "mixed top and p2s2 source rows"
        ),
        "scope": (
            "this excludes the natural linear/source-degree lift only; higher "
            "nonlinear ideal membership or additional response sectors are not "
            "excluded"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"seven-row ledger changed: {digest}")
    print("N=8 filtered high-pair seven-row defect: PASS")
    print("defect: 66 terms = 15 symmetric offdiagonal-star factors")
    print("bounded source span: 48756 candidates, rank 48426 over Q")
    print("defect remainder: unchanged (66 terms)")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
