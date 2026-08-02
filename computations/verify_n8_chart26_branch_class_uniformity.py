#!/usr/bin/env python3
"""Refine the two branch-only weighted degree-six census classes.

This checker starts from the complete weighted degree-four and degree-five
lead dictionaries.  It re-enumerates every member of the coarse 8,412 and
45,776 classes, retains the actual source labels, and counts their selected
support-stabilizer types.  The second pass audits the source-cube patterns
which control the closed/open vertex split.

The expensive polynomial audit is intentionally kept separate from the
coarse degree-six census: only the two selected classes are expanded.
"""

from collections import Counter, defaultdict
from heapq import heapify, heappop, heappush
from hashlib import sha256
from itertools import combinations
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CENSUS = load(
    "n8_chart26_branch_uniformity_census",
    "verify_n8_chart26_weighted_degree6_census.py",
)
FIRST = CENSUS.FIRST
COMPLETE = CENSUS.COMPLETE
D5 = CENSUS.D5
WEIGHT = CENSUS.WEIGHT

EXPECTED_LEDGER_SHA256 = (
    "c03003ac8d6261314c2dd5310e97be41ba4651e2c8acf2a2b8ae20f2c95475e9"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def hamming(first, second, words):
    return sum(a != b for a, b in zip(words[first], words[second]))


def target_45_signature(core, first, second, degree4, degree5, words):
    source_code = degree4[first]
    left, right, distance = degree5[second]
    source_signature = (
        distance,
        *sorted((hamming(source_code, left, words),
                 hamming(source_code, right, words))),
    )
    return (
        source_signature == (2, 1, 1)
        and CENSUS.overlap_signature(core, first, second) == (
            ((1, 1, 1, 1, 1, 1), (1, 1, 1)),
            ((3, 2, 2, 1, 1, 1, 1, 1), (2, 1, 1, 1, 1)),
        )
    )


def target_55_signature(core, first, second, degree5, words):
    first_left, first_right, first_distance = degree5[first]
    second_left, second_right, second_distance = degree5[second]
    first_sources = {first_left, first_right}
    second_sources = {second_left, second_right}
    cross_distances = tuple(sorted(
        hamming(left, right, words)
        for left in first_sources for right in second_sources
    ))
    source_signature = (
        min(first_distance, second_distance),
        max(first_distance, second_distance),
        len(first_sources & second_sources),
        cross_distances,
    )
    return (
        source_signature == (1, 2, 1, (0, 1, 1, 2))
        and CENSUS.overlap_signature(core, first, second) == (
            ((2, 1, 1, 1, 1, 1, 1), (1, 1, 1, 1)),
            ((3, 2, 2, 1, 1, 1, 1, 1), (2, 1, 1, 1, 1)),
        )
    )


def enumerate_target_pairs(degree4, degree5, words):
    degree4_by_three = defaultdict(list)
    degree5_by_three = defaultdict(list)
    for monomial in degree4:
        for core in combinations(monomial, 3):
            degree4_by_three[bytes(core)].append(monomial)
    for monomial in degree5:
        for core in combinations(monomial, 3):
            degree5_by_three[bytes(core)].append(monomial)

    pairs45 = []
    for core, firsts in degree4_by_three.items():
        for first in firsts:
            for second in degree5_by_three.get(core, ()):
                if (len(set(first) & set(second)) == 3
                        and target_45_signature(
                            core, first, second, degree4, degree5, words
                        )):
                    pairs45.append((first, second))

    degree5_by_four = defaultdict(list)
    for monomial in degree5:
        for core in combinations(monomial, 4):
            degree5_by_four[bytes(core)].append(monomial)
    pairs55 = []
    for core, monomials in degree5_by_four.items():
        for index, first in enumerate(monomials):
            for second in monomials[index + 1:]:
                if target_55_signature(core, first, second, degree5, words):
                    pairs55.append((first, second))

    require(len(pairs45) == 8412, "the branch-only 45 class changed")
    require(len(pairs55) == 45776, "the branch-only 55 class changed")
    return pairs45, pairs55


def canonical_lead_pair(kind, pair):
    first, second = pair
    if kind == "45":
        return min(
            bytes(sorted(transform[value] for value in first))
            + bytes(sorted(transform[value] for value in second))
            for transform in D5.VARIABLE_TRANSFORMS
        )
    return min(
        b"".join(sorted((
            bytes(sorted(transform[value] for value in first)),
            bytes(sorted(transform[value] for value in second)),
        )))
        for transform in D5.VARIABLE_TRANSFORMS
    )


def canonical_source_label(kind, pair, degree4, degree5):
    first, second = pair
    if kind == "45":
        code = degree4[first]
        left, right, _distance = degree5[second]
        return min(
            (D5.WORD_TRANSFORMS[index][code],)
            + tuple(sorted((D5.WORD_TRANSFORMS[index][left],
                            D5.WORD_TRANSFORMS[index][right])))
            for index in range(len(D5.WORD_TRANSFORMS))
        )

    first_sources = degree5[first][:2]
    second_sources = degree5[second][:2]
    return min(
        tuple(sorted((
            tuple(sorted(D5.WORD_TRANSFORMS[index][code]
                         for code in first_sources)),
            tuple(sorted(D5.WORD_TRANSFORMS[index][code]
                         for code in second_sources)),
        )))
        for index in range(len(D5.WORD_TRANSFORMS))
    )


def source_pattern(kind, pair, degree4, degree5, words):
    """Return the abstract Hamming-square incidence of one labelled pair."""
    first, second = pair
    if kind == "45":
        middle = degree4[first]
        left, right, distance = degree5[second]
        require(distance == 2, "45 transport stopped being a double move")
        differing = tuple(
            index for index, values in enumerate(zip(words[left], words[right]))
            if values[0] != values[1]
        )
        require(len(differing) == 2, "45 source square lost two directions")
        require(hamming(middle, left, words) == 1
                and hamming(middle, right, words) == 1,
                "45 generator stopped being a source-square corner")
        other_word = list(words[middle])
        for position in differing:
            if words[middle][position] == words[left][position]:
                other_word[position] = words[right][position]
            else:
                other_word[position] = words[left][position]
        other = D5.word_code(tuple(other_word))
        require(hamming(other, left, words) == hamming(other, right, words) == 1,
                "45 fourth square corner is invalid")
        return (middle, min(left, right), max(left, right), other, differing)

    first_sources = set(degree5[first][:2])
    second_sources = set(degree5[second][:2])
    shared = tuple(first_sources & second_sources)
    require(len(shared) == 1, "55 cells stopped sharing one source")
    center = shared[0]
    outer_first = next(iter(first_sources - {center}))
    outer_second = next(iter(second_sources - {center}))
    distances = (hamming(center, outer_first, words),
                 hamming(center, outer_second, words))
    require(sorted(distances) == [1, 2],
            "55 shared-source directions changed")
    near = outer_first if distances[0] == 1 else outer_second
    far = outer_second if distances[0] == 1 else outer_first
    differing = tuple(
        index for index, values in enumerate(zip(words[center], words[far]))
        if values[0] != values[1]
    )
    require(len(differing) == 2 and hamming(near, far, words) == 1,
            "55 sources stopped spanning three sides of a square")
    fourth_word = list(words[center])
    for position in differing:
        if words[near][position] == words[center][position]:
            fourth_word[position] = words[far][position]
    fourth = D5.word_code(tuple(fourth_word))
    require(hamming(fourth, center, words) == 1
            and hamming(fourth, near, words) == 2
            and hamming(fourth, far, words) == 1,
            "55 fourth source-square corner is invalid")
    return (center, near, far, fourth, differing)


def multiplicity_histogram(counter):
    return dict(sorted(Counter(counter.values()).items()))


def add_value(polynomial, monomial, coefficient, heap=None):
    value = polynomial.get(monomial, 0) + coefficient
    if value:
        polynomial[monomial] = value
        if heap is not None:
            heappush(heap, (order_key(monomial), monomial))
    else:
        polynomial.pop(monomial, None)


def add_scaled(target, source, scalar, multiplier):
    for monomial, coefficient in source.items():
        add_value(
            target,
            FIRST.multiply(multiplier, monomial),
            scalar * coefficient,
        )


def order_key(monomial):
    return -len(monomial), -WEIGHT.weight(monomial), monomial


def weighted_lead(polynomial):
    return min(polynomial, key=order_key)


def repeated_excess(monomial):
    return sum(value - 1 for value in Counter(monomial).values())


def remove_copies(monomial, variable, count):
    result = list(monomial)
    for _index in range(count):
        require(variable in result, "localized pivot lost its split factor")
        result.remove(variable)
    return bytes(result)


def polynomial_audit(
        kind, pairs, originals, degree4, code_to_lead, degree5):
    """Expand and exactly lower-reduce every member of one selected class."""
    normalized_originals = {}

    def original_polynomial(lead):
        if lead not in normalized_originals:
            source = originals[degree4[lead]]
            pivot = source[lead]
            require(abs(pivot) == 1, "an original pivot left the unit group")
            normalized_originals[lead] = {
                row: value // pivot for row, value in source.items()
            }
        return normalized_originals[lead]

    def transport_polynomial(lead):
        first, second, _distance = degree5[lead]
        lcm = bytes(sorted(
            set(code_to_lead[first]) | set(code_to_lead[second])
        ))
        source = COMPLETE.s_polynomial(
            lcm, first, second, originals, code_to_lead
        )
        pivot = source[lead]
        require(abs(pivot) == 1, "a transport pivot left the unit group")
        return {row: value // pivot for row, value in source.items()}

    def basis_polynomial(cell_kind, lead, local):
        key = cell_kind, lead
        if key not in local:
            local[key] = (original_polynomial(lead) if cell_kind == "4"
                          else transport_polynomial(lead))
        return local[key]

    def source_spoly(pair, local):
        first, second = pair
        first_kind = "4" if kind == "45" else "5"
        lcm = CENSUS.monomial_lcm(first, second)
        answer = {}
        add_scaled(
            answer,
            basis_polynomial(first_kind, first, local),
            1,
            FIRST.quotient(lcm, first),
        )
        add_scaled(
            answer,
            basis_polynomial("5", second, local),
            -1,
            FIRST.quotient(lcm, second),
        )
        return answer

    def reduce_full(source, local):
        work = dict(source)
        heap = [(order_key(row), row) for row in work]
        heapify(heap)
        remainder = {}
        certificate = []
        while heap:
            _key, row = heappop(heap)
            if row not in work:
                continue
            coefficient = work.pop(row)
            choice = None
            if len(row) >= 5:
                for divisor in FIRST.divisors(row, 5):
                    if divisor in degree5:
                        choice = "5", divisor
                        break
            if choice is None and len(row) >= 4:
                for divisor in FIRST.divisors(row, 4):
                    if divisor in degree4:
                        choice = "4", divisor
                        break
            if choice is None:
                remainder[row] = coefficient
                continue
            cell_kind, lead = choice
            reducer = basis_polynomial(cell_kind, lead, local)
            multiplier = FIRST.quotient(row, lead)
            factor = coefficient
            certificate.append((cell_kind, lead, multiplier, factor))
            for term, value in reducer.items():
                output = FIRST.multiply(multiplier, term)
                if output != row:
                    require(order_key(output) > order_key(row),
                            "a weighted class reduction increased")
                    add_value(work, output, -factor * value, heap)
            require(len(certificate) <= 100,
                    "a selected class developed a long lower reduction")
        return remainder, certificate

    def lower_divisor(monomial):
        if len(monomial) >= 5 and any(
                divisor in degree5 for divisor in FIRST.divisors(monomial, 5)):
            return True
        return len(monomial) >= 4 and any(
            divisor in degree4 for divisor in FIRST.divisors(monomial, 4)
        )

    outcome = Counter()
    squarefree_skeletons = Counter()
    certificate_lengths = Counter()
    repeated_variables = Counter()
    localized_skeletons = Counter()
    closed_surviving_columns = Counter()
    normality_failures = 0
    source_type_outcomes = defaultdict(Counter)
    ledger_digest = sha256()

    for pair_index, pair in enumerate(pairs, 1):
        local = {}
        source = source_spoly(pair, local)
        remainder, certificate = reduce_full(source, local)
        certificate_lengths[len(certificate)] += 1
        if not remainder:
            outcome["zero"] += 1
            source_type_outcomes[
                canonical_source_label(kind, pair, degree4, degree5)
            ]["zero"] += 1
            record = (pair[0].hex(), pair[1].hex(), "zero", len(certificate))
            ledger_digest.update(repr(record).encode() + b"\n")
            continue

        lead = weighted_lead(remainder)
        excess = repeated_excess(lead)
        if not excess:
            outcome["squarefree"] += 1
            source_type_outcomes[
                canonical_source_label(kind, pair, degree4, degree5)
            ]["squarefree"] += 1
            squarefree_skeletons[CENSUS.skeleton_type(lead)] += 1
            record = (
                pair[0].hex(), pair[1].hex(), "squarefree",
                lead.hex(), len(certificate),
            )
            ledger_digest.update(repr(record).encode() + b"\n")
            continue

        outcome["branch"] += 1
        source_type_outcomes[
            canonical_source_label(kind, pair, degree4, degree5)
        ]["branch"] += 1
        multiplicities = Counter(lead)
        repeated = tuple(
            value for value, count in multiplicities.items() if count > 1
        )
        require(excess == 1 and len(repeated) == 1
                and multiplicities[repeated[0]] == 2,
                "a branch lead is not one simple double collision")
        x = repeated[0]
        repeated_variables[f"{x:02x}"] += 1

        # The complete source-labelled expression for G consists of its two
        # S-pair columns followed by the replayed lower reductions.  On x=0,
        # precisely the columns whose multipliers avoid x survive and give
        # an explicit restricted lower-complex contraction.
        first, second = pair
        lcm = CENSUS.monomial_lcm(first, second)
        expression = [
            ("4" if kind == "45" else "5", first,
             FIRST.quotient(lcm, first), 1),
            ("5", second, FIRST.quotient(lcm, second), -1),
        ]
        expression.extend(
            (cell_kind, reducer, multiplier, -factor)
            for cell_kind, reducer, multiplier, factor in certificate
        )
        survivors = [column for column in expression if x not in column[2]]
        require(survivors,
                "a closed branch lost its source-labelled contraction")
        closed_surviving_columns[len(survivors)] += 1

        # Check the closed identity term-by-term rather than inferring it
        # from the ambient equality.
        closed = {
            row: coefficient for row, coefficient in remainder.items()
            if x not in row
        }
        reconstructed = {}
        for cell_kind, reducer, multiplier, factor in survivors:
            add_scaled(
                reconstructed,
                basis_polynomial(cell_kind, reducer, local),
                factor,
                multiplier,
            )
        reconstructed = {
            row: coefficient for row, coefficient in reconstructed.items()
            if x not in row
        }
        require(reconstructed == closed,
                "a source-labelled closed contraction failed")

        # On x!=0 divide by the full repeated pivot power.  The pivot then
        # has no repeated decorated coordinate, so the local collision
        # excess drops from one to zero.
        localized_pivot = remove_copies(lead, x, 2)
        require(len(localized_pivot) == len(set(localized_pivot)),
                "an open Laurent pivot retained a collision")
        localized_skeletons[CENSUS.skeleton_type(localized_pivot)] += 1

        # Lower normality after multiplying by x is the finite colon test;
        # squarefreeness of every lower lead then makes all x^k, k>=1,
        # equivalent at the divisibility level.
        for row in remainder:
            xrow = FIRST.multiply(bytes((x,)), row)
            if lower_divisor(xrow):
                normality_failures += 1
                break

        record = (
            pair[0].hex(), pair[1].hex(), "branch", lead.hex(),
            f"{x:02x}", len(certificate), len(survivors),
            localized_pivot.hex(),
        )
        ledger_digest.update(repr(record).encode() + b"\n")

    require(not normality_failures,
            "an open branch acquired a lower divisor after x multiplication")
    source_type_behavior = Counter(
        "+".join(sorted(values)) for values in source_type_outcomes.values()
    )
    return {
        "outcome_histogram": dict(sorted(outcome.items())),
        "squarefree_lead_skeleton_histogram": dict(sorted(
            squarefree_skeletons.items()
        )),
        "source_type_behavior_histogram": dict(sorted(
            source_type_behavior.items()
        )),
        "lower_reduction_length_histogram": dict(sorted(
            certificate_lengths.items()
        )),
        "branch_repeated_coordinate_histogram": dict(sorted(
            repeated_variables.items()
        )),
        "closed_surviving_source_column_histogram": dict(sorted(
            closed_surviving_columns.items()
        )),
        "open_localized_pivot_skeleton_histogram": dict(sorted(
            localized_skeletons.items()
        )),
        "open_positive_power_lower_normality_failures": normality_failures,
        "pair_outcome_sha256": ledger_digest.hexdigest(),
    }


def audit():
    originals, degree4, code_to_lead, degree5, words = CENSUS.build_leads()
    words = {code: D5.decode_word(code) for code in range(3 ** 8)}
    require(len(originals) == len(degree4) == 6558,
            "the original weighted layer changed")
    require(len(degree5) == 84005, "the degree-five layer changed")
    pairs45, pairs55 = enumerate_target_pairs(degree4, degree5, words)

    records = []
    for kind, pairs in (("45", pairs45), ("55", pairs55)):
        lead_types = Counter(canonical_lead_pair(kind, pair) for pair in pairs)
        source_types = Counter(
            canonical_source_label(kind, pair, degree4, degree5)
            for pair in pairs
        )
        patterns = [
            source_pattern(kind, pair, degree4, degree5, words)
            for pair in pairs
        ]
        direction_histogram = Counter(
            tuple(sorted(pattern[-1])) for pattern in patterns
        )
        fourth_corner_mixed = sum(
            len(set(words[pattern[3]])) > 1 for pattern in patterns
        )
        exact_polynomial = polynomial_audit(
            kind, pairs, originals, degree4, code_to_lead, degree5
        )
        expected_exact = {
            "45": {
                "outcome_histogram": {"branch": 5426, "squarefree": 2986},
                "lower_reduction_length_histogram": {1: 8412},
                "closed_surviving_source_column_histogram": {2: 5426},
                "squarefree_lead_skeleton_histogram": {
                    "G4e4d3-2-2-1+P2+P2": 510,
                    "G6e5d3-2-2-1-1-1+P2": 2476,
                },
                "source_type_behavior_histogram": {
                    "branch": 1819,
                    "branch+squarefree": 550,
                    "squarefree": 2428,
                },
            },
            "55": {
                "outcome_histogram": {"branch": 16564, "squarefree": 29212},
                "lower_reduction_length_histogram": {
                    0: 30239, 1: 12627, 2: 2910,
                },
                "closed_surviving_source_column_histogram": {1: 16564},
                "squarefree_lead_skeleton_histogram": {
                    "G4e4d3-2-2-1+P2+P2": 14259,
                    "G6e5d3-2-2-1-1-1+P2": 8663,
                    "multi[2,1,1,1,1]:P4+P2+P2": 6290,
                },
                "source_type_behavior_histogram": {
                    "branch": 8371,
                    "branch+squarefree": 4950,
                    "squarefree": 23232,
                },
            },
        }[kind]
        for field, expected in expected_exact.items():
            require(exact_polynomial[field] == expected,
                    f"the exact {kind} {field} changed")
        require(exact_polynomial[
                    "open_localized_pivot_skeleton_histogram"
                ] == {"P3+P2+P2+P1": expected_exact[
                    "outcome_histogram"
                ]["branch"]},
                f"the exact {kind} Laurent skeleton changed")
        require(not exact_polynomial[
                    "open_positive_power_lower_normality_failures"
                ], f"the exact {kind} colon audit failed")
        records.append({
            "kind": kind,
            "labelled_pairs": len(pairs),
            "selected_stabilizer_lead_types": len(lead_types),
            "selected_stabilizer_lead_multiplicity_histogram": (
                multiplicity_histogram(lead_types)
            ),
            "selected_stabilizer_source_types": len(source_types),
            "selected_stabilizer_source_multiplicity_histogram": (
                multiplicity_histogram(source_types)
            ),
            "source_square_patterns": len(patterns),
            "source_direction_pair_histogram": {
                ",".join(map(str, key)): value
                for key, value in sorted(direction_histogram.items())
            },
            "fourth_corner_mixed": fourth_corner_mixed,
            "fourth_corner_pure": len(patterns) - fourth_corner_mixed,
            "exact_polynomial_audit": exact_polynomial,
        })

    ledger = {
        "complete_lower_basis": {"degree4": 6558, "degree5": 84005},
        "records": records,
        "scope_guard": (
            "this is the complete labelled-pair audit of the two frozen "
            "coarse signatures; it makes no claim about other degree-six "
            "classes or later Buchberger layers"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return ledger, digest


def main():
    ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                "the branch-class uniformity ledger changed")
    print("n=8 chart26 branch-class refinement: PASS")
    print(json.dumps(ledger, sort_keys=True))
    print("sha256:", digest)


if __name__ == "__main__":
    main()
