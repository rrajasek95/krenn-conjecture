#!/usr/bin/env python3
"""Independent strict audit of the complete grouped 59-ID K23 assembly."""

from __future__ import annotations

from collections import Counter
from contextlib import redirect_stdout
from fractions import Fraction
import hashlib
import importlib.util
import io
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
U = 400_591_699_200
ASSEMBLY = ROOT / "computations/unaudited-codex-orbit0-k23-direct-k15-production-interface-2026-08-24"
MANIFEST = ASSEMBLY / "k23_manifest_complete_59_of_59.json"
RESULT = ASSEMBLY / "results_k23_complete_59_of_59.json"
BASE47 = ROOT / "computations/unaudited-codex-orbit0-k23-d14-source-three-fold-2026-08-24/k23_manifest_current_47_of_59.json"
K15 = ASSEMBLY / "k23_direct_k15_fragment_manifest.json"
K15_AUDIT = ASSEMBLY / "results_k23_direct_k15_final_independent_audit.json"
ASSEMBLER = ROOT / "computations/unaudited-codex-orbit0-k23-availability-schedule-2026-08-24/assemble_k23_59_exact.py"
DAG = ROOT / "computations/unaudited-codex-orbit0-k14-k24-recurrence-dag-2026-08-23/results_recurrence_dag.json"
THROUGH22 = ROOT / "computations/unaudited-codex-orbit0-filtered-charge-ledger-through-k22-2026-08-24/results_charge_ledger_through_k22.json"
LEDGER = HERE / "results_charge_ledger_through_k23.json"
PINS = {
    MANIFEST: "940d3c97e8dc3d91e1b003d5d37cc3123aa7e97f3051b046b37be4a95a973fe0",
    RESULT: "ed8678d12c7ebd7a301951f9dfd9dc814a0f9dac8fd729086ad35143c916df7b",
    BASE47: "35089c36f649a5942c3203ce0f6b1c612aef9ce9dd741e159edeb946074b13b1",
    K15: "7b16c53e372282a02aaa054fcd1abc3bf45159c2e9c190ab7d1ed47ca6ec10b5",
    K15_AUDIT: "90ff932ff39ace3f54707061276d8b21f4f23232a8ae15422006c6add1deae22",
    ASSEMBLER: "b189ddf195af4e5e896aee495bf7adbc074af0108a4f026ae852fbbabaacbaaf",
    DAG: "469639f662682d3e39b5b9f2d1055e113826a93bd416dbdcb788881e9ffe44fa",
    THROUGH22: "2bddded61e04f7e789b633503ac40419833c00091fd1caa72b2092a99e066741",
}
GROUP_KEYS = {"group_id", "ids", "full_scaled_U", "irreducible_scaled_U",
              "full", "irreducible", "evidence_path", "evidence_sha256"}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def load_module():
    spec = importlib.util.spec_from_file_location("independent_k23_assembler", ASSEMBLER)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, "assembler loader")
    spec.loader.exec_module(module)
    return module


def main():
    for path, digest in PINS.items():
        require(path.is_file() and sha(path) == digest, f"hash pin {path}")
    manifest = json.loads(MANIFEST.read_text())
    result = json.loads(RESULT.read_text())
    dag = json.loads(DAG.read_text())
    base = json.loads(BASE47.read_text())
    k15 = json.loads(K15.read_text())
    k15_audit = json.loads(K15_AUDIT.read_text())
    prior = json.loads(THROUGH22.read_text())
    ledger = json.loads(LEDGER.read_text())
    module = load_module()

    require(set(manifest) == {"degree", "scale_U", "fragment_inputs", "groups", "scope"},
            "manifest top-level shape")
    require(manifest["degree"] == 23 and manifest["scale_U"] == U, "degree/U")
    require(len(base["groups"]) == 13 and sum(map(lambda x: len(x["ids"]), base["groups"])) == 47,
            "corrected 47/59 baseline")
    require(len(k15["groups"]) == 4 and sum(map(lambda x: len(x["ids"]), k15["groups"])) == 12,
            "K15 12-ID fragment")
    require(manifest["groups"] == base["groups"] + k15["groups"], "47+12 manifest concatenation")
    require(len(manifest["fragment_inputs"]) == 6 and
            sum(entry["scalar_groups"] for entry in manifest["fragment_inputs"]) == 17,
            "six inputs / 17 scalar groups")
    for entry in manifest["fragment_inputs"]:
        path = ROOT / entry["path"]
        require(path.is_file() and sha(path) == entry["sha256"], f"fragment hash {path}")

    required = dag["required_reachable_lineage_ids_by_degree"]["23"]
    require(len(required) == len(set(required)) == 59, "frozen DAG K23 census")
    seen_groups = Counter()
    seen_ids = []
    full_scaled = 0
    irreducible_scaled = 0
    for entry in manifest["groups"]:
        require(set(entry) == GROUP_KEYS, f"group shape {entry.get('group_id')}")
        group_id = entry["group_id"]
        require(group_id in module.EXPECTED_GROUPS and
                entry["ids"] == module.EXPECTED_GROUPS[group_id], f"group partition {group_id}")
        seen_groups[group_id] += 1
        seen_ids.extend(entry["ids"])
        evidence = ROOT / entry["evidence_path"]
        require(evidence.is_file() and sha(evidence) == entry["evidence_sha256"],
                f"evidence hash {group_id}")
        full_integer = int(entry["full_scaled_U"])
        irreducible_integer = int(entry["irreducible_scaled_U"])
        require(Fraction(full_integer, U) == Fraction(entry["full"]), f"full U {group_id}")
        require(Fraction(irreducible_integer, U) == Fraction(entry["irreducible"]),
                f"irreducible U {group_id}")
        require(full_integer == irreducible_integer, f"terminal mismatch {group_id}")
        full_scaled += full_integer
        irreducible_scaled += irreducible_integer
    require(set(seen_groups) == set(module.EXPECTED_GROUPS) and
            all(count == 1 for count in seen_groups.values()), "group scalar once")
    id_counts = Counter(seen_ids)
    missing = sorted(set(required) - set(seen_ids))
    duplicate = sorted(item for item, count in id_counts.items() if count != 1)
    extra = sorted(set(seen_ids) - set(required))
    require(not missing and not duplicate and not extra and len(seen_ids) == 59,
            "DAG set equality")

    with redirect_stdout(io.StringIO()):
        hostile = module.self_test()
    recomputed = module.assemble(manifest, allow_partial=False)
    require(hostile["status"] == "PASS_K23_59_ID_STRICT_ASSEMBLER_HOSTILE_SELFTEST",
            "hostile self-test")
    require(recomputed["status"] == result["status"] == "PASS_COMPLETE_K23_59_ID_EXACT_Q",
            "complete status")
    for key in ("complete_K23_claim", "covered_paths", "required_paths", "scalar_groups",
                "required_scalar_groups", "missing_paths", "duplicate_paths", "extra_paths",
                "missing_scalar_groups", "full_scaled_U", "irreducible_scaled_U", "full",
                "irreducible", "covered_ids", "full_equals_irreducible", "dag_logical_sha256",
                "manifest_logical_sha256"):
        require(result[key] == recomputed[key], f"stored/recomputed {key}")
    require(full_scaled == irreducible_scaled == int(result["full_scaled_U"]), "manual scalar sum")
    require(k15_audit["status"] == "PASS_INDEPENDENT_K23_DIRECT_K15_FINAL_EIGHT_SHARD_REFEREE" and
            k15_audit["logical_sha256"] == "8a3de5cfc7c45547469a597c1a4aa119bd895592dfc8720cf4a02864c0038f7d",
            "K15 independent final audit")

    k23 = Fraction(full_scaled, U)
    through22 = Fraction(prior["cumulative_K14_through_K22"]["numerator"],
                         prior["cumulative_K14_through_K22"]["denominator"])
    cumulative = through22 + k23
    require(k23 == Fraction(-428913276887351456, 24838275), "K23 rational")
    require(cumulative == Fraction(-829424811081283712, 173867925), "cumulative rational")
    require(ledger["status"] == "PASS_COMPLETE_CHARGE_LEDGER_THROUGH_K23" and
            ledger["coverage"]["K23"] == 59 and ledger["future_degree_allocation"] is None,
            "stored ledger status/scope")
    require(Fraction(ledger["charges"]["K23"]["numerator"],
                     ledger["charges"]["K23"]["denominator"]) == k23,
            "stored K23 ledger charge")
    require(Fraction(ledger["cumulative_K14_through_K23"]["numerator"],
                     ledger["cumulative_K14_through_K23"]["denominator"]) == cumulative and
            Fraction(ledger["unallocated_conservation_residual_after_K23"]["numerator"],
                     ledger["unallocated_conservation_residual_after_K23"]["denominator"]) == -cumulative,
            "stored cumulative/residual")
    for source in ledger["sources"].values():
        source_path = ROOT / source["path"]
        require(source_path.is_file() and sha(source_path) == source["sha256"],
                f"ledger source {source_path}")
    answer = {
        "status": "PASS_INDEPENDENT_COMPLETE_K23_59_ID_EXACT_Q_AND_LEDGER",
        "degree": 23, "scale_U": U,
        "required_paths": 59, "covered_paths": 59,
        "required_scalar_groups": 17, "scalar_groups": 17,
        "missing_paths": missing, "duplicate_paths": duplicate, "extra_paths": extra,
        "group_scalar_counted_once": True,
        "all_fragment_and_evidence_hashes_replayed": True,
        "hostile_tests": hostile["status"],
        "K23": {"numerator": k23.numerator, "denominator": k23.denominator, "text": str(k23)},
        "cumulative_K14_through_K23": {
            "numerator": cumulative.numerator, "denominator": cumulative.denominator,
            "text": str(cumulative)},
        "unallocated_conservation_residual_after_K23": {
            "numerator": -cumulative.numerator, "denominator": cumulative.denominator,
            "text": str(-cumulative)},
        "K23_manifest_sha256": PINS[MANIFEST],
        "K23_result_sha256": PINS[RESULT],
        "K15_final_audit_logical_sha256": k15_audit["logical_sha256"],
        "scope": "complete K23 exact charge and cumulative K14..K23 arithmetic only; no K24 or conjecture verdict",
    }
    print(json.dumps(answer, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
