#!/usr/bin/env python3
"""Audit the anchor-preserving initial-form frontier of the Segre--K4 chart.

The 14 fixed H cells determine a literal site/colour incidence lattice.
An affine word-diagonal degeneration which retains a pure-00 matching must
give weight zero to H and to the three cells of that matching.  This checker
computes the resulting exact quotient for all 15 pure matchings.

When the matching contains the distinguished edge 01, only four outside
mixed cells are forced to weight zero.  All 16 subsets of those four cells
are then proved top-empty by exact Singular source lifts.  The remaining
failure of the chart degeneration is the simultaneous A/B incidence pair.
When the matching avoids 01, a 24-cell zero class remains instead; this is
the sharp unresolved simultaneous-deformation guard.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import itertools
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DEPENDENCY = "computations/verify_n8_one_bad_segre_cube_four_residual_units.py"
DEPENDENCY_SHA256 = (
    "a09d41c4bed6b774026395b953bc5d51e19d74f3b41ae2d513a6c6b263a4a1d0"
)
EXPECTED_LEDGER_SHA256 = (
    "1be15004260753354a4cd17df132a776fd3bae943635ae4bef83cdbc3c0eb04b"
)

SITES = tuple(range(6))
COLOURS = tuple(range(3))
EDGES = tuple(itertools.combinations(SITES, 2))
COORDINATES = tuple((site, colour) for site in SITES for colour in COLOURS)
COORDINATE_INDEX = {coordinate: index
                    for index, coordinate in enumerate(COORDINATES)}

ZERO_CLASS = frozenset((
    "23:21", "25:21", "34:12", "45:21",
))
NEGATIVE_CLASS = frozenset((
    "02:02", "02:10", "02:12", "02:20",
    "03:01", "03:10", "03:20", "03:21",
    "04:02", "04:10", "04:12", "04:20",
    "05:01", "05:10", "05:20", "05:21",
))
POSITIVE_CLASS = frozenset((
    "12:02", "13:01", "14:02", "15:01",
))
LARGE_ZERO_CLASS = ZERO_CLASS | NEGATIVE_CLASS | POSITIVE_CLASS

# Both tables vanish on H and on the canonical pure matching 01|23|45.
# The first is positive on every outside mixed cell except ZERO_CLASS and
# NEGATIVE_CLASS; the second exchanges NEGATIVE_CLASS/POSITIVE_CLASS.
SEPARATOR_WITHOUT_NEGATIVE = (
    (-1, -1, -1), (1, 2, 2), (0, 2, 0),
    (0, 0, 2), (0, 2, 0), (0, 0, 2),
)
SEPARATOR_WITHOUT_POSITIVE = (
    (1, 1, 1), (-1, 1, 1), (0, 2, 0),
    (0, 0, 2), (0, 2, 0), (0, 0, 2),
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_dependency():
    path = ROOT / DEPENDENCY
    actual = sha256(path.read_bytes()).hexdigest()
    require(actual == DEPENDENCY_SHA256,
            f"dependency changed: {DEPENDENCY}: {actual}")
    spec = spec_from_file_location("four_residual", path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        remainder = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remainder):
            yield ((first, second),) + tail


MATCHINGS = tuple(perfect_matchings(SITES))


def cell_label(cell):
    edge, colours = cell
    return f"{edge[0]}{edge[1]}:{colours[0]}{colours[1]}"


def parse_cell(label):
    return ((int(label[0]), int(label[1])),
            (int(label[3]), int(label[4])))


def incidence(cell):
    edge, colours = cell
    row = [Fraction(0) for _ in COORDINATES]
    row[COORDINATE_INDEX[(edge[0], colours[0])]] += 1
    row[COORDINATE_INDEX[(edge[1], colours[1])]] += 1
    return tuple(row)


def vector_add(*vectors):
    return tuple(sum(entries, Fraction(0)) for entries in zip(*vectors))


def matrix_rank(rows):
    matrix = [list(map(Fraction, row)) for row in rows]
    if not matrix:
        return 0
    row_count = len(matrix)
    column_count = len(matrix[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next((row for row in range(pivot_row, row_count)
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / scale for entry in matrix[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [left - scale * right for left, right in
                           zip(matrix[row], matrix[pivot_row], strict=True)]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def in_span(vector, rows):
    return matrix_rank(rows + [vector]) == matrix_rank(rows)


def weight(cell, table):
    edge, colours = cell
    return (table[edge[0]][colours[0]]
            + table[edge[1]][colours[1]])


def audit_incidence(source, support_H):
    outside = frozenset(
        (edge, colours)
        for edge in EDGES
        for colours in itertools.product(COLOURS, repeat=2)
        if colours[0] != colours[1]
        and (edge, colours) not in support_H
    )
    require(len(outside) == 76,
            "the mixed outside-cell universe changed")
    h_rows = [incidence(cell) for cell in sorted(support_H)]
    require(matrix_rank(h_rows) == 9,
            "the H site/colour incidence rank changed")

    zero_class_by_matching = {}
    for matching in MATCHINGS:
        anchor_cells = tuple((edge, (0, 0)) for edge in matching)
        rows = h_rows + [incidence(cell) for cell in anchor_cells]
        zero = frozenset(cell_label(cell) for cell in outside
                         if in_span(incidence(cell), rows))
        label = "|".join(f"{left}{right}" for left, right in matching)
        zero_class_by_matching[label] = sorted(zero)
        if (0, 1) in matching:
            require(zero == ZERO_CLASS,
                    f"the edge-01 anchor zero class changed: {label}: {zero}")
        else:
            require(zero == LARGE_ZERO_CLASS,
                    f"the off-01 anchor zero class changed: {label}: {zero}")

    canonical = ((0, 1), (2, 3), (4, 5))
    canonical_rows = h_rows + [incidence((edge, (0, 0)))
                               for edge in canonical]
    require(matrix_rank(canonical_rows) == 11,
            "the H plus unary-anchor incidence rank changed")

    # The two explicit cocharacters prove the full separation statement.
    for table, exceptional in (
            (SEPARATOR_WITHOUT_NEGATIVE, NEGATIVE_CLASS),
            (SEPARATOR_WITHOUT_POSITIVE, POSITIVE_CLASS)):
        require(all(weight(cell, table) == 0 for cell in support_H),
                "a separator stopped fixing H")
        require(all(weight((edge, (0, 0)), table) == 0
                    for edge in canonical),
                "a separator stopped fixing the unary anchor matching")
        for cell in outside:
            label = cell_label(cell)
            value = weight(cell, table)
            if label in ZERO_CLASS:
                require(value == 0,
                        f"a forced-zero direction moved: {label}: {value}")
            elif label in exceptional:
                require(value == -1,
                        f"an exceptional direction changed: {label}: {value}")
            else:
                require(value > 0,
                        f"a suppressible direction lost positivity: "
                        f"{label}: {value}")

    # Every negative/positive pair is an exact positive circuit modulo the
    # retained H and unary-anchor incidences.  Hence no cocharacter fixing
    # that initial face can make both members strictly positive.
    for negative in sorted(NEGATIVE_CLASS):
        for positive in sorted(POSITIVE_CLASS):
            circuit = vector_add(incidence(parse_cell(negative)),
                                 incidence(parse_cell(positive)))
            require(in_span(circuit, canonical_rows),
                    f"the A/B positive circuit changed: {negative}, {positive}")

    return {
        "H_incidence_rank": matrix_rank(h_rows),
        "H_plus_anchor_rank": matrix_rank(canonical_rows),
        "outside_mixed_cells": len(outside),
        "anchor_matchings_with_01": sum("01" in label.split("|")
                                        for label in zero_class_by_matching),
        "edge_01_zero_class": sorted(ZERO_CLASS),
        "off_01_zero_class": sorted(LARGE_ZERO_CLASS),
        "negative_class": sorted(NEGATIVE_CLASS),
        "positive_class": sorted(POSITIVE_CLASS),
        "positive_pair_circuits": len(NEGATIVE_CLASS) * len(POSITIVE_CLASS),
        "zero_classes_by_anchor_matching": zero_class_by_matching,
        "criterion": (
            "for an anchor matching through 01, every outside mixed support "
            "avoiding one of the two exceptional classes degenerates to "
            "the 45-variable chart plus its supported forced-zero cells"
        ),
    }


def poly_constant(variable_count, value):
    value = Fraction(value)
    return {} if not value else {(0,) * variable_count: value}


def poly_variable(variable_count, index):
    exponent = [0] * variable_count
    exponent[index] = 1
    return {tuple(exponent): Fraction(1)}


def poly_add(*values):
    result = Counter()
    for value in values:
        result.update(value)
    return {monomial: coefficient for monomial, coefficient in result.items()
            if coefficient}


def poly_mul(left, right):
    result = Counter()
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(a + b for a, b in
                             zip(left_monomial, right_monomial, strict=True))
            result[monomial] += left_coefficient * right_coefficient
    return {monomial: coefficient for monomial, coefficient in result.items()
            if coefficient}


def poly_product(values, variable_count):
    result = poly_constant(variable_count, 1)
    for value in values:
        result = poly_mul(result, value)
    return result


def coefficient(source, support, word, variable_count):
    terms = []
    for matching in source.MATCHINGS:
        cells = tuple((edge, (word[edge[0]], word[edge[1]]))
                      for edge in matching)
        if all(cell in support for cell in cells):
            terms.append(poly_product((support[cell] for cell in cells),
                                      variable_count))
    return poly_add(*terms)


def singular_monomial(exponent):
    factors = []
    for index, power in enumerate(exponent):
        if power == 1:
            factors.append(f"x{index}")
        elif power:
            factors.append(f"x{index}^{power}")
    return "*".join(factors) or "1"


def singular_polynomial(polynomial):
    terms = []
    for exponent, coefficient in sorted(polynomial.items()):
        require(coefficient.denominator == 1,
                "a nonintegral coefficient entered the chart")
        coefficient = int(coefficient)
        monomial = singular_monomial(exponent)
        if coefficient == 1:
            terms.append(monomial)
        elif coefficient == -1:
            terms.append("-" + monomial)
        else:
            terms.append(f"{coefficient}*{monomial}")
    return "+".join(terms).replace("+-", "-") or "0"


def build_chart(source, support_H, weights_H, subset):
    variable_count = 45 + len(subset)
    variables = tuple(poly_variable(variable_count, index)
                      for index in range(variable_count))
    support = {cell: poly_constant(variable_count, weights_H[cell])
               for cell in support_H}
    for edge_index, edge in enumerate(EDGES):
        for colour, offset in ((0, 0), (1, 15), (2, 30)):
            support[(edge, (colour, colour))] = variables[offset + edge_index]
    for index, label in enumerate(subset, 45):
        support[parse_cell(label)] = variables[index]

    labels = []
    generators = []
    term_count = 0
    for word in itertools.product(COLOURS, repeat=6):
        polynomial = coefficient(source, support, word, variable_count)
        if not polynomial:
            continue
        expression = singular_polynomial(polynomial)
        target = int(word == (0,) * 6)
        if target:
            expression = f"({expression})-1"
        labels.append("".join(map(str, word)))
        generators.append(expression)
        term_count += len(polynomial) + target
    return variable_count, labels, generators, term_count


def singular_lift_program(variable_count, generators):
    variables = ",".join(f"x{index}" for index in range(variable_count))
    code = f"ring r=0,({variables}),dp; option(redSB);\n"
    code += "ideal I=" + ",".join(generators) + ";\n"
    code += "matrix L; ideal G=liftstd(I,L);\n"
    code += (
        "if(size(G)!=1 || deg(G[1])!=0 || G[1]==0)"
        "{ print(\"UNIT_SHAPE_FAILED\"); }\n"
    )
    code += (
        "if(matrix(I)*L-matrix(G)!=0)"
        "{ print(\"SOURCE_LIFT_FAILED\"); }\n"
    )
    code += "int i; int nz=0;\n"
    code += "for(i=1;i<=nrows(L);i++){if(L[i,1]!=0){nz=nz+1;}}\n"
    code += "print(\"CONSTANT\"); print(G[1]);\n"
    code += "print(\"NONZERO\"); print(nz);\n"
    code += "print(\"ROWS\");\n"
    code += "for(i=1;i<=nrows(L);i++){if(L[i,1]!=0){print(i);}}\n"
    code += "print(\"BEGIN_LIFT\"); print(L); print(\"END_LIFT\");\n"
    code += "quit;\n"
    return code


def marker_value(output, marker):
    lines = output.splitlines()
    index = lines.index(marker)
    return lines[index + 1]


def audit_zero_subset(source, support_H, weights_H, subset):
    variable_count, labels, generators, term_count = build_chart(
        source, support_H, weights_H, subset
    )
    result = subprocess.run(
        ("/usr/local/bin/Singular", "-q"),
        input=singular_lift_program(variable_count, generators),
        text=True,
        capture_output=True,
        check=False,
        timeout=30,
    )
    require(result.returncode == 0,
            f"Singular failed on {subset}: {result.stderr or result.stdout}")
    require("UNIT_SHAPE_FAILED" not in result.stdout,
            f"the unit shape failed on {subset}")
    require("SOURCE_LIFT_FAILED" not in result.stdout,
            f"the source lift failed on {subset}")
    nonzero = int(marker_value(result.stdout, "NONZERO"))
    rows_text = result.stdout.split("ROWS\n", 1)[1].split(
        "BEGIN_LIFT\n", 1
    )[0]
    active_rows = tuple(map(int, rows_text.split()))
    require(len(active_rows) == nonzero,
            f"the active-row ledger failed on {subset}")
    lift = result.stdout.split("BEGIN_LIFT\n", 1)[1].split(
        "\nEND_LIFT", 1
    )[0]
    return {
        "variables": variable_count,
        "source_rows": len(generators),
        "source_terms": term_count,
        "unit_constant": marker_value(result.stdout, "CONSTANT"),
        "active_row_count": nonzero,
        "active_labels": [labels[index - 1] for index in active_rows],
        "lift_sha256": sha256(lift.encode()).hexdigest(),
    }


def audit_forced_zero_face(source, support_H, weights_H):
    labels = tuple(sorted(ZERO_CLASS))
    audits = {}
    for size in range(len(labels) + 1):
        for subset in itertools.combinations(labels, size):
            key = ",".join(subset) or "empty"
            audits[key] = audit_zero_subset(
                source, support_H, weights_H, subset
            )
    require(len(audits) == 16,
            "the forced-zero subset census changed")
    return {
        "subsets_checked": len(audits),
        "all_top_ideals_unit": True,
        "subsets": audits,
    }


def main():
    four_residual = load_dependency()
    one_cell = four_residual.load_dependency()
    first_variation = one_cell.load_dependency()
    diagonal_unit = first_variation.load_dependency()
    pure_unary = diagonal_unit.load_dependency()
    source = pure_unary.load_dependency()
    support_H, weights_H = pure_unary.build_top_null_H(source)
    incidence_audit = audit_incidence(source, support_H)
    zero_face_audit = audit_forced_zero_face(source, support_H, weights_H)
    ledger = {
        "dependency": {"path": DEPENDENCY, "sha256": DEPENDENCY_SHA256},
        "incidence": incidence_audit,
        "forced_zero_face": zero_face_audit,
        "consequence": (
            "an anchor-preserving degeneration through a pure-00 matching "
            "containing 01 closes unless the source support contains both "
            "exceptional incidence classes; a pure-00 matching avoiding 01 "
            "instead leaves the exact 24-cell simultaneous guard"
        ),
        "scope": (
            "literal site/colour diagonal one-parameter degenerations of "
            "the fixed weighted H chart; no claim that arbitrary common-q "
            "one-bad provenance selects an anchor matching through 01, and "
            "no closure of the 24-cell off-01 zero face"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"anchor-initial ledger changed: {digest}")
    print("N=8 Segre-K4 anchor-preserving initial cover: PASS")
    print("pure-00 anchors through 01: forced zero face has 4 cells")
    print("all 16 subsets of the four-cell face: exact top unit")
    print("remaining through-01 obstruction: 16 x 4 positive circuits")
    print("pure-00 anchors avoiding 01: 24-cell zero-face counterguard")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
