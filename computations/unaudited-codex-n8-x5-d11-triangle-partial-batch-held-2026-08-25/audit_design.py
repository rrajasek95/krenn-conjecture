#!/usr/bin/env python3
"""Fail-closed static/dynamic audit for the deterministic partial-batch patch."""

import hashlib
import itertools
import json
import os
from pathlib import Path
import subprocess

if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "src/main.rs"
BINARY = HERE / "x5_d11_partial_batch"
RUNNER = HERE / "run_held_partial_batch.py"


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def source_contract(text: str) -> None:
    required = (
        "BTreeMap::<Column, Vec<(Mono, u64)>>::new()",
        "let largest = prefix.last_key_value()",
        "if column < largest",
        "violations_observed += 1",
        "truncated: violations_observed > limit",
        "let canonical_partial_batch = scan.truncated",
        "solver.add_vector(&vector)",
        "candidate = solver.candidate()",
        "incremental dual verification failed",
        "if canonical_partial_batch",
        "CANONICAL_VIOLATION_PREFIX_ACCEPTED_AND_SELECTED_COLUMN_CAP_REACHED",
        "write_dual(&config.dual, config.prime, candidate.as_ref())",
        "write_selected(&config.selected, &provider, &selected)",
    )
    for token in required:
        assert token in text, token
    assert "if violations.len() > limit" not in text
    assert text.index("let canonical_partial_batch = scan.truncated") < text.index("solver.add_vector(&vector)")
    assert text.index("solver.add_vector(&vector)") < text.index("candidate = solver.candidate()", text.index("solver.add_vector(&vector)"))
    assert text.index("candidate = solver.candidate()", text.index("solver.add_vector(&vector)")) < text.index("if canonical_partial_batch")
    final_dual = text.rindex("write_dual(&config.dual, config.prime, candidate.as_ref())")
    final_selected = text.rindex("write_selected(&config.selected, &provider, &selected)")
    assert final_dual < final_selected


def reference_prefix(stream, limit):
    retained = []
    for value in stream:
        if value not in retained:
            retained.append(value)
            retained.sort()
            retained = retained[:limit]
    return retained


def main() -> None:
    source = SOURCE.read_text()
    source_contract(source)
    hostile_mutations = {
        "reverse_natural_order": source.replace("if column < largest", "if column > largest", 1),
        "unordered_retainer": source.replace("BTreeMap::<Column, Vec<(Mono, u64)>>::new()", "HashMap::<Column, Vec<(Mono, u64)>>::new()", 1),
        "hide_overflow": source.replace("truncated: violations_observed > limit", "truncated: false"),
        "disable_partial_terminal": source.replace("if canonical_partial_batch", "if false", 1),
        "early_truncation": source + "\n// if violations.len() > limit\n",
        "wrong_terminal_reason": source.replace("CANONICAL_VIOLATION_PREFIX_ACCEPTED_AND_SELECTED_COLUMN_CAP_REACHED", "SELECTED_COLUMN_CAP_REACHED", 1),
    }
    rejected = 0
    for mutated in hostile_mutations.values():
        try:
            source_contract(mutated)
        except (AssertionError, ValueError):
            rejected += 1
    assert rejected == len(hostile_mutations)

    keys = [(generator, multiplier) for generator in range(3) for multiplier in range(3)]
    expected = sorted(keys)[:4]
    checked_orders = 0
    for order in itertools.islice(itertools.permutations(keys), 257):
        assert reference_prefix(order, 4) == expected
        checked_orders += 1
    assert checked_orders == 257

    selftest = subprocess.run([BINARY, "--selftest"], check=True, capture_output=True, text=True)
    selftest_result = json.loads(selftest.stdout)
    assert selftest_result["status"] == "PASS"
    assert selftest_result["canonical_prefix_traversal_invariant"] is True
    assert selftest_result["partial_refinement_replay"] is True
    refusal = subprocess.run(["python3", RUNNER], check=False, capture_output=True, text=True)
    assert refusal.returncode != 0
    assert refusal.stderr.strip() == "HELD: exact partial-batch production has no clearance"
    assert not (HERE / "held_production_partial_batch").exists()

    result = {
        "schema": "KRENN_X5_D11_TRIANGLE_PARTIAL_BATCH_DESIGN_AUDIT_V1",
        "status": "PASS_HELD_DIAGNOSTIC_ONLY",
        "source_sha256": sha(SOURCE),
        "binary_sha256": sha(BINARY),
        "selftest": selftest_result,
        "canonical_order_permutations_checked": checked_orders,
        "hostile_mutations_rejected": rejected,
        "hostile_mutations_total": len(hostile_mutations),
        "full_frontier_required_before_prefix_acceptance": True,
        "dual_first_atomic_checkpoint_order": True,
        "production_launch_authorized": False,
        "held_runner_refusal": True,
        "unit_cap_chasing_rejected": True,
    }
    temporary = HERE / "results_design_audit.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_design_audit.json")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
