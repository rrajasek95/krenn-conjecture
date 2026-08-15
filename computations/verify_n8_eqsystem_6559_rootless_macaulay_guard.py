#!/usr/bin/env python3
"""A literal N=8 EqSystem rootless-line guard with only two missing rows.

This is an intrinsic coefficient calculation.  It uses no auxiliary B/Eq,
Gamma, or AugP2 coordinates.  Starting from the committed 22-parameter
site-square-zero near-miss family, it freezes the base tensor A and proves:

* A has 77 nonzero edge-colour cells and satisfies 6559 of the 6561 literal
  GHZ coefficient equations; the only failures are 0^8 and 1^8, both 0=1;
* for endpoints (p,q)=(0,3), residual sites (1,2,4,5,6,7), and the physical
  cap line K_z=E_01+zI, alpha=A_03(0,1)=2 and trace(A_03)=14, hence the
  activity polynomial is z^3(2+14z), not identically zero;
* two clean-error coordinates have relatively prime cubics.  Their six
  degree-two Macaulay multiples form an explicit nonsingular 6x6 Sylvester
  matrix.  Thus the full 6x2187 clean-error Macaulay map has rank six and the
  projective line contains no clean point at all.

Consequently, if J is the literal EqSystem ideal with only the two equations
for 0^8 and 1^8 omitted and Delta is the displayed maximal minor, then
J:(alpha*Delta)^infinity is proper.  Any intrinsic Nullstellensatz proof of
the rootless-line theorem must therefore use at least one of those two pure
normalization rows (or a consequence which genuinely contains it).

This is NOT an exact GHZ source and hence not a counterexample to Krenn's
conjecture.  Nor does it prove that either omitted row alone is indispensable.

Exact stdlib arithmetic only.  Verification:

    python3       computations/verify_n8_eqsystem_6559_rootless_macaulay_guard.py
    python3 -O    computations/verify_n8_eqsystem_6559_rootless_macaulay_guard.py
    python3 -I    computations/verify_n8_eqsystem_6559_rootless_macaulay_guard.py
    python3 -S    computations/verify_n8_eqsystem_6559_rootless_macaulay_guard.py
    python3 -I -S computations/verify_n8_eqsystem_6559_rootless_macaulay_guard.py
    python3 -m py_compile computations/verify_n8_eqsystem_6559_rootless_macaulay_guard.py
"""

from __future__ import annotations

import importlib
import os
import sys
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, product

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


PINNED_SOURCES = {
    "verify_n8_d2_kill_and_monochrome_rigidity.py":
        "6320c3bdb795df3050952e52bd9c0fb9f4d5f2cdbf9eb543cd3467179630a745",
    "verify_cap_line_cubic_activity_dichotomy.py":
        "39a0b8ee22e4eec56b1174d200e29679a3baeae1a814ec422f69b6a9725f1300",
}


def pin_sources():
    got = {}
    for name, want in sorted(PINNED_SOURCES.items()):
        with open(os.path.join(HERE, name), "rb") as handle:
            got[name] = sha256(handle.read()).hexdigest()
        require(got[name] == want,
                "pinned source %s changed: got %s" % (name, got[name]))
    return got


PINS = pin_sources()
D = importlib.import_module("verify_n8_d2_kill_and_monochrome_rigidity")
L = importlib.import_module("verify_cap_line_cubic_activity_dichotomy")

COLORS = (0, 1, 2)
ALL_SITES = tuple(range(8))
ENDPOINTS = (0, 3)
RESIDUAL = tuple(x for x in ALL_SITES if x not in ENDPOINTS)
SELECTED_COLOURS = (0, 1)
SELECTED_WORDS = ((0, 0, 2, 2, 2, 2), (0, 1, 2, 2, 2, 2))
EXPECTED_CUBICS = (
    (Q(-2376), Q(158424), Q(1108992), Q(1422096)),
    (Q(-6264), Q(-196872), Q(-2392464), Q(-7644624)),
)
EXPECTED_DETERMINANT = 4723356504268883541779583860736
EXPECTED_LEDGER_SHA256 = (
    "c4864039f8fdb44feb3d8627520cf8ad1661ef6c0fb50dfc0c2b9a6a49d9f9e5"
)


def as_chart_packet(blocks):
    """Restrict the literal eight-site tensor to the (0,3) pair chart.

    The construction retains every edge-colour entry.  It is merely an
    endpoint/residual reindexing, not a quotient or specialization.
    """
    local = {site: index for index, site in enumerate(RESIDUAL)}
    q, p, s, direct = {}, {}, {}, {}
    for x, y in combinations(RESIDUAL, 2):
        block = D.C.oriented(blocks, x, y)
        for a, b in product(COLORS, repeat=2):
            if block[a][b]:
                q[(local[x], local[y], a, b)] = block[a][b]
    for x in RESIDUAL:
        left = D.C.oriented(blocks, ENDPOINTS[0], x)
        right = D.C.oriented(blocks, ENDPOINTS[1], x)
        for a, c in product(COLORS, repeat=2):
            if left[a][c]:
                p[(a, local[x], c)] = left[a][c]
            if right[a][c]:
                s[(a, local[x], c)] = right[a][c]
    block = D.C.oriented(blocks, *ENDPOINTS)
    for a, b in product(COLORS, repeat=2):
        if block[a][b]:
            direct[(a, b)] = block[a][b]
    return L.Packet(q, p, s, direct)


def full_word(residual_word, left_colour, right_colour):
    word = dict(zip(RESIDUAL, residual_word))
    word[ENDPOINTS[0]] = left_colour
    word[ENDPOINTS[1]] = right_colour
    return word


def audit_literal_eqsystem(blocks, packet):
    """Replay all 6561 source coefficients and the exact chart equality."""
    defects = {}
    chart_mismatches = 0
    for residual_word in L.WORDS:
        local_word = dict(enumerate(residual_word))
        for i, j in product(COLORS, repeat=2):
            word = full_word(residual_word, i, j)
            source_value = D.C.coefficient(blocks, ALL_SITES, word)
            chart_value = packet.row(i, j, local_word)
            if source_value != chart_value:
                chart_mismatches += 1
            target = Q(1) if len(set(word.values())) == 1 else Q(0)
            if source_value != target:
                defects[tuple(word[x] for x in ALL_SITES)] = (
                    source_value, target)
    require(chart_mismatches == 0,
            "pair-chart formula disagrees with the literal source recursion")
    want = {(0,) * 8: (Q(0), Q(1)), (1,) * 8: (Q(0), Q(1))}
    require(defects == want,
            "the literal defect ledger is not exactly the two pure rows: %s"
            % (defects,))
    return defects


def shifted_column(cubic, shift):
    """Coefficients in degrees 0..5 of z^shift*cubic(z)."""
    values = [Q(0)] * 6
    for degree, coefficient in enumerate(cubic):
        values[degree + shift] = coefficient
    return tuple(values)


def determinant(matrix):
    """Exact Gaussian determinant, including mutation-sensitive row swaps."""
    work = [list(map(Q, row)) for row in matrix]
    n = len(work)
    require(n and all(len(row) == n for row in work),
            "determinant expects a nonempty square matrix")
    answer = Q(1)
    for column in range(n):
        pivot = next((row for row in range(column, n)
                      if work[row][column]), None)
        if pivot is None:
            return Q(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            answer = -answer
        value = work[column][column]
        answer *= value
        for row in range(column + 1, n):
            factor = work[row][column] / value
            for col in range(column + 1, n):
                work[row][col] -= factor * work[column][col]
    return answer


def audit_rootless_line(packet):
    i, j = SELECTED_COLOURS
    direct_block = tuple(tuple(packet.de(a, b) for b in COLORS)
                         for a in COLORS)
    require(direct_block == ((Q(10), Q(2), Q(4)),
                             (Q(20), Q(4), Q(8)),
                             (Q(0), Q(0), Q(0))),
            "the selected direct block changed: %s" % (direct_block,))
    alpha = packet.de(i, j)
    tau = sum((packet.de(c, c) for c in COLORS), Q(0))
    require((alpha, tau) == (Q(2), Q(14)),
            "the selected scalar pencil is no longer 2+14z")

    info = L.line_verdict(packet, i, j)
    require(info["s"] == (Q(2), Q(14)), "s(K_z) changed")
    require(info["act"] == (Q(0), Q(0), Q(0), Q(2), Q(14)),
            "activity is not z^3(2+14z): %s" % (info["act"],))
    require(info["gcd"] == (Q(1),) and info["verdict"] == "rootless (gcd one)",
            "the clean-error family is not rootless: %s" % (info,))
    require(info["rank"] == 4,
            "the 729x4 clean-coordinate coefficient matrix lost rank four")

    cubics = tuple(info["cubics"][word] for word in SELECTED_WORDS)
    require(cubics == EXPECTED_CUBICS,
            "the two selected clean cubics changed: %s" % (cubics,))
    columns = tuple(shifted_column(cubic, shift)
                    for cubic in cubics for shift in range(3))
    # Multiplication by the cubics maps the six inputs
    # (u^2,uv,v^2) for each coordinate into Sym^5.  The columns below are
    # the standard Sylvester/Macaulay matrix in coefficient order 0..5.
    matrix = tuple(tuple(columns[column][row] for column in range(6))
                   for row in range(6))
    delta = determinant(matrix)
    require(delta == EXPECTED_DETERMINANT,
            "the selected 6x6 Macaulay minor changed: %s" % delta)
    require(L.rank_of(columns, 6) == 6,
            "the selected degree-two Macaulay columns do not span Sym^5")

    all_columns = [shifted_column(cubic, shift)
                   for cubic in info["cubics"].values()
                   for shift in range(3)]
    require(len(all_columns) == 3 * 3 ** 6,
            "the full Macaulay map is not 6x2187")
    require(L.rank_of(all_columns, 6) == 6,
            "the full clean-error Macaulay map is not rank six")
    # A designed mutation of the selected minor must be visible.
    damaged = [list(row) for row in matrix]
    damaged[0] = [Q(0)] * 6
    require(determinant(damaged) == 0,
            "the determinant control accepted a matrix with a zero row")
    return {
        "endpoints": ENDPOINTS,
        "residual": RESIDUAL,
        "selected_colours": SELECTED_COLOURS,
        "direct_block": direct_block,
        "alpha": alpha,
        "tau": tau,
        "activity": info["act"],
        "coordinate_rank": info["rank"],
        "nonzero_clean_coordinates": info["nonzero"],
        "gcd": info["gcd"],
        "selected_words_local": SELECTED_WORDS,
        "selected_words_global": tuple(
            tuple(full_word(word, i, j)[x] for x in ALL_SITES)
            for word in SELECTED_WORDS),
        "selected_cubics": cubics,
        "sylvester_matrix": matrix,
        "sylvester_determinant": delta,
        "full_macaulay_shape": (6, len(all_columns)),
        "full_macaulay_rank": L.rank_of(all_columns, 6),
    }


def build_ledger():
    blocks = D.build_stage_a(D.STAGE_A_BASE)
    nonzero_cells = sum(entry != 0 for block in blocks.values()
                        for row in block for entry in row)
    require(nonzero_cells == 77,
            "the literal near-miss support is no longer 77 cells")
    packet = as_chart_packet(blocks)
    defects = audit_literal_eqsystem(blocks, packet)
    rootless = audit_rootless_line(packet)
    return {
        "pinned_sources": PINS,
        "literal_nonzero_cells": nonzero_cells,
        "eqsystem_rows": 3 ** 8,
        "satisfied_rows": 3 ** 8 - len(defects),
        "defects": tuple(sorted((word, value, target)
                                for word, (value, target) in defects.items())),
        "rootless_line": rootless,
        "ideal_consequence": (
            "For J=I_8 without the pure 0^8 and 1^8 equations, the displayed "
            "rational point lies in V(J) with alpha*Delta nonzero; hence "
            "J:(alpha*Delta)^infinity is proper."
        ),
        "scope": (
            "literal site-square-zero N=8 tensor, but not an exact GHZ source; "
            "it fails exactly two pure normalization rows"
        ),
    }


def main():
    ledger = build_ledger()
    digest = D.content_hash(ledger)
    require(digest == EXPECTED_LEDGER_SHA256,
            "ledger digest changed: got %s" % digest)
    line = ledger["rootless_line"]
    print("PASS: literal 77-cell N=8 tensor satisfies 6559/6561 EqSystem rows")
    print("defects: pure 0^8 and 1^8 only (both 0=1)")
    print("line: endpoints %s, K_z=E_01+zI, activity z^3(2+14z)" %
          (ENDPOINTS,))
    print("clean Macaulay: shape %s, rank %d; selected determinant %s" %
          (line["full_macaulay_shape"], line["full_macaulay_rank"],
           line["sylvester_determinant"]))
    print("saturated consequence: J:(alpha*Delta)^infinity is proper")
    print("sha256: %s" % digest)


if __name__ == "__main__":
    main()
