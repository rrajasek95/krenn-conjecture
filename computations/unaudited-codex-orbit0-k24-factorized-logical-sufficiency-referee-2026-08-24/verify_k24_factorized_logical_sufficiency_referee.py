#!/usr/bin/env python3
"""Read-only fail-closed verifier for the K24 logical sufficiency theorem."""
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RESULT = HERE / "results_k24_factorized_logical_sufficiency_referee.json"
PATHS = {
    "factorized_gate_report_sha256": ROOT / "computations/unaudited-codex-orbit0-k24-residual-direct-d17-d18-gate-2026-08-24/REPORT.md",
    "factorized_interface_schema_sha256": ROOT / "computations/unaudited-codex-orbit0-k24-residual-direct-d17-d18-gate-2026-08-24/factorized_k24_residual_interface.schema.json",
    "terminal_structure_report_sha256": ROOT / "computations/unaudited-codex-orbit0-k24-terminal-structure-2026-08-23/REPORT.md",
    "terminal_structure_result_sha256": ROOT / "computations/unaudited-codex-orbit0-k24-terminal-structure-2026-08-23/results_k24_terminal_structure.json",
    "filtered_reducer_report_sha256": ROOT / "computations/unaudited-codex-orbit0-filtered-k24-reducer-design-2026-08-23/REPORT.md",
    "filtered_reducer_result_sha256": ROOT / "computations/unaudited-codex-orbit0-filtered-k24-reducer-design-2026-08-23/results_filtered_k24_reducer_design.json",
    "gram_report_sha256": ROOT / "computations/unaudited-codex-orbit0-k24-factorized-gram-2026-08-23/REPORT.md",
    "gram_result_sha256": ROOT / "computations/unaudited-codex-orbit0-k24-factorized-gram-2026-08-23/results_k24_factorized_gram.json",
    "factorized_producer_report_sha256": ROOT / "computations/unaudited-codex-orbit0-k24-factorized-direct-d17-d18-producer-2026-08-24/REPORT.md",
    "canonical_order_audit_sha256": ROOT / "computations/unaudited-codex-orbit0-k24-factorized-direct-d17-d18-producer-2026-08-24/audit_fast_h_canonicalization_design.py",
    "canonical_order_witnesses_sha256": ROOT / "computations/unaudited-codex-orbit0-k24-factorized-direct-d17-d18-producer-2026-08-24/prefix1/literal_witnesses.tsv",
    "gram_provider_sha256": ROOT / "computations/unaudited-codex-orbit0-k24-factorized-gram-2026-08-23/k24_factorized_gram_provider.py",
}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_provider(path):
    spec = importlib.util.spec_from_file_location("logical_referee_provider", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    result = json.loads(RESULT.read_text())
    need(result["status"] == "PASS_READ_ONLY_K24_LOGICAL_SUFFICIENCY_REFEREE", "status")
    for key, path in PATHS.items():
        need(path.is_file() and sha(path) == result["source_pins"][key], f"source pin {key}")
    verdict = result["verdict"]
    need(verdict["complete_weighted_top_ledgers_alone_certify_terminal_relative_membership"] is False, "load-bearing no verdict")
    need(verdict["exact_top_ledger_equality_certifies_raw_projected_span_membership"] is True, "conditional raw yes")
    need(verdict["raw_top_gram_closure_repairs_missing_lower_lift"] is False, "raw Gram limitation")
    need(verdict["complete_gram_on_the_correct_relative_operator_can_decide_membership"] is True, "relative Gram role")
    theorem = result["theorem"]
    need("ker(L)" in theorem["correct_relative_operator"] and "image(A24_rel)" in theorem["criterion"], "relative operator theorem")
    # Exact one-dimensional counterexample: L=T=[1].  Raw top image is Q,
    # while ker(L)={0}, so the relative top image is {0} and excludes R=1.
    counterexample = theorem["counterexample"]
    need(counterexample["lower_matrix"] == [[1]] and counterexample["top_matrix"] == [[1]], "counterexample matrices")
    need(counterexample["residual_top"] == [1] and counterexample["raw_image_membership"] is True, "counterexample raw membership")
    need(counterexample["lower_kernel"] == "{0}" and counterexample["relative_image_membership"] is False, "counterexample relative failure")
    schema = json.loads(PATHS["factorized_interface_schema_sha256"].read_text())
    need("constructive_span_certificate" in schema["x-exact-semantics"], "schema claim located")
    terminal = json.loads(PATHS["terminal_structure_result_sha256"].read_text())
    need("relative cokernel" in terminal["exact_terminal_criterion"], "terminal relative criterion located")
    reducer = json.loads(PATHS["filtered_reducer_result_sha256"].read_text())
    need(reducer["recurrence"] == "after collection, a pivot at Kd emits K(d+2), K(d+3), K(d+4)", "triangular reducer")
    need(reducer["chosen_later_policy"] == "average all literal dividing mixed K0 pivots over each labelled H orbit", "frozen pivot policy")
    gram = json.loads(PATHS["gram_result_sha256"].read_text())
    need("COMPLETE" in gram["exact_H_Gram"]["membership"], "complete Gram guard")
    provider = load_provider(PATHS["gram_provider_sha256"])
    need(len(provider.H) == 384, "H order")
    lines = PATHS["canonical_order_witnesses_sha256"].read_text().splitlines()
    need(len(lines) == 258, "257 canonical witnesses")
    divergences = 0
    for line in lines[1:]:
        fields = line.split("\t")
        column = (tuple(map(int, fields[12])), bytes.fromhex(fields[13]))
        orbit = provider.column_orbit(column)
        recorded = provider.parse_column_key(fields[14])
        natural = min(orbit)
        need(recorded in orbit and recorded == natural, "producer natural representative")
        need(len(orbit) == int(fields[15]), "orbit size")
        divergences += orbit[0] != natural
    need(divergences == result["canonical_order_correction"]["repr_vs_natural_minimum_divergences"] == 228, "natural/repr divergence census")
    guard = result["publication_guard"]
    required = guard["required_before_constructive_terminal_PASS"]
    need(len(required) == len(set(required)) == 9, "publication guard key count")
    need("A24_rel" in guard["if_explicit_valid_x_absent"] and guard["fail_closed_status_without_all_guards"] == "REJECT_K24_CONSTRUCTIVE_SPAN_CERTIFICATE", "fail-closed relative Gram guard")
    print(json.dumps({
        "status": "PASS_K24_LOGICAL_SUFFICIENCY_REFEREE_REPLAY",
        "answer_load_bearing_terminal_claim": "NO",
        "conditional_raw_projection_answer": "YES_IF_EXACT_Tx_EQUALS_R24",
        "relative_operator": "A24_rel=T|ker(L)",
        "raw_gram_sufficient_for_lower_lift": False,
        "natural_repr_divergences_replayed": divergences,
        "source_pins_rehashed": len(PATHS),
        "heavy_run": False,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
