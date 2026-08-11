#!/usr/bin/env python3
"""Audit the nonanchor off-diagonal reselection lemma.

Choose one nonzero pure matching monomial in each of the three target
coefficients of an exact ternary source.  If a nonzero off-diagonal cell is
supported on a physical pair used by none of the three matchings, reselecting
that pair leaves one chosen diagonal anchor in every endpoint row.  The two
deleted-star maps therefore both have rank three.  The already proved
target-augmented private-site identity then puts the same direct cell in the
active determinant/cofactor branch.

The proof is uniform in the even order.  The finite audit below checks every
one of the 31 S8 x S3 anchor types at N=8 and every absent physical pair.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_n8_balanced_anchor_chart_cover.py":
        "3f30d143f3f069f6123bfb41d7ae26833ef508c572c42e09544fe5d415f70d55",
    "computations/verify_uniform_target_augmented_private_site_active_minor.py":
        "c53ba30dd8b7084cc27e05f11aa6066354fdec45ff2cf72ebdfb85bb8517169b",
}
EXPECTED_LEDGER_SHA256 = (
    "88d8f53d4bcdea207b6d4c375f48727798911db4d953252f3a64a16650eed464"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency changed: {relative}: {actual}")


def load(relative, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(spec is not None and spec.loader is not None,
            f"cannot load dependency: {relative}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def matching_neighbour(matching, vertex):
    for left, right in matching:
        if left == vertex:
            return right
        if right == vertex:
            return left
    raise RuntimeError(f"matching does not cover vertex {vertex}: {matching}")


def endpoint_anchor_columns(triple, endpoint, deleted_other):
    """Return the three literal surviving star coordinates.

    Coordinate ``(neighbour, colour)`` is a basis coordinate in the deleted
    star codomain.  Distinct colours remain distinct even when two selected
    matching edges share the same physical neighbour.
    """
    columns = []
    for colour, matching in enumerate(triple):
        neighbour = matching_neighbour(matching, endpoint)
        require(neighbour != deleted_other,
                "the selected pair was unexpectedly an anchor edge")
        columns.append((neighbour, colour))
    return tuple(columns)


def audit_n8_anchor_orbits(module):
    representatives = module.anchor_orbits()
    require(len(representatives) == 31,
            "the balanced-anchor orbit census changed")

    absent_histogram = Counter()
    audited_pairs = 0
    audited_oriented_offdiagonal_cells = 0
    minimum_rank = 3
    for triple in representatives:
        anchor_pairs = {
            edge for matching in triple for edge in matching
        }
        absent = tuple(
            (left, right)
            for left in range(module.N)
            for right in range(left + 1, module.N)
            if (left, right) not in anchor_pairs
        )
        absent_histogram[len(absent)] += 1
        for left, right in absent:
            left_columns = endpoint_anchor_columns(triple, left, right)
            right_columns = endpoint_anchor_columns(triple, right, left)
            left_rank = len(set(left_columns))
            right_rank = len(set(right_columns))
            require((left_rank, right_rank) == (3, 3),
                    "an absent pair lost a rank-three deleted star")
            minimum_rank = min(minimum_rank, left_rank, right_rank)
            audited_pairs += 1
            # Six ordered off-diagonal decorations on every physical pair.
            audited_oriented_offdiagonal_cells += 6

    return {
        "anchor_orbits_mod_S8xS3": len(representatives),
        "absent_pair_histogram_per_representative":
            sorted(absent_histogram.items()),
        "absent_pairs_audited": audited_pairs,
        "oriented_offdiagonal_cells_audited":
            audited_oriented_offdiagonal_cells,
        "minimum_deleted_star_rank": minimum_rank,
    }


def main():
    pin_dependencies()
    balanced = load(
        "computations/verify_n8_balanced_anchor_chart_cover.py",
        "nonanchor_good_pair_balanced_anchor_dependency",
    )
    private = load(
        "computations/verify_uniform_target_augmented_private_site_active_minor.py",
        "nonanchor_good_pair_target_augmented_dependency",
    )

    orbit_audit = audit_n8_anchor_orbits(balanced)
    # Reuse the dependency's exact symbolic identity checks, not just its
    # prose statement.  N=8 is the finite audit; the displayed recurrence in
    # that dependency proves the determinant/cofactor conclusion uniformly.
    source_identity = private.target_augmented_identity(
        private.load(
            "computations/verify_hafnian_private_site_matching_bijection_lemma.py",
            "nonanchor_good_pair_private_site_dependency",
        ),
        8,
    )
    require(source_identity["exact_source_consequence"]
            == "sum_s Delta_us*C_s=-q_u",
            "the target-augmented source consequence changed")

    ledger = {
        "dependencies": PINS,
        "n8_exhaustive_anchor_audit": orbit_audit,
        "target_augmented_identity_at_n8": source_identity,
        "uniform_theorem": (
            "for any three chosen nonzero pure target matchings, a nonzero "
            "off-diagonal cell on a physical pair outside their union can "
            "be reselected without changing the source; both deleted-star "
            "maps have rank three, and the target-augmented private-site "
            "identity forces a nonzero determinant/cofactor product"
        ),
        "chart_cover_consequence": (
            "the unresolved axis-purified cancellation web may be confined "
            "to diagonal cells and off-diagonal decorations of physical "
            "edges already used by at least one chosen target matching; "
            "every other off-diagonal cell returns to a good active-minor "
            "chart"
        ),
        "scope": (
            "goodness plus an active determinant/cofactor is not by itself "
            "an active clean cap or the curved doubly-good OO conclusion"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"nonanchor good-pair ledger changed: {digest}")

    print("uniform nonanchor off-diagonal good-pair reselection: PASS")
    print("N=8 anchor orbits / absent pairs / decorated cells:",
          orbit_audit["anchor_orbits_mod_S8xS3"],
          orbit_audit["absent_pairs_audited"],
          orbit_audit["oriented_offdiagonal_cells_audited"])
    print("minimum deleted-star rank:",
          orbit_audit["minimum_deleted_star_rank"])
    print("remaining branch: decorated anchor edges / diagonal cycle webs")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
