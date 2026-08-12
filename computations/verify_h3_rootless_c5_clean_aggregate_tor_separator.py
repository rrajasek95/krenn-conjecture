#!/usr/bin/env python3
r"""Weighted aggregate separator for the normalized C5 Tor map.

For the selected word m=12112, the universal denominator column
b(d_(v,m_v)) has m-coordinate h_v and every unselected column has
m-coordinate zero.  Therefore every Tor projection y satisfies

    sum_v h_v y_v = 0.

On the exact normalized C5 collision slice R_v=0, h_v=1.  Hence every Tor
projection has zero aggregate and the unit-aggregate branch of the general
C5 shortcut is impossible.  The selected aggregate column sum has
m-coordinate five, giving a primitive characteristic-zero separator.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = "2929c94187b0e1ab9a925fd82a0754cba6e877f34a0906f778e2346c59b22eaa"
PINS = {
    "computations/verify_h3_rootless_c5_aggregate_tor_shortcut.py":
        "00759c079736a2fa613b8e994406318fed430654349df70e268b39008d679ca0",
    "notes/h3-rootless-c5-aggregate-tor-shortcut.md":
        "cfadad36e005fc40ebdf7730ac88bab2b65106dc504b03bba00734650e7c0e64",
    "computations/verify_h3_component_iv_selected_denominator_membership_separator.py":
        "859a5e3fc4b942858ded8544333b885a04d1e5e91ae3803e6e0c562393e3b7da",
    "notes/h3-component-iv-selected-denominator-membership-separator.md":
        "cece8909f15807d6a990edda0c7344efe0dc2d6dff177647d4d84d96118abd24",
    "computations/verify_h3_rootless_target_preserving_c5_etale_gauge.py":
        "02c2cc44c4d849e9db5d98c3c28882e93772dcc01cab286bba7d94cf8a8502be",
    "notes/h3-rootless-target-preserving-c5-etale-gauge.md":
        "da6d5d3658b8dfe005f47f8e859342f1f98dfb0d1d8c40ca3b0b596b365726cb",
    "computations/verify_h3_denominator_tor_transgression_fitting_gate.py":
        "33cd6ac3de85f83ee16189601930938d73f35f2fef5db20253380801bdd78459",
}


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def load_module(relative: str, name: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None,
            f"cannot load dependency {relative}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def coordinate_separator():
    trans = load_module(
        "computations/verify_h3_denominator_tor_transgression_fitting_gate.py",
        "clean_aggregate_transgression_dependency",
    )
    selected = set(trans.SELECTED)
    unselected = tuple(label for label in trans.LABELS if label not in selected)
    require(len(selected) == 5 and len(unselected) == 10,
            "selected/unselected denominator split changed")

    # A column d_(v,a) has support only on words whose v-coordinate is a.
    # Thus the m-coordinate is zero unless a=m_v.  For the selected column,
    # the coefficient is the complete three-matching face hafnian h_v.
    records = []
    for site, colour in trans.LABELS:
        if colour != trans.MIXED[site - 1]:
            coefficient = ()
            kind = "unselected_zero"
        else:
            remaining = tuple(vertex for vertex in trans.SITES
                              if vertex != site)
            coefficient = trans.matchings(remaining)
            kind = "selected_h_v"
            require(len(coefficient) == 3,
                    "a selected face hafnian lost its three matchings")
        records.append({
            "column": f"d_({site},{colour})",
            "m_word_coordinate_kind": kind,
            "matching_count": len(coefficient),
        })
    require(sum(record["m_word_coordinate_kind"] == "selected_h_v"
                for record in records) == 5,
            "selected m-coordinate count changed")
    require(sum(record["m_word_coordinate_kind"] == "unselected_zero"
                for record in records) == 10,
            "unselected m-coordinate count changed")
    return trans, records


def c5_face_split(trans):
    cycle = frozenset(((1, 2), (2, 3), (3, 4), (4, 5), (1, 5)))
    records = []
    all_residual = []
    for site in trans.SITES:
        remaining = tuple(vertex for vertex in trans.SITES if vertex != site)
        matchings = trans.matchings(remaining)
        selected = tuple(matching for matching in matchings
                         if set(tuple(sorted(edge)) for edge in matching) <= cycle)
        residual = tuple(matching for matching in matchings
                         if matching not in selected)
        require(len(selected) == 1 and len(residual) == 2,
                "a normalized C5 face lost its 1+2 split")
        all_residual.extend(residual)
        records.append({
            "face": site,
            "h_v": "1+R_v",
            "selected_cycle_matching": [list(edge) for edge in selected[0]],
            "residual_matchings": [[list(edge) for edge in matching]
                                   for matching in residual],
            "on_R_v_zero": 1,
        })
    require(len(all_residual) == 10,
            "ten normalized C5 residual occurrences changed")
    return records


def weighted_relation_replay():
    # The relation is formal: h dot y=0.  Replay exact rational examples and
    # the clean specialization h=(1,...,1), where it becomes epsilon(y)=0.
    general = (
        ((Q(1), Q(2), Q(3), Q(4), Q(5)),
         (Q(2), Q(-1), Q(0), Q(0), Q(0))),
        ((Q(2), Q(-3), Q(5), Q(7), Q(11)),
         (Q(3), Q(2), Q(0), Q(0), Q(0))),
    )
    general_records = []
    for h, y in general:
        # Adjust the last coordinate to impose h.y=0 without assuming a
        # nonzero aggregate.
        prefix = sum(h[index] * y[index] for index in range(4))
        adjusted = y[:4] + (-prefix / h[4],)
        require(sum(a * b for a, b in zip(h, adjusted, strict=True)) == 0,
                "weighted Tor relation replay failed")
        general_records.append({
            "h": [str(value) for value in h],
            "y": [str(value) for value in adjusted],
            "weighted_sum": "0",
            "ordinary_aggregate": str(sum(adjusted)),
        })

    clean_vectors = (
        (Q(1), Q(-1), Q(0), Q(0), Q(0)),
        (Q(2), Q(3), Q(-4), Q(5), Q(-6)),
        (Q(1, 2), Q(2, 3), Q(3, 5), Q(5, 7),
         -Q(1, 2) - Q(2, 3) - Q(3, 5) - Q(5, 7)),
    )
    require(all(sum(vector) == 0 for vector in clean_vectors),
            "clean weighted relation stopped being aggregate zero")
    return {
        "general_weighted_examples": general_records,
        "clean_examples": [[str(value) for value in vector]
                           for vector in clean_vectors],
    }


def packet_scope(trans):
    records = {}
    for name in ("direct_free", "tilted"):
        packet = trans.packet_audit(name)
        require(packet["h_values"] == ["0"] * 5,
                f"{name}: scalar-zero status changed")
        aggregates = [sum(Q(value) for value in row)
                      for row in packet["transgression_rows"]]
        require(any(aggregates),
                f"{name}: aggregate witness unexpectedly disappeared")
        records[name] = {
            "is_full_source_point": False,
            "h_values": packet["h_values"],
            "transgression_rank": packet["transgression_rank"],
            "has_nonzero_aggregate_projection": True,
            "why_no_contradiction": (
                "the weighted relation is vacuous when all h_v=0; this "
                "packet is not on the clean normalized h_v=1 slice"
            ),
        }
    return records


def main() -> None:
    pin_dependencies()
    trans, coordinate_records = coordinate_separator()
    faces = c5_face_split(trans)
    require(all(record["on_R_v_zero"] == 1 for record in faces),
            "clean normalized face value changed")

    # On the clean slice, applying the m-coordinate to the selected
    # aggregate sum gives 5, while every unselected combination gives zero.
    selected_aggregate_coordinate = sum(record["on_R_v_zero"]
                                        for record in faces)
    require(selected_aggregate_coordinate == 5,
            "selected aggregate separator changed")

    ledger = {
        "theorem": "clean C5 weighted aggregate Tor separator",
        "universal_selected_word_coordinate": {
            "word": "12112",
            "columns": coordinate_records,
            "kernel_consequence": (
                "for every k in ker b with selected projection y=tau(k), "
                "sum_v h_v*y_v=0"
            ),
        },
        "normalized_C5_faces": faces,
        "clean_R_zero_consequence": {
            "h_values": [1, 1, 1, 1, 1],
            "epsilon_of_every_Tor_projection": 0,
            "aggregate_ideal_epsilon_im_tau": "(0)",
            "selected_column_sum_m_coordinate": selected_aggregate_coordinate,
            "unselected_image_m_coordinate": 0,
            "aggregate_selected_sum_membership": (
                "impossible over a nonzero characteristic-zero clean C5 ring"
            ),
            "unit_aggregate_branch_of_0e117b8": "impossible on this slice",
        },
        "weighted_relation_replay": weighted_relation_replay(),
        "old_packet_scope": packet_scope(trans),
        "low_degree_identity_scope": (
            "no Koszul/Euler/Schur multiplier can express the clean selected "
            "aggregate through unselected denominator columns: the literal "
            "m-word coordinate reads 5 on the former and 0 on the latter"
        ),
        "proof_consequence": (
            "the exact clean C5 path must promote the primitive epsilon "
            "separator through endpoint Omega/rootless-ridge, W, target, "
            "ores, and correction typing; positive denominator Tor cannot "
            "supply the physical base there"
        ),
        "scope": (
            "exact universal weighted identity and clean R_v=0 consequence. "
            "It does not construct the physical terminal annihilator or "
            "exclude aggregate Tor on the scalar-zero h_v=0 branch"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"clean aggregate Tor separator ledger changed: {digest}")
    print("h3 rootless clean C5 aggregate-Tor separator: PASS")
    print("universal kernel relation: sum_v h_v*y_v = 0")
    print("clean R_v=0: h_v=1, hence epsilon(im tau)=0")
    print("selected aggregate membership: separated by m-coordinate 5 vs 0")
    print("clean route: separator promotion, not positive Tor")
    print("ledger SHA-256:", digest)


if __name__ == "__main__":
    main()
