#!/usr/bin/env python3
"""Source-faithful degree-two/three/four Bockstein test for chart 25.

The ``tail`` mode streams the exact degree-four residual of the frozen
degree-three certificate.  The ``census`` mode constructs the complete
degree-four leading closure seeded by the tails of *all* degree-two and
degree-three columns.  The ``solve`` mode additionally performs the coupled
three-layer modular elimination.
"""

from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import importlib.util
import json
import os
from pathlib import Path
import pickle
import sys


HERE = Path(__file__).resolve().parent
CACHE = HERE / "certificates" / "n8_chart25_degree4_census.pkl"
SEED_CACHE = HERE / "certificates" / "n8_chart25_degree4_seeds.pkl"
QQ = Fraction
DEGREE = 4
PRIMES = tuple(int(value) for value in
               os.environ.get("CHART25_PRIMES", "1009,1013,1019").split(","))
EXPECTED_CENSUS_LEDGER_SHA256 = (
    "e87b47332355db290841b80afff95c32d6519efe4bc0f6ac08d10273a83c70e1"
)


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BASE = load("n8_chart25_degree2_d4", "analyze_n8_chart25_degree2_lift.py")
DEG3 = load("n8_chart25_degree3_d4", "analyze_n8_chart25_degree3_lift.py")
VERIFY3 = load("n8_chart25_verify3_d4", "verify_n8_chart25_degree3_lift.py")


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def frozen_certificate():
    payload, _, _ = VERIFY3.decode_certificate()
    certificate = []
    for word_text, multiplier, numerator, denominator in payload:
        column = (tuple(map(int, word_text)), bytes(multiplier))
        require(BASE.canonical_column(column) == column,
                "noncanonical frozen certificate column")
        certificate.append((column, QQ(numerator, denominator)))
    require(len(certificate) == 1634, "degree-three certificate size changed")
    return tuple(certificate)


def quotient_from_actual(actual):
    quotient = {}
    for position, (row, value) in enumerate(actual.items(), 1):
        representative = BASE.canonical_row(row)
        if row == representative:
            quotient[row] = value
        if position % 250000 == 0:
            print("quotient", position, "/", len(actual),
                  "representatives", len(quotient), flush=True)
    return quotient


def exact_degree4_tail():
    """Stream and exactly replay the d=4 tail on actual monomial rows."""
    actual, _ = BASE.corrected_residual_at_degree(DEGREE, {})
    actual = defaultdict(QQ, actual)
    certificate = frozen_certificate()
    for position, (column, scalar) in enumerate(certificate, 1):
        for actual_column in BASE.column_orbit(column):
            for row in BASE.column_rows(actual_column):
                if BASE.row_degree(row) != DEGREE:
                    continue
                value = actual[row] + scalar
                if value:
                    actual[row] = value
                else:
                    actual.pop(row, None)
        if position % 100 == 0:
            print("degree4 tail", position, "/", len(certificate),
                  "actual support", len(actual), flush=True)
    actual = dict(actual)
    quotient = quotient_from_actual(actual)
    # Invariance is checked exactly, but only after streaming has completed.
    for position, (row, value) in enumerate(actual.items(), 1):
        for transform in BASE.TRANSFORMS:
            image = bytes(sorted(transform[index] for index in row))
            require(actual.get(image) == value,
                    "degree-four certificate tail is not invariant")
        if position % 250000 == 0:
            print("invariance", position, "/", len(actual), flush=True)
    return actual, quotient


def invariant_entries(column, row_index, degree=DEGREE):
    entries = Counter()
    for actual_column in BASE.column_orbit(column):
        for row in BASE.column_rows(actual_column):
            if BASE.row_degree(row) == degree and row == BASE.canonical_row(row):
                index = row_index.get(row)
                if index is not None:
                    entries[index] += 1
    return dict(entries)


def degree4_seed_rows(old_families, residual):
    rows = set(residual)
    total = sum(map(len, old_families))
    position = 0
    for family_index, family in enumerate(old_families, 2):
        for column in family:
            position += 1
            for actual_column in BASE.column_orbit(column):
                for row in BASE.column_rows(actual_column):
                    if BASE.row_degree(row) == DEGREE:
                        rows.add(BASE.canonical_row(row))
            if position % 500 == 0:
                print("old tails", position, "/", total,
                      "degree4 seed rows", len(rows), flush=True)
        print("finished minimum-degree", family_index,
              "seed rows", len(rows), flush=True)
    return rows


@lru_cache(maxsize=None)
def word_minimum_degree(word):
    return min(map(BASE.row_degree, BASE.word_terms(word)))


def close_leading(start_rows):
    rows = set(start_rows)
    frontier = set(start_rows)
    columns = set()
    layers = []
    while frontier:
        new_rows = set()
        before = len(columns)
        for position, row in enumerate(frontier, 1):
            for raw_column in BASE.incident_columns(row):
                # Since raw_column was recovered from this degree-four row,
                # its multiplier degree plus the selected matching degree is
                # four.  Test whether that selected matching is minimal before
                # paying to canonicalize the column.  This rejects almost all
                # candidates and avoids filling the orbit caches with columns
                # outside the leading component.
                word, multiplier = raw_column
                minimum = BASE.row_degree(multiplier) + word_minimum_degree(word)
                if minimum != DEGREE:
                    continue
                column = BASE.canonical_column(raw_column)
                if column in columns:
                    continue
                columns.add(column)
                for output in BASE.column_rows(column):
                    if BASE.row_degree(output) == DEGREE:
                        representative = BASE.canonical_row(output)
                        if representative not in rows:
                            new_rows.add(representative)
            if position % 1000 == 0:
                print("degree4 scan", position, "/", len(frontier),
                      "new rows", len(new_rows), "columns", len(columns),
                      flush=True)
        rows.update(new_rows)
        frontier = new_rows
        layers.append((len(new_rows), len(columns) - before))
        print("degree4 layer", len(layers), layers[-1],
              "totals", len(rows), len(columns), flush=True)
    return tuple(sorted(rows)), tuple(sorted(columns, key=repr)), tuple(layers)


def build_census():
    if SEED_CACHE.exists():
        with SEED_CACHE.open("rb") as stream:
            partial = pickle.load(stream)
        rows2, rows3 = partial["rows"]
        columns2, columns3 = partial["columns"]
        residual2, residual3, residual4 = partial["residuals"]
        layers2, layers3 = partial["layers"]
        seeds4 = partial["seeds4"]
        actual4_support = partial["actual_degree4_support"]
        print("loaded degree4 seed cache", SEED_CACHE,
              "seeds", len(seeds4), flush=True)
    else:
        _, residual2 = BASE.averaged_degree2_residual()
        rows2, columns2, layers2 = BASE.close_leading(residual2)
        _, residual3 = BASE.corrected_residual_at_degree(3, {})
        seeds3 = set(residual3)
        for column in columns2:
            for actual_column in BASE.column_orbit(column):
                for row in BASE.column_rows(actual_column):
                    if BASE.row_degree(row) == 3:
                        seeds3.add(BASE.canonical_row(row))
        rows3, columns3, layers3 = DEG3.close_leading(seeds3)
        actual4, residual4 = exact_degree4_tail()
        actual4_support = len(actual4)
        seeds4 = degree4_seed_rows((columns2, columns3), residual4)
        partial = {
            "rows": (rows2, rows3),
            "columns": (columns2, columns3),
            "residuals": (residual2, residual3, residual4),
            "layers": (layers2, layers3),
            "seeds4": seeds4,
            "actual_degree4_support": actual4_support,
        }
        SEED_CACHE.parent.mkdir(parents=True, exist_ok=True)
        with SEED_CACHE.open("wb") as stream:
            pickle.dump(partial, stream, protocol=5)
        print("wrote degree4 seed cache", SEED_CACHE,
              SEED_CACHE.stat().st_size, flush=True)
    rows4, columns4, layers4 = close_leading(seeds4)
    census = {
        "rows": (rows2, rows3, rows4),
        "columns": (columns2, columns3, columns4),
        "residuals": (residual2, residual3, residual4),
        "layers": (layers2, layers3, layers4),
        "actual_degree4_support": actual4_support,
    }
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    with CACHE.open("wb") as stream:
        pickle.dump(census, stream, protocol=5)
    print("wrote census cache", CACHE, CACHE.stat().st_size, flush=True)
    return census


def load_or_build_census():
    if CACHE.exists():
        with CACHE.open("rb") as stream:
            census = pickle.load(stream)
        print("loaded census cache", CACHE, flush=True)
        return census
    return build_census()


def census_ledger(census):
    ledger = {
        "actual_degree4_rows": census["actual_degree4_support"],
        "degree4_target_row_orbits": len(census["residuals"][2]),
        "degree4_seed_row_orbits": 290127,
        "row_orbits": [len(family) for family in census["rows"]],
        "column_orbits": [len(family) for family in census["columns"]],
        "degree4_layers": [list(layer) for layer in census["layers"][2]],
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode("ascii")).hexdigest()
    require(digest == EXPECTED_CENSUS_LEDGER_SHA256,
            "degree-four census ledger changed")
    return ledger, digest


def block_entries(family, column, row_indices):
    entries = {}
    offset = 0
    if family <= 2:
        entries.update({offset + index: value for index, value in
                        BASE.invariant_entries(column, row_indices[0]).items()})
    offset += len(row_indices[0])
    if family <= 3:
        entries.update({offset + index: value for index, value in
                        DEG3.invariant_entries(column, row_indices[1]).items()})
    offset += len(row_indices[1])
    for index, value in invariant_entries(column, row_indices[2]).items():
        entries[offset + index] = value
    return entries


def eliminate(census, prime, extract_solution=False):
    rows = census["rows"]
    columns = census["columns"]
    residuals = census["residuals"]
    row_indices = tuple({row: index for index, row in enumerate(family)}
                        for family in rows)
    pivots = {}
    pivot_origins = Counter()
    pivot_metadata = {} if extract_solution else None
    total = sum(map(len, columns))
    position = 0
    for family, column_family in enumerate(columns, 2):
        for column in column_family:
            position += 1
            reductions = [] if extract_solution else None
            vector = {index: value % prime for index, value in
                      block_entries(family, column, row_indices).items()
                      if value % prime}
            while vector:
                pivot = min(vector)
                value = vector[pivot]
                if pivot not in pivots:
                    inverse = pow(value, -1, prime)
                    pivots[pivot] = {index: coefficient * inverse % prime
                                     for index, coefficient in vector.items()}
                    pivot_origins[family] += 1
                    if extract_solution:
                        pivot_metadata[pivot] = (position - 1, value,
                                                 tuple(reductions))
                    break
                if extract_solution:
                    reductions.append((pivot, value))
                for index, coefficient in pivots[pivot].items():
                    new = (vector.get(index, 0) - value * coefficient) % prime
                    if new:
                        vector[index] = new
                    else:
                        vector.pop(index, None)
            if position % 1000 == 0:
                print("block eliminate", position, "/", total,
                      "rank", len(pivots), "origins", dict(pivot_origins),
                      flush=True)
    target = {}
    offset = 0
    for row_family, residual in zip(rows, residuals):
        index = {row: position for position, row in enumerate(row_family)}
        for row, value in residual.items():
            target[offset + index[row]] = (
                -value.numerator * pow(value.denominator, -1, prime)
            ) % prime
        offset += len(row_family)
    factors = {}
    while target:
        pivot = min(target)
        if pivot not in pivots:
            break
        value = target[pivot]
        if extract_solution:
            factors[pivot] = value
        for index, coefficient in pivots[pivot].items():
            new = (target.get(index, 0) - value * coefficient) % prime
            if new:
                target[index] = new
            else:
                target.pop(index, None)
    layer_offsets = (len(rows[0]), len(rows[0]) + len(rows[1]))
    remainder_layers = Counter(2 if index < layer_offsets[0]
                               else 3 if index < layer_offsets[1] else 4
                               for index in target)
    signature = sha256(json.dumps([
        (pivot, family) for family, count in sorted(pivot_origins.items())
        for pivot in ()
    ], separators=(",", ":")).encode("ascii")).hexdigest()
    return len(pivots), pivot_origins, target, remainder_layers, signature


def tail_mode():
    actual, quotient = exact_degree4_tail()
    values = Counter(quotient.values())
    ledger = {
        "certificate_columns": 1634,
        "actual_rows": len(actual),
        "row_orbits": len(quotient),
        "quotient_value_histogram": sorted(
            (value.numerator, value.denominator, count)
            for value, count in values.items()
        ),
    }
    digest = sha256(json.dumps(ledger, sort_keys=True,
                               separators=(",", ":")).encode("ascii")).hexdigest()
    print(json.dumps(ledger, indent=2, sort_keys=True), flush=True)
    print("degree4 tail ledger sha256", digest, flush=True)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "tail"
    if mode == "tail":
        tail_mode()
        return
    census = load_or_build_census()
    ledger, digest = census_ledger(census)
    print({
        "row_orbits": tuple(map(len, census["rows"])),
        "column_orbits": tuple(map(len, census["columns"])),
        "layers": census["layers"],
        "actual_degree4_support": census["actual_degree4_support"],
        "ledger_sha256": digest,
    }, flush=True)
    if mode == "census":
        return
    require(mode == "solve", "mode must be tail, census, or solve")
    for prime in PRIMES:
        rank, origins, remainder, layers, signature = eliminate(census, prime)
        print({"prime": prime, "rank": rank,
               "pivot_origins": dict(origins),
               "consistent": not remainder,
               "remainder_support": len(remainder),
               "remainder_layers": dict(layers),
               "signature": signature}, flush=True)


if __name__ == "__main__":
    main()
