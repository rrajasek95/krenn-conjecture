#!/usr/bin/env python3
"""Construct the filtered marked lift on the h=3 common-tail branch.

In the 15-dimensional perfect-matching module, the ten physical
colour-diagonal tangent-Hasse cubes have cut-permanent top faces.  Their
centered differences span the common kernel of augmentation and the five
alternating K3,3 determinant coordinates.  A profile in that kernel has an
explicit source-valid filtered lift (top, lower)=(v,-v), preserving any
ordinary occurrence marker because that marker vanishes on collision grade.

This is a filtered lift.  Descent to an underived physical source map still
requires a Cartan--Spencer nullhomotopy of the lower collision face.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_tangent_euler_occurrence_splitter_fredholm.py":
        "ba2c32a41b1d070d2af24546819e838697aba0273e85586a796ee25a27f5a950",
    "computations/verify_frame_circuit_complete_source_kernel_lift_gate.py":
        "81738d71a423635da70caf7f3d46ca334cb0ebee7cd8240a0b7a7410c386f76c",
    "computations/verify_rectangular_interference_anchor_cartan_alternative.py":
        "b3d4db9e58f374bfd1f99a43931cac87fdab109c5d33c2f1c7d110e51e8f9a0a",
    "computations/verify_frame_circuit_matching_lift_trichotomy.py":
        "e0bdd386a63b17b67038ef8e8d0faf15ff041a1e8cb9f6f138e6a781233d44f1",
}
EXPECTED_LEDGER_SHA256 = "75ae40a75fc7419cd64f84e9c4e72b2243bec229658e82ea7087a6403a8275d6"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(relative, name):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def add(left, right):
    return tuple(Q(a) + Q(b) for a, b in zip(left, right, strict=True))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


def dot(left, right):
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def rank(vectors):
    if not vectors:
        return 0
    work = [list(map(Q, row)) for row in vectors]
    rows = len(work)
    columns = len(work[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next((row for row in range(pivot_row, rows)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def solve_columns(columns, target):
    """Solve sum coefficients[i]*columns[i]=target, or return None."""
    rows = len(target)
    variables = len(columns)
    work = [[Q(columns[column][row]) for column in range(variables)]
            + [Q(target[row])] for row in range(rows)]
    pivot_row = 0
    pivots = []
    for column in range(variables):
        pivot = next((row for row in range(pivot_row, rows)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivots.append(column)
        pivot_row += 1
    if any(not any(row[:variables]) and row[-1] for row in work):
        return None
    answer = [Q(0)] * variables
    for row, column in enumerate(pivots):
        answer[column] = work[row][-1]
    reconstructed = tuple(sum(answer[column] * columns[column][row]
                              for column in range(variables))
                          for row in range(rows))
    require(reconstructed == tuple(map(Q, target)),
            "cut-coordinate reconstruction failed")
    return tuple(answer)


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    tangent = load(
        "computations/verify_h3_tangent_euler_occurrence_splitter_fredholm.py",
        "filtered_common_tail_tangent")
    permanents = tuple(tangent.cut_permanent(cut) for cut in tangent.CUTS)
    determinants = tuple(tangent.cut_determinant(cut) for cut in tangent.CUTS)
    centered = tuple(add(permanent, scale(-1, permanents[0]))
                     for permanent in permanents[1:])
    augmentation = tuple(Q(1) for _ in tangent.MATCHINGS)

    # This is the exact Fredholm equality, not a finite-profile heuristic.
    # Five independent determinant rows plus augmentation impose rank six;
    # their kernel has dimension nine and contains the nine independent
    # centered cut packets.
    constraint_rows = (augmentation,) + determinants
    require(rank(determinants) == 5
            and rank(constraint_rows) == 6
            and rank(centered) == 9,
            "the 15=1+9+5 decomposition changed")
    require(all(dot(row, packet) == 0
                for row in constraint_rows for packet in centered),
            "a centered cut packet left the constrained kernel")
    require(len(tangent.MATCHINGS) - rank(constraint_rows) == len(centered),
            "the constrained kernel has an unaccounted direction")

    # Freeze coefficient-level constructivity throughout a nontrivial small
    # box.  Since the nine centered packets are independent, their displayed
    # coefficients are also the unique Hasse-cube-difference coefficients.
    coefficient_packets = 0
    marked_packets = 0
    marked_index = tangent.MATCHING_INDEX[tangent.BASE_MATCHING]
    profiles_seen = set()
    for coefficients in product((-1, 0, 1), repeat=len(centered)):
        profile = tuple(sum(Q(coefficient) * packet[index]
                            for coefficient, packet in
                            zip(coefficients, centered, strict=True))
                        for index in range(len(tangent.MATCHINGS)))
        require(all(dot(row, profile) == 0 for row in constraint_rows),
                "a generated filtered profile left the Fredholm kernel")
        profiles_seen.add(profile)
        coefficient_packets += 1
        marked_packets += bool(profile[marked_index])
    require(len(profiles_seen) == coefficient_packets,
            "the centered cut expansion stopped being unique")

    # An explicit complete contaminated profile with nonzero marked
    # coordinate.  It has eight ordinary occurrences rather than the bare
    # two-term frame pair.  Its complete tangent-Hasse lift is the difference
    # of two physical cubes: top=v and lower=-v.
    profile = centered[4]
    coordinates = solve_columns(centered, profile)
    top = profile
    lower = scale(-1, profile)
    total_boundary = add(top, lower)
    occurrence_marker = tuple(
        Q(int(index == marked_index)) for index in range(len(top)))
    filtered_marker = occurrence_marker + (Q(0),) * len(lower)
    filtered_cycle = top + lower
    collision_chain = (Q(0),) * len(top) + lower
    require(coordinates is not None and coordinates[4] == 1
            and sum(bool(value) for value in profile) == 8,
            "the explicit contaminated cut profile changed")
    require(top[marked_index] == 1 and not any(total_boundary),
            "the explicit filtered marked cycle stopped closing")
    require(dot(filtered_marker, filtered_cycle) == 1
            and not dot(filtered_marker, collision_chain),
            "the ordinary marker leaked into collision grade")
    require(all(dot(determinant, profile) == 0
                for determinant in determinants)
            and dot(augmentation, profile) == 0,
            "the positive profile acquired determinant/augmentation debt")

    # Bare common-tail differences never enter the positive sector.  This is
    # why contaminating complete-row terms are data rather than disposable
    # noise.  Classify by one shared edge (C4) or no shared edge (C6).
    pair_counts = Counter()
    reading_counts = Counter()
    for left_index, left_matching in enumerate(tangent.MATCHINGS):
        for right_index in range(left_index + 1, len(tangent.MATCHINGS)):
            right_matching = tangent.MATCHINGS[right_index]
            cycle_type = (
                "C4" if set(left_matching).intersection(right_matching)
                else "C6"
            )
            pair = tuple(Q(int(index == left_index)
                           - int(index == right_index))
                         for index in range(len(tangent.MATCHINGS)))
            readings = tuple(dot(determinant, pair)
                             for determinant in determinants)
            nonzero = sum(bool(value) for value in readings)
            require(nonzero == 6 and solve_columns(centered, pair) is None,
                    "a bare common-tail pair entered the tangent sector")
            pair_counts[cycle_type] += 1
            reading_counts[(cycle_type, nonzero)] += 1
    require(pair_counts == Counter({"C6": 60, "C4": 45}),
            "the six-site pair split changed")

    # Abstract determinant debt is not automatically a physical minor.  The
    # balanced 024|135 determinant reads two on a literal C4 difference, but
    # an all-ones evaluated cross-cut matrix makes both monomials nonzero and
    # its decorated determinant zero.
    guard_cut = (0, 2, 4)
    guard_determinant = tangent.cut_determinant(guard_cut)
    guard_pair_indices = (0, 2)
    guard_pair = tuple(Q(int(index == guard_pair_indices[0])
                         - int(index == guard_pair_indices[1]))
                       for index in range(len(tangent.MATCHINGS)))
    all_ones_matrix = tuple(tuple(Q(1) for _ in range(3)) for _ in range(3))
    occurrence_values = tangent.evaluated_cross_cut_occurrences(
        guard_cut, all_ones_matrix)
    require(dot(guard_determinant, guard_pair) == 2
            and occurrence_values[guard_pair_indices[0]] == 1
            and occurrence_values[guard_pair_indices[1]] == 1
            and tangent.determinant(all_ones_matrix) == 0
            and dot(guard_determinant, occurrence_values) == 0,
            "the abstract/evaluated common-tail determinant guard changed")

    ledger = {
        "pins": PINS,
        "matching_module": {
            "dimension": len(tangent.MATCHINGS),
            "augmentation_rank": 1,
            "determinant_rank": rank(determinants),
            "joint_constraint_rank": rank(constraint_rows),
            "centered_cut_rank": rank(centered),
        },
        "constructive_small_box": {
            "coefficient_profiles": coefficient_packets,
            "profiles_visible_at_base_occurrence": marked_packets,
            "coefficient_range": [-1, 0, 1],
            "unique_cut_expansion": True,
        },
        "explicit_filtered_marked_lift": {
            "word": "001122",
            "marked_matching": tangent.matching_text(tangent.BASE_MATCHING),
            "ordinary_support": sum(bool(value) for value in profile),
            "ordinary_profile": list(map(str, top)),
            "collision_profile": list(map(str, lower)),
            "total_boundary": 0,
            "ordinary_marked_value": str(top[marked_index]),
            "collision_marked_value": "0 (grade typing)",
            "cut_difference_coefficients": list(map(str, coordinates)),
        },
        "bare_pair_guard": {
            "C4_pairs": pair_counts["C4"],
            "C6_pairs": pair_counts["C6"],
            "nonzero_determinant_readings_per_pair": 6,
            "pair_in_centered_cut_sector": False,
        },
        "abstract_evaluated_guard": {
            "cut": list(guard_cut),
            "C4_pair": [
                tangent.matching_text(tangent.MATCHINGS[index])
                for index in guard_pair_indices
            ],
            "abstract_pair_reading": str(dot(
                guard_determinant, guard_pair)),
            "both_evaluated_monomials": ["1", "1"],
            "evaluated_decorated_minor": "0",
        },
        "filtered_entry_theorem": (
            "for the balanced h=3 word, a complete matching-occurrence "
            "profile v with zero augmentation and zero alternating K3,3 "
            "coordinates has a unique expansion in centered cut permanents. "
            "The corresponding difference of physical tangent-Hasse cubes "
            "is a filtered source cycle with top v and lower collision face "
            "-v.  Any ordinary occurrence marker vanishing on lower grade "
            "retains the value of v at that occurrence"
        ),
        "descent_interface": (
            "in the Hasse-filtered total source map this is already the "
            "marked kernel lift.  Descent to the underived physical source "
            "presentation is exactly a Cartan-Spencer nullhomotopy of the "
            "lower collision profile -v, with zero marked ordinary readout "
            "and compatible target/residue/terminal grades"
        ),
        "negative_branch": (
            "a nonzero abstract determinant coordinate obstructs this "
            "tangent correction but is not automatically a row-space pivot "
            "of the complete source map.  It is a physical Fitting carrier "
            "only when the same alternating covector evaluates to a nonzero "
            "decorated 3x3 minor.  Otherwise it remains a dual occurrence "
            "coordinate and another source correction may still remove it"
        ),
        "anchor_variance_guard": (
            "the ordinary occurrence marker e_mu^* is an auxiliary domain "
            "covector.  It need not equal the physical pure-anchor row in "
            "the rectangular augmentation.  If the full source lift gate "
            "returns e_mu^*=lambda^T M, it isolates a nonzero localized "
            "monomial and is a source pivot; on the kernel branch, nonzero "
            "e_mu^*(c) alone does not prove that the physical anchor sees c"
        ),
        "scope": (
            "exact h=3 balanced-word filtered theorem.  It does not "
            "construct the Cartan-Spencer nullhomotopy, identify an abstract "
            "determinant with a nonzero evaluated minor, or type the physical "
            "pure-anchor covector on the resulting kernel"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("filtered common-tail ledger changed", digest))
    return ledger, digest


def main():
    ledger, digest = audit()
    print("h3 filtered common-tail marked-kernel lift: PASS")
    print("matching split: 15=1+9+5")
    print("small coefficient profiles:",
          ledger["constructive_small_box"]["coefficient_profiles"])
    print("bare pairs: C4=45 C6=60; each has six determinant readings")
    print("remaining: Cartan-Spencer nullhomotopy of lower collision face")
    print("ledger_sha256", digest)


if __name__ == "__main__":
    main()
