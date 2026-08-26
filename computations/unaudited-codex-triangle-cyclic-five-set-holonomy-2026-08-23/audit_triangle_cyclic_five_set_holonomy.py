#!/usr/bin/env python3
"""Exact literal-term audit of the three cyclic triangle five-set identities."""

from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
import argparse
import json
import sys


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_triangle_cyclic_five_set_holonomy.json"
P, Q = 6, 7
TRIANGLE = {0, 1, 2}
OUTSIDE = {3, 4, 5}


def edge(u, v):
    return (u, v) if u < v else (v, u)


def cell(u, v, a, b):
    return (u, v, a, b) if u < v else (v, u, b, a)


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


def survivor_matchings(t):
    x, y = sorted(TRIANGLE - {t})
    answer = set()
    for u in OUTSIDE:
        a, b = sorted(OUTSIDE - {u})
        answer.add(tuple(sorted((edge(t, u), edge(a, b), edge(P, x), edge(Q, y)))))
        answer.add(tuple(sorted((edge(t, u), edge(a, b), edge(P, y), edge(Q, x)))))
    assert len(answer) == 6
    return answer


def response_formal_support(a, b, mutate=False):
    """All labelled coefficient monomials of R_ab: 9 output x 9 K x 2."""
    answer = set()
    for alpha, beta, i, j in product(range(3), repeat=4):
        first = tuple(sorted((cell(P, a, i, alpha), cell(Q, b, j, beta))))
        second_beta = alpha if mutate else beta
        second_alpha = beta if mutate else alpha
        second = tuple(sorted((
            cell(P, b, i, second_beta), cell(Q, a, j, second_alpha)
        )))
        answer.add((alpha, beta, i, j, 0, first))
        answer.add((alpha, beta, i, j, 1, second))
    assert len(answer) == 162
    return answer


def zeros():
    return [[0] * 3 for _ in range(3)]


def identity():
    return [[int(i == j) for j in range(3)] for i in range(3)]


def e00():
    value = zeros()
    value[0][0] = 1
    return value


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def set_oriented(blocks, u, v, matrix):
    blocks[edge(u, v)] = matrix if u < v else transpose(matrix)


def oriented(blocks, u, v):
    matrix = blocks.get(edge(u, v), zeros())
    return matrix if u < v else transpose(matrix)


def response_rows(blocks, a, b):
    p_a = oriented(blocks, P, a)
    p_b = oriented(blocks, P, b)
    q_a = oriented(blocks, Q, a)
    q_b = oriented(blocks, Q, b)
    rows = []
    for alpha, beta in product(range(3), repeat=2):
        rows.append([
            p_a[i][alpha] * q_b[j][beta]
            + p_b[i][beta] * q_a[j][alpha]
            for i, j in product(range(3), repeat=2)
        ])
    return rows


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
        scale = matrix[rank][column]
        matrix[rank] = [value / scale for value in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [
                value - scale * pivot_value
                for value, pivot_value in zip(matrix[row], matrix[rank])
            ]
        rank += 1
    return rank


def in_rowspan(row, rows):
    return matrix_rank(rows + [row]) == matrix_rank(rows)


def response_level_guard():
    blocks = {}
    # Triangle star data: R_01(K)=K, R_02(K)=K, R_12(K)=K^T.
    set_oriented(blocks, P, 0, identity())
    set_oriented(blocks, Q, 0, zeros())
    set_oriented(blocks, P, 1, zeros())
    set_oriented(blocks, Q, 1, identity())
    set_oriented(blocks, P, 2, identity())
    set_oriented(blocks, Q, 2, identity())
    # One outside response inserts K_00 into L.  Cross terms enlarge L but
    # leave K_11 and K_22 outside it.
    set_oriented(blocks, P, 3, e00())
    set_oriented(blocks, Q, 4, e00())
    set_oriented(blocks, P, Q, identity())

    outside_edges = [
        ab for ab in combinations(range(6), 2) if not set(ab) <= TRIANGLE
    ]
    assert len(outside_edges) == 12
    l_rows = [
        row for a, b in outside_edges for row in response_rows(blocks, a, b)
    ]
    assert len(l_rows) == 108
    assert matrix_rank(l_rows) == 5

    diagonals = []
    for index in (0, 4, 8):
        row = [0] * 9
        row[index] = 1
        diagonals.append(row)
    direct = [int(i == j) for i, j in product(range(3), repeat=2)]
    memberships = [in_rowspan(row, l_rows) for row in diagonals]
    assert memberships == [True, False, False]
    assert not in_rowspan(direct, l_rows)

    triangle_rows = {
        edge(a, b): response_rows(blocks, a, b)
        for a, b in combinations(sorted(TRIANGLE), 2)
    }
    assert all(matrix_rank(rows) == 9 for rows in triangle_rows.values())
    increments = {
        f"{a}{b}": matrix_rank(l_rows + rows) - matrix_rank(l_rows)
        for (a, b), rows in triangle_rows.items()
    }
    assert set(increments.values()) == {4}

    # The same selected blocker K_11 is literally the output-(1,1) row of
    # all three responses, so all cyclic augmented identities can hold with
    # b=e_1 and theta selecting that output coordinate.
    selected = diagonals[1]
    for rows in triangle_rows.values():
        assert rows[4] == selected
        assert in_rowspan(selected, l_rows + rows)
    assert not in_rowspan(selected, l_rows)

    return {
        "literal_nonzero_star_blocks": [
            "A_60=I", "A_70=0", "A_61=0", "A_71=I",
            "A_62=I", "A_72=I", "A_63=E00", "A_74=E00",
            "A_67=I",
        ],
        "L_triangle_rank": matrix_rank(l_rows),
        "diagonal_memberships_K00_K11_K22": memberships,
        "direct_membership": in_rowspan(direct, l_rows),
        "triangle_response_maps": {
            "R_01": "K",
            "R_02": "K",
            "R_12": "transpose(K)",
        },
        "triangle_response_rank_increments_mod_L": increments,
        "common_augmented_blocker": "K_11",
        "common_augmented_blocker_in_L": False,
        "carrier_active": False,
        "why_not_active": "K_00 is already in rowspan(L_triangle)",
        "scope": (
            "literal response-star/rowspace counterguard; the theta maps "
            "are the named diagonal projections with b=e_1.  This is not "
            "a simultaneous internal-cofactor realization or normalized X5 point."
        ),
    }


def audit(mutate=False):
    survivor_sets = {t: survivor_matchings(t) for t in sorted(TRIANGLE)}
    intersections = {
        f"{a}{b}": len(survivor_sets[a].intersection(survivor_sets[b]))
        for a, b in combinations(sorted(TRIANGLE), 2)
    }
    assert intersections == {"01": 0, "02": 0, "12": 0}
    assert len(set().union(*survivor_sets.values())) == 18

    formal_supports = {
        edge(a, b): response_formal_support(a, b, mutate=mutate)
        for a, b in combinations(sorted(TRIANGLE), 2)
    }
    support_intersections = {
        f"{a[0]}{a[1]}_{b[0]}{b[1]}": len(
            formal_supports[a].intersection(formal_supports[b])
        )
        for a, b in combinations(sorted(formal_supports), 2)
    }
    assert set(support_intersections.values()) == {0}
    assert len(set().union(*formal_supports.values())) == 486
    if mutate:
        raise RuntimeError("hostile crossed-endpoint mutation was not source-faithful")

    guard = response_level_guard()
    result = {
        "status": "PASS cyclic five-set has no source-universal response holonomy",
        "canonical_carrier": {
            "cap_pair": [P, Q],
            "triangle": sorted(TRIANGLE),
            "outside": sorted(OUTSIDE),
        },
        "literal_sector_audit": {
            "survivors_per_cycle": {
                str(t): len(value) for t, value in survivor_sets.items()
            },
            "pairwise_survivor_intersections": intersections,
            "union_survivor_matchings": 18,
            "formal_response_terms_per_edge": 162,
            "formal_response_union": 486,
            "formal_response_pairwise_intersections": support_intersections,
            "consequence": (
                "no nonzero source-universal linear combination of the "
                "three cyclic residual packets cancels termwise"
            ),
        },
        "response_level_counterguard": guard,
        "sharp_positive_open": {
            "condition": (
                "for every needed (t,c), the five-set quotient map from "
                "annihilators with beta(e_c^5)=0 onto Mat_3^* has rank 9"
            ),
            "consequence": (
                "each omitted R_xy row already belongs to rowspan(L_T), "
                "so the augmented identity gives b_c*K_cc in rowspan(L_T)"
            ),
            "role_of_cycle": "none; the three edges are absorbed separately",
        },
        "terminal_verdict": (
            "The three universal five-set identities alone imply neither "
            "ell in rowspan(L_T) nor an active clean cap.  A global proof "
            "must use the rank-nine open separately and route the rank-drop "
            "boundary through literal cross-word/full-X5 coupling."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode()).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    parser.add_argument("--mutate-crossed-orientation", action="store_true")
    args = parser.parse_args()
    result = audit(args.mutate_crossed_orientation)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_results:
        OUT.write_text(text)
    if args.check_results:
        assert OUT.read_text() == text
    print(text, end="")


if __name__ == "__main__":
    main()
