#!/usr/bin/env python3
"""Bounded affine/homogeneous unit probe for a frozen recursive face chart."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import time


HERE = Path(__file__).resolve().parent
INPUT = HERE / "results_recursive_face_charts.json"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("key")
    parser.add_argument("--characteristic", type=int, default=1009)
    parser.add_argument("--timeout", type=float, default=120)
    parser.add_argument("--homogeneous", action="store_true")
    parser.add_argument("--modgb", action="store_true")
    parser.add_argument("--combined-localizer", action="store_true")
    parser.add_argument("--drop-localizer", action="append", default=[])
    parser.add_argument("--max-t-power", type=int, default=256)
    parser.add_argument("--print-basis", action="store_true")
    parser.add_argument("--extra-generator", action="append", default=[])
    args = parser.parse_args()
    payload = json.loads(INPUT.read_text())
    record = next(row for row in payload["states"] if row["key"] == args.key)
    generators = [row["polynomial"] for row in record["rows"]]
    localizers = [value for label, value in record["localizers"].items()
                  if label not in set(args.drop_localizer)]
    if args.combined_localizer:
        factors = []
        for value in localizers:
            require_suffix = value.endswith("-1") and "*(" in value
            if not require_suffix:
                raise RuntimeError("unexpected localizer encoding")
            factors.append(value[value.index("*(") + 1:-2])
        generators.append("s*" + "*".join(factors) + "-1")
        localizer_names = ["s"]
    else:
        generators += localizers
        localizer_names = ["u", "z", "w", "v"]
    generators += args.extra_generator
    names = record["variable_names"] + localizer_names
    names = [name for name in names
             if any(re.search(rf"\b{re.escape(name)}\b", generator)
                    for generator in generators)]
    if args.homogeneous:
        names.append("t")
    library = 'LIB "modstd.lib";' if args.modgb else ""
    basis = ('modGB("slimgb",J,1)' if args.modgb else "slimgb(J)")
    if args.homogeneous:
        test = (
            f'int hit=-1;for(int n=0;n<={args.max_t_power};n++)'
            '{if(hit<0 && reduce(t^n,G)==0){hit=n;}};print(hit);'
        )
        ideal_setup = f"ideal I={','.join(generators)};ideal J=homog(I,t);"
    else:
        test = 'print(string(reduce(1,G)));'
        ideal_setup = f"ideal I={','.join(generators)};ideal J=I;"
    basis_print = 'print("BASIS");print(G);' if args.print_basis else ""
    command = (
        f"{library}ring R={args.characteristic},({','.join(names)}),dp;"
        f"{ideal_setup}ideal G={basis};{basis_print}print(\"BEGIN\");{test}"
        'print(size(G));print(dim(G));print("END");quit;'
    )
    started = time.monotonic()
    try:
        singular = ["Singular"] + (["--cpus=1"] if args.modgb else [])
        completed = subprocess.run(
            singular + ["-q", "-c", command], text=True,
            capture_output=True, timeout=args.timeout, check=False,
        )
    except subprocess.TimeoutExpired:
        print(f"TIMEOUT after {time.monotonic() - started:.3f}s")
        return
    print("returncode:", completed.returncode)
    print(f"elapsed_seconds: {time.monotonic() - started:.3f}")
    print("active_names:", names)
    print(completed.stdout[-5000:])
    print(completed.stderr[-2000:])


if __name__ == "__main__":
    main()
