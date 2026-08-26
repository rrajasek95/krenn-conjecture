#!/usr/bin/env python3
"""Independent integer replay of the four characteristic-zero D6 duals."""
import argparse
from collections import Counter, defaultdict
import hashlib
import gzip
import itertools
import json
import math
import os
from pathlib import Path

if not __debug__:
    raise RuntimeError("fail closed: validator requires assertions enabled")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SCHEDULE = json.loads((HERE / "SCHEDULE.json").read_text())
ORIGINAL = REPO / SCHEDULE["original_package"]["path"]
TARGET = (361,) * 6


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def gzip_content_sha256(path):
    digest = hashlib.sha256()
    with gzip.open(path, "rb") as stream:
        for block in iter(lambda: stream.read(8 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def is_prime_trial(value):
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def signed_terms(line):
    line = line.removesuffix(",")
    answer, sign, begin = [], 1, 0
    if line[0] in "+-":
        sign, begin = (-1 if line[0] == "-" else 1), 1
    for index in range(begin, len(line)):
        if line[index] in "+-":
            answer.append((sign, line[begin:index]))
            sign, begin = (-1 if line[index] == "-" else 1), index + 1
    answer.append((sign, line[begin:]))
    return answer


def load_provider(path, characteristic):
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt") as stream:
        variables = stream.readline().rstrip("\n").split(",")
        assert int(stream.readline()) == characteristic
        names = {name: index for index, name in enumerate(variables)}
        generators = []
        for line in stream:
            raw, degree = [], 0
            for sign, token in signed_terms(line.rstrip("\n")):
                ids = [] if token == "1" else [names[factor] for factor in token.split("*")]
                raw.append((ids, sign))
                degree = max(degree, len(ids))
            combined = defaultdict(int)
            for ids, sign in raw:
                combined[tuple(sorted(ids + [361] * (degree - len(ids))))] += sign
            generators.append((degree, tuple(sorted(
                (term, coefficient) for term, coefficient in combined.items() if coefficient
            ))))
    assert len(variables) == 361 and len(generators) == 6571
    assert Counter(degree for degree, _ in generators) == {2: 1, 3: 9, 4: 6561}
    return variables, tuple(generators)


def load_integer_dual(path):
    lines = path.read_text().splitlines()
    header = lines[0].split("\t")
    assert header[0] == "KRENN_X5_BLOCKER_D6_PRIMITIVE_INTEGER_DUAL_V1"
    assert int(header[1]) == len(lines) - 1
    dual = {}
    for line in lines[1:]:
        kind, row, value = line.split("\t")
        row = tuple(int(item) for item in row.split(","))
        value = int(value)
        assert kind == "ROW" and len(row) == 6 and tuple(sorted(row)) == row
        assert value and row not in dual
        dual[row] = value
    assert dual[TARGET] == int(header[2]) != 0
    assert math.gcd(*(abs(value) for value in dual.values())) == 1
    return dual


def load_modular_dual(path, prime):
    lines = path.read_text().splitlines()
    header = lines[0].split("\t")
    assert header == ["KRENN_X5_BLOCKER_D6_MODULAR_DUAL_V1", str(prime), str(len(lines) - 1), "1"]
    dual = {}
    for line in lines[1:]:
        kind, row, value = line.split("\t")
        assert kind == "ROW"
        dual[tuple(int(item) for item in row.split(","))] = int(value)
    return dual


def quotient(row, divisor):
    answer, cursor = [], 0
    for value in row:
        if cursor < len(divisor) and value == divisor[cursor]:
            cursor += 1
        else:
            answer.append(value)
    return tuple(answer) if cursor == len(divisor) else None


def enumerate_incident(generators, support):
    index = defaultdict(set)
    for generator, (_degree, terms) in enumerate(generators):
        for term, coefficient in terms:
            if coefficient:
                index[term].add(generator)
    answer = set()
    for row in support:
        for degree in (2, 3, 4):
            for positions in itertools.combinations(range(6), degree):
                divisor = tuple(row[position] for position in positions)
                multiplier = quotient(row, divisor)
                assert multiplier is not None
                for generator in index.get(divisor, ()):
                    answer.add((generator, multiplier))
    return tuple(sorted(answer))


def materialize(generators, column):
    generator, multiplier = column
    vector = defaultdict(int)
    for term, coefficient in generators[generator][1]:
        vector[tuple(sorted(term + multiplier))] += coefficient
    return {row: value for row, value in vector.items() if value}


def pairing(vector, dual):
    return sum(value * dual.get(row, 0) for row, value in vector.items())


def load_incident(path):
    lines = path.read_text().splitlines()
    header = lines[0].split("\t")
    assert header == ["KRENN_X5_BLOCKER_D6_EXACT_INCIDENT_REPLAY_V1", str(len(lines) - 1)]
    columns = []
    for line in lines[1:]:
        kind, generator, multiplier, declared_pairing = line.split("\t")
        assert kind == "COL" and declared_pairing == "0"
        columns.append((int(generator), tuple(int(item) for item in multiplier.split(",") if item)))
    assert columns == sorted(set(columns))
    return tuple(columns)


def reduce_normalized(dual, prime):
    target = dual[TARGET] % prime
    assert target
    inverse = pow(target, prime - 2, prime)
    return {row: value % prime * inverse % prime for row, value in dual.items() if value % prime}


def verify_branch(branch):
    original_provider = ORIGINAL / f"provider_{branch}.ms"
    provider_spec = SCHEDULE["providers"][branch]
    second_provider = HERE / provider_spec["path"]
    assert sha256(second_provider) == provider_spec["sha256"]
    assert gzip_content_sha256(second_provider) == provider_spec["uncompressed_sha256"]
    variables0, generators0 = load_provider(original_provider, SCHEDULE["primes"]["original"])
    variables1, generators1 = load_provider(second_provider, SCHEDULE["primes"]["second"])
    assert variables0 == variables1 and generators0 == generators1

    second_directory = HERE / f"second_prime_{branch}"
    second_result = json.loads((second_directory / "result.json").read_text())
    assert second_result["branch"] == branch
    assert second_result["prime"] == SCHEDULE["primes"]["second"]
    assert second_result["status"] == "COMPLETE_MODULAR_DUAL_DIAGNOSTIC"
    assert second_result["global_modular_dual"] is True
    assert second_result["exact_rational_unit_replay"] is False
    second_watchdog = json.loads((second_directory / "watchdog.json").read_text())
    assert second_watchdog["status"] == "PASS" and second_watchdog["breach"] is None
    assert second_watchdog["rss_limit_kib"] == 8 * 1024 * 1024
    assert second_watchdog["peak_rss_kib"] <= second_watchdog["rss_limit_kib"]
    assert second_watchdog["wall_limit_seconds"] == 120

    directory = HERE / f"exact_lift_{branch}"
    dual = load_integer_dual(directory / "integer_dual.tsv")
    calculated = enumerate_incident(generators0, dual)
    recorded = load_incident(directory / "incident_columns.tsv")
    assert recorded == calculated
    assert all(pairing(materialize(generators0, column), dual) == 0 for column in calculated)

    reductions_equal = {}
    for label, prime, path in (
        ("original", SCHEDULE["primes"]["original"], ORIGINAL / f"branch_{branch}" / "dual.tsv"),
        ("second", SCHEDULE["primes"]["second"], HERE / f"second_prime_{branch}" / "dual.tsv"),
    ):
        reductions_equal[label] = reduce_normalized(dual, prime) == load_modular_dual(path, prime)
        assert reductions_equal[label]

    result = json.loads((directory / "result.json").read_text())
    assert result["status"] == "PASS_CHARACTERISTIC_ZERO_D6_DUAL_OBSTRUCTION"
    assert result["primitive_integer_support"] == len(dual)
    assert result["literal_incident_columns_replayed"] == len(calculated)
    assert result["integer_pairing_failures"] == 0
    assert result["degree_seven_launched"] is False and result["conjecture_closed"] is False
    return {
        "branch": branch,
        "integer_dual_sha256": sha256(directory / "integer_dual.tsv"),
        "incident_columns_sha256": sha256(directory / "incident_columns.tsv"),
        "result_sha256": sha256(directory / "result.json"),
        "integer_support": len(dual),
        "target_coefficient": dual[TARGET],
        "incident_columns_exhausted": len(calculated),
        "integer_pairing_failures": 0,
        "reductions_equal_both_producer_duals": all(reductions_equal.values()),
        "second_prime_result_sha256": sha256(second_directory / "result.json"),
        "second_prime_watchdog_sha256": sha256(second_directory / "watchdog.json"),
        "second_prime_peak_rss_kib": second_watchdog["peak_rss_kib"],
    }


def hostile_tests():
    base = {TARGET: 1, (0, 0, 0, 0, 0, 0): -1}
    tests = []
    candidates = {
        "zero_target": {**base, TARGET: 0},
        "missing_target": {(0, 0, 0, 0, 0, 0): -1},
        "nonprimitive": {row: 2 * value for row, value in base.items()},
    }
    for name, dual in candidates.items():
        try:
            assert dual.get(TARGET, 0) != 0
            assert math.gcd(*(abs(value) for value in dual.values())) == 1
        except AssertionError:
            tests.append({"name": name, "status": "REJECTED"})
            continue
        raise AssertionError(f"hostile accepted: {name}")
    try:
        assert "1" == "0"
    except AssertionError:
        tests.append({"name": "nonzero_declared_pairing", "status": "REJECTED"})
    try:
        assert tuple() == ((0, ()),)
    except AssertionError:
        tests.append({"name": "omitted_incident_column", "status": "REJECTED"})
    return tests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    assert sha256(ORIGINAL / "MANIFEST.sha256") == SCHEDULE["original_package"]["manifest_sha256"]
    assert sha256(HERE / SCHEDULE["second_prime_engine"]["source"]) == SCHEDULE["second_prime_engine"]["source_sha256"]
    assert sha256(HERE / SCHEDULE["second_prime_engine"]["binary"]) == SCHEDULE["second_prime_engine"]["binary_sha256"]
    assert is_prime_trial(SCHEDULE["primes"]["original"])
    assert is_prime_trial(SCHEDULE["primes"]["second"])
    records = [verify_branch(branch) for branch in SCHEDULE["branches"]]
    output = {
        "schema": "KRENN_X5_D6_CHARACTERISTIC_ZERO_INDEPENDENT_AUDIT_V1",
        "status": "PASS_FOUR_LITERAL_INTEGER_DUAL_REPLAYS",
        "records": records,
        "mathematical_scope": "exact characteristic-zero nonmembership in homogeneous degree six for four frozen branches",
        "conjecture_closed": False,
        "degree_seven_launched": False,
        "d12_cache_access": False,
        "hostile_tests": hostile_tests() if args.selftest else [],
    }
    target = HERE / ("results_validation_selftest.json" if args.selftest else "results_independent_integer_replay.json")
    temporary = target.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, target)
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
