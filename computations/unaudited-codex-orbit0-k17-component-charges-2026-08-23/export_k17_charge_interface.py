#!/usr/bin/env python3
"""Export the compact exact interface for the two K17 tail charges."""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import product
import ast
import importlib.util
import json
from pathlib import Path
import struct

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DESIGN = (ROOT / "computations/unaudited-codex-orbit0-filtered-k24-reducer-design-2026-08-23"
          / "filtered_k24_reducer.py")
COVER = (ROOT / "computations/unaudited-codex-orbit0-k14-interface-audit-2026-08-21"
         / "results_k16_anchor_cover.json")
OUT = HERE / "k17_charge_interface.bin"
RESULT = HERE / "results_k17_charge_interface.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, path)
    spec.loader.exec_module(module)
    return module


def main():
    d = load("k17_charge_design", DESIGN)
    cover_raw = json.loads(COVER.read_text())
    cover = frozenset(ast.literal_eval(row) for row in
                      cover_raw["single_pivot_cover"]["minimum_cover_orbit_representatives"])
    require(len(cover) == 25, len(cover))

    words = tuple(d.F.word_from_pair_colours(row) for row in d.F.PAIR_COLOURS)
    e2 = tuple(tuple(term for term in d.F.BASE.word_terms(word)
                     if d.F.row_k_degree(term) == 2) for word in words)
    packet = Counter()
    for left in e2[0]:
        for middle in e2[1]:
            for right in e2[2]:
                packet[bytes(sorted(left + middle + right))] += 1
    require(len(packet) == sum(packet.values()) == 1728, len(packet))
    records = []
    for row, size, coefficient in d.r8_h_records():
        mass = coefficient * size
        require(mass.denominator == 1, mass)
        records.append((row, mass.numerator))
    require(len(records) == 485, len(records))

    signatures = set()
    for row, _mass in records:
        for tail in packet:
            signatures.add(d.CTX.signature(bytes(sorted(row + tail))))
    require(len(signatures) == 216, len(signatures))

    def valid(signature):
        answer = []
        for pivot in d.CTX.pivots(signature):
            base = tuple(left - right for left, right in
                         zip(signature, d.CTX.vectors[pivot], strict=True))
            survivors = set()
            for tail in d.CTX.tails[pivot][2]:
                counts = Counter(tail)
                child = tuple(left + counts[cell] for left, cell in
                              zip(base, d.CTX.anchor_cells, strict=True))
                if not d.CTX.pivots(child):
                    survivors.add(d.CTX.canonical_signature(child))
            if survivors <= cover:
                answer.append(pivot)
        require(answer, signature)
        return tuple(answer)

    policies = {signature: valid(signature) for signature in signatures}
    histogram = Counter(map(len, policies.values()))
    occurrence_histogram = Counter()
    for row, _mass in records:
        for tail in packet:
            occurrence_histogram[len(policies[d.CTX.signature(bytes(sorted(row + tail)))])] += 1
    expected = {int(key): value for key, value in
                json.loads((ROOT / "computations/unaudited-codex-orbit0-k16-literal-collection-2026-08-22"
                            / "results_orbit0_k16_literal_residual.json").read_text())
                ["source_provenance"]["valid_pivot_count_histogram_per_factored_pair"].items()}
    require(dict(occurrence_histogram) == expected, (occurrence_histogram, expected))

    payload = bytearray(b"K17CHG1\0")
    payload.extend(struct.pack("<IIII", len(policies), len(records), len(packet), 78))
    payload.extend(bytes(d.CTX.anchor_cells))
    for u, v, a, b in d.F.BASE.CELLS:
        payload.extend((3 * u + a, 3 * v + b))
    for pivot in range(78):
        payload.extend(d.CTX.anchors[pivot])
        for tail in d.CTX.tails[pivot][2]:
            payload.extend(tail)
        for tail in d.CTX.tails[pivot][3]:
            payload.extend(tail)
    for signature, choices in sorted(policies.items()):
        payload.extend(bytes(signature))
        payload.append(len(choices))
        payload.extend(choices)
    for row, mass in records:
        payload.extend(row)
        payload.extend(struct.pack("<q", mass))
    for row, coefficient in sorted(packet.items()):
        require(coefficient == 1, coefficient)
        payload.extend(row)
    OUT.write_bytes(payload)
    result = {
        "schema": "orbit0-k17-charge-interface-v1",
        "status": "EXACT_K17_CHARGE_INTERFACE",
        "valid_signatures": len(policies),
        "valid_choice_count_by_signature": dict(sorted(histogram.items())),
        "valid_choice_count_by_occurrence": dict(sorted(occurrence_histogram.items())),
        "R8_H_records": len(records),
        "K14_E2_cubed_packet": len(packet),
        "K14_pivot_uses": sum(count * choices for choices, count in occurrence_histogram.items()),
        "K14_K3_tail_occurrences": sum(count * choices * 32 for choices, count in occurrence_histogram.items()),
        "interface_sha256": sha256(payload).hexdigest(),
        "pins": {"design": sha256(DESIGN.read_bytes()).hexdigest(),
                 "cover": sha256(COVER.read_bytes()).hexdigest()},
    }
    require(result["K14_pivot_uses"] == 6_619_280
            and result["K14_K3_tail_occurrences"] == 211_816_960, result)
    logical = dict(result)
    result["logical_sha256"] = sha256(json.dumps(
        logical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
