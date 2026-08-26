#!/usr/bin/env python3
"""Merge the sign-corrected frozen tail and irreducible direct K16 input."""

from collections import Counter
from hashlib import sha256
import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FROZEN = (ROOT / "computations/unaudited-codex-orbit0-k16-literal-collection-2026-08-22"
          / "results_orbit0_k16_literal_residual.json")
DIRECT = HERE / "missing_direct_irreducible_H_orbits.tsv"
DIRECT_RESULT = HERE / "results_missing_input_cycle_charge.json"
SIGN_RESULT = HERE / "results_frozen_collector_sign_referee.json"
TSV = HERE / "sign_corrected_combined_k16_H_orbits.tsv"
OUT = HERE / "results_sign_corrected_combined_k16.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutate", action="store_true")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    frozen = json.loads(FROZEN.read_text())
    direct_result = json.loads(DIRECT_RESULT.read_text())
    sign = json.loads(SIGN_RESULT.read_text())
    require(len(frozen["literal_orbits"]) == 1_848_174
            and frozen["logical_sha256"]
            == "8eb9f7dbb220afd759533c10a4881a502a43bdb3bfa28c36e3b89cf98a4ee58c",
            "frozen tail drift")
    require(sign["status"] == "EXACT_FROZEN_COLLECTOR_GLOBAL_SIGN_REVERSED"
            and sign["sign_corrected_cycle_charge"] == 311_258_112,
            "sign referee drift")
    require(direct_result["irreducible_collected_H_orbits"] == 93_328
            and direct_result["collected_missing_direct_irreducible_pairing"]
            == 63_869_184, "direct residual drift")

    # Frozen masses have the wrong global sign; negate them on load.
    combined = {}
    frozen_keys = set()
    for row_hex, numerator, denominator in frozen["literal_orbits"]:
        require(denominator == 1, (row_hex, numerator, denominator))
        row = bytes.fromhex(row_hex)
        require(row not in combined, row_hex)
        combined[row] = -numerator
        frozen_keys.add(row)
    if args.mutate:
        combined[min(combined)] += 1

    direct_masses = {}
    rows = DIRECT.read_text().splitlines()
    require(rows[0] == "row\tmissing_direct_orbit_mass", "direct header drift")
    for line in rows[1:]:
        row_hex, coefficient = line.split("\t")
        row = bytes.fromhex(row_hex)
        require(row not in direct_masses, row_hex)
        direct_masses[row] = int(coefficient)
    require(len(direct_masses) == 93_328, len(direct_masses))

    direct_keys = set(direct_masses)
    overlap = frozen_keys & direct_keys
    cancellations = 0
    changed_overlap = 0
    for row, coefficient in direct_masses.items():
        updated = combined.get(row, 0) + coefficient
        if updated:
            combined[row] = updated
            changed_overlap += int(row in overlap)
        else:
            require(row in overlap, row.hex())
            combined.pop(row, None)
            cancellations += 1
    require(cancellations + changed_overlap == len(overlap),
            (cancellations, changed_overlap, len(overlap)))

    lines = ["row\tsign_corrected_combined_orbit_mass"]
    histogram = Counter()
    for row, coefficient in sorted(combined.items()):
        require(coefficient, row.hex())
        histogram[coefficient] += 1
        lines.append(f"{row.hex()}\t{coefficient}")
    payload = "\n".join(lines) + "\n"
    payload_hash = sha256(payload.encode()).hexdigest()
    if not args.verify:
        TSV.write_text(payload)

    result = {
        "schema": "orbit0-k16-sign-corrected-combined-collection-v1",
        "status": "EXACT_SIGN_CORRECTED_COMBINED_K16_COLLECTION",
        "frozen_stored_H_orbits": len(frozen_keys),
        "sign_corrected_frozen_H_orbits": len(frozen_keys),
        "irreducible_direct_H_orbits": len(direct_keys),
        "support_overlap": len(overlap),
        "exact_zero_cancellations": cancellations,
        "nonzero_changed_overlap": changed_overlap,
        "direct_only_H_orbits": len(direct_keys - frozen_keys),
        "frozen_only_H_orbits": len(frozen_keys - direct_keys),
        "combined_nonzero_H_orbits": len(combined),
        "combined_orbit_mass_coefficient_histogram": {
            str(value): count for value, count in sorted(histogram.items())},
        "stored_frozen_cycle_charge": -311_258_112,
        "sign_corrected_frozen_cycle_charge": 311_258_112,
        "irreducible_direct_cycle_charge": 63_869_184,
        "combined_cycle_charge": 375_127_296,
        "combined_tsv_sha256": payload_hash,
        "pins": {
            "frozen_file_sha256": sha256(FROZEN.read_bytes()).hexdigest(),
            "direct_file_sha256": sha256(DIRECT.read_bytes()).hexdigest(),
            "direct_logical": direct_result["logical_sha256"],
            "sign_referee_logical": sign["logical_sha256"],
        },
        "scope_guard": ("Exact coefficient merge at K16 only; singleton-generated "
                        "K18 tails and all later pages are omitted."),
    }
    logical = dict(result)
    result["logical_sha256"] = sha256(json.dumps(
        logical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    require(result["logical_sha256"]
            == "b663791faa47a549ac026b07a999cd76337d1096f6a98ec2a45daefbf69c3445",
            "hostile coefficient mutation or combined collection drift")
    if not args.verify:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: result[key] for key in (
        "status", "support_overlap", "exact_zero_cancellations",
        "combined_nonzero_H_orbits", "combined_cycle_charge",
        "combined_tsv_sha256", "logical_sha256")}, sort_keys=True))


if __name__ == "__main__":
    main()
