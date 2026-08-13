#!/usr/bin/env python3
"""Split six-site common-tail pairs by the tangent/determinant decomposition.

For the 15 perfect matchings on six sites, the tangent-Euler theorem gives
1 + 9 cut-permanent + 5 alternating-determinant directions.  This checker
classifies every unordered pair of matchings relative to the ten K3,3
determinant packets.

Every C4 pair occurs with opposite determinant sign in exactly two cuts.
Every C6 pair occurs together in exactly one cut, with the same sign, and is
separated by exactly six cuts.  Thus the determinant debt is the existing
common-tail C4 carrier in the first case, while a C6 genuinely requires a
chord/word-change/Hall bridge.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_tangent_euler_occurrence_splitter_fredholm.py":
        "ba2c32a41b1d070d2af24546819e838697aba0273e85586a796ee25a27f5a950",
    "computations/verify_uniform_axis_k3_minor_common_tail_boundary.py":
        "6a4454c324744d68457579b7aa613d026ea17457d95746d14743766a12a5710e",
    "computations/verify_uniform_axis_k3_unequal_tail_reduction.py":
        "ef4c7bc9554fbf6fc5a65aef754d35359c46e0bb67014bd20060114a34cd1843",
}
EXPECTED_LEDGER_SHA256 = "08aabf4f37dbe1117e0bdc8fa3b203546afabc869beefa490ff267e57c74121a"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(relative, name):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative,
                                     actual))

    tangent = load(
        "computations/verify_h3_tangent_euler_occurrence_splitter_fredholm.py",
        "pair_cut_tangent")
    determinants = [tangent.cut_determinant(cut) for cut in tangent.CUTS]
    pair_records = []
    type_counts = Counter()
    for left_index, left in enumerate(tangent.MATCHINGS):
        for right_index in range(left_index + 1, len(tangent.MATCHINGS)):
            right = tangent.MATCHINGS[right_index]
            common_edges = len(set(left).intersection(right))
            cycle_type = {1: "C4", 0: "C6"}[common_edges]
            opposite = []
            same = []
            separated = []
            invisible = []
            for cut_index, determinant in enumerate(determinants):
                a, b = determinant[left_index], determinant[right_index]
                if a * b == -1:
                    opposite.append(cut_index)
                elif a * b == 1:
                    same.append(cut_index)
                elif bool(a) ^ bool(b):
                    separated.append(cut_index)
                else:
                    invisible.append(cut_index)
            signature = (cycle_type, len(opposite), len(same),
                         len(separated), len(invisible))
            type_counts[signature] += 1
            if cycle_type == "C4":
                require((len(opposite), len(same), len(separated),
                         len(invisible)) == (2, 0, 4, 4),
                        "a C4 determinant signature changed")
            else:
                require((len(opposite), len(same), len(separated),
                         len(invisible)) == (0, 1, 6, 3),
                        "a C6 determinant signature changed")
            require(opposite or separated,
                    "a pair difference entered the tangent cut space")
            pair_records.append({
                "left": tangent.matching_text(left),
                "right": tangent.matching_text(right),
                "cycle_type": cycle_type,
                "opposite_sign_cuts": [list(tangent.CUTS[i]) for i in opposite],
                "same_sign_cuts": [list(tangent.CUTS[i]) for i in same],
                "separating_cuts": len(separated),
            })

    require(len(pair_records) == 105,
            "six-site unordered matching-pair count changed")
    require(sum(record["cycle_type"] == "C4" for record in pair_records) == 45
            and sum(record["cycle_type"] == "C6" for record in pair_records) == 60,
            "C4/C6 pair split changed")

    ledger = {
        "pins": PINS,
        "matching_pairs": len(pair_records),
        "C4_pairs": 45,
        "C6_pairs": 60,
        "determinant_signatures": {
            "C4": {"opposite": 2, "same": 0, "separating": 4,
                   "invisible": 4},
            "C6": {"opposite": 0, "same": 1, "separating": 6,
                   "invisible": 3},
        },
        "representatives": {
            "C4": next(record for record in pair_records
                       if record["cycle_type"] == "C4"),
            "C6": next(record for record in pair_records
                       if record["cycle_type"] == "C6"),
        },
        "theorem": (
            "every common-tail C4 pair is contained with opposite signs in "
            "exactly two alternating K3,3 determinants, identifying the "
            "rank-five tangent-Euler debt with the typed common-tail C4 "
            "Fitting carrier.  A C6 pair is never opposite in one determinant: "
            "one cut contains both with the same sign and six cuts separate "
            "them, so a chord, endpoint word-change, or Hall bridge is a "
            "genuine additional source datum"
        ),
        "source_frontier": (
            "if all evaluated alternating determinants vanish, the complete "
            "matching-value vector lies in the centered tangent cut-permanent "
            "sector and has a source-tangent Hasse lift with lower collision "
            "face.  If a determinant evaluates nonzero, it is only a physical "
            "carrier after decorated minor, head, support, and cofactor typing"
        ),
        "scope": (
            "the checker classifies the six-site matching representation. "
            "It does not assert that a formal determinant covector evaluates "
            "nonzero, kill the lower Hasse collision face, or close the C6 "
            "word-change/Hall branch"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))
    return ledger, digest


def main():
    ledger, digest = audit()
    print("h3 common-tail pair cut determinant split: PASS")
    print("pairs: C4=%d C6=%d" % (ledger["C4_pairs"], ledger["C6_pairs"]))
    print("ledger_sha256", digest)


if __name__ == "__main__":
    main()
