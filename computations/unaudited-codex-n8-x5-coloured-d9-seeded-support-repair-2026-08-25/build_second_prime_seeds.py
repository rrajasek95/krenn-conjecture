#!/usr/bin/env python3
"""Derive p=1000000007 D9 transport seeds from sealed integer D8 duals."""
import hashlib
import json
import os
from pathlib import Path

if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
P0, P1, T = 1073741827, 1000000007, 361
BRANCHES = {
    "triangle_endpoint_colour": ("5dd800c60fd8ac25c8aa4a315bec69d6ee8685ba25d5d1f0e769bc081d411095", "1a58301d9a316c37fda825bf1112d38b5bae19479308f7de23fe5ef7b0d8ee16"),
    "third_colour": ("181f1b799ed2b7b5018e719a94acc5f39ad541706f2baadb204afa67ab6eafd1", "e761815e90f949bce7ab32598749610e36db54293b87693a7af522241acde1ec"),
    "cap_endpoint_colour": ("a5b5b518ec4feeeab1c7b48584bbc97db0715db548ae32482ddc431cd9e010bf", "08aaff0a26cb8d4b382e889ea956e48654baf856f80810162fc19d12c2eba744"),
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
    for branch, (dual_sha, provider_sha) in BRANCHES.items():
        provider = HERE / f"provider_{branch}_p{P1}.ms"
        assert sha(provider) == provider_sha
        header = provider.open().readline().rstrip("\n").split(",")
        with provider.open() as stream:
            variables = stream.readline().rstrip("\n").split(",")
            characteristic = int(stream.readline())
            equation_count = sum(1 for _line in stream)
        assert header == variables and len(variables) == 361 and characteristic == P1 and equation_count == 6571
        d8 = REPO / f"computations/unaudited-codex-n8-x5-four-blocker-d8-two-prime-lift-2026-08-25/exact_lift_{branch}/integer_dual.tsv"
        assert sha(d8) == dual_sha
        transported = {}
        for line in d8.read_text().splitlines()[1:]:
            kind, raw, value = line.split("\t")
            row = tuple(map(int, raw.split(",")))
            assert kind == "ROW" and len(row) == 8
            transported[tuple(sorted(row + (T,)))] = int(value) % P1
        assert transported[(T,) * 9] == 1 and all(0 < value < P1 for value in transported.values())
        source_seed = HERE / f"seed_{branch}_p{P0}/selected.tsv"
        source_lines = source_seed.read_text().splitlines()
        assert source_lines[0] == "KRENN_X5_BLOCKER_D9_SELECTED_COLUMNS_V1" and len(source_lines) == 19
        directory = HERE / f"seed_{branch}_p{P1}"
        assert not directory.exists()
        directory.mkdir()
        (directory / "selected.tsv").write_text("\n".join(source_lines) + "\n")
        lines = [f"KRENN_X5_BLOCKER_D9_MODULAR_DUAL_V1\t{P1}\t{len(transported)}\t1"]
        lines.extend(f"ROW\t{','.join(map(str, row))}\t{value}" for row, value in sorted(transported.items()))
        (directory / "transported_d8_dual.tsv").write_text("\n".join(lines) + "\n")
        record = {
            "branch": branch,
            "prime": P1,
            "provider_sha256": provider_sha,
            "d8_integer_dual_sha256": dual_sha,
            "transported_support": len(transported),
            "selected_seed_columns": 18,
            "selected_sha256": sha(directory / "selected.tsv"),
            "transported_dual_sha256": sha(directory / "transported_d8_dual.tsv"),
            "selected_equals_first_prime": sha(directory / "selected.tsv") == sha(source_seed),
        }
        atomic(directory / "seed_audit.json", record)
        record["seed_audit_sha256"] = sha(directory / "seed_audit.json")
        records.append(record)
    result = {
        "schema": "KRENN_X5_COLOURED_D9_SECOND_PRIME_TRANSPORT_SEEDS_V1",
        "status": "PASS_THREE_SECOND_PRIME_SEEDS",
        "records": records,
    }
    atomic(HERE / "results_second_prime_seed_build.json", result)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
