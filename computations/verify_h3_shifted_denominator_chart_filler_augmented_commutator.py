#!/usr/bin/env python3
"""Augmented differential of the first shifted denominator chart filler.

The external two-edge face required by f872900 is realized in the complete
Hasse/Koszul/cap totalization.  It has zero target and ordinary residue and,
after chart subtraction, the required -S_v terminal correction.  Its
isolated underived differential has the exact first commutator

    h_v * (H_0-u) * e_Eq.

All Boolean Hasse faces cancel that commutator in the derived presentation.
At the q-zero top the commutator becomes (H_0-u)e_Eq, proving that physical
underived descent, not target/ores or chart parity, is the remaining gate.
"""

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
QQ = Fraction
DELETED = 1
EXPECTED_DIGEST = "bdcc6a2734c3bd31f060d56fd88f8f5344f39e43aed03f70f18cfa65eef74b92"
PINS = {
    "computations/verify_h3_non_euler_chart_h1_first_comparison_gate.py":
        "f96cf470fc09255dd092b0d904c2aa85bab3d9ca6966c48c383a19b5ce31e54d",
    "computations/verify_h3_full_hasse_koszul_cap_totalization.py":
        "51940ce0ac8387b68e7725508db6da1a1c055ea036335bbf19750580c69e13fb",
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"pinned dependency changed: {relative}")


GATE = load(
    "h3_shifted_denominator_augmented_gate",
    "verify_h3_non_euler_chart_h1_first_comparison_gate.py",
)
TOTAL = load(
    "h3_shifted_denominator_augmented_total",
    "verify_h3_full_hasse_koszul_cap_totalization.py",
)


def module_subtract(left, right):
    return TOTAL.module_add(left, TOTAL.module_scale(-1, right))


def audit():
    pin_dependencies()
    gate, gate_digest = GATE.audit()
    require(gate_digest
            == "980a89c64009ba6eedbaa7f2c6969b8fcf7b2bfe4031983a163360bf6126c91e",
            "first comparison gate changed")
    require(gate["earliest_candidate"]["principal_parts_order"] == 2
            and gate["earliest_candidate"]["required_chart_tail"] == "-S_v",
            "first comparison candidate changed")
    require(gate["minimal_shift"]["shift_sites"] == [0, 6, 7]
            and gate["minimal_shift"]["shift_weight"] == 3,
            "unique sigma shift changed")

    matching = TOTAL.matchings(TOTAL.face(DELETED))[0]
    internal = TOTAL.internal_variables(matching)
    marked_u, marked_t = TOTAL.endpoint_variables(DELETED)
    eps_u, eps_t, eps_e, eps_f = tuple(
        ("eps", name) for name in ("u", "t", "e", "f")
    )
    directions = {
        marked_u: eps_u,
        marked_t: eps_t,
        internal[0]: eps_e,
        internal[1]: eps_f,
    }
    total_chain, total_boundary, differential, target, ores = (
        TOTAL.translated_totalization(directions)
    )
    all_eps = (eps_u, eps_t, eps_e, eps_f)
    internal_eps = (eps_e, eps_f)

    # Complete external face: tau_int(h_v)*(r_0-T).  Its coefficient at
    # internal order zero is the desired initial h_v-layer filler.
    external_chain = TOTAL.module_external_face(
        total_chain, (eps_u, eps_t)
    )
    external_boundary = TOTAL.module_external_face(
        total_boundary, (eps_u, eps_t)
    )
    h_v = TOTAL.face_hafnian(DELETED)
    initial_chain = TOTAL.module_coefficient(
        external_chain, (), internal_eps
    )
    initial_boundary = TOTAL.module_coefficient(
        external_boundary, (), internal_eps
    )
    expected_initial_chain = {
        "r_0": h_v,
        "T": TOTAL.scale(-1, h_v),
    }
    expected_initial_boundary = {
        "w": TOTAL.multiply(h_v, TOTAL.CAP_Y)
    }
    require(initial_chain == expected_initial_chain,
            "external order-two filler is not h_v*(r_0-T)")
    require(initial_boundary == expected_initial_boundary,
            "external order-two boundary is not h_v*Y*w")
    require(not TOTAL.apply_module_map(initial_chain, target),
            "initial filler retained target")
    require(not TOTAL.apply_module_map(initial_chain, ores),
            "initial filler retained ordinary residue")

    # The complete two-direction indexed Hasse companion.  This is the
    # actual derived-presentation chain whose diagonal term is
    # h_v*r_0[empty].  The four other source terms cancel its Eq residual.
    two_directions = (marked_u, marked_t)
    source_companion = TOTAL.indexed_top_koszul_cycle(two_directions)
    require(not TOTAL.indexed_hasse_chain_differential(
        source_companion, two_directions
    ), "two-direction indexed Hasse companion is not closed")
    two_full_mask = 3
    require(len(source_companion) == 5,
            "two-direction source companion term count changed")
    require(source_companion[("r_0", 0)] == h_v,
            "two-direction companion lost h_v*r_0[empty]")
    require(source_companion[("r_m", two_full_mask)]
            == TOTAL.scale(-1, TOTAL.F_PURE),
            "two-direction companion lost -(H_0-u)*r_m[ut]")
    # Target is supported only on the zero-jet r_0 row; subtracting h_v*T
    # cancels it.  The source companion is Eq-closed, while d(-h_v*T)
    # equals +h_v*Y*w.  No source row or T row carries ordinary residue.
    source_companion_target = source_companion[("r_0", 0)]
    cap_target = TOTAL.scale(-1, h_v)
    require(TOTAL.add(source_companion_target, cap_target) == {},
            "two-direction filler retained target")
    two_direction_boundary = {
        "w": TOTAL.multiply(h_v, TOTAL.CAP_Y)
    }
    require(two_direction_boundary == expected_initial_boundary,
            "two-direction filler boundary changed")

    # If this coefficient is isolated and evaluated with the original
    # underived differential, it has one extra Eq boundary.  This is the
    # earliest exact commutator.  The full translated differential cancels
    # it with lower Hasse faces.
    original_differential = {
        "r_0": {"eq": TOTAL.F_PURE},
        "r_m": {"eq": TOTAL.H_MIXED},
        "T": {"w": TOTAL.scale(-1, TOTAL.CAP_Y)},
        "rho": {"w": TOTAL.constant()},
    }
    isolated_boundary = TOTAL.apply_module_map(
        initial_chain, original_differential
    )
    residual = module_subtract(isolated_boundary, expected_initial_boundary)
    expected_residual = {
        "eq": TOTAL.multiply(h_v, TOTAL.F_PURE)
    }
    require(residual == expected_residual and residual,
            "first underived commutator is not h_v*(H_0-u)*eq")
    require(len(expected_residual["eq"]) == 273,
            "first commutator support changed")

    # The full translated generating chain has the exact augmented boundary
    # and no augmentation defects.  This is a positive filler in the
    # derived-presentation totalization.
    require(TOTAL.apply_module_map(total_chain, differential)
            == total_boundary,
            "complete translated filler lost its boundary")
    require(not TOTAL.apply_module_map(total_chain, target)
            and not TOTAL.apply_module_map(total_chain, ores),
            "complete translated filler retained an augmentation")

    # Literal chart placement on every internal face.  The source chart
    # difference has +S_v; the corrected comparison subtracts this chain,
    # hence supplies exactly the -S_v required by f872900.
    tau_hm = TOTAL.translate(TOTAL.H_MIXED, directions)
    pq_direct, pq_star = TOTAL.partition(
        TOTAL.H_MIXED, (TOTAL.P, TOTAL.QSITE)
    )
    pr_direct, pr_star = TOTAL.partition(
        TOTAL.H_MIXED, (TOTAL.P, TOTAL.R)
    )
    for subset in TOTAL.subsets(internal_eps):
        selected = (eps_u, eps_t) + subset
        expected = TOTAL.hasse_coefficient(tau_hm, selected, all_eps)
        require(TOTAL.hasse_coefficient(
            TOTAL.translate(pq_direct, directions), selected, all_eps
        ) == expected, "pq external face left direct sector")
        require(not TOTAL.hasse_coefficient(
            TOTAL.translate(pq_star, directions), selected, all_eps
        ), "pq external face entered star sector")
        require(not TOTAL.hasse_coefficient(
            TOTAL.translate(pr_direct, directions), selected, all_eps
        ), "pr external face entered direct sector")
        require(TOTAL.hasse_coefficient(
            TOTAL.translate(pr_star, directions), selected, all_eps
        ) == expected, "pr external face left two-star sector")

    chart_difference = {
        "r_0_pq": tau_hm,
        "r_m_pq": TOTAL.scale(-1, TOTAL.F_PURE),
        "r_0_pr": TOTAL.scale(-1, tau_hm),
        "r_m_pr": TOTAL.F_PURE,
    }
    chart_differential = {
        "r_0_pq": {"eq": TOTAL.F_PURE},
        "r_m_pq": {"eq": tau_hm},
        "r_0_pr": {"eq": TOTAL.F_PURE},
        "r_m_pr": {"eq": tau_hm},
    }
    chart_target = {
        "r_0_pq": {"target": TOTAL.constant()},
        "r_m_pq": {},
        "r_0_pr": {"target": TOTAL.constant()},
        "r_m_pr": {},
    }
    require(not TOTAL.apply_module_map(chart_difference, chart_differential)
            and not TOTAL.apply_module_map(chart_difference, chart_target),
            "strict chart difference is not a closed target-zero chain")
    external_chart = TOTAL.module_coefficient(
        TOTAL.module_external_face(chart_difference, (eps_u, eps_t)),
        (), internal_eps,
    )
    require(external_chart == {"r_0_pq": h_v,
                               "r_0_pr": TOTAL.scale(-1, h_v)},
            "external strict chart face is not +S_v")
    corrected_chart = TOTAL.module_scale(-1, external_chart)
    require(corrected_chart == {"r_0_pq": TOTAL.scale(-1, h_v),
                                 "r_0_pr": h_v},
            "subtracted filler is not -S_v")

    # Top q-zero face.  The full derived totalization still closes, but the
    # diagonal projection to the original source retains the monic pure Eq
    # defect.  This is the first surviving obstruction after all target,
    # ores, chart, proper-face, and denominator checks.
    top_chain = TOTAL.module_coefficient(total_chain, all_eps, all_eps)
    top_boundary = TOTAL.module_coefficient(total_boundary, all_eps, all_eps)
    require(top_chain == {"r_0": TOTAL.constant(),
                          "T": TOTAL.constant(-1)},
            "q-zero top chain changed")
    require(top_boundary == {"w": TOTAL.CAP_Y},
            "q-zero top boundary changed")
    projected_top = TOTAL.apply_module_map(top_chain, original_differential)
    top_residual = module_subtract(projected_top, top_boundary)
    require(top_residual == {"eq": TOTAL.F_PURE},
            "top physical descent commutator is not (H_0-u)*eq")

    # Re-run the complete one-cube audit to retain all fifteen denominator
    # columns and their 5,3,3,1 proper-face support in this theorem.
    complete_record = TOTAL.audit_one_cube(DELETED, matching)
    require(complete_record["target"] == 0
            and complete_record["ordinary_residue"] == 0
            and complete_record["denominator_selected_columns_by_internal_face"]
            == [5, 3, 3, 1],
            "complete denominator/augmentation audit changed")

    ledger = {
        "face": DELETED,
        "matching": [list(pair) for pair in matching],
        "sigma": {"sites": [0, 6, 7], "weight": 3, "unique": True},
        "initial_layer": {
            "chain": "h_v*(r_0-T)",
            "boundary": "h_v*Y*w",
            "target": 0,
            "ordinary_residue": 0,
            "chart_face": "+S_v",
            "corrected_subtraction": "-S_v",
            "isolated_underived_commutator": "h_v*(H_0-u)*eq",
            "commutator_terms": len(expected_residual["eq"]),
        },
        "two_direction_derived_filler": {
            "source_companion": (
                "H_m*r_0[ut]+du(H_m)*r_0[t]+dt(H_m)*r_0[u]+"
                "h_v*r_0[empty]-(H_0-u)*r_m[ut]"
            ),
            "source_companion_terms": len(source_companion),
            "source_companion_eq_boundary": 0,
            "filler": "n_v=s_ut-h_v*T",
            "boundary": "h_v*Y*w",
            "target": 0,
            "ordinary_residue": 0,
            "scope": (
                "constructs dn_v in the indexed derived presentation; "
                "does not construct db_v=k_v in the underived physical "
                "two-chart source"
            ),
        },
        "complete_derived_totalization": {
            "chain": "tau(H_m)*(r_0-T)-tau(H_0-u)*r_m",
            "boundary": "tau(H_m)*Y*w",
            "target": 0,
            "ordinary_residue": 0,
            "strict_chart_difference": "closed and invisible",
            "denominator_support_by_internal_face": [5, 3, 3, 1],
            "verdict": "positive filler in the derived-presentation complex",
        },
        "qzero_top": {
            "chain": "r_0-T",
            "boundary": "Y*w",
            "diagonal_projection_commutator": "(H_0-u)*eq",
            "underived_source_descent": False,
        },
        "first_surviving_gate": (
            "a comparison from the complete derived Hasse/Koszul "
            "totalization to the underived physical source which kills the "
            "monic (H_0-u)*eq commutator while preserving target, ordinary "
            "residue, and the -S_v chart face"
        ),
        "scope": (
            "exact h=3 one-face augmentation/chart audit; constructs the "
            "filler in the prolonged derived presentation but not in the "
            "underived physical source and does not identify the later "
            "kappa*Y*w cap landing"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode("ascii")).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_PINNED":
        require(digest == EXPECTED_DIGEST,
                f"shifted denominator augmented ledger changed: {digest}")
    return ledger, digest


def main():
    ledger, digest = audit()
    print("h=3 shifted denominator augmented chart filler: PASS (exact)")
    print("initial derived filler:       h_v*(r_0-T), tgt=ores=0")
    print("corrected chart face:         -S_v")
    print("isolated order-2 commutator:  h_v*(H_0-u)*eq")
    print("complete Hasse faces:         cancel in derived presentation")
    print("underived q-zero obstruction: (H_0-u)*eq")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
