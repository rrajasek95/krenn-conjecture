#!/usr/bin/env python3
"""Exact Hermitian least-star trace identity and hostile controls."""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "results_hermitian_star_trace.json"
GAUGE = ROOT / "computations/verify_minimal_norm_gauge.py"
STAR_OVERLAP = (ROOT / "computations/unaudited-codex-star-dual-overlap-2026-08-22"
                / "audit_star_dual_overlap.py")
PINS = {
    GAUGE: "bbd46d45976adc178261b7a01bcd6c3a4e6915ce4232131fb4d7ec07ababe94c",
    STAR_OVERLAP: "c6ec60aaa6fa41debb9bd2e8327656a8adee89808cc02cdbe11b08b9621a404a",
}

# Exact Q(omega), omega^2+omega+1=0, represented by a+b*omega.
ZERO = (Fraction(0), Fraction(0))
ONE = (Fraction(1), Fraction(0))
OMEGA = (Fraction(0), Fraction(1))
OMEGA2 = (Fraction(-1), Fraction(-1))


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def z(value):
    return (Fraction(value), Fraction(0))


def zadd(left, right):
    return left[0] + right[0], left[1] + right[1]


def zneg(value):
    return -value[0], -value[1]


def zsub(left, right):
    return zadd(left, zneg(right))


def zmul(left, right):
    a, b = left
    c, d = right
    return a*c-b*d, a*d+b*c-b*d


def zconj(value):
    a, b = value
    return a-b, -b


def zinv(value):
    norm = value[0]*value[0] - value[0]*value[1] + value[1]*value[1]
    require(norm != 0, value)
    conjugate = zconj(value)
    return conjugate[0]/norm, conjugate[1]/norm


def zdiv(left, right):
    return zmul(left, zinv(right))


def zsum(values):
    answer = ZERO
    for value in values:
        answer = zadd(answer, value)
    return answer


def znorm(value):
    result = zmul(zconj(value), value)
    require(result[1] == 0, result)
    return result[0]


def ztext(value):
    a, b = value
    if b == 0:
        return str(a)
    return f"({a})+({b})*omega"


def zreal(value):
    """Real part under omega=-1/2+i*sqrt(3)/2."""
    return value[0] - value[1]/2


def file_sha(path):
    return sha256(path.read_bytes()).hexdigest()


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def zpow_omega(exponent):
    return (ONE, OMEGA, OMEGA2)[exponent % 3]


def n4_source():
    layers = {
        0: ((0, 1), (2, 3)),
        1: ((0, 2), (1, 3)),
        2: ((0, 3), (1, 2)),
    }
    source = {}
    for colour, matching in layers.items():
        for edge in matching:
            matrix = [[ZERO for _ in range(3)] for _ in range(3)]
            matrix[colour][colour] = ONE
            source[edge] = tuple(tuple(row) for row in matrix)
    for edge in combinations(range(4), 2):
        source.setdefault(edge, tuple(tuple(ZERO for _ in range(3))
                                      for _ in range(3)))
    return source


FACTORS = (
    ((0, 1), (2, 3), (4, 5)),
    ((0, 5), (1, 2), (3, 4)),
    ((0, 2), (1, 4), (3, 5)),
    ((0, 3), (1, 5), (2, 4)),
    ((0, 4), (1, 3), (2, 5)),
)
PHASES = {(0, 5): OMEGA2, (3, 4): OMEGA2,
          (0, 4): OMEGA2, (2, 5): OMEGA}


def n6_source():
    fourier = tuple(tuple(zpow_omega(i*j) for j in range(3))
                    for i in range(3))
    source = {}
    for edge in FACTORS[0] + FACTORS[1]:
        source[edge] = fourier
    for colour, matching in enumerate(FACTORS[2:]):
        matrix = tuple(tuple(ONE if i == colour and j == colour else ZERO
                             for j in range(3)) for i in range(3))
        for edge in matching:
            source[edge] = matrix
    for edge, phase in PHASES.items():
        source[edge] = tuple(tuple(zmul(phase, value) for value in row)
                             for row in source[edge])
    require(set(source) == set(combinations(range(6), 2)), len(source))
    return source


def amplitudes(source, n):
    answer = {}
    for word in product(range(3), repeat=n):
        value = ZERO
        for matching in perfect_matchings(range(n)):
            term = ONE
            for u, v in matching:
                term = zmul(term, source[u, v][word[u]][word[v]])
            value = zadd(value, term)
        answer[word] = value
    return answer


def cofactor(source, word, residual):
    answer = ZERO
    for matching in perfect_matchings(residual):
        term = ONE
        for u, v in matching:
            term = zmul(term, source[u, v][word[u]][word[v]])
        answer = zadd(answer, term)
    return answer


def star_matrix(source, n, vertex):
    edges = tuple(edge for edge in combinations(range(n), 2) if vertex in edge)
    labels = tuple((*edge, a, b) for edge in edges
                   for a, b in product(range(3), repeat=2))
    words = tuple(product(range(3), repeat=n))
    rows = []
    for word in words:
        row = []
        for u, v, a, b in labels:
            if word[u] != a or word[v] != b:
                row.append(ZERO)
                continue
            residual = tuple(site for site in range(n) if site not in (u, v))
            row.append(cofactor(source, word, residual))
        rows.append(row)
    source_vector = [source[u, v][a][b] for u, v, a, b in labels]
    return words, labels, rows, source_vector


def hermitian_gram(rows):
    width = len(rows[0])
    gram = [[ZERO for _ in range(width)] for _ in range(width)]
    for row in rows:
        live = [(index, value) for index, value in enumerate(row)
                if value != ZERO]
        for i, left in live:
            for j, right in live:
                gram[i][j] = zadd(gram[i][j], zmul(zconj(left), right))
    return gram


def solve(matrix, vector):
    n = len(matrix)
    rows = [[matrix[i][j] for j in range(n)] + [vector[i]]
            for i in range(n)]
    for column in range(n):
        pivot = next((row for row in range(column, n)
                      if rows[row][column] != ZERO), None)
        require(pivot is not None, ("singular", column))
        rows[column], rows[pivot] = rows[pivot], rows[column]
        scale = zinv(rows[column][column])
        rows[column] = [zmul(scale, value) for value in rows[column]]
        for row in range(n):
            if row == column or rows[row][column] == ZERO:
                continue
            scale = rows[row][column]
            rows[row] = [zsub(left, zmul(scale, right))
                         for left, right in zip(rows[row], rows[column])]
    return [rows[i][-1] for i in range(n)]


def matvec(matrix, vector):
    return [zsum(zmul(value, coordinate)
                 for value, coordinate in zip(row, vector))
            for row in matrix]


def adjoint_matvec(matrix, vector):
    width = len(matrix[0])
    return [zsum(zmul(zconj(matrix[row][column]), vector[row])
                 for row in range(len(matrix)))
            for column in range(width)]


def inner(left, right):
    return zsum(zmul(zconj(a), b) for a, b in zip(left, right))


def least_star_control(source, n):
    output = amplitudes(source, n)
    pure_words = {(colour,)*n for colour in range(3)}
    records = []
    totals = Counter()
    sum_total = ZERO
    sum_pure = ZERO
    sum_mixed = ZERO
    for vertex in range(n):
        words, labels, matrix, source_vector = star_matrix(source, n, vertex)
        gram = hermitian_gram(matrix)
        coordinate = solve(gram, source_vector)
        least_dual = matvec(matrix, coordinate)
        require(adjoint_matvec(matrix, least_dual) == source_vector,
                (n, vertex, "normal equation"))
        output_vector = [output[word] for word in words]
        total = inner(least_dual, output_vector)
        pure = zsum(zmul(zconj(least_dual[index]), output[word])
                    for index, word in enumerate(words) if word in pure_words)
        mixed = zsub(total, pure)
        star_norm = sum(znorm(value) for value in source_vector)
        require(total == z(star_norm), (n, vertex, total, star_norm))
        records.append({
            "vertex": vertex,
            "star_columns": len(labels),
            "star_norm_squared": str(star_norm),
            "pairing_total": ztext(total),
            "pairing_pure": ztext(pure),
            "pairing_mixed": ztext(mixed),
            "least_dual_support": sum(value != ZERO for value in least_dual),
        })
        sum_total = zadd(sum_total, total)
        sum_pure = zadd(sum_pure, pure)
        sum_mixed = zadd(sum_mixed, mixed)
    source_norm = sum(znorm(value) for matrix in source.values()
                      for row in matrix for value in row)
    require(sum_total == z(2*source_norm),
            (n, sum_total, source_norm))
    require(zadd(sum_pure, sum_mixed) == sum_total,
            (sum_pure, sum_mixed, sum_total))
    mixed_output_count = sum(value != ZERO and word not in pure_words
                             for word, value in output.items())
    return {
        "n": n,
        "source_norm_squared": str(source_norm),
        "mixed_output_nonzero_count": mixed_output_count,
        "per_vertex": records,
        "summed_identity": {
            "left_2_source_norm_squared": str(2*source_norm),
            "all_output_pairing": ztext(sum_total),
            "pure_pairing": ztext(sum_pure),
            "mixed_pairing": ztext(sum_mixed),
            "pure_pairing_real_part": str(zreal(sum_pure)),
            "mixed_pairing_real_part": str(zreal(sum_mixed)),
            "opposite_omega_coefficients_cancel": sum_pure[1] == -sum_mixed[1],
        },
    }


def logical_sha(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--mutate-n4-mixed", action="store_true")
    args = parser.parse_args()
    for path, digest in PINS.items():
        require(file_sha(path) == digest, (str(path), file_sha(path), digest))
    n4 = least_star_control(n4_source(), 4)
    n6 = least_star_control(n6_source(), 6)
    if args.mutate_n4_mixed:
        n4["summed_identity"]["mixed_pairing"] = "1"
    require(n4["summed_identity"]["mixed_pairing"] == "0", n4)
    require(n6["summed_identity"]["mixed_pairing"] != "0", n6)
    payload = {
        "status": "PASS exact Hermitian least-star trace; terminal scalar no-go",
        "candidate_survey": [
            {
                "rank": 1,
                "candidate": "least-star positive pseudoinverse trace",
                "identity": (
                    "For Lambda_v=L_v(L_v^*L_v)^(-1)A_v*, "
                    "||A_v*||^2=<Lambda_v,F>. Summing vertices gives "
                    "2||A||^2=sum_v <Lambda_v,F>."
                ),
                "why_strongest": (
                    "It is Hermitian, regularity-free on each injective-star "
                    "chart, and uses the canonical least dual rather than an "
                    "arbitrary conormal gauge."
                ),
            },
            {
                "rank": 2,
                "candidate": "global conormal Euler trace",
                "identity": (
                    "If A=J_A^*lambda for a degree-m matching map, then "
                    "||A||^2=<lambda,J_A A>=m<lambda,F(A)>."
                ),
                "limitation": "Multiplier nonuniqueness and no sign on mixed pairing.",
            },
            {
                "rank": 3,
                "candidate": "matching-Gram/Fischer-Bombieri SOS",
                "identity": "||F||^2=3+sum_mixed |F_w|^2 at pure normalization",
                "limitation": (
                    "Only the trivial perfect-matching association-scheme "
                    "sector contributes; this restates X5 and supplies no "
                    "source-relative positive remainder."
                ),
            },
        ],
        "strongest_scalar_derivation": {
            "normal_equation": "A_v*=L_v^*Lambda_v",
            "star_reconstruction": "L_v(A_v*)=F(A), since each perfect matching uses one v-star edge",
            "paired": "||A_v*||^2=<Lambda_v,F(A)>",
            "summed": "2||A||^2=sum_v <Lambda_v,F(A)>",
            "GHZ_specialization": (
                "If every mixed F_w=0 and the three pure coefficients are 1, "
                "then 2||A||^2=sum_(v,c) conjugate(Lambda_v[c^n])."
            ),
            "mixed_equation_pairing": (
                "sum_v sum_(w mixed) conjugate(Lambda_v[w]) F_w=0. "
                "This is the exact scalar obtained by pairing and summing all "
                "mixed GHZ equations."
            ),
        },
        "controls": {
            "n4_exact_GHZ_global_minimum": n4,
            "n6_phased_block_injective_local_minimum": n6,
        },
        "terminal_verdict": (
            "The identity does use simultaneous mixed zeros and distinguishes "
            "the controls: the n4 mixed pairing is zero, while the phased n6 "
            "least-star mixed pairing is nonzero. But it gives no contradiction "
            "or positive mixed term. At GHZ the mixed contribution vanishes "
            "because the equations say so, leaving an unconstrained pure-dual "
            "trace equal to 2||A||^2. The least-star pseudoinverse is PSD as an "
            "operator, yet the pure/mixed cross decomposition is indefinite; "
            "no source-faithful SOS remainder survives."
        ),
    }
    payload["logical_sha256"] = logical_sha(payload)
    if args.write_results:
        HERE.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(payload["status"])
    print("n4", n4["summed_identity"])
    print("n6", n6["summed_identity"])
    print("logical", payload["logical_sha256"])


if __name__ == "__main__":
    main()
