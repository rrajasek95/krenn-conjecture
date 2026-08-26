#!/usr/bin/env python3
"""Compiled F4 gates for low-rank normal planes mixing the two shores."""

from collections import defaultdict
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from audit_colour_only_hamming_certificate import VARIABLES, build_generators
from audit_first_edge_deviation_lift import EDGES, literal_target, literal_word


LEFT = (0, 1, 2, 6, 7)
RIGHT = (3, 4, 5)
INTERNAL = set(combinations(LEFT, 2)) | set(combinations(RIGHT, 2))


def direction_coefficients(cell, internal_rank, cross_rank):
    u, v, a, b = cell
    edge_index = EDGES.index((u, v))
    rank = internal_rank if (u, v) in INTERNAL else cross_rank
    offset = 0 if (u, v) in INTERNAL else internal_rank
    out = []
    for direction in range(rank):
        modulus = (5, 7, 11, 13, 17, 19)[direction]
        value = 1 + ((9 * edge_index + 3 * a + b + 2 * direction) % modulus)
        out.append((offset + direction, value))
    return out


def expansion(poly, internal_rank, cross_rank, squarefree=False):
    rank = internal_rank + cross_rank
    out = defaultdict(int)
    for term, coefficient in poly.items():
        ybase = [0] * 9
        for _, _, a, b in term:
            ybase[3 * a + b] += 1
        states = {((0,) * rank, tuple(ybase)): coefficient}
        for cell in term:
            updated = defaultdict(int)
            for (degrees, ykey), value in states.items():
                updated[(degrees, ykey)] += value
                for variable, scalar in direction_coefficients(
                    cell, internal_rank, cross_rank
                ):
                    # In the quotient by (s_i^2,t_j^2), every state which
                    # reuses a parameter is already zero.  Pruning it here
                    # is exactly reduction modulo the appended square rows,
                    # and prevents an otherwise enormous dead expansion.
                    if squarefree and degrees[variable]:
                        continue
                    shifted_y = list(ykey)
                    shifted_y[3 * cell[2] + cell[3]] -= 1
                    shifted_degrees = list(degrees)
                    shifted_degrees[variable] += 1
                    updated[(tuple(shifted_degrees), tuple(shifted_y))] += scalar * value
            states = {key: value for key, value in updated.items() if value}
        for key, value in states.items():
            out[key] += value
    return {key: value for key, value in out.items() if value}


def polynomial(poly, parameter_names, prime):
    pieces = []
    for (degrees, ykey), integer_coefficient in sorted(poly.items()):
        coefficient = integer_coefficient % prime
        if not coefficient:
            continue
        factors = []
        for variable, degree in zip(parameter_names, degrees):
            if degree == 1:
                factors.append(variable)
            elif degree:
                factors.append(f"{variable}^{degree}")
        for variable, degree in zip(VARIABLES, ykey):
            if degree == 1:
                factors.append(variable)
            elif degree:
                factors.append(f"{variable}^{degree}")
        pieces.append(f"{coefficient}*" + ("*".join(factors) or "1"))
    return "+".join(pieces) or "0"


def run_audit(
    internal_rank, cross_rank, prime=1009, timeout=600, mutate=False, threads=1,
    squarezero=False,
):
    parameter_names = tuple(
        [f"s{i}" for i in range(internal_rank)] +
        [f"t{i}" for i in range(cross_rank)]
    )
    generator_map = {
        "".join(map(str, word)): word for word, _ in build_generators()
    }
    closure_words = json.loads(
        (HERE / "results_second_order_lift_support.json").read_text()
    )["combined_closure_words"]
    row_expansions = [
        expansion(
            literal_word(generator_map[word]), internal_rank, cross_rank,
            squarefree=squarezero,
        )
        for word in closure_words
    ]
    target_expansion = expansion(
        literal_target(), internal_rank, cross_rank, squarefree=squarezero
    )
    rows = [polynomial(row, parameter_names, prime) for row in row_expansions]
    if squarezero:
        rows.extend(f"{parameter}^2" for parameter in parameter_names)
    target = polynomial(target_expansion, parameter_names, prime)
    if mutate:
        target += "+1"
    with tempfile.TemporaryDirectory(prefix="krenn-lowrank-plane-") as directory:
        directory = Path(directory)
        input_path = directory / "input.ms"
        output_path = directory / "output.ms"
        input_path.write_text(
            ",".join(VARIABLES + parameter_names) + "\n" + str(prime) + "\n" +
            ",\n".join(rows + [target]) + "\n"
        )
        input_bytes = input_path.stat().st_size
        completed = subprocess.run(
            ["msolve", "-f", str(input_path), "-o", str(output_path),
             "-n", "1", "-t", str(threads), "-v", "1",
             "--random-seed", "0"],
            text=True, capture_output=True, timeout=timeout, check=False,
            stdin=subprocess.DEVNULL,
        )
        output = output_path.read_text() if output_path.exists() else ""
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr + completed.stdout[-8000:])
    zero = "".join(output.split()) in ("[0]", "[0]:")
    labels = (
        "size of basis", "#terms in basis", "#pairs reduced", "#rows reduced",
        "#zero reductions", "max. matrix data",
    )
    stats = {}
    for line in completed.stderr.splitlines():
        stripped = line.strip()
        for label in labels:
            if stripped.startswith(label):
                stats[label] = stripped[len(label):].strip()
    return {
        "status": (
            "PASS hostile mutation has nonzero normal form" if mutate and not zero else
            "PASS low-rank plane has zero normal form" if not mutate and zero else
            "UNEXPECTED low-rank plane verdict"
        ),
        "internal_rank": internal_rank,
        "cross_rank": cross_rank,
        "total_rank": internal_rank + cross_rank,
        "characteristic": prime,
        "mutate_target_by_constant": mutate,
        "threads": threads,
        "squarezero_parameter_quotient": squarezero,
        "normal_form_zero": zero,
        "output": output,
        "output_sha256": hashlib.sha256(output.encode()).hexdigest(),
        "source_rows": len(rows),
        "source_terms_after_collection": sum(map(len, row_expansions)),
        "target_terms_after_collection": len(target_expansion),
        "input_bytes": input_bytes,
        "msolve_stable_statistics": stats,
        "scope": (
            "Exact finite-field normal form on the deterministic low-rank "
            "normal plane. This does not by itself prove the universal "
            "252-parameter identity."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--internal-rank", type=int, default=2)
    parser.add_argument("--cross-rank", type=int, default=1)
    parser.add_argument("--prime", type=int, default=1009)
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--mutate-target", action="store_true")
    parser.add_argument("--threads", type=int, default=1)
    parser.add_argument("--squarezero", action="store_true")
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    args = parser.parse_args()
    result = run_audit(
        args.internal_rank, args.cross_rank, args.prime, args.timeout,
        args.mutate_target, args.threads, args.squarezero,
    )
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    suffix = "_squarezero" if args.squarezero else ""
    result_path = HERE / (
        f"results_lowrank_plane_i{args.internal_rank}_c{args.cross_rank}{suffix}.json"
    )
    if args.write_results:
        if args.mutate_target:
            raise RuntimeError("refusing to store hostile result")
        result_path.write_text(text)
    if args.check_results and result_path.read_text() != text:
        raise RuntimeError("stored low-rank plane result changed")
    print(text, end="")


if __name__ == "__main__":
    main()
