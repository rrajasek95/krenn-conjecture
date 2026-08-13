#!/usr/bin/env python3
"""Relate the full-q protection survivor to the active-fan coloop gate.

The h=3 full-q domain has 171 literal columns.  A marked nonzero occurrence
has, after logarithmic localization, anchor differential

    H = dlog(p1[0,1]) + dlog(q23[0,0]) + dlog(q45[0,0]).

This checker embeds the sharp protection-only quotient in that full labelled
domain.  Its guard row space models a codimension-one evaluated physical row
space: basis-normalized representatives of Lambda and the fan-q readout lie
in it, while H does not.  A rank-one projection Phi fixes every guard row
and both readouts but kills the H quotient.  Thus even a chain
square and exact q transport do not remove the survivor; the missing datum is
the single anchor quotient identity

    H - h_fan Phi in row(A).

Separately, the pinned active-fan guard contains a literal nonzero
offdiagonal cell and a pure-colour coloop.  Such a packet is outside the
axis-pure coordinate locus by definition.  Row-space darkness cannot set
that base-point cell to zero, so global axis-pure emptiness does not close
this arm without the displayed fan-grade comparison law.

The 171-column packet is a sharp compatibility/counterguard for the stated
linear and support data, not an asserted complete GHZ source point.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_trapped_carrier_full_q_six_term_extension.py":
        "f194101187d92255a8396b762769df2d3e058f0adc2072ae822da4881f1a4e3d",
    "notes/h3-trapped-carrier-full-q-six-term-extension.md":
        "a5b1a81c834095e69c403d054a38d9f34ebb8b0b3f1d3ce720a27f0b275d04a5",
    "computations/verify_h3_active_fan_coloop_or_four_good.py":
        "93030f2994e2e6a2052a09a5fefd179c99e0b8fb55cd0c77bee2cb9f8dbc6bb4",
    "notes/h3-active-fan-coloop-or-four-good.md":
        "9be8996264fa2070a8f5d7f725f3fcb154b6ee2df2b3e5d3ccd4a6412ec5b03a",
    "computations/verify_h3_fan_coloop_packet_q_comparison_defect.py":
        "86db5c89196a183c5ddc2b1c2198029fa45ea1cdff1f7d239a74870cd4957e94",
    "notes/h3-fan-coloop-packet-q-comparison-defect.md":
        "a66eff0a65488b3c4f824a2558cc093d57a0ba8f9ec6c2ffc3af57b630a9ea6d",
    "computations/verify_h3_interface_ii_anchor_faithful_central_comparison.py":
        "fe77afbafa23656d8afd6aaa0218e6134776205ffe4525658273de80f9f004a6",
    "notes/h3-interface-ii-anchor-faithful-central-comparison.md":
        "16c29c5378e68426aa9c22af96a4b2f251511baed93ca2f6641dfee4ec86aa73",
    "computations/verify_h3_axis_pure_global_min_support_census.py":
        "4b88379419c94aa21f8a457b89821fb107d4b841c17ffa38ec10516e48426156",
    "notes/h3-axis-pure-global-min-support-census.md":
        "8889c50a1bbeb6049f8c06b61f451e84cd60a1185fd3ad8407390ff5a3a9098d",
    "computations/verify_h3_active_fan_coloop_gate_ii_assembly_boundary.py":
        "22e1e7a6a933b1ba71bbd95bb605b1351e823506e495682cccff312cd3df3b15",
    "notes/h3-active-fan-coloop-gate-ii-assembly-boundary.md":
        "bacb7b4b138882c0cc07f13767f2e4ead86aa630c55cf1a946943141b7cee7a7",
    "computations/verify_h3_affine_pointed_pf_coloop_pivot_gate.py":
        "c5fdf06fb372ec748d2b98398f2968246e2c839dba9282cec29f675a5ca8684e",
    "notes/h3-affine-pointed-pf-coloop-pivot-gate.md":
        "97b07f0814604ed54c266c65ba58e8c6a26fd861755f501852cc2ba3fb251e0e",
}
EXPECTED_LEDGER_SHA256 = "e3a6281dec9746218e447d5e9b4263273fa6aa59245fa7ea1bbf5643e9407412"


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


def add(left, right):
    return tuple(Q(a) + Q(b) for a, b in zip(left, right, strict=True))


def subtract(left, right):
    return tuple(Q(a) - Q(b) for a, b in zip(left, right, strict=True))


def scale(value, vector):
    return tuple(Q(value) * Q(entry) for entry in vector)


def unit(width: int, index: int):
    return tuple(Q(position == index) for position in range(width))


def rref(rows, width: int):
    work = [list(map(Q, row)) for row in rows]
    require(all(len(row) == width for row in work), "ragged matrix")
    pivots = []
    pivot_row = 0
    for column in range(width):
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
        if pivot_row == len(work):
            break
    return tuple(tuple(row) for row in work), tuple(pivots)


def rank(rows, width: int):
    return len(rref(rows, width)[1])


def in_row_span(rows, target):
    width = len(target)
    return rank(rows, width) == rank(tuple(rows) + (tuple(target),), width)


def literal_columns(full_q):
    endpoint = tuple(("p", i, site, colour)
                     for i in range(2) for site in range(6)
                     for colour in range(3))
    q_columns = tuple(("q",) + tuple(label) for label in full_q.Q_COLUMNS)
    columns = endpoint + q_columns
    require(len(endpoint) == 36 and len(q_columns) == 135
            and len(columns) == 171 and len(set(columns)) == 171,
            "the literal full-q domain changed")
    return columns


def audit_full_171_survivor_and_dark_phi(full_q):
    columns = literal_columns(full_q)
    index = {label: position for position, label in enumerate(columns)}
    anchor_labels = (
        ("p", 0, 0, 1),
        ("q", 2, 3, 0, 0),
        ("q", 4, 5, 0, 0),
    )
    anchor_indices = tuple(index[label] for label in anchor_labels)
    fan_offdiagonal = ("q", 0, 1, 0, 1)
    pure_coloop_cell = ("q", 0, 1, 0, 0)
    fan_index = index[fan_offdiagonal]
    coloop_index = index[pure_coloop_cell]
    require(len(set(anchor_indices + (fan_index, coloop_index))) == 5,
            "the anchor and fan labels collided")

    # On the localization where the marked occurrence is nonzero, diagonal
    # rescaling to logarithmic tangent coordinates turns df/f into the sum
    # of the three displayed coordinate covectors.
    H = tuple(sum(position == anchor for anchor in anchor_indices)
              for position in range(len(columns)))
    xi = tuple(Q(position in anchor_indices) for position in range(len(columns)))

    # A maximally constrained sharp guard: all non-anchor selectors and the
    # two centered differences between the three anchor coordinates.  Its
    # row space is exactly xi^perp and has one-dimensional quotient [H].
    rows = [unit(len(columns), position) for position in range(len(columns))
            if position not in anchor_indices]
    rows.append(subtract(unit(len(columns), anchor_indices[0]),
                         unit(len(columns), anchor_indices[1])))
    rows.append(subtract(unit(len(columns), anchor_indices[1]),
                         unit(len(columns), anchor_indices[2])))
    A = tuple(rows)
    # These are basis-normalized representatives of two covectors already
    # assumed to lie in row(A).  They are deliberately placed on literal
    # labelled complement slots; this does not identify the formula q=M-a
    # with a source-coordinate selector.
    Lambda = unit(len(columns), fan_index)
    q_fan = unit(len(columns), coloop_index)
    require(len(A) == 170 and rank(A, len(columns)) == 170
            and all(dot(row, xi) == 0 for row in A)
            and dot(H, xi) == 3,
            "the full-width protection quotient changed")
    require(in_row_span(A, Lambda) and in_row_span(A, q_fan)
            and not in_row_span(A, H),
            "the full-width survivor memberships changed")

    # Phi_dark is the projection v |-> v-xi*H(v)/3.  Since every A-row,
    # Lambda, and q_fan kills xi, pullback by Phi_dark fixes them.  H itself
    # pulls back to zero.  This gives A Phi=A and exact q/Lambda transport
    # while failing only the anchor quotient law.
    def phi_dark(vector):
        return subtract(tuple(map(Q, vector)), scale(dot(H, vector) / 3, xi))

    require(phi_dark(xi) == (Q(0),) * len(columns),
            "the dark comparison stopped killing the anchor tangent")
    probes = A + (Lambda, q_fan)
    # Pullback of a covector r is r Phi.  For this self-adjoint projection,
    # it is given by the same formula because H=xi in the normalized chart.
    require(all(phi_dark(row) == row for row in probes)
            and phi_dark(H) == (Q(0),) * len(columns),
            "the dark comparison stopped fixing the physical packet")
    anchor_defect = subtract(H, phi_dark(H))
    require(not in_row_span(A, anchor_defect),
            "the dark comparison unexpectedly became anchor-faithful")

    # Identity is the minimal positive comparison on this quotient.
    require(in_row_span(A, subtract(H, H)),
            "the bright identity comparison lost anchor faithfulness")
    return {
        "literal_domain_columns": len(columns),
        "endpoint_columns": 36,
        "q_columns": 135,
        "localized_anchor_labels": [repr(label) for label in anchor_labels],
        "literal_offdiagonal_fan_label": repr(fan_offdiagonal),
        "literal_pure_coloop_label": repr(pure_coloop_cell),
        "guard_row_rank": rank(A, len(columns)),
        "protection_quotient_dimension": len(columns) - rank(A, len(columns)),
        "Lambda_in_row_A": in_row_span(A, Lambda),
        "q_fan_in_row_A": in_row_span(A, q_fan),
        "H_in_row_A": in_row_span(A, H),
        "normalized_kernel_witness_support": [repr(label)
                                                for label in anchor_labels],
        "H_on_kernel_witness": str(dot(H, scale(Q(1, 3), xi))),
        "dark_Phi": {
            "formula": "Phi=I-xi*H/3",
            "A_Phi_equals_A": True,
            "Lambda_transport": True,
            "q_transport": True,
            "Phi_xi": 0,
            "anchor_quotient_identity": False,
        },
        "smallest_repair": (
            "one scalar quotient law [H]=Phi^*[h_fan] in "
            "X^*/row(A), equivalently h_fan(Phi xi)=H(xi)=1"
        ),
    }


def audit_literal_fan_is_not_axis_pure(active_fan, axis_global):
    guard = active_fan.audit_sharp_adjacent_coloop_guard()
    require(guard["pure_coloops"] == {
        "colour_0": [0, 1], "colour_1": [0, 2]
    } and guard["private_site_identity"] == "q_e + Delta_ef*C_f = 1-1 = 0"
            and guard["distinct_centre_heads"],
            "the literal active-fan coloop guard changed")
    base = axis_global.load_base()
    formula = axis_global.build_formula(base)
    offdiagonal = ("q", 0, 1, 0, 1)
    require(len(formula["cell_vars"]) == 69
            and len(formula["terms"]) == 3645
            and all(len(coordinate) == 3 for coordinate in base.ALL_COORDINATES)
            and offdiagonal not in base.ALL_COORDINATES,
            "the axis-pure coordinate locus changed")
    return {
        "active_fan_edges": guard["active_adjacent_pairs"],
        "literal_pure_coloops": guard["pure_coloops"],
        "nonzero_offdiagonal_cell": "q_01^[0,1]=1",
        "axis_pure_q_coordinates": "only q_uv^[c,c]",
        "offdiagonal_cell_in_axis_pure_coordinate_universe": False,
        "axis_pure_census_models": 6,
        "axis_pure_coefficient_lifts": 0,
        "consequence": (
            "an actual packet retaining the nonzero offdiagonal fan cell is "
            "already outside the axis-pure locus.  Darkness of a tangent "
            "or comparison readout does not set that base-point value to zero"
        ),
        "scope": guard["scope"],
    }


def audit_existing_q_law_is_independent(
        q_comparison, interface_ii, gate_ii, pointed):
    q_independence = q_comparison.audit_anchor_independence()
    anchor_guard = interface_ii.audit_chain_square_without_anchor_law()
    assembly = gate_ii.audit_branch_assembly()
    pointed_gate = pointed.pointed_gate_audit()
    require(q_independence["q_comparison_defect"] == [0, 0, 0]
            and q_independence["anchor_defect_on_circuit"] == "1"
            and anchor_guard["chain_square"]
            and not anchor_guard["anchor_quotient_identity"]
            and assembly["only_nonterminal_after_saturation"]
            == "single missing fan-grade physical Phi/q packet"
            and not pointed_gate["U_bright_guard"]
            ["selected_P_f_in_row_span"]
            and not pointed_gate["V_bright_guard"]
            ["selected_P_f_in_row_span"],
            (q_independence, anchor_guard, assembly, pointed_gate))
    return {
        "physical_q_transport_can_hold": True,
        "chain_square_can_hold": True,
        "anchor_quotient_can_still_fail": True,
        "affine_identification": "du=0, so P_f=df-du=df=H",
        "coloop_pivot_constructs_P_f": False,
        "first_pivot_obstruction": (
            "two-occurrence internal redistribution in either U- or V-bright "
            "aggregate is invisible to the complete coloop pivot and visible "
            "to P_f"
        ),
        "fan_gate_before_this_audit": (
            "complete fan-grade Phi/q packet, with anchor comparison not "
            "deduced from q transport"
        ),
        "sharpened_single_datum_on_protection_survivor": (
            "after the fan chain square and q row have been placed, require "
            "H-h_fan*Phi in row(A); on the one-dimensional survivor this is "
            "one nonzero/equality scalar, equivalently the physical pointed "
            "occurrence conormal P_f on the affine chart"
        ),
    }


def audit():
    pin_dependencies()
    full_q = load(
        "computations/verify_h3_trapped_carrier_full_q_six_term_extension.py",
        "protection_active_full_q",
    )
    active_fan = load(
        "computations/verify_h3_active_fan_coloop_or_four_good.py",
        "protection_active_fan",
    )
    q_comparison = load(
        "computations/verify_h3_fan_coloop_packet_q_comparison_defect.py",
        "protection_active_q_comparison",
    )
    interface_ii = load(
        "computations/verify_h3_interface_ii_anchor_faithful_central_comparison.py",
        "protection_active_interface_ii",
    )
    axis_global = load(
        "computations/verify_h3_axis_pure_global_min_support_census.py",
        "protection_active_axis_global",
    )
    gate_ii = load(
        "computations/verify_h3_active_fan_coloop_gate_ii_assembly_boundary.py",
        "protection_active_gate_ii",
    )
    pointed = load(
        "computations/verify_h3_affine_pointed_pf_coloop_pivot_gate.py",
        "protection_active_pointed",
    )
    ledger = {
        "theorem": "h3 protection survivor / active-coloop Phi gate",
        "pins": PINS,
        "full_171_counterguard":
            audit_full_171_survivor_and_dark_phi(full_q),
        "literal_fan_versus_axis_pure":
            audit_literal_fan_is_not_axis_pure(active_fan, axis_global),
        "q_and_anchor_independence":
            audit_existing_q_law_is_independent(
                q_comparison, interface_ii, gate_ii, pointed),
        "exact_verdict": (
            "The current physical and support theorems do not force the "
            "protection-only survivor into the axis-pure branch.  A literal "
            "active fan has a nonzero offdiagonal cell, hence is unpurified.  "
            "The 171-column sharp guard admits Lambda in row(A), physical q "
            "transport and a commuting fan comparison while H remains "
            "nonzero modulo row(A).  On the sole one-dimensional survivor, "
            "the first missing fan-grade datum is exactly the anchor quotient "
            "law H-h_fan Phi in row(A), equivalently the selected pointed "
            "occurrence conormal P_f because du=0 on the physical affine chart"
        ),
        "positive_use": (
            "Once a physical fan-grade Phi supplies both q transport and the "
            "anchor quotient law, H notin row(A) becomes an h_fan-visible "
            "protected kernel class and the already pinned Gate-II/central "
            "generator-separator alternatives consume it"
        ),
        "scope": (
            "exact 171-label linear/support compatibility guard and quotient "
            "reduction.  The active-fan support packet is a pinned local "
            "source-grade guard, not a complete GHZ source point; this file "
            "therefore proves that the current hypotheses do not imply a "
            "contradiction, not that a conjectural counterexample exists"
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
    print("h3 protection survivor + literal active coloop: NOT CONTRADICTORY")
    print("axis-pure fallback: unavailable while offdiagonal fan cell is live")
    print("chain square + Lambda/q transport: survivor can remain")
    print("missing datum: [H]=Phi^*[h_fan] modulo row(A)")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
