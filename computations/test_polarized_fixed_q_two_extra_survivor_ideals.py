#!/usr/bin/env python3
"""Exact saturated ideals for the 16 two-extra projective survivors.

Discovery only.  The same sparse z remains a polarized preimage for all
cross-debt-free pairs e,f.  Projective singleton closure handles 3944/3960;
this script reconstructs every coordinate equation for the remaining 16,
saturates by t*u, and asks Singular for the exact characteristic-zero ideal.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import combinations
import shutil
import subprocess
import time

from explore_polarized_fixed_q_two_extra_frontier import cross_debt
from explore_polarized_fixed_q_two_extra_projective_closure import closes, forms
from verify_polarized_eight_site_fixed_q_one_extra_pair_cap_obstruction import (
    beta_expression,
    singular_ring_variables,
)
from verify_polarized_eight_site_single_invisible_cell_projective_closure_independent import (
    ALL_CELLS,
    COLOURS,
    DELTA_WORDS,
    polarized_derivative,
)


TAG_MONOMIAL = {0: "", 1: "t", 2: "u", 3: "t*u"}


def append_term(terms, coefficient, factors):
    pieces = []
    if coefficient != 1:
        pieces.append(str(coefficient))
    pieces.extend(factor for factor in factors if factor)
    terms.append("*".join(pieces) if pieces else "1")


def full_program(left, right):
    f, q4 = forms(left, right)
    words = sorted(set(f) | set(q4) | set(DELTA_WORDS))
    equations = []
    for word in words:
        terms = []
        for (edge, tag), coefficient in sorted(f.get(word, {}).items()):
            append_term(terms, 4 * coefficient,
                        (TAG_MONOMIAL[tag], beta_expression(edge)))
        for tag, coefficient in sorted(q4.get(word, {}).items()):
            append_term(terms, 4 * coefficient,
                        ("a", TAG_MONOMIAL[tag]))
        if word in DELTA_WORDS:
            terms.append("-1")
        if terms:
            equations.append("+".join(terms))
    equations.append("v*t*u-1")
    variables = singular_ring_variables(include_parameter=False)
    variables += ["a", "t", "u", "v"]
    program = (
        f"ring r=0,({','.join(variables)}),dp;\n"
        f"ideal I={','.join(equations)};\n"
        "option(redSB);\nideal G=std(I);\n"
        'print("BASIS_SIZE");\nprint(size(G));\n'
        'print("BASIS_FIRST");\nprint(G[1]);\n'
    )
    return program, len(equations), len(variables)


def run_job(singular, pair):
    program, equation_count, variable_count = full_program(*pair)
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
    return pair, size, first, equation_count, variable_count, elapsed


def main():
    singular = shutil.which("Singular")
    if singular is None:
        raise SystemExit("Singular required")
    invisible = tuple(cell for cell in ALL_CELLS if not polarized_derivative(cell))
    compatible = tuple(
        pair for pair in combinations(invisible, 2) if not cross_debt(*pair)
    )
    survivors = tuple(pair for pair in compatible if not closes(*pair)[0])
    assert len(compatible) == 3960
    assert len(survivors) == 16

    start = time.monotonic()
    outputs = []
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {pool.submit(run_job, singular, pair): pair for pair in survivors}
        for future in as_completed(futures):
            outputs.append(future.result())
    for pair, size, first, equations, variables, elapsed in sorted(outputs):
        print(pair, "basis", size, first, "equations", equations,
              "variables", variables, "seconds", f"{elapsed:.3f}")
    unit = [output for output in outputs if output[1] == output[2] == "1"]
    print("two-extra survivor ideals unit:", len(unit), "/", len(outputs))
    print("parallel wall seconds", f"{time.monotonic() - start:.3f}")


if __name__ == "__main__":
    main()
