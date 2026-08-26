#!/usr/bin/env python3
"""Strict hash, arithmetic, lineage, shard, and witness audit for the K23 direct23 fragment."""
from __future__ import annotations

import hashlib
import json
import os
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
U = 400_591_699_200
LOCAL_PINS = {
    "k23_direct23_fragment_manifest.json": "57cdec4a6445c52bd7d35e1a97d37ef5f476f85e6c1de5b598d8c354b5db2d3b",
    "results_k23_direct23.json": "e84a39d027e07ad56d1c4d67dd9cab733ef25575aa324c892157deb80272767f",
    "results_k23_direct23.json.samples.tsv": "5968ec8c82678f79887cc208420108ec2878d9ab820793e818dd4c16402a804f",
    "referee_k23_direct23_samples.json": "80dd59f38f7e269b06385be7c7990dad22d9bb30ecf090fbeb7b226fa8151efa",
    "results_k23_direct23_assembler_partial.json": "3b749540b4df485a9c0d049ddf4e3770de4454b6d6a9a0e5235eeeb0543cad6e",
    "results_k23_direct23_shard0.json": "65c1591ee95042ccdca29617e43e75a86c1bead4a4faf2454a65d6833d36975d",
    "results_k23_direct23_shard0.json.samples.tsv": "098a078203d39431a9f3123b0830788b367213669255aa930a30cb1f99ea8942",
    "results_k23_direct23_shard1.json": "a819ca879bbfb4227bf797066791201fcd82fa7c0d754d8a672d4d89d7e7f9cb",
    "results_k23_direct23_shard1.json.samples.tsv": "08706b5c0b3855590d7c8ba4652a96f3e58312b339ddf13dc4b3792040f44e09",
    "results_k23_direct23_shard2.json": "4266db2f9e3833ae7c63498987f18d792b5aa1340b4cd5b8faca505bf1834503",
    "results_k23_direct23_shard2.json.samples.tsv": "0ce07ef82946c0574471ab01bd7db9d9691ad5808c8bfc861cced59b42f59d50",
    "run_k23_direct23_source_fold_v1.rs": "d60c5f3545963baa87b48c0d302648725b32e95469aa11112303f8597b712c10",
    "run_k23_direct23_source_fold.rs": "d0f92693b39f37d378a58a5dc1890704d9c1381b6a1bbb6e4857fa3bb8fc1d02",
    "merge_k23_direct23_shards.py": "d76f36ff816831d1c55989f8898ccb7b8d9ead81e749a33310f5564c51889575",
    "verify_k23_direct23_samples.rs": "54351f7500b0fca08dbeeb9082433b940ef36ae22aebbb21dbaf38cb03abc223",
}
EXTERNAL_PINS = {
    "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k16_structure.bin": "55e3823101f37f615f45ded7a3a4ca09c3d7ecd656c00f4bf3a9d5c33a5b260b",
    "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k17_aux.bin": "f8c78389c91498b625627f17429854178a0ee6c2c456288ddf108d97944d47ab",
    "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k17_cycle_aux.bin": "8213a3cbac99009ef71b5c055a977b440bc88979bb9119bbed022740d2397fc7",
    "computations/unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/filtered_k18_k4.bin": "4cec01e1695241c918f27625e79d767a8fb30fe5d1741b57f217f33712c35aa3",
    "computations/unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/run_k18_charge.rs": "24fa6d9ef9d8cadfa8b0b9e5ae01692f96bdf9df2168f4a26ccfa94b062e6045",
    "computations/unaudited-codex-orbit0-k23-availability-schedule-2026-08-24/k23_expected_scalar_groups.json": "6d59f1a24771e3a5e595ab79d8d0309881edea085da62c34b8e70cf93757c9ab",
    "computations/unaudited-codex-orbit0-k23-availability-schedule-2026-08-24/assemble_k23_59_exact.py": "b189ddf195af4e5e896aee495bf7adbc074af0108a4f026ae852fbbabaacbaaf",
    "computations/unaudited-codex-orbit0-k14-k24-recurrence-dag-2026-08-23/results_recurrence_dag.json": "469639f662682d3e39b5b9f2d1055e113826a93bd416dbdcb788881e9ffe44fa",
}
GROUPS = {
    "source_D17_R2_4": ([f"D17:{x}|R:2-4" for x in (234,243,324,333,342,423,432)], -603757293605464965120, Fraction(-52750731776,35), "p2_uses", 60),
    "source_D17_R3_3": ([f"D17:{x}|R:3-3" for x in (234,243,324,333,342,423,432)], -283096452568920883200, Fraction(-4946870272,7), "p2_uses", 32),
    "source_D18_R2_3": ([f"D18:{x}|R:2-3" for x in (244,334,343,424,433,442)], -51016487368812134400, Fraction(-127352832), "p2_uses", 32),
    "source_D19_R4": ([f"D19:{x}|R:4" for x in (344,434,443)], -3960127758414643200, Fraction(-9885696), "p1_uses", 60),
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    for name, digest in LOCAL_PINS.items():
        assert sha(HERE / name) == digest, name
    for name, digest in EXTERNAL_PINS.items():
        assert sha(ROOT / name) == digest, name

    v1 = (HERE / "run_k23_direct23_source_fold_v1.rs").read_text()
    v2 = (HERE / "run_k23_direct23_source_fold.rs").read_text()
    old = 'if let Some((_,g))=tar{let line=slots[g].take().unwrap_or_else(||panic!("no nonzero sample ri={} group={}",ri,g));samples.lock().unwrap().push(format!("{}\\t{}",g,line))}'
    new = 'if let Some((_,preferred))=tar{let(g,line)=(0..4).map(|delta|(preferred+delta)%4).find_map(|g|slots[g].take().map(|line|(g,line))).unwrap_or_else(||panic!("no nonzero sample in any group at ri={}",ri));samples.lock().unwrap().push(format!("{}\\t{}",g,line))}'
    assert old in v1 and new not in v1 and new in v2 and old not in v2
    assert v1.replace(old, new) == v2, "v1/v2 differ outside the documented sample-only line"

    result = json.loads((HERE / "results_k23_direct23.json").read_text())
    assert result["status"] == "PASS_COMPLETE_K23_DIRECT_D17_D19_23_ID_SOURCE_FOLD"
    assert result["degree"] == 23 and int(result["scale_U"]) == U
    assert result["source_selection"] == {"mode":"strict_three_shard_merge","intervals":[[0,161],[161,323],[323,485]],"record_count":485}
    assert result["covered_ids"] == 23 and result["scalar_groups"] == 4 and "rows" not in result
    assert [g["group_id"] for g in result["groups"]] == list(GROUPS)
    all_ids = []
    scaled = 0
    for observed in result["groups"]:
        ids, expected_scaled, exact, base, ratio = GROUPS[observed["group_id"]]
        assert observed["ids"] == ids
        all_ids.extend(ids)
        assert int(observed["full_charge_scaled_U"]) == expected_scaled
        assert observed["full_charge_scaled_U"] == observed["irreducible_charge_scaled_U"]
        assert observed["full_occurrences"] == observed["irreducible_occurrences"] == observed["K23_terminal_occurrences"]
        assert observed["K23_terminal_occurrences"] == ratio * observed[base]
        assert Fraction(expected_scaled, U) == exact == Fraction(observed["exact_charge"])
        scaled += expected_scaled
    assert len(all_ids) == len(set(all_ids)) == 23
    assert scaled == -941830361301612625920 and Fraction(scaled, U) == Fraction(-82288431616,35)
    assert result["literal_samples"] == 257 and result["literal_sample_group_counts"] == [66,64,64,63]
    assert result["cache"]["terminality_assertions_on_realized_keys"] == 7194103212
    assert result["cache"]["peak_literal_first_keys_per_R8"] <= result["cache"]["hard_literal_first_cap_per_R8"]
    assert result["cache"]["peak_terminal_keys_per_R8"] <= result["cache"]["hard_terminal_cap_per_R8"]

    manifest = json.loads((HERE / "k23_direct23_fragment_manifest.json").read_text())
    assert manifest["degree"] == 23 and manifest["scale_U"] == U
    assert [x["group_id"] for x in manifest["groups"]] == list(GROUPS)
    for entry in manifest["groups"]:
        ids, expected_scaled, exact, _, _ = GROUPS[entry["group_id"]]
        assert entry["ids"] == ids
        assert int(entry["full_scaled_U"]) == int(entry["irreducible_scaled_U"]) == expected_scaled
        assert Fraction(entry["full"]) == Fraction(entry["irreducible"]) == exact
        assert entry["evidence_sha256"] == LOCAL_PINS["results_k23_direct23.json"]

    lines = (HERE / "results_k23_direct23.json.samples.tsv").read_text().splitlines()
    assert len(lines) == 258
    ordinals = set(); counts = [0,0,0,0]; fallbacks = []
    for line in lines[1:]:
        c = line.split("\t"); assert len(c) == 20
        group, ordinal, ri = map(int, c[:3]); assert 0 <= group < 4 and ordinal not in ordinals
        ordinals.add(ordinal); counts[group] += 1
        assert ri == ordinal * 484 // 256 and int(c[15]) != 0 and int(c[18]) != 0
        if group != ordinal % 4: fallbacks.append((ordinal,ri,ordinal%4,group))
    assert ordinals == set(range(257)) and counts == [66,64,64,63]
    assert fallbacks == [(227,429,3,0)]

    referee = json.loads((HERE / "referee_k23_direct23_samples.json").read_text())
    assert referee["status"] == "PASS_INDEPENDENT_K23_DIRECT23_LITERAL_SAMPLE_REPLAY"
    assert referee["witnesses"] == referee["source_membership_replays"] == referee["literal_terminal_replays"] == 257
    assert referee["literal_intermediate_replays"] == 194 and referee["terminal_children_exhaustively_checked"] == 11836
    assert referee["group_counts"] == counts and len(referee["fallbacks"]) == 1

    partial = json.loads((HERE / "results_k23_direct23_assembler_partial.json").read_text())
    assert partial["status"] == "REJECT_INCOMPLETE_K23_59_ID_GATE" and not partial["complete_K23_claim"]
    assert partial["covered_paths"] == 23 and partial["scalar_groups"] == 4 and len(partial["missing_paths"]) == 36
    assert partial["duplicate_paths"] == partial["extra_paths"] == []
    assert Fraction(partial["full"]["text"]) == Fraction(partial["irreducible"]["text"]) == Fraction(-82288431616,35)

    audit = {
        "status":"PASS_STRICT_K23_DIRECT23_PACKAGE_AUDIT",
        "degree":23,
        "covered_ids":23,
        "scalar_groups":4,
        "full_equals_irreducible":True,
        "subtotal_scaled_U":str(scaled),
        "subtotal":"-82288431616/35",
        "source_intervals":[[0,161],[161,323],[323,485]],
        "literal_witnesses":257,
        "terminal_children_independently_replayed":11836,
        "producer_terminality_assertions":7194103212,
        "sample_only_revision_boundary_verified":True,
        "assembler_partial_coverage":23,
        "assembler_expected_remaining":36,
        "result_sha256":LOCAL_PINS["results_k23_direct23.json"],
        "samples_sha256":LOCAL_PINS["results_k23_direct23.json.samples.tsv"],
    }
    output = HERE / "package_audit.json"
    tmp = Path(f"{output}.tmp")
    tmp.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n")
    os.replace(tmp, output)
    print(json.dumps(audit, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
