#!/usr/bin/env python3
"""Construct the literal residual-q M_v image from old cap plus Cartan.

On the normalized Y=1 canonical repeated P3+K2 slice, let

    O_alpha = sum_j alpha_j(-r0_j+T_j+rho_j),
    alpha = (-1,+1,+1,-1).

The complete literal audit gives O_alpha boundary -sum alpha_j B_j,
Eq=-alpha, residue=alpha, and zero protected rows.  The physical
endpoint-odd Cartan/HPL cell K has zero literal source and first Spencer
output, residue alpha, zero protected rows, and the -dOmega eta/sigma ridge.
Therefore

                         M_v = -O_alpha + K

has exactly the previously missing literal mapping-cone image.  This closes
output-side membership; it does not construct the 15-label input Phi.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_residual_q_literal_mapping_cone_private_boundary_gate.py":
        "b890195a8fc0c4e90c9c9c0c03c41a95690228c81026f4c2ea1fa95908564e38",
    "computations/verify_h3_order6_endpoint_odd_hpl_secondary_transfer.py":
        "5a89d25227562b397d6cf3f16306346ce7d9fd16fb73a0f0a4486355a7cef29e",
    "computations/verify_h3_physical_cartan_source_orbit_descent.py":
        "c92667c38c57c69dff18fd7570fa154db7e1a634a83f462dfde6bd5553128a3a",
    "computations/verify_h3_physical_cartan_closes_residual_q_ks_hypothesis.py":
        "4453dad26b5d13767fc206e9a8dc98af5428ac6d00cfc9444ac6b4253c834f7c",
    "computations/verify_h3_residual_q_terminal_ridge_kahler_identification.py":
        "aea73ce5ff6ce183245d209393ed60192066d38eab7d4d203caa0c82cc5b16d6",
}
EXPECTED_LEDGER_SHA256 = (
    "84904cfd9f434eb8ff36548a0b2e0b2e68b8ec562c6559a89acdefb94500eb64"
)


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


def literal_full_nine_audit(literal):
    complete = load(
        "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py",
        "mv_cap_cartan_complete",
    )
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "mv_cap_cartan_base",
    )
    supports = []
    digests = []
    records = []
    for component, (left, right, left_cell, _right_cell) in enumerate(
            complete.CUBIC_PAIRS):
        degree = complete.degree_add(
            base.lambda_degree(left),
            complete.cell_degree(complete.CYCLE_CELLS[left_cell]),
        )
        block = complete.component(base, degree)
        pure = [
            (word, multiplier, boundary)
            for word, multiplier, boundary in block["columns"]
            if word == complete.PURE_WORD
        ]
        require(len(pure) == 6,
                ("the pure r0 corner inventory changed", component))
        component_supports = []
        for selected in combinations(pure, 4):
            aggregate = defaultdict(Q)
            for coefficient, (_word, _multiplier, boundary) in zip(
                    literal.ALPHA, selected, strict=True):
                for feature in boundary:
                    aggregate[feature] += coefficient
            aggregate = {feature: value for feature, value in
                         aggregate.items() if value}
            require(len(aggregate) == 360,
                    ("a literal alpha aggregate stopped having 360 terms",
                     component, len(aggregate)))
            supports.append(len(aggregate))
            component_supports.append(len(aggregate))
            digests.append(sha256(json.dumps(sorted(
                (repr(feature), str(value)) for feature, value in
                aggregate.items()
            ), separators=(",", ":")).encode()).hexdigest())
        records.append({
            "component": component,
            "faces": [left, right],
            "four_corner_choices": len(component_supports),
            "minus_O_literal_boundary_support": sorted(
                set(component_supports)),
        })
    require(len(supports) == 75 and set(supports) == {360}
            and len(set(digests)) == 75,
            "the complete literal -O_alpha census changed")
    return records, digests


def augmented_sign_audit(literal, cartan, hpl, ridge):
    alpha = literal.ALPHA
    terminal = {
        **{f"eta{face}_constant": 1 for face in range(1, 6)},
        "eta1_U1": 1,
        "sigma_qpq22": -1,
    }

    per_corner = {}
    for corner in literal.CORNERS:
        per_corner[corner] = {
            "r0": literal.vector(**{
                f"private_{corner}": 1,
                f"Eq_{corner}": 1,
                f"target_{corner}": 1,
                "ainc": -1,
            }),
            "T": literal.vector(**{
                f"W_{corner}": -1,
                f"target_{corner}": 1,
            }),
            "rho": literal.vector(**{
                f"W_{corner}": 1,
                f"R_{corner}": 1,
            }),
        }

    O_alpha = literal.add(*(
        literal.scale(alpha[index], literal.add(
            literal.scale(-1, per_corner[corner]["r0"]),
            per_corner[corner]["T"],
            per_corner[corner]["rho"],
        ))
        for index, corner in enumerate(literal.CORNERS)
    ))
    minus_O = literal.scale(-1, O_alpha)

    K = literal.vector(**{
        **{f"R_{corner}": alpha[index]
           for index, corner in enumerate(literal.CORNERS)},
        **terminal,
    })
    candidate = literal.add(minus_O, K)
    desired = literal.add(*(
        literal.vector(**{
            f"private_{corner}": alpha[index],
            f"Eq_{corner}": alpha[index],
        })
        for index, corner in enumerate(literal.CORNERS)
    ), literal.vector(**terminal))
    require(candidate == desired,
            "-O_alpha+K stopped equalling the literal M_v signature")

    for index, corner in enumerate(literal.CORNERS):
        require(
            minus_O[literal.ROWS.index(f"private_{corner}")] == alpha[index]
            and minus_O[literal.ROWS.index(f"Eq_{corner}")] == alpha[index]
            and minus_O[literal.ROWS.index(f"R_{corner}")] == -alpha[index]
            and K[literal.ROWS.index(f"R_{corner}")] == alpha[index],
            ("a corner sign changed", corner),
        )
    require(all(candidate[literal.ROWS.index(row)] == 0 for row in (
        *(f"R_{corner}" for corner in literal.CORNERS),
        *(f"W_{corner}" for corner in literal.CORNERS),
        *(f"target_{corner}" for corner in literal.CORNERS),
        "ainc",
    )), "the cap/Cartan sum retained a protected or residue row")

    hpl_ledger, hpl_digest = hpl.audit()
    require(hpl_digest == hpl.EXPECTED_LEDGER_SHA256,
            "the exact order-six HPL ledger changed")
    operator = hpl_ledger["bounded_physical_operator_module"]
    require(operator["literal_source_output"] == 0
            and operator["first_transfer_support"] == 0
            and hpl_ledger["hpl_identification"]["D2_value"]
            == "-delta=(-1,+1,+1,-1)",
            "K acquired a literal/private or first-Spencer output")

    physical = cartan.audit()
    packet = physical["physical_packet"]
    require(tuple(map(Q, packet["ordinary_residue"])) == alpha
            and packet["protected_D_W_target_anchor_Eq"] == 0
            and packet["common_repeated_grade"]
            == "canonical endpoint-recoloured faces-(3,5) bridge",
            "the physical Cartan packet stopped matching the cap grade")

    ridge_ledger = ridge.audit()
    require(ridge_ledger["terminal_ridge_uniqueness"]["eta_contraction"]
            == "1+delta_(vz)*u_z/t"
            and ridge_ledger["terminal_ridge_uniqueness"]["sigma_contraction"]
            == "-q_pq^22",
            "the Cartan ridge stopped supplying the M_v terminal")

    return {
        "alpha": [int(value) for value in alpha],
        "O_alpha": {
            "formula": "sum_j alpha_j(-r0_j+T_j+rho_j)",
            "literal_boundary": "-sum_j alpha_j B_j",
            "Eq": [int(-value) for value in alpha],
            "ordinary_residue": [int(value) for value in alpha],
            "D_W_target_ainc": [0, 0, 0, 0],
        },
        "minus_O_alpha": {
            "literal_boundary": "+sum_j alpha_j B_j",
            "Eq": [int(value) for value in alpha],
            "ordinary_residue": [int(-value) for value in alpha],
            "D_W_target_ainc": [0, 0, 0, 0],
        },
        "K": {
            "literal_source_output": operator["literal_source_output"],
            "first_Spencer_output": operator["first_transfer_support"],
            "ordinary_residue": [int(value) for value in alpha],
            "protected_D_W_target_ainc_Eq": 0,
            "eta_z": "1+delta_(vz)*u_z/t",
            "sigma": "-q_pq^22",
            "source_provenant": True,
            "common_repeated_grade": packet["common_repeated_grade"],
        },
        "M_v_equals_minus_O_plus_K": {
            "literal_boundary": "+sum_j alpha_j B_j",
            "literal_boundary_support": 360,
            "Eq": [int(value) for value in alpha],
            "ordinary_residue": [0, 0, 0, 0],
            "D_W_target_ainc": [0, 0, 0, 0],
            "eta_z": "1+delta_(vz)*u_z/t",
            "sigma": "-q_pq^22",
            "all_augmented_rows_match": True,
        },
    }


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    literal = load(
        "computations/verify_h3_residual_q_literal_mapping_cone_private_boundary_gate.py",
        "mv_cap_cartan_literal",
    )
    hpl = load(
        "computations/verify_h3_order6_endpoint_odd_hpl_secondary_transfer.py",
        "mv_cap_cartan_hpl",
    )
    cartan = load(
        "computations/verify_h3_physical_cartan_source_orbit_descent.py",
        "mv_cap_cartan_physical",
    )
    closure = load(
        "computations/verify_h3_physical_cartan_closes_residual_q_ks_hypothesis.py",
        "mv_cap_cartan_closure",
    )
    ridge = load(
        "computations/verify_h3_residual_q_terminal_ridge_kahler_identification.py",
        "mv_cap_cartan_ridge",
    )

    literal_ledger, literal_digest = literal.audit()
    require(literal_digest == literal.EXPECTED_LEDGER_SHA256,
            "the literal M_v gate changed")
    require(literal_ledger["normalization_scope"].startswith(
                "marked clean-C5 slice with cap normalization Y=1"),
            "the literal normalization scope changed")
    full_records, aggregate_digests = literal_full_nine_audit(literal)
    composition = augmented_sign_audit(literal, cartan, hpl, ridge)

    closure_ledger = closure.audit()
    require(closure_ledger["common_source_type"]["word"]
            == "1211222 after deleting the distinguished endpoint"
            and closure_ledger["common_source_type"]["ordinary_residue"]
            == [-1, 1, 1, -1]
            and closure_ledger["common_source_type"][
                "protected_D_W_target_anchor_Eq"] == 0,
            "the Cartan/KS common source type changed")

    ledger = {
        "theorem": "literal M_v image is the old cap/physical Cartan composition",
        "normalization_scope": (
            "canonical marked clean-C5 slice with Y=1.  A general-Y claim "
            "requires rederiving the cap coefficients"
        ),
        "complete_literal_census": full_records,
        "literal_alpha_aggregates": len(aggregate_digests),
        "distinct_literal_alpha_aggregates": len(set(aggregate_digests)),
        "composition": composition,
        "construction": (
            "in the complete physical relative source module set "
            "M_v=-O_alpha+K.  Here O_alpha is an actual combination of the "
            "old r0,T,rho source cells and K is the source-provenant "
            "endpoint-odd Cartan/HPL cell.  Their ordinary residues cancel; "
            "the former supplies every literal B_j/Eq row and the latter "
            "supplies only the required eta/sigma ridge beyond residue"
        ),
        "probe_assumption_audit": (
            "the coarse assumption that K has zero private rows is justified "
            "by the exact 8580-column order-six theorem: its literal source "
            "output and D1/first-Spencer output both vanish.  No free ULTRA "
            "unit or presentation-only private cancellation is used"
        ),
        "frontier_shift": (
            "output-side M_v membership is constructed on the normalized "
            "canonical slice.  Gate I now consists only of constructing the "
            "input-side physical comparison on the 15 collision labels "
            "(equivalently absorbing the complementary word packet of the "
            "overlapping-root odd Cartan prism)"
        ),
        "nonclaims": [
            "no general-Y cap composition is claimed",
            "no 15-label input Phi is constructed by this theorem",
            "no inactive normal-grade or diagonal-Rees extension is claimed",
        ],
        "pins": PINS,
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("literal M_v cap/Cartan ledger changed", digest))
    return ledger, digest


def main():
    ledger, digest = audit()
    print("h3 literal M_v cap/Cartan composition: CONSTRUCTED")
    print("M_v=-O_alpha+K; literal boundary support=360")
    print("ordinary residue: -alpha+alpha=0")
    print("eta/sigma: physical -dOmega ridge")
    print("remaining Gate I: 15-label input Phi")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
