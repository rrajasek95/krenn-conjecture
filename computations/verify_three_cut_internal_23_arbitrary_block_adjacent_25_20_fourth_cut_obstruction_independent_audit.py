#!/usr/bin/env python3
"""Clean-room exact audit of the coupled adjacent E20 fourth-cut obstruction.

Audited family: the fixed six-site interior

    01:E00  45:E00  02:E11  14:E11  04:E22  13:E22  35:E10,

with A23 = X an arbitrary complex 3x3 block and A25 = E00 + t*E20, both
boundary stars and A67 arbitrary.  The claim is that no complex (X, t,
stars, A67) admits a fourth complete cut z in {0,1,5} beside cuts 2,3,4.

This checker imports no project module and consumes no matrix, killed
set, normal, program string, or hash from the primary implementation.
Everything is rebuilt from the definitions with different algorithmic
choices: perfect matchings by a smallest-vertex recursion with mates
scanned downward, reverse-lexicographic word and column orders,
greatest-coordinate sparse Gauss-Jordan elimination and double
annihilators for all spans and intersections, a reversed Singular ring
variable and generator order, and `std` instead of `slimgb`.  Only the
frozen per-case configuration (colour pair, lock usage, expected
expanded-overspace dimensions) is read from the primary's table, as the
audit brief allows.

The coupled point of this direction: wt(t) = wt(x20) - wt(x00) on the
fixed-cell stabilizer torus, so t cannot be normalized independently of
X and is kept as an ordinary polynomial variable in every certificate.
Each case projects the word space by its own freshly computed killed
set, expands every cylinder over the parameter unit points, intersects
the four expanded cylinders into the overspace N+_z, and requires the
four-fibre shared-star packet ideal (plus exact lock rows on the
x12+x21=x11+x22 circuit chart) to be the unit ideal over Q[t(,lam)].

Run from the repository root:

    uv run python computations/verify_three_cut_internal_23_arbitrary_block_adjacent_25_20_fourth_cut_obstruction_independent_audit.py --workers 8
"""

from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from fractions import Fraction
from functools import lru_cache
from itertools import combinations

Q = Fraction
COLOURS = (0, 1, 2)
SIX = tuple(range(6))
EIGHT = tuple(range(8))
CELLS = tuple((a, b) for a in COLOURS for b in COLOURS)
CELL_BIT = {cell: index for index, cell in enumerate(CELLS)}
DIRECTION = (2, 0)
FIXED_SOURCES = (
    (0, 1, 0, 0),
    (4, 5, 0, 0),
    (0, 2, 1, 1),
    (1, 4, 1, 1),
    (0, 4, 2, 2),
    (1, 3, 2, 2),
    (3, 5, 1, 0),
    (2, 5, 0, 0),
)
MOVING_SOURCE = (2, 5) + DIRECTION
BASE_CUTS = (2, 3, 4)
FINAL_CUTS = (0, 1, 5)
OUTSIDE_ORDER = ((1, 0), (1, 2), (2, 0), (2, 2))
FIVE_LOCUS = ((0, 0), (0, 1), (0, 2), (1, 1), (2, 1))

# Frozen configuration read from the primary verifier, as the audit brief
# permits: per case and final cut, the active colour pair, whether lock
# rows are used, and the expected expanded-overspace dimension.  No
# generator count and no hash is reproduced from the primary.
CONFIG = {}
for _name in ("old_no_x00",):
    CONFIG[_name] = {"pair": (0, 2), "locks": False, "dims": {0: 1, 1: 1, 5: 1}}
CONFIG["old_x00_no_x11_no_x21"] = {"pair": (1, 2), "locks": False, "dims": {0: 1, 1: 1, 5: 1}}
CONFIG["old_x00_no_x11_with_x21"] = {"pair": (1, 2), "locks": False, "dims": {0: 2, 1: 2, 5: 2}}
CONFIG["old_x00_x11_no_x21"] = {"pair": (1, 2), "locks": False, "dims": {0: 3, 1: 3, 5: 3}}
CONFIG["old_x00_x11_with_x21"] = {"pair": (1, 2), "locks": False, "dims": {0: 3, 1: 3, 5: 3}}
for _d in (0, 2, 4, 6):
    for _b in (0, 1):
        CONFIG[f"outside_x10_d{_d}_b{_b}"] = {
            "pair": (1, 2), "locks": False, "dims": {0: 3, 1: 3, 5: 3}}
        CONFIG[f"outside_x20_d{_d}_b{_b}"] = {
            "pair": (1, 2), "locks": False, "dims": {0: 3, 1: 3, 5: 3}}
for _d, _b in ((0, 0), (0, 1), (2, 0), (2, 1), (4, 0), (4, 1), (6, 0)):
    CONFIG[f"outside_x12_d{_d}_b{_b}"] = {
        "pair": (1, 2), "locks": False, "dims": {0: 2, 1: 2, 5: 2}}
CONFIG["outside_x12_crossratio"] = {
    "pair": (1, 2), "locks": True, "dims": {0: 3, 1: 3, 5: 5}}
for _d in (4, 6):
    for _b in (0, 1):
        CONFIG[f"outside_x22_d{_d}_b{_b}"] = {
            "pair": (1, 2), "locks": False, "dims": {0: 3, 1: 3, 5: 2}}
assert len(CONFIG) == 33

# Frozen after the first fully successful independent replay; guards this
# audit's own differently ordered program ledger against drift.
EXPECTED_PROGRAM_LEDGER_SHA256 = ""

# ---------------------------------------------------------------------------
# Matchings, tensors, columns, atoms


@lru_cache(maxsize=None)
def perfect_matchings(vertices):
    """Pair the smallest remaining vertex; mates are scanned downward."""
    if not vertices:
        return ((),)
    first = vertices[0]
    rest = vertices[1:]
    answer = []
    for position in range(len(rest) - 1, -1, -1):
        mate = rest[position]
        remainder = rest[:position] + rest[position + 1:]
        for tail in perfect_matchings(remainder):
            answer.append(((first, mate),) + tail)
    return tuple(answer)


def internal_blocks(x_values, t_value):
    """Blocks on the six internal sites; x_values maps cells to weights."""
    blocks = {}
    for left, right, left_colour, right_colour in FIXED_SOURCES:
        blocks.setdefault((left, right), {})[(left_colour, right_colour)] = Q(1)
    if t_value:
        blocks[(2, 5)][DIRECTION] = t_value
    for cell, value in x_values.items():
        if value:
            blocks.setdefault((2, 3), {})[cell] = value
    return blocks


def matching_tensor(vertices, blocks):
    position = {site: index for index, site in enumerate(vertices)}
    answer = {}
    for matching in perfect_matchings(tuple(vertices)):
        options = []
        for left, right in matching:
            cells = blocks.get((left, right))
            if not cells:
                break
            options.append(((left, right), tuple(cells.items())))
        else:
            stack = [((), Q(1))]
            for (left, right), cells in options:
                stack = [
                    (partial + ((left, left_colour), (right, right_colour)),
                     weight * value)
                    for partial, weight in stack
                    for (left_colour, right_colour), value in cells
                ]
            for assignment, weight in stack:
                word = [None] * len(vertices)
                for site, colour in assignment:
                    word[position[site]] = colour
                key = tuple(word)
                total = answer.get(key, 0) + weight
                if total:
                    answer[key] = total
                else:
                    answer.pop(key, None)
    return answer


def raw_columns(cut, blocks):
    """45 insertion columns; holes, cut colours, hole colours descending."""
    others = tuple(site for site in SIX if site != cut)
    columns = []
    labels = []
    for hole in reversed(others):
        rest = tuple(site for site in others if site != hole)
        cofactor = matching_tensor(rest, blocks)
        for cut_colour in (2, 1, 0):
            for hole_colour in (2, 1, 0):
                vector = {}
                for rest_word, value in cofactor.items():
                    assignment = dict(zip(rest, rest_word))
                    assignment[hole] = hole_colour
                    assignment[cut] = cut_colour
                    vector[tuple(assignment[site] for site in SIX)] = value
                columns.append(vector)
                labels.append((hole, cut_colour, hole_colour))
    assert len(columns) == 45
    return tuple(columns), tuple(labels)


def pair_atoms(blocks):
    """Deleted-pair cofactor atoms grouped by six-site word.

    atoms[word][(i, ci, j, cj)] with i < j is the cofactor coefficient of
    the word obtained from the {i,j}-deleted four-site tensor extended by
    colour ci at i and cj at j.  Pairs and colours are scanned downward.
    """
    grouped = {}
    for j in range(5, 0, -1):
        for i in range(j - 1, -1, -1):
            rest = tuple(site for site in SIX if site not in (i, j))
            cofactor = matching_tensor(rest, blocks)
            for rest_word, value in cofactor.items():
                base = dict(zip(rest, rest_word))
                for ci in (2, 1, 0):
                    for cj in (2, 1, 0):
                        assignment = dict(base)
                        assignment[i] = ci
                        assignment[j] = cj
                        word = tuple(assignment[site] for site in SIX)
                        slot = grouped.setdefault(word, {})
                        key = (i, ci, j, cj)
                        total = slot.get(key, 0) + value
                        if total:
                            slot[key] = total
                        else:
                            slot.pop(key, None)
    return {word: slot for word, slot in grouped.items() if slot}


# ---------------------------------------------------------------------------
# Sparse exact linear algebra, greatest coordinate first


def rref(rows, coords=None):
    work = [dict(row) for row in rows if row]
    if coords is None:
        keys = set()
        for row in work:
            keys.update(row)
        coords = sorted(keys, reverse=True)
    basis = []
    pivots = []
    for coord in coords:
        found = None
        for index, row in enumerate(work):
            if row.get(coord):
                found = index
                break
        if found is None:
            continue
        pivot_row = work.pop(found)
        inverse = 1 / pivot_row[coord]
        pivot_row = {key: value * inverse for key, value in pivot_row.items()}
        for row in work:
            factor = row.get(coord)
            if factor:
                for key, value in pivot_row.items():
                    updated = row.get(key, 0) - factor * value
                    if updated:
                        row[key] = updated
                    else:
                        row.pop(key, None)
        for other in basis:
            factor = other.get(coord)
            if factor:
                for key, value in pivot_row.items():
                    updated = other.get(key, 0) - factor * value
                    if updated:
                        other[key] = updated
                    else:
                        other.pop(key, None)
        basis.append(pivot_row)
        pivots.append(coord)
        work = [row for row in work if row]
        if not work:
            break
    assert not work
    return tuple(basis), tuple(pivots)


def annihilator(rows, coords):
    basis, pivots = rref(rows, coords)
    pivot_set = set(pivots)
    functionals = []
    for free in coords:
        if free in pivot_set:
            continue
        functional = {free: Q(1)}
        for row, pivot in zip(basis, pivots):
            value = row.get(free)
            if value:
                functional[pivot] = -value
        functionals.append(functional)
    return tuple(functionals)


def dot(functional, vector):
    if len(functional) > len(vector):
        functional, vector = vector, functional
    return sum(value * vector.get(key, 0) for key, value in functional.items())


def reduce_vector(vector, basis, pivots):
    remainder = dict(vector)
    for row, pivot in zip(basis, pivots):
        factor = remainder.get(pivot)
        if factor:
            for key, value in row.items():
                updated = remainder.get(key, 0) - factor * value
                if updated:
                    remainder[key] = updated
                else:
                    remainder.pop(key, None)
    return remainder


def in_span(vector, basis, pivots):
    return not reduce_vector(vector, basis, pivots)


def intersect_pair(left, right):
    coords = sorted(
        {key for row in left for key in row}
        | {key for row in right for key in row},
        reverse=True,
    )
    dual = list(annihilator(left, coords)) + list(annihilator(right, coords))
    return rref(annihilator(rref(dual, coords)[0], coords), coords)[0]


def intersect_many(spaces):
    result = rref(spaces[0])[0]
    for space in spaces[1:]:
        if not result:
            return ()
        result = intersect_pair(result, rref(space)[0])
    return result


# ---------------------------------------------------------------------------
# Joint affine model in (X, t) and the coordinate geometry

WORD_KEY = "H"


def evaluate_system(x_values, t_value):
    """Six-site tensor plus all deleted-pair atoms at one (X, t) point."""
    blocks = internal_blocks(x_values, t_value)
    tensor = matching_tensor(SIX, blocks)
    atoms = pair_atoms(blocks)
    flat = {}
    for word, value in tensor.items():
        flat[(word, WORD_KEY)] = value
    for word, slot in atoms.items():
        for key, value in slot.items():
            flat[(word, key)] = value
    return flat


def build_linear_model():
    """Exact coefficients of 1, x_ab, t for every tensor and atom entry.

    Every perfect matching uses the variable edge 23 at most once and,
    since 23 and 25 share site 2, never together with the moving cell of
    25; each matching weight is therefore jointly affine-linear in the
    nine x_ab and t with no products.  The model below is consequently
    exact, and it is verified against dense rational probes.
    """
    base = evaluate_system({}, Q(0))
    per_cell = {
        cell: evaluate_system({cell: Q(1)}, Q(0)) for cell in CELLS
    }
    with_t = evaluate_system({}, Q(1))
    keys = set(base) | set(with_t)
    for flat in per_cell.values():
        keys |= set(flat)
    model = {}
    for key in keys:
        constant = base.get(key, Q(0))
        cell_part = {}
        for cell in CELLS:
            value = per_cell[cell].get(key, Q(0)) - constant
            if value:
                cell_part[cell] = value
        t_part = with_t.get(key, Q(0)) - constant
        model[key] = (constant, cell_part, t_part)
    return model


def model_prediction(model, x_values, t_value):
    prediction = {}
    for key, (constant, cell_part, t_part) in model.items():
        value = constant + t_part * t_value
        for cell, coefficient in cell_part.items():
            value += coefficient * x_values.get(cell, 0)
        if value:
            prediction[key] = value
    return prediction


def audit_affine_model(model):
    dense = {cell: Q(3 + 2 * index, 5 + index) for index, cell in enumerate(CELLS)}
    for t_value in (Q(0), Q(1), Q(17, 5), Q(-4, 3)):
        assert evaluate_system(dense, t_value) == model_prediction(
            model, dense, t_value
        )
    sparse = {(1, 0): Q(7, 2), (2, 2): Q(-5, 3)}
    assert evaluate_system(sparse, Q(9, 4)) == model_prediction(
        model, sparse, Q(9, 4)
    )
    # Mixed second differences: cell versus t, in tensors, atoms, columns.
    for cell in CELLS:
        for flavour in (
            evaluate_system,
            lambda xv, tv: {
                (cut, index, word): value
                for cut in SIX
                for index, column in enumerate(
                    raw_columns(cut, internal_blocks(xv, tv))[0]
                )
                for word, value in column.items()
            },
        ):
            f11 = flavour({cell: Q(1)}, Q(1))
            f10 = flavour({cell: Q(1)}, Q(0))
            f01 = flavour({}, Q(1))
            f00 = flavour({}, Q(0))
            keys = set(f11) | set(f10) | set(f01) | set(f00)
            for key in keys:
                mixed = (
                    f11.get(key, 0) - f10.get(key, 0)
                    - f01.get(key, 0) + f00.get(key, 0)
                )
                assert mixed == 0, (cell, key)
    # Second difference in t on a dense X.
    e0 = evaluate_system(dense, Q(0))
    e1 = evaluate_system(dense, Q(1))
    e2 = evaluate_system(dense, Q(2))
    for key in set(e0) | set(e1) | set(e2):
        assert e2.get(key, 0) - 2 * e1.get(key, 0) + e0.get(key, 0) == 0


def audit_geometry(model):
    """Output blocks, moving block, fixed support, and their interplay."""
    blocks_of = {cell: set() for cell in CELLS}
    t_block = set()
    t_pairs = set()
    for (word, key), (_constant, cell_part, t_part) in model.items():
        for cell in cell_part:
            blocks_of[cell].add(word)
        if t_part:
            t_block.add(word)
            if key != WORD_KEY:
                t_pairs.add((key[0], key[2]))
    fixed_support = set(matching_tensor(SIX, internal_blocks({}, Q(0))))

    for cell in CELLS:
        assert len(blocks_of[cell]) == 35, cell
    for left, right in combinations(CELLS, 2):
        assert not blocks_of[left] & blocks_of[right]
    union = set().union(*blocks_of.values())
    assert len(union) == 315
    assert len(t_block) == 35
    overlaps = tuple(len(t_block & blocks_of[cell]) for cell in CELLS)
    assert overlaps == (0, 0, 0, 0, 0, 0, 9, 9, 12), overlaps
    assert t_pairs == {(0, 3), (0, 4), (1, 3), (3, 4)}
    assert fixed_support == {
        (1, 2, 1, 2, 0, 0), (1, 1, 1, 1, 1, 0), (2, 2, 0, 2, 2, 0)
    }
    assert not t_block & fixed_support
    for colour in COLOURS:
        target = (colour,) * 6
        assert target not in t_block
        assert target in blocks_of[(colour, colour)]
        for cell in CELLS:
            if cell != (colour, colour):
                assert target not in blocks_of[cell]
    # The moving cell's own tensor word.
    t_words = {
        word for (word, key), (_c, _cp, tp) in model.items()
        if key == WORD_KEY and tp
    }
    assert t_words == {(2, 2, 2, 2, 2, 0)}
    return blocks_of, t_block, fixed_support


# ---------------------------------------------------------------------------
# Stabilizer torus and coupled characters


def integer_rank(rows):
    sparse = [
        {index: Q(value) for index, value in enumerate(row) if value}
        for row in rows
    ]
    return len(rref(sparse, tuple(range(len(rows[0]) - 1, -1, -1)))[0])


def character_data():
    def exponent_row(source):
        left, right, left_colour, right_colour = source
        row = [0] * 18
        row[3 * left + left_colour] += 1
        row[3 * right + right_colour] += 1
        return tuple(row)

    fixed_rows = [exponent_row(source) for source in FIXED_SOURCES]
    assert integer_rank(fixed_rows) == 8
    sparse = [
        {index: Q(value) for index, value in enumerate(row) if value}
        for row in fixed_rows
    ]
    kernel = annihilator(sparse, tuple(range(17, -1, -1)))
    assert len(kernel) == 10

    def character(source):
        row = exponent_row(source)
        return tuple(
            sum(vector.get(index, 0) * row[index] for index in range(18))
            for vector in kernel
        )

    x_chars = {cell: character((2, 3) + cell) for cell in CELLS}
    t_char = character(MOVING_SOURCE)
    return x_chars, t_char


def vector_rank(vectors):
    sparse = [
        {index: Q(value) for index, value in enumerate(vector) if value}
        for vector in vectors
    ]
    width = max((len(vector) for vector in vectors), default=0)
    return len(rref(sparse, tuple(range(width - 1, -1, -1)))[0])


def audit_coupled_character(x_chars, t_char):
    rows = [x_chars[cell] for cell in CELLS]
    assert vector_rank(rows) == 5
    difference = tuple(
        t - (a - b)
        for t, a, b in zip(t_char, x_chars[(2, 0)], x_chars[(0, 0)])
    )
    assert not any(difference), "wt(t) != wt(x20) - wt(x00)"
    assert vector_rank(rows + [t_char]) == 5
    circuit = tuple(
        p + q - r - s
        for p, q, r, s in zip(
            x_chars[(1, 1)], x_chars[(2, 2)], x_chars[(1, 2)], x_chars[(2, 1)]
        )
    )
    assert not any(circuit)


# ---------------------------------------------------------------------------
# Case partition of the 512 supports

OLD_SPECS = (
    # name, class-defining nonzero cells, maximal-member cells M, kept P,
    # free member cells
    ("old_no_x00", (), ((0, 1), (0, 2), (1, 1), (2, 1)), (),
     ((0, 1), (0, 2), (1, 1), (2, 1))),
    ("old_x00_no_x11_no_x21", ((0, 0),), ((0, 0), (0, 1), (0, 2)), (),
     ((0, 1), (0, 2))),
    ("old_x00_no_x11_with_x21", ((0, 0), (2, 1)),
     ((0, 0), (0, 1), (0, 2), (2, 1)), ((0, 0), (2, 1)), ((0, 1), (0, 2))),
    ("old_x00_x11_no_x21", ((0, 0), (1, 1)),
     ((0, 0), (0, 1), (0, 2), (1, 1)), ((0, 0), (1, 1)), ((0, 1), (0, 2))),
    ("old_x00_x11_with_x21", ((0, 0), (1, 1), (2, 1)), FIVE_LOCUS,
     ((0, 0), (1, 1), (2, 1)), ((0, 1), (0, 2))),
)

FAMILY_SPECS = {
    # family -> (pivot, retained blocks, free member cells)
    "x10": ((1, 0), ((1, 0), (1, 1), (2, 1), (2, 2)),
            ((0, 0), (0, 1), (0, 2), (1, 2), (2, 0))),
    "x12": ((1, 2), ((1, 1), (1, 2), (2, 1), (2, 2)),
            ((0, 0), (0, 1), (0, 2), (2, 0))),
    "x20": ((2, 0), ((1, 0), (1, 1), (2, 0), (2, 1), (2, 2)),
            ((0, 0), (0, 1), (0, 2))),
    "x22": ((2, 2), ((1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)),
            ((0, 0), (0, 1), (0, 2))),
}

OLD_KILLED_SIZES = {
    "old_no_x00": 141,
    "old_x00_no_x11_no_x21": 107,
    "old_x00_no_x11_with_x21": 72,
    "old_x00_x11_no_x21": 71,
    "old_x00_x11_with_x21": 71,
}
FAMILY_KILLED_SIZES = {"x10": 175, "x12": 175, "x20": 140, "x22": 105}


def case_of_mask(mask):
    present = {CELLS[bit] for bit in range(9) if mask >> bit & 1}
    pivot = next((cell for cell in OUTSIDE_ORDER if cell in present), None)
    if pivot is None:
        if (0, 0) not in present:
            return "old_no_x00"
        if (1, 1) in present:
            return ("old_x00_x11_with_x21" if (2, 1) in present
                    else "old_x00_x11_no_x21")
        return ("old_x00_no_x11_with_x21" if (2, 1) in present
                else "old_x00_no_x11_no_x21")
    family = f"x{pivot[0]}{pivot[1]}"
    pattern = 2 if (1, 1) in present else 0
    if pivot == (2, 2):
        pattern |= 4
    elif (2, 2) in present:
        pattern |= 4
    binary = 1 if (2, 1) in present else 0
    if family == "x12" and pattern == 6 and binary == 1:
        return "outside_x12_crossratio"
    return f"outside_{family}_d{pattern}_b{binary}"


class Case:
    def __init__(self, name, kind, pair, locks, dims, present, killed_cells,
                 kept_blocks, arbitrary_cells, member_masks, two_params):
        self.name = name
        self.kind = kind
        self.pair = pair
        self.locks = locks
        self.dims = dims
        self.present = present
        self.killed_cells = killed_cells
        self.kept_blocks = kept_blocks
        self.arbitrary_cells = arbitrary_cells
        self.member_masks = member_masks
        self.two_params = two_params
        self.killed_words = None
        self.thetas = (
            ((Q(0), Q(0)), (Q(1), Q(0)), (Q(0), Q(1)))
            if two_params else ((Q(0), Q(0)), (Q(1), Q(0)))
        )

    def x_values(self, theta, extra=()):
        t_value, lam_value = theta
        values = {cell: Q(1) for cell in self.present}
        if self.name == "outside_x12_crossratio":
            if lam_value:
                values[(2, 1)] = lam_value
            else:
                values.pop((2, 1), None)
        for cell in extra:
            values[cell] = Q(1)
        return values, t_value


def mask_of_cells(cells):
    mask = 0
    for cell in cells:
        mask |= 1 << CELL_BIT[cell]
    return mask


def build_cases():
    cases = []
    for name, nonzero, maximal, kept, free in OLD_SPECS:
        killed_cells = tuple(cell for cell in maximal if cell not in kept)
        members = []
        for r in range(len(free) + 1):
            for subset in combinations(free, r):
                members.append(mask_of_cells(nonzero + subset))
        cases.append(Case(
            name, "old", CONFIG[name]["pair"], CONFIG[name]["locks"],
            CONFIG[name]["dims"], tuple(nonzero), killed_cells, tuple(kept),
            (), tuple(members), False,
        ))
    for family, (pivot, retained, free) in FAMILY_SPECS.items():
        killed_cells = tuple(cell for cell in CELLS if cell not in retained)
        d_values = (4, 6) if family == "x22" else (0, 2, 4, 6)
        for d in d_values:
            for b in (0, 1):
                present = [pivot]
                if d & 2:
                    present.append((1, 1))
                if family != "x22" and d & 4:
                    present.append((2, 2))
                if b:
                    present.append((2, 1))
                crossratio = family == "x12" and d == 6 and b == 1
                name = ("outside_x12_crossratio" if crossratio
                        else f"outside_{family}_d{d}_b{b}")
                if crossratio:
                    present = [(1, 1), (1, 2), (2, 2), (2, 1)]
                members = []
                base_cells = tuple(present) if not crossratio else (
                    (1, 1), (1, 2), (2, 2), (2, 1))
                for r in range(len(free) + 1):
                    for subset in combinations(free, r):
                        members.append(mask_of_cells(base_cells + subset))
                cases.append(Case(
                    name, "outside", CONFIG[name]["pair"],
                    CONFIG[name]["locks"], CONFIG[name]["dims"],
                    tuple(present) if not crossratio
                    else ((1, 1), (1, 2), (2, 2)),
                    killed_cells, tuple(retained), killed_cells,
                    tuple(members), crossratio,
                ))
    assert len(cases) == 33
    assert {case.name for case in cases} == set(CONFIG)
    return cases


def audit_census(cases, x_chars, t_char):
    census = {}
    for mask in range(1 << 9):
        census.setdefault(case_of_mask(mask), set()).add(mask)
    assert set(census) == set(CONFIG)
    assert sum(len(masks) for masks in census.values()) == 512
    old_total = sum(
        len(masks) for name, masks in census.items() if name.startswith("old_")
    )
    assert old_total == 32
    family_totals = {"x10": 0, "x12": 0, "x20": 0, "x22": 0}
    for name, masks in census.items():
        if name.startswith("outside_"):
            family = "x12" if name == "outside_x12_crossratio" else name.split("_")[1]
            family_totals[family] += len(masks)
    assert family_totals == {"x10": 256, "x12": 128, "x20": 64, "x22": 32}
    for case in cases:
        assert census[case.name] == set(case.member_masks), case.name
    # The two coupled x00-open supports called out by the theorem note.
    assert case_of_mask(mask_of_cells(((0, 0), (2, 0), (2, 1)))) == \
        "outside_x20_d0_b1"
    assert case_of_mask(mask_of_cells(
        ((0, 0), (0, 2), (1, 1), (2, 0), (2, 2)))) == "outside_x20_d6_b0"
    # Per-case torus normalizability of the representative cells.
    for case in cases:
        rows = [x_chars[cell] for cell in sorted(case.present)]
        if case.name == "outside_x12_crossratio":
            rows = [x_chars[cell] for cell in
                    ((1, 1), (1, 2), (2, 1), (2, 2))]
            assert vector_rank(rows) == 3
        else:
            assert vector_rank(rows) == len(rows), case.name
    counts = {name: len(masks) for name, masks in census.items()}
    return counts


# ---------------------------------------------------------------------------
# Killed word sets and projections


def killed_words_for(case, blocks_of, t_block):
    killed = set()
    for cell in case.killed_cells:
        killed |= blocks_of[cell]
    if case.kind == "old":
        spared = set(t_block)
        for cell in case.kept_blocks:
            spared |= blocks_of[cell]
    else:
        spared = set(t_block)
        for cell in case.kept_blocks:
            spared |= blocks_of[cell]
    fixed_support = {(1, 2, 1, 2, 0, 0), (1, 1, 1, 1, 1, 0), (2, 2, 0, 2, 2, 0)}
    killed |= {word for word in fixed_support if word not in spared}
    return frozenset(killed)


def project(vector, killed):
    return {word: value for word, value in vector.items() if word not in killed}


def project_atoms(atoms, killed):
    return {
        word: slot for word, slot in atoms.items() if word not in killed
    }


# ---------------------------------------------------------------------------
# Per-case data


class CaseData:
    """Projected tensors, atoms, columns, overspaces for one case."""

    def __init__(self, case, blocks_of, t_block):
        self.case = case
        case.killed_words = killed_words_for(case, blocks_of, t_block)
        expected = (OLD_KILLED_SIZES[case.name] if case.kind == "old"
                    else FAMILY_KILLED_SIZES[self.family_of(case)])
        assert len(case.killed_words) == expected, (case.name, len(case.killed_words))
        self.tensors = {}
        self.atoms = {}
        self.columns = {}
        for theta in case.thetas:
            x_values, t_value = case.x_values(theta)
            blocks = internal_blocks(x_values, t_value)
            self.tensors[theta] = project(
                matching_tensor(SIX, blocks), case.killed_words)
            self.atoms[theta] = project_atoms(
                pair_atoms(blocks), case.killed_words)
            for cut in SIX:
                columns, labels = raw_columns(cut, blocks)
                self.columns[theta, cut] = tuple(
                    project(column, case.killed_words) for column in columns
                )
        self.spans = {}
        for cut in SIX:
            vectors = [
                column
                for theta in case.thetas
                for column in self.columns[theta, cut]
                if column
            ]
            self.spans[cut] = rref(vectors)[0]
        self.base = intersect_many([
            self.spans[2], self.spans[3], self.spans[4]
        ])
        self.overspaces = {}
        for cut in FINAL_CUTS:
            self.overspaces[cut] = intersect_pair(
                self.base, self.spans[cut]) if self.base else ()

    @staticmethod
    def family_of(case):
        if case.name == "outside_x12_crossratio":
            return "x12"
        return case.name.split("_")[1]

    def atom_triples(self):
        """word -> atom key -> (c0, ct, clam), dropping zero triples."""
        thetas = self.case.thetas
        zero = thetas[0]
        result = {}
        words = set()
        for theta in thetas:
            words |= set(self.atoms[theta])
        for word in words:
            slot0 = self.atoms[zero].get(word, {})
            slot_t = self.atoms[thetas[1]].get(word, {})
            slot_l = self.atoms[thetas[2]].get(word, {}) if len(thetas) > 2 else {}
            keys = set(slot0) | set(slot_t) | set(slot_l)
            merged = {}
            for key in keys:
                c0 = slot0.get(key, Q(0))
                ct = slot_t.get(key, Q(0)) - c0
                cl = slot_l.get(key, Q(0)) - c0 if len(thetas) > 2 else Q(0)
                if c0 or ct or cl:
                    merged[key] = (c0, ct, cl)
            if merged:
                result[word] = merged
        return result

    def column_triples(self, cut):
        thetas = self.case.thetas
        triples = []
        for index in range(45):
            c0 = self.columns[thetas[0], cut][index]
            ct = subtract(self.columns[thetas[1], cut][index], c0)
            cl = (subtract(self.columns[thetas[2], cut][index], c0)
                  if len(thetas) > 2 else {})
            triples.append((c0, ct, cl))
        return triples


def subtract(left, right):
    result = dict(left)
    for key, value in right.items():
        updated = result.get(key, 0) - value
        if updated:
            result[key] = updated
        else:
            result.pop(key, None)
    return result


def audit_case_affine_probe(case, data):
    """Exact probe of joint (t, lam) affineness of atoms and columns."""
    probe = (Q(7, 3), Q(5, 2)) if case.two_params else (Q(7, 3), Q(0))
    x_values, t_value = case.x_values(probe)
    blocks = internal_blocks(x_values, t_value)
    fresh_atoms = pair_atoms(blocks)
    triples = {}
    thetas = case.thetas
    for theta in thetas:
        x_theta, t_theta = case.x_values(theta)
        for word, slot in pair_atoms(internal_blocks(x_theta, t_theta)).items():
            for key, value in slot.items():
                triples.setdefault((word, key), {})[theta] = value
    for (word, key), values in triples.items():
        c0 = values.get(thetas[0], Q(0))
        ct = values.get(thetas[1], Q(0)) - c0
        cl = (values.get(thetas[2], Q(0)) - c0) if len(thetas) > 2 else Q(0)
        predicted = c0 + ct * probe[0] + cl * probe[1]
        observed = fresh_atoms.get(word, {}).get(key, Q(0))
        assert predicted == observed, (case.name, word, key)
    for (word, slot) in fresh_atoms.items():
        for key, value in slot.items():
            assert (word, key) in triples, (case.name, word, key)
    for cut in SIX:
        fresh_columns, _labels = raw_columns(cut, blocks)
        for index, (c0, ct, cl) in enumerate(data.column_triples(cut)):
            predicted = dict(c0)
            for source, scale in ((ct, probe[0]), (cl, probe[1])):
                for key, value in source.items():
                    updated = predicted.get(key, 0) + scale * value
                    if updated:
                        predicted[key] = updated
                    else:
                        predicted.pop(key, None)
            observed = project(fresh_columns[index], case.killed_words)
            assert predicted == observed, (case.name, cut, index)


def audit_invariance(case, data):
    """Killed-cell arbitrariness resp. old-class member reproduction."""
    if case.kind == "old":
        variants = [
            {CELLS[bit]: Q(1) for bit in range(9) if mask >> bit & 1}
            for mask in case.member_masks
        ]
    else:
        variants = []
        for cell in case.arbitrary_cells:
            variants.append(("cell", cell))
    for theta in case.thetas:
        reference_tensor = data.tensors[theta]
        reference_atoms = data.atoms[theta]
        reference_columns = {
            cut: data.columns[theta, cut] for cut in SIX
        }
        for variant in variants:
            if case.kind == "old":
                x_values = dict(variant)
                t_value = theta[0]
            else:
                _tag, cell = variant
                x_values, t_value = case.x_values(theta, extra=(cell,))
            blocks = internal_blocks(x_values, t_value)
            assert project(
                matching_tensor(SIX, blocks), case.killed_words
            ) == reference_tensor, (case.name, theta, variant)
            assert project_atoms(
                pair_atoms(blocks), case.killed_words
            ) == reference_atoms, (case.name, theta, variant)
            for cut in SIX:
                columns, _labels = raw_columns(cut, blocks)
                projected = tuple(
                    project(column, case.killed_words) for column in columns
                )
                assert projected == reference_columns[cut], (
                    case.name, theta, variant, cut)


def audit_overspaces(case, data):
    records = []
    for cut in FINAL_CUTS:
        overspace = data.overspaces[cut]
        assert len(overspace) == case.dims[cut], (
            case.name, cut, len(overspace), case.dims[cut])
        basis, pivots = rref(overspace)
        for theta in case.thetas:
            assert in_span(data.tensors[theta], basis, pivots), (
                case.name, cut, theta)
        for colour in case.pair:
            target = (colour,) * 6
            assert target not in case.killed_words, (case.name, colour)
            assert not in_span({target: Q(1)}, basis, pivots), (
                case.name, cut, colour)
        records.append((case.name, cut, len(overspace)))
    return records


# ---------------------------------------------------------------------------
# Lock functionals for the circuit chart


def lock_space(case, data, cut, retained_union):
    """Functionals phi0 + t phi1 + lam phi2 killing every projected column
    of the cut identically in (t, lam), supported on retained coordinates
    that the columns actually touch."""
    triples = data.column_triples(cut)
    support = set()
    for c0, ct, cl in triples:
        support |= set(c0) | set(ct) | set(cl)
    support &= retained_union
    support -= case.killed_words
    coords = tuple(
        (layer, word)
        for layer in (2, 1, 0)
        for word in sorted(support, reverse=True)
    )
    constraints = []
    for c0, ct, cl in triples:
        c0 = {w: v for w, v in c0.items() if w in support}
        ct = {w: v for w, v in ct.items() if w in support}
        cl = {w: v for w, v in cl.items() if w in support}
        rows = (
            {(0, w): v for w, v in c0.items()},
            {**{(0, w): v for w, v in ct.items()},
             **{(1, w): v for w, v in c0.items()}},
            {**{(0, w): v for w, v in cl.items()},
             **{(2, w): v for w, v in c0.items()}},
            {(1, w): v for w, v in ct.items()},
            {(2, w): v for w, v in cl.items()},
            {**{(1, w): v for w, v in cl.items()},
             **{(2, w): v for w, v in ct.items()}},
        )
        constraints.extend(row for row in rows if row)
    locks = annihilator(constraints, coords)
    # Quotient by the junk part whose three layers each annihilate the
    # whole expanded column span: those rows repeat plain annihilator
    # information and add nothing beyond the packet generators.
    span_rows = [
        {w: v for w, v in piece.items() if w in support}
        for triple in triples for piece in triple if piece
    ]
    word_coords = tuple(sorted(support, reverse=True))
    junk_layer = annihilator(span_rows, word_coords)
    junk = []
    for layer in (0, 1, 2):
        for functional in junk_layer:
            junk.append({(layer, w): v for w, v in functional.items()})
    basis, pivots = rref(junk, coords)
    effective = []
    for lock in locks:
        remainder = reduce_vector(lock, basis, pivots)
        if remainder:
            effective.append(remainder)
            basis, pivots = rref(tuple(basis) + (remainder,), coords)
    split = []
    for lock in effective:
        phi0 = {w: v for (layer, w), v in lock.items() if layer == 0}
        phi1 = {w: v for (layer, w), v in lock.items() if layer == 1}
        phi2 = {w: v for (layer, w), v in lock.items() if layer == 2}
        split.append((phi0, phi1, phi2))
    return split


def audit_locks(case, data, lock_table):
    """Verify each lock kills every projected column at 3 probe points."""
    probes = ((Q(2), Q(3)), (Q(5), Q(7)), (Q(11), Q(13)))
    checked = 0
    for cut, locks in lock_table.items():
        for t_value, lam_value in probes:
            x_values, t_actual = case.x_values((t_value, lam_value))
            blocks = internal_blocks(x_values, t_actual)
            columns, _labels = raw_columns(cut, blocks)
            for phi0, phi1, phi2 in locks:
                functional = dict(phi0)
                for source, scale in ((phi1, t_value), (phi2, lam_value)):
                    for key, value in source.items():
                        functional[key] = functional.get(key, 0) + scale * value
                for column in columns:
                    projected = project(column, case.killed_words)
                    assert dot(functional, projected) == 0, (case.name, cut)
                    checked += 1
    return checked


# ---------------------------------------------------------------------------
# Singular systems


def star_name(kind, boundary_colour, site, colour):
    return f"{kind}{boundary_colour}s{site}c{colour}"


def ring_variables(case):
    naive = ["t"]
    if case.two_params:
        naive.append("lam")
    for kind in ("p", "q"):
        for boundary_colour in case.pair:
            for site in SIX:
                for colour in COLOURS:
                    naive.append(star_name(kind, boundary_colour, site, colour))
    return tuple(reversed(naive))


def poly_terms(coeffs):
    """coeffs: {(i, j): Fraction} for t^i lam^j -> list of monomial text."""
    parts = []
    for (i, j), value in sorted(coeffs.items()):
        if not value:
            continue
        monomial = []
        if i == 1:
            monomial.append("t")
        elif i > 1:
            monomial.append(f"t^{i}")
        if j == 1:
            monomial.append("lam")
        elif j > 1:
            monomial.append(f"lam^{j}")
        text = str(value)
        if monomial:
            text = f"{text}*" + "*".join(monomial)
        parts.append(text)
    return parts


def scale_generator(pieces):
    """pieces: list of ({(i,j): Q}, monomial-text-or-None); clear denominators."""
    lcm = 1
    for coeffs, _monomial in pieces:
        for value in coeffs.values():
            d = value.denominator
            g = gcd(lcm, d)
            lcm = lcm // g * d
    chunks = []
    for coeffs, monomial in pieces:
        scaled = {key: value * lcm for key, value in coeffs.items()}
        assert all(value.denominator == 1 for value in scaled.values())
        scaled = {key: value.numerator for key, value in scaled.items()}
        terms = poly_terms({k: Q(v) for k, v in scaled.items() if v})
        if not terms:
            continue
        body = "+".join(terms).replace("+-", "-")
        if monomial is None:
            chunks.append(f"({body})")
        else:
            chunks.append(f"({body})*{monomial}")
    if not chunks:
        return None
    return "+".join(chunks)


def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)


def affine_to_coeffs(triple):
    c0, ct, cl = triple
    coeffs = {}
    if c0:
        coeffs[(0, 0)] = c0
    if ct:
        coeffs[(1, 0)] = ct
    if cl:
        coeffs[(0, 1)] = cl
    return coeffs


def multiply_affine(left, right):
    """(l0 + l1 t + l2 lam) * (r0 + r1 t + r2 lam) as {(i, j): Q}."""
    l0, l1, l2 = left
    r0, r1, r2 = right
    raw = {
        (0, 0): l0 * r0,
        (1, 0): l0 * r1 + l1 * r0,
        (0, 1): l0 * r2 + l2 * r0,
        (2, 0): l1 * r1,
        (0, 2): l2 * r2,
        (1, 1): l1 * r2 + l2 * r1,
    }
    return {key: value for key, value in raw.items() if value}


def pair_monomial(a, b, key):
    i, ci, j, cj = key
    return (
        f"({star_name('p', a, i, ci)}*{star_name('q', b, j, cj)}"
        f"+{star_name('p', a, j, cj)}*{star_name('q', b, i, ci)})"
    )


def build_system(case, data, cut, lock_table):
    atom_triples = data.atom_triples()
    overspace = data.overspaces[cut]
    coords = set(atom_triples)
    for row in overspace:
        coords |= set(row)
    targets = {colour: (colour,) * 6 for colour in case.pair}
    coords |= set(targets.values())
    coords = tuple(sorted(coords, reverse=True))
    rows = annihilator(overspace, coords)
    a_colour, b_colour = case.pair
    fibres = (
        (b_colour, b_colour), (b_colour, a_colour),
        (a_colour, b_colour), (a_colour, a_colour),
    )
    generators = []
    for a, b in fibres:
        for functional in rows:
            pieces = []
            constant = {}
            for word, weight in functional.items():
                for key, triple in atom_triples.get(word, {}).items():
                    scaled = (
                        weight * triple[0], weight * triple[1],
                        weight * triple[2],
                    )
                    pieces.append((affine_to_coeffs(scaled),
                                   pair_monomial(a, b, key)))
                if a == b and word == (a,) * 6:
                    constant[(0, 0)] = constant.get((0, 0), Q(0)) - weight
            if constant.get((0, 0)):
                pieces.append((constant, None))
            text = scale_generator(pieces)
            if text is not None:
                generators.append(text)
    if case.locks:
        for lock_cut in (cut, 4, 3, 2):
            for phi0, phi1, phi2 in lock_table[lock_cut]:
                for a, b in fibres:
                    pieces = []
                    constant = {}
                    words = set(phi0) | set(phi1) | set(phi2)
                    for word in words:
                        phi_triple = (
                            phi0.get(word, Q(0)), phi1.get(word, Q(0)),
                            phi2.get(word, Q(0)),
                        )
                        for key, triple in atom_triples.get(word, {}).items():
                            coeffs = multiply_affine(phi_triple, triple)
                            if coeffs:
                                pieces.append(
                                    (coeffs, pair_monomial(a, b, key)))
                        if a == b and word == (a,) * 6:
                            for slot, value in zip(
                                ((0, 0), (1, 0), (0, 1)), phi_triple
                            ):
                                if value:
                                    constant[slot] = constant.get(
                                        slot, Q(0)) - value
                    if constant:
                        pieces.append((constant, None))
                    text = scale_generator(pieces)
                    if text is not None:
                        generators.append(text)
    generators = list(dict.fromkeys(reversed(generators)))
    names = ring_variables(case)
    program = "ring R=0,(" + ",".join(names) + "),dp;\n"
    program += "option(redSB);\n"
    program += "ideal I=" + ",\n".join(generators) + ";\n"
    program += "ideal G=std(I);\n"
    program += "int ok=0;\nif(reduce(1,G)==0){ok=1;}\n"
    program += 'print("A20UNIT");\nok;\nprint("A20SIZE");\nsize(G);\nquit;\n'
    return program, len(generators), len(names), len(coords), len(rows)


def marker(output, name):
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    return int(lines[lines.index(name) + 1])


def run_singular(program, timeout):
    executable = shutil.which("Singular")
    if executable is None:
        raise SystemExit("Singular is required on PATH")
    started = time.monotonic()
    completed = subprocess.run(
        [executable, "-q"], input=program, text=True,
        capture_output=True, check=True, timeout=timeout,
    )
    if completed.stderr.strip():
        raise AssertionError(completed.stderr[:2000])
    unit = marker(completed.stdout, "A20UNIT")
    size = marker(completed.stdout, "A20SIZE")
    return unit, size, time.monotonic() - started


# ---------------------------------------------------------------------------
# Literal eight-site boundary identity


def audit_literal_eight_site_identity():
    x_values = {
        cell: Q(101 + 7 * index, 89 + index)
        for index, cell in enumerate(CELLS)
    }
    t_value = Q(23, 19)
    interior = internal_blocks(x_values, t_value)
    p_values = {
        (a, site, colour): Q(1009 + 100 * a + 10 * site + colour, 883)
        for a in COLOURS for site in SIX for colour in COLOURS
    }
    q_values = {
        (b, site, colour): Q(2027 + 100 * b + 10 * site + colour, 877)
        for b in COLOURS for site in SIX for colour in COLOURS
    }
    r_values = {
        (a, b): Q(3049 + 10 * a + b, 863) for a in COLOURS for b in COLOURS
    }
    blocks = {edge: dict(cells) for edge, cells in interior.items()}
    for site in SIX:
        blocks[(site, 6)] = {
            (colour, a): p_values[a, site, colour]
            for colour in COLOURS for a in COLOURS
        }
        blocks[(site, 7)] = {
            (colour, b): q_values[b, site, colour]
            for colour in COLOURS for b in COLOURS
        }
    blocks[(6, 7)] = dict(r_values)
    full = matching_tensor(EIGHT, blocks)
    hs = matching_tensor(SIX, interior)
    atoms = pair_atoms(interior)
    for a in COLOURS:
        for b in COLOURS:
            observed = {
                word[:6]: value for word, value in full.items()
                if word[6:] == (a, b)
            }
            expected = {}
            for word, value in hs.items():
                total = expected.get(word, 0) + r_values[a, b] * value
                if total:
                    expected[word] = total
                else:
                    expected.pop(word, None)
            for word, slot in atoms.items():
                total = expected.get(word, 0)
                for (i, ci, j, cj), coefficient in slot.items():
                    total += coefficient * (
                        p_values[a, i, ci] * q_values[b, j, cj]
                        + p_values[a, j, cj] * q_values[b, i, ci]
                    )
                if total:
                    expected[word] = total
                else:
                    expected.pop(word, None)
            assert observed == expected, (a, b)


# ---------------------------------------------------------------------------
# Main


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--timeout", type=int, default=3600)
    parser.add_argument("--skip-singular", action="store_true")
    parser.add_argument("--geometry-only", action="store_true")
    parser.add_argument("--case", action="append", default=None,
                        help="restrict to named cases (debugging)")
    args = parser.parse_args()

    started_all = time.monotonic()
    model = build_linear_model()
    audit_affine_model(model)
    blocks_of, t_block, fixed_support = audit_geometry(model)
    x_chars, t_char = character_data()
    audit_coupled_character(x_chars, t_char)
    audit_literal_eight_site_identity()
    cases = build_cases()
    counts = audit_census(cases, x_chars, t_char)
    print("GEOMETRY pass=1 blocks=9x35 t_block=35 overlaps=(9,9,12)@x2*",
          flush=True)
    print(f"CENSUS masks=512 old=32 outside=480 cases={len(cases)}",
          flush=True)
    if args.geometry_only:
        return
    if args.case:
        cases = [case for case in cases if case.name in set(args.case)]

    jobs = []
    lock_totals = {}
    dim_records = []
    for case in cases:
        case_started = time.monotonic()
        data = CaseData(case, blocks_of, t_block)
        audit_case_affine_probe(case, data)
        audit_invariance(case, data)
        dim_records.extend(audit_overspaces(case, data))
        lock_table = {}
        if case.locks:
            retained_union = set(t_block)
            for cell in case.kept_blocks:
                retained_union |= blocks_of[cell]
            for cut in set(BASE_CUTS) | set(FINAL_CUTS):
                lock_table[cut] = lock_space(case, data, cut, retained_union)
            checked = audit_locks(case, data, lock_table)
            lock_totals[case.name] = {
                cut: len(lock_table[cut]) for cut in sorted(lock_table)
            }
            print(f"LOCKS case={case.name} "
                  f"dims={lock_totals[case.name]} probes={checked}",
                  flush=True)
        for cut in FINAL_CUTS:
            program, generators, variables, coordinates, rows = build_system(
                case, data, cut, lock_table)
            digest = hashlib.sha256(program.encode()).hexdigest()
            jobs.append({
                "case": case.name, "cut": cut, "program": program,
                "generators": generators, "variables": variables,
                "coordinates": coordinates, "annihilator_rows": rows,
                "sha256": digest,
            })
        print(
            f"CASE {case.name} dims="
            f"{tuple(len(data.overspaces[cut]) for cut in FINAL_CUTS)} "
            f"killed={len(case.killed_words)} "
            f"seconds={time.monotonic() - case_started:.2f}",
            flush=True,
        )

    full_run = args.case is None
    if full_run:
        assert len(jobs) == 99
    ledger_rows = sorted(
        (job["case"], job["cut"], job["sha256"]) for job in jobs
    )
    ledger = hashlib.sha256(
        "\n".join(map(repr, ledger_rows)).encode()).hexdigest()
    if full_run and EXPECTED_PROGRAM_LEDGER_SHA256:
        assert ledger == EXPECTED_PROGRAM_LEDGER_SHA256, ledger
    programs = {}
    for job in jobs:
        programs.setdefault(job["sha256"], job["program"])
    for job in jobs:
        print(
            f"SYSTEM {job['case']} cut={job['cut']} "
            f"generators={job['generators']} variables={job['variables']} "
            f"coordinates={job['coordinates']} rows={job['annihilator_rows']} "
            f"sha256={job['sha256'][:16]}",
            flush=True,
        )
    print(f"LEDGER systems={len(jobs)} unique={len(programs)} "
          f"sha256={ledger}", flush=True)
    if args.skip_singular:
        return

    exact_started = time.monotonic()
    elapsed = {}
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(run_singular, program, args.timeout): digest
            for digest, program in programs.items()
        }
        for future in as_completed(futures):
            digest = futures[future]
            unit, size, seconds = future.result()
            assert (unit, size) == (1, 1), (digest, unit, size)
            elapsed[digest] = seconds
            print(f"UNIT {digest[:16]} seconds={seconds:.3f}", flush=True)
    exact_wall = time.monotonic() - exact_started

    print("independent adjacent-E20 coupled-quotient audit: PASS")
    print("literal eight-site fibres, endpoint order, arbitrary A67: PASS")
    print("coupled character wt(t)=wt(x20)-wt(x00), X-rank 5 stays 5: PASS")
    print("512 masks = 32 old + 480 outside; 5+27+1 cases; torus ranks: PASS")
    print("moving block 35 words, overlaps (9,9,12) on x20,x21,x22 only: PASS")
    print("killed sets rebuilt; killed-cell/member invariance at all "
          "specializations: PASS")
    print("expanded overspaces match frozen dims; H_S inside; targets "
          "outside: PASS")
    print(f"{len(jobs)} case/cut systems, {len(programs)} distinct programs, "
          "all unit over Q[t(,lam)]: PASS")
    print(f"cases={len(cases)} systems={len(jobs)} "
          f"unit_ideals={len(programs)}")
    print(f"program ledger SHA256: {ledger}")
    if elapsed:
        print(f"maximum Singular time: {max(elapsed.values()):.3f}s")
    print(f"parallel Singular wall time: {exact_wall:.3f}s")
    print(f"independent total wall time: {time.monotonic() - started_all:.3f}s")


if __name__ == "__main__":
    main()
