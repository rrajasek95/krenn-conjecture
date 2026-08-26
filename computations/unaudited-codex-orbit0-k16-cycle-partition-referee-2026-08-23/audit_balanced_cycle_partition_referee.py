#!/usr/bin/env python3
"""Independent exact referee of the balanced-port cycle quotient.

No source-column language is traversed.  We enumerate the universal abstract
four-path profiles, compute their exact Q rank, stream the frozen 1.848m-row
target once, and replay the independently supplied integer separator.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations_with_replacement
import importlib.util
import json
import mmap
from math import gcd
from pathlib import Path
import re


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
K14_PATH = (ROOT / "computations/unaudited-codex-orbit0-k14-interface-audit-2026-08-21"
            / "audit_orbit0_k14_interface.py")
LITERAL = (ROOT / "computations/unaudited-codex-orbit0-k16-literal-collection-2026-08-22"
           / "results_orbit0_k16_literal_residual.json")
TAIL_DIR = ROOT / "computations/unaudited-codex-orbit0-k16-weighted-dafsa-2026-08-23"
TAIL_DUAL = TAIL_DIR / "k16_cycle_partition_dual.tsv"
TAIL_TARGET = TAIL_DIR / "k16_target_cycle_partition_vector.tsv"
TAIL_RESULT = TAIL_DIR / "results_k16_cycle_partition_quotient.json"
OUT = HERE / "results_balanced_cycle_partition_referee.json"
DUAL_OUT = HERE / "replayed_cycle_partition_dual.tsv"
TARGET_OUT = HERE / "replayed_target_cycle_vector.tsv"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def file_sha256(path):
    digest = sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


SPEC = importlib.util.spec_from_file_location("cycle_referee_k14", K14_PATH)
K14 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(K14)
BASE = K14.FROZEN.BASE


@lru_cache(None)
def integer_partitions(total, minimum=2):
    if total == 0:
        return ((),)
    return tuple((part,) + tail
                 for part in range(minimum, total + 1)
                 for tail in integer_partitions(total - part, part))


@lru_cache(None)
def perfect_matchings(vertices):
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index, second in enumerate(vertices[1:], 1):
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


PM8 = perfect_matchings(tuple(range(8)))
require(len(PM8) == 105, len(PM8))


def path_set_partition(matching):
    parent = list(range(4))

    def root(index):
        while parent[index] != index:
            index = parent[index]
        return index

    for left, right in matching:
        a, b = root(left // 2), root(right // 2)
        if a != b:
            parent[b] = a
    blocks = Counter()
    for index in range(4):
        blocks[root(index)] += 1
    return tuple(sorted(blocks.values()))


SET_PARTITION_TYPE_MASS = Counter(path_set_partition(matching) for matching in PM8)
require(SET_PARTITION_TYPE_MASS == {
    (1, 1, 1, 1): 1,
    (1, 1, 2): 12,
    (1, 3): 32,
    (2, 2): 12,
    (4,): 48,
}, SET_PARTITION_TYPE_MASS)


def block_partition(matching):
    parent = list(range(4))

    def root(index):
        while parent[index] != index:
            index = parent[index]
        return index

    for left, right in matching:
        a, b = root(left // 2), root(right // 2)
        if a != b:
            parent[b] = a
    groups = {}
    for index in range(4):
        groups.setdefault(root(index), []).append(index)
    return tuple(sorted(tuple(group) for group in groups.values()))


BLOCK_MASS = Counter(block_partition(matching) for matching in PM8)
CONNECTED_WEIGHTS = {1: 1, 2: 2, 3: 8, 4: 48}
for blocks, mass in BLOCK_MASS.items():
    expected = 1
    for block in blocks:
        expected *= CONNECTED_WEIGHTS[len(block)]
    require(mass == expected, (blocks, mass, expected))
require(sum(BLOCK_MASS.values()) == 105, sum(BLOCK_MASS.values()))


def abstract_profiles():
    """Four positive path edge lengths plus closed cycles, total 20 edges."""
    answer = []
    for paths in combinations_with_replacement(range(1, 21), 4):
        remainder = 20 - sum(paths)
        if remainder < 0:
            continue
        for closed in integer_partitions(remainder):
            answer.append((paths, closed))
    require(len(answer) == len(set(answer)) == 1162, len(answer))
    return tuple(answer)


def completion_vector(profile):
    paths, closed = profile
    answer = Counter()
    for blocks, mass in BLOCK_MASS.items():
        new_cycles = tuple(sum(paths[index] + 1 for index in block)
                           for block in blocks)
        completed = tuple(sorted(closed + new_cycles))
        require(sum(completed) == 24 and min(completed) >= 2,
                (profile, blocks, completed))
        answer[completed] += mass
    require(sum(answer.values()) == 105, (profile, answer))
    return answer


def sparse_rank(vectors):
    """Exact Q rank by sparse normalized column echelon reduction."""
    basis = {}
    for source in vectors:
        value = {row: Fraction(coefficient)
                 for row, coefficient in source.items() if coefficient}
        while value:
            pivot = min(value)
            if pivot not in basis:
                scale = value[pivot]
                basis[pivot] = {row: coefficient / scale
                                for row, coefficient in value.items()}
                break
            scale = value[pivot]
            old = basis[pivot]
            for row, coefficient in old.items():
                updated = value.get(row, Fraction()) - scale * coefficient
                if updated:
                    value[row] = updated
                else:
                    value.pop(row, None)
    return len(basis)


def cycle_partition(row):
    adjacency = [[] for _ in range(24)]
    degrees = [0] * 24
    for cell in row:
        left_site, right_site, left_colour, right_colour = BASE.CELLS[cell]
        left = 3 * left_site + left_colour
        right = 3 * right_site + right_colour
        adjacency[left].append(right)
        adjacency[right].append(left)
        degrees[left] += 1
        degrees[right] += 1
    require(set(degrees) == {2}, Counter(degrees))
    seen = set()
    cycles = []
    for start in range(24):
        if start in seen:
            continue
        stack = [start]
        seen.add(start)
        size = 0
        while stack:
            vertex = stack.pop()
            size += 1
            for target in adjacency[vertex]:
                if target not in seen:
                    seen.add(target)
                    stack.append(target)
        require(size >= 2, (row.hex(), size))
        cycles.append(size)
    answer = tuple(sorted(cycles))
    require(sum(answer) == 24, answer)
    return answer


LITERAL_RECORD = re.compile(
    rb'\[\s*"([0-9a-f]{48})",\s*(-?[0-9]+),\s*([0-9]+)\s*\]')


def stream_target():
    target = Counter()
    record_count = 0
    denominator_histogram = Counter()
    raw_cycle_histogram = Counter()
    with LITERAL.open("rb") as handle:
        data = mmap.mmap(handle.fileno(), 0, access=mmap.ACCESS_READ)
        for match in LITERAL_RECORD.finditer(data):
            row = bytes.fromhex(match.group(1).decode())
            numerator = int(match.group(2))
            denominator = int(match.group(3))
            partition = cycle_partition(row)
            target[partition] += Fraction(numerator, denominator)
            denominator_histogram[denominator] += 1
            raw_cycle_histogram[partition] += 1
            record_count += 1
        data.close()
    target = Counter({key: value for key, value in target.items() if value})
    require(record_count == 1_848_174, record_count)
    require(len(raw_cycle_histogram) == 120 and len(target) == 118,
            (len(raw_cycle_histogram), len(target)))
    require(denominator_histogram == {1: record_count}, denominator_histogram)
    require(all(value.denominator == 1 for value in target.values()),
            "nonintegral projected target mass")
    return target, record_count, raw_cycle_histogram


def load_dual(path):
    lines = path.read_text().splitlines()
    require(lines[0] == "cycle_partition\tinteger_coefficient", lines[0])
    answer = {}
    for line in lines[1:]:
        partition, coefficient = line.split("\t")
        answer[tuple(map(int, partition.split(",")))] = int(coefficient)
    return answer


def load_target_tsv(path):
    lines = path.read_text().splitlines()
    require(lines[0] == "cycle_partition\tnumerator\tdenominator", lines[0])
    answer = {}
    for line in lines[1:]:
        partition, numerator, denominator = line.split("\t")
        answer[tuple(map(int, partition.split(",")))] = Fraction(
            int(numerator), int(denominator))
    return answer


def original_structured_aT_vector():
    base = ((0, 1), (2, 3), (4, 5), (6, 7))
    one_colour = Counter()
    for matching in PM8:
        adjacency = [[] for _ in range(8)]
        for left, right in base + matching:
            adjacency[left].append(right)
            adjacency[right].append(left)
        require(set(map(len, adjacency)) == {2}, adjacency)
        seen = set()
        cycles = []
        for start in range(8):
            if start in seen:
                continue
            stack = [start]
            seen.add(start)
            size = 0
            while stack:
                vertex = stack.pop()
                size += 1
                for target in adjacency[vertex]:
                    if target not in seen:
                        seen.add(target)
                        stack.append(target)
            cycles.append(size)
        one_colour[tuple(sorted(cycles))] += 1
    require(sum(one_colour.values()) == 105, one_colour)
    answer = Counter({(): 1})
    for _ in range(3):
        updated = Counter()
        for left, left_mass in answer.items():
            for right, right_mass in one_colour.items():
                updated[tuple(sorted(left + right))] += left_mass * right_mass
        answer = updated
    require(len(answer) == 30 and sum(answer.values()) == 105 ** 3,
            (len(answer), sum(answer.values())))
    return answer


def main():
    row_partitions = integer_partitions(24)
    require(len(row_partitions) == 320, len(row_partitions))
    profiles = abstract_profiles()
    vectors = tuple(completion_vector(profile) for profile in profiles)
    require(len(set(tuple(sorted(vector.items())) for vector in vectors)) == 1162,
            "abstract completion vectors collided")
    abstract_rank = sparse_rank(vectors)
    require(abstract_rank == 271, abstract_rank)
    dual_dimension = len(row_partitions) - abstract_rank
    require(dual_dimension == 49, dual_dimension)

    target, records, raw_cycle_histogram = stream_target()
    augmented_rank = sparse_rank(vectors + (target,))
    require(augmented_rank == 272, augmented_rank)
    tail_target = load_target_tsv(TAIL_TARGET)
    require(dict(target) == tail_target, "streamed target differs from Tail TSV")

    dual = load_dual(TAIL_DUAL)
    require(len(dual) == 77 and max(map(abs, dual.values())) == 2_956_800,
            (len(dual), max(map(abs, dual.values()))))
    divisor = 0
    for value in dual.values():
        divisor = gcd(divisor, abs(value))
    require(divisor == 1, divisor)

    def pair(vector):
        return sum(dual.get(partition, 0) * coefficient
                   for partition, coefficient in vector.items())

    profile_pairings = tuple(pair(vector) for vector in vectors)
    require(set(profile_pairings) == {0}, Counter(profile_pairings))
    target_pairing = pair(target)
    require(target_pairing == -311_258_112, target_pairing)
    original_aT = original_structured_aT_vector()
    original_aT_pairing = pair(original_aT)
    require(original_aT_pairing == 0, original_aT_pairing)

    # Re-emit independent canonical ledgers and require byte equality.
    DUAL_OUT.write_text("cycle_partition\tinteger_coefficient\n" + "".join(
        f"{','.join(map(str, partition))}\t{dual[partition]}\n"
        for partition in sorted(dual)))
    TARGET_OUT.write_text("cycle_partition\tnumerator\tdenominator\n" + "".join(
        f"{','.join(map(str, partition))}\t{target[partition].numerator}\t"
        f"{target[partition].denominator}\n"
        # Preserve the frozen ledger's insertion order; coefficient equality
        # was independently checked above from the streamed literal source.
        for partition in tail_target))
    require(DUAL_OUT.read_bytes() == TAIL_DUAL.read_bytes(),
            "dual byte replay differs")
    require(TARGET_OUT.read_bytes() == TAIL_TARGET.read_bytes(),
            "target byte replay differs")

    result = {
        "schema": "orbit0-k16-balanced-cycle-partition-referee-v1",
        "status": "PASS_EXACT_Q_ABSTRACT_SEPARATOR_WITH_CONSERVATION_GUARD",
        "abstract_source": {
            "balanced_ports": 24,
            "row_cycle_partitions": len(row_partitions),
            "four_path_closed_cycle_profiles": len(profiles),
            "distinct_completion_vectors": len(vectors),
            "perfect_matchings_of_eight_endpoints": len(PM8),
            "connected_block_weights": {str(k): v
                                        for k, v in CONNECTED_WEIGHTS.items()},
            "set_partition_type_mass": {
                "+".join(map(str, key)): value
                for key, value in sorted(SET_PARTITION_TYPE_MASS.items())
            },
        },
        "exact_linear_algebra": {
            "rank_over_Q": abstract_rank,
            "dual_space_dimension_over_Q": dual_dimension,
            "rank_with_streamed_target_over_Q": augmented_rank,
            "separator_support": len(dual),
            "separator_max_abs": max(map(abs, dual.values())),
            "separator_primitive_gcd": divisor,
            "abstract_profiles_annihilated": sum(value == 0
                                                  for value in profile_pairings),
        },
        "streamed_target": {
            "literal_H_orbit_records": records,
            "raw_cycle_types": len(raw_cycle_histogram),
            "nonzero_cycle_coordinates": len(target),
            "target_pairing": int(target_pairing),
            "target_vector_sha256": file_sha256(TARGET_OUT),
        },
        "original_structured_aT_guard": {
            "support": len(original_aT),
            "term_mass": sum(original_aT.values()),
            "pairing": int(original_aT_pairing),
            "meaning": (
                "The charge separates the frozen K16 residual but annihilates "
                "the original structured a*H0*H1*H2 target. Therefore omitted "
                "filtration layers/corrections carry the compensating charge; "
                "this is conservation/migration, not full ideal nonmembership."
            ),
        },
        "theorem_scope": {
            "positive": (
                "Every balanced degree24 mixed source column has four positive "
                "path edge lengths and closed cycles totaling20, hence its full "
                "105-term cycle vector is one of the 1162 abstract profiles and "
                "is annihilated by the displayed integer functional."
            ),
            "negative_guard": (
                "The functional need not annihilate a K-truncated slice of a "
                "source column. Nonzero charge on the frozen K16 residual cannot "
                "prove localized or full-source nonmembership because K12--15 "
                "and K17--24 terms may carry the opposite charge."
            ),
        },
        "digests": {
            "dual_sha256": file_sha256(DUAL_OUT),
            "target_sha256": file_sha256(TARGET_OUT),
        },
        "pinned": {
            str(K14_PATH.relative_to(ROOT)): file_sha256(K14_PATH),
            str(LITERAL.relative_to(ROOT)): file_sha256(LITERAL),
            str(TAIL_DUAL.relative_to(ROOT)): file_sha256(TAIL_DUAL),
            str(TAIL_TARGET.relative_to(ROOT)): file_sha256(TAIL_TARGET),
            str(TAIL_RESULT.relative_to(ROOT)): file_sha256(TAIL_RESULT),
        },
    }
    logical = sha256(json.dumps(result, sort_keys=True,
                                separators=(",", ":")).encode()).hexdigest()
    result["logical_sha256"] = logical
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "rank": abstract_rank,
        "augmented_rank": augmented_rank,
        "dual_dimension": dual_dimension,
        "target_pairing": int(target_pairing),
        "original_aT_pairing": int(original_aT_pairing),
        "logical_sha256": logical,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
