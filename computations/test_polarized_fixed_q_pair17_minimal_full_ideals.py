#!/usr/bin/env python3
"""Test the four minimal support-only survivors in the full 17 block.

Discovery only.  For each minimal open support from the projective singleton
closure, build every pair-cap coordinate equation with independent nonzero
cell parameters and ask Singular for the saturated characteristic-zero
ideal.  No result from this script is promoted without a separate audit.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
import shutil
import subprocess
import time

from verify_polarized_eight_site_fixed_q_one_extra_pair_cap_obstruction import (
    COLOURS,
    Q_CELLS,
    beta_expression,
    cell_word,
    divided_power,
    gram_coordinate_forms,
    literal_polynomial,
    multiply,
    singular_ring_variables,
)


CASES = {
    "00_12": ((1, 7, 0, 0), (1, 7, 1, 2)),
    "01_02_12": ((1, 7, 0, 1), (1, 7, 0, 2), (1, 7, 1, 2)),
    "01_22": ((1, 7, 0, 1), (1, 7, 2, 2)),
    "00_02_22": ((1, 7, 0, 0), (1, 7, 0, 2), (1, 7, 2, 2)),
    "full_block": tuple(
        (1, 7, left_colour, right_colour)
        for left_colour in COLOURS for right_colour in COLOURS
    ),
}


def coordinate_program(cells, saturate=True):
    q = literal_polynomial(Q_CELLS)
    q2 = divided_power(q, 2)
    q3 = divided_power(q, 3)
    q4 = divided_power(q, 4)
    old_forms = gram_coordinate_forms(q3)

    variations = []
    for cell in cells:
        e = {cell_word(*cell): Fraction(1)}
        variations.append((
            gram_coordinate_forms(multiply(e, q2)),
            multiply(e, q3),
        ))

    delta_words = {(colour,) * 8 for colour in COLOURS}
    words = set(old_forms) | set(q4) | delta_words
    for fvar, qvar in variations:
        words.update(fvar)
        words.update(qvar)

    equations = []
    for word in sorted(words):
        terms = []
        for entry, coefficient in sorted(old_forms.get(word, {}).items()):
            terms.append(f"{4 * coefficient}*{beta_expression(entry)}")
        for index, (fvar, _qvar) in enumerate(variations):
            for entry, coefficient in sorted(fvar.get(word, {}).items()):
                terms.append(
                    f"{4 * coefficient}*x{index}*{beta_expression(entry)}"
                )
        if word in q4:
            terms.append(f"{4 * int(q4[word])}*a")
        for index, (_fvar, qvar) in enumerate(variations):
            if word in qvar:
                terms.append(f"{4 * int(qvar[word])}*a*x{index}")
        if word in delta_words:
            terms.append("-1")
        if terms:
            equations.append("+".join(terms))

    parameter_names = [f"x{index}" for index in range(len(cells))]
    if saturate:
        equations.append("u*" + "*".join(parameter_names) + "-1")
    variables = singular_ring_variables(include_parameter=False)
    variables += ["a"] + parameter_names + (["u"] if saturate else [])
    program = (
        f"ring r=0,({','.join(variables)}),dp;\n"
        f"ideal I={','.join(equations)};\n"
        "option(redSB);\n"
        "ideal G=std(I);\n"
        'print("BASIS_SIZE");\nprint(size(G));\n'
        'print("BASIS_FIRST");\nprint(G[1]);\n'
    )
    return program, len(equations), len(variables)


def main():
    singular = shutil.which("Singular")
    if singular is None:
        raise SystemExit("Singular required")
    for name, cells in CASES.items():
        program, equations, variables = coordinate_program(cells)
        start = time.monotonic()
        try:
            result = subprocess.run(
                [singular, "-q"], input=program, text=True,
                capture_output=True, check=True, timeout=600,
            )
        except subprocess.TimeoutExpired:
            print(name, "TIMEOUT", "equations", equations, "variables", variables)
            continue
        elapsed = time.monotonic() - start
        if result.stderr.strip():
            raise AssertionError(result.stderr)
        lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        size = lines[lines.index("BASIS_SIZE") + 1]
        first = lines[lines.index("BASIS_FIRST") + 1]
        print(name, "basis", size, first, "equations", equations,
              "variables", variables, "seconds", f"{elapsed:.3f}")

    cells = CASES["full_block"]
    program, equations, variables = coordinate_program(cells, saturate=False)
    start = time.monotonic()
    result = subprocess.run(
        [singular, "-q"], input=program, text=True,
        capture_output=True, check=True, timeout=600,
    )
    elapsed = time.monotonic() - start
    if result.stderr.strip():
        raise AssertionError(result.stderr)
    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    size = lines[lines.index("BASIS_SIZE") + 1]
    first = lines[lines.index("BASIS_FIRST") + 1]
    print("full_block_unrestricted", "basis", size, first,
          "equations", equations, "variables", variables,
          "seconds", f"{elapsed:.3f}")


if __name__ == "__main__":
    main()
