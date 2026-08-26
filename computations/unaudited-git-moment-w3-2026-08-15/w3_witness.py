"""UNAUDITED PROBE (W3, Route A, 2026-08-15). HEAD 26ba69f7.

Extract, minimise and FULLY verify an explicit floor-lift gap witness:
a coordinate chart on which the committed support kills M8 (missing pure
row) and M9 (singleton mixed row) are both silent, yet the gauge mechanism
of Theorem A.1 forces a strict support degeneration.

Verification is end-to-end and does not reuse the fast criterion:
  * M8/M9 are recomputed from the literal 3^8 word multiplicities;
  * the instability certificate w is produced and checked exactly
    (integer arithmetic: W_w(s) >= 0 on S, sum_v w_{v,c} = 0, S_0 proper);
  * the surviving support is confirmed to still satisfy the pure rows.
"""

from __future__ import annotations

import itertools
import json
import random
from fractions import Fraction

from w3_balance import classify, verify_degeneration
from w3_band import ALL_EDGES, N, VERTS, failing_edges
from w3_core import cell_index, edge_index, is_pure, live_terms, words
from w3_gapsearch import _pm, anneal, m8_silent, m9_silent, o5_fires


def chart_from_H0(H0):
    """T_uv = {1,2} u ({0} if uv in H_0)."""
    return {e: sorted({1, 2} | ({0} if e in H0 else set())) for e in ALL_EDGES}


def cell_support(T):
    EI, CI = edge_index(N), cell_index(N)
    return frozenset(CI[(EI[e], c, c)] for e, cs in T.items() for c in cs)


def literal_word_check(T):
    """Recompute M8/M9 from the literal 3^8 rows, independently of the
    pm-product shortcut."""
    S = cell_support(T)
    singles = []
    pure = {}
    for w in words(N):
        live = live_terms(N, S, w)
        if is_pure(w):
            pure[w[0]] = len(live)
        elif len(live) == 1:
            singles.append(w)
    return pure, singles


def minimise(H0):
    """Greedily drop edges of H_0 while the gap property survives."""
    H = set(H0)
    changed = True
    while changed:
        changed = False
        for e in sorted(H):
            H2 = H - {e}
            if m8_silent(H2) and m9_silent(H2) and o5_fires(H2):
                H = H2
                changed = True
                break
    return frozenset(H)


def full_report(H0, label=""):
    T = chart_from_H0(H0)
    S = cell_support(T)
    pure, singles = literal_word_check(T)
    dead = failing_edges(tuple(H0))
    tag, cert = classify(N, S)
    print(f"--- {label}")
    print(f"    H_0 ({len(H0)} edges) = {sorted(H0)}")
    deg = {v: sum(1 for e in H0 if v in e) for v in VERTS}
    print(f"    degrees in H_0: {[deg[v] for v in VERTS]}   pm(H_0) = "
          f"{_pm(frozenset(H0), tuple(VERTS))}")
    print(f"    literal pure-row multiplicities: {pure}   (M8 silent: "
          f"{all(v >= 1 for v in pure.values())})")
    print(f"    literal mixed singletons: {len(singles)}   (M9 silent: "
          f"{not singles})")
    print(f"    edges of H_0 in no fractional pm: {sorted(dead)}")
    print(f"    exact balance LP on the full 3-colour cell support: {tag}")
    if tag.startswith("D"):
        ok = verify_degeneration(N, S, cert)
        killed = sorted(cert["killed"])
        EI = edge_index(N)
        inv = {v: k for k, v in cell_index(N).items()}
        names = [inv[s] for s in killed]
        E = list(ALL_EDGES)
        pretty = sorted((E[k], i, j) for (k, i, j) in names)
        print(f"    exact certificate verified: {ok}")
        print(f"    cells killed by the degeneration ({len(killed)}): {pretty}")
        S0 = cert["S0"]
        pure0 = {}
        for w in words(N):
            if is_pure(w):
                pure0[w[0]] = len(live_terms(N, S0, w))
        print(f"    pure rows on the degenerate support S_0: {pure0} "
              f"(all >= 1: {all(v >= 1 for v in pure0.values())})")
        blocks_before = len({(k) for (k, i, j) in (inv[s] for s in S)})
        blocks_after = len({(k) for (k, i, j) in (inv[s] for s in S0)})
        print(f"    aggregate blocks: {blocks_before} -> {blocks_after}")
    return tag


if __name__ == "__main__":
    print("UNAUDITED PROBE  W3 / Route A  HEAD 26ba69f7")
    print("EXPLICIT FLOOR-LIFT GAP WITNESSES")
    print("=" * 78)
    found = []
    for seed in range(6):
        r = anneal(seed=seed, steps=40000)
        if r is None or r[0] != 0:
            continue
        H = minimise(r[1])
        if H not in found:
            found.append(H)
    print(f"{len(found)} distinct minimised witnesses\n")
    for i, H in enumerate(found[:4]):
        full_report(H, f"witness {i}")
        print()
    if found:
        with open("gap_witnesses.json", "w") as fh:
            json.dump([sorted(map(list, H)) for H in found], fh, indent=1)
        print(f"wrote gap_witnesses.json ({len(found)} witnesses)")
