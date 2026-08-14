#!/usr/bin/env python3
"""Audit the uniform-response route to the Gate-II relative carrier orbit.

The h=3 endpoint response has ninety occurrence coordinates.  Its universal
centered deformation gives the presentation-safe relative graph

    d beta_f = c_f-u_f,             c_f=90 e_f-1_90.

The residual matching numerator M=A+I commutes with centering and satisfies

    M c_f = 3 c_01,                 c_01=30 b_01-1_90.

Consequently it gives a *relative* selected-fibre graph, not an absolute
boundary for b_01.  Endpoint transport gives the B and C chart fibres.  It
does not give the direct Dq_01 chart A.  In the local three-chart module the
endpoint fibres B,C have rank two, while either R_01=A+B+C or
L_01=2A-B-C raises the rank to three.  The missing augmentation-one direct
chart is exactly U_C4[D,Q01;2345] followed by its physical Dq_01 cap.

At principal-parts order the first obstruction has two honest levels.  With
no extra physical comparison, the matching construction already stops at
the selected six-term db_01 face.  If one grants that face, its endpoint
mate, and the lower symmetric-C4 tail, the remaining combined three-cap
face is precisely the eighteen direction-factor derivatives of dL_01.
Only after that face is placed does the committed labelled descent reach the
word-0102 carrier and its dq/Q/labelled-ores ladder.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_universal_response_deformation_e14_orbit_ks_gate.py":
        "39713f3683dd3d2376e5a911987ee3670ec291cf850072d6b4932e7a93745fc7",
    "computations/verify_h3_centered_occurrence_endpoint_matching_maschke_pointed_gate.py":
        "1994697181c6034267d98a26a28ab4c69c3fcb979b657c8d7d06fc81b86650ed",
    "computations/verify_h3_e14_selected_fibre_graph_keq_koszul_gate.py":
        "9d57cbcfaeebb8d7f67d6efea87a124b4a46ad1dc054d5fc0954ab0c2338b157",
    "computations/verify_h3_generic_symmetric_c4_placement_terminal_gate.py":
        "ecb8725715747c3270fb069545309283d1890fbac6e66dfb6ed2f53b609e0030",
    "computations/verify_h3_h2_l01_three_cap_first_pp_curvature_gate.py":
        "59babf6e706973f2eaa8a8fdd7cdb624ddf88560c08243c5fcd05c3a5425a5d7",
    "computations/verify_h3_gate_ii_psidelta_same_grade_extension_chain.py":
        "d5628f66ffbf94e2de37318ab136adda96af5e114e2bea8dce22542ec9f30cb1",
    "computations/verify_h3_gate_ii_three_cap_relative_tate_carrier_obstruction.py":
        "0be2bde12d3d4b85cad67b4a647b4cb4f7e89ed1a04bff14f6091eb257224dcc",
}
EXPECTED_LEDGER_SHA256 = (
    "5f75ad36c89a961850e0a56eae2fe8d68810f59fd5a004302e119ac25587d9b4"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def add(*vectors):
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum((Q(vector[index]) for vector in vectors), Q(0))
                 for index in range(len(vectors[0])))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


def dot(left, right):
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b) for a, b in
                zip(left, right, strict=True)), Q(0))


def rank(columns) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank width")
    rows = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        value = rows[answer][column]
        rows[answer] = [entry / value for entry in rows[answer]]
        for row in range(height):
            if row == answer or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def vector(order, values):
    return tuple(Q(values.get(label, 0)) for label in order)


def endpoint_relative_carrier_audit() -> dict[str, object]:
    maschke = load(
        "computations/verify_h3_centered_occurrence_endpoint_matching_maschke_pointed_gate.py",
        "gate_ii_uniform_carrier_maschke",
    )
    occurrences = maschke.occurrences()
    lookup = {value: index for index, value in enumerate(occurrences)}
    marked_value = (0, 1, ((2, 3), (4, 5)))
    marked = lookup[marked_value]
    size = len(occurrences)
    require(size == 90, "the endpoint occurrence count changed")
    one = (Q(1),) * size
    e_f = maschke.unit(marked, size)
    c_f = add(scale(size, e_f), scale(-1, one))

    fixed_fibre = tuple(index for index, value in enumerate(occurrences)
                        if value[:2] == marked_value[:2])
    b_01 = tuple(Q(index in fixed_fibre) for index in range(size))
    c_01 = add(scale(30, b_01), scale(-1, one))
    matching_neighbors = {
        value: maschke.matching_neighbors(value) for value in occurrences
    }
    apply_a = lambda values: maschke.apply_operator(
        values, matching_neighbors, lookup
    )
    matching_cf = add(apply_a(c_f), c_f)
    require(len(fixed_fibre) == 3
            and matching_cf == scale(3, c_01)
            and sum(c_f, Q(0)) == sum(c_01, Q(0)) == 0,
            "(A+I)c_f=3c_01 changed")

    # A monic carrier graph preserves H0.  Absolute folding by c_f does not.
    response_extended = one + (Q(0),)
    relative_graph = scale(-1, c_f) + (Q(1),)
    old_h0 = size - rank((one,))
    graph_h0 = size + 1 - rank((response_extended, relative_graph))
    absolute_h0 = size - rank((one, c_f))
    require((old_h0, graph_h0, absolute_h0) == (89, 89, 88),
            "the endpoint relative-carrier H0 test changed")

    # Applying M/3 to d beta_f=c_f-u_f gives
    # d(M beta_f/3)=c_01-u_01 with u_01=M u_f/3.  Combining with the old
    # complete endpoint response generator reconstructs only a relative
    # selected fibre: d epsilon_01=b_01-t_B, t_B=u_01/30.
    reconstructed = scale(Q(1, 30), add(one, c_01))
    require(reconstructed == b_01,
            "the relative selected-fibre reconstruction changed")

    reverse_value = (1, 0, ((2, 3), (4, 5)))
    reverse_fibre = tuple(index for index, value in enumerate(occurrences)
                          if value[:2] == reverse_value[:2])
    b_10 = tuple(Q(index in reverse_fibre) for index in range(size))
    require(len(reverse_fibre) == 3 and rank((b_01, b_10)) == 2,
            "the two endpoint chart fibres changed")

    universal = load(
        "computations/verify_h3_universal_response_deformation_e14_orbit_ks_gate.py",
        "gate_ii_uniform_carrier_universal",
    )
    universal_ledger, universal_digest = universal.audit()
    require(universal_digest == universal.EXPECTED_LEDGER_SHA256
            and universal_ledger["matching_endpoint_equivariance"]
                ["centered_KS_commutes_with_A_plus_I"]
            and not universal_ledger["matching_endpoint_equivariance"]
                ["physical_augmented_B_naturality_constructed"],
            "the universal response naturality scope changed")

    return {
        "endpoint_occurrences": size,
        "centered_marked_class": "c_f=90e_f-1_90",
        "matching_identity": "(A+I)c_f=3c_01",
        "centered_selected_fibre": "c_01=30b_01-1_90",
        "relative_graph": "d beta_f=c_f-u_f",
        "matching_transport_of_graph": (
            "d((A+I)beta_f/3)=c_01-u_01, u_01=(A+I)u_f/3"
        ),
        "relative_selected_fibre": (
            "d epsilon_01=b_01-t_B, t_B=u_01/30"
        ),
        "H0_old_relative_absolute": [old_h0, graph_h0, absolute_h0],
        "endpoint_orbit_supplies_relative_B_and_C_carriers": True,
        "absolute_B_or_C_boundary_supplied": False,
        "coefficient_matching_naturality": True,
        "fixed_physical_PP_augmented_naturality": False,
        "interpretation": (
            "the coefficient identity lands the centered response KS class "
            "on a retained selected-fibre carrier.  It does not kill that "
            "carrier or make the selected fibre a boundary in the old source"
        ),
    }


def three_chart_carrier_scope_audit() -> dict[str, object]:
    curvature = load(
        "computations/verify_h3_h2_l01_three_cap_first_pp_curvature_gate.py",
        "gate_ii_uniform_carrier_curvature",
    )
    matchings, directions, tails, l01_values, r01_values, ah_values = (
        curvature.polynomial_data()
    )
    order = tuple(matchings)
    charts = []
    for direction in directions:
        charts.append(tuple(Q(
            set(direction).issubset(set(matching))
        ) for matching in order))
    a, b, c = charts
    r01 = vector(order, r01_values)
    l01 = vector(order, l01_values)
    require(r01 == add(a, b, c)
            and l01 == add(scale(2, a), scale(-1, b), scale(-1, c))
            and rank((b, c)) == 2
            and rank((b, c, r01)) == rank((b, c, l01)) == 3
            and rank((b, c, r01, l01)) == 3,
            "the direct-versus-endpoint chart ranks changed")
    direct_dual = tuple(Q(value) for value in a)
    # Divide by the three A occurrences so this is a normalized average on A.
    direct_dual = scale(Q(1, 3), direct_dual)
    require(dot(direct_dual, b) == dot(direct_dual, c) == 0
            and dot(direct_dual, r01) == 1
            and dot(direct_dual, l01) == 2,
            "the missing direct-chart detector changed")

    # Three independent monic graphs give the desired top carriers by a
    # literal change of basis.  The construction is conditional on Gamma_A.
    local_zero = (Q(0), Q(0), Q(0))
    gamma_a = (Q(-1), Q(0), Q(0)) + (Q(1), Q(0), Q(0))
    gamma_b = (Q(0), Q(-1), Q(0)) + (Q(0), Q(1), Q(0))
    gamma_c = (Q(0), Q(0), Q(-1)) + (Q(0), Q(0), Q(1))
    require(rank((gamma_a, gamma_b, gamma_c)) == 3
            and 6 - rank((gamma_a, gamma_b, gamma_c)) == 3,
            "the three-chart graph stopped preserving the local dimension")
    gamma_r = add(gamma_a, gamma_b, gamma_c)
    gamma_l = add(scale(2, gamma_a), scale(-1, gamma_b), scale(-1, gamma_c))
    require(rank((gamma_r, gamma_l)) == 2,
            "the R/L graph basis changed")

    generic = load(
        "computations/verify_h3_generic_symmetric_c4_placement_terminal_gate.py",
        "gate_ii_uniform_carrier_c4",
    )
    generic_ledger, generic_digest = generic.audit()
    missing = generic_ledger["missing_column_and_terminal_extension"][
        "one_explicit_missing_source_column"
    ]
    require(generic_digest == generic.EXPECTED_LEDGER_SHA256
            and missing["name"] == "U_C4[D,Q01;2345]"
            and missing["status"].startswith("NOT CONSTRUCTED"),
            "the independent direct-C4 input changed")
    return {
        "chart_basis": ["AH=Dq01*H", "BH=p0s1*H", "CH=p1s0*H"],
        "endpoint_carrier_span_rank": rank((b, c)),
        "rank_after_R01_or_L01": 3,
        "direct_chart_detector_values_B_C_R_L": [
            str(dot(direct_dual, value)) for value in (b, c, r01, l01)
        ],
        "conditional_three_graphs": [
            "dGamma_A=t_A-AH", "dGamma_B=t_B-BH", "dGamma_C=t_C-CH",
        ],
        "conditional_change_of_basis": {
            "t_R": "t_A+t_B+t_C",
            "t_L": "2t_A-t_B-t_C",
            "boundaries": ["t_R-R01", "t_L-L01"],
            "preserves_local_H0": True,
        },
        "endpoint_response_deformation_constructs": ["Gamma_B", "Gamma_C"],
        "endpoint_response_deformation_does_not_construct": "Gamma_A",
        "first_independent_direct_input": missing["name"],
        "direct_input_requires_physical_cap": (
            "U_C4 must be reinserted by D*q01 with its Leibniz faces"
        ),
        "conclusion": (
            "the uniform endpoint projector does not by itself source R01 "
            "or L01.  It supplies two relative endpoint charts; the third, "
            "augmentation-one DQ chart remains independent"
        ),
    }


def first_product_rule_face_audit() -> dict[str, object]:
    curvature = load(
        "computations/verify_h3_h2_l01_three_cap_first_pp_curvature_gate.py",
        "gate_ii_uniform_carrier_pp",
    )
    matchings, directions, tails, l01_values, r01_values, ah_values = (
        curvature.polynomial_data()
    )
    d_response_values = curvature.differential(
        {matching: Q(1) for matching in matchings}
    )
    d_l01_values = curvature.differential(l01_values)
    d_r01_values = curvature.differential(r01_values)
    d_ah_values = curvature.differential(ah_values)
    order = tuple(d_response_values)
    selected_sites = {0, 1, 6, 7}
    tail = vector(order, {
        label: value for label, value in d_l01_values.items()
        if set(label[1]).isdisjoint(selected_sites)
    })
    direction = vector(order, {
        label: value for label, value in d_l01_values.items()
        if set(label[1]).issubset(selected_sites)
    })
    d_l01 = vector(order, d_l01_values)
    require(add(tail, direction) == d_l01
            and sum(bool(value) for value in tail) == 18
            and sum(bool(value) for value in direction) == 18,
            "the 18+18 product-rule split changed")

    chart_tail_counts = []
    chart_direction_counts = []
    for chart_index, chart in enumerate(directions):
        chart_matchings = {
            tuple(sorted(chart + residual)): (Q(2), Q(-1), Q(-1))[chart_index]
            for residual in tails
        }
        differential = curvature.differential(chart_matchings)
        chart_tail_counts.append(sum(
            set(label[1]).isdisjoint(selected_sites) for label in differential
        ))
        chart_direction_counts.append(sum(
            set(label[1]).issubset(selected_sites) for label in differential
        ))
    require(chart_tail_counts == chart_direction_counts == [6, 6, 6],
            "the per-chart product-rule census changed")

    selected_tail = tails[0]
    b_occurrence = tuple(sorted(directions[1] + selected_tail))
    c_occurrence = tuple(sorted(directions[2] + selected_tail))
    b_label = (b_occurrence, directions[1][0])
    c_label = (c_occurrence, directions[2][0])
    outside_label = next(label for label in d_response_values
                         if label[0] not in r01_values)
    raw_psi = vector(order, {
        b_label: Q(1), c_label: Q(1), outside_label: Q(-2),
    })
    psi = scale(Q(-1, 2), raw_psi)
    d_response = vector(order, d_response_values)
    d_r01 = vector(order, d_r01_values)
    d_ah = vector(order, d_ah_values)
    require(dot(psi, d_response) == dot(psi, d_ah) == 0
            and dot(psi, d_r01) == -1 and dot(psi, d_l01) == 1
            and dot(psi, tail) == 0 and dot(psi, direction) == 1,
            "the product-rule separating dual changed")

    maschke = load(
        "computations/verify_h3_centered_occurrence_endpoint_matching_maschke_pointed_gate.py",
        "gate_ii_uniform_carrier_pp_maschke",
    )
    maschke_ledger, maschke_digest = maschke.audit()
    pointed = maschke_ledger["pointed_relative_cone"]
    require(maschke_digest == maschke.EXPECTED_LEDGER_SHA256
            and pointed["selected_PP_rank_before_then_after_db01"] == [2, 3],
            "the selected db01 physical rank gate changed")
    return {
        "current_first_physical_nonfill": {
            "face": "selected db_01 in word 11:110000",
            "literal_terms": 6,
            "rank_before_then_after": [2, 3],
            "identity": "dc_01=30db_01-dR",
            "reason": (
                "coefficient matching naturality transports the formal "
                "carrier, but the fixed physical comparison is not PP-natural"
            ),
        },
        "strongest_grant": [
            "physical selected db_01 and endpoint-orbit mate",
            "same-grade U_C4 lower tail and its A*dH face",
        ],
        "after_strongest_grant_first_remaining_face": {
            "face": "endpoint/direction part of dL01",
            "support": 18,
            "per_chart_support": chart_direction_counts,
            "six_labelled_marginals": [6, 6, -3, -3, -3, -3],
            "primitive_profile": [2, 2, -1, -1, -1, -1],
            "normalized_Gate_II_dual_value": str(dot(psi, direction)),
        },
        "tail_half": {
            "support": 18,
            "per_chart_support": chart_tail_counts,
            "normalized_Gate_II_dual_value": str(dot(psi, tail)),
        },
        "direct_cap_Leibniz_faces": [
            "(delta D)*q01*U_C4", "D*(delta q01)*U_C4",
        ],
        "conclusion": (
            "db01 is the first ungranted physical product-rule face.  Even "
            "granting it and the lower tail does not close the carrier: the "
            "independent eighteen-term direction face remains"
        ),
    }


def downstream_scope_audit() -> dict[str, object]:
    chain = load(
        "computations/verify_h3_gate_ii_psidelta_same_grade_extension_chain.py",
        "gate_ii_uniform_carrier_chain",
    )
    chain_ledger, chain_digest = chain.audit()
    relative = load(
        "computations/verify_h3_gate_ii_three_cap_relative_tate_carrier_obstruction.py",
        "gate_ii_uniform_carrier_relative",
    )
    relative_ledger, relative_digest = relative.audit()
    word = chain_ledger["downstream_word_0102"]
    p2 = relative_ledger["downstream_P2"]
    require(chain_digest == chain.EXPECTED_LEDGER_SHA256
            and relative_digest == relative.EXPECTED_LEDGER_SHA256
            and word["word"] == "0102"
            and p2["forced_carrier_dual"]["formula"] == "C*d=12*d"
            and p2["dq_Q_ores_ladder"]["remaining_labelled_ores_detector"]
                == "-35/72",
            "the downstream carrier frontier changed")
    return {
        "propagation_after_eighteen_term_section": (
            "one labelled two-root Hasse square reaches word 0102"
        ),
        "word_0102_private_detector": word["primitive_detector"],
        "forced_word_0102_carrier_dual": "C*d=12*d",
        "q23_reinsertion": "forced dq/Q face",
        "best_formal_remaining_labelled_ores": "-35/72",
        "scalar_ordinary_residue_on_packet": "0",
        "physical_propagation_constructed_by_uniform_response_family": False,
        "accepted_terminal_now": False,
        "reason": (
            "the response parameter has no fixed word/fine/repeated AugP2 "
            "image and no physical q, W or labelled ridge before the same-"
            "grade comparison is constructed"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 Gate-II uniform-response relative-carrier landing gate",
        "pins": PINS,
        "endpoint_relative_carrier": endpoint_relative_carrier_audit(),
        "three_chart_scope": three_chart_carrier_scope_audit(),
        "first_product_rule_face": first_product_rule_face_audit(),
        "downstream_scope": downstream_scope_audit(),
        "verdict": (
            "The identity (A+I)c_f=3c_01 and the universal centered response "
            "deformation do construct presentation-safe relative carriers "
            "for the two endpoint chart fibres B and C without changing H0. "
            "They do not construct the direct Dq01 chart A, so they do not "
            "by themselves source R01 or L01.  Adding the independently "
            "missing same-grade U_C4[D,Q01;2345] and a physical cap would "
            "complete the three relative chart graphs and hence t_R,t_L. "
            "Before that grant the first physical nonfill is the invariant "
            "six-term db01 face.  Even after granting all three tail faces, "
            "the exact next independent product-rule face is the eighteen "
            "direction-factor terms of dL01.  The known descent to word 0102 "
            "and dq/Q/ores is therefore conditional, not a closed landing or "
            "an accepted terminal"
        ),
        "shortest_positive_datum": (
            "one source-labelled, termwise-PP-natural comparison for the "
            "universal endpoint carrier whose selected face is db01, plus "
            "the covariant same-grade U_C4[D,Q01;2345] cap; totalize their "
            "eighteen direction-factor faces in the labelled two-root square. "
            "The committed 0102/q/Q/ores ladder then applies"
        ),
        "scope": (
            "exact canonical h=3 endpoint occurrence, local K8 three-chart, "
            "first-PP, and pinned word-0102 carrier modules over Q.  Formal "
            "response-family graphs are not called fixed physical chains; no "
            "new q, W, ridge, target, residue or terminal row is asserted"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("uniform-response carrier ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 == "TO_BE_FROZEN":
        print("freeze EXPECTED_LEDGER_SHA256=" + digest)
        return
    print("endpoint c_f -> c_01 carrier: RELATIVE AND H0-SAFE")
    print("endpoint carrier supplies B,C charts: YES")
    print("direct Dq01 chart / U_C4 cap: INDEPENDENT AND OPEN")
    print("current first physical face: selected six-term db01")
    print("after tail grants: 18 DIRECTION-FACTOR TERMS")
    print("word-0102/dq/Q/ores propagation: CONDITIONAL")
    print("accepted terminal: NO")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
