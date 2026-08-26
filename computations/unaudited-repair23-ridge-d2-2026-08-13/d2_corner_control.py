#!/usr/bin/env python3
r"""REPAIR PROBE (item 3, control): are the D1 rows load-bearing?

UNAUDITED.  Pinned to krenn-conjecture HEAD 7d57c552a3ef57d3a95c3bc933af547ad55e087d.

d2_corner_canonicity.py finds dim(F cap W) = 1 on ker(source, D1), i.e. the
D2 corner class is canonical up to scale.  A canonicity statement is only
meaningful if the constraints doing the work are the ones claimed.  This
control recomputes dim(F cap W) with the SOURCE ROWS ONLY (the first
endpoint-Spencer / D1 rows deleted from the constraint set).  If the answer
grows, the D1 rows are load-bearing; if it does not, the corner class was
already pinned by the source rows and the D1 half of the committed claim is
decorative.

A second control mutates one operator column (scaling its shadow entries) and
re-checks the positive control, so that a block that had lost contact with the
mathematics would be detected.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PRIME = (1 << 61) - 1


def load(relative, name, root):
    specification = importlib.util.spec_from_file_location(
        name, root / relative)
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


main_probe = load("d2_corner_canonicity.py", "repair23_d2c", HERE)


def restrict(columns, drop_kind):
    return [{row: value for row, value in column.items()
             if row[0] != drop_kind} for column in columns]


def run(columns, blocks, reference, shadow_kind, label):
    return main_probe.analyse(columns, blocks, reference, shadow_kind, PRIME,
                              label)


def main():
    columns, commutator, shadow_kind = main_probe.build_block(False)
    blocks, reference = main_probe.corner_blocks(commutator, shadow_kind)
    print("columns:", len(columns), flush=True)

    records = []

    baseline = run(columns, blocks, reference, shadow_kind, "source+D1")
    records.append(baseline)
    print(json.dumps({k: v for k, v in baseline.items()
                      if k != "attainable_corner_directions"},
                     sort_keys=True), flush=True)

    source_only = run(restrict(columns, 1), blocks, reference, shadow_kind,
                      "source only (D1 rows deleted)")
    records.append(source_only)
    print(json.dumps({k: v for k, v in source_only.items()
                      if k != "attainable_corner_directions"},
                     sort_keys=True), flush=True)
    print("  attainable corner directions:",
          source_only["attainable_corner_directions"], flush=True)

    # Mutation: scale the shadow entries of one column by 2.  The block then
    # no longer represents the committed operator; the positive control
    # (-delta attainable) or the dimension is expected to move.
    mutated = [dict(column) for column in columns]
    victim = next(index for index, column in enumerate(mutated)
                  if any(row[0] == shadow_kind for row in column))
    for row in list(mutated[victim]):
        if row[0] == shadow_kind:
            mutated[victim][row] = mutated[victim][row] * 3
    mutation = run(mutated, blocks, reference, shadow_kind,
                   "mutated shadow column")
    records.append(mutation)
    print(json.dumps({k: v for k, v in mutation.items()
                      if k != "attainable_corner_directions"},
                     sort_keys=True), flush=True)

    ledger = {
        "probe": "repair item 3 control: load-bearingness of the D1 rows",
        "status": "UNAUDITED REPAIR PROBE",
        "pinned_head": main_probe.PINNED_HEAD,
        "prime": PRIME,
        "records": records,
        "D1_rows_are_load_bearing":
            source_only["dim_F_cap_W"] > baseline["dim_F_cap_W"],
        "mutation_changes_the_answer": (
            mutation["dim_F_cap_W"] != baseline["dim_F_cap_W"]
            or not mutation["positive_control_minus_delta_attainable"]
            or mutation["attainable_corner_directions"]
            != baseline["attainable_corner_directions"]),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    print("D1 rows load-bearing:", ledger["D1_rows_are_load_bearing"])
    print("mutation detected   :", ledger["mutation_changes_the_answer"])
    print("ledger_sha256=" + sha256(payload.encode()).hexdigest())
    HERE.joinpath("ledger_d2_corner_control.json").write_text(
        json.dumps(ledger, sort_keys=True, indent=1) + "\n")


if __name__ == "__main__":
    main()
