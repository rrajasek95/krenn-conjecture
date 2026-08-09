#!/usr/bin/env python3
"""Cheap exact least-cell cutoff from the eleven sharp mate families.

This does not solve any coefficient ideal.  It proves that a direct repair
whose least optional-cell index is beyond a finite cutoff cannot meet even
the original eleven singleton obligations, so the corresponding later SAT
blocks are structurally empty.
"""

from __future__ import annotations

from collections import Counter
from contextlib import redirect_stdout
import io

import search_n8_sharp_full_fibre_completion as sharp
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver


EXPECTED_FAMILY_SIZES = (72, 72, 92, 72, 92, 47, 92, 72, 92, 92, 92)
EXPECTED_MAXIMUM_LEAST_INDICES = (
    234, 208, 164, 192, 144, 234, 142, 172, 172, 143, 145
)
EXPECTED_CUTOFF = 142
EXPECTED_POSSIBLE_LEAST_INDICES = (
    1, 4, 5, 6, 8, 10, 13, 15, 16, 17, 19, 24, 28, 30, 31, 32,
    33, 34, 37, 39, 41, 42, 46, 49, 50, 51, 52, 54, 57, 58, 61,
    62, 65, 68, 74, 79, 84, 88, 94, 97, 98, 103, 105, 107, 116,
    126, 128, 136, 142,
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def exact_least_witness(index_families, least, number_cells,
                        forbidden_repairs, budget=10):
    """Solve only the eleven-family hypergraph, with essential least cell."""

    allowed_families = tuple(tuple(
        requirement for requirement in family
        if min(requirement) >= least
    ) for family in index_families)
    if any(not family for family in allowed_families):
        return None

    # Cell variable i is i+1.  Selector variables witness a complete mate
    # requirement in each family.  This is a tiny structural formula, not a
    # matching-fibre SAT enumeration.
    next_variable = number_cells
    clauses = []
    for family in allowed_families:
        selectors = []
        for requirement in family:
            next_variable += 1
            selector = next_variable
            selectors.append(selector)
            clauses.extend([-selector, value + 1]
                           for value in requirement)
        clauses.append(selectors)
    cardinality = CardEnc.atmost(
        lits=list(range(1, number_cells + 1)),
        bound=budget,
        top_id=next_variable,
        encoding=EncType.kmtotalizer,
    )
    next_variable = cardinality.nv
    clauses.extend(cardinality.clauses)
    clauses.append([least + 1])
    clauses.extend(
        [-(value + 1) for value in repair]
        for repair in forbidden_repairs
    )

    # One guard per possible obligation for which the least cell is
    # essential.  Under the guard, every alternative requirement omitting
    # that cell is forbidden from being completely selected.
    guards = []
    for family in allowed_families:
        if not any(least in requirement for requirement in family):
            guards.append(None)
            continue
        next_variable += 1
        guard = next_variable
        guards.append(guard)
        for requirement in family:
            if least not in requirement:
                clauses.append([-guard] + [-(value + 1)
                                           for value in requirement])

    solver = Solver(name="glucose42", bootstrap_with=clauses)
    try:
        for family_number, guard in enumerate(guards):
            if guard is None or not solver.solve(assumptions=[guard]):
                continue
            positive = {value for value in solver.get_model() if value > 0}
            chosen = {
                index for index in range(number_cells)
                if index + 1 in positive
            }

            def hits(candidate, family):
                return any(requirement <= candidate for requirement in family)

            require(all(hits(chosen, family)
                        for family in allowed_families),
                    "family-only SAT witness failed semantic replay")
            essential_family = allowed_families[family_number]
            require(not hits(chosen - {least}, essential_family),
                    "least-cell guard did not make the cell essential")
            # Remove every irrelevant cell.  The separately certified
            # no-<=9 family formula then forces the result to have size 10.
            changed = True
            while changed:
                changed = False
                for value in sorted(chosen - {least}, reverse=True):
                    candidate = chosen - {value}
                    if (all(hits(candidate, family)
                            for family in allowed_families)
                            and not hits(candidate - {least},
                                         essential_family)):
                        chosen = candidate
                        changed = True
            return frozenset(chosen)
        return None
    finally:
        solver.delete()


def main():
    instance = sharp.TightNoSingletonSearch(26, "glucose42")
    try:
        seed_fibres = sharp.supported_fibres(sharp.SEED, instance.matchings)
        singletons = tuple(
            (word, terms[0][0])
            for word, terms in sorted(seed_fibres.items())
            if len(set(word)) > 1 and len(terms) == 1
        )
        require(len(singletons) == 11, "seed singleton census changed")
        optional = tuple(cell for cell in instance.cells
                         if cell not in sharp.SEED)
        optional_index = {cell: index for index, cell in enumerate(optional)}
        families = tuple(
            sharp.minimal_mate_requirements(
                instance, word, trigger, sharp.SEED
            )
            for word, trigger in singletons
        )
        family_sizes = tuple(len(family) for family in families)

        # If i is the least selected optional index, each obligation family
        # must have a requirement all of whose cells have index >= i.  The
        # largest possible i for a fixed family is therefore the largest
        # least-cell index among its minimal requirements.  Taking the
        # minimum over all eleven families is a rigorous global cutoff.
        maximum_least_indices = tuple(
            max(min(optional_index[cell] for cell in requirement)
                for requirement in family)
            for family in families
        )
        cutoff = min(maximum_least_indices)
        witness_family = maximum_least_indices.index(cutoff)

        if EXPECTED_FAMILY_SIZES is not None:
            require(family_sizes == EXPECTED_FAMILY_SIZES,
                    "mate-family size census changed")
        if EXPECTED_MAXIMUM_LEAST_INDICES is not None:
            require(maximum_least_indices == EXPECTED_MAXIMUM_LEAST_INDICES,
                    "family least-index bounds changed")
        if EXPECTED_CUTOFF is not None:
            require(cutoff == EXPECTED_CUTOFF,
                    "global least-cell cutoff changed")

        # Replay the exclusion literally for every later index.
        excluded = 0
        family = families[witness_family]
        for least in range(cutoff + 1, len(optional)):
            require(not any(
                all(optional_index[cell] >= least for cell in requirement)
                for requirement in family
            ), "a structurally excluded late block regained a requirement")
            excluded += 1

        index_families = tuple(tuple(
            frozenset(optional_index[cell] for cell in requirement)
            for requirement in family
        ) for family in families)
        # Reuse the already-certified lower direct frontier only as blocking
        # clauses: an exact-ten inclusion-minimal repair cannot contain any
        # of these 46 size-eight or 1,452 size-nine repairs.
        with redirect_stdout(io.StringIO()):
            small_repairs = sharp.direct_frontier("glucose42")
        indexed_small_repairs = tuple(
            frozenset(optional_index[cell] for cell in repair)
            for repair in small_repairs
        )
        require(Counter(map(len, indexed_small_repairs))
                == Counter({8: 46, 9: 1452}),
                "lower direct-repair frontier changed")
        possible = []
        witnesses = {}
        for least in range(cutoff + 1):
            witness = exact_least_witness(
                index_families, least, len(optional), indexed_small_repairs
            )
            if witness is not None:
                possible.append(least)
                witnesses[least] = witness
        possible = tuple(possible)
        if EXPECTED_POSSIBLE_LEAST_INDICES is not None:
            require(possible == EXPECTED_POSSIBLE_LEAST_INDICES,
                    "exact possible least-cell indices changed")
        require(all(len(witness) == 10 for witness in witnesses.values()),
                "a possible least block has a non-exact-ten minimal witness")

        print("minimal mate-family sizes:", family_sizes)
        print("family maximum possible least indices:",
              maximum_least_indices)
        print("global possible least-index interval: 0..", cutoff)
        print("cutoff witness family:", witness_family)
        print("structurally excluded later blocks:", excluded)
        print("optional cells:", len(optional))
        print("exact possible least indices:", possible)
        print("exact possible least blocks:", len(possible))
    finally:
        instance.delete()


if __name__ == "__main__":
    main()
