#!/usr/bin/env python3
"""Discovery probe for the c=0 face of the branch-0 four-cycle stratum.

The source rows and denominator clearing come from
``probe_branch0_defect_support.py``.  We add the lossless residual-clone
gauge b2=b4=b5=d2=1 and the observed equations a_e*d_e=-1 on the four
cycle edges 1,2,3,4.  Output is discovery data, not a certificate.
"""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


PROBE = load("n8_branch0_cycle_probe", HERE / "probe_branch0_defect_support.py")


def command(characteristic, print_gb=False):
    support = (1, 2, 3, 4)
    rows, hafnian, _ = PROBE.derived(support)
    names = ([f"a{i}" for i in range(6)]
             + [f"b{i}" for i in range(6)]
             + [f"d{i}" for i in support] + ["z"])
    constraints = ["b2-1", "b4-1", "b5-1", "d2-1"]
    constraints += [f"a{i}*d{i}+1" for i in support]
    localization = (
        f"z*({PROBE.singular(hafnian)})*b0*b1*b3*d1*d3*d4-1"
    )
    generators = [row[3] for row in rows] + constraints + [localization]
    tail = ('print("BEGIN");size(G);dim(G);G;print("END");quit;'
            if print_gb else
            'print("BEGIN");size(G);dim(G);reduce(1,G);print("END");quit;')
    return (
        f"ring R={characteristic},({','.join(names)}),dp;"
        f"ideal I={','.join(generators)};"
        "ideal G=slimgb(I);"
        + tail
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--print-gb", action="store_true")
    args = parser.parse_args()
    for characteristic in (1009, 0):
        try:
            completed = subprocess.run(
                ["Singular", "-q", "-c", command(characteristic, args.print_gb)],
                text=True, capture_output=True, timeout=180, check=False,
            )
            print("characteristic", characteristic, "return", completed.returncode)
            print(completed.stdout)
            print(completed.stderr)
        except subprocess.TimeoutExpired:
            print("characteristic", characteristic, "TIMEOUT")


if __name__ == "__main__":
    main()
