#!/usr/bin/env python3
"""Build exact p107 D10 seeds from the four characteristic-zero D9 duals."""
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
PRIME, T = 1073741827, 361
BRANCHES = ("direct", "triangle_endpoint_colour", "third_colour", "cap_endpoint_colour")
D9 = {
    "direct": ("computations/unaudited-codex-n8-x5-four-dual-degree-recurrence-audit-2026-08-25/d9_span_dual_direct.tsv", "8ee0166568fb24ce8f664ac2c0006991eca4dbbb929164e3620e5a106cc2c265"),
    "triangle_endpoint_colour": ("computations/unaudited-codex-n8-x5-coloured-d9-seeded-support-repair-2026-08-25/exact_lift_triangle_endpoint_colour/integer_dual.tsv", "93889d6212108f371d95f504be0b8f5b06a9f02fca3139881fb2289d8a40fa12"),
    "third_colour": ("computations/unaudited-codex-n8-x5-coloured-d9-seeded-support-repair-2026-08-25/exact_lift_third_colour/integer_dual.tsv", "ff23df3477d8d1784b9cfe40c53698a4acd56a35917c40d0bc94b45383033b94"),
    "cap_endpoint_colour": ("computations/unaudited-codex-n8-x5-coloured-d9-seeded-support-repair-2026-08-25/exact_lift_cap_endpoint_colour/integer_dual.tsv", "b59d2d6f4619f24fb77f01475c0980ad30ddb979e76042a978748992dffee7ac"),
}


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def module():
    assert sha(AUDIT) == AUDIT_SHA
    spec = importlib.util.spec_from_file_location("recurrence_audit", AUDIT)
    value = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(value)
    return value


def load_integer(path):
    lines = path.read_text().splitlines()
    header = lines[0].split("\t")
    count = int(header[1] if len(header) == 3 else header[2])
    target = int(header[2] if len(header) == 3 else header[3])
    assert count == len(lines) - 1 and target == 1
    answer = {}
    for line in lines[1:]:
        kind, raw, value = line.split("\t")
        row = tuple(map(int, raw.split(",")))
        value = int(value)
        assert kind == "ROW" and len(row) == 9 and row not in answer and value in (-1, 1)
        answer[row] = value
    assert answer[(T,) * 9] == 1
    return answer


def atomic(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def main():
    audit = module()
    records = []
    for branch in BRANCHES:
        d9_path = REPO / D9[branch][0]
        assert sha(d9_path) == D9[branch][1]
        d9 = load_integer(d9_path)
        transported_integer = {tuple(sorted(row + (T,))): value for row, value in d9.items()}
        transported = {row: value % PRIME for row, value in transported_integer.items()}
        generators = audit.load_provider(branch)
        incident_count, failures = audit.incident_replay(generators, transported_integer)
        columns = tuple(sorted((item["generator"], item["multiplier"]) for item in failures))
        assert len(columns) == len(set(columns)) and columns
        assert all(T not in multiplier for _generator, multiplier in columns)
        directory = HERE / f"seed_{branch}_p{PRIME}"
        assert not directory.exists()
        directory.mkdir()
        selected = ["KRENN_X5_BLOCKER_D10_SELECTED_COLUMNS_V1"]
        selected.extend(
            f"COL\t{generator}\t{generators[generator][0]}\t{','.join(map(str, multiplier))}"
            for generator, multiplier in columns
        )
        (directory / "selected.tsv").write_text("\n".join(selected) + "\n")
        dual = [f"KRENN_X5_BLOCKER_D10_MODULAR_DUAL_V1\t{PRIME}\t{len(transported)}\t1"]
        dual.extend(f"ROW\t{','.join(map(str, row))}\t{value}" for row, value in sorted(transported.items()))
        (directory / "transported_d9_dual.tsv").write_text("\n".join(dual) + "\n")
        record = {
            "branch": branch,
            "prime": PRIME,
            "provider_sha256": audit.PROVIDER_SHA[branch],
            "d9_integer_dual_sha256": D9[branch][1],
            "transported_support": len(transported),
            "transported_target_coefficient": transported[(T,) * 10],
            "transported_incident_columns": incident_count,
            "exact_transport_pairing_failures": len(failures),
            "all_offenders_t_free_c1": True,
            "offending_generator_histogram": dict(sorted((
                (str(generator), sum(1 for item in failures if item["generator"] == generator))
                for generator in set(item["generator"] for item in failures)
            ))),
            "selected_sha256": sha(directory / "selected.tsv"),
            "transported_dual_sha256": sha(directory / "transported_d9_dual.tsv"),
        }
        atomic(directory / "seed_audit.json", record)
        record["seed_audit_sha256"] = sha(directory / "seed_audit.json")
        records.append(record)
    result = {
        "schema": "KRENN_X5_FOUR_D10_TRANSPORT_SEED_BUILD_V1",
        "status": "PASS_FOUR_EXACT_D10_TRANSPORT_SEEDS",
        "records": records,
        "full_d10_closure_or_solve": False,
        "degree_eleven_launched": False,
    }
    atomic(HERE / "results_seed_build.json", result)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
