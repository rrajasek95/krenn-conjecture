#!/usr/bin/env python3
"""Independently replay TP N5^3 Macaulay solution ledgers.

The verifier knows only the frozen JSONL matrix interface.  It checks a Rust
modular solution literally, emits its selected source-column indices for an
independent-prime ``solve-selected`` run, and can replay a later rational
coefficient ledger exactly with ``Fraction`` arithmetic.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path


def mod_inverse(value, prime):
    return pow(value % prime, -1, prime)


def load_solution(path):
    data = json.loads(path.read_text())
    if not data.get("target_in_image"):
        raise RuntimeError(("solution says target is outside image", path))
    coefficients = {int(index): int(value)
                    for index, value in data["solution"]}
    if len(coefficients) != len(data["solution"]):
        raise RuntimeError("duplicate source-column index in solution")
    return data, coefficients


def load_rational(path):
    data = json.loads(path.read_text())
    records = data.get("coefficients", data)
    coefficients = {int(index): Fraction(int(numerator), int(denominator))
                    for index, numerator, denominator in records}
    if len(coefficients) != len(records):
        raise RuntimeError("duplicate source-column index in rational ledger")
    return coefficients


def add_mod(accumulator, entries, scale, prime):
    for row, value in entries:
        updated = (accumulator.get(row, 0) + scale*value) % prime
        if updated:
            accumulator[row] = updated
        else:
            accumulator.pop(row, None)


def add_q(accumulator, entries, scale):
    for row, value in entries:
        updated = accumulator.get(row, Fraction(0)) + scale*value
        if updated:
            accumulator[row] = updated
        else:
            accumulator.pop(row, None)


def replay(interface, modular_ledgers, rational_coefficients=None):
    digest = sha256()
    with interface.open() as stream:
        header_line = next(stream)
        digest.update(header_line.encode("ascii"))
        header = json.loads(header_line)
        if header.get("type") != "header":
            raise RuntimeError("first JSONL record is not a header")
        modular_accumulators = [{} for _ in modular_ledgers]
        selected = [set(coefficients) for _, coefficients in modular_ledgers]
        rational_accumulator = {} if rational_coefficients is not None else None
        rational_selected = (set(rational_coefficients)
                             if rational_coefficients is not None else set())
        seen = 0
        provenance = {}
        for line in stream:
            digest.update(line.encode("ascii"))
            record = json.loads(line)
            if record.get("type") != "column" or record["index"] != seen:
                raise RuntimeError(("column ordering changed", seen, record))
            entries = [(int(row), int(value))
                       for row, value in record["entries"]]
            for ledger_index, (prime, coefficients) in enumerate(modular_ledgers):
                if seen in selected[ledger_index]:
                    add_mod(modular_accumulators[ledger_index], entries,
                            coefficients[seen], prime)
                    provenance[seen] = {
                        key: record[key] for key in
                        ("source_label", "source_position", "multiplier")
                        if key in record
                    }
            if rational_accumulator is not None and seen in rational_selected:
                add_q(rational_accumulator, entries,
                      rational_coefficients[seen])
                provenance[seen] = {
                    key: record[key] for key in
                    ("source_label", "source_position", "multiplier")
                    if key in record
                }
            seen += 1
    if seen != header["column_count"]:
        raise RuntimeError(("column count changed", seen, header["column_count"]))
    for ledger_index, (prime, _) in enumerate(modular_ledgers):
        target = {}
        for row, numerator, denominator in header["target"]:
            value = numerator*mod_inverse(denominator, prime) % prime
            if value:
                target[int(row)] = value
        if modular_accumulators[ledger_index] != target:
            keys = set(modular_accumulators[ledger_index]) | set(target)
            discrepancy = {row: (modular_accumulators[ledger_index].get(row, 0)
                                 - target.get(row, 0)) % prime
                           for row in keys}
            discrepancy = {row: value for row, value in discrepancy.items()
                           if value}
            raise RuntimeError(("modular replay failed", prime,
                                len(discrepancy), list(discrepancy.items())[:10]))
    if rational_accumulator is not None:
        target_q = {int(row): Fraction(int(numerator), int(denominator))
                    for row, numerator, denominator in header["target"]}
        if rational_accumulator != target_q:
            keys = set(rational_accumulator) | set(target_q)
            discrepancy = {row: rational_accumulator.get(row, Fraction(0))
                            - target_q.get(row, Fraction(0)) for row in keys}
            discrepancy = {row: value for row, value in discrepancy.items()
                           if value}
            raise RuntimeError(("exact-Q replay failed", len(discrepancy),
                                list(discrepancy.items())[:10]))
    return header, digest.hexdigest(), provenance


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--interface", type=Path, required=True)
    parser.add_argument("--solution", type=Path, required=True)
    parser.add_argument("--second-solution", type=Path)
    parser.add_argument("--rational-coefficients", type=Path)
    parser.add_argument("--selected-out", type=Path)
    args = parser.parse_args()
    first_data, first = load_solution(args.solution)
    modular = [(int(first_data["prime"]), first)]
    if args.second_solution:
        second_data, second = load_solution(args.second_solution)
        if int(second_data["prime"]) == int(first_data["prime"]):
            raise RuntimeError("second solution uses the same prime")
        modular.append((int(second_data["prime"]), second))
    rational = (load_rational(args.rational_coefficients)
                if args.rational_coefficients else None)
    header, interface_sha, provenance = replay(args.interface, modular, rational)
    if args.selected_out:
        args.selected_out.write_text("".join(f"{index}\n" for index in sorted(first)))
    print("TP N5^3 Macaulay solution replay: PASS")
    print("interface rows / columns:", header["row_count"],
          header["column_count"])
    print("interface sha256:", interface_sha)
    print("modular primes / solution terms:",
          [(prime, len(coefficients)) for prime, coefficients in modular])
    print("exact-Q replayed:", rational is not None)
    print("selected provenance digest:", sha256(json.dumps(
        provenance, sort_keys=True, separators=(",", ":")).encode("ascii"))
        .hexdigest())


if __name__ == "__main__":
    main()
