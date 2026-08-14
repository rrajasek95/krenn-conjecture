#!/usr/bin/env python3
"""Resolve the first site-repeating order-six face and its seed-family span.

The first forbidden target coordinate is

    (01:11) wedge (07:11).

Inside each of the two literal fine shifts, an exact three-operator
combination has zero order-six source and singleton Spencer boundary and a
monic value on this pair.  Its remaining D2 boundary has respectively 36
and 30 labelled pair terms.  Both cycles are nevertheless homogeneous
response-Spencer operations, not response-to-cap operations.

The strongest literal seed family consisting of every raw operator which
contains this pair has 819 columns.  Its constrained site-repeating
projection has rank 76 on 84 coordinates at both pinned primes.  Since the
complete family has rank 153 on 159 coordinates, a rank-77 quotient remains
outside the seed-containing family before any additional group/naturality
orbit is supplied.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_order6_site_repeating_target_enrichment_current_tree.py":
        "f1bc7a9f8fdb9148fde5c4d79a4b7f59a3bd03cd6ff00dc1c2fb3c0e7f511ea9",
    "computations/verify_h3_residual_q_order6_spencer_affine_feasibility.py":
        "ef9bd416986f7dc8c07ffa3b396d1c1f92237c8e1a0539ecbb0ddbeaadb1c18e",
    "computations/verify_h3_gamma_star_source_derived_free_closure_census.py":
        "a479ac8759bf7a18b43ee91d8b1ab7d0b432c48a7787b065cac68403ace3df3a",
}
EXPECTED_LEDGER_SHA256 = "534d40e41691b063fbe6cc4f9fb4ed5569b39bc3e048c90e33fb41a48de5ba94"

FIRST_PAIR = (
    (0, 1, 1, 1),
    (0, 7, 1, 1),
)
FIRST_ROW = (2, FIRST_PAIR)
EXPECTED_FULL_SUPPORT_RANK = (159, 153)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def exact_row_solution(columns, target):
    """Solve the sparse rational row system, leaving free columns zero."""
    equations = defaultdict(dict)
    for column_index, column in enumerate(columns):
        for row, value in column.items():
            if value:
                equations[row][column_index] = Q(value)
    for row in target:
        equations.setdefault(row, {})
    occurrence = Counter(column for vector in equations.values()
                         for column in vector)
    ordered_rows = sorted(equations, key=lambda row: len(equations[row]))
    basis = {}
    insertion_order = []
    for row in ordered_rows:
        vector = dict(equations[row])
        rhs = Q(target.get(row, 0))
        while True:
            old_pivots = set(vector) & set(basis)
            if not old_pivots:
                break
            pivot = min(old_pivots,
                        key=lambda column: (occurrence[column], column))
            coefficient = vector[pivot]
            basis_vector, basis_rhs = basis[pivot]
            for column, value in basis_vector.items():
                result = vector.get(column, Q(0)) - coefficient * value
                if result:
                    vector[column] = result
                else:
                    vector.pop(column, None)
            rhs -= coefficient * basis_rhs
        if not vector:
            require(not rhs, ("inconsistent exact seed equation", row))
            continue
        pivot = min(vector, key=lambda column: (occurrence[column], column))
        inverse = Q(1) / vector[pivot]
        vector = {column: inverse * value
                  for column, value in vector.items()}
        basis[pivot] = (vector, rhs * inverse)
        insertion_order.append(pivot)

    solution = {}
    for pivot in reversed(insertion_order):
        vector, rhs = basis[pivot]
        value = rhs - sum(
            (coefficient * solution.get(column, Q(0))
             for column, coefficient in vector.items() if column != pivot),
            Q(0),
        )
        if value:
            solution[pivot] = value
    reconstruction = Counter()
    for column_index, coefficient in solution.items():
        for row, value in columns[column_index].items():
            reconstruction[row] += coefficient * value
    reconstruction = Counter({row: value
                              for row, value in reconstruction.items()
                              if value})
    require(reconstruction == Counter(target),
            ("exact seed reconstruction failed", reconstruction, target))
    return solution, len(basis)


def ordered_metadata(loaded, columns, shifts):
    """Reconstruct the exact metadata order used by build_operator_columns."""
    aff = loaded["aff"]
    order6 = loaded["order6"]
    repair = loaded["repair"]
    commutator = loaded["commutator"]
    base = loaded["base"]
    system = repair.build_system(base, commutator)
    sixth = order6.build_exact_sixth_derivatives(system)
    metadata = set()
    for _product, directions in sixth:
        if not loaded["site"].MISSING.issubset(directions):
            continue
        for coefficient in order6.eligible_coefficients(
                repair, commutator, directions):
            metadata.add((coefficient, directions))
    raw = sorted(metadata, key=repr)
    raw_shifts = [repair.degree_subtract(
        repair.colour_degree(coefficient),
        repair.colour_degree(directions),
    ) for coefficient, directions in raw]
    order = sorted(range(len(raw)),
                   key=lambda index: (repr(raw_shifts[index]), index))
    result = tuple(raw[index] for index in order)
    ordered_shifts = tuple(raw_shifts[index] for index in order)
    require(len(result) == len(columns) == 8580
            and ordered_shifts == tuple(shifts),
            "operator metadata ordering changed")
    # ``aff`` is used by the pinned column constructor; retaining this check
    # prevents an accidental import of a different Spencer implementation.
    require(aff.endpoint_composition_antisymmetric is not None,
            "endpoint composition constructor disappeared")
    return result


def word_of_negative_fine_shift(shift) -> str:
    word = []
    require(len(shift) == 24, "fine shift width")
    for site in range(8):
        block = shift[3 * site:3 * site + 3]
        require(block.count(-1) == 1 and block.count(0) == 2,
                ("fine shift is not a negative word", site, block))
        word.append(str(block.index(-1)))
    return "".join(word)


def exact_seed_cycles(site, loaded, columns, shifts, metadata):
    direct_free_pair = loaded["base"].DIRECT_FREE_PAIR
    seed_indices = tuple(index for index, column in enumerate(columns)
                         if column.get(FIRST_ROW))
    require(len(seed_indices) == 819, len(seed_indices))
    seed_shifts = tuple(sorted({shifts[index] for index in seed_indices},
                               key=repr))
    require(len(seed_shifts) == 2, seed_shifts)
    records = []
    for shift in seed_shifts:
        indices = tuple(index for index in seed_indices
                        if shifts[index] == shift)
        reduced_columns = tuple({
            row: value for row, value in columns[index].items()
            if row[0] < 2 or row == FIRST_ROW
        } for index in indices)
        solution, equation_rank = exact_row_solution(
            reduced_columns, {FIRST_ROW: Q(1)})
        require(len(solution) == 3, (shift, solution))

        full_boundary = Counter()
        for local_index, coefficient in solution.items():
            for row, value in columns[indices[local_index]].items():
                full_boundary[row] += coefficient * value
        full_boundary = Counter({row: value
                                 for row, value in full_boundary.items()
                                 if value})
        require(not any(row[0] < 2 for row in full_boundary)
                and full_boundary[FIRST_ROW] == 1
                and all(row[0] == 2 for row in full_boundary),
                ("seed acquired a proper face", shift, full_boundary))
        d2 = Counter({row: value for row, value in full_boundary.items()
                      if row[0] == 2})
        forbidden = Counter({
            row: value for row, value in d2.items()
            if not site.physical_pair(row[1], direct_free_pair)
        })
        word = word_of_negative_fine_shift(shift)
        terms = []
        for local_index, coefficient in sorted(solution.items()):
            global_index = indices[local_index]
            operator_coefficient, directions = metadata[global_index]
            require(set(FIRST_PAIR).issubset(directions),
                    (word, directions))
            terms.append({
                "weight": str(coefficient),
                "quadratic_coefficient": repr(operator_coefficient),
                "six_directions": repr(directions),
            })
        record = {
            "word": word,
            "fine_shift": list(shift),
            "raw_seed_columns_in_shift": len(indices),
            "exact_equation_rank": equation_rank,
            "exact_operator_terms": terms,
            "operator_weight_profile": sorted(
                (str(value) for value in solution.values())),
            "source_D0_boundary_terms": 0,
            "singleton_D1_boundary_terms": 0,
            "D2_pair_boundary_terms": len(d2),
            "D2_site_repeating_terms": len(forbidden),
            "D2_direct_free_terms": len(d2) - len(forbidden),
            "first_forbidden_pair_coefficient": str(d2[FIRST_ROW]),
            "D2_squared_norm": str(sum(
                (value * value for value in d2.values()), Q(0))),
            "D2_boundary_sha256": sha256(json.dumps(
                sorted((repr(row[1]), str(value)) for row, value in d2.items()),
                separators=(",", ":"),
            ).encode()).hexdigest(),
            "operation_endpoint": "response -> response",
            "cap_r0_projection": 0,
        }
        records.append(record)
    require([record["word"] for record in records]
            == ["11111111", "11211211"]
            and [record["raw_seed_columns_in_shift"] for record in records]
            == [627, 192]
            and [record["exact_equation_rank"] for record in records]
            == [254, 67]
            and [record["D2_pair_boundary_terms"] for record in records]
            == [36, 30]
            and [record["D2_site_repeating_terms"] for record in records]
            == [9, 6]
            and [record["D2_squared_norm"] for record in records]
            == ["18", "39"],
            records)
    return tuple(seed_indices), records


def seed_family_projection_audit(site, loaded, columns, shifts,
                                 seed_indices):
    seed_columns = [columns[index] for index in seed_indices]
    seed_shifts = [shifts[index] for index in seed_indices]
    records = []
    for prime in site.PRIMES:
        record = site.prime_audit(
            seed_columns, seed_shifts,
            loaded["base"].DIRECT_FREE_PAIR, prime,
        )
        require(record["dim_S"] == 178
                and record["site_repeating_coordinate_count"] == 84
                and record["rank_site_repeating_projection"] == 76
                and record[
                    "dim_S_intersection_direct_free_coordinate_space"] == 102,
                record)
        records.append({key: value for key, value in record.items()
                        if key not in ("hit_set",
                                       "first_five_site_repeating_coordinates")})
    return {
        "definition": (
            "all raw homogeneous order-six operators whose D2 direction "
            "set literally contains (01:11) wedge (07:11)"
        ),
        "raw_columns": len(seed_indices),
        "two_prime_records": records,
        "full_family_site_repeating_coordinates_rank": list(
            EXPECTED_FULL_SUPPORT_RANK),
        "coordinate_support_not_hit_by_seed_family": 159 - 84,
        "rank_quotient_full_mod_seed_family": 153 - 76,
        "verdict": (
            "the literal first-face-containing family supplies rank 76, "
            "not the full rank 153; a rank-77 modular quotient remains"
        ),
    }


def operation_idempotent_audit(free_closure):
    ledger, digest = free_closure.audit()
    require(digest == free_closure.EXPECTED_LEDGER_SHA256, digest)
    closure = ledger["typed_free_closure"]
    require(closure["Hom0_response_cap_dimension"] == 0
            and closure["free_closure_operation_changing_C1_count"] == 0,
            closure)
    return {
        "seed_cycle_parent": "order-six EqSystem/response Spencer operator",
        "seed_words": ["11111111", "11211211"],
        "seed_repeated_grade": (
            "labelled codimension-two P3/P4 coloured-cell pair shadow"
        ),
        "cap_word": "01211222",
        "cap_fine_grade": "six t*q_(v,N) P3+K2 occurrence degrees",
        "cap_repeated_grade": "P3+K2",
        "required_operation": "response -> AugP2/K_Eq cap",
        "current_Hom0_response_cap": 0,
        "current_operation_changing_C1": 0,
        "seed_boundary_into_r0": False,
        "first_failure": "operation idempotent, already before cap B/Eq incidence",
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    site = load(
        "computations/verify_h3_order6_site_repeating_target_enrichment_current_tree.py",
        "first_forbidden_seed_site",
    )
    free_closure = load(
        "computations/verify_h3_gamma_star_source_derived_free_closure_census.py",
        "first_forbidden_seed_free_closure",
    )
    loaded = site.modules()
    loaded["site"] = site
    columns, shifts = site.build_operator_columns(loaded)
    metadata = ordered_metadata(loaded, columns, shifts)
    seed_indices, cycle_records = exact_seed_cycles(
        site, loaded, columns, shifts, metadata)
    ledger = {
        "theorem": "h3 first forbidden order-six exact seed-cycle gate",
        "pins": PINS,
        "first_forbidden_row": repr(FIRST_ROW),
        "exact_homogeneous_seed_cycles": cycle_records,
        "seed_containing_family": seed_family_projection_audit(
            site, loaded, columns, shifts, seed_indices),
        "literal_operation_and_cap_gate": operation_idempotent_audit(
            free_closure),
        "verdict": (
            "The first site-repeating row has two exact source-provenant "
            "three-operator lifts, one in each pure/mixed response fine "
            "shift.  Both kill the literal source and singleton Spencer "
            "faces and expose the row monically, but their remaining D2 "
            "boundaries stay in End(response) and have zero cap-r0 "
            "projection.  Even the complete 819-column family containing "
            "this seed has site-repeating rank only 76 at both primes, "
            "leaving a rank-77 quotient before further naturality or a "
            "second generator type is supplied"
        ),
        "scope": (
            "exact rational seed cycles and literal word/fine/operation "
            "typing; two-prime modular seed-family and full-family ranks.  "
            "This does not compute the group orbit of the seed cycles or "
            "construct a response-to-cap bimodule map"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("first forbidden seed ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("all", "cycles", "span", "cap"),
                        default="all")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "sha256": digest}, indent=2, sort_keys=True))
    else:
        print(f"h3 first forbidden exact seed-cycle gate ({arguments.mode}): PASS")
        print("exact seed cycles: THREE OPERATORS IN BOTH WORD SHIFTS")
        print("proper D0/D1 boundaries: ZERO; monic 01^07 face: YES")
        print("seed-containing projection: 84 COORDINATES / RANK 76")
        print("full projection quotient: RANK 77 (BOTH PRIMES)")
        print("boundary into r0: NO, OPERATION IDEMPOTENT FAILURE")
        print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
