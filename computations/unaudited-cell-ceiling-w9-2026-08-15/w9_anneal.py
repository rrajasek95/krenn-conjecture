#!/usr/bin/env python3
"""W9 -- honest Sigma_min: minimise cells over templates satisfying ONLY the
conditions FORCED on an exact eight-site source.

W6 measured Sigma_min with beta PINNED to the floor max(0, 3N-m).  That is
not forced -- the budget gives beta >= 3N-m+|H|, a LOWER bound -- and pinning
can only INFLATE Sigma_min.  Sigma_min sits on the right of the inequality
H4 must beat, so an inflated value makes H4 look easier than it is.

Forced conditions used (source in brackets):
  (T1) m nonempty blocks                       [definition of support]
  (Tb) beta >= max(0, 3N - m)                  [W6 budget, |H| >= 0]
  (T4) each pure word has fibre >= 1           [H(c^N)=1 != 0]
  (T6) every (vertex,colour) slot has a cell   [implied by (T4)]
  (T5) every vertex meets >= 3 blocks          [slice-cover d_R(v) >= 3]
  (S)  no mixed word has fibre 1               [O2]

Fibre counts are exact int32 numpy counts (<= 105 at N=8; no floats).
Every reported certificate is re-verified by the independent pure-Python
counter in w9_template.py.
"""
from __future__ import annotations
import math, os, random, sys, time
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "unaudited-bridge-w6-2026-08-15"))
from w6_task2_collision8 import geometry            # noqa: E402

CELLS = tuple((a, b) for a in range(3) for b in range(3))
_CELLMASK = {}


def cellmask(geo, n, cell):
    key = (geo.size, n, cell)
    if key not in _CELLMASK:
        u, v = geo.edges[n]
        _CELLMASK[key] = ((geo.colour[:, u] == cell[0])
                          & (geo.colour[:, v] == cell[1]))
    return _CELLMASK[key]


_ALLOWED = {}


def allowed_of(geo, n, sup):
    key = (geo.size, n, sup)
    a = _ALLOWED.get(key)
    if a is None:
        a = np.zeros(len(geo.colour), dtype=bool)
        for c in sup:
            a |= cellmask(geo, n, c)
        if len(_ALLOWED) > 400000:
            _ALLOWED.clear()
        _ALLOWED[key] = a
    return a


def evaluate(geo, template):
    allowed = [None if not s else allowed_of(geo, n, s)
               for n, s in enumerate(template)]
    total = np.zeros(len(geo.colour), dtype=np.int32)
    for indices in geo.matching_edges:
        mask = None
        for n in indices:
            a = allowed[n]
            if a is None:
                mask = None
                break
            mask = a if mask is None else (mask & a)
        if mask is not None:
            total += mask
    missing = sum(1 for row in geo.constant_rows if total[row] == 0)
    singles = int(np.count_nonzero((total == 1) & geo.mixed))
    deg = [0] * geo.size
    slots = set()
    for n, sup in enumerate(template):
        if not sup:
            continue
        u, v = geo.edges[n]
        deg[u] += 1
        deg[v] += 1
        for a, b in sup:
            slots.add((u, a))
            slots.add((v, b))
    return (missing, singles, geo.size * 3 - len(slots),
            sum(max(0, 3 - d) for d in deg), sum(len(s) for s in template))


def cost(geo, template, m, beta_floor, W=400):
    live = [n for n, s in enumerate(template) if s]
    if len(live) != m:
        return None, None
    beta = sum(1 for n in live if len(template[n]) == 1)
    miss, sing, slotdef, degdef, Sigma = evaluate(geo, template)
    betadef = max(0, beta_floor - beta)
    bad = miss + sing + slotdef + degdef + betadef
    rec = {"missing": miss, "singletons": sing, "slot_deficit": slotdef,
           "degree_deficit": degdef, "beta": beta, "beta_deficit": betadef,
           "sigma": Sigma, "bad": bad, "feasible": bad == 0}
    return W * bad + Sigma, rec


def move(geo, rng, tpl):
    out = [set(s) for s in tpl]
    live = [n for n, s in enumerate(out) if s]
    multi = [n for n in live if len(out[n]) >= 2]
    singles = [n for n in live if len(out[n]) == 1]
    r = rng.random()
    if r < 0.40 and multi:                       # drop a cell (bias to shrink)
        n = rng.choice(multi)
        out[n].discard(rng.choice(sorted(out[n])))
    elif r < 0.62:                               # add a cell
        n = rng.choice(live)
        if len(out[n]) >= 9:
            return None
        out[n].add(rng.choice(CELLS))
    elif r < 0.78 and singles:                   # recolour a single cell
        n = rng.choice(singles)
        out[n] = {rng.choice(CELLS)}
    elif r < 0.90 and multi:                     # recolour one cell of a multi
        n = rng.choice(multi)
        c = rng.choice(sorted(out[n]))
        out[n].discard(c)
        out[n].add(rng.choice(CELLS))
        if not out[n]:
            return None
    else:                                        # relocate a whole edge
        empty = [n for n in range(len(geo.edges)) if not out[n]]
        if not empty:
            return None
        src, dst = rng.choice(live), rng.choice(empty)
        out[dst], out[src] = set(out[src]), set()
    return [frozenset(s) for s in out]


def anneal(geo, rng, m, beta_floor, seconds, warm=None, T0=8.0):
    """Simulated annealing on 400*infeasibility + Sigma.  ``warm`` is a
    feasible starting template (e.g. one of W6's certificates)."""
    start = time.time()
    best = None
    cur_tpl = warm
    while time.time() - start < seconds:
        if cur_tpl is None:
            cur_tpl = _random_seed(geo, rng, m, beta_floor)
            if cur_tpl is None:
                return best
        cur, rec = cost(geo, cur_tpl, m, beta_floor)
        if cur is None:
            cur_tpl = None
            continue
        if rec["feasible"] and (best is None or rec["sigma"] < best[0]):
            best = (rec["sigma"], [sorted(s) for s in cur_tpl], dict(rec))
        T = T0
        tpl = cur_tpl
        while time.time() - start < seconds:
            T = max(T * 0.9997, 0.15)
            cand = move(geo, rng, tpl)
            if cand is None:
                continue
            val, r2 = cost(geo, cand, m, beta_floor)
            if val is None:
                continue
            if val <= cur or rng.random() < math.exp(-(val - cur) / T):
                tpl, cur = cand, val
                if r2["feasible"] and (best is None or r2["sigma"] < best[0]):
                    best = (r2["sigma"], [sorted(s) for s in cand], dict(r2))
        cur_tpl = None if best is None else [frozenset(map(tuple, s))
                                             for s in best[1]]
    return best


def _random_seed(geo, rng, m, beta_floor, tries=400):
    universe = list(range(len(geo.edges)))
    for _ in range(tries):
        edges = rng.sample(universe, m)
        nb = rng.randint(beta_floor, min(m, beta_floor + 6))
        singles = set(rng.sample(edges, nb))
        tpl = [frozenset() for _ in geo.edges]
        for n in edges:
            tpl[n] = (frozenset({rng.choice(CELLS)}) if n in singles
                      else frozenset(rng.sample(CELLS, rng.choice([3, 4, 6, 9]))))
        v, _ = cost(geo, tpl, m, beta_floor)
        if v is not None:
            return tpl
    return None
