#!/usr/bin/env python3
"""Relative-incidence closure of the bidirectional five-lock residual.

The two target-augmented private-site identities attached to one nonzero
off-diagonal cell have the same inhomogeneous term.  After the already
certified kernel and crossed-wedge exits, an exact common-tail pairing of
all remaining unary/11/12/21/22 occurrences is therefore a *relative*
signless-incidence component with two marked ends, one from each transposed
fan.  Equal literal tail weights and source-word parity make the marked
path even.  Its alternating row sum is E_plus-E_minus.

Together with the existing rootless bar B=(0,0,-1,1), this is precisely the
missing attachment A=(1,-1,1,-1).  The checker also freezes the sharp
boundary: one unequal tail weight on an otherwise complete all-five-row
path leaves the internal lock map injective, has no crossed shared port,
and separates E_plus-E_minus.  This is an exact source-labelled lock-module
guard, not a physical full GHZ source.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_bidirectional_private_site_fan_rank_boundary.py":
        "c4e175ca053cd98e788cca1a38a1851e708e7e47a9ea5745ef4ac6e303ddfd40",
    "computations/verify_uniform_hall_five_lock_signless_incidence_boundary.py":
        "34bf365f2a9e154a10feab8fa7cc83b0aba519f4124b8e28ed959f280a51e721",
    "computations/verify_uniform_five_lock_wedge_or_switch.py":
        "c2541a60db1f8e7a661bc698d2bd1f1a1f396a0f0bfde389ea89bea17fac175e",
    "computations/verify_h3_shared_same_word_endpoint_companion_attachment_gate.py":
        "ef6f336c3582c66ca65250a3d812deaed5aa3a6d998ce1e428e0bc03fa2fab37",
    "computations/verify_reciprocal_response_hasse_bianchi.py":
        "d5bb78f9a0ca2cfab30932ccfcaeca8c6de9d3bff5351983045e66fee4d1d432",
}
EXPECTED_LEDGER_SHA256 = (
    "83ad53294febb9004b81d9799d60d2c22b92afd6377dc1de76fc6ea8a9a38e68"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(relative, name):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            f"cannot load dependency: {relative}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def rank(rows):
    matrix = [[Q(entry) for entry in row] for row in rows]
    if not matrix:
        return 0
    columns = len(matrix[0])
    require(all(len(row) == columns for row in matrix), "ragged matrix")
    pivot_row = 0
    for column in range(columns):
        pivot = next((row for row in range(pivot_row, len(matrix))
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [left - value * right for left, right in
                           zip(matrix[row], matrix[pivot_row], strict=True)]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def in_row_span(rows, target):
    return rank(rows) == rank(list(rows) + [list(target)])


def row_combination(coefficients, rows):
    return tuple(sum(Q(coefficient) * Q(rows[index][column])
                     for index, coefficient in enumerate(coefficients))
                 for column in range(len(rows[0])))


def path_rows(edge_weights):
    """Rows a_i*z_i+b_i*z_(i+1) on an ordered relative path."""
    rows = []
    for index, (left_weight, right_weight) in enumerate(edge_weights):
        row = [Q(0)] * (len(edge_weights) + 1)
        row[index] = Q(left_weight)
        row[index + 1] = Q(right_weight)
        rows.append(tuple(row))
    return tuple(rows)


def path_kernel(edge_weights):
    """Primitive-up-to-scale dual propagated from lambda_0=1."""
    values = [Q(1)]
    for left_weight, right_weight in edge_weights:
        require(right_weight, "a path tail weight vanished")
        values.append(-Q(left_weight) * values[-1] / Q(right_weight))
    rows = path_rows(edge_weights)
    require(all(sum(entry * value for entry, value in
                    zip(row, values, strict=True)) == 0 for row in rows),
            "the weighted path dual stopped killing its rows")
    return tuple(values)


def audit_bidirectional_source_boundary(bidirectional):
    typing = bidirectional.audit_bidirectional_typing()
    private_site = bidirectional.load(
        "computations/verify_uniform_target_augmented_private_site_active_minor.py",
        "relative_private_site",
    )
    private_core = private_site.load(
        "computations/verify_hafnian_private_site_matching_bijection_lemma.py",
        "relative_private_core",
    )
    identities = bidirectional.audit_source_identities(private_site, private_core)
    require(typing["type_count"] == 6,
            "the bidirectional off-diagonal type count changed")
    require(identities["first_fan"]["exact_source_consequence"]
            == identities["transposed_fan"]["exact_source_consequence"]
            == "sum_s Delta_us*C_s=-q_u",
            "the two fan identities lost their common inhomogeneous cell")
    return {
        "offdiagonal_types": typing["type_count"],
        "first_fan": identities["first_fan"]["exact_source_consequence"],
        "transposed_fan":
            identities["transposed_fan"]["exact_source_consequence"],
        "relative_boundary": (
            "subtracting the two identities cancels the same physical "
            "off-diagonal cell; after literal full-row pairing the only "
            "marked boundary is E_plus-E_minus"
        ),
    }


def audit_equal_tail_relative_paths():
    records = []
    for length in range(2, 14, 2):
        weights = tuple((Q(1), Q(1)) for _edge in range(length))
        rows = path_rows(weights)
        coefficients = tuple(Q(1 if index % 2 == 0 else -1)
                             for index in range(length))
        difference = tuple(Q(int(index == 0) - int(index == length))
                           for index in range(length + 1))
        actual = row_combination(coefficients, rows)
        require(actual == difference,
                f"the even relative path boundary changed at length {length}")
        kernel = path_kernel(weights)
        require(kernel[0] == kernel[-1] == 1
                and rank(rows) == length
                and in_row_span(rows, difference),
                f"the equal-tail endpoint holonomy changed at length {length}")

        # Marked endpoint columns are not switch directions.  Restricting to
        # the internal columns gives an injective lock map, so the path is
        # genuinely the relative/A alternative rather than a hidden
        # same-star dependence.
        internal_rows = [row[1:-1] for row in rows]
        require(rank(internal_rows) == length - 1,
                "the relative path acquired an internal lock kernel")
        records.append({
            "path_length": length,
            "row_rank": rank(rows),
            "internal_lock_rank": rank(internal_rows),
            "internal_lock_columns": length - 1,
            "endpoint_dual_values": [str(kernel[0]), str(kernel[-1])],
            "alternating_boundary": "E_plus-E_minus",
        })

    # Odd equal-tail paths produce only the signless endpoint sum.  The
    # physical source-word grading in the intended component must therefore
    # put the two transposed fan marks in the same bipartition class.
    odd_records = []
    for length in range(1, 12, 2):
        rows = path_rows(tuple((Q(1), Q(1)) for _edge in range(length)))
        endpoint_sum = tuple(Q(int(index in (0, length)))
                             for index in range(length + 1))
        difference = tuple(Q(int(index == 0) - int(index == length))
                           for index in range(length + 1))
        require(in_row_span(rows, endpoint_sum)
                and not in_row_span(rows, difference),
                f"the odd-path parity guard changed at length {length}")
        odd_records.append({
            "path_length": length,
            "row_span_endpoint": "E_plus+E_minus",
            "difference_in_row_span": False,
        })
    return {
        "even_common_tail_paths": records,
        "odd_parity_guards": odd_records,
        "uniform_even_path_identity": (
            "sum_i (-1)^i(z_i+z_(i+1))=E_plus-E_minus"
        ),
    }


def audit_all_five_row_holonomy_guard():
    # Use every row type.  The crossed rows are assigned distinct physical
    # ports, so the pinned complementary-wedge hypothesis is absent.
    labels = ("unary", "11", "12", "unary", "21", "22")
    crossed_ports = {"12": "port-r", "21": "port-s"}
    equal_weights = tuple((Q(1), Q(1)) for _label in labels)
    unequal_weights = list(equal_weights)
    unequal_weights[3] = (Q(1), Q(2))
    unequal_weights = tuple(unequal_weights)

    equal_rows = path_rows(equal_weights)
    unequal_rows = path_rows(unequal_weights)
    endpoint_difference = tuple(
        Q(int(index == 0) - int(index == len(labels)))
        for index in range(len(labels) + 1)
    )
    equal_dual = path_kernel(equal_weights)
    unequal_dual = path_kernel(unequal_weights)
    require(equal_dual[0] == equal_dual[-1] == 1
            and in_row_span(equal_rows, endpoint_difference),
            "equal provenance stopped producing the endpoint difference")
    require(unequal_dual[0] == 1 and unequal_dual[-1] == Q(1, 2)
            and not in_row_span(unequal_rows, endpoint_difference),
            "the unequal-tail endpoint separator changed")

    # Both relative systems remain injective on the five internal lock
    # columns.  Thus the guard has neither an internal same-star dependence
    # nor a shared-port crossed mate.
    equal_internal_rank = rank([row[1:-1] for row in equal_rows])
    unequal_internal_rank = rank([row[1:-1] for row in unequal_rows])
    require(equal_internal_rank == unequal_internal_rank == 5,
            "the all-five path acquired an internal switch kernel")
    require(len(set(crossed_ports.values())) == 2,
            "the crossed guard acquired a common physical port")
    return {
        "row_labels": list(labels),
        "crossed_ports": crossed_ports,
        "internal_lock_columns": 5,
        "equal_tail_internal_rank": equal_internal_rank,
        "unequal_tail_internal_rank": unequal_internal_rank,
        "equal_tail_endpoint_dual": [str(equal_dual[0]),
                                     str(equal_dual[-1])],
        "unequal_tail_endpoint_dual": [str(unequal_dual[0]),
                                       str(unequal_dual[-1])],
        "equal_tail_spans_D": True,
        "unequal_tail_spans_D": False,
        "same_star_dependence_in_guard": False,
        "opposite_crossed_shared_port_in_guard": False,
        "sharp_obstruction": (
            "one literal tail coefficient differs, so the propagated "
            "Fredholm dual has lambda(E_plus)!=lambda(E_minus)"
        ),
        "scope": (
            "exact rational full-five source-labelled lock module; not a "
            "physical common-q GHZ source"
        ),
    }


def audit_attachment_identification(attachment):
    gate = attachment.sufficient_attachment_theorem()
    S = tuple(gate["existing_signless_endpoint_row_S"])
    B = tuple(gate["existing_rootless_bar_B"])
    A = tuple(gate["required_same_word_attachment_A"])
    D = tuple(gate["derived_endpoint_difference_D=A+B"])
    require(S == (1, 1, 0, 0)
            and B == (0, 0, -1, 1)
            and A == (1, -1, 1, -1)
            and D == (1, -1, 0, 0),
            "the four-coordinate attachment gate changed")
    require(tuple(D[index] - B[index] for index in range(4)) == A,
            "relative endpoint difference minus the bar stopped being A")
    require(rank([S, B]) == 2 and rank([S, B, D]) == 3,
            "the attachment quotient ranks changed")
    return {
        "coordinate_order": gate["coordinate_order"],
        "signless_endpoint_row_S": list(S),
        "rootless_bar_B": list(B),
        "relative_fan_boundary_D": list(D),
        "forced_attachment_A=D-B": list(A),
        "endpoint_lattice_determinant":
            gate["endpoint_lattice_determinant"],
        "characteristic_zero_consequence": (
            "S and D split E_plus,E_minus after inverting 2"
        ),
    }


def audit_hasse_bianchi_shadow(hasse, attachment):
    # Take the reciprocal off-diagonal direct cell d=-E_10 and compare it
    # with each diagonal response direction.  Equation (3) has a nonzero
    # pure target on the right for every diagonal colour.
    direct = {(1, 0): Q(-1)}
    targets = {
        colour: hasse.bianchi_target(direct, (1, 0), (colour, colour))
        for colour in range(3)
    }
    require(targets == {
        0: (Q(-1), Q(0), Q(0)),
        1: (Q(0), Q(-1), Q(0)),
        2: (Q(0), Q(0), Q(-1)),
    }, "the reciprocal Hasse--Bianchi curvature table changed")

    gate = attachment.sufficient_attachment_theorem()
    S = tuple(gate["existing_signless_endpoint_row_S"])
    B = tuple(gate["existing_rootless_bar_B"])
    D = tuple(gate["derived_endpoint_difference_D=A+B"])
    require(D == (1, -1, 0, 0)
            and rank([S, B]) == 2
            and rank([S, B, D]) == 3,
            "the Hasse shadow stopped detecting the endpoint difference")

    # If both residual insertions in Eq. (3) lifted to tangent variations of
    # the full source fibre, both derivative defects on the left would be
    # zero.  The displayed nonzero target makes that impossible.  The
    # bidirectional private-site identities land determinant/cofactor values
    # in degree zero; they do not construct either corrected tangent lift.
    require(all(any(value) for value in targets.values()),
            "a diagonal Hasse curvature target vanished")
    return {
        "formal_left_shadow": "E_plus-E_minus",
        "four_coordinate_shadow_D": list(D),
        "opposite_diagonal_targets": {
            str(colour): [str(entry) for entry in value]
            for colour, value in targets.items()
        },
        "shadow_rank_gain": rank([S, B, D]) - rank([S, B]),
        "both_Hasse_directions_tangent": False,
        "bidirectional_fan_landing": (
            "nonzero degree-zero determinant/cofactor products only"
        ),
        "missing_lift": (
            "a corrected source variation realizing q-dot=r_cc or r_10 "
            "while killing the complete unary and four response defects"
        ),
        "verdict": (
            "Eq.(3) has exactly the desired endpoint-difference curvature "
            "shadow, but it is not a physical boundary row.  The nonzero "
            "pure target proves that at least one insertion is non-tangent; "
            "the bidirectional fans do not repair that tangent lift"
        ),
    }


def main():
    pin_dependencies()
    bidirectional = load(
        "computations/verify_uniform_bidirectional_private_site_fan_rank_boundary.py",
        "relative_bidirectional_fans",
    )
    signless = load(
        "computations/verify_uniform_hall_five_lock_signless_incidence_boundary.py",
        "relative_signless_hall",
    )
    attachment = load(
        "computations/verify_h3_shared_same_word_endpoint_companion_attachment_gate.py",
        "relative_attachment_gate",
    )
    hasse = load(
        "computations/verify_reciprocal_response_hasse_bianchi.py",
        "relative_hasse_bianchi",
    )
    cycle_certificates = signless.audit_cycle_certificates()
    require(all(record["certificate"]["type"] in
                {"bipartite kernel", "localized 2z unit"}
                for record in cycle_certificates),
            "the closed Hall component dichotomy changed")

    ledger = {
        "pins": PINS,
        "bidirectional_source_boundary":
            audit_bidirectional_source_boundary(bidirectional),
        "closed_component_replay": cycle_certificates,
        "relative_common_tail_paths": audit_equal_tail_relative_paths(),
        "all_five_row_holonomy_guard": audit_all_five_row_holonomy_guard(),
        "shared_attachment": audit_attachment_identification(attachment),
        "Hasse_Bianchi_degree_zero_shadow":
            audit_hasse_bianchi_shadow(hasse, attachment),
        "conditional_closure_theorem": (
            "after the five-lock kernel and complementary crossed-wedge "
            "exits, suppose every remaining occurrence in the component of "
            "the two transposed fan marks is accounted for by an equal-"
            "weight literal common-tail unary/11/12/21/22 row and the two "
            "marks have the same source-word parity.  Closed components "
            "give the pinned even-kernel/odd-unit alternatives; the marked "
            "component is an even relative path whose alternating row sum "
            "is D=E_plus-E_minus.  With the existing rootless bar, D-B is "
            "exactly A=(1,-1,1,-1)"
        ),
        "sharp_remaining_obligation": (
            "prove literal equal-tail/complete-incidence provenance in the "
            "marked component, or route a failed row.  A single unequal "
            "tail has a one-dimensional endpoint-holonomy separator and "
            "is not removed by Hall incidence or by the five aggregate "
            "row labels alone.  Hasse--Bianchi Eq.(3) detects D as "
            "curvature but still needs a corrected tangent lift before D "
            "belongs to the physical source-row image"
        ),
        "scope": (
            "uniform relative graph/module theorem plus exact rational "
            "all-five guard.  It identifies the unique A boundary under "
            "common provenance; it does not assert that every physical "
            "full source has that provenance and does not construct a GHZ "
            "source or counterexample"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"relative five-lock homotopy ledger changed: {digest}")
    print("uniform bidirectional five-lock relative homotopy: BOUNDARY")
    print("equal common-tail relative component -> D=E_plus-E_minus")
    print("D-rootless_bar -> A=(1,-1,1,-1)")
    print("Hasse--Bianchi Eq.(3): correct D shadow, tangent lift still open")
    print("closed components -> same-star kernel or localized odd unit")
    print("sharp residual -> unequal/unmatched tail holonomy separator")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
