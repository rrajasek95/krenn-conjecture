"""UNAUDITED PROBE (W3, Route A, 2026-08-15). HEAD 26ba69f7.

How often does the gauge degeneration lift the aggregate-support floor?

Charts considered: diagonal/coordinate charts given by three colour classes
H_0,H_1,H_2 <= K_8, cell support {(uv,c,c) : uv in H_c}.  Aggregate support
graph is G = H_0 u H_1 u H_2.

For such a chart (exact reduction, see w3_gapsearch):

   mult(word w) = pm(H_0[A]) * pm(H_1[B]) * pm(H_2[C]),
                  A,B,C = the colour classes of w

   M8 silent  <=>  pm(H_c) >= 1 for each c
   M9 silent  <=>  no mixed (A,B,C) with all three factors equal to 1
   O5 fires   <=>  some H_c has an edge in no fractional perfect matching
   BLOCK DIES <=>  an edge uv is inessential in EVERY H_c containing it
"""

from __future__ import annotations

import itertools
import random
from collections import Counter

from w3_band import ALL_EDGES, N, VERTS, failing_edges
from w3_gapsearch import _pm

PARTS = None


def partitions():
    """All (A,B,C) ordered partitions of V into three (possibly empty) parts,
    excluding the three pure ones."""
    global PARTS
    if PARTS is None:
        out = []
        for assign in itertools.product(range(3), repeat=N):
            if len(set(assign)) == 1:
                continue
            A = tuple(v for v in VERTS if assign[v] == 0)
            B = tuple(v for v in VERTS if assign[v] == 1)
            C = tuple(v for v in VERTS if assign[v] == 2)
            out.append((A, B, C))
        PARTS = out
    return PARTS


def m8_silent(Hs):
    return all(_pm(frozenset(H), tuple(VERTS)) >= 1 for H in Hs)


def m9_silent(Hs):
    fs = [frozenset(H) for H in Hs]
    for (A, B, C) in partitions():
        if _pm(fs[0], A) == 1 and _pm(fs[1], B) == 1 and _pm(fs[2], C) == 1:
            return False
    return True


def o5_dead(Hs):
    return [set(failing_edges(tuple(H))) for H in Hs]


def block_deaths(Hs, dead):
    G = set().union(*[set(H) for H in Hs])
    out = []
    for e in G:
        live = [c for c in range(3) if e in Hs[c]]
        if live and all(e in dead[c] for c in live):
            out.append(e)
    return out


def survey(mode, trials=4000, seed=5, p=0.7):
    """mode 'uniform': H_0=H_1=H_2=H.   mode 'independent': three random H_c."""
    rng = random.Random(seed)
    st = Counter()
    cuts = []
    for _ in range(trials):
        if mode == "uniform":
            H = [e for e in ALL_EDGES if rng.random() < p]
            Hs = [H, H, H]
        else:
            Hs = [[e for e in ALL_EDGES if rng.random() < p] for _ in range(3)]
        G = set().union(*[set(H) for H in Hs])
        deg = Counter()
        for e in G:
            deg[e[0]] += 1
            deg[e[1]] += 1
        if len(G) < 13 or min(deg.get(v, 0) for v in VERTS) < 3:
            continue
        st["charts"] += 1
        if not m8_silent(Hs):
            st["m8"] += 1
            continue
        if not m9_silent(Hs):
            st["m9"] += 1
            continue
        st["survive_committed"] += 1
        dead = o5_dead(Hs)
        if any(dead):
            st["o5"] += 1
            bd = block_deaths(Hs, dead)
            if bd:
                st["blocks_die"] += 1
                cuts.append((len(G), len(G) - len(bd)))
    return st, cuts


if __name__ == "__main__":
    print("UNAUDITED PROBE  W3 / Route A  HEAD 26ba69f7")
    print("FLOOR-LIFT RATE on diagonal/coordinate charts (min degree >= 3)")
    print("=" * 84)
    for mode in ("uniform", "independent"):
        print(f"\nmode = {mode}")
        print(f"{'p':>5} {'charts':>7} {'M8':>6} {'M9':>7} {'survive':>8} "
              f"{'O5 fires':>9} {'blocks die':>11}  typical support drop")
        for p in (0.45, 0.55, 0.65, 0.75, 0.85):
            st, cuts = survey(mode, trials=1500, p=p, seed=11)
            n = st["charts"]
            if not n:
                continue
            sv = st["survive_committed"]
            drops = Counter(cuts)
            common = ", ".join(
                f"{a}->{b} x{k}" for (a, b), k in drops.most_common(3)
            )
            print(
                f"{p:>5} {n:>7} {st['m8']:>6} {st['m9']:>7} {sv:>8} "
                f"{st['o5']:>9} {st['blocks_die']:>11}  {common}"
            )
