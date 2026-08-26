#!/usr/bin/env python3
"""Find and freeze exact two-rescue determinants for Hall shapes 220/211."""

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "results_tail_polar_source_lift.json"
COVER = HERE / "results_332_rescue_orbit_cover.json"
OUT = HERE / "results_332_two_rescue_thetas.json"
SEEDS = ("F_01001212", "F_01100212")
REPRESENTATIVES = {
    "Theta_220": (0, 1, 2, 3),
    "Theta_211": (0, 1, 2, 4),
}
EXPECTED_DELTA_PAIR = {"Theta_220": (2, 3), "Theta_211": (2, 4)}


def require(value, detail):
    if not value:
        raise RuntimeError(detail)


def logical_hash(value):
    return sha256(json.dumps(value, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def vertex_actions():
    for block_permutation in permutations(range(3)):
        for flips in product((0, 1), repeat=4):
            mapping = {}
            for vertex in range(8):
                block, clone = divmod(vertex, 2)
                image_block = (block_permutation[block]
                               if block < 3 else 3)
                mapping[vertex] = 2*image_block + (clone ^ flips[block])
            yield mapping


def transform_label(label, action):
    old = label.removeprefix("F_")
    new = [None]*8
    for vertex, colour in enumerate(old):
        new[action[vertex]] = colour
    return "F_"+"".join(new)


def sign(permutation):
    inversions = sum(permutation[i] > permutation[j]
                     for i in range(len(permutation))
                     for j in range(i+1, len(permutation)))
    return -1 if inversions % 2 else 1


def formal_determinant(matrix, columns):
    answer = Counter()
    for permutation in permutations(columns):
        terms = []
        coefficient = sign(tuple(columns.index(value) for value in permutation))
        for row, column in zip(matrix, permutation):
            if column not in row:
                break
            row_coefficient, factors = row[column]
            coefficient *= row_coefficient
            terms.extend(factors)
        else:
            answer[tuple(sorted(terms))] += coefficient
    return Counter({monomial: coefficient for monomial, coefficient
                    in answer.items() if coefficient})


def formal_determinant_dp(matrix, columns):
    """Exact sparse determinant in O(n 2^n) polynomial-state steps."""
    index = {column: position for position, column in enumerate(columns)}
    states = {0: Counter({(): 1})}
    for row in matrix:
        updated = {}
        for mask, polynomial in states.items():
            for column, (entry_coefficient, entry_factors) in row.items():
                position = index[column]
                bit = 1 << position
                if mask & bit:
                    continue
                inversions = (mask >> (position+1)).bit_count()
                coefficient = entry_coefficient*(-1 if inversions % 2 else 1)
                target = updated.setdefault(mask | bit, Counter())
                for monomial, value in polynomial.items():
                    target[tuple(sorted(monomial+entry_factors))] += (
                        coefficient*value)
        states = {mask: Counter({monomial: coefficient
                                 for monomial, coefficient in polynomial.items()
                                 if coefficient})
                  for mask, polynomial in updated.items()}
    answer = states.get((1 << len(columns))-1, Counter())
    return Counter({monomial: coefficient for monomial, coefficient
                    in answer.items() if coefficient})


def rescue_row(record, sites, reduced):
    answer = {}
    for column, coefficient in record["nonzero_columns"].items():
        site = int(column[1:])
        if site not in sites:
            continue
        factors = tuple(coefficient.split("*"))
        if reduced:
            if column[0] == "y":
                answer[site] = (1, factors+(f"V{site}",))
            else:
                answer[site] = (-1, factors+(f"U{site}",))
        else:
            answer[column] = (1, factors)
    return answer


def reduced_matrix(sites, rescue_records):
    matrix = [
        {site: (1, (f"P{site}", f"V{site}")) for site in sites},
        {site: (-1, (f"Q{site}", f"U{site}")) for site in sites},
    ]
    matrix.extend(rescue_row(record, sites, True)
                  for record in rescue_records)
    return matrix


def full_matrix(sites, rescue_records):
    y = tuple(f"y{site}" for site in sites)
    z = tuple(f"z{site}" for site in sites)
    matrix = [
        {column: (1, (f"P{int(column[1:])}",)) for column in y},
        {column: (1, (f"Q{int(column[1:])}",)) for column in z},
    ]
    for site in sites:
        matrix.append({f"y{site}": (1, (f"U{site}",)),
                       f"z{site}": (1, (f"V{site}",))})
    matrix.extend(rescue_row(record, sites, False)
                  for record in rescue_records)
    return matrix, y+z


def common_monomial(polynomial):
    counters = [Counter(monomial) for monomial in polynomial]
    common = counters[0].copy()
    for counter in counters[1:]:
        common &= counter
    factors = tuple(sorted(common.elements()))
    residual = Counter()
    for monomial, coefficient in polynomial.items():
        value = list(monomial)
        for factor in factors:
            value.remove(factor)
        residual[tuple(value)] += coefficient
    return factors, residual


def encode(polynomial):
    return [
        {"coefficient": coefficient, "factors": list(monomial)}
        for monomial, coefficient in sorted(polynomial.items())
    ]


def delta_atoms(left, right):
    return Counter({
        tuple(sorted((f"P{left}", f"Q{right}",
                      f"V{left}", f"U{right}"))): 1,
        tuple(sorted((f"P{right}", f"Q{left}",
                      f"U{left}", f"V{right}"))): -1,
    })


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    source = json.loads(SOURCE.read_text())
    cover = json.loads(COVER.read_text())
    require(cover["minimal_uncovered_containment_antichain"] == [
        {"double_block_shape": [2, 2, 0],
         "double_sites": [0, 1, 2, 3], "minimal_new_factor": "Theta_220"},
        {"double_block_shape": [2, 1, 1],
         "double_sites": [0, 1, 2, 4], "minimal_new_factor": "Theta_211"},
    ], "uncovered antichain changed")
    rows = {row["source_label"]: row for row in source["row_ledger"]}
    candidates = sorted({transform_label(seed, action)
                         for seed in SEEDS for action in vertex_actions()})
    require(len(candidates) == 96 and
            all(rows[label]["profile"] == "3+3+2" for label in candidates),
            "transported rescue-row set changed")

    records = []
    for theta, sites in REPRESENTATIVES.items():
        started = time.monotonic()
        best = None
        tested = 0
        for left, right in combinations(candidates, 2):
            rescue_records = (rows[left], rows[right])
            polynomial = formal_determinant(
                reduced_matrix(sites, rescue_records), sites)
            tested += 1
            if not polynomial:
                continue
            common, residual = common_monomial(polynomial)
            score = (len(residual), len(polynomial), left, right)
            if best is None or score < best[0]:
                best = (score, (left, right), polynomial, common, residual)
                if score[0] == 1:
                    break
        elapsed = time.monotonic()-started
        require(elapsed < 120 and best is not None,
                ("two-rescue search failed/cap", theta, elapsed))
        _, labels, polynomial, common, residual = best
        delta_pair = EXPECTED_DELTA_PAIR[theta]
        expected_delta = delta_atoms(*delta_pair)
        require(residual in (expected_delta, Counter(
            {monomial: -coefficient for monomial, coefficient
             in expected_delta.items()})),
            ("primitive two-rescue factor ceased to be Delta", theta))
        selected = tuple(rows[label] for label in labels)
        full, full_columns = full_matrix(sites, selected)
        full_polynomial = formal_determinant(full, full_columns)
        require(full_polynomial in (polynomial, Counter(
            {monomial: -coefficient for monomial, coefficient
             in polynomial.items()})),
            ("Schur/Laplace reduced determinant changed", theta))
        records.append({
            "name": theta,
            "double_sites": list(sites),
            "source_labels": list(labels),
            "source_row_coefficients": {
                label: rows[label]["nonzero_columns"] for label in labels
            },
            "candidate_pairs_tested": tested,
            "symbolic_cap_seconds": 120,
            "full_minor_rows": ["Y", "Z"]+
                               [f"E{site}" for site in sites]+list(labels),
            "full_minor_columns": list(full_columns),
            "determinant_term_count": len(polynomial),
            "common_monomial_factors": list(common),
            "primitive_factor_term_count": len(residual),
            "primitive_factor_name": f"Delta_{delta_pair[0]}{delta_pair[1]}",
            "factorization": (
                "("+"*".join(common)+")*"+
                f"Delta_{delta_pair[0]}{delta_pair[1]}"
            ),
            "primitive_factor": encode(residual),
            "full_determinant": encode(polynomial),
            "literal_full_vs_reduced_replay": True,
        })

    result = {
        "status": "PASS exact source-labelled two-rescue Theta determinants",
        "transported_rescue_row_count": len(candidates),
        "determinants": records,
        "reduction_identity": (
            "For doubled sites D, pivot the E_a rows against z_a. After "
            "clearing the diagonal V_a factors, the exact remaining matrix "
            "has Y_a=P_a*V_a, Z_a=-Q_a*U_a, y-rescue r_a*V_a, and "
            "z-rescue -r_a*U_a. Direct full 8x8 determinants replay the "
            "reduced 4x4 determinants up to the audited ordering sign."
        ),
        "atom_dictionary": {
            "P_a": "h0_a6", "Q_a": "h0_a7",
            "U_a": "h1_a6", "V_a": "h1_a7",
        },
        "scope_guard": (
            "Each result is an exact literal source minor on its displayed "
            "factor open. Vanishing primitive factors are routed separately."
        ),
        "source_hashes": {
            "source": sha256(SOURCE.read_bytes()).hexdigest(),
            "cover": sha256(COVER.read_bytes()).hexdigest(),
        },
    }
    result["logical_sha256"] = logical_hash(result)
    if args.write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("two-rescue Thetas: PASS", result["logical_sha256"])
    for record in records:
        print(record["name"], record["source_labels"],
              "terms", record["determinant_term_count"],
              "primitive", record["primitive_factor_term_count"],
              "cap", record["symbolic_cap_seconds"])


if __name__ == "__main__":
    main()
