#!/usr/bin/env python3
"""Independent integer and two-prime replay of the three coloured D9 duals."""
from collections import defaultdict
import hashlib
import itertools
import json
import os
from pathlib import Path

if not __debug__:
    raise RuntimeError("assertions required")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
T = 361
BRANCHES = {
    "triangle_endpoint_colour": "06df5052a50099dc400d622323257fef9b3077a791f918c8f1c46d7bf7a5782c",
    "third_colour": "b5ce054d529a5390c366254d08e43595cfa16e04854514f80db1b34f109d4ae8",
    "cap_endpoint_colour": "d040d1525989588bce3b912413aa6841869de63575bb3ebf976de817869e0b64",
}
PRIMES = (1073741827, 1000000007)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tokens(line):
    line = line.rstrip("\n,")
    out, start, sign = [], 0, 1
    if line[0] in "+-":
        sign, start = (-1 if line[0] == "-" else 1), 1
    for i in range(start, len(line)):
        if line[i] in "+-":
            out.append((sign, line[start:i]))
            sign, start = (-1 if line[i] == "-" else 1), i + 1
    out.append((sign, line[start:]))
    return out


def provider(path, expected_sha):
    assert sha(path) == expected_sha
    with path.open() as stream:
        variables = stream.readline().rstrip("\n").split(",")
        assert len(variables) == 361 and int(stream.readline()) == 1073741827
        ids = {name: i for i, name in enumerate(variables)}
        generators = []
        for line in stream:
            raw = []
            for coefficient, token in tokens(line):
                term = () if token == "1" else tuple(sorted(ids[x] for x in token.split("*")))
                raw.append((term, coefficient))
            degree = max(map(lambda x: len(x[0]), raw))
            combined = defaultdict(int)
            for term, coefficient in raw:
                combined[tuple(sorted(term + (T,) * (degree - len(term))))] += coefficient
            generators.append((degree, tuple((row, c) for row, c in sorted(combined.items()) if c)))
    assert len(generators) == 6571
    return generators


def dual(path, degree):
    lines = path.read_text().splitlines()
    header = lines[0].split("\t")
    if len(header) == 3:
        assert int(header[1]) == len(lines) - 1 and int(header[2]) == 1
    else:
        assert len(header) == 4 and int(header[2]) == len(lines) - 1 and int(header[3]) == 1
    out = {}
    for line in lines[1:]:
        kind, raw, value = line.split("\t")
        row = tuple(map(int, raw.split(",")))
        assert kind == "ROW" and len(row) == degree and row == tuple(sorted(row)) and row not in out
        out[row] = int(value)
    assert out[(T,) * degree] == 1
    return out


def quotient(row, divisor):
    answer, j = [], 0
    for x in row:
        if j < len(divisor) and x == divisor[j]:
            j += 1
        else:
            answer.append(x)
    return tuple(answer) if j == len(divisor) else None


def main():
    records = []
    for branch, provider_sha in BRANCHES.items():
        provider_path = REPO / f"computations/unaudited-codex-n8-x5-four-blocker-d6-cegar-gate-2026-08-25/provider_{branch}.ms"
        generators = provider(provider_path, provider_sha)
        integer_path = HERE / f"exact_lift_{branch}/integer_dual.tsv"
        integer = dual(integer_path, 9)
        assert set(integer.values()) == {-1, 1}
        term_index = defaultdict(set)
        for g, (_degree, terms) in enumerate(generators):
            for term, coefficient in terms:
                if coefficient:
                    term_index[term].add(g)
        columns = set()
        for row in integer:
            for degree in (2, 3, 4):
                for positions in itertools.combinations(range(9), degree):
                    divisor = tuple(row[i] for i in positions)
                    multiplier = quotient(row, divisor)
                    for g in term_index.get(divisor, ()):
                        columns.add((g, multiplier))
        for g, multiplier in columns:
            value = sum(c * integer.get(tuple(sorted(term + multiplier)), 0) for term, c in generators[g][1])
            assert value == 0
        modular_equal = {}
        for prime in PRIMES:
            modular = dual(HERE / f"p{prime}_{branch}/dual.tsv", 9)
            reduced = {row: value % prime for row, value in integer.items()}
            assert modular == reduced
            modular_equal[str(prime)] = True
        records.append({
            "branch": branch,
            "provider_sha256": provider_sha,
            "integer_dual_sha256": sha(integer_path),
            "support": len(integer),
            "weight_set": sorted(set(integer.values())),
            "target_coefficient": integer[(T,) * 9],
            "literal_incident_columns_replayed": len(columns),
            "pairing_failures": 0,
            "modular_reductions_equal": modular_equal,
        })
    result = {
        "schema": "KRENN_X5_THREE_COLOURED_D9_INDEPENDENT_INTEGER_REPLAY_V1",
        "status": "PASS_THREE_CHARACTERISTIC_ZERO_D9_OBSTRUCTIONS",
        "records": records,
        "all_nonincident_columns_support_disjoint": True,
        "degree_ten_launched": False,
    }
    temporary = HERE / "results_independent_integer_replay.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_independent_integer_replay.json")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
