#!/usr/bin/env python3
"""Audit the last K d(u_012) interface in the cut-swap odd prism.

The collision-label calculation fixes all signs.  If W=001122,
W'=021102, rho=(1 4), and w is the signed two-root 0<->2 Weyl action,
then for the unsigned nine-label 012 packet u

    (1-rho)(w-1)u_W = l_W+l_W',   l=(rho-1)u.

Thus the filtered auxiliary is -rho F_W, and

    F_W-rho F_W-K(u)  has residual K d(u).

The committed data do not yet define that residual labelwise.  The
15-label module only has an occurrence shadow, while the literal M_v image
has 360 seven-edge features in the eight-site repeated P3+K2 module.  A
physical shifted label/tail map between those bases is exactly the missing
datum.  Hence equality with M_v is presently ill-typed, not disproved.

The checker also excludes the root-even adjacent-power cell as the residual:
K d(u) lies in the rho-odd image of 1-rho, whereas that companion is
rho-even and target-bearing.  The proposed D+S split requires precisely
that independent even companion and is not a workaround.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_complete_tangent_lower_protected_phi_reduction.py":
        "ea45c09a8347c312ea9721475d54a4b4f9aad21d8d51cb9d4d297aeaa99ba429",
    "computations/verify_h3_cut_swap_collision_word_orbit_obstruction.py":
        "d7281084a0fc084e6d951f527daf92c92faefebec183a83d6cfa33e055596c77",
    "computations/verify_h3_literal_mv_cap_cartan_composition.py":
        "8e54a161402499c638dcba6177069fc3bb37648fb37c3546955310a56889744e",
    "computations/verify_h3_signless_cartan_adjacent_power_shared_cell_gate.py":
        "9679c047e440f48899f1385682bcf64b725e049da01a42b8134b40c3fda73177",
    "computations/verify_h3_order6_endpoint_odd_hpl_secondary_transfer.py":
        "5a89d25227562b397d6cf3f16306346ce7d9fd16fb73a0f0a4486355a7cef29e",
}
EXPECTED_LEDGER_SHA256 = (
    "86c90e8001f6a7bb7153602183813759cdccb362040eb88567727bd8e6b84982"
)

W = (0, 0, 1, 1, 2, 2)
WP = (0, 2, 1, 1, 0, 2)
RHO = (0, 4, 2, 3, 1, 5)
ROOT_SITES = (1, 4)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def add(*vectors):
    answer = defaultdict(Q)
    for vector in vectors:
        for basis, value in vector.items():
            answer[basis] += Q(value)
    return {basis: value for basis, value in answer.items() if value}


def scale(value, vector):
    return {basis: Q(value) * Q(coefficient)
            for basis, coefficient in vector.items()
            if Q(value) * Q(coefficient)}


def permute_edge(edge, permutation):
    return tuple(sorted(permutation[site] for site in edge))


def permute_matching(matching, permutation):
    return tuple(sorted(permute_edge(edge, permutation) for edge in matching))


def rho_word(word):
    answer = [None] * len(word)
    for old_site, colour in enumerate(word):
        answer[RHO[old_site]] = colour
    return tuple(answer)


def weyl_word(word):
    answer = list(word)
    sign = 1
    for site in ROOT_SITES:
        if answer[site] == 0:
            answer[site] = 2
            sign *= -1
        elif answer[site] == 2:
            answer[site] = 0
    return tuple(answer), sign


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    lower = load(
        "computations/verify_h3_complete_tangent_lower_protected_phi_reduction.py",
        "kdu_lower",
    )
    tangent = load(
        "computations/verify_h3_tangent_euler_occurrence_splitter_fredholm.py",
        "kdu_tangent",
    )
    literal = load(
        "computations/verify_h3_residual_q_literal_mapping_cone_private_boundary_gate.py",
        "kdu_literal",
    )
    complete = load(
        "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py",
        "kdu_complete",
    )
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "kdu_base",
    )
    mv = load(
        "computations/verify_h3_literal_mv_cap_cartan_composition.py",
        "kdu_mv",
    )
    signless = load(
        "computations/verify_h3_signless_cartan_adjacent_power_shared_cell_gate.py",
        "kdu_signless",
    )
    hpl = load(
        "computations/verify_h3_order6_endpoint_odd_hpl_secondary_transfer.py",
        "kdu_hpl",
    )

    base_labels = lower.lower_labels(tangent, (0, 1, 2))
    other_labels = lower.lower_labels(tangent, (0, 2, 4))
    key = lambda label: (label[1], label[2])
    u_labels = frozenset(map(key, base_labels))
    all_labels = tuple(sorted(u_labels | frozenset(map(key, other_labels))))

    def rho_label(label):
        matching_index, repeated_edge = label
        matching = permute_matching(tangent.MATCHINGS[matching_index], RHO)
        return (tangent.MATCHING_INDEX[matching],
                permute_edge(repeated_edge, RHO))

    def rho_vector(vector):
        return {
            (rho_word(word), rho_label(label)): value
            for (word, label), value in vector.items()
        }

    def weyl_vector(vector):
        answer = defaultdict(Q)
        for (word, label), value in vector.items():
            changed, sign = weyl_word(word)
            answer[(changed, label)] += sign * value
        return dict(answer)

    u_w = {(W, label): Q(1) for label in u_labels}
    rho_u_w = rho_vector(u_w)
    l = {
        label: Q(int(label in set(map(rho_label, u_labels))))
        - Q(int(label in u_labels))
        for label in all_labels
    }
    l = {label: value for label, value in l.items() if value}
    expected_corners = add(
        {(W, label): value for label, value in l.items()},
        {(WP, label): value for label, value in l.items()},
    )
    boundary = add(
        add(weyl_vector(u_w), scale(-1, u_w)),
        scale(-1, rho_vector(add(weyl_vector(u_w), scale(-1, u_w)))),
    )
    require(boundary == expected_corners,
            ("odd prism corner signs changed", boundary, expected_corners))
    require(weyl_word(W) == (WP, -1)
            and weyl_word(WP) == (W, -1)
            and rho_word(W) == WP and rho_word(WP) == W,
            "the W/W' signed action changed")
    require(len(all_labels) == 15 and len(l) == 12,
            "the collision packet changed")

    # rho(v)=-v and rho(l)=-l.  Therefore -rho F_W has the same top/lower
    # orientations in W' as F_W has in W.  Its sum with F_W has exactly the
    # two corner packets above.  Subtracting K(u) leaves +K d(u), by
    # dK+Kd=(1-rho)(w-1).
    l_w = {(W, label): value for label, value in l.items()}
    auxiliary = scale(-1, rho_vector(l_w))
    require(auxiliary == {(WP, label): value for label, value in l.items()},
            "the complementary filtered lower acquired the wrong sign")
    require(add(l_w, auxiliary) == expected_corners,
            "the two filtered lowers stopped matching the odd-prism corners")

    lower_ledger, lower_digest = lower.audit()
    require(lower_digest == lower.EXPECTED_LEDGER_SHA256,
            "the complete lower ledger changed")
    require("does not construct the physical 15-label Phi"
            in lower_ledger["scope"],
            "the input checker now claims a physical comparison")

    # Reconstruct one of the 75 actual normalized M_v literal boundaries.
    left, _right, left_cell, _right_cell = complete.CUBIC_PAIRS[0]
    degree = complete.degree_add(
        base.lambda_degree(left),
        complete.cell_degree(complete.CYCLE_CELLS[left_cell]),
    )
    component = complete.component(base, degree)
    pure = [(word, multiplier, row) for word, multiplier, row
            in component["columns"] if word == complete.PURE_WORD]
    selected = pure[:4]
    literal_boundary = defaultdict(Q)
    for coefficient, (_word, _multiplier, row) in zip(
            literal.ALPHA, selected, strict=True):
        for feature in row:
            literal_boundary[feature] += coefficient
    literal_boundary = {feature: value for feature, value
                        in literal_boundary.items() if value}
    require(len(literal_boundary) == 360,
            "the representative literal M_v boundary changed")
    feature_cell_counts = {len(feature) for feature in literal_boundary}
    feature_site_sets = {
        tuple(sorted({site for cell in feature for site in cell[:2]}))
        for feature in literal_boundary
    }
    require(feature_cell_counts == {7}
            and feature_site_sets == {tuple(range(8))},
            "the literal M_v basis type changed")

    mv_ledger, mv_digest = mv.audit()
    require(mv_digest == mv.EXPECTED_LEDGER_SHA256
            and mv_ledger["composition"]["M_v_equals_minus_O_plus_K"][
                "literal_boundary_support"] == 360,
            "the positive literal M_v theorem changed")

    hpl_ledger, hpl_digest = hpl.audit()
    require(hpl_digest == hpl.EXPECTED_LEDGER_SHA256
            and "construct/identify the filtered chain map"
            in hpl_ledger["remaining_comparison"],
            "the operator/correction comparison status changed")

    signless_ledger, signless_digest = signless.audit()
    require(signless_ledger["cell_and_terminal_types"][
                "signless_relative_cell"]["rho_parity"] == "even"
            and signless_ledger["cut_and_target"][
                "signless_target_defect"] == "2*(w-1)*Delta",
            "the root-even companion type changed")

    ledger = {
        "theorem": "cut-swap odd-prism Kd typing gate",
        "pins": PINS,
        "exact_corner_calculation": {
            "W": "001122",
            "W_prime": "021102",
            "w_W": "-W_prime",
            "w_W_prime": "-W",
            "rho_W": "W_prime",
            "unsigned_u012_labels": len(u_labels),
            "physical_collision_labels": len(all_labels),
            "l_support": len(l),
            "identity": "(1-rho)(w-1)u_W=l_W+l_Wprime",
            "filtered_auxiliary": "F_Wprime=-rho F_W",
            "totalization": (
                "F_W-rho*F_W-K(u012) has residual +K*d(u012); "
                "reversing the global K convention reverses both signs"
            ),
        },
        "literal_type_comparison": {
            "collision_basis": "(six-site matching, repeated collision edge)",
            "collision_basis_size": len(all_labels),
            "available_boundary": (
                "only the 15-coordinate occurrence-forgetful shadow; the "
                "complete protected J_col columns are not constructed"
            ),
            "M_v_basis": (
                "eight-site decorated seven-edge monomials in one labelled "
                "repeated P3+K2 component"
            ),
            "M_v_literal_support": len(literal_boundary),
            "equality_Kd_u012_equals_M_v_well_typed": False,
            "reason": (
                "no committed map sends each collision label, with its word "
                "and repeated-edge grade, to the seven-edge literal feature "
                "module.  Comparing the 12-coordinate corner shadow with "
                "the 360 literal features would assume the desired Phi"
            ),
            "smallest_missing_interface": (
                "a source-provenant shifted tail/label map tau on the 15 "
                "collision labels, agreeing on the three shared labels, "
                "such that the complete protected boundary of tau(u012) "
                "can be compared with J(M_v)"
            ),
        },
        "parity_and_D_plus_S": {
            "K_d_u012_parity": (
                "rho-odd, because K=(1-rho)H_w has image in im(1-rho)"
            ),
            "root_even_adjacent_power_companion_parity": "rho-even",
            "root_even_companion_target": "-2*(w-1)*Delta",
            "residual_is_root_even_companion": False,
            "D_plus_S_verdict": (
                "the formal S needed to split l_W from l_Wprime is the "
                "rho-even corner.  Its physical realization is exactly the "
                "independent target-bearing C_plus gate, so (D+S)/2 does "
                "not bypass either the Kd comparison or C_plus"
            ),
        },
        "sharp_status": (
            "all W/W' signs and complementary-word absorption are fixed.  "
            "The sole remaining equality cannot yet be evaluated labelwise: "
            "the physical J_col/tail map is the missing source datum.  The "
            "difference cannot be reclassified as the known root-even "
            "adjacent-power companion by parity and target type"
        ),
        "nonclaims": [
            "K*d(u012) is not asserted unequal to M_v",
            "the occurrence shadow is not promoted to a protected boundary",
            "no general-Y comparison is claimed",
        ],
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("cut-swap odd-prism Kd ledger changed", digest))
    return ledger, digest


def main():
    ledger, digest = audit()
    print("h3 cut-swap odd-prism Kd typing gate: PASS")
    print("corner identity: (1-rho)(w-1)u=l_W+l_Wprime")
    print("filtered residual: +K*d(u012)")
    print("Kd versus literal M_v: NOT YET WELL-TYPED")
    print("root-even C_plus: EXCLUDED AS THIS RESIDUAL")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
