#!/usr/bin/env python3
"""Exact bounded audit of the universal S3 kernel against translated PM4 cells.

The input PM4 packet contains 2,206 disjoint three-term quadratic blocks.
Multiplying a block by one normalized chart variable gives a cubic three-term
cell.  Rather than materialize all 2,206*240 cells, this checker uses the
disjointness of the quadratic terms: deleting one byte from a cubic monomial
identifies its unique possible PM4 parent.  It therefore constructs exactly
the connected component of the translated-cell hypergraph meeting S3.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE_DIR = ROOT / "computations/unaudited-codex-n8-orbit26-direct-target-2026-08-23"
KERNEL_PACKET = SOURCE_DIR / "direct_fh_transfer_kernels.txt"
BLOCK_PACKET = SOURCE_DIR / "quadratic_pm4_blocks.txt"
RESULT_PATH = HERE / "results_s3_pm4_translate.json"
EXPECTED = {
    KERNEL_PACKET: "859f144440e45ca64c1534ae99506e31524d76cd3c47e83911b384c2fea49650",
    BLOCK_PACKET: "28bd60422fb75c96d7296b5903073ee879f61c004138f397db6293d6f1b965bb",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def parse_s3():
    active = False
    answer = {}
    for line in KERNEL_PACKET.read_text(encoding="ascii").splitlines():
        fields = line.split()
        if fields[:2] == ["BEGIN", "S3"]:
            active = True
        elif fields[:2] == ["END", "S3"]:
            active = False
        elif active and fields[0] == "ROW":
            answer[bytes.fromhex(fields[1])] = int(fields[2])
    require(len(answer) == 66 and Counter(answer.values()) == Counter({1: 53, -1: 13}),
            "S3 packet profile changed")
    require(all(len(row) == 3 for row in answer), "S3 stopped being cubic")
    return answer


def parse_blocks():
    blocks = []
    sources = []
    for line in BLOCK_PACKET.read_text(encoding="ascii").splitlines():
        fields = line.split()
        if fields[0] == "BLOCK":
            term_field = next(field for field in fields if field.startswith("TERMS="))
            source_field = next(field for field in fields if field.startswith("SOURCES="))
            blocks.append(tuple(bytes.fromhex(item)
                                for item in term_field.removeprefix("TERMS=").split(",")))
            sources.append(int(source_field.removeprefix("SOURCES=")))
    require(len(blocks) == 2206 and all(len(block) == 3 for block in blocks),
            "PM4 block census changed")
    require(Counter(sources) == Counter({1: 2114, 2: 92}),
            "PM4 source multiplicities changed")
    term_parent = {}
    for index, block in enumerate(blocks):
        for term in block:
            require(len(term) == 2 and term not in term_parent,
                    "quadratic PM4 terms stopped being disjoint")
            term_parent[term] = index
    require(len(term_parent) == 6618, "quadratic PM4 term count changed")
    return blocks, sources, term_parent


def remove_position(row, position):
    return row[:position] + row[position + 1:]


def translated_column(block, variable):
    return tuple(sorted(bytes(sorted(term + bytes([variable]))) for term in block))


def incident_columns(row, blocks, term_parent):
    """All translated PM4 cells containing the cubic monomial row."""
    answer = set()
    for position, variable in enumerate(row):
        quadratic = remove_position(row, position)
        block_index = term_parent.get(quadratic)
        if block_index is None:
            continue
        column = translated_column(blocks[block_index], variable)
        require(row in column, "inverse translated-cell lookup failed")
        answer.add((block_index, variable, column))
    return answer


def component(seed, blocks, term_parent):
    rows = set(seed)
    columns = {}
    queue = deque(sorted(seed))
    while queue:
        row = queue.popleft()
        for block_index, variable, column in incident_columns(row, blocks, term_parent):
            key = (block_index, variable)
            if key in columns:
                require(columns[key] == column, "translated column key collision")
                continue
            columns[key] = column
            for item in column:
                if item not in rows:
                    rows.add(item)
                    queue.append(item)
    return tuple(sorted(rows)), tuple((key, columns[key]) for key in sorted(columns))


def sparse_rank_and_reduce(rows, columns, target, prime):
    """Column elimination over F_p; return rank and target remainder."""
    row_index = {row: index for index, row in enumerate(rows)}
    pivots = {}

    def reduce(vector):
        vector = {index: value % prime for index, value in vector.items() if value % prime}
        while vector:
            pivot = min(vector)
            if pivot not in pivots:
                return vector
            scale = vector[pivot]
            basis = pivots[pivot]
            for index, value in basis.items():
                updated = (vector.get(index, 0) - scale * value) % prime
                if updated:
                    vector[index] = updated
                else:
                    vector.pop(index, None)
        return vector

    for _key, column in columns:
        vector = reduce({row_index[row]: 1 for row in column})
        if vector:
            pivot = min(vector)
            inverse = pow(vector[pivot], prime - 2, prime)
            pivots[pivot] = {index: value * inverse % prime
                             for index, value in vector.items()}
    remainder = reduce({row_index[row]: coefficient for row, coefficient in target.items()})
    return len(pivots), remainder, pivots, row_index


def exact_dual(rows, columns, target, modular_remainder, prime):
    """Lift a sparse modular remainder witness to an exact left null vector.

    The modular reduction alone is a rank/nonmembership result at one prime.
    For a reusable Q certificate, solve the transpose constraints on the whole
    connected component with exact Fractions, fixing one remainder coordinate
    to one.  This routine is invoked only for a small component.
    """
    if not modular_remainder:
        return None
    # Build homogeneous equations d_a+d_b+d_c=0 for every translated cell,
    # plus the target normalization <d,S3>=1. Sparse exact row reduction is
    # performed on dual variables.  The modular remainder is retained only as
    # a guard that a separator should exist at the checked prime.
    n = len(rows)
    row_index = {row: index for index, row in enumerate(rows)}
    equations = []
    for _key, column in columns:
        equations.append({row_index[row]: Fraction(1) for row in column})
    require(modular_remainder, "exact dual requested for a modular member")
    normalization = {row_index[row]: Fraction(coefficient)
                     for row, coefficient in target.items()}
    normalization[n] = Fraction(-1)
    equations.append(normalization)

    pivots = {}
    for equation in equations:
        vector = dict(equation)
        while True:
            variables = [index for index in vector if index < n and vector[index]]
            if not variables:
                break
            pivot = min(variables)
            if pivot not in pivots:
                scale = vector[pivot]
                pivots[pivot] = {index: value / scale for index, value in vector.items()}
                break
            scale = vector[pivot]
            basis = pivots[pivot]
            for index, value in basis.items():
                updated = vector.get(index, Fraction(0)) - scale * value
                if updated:
                    vector[index] = updated
                else:
                    vector.pop(index, None)
    # Back-substitute with all free variables zero. Augmented coordinate n is
    # the constant term, so pivot equations encode x_p + ... + c = 0.
    solution = [Fraction(0)] * n
    for pivot in sorted(pivots, reverse=True):
        equation = pivots[pivot]
        rhs = -equation.get(n, Fraction(0))
        for index, value in equation.items():
            if index not in (pivot, n):
                rhs -= value * solution[index]
        solution[pivot] = rhs
    require(all(sum(solution[row_index[row]] for row in column) == 0
                for _key, column in columns), "exact dual failed a translated PM4 cell")
    pairing = sum(solution[row_index[row]] * coefficient
                  for row, coefficient in target.items())
    require(pairing == 1, "exact target-normalized dual did not pair S3 to one")
    return solution, pairing


def audit(mutate=False):
    for path, digest in EXPECTED.items():
        require(sha256(path.read_bytes()).hexdigest() == digest,
                f"source drift: {path}")
    s3 = parse_s3()
    blocks, source_multiplicity, term_parent = parse_blocks()
    rows, columns = component(s3, blocks, term_parent)
    require(set(s3) <= set(rows), "S3 left its component")

    direct_crossing = [
        (block_index, variable) for (block_index, variable), column in columns
        if any(row in s3 for row in column)
    ]
    translated_source_histogram = Counter(
        source_multiplicity[block_index] for (block_index, _variable), _column in columns
    )
    ranks = {}
    modular = {}
    chosen = None
    for prime in (1009, 1013):
        rank, remainder, pivots, row_index = sparse_rank_and_reduce(
            rows, columns, s3, prime
        )
        ranks[prime] = rank
        modular[prime] = {
            "remainder_support": len(remainder),
            "remainder": [[rows[index].hex(), value]
                          for index, value in sorted(remainder.items())],
        }
        if chosen is None:
            chosen = (remainder, prime)
    require(len(set(ranks.values())) == 1, "component rank differs at two primes")

    if mutate:
        first = min(s3)
        s3[first] = -s3[first]

    exact = exact_dual(rows, columns, s3, chosen[0], chosen[1])
    if exact is None:
        exact_summary = {"membership": True}
    else:
        solution, pairing = exact
        nonzero = [(rows[index].hex(), value) for index, value in enumerate(solution) if value]
        denominator_lcm = 1
        from math import gcd
        for _row, value in nonzero:
            denominator_lcm = denominator_lcm * value.denominator // gcd(
                denominator_lcm, value.denominator
            )
        integer = [(row, int(value * denominator_lcm)) for row, value in nonzero]
        common = 0
        for _row, value in integer:
            common = gcd(common, abs(value))
        common = max(common, 1)
        integer = [(row, value // common) for row, value in integer]
        integer_pairing = int(pairing * denominator_lcm) // common
        exact_summary = {
            "membership": False,
            "dual_support": len(integer),
            "dual_max_abs": max(abs(value) for _row, value in integer),
            "target_pairing": integer_pairing,
            "dual": [[row, value] for row, value in integer],
        }

    result = {
        "format": "n8-S3-translated-PM4-component-v1",
        "status": "EXACT_COMPONENT_TEST",
        "source_sha256": {str(path.relative_to(ROOT)): digest
                          for path, digest in EXPECTED.items()},
        "S3": {
            "rows": len(s3),
            "coefficient_histogram": dict(sorted(Counter(s3.values()).items())),
        },
        "PM4": {
            "blocks": len(blocks),
            "quadratic_rows": len(term_parent),
            "all_degree_one_translates": len(blocks) * 240,
            "inverse_lookup_reason": (
                "the 6618 quadratic terms partition into 2206 triples; deleting "
                "one factor from a cubic row identifies every incident translate"
            ),
        },
        "S3_component": {
            "cubic_rows": len(rows),
            "translated_cells": len(columns),
            "direct_S3_crossing_cells": len(direct_crossing),
            "source_multiplicity_histogram": dict(sorted(translated_source_histogram.items())),
            "rank_mod_primes": ranks,
            "modular_remainders": modular,
        },
        "exact": exact_summary,
        "attachment66_comparison": {
            "literal_identity": False,
            "reason": (
                "S3 is cubic with coefficients +/-1 (53/13); the independently "
                "frozen attachment has y-degree8 and coefficient magnitudes 1,2,3,4 "
                "(positive/negative 34/32). Symmetry, global sign, and t-shift "
                "preserve these invariants."
            ),
        },
        "scope": (
            "exact component of all degree-one translates of the 2206 literal N4 "
            "leading triples that meets S3; no higher translates, S4 cells, or "
            "full y10 residual are included"
        ),
    }
    result["logical_sha256"] = sha256(json.dumps(
        result, sort_keys=True, separators=(",", ":")
    ).encode("ascii")).hexdigest()
    return json.loads(json.dumps(result))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    parser.add_argument("--mutate", action="store_true")
    args = parser.parse_args()
    result = audit(args.mutate)
    if args.write_results:
        RESULT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    if args.check_results:
        require(RESULT_PATH.exists() and json.loads(RESULT_PATH.read_text()) == result,
                "stored result changed")
    print(result["status"])
    print("component rows/cells/rank=", result["S3_component"]["cubic_rows"],
          result["S3_component"]["translated_cells"],
          result["S3_component"]["rank_mod_primes"])
    print("membership/dual=", result["exact"]["membership"],
          result["exact"].get("dual_support"))
    print("logical", result["logical_sha256"])


if __name__ == "__main__":
    main()
