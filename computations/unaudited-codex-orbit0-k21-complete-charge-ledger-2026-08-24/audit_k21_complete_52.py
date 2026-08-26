#!/usr/bin/env python3
"""Independent exact-Q and strict-coverage audit of the complete K21 ledger."""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ASSEMBLY = ROOT / "computations/unaudited-codex-orbit0-k21-charge-assembly-2026-08-24"
MANIFEST = ASSEMBLY / "k21_manifest_complete_52.json"
RESULT = ASSEMBLY / "results_k21_complete_52_exact.json"
PARTIAL_MANIFEST = ASSEMBLY / "k21_manifest_47_of_52_partial.json"
ASSEMBLER = ASSEMBLY / "assemble_filtered_degree_exact.py"
DAG = ROOT / "computations/unaudited-codex-orbit0-k14-k24-recurrence-dag-2026-08-23/results_recurrence_dag.json"
GENERIC_REF = ROOT / "computations/unaudited-codex-orbit0-k21-charge-assembly-referee-2026-08-24/results_filtered_degree_exact_referee.json"
H232 = ROOT / "computations/unaudited-codex-orbit0-k21-hidden-232-charge-2026-08-24/results_hidden_232_k21_charge.json"
H232_REF = H232.with_name("results_hidden_232_independent_referee.json")
D14322 = ROOT / "computations/unaudited-codex-orbit0-k21-d14-322-charge-2026-08-24/results_k21_d14_322_charge.json"
D14322_REF = D14322.with_name("results_k21_d14_322_audit.json")
D15222 = ROOT / "computations/unaudited-codex-orbit0-k21-d15-r2-2-2-charge-2026-08-24/results_k21_d15_r2_2_2.json"
D15222_REF = ROOT / "computations/unaudited-codex-orbit0-k21-d15-r2-2-2-referee-2026-08-24/results_d15_r2_2_2_independent_audit.json"
OUT = HERE / "results_k21_complete_52_audit.json"
U = 400_591_699_200
EXPECTED = Fraction(-15_276_224_591_027_275_648, 521_603_775)
PINS = {
    MANIFEST: "9085dec995d7bbbc26f4f875b43cc54c8f5ad9e9d34af413e6dd3a4a4889fe96",
    RESULT: "4df5a6316a8bfac70efb793d27f7e72ea269b491d8a565ecedb17d7997f81340",
    PARTIAL_MANIFEST: "1bacbb09d64027fc409c66fb7dbe47942b80a7c4225a9d8fdd4d07385fb59d84",
    ASSEMBLER: "cf4a5214a15081b91d89c90fc4b79c39e0d54e9b183f442131eec258bf1bce69",
    DAG: "469639f662682d3e39b5b9f2d1055e113826a93bd416dbdcb788881e9ffe44fa",
    GENERIC_REF: "fa51481128ba75a4d308fc43f02bf6d52b3af232bec2e315721dfe7a525b2c51",
    H232: "a58fa70195e5bb42ddad9b971a05145d15043f35af044c5339b1779ea56f3bae",
    H232_REF: "7cc51a5d537d41e00c0643f79e92ccf79a75ef908cae67bcf6d2f528ecd86846",
    D14322: "46065e0c432be6b37ca4044998a8cada8a0e83527699581ff2040735cdd7f7aa",
    D14322_REF: "eaac9ed6e4de6cf38819b129c435ce52208f6bec2aad6478c022b9c67a41d33a",
    D15222: "c6879b6605dc58e28418487b258018ef45c029aa4881f422c467ed73c3f6798e",
}


def require(ok, detail):
    if not ok:
        raise RuntimeError(detail)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def ids(entry):
    require(("id" in entry) != ("ids" in entry), entry)
    value = [entry["id"]] if "id" in entry else entry["ids"]
    require(isinstance(value, list) and value and all(isinstance(x, str) for x in value), value)
    require(len(value) == len(set(value)), value)
    return value


def q(value):
    if isinstance(value, str) or isinstance(value, int):
        return Fraction(value)
    return Fraction(int(value["numerator"]), int(value["denominator"]))


def main():
    # D15 referee is deliberately pinned dynamically in the package manifest;
    # all already-frozen external inputs are byte-pinned here.
    for path, expected in PINS.items():
        require(digest(path) == expected, (path, digest(path), expected))
    d15_ref = json.loads(D15222_REF.read_text())
    require(d15_ref["status"] == "PASS_INDEPENDENT_D15_R2_2_2_SOURCE_COUNT_SAMPLE_TERMINAL_REFEREE", d15_ref)
    require(d15_ref["logical_sha256"] == "7d9fef5ed2796f7e09b45ccbc7bc55af7f126cfeb2916cb15750f498fd328b27", d15_ref)

    dag = json.loads(DAG.read_text())
    required_from_nodes = sorted(node["id"] for node in dag["nodes"]
                                 if node["reachable"] and node["degree"] == 21)
    required = dag["required_reachable_lineage_ids_by_degree"]["21"]
    require(required_from_nodes == required and len(required) == len(set(required)) == 52, len(required))
    manifest = json.loads(MANIFEST.read_text())
    partial = json.loads(PARTIAL_MANIFEST.read_text())
    entries = manifest["groups"]
    require(entries[:len(partial["groups"])] == partial["groups"] and len(entries) == 15, len(entries))
    flat = [lineage for entry in entries for lineage in ids(entry)]
    counts = Counter(flat)
    require(len(flat) == len(counts) == 52 and max(counts.values()) == 1, counts)
    require(set(flat) == set(required), (set(required)-set(flat), set(flat)-set(required)))

    missing_before = [x for x in required if x not in {y for e in partial["groups"] for y in ids(e)}]
    require(missing_before == [
        "D14:222|R:2-3-2", "D14:222|R:3-2-2",
        "D15:223|R:2-2-2", "D15:232|R:2-2-2", "D15:322|R:2-2-2"], missing_before)
    appended = entries[-3:]
    require([ids(x) for x in appended] == [
        ["D14:222|R:2-3-2"], ["D14:222|R:3-2-2"],
        ["D15:223|R:2-2-2", "D15:232|R:2-2-2", "D15:322|R:2-2-2"]], appended)

    h232 = json.loads(H232_REF.read_text())
    d14322 = json.loads(D14322_REF.read_text())
    d15222 = json.loads(D15222.read_text())
    expected_appended = [
        (Fraction(h232["charge"]["reduced_full_and_irreducible"]), digest(H232)),
        (Fraction(d14322["charge"]), digest(D14322)),
        (Fraction(d15_ref["charge"]), digest(D15222)),
    ]
    for entry, (charge, evidence) in zip(appended, expected_appended, strict=True):
        require(q(entry["full"]) == q(entry["irreducible"]) == charge, (entry, charge))
        require(entry["evidence_sha256"] == evidence, (entry, evidence))
    require(d15222["ids"] == ids(appended[2]) and d15222["individual_id_charges"] is None, d15222)

    full = sum((q(entry["full"]) for entry in entries), Fraction())
    irreducible = sum((q(entry["irreducible"]) for entry in entries), Fraction())
    require(full == irreducible == EXPECTED, (full, irreducible, EXPECTED))
    multiplied_wrong = sum((q(entry["full"])*len(ids(entry)) for entry in entries), Fraction())
    require(multiplied_wrong != full, "group-once test was not discriminating")

    result = json.loads(RESULT.read_text())
    require(result["status"] == "PASS_COMPLETE_K21_52_ID_EXACT_Q" and result["complete_claim"] is True, result)
    require((result["required_paths"], result["covered_paths"], result["scalar_groups"]) == (52, 52, 15), result)
    require(result["covered_ids"] == flat, result)
    require(result["missing_paths"] == result["duplicate_paths"] == result["extra_paths"] == [], result)
    require(q(result["full"]) == q(result["irreducible"]) == EXPECTED, result)
    require(result["dag_logical_sha256"] == dag["logical_sha256"] ==
            "ad59639716fe2a2cc04fca83a189d74ff8c1f5bbe6d7257676dd458f4c768a66", result)
    manifest_logical = sha256(json.dumps(manifest, sort_keys=True,
                                        separators=(",", ":")).encode()).hexdigest()
    require(result["manifest_logical_sha256"] == manifest_logical ==
            "5e257c21950dfe539e8771e52be9e3e82aaf6593ac3c45e97df2311b7b0eae8b", result)
    generic_ref = json.loads(GENERIC_REF.read_text())
    require(generic_ref["status"] == "PASS_INDEPENDENT_FILTERED_DEGREE_EXACT_ASSEMBLER_REFEREE", generic_ref)

    report = {
        "status": "PASS_INDEPENDENT_COMPLETE_K21_52_ID_EXACT_CHARGE_LEDGER",
        "degree": 21,
        "coverage": {
            "required_ids": 52, "covered_ids": 52, "scalar_groups": 15,
            "missing": [], "duplicates": [], "extra": [],
            "required_set_rederived_from_reachable_DAG_nodes": True,
        },
        "charge": {
            "full": str(full), "irreducible": str(irreducible),
            "equal": True, "common_scale_U": str(U),
        },
        "grouped_scalar_once": {
            "enabled": True, "per_ID_multiplication_rejected": True,
            "D15_R2_2_2_group_size": 3,
            "D15_R2_2_2_scalar": str(q(appended[2]["full"])),
        },
        "newly_closed_five_ID_gap": missing_before,
        "guards": {
            "generic_assembler_independently_refereed": True,
            "three_new_producer_results_byte_pinned": True,
            "three_new_independent_referees_PASS": True,
            "prior_47_ID_manifest_preserved_exactly": True,
            "strict_complete_gate": True,
            "no_membership_or_nonmembership_inference": True,
        },
        "pinned": {str(path.relative_to(ROOT)): expected for path, expected in PINS.items()} | {
            str(D15222_REF.relative_to(ROOT)): digest(D15222_REF),
        },
    }
    logical = json.dumps(report, sort_keys=True, separators=(",", ":")).encode()
    report["logical_sha256"] = sha256(logical).hexdigest()
    OUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
