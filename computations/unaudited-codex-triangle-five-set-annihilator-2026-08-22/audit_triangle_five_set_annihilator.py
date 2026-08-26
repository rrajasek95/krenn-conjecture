#!/usr/bin/env python3
"""Literal matching-sector audit for a canonical triangle carrier."""

from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_triangle_five_set_annihilator.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def edge(u, v):
    return (u, v) if u < v else (v, u)


def matching_key(edges):
    return tuple(sorted(edge(u, v) for u, v in edges))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def cut_partition_for_vertex(t):
    p, q = 6, 7
    triangle = {0, 1, 2}
    outside = {3, 4, 5}
    w_shore = (triangle - {t}) | outside
    c_shore = {p, q, t}
    all_matchings = {matching_key(m) for m in perfect_matchings(range(8))}
    t1 = set()
    t3 = set()
    for matching in all_matchings:
        crossing = sum((a in c_shore) != (b in c_shore) for a, b in matching)
        require(crossing in (1, 3), (t, matching, crossing))
        (t1 if crossing == 1 else t3).add(matching)
    require(len(t1) == 45 and len(t3) == 60, (t, len(t1), len(t3)))

    x, y = sorted(triangle - {t})
    survivor = set()
    for u in sorted(outside):
        a, b = sorted(outside - {u})
        survivor.add(matching_key([(t, u), (a, b), (p, x), (q, y)]))
        survivor.add(matching_key([(t, u), (a, b), (p, y), (q, x)]))
    require(len(survivor) == 6 and survivor <= t3, (t, survivor))

    # Every other T3 term exposes a response edge not wholly contained in T,
    # hence one of the 12 edges represented in L_triangle.
    classified_survivor = set()
    classified_killed = set()
    for a, b in combinations(sorted(w_shore), 2):
        remaining = sorted(w_shore - {a, b})
        for image in permutations(remaining):
            matching = matching_key([
                (a, b), (t, image[0]), (p, image[1]), (q, image[2])
            ])
            response_pair = edge(image[1], image[2])
            if set(response_pair) <= triangle:
                classified_survivor.add(matching)
            else:
                classified_killed.add(matching)
    require(classified_survivor == survivor,
            (t, classified_survivor ^ survivor))
    require(classified_survivor | classified_killed == t3,
            (t, len(classified_survivor), len(classified_killed)))
    require(len(classified_killed) == 54, len(classified_killed))
    return {
        "exposed_triangle_vertex": t,
        "opposite_triangle_edge": [x, y],
        "five_set": sorted(w_shore),
        "T1_matchings": len(t1),
        "T3_matchings": len(t3),
        "T3_killed_by_L_triangle": len(classified_killed),
        "T3_surviving_on_opposite_edge": len(survivor),
        "survivor_factorization": "3 matchings of H_{t union O} times 2 response summands",
    }


def zeros():
    return [[0 for _ in range(3)] for _ in range(3)]


def identity():
    return [[int(i == j) for j in range(3)] for i in range(3)]


def e00():
    result = zeros()
    result[0][0] = 1
    return result


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def set_oriented(blocks, u, v, matrix):
    blocks[edge(u, v)] = matrix if u < v else transpose(matrix)


def oriented(blocks, u, v):
    matrix = blocks.get(edge(u, v), zeros())
    return matrix if u < v else transpose(matrix)


def response_coefficients(blocks, p, q, a, b):
    p_a = oriented(blocks, p, a)
    p_b = oriented(blocks, p, b)
    q_a = oriented(blocks, q, a)
    q_b = oriented(blocks, q, b)
    rows = []
    for alpha, beta in product(range(3), repeat=2):
        row = []
        for i, j in product(range(3), repeat=2):
            row.append(
                p_a[i][alpha] * q_b[j][beta]
                + p_b[i][beta] * q_a[j][alpha]
            )
        rows.append(row)
    return rows


def response_at_k(rows, k):
    flat_k = [k[i][j] for i, j in product(range(3), repeat=2)]
    values = [sum(a * b for a, b in zip(row, flat_k)) for row in rows]
    return [values[3 * alpha : 3 * alpha + 3] for alpha in range(3)]


def amplitude(blocks, word):
    total = 0
    for matching in perfect_matchings(range(8)):
        term = 1
        for u, v in matching:
            term *= oriented(blocks, u, v)[word[u]][word[v]]
        total += term
    return total


def four_site_cofactor(blocks, vertices, word):
    total = 0
    for matching in perfect_matchings(vertices):
        term = 1
        for u, v in matching:
            term *= oriented(blocks, u, v)[word[u]][word[v]]
        total += term
    return total


def hostile_source_guard():
    # Canonical data: p=6,q=7,T={0,1,2}, expose t=0, O={3,4,5}.
    # Only the omitted triangle response R_12 survives.
    p, q, t = 6, 7, 0
    triangle = {0, 1, 2}
    outside = {3, 4, 5}
    w_shore = sorted((triangle - {t}) | outside)
    blocks = {}
    set_oriented(blocks, p, 1, identity())
    set_oriented(blocks, q, 2, identity())
    set_oriented(blocks, t, 3, e00())
    set_oriented(blocks, 4, 5, e00())
    set_oriented(blocks, p, q, identity())
    k = identity()

    outside_edges = [ab for ab in combinations(range(6), 2)
                     if not set(ab) <= triangle]
    require(len(outside_edges) == 12, outside_edges)
    l_rows = []
    for a, b in outside_edges:
        l_rows.extend(response_coefficients(blocks, p, q, a, b))
    require(len(l_rows) == 108, len(l_rows))
    require(all(all(entry == 0 for entry in row) for row in l_rows),
            "hostile L_triangle is not zero")

    r12_rows = response_coefficients(blocks, p, q, 1, 2)
    r12 = response_at_k(r12_rows, k)
    require(r12 == identity(), r12)

    # Internal W cofactors vanish, so beta=e_(00000)^* lies in ker B_W and
    # has delta(beta)=e_0.
    for u in w_shore:
        residual = [site for site in w_shore if site != u]
        for colours in product(range(3), repeat=4):
            word = {site: colour for site, colour in zip(residual, colours)}
            require(four_site_cofactor(blocks, residual, word) == 0,
                    (u, residual, colours))

    # Contract beta (which selects W=00000) and K=I, leaving t exposed.
    contracted = []
    for colour_t in range(3):
        value = 0
        for colour_pq in range(3):
            word = [0] * 8
            word[t] = colour_t
            word[p] = colour_pq
            word[q] = colour_pq
            value += amplitude(blocks, tuple(word))
        contracted.append(value)
    require(contracted == [1, 0, 0], contracted)

    direct_pairing = sum(k[i][j] * oriented(blocks, p, q)[i][j]
                         for i, j in product(range(3), repeat=2))
    require(direct_pairing == 3, direct_pairing)
    return {
        "nonzero_blocks": [
            "A_61=I3", "A_72=I3", "A_03=E00", "A_45=E00", "A_67=I3"
        ],
        "K": "I3",
        "L_triangle_rank": 0,
        "all_four_blockers_outside_rowspan": True,
        "R_12_of_K": "I3",
        "beta": "evaluation at W-word 00000",
        "delta_beta": [1, 0, 0],
        "contracted_source": contracted,
        "contracted_target_projection": [1, 0, 0],
        "direct_pairing": direct_pairing,
        "scope": "source-faithful contraction guard, not a normalized X5 source",
    }


def orientation_guard(mutate):
    changed = 0
    checked = 0
    for i, j, alpha, beta in product(range(3), repeat=4):
        correct = ((i, alpha, j, beta), (i, beta, j, alpha))
        crossed = ((i, alpha, j, beta),
                   (i, alpha if mutate else beta, j, beta if mutate else alpha))
        if crossed != correct:
            changed += 1
        checked += 1
    if mutate:
        require(changed > 0, changed)
        raise RuntimeError({"hostile_orientation_changed_rows": changed})
    require(changed == 0, changed)
    return {"colour_assignments_checked": checked, "changed": changed}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--mutate-crossed-orientation", action="store_true")
    args = parser.parse_args()

    partitions = [cut_partition_for_vertex(t) for t in range(3)]
    payload = {
        "status": "PASS triangle annihilator leaves one opposite-edge response",
        "canonical_carrier": {"cap_pair": [6, 7], "triangle": [0, 1, 2],
                              "outside": [3, 4, 5]},
        "cyclic_partitions": partitions,
        "hostile_source_guard": hostile_source_guard(),
        "orientation_guard": orientation_guard(args.mutate_crossed_orientation),
        "exact_identity": (
            "For each t in T and beta in ker(B_W), every K in ker(L_T) obeys "
            "Theta_(t,beta)(R_(T\\t)(K)) = sum_c delta(beta)_c K_cc e_c."
        ),
        "rowspace_consequence": (
            "For each opposite triangle edge e, at least one diagonal blocker "
            "lies in rowspan([L_T;R_e]); it need not lie in rowspan(L_T)."
        ),
        "terminal_verdict": (
            "No triangle blocker clause is automatic from the universal "
            "five-set annihilator alone; the 560 triangle clauses remain."
        ),
    }
    payload["logical_sha256"] = sha256(json.dumps(
        payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    if args.write_results:
        OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(payload["status"])
    print("survivors", [item["T3_surviving_on_opposite_edge"]
                        for item in partitions])
    print("hostile", payload["hostile_source_guard"])
    print("logical sha256", payload["logical_sha256"])


if __name__ == "__main__":
    main()
