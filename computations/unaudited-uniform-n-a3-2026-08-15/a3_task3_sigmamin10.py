#!/usr/bin/env python3
"""A3 Task 3(d) -- does W6's cell price of singleton-freeness,
Sigma_min(N,m) ~ 3.2 m, persist at N = 10?

FRESH implementation (no W6 code imported).  W6 evaluates by AND-ing 3^N
boolean word masks along each matching; at N = 10 that is 945 x 5 x 59049
boolean ops per template.  Here each (edge, cell) is given the base-3 code
    val(e,(a,b)) = a*3^u + b*3^v ,   e = uv,
so a matching's contributed words are the CARTESIAN SUM of its five edges'
code arrays -- one numpy outer-sum chain per matching, then a single
bincount.  Exact integer arithmetic throughout (fibre sizes are counts).

Model (W6's, restated): a template assigns each edge a set of cells
(a,b) in [3]x[3]; empty = absent.  m = #live edges, Sigma = total cells,
beta = #edges with exactly one cell.  fibre(c) = #{matchings all of whose
edges carry the cell (c_u,c_v)} -- because the word determines the cell.
Structural constraints (W6's structural_ok): |live| = m, #single-cell = beta,
min live degree >= 3, all 3N (vertex,colour) slots covered.
Cost = 500*(missing constants) + 50*(mixed singletons) + Sigma.

Sigma_min reported is an UPPER bound (a search finds templates), which is the
conservative direction: the cell ceiling a closing lemma must beat is at most
this.
"""

from __future__ import annotations

import json
import math
import random
import sys
import time

import numpy as np

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from a3_core import geometry

CELLS = [(a, b) for a in range(3) for b in range(3)]


class Frame:
    def __init__(self, n):
        self.n = n
        self.geo = geometry(n)
        self.edges = self.geo.edges
        self.ne = len(self.edges)
        self.nwords = 3 ** n
        pw = [3 ** v for v in range(n)]
        # code[e][k] for cell CELLS[k] on edge e
        self.code = [np.array([a * pw[u] + b * pw[v] for (a, b) in CELLS],
                              dtype=np.int64)
                     for (u, v) in self.edges]
        self.matching_edges = self.geo.matching_edges
        self.constant_codes = [sum(r * pw[v] for v in range(n))
                               for r in range(3)]
        mixed = np.ones(self.nwords, dtype=bool)
        for c in self.constant_codes:
            mixed[c] = False
        self.mixed = mixed

    def evaluate(self, template):
        """(missing constants, mixed singletons, fibre-size array)."""
        arrays = [self.code[e][sorted(template[e])] if template[e] else None
                  for e in range(self.ne)]
        chunks = []
        for idx in self.matching_edges:
            acc = None
            ok = True
            for e in idx:
                a = arrays[e]
                if a is None:
                    ok = False
                    break
                acc = a if acc is None else (acc[:, None] + a[None, :]).ravel()
            if ok:
                chunks.append(acc)
        if not chunks:
            return 3, 0, None
        total = np.bincount(np.concatenate(chunks), minlength=self.nwords)
        missing = sum(1 for c in self.constant_codes if total[c] == 0)
        singles = int(np.count_nonzero((total == 1) & self.mixed))
        return missing, singles, total


def structural_ok(fr, template, m, beta, require_sc=True):
    """W6's conditions PLUS, when require_sc, the committed slice-cover
    condition (SC): for every (vertex p, colour r) some incident edge has ALL
    its cells carrying colour r at the FAR endpoint.  W6 (and my first run)
    imposed only the weaker 'every (vertex,colour) slot is touched by SOME
    cell', which admits templates the committed condition excludes."""
    live = [e for e in range(fr.ne) if template[e]]
    if len(live) != m:
        return False
    if sum(1 for e in live if len(template[e]) == 1) != beta:
        return False
    deg = [0] * fr.n
    slots = set()
    sc = set()
    for e in live:
        u, v = fr.edges[e]
        deg[u] += 1
        deg[v] += 1
        cells = [CELLS[k] for k in template[e]]
        for a, b in cells:
            slots.add((u, a))
            slots.add((v, b))
        # (SC): all cells of e have the same FAR colour, seen from u then v
        if len({b for a, b in cells}) == 1:
            sc.add((u, cells[0][1]))
        if len({a for a, b in cells}) == 1:
            sc.add((v, cells[0][0]))
    if min(deg) < 3 or len(slots) != 3 * fr.n:
        return False
    return (not require_sc) or len(sc) == 3 * fr.n


def cost(fr, template, m, beta):
    if not structural_ok(fr, template, m, beta):
        return None, None
    missing, singles, _ = fr.evaluate(template)
    sig = sum(len(s) for s in template)
    return 500 * missing + 50 * singles + sig, dict(
        missing=missing, singletons=singles, sigma=sig)


def seed(fr, rng, m, beta, tries=4000):
    for _ in range(tries):
        live = rng.sample(range(fr.ne), m)
        singles = set(rng.sample(live, beta))
        template = [set() for _ in range(fr.ne)]
        for e in live:
            if e in singles:
                template[e] = {rng.randrange(9)}
            else:
                k = rng.randint(2, 5)
                template[e] = set(rng.sample(range(9), k))
        if structural_ok(fr, template, m, beta):
            return template
    return None


def anneal(fr, rng, m, beta, steps, t0=60.0, t1=1.0):
    template = seed(fr, rng, m, beta)
    if template is None:
        return None
    cur, _ = cost(fr, template, m, beta)
    best, best_t, best_info = cur, [set(s) for s in template], None
    for t in range(steps):
        temp = t0 * (t1 / t0) ** (t / max(1, steps - 1))
        e = rng.randrange(fr.ne)
        if not template[e]:
            continue
        old = set(template[e])
        if len(old) == 1:
            k = rng.randrange(9)
            template[e] = {k}
        else:
            if rng.random() < 0.5 and len(old) > 2:
                template[e] = old - {rng.choice(sorted(old))}
            else:
                template[e] = old | {rng.randrange(9)}
                if len(template[e]) == 1:
                    template[e] = old
        val, info = cost(fr, template, m, beta)
        if val is None:
            template[e] = old
            continue
        if val <= cur or rng.random() < math.exp(-(val - cur) / temp):
            cur = val
            if info["missing"] == 0 and info["singletons"] == 0:
                if best_info is None or info["sigma"] < best_info["sigma"]:
                    best_info = dict(info)
                    best_t = [set(s) for s in template]
        else:
            template[e] = old
    return best_info, best_t


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    steps = int(sys.argv[2]) if len(sys.argv) > 2 else 4000
    restarts = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    fr = Frame(n)
    rng = random.Random(20260815)
    out = {"N": n, "steps": steps, "restarts": restarts, "rows": []}
    supports = ([16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 45] if n == 10
                else [16, 19, 22, 25, 27, 28])
    t0 = time.time()
    for m in supports:
        beta = max(0, 3 * n - m)
        if beta > m:
            continue
        best = None
        for _ in range(restarts):
            r = anneal(fr, rng, m, beta, steps)
            if r is None:
                continue
            info, tpl = r
            if info and (best is None or info["sigma"] < best["sigma"]):
                best = info
        row = dict(m=m, beta=beta,
                   sigma_min_upper=best["sigma"] if best else None,
                   ratio=round(best["sigma"] / m, 3) if best else None)
        out["rows"].append(row)
        print(f"N={n} m={m:3d} beta={beta:3d} -> Sigma_min <= "
              f"{row['sigma_min_upper']}  ratio={row['ratio']}"
              f"   [{time.time()-t0:.0f}s]")
    out["seconds"] = round(time.time() - t0, 1)
    path = __file__.rsplit("/", 1)[0] + f"/results_sigmamin_N{n}.json"
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1)
    print("wrote", path)


if __name__ == "__main__":
    main()
