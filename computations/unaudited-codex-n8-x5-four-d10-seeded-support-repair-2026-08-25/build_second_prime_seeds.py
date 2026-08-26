#!/usr/bin/env python3
"""Derive p=1000000007 D10 transport seeds from sealed integer D9 duals."""
import hashlib
import json
import os
from pathlib import Path

if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
P0, P1, T = 1073741827, 1000000007, 361
RECURRENCE = REPO / "computations/unaudited-codex-n8-x5-four-dual-degree-recurrence-audit-2026-08-25"
COLOURED = REPO / "computations/unaudited-codex-n8-x5-coloured-d9-seeded-support-repair-2026-08-25"
BRANCHES = {
    "direct": (RECURRENCE / "d9_span_dual_direct.tsv", "8ee0166568fb24ce8f664ac2c0006991eca4dbbb929164e3620e5a106cc2c265", "343383c57eed5de414052f8defeaa91784dd9ced0df5355338e328f346f8a3a1"),
    "triangle_endpoint_colour": (COLOURED / "exact_lift_triangle_endpoint_colour/integer_dual.tsv", "93889d6212108f371d95f504be0b8f5b06a9f02fca3139881fb2289d8a40fa12", "1a58301d9a316c37fda825bf1112d38b5bae19479308f7de23fe5ef7b0d8ee16"),
    "third_colour": (COLOURED / "exact_lift_third_colour/integer_dual.tsv", "ff23df3477d8d1784b9cfe40c53698a4acd56a35917c40d0bc94b45383033b94", "e761815e90f949bce7ab32598749610e36db54293b87693a7af522241acde1ec"),
    "cap_endpoint_colour": (COLOURED / "exact_lift_cap_endpoint_colour/integer_dual.tsv", "b59d2d6f4619f24fb77f01475c0980ad30ddb979e76042a978748992dffee7ac", "08aaff0a26cb8d4b382e889ea956e48654baf856f80810162fc19d12c2eba744"),
}

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
    records = []
    for branch, (d9, d9_sha, provider_sha) in BRANCHES.items():
        provider = HERE / f"provider_{branch}_p{P1}.ms"
        assert sha(provider) == provider_sha and sha(d9) == d9_sha
        with provider.open() as stream:
            variables = stream.readline().rstrip("\n").split(",")
            characteristic = int(stream.readline())
            equation_count = sum(1 for _line in stream)
        assert len(variables) == 361 and characteristic == P1 and equation_count == 6571
        transported = {}
        for line in d9.read_text().splitlines()[1:]:
            kind, raw, value = line.split("\t")
            row = tuple(map(int, raw.split(",")))
            assert kind == "ROW" and len(row) == 9 and row == tuple(sorted(row))
            transported[tuple(sorted(row + (T,)))] = int(value) % P1
        assert transported[(T,) * 10] == 1 and all(0 < value < P1 for value in transported.values())
        source_seed = HERE / f"seed_{branch}_p{P0}/selected.tsv"
        source_lines = source_seed.read_text().splitlines()
        assert source_lines[0] == "KRENN_X5_BLOCKER_D10_SELECTED_COLUMNS_V1"
        directory = HERE / f"seed_{branch}_p{P1}"
        assert not directory.exists()
        directory.mkdir()
        (directory / "selected.tsv").write_text("\n".join(source_lines) + "\n")
        lines = [f"KRENN_X5_BLOCKER_D10_MODULAR_DUAL_V1\t{P1}\t{len(transported)}\t1"]
        lines.extend(f"ROW\t{','.join(map(str, row))}\t{value}" for row, value in sorted(transported.items()))
        (directory / "transported_d9_dual.tsv").write_text("\n".join(lines) + "\n")
        record = {
            "branch": branch, "prime": P1, "provider_sha256": provider_sha,
            "d9_integer_dual_sha256": d9_sha, "transported_support": len(transported),
            "selected_seed_columns": len(source_lines) - 1,
            "selected_sha256": sha(directory / "selected.tsv"),
            "transported_dual_sha256": sha(directory / "transported_d9_dual.tsv"),
            "selected_equals_first_prime": sha(directory / "selected.tsv") == sha(source_seed),
        }
        atomic(directory / "seed_audit.json", record)
        record["seed_audit_sha256"] = sha(directory / "seed_audit.json")
        records.append(record)
    result = {"schema": "KRENN_X5_FOUR_D10_SECOND_PRIME_TRANSPORT_SEEDS_V1", "status": "PASS_FOUR_SECOND_PRIME_SEEDS", "records": records}
    atomic(HERE / "results_second_prime_seed_build.json", result)
    print(json.dumps(result, sort_keys=True))

if __name__ == "__main__":
    main()
