#!/usr/bin/env python3
"""Discovery: minimize the exact fixed-support-six partner unit packet."""

from __future__ import annotations

from collections import Counter
import importlib.util
from itertools import combinations
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "computations/unaudited-codex-n8-orbit0-normalized-78-2026-08-20"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CORE = load("n8_s6_partner_core",
            SOURCE / "audit_polarized_superpair_core_identity.py")
PROBE = load("n8_s6_partner_probe",
             SOURCE / "probe_cofactor_orientation_classes.py")
H = CORE.pure_hafnian()


def raw_variable(index):
    return Counter({(index,): 1})


ZERO_CELLS = frozenset((9, 10, 13, 14))


def specialize_zero_cells(poly):
    return Counter({monomial: coefficient for monomial, coefficient in poly.items()
                    if not any(variable in ZERO_CELLS for variable in monomial)})


ROWS = []
for edge in CORE.SUPER_EDGES:
    ROWS.append(("e_" + "".join(map(str, edge)), CORE.e_pair(*edge)))
for triple in combinations(range(4), 3):
    ROWS.append(("t_" + "".join(map(str, triple)),
                 CORE.t_triple(*triple)))
for edge in range(6):
    for position in (1, 2):
        ROWS.append((f"cofactor_{edge}_{position}",
                     PROBE.derivative(H, 4 * edge + position)))
for value in (3, 5, 6, 9, 10, 12):
    bits = tuple((value >> (3 - site)) & 1 for site in range(4))
    ROWS.append((f"Q_{value}", CORE.q_orientation(bits)))
for index in (9, 10, 13, 14):
    ROWS.append((f"cell_{index}", raw_variable(index)))


def unit(indices, timeout=30):
    variables = ",".join([f"x{i}" for i in range(24)
                          if i not in ZERO_CELLS] + ["u"])
    ideal = ",".join(PROBE.singular(specialize_zero_cells(ROWS[index][1]))
                     for index in indices)
    h = specialize_zero_cells(H)
    command = (
        f"ring R=0,({variables}),dp; ideal I={ideal},"
        f"u*({PROBE.singular(h)})-1; ideal G=slimgb(I); "
        "poly r=reduce(1,G); if(r==0){print(\"UNIT\");}"
        "else{print(\"NONUNIT\");}; quit;"
    )
    try:
        completed = subprocess.run(["Singular", "-q", "-c", command],
                                   text=True, capture_output=True,
                                   timeout=timeout, check=False)
    except subprocess.TimeoutExpired:
        return False
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr[-1000:])
    return "UNIT" in completed.stdout.split()


def main():
    active = list(range(len(ROWS) - len(ZERO_CELLS)))
    if not unit(active):
        raise RuntimeError("full fixed-left partner ideal is not unit")
    print("initial unit rows", len(active), flush=True)
    changed = True
    while changed:
        changed = False
        for index in tuple(reversed(active)):
            trial = [value for value in active if value != index]
            if unit(trial):
                active = trial
                changed = True
                print("deleted", ROWS[index][0], "remaining", len(active),
                      flush=True)
    print("MINIMAL", len(active))
    for index in active:
        print(index, ROWS[index][0])


if __name__ == "__main__":
    main()
