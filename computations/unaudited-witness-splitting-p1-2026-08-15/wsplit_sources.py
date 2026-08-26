#!/usr/bin/env python3
"""UNAUDITED PROBE -- P1: exact source families for the cap-error study.

Pinned HEAD: 86a9479bef38169bbfd8d9100c6d81ce4c66209a

Provides
  * the committed near-exact eight-site tensor (STAGE_A, 6559 of 6561 GHZ
    rows correct; built by verify_n8_d2_kill_and_monochrome_rigidity.py)
    re-charted to any pair (p,q);
  * degenerate families with prescribed r-support used for the structural
    analysis (two-star, three-star, single-star);
  * random exact-integer sources at several sparsity levels.
All values are Fractions/ints.  No floating point.
"""

from __future__ import annotations

import importlib
import os
import sys
from fractions import Fraction
from itertools import combinations

import wsplit_core as core
from wsplit_core import COLORS, P, Q, U, kidx, require

REPO_COMPUTATIONS = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
)


def load_stage_a(second: bool = False) -> dict:
    """The committed near-exact eight-site source, physical labels 0..7."""
    if REPO_COMPUTATIONS not in sys.path:
        sys.path.insert(0, REPO_COMPUTATIONS)
    mod = importlib.import_module("verify_n8_d2_kill_and_monochrome_rigidity")
    params = mod.STAGE_A_SECOND if second else mod.STAGE_A_BASE
    blocks = mod.build_stage_a(params)
    out = {}
    for u, v in combinations(range(8), 2):
        table = mod.C.oriented(blocks, u, v)
        out[(u, v)] = [[table[a][b] for b in COLORS] for a in COLORS]
    return out


def rechart(physical: dict, p: int, q: int) -> dict:
    """Relabel an eight-site source so that p -> P=0, q -> Q=1, rest -> U."""
    rest = [x for x in range(8) if x not in (p, q)]
    label = {p: P, q: Q}
    for n, site in enumerate(rest):
        label[site] = U[n]
    src = core.zero_source()
    for u, v in combinations(range(8), 2):
        table = physical[(u, v)]
        lu, lv = label[u], label[v]
        if lu < lv:
            src[(lu, lv)] = [[table[a][b] for b in COLORS] for a in COLORS]
        else:
            src[(lv, lu)] = [[table[a][b] for a in COLORS] for b in COLORS]
    return src


def ghz_defects(physical: dict) -> int:
    """Count boundary words where H_B(A) != Delta_{B,3} (independent check)."""
    from itertools import product as iproduct
    matchings = core.perfect_matchings(tuple(range(8)))
    bad = 0
    for word in iproduct(COLORS, repeat=8):
        total = 0
        for matching in matchings:
            term = 1
            for u, v in matching:
                term *= physical[(u, v)][word[u]][word[v]]
                if not term:
                    break
            total += term
        target = 1 if len(set(word)) == 1 else 0
        if total != target:
            bad += 1
    return bad


# ------------------------------------------------------------ star families


def star_source(pairs, colors, pvecs, qvecs, x_blocks=None, apq=None) -> dict:
    """A source whose r is supported on the p-star x q-star edges only.

    ``pairs`` is a tuple of (p_site, q_site); ``colors[n]`` is the colour at
    which the n-th p-block and q-block are concentrated:

        A_{p,p_site_n}[i][alpha] = delta_{i, colors[n]} * pvecs[n][alpha]
        A_{q,q_site_n}[j][beta]  = delta_{j, colors[n]} * qvecs[n][beta]

    so R_{p_site_a, q_site_b} = (pvec_a (x) qvec_b) * K_{colors[a],colors[b]}.
    """
    src = core.zero_source()
    src[(P, Q)] = [list(row) for row in (apq or ((1, 0, 0), (0, 1, 0),
                                                 (0, 0, 1)))]
    for n, (psite, qsite) in enumerate(pairs):
        c = colors[n]
        for i in COLORS:
            for a in COLORS:
                src[core.edge_key(P, psite)][i][a] = (
                    pvecs[n][a] if i == c else 0)
        for j in COLORS:
            for b in COLORS:
                src[core.edge_key(Q, qsite)][j][b] = (
                    qvecs[n][b] if j == c else 0)
    for edge, table in (x_blocks or {}).items():
        src[edge] = [list(row) for row in table]
    return src


def two_star(c1: int, c2: int, x67=((1, 0, 2), (0, 1, 1), (3, 1, 0)),
             apq=((1, 0, 0), (0, 2, 0), (0, 0, 3))) -> dict:
    """r on the 2x2 star {2,4} x {3,5}; the only U-block is x_{67}.

    E_w = s * x67(w) * (prod of star weights) * (k_{c1}k_{c2} + K_{c1c2}K_{c2c1}).
    """
    return star_source(((2, 3), (4, 5)), (c1, c2),
                       ((1, 2, -1), (1, -1, 2)),
                       ((3, 1, 1), (2, 1, -3)),
                       {(6, 7): x67}, apq)


def three_star(c1: int, c2: int, c3: int,
               apq=((1, 0, 0), (0, 1, 0), (0, 0, 1))) -> dict:
    """r on the 3x3 star {2,4,6} x {3,5,7}, x == 0 on U, so 6E = r^3.

    E_w = 6 * (prod of star weights) * per( K[{c1,c2,c3} , {c1,c2,c3}] ).
    """
    return star_source(((2, 3), (4, 5), (6, 7)), (c1, c2, c3),
                       ((1, 2, -1), (1, -1, 2), (2, 1, 1)),
                       ((3, 1, 1), (2, 1, -3), (1, 1, 2)),
                       {}, apq)


def single_star(apq=((1, 0, 0), (0, 1, 0), (0, 0, 1))) -> dict:
    """r supported on one edge => r^2 = 0 => E == 0 (plan case (c))."""
    src = star_source(((2, 3),), (0,), ((1, 2, -1),), ((3, 1, 1),),
                      {(4, 5): ((1, 0, 1), (0, 1, 0), (1, 1, 1)),
                       (6, 7): ((1, 0, 1), (0, 1, 0), (1, 1, 1)),
                       (2, 3): ((1, 0, 1), (0, 1, 0), (1, 1, 1))}, apq)
    return src


def dead_edge(src: dict) -> dict:
    out = {k: [list(r) for r in v] for k, v in src.items()}
    out[(P, Q)] = [[0] * 3 for _ in range(3)]
    return out


def scaled_star(pairs, colors, scale_p, scale_q, x_blocks=None,
                apq=((1, 0, 0), (0, 1, 0), (0, 0, 1))) -> dict:
    """Star family with caller-supplied weight vectors (for pattern search)."""
    return star_source(pairs, colors, scale_p, scale_q, x_blocks, apq)
