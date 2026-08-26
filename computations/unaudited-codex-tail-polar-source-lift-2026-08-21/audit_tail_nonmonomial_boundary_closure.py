#!/usr/bin/env python3
"""Close the Delta/Lambda/Omega tail boundaries by literal source minors.

The earlier tail-response theorem chose every maximal minor to contain both
7+1 channel rows.  That choice creates Delta, and its particular d=5/6 row
extensions create Lambda/Omega.  Here we also allow one channel row, or no
channel row, and use one or two additional literal 3+3+2 source rows.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "results_tail_polar_source_lift.json"
OLD_THEOREM = HERE / "results_tail_response_rescue_theorem.json"
CORE_PATH = HERE / "audit_332_two_rescue_thetas.py"
ORBIT_PATH = HERE / "audit_332_rescue_orbit_cover.py"
OUT = HERE / "results_tail_nonmonomial_boundary_closure.json"
EXPECTED_OLD = "c7c0c3144efca8ad4181e94cd11127c27e64defea9c73c08a2889a38bee46dbf"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    if spec.loader is None:
        raise RuntimeError(("missing module loader", path))
    spec.loader.exec_module(module)
    return module


CORE = load("tail_nonmonomial_core", CORE_PATH)
ORBIT = load("tail_nonmonomial_orbit_core", ORBIT_PATH)


def require(value, detail):
    if not value:
        raise RuntimeError(detail)


def logical_hash(value):
    return sha256(json.dumps(value, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def negate(polynomial):
    return Counter({monomial: -coefficient
                    for monomial, coefficient in polynomial.items()})


def multiply(left, right):
    answer = Counter()
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            answer[tuple(sorted(left_monomial+right_monomial))] += (
                left_coefficient*right_coefficient)
    return Counter({monomial: coefficient for monomial, coefficient
                    in answer.items() if coefficient})


def add(left, right, right_scale=1):
    answer = Counter(left)
    for monomial, coefficient in right.items():
        answer[monomial] += right_scale*coefficient
    return Counter({monomial: coefficient for monomial, coefficient
                    in answer.items() if coefficient})


def xi_atoms(left, right):
    """Minor of C_i=U_i*g0_i7 and D_i=V_i*g0_i6."""
    return Counter({
        tuple(sorted((f"U{left}", f"V{right}",
                      f"g0_{left}7", f"g0_{right}6"))): 1,
        tuple(sorted((f"U{right}", f"V{left}",
                      f"g0_{left}6", f"g0_{right}7"))): -1,
    })


def sigma_atoms(left, right):
    """The complementary permanent C_i*D_j+C_j*D_i."""
    return Counter({
        tuple(sorted((f"U{left}", f"V{right}",
                      f"g0_{left}7", f"g0_{right}6"))): 1,
        tuple(sorted((f"U{right}", f"V{left}",
                      f"g0_{left}6", f"g0_{right}7"))): 1,
    })


def raw_rescue_row(record, sites):
    answer = {}
    for column, coefficient in record["nonzero_columns"].items():
        if int(column[1:]) in sites:
            answer[column] = (1, tuple(coefficient.split("*")))
    return answer


def reduced_matrix(sites, channel, records):
    matrix = []
    if channel == "Y":
        matrix.append({site: (1, (f"P{site}", f"V{site}"))
                       for site in sites})
    elif channel == "Z":
        matrix.append({site: (-1, (f"Q{site}", f"U{site}"))
                       for site in sites})
    else:
        require(channel is None, ("unknown channel", channel))
    matrix.extend(CORE.rescue_row(record, sites, True)
                  for record in records)
    return matrix


def full_matrix(sites, channel, records):
    y_columns = tuple(f"y{site}" for site in sites)
    z_columns = tuple(f"z{site}" for site in sites)
    matrix = []
    if channel == "Y":
        matrix.append({column: (1, (f"P{column[1:]}",))
                       for column in y_columns})
    elif channel == "Z":
        matrix.append({column: (1, (f"Q{column[1:]}",))
                       for column in z_columns})
    else:
        require(channel is None, ("unknown channel", channel))
    for site in sites:
        matrix.append({f"y{site}": (1, (f"U{site}",)),
                       f"z{site}": (1, (f"V{site}",))})
    matrix.extend(raw_rescue_row(record, sites) for record in records)
    return matrix, y_columns+z_columns


def pure_orientation(record):
    orientations = {column[0] for column in record["nonzero_columns"]}
    return len(orientations) == 1


CERTIFICATES = (
    {
        "shape": "210", "sites": (0, 1, 2), "channel": "Y",
        "labels": ("F_00101212", "F_01100212"),
        "expected": "monomial", "old_orbit_count": 10,
    },
    {
        "shape": "111", "sites": (0, 2, 4), "channel": "Y",
        "labels": ("F_00011212", "F_00101212"),
        "expected": "monomial", "old_orbit_count": 6,
    },
    {
        "shape": "220", "sites": (0, 1, 2, 3), "channel": "Y",
        "labels": ("F_00101212", "F_01100212", "F_01120012"),
        "expected": "monomial", "old_orbit_count": 4,
    },
    {
        "shape": "211", "sites": (0, 1, 2, 4), "channel": "Y",
        "labels": ("F_00101212", "F_01100212", "F_01102012"),
        "expected": "monomial", "old_orbit_count": 4,
    },
    {
        "shape": "221", "sites": (0, 1, 2, 3, 4), "channel": "Y",
        "labels": ("F_00101212", "F_01100212", "F_01120012",
                   "F_01122001"),
        "expected": "monomial", "old_orbit_count": 2,
    },
    {
        "shape": "222_Xi", "sites": tuple(range(6)), "channel": "Y",
        "labels": ("F_00101212", "F_01100212", "F_01120012",
                   "F_01122001", "F_01122010"),
        "expected": "Xi_05", "old_orbit_count": 1,
    },
    {
        "shape": "222_Sigma", "sites": tuple(range(6)), "channel": None,
        "labels": ("F_10002121", "F_02102110", "F_22101010",
                   "F_00122110", "F_01122001", "F_01210201"),
        "expected": "Sigma_05", "old_orbit_count": 1,
    },
)


def normalized_equal(polynomial, expected):
    return polynomial == expected or polynomial == negate(expected)


def transport_check(certificate, rows, actions):
    original_pair = (0, 5)
    checked = 0
    for action in actions:
        sites = tuple(sorted(action[site] for site in certificate["sites"]))
        channel = certificate["channel"]
        if channel is not None and action[6] == 7:
            channel = "Z" if channel == "Y" else "Y"
        labels = tuple(CORE.transform_label(label, action)
                       for label in certificate["labels"])
        records = tuple(rows[label] for label in labels)
        polynomial = CORE.formal_determinant_dp(
            reduced_matrix(sites, channel, records), sites)
        require(polynomial, ("transported determinant vanished",
                             certificate["shape"], action))
        _common, residual = CORE.common_monomial(polynomial)
        expected_kind = certificate["expected"]
        if expected_kind == "monomial":
            require(len(residual) == 1,
                    ("transported monomial changed",
                     certificate["shape"], action, CORE.encode(residual)))
        else:
            pair = tuple(sorted((action[original_pair[0]],
                                 action[original_pair[1]])))
            expected = (xi_atoms(*pair) if expected_kind == "Xi_05"
                        else sigma_atoms(*pair))
            require(normalized_equal(residual, expected),
                    ("transported two-term atom changed", expected_kind,
                     action, CORE.encode(residual), CORE.encode(expected)))
        checked += 1
    return checked


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()

    source = json.loads(SOURCE.read_text())
    old = json.loads(OLD_THEOREM.read_text())
    require(old["logical_sha256"] == EXPECTED_OLD,
            "old generic tail-response theorem digest changed")
    require(old["generic_principal_open_coverage"] == {
        "SDR": 66, "Delta_layer": 33, "Hall_d3": 16,
        "Hall_d4": 8, "Hall_d5": 2, "Hall_d6": 1,
        "total": 126,
    }, "old orbit coverage census changed")
    old_certificate_counts = Counter(
        record["certificate"] for record in old["orbit_coverage"])
    require(old_certificate_counts == {
        "611+71_SDR": 66, "M_sep": 20, "M_adj": 13,
        "Hall_adjacent_triple": 10, "Hall_separated_triple": 6,
        "Theta_220": 4, "Theta_211": 4, "Theta_221": 2,
        "Theta_222": 1,
    }, ("old certificate orbit ledger changed", old_certificate_counts))
    rows = {row["source_label"]: row for row in source["row_ledger"]}
    actions = ORBIT.vertex_actions()
    require(len(actions) == 96, "fixed-tail group order changed")

    # Literal covariance is checked for every row used here, including the
    # rescue-only certificate, rather than inferred from support patterns.
    used_labels = sorted({label for certificate in CERTIFICATES
                          for label in certificate["labels"]})
    coefficient_transports = 0
    for label in used_labels:
        record = rows[label]
        require(record["profile"] == "3+3+2" and pure_orientation(record),
                ("certificate row is not a pure literal 332 row", label))
        for action in actions:
            image_label = CORE.transform_label(label, action)
            expected = {
                ORBIT.transform_column(column, action):
                    ORBIT.transform_coefficient(coefficient, action)
                for column, coefficient in record["nonzero_columns"].items()
            }
            require(rows[image_label]["nonzero_columns"] == expected,
                    ("literal coefficient transport changed", label,
                     image_label))
            coefficient_transports += 1

    records = []
    for certificate in CERTIFICATES:
        sites = certificate["sites"]
        selected = tuple(rows[label] for label in certificate["labels"])
        reduced = CORE.formal_determinant_dp(
            reduced_matrix(sites, certificate["channel"], selected), sites)
        require(reduced, ("selected reduced determinant vanished",
                          certificate["shape"]))
        common, residual = CORE.common_monomial(reduced)
        if certificate["expected"] == "monomial":
            require(len(reduced) == 1 and len(residual) == 1,
                    ("monomial tail certificate changed",
                     certificate["shape"], CORE.encode(residual)))
        elif certificate["expected"] == "Xi_05":
            require(normalized_equal(residual, xi_atoms(0, 5)),
                    ("Xi certificate changed", CORE.encode(residual)))
        else:
            require(normalized_equal(residual, sigma_atoms(0, 5)),
                    ("Sigma certificate changed", CORE.encode(residual)))

        full, columns = full_matrix(sites, certificate["channel"], selected)
        full_determinant = CORE.formal_determinant_dp(full, columns)
        require(full_determinant in (reduced, negate(reduced)),
                ("literal full/reduced determinant replay changed",
                 certificate["shape"]))
        transported = transport_check(certificate, rows, actions)
        records.append({
            "shape": certificate["shape"],
            "double_sites": list(sites),
            "old_orbit_count": certificate["old_orbit_count"],
            "channel_rows_retained": ([] if certificate["channel"] is None
                                      else [certificate["channel"]]),
            "source_labels": list(certificate["labels"]),
            "source_row_coefficients": {
                label: rows[label]["nonzero_columns"]
                for label in certificate["labels"]
            },
            "full_minor_rows": (([] if certificate["channel"] is None
                                  else [certificate["channel"]])+
                                 [f"E{site}" for site in sites]+
                                 list(certificate["labels"])),
            "full_minor_columns": list(columns),
            "determinant_term_count": len(reduced),
            "common_monomial_factors": list(common),
            "primitive_factor": CORE.encode(residual),
            "primitive_factor_name": certificate["expected"],
            "literal_full_vs_reduced_replay": True,
            "fixed_tail_transports_checked": transported,
        })

    # The two d=6 primitives are a determinant/permanent pair in the same
    # two monomials.  Their common zero on the support torus is empty over Q.
    xi = xi_atoms(0, 5)
    sigma = sigma_atoms(0, 5)
    positive = Counter({
        tuple(sorted(("U0", "V5", "g0_07", "g0_56"))): 2})
    negative = Counter({
        tuple(sorted(("U5", "V0", "g0_06", "g0_57"))): 2})
    require(add(sigma, xi) == positive and
            add(sigma, xi, right_scale=-1) == negative,
            "Xi/Sigma sum-difference unit identity changed")

    cross_block_pairs = {
        tuple(sorted((action[0], action[5]))) for action in actions
    }
    expected_cross_block_pairs = {
        (left, right) for left in range(6) for right in range(left+1, 6)
        if left//2 != right//2
    }
    require(cross_block_pairs == expected_cross_block_pairs and
            len(cross_block_pairs) == 12,
            "cross-block pair orbit changed")

    site_orbit_sizes = {}
    for certificate in CERTIFICATES[:6]:
        sites = frozenset(certificate["sites"])
        orbit = {frozenset(action[site] for site in sites)
                 for action in actions}
        site_orbit_sizes[certificate["shape"]] = len(orbit)
    require(site_orbit_sizes == {
        "210": 12, "111": 8, "220": 3, "211": 12,
        "221": 6, "222_Xi": 1,
    }, ("canonical Hall site-orbit sizes changed", site_orbit_sizes))

    result = {
        "status": (
            "PASS exact Delta/Lambda/Omega-free tail-response closure"),
        "supersedes_generic_boundary_ledger": EXPECTED_OLD,
        "tail_missing_pattern_orbits": 126,
        "closed_orbit_census": {
            "old_SDR": 66,
            "old_Delta_layer": 33,
            "Hall_d3": 16,
            "Hall_d4": 8,
            "Hall_d5": 2,
            "Hall_d6": 1,
            "total": 126,
        },
        "literal_hitting_set": records,
        "structural_meanings": {
            "Delta_ab": (
                "det[[A_a,A_b],[B_a,B_b]] for A_i=P_i*V_i and "
                "B_i=Q_i*U_i"),
            "Delta_rank_one_parameterization": (
                "A_i=rho*s_i, B_i=sigma*s_i; this is division-free and "
                "retains zero-column boundary components"),
            "Lambda_UV_ab": "det[[U_a,U_b],[V_a,V_b]]",
            "Lambda_rank_one_parameterization": (
                "U_i=rho*s_i, V_i=sigma*s_i, without division"),
            "Omega_015": (
                "with A=g0_01*g0_45 and "
                "B=g0_04*g0_15-g0_05*g0_14, Omega equals "
                "2*U0*V4*V5*A+U4*V0*V5*(-A+B)+"
                "U5*V0*V4*(-A-B); it is one trilinear incidence, "
                "not an intrinsic source-rank factor"),
            "Xi_ab": (
                "det[[C_a,C_b],[D_a,D_b]] for "
                "C_i=U_i*g0_i7 and D_i=V_i*g0_i6"),
            "Xi_rank_one_parameterization": (
                "U_i=rho*s_i*g0_i6, V_i=sigma*s_i*g0_i7; on the "
                "support torus this parametrizes the rank-one incidence "
                "without dividing by a displayed factor"),
        },
        "common_locus_theorem": {
            "d3_to_d5": (
                "For each canonical Hall shape, a one-channel plus d-1 "
                "literal 332 minor is already a support monomial. Thus "
                "simultaneous Delta vanishing does not lower full source "
                "rank; the redundant second channel row is simply omitted."),
            "d6": (
                "One-channel plus five 332 rows gives M*Xi_05. Six 332 "
                "rows and no channel row give N*Sigma_05, transported from "
                "Sigma_35. Since Sigma_05+Xi_05=2*C0*D5 and "
                "Sigma_05-Xi_05=2*C5*D0, their common zero is empty on "
                "the characteristic-zero support torus."),
            "order_96_transport": (
                "The fixed-tail group sends the representatives through "
                "every required Hall site shape; Xi/Sigma cross-block "
                "pairs form one 12-element orbit. Every used literal row "
                "coefficient was replayed under all 96 actions."),
        },
        "removed_nonmonomial_factor_orbits": [
            "Delta_sep", "Lambda_UV_sep", "Omega_015"],
        "remaining_recursive_divisor_antichain": [{
            "factor_family": "support_monomial",
            "factor_orbit_count": 4,
            "suborbits": [
                "h_residual_tail", "g_residual_same_block",
                "g_residual_distinct_blocks", "g_residual_tail",
            ],
            "route": "smaller cofactor/edge-support charts",
        }],
        "characteristic_guard": (
            "The d=6 unit-on-the-support-torus uses 2 != 0; the theorem "
            "is over Q/characteristic zero."),
        "symmetry_audit": {
            "fixed_tail_group_order": len(actions),
            "used_literal_source_rows": len(used_labels),
            "literal_coefficient_transports_checked":
                coefficient_transports,
            "canonical_site_orbit_sizes": site_orbit_sizes,
            "cross_block_Xi_Sigma_pair_orbit_size":
                len(cross_block_pairs),
        },
        "mutation_guards": {
            "replace_Sigma_plus_by_Xi_minus": (
                add(xi, xi) != positive),
            "characteristic_two_would_kill_common_locus_identity": True,
            "every_selected_row_is_literal_pure_orientation_332": True,
        },
        "scope_guard": (
            "This closes the nonmonomial determinant boundaries on the "
            "same displayed support-monomial opens as the frozen tail "
            "theorem. Vanishing support factors still route to the existing "
            "cofactor/edge-support recursion; no mate or one-colour H "
            "condition is inferred here."),
        "source_hashes": {
            "source": sha256(SOURCE.read_bytes()).hexdigest(),
            "old_theorem": sha256(OLD_THEOREM.read_bytes()).hexdigest(),
            "core": sha256(CORE_PATH.read_bytes()).hexdigest(),
            "orbit_core": sha256(ORBIT_PATH.read_bytes()).hexdigest(),
        },
    }
    require(result["mutation_guards"][
        "replace_Sigma_plus_by_Xi_minus"],
        "Sigma sign mutation did not fire")
    result["logical_sha256"] = logical_hash(result)
    if args.write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("tail nonmonomial boundary closure: PASS",
          result["logical_sha256"])
    print("remaining divisor orbits", 4, "all support-monomial")
    print("literal coefficient transports", coefficient_transports)


if __name__ == "__main__":
    main()
