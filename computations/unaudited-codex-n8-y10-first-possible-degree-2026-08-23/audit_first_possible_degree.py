#!/usr/bin/env python3
"""Audit the first filtration slice that can reach the frozen y10*t2 row.

This is a structural incidence audit, not a degree-eight membership solve.
The normalized chart records only off-support variables y; a term of encoded
length r in a total-degree-four source generator carries t^(4-r).
"""

from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / "computations/verify_n8_chart26_weighted_degree6_census.py"
D7_RESULT = (
    ROOT / "computations/unaudited-codex-n8-orbit26-direct-target-2026-08-23"
    / "results_y10_d7_staged_blocks.json"
)
TARGET = bytes.fromhex("0111202020494f4f50f8")
EXPECTED_LOGICAL_SHA256 = (
    "5f010bd72d286423464cefe6b8c78bee6f212167b52827f6f29372eaef1a5c12"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_source():
    spec = importlib.util.spec_from_file_location("n8_d8_structural_source", SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def divisors(row, degree):
    return {
        bytes(row[index] for index in positions)
        for positions in combinations(range(len(row)), degree)
    }


def quotient(dividend, divisor):
    answer = list(dividend)
    for value in divisor:
        if value not in answer:
            return None
        answer.remove(value)
    return bytes(answer)


def site_support(row, coordinates):
    answer = set()
    for value in row:
        i, j, _a, _b = coordinates[value]
        answer.update((i, j))
    return answer


def make_term_sources(originals):
    answer = defaultdict(list)
    for code, polynomial in originals.items():
        for term in polynomial:
            answer[term].append(code)
    return answer


def direct_columns(term_sources, total_degree, y_degree):
    """Return source columns having a term equal to a target divisor.

    A column is g_code times a homogeneous multiplier of total degree D-4.
    Its encoded multiplier is forced to q/term.  The omitted multiplier
    t-exponent is nonnegative exactly when len(q/term) <= D-4.
    """
    candidates = divisors(TARGET, y_degree)
    columns = defaultdict(set)
    term_witnesses = defaultdict(set)
    minimum_term_degree = max(0, y_degree - (total_degree - 4))
    for q in candidates:
        for term_degree in range(minimum_term_degree, min(4, y_degree) + 1):
            for term in divisors(q, term_degree):
                multiplier = quotient(q, term)
                if len(multiplier) > total_degree - 4:
                    continue
                for code in term_sources.get(term, ()):
                    key = (code, multiplier)
                    columns[q].add(key)
                    term_witnesses[(q, key)].add(term)
    return candidates, columns, term_witnesses


def record_slice(term_sources, coordinates, total_degree, y_degree):
    candidates, columns, witnesses = direct_columns(
        term_sources, total_degree, y_degree
    )
    keys = {key for values in columns.values() for key in values}
    primitive_keys = {
        key for key in keys if len(key[1]) == total_degree - 4
    }
    first = None
    if columns:
        q = min(columns)
        key = min(columns[q])
        term = min(witnesses[(q, key)])
        first = {
            "divisor": q.hex(),
            "code": key[0],
            "multiplier_y": key[1].hex(),
            "source_term_y": term.hex(),
            "source_term_t_exponent": 4 - len(term),
            "source_term_missing_sites": sorted(
                set(range(8)) - site_support(term, coordinates)
            ),
        }
    return {
        "total_degree": total_degree,
        "y_degree": y_degree,
        "t_exponent": total_degree - y_degree,
        "target_divisors": len(candidates),
        "touched_target_divisors": len(columns),
        "direct_source_columns": len(keys),
        "primitive_t_free_multiplier_columns": len(primitive_keys),
        "source_term_y_degree_histogram": dict(sorted(Counter(
            len(term)
            for q, values in columns.items()
            for key in values
            for term in witnesses[(q, key)]
        ).items())),
        "lex_first_witness": first,
    }, columns, witnesses


def matching_edges(row, coordinates):
    edges = {coordinates[value][:2] for value in row}
    require(len(row) == 4 and len(edges) == 4,
            "a top source term stopped being a physical perfect matching")
    require(len(site_support(row, coordinates)) == 8,
            "a top source term stopped covering all eight sites")
    return edges


def exchange_type(left, right, coordinates):
    first = matching_edges(left, coordinates)
    second = matching_edges(right, coordinates)
    if first == second:
        return "same-physical-matching-decoration"
    shared = len(first & second)
    if shared == 2:
        return "C4"
    if shared == 1:
        return "C6"
    if shared == 0:
        union = first | second
        adjacency = defaultdict(set)
        for a, b in union:
            adjacency[a].add(b)
            adjacency[b].add(a)
        seed = min(adjacency)
        seen = {seed}
        pending = [seed]
        while pending:
            vertex = pending.pop()
            for neighbor in adjacency[vertex]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    pending.append(neighbor)
        return "C8" if len(seen) == 8 else "C4+C4"
    raise RuntimeError("distinct perfect matchings shared three physical edges")


def classify_d8_primitive_seeds(originals, term_sources, coordinates,
                                 slice_data):
    top_sources = {
        term: tuple(codes) for term, codes in term_sources.items()
        if len(term) == 4
    }

    def summarize(primitive):
        top_rows = set()
        seed_top_pairs = set()
        for key in primitive:
            code, multiplier = key
            for term in originals[code]:
                if len(term) == 4:
                    row = bytes(sorted(term + multiplier))
                    top_rows.add(row)
                    seed_top_pairs.add((row, term))

        factorization_histogram = Counter()
        exchange_histogram = Counter()
        multi_factor_rows = 0
        forced_site5_failures = 0
        for row in top_rows:
            factorizations = []
            for term in divisors(row, 4):
                if term not in top_sources:
                    continue
                multiplier = quotient(row, term)
                for code in top_sources[term]:
                    factorizations.append((code, multiplier, term))
            factorizations = sorted(set(factorizations))
            factorization_histogram[len(factorizations)] += 1
            if len(factorizations) > 1:
                multi_factor_rows += 1
            site5_cells = [
                value for value in row if 5 in coordinates[value][:2]
            ]
            if len(site5_cells) != 1:
                forced_site5_failures += 1
            for first_index, first in enumerate(factorizations):
                for second in factorizations[first_index + 1:]:
                    exchange_histogram[
                        exchange_type(first[2], second[2], coordinates)
                    ] += 1

        return {
            "primitive_columns": len(primitive),
            "top_rows": len(top_rows),
            "seed_top_incidence_pairs": len(seed_top_pairs),
            "top_factorization_count_histogram": dict(sorted(
                factorization_histogram.items()
            )),
            "top_rows_with_multiple_factorizations": multi_factor_rows,
            "pair_exchange_type_histogram": dict(sorted(
                exchange_histogram.items()
            )),
            "rows_not_having_unique_site5_cell": forced_site5_failures,
        }

    by_slice = {}
    primitive_all = set()
    for (degree, y_degree), (_record, columns, _witnesses) in slice_data.items():
        if degree != 8:
            continue
        primitive = {
            key for values in columns.values() for key in values
            if len(key[1]) == 4
        }
        primitive_all.update(primitive)
        by_slice[f"y{y_degree}*t{degree - y_degree}"] = summarize(primitive)
    return {"all": summarize(primitive_all), "by_slice": by_slice}


def audit():
    source = load_source()
    originals, _leads = source.FIRST.original_basis()
    term_sources = make_term_sources(originals)
    coordinates = source.D5.COORDINATES
    d7 = json.loads(D7_RESULT.read_text())
    require(d7["status"] == "EXACT_TARGET_STANDARD_THROUGH_TOTAL_D7",
            "the frozen degree-seven terminal changed")
    require(d7["new_head_kernel_dimension"] == 0,
            "the frozen degree-seven head is no longer injective")

    slice_data = {
        (degree, y_degree): record_slice(
            term_sources, coordinates, degree, y_degree
        )
        for degree in (7, 8)
        for y_degree in range(degree - 2, degree + 1)
    }
    slices = [slice_data[key][0] for key in sorted(slice_data)]
    lookup = {(item["total_degree"], item["y_degree"]): item for item in slices}

    # Missing site 5 forbids every t-free target divisor at every degree:
    # a y^4 source term is a full physical perfect matching and hence uses 5.
    require(lookup[(7, 7)]["direct_source_columns"] == 0,
            "a t-free d7 column reached a divisor missing site 5")
    require(lookup[(8, 8)]["direct_source_columns"] == 0,
            "a t-free d8 column reached a divisor missing site 5")

    first_d7 = lookup[(7, 6)]["lex_first_witness"]
    require(first_d7 == {
        "divisor": "0111202049f8",
        "code": 2327,
        "multiplier_y": "011120",
        "source_term_y": "2049f8",
        "source_term_t_exponent": 1,
        "source_term_missing_sites": [2, 5],
    }, "the canonical d7 one-t provider changed")

    first_d8 = lookup[(8, 7)]["lex_first_witness"]
    require(first_d8 == {
        "divisor": "011120202049f8",
        "code": 2327,
        "multiplier_y": "01112020",
        "source_term_y": "2049f8",
        "source_term_t_exponent": 1,
        "source_term_missing_sites": [2, 5],
    }, "the canonical d8 one-t provider changed")

    d8_seed_exchange = classify_d8_primitive_seeds(
        originals, term_sources, coordinates, slice_data
    )
    require(d8_seed_exchange["all"]["primitive_columns"] == 205,
            "the frozen 205 primitive d8 seed census changed")
    require(d8_seed_exchange["all"]["rows_not_having_unique_site5_cell"] == 0,
            "a d8 target seed lost the forced site-5 source cell")
    require(not ({"C8", "C4+C4"} & set(
        d8_seed_exchange["all"]["pair_exchange_type_histogram"]
    )), "a forbidden no-shared-edge exchange reached a target seed")

    theorem = (
        "The target misses physical site 5, so no t-free source term can "
        "divide any target divisor: every y4 term is a full perfect matching. "
        "A one-t divisor can first be reached by a y3*t source term whose "
        "omitted normalized support edge contains site 5. Degree 7 has these "
        "raw incidences, but its exact target-rooted y7 head is injective and "
        "all lower slices are t multiples of degree 6. At degree 8 the new "
        "primitive slice is y7*t: y3*t source terms times y4 multipliers. "
        "Degree 8 is also the first universal top-syzygy degree, because two "
        "degree-4 top forms have their Koszul relation there. Its first "
        "Bockstein can therefore land in y7*t. Among the 205 primitive d8 "
        "target seeds, the missing site forces every top row to reuse one "
        "site-5 cell, excluding C8 and C4+C4 matching exchange; the physical "
        "exchange types are C4/C6, besides decoration-only swaps. This "
        "predicts y7*t, not y8 or y6*t2, as the first slice requiring a "
        "genuinely new kernel test."
    )
    payload = {
        "format": "n8-y10-first-possible-degree-v1",
        "target": TARGET.hex(),
        "target_total_degree": 12,
        "target_t_exponent": 2,
        "d7_terminal_logical_sha256": d7["logical_sha256"],
        "d7_result_sha256": sha256(D7_RESULT.read_bytes()).hexdigest(),
        "slices": slices,
        "d8_primitive_seed_exchange": d8_seed_exchange,
        "first_possible_new_degree": 8,
        "predicted_first_new_slice": "y7*t",
        "prediction_scope": (
            "structural incidence and first universal top-syzygy degree; "
            "not a degree-eight rank or membership result"
        ),
        "theorem": theorem,
    }
    logical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["logical_sha256"] = sha256(logical.encode()).hexdigest()
    require(payload["logical_sha256"] == EXPECTED_LOGICAL_SHA256,
            "the first-possible-degree structural ledger changed")
    return payload


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
