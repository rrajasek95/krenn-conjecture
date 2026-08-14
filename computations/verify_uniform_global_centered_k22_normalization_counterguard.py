#!/usr/bin/env python3
"""Global centered-K2,2 normalization boundary.

For each complete-row component let B be its companion incidence and T its
three pure-target coefficient map.  The normalized affine equations are

    T^t p + B^t z = 0,                 p = (1,1,1).

On a flat K2,2 the unique transported charge is lambda=(1,1,-1,-1).
The affine equations are soluble exactly when (T lambda).p=0.  In
particular, coordinatewise centeredness T lambda=0 makes the three target
normalizations compatible; it cannot force an uncentered component.

The checker freezes two exact guards.  The smallest occurrence-typed guard
uses two K2,2 blocks, with shorewise colour words 01|01 and 20|20.  If every
component is required to have one monochromatic common core, the smallest
guard is the disjoint family of three blocks, one for each target colour.
Every companion is paired, every row has two companions, all holonomies are
even, and p_c=1,z_e=-1/2 kills all complete zero rows.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_recurrent_core_complete_row_projection_boundary.py":
        "3dc0ee0a0fbb7f0c1c1ea779bd6f3ee54114fece4f00a70877df8b2904cada2d",
    "notes/uniform-recurrent-core-complete-row-projection-boundary.md":
        "5305846b4377fba058725da7b40733522fed31d50ff78010e8b0763e24e80347",
    "computations/verify_uniform_balanced_chart_square_master_obstruction.py":
        "306980dc569795fa3ec2c8e6fdbdf2b67fa5d85cd75ebebe62be7db15b1e1a59",
    "notes/uniform-balanced-chart-square-master-obstruction.md":
        "c758fb43f88d9c02f5200921c6c50637bfe04402536edc3e947f74d108fbd93b",
}
EXPECTED_LEDGER_SHA256 = (
    "59eb45a3279282c5ddafbe2e8c5617c79d9f38f835eb1bfc0173a8ffcb47e42d"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def dot(left, right):
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def transpose(matrix):
    if not matrix:
        return []
    return [list(column) for column in zip(*matrix, strict=True)]


def matvec(matrix, vector):
    return tuple(dot(row, vector) for row in matrix)


def rref(matrix):
    rows = [[Q(entry) for entry in row] for row in matrix]
    if not rows:
        return rows, ()
    width = len(rows[0])
    require(all(len(row) == width for row in rows), "ragged matrix")
    pivots = []
    pivot_row = 0
    for column in range(width):
        pivot = next((row for row in range(pivot_row, len(rows))
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        value = rows[pivot_row][column]
        rows[pivot_row] = [entry / value for entry in rows[pivot_row]]
        for row in range(len(rows)):
            if row == pivot_row or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right for left, right in
                         zip(rows[row], rows[pivot_row], strict=True)]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return rows, tuple(pivots)


def rank(matrix):
    return len(rref(matrix)[1])


def nullspace(matrix):
    reduced, pivots = rref(matrix)
    width = len(matrix[0]) if matrix else 0
    free = tuple(column for column in range(width)
                 if column not in pivots)
    basis = []
    for free_column in free:
        vector = [Q(0)] * width
        vector[free_column] = Q(1)
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][free_column]
        basis.append(tuple(vector))
    return tuple(basis)


def same_line(left, right):
    require(len(left) == len(right), "line width")
    pivot = next((index for index, value in enumerate(right) if value), None)
    if pivot is None or not left[pivot]:
        return False
    scale = Q(left[pivot]) / Q(right[pivot])
    return all(Q(a) == scale * Q(b)
               for a, b in zip(left, right, strict=True))


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


K22_INCIDENCE = (
    (Q(1), Q(0), Q(1), Q(0)),  # z00 at A0,B0
    (Q(1), Q(0), Q(0), Q(1)),  # z01 at A0,B1
    (Q(0), Q(1), Q(1), Q(0)),  # z10 at A1,B0
    (Q(0), Q(1), Q(0), Q(1)),  # z11 at A1,B1
)
K22_CHARGE = (Q(1), Q(1), Q(-1), Q(-1))


def block_diagonal(blocks):
    total_width = sum(len(block[0]) for block in blocks)
    answer = []
    offset = 0
    for block in blocks:
        width = len(block[0])
        for row in block:
            answer.append([Q(0)] * offset + list(row)
                          + [Q(0)] * (total_width - offset - width))
        offset += width
    return answer


def target_map(colour_words):
    # T has target coordinates as rows and complete source rows as columns.
    return [[Q(int(colour == target))
             for word in colour_words for colour in word]
            for target in range(3)]


def embedded_charge(block, block_count):
    return ((Q(0),) * (4 * block) + K22_CHARGE
            + (Q(0),) * (4 * (block_count - block - 1)))


def audit_family(name, colour_words):
    require(all(len(word) == 4 for word in colour_words), "K2,2 word width")
    block_count = len(colour_words)
    companion = block_diagonal([K22_INCIDENCE] * block_count)
    targets = target_map(colour_words)
    charge_basis = tuple(embedded_charge(block, block_count)
                         for block in range(block_count))

    kernel = nullspace(companion)
    require(len(kernel) == block_count
            and all(any(same_line(vector, charge)
                        for vector in kernel)
                    for charge in charge_basis),
            (name, "global companion kernel changed"))
    transported = tuple(matvec(targets, charge)
                        for charge in charge_basis)
    require(transported == ((Q(0), Q(0), Q(0)),) * block_count,
            (name, "a component stopped being coordinatewise centered"))

    # The full complete-row matrix has basis P0,P1,P2 followed by every
    # companion coordinate.  Its only row-combination syzygies are the
    # centered component charges, and all have zero pure-target image.
    complete = targets + companion
    require(rank(complete) == rank(companion) == 3 * block_count,
            (name, "centered target rows changed complete-row rank"))

    # Exact normalized point: every row has one target occurrence of value
    # one and two incident companion occurrences of value -1/2.
    p = (Q(1), Q(1), Q(1))
    z = (Q(-1, 2),) * (4 * block_count)
    evaluation = p + z
    values = matvec(transpose(complete), evaluation)
    require(values == (Q(0),) * (4 * block_count),
            (name, "normalized exact point stopped killing all rows"))

    companion_degrees = tuple(sum(row) for row in companion)
    row_degrees = tuple(sum(companion[edge][vertex]
                            for edge in range(len(companion)))
                        for vertex in range(4 * block_count))
    require(companion_degrees == (Q(2),) * (4 * block_count)
            and row_degrees == (Q(2),) * (4 * block_count),
            (name, "boundary completeness changed"))
    support = sorted({colour for word in colour_words for colour in word})
    require(support == [0, 1, 2], (name, "not all targets participate"))

    return {
        "name": name,
        "block_colour_words_A0A1B0B1": [list(word)
                                          for word in colour_words],
        "block_count": block_count,
        "complete_zero_rows": 4 * block_count,
        "internal_paired_companions": 4 * block_count,
        "companion_rank": rank(companion),
        "complete_row_rank": rank(complete),
        "kernel_dimension": len(kernel),
        "transported_target_charges": [
            [str(entry) for entry in vector] for vector in transported
        ],
        "normalized_exact_point": {
            "P0=P1=P2": "1",
            "all_internal_companions": "-1/2",
            "all_complete_zero_rows": "0",
        },
        "companions_per_row": [int(value) for value in row_degrees],
        "rows_per_companion": [int(value) for value in companion_degrees],
        "component_holonomy": ["even"] * block_count,
        "outside_fan_companions": 0,
        "unit_ideal": False,
        "pure_target_projection_from_complete_zero_rows": False,
    }


def audit_minimality():
    # Each row is occurrence-typed by exactly one of the three targets.
    # Componentwise coordinate centering says the two colour multisets on
    # A0,A1 and B0,B1 agree.  One K2,2 can therefore use at most two target
    # colours; two blocks are both necessary and sufficient to use all three.
    least = None
    witnesses = 0
    for block_count in (1, 2):
        for flat in itertools.product(range(3), repeat=4 * block_count):
            words = tuple(tuple(flat[4 * block + index]
                                for index in range(4))
                          for block in range(block_count))
            if any(sorted(word[:2]) != sorted(word[2:]) for word in words):
                continue
            if set(flat) != {0, 1, 2}:
                continue
            if least is None:
                least = block_count
            if block_count == least:
                witnesses += 1
        if least is not None:
            break
    require(least == 2 and witnesses > 0,
            ("occurrence-typed minimum changed", least, witnesses))

    # Under the stronger recurrent-core typing, all four rows of a block
    # have the same target colour.  Covering three target rows then needs
    # exactly three components.
    monochromatic_minimum = next(
        blocks for blocks in range(1, 4)
        if any(set(words) == {0, 1, 2}
               for words in itertools.product(range(3), repeat=blocks))
    )
    require(monochromatic_minimum == 3,
            "monochromatic common-core minimum changed")
    return {
        "typing": (
            "one pure-target occurrence per complete row; every component "
            "is centered separately in each target coordinate"
        ),
        "minimum_K2,2_blocks_covering_three_targets": least,
        "labelled_minimizers": witnesses,
        "reason": (
            "a centered K2,2 has equal colour multisets on its two "
            "two-vertex shores, so one block uses at most two colours"
        ),
        "minimum_if_each_block_has_one_monochromatic_common_core":
            monochromatic_minimum,
    }


def audit_fredholm_boundary():
    # Test the exact scalar obstruction on every one-hot colour assignment
    # and every normalized pure target p in a small exact grid.  This is a
    # finite audit of the general identity lambda^t T^t p=(T lambda).p.
    checked = 0
    for word in itertools.product(range(3), repeat=4):
        targets = target_map((word,))
        transported = matvec(targets, K22_CHARGE)
        for p in itertools.product((Q(-1), Q(0), Q(1)), repeat=3):
            core_values = matvec(transpose(targets), p)
            left = dot(K22_CHARGE, core_values)
            right = dot(transported, p)
            require(left == right, "Fredholm pairing identity changed")
            # B^t z=-core_values is soluble iff its unique left-kernel
            # charge annihilates core_values.
            augmented = [list(row) + [-core_values[index]]
                         for index, row in
                         enumerate(transpose(K22_INCIDENCE))]
            soluble = rank(augmented) == rank(transpose(K22_INCIDENCE))
            require(soluble == (left == 0),
                    "Fredholm solvability criterion changed")
            checked += 1
    return {
        "identity": "lambda^t T^t p = (T lambda).p",
        "normalized_target": ["1", "1", "1"],
        "coordinatewise_centered_consequence": (
            "T lambda=0, so normalized target values are automatically "
            "compatible with the complete zero rows"
        ),
        "finite_exact_cases_checked": checked,
    }


def audit():
    pin_dependencies()
    require(rank(K22_INCIDENCE) == 3
            and len(nullspace(K22_INCIDENCE)) == 1
            and same_line(nullspace(K22_INCIDENCE)[0], K22_CHARGE),
            "base K2,2 incidence changed")

    two_block = audit_family(
        "smallest occurrence-typed global guard",
        ((0, 1, 0, 1), (2, 0, 2, 0)),
    )
    monochromatic = audit_family(
        "monochromatic common-core global guard",
        ((0, 0, 0, 0), (1, 1, 1, 1), (2, 2, 2, 2)),
    )
    ledger = {
        "theorem": "global centered K2,2 normalization counterguard",
        "pins": PINS,
        "fredholm_boundary": audit_fredholm_boundary(),
        "minimality": audit_minimality(),
        "smallest_occurrence_typed_guard": two_block,
        "monochromatic_common_core_guard": monochromatic,
        "verdict": (
            "a finite family of coordinatewise centered balanced K2,2 "
            "components is exactly compatible with P0=P1=P2=1; neither "
            "normalization nor a global signed sum forces an uncentered "
            "component, odd holonomy, unit, or active outside fan"
        ),
        "sharp_missing_hypothesis": (
            "a physical cross-component boundary must create a companion "
            "outside an internal block, or the exact transported target "
            "charge T lambda of some complete component must be nonzero "
            "and pair nontrivially with the normalized target vector"
        ),
        "scope": (
            "exact complete-row incidence counterguard, not a claimed full "
            "ternary decorated-hafnian source realization"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("global centered K2,2 family: NORMALIZATION-COMPATIBLE")
    print("Fredholm obstruction: (T lambda).p; centeredness makes it zero")
    print("smallest occurrence-typed guard: two K2,2 blocks")
    print("monochromatic common-core guard: three K2,2 blocks")
    print("all companions paired/internal; all holonomies even; no unit")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
