#!/usr/bin/env python3
"""Exact audit of the fixed-cap response transition/holonomy construction.

The point of the audit is deliberately negative.  On one fixed cap pair all
response-edge maps have the same domain Mat_3.  If they are invertible, the
only canonical transition is therefore a change of coordinates.  Its face
holonomy is an adjugate identity, before any amplitude equation is imposed.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_fullrank_response_holonomy.json"
COLOURS = range(3)
CAP = (6, 7)
TETRAHEDRON = (0, 1, 2, 3)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def zero_matrix(n, m):
    return [[Fraction(0) for _ in range(m)] for _ in range(n)]


def identity(n):
    answer = zero_matrix(n, n)
    for i in range(n):
        answer[i][i] = Fraction(1)
    return answer


def transpose(a):
    return [list(row) for row in zip(*a)]


def matmul(a, b):
    require(len(a[0]) == len(b), (len(a[0]), len(b)))
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(row, column))
             for column in bt] for row in a]


def matsub(a, b):
    return [[x - y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def scalar_matrix(c, a):
    return [[c * x for x in row] for row in a]


def determinant(a):
    """Fraction-free Bareiss determinant."""
    work = [list(map(Fraction, row)) for row in a]
    n = len(work)
    require(all(len(row) == n for row in work), "determinant not square")
    sign = 1
    previous = Fraction(1)
    for k in range(n - 1):
        pivot = next((r for r in range(k, n) if work[r][k]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != k:
            work[k], work[pivot] = work[pivot], work[k]
            sign *= -1
        value = work[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                work[i][j] = (
                    work[i][j] * value - work[i][k] * work[k][j]
                ) / previous
        previous = value
    return Fraction(sign) * work[n - 1][n - 1]


def inverse(a):
    n = len(a)
    work = [list(map(Fraction, row)) + identity(n)[i]
            for i, row in enumerate(a)]
    for column in range(n):
        pivot = next((r for r in range(column, n) if work[r][column]), None)
        require(pivot is not None, "singular matrix")
        work[column], work[pivot] = work[pivot], work[column]
        value = work[column][column]
        work[column] = [entry / value for entry in work[column]]
        for row in range(n):
            if row == column or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [x - value * y
                         for x, y in zip(work[row], work[column])]
    return [row[n:] for row in work]


def matrix_rank(a):
    work = [list(map(Fraction, row)) for row in a]
    if not work:
        return 0
    ncols = len(work[0])
    rank = 0
    for column in range(ncols):
        pivot = next((r for r in range(rank, len(work)) if work[r][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        value = work[rank][column]
        work[rank] = [entry / value for entry in work[rank]]
        for row in range(len(work)):
            if row == rank or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [x - value * y for x, y in zip(work[row], work[rank])]
        rank += 1
        if rank == len(work):
            break
    return rank


def dense_stored_block(residual, endpoint):
    """The pinned dense-control formula, in stored residual/endpoint order."""
    return [[Fraction(
        1 + ((((residual * 8 + endpoint) * 9 + a * 3 + b + 1) ** 2
              + 17 * residual + 29 * endpoint + 5 * a + 7 * b) % 97)
    ) for b in COLOURS] for a in COLOURS]


def build_star_only_source():
    zero = zero_matrix(3, 3)
    source = {(u, v): [row[:] for row in zero]
              for u in range(8) for v in range(u + 1, 8)}
    for endpoint in CAP:
        for residual in range(6):
            source[(residual, endpoint)] = dense_stored_block(
                residual, endpoint)
    return source


def block(source, u, v):
    """Endpoint-ordered 3x3 block, rows at u and columns at v."""
    if u < v:
        return source[(u, v)]
    return transpose(source[(v, u)])


def cell(source, u, v, a, b):
    return block(source, u, v)[a][b]


def response_map(source, a, b, mutate=False):
    """Rows alpha,beta and columns i,j of the literal R_ab map."""
    rows = []
    for alpha in COLOURS:
        for beta in COLOURS:
            row = []
            for i in COLOURS:
                for j in COLOURS:
                    first = cell(source, 6, a, i, alpha) * cell(
                        source, 7, b, j, beta)
                    if mutate:
                        second = cell(source, 6, b, i, alpha) * cell(
                            source, 7, a, j, beta)
                    else:
                        second = cell(source, 6, b, i, beta) * cell(
                            source, 7, a, j, alpha)
                    row.append(first + second)
            rows.append(row)
    return rows


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


MATCHINGS = perfect_matchings(range(8))


def amplitude(source, word):
    total = Fraction(0)
    for matching in MATCHINGS:
        term = Fraction(1)
        for u, v in matching:
            term *= cell(source, u, v, word[u], word[v])
            if not term:
                break
        total += term
    return total


def cross_word_matrix(source, residual_word):
    require(len(residual_word) == 6, residual_word)
    return [[amplitude(source, tuple(map(int, residual_word)) + (i, j))
             for j in COLOURS] for i in COLOURS]


def adjugate_from_inverse(matrix, determinant_value):
    return scalar_matrix(determinant_value, inverse(matrix))


def transition_numerator(target_map, source_adjugate):
    return matmul(target_map, source_adjugate)


def face_defect(maps, determinants, adjugates, face):
    """Cleared U->V->W->U transition holonomy."""
    a, b, c = face
    u, v, w = (a, b), (a, c), (b, c)
    n_vu = transition_numerator(maps[v], adjugates[u])
    n_wv = transition_numerator(maps[w], adjugates[v])
    n_uw = transition_numerator(maps[u], adjugates[w])
    left = matmul(n_uw, matmul(n_wv, n_vu))
    right = scalar_matrix(determinants[u] * determinants[v] * determinants[w],
                          identity(9))
    return matsub(left, right)


def even_cycle_transport(source, cycle):
    """Gauge-covariant endomorphism at the first vertex of a 4-cycle."""
    a, b, c, d = cycle
    return matmul(
        transpose(inverse(block(source, a, d))),
        matmul(transpose(block(source, c, d)),
               matmul(inverse(block(source, b, c)),
                      transpose(block(source, a, b)))),
    )


def fraction_string(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def logical_digest(payload):
    return sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"))
                  .encode()).hexdigest()


def source_digest(source):
    payload = [
        [u, v, [[fraction_string(value) for value in row] for row in matrix]]
        for (u, v), matrix in sorted(source.items())
    ]
    return sha256(json.dumps(payload, separators=(",", ":")).encode()).hexdigest()


def run(mutate=False):
    source = build_star_only_source()
    edges = tuple(combinations(TETRAHEDRON, 2))
    maps = {edge: response_map(source, *edge, mutate=mutate) for edge in edges}
    determinants = {edge: determinant(matrix) for edge, matrix in maps.items()}
    require(all(determinants.values()), ("rank-nine edge failed", determinants))
    adjugates = {edge: adjugate_from_inverse(maps[edge], determinants[edge])
                 for edge in edges}
    for edge in edges:
        require(matmul(maps[edge], adjugates[edge]) ==
                scalar_matrix(determinants[edge], identity(9)), edge)

    faces = tuple(combinations(TETRAHEDRON, 3))
    defects = {face: face_defect(maps, determinants, adjugates, face)
               for face in faces}
    require(all(not any(any(row) for row in defect)
                for defect in defects.values()), "nonzero face holonomy")

    # Two literal full-X5 cross-word packets.  The star-only guard kills all
    # amplitudes, since after matching 6 and 7 four residual vertices remain
    # but every residual-residual block is zero.
    residual_words = ("001122", "012012")
    word_matrices = {word: cross_word_matrix(source, word)
                     for word in residual_words}
    require(all(not any(any(row) for row in matrix)
                for matrix in word_matrices.values()), word_matrices)
    all_amplitudes = [amplitude(source, word)
                      for word in __import__("itertools").product(range(3), repeat=8)]
    require(not any(all_amplitudes), "star-only source has a top amplitude")

    # The corresponding X5-decorated transition identity is already an
    # adjugate identity for an arbitrary 3x3 row packet E.  Test it on a
    # hostile nonzero formal E so the zero amplitudes do not make it vacuous.
    formal_e = [[Fraction(1 + 3 * i + j) for j in COLOURS]
                for i in COLOURS]
    evec = [[formal_e[i][j] for i in COLOURS for j in COLOURS]]
    decorated_checks = []
    for source_edge, target_edge in zip(edges, edges[1:] + edges[:1]):
        lhs = matmul(evec, matmul(adjugates[target_edge],
                                  matmul(maps[target_edge], adjugates[source_edge])))
        rhs = scalar_matrix(determinants[target_edge],
                            matmul(evec, adjugates[source_edge]))
        require(lhs == rhs, (source_edge, target_edge))
        decorated_checks.append((source_edge, target_edge))

    # A simultaneous site-colour gauge to diagonal edge blocks would make
    # all even-cycle transports at site 6 diagonal, hence commuting.
    h1 = even_cycle_transport(source, (6, 0, 7, 1))
    h2 = even_cycle_transport(source, (6, 0, 7, 2))
    commutator = matsub(matmul(h1, h2), matmul(h2, h1))
    commutator_rank = matrix_rank(commutator)
    require(commutator_rank > 0, "guard accidentally channel diagonalizable")
    first_nonzero = next((i, j, commutator[i][j])
                         for i in range(3) for j in range(3)
                         if commutator[i][j])

    determinant_strings = {
        f"{a}{b}": fraction_string(value)
        for (a, b), value in determinants.items()
    }
    core = {
        "status": "PASS exact full-rank response holonomy no-go",
        "cap_pair": list(CAP),
        "residual_tetrahedron": list(TETRAHEDRON),
        "response_edge_labels": [f"R_{a}{b}:alpha,beta<-i,j"
                                 for a, b in edges],
        "response_edge_determinants": determinant_strings,
        "response_edge_ranks": {f"{a}{b}": 9 for a, b in edges},
        "triangle_carrier_selected_minors": {
            "012": "R_03", "013": "R_02",
            "023": "R_01", "123": "R_01",
        },
        "face_labels": ["".join(map(str, face)) for face in faces],
        "cleared_face_defect": {
            "formula": "N_uw N_wv N_vu - delta_u delta_v delta_w I_9",
            "N_vu": "R_v adj(R_u)",
            "source_degree": 54,
            "entry_count": 4 * 81,
            "all_entries_zero": True,
            "reason": "adj(R)R=R adj(R)=det(R)I; no X5 row is used",
        },
        "literal_cross_word_packets": {
            "residual_words": list(residual_words),
            "full_words": [word + str(i) + str(j)
                           for word in residual_words
                           for i in COLOURS for j in COLOURS],
            "row_count": 18,
            "profile_histogram": {"3+3+2": 12, "4+2+2": 6},
            "all_zero_on_guard": True,
            "decorated_pair_defect_degree": 38,
            "decorated_identity": (
                "E^T adj(R_f) R_f adj(R_e) "
                "- det(R_f) E^T adj(R_e)=0"
            ),
            "formal_nonzero_E_checked": True,
            "conclusion": (
                "Transporting a literal X5 cap-word packet is functorial "
                "for every E, so E=0 supplies no curvature."
            ),
        },
        "counterguard": {
            "support": "only the 12 cap-star blocks A_6a,A_7a (0<=a<=5)",
            "source_sha256": source_digest(source),
            "all_6561_top_amplitudes_zero": True,
            "therefore_all_mixed_X5_rows_zero": True,
            "pure_normalization_values": [0, 0, 0],
            "even_cycles": ["6-0-7-1-6", "6-0-7-2-6"],
            "cycle_commutator_rank": commutator_rank,
            "first_nonzero_commutator_entry": [
                first_nonzero[0], first_nonzero[1],
                fraction_string(first_nonzero[2]),
            ],
            "meaning": (
                "The selected full-rank response maps and every homogeneous "
                "mixed X5 row do not force a simultaneous channel gauge. "
                "The guard is outside normalized X5 because its pure rows "
                "are zero."
            ),
        },
        "verdict": (
            "On one fixed cap pair, invertible response-edge maps give only "
            "coordinate changes on the same Mat_3. Their nonlinear triangle "
            "and tetrahedron holonomies are universal adjugate identities. "
            "A non-tautological theorem must add a transition between genuinely "
            "different cap/source quotients or a normalized pure-row coupling."
        ),
        "mutation": mutate,
    }
    core["logical_sha256"] = logical_digest(core)
    return core


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    parser.add_argument("--mutate-crossed-orientation", action="store_true")
    args = parser.parse_args()
    result = run(mutate=args.mutate_crossed_orientation)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.mutate_crossed_orientation:
        require(OUT.exists() and OUT.read_text() == text,
                "PASS hostile crossed-orientation mutation changed the artifact")
    if args.check_results:
        require(OUT.exists(), "missing result artifact")
        require(OUT.read_text() == text, "result artifact mismatch")
    if args.write_results:
        OUT.write_text(text)
    print(json.dumps({
        "status": result["status"],
        "logical_sha256": result["logical_sha256"],
        "commutator_rank": result["counterguard"]["cycle_commutator_rank"],
        "face_defects_zero": result["cleared_face_defect"]["all_entries_zero"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
