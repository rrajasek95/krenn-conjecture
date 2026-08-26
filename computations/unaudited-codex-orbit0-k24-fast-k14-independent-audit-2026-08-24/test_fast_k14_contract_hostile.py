#!/usr/bin/env python3
"""Hostile mutations for the independent fast-K14 raw-result validator."""

import copy
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FAST = HERE.parent / "unaudited-codex-orbit0-k24-charge-only-fast-prototype-2026-08-24"

audit_spec = importlib.util.spec_from_file_location("fast_k14_audit", HERE / "audit_fast_k14_against_sealed.py")
audit = importlib.util.module_from_spec(audit_spec)
audit_spec.loader.exec_module(audit)
legacy_spec = importlib.util.spec_from_file_location("legacy_k14_validator", FAST / "validate_k14_source.py")
legacy = importlib.util.module_from_spec(legacy_spec)
legacy_spec.loader.exec_module(legacy)

GOOD_PATH = HERE / "fast_exact_record0.json"
GOOD = json.loads(GOOD_PATH.read_text())


def strict_reject(name, mutate):
    value = copy.deepcopy(GOOD)
    mutate(value)
    try:
        audit.validate_raw(value, GOOD_PATH)
    except (RuntimeError, KeyError, TypeError, ValueError):
        return name
    raise RuntimeError("strict validator accepted hostile " + name)


def legacy_accepts(mutate):
    value = copy.deepcopy(GOOD)
    mutate(value)
    try:
        legacy.validate(value)
    except (AssertionError, KeyError, TypeError, ValueError):
        return False
    return True


MUTATIONS = [
    ("extra_top", lambda x: x.__setitem__("untrusted", 1)),
    ("wrong_status", lambda x: x.__setitem__("status", "PASS")),
    ("duplicate_id", lambda x: x["covered_lineage_ids"].__setitem__(1, audit.IDS[0])),
    ("interval_count_mismatch", lambda x: x.__setitem__("R8_records_consumed", 2)),
    ("wrong_source_heads", lambda x: x.__setitem__("source_heads", 1)),
    ("wrong_source_mass", lambda x: x.__setitem__("source_mass_sum", "0")),
    ("full_irr_scalar", lambda x: x["sinks"][audit.IDS[0]].__setitem__("irreducible_charge_scaled_U", "0")),
    ("product_hist_cardinality", lambda x: x["sinks"][audit.IDS[0]]["product_denominator_hist"].__setitem__("3", 0)),
    ("inexact_U_division", lambda x: x["sinks"][audit.IDS[0]]["product_denominator_hist"].__setitem__("37", x["sinks"][audit.IDS[0]]["product_denominator_hist"].pop("3"))),
    ("abstract_literal_guard_false", lambda x: x["literal_sample_guard"].__setitem__("all_abstract_literal_cycle_keys_equal", False)),
    ("sample_count_wrong", lambda x: x["literal_sample_guard"].__setitem__("records", 0)),
    ("sample_ledger_detached", lambda x: x["literal_sample_guard"].__setitem__("ledger", "/tmp/not-the-result-ledger.tsv")),
    ("negative_cache_clears", lambda x: x["sinks"][audit.IDS[0]]["terminal_profile_cache"].__setitem__("clears_at_hard_cap", -1)),
    ("resource_peak_over_cap", lambda x: x["terminal_cache_resource_guard"].__setitem__("peak_keys_per_worker", 3_000_001)),
    ("elapsed_over_gate", lambda x: x.__setitem__("elapsed_seconds", 600.0)),
]

rejected = [strict_reject(name, mutate) for name, mutate in MUTATIONS]
legacy_false_accepts = [name for name, mutate in MUTATIONS if legacy_accepts(mutate)]

need_legacy_false_accepts = {
    "extra_top", "wrong_status", "interval_count_mismatch", "wrong_source_mass",
    "product_hist_cardinality", "abstract_literal_guard_false", "sample_count_wrong",
    "sample_ledger_detached", "negative_cache_clears", "resource_peak_over_cap",
    "elapsed_over_gate",
}
if not need_legacy_false_accepts.issubset(set(legacy_false_accepts)):
    raise RuntimeError("legacy weakness set changed: " + repr(legacy_false_accepts))

print(json.dumps({
    "status": "PASS_HOSTILE_FAST_K14_RAW_RESULT_CONTRACT",
    "strict_rejected": rejected,
    "strict_rejected_count": len(rejected),
    "legacy_validator_false_accepts": legacy_false_accepts,
    "legacy_validator_false_accept_count": len(legacy_false_accepts),
}, sort_keys=True))
