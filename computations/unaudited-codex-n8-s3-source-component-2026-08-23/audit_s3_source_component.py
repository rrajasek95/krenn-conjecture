#!/usr/bin/env python3
"""Audit the universal cubic S3 against literal chart-26 source cells.

There are two finite tests.

* Classify the 66 S3 monomials by physical and site-colour-port skeleton and
  locate their literal cubic occurrences in the 6,558 mixed generators.
* In homogeneous total degree five, build exactly the degree-at-most-three
  connected component of every t*g and x*g source column meeting the 52
  nonliteral S3 rows.  This lower projection is a necessary condition for a
  source reduction, so an exact dual here is a valid obstruction to every
  degree-five reduction.  No higher residual or broad Groebner solve enters.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from math import gcd
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DIRECT = ROOT / "computations/unaudited-codex-n8-orbit26-direct-target-2026-08-23"
KERNEL = DIRECT / "direct_fh_transfer_kernels.txt"
PHYSICAL = DIRECT / "s3_physical_skeleton.txt"
SOURCE_CLOSURE = DIRECT / "s3_source_closure.txt"
NORMALIZED = ROOT / "computations/verify_n8_normalized_critical_contraction.py"
COMPLETE_D5 = ROOT / "computations/verify_n8_chart26_complete_degree5_buchberger.py"
PATH_FOREST = ROOT / "computations/verify_n8_chart26_path_forest_skeleton.py"
POLARIZED = ROOT / "computations/verify_n8_one_bad_multiplicity_polarized_grade_split.py"
RESULT_PATH = HERE / "results_s3_source_component.json"
EXPECTED = {
    KERNEL: "859f144440e45ca64c1534ae99506e31524d76cd3c47e83911b384c2fea49650",
    PHYSICAL: "f6757cbe3d03c3049e5e12be48eca14888abbecd4a275610d02ee34d2fbba4d1",
    SOURCE_CLOSURE: "3fe8db467ea28ff6afdd04384b5fb65c5cf8dfe2a2b49b69cf0129c8f5ab25e1",
    NORMALIZED: "4e2ce4b12626edaedd9a8a5a4a9635ab5c74a5f139ecf52507018ca5478acd62",
    COMPLETE_D5: "3d96ec2b26781b70e5cac1878d7090e525c135e285815f9fecb48fca88bd7e30",
    PATH_FOREST: "121b5b27bd41ce40a06613b644a0e7fe39284808abf3fba248a87d04bf074e30",
    POLARIZED: "f3df3eb8b19d0fdfef4417b8c050a3653107b1a0675575ab295cdba41d03328a",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_normalized():
    spec = importlib.util.spec_from_file_location("s3_normalized", NORMALIZED)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, "cannot load normalized chart module")
    spec.loader.exec_module(module)
    return module


def parse_kernel(label):
    active = False
    answer = {}
    for line in KERNEL.read_text(encoding="ascii").splitlines():
        fields = line.split()
        if fields[:2] == ["BEGIN", label]:
            active = True
        elif fields[:2] == ["END", label]:
            active = False
        elif active and fields[0] == "ROW":
            answer[bytes.fromhex(fields[1])] = int(fields[2])
    return answer


def normalized_polynomials(D5):
    answer = {}
    for code in range(3 ** 8):
        if len(set(D5.decode_word(code))) == 1:
            continue
        polynomial = Counter()
        for literal in D5.iter_word_terms(code):
            row = bytes(sorted(x for x in literal if D5.IS_OFF_SUPPORT[x]))
            polynomial[row] += 1
        answer[code] = dict(polynomial)
    require(len(answer) == 6558, "mixed generator census changed")
    return answer


def skeleton(row, D5):
    site_degree = Counter()
    port_degree = Counter()
    physical_edges = []
    for identifier in row:
        left, right, a, b = D5.COORDINATES[identifier]
        physical_edges.append(tuple(sorted((left, right))))
        site_degree.update((left, right))
        port_degree.update((3 * left + a, 3 * right + b))
    site_profile = tuple(sorted(site_degree.values(), reverse=True))
    if site_profile == (1, 1, 1, 1, 1, 1):
        physical_type = "3P2"
    elif site_profile == (2, 1, 1, 1, 1):
        physical_type = "P3+P2"
    elif site_profile == (2, 2, 1, 1):
        physical_type = "P4"
    else:
        physical_type = "other"
    return {
        "physical_type": physical_type,
        "physical_edges": tuple(sorted(physical_edges)),
        "site_profile": site_profile,
        "port_profile": tuple(sorted(port_degree.values(), reverse=True)),
        "decorated_squarefree": len(row) == len(set(row)),
    }


def build_low_component(target, polynomials):
    """Connected low projection of total-degree-five raw source columns.

    key (code,-1) is t*g; key (code,x) is x*g.  At y-degree <=3,
    t*g retains base rows of degree <=3, while x*g retains base rows of
    degree <=2 and adjoins x.  Inverse deletion enumerates every incident
    column without scanning all 6,558*241 possibilities.
    """
    term_sources = defaultdict(list)
    for code, polynomial in polynomials.items():
        for row in polynomial:
            if len(row) <= 3:
                term_sources[row].append(code)

    rows = set(target)
    queue = deque(sorted(target))
    columns = {}
    while queue:
        row = queue.popleft()
        for code in term_sources.get(row, ()):
            key = (code, -1)
            if key in columns:
                continue
            column = {item: coefficient
                      for item, coefficient in polynomials[code].items()
                      if len(item) <= 3}
            columns[key] = column
            for item in column:
                if item not in rows:
                    rows.add(item)
                    queue.append(item)
        for position, variable in enumerate(row):
            base = row[:position] + row[position + 1:]
            for code in term_sources.get(base, ()):
                key = (code, variable)
                if key in columns:
                    continue
                column = Counter()
                for item, coefficient in polynomials[code].items():
                    if len(item) <= 2:
                        column[bytes(sorted(item + bytes([variable])))] += coefficient
                columns[key] = {item: coefficient for item, coefficient in column.items()
                                if coefficient}
                for item in columns[key]:
                    if item not in rows:
                        rows.add(item)
                        queue.append(item)
    return tuple(sorted(rows)), {key: columns[key] for key in sorted(columns)}


def modular_rank(rows, columns, prime):
    row_index = {row: index for index, row in enumerate(rows)}
    pivots = {}

    def reduce(vector):
        vector = {index: coefficient % prime
                  for index, coefficient in vector.items()
                  if coefficient % prime}
        while vector:
            pivot = min(vector)
            if pivot not in pivots:
                return vector
            scale = vector[pivot]
            for index, coefficient in pivots[pivot].items():
                value = (vector.get(index, 0) - scale * coefficient) % prime
                if value:
                    vector[index] = value
                else:
                    vector.pop(index, None)
        return vector

    for column in columns.values():
        vector = reduce({row_index[row]: coefficient
                         for row, coefficient in column.items()})
        if vector:
            pivot = min(vector)
            inverse = pow(vector[pivot], prime - 2, prime)
            pivots[pivot] = {index: coefficient * inverse % prime
                             for index, coefficient in vector.items()}
    return len(pivots)


def stopping_set_census(rows, columns, target):
    row_index = {row: index for index, row in enumerate(rows)}
    column_items = list(columns.items())
    column_rows = [set(row_index[row] for row in column) for _key, column in column_items]
    row_columns = [[] for _row in rows]
    for column_index, support in enumerate(column_rows):
        for index in support:
            row_columns[index].append(column_index)
    target_index = {row_index[row]: coefficient for row, coefficient in target.items()}

    def rank_mod(matrix, prime=1009):
        matrix = [[value % prime for value in row] for row in matrix
                  if any(value % prime for value in row)]
        if not matrix:
            return 0
        rank = 0
        width = len(matrix[0])
        for column in range(width):
            chosen = next((index for index in range(rank, len(matrix))
                           if matrix[index][column]), None)
            if chosen is None:
                continue
            matrix[rank], matrix[chosen] = matrix[chosen], matrix[rank]
            inverse = pow(matrix[rank][column], prime - 2, prime)
            matrix[rank] = [value * inverse % prime for value in matrix[rank]]
            for index in range(len(matrix)):
                if index == rank or not matrix[index][column]:
                    continue
                scale = matrix[index][column]
                matrix[index] = [
                    (left - scale * right) % prime
                    for left, right in zip(matrix[index], matrix[rank])
                ]
            rank += 1
        return rank

    frontier = {frozenset((index,)) for index in target_index}
    visited = set(frontier)
    census = []
    separating = []
    for size in range(1, 4):
        next_frontier = set()
        terminal = []
        for support in frontier:
            bad = []
            for row in support:
                for column in row_columns[row]:
                    if len(column_rows[column] & support) == 1:
                        bad.append((len(column_rows[column]), column))
            if not bad:
                terminal.append(support)
            elif size < 3:
                _width, column = min(bad)
                for other in column_rows[column] - support:
                    enlarged = support | {other}
                    if enlarged not in visited:
                        visited.add(enlarged)
                        next_frontier.add(enlarged)
        separating_at_size = []
        for support in terminal:
            selected = sorted(support)
            incident = sorted({column for row in support for column in row_columns[row]})
            matrix = [
                [column_items[column][1].get(rows[row], 0) for row in selected]
                for column in incident
            ]
            rank = rank_mod(matrix)
            target_row = [target_index.get(row, 0) for row in selected]
            augmented_rank = rank_mod(matrix + [target_row])
            if rank < len(selected) and augmented_rank > rank:
                separating_at_size.append(support)
        separating.extend(separating_at_size)
        census.append({
            "support_size": size,
            "frontier_sets": len(frontier),
            "stopping_sets": len(terminal),
            "separating_sets": len(separating_at_size),
        })
        if separating:
            break
        frontier = next_frontier
    require(census == [
        {"support_size": 1, "frontier_sets": 52,
         "stopping_sets": 0, "separating_sets": 0},
        {"support_size": 2, "frontier_sets": 238,
         "stopping_sets": 13, "separating_sets": 0},
        {"support_size": 3, "frontier_sets": 1500,
         "stopping_sets": 72, "separating_sets": 28},
    ], "minimal stopping/separator census changed")
    return census, separating, row_index


def audit(mutate=False):
    for path, digest in EXPECTED.items():
        require(sha256(path.read_bytes()).hexdigest() == digest,
                f"source drift: {path}")
    NORM = load_normalized()
    D5 = NORM.D5
    s3 = parse_kernel("S3")
    h3 = parse_kernel("H3")
    require(len(s3) == 66 and Counter(s3.values()) == Counter({1: 53, -1: 13}),
            "S3 profile changed")
    polynomials = normalized_polynomials(D5)

    physical = {row: skeleton(row, D5) for row in s3}
    physical_histogram = Counter(item["physical_type"] for item in physical.values())
    require(physical_histogram == Counter({"3P2": 28, "P3+P2": 28, "P4": 10}),
            "S3 physical skeleton split changed")
    require(all(item["port_profile"] == (1, 1, 1, 1, 1, 1)
                and item["decorated_squarefree"] for item in physical.values()),
            "S3 stopped being a matching on six distinct site-colour ports")

    cubic_sources = defaultdict(list)
    degree_by_code = {}
    for code, polynomial in polynomials.items():
        degree_by_code[code] = min(map(len, polynomial))
        for row in polynomial:
            if len(row) == 3:
                cubic_sources[row].append(code)
    literal = {row: s3[row] for row in s3 if cubic_sources.get(row)}
    residual = {row: coefficient for row, coefficient in s3.items()
                if row not in literal}
    require(len(literal) == 14 and len(residual) == 52
            and set(code for row in literal for code in cubic_sources[row]) == {3780}
            and all(degree_by_code[code] == 0
                    for row in literal for code in cubic_sources[row]),
            "literal/nonliteral S3 partition changed")
    require(not any(degree_by_code[code] in (2, 3)
                    for row in s3 for code in cubic_sources.get(row, ())),
            "an S3 row entered an N4 or N6 leading source fibre")

    matching = {row for row, item in physical.items() if item["physical_type"] == "3P2"}
    matching_literal = matching & set(literal)
    matching_nonliteral = matching - set(literal)
    collision = set(s3) - matching
    require((len(matching_literal), len(matching_nonliteral), len(collision)) == (14, 14, 38),
            "matching/collision split changed")

    rows, columns = build_low_component(residual, polynomials)
    require((len(rows), len(columns)) == (1311, 330),
            "degree-five low component changed")
    support_histogram = Counter(len(column) for column in columns.values())
    require(support_histogram == Counter({7: 328, 45: 2}),
            "low-column support histogram changed")
    ranks = {prime: modular_rank(rows, columns, prime) for prime in (1009, 1013)}
    require(ranks == {1009: 330, 1013: 330},
            "low-component rank changed")

    # The lexicographically selected exact minimal separator.  Its only two
    # incident raw source columns give equations lambda_1+lambda_2=0 and
    # lambda_0+lambda_2=0.
    dual = {
        bytes.fromhex("0c4fcc"): 1,
        bytes.fromhex("1557a7"): 1,
        bytes.fromhex("3072a7"): -1,
    }
    if mutate:
        dual[bytes.fromhex("1557a7")] = 2
    incident = {}
    for key, column in columns.items():
        pairing = sum(dual.get(row, 0) * coefficient
                      for row, coefficient in column.items())
        if set(column) & set(dual):
            incident[key] = {
                "rows": [[row.hex(), column[row]]
                         for row in sorted(set(column) & set(dual))],
                "pairing": pairing,
            }
        require(pairing == 0, f"dual does not annihilate source column {key}")
    target_pairing = sum(dual.get(row, 0) * coefficient
                         for row, coefficient in residual.items())
    require(target_pairing == 1, "dual stopped separating residual52")
    require(incident == {
        (3645, 167): {"rows": [["1557a7", 1], ["3072a7", 1]], "pairing": 0},
        (3780, -1): {"rows": [["0c4fcc", 1], ["3072a7", 1]], "pairing": 0},
    }, "minimal dual incidence changed")

    stopping_census, separating, row_index = stopping_set_census(
        rows, columns, residual
    )
    chosen_indices = frozenset(row_index[row] for row in dual)
    require(chosen_indices in separating, "chosen exact support left minimal separator census")

    result = {
        "format": "n8-S3-source-component-v1",
        "status": "EXACT_NONLITERAL_CUBIC_OBSTRUCTION",
        "source_sha256": {str(path.relative_to(ROOT)): digest
                          for path, digest in EXPECTED.items()},
        "S3_partition": {
            "rows": len(s3),
            "physical_skeleton_histogram": dict(sorted(physical_histogram.items())),
            "site_colour_port_matchings": len(s3),
            "literal_mixed_cubic_rows": len(literal),
            "literal_source_code": 3780,
            "literal_source_word": "12012000",
            "literal_source_minimum_y_degree": 0,
            "nonliteral_matching_rows": len(matching_nonliteral),
            "physical_collision_rows": len(collision),
            "residual_nonliteral_rows": len(residual),
            "N4_degree2_leading_fibre_hits": 0,
            "N6_degree3_leading_fibre_hits": 0,
            "H3_intersection": len(set(s3) & set(h3)),
        },
        "degree5_low_source_component": {
            "definition": (
                "y-degree<=3 projection of every total-degree5 raw mixed-source "
                "column t*g and x*g connected to residual52"
            ),
            "rows": len(rows),
            "columns": len(columns),
            "column_support_histogram": dict(sorted(support_histogram.items())),
            "rank_mod_primes": ranks,
            "Q_rank": len(columns),
            "residual52_membership": False,
            "reason_full_degree5_cells_are_covered": (
                "every complete degree5 Buchberger cell is a difference of the "
                "raw x*g columns annihilated here"
            ),
        },
        "minimal_exact_dual": {
            "support": [[row.hex(), coefficient] for row, coefficient in sorted(dual.items())],
            "support_size": len(dual),
            "target_pairing": target_pairing,
            "incident_source_columns": [
                {"code": key[0], "multiplier": "t" if key[1] == -1 else key[1],
                 **value}
                for key, value in sorted(incident.items())
            ],
            "minimality_census": stopping_census,
            "proof_of_minimality": (
                "a nonzero dual support must be a stopping set in the source "
                "incidence hypergraph; all size1/2 stopping supports meeting "
                "residual52 were enumerated and none separates"
            ),
        },
        "path_forest_comparison": {
            "physical_path_forest_match": False,
            "reason": (
                "the archived Buchberger leads are spanning physical forests "
                "P4+P2+P2 (then P6+P2/P4+P4), whereas the 38 collision rows "
                "are nonspanning P3+P2 or P4 triples"
            ),
            "repeated_decorated_coordinate_rows": 0,
            "port_polarized_interpretation": (
                "all 38 collision rows become ordinary three-edge matchings on "
                "six distinct site-colour ports; polarization erases precisely "
                "the physical-site collision"
            ),
            "diagonal_Tor_verdict": (
                "exact first diagonal-Tor signature and cubic truncated dual, "
                "not yet an identification with the archived higher Bockstein class"
            ),
        },
        "scope": (
            "exact cubic and homogeneous-degree5 lower projection only; it does "
            "not decide S4, the full y10 circuit, or all-order t-saturation"
        ),
    }
    result["logical_sha256"] = sha256(json.dumps(
        result, sort_keys=True, separators=(",", ":")
    ).encode("ascii")).hexdigest()
    return json.loads(json.dumps(result))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    parser.add_argument("--mutate", action="store_true")
    args = parser.parse_args()
    result = audit(args.mutate)
    if args.write_results:
        RESULT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    if args.check_results:
        require(RESULT_PATH.exists() and json.loads(RESULT_PATH.read_text()) == result,
                "stored result changed")
    print(result["status"])
    print("S3 literal/residual/collision=", 14, 52, 38)
    print("low component rows/columns/rank=", 1311, 330,
          result["degree5_low_source_component"]["Q_rank"])
    print("minimal dual/pairing=", 3,
          result["minimal_exact_dual"]["target_pairing"])
    print("logical", result["logical_sha256"])


if __name__ == "__main__":
    main()
