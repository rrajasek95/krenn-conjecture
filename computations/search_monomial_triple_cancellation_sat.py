#!/usr/bin/env python3
"""CEGAR search for a cubic-root monomial Krenn counterexample.

This is a discovery tool, not by itself a proof.  Fix three edge-disjoint
perfect matchings and label them by the three constant colors.  Every other
underlying pair is absent or has one ordered endpoint-color label.  We ask
that each constant coloring have exactly its fixed matching and that the
number of matchings in every mixed coloring fiber be divisible by three.

The latter condition is necessary for cancellation by third roots of unity:
if every edge weight is a power of omega, then a sum of matching weights can
vanish only when the three phase multiplicities agree.  Constraints are
added lazily, one violated coloring fiber at a time.
"""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations, permutations, product

from pysat.solvers import Solver


Q = 3
ABSENT = 0


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for k in range(1, len(vertices)):
        v = vertices[k]
        rest = vertices[1:k] + vertices[k + 1 :]
        for tail in perfect_matchings(rest):
            yield tuple(sorted(((u, v),) + tail))


def canonical_matching(n: int):
    return tuple((2 * k, 2 * k + 1) for k in range(n // 2))


def stabilizer_of_canonical_matching(n: int):
    h = n // 2
    for pair_perm in permutations(range(h)):
        for flips in product(range(2), repeat=h):
            p = [0] * n
            for k in range(h):
                for bit in range(2):
                    p[2 * k + bit] = 2 * pair_perm[k] + (bit ^ flips[k])
            yield tuple(p)


def relabel_matching(matching, p):
    return tuple(sorted((min(p[u], p[v]), max(p[u], p[v])) for u, v in matching))


def target_orbits(n: int):
    vertices = tuple(range(n))
    matchings = tuple(perfect_matchings(vertices))
    p0 = canonical_matching(n)
    p0s = set(p0)
    stabilizer = tuple(stabilizer_of_canonical_matching(n))

    def canonical_pair(p1, p2):
        forms = []
        for p in stabilizer:
            q1, q2 = relabel_matching(p1, p), relabel_matching(p2, p)
            forms.extend(((q1, q2), (q2, q1)))
        return min(forms)

    reps = {
        canonical_pair(p1, p2)
        for p1 in matchings
        if not p0s.intersection(p1)
        for p2 in matchings
        if not p0s.intersection(p2) and not set(p1).intersection(p2)
    }
    return tuple((p0,) + pair for pair in sorted(reps))


class Pool:
    def __init__(self):
        self.top = 0

    def new(self):
        self.top += 1
        return self.top


def state_for(a: int, b: int):
    return 1 + Q * a + b


class Search:
    def __init__(self, n: int, targets):
        self.n = n
        self.vertices = tuple(range(n))
        self.edges = tuple(combinations(self.vertices, 2))
        self.edge_index = {e: i for i, e in enumerate(self.edges)}
        self.matchings = tuple(perfect_matchings(self.vertices))
        self.pool = Pool()
        self.solver = Solver(name="cadical195")
        self.state = [[self.pool.new() for _ in range(1 + Q * Q)] for _ in self.edges]
        for variables in self.state:
            self.solver.add_clause(variables)
            for x, y in combinations(variables, 2):
                self.solver.add_clause([-x, -y])
        for color, matching in enumerate(targets):
            for edge in matching:
                self.solver.add_clause([
                    self.state[self.edge_index[edge]][state_for(color, color)]
                ])
        self.constrained: set[tuple[int, ...]] = set()

    def witnesses(self, coloring: tuple[int, ...]):
        answer = []
        for matching in self.matchings:
            required = [
                self.state[self.edge_index[e]][state_for(coloring[e[0]], coloring[e[1]])]
                for e in matching
            ]
            w = self.pool.new()
            for s in required:
                self.solver.add_clause([-w, s])
            self.solver.add_clause([w] + [-s for s in required])
            answer.append(w)
        return answer

    def constrain(self, coloring: tuple[int, ...]):
        if coloring in self.constrained:
            return
        self.constrained.add(coloring)
        ws = self.witnesses(coloring)
        if len(set(coloring)) == 1:
            # The fixed target matching is already true, so exact multiplicity
            # one is simply pairwise at-most-one.
            for x, y in combinations(ws, 2):
                self.solver.add_clause([-x, -y])
            return

        # Deterministic modulo-three counter.  r[i,k] means the first i
        # witnesses have sum k mod 3.
        previous = [self.pool.new() for _ in range(3)]
        self.solver.add_clause([previous[0]])
        self.solver.add_clause([-previous[1]])
        self.solver.add_clause([-previous[2]])
        for w in ws:
            following = [self.pool.new() for _ in range(3)]
            self.solver.add_clause(following)
            for x, y in combinations(following, 2):
                self.solver.add_clause([-x, -y])
            for old in range(3):
                for bit in range(2):
                    valid = (old + bit) % 3
                    for new in range(3):
                        if new == valid:
                            continue
                        # Forbid previous[old] & (w == bit) & following[new].
                        self.solver.add_clause(
                            [-previous[old], -w if bit else w, -following[new]]
                        )
            previous = following
        self.solver.add_clause([previous[0]])

    def decode(self, model):
        positive = {x for x in model if x > 0}
        return tuple(
            next(s for s, variable in enumerate(variables) if variable in positive)
            for variables in self.state
        )

    def fibers(self, states):
        ans = Counter()
        members = {}
        for number, matching in enumerate(self.matchings):
            coloring = [-1] * self.n
            supported = True
            for u, v in matching:
                s = states[self.edge_index[u, v]]
                if s == ABSENT:
                    supported = False
                    break
                coloring[u], coloring[v] = divmod(s - 1, Q)
            if supported:
                key = tuple(coloring)
                ans[key] += 1
                members.setdefault(key, []).append(number)
        return ans, members

    def run(self, max_rounds: int):
        for color in range(Q):
            self.constrain((color,) * self.n)
        for round_number in range(max_rounds):
            if not self.solver.solve():
                return None, round_number
            states = self.decode(self.solver.get_model())
            fibers, members = self.fibers(states)
            bad = [
                c for c, count in fibers.items()
                if (len(set(c)) == 1 and count != 1)
                or (len(set(c)) > 1 and count % 3 != 0)
            ]
            if not bad:
                return (states, fibers, members), round_number
            # Add several of the sparsest violations per round; singleton
            # clauses are particularly informative.
            bad.sort(key=lambda c: (fibers[c], c))
            for coloring in bad[:32]:
                self.constrain(coloring)
            if round_number % 10 == 0:
                print(
                    f"round={round_number} fibers={len(fibers)} bad={len(bad)} "
                    f"constrained={len(self.constrained)} vars={self.pool.top}",
                    flush=True,
                )
        return None, max_rounds


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=8)
    parser.add_argument("--orbit", type=int)
    parser.add_argument(
        "--cyclic10",
        action="store_true",
        help="use one pairwise-Hamilton triple on ten vertices",
    )
    parser.add_argument("--max-rounds", type=int, default=1000)
    args = parser.parse_args()
    if args.cyclic10:
        if args.n != 10:
            raise SystemExit("--cyclic10 requires --n 10")
        orbits = ((
            ((0, 1), (2, 3), (4, 5), (6, 7), (8, 9)),
            ((0, 9), (1, 2), (3, 4), (5, 6), (7, 8)),
            ((0, 2), (1, 4), (3, 6), (5, 8), (7, 9)),
        ),)
    else:
        orbits = target_orbits(args.n)
    indices = range(len(orbits)) if args.orbit is None else (args.orbit,)
    print(f"n={args.n} target_orbits={len(orbits)}", flush=True)
    for orbit in indices:
        print(f"orbit={orbit} targets={orbits[orbit]}", flush=True)
        search = Search(args.n, orbits[orbit])
        result, rounds = search.run(args.max_rounds)
        if result is None:
            status = "UNSAT" if rounds < args.max_rounds else "LIMIT"
            print(f"orbit={orbit} {status} after {rounds} rounds", flush=True)
            continue
        states, fibers, _members = result
        print(
            f"orbit={orbit} SAT rounds={rounds} distribution="
            f"{dict(sorted(Counter(fibers.values()).items()))}"
        )
        for edge, state in zip(search.edges, states):
            if state:
                print(edge, divmod(state - 1, Q))
        return


if __name__ == "__main__":
    main()
