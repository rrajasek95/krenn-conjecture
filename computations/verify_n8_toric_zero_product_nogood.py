#!/usr/bin/env python3
"""Independent Boolean audit of the toric zero-product nogood schema."""

from __future__ import annotations

from itertools import product

import search_parallel_binomial_nonzero_constants_cegar as toric


def term_definition_satisfied(support_bits, term_bit):
    """CNF used by the encoder for ``term iff AND(support_bits)``."""

    clauses = [not term_bit or bit for bit in support_bits]
    clauses.append(any(not bit for bit in support_bits) or term_bit)
    return all(clauses)


def pair_trigger_definition_satisfied(non_target_terms, trigger_bit):
    """Clause for ``exact {target,Q} fibre -> trigger``."""

    other_term = non_target_terms[0]
    absent_terms = non_target_terms[1:]
    return fibre_trigger_definition_satisfied(
        (other_term,), absent_terms, trigger_bit
    )


def fibre_trigger_definition_satisfied(
    required_terms, absent_terms, trigger_bit
):
    """Clause for an arbitrary exact pure fibre forcing its trigger."""

    return (
        trigger_bit
        or any(not term for term in required_terms)
        or any(absent_terms)
    )


def main():
    # Exhaust the exact four-cell matching-term definition.
    for support_bits in product((False, True), repeat=4):
        satisfying = [
            term_bit
            for term_bit in (False, True)
            if term_definition_satisfied(support_bits, term_bit)
        ]
        assert satisfying == [all(support_bits)]

    # Exhaust the shared pure-pair trigger and its existential projection.
    # The target term is forced true and omitted.  Index zero is Q; the other
    # three bits represent all remaining non-target terms in this abstraction.
    for non_target_terms in product((False, True), repeat=4):
        satisfying_triggers = [
            trigger_bit
            for trigger_bit in (False, True)
            if pair_trigger_definition_satisfied(
                non_target_terms, trigger_bit
            )
        ]
        exact_pair = (
            non_target_terms[0] and not any(non_target_terms[1:])
        )
        assert satisfying_triggers == (
            [True] if exact_pair else [False, True]
        )
        for guard_bits in product((False, True), repeat=3):
            projected_short_clause = any(
                pair_trigger_definition_satisfied(
                    non_target_terms, trigger_bit
                )
                and (not all(guard_bits) or not trigger_bit)
                for trigger_bit in (False, True)
            )
            original_long_clause = (
                not all(guard_bits)
                or not non_target_terms[0]
                or any(non_target_terms[1:])
            )
            assert projected_short_clause == original_long_clause
        for first_guard in product((False, True), repeat=2):
            for second_guard in product((False, True), repeat=2):
                projected_shared_trigger = any(
                    pair_trigger_definition_satisfied(
                        non_target_terms, trigger_bit
                    )
                    and (not all(first_guard) or not trigger_bit)
                    and (not all(second_guard) or not trigger_bit)
                    for trigger_bit in (False, True)
                )
                original_two_clauses = all(
                    not all(guard)
                    or not non_target_terms[0]
                    or any(non_target_terms[1:])
                    for guard in (first_guard, second_guard)
                )
                assert projected_shared_trigger == original_two_clauses

    # Exercise a larger exact fibre with two required non-target terms and
    # two required absences, as used by the size-four and size-six schemas.
    for required_terms in product((False, True), repeat=2):
        for absent_terms in product((False, True), repeat=2):
            exact_fibre = all(required_terms) and not any(absent_terms)
            satisfying_triggers = [
                trigger_bit
                for trigger_bit in (False, True)
                if fibre_trigger_definition_satisfied(
                    required_terms, absent_terms, trigger_bit
                )
            ]
            assert satisfying_triggers == (
                [True] if exact_fibre else [False, True]
            )
            for guard_bits in product((False, True), repeat=3):
                projected = any(
                    fibre_trigger_definition_satisfied(
                        required_terms, absent_terms, trigger_bit
                    )
                    and (not all(guard_bits) or not trigger_bit)
                    for trigger_bit in (False, True)
                )
                original = not all(guard_bits) or not exact_fibre
                assert projected == original

    # A small abstract fibre system exercises the learned long clause.  The
    # current mixed equations require cells 0,1,2,3.  Pure matching terms are
    # arbitrary conjunctions of cells; their current truth assignment is
    # computed from the reference support, exactly as in the n=8 encoder.
    universe = tuple(range(7))
    mixed_required = frozenset({0, 1, 2, 3})
    pure_terms = (
        (frozenset({0, 4}), frozenset({1, 5}), frozenset({4, 6})),
        (frozenset({2, 4}), frozenset({3, 6}), frozenset({0, 5})),
        (frozenset({1, 6}), frozenset({2, 5}), frozenset({3, 4})),
    )
    reference = frozenset({0, 1, 2, 3, 4})
    reference_pure = tuple(
        tuple(term <= reference for term in family)
        for family in pure_terms
    )

    for bits in product((False, True), repeat=len(universe)):
        support = frozenset(i for i, bit in enumerate(bits) if bit)
        term_bits = tuple(
            tuple(term <= support for term in family)
            for family in pure_terms
        )
        clause_satisfied = (
            any(cell not in support for cell in mixed_required)
            or any(
                term_bits[colour][number]
                != reference_pure[colour][number]
                for colour in range(3)
                for number in range(3)
            )
        )
        guarded_data_unchanged = (
            mixed_required <= support and term_bits == reference_pure
        )
        assert clause_satisfied == (not guarded_data_unchanged)

    # Regression for color-set selection in the certificate minimizer.  With
    # x=y=z=-1 the first pure polynomial 1+xyz vanishes, but no individual
    # equation kills it.  The later color polynomial 1+x does have the
    # stronger one-row certificate, which must be found before ddmin commits
    # to the lexicographically first color.
    cells = ("x", "y", "z")
    cell_index = {cell: index for index, cell in enumerate(cells)}
    rows = (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
    )
    fibres = {
        (0,): ((0, ()), (1, ("x", "y", "z"))),
        (1,): ((0, ()), (1, ("x",))),
        (2,): ((0, ()),),
    }
    used_rows, used_colors = toric.minimize_zero_product_certificate(
        1, fibres, rows, cells, cell_index
    )
    assert used_rows == (0,)
    assert used_colors == (1,)

    print(
        "PASS: exact term-indicator CNF and zero-product nogood semantics "
        "for all 2^4 and 2^7 Boolean assignments; exact pure-fibre trigger "
        "projection; cross-color singleton minimization regression"
    )


if __name__ == "__main__":
    main()
