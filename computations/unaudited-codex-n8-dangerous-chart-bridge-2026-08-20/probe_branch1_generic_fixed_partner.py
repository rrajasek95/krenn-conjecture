#!/usr/bin/env python3
"""Discovery probe for arbitrary mates of the two T-nonzero components."""

from __future__ import annotations

from collections import Counter
import importlib.util
from itertools import combinations
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "unaudited-codex-n8-orbit0-normalized-78-2026-08-20"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CORE = load("n8_b1_mate_core", SOURCE / "audit_polarized_superpair_core_identity.py")
PROBE = load("n8_b1_mate_probe", SOURCE / "probe_cofactor_orientation_classes.py")
H = CORE.pure_hafnian()
Q_ZEROS = (3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15)
LEFT_C = {"p14": (3, 5, 6, 17, 18),
          "pm2": (3, 9, 10, 13, 14)}


def raw_variable(index):
    return Counter({(index,): 1})


def q(value):
    return CORE.q_orientation(tuple((value >> (3 - site)) & 1
                                    for site in range(4)))


def main():
    base = [CORE.e_pair(*edge) for edge in CORE.SUPER_EDGES]
    base += [CORE.t_triple(*triple)
             for triple in combinations(range(4), 3)]
    base += [PROBE.derivative(H, 4 * edge + position)
             for edge in range(6) for position in (0, 1, 2)]
    base += [q(value) for value in Q_ZEROS]
    variables = ",".join(f"x{index}" for index in range(24))
    for name, cells in LEFT_C.items():
        equations = base + [raw_variable(index) for index in cells]
        ideal = ",".join(PROBE.singular(poly) for poly in equations)
        command = (
            f"ring R=0,({variables}),dp; ideal I={ideal}; "
            "ideal G=slimgb(I); poly r=reduce(1,G); "
            'if(r==0){print("UNIT");}else{print("NONUNIT");}; '
            "print(size(G)); print(dim(G)); quit;"
        )
        try:
            completed = subprocess.run(["Singular", "-q", "-c", command],
                                       text=True, capture_output=True,
                                       timeout=120, check=False)
            print(name, "return", completed.returncode,
                  "stdout", completed.stdout.splitlines()[-3:],
                  "stderr", completed.stderr[-500:], flush=True)
        except subprocess.TimeoutExpired:
            print(name, "TIMEOUT", flush=True)


if __name__ == "__main__":
    main()
