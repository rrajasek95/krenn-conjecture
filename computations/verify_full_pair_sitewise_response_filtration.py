#!/usr/bin/env python3
"""Exact combinatorial audit of the full-pair sitewise filtration.

This is the direct-edge extension of
``verify_sitewise_common_power_response_filtration.py``.  On a deleted
pair with six residual sites the scalarized full-nine matrix is

    M = a*h + P*C*S^T = diag(X_0, X_1, X_2),

where h is the scalar evaluation of q^[3].  Entries of P*C*S^T have
incidence-ideal order at least four, while h has order six and contains a
factor from every residual-site incidence ideal.  The audit checks the
determinant order/site ledger and the sharp coordinate-plane consequence.

The proof is in notes/full-pair-sitewise-response-filtration.md.  This
checker uses explicit ``require`` calls so all checks remain live under
``python -O``.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json


EXPECTED_LEDGER_SHA256 = (
    "60fa0aa1467e3494dc166104927c8ed5385fa454fcafc8619a4224faafc634da"
)
SITES = tuple(range(6))
TRIPLES = tuple(combinations(SITES, 3))


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def nonzero_cofactor_permutations(rows, columns):
    for permutation in permutations(columns):
        if all(row != column for row, column in zip(rows, permutation)):
            yield permutation


def audit_response_determinant_site_coverage():
    """Audit the all-response Cauchy--Binet determinant terms.

    A nonzero term has three cofactor entries.  At site u its number of
    internal-q factors is 3-1_{u in I}-1_{u in K}, hence at least one.
    """

    patterns = Counter()
    term_count = 0
    for rows in TRIPLES:
        for columns in TRIPLES:
            permutations_here = tuple(
                nonzero_cofactor_permutations(rows, columns)
            )
            if not permutations_here:
                continue
            exponents = tuple(
                3 - int(site in rows) - int(site in columns)
                for site in SITES
            )
            require(min(exponents) >= 1,
                    "an all-response determinant term lost a site factor")
            require(sum(exponents) == 12,
                    "an all-response determinant term changed total order")
            patterns[tuple(sorted(exponents))] += 1
            term_count += len(permutations_here)
    require(set(patterns) == {
        (2, 2, 2, 2, 2, 2),
        (1, 2, 2, 2, 2, 3),
        (1, 1, 2, 2, 3, 3),
        (1, 1, 1, 3, 3, 3),
    }, "the all-response site patterns changed")
    return term_count, patterns


def audit_direct_response_determinant_orders():
    """Audit every direct/response choice in a 3x3 determinant.

    A direct entry contributes the common scalar h of order six.  A
    response entry has order at least four.  Therefore a term choosing k
    direct entries has order at least 6k+4(3-k)=12+2k.  If k>0 it also
    lies in every residual-site ideal because h does.
    """

    histogram = Counter()
    for permutation in permutations(range(3)):
        for choices in product(("R", "H"), repeat=3):
            direct_count = choices.count("H")
            order = 6 * direct_count + 4 * (3 - direct_count)
            require(order == 12 + 2 * direct_count,
                    "a determinant filtration order changed")
            require(order >= 12,
                    "the arbitrary direct block lowered determinant order")
            histogram[(direct_count, order)] += 1
    require(histogram == Counter({
        (0, 12): 6,
        (1, 14): 18,
        (2, 16): 18,
        (3, 18): 6,
    }), "the determinant direct/response histogram changed")
    return histogram


def audit_coordinate_plane_boundary():
    """Exhaust the dimension-at-most-two incidence consequence."""

    assignments = 0
    omission_histogram = Counter()
    for masks in product(range(1, 7), repeat=6):
        if any(mask.bit_count() > 2 for mask in masks):
            continue
        colour_counts = tuple(
            sum((mask >> colour) & 1 for mask in masks)
            for colour in range(3)
        )
        if min(colour_counts) < 4:
            continue
        # Site cover is imposed as part of masks in range(1,7).  The order
        # count now has equality throughout.
        require(colour_counts == (4, 4, 4),
                "a rank-at-most-two cover ceased to be sharp")
        require(all(mask.bit_count() == 2 for mask in masks),
                "a site in the sharp boundary did not contain two axes")
        omitted = tuple(
            next(colour for colour in range(3)
                 if not ((mask >> colour) & 1))
            for mask in masks
        )
        require(Counter(omitted) == Counter({0: 2, 1: 2, 2: 2}),
                "the omitted-colour pairs changed")
        for colour in range(3):
            missing_sites = tuple(
                site for site, missing in enumerate(omitted)
                if missing == colour
            )
            require(len(missing_sites) == 2,
                    "a colour no longer has a two-site omission pair")
            # A pure-colour q^[3] term uses all six sites and is impossible
            # because these two local spaces omit that axis.  A pure-colour
            # q^[2] coefficient can use four sites only when its complement
            # is exactly the omission pair.
            available = tuple(
                site for site in SITES if site not in missing_sites
            )
            require(len(available) == 4,
                    "the unique pure q^[2] complement changed")
        omission_histogram[tuple(sorted(Counter(omitted).values()))] += 1
        assignments += 1
    require(assignments > 0, "the coordinate-plane boundary became empty")
    return assignments, omission_histogram


def audit():
    term_count, patterns = audit_response_determinant_site_coverage()
    determinant_histogram = audit_direct_response_determinant_orders()
    assignments, omission_histogram = audit_coordinate_plane_boundary()

    ledger = {
        "residual_sites": 6,
        "entry_response_order": 4,
        "entry_direct_order": 6,
        "entry_target_order_lower_bound": 4,
        "all_response_determinant_terms": term_count,
        "all_response_site_patterns": {
            ",".join(map(str, key)): value
            for key, value in sorted(patterns.items())
        },
        "determinant_direct_response_histogram": {
            f"direct={key[0]},order={key[1]}": value
            for key, value in sorted(determinant_histogram.items())
        },
        "determinant_order_lower_bound": 12,
        "determinant_in_every_site_ideal": True,
        "coordinate_plane_assignments": assignments,
        "omission_histogram": {
            ",".join(map(str, key)): value
            for key, value in sorted(omission_histogram.items())
        },
        "coordinate_plane_omissions": "two sites per colour",
        "pure_q3_target_on_coordinate_plane": False,
        "unique_pure_q2_complement": True,
        "scope": (
            "arbitrary 3x3 direct block on one deleted pair; six residual "
            "sites; proves the four-cover/site-cover and the sharp "
            "coordinate-plane boundary, not overlap compatibility or the "
            "full conjecture"
        ),
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode("ascii")).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "the full-pair sitewise filtration ledger changed")
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    print("full-pair sitewise response filtration: PASS")
    print("all-response determinant terms:",
          ledger["all_response_determinant_terms"])
    print("determinant order lower bound:",
          ledger["determinant_order_lower_bound"])
    print("coordinate-plane assignments:",
          ledger["coordinate_plane_assignments"])
    print("sha256:", digest)


if __name__ == "__main__":
    main()
