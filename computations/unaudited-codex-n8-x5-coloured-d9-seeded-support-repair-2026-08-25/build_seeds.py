#!/usr/bin/env python3
"""Build exact 18-column D9 repair seeds from transported coloured D8 duals."""
from collections import defaultdict
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
PRIME = 1073741827
T = 361
BRANCHES = ("triangle_endpoint_colour", "third_colour", "cap_endpoint_colour")


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def load_audit():
    assert sha(AUDIT) == AUDIT_SHA
    spec = importlib.util.spec_from_file_location("sealed_recurrence_audit", AUDIT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def vector(generators, column):
    generator, multiplier = column
    values = defaultdict(int)
    for term, coefficient in generators[generator][1]:
        values[tuple(sorted(term + multiplier))] += coefficient
    return {row: value % PRIME for row, value in values.items() if value % PRIME}


def pairing(values, dual):
    return sum(coefficient * dual.get(row, 0) for row, coefficient in values.items()) % PRIME


def solve(columns, vectors, target):
    frequency = defaultdict(int)
    for column in columns:
        for row, coefficient in vectors[column].items():
            if row != target and coefficient:
                frequency[row] += 1
    infinite = 1 << 60
    order = lambda row: (frequency.get(row, infinite), row)
    basis = {}
    for column in columns:
        raw = vectors[column]
        rhs = (-raw.get(target, 0)) % PRIME
        equation = {row: coefficient for row, coefficient in raw.items() if row != target and coefficient}
        inserted = False
        while equation:
            pivot = min(equation, key=order)
            value = equation[pivot]
            if pivot in basis:
                record, record_rhs = basis[pivot]
                for row, coefficient in record.items():
                    new = (equation.get(row, 0) - value * coefficient) % PRIME
                    if new:
                        equation[row] = new
                    else:
                        equation.pop(row, None)
                rhs = (rhs - value * record_rhs) % PRIME
                continue
            inverse = pow(value, PRIME - 2, PRIME)
            equation = {row: coefficient * inverse % PRIME for row, coefficient in equation.items()}
            rhs = rhs * inverse % PRIME
            basis[pivot] = (equation, rhs)
            inserted = True
            break
        if not inserted and rhs:
            return None
    candidate = {target: 1}
    for pivot in sorted(basis, key=order, reverse=True):
        record, rhs = basis[pivot]
        value = rhs
        for row, coefficient in record.items():
            if row != pivot:
                value = (value - coefficient * candidate.get(row, 0)) % PRIME
        if value:
            candidate[pivot] = value
    assert all(pairing(vectors[column], candidate) == 0 for column in columns)
    return candidate


def write_dual(path, dual, schema="KRENN_X5_BLOCKER_D9_MODULAR_DUAL_V1"):
    lines = [f"{schema}\t{PRIME}\t{len(dual)}\t1"]
    lines.extend(f"ROW\t{','.join(map(str, row))}\t{value}" for row, value in sorted(dual.items()))
    path.write_text("\n".join(lines) + "\n")


def atomic_json(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def main():
    audit = load_audit()
    records = []
    for branch in BRANCHES:
        generators = audit.load_provider(branch)
        d8, d8_path = audit.load_dual(8, branch)
        transported_integer = audit.extend_t(d8, 1)
        transported = {row: value % PRIME for row, value in transported_integer.items()}
        incident_count, failures = audit.incident_replay(generators, transported_integer)
        assert len(failures) == 18 and all(T not in item["multiplier"] for item in failures)
        columns = tuple(sorted((item["generator"], item["multiplier"]) for item in failures))
        assert len(set(columns)) == 18
        vectors = {column: vector(generators, column) for column in columns}
        assert all(pairing(vectors[column], transported) != 0 for column in columns)
        target = (T,) * 9
        postrepair = solve(columns, vectors, target)
        assert postrepair is not None and postrepair[target] == 1
        assert all(pairing(vectors[column], postrepair) == 0 for column in columns)
        directory = HERE / f"seed_{branch}_p{PRIME}"
        assert not directory.exists()
        directory.mkdir()
        selected_lines = ["KRENN_X5_BLOCKER_D9_SELECTED_COLUMNS_V1"]
        selected_lines.extend(
            f"COL\t{generator}\t{generators[generator][0]}\t{','.join(map(str, multiplier))}"
            for generator, multiplier in columns
        )
        (directory / "selected.tsv").write_text("\n".join(selected_lines) + "\n")
        write_dual(directory / "transported_d8_dual.tsv", transported)
        write_dual(directory / "postrepair_resume_dual.tsv", postrepair)
        record = {
            "branch": branch,
            "prime": PRIME,
            "provider_sha256": audit.PROVIDER_SHA[branch],
            "d8_integer_dual_sha256": sha(d8_path),
            "transported_support": len(transported),
            "transported_target_coefficient": transported[target],
            "transported_incident_columns": incident_count,
            "exact_transport_pairing_failures": len(failures),
            "all_offenders_t_free_c1": True,
            "offending_generator_histogram": dict(sorted((
                (str(generator), sum(1 for item in failures if item["generator"] == generator))
                for generator in set(item["generator"] for item in failures)
            ))),
            "selected_seed_columns": len(columns),
            "postrepair_support": len(postrepair),
            "postrepair_all_seed_pairings_zero": True,
            "selected_sha256": sha(directory / "selected.tsv"),
            "transported_dual_sha256": sha(directory / "transported_d8_dual.tsv"),
            "postrepair_resume_dual_sha256": sha(directory / "postrepair_resume_dual.tsv"),
        }
        atomic_json(directory / "seed_audit.json", record)
        record["seed_audit_sha256"] = sha(directory / "seed_audit.json")
        records.append(record)
    result = {
        "schema": "KRENN_X5_COLOURED_D9_18_COLUMN_SEED_BUILD_V1",
        "status": "PASS_THREE_EXACT_TRANSPORT_REPAIR_SEEDS",
        "records": records,
        "full_d9_closure_or_solve": False,
    }
    atomic_json(HERE / "results_seed_build.json", result)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
