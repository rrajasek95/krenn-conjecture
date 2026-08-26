#!/usr/bin/env python3
"""UNAUDITED PROBE (W8) -- exact SAT decision for

    "is there a template with support <= m that is FIE-admissible, supports
     all three constant words, and has NO mixed singleton fibre?"

Pinned HEAD: a1196b4dca9f83452483734a3273c0c43d5cf3b5

UNSAT at m  =>  every exact N=8 source of support <= m has a mixed singleton
fibre, hence a nonzero mixed coefficient (O2) -- the band closes below m by
O2 alone, with no value-level work.
SAT at m    =>  an explicit admissible zero-singleton template, handed to the
value-level kill engine (w8_core.analyse).

ENCODING (exact, cell level; no R_cell / monomial assumption).
  c[e][k], k = 3i+j        cell (i,j) of edge e is occupied            252 vars
  present[e] <-> OR_k c[e][k]
  Sigma_e present[e] <= m                                     (pysat CardEnc)
  thin[e][s][r] -> block e is nonempty and lives in colour r at endpoint s
  (FIE) for every vertex p, colour r:  OR over neighbours j of thin[pj][j][r]
  (CONST) for every colour c: OR over the 105 matchings M of const[c][M],
          const[c][M] -> all four cells (c,c) of M present
  (NOSING) lazily, per word w, the exact constraint "fibre(w) != 1":
          for every matching M:  (M compatible with w) -> OR_{M' != M}
          z[w][M'],   z[w][M'] -> M' compatible with w.
          Every such clause is a logical consequence of the requirement, so
          adding them lazily keeps the final UNSAT a genuine exhaustion.

Only the -> direction is needed for thin/const/z because those variables occur
positively in the constraints they feed; the encoding therefore admits every
admissible template (completeness) and every model decodes to a template that
really satisfies the constraints (soundness) -- both checked at run time by
re-deciding every model with the independent numpy fibre engine.

Run: python3 w8_sat.py --m 15 [--rounds 200000] [--seconds 3600]
     python3 w8_sat.py --m 15 --collect 20     (enumerate zero-singleton
                                                templates instead of stopping)
"""

from __future__ import annotations

import argparse
import json
import sys
import time

import numpy as np

import w8_core as C
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Solver


class Encoding:
    def __init__(self, geo, m, solver_name="cadical153", style="counter",
                 bare=False):
        self.geo = geo
        self.m = m
        self.style = style
        self.pool = IDPool()
        self.clauses = []
        self.cell = [[self.pool.id(("c", e, k)) for k in range(9)]
                     for e in range(len(geo.edges))]
        self.present = [self.pool.id(("p", e)) for e in range(len(geo.edges))]
        for e in range(len(geo.edges)):
            self.clauses.append([-self.present[e]] + self.cell[e])
            for k in range(9):
                self.clauses.append([-self.cell[e][k], self.present[e]])
        if not bare:
            card = CardEnc.atmost(lits=self.present, bound=m, vpool=self.pool,
                                  encoding=EncType.seqcounter)
            self.clauses.extend([list(cl) for cl in card.clauses])

        # thin[e][side][r]: block e nonempty, supported in colour r at side
        self.thin = {}
        for e, (u, v) in enumerate(geo.edges):
            for side in range(2):
                for r in range(3):
                    t = self.pool.id(("t", e, side, r))
                    self.thin[(e, side, r)] = t
                    keep, drop = [], []
                    for k in range(9):
                        i, j = divmod(k, 3)
                        if (j if side == 1 else i) == r:
                            keep.append(self.cell[e][k])
                        else:
                            drop.append(self.cell[e][k])
                    self.clauses.append([-t] + keep)
                    for lit in drop:
                        self.clauses.append([-t, -lit])
        # (FIE)
        for p in ([] if bare else range(geo.size)):
            for r in range(3):
                literals = []
                for e in geo.incident[p]:
                    u, v = geo.edges[e]
                    side = 1 if u == p else 0      # the FAR endpoint's side
                    literals.append(self.thin[(e, side, r)])
                self.clauses.append(literals)
        # (CONST)
        self.const = {}
        for colour in ([] if bare else range(3)):
            literals = []
            for n, edges in enumerate(geo.matching_edges):
                d = self.pool.id(("d", colour, n))
                self.const[(colour, n)] = d
                literals.append(d)
                for e in edges:
                    self.clauses.append([-d, self.cell[e][4 * colour]])
            self.clauses.append(literals)

        self.solver = Solver(name=solver_name, bootstrap_with=self.clauses)
        self.log = []                 # every clause added after bootstrap
        self.added_words = set()
        self.nogood_clauses = 0
        self.zwords = {}

    def add(self, clause):
        self.log.append(list(clause))
        self.solver.add_clause(clause)

    def all_clauses(self):
        return [list(c) for c in self.clauses] + [list(c) for c in self.log]

    def cell_lit(self, e, i, j):
        return self.cell[e][3 * i + j]

    def ensure_z(self, w):
        """Define z[w][M] <-> (M is compatible with w) for all 105 matchings."""
        if w in self.zwords:
            return self.zwords[w]
        geo = self.geo
        word = geo.words[w]
        z = {}
        for n, edges in enumerate(geo.matching_edges):
            cellsel = []
            for e in edges:
                u, v = geo.edges[e]
                cellsel.append(self.cell_lit(e, word[u], word[v]))
            zn = self.pool.id(("z", w, n))
            z[n] = zn
            for lit in cellsel:
                self.add([-zn, lit])
            self.add([-lit for lit in cellsel] + [zn])
        self.zwords[w] = z
        return z

    def fibre_nogood(self, pairs):
        """Clause forbidding 'word w has exactly fibre F' for every (w, F)."""
        clause = []
        for w, fibre in pairs:
            z = self.ensure_z(w)
            fibre = set(fibre)
            for n in range(len(self.geo.matchings)):
                clause.append(-z[n] if n in fibre else z[n])
        self.add(clause)
        return len(clause)

    def word_constraint(self, w, style=None):
        """Add the exact 'fibre(w) != 1' constraint for one word (once).

        style 'counter' (default): z[M] <-> M compatible with w, plus a
        two-state sequential counter forcing (count >= 1) -> (count >= 2).
        style 'long': the original one clause per matching listing all the
        other matchings.  The two encodings are logically equivalent; both
        are kept so that runs can be cross-validated (encoding control).
        """
        if w in self.added_words:
            return 0
        self.added_words.add(w)
        style = style or self.style
        geo = self.geo
        word = geo.words[w]
        lits = {}
        for n, edges in enumerate(geo.matching_edges):
            cellsel = []
            for e in edges:
                u, v = geo.edges[e]
                cellsel.append(self.cell_lit(e, word[u], word[v]))
            lits[n] = cellsel
        z = self.ensure_z(w)
        added = 0
        if style == "long":
            for n in range(len(geo.matchings)):
                clause = [-lit for lit in lits[n]] + [z[k] for k in z if k != n]
                self.add(clause)
                added += 1
        else:
            s1prev = s2prev = None
            for n in range(len(geo.matchings)):
                s1 = self.pool.id(("s1", w, n))
                s2 = self.pool.id(("s2", w, n))
                self.add([-z[n], s1])
                if s1prev is not None:
                    self.add([-s1prev, s1])
                    self.add([-s1, s1prev, z[n]])
                    self.add([-s2, s2prev, z[n]])
                    self.add([-s2, s2prev, s1prev])
                else:
                    self.add([-s1, z[n]])
                    self.add([-s2])
                added += 5
                s1prev, s2prev = s1, s2
            self.add([-s1prev, s2prev])
            added += 1
        self.nogood_clauses += added
        return added

    def decode(self, model):
        positive = {lit for lit in model if lit > 0}
        template = []
        for e in range(len(self.geo.edges)):
            mask = 0
            for k in range(9):
                if self.cell[e][k] in positive:
                    mask |= 1 << k
            template.append(mask)
        return tuple(template)

    def block(self, template):
        """Block one exact template (used only in --collect mode)."""
        clause = []
        for e, mask in enumerate(template):
            for k in range(9):
                if (mask >> k) & 1:
                    clause.append(-self.cell[e][k])
                else:
                    clause.append(self.cell[e][k])
        self.add(clause)


def near_constant_words(geo, radius=2):
    """Words with at most `radius` sites off the majority colour."""
    out = []
    for w in range(len(geo.words)):
        word = geo.words[w]
        best = min(8 - word.count(c) for c in range(3))
        if 1 <= best <= radius:
            out.append(w)
    return out


def run(m, seconds, rounds, collect, solver_name, seed_words, style="counter"):
    geo = C.geometry(8)
    enc = Encoding(geo, m, solver_name, style)
    for w in seed_words:
        enc.word_constraint(w)
    start = time.time()
    found = []
    stats = {"m": m, "rounds": 0, "words_constrained": len(enc.added_words),
             "solver": solver_name}
    while True:
        if time.time() - start > seconds:
            stats["status"] = "timeout"
            break
        if enc.solver.solve() is False:
            stats["status"] = "UNSAT"
            break
        stats["rounds"] += 1
        if stats["rounds"] > rounds:
            stats["status"] = "round-limit"
            break
        template = enc.decode(enc.solver.get_model())
        compat = C.compat_matrix(geo, template)
        sizes = compat.sum(axis=0, dtype=np.int64)
        # independent re-check of the encoded constraints
        assert C.fie_ok(geo, template), "encoding unsound: FIE"
        assert C.constants_ok(geo, template, compat), "encoding unsound: const"
        assert C.support(template) <= m, "encoding unsound: support"
        bad = np.nonzero((sizes == 1) & geo.mixed)[0]
        if len(bad) == 0:
            found.append(template)
            print(f"  [{time.time()-start:7.1f}s] round {stats['rounds']}: "
                  f"ZERO-SINGLETON template, support {C.support(template)}, "
                  f"Sigma {C.sigma(template)}", flush=True)
            if len(found) >= collect:
                stats["status"] = "found"
                break
            enc.block(template)
            continue
        # add the exact word constraints for a batch of violated words
        order = sorted(int(x) for x in bad)
        for w in order[:32]:
            enc.word_constraint(w)
        if stats["rounds"] % 25 == 0:
            print(f"  [{time.time()-start:7.1f}s] round {stats['rounds']}: "
                  f"support {C.support(template)}, Sigma {C.sigma(template)}, "
                  f"{len(bad)} singleton words, "
                  f"{len(enc.added_words)} words constrained, "
                  f"{enc.nogood_clauses} nogood clauses", flush=True)
    stats["words_constrained"] = len(enc.added_words)
    stats["nogood_clauses"] = enc.nogood_clauses
    stats["seconds"] = round(time.time() - start, 1)
    stats["found"] = [list(t) for t in found]
    return stats


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--m", type=int, default=15)
    parser.add_argument("--seconds", type=float, default=1800.0)
    parser.add_argument("--rounds", type=int, default=10 ** 6)
    parser.add_argument("--collect", type=int, default=1)
    parser.add_argument("--solver", default="cadical153")
    parser.add_argument("--out", default=None)
    parser.add_argument("--style", default="counter")
    parser.add_argument("--seed-radius", type=int, default=2)
    args = parser.parse_args()
    print(f"UNAUDITED PROBE (W8) -- admissible zero-singleton SAT, "
          f"support <= {args.m}", flush=True)
    geo = C.geometry(8)
    seeds = near_constant_words(geo, args.seed_radius) if args.seed_radius else []
    print(f"seeding {len(seeds)} near-constant words, style {args.style}",
          flush=True)
    stats = run(args.m, args.seconds, args.rounds, args.collect, args.solver,
                seed_words=seeds, style=args.style)
    print(json.dumps({k: v for k, v in stats.items() if k != "found"},
                     indent=1))
    name = args.out or f"results_sat_m{args.m}.json"
    with open(name, "w") as handle:
        json.dump(stats, handle, indent=1)
    print(f"wrote {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
