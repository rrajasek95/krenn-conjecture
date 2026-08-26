#!/usr/bin/env python3
"""Reconstruct and replay the fixed-minor cutoff-7 certificate over Q."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path

from verify_accelerator import crt, rational_reconstruct


HERE = Path(__file__).resolve().parent
INTERFACE = HERE / "results_chart26_cutoff7_direct.jsonl"
OUT = HERE / "results_chart26_cutoff7_exact_core_certificate.json"
TSV = HERE / "results_chart26_cutoff7_exact_solution.tsv"
INTERFACE_SHA = "487662cd76c11452bd8bf7feb343f290bffc3a623b18988c974d395ebdf55328"
PRIMES = (
    1009, 1019, 1031, 1033, 1039, 1049, 1051, 1061,
    1063, 1069, 1087, 1091, 1093, 1097, 1103, 1109,
    1117, 1123, 1129, 1151, 1153, 1163, 1171, 1181,
    1187, 1193, 1201, 1213, 1217, 1223, 1229, 1231,
)


def solution_path(prime):
    if prime in (1009, 1019):
        return HERE / f"results_chart26_cutoff7_solution_p{prime}.json"
    return HERE / f"results_chart26_cutoff7_selected_p{prime}.json"


def reconstruct():
    modular = []
    for prime in PRIMES:
        data = json.loads(solution_path(prime).read_text())
        assert data["prime"] == prime and data["rank"] == 13202
        assert data["target_in_image"] and not data["remainder"]
        modular.append(dict(data["solution"]))
    support = sorted(set().union(*modular))
    coefficients = {}
    modulus = PRIMES[0]
    residues = dict(modular[0])
    for prime, solution in zip(PRIMES[1:], modular[1:]):
        residues = {
            index: crt(residues.get(index, 0), modulus,
                       solution.get(index, 0), prime)
            for index in support
        }
        modulus *= prime
    for index in support:
        value = rational_reconstruct(residues[index], modulus)
        if value:
            coefficients[index] = value
    assert len(coefficients) == 11460
    return coefficients


def exact_replay(coefficients):
    assert sha256(INTERFACE.read_bytes()).hexdigest() == INTERFACE_SHA
    replay = Counter()
    selected_vectors = {}
    with INTERFACE.open() as handle:
        header = json.loads(next(handle))
        target = Counter({index: Fraction(numerator, denominator)
                          for index, numerator, denominator in header["target"]})
        for line in handle:
            record = json.loads(line)
            coefficient = coefficients.get(record["index"])
            if coefficient:
                vector = Counter(dict(record["entries"]))
                selected_vectors[record["index"]] = vector
                for row, value in vector.items():
                    replay[row] += coefficient * value
    replay += Counter()
    target += Counter()
    assert replay == target
    first = min(coefficients)
    mutation = Counter(replay)
    for row, value in selected_vectors[first].items():
        mutation[row] += value
    mutation += Counter()
    assert mutation != target


def main():
    coefficients = reconstruct()
    exact_replay(coefficients)
    TSV.write_text("".join(
        f"{index}\t{value.numerator}\t{value.denominator}\n"
        for index, value in sorted(coefficients.items())
    ))
    core = {
        "status": "EXACT-Q reconstructed fixed-minor core certificate",
        "chart": 26,
        "cutoff": 7,
        "prime": None,
        "crt_primes": list(PRIMES),
        "coefficients": [
            [index, value.numerator, value.denominator]
            for index, value in sorted(coefficients.items())
        ],
        "core_interface_sha256": INTERFACE_SHA,
    }
    encoded = json.dumps(core, sort_keys=True, separators=(",", ":"))
    core["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(core, indent=2, sort_keys=True) + "\n")
    print("cutoff7 fixed-minor exact reconstruction: PASS")
    print("terms:", len(coefficients))
    print("logical sha256:", core["result_sha256"])
    print("file sha256:", sha256(OUT.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
