#!/usr/bin/env python3
"""Exact common-power audit for six pure lifts on two physical pairs.

Let ``P != Q`` be missing pairs on six sites and put

    F = sum_c (lambda_c E_c(P) + mu_c E_c(Q)),

with all six coefficients nonzero.  Independent target-axis rescalings
normalize the coefficients to one.  Up to S_6, P and Q are adjacent or
disjoint.  For each case this script:

* constructs every coefficient of the necessary equation q F = 0;
* computes an exact rational RREF and verifies a full kernel basis;
* substitutes that kernel into all 1,215 coefficients of q^[2] - F; and
* asks Singular for the unsaturated affine ideal over QQ.

The q variables are all 15 * 3 * 3 endpoint-ordered local cells.  Thus no
monomial, pure-block, support, nonvanishing, or genericity assumption is
made on q.  Independent five-term (2,2,1) and four-term (2,1,1) controls
use the same unrestricted construction.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import combinations, product
import shutil
import subprocess
import time


U = tuple(range(6))
COLOURS = tuple(range(3))
EDGES = tuple(combinations(U, 2))
EDGE_INDEX = {pair: index for index, pair in enumerate(EDGES)}
N_Q_CELL = len(EDGES) * len(COLOURS) ** 2
CASES = {
    "adjacent": ((0, 1), (0, 2)),
    "disjoint": ((0, 1), (2, 3)),
}
EXPECTED = {
    ("211", "adjacent"): {
        "row_count": 33,
        "rank": 18,
        "nullity": 117,
        "generator_count": 1215,
        "sha256": "15f664ff5212765ba9d67b722b795b66fc6fee7be2af073fb5ba0b72b6a38e3d",
    },
    ("211", "disjoint"): {
        "row_count": 35,
        "rank": 18,
        "nullity": 117,
        "generator_count": 1215,
        "sha256": "b69d746581794a828838c0fb514dcd67a7a0100adf188e8add762d6cd2a06a0e",
    },
    ("221", "adjacent"): {
        "row_count": 39,
        "rank": 18,
        "nullity": 117,
        "generator_count": 1215,
        "sha256": "65aa8dcdfbbeb883c262981c4b06c77b84764d945444b5c9a268da788bccab81",
    },
    ("221", "disjoint"): {
        "row_count": 43,
        "rank": 18,
        "nullity": 117,
        "generator_count": 1215,
        "sha256": "77ce7cebc198aa491f2aa88054909f22b19a391a30da23c0ae4955e6ddd87d56",
    },
    ("222", "adjacent"): {
        "row_count": 45,
        "rank": 18,
        "nullity": 117,
        "generator_count": 1215,
        "sha256": "038c784c558b61d11d87e8e77753c4c63c460041aef8e1d3e2c7e1a541f2e02d",
    },
    ("222", "disjoint"): {
        "row_count": 51,
        "rank": 18,
        "nullity": 117,
        "generator_count": 1215,
        "sha256": "1c2fbc31726f15bb2ff1be6c0db53330f6181293279a61f3337beb2ab8e3b8e7",
    },
}


def terms_for(pairs, profile):
    if profile == "222":
        return tuple((pair, colour) for pair in pairs for colour in COLOURS)
    if profile == "221":
        # The exact special case used in the aligned-three-field reduction:
        # colours 0 and 1 occupy both P,Q; colour 2 occupies Q only.
        return tuple(
            (pair, colour) for pair in pairs for colour in (0, 1)
        ) + ((pairs[1], 2),)
    if profile == "211":
        # One colour occupies both pairs; the two singleton colours must
        # occupy different pairs (same-pair singleton collisions cannot
        # satisfy the response table in the aligned application).
        return (
            (pairs[0], 0), (pairs[1], 0),
            (pairs[0], 1), (pairs[1], 2),
        )
    raise ValueError(profile)


def q_index(pair, cu, cv):
    return 9 * EDGE_INDEX[pair] + 3 * cu + cv


def qf_rows(terms):
    """All sparse coefficient rows of qF=0, collecting collisions."""
    rows = {}
    for pair, colour in terms:
        u, v = pair
        for cu, cv in product(COLOURS, repeat=2):
            word = [colour] * len(U)
            word[u], word[v] = cu, cv
            row = rows.setdefault(tuple(word), {})
            column = q_index(pair, cu, cv)
            row[column] = row.get(column, Fraction(0)) + 1
    return tuple(row for row in rows.values() if row)


def sparse_rref(source_rows):
    """Return exact RREF as a pivot-column dictionary of sparse rows."""
    pivots = {}
    for source in source_rows:
        row = {
            column: Fraction(value)
            for column, value in source.items()
            if value
        }
        for column in sorted(pivots):
            if column not in row:
                continue
            scale = row[column]
            for key, value in pivots[column].items():
                row[key] = row.get(key, Fraction(0)) - scale * value
                if row[key] == 0:
                    del row[key]
        if not row:
            continue
        column = min(row)
        scale = row[column]
        row = {key: value / scale for key, value in row.items()}
        for old_row in pivots.values():
            if column not in old_row:
                continue
            old_scale = old_row[column]
            for key, value in row.items():
                old_row[key] = old_row.get(key, Fraction(0)) - old_scale * value
                if old_row[key] == 0:
                    del old_row[key]
        pivots[column] = row
        pivots = dict(sorted(pivots.items()))
    return pivots


def kernel_basis(pivots):
    free = tuple(column for column in range(N_Q_CELL) if column not in pivots)
    basis = []
    for column in free:
        vector = {column: Fraction(1)}
        for pivot, row in pivots.items():
            if column in row:
                vector[pivot] = -row[column]
        basis.append(vector)
    return free, tuple(basis)


def audit_kernel(terms):
    rows = qf_rows(terms)
    pivots = sparse_rref(rows)
    free, basis = kernel_basis(pivots)
    assert len(pivots) + len(basis) == N_Q_CELL
    for vector in basis:
        for row in rows:
            assert sum(
                value * vector.get(column, Fraction(0))
                for column, value in row.items()
            ) == 0
    return rows, pivots, free, basis


def fraction_string(value):
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    return f"({value.numerator}/{value.denominator})"


def linear_expression(terms):
    pieces = []
    for variable, coefficient in terms:
        coefficient = Fraction(coefficient)
        if not coefficient:
            continue
        if coefficient == 1:
            term = variable
        elif coefficient == -1:
            term = f"-({variable})"
        else:
            term = f"({fraction_string(coefficient)})*({variable})"
        pieces.append(term)
    return "0" if not pieces else "(" + ")+(".join(pieces) + ")"


def add(*terms):
    terms = tuple(term for term in terms if term != "0")
    if not terms:
        return "0"
    if len(terms) == 1:
        return terms[0]
    return "(" + ")+(".join(terms) + ")"


def multiply(left, right):
    if left == "0" or right == "0":
        return "0"
    return f"({left})*({right})"


def cell(values, u, v, cu, cv):
    if u < v:
        return values[(u, v), cu, cv]
    return values[(v, u), cv, cu]


def equations(terms):
    rows, pivots, free, basis = audit_kernel(terms)
    variables = tuple(f"t{index}" for index in range(len(free)))
    by_column = [[] for _ in range(N_Q_CELL)]
    for variable, vector in zip(variables, basis):
        for column, coefficient in vector.items():
            by_column[column].append((variable, coefficient))
    values = {}
    for pair in EDGES:
        for cu, cv in product(COLOURS, repeat=2):
            values[pair, cu, cv] = linear_expression(
                by_column[q_index(pair, cu, cv)]
            )

    target = Counter()
    for pair, colour in terms:
        sites = tuple(u for u in U if u not in pair)
        target[sites, (colour,) * 4] += 1

    matching_patterns = ((0, 1, 2, 3), (0, 2, 1, 3), (0, 3, 1, 2))
    generators = []
    for sites in combinations(U, 4):
        for colours in product(COLOURS, repeat=4):
            polynomial = add(*(
                multiply(
                    cell(values, sites[i], sites[j], colours[i], colours[j]),
                    cell(values, sites[k], sites[l], colours[k], colours[l]),
                )
                for i, j, k, l in matching_patterns
            ))
            constant = target[sites, colours]
            if constant:
                polynomial = add(polynomial, str(-constant))
            if polynomial != "0":
                generators.append(polynomial)
    return rows, pivots, variables, tuple(generators)


def ledger_digest(rows, pivots, generators):
    digest = hashlib.sha256()
    for row in rows:
        digest.update(repr(tuple(sorted(row.items()))).encode("ascii"))
        digest.update(b"\n")
    digest.update(b"RREF\n")
    for pivot, row in pivots.items():
        digest.update(repr((pivot, tuple(sorted(row.items())))).encode("ascii"))
        digest.update(b"\n")
    digest.update(b"GENERATORS\n")
    for generator in generators:
        digest.update(generator.encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def run(case, profile, timeout):
    pairs = CASES[case]
    terms = terms_for(pairs, profile)
    rows, pivots, variables, generators = equations(terms)
    digest = ledger_digest(rows, pivots, generators)
    executable = shutil.which("Singular")
    if executable is None:
        raise SystemExit("Singular is required")
    program = (
        f"ring r=0,({','.join(variables)}),dp;\n"
        f"ideal I={','.join(generators)};\n"
        "ideal G=slimgb(I);\n"
        'print("BASIS_SIZE"); print(size(G));\n'
        'print("BASIS_FIRST"); print(G[1]);\n'
    )
    started = time.monotonic()
    result = subprocess.run(
        (executable, "-q"), input=program, text=True, capture_output=True,
        timeout=timeout,
    )
    elapsed = time.monotonic() - started
    if result.returncode:
        status = "ERROR"
        detail = result.stderr
    else:
        lines = tuple(line.strip() for line in result.stdout.splitlines() if line.strip())
        try:
            size = lines[lines.index("BASIS_SIZE") + 1]
            first = lines[lines.index("BASIS_FIRST") + 1]
            status = "UNIT" if size == first == "1" else f"NONUNIT:{size}:{first}"
            detail = ""
        except (ValueError, IndexError):
            status = "MALFORMED"
            detail = result.stdout
    return {
        "case": case,
        "profile": profile,
        "pairs": pairs,
        "row_count": len(rows),
        "rank": len(pivots),
        "nullity": len(variables),
        "generator_count": len(generators),
        "sha256": digest,
        "status": status,
        "seconds": elapsed,
        "detail": detail,
    }


def audit_frozen_result(result):
    expected = EXPECTED[result["profile"], result["case"]]
    for key, value in expected.items():
        assert result[key] == value, (key, result[key], value)
    assert result["status"] == "UNIT", result


def audit_weight_normalization():
    """Every distinct pair-character pair has rank two on the site torus."""
    projected = {}
    for pair in EDGES:
        row = []
        for variable_site in range(5):
            coefficient = int(variable_site in pair)
            if 5 in pair:
                coefficient -= 1
            row.append(coefficient)
        projected[pair] = tuple(row)
    checked = 0
    for left, right in combinations(EDGES, 2):
        minors = tuple(
            projected[left][a] * projected[right][b]
            - projected[left][b] * projected[right][a]
            for a, b in combinations(range(5), 2)
        )
        assert any(minors)
        checked += 1
    assert checked == 105
    return checked


def audit_pair_orbits():
    census = Counter(
        "adjacent" if set(left).intersection(right) else "disjoint"
        for left, right in combinations(EDGES, 2)
    )
    assert census == Counter({"adjacent": 60, "disjoint": 45})
    return census


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=tuple(CASES), action="append")
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument("--skip-two-two-one-controls", action="store_true")
    parser.add_argument("--skip-two-one-one-controls", action="store_true")
    args = parser.parse_args()

    checked = audit_weight_normalization()
    print("distinct pair-character ranks checked:", checked)
    print("two-distinct-pair orbit census:", dict(sorted(audit_pair_orbits().items())))
    selected = args.case or list(CASES)
    if not args.skip_two_two_one_controls:
        for case in selected:
            control = run(case, "221", args.timeout)
            print(
                "two-two-one control", control["case"], "pairs", control["pairs"],
                "qF rows/rank/nullity",
                f'{control["row_count"]}/{control["rank"]}/{control["nullity"]}',
                "q2 generators", control["generator_count"],
                "sha256", control["sha256"], control["status"],
                "seconds", f'{control["seconds"]:.3f}',
                flush=True,
            )
            if control["detail"]:
                print(control["detail"])
            audit_frozen_result(control)
    if not args.skip_two_one_one_controls:
        for case in selected:
            control = run(case, "211", args.timeout)
            print(
                "two-one-one control", control["case"], "pairs", control["pairs"],
                "qF rows/rank/nullity",
                f'{control["row_count"]}/{control["rank"]}/{control["nullity"]}',
                "q2 generators", control["generator_count"],
                "sha256", control["sha256"], control["status"],
                "seconds", f'{control["seconds"]:.3f}',
                flush=True,
            )
            if control["detail"]:
                print(control["detail"])
            audit_frozen_result(control)
    for case in selected:
        result = run(case, "222", args.timeout)
        print(
            result["case"], "pairs", result["pairs"],
            "qF rows/rank/nullity",
            f'{result["row_count"]}/{result["rank"]}/{result["nullity"]}',
            "q2 generators", result["generator_count"],
            "sha256", result["sha256"], result["status"],
            "seconds", f'{result["seconds"]:.3f}',
            flush=True,
        )
        if result["detail"]:
            print(result["detail"])
        audit_frozen_result(result)
    print("two-pair six-term common-power obstruction exact audit: PASS")


if __name__ == "__main__":
    main()
