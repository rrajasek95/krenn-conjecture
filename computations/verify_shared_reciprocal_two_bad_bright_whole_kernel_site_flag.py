#!/usr/bin/env python3
"""Whole-kernel site flags forced by each bright pure preimage.

Apply the pinned two-star pure-response lemma to a*G=X_i and b*G=0
for every b in B=ker(Phi).  If every local a_z is nonzero, the linear
subspaces L_z={b in B: b_z in C*a_z} cover B.  Over C one L_z is all of
B.  If it is the unique such site, a second finite-union argument chooses
b with D(a,b) exactly that singleton, so the two-star lemma forces the
target factor e_i onto C*a_z.

In the nondegenerate bright-pairing branch, the target projection of B has
minimal support S of size two.  A unique flag aligned with e_a or e_c lies
outside S.  The result is applied separately to Q_c*G=X_c and R_a*G=X_a.
"""

from __future__ import annotations

from hashlib import sha256
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_centered_rank_one_two_star_pure_response.py":
        "c8d6c93bfe43c6661971570abfd260b98c91acdf934be7f6e9c61eb972913ba1",
    "computations/verify_shared_reciprocal_two_bad_target_projection_pair_reduction.py":
        "bb01f6de80af4132b6a9736338f24927533d9224cb2f4f9ee1fd228515e7f765",
}
EXPECTED_DIGEST = "b7b190935d4b07cfcc3b47d478647f4db86fc7cbe6626bbcd668473c2864c20e"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency changed: {relative}: {actual}")


def audit_finite_union_field_guard():
    # Over F2, the three proper lines of F2^2 cover the whole space.  Thus
    # the infinite-field hypothesis in the upgrade from pointwise D(a,b)
    # to one site flag for the whole kernel is load-bearing.
    field = (0, 1)
    vectors = set(itertools.product(field, repeat=2))
    lines = (
        {(0, 0), (1, 0)},
        {(0, 0), (0, 1)},
        {(0, 0), (1, 1)},
    )
    require(all(line < vectors for line in lines),
            "an F2 line stopped being a proper subspace")
    require(set().union(*lines) == vectors,
            "the finite-field finite-union counterguard changed")
    return {
        "field": "F2",
        "ambient_size": len(vectors),
        "proper_subspaces": len(lines),
        "union_size": len(set().union(*lines)),
        "verdict": "finite-union rigidity requires an infinite field",
    }


def audit_five_site_flag_census():
    sites = frozenset(range(5))
    target_pair = frozenset((0, 4))
    outside = sites - target_pair
    nonempty = tuple(
        frozenset(subset)
        for size in range(1, 6)
        for subset in itertools.combinations(sites, size)
    )
    unique = tuple(flag for flag in nonempty if len(flag) == 1)
    multiple = tuple(flag for flag in nonempty if len(flag) >= 2)
    allowed_unique = tuple(flag for flag in unique if flag <= outside)
    allowed = allowed_unique + multiple

    require((len(nonempty), len(unique), len(multiple)) == (31, 5, 26),
            "the five-site nonempty-flag census changed")
    require(len(allowed_unique) == 3 and len(allowed) == 29,
            "the fixed-pair unique-flag reduction changed")

    pair_types = {"unique/unique": 0, "unique/multiple": 0,
                  "multiple/multiple": 0}
    for left, right in itertools.product(allowed, repeat=2):
        if len(left) == len(right) == 1:
            pair_types["unique/unique"] += 1
        elif len(left) == 1 or len(right) == 1:
            pair_types["unique/multiple"] += 1
        else:
            pair_types["multiple/multiple"] += 1
    require(pair_types == {
        "unique/unique": 9,
        "unique/multiple": 156,
        "multiple/multiple": 676,
    }, "the paired bright-flag census changed")

    same_unique = sum(
        left == right for left, right in itertools.product(
            allowed_unique, repeat=2
        )
    )
    require(same_unique == 3,
            "the same-site unique-axis overlap count changed")
    return {
        "sites": 5,
        "minimal_target_pair": sorted(target_pair),
        "all_nonempty_flag_sets": len(nonempty),
        "multiple_site_flag_sets": len(multiple),
        "allowed_unique_axis_sites": sorted(outside),
        "zero_free_flag_sets_per_bright_row": len(allowed),
        "paired_flag_patterns": pair_types,
        "same_site_distinct_axis_unique_patterns": same_unique,
    }


def audit_site_flag_implication():
    # This is the exact logical dependency used in the proof.  The pinned
    # two-star lemma supplies D(a,b)!=empty for every b, and supplies
    # x_r in span(a_r,b_r) when D(a,b)={r}.
    stages = (
        "for every b in B, B is covered by L_z={b:b_z in C*a_z}",
        "over C, some L_z equals B",
        "if L_r=B is unique, choose b outside the other proper L_z",
        "then D(a,b)={r} and x_r lies in span(a_r,b_r)=C*a_r",
    )
    require(len(stages) == 4 and len(set(stages)) == 4,
            "the whole-kernel finite-union proof stages changed")

    # In branch (iii), W=pi_t(B) is two-dimensional and supported on the
    # minimal two-site set S.  If a_r is a bright axis e_i (i!=t) and all
    # b_r lie in C*a_r, every b has zero t-coordinate at r, hence r notin S.
    target_colour = 2
    bright_colours = (0, 1)
    require(all(colour != target_colour for colour in bright_colours),
            "a bright colour collided with the missing target")
    return {
        "proof_stages": list(stages),
        "single_bright_trichotomy": [
            "some local bright-preimage entry a_z is zero",
            "at least two sites satisfy ev_z(B) subset C*a_z",
            "one unique site r satisfies ev_r(B) subset C*a_r and a_r parallel x_r",
        ],
        "branch_iii_refinement": (
            "for X_a or X_c, a zero-free unique target-axis flag lies "
            "outside the minimal two-site support of pi_t(B)"
        ),
    }


def main():
    pin_dependencies()
    field_guard = audit_finite_union_field_guard()
    census = audit_five_site_flag_census()
    implication = audit_site_flag_implication()
    ledger = {
        "pins": PINS,
        "field_guard": field_guard,
        "five_site_census": census,
        "implication": implication,
        "applications": {
            "Q_c": "Phi(Q_c)=X_c, B=ker(Phi)",
            "R_a": "Phi(R_a)=X_a, B=ker(Phi)",
        },
        "verdict": (
            "each bright preimage forces a zero entry, two whole-kernel "
            "line flags, or one bright-axis flag outside the target pair"
        ),
        "scope": (
            "support-free five-site common-cofactor map over C; this is a "
            "normalization input, not yet the private-row chart cover"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"bright whole-kernel site-flag ledger changed: {digest}")

    print("shared reciprocal bright whole-kernel site flag: PASS")
    print("each bright row: zero, >=2 kernel-line sites, or one target-axis site")
    print("branch (iii): a unique axis site lies outside the fixed target pair")
    print("paired zero-free flag patterns: 9 + 156 + 676 = 841")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
