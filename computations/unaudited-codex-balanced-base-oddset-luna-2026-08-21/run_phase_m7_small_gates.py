#!/usr/bin/env python3
"""Run the bounded family of tiny exact m=7 coefficient gates."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "manifest_phase_m7_small_gates.json"
OUTPUT = HERE / "results_phase_m7_small_gates.json"


def run(item):
    try:
        completed = subprocess.run(
            ["Singular", "-q", item["path"]], cwd=HERE,
            capture_output=True, text=True, timeout=20, check=False,
        )
        output = completed.stdout.strip()
        fields = output.splitlines()
        unit = (completed.returncode == 0 and "SENTINEL_BEGIN" in fields
                and fields[-2:] == ["0", "SENTINEL_END"])
        return {
            **item,
            "exit_code": completed.returncode,
            "timed_out": False,
            "stdout": output,
            "stderr": completed.stderr.strip(),
            "unit": unit,
        }
    except subprocess.TimeoutExpired as error:
        return {
            **item,
            "exit_code": None,
            "timed_out": True,
            "stdout": (error.stdout or "").strip(),
            "stderr": (error.stderr or "").strip(),
            "unit": False,
        }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text())
    flat = [(branch, item) for branch, items in manifest.items() for item in items]
    results = {branch: [] for branch in manifest}
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(run, item): branch for branch, item in flat}
        for future in as_completed(futures):
            branch = futures[future]
            results[branch].append(future.result())
    for items in results.values():
        items.sort(key=lambda item: item["orbit"])
    summary = {
        branch: {
            "gates": len(items),
            "unit": sum(item["unit"] for item in items),
            "nonunit": sum(not item["unit"] and not item["timed_out"] for item in items),
            "timeout": sum(item["timed_out"] for item in items),
            "first_nonunit": next((item["orbit"] for item in items
                                   if not item["unit"] and not item["timed_out"]), None),
        }
        for branch, items in results.items()
    }
    args.output.write_text(json.dumps({"summary": summary, "results": results},
                                     indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
