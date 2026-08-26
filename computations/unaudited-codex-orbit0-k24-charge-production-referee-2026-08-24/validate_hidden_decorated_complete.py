#!/usr/bin/env python3
"""Independent structural referee for the full fast hidden-decorated K24 result."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
U = 400_591_699_200
N = 101_545_723
ID = "D14:222|R:2-4-4"
INPUT = ROOT / "computations/unaudited-codex-orbit0-hidden-k16-k2-full-orbit-2026-08-23/hidden_k16_decorated_pair_orbits_full.bin"
INPUT_SHA = "22f91fc887caecb628df495b6a19e319c0ada39b6940b1ca4f795ae09d6c21c8"
SOURCE_PINS = {
    "run_k24_charge_hidden_decorated.rs": "cd3777be520f5d4d77d6da72a4b54ef1a0e7eff91fb923b037b447b730276deb",
    "k24_hidden_decorated_impl.rs": "fb879aee3d8d7ba0ee17f3d0289c037e99d2f191b27567ff2603b8c5e2b226bb",
    "k24_hidden_base.rs": "ec68ac205d1737778d7fe1c23d1f2108fc2b274c8c54cb29716915ec8ba17c08",
    "k24_hidden_base_run_filtered_k17.rs": "5b0b5a467c6418b2bf042b47a89636c0135d93cdea656fd864fb5708f7682056",
    "run_k24_charge_hidden_decorated": "fc65915201e0378f6e9f68857907c3e48041aa207c10513319ac353723db4e71",
}
HEADER = [
    "input_index", "K16_row", "p2", "weight_after_p2", "pair_uses", "orbit",
    "stabilizer", "first_children", "pivotable_intermediate", "selected_p3",
    "terminal_K24", "terminal_weight_scaled", "charge_scaled", "nonzero",
]


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def number(value, name: str) -> int:
    require(not isinstance(value, bool), f"{name}: bool is not integer")
    try:
        return int(value)
    except (ValueError, TypeError) as exc:
        raise ValueError(f"{name}: bad integer {value!r}") from exc


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(8 << 20):
            h.update(chunk)
    return h.hexdigest()


def validate(result_path: Path, samples_path: Path, hash_input: bool) -> dict:
    source_dir = ROOT / "computations/unaudited-codex-orbit0-k24-charge-only-fast-prototype-2026-08-24"
    for name, expected in SOURCE_PINS.items():
        require(sha256(source_dir / name) == expected, f"producer pin mismatch: {name}")
    if hash_input:
        require(sha256(INPUT) == INPUT_SHA, "hidden-decorated input hash mismatch")
    result = json.loads(result_path.read_text())
    require(result.get("status") == "PASS_COMPLETE_K24_HIDDEN_DECORATED_R244_CHARGE_ONLY", "hidden-decorated full status")
    require(number(result.get("degree"), "degree") == 24 and number(result.get("scale_U"), "U") == U, "hidden-decorated degree/U")
    require(result.get("covered_lineage_ids") == [ID], "hidden-decorated strict scope")
    require(result.get("input") == str(INPUT.relative_to(ROOT)) and result.get("input_sha256_expected") == INPUT_SHA, "hidden-decorated input declaration")
    require(number(result.get("input_records_declared"), "declared records") == N and result.get("input_interval") == [0, N] and number(result.get("input_records_consumed"), "consumed records") == N, "hidden-decorated full interval")
    require(number(result.get("retained_pair_uses"), "pair uses") == 511_214_060, "hidden-decorated pair-use pin")
    require(number(result.get("pair_weight_sum_scaled"), "pair weight") == 146_230_609_431_055_564_800, "hidden-decorated pair-weight pin")
    sink = result.get("sink", {})
    require([number(sink.get(k), k) for k in ("first_tail_degree", "intermediate_degree", "terminal_tail_degree")] == [4, 20, 4], "hidden-decorated degree route")
    require(number(sink.get("first_tail_evaluations"), "first tails") == 60 * N, "hidden-decorated first-tail identity")
    pivotable = number(sink.get("pivotable_intermediate_children"), "pivotable intermediate")
    selected = number(sink.get("selected_p3"), "selected p3")
    terminal = number(sink.get("terminal_K24_occurrences"), "terminal occurrences")
    require(terminal == 60 * selected == number(sink.get("full_occurrences"), "full") == number(sink.get("irreducible_occurrences"), "irreducible"), "hidden-decorated terminal identity")
    require(number(sink.get("pivotable_weight_scaled"), "pivotable weight") == -number(sink.get("normalized_p3_weight_scaled"), "normalized weight"), "hidden-decorated normalized sign")
    require(number(sink.get("terminal_weight_scaled"), "terminal weight") == 60 * number(sink.get("normalized_p3_weight_scaled"), "normalized weight"), "hidden-decorated terminal weight")
    charge = number(sink.get("full_charge_scaled_U"), "charge")
    require(charge == number(sink.get("irreducible_charge_scaled_U"), "irreducible charge") == 97_324_923_903_254_986_752, "hidden-decorated charge pin/equality")
    require(number(sink.get("cache_hits"), "hits") + number(sink.get("cache_misses"), "misses") == selected, "hidden-decorated cache identity")
    require(number(sink.get("cache_peak_keys"), "peak keys") <= 300_720 and number(sink.get("cache_clears"), "cache clears") == 1009, "hidden-decorated cache guard")
    hist = sink.get("m2_m3_histogram", {})
    require(isinstance(hist, dict), "hidden-decorated divisor histogram")
    parsed_hist = {}
    for key, value in hist.items():
        parts = key.split("_")
        require(len(parts) == 2, "hidden-decorated histogram key")
        m2, m3 = map(int, parts)
        require(m2 > 0 and m3 > 0 and U % (m2 * m3) == 0, "hidden-decorated denominator outside U")
        parsed_hist[m2, m3] = number(value, "histogram value")
    require(sum(parsed_hist.values()) == pivotable and sum(m3 * value for (_, m3), value in parsed_hist.items()) == selected, "hidden-decorated histogram identities")
    stabilizers = {number(key, "stabilizer"): number(value, "stabilizer count") for key, value in result.get("stabilizer_histogram", {}).items()}
    require(sum(stabilizers.values()) == N and all(stab > 0 and 384 % stab == 0 for stab in stabilizers), "hidden-decorated stabilizer histogram")
    require(number(result.get("literal_witness_records"), "witness records") == 257 and number(result.get("literal_nonzero_records"), "nonzero records") == 42, "hidden-decorated witness pins")
    require(Path(result.get("sample_ledger", "")).name == samples_path.name, "hidden-decorated ledger declaration")
    with samples_path.open(newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        require(reader.fieldnames == HEADER, "hidden-decorated ledger schema")
        rows = list(reader)
    require(len(rows) == 257, "hidden-decorated ledger length")
    expected_indices = [j * (N - 1) // 256 for j in range(257)]
    require([number(row["input_index"], "sample index") for row in rows] == expected_indices, "hidden-decorated distributed sample indices")
    require(sum(number(row["nonzero"], "sample flag") for row in rows) == 42 and all(row["nonzero"] in {"0", "1"} for row in rows), "hidden-decorated sample flags")
    require(all(len(row["K16_row"]) == 48 for row in rows), "hidden-decorated sample row length")
    for row in rows:
        int(row["K16_row"], 16)
        require(number(row["orbit"], "sample orbit") * number(row["stabilizer"], "sample stabilizer") == 384, "hidden-decorated sample orbit identity")
        require(number(row["first_children"], "sample first children") == 60, "hidden-decorated sample first-tail count")
        require(number(row["terminal_K24"], "sample terminal") == 60 * number(row["selected_p3"], "sample selected p3"), "hidden-decorated sample terminal identity")
        require((number(row["selected_p3"], "sample selected p3") > 0) == (row["nonzero"] == "1"), "hidden-decorated sample flag meaning")
    require(result.get("universal_terminality") == "every terminal K4 child has active-anchor mass 0", "hidden-decorated terminality declaration")
    require(number(result.get("workers"), "workers") == 8 and number(result.get("cache_chunk_records"), "cache chunk") == 100_000, "hidden-decorated launch controls")
    require(float(result.get("elapsed_seconds")) < 600 and float(result.get("linear_full_projection_seconds")) < 600, "hidden-decorated wall gate")
    return {
        "status": "PASS_INDEPENDENT_K24_HIDDEN_DECORATED_COMPLETE_STRUCTURE",
        "result_sha256": sha256(result_path), "samples_sha256": sha256(samples_path),
        "input_sha256": INPUT_SHA, "input_hash_recomputed": hash_input,
        "strict_lineage_ids": [ID], "covered_ids": 1, "charge_scaled_U": str(charge),
        "terminal_occurrences": terminal, "literal_witness_records": len(rows),
        "literal_flagged_nonzero_records": 42, "producer_source_pins": SOURCE_PINS,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True); parser.add_argument("--samples", type=Path, required=True)
    parser.add_argument("--hash-input", action="store_true"); parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = validate(args.result, args.samples, args.hash_input)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": report["status"], "witnesses": report["literal_witness_records"]}))


if __name__ == "__main__":
    main()
