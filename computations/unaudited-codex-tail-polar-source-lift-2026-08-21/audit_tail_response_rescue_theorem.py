#!/usr/bin/env python3
"""Finite exact tail-response theorem and remaining divisor antichain."""

import argparse
from collections import Counter
from hashlib import sha256
import importlib.util
from itertools import permutations, product
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "results_tail_polar_source_lift.json"
FROZEN = HERE / "results_611_71_sdr_and_332_rescue.json"
COVER = HERE / "results_332_rescue_orbit_cover.json"
TWO = HERE / "results_332_two_rescue_thetas.json"
LARGER = HERE / "results_332_larger_rescue_thetas.json"
OUT = HERE / "results_tail_response_rescue_theorem.json"
COVER_SCRIPT = HERE / "audit_332_rescue_orbit_cover.py"
SUPPORT6 = (HERE.parent /
    "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20" /
    "results_support6_forced_mate_compact_identity.json")
SUPPORT6_CERT = (HERE.parent /
    "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20" /
    "results_support6_component_pairwise_obstruction.json")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    if spec.loader is None:
        raise RuntimeError("missing module loader")
    spec.loader.exec_module(module)
    return module


COVARIANCE = load("tail_response_covariance_core", COVER_SCRIPT)


def require(value, detail):
    if not value:
        raise RuntimeError(detail)


def logical_hash(value):
    return sha256(json.dumps(value, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def doubled_sites(columns):
    names = set(columns)
    return tuple(site for site in range(6)
                 if f"y{site}" in names and f"z{site}" in names)


def block_shape(sites):
    counts = Counter(site//2 for site in sites)
    return tuple(sorted((counts.get(block, 0) for block in range(3)),
                        reverse=True))


def site_image_set(sites, action):
    return frozenset(action[site] for site in sites)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    source = json.loads(SOURCE.read_text())
    frozen = json.loads(FROZEN.read_text())
    cover = json.loads(COVER.read_text())
    two = json.loads(TWO.read_text())
    larger = json.loads(LARGER.read_text())
    support6 = json.loads(SUPPORT6.read_text())
    support6_cert = json.loads(SUPPORT6_CERT.read_text())
    require(frozen["logical_sha256"] ==
            "6d55fe4a761cc60665268e1ebfa61215390b6994134749b7fa6fe5610f2b4ad2",
            "frozen Hall/rescue theorem changed")
    require(cover["logical_sha256"] ==
            "797afdda14adb6557807b95990d165309fbd569a8a9e863e7f4edb79ee1b9edb",
            "orbit coverage digest changed")
    require(two["logical_sha256"] ==
            "dd662ba48005cb31f323f92a9eafe32beeda594f6a4381747339c8264b2a52f4",
            "two-rescue digest changed")
    require(larger["logical_sha256"] ==
            "c68081d41b2d12348f72c94adbef01e30196aefe6f1aa2688cb4b3aa2368ab3b",
            "larger-rescue digest changed")

    actions = list(COVARIANCE.vertex_actions())
    rows = {row["source_label"]: row for row in source["row_ledger"]}
    determinant_by_name = {
        record["name"]: record
        for record in two["determinants"]+larger["determinants"]
    }
    canonical_sites = {
        (2, 0, 0): (0, 1), (1, 1, 0): (0, 2),
        (2, 1, 0): (0, 1, 2), (1, 1, 1): (0, 2, 4),
        (2, 2, 0): (0, 1, 2, 3), (2, 1, 1): (0, 1, 2, 4),
        (2, 2, 1): (0, 1, 2, 3, 4),
        (2, 2, 2): (0, 1, 2, 3, 4, 5),
    }
    certificate_for_shape = {
        (2, 0, 0): "M_adj", (1, 1, 0): "M_sep",
        (2, 1, 0): "Hall_adjacent_triple",
        (1, 1, 1): "Hall_separated_triple",
        (2, 2, 0): "Theta_220", (2, 1, 1): "Theta_211",
        (2, 2, 1): "Theta_221", (2, 2, 2): "Theta_222",
    }
    divisors_for_shape = {
        (2, 0, 0): ["support_monomial"],
        (1, 1, 0): ["support_monomial"],
        (2, 1, 0): ["support_monomial", "Delta_sep"],
        (1, 1, 1): ["support_monomial", "Delta_sep"],
        (2, 2, 0): ["support_monomial", "Delta_sep"],
        (2, 1, 1): ["support_monomial", "Delta_sep"],
        (2, 2, 1): ["support_monomial", "Delta_sep", "Lambda_UV_sep"],
        (2, 2, 2): ["support_monomial", "Delta_sep", "Omega_015"],
    }

    theorem_rows = []
    counts = Counter()
    for record in frozen["orbit_ledger"]:
        status = record["status"]
        if status == "full_SDR":
            certificate = "611+71_SDR"
            divisors = ["displayed_channel_cofactor"]
            witness = None
        else:
            sites = doubled_sites(record["representative_columns"])
            shape = block_shape(sites)
            certificate = certificate_for_shape[shape]
            divisors = divisors_for_shape[shape]
            canonical = canonical_sites[shape]
            witnesses = [action for action in actions
                         if site_image_set(canonical, action) == frozenset(sites)]
            require(witnesses, ("missing determinant transport", shape, sites))
            witness = [witnesses[0][vertex] for vertex in range(8)]
        theorem_rows.append({
            "representative_mask": record["representative_mask"],
            "fixed_tail_orbit_size": record["orbit_size"],
            "status": status,
            "double_sites": record["double_sites"],
            "single_sites": record["single_sites"],
            "certificate": certificate,
            "principal_open_factors": divisors,
            "transport_vertex_map": witness,
        })
        counts[certificate] += 1
    require(len(theorem_rows) == 126 and counts == {
        "611+71_SDR": 66, "M_adj": 13, "M_sep": 20,
        "Hall_adjacent_triple": 10, "Hall_separated_triple": 6,
        "Theta_220": 4, "Theta_211": 4,
        "Theta_221": 2, "Theta_222": 1,
    }, ("terminal coverage census changed", counts))

    # Every selected larger source row lies in the two coefficient-level
    # seed orbits already replayed under all 96 actions.
    transported_labels = set()
    for seed in COVARIANCE.SEED_ROWS:
        for action in actions:
            transported_labels.add(COVARIANCE.transform_label(seed, action))
    selected_labels = {
        label for record in determinant_by_name.values()
        for label in record["source_labels"]
    }
    require(selected_labels <= transported_labels and
            all(rows[label]["profile"] == "3+3+2"
                for label in selected_labels),
            "selected Theta rows left the audited transport orbits")

    divisor_antichain = [
        {
            "factor_family": "support_monomial",
            "factor_orbit_count": 4,
            "factor_suborbits": [
                {"name": "h_residual_tail", "labelled_count_with_colours": 36},
                {"name": "g_residual_same_block", "labelled_count_with_colours": 9},
                {"name": "g_residual_distinct_blocks", "labelled_count_with_colours": 36},
                {"name": "g_residual_tail", "labelled_count_with_colours": 36},
            ],
            "representatives": [
                "h^c_at", "g^c_ab(same residual block)",
                "g^c_ab(distinct residual blocks)", "g^c_at(residual-tail)"],
            "route": "smaller_cofactor_or_edge_support_chart",
            "route_kind": "existing_support_clause_when_signature_matches",
            "terminal_existing_units": {
                "support6_arbitrary_mate":
                    support6_cert["result_sha256"],
                "support8_forced_mate": support6["result_sha256"],
            },
            "guard": (
                "Existing units fire only after the resulting joint support "
                "signature is exactly matched; no generic support boundary "
                "is declared closed merely by containment."),
        },
        {
            "factor_family": "Delta_sep",
            "factor_orbit_count": 1,
            "representative": "P_a*Q_b*V_a*U_b-P_b*Q_a*U_a*V_b",
            "route": "next_exact_determinantal_divisor",
            "route_kind": "genuinely_new_coefficient_boundary",
        },
        {
            "factor_family": "Lambda_UV_sep",
            "factor_orbit_count": 1,
            "representative": "U_a*V_b-U_b*V_a",
            "route": "next_exact_determinantal_divisor_after_Theta_221",
            "route_kind": "genuinely_new_coefficient_boundary",
        },
        {
            "factor_family": "Omega_015",
            "factor_orbit_count": 1,
            "representative": (
                "the frozen seven-term primitive in Theta_222 after "
                "removing its monomial and Delta_23 factors"),
            "route": "next_exact_determinantal_divisor_after_Theta_222",
            "route_kind": "genuinely_new_coefficient_boundary",
        },
    ]
    require(sum(row["factor_orbit_count"] for row in divisor_antichain) == 7,
            "recursive factor-orbit antichain count changed")

    result = {
        "status": "PASS finite exact tail-response rescue theorem",
        "tail_missing_pattern_orbits": 126,
        "generic_principal_open_coverage": {
            "SDR": 66, "Delta_layer": 33, "Hall_d3": 16,
            "Hall_d4": 8, "Hall_d5": 2, "Hall_d6": 1,
            "total": 126,
        },
        "certificate_orbit_counts": dict(sorted(counts.items())),
        "orbit_coverage": theorem_rows,
        "symmetry_transport": {
            "fixed_tail_group_order": len(actions),
            "literal_coefficient_transport": True,
            "transported_332_row_count": len(transported_labels),
            "selected_Theta_rows_in_transported_orbits": True,
        },
        "exact_factor_profiles": {
            "Theta_220": determinant_by_name["Theta_220"]["factorization"],
            "Theta_211": determinant_by_name["Theta_211"]["factorization"],
            "Theta_221": "support_monomial*Delta_23*Lambda_UV_04",
            "Theta_222": "support_monomial*Delta_23*Omega_015",
        },
        "remaining_finite_divisor_antichain": divisor_antichain,
        "remaining_factor_orbit_count": sum(
            row["factor_orbit_count"] for row in divisor_antichain),
        "tail_response_lemma": (
            "For every fixed-tail missing pattern, the literal 611, 71, "
            "and transported 332 source rows have full missing-column rank "
            "on one of the finitely displayed principal opens. The only "
            "remaining recursion is the four-family divisor antichain "
            "support/Delta/Lambda/Omega; no sampled rank screen is used."
        ),
        "X4_to_cap_use": (
            "On any diagonal chart avoiding the finite divisor antichain, "
            "the lowest crossing-tail layer is in the literal source ideal. "
            "This supplies the tail-response no-good/induction step; the "
            "listed divisors are the exact boundary obligations."
        ),
        "scope_guard": (
            "This is generic principal-open coverage plus an exact finite "
            "boundary recursion, not unconditional closure of the divisor "
            "antichain. Arbitrary-mate units are invoked only on exact "
            "matching support signatures."
        ),
        "source_hashes": {
            "source": sha256(SOURCE.read_bytes()).hexdigest(),
            "frozen": sha256(FROZEN.read_bytes()).hexdigest(),
            "cover": sha256(COVER.read_bytes()).hexdigest(),
            "two": sha256(TWO.read_bytes()).hexdigest(),
            "larger": sha256(LARGER.read_bytes()).hexdigest(),
            "support6": sha256(SUPPORT6.read_bytes()).hexdigest(),
            "support6_certificate": sha256(SUPPORT6_CERT.read_bytes()).hexdigest(),
        },
    }
    result["logical_sha256"] = logical_hash(result)
    if args.write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("tail response rescue theorem: PASS", result["logical_sha256"])
    print("coverage", result["generic_principal_open_coverage"])
    print("divisor antichain", [row["factor_family"]
                                for row in divisor_antichain])


if __name__ == "__main__":
    main()
