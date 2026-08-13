#!/usr/bin/env python3
"""Identify the last C-plus W law with the old physical Yw/W cap law.

The conditional C-plus core records the net P2 target/Eq packet

    (Eq,target)=(-E,-E),  E=2 D_root tensor (B1+B4)/2.

The complete Hasse top contains the literal physical cap

    B_E=(r0-T)_E,  (Eq,Yw,W,target)=(E,E,E,0).

Extracting it leaves a Yw/W-dark Cartan/Spencer remainder with
(Eq,target)=(-2E,-E).  The target path T_E has
(Yw,W,target)=(-E,-E,E), and the clean K_Eq face has Eq=E.  Hence

    T_E + B_E + C_E + K_Eq = 0

simultaneously in Eq, derived Yw, physical W, and target.  Thus the last W
equation is exactly the already isolated map Yw_E -> W_E furnished by
r0-T; it is not a fourth source-generator type.  A projected theorem which
forgets W remains insufficient, detected by the primitive W-Yw covector.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_cplus_conditional_physical_dressing_assembly.py":
        "e8014fdfd2263a8eb6bffff11e31c339b5b7965989a61324f8d118a91f791f46",
    "computations/verify_h3_cplus_q_ridge_w_terminal_reduction.py":
        "b2ace6e49aa5ec1b8347a0e88cc39f36e5d773e1aab1d82f424533de8ce52a9a",
    "computations/verify_h3_interface_iii_augmented_cap_factorization.py":
        "06e64c5db2a59b8877cb112515d50779be95010801f19690f97060bf08621213",
    "computations/verify_h3_reduced_eq_full_physical_augmentation_matrix.py":
        "f66752bd3a44a9506b4a31467ce52dcb16e52f841b0f29ce66066a38ec7f97c1",
    "computations/verify_h3_full_hasse_koszul_cap_totalization.py":
        "51940ce0ac8387b68e7725508db6da1a1c055ea036335bbf19750580c69e13fb",
    "computations/verify_h3_component_iv_weighted_normal_hasse_companions.py":
        "f94b13e3d08d0f090112648f0b7a1d9b7d07ce857d6b5d979d730dc4761a8ce0",
    "computations/verify_h2_lower_even_cartan_jstar_target_cone_gate.py":
        "09ba792f229bb3a1e930b2c59b0de2356b08a7434c648aad9573d8382c652a52",
}
EXPECTED_LEDGER_SHA256 = (
    "5d8ecff55e53cfb0430bcbc0784f981c2bef1efea1d350e3455df5ee40170b1e"
)

ROOT_WORDS = 4
LABELS = 6
WIDTH = ROOT_WORDS * LABELS
D_ROOT = tuple(map(Q, (-1, 1, -1, 1)))
V = tuple(map(Q, (0, Q(1, 2), 0, 0, Q(1, 2), 0)))
E = tuple(2 * root * label for root in D_ROOT for label in V)

EQ = slice(0, WIDTH)
YW = slice(EQ.stop, EQ.stop + WIDTH)
W = slice(YW.stop, YW.stop + WIDTH)
TARGET = slice(W.stop, W.stop + WIDTH)
AINC = TARGET.stop
ROWS = AINC + 1


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


def add(*vectors):
    return tuple(sum(entries, Q(0)) for entries in zip(*vectors, strict=True))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(entry) for entry in vector)


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


def vector(*, eq=(), yw=(), w=(), target=(), ainc=0):
    answer = [Q(0)] * ROWS
    for section, values in ((EQ, eq), (YW, yw), (W, w), (TARGET, target)):
        if values:
            require(len(values) == WIDTH, (section, len(values)))
            answer[section] = values
    answer[AINC] = Q(ainc)
    return tuple(answer)


def root_even_cap_table() -> dict[str, object]:
    zero = (Q(0),) * WIDTH
    require(len(E) == WIDTH and sum(E, Q(0)) == 0
            and sum(value != 0 for value in E) == 8,
            "the root-even E packet changed")

    # Literal cap T and its target-zero physical top B=r0-T.  The anchor of
    # B_E is -sum(E)=0, so root decoration introduces no hidden anchor debt.
    target_path = vector(yw=scale(-1, E), w=scale(-1, E), target=E)
    cap_top = vector(eq=E, yw=E, w=E, ainc=-sum(E, Q(0)))

    # The conditional core gives the net P2 packet (Eq,target)=(-E,-E).
    # Therefore, after extracting its literal B_E top, the remaining
    # Cartan/Spencer part has (-2E,-E) and is dark in Yw/W.
    cartan_remainder = vector(eq=scale(-2, E), target=scale(-1, E))
    p2_total = add(cap_top, cartan_remainder)
    expected_p2 = vector(eq=scale(-1, E), yw=E, w=E,
                         target=scale(-1, E))
    require(p2_total == expected_p2,
            "the cap extraction stopped reconstructing the P2 packet")

    clean_k_eq = vector(eq=E)
    require(add(target_path, p2_total, clean_k_eq) == vector(),
            "the completed target/Eq/Yw/W square stopped closing")
    require(target_path[YW] == target_path[W] == scale(-1, E)
            and cap_top[YW] == cap_top[W] == E,
            "the cap law stopped being coefficientwise Yw=W")

    return {
        "E": "2 D_root tensor (B1+B4)/2",
        "E_nonzero_root_labels": sum(value != 0 for value in E),
        "E_augmentation": str(sum(E, Q(0))),
        "table": {
            "T_E": {"Eq": "0", "Yw": "-E", "W": "-E",
                    "target": "+E"},
            "B_E=(r0-T)_E": {"Eq": "+E", "Yw": "+E", "W": "+E",
                              "target": "0", "ainc": "-sum(E)=0"},
            "Cartan_Spencer_remainder": {
                "Eq": "-2E", "Yw": "0", "W": "0", "target": "-E"
            },
            "clean_K_Eq": {"Eq": "+E", "Yw": "0", "W": "0",
                            "target": "0"},
        },
        "sum_Eq_Yw_W_target_ainc": 0,
        "P2_net": {"Eq": "-E", "Yw": "+E", "W": "+E",
                   "target": "-E"},
        "physical_W_map_needed": "Phi_cap(Yw_E)=W_E (identity on E-line)",
    }


def literal_source_and_jet_audit() -> dict[str, object]:
    # Re-run the committed physical factorization, including its normal jets.
    interface = load(
        "computations/verify_h3_interface_iii_augmented_cap_factorization.py",
        "cplus_w_interface_iii",
    )
    old_cap, repairs, physical = interface.base_factorization()
    require(old_cap[interface.ROWS.index("Yw_boundary")]
            == old_cap[interface.ROWS.index("W")] == 1,
            "the literal r0-T cap stopped realizing Yw=W=1")
    require(all(repair[interface.ROWS.index("Yw_boundary")] == 0
                and repair[interface.ROWS.index("W")] == 0
                for repair in repairs),
            "an Interface-III repair acquired a Yw/W face")
    require(all(column[interface.ROWS.index("Yw_boundary")]
                == column[interface.ROWS.index("W")] == 1
                for column in physical),
            "the completed physical columns lost Yw/W equality")
    jets = interface.jet_factorization()
    require(len(jets) == 4
            and all(record["Yw_boundary_equals_W_gradewise"]
                    and not record["new_cap_generator_type"]
                    for record in jets),
            "normal/Rees prolongation stopped preserving the cap law")

    # Pin the literal full Hasse fact which supplies the source provenance:
    # the top coefficient is r0-T and its diagonal boundary is Eq+Yw.
    full = (ROOT / (
        "computations/verify_h3_full_hasse_koszul_cap_totalization.py"
    )).read_text()
    require('"r_0": constant(), "T": constant(-ONE)' in full
            and '== {"eq": F_PURE, "w": CAP_Y}' in full,
            "the full-Hasse r0-T top/boundary changed")

    return {
        "literal_source_top": "r0-T in every one of the 15 full Hasse cubes",
        "diagonal_boundary_before_KEq": "(H0-u)e_Eq+Yw",
        "pointed_KEq_role": "remove the Eq face without changing Yw or W",
        "physical_cap_readout": "Yw=W=1 on r0-T",
        "normal_Rees_orders_checked": [record["normal_order"]
                                        for record in jets],
        "normal_jet_law": "Yw_k=W_k coefficientwise/convolutionwise",
        "fourth_source_generator_needed_for_W": False,
    }


def sharp_dual_audit() -> dict[str, object]:
    # Forgetting physical W permits a mutation which keeps Eq, Yw, target,
    # anchor, and every already assembled core row but changes W(B_E) from E
    # to zero.  The final total then has W=-E.  W-Yw detects the failure on
    # the cap column while killing every correctly typed cap column.
    target_path = vector(yw=scale(-1, E), w=scale(-1, E), target=E)
    good_cap = vector(eq=E, yw=E, w=E)
    bad_cap = vector(eq=E, yw=E, w=(Q(0),) * WIDTH)
    repair = vector(eq=scale(-2, E), target=scale(-1, E))
    k_eq = vector(eq=E)
    keep = tuple(index for index in range(ROWS)
                 if not (W.start <= index < W.stop))
    require(tuple(good_cap[index] for index in keep)
            == tuple(bad_cap[index] for index in keep),
            "the W mutation changed a projected row")
    good_total = add(target_path, good_cap, repair, k_eq)
    bad_total = add(target_path, bad_cap, repair, k_eq)
    require(good_total == vector()
            and bad_total[W] == scale(-1, E)
            and all(bad_total[index] == 0 for index in keep),
            "the final W-only mutation guard changed")

    nonzero = next(index for index, value in enumerate(E) if value)
    e_dual = [Q(0)] * WIDTH
    e_dual[nonzero] = Q(1) / E[nonzero]
    e_dual = tuple(e_dual)
    cap_covector = vector(yw=scale(-1, e_dual), w=e_dual)
    require(dot(cap_covector, good_cap) == 0
            and dot(cap_covector, bad_cap) == -1,
            "the primitive W-Yw cap dual changed")
    final_w_covector = vector(w=e_dual)
    require(dot(final_w_covector, good_total) == 0
            and dot(final_w_covector, bad_total) == -1,
            "the final W scalar dual changed")
    return {
        "hidden_mutation": "keep Yw(B_E)=E but set physical W(B_E)=0",
        "all_nonW_rows_unchanged": True,
        "bad_final_only_debt": "W=-E",
        "primitive_comparison_dual": "one E-coordinate of W-Yw",
        "primitive_final_dual": "the same E-coordinate of W",
        "dual_values_good_bad": [0, -1],
        "consequence": (
            "a theorem projected away from physical W cannot prove the final "
            "C-plus compatibility; columnwise Yw/W typing is load-bearing"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    ledger = {
        "theorem": "final C-plus W is the old derived-Yw/physical-W cap law",
        "pins": PINS,
        "root_even_factorization": root_even_cap_table(),
        "literal_and_normal_source_provenance": literal_source_and_jet_audit(),
        "projection_counterguard": sharp_dual_audit(),
        "conclusion": (
            "After the P2/pointed-KEq/d_even main assembly, no independent W "
            "generator remains.  The literal Hasse top r0-T supplies the "
            "identity Yw_E->W_E and the Yw/W-dark repair supplies the other "
            "rows.  This closes W conditionally on a fully augmented "
            "source-labelled P2/KEq comparison; if W is omitted from that "
            "comparison, W-Yw is the sharp primitive dual."
        ),
        "scope": (
            "generic h3 root-even C-plus and normal/Rees orders zero through "
            "three; no construction of P2, d_even, pointed K_Eq, its labelled "
            "ridge, or beta-zero D0"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("h3 final C-plus W: SAME Yw/W CAP LAW")
    print("physical map: Yw_E -> W_E via (r0-T)_E")
    print("normal/Rees orders 0..3: equality preserved")
    print("projected-away-W guard: primitive W-Yw dual survives")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
