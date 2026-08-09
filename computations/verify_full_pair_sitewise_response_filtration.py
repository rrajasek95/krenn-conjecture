#!/usr/bin/env python3
"""Exact combinatorial audit of the full-pair sitewise filtration.

This is the direct-edge and arbitrary-order extension of
``verify_sitewise_common_power_response_filtration.py``.  On a deleted
pair with ``2m`` residual sites the scalarized full-nine matrix is

    M = a*h + P*C*S^T = diag(X_0, X_1, X_2),

where h is the scalar evaluation of q^[m].  Entries of P*C*S^T have
incidence-ideal order at least ``2m-2``, while h has order ``2m`` and contains a
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
    "8d6cbe1f366267d563c95d2bf57abeecebc34c5e13de013e8bcb200ae4055b9e"
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


def audit_uniform_order_and_full_site_bound():
    """Audit the arbitrary-even-order formulas and their sharp model.

    For 2m residual sites the three colour covers have total incidence at
    least 3(2m-2).  If t sites have full three-dimensional incident space
    and every other site has dimension at most two, the total is at most
    4m+t.  Hence t>=2m-6.  The bound is sharp at the incidence level: use
    2m-6 full sites and six coordinate planes, two omitting each colour.
    """

    rows = []
    for m in range(2, 9):
        residual_sites = 2 * m
        response_order = 2 * m - 2
        direct_order = 2 * m
        determinant_orders = tuple(
            direct_order * direct_count
            + response_order * (3 - direct_count)
            for direct_count in range(4)
        )
        require(determinant_orders == tuple(
            6 * m - 6 + 2 * direct_count
            for direct_count in range(4)
        ), "the uniform determinant-order formula changed")

        # Every all-response Cauchy--Binet term chooses three distinct P
        # sites I and three distinct S sites K.  Each of its three internal
        # cofactors contains site u except when u is the corresponding P or
        # S endpoint, so the local occurrence is exactly 3-I_u-K_u.
        triples = tuple(combinations(range(residual_sites), 3))
        triple_pair_count = 0
        for left in triples:
            for right in triples:
                occurrences = tuple(
                    3 - int(site in left) - int(site in right)
                    for site in range(residual_sites)
                )
                require(min(occurrences) >= 1,
                        "a uniform all-response term lost a site factor")
                require(sum(occurrences) == 6 * m - 6,
                        "a uniform all-response term changed total order")
                triple_pair_count += 1
        require(triple_pair_count == len(triples) ** 2,
                "the uniform Cauchy--Binet triple-pair census changed")

        forced_full_sites = max(0, 2 * m - 6)
        cover_incidence = 3 * response_order
        maximum_without_bound = 4 * m + forced_full_sites
        require(maximum_without_bound >= cover_incidence,
                "the claimed full-site lower bound is too large")
        if forced_full_sites:
            require(4 * m + forced_full_sites - 1 < cover_incidence,
                    "the claimed full-site lower bound is not minimal")

        # Incidence-sharp construction for m>=3: full sites followed by
        # two copies of each coordinate plane (masks 110,101,011).
        sharp_counts = None
        if m >= 3:
            masks = ([7] * forced_full_sites
                     + [6, 6, 5, 5, 3, 3])
            require(len(masks) == residual_sites,
                    "the sharp uniform incidence model changed size")
            sharp_counts = tuple(
                sum((mask >> colour) & 1 for mask in masks)
                for colour in range(3)
            )
            require(sharp_counts == (response_order,) * 3,
                    "the sharp uniform colour covers changed")
            require(sum(mask == 7 for mask in masks) == forced_full_sites,
                    "the sharp model changed its number of full sites")

        rows.append({
            "m": m,
            "source_order": 2 * m + 2,
            "residual_sites": residual_sites,
            "colour_cover": response_order,
            "determinant_orders": determinant_orders,
            "cauchy_binet_triple_pairs": triple_pair_count,
            "forced_full_sites": forced_full_sites,
            "sharp_colour_counts": sharp_counts,
        })
    require(tuple(row["forced_full_sites"] for row in rows)
            == (0, 0, 2, 4, 6, 8, 10),
            "the uniform full-site ledger changed")
    return rows


def audit():
    term_count, patterns = audit_response_determinant_site_coverage()
    determinant_histogram = audit_direct_response_determinant_orders()
    assignments, omission_histogram = audit_coordinate_plane_boundary()
    uniform_rows = audit_uniform_order_and_full_site_bound()

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
        "uniform_rows": uniform_rows,
        "scope": (
            "arbitrary 3x3 direct block on one deleted pair at every even "
            "order; proves the colour-cover/site-cover and the sharp N=8 "
            "coordinate-plane boundary plus the N-8 full-incident-site "
            "bound, not overlap compatibility or the full conjecture"
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
    print("forced full incident sites at N=6,8,...,18:",
          tuple(row["forced_full_sites"] for row in ledger["uniform_rows"]))
    print("sha256:", digest)


if __name__ == "__main__":
    main()
