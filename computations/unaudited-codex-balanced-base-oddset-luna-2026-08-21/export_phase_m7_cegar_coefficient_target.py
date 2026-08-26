#!/usr/bin/env python3
"""Export a literal coefficient target for one CEGAR support iteration."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from audit_phase_m7_support_coefficients import replay_model  # noqa: E402


def atom_tuple(name):
    return tuple(map(int, name.split("_")[1:]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--iteration", type=int, required=True)
    parser.add_argument("--input", type=Path,
                        default=HERE / "results_phase_m7_1222_k4_cegar.json")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.input.read_text())
    record = data["iterations"][args.iteration - 1]
    support = frozenset(atom_tuple(name) for name in record["support"])
    replay = replay_model(support)
    output = {
        "branch": "1222_k4_C1222",
        "cegar_iteration": args.iteration,
        "coefficient_system": replay,
    }
    args.output.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(args.iteration, replay["variable_count"], replay["mixed_equation_count"])


if __name__ == "__main__":
    main()
