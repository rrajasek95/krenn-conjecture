#!/usr/bin/env python3
r"""Exact graph-lock no-go for the standard residual-q KS transport.

The curvature/rootless-bar near-hit leaves

    delta = (P+q00,P-q00,P+q11,P-q11) = (1,-1,-1,1),

where q00=a24:11*a35:11 and q11=a24:21*a35:12.  A correcting
Kodaira--Spencer chain must therefore contribute -delta, with zero main
endpoint boundary and W/target/anchor-incidence readouts.

Project the pinned source inventory to the endpoint-odd sector.  The two
tail changes form the complete square q00,q10,q01,q11.  At every corner the
mixed bar-curvature landing has equal main-boundary and ordinary-residue
coefficient.  Consequently its column is

    g_w = (D_w,R_w) = (e_w,e_w).

Every standard local bar/first-PP edge is g_v-g_w.  The Hasse/Bianchi square
is the unique incidence relation between the four edges.  Endpoint-even
response rows project to zero; matching changes either leave the selected
matching grade or project to the same incidence columns.  Hence the whole
standard two-site transport inventory lies in the graph R=D.

The required correction is residue-only,

    z = (D=0, R=-e_q00+e_q11),

and is detected by the primitive covector Phi_q11=R_q11-D_q11.  This is a
complete no-go for the pinned standard response/bar/PP/Hasse/matching
inventory in the first repeated P3+K2 grade.  It is not an exhaustive
physical source-resolution no-go: a new relative/Spencer comparison cell
can break graph lock, but must also satisfy the already-pinned eta law.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = "1ca1b295c8a9f8ce59696a37dea124a71cea06c084d827ddb92bf2f6e53c989a"
PINS = {
    "computations/verify_h3_shared_four_term_endpoint_word_change_inventory_boundary.py":
        "00db2478df3162a374434ea7d0ab285f770510d33b72619377560404c96b16e8",
    "computations/verify_h3_gl3_normalized_bar_word_change_obstruction.py":
        "ed3c1baafd7d83819c1b6842857611b5b540c57ef95c8ca8a450de357312670a",
    "computations/verify_h3_mixed_bar_curvature_bicomplex.py":
        "6d239dfa1610d36de3385f9e084693523225528f8343ea9412773604fe396318",
    "computations/verify_h3_reciprocal_response_rootless_attachment_parity_gate.py":
        "13aef43505fa09d3c43cf0098598dc62a690598759637820a29672d195139d71",
    "computations/verify_h3_residual_q_physical_duality_interface_counterguard.py":
        "6f7fa68eb081a1dd3c3754cff5e1974e54c4df81c8ce6d36ffe8d37efba953ba",
}

CORNERS = ("q00", "q10", "q01", "q11")
EDGES = (
    ("q00", "q10", "site24"),
    ("q10", "q11", "site35"),
    ("q00", "q01", "site35"),
    ("q01", "q11", "site24"),
)
ROWS = tuple(f"D_{corner}" for corner in CORNERS) + tuple(
    f"R_{corner}" for corner in CORNERS
)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def load(relative: str, name: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def vector(**entries: int) -> tuple[Q, ...]:
    require(set(entries) <= set(ROWS), ("unknown rows", entries))
    return tuple(Q(entries.get(row, 0)) for row in ROWS)


def add(*vectors: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(sum(values, Q(0)) for values in zip(*vectors, strict=True))


def scale(value: int, source: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(Q(value) * entry for entry in source)


def dot(left: tuple[Q, ...], right: tuple[Q, ...]) -> Q:
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def rank(columns: list[tuple[Q, ...]]) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "ragged matrix")
    work = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, height)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(height):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in zip(
                work[row], work[pivot_row], strict=True
            )]
        pivot_row += 1
    return pivot_row


def in_span(columns: list[tuple[Q, ...]], target: tuple[Q, ...]) -> bool:
    return rank(columns) == rank(columns + [target])


def graph_lock_audit() -> dict[str, object]:
    corner_columns = {
        corner: vector(**{f"D_{corner}": 1, f"R_{corner}": 1})
        for corner in CORNERS
    }
    edge_columns = {
        f"{left}->{right}": add(corner_columns[right],
                                scale(-1, corner_columns[left]))
        for left, right, _site in EDGES
    }

    require(rank(list(corner_columns.values())) == 4,
            "corner graph rank changed")
    require(rank(list(edge_columns.values())) == 3,
            "tail-square incidence rank changed")
    require(rank(list(corner_columns.values()) + list(edge_columns.values())) == 4,
            "standard transports escaped the corner graph")

    # The two monotone paths q00->q10->q11 and q00->q01->q11 agree.  This
    # is exactly the first Hasse/Bianchi square and it contributes no column.
    upper_path = add(edge_columns["q00->q10"],
                     edge_columns["q10->q11"])
    lower_path = add(edge_columns["q00->q01"],
                     edge_columns["q01->q11"])
    require(upper_path == lower_path
            == add(corner_columns["q11"],
                   scale(-1, corner_columns["q00"])),
            "Hasse/Bianchi square stopped commuting")

    # Curvature-minus-bar has delta=(P+-P-)(q00-q11).  Its negative is the
    # required residue correction: -q00+q11 in the endpoint-odd projection.
    desired = vector(R_q00=-1, R_q11=1)
    phi_q11 = vector(D_q11=-1, R_q11=1)
    phi_q00 = vector(D_q00=-1, R_q00=1)
    all_standard = list(corner_columns.values()) + list(edge_columns.values())
    require(all(dot(phi_q11, column) == 0 for column in all_standard)
            and all(dot(phi_q00, column) == 0 for column in all_standard),
            "primitive graph cokernel stopped killing the inventory")
    require(dot(phi_q11, desired) == 1
            and dot(phi_q00, desired) == -1,
            "primitive graph cokernel stopped detecting the correction")
    require(not in_span(all_standard, desired),
            "residue-only KS correction entered the standard graph")

    # More directly: on the graph, zero main boundary forces zero residue.
    require(all(column[:4] == column[4:] for column in all_standard),
            "a standard column broke R=D")

    return {
        "tail_corner_order": list(CORNERS),
        "tail_corner_monomials": {
            "q00": "a24:11*a35:11",
            "q10": "a24:21*a35:11",
            "q01": "a24:11*a35:12",
            "q11": "a24:21*a35:12",
        },
        "endpoint_odd_projection_rows": list(ROWS),
        "corner_columns": {
            name: [int(entry) for entry in column]
            for name, column in corner_columns.items()
        },
        "tail_edges": [f"{left}->{right}:{site}"
                       for left, right, site in EDGES],
        "tail_edge_rank": rank(list(edge_columns.values())),
        "hasse_bianchi_square_relation": (
            "(q00->q10)+(q10->q11)="
            "(q00->q01)+(q01->q11)"
        ),
        "full_standard_graph_rank": rank(all_standard),
        "ambient_rank": len(ROWS),
        "standard_law": "R_w=D_w coefficientwise",
        "curvature_minus_bar_delta_full_residue_basis": [1, -1, -1, 1],
        "required_correction_minus_delta_full_residue_basis": [-1, 1, 1, -1],
        "required_correction_endpoint_odd_projection": [
            int(entry) for entry in desired
        ],
        "required_main_boundary": [0, 0, 0, 0],
        "required_protected_readouts": {"W": 0, "target": 0, "ainc": 0},
        "primitive_separators": {
            "Phi_q11=R_q11-D_q11": [int(entry) for entry in phi_q11],
            "Phi_q00=R_q00-D_q00": [int(entry) for entry in phi_q00],
        },
        "separator_pairings_with_required_correction": [1, -1],
        "required_correction_in_standard_span": False,
    }


def pinned_inventory_audit() -> dict[str, object]:
    shared = load(
        "computations/verify_h3_shared_four_term_endpoint_word_change_inventory_boundary.py",
        "residual_q_graph_shared",
    )
    normalized = load(
        "computations/verify_h3_gl3_normalized_bar_word_change_obstruction.py",
        "residual_q_graph_normalized_bar",
    )
    mixed = load(
        "computations/verify_h3_mixed_bar_curvature_bicomplex.py",
        "residual_q_graph_mixed_curvature",
    )
    reciprocal = load(
        "computations/verify_h3_reciprocal_response_rootless_attachment_parity_gate.py",
        "residual_q_graph_reciprocal",
    )
    physical = load(
        "computations/verify_h3_residual_q_physical_duality_interface_counterguard.py",
        "residual_q_graph_physical_interface",
    )

    curvature = shared.curvature_kodaira_spencer_audit()
    candidate = curvature["combined_candidate"]
    require(candidate["residue_vector"] == [1, -1, -1, 1]
            and not candidate["residue_zero"],
            "curvature/rootless residual delta changed")
    require(curvature["mixed_bar_curvature"]["target"] == 0,
            "mixed-curvature target changed")

    sample = {
        "A": Q(2), "B": Q(3), "F": Q(5), "U": Q(11), "z": Q(1),
        "x": Q(7), "y": Q(-2), "t": Q(4), "v": Q(3),
        "Ecoef": Q(5, 2),
    }
    packet = mixed.audit_bicomplex(sample)
    require(packet["L_q_augmentation"]
            == packet["L_old_ordinary_residue"],
            "mixed-curvature endpoint/residue graph law changed")
    require(packet["target_complete_seven_site_word"] == 0,
            "mixed-curvature complete-word target changed")

    square = normalized.cube_audit(2, audit_all_shuffles=True)
    require(square["vertices"] == 4 and square["edges"] == 4
            and square["incidence_rank"] == 3
            and square["h0_dimension"] == 1,
            "complete two-site normalized bar square changed")

    parity = reciprocal.parity_and_residue_gate()
    require(parity["ordinary_residue_of_every_endpoint_odd_response"] == 0,
            "endpoint-odd response acquired ordinary residue")
    require(parity["exact_reciprocal_endpoint_projection"] == [1, 1],
            "reciprocal response stopped being endpoint-even")

    # Replay the bounded literal response/unary and bar/PP/Hasse/matching
    # censuses.  They establish that nothing outside the local tail square
    # contributes a new endpoint-odd column in this pinned inventory.
    response = shared.complete_response_and_unary_search()
    other = shared.bar_bianchi_hasse_pp_matching_search()
    require(response["complete_response_rows"] == 3 ** 6
            and response["unique_hit_endpoint_coefficients"] == [1, 1]
            and response["chi_on_every_correct_tail_response"] == 0,
            "complete response projection changed")
    require(other["fourth_Hasse"]["formal_candidate_source_valid"] is False
            and other["principal_parts"][
                "formal_difference_is_available_source_column"] is False
            and other["matching_square"][
                "ordinary_matching_or_Tate_cell_supplies_it"] is False,
            "pinned PP/Hasse/matching exclusion changed")

    require(tuple(physical.DELTA) == (Q(1), Q(-1), Q(-1), Q(1))
            and tuple(physical.NEGATIVE_DELTA)
            == (Q(-1), Q(1), Q(1), Q(-1)),
            "physical interface correction sign changed")

    return {
        "common_word": "1211222",
        "first_common_fine_grade": "labelled repeated P3+K2",
        "normalized_two_site_square": square,
        "mixed_curvature_qaug_equals_ordinary_residue": True,
        "complete_response_row_count": response["complete_response_rows"],
        "correct_tail_response_endpoint_projection": [1, 1],
        "correct_tail_response_endpoint_odd_projection": 0,
        "reciprocal_K_antisymmetrization": 0,
        "literal_fourth_Hasse_candidate_source_valid": False,
        "literal_first_PP_difference_available": False,
        "ordinary_matching_or_Tate_cell_supplies_correction": False,
        "inventory_projection": {
            "endpoint-even_response_rows": "zero",
            "mixed_curvature_corner": "g_w=(e_w,e_w)",
            "local_bar_or_first_PP": "g_v-g_w",
            "Hasse_or_Bianchi_square": "one incidence relation; no new rank",
            "matching_switch": (
                "different selected-matching grade, or the same incidence "
                "projection after alignment"
            ),
        },
        "physical_eta_promotion_already_required": True,
        "source_resolution_exhaustive": False,
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "pinned_inventory": pinned_inventory_audit(),
        "standard_transport_graph_lock": graph_lock_audit(),
        "smallest_new_cell": {
            "type": "relative/Spencer residual-q comparison generator",
            "endpoint_odd_main_boundary": [0, 0, 0, 0],
            "ordinary_residue": "-q00+q11 (equivalently -delta before odd projection)",
            "W_target_ainc": [0, 0, 0],
            "must_break": "R=D graph lock",
            "additional_physical_eta_law": (
                "d r_v(eta_z)=-d Omega_v(eta_z)="
                "1+delta_(vz)u_z/t, with aggregate compensation 5+u_z/t"
            ),
            "generator_count_forced_by_current_obstructions": 1,
            "count_interpretation": (
                "graph breaking and eta compatibility are two independent "
                "readout conditions on one possible relative/Spencer cell; "
                "the current ranks do not force two separate generators"
            ),
        },
        "verdict": (
            "no source-valid column in the pinned standard response/bar/PP/"
            "Hasse/matching inventory supplies the residual-q KS correction: "
            "after endpoint-odd projection every available two-site transport "
            "has R=D, while the required -delta correction has D=0 and R!=0. "
            "A genuinely relative/Spencer comparison cell is the first "
            "possible graph-breaking object; the full physical source census "
            "remains open"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, ledger))
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    print("h=3 residual-q standard KS transport graph lock: PASS")
    print("tail edge rank / graph rank: 3 / 4")
    print("required correction in standard span: False")
    print("primitive separator pairings: 1 / -1")
    print("ledger_sha256:", digest)


if __name__ == "__main__":
    main()
