#!/usr/bin/env python3
"""Exact factored raw and singleton-irreducible direct K17 cycle charge."""

from collections import Counter
from hashlib import sha256
import argparse
import importlib.util
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
K16_DIR = (ROOT / "computations"
           / "unaudited-codex-orbit0-k16-missing-input-cycle-charge-2026-08-23")
K16_AUDIT = K16_DIR / "audit_missing_input_cycle_charge.py"
K16_INPUT = K16_DIR / "missing_input_cycle_charge_input.tsv"
RUST = K16_DIR / "pair_missing_input_cycle_charge.rs"
DUAL = (ROOT / "computations/unaudited-codex-orbit0-k16-weighted-dafsa-2026-08-23"
        / "k16_cycle_partition_dual.tsv")
INPUT = HERE / "direct_k17_cycle_charge_input.tsv"
RESIDUAL = HERE / "direct_k17_irreducible_H_orbits.tsv"
BIN = HERE / "pair_direct_k17_cycle_charge"
OUT = HERE / "results_direct_k17_cycle_charge.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, path)
    spec.loader.exec_module(module)
    return module


def build_input(mutate=False):
    audit = load("direct_k17_base", K16_AUDIT)
    k14 = audit.load("direct_k17_k14", audit.K14_PATH)
    frozen = k14.FROZEN
    words = tuple(frozen.word_from_pair_colours(colours)
                  for colours in frozen.PAIR_COLOURS)
    groups = []
    for word in words:
        by_degree = {degree: tuple(term for term in frozen.BASE.word_terms(word)
                                   if frozen.row_k_degree(term) == degree)
                     for degree in (2, 3, 4)}
        require(tuple(map(len, by_degree.values())) == (12, 32, 60),
                tuple(map(len, by_degree.values())))
        groups.append(by_degree)
    profiles = tuple((left, middle, 9 - left - middle)
                     for left in (2, 3, 4) for middle in (2, 3, 4)
                     if 9 - left - middle in (2, 3, 4))
    require(len(profiles) == 7 and set(profiles) == {
        (3, 3, 3), (2, 3, 4), (2, 4, 3), (3, 2, 4),
        (3, 4, 2), (4, 2, 3), (4, 3, 2)}, profiles)
    packet = Counter()
    for degrees in profiles:
        for first in groups[0][degrees[0]]:
            for second in groups[1][degrees[1]]:
                for third in groups[2][degrees[2]]:
                    packet[bytes(sorted(first + second + third))] += 1
    require(len(packet) == sum(packet.values()) == 171_008
            and set(packet.values()) == {1}, "K17 packet collection drift")
    if mutate:
        packet[min(packet)] += 1

    old = K16_INPUT.read_text().splitlines()
    require(old[0] == "KRENN_MISSING_K16_CYCLE_CHARGE_V1"
            and old[1] == "R 485", old[:2])
    fixed = [line for line in old[3:] if not line.startswith("P\t")]
    require(sum(line.startswith("R\t") for line in fixed) == 485, "R cache drift")
    lines = [old[0], old[1], f"P {len(packet)}"] + fixed
    for row, coefficient in sorted(packet.items()):
        lines.append(f"P\t{row.hex()}\t{audit.matching_code(frozen.BASE, row).hex()}\t{coefficient}")
    payload = "\n".join(lines) + "\n"
    INPUT.write_text(payload)
    return payload, profiles


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutate", action="store_true")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    payload, profiles = build_input(args.mutate)
    subprocess.run(["rustc", "-O", str(RUST), "-o", str(BIN)], check=True)
    process = subprocess.run([str(BIN), str(INPUT), str(DUAL), str(RESIDUAL)],
                             check=True, text=True, capture_output=True)
    paired = json.loads(process.stdout)
    result = {
        "schema": "orbit0-direct-k17-cycle-charge-v1",
        "status": "EXACT_DIRECT_K17_SINGLETON_REDUCTION",
        "K17_layer_profiles": [list(profile) for profile in profiles],
        "K17_packet_terms_per_H_slice": 171_008,
        "R8prime_H_slices": 485,
        "input_sha256": sha256(payload.encode()).hexdigest(),
        "irreducible_residual_sha256": sha256(RESIDUAL.read_bytes()).hexdigest(),
        "scope_guard": ("Direct -R8prime*E K17 input only; excludes every "
                        "K14/K15 pivot tail and all K18+ outputs."),
        **paired,
    }
    logical = dict(result)
    result["logical_sha256"] = sha256(json.dumps(
        logical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    require(result["logical_sha256"]
            == "fb8fcf04ea18b701c1707a86b9b514a2640cf67b853ad24e1ece64dde078be80",
            "hostile packet mutation or direct K17 collection drift")
    if not args.verify:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
