#!/usr/bin/env python3
"""Propagate the independently replayed direct-K19 correction through K24."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
U = 400_591_699_200

FILES = {
    "referee": ("computations/unaudited-codex-orbit0-k19-direct-charge-correction-referee-2026-08-24/results_corrected_direct_k19_referee.json", None),
    "old_direct": ("computations/unaudited-codex-orbit0-k19-charge-2026-08-23/results_direct_k19.json", "7e5c821b6831f307c6833d93bb232c9a2f4421716183227cae1b65bacde376dd"),
    "old_complete_k19": ("computations/unaudited-codex-orbit0-k19-complete-charge-2026-08-23/results_complete_k19_charge.json", "d976b0a943ae3e1565054814882b2b280223a8f50dd0364e8fa1a8b01d8e055d"),
    "old_through_k23": ("computations/unaudited-codex-orbit0-filtered-charge-ledger-through-k23-2026-08-24/results_charge_ledger_through_k23.json", "45c94294cee372dc0674efd68e1cd02144f5af9c1366c9b1c7f9ff02b72b01a8"),
    "k24": ("computations/unaudited-codex-orbit0-k24-complete35-audit-2026-08-24/results_k24_complete35_exact.json", "c9823d5c33b7e11b0c92eb89a50b33de0223fea5fdf53b2838b1094e13b9dfe6"),
    "r8prime": ("computations/unaudited-codex-n8-dangerous-chart-bridge-2026-08-20/results_orbit0_cutoff9_sparse_r8.json", "62013c8a8453ffe68e6ef08740859db6efecaf825f121c19dc885b6afa7feb4b"),
    "r8prime_interface": ("computations/unaudited-codex-n8-dangerous-chart-bridge-2026-08-20/results_orbit0_anchor_times_r8_unary.json", "085020eea857a850fb97fbd3dc017918b0beaaa2a2b0d77800127d0c62775a36"),
}


def fail(message: str) -> None:
    raise ValueError(message)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name: str) -> dict:
    path, expected = FILES[name]
    full = ROOT / path
    if expected is not None and sha(full) != expected:
        fail(f"hash mismatch: {path}")
    value = json.loads(full.read_text())
    if not isinstance(value, dict):
        fail(f"object required: {path}")
    return value


def fraction(record: dict) -> Fraction:
    return Fraction(int(record["numerator"]), int(record["denominator"]))


def render(value: Fraction) -> dict:
    text = str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    return {"numerator": value.numerator, "denominator": value.denominator, "text": text}


def validate_referee(referee: dict) -> None:
    if referee.get("status") != "PASS_INDEPENDENT_CORRECTED_DIRECT_K19_FULL_IRREDUCIBLE_AND_27_PACKET_REPLAY":
        fail("referee status")
    corrected = referee.get("corrected_replay", {})
    historical = referee.get("historical_replay_control", {})
    delta = referee.get("corrected_minus_historical", {})
    if corrected != {
        "source_path": "computations/unaudited-codex-orbit0-k19-direct-conservation-audit-2026-08-24/recompute_d19_parent_charge.rs",
        "source_sha256": "7280d987f9ea1dbb4b492787f2b7577744fb6eb8331de84258165a546f0a3ffc",
        "binary_path": "computations/unaudited-codex-orbit0-k19-direct-conservation-audit-2026-08-24/recompute_d19_parent_charge",
        "binary_sha256": "715a2caf3a3f0df08aafc494f9a910d4636c40caf694b6d044ed3c345c784f60",
        "workers": 8, "rows": 167616000, "irreducible_rows": 55872000,
        "full_charge": 174465024, "irreducible_charge": 126418944,
        "pivotable_charge": 48046080, "scale_S_squared": "79412096674310400",
        "full_charge_scaled": "13854633352173884119449600",
        "irreducible_charge_scaled": "10039193402392232696217600",
    }:
        fail("corrected direct-K19 replay fields")
    if historical != {"rows": 167616000, "irreducible_rows": 55872000, "full_charge": 202278912, "irreducible_charge": 141570048, "pivotable_charge": 60708864}:
        fail("historical direct-K19 control")
    if delta != {"full_charge": -27813888, "irreducible_charge": -15151104, "pivotable_charge": -12662784}:
        fail("direct-K19 deltas")
    literal = referee.get("literal_transition_control", {})
    if literal.get("pivot_uses") != 230400 or literal.get("failures") != 0 or literal.get("residual_sum") != 0:
        fail("literal transition control")
    packets = referee.get("all_27_direct_packets", {})
    if packets.get("total_charge") != 4564224:
        fail("27-packet total")
    degrees = packets.get("degrees", {})
    expected = {"K14": 230092800, "K15": -539203584, "K16": 388502016, "K17": 53763072, "K18": -272994816, "K19": 174465024, "K20": -30060288}
    if {key: value.get("charge") for key, value in degrees.items()} != expected or sum(expected.values()) != 4564224:
        fail("27-packet per-degree identity")


def audit(referee: dict, old_direct: dict, old_complete: dict, old_ledger: dict,
          k24: dict, r8prime: dict, interface: dict) -> dict:
    validate_referee(referee)
    if old_direct.get("full_charge_scaled") != 16063392514918326062284800 or old_direct.get("irreducible_charge_scaled") != 11242374337962763694899200:
        fail("historical raw direct result")
    old_direct_scale = int(old_direct["scale"])
    if old_direct_scale != 79_412_096_674_310_400:
        fail("historical direct scale")
    if old_direct["full_charge_scaled"] // old_direct_scale != 202278912 or old_direct["irreducible_charge_scaled"] // old_direct_scale != 141570048:
        fail("historical direct scalar decode")

    old_full = fraction(old_complete["K19"]["corrected_complete_24_path_total"]["full"])
    old_irr = fraction(old_complete["K19"]["corrected_complete_24_path_total"]["irreducible"])
    corrected_full = old_full - 27_813_888
    corrected_irr = old_irr - 15_151_104
    if corrected_full != Fraction(-791_778_923_704_177_408, 57_955_975):
        fail("corrected complete K19 full")
    if corrected_irr != Fraction(-2_120_489_519_568_692_992, 173_867_925):
        fail("corrected complete K19 irreducible")

    if old_ledger.get("status") != "PASS_COMPLETE_FILTERED_CHARGE_LEDGER_THROUGH_K23":
        fail("old K23 ledger status")
    charges = {key: fraction(value) for key, value in old_ledger["charges"].items()}
    if charges["K19"] != old_irr:
        fail("old ledger/complete K19 linkage")
    charges["K19"] = corrected_irr
    if int(k24["scale_U"]) != U or k24["coverage"]["exact_set_equality"] is not True:
        fail("K24 exact result scope/U")
    charges["K24"] = Fraction(int(k24["actual_K24_scaled_U"]), U)

    cumulative = Fraction(0)
    cumulatives = {}
    for degree in range(14, 25):
        key = f"K{degree}"
        cumulative += charges[key]
        if degree >= 19:
            cumulatives[f"through_{key}"] = render(cumulative)
    if cumulative != 4_564_224:
        fail("corrected K14-through-K24 total")
    old_total = fraction(k24["cumulative_K14_through_K24"])
    if old_total != 19_715_328 or cumulative != old_total - 15_151_104:
        fail("old/new cumulative delta")
    raw_packet_total = referee["all_27_direct_packets"]["total_charge"]
    if cumulative != raw_packet_total:
        fail("filtered ledger does not conserve corrected raw packet charge")

    if r8prime.get("status") != "UNAUDITED exact-Q sparse K8 representative with full pivot replay" or r8prime.get("residual_K_degree") != 8:
        fail("R8prime cutoff representative")
    guard = interface.get("scope_guard", "")
    if "T=R8' mod (I_mix+K^9)" not in guard or "can have a K9 tail" not in guard or "separate full-column expansion" not in guard:
        fail("R8prime omitted-K9 interface guard")
    if interface.get("target_total_degree") != 24 or interface.get("target_K_degree") != 8:
        fail("R8prime interface degrees")

    corrected_target_k24_q = -sum(charges[f"K{i}"] for i in range(14, 24))
    if corrected_target_k24_q != Fraction(832_059_102_095_222_912, 173_867_925):
        fail("conditional corrected K24 zero target")
    target_scaled = corrected_target_k24_q * U
    if target_scaled.denominator != 1 or target_scaled.numerator != 1_917_064_171_227_393_589_248:
        fail("conditional corrected K24 scaled target")
    remaining_scaled = cumulative * U
    if remaining_scaled != 1_828_390_247_689_420_800:
        fail("remaining scaled packet charge")

    return {
        "status": "PASS_CORRECTED_K19_THROUGH_K24_LEDGER_CONSERVES_TRUNCATED_R8PRIME_PACKET_EXACTLY",
        "scale_U": str(U),
        "corrected_direct_K19": {
            "full": 174465024, "irreducible": 126418944,
            "pivotable": 48046080, "full_evaluations": 167616000,
            "irreducible_evaluations": 55872000,
        },
        "corrected_complete_K19_24_path": {"full": render(corrected_full), "irreducible": render(corrected_irr)},
        "corrected_charges": {key: render(value) for key, value in charges.items()},
        "corrected_cumulative_ledgers": cumulatives,
        "conditional_zero_K24_target_after_K19_fix": {"charge": render(corrected_target_k24_q), "scaled_U": str(target_scaled.numerator)},
        "actual_K24": {"charge": render(charges["K24"]), "scaled_U": k24["actual_K24_scaled_U"]},
        "actual_minus_conditional_zero_target": {"charge": render(cumulative), "scaled_U": str(remaining_scaled.numerator)},
        "raw_27_packet_charge": render(Fraction(raw_packet_total)),
        "conservation_against_actual_input": {
            "corrected_K14_through_K24_equals_raw_27_packet_charge": True,
            "unexplained_residual": render(Fraction(0)),
            "meaning": "After the K19 fix, every retained filtered page together carries exactly the charge of the actual truncated -R8prime*E0*E1*E2 input.",
        },
        "interface_classification": {
            "remaining_4564224_is_sign_error": False,
            "remaining_4564224_is_transition_error": False,
            "remaining_4564224_is_expected_raw_packet_charge": True,
            "zero_charge_applies_to_this_truncated_R8prime_packet": False,
            "reason": "R8prime is only the K8 cutoff-nine representative T=R8prime mod (I_mix+K^9); the source explicitly warns that an omitted K9 tail requires a separate full-column expansion.",
            "required_omitted_correction_charge_to_lift_to_zero_charge_aT": -4_564_224,
            "required_only_not_computed": True,
        },
        "scope": "Corrected exact scalar ledgers only. K20-K24 producer charges are unchanged. This identifies the remaining scalar with the actual truncated input and does not compute the omitted K9+ lift, membership, or a conjecture verdict.",
        "source_pins": {name: {"path": path, "sha256": (expected if expected is not None else sha(ROOT / path))} for name, (path, expected) in FILES.items()},
        "python_optimize": sys.flags.optimize,
    }


def expect_fail(label: str, fn) -> dict:
    try:
        fn()
    except (ValueError, KeyError, TypeError, ZeroDivisionError) as exc:
        return {"case": label, "rejected": True, "error": str(exc)}
    fail(f"hostile accepted: {label}")


def self_test(values: dict[str, dict]) -> dict:
    cases = []
    mutations = []
    x = copy.deepcopy(values); x["referee"]["corrected_replay"]["irreducible_charge"] += 1; mutations.append(("wrong_K19_irreducible", x))
    x = copy.deepcopy(values); x["referee"]["corrected_minus_historical"]["pivotable_charge"] += 1; mutations.append(("wrong_transition_delta", x))
    x = copy.deepcopy(values); x["referee"]["all_27_direct_packets"]["total_charge"] = 0; mutations.append(("forced_zero_packet", x))
    x = copy.deepcopy(values); x["old_through_k23"]["charges"]["K19"]["numerator"] += 1; mutations.append(("stale_K19_ledger_link", x))
    x = copy.deepcopy(values); x["k24"]["actual_K24_scaled_U"] = str(int(x["k24"]["actual_K24_scaled_U"]) + 1); mutations.append(("wrong_K24_scalar", x))
    x = copy.deepcopy(values); x["r8prime_interface"]["scope_guard"] = "complete exact target"; mutations.append(("erased_K9_scope_guard", x))
    for label, item in mutations:
        cases.append(expect_fail(label, lambda item=item: audit(item["referee"], item["old_direct"], item["old_complete_k19"], item["old_through_k23"], item["k24"], item["r8prime"], item["r8prime_interface"])))
    return {"status": "PASS_CORRECTED_K19_LEDGER_HOSTILES", "cases": cases, "cases_passed": len(cases), "python_optimize": sys.flags.optimize}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--output", type=Path, default=HERE / "results_corrected_k19_through_k24_ledgers.json")
    args = parser.parse_args()
    values = {name: load(name) for name in FILES}
    result = self_test(values) if args.self_test else audit(values["referee"], values["old_direct"], values["old_complete_k19"], values["old_through_k23"], values["k24"], values["r8prime"], values["r8prime_interface"])
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
