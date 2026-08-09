#!/usr/bin/env python3
"""Exact source-faithful Segre leaf template for all five-cross pair blocks."""

from __future__ import annotations

import importlib.util
from collections import Counter
from pathlib import Path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_palette():
    path = Path(__file__).with_name(
        "verify_n10_five_cross_affine_signature_palette.py"
    )
    spec = importlib.util.spec_from_file_location("signature_palette", path)
    require(spec is not None and spec.loader is not None, "cannot load palette")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def add_exponents(left, right):
    return tuple(a + b for a, b in zip(left, right))


def main() -> None:
    palette = load_palette()
    five = palette.load_five_frontier()
    four = five.load_four_closure()
    bounded = four.load_bounded_frontier()
    data = bounded.prepare()
    left_coordinates = tuple(
        coordinate for coordinate in data["coordinates"] if coordinate[1] == 8
    )
    right_coordinates = tuple(
        coordinate for coordinate in data["coordinates"] if coordinate[1] == 9
    )
    pair_survivors = five.universal_pair_survivors(
        data, left_coordinates, right_coordinates
    )
    require(len(pair_survivors) == 196, "pair-survivor count changed")

    # The six possible crossing products are the coordinates of a 2 by 3
    # rank-one matrix.  Their three quadratic Segre relations hold already
    # at the monomial-exponent level, without evaluating coefficients.
    segre_coordinates = (
        (1, 0, 1, 0, 0),  # ac
        (1, 0, 0, 1, 0),  # ad
        (1, 0, 0, 0, 1),  # ae
        (0, 1, 1, 0, 0),  # bc
        (0, 1, 0, 1, 0),  # bd
        (0, 1, 0, 0, 1),  # be
    )
    segre_relations = ((0, 4, 1, 3), (0, 5, 2, 3), (1, 5, 2, 4))
    require(
        all(
            add_exponents(segre_coordinates[i], segre_coordinates[j])
            == add_exponents(segre_coordinates[k], segre_coordinates[l])
            for i, j, k, l in segre_relations
        ),
        "Segre monomial relations changed",
    )

    grade_signature_ids = {}
    grade_ids = []
    for record in data["grade_data"]:
        signature = (
            palette.basis_key(record[1]),
            palette.table_key(record[2]),
            record[3],
        )
        grade_ids.append(
            grade_signature_ids.setdefault(signature, len(grade_signature_ids))
        )
    require(len(grade_signature_ids) == 1_805, "grade signatures changed")

    labelled_leaf_templates = {}
    grade_valencies = Counter()
    valid_edge_total = 0
    for pair in pair_survivors:
        pair_grades = set()
        leaves = []
        for right in right_coordinates:
            leaf = []
            for left_index, left in enumerate(pair):
                grade = data["oriented_pair_to_grade"].get((left, right))
                require(
                    grade == bounded.grade_for_coordinates(data, left, right),
                    "leaf grade lookup changed",
                )
                if grade is None:
                    continue
                leaf.append((left_index, grade_ids[grade]))
                pair_grades.add(grade)
                valid_edge_total += 1
            require(len(leaf) in (0, 1, 2), "bad leaf valency")
            leaves.append(tuple(leaf))
        require(len(pair_grades) == 126, "a pair grade collision appeared")
        grade_valencies[len(pair_grades)] += 1
        labelled_leaf_templates[pair] = tuple(leaves)
    require(valid_edge_total == 196 * 126 == 24_696, "leaf edge count changed")
    require(grade_valencies == Counter({126: 196}), "pair valencies changed")
    require(
        len(set(labelled_leaf_templates.values())) == 196,
        "labelled source-faithful leaf templates collided",
    )

    span_groups, _signatures, unlabelled_leaf_maps = (
        palette.exact_pair_signatures(
            data, pair_survivors, right_coordinates
        )
    )
    require(len(span_groups) == 66, "two-centre span quotient changed")
    require(
        len(set(unlabelled_leaf_maps.values())) == 196,
        "source-faithful leaf-map obstruction changed",
    )

    # A weight-independent row functional cannot finish any survivor pair:
    # by definition of the exact pair sieve, all old residual rows already
    # lie in the universal span of its 126 grade cylinders.
    module = data["module"]
    two_cell = data["two_cell"]
    universal_absorptions = 0
    for pair in pair_survivors:
        grades = {
            data["oriented_pair_to_grade"][(left, right)]
            for left in pair
            for right in right_coordinates
            if (left, right) in data["oriented_pair_to_grade"]
        }
        generators = []
        for grade in grades:
            generators.extend(data["grade_data"][grade][1].values())
            generators.extend(data["grade_data"][grade][2].values())
        basis = module.rational_basis(generators)
        if all(
            module.rational_member(row, basis)
            for row in data["residual_q"].values()
        ):
            universal_absorptions += 1
        require(
            not {
                word: two_cell.quotient_remainder(row, basis)
                for word, row in data["residual_q"].items()
                if not module.rational_member(row, basis)
            },
            "a survivor pair regained a universal linear obstruction",
        )
    require(universal_absorptions == 196, "universal absorption count changed")
    require(
        four.discrete_stabilizer(data) == ((tuple(range(8)), tuple(range(3))),),
        "anchored source stabilizer changed",
    )

    shape_census = Counter(map(palette.pair_shape, pair_survivors))
    require(len(shape_census) == 12, "ambient pair-shape count changed")
    print("N=10 five-cross Segre leaf template: exact PASS")
    print("pair survivors: 196; leaf records: 14112; valid grade edges: 24696")
    print("every pair: 126 distinct source grades; Segre coordinates: 6")
    print("Segre relations: 3; ambient shapes: 12; exact span signatures: 66")
    print("source-faithful leaf templates: 196 (no transfer collision)")
    print("universal pair spans absorbing the old residual: 196")
    print("stopping point: literal Fitting minors still require leaf provenance")


if __name__ == "__main__":
    main()
