#!/usr/bin/env python3
"""Independent exact audit of the three-adjacent-five-cut countermodel.

This checker does not import the primary verifier.  It rebuilds the
endpoint-ordered decorated-source tensor over Q, the five-site insertion
spaces, the annihilator quotients, the three displayed residual
decompositions, deletion-only support minimality, and the two-source repair.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from itertools import product


Q = Fraction
ALL_SITES = tuple(range(8))
SIX_SITES = tuple(range(6))
OUTSIDE = (6, 7)
CUT_LABELS = (2, 3, 4)
COLOURS = tuple(range(3))

# A source is (first site, second site, colour at first site,
# colour at second site, weight).  The endpoints need not be listed in
# increasing order; canonical_source retains their endpoint colours.
PRIMARY_SOURCES = (
    (0, 1, 0, 0, 1),
    (4, 5, 0, 0, 1),
    (0, 2, 1, 1, 1),
    (1, 4, 1, 1, 1),
    (3, 6, 1, 1, 1),
    (5, 7, 1, 1, 1),
    (0, 4, 2, 2, 1),
    (1, 3, 2, 2, 1),
    (2, 7, 2, 2, 1),
    (5, 6, 2, 2, 1),
    (2, 5, 0, 0, 1),
    (3, 5, 1, 0, 1),
)

REPAIR_SOURCES = (
    (2, 3, 2, 1, 1),
    (6, 7, 1, 2, -1),
)

Word = tuple[int, ...]
Vector = dict[Word, Q]
Tensor = dict[Word, Q]
Source = tuple[int, int, int, int, int]
Edge = tuple[int, int]
Cell = tuple[int, int]
Blocks = dict[Edge, dict[Cell, Q]]


def canonical_source(source: Source) -> tuple[Edge, Cell, Q]:
    """Put a source in increasing site order without swapping its colours."""
    u, v, colour_u, colour_v, weight = source
    if u < v:
        return (u, v), (colour_u, colour_v), Q(weight)
    if v < u:
        return (v, u), (colour_v, colour_u), Q(weight)
    raise ValueError("a degree-two source must have two distinct endpoints")


def aggregate_blocks(sources: tuple[Source, ...]) -> Blocks:
    """Sum parallel decorated cells exactly, deleting cancelled cells."""
    blocks: Blocks = {}
    for source in sources:
        edge, cell, weight = canonical_source(source)
        block = blocks.setdefault(edge, {})
        total = block.get(cell, Q(0)) + weight
        if total:
            block[cell] = total
        else:
            block.pop(cell, None)
        if not block:
            blocks.pop(edge, None)
    return blocks


def labelled_blocks(sources: tuple[Source, ...]):
    """Keep parallel sources separate for a direct source-level expansion."""
    blocks: dict[Edge, list[tuple[Cell, Q]]] = {}
    for source in sources:
        edge, cell, weight = canonical_source(source)
        if weight:
            blocks.setdefault(edge, []).append((cell, weight))
    return blocks


@lru_cache(maxsize=None)
def pairings(vertices: tuple[int, ...]) -> tuple[tuple[Edge, ...], ...]:
    """Enumerate all perfect matchings of an ordered even vertex tuple."""
    vertices = tuple(sorted(vertices))
    if not vertices:
        return ((),)
    first = vertices[0]
    answer: list[tuple[Edge, ...]] = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        remaining = vertices[1:position] + vertices[position + 1 :]
        for tail in pairings(remaining):
            answer.append((((first, second),) + tail))
    return tuple(answer)


def add_coefficient(tensor: Tensor, word: Word, coefficient: Q) -> None:
    total = tensor.get(word, Q(0)) + coefficient
    if total:
        tensor[word] = total
    else:
        tensor.pop(word, None)


def expanded_terms(vertices: tuple[int, ...], blocks):
    """Expand either aggregate cells or individually labelled sources."""
    positions = {site: index for index, site in enumerate(vertices)}
    for matching in pairings(vertices):
        choices = []
        for edge in matching:
            block = blocks.get(edge, {})
            choices.append(tuple(block.items()) if isinstance(block, dict) else block)
        if any(not choice for choice in choices):
            continue
        for selected in product(*choices):
            word = [-1] * len(vertices)
            coefficient = Q(1)
            for (u, v), (cell, weight) in zip(matching, selected):
                colour_u, colour_v = cell
                word[positions[u]] = colour_u
                word[positions[v]] = colour_v
                coefficient *= weight
            if coefficient:
                yield matching, tuple(word), coefficient


def matching_tensor(vertices: tuple[int, ...], blocks) -> Tensor:
    tensor: Tensor = {}
    for _matching, word, coefficient in expanded_terms(vertices, blocks):
        add_coefficient(tensor, word, coefficient)
    return tensor


def tensor_linear_combination(*terms: tuple[Q, Tensor]) -> Tensor:
    answer: Tensor = {}
    for scalar, tensor in terms:
        for word, coefficient in tensor.items():
            add_coefficient(answer, word, scalar * coefficient)
    return answer


DELTA: Tensor = {(colour,) * 8: Q(1) for colour in COLOURS}


def crossing_sector(c_sites: tuple[int, ...], number: int, blocks: Blocks) -> Tensor:
    c_set = set(c_sites)
    answer: Tensor = {}
    for matching, word, coefficient in expanded_terms(ALL_SITES, blocks):
        crossings = sum((u in c_set) != (v in c_set) for u, v in matching)
        if crossings == number:
            add_coefficient(answer, word, coefficient)
    return answer


def cofactor_insertion_columns(u_sites: tuple[int, ...], blocks: Blocks) -> list[Vector]:
    columns: list[Vector] = []
    for hole in u_sites:
        remaining = tuple(site for site in u_sites if site != hole)
        cofactor = matching_tensor(remaining, blocks)
        for colour in COLOURS:
            column: Vector = {}
            for cofactor_word, coefficient in cofactor.items():
                assignment = dict(zip(remaining, cofactor_word))
                assignment[hole] = colour
                word = tuple(assignment[site] for site in u_sites)
                add_coefficient(column, word, coefficient)
            if column:
                columns.append(column)
    return columns


def one_insertion_column(
    u_sites: tuple[int, ...], hole: int, colour: int, blocks: Blocks
) -> Vector:
    remaining = tuple(site for site in u_sites if site != hole)
    cofactor = matching_tensor(remaining, blocks)
    column: Vector = {}
    for cofactor_word, coefficient in cofactor.items():
        assignment = dict(zip(remaining, cofactor_word))
        assignment[hole] = colour
        add_coefficient(column, tuple(assignment[site] for site in u_sites), coefficient)
    return column


def echelon_basis(vectors: list[Vector]) -> dict[Word, Vector]:
    """Sparse exact column-space basis, keyed by lexicographic pivot."""
    basis: dict[Word, Vector] = {}
    for supplied in vectors:
        vector = {word: Q(value) for word, value in supplied.items() if value}
        while vector:
            pivot = min(vector)
            if pivot not in basis:
                pivot_value = vector[pivot]
                basis[pivot] = {
                    word: value / pivot_value for word, value in vector.items()
                }
                break
            multiple = vector[pivot]
            for word, value in basis[pivot].items():
                updated = vector.get(word, Q(0)) - multiple * value
                if updated:
                    vector[word] = updated
                else:
                    vector.pop(word, None)
    return basis


def belongs(vector: Vector, basis: dict[Word, Vector]) -> bool:
    remainder = {word: Q(value) for word, value in vector.items() if value}
    while remainder:
        pivot = min(remainder)
        if pivot not in basis:
            return False
        multiple = remainder[pivot]
        for word, value in basis[pivot].items():
            updated = remainder.get(word, Q(0)) - multiple * value
            if updated:
                remainder[word] = updated
            else:
                remainder.pop(word, None)
    return True


def flatten_on_cut(
    tensor: Tensor, c_sites: tuple[int, ...], u_sites: tuple[int, ...]
) -> dict[Word, Vector]:
    rows: dict[Word, Vector] = {}
    for full_word, coefficient in tensor.items():
        c_word = tuple(full_word[site] for site in c_sites)
        u_word = tuple(full_word[site] for site in u_sites)
        row = rows.setdefault(c_word, {})
        add_coefficient(row, u_word, coefficient)
    return rows


def tensor_in_cylinder(
    tensor: Tensor,
    c_sites: tuple[int, ...],
    u_sites: tuple[int, ...],
    insertion_basis: dict[Word, Vector],
) -> bool:
    return all(
        belongs(row, insertion_basis)
        for row in flatten_on_cut(tensor, c_sites, u_sites).values()
    )


def rref_equations(equations: list[Vector], coordinates: tuple[Word, ...]):
    """RREF of equations beta -> <equation,beta>, for an annihilator basis."""
    rows = [{word: Q(value) for word, value in equation.items() if value} for equation in equations]
    rows = [row for row in rows if row]
    pivot_words: list[Word] = []
    active = 0
    for coordinate in coordinates:
        found = next(
            (index for index in range(active, len(rows)) if rows[index].get(coordinate)),
            None,
        )
        if found is None:
            continue
        rows[active], rows[found] = rows[found], rows[active]
        scale = rows[active][coordinate]
        rows[active] = {word: value / scale for word, value in rows[active].items()}
        for index, row in enumerate(rows):
            if index == active or not row.get(coordinate):
                continue
            multiple = row[coordinate]
            for word, value in rows[active].items():
                updated = row.get(word, Q(0)) - multiple * value
                if updated:
                    row[word] = updated
                else:
                    row.pop(word, None)
        pivot_words.append(coordinate)
        active += 1
        if active == len(rows):
            break
    # Dependent supplied equations have reduced to zero rows below `active`.
    assert all(not row for row in rows[active:])
    return rows[:active], tuple(pivot_words)


def annihilator_basis(columns: list[Vector], u_sites: tuple[int, ...]) -> list[Vector]:
    coordinates = tuple(product(COLOURS, repeat=len(u_sites)))
    rows, pivots = rref_equations(columns, coordinates)
    pivot_set = set(pivots)
    answer: list[Vector] = []
    for free in coordinates:
        if free in pivot_set:
            continue
        vector: Vector = {free: Q(1)}
        for row, pivot in zip(rows, pivots):
            value = -row.get(free, Q(0))
            if value:
                vector[pivot] = value
        answer.append(vector)
    for beta in answer:
        assert all(
            sum((coefficient * beta.get(word, Q(0)) for word, coefficient in column.items()), Q(0)) == 0
            for column in columns
        )
    assert len(answer) == len(coordinates) - len(rows)
    return answer


def contract_u(
    tensor: Tensor,
    c_sites: tuple[int, ...],
    u_sites: tuple[int, ...],
    beta: Vector,
) -> Tensor:
    answer: Tensor = {}
    for full_word, coefficient in tensor.items():
        u_word = tuple(full_word[site] for site in u_sites)
        beta_value = beta.get(u_word, Q(0))
        if beta_value:
            c_word = tuple(full_word[site] for site in c_sites)
            add_coefficient(answer, c_word, coefficient * beta_value)
    return answer


def target_contraction(beta: Vector) -> Tensor:
    answer: Tensor = {}
    for colour in COLOURS:
        value = beta.get((colour,) * 5, Q(0))
        if value:
            answer[(colour,) * 3] = value
    return answer


def cut_data(z: int, blocks: Blocks, full_tensor: Tensor | None = None):
    u_sites = tuple(site for site in SIX_SITES if site != z)
    c_sites = (z,) + OUTSIDE
    columns = cofactor_insertion_columns(u_sites, blocks)
    basis = echelon_basis(columns)
    t1 = crossing_sector(c_sites, 1, blocks)
    t3 = crossing_sector(c_sites, 3, blocks)
    quotient_residual = tensor_linear_combination((Q(1), t3), (Q(-1), DELTA))
    if full_tensor is None:
        full_tensor = matching_tensor(ALL_SITES, blocks)
    full_residual = tensor_linear_combination((Q(1), full_tensor), (Q(-1), DELTA))
    quotient_identity = tensor_in_cylinder(
        quotient_residual, c_sites, u_sites, basis
    )
    common_residual = tensor_in_cylinder(full_residual, c_sites, u_sites, basis)
    one_crossing_factor = tensor_in_cylinder(t1, c_sites, u_sites, basis)
    constants = [{(colour,) * 5: Q(1)} for colour in COLOURS]
    augmented_rank = len(echelon_basis(columns + constants))
    flags = tuple(belongs(constant, basis) for constant in constants)
    return {
        "u_sites": u_sites,
        "c_sites": c_sites,
        "columns": columns,
        "basis": basis,
        "t1": t1,
        "t3": t3,
        "quotient_identity": quotient_identity,
        "common_residual": common_residual,
        "one_crossing_factor": one_crossing_factor,
        "constant_flags": flags,
        "defect": augmented_rank - len(basis),
    }


def lift_insertion_row(
    c_sites: tuple[int, ...],
    u_sites: tuple[int, ...],
    c_word: Word,
    row: Vector,
) -> Tensor:
    answer: Tensor = {}
    for u_word, coefficient in row.items():
        assignment = dict(zip(c_sites, c_word))
        assignment.update(zip(u_sites, u_word))
        add_coefficient(
            answer,
            tuple(assignment[site] for site in ALL_SITES),
            coefficient,
        )
    return answer


def audit_endpoint_order_and_aggregation() -> None:
    # Two parallel cells cancel, while a source deliberately listed in
    # reverse endpoint order verifies that its endpoint colours are swapped
    # together with its sites.
    probe_sources = (
        (0, 1, 0, 2, 2),
        (0, 1, 0, 2, -2),
        (0, 1, 2, 0, 3),
        (3, 2, 2, 1, 5),
    )
    aggregate = aggregate_blocks(probe_sources)
    direct = matching_tensor((0, 1, 2, 3), labelled_blocks(probe_sources))
    combined = matching_tensor((0, 1, 2, 3), aggregate)
    assert direct == combined == {(2, 0, 1, 2): Q(15)}
    assert (0, 2) not in aggregate[(0, 1)]
    assert aggregate[(2, 3)] == {(1, 2): Q(5)}


def audit_original_tensor_and_decompositions() -> tuple[Blocks, Tensor]:
    blocks = aggregate_blocks(PRIMARY_SOURCES)
    direct = matching_tensor(ALL_SITES, labelled_blocks(PRIMARY_SOURCES))
    aggregated = matching_tensor(ALL_SITES, blocks)
    assert direct == aggregated
    assert len(pairings(ALL_SITES)) == 105

    supported_terms = list(expanded_terms(ALL_SITES, blocks))
    expected_matchings = {
        ((0, 1), (2, 7), (3, 6), (4, 5)),
        ((0, 2), (1, 4), (3, 6), (5, 7)),
        ((0, 4), (1, 3), (2, 7), (5, 6)),
    }
    assert {matching for matching, _word, _coefficient in supported_terms} == expected_matchings
    assert len(supported_terms) == 3

    mixed = (0, 0, 2, 1, 0, 0, 1, 2)
    expected_tensor = {
        mixed: Q(1),
        (1,) * 8: Q(1),
        (2,) * 8: Q(1),
    }
    assert aggregated == expected_tensor
    residual = tensor_linear_combination((Q(1), aggregated), (Q(-1), DELTA))
    assert residual == {mixed: Q(1), (0,) * 8: Q(-1)}

    # Audit every cofactor named in the three displayed decompositions and
    # in the constant-word intersection argument.
    named_cofactors = {
        (0, 1, 4, 5): {(0, 0, 0, 0): Q(1)},
        (0, 1, 3, 5): {(0, 0, 1, 0): Q(1)},
        (0, 1, 2, 5): {(0, 0, 0, 0): Q(1)},
        (0, 1, 3, 4): {(2, 2, 2, 2): Q(1)},
        (0, 1, 2, 4): {(1, 1, 1, 1): Q(1)},
    }
    for vertices, expected in named_cofactors.items():
        assert matching_tensor(vertices, blocks) == expected

    descriptions = {
        2: (
            ((2, 1, 2), 3, 1, Q(1)),
            ((0, 0, 0), 3, 0, Q(-1)),
        ),
        3: (
            ((1, 1, 2), 2, 2, Q(1)),
            ((0, 0, 0), 2, 0, Q(-1)),
        ),
        4: (
            ((0, 1, 2), 2, 2, Q(1)),
            ((0, 0, 0), 3, 0, Q(-1)),
        ),
    }
    for z, summands in descriptions.items():
        u_sites = tuple(site for site in SIX_SITES if site != z)
        c_sites = (z,) + OUTSIDE
        reconstructed: Tensor = {}
        for c_word, hole, colour, scalar in summands:
            row = one_insertion_column(u_sites, hole, colour, blocks)
            assert row
            lifted = lift_insertion_row(c_sites, u_sites, c_word, row)
            reconstructed = tensor_linear_combination(
                (Q(1), reconstructed), (scalar, lifted)
            )
        assert reconstructed == residual
    return blocks, aggregated


def audit_three_quotients(blocks: Blocks, full_tensor: Tensor) -> None:
    expected_flags = {
        2: (True, False, True),
        3: (True, True, False),
        4: (True, False, False),
    }
    expected_t3 = {
        2: {(1,) * 8: Q(1)},
        3: {(2,) * 8: Q(1)},
        4: {
            (0, 0, 2, 1, 0, 0, 1, 2): Q(1),
            (1,) * 8: Q(1),
            (2,) * 8: Q(1),
        },
    }
    for z in CUT_LABELS:
        data = cut_data(z, blocks, full_tensor)
        assert data["one_crossing_factor"]
        assert data["quotient_identity"]
        assert data["common_residual"]
        assert data["quotient_identity"] == data["common_residual"]
        assert data["constant_flags"] == expected_flags[z]
        assert data["defect"] == expected_flags[z].count(False)
        assert data["t3"] == expected_t3[z]

        # Verify the complete quotient formula directly on a basis of the
        # full annihilator K_U, independently of residual row membership.
        annihilators = annihilator_basis(data["columns"], data["u_sites"])
        assert annihilators
        for beta in annihilators:
            assert contract_u(
                data["t3"], data["c_sites"], data["u_sites"], beta
            ) == target_contraction(beta)

        # The omitted constant-coordinate functionals are explicit target
        # witnesses, while included constants force the corresponding
        # target coordinate to vanish throughout K_U.
        for colour, included in enumerate(expected_flags[z]):
            coordinate_beta = {(colour,) * 5: Q(1)}
            annihilates = all(
                sum(
                    (
                        coefficient * coordinate_beta.get(word, Q(0))
                        for word, coefficient in column.items()
                    ),
                    Q(0),
                )
                == 0
                for column in data["columns"]
            )
            assert annihilates == (not included)


def supports_active_triple(sources: tuple[Source, ...]) -> bool:
    blocks = aggregate_blocks(sources)
    full_tensor = matching_tensor(ALL_SITES, blocks)
    for z in CUT_LABELS:
        data = cut_data(z, blocks, full_tensor)
        if not data["quotient_identity"] or data["defect"] == 0:
            return False
    return True


def audit_deletion_only_minimality() -> None:
    number = len(PRIMARY_SOURCES)
    full_mask = (1 << number) - 1
    assert supports_active_triple(PRIMARY_SOURCES)
    assert not supports_active_triple(())
    survivors: list[int] = []
    tested = 0
    for mask in range(1, full_mask):
        subfamily = tuple(
            source
            for index, source in enumerate(PRIMARY_SOURCES)
            if mask & (1 << index)
        )
        tested += 1
        if supports_active_triple(subfamily):
            survivors.append(mask)
    assert tested == 4094
    assert survivors == []


def audit_two_source_repair() -> None:
    sources = PRIMARY_SOURCES + REPAIR_SOURCES
    blocks = aggregate_blocks(sources)
    direct = matching_tensor(ALL_SITES, labelled_blocks(sources))
    repaired = matching_tensor(ALL_SITES, blocks)
    assert direct == repaired

    killed = (0, 0, 2, 1, 0, 0, 1, 2)
    expected = {
        (1,) * 8: Q(1),
        (2,) * 8: Q(1),
        (1, 2, 1, 2, 0, 0, 1, 2): Q(-1),
        (1, 1, 1, 1, 1, 0, 1, 2): Q(-1),
        (2, 2, 0, 2, 2, 0, 1, 2): Q(-1),
    }
    assert repaired == expected
    assert killed not in repaired

    expected_flags = {
        2: (True, False, True),
        3: (True, True, False),
        4: (True, False, False),
    }
    for z in CUT_LABELS:
        data = cut_data(z, blocks, repaired)
        assert data["one_crossing_factor"]
        assert data["quotient_identity"]
        assert data["common_residual"]
        assert data["constant_flags"] == expected_flags[z]
        assert data["defect"] == expected_flags[z].count(False)
        annihilators = annihilator_basis(data["columns"], data["u_sites"])
        for beta in annihilators:
            assert contract_u(
                data["t3"], data["c_sites"], data["u_sites"], beta
            ) == target_contraction(beta)


def main() -> None:
    audit_endpoint_order_and_aggregation()
    blocks, full_tensor = audit_original_tensor_and_decompositions()
    audit_three_quotients(blocks, full_tensor)
    audit_deletion_only_minimality()
    audit_two_source_repair()
    print("independent three-adjacent-five-cut audit: PASS")
    print("endpoint order, parallel aggregation, and exact cancellation: PASS")
    print("explicit E_2/E_3/E_4 residual decompositions: PASS")
    print("complete quotient identities and defect dimensions 1,1,2: PASS")
    print("4094 fixed-weight proper deletion subfamilies fail: PASS")
    print("two-source mixed-word repair and repaired quotients: PASS")


if __name__ == "__main__":
    main()
