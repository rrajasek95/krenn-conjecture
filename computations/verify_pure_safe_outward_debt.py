#!/usr/bin/env python3
"""Verify pure-singleton-preserving closure obstructions at n=6 and n=8.

Starting from the Hamiltonian cycle-cover modules, allow every additional
off-diagonal endpoint-coordinate cell on every vertex pair, but no new
monochromatic cell.  The latter restriction keeps each pure fibre literally
equal to its seeded one-factor.  This script proves that no subset of those
optional cells can eliminate all mixed singleton fibres.

At n=6 a five-word hand-checkable propagation suffices.  At n=8 the script
constructs the canonical term-indicator CNF implicitly, derives a conflict
by unit propagation, extracts a 107-clause/106-variable backward core, and
checks that this core is deletion-minimal for unit propagation.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Iterator, Sequence
from itertools import combinations, product


Cell = tuple[int, int, int, int]
Edge = tuple[int, int]
Matching = tuple[Edge, ...]
Word = tuple[int, ...]


def cell(u: int, v: int, a: int, b: int) -> Cell:
    return (u, v, a, b) if u < v else (v, u, b, a)


def perfect_matchings(vertices: Sequence[int]) -> Iterator[Matching]:
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], start=1):
        remainder = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(remainder):
            yield ((first, second),) + tail


def module(order: int) -> frozenset[Cell]:
    if order == 6:
        pure = (
            ((0, 1), (2, 3), (4, 5)),
            ((1, 2), (3, 4), (0, 5)),
            ((0, 2), (1, 4), (3, 5)),
        )
        extras = (
            (((0, 3), (1, 5), (2, 4)), (0, 0, 0, 1, 2, 2)),
            (((0, 4), (1, 3), (2, 5)), (0, 2, 1, 0, 1, 0)),
        )
    elif order == 8:
        pure = (
            ((0, 1), (2, 3), (4, 5), (6, 7)),
            ((1, 2), (3, 4), (5, 6), (0, 7)),
            ((0, 2), (1, 4), (3, 6), (5, 7)),
        )
        extras = (
            (((0, 3), (1, 5), (2, 6), (4, 7)), (1, 2, 0, 0, 2, 1, 1, 1)),
            (((0, 4), (1, 6), (2, 5), (3, 7)), (1, 1, 1, 2, 0, 0, 2, 1)),
        )
    else:  # pragma: no cover - guarded by the two audits below
        raise ValueError(order)

    seed = {
        cell(u, v, colour, colour)
        for colour, one_factor in enumerate(pure)
        for u, v in one_factor
    }
    seed.update(
        cell(u, v, word[u], word[v])
        for one_factor, word in extras
        for u, v in one_factor
    )
    assert len(seed) == 5 * order // 2
    return frozenset(seed)


def allowed_cells(order: int, seed: frozenset[Cell]) -> tuple[Cell, ...]:
    answer = set(seed)
    answer.update(
        (u, v, a, b)
        for u, v in combinations(range(order), 2)
        for a, b in product(range(3), repeat=2)
        if a != b
    )
    return tuple(sorted(answer))


def decorated_term(word: Word, matching: Matching) -> tuple[Cell, ...]:
    return tuple(cell(u, v, word[u], word[v]) for u, v in matching)


def feasible_fibres(
    order: int, allowed: set[Cell]
) -> tuple[
    tuple[tuple[int, ...], ...],
    tuple[tuple[Word, int], ...],
    tuple[tuple[int, ...], ...],
    tuple[Word, ...],
    tuple[Matching, ...],
    tuple[Cell, ...],
]:
    """Return cell-index terms and mixed fibres in deterministic order."""

    cells = tuple(sorted(allowed))
    cell_index = {entry: index for index, entry in enumerate(cells)}
    matchings = tuple(perfect_matchings(tuple(range(order))))
    terms: list[tuple[int, ...]] = []
    term_info: list[tuple[Word, int]] = []
    fibres: list[tuple[int, ...]] = []
    words: list[Word] = []
    for word in product(range(3), repeat=order):
        if len(set(word)) == 1:
            continue
        indices = []
        for matching_number, matching in enumerate(matchings):
            decorated = decorated_term(word, matching)
            if set(decorated) <= allowed:
                indices.append(len(terms))
                terms.append(tuple(cell_index[entry] for entry in decorated))
                term_info.append((word, matching_number))
        if indices:
            fibres.append(tuple(indices))
            words.append(word)
    return (
        tuple(terms),
        tuple(term_info),
        tuple(fibres),
        tuple(words),
        matchings,
        cells,
    )


def feasible_terms_for_word(
    word: Word,
    matchings: Sequence[Matching],
    allowed: set[Cell],
) -> tuple[frozenset[Cell], ...]:
    return tuple(
        frozenset(decorated)
        for matching in matchings
        for decorated in (decorated_term(word, matching),)
        if set(decorated) <= allowed
    )


def audit_six_site_chain() -> None:
    order = 6
    seed = module(order)
    allowed = set(allowed_cells(order, seed))
    matchings = tuple(perfect_matchings(tuple(range(order))))

    first_words = ((0, 0, 0, 0, 1, 0), (0, 0, 1, 0, 0, 0), (0, 2, 0, 0, 0, 0))
    first_absent = (
        cell(4, 5, 1, 0),
        cell(2, 3, 1, 0),
        cell(0, 1, 0, 2),
    )
    absent: set[Cell] = set()
    for word, forced_absent in zip(first_words, first_absent, strict=True):
        terms = feasible_terms_for_word(word, matchings, allowed)
        assert len(terms) == 1
        assert terms[0] - seed == {forced_absent}
        # If this sole optional cell were present, the displayed mixed word
        # would have exactly one term.  No-singleton therefore kills it.
        absent.add(forced_absent)

    bridge_word = (0, 2, 1, 0, 0, 0)
    bridge_terms = feasible_terms_for_word(bridge_word, matchings, allowed)
    assert len(bridge_terms) == 2
    surviving = [term for term in bridge_terms if not term & absent]
    assert len(surviving) == 1
    bridge_absent = cell(0, 2, 0, 1)
    assert surviving[0] - seed == {bridge_absent}
    absent.add(bridge_absent)

    terminal_word = (0, 2, 1, 0, 1, 0)
    terminal_terms = feasible_terms_for_word(terminal_word, matchings, allowed)
    seeded = [term for term in terminal_terms if term <= seed]
    assert len(terminal_terms) == 6 and len(seeded) == 1
    assert all(term & absent for term in terminal_terms if term not in seeded)
    # The seeded term is unavoidably present and all five possible mates are
    # disabled.  This is the final mixed singleton contradiction.


def unit_conflict(clauses: Sequence[tuple[int, ...]]) -> bool:
    values: dict[int, bool] = {}
    while True:
        changed = False
        for clause in clauses:
            unassigned = []
            satisfied = False
            for literal in clause:
                variable = abs(literal)
                if variable in values:
                    if values[variable] == (literal > 0):
                        satisfied = True
                        break
                else:
                    unassigned.append(literal)
            if satisfied:
                continue
            if not unassigned:
                return True
            if len(unassigned) == 1:
                literal = unassigned[0]
                variable = abs(literal)
                if variable not in values:
                    values[variable] = literal > 0
                    changed = True
        if not changed:
            return False


def audit_eight_site_unit_core() -> None:
    order = 8
    seed = module(order)
    allowed_tuple = allowed_cells(order, seed)
    allowed = set(allowed_tuple)
    terms, term_info, fibres, words, _matchings, cells = feasible_fibres(order, allowed)
    cell_index = {entry: index for index, entry in enumerate(cells)}
    assert len(cells) == 180
    assert len(terms) == 179_750
    assert len(fibres) == 6_558

    # States are -1=false, 0=unassigned, +1=true.  These are precisely the
    # unit-resolution rules for y_M <-> AND_{cell in M} x_cell together with
    # -y_M OR (OR of all same-word mates).
    cell_state = [0] * len(cells)
    cell_reason: list[tuple | None] = [None] * len(cells)
    for entry in seed:
        index = cell_index[entry]
        cell_state[index] = 1
        cell_reason[index] = ("seed",)
    term_state = [0] * len(terms)
    term_reason: list[tuple | None] = [None] * len(terms)
    conflict = None

    for round_number in range(20):
        for term_index, support in enumerate(terms):
            if term_state[term_index] == 0:
                false_cell = next(
                    (index for index in support if cell_state[index] < 0), None
                )
                if false_cell is not None:
                    term_state[term_index] = -1
                    term_reason[term_index] = ("cell_false", false_cell)
                elif all(cell_state[index] > 0 for index in support):
                    term_state[term_index] = 1
                    term_reason[term_index] = ("all_cells_true", support)

            if term_state[term_index] > 0:
                for index in support:
                    if cell_state[index] == 0:
                        cell_state[index] = 1
                        cell_reason[index] = ("term_true", term_index)
                    elif cell_state[index] < 0:
                        conflict = ("true_cell", term_index, index)
                        break
            elif term_state[term_index] < 0:
                unknown = [index for index in support if cell_state[index] == 0]
                if len(unknown) == 1 and all(
                    cell_state[index] > 0
                    for index in support
                    if index != unknown[0]
                ):
                    index = unknown[0]
                    cell_state[index] = -1
                    cell_reason[index] = (
                        "term_false_rest_true",
                        term_index,
                        tuple(other for other in support if other != index),
                    )
            if conflict is not None:
                break
        if conflict is not None:
            break

        for fibre_index, fibre in enumerate(fibres):
            possible = [index for index in fibre if term_state[index] >= 0]
            true_terms = [index for index in possible if term_state[index] > 0]
            if len(possible) == 1:
                term_index = possible[0]
                if term_state[term_index] > 0:
                    conflict = (
                        "unique_true",
                        fibre_index,
                        term_index,
                        tuple(index for index in fibre if index != term_index),
                    )
                    break
                term_state[term_index] = -1
                term_reason[term_index] = (
                    "sole_possible",
                    fibre_index,
                    tuple(index for index in fibre if index != term_index),
                )
            elif len(possible) == 2 and len(true_terms) == 1:
                other = next(index for index in possible if term_state[index] == 0)
                term_state[other] = 1
                term_reason[other] = (
                    "mate_for_true",
                    fibre_index,
                    true_terms[0],
                    tuple(
                        index
                        for index in fibre
                        if index not in (other, true_terms[0])
                    ),
                )
        if conflict is not None:
            break
    assert conflict is not None
    assert conflict[0] == "unique_true"
    assert words[conflict[1]] == (1, 2, 0, 0, 0, 1, 0, 0)
    assert round_number == 5

    # Trace only the assignments needed for the conflict.
    needed_cells: set[int] = set()
    needed_terms: set[int] = set()
    stack: list[tuple[str, int]] = []

    def need_cell(index: int) -> None:
        if index not in needed_cells:
            needed_cells.add(index)
            stack.append(("cell", index))

    def need_term(index: int) -> None:
        if index not in needed_terms:
            needed_terms.add(index)
            stack.append(("term", index))

    if conflict[0] == "unique_true":
        _, _fibre_index, term_index, other_terms = conflict
        need_term(term_index)
        for index in other_terms:
            need_term(index)
    else:  # pragma: no cover - retained for completeness of the tracer
        _, term_index, index = conflict
        need_term(term_index)
        need_cell(index)

    while stack:
        kind, index = stack.pop()
        reason = cell_reason[index] if kind == "cell" else term_reason[index]
        assert reason is not None
        tag = reason[0]
        if tag == "seed":
            continue
        if kind == "cell":
            if tag == "term_true":
                need_term(reason[1])
            elif tag == "term_false_rest_true":
                need_term(reason[1])
                for other in reason[2]:
                    need_cell(other)
            else:  # pragma: no cover - catches a malformed reason graph
                raise AssertionError(reason)
        elif tag == "cell_false":
            need_cell(reason[1])
        elif tag == "all_cells_true":
            for other in reason[1]:
                need_cell(other)
        elif tag == "sole_possible":
            for other in reason[2]:
                need_term(other)
        elif tag == "mate_for_true":
            need_term(reason[2])
            for other in reason[3]:
                need_term(other)
        else:  # pragma: no cover - catches a malformed reason graph
            raise AssertionError(reason)

    # Reify the backward trace as an ordinary CNF core.  Cell variables are
    # 1..180 and term variables start at 181.
    def x(index: int) -> int:
        return index + 1

    def y(index: int) -> int:
        return len(cells) + index + 1

    clauses: list[tuple[int, ...]] = []
    clause_kinds: list[str] = []

    def add_clause(literals: Iterable[int], kind: str) -> None:
        clauses.append(tuple(literals))
        clause_kinds.append(kind)

    for index in needed_cells:
        reason = cell_reason[index]
        assert reason is not None
        if reason[0] == "seed":
            add_clause((x(index),), "seed")
        elif reason[0] == "term_true":
            add_clause((-y(reason[1]), x(index)), "term_implies_cell")
        elif reason[0] == "term_false_rest_true":
            add_clause(
                (y(reason[1]),)
                + tuple(-x(other) for other in reason[2])
                + (-x(index),),
                "cells_imply_term",
            )
        else:  # pragma: no cover
            raise AssertionError(reason)

    for index in needed_terms:
        reason = term_reason[index]
        assert reason is not None
        if reason[0] == "cell_false":
            add_clause((-y(index), x(reason[1])), "term_implies_cell")
        elif reason[0] == "all_cells_true":
            add_clause(
                (y(index),) + tuple(-x(other) for other in reason[1]),
                "cells_imply_term",
            )
        elif reason[0] == "sole_possible":
            add_clause(
                (-y(index),) + tuple(y(other) for other in reason[2]),
                "no_singleton",
            )
        elif reason[0] == "mate_for_true":
            add_clause(
                (-y(reason[2]), y(index))
                + tuple(y(other) for other in reason[3]),
                "no_singleton",
            )
        else:  # pragma: no cover
            raise AssertionError(reason)

    _, _fibre_index, term_index, other_terms = conflict
    add_clause(
        (-y(term_index),) + tuple(y(other) for other in other_terms),
        "conflict_no_singleton",
    )

    assert len(needed_cells) == 41
    assert len(needed_terms) == 65
    assert len(clauses) == 107
    assert Counter(clause_kinds) == Counter(
        {
            "term_implies_cell": 42,
            "cells_imply_term": 23,
            "no_singleton": 22,
            "seed": 19,
            "conflict_no_singleton": 1,
        }
    )
    assert len({term_info[index][0] for index in needed_terms}) == 23
    assert unit_conflict(clauses)
    # Every clause participates in this particular unit-resolution proof.
    assert all(
        not unit_conflict(clauses[:index] + clauses[index + 1 :])
        for index in range(len(clauses))
    )


def main() -> None:
    audit_six_site_chain()
    audit_eight_site_unit_core()
    print("PASS pure-safe outward-debt obstruction")
    print("n=6: five mixed words force four cells absent, then a seeded singleton")
    print("n=8: 107-clause/106-variable deletion-minimal unit core on 23 words")
    print("no off-diagonal coordinate-cell extension can preserve singleton pure fibres")


if __name__ == "__main__":
    main()
