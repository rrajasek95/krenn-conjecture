#!/usr/bin/env python3
"""Quotient systems for the coupled adjacent directions A25=E00+tE10, tE20.

The moving stabilizer character of these two directions is dependent:
wt(t) = wt(x10) - wt(x00), respectively wt(t) = wt(x20) - wt(x00).  No
independent normalization of t exists on supports whose character span
already contains the moving character, so every case below keeps t as an
ordinary polynomial ring variable.  A unit ideal over Q[t, ...] therefore
covers every complex t, including t=0 and every cross-ratio value.

Structure, following the audited E11 quotient theorem:

* the 512 A23 supports split into the 32-mask old five-cell locus (five
  classes) and 480 outside masks (27 finite retained charts plus one
  Q[lam,t] chart for the x12+x21=x11+x22 circuit);
* each case kills the coordinate blocks of its non-retained cells, so those
  coefficients are provably arbitrary;
* all tensors and insertion columns are affine in (t, lam) jointly, with no
  cross terms (edges 23 and 25 share site 2; the circuit cell x21 lies on
  edge 23).  Spanning the cylinders at the affine specialization points
  gives a rational overspace of the projected common normal valid for every
  parameter value;
* when the plain overspace membership packet is not already contradictory,
  exact pointwise lock functionals phi(theta) with phi(theta).c(theta)=0
  for every insertion column restore the lost cylinder information.

This module is a generator/discovery driver; the two standalone verifiers
freeze its output ledgers.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import itertools
import shutil
import subprocess
import time

import explore_three_cut_internal_23_adjacent_25_11 as adjacent
import explore_three_cut_internal_23_full_supports as full
import explore_three_cut_internal_23_perturbation as equations
import test_three_cut_internal_23_x12_crossratio_symbolic as old_symbolic
import verify_three_cut_internal_23_arbitrary_block_fourth_cut_obstruction as old_full
import verify_three_cut_internal_23_plane_support_fourth_cut_obstruction as old_locus


Q = full.Q
CUTS = (0, 1, 5)
LOCAL_TO_FULL = (0, 1, 2, 4, 7)
PAIR_ORDER = ((1, 2), (0, 2), (0, 1))
DIRECTIONS = {"10": (1, 0), "20": (2, 0)}

EXPECTED_GEOMETRY = {
    (1, 0): {
        "t_block": 35,
        "x_overlaps": (0, 0, 0, 9, 9, 12, 0, 0, 0),
        "uplus_overlap": 2,
        "targets_in_t_block": (False, False, False),
        "details": ((0, 3), (0, 4), (1, 3), (3, 4)),
    },
    (2, 0): {
        "t_block": 35,
        "x_overlaps": (0, 0, 0, 0, 0, 0, 9, 9, 12),
        "uplus_overlap": 0,
        "targets_in_t_block": (False, False, False),
        "details": ((0, 3), (0, 4), (1, 3), (3, 4)),
    },
}


def select_direction(cell):
    adjacent.T_CELL = cell
    adjacent.T_BLOCK, adjacent.T_DETAILS = adjacent.variable_coordinate_block(
        adjacent.T_EDGE, cell
    )


def audit_direction_geometry(cell):
    expected = EXPECTED_GEOMETRY[cell]
    adjacent.no_mixed_x_t_terms()
    assert len(adjacent.T_BLOCK) == expected["t_block"]
    assert tuple(adjacent.T_DETAILS) == expected["details"]
    assert tuple(
        len(adjacent.T_BLOCK & block) for block in adjacent.X_BLOCKS
    ) == expected["x_overlaps"]
    assert len(adjacent.T_BLOCK & set(full.UPLUS)) == expected["uplus_overlap"]
    assert tuple(
        (colour,) * 6 in adjacent.T_BLOCK for colour in full.COLOURS
    ) == expected["targets_in_t_block"]


def audit_coupled_stabilizer(cell):
    """The moving character is dependent: wt(t)=wt(x_cd)-wt(x00)."""
    import sympy as sp

    fixed = (
        ((0, 1), (0, 0)), ((4, 5), (0, 0)),
        ((0, 2), (1, 1)), ((1, 4), (1, 1)),
        ((0, 4), (2, 2)), ((1, 3), (2, 2)),
        ((2, 5), (0, 0)), ((3, 5), (1, 0)),
    )
    constraints = sp.Matrix.vstack(*(
        adjacent.cell_weight(edge, fixed_cell) for edge, fixed_cell in fixed
    ))
    assert constraints.rank() == 8
    kernel = sp.Matrix.hstack(*constraints.nullspace())
    x_rows = tuple(
        adjacent.cell_weight((2, 3), x_cell) * kernel for x_cell in full.CELLS
    )
    t_row = adjacent.cell_weight((2, 5), cell) * kernel
    stack = sp.Matrix.vstack(*x_rows)
    assert stack.rank() == 5
    assert sp.Matrix.vstack(stack, t_row).rank() == 5
    difference = x_rows[full.CELLS.index(cell)] - x_rows[0]
    assert (t_row - difference).is_zero_matrix
    return True


def audit_literal_boundary_identity():
    coefficients = {
        cell: Q(2001 + bit) for bit, cell in enumerate(full.CELLS)
    }
    internal = adjacent.blocks_for(coefficients, Q(2501))
    p = {
        (a, i, c): Q(1 + 100 * a + 10 * i + c)
        for a in full.COLOURS for i in full.SIX for c in full.COLOURS
    }
    q = {
        (b, i, c): Q(701 + 100 * b + 10 * i + c)
        for b in full.COLOURS for i in full.SIX for c in full.COLOURS
    }
    r = {
        (a, b): Q(1301 + 10 * a + b)
        for a in full.COLOURS for b in full.COLOURS
    }
    blocks = {edge: dict(block) for edge, block in internal.items()}
    for i in full.SIX:
        blocks[i, 6] = {
            (c, a): p[a, i, c] for c in full.COLOURS for a in full.COLOURS
        }
        blocks[i, 7] = {
            (c, b): q[b, i, c] for c in full.COLOURS for b in full.COLOURS
        }
    blocks[6, 7] = dict(r)
    observed_full = equations.cylinders.matching_tensor(tuple(range(8)), blocks)
    hs = equations.cylinders.matching_tensor(full.SIX, internal)
    word_terms = equations.reconstruct_word_terms(internal)
    for a, b in itertools.product(full.COLOURS, repeat=2):
        observed = {
            word[:6]: value for word, value in observed_full.items()
            if word[6:] == (a, b)
        }
        expected = {}
        for word, value in hs.items():
            equations.cylinders.add(expected, word, r[a, b] * value)
        for word, values in word_terms.items():
            total = Q(0)
            for ((i, c), (j, d)), value in values:
                total += value * (
                    p[a, i, c] * q[b, j, d] + p[a, j, d] * q[b, i, c]
                )
            equations.cylinders.add(expected, word, total)
        assert observed == expected


def old_class_killed(maximal_local, retained_local):
    maximal_full = {
        LOCAL_TO_FULL[bit] for bit in range(5) if maximal_local & (1 << bit)
    }
    retained_full = {LOCAL_TO_FULL[bit] for bit in retained_local}
    retained_union = set(adjacent.T_BLOCK)
    for bit in retained_full:
        retained_union.update(adjacent.X_BLOCKS[bit])
    killed = set(full.UPLUS) - retained_union
    for bit in maximal_full - retained_full:
        killed.update(adjacent.X_BLOCKS[bit])
    return killed


def specialization_points(parameters):
    points = [dict.fromkeys(parameters, Q(0))]
    for name in parameters:
        point = dict.fromkeys(parameters, Q(0))
        point[name] = Q(1)
        points.append(point)
    return tuple(points)


def blocks_at(coefficients, point, lam_bit=None):
    values = dict(coefficients)
    if lam_bit is not None:
        lam = point.get("lam", Q(0))
        if lam:
            values[full.CELLS[lam_bit]] = lam
        else:
            values.pop(full.CELLS[lam_bit], None)
    return adjacent.blocks_for(values, point.get("t", Q(0)))


def coefficient_maps_at(coefficients, point, killed, lam_bit=None):
    blocks = blocks_at(coefficients, point, lam_bit)
    maps = old_symbolic.coefficient_maps(
        equations.reconstruct_word_terms(blocks)
    )
    return {word: data for word, data in maps.items() if word not in killed}


def audit_affine_exactness(coefficients, parameters, killed, lam_bit=None):
    """Word terms are jointly affine in (t, lam): no cross or higher terms."""
    points = specialization_points(parameters)
    base = coefficient_maps_at(coefficients, points[0], killed, lam_bit)
    slopes = []
    for point in points[1:]:
        at_one = coefficient_maps_at(coefficients, point, killed, lam_bit)
        slope = {}
        for word in set(base) | set(at_one):
            row = {}
            left = base.get(word, {})
            right = at_one.get(word, {})
            for endpoint in set(left) | set(right):
                value = right.get(endpoint, Q(0)) - left.get(endpoint, Q(0))
                if value:
                    row[endpoint] = value
            if row:
                slope[word] = row
        slopes.append(slope)
    probes = [dict(zip(parameters, values)) for values in (
        (Q(1),) * len(parameters),
        tuple(Q(2 + index) for index in range(len(parameters))),
    )]
    for probe in probes:
        observed = coefficient_maps_at(coefficients, probe, killed, lam_bit)
        expected = {}
        for word, data in base.items():
            expected[word] = dict(data)
        for name, slope in zip(parameters, slopes):
            factor = probe[name]
            for word, row in slope.items():
                target = expected.setdefault(word, {})
                for endpoint, value in row.items():
                    total = target.get(endpoint, Q(0)) + factor * value
                    if total:
                        target[endpoint] = total
                    else:
                        target.pop(endpoint, None)
        expected = {
            word: data for word, data in expected.items() if data
        }
        assert observed == expected, "terms are not affine in the parameters"
    return base, slopes


def projected_columns_raw(cut, blocks, killed):
    u_sites = tuple(site for site in full.SIX if site != cut)
    five_columns = equations.cylinders.insertion_columns(u_sites, blocks)
    columns = []
    for colour_z in full.COLOURS:
        for column in five_columns:
            vector = {}
            for u_word, coefficient in column.items():
                assignment = dict(zip(u_sites, u_word))
                assignment[cut] = colour_z
                word = tuple(assignment[site] for site in full.SIX)
                if word not in killed:
                    equations.cylinders.add(vector, word, coefficient)
            columns.append(vector)
    return columns


def column_families(coefficients, parameters, killed, lam_bit=None):
    points = specialization_points(parameters)
    families = {}
    for cut in range(6):
        per_point = [
            projected_columns_raw(
                cut, blocks_at(coefficients, point, lam_bit), killed
            )
            for point in points
        ]
        base = per_point[0]
        slopes = []
        for at_one in per_point[1:]:
            slopes.append([
                {
                    word: at_one[index].get(word, Q(0))
                    - base[index].get(word, Q(0))
                    for word in set(base[index]) | set(at_one[index])
                }
                for index in range(len(base))
            ])
        families[cut] = (base, slopes)
    return families


def audit_column_affine_exactness(
    coefficients, parameters, killed, families, lam_bit=None
):
    probe = dict(zip(parameters, (Q(3), Q(5))[: len(parameters)]))
    for cut in range(6):
        base, slopes = families[cut]
        observed = projected_columns_raw(
            cut, blocks_at(coefficients, probe, lam_bit), killed
        )
        for index in range(len(base)):
            expected = dict(base[index])
            for name, slope in zip(parameters, slopes):
                factor = probe[name]
                for word, value in slope[index].items():
                    equations.cylinders.add(expected, word, factor * value)
            expected = {
                word: value for word, value in expected.items() if value
            }
            cleaned = {
                word: value for word, value in observed[index].items() if value
            }
            assert expected == cleaned, (cut, index)


def lock_functionals(families, cut, coordinates):
    """Basis of phi(theta)=phi0+sum theta_k phi_k with phi(theta).c(theta)=0.

    The conditions are exact for every parameter value: constant, linear,
    and quadratic coefficients of theta all vanish.
    """
    base, slopes = families[cut]
    parameter_count = len(slopes)
    index = {word: position for position, word in enumerate(coordinates)}
    width = (parameter_count + 1) * len(coordinates)
    rows = []

    def chunk(vector, part):
        row = {}
        for word, value in vector.items():
            if word in index and value:
                row[part * len(coordinates) + index[word]] = value
        return row

    for column_index in range(len(base)):
        constant = base[column_index]
        deltas = [slope[column_index] for slope in slopes]
        row = chunk(constant, 0)
        if row:
            rows.append(row)
        for k in range(parameter_count):
            row = chunk(deltas[k], 0)
            for key, value in chunk(constant, k + 1).items():
                row[key] = row.get(key, Q(0)) + value
            row = {key: value for key, value in row.items() if value}
            if row:
                rows.append(row)
        for k in range(parameter_count):
            for j in range(k, parameter_count):
                row = chunk(deltas[j], k + 1)
                if j != k:
                    for key, value in chunk(deltas[k], j + 1).items():
                        row[key] = row.get(key, Q(0)) + value
                row = {key: value for key, value in row.items() if value}
                if row:
                    rows.append(row)
    basis = equations.cylinders.annihilator_basis(rows, tuple(range(width)))
    locks = []
    for vector in basis:
        parts = []
        for part in range(parameter_count + 1):
            component = {}
            for position, value in vector.items():
                if part * len(coordinates) <= position < (part + 1) * len(coordinates):
                    component[coordinates[position - part * len(coordinates)]] = value
            parts.append(component)
        locks.append(tuple(parts))
    return locks


def audit_locks(families, cut, locks, parameters):
    base, slopes = families[cut]
    probes = [
        dict(zip(parameters, values))
        for values in ((Q(0),) * len(parameters), (Q(1), Q(0))[: len(parameters)],
                       (Q(2), Q(3))[: len(parameters)])
    ]
    for probe in probes:
        columns = []
        for index in range(len(base)):
            vector = dict(base[index])
            for name, slope in zip(parameters, slopes):
                factor = probe[name]
                for word, value in slope[index].items():
                    equations.cylinders.add(vector, word, factor * value)
            columns.append(vector)
        for lock in locks:
            functional = dict(lock[0])
            for name, part in zip(parameters, lock[1:]):
                factor = probe[name]
                for word, value in part.items():
                    equations.cylinders.add(functional, word, factor * value)
            for vector in columns:
                total = sum(
                    (functional.get(word, Q(0)) * value
                     for word, value in vector.items()),
                    Q(0),
                )
                assert total == 0
    return True


def parameter_text(parameters, constant, slopes):
    pieces = []
    if constant:
        pieces.append(equations.qtext(constant))
    for name, slope in zip(parameters, slopes):
        if slope:
            pieces.append(f"{name}*(" + equations.qtext(slope) + ")")
    return "+".join(pieces) if pieces else "0"


def bilinear_text(parameters, base, slopes, a, b, word):
    maps = [base.get(word, {})] + [slope.get(word, {}) for slope in slopes]
    endpoints = sorted(set().union(*maps))
    terms = []
    for left, right in endpoints:
        coefficient = parameter_text(
            parameters,
            maps[0].get((left, right), Q(0)),
            [component.get((left, right), Q(0)) for component in maps[1:]],
        )
        if coefficient == "0":
            continue
        terms.append(
            "(" + coefficient + ")*("
            + equations.variable("p", a, left) + "*"
            + equations.variable("q", b, right) + "+"
            + equations.variable("p", a, right) + "*"
            + equations.variable("q", b, left) + ")"
        )
    return "+".join(terms) if terms else "0"


def case_normals(coefficients, parameters, killed, lam_bit=None):
    points = specialization_points(parameters)
    block_list = tuple(
        blocks_at(coefficients, point, lam_bit) for point in points
    )
    normals = {
        cut: full.expanded_projected_cylinder_intersection(
            (2, 3, 4, cut), block_list, killed
        )
        for cut in CUTS
    }
    h_points = tuple(
        full.project_vector(
            equations.cylinders.matching_tensor(full.SIX, blocks), killed
        )
        for blocks in block_list
    )
    return normals, h_points


def build_system(
    name, parameters, base, slopes, basis, coordinates, active, final_cut,
    lock_rows,
):
    rows = equations.membership_rows(basis, coordinates)
    generators = []
    for a, b in itertools.product(active, repeat=2):
        target_word = (a,) * 6 if a == b else None
        for row in rows:
            terms = []
            constant = Q(0)
            for word, row_coefficient in row.items():
                expression = bilinear_text(parameters, base, slopes, a, b, word)
                if expression != "0":
                    terms.append(
                        "(" + equations.qtext(row_coefficient) + ")*("
                        + expression + ")"
                    )
                if word == target_word:
                    constant -= row_coefficient
            if constant:
                terms.append(equations.qtext(constant))
            generators.append("+".join(terms) if terms else "0")
        for lock in lock_rows:
            terms = []
            tail_constant = [Q(0)] * len(lock)
            for word in sorted(set().union(*lock)):
                expression = bilinear_text(parameters, base, slopes, a, b, word)
                coefficient = parameter_text(
                    parameters, lock[0].get(word, Q(0)),
                    [part.get(word, Q(0)) for part in lock[1:]],
                )
                if expression != "0" and coefficient != "0":
                    terms.append(
                        "(" + coefficient + ")*(" + expression + ")"
                    )
                if word == target_word:
                    for part_index, part in enumerate(lock):
                        tail_constant[part_index] -= part.get(word, Q(0))
            tail = parameter_text(
                parameters, tail_constant[0], tail_constant[1:]
            )
            if tail != "0":
                terms.append(tail)
            generators.append("+".join(terms) if terms else "0")
        del target_word
    generators = [g for g in dict.fromkeys(generators) if g != "0"]
    endpoints = tuple(itertools.product(range(6), range(3)))
    star_names = [
        equations.variable(kind, boundary, endpoint)
        for kind in ("p", "q") for boundary in active for endpoint in endpoints
    ]
    body = ",".join(generators)
    names = list(parameters) + [name for name in star_names if name in body]
    program = "ring r=0,(" + ",".join(names) + "),dp;\n"
    program += "option(redSB);\n"
    program += "ideal I=" + body + ";\n"
    program += "ideal G=slimgb(I);\n"
    program += 'print("UNIT"); if(G[1]==1){1;}else{0;}\n'
    program += 'print("GBSIZE"); size(G);\n'
    return program, len(generators)


class Case:
    def __init__(
        self, name, coefficients, killed, parameters, lam_bit=None,
        retained=(),
    ):
        self.name = name
        self.coefficients = coefficients
        self.killed = killed
        self.parameters = parameters
        self.lam_bit = lam_bit
        self.retained = tuple(retained)

    def prepare(self):
        self.base, self.slopes = audit_affine_exactness(
            self.coefficients, self.parameters, self.killed, self.lam_bit
        )
        self.families = column_families(
            self.coefficients, self.parameters, self.killed, self.lam_bit
        )
        audit_column_affine_exactness(
            self.coefficients, self.parameters, self.killed, self.families,
            self.lam_bit,
        )
        self.normals, self.h_points = case_normals(
            self.coefficients, self.parameters, self.killed, self.lam_bit
        )
        for cut in CUTS:
            span = equations.cylinders.echelon(self.normals[cut])
            for h_point in self.h_points:
                assert equations.cylinders.member(h_point, span), (
                    self.name, cut,
                )

    def admissible_pairs(self, cut):
        span = equations.cylinders.echelon(self.normals[cut])
        good = tuple(
            colour for colour in full.COLOURS
            if (colour,) * 6 not in self.killed
            and not equations.cylinders.member(
                {(colour,) * 6: Q(1)}, span
            )
        )
        return tuple(
            pair for pair in PAIR_ORDER
            if pair[0] in good and pair[1] in good
        )

    def coordinates_for(self, cut, active):
        return tuple(sorted(
            set(self.base)
            | set().union(*(set(slope) for slope in self.slopes))
            | {word for vector in self.normals[cut] for word in vector}
            | {(colour,) * 6 for colour in active}
        ))

    def system(self, cut, active, with_locks):
        coordinates = self.coordinates_for(cut, active)
        lock_rows = []
        if with_locks:
            for lock_cut in (2, 3, 4, cut):
                locks = lock_functionals(self.families, lock_cut, coordinates)
                audit_locks(self.families, lock_cut, locks, self.parameters)
                lock_rows.extend(locks)
        return build_system(
            self.name, self.parameters, self.base, self.slopes,
            self.normals[cut], coordinates, active, cut, lock_rows,
        )


def outside_cases():
    cases = []
    for name in ("x10", "x12", "x20", "x22"):
        spec = old_full.FAMILIES[name]
        killed = adjacent.quotient_killed(spec["retained"], retain_t=True)
        for pattern in spec["patterns"]:
            for x21 in spec["x21"]:
                if name == "x12" and pattern == 6 and x21:
                    continue
                coefficients = old_full.coefficients_for_case(
                    spec, pattern, x21
                )
                cases.append(Case(
                    f"outside_{name}_d{pattern}_b{x21}",
                    coefficients, killed, ("t",),
                    retained=spec["retained"],
                ))
    spec = old_full.FAMILIES["x12"]
    killed = adjacent.quotient_killed(spec["retained"], retain_t=True)
    coefficients = old_full.coefficients_for_case(spec, 6, 0)
    cases.append(Case(
        "outside_x12_crossratio", coefficients, killed, ("t", "lam"),
        lam_bit=7, retained=spec["retained"],
    ))
    return cases


def old_cases():
    cases = []
    for spec in old_locus.CLASS_SPECS:
        name, maximal, retained_local = spec[0], spec[1], spec[2]
        coefficients = {
            full.CELLS[LOCAL_TO_FULL[bit]]: Q(1) for bit in retained_local
        }
        killed = old_class_killed(maximal, retained_local)
        cases.append(Case(
            f"old_{name}", coefficients, killed, ("t",),
        ))
    return cases


def audit_outside_killed_arbitrary(case):
    """Adding any non-retained cell leaves the projected data unchanged."""
    retained_bits = set(case.retained)
    for bit in range(9):
        if full.CELLS[bit] in case.coefficients:
            assert bit in retained_bits, (case.name, bit)
    if case.lam_bit is not None:
        assert case.lam_bit in retained_bits
    points = specialization_points(case.parameters)
    for bit in range(9):
        if bit in retained_bits:
            continue
        for point in points:
            blocks = blocks_at(case.coefficients, point, case.lam_bit)
            augmented_values = dict(case.coefficients)
            augmented_values[full.CELLS[bit]] = Q(1)
            augmented = blocks_at(augmented_values, point, case.lam_bit)
            base_maps = old_symbolic.coefficient_maps(
                equations.reconstruct_word_terms(blocks)
            )
            augmented_maps = old_symbolic.coefficient_maps(
                equations.reconstruct_word_terms(augmented)
            )
            assert {
                word: data for word, data in base_maps.items()
                if word not in case.killed
            } == {
                word: data for word, data in augmented_maps.items()
                if word not in case.killed
            }, (case.name, bit)
            for cut in range(6):
                assert equations.same_span(
                    full.projected_cylinder_columns(cut, augmented, case.killed),
                    full.projected_cylinder_columns(cut, blocks, case.killed),
                ), (case.name, bit, cut)


def audit_old_members(case, maximal_local, retained_local):
    members = [
        mask for mask in range(32)
        if old_locus.class_name(mask) == case.name[len("old_"):]
    ]
    points = specialization_points(case.parameters)
    for mask in members:
        assert mask & maximal_local == mask
        assert all(mask & (1 << bit) for bit in retained_local)
        member_values = {
            full.CELLS[LOCAL_TO_FULL[bit]]: Q(1)
            for bit in range(5) if mask & (1 << bit)
        }
        for point in points:
            blocks = blocks_at(case.coefficients, point)
            member_blocks = blocks_at(member_values, point)
            base_maps = old_symbolic.coefficient_maps(
                equations.reconstruct_word_terms(blocks)
            )
            member_maps = old_symbolic.coefficient_maps(
                equations.reconstruct_word_terms(member_blocks)
            )
            assert {
                word: data for word, data in base_maps.items()
                if word not in case.killed
            } == {
                word: data for word, data in member_maps.items()
                if word not in case.killed
            }, (case.name, mask)
            for cut in range(6):
                assert equations.same_span(
                    full.projected_cylinder_columns(
                        cut, member_blocks, case.killed
                    ),
                    full.projected_cylinder_columns(cut, blocks, case.killed),
                ), (case.name, mask, cut)
    return len(members)


def run_program(program, timeout=3600):
    singular = shutil.which("Singular")
    if singular is None:
        raise SystemExit("Singular is required")
    started = time.monotonic()
    completed = subprocess.run(
        [singular, "-q"], input=program, text=True, capture_output=True,
        check=True, timeout=timeout,
    )
    if completed.stderr.strip():
        raise AssertionError(completed.stderr)
    lines = [line.strip() for line in completed.stdout.splitlines() if line.strip()]
    unit = int(lines[lines.index("UNIT") + 1])
    size = int(lines[lines.index("GBSIZE") + 1])
    return unit, size, time.monotonic() - started


def discover_case(case):
    case.prepare()
    records = []
    for cut in CUTS:
        chosen = None
        for with_locks in (False, True):
            for active in case.admissible_pairs(cut):
                program, generators = case.system(cut, active, with_locks)
                unit, size, elapsed = run_program(program)
                if unit == 1 and size == 1:
                    chosen = {
                        "cut": cut, "active": active, "locks": with_locks,
                        "generators": generators,
                        "sha256": hashlib.sha256(program.encode()).hexdigest(),
                        "seconds": elapsed,
                        "normal_dim": len(case.normals[cut]),
                    }
                    break
            if chosen:
                break
        records.append(chosen or {"cut": cut, "FAILED": True})
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--direction", choices=("10", "20"), required=True)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--only", action="append")
    args = parser.parse_args()
    cell = DIRECTIONS[args.direction]
    select_direction(cell)
    audit_direction_geometry(cell)
    audit_coupled_stabilizer(cell)
    audit_literal_boundary_identity()
    old_full.audit_support_partition_and_torus()

    cases = outside_cases() + old_cases()
    if args.only:
        cases = [case for case in cases if case.name in set(args.only)]
    started = time.monotonic()
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        results = list(executor.map(discover_case, cases))
    for case, records in zip(cases, results):
        for record in records:
            print("CASE", case.name, record, flush=True)
    print(f"total wall time {time.monotonic() - started:.1f}s")


if __name__ == "__main__":
    main()
