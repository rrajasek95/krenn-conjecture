#!/usr/bin/env python3
r"""Typed composition gate for the rootless ridge/Eq/tail attachments.

The physical base correction relative to r0-T is -r_v-e_Eq.  A complete
endpoint bar route has (-Omega_v,+q_(v,N)); after multiplication by the
selected incident cycle cell its tail has the correct repeated P3+K2 site
profile.  Granting a comparison Omega_v -> r_v, it leaves +Q_(v,N).

The normal Hasse face contributes -e_Eq but no independent -Q tail.  Hence
the two paths compose only after adjoining the reduced companion cell
(0,-Q), exactly the unconstructed denominator-Tor transgression.  The
8771755 unmatched-tail theorem is a conditional routing theorem on the
off-cycle R_v tails; it is not this nullhomotopy and is vacuous on the exact
R_v=0 specialization.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = "2cd7a79b24057e3653bb0af9020f183f0544a13dbca0ef4313b53da0c9a189eb"
PINS = {
    "computations/verify_h3_rootless_normalized_c5_base_column_source_separator.py":
        "635b3e667613049817f04440401d31237db259ab7cf9948989e0da2674efb022",
    "computations/verify_h3_component_iv_endpoint_word_change_cokernel.py":
        "e452467b235391fa434ddd10364bd27a35fe32791fab8e07e5c4576dd5f5b5eb",
    "computations/verify_h3_cyclotomic_regularized_shifted_filler_normal_face.py":
        "c409a62957dba0d101d1298ec16695482fce705d3131323a8d3657074f1bf2b0",
    "computations/verify_h3_shifted_chart_h1_candidate_complete_differential.py":
        "310e9908b9445fd176b535865e10acb52bacecb72ddbf0b0d4c60ad9c69bdabf",
    "computations/verify_h3_component_iv_reduced_companion_tor_gate.py":
        "5bf7e0960b413c4e5d587b3c8f46d51493010bb73413682d7705bb28070d0935",
    "computations/verify_h3_rootless_c5_first_unmatched_tail_attachment_boundary.py":
        "ef235f2e17b7f62a7160bdc9fccd18efae5842c00ae2fc4ae7d900de34255f0d",
}

ODD = (1, 2, 3, 4, 5)
FACE_ORDER = (1, 3, 5, 2, 4)
CYCLE = frozenset(((1, 2), (2, 3), (3, 4), (4, 5), (1, 5)))
FIRST_TOR_MULTIPLIERS = {
    (1, 3): {(1, 3): (1, 2), (3, 1): (2, 3)},
    (3, 5): {(3, 5): (3, 4), (5, 3): (4, 5)},
    (5, 2): {(5, 2): (1, 5), (2, 5): (1, 2)},
    (2, 4): {(2, 4): (2, 3), (4, 2): (3, 4)},
    (4, 1): {(4, 1): (4, 5), (1, 4): (1, 5)},
}
ROWS = ("rootless_ridge", "endpoint_Omega", "Eq", "Q_tail",
        "W", "target", "ores", "ainc", "chart_S")


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def vector(**entries: int) -> tuple[int, ...]:
    require(set(entries).issubset(ROWS), ("unknown typed row", entries))
    return tuple(entries.get(row, 0) for row in ROWS)


def add(*values: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sum(value[index] for value in values)
                 for index in range(len(ROWS)))


def scale(coefficient: int, value: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(coefficient * entry for entry in value)


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for second in vertices[1:]:
        rest = tuple(site for site in vertices if site not in (first, second))
        for tail in perfect_matchings(rest):
            answer.append(tuple(sorted(((first, second),) + tail)))
    return tuple(answer)


def site_profile(edges: tuple[tuple[int, int], ...]) -> tuple[int, ...]:
    count = {site: 0 for site in ODD}
    for left, right in edges:
        count[left] += 1
        count[right] += 1
    return tuple(count[site] for site in ODD)


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")

    grade_records = []
    selected_matchings = {}
    residual_matchings = set()
    for index, left_face in enumerate(FACE_ORDER):
        right_face = FACE_ORDER[(index + 1) % len(FACE_ORDER)]
        for face, other in ((left_face, right_face),
                            (right_face, left_face)):
            matchings = perfect_matchings(tuple(site for site in ODD
                                                if site != face))
            selected = tuple(matching for matching in matchings
                             if set(matching).issubset(CYCLE))
            require(len(matchings) == 3 and len(selected) == 1,
                    "deletion face lost its selected C5 matching")
            selected_matchings[face] = selected[0]
            residual_matchings.update(matching for matching in matchings
                                      if matching != selected[0])
            multiplier = FIRST_TOR_MULTIPLIERS[(left_face, right_face)][
                (face, other)
            ]
            for matching in matchings:
                repeated_edges = tuple(sorted(matching + (multiplier,)))
                profile = site_profile(repeated_edges)
                require(sorted(profile) == [1, 1, 1, 1, 2],
                        ("cycle multiplier did not make P3+K2", face,
                         matching, multiplier, profile))
                grade_records.append({
                    "faces": [left_face, right_face],
                    "route_face": face,
                    "matching": [list(edge) for edge in matching],
                    "selected_cycle_multiplier": list(multiplier),
                    "site_profile": list(profile),
                    "normalization_value_of_multiplier": 1,
                    "fine_degree_erased_by_normalization": False,
                })

    # Coarse typed source columns.  The bar's ridge is Omega, not the
    # rootless r.  The `transported_bar` is therefore explicitly conditional
    # on an additional source comparison Omega -> r.
    endpoint_bar = vector(endpoint_Omega=-1, Q_tail=1,
                          target=0, ores=1)
    transported_bar = vector(rootless_ridge=-1, Q_tail=1, ores=1)
    normal_reduced_eq = vector(Eq=-1, chart_S=-1)
    tail_nullhomotopy = vector(Q_tail=-1, ores=-1)
    desired_correction = vector(rootless_ridge=-1, Eq=-1)

    require(add(transported_bar, normal_reduced_eq,
                tail_nullhomotopy)
            == add(desired_correction, vector(chart_S=-1)),
            "conditional three-piece composition changed")
    require(add(transported_bar, normal_reduced_eq)
            == add(desired_correction,
                   vector(Q_tail=1, ores=1, chart_S=-1)),
            "bar plus normal face stopped leaving exactly +Q")
    require(add(endpoint_bar, normal_reduced_eq,
                tail_nullhomotopy)[ROWS.index("endpoint_Omega")] == -1,
            "untransported endpoint ridge unexpectedly became rootless")
    require(add(endpoint_bar, normal_reduced_eq,
                tail_nullhomotopy)[ROWS.index("rootless_ridge")] == 0,
            "untransported composition acquired a rootless ridge")

    # Exact signs from the natural endpoint module: every route is
    # (-Omega,+q); the desired reduced augmentation is (0,-q).  The latter
    # is precisely the unconstructed Tor transgression, not a Hasse face.
    endpoint_routes = [
        vector(endpoint_Omega=-1, Q_tail=1)
        for _face in ODD for _matching in range(3)
    ]
    require(len(endpoint_routes) == 15
            and all(column == vector(endpoint_Omega=-1, Q_tail=1)
                    for column in endpoint_routes),
            "endpoint route signs changed")

    # The normal source face has only an Eq boundary in the decisive
    # projection.  Expanding h_v into q_N changes coefficients of Eq; it
    # does not create an independent Q_tail row.  At the q-zero top,
    # differentiation by N consumes q_N and leaves the unit.
    require(normal_reduced_eq[ROWS.index("Q_tail")] == 0,
            "normal Hasse face acquired a response-tail coordinate")
    require(normal_reduced_eq[ROWS.index("Eq")] == -1,
            "normal Hasse face lost its reduced Eq sign")

    # 8771755 concerns only the two off-cycle residual matchings in R_v.
    # On R_v=0 these literal occurrences vanish; the selected C5 matching,
    # which is normalized to one, is not in that theorem's ten-tail domain.
    require(len(residual_matchings) == 10,
            "normalized C5 off-cycle residual matching count changed")
    require(all(selected not in residual_matchings
                for selected in selected_matchings.values()),
            "877 tail domain acquired a selected C5 matching")

    ledger = {
        "pins": PINS,
        "repeated_site_grade_audit": {
            "records": grade_records,
            "all_site_profiles": "P3+K2=(2,1,1,1,1) up to order",
            "selected_cycle_cells_are_units_on_slice": True,
            "unit_localization_erases_fine_degree": False,
        },
        "literal_columns": {
            "row_order": list(ROWS),
            "endpoint_bar": list(endpoint_bar),
            "conditional_endpoint_bar_after_Omega_to_r": list(transported_bar),
            "derived_normal_reduced_Eq": list(normal_reduced_eq),
            "missing_tail_nullhomotopy": list(tail_nullhomotopy),
            "desired_base_correction_relative_to_r0_minus_T":
                list(desired_correction),
        },
        "conditional_composition": (
            "after a source-valid Omega_v->r_v comparison and physical "
            "promotion of the normal face, (-r_v+Q,ores=1)+(-Eq)+"
            "(-Q,ores=-1)=-r_v-Eq; the chart -S coordinate is not "
            "physical ainc"
        ),
        "committed_status": {
            "Omega_to_rootless_ridge_map": False,
            "normal_face_physical_promotion": False,
            "normal_face_contains_minus_Q_tail": False,
            "reduced_companion_minus_Q": (
                "exactly the unconstructed denominator-Tor transgression "
                "of the Component-IV reduced-companion gate"
            ),
            "composition_constructed": False,
        },
        "unmatched_tail_8771755_scope": {
            "literal_tail_occurrences": len(residual_matchings),
            "domain": "off-cycle R_v monomials with an active endpoint hole",
            "selected_C5_matching_in_domain": False,
            "on_exact_R_v_zero_specialization": "no active unmatched tail",
            "output": "unit/deletion/Fitting/offanchor/Hall routing",
            "supplies_zero-ridge_minus-Q_source_cell": False,
        },
        "verdict": (
            "paths #1 and #2 meet at the same formal Q-tail cancellation, "
            "but no committed source cell realizes it: the normal face has "
            "no -Q component, 8771755 is not a nullhomotopy, and Omega/ridge "
            "typing remains distinct"
        ),
        "smallest_shared_attachment": (
            "a multidegree-preserving mapping-cone cell whose boundary is "
            "the transported endpoint route plus the physical reduced-Eq "
            "face and whose all-D companion is -Q_(v,N); equivalently the "
            "selected denominator Tor kernel vector plus Omega->ridge typing"
        ),
        "scope": (
            "exact conditional composition and sharp type no-go for the "
            "committed bar/normal/877 inventories; no arbitrary higher "
            "relative generator is excluded"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("h=3 rootless ridge/Eq/tail attachment composition: CONDITIONAL")
    print("endpoint bar: -Omega + Q")
    print("normal face: -Eq, not -Eq-Q")
    print("missing transgression: -Q")
    print("877 unmatched-tail theorem supplies nullhomotopy: NO")
    print("physical base column constructed: NO")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
