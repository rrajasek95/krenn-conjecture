#!/usr/bin/env python3
"""Audit the S8-module left after all balanced contrast contractions.

Let p=(1,0), q=(0,1), and r=q-p in a two-dimensional contrast plane.
For each of the three ordered count profiles (3,3,2), (3,2,3), and
(2,3,3), take every labelled tensor with those numbers of p,q,r factors.
Their span W is the raw linear span of the 1,680 balanced contractions.

This script computes W inside (Q^2)^{tensor 8} modulo two good primes and
computes the character of the quotient on every conjugacy class of S8.
The quotient character is exactly 6*[8] + 3*[7,1].
"""

from __future__ import annotations

from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_contrast_annihilator_module.json"
N = 8
DIM = 1 << N


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def assignments() -> tuple[tuple[int, ...], ...]:
    answer = []
    for counts in ((3, 3, 2), (3, 2, 3), (2, 3, 3)):
        seed = tuple(direction for direction, count in enumerate(counts)
                     for _ in range(count))
        answer.extend(sorted(set(permutations(seed))))
    return tuple(answer)


ASSIGNMENTS = assignments()


def tensor_row(assignment: tuple[int, ...], prime: int) -> list[int]:
    """Coordinates of tensor_product(v_i), p=e0,q=e1,r=e1-e0."""
    row = [0] * DIM
    r_sites = tuple(i for i, direction in enumerate(assignment)
                    if direction == 2)
    base = sum(1 << i for i, direction in enumerate(assignment)
               if direction == 1)
    for mask in range(1 << len(r_sites)):
        index = base
        coefficient = 1
        for j, site in enumerate(r_sites):
            if (mask >> j) & 1:
                index |= 1 << site
            else:
                coefficient = -coefficient
        row[index] = coefficient % prime
    return row


def rref(prime: int) -> tuple[tuple[int, ...], tuple[tuple[int, ...], ...]]:
    basis: dict[int, list[int]] = {}
    for assignment in ASSIGNMENTS:
        vector = tensor_row(assignment, prime)
        for pivot, row in basis.items():
            scalar = vector[pivot]
            if scalar:
                vector = [(a - scalar * b) % prime
                          for a, b in zip(vector, row)]
        pivot = next((i for i, value in enumerate(vector) if value), None)
        if pivot is None:
            continue
        inverse = pow(vector[pivot], -1, prime)
        vector = [(inverse * value) % prime for value in vector]
        for old_pivot, row in tuple(basis.items()):
            scalar = row[pivot]
            if scalar:
                basis[old_pivot] = [(a - scalar * b) % prime
                                    for a, b in zip(row, vector)]
        basis[pivot] = vector
    pivots = tuple(sorted(basis))
    rows = tuple(tuple(basis[pivot]) for pivot in pivots)
    require(all(rows[i][pivot] == 1 for i, pivot in enumerate(pivots)),
            "pivot normalization failed")
    return pivots, rows


def permutation_of_cycle_type(parts: tuple[int, ...]) -> tuple[int, ...]:
    image = list(range(N))
    start = 0
    for length in parts:
        cycle = tuple(range(start, start + length))
        for i, site in enumerate(cycle):
            image[site] = cycle[(i + 1) % length]
        start += length
    require(start == N, "cycle type does not partition eight sites")
    return tuple(image)


def bit_permutation(index: int, permutation: tuple[int, ...]) -> int:
    answer = 0
    for site in range(N):
        if (index >> site) & 1:
            answer |= 1 << permutation[site]
    return answer


def cycle_count(permutation: tuple[int, ...]) -> int:
    seen = set()
    count = 0
    for start in range(N):
        if start in seen:
            continue
        count += 1
        site = start
        while site not in seen:
            seen.add(site)
            site = permutation[site]
    return count


def quotient_character(prime: int, pivots: tuple[int, ...],
                       rows: tuple[tuple[int, ...], ...],
                       parts: tuple[int, ...]) -> int:
    permutation = permutation_of_cycle_type(parts)
    inverse = [0] * N
    for site, image in enumerate(permutation):
        inverse[image] = site
    # RREF pivot columns identify coordinates on W.  The trace of the
    # transformed RREF basis is therefore the following diagonal sum.
    transformed_pivots = tuple(bit_permutation(pivot, tuple(inverse))
                               for pivot in pivots)
    trace_w = sum(rows[i][transformed_pivots[i]]
                  for i in range(len(pivots))) % prime
    trace_full = pow(2, cycle_count(permutation), prime)
    value = (trace_full - trace_w) % prime
    return value if value <= prime // 2 else value - prime


def standard_character(parts: tuple[int, ...]) -> int:
    fixed_points = sum(length == 1 for length in parts)
    return fixed_points - 1


def main() -> None:
    require(len(ASSIGNMENTS) == 1680, "balanced assignment census changed")
    cycle_types = tuple(
        parts for parts in (
            (1, 1, 1, 1, 1, 1, 1, 1),
            (2, 1, 1, 1, 1, 1, 1),
            (2, 2, 1, 1, 1, 1),
            (2, 2, 2, 1, 1),
            (2, 2, 2, 2),
            (3, 1, 1, 1, 1, 1),
            (3, 2, 1, 1, 1),
            (3, 3, 1, 1),
            (4, 1, 1, 1, 1),
            (4, 2, 1, 1),
            (4, 2, 2),
            (4, 3, 1),
            (4, 4),
            (5, 1, 1, 1),
            (5, 2, 1),
            (5, 3),
            (6, 1, 1),
            (6, 2),
            (7, 1),
            (8,),
        )
    )
    expected = {
        "".join(map(str, parts)): 6 + 3 * standard_character(parts)
        for parts in cycle_types
    }
    prime_results = {}
    mutation_fires = False
    for prime in (1009, 1013):
        pivots, rows = rref(prime)
        require(len(pivots) == 229, "balanced tensor rank changed")
        character = {
            "".join(map(str, parts)):
                quotient_character(prime, pivots, rows, parts)
            for parts in cycle_types
        }
        require(character == expected,
                "quotient character differs from 6*[8]+3*[7,1]")
        mutated = dict(character)
        mutated["8"] += 1
        mutation_fires |= mutated != expected
        prime_results[str(prime)] = {
            "rank": len(pivots),
            "quotient_dimension": DIM - len(pivots),
            "character": character,
            "pivot_digest": sha256(repr(pivots).encode()).hexdigest(),
        }
    require(mutation_fires, "character mutation did not fire")

    result = {
        "status": "UNAUDITED exact modular S8-module audit",
        "ambient_dimension": DIM,
        "balanced_assignments": len(ASSIGNMENTS),
        "balanced_span_rank": 229,
        "annihilator_dimension": 27,
        "annihilator_decomposition": "6*S^(8) + 3*S^(7,1)",
        "expected_character": expected,
        "prime_results": prime_results,
        "mutation_fires": mutation_fires,
        "scope": (
            "This is the raw linear contrast-tensor quotient.  It does not "
            "by itself impose the nonlinear condition that the tensor comes "
            "from the 28 edge bilinear forms through the Hafnian map."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode()).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("contrast annihilator module audit: PASS")
    print("rank / quotient:", 229, 27)
    print("decomposition:", result["annihilator_decomposition"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
