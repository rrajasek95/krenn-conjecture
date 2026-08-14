#!/usr/bin/env python3
"""Re-audit the order-six whole-module target obstruction on the current tree.

This is an independent, source-derived replay of the formerly external
``repair1`` step-9 computation.  It rebuilds all 8,580 order-six operator
columns from the five pinned repository constructors.  For each of two large
primes it computes

    S = D2(ker(source,D1))

and projects S to pair coordinates which cannot occur in the shadow of a
direct-free perfect matching.  The nonphysical coordinates are precisely the
first rows a site-repeating P3/P4 target enlargement must contain.

The full mode is intentionally expensive.  Structural mode checks pins and
the direct-free/site-repeating predicate without performing elimination.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_residual_q_order6_spencer_affine_feasibility.py":
        "ef9bd416986f7dc8c07ffa3b396d1c1f92237c8e1a0539ecbb0ddbeaadb1c18e",
    "computations/verify_h3_residual_q_order6_missing_face_probe.py":
        "5f0e6ad385547aed67f1d954da57c71929d336552bb98d07c68d271889b982ab",
    "computations/verify_h3_residual_q_order5_generator_repair.py":
        "f4b338f557729313fa70da78caec17de861738275b89e7dc9dc97d7e2ae83267",
    "computations/verify_h3_residual_q_covariance_curvature_commutator.py":
        "46a3b6595ab147a17e80908157571a33b61e7faed32deb996506068e206baee9",
    "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py":
        "190171b72493e661dedb8e7aa369a9b72f1a71e14487632df2841ca7eeb19bf4",
}
PRIMES = (1_000_003, 999_983)
MISSING = frozenset(((0, 7, 1, 1), (2, 4, 1, 1)))
EXPECTED_FULL_LEDGER_SHA256 = "a8dc5b16e95bbd2fd603abf09dad36ebd89bb9a269090526231ea16bd95b37fc"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def modules() -> dict[str, object]:
    return {
        "aff": load(
            "computations/verify_h3_residual_q_order6_spencer_affine_feasibility.py",
            "site_repeat_aff",
        ),
        "order6": load(
            "computations/verify_h3_residual_q_order6_missing_face_probe.py",
            "site_repeat_order6",
        ),
        "repair": load(
            "computations/verify_h3_residual_q_order5_generator_repair.py",
            "site_repeat_repair",
        ),
        "commutator": load(
            "computations/verify_h3_residual_q_covariance_curvature_commutator.py",
            "site_repeat_commutator",
        ),
        "base": load(
            "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
            "site_repeat_base",
        ),
    }


def build_operator_columns(modules_by_name: dict[str, object]):
    aff = modules_by_name["aff"]
    order6 = modules_by_name["order6"]
    repair = modules_by_name["repair"]
    commutator = modules_by_name["commutator"]
    base = modules_by_name["base"]
    system = repair.build_system(base, commutator)
    sixth = order6.build_exact_sixth_derivatives(system)
    fifth = aff.exact_derivatives_of_order(system, 5)
    seventh = aff.exact_derivatives_of_order(system, 7)

    metadata = set()
    for _pi, directions in sixth:
        if not MISSING.issubset(directions):
            continue
        for coefficient in order6.eligible_coefficients(
                repair, commutator, directions):
            metadata.add((coefficient, directions))

    columns = []
    shifts = []
    for coefficient, directions in sorted(metadata, key=repr):
        column = Counter()
        for pi in range(3):
            for remainder, value in sixth.get((pi, directions), {}).items():
                column[(0, pi, tuple(sorted(remainder + coefficient)))] += value
        for (new_coefficient, new_directions), weight in \
                aff.endpoint_composition_antisymmetric((coefficient, directions)).items():
            for selected, multiplicity in Counter(new_directions).items():
                rest = list(new_directions)
                rest.remove(selected)
                rest = tuple(rest)
                table = {5: fifth, 6: sixth, 7: seventh}.get(len(rest))
                require(table is not None, "endpoint composition order")
                for pi in range(3):
                    for remainder, value in table.get((pi, rest), {}).items():
                        column[(
                            1, pi, selected,
                            tuple(sorted(remainder + new_coefficient)),
                        )] += weight * multiplicity * value
        for left in range(6):
            for right in range(left + 1, 6):
                pair = tuple(sorted((directions[left], directions[right])))
                column[(2, pair)] += 1
        shifts.append(repair.degree_subtract(
            repair.colour_degree(coefficient),
            repair.colour_degree(directions),
        ))
        columns.append({row: value for row, value in column.items() if value})
    order = sorted(range(len(columns)), key=lambda index: (repr(shifts[index]), index))
    return ([columns[index] for index in order],
            [shifts[index] for index in order])


def row_order(row) -> tuple[bool, str]:
    return row[0] >= 2, repr(row)


def reduce_mod(vector, basis, prime):
    vector = {row: value % prime for row, value in vector.items()
              if value % prime}
    while vector:
        pivot = min(vector, key=row_order)
        if pivot not in basis:
            return vector, pivot
        coefficient = vector[pivot]
        for row, value in basis[pivot].items():
            result = (vector.get(row, 0) - coefficient * value) % prime
            if result:
                vector[row] = result
            else:
                vector.pop(row, None)
    return {}, None


def insert(vector, basis, prime):
    reduced, pivot = reduce_mod(vector, basis, prime)
    if not reduced:
        return False, None
    inverse = pow(reduced[pivot], prime - 2, prime)
    basis[pivot] = {row: value * inverse % prime
                    for row, value in reduced.items()}
    return True, pivot


def physical_pair(pair, direct_free_pair) -> bool:
    (a1, b1, _x, _y), (a2, b2, _z, _w) = pair
    if len({a1, b1, a2, b2}) != 4:
        return False
    if frozenset((a1, b1)) == direct_free_pair:
        return False
    if frozenset((a2, b2)) == direct_free_pair:
        return False
    return True


def prime_audit(columns, shifts, direct_free_pair, prime):
    by_shift = defaultdict(list)
    for column, shift in zip(columns, shifts, strict=True):
        by_shift[repr(shift)].append(column)

    constrained_shadows = []
    for key in sorted(by_shift):
        basis = {}
        for column in by_shift[key]:
            added, pivot = insert(dict(column), basis, prime)
            if added and pivot[0] == 2:
                constrained_shadows.append(basis[pivot])
    shadow_basis = {}
    for vector in constrained_shadows:
        insert(dict(vector), shadow_basis, prime)

    projected = {}
    hit = set()
    for vector in shadow_basis.values():
        nonphysical = {
            row: value for row, value in vector.items()
            if not physical_pair(row[1], direct_free_pair)
        }
        hit.update(nonphysical)
        insert(nonphysical, projected, prime)

    return {
        "prime": prime,
        "dim_S": len(shadow_basis),
        "site_repeating_coordinate_count": len(hit),
        "rank_site_repeating_projection": len(projected),
        "dim_S_intersection_direct_free_coordinate_space":
            len(shadow_basis) - len(projected),
        "S_contained_in_direct_free_target": not projected,
        "first_five_site_repeating_coordinates": [
            repr(row) for row in sorted(hit, key=repr)[:5]
        ],
        "hit_set": tuple(sorted(map(repr, hit))),
    }


def structural_audit(base) -> dict[str, object]:
    direct_free_pair = base.DIRECT_FREE_PAIR
    repeated = (
        (0, 1, 1, 1),
        (0, 7, 1, 1),
    )
    disjoint = (
        (0, 7, 1, 1),
        (2, 4, 1, 1),
    )
    require(not physical_pair(repeated, direct_free_pair)
            and physical_pair(disjoint, direct_free_pair),
            "site-repeating predicate changed")
    return {
        "direct_free_pair": sorted(direct_free_pair),
        "physical_pair_criterion": (
            "the two coloured cells use four distinct sites and neither is "
            "the deleted direct-free endpoint pair"
        ),
        "site_repeating_example": repr(repeated),
        "example_is_direct_free_matching_shadow": False,
        "disjoint_control": repr(disjoint),
        "control_is_direct_free_matching_shadow": True,
    }


def audit(full: bool) -> tuple[dict[str, object], str]:
    pin_dependencies()
    loaded = modules()
    structural = structural_audit(loaded["base"])
    ledger = {
        "theorem": "h3 current-tree order-six site-repeating target enrichment audit",
        "pins": PINS,
        "structural": structural,
        "full_elimination_performed": full,
    }
    if full:
        columns, shifts = build_operator_columns(loaded)
        require(len(columns) == len(shifts) == 8580,
                "order-six column count changed")
        records = tuple(prime_audit(
            columns, shifts, loaded["base"].DIRECT_FREE_PAIR, prime,
        ) for prime in PRIMES)
        public_records = []
        for record in records:
            require(record["dim_S"] == 488
                    and record["site_repeating_coordinate_count"] == 159
                    and record["rank_site_repeating_projection"] == 153
                    and record[
                        "dim_S_intersection_direct_free_coordinate_space"] == 335
                    and not record["S_contained_in_direct_free_target"],
                    record)
            public_records.append({
                key: value for key, value in record.items() if key != "hit_set"
            })
        require(records[0]["hit_set"] == records[1]["hit_set"],
                "the two primes see different site-repeating supports")
        ledger.update({
            "operator_columns": len(columns),
            "prime_audits": public_records,
            "two_prime_site_repeating_support_agrees": True,
            "minimal_coordinate_enlargement": {
                "new_pair_coordinates": 159,
                "rank_seen_by_constrained_universal_D2": 153,
                "effect": (
                    "removes the direct-free coordinate-support obstruction; "
                    "it does not construct a termwise target differential"
                ),
            },
            "verdict": (
                "On the current pinned tree the constrained universal D2 image "
                "has dimension 488.  Its projection to 159 pair coordinates "
                "forbidden in a direct-free matching target has rank 153 at "
                "both primes.  Therefore a whole-module mixed-jet comparison "
                "cannot land in the direct-free target.  A minimal coordinate "
                "target must add exactly those 159 site-repeating P3/P4 pair "
                "rows; only 153 independent combinations are used here."
            ),
            "scope": (
                "two-prime exact-constructor modular rank replay.  It proves "
                "necessity of site-repeating target rows, not sufficiency of "
                "the enlarged target or existence of Phi."
            ),
        })
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if full and EXPECTED_FULL_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_FULL_LEDGER_SHA256,
                ("site-repeating full ledger changed", digest))
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("full", "structural"), default="full")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit(arguments.mode == "full")
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "sha256": digest}, indent=2, sort_keys=True))
    elif arguments.mode == "full":
        print("h3 order-six current-tree site-repeating target audit: PASS")
        print("columns=8580; dim S=488; direct-free intersection=335")
        print("site-repeating coordinates=159; projected rank=153 (both primes)")
        print("whole-module direct-free target: OBSTRUCTED")
        print("ledger_sha256=" + digest)
    else:
        print("h3 order-six site-repeating structural audit: PASS")
        print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
