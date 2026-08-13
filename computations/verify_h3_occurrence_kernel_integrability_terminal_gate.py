#!/usr/bin/env python3
"""Classify what a surviving pointed-occurrence tangent actually yields.

For the complete h=3 endpoint-plus-q Jacobian A on 171 columns, a surviving
pointed class H=P_f modulo row(A) gives xi in ker(A) with H(xi)!=0.  This is
only first-order data.  It does not by itself delete support and it does not
already define a Macaulay terminal.

The first nonlinear source condition is the second Hasse obstruction

    o2 = [F_[2](xi)] in coker(A).

If o2 vanishes, choose a second jet and continue; support deletion still
requires an anchor-safe exact line or a global arc meeting the boundary.  If
o2 is nonzero, Fredholm duality gives an output covector psi killing im(A)
and detecting o2.  Promotion of psi to the physical augmented terminal is a
separate extension problem, equivalent to psi killing the intersection of
the local output with the full augmented image.

The checker gives sharp small guards for all three nonimplications and pins
the literal 171-column, occurrence, and terminal interfaces.  It does not
claim that its small guards are complete GHZ source points.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_protection_survivor_active_coloop_phi_gate.py":
        "031d680f72b99fc864c1d9a2e87a180981f76ed8477cd154ddb81a6c3a45b72a",
    "notes/h3-protection-survivor-active-coloop-phi-gate.md":
        "c1492d41e5cd85f18c57ead28ef13df973b30680fb24b7adac4df79cbccaa501",
    "computations/verify_h3_trapped_carrier_full_q_six_term_extension.py":
        "f194101187d92255a8396b762769df2d3e058f0adc2072ae822da4881f1a4e3d",
    "notes/h3-trapped-carrier-full-q-six-term-extension.md":
        "a5b1a81c834095e69c403d054a38d9f34ebb8b0b3f1d3ce720a27f0b275d04a5",
    "computations/verify_h3_scaled_occurrence_anchor_bridge_alternative.py":
        "ba01612572513e02c60bd5d9a319d8302013e3d73e6a52ae229af8b07dd02507",
    "notes/h3-scaled-occurrence-anchor-bridge-alternative.md":
        "d89d40b3ff69e0d7dc8105b1aa1eea40dceabc84007c1b9759d1a2932ecba572",
    "computations/verify_h3_trapped_carrier_occurrence_graph_hessian_cone_gate.py":
        "ce28ff5d25bf575c280a21c0e35c6dc1ebef54eb039ac94cdc25932a61b95829",
    "notes/h3-trapped-carrier-occurrence-graph-hessian-cone-gate.md":
        "2aa8696ccff97cd2d25de0cdc4b1328ff686193cc45c05e29314a8872e4b0734",
    "computations/verify_h3_affine_pointed_pf_coloop_pivot_gate.py":
        "c5fdf06fb372ec748d2b98398f2968246e2c839dba9282cec29f675a5ca8684e",
    "notes/h3-affine-pointed-pf-coloop-pivot-gate.md":
        "97b07f0814604ed54c266c65ba58e8c6a26fd861755f501852cc2ba3fb251e0e",
    "computations/verify_h3_coloop_alpha_localized_pointed_pf_ga_fitting_gate.py":
        "f0905b3e33a45b51f03dd6716c3f6b29ae21c39fecf50a4ffc32960499a608c7",
    "notes/h3-coloop-alpha-localized-pointed-pf-ga-fitting-gate.md":
        "5d637d94ec2bab2f968dcb31b45b805fecd66da13fb1c927a490a6e20927fe4f",
    "computations/verify_h3_beta_zero_d0_augmented_terminal_saturation_gate.py":
        "d4fabdb5e180ce63e4a0ff018197f4aaf33767bfcf6940291af7783d2f150b27",
    "notes/h3-beta-zero-d0-augmented-terminal-saturation-gate.md":
        "5a58dc9fab666b789a88de71c41c27a8f3e1a004a7d307d31d24b5dbf93f7075",
}
EXPECTED_LEDGER_SHA256 = "9251bc70062d6362cdcaa247013d694747e17b9c0ab205b8e1b7213911c3bf5a"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


def mat_vec(matrix, vector):
    return tuple(dot(row, vector) for row in matrix)


def transpose(matrix):
    return tuple(tuple(row) for row in zip(*matrix, strict=True))


def polynomial_product(left, right, cutoff):
    answer = [Q(0)] * (cutoff + 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            if i + j <= cutoff:
                answer[i + j] += Q(a) * Q(b)
    return tuple(answer)


def rank(rows):
    work = [list(map(Q, row)) for row in rows]
    if not work:
        return 0
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next((row for row in range(pivot_row, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def in_column_span(matrix, target):
    columns = transpose(matrix)
    return rank(columns) == rank(columns + (tuple(map(Q, target)),))


def solve(matrix, rhs):
    matrix = tuple(tuple(map(Q, row)) for row in matrix)
    rhs = tuple(map(Q, rhs))
    variables = len(matrix[0]) if matrix else 0
    work = [list(row) + [rhs[index]] for index, row in enumerate(matrix)]
    pivot_row = 0
    pivots = []
    for column in range(variables):
        pivot = next((row for row in range(pivot_row, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivots.append(column)
        pivot_row += 1
    if any(not any(row[:variables]) and row[variables] for row in work):
        return None
    answer = [Q(0)] * variables
    for row, pivot in enumerate(pivots):
        answer[pivot] = work[row][variables]
    require(mat_vec(matrix, answer) == rhs,
            ("solution reconstruction failed", matrix, rhs, answer))
    return tuple(answer)


def audit_literal_171_fredholm_entry(protection, full_q):
    full_guard = protection.audit_full_171_survivor_and_dark_phi(full_q)
    require(full_guard["literal_domain_columns"] == 171
            and full_guard["guard_row_rank"] == 170
            and full_guard["protection_quotient_dimension"] == 1
            and full_guard["Lambda_in_row_A"]
            and not full_guard["H_in_row_A"]
            and full_guard["H_on_kernel_witness"] == "1",
            full_guard)
    return {
        "domain": "36 endpoint plus 135 decorated-q columns",
        "columns": full_guard["literal_domain_columns"],
        "survivor": "Lambda in row(A), H=P_f nonzero modulo row(A)",
        "fredholm_consequence": (
            "there exists xi in ker(A) with H(xi)=1 after normalization"
        ),
        "what_is_not_in_the_consequence": [
            "an exact source line",
            "a formal source arc beyond first order",
            "an anchor-safe boundary point",
            "an augmented Macaulay terminal",
        ],
    }


def audit_minimum_support_no_deletion_guard():
    # The exact fibre xy=1 has minimum occupied scalar support two: every
    # point on it has x,y nonzero.  At (1,1), xi=(1,-1) changes f=x.
    point = (Q(1), Q(1))
    d_source = (Q(1), Q(1))
    xi = (Q(1), Q(-1))
    H = (Q(1), Q(0))
    require(point[0] * point[1] == 1
            and dot(d_source, xi) == 0 and dot(H, xi) == 1,
            "the minimum-support torus tangent changed")

    # x(t)=1+t, y(t)=(1+t)^-1.  Verify the exact formal inverse through a
    # substantial finite order; the closed geometric-series formula proves
    # it to all orders.
    cutoff = 12
    x_series = (Q(1), Q(1)) + (Q(0),) * (cutoff - 1)
    y_series = tuple(Q(-1) ** degree for degree in range(cutoff + 1))
    product = polynomial_product(x_series, y_series, cutoff)
    require(product == (Q(1),) + (Q(0),) * cutoff,
            "the torus formal arc stopped solving xy=1")
    require(all(value for value in point)
            and all(x and y and x * y == 1 for x, y in (
                (Q(1), Q(1)), (Q(2), Q(1, 2)), (Q(1, 2), Q(2)))),
            "the torus fibre acquired a lower-support point")
    return {
        "exact_source_fibre": "x*y=1",
        "marked_occurrence_shadow": "f=x",
        "base_point": ["1", "1"],
        "minimum_occupied_support": 2,
        "lower_support_point_on_fibre": False,
        "kernel_tangent": ["1", "-1"],
        "df_on_tangent": "1",
        "formal_arc": "x=1+t, y=(1+t)^-1",
        "formal_orders_checked": cutoff,
        "support_along_formal_arc": (
            "both coordinates are units, hence occupied support stays two"
        ),
        "consequence": (
            "minimum support plus H-visible integrable tangent does not imply "
            "support deletion or even a nearby support change"
        ),
    }


def audit_localized_coloop_lift_gate(localized_coloop):
    # The literal localized coloop packet is stronger than a tangent: on
    # either bright U/V chart it carries the algebraic redistribution
    # f -> f+t, g -> g-t.  This proves that no obstruction lives in the
    # aggregate coloop rows themselves.  What is not proved is that the
    # action preserves every one of the complete source equations (or the
    # protected anchor at its boundary specialization).
    u_chart = localized_coloop.localized_ga_audit("U")
    v_chart = localized_coloop.localized_ga_audit("V")
    fitting = localized_coloop.fitting_audit()
    for chart in (u_chart, v_chart):
        require(chart["localized_quotient"] == "k[alpha^{+/-1},d,C,f]"
                and chart["integrated_action"] == "f -> f+t, g -> g-t"
                and chart["P_f_on_infinitesimal_generator"] == 1
                and chart["ideal_status"] ==
                "prime and proper Laurent-chart ideal; no source unit",
                chart)
    require(fitting["transverse_minor_for_row_(r_f,r_g)"] == "r_g-r_f"
            and fitting["relative_Fitt0"] ==
            "(0) before an occurrence-asymmetric physical row"
            and fitting["unit_minor_if_P_f_is_physical"] == -1,
            fitting)
    return {
        "literal_local_packet": "alpha-localized U-bright or V-bright coloop",
        "exact_action": "f -> f+t, g -> g-t",
        "P_f_on_generator": 1,
        "local_source_status": "prime proper Laurent chart; no source unit",
        "transverse_Fitting_minor": "r_g-r_f",
        "what_this_proves": (
            "the selected-occurrence redistribution integrates algebraically "
            "on the localized aggregate coloop packet"
        ),
        "first_unproved_lift": (
            "the same redistribution must preserve every complete physical "
            "source equation; infinitesimally this is the 171-column kernel "
            "condition and at second order its first obstruction is o2"
        ),
        "deletion_clause_after_a_full_lift": (
            "the specialization t=-f deletes the marked occurrence only if "
            "it remains in the physical source and preserves the anchors"
        ),
    }


def audit_first_nonlinear_integrability_gate():
    # Same first-order data, different second-order source germs.  In local
    # coordinate z around the active value 1, the smooth germ has no extra
    # equation; the doubled germ (z-1)^2=0 has zero Jacobian but H=dz and
    # second Hasse coefficient one.  Thus A,H do not determine integrability.
    A = ((Q(0),),)
    xi = (Q(1),)
    H = (Q(1),)
    smooth_o2 = (Q(0),)
    doubled_o2 = (Q(1),)
    require(mat_vec(A, xi) == (Q(0),) and dot(H, xi) == 1
            and in_column_span(A, smooth_o2)
            and not in_column_span(A, doubled_o2),
            "the same-tangent second-order guard changed")

    # For a degree-at-most-three physical source map, restriction to the
    # straight line x+t*xi is exactly the three Hasse coefficients.  Freeze
    # a scalar cubic with vanishing first but nonzero second and third faces.
    # G(t)=t^2+t^3 is not zero despite G_[1]=0.
    line_coefficients = (Q(0), Q(0), Q(1), Q(1))
    require(line_coefficients[1] == 0
            and line_coefficients[2:] == (Q(1), Q(1)),
            "the cubic straight-line Hasse guard changed")
    return {
        "same_first_order_packet": {
            "A": [["0"]], "H": ["1"], "xi": ["1"],
        },
        "smooth_germ": "no equation in z; xi integrates",
        "obstructed_germ": "(z-1)^2=0; F_[2](xi)=1 notin im(A)",
        "first_missing_condition": (
            "[F_[2](xi)]=0 in coker(A), equivalently solve "
            "A*xi_2=-F_[2](xi)"
        ),
        "straight_line_degree_three_criterion": (
            "A*xi=0, F_[2](xi)=0, and F_[3](xi)=0"
        ),
        "straight_line_guard": "G(x+t*xi)=t^2+t^3",
        "first_order_data_decides_integrability": False,
    }


def audit_second_order_fredholm_alternative():
    # A:X=Q^2 -> Y=Q^2.  xi is tangent and H-visible.  One o2 is liftable;
    # the other is detected by the primitive output covector psi.
    A = (
        (Q(1), Q(0)),
        (Q(0), Q(0)),
    )
    xi = (Q(0), Q(1))
    H = (Q(0), Q(1))
    liftable = (Q(1), Q(0))
    obstructed = (Q(0), Q(1))
    psi = (Q(0), Q(1))
    xi2 = solve(A, tuple(-value for value in liftable))
    require(mat_vec(A, xi) == (Q(0), Q(0)) and dot(H, xi) == 1
            and xi2 == (Q(-1), Q(0))
            and in_column_span(A, liftable)
            and not in_column_span(A, obstructed)
            and all(dot(psi, column) == 0 for column in transpose(A))
            and dot(psi, obstructed) == 1,
            "the second-order Fredholm alternative changed")
    return {
        "liftable_arm": {
            "o2": ["1", "0"],
            "xi_2": ["-1", "0"],
            "next_action": "continue to the third and higher arc equations",
            "support_deletion_obtained": False,
        },
        "obstructed_arm": {
            "o2": ["0", "1"],
            "output_covector_psi": ["0", "1"],
            "psi_A": 0,
            "psi_o2": 1,
            "local_output_dual_obtained": True,
            "physical_Macaulay_terminal_obtained": False,
        },
    }


def audit_terminal_extension_gate(beta_terminal):
    pinned = beta_terminal.audit_terminal_extension_counterguard()
    require(pinned["compatible_completion_exists"]
            and pinned["same_local_map_incompatible_completion_exists"]
            and not pinned["bounded_local_separator_is_final_Fredholm"],
            pinned)

    # Repeat the minimal intersection calculation in the present notation.
    # Local Y is the first two coordinates and psi=(0,1).  The good full map
    # has columns e1 and e2+T, so its image meets local Y only in <e1>.
    # Adding T makes e2=(e2+T)-T enter the intersection, blocking extension.
    e1 = (Q(1), Q(0), Q(0))
    e2_plus_t = (Q(0), Q(1), Q(1))
    t = (Q(0), Q(0), Q(1))
    psi_local = (Q(0), Q(1))
    good_extension = (Q(0), Q(1), Q(-1))
    require(dot(good_extension, e1) == 0
            and dot(good_extension, e2_plus_t) == 0,
            "the good Macaulay extension changed")
    required_terminal_coefficients = (
        -dot(psi_local, e2_plus_t[:2]),
        -dot(psi_local, t[:2]),
    )
    bad_solution = solve(((Q(1),), (Q(1),)),
                         required_terminal_coefficients)
    require(required_terminal_coefficients == (Q(-1), Q(0))
            and bad_solution is None,
            "the bad Macaulay extension guard changed")
    return {
        "local_output": "Y_loc=<e1,e2>",
        "local_Fredholm_covector": "psi=e2^*",
        "good_augmented_columns": ["e1", "e2+T"],
        "good_extension": "psi_tilde=e2^*-T^*",
        "bad_extra_column": "T",
        "bad_intersection": "e2=(e2+T)-T lies in Y_loc intersect im(J_aug)",
        "exact_extension_criterion": (
            "psi must kill i(Y_loc) intersect im(J_aug), and the extension "
            "must have the normalized physical terminal value"
        ),
        "same_local_A_and_psi_decide_terminal_promotion": False,
        "failure_of_extension": (
            "a new augmented relative class; it reaches an accepted terminal "
            "only after comparison with the physical six-term/W readout"
        ),
    }


def audit():
    pin_dependencies()
    protection = load(
        "computations/verify_h3_protection_survivor_active_coloop_phi_gate.py",
        "occurrence_integrability_protection",
    )
    full_q = load(
        "computations/verify_h3_trapped_carrier_full_q_six_term_extension.py",
        "occurrence_integrability_full_q",
    )
    beta_terminal = load(
        "computations/verify_h3_beta_zero_d0_augmented_terminal_saturation_gate.py",
        "occurrence_integrability_terminal",
    )
    localized_coloop = load(
        "computations/verify_h3_coloop_alpha_localized_pointed_pf_ga_fitting_gate.py",
        "occurrence_integrability_localized_coloop",
    )
    ledger = {
        "theorem": "h3 pointed-occurrence kernel integrability/terminal gate",
        "pins": PINS,
        "full_171_fredholm_entry":
            audit_literal_171_fredholm_entry(protection, full_q),
        "localized_coloop_lift_gate":
            audit_localized_coloop_lift_gate(localized_coloop),
        "minimum_support_guard": audit_minimum_support_no_deletion_guard(),
        "first_nonlinear_gate": audit_first_nonlinear_integrability_gate(),
        "second_order_alternative": audit_second_order_fredholm_alternative(),
        "terminal_extension": audit_terminal_extension_gate(beta_terminal),
        "source_level_statement": (
            "The alpha-localized coloop packet has the exact redistribution "
            "f->f+t,g->g-t, so the aggregate coloop equations do not obstruct "
            "occurrence isolation.  At an actual h=3 source, H=P_f nonzero "
            "modulo row(A) supplies an H-visible xi in ker(A).  Lifting the "
            "local redistribution through the complete source first meets "
            "o2=[F_[2](xi)] in coker(A).  If o2=0, choose xi_2 and continue; "
            "support deletion requires in addition an anchor-safe exact "
            "same-row line or a proved global arc-to-boundary theorem.  If "
            "o2!=0, a local physical output covector psi detects it, but psi "
            "is a Macaulay terminal only after it extends across the complete "
            "augmented source map with normalized six-term/W readout"
        ),
        "shortest_positive_clauses": [
            "integrability: solve A*xi_2=-F_[2](xi) (then all later arc equations)",
            "deletion: type an exact kernel line on occupied same-row scalar cells and preserve anchors",
            "terminal: extend psi through the exhaustive augmented map, equivalently kill the local/full-image intersection",
        ],
        "verdict": (
            "Neither branch is automatic from the 171-column Jacobian and "
            "minimum support.  The first genuinely new source datum is the "
            "second Hasse/Spencer obstruction.  Its lift arm does not yet "
            "delete support; its dual arm is not yet the final physical "
            "Macaulay terminal without the displayed extension law"
        ),
        "scope": (
            "exact first- and second-order algebra plus sharp source/terminal "
            "guards.  The small germs are logical counterguards, not complete "
            "GHZ source points, and no all-order arc or terminal comparison "
            "is constructed"
        ),
    }
    digest = sha256(json.dumps(ledger, sort_keys=True,
                               separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("h3 P_f kernel: FIRST ORDER DOES NOT DELETE SUPPORT")
    print("first nonlinear condition: [F_[2](xi)] in coker(A)")
    print("liftable o2: continue arc; no deletion yet")
    print("nonliftable o2: local output dual; terminal extension still required")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
