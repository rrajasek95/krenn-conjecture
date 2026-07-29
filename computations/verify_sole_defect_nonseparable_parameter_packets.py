#!/usr/bin/env python3
"""Exact common-power ideals for the twelve full-packet parameter orbits.

After removal of every support with a locally separable SDR, 145 of the 157
remaining packet orbits have all lift coefficients normalizable to one.  In
each of the other twelve, exactly one incident packet has all four good arms.
Good-site field rescaling leaves one nonzero invariant ``mu``; we normalize
the incident lift and three arms to one and put ``mu`` on the fourth arm.

The qF=0 equations are row-reduced over QQ(mu), while explicitly checking
that every inverted pivot is a Laurent unit c*mu^k.  Thus the reduction is
valid over QQ[mu,mu^-1].  The latter ring is represented in Singular by
adjoining ``z`` and the equation mu*z-1.  A unit ideal therefore rules out
the whole nonzero parameter family, including every specialization.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
from itertools import combinations, product
import shutil
import subprocess
import time

import sympy as sp

from explore_sole_defect_nonseparable_packet_orbits import (
    TYPES,
    arm_count,
    nonseparable_only_representatives,
)
from verify_sole_defect_distinct_common_power import (
    U,
    add,
    local_data,
    multiply,
    pure_lift,
    q_cells,
)


MU = sp.Symbol("mu")
Z = "z"

EXPECTED_COMBINED = {
    "coincident_k2": "ad85e0d56bacd618338483baabb9da62bd427960e6feb8548fafaebc31537874",
    "rank1_k2": "3c69d3157bd1ea0a09d2876531ef6faeab5aa53b5edc235ad6ca9a4f0f794700",
}


def representatives(name):
    killed_size = 1 if name.endswith("_k1") else 2
    return tuple(
        families
        for families in nonseparable_only_representatives(name)
        if max(arm_count(families[r]) for r in range(killed_size)) == 4
    )


def weighted_families(families):
    """Put the sole packet invariant on a deterministic fourth arm."""
    full_fields = tuple(
        field for field, family in enumerate(families) if arm_count(family) == 4
    )
    assert len(full_fields) == 1
    full_field = full_fields[0]
    full_family = families[full_field]
    parameter_pair = max(pair for pair in full_family if 0 not in pair)
    return tuple(
        tuple(
            (pair, MU if field == full_field and pair == parameter_pair else sp.Integer(1))
            for pair in family
        )
        for field, family in enumerate(families)
    ), full_field, parameter_pair


def f_coefficients(weighted, dims, bad_vectors):
    by_support = Counter()
    for colour, family in enumerate(weighted):
        for pair, lift_coefficient in family:
            for local_word, coefficient in pure_lift(
                pair, colour, dims, bad_vectors
            ).items():
                support = tuple(site for site, coordinate in local_word)
                word = tuple(coordinate for site, coordinate in local_word)
                by_support[support, word] += lift_coefficient * coefficient
    return {
        key: sp.cancel(value) for key, value in by_support.items()
        if sp.cancel(value) != 0
    }


def qf_rows(weighted, dims, bad_vectors, cell_index):
    rows = {}
    for colour, family in enumerate(weighted):
        for pair, lift_coefficient in family:
            lift = pure_lift(pair, colour, dims, bad_vectors)
            u, v = pair
            for cu in range(dims[u]):
                for cv in range(dims[v]):
                    column = cell_index[(pair, cu, cv)]
                    for local_word, coefficient in lift.items():
                        full = dict(local_word)
                        full[u], full[v] = cu, cv
                        word = tuple(full[site] for site in U)
                        row = rows.setdefault(word, {})
                        row[column] = sp.cancel(
                            row.get(column, 0)
                            + lift_coefficient * coefficient
                        )
    return tuple(
        {column: value for column, value in row.items() if value != 0}
        for row in rows.values() if any(value != 0 for value in row.values())
    )


def laurent_unit(expression):
    """Return whether expression is a nonzero rational times a power of mu."""
    expression = sp.cancel(expression)
    if expression == 0:
        return False
    numerator, denominator = sp.fraction(expression)
    for part in (numerator, denominator):
        coefficient, exponent = part.as_coeff_exponent(MU)
        if not coefficient.is_Rational or exponent < 0:
            return False
        if sp.expand(part - coefficient * MU**exponent) != 0:
            return False
    return True


def sparse_laurent_rref(source_rows):
    """RREF using only divisions by units of QQ[mu,mu^-1]."""
    pivots = {}
    inverted = []
    for source in source_rows:
        row = {
            column: sp.cancel(value)
            for column, value in source.items() if sp.cancel(value) != 0
        }
        for column in sorted(pivots):
            if column not in row:
                continue
            scale = row[column]
            for key, value in pivots[column].items():
                updated = sp.cancel(row.get(key, 0) - scale * value)
                if updated == 0:
                    row.pop(key, None)
                else:
                    row[key] = updated
        if not row:
            continue
        unit_columns = tuple(
            column for column in sorted(row) if laurent_unit(row[column])
        )
        assert unit_columns, (
            "qF reduction would require a non-Laurent pivot",
            tuple(sorted(row.items())),
        )
        column = unit_columns[0]
        scale = row[column]
        inverted.append(sp.cancel(scale))
        row = {key: sp.cancel(value / scale) for key, value in row.items()}
        for old in pivots.values():
            if column not in old:
                continue
            scale = old[column]
            for key, value in row.items():
                updated = sp.cancel(old.get(key, 0) - scale * value)
                if updated == 0:
                    old.pop(key, None)
                else:
                    old[key] = updated
        pivots[column] = row
        pivots = dict(sorted(pivots.items()))
    assert all(laurent_unit(scale) for scale in inverted)
    return pivots, tuple(inverted)


def laurent_string(expression):
    """Render a Laurent polynomial as a QQ[mu,z]/(mu*z-1) expression."""
    expression = sp.cancel(expression)
    numerator, denominator = sp.fraction(expression)
    coefficient, exponent = denominator.as_coeff_exponent(MU)
    assert coefficient.is_Rational and exponent >= 0
    assert sp.expand(denominator - coefficient * MU**exponent) == 0, expression
    polynomial = sp.expand(numerator / coefficient)
    rendered = sp.sstr(polynomial).replace("**", "^")
    if exponent:
        rendered = f"({rendered})*({Z}^{exponent})"
    return rendered


def linear_expression(terms):
    pieces = []
    for variable, coefficient in terms:
        coefficient = sp.cancel(coefficient)
        if coefficient == 1:
            pieces.append(variable)
        elif coefficient == -1:
            pieces.append(f"-({variable})")
        else:
            pieces.append(f"({laurent_string(coefficient)})*({variable})")
    return "0" if not pieces else "(" + ")+(".join(pieces) + ")"


def build(case, name, kind):
    families = representatives(name)[case]
    weighted, full_field, parameter_pair = weighted_families(families)
    dims, bad_vectors = local_data(kind)
    cells = q_cells(dims)
    cell_index = {cell: index for index, cell in enumerate(cells)}
    rows = qf_rows(weighted, dims, bad_vectors, cell_index)
    pivots, inverted = sparse_laurent_rref(rows)
    # This stronger audit is what makes the specialization claim uniform:
    # no exceptional factor other than the already excluded mu=0 is inverted.
    assert set(inverted) <= {sp.Integer(1), MU}
    free = tuple(index for index in range(len(cells)) if index not in pivots)
    variables = tuple(f"t{i}" for i in range(len(free)))
    free_variable = dict(zip(free, variables))
    expressions = {}
    for column, cell in enumerate(cells):
        if column in free_variable:
            expressions[cell] = free_variable[column]
        else:
            row = pivots[column]
            expressions[cell] = linear_expression(tuple(
                (free_variable[key], -value)
                for key, value in row.items() if key != column
            ))

    target = f_coefficients(weighted, dims, bad_vectors)
    generators = ["(mu)*(z)-1"]
    matchings = ((0, 1, 2, 3), (0, 2, 1, 3), (0, 3, 1, 2))
    for sites in combinations(U, 4):
        ranges = tuple(range(dims[site]) for site in sites)
        for word in product(*ranges):
            terms = []
            for i, j, k, l in matchings:
                left_sites = tuple(sorted((sites[i], sites[j])))
                right_sites = tuple(sorted((sites[k], sites[l])))
                left_word = (
                    (word[i], word[j]) if sites[i] < sites[j]
                    else (word[j], word[i])
                )
                right_word = (
                    (word[k], word[l]) if sites[k] < sites[l]
                    else (word[l], word[k])
                )
                terms.append(multiply(
                    expressions[(left_sites, *left_word)],
                    expressions[(right_sites, *right_word)],
                ))
            polynomial = add(*terms)
            constant = target.get((sites, word), 0)
            if constant != 0:
                polynomial = add(polynomial, f"-({laurent_string(constant)})")
            if polynomial != "0":
                generators.append(polynomial)
    return (
        families, full_field, parameter_pair, dims, cells, rows, pivots,
        inverted, variables, tuple(generators),
    )


def ledger_digest(name, families, full_field, parameter_pair, cells, rows,
                  pivots, inverted, generators):
    digest = hashlib.sha256()
    digest.update(repr((name, families, full_field, parameter_pair, cells)).encode("ascii"))
    digest.update(b"\nROWS\n")
    for row in rows:
        digest.update(repr(tuple((key, str(value)) for key, value in sorted(row.items()))).encode("ascii"))
        digest.update(b"\n")
    digest.update(b"RREF\n")
    for pivot, row in pivots.items():
        digest.update(repr((pivot, tuple((key, str(value)) for key, value in sorted(row.items())))).encode("ascii"))
        digest.update(b"\n")
    digest.update(repr(tuple(map(str, inverted))).encode("ascii"))
    digest.update(b"\nGENERATORS\n")
    for generator in generators:
        digest.update(generator.encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def run(case, name, kind, timeout, run_ideal=True):
    (
        families, full_field, parameter_pair, dims, cells, rows, pivots,
        inverted, variables, generators,
    ) = build(case, name, kind)
    digest = ledger_digest(
        name, families, full_field, parameter_pair, cells, rows, pivots,
        inverted, generators,
    )
    status = "SKIPPED"
    elapsed = 0.0
    stderr = ""
    if run_ideal:
        executable = shutil.which("Singular")
        if executable is None:
            raise SystemExit("Singular is required")
        ring_variables = variables + ("mu", Z)
        program = (
            f"ring r=0,({','.join(ring_variables)}),dp;\n"
            f"ideal I={','.join(generators)};\n"
            "ideal G=slimgb(I);\n"
            'print("SIZE");print(size(G));print("FIRST");print(G[1]);\n'
        )
        started = time.monotonic()
        result = subprocess.run(
            (executable, "-q"), input=program, text=True, capture_output=True,
            timeout=timeout,
        )
        elapsed = time.monotonic() - started
        stderr = result.stderr
        output = tuple(line.strip() for line in result.stdout.splitlines() if line.strip())
        status = "ERROR"
        if result.returncode == 0 and "SIZE" in output and "FIRST" in output:
            size = output[output.index("SIZE") + 1]
            first = output[output.index("FIRST") + 1]
            status = "UNIT" if size == first == "1" else f"NONUNIT:{size}:{first}"
    return {
        "case": case,
        "type": name,
        "families": families,
        "full_field": full_field,
        "parameter_pair": parameter_pair,
        "dims": dims,
        "cells": len(cells),
        "rows": len(rows),
        "rank": len(pivots),
        "nullity": len(variables),
        "inverted_pivots": tuple(map(str, inverted)),
        "generators": len(generators),
        "sha256": digest,
        "status": status,
        "seconds": elapsed,
        "stderr": stderr,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", choices=("coincident_k2", "rank1_k2"), action="append")
    parser.add_argument("--case", type=int, action="append")
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument("--ledger-only", action="store_true")
    args = parser.parse_args()

    selected = set(args.type) if args.type else None
    total = 0
    for name, kind, killed in TYPES:
        if name not in {"coincident_k2", "rank1_k2"}:
            continue
        if selected is not None and name not in selected:
            continue
        reps = representatives(name)
        total += len(reps)
        print(name, "parameter residual orbit count:", len(reps), flush=True)
        combined = hashlib.sha256()
        for case in args.case or range(len(reps)):
            result = run(case, name, kind, args.timeout, not args.ledger_only)
            print(result, flush=True)
            if not args.ledger_only:
                assert result["status"] == "UNIT", result
            combined.update(f'{case}:{result["sha256"]}\n'.encode("ascii"))
        combined_digest = combined.hexdigest()
        print(name, "combined ledger sha256:", combined_digest, flush=True)
        if not args.case:
            assert combined_digest == EXPECTED_COMBINED[name]
    if not args.type and not args.case:
        assert total == 12
    print("sole-defect parameter nonseparable packet ideals: PASS")


if __name__ == "__main__":
    main()
