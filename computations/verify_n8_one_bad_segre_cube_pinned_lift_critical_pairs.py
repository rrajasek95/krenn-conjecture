#!/usr/bin/env python3
"""Audit the second-cell stability of the four pinned one-cell lifts.

The four residual one-cell charts are empty because ``liftstd`` supplies an
exact source combination equal to 2.  This checker keeps each such lift
pinned, adjoins each of the other 75 missing decorated cells, and tests the
same source combination in the enlarged chart.  Only pairs on which a pinned
lift genuinely changes are sent to a full exact standard-basis calculation.

This is a source-certificate critical-pair audit.  It deliberately does not
enumerate all 2850 two-cell supports.
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
    "computations/verify_n8_one_bad_segre_cube_four_residual_units.py"
)
DEPENDENCY_SHA256 = (
    "a09d41c4bed6b774026395b953bc5d51e19d74f3b41ae2d513a6c6b263a4a1d0"
)
RESIDUAL = ("02:20", "03:10", "04:20", "05:10")

EXPECTED_TRANSGRESSIONS = {
    "02:20": (
        "02:02", "02:10", "02:12", "03:01", "03:10", "03:20",
        "03:21", "04:02", "04:10", "04:12", "04:20", "05:10",
        "05:20", "05:21", "12:02", "13:01", "14:02", "15:01",
        "23:21", "25:21", "34:12", "45:21",
    ),
    "03:10": (
        "02:02", "02:10", "02:12", "02:20", "03:01", "03:20",
        "03:21", "04:02", "04:10", "04:12", "04:20", "05:10",
        "05:20", "05:21", "12:02", "13:01", "14:02", "15:01",
        "23:21", "34:12", "45:21",
    ),
    "04:20": (
        "02:02", "02:10", "02:12", "02:20", "03:01", "03:10",
        "03:20", "03:21", "04:02", "04:10", "04:12", "05:10",
        "05:20", "05:21", "12:02", "13:01", "14:02", "15:01",
        "23:21", "25:21", "34:12", "45:21",
    ),
    "05:10": (
        "02:02", "02:10", "02:12", "02:20", "03:01", "03:10",
        "03:20", "03:21", "04:02", "04:10", "04:12", "04:20",
        "05:20", "05:21", "12:02", "13:01", "14:02", "15:01",
        "23:21", "34:12", "45:21",
    ),
}

EXPECTED_PROPER = {
    "02:10+02:20": {
        "basis_size": 70,
        "dimension": 9,
        "basis_sha256":
            "2d285867a4c975fb6ab93e9b229d9db56687078b815ad1a244123812edaa471a",
    },
    "03:10+03:20": {
        "basis_size": 70,
        "dimension": 9,
        "basis_sha256":
            "b2872371f35389c91867ff1c16d40dc7962512c963d393e2152cd3312eafc8c9",
    },
    "04:10+04:20": {
        "basis_size": 80,
        "dimension": 9,
        "basis_sha256":
            "3ee0fc2ebf31d8e3e42c78a9c84637fcb7df90696f0e0414a7640ffb638551eb",
    },
    "05:10+05:20": {
        "basis_size": 75,
        "dimension": 9,
        "basis_sha256":
            "9b8cf47598a783fc7a0e20793a828ac33d9e3e0eca0d87422666bab7fb4b4b81",
    },
}
EXPECTED_LEDGER_SHA256 = (
    "388b9c33c354e81e5032d49b034790b52984dcc3c39375540ccc7fb666731b03"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_dependency():
    path = ROOT / DEPENDENCY
    actual = sha256(path.read_bytes()).hexdigest()
    if DEPENDENCY_SHA256 != "TO_BE_FILLED":
        require(actual == DEPENDENCY_SHA256,
                f"dependency changed: {DEPENDENCY}: {actual}")
    spec = spec_from_file_location("four_residual", path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, actual


def parse_cell(label):
    return ((int(label[0]), int(label[1])),
            (int(label[3]), int(label[4])))


def cell_label(cell):
    edge, colours = cell
    return f"{edge[0]}{edge[1]}:{colours[0]}{colours[1]}"


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
                "a nonintegral source coefficient entered a pair chart")
        coefficient = int(coefficient)
        monomial = singular_monomial(exponent)
        if coefficient == 1:
            terms.append(monomial)
        elif coefficient == -1:
            terms.append("-" + monomial)
        else:
            terms.append(f"{coefficient}*{monomial}")
    return "+".join(terms).replace("+-", "-") or "0"


def coefficient_rows(first_variation, source, support):
    rows = {}
    for word in itertools.product(range(3), repeat=6):
        polynomial = first_variation.coefficient(source, support, word)
        if not polynomial:
            continue
        label = "".join(map(str, word))
        if word == (0,) * 6:
            polynomial = first_variation.poly_add(
                polynomial, first_variation.poly_constant(-1)
            )
        rows[label] = polynomial
    return rows


def ideal_expression(rows, labels=None):
    labels = tuple(rows) if labels is None else labels
    return ",".join(singular_polynomial(rows[label]) for label in labels)


def run_singular(code, timeout=180):
    result = subprocess.run(
        ("/usr/local/bin/Singular", "-q"),
        input=code,
        text=True,
        capture_output=True,
        check=False,
        timeout=timeout,
    )
    require(result.returncode == 0,
            f"Singular failed: {result.stderr or result.stdout}")
    return result.stdout


def pinned_transgressions(first_variation, source, base, missing, first):
    support = dict(base)
    support[parse_cell(first)] = first_variation.poly_variable(45)
    original = coefficient_rows(first_variation, source, support)
    labels = tuple(original)
    require(len(labels) == 411,
            f"the pinned source-row count changed for {first}")

    variables = ",".join(f"x{index}" for index in range(47))
    code = f"ring r=0,({variables}),dp; option(redSB);\n"
    code += "ideal I=" + ideal_expression(original, labels) + ";\n"
    code += "matrix L; ideal G=liftstd(I,L);\n"
    code += (
        "if(size(G)!=1 || G[1]!=2 || "
        "matrix(I)*L-matrix(G)!=0){ print(\"PIN_FAILED\"); }\n"
    )
    for second in missing:
        if second == first:
            continue
        enlarged = dict(support)
        enlarged[parse_cell(second)] = first_variation.poly_variable(46)
        rows = coefficient_rows(first_variation, source, enlarged)
        require(set(labels).issubset(rows),
                f"a pinned row disappeared for {first}+{second}")
        name = second.replace(":", "_")
        code += f"ideal J{name}=" + ideal_expression(rows, labels) + ";\n"
        code += (
            f"if(matrix(J{name})*L-matrix(G)!=0)"
            f"{{ print(\"TRANS {second}\"); }}\n"
        )
        code += f"kill J{name};\n"
    code += "quit;\n"
    output = run_singular(code)
    require("PIN_FAILED" not in output,
            f"the pinned exact lift failed for {first}")
    actual = tuple(
        line.split(" ", 1)[1]
        for line in output.splitlines() if line.startswith("TRANS ")
    )
    require(actual == EXPECTED_TRANSGRESSIONS[first],
            f"the pinned transgressions changed for {first}: {actual}")
    return actual


def canonical_pair(left, right):
    return tuple(sorted((left, right)))


def full_pair_standard_basis(first_variation, source, base, pair):
    support = dict(base)
    support[parse_cell(pair[0])] = first_variation.poly_variable(45)
    support[parse_cell(pair[1])] = first_variation.poly_variable(46)
    rows = coefficient_rows(first_variation, source, support)
    variables = ",".join(f"x{index}" for index in range(47))
    code = f"ring r=0,({variables}),dp; option(redSB);\n"
    code += "ideal I=" + ideal_expression(rows) + ";\n"
    code += "ideal G=std(I);\n"
    code += "print(\"UNIT\"); print(reduce(1,G)==0);\n"
    code += "print(\"SIZE\"); print(size(G));\n"
    code += "print(\"DIM\"); print(dim(G));\n"
    code += "print(\"BEGIN_BASIS\"); print(G); print(\"END_BASIS\");\n"
    code += "quit;\n"
    output = run_singular(code, timeout=60)
    lines = output.splitlines()
    unit = int(lines[lines.index("UNIT") + 1])
    size = int(lines[lines.index("SIZE") + 1])
    dimension = int(lines[lines.index("DIM") + 1])
    basis = output.split("BEGIN_BASIS\n", 1)[1].split(
        "\nEND_BASIS", 1
    )[0]
    return {
        "source_rows": len(rows),
        "source_terms": sum(len(value) for value in rows.values()),
        "unit": bool(unit),
        "basis_size": size,
        "dimension": dimension,
        "basis_sha256": sha256(basis.encode()).hexdigest(),
        "first_basis_polynomial": basis.splitlines()[0].removesuffix(","),
    }


def main():
    four_residual, dependency_digest = load_dependency()
    one_cell = four_residual.load_dependency()
    first_variation = one_cell.load_dependency()
    # The imported arithmetic is parameterized by these two globals.
    first_variation.VARIABLE_COUNT = 47
    first_variation.ZERO_EXPONENT = (0,) * 47
    diagonal_unit = first_variation.load_dependency()
    source, edges, _variables, base, _multipliers = first_variation.setup(
        diagonal_unit
    )
    universe = {
        (edge, colours)
        for edge in edges
        for colours in itertools.product(range(3), repeat=2)
    }
    missing_cells = tuple(sorted(universe - set(base)))
    missing = tuple(map(cell_label, missing_cells))
    require(len(missing) == 76,
            "the missing decorated-cell universe changed")

    directed = {
        first: pinned_transgressions(
            first_variation, source, base, missing, first
        )
        for first in RESIDUAL
    }
    require(sum(map(len, directed.values())) == 86,
            "the directed transgression count changed")
    critical = tuple(sorted({
        canonical_pair(first, second)
        for first, seconds in directed.items() for second in seconds
    }))
    require(len(critical) == 80,
            "the unordered critical-pair count changed")

    pair_audits = {}
    for pair in critical:
        key = "+".join(pair)
        pair_audits[key] = full_pair_standard_basis(
            first_variation, source, base, pair
        )
    proper = {
        key: audit for key, audit in pair_audits.items()
        if not audit["unit"]
    }
    require(set(proper) == set(EXPECTED_PROPER),
            f"the proper critical-pair ideals changed: {tuple(proper)}")
    for key, expected in EXPECTED_PROPER.items():
        audit = proper[key]
        require(audit["basis_size"] == expected["basis_size"],
                f"the basis size changed for {key}: {audit}")
        if expected["dimension"] != -1:
            require(audit["dimension"] == expected["dimension"],
                    f"the dimension changed for {key}: {audit}")
        if expected["basis_sha256"] != "TO_BE_FILLED":
            require(audit["basis_sha256"] == expected["basis_sha256"],
                    f"the basis changed for {key}: {audit}")
        require(audit["first_basis_polynomial"] == "x45-x46",
                f"the first basis polynomial changed for {key}: {audit}")
    require(sum(audit["unit"] for audit in pair_audits.values()) == 76,
            "the critical-pair unit count changed")

    ledger = {
        "dependency": {"path": DEPENDENCY,
                       "sha256": dependency_digest},
        "pinned_lifts": {
            "first_cells": list(RESIDUAL),
            "second_cells_per_lift": 75,
            "preserved_directed": 214,
            "transgressing_directed": 86,
            "transgressions": {
                first: list(seconds) for first, seconds in directed.items()
            },
        },
        "critical_pair_ideals": {
            "unordered_pairs": len(critical),
            "unit_ideals": 76,
            "proper_ideals": proper,
            "source_row_histogram": dict(sorted(Counter(
                audit["source_rows"] for audit in pair_audits.values()
            ).items())),
            "source_term_histogram": dict(sorted(Counter(
                audit["source_terms"] for audit in pair_audits.values()
            ).items())),
        },
        "verdict": (
            "among the 80 unordered pairs on which one of the four pinned "
            "one-cell source lifts changes, 76 full top ideals are unit "
            "and exactly four same-edge 10/20 pairs remain proper"
        ),
        "scope": (
            "the four pinned residual source certificates and their 80 "
            "transgressing critical pairs; proper means a genuine complex "
            "top packet, not a rational point and not yet satisfaction of "
            "the four one-bad response equations"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"pinned-lift critical-pair ledger changed: {digest}")
    print("N=8 Segre-K4 pinned-lift critical pairs: PASS")
    print("directed lifts: 300 = 214 preserved + 86 transgressing")
    print("unordered critical pairs: 80 = 76 unit + 4 proper")
    for key, audit in proper.items():
        print(f"{key}: dim {audit['dimension']}, {audit['basis_size']} rows, "
              f"{audit['basis_sha256']}")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
