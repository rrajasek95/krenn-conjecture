#!/usr/bin/env python3
"""Fail-closed CLI and persistent-cache tests for sparse_d12_dual."""

import argparse
import json
import subprocess
import tempfile
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--vector-cache", type=Path, required=True)
    parser.add_argument("--ahead-vector-cache", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    binary = args.binary.resolve()
    input_path = args.input.resolve()
    checkpoint = args.checkpoint.resolve()
    vector_cache = args.vector_cache.resolve()
    ahead_vector_cache = args.ahead_vector_cache.resolve()
    rejected = []

    with tempfile.TemporaryDirectory() as name:
        root = Path(name)

        def command(**changes):
            values = {
                "--input": input_path,
                "--output": root / "result.json",
                "--checkpoint": checkpoint,
                "--vector-cache": vector_cache,
                "--dual": root / "dual.tsv",
                "--prime": "1073741827",
                "--wall-seconds": "20",
                "--rss-gib": "8",
                "--workers": "4",
                "--pivot": "first",
                "--strategy": "cold",
                "--incremental": "no",
                "--support-cap": "100000",
                "--column-cap": "1000000",
                "--round-cap": "5",
            }
            values.update(changes)
            cmd = [str(binary)]
            for key, value in values.items():
                cmd.extend((key, str(value)))
            return cmd

        cases = [
            ("even_modulus", command(**{"--prime": "10000"})),
            ("workers_above_contract", command(**{"--workers": "19"})),
            ("bad_pivot", command(**{"--pivot": "middle"})),
            ("bad_strategy", command(**{"--strategy": "hybrid"})),
            ("bad_incremental", command(**{"--incremental": "maybe"})),
            ("bad_elimination", command(**{"--elimination": "hash"})),
            ("incremental_vec_mismatch", command(**{"--incremental": "yes", "--elimination": "vec"})),
            ("bad_portfolio_period", command(**{"--portfolio-period": "0"})),
            ("bad_portfolio_parallel", command(**{"--portfolio-parallel": "maybe"})),
            ("support_below_contract", command(**{"--support-cap": "6"})),
            ("columns_below_contract", command(**{"--column-cap": "16"})),
            ("rounds_below_contract", command(**{"--round-cap": "0"})),
            ("cache_ahead_of_checkpoint", command(**{"--vector-cache": ahead_vector_cache})),
        ]

        corrupted_provider = root / "provider-corrupt.bin"
        payload = bytearray(vector_cache.read_bytes())
        payload[20] ^= 1
        corrupted_provider.write_bytes(payload)
        cases.append(("cache_provider_fingerprint", command(**{"--vector-cache": corrupted_provider})))

        corrupted_checksum = root / "checksum-corrupt.bin"
        payload = bytearray(vector_cache.read_bytes())
        payload[28] ^= 1
        corrupted_checksum.write_bytes(payload)
        cases.append(("cache_vector_checksum", command(**{"--vector-cache": corrupted_checksum})))

        truncated = root / "truncated.bin"
        truncated.write_bytes(vector_cache.read_bytes()[:100])
        cases.append(("cache_truncated", command(**{"--vector-cache": truncated})))

        for label, cmd in cases:
            (root / "result.json").unlink(missing_ok=True)
            (root / "dual.tsv").unlink(missing_ok=True)
            run = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert run.returncode == 2 and not (root / "result.json").exists(), (label, run.returncode, run.stderr[-200:])
            rejected.append(label)

        (root / "result.json").unlink(missing_ok=True)
        run = subprocess.run(command(), check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = json.loads((root / "result.json").read_text())
        assert run.returncode == 0
        assert result["status"] == "INCOMPLETE_SEARCH_CAP" and result["incomplete_reason"] == "ROUND_CAP"
        assert result["cached_vectors_loaded"] == 308 and result["vectors_materialized_on_restore"] == 0
        assert result["global_annihilation"] is None and result["target_pairing"] is None

    report = {
        "schema": "KRENN_AFFINE251_D12_SPARSE_HOSTILE_SELFTEST_V1",
        "status": "PASS",
        "hard_rejections": rejected,
        "warm_cache_round_cap_fail_closed": True,
        "tests": len(rejected) + 1,
    }
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
