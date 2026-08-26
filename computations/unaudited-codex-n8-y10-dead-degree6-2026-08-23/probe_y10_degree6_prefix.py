#!/usr/bin/env python3
"""Modular target-rooted filtered closure for all d6 divisors of y10*t2."""

from collections import defaultdict, deque
from itertools import combinations, combinations_with_replacement
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PATH = ROOT / "computations/verify_n8_chart26_weighted_degree6_census.py"


def load():
    spec = importlib.util.spec_from_file_location("d6prefix_source", PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def divisors(row, degree):
    if degree == 0:
        return {b""}
    return {bytes(row[index] for index in positions)
            for positions in combinations(range(len(row)), degree)}


def add_value(vector, row, value, prime):
    value = (vector.get(row, 0) + value) % prime
    if value:
        vector[row] = value
    else:
        vector.pop(row, None)


def row_weight(row, coordinates):
    answer = [0] * 24
    for value in row:
        i, j, a, b = coordinates[value]
        answer[3 * i + a] += 1
        answer[3 * j + b] += 1
    return tuple(answer)


def subtract(left, right):
    answer = tuple(a - b for a, b in zip(left, right))
    return answer if min(answer, default=0) >= 0 else None


def word_from_weight(value):
    if value is None:
        return None
    word = []
    for site in range(8):
        block = value[3 * site:3 * site + 3]
        if sum(block) != 1 or max(block) != 1:
            return None
        word.append(block.index(1))
    return tuple(word)


def encode_word(word):
    code = 0
    for value in word:
        code = 3 * code + value
    return code


def audit(prime=1009, cap=200000):
    M = load()
    F, D = M.FIRST, M.D5
    originals, _d4, _c2l, _d5, words = M.build_leads()
    coordinates = D.COORDINATES
    term_sources = defaultdict(list)
    for code, polynomial in originals.items():
        for row in polynomial:
            term_sources[row].append(code)

    off = tuple(index for index in range(len(coordinates))
                if D.IS_OFF_SUPPORT[index])
    pair_by_weight = defaultdict(list)
    for left, right in combinations_with_replacement(off, 2):
        multiplier = bytes((left, right))
        pair_by_weight[row_weight(multiplier, coordinates)].append(multiplier)
    word_weights = {}
    for code, word in words.items():
        value = [0] * 24
        for site, colour in enumerate(word):
            value[3 * site + colour] = 1
        word_weights[code] = tuple(value)

    column_cache = {}
    def column(key):
        if key not in column_cache:
            code, multiplier = key
            vector = {}
            for row, coefficient in originals[code].items():
                add_value(vector, bytes(sorted(row + multiplier)), coefficient, prime)
            column_cache[key] = vector
        return dict(column_cache[key])

    def grade_of(key):
        code, multiplier = key
        return tuple(a + b for a, b in zip(
            word_weights[code], row_weight(multiplier, coordinates)))

    grade_columns_cache = {}
    def grade_columns(grade):
        if grade not in grade_columns_cache:
            answer = []
            for multiplier_weight, multipliers in pair_by_weight.items():
                word = word_from_weight(subtract(grade, multiplier_weight))
                if word is None or len(set(word)) == 1:
                    continue
                code = encode_word(word)
                if code in originals:
                    answer.extend((code, multiplier) for multiplier in multipliers)
            grade_columns_cache[grade] = tuple(sorted(answer))
        return grade_columns_cache[grade]

    def eliminate_at_degree(vectors, degree):
        pivots = {}
        tails = []
        for source in vectors:
            work = dict(source)
            while True:
                active = [row for row in work if len(row) == degree]
                if not active:
                    if work:
                        tails.append(work)
                    break
                lead = min(active)
                if lead not in pivots:
                    inverse = pow(work[lead], prime - 2, prime)
                    work = {row: value * inverse % prime
                            for row, value in work.items()}
                    pivots[lead] = work
                    break
                scale = work[lead]
                for row, value in pivots[lead].items():
                    add_value(work, row, -scale * value, prime)
        return pivots, tails

    target = bytes.fromhex("0111202020494f4f50f8")
    candidates = {degree: sorted(divisors(target, degree))
                  for degree in (4, 5, 6)}

    pending_grades = deque()
    seen_grades = set()
    pending_direct5 = deque()
    seen_direct5 = set()
    pending_rows5 = deque(candidates[5])
    seen_rows5 = set(candidates[5])
    generators5 = []
    top6_pivot_count = 0
    top6_kernel_tail_count = 0

    def schedule_column(key):
        code, multiplier = key
        if len(multiplier) == 2:
            grade = grade_of(key)
            if grade not in seen_grades:
                seen_grades.add(grade)
                pending_grades.append(grade)
        elif len(multiplier) == 1 and key not in seen_direct5:
            seen_direct5.add(key)
            pending_direct5.append(key)

    def inverse_columns(row, multiplier_degrees):
        for degree in multiplier_degrees:
            for multiplier in divisors(row, degree):
                base = F.quotient(row, multiplier)
                for code in term_sources.get(base, ()):
                    yield code, multiplier

    for row in candidates[4] + candidates[5]:
        for key in inverse_columns(row, (1, 2)):
            schedule_column(key)

    processed_rows = 0
    while pending_grades or pending_direct5 or pending_rows5:
        while pending_grades:
            grade = pending_grades.popleft()
            vectors = [column(key) for key in grade_columns(grade)]
            pivots6, tails = eliminate_at_degree(vectors, 6)
            top6_pivot_count += len(pivots6)
            top6_kernel_tail_count += len(tails)
            for tail in tails:
                generators5.append(tail)
                for row in tail:
                    if len(row) == 5 and row not in seen_rows5:
                        seen_rows5.add(row)
                        pending_rows5.append(row)
        while pending_direct5:
            key = pending_direct5.popleft()
            vector = column(key)
            generators5.append(vector)
            for row in vector:
                if len(row) == 5 and row not in seen_rows5:
                    seen_rows5.add(row)
                    pending_rows5.append(row)
        if pending_rows5:
            row = pending_rows5.popleft()
            processed_rows += 1
            for key in inverse_columns(row, (1, 2)):
                schedule_column(key)
        if len(seen_rows5) > cap:
            return {
                "status": "ROW5_CAP", "prime": prime,
                "grades": len(seen_grades), "direct5": len(seen_direct5),
                "rows5": len(seen_rows5), "generators5": len(generators5),
                "processed_rows5": processed_rows,
            }

    pivots5, tails4 = eliminate_at_degree(generators5, 5)
    naive_direct5_leads = [
        min(row for row in column(key) if len(row) == 5)
        for key in sorted(seen_direct5)
    ]
    return {
        "status": "Y5_CLOSED", "prime": prime,
        "grades": len(seen_grades), "grade_columns": sum(
            len(grade_columns(grade)) for grade in seen_grades),
        "top6_pivots": top6_pivot_count,
        "top6_kernel_tails": top6_kernel_tail_count,
        "direct5": len(seen_direct5), "rows5": len(seen_rows5),
        "generators5": len(generators5), "rank5": len(pivots5),
        "tails4": len(tails4),
        "direct5_naive_leads_distinct": (
            len(set(naive_direct5_leads)) == len(naive_direct5_leads)
        ),
        "direct5_naive_target_hits": sorted(
            row.hex() for row in set(naive_direct5_leads) & set(candidates[5])
        ),
        "direct5_keys": [[code, multiplier.hex()]
                         for code, multiplier in sorted(seen_direct5)],
        "pivot5_rows": sorted(row.hex() for row in pivots5),
        "target_y5_pivots": sorted(row.hex() for row in candidates[5]
                                   if row in pivots5),
        "cache_columns": len(column_cache),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(audit(), sort_keys=True))
