#!/usr/bin/env python3
"""Mutation tests for the exact D12 continuation audit."""

import argparse
import json
import subprocess
import tempfile
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", type=Path, required=True)
    parser.add_argument("--base-result", type=Path, required=True)
    parser.add_argument("--period1-result", type=Path, required=True)
    parser.add_argument("--continuation-result", type=Path, required=True)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--vectors", type=Path, required=True)
    parser.add_argument("--fixed-result", type=Path, required=True)
    parser.add_argument("--fixed-checkpoint", type=Path, required=True)
    parser.add_argument("--fixed-vectors", type=Path, required=True)
    parser.add_argument(
        "--advanced-state", nargs=3, action="append", default=[],
        metavar=("RESULT", "CHECKPOINT", "VECTORS"),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    originals = {
        "base": json.loads(args.base_result.read_text()),
        "period1": json.loads(args.period1_result.read_text()),
        "continuation": json.loads(args.continuation_result.read_text()),
    }
    for index, (result, _checkpoint, _vectors) in enumerate(args.advanced_state):
        originals[f"advanced_{index}"] = json.loads(Path(result).read_text())
    latest_name = f"advanced_{len(args.advanced_state) - 1}" if args.advanced_state else "continuation"
    mutations = {
        "forged_complete": ("continuation", "status", "COMPLETE_MODULAR_DUAL"),
        "forged_pairing": ("continuation", "target_pairing", 1),
        "wrong_latest_columns": (latest_name, "column_orbits_exposed", 333_198),
        "wrong_period1_pivot": ("period1", "rounds.0.selected_pivot", "first"),
        "wrong_base_state": ("base", "rounds_completed", 539),
    }
    rejected = []
    with tempfile.TemporaryDirectory() as tmp_name:
        tmp = Path(tmp_name)
        for label, (which, field, value) in mutations.items():
            values = {name: json.loads(json.dumps(payload)) for name, payload in originals.items()}
            target = values[which]
            path = field.split(".")
            for token in path[:-1]:
                target = target[int(token)] if token.isdigit() else target[token]
            last = path[-1]
            if last.isdigit():
                target[int(last)] = value
            else:
                target[last] = value
            paths = {}
            for name, payload in values.items():
                paths[name] = tmp / f"{label}_{name}.json"
                paths[name].write_text(json.dumps(payload) + "\n")
            result = tmp / f"{label}_audit.json"
            command = [
                "python3", str(args.audit),
                "--base-result", str(paths["base"]),
                "--period1-result", str(paths["period1"]),
                "--continuation-result", str(paths["continuation"]),
                "--checkpoint", str(args.checkpoint),
                "--vectors", str(args.vectors),
                "--fixed-result", str(args.fixed_result),
                "--fixed-checkpoint", str(args.fixed_checkpoint),
                "--fixed-vectors", str(args.fixed_vectors),
                "--output", str(result),
            ]
            for index, (_advanced_result, advanced_checkpoint, advanced_vectors) in enumerate(args.advanced_state):
                command.extend([
                    "--advanced-state",
                    str(paths[f"advanced_{index}"]),
                    str(advanced_checkpoint),
                    str(advanced_vectors),
                ])
            run = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert run.returncode != 0 and not result.exists(), label
            rejected.append(label)

    report = {
        "schema": "KRENN_AFFINE251_D12_PORTFOLIO_HOSTILE_SELFTEST_V1",
        "status": "PASS",
        "rejected": rejected,
        "tests": len(rejected),
    }
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
