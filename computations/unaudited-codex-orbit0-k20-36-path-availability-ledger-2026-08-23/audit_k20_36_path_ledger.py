#!/usr/bin/env python3
"""Read-only provenance audit for the complete 36-lineage K20 charge page."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).with_name("results_k20_36_path_ledger.json")

DAG = "computations/unaudited-codex-orbit0-k14-k24-recurrence-dag-2026-08-23/results_recurrence_dag.json"
TEMPLATE = "computations/unaudited-codex-orbit0-k14-k24-recurrence-dag-2026-08-23/interface_template_K20.json"
PARTIAL = "computations/unaudited-codex-orbit0-k20-222-consumer-design-2026-08-23/results_partial_k20_charge_and_34_path_gap.json"
K20_222 = "computations/unaudited-codex-orbit0-k20-222-consumer-design-2026-08-23/results_k20_222_charge.json"
K20_222_REF = "computations/unaudited-codex-orbit0-k20-222-referee-2026-08-23/results_k20_222_referee.json"
HIDDEN_K34 = "computations/unaudited-codex-orbit0-hidden-k16-full-charge-2026-08-23/results_full_hidden_k3_k4_charge.json"
K19 = "computations/unaudited-codex-orbit0-k19-charge-2026-08-23/results_k19_charge.json"
K18 = "computations/unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/results_k18_charge.json"
K18_COMPLETE = "computations/unaudited-codex-orbit0-hidden-k16-k18-complete-charge-2026-08-23/results_complete_k18_charge.json"
FEED = "computations/unaudited-codex-orbit0-k20-feed-dag-referee-2026-08-23/results_k20_feed_dag_referee.json"

PROFILE_GROUPS = {
    "K14_R33": {
        "ids": ["D14:222|R:3-3"],
        "artifact": "computations/unaudited-codex-orbit0-k19-charge-2026-08-23/weights_k17_k14_k2.bin",
        "sha256": "34fdbffd1331035831dc86f2eb5ddf0183f5adba1300868248c4023916feee66",
        "conversion": "reuse the K17 parent profile/pivot weights and replace terminal K2 evaluation by K3",
    },
    "K15_R23": {
        "ids": [f"D15:{p}|R:2-3" for p in ("223", "232", "322")],
        "artifact": "computations/unaudited-codex-orbit0-k19-charge-2026-08-23/weights_k17_k15_k2.bin",
        "sha256": "864b3cac1230047db3200a4560d5ce3240747c9e89d0f4cfd5a8fe1236235b1d",
        "conversion": "reuse the collected K17 parent profile/pivot weights and replace terminal K2 evaluation by K3",
    },
    "K16_R4": {
        "ids": [f"D16:{p}|R:4" for p in ("224", "233", "242", "323", "332", "422")],
        "artifact": "computations/unaudited-codex-orbit0-k19-charge-2026-08-23/weights_k16_direct_k3.bin",
        "sha256": "d7dee1ea547253839884964cd0b58eb29b8d4bdaf4eb182fe921f0c46233ddfa",
        "conversion": "reuse the direct-K16 parent profile/pivot weights and replace terminal K3 evaluation by K4",
    },
    "K17_R3": {
        "ids": [f"D17:{p}|R:3" for p in ("234", "243", "324", "333", "342", "423", "432")],
        "artifact": "computations/unaudited-codex-orbit0-k19-charge-2026-08-23/weights_k17_direct_k2.bin",
        "sha256": "4fa59665dcbec7fbd4c5a7682bc02d1094f8c4a64a712f1c451453b1644bf5ec",
        "conversion": "reuse the direct-K17 parent profile/pivot weights and replace terminal K2 evaluation by K3",
    },
}

SCALAR_GROUPS = {
    "K14_R42": {
        "ids": ["D14:222|R:4-2"],
        "component": "K14_K4",
    },
    "K15_R32": {
        "ids": [f"D15:{p}|R:3-2" for p in ("223", "232", "322")],
        "component": "K15_K3",
    },
    "K16_R22": {
        "ids": [f"D16:{p}|R:2-2" for p in ("224", "233", "242", "323", "332", "422")],
        "component": "K16_K2",
    },
    "DIRECT_K18_R2": {
        "ids": [f"D18:{p}|R:2" for p in ("244", "334", "343", "424", "433", "442")],
        "component": "direct",
    },
}

EXACT = {
    "D14:222|R:2-2-2": (K20_222, "a022874ad36361caf44de2473b4a5c7534ecfb9c082df046e3f26046fcc90a57"),
    "D14:222|R:2-4": (HIDDEN_K34, "aa25a2deee2aff213b9f49b9f61826d161293651ccafa1cd7332ef978ae89934"),
}


def load(rel: str):
    return json.loads((ROOT / rel).read_text())


def sha(rel: str) -> str:
    h = hashlib.sha256()
    with (ROOT / rel).open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def logical_digest(value) -> str:
    clean = dict(value)
    clean.pop("logical_sha256", None)
    return hashlib.sha256(json.dumps(clean, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def main() -> None:
    required = set(load(TEMPLATE)["covered_lineages"])
    dag = load(DAG)
    partial = load(PARTIAL)
    assert required == set(dag["required_reachable_lineage_ids_by_degree"]["20"])
    assert set(EXACT) == set(partial["dag"]["covered_paths"])
    assert len(required) == 36

    # Pin small, load-bearing metadata artifacts byte-for-byte.  Large profile
    # hashes are checked against the frozen K19 result's own pinned ledger.
    expected_small = {
        DAG: "469639f662682d3e39b5b9f2d1055e113826a93bd416dbdcb788881e9ffe44fa",
        TEMPLATE: "4af00e877a07e068660c4f09134ff2ccba1988902da352e34da40f9b0dea6c21",
        PARTIAL: "07ff4265ce39b41bc3312fae21f3b224ab5d066b640b7493ee6a4ba88cf9b7f4",
        K20_222: EXACT["D14:222|R:2-2-2"][1],
        K20_222_REF: "5f4b8bf860a8477f6e54585413eba6d7e5858e36d37e3501481858b6725fa6ce",
        HIDDEN_K34: EXACT["D14:222|R:2-4"][1],
        K18: "eff58152c9b465b4fa770642898ada990f682bc677dac9363374f54aa65d5d47",
        K18_COMPLETE: "419d2cb639200a9e07b74faa2f6576cba64951acf042a359dbd3a3d145a537cd",
        FEED: "5b180bfe1ad0cb8398ac130c2f39be68b47e4fe016c0541bf3b3a68d01c07bfc",
    }
    for rel, digest in expected_small.items():
        assert sha(rel) == digest, rel

    k19 = load(K19)
    for group in PROFILE_GROUPS.values():
        assert (ROOT / group["artifact"]).exists()
        assert k19["pinned"][group["artifact"]] == group["sha256"]

    by_id = {n["id"]: n for n in dag["nodes"] if n["id"] in required}
    lines = []
    used = set()
    for lineage in sorted(required):
        node = by_id[lineage]
        common = {
            "lineage_id": lineage,
            "direct_packet_degree": node["direct_packet"]["degree"],
            "direct_packet_shifts": node["direct_packet"]["ordered_factor_shifts"],
            "response_shifts": node["response_shifts"],
            "sign": node["sign_relative_to_unsigned_R8prime"],
        }
        if lineage in EXACT:
            rel, digest = EXACT[lineage]
            common.update({
                "availability": "EXACT_K20_CHARGE_COMPUTED",
                "evidence": [{"artifact": rel, "sha256": digest}],
                "next_action": "reuse exact full and irreducible rational charges",
            })
        else:
            match = [(name, g) for name, g in PROFILE_GROUPS.items() if lineage in g["ids"]]
            scalar = [(name, g) for name, g in SCALAR_GROUPS.items() if lineage in g["ids"]]
            assert len(match) + len(scalar) <= 1
            if match:
                name, g = match[0]
                common.update({
                    "availability": "TERMINAL_PARENT_PROFILE_CHECKPOINT_AVAILABLE",
                    "coverage_granularity": "group-aggregated; sufficient for total charge, not an individual-lineage scalar",
                    "group": name,
                    "evidence": [{"artifact": g["artifact"], "sha256": g["sha256"]}, {"artifact": K19, "sha256": "8af5f43965fa6ab53d857dfea6b2b0241634783e744c100d85c24b3403f96e5a"}],
                    "next_action": g["conversion"],
                })
            elif scalar:
                name, g = scalar[0]
                common.update({
                    "availability": "SCALAR_ONLY_IMMEDIATE_PARENT_RECONSTRUCTION_REQUIRED",
                    "group": name,
                    "prior_scalar_component": g["component"],
                    "evidence": [{"artifact": K18, "sha256": expected_small[K18]}, {"artifact": K18_COMPLETE, "sha256": expected_small[K18_COMPLETE]}],
                    "next_action": "replay the source component, signed-collect pivotable K18 parents, then emit terminal K2 tails",
                })
            else:
                assert lineage == "D20:444|R:direct"
                common.update({
                    "availability": "DIRECT_SOURCE_PACKET_AVAILABLE_CHARGE_MISSING",
                    "evidence": [{"artifact": FEED, "sha256": expected_small[FEED]}],
                    "next_action": "evaluate the factorized direct 444 packet once; no parent checkpoint is needed",
                })
        used.add(lineage)
        lines.append(common)

    assert used == required
    counts = {}
    for line in lines:
        counts[line["availability"]] = counts.get(line["availability"], 0) + 1
    assert counts == {
        "EXACT_K20_CHARGE_COMPUTED": 2,
        "TERMINAL_PARENT_PROFILE_CHECKPOINT_AVAILABLE": 17,
        "SCALAR_ONLY_IMMEDIATE_PARENT_RECONSTRUCTION_REQUIRED": 16,
        "DIRECT_SOURCE_PACKET_AVAILABLE_CHARGE_MISSING": 1,
    }

    result = {
        "status": "PASS_AUTHORITATIVE_K20_36_PATH_ARTIFACT_AVAILABILITY_LEDGER",
        "scope": "Read-only artifact/provenance audit and minimal complete-charge schedule; no K20 charge evaluation or row expansion.",
        "dag": {"required_paths": 36, "artifact": DAG, "sha256": expected_small[DAG], "logical_sha256": dag["logical_sha256"]},
        "counts": counts,
        "lineages": lines,
        "minimal_complete_charge_schedule": [
            {
                "stage": 0,
                "action": "Reuse the two independently frozen exact K20 path charges D14:222|R:2-2-2 and D14:222|R:2-4.",
                "covers": 2,
            },
            {
                "stage": 1,
                "action": "Run four terminal profile evaluators on the frozen K17/K16 profile-weight interfaces, changing only the requested final tail degree (K14 R33, K15 R23, K16 R4, K17 R3). Accumulate group totals over Q.",
                "covers": 17,
                "materialize_rows": False,
            },
            {
                "stage": 2,
                "action": "Replay four source components whose K18 artifacts are scalar-only (K14/K4, K15/K3, K16/K2, direct K18), signed-canonical-collect only pivotable K18 parents, and feed all four streams to one terminal K2 charge evaluator.",
                "covers": 16,
                "materialize": "pivotable K18 parent profiles/rows only; the old scalar files cannot be prolonged",
            },
            {
                "stage": 3,
                "action": "Evaluate the direct D20:444 packet factorwise.",
                "covers": 1,
            },
            {
                "stage": 4,
                "action": "Assemble exact full and irreducible rational charges and require literal coverage equality with all 36 DAG IDs. Do not reuse the retracted old K20 interface subtotal.",
                "covers": 36,
            },
        ],
        "guards": {
            "current_exact_charge_count": 2,
            "old_34_path_gap_remains_a_charge_gap": True,
            "profile_checkpoint_scope": "The four large weight files are exact source-compressed parent-profile interfaces for the cycle charge only; they are not literal parent-row checkpoints and cannot justify later row collection.",
            "scalar_nonprolongation": "A K18 full/irreducible scalar does not determine its pivotable parent stream or outgoing K2 charge.",
            "raw_k17_checkpoint_guard": "checkpoint_k17_*.bin stores irreducible normals and is not used as a K20 parent feed.",
            "retracted_claim": "The superseded incomplete K20 interface is not a subtotal or coverage certificate.",
        },
        "pinned": expected_small,
    }
    result["logical_sha256"] = logical_digest(result)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "counts": counts, "logical_sha256": result["logical_sha256"]}, sort_keys=True))


if __name__ == "__main__":
    main()
