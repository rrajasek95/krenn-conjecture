#!/usr/bin/env python3
"""Classify and close the primary critical two-cell Segre deformations.

Around the fixed H plus arbitrary 00/11/22 chart, compute the mixed second
variation of the pinned six-row diagonal-carrier functional for all pairs of
the 76 missing decorated cells.  Only nine of 2850 pairs are nonzero.  Their
joint remainders factor into one pure d variable times one of three small
quadratic packets.

For each of the nine critical pairs this checker then builds every literal
coefficient of q^[3]-X0 with two independent new variables.  Singular's
liftstd returns an exact source lift of the unit 1 or 2.  Thus all nine
primary second-variation charts are top-empty over characteristic zero.
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
DEPENDENCY = (
    "computations/"
    "verify_n8_one_bad_segre_cube_diagonal_carrier_first_variation.py"
)
DEPENDENCY_SHA256 = (
    "477c6a05e2cc95662bea9f3909e532de2d17c88614de16795d0be6e757c130c9"
)
EXPECTED_LIFT_SHA256 = {
    "02:10+14:02": "96507444c7325da5847a5d6c5b71b6d1012addec019552f4ab796d674be36363",
    "02:20+15:01": "d3b260bde6c79141522cee66e95af9607629b82b633e4f3d72976200d1b51982",
    "03:10+12:02": "2f1761d30724d6e68e6ad8696e7d6c09341fd3cef17636f0f5200462957fa5f0",
    "03:10+14:02": "8ac82cb5d66e89361d0208d7c1dcd0403c4b6a5f019be734c21ffcd41003cac0",
    "03:20+15:01": "45bec077183fc4a6606954e8d7ebfdcc2fe703439574c033dab15e0012ededdf",
    "04:10+12:02": "68cdd82b0b62abd9a5a127d74449bca9c0f680294511f1574896dc99dff73e5e",
    "04:20+15:01": "3dd8df1446146b4c6215e6413fa9cb80652e042d9d3f6abb7431c27d19317ace",
    "05:10+12:02": "af38caf88f8797227fc19f256374540df03049ae47e231a929135b5a8eeb4325",
    "05:10+14:02": "d4053316d78686141845d693f32db5ef395dc314532545e2981b710cc980b36f",
}
EXPECTED_LEDGER_SHA256 = (
    "85a530ce106f845e156302202f2f3a97904850e74dff21e1bd119c0a565f8efc"
)

CRITICAL = (
    ("02:10", "14:02", 4, 13, "A", 1),
    ("02:20", "15:01", 4, 12, "B", -1),
    ("03:10", "12:02", 2, 14, "C", -1),
    ("03:10", "14:02", 4, 11, "A", 1),
    ("03:20", "15:01", 4, 10, "B", -1),
    ("04:10", "12:02", 2, 13, "C", -1),
    ("04:20", "15:01", 4, 9, "B", -1),
    ("05:10", "12:02", 2, 12, "C", -1),
    ("05:10", "14:02", 4, 9, "A", 1),
)
EXPECTED_CONSTANT = {
    "02:10+14:02": 1,
    "02:20+15:01": 2,
    "03:10+12:02": 2,
    "03:10+14:02": 2,
    "03:20+15:01": 1,
    "04:10+12:02": 1,
    "04:20+15:01": 2,
    "05:10+12:02": 2,
    "05:10+14:02": 2,
}
EXPECTED_ACTIVE = {
    "02:10+14:02": 7,
    "02:20+15:01": 18,
    "03:10+12:02": 12,
    "03:10+14:02": 18,
    "03:20+15:01": 7,
    "04:10+12:02": 7,
    "04:20+15:01": 18,
    "05:10+12:02": 19,
    "05:10+14:02": 18,
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_dependency():
    path = ROOT / DEPENDENCY
    actual = sha256(path.read_bytes()).hexdigest()
    require(actual == DEPENDENCY_SHA256,
            f"dependency changed: {DEPENDENCY}: {actual}")
    spec = spec_from_file_location("first_variation", path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_cell(label):
    return ((int(label[0]), int(label[1])),
            (int(label[3]), int(label[4])))


def only_extra_degree(polynomial, degree, extra_index):
    return {
        exponent: coefficient
        for exponent, coefficient in polynomial.items()
        if exponent[extra_index] == degree
    }


def expected_joint(first_variation, variables, linear, packet, sign):
    packets = {
        "A": ((1, 6), (1, 7), (2, 5), (3, 5)),
        "B": ((1, 6), (1, 8), (2, 5), (4, 5)),
        "C": ((1, 6), (2, 5)),
    }
    quadratic = first_variation.quadratic(variables, packets[packet])
    answer = first_variation.poly_product((
        variables[linear], quadratic, variables[45], variables[45]
    ))
    return first_variation.poly_scale(answer, sign)


def audit_joint_variation(first_variation):
    diagonal_unit = first_variation.load_dependency()
    source, edges, variables, base, multipliers = first_variation.setup(
        diagonal_unit
    )
    require(len(variables) == 46,
            "the one-direction polynomial ring changed")
    universe = {
        (edge, colours)
        for edge in edges
        for colours in itertools.product(range(3), repeat=2)
    }
    missing = tuple(sorted(universe - set(base)))
    require(len(missing) == 76,
            "the missing-cell universe changed")

    critical = []
    term_histogram = Counter()
    expected_by_pair = {
        (left, right): (terms, linear, packet, sign)
        for left, right, terms, linear, packet, sign in CRITICAL
    }
    for left, right in itertools.combinations(missing, 2):
        support = dict(base)
        # Identifying the two new variables makes the mixed derivative the
        # exact extra-variable degree-two part.  The degree-one part retains
        # the two separate first variations and is intentionally discarded.
        support[left] = variables[45]
        support[right] = variables[45]
        remainder = first_variation.functional(
            source, support, multipliers
        )
        joint = only_extra_degree(remainder, 2, 45)
        term_histogram[len(joint)] += 1
        if not joint:
            continue
        labels = (first_variation.cell_label(left),
                  first_variation.cell_label(right))
        require(labels in expected_by_pair,
                f"an unexpected critical pair appeared: {labels}")
        terms, linear, packet, sign = expected_by_pair[labels]
        require(len(joint) == terms,
                f"the joint term count changed for {labels}")
        require(joint == expected_joint(
            first_variation, variables, linear, packet, sign
        ), f"the joint factorization changed for {labels}")
        critical.append((labels, terms, linear, packet, sign))

    require(len(critical) == 9,
            f"the primary critical-pair count changed: {critical}")
    require(term_histogram == Counter({0: 2841, 2: 3, 4: 6}),
            f"the joint-variation histogram changed: {term_histogram}")
    return {
        "missing_cells": missing,
        "critical": critical,
        "term_histogram": term_histogram,
    }


def singular_monomial(exponent):
    factors = []
    for index, power in enumerate(exponent):
        if power == 1:
            factors.append(f"x{index}")
        elif power > 1:
            factors.append(f"x{index}^{power}")
    return "*".join(factors) or "1"


def singular_polynomial(polynomial):
    terms = []
    for exponent, coefficient in sorted(polynomial.items()):
        require(coefficient.denominator == 1,
                "a nonintegral source coefficient entered the pair chart")
        coefficient = int(coefficient)
        monomial = singular_monomial(exponent)
        if coefficient == 1:
            terms.append(monomial)
        elif coefficient == -1:
            terms.append("-" + monomial)
        else:
            terms.append(f"{coefficient}*{monomial}")
    return "+".join(terms).replace("+-", "-") or "0"


def build_generators(first_variation, source, base, pair):
    support = dict(base)
    support[parse_cell(pair[0])] = first_variation.poly_variable(45)
    support[parse_cell(pair[1])] = first_variation.poly_variable(46)
    labels = []
    generators = []
    term_count = 0
    for word in itertools.product(range(3), repeat=6):
        polynomial = first_variation.coefficient(source, support, word)
        if not polynomial:
            continue
        target = int(word == (0,) * 6)
        expression = singular_polynomial(polynomial)
        if target:
            expression = f"({expression})-1"
        labels.append("".join(map(str, word)))
        generators.append(expression)
        term_count += len(polynomial) + target
    require(len(generators) in (411, 417),
            f"the source-row count changed for {pair}")
    require(term_count == 951,
            f"the source-term count changed for {pair}: {term_count}")
    return labels, generators, term_count


def singular_program(generators):
    variables = ",".join(f"x{index}" for index in range(47))
    code = f"ring r=0,({variables}),dp; option(redSB);\n"
    code += "ideal I=" + ",".join(generators) + ";\n"
    code += "matrix L; ideal G=liftstd(I,L);\n"
    code += "if(size(G)!=1){ print(\"UNIT_SHAPE_FAILED\"); }\n"
    code += (
        "if(matrix(I)*L-matrix(G)!=0){ print(\"SOURCE_LIFT_FAILED\"); }\n"
    )
    code += "print(\"UNIT\"); print(G[1]);\n"
    code += "int i; int nz=0;\n"
    code += "for(i=1;i<=nrows(L);i++){ if(L[i,1]!=0){ nz=nz+1; } }\n"
    code += "print(\"NONZERO\"); print(nz); print(\"ROWS\");\n"
    code += "for(i=1;i<=nrows(L);i++){ if(L[i,1]!=0){ print(i); } }\n"
    code += "print(\"BEGIN_LIFT\"); print(L); print(\"END_LIFT\");\n"
    code += "quit;\n"
    return code


def marker_value(output, marker):
    lines = output.splitlines()
    index = lines.index(marker)
    return lines[index + 1]


def audit_pair(first_variation, source, base, pair):
    key = "+".join(pair)
    labels, generators, term_count = build_generators(
        first_variation, source, base, pair
    )
    result = subprocess.run(
        ("/usr/local/bin/Singular", "-q"),
        input=singular_program(generators),
        text=True,
        capture_output=True,
        check=False,
        timeout=30,
    )
    require(result.returncode == 0,
            f"Singular failed on {key}: {result.stderr or result.stdout}")
    require("UNIT_SHAPE_FAILED" not in result.stdout,
            f"the unit shape failed on {key}")
    require("SOURCE_LIFT_FAILED" not in result.stdout,
            f"the source lift failed on {key}")
    unit = int(marker_value(result.stdout, "UNIT"))
    require(unit == EXPECTED_CONSTANT[key],
            f"the unit constant changed on {key}: {unit}")
    nonzero = int(marker_value(result.stdout, "NONZERO"))
    require(nonzero == EXPECTED_ACTIVE[key],
            f"the active-row count changed on {key}: {nonzero}")
    rows_text = result.stdout.split("ROWS\n", 1)[1].split(
        "BEGIN_LIFT\n", 1
    )[0]
    active_rows = tuple(map(int, rows_text.split()))
    require(len(active_rows) == nonzero,
            f"the active-row ledger changed on {key}")
    active_labels = [labels[index - 1] for index in active_rows]
    lift = result.stdout.split("BEGIN_LIFT\n", 1)[1].split(
        "\nEND_LIFT", 1
    )[0]
    lift_digest = sha256(lift.encode()).hexdigest()
    expected = EXPECTED_LIFT_SHA256[key]
    if expected != "TO_BE_FILLED":
        require(lift_digest == expected,
                f"the source lift changed on {key}: {lift_digest}")
    return {
        "source_rows": len(generators),
        "source_terms": term_count,
        "unit_constant": unit,
        "active_row_count": nonzero,
        "active_labels": active_labels,
        "lift_sha256": lift_digest,
    }


def audit_critical_units(first_variation, critical):
    # Give the two new cells independent variables.  The first-variation
    # module's arithmetic is intentionally reused after expanding its ring.
    first_variation.VARIABLE_COUNT = 47
    first_variation.ZERO_EXPONENT = (0,) * 47
    diagonal_unit = first_variation.load_dependency()
    source, _edges, variables, base, _multipliers = first_variation.setup(
        diagonal_unit
    )
    require(len(variables) == 47,
            "the two-direction polynomial ring changed")
    return {
        "+".join(labels): audit_pair(
            first_variation, source, base, labels
        )
        for labels, _terms, _linear, _packet, _sign in critical
    }


def main():
    first_variation = load_dependency()
    joint = audit_joint_variation(first_variation)
    units = audit_critical_units(first_variation, joint["critical"])
    ledger = {
        "dependency": {"path": DEPENDENCY, "sha256": DEPENDENCY_SHA256},
        "primary_joint_variation": {
            "missing_cell_pairs": 2850,
            "zero_joint_remainder": joint["term_histogram"][0],
            "critical_pairs": [
                {
                    "cells": list(labels),
                    "joint_terms": terms,
                    "factor": f"{sign:+d}*d{linear}*Q{packet}",
                }
                for labels, terms, linear, packet, sign in joint["critical"]
            ],
            "joint_term_histogram": {
                str(terms): count
                for terms, count in sorted(joint["term_histogram"].items())
            },
        },
        "critical_pair_source_units": units,
        "verdict": (
            "the primary six-row functional has only nine nonzero mixed "
            "second variations, and every corresponding exact two-cell "
            "top ideal contains the integral unit 1 or 2"
        ),
        "scope": (
            "the nine critical pairs for the pinned primary functional; "
            "this does not audit cross-variation of every alternative "
            "one-cell certificate across all other directions"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"critical-pair ledger changed: {digest}")
    print("N=8 Segre-K4 critical two-cell units: PASS")
    print("joint pairs: 2850 = 2841 zero + 9 critical")
    print("nine critical full top ideals: exact source units 1 or 2")
    for key, audit in units.items():
        print(f"{key}: unit {audit['unit_constant']}, "
              f"{audit['active_row_count']} rows, {audit['lift_sha256']}")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
