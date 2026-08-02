#!/usr/bin/env python3
"""Exact degree-seven closure and dual in the normalized n=8 chart 26.

This checker starts from the six-column normalized contraction, orients all
mixed generators by their squarefree degree-four leading terms, and closes
the resulting invariant component under every degree-nonincreasing column.
Three exact dual-guided extensions exhaust all columns with multiplier
degree at most three which meet the current dual.  The final 49-row rational
functional annihilates every such bounded column and pairs to one with both
the unit and the normalized pure target.

This is a degree-cap theorem only.  Since the normalized ideal is
inhomogeneous, higher-degree S-pairs may cancel their top terms and descend
into degree at most seven.
"""

from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from heapq import heappop, heappush
from itertools import combinations
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
D5_PATH = HERE / "verify_n8_full_source_pure_product_degree5_lift.py"
SPEC = importlib.util.spec_from_file_location("n8_degree5", D5_PATH)
D5 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(D5)

QQ = Fraction
EXPECTED_LEDGER_SHA256 = (
    "2f4fcd2d53c69ea2ec44f7c3d9eb050bd577471be823c02a220e1c1e5d41a570"
)
VERBOSE = False
SEED_COLUMNS = (
    (QQ(-1, 2), 5, bytes.fromhex("0f5d")),
    (QQ(-1, 2), 2919, bytes.fromhex("4f80e1")),
    (QQ(-1, 2), 3002, bytes.fromhex("0f4be2")),
    (QQ(-1, 2), 3064, bytes.fromhex("05ae")),
    (QQ(1, 2), 3780, b""),
    (QQ(-1, 2), 3780, bytes.fromhex("0fec")),
)


def add_value(vector, monomial, value):
    result = vector.get(monomial, QQ(0)) + value
    if result:
        vector[monomial] = result
    else:
        vector.pop(monomial, None)


def multiply(left, right):
    return bytes(sorted(left + right))


def quotient(dividend, divisor):
    counts = Counter(dividend)
    counts.subtract(divisor)
    if any(value < 0 for value in counts.values()):
        return None
    return bytes(
        value for value in sorted(counts) for _ in range(counts[value])
    )


@lru_cache(maxsize=None)
def normalized_generator(code):
    terms = Counter()
    for term in D5.iter_word_terms(code):
        normalized = bytes(
            value for value in term if value not in D5.SUPPORT_IDS
        )
        terms[normalized] += 1
    return dict(terms)


def leading_monomial(polynomial):
    maximum_degree = max(map(len, polynomial))
    # With x_0 > x_1 > ... and fixed total degree, the lexicographically
    # largest exponent vector is the smallest sorted variable tuple.
    return min(term for term in polynomial if len(term) == maximum_degree)


def transformed_column(code, multiplier, transform_index):
    transformed_code = D5.WORD_TRANSFORMS[transform_index][code]
    transform = D5.VARIABLE_TRANSFORMS[transform_index]
    transformed_multiplier = bytes(sorted(transform[value] for value in multiplier))
    return transformed_code, transformed_multiplier


@lru_cache(maxsize=None)
def normalized_row_orbit(row):
    return tuple(sorted(set(
        bytes(sorted(transform[value] for value in row))
        for transform in D5.VARIABLE_TRANSFORMS
    )))


def canonical_normalized_row(row):
    return normalized_row_orbit(row)[0]


def normalized_column_orbit(column):
    code, multiplier = column
    return tuple(sorted(set(
        transformed_column(code, multiplier, index)
        for index in range(len(D5.VARIABLE_TRANSFORMS))
    )))


def canonical_normalized_column(column):
    return normalized_column_orbit(column)[0]


@lru_cache(maxsize=None)
def word_from_top_term(term):
    if len(term) != 4:
        return None
    word = [None] * 8
    for value in term:
        left, right, left_colour, right_colour = D5.COORDINATES[value]
        if word[left] is not None or word[right] is not None:
            return None
        word[left] = left_colour
        word[right] = right_colour
    if any(value is None for value in word) or len(set(word)) == 1:
        return None
    return D5.word_code(tuple(word))


@lru_cache(maxsize=None)
def top_incident_columns(row):
    answer = set()
    for positions in combinations(range(len(row)), 4):
        term = bytes(row[position] for position in positions)
        code = word_from_top_term(term)
        if code is None:
            continue
        selected = set(positions)
        multiplier = bytes(
            row[position] for position in range(len(row))
            if position not in selected
        )
        answer.add(canonical_normalized_column((code, multiplier)))
    return tuple(sorted(answer))


def normalized_column_outputs(column):
    code, multiplier = column
    return tuple(
        (multiply(multiplier, term), coefficient)
        for term, coefficient in normalized_generator(code).items()
    )


def invariant_column_entries(column, row_index):
    entries = defaultdict(int)
    for actual_column in normalized_column_orbit(column):
        for output, coefficient in normalized_column_outputs(actual_column):
            if output == canonical_normalized_row(output):
                entries[row_index[output]] += coefficient
    return dict(entries)


def top_degree_closure(start_rows, forced_columns=(), maximum_rows=2_000_000):
    rows = set(start_rows)
    frontier = set(start_rows)
    columns = set(forced_columns)
    for column in forced_columns:
        for output, _coefficient in normalized_column_outputs(column):
            representative = canonical_normalized_row(output)
            if representative not in rows:
                rows.add(representative)
                frontier.add(representative)
    layers = []
    while frontier:
        new_rows = set()
        new_columns = 0
        for processed, row in enumerate(frontier, 1):
            for column in top_incident_columns(row):
                if column in columns:
                    continue
                columns.add(column)
                new_columns += 1
                for output, _coefficient in normalized_column_outputs(column):
                    representative = canonical_normalized_row(output)
                    if representative not in rows:
                        new_rows.add(representative)
            if VERBOSE and processed % 10000 == 0:
                print("closure frontier", processed, "/", len(frontier),
                      "new rows", len(new_rows), "cols", len(columns), flush=True)
            if len(rows) + len(new_rows) > maximum_rows:
                raise RuntimeError("top-degree closure exceeded row guard")
        new_rows -= rows
        layers.append((len(new_rows), new_columns))
        if VERBOSE:
            print("closure layer", len(layers), "rows", len(rows), "+",
                  len(new_rows), "columns", len(columns), "+", new_columns,
                  flush=True)
        rows.update(new_rows)
        frontier = new_rows
    return tuple(sorted(rows)), tuple(sorted(columns)), tuple(layers)


def modular_rank_and_target(rows, columns, target, prime):
    ordered_rows = tuple(sorted(rows, key=lambda row: (-len(row), row)))
    row_index = {row: index for index, row in enumerate(ordered_rows)}
    matrix = []
    for processed, column in enumerate(columns, 1):
        entries = invariant_column_entries(column, row_index)
        matrix.append(entries)
        if processed % 100 == 0:
            print("matrix", processed, "/", len(columns), "nnz",
                  sum(map(len, matrix)), flush=True)
    matrix.sort(key=lambda vector: (min(vector), len(vector)))

    pivots = {}
    for vector in matrix:
        vector = {row: value % prime for row, value in vector.items()
                  if value % prime}
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            if pivot not in pivots:
                inverse = pow(value, prime - 2, prime)
                pivots[pivot] = {
                    row: coefficient * inverse % prime
                    for row, coefficient in vector.items()
                }
                break
            basis = pivots[pivot]
            for row, coefficient in basis.items():
                result = (vector.get(row, 0) - value * coefficient) % prime
                if result:
                    vector[row] = result
                else:
                    vector.pop(row, None)

    residual = {
        row_index[row]: (
            coefficient.numerator
            * pow(coefficient.denominator, prime - 2, prime)
        ) % prime
        for row, coefficient in target.items() if coefficient
    }
    while residual:
        pivot = min(residual)
        value = residual[pivot]
        if pivot not in pivots:
            break
        for row, coefficient in pivots[pivot].items():
            result = (residual.get(row, 0) - value * coefficient) % prime
            if result:
                residual[row] = result
            else:
                residual.pop(row, None)
    return len(pivots), residual, ordered_rows


def exact_rank_and_target(rows, columns, target):
    ordered_rows = tuple(sorted(rows, key=lambda row: (-len(row), row)))
    row_index = {row: index for index, row in enumerate(ordered_rows)}
    matrix = [invariant_column_entries(column, row_index) for column in columns]
    matrix.sort(key=lambda vector: (min(vector), len(vector)))
    pivots = {}
    maximum_basis = 0
    for processed, source in enumerate(matrix, 1):
        vector = {row: QQ(value) for row, value in source.items() if value}
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            if pivot not in pivots:
                pivots[pivot] = {
                    row: coefficient / value
                    for row, coefficient in vector.items()
                }
                maximum_basis = max(maximum_basis, len(vector))
                break
            basis = pivots[pivot]
            for row, coefficient in basis.items():
                result = vector.get(row, QQ(0)) - value * coefficient
                if result:
                    vector[row] = result
                else:
                    vector.pop(row, None)
        if VERBOSE and processed % 50 == 0:
            print("exact elim", processed, "/", len(matrix), "rank", len(pivots),
                  "max basis", maximum_basis, flush=True)

    work = {
        row_index[row]: QQ(coefficient)
        for row, coefficient in target.items() if coefficient
    }
    remainder = {}
    while work:
        pivot = min(work)
        value = work[pivot]
        if pivot not in pivots:
            remainder[pivot] = value
            work.pop(pivot)
            continue
        for row, coefficient in pivots[pivot].items():
            result = work.get(row, QQ(0)) - value * coefficient
            if result:
                work[row] = result
            else:
                work.pop(row, None)
    remainder_by_row = {
        ordered_rows[row]: value for row, value in remainder.items()
    }
    if not remainder:
        return len(pivots), remainder_by_row, maximum_basis, {}, QQ(0)
    selected = min(remainder)
    dual = {selected: QQ(1)}
    for pivot in sorted(pivots, reverse=True):
        value = -sum(
            coefficient * dual.get(row, QQ(0))
            for row, coefficient in pivots[pivot].items()
            if row != pivot
        )
        if value:
            dual[pivot] = value
    dual_by_row = {
        ordered_rows[row]: value for row, value in dual.items()
    }
    for source in matrix:
        pairing = sum(
            QQ(coefficient) * dual.get(row, QQ(0))
            for row, coefficient in source.items()
        )
        if pairing:
            raise RuntimeError("exact closure dual does not annihilate a column")
    target_pairing = sum(
        coefficient * dual_by_row.get(row, QQ(0))
        for row, coefficient in target.items()
    )
    if target_pairing != remainder[selected]:
        raise RuntimeError("exact closure dual has the wrong pairings")
    return (len(pivots), remainder_by_row, maximum_basis, dual_by_row,
            target_pairing)


@lru_cache(maxsize=None)
def codes_for_normalized_term(term):
    if len(term) > 4:
        return ()
    assigned = {}
    for value in term:
        left, right, left_colour, right_colour = D5.COORDINATES[value]
        if left in assigned or right in assigned:
            return ()
        assigned[left] = left_colour
        assigned[right] = right_colour
    remaining = set(range(8)) - set(assigned)
    support_values = tuple(sorted(D5.SUPPORT_IDS))
    codes = set()
    for completion in combinations(support_values, 4 - len(term)):
        word = dict(assigned)
        valid = True
        covered = set()
        for value in completion:
            left, right, left_colour, right_colour = D5.COORDINATES[value]
            if (left not in remaining or right not in remaining
                    or left in covered or right in covered):
                valid = False
                break
            covered.update((left, right))
            word[left] = left_colour
            word[right] = right_colour
        if not valid or covered != remaining:
            continue
        values = tuple(word[index] for index in range(8))
        if len(set(values)) > 1:
            codes.add(D5.word_code(values))
    return tuple(sorted(codes))


def bounded_incident_columns(rows, maximum_output_degree=7):
    columns = set()
    for row in rows:
        for term in set(divisors(row, range(5))):
            multiplier = quotient(row, term)
            if multiplier is None or len(multiplier) + 4 > maximum_output_degree:
                continue
            for code in codes_for_normalized_term(term):
                columns.add(canonical_normalized_column((code, multiplier)))
    return columns


def dual_violating_columns(dual, known_columns):
    candidates = bounded_incident_columns(dual)
    violating = set()
    pairing_histogram = Counter()
    for column in candidates:
        pairing = QQ(0)
        for actual_column in normalized_column_orbit(column):
            for output, coefficient in normalized_column_outputs(actual_column):
                if output == canonical_normalized_row(output):
                    pairing += dual.get(output, QQ(0)) * coefficient
        if pairing:
            pairing_histogram[pairing] += 1
            if column not in known_columns:
                violating.add(column)
    return candidates, violating, pairing_histogram


def audit_expanded_dual(dual, incident_columns):
    full_weights = {
        row: value / len(normalized_row_orbit(row))
        for row, value in dual.items()
    }
    actual_columns = set()
    for column in incident_columns:
        for actual_column in normalized_column_orbit(column):
            actual_columns.add(actual_column)
            pairing = QQ(0)
            for output, coefficient in normalized_column_outputs(actual_column):
                representative = canonical_normalized_row(output)
                pairing += full_weights.get(representative, QQ(0)) * coefficient
            if pairing:
                raise RuntimeError(
                    "expanded bounded dual does not annihilate an actual column"
                )
    return len(actual_columns)


def pure_target_on_rows(rows):
    pure = tuple(
        normalized_generator(D5.word_code((colour,) * 8))
        for colour in range(3)
    )
    last = dict(pure[2])
    answer = {}
    for target in rows:
        coefficient = 0
        target_counter = Counter(target)
        for first, first_coefficient in pure[0].items():
            if not Counter(first) <= target_counter:
                continue
            after_first = quotient(target, first)
            after_first_counter = Counter(after_first)
            for second, second_coefficient in pure[1].items():
                if not Counter(second) <= after_first_counter:
                    continue
                third = quotient(after_first, second)
                coefficient += (
                    first_coefficient * second_coefficient * last.get(third, 0)
                )
        if coefficient:
            answer[target] = coefficient
    return answer


def fraction_histogram(values):
    return [
        [[value.numerator, value.denominator], count]
        for value, count in sorted(Counter(values).items())
    ]


def seed_residual():
    image = {}
    canonical_columns = set()
    actual_columns = set()
    for coefficient, code, multiplier in SEED_COLUMNS:
        canonical = D5.canonical_column((code, multiplier))
        if canonical != (code, multiplier):
            raise RuntimeError("seed column is not canonical")
        canonical_columns.add(canonical)
        orbit = set(
            transformed_column(code, multiplier, index)
            for index in range(len(D5.VARIABLE_TRANSFORMS))
        )
        for actual_code, actual_multiplier in orbit:
            actual_columns.add((actual_code, actual_multiplier))
            for term, multiplicity in normalized_generator(actual_code).items():
                add_value(
                    image,
                    multiply(actual_multiplier, term),
                    coefficient * multiplicity,
                )
    if image.get(b"", 0) != 1:
        raise RuntimeError("seed relation does not have constant coefficient one")
    image.pop(b"")
    return image, canonical_columns, actual_columns


def reducer_index():
    by_lead = defaultdict(list)
    degree_histogram = Counter()
    constant_words = []
    for code in range(3 ** 8):
        word = D5.decode_word(code)
        if len(set(word)) == 1:
            continue
        polynomial = normalized_generator(code)
        lead = leading_monomial(polynomial)
        by_lead[lead].append(code)
        degree_histogram[len(lead)] += 1
        if b"" in polynomial:
            constant_words.append(code)
    return {
        lead: tuple(sorted(words)) for lead, words in by_lead.items()
    }, degree_histogram, tuple(constant_words)


def divisors(monomial, degrees):
    for degree in degrees:
        if degree > len(monomial):
            continue
        seen = set()
        for positions in combinations(range(len(monomial)), degree):
            candidate = bytes(monomial[position] for position in positions)
            if candidate not in seen:
                seen.add(candidate)
                yield candidate


def reduce_polynomial(polynomial, by_lead, report_every=10000):
    work = dict(polynomial)
    remainder = {}
    certificate = {}
    heaps = defaultdict(list)
    for monomial in work:
        heappush(heaps[len(monomial)], monomial)
    degrees = tuple(sorted({len(lead) for lead in by_lead}, reverse=True))
    steps = 0
    maximum_terms = len(work)

    while work:
        degree = max(index for index, heap in heaps.items() if heap)
        heap = heaps[degree]
        while heap and heap[0] not in work:
            heappop(heap)
        if not heap:
            continue
        monomial = heappop(heap)
        coefficient = work.pop(monomial)

        choices = []
        for divisor in divisors(monomial, degrees):
            words = by_lead.get(divisor)
            if words:
                # Prefer the largest leading divisor, then the first word.
                choices.append((len(divisor), divisor, words[0]))
        if not choices:
            remainder[monomial] = coefficient
            continue
        _lead_degree, lead, code = max(
            choices, key=lambda item: (item[0], tuple(-x for x in item[1]), -item[2])
        )
        multiplier = quotient(monomial, lead)
        if multiplier is None:
            raise RuntimeError("selected leading monomial does not divide row")
        polynomial_g = normalized_generator(code)
        lead_coefficient = polynomial_g[lead]
        factor = coefficient / lead_coefficient
        column = (code, multiplier)
        add_value(certificate, column, factor)
        for term, value in polynomial_g.items():
            output = multiply(multiplier, term)
            if output == monomial:
                continue
            # Global graded lex: no output may exceed the cancelled lead.
            if len(output) > len(monomial):
                raise RuntimeError("graded reducer raised total degree")
            if len(output) == len(monomial) and output <= monomial:
                raise RuntimeError("graded reducer failed to lower lex order")
            was_absent = output not in work
            add_value(work, output, -factor * value)
            if was_absent and output in work:
                heappush(heaps[len(output)], output)
        steps += 1
        maximum_terms = max(maximum_terms, len(work))
        if report_every and steps % report_every == 0:
            print(
                "steps", steps, "work", len(work), "remainder", len(remainder),
                "certificate", len(certificate), "degree", degree,
                "maxwork", maximum_terms, flush=True,
            )
    return remainder, certificate, steps, maximum_terms


def main():
    residual, canonical_seed, actual_seed = seed_residual()
    by_lead, degree_histogram, constant_words = reducer_index()
    if VERBOSE:
        print("seed canonical/actual", len(canonical_seed), len(actual_seed))
        print("seed residual", len(residual), "degrees", Counter(map(len, residual)))
        print("reducers leads", len(by_lead), "hist",
              sorted(degree_histogram.items()))
        print("constant mixed words", constant_words)
    remainder, certificate, steps, maximum_terms = reduce_polynomial(
        residual, by_lead, report_every=0
    )
    if VERBOSE:
        print("RESULT remainder", len(remainder), "degrees",
              Counter(map(len, remainder)))
        print("certificate", len(certificate), "steps", steps, "maxwork",
              maximum_terms)
    invariant_residual = {}
    for row, coefficient in residual.items():
        representative = canonical_normalized_row(row)
        if representative in invariant_residual:
            if invariant_residual[representative] != coefficient:
                raise RuntimeError("seed residual is not invariant")
        else:
            invariant_residual[representative] = coefficient
    if VERBOSE:
        print("invariant residual", len(invariant_residual), "degrees",
              Counter(map(len, invariant_residual)))
    rows, columns, layers = top_degree_closure(invariant_residual)
    if VERBOSE:
        print("TOP CLOSURE", len(rows), len(columns), "layers", layers)
    rank, target_remainder, maximum_basis, dual, target_pairing = exact_rank_and_target(
        rows, columns, invariant_residual
    )
    if VERBOSE:
        print("EXACT rank", rank, "remainder",
              [(row.hex(), value) for row, value in target_remainder.items()],
              "max basis", maximum_basis)
        print("DUAL support", len(dual), "degrees", Counter(map(len, dual)),
              "coefficients", Counter(dual.values()), "pairing",
              target_pairing)
    closure_records = []
    forced = set()
    round_number = 0
    while True:
        candidates, violating, pairing_histogram = dual_violating_columns(
            dual, set(columns)
        )
        closure_records.append({
            "round": round_number,
            "rows": len(rows),
            "columns": len(columns),
            "rank": rank,
            "layers": [list(item) for item in layers],
            "dual_support": len(dual),
            "dual_degree_histogram": dict(sorted(Counter(map(len, dual)).items())),
            "dual_coefficient_histogram": fraction_histogram(dual.values()),
            "target_remainder": [
                [row.hex(), value.numerator, value.denominator]
                for row, value in sorted(target_remainder.items())
            ],
            "target_pairing": [target_pairing.numerator,
                               target_pairing.denominator],
            "bounded_incident_columns": len(candidates),
            "new_dual_violating_columns": len(violating),
            "violating_pairing_histogram": fraction_histogram(
                pairing for pairing, count in pairing_histogram.items()
                for _ in range(count)
            ),
        })
        if VERBOSE:
            print("ADAPT", round_number, "dual", len(dual), "candidates",
                  len(candidates), "new violating", len(violating), "pairings",
                  pairing_histogram, flush=True)
        if not violating:
            break
        round_number += 1
        if round_number > 8:
            raise RuntimeError("adaptive closure did not terminate")
        forced.update(violating)
        rows, columns, layers = top_degree_closure(
            invariant_residual, forced_columns=forced
        )
        if VERBOSE:
            print("ADAPT CLOSURE", round_number, len(rows), len(columns),
                  layers, flush=True)
        rank, target_remainder, maximum_basis, dual, target_pairing = (
            exact_rank_and_target(rows, columns, invariant_residual)
        )
        if VERBOSE:
            print("ADAPT EXACT", round_number, "rank", rank, "remainder",
                  len(target_remainder), "dual", len(dual), "pairing",
                  target_pairing, flush=True)
        if not target_remainder:
            break

    if [record["rows"] for record in closure_records] != [
            20859, 134041, 216350, 273857]:
        raise RuntimeError("adaptive closure row census changed")
    if [record["columns"] for record in closure_records] != [
            298, 1849, 2955, 3721]:
        raise RuntimeError("adaptive closure column census changed")
    if any(record["rank"] != record["columns"]
           for record in closure_records):
        raise RuntimeError("an adaptive top-degree component gained a syzygy")
    if [record["new_dual_violating_columns"]
            for record in closure_records] != [13, 8, 6, 0]:
        raise RuntimeError("dual-guided violation census changed")
    if target_remainder != {b"": QQ(-1)}:
        raise RuntimeError("final bounded target remainder changed")
    if len(dual) != 49 or dual.get(b"") != 1:
        raise RuntimeError("final bounded dual support changed")
    actual_incident_columns = audit_expanded_dual(dual, candidates)

    pure_target = pure_target_on_rows(dual)
    pure_pairing = sum(
        dual[row] * coefficient for row, coefficient in pure_target.items()
    )
    if VERBOSE:
        print("PURE target support on dual", len(pure_target), "pairing",
              pure_pairing)

    final_dual_record = [
        [row.hex(), value.numerator, value.denominator]
        for row, value in sorted(dual.items())
    ]
    final_dual_digest = sha256(json.dumps(
        final_dual_record, separators=(",", ":")
    ).encode()).hexdigest()
    ledger = {
        "normalized_variables": 240,
        "mixed_generators": 6558,
        "constant_term_mixed_generators": list(constant_words),
        "distinct_graded_lex_leading_monomials": len(by_lead),
        "leading_degree_histogram": dict(sorted(degree_histogram.items())),
        "six_seed_canonical_columns": len(canonical_seed),
        "six_seed_actual_columns": len(actual_seed),
        "seed_invariant_tail_rows": len(invariant_residual),
        "seed_invariant_degree_histogram": dict(sorted(
            Counter(map(len, invariant_residual)).items()
        )),
        "raw_graded_lex_division_steps": steps,
        "raw_graded_lex_remainder_rows": len(remainder),
        "raw_graded_lex_remainder_degree_histogram": dict(sorted(
            Counter(map(len, remainder)).items()
        )),
        "raw_graded_lex_remainder_coefficient_histogram": fraction_histogram(
            remainder.values()
        ),
        "adaptive_closure": closure_records,
        "forced_external_column_orbits": len(forced),
        "final_bounded_dual_support": len(dual),
        "final_bounded_dual_degree_histogram": dict(sorted(
            Counter(map(len, dual)).items()
        )),
        "final_bounded_dual_coefficient_histogram": fraction_histogram(
            dual.values()
        ),
        "final_bounded_dual_sha256": final_dual_digest,
        "final_bounded_dual_unit_pairing": [1, 1],
        "final_bounded_dual_incident_column_orbits": len(candidates),
        "final_bounded_dual_incident_actual_columns": actual_incident_columns,
        "pure_target_support_on_final_dual": len(pure_target),
        "pure_target_pairing": [pure_pairing.numerator, pure_pairing.denominator],
        "degree_cap": 7,
        "multiplier_degree_cap": 3,
        "conclusion": (
            "no normalized unit certificate using mixed-generator "
            "multipliers of degree at most three"
        ),
        "scope_guard": (
            "inhomogeneous higher-degree S-pairs may cancel their top terms "
            "and descend below degree eight; this is not an unrestricted "
            "localized nonmembership obstruction"
        ),
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED" and digest != EXPECTED_LEDGER_SHA256:
        raise RuntimeError("normalized top-degree closure ledger changed")
    print(
        "n=8 chart26 normalized degree-seven closure: PASS; "
        "adaptive rows/columns=273857/3721, rank=3721, final dual=49"
    )
    print(json.dumps(ledger, sort_keys=True))
    print("sha256:", digest)


if __name__ == "__main__":
    main()
