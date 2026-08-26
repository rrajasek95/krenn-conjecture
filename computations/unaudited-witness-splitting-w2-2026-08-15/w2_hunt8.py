#!/usr/bin/env python3
"""UNAUDITED PROBE (W2) -- adversarial hunt at eight sites (task D).

Pinned HEAD: 26ba69f7e643694c6a58464af6e9e1de9ec92f01

TARGET.  A coordinate template on eight sites with

    support >= 18 edges,
    every constant fibre nonempty,
    NO mixed singleton fibre,
    NO odd holonomy and no one-live-class collapse (the committed O1/O2
    oracle, in the closure form of w2_monomial.analyse).

Such a template would be a source no committed mechanism kills: it sharpens
the counterexample portrait and redirects lemma J.2.

METHOD.  The "no mixed singleton" condition is the committed SAT encoding of
computations/search_monomial_no_singleton_sat.py (build_formula), which fixes
three edge-disjoint constant matchings and is exact for that condition.  We
add an at-most-k cardinality bound on ABSENT edges (support >= 28 - k) and
enumerate models; each model is decided exactly by the O1/O2 closure engine.

Two blocking modes:
  --mode hunt    block the exact model (sound for search, not exhaustion);
  --mode exhaust block an EXACT nogood: the certificate's cells must all be
                 present AND no further matching may join the certificate's
                 fibres.  The second half needs one auxiliary variable per
                 (matching, involved colouring) with t -> "all labels of that
                 colouring present", so setting t true genuinely exhibits an
                 extra term.  UNSAT in this mode is a real exhaustion.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
import random
import sys
import time

from w2_monomial import Q, analyse, fibre_profile, geometry, is_mixed

sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations")
from search_monomial_no_singleton_sat import (ABSENT, build_formula,  # noqa: E402
                                              colored_triple_orbits, edge_state)
from pysat.card import CardEnc, EncType  # noqa: E402
from pysat.formula import IDPool  # noqa: E402
from pysat.solvers import Solver  # noqa: E402


def decode(model, state):
    positive = {literal for literal in model if literal > 0}
    return [next(value for value, variable in enumerate(row)
                 if variable in positive) for row in state]


def to_labels(states):
    return [None if value == ABSENT else divmod(value - 1, Q) for value in states]


class Hunt:
    def __init__(self, size, targets, min_support, mode):
        self.geo = geometry(size)
        self.size = size
        self.mode = mode
        (top, clauses, self.state, self.edges, self.edge_index,
         self.matchings) = build_formula(size, targets)
        self.pool = IDPool(start_from=top + 1)
        absent = [self.state[index][ABSENT] for index in range(len(self.edges))]
        bound = len(self.edges) - min_support
        card = CardEnc.atmost(lits=absent, bound=bound, vpool=self.pool,
                              encoding=EncType.seqcounter)
        clauses = list(clauses) + [list(c) for c in card.clauses]
        self.solver = Solver(name="cadical195", bootstrap_with=clauses)
        self.joiner: dict[tuple[int, tuple[int, ...]], int] = {}

    def join_variable(self, number, colouring):
        """t -> matching `number` carries exactly the labels of `colouring`."""
        key = (number, colouring)
        if key in self.joiner:
            return self.joiner[key]
        variable = self.pool.id(("join", number, colouring))
        for u, v in self.matchings[number]:
            literal = self.state[self.edge_index[(u, v)]][
                edge_state((colouring[u], colouring[v]))]
            self.solver.add_clause([-variable, literal])
        self.joiner[key] = variable
        return variable

    def cells_of(self, number, colouring):
        return [self.state[self.edge_index[(u, v)]][
            edge_state((colouring[u], colouring[v]))]
            for u, v in self.matchings[number]]

    def block_exact_model(self, states):
        self.solver.add_clause([-self.state[index][value]
                                for index, value in enumerate(states)])

    def block_certificate(self, table, involved):
        """involved: list of colourings whose EXACT term sets are used."""
        literals = set()
        for colouring in involved:
            for number in table[colouring]:
                literals.update(self.cells_of(number, colouring))
        clause = [-literal for literal in literals]
        members = {colouring: set(table[colouring]) for colouring in involved}
        for colouring in involved:
            for number in range(len(self.matchings)):
                if number in members[colouring]:
                    continue
                clause.append(self.join_variable(number, colouring))
        self.solver.add_clause(clause)

    def involved_words(self, table, verdict):
        if verdict["verdict"] == "O2-literal-singleton":
            return [tuple(verdict["words"][0])]
        if verdict["verdict"] == "O2-one-live-class":
            # The class computation used the whole binomial lattice; be safe
            # and pin every binomial fibre plus the collapsed one.
            return [tuple(verdict["word"])] + [
                c for c, m in table.items() if is_mixed(c) and len(m) == 2]
        if verdict["verdict"] == "O1-odd-holonomy":
            if "words" in verdict:
                return [tuple(w) for w in verdict["words"]]
            return [c for c, m in table.items() if is_mixed(c) and len(m) == 2]
        if verdict["verdict"] == "K3-pure-vanishing":
            return [tuple(verdict["colour"])] + [
                c for c, m in table.items() if is_mixed(c) and len(m) == 2]
        return [c for c in table]

    def run(self, rounds, log_every=25):
        verdicts = Counter()
        survivors = []
        histograms = Counter()
        supports = Counter()
        models = []
        start = time.time()
        for round_number in range(rounds):
            if not self.solver.solve():
                return {"status": "UNSAT", "rounds": round_number,
                        "verdicts": dict(verdicts), "survivors": survivors,
                        "models": models,
                        "mixed_histograms": {str(dict(k)): v
                                             for k, v in histograms.items()},
                        "supports": {str(k): v for k, v in supports.items()},
                        "seconds": round(time.time() - start, 1)}
            states = decode(self.solver.get_model(), self.state)
            labels = to_labels(states)
            support = sum(1 for label in labels if label is not None)
            supports[support] += 1
            verdict = analyse(self.geo, labels)
            verdicts[verdict["verdict"]] += 1
            models.append({"support": support, "verdict": verdict["verdict"],
                           "labels": [list(x) if x else None for x in labels]})
            from w2_monomial import fibres
            table = fibres(self.geo, labels)
            _singles, histogram = fibre_profile(table)
            histograms[tuple(sorted(histogram.items()))] += 1
            if verdict["verdict"] == "survivor":
                survivors.append({
                    "support": support,
                    "labels": [list(x) if x else None for x in labels],
                    "edges": [list(e) for e in self.edges],
                    "mixed_histogram": {str(k): v for k, v in histogram.items()},
                    "detail": {k: v for k, v in verdict.items()
                               if k != "fibres"},
                })
                print(f"  *** SURVIVOR at round {round_number}, support "
                      f"{support}, mixed histogram {dict(histogram)}",
                      flush=True)
            if self.mode == "hunt":
                self.block_exact_model(states)
            else:
                self.block_certificate(table, self.involved_words(table, verdict))
            if round_number % log_every == 0:
                print(f"  round={round_number} support={support} "
                      f"verdict={verdict['verdict']} hist={dict(histogram)} "
                      f"({time.time() - start:.0f}s)", flush=True)
        return {"status": "rounds-exhausted", "rounds": rounds,
                "verdicts": dict(verdicts), "survivors": survivors,
                "models": models,
                "mixed_histograms": {str(dict(k)): v for k, v in histograms.items()},
                "supports": {str(k): v for k, v in supports.items()},
                "seconds": round(time.time() - start, 1)}


def sample_profile(size, targets, trials, min_support, seed):
    """Random templates: how many mixed words have singleton fibres?"""
    geo = geometry(size)
    rng = random.Random(seed)
    base = [None] * len(geo.edges)
    used = set()
    for colour, matching in enumerate(targets):
        for edge in matching:
            base[geo.index[edge]] = (colour, colour)
            used.add(geo.index[edge])
    free = [e for e in range(len(geo.edges)) if e not in used]
    rows = Counter()
    zero_singleton = 0
    from w2_monomial import fibres
    for _ in range(trials):
        extra = rng.randint(max(0, min_support - len(used)), len(free))
        chosen = rng.sample(free, extra)
        labels = list(base)
        for index in chosen:
            labels[index] = (rng.randrange(Q), rng.randrange(Q))
        support = len(used) + extra
        table = fibres(geo, labels)
        if any(not table.get(tuple([r] * size)) for r in range(Q)):
            continue
        singles, _ = fibre_profile(table)
        rows[(support, singles)] += 1
        if singles == 0:
            zero_singleton += 1
    return rows, zero_singleton


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=8)
    parser.add_argument("--min-support", type=int, default=18)
    parser.add_argument("--rounds", type=int, default=400)
    parser.add_argument("--mode", choices=("hunt", "exhaust"), default="hunt")
    parser.add_argument("--orbit", type=int)
    parser.add_argument("--sample", type=int, default=0)
    parser.add_argument("--out", default="hunt8.json")
    args = parser.parse_args()

    print(f"UNAUDITED PROBE (W2) -- n={args.n} hunt, HEAD 26ba69f, "
          f"mode={args.mode}, support>={args.min_support}", flush=True)
    orbits = colored_triple_orbits(args.n)
    print(f"colored triple orbits: {len(orbits)}", flush=True)
    indices = range(len(orbits)) if args.orbit is None else [args.orbit]
    report = {"min_support": args.min_support, "mode": args.mode,
              "orbits": len(orbits), "results": {}}

    if args.sample:
        profile = {}
        for index in indices:
            rows, zeros = sample_profile(args.n, orbits[index], args.sample,
                                         args.min_support, 900 + index)
            profile[f"orbit{index}"] = {
                "zero_singleton_templates": zeros,
                "rows": {f"{s}:{k}": v for (s, k), v in sorted(rows.items())},
            }
            worst = min((k for (s, k) in rows), default=None)
            print(f"orbit{index}: sampled {sum(rows.values())} valid, "
                  f"min singleton count = {worst}, zero-singleton = {zeros}",
                  flush=True)
        report["sampling"] = profile

    for index in indices:
        print(f"orbit {index}: targets={orbits[index]}", flush=True)
        hunt = Hunt(args.n, orbits[index], args.min_support, args.mode)
        result = hunt.run(args.rounds)
        report["results"][f"orbit{index}"] = result
        print(f"orbit {index}: {result['status']} rounds={result['rounds']} "
              f"verdicts={result['verdicts']} "
              f"survivors={len(result['survivors'])} "
              f"({result['seconds']}s)", flush=True)
        with open(args.out, "w") as handle:
            json.dump(report, handle, indent=1)


if __name__ == "__main__":
    main()
