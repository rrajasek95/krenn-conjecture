#!/usr/bin/env python3
"""Fail-closed referee for a resource-capped D12 run."""

import argparse
import json
import struct
from pathlib import Path

from audit_affine251_orbit import INPUT_SHA, sha256


def checkpoint_header(path: Path):
    with path.open("rb") as stream:
        header = stream.read(46)
    assert header[:12] == b"AFF251CL1\0\0\0" and header[12] == 12
    complete = bool(header[13])
    rows, columns, row_frontier, column_frontier = struct.unpack_from("<QQQQ", header, 14)
    return complete, rows, columns, row_frontier, column_frontier


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--cegar", type=Path, required=True)
    parser.add_argument("--prolongation", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    assert sha256(args.input) == INPUT_SHA
    result = json.loads(args.result.read_text())
    assert result["schema"] == "KRENN_AFFINE251_ORBIT_MEMBERSHIP_V1"
    assert result["status"] == "INCOMPLETE_RESOURCE_GATE"
    assert result["incomplete_reason"] == "WALL_CAP" and result["degree"] == 12
    assert result["member_mod_prime"] is None and result["rank"] == -1
    assert result["wall_limit_seconds"] <= 780 and result["rss_limit_gib"] == 42
    complete, rows, columns, row_frontier, column_frontier = checkpoint_header(args.checkpoint)
    assert not complete and row_frontier + column_frontier > 0
    assert result["row_orbits"] == rows and result["column_orbits"] == columns
    cegar = json.loads(args.cegar.read_text())
    assert cegar["status"] == "INCOMPLETE_OR_TARGET_FORCED"
    assert cegar["searches"][0]["status"] == "WALL_CAP"
    prolongation = json.loads(args.prolongation.read_text())
    assert prolongation["status"] == "PASS_D8_D11_PROLONGATION_D12_COUNTERWITNESS"
    assert prolongation["first_failure"]["degree"] == 12
    audit = {
        "schema": "KRENN_AFFINE251_D12_INCOMPLETE_AUDIT_V1",
        "status": "PASS_INCOMPLETE_RESOURCE_GATE",
        "input_sha256": sha256(args.input),
        "result_sha256": sha256(args.result),
        "checkpoint_sha256": sha256(args.checkpoint),
        "cegar_sha256": sha256(args.cegar),
        "prolongation_sha256": sha256(args.prolongation),
        "row_orbits_discovered": rows,
        "column_orbits_discovered": columns,
        "row_frontier": row_frontier,
        "column_frontier": column_frontier,
        "closure_complete": False,
        "mathematical_verdict": None,
    }
    args.output.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n")
    print(json.dumps(audit, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
