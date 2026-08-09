#!/usr/bin/env python3
"""Exact full-fibre completion search above the corrected sharp N=8 seed.

The fixed 16-cell seed consists of a chart-26 pure matching triple and the
off-diagonal mate which cancels the formerly misidentified "sharp
trinomial" word.  Optional cells range over all 252 endpoint-colour cells.
For every mixed word, all 105 physical perfect matchings are considered.

The lazy clauses are projection-exact for the support condition

    number of supported terms in every mixed fibre is 0 or at least 2.

At a fixed cell cap, infeasible and non-minimal mate requirements are removed
without changing that projection.  Therefore UNSAT is a rigorous bounded
support obstruction and NO_SINGLETON is an explicit semantic survivor.  No
claim about the coefficient equations is made by this support-only program.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict

import search_n8_sparse_triple_completion as sparse
import verify_monomial_n8_counterexample as diagonal_guard
import verify_n8_target_triple_localization_orbits as charts


N = 8
Q = 3

ANCHORS = (
    ((0, 1), (2, 3), (4, 5), (6, 7)),
    ((0, 2), (1, 4), (3, 6), (5, 7)),
    ((0, 3), (1, 5), (2, 7), (4, 6)),
)

# On word 00002121, these four off-diagonal cells support the mate
# 04|15|26|37.  Give 04;02 weight -1 and every other displayed seed cell
# weight +1 to cancel the anchor term 01|23|46|57 exactly.
OFFDIAGONAL_MATE = frozenset({
    (0, 4, 0, 2),
    (1, 5, 0, 1),
    (2, 6, 0, 2),
    (3, 7, 0, 1),
})

SEED = frozenset(
    (left, right, colour, colour)
    for colour, matching in enumerate(ANCHORS)
    for left, right in matching
) | OFFDIAGONAL_MATE

SHARP_WORD = (0, 0, 0, 0, 2, 1, 2, 1)
SHARP_MATCHINGS = frozenset({
    ((0, 1), (2, 3), (4, 6), (5, 7)),
    ((0, 4), (1, 5), (2, 6), (3, 7)),
})


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def chart_index(triple) -> int:
    """Return the exact 1-based S8 x S3 localization-chart index."""

    mate = [-1] * (3 * N)
    for colour, matching in enumerate(triple):
        for left, right in matching:
            first, second = 3 * left + colour, 3 * right + colour
            mate[first] = second
            mate[second] = first
    require(all(port >= 0 for port in mate), "anchor triple lost a port")
    rows = tuple(sorted(charts.SOURCE.target_orbit_rows()))
    return rows.index(charts.SOURCE.canonical_key(tuple(mate))) + 1


class TightNoSingletonSearch(sparse.SparseCompletionSearch):
    """Cap-aware exact no-singleton CEGAR for the fixed sharp seed."""

    def __init__(self, cap: int, solver_name: str):
        self.cell_cap = cap
        super().__init__(
            cap,
            solver_name,
            orbit=1,
            seed_cells=SEED,
        )

    def add_singleton_gadget(self, colouring, trigger_number):
        """Require one feasible inclusion-minimal mate for the trigger."""

        key = colouring, trigger_number
        if key in self.singleton_gadgets:
            return False
        trigger = frozenset(self.terms(colouring)[trigger_number])
        requirements = set()
        for number, decorated in enumerate(self.terms(colouring)):
            if number == trigger_number:
                continue
            requirement = frozenset(decorated) - trigger
            if len(self.seed | trigger | requirement) <= self.cell_cap:
                requirements.add(requirement)
        requirements = {
            requirement
            for requirement in requirements
            if not any(smaller < requirement for smaller in requirements)
        }

        selectors = []
        new_variables = []
        for requirement in sorted(
            requirements, key=lambda value: (len(value), sorted(value))
        ):
            selector = self.pool.new()
            selectors.append(selector)
            new_variables.append(selector)
            for cell in requirement:
                self.solver.add_clause([-selector, self.support[cell]])
        # An empty selector list is the desired contradiction when no mate
        # fits under the global cell cap.
        self.solver.add_clause(
            [-self.support[cell] for cell in sorted(trigger)] + selectors
        )
        self.solver.set_phases([-variable for variable in new_variables])
        self.singleton_gadgets.add(key)
        return True


def audit_seed() -> None:
    require(len(SEED) == 16, "sharp seed size changed")
    matchings = tuple(sparse.toric.perfect_matchings(tuple(range(N))))
    require(len(matchings) == 105, "physical matching count changed")
    fibres = sparse.toric.exact_fibres(N, SEED, matchings)
    histogram = Counter(
        len(terms)
        for word, terms in fibres.items()
        if len(set(word)) > 1
    )
    require(histogram == Counter({1: 11, 2: 1}),
            "sharp-seed full mixed histogram changed")
    sharp_terms = fibres[SHARP_WORD]
    require(len(sharp_terms) == 2, "sharp word is not a full binomial")
    require(
        frozenset(
            tuple(sorted((cell[0], cell[1]) for cell in term[1]))
            for term in sharp_terms
        )
        == SHARP_MATCHINGS,
        "sharp word lost its off-diagonal physical mate",
    )
    pure_sizes = tuple(len(fibres[(colour,) * N]) for colour in range(Q))
    require(pure_sizes == (1, 1, 1), "pure anchors changed")
    require(chart_index(ANCHORS) == 26, "sharp anchors left chart 26")

    # The familiar 28-cell diagonal no-singleton guard does not secretly
    # settle this chart.  Its 24*1*4 choices of pure anchor monomials occupy
    # exactly charts 28--31, with the multiplicities below.
    pure_matchings = defaultdict(list)
    for matching in diagonal_guard.MATCHINGS:
        word = diagonal_guard.induced_coloring(matching)
        if len(set(word)) == 1:
            pure_matchings[word[0]].append(matching)
    diagonal_chart_census = Counter(
        chart_index((first, second, third))
        for first in pure_matchings[0]
        for second in pure_matchings[1]
        for third in pure_matchings[2]
    )
    require(
        diagonal_chart_census == Counter({28: 16, 29: 32, 30: 16, 31: 32}),
        "diagonal no-singleton chart census changed",
    )
    print("seed cells: 16")
    print("localized anchor chart: 26")
    print("physical perfect matchings per word: 105")
    print("mixed fibre histogram:", dict(sorted(histogram.items())))
    print("sharp word terms: 01|23|46|57 and 04|15|26|37")
    print("weights: anchor=+1, mate=+1 except 04;02=-1")
    print("known diagonal guard charts:", dict(sorted(diagonal_chart_census.items())))


def analyze_coefficients(instance, selected, fibres) -> None:
    """Apply the first exact coefficient guard to a semantic survivor."""

    mixed, rows = sparse.binomial_system(instance, fibres)
    consistent, _lattice = sparse.toric.signed_quotient_lattice(
        rows, len(instance.cells)
    )
    triangles = sparse.toric_search.unit_triangle_circuits(rows)
    print(
        f"coefficient guard: binomials={len(rows)} "
        f"signed_laurent_consistent={consistent} "
        f"unit_odd_triangles={len(triangles)}"
    )
    if triangles:
        words = tuple(mixed[index][0] for index in triangles[0])
        print("first exact odd-Laurent circuit words:", words)
    elif consistent:
        print(
            "coefficient frontier: reduce the >=3-term equations in the "
            "signed Laurent quotient, then seek a smooth F_p torus point"
        )


def search(cap: int, solver_name: str, max_rounds: int):
    require(cap >= len(SEED), "cell cap is smaller than the fixed seed")
    instance = TightNoSingletonSearch(cap, solver_name)
    try:
        for round_number in range(max_rounds):
            if not instance.solver.solve():
                print(
                    f"UNSAT cap={cap} rounds={round_number} "
                    f"singleton_gadgets={len(instance.singleton_gadgets)}"
                )
                return None
            selected = instance.decode(instance.solver.get_model())
            fibres = sparse.exact_fibres(instance, selected)
            singletons = [
                (word, terms[0][0])
                for word, terms in sorted(fibres.items())
                if len(set(word)) > 1 and len(terms) == 1
            ]
            if not singletons:
                histogram = Counter(
                    len(terms)
                    for word, terms in fibres.items()
                    if len(set(word)) > 1
                )
                print(
                    f"NO_SINGLETON cap={cap} round={round_number} "
                    f"cells={len(selected)} "
                    f"histogram={dict(sorted(histogram.items()))}"
                )
                print("EXTRA", sorted(selected - SEED))
                analyze_coefficients(instance, selected, fibres)
                return selected
            for word, trigger_number in singletons:
                require(
                    instance.add_singleton_gadget(word, trigger_number),
                    "a semantic singleton repeated after its exact gadget",
                )
            if round_number < 20 or round_number % 20 == 0:
                print(
                    f"round={round_number} cells={len(selected)} "
                    f"singletons={len(singletons)} "
                    f"gadgets={len(instance.singleton_gadgets)}",
                    flush=True,
                )
        print(
            f"BOUNDARY cap={cap} rounds={max_rounds} "
            f"singleton_gadgets={len(instance.singleton_gadgets)}"
        )
        return None
    finally:
        instance.delete()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit-seed", action="store_true")
    parser.add_argument("--cap", type=int, default=25)
    parser.add_argument("--solver", default="glucose42")
    parser.add_argument("--max-rounds", type=int, default=10000)
    args = parser.parse_args()
    audit_seed()
    if not args.audit_seed:
        search(args.cap, args.solver, args.max_rounds)


if __name__ == "__main__":
    main()
