#!/usr/bin/env python3
"""Exclude one extra coupled channel beyond every minimal mate type.

For each of the four Laurent mate charts, adjoin every one of the 74 unused
endpoint-colour coordinates with nonzero weight h.  Delete the duplicate
column belonging to the old kernel U and audit maximal minors of the
resulting 243x14 matrix over Q[x^+-1,p^+-1,h^+-1].

Sixty-five coordinates leave the original unit minor unchanged.  For each
of the nine exceptional coordinates, a finite family of complementary
maximal minors has saturated Laurent ideal (1).  Therefore rank(Phi)>=14
for all 296 one-channel charts, so a two-dimensional kernel is impossible.
"""

from __future__ import annotations

from hashlib import sha256
import itertools
import json
from pathlib import Path

import sympy as sp

import verify_shared_reciprocal_two_bad_mixed_bright_completion as chart
import verify_shared_reciprocal_two_bad_mixed_private_row_mates as mates


ROOT = Path(__file__).resolve().parents[1]
PINNED_MATES_SHA256 = (
    "faa0dd9b9f194146203d88fa98bc4f715d71acc650416dec8d091a1caba2dfb7"
)
EXPECTED_DIGEST = "909703d990302ed5e5fcda5b15ed9f2c3ecbdf7ace575f4fdd2ff8c5d313d8ca"

X, P, H = sp.symbols("x p h", nonzero=True)
XI, PI, HI = sp.symbols("xi pi hi")
SAMPLE_H = (1, -1, 2, -2, sp.Rational(1, 2),
            sp.Rational(-1, 2), 3, -3)
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
        "verify_shared_reciprocal_two_bad_mixed_private_row_mates.py"
    )
    require(sha256(path.read_bytes()).hexdigest() == PINNED_MATES_SHA256,
            "the private-row mate dependency changed")


def numerator(expression):
    return sp.factor(sp.together(expression).as_numer_denom()[0])


def is_laurent_monomial(expression):
    polynomial = sp.Poly(numerator(expression), H, X, P)
    return len(polynomial.terms()) == 1


def saturated_unit(minors):
    generators = [numerator(minor) for minor in minors]
    generators.extend((H * HI - 1, X * XI - 1, P * PI - 1))
    basis = sp.groebner(
        generators, H, X, P, HI, XI, PI, order="grevlex"
    )
    return len(basis.polys) == 1 and basis.polys[0].as_expr() == 1


def audit_type(cc_kind, tc_kind):
    base = mates.add_mates(cc_kind, tc_kind, X, P)
    candidates = tuple(cell for cell in ALL_CELLS if cell not in base)
    require(len(base) == 16 and len(candidates) == 74,
            "the one-extra support count changed")

    phi, _cofactors = chart.phi_matrix(base)
    selected_columns = tuple(
        index for index, label in enumerate(chart.LABELS)
        if label != (1, chart.A)
    )
    require(len(selected_columns) == 14,
            "the old-kernel column deletion changed")
    matrix = phi[:, selected_columns]
    pivot_rows = tuple(
        matrix.subs({X: 1, P: 1}).T.rref()[1]
    )
    require(len(pivot_rows) == 14,
            "the base mate chart lost rank 14")

    direct = []
    exceptional = []
    for cell in candidates:
        cells = dict(base)
        cells[cell] = H
        extended, _ = chart.phi_matrix(cells)
        reduced = extended[:, selected_columns]
        first_minor = sp.factor(
            reduced.extract(pivot_rows, tuple(range(14))).det()
        )
        if is_laurent_monomial(first_minor):
            direct.append(cell)
            continue

        minors = [first_minor]
        row_sets = [pivot_rows]
        for value in SAMPLE_H:
            rows = tuple(reduced.subs({X: 1, P: 1, H: value}).T.rref()[1])
            require(len(rows) == 14,
                    "an exceptional reduced matrix lost numeric rank")
            if rows in row_sets:
                continue
            row_sets.append(rows)
            minor = sp.factor(
                reduced.extract(rows, tuple(range(14))).det()
            )
            if minor not in minors:
                minors.append(minor)
        require(saturated_unit(minors),
                f"a one-extra Laurent rank-drop component survived: "
                f"{cc_kind}/{tc_kind} {cell} {minors}")
        exceptional.append({
            "cell": [list(cell[0]), cell[1], cell[2]],
            "first_minor": str(first_minor),
            "complementary_minor_count": len(minors) - 1,
            "complementary_minors": [str(minor) for minor in minors[1:]],
            "saturated_ideal": "1",
        })

    require(len(direct) == 65 and len(exceptional) == 9,
            "the 65+9 one-extra split changed")
    return {
        "type": [cc_kind, tc_kind],
        "base_support": len(base),
        "candidate_coordinates": len(candidates),
        "direct_unit_minor_coordinates": len(direct),
        "exceptional_coordinates": exceptional,
        "verdict": "rank(Phi)>=14 on every localized one-extra chart",
    }


def main():
    pin_dependency()
    records = [
        audit_type(cc_kind, tc_kind)
        for cc_kind, tc_kind in itertools.product(
            mates.CC_ROUTES, mates.TC_ROUTES
        )
    ]
    require(sum(record["candidate_coordinates"] for record in records) == 296,
            "the global one-extra chart count changed")
    require(sum(record["direct_unit_minor_coordinates"] for record in records)
            == 260, "the global direct-unit count changed")
    require(sum(len(record["exceptional_coordinates"]) for record in records)
            == 36, "the global exceptional count changed")

    ledger = {
        "pinned_mates_sha256": PINNED_MATES_SHA256,
        "type_records": records,
        "global_counts": {
            "charts": 4,
            "one_extra_coordinates": 296,
            "direct_unit_minor": 260,
            "saturated_exceptional": 36,
        },
        "repair_invariant": (
            "every one-extra localized chart has rank(Phi)>=14 and hence "
            "kernel dimension at most one"
        ),
        "verdict": (
            "one additional shared mate/cancellation coordinate cannot "
            "restore a two-dimensional kernel, irrespective of bright rows"
        ),
        "scope": (
            "all single endpoint-colour coordinates outside each of the "
            "four minimal mate supports, with all new/mate weights nonzero"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"one-extra channel ledger changed: {digest}")

    print("shared reciprocal two-bad one-extra channel: PASS")
    print("localized charts: 4 x 74 = 296")
    print("unit original minors: 260")
    print("exceptional saturated minor ideals: 36/36 equal (1)")
    print("every chart: rank(Phi)>=14, so dim ker(Phi)<=1")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
