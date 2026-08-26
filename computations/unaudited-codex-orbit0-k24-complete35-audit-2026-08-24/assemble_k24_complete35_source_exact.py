#!/usr/bin/env python3
"""Fail-closed, source-extracting exact assembler for the frozen 35-ID K24 DAG."""

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
MANIFEST = HERE / "k24_complete35_source_manifest.json"
OUT = HERE / "results_k24_complete35_exact.json"
U = 400_591_699_200

MANIFEST_KEYS = {
    "schema", "degree", "scale_U", "expected_charge_sign", "grouped_scalar_once",
    "expected_groups_path", "expected_groups_sha256", "prior_ledger_path",
    "prior_ledger_sha256", "prior_ledger_referee_path", "prior_ledger_referee_sha256",
    "forced_k24_scaled_U", "groups",
}
GROUP_KEYS = {
    "group_id", "extractor", "raw_path", "raw_sha256", "raw_status",
    "acceptance_path", "acceptance_sha256", "acceptance_status",
}


def fail(msg: str) -> None:
    raise ValueError(msg)


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        fail(f"JSON object required: {path}")
    return value


def exact_keys(value: dict, expected: set[str], label: str) -> None:
    if set(value) != expected:
        fail(f"{label} keys mismatch: missing={sorted(expected-set(value))}, extra={sorted(set(value)-expected)}")


def rational_record(value: Fraction) -> dict:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "text": f"{value.numerator}/{value.denominator}",
    }


def select_payload(group_id: str, extractor: str, raw: dict) -> tuple[dict, list[str] | None]:
    if extractor == "flat":
        ids = raw.get("ids")
        if ids is None and isinstance(raw.get("strict_id"), str):
            ids = [raw["strict_id"]]
        payload = raw
    elif extractor == "sink":
        ids = raw.get("covered_lineage_ids")
        payload = raw.get("sink")
    elif extractor == "k14_sink_334":
        ids = ["D14:222|R:3-3-4"]
        payload = raw.get("sinks", {}).get("D14:222|R:3-3-4")
    elif extractor == "k14_sink_424":
        ids = ["D14:222|R:4-2-4"]
        payload = raw.get("sinks", {}).get("D14:222|R:4-2-4")
    elif extractor == "k15_sink_234":
        payload = raw.get("sinks", {}).get("D15:{223,232,322}|R:2-3-4")
        ids = payload.get("ids") if isinstance(payload, dict) else None
    elif extractor == "k15_sink_324":
        payload = raw.get("sinks", {}).get("D15:{223,232,322}|R:3-2-4")
        ids = payload.get("ids") if isinstance(payload, dict) else None
    elif extractor == "direct_group_D17":
        payload = next((g for g in raw.get("groups", []) if g.get("group_id") == group_id), None)
        ids = payload.get("ids") if isinstance(payload, dict) else None
    elif extractor == "direct_group_D18":
        payload = next((g for g in raw.get("groups", []) if g.get("group_id") == group_id), None)
        ids = payload.get("ids") if isinstance(payload, dict) else None
    else:
        fail(f"unknown extractor: {extractor}")
    if not isinstance(payload, dict):
        fail(f"missing source payload for {group_id}")
    return payload, ids


def payload_numbers(payload: dict) -> tuple[int, int, int, int]:
    full_scaled = payload.get("full_charge_scaled_U")
    irr_scaled = payload.get("irreducible_charge_scaled_U")
    full = payload.get("full_occurrences")
    irr = payload.get("irreducible_occurrences")
    if any(isinstance(x, bool) or not isinstance(x, (str, int)) for x in (full_scaled, irr_scaled, full, irr)):
        fail("scalar/count fields must be decimal strings or integers")
    try:
        return int(full_scaled), int(irr_scaled), int(full), int(irr)
    except Exception as exc:
        fail(f"invalid scalar/count integer: {exc}")


def validate_payload(group_id: str, payload: dict, ids: list[str] | None,
                     expected_ids: list[str], expected_sign: str) -> dict:
    if ids != expected_ids:
        fail(f"{group_id}: source IDs mismatch")
    fs, irs, full, irr = payload_numbers(payload)
    if fs != irs or full != irr:
        fail(f"{group_id}: full/irreducible identity failed")
    if full <= 0:
        fail(f"{group_id}: non-positive occurrence count")
    if expected_sign != "positive" or fs <= 0:
        fail(f"{group_id}: expected positive charge sign")
    return {
        "ids": ids,
        "full_scaled_U": str(fs),
        "irreducible_scaled_U": str(irs),
        "full_occurrences": full,
        "irreducible_occurrences": irr,
        "charge": rational_record(Fraction(fs, U)),
    }


def assemble(manifest: dict) -> dict:
    exact_keys(manifest, MANIFEST_KEYS, "manifest")
    if manifest["schema"] != "k24_complete35_source_manifest_v1" or manifest["degree"] != 24:
        fail("manifest schema/degree mismatch")
    if manifest["scale_U"] != str(U):
        fail("manifest U mismatch")
    if manifest["expected_charge_sign"] != "positive":
        fail("manifest sign guard mismatch")
    if manifest["grouped_scalar_once"] is not True:
        fail("grouped-scalar-once guard missing")

    expected_path = ROOT / manifest["expected_groups_path"]
    if sha(expected_path) != manifest["expected_groups_sha256"]:
        fail("expected-group contract hash mismatch")
    expected_doc = load_json(expected_path)
    if expected_doc.get("degree") != 24 or int(expected_doc.get("scale_U", 0)) != U:
        fail("expected-group contract degree/U mismatch")
    expected = expected_doc.get("groups")
    if not isinstance(expected, dict) or len(expected) != 10:
        fail("expected exactly ten scalar groups")

    specs = manifest["groups"]
    if not isinstance(specs, list):
        fail("manifest groups must be a list")
    for i, spec in enumerate(specs):
        if not isinstance(spec, dict):
            fail(f"group spec {i} not an object")
        exact_keys(spec, GROUP_KEYS, f"group spec {i}")
    group_ids = [s["group_id"] for s in specs]
    if len(group_ids) != len(set(group_ids)):
        fail("duplicate scalar group")
    if set(group_ids) != set(expected):
        fail(f"group set mismatch: missing={sorted(set(expected)-set(group_ids))}, extra={sorted(set(group_ids)-set(expected))}")

    ledger = []
    seen_ids: list[str] = []
    total_scaled = 0
    for spec in specs:
        group_id = spec["group_id"]
        raw_path = ROOT / spec["raw_path"]
        acceptance_path = ROOT / spec["acceptance_path"]
        if sha(raw_path) != spec["raw_sha256"]:
            fail(f"{group_id}: raw evidence hash mismatch")
        if sha(acceptance_path) != spec["acceptance_sha256"]:
            fail(f"{group_id}: acceptance hash mismatch")
        raw = load_json(raw_path)
        acceptance = load_json(acceptance_path)
        if raw.get("status") != spec["raw_status"]:
            fail(f"{group_id}: raw status mismatch")
        if acceptance.get("status") != spec["acceptance_status"]:
            fail(f"{group_id}: acceptance status mismatch")
        if str(raw.get("scale_U")) != str(U):
            fail(f"{group_id}: raw U mismatch")

        payload, ids = select_payload(group_id, spec["extractor"], raw)
        entry = validate_payload(group_id, payload, ids, expected[group_id], manifest["expected_charge_sign"])
        if len(expected[group_id]) > 1:
            if payload.get("individual_id_charges", None) is not None:
                fail(f"{group_id}: grouped scalar was split across IDs")
            if group_id.startswith("source_D15_") and raw.get("grouped_scalar_once") is not True:
                fail(f"{group_id}: K15 grouped-once evidence missing")
            if group_id.startswith("source_D16_") and "only the grouped six-ID scalar is source-faithful" not in raw.get("packet_grouping_guard", ""):
                fail(f"{group_id}: K16 grouped-once evidence missing")
        entry.update({
            "group_id": group_id,
            "raw_evidence": {"path": spec["raw_path"], "sha256": spec["raw_sha256"]},
            "acceptance": {"path": spec["acceptance_path"], "sha256": spec["acceptance_sha256"]},
            "extractor": spec["extractor"],
            "grouped_scalar_counted": 1,
        })
        ledger.append(entry)
        seen_ids.extend(ids)
        total_scaled += int(entry["full_scaled_U"])

    if len(seen_ids) != 35 or len(set(seen_ids)) != 35:
        fail("assembled IDs are not exactly 35 unique IDs")
    expected_ids = [item for group in expected.values() for item in group]
    if set(seen_ids) != set(expected_ids):
        fail("assembled ID set differs from frozen 35-ID contract")

    prior_path = ROOT / manifest["prior_ledger_path"]
    prior_ref_path = ROOT / manifest["prior_ledger_referee_path"]
    if sha(prior_path) != manifest["prior_ledger_sha256"] or sha(prior_ref_path) != manifest["prior_ledger_referee_sha256"]:
        fail("prior ledger/referee hash mismatch")
    prior = load_json(prior_path)
    prior_q = Fraction(prior["cumulative_K14_through_K23"]["numerator"], prior["cumulative_K14_through_K23"]["denominator"])
    forced_q = Fraction(prior["necessary_K24_aggregate_charge_under_conservation"]["numerator"], prior["necessary_K24_aggregate_charge_under_conservation"]["denominator"])
    forced_scaled = int(manifest["forced_k24_scaled_U"])
    if forced_q * U != forced_scaled or forced_q != -prior_q:
        fail("forced target is not exactly the pinned negative prior ledger")
    actual_q = Fraction(total_scaled, U)
    residual_q = prior_q + actual_q
    residual_scaled = total_scaled - forced_scaled
    if residual_q * U != residual_scaled:
        fail("scaled/rational residual identity failed")

    return {
        "status": "PASS_COMPLETE_K24_35_ID_SOURCE_EXTRACTED_ASSEMBLY_WITH_NONZERO_CONSERVATION_RESIDUAL",
        "degree": 24,
        "scale_U": str(U),
        "coverage": {
            "expected_groups": 10, "assembled_groups": 10,
            "expected_ids": 35, "assembled_ids": 35,
            "missing_groups": [], "extra_groups": [], "duplicate_groups": [],
            "missing_ids": [], "extra_ids": [], "duplicate_ids": [],
            "exact_set_equality": True,
        },
        "grouped_scalar_semantics": "each source group is extracted from its pinned raw evidence and counted exactly once; no group scalar is multiplied by its ID count",
        "groups": ledger,
        "actual_K24_scaled_U": str(total_scaled),
        "actual_K24_charge": rational_record(actual_q),
        "forced_K24_scaled_U": str(forced_scaled),
        "forced_K24_charge": rational_record(forced_q),
        "actual_minus_forced_scaled_U": str(residual_scaled),
        "actual_minus_forced_charge": rational_record(actual_q - forced_q),
        "cumulative_K14_through_K24": rational_record(residual_q),
        "zero_conservation_matches": residual_q == 0,
        "prior_ledger": {"path": manifest["prior_ledger_path"], "sha256": manifest["prior_ledger_sha256"]},
        "prior_ledger_referee": {"path": manifest["prior_ledger_referee_path"], "sha256": manifest["prior_ledger_referee_sha256"]},
        "scope": "Exact K24 charge assembly over the frozen 35-ID/10-group DAG. This result does not by itself certify the global recurrence/source-column partition required by the conditional zero-charge theorem, terminal span, membership, or a conjecture verdict.",
        "conjecture_claim_authorized": False,
    }


def expect_fail(label: str, fn) -> dict:
    try:
        fn()
    except (ValueError, KeyError, TypeError, FileNotFoundError) as exc:
        return {"case": label, "rejected": True, "error": str(exc)}
    fail(f"hostile case was accepted: {label}")


def self_test(manifest: dict) -> dict:
    cases = []
    mutations = []
    m = copy.deepcopy(manifest); m["groups"].pop(); mutations.append(("missing_group", m))
    m = copy.deepcopy(manifest); m["groups"].append(copy.deepcopy(m["groups"][0])); mutations.append(("duplicate_group", m))
    m = copy.deepcopy(manifest); m["groups"][0]["group_id"] = "hostile_extra"; mutations.append(("extra_group", m))
    m = copy.deepcopy(manifest); m["grouped_scalar_once"] = False; mutations.append(("grouped_once_false", m))
    m = copy.deepcopy(manifest); m["scale_U"] = str(U + 1); mutations.append(("wrong_U", m))
    m = copy.deepcopy(manifest); m["expected_charge_sign"] = "negative"; mutations.append(("wrong_sign_contract", m))
    m = copy.deepcopy(manifest); m["groups"][0]["raw_sha256"] = "0" * 64; mutations.append(("wrong_raw_hash", m))
    m = copy.deepcopy(manifest); m["forced_k24_scaled_U"] = str(-int(m["forced_k24_scaled_U"])); mutations.append(("forced_sign_flip", m))
    for label, hostile in mutations:
        cases.append(expect_fail(label, lambda hostile=hostile: assemble(hostile)))

    spec = manifest["groups"][0]
    raw = load_json(ROOT / spec["raw_path"])
    payload, ids = select_payload(spec["group_id"], spec["extractor"], raw)
    p = copy.deepcopy(payload); p["irreducible_charge_scaled_U"] = str(int(p["full_charge_scaled_U"]) + 1)
    cases.append(expect_fail("full_irreducible_scalar_mismatch", lambda: validate_payload(spec["group_id"], p, ids, ids, "positive")))
    p = copy.deepcopy(payload); p["irreducible_occurrences"] = int(p["full_occurrences"]) + 1
    cases.append(expect_fail("full_irreducible_count_mismatch", lambda: validate_payload(spec["group_id"], p, ids, ids, "positive")))
    p = copy.deepcopy(payload); p["full_charge_scaled_U"] = str(-int(p["full_charge_scaled_U"])); p["irreducible_charge_scaled_U"] = p["full_charge_scaled_U"]
    cases.append(expect_fail("negative_group_sign", lambda: validate_payload(spec["group_id"], p, ids, ids, "positive")))
    cases.append(expect_fail("source_ID_mismatch", lambda: validate_payload(spec["group_id"], payload, ["hostile"], ids, "positive")))
    assemble(manifest)
    return {"status": "PASS_K24_COMPLETE35_HOSTILE_SELFTEST", "python_optimize": sys.flags.optimize, "cases": cases, "cases_passed": len(cases)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--output", type=Path, default=OUT)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    manifest = load_json(args.manifest)
    result = self_test(manifest) if args.self_test else assemble(manifest)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
