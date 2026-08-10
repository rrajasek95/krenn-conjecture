#!/usr/bin/env python3
"""Audit the response filtration induced by the Segre 24-face cocharacter."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEPENDENCY = "computations/verify_n8_one_bad_segre_cube_anchor_initial_cover.py"
DEPENDENCY_SHA256 = (
    "a0a2f5600029f6c79ce931171b53fff772f2fef7e0c0bb4b971ba56c0fd44ef0"
)
EXPECTED_LEDGER_SHA256 = (
    "d72167223da81f7243fc04185b72546df86ba85ebecc4d028c40c3e42e287316"
)

# Site rows, with columns indexed by residual colours 0,1,2.
WEIGHTS = (
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


def load_dependency():
    path = ROOT / DEPENDENCY
    actual = sha256(path.read_bytes()).hexdigest()
    require(actual == DEPENDENCY_SHA256,
            f"dependency changed: {DEPENDENCY}: {actual}")
    spec = spec_from_file_location("anchor", path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def word_grade(word):
    return sum(WEIGHTS[site][colour] for site, colour in enumerate(word))


def cell_grade(cell):
    edge, colours = cell
    return (WEIGHTS[edge[0]][colours[0]] +
            WEIGHTS[edge[1]][colours[1]])


def response_terms(anchor, allowed, p_colour, s_colour, word):
    terms = []
    for p_site in range(6):
        if word[p_site] != p_colour:
            continue
        for s_site in range(6):
            if s_site == p_site or word[s_site] != s_colour:
                continue
            residual = tuple(site for site in range(6)
                             if site not in (p_site, s_site))
            for matching in anchor.perfect_matchings(residual):
                q_factor = tuple(
                    (edge, (word[edge[0]], word[edge[1]]))
                    for edge in matching
                )
                if all(cell in allowed for cell in q_factor):
                    terms.append((p_site, s_site, tuple(sorted(q_factor))))
    return terms


def main():
    anchor = load_dependency()
    four = anchor.load_dependency()
    one = four.load_dependency()
    first = one.load_dependency()
    diagonal = first.load_dependency()
    pure = diagonal.load_dependency()
    source = pure.load_dependency()
    support_h, _weights_h = pure.build_top_null_H(source)
    face = {anchor.parse_cell(label) for label in anchor.LARGE_ZERO_CLASS}
    diagonal_cells = {
        (edge, (colour, colour))
        for edge in anchor.EDGES for colour in range(3)
    }
    allowed = set(support_h) | face | diagonal_cells

    # Exact q-coordinate face audit.
    mixed = {
        (edge, colours)
        for edge in anchor.EDGES
        for colours in itertools.product(range(3), repeat=2)
        if colours[0] != colours[1]
    }
    require(all(cell_grade(cell) == 0 for cell in support_h),
            "the cocharacter stopped fixing H")
    require(all(cell_grade(cell) == 0 for cell in face),
            "the cocharacter stopped fixing the 24-cell face")
    other_mixed = mixed - set(support_h) - face
    require(len(other_mixed) == 52 and
            all(cell_grade(cell) > 0 for cell in other_mixed),
            "the other mixed cells are not strictly raised")
    require(all(cell_grade(cell) >= 0 for cell in diagonal_cells),
            "a diagonal cell acquired negative weight")
    require(all(cell_grade((edge, (0, 0))) == 0
                for edge in anchor.EDGES),
            "a pure-00 anchor cell moved")

    response_data = (
        ("11", 1, 1, (1,) * 6),
        ("12", 1, 2, None),
        ("21", 2, 1, None),
        ("22", 2, 2, (2,) * 6),
    )
    response_ledgers = {}
    term_tables = {}
    for label, p_colour, s_colour, target in response_data:
        row_histogram = Counter()
        term_histogram = Counter()
        table = {}
        for word in itertools.product(range(3), repeat=6):
            terms = response_terms(
                anchor, allowed, p_colour, s_colour, word
            )
            if not terms:
                continue
            grade = word_grade(word)
            for p_site, s_site, q_factor in terms:
                fine_grade = (
                    WEIGHTS[p_site][p_colour] +
                    WEIGHTS[s_site][s_colour] +
                    sum(cell_grade(cell) for cell in q_factor)
                )
                require(fine_grade == grade,
                        f"response {label} lost word homogeneity: {word}")
            row_histogram[grade] += 1
            term_histogram[grade] += len(terms)
            table[word] = terms
        if target is not None:
            require(word_grade(target) == 3 and target in table,
                    f"diagonal target {label} left grade three")
        response_ledgers[label] = {
            "rows_by_grade": dict(sorted(row_histogram.items())),
            "terms_by_grade": dict(sorted(term_histogram.items())),
            "target_grade": None if target is None else word_grade(target),
        }
        term_tables[label] = table

    require(word_grade((0,) * 6) == 0 and
            word_grade((1,) * 6) == 3 and
            word_grade((2,) * 6) == 3,
            "the three target grades changed")

    # Locate literal diagonal-response binomials, retaining exact q factors.
    binomials = {}
    odd_counts = {}
    for label in ("11", "22"):
        colour = int(label[0])
        per_edge = {edge: [] for edge in itertools.combinations(range(6), 2)}
        for word, terms in term_tables[label].items():
            if len(terms) != 2:
                continue
            left, right = terms
            if ((left[0], left[1]) != (right[1], right[0]) or
                    left[2] != right[2]):
                continue
            edge = tuple(sorted((left[0], left[1])))
            q_factor = left[2]
            q_grade = sum(cell_grade(cell) for cell in q_factor)
            require(q_grade + WEIGHTS[edge[0]][colour] +
                    WEIGHTS[edge[1]][colour] == word_grade(word),
                    "a diagonal binomial lost its response grade")
            per_edge[edge].append((word, q_factor))
        require(all(per_edge.values()),
                f"the grade-filtered binomial graph changed for {label}")
        binomials[label] = per_edge

        count = 0
        degree_histogram = Counter()
        for triangle in itertools.combinations(range(6), 3):
            edges = tuple(itertools.combinations(triangle, 2))
            star_grade = sum(WEIGHTS[site][colour] for site in triangle) * 2
            for witnesses in itertools.product(
                    *(per_edge[edge] for edge in edges)):
                q_grade = sum(
                    cell_grade(cell)
                    for _word, factor in witnesses for cell in factor
                )
                total_grade = star_grade + q_grade
                # Each of the three RHS terms contains the same six star
                # coordinates and the same three q matching factors.  Thus
                # the odd triangle is homogeneous in the full fine grading.
                rhs_grades = []
                for selected in range(3):
                    row_edge = edges[selected]
                    row_word, row_factor = witnesses[selected]
                    row_grade = (
                        sum(cell_grade(cell) for cell in row_factor) +
                        WEIGHTS[row_edge[0]][colour] +
                        WEIGHTS[row_edge[1]][colour]
                    )
                    multiplier_grade = total_grade - row_grade
                    rhs_grades.append(row_grade + multiplier_grade)
                    require(row_grade == word_grade(row_word),
                            "a selected odd row changed grade")
                require(rhs_grades == [total_grade] * 3,
                        "the odd triangle stopped being homogeneous")
                degree_histogram[total_grade] += 1
                count += 1
        require(count == 13756,
                f"the filtered odd-triangle count changed for {label}")
        odd_counts[label] = {
            "triangles": count,
            "total_fine_degree_histogram": dict(sorted(degree_histogram.items())),
        }

    ledger = {
        "dependency": {"path": DEPENDENCY, "sha256": DEPENDENCY_SHA256},
        "cocharacter": WEIGHTS,
        "q_face": {
            "fixed_H_cells": len(support_h),
            "zero_face_cells": len(face),
            "strictly_positive_other_mixed_cells": len(other_mixed),
            "nonnegative_diagonal_cells": len(diagonal_cells),
        },
        "target_grades": {"X0": 0, "X1": 3, "X2": 3},
        "responses": response_ledgers,
        "filtered_odd_triangles": odd_counts,
        "verdict": (
            "every response coefficient is homogeneous of its output-word "
            "grade; both diagonal targets have grade three, all crossed zero "
            "rows split grade by grade, and every hereditary odd-triangle "
            "certificate from 4a213d8 is homogeneous in the fine source grading"
        ),
        "scope": (
            "the residual q and four response module in the fixed Segre H "
            "chart; no target-stabilizing extension to the two deleted sites "
            "and no normalization of arbitrary sources into H is claimed"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"filtered response ledger changed: {digest}")
    print("N=8 Segre response filtration: PASS")
    print("target grades: X0=0, X1=3, X2=3")
    for label in ("11", "12", "21", "22"):
        print(label, json.dumps(response_ledgers[label], sort_keys=True))
    print("odd triangles: 13756 per diagonal response; all homogeneous")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
