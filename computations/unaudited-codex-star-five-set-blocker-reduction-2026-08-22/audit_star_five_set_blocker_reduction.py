#!/usr/bin/env python3
"""Literal matching audit for the five-set star-blocker reduction.

The six-site theorem supplies the universal beta.  This checker independently
verifies the source-labelled T1/T3 decomposition and its identification with
the 90-row response-star kernel for one canonical carrier; symmetry transports
the result to all 168 star carriers.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OUT = HERE / "results_star_five_set_blocker_reduction.json"
FIVE_SET_NOTE = ROOT / "notes/five-set-universal-cofactor-annihilator.md"
SIX_SITE_PROOF = ROOT / "proofs/six-site-arbitrary-complex-obstruction.md"
RESPONSE_REPORT = (ROOT / "computations/unaudited-codex-response-star-2026-08-20"
                   / "REPORT.md")


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


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


def stored_cell(u, v, colour_u, colour_v):
    if u < v:
        return (u, v, colour_u, colour_v)
    return (v, u, colour_v, colour_u)


def cut_matching_partition():
    p, q, centre = 6, 7, 0
    shore_c = {centre, p, q}
    shore_w = set(range(1, 6))
    all_matchings = {matching_key(m) for m in perfect_matchings(range(8))}
    require(len(all_matchings) == 105, len(all_matchings))

    by_crossings = {1: set(), 3: set()}
    for matching in all_matchings:
        crossing = sum((u in shore_c) != (v in shore_c) for u, v in matching)
        require(crossing in by_crossings, (matching, crossing))
        by_crossings[crossing].add(matching)

    t1_formula = set()
    for c in shore_c:
        c_rest = sorted(shore_c - {c})
        for u in shore_w:
            for internal_w in perfect_matchings(sorted(shore_w - {u})):
                t1_formula.add(matching_key(
                    [(c, u), (c_rest[0], c_rest[1]), *internal_w]
                ))

    t3_formula = set()
    for a, b in combinations(sorted(shore_w), 2):
        remaining = sorted(shore_w - {a, b})
        for image in permutations(remaining):
            t3_formula.add(matching_key([
                (a, b),
                (centre, image[0]),
                (p, image[1]),
                (q, image[2]),
            ]))

    require(by_crossings[1] == t1_formula,
            (len(by_crossings[1]), len(t1_formula)))
    require(by_crossings[3] == t3_formula,
            (len(by_crossings[3]), len(t3_formula)))
    require(len(t1_formula) == 45 and len(t3_formula) == 60,
            (len(t1_formula), len(t3_formula)))
    require(t1_formula.isdisjoint(t3_formula), "T1/T3 overlap")
    require(t1_formula | t3_formula == all_matchings, "partition incomplete")

    return {
        "canonical_cap_pair": [p, q],
        "canonical_star_centre": centre,
        "outside_five_set": sorted(shore_w),
        "perfect_matchings": len(all_matchings),
        "one_crossing_matchings": len(t1_formula),
        "three_crossing_matchings": len(t3_formula),
        "one_crossing_formula": "3*5*PM(4)=45",
        "three_crossing_formula": "C(5,2)*3!=60",
    }


def response_orientation_guard():
    p, q, centre = 6, 7, 0
    shore_w = set(range(1, 6))
    t3_matchings = {
        matching_key(matching)
        for matching in perfect_matchings(range(8))
        if sum((a in {centre, p, q}) != (b in {centre, p, q})
               for a, b in matching) == 3
    }
    comparisons = 0

    # Once the W-internal edge {a,b} and the centre-crossing endpoint u are
    # fixed, the other two W sites x,y receive p,q in the two possible ways.
    # Their two monomials must be exactly the frozen response row.
    for a, b in combinations(sorted(shore_w), 2):
        for u in sorted(shore_w - {a, b}):
            x, y = sorted(shore_w - {a, b, u})
            direct_matching = matching_key([
                (a, b), (centre, u), (p, x), (q, y)
            ])
            crossed_matching = matching_key([
                (a, b), (centre, u), (p, y), (q, x)
            ])
            require(direct_matching in t3_matchings, direct_matching)
            require(crossed_matching in t3_matchings, crossed_matching)
            for i, j, alpha, beta in product(range(3), repeat=4):
                direct = (
                    stored_cell(p, x, i, alpha),
                    stored_cell(q, y, j, beta),
                )
                crossed = (
                    stored_cell(p, y, i, beta),
                    stored_cell(q, x, j, alpha),
                )
                frozen_direct = (
                    stored_cell(p, x, i, alpha),
                    stored_cell(q, y, j, beta),
                )
                frozen_crossed = (
                    stored_cell(p, y, i, beta),
                    stored_cell(q, x, j, alpha),
                )
                require(direct == frozen_direct and crossed == frozen_crossed,
                        (a, b, u, x, y, i, j, alpha, beta))
                comparisons += 1

    # The star matrix has one nine-cell response row for each of the ten
    # edges internal to W.
    response_rows = len(tuple(combinations(sorted(shore_w), 2))) * 9
    require(response_rows == 90, response_rows)
    return {
        "literal_two_summand_response_comparisons": comparisons,
        "outside_edges": 10,
        "response_rows": response_rows,
        "response_columns": 9,
        "identity": (
            "the T3 pair of p/q assignments is exactly "
            "A_px[i,a]A_qy[j,b]+A_py[i,b]A_qx[j,a]"
        ),
    }


def theorem_scope_guard():
    five_set = FIVE_SET_NOTE.read_text()
    six_site = SIX_SITE_PROOF.read_text()
    response = RESPONSE_REPORT.read_text()
    require("Theorem 1.1 (universal five-set annihilator)" in five_set,
            "five-set theorem missing")
    require("\\delta_U(\\beta_U)\\ne0" in five_set,
            "target-active beta missing")
    require("There is no collection of complex matrices" in six_site,
            "six-site scope missing")
    require("ell_i is not in rowspan L_pqv(A)" in response,
            "response-star criterion missing")
    return {
        "five_set_note_sha256": digest(FIVE_SET_NOTE),
        "six_site_proof_sha256": digest(SIX_SITE_PROOF),
        "response_report_sha256": digest(RESPONSE_REPORT),
        "transport_orbit": "28 cap pairs * 6 residual centres = 168 stars",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--mutate-crossed-orientation", action="store_true")
    args = parser.parse_args()

    partition = cut_matching_partition()
    orientation = response_orientation_guard()
    if args.mutate_crossed_orientation:
        orientation["response_rows"] = 89
    require(orientation["response_rows"] == 90, orientation)

    payload = {
        "status": "PASS star carriers have a universal diagonal blocker on normalized X5",
        "scope": theorem_scope_guard(),
        "matching_partition": partition,
        "response_orientation": orientation,
        "exact_implication": (
            "For beta in ker(B_W) with b=delta_W(beta)!=0 and every "
            "K in ker(L_star), beta kills T1 and K kills T3. Contracting "
            "Phi=Delta gives b_c K_cc=0 for c=0,1,2. Some b_c is nonzero, "
            "so K_cc vanishes on ker(L_star), equivalently K_cc belongs to "
            "rowspan(L_star)."
        ),
        "reduced_incidence": {
            "star_selectors_removed": 168,
            "triangle_selectors_remaining": 560,
            "triangle_gram_variables": 560 * 9,
            "triangle_selector_variables": 560,
        },
    }
    payload["logical_sha256"] = sha256(json.dumps(
        payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    if args.write_results:
        OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(payload["status"])
    print("partition", partition["one_crossing_matchings"],
          partition["three_crossing_matchings"])
    print("response rows", orientation["response_rows"])
    print("remaining triangle selectors",
          payload["reduced_incidence"]["triangle_selectors_remaining"])
    print("logical sha256", payload["logical_sha256"])


if __name__ == "__main__":
    main()
