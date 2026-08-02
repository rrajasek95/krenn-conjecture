#!/usr/bin/env python3
"""Linear L0 obstruction to the exact 1I+5Z rank-55 guard.

Research evidence only.  Krenn's conjecture remains open, SP-CLEAN-BRIDGE is
untouched, and no certified dependency changes.

The residual packet from verify_level_two_one_invertible_five_zero_r2_guard.py
has rank(dPsi)=55, but neither pure binary target e_(0^6), e_(1^6) lies in
the differential image.  This excludes that fixed packet from any full
eight-site completion.  It does not exclude the full 1I+5Z stratum or assert
anything about other residual packets.

Standard library only; all assertions remain active under -O and -I -S.
"""

from itertools import combinations, product
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
SOURCE = run_path(str(
    HERE / "verify_level_two_one_invertible_five_zero_r2_guard.py"
))
L0 = run_path(str(
    HERE / "verify_level_two_three_invertible_l0_obstruction.py"
))

SITES = tuple(range(6))
COLOURS = (0, 1)
WORDS = tuple(product(COLOURS, repeat=6))
PACKET = SOURCE["build_internal_packet"]()


def append_columns(matrix, *columns):
    require(
        all(len(column) == len(matrix) for column in columns),
        "an augmented column has the wrong height",
    )
    return [
        row[:] + [column[index] for column in columns]
        for index, row in enumerate(matrix)
    ]


def ranks_over_three_fields(matrix):
    return (
        L0["rational_rank"](matrix),
        L0["modular_rank"](matrix, 101),
        L0["modular_rank"](matrix, 1_000_003),
    )


def audit_source_guard():
    derivative, slope = SOURCE["audit_differential"](PACKET)
    p_star, q_star, potentials, direct = SOURCE["endpoint_data"]()
    endpoint_ranks = SOURCE["audit_endpoint_ranks_and_generic_kernel"](
        PACKET, p_star, q_star, potentials
    )
    eight_packet = SOURCE["audit_selected_equations"](
        PACKET, derivative, slope, p_star, q_star, direct
    )
    r2 = SOURCE["audit_selected_residual_r2"](eight_packet)
    require(endpoint_ranks == (2, 0, 0, 0, 0, 0),
            ("source endpoint ranks changed", endpoint_ranks))
    require(len(r2) == 6, ("source residual R2 audit changed", len(r2)))
    return derivative, slope, endpoint_ranks, r2


def audit_l0_slice_formula():
    # Rebind the universal matching-partition audit to this exact residual
    # packet.  All formal endpoint monomials remain independent counters.
    names = (
        "literal_slice_counter",
        "derived_slice_counter",
        "audit_matching_partition_and_slice_formula",
    )
    globals_dict = L0[names[0]].__globals__
    require(
        all(L0[name].__globals__ is globals_dict for name in names),
        "the imported formal L0 audits no longer share globals",
    )
    globals_dict["M"] = PACKET
    checked = L0["audit_matching_partition_and_slice_formula"]()
    require(checked == 256, ("formal L0 slice count changed", checked))
    return checked


def audit_euler_and_incidence():
    slope = L0["matching_tensor"](PACKET)
    require(
        L0["apply_differential"](PACKET, PACKET)
        == [3 * value for value in slope],
        "Euler identity dPsi_M(M)=3 Psi(M) failed",
    )

    derivative = L0["differential_matrix"](PACKET)
    pure_zero = [int(word == (0,) * 6) for word in WORDS]
    pure_one = [int(word == (1,) * 6) for word in WORDS]
    mixed = [
        row
        for row, word in zip(derivative, WORDS)
        if word not in ((0,) * 6, (1,) * 6)
    ]
    ranks = {
        "D": ranks_over_three_fields(derivative),
        "D_mixed": ranks_over_three_fields(mixed),
        "D|e0": ranks_over_three_fields(
            append_columns(derivative, pure_zero)
        ),
        "D|e1": ranks_over_three_fields(
            append_columns(derivative, pure_one)
        ),
        "D|e0,e1": ranks_over_three_fields(
            append_columns(derivative, pure_zero, pure_one)
        ),
    }
    require(
        ranks == {
            "D": (55, 55, 55),
            "D_mixed": (55, 55, 55),
            "D|e0": (56, 56, 56),
            "D|e1": (56, 56, 56),
            "D|e0,e1": (57, 57, 57),
        },
        ("pure-target L0 incidence ranks changed", ranks),
    )
    return ranks


def audit_completion_scope():
    total_ternary_cells = (
        len(tuple(combinations(range(8), 2))) * 3 * 3
    )
    residual_binary_cells = (
        len(tuple(combinations(SITES, 2))) * 2 * 2
    )
    outside_cells = total_ternary_cells - residual_binary_cells
    require(
        (total_ternary_cells, residual_binary_cells, outside_cells)
        == (252, 60, 192),
        "residual/outside cell scope changed",
    )
    return residual_binary_cells, outside_cells


def main():
    _derivative, _slope, endpoint_ranks, r2 = audit_source_guard()
    formal_slices = audit_l0_slice_formula()
    ranks = audit_euler_and_incidence()
    residual_cells, outside_cells = audit_completion_scope()
    print("one-invertible five-zero L0 obstruction: all checks passed")
    print(f"  source endpoint ranks       : {endpoint_ranks}")
    print(f"  selected residual R2 rows   : {len(r2)}/6")
    print(f"  formal L0 slices            : {formal_slices}/256")
    print(f"  pure-target incidence ranks : {ranks}")
    print(
        "  completion scope           : "
        f"{residual_cells} fixed residual cells; "
        f"{outside_cells} outside cells cannot repair"
    )
    print("  conclusion                 : exact packet excluded; stratum open")


if __name__ == "__main__":
    main()
