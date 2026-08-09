#!/usr/bin/env python3
"""Exact exclusion of every permanent-zero cross source on the anchored N=10 lift.

If all swap-symmetrized quadratic cross permanents vanish, the full matching
tensor is exactly the isolated forced-pair lift and every quadratic cofactor
contribution vanishes.  The only change in a cut cylinder is therefore the
linear sum of one-cross cofactor directions.

For each cut this checker builds a universal superspace containing the base
cofactor columns and every linear direction from all 144 cross coordinates,
independently.  The actual cofactor span of any permanent-zero source is a
subspace of it.  Exact quotient reduction finds a forced-lift residual row
outside this universal space on every one of the six cuts.  Consequently no
permanent-zero cross source can have even one complete high-sector cylinder,
so it cannot preserve the fixed triple or create a fourth.
"""

from __future__ import annotations

import importlib.util
from fractions import Fraction
from pathlib import Path


Q = Fraction


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_rank_one_intersection():
    path = Path(__file__).with_name(
        "verify_n10_permanent_kernel_rank_one_intersection.py"
    )
    spec = importlib.util.spec_from_file_location("rank_one", path)
    require(spec is not None and spec.loader is not None, "cannot load rank-one audit")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def expected_bad_rows():
    return {
        0: {
            (1, 1, 1): {1089: Q(1), 1097: Q(1)},
            (2, 2, 2): {2178: Q(1), 2182: Q(1)},
            (0, 0, 0): {567: Q(1)},
            (0, 1, 2): {567: Q(1), 571: Q(1), 575: Q(1)},
        },
        1: {
            (1, 1, 1): {1089: Q(1), 1097: Q(1)},
            (2, 2, 2): {2178: Q(1), 2182: Q(1)},
            (0, 0, 0): {567: Q(1)},
            (0, 1, 2): {567: Q(1), 571: Q(1), 575: Q(1)},
        },
        2: {(1, 1, 1): {1089: Q(1), 1097: Q(1)}},
        3: {(2, 2, 2): {2178: Q(1), 2182: Q(1)}},
        4: {
            (1, 1, 1): {1089: Q(1), 1097: Q(1)},
            (2, 2, 2): {2178: Q(1), 2182: Q(1)},
        },
        5: {
            (0, 0, 0): {1350: Q(1), 189: Q(1)},
            (0, 1, 2): {189: Q(1), 193: Q(1), 197: Q(1)},
        },
    }


def main() -> None:
    rank_one = load_rank_one_intersection()
    permanent_kernel = rank_one.load_permanent_kernel()
    provenance = permanent_kernel.load_provenance_cancellation()
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
    base_tensor10 = module.matching_tensor(provenance.B10, lifted_base)
    residual10 = forced_pair.tensor_difference(
        base_tensor10, forced_pair.delta_tensor(provenance.B10)
    )

    coordinates = frontier.cross_coordinates()
    require(len(coordinates) == 144, "cross-coordinate census changed")
    universal_records = {}
    expected_ranks = {0: 126, 1: 126, 2: 126, 3: 126, 4: 126, 5: 135}
    expected_bad = expected_bad_rows()

    for z in module.S:
        u_set = tuple(vertex for vertex in module.S if vertex != z) + (8, 9)
        base_columns = forced_pair.insertion_columns(module, u_set, lifted_base)
        universal_generators = list(base_columns.values())

        for coordinate in coordinates:
            cells1 = provenance.add_weighted_coordinates(
                module, lifted_base, ((coordinate, Q(1)),)
            )
            cells2 = provenance.add_weighted_coordinates(
                module, lifted_base, ((coordinate, Q(2)),)
            )
            require(
                module.matching_tensor(provenance.B10, cells1) == base_tensor10
                and module.matching_tensor(provenance.B10, cells2) == base_tensor10,
                f"one cross coordinate entered the full tensor at {coordinate}",
            )
            columns1 = forced_pair.insertion_columns(module, u_set, cells1)
            columns2 = forced_pair.insertion_columns(module, u_set, cells2)
            for label, base_column in base_columns.items():
                derivative = one_cell.sparse_difference(
                    columns1[label], base_column
                )
                require(
                    one_cell.sparse_difference(columns2[label], base_column)
                    == {index: 2 * value for index, value in derivative.items()},
                    f"one-cross column direction is not affine at {(z, coordinate, label)}",
                )
                universal_generators.append(derivative)

        universal_basis = module.rational_basis(universal_generators)
        require(
            len(universal_basis) == expected_ranks[z],
            f"universal linear cylinder rank changed at cut {z}",
        )
        rows = forced_pair.flatten_rows(
            residual10,
            provenance.B10,
            (z, 6, 7),
            u_set,
        )
        bad_rows = {
            word: two_cell.quotient_remainder(row, universal_basis)
            for word, row in rows.items()
            if not module.rational_member(row, universal_basis)
        }
        require(
            bad_rows == expected_bad[z],
            f"universal linear quotient witnesses changed at cut {z}",
        )
        universal_records[z] = (len(universal_basis), bad_rows)

    # Rebuild the smallest nontrivial permanent-zero block.  Its full tensor
    # and pure anchors are unchanged, its actual cofactor spaces lie in the
    # audited universal spaces, and no cut is complete.
    zero_block = (
        (provenance.PAIR_A[0], Q(1)),
        (provenance.PAIR_A[1], Q(1)),
        (provenance.PAIR_B[0], Q(1)),
        (provenance.PAIR_B[1], Q(-1)),
    )
    zero_cells = provenance.add_weighted_coordinates(
        module, lifted_base, zero_block
    )
    zero_tensor = module.matching_tensor(provenance.B10, zero_cells)
    require(zero_tensor == base_tensor10, "zero block changed the full tensor")
    pure_words = tuple((colour,) * 10 for colour in range(3))
    require(
        tuple(zero_tensor.get(word, Q(0)) for word in pure_words) == (1, 1, 1),
        "zero block changed the three pure anchors",
    )
    actual_records = {}
    for z in module.S:
        u_set = tuple(vertex for vertex in module.S if vertex != z) + (8, 9)
        columns = forced_pair.insertion_columns(module, u_set, zero_cells)
        basis = module.rational_basis(list(columns.values()))
        rows = forced_pair.flatten_rows(
            residual10,
            provenance.B10,
            (z, 6, 7),
            u_set,
        )
        full = all(module.rational_member(row, basis) for row in rows.values())
        actual_records[z] = (len(basis), full)
    require(
        actual_records
        == {
            0: (19, False),
            1: (19, False),
            2: (20, False),
            3: (20, False),
            4: (20, False),
            5: (21, False),
        },
        "smallest permanent-zero block cut census changed",
    )

    print("N=10 permanent-zero cross linear-superspace exclusion: exact PASS")
    print("cross coordinates included independently: 144")
    print(f"universal cut records: {universal_records}")
    print("every universal cylinder has a nonzero forced-residual quotient row")
    print("source-level verdict: no permanent-zero cross source has a complete cut")
    print("fixed cuts 2,3,4 therefore cannot be preserved at N=10")
    print("smallest nontrivial four-cell zero block preserves all pure anchors")
    print(f"four-cell actual cut census: {actual_records}")
    print("verdict: permanent-zero lower-degree rescue excluded on anchored model")
    print("scope: nonzero permanent grades and arbitrary N-stability remain separate")


if __name__ == "__main__":
    main()
