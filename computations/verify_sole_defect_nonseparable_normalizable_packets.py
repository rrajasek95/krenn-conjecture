#!/usr/bin/env python3
"""Exact common-power ideals for coefficient-normalizable defect packets.

The packet census first removes every support admitting a locally separable
SDR.  This checker treats the remaining orbits in which every incident
packet has at most three good arms, so all nonzero lift coefficients can be
normalized to one by independent good-site field scalings.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
from itertools import combinations, product
import shutil
import subprocess
import time

from explore_sole_defect_nonseparable_packet_orbits import (
    TYPES,
    arm_count,
    nonseparable_only_representatives,
)
from verify_sole_defect_distinct_common_power import (
    U,
    add,
    linear_expression,
    local_data,
    multiply,
    q_cells,
    sparse_rref,
)
from verify_sole_defect_two_pair_common_power import f_coefficients, qf_rows


EXPECTED_COMBINED = {
    "circuit_k2": "0469cf5512cd43e33bb5d8a1c645fc35cae0a34ced35d5c2d627c453e96331aa",
    "coincident_k1": "c9db1b099b249d534ee94a3063f5c1fd5a4e55dbd49f2a92f68d388cd904a68e",
    "coincident_k2": "e97b5045642a2715e670cf503c24d0543b36bfe849966edd5a5bfe3e422eeddc",
    "rank1_k1": "97a703257591444e12fcc364ddf6e87e7c17b449b3199deefabc401b8169542d",
    "rank1_k2": "c31e02b0af67b5c10eedbdc91d21921a49b4897147a61a115a7722f1e4ec6aa3",
}


def representatives(name):
    killed_size = 1 if name.endswith("_k1") else 2
    return tuple(
        families
        for families in nonseparable_only_representatives(name)
        if max(arm_count(families[r]) for r in range(killed_size)) <= 3
    )


def build(case, name, kind):
    families = representatives(name)[case]
    dims, bad_vectors = local_data(kind)
    cells = q_cells(dims)
    cell_index = {cell: index for index, cell in enumerate(cells)}
    rows = qf_rows(families, dims, bad_vectors, cell_index)
    pivots = sparse_rref(rows)
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

    target = f_coefficients(families, dims, bad_vectors)
    generators = []
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
            constant = target.get((sites, word), Fraction(0))
            if constant:
                polynomial = add(polynomial, str(-constant))
            if polynomial != "0":
                generators.append(polynomial)
    return families, dims, cells, rows, pivots, variables, tuple(generators)


def ledger_digest(name, families, cells, rows, pivots, generators):
    digest = hashlib.sha256()
    digest.update(repr((name, families, cells)).encode("ascii"))
    digest.update(b"\nROWS\n")
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


def run(case, name, kind, timeout, run_ideal=True):
    families, dims, cells, rows, pivots, variables, generators = build(
        case, name, kind
    )
    digest = ledger_digest(name, families, cells, rows, pivots, generators)
    status = "SKIPPED"
    elapsed = 0.0
    stderr = ""
    if run_ideal:
        executable = shutil.which("Singular")
        if executable is None:
            raise SystemExit("Singular is required")
        program = (
            f"ring r=0,({','.join(variables)}),dp;\n"
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
        "dims": dims,
        "cells": len(cells),
        "rows": len(rows),
        "rank": len(pivots),
        "nullity": len(variables),
        "generators": len(generators),
        "sha256": digest,
        "status": status,
        "seconds": elapsed,
        "stderr": stderr,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", choices=tuple(name for name, _, _ in TYPES), action="append")
    parser.add_argument("--case", type=int, action="append")
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument("--ledger-only", action="store_true")
    args = parser.parse_args()

    selected = set(args.type) if args.type else None
    total = 0
    for name, kind, killed in TYPES:
        if selected is not None and name not in selected:
            continue
        reps = representatives(name)
        total += len(reps)
        print(name, "normalizable residual orbit count:", len(reps), flush=True)
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
        assert total == 145
    print("sole-defect normalizable nonseparable packet ideals: PASS")


if __name__ == "__main__":
    main()
