#!/usr/bin/env python3
r"""Can the eta primitive and residual-q correction be one physical cell?

Two exact local requirements have been isolated in the same rootless
frontier:

  residue:  -delta=(-1,1,1,-1),
  eta:      c_v=t-u_v, so eta_z(c_v)=1+delta_(vz)u_z/t.

They cannot be combined by treating c_v as an ordinary coefficient of the
residual correction.  The cells t=q_pq^00 and u_v=q_xv^00 have different
full site degrees.  Adding the same residual tail preserves that mismatch;
the minimal complementary homogenization is the zero identity

  u_v*(t*delta)-t*(u_v*delta)=0.

Nor is c_v the complete terminal law: the further physical stabilizer
sigma_(p,2)-(x,2) fixes t,u_v but moves Omega_v+c_v by q_pq^22.  A physical
one-cell realization must therefore carry a third, hidden terminal response
-q_pq^22 facewise.

There is no incompatibility at the augmented-row level.  The residue packet,
eta packet, and sigma correction have the same zero main-boundary/W/target/
anchor landing, so they define one element of the formal fiber product.  A
single new relative/Spencer cell is algebraically sufficient.  Its actual
existence is exactly membership of that element in the image of the complete
source-labelled physical map; none of the pinned files proves this image
membership.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = "cb1dace33e0557afc263026ecac86927d2013706cc3735e0f2a658957bf295f7"
PINS = {
    "computations/verify_h3_residual_q_ks_standard_transport_graph_lock.py":
        "eede8aabd5c4740520ed13f1aacc897326a3a02573f860f5b2613c9df91fd53c",
    "computations/verify_h3_rootless_eta_cyclic_compensation_boundary.py":
        "9beab390c8ed2c89f1a8f62ee54857c03199fecd5ad9a69ab6f29d6a04140b6d",
    "computations/verify_h3_rootless_eta_character_source_interface.py":
        "2357e1a4e1c22c4496d99be12b8bf49deea3838337743ea849da29757508517c",
    "computations/verify_h3_residual_q_physical_duality_interface_counterguard.py":
        "6f7fa68eb081a1dd3c3754cff5e1974e54c4df81c8ce6d36ffe8d37efba953ba",
}

FACES = (1, 2, 3, 4, 5)
SITES = tuple(range(8))
X, P, QSITE = 0, 6, 7
CORNERS = ("q00", "q10", "q01", "q11")
RESIDUAL_ROWS = tuple(f"D_{corner}" for corner in CORNERS) + tuple(
    f"R_{corner}" for corner in CORNERS
)
ETA_ROWS = tuple(f"eta{z}_constant" for z in FACES) + tuple(
    f"eta{z}_U{z}" for z in FACES
)
ROWS = RESIDUAL_ROWS + ETA_ROWS + (
    "sigma_qpq22", "W", "target", "ainc",
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


def vector(**entries: int) -> tuple[Q, ...]:
    require(set(entries) <= set(ROWS), ("unknown row", entries))
    return tuple(Q(entries.get(row, 0)) for row in ROWS)


def add(*vectors: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(sum(values, Q(0)) for values in zip(*vectors, strict=True))


def scale(value: int, source: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(Q(value) * entry for entry in source)


def dot(left, right) -> Q:
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def rank(columns: list[tuple[Q, ...]]) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "ragged matrix")
    matrix = [[Q(columns[column][row]) for column in range(len(columns))]
              for row in range(height)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, height)
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for row in range(height):
            if row == pivot_row or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [left - value * right for left, right in zip(
                matrix[row], matrix[pivot_row], strict=True
            )]
        pivot_row += 1
    return pivot_row


def site_degree(*sites: int) -> tuple[int, ...]:
    return tuple(int(site in sites) for site in SITES)


def degree_add(left, right):
    return tuple(a + b for a, b in zip(left, right, strict=True))


def degree_subtract(left, right):
    return tuple(a - b for a, b in zip(left, right, strict=True))


def coefficient_multigrading_no_go(source_interface) -> dict[str, object]:
    source_gate = source_interface.stabilizer_and_degree_no_go()
    degree_t = site_degree(P, QSITE)
    require(source_gate["site_degree_t"] == list(degree_t),
            "marked t degree changed")

    records = []
    # The proof is independent of the residual grade g: it cancels from the
    # difference.  Use a nonconstant symbolic witness vector to guard the
    # implementation as well as recording the exact identity.
    residual_grade = tuple(index + 2 for index in SITES)
    for face in FACES:
        degree_u = site_degree(X, face)
        require(source_gate["site_degrees_u"][str(face)] == list(degree_u),
                ("marked u degree changed", face))
        t_delta = degree_add(degree_t, residual_grade)
        u_delta = degree_add(degree_u, residual_grade)
        require(t_delta != u_delta,
                "multiplying delta made t and u homogeneous")
        require(degree_subtract(t_delta, u_delta)
                == degree_subtract(degree_t, degree_u),
                "the common residual grade did not cancel")

        # Since the supports of t and u_v are disjoint, their lcm degree is
        # degree_t+degree_u.  Complementing t*delta by u and u*delta by t
        # gives the identical labelled monomial t*u*delta on both sides.
        lcm = degree_add(degree_t, degree_u)
        left_completion = degree_add(degree_u, degree_t)
        right_completion = degree_add(degree_t, degree_u)
        require(left_completion == right_completion == lcm,
                "minimal complementary degree changed")
        formal_delta = (Q(-1), Q(1), Q(1), Q(-1))
        require(add(formal_delta, scale(-1, formal_delta)) == (Q(0),) * 4,
                "complementary homogenization stopped being tautological")
        records.append({
            "face": face,
            "deg_t": list(degree_t),
            "deg_u_v": list(degree_u),
            "deg_t_plus_g_equals_deg_u_plus_g": False,
            "degree_difference": list(
                degree_subtract(degree_t, degree_u)
            ),
            "minimal_complementary_lcm": list(lcm),
            "homogenized_expression":
                "u_v*(t*(-delta))-t*(u_v*(-delta))=0",
        })

    return {
        "records": records,
        "common_tail_or_residual_grade_repairs_mismatch": False,
        "ordinary_product_(t-u_v)*(-delta)_is_homogeneous": False,
        "ordinary_product_also_has_wrong_residue":
            "-(t-u_v)*delta rather than -delta",
        "minimal_polynomial_homogenization_is_zero": True,
        "consequence": (
            "c_v may be a normalized terminal value of a relative cell, "
            "but it is not a coefficient-ring multiplier of the residual "
            "correction in one physical source grade"
        ),
    }


def eta_and_full_stabilizer_gate(eta, source_interface) -> dict[str, object]:
    eta_gate = eta.compensation_audit()
    source_gate = source_interface.stabilizer_and_degree_no_go()
    require(eta_gate["facewise_rootless_value"] == "r_v^comp=t-u_v",
            "eta primitive changed")
    require(source_gate["derivative_of_corrected_scalar"]
            == "5*q_pq^22"
            and not source_gate["marked_cell_scalar_repairs_full_kernel"],
            "full stabilizer scalar no-go changed")

    records = []
    for face in FACES:
        eta_entries = {
            **{f"eta{z}_constant": 1 for z in FACES},
            f"eta{face}_U{face}": 1,
        }
        c_packet = vector(**eta_entries)
        # The further sigma fixes t and u_v, so the literal affine primitive
        # contributes zero in the sigma row.  But Omega_v+c_v transforms by
        # +q_pq22, requiring a hidden -q_pq22 terminal component.
        require(c_packet[ROWS.index("sigma_qpq22")] == 0,
                "literal c_v acquired a sigma response")
        required_terminal = add(c_packet, vector(sigma_qpq22=-1))
        records.append({
            "face": face,
            "eta_terminal_law":
                f"1+delta_({face},z)*u_z/t",
            "literal_c_v_sigma_qpq22": 0,
            "sigma_on_Omega_v_plus_c_v": "+q_pq^22",
            "additional_hidden_terminal_requirement": "-q_pq^22",
            "formal_terminal_packet": [str(x) for x in required_terminal],
        })

    return {
        "records": records,
        "eta_primitive_is_exact_on_marked_clean_slice": True,
        "eta_primitive_is_complete_full_kernel_terminal": False,
        "aggregate_sigma_failure_of_sum_Omega_plus_c": "5*q_pq^22",
        "residual_signature_minus_delta_implies_sigma_correction": False,
        "reason": (
            "ordinary residue and full-stabilizer terminal response are "
            "independent augmented rows; the former does not determine the latter"
        ),
    }


def one_cell_fiber_product(graph, physical) -> dict[str, object]:
    graph_ledger, graph_digest = graph.audit()
    require(graph_digest == graph.EXPECTED_LEDGER_SHA256,
            "standard graph-lock ledger changed")
    graph_gate = graph_ledger["standard_transport_graph_lock"]
    require(graph_gate["required_correction_in_standard_span"] is False,
            "residual correction entered the standard source image")
    require(tuple(physical.NEGATIVE_DELTA)
            == (Q(-1), Q(1), Q(1), Q(-1)),
            "full four-corner correction sign changed")

    # Work at one face v=1; cyclic relabelling gives the other four.  The
    # endpoint-odd correction is R_q00=-1,R_q11=+1 with D=0.
    residual = vector(R_q00=-1, R_q11=1)
    eta_entries = {
        **{f"eta{z}_constant": 1 for z in FACES},
        "eta1_U1": 1,
    }
    eta_only = vector(**eta_entries)
    naive_pair = add(residual, eta_only)
    full_terminal = vector(**eta_entries, sigma_qpq22=-1)
    desired = add(residual, full_terminal)

    protected = ("W", "target", "ainc")
    require(all(desired[ROWS.index(row)] == 0 for row in protected),
            "fiber target acquired a protected readout")
    require(all(desired[ROWS.index(f"D_{corner}")] == 0
                for corner in CORNERS),
            "fiber target acquired main endpoint boundary")
    require(sum(desired[ROWS.index(f"R_{corner}")]
                for corner in CORNERS) == 0,
            "residual packet is not tail-incidence closed")
    require(desired[ROWS.index("sigma_qpq22")] == -1
            and naive_pair[ROWS.index("sigma_qpq22")] == 0,
            "full stabilizer completion changed")

    # Extend the complete standard graph columns by zero in the new rows.
    standard = []
    for corner in CORNERS:
        standard.append(vector(**{
            f"D_{corner}": 1, f"R_{corner}": 1,
        }))
    phi = vector(D_q11=-1, R_q11=1)
    require(all(dot(phi, column) == 0 for column in standard)
            and dot(phi, desired) == 1,
            "fiber target lost its primitive graph-breaking projection")
    require(rank(standard) == 4
            and rank(standard + [desired]) == 5,
            "one formal fiber column no longer supplies the rank jump")

    return {
        "base_rows_shared_by_both_interfaces": [
            "endpoint-odd main boundary D=0",
            "W=0", "target=0", "anchor incidence=0",
            "word 1211222", "labelled repeated P3+K2 comparison grade",
        ],
        "residual_projection": {
            "full_four_corner_value": [-1, 1, 1, -1],
            "endpoint_odd_value": "R_q00=-1, R_q11=+1",
            "tail_incidence_closed": True,
            "in_standard_source_image": False,
        },
        "terminal_projection_on_face_1": {
            "eta_z": "1+delta_(1,z)*u_z/t",
            "sigma_qpq22": -1,
        },
        "naive_(minus_delta,c_v)_misses_sigma": True,
        "formal_fiber_target": [str(x) for x in desired],
        "formal_compatibility_obstruction": False,
        "one_new_column_algebraically_sufficient": True,
        "one_new_column_forced_by_current_rank": True,
        "physical_criterion": (
            "let Psi_v be the complete source-labelled relative/Spencer map "
            "in the fixed word/grade to the fiber product of residual and "
            "terminal packets over the zero D/W/target/ainc base.  One "
            "physical cell exists iff the displayed formal fiber target lies "
            "in im(Psi_v)"
        ),
        "physical_image_membership_proved": False,
        "why_not": (
            "ordinary multiplication by t-u_v is multigraded-invalid and "
            "sigma-incomplete; no committed relative source generator maps "
            "to the displayed three-projection packet"
        ),
    }


def main() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    graph = load(
        "computations/verify_h3_residual_q_ks_standard_transport_graph_lock.py",
        "eta_residual_fiber_graph",
    )
    eta = load(
        "computations/verify_h3_rootless_eta_cyclic_compensation_boundary.py",
        "eta_residual_fiber_eta",
    )
    source_interface = load(
        "computations/verify_h3_rootless_eta_character_source_interface.py",
        "eta_residual_fiber_source",
    )
    physical = load(
        "computations/verify_h3_residual_q_physical_duality_interface_counterguard.py",
        "eta_residual_fiber_physical",
    )

    ledger = {
        "theorem": "residual-q/eta one-cell fiber-product gate",
        "coefficient_combination_no_go":
            coefficient_multigrading_no_go(source_interface),
        "physical_stabilizer_completion":
            eta_and_full_stabilizer_gate(eta, source_interface),
        "one_cell_fiber_product": one_cell_fiber_product(graph, physical),
        "verdict": {
            "actual_source_cell_constructed": False,
            "literal_(t-u_v)_times_minus_delta_valid": False,
            "minus_delta_plus_eta_primitive_physically_complete": False,
            "sharpest_positive_statement": (
                "one relative/Spencer cell can algebraically carry all three "
                "required projections; its existence is one exact fiber-product "
                "image-membership theorem, not two independent constructions"
            ),
            "additional_full_kernel_row":
                "sigma terminal correction -q_pq^22 facewise",
        },
        "scope": (
            "exact for the pinned standard residual graph, marked clean eta "
            "slice, first extra full stabilizer, and full site multigrading. "
            "No claim of an exhaustive relative source resolution"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))

    print("h3 residual-q/eta one-cell fiber product: SHARP INTERFACE")
    print("literal (t-u_v)*(-delta) source-valid: NO")
    print("naive (-delta,c_v) full-stabilizer complete: NO")
    print("additional sigma row: -q_pq^22 facewise")
    print("one relative cell algebraically sufficient: YES")
    print("physical source image membership: OPEN")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
