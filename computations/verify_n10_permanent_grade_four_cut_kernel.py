#!/usr/bin/env python3
"""Exact smallest kernel among swap-symmetrized N=10 permanent grades.

Quotient the 4,536 ordered opposite-new/distinct-old cross-pair grades by the
endpoint swap.  The resulting 2,268 permanent grades retain both their full
matching tensor and every labelled quadratic cofactor column on all six
adjacent cuts.

Within anchored target-stabilizing character classes, the combined data map
still has a kernel.  The smallest circuit has four permanent grades:

  G_(2,7;22) - G_(3,6;11) + G_(5,7;11) - G_(5,6;22) = 0.

The checker verifies the identity in the full tensor and every quadratic
cofactor column on all six cuts, exhausts all 55,000 possible triples in the
only full-output-dependent character groups, and confirms no smaller
combined circuit.  This is a kernel of the linearized provenance map, not a
finite Krenn counterexample and not a claim that the four coefficients can
be realized in isolation by one rank-one cross-weight product matrix.
"""

from __future__ import annotations

import importlib.util
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations
from pathlib import Path


Q = Fraction
CIRCUIT = (
    (((2, 8, 2, 0), (7, 9, 2, 0)), Q(1)),
    (((3, 8, 1, 0), (6, 9, 1, 0)), Q(-1)),
    (((5, 8, 1, 0), (7, 9, 1, 0)), Q(1)),
    (((5, 8, 2, 0), (6, 9, 2, 0)), Q(-1)),
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_provenance_cancellation():
    path = Path(__file__).with_name(
        "verify_n10_cross_pair_provenance_cancellation.py"
    )
    spec = importlib.util.spec_from_file_location("provenance", path)
    require(spec is not None and spec.loader is not None, "cannot load cancellation audit")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def word_index(word):
    answer = 0
    for colour in word:
        answer = 3 * answer + colour
    return answer


def permanent_representatives(provenance, frontier):
    representatives = []
    seen = set()
    coordinates = frontier.cross_coordinates()
    for left in coordinates:
        if left[1] != 8:
            continue
        for right in coordinates:
            if right[1] != 9 or left[0] == right[0]:
                continue
            pair = (left, right)
            representative = min(pair, provenance.swap_pair(pair))
            if representative in seen:
                continue
            seen.add(representative)
            representatives.append(representative)
    require(len(representatives) == 2_268, "permanent-grade count changed")
    return tuple(representatives)


def character_groups(
    provenance, two_cell, constraint_basis, representatives
):
    groups = defaultdict(list)
    for pair in representatives:
        remainder = two_cell.quotient_remainder(
            provenance.pair_character(pair), constraint_basis
        )
        groups[provenance.exact_key(remainder)].append(pair)
    require(len(groups) == 959, "permanent character-class count changed")
    require(
        Counter(len(records) for records in groups.values())
        == Counter({1: 612, 3: 174, 4: 120, 12: 20, 6: 12, 9: 12, 22: 6, 18: 2, 66: 1}),
        "permanent character-class histogram changed",
    )
    return groups


def full_grades(provenance, module, base, representatives):
    grades = {
        pair: provenance.ordered_pair_grade(
            module, base, pair, provenance.B8, (8, 9)
        )
        for pair in representatives
    }
    require(
        len(
            {
                provenance.projective_tensor_key(grade)
                for grade in grades.values()
            }
        )
        == len(representatives),
        "two distinct permanent grades became proportional",
    )
    return grades


def cofactor_grades(
    provenance,
    frontier,
    forced_pair,
    one_cell,
    module,
    lifted_base,
    pairs,
):
    answer = {}
    for pair in pairs:
        for z in module.S:
            u_set = tuple(vertex for vertex in module.S if vertex != z) + (8, 9)
            answer[(pair, z)] = provenance.mixed_column_components(
                frontier,
                forced_pair,
                one_cell,
                module,
                lifted_base,
                pair,
                u_set,
            )
    return answer


def combined_signature(full_grade, cofactor_table, cuts):
    answer = {word_index(word): coefficient for word, coefficient in full_grade.items()}
    offset = 3**10
    for cut_index, z in enumerate(cuts):
        table = cofactor_table[z]
        labels = tuple(sorted(table))
        require(len(labels) == 21, f"cofactor label count changed at cut {z}")
        for label_index, label in enumerate(labels):
            for index, coefficient in table[label].items():
                key = offset + (cut_index * 21 + label_index) * 3**7 + index
                answer[key] = coefficient
    return answer


def sparse_relation(one_cell, vectors_and_coefficients):
    return one_cell.sparse_linear_combination(
        *((coefficient, vector) for vector, coefficient in vectors_and_coefficients)
    )


def main() -> None:
    provenance = load_provenance_cancellation()
    graded_guard = provenance.load_graded_guard()
    multitrace = graded_guard.load_multitrace()
    frontier = multitrace.load_frontier()
    one_cross = frontier.load_one_cross_edge()
    forced_pair = one_cross.load_forced_pair_contraction()
    certificate = forced_pair.load_positive_moduli_certificate()
    two_cell = certificate.load_two_cell_audit()
    one_cell = two_cell.load_one_cell_elimination()
    unit_gate = one_cell.load_unit_gate()
    module = unit_gate.load_three_cut_verifier()
    base = unit_gate.build_base(module)
    unit_gate.audit_base(module, base)
    lifted_base = forced_pair.lift_cells(module, base)

    support = tuple(
        (left, right, colour_l, colour_r)
        for (left, right), entries in lifted_base.items()
        for colour_l, colour_r, weight in entries
        if weight
    )
    target_characters = tuple(
        {3 * vertex + colour: Q(1) for vertex in provenance.B10}
        for colour in range(3)
    )
    constraint_basis = module.rational_basis(
        [provenance.coordinate_character(coordinate) for coordinate in support]
        + list(target_characters)
    )
    require(len(constraint_basis) == 18, "constraint rank changed")

    representatives = permanent_representatives(provenance, frontier)
    groups = character_groups(
        provenance, two_cell, constraint_basis, representatives
    )
    grades = full_grades(provenance, module, base, representatives)

    full_rank_patterns = Counter()
    dependent_groups = []
    for character, records in groups.items():
        rank = len(module.rational_basis([grades[pair] for pair in records]))
        full_rank_patterns[(len(records), rank)] += 1
        if rank < len(records):
            dependent_groups.append((character, records))
    require(
        full_rank_patterns
        == Counter(
            {
                (1, 1): 612,
                (3, 3): 174,
                (4, 4): 120,
                (12, 12): 20,
                (6, 6): 12,
                (9, 9): 12,
                (22, 15): 6,
                (18, 18): 2,
                (66, 45): 1,
            }
        ),
        "full permanent-grade rank patterns changed",
    )
    require(len(dependent_groups) == 7, "dependent character-group count changed")
    dependent_pairs = {
        pair for _character, records in dependent_groups for pair in records
    }
    require(len(dependent_pairs) == 198, "dependent permanent-grade count changed")

    cofactors = cofactor_grades(
        provenance,
        frontier,
        forced_pair,
        one_cell,
        module,
        lifted_base,
        dependent_pairs,
    )

    def signature(pair, cuts):
        return combined_signature(
            grades[pair],
            {z: cofactors[(pair, z)] for z in cuts},
            cuts,
        )

    all_cut_patterns = Counter()
    for _character, records in dependent_groups:
        rank = len(
            module.rational_basis(
                [signature(pair, tuple(module.S)) for pair in records]
            )
        )
        all_cut_patterns[(len(records), rank)] += 1
    require(
        all_cut_patterns == Counter({(22, 21): 6, (66, 63): 1}),
        "all-cut combined rank patterns changed",
    )

    quartet_patterns = {}
    for candidate in (0, 1, 5):
        cuts = (2, 3, 4, candidate)
        pattern = Counter()
        for _character, records in dependent_groups:
            rank = len(
                module.rational_basis(
                    [signature(pair, cuts) for pair in records]
                )
            )
            pattern[(len(records), rank)] += 1
        require(
            pattern == Counter({(22, 21): 6, (66, 63): 1}),
            f"four-cut combined rank patterns changed at candidate {candidate}",
        )
        quartet_patterns[candidate] = pattern

    # The explicit four-class circuit has zero target-stabilizing character.
    for pair, _coefficient in CIRCUIT:
        require(
            not two_cell.quotient_remainder(
                provenance.pair_character(pair), constraint_basis
            ),
            f"circuit grade left the zero character class at {pair}",
        )
    require(
        not sparse_relation(
            one_cell,
            tuple((grades[pair], coefficient) for pair, coefficient in CIRCUIT),
        ),
        "four-class full tensor circuit changed",
    )
    for z in module.S:
        labels = tuple(sorted(cofactors[(CIRCUIT[0][0], z)]))
        for label in labels:
            require(
                not sparse_relation(
                    one_cell,
                    tuple(
                        (cofactors[(pair, z)][label], coefficient)
                        for pair, coefficient in CIRCUIT
                    ),
                ),
                f"four-class cofactor circuit failed at {(z, label)}",
            )

    # No two-class circuit exists because permanent representatives were
    # chosen from distinct projective full-output classes.  Any combined
    # triple circuit would already be a full-output triple circuit, so it is
    # enough to exhaust triples in the seven full-dependent groups.
    tested_triples = 0
    for _character, records in dependent_groups:
        signatures = {
            pair: signature(pair, tuple(module.S)) for pair in records
        }
        for triple in combinations(records, 3):
            tested_triples += 1
            require(
                len(module.rational_basis([signatures[pair] for pair in triple]))
                == 3,
                f"unexpected combined triple circuit at {triple}",
            )
    require(tested_triples == 55_000, "triple-circuit census changed")

    # The same full circuit persists after an additional isolated old pair.
    circuit12 = []
    shifted_circuit = []
    for pair, coefficient in CIRCUIT:
        shifted = (
            (pair[0][0], 10, pair[0][2], pair[0][3]),
            (pair[1][0], 11, pair[1][2], pair[1][3]),
        )
        grade12 = provenance.ordered_pair_grade(
            module, lifted_base, shifted, provenance.B10, (10, 11)
        )
        circuit12.append((grade12, coefficient))
        shifted_circuit.append((shifted, coefficient))
    require(
        not sparse_relation(one_cell, tuple(circuit12)),
        "four-class full circuit failed after forced-pair lift",
    )
    for z in module.S:
        u_set12 = (
            tuple(vertex for vertex in module.S if vertex != z)
            + (8, 9, 10, 11)
        )
        tables = tuple(
            (
                provenance.mixed_column_components(
                    frontier,
                    forced_pair,
                    one_cell,
                    module,
                    lifted_base,
                    pair,
                    u_set12,
                ),
                coefficient,
            )
            for pair, coefficient in shifted_circuit
        )
        for label in tables[0][0]:
            require(
                not sparse_relation(
                    one_cell,
                    tuple(
                        (table[label], coefficient)
                        for table, coefficient in tables
                    ),
                ),
                f"four-class N=12 cofactor circuit failed at {(z, label)}",
            )

    print("N=10 swap-symmetrized permanent-grade kernel: exact PASS")
    print("permanent grades: 2268 in 959 exact character classes")
    print(f"full rank patterns: {full_rank_patterns}")
    print(f"all-six combined rank patterns: {all_cut_patterns}")
    print(f"fixed-three-plus-candidate patterns: {quartet_patterns}")
    print("smallest combined circuit support: 4 permanent classes")
    print(f"exhaustive independent triples: {tested_triples}")
    print(f"circuit: {CIRCUIT}")
    print("circuit cancels full tensor and every quadratic cofactor on all cuts")
    print("forced-pair full/cofactor stability: exact at N=12")
    print("verdict: symmetrized linear provenance separation is false")


if __name__ == "__main__":
    main()
