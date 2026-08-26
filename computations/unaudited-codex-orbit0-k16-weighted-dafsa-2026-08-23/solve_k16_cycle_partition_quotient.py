#!/usr/bin/env python3
"""Exact-Q cycle-partition quotient and universal dual for the K16 packet."""

from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from math import gcd, lcm
import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROFILES = HERE / "k16_multiplier_cycle_profiles.tsv"
TARGET = HERE / "k16_target_cycle_partition_vector.tsv"
DUAL = HERE / "k16_cycle_partition_dual.tsv"
RESULT = HERE / "results_k16_cycle_partition_quotient.json"
PRIMES = (32003, 32009)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


@lru_cache(None)
def perfect_matchings(vertices):
    if not vertices:
        return ((),)
    u = vertices[0]
    answer = []
    for i, v in enumerate(vertices[1:], 1):
        rest = vertices[1:i] + vertices[i + 1:]
        for tail in perfect_matchings(rest):
            answer.append(((u, v),) + tail)
    return tuple(answer)


PM8 = perfect_matchings(tuple(range(8)))


def profile_vector(paths, closed):
    answer = Counter()
    for matching in PM8:
        parent = list(range(4))

        def root(x):
            while parent[x] != x:
                x = parent[x]
            return x

        for a, b in matching:
            left, right = root(a // 2), root(b // 2)
            if left != right:
                parent[right] = left
        groups = {}
        for i in range(4):
            groups.setdefault(root(i), []).append(i)
        completed = tuple(sum(paths[i] + 1 for i in group)
                          for group in groups.values())
        answer[tuple(sorted(closed + completed))] += 1
    require(sum(answer.values()) == 105, (paths, closed))
    return answer


@lru_cache(None)
def cycle_partitions(total, minimum=2):
    if total == 0:
        return ((),)
    return tuple((part,) + tail
                 for part in range(minimum, total + 1)
                 for tail in cycle_partitions(total - part, part))


def abstract_profiles():
    answer = []
    for a in range(1, 21):
        for b in range(a, 21):
            for c in range(b, 21):
                for d in range(c, 21):
                    used = a + b + c + d
                    if used > 20:
                        break
                    for closed in cycle_partitions(20 - used):
                        answer.append(((a, b, c, d), closed))
    require(len(answer) == len(set(answer)) == 1162, len(answer))
    return tuple(answer)


def load_realized():
    rows = PROFILES.read_text().splitlines()
    require(rows[0] == "path_edge_lengths\tclosed_cycle_lengths\tcolumn_H_orbits",
            "profile header changed")
    answer = []
    total = 0
    for row in rows[1:]:
        paths, cycles, count = row.split("\t")
        record = (tuple(map(int, paths.split(","))),
                  tuple(map(int, cycles.split(","))) if cycles else ())
        answer.append(record)
        total += int(count)
    require(len(answer) == len(set(answer)) == 811 and total == 98_609_090,
            (len(answer), total))
    return tuple(answer)


def load_target():
    rows = TARGET.read_text().splitlines()
    require(rows[0] == "cycle_partition\tnumerator\tdenominator",
            "target header changed")
    answer = {}
    for row in rows[1:]:
        partition, numerator, denominator = row.split("\t")
        answer[tuple(map(int, partition.split(",")))] = Fraction(
            int(numerator), int(denominator))
    require(len(answer) == 118 and all(value.denominator == 1
                                       for value in answer.values()),
            "target orbit-mass vector changed")
    return answer


def modular_basis(columns, prime):
    basis = {}
    chosen = []
    for index, column in enumerate(columns):
        value = [entry % prime for entry in column]
        while True:
            pivot = next((i for i, entry in enumerate(value) if entry), None)
            if pivot is None:
                break
            if pivot not in basis:
                scale = pow(value[pivot], prime - 2, prime)
                value = [entry * scale % prime for entry in value]
                basis[pivot] = value
                chosen.append(index)
                break
            scale = value[pivot]
            row = basis[pivot]
            value = [(left - scale * right) % prime
                     for left, right in zip(value, row, strict=True)]
    return chosen


def exact_rref(rows):
    rows = [[Fraction(value) for value in row] for row in rows]
    rank = 0
    pivots = []
    width = len(rows[0])
    for column in range(width):
        pivot = next((i for i in range(rank, len(rows))
                      if rows[i][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = rows[rank][column]
        rows[rank] = [value / scale for value in rows[rank]]
        for i in range(len(rows)):
            if i == rank or not rows[i][column]:
                continue
            scale = rows[i][column]
            rows[i] = [left - scale * right
                       for left, right in zip(rows[i], rows[rank], strict=True)]
        pivots.append(column)
        rank += 1
        if rank == len(rows):
            break
    require(rank == len(rows), (rank, len(rows)))
    return rows, pivots


def primitive_integer(values):
    denominator = 1
    for value in values:
        denominator = lcm(denominator, value.denominator)
    integers = [value.numerator * (denominator // value.denominator)
                for value in values]
    divisor = 0
    for value in integers:
        divisor = gcd(divisor, abs(value))
    require(divisor, "zero dual")
    integers = [value // divisor for value in integers]
    first = next(value for value in integers if value)
    if first < 0:
        integers = [-value for value in integers]
    return integers


def original_structured_aT_vector():
    """Cycle vector of `a * H0 * H1 * H2` without expanding 105^3 rows."""
    base = ((0, 1), (2, 3), (4, 5), (6, 7))
    one_colour = Counter()
    for matching in PM8:
        parent = list(range(8))
        edges = [0] * 8

        def root(x):
            while parent[x] != x:
                x = parent[x]
            return x

        for u, v in base + matching:
            left, right = root(u), root(v)
            if left == right:
                edges[left] += 1
            else:
                parent[right] = left
                edges[left] += edges[right] + 1
        partition = tuple(sorted(edges[i] for i in range(8)
                                 if root(i) == i))
        require(sum(partition) == 8, partition)
        one_colour[partition] += 1
    require(sum(one_colour.values()) == 105, one_colour)
    answer = Counter({(): 1})
    for _ in range(3):
        answer = Counter({partition:
                          sum(left_count * right_count
                              for left, left_count in answer.items()
                              for right, right_count in one_colour.items()
                              if tuple(sorted(left + right)) == partition)
                          for partition in {
                              tuple(sorted(left + right))
                              for left in answer for right in one_colour
                          }})
    require(sum(answer.values()) == 105 ** 3
            and all(sum(partition) == 24 for partition in answer),
            "structured a*T convolution changed")
    return answer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutate", action="store_true")
    args = parser.parse_args()
    realized = load_realized()
    abstract = abstract_profiles()
    require(set(realized) < set(abstract)
            and len(set(abstract) - set(realized)) == 351,
            "realized/abstract coverage guard changed")
    target = load_target()
    realized_vectors = [profile_vector(*profile) for profile in realized]
    abstract_vectors = [profile_vector(*profile) for profile in abstract]
    partitions = sorted(set(target).union(
        *(set(vector) for vector in abstract_vectors)))
    require(len(partitions) == 320, len(partitions))
    dense_realized = [[vector.get(partition, 0) for partition in partitions]
                      for vector in realized_vectors]
    dense_abstract = [[vector.get(partition, 0) for partition in partitions]
                      for vector in abstract_vectors]
    target_dense = [target.get(partition, 0) for partition in partitions]

    ranks = {}
    chosen = None
    for prime in PRIMES:
        real_basis = modular_basis(dense_realized, prime)
        abstract_basis = modular_basis(dense_abstract, prime)
        augmented_basis = modular_basis(
            dense_abstract + [[int(value) % prime for value in target_dense]], prime)
        ranks[str(prime)] = {
            "realized_profiles": len(real_basis),
            "all_abstract_profiles": len(abstract_basis),
            "with_target": len(augmented_basis),
        }
        require((len(real_basis), len(abstract_basis), len(augmented_basis))
                == (252, 271, 272), ranks[str(prime)])
        if chosen is None:
            chosen = abstract_basis
        else:
            require(chosen == abstract_basis,
                    "modular basis indices diverged")

    rref, pivots = exact_rref([dense_abstract[index] for index in chosen])
    free = [i for i in range(len(partitions)) if i not in set(pivots)]
    candidates = []
    for coordinate in free:
        dual = [Fraction(0) for _ in partitions]
        dual[coordinate] = 1
        for row, pivot in zip(rref, pivots, strict=True):
            dual[pivot] = -row[coordinate]
        pairing = sum(value * coefficient
                      for value, coefficient in zip(target_dense, dual, strict=True))
        if pairing:
            integers = primitive_integer(dual)
            integer_pairing = sum(int(value) * coefficient
                                  for value, coefficient in zip(target_dense, integers,
                                                                strict=True))
            candidates.append((sum(value != 0 for value in integers),
                               max(map(abs, integers)), abs(integer_pairing),
                               integers, integer_pairing))
    require(candidates, "every exact null vector killed the target")
    _, _, _, dual, target_pairing = min(candidates, key=lambda row: row[:3])
    if args.mutate:
        dual[0] += 1

    def pairing(vector):
        return sum(dual[i] * vector.get(partition, 0)
                   for i, partition in enumerate(partitions))

    abstract_pairings = [pairing(vector) for vector in abstract_vectors]
    require(set(abstract_pairings) == {0},
            "hostile dual mutation/full abstract-profile replay fired")
    require(pairing(Counter(target)) == target_pairing != 0,
            "target pairing changed")
    original_aT = original_structured_aT_vector()
    original_aT_pairing = pairing(original_aT)
    require(original_aT_pairing == 0,
            "conservation guard: original structured a*T acquired charge")
    dual_support = sum(value != 0 for value in dual)
    print("DUAL_CANDIDATE", dual_support, max(map(abs, dual)), target_pairing)
    require(dual_support > 0, "dual support vanished")

    DUAL.write_text("cycle_partition\tinteger_coefficient\n" + "".join(
        f"{','.join(map(str, partition))}\t{coefficient}\n"
        for partition, coefficient in zip(partitions, dual, strict=True)
        if coefficient))
    result = {
        "schema": "orbit0-k16-cycle-partition-quotient-v1",
        "status": "EXACT_Q_SEPARATOR",
        "realized_multiplier_profiles": len(realized),
        "missing_abstract_profiles": len(set(abstract) - set(realized)),
        "all_abstract_four_path_cycle_profiles": len(abstract),
        "cycle_partition_coordinates": len(partitions),
        "modular_rank_replays": ranks,
        "exact_dual_support": sum(value != 0 for value in dual),
        "exact_dual_max_abs_coefficient": max(map(abs, dual)),
        "exact_target_pairing": target_pairing,
        "all_abstract_profile_pairings_zero": len(abstract_pairings),
        "realized_column_H_orbits_covered": 98_609_090,
        "target_orbit_mass_support": len(target),
        "original_structured_aT_cycle_support": len(original_aT),
        "original_structured_aT_terms": sum(original_aT.values()),
        "original_structured_aT_pairing": original_aT_pairing,
        "conservation_scope_guard": (
            "the separator detects the frozen K16 residual polynomial but "
            "annihilates original a*T; omitted K17--K24 tails must carry the "
            "opposite charge in the prior filtered congruence"
        ),
        "literal_source_scope": (
            "every balanced degree-24 mixed source column has four positive "
            "path lengths plus closed cycles totaling 20, hence belongs to the "
            "1162-profile abstract superset annihilated by the dual"
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode()).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("PASS", result["logical_sha256"], "dual_support",
          result["exact_dual_support"], "target_pairing", target_pairing)


if __name__ == "__main__":
    main()
