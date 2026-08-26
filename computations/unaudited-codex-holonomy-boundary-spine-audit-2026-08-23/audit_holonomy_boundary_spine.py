#!/usr/bin/env python3
"""Audit the exact downstream obligations after a provisional H=0 theorem."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import argparse
import json


ROOT = Path(__file__).resolve().parents[2]
FILES = {
    "triangle": ROOT / "computations/unaudited-codex-triangle-crossword-observation-2026-08-22/results_triangle_crossword_observation.json",
    "incidence": ROOT / "computations/unaudited-codex-star-tautology-triangle-replacement-2026-08-22/canonical_triangle_incidence_manifest.json",
    "five_set": ROOT / "computations/unaudited-codex-five-set-response-surjectivity-2026-08-22/results.json",
    "pure_quotient": ROOT / "computations/unaudited-codex-triangle-pure-quotient-collapse-2026-08-22/results.json",
}
EXPECTED = {
    "triangle": "80ea9a26eb958f174d4e172570cfb1fd9d1fdfd187518f8f02e95a8c2dd62e8f",
    "incidence": "0b556f2f217e1a1f158edb66e64d74fa8f5f7b649be182c797c10711f378b529",
    "five_set": "20ce72a7aa63c9bb4f85e6e7441e9e7b8bdbb0bd6a2aef3d0a3d590f559a6bcb",
    "pure_quotient": "cf2ca70211cbacd9ddaa99afcca09f7c7cc2973a156de92bb118f3d9fb7a5db8",
}
EXPECTED_LOGICAL_SHA256 = "4e81b9bcc837343e08095b4fd6ce1739de62ec412e154dc46c35ff1a66a25325"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def rank(matrix):
    work = [[Fraction(value) for value in row] for row in matrix]
    if not work:
        return 0
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next((r for r in range(pivot_row, len(work))
                      if work[r][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for row_index in range(len(work)):
            if row_index == pivot_row or not work[row_index][column]:
                continue
            scale = work[row_index][column]
            work[row_index] = [
                value - scale * base
                for value, base in zip(work[row_index], work[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def determinant3(rows):
    (a, b, c), (d, e, f), (g, h, i) = rows
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def run_audit():
    frozen = {}
    hashes = {}
    for label, path in FILES.items():
        data = path.read_bytes()
        hashes[label] = sha256(data).hexdigest()
        require(hashes[label] == EXPECTED[label], (label, hashes[label], EXPECTED[label]))
        frozen[label] = json.loads(data)

    triangle = frozen["triangle"]
    incidence = frozen["incidence"]
    require(triangle["global_observation_map"]["physical_internal_triangle_cells"] == 27,
            triangle["global_observation_map"])
    require(triangle["global_observation_map"]["rows"] == 6561,
            triangle["global_observation_map"])
    require(triangle["global_rootless_three_pure_dependency"]["witness"]
            ["comparison_outside_words"] == ["11222", "00000", "11111", "22222"],
            triangle["global_rootless_three_pure_dependency"])
    require(triangle["cramer_remainder_cap_partition"] == {
        "direct_A67": 6,
        "internal_triangle_response": 18,
        "outside_triangle_response": 36,
        "triangle_kernel_consequence": triangle["cramer_remainder_cap_partition"]
        ["triangle_kernel_consequence"],
    }, triangle["cramer_remainder_cap_partition"])
    require(incidence["counts_per_branch"]["variables"] == 361,
            incidence["counts_per_branch"])
    require(incidence["counts_per_branch"]["equations"] == 6571,
            incidence["counts_per_branch"])
    require(len(incidence["outside_response_rows"]) == 108,
            len(incidence["outside_response_rows"]))
    require(len(incidence["rowspan_witness_variables"]) == 108,
            len(incidence["rowspan_witness_variables"]))
    require(frozen["five_set"]["profiles_per_source"] == 5040,
            frozen["five_set"])
    require(frozen["five_set"]["triangle_colour_groups_per_source"] == 1680,
            frozen["five_set"])
    require(frozen["pure_quotient"]["triangle_groups_per_source_prime"] == 1680,
            frozen["pure_quotient"])

    # Exact abstract counterguard: rank(C)<=2 and the simultaneous rank-nine
    # response open do not, as linear algebra, contradict all four blockers.
    carrier_cofactor = [
        [1, 0, 0], [0, 1, 0], [1, 1, 0], [2, 1, 0],
        [1, 2, 0], [3, 1, 0], [1, 3, 0], [2, 3, 0],
    ]
    minors = [
        determinant3([carrier_cofactor[index] for index in triple])
        for triple in combinations(range(8), 3)
    ]
    require(len(minors) == 56 and not any(minors), minors)
    require(rank(carrier_cofactor) == 2, rank(carrier_cofactor))

    response = [
        [1 if row == column else 0 for column in range(9)]
        for row in range(9)
    ] + [[0] * 9 for _ in range(99)]
    blockers = {
        "K00": [1, 0, 0, 0, 0, 0, 0, 0, 0],
        "K11": [0, 0, 0, 0, 1, 0, 0, 0, 0],
        "K22": [0, 0, 0, 0, 0, 0, 0, 0, 1],
        "direct": [1, 2, 3, 4, 5, 6, 7, 8, 9],
    }
    require(rank(response) == 9, rank(response))
    require(all(rank(response + [blocker]) == 9 for blocker in blockers.values()),
            blockers)
    quotient_maps = [response[:9] for _ in range(9)]
    require(all(rank(matrix) == 9 for matrix in quotient_maps), "rank-nine open failed")

    base_variables = incidence["counts_per_branch"]["variables"]
    base_equations = incidence["counts_per_branch"]["equations"]
    result = {
        "status": "PASS exact downstream audit; H=0 is not a cap contradiction",
        "pinned_sha256": hashes,
        "literal_H_consequence": (
            "On a nonzero cone chart, the frozen H=0 makes only its selected "
            "three six-site cofactor triples linearly dependent."
        ),
        "carrier_alignment_guard": (
            "The frozen H uses global outside slices 11222,00000,11111, "
            "whereas the blocker Cramer matrix fixes a pure residual colour "
            "and varies eight cap words. H is not the list of all 56 carrier minors."
        ),
        "carrier_rank_two_minors_per_colour": len(minors),
        "carrier_rank_two_minors_all_colours": 3 * len(minors),
        "abstract_counterguard": {
            "carrier_cofactor_shape": [8, 3],
            "carrier_cofactor_rank": rank(carrier_cofactor),
            "vanishing_maximal_minors": sum(value == 0 for value in minors),
            "triangle_response_shape": [108, 9],
            "triangle_response_rank": rank(response),
            "simultaneous_rank_nine_maps": len(quotient_maps),
            "all_four_blockers_in_rowspan": True,
            "scope": (
                "Exact rational linear-algebra counterguard, not a literal "
                "source or normalized-X5 realization. It proves that a "
                "finishing lemma must use source coupling/X5, not ranks alone."
            ),
        },
        "smallest_open_boundary_system": {
            "source_and_membership_variables": base_variables,
            "one_open_product_inverse": 1,
            "total_variables": base_variables + 1,
            "base_equations": base_equations,
            "one_colour_rank_two_minors": len(minors),
            "open_product_equation": 1,
            "total_equations": base_equations + len(minors) + 1,
            "open_product_factors": (
                "H_0 H_1 H_2 times one chosen nonzero 9x9 minor for each "
                "of the 3 vertices and 3 colours"
            ),
            "full_three_colour_equations": base_equations + 3 * len(minors) + 1,
        },
        "required_open_boundary_lemma": (
            "On normalized X5 and the canonical live-cell chart, simultaneous "
            "five-set rank-nine plus H_0 H_1 H_2 nonzero plus rank(C_c)<=2 "
            "forces the direct blocker outside rowspan(L_T), or is empty."
        ),
        "remaining_boundary_lemma": (
            "Every divisor where a selected five-set 9x9 minor or a pure "
            "six-site cofactor H_c vanishes must yield a source-labelled "
            "E1/E2 good-pair descent or an active clean cap."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    digest = sha256(logical.encode()).hexdigest()
    if EXPECTED_LOGICAL_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LOGICAL_SHA256,
                (digest, EXPECTED_LOGICAL_SHA256))
    result["logical_sha256"] = digest
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    args = parser.parse_args()
    result = run_audit()
    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    result_path = Path(__file__).with_name("results_holonomy_boundary_spine.json")
    if args.write_results:
        result_path.write_text(output)
    if args.check_results:
        require(result_path.read_text() == output, "stored result changed")
    print(output, end="")


if __name__ == "__main__":
    main()
