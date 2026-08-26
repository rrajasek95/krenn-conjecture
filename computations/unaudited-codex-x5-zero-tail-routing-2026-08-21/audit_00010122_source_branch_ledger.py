#!/usr/bin/env python3
"""Exact source-faithful branch ledger for the 00010122 tail row.

The normalized row is Q_0[0124] X_1[35], since X_2[67] is an anchor.
This audit records the disjoint product-zero split, checks which purported
cofactor consequences are actually available on each branch, and guards the
scope of the existing fixed-left mate certificates.  It does not run a
Groebner basis: neither branch fixes a finite left (X,C,Q,H) signature.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
EXTENSION_SCRIPT = HERE / "audit_440_2110_extension.py"
ORBIT_SCRIPT = HERE / "audit_422_nonpairconstant_extension.py"
ROUTING = HERE / "results_x5_zero_tail_routing.json"
SUPPORT_LEDGER = (ROOT / "computations" /
    "unaudited-codex-tail-polar-source-lift-2026-08-21" /
    "audit_tail_support_boundary_orbits.py")
SUPPORT6 = (ROOT / "computations" /
    "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20" /
    "results_support6_component_pairwise_obstruction.json")
SUPPORT6_UNIT = (ROOT / "computations" /
    "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20" /
    "results_support6_fixed_left_partner_certificate_audit.json")
SUPPORT8_UNIT = (ROOT / "computations" /
    "unaudited-codex-orbit0-t2-radical-2026-08-20" /
    "results_forced_one_y_mate_unit_identity.json")
AB_UNIT = (ROOT / "computations" /
    "unaudited-codex-generic-cycle-mate-incidence-2026-08-21" /
    "results_AB_component_weak_mate_exact_audit.json")
OUT = HERE / "results_00010122_source_branch_ledger.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    require(spec.loader is not None, f"missing loader for {path}")
    spec.loader.exec_module(module)
    return module


EXT = load("x5_00010122_extension", EXTENSION_SCRIPT)
ORB = load("x5_00010122_orbit", ORBIT_SCRIPT)
TAIL = load("x5_00010122_support", SUPPORT_LEDGER)
CORE = EXT.CORE


def file_sha(path):
    return sha256(path.read_bytes()).hexdigest()


def logical_sha(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def normalized_edge(u, v):
    """Physical edge after setting each of the four anchors equal to one."""
    require(u != v, "loops are not graph edges")
    if u > v:
        u, v = v, u
    super_u, clone_u = divmod(u, 2)
    super_v, clone_v = divmod(v, 2)
    if super_u == super_v:
        require(clone_u != clone_v, "repeated physical vertex")
        return CORE.ONE
    return CORE.entry(super_u, super_v, clone_u, clone_v)


def hafnian_subset(vertices):
    answer = Counter()
    for matching in CORE.perfect_matchings(tuple(vertices)):
        answer = EXT.add(answer, EXT.multiply(*(
            normalized_edge(u, v) for u, v in matching)))
    return answer


def serialize(poly, offset=0):
    return [{
        "coefficient": coefficient,
        "variables": [EXT.variable_name(index + offset)
                      for index in monomial],
    } for monomial, coefficient in sorted(poly.items())]


def main():
    routing = json.loads(ROUTING.read_text())
    route = next(row for row in routing["routing_table"]
                 if row["canonical_word"] == "00010122")
    actions = ORB.vertex_actions()
    orbit = ORB.word_orbit("00010122", actions)
    require(len(actions) == 384 and len(orbit) == 288,
            "B4 x S3 orbit size changed")
    require(orbit == frozenset(route["literal_source_labels"]),
            "literal 00010122 orbit transport changed")

    q0124 = hafnian_subset((0, 1, 2, 4))
    expected_q = EXT.add(CORE.variable(1, 2, 0, 0),
                         EXT.multiply(CORE.variable(0, 1, 0, 0),
                                      CORE.variable(0, 2, 1, 0)),
                         EXT.multiply(CORE.variable(0, 2, 0, 0),
                                      CORE.variable(0, 1, 1, 0)))
    require(q0124 == expected_q and len(q0124) == 3,
            "literal Q[0124] expansion changed")
    x35 = normalized_edge(3, 5)
    require(x35 == CORE.variable(1, 2, 1, 1),
            "X[35] is no longer raw cell 15")
    canonical = EXT.word_poly("00010122", colours=3)
    require(canonical == EXT.multiply(q0124, EXT.shift(x35, 24)),
            "normalized 00010122 factorization changed")

    raw_h = CORE.pure_hafnian()
    c35 = EXT.derivative(raw_h, 15)
    anchor_checks = []
    anchors = ((0, 1), (2, 3), (4, 5), (6, 7))
    for anchor_index, anchor in enumerate(anchors):
        complement = tuple(v for v in range(8) if v not in anchor)
        remaining_supervertices = tuple(i for i in range(4)
                                        if i != anchor_index)
        cofactor = hafnian_subset(complement)
        triangle = CORE.t_triple(*remaining_supervertices)
        require(cofactor == triangle,
                f"anchor cofactor C{anchor} ceased to equal a t row")
        anchor_checks.append({
            "anchor": list(anchor),
            "equals_reduced_triangle": "t_" + "".join(
                map(str, remaining_supervertices)),
        })

    # The permanent/triangle support face is large even before coefficient
    # constraints are considered.  This is a guard against treating X15=0
    # as a finite fixed-left signature.
    _accepted, minima = TAIL.cross_supports()
    entry_zero_minima = tuple(mask for mask in minima
                              if not ((mask >> 15) & 1))
    entry_live_minima = tuple(mask for mask in minima
                              if (mask >> 15) & 1)
    require((len(minima), len(entry_zero_minima), len(entry_live_minima)) ==
            (1224, 504, 720), "entry-15 support-face census changed")

    support6 = json.loads(SUPPORT6.read_text())
    support6_unit = json.loads(SUPPORT6_UNIT.read_text())
    support8_unit = json.loads(SUPPORT8_UNIT.read_text())
    ab_unit = json.loads(AB_UNIT.read_text())
    support6_x = frozenset(support6["x_support"])
    support6_c = frozenset(support6["cofactor_support"])
    support6_q = frozenset(support6["q_support"])
    support8_left = support8_unit["fixed_left"]
    require(15 not in support6_x and 15 not in
            set(support8_left["entry_live_cells"]),
            "known entry-zero controls changed")
    require((len(support6_x), len(support6_c), len(support6_q)) == (12, 4, 6)
            and (len(support8_left["entry_live_cells"]),
                 len(support8_left["cofactor_live_cells"]),
                 len(support8_left["Q_support"])) == (18, 8, 8),
            "known distinct fixed-left signatures changed")

    result = {
        "status": "PASS exact source-faithful 00010122 branch ledger",
        "canonical_row": {
            "source_label": "00010122",
            "normalized_factorization": "Q_0[0124]*X_1[35]",
            "anchor_factor": "X_2[67]=1",
            "Q_0_0124": serialize(q0124),
            "X_1_35_raw_cell": 15,
            "expanded_sha256": EXT.poly_sha(canonical),
        },
        "anchor_cofactor_redundancy": {
            "checks": anchor_checks,
            "consequence": (
                "C_0[67]=C_1[67]=0 are already copies of the base "
                "reduced-triangle row t_012; they do not refine either "
                "branch signature."),
        },
        "source_faithful_disjoint_antichain": [
            {
                "name": "A_entry_zero",
                "equations_added_to_full_packet": ["X_1[35]=0"],
                "redundant_rows": ["C_0[67]=t^0_012=0",
                                   "C_1[67]=t^1_012=0"],
                "not_forced": ["C_0[35]=0", "C_2[35]=0",
                               "Q_0[0124]=0"],
                "minimal_ideal_interface": {
                    "ordinary_packet": (
                        "three diagonal e/t packets, both directional X*C "
                        "packets, and full 440 for all three colour pairs"),
                    "extra_generator": "x1_15",
                    "localizers": ["H_0", "H_1", "H_2"],
                },
            },
            {
                "name": "B_entry_live_Q_zero",
                "equations_added_to_full_packet": [
                    "Q_0[0124]=0", "C_0[35]=0", "C_2[35]=0"],
                "localizer_added": "X_1[35]!=0",
                "rabinowitsch_row": "u*X_1[35]-1",
                "redundant_rows": ["C_0[67]=t^0_012=0",
                                   "C_1[67]=t^1_012=0"],
                "minimal_ideal_interface": {
                    "ordinary_packet": (
                        "three diagonal e/t packets, both directional X*C "
                        "packets, and full 440 for all three colour pairs"),
                    "extra_generators": ["Q0_0124", "C0_15", "C2_15",
                                         "u*x1_15-1"],
                    "Q0_0124_polynomial": serialize(q0124),
                    "C_15_polynomial": serialize(c35),
                    "localizers": ["H_0", "H_1", "H_2", "X_1[35]"],
                },
            },
        ],
        "support_face_census": {
            "one_colour_inclusion_minimal_e_t_supports": len(minima),
            "with_X_35_zero": len(entry_zero_minima),
            "with_X_35_live": len(entry_live_minima),
            "meaning": (
                "Already at exact support level, neither branch selects a "
                "finite joint (X,C,Q,H) signature."),
        },
        "existing_certificate_matching": {
            "support6": {
                "certificate_sha256": support6_unit["result_sha256"],
                "canonical_signature_sizes_X_C_Q": [12, 4, 6],
                "relation_to_branches": (
                    "The canonical support6 point lies on X[35]=0, but the "
                    "whole A branch is not its 24-record joint orbit. Exact "
                    "orbit matches remain terminal subloci only."),
            },
            "support8_one_y": {
                "certificate_sha256": support8_unit["result_sha256"],
                "canonical_signature_sizes_X_C_Q": [18, 8, 8],
                "relation_to_branches": (
                    "The canonical one-y point also lies on X[35]=0, with a "
                    "different full signature. Exact orbit matches remain "
                    "terminal subloci only."),
            },
            "AB_generic_cycle_component": {
                "certificate_sha256": ab_unit["result_sha256"],
                "relation_to_branches": (
                    "The unit is component-wide only after the exact A=B "
                    "generic-cycle component equations and live chart are "
                    "proved. Neither partial branch implies that component."),
            },
            "unconditional_literal_match": False,
        },
        "solve_decision": {
            "tiny_fixed_left_gate_run": False,
            "reason": (
                "No finite fixed-left signature is forced: branch A contains "
                "504 minimal e/t support records and branch B contains 720 "
                "before its coefficient equations. A coefficient solve here "
                "would be a broad 72-variable component classification, "
                "outside the requested tiny-gate rule."),
            "next_missing_machinery": (
                "An exact one-colour component/radical routing theorem for "
                "X[35]=0 and for the localized face "
                "Q[0124]=C[35]=0, followed by literal signature matching."),
        },
        "B4_times_S3_transport": {
            "group_order": 384 * 6,
            "canonical_orbit_size": len(orbit),
            "literal_labels_equal_computed_orbit": True,
            "coverage": (
                "Transport the disjoint factor split and all colour/physical "
                "indices along each of the 288 literal source labels."),
        },
        "scope_guard": (
            "Product-zero is used only as the union X_1[35]=0 or, on its "
            "complement, Q_0[0124]=0. Off-diagonal cofactor zeros are inferred "
            "only on the live-entry branch. No partial support data are "
            "promoted to a support6, support8, or A=B component signature."),
        "source_hashes": {str(path.relative_to(ROOT)): file_sha(path)
                          for path in (EXTENSION_SCRIPT, ORBIT_SCRIPT, ROUTING,
                                       SUPPORT_LEDGER, SUPPORT6, SUPPORT6_UNIT,
                                       SUPPORT8_UNIT, AB_UNIT)},
    }
    result["logical_sha256"] = logical_sha(result)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if "--write-results" in sys.argv:
        OUT.write_text(text)
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
