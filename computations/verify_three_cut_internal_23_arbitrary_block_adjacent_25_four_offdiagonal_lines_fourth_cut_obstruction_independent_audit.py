#!/usr/bin/env python3
"""Independent exact audit of four off-diagonal A25 affine lines.

The primary verifier and all of its helper modules are deliberately absent
from this import graph.  This audit extends the separately written clean-room
matching/linear-algebra engine used for the E11-line audit.  It reconstructs
all direction-dependent tensors, quotient normals, fibre equations, and
Singular programs for

    A23 = arbitrary X,    A25 = E00 + t E_cd,
    cd in {01, 02, 12, 21}.

Perfect matchings use rightmost-vertex recursion, intersections use double
annihilators over Fraction, and star variables are ordered oppositely to the
primary verifier.  No primary orbit, normal, equation, or certificate is read.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from fractions import Fraction
import hashlib
from itertools import combinations, product
import os
import shutil
import subprocess
import time

import verify_three_cut_internal_23_arbitrary_block_adjacent_25_line_fourth_cut_obstruction_independent_audit as clean


Q = Fraction
DIRECTIONS = ((0, 1), (0, 2), (1, 2), (2, 1))
ACTIVE = (1, 2)
FINAL_CUTS = (0, 1, 5)

# Structural quotient charts.  These data are combinatorial choices, not
# output copied from the primary verifier.
@dataclass(frozen=True)
class Chart:
    name: str
    first: int
    retained: frozenset[int]
    optional: tuple[int, ...]


CHARTS = (
    Chart("x10", clean.X10, frozenset((clean.X10, clean.X11, clean.X21, clean.X22)),
          (clean.X11, clean.X21, clean.X22)),
    Chart("x12", clean.X12, frozenset((clean.X12, clean.X11, clean.X21, clean.X22)),
          (clean.X11, clean.X21, clean.X22)),
    Chart("x20", clean.X20,
          frozenset((clean.X10, clean.X20, clean.X11, clean.X21, clean.X22)),
          (clean.X11, clean.X21, clean.X22)),
    Chart("x22", clean.X22,
          frozenset((clean.X10, clean.X12, clean.X20,
                     clean.X11, clean.X21, clean.X22)),
          (clean.X11, clean.X21)),
)
CHART_BY_FIRST = {chart.first: chart for chart in CHARTS}

EXPECTED_NORMAL_DIMENSIONS = {
    (0, 1): {"x10": 2, "x12": 1, "x20": 2, "x22": 1},
    (0, 2): {"x10": 2, "x12": 1, "x20": 2, "x22": 1},
    (1, 2): {"x10": 2, "x12": 1, "x20": 2, "x22": 1},
    (2, 1): {"x10": 3, "x12": 1, "x20": 3, "x22": 1},
}

# Counts are asserted only after the clean-room equations have been generated.
# They are included to make disagreement with the theorem visible immediately.
EXPECTED_OUTSIDE_COUNTS = {
    (0, 1): {
        "x10": (360, 464, 444, 548, 472, 576, 556, 660),
        "x12": (364, 468, 448, 552, 476, 580, 560),
        "x20": (388, 492, 472, 576, 500, 604, 584, 688),
        "x22": (416, 520, 500, 604),
    },
    (0, 2): {
        "x10": (360, 464, 444, 548, 472, 576, 556, 660),
        "x12": (364, 468, 448, 552, 476, 580, 560),
        "x20": (388, 492, 472, 576, 500, 604, 584, 688),
        "x22": (416, 520, 500, 604),
    },
    (1, 2): {
        "x10": (380, 484, 432, 536, 492, 596, 544, 648),
        "x12": (384, 488, 436, 540, 496, 600, 548),
        "x20": (440, 544, 492, 596, 552, 656, 604, 708),
        "x22": (496, 600, 548, 652),
    },
    (2, 1): {
        "x10": (424, 492, 508, 576, 504, 572, 588, 656),
        "x12": (432, 500, 516, 584, 512, 580, 596),
        "x20": (452, 520, 536, 604, 532, 600, 616, 684),
        "x22": (488, 556, 572, 640),
    },
}
EXPECTED_OLD_COUNTS = {
    (0, 1): (284, 300, 536, 516, 620),
    (0, 2): (284, 300, 536, 516, 620),
    (1, 2): (292, 376, 612, 560, 664),
    (2, 1): (312, 400, 600, 616, 684),
}
EXPECTED_SYMBOLIC_COUNTS = {
    (0, 1): 660,
    (0, 2): 660,
    (1, 2): 648,
    (2, 1): 660,
}

# Frozen after the first clean-room replay so later runs detect any accidental
# change in the independent certificate ledger.
EXPECTED_LEDGER_SHA256 = "a33160985522290a1c511bde58a24f57700625c57a0ef290aa5575eeabeb13c2"
EXPECTED_DIRECTION_SHA256 = {
    (0, 1): "dcf98fea03d46545e86849327606c8b08a6eed626e19c04ccf83c2bea6f87161",
    (0, 2): "df27cc4c54aa8dd23413a2a472bd1288f576d9cb6224ac9e24bbab578af72579",
    (1, 2): "20365fcc281e0d59077530d4a6b3a70087b4eaabc25479b2c28036b46bc68de2",
    (2, 1): "5b62548b3dd12ef05e63d0a88a0d7228882a0c05e65c59c02a7539d989a9e341",
}


def select_direction(cell):
    # All clean-engine routines consult this endpoint-ordered source at call
    # time.  The lower endpoint 2 receives c and upper endpoint 5 receives d.
    clean.T_SOURCE = (2, 5, cell[0], cell[1])


def fixed_character_data(cell):
    coordinate = {
        (site, colour): 3 * site + colour
        for site in clean.INTERIOR for colour in clean.COLOURS
    }
    fixed_rows = []
    for left, right, left_colour, right_colour in clean.BASE_SOURCES:
        row = [0] * 18
        row[coordinate[left, left_colour]] = 1
        row[coordinate[right, right_colour]] = 1
        fixed_rows.append(row)
    assert clean.matrix_rank(fixed_rows) == 8
    kernel = clean.nullspace_numeric(fixed_rows, 18)
    assert len(kernel) == 10

    def character(source):
        left, right, left_colour, right_colour = source
        return tuple(
            vector[coordinate[left, left_colour]]
            + vector[coordinate[right, right_colour]]
            for vector in kernel
        )

    x_rows = tuple(character((2, 3, a, b)) for a, b in clean.CELLS)
    t_row = character((2, 5, cell[0], cell[1]))
    assert clean.matrix_rank(x_rows) == 5
    assert clean.matrix_rank(x_rows + (t_row,)) == 6
    for mask in range(1 << 9):
        selected = tuple(
            x_rows[index] for index in range(9) if mask & (1 << index)
        )
        assert clean.matrix_rank(selected + (t_row,)) == clean.matrix_rank(selected) + 1
    return x_rows, t_row


def audit_torus_and_supports(cell):
    x_rows, _t_row = fixed_character_data(cell)
    census = Counter()
    for mask in range(1 << 9):
        rows = tuple(x_rows[index] for index in range(9) if mask & (1 << index))
        census[len(rows) - clean.matrix_rank(rows)] += 1
    assert tuple(census[index] for index in range(5)) == (328, 132, 42, 9, 1)
    assert set(census) == set(range(5))

    old_masks = []
    masks_by_chart = defaultdict(list)
    finite = []
    cross_masks = []
    for mask in range(1 << 9):
        first = next(
            (index for index in (clean.X10, clean.X12, clean.X20, clean.X22)
             if mask & (1 << index)),
            None,
        )
        if first is None:
            old_masks.append(mask)
        else:
            masks_by_chart[CHART_BY_FIRST[first].name].append(mask)
    assert len(old_masks) == 32
    assert tuple(len(masks_by_chart[chart.name]) for chart in CHARTS) == (
        256, 128, 64, 32,
    )

    expected_signatures = {
        "x10": ((0, 0), (0, 1), (2, 0), (2, 1),
                 (4, 0), (4, 1), (6, 0), (6, 1)),
        "x12": ((0, 0), (0, 1), (2, 0), (2, 1),
                 (4, 0), (4, 1), (6, 0), (6, 1)),
        "x20": ((0, 0), (0, 1), (2, 0), (2, 1),
                 (4, 0), (4, 1), (6, 0), (6, 1)),
        "x22": ((4, 0), (4, 1), (6, 0), (6, 1)),
    }
    for chart in CHARTS:
        observed = sorted({
            (2 * bool(mask & (1 << clean.X11))
             + 4 * bool(mask & (1 << clean.X22)),
             int(bool(mask & (1 << clean.X21))))
            for mask in masks_by_chart[chart.name]
        })
        assert tuple(observed) == expected_signatures[chart.name]
        for signature in observed:
            support = {chart.first}
            d, b = signature
            if d & 2:
                support.add(clean.X11)
            if d & 4:
                support.add(clean.X22)
            if b:
                support.add(clean.X21)
            support = frozenset(support)
            rows = tuple(x_rows[index] for index in sorted(support))
            if chart.name == "x12" and signature == (6, 1):
                assert support == frozenset((clean.X11, clean.X12,
                                             clean.X21, clean.X22))
                assert clean.matrix_rank(rows) == 3
                assert all(
                    x_rows[clean.X12][column] + x_rows[clean.X21][column]
                    - x_rows[clean.X11][column] - x_rows[clean.X22][column] == 0
                    for column in range(len(x_rows[0]))
                )
                assert clean.matrix_rank(tuple(
                    x_rows[index]
                    for index in (clean.X12, clean.X11, clean.X22)
                )) == 3
                cross_masks.extend(
                    mask for mask in masks_by_chart[chart.name]
                    if (2 * bool(mask & (1 << clean.X11))
                        + 4 * bool(mask & (1 << clean.X22)),
                        int(bool(mask & (1 << clean.X21)))) == signature
                )
            else:
                assert clean.matrix_rank(rows) == len(rows)
                finite.append((chart, signature, support))
    assert len(finite) == 27
    assert len(cross_masks) == 16

    # Every old-locus support has no X modulus.  Together with the
    # supportwise t-character check above, nonzero retained coefficients and
    # t can be normalized without sacrificing a continuous invariant.
    for mask in old_masks:
        rows = tuple(x_rows[clean.OLD_GLOBAL_CELLS[bit]]
                     for bit in range(5) if mask & (1 << bit))
        assert clean.matrix_rank(rows) == len(rows)
    return masks_by_chart, tuple(old_masks), tuple(finite), tuple(cross_masks)


def direction_output_blocks(cell):
    select_direction(cell)
    zero_x = clean.coefficients_for(())
    base_atoms = clean.atom_map(zero_x, Q(0))
    x_blocks = []
    x_pairs = []
    for index in range(9):
        delta = clean.delta_map(clean.atom_map(clean.coefficients_for((index,)), Q(0)),
                                base_atoms)
        x_blocks.append(frozenset(key[0] for key in delta))
        x_pairs.append(tuple(sorted({(key[1], key[3]) for key in delta})))
    t_delta = clean.delta_map(clean.atom_map(zero_x, Q(1)), base_atoms)
    t_block = frozenset(key[0] for key in t_delta)
    t_pairs = tuple(sorted({(key[1], key[3]) for key in t_delta}))

    assert all(len(block) == 35 for block in x_blocks)
    assert all(left.isdisjoint(right) for left, right in combinations(x_blocks, 2))
    assert len(set().union(*x_blocks)) == 315
    assert all(pairs == clean.X_COFACTOR_PAIRS for pairs in x_pairs)
    assert len(t_block) == 35
    assert t_pairs == clean.T_COFACTOR_PAIRS
    expected_row = cell[0]
    assert tuple(len(t_block & block) for block in x_blocks) == tuple(
        9 if index // 3 == expected_row else 0 for index in range(9)
    )
    uplus = clean.matching_tensor(clean.INTERIOR, clean.internal_blocks(zero_x, Q(0)))
    assert uplus == {word: Q(1) for word in clean.UPLUS_WORDS}
    assert t_block.isdisjoint(uplus)
    assert not any((colour,) * 6 in t_block for colour in clean.COLOURS)
    return tuple(x_blocks), t_block, uplus


def audit_affinity_and_literal_boundary(cell):
    select_direction(cell)
    clean.audit_no_mixed_terms_and_explicit_t()
    clean.audit_literal_eight_site_identity()


def killed_for_chart(chart, x_blocks):
    return frozenset().union(*(
        x_blocks[index] for index in set(range(9)) - set(chart.retained)
    ))


def four_cut_normal(x_coefficients, killed, final):
    return clean.intersection_many(tuple(
        clean.projected_cylinder(cut, x_coefficients, Q(1), killed)
        for cut in (2, 3, 4, final)
    ))


def audit_omitted_coefficients(x_blocks, uplus):
    zero_x = clean.coefficients_for(())
    for chart in CHARTS:
        killed = killed_for_chart(chart, x_blocks)
        baseline_h = clean.matching_tensor(
            clean.INTERIOR, clean.internal_blocks(zero_x, Q(1)))
        baseline_atoms = clean.atom_map(zero_x, Q(1))
        baseline_columns = {
            cut: clean.insertion_columns(cut, zero_x, Q(1))
            for cut in clean.INTERIOR
        }
        for index in set(range(9)) - set(chart.retained):
            one_x = clean.coefficients_for((index,))
            assert not clean.project_vector(clean.subtract(
                clean.matching_tensor(clean.INTERIOR,
                                      clean.internal_blocks(one_x, Q(1))),
                baseline_h), killed)
            observed_atoms = clean.atom_map(one_x, Q(1))
            for key in set(baseline_atoms) | set(observed_atoms):
                if observed_atoms.get(key, Q(0)) != baseline_atoms.get(key, Q(0)):
                    assert key[0] in killed
            for cut in clean.INTERIOR:
                observed_columns = clean.insertion_columns(cut, one_x, Q(1))
                for baseline, observed in zip(baseline_columns[cut], observed_columns):
                    assert not clean.project_vector(clean.subtract(observed, baseline),
                                                    killed)

    # Independently verify each of the 32 old-locus masks, rather than relying
    # on the primary interval representatives.
    for spec in clean.OLD_CLASSES:
        killed = clean.old_killed(spec, x_blocks, uplus)
        maximal = clean.old_global_support(spec.maximal_mask)
        reference_x = clean.coefficients_for(sorted(maximal))
        reference_h = clean.project_vector(
            clean.matching_tensor(clean.INTERIOR,
                                  clean.internal_blocks(reference_x, Q(1))), killed)
        reference_atoms = clean.project_atoms(clean.atom_map(reference_x, Q(1)), killed)
        reference_columns = {
            cut: tuple(clean.project_vector(column, killed) for column in
                       clean.insertion_columns(cut, reference_x, Q(1)))
            for cut in clean.INTERIOR
        }
        members = [mask for mask in range(32)
                   if clean.old_class_name(mask) == spec.name]
        for mask in members:
            observed_x = clean.coefficients_for(
                sorted(clean.old_global_support(mask)))
            assert clean.project_vector(
                clean.matching_tensor(clean.INTERIOR,
                                      clean.internal_blocks(observed_x, Q(1))),
                killed) == reference_h
            assert clean.project_atoms(clean.atom_map(observed_x, Q(1)),
                                       killed) == reference_atoms
            for cut in clean.INTERIOR:
                observed = tuple(clean.project_vector(column, killed) for column in
                                 clean.insertion_columns(cut, observed_x, Q(1)))
                assert observed == reference_columns[cut]


def assert_safe_normal(normal, killed, x_coefficients, active):
    hs = clean.project_vector(
        clean.matching_tensor(clean.INTERIOR,
                              clean.internal_blocks(x_coefficients, Q(1))), killed)
    assert clean.in_span(hs, normal)
    for colour in active:
        word = (colour,) * 6
        assert word not in killed
        assert not clean.in_span({word: Q(1)}, normal)
    return hs


def outside_cases(cell, families, x_blocks):
    records = []
    by_name = defaultdict(list)
    for chart, signature, support in families:
        killed = killed_for_chart(chart, x_blocks)
        x_coefficients = clean.coefficients_for(sorted(support))
        normals = {
            final: four_cut_normal(x_coefficients, killed, final)
            for final in FINAL_CUTS
        }
        expected_dimension = EXPECTED_NORMAL_DIMENSIONS[cell][chart.name]
        assert all(len(normal) == expected_dimension for normal in normals.values())
        assert clean.same_span(normals[0], normals[1])
        assert clean.same_span(normals[0], normals[5])
        normal = normals[0]
        assert_safe_normal(normal, killed, x_coefficients, ACTIVE)
        atoms = clean.project_atoms(clean.atom_map(x_coefficients, Q(1)), killed)
        grouped = clean.atoms_by_word(atoms)
        program, generators = clean.finite_singular_program(grouped, normal, ACTIVE)
        record = {
            "name": f"{cell[0]}{cell[1]}_outside_{chart.name}_d{signature[0]}_b{signature[1]}",
            "family": chart.name,
            "signature": signature,
            "normal_dimension": len(normal),
            "generators": generators,
            "program": program,
            "direction": cell,
        }
        records.append(record)
        by_name[chart.name].append(record)
    for chart in CHARTS:
        ordered = sorted(by_name[chart.name], key=lambda row: row["signature"])
        assert tuple(row["generators"] for row in ordered) == \
            EXPECTED_OUTSIDE_COUNTS[cell][chart.name]
    assert len(records) == 27
    return tuple(records)


def old_locus_cases(cell, x_blocks, uplus):
    records = []
    members = defaultdict(list)
    for mask in range(32):
        members[clean.old_class_name(mask)].append(mask)
    assert tuple(len(members[spec.name]) for spec in clean.OLD_CLASSES) == (16, 4, 4, 4, 4)
    for spec in clean.OLD_CLASSES:
        killed = clean.old_killed(spec, x_blocks, uplus)
        support = clean.old_global_support(spec.maximal_mask)
        x_coefficients = clean.coefficients_for(sorted(support))
        normals = {
            final: four_cut_normal(x_coefficients, killed, final)
            for final in FINAL_CUTS
        }
        assert clean.same_span(normals[0], normals[1])
        assert clean.same_span(normals[0], normals[5])
        normal = normals[0]
        assert_safe_normal(normal, killed, x_coefficients, spec.active_colours)
        atoms = clean.project_atoms(clean.atom_map(x_coefficients, Q(1)), killed)
        grouped = clean.atoms_by_word(atoms)
        program, generators = clean.finite_singular_program(
            grouped, normal, spec.active_colours)
        records.append({
            "name": f"{cell[0]}{cell[1]}_{spec.name}",
            "family": spec.name,
            "normal_dimension": len(normal),
            "generators": generators,
            "program": program,
            "direction": cell,
        })
    assert tuple(row["generators"] for row in records) == EXPECTED_OLD_COUNTS[cell]
    return tuple(records)


def symbolic_coordinate_polynomial(grouped_atoms, a, b, word):
    return clean.coordinate_polynomial(grouped_atoms, a, b, word, symbolic=True)


def affine_text(constant, slope):
    if not slope:
        return clean.qtext(constant)
    if not constant:
        return f"({clean.qtext(slope)})*lam"
    return f"({clean.qtext(constant)}+({clean.qtext(slope)})*lam)"


def symbolic_line_program(grouped_atoms, hs0, e):
    coordinates = tuple(sorted(
        set(grouped_atoms) | set(hs0) | set(e)
        | {(colour,) * 6 for colour in ACTIVE}
    ))
    pivot = clean.LOCK_WORD
    assert hs0.get(pivot, Q(0)) == 1
    assert not e.get(pivot, Q(0))
    generators = []
    for a, b in product(ACTIVE, repeat=2):
        target = (a,) * 6 if a == b else None
        pivot_beta = symbolic_coordinate_polynomial(grouped_atoms, a, b, pivot)
        pivot_target = Q(1) if target == pivot else Q(0)
        for word in coordinates:
            if word == pivot:
                continue
            beta = symbolic_coordinate_polynomial(grouped_atoms, a, b, word)
            target_value = Q(1) if target == word else Q(0)
            hword = affine_text(hs0.get(word, Q(0)), e.get(word, Q(0)))
            generators.append(
                f"({beta})-({clean.qtext(target_value)})-({hword})*"
                f"(({pivot_beta})-({clean.qtext(pivot_target)}))"
            )
    lines = [
        "ring R=0,(lam," + ",".join(clean.star_variables(ACTIVE)) + "),dp;",
        "option(redSB);",
        "ideal I=" + ",".join(generators) + ";",
        "ideal G=std(I);",
        'print("CLEAN_UNIT"); if(reduce(1,G)==0){1;}else{0;}',
        'print("CLEAN_SIZE"); size(G);',
    ]
    return "\n".join(lines) + "\n", len(generators)


def crossratio_case(cell, x_blocks):
    chart = CHART_BY_FIRST[clean.X12]
    killed = killed_for_chart(chart, x_blocks)
    support0 = (clean.X11, clean.X12, clean.X22)
    support1 = (clean.X11, clean.X12, clean.X21, clean.X22)
    x0 = clean.coefficients_for(support0)
    x1 = clean.coefficients_for(support1)
    x2 = clean.coefficients_for(support1, (Q(1), Q(1), Q(2), Q(1)))

    expanded = {}
    raw = {}
    for cut in clean.INTERIOR:
        columns0 = tuple(clean.project_vector(column, killed) for column in
                         clean.insertion_columns(cut, x0, Q(1)))
        columns1 = tuple(clean.project_vector(column, killed) for column in
                         clean.insertion_columns(cut, x1, Q(1)))
        columns2 = tuple(clean.project_vector(column, killed) for column in
                         clean.insertion_columns(cut, x2, Q(1)))
        for at_zero, at_one, at_two in zip(columns0, columns1, columns2):
            assert at_two == clean.linear_combination(((at_one, Q(2)),
                                                       (at_zero, Q(-1))))
        raw[cut] = (columns0, columns1)
        expanded[cut] = clean.rref_basis(columns0 + columns1)[0]

    hs0 = clean.project_vector(
        clean.matching_tensor(clean.INTERIOR, clean.internal_blocks(x0, Q(1))),
        killed)
    hs1 = clean.project_vector(
        clean.matching_tensor(clean.INTERIOR, clean.internal_blocks(x1, Q(1))),
        killed)
    e = clean.subtract(hs1, hs0)
    assert e == {clean.E_WORD: Q(1)}
    assert hs0.get(clean.E_WORD, Q(0)) == 0
    assert hs0.get(clean.LOCK_WORD, Q(0)) == 1
    assert clean.LOCK_WORD not in e

    expected_plane = (e, hs0)
    for final in FINAL_CUTS:
        upper = clean.intersection_many(tuple(
            expanded[cut] for cut in (2, 3, 4, final)
        ))
        assert len(upper) == 2
        assert clean.same_span(upper, expected_plane)

        # ell_lam = E* - lam LOCK* annihilates every raw final-cylinder
        # column coefficientwise.  Since any actual common normal is inside
        # the expanded plane, this locks it into span(H_S(lambda)).
        for constant, at_one in zip(*raw[final]):
            slope = clean.subtract(at_one, constant)
            coefficients = (
                constant.get(clean.E_WORD, Q(0)),
                slope.get(clean.E_WORD, Q(0))
                - constant.get(clean.LOCK_WORD, Q(0)),
                -slope.get(clean.LOCK_WORD, Q(0)),
            )
            assert coefficients == (0, 0, 0)

    atoms0 = clean.project_atoms(clean.atom_map(x0, Q(1)), killed)
    atoms1 = clean.project_atoms(clean.atom_map(x1, Q(1)), killed)
    atoms2 = clean.project_atoms(clean.atom_map(x2, Q(1)), killed)
    for key in set(atoms0) | set(atoms1) | set(atoms2):
        assert atoms2.get(key, Q(0)) == (
            2 * atoms1.get(key, Q(0)) - atoms0.get(key, Q(0))
        )
    symbolic_atoms = clean.linear_atom_map(atoms0, atoms1)
    grouped = clean.atoms_by_word(symbolic_atoms)
    program, generators = symbolic_line_program(grouped, hs0, e)
    assert generators == EXPECTED_SYMBOLIC_COUNTS[cell]
    return {
        "name": f"{cell[0]}{cell[1]}_outside_x12_crossratio_lambda",
        "family": "x12_crossratio",
        "normal_dimension": 1,
        "generators": generators,
        "program": program,
        "direction": cell,
    }


def build_direction(cell):
    select_direction(cell)
    _masks, old_masks, families, cross_masks = audit_torus_and_supports(cell)
    assert len(old_masks) + sum((256, 128, 64, 32)) == 512
    assert len(cross_masks) == 16
    x_blocks, t_block, uplus = direction_output_blocks(cell)
    audit_affinity_and_literal_boundary(cell)
    audit_omitted_coefficients(x_blocks, uplus)
    outside = outside_cases(cell, families, x_blocks)
    old = old_locus_cases(cell, x_blocks, uplus)
    symbolic = crossratio_case(cell, x_blocks)
    records = old + outside + (symbolic,)
    assert len(records) == 33
    return records, t_block


def program_hash(record):
    return hashlib.sha256(record["program"].encode()).hexdigest()


def ledger_hash(records):
    rows = [
        f'{record["name"]}|{record["generators"]}|{record["normal_dimension"]}|'
        f'{program_hash(record)}'
        for record in sorted(records, key=lambda row: row["name"])
    ]
    return hashlib.sha256("\n".join(rows).encode()).hexdigest()


def audit_template_duplicates(records):
    by_direction = {
        cell: {program_hash(record) for record in records
               if record["direction"] == cell}
        for cell in DIRECTIONS
    }
    assert all(len(hashes) == 33 for hashes in by_direction.values())
    assert len(set().union(*by_direction.values())) == 102
    assert len(by_direction[(0, 1)] & by_direction[(0, 2)]) == 30
    for left, right in combinations(DIRECTIONS, 2):
        if {left, right} == {(0, 1), (0, 2)}:
            continue
        assert not (by_direction[left] & by_direction[right])

    # Identify rather than merely count the three nonshared 01/02 templates.
    hashes01 = {program_hash(record): record["family"] for record in records
                if record["direction"] == (0, 1)}
    hashes02 = {program_hash(record): record["family"] for record in records
                if record["direction"] == (0, 2)}
    assert Counter(hashes01[h] for h in set(hashes01) - set(hashes02)) == Counter({
        "old_x00_x21_no_x11": 1,
        "old_x00_x11_no_x21": 1,
        "old_x00_x11_x21": 1,
    })
    assert Counter(hashes02[h] for h in set(hashes02) - set(hashes01)) == Counter({
        "old_x00_x21_no_x11": 1,
        "old_x00_x11_no_x21": 1,
        "old_x00_x11_x21": 1,
    })


def marker(output, name):
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    return int(lines[lines.index(name) + 1])


def run_singular(record):
    singular = shutil.which("Singular")
    if singular is None:
        raise RuntimeError("Singular is required for this exact-Q audit")
    started = time.monotonic()
    completed = subprocess.run(
        [singular, "-q"], input=record["program"], text=True,
        capture_output=True, check=True, timeout=3600)
    if completed.stderr.strip():
        raise AssertionError(f'{record["name"]}: {completed.stderr}')
    assert marker(completed.stdout, "CLEAN_UNIT") == 1
    assert marker(completed.stdout, "CLEAN_SIZE") == 1
    return record["name"], record["direction"], time.monotonic() - started


def run_all(records, workers):
    elapsed = {}
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(run_singular, record): record["name"]
                   for record in records}
        for future in as_completed(futures):
            name, cell, duration = future.result()
            elapsed[name] = duration
            print(f"independent certificate {name}: unit ({duration:.3f}s)", flush=True)
    assert len(elapsed) == len(records)
    return elapsed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--geometry-only", action="store_true")
    parser.add_argument("--workers", type=int,
                        default=min(12, max(1, os.cpu_count() or 1)))
    args = parser.parse_args()
    started = time.monotonic()

    all_records = []
    for cell in DIRECTIONS:
        records, _t_block = build_direction(cell)
        all_records.extend(records)
        print(f"independent direction={cell[0]}{cell[1]} geometry: PASS jobs=33",
              flush=True)
    assert len(all_records) == 132
    audit_template_duplicates(all_records)

    digest = ledger_hash(all_records)
    direction_digests = {
        cell: ledger_hash(tuple(record for record in all_records
                                if record["direction"] == cell))
        for cell in DIRECTIONS
    }
    assert digest == EXPECTED_LEDGER_SHA256, (digest, EXPECTED_LEDGER_SHA256)
    assert direction_digests == EXPECTED_DIRECTION_SHA256
    print(f"independent ledger SHA256: {digest}")
    for cell in DIRECTIONS:
        print(f"independent direction={cell[0]}{cell[1]} ledger SHA256: "
              f"{direction_digests[cell]}")
    print("independent templates: 102; shared 01/02: 30; all other overlaps: 0")
    if args.geometry_only:
        print(f"independent geometry wall time: {time.monotonic() - started:.3f}s")
        return

    exact_started = time.monotonic()
    elapsed = run_all(all_records, max(1, args.workers))
    print("independent four-offdiagonal A25 audit: PASS")
    print("t=0 inherited; t!=0 supportwise independent and normalized: PASS")
    print("512 supports per direction; 4*(5 old+27 finite+1 Q[lambda]): PASS")
    print("rightmost endpoint-ordered matchings and literal eight-site fibres: PASS")
    print("safe projected normals, arbitrary omitted X, 108 stars, arbitrary A67: PASS")
    for cell in DIRECTIONS:
        selected = [elapsed[record["name"]] for record in all_records
                    if record["direction"] == cell]
        print(f"direction={cell[0]}{cell[1]} exact_wall_max={max(selected):.3f}s "
              f"certificates={len(selected)}")
    print(f"independent exact-Q wall time: {time.monotonic() - exact_started:.3f}s")
    print(f"independent total wall time: {time.monotonic() - started:.3f}s")


if __name__ == "__main__":
    main()
