#!/usr/bin/env python3
"""Fail-closed CLI/resource/checkpoint tests for the native solver."""

import argparse
import json
import subprocess
import tempfile
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--d8-checkpoint", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rejected = []
    with tempfile.TemporaryDirectory() as name:
        root = Path(name)

        def command(degree="8", prime="1073741827", workers="4", wall="30", checkpoint=None,
                    pivot="first"):
            return [str(args.binary), "--input", str(args.input), "--degree", degree,
                    "--prime", prime, "--output", str(root / "result.json"),
                    "--checkpoint", str(checkpoint or root / "closure.bin"),
                    "--dual", str(root / "dual.tsv"), "--wall-seconds", wall,
                    "--rss-gib", "42", "--workers", workers, "--pivot", pivot]

        cases = [
            ("degree_below_contract", command(degree="3")),
            ("degree_above_contract", command(degree="13")),
            ("composite_even_modulus", command(prime="10000")),
            ("worker_count_above_host", command(workers="19")),
            ("invalid_pivot_order", command(pivot="middle")),
            ("checkpoint_degree_mismatch", command(degree="9", checkpoint=args.d8_checkpoint)),
        ]
        for label, cmd in cases:
            (root / "result.json").unlink(missing_ok=True)
            run = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert run.returncode == 2 and not (root / "result.json").exists(), (label, run.returncode)
            rejected.append(label)

        capped = subprocess.run(command(wall="0"), check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        data = json.loads((root / "result.json").read_text())
        assert capped.returncode == 0
        assert data["status"] == "INCOMPLETE_RESOURCE_GATE" and data["incomplete_reason"] == "WALL_CAP"
        assert data["member_mod_prime"] is None and data["rank"] == -1
    result = {
        "schema": "KRENN_AFFINE251_HOSTILE_SELFTEST_V1",
        "status": "PASS",
        "hard_rejections": rejected,
        "resource_cap_fail_closed": True,
        "tests": len(rejected) + 1,
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
