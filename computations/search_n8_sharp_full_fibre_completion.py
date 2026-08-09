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
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.solvers import Solver
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

EXPECTED_DIRECT_FRONTIER_SHA256 = (
    "96d9883ab36adbbbba87f7b4de92d078694d70f5ec392469b69cf994931eb97a"
)


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

    def __init__(self, cap: int, solver_name: str, resume_prefix=None):
        self.cell_cap = cap
        self.pool = sparse.toric.Pool()
        self.cells = tuple(
            (left, right, left_colour, right_colour)
            for left, right in combinations(range(N), 2)
            for left_colour, right_colour in product(range(Q), repeat=2)
        )
        self.cell_index = {
            cell: index for index, cell in enumerate(self.cells)
        }
        self.support = {cell: self.pool.new() for cell in self.cells}
        self.matchings = tuple(
            sparse.toric.perfect_matchings(tuple(range(N)))
        )
        self.orbit = 1
        self.seed = SEED
        self.forbidden = frozenset()
        self._terms = {}
        self.singleton_gadgets = set()
        self.core_gadgets = set()
        self.term_variables = {}
        self.zero_product_cuts = 0

        if resume_prefix is None:
            clauses = [[self.support[cell]] for cell in sorted(self.seed)]
            cardinality = CardEnc.atmost(
                lits=[self.support[cell] for cell in self.cells],
                bound=cap,
                top_id=self.pool.top,
                encoding=EncType.kmtotalizer,
            )
            self.pool.top = cardinality.nv
            clauses.extend(cardinality.clauses)
            self.hard_clauses = [tuple(clause) for clause in clauses]
        else:
            self.hard_clauses = self._read_dimacs(
                Path(resume_prefix).with_suffix(".cnf")
            )
            manifest = json.loads(
                Path(resume_prefix).with_suffix(".json").read_text()
            )
            require(manifest["cap"] == cap, "checkpoint cap changed")
            require(manifest["seed"] == [list(cell) for cell in sorted(SEED)],
                    "checkpoint seed changed")
            self.pool.top = manifest["variables"]
            self.singleton_gadgets = {
                (tuple(word), trigger)
                for word, trigger in manifest["singleton_gadgets"]
            }

        self.solver = Solver(
            name=solver_name, bootstrap_with=self.hard_clauses
        )
        self.solver.set_phases([
            self.support[cell] if cell in self.seed else -self.support[cell]
            for cell in self.cells
        ])

    @staticmethod
    def _read_dimacs(path: Path):
        clauses = []
        pending = []
        for line in path.read_text().splitlines():
            if not line or line[0] in "cp":
                continue
            for token in line.split():
                literal = int(token)
                if literal:
                    pending.append(literal)
                else:
                    clauses.append(tuple(pending))
                    pending = []
        require(not pending, "checkpoint DIMACS has unterminated clause")
        return clauses

    def add_hard_clause(self, clause) -> None:
        clause = tuple(clause)
        self.solver.add_clause(clause)
        self.hard_clauses.append(clause)

    def write_checkpoint(self, prefix: str) -> None:
        """Persist a solver-independent CNF plus semantic resume manifest."""

        base = Path(prefix)
        cnf_path = base.with_suffix(".cnf")
        manifest_path = base.with_suffix(".json")
        cnf_temporary = cnf_path.with_suffix(".cnf.tmp")
        manifest_temporary = manifest_path.with_suffix(".json.tmp")
        with cnf_temporary.open("w") as stream:
            stream.write(f"p cnf {self.pool.top} {len(self.hard_clauses)}\n")
            for clause in self.hard_clauses:
                stream.write(" ".join(map(str, clause)) + " 0\n")
        manifest = {
            "cap": self.cell_cap,
            "variables": self.pool.top,
            "clauses": len(self.hard_clauses),
            "seed": [list(cell) for cell in sorted(SEED)],
            "singleton_gadgets": [
                [list(word), trigger]
                for word, trigger in sorted(self.singleton_gadgets)
            ],
        }
        manifest_temporary.write_text(
            json.dumps(manifest, sort_keys=True, separators=(",", ":"))
            + "\n"
        )
        cnf_temporary.replace(cnf_path)
        manifest_temporary.replace(manifest_path)

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
                self.add_hard_clause([-selector, self.support[cell]])
        # An empty selector list is the desired contradiction when no mate
        # fits under the global cell cap.
        self.add_hard_clause(
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
    seed_stabilizer = sum(
        {
            sparse.signed.image_cell(cell, vertex_permutation,
                                     colour_permutation)
            for cell in SEED
        } == SEED
        for vertex_permutation in permutations(range(N))
        for colour_permutation in permutations(range(Q))
    )
    require(seed_stabilizer == 1, "corrected seed stabilizer changed")

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
    print("corrected seed stabilizer in S8 x S3: 1")
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


def supported_fibres(selected, matchings):
    """Enumerate only terms supported by a sparse endpoint-coloured chart."""

    pair_options = defaultdict(list)
    for left, right, left_colour, right_colour in selected:
        pair_options[left, right].append(
            (left_colour, right_colour,
             (left, right, left_colour, right_colour))
        )
    fibres = defaultdict(list)
    for matching_number, matching in enumerate(matchings):
        options = [pair_options[pair] for pair in matching]
        if not all(options):
            continue
        for choice in product(*options):
            word = [-1] * N
            decorated = []
            for (left, right), (left_colour, right_colour, cell) in zip(
                matching, choice
            ):
                word[left] = left_colour
                word[right] = right_colour
                decorated.append(cell)
            fibres[tuple(word)].append(
                (matching_number, tuple(decorated))
            )
    return fibres


def minimal_mate_requirements(instance, word, trigger_number, fixed,
                              maximum_size=None):
    trigger = frozenset(instance.terms(word)[trigger_number])
    requirements = {
        frozenset(decorated) - trigger - fixed
        for number, decorated in enumerate(instance.terms(word))
        if number != trigger_number
    }
    requirements.discard(frozenset())
    if maximum_size is not None:
        requirements = {
            requirement for requirement in requirements
            if len(requirement) <= maximum_size
        }
    return frozenset(
        requirement
        for requirement in requirements
        if not any(smaller < requirement for smaller in requirements)
    )


def direct_frontier(solver_name: str):
    """Close every <=9-cell minimal repair inside the cap-26 problem."""

    # At most nine additions means total support cap 25.  Blocking the
    # upward closure of each minimized model enumerates inclusion-minimal
    # mate-choice transversals, not all of their irrelevant supersets.
    instance = TightNoSingletonSearch(25, solver_name)
    try:
        seed_fibres = supported_fibres(SEED, instance.matchings)
        seed_singletons = [
            (word, terms[0][0])
            for word, terms in sorted(seed_fibres.items())
            if len(set(word)) > 1 and len(terms) == 1
        ]
        require(len(seed_singletons) == 11,
                "sharp seed singleton count changed")
        requirements = []
        for word, trigger_number in seed_singletons:
            instance.add_singleton_gadget(word, trigger_number)
            requirements.append(minimal_mate_requirements(
                instance, word, trigger_number, SEED
            ))

        def directly_repairs(extra):
            return all(
                any(requirement <= extra for requirement in family)
                for family in requirements
            )

        minimal_repairs = []
        while instance.solver.solve():
            extra = set(instance.decode(instance.solver.get_model()) - SEED)
            require(directly_repairs(extra),
                    "SAT direct-repair model failed semantic replay")
            changed = True
            while changed:
                changed = False
                for cell in sorted(extra):
                    if directly_repairs(extra - {cell}):
                        extra.remove(cell)
                        changed = True
            require(all(
                not directly_repairs(extra - {cell}) for cell in extra
            ), "direct repair is not inclusion-minimal")
            repair = frozenset(extra)
            require(repair not in minimal_repairs,
                    "direct repair was enumerated twice")
            minimal_repairs.append(repair)
            # Exclude this repair and every support containing it.
            instance.add_hard_clause(
                [-instance.support[cell] for cell in sorted(repair)]
            )

        size_census = Counter(map(len, minimal_repairs))
        require(size_census == Counter({8: 46, 9: 1452}),
                "direct-repair frontier census changed")

        secondary_census = Counter()
        completion_census = Counter()
        for repair in minimal_repairs:
            selected = SEED | repair
            fibres = supported_fibres(selected, instance.matchings)
            secondary = [
                (word, terms[0][0])
                for word, terms in sorted(fibres.items())
                if len(set(word)) > 1 and len(terms) == 1
            ]
            remaining = 10 - len(repair)
            secondary_census[len(repair), len(secondary)] += 1
            families = [
                minimal_mate_requirements(
                    instance, word, trigger_number, selected, remaining
                )
                for word, trigger_number in secondary
            ]
            partial_unions = {frozenset()}
            for family in sorted(families, key=len):
                partial_unions = {
                    previous | requirement
                    for previous in partial_unions
                    for requirement in family
                    if len(previous | requirement) <= remaining
                }
                partial_unions = {
                    union for union in partial_unions
                    if not any(smaller < union for smaller in partial_unions)
                }
                if not partial_unions:
                    break
            completion_census[len(repair), len(partial_unions)] += 1
            require(not partial_unions,
                    "small direct repair acquired a cap-26 completion")

        ledger = "".join(
            f"{len(repair)}:{tuple(sorted(repair))}\n"
            for repair in sorted(
                minimal_repairs,
                key=lambda value: (len(value), tuple(sorted(value))),
            )
        )
        digest = sha256(ledger.encode("ascii")).hexdigest()
        if EXPECTED_DIRECT_FRONTIER_SHA256 != "TO_BE_FROZEN":
            require(digest == EXPECTED_DIRECT_FRONTIER_SHA256,
                    "direct-repair frontier digest changed")
        print("direct minimal repairs through nine extras:", len(minimal_repairs))
        print("direct repair size census:", dict(sorted(size_census.items())))
        print("cap-26 completions of those repairs: 0")
        print("secondary singleton census:", dict(sorted(secondary_census.items())))
        print("completion-union census:", dict(sorted(completion_census.items())))
        print("direct frontier sha256:", digest)
        print("remaining cap-26 stratum: inclusion-minimal size-10 repairs")
        return minimal_repairs
    finally:
        instance.delete()


def search(cap: int, solver_name: str, max_rounds: int,
           checkpoint_prefix=None, resume_prefix=None):
    require(cap >= len(SEED), "cell cap is smaller than the fixed seed")
    instance = TightNoSingletonSearch(cap, solver_name, resume_prefix)
    singleton_frequency = Counter()
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
                singleton_frequency[word] += 1
                require(
                    instance.add_singleton_gadget(word, trigger_number),
                    "a semantic singleton repeated after its exact gadget",
                )
            if checkpoint_prefix is not None:
                instance.write_checkpoint(checkpoint_prefix)
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
        print("recurring singleton words:", singleton_frequency.most_common(10))
        return None
    finally:
        instance.delete()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit-seed", action="store_true")
    parser.add_argument("--direct-frontier", action="store_true")
    parser.add_argument("--cap", type=int, default=25)
    parser.add_argument("--solver", default="glucose42")
    parser.add_argument("--max-rounds", type=int, default=10000)
    parser.add_argument("--checkpoint")
    parser.add_argument("--resume")
    args = parser.parse_args()
    audit_seed()
    if args.direct_frontier:
        direct_frontier(args.solver)
    elif not args.audit_seed:
        search(
            args.cap, args.solver, args.max_rounds,
            checkpoint_prefix=args.checkpoint,
            resume_prefix=args.resume,
        )


if __name__ == "__main__":
    main()
