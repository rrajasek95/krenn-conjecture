#!/usr/bin/env python3
"""Fail-closed static audit of every support_cap occurrence in frozen D12 v4.1."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / "computations/unaudited-codex-n8-affine251-d12-hierarchical-v4-rare-index-2026-08-25/sealed_v4_1/main.rs"
OUTPUT = HERE / "results_static_support_cap_audit.json"
EXPECTED_SOURCE_SHA256 = "3139689fb546aa1233a366e2dfa1dc007ea2f13399b89c951181d28636f43f59"


def need(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit("REJECT: " + message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


source = SOURCE.read_text()
need(sha256(SOURCE) == EXPECTED_SOURCE_SHA256, "frozen source SHA")
lines = source.splitlines()
occurrence_lines = [index + 1 for index, line in enumerate(lines) if "support_cap" in line]
cli_flag_lines = [index + 1 for index, line in enumerate(lines) if "--support-cap" in line]
need(occurrence_lines == [1630, 1728, 1766, 1797, 3188, 3783], "complete occurrence line census")
need(cli_flag_lines == [1729], "CLI flag line census")
need(source.count("support_cap") == 7, "support_cap token census")
need(source.count("config.support_cap") == 2, "config.support_cap use census")
need(source.count('values\n        .get("--support-cap")') == 1, "CLI parse occurrence")
need(source.count('writeln!(out, "  \\"support_cap\\": {},", config.support_cap)') == 1, "result serialization occurrence")
need(source.count("if next.len() > config.support_cap {") == 1, "sole semantic guard")

markers = {
    "loop_top_gate": "if let Err(reason) = gate.check() {",
    "round_cap_guard": "if completed_rounds >= config.round_cap {",
    "column_cap_guard": "if columns.len() + new_columns.len() > config.column_cap {",
    "materialize": "let values =\n            parallel_invariant_columns(&provider, &new_columns, config.prime, config.workers);",
    "columns_extend": "columns.extend(new_columns.iter().copied());",
    "deterministic_choice": "let Some((next, selected_strategy, selected_pivot)) = choices.into_iter().next() else {",
    "support_guard": "if next.len() > config.support_cap {",
    "candidate_commit": "candidate = next;",
    "round_commit": "completed_rounds += 1;",
}
positions = {name: source.index(text) for name, text in markers.items()}
need(
    positions["loop_top_gate"]
    < positions["round_cap_guard"]
    < positions["column_cap_guard"]
    < positions["materialize"]
    < positions["columns_extend"]
    < positions["deterministic_choice"]
    < positions["support_guard"]
    < positions["candidate_commit"]
    < positions["round_commit"],
    "guard timing order",
)

guard_start = positions["support_guard"]
guard_end = positions["candidate_commit"]
guard_block = source[guard_start:guard_end]
need("sparse_write_checkpoint(" in guard_block, "guard writes checkpoint")
need("&columns," in guard_block and "&candidate," in guard_block, "guard checkpoint state")
need("sparse_maybe_write_vectors(" in guard_block, "guard writes materialized vector cache")
need('"INCOMPLETE_SEARCH_CAP"' in guard_block and 'Some("SUPPORT_CAP")' in guard_block, "guard result status")
need("columns.len()," in guard_block and "next.len()," in guard_block, "guard result censuses")
need("candidate = next;" not in guard_block and "completed_rounds += 1;" not in guard_block, "no candidate/round commit before return")
need("return;" in guard_block, "guard returns")

result = {
    "schema": "KRENN_AFFINE251_D12_SUPPORT_CAP_STATIC_SOURCE_AUDIT_V1",
    "status": "PASS_SUPPORT_CAP_SINGLE_POST_SOLVE_PRE_CANDIDATE_GUARD",
    "source": str(SOURCE.relative_to(ROOT)),
    "source_sha256": EXPECTED_SOURCE_SHA256,
    "occurrence_census": {
        "support_cap_tokens": 7,
        "config_support_cap_uses": 2,
        "lines": occurrence_lines,
        "cli_flag_lines": cli_flag_lines,
        "roles": [
            "configuration struct field",
            "parsed local binding associated with the sole CLI --support-cap lookup",
            "minimum-value validation",
            "configuration construction",
            "result serialization key literal",
            "result serialization configuration read",
            "sole semantic next-support guard configuration read",
        ],
    },
    "sole_semantic_guard": {
        "expression": "next.len() > config.support_cap",
        "strict_comparison": True,
        "timing": "after new-column enumeration/materialization, exposed-frequency update, elimination/backsolve/verification, and deterministic next choice; before candidate=next and completed_rounds+=1",
        "candidate_committed_on_failure": False,
        "round_committed_on_failure": False,
        "columns_and_vectors_already_extended_on_failure": True,
        "failure_writes_checkpoint_and_vector_cache": True,
        "failure_status": "INCOMPLETE_SEARCH_CAP/SUPPORT_CAP",
    },
    "mathematical_noninterference": {
        "support_cap_not_read_by": [
            "provider parsing or fingerprinting",
            "incident enumeration",
            "invariant-column arithmetic",
            "rare-order ranking",
            "hierarchical elimination",
            "backsolve",
            "verification",
            "choice ordering",
        ],
        "higher_cap_same_source_provider_math": True,
        "condition": "Commands differ only in support-cap after independently fixing all other source/binary/provider/mode/resource literals.",
    },
    "lower_cap_control": {
        "can_witness_next_support_exceeds_cap": True,
        "can_be_byte_unchanged": False,
        "safe_only_as_isolated_quarantined_diagnostic_clone": True,
        "may_be_resumed_or_promoted": False,
        "reason": "The guard runs after new columns and vectors have been materialized and inserted, so failure writes a hybrid checkpoint/cache with old candidate and round but extended columns/vector cache.",
        "recommendation": "Do not run a lower-cap control; use this exact source theorem plus a fresh higher-cap candidate and strict descendant/full replay.",
    },
}

temporary = OUTPUT.with_suffix(".json.tmp")
temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
os.replace(temporary, OUTPUT)
print(json.dumps({"status": result["status"], "occurrences": occurrence_lines}, sort_keys=True))
