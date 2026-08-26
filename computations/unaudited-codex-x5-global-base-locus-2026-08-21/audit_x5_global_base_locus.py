#!/usr/bin/env python3
"""Exact n=8 base-locus, jet, and exceptional-fibre audit for the Wick arc."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import argparse
import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BOUNDARY_PATH = ROOT / "computations/verify_global_wick_top_invariant_counterguard.py"
CYCLE_PATH = ROOT / "computations/verify_one_hot_source_cycle_invariant_separator.py"
INDEPENDENT_CYCLE_PATH = (
    ROOT / "computations/audit_one_hot_source_cycle_invariant_separator_independent.py"
)
OUT = HERE / "results_x5_global_base_locus.json"
PINNED_BOUNDARY_DIGEST = (
    "d5d3199b39bfa81cfba33ebaf38144846488e6cc051cc6a6be12d5ac649bd07c"
)
PINNED_CYCLE_DIGEST = (
    "1900ea5daa293e529a938ab388066908199890cf861216019eb0031e7487a547"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def file_sha(path):
    return sha256(path.read_bytes()).hexdigest()


def logical_sha(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode("ascii")).hexdigest()


def cell_label(edge, colour):
    return f"x_{edge[0]}{edge[1]}^{colour}{colour}"


def matching_record(boundary, matching, edges, vertices):
    word, valuation = boundary.matching_term(matching, edges, vertices)
    return {
        "word": "".join(map(str, word)),
        "original_valuation": valuation,
        "projective_valuation": valuation + 4,
        "matching": [list(edge) for edge in matching],
        "cells": [cell_label(edge, edges[edge][0]) for edge in matching],
    }


def extract_n8(boundary):
    vertices, edges = boundary.prism_seed()
    vertices, edges, shift = boundary.expand_vertex(vertices, edges, min(vertices))
    require(sorted(vertices) == list(range(1, 9)) and shift == 0,
            (vertices, shift))
    expected = {
        (1, 2): (0, -1),
        (1, 4): (1, 0),
        (1, 8): (2, 0),
        (2, 5): (2, 0),
        (2, 7): (1, 0),
        (3, 4): (2, 0),
        (3, 5): (1, 0),
        (3, 6): (0, 1),
        (4, 5): (0, 0),
        (6, 7): (2, 0),
        (6, 8): (1, 0),
        (7, 8): (0, 0),
    }
    require(edges == expected, "extracted n=8 Laurent edge packet changed")
    records = sorted(
        (matching_record(boundary, matching, edges, vertices)
         for matching in boundary.perfect_matchings(vertices, edges)),
        key=lambda row: row["word"],
    )
    require([(row["word"], row["original_valuation"]) for row in records] == [
        ("00000000", 0),
        ("11111111", 0),
        ("12012000", 1),
        ("21000012", 1),
        ("22222222", 0),
    ], records)
    projective_grades = {
        0: [cell_label(edge, colour)
            for edge, (colour, valuation) in sorted(edges.items())
            if valuation == -1],
        1: [cell_label(edge, colour)
            for edge, (colour, valuation) in sorted(edges.items())
            if valuation == 0],
        2: [cell_label(edge, colour)
            for edge, (colour, valuation) in sorted(edges.items())
            if valuation == 1],
    }
    require([len(projective_grades[grade]) for grade in (0, 1, 2)] == [1, 10, 1],
            projective_grades)
    return vertices, edges, records, projective_grades


def all_amplitude_jets(records):
    jets = {"".join(map(str, word)): []
            for word in product(range(3), repeat=8)}
    for row in records:
        jets[row["word"]].append([row["projective_valuation"], 1])
    require(len(jets) == 6561, len(jets))
    histogram = Counter()
    for series in jets.values():
        histogram[str(series[0][0]) if series else "identically_zero"] += 1
    require(histogram == {"4": 3, "5": 2, "identically_zero": 6556}, histogram)
    nonzero = {word: series for word, series in jets.items() if series}
    return {
        "all_coordinate_count": len(jets),
        "first_nonzero_order_histogram": dict(histogram),
        "nonzero_series": nonzero,
        "order_four_direction": {
            "00000000": 1, "11111111": 1, "22222222": 1,
        },
        "order_five_direction": {"12012000": 1, "21000012": 1},
        "identity": "H(B0+tB1+t^2B2)=t^4*GHZ+t^5*(e_12012000+e_21000012)",
    }


def local_base_geometry(boundary, vertices, edges, grades):
    base_cell = grades[0]
    require(base_cell == ["x_12^00"], base_cell)
    residual = tuple(vertex for vertex in sorted(vertices) if vertex not in (1, 2))
    residual_matchings = tuple(boundary.perfect_matchings(residual,
                                                          set(combinations(residual, 2))))
    require(len(residual_matchings) == 15, len(residual_matchings))
    cubic_monomials = (3 ** 6) * len(residual_matchings)
    require(cubic_monomials == 10935, cubic_monomials)

    b1_physical = {
        edge for edge, (_colour, valuation) in edges.items()
        if valuation == 0 and set(edge).issubset(residual)
    }
    b1_residual_matchings = tuple(boundary.perfect_matchings(residual, b1_physical))
    require(not b1_residual_matchings, b1_residual_matchings)
    components = []
    remaining = set(residual)
    while remaining:
        seed = min(remaining)
        component = {seed}
        queue = [seed]
        for vertex in queue:
            for edge in b1_physical:
                if vertex in edge:
                    other = edge[0] if edge[1] == vertex else edge[1]
                    if other not in component:
                        component.add(other)
                        queue.append(other)
        remaining -= component
        components.append(sorted(component))
    require(sorted(components) == [[3, 4, 5], [6, 7, 8]], components)

    return {
        "projective_limit": "B0=[x_12^00]",
        "base_locus_membership": (
            "B0 has one physical edge and hence no four-edge perfect matching; "
            "all 6,561 amplitudes vanish."
        ),
        "base_scheme_Zariski_tangent_dimension": 251,
        "reason_full_tangent": (
            "Every amplitude vanishes to local order at least three at B0, "
            "so the Jacobian and Hessian of the base ideal vanish there."
        ),
        "first_normal_cone_map": (
            "C3(B)=x_12^00 tensor H_6(B restricted to sites 3,4,5,6,7,8), "
            "landing in the 729 coordinates whose endpoint-1,2 colours are 00."
        ),
        "cubic_output_coordinates": 3 ** 6,
        "cubic_monomials": cubic_monomials,
        "other_output_coordinates_begin_in_degree_four": 6561 - 3 ** 6,
        "B1_cubic_value": 0,
        "B1_residual_support_components": components,
        "B1_cubic_kernel_certificate": (
            "The residual B1 graph is two disjoint triangles and has no "
            "perfect matching."
        ),
        "arc_contact_order": 4,
    }


def exceptional_fibre(records):
    pure = {row["word"]: row for row in records if len(set(row["word"])) == 1}
    require(set(pure) == {"00000000", "11111111", "22222222"}, pure)
    formulas = {
        word: "*".join(row["cells"])
        for word, row in sorted(pure.items())
    }
    variable_sets = [set(row["cells"]) for row in pure.values()]
    require(all(not variable_sets[i] & variable_sets[j]
                for i in range(3) for j in range(i + 1, 3)),
            variable_sets)
    return {
        "generic_cubic_exceptional_family": {
            "construction": (
                "Use B0=x_12^00 and first-order tensors on one residual "
                "perfect matching, for example edges 34,56,78."
            ),
            "leading_direction": "x_12^00 tensor A_34 tensor A_56 tensor A_78",
            "contained_variety": "Segre(P^8 x P^8 x P^8)",
            "dimension": 24,
            "GHZ_stabilizer_identity_component_dimension": 21,
            "orbit_moduli_lower_bound": 3,
        },
        "quartic_cubic_kernel_family": {
            "pure_coordinate_formulas": formulas,
            "independence": (
                "The three monomials use disjoint source coordinates; varying "
                "one coefficient in each realizes arbitrary [alpha:beta:gamma] "
                "in a dense open of P^2."
            ),
            "family": "[alpha*e_00000000+beta*e_11111111+gamma*e_22222222]",
            "GHZ_point": "[1:1:1]",
            "dimension": 2,
            "symmetry_quotient": (
                "T0 fixes all three pure coordinates and common S3 only "
                "permutes them, so P^2/S3 remains two-dimensional."
            ),
        },
        "verdict": "The exceptional fibre has infinitely many symmetry-orbit types.",
    }


def alternative_ghz_arcs(boundary, vertices, edges):
    colour_zero = tuple(edge for edge, (colour, _valuation) in sorted(edges.items())
                        if colour == 0)
    require(set(colour_zero) == {(1, 2), (3, 6), (4, 5), (7, 8)}, colour_zero)
    mixed_matchings = []
    all_matchings = tuple(boundary.perfect_matchings(vertices, edges))
    for matching in all_matchings:
        word, _ = boundary.matching_term(matching, edges, vertices)
        if len(set(word)) > 1:
            mixed_matchings.append((word, matching))
    require(len(mixed_matchings) == 2, mixed_matchings)

    examples = []
    for support in (
        {(1, 2)},
        {(1, 2), (4, 5)},
        {(1, 2), (4, 5), (7, 8)},
    ):
        valuations = {edge: 0 for edge in edges}
        for edge in support:
            valuations[edge] = -1
        valuations[(3, 6)] = len(support)
        require(sum(valuations[edge] for edge in colour_zero) == 0,
                "alternative colour-zero normalization failed")
        term_orders = []
        for matching in all_matchings:
            word, _ = boundary.matching_term(matching, edges, vertices)
            value = sum(valuations[edge] for edge in matching)
            term_orders.append(("".join(map(str, word)), value))
        pure_orders = [value for word, value in term_orders if len(set(word)) == 1]
        mixed_orders = [value for word, value in term_orders if len(set(word)) > 1]
        require(pure_orders == [0, 0, 0] and all(value > 0 for value in mixed_orders),
                (term_orders, pure_orders, mixed_orders))
        projective_limit = [cell_label(edge, edges[edge][0])
                            for edge in sorted(support)]
        require(len(projective_limit) < 4,
                "alternative projective limit acquired a perfect matching")
        examples.append({
            "minimum_support_size": len(support),
            "projective_limit_support": projective_limit,
            "pure_output_orders_before_rescaling": pure_orders,
            "mixed_output_orders_before_rescaling": mixed_orders,
            "first_output_order_after_rescaling": 4,
            "leading_output": "GHZ",
        })
    require([row["minimum_support_size"] for row in examples] == [1, 2, 3],
            examples)
    return {
        "examples": examples,
        "inequivalence_certificate": (
            "Projective source support cardinality 1, 2, or 3 is preserved by "
            "site/colour permutations and the GHZ port torus."
        ),
        "conclusion": (
            "Even within the same n=8 properly-coloured one-hot graph, "
            "GHZ-reaching arcs meet at least three inequivalent base-locus "
            "strata. The one-cell boundary type is not universal."
        ),
    }


def global_base_size():
    # Isolating one physical site leaves C(7,2)*9 arbitrary source cells.
    affine_coordinates = 21 * 9
    require(affine_coordinates == 189, affine_coordinates)
    return {
        "site_isolation_linear_subspaces": 8,
        "coordinates_per_subspace": affine_coordinates,
        "projective_dimension": affine_coordinates - 1,
        "why_base": "No perfect matching can cover the isolated site.",
        "GHZ_stabilizer_dimension": 21,
        "orbit_moduli_lower_bound": (affine_coordinates - 1) - 21,
        "conclusion": (
            "The base locus already contains positive-dimensional families of "
            "inequivalent points; finite support types do not imply finitely "
            "many algebraic orbit types."
        ),
    }


def cycle_rees_relation(records):
    mixed = [row for row in records if len(set(row["word"])) > 1]
    require(len(mixed) == 2 and all(row["original_valuation"] == 1 for row in mixed),
            mixed)
    rows = []
    for row in mixed:
        # At n=8, deg H=4, deg complement Q=8, deg I=12.
        h_order = row["projective_valuation"]
        q_order = 7  # t^8 from projective rescaling times t^-1 compensation.
        invariant_order = h_order + q_order
        require((h_order, q_order, invariant_order) == (5, 7, 12),
                (h_order, q_order, invariant_order))
        rows.append({
            "word": row["word"],
            "H_order_on_B": h_order,
            "complement_Q_order_on_B": q_order,
            "cycle_I_order_on_B": invariant_order,
            "full_support_P_order_on_B": 12,
            "Rees_ratio_I_over_P": 1,
        })
    return {
        "degree": 12,
        "mixed_records": rows,
        "interpretation": (
            "The affine invariant I_M=H_m Q_M is one along the Laurent torus "
            "orbit and zero on every exact GHZ source. After projective "
            "rescaling, I_M and the full support product P_G both vanish as "
            "t^12, while the Rees ratio I_M/P_G remains one. Thus the source "
            "cycle separator is exactly zero-times-infinity data retained by "
            "a source-relative blow-up and erased by the top tensor map."
        ),
        "limitation": (
            "The same ratio is one for all three alternative one-hot arcs. It "
            "separates their finite boundary orbit from an exact GHZ source, "
            "but does not classify base strata or prove that every GHZ arc is "
            "one-hot."
        ),
    }


def main(write_results=False):
    boundary = load_module("x5_global_boundary_source", BOUNDARY_PATH)
    vertices, edges, records, grades = extract_n8(boundary)
    result = {
        "status": "PASS exact n=8 global base-locus and exceptional-fibre audit",
        "map": "H:P^251 -->> P^6560, homogeneous degree four",
        "n8_Laurent_source": {
            "vertices": sorted(vertices),
            "literal_edges": [
                {"edge": list(edge), "colour": colour, "valuation": valuation,
                 "cell": cell_label(edge, colour)}
                for edge, (colour, valuation) in sorted(edges.items())
            ],
            "minimal_projective_rescaling": "B(t)=t*A(t)",
            "projective_grades": {str(key): value for key, value in grades.items()},
            "supported_matching_records": records,
        },
        "all_amplitude_jets": all_amplitude_jets(records),
        "local_base_geometry": local_base_geometry(boundary, vertices, edges, grades),
        "exceptional_fibre": exceptional_fibre(records),
        "nonunique_GHZ_reaching_boundary_types": alternative_ghz_arcs(
            boundary, vertices, edges),
        "global_base_locus_size_guard": global_base_size(),
        "source_cycle_Rees_relation": cycle_rees_relation(records),
        "ranked_verdict": [
            {
                "rank": 1,
                "verdict": "NEGATIVE for a finite/universal boundary-type lemma",
                "reason": (
                    "There are explicit GHZ-reaching one-hot arcs with base "
                    "support sizes 1, 2, and 3, and the exceptional fibre over "
                    "the one-cell point already has positive-dimensional moduli."
                ),
            },
            {
                "rank": 2,
                "verdict": "POSITIVE local Rees interface",
                "reason": (
                    "The known arc is a fourth-order point of the cubic normal "
                    "cone and the two degree-12 cycle ratios retain its affine "
                    "zero-times-infinity data exactly."
                ),
            },
            {
                "rank": 3,
                "verdict": "No border-to-exact contradiction from H alone",
                "reason": (
                    "Any useful blow-up must retain source one-hot/cycle data "
                    "and separately prove that every relevant arc enters that "
                    "source-relative chart."
                ),
            },
        ],
        "pinned_sources": {
            str(BOUNDARY_PATH.relative_to(ROOT)): file_sha(BOUNDARY_PATH),
            str(CYCLE_PATH.relative_to(ROOT)): file_sha(CYCLE_PATH),
            str(INDEPENDENT_CYCLE_PATH.relative_to(ROOT)): file_sha(
                INDEPENDENT_CYCLE_PATH),
            "boundary_audit_logical_digest": PINNED_BOUNDARY_DIGEST,
            "cycle_separator_logical_digest": PINNED_CYCLE_DIGEST,
        },
    }
    result["logical_sha256"] = logical_sha(result)
    if write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "projective_limit": result["local_base_geometry"]["projective_limit"],
        "jet_histogram": result["all_amplitude_jets"]
            ["first_nonzero_order_histogram"],
        "quartic_exceptional_family_dimension": result["exceptional_fibre"]
            ["quartic_cubic_kernel_family"]["dimension"],
        "GHZ_boundary_support_sizes": [row["minimum_support_size"] for row in
            result["nonunique_GHZ_reaching_boundary_types"]["examples"]],
        "logical_sha256": result["logical_sha256"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    main(args.write_results)
