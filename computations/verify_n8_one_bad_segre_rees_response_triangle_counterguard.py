#!/usr/bin/env python3
"""Exact Rees audit for the off-01 Segre response equations.

The off-01 cocharacter makes the residual top equation homogeneous, but it
does not discard the positive-weight q cells from the associated-graded
response equations.  This checker verifies the complete weight statement,
the cofactor-valued lift of the odd-triangle identity, and a literal one-cell
counterguard to lifting the support clause from commit 4a213d8.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ANCHOR = ROOT / "computations/verify_n8_one_bad_segre_cube_anchor_initial_cover.py"
ANCHOR_SHA256 = "a0a2f5600029f6c79ce931171b53fff772f2fef7e0c0bb4b971ba56c0fd44ef0"
SCOPE = ROOT / "computations/verify_n8_one_bad_segre_off01_cocharacter_response_scope.py"
SCOPE_SHA256 = "c64254996f8caf8e6382730ff6b1b27a5069e795e665444c8a3f3e628cc0b5b1"
EXPECTED_LEDGER_SHA256 = (
    "2948ec5797cbeab6303b030ee7f1e9354e29dd50fccb1ae6dfc5d93b6f141fc5"
)

COCHARACTER = (
    (0, 0, 0),
    (0, 1, 1),
    (0, 1, 0),
    (0, 0, 1),
    (0, 1, 0),
    (0, 0, 1),
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(path, expected, name):
    actual = sha256(path.read_bytes()).hexdigest()
    require(actual == expected, f"{name} dependency changed: {actual}")
    spec = spec_from_file_location(name, path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def monomial(*names):
    return {tuple(sorted(names)): 1}


def poly_add(*polynomials):
    result = Counter()
    for polynomial in polynomials:
        result.update(polynomial)
    return {term: coefficient for term, coefficient in result.items()
            if coefficient}


def poly_scale(polynomial, scalar):
    return {term: scalar * coefficient
            for term, coefficient in polynomial.items() if scalar * coefficient}


def poly_mul(*polynomials):
    result = {(): 1}
    for polynomial in polynomials:
        product = Counter()
        for left, left_coefficient in result.items():
            for right, right_coefficient in polynomial.items():
                product[tuple(sorted(left + right))] += (
                    left_coefficient * right_coefficient
                )
        result = {term: coefficient for term, coefficient in product.items()
                  if coefficient}
    return result


def q_weight(cell):
    edge, colours = cell
    return (COCHARACTER[edge[0]][colours[0]]
            + COCHARACTER[edge[1]][colours[1]])


def word_grade(word):
    return sum(COCHARACTER[site][colour]
               for site, colour in enumerate(word))


def q_factor(word, matching):
    return tuple((edge, (word[edge[0]], word[edge[1]]))
                 for edge in matching)


def cofactor_terms(anchor, word, holes):
    residual = tuple(site for site in anchor.SITES if site not in holes)
    return tuple(q_factor(word, matching)
                 for matching in anchor.perfect_matchings(residual))


def product_value(q_values, cells):
    value = 1
    for cell in cells:
        value *= q_values.get(cell, 0)
    return value


def response_value(anchor, q_values, p_values, s_values, colour, word):
    total = 0
    for p_site in anchor.SITES:
        if word[p_site] != colour:
            continue
        for s_site in anchor.SITES:
            if s_site == p_site or word[s_site] != colour:
                continue
            for cells in cofactor_terms(anchor, word, {p_site, s_site}):
                total += (p_values.get(p_site, 0)
                          * s_values.get(s_site, 0)
                          * product_value(q_values, cells))
    return total


def main():
    anchor = load(ANCHOR, ANCHOR_SHA256, "anchor")
    scope = load(SCOPE, SCOPE_SHA256, "scope")
    require(scope.COMMON_COCHARACTER == COCHARACTER,
            "the scope cocharacter changed")
    four = anchor.load_dependency()
    one = four.load_dependency()
    first = one.load_dependency()
    diagonal = first.load_dependency()
    pure = diagonal.load_dependency()
    source = pure.load_dependency()
    support_h, weights_h = pure.build_top_null_H(source)

    # Every physical matching term in a fixed top coefficient has exactly
    # the output-word grade.  Hence the top map is already Rees homogeneous.
    top_rows = 0
    for word in itertools.product(anchor.COLOURS, repeat=6):
        grade = word_grade(word)
        for matching in anchor.MATCHINGS:
            cells = q_factor(word, matching)
            require(sum(q_weight(cell) for cell in cells) == grade,
                    f"a top term changed grade: {word}, {matching}")
        top_rows += 1
    require(top_rows == 729, "the top word count changed")

    # Give p_c@r and s_c@r the residual site weight u_{r,c}.  The same
    # identity then holds for every response term, including both cross rows.
    response_specs = ((1, 1), (1, 2), (2, 1), (2, 2))
    nonempty_response_rows = Counter()
    for p_colour, s_colour in response_specs:
        for word in itertools.product(anchor.COLOURS, repeat=6):
            terms = 0
            grade = word_grade(word)
            for p_site in anchor.SITES:
                if word[p_site] != p_colour:
                    continue
                for s_site in anchor.SITES:
                    if s_site == p_site or word[s_site] != s_colour:
                        continue
                    for cells in cofactor_terms(anchor, word,
                                                {p_site, s_site}):
                        term_grade = (COCHARACTER[p_site][p_colour]
                                      + COCHARACTER[s_site][s_colour]
                                      + sum(q_weight(cell) for cell in cells))
                        require(term_grade == grade,
                                "a response term changed Rees grade")
                        terms += 1
            if terms:
                nonempty_response_rows[f"{p_colour}{s_colour}"] += 1
    require(nonempty_response_rows == Counter({"11": 473, "12": 602,
                                                "21": 602, "22": 473}),
            f"response row census changed: {nonempty_response_rows}")

    q_weight_histogram = Counter(
        q_weight((edge, colours))
        for edge in anchor.EDGES
        for colours in itertools.product(anchor.COLOURS, repeat=2)
    )
    require(q_weight_histogram == Counter({0: 59, 1: 62, 2: 14}),
            f"q Rees weights changed: {q_weight_histogram}")
    star_weight_histogram = Counter(
        COCHARACTER[site][colour]
        for colour in (1, 2)
        for _star in ("p", "s")
        for site in anchor.SITES
    )
    require(star_weight_histogram == Counter({0: 12, 1: 12}),
            f"star Rees weights changed: {star_weight_histogram}")
    require(tuple(sum(COCHARACTER[site][colour] for site in anchor.SITES)
                  for colour in anchor.COLOURS) == (0, 3, 3),
            "the three diagonal target grades changed")

    # The ordinary odd-triangle identity does lift, but only after replacing
    # each restricted-face monomial Q_e by the full three-term q cofactor F_e.
    A, B, C = (monomial(name) for name in ("A", "B", "C"))
    aa, bb, cc = (monomial(name) for name in ("a", "b", "c"))
    F01, F02, F12 = (monomial(name) for name in ("F01", "F02", "F12"))
    f01 = poly_add(poly_mul(A, bb), poly_mul(B, aa))
    f02 = poly_add(poly_mul(A, cc), poly_mul(C, aa))
    f12 = poly_add(poly_mul(B, cc), poly_mul(C, bb))
    g01, g02, g12 = (poly_mul(F01, f01), poly_mul(F02, f02),
                      poly_mul(F12, f12))
    lhs = poly_scale(poly_mul(A, B, C, aa, bb, cc, F01, F02, F12), 2)
    rhs = poly_add(
        poly_mul(C, aa, A, bb, F01, F02, g12),
        poly_scale(poly_mul(C, bb, A, bb, F01, F12, g02), -1),
        poly_mul(C, bb, A, cc, F02, F12, g01),
    )
    require(lhs == rhs, "the cofactor-valued odd identity changed")

    # Literal minimal clause counterguard.  In the restricted face, the three
    # rows below have selected q factors Q_e.  The single positive-weight cell
    # 35:02 activates one alternate matching in all three full cofactors.
    words = {
        "01": (1, 1, 0, 0, 2, 2),
        "02": (1, 0, 1, 0, 2, 2),
        "12": (0, 1, 1, 0, 2, 2),
    }
    holes = {"01": {0, 1}, "02": {0, 2}, "12": {1, 2}}
    selected = {
        "01": (anchor.parse_cell("23:00"), anchor.parse_cell("45:22")),
        "02": (anchor.parse_cell("13:00"), anchor.parse_cell("45:22")),
        "12": (anchor.parse_cell("03:00"), anchor.parse_cell("45:22")),
    }
    q_values = dict(weights_h)
    for label in ("23:00", "45:22", "13:00", "03:00"):
        q_values[anchor.parse_cell(label)] = 1
    for label in ("14:02", "04:02"):
        q_values[anchor.parse_cell(label)] = -1
    added_cell = anchor.parse_cell("35:02")
    q_values[added_cell] = 1
    restricted_universe = (set(support_h)
                           | {anchor.parse_cell(label)
                              for label in anchor.LARGE_ZERO_CLASS}
                           | {(edge, (colour, colour))
                              for edge in anchor.EDGES
                              for colour in anchor.COLOURS})
    require(added_cell not in restricted_universe,
            "the counterguard cell entered the 4a universe")
    require(all(cell in restricted_universe or cell == added_cell
                for cell, value in q_values.items() if value),
            "a second cell outside the 4a universe became nonzero")
    require(q_weight(added_cell) == 1,
            "the sole added cell stopped having positive Rees weight")
    require(weights_h[anchor.parse_cell("24:02")] == -1,
            "the fixed H cancellation sign changed")

    p_values = {site: 1 for site in (0, 1, 2)}
    s_values = dict(p_values)
    cofactor_ledger = {}
    for edge in ("01", "02", "12"):
        terms = cofactor_terms(anchor, words[edge], holes[edge])
        require(len(terms) == 3, "a K4 cofactor lost a matching")
        values = tuple(int(product_value(q_values, term)) for term in terms)
        require(sorted(values) == [-1, 0, 1],
                f"the literal cofactor cancellation changed: {edge}: {values}")
        require(sum(values) == 0,
                f"the full cofactor stopped vanishing: {edge}")
        require(product_value(q_values, selected[edge]) == 1,
                f"the selected 4a monomial died: {edge}")
        require(response_value(anchor, q_values, p_values, s_values, 1,
                               words[edge]) == 0,
                f"the full response row stopped vanishing: {edge}")
        cofactor_ledger[edge] = {
            "word": "".join(map(str, words[edge])),
            "terms": [[anchor.cell_label(cell) for cell in term]
                      for term in terms],
            "values": values,
            "selected_Q": [anchor.cell_label(cell)
                           for cell in selected[edge]],
        }
    require(all(p_values[site] and s_values[site] for site in (0, 1, 2)),
            "the odd star antecedent stopped being live")

    ledger = {
        "dependencies": {
            str(ANCHOR.relative_to(ROOT)): ANCHOR_SHA256,
            str(SCOPE.relative_to(ROOT)): SCOPE_SHA256,
        },
        "q_variable_weights": dict(q_weight_histogram),
        "pure_star_variable_weights": dict(star_weight_histogram),
        "target_grades": {"X0": 0, "X1": 3, "X2": 3},
        "top_rows": top_rows,
        "nonempty_response_rows": dict(nonempty_response_rows),
        "leading_system": (
            "all 135 q cells and all 24 pure-colour star entries remain as "
            "homogeneous Rees variables; 14 H coefficients are pinned, so "
            "there are 145 free leading coefficients"
        ),
        "odd_identity": (
            "2ABCabc*F01*F02*F12 is in (F01*f01,F02*f02,F12*f12)"
        ),
        "counterguard": {
            "colour": 1,
            "triangle": [0, 1, 2],
            "sole_cell_outside_the_4a_universe": "35:02",
            "sole_cell_weight": 1,
            "cofactors": cofactor_ledger,
            "six_star_values": 1,
            "full_response_values": [0, 0, 0],
            "selected_4a_Q_values": [1, 1, 1],
        },
        "consequence": (
            "the polynomial odd circuit lifts only conditional on the full "
            "cofactors F_e; the monomial-support clauses of 4a213d8 do not "
            "lift after restoring positive-weight q cells"
        ),
        "scope": (
            "a literal local three-row counterguard, not a solution of the "
            "complete top-plus-four-response one-bad system"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"Rees response ledger changed: {digest}")

    print("N=8 Segre Rees response triangle counterguard: PASS")
    print("q weights: 59 grade0, 62 grade1, 14 grade2")
    print("star weights: 12 grade0, 12 grade1; X1/X2 grade3")
    print("full odd identity lifts with three-term cofactors")
    print("one grade-1 cell kills all three monomial odd clauses")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
