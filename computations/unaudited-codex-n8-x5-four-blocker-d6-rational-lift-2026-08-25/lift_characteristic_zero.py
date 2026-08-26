#!/usr/bin/env python3
"""Exact characteristic-zero lift and literal replay of the two-prime D6 duals."""
from collections import Counter, defaultdict
from fractions import Fraction
import gzip
import hashlib
import itertools
import json
import math
import os
from pathlib import Path

if not __debug__:
    raise RuntimeError("fail closed: exact lift requires Python assertions enabled")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SCHEDULE = json.loads((HERE / "SCHEDULE.json").read_text())
ORIGINAL = REPO / SCHEDULE["original_package"]["path"]
T_ID = 361
TARGET = (T_ID,) * 6


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


def atomic_json(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


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
    answer = []
    sign = 1
    begin = 0
    if line[0] in "+-":
        sign = -1 if line[0] == "-" else 1
        begin = 1
    for index in range(begin, len(line)):
        if line[index] in "+-":
            answer.append((sign, line[begin:index]))
            sign = -1 if line[index] == "-" else 1
            begin = index + 1
    answer.append((sign, line[begin:]))
    return answer


def load_provider(path, expected_characteristic):
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt") as stream:
        variables = stream.readline().rstrip("\n").split(",")
        characteristic = int(stream.readline())
        names = {name: index for index, name in enumerate(variables)}
        generators = []
        for line in stream:
            raw = []
            maximum = 0
            for sign, token in signed_terms(line.rstrip("\n")):
                ids = [] if token == "1" else [names[factor] for factor in token.split("*")]
                maximum = max(maximum, len(ids))
                raw.append((ids, sign))
            combined = defaultdict(int)
            for ids, sign in raw:
                key = tuple(sorted(ids + [T_ID] * (maximum - len(ids))))
                combined[key] += sign
            generators.append((
                maximum,
                tuple(sorted((key, value) for key, value in combined.items() if value)),
            ))
    assert len(variables) == 361 and characteristic == expected_characteristic
    assert len(generators) == 6571
    assert Counter(degree for degree, _terms in generators) == {2: 1, 3: 9, 4: 6561}
    return variables, tuple(generators)


def load_dual(path, prime):
    lines = path.read_text().splitlines()
    header = lines[0].split("\t")
    assert header == ["KRENN_X5_BLOCKER_D6_MODULAR_DUAL_V1", str(prime), str(len(lines) - 1), "1"]
    dual = {}
    for line in lines[1:]:
        kind, row, value = line.split("\t")
        row = tuple(int(item) for item in row.split(","))
        assert kind == "ROW" and len(row) == 6 and row == tuple(sorted(row))
        assert row not in dual
        dual[row] = int(value)
    assert dual[TARGET] == 1
    return dual


def multiset_quotient(row, divisor):
    quotient = []
    cursor = 0
    for value in row:
        if cursor < len(divisor) and value == divisor[cursor]:
            cursor += 1
        else:
            quotient.append(value)
    return tuple(quotient) if cursor == len(divisor) else None


def incident_columns(generators, support):
    term_to_generators = defaultdict(set)
    for generator, (_degree, terms) in enumerate(generators):
        for term, coefficient in terms:
            if coefficient:
                term_to_generators[term].add(generator)
    columns = set()
    for row in support:
        for degree in (2, 3, 4):
            divisors = {
                tuple(row[index] for index in positions)
                for positions in itertools.combinations(range(6), degree)
            }
            for divisor in divisors:
                multiplier = multiset_quotient(row, divisor)
                assert multiplier is not None
                for generator in term_to_generators.get(divisor, ()):
                    assert generators[generator][0] == degree
                    columns.add((generator, multiplier))
    return tuple(sorted(columns))


def materialize(generators, column):
    generator, multiplier = column
    values = defaultdict(int)
    for term, coefficient in generators[generator][1]:
        values[tuple(sorted(term + multiplier))] += coefficient
    return {row: value for row, value in values.items() if value}


def solve_rational(rows, columns, generators):
    """RREF the exact dual equations, fixing the target coordinate to one."""
    index = {row: position for position, row in enumerate(rows)}
    matrix = []
    target_equation = [Fraction(0) for _ in range(len(rows) + 1)]
    target_equation[index[TARGET]] = Fraction(1)
    target_equation[-1] = Fraction(1)
    matrix.append(target_equation)
    for column in columns:
        vector = materialize(generators, column)
        equation = [Fraction(vector.get(row, 0)) for row in rows] + [Fraction(0)]
        if any(equation[:-1]):
            matrix.append(equation)

    pivot_columns = []
    pivot_row = 0
    for column in range(len(rows)):
        found = next((row for row in range(pivot_row, len(matrix)) if matrix[row][column]), None)
        if found is None:
            continue
        matrix[pivot_row], matrix[found] = matrix[found], matrix[pivot_row]
        pivot = matrix[pivot_row][column]
        matrix[pivot_row] = [value / pivot for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [left - factor * right
                           for left, right in zip(matrix[row], matrix[pivot_row])]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    for equation in matrix:
        assert any(equation[:-1]) or not equation[-1], "exact dual system is inconsistent"
    solution = [Fraction(0) for _ in rows]
    for row, column in enumerate(pivot_columns):
        solution[column] = matrix[row][-1]
    assert solution[index[TARGET]] == 1
    for equation in matrix:
        assert sum(left * right for left, right in zip(equation[:-1], solution)) == equation[-1]
    return solution, len(pivot_columns), len(matrix)


def primitive_integer(solution):
    denominator = 1
    for value in solution:
        denominator = math.lcm(denominator, value.denominator)
    weights = [value.numerator * (denominator // value.denominator) for value in solution]
    divisor = 0
    for value in weights:
        divisor = math.gcd(divisor, abs(value))
    assert divisor > 0
    weights = [value // divisor for value in weights]
    if weights[-1] < 0:
        weights = [-value for value in weights]
    return weights


def pairing(vector, dual):
    return sum(value * dual.get(row, 0) for row, value in vector.items())


def normalized_reduction(integer_dual, prime):
    target = integer_dual[TARGET] % prime
    assert target
    inverse = pow(target, prime - 2, prime)
    return {row: (value % prime) * inverse % prime
            for row, value in integer_dual.items() if value % prime}


def write_integer_dual(path, dual):
    lines = [
        f"KRENN_X5_BLOCKER_D6_PRIMITIVE_INTEGER_DUAL_V1\t{len(dual)}\t{dual[TARGET]}"
    ]
    lines.extend(f"ROW\t{','.join(map(str, row))}\t{value}" for row, value in sorted(dual.items()))
    path.write_text("\n".join(lines) + "\n")


def write_incident(path, columns):
    lines = [f"KRENN_X5_BLOCKER_D6_EXACT_INCIDENT_REPLAY_V1\t{len(columns)}"]
    lines.extend(
        f"COL\t{generator}\t{','.join(map(str, multiplier))}\t0"
        for generator, multiplier in columns
    )
    path.write_text("\n".join(lines) + "\n")


def lift_branch(branch):
    original_provider = ORIGINAL / f"provider_{branch}.ms"
    provider_spec = SCHEDULE["providers"][branch]
    second_provider = HERE / provider_spec["path"]
    assert sha256(second_provider) == provider_spec["sha256"]
    assert gzip_content_sha256(second_provider) == provider_spec["uncompressed_sha256"]
    variables0, generators0 = load_provider(original_provider, SCHEDULE["primes"]["original"])
    variables1, generators1 = load_provider(second_provider, SCHEDULE["primes"]["second"])
    assert variables0 == variables1 and generators0 == generators1

    dual0 = load_dual(ORIGINAL / f"branch_{branch}" / "dual.tsv", SCHEDULE["primes"]["original"])
    dual1 = load_dual(HERE / f"second_prime_{branch}" / "dual.tsv", SCHEDULE["primes"]["second"])
    rows = tuple(sorted(set(dual0) | set(dual1)))
    columns = incident_columns(generators0, rows)
    solution, rank, equations = solve_rational(rows, columns, generators0)
    integer_weights = primitive_integer(solution)
    integer_dual = {row: value for row, value in zip(rows, integer_weights) if value}
    assert integer_dual[TARGET] != 0

    # Recompute incidence after zero coordinates disappear, then replay every
    # possibly nonzero literal pairing over Z.
    exact_columns = incident_columns(generators0, integer_dual)
    for column in exact_columns:
        assert pairing(materialize(generators0, column), integer_dual) == 0
    reductions = {}
    for label, prime, producer in (
        ("original", SCHEDULE["primes"]["original"], dual0),
        ("second", SCHEDULE["primes"]["second"], dual1),
    ):
        reduced = normalized_reduction(integer_dual, prime)
        for column in exact_columns:
            assert pairing(materialize(generators0, column), reduced) % prime == 0
        reductions[label] = {
            "prime": prime,
            "normalized_integer_reduction_equals_producer_dual": reduced == producer,
            "normalized_support": len(reduced),
        }

    directory = HERE / f"exact_lift_{branch}"
    assert not directory.exists()
    directory.mkdir()
    write_integer_dual(directory / "integer_dual.tsv", integer_dual)
    write_incident(directory / "incident_columns.tsv", exact_columns)
    result = {
        "schema": "KRENN_X5_BLOCKER_D6_CHARACTERISTIC_ZERO_LIFT_RESULT_V1",
        "status": "PASS_CHARACTERISTIC_ZERO_D6_DUAL_OBSTRUCTION",
        "branch": branch,
        "degree": 6,
        "target": "t^6",
        "union_modular_support": len(rows),
        "exact_rational_rank": rank,
        "exact_rational_equations": equations,
        "primitive_integer_support": len(integer_dual),
        "primitive_integer_target_coefficient": integer_dual[TARGET],
        "literal_incident_columns_replayed": len(exact_columns),
        "all_other_columns_support_disjoint": True,
        "integer_pairing_failures": 0,
        "reductions": reductions,
        "degree_six_rational_membership_excluded": True,
        "conjecture_closed": False,
        "degree_seven_launched": False,
    }
    atomic_json(directory / "result.json", result)
    return result


def main():
    assert sha256(ORIGINAL / "MANIFEST.sha256") == SCHEDULE["original_package"]["manifest_sha256"]
    assert is_prime_trial(SCHEDULE["primes"]["original"])
    assert is_prime_trial(SCHEDULE["primes"]["second"])
    records = [lift_branch(branch) for branch in SCHEDULE["branches"]]
    result = {
        "schema": "KRENN_X5_D6_FOUR_BRANCH_CHARACTERISTIC_ZERO_LIFT_AUDIT_V1",
        "status": "PASS_FOUR_CHARACTERISTIC_ZERO_D6_DUAL_OBSTRUCTIONS",
        "records": records,
        "all_four_exact_integer_replays": True,
        "degree_seven_recommendation": (
            "Degree six is now exactly excluded in all four branches.  A bounded degree-seven membership gate "
            "is the next algebraic experiment, but was not launched."
        ),
        "conjecture_closed": False,
        "degree_seven_launched": False,
        "d12_cache_access": False,
    }
    atomic_json(HERE / "results_characteristic_zero_lift.json", result)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
