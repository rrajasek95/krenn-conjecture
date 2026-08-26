#!/usr/bin/env python3
"""Independent arithmetic/provenance audit of the sealed 1028-witness referee."""

from __future__ import annotations

from collections import Counter
import json
import math
from pathlib import Path

import k23_direct_k15_contract as C


REF_SOURCE = C.GATE / "referee_k23_direct_k15_literal.rs"
REF_BINARY = C.GATE / "referee_k23_direct_k15_literal"
RESULT = C.GATE / "results_k23_direct_k15_literal_referee.json"
LEDGER = C.GATE / "k23_direct_k15_literal_samples.tsv"
PINS = {
    REF_SOURCE: "0678d51c89228109f62a141d8e9f39637686124101155df0b10842e733e5e6ca",
    REF_BINARY: "b53f0733f4e549633b072d4df688b20c90feccfefea6d2d03311a7deb296b5c4",
    RESULT: "da28e1d4402ef0903b25e1048bfbc5e614128a3bcc8d7623c7de975e3394ebb6",
    LEDGER: "9a685bc1d1ead2bb92f6757cc7dcf1f27c4ab90594d9e297e6e11562290158da",
}
HEADER = ("ordinal\tsource_slice\tpacket\tpacket_label\tsink\tsource_positive\t"
          "a\tb\tc\tintermediate_pivot_tail\tpivot_counts\tterminal_K23_children\t"
          "literal_charge\tweighted_charge_scaled_U")


def main():
    C.verify_pins()
    for path, digest in PINS.items():
        C.require(path.is_file() and C.sha256(path) == digest, f"literal referee pin {path.name}")
    result = json.loads(RESULT.read_text())
    C.require(result["status"] == "PASS_INDEPENDENT_257_DISTRIBUTED_LITERAL_DIRECT_K15_FOUR_SINK_K23_REPLAY",
              "literal status")
    C.require(result["source_samples"] == 257 and result["first_slice"] == 0 and
              result["last_slice"] == 484, "distributed endpoints")
    C.require(result["all_divisions_exact"] is True and
              result["all_literal_K23_children_terminal"] is True and
              result["terminal_anchor_signature_mass"] == 1 and
              result["source_provenance_preserved_through_all_pivots"] is True and
              result["cache_abstraction_used"] is False, "literal global assertions")
    lines = LEDGER.read_text().splitlines()
    C.require(len(lines) == 1029 and lines[0] == HEADER, "literal ledger schema/count")
    aggregates = {name: {"children": 0, "charge": 0, "scaled": 0,
                         "packets": Counter()} for name in C.NAMES}
    for ordinal in range(257):
        rows = [line.split("\t") for line in lines[1 + 4 * ordinal:1 + 4 * (ordinal + 1)]]
        source_slice = ordinal * 484 // 256
        packet = ordinal % 3
        label = ["322", "232", "223"][packet]
        C.require([row[4] for row in rows] == C.NAMES, f"sink order {ordinal}")
        for name, degrees, row in zip(C.NAMES, C.PATHS, rows):
            C.require(len(row) == 14, f"ledger field count {ordinal}/{name}")
            C.require((int(row[0]), int(row[1]), int(row[2]), row[3]) ==
                      (ordinal, source_slice, packet, label), f"distributed provenance {ordinal}/{name}")
            positive = int(row[5]); C.require(positive != 0, f"zero source {ordinal}/{name}")
            C.require(all(int(value) >= 0 for value in row[6:9]), f"factor ordinals {ordinal}/{name}")
            steps = [] if not row[9] else [tuple(map(int, item.split(":"))) for item in row[9].split(",")]
            C.require(len(steps) == len(degrees) - 1 and
                      all(0 <= pivot < 78 and tail >= 0 for pivot, tail in steps),
                      f"pivot/tail steps {ordinal}/{name}")
            divisors = list(map(int, row[10].split(",")))
            C.require(len(divisors) == len(degrees) and all(value > 0 for value in divisors),
                      f"divisor tuple {ordinal}/{name}")
            product = math.prod(divisors)
            C.require(C.U % product == 0, f"nonexact division {ordinal}/{name}")
            children, charge, scaled = map(int, row[11:14])
            terminal_fan = {2: 12, 3: 32, 4: 60}[degrees[-1]]
            C.require(children > 0 and children % terminal_fan == 0,
                      f"terminal fan {ordinal}/{name}")
            sign = -positive if len(degrees) % 2 == 0 else positive
            C.require(scaled == sign * (C.U // product) * charge,
                      f"signed U charge replay {ordinal}/{name}")
            agg = aggregates[name]
            agg["children"] += children; agg["charge"] += charge; agg["scaled"] += scaled
            agg["packets"][label] += 1
    for name, degrees in zip(C.NAMES, C.PATHS):
        sink = result["sinks"][name]
        C.require(sink["strict_grouped_ids"] == C.IDS[name] and sink["degrees"] == degrees,
                  f"referee group shape {name}")
        agg = aggregates[name]
        C.require(sink["samples"] == 257 and sink["packet_witness_counts"] ==
                  {"322": 86, "232": 86, "223": 85}, f"packet coverage {name}")
        C.require((sink["literal_terminal_K23_children"], int(sink["literal_charge_sum"]),
                   int(sink["sample_weighted_charge_scaled_U"])) ==
                  (agg["children"], agg["charge"], agg["scaled"]), f"aggregate replay {name}")
    print(json.dumps({
        "status": "PASS_K23_DIRECT_K15_INDEPENDENT_1028_WITNESS_REFEREE",
        "distributed_source_slices": 257, "literal_sink_witnesses": 1028,
        "first_slice": 0, "last_slice": 484,
        "packet_witnesses_per_sink": {"322": 86, "232": 86, "223": 85},
        "all_signed_U_divisions_and_aggregates_replayed": True,
        "terminality_proved_by_pinned_cache_free_Rust_referee": True,
        "referee_source_sha256": PINS[REF_SOURCE],
        "referee_binary_sha256": PINS[REF_BINARY],
        "ledger_sha256": PINS[LEDGER], "result_sha256": PINS[RESULT],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
