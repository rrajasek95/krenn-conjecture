#!/usr/bin/env python3
"""Lightweight integrity replay for the bounded critical-span terminal."""

from hashlib import sha256
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
RESULT = HERE / "results_coloured_necklace_critical_span.json"
SELECTED = HERE / "coloured_necklace_critical_span_selected.tsv"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def main():
    result = json.loads(RESULT.read_text())
    selected = SELECTED.read_bytes()
    if "--mutate" in sys.argv:
        selected = selected[:-1] + bytes([selected[-1] ^ 1])
    require(result["status"] == "UNRESOLVED_CAP" and result["cap_reason"] == "time",
            (result["status"], result["cap_reason"]))
    require(result["modular_target_zero"] is False, result["modular_target_zero"])
    require(result["corrected_target_normal_support"] == 10_354, result)
    require(result["states_checked"] == 678, result["states_checked"])
    require(result["distinct_nonzero_critical_relations"] == 4_310, result)
    require(result["modular_critical_rank"] == result["selected_relation_rows"] == 4_046,
            result)
    require(result["modular_target_remainder_support"] == 10_353, result)
    require(sha256(selected).hexdigest() == result["selected_tsv_sha256"],
            "selected ledger digest mismatch")
    lines = selected.decode().splitlines()
    require(len(lines) == 1 + result["selected_relation_rows"], len(lines))
    require(lines[0] == "ordinal\tstate\tindices\tcuts\tdifference_support\tpivot",
            lines[0])
    require(all(int(row.split("\t", 1)[0]) == ordinal
                for ordinal, row in enumerate(lines[1:], 1)),
            "selected ordinals are not contiguous")
    logical = dict(result)
    stored = logical.pop("logical_sha256")
    logical.pop("elapsed_seconds")
    replay = sha256(json.dumps(logical, sort_keys=True,
                               separators=(",", ":")).encode()).hexdigest()
    require(replay == stored, (replay, stored))
    print(json.dumps({
        "status": "PASS bounded-result integrity replay",
        "logical_sha256": stored,
        "selected_tsv_sha256": result["selected_tsv_sha256"],
        "modular_target_zero": False,
        "scope": "integrity replay only; it does not rerun the 235-second discovery",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
