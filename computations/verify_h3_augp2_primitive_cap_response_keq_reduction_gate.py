#!/usr/bin/env python3
"""Reduce AugP2's primitive cap after granting the physical K_Eq lift.

The selected even cap aggregate uses y=(e3+e5)/2 in the five deletion-face
module.  Its primitive cap and invisible K_Eq lift are

    p_y=(-y,-ores_cap),       n_y=(+y,0),

so p_y+n_y is one pure scalar ordinary-residue class in the *cap* word and
P3+K2 grade.  Pointed conormals, centered complete-response gauges, K_Eq,
and d_even all have zero value on that scalar cap-residue coordinate.  The
coarse physical d_ores column lives in a separately typed source summand;
identifying it with the cap residue is precisely the missing placement map.

This checker proves the sharp reduction and guards against a circular use of
the response gauge: the shift z -> z+(k/8)1_12 changes coefficients of an
already granted p_Q/p_ores family and is not an ores-bearing source column
when p is absent.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_centered_endpoint_projector_primitive_cap_lift_gate.py":
        "d5c90e6404670c7b666b6aa2b3448f5f16c2aebc7fac47f749fb269250413a28",
    "computations/verify_h3_pointed_occurrence_primitive_cap_p2_propagation_gate.py":
        "a8dfe952ce4fbbaf71ffd4ef748e456d5284dbf6b71655cce6f2f10576db0d06",
    "computations/verify_h3_centered_base_denominator_deven_composition_gate.py":
        "ee8952a30b9d1a583f3d0e78b8289e5ed839d399d0865b0457315c969c117291",
    "computations/verify_h3_p2_labelled_ores_cut_even_deven_gauge_gate.py":
        "0a4215db2b91843753cc636b489a81f8e30a8c3de234979c74c9f852d74e3d8a",
    "computations/verify_h2_p2_relative_occurrence_graph_resolution_gate.py":
        "4dfb2846c698e5603dadeb1a73add17a7984ccedbad25e3bb09b6aa4170e62ce",
    "computations/verify_h3_degree4_reset_five_face_aggregate_gate.py":
        "01961c9ae83b91dad31ba859ea2f8a2d5775d73d7ad591aa0a369e7d971f8079",
    "computations/verify_h3_rootless_clean_separator_repeated_inventory_gate.py":
        "af9a69ad996bd4390ff3fe9139e357a3bb765292ec969350a948612d9b824fa7",
}
EXPECTED_LEDGER_SHA256 = "b28588d688abd0b90b2bac58373e9c37f342f3f9767f27af702a87d8f6f27824"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def add(*vectors):
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum((Q(vector[index]) for vector in vectors), Q(0))
                 for index in range(len(vectors[0])))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in
                zip(left, right, strict=True)), Q(0))


def rank(columns) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
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
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def unit(index: int, width: int):
    return tuple(Q(int(position == index)) for position in range(width))


def cap_aggregate_audit() -> dict[str, object]:
    # The five physical Cartan paths are the oriented C5 incidence columns.
    edges = []
    for index in range(5):
        edge = [Q(0)] * 5
        edge[index] = -1
        edge[(index + 1) % 5] = 1
        edges.append(tuple(edge))
    epsilon = (Q(1),) * 5
    y = scale(Q(1, 2), add(unit(2, 5), unit(4, 5)))
    require(rank(edges) == 4
            and all(dot(epsilon, edge) == 0 for edge in edges)
            and dot(epsilon, y) == 1,
            "the selected cap aggregate changed")

    # Rows are (five cap Q faces, scalar cap ores).  K_Eq supplies n_y.
    n_y = y + (Q(0),)
    p_y = scale(-1, y) + (Q(-1),)
    z_cap = (Q(0),) * 5 + (Q(-1),)
    require(add(n_y, p_y) == z_cap
            and add(z_cap, scale(-1, n_y)) == p_y,
            "the p/n scalar-residue transgression changed")

    edge_columns = tuple(edge + (Q(0),) for edge in edges)
    old = edge_columns + (n_y,)
    scalar_cap_dual = (Q(0),) * 5 + (Q(1),)
    require(rank(old) == 5 and rank(old + (p_y,)) == 6
            and all(dot(scalar_cap_dual, column) == 0 for column in old)
            and dot(scalar_cap_dual, p_y) == -1,
            "the post-K_Eq primitive cap quotient changed")
    return {
        "face_module": "Q^5 with physical Cartan image ker(sum)",
        "selected_even_aggregate_y": [str(value) for value in y],
        "epsilon_y": "1",
        "physical_K_Eq_invisible_lift_n_y": [str(value) for value in n_y],
        "primitive_cap_p_y": [str(value) for value in p_y],
        "pure_cap_residue_z_cap_equals_p_plus_n": [str(value)
                                                     for value in z_cap],
        "identity": "p_y=z_cap-n_y",
        "rank_before_after_p": [rank(old), rank(old + (p_y,))],
        "post_K_Eq_primitive_dual": "scalar ordinary residue in cap grade",
    }


def expanded_face_independence_audit() -> dict[str, object]:
    # Coordinate blocks:
    # pointed | cap Q^5 | cap scalar ores | coarse scalar ores |
    # labelled ores B^6 | complete response occurrence^12 | Eq.
    widths = (1, 5, 1, 1, 6, 12, 1)
    offsets = []
    current = 0
    for width in widths:
        offsets.append(current)
        current += width
    width = current
    (pointed_offset, q_offset, cap_ores_offset, coarse_ores_offset,
     labelled_offset, response_offset, eq_offset) = offsets

    def vector(entries=()):
        result = [Q(0)] * width
        for index, value in entries:
            result[index] += Q(value)
        return tuple(result)

    p_f = vector(((pointed_offset, 1),))
    k_eq_core = vector(((eq_offset, 1),))
    y_entries = ((q_offset + 2, Q(1, 2)),
                 (q_offset + 4, Q(1, 2)))
    n_y = vector(y_entries)
    p_y = vector(tuple((index, -value) for index, value in y_entries)
                 + ((cap_ores_offset, -1),))
    z_cap = vector(((cap_ores_offset, -1),))
    coarse_d_ores = vector(((coarse_ores_offset, 1),))
    response_gauge = vector(tuple((response_offset + index, 1)
                                  for index in range(12)))
    d_even = vector(((labelled_offset + 1, Q(1, 2)),
                     (labelled_offset + 4, Q(1, 2))))

    cartan = []
    for index in range(5):
        cartan.append(vector(((q_offset + index, -1),
                              (q_offset + (index + 1) % 5, 1))))
    available = tuple(cartan) + (
        p_f, k_eq_core, n_y, coarse_d_ores, response_gauge, d_even,
    )
    cap_ores_dual = unit(cap_ores_offset, width)
    require(all(dot(cap_ores_dual, column) == 0 for column in available)
            and dot(cap_ores_dual, p_y) == -1
            and rank(available + (p_y,)) == rank(available) + 1,
            "P_f/response/K_Eq/d_even unexpectedly constructed p")

    # The coarse d_ores becomes useful only after a physical grade/word
    # transport.  A relative placement cell has boundary
    # cap_ores-coarse_ores; together with coarse d_ores it gives z_cap.
    placement = vector(((cap_ores_offset, -1),
                        (coarse_ores_offset, -1)))
    # Signs: coarse_d_ores=(0,+1); placement=(-cap,-coarse), so their sum is
    # (-cap,0)=z_cap.
    require(add(coarse_d_ores, placement) == z_cap
            and add(z_cap, scale(-1, n_y)) == p_y
            and rank(available + (placement, p_y))
            == rank(available + (placement,)),
            "the relative scalar-residue placement criterion changed")

    # The previous complete-response gauge is an affine coefficient freedom
    # in an already granted p-family.  As an independent old source column it
    # has only the complete-response block and zero cap ores, as displayed.
    require(dot(cap_ores_dual, response_gauge) == 0
            and dot(cap_ores_dual, d_even) == 0,
            "a coefficient gauge acquired a primitive cap residue")
    return {
        "row_blocks": [
            "pointed conormal", "cap Q faces (5)",
            "scalar ores in cap word/grade", "coarse scalar ores",
            "labelled ores B0..B5", "complete response occurrences (12)",
            "complete Eq",
        ],
        "available_columns": [
            "physical C5 Cartan differences", "P_f", "K_Eq core",
            "K_Eq invisible n_y", "coarse d_ores",
            "centered complete-response gauge", "d_even",
        ],
        "p_in_expanded_available_span": False,
        "rank_before_after_p": [rank(available), rank(available + (p_y,))],
        "separating_covector": "scalar cap-ores coordinate",
        "response_gauge_is_independent_ores_column": False,
        "reason_response_gauge_is_circular": (
            "z -> z+(k/8)1_12 changes coefficients of a previously granted "
            "same-labelled p_Q/p_ores family; without p it contributes only "
            "a complete-response row"
        ),
        "d_even_has_scalar_cap_ores": 0,
        "coarse_d_ores_has_scalar_cap_ores": 0,
        "smallest_positive_relative_cell": (
            "a word/fine/repeated-grade placement with boundary "
            "z_cap-d_ores_coarse; equivalently a pure z_cap cell"
        ),
        "after_placement": "p_y=z_cap-n_y",
    }


def terminal_extension_audit() -> dict[str, object]:
    # Local covector weights are (Omega,Q,cap ores,r_terminal).  Granting n
    # forces Q weight zero.  Killing B=(-Omega,+Q,+ores) then forces
    # Omega=ores.  On target-stabilizer eta_z, Omega reads -(5+u_z/t), while
    # Q and ores read zero.  Without a terminal/ridge mate carrying the same
    # readout, the coefficient of the algebraically free u_z/t forces the
    # cap-ores weight to zero.
    #
    # Work symbolically with constant and u_z/t coefficients.  Unknowns are
    # (A,b,d,c), and rows are linear equations from n, endpoint, eta constant,
    # eta variable.  The old terminal mate is zero, so c does not help.
    n_equation = (Q(0), Q(1), Q(0), Q(0))
    endpoint_equation = (Q(-1), Q(1), Q(1), Q(0))
    eta_constant = (Q(-5), Q(0), Q(0), Q(0))
    eta_variable = (Q(-1), Q(0), Q(0), Q(0))
    equations = (n_equation, endpoint_equation,
                 eta_constant, eta_variable)
    require(rank(equations) == 3,
            "the local terminal extension equations changed rank")

    # Any solution has b=0 and A=d=0; c is invisible because no existing
    # terminal comparison has the compensating eta readout.  In particular
    # there is no solution normalized by d=1.
    normalized_d = (Q(0), Q(0), Q(1), Q(0))
    require(rank(equations + (normalized_d,)) == 3,
            "a normalized scalar cap-residue terminal appeared")

    # If a new physical terminal/ridge mate r has eta readout +(5+u/t), the
    # eta equations become -A+c=0 in both coefficients.  A=b? The normalized
    # choice (A,b,d,c)=(1,0,1,1) then kills n, endpoint, and eta.
    promoted = (Q(1), Q(0), Q(1), Q(1))
    require(dot(n_equation, promoted) == 0
            and dot(endpoint_equation, promoted) == 0,
            "the promoted terminal weights stopped killing n/endpoint")
    eta_with_mate_constant = (Q(-5), Q(0), Q(0), Q(5))
    eta_with_mate_variable = (Q(-1), Q(0), Q(0), Q(1))
    require(dot(eta_with_mate_constant, promoted) == 0
            and dot(eta_with_mate_variable, promoted) == 0,
            "the Omega/terminal eta compensation changed")
    return {
        "local_primitive_dual": "scalar ordinary residue in the cap grade",
        "kills_K_Eq_n": True,
        "endpoint_bar_forces": "Omega weight = cap-ores weight",
        "target_stabilizer_pairing": "-A*(5+u_z/t)",
        "normalized_local_dual_extends_with_current_terminal_rows": False,
        "first_terminal_promotion_datum": (
            "a physical rootless/ridge terminal mate with eta_z readout "
            "+(5+u_z/t), target=ores=ainc=0"
        ),
        "exact_complete_alternative": (
            "for the complete physically typed cap-grade matrix J_cap, "
            "either z_cap is in im(J_cap), hence p=z_cap-n, or a left "
            "covector lambda with lambda J_cap=0 and lambda(z_cap)=1 is "
            "the Fredholm terminal; current data do not construct that "
            "extension"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    ledger = {
        "theorem": "AugP2 primitive-cap response/K_Eq reduction gate",
        "pins": PINS,
        "aggregate_cap_quotient": cap_aggregate_audit(),
        "expanded_face_independence": expanded_face_independence_audit(),
        "terminal_extension": terminal_extension_audit(),
        "sharp_verdict": (
            "P_f, the centered complete-response gauge, physical K_Eq, and "
            "d_even do not construct the primitive cap.  After K_Eq the "
            "only missing primal class is the pure scalar ordinary-residue "
            "landing z_cap in word 01211222 and repeated P3+K2, because "
            "p=z_cap-n.  The coarse d_ores column closes this exactly after "
            "one source-valid word/grade placement.  Without that placement "
            "the local scalar-residue dual survives, but promoting it to a "
            "physical terminal still needs the Omega/rootless eta-compatible "
            "comparison or the full augmented left-kernel solve."
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("AugP2 primitive-cap reduction changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("primitive p from P_f + response gauge + K_Eq + d_even: NO")
    print("after K_Eq: p = z_cap - n; only pure scalar cap-residue remains")
    print("coarse d_ores closes p only after word/grade placement")
    print("local cap-residue dual: YES / physical terminal extension: OPEN")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
