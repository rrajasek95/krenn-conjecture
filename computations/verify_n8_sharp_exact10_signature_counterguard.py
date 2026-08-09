#!/usr/bin/env python3
"""Exact counterguard to an incidence-only exact-ten classification.

Two inclusion-minimal ten-cell repairs of the corrected chart-26 seed have
the same named structural invariants: essential obligation/cell incidence,
obligation overlap graph, original fibre sizes, binomial rank/count, and the
complete alternating-cycle census.  Nevertheless one signed binomial lattice
is consistent and leaves a four-term fibre as one Laurent class, while the
other has an explicit odd three-row relation.

The examples are not no-singleton supports and are not Krenn
counterexamples.  They show only that the proposed structural invariants do
not select the algebraic certificate branch.
"""

from __future__ import annotations

from collections import Counter, defaultdict

from flint import fmpz_mat

import search_n8_sharp_full_fibre_completion as sharp
import search_n8_sparse_triple_completion as sparse


MONOMIAL_EXTRA = frozenset({
    (0, 4, 2, 2),
    (1, 7, 1, 1),
    (2, 6, 0, 0),
    (2, 6, 2, 1),
    (3, 4, 0, 2),
    (3, 6, 2, 2),
    (3, 7, 0, 0),
    (3, 7, 1, 2),
    (4, 5, 1, 1),
    (6, 7, 2, 1),
})

ODD_EXTRA = frozenset({
    (0, 1, 2, 0),
    (1, 7, 1, 1),
    (2, 6, 0, 0),
    (2, 6, 2, 1),
    (3, 4, 0, 2),
    (3, 5, 2, 1),
    (3, 7, 0, 0),
    (3, 7, 1, 2),
    (4, 5, 1, 1),
    (6, 7, 2, 1),
})

EXPECTED_ESSENTIAL_INCIDENCE = (
    (9,),
    (2, 6),
    (3, 7),
    (3, 7),
    (2, 6),
    (9,),
    (3, 7),
    (4, 9),
    (4, 9),
    (0, 5),
    (1, 8),
)

EXPECTED_OVERLAP_EDGES = (
    (0, 5), (0, 7), (0, 8),
    (1, 4),
    (2, 3), (2, 6),
    (3, 6),
    (5, 7), (5, 8),
    (7, 8),
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def alternating_cycle_profile(first, second):
    first_edges = {(cell[0], cell[1]) for cell in first}
    second_edges = {(cell[0], cell[1]) for cell in second}
    adjacency = defaultdict(set)
    for left, right in first_edges ^ second_edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    unseen = set(adjacency)
    sizes = []
    while unseen:
        root = min(unseen)
        component = {root}
        stack = [root]
        while stack:
            vertex = stack.pop()
            for other in adjacency[vertex]:
                if other not in component:
                    component.add(other)
                    stack.append(other)
        unseen -= component
        sizes.append(len(component))
    return tuple(sorted(sizes))


def structural_record(instance, extra, original, requirement_families):
    selected = sharp.SEED | extra
    fibres = sparse.exact_fibres(instance, selected)
    mixed, rows = sparse.binomial_system(instance, fibres)

    essential_rows = []
    used_by_obligation = []
    ordered_extra = tuple(sorted(extra))
    extra_index = {cell: index for index, cell in enumerate(ordered_extra)}
    for family in requirement_families:
        active = [requirement for requirement in family if requirement <= extra]
        require(active, "an original singleton obligation was not repaired")
        essential = set.intersection(*map(set, active))
        used = set().union(*active)
        essential_rows.append(tuple(sorted(extra_index[cell] for cell in essential)))
        used_by_obligation.append(used)

    overlap_edges = tuple(
        (left, right)
        for left in range(len(original))
        for right in range(left + 1, len(original))
        if used_by_obligation[left] & used_by_obligation[right]
    )
    original_sizes = tuple(len(fibres[word]) for word, _trigger in original)
    cycle_census = Counter(
        alternating_cycle_profile(terms[0][1], terms[1][1])
        for _word, terms in mixed
    )
    return {
        "fibres": fibres,
        "mixed": mixed,
        "rows": rows,
        "rank": int(fmpz_mat(rows).rank()),
        "essential": tuple(essential_rows),
        "overlap": overlap_edges,
        "original_sizes": original_sizes,
        "cycles": cycle_census,
    }


def main() -> None:
    instance = sharp.TightNoSingletonSearch(26, "glucose42")
    try:
        seed_fibres = sharp.supported_fibres(sharp.SEED, instance.matchings)
        original = tuple(
            (word, terms[0][0])
            for word, terms in sorted(seed_fibres.items())
            if len(set(word)) > 1 and len(terms) == 1
        )
        require(len(original) == 11, "sharp singleton obligations changed")
        requirement_families = tuple(
            sharp.minimal_mate_requirements(
                instance, word, trigger, sharp.SEED
            )
            for word, trigger in original
        )

        records = {}
        for name, extra in (
            ("monomial", MONOMIAL_EXTRA),
            ("odd", ODD_EXTRA),
        ):
            require(len(extra) == 10, f"{name} repair is not exact-ten")
            require(all(
                any(requirement <= extra for requirement in family)
                for family in requirement_families
            ), f"{name} repair misses an original obligation")
            require(all(
                not all(
                    any(requirement <= extra - {cell}
                        for requirement in family)
                    for family in requirement_families
                )
                for cell in extra
            ), f"{name} repair is not inclusion-minimal")
            records[name] = structural_record(
                instance, extra, original, requirement_families
            )

        monomial = records["monomial"]
        odd = records["odd"]
        for record in records.values():
            require(record["rank"] == 7, "binomial rank changed")
            require(len(record["rows"]) == 25, "binomial count changed")
            require(record["essential"] == EXPECTED_ESSENTIAL_INCIDENCE,
                    "essential incidence changed")
            require(record["overlap"] == EXPECTED_OVERLAP_EDGES,
                    "obligation overlap graph changed")
            require(record["original_sizes"] == (2,) * 11,
                    "original fibre sizes changed")
            require(record["cycles"] == Counter({(4,): 23, (6,): 2}),
                    "alternating-cycle census changed")

        monomial_consistent, _ = sparse.toric.signed_quotient_lattice(
            monomial["rows"], len(instance.cells)
        )
        require(monomial_consistent,
                "monomial guard's signed binomial lattice became inconsistent")
        closure = sparse.quotient_binomial_closure(
            instance, monomial["fibres"], monomial["rows"]
        )
        require(closure["status"] == "monomial" and closure["rounds"] == 0,
                "monomial guard lost its immediate quotient obstruction")
        sharp_remainder = closure["remainders"][sharp.SHARP_WORD]
        require(len(monomial["fibres"][sharp.SHARP_WORD]) == 4,
                "monomial guard sharp fibre is not four-term")
        require(len(sharp_remainder) == 1
                and tuple(sharp_remainder.values()) == (-2,),
                "four-term sharp fibre is not the frozen -2 Laurent monomial")

        odd_consistent, _ = sparse.toric.signed_quotient_lattice(
            odd["rows"], len(instance.cells)
        )
        require(not odd_consistent,
                "odd guard's signed binomial lattice became consistent")
        triangles = sparse.toric_search.unit_triangle_circuits(odd["rows"])
        require(len(triangles) == 10, "odd triangle count changed")
        first_triangle = triangles[0]
        require(first_triangle == (0, 12, 18),
                "frozen odd triangle indices changed")
        triangle_rows = [odd["rows"][index] for index in first_triangle]
        require(all(
            -triangle_rows[0][column]
            + triangle_rows[1][column]
            + triangle_rows[2][column] == 0
            for column in range(len(instance.cells))
        ), "frozen -r0+r12+r18 relation failed")
        triangle_words = tuple(
            odd["mixed"][index][0] for index in first_triangle
        )
        require(triangle_words == (
            (0, 0, 0, 0, 0, 0, 2, 1),
            (1, 0, 1, 0, 2, 1, 2, 1),
            (2, 0, 0, 0, 2, 1, 2, 1),
        ), "frozen odd triangle words changed")

        # Both supports have secondary singleton fibres.  This makes explicit
        # that the counterguard concerns certificate classification only.
        histograms = {
            name: Counter(
                len(terms)
                for word, terms in record["fibres"].items()
                if len(set(word)) > 1
            )
            for name, record in records.items()
        }
        require(histograms == {
            "monomial": Counter({1: 49, 2: 25, 4: 1}),
            "odd": Counter({1: 53, 2: 25, 4: 1}),
        }, "counterguard fibre histograms changed")

        print("verified two inclusion-minimal exact-ten repairs")
        print("common binomial rank/count: 7/25")
        print("common alternating cycles: 23 C4 and 2 C6")
        print("common essential incidence:", EXPECTED_ESSENTIAL_INCIDENCE)
        print("common obligation overlap edges:", EXPECTED_OVERLAP_EDGES)
        print("monomial branch: four-term sharp fibre -> one class, coefficient -2")
        print("odd branch: -r0+r12+r18=0 with odd coefficient sum 1")
        print("mixed histograms:", histograms)
    finally:
        instance.delete()


if __name__ == "__main__":
    main()
