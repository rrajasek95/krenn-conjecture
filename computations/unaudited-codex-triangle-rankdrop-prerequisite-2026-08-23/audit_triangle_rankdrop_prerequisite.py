#!/usr/bin/env python3
"""Exact sparse-minor and frozen-packet audit for L_(67,012)."""

from fractions import Fraction
from hashlib import sha256
from itertools import product
from pathlib import Path
import argparse
import json
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = (
    ROOT
    / "computations/unaudited-codex-rootless-fine-macaulay-2026-08-22"
    / "results_closure22_plus_full_profile71_joint_cegar_rust_p32003.json"
)
OUT = HERE / "results_triangle_rankdrop_prerequisite.json"
P, Q = 6, 7
TRIANGLE = {0, 1, 2}
MINOR_EDGE = (0, 3)
UNIVERSAL_EDGES = {(0, 6), (3, 7)}


def edge(u, v):
    return (u, v) if u < v else (v, u)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted((edge(first, second),) + tail))


MATCHINGS = tuple(perfect_matchings(range(8)))


def matching_count(vertices, allowed_edges):
    vertices = tuple(sorted(vertices))
    if len(vertices) % 2:
        return 0
    return sum(
        all(pair in allowed_edges for pair in matching)
        for matching in perfect_matchings(vertices)
    )


def packet_words():
    payload = json.loads(SOURCE.read_text())
    words = tuple(payload["source_words"])
    assert len(words) == 62
    assert len(set(words)) == 62
    assert all(len(word) == 8 and set(word) <= set("012") for word in words)
    return words


def find_diagonal_packet_guard(words):
    # A_60=A_73=I supplies the two universal diagonal edges.  For colour c,
    # add the diagonal c,c cells on one perfect matching M_c.  Retain only
    # matchings for which the c^8 amplitude is exactly one.
    candidates = []
    for matching in MATCHINGS:
        allowed = set(matching) | UNIVERSAL_EDGES
        if matching_count(range(8), allowed) != 1:
            continue
        masks = []
        for colour in range(3):
            mask = 0
            for index, word in enumerate(words):
                vertices = [site for site, value in enumerate(word) if int(value) == colour]
                if matching_count(vertices, allowed):
                    mask |= 1 << index
            masks.append(mask)
        candidates.append((matching, masks))
    assert candidates

    for matching0, masks0 in candidates:
        for matching1, masks1 in candidates:
            partial = masks0[0] & masks1[1]
            for matching2, masks2 in candidates:
                if partial & masks2[2] == 0:
                    chosen = (matching0, matching1, matching2)
                    amplitudes = {}
                    for word in words:
                        value = 1
                        for colour, matching in enumerate(chosen):
                            allowed = set(matching) | UNIVERSAL_EDGES
                            vertices = [
                                site for site, symbol in enumerate(word)
                                if int(symbol) == colour
                            ]
                            value *= matching_count(vertices, allowed)
                        amplitudes[word] = value
                    assert not any(amplitudes.values())
                    pure = {
                        str(colour): matching_count(
                            range(8), set(chosen[colour]) | UNIVERSAL_EDGES
                        )
                        for colour in range(3)
                    }
                    assert pure == {"0": 1, "1": 1, "2": 1}
                    all_mixed_nonzero = {}
                    for symbols in product(range(3), repeat=8):
                        if len(set(symbols)) == 1:
                            continue
                        word = "".join(str(symbol) for symbol in symbols)
                        value = 1
                        for colour, matching in enumerate(chosen):
                            allowed = set(matching) | UNIVERSAL_EDGES
                            vertices = [
                                site for site, symbol in enumerate(symbols)
                                if symbol == colour
                            ]
                            value *= matching_count(vertices, allowed)
                        if value:
                            all_mixed_nonzero[word] = value
                    assert len(all_mixed_nonzero) == 22
                    profile_census = {}
                    for word in all_mixed_nonzero:
                        profile = tuple(
                            sorted((word.count(str(c)) for c in range(3) if str(c) in word),
                                   reverse=True)
                        )
                        key = "+".join(str(value) for value in profile)
                        profile_census[key] = profile_census.get(key, 0) + 1
                    assert profile_census == {"6+2": 8, "4+4": 6, "4+2+2": 8}
                    return {
                        "candidate_matching_count": len(candidates),
                        "colour_matchings": [
                            [list(pair) for pair in matching] for matching in chosen
                        ],
                        "packet_word_count": len(words),
                        "packet_nonzero_amplitudes": {
                            word: value for word, value in amplitudes.items() if value
                        },
                        "pure_amplitudes": pure,
                        "full_X5_nonzero_mixed_amplitudes": all_mixed_nonzero,
                        "full_X5_nonzero_profile_census": profile_census,
                    }
    raise AssertionError("no diagonal packet guard found")


def zeros():
    return [[0] * 3 for _ in range(3)]


def identity():
    return [[int(i == j) for j in range(3)] for i in range(3)]


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def oriented(blocks, u, v):
    matrix = blocks.get(edge(u, v), zeros())
    return matrix if u < v else transpose(matrix)


def response_rows(blocks, a, b):
    p_a = oriented(blocks, P, a)
    p_b = oriented(blocks, P, b)
    q_a = oriented(blocks, Q, a)
    q_b = oriented(blocks, Q, b)
    return [
        [
            p_a[i][alpha] * q_b[j][beta]
            + p_b[i][beta] * q_a[j][alpha]
            for i, j in product(range(3), repeat=2)
        ]
        for alpha, beta in product(range(3), repeat=2)
    ]


def determinant(matrix):
    matrix = [[Fraction(value) for value in row] for row in matrix]
    answer = Fraction(1)
    for column in range(len(matrix)):
        pivot = next(
            (row for row in range(column, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
            answer *= -1
        value = matrix[column][column]
        answer *= value
        matrix[column] = [entry / value for entry in matrix[column]]
        for row in range(column + 1, len(matrix)):
            value = matrix[row][column]
            if not value:
                continue
            matrix[row] = [
                entry - value * pivot_entry
                for entry, pivot_entry in zip(matrix[row], matrix[column])
            ]
    return answer


def sparse_minor_guard(diagonal_guard):
    blocks = {}
    blocks[edge(0, 6)] = identity()
    blocks[edge(3, 7)] = identity()
    for colour, matching in enumerate(diagonal_guard["colour_matchings"]):
        for u, v in matching:
            matrix = blocks.setdefault(edge(u, v), zeros())
            matrix[colour][colour] = 1

    minor = response_rows(blocks, *MINOR_EDGE)
    # The reversed-edge convention gives P_0=A_60=I, Q_3=A_73=I,
    # while P_3=Q_0=0.  Hence R_03(K)=K, with the same row/column order.
    assert minor == identity_operator(9)
    assert determinant(minor) == 1

    outside_edges = [
        pair for pair in (edge(a, b) for a in range(6) for b in range(a + 1, 6))
        if not set(pair) <= TRIANGLE
    ]
    l_rows = [
        row for pair in outside_edges for row in response_rows(blocks, *pair)
    ]
    assert len(l_rows) == 108
    rank = matrix_rank(l_rows)
    assert rank == 9
    return {
        "selected_rows": "all nine output-cell rows of R_03 inside L_(67,012)",
        "minor_polynomial": "Delta_03=det(K -> P_0^T K Q_3 + Q_0^T K^T P_3)",
        "total_degree": 18,
        "specialization": "P_0=I,Q_3=I,P_3=Q_0=0",
        "specialized_operator": "identity on Mat_3",
        "specialized_minor": 1,
        "specialized_L_rank": rank,
    }


def identity_operator(size):
    return [[int(i == j) for j in range(size)] for i in range(size)]


def matrix_rank(rows):
    if not rows:
        return 0
    matrix = [[Fraction(value) for value in row] for row in rows]
    rank = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (row for row in range(rank, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        value = matrix[rank][column]
        matrix[rank] = [entry / value for entry in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [
                entry - value * pivot_entry
                for entry, pivot_entry in zip(matrix[row], matrix[rank])
            ]
        rank += 1
    return rank


def audit():
    words = packet_words()
    diagonal_guard = find_diagonal_packet_guard(words)
    minor = sparse_minor_guard(diagonal_guard)
    source_digest = sha256(SOURCE.read_bytes()).hexdigest()
    result = {
        "status": "PASS frozen 62-word packet does not force triangle rank drop",
        "canonical_carrier": {
            "cap_pair": [P, Q],
            "triangle": sorted(TRIANGLE),
            "outside": [3, 4, 5],
        },
        "sparse_minor": minor,
        "literal_diagonal_counterguard": diagonal_guard,
        "packet_scope": {
            "source": str(SOURCE.relative_to(ROOT)),
            "source_sha256": source_digest,
            "abstract_words": 62,
            "translation_degree": 13,
            "minor_degree": 18,
            "conclusion": (
                "Even after adjoining the three pure normalizations, the literal "
                "62 amplitude rows vanish at a source with Delta_03=1.  Therefore "
                "Delta_03 is not in that literal packet ideal.  The frozen abstract "
                "degree-13 semigroup quotient is weaker still and cannot certify its "
                "degree-18 reduction."
            ),
        },
        "scope_guard": (
            "The constructed source is not a full normalized X5 point: unlisted "
            "mixed amplitudes may be nonzero.  Thus this disproves rank drop from "
            "the strongest frozen closure22/profile71 packet, not from the complete "
            "6558-row normalized X5 ideal."
        ),
        "smallest_unresolved_test": (
            "Any extension capable of excluding this guard must use at least one "
            "of its 22 nonzero unlisted mixed rows (profiles 6+2, 4+4, and 4+2+2). "
            "The exact global target remains reduction of Delta_03 in the complete "
            "normalized X5 ideal, or a saturation unit on Delta_03!=0."
        ),
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(canonical.encode()).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-results", action="store_true")
    args = parser.parse_args()
    result = audit()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.check_results:
        if not OUT.exists() or OUT.read_text() != rendered:
            print("frozen result mismatch", file=sys.stderr)
            return 1
        print(result["status"], result["logical_sha256"])
        return 0
    OUT.write_text(rendered)
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
