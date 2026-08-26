#!/usr/bin/env python3
"""Bounded exact screen for the h=3 normalized B_ab=0 branch.

The screened stratum has six residual sites and a minimal diagonal q:
for each of the three colours its support is exactly a two-edge matching,
with unit coefficients.  We quotient these supports by S6 x S3.  For each
orbit and finite field, we test the selected physical equation

    q^[3] + (p_a s_b) q^[2] = 0

for every projective p_a supported on one or two decorated ports, while
s_b is completely unrestricted.  For fixed p_a this is an ordinary exact
linear system in the 18 coefficients of s_b.  This is deliberately a
small-stratum screen, not a full-source or characteristic-zero theorem.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_minimal_q_selected_row.json"
SITES = tuple(range(6))
COLOURS = tuple(range(3))
PORTS = tuple(product(SITES, COLOURS))
PORT_INDEX = {port: index for index, port in enumerate(PORTS)}
WORDS = tuple(product(COLOURS, repeat=6))
WORD_INDEX = {word: index for index, word in enumerate(WORDS)}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            answer.append(((min(first, second), max(first, second)),) + tail)
    return tuple(answer)


PM6 = perfect_matchings(SITES)
TWO_MATCHINGS = tuple(sorted({
    tuple(sorted(edges))
    for omitted in combinations(SITES, 2)
    for edges in perfect_matchings(tuple(x for x in SITES if x not in omitted))
}))
S6 = tuple(permutations(SITES))


def move_matching(matching, permutation):
    return tuple(sorted(
        (min(permutation[u], permutation[v]), max(permutation[u], permutation[v]))
        for u, v in matching
    ))


def canonical_triple(triple):
    return min(
        tuple(sorted(move_matching(matching, permutation) for matching in triple))
        for permutation in S6
    )


def q_orbit_representatives():
    representatives = {}
    for triple in combinations(TWO_MATCHINGS, 3):
        canonical = canonical_triple(triple)
        representatives.setdefault(canonical, triple)
    # Repeated colour supports are allowed, so add multiplicity types 2+1,3.
    for first in TWO_MATCHINGS:
        for second in TWO_MATCHINGS:
            triple = tuple(sorted((first, first, second)))
            canonical = canonical_triple(triple)
            representatives.setdefault(canonical, triple)
    return tuple(sorted(representatives))


def q_from_triple(triple, prime):
    q = {}
    for colour, matching in enumerate(triple):
        for u, v in matching:
            q[(u, v, colour, colour)] = 1 % prime
    return q


def q_entry(q, u, v, left_colour, right_colour):
    if u < v:
        return q.get((u, v, left_colour, right_colour), 0)
    return q.get((v, u, right_colour, left_colour), 0)


def hafnian(q, word, vertices, prime):
    total = 0
    for matching in perfect_matchings(vertices):
        term = 1
        for u, v in matching:
            term = (term * q_entry(q, u, v, word[u], word[v])) % prime
            if not term:
                break
        total = (total + term) % prime
    return total


def q_cube_and_cofactors(q, prime):
    cube = [0] * len(WORDS)
    cofactors = []
    for word_index, word in enumerate(WORDS):
        cube[word_index] = hafnian(q, word, SITES, prime)
        row = {}
        for u, v in combinations(SITES, 2):
            rest = tuple(x for x in SITES if x not in (u, v))
            value = hafnian(q, word, rest, prime)
            if value:
                row[(u, v)] = value
        cofactors.append(row)
    return tuple(cube), tuple(cofactors)


def selected_matrix(left, cofactors, prime):
    """Matrix s -> (left*s)q^[2], stored as sparse equation rows."""
    rows = []
    for word, cofactor_row in zip(WORDS, cofactors, strict=True):
        equation = [0] * len(PORTS)
        for (u, v), cofactor in cofactor_row.items():
            lu = left.get((u, word[u]), 0)
            lv = left.get((v, word[v]), 0)
            if lu:
                index = PORT_INDEX[(v, word[v])]
                equation[index] = (
                    equation[index] + lu * cofactor
                ) % prime
            if lv:
                index = PORT_INDEX[(u, word[u])]
                equation[index] = (
                    equation[index] + lv * cofactor
                ) % prime
        rows.append(equation)
    return rows


def rank_mod(rows, prime):
    rows = [list(value % prime for value in row) for row in rows if any(row)]
    if not rows:
        return 0
    columns = len(rows[0])
    rank = 0
    for column in range(columns):
        pivot = next((index for index in range(rank, len(rows))
                      if rows[index][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inverse = pow(rows[rank][column], prime - 2, prime)
        rows[rank] = [(entry * inverse) % prime for entry in rows[rank]]
        for index in range(len(rows)):
            if index == rank or not rows[index][column]:
                continue
            factor = rows[index][column]
            rows[index] = [
                (entry - factor * pivot_entry) % prime
                for entry, pivot_entry in zip(rows[index], rows[rank], strict=True)
            ]
        rank += 1
        if rank == len(rows):
            break
    return rank


def consistent(matrix, target, prime):
    rank = rank_mod(matrix, prime)
    augmented = [row + [value % prime]
                 for row, value in zip(matrix, target, strict=True)]
    return rank == rank_mod(augmented, prime), rank


def projective_lefts(prime):
    for port in PORTS:
        yield {port: 1}, (port,)
    for first, second in combinations(PORTS, 2):
        for ratio in range(1, prime):
            yield {first: 1, second: ratio}, (first, second)


def screen_prime(prime, representatives):
    orbit_records = []
    total_tests = 0
    total_solutions = 0
    for orbit_index, triple in enumerate(representatives):
        q = q_from_triple(triple, prime)
        cube, cofactors = q_cube_and_cofactors(q, prime)
        target = tuple((-value) % prime for value in cube)
        support_histogram = {"1": 0, "2": 0}
        rank_histogram = {}
        witnesses = []
        for left, support in projective_lefts(prime):
            matrix = selected_matrix(left, cofactors, prime)
            ok, rank = consistent(matrix, target, prime)
            total_tests += 1
            rank_histogram[str(rank)] = rank_histogram.get(str(rank), 0) + 1
            if ok:
                total_solutions += 1
                support_histogram[str(len(support))] += 1
                if len(witnesses) < 3:
                    witnesses.append({
                        "left_support": [[site, colour] for site, colour in support],
                        "left_coefficients": [left[port] for port in support],
                        "linear_rank": rank,
                    })
        orbit_records.append({
            "orbit": orbit_index,
            "triple": [[[u, v] for u, v in matching] for matching in triple],
            "q_cube_support": sum(value != 0 for value in cube),
            "selected_row_solutions": sum(support_histogram.values()),
            "solution_support_histogram": support_histogram,
            "linear_rank_histogram": rank_histogram,
            "witnesses_without_right_solution_export": witnesses,
        })
    return {
        "prime": prime,
        "tests": total_tests,
        "selected_row_solutions": total_solutions,
        "orbits_with_solution": sum(
            record["selected_row_solutions"] > 0 for record in orbit_records
        ),
        "orbits": orbit_records,
    }


def build():
    representatives = q_orbit_representatives()
    require(len(TWO_MATCHINGS) == 45, len(TWO_MATCHINGS))
    result = {
        "status": "PASS bounded exact finite-field selected-row screen",
        "scope": (
            "q has exactly two unit diagonal edges per colour; supports are "
            "quotiented by S6 x S3. The selected left star is projective "
            "with one or two decorated ports; the selected right star is "
            "unrestricted. This is not the complete nine-row system and "
            "does not imply a characteristic-zero theorem."
        ),
        "equation": "q^[3] + (p_a*s_b) q^[2] = 0",
        "q_support_orbits": len(representatives),
        "primes": [screen_prime(prime, representatives) for prime in (5, 7)],
    }
    logical = sha256(json.dumps(result, sort_keys=True,
                                separators=(",", ":")).encode()).hexdigest()
    result["logical_sha256"] = logical
    return result


def main(write_results=False):
    result = build()
    if write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "q_support_orbits": result["q_support_orbits"],
        "prime_summaries": [{
            key: row[key] for key in
            ("prime", "tests", "selected_row_solutions", "orbits_with_solution")
        } for row in result["primes"]],
        "logical_sha256": result["logical_sha256"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    main(args.write_results)
