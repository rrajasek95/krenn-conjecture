#!/usr/bin/env python3
"""Certify the zero-repair direct D11 transport over the integers."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path

if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
T = 361
PRIME = 1073741827
AUDIT = REPO / "computations/unaudited-codex-n8-x5-four-dual-degree-recurrence-audit-2026-08-25/audit_recurrence.py"
AUDIT_SHA = "b0210a9c8a4a6361f4519aa91930563424fdca5f3d09ebb20e5425e6b2bdb2f9"
D10 = REPO / "computations/unaudited-codex-n8-x5-four-d10-seeded-support-repair-2026-08-25/exact_lift_direct/integer_dual.tsv"
D10_SHA = "c639faa986903b66d003dc4513bb9ad029f5b0027dd15714d8c5449a494c8246"

def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()

def atomic(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)

def main():
    assert sha(AUDIT) == AUDIT_SHA and sha(D10) == D10_SHA
    spec = importlib.util.spec_from_file_location("sealed_audit", AUDIT)
    audit = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(audit)
    d10 = {}
    for line in D10.read_text().splitlines()[1:]:
        kind, raw, value = line.split("\t")
        row, value = tuple(map(int, raw.split(","))), int(value)
        assert kind == "ROW" and len(row) == 10 and row not in d10 and value in (-1, 1)
        d10[row] = value
    integer = {tuple(sorted(row + (T,))): value for row, value in d10.items()}
    assert integer[(T,) * 11] == 1 and len(integer) == 243
    generators = audit.load_provider("direct")
    incident_count, failures = audit.incident_replay(generators, integer)
    assert not failures
    modular_lines = (HERE / f"p{PRIME}_direct/dual.tsv").read_text().splitlines()
    modular = {tuple(map(int, line.split("\t")[1].split(","))): int(line.split("\t")[2]) for line in modular_lines[1:]}
    assert modular == {row: value % PRIME for row, value in integer.items()}
    directory = HERE / "exact_lift_direct"
    assert not directory.exists()
    directory.mkdir()
    lines = [f"KRENN_X5_BLOCKER_D11_PRIMITIVE_INTEGER_DUAL_V1\t{len(integer)}\t1"]
    lines.extend(f"ROW\t{','.join(map(str, row))}\t{value}" for row, value in sorted(integer.items()))
    certificate = directory / "integer_dual.tsv"
    certificate.write_text("\n".join(lines) + "\n")
    result = {"schema": "KRENN_X5_DIRECT_D11_EXACT_TRANSPORT_RESULT_V1",
              "status": "PASS_DIRECT_CHARACTERISTIC_ZERO_D11_OBSTRUCTION", "branch": "direct",
              "degree": 11, "target": "t^11", "support": len(integer), "weight_set": [-1, 1],
              "target_coefficient": 1, "literal_incident_columns_replayed": incident_count,
              "pairing_failures": 0, "p107_modular_reduction_equal": True,
              "d10_integer_dual_sha256": D10_SHA, "integer_dual_sha256": sha(certificate),
              "degree_twelve_launched": False}
    atomic(directory / "result.json", result)
    print(json.dumps(result, sort_keys=True))

if __name__ == "__main__":
    main()
