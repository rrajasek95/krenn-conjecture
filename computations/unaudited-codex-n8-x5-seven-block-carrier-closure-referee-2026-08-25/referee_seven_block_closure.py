#!/usr/bin/env python3
"""Independent, fail-closed referee for the proposed seven-block closure."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PKG = Path(__file__).resolve().parent

BOUNDARY = ROOT / "computations/unaudited-codex-n8-x5-seven-block-support-boundary-2026-08-25"
REDUCTION = ROOT / "computations/unaudited-codex-n8-x5-seven-block-two-sandwich-reduction-2026-08-25"
RANK1 = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rank1-incidence-gate-2026-08-25"
RANK2 = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rank2-incidence-gate-2026-08-25"
REP3 = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep3-low-rank-carrier-2026-08-25"
REPS145 = ROOT / "computations/unaudited-codex-n8-x5-seven-block-reps1-4-5-low-rank-carrier-2026-08-25"
REP2 = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep2-exhaustive-carrier-closure-2026-08-25"

EXPECTED_MANIFESTS = {
    BOUNDARY: "13bb284c0b400f7227db74f8a135155dd324251147ebf48711b9af8d10adcc85",
    REDUCTION: "056d73cd56818a18e2976707815f902cc433839ce69b192a88b118b7a9a5d707",
    RANK1: "45ab914ff35c446f67fcc2ec86a6d4201c8ddf3e0afed0b9420e269ad610daa9",
    RANK2: "3e408289040035bf1dcf9152611d62cd495050817e9a990c0315483d8993b0de",
    REP3: "050dd75b8de30bc05bec61c9da1b8df2720a5a2e88741b49ff19e3de69d861c0",
    REPS145: "63f5f18c7740cb73d4832e2bff477a43d160ea5db9370b2ce64c3188de87bf68",
    REP2: "006512d367abfe79d554ce1f1ad3d2db897abc03659b642d9b7a2c148654681a",
}


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load(path: Path):
    with path.open() as f:
        return json.load(f)


def support_key(record) -> tuple[str, ...]:
    return tuple(record["added"])


def flag_key(record) -> tuple[str, ...]:
    return tuple(record["nonzero_variable_blocks"])


def main() -> None:
    pins = {}
    for package, expected in EXPECTED_MANIFESTS.items():
        actual = sha(package / "MANIFEST.sha256")
        assert actual == expected, (package, actual, expected)
        pins[str((package / "MANIFEST.sha256").relative_to(ROOT))] = actual

    boundary_path = BOUNDARY / "results_seven_block_support_boundary.json"
    reduction_path = REDUCTION / "results_two_sandwich_reduction.json"
    boundary = load(boundary_path)
    reduction = load(reduction_path)
    pins[str(boundary_path.relative_to(ROOT))] = sha(boundary_path)
    pins[str(reduction_path.relative_to(ROOT))] = sha(reduction_path)

    orbit_records = boundary["exact_variable_stratum_classification"]["unresolved_orbit_records"]
    records = []
    for orbit in orbit_records:
        assert len(orbit["members"]) == 2
        for member_index, member in enumerate(orbit["members"]):
            records.append({"orbit_id": orbit["orbit_id"], "member_index": member_index, **member})
    assert len(records) == 64
    record_keys = {(support_key(r), flag_key(r)) for r in records}
    assert len(record_keys) == 64

    reductions = reduction["reductions"]
    reduction_keys = {(tuple(r["added"]), tuple(r["nonzero_variable_blocks"])) for r in reductions}
    assert len(reductions) == 64 and reduction_keys == record_keys
    assert all(len(r["supported_forbidden_terms"]) == 2 for r in reductions)
    assert all(
        r["supported_forbidden_terms"][0]["response_pair"]
        != r["supported_forbidden_terms"][1]["response_pair"]
        for r in reductions
    )

    # Reconstruct the six canonical supports from the sealed packages.
    rep_support = {
        0: tuple(load(RANK1 / "rank1_ideal_metadata.json")["support"]["added"]),
        2: tuple(load(REP2 / "results_rep2_exhaustive_carrier.json")["support"]["added_nonzero"]),
        3: tuple(load(REP3 / "results_rep3_low_rank_carrier.json")["support"]["added_nonzero"]),
    }
    for rep in load(REPS145 / "results_remaining_reps_low_rank_carrier.json")["representatives"]:
        rep_support[rep["representative_id"]] = tuple(rep["support"]["added_nonzero"])
    assert sorted(rep_support) == list(range(6))
    assert tuple(load(RANK2 / "rank2_ideal_metadata.json")["support"]["added"]) == rep_support[0]

    # Find the order-two guard mate from the all-four-variable boundary orbit.
    support_owner = {}
    representative_supports = {}
    full_flags = ("04", "12", "35", "67")
    for rep_id, canonical in rep_support.items():
        matching_orbits = [
            orbit for orbit in orbit_records
            if any(support_key(m) == canonical and flag_key(m) == full_flags for m in orbit["members"])
        ]
        assert len(matching_orbits) == 1, (rep_id, canonical, len(matching_orbits))
        pair = {support_key(m) for m in matching_orbits[0]["members"]}
        assert len(pair) == 2 and canonical in pair
        representative_supports[rep_id] = sorted(pair)
        for key in pair:
            assert key not in support_owner
            support_owner[key] = rep_id
    assert len(support_owner) == 12

    # Each representative support occurs with all four A12/A67 zero/nonzero flags.
    expected_flags = {
        ("04", "35"),
        ("04", "12", "35"),
        ("04", "35", "67"),
        ("04", "12", "35", "67"),
    }
    for support in support_owner:
        assert {flag_key(r) for r in records if support_key(r) == support} == expected_flags

    # Rep0 is the only sealed representative whose proof checks all four
    # functionals (three diagonal readouts and cap pairing) across all ranks.
    # Reps1--5 prove only the cap-pairing clause from P proper.
    valid_rep_ids = {0}
    invalid_rep_ids = {1, 2, 3, 4, 5}

    covered = []
    uncovered = []
    for record in records:
        owner = support_owner.get(support_key(record))
        compact = {
            "orbit_id": record["orbit_id"],
            "member_index": record["member_index"],
            "added": record["added"],
            "nonzero_variable_blocks": record["nonzero_variable_blocks"],
        }
        if owner in valid_rep_ids:
            covered.append({**compact, "representative_id": owner})
        elif owner in invalid_rep_ids:
            uncovered.append({
                **compact,
                "candidate_representative_id": owner,
                "reason": "CAP_PAIRING_ONLY_DOES_NOT_EXCLUDE_DIAGONAL_INCIDENCE",
            })
        else:
            uncovered.append({
                **compact,
                "candidate_representative_id": None,
                "reason": "NO_SIX_REPRESENTATIVE_SUPPORT_THEOREM",
            })

    assert len(covered) == 8
    assert len(uncovered) == 56
    assert sum(u["reason"] == "CAP_PAIRING_ONLY_DOES_NOT_EXCLUDE_DIAGONAL_INCIDENCE" for u in uncovered) == 40
    assert sum(u["reason"] == "NO_SIX_REPRESENTATIVE_SUPPORT_THEOREM" for u in uncovered) == 16

    # Hostile abstract counterexample to the invalid inference:
    # P=Q=<e0>, hence P tensor Q=<E00>.  I is outside it, so trace is live
    # on the kernel, but K00 vanishes identically on that kernel.
    hostile = {
        "P_basis": ["e0"],
        "Q_basis": ["e0"],
        "response_row_space_basis": ["E00"],
        "identity_in_response_row_space": False,
        "trace_live_on_kernel_witness": "E11",
        "K00_identically_zero_on_kernel": True,
        "star_active": False,
    }
    assert not hostile["identity_in_response_row_space"]
    assert hostile["K00_identically_zero_on_kernel"] and not hostile["star_active"]

    # The identity-pairing sublemma itself is sound: rank(I3)=3, while every
    # element of P tensor Q has rank <= min(dim P, dim Q).  Thus I3 membership
    # forces dim P=dim Q=3.  It is only one of four required functionals.
    for p_dim in range(4):
        for q_dim in range(4):
            if min(p_dim, q_dim) >= 3:
                assert p_dim == q_dim == 3

    output = {
        "schema": "seven-block-carrier-closure-referee-v1",
        "status": "REJECT_COMPLETE_CLOSURE_EXACT_8_OF_64_PROVED",
        "pins": pins,
        "census": {
            "boundary_records": len(records),
            "two_sandwich_records": len(reductions),
            "representative_supports_with_guard_mates": len(support_owner),
            "validly_covered_records": len(covered),
            "uncovered_records": len(uncovered),
            "uncovered_bad_activity_inference": 40,
            "uncovered_no_representative_support": 16,
        },
        "representative_supports": {
            str(k): [list(x) for x in v] for k, v in sorted(representative_supports.items())
        },
        "valid_representatives": [0],
        "rejected_representative_claims": [1, 2, 3, 4, 5],
        "covered": covered,
        "uncovered": uncovered,
        "tensor_referee": {
            "orientation": "For L(K)=(U^T K B_j)_j, im(L*) consists of matrices with column space in Col(U) and row space in ColSpan(B_j); the common-right case is its transpose.",
            "diagonal_failure_iff": "K_ii vanishes on ker(L) iff E_ii=e_i e_i^T lies in P tensor Q, equivalently e_i in P and e_i in Q.",
            "cap_failure_iff": "<K,A_cap> vanishes on ker(L) iff A_cap lies in P tensor Q.",
            "identity_pairing_sublemma": "SOUND: I3 in P tensor Q forces P=Q=Q^3 by rank(I3)=3.",
            "invalid_inference": "I3 not in P tensor Q proves only the cap functional is live; it does not prove all three diagonal functionals are live.",
            "hostile_counterexample": hostile,
        },
        "zero_factor_referee": {
            "outside_factor_nonzero": "Guard makes the common factor singular, but an incidence/full-X5 argument is still required to exclude each e_i in P intersection Q.",
            "outside_factor_zero_A67_nonzero": "Companion factor is guard-forced zero; L67=0, so all diagonal functionals are live and nonzero A67 makes the cap functional live.",
            "outside_factor_zero_A67_zero": "The cap67 functional is zero, so the claimed carrier is inactive; closure requires explicit descent to the already-sealed <=6-added-block theorem.",
        },
        "next_exact_obligations": {
            "reps1_to_5": "For every rank/chart, prove no e_i lies in both P and Q, or use guard/full-X5 equations to produce another active carrier/block-zero descent.",
            "unrepresented_16": "Supply carrier theorems for the eight added supports in boundary orbit_ids 0..7 (two guard mates, A12 absent/present, A67 absent).",
            "eight_block": "NOT_READY: a seven-block induction base cannot be cited until these 56 records are discharged.",
        },
    }

    out = PKG / "results_seven_block_closure_referee.json"
    out.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": output["status"], "covered": len(covered), "uncovered": len(uncovered)}))


if __name__ == "__main__":
    main()
