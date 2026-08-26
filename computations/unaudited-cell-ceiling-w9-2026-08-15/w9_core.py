#!/usr/bin/env python3
"""UNAUDITED PROBE (W9) -- the cell ceiling H4: shared exact core.

Pinned HEAD: see PINNED_HEAD.txt (a1196b4dca9f83452483734a3273c0c43d5cf3b5).
Plan: notes/2026-08-15-resolution-master-plan.md (v8 addendum, H4).
NOTHING HERE IS A PROVED CLAIM.  Exact integer/Fraction arithmetic only.

H4 (the target, OPEN): an exact N=8 source with support m in 19..27 has
occupied-cell count Sigma <= C(m) with C(m) < Sigma_min(m), the measured
price of singleton-freeness (61@19, 64@20, 68@21, 70@22, 77@23, 82@24,
85@25, 99@26, 98@27).

Vocabulary (matches w6_core.py):
  source     dict (u,v) -> 3x3 table, u<v; row index = colour at u.
  m          # nonzero blocks  ("support", live edges)
  Sigma      # nonzero cells summed over all blocks
  beta       # single-cell blocks
  |H|        # blocks of rank >= 2
"""

from __future__ import annotations

import os
import sys
from fractions import Fraction
from itertools import combinations, product

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
COMPUTATIONS = os.path.join(REPO, "computations")
for _p in (os.path.join(COMPUTATIONS, "unaudited-bridge-w6-2026-08-15"),
           os.path.join(COMPUTATIONS, "unaudited-witness-splitting-p1-2026-08-15"),
           COMPUTATIONS):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import w6_core as w6            # noqa: E402
from w6_core import COLORS, hafnian, oriented, edge_key, matrix_rank, cells  # noqa: E402
from w6_core import classify_block, block_census, pair_expansion, require   # noqa: E402


# --------------------------------------------------------------- sources

def load_stage_a(second: bool = False) -> dict:
    """The committed near-exact eight-site source (defects: 0^8 and 1^8 only)."""
    import importlib
    mod = importlib.import_module("verify_n8_d2_kill_and_monochrome_rigidity")
    params = mod.STAGE_A_SECOND if second else mod.STAGE_A_BASE
    blocks = mod.build_stage_a(params)
    out = {}
    for u, v in combinations(range(8), 2):
        table = mod.C.oriented(blocks, u, v)
        out[(u, v)] = [[Fraction(table[a][b]) for b in COLORS] for a in COLORS]
    return out


def defect_words(source, size=8):
    """{word: (got, want)} over all 3^size words where H != Delta."""
    out = {}
    sites = tuple(range(size))
    for word in product(COLORS, repeat=size):
        colour = {u: word[u] for u in sites}
        got = hafnian(source, sites, colour)
        want = 1 if len(set(word)) == 1 else 0
        if got != want:
            out[word] = (got, want)
    return out


def mixed_defect_count(source, size=8):
    """# mixed (non-constant) words with H != 0."""
    bad = 0
    sites = tuple(range(size))
    for word in product(COLORS, repeat=size):
        if len(set(word)) == 1:
            continue
        if hafnian(source, sites, {u: word[u] for u in sites}) != 0:
            bad += 1
    return bad


# ---------------------------------------------------------------- census

def full_census(source, size=8):
    """The W9 calibration census of one source."""
    per_block = {}
    Sigma = 0
    m = 0
    beta = 0
    Hcount = 0
    kinds = {}
    cellhist = {}
    for u, v in combinations(range(size), 2):
        mat = source[(u, v)]
        cs = cells(mat)
        r = matrix_rank(mat)
        kind = classify_block(mat)
        per_block[(u, v)] = {"cells": len(cs), "rank": r, "kind": kind,
                             "support": cs}
        kinds[kind] = kinds.get(kind, 0) + 1
        Sigma += len(cs)
        if cs:
            m += 1
            cellhist[len(cs)] = cellhist.get(len(cs), 0) + 1
            if len(cs) == 1:
                beta += 1
            if r >= 2:
                Hcount += 1
    return {"m": m, "Sigma": Sigma, "beta": beta, "H": Hcount,
            "kinds": kinds, "cell_histogram": cellhist,
            "per_block": per_block,
            "Sigma_over_m": (Fraction(Sigma, m) if m else None)}


def degree_profile(source, size=8):
    """(live-degree, rank-one-degree) per vertex."""
    dlive = [0] * size
    dR = [0] * size
    for u, v in combinations(range(size), 2):
        mat = source[(u, v)]
        if cells(mat):
            dlive[u] += 1
            dlive[v] += 1
        if matrix_rank(mat) == 1:
            dR[u] += 1
            dR[v] += 1
    return dlive, dR


SIGMA_MIN = {16: 52, 17: 55, 18: 58, 19: 61, 20: 64, 21: 68, 22: 70,
             23: 77, 24: 82, 25: 85, 26: 99, 27: 98, 28: 102}
