#!/usr/bin/env python3
"""Freeze the sound relative-cokernel replacement for a C10 coordinate."""

from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
KERNEL = ROOT / "computations/unaudited-codex-n8-orbit26-direct-target-2026-08-23/results_c10_constant_provider_kernel.json"
CAP = ROOT / "computations/unaudited-codex-n8-orbit26-direct-target-2026-08-23/results_c10_lower_kernel_invariance.json"
D12_REPORT = ROOT / "computations/unaudited-codex-n8-y10-degree12-seeds-2026-08-23/REPORT.md"
D12_CHECK = ROOT / "computations/unaudited-codex-n8-y10-degree12-seeds-2026-08-23/audit_degree12_restricted.py"
C10 = ROOT / "computations/unaudited-codex-n8-orbit26-direct-target-2026-08-23/results_full_y10_aggregate.json"
RESULT = HERE / "results_c10_relative_cokernel.json"
EXPECTED = {
    KERNEL: "cb1a569493022716d118e8796f8441f902ba693ed7699ccea7a3e51ca6ceb6f0",
    CAP: "720fc8a17c7f05983d3609c1be9acad411a8049954e06fac80c8eabafc98add2",
    D12_REPORT: "a7ad49d0772ebae72d241e32df941fca16e6acb667324f9d3663eb430a443242",
    D12_CHECK: "723c03ff0ae9bf56bb92c498e0889d30d767fa594bcccdfae5221456710dff4b",
    C10: "fa0bf7ae3d50d232450c0ea3188bd4aad6f6f4b4513d014899b4e1edf67949ed",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def audit(mutate=False):
    for path, digest in EXPECTED.items():
        require(sha256(path.read_bytes()).hexdigest() == digest,
                f"source drift: {path}")
    kernel = json.loads(KERNEL.read_text())
    cap = json.loads(CAP.read_text())
    c10 = json.loads(C10.read_text())
    require(kernel["status"] == "EXACT_LITERAL_LOWER_KERNEL_CHANGES_LEX_C10"
            and kernel["logical_sha256"]
            == "edc37a9c5c1785db383cc518fa151912ad1589e70d929b9e71915153fb3db80e",
            "exact lower-kernel counterexample changed")
    witness = kernel["lex_smallest_minimal_column_witness"]
    require(witness["literal_lower_rows_after_collection"] == 0
            and witness["terminal_y10_rows"] == 714
            and witness["target_coefficient"] == 1,
            "lower-kernel terminal witness changed")
    require(cap["status"] == "C10_INVARIANCE_CAP_UNRESOLVED"
            and cap["target_owners_forced_zero"] == 0
            and cap["unexpanded_active_columns"] == 283468,
            "capped coordinate-invariance audit changed")
    require(c10["PM4_incidence"]["lex_dead_coefficient"] == -4
            and c10["PM4_incidence"]["lex_dead_row"]
            == kernel["target_y10"], "C10 selected coordinate changed")

    terminal_support = witness["terminal_y10_rows"]
    if mutate:
        terminal_support -= 1
    require(terminal_support == 714, "hostile terminal-support mutation survived")

    result = {
        "format": "n8-c10-relative-cokernel-audit-v1",
        "status": "RELATIVE_COKERNEL_IS_SOUND_MONOMIAL_DUAL_DESCENDS_ONLY_EXISTENTIALLY",
        "linear_interface": {
            "source_space": "E = all homogeneous total-degree12 mixed source columns",
            "lower_map": "L:E -> R_(y<=9)",
            "terminal_map": "H:E -> R_(y>=10)",
            "lower_kernel": "K=ker(L)",
            "boundary": "B=H(K)",
            "invariant": "[C10] in coker_relative = R_(y>=10)/B",
        },
        "dual_interface": {
            "condition": "lambda in B^perp iff lambda*H vanishes on ker(L)",
            "factorization": "equivalently there is mu with H^T*lambda = L^T*mu",
            "separation_target": "find (mu,lambda) with lambda(C10)!=0",
            "advantage": "does not require an explicit basis of the full lower kernel",
            "counterguard": "without sparse support or symmetry this transpose system is the full degree12 Macaulay dual in another form",
        },
        "exact_coordinate_failure": {
            "source_columns": witness["source_column_count"],
            "lower_output_rows": witness["literal_lower_rows_after_collection"],
            "terminal_y10_support": terminal_support,
            "selected_coordinate": kernel["target_y10"],
            "selected_coordinate_value": witness["target_coefficient"],
            "consequence": (
                "delta_m is not in B^perp. Adding -4 times this lower-kernel "
                "vector cancels the deterministic coefficient -4 at m and "
                "moves it to the other 713 terminal rows without changing the "
                "relative cokernel class."
            ),
        },
        "degree12_monomial_certificate": {
            "monomial": kernel["target_y10"] + "*t^2",
            "logical_sha256": "8030714e1f1edaa844664c893bb28f6574e32cca7d3e88a3e1379cfc25d541bd",
            "descent": (
                "Existentially yes: m not in im(L,H) implies a full degree12 "
                "dual phi=(mu,lambda) with phi(m)!=0. For k in ker(L), "
                "lambda(Hk)=phi((L,H)k)=0, so lambda descends and [m]!=0 in "
                "the relative cokernel."
            ),
            "missing": (
                "The restricted-owner artifact does not export this full dual, "
                "and phi(m)!=0 says nothing about phi(C10). The other C10 rows "
                "may pair to -phi(m)*(-4) and cancel."
            ),
        },
        "smallest_exact_finite_packet": {
            "boundary_rank_lower_bound": 1,
            "boundary_generator_support": 714,
            "quotient": "R_y10 / span<v0> for the displayed one-dimensional sub-boundary",
            "effect": "kills the isolated m-coordinate argument but does not approximate the full B sufficiently for a C10 verdict",
        },
        "capped_full_coordinate_audit": {
            "known_lower_rows": cap["known_lower_rows"],
            "known_global_owner_columns": cap["known_global_owner_columns"],
            "unexpanded_active_columns": cap["unexpanded_active_columns"],
            "verdict": "no finite closure or coordinate invariant was obtained; the exact 90-column kernel already refutes the hoped-for coordinate",
        },
        "scope": (
            "exact conceptual quotient and exact one-dimensional boundary "
            "counterguard in normalized orbit26/total degree12; no full lower-kernel "
            "basis, full C10 pairing, t-saturation, or global chart inference"
        ),
        "source_sha256": {str(path.relative_to(ROOT)): digest
                          for path, digest in EXPECTED.items()},
    }
    result["logical_sha256"] = sha256(json.dumps(
        result, sort_keys=True, separators=(",", ":")
    ).encode("ascii")).hexdigest()
    return result


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    parser.add_argument("--mutate", action="store_true")
    args = parser.parse_args()
    result = audit(args.mutate)
    if args.write_results:
        RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    if args.check_results:
        require(RESULT.exists() and json.loads(RESULT.read_text()) == result,
                "stored result changed")
    print(result["status"])
    print("logical", result["logical_sha256"])


if __name__ == "__main__":
    main()
