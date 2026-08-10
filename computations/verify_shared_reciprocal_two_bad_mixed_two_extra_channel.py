#!/usr/bin/env python3
"""Exclude two extra coupled channels beyond every minimal mate type.

For each of the four Laurent mate charts, adjoin every unordered pair of
the 74 unused endpoint-colour coordinates with nonzero weights h,k.  The
combinatorial S5 x S3 stabilizer of the four-chart family is first checked;
it is trivial, so all 4*C(74,2)=10804 pair charts are honest orbits.

The cofactor map is quadratic in source cells.  Thus a pair chart inherits
a one-extra Fitting certificate whenever the second cell changes none of
its certified entries.  This exact support test closes 7376 charts.  On the
remaining charts, replay the inherited row bases and keep every Laurent
monomial maximal minor.  Only 459 charts require new minors.  Deterministic
pivot bases and row permutations generate finite maximal-minor families
whose ideals, saturated by x*p*h*k, are (1) over Q.  Hence every pair chart
has rank(Phi)>=14 and kernel dimension at most one.
"""

from __future__ import annotations

from hashlib import sha256
import itertools
import json
from pathlib import Path
import random

import sympy as sp

import verify_shared_reciprocal_two_bad_mixed_bright_completion as chart
import verify_shared_reciprocal_two_bad_mixed_private_row_mates as mates


ROOT = Path(__file__).resolve().parents[1]
PINNED_ONE_EXTRA_SHA256 = (
    "e9af9f227833cc52afd09d0bd053a1ce98b2648e2308ba269fbfbf5cc5cdb530"
)
EXPECTED_DIGEST = "326d888077538c220cbb82a81d5ee8b576c1f848c1e20fae7ab190421517ef39"

X, P, H, K, U = sp.symbols("x p h k u", nonzero=True)
ONE_SAMPLES = (
    1, -1, 2, -2, sp.Rational(1, 2), sp.Rational(-1, 2), 3, -3
)
PAIR_VALUES = ONE_SAMPLES
PAIR_SAMPLES = (
    tuple((1, 1, h, k) for h, k in itertools.product(PAIR_VALUES, repeat=2))
    + tuple((x, p, 1, 1) for x, p in itertools.product(PAIR_VALUES, repeat=2))
    + ((2, 3, 5, 7), (3, 2, 7, 5))
)
ALL_CELLS = tuple(
    (edge, left, right)
    for edge in itertools.combinations(chart.SITES, 2)
    for left in range(3) for right in range(3)
)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def pin_dependency():
    path = ROOT / (
        "computations/"
        "verify_shared_reciprocal_two_bad_mixed_one_extra_channel.py"
    )
    require(sha256(path.read_bytes()).hexdigest() == PINNED_ONE_EXTRA_SHA256,
            "the one-extra channel dependency changed")


def transform_cell(cell, site_permutation, colour_permutation):
    edge, left, right = cell
    u, v = site_permutation[edge[0]], site_permutation[edge[1]]
    left, right = colour_permutation[left], colour_permutation[right]
    if u > v:
        u, v, left, right = v, u, right, left
    return ((u, v), left, right)


def audit_symmetry():
    types = tuple(itertools.product(mates.CC_ROUTES, mates.TC_ROUTES))
    supports = {
        kind: frozenset(mates.add_mates(*kind, 1, 1)) for kind in types
    }
    family_maps = []
    for site_permutation in itertools.permutations(chart.SITES):
        for colour_permutation in itertools.permutations(range(3)):
            mapping = {}
            for kind, support in supports.items():
                image = frozenset(transform_cell(
                    cell, site_permutation, colour_permutation
                ) for cell in support)
                target = next(
                    (other for other, candidate in supports.items()
                     if candidate == image),
                    None,
                )
                if target is None:
                    break
                mapping[kind] = target
            else:
                family_maps.append((site_permutation, colour_permutation,
                                    mapping))
    require(len(family_maps) == 1,
            "the four-chart family acquired a nontrivial symmetry")
    site_permutation, colour_permutation, mapping = family_maps[0]
    require(site_permutation == chart.SITES,
            "the surviving site permutation is not the identity")
    require(colour_permutation == tuple(range(3)),
            "the surviving colour permutation is not the identity")
    require(all(mapping[kind] == kind for kind in types),
            "the identity does not fix every mate type")
    return {"S5xS3_family_stabilizer_order": 1,
            "pair_orbits_per_type": 2701}


def numerator(expression):
    return sp.factor(sp.together(expression).as_numer_denom()[0])


def is_laurent_monomial(expression):
    return len(sp.Poly(numerator(expression), H, K, X, P).terms()) == 1


def saturated_unit(minors):
    generators = list(dict.fromkeys(
        numerator(minor) for minor in minors if minor != 0
    ))
    generators.append(U * H * K * X * P - 1)
    basis = sp.groebner(
        generators, H, K, X, P, U, order="grevlex"
    )
    return (len(basis.polys) == 1
            and basis.polys[0].as_expr() == 1), len(generators) - 1


def pair_positions(first, second):
    """Matrix positions supplied by a disjoint physical cell pair."""
    if not set(first[0]).isdisjoint(second[0]):
        return set()
    sites = set(first[0]) | set(second[0])
    hole = next(iter(set(chart.SITES) - sites))
    colouring = {
        first[0][0]: first[1], first[0][1]: first[2],
        second[0][0]: second[1], second[0][1]: second[2],
    }
    answer = set()
    for inserted_colour in range(3):
        word = dict(colouring)
        word[hole] = inserted_colour
        answer.add((
            chart.WORDS.index(tuple(word[site] for site in chart.SITES)),
            chart.LABELS.index((hole, inserted_colour)),
        ))
    return answer


def one_extra_row_certificates(base, candidates, selected_columns,
                               pivot_rows):
    certificates = {}
    for cell in candidates:
        cells = dict(base)
        cells[cell] = H
        phi, _ = chart.phi_matrix(cells)
        matrix = phi[:, selected_columns]
        row_sets = [pivot_rows]
        for value in ONE_SAMPLES:
            rows = tuple(
                matrix.subs({X: 1, P: 1, H: value}).T.rref()[1]
            )
            require(len(rows) == 14,
                    "a pinned one-extra chart lost numeric rank")
            if rows not in row_sets:
                row_sets.append(rows)
        certificates[cell] = tuple(row_sets)
    return certificates


def certificate_unaffected(primary, other, base_cells, certificates,
                           selected_columns):
    changed_positions = set()
    for cell in base_cells:
        changed_positions |= pair_positions(other, cell)
    changed_positions |= pair_positions(other, primary)
    return all(
        all((row, column) not in changed_positions
            for row in rows for column in selected_columns)
        for rows in certificates[primary]
    )


def certify_exceptional(phi, selected_matrix, row_sets, chart_index):
    minors = [sp.factor(selected_matrix.extract(
        rows, tuple(range(14))
    ).det()) for rows in row_sets]
    unit, _ = saturated_unit(minors)
    full_shapes = []

    for values in PAIR_SAMPLES:
        if unit:
            break
        substitutions = dict(zip((X, P, H, K), values))
        numeric_selected = selected_matrix.subs(substitutions)
        rows = tuple(numeric_selected.T.rref()[1])
        if len(rows) == 14 and rows not in row_sets:
            row_sets.append(rows)
            minors.append(sp.factor(selected_matrix.extract(
                rows, tuple(range(14))
            ).det()))
            if is_laurent_monomial(minors[-1]):
                unit = True
                break
            unit, _ = saturated_unit(minors)
        if unit:
            break

        numeric_full = phi.subs(substitutions)
        columns = tuple(numeric_full.rref()[1][:14])
        if len(columns) == 14:
            rows = tuple(numeric_full[:, columns].T.rref()[1])
            shape = (rows, columns)
            if shape not in full_shapes:
                full_shapes.append(shape)
                minors.append(sp.factor(phi.extract(rows, columns).det()))
                if is_laurent_monomial(minors[-1]):
                    unit = True
                    break
                unit, _ = saturated_unit(minors)

    if not unit:
        rng = random.Random(1729 + chart_index)
        numeric = selected_matrix.subs({X: 2, P: 3, H: 5, K: 7})
        for _ in range(12):
            permutation = list(range(len(chart.WORDS)))
            rng.shuffle(permutation)
            pivots = numeric[permutation, :].T.rref()[1]
            if len(pivots) < 14:
                continue
            rows = tuple(permutation[index] for index in pivots[:14])
            if rows in row_sets:
                continue
            row_sets.append(rows)
            minors.append(sp.factor(selected_matrix.extract(
                rows, tuple(range(14))
            ).det()))
            if is_laurent_monomial(minors[-1]):
                unit = True
                break
            unit, _ = saturated_unit(minors)
            if unit:
                break

    unit, generator_count = saturated_unit(minors)
    require(unit, "a two-extra Laurent rank-drop component survived")
    return generator_count


def audit_type(cc_kind, tc_kind):
    base = mates.add_mates(cc_kind, tc_kind, X, P)
    candidates = tuple(cell for cell in ALL_CELLS if cell not in base)
    require(len(base) == 16 and len(candidates) == 74,
            "the two-extra support count changed")

    phi, _ = chart.phi_matrix(base)
    selected_columns = tuple(
        index for index, label in enumerate(chart.LABELS)
        if label != (1, chart.A)
    )
    base_matrix = phi[:, selected_columns]
    pivot_rows = tuple(
        base_matrix.subs({X: 1, P: 1}).T.rref()[1]
    )
    require(len(pivot_rows) == 14,
            "the base mate chart lost rank 14")
    certificates = one_extra_row_certificates(
        base, candidates, selected_columns, pivot_rows
    )

    inherited_unchanged = 0
    new_pairs = []
    base_cells = tuple(base)
    for first, second in itertools.combinations(candidates, 2):
        if (certificate_unaffected(first, second, base_cells, certificates,
                                   selected_columns)
                or certificate_unaffected(second, first, base_cells,
                                           certificates,
                                           selected_columns)):
            inherited_unchanged += 1
        else:
            new_pairs.append((first, second))

    inherited_monomial = 0
    exceptional = []
    for first, second in new_pairs:
        cells = dict(base)
        cells[first] = H
        cells[second] = K
        extended, _ = chart.phi_matrix(cells)
        selected = extended[:, selected_columns]
        row_sets = []
        for rows in certificates[first] + certificates[second]:
            if rows not in row_sets:
                row_sets.append(rows)
        minors = [sp.factor(selected.extract(
            rows, tuple(range(14))
        ).det()) for rows in row_sets]
        if any(is_laurent_monomial(minor) for minor in minors):
            inherited_monomial += 1
        else:
            exceptional.append((extended, selected, row_sets))

    generator_counts = []
    for index, (extended, selected, row_sets) in enumerate(exceptional):
        generator_counts.append(certify_exceptional(
            extended, selected, row_sets, index
        ))

    return {
        "type": [cc_kind, tc_kind],
        "unordered_pair_orbits": len(tuple(itertools.combinations(
            candidates, 2
        ))),
        "unchanged_one_extra_certificate": inherited_unchanged,
        "new_pair_charts": len(new_pairs),
        "inherited_monomial_certificate": inherited_monomial,
        "saturated_exceptional": len(exceptional),
    }


def main():
    pin_dependency()
    symmetry = audit_symmetry()
    records = [
        audit_type(cc_kind, tc_kind)
        for cc_kind, tc_kind in itertools.product(
            mates.CC_ROUTES, mates.TC_ROUTES
        )
    ]
    require([record["unchanged_one_extra_certificate"] for record in records]
            == [1847, 1841, 1848, 1840],
            "the unchanged-certificate census changed")
    require([record["new_pair_charts"] for record in records]
            == [854, 860, 853, 861],
            "the coupled-pair census changed")
    require([record["saturated_exceptional"] for record in records]
            == [123, 120, 95, 121],
            "the exact saturation census changed")
    require(sum(record["unordered_pair_orbits"] for record in records)
            == 10804, "the global pair count changed")
    require(sum(record["unchanged_one_extra_certificate"]
                for record in records) == 7376,
            "the global unchanged-certificate count changed")
    require(sum(record["inherited_monomial_certificate"]
                for record in records) == 2969,
            "the global inherited-monomial count changed")
    require(sum(record["saturated_exceptional"] for record in records)
            == 459, "the global saturation count changed")

    ledger = {
        "pinned_one_extra_sha256": PINNED_ONE_EXTRA_SHA256,
        "symmetry": symmetry,
        "type_records": records,
        "global_counts": {
            "mate_types": 4,
            "unordered_pair_orbits": 10804,
            "unchanged_one_extra_certificate": 7376,
            "new_pair_charts": 3428,
            "inherited_monomial_certificate": 2969,
            "saturated_exceptional": 459,
        },
        "repair_invariant": (
            "every localized two-extra chart has rank(Phi)>=14 and hence "
            "kernel dimension at most one"
        ),
        "verdict": (
            "two further endpoint-colour coordinates cannot restore the "
            "two-dimensional kernel required by the mixed two-bad packet"
        ),
        "scope": (
            "all unordered pairs outside each of the four minimal mate "
            "supports, with x,p,h,k nonzero over characteristic zero"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"two-extra channel ledger changed: {digest}")

    print("shared reciprocal two-bad two-extra channel: PASS")
    print("honest S5 x S3 family stabilizer: 1")
    print("unordered pair charts: 4 x C(74,2) = 10804")
    print("unchanged certificates: 7376")
    print("new exact charts: 3428 = 2969 monomial + 459 saturated")
    print("every chart: rank(Phi)>=14, so dim ker(Phi)<=1")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
