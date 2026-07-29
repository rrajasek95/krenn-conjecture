#!/usr/bin/env python3
"""Search exact Glynn-kernel covers yielding Per_m -> Delta_3.

For normalized sign vectors d in {+/-1}^m / {+/-1}, Glynn's formula writes
the permanent tensor as a signed sum of product vectors.  If, at each tensor
factor, the local map kills a codimension-three signed-partition subspace,
then its killed sign vectors form an affine codimension-three cube.  This
script searches for at most m such cubes covering every sign vector except
three survivors, while the three survivor images are independent.
"""

from __future__ import annotations

import argparse
import itertools
import random

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import csc_matrix
from pysat.card import CardEnc, EncType
from pysat.formula import CNF
from pysat.solvers import Solver


def signs(mask: int, m: int) -> np.ndarray:
    return np.array([1] + [1 if not (mask >> (j - 1)) & 1 else -1
                           for j in range(1, m)], dtype=np.int8)


def forest(m: int, edges: tuple[tuple[int, int], ...]) -> bool:
    parent = list(range(m))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in edges:
        a, b = find(a), find(b)
        if a == b:
            return False
        parent[a] = b
    return True


def candidates(m: int, survivor_masks: tuple[int, int, int], star_only: bool = False):
    vec = {mask: signs(mask, m) for mask in range(1 << (m - 1))}
    survivors = [vec[x] for x in survivor_masks]
    universe = [x for x in vec if x not in survivor_masks]
    pos = {x: i for i, x in enumerate(universe)}
    ans = []
    edges_all = list(itertools.combinations(range(m), 2))
    for edges in itertools.combinations(edges_all, 3):
        if star_only and not all(a == 0 for a, _b in edges):
            continue
        if not forest(m, edges):
            continue
        for parity in range(8):
            # Equation row is x_a - eps*x_b; eps=(-1)^c.
            dmat = np.zeros((3, m), dtype=np.int8)
            for k, (a, b) in enumerate(edges):
                dmat[k, a] = 1
                dmat[k, b] = -1 if not ((parity >> k) & 1) else 1
            images = np.column_stack([dmat @ s for s in survivors])
            if abs(round(np.linalg.det(images))) == 0:
                continue
            killed = []
            for mask in universe:
                if np.all(dmat @ vec[mask] == 0):
                    killed.append(pos[mask])
            if killed:
                ans.append((tuple(killed), edges, parity, dmat, images))
    return universe, ans


def heuristic_cover(universe, cand, m: int, tries: int = 2000):
    full = (1 << len(universe)) - 1
    bits = []
    for item in cand:
        z = 0
        for i in item[0]:
            z |= 1 << i
        bits.append(z)
    rng = random.Random(739391)
    best = (0, [])
    for _ in range(tries):
        covered = 0
        chosen = []
        pool = list(range(len(cand)))
        for _step in range(m):
            scores = [(bits[j] & ~covered).bit_count() for j in pool]
            top = sorted(range(len(pool)), key=lambda k: scores[k], reverse=True)[:50]
            pick_pos = rng.choice(top[:max(1, min(len(top), 1 + _step * 3))])
            j = pool.pop(pick_pos)
            chosen.append(j)
            covered |= bits[j]
        score = covered.bit_count()
        if score > best[0]:
            best = (score, chosen)
            print("heuristic", score, "/", len(universe), flush=True)
        if covered == full:
            return chosen
    return None


def solve(m: int, survivor_masks: tuple[int, int, int], heuristic: bool,
          star_only: bool, bound: int | None, sat: bool) -> None:
    universe, cand = candidates(m, survivor_masks, star_only)
    unique = {}
    for item in cand:
        unique.setdefault(item[0], item)
    cand = list(unique.values())
    print("m", m, "survivors", survivor_masks, "universe", len(universe),
          "candidates", len(cand), flush=True)
    if heuristic:
        chosen = heuristic_cover(universe, cand, m)
        if chosen is None:
            print("no heuristic cover")
            return
        result_x = np.zeros(len(cand))
        result_x[chosen] = 1
    elif sat:
        by_point = [[] for _ in universe]
        for j, item in enumerate(cand, start=1):
            for i in item[0]:
                by_point[i].append(j)
        if any(not clause for clause in by_point):
            print("uncovered point")
            return
        cnf = CNF(from_clauses=by_point)
        card = CardEnc.atmost(list(range(1, len(cand) + 1)), bound=bound or m,
                             top_id=len(cand), encoding=EncType.seqcounter)
        cnf.extend(card.clauses)
        with Solver(name="cadical195", bootstrap_with=cnf) as solver:
            okay = solver.solve()
            print("SAT" if okay else "UNSAT", "clauses", len(cnf.clauses),
                  "vars", cnf.nv, flush=True)
            if not okay:
                return
            model = set(x for x in solver.get_model() if x > 0)
        result_x = np.array([1 if j in model else 0
                             for j in range(1, len(cand) + 1)])
    else:
        rows, cols = [], []
        for j, item in enumerate(cand):
            for i in item[0]:
                rows.append(i)
                cols.append(j)
        data = np.ones(len(rows), dtype=float)
        cover = csc_matrix((data, (rows, cols)), shape=(len(universe), len(cand)))
        constraints = [LinearConstraint(cover, lb=np.ones(len(universe)),
                                        ub=np.full(len(universe), np.inf)),
                       LinearConstraint(np.ones((1, len(cand))), lb=-np.inf,
                                        ub=np.array([bound or m], dtype=float))]
        result = milp(np.ones(len(cand)), integrality=np.ones(len(cand)),
                      bounds=Bounds(np.zeros(len(cand)), np.ones(len(cand))),
                      constraints=constraints,
                      options={"time_limit": 120, "mip_rel_gap": 0})
        print(result.message, "objective", result.fun, flush=True)
        if result.x is None:
            return
        result_x = result.x
    chosen = [j for j, x in enumerate(result_x) if x > 0.5]
    for j in chosen:
        killed, edges, parity, dmat, images = cand[j]
        print("candidate", j, "edges", edges, "parity", parity,
              "kills", len(killed))
        print("D=", dmat.tolist())
        print("survivor_images=", images.tolist())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("m", type=int)
    parser.add_argument("survivors", nargs=3, type=lambda x: int(x, 0))
    parser.add_argument("--heuristic", action="store_true")
    parser.add_argument("--star", action="store_true")
    parser.add_argument("--bound", type=int)
    parser.add_argument("--sat", action="store_true")
    args = parser.parse_args()
    solve(args.m, tuple(args.survivors), args.heuristic, args.star, args.bound,
          args.sat)


if __name__ == "__main__":
    main()
