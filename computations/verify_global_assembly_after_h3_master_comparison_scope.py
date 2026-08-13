#!/usr/bin/env python3
"""Audit whether the h=3 master comparison closes the all-even conjecture.

The exact descent argument is uniform: at order N=2h+2 it needs an active
clean cap (or a contradiction) for every h>=3.  The current reduced-Eq
master comparison and selected Xi/M_v equation are explicitly h=3 objects.
This checker pins that scope, the uniform prolongation warning, the
face-zero and terminal-promotion guards, and the certified-spine ledger.

It also exhausts the finite logical shadow of the minimal-order induction:
once the *uniform* bridge says every bad N>=8 descends to bad N-2 and N=6
is impossible, no bad even order exists.  Thus induction is not the gap;
the missing implication is the uniform packet-to-active-clean/terminal
bridge (SP-CLEAN-BRIDGE), including physical terminal promotion.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_reduced_eq_integral_rho_comparison_master_gate.py":
        "813419c756e7f21c09d63d3ec10f44c787e9580ca08c87809b7c4c550b908b4f",
    "computations/verify_h3_selected_lower_one_chain_comparison_reduction.py":
        "c9fc8c847327d0e119264a3a83cf39d0f4c2ff45b4ddd4e048f42a57cac0e887",
    "computations/verify_uniform_adjacent_cycle_filtered_prolongation.py":
        "2b2555fac43a5914469a857b3a6bf19aa715ab6576220dc1dfd66dd808cad86e",
    "computations/verify_clean_pair_cap_exact_descent_target.py":
        "263e8cc2fad4143803e0ce88d248c44a085a271b2d1569de86410c4448a47659",
    "computations/verify_h3_six_term_exhaustive_relative_extension_alternative.py":
        "bcc55b05c10ba1ac6f3c4415c18a70274ecc29dd506fbed8e69d471b5f0a5607",
    "computations/verify_h3_rootless_augmented_pentagon_fredholm_alternative.py":
        "0b0831391416f85302b5f2d89da0672e07dca4c73fc5f3893ad992abd48c1d2b",
    "computations/verify_h3_anchor_conormal_functoriality_bridge.py":
        "83879756547765878c36944c1ab14827ab77a1f217931bc05db0c72cb0af32a8",
    "computations/verify_h3_component_iv_face_zero_routing_boundary.py":
        "217d14b451a36b6e86caadf14bd5ce63aeda484f8e0917b7f2e1034b640a4fc0",
    "notes/h3-reduced-eq-integral-rho-comparison-master-gate.md":
        "3fa8fdc6bcd17145bc1e40c608259b2312ee52f1482520fbe9e0f5a3cd1e7a76",
    "notes/h3-selected-lower-one-chain-comparison-reduction.md":
        "429f7a99ce89bdeaaa62afd08bbadad1e6cb08c20c725bd9d46867ce43f21b16",
    "notes/uniform_adjacent_cycle_filtered_prolongation.md":
        "90926cce63f1dec2a6fe62900afa0c29bea454d642c5b68b9791c5f87904f8bc",
    "notes/unified-full-nine-two-chart-overlap-jet-saturation-target.md":
        "84a2498eca71bf8813fb748832000b21693c0d8280b56a9baa66b9f33deec4fb",
    "notes/clean-pair-cap-exact-descent-target.md":
        "90f49ac4fde9b793409d9081977e7a7135ebd76c1b5df5d699387d142c2b9b75",
    "notes/clean-bridge-at-eight-is-the-open-case.md":
        "86b4f7d19443ab48c2df4a29cb644829fbcb5c24b1d5c7a200253d0ee394b468",
    "notes/h3-rootless-augmented-pentagon-fredholm-alternative.md":
        "4febecdfa01b6697970af0d518721058842afe784ac59f267b8ebc847a43cecb",
    "notes/h3-component-iv-face-zero-routing-boundary.md":
        "21e1ee5557dbaee26cf564353d06d9e2a5fca5c3877290f87c1665b9af4c37e9",
    "formal/FORMALIZATION.md":
        "38ba8b03507275f7887715008be4b55f94ef28a5678a74ff504177b8a21943df",
    "certification/BASELINE.md":
        "2b3a966a7873a58569e1f4ae0d94d4f32c7139da4bcdaef2cef4bddb254b7f24",
    "certification/SUPERSESSIONS.md":
        "9a758003df15c97ac3b69d36ccf3edfae289ca27b7afd94dd448cf99c85ecda1",
}
EXPECTED_LEDGER_SHA256 = "11fd5ec313498002fd3013883626a117d4d2bad22b72abfce605d352bf3283c0"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def literal_scope_audit() -> dict[str, object]:
    h3_master = (ROOT / (
        "computations/verify_h3_reduced_eq_integral_rho_comparison_master_gate.py"
    )).read_text()
    selected = (ROOT / (
        "notes/h3-selected-lower-one-chain-comparison-reduction.md"
    )).read_text()
    uniform = (ROOT / (
        "notes/uniform_adjacent_cycle_filtered_prolongation.md"
    )).read_text()
    unified = (ROOT / (
        "notes/unified-full-nine-two-chart-overlap-jet-saturation-target.md"
    )).read_text()

    require("At h=3" in h3_master
            and "Phi:U_{15}\\longrightarrow L_{h=3}" in selected,
            "the literal h=3 master-comparison scope changed")
    require(r"site suspension of the hypothetical \(h=3\) row does not prove"
            in uniform
            and r"Suppose, for every relevant \(h\ge3\)" in uniform,
            "the uniform-prolongation warning changed")
    require(r"The theorem is uniform in \(h\ge3\)" in unified
            and r"an \(h=3\) two-column or grade-split"
            in unified
            and "only a bounded test" in unified,
            "the global unified-theorem scope changed")
    return {
        "literal_master_order": "h=3, hence N=2h+2=8",
        "selected_map": "Phi:U15 -> L_{h=3}",
        "uniform_h_ge_3_comparison_constructed": False,
        "site_suspension_suffices": False,
        "global_target_scope": "every h>=3 and every automatic two-chart packet",
    }


def induction_audit() -> dict[str, object]:
    # Exhaust every putative set of bad even orders through 20.  The two
    # mathematical implications are: 6 is not bad (SP-K6), and every bad
    # N>=8 produces a bad N-2 source (SP-DESCENT after SP-CLEAN-BRIDGE).
    orders = tuple(range(6, 22, 2))
    admissible_bad_sets = []
    for bits in product((False, True), repeat=len(orders)):
        bad = {order for order, bit in zip(orders, bits, strict=True) if bit}
        if 6 in bad:
            continue
        if any(order >= 8 and order - 2 not in bad for order in bad):
            continue
        admissible_bad_sets.append(tuple(sorted(bad)))
    require(admissible_bad_sets == [()],
            ("minimal-order induction acquired a survivor", admissible_bad_sets))
    return {
        "orders_exhausted": list(orders),
        "candidate_bad_sets": 2 ** len(orders),
        "sets_compatible_with_K6_and_uniform_descent": 1,
        "unique_compatible_set": [],
        "induction_gap": False,
        "uniform_bridge_gap": True,
    }


def terminal_promotion_audit() -> dict[str, object]:
    q_alternative = (ROOT / (
        "notes/h3-six-term-exhaustive-relative-extension-alternative.md"
    )).read_text()
    fredholm = (ROOT / (
        "notes/h3-rootless-augmented-pentagon-fredholm-alternative.md"
    )).read_text()
    face_zero = (ROOT / (
        "notes/h3-component-iv-face-zero-routing-boundary.md"
    )).read_text()
    require("The theorem does not manufacture the physical map" in q_alternative,
            "the six-term alternative lost its physical-map guard")
    require(r"When \(Q\) is the source-provenant terminal/Macaulay quotient"
            in fredholm,
            "the rootless separator lost its terminal-quotient hypothesis")
    require("No existing rootless-to-inactive landing" in face_zero
            and "Neither implication is present" in face_zero
            and "committed dependency graph" in face_zero,
            "the face-zero routing guard changed")
    return {
        "q_linear_alternative": (
            "generator in ker(J) or left separator of the augmented image"
        ),
        "q_alternative_alone_is_global_terminal": False,
        "extra_terminal_hypothesis": (
            "the quotient/comparison is the actual source-provenant "
            "terminal-Macaulay quotient, so its generator/separator is a "
            "contradiction or the required physical anchor"
        ),
        "simultaneous_face_zero_routing_constructed": False,
        "missing_face_zero_clause": (
            "rootless source implies some h_v is nonzero, or the all-zero "
            "stratum routes source-validly to a closed inactive/unit branch"
        ),
    }


def certification_audit() -> dict[str, object]:
    baseline = (ROOT / "certification/BASELINE.md").read_text()
    supersessions = (ROOT / "certification/SUPERSESSIONS.md").read_text()
    formalization = (ROOT / "formal/FORMALIZATION.md").read_text()
    require("`SP-CLEAN-BRIDGE`" in baseline
            and "Open implication" in baseline,
            "the certified bridge status changed")
    require("Dependency ID: `SP-CLEAN-BRIDGE`" not in supersessions,
            "SP-CLEAN-BRIDGE acquired a supersession; update this audit")
    require("A6" in formalization
            and "identification needs A1–A4b" in formalization,
            "the k_max model-bridge ledger changed")
    return {
        "certified_open_dependency": "SP-CLEAN-BRIDGE",
        "accepted_supersession_present": False,
        "research_commits_change_certified_spine": False,
        "k_max_identification_formalized": False,
        "formalization_tail_only": (
            "aggregation, exact palette/range, and identification of k_max "
            "with solvable EqSystem palette size are not yet all in Lean; "
            "the prose descent theorem already supplies the mathematical "
            "aggregate-to-decorated reconstruction and palette projection"
        ),
    }


def global_dependency_theorem() -> dict[str, object]:
    return {
        "theorem": (
            "For every h>=3 and N=2h+2, suppose every synchronized "
            "maximum-anchor/minimum-support exact ternary source has its "
            "automatic full-nine two-chart packet, and a branch-complete "
            "pointed augmented comparison-or-terminal theorem sends that "
            "packet either to an active clean cap or to an actual physical "
            "contradiction.  If the comparison covers both mixed gcd "
            "assignments, all rootless tails, every inactive normal/trace "
            "face through order h, the simultaneous face-zero stratum, and "
            "its terminal quotients, then SP-DESCENT plus SP-K6 exclude exact "
            "ternary sources at every even N>=6.  Palette projection then "
            "gives k_max(N)<=2"
        ),
        "proved_consumers": [
            "synchronized maximum-anchor/minimum-support selection",
            "physical curvature line and automatic two-chart extraction",
            "exact active-clean N-to-N-2 descent",
            "six-site arbitrary-complex obstruction",
            "palette projection from D>=3 to D=3",
        ],
        "clauses_not_contained_in_literal_h3_master": [
            "uniform construction for every h>=3",
            "application to every automatic full-nine packet/chart assignment",
            "rootless residual-tail and simultaneous h_v=0 routing",
            "all inactive normal, intrinsic order-h, and horizontal Rees faces",
            "promotion of every local q/Fredholm dual to the actual terminal quotient",
            "an explicit implication from the comparison outputs to active cleanliness or contradiction",
        ],
        "mechanization_tail_not_an_extra_mathematical_hypothesis": [
            "A1--A4b and A6 are not all formalized in Lean",
            "the committed prose proof of SP-DESCENT reconstructs a finite "
            "decorated ternary source and projects every palette D>=3 to D=3",
        ],
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "global assembly scope after the h=3 master comparison",
        "pins": PINS,
        "literal_scope": literal_scope_audit(),
        "minimal_order_induction": induction_audit(),
        "terminal_promotion": terminal_promotion_audit(),
        "certified_spine": certification_audit(),
        "precise_strong_conditional": global_dependency_theorem(),
        "answer_to_audit": (
            "NO for the literal assumed h=3 comparison.  YES only after it "
            "is strengthened to the displayed uniform branch-complete and "
            "terminal-promoting theorem for every h>=3.  The first missing "
            "global implication is comparison-or-terminal on one canonical "
            "h=3 packet => SP-CLEAN-BRIDGE on every automatic packet/order"
        ),
        "first_unavoidable_global_obstruction": (
            "uniform physical descent/terminal promotion, not induction: "
            "the h=3 comparison has no proved source-labelled prolongation "
            "to the intrinsic order-h inactive faces, and the q/Fredholm "
            "linear alternative is terminal only after comparison with the "
            "actual source-provenant terminal quotient"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("global assembly ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("global assembly after h3 master: LOCAL ASSUMPTION INSUFFICIENT")
    print("minimal-order induction: COMPLETE once uniform bridge is granted")
    print("first missing implication: h3 Phi -> uniform SP-CLEAN-BRIDGE")
    print("terminal promotion and face-zero/intrinsic-order-h routing: OPEN")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
