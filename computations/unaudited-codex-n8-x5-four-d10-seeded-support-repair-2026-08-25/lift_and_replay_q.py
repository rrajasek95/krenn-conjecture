#!/usr/bin/env python3
"""Exact integer lift and literal incident-column replay of four D10 duals."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path

if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
AUDIT = REPO / "computations/unaudited-codex-n8-x5-four-dual-degree-recurrence-audit-2026-08-25/audit_recurrence.py"
AUDIT_SHA = "b0210a9c8a4a6361f4519aa91930563424fdca5f3d09ebb20e5425e6b2bdb2f9"
PRIMES = (1073741827, 1000000007)
BRANCHES = ("direct", "triangle_endpoint_colour", "third_colour", "cap_endpoint_colour")
T = 361

def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()

def audit_module():
    assert sha(AUDIT) == AUDIT_SHA
    spec = importlib.util.spec_from_file_location("sealed_recurrence_audit", AUDIT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module

def modular_dual(path, prime):
    lines = path.read_text().splitlines()
    header = lines[0].split("\t")
    assert header == ["KRENN_X5_BLOCKER_D10_MODULAR_DUAL_V1", str(prime), str(len(lines) - 1), "1"]
    answer = {}
    for line in lines[1:]:
        kind, raw, value = line.split("\t")
        row, value = tuple(map(int, raw.split(","))), int(value)
        assert kind == "ROW" and len(row) == 10 and row == tuple(sorted(row)) and 0 < value < prime and row not in answer
        answer[row] = value
    assert answer[(T,) * 10] == 1
    return answer

def signed(dual, prime):
    answer = {row: (value if value <= prime // 2 else value - prime) for row, value in dual.items()}
    # The D10 repair creates primitive coefficients of magnitude at most two
    # in the coloured branches (the direct branch remains +/-1).
    assert answer and 0 not in answer.values()
    assert max(abs(value) for value in answer.values()) <= 2 and answer[(T,) * 10] == 1
    return answer

def atomic(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)

def main():
    first = json.loads((HERE / "results_first_prime.json").read_text())
    second = json.loads((HERE / "results_second_prime.json").read_text())
    assert first["all_four_global_duals"] is True and second["all_four_global_duals"] is True
    audit = audit_module()
    records = []
    for branch in BRANCHES:
        maps, hashes = [], {}
        for prime in PRIMES:
            path = HERE / f"p{prime}_{branch}/dual.tsv"
            maps.append(signed(modular_dual(path, prime), prime))
            hashes[str(prime)] = sha(path)
        assert maps[0] == maps[1]
        integer = maps[0]
        generators = audit.load_provider(branch)
        incident_count, failures = audit.incident_replay(generators, integer)
        assert not failures
        directory = HERE / f"exact_lift_{branch}"
        directory.mkdir(exist_ok=True)
        lines = [f"KRENN_X5_BLOCKER_D10_PRIMITIVE_INTEGER_DUAL_V1\t{len(integer)}\t1"]
        lines.extend(f"ROW\t{','.join(map(str, row))}\t{value}" for row, value in sorted(integer.items()))
        certificate = directory / "integer_dual.tsv"
        certificate.write_text("\n".join(lines) + "\n")
        result = {
            "schema": "KRENN_X5_D10_CHARACTERISTIC_ZERO_LIFT_RESULT_V1",
            "status": "PASS_CHARACTERISTIC_ZERO_D10_DUAL_OBSTRUCTION", "branch": branch,
            "degree": 10, "target": "t^10", "primitive_integer_support": len(integer),
            "primitive_integer_target_coefficient": integer[(T,) * 10],
            "integer_weight_set": sorted(set(integer.values())), "two_prime_signed_maps_equal": True,
            "modular_dual_sha256": hashes, "integer_dual_sha256": sha(certificate),
            "literal_incident_columns_replayed": incident_count, "integer_pairing_failures": 0,
            "all_other_columns_support_disjoint": True, "degree_ten_rational_membership_excluded": True,
            "degree_eleven_launched": False,
        }
        atomic(directory / "result.json", result)
        result["result_sha256"] = sha(directory / "result.json")
        records.append(result)
    summary = {"schema": "KRENN_X5_FOUR_D10_CHARACTERISTIC_ZERO_LIFT_AUDIT_V1",
               "status": "PASS_FOUR_CHARACTERISTIC_ZERO_D10_DUAL_OBSTRUCTIONS", "records": records,
               "all_four_exact_integer_replays": True, "degree_eleven_launched": False}
    atomic(HERE / "results_characteristic_zero_lift.json", summary)
    print(json.dumps(summary, sort_keys=True))

if __name__ == "__main__":
    main()
