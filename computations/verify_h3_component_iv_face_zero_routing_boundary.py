#!/usr/bin/env python3
"""Exact routing boundary after the Component-IV face separator.

This checker records two facts needed to interpret the separator correctly:

* curvature localization alone does not force a deleted-face hafnian to be
  nonzero (both exact rational curvature guards have all h_v=0); and
* the five-cycle Laurent model makes every h_v a unit, so the five selected
  memberships are impossible there.

The Laurent model is a specialization used to test the rootless module; it
is not a chart-cover theorem for physical sources.  No claim is made that
the full-source scalar-zero locus is nonempty or that it lands in the
all-inactive cap-line branch.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

import verify_h3_component_iv_selected_denominator_membership_separator as SEP
import verify_h3_denominator_tor_transgression_fitting_gate as TRANS
import verify_h3_rootless_five_cycle_first_tor_multidegree_gate as C5


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_DIGEST = "4fc6820616d135d0e04df3232134e5c54a4e94e9689d3cd90d54a989526f4197"
PINS = {
    "computations/verify_h3_component_iv_selected_denominator_membership_separator.py":
        "859a5e3fc4b942858ded8544333b885a04d1e5e91ae3803e6e0c562393e3b7da",
    "computations/verify_h3_denominator_tor_transgression_fitting_gate.py":
        "33cd6ac3de85f83ee16189601930938d73f35f2fef5db20253380801bdd78459",
    "computations/verify_h3_rootless_five_cycle_first_tor_multidegree_gate.py":
        "a5d9021664b904f895323c29806a825545afd16085c971dc573353bb6c11a81f",
    "notes/two-chart-joint-hypothesis-extraction.md":
        "68554fc43835c2a8aa32d0297bc14cf23a45d7385a8ddf1d1265dedb802b3ab3",
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative, actual))


def curvature_does_not_force_face_open():
    packets = {}
    for name in ("direct_free", "tilted"):
        audit = TRANS.packet_audit(name)
        require(audit["kappa"] != "0", (name, "curvature vanished"))
        require(audit["h_values"] == ["0"] * 5,
                (name, "left the simultaneous face-zero locus"))
        packets[name] = {
            "kappa": audit["kappa"],
            "h_values": audit["h_values"],
            "is_full_source_point": False,
            "failed_membership_faces": [
                site for site, hit in
                zip(TRANS.SITES, audit["individual_classes_hit"])
                if not hit
            ],
        }
    return {
        "packets": packets,
        "proved_implication_false": "kappa != 0 implies some h_v != 0",
        "scope": (
            "the guards are not full-source points, so they do not prove "
            "that the full-source intersection V(h_1,...,h_5) is nonempty"
        ),
    }


def c5_laurent_membership_verdict():
    # Order: (h1,h3,h5,h2,h4), variables (a,b,c,d,e).
    generators = C5.c5_generators()
    expected = (
        (0, 1, 0, 1, 0),  # b*d
        (1, 0, 0, 1, 0),  # a*d
        (1, 0, 1, 0, 0),  # a*c
        (0, 0, 1, 0, 1),  # c*e
        (0, 1, 0, 0, 1),  # b*e
    )
    require(generators == expected, "C5 face generators changed")
    require(all(sum(generator) == 2 for generator in generators),
            "a C5 face ceased to be a quadratic monomial")

    # At a=b=c=d=e=1 all five h's equal one; in the Laurent ring every
    # displayed monomial is a unit.  SEP then forbids each membership in a
    # nonzero quotient.
    values_at_diagonal = [1] * len(generators)
    require(values_at_diagonal == [1] * 5, "diagonal C5 point changed")
    separator = SEP.symbolic_separator()
    require(separator["localized_consequence"]
            == "over S[h_v^-1], membership is impossible unless 1=0",
            "membership localization theorem changed")
    return {
        "variable_laurent_product": "a*b*c*d*e",
        "face_order": ["h1", "h3", "h5", "h2", "h4"],
        "face_monomials": ["b*d", "a*d", "a*c", "c*e", "b*e"],
        "all_five_faces_are_units": True,
        "all_five_memberships_in_a_nonzero_quotient": False,
        "diagonal_point": "a=b=c=d=e=1, hence every h_v=1",
        "scope": (
            "this is the exact Laurent C5 test specialization, not a "
            "source-routing or chart-cover theorem"
        ),
    }


def main():
    pin_dependencies()
    ledger = {
        "scope": "routing after the h=3 Component-IV face separator",
        "curvature_only": curvature_does_not_force_face_open(),
        "rootless_C5_Laurent_test": c5_laurent_membership_verdict(),
        "physical_branch_boundary": {
            "open_union_D_hv": (
                "the five memberships contradict every nonzero source "
                "quotient on this open union"
            ),
            "closed_face_zero_locus": "V(h_1,h_2,h_3,h_4,h_5)",
            "existing_routing_to_all_inactive": False,
            "reason": (
                "rootless/all-inactive is the gcd split of the clean-error "
                "polynomial on a cap line; h_v are five internal deleted-"
                "face coefficients at one output word"
            ),
            "exact_missing_landing": (
                "prove a physical rootless source meets union_v D(h_v), "
                "or prove that its simultaneous face-zero stratum routes "
                "to an already-closed inactive/source-unit branch"
            ),
            "converse_membership_on_face_zero_locus_pursued": False,
        },
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST, ("ledger changed", digest))

    print("h=3 Component-IV face-zero routing boundary: PASS")
    print("kappa-localization alone: does not force any h_v nonzero")
    print("C5 Laurent test: all h_v units, hence all five memberships impossible")
    print("physical V(h_1,...,h_5) -> all-inactive routing: NOT PROVED")
    print(f"ledger sha256: {digest}")


if __name__ == "__main__":
    main()
