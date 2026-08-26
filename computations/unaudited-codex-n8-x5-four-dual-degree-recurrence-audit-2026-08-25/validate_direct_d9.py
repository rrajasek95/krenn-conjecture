#!/usr/bin/env python3
"""Independent literal replay of the transported 38-row direct D9 dual."""
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
PROVIDER = REPO / "computations/unaudited-codex-n8-x5-four-blocker-d6-cegar-gate-2026-08-25/provider_direct.ms"
D8_DUAL = REPO / "computations/unaudited-codex-n8-x5-four-blocker-d8-two-prime-lift-2026-08-25/exact_lift_direct/integer_dual.tsv"
D9_DUAL = HERE / "d9_span_dual_direct.tsv"


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


def provider():
    assert sha(PROVIDER) == "53850c4224fcc901bb5bd0d4c5be58d92ae4f4fb04bfdc887bc4492f4dd41d6c"
    with PROVIDER.open() as stream:
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
    assert int(header[1]) == len(lines) - 1 and int(header[2]) == 1
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
    generators = provider()
    d8, d9 = dual(D8_DUAL, 8), dual(D9_DUAL, 9)
    expected = {tuple(sorted(row + (T,))): value for row, value in d8.items()}
    assert d9 == expected and len(d9) == 38 and set(d9.values()) == {-1, 1}
    term_index = defaultdict(set)
    for g, (_degree, terms) in enumerate(generators):
        for term, coefficient in terms:
            if coefficient:
                term_index[term].add(g)
    columns = set()
    for row in d9:
        for degree in (2, 3, 4):
            for positions in itertools.combinations(range(9), degree):
                divisor = tuple(row[i] for i in positions)
                multiplier = quotient(row, divisor)
                for g in term_index.get(divisor, ()):
                    columns.add((g, multiplier))
    for g, multiplier in columns:
        value = sum(c * d9.get(tuple(sorted(term + multiplier)), 0) for term, c in generators[g][1])
        assert value == 0
    result = {
        "schema": "KRENN_X5_DIRECT_D9_TRANSPORTED_DUAL_INDEPENDENT_REPLAY_V1",
        "status": "PASS_EXACT_CHARACTERISTIC_ZERO_DIRECT_D9_OBSTRUCTION",
        "provider_sha256": sha(PROVIDER),
        "d8_dual_sha256": sha(D8_DUAL),
        "d9_dual_sha256": sha(D9_DUAL),
        "d9_equals_d8_append_t": True,
        "support": len(d9),
        "weight_set": sorted(set(d9.values())),
        "target": "t^9",
        "target_coefficient": d9[(T,) * 9],
        "literal_incident_columns_replayed": len(columns),
        "pairing_failures": 0,
        "all_nonincident_columns_support_disjoint": True,
        "degree_nine_full_closure_or_solve": False,
    }
    temporary = HERE / "results_direct_d9_independent_replay.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_direct_d9_independent_replay.json")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
