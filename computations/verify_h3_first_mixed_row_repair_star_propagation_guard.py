#!/usr/bin/env python3
"""Exact propagation of the first c8a0383 mixed-word defect.

The 20-cell guard of c8a0383 first fails at row 00:000011.  Its two
rootless-repair stars also have exactly four joint physical descendants,
the rows 01:01d01 for d in {00,01,11,22}.  This checker enforces the first
row and all four descendants without introducing formal response tensors.

There is no one-cell physical repair preserving the original 36 rows.  The
support-minimal two-cell branch

    q_05^(01) = 1,      p_0(4,1) = -1

repairs all five rows, preserves common q, exact GHZ quotient slices, the
direct/K_* relation, activity, and rootlessness.  It replaces a 12-row
defect orbit by an eight-row private orbit.  The first private row has three
one-cell continuations; the best one, q_34^(00)=1, replaces the same 12 old
defects by six new ones and lowers the full defect count from 106 to 100.

Thus this propagation is not a unit contradiction.  It gives a strictly
smaller literal rootless guard and identifies the next six-row orbit.
"""

from __future__ import annotations

import importlib
import os
import sys
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


PINS = {
    "verify_h3_pure_selected_mixed_rootless_common_q_guard.py":
        "ad6534cb08b29b66217cfefc7aa241964f95ced752ea0b6e81a9775517ccf7a1",
    "../notes/2026-08-15-h3-pure-selected-mixed-rootless-common-q-guard.md":
        "c9a26002177c16e41fe3c4f50c31ace1522ad7b5abb9d1f05ebdd7c27a80a861",
}
EXPECTED_LEDGER_SHA256 = (
    "f0da2eedd52d72366273ae5b8f324499bfe0cf4b1aeb0380647018b1e12ea2fd"
)


def pin_sources():
    result = {}
    for relative, expected in sorted(PINS.items()):
        path = os.path.normpath(os.path.join(HERE, relative))
        with open(path, "rb") as handle:
            result[relative] = sha256(handle.read()).hexdigest()
        require(result[relative] == expected,
                "pinned source changed: %s (%s)" %
                (relative, result[relative]))
    return result


PINNED = pin_sources()
G = importlib.import_module(
    "verify_h3_pure_selected_mixed_rootless_common_q_guard")
H, N, A, L = G.H, G.N, G.A, G.L

FIRST = (0, 0, (0, 0, 0, 0, 1, 1))
DELETED_PAIRS = ((0, 0), (0, 1), (1, 1), (2, 2))
STAR_FORCED = tuple(
    (0, 1, (0, 1) + deleted + (0, 1))
    for deleted in DELETED_PAIRS
)
FIRST_PRIVATE = (0, 0, (0, 0, 0, 0, 0, 1))


def target(i, j, word):
    return G.target(i, j, word)


def build_two_cell_guard():
    base = G.build_packet()
    q, p = dict(base.q), dict(base.p)
    q[(0, 5, 0, 1)] = Q(1)
    p[(0, 4, 1)] = Q(-1)
    return L.Packet(q, p, dict(base.s), dict(base.d))


def build_best_continuation():
    guard = build_two_cell_guard()
    q = dict(guard.q)
    q[(3, 4, 0, 0)] = Q(1)
    return L.Packet(q, dict(guard.p), dict(guard.s), dict(guard.d))


def row_value(packet, key):
    i, j, word = key
    return packet.row(i, j, dict(enumerate(word)))


def defect_ledger(packet):
    defects = {}
    for i, j in product(A.COLORS, repeat=2):
        for word in A.WORDS:
            difference = row_value(packet, (i, j, word)) - target(i, j, word)
            if difference:
                defects[(i, j, word)] = difference
    return defects


def missing_cells(packet):
    cells = []
    for key in ((x, y, a, b) for x, y in L.PAIRS
                for a, b in product(A.COLORS, repeat=2)):
        if not packet.q.get(key, Q(0)):
            cells.append(("q", key))
    for key in product(A.COLORS, L.SITES, A.COLORS):
        if not packet.p.get(key, Q(0)):
            cells.append(("p", key))
        if not packet.s.get(key, Q(0)):
            cells.append(("s", key))
    return tuple(cells)


def adjoin(packet, kind, key, value):
    blocks = [dict(packet.q), dict(packet.p), dict(packet.s), dict(packet.d)]
    blocks[{"q": 0, "p": 1, "s": 2}[kind]][key] = value
    return L.Packet(*blocks)


def single_cell_repairs(packet, constraints):
    """All nonzero rational one-cell repairs; dependence is affine-linear."""
    repairs = []
    for kind, key in missing_cells(packet):
        unit = adjoin(packet, kind, key, Q(1))
        double = adjoin(packet, kind, key, Q(2))
        required_values = set()
        possible = True
        for i, j, word, want in constraints:
            base = row_value(packet, (i, j, word)) - want
            slope = (row_value(unit, (i, j, word))
                     - row_value(packet, (i, j, word)))
            require(row_value(double, (i, j, word))
                    - row_value(packet, (i, j, word)) == 2 * slope,
                    "a purported one-cell direction was not affine-linear")
            if slope:
                required_values.add(-base / slope)
            elif base:
                possible = False
        if (possible and len(required_values) == 1
                and next(iter(required_values))):
            repairs.append((kind, key, next(iter(required_values))))
    return tuple(repairs)


def local_constraints():
    return tuple(
        (i, j, word, target(i, j, word))
        for word in G.LOCAL_WORDS
        for i, j in product(A.COLORS, repeat=2)
    )


def polynomial_rows():
    """The exact two-variable ideal for the support-minimal repair chart."""
    base = G.build_packet()
    polynomial = L.P

    def convert(block):
        return {key: polynomial.const(value) for key, value in block.items()}

    q, p, s, direct = (convert(block) for block in
                       (base.q, base.p, base.s, base.d))
    q[(0, 5, 0, 1)] = polynomial.var("t")
    p[(0, 4, 1)] = polynomial.var("r")
    symbolic = L.Packet(q, p, s, direct, symbolic=True)

    result = {
        "first": row_value(symbolic, FIRST).t,
        "forced": tuple(row_value(symbolic, key).t for key in STAR_FORCED),
        "private": row_value(symbolic, FIRST_PRIVATE).t,
    }
    require(result["first"] == {
        (): Q(1), ("r", "t"): Q(1)},
        "the first repair equation is not 1+r*t")
    require(all(row == {(): Q(1), ("t",): Q(-1)}
                for row in result["forced"]),
            "the four repair-star equations are not all 1-t")
    require(result["private"] == {("t",): Q(-1)},
            "the private propagation equation is not -t")
    return result


def selected_rootless_minor(packet):
    line = L.line_verdict(packet, 0, 1)
    selected, columns = [], []
    for word, cubic in line["cubics"].items():
        for shift in range(3):
            column = G.shifted_column(cubic, shift)
            if L.rank_of(columns + [column], 6) > len(columns):
                selected.append((word, shift))
                columns.append(column)
            if len(columns) == 6:
                break
        if len(columns) == 6:
            break
    require(len(columns) == 6,
            "the greedy exact rootless minor did not reach rank six")
    minor = tuple(tuple(columns[column][row] for column in range(6))
                  for row in range(6))
    return line, tuple(selected), minor, G.determinant(minor)


def generic_audit(packet):
    p_vectors = tuple(A.star_vector(packet, "P", colour)
                      for colour in A.COLORS)
    s_vectors = tuple(A.star_vector(packet, "S", colour)
                      for colour in A.COLORS)
    ranks = (A.D.C.rank(p_vectors), A.D.C.rank(s_vectors),
             A.D.C.rank(p_vectors + s_vectors))
    require(ranks == (3, 3, 6), "a propagated endpoint split lost rank")

    q3 = A.q_cube(packet)
    targets = tuple(A.target_vector(colour) for colour in A.COLORS)
    require(all(q3[A.WORDS.index((colour,) * 6)] == 0
                for colour in A.COLORS),
            "a propagated q cube acquired a pure coordinate")
    require(len(A.independent_vectors((q3,) + targets)) == 4,
            "the propagated q cube lost generic independence")

    _, cross, common_q = H.audit_common_q(packet, p_vectors, s_vectors)
    slices = []
    for colour in A.COLORS:
        functional, _ = N.functional_for_pure_target(q3, colour)
        slices.append([[A.pairing(functional, cross[i][j])
                        for j in A.COLORS] for i in A.COLORS])
    slices = tuple(slices)
    require(slices == N.canonical_slices(),
            "a propagated packet lost the exact labelled GHZ slices")

    direct = tuple(tuple(packet.de(i, j) for j in A.COLORS)
                   for i in A.COLORS)
    require(direct == ((Q(-1), Q(-1), Q(0)),
                       (Q(0), Q(0), Q(0)),
                       (Q(0), Q(0), Q(0))),
            "the direct block/K_* input changed")
    line, selected, minor, determinant = selected_rootless_minor(packet)
    columns = [G.shifted_column(cubic, shift)
               for cubic in line["cubics"].values() for shift in range(3)]
    require(line["act"] == (Q(0), Q(0), Q(0), Q(-1), Q(-1)),
            "the propagated activity polynomial changed")
    require(line["gcd"] == (Q(1),)
            and L.rank_of(columns, 6) == 6 and determinant == Q(-192),
            "the propagated packet is not explicitly rootless")
    return {
        "star_ranks": ranks,
        "q3_support": sum(bool(value) for value in q3),
        "rank_q3_targets": 4,
        "quotient_slices": tuple(tuple(tuple(row) for row in matrix)
                                  for matrix in slices),
        "common_q": common_q,
        "direct": direct,
        "activity": line["act"],
        "clean_gcd": line["gcd"],
        "macaulay_rank": L.rank_of(columns, 6),
        "selected_columns": selected,
        "selected_minor": minor,
        "selected_minor_determinant": determinant,
    }


def audit():
    base = G.build_packet()
    two_cell = build_two_cell_guard()
    best = build_best_continuation()

    # The joint contribution of the two original rootless-repair stars is
    # exhaustive: deleting either changes exactly these four source rows.
    star_changes = []
    for shore, key in (("p", (0, 4, 0)), ("s", (1, 5, 1))):
        blocks = [dict(base.q), dict(base.p), dict(base.s), dict(base.d)]
        del blocks[1 if shore == "p" else 2][key]
        deleted = L.Packet(*blocks)
        changed = tuple(
            key0 for i, j in product(A.COLORS, repeat=2)
            for word in A.WORDS
            for key0 in ((i, j, word),)
            if row_value(base, key0) != row_value(deleted, key0)
        )
        require(changed == STAR_FORCED,
                "a repair star changed rows outside the four-row orbit")
        line = L.line_verdict(deleted, 0, 1)
        columns = [G.shifted_column(cubic, shift)
                   for cubic in line["cubics"].values()
                   for shift in range(3)]
        require(line["gcd"] == (Q(0), Q(1), Q(1))
                and L.rank_of(columns, 6) == 4,
                "deleting an original repair star did not restore z(z+1)")
        star_changes.append((shore, key, changed))

    constraints37 = local_constraints() + (
        (FIRST[0], FIRST[1], FIRST[2], Q(0)),)
    first_single = single_cell_repairs(base, constraints37)
    require(len(missing_cells(base)) == 225 and not first_single,
            "the first bad row unexpectedly has a one-cell repair")

    # The two-cell packet repairs the first row and the complete four-row
    # star orbit, while retaining every original local row.
    repaired_keys = (FIRST,) + STAR_FORCED
    require(all(row_value(two_cell, key) == target(*key)
                for key in repaired_keys),
            "the support-minimal two-cell packet missed a required row")
    require(all(row_value(two_cell, (i, j, word)) == want
                for i, j, word, want in local_constraints()),
            "the support-minimal repair broke an original local row")

    symbolic = polynomial_rows()
    # From 1-t=0 and 1+r*t=0 one gets t=1,r=-1; the next row is -t=-1.
    require(row_value(two_cell, FIRST_PRIVATE) == Q(-1),
            "the first private propagation row changed")

    constraints42 = (local_constraints()
                     + tuple((i, j, word, Q(0))
                             for i, j, word in repaired_keys)
                     + ((FIRST_PRIVATE[0], FIRST_PRIVATE[1],
                         FIRST_PRIVATE[2], Q(0)),))
    continuations = single_cell_repairs(two_cell, constraints42)
    expected_continuations = (
        ("q", (1, 4, 0, 0), Q(-1)),
        ("q", (3, 4, 0, 0), Q(1)),
        ("q", (4, 5, 0, 1), Q(1)),
    )
    require(len(missing_cells(two_cell)) == 223
            and continuations == expected_continuations,
            "the exact first-private one-cell continuation census changed")

    continuation_audit = []
    for continuation in continuations:
        propagated = adjoin(two_cell, *continuation)
        line, selected, _, determinant = selected_rootless_minor(propagated)
        all_columns = [G.shifted_column(cubic, shift)
                       for cubic in line["cubics"].values()
                       for shift in range(3)]
        require(line["gcd"] == (Q(1),)
                and L.rank_of(all_columns, 6) == 6 and determinant,
                "a first-private continuation lost rootlessness")
        continuation_audit.append(
            (continuation, len(defect_ledger(propagated)),
             selected, determinant))
    require(tuple(entry[1] for entry in continuation_audit)
            == (111, 100, 121),
            "the three first-private continuation defect counts changed")

    base_defects = defect_ledger(base)
    two_defects = defect_ledger(two_cell)
    best_defects = defect_ledger(best)
    require((len(base_defects), len(two_defects), len(best_defects))
            == (106, 102, 100),
            "the monotone defect counts changed")

    removed = set(base_defects) - set(best_defects)
    added = set(best_defects) - set(base_defects)
    common_changed = {key for key in set(base_defects) & set(best_defects)
                      if base_defects[key] != best_defects[key]}
    expected_removed = {
        (0, j, (0, j) + deleted + tail)
        for j, tail in ((0, (1, 1)), (1, (0, 1)), (2, (1, 1)))
        for deleted in DELETED_PAIRS
    }
    expected_added = {
        (0, j, (0, j) + deleted + (0, 1))
        for j in (0, 2)
        for deleted in ((0, 1), (1, 1), (2, 2))
    }
    require(removed == expected_removed and added == expected_added
            and not common_changed,
            "the 12-to-6 defect-orbit propagation changed")
    require(all(base_defects[key] == Q(1) for key in removed)
            and all(best_defects[key] == Q(-1) for key in added),
            "the propagated orbit signs changed")
    require(next(iter(sorted(best_defects.items())))
            == ((0, 0, (0, 0, 0, 0, 2, 2)), Q(1)),
            "the next full-source defect changed")

    two_generic = generic_audit(two_cell)
    best_generic = generic_audit(best)
    return {
        "pins": PINNED,
        "repair_star_changes": tuple(star_changes),
        "first_row": FIRST,
        "first_row_single_cell_candidate_count": len(first_single),
        "two_cell_repair": (
            ("q", (0, 5, 0, 1), Q(1)),
            ("p", (0, 4, 1), Q(-1)),
        ),
        "exact_two_variable_rows": symbolic,
        "first_private_row": (FIRST_PRIVATE, Q(-1)),
        "private_one_cell_continuations": continuations,
        "private_continuation_audit": tuple(continuation_audit),
        "best_continuation": ("q", (3, 4, 0, 0), Q(1)),
        "defect_counts": (106, 102, 100),
        "removed_orbit": tuple(sorted((key, base_defects[key])
                                      for key in removed)),
        "new_private_orbit": tuple(sorted((key, best_defects[key])
                                          for key in added)),
        "next_full_source_defect": next(iter(sorted(best_defects.items()))),
        "two_cell_generic_audit": two_generic,
        "best_generic_audit": best_generic,
        "scope": (
            "literal physical monotone propagation from the fixed 20-cell "
            "chart; the 23-cell endpoint is not a full source and no global "
            "minimality outside this chart is claimed"
        ),
    }


def build_ledger():
    return {
        "theorem": (
            "the first mixed row and complete joint repair-star orbit admit "
            "a support-minimal physical repair; propagation strictly shrinks "
            "the defect orbit 12-to-6 but leaves an exact rootless guard"
        ),
        "audit": audit(),
        "terminal_alternative": (
            "deleting either original repair star restores the common root "
            "z(z+1); keeping both permits the displayed smaller guard"
        ),
    }


def main():
    ledger = build_ledger()
    digest = A.D.content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 == "TO_BE_FILLED":
        print("computed-sha256:", digest)
        return
    require(digest == EXPECTED_LEDGER_SHA256,
            "ledger digest changed: got %s" % digest)
    print("PASS: first mixed row propagates to a smaller rootless guard")
    print("repair DAG: 20 cells/106 defects -> 22/102 -> 23/100")
    print("old 12-row orbit -> new six-row private orbit")
    print("common-q, exact GHZ slices, K*, activity, rootless det -192 pass")
    print("next full row: 00:000022=1")
    print("sha256:", digest)


if __name__ == "__main__":
    main()
