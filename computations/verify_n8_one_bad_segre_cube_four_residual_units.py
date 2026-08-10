#!/usr/bin/env python3
"""Close the four residual one-cell Segre--K4 deformations over Q.

The degree-filtered coefficient identities leave four endpoint-star cells.
For each cell, this checker builds every nonzero coefficient of q^[3]-X0
and asks Singular for a source lift.  The returned integral combination is
the constant 2, so each chart is the unit ideal in characteristic zero.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import itertools
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DEPENDENCY = (
    "computations/verify_n8_one_bad_segre_cube_one_cell_closure.py"
)
DEPENDENCY_SHA256 = (
    "a28f2b2b8ddc3f814d8f2a32cbc3772cbea9d92ace94e12d9a8a3ab440921c49"
)
EXPECTED_LIFT_SHA256 = {
    "02:20": "b1e635f5bb41b6b2fd4a6d2b9852ee8cb2d121fd3ff639b4388b3fab625ce468",
    "03:10": "b25d11cac74ddcc5a0e70a2336402f261fc07480fa7d43b156302cdb2ec8d22b",
    "04:20": "0b40608c99cd7deeb0047b578b882b2df238945a27c9cb26d39f2b44cb973e61",
    "05:10": "47d80be6e12e7b245a46f6523b76db2f9aa84e2c50339f40859282dfda024083",
}
EXPECTED_LEDGER_SHA256 = (
    "b3f7c7a6aef53d266390b6e90da85b5df33b67cba83280b45e4e75ec2501ec55"
)
RESIDUAL = ("02:20", "03:10", "04:20", "05:10")


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_dependency():
    path = ROOT / DEPENDENCY
    actual = sha256(path.read_bytes()).hexdigest()
    require(actual == DEPENDENCY_SHA256,
            f"dependency changed: {DEPENDENCY}: {actual}")
    spec = spec_from_file_location("one_cell", path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_cell(label):
    return ((int(label[0]), int(label[1])),
            (int(label[3]), int(label[4])))


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
                "a nonintegral source coefficient entered the chart")
        coefficient = int(coefficient)
        monomial = singular_monomial(exponent)
        if coefficient == 1:
            terms.append(monomial)
        elif coefficient == -1:
            terms.append("-" + monomial)
        else:
            terms.append(f"{coefficient}*{monomial}")
    return "+".join(terms).replace("+-", "-") or "0"


def build_generators(first_variation, source, variables, base, cell_label):
    support = dict(base)
    support[parse_cell(cell_label)] = variables[45]
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
    require(len(generators) == 411,
            f"the source-row count for {cell_label} changed")
    require(term_count == 901,
            f"the source-term count for {cell_label} changed")
    require(labels[0] == "000000",
            "the unary row stopped being the first generator")
    return labels, generators, term_count


def singular_program(generators):
    variables = ",".join(f"x{index}" for index in range(46))
    code = f"ring r=0,({variables}),dp; option(redSB);\n"
    code += "ideal I=" + ",".join(generators) + ";\n"
    code += "matrix L; ideal G=liftstd(I,L);\n"
    code += (
        "if(size(G)!=1 || G[1]!=2){ print(\"UNIT_SHAPE_FAILED\"); }\n"
    )
    code += (
        "if(matrix(I)*L-matrix(G)!=0){ print(\"SOURCE_LIFT_FAILED\"); }\n"
    )
    code += "int i; int nz=0;\n"
    code += (
        "for(i=1;i<=nrows(L);i++){ if(L[i,1]!=0){ nz=nz+1; } }\n"
    )
    code += "print(\"NONZERO\"); print(nz);\n"
    code += "print(\"ROWS\");\n"
    code += (
        "for(i=1;i<=nrows(L);i++){ if(L[i,1]!=0){ print(i); } }\n"
    )
    code += "print(\"BEGIN_LIFT\"); print(L); print(\"END_LIFT\");\n"
    code += "quit;\n"
    return code


def marker_value(output, marker):
    lines = output.splitlines()
    index = lines.index(marker)
    return lines[index + 1]


def audit_chart(first_variation, source, variables, base, cell_label):
    labels, generators, term_count = build_generators(
        first_variation, source, variables, base, cell_label
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
            f"Singular failed on {cell_label}: "
            f"{result.stderr or result.stdout}")
    require("UNIT_SHAPE_FAILED" not in result.stdout,
            f"the unit shape failed on {cell_label}")
    require("SOURCE_LIFT_FAILED" not in result.stdout,
            f"the source lift failed on {cell_label}")
    nonzero = int(marker_value(result.stdout, "NONZERO"))
    rows_text = result.stdout.split("ROWS\n", 1)[1].split(
        "BEGIN_LIFT\n", 1
    )[0]
    active_rows = tuple(map(int, rows_text.split()))
    require(len(active_rows) == nonzero,
            f"the active-row count failed on {cell_label}")
    lift = result.stdout.split("BEGIN_LIFT\n", 1)[1].split(
        "\nEND_LIFT", 1
    )[0]
    lift_digest = sha256(lift.encode()).hexdigest()
    expected = EXPECTED_LIFT_SHA256[cell_label]
    if expected != "TO_BE_FILLED":
        require(lift_digest == expected,
                f"the source lift changed on {cell_label}: {lift_digest}")
    active_labels = [labels[index - 1] for index in active_rows]
    expected_counts = {"02:20": 14, "03:10": 15,
                       "04:20": 14, "05:10": 15}
    require(nonzero == expected_counts[cell_label],
            f"the active source core changed on {cell_label}")
    return {
        "source_rows": len(generators),
        "source_terms": term_count,
        "unit_constant": 2,
        "active_rows": list(active_rows),
        "active_labels": active_labels,
        "active_row_count": nonzero,
        "lift_sha256": lift_digest,
    }


def main():
    one_cell = load_dependency()
    first_variation = one_cell.load_dependency()
    diagonal_unit = first_variation.load_dependency()
    source, _edges, variables, base, _multipliers = first_variation.setup(
        diagonal_unit
    )
    audits = {
        cell: audit_chart(first_variation, source, variables, base, cell)
        for cell in RESIDUAL
    }
    ledger = {
        "dependency": {"path": DEPENDENCY, "sha256": DEPENDENCY_SHA256},
        "residual_units": audits,
        "consequence": (
            "all 76 one-cell deformations of the full diagonal-carrier "
            "Segre-K4 chart are top-empty over characteristic zero"
        ),
        "scope": (
            "one added decorated coordinate at a time; simultaneous "
            "multi-coordinate deformations are not excluded"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"four-residual ledger changed: {digest}")
    print("N=8 Segre-K4 four residual units: PASS")
    print("four residual charts: integral source lift to constant 2")
    print("consequence: all 76 one-cell deformations are top-empty")
    for cell, audit in audits.items():
        print(f"{cell}: {audit['active_row_count']} rows, "
              f"lift {audit['lift_sha256']}")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
