#!/usr/bin/env python3
"""UNAUDITED RISK PROBE - target (output) side invariants for J(M_v).

Pinned HEAD b63c76c8624996044423a0dde60a2b60c9e8fa3d, frozen snapshot ./snap.
Exact rational arithmetic only.

Objects are taken verbatim from the committed checkers:
  verify_h3_rootless_c5_complete_multidegree_source_no_go.py   (component)
  verify_h3_direct_free_complete_first_fine_degree_membership.py (full_row)
  verify_h3_residual_q_literal_mapping_cone_private_boundary_gate.py (ALPHA)
"""
from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
from itertools import combinations, permutations
import importlib.util
import json
import pickle
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "snap"
CACHE = HERE / "target_cache.pkl"


def load(relative, name):
    spec = importlib.util.spec_from_file_location(name, SNAP / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def add_sparse(*vectors):
    answer = defaultdict(Q)
    for vector in vectors:
        for key, value in vector.items():
            answer[key] += Q(value)
    return {k: v for k, v in answer.items() if v}


def feature_degree(feature, sites=8, colours=3):
    """24-vector fine multidegree of a literal seven-cell monomial."""
    degree = [0] * (sites * colours)
    for cell in feature:
        left, right, left_colour, right_colour = cell
        degree[colours * left + left_colour] += 1
        degree[colours * right + right_colour] += 1
    return tuple(degree)


def permute_cell(cell, perm):
    left, right, lc, rc = cell
    a, b = perm[left], perm[right]
    if a <= b:
        return (a, b, lc, rc)
    return (b, a, rc, lc)


def permute_feature(feature, perm):
    return tuple(sorted(permute_cell(cell, perm) for cell in feature))


def gather():
    complete = load(
        "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py",
        "probe_complete")
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "probe_base")
    literal = load(
        "computations/verify_h3_residual_q_literal_mapping_cone_private_boundary_gate.py",
        "probe_literal")

    records = []
    for index, (left, _right, left_cell, _right_cell) in enumerate(
            complete.CUBIC_PAIRS):
        degree = complete.degree_add(
            base.lambda_degree(left),
            complete.cell_degree(complete.CYCLE_CELLS[left_cell]))
        block = complete.component(base, degree)
        pure = [(word, multiplier, boundary)
                for word, multiplier, boundary in block["columns"]
                if word == complete.PURE_WORD]
        records.append({
            "component": index,
            "target_degree": degree,
            "columns": len(block["columns"]),
            "pure": pure,
            "feature_count": block["feature_count"],
        })
    return records, tuple(literal.ALPHA), complete.PURE_WORD


def cached():
    if CACHE.exists():
        with CACHE.open("rb") as handle:
            return pickle.load(handle)
    data = gather()
    with CACHE.open("wb") as handle:
        pickle.dump(data, handle)
    return data


def degree_symmetries(degree, sites=8, colours=3):
    """All site permutations of {0..7} preserving the 24-vector degree."""
    per_site = [tuple(degree[colours * s: colours * (s + 1)])
                for s in range(sites)]
    answer = []
    for perm in permutations(range(sites)):
        # perm sends site s to perm[s]; degree must be preserved.
        if all(per_site[s] == per_site[perm[s]] for s in range(sites)):
            answer.append(perm)
    return answer


def analyse(record, alpha):
    pure = record["pure"]
    boundaries = [set(boundary) for _w, _m, boundary in pure]
    degree = record["target_degree"]

    # 1. every literal feature of every pure column has the component degree
    homogeneous = all(feature_degree(feature) == degree
                      for _w, _m, boundary in pure for feature in boundary)

    # 2. the 15 four-corner selections
    selections = []
    for choice in combinations(range(len(pure)), 4):
        aggregate = add_sparse(*(
            {feature: alpha[position] for feature in pure[index][2]}
            for position, index in enumerate(choice)))
        pairwise = [len(boundaries[a] & boundaries[b])
                    for a, b in combinations(choice, 2)]
        selections.append({
            "choice": list(choice),
            "support": len(aggregate),
            "coefficients": sorted(Counter(str(v) for v in
                                           aggregate.values()).items()),
            "max_pairwise_boundary_overlap": max(pairwise),
        })

    # 3. site symmetries of the fine degree and their action on pure columns
    syms = degree_symmetries(degree)
    multiplier_of = {index: frozenset(m) for index, (_w, m, _b) in enumerate(pure)}
    lookup = {frozenset(m): index for index, (_w, m, _b) in enumerate(pure)}
    induced = set()
    for perm in syms:
        image = []
        ok = True
        for index in range(len(pure)):
            moved = frozenset(permute_cell(cell, perm)
                              for cell in multiplier_of[index])
            if moved not in lookup:
                ok = False
                break
            image.append(lookup[moved])
        if ok:
            induced.add(tuple(image))
    induced = sorted(induced)

    # 4. does any induced involution act on a four-subset with alpha -> -alpha?
    odd_witnesses = []
    for choice in combinations(range(len(pure)), 4):
        position = {index: slot for slot, index in enumerate(choice)}
        for image in induced:
            if any(image[index] not in position for index in choice):
                continue
            if any(image[image[index]] != index for index in choice):
                continue
            if all(alpha[position[image[index]]] == -alpha[position[index]]
                   for index in choice):
                odd_witnesses.append({"choice": list(choice),
                                      "involution": list(image)})
    return {
        "component": record["component"],
        "target_degree": list(degree),
        "target_degree_colour_character": [
            sum(degree[3 * s + c] for s in range(8)) for c in range(3)],
        "target_degree_total": sum(degree),
        "target_degree_per_site": [sum(degree[3 * s: 3 * s + 3])
                                   for s in range(8)],
        "component_columns": record["columns"],
        "component_features": record["feature_count"],
        "pure_columns": len(pure),
        "pure_column_boundary_sizes": sorted({len(b) for b in boundaries}),
        "all_features_have_component_degree": homogeneous,
        "four_corner_selections": len(selections),
        "selection_supports": sorted({s["support"] for s in selections}),
        "selection_coefficients": sorted({str(s["coefficients"])
                                          for s in selections}),
        "max_pairwise_corner_overlap": max(s["max_pairwise_boundary_overlap"]
                                           for s in selections),
        "site_permutations_preserving_degree": len(syms),
        "induced_permutations_of_pure_columns": len(induced),
        "induced_permutation_list": [list(p) for p in induced],
        "alpha_odd_involution_witnesses": len(odd_witnesses),
    }


def main():
    records, alpha, pure_word = cached()
    out = {
        "alpha": [int(a) for a in alpha],
        "pure_word": list(pure_word),
        "components": [analyse(record, alpha) for record in records],
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
