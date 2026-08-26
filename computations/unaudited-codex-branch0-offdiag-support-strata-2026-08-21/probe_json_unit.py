#!/usr/bin/env python3
"""Run a bounded Singular unit test on a frozen JSON generator interface.

This is a discovery helper, not a theorem artifact.  It deliberately prints
the exact generator labels and replacement used so a successful probe can be
rebuilt from the raw packet before being cited.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import time


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("interface", type=Path)
    parser.add_argument("--characteristic", type=int, default=1009)
    parser.add_argument("--timeout", type=float, default=120)
    parser.add_argument("--order", default="dp")
    parser.add_argument("--algorithm", choices=("slimgb", "std"),
                        default="slimgb")
    parser.add_argument("--compact-variables", action="store_true")
    parser.add_argument(
        "--replace-last",
        help="replace the final generator (normally the product C localizer)",
    )
    parser.add_argument(
        "--drop-label",
        action="append",
        default=[],
        help="drop every generator with this exact frozen label",
    )
    args = parser.parse_args()

    payload = json.loads(args.interface.read_text())
    names = payload["variables"]
    generators = list(payload["generators"])
    labels = list(payload["labels"])
    if args.replace_last is not None:
        generators[-1] = args.replace_last
        labels[-1] = "C_SINGLE"
    kept = [(generator, label) for generator, label in zip(generators, labels)
            if label not in set(args.drop_label)]
    generators = [generator for generator, _ in kept]
    labels = [label for _, label in kept]
    if args.compact_variables:
        names = [name for name in names
                 if any(re.search(rf"\b{re.escape(name)}\b", generator)
                        for generator in generators)]

    command = (
        f"ring R={args.characteristic},({','.join(names)}),{args.order};"
        f"ideal I={','.join(generators)};"
        f'ideal G={args.algorithm}(I);print("BEGIN");'
        'print(string(reduce(1,G)));'
        'print(size(G));print(dim(G));print("END");quit;'
    )
    started = time.monotonic()
    try:
        completed = subprocess.run(
            ["Singular", "-q", "-c", command],
            text=True,
            capture_output=True,
            timeout=args.timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        elapsed = time.monotonic() - started
        print(f"TIMEOUT after {elapsed:.3f}s")
        print("labels:", labels)
        return

    elapsed = time.monotonic() - started
    print("returncode:", completed.returncode)
    print(f"elapsed_seconds: {elapsed:.3f}")
    print("labels:", labels)
    print("replacement:", args.replace_last)
    print(completed.stdout[-4000:])
    print(completed.stderr[-1000:])


if __name__ == "__main__":
    main()
