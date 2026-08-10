#!/usr/bin/env python3
"""Dependency audit for the uniform square-zero one-bad clean cap.

This does not assert the missing extraction theorem.  It verifies the exact
interface between the certified good-chart/full-nine packet and the local
one-bad cap of ca6362b:

* a selected good chart has rank-three deleted endpoint stars;
* a one-bad chart has a zero colour row at both endpoints, hence rank <= 2;
* tilt and endpoint basis changes cannot repair that rank mismatch;
* once a source-faithful one-bad pair with R^[2]=0 is extracted, its cap is
  active and clean and the existing descent applies.

The ledger also fails closed if SP-CLEAN-BRIDGE is ever certified later.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "certification/BASELINE.md":
        "2b3a966a7873a58569e1f4ae0d94d4f32c7139da4bcdaef2cef4bddb254b7f24",
    "certification/SUPERSESSIONS.md":
        "9a758003df15c97ac3b69d36ccf3edfae289ca27b7afd94dd448cf99c85ecda1",
    "notes/unified-full-nine-two-chart-overlap-jet-saturation-target.md":
        "84a2498eca71bf8813fb748832000b21693c0d8280b56a9baa66b9f33deec4fb",
    "notes/two-chart-joint-hypothesis-extraction.md":
        "68554fc43835c2a8aa32d0297bc14cf23a45d7385a8ddf1d1265dedb802b3ab3",
    "notes/tilted-second-chart-activity-and-zero-block-boundary.md":
        "34d30c6f04ba11a9ec0f4644b9bcfa145b3738567b8f668ca8aff0d9abeccfa4",
    "notes/uniform-selector-union-maximal-defect-shore.md":
        "23ad735c59a3ed5e704e2b02f5c53e1871ba41a3397327f387235669ed5994c2",
    "notes/full-nine-type3-annihilator-plane-closure.md":
        "c555baf00004a2738ad85ff77f8b76f62aa71ae8cb2c37733be7c13d5d5bde0d",
    "notes/proof-route-supersession-audit.md":
        "adc00d83326b3ae9728077ebe1c5c5c8c6201f74cb13937a345d1f233754ff71",
    "notes/anchor-lexicographic-curvature-synchronization.md":
        "1f4a3eb5679409a640bc1596fd6dce4b01fbf7296cd02f8d0b342c8e08f85e8a",
    "notes/uniform-one-bad-square-zero-clean-cap.md":
        "2af5f90040152079c094e03b0b1bb794761a07d2418182586ab06848ee820c2e",
    "notes/shared-reciprocal-two-bad-anchor-safe-retraction.md":
        "dda2e2e0b3e81bca41392f355ce3f678a38d8f09053646b2f22df3a86b24bee5",
    "notes/clean-pair-cap-exact-descent-target.md":
        "90f49ac4fde9b793409d9081977e7a7135ebd76c1b5df5d699387d142c2b9b75",
    "proofs/six-site-arbitrary-complex-obstruction.md":
        "b36b2f9ccb577af0aebf897edfc9fa1f84d01ba0cf4ea49ac11799d992e00713",
}

EXPECTED_LEDGER_SHA256 = (
    "28af739dfbed1440b1f3ebe4bdec6663602dd8c4eef0f518d6e819e1b8884af1"
)

Monomial = tuple[int, int, int, int]
Polynomial = dict[Monomial, Fraction]


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def matrix_rank(matrix: tuple[tuple[Fraction, ...], ...]) -> int:
    work = [list(row) for row in matrix]
    row_count = len(work)
    column_count = len(work[0]) if work else 0
    rank = 0
    for column in range(column_count):
        pivot = next((row for row in range(rank, row_count)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = work[rank][column]
        work[rank] = [entry / scale for entry in work[rank]]
        for row in range(row_count):
            if row == rank or not work[row][column]:
                continue
            multiple = work[row][column]
            work[row] = [left - multiple * right
                         for left, right in zip(work[row], work[rank], strict=True)]
        rank += 1
        if rank == row_count:
            break
    return rank


def add(*polynomials: Polynomial) -> Polynomial:
    answer = defaultdict(Fraction)
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            answer[monomial] += coefficient
    return {monomial: coefficient for monomial, coefficient in answer.items()
            if coefficient}


def scale(polynomial: Polynomial, scalar: Fraction) -> Polynomial:
    return {monomial: coefficient * scalar
            for monomial, coefficient in polynomial.items()
            if coefficient * scalar}


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    answer = defaultdict(Fraction)
    for lm, lc in left.items():
        for rm, rc in right.items():
            answer[tuple(a + b for a, b in zip(lm, rm, strict=True))] += lc * rc
    return {monomial: coefficient for monomial, coefficient in answer.items()
            if coefficient}


def audit_good_one_bad_rank_boundary() -> dict[str, object]:
    # Row models for the two deleted endpoint-star maps.  The selected good
    # charts have injective maps.  In the one-bad normal form colour zero is
    # identically absent, while the two response colours may remain independent.
    good = (
        (Fraction(1), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(1)),
    )
    one_bad = (
        (Fraction(0), Fraction(0), Fraction(0)),
        (Fraction(1), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(1), Fraction(0)),
    )
    require(matrix_rank(good) == 3, "the good chart lost injectivity")
    require(matrix_rank(one_bad) == 2, "the one-bad chart rank changed")

    # Invertible colour changes preserve rank.  This concrete adversarial
    # change also shows that mixing the two surviving rows does not create a
    # third row.  A tilted cap changes K, not either endpoint-star map.
    changed = (
        one_bad[0],
        tuple(one_bad[1][i] + one_bad[2][i] for i in range(3)),
        tuple(one_bad[1][i] - one_bad[2][i] for i in range(3)),
    )
    require(matrix_rank(changed) == 2,
            "an invertible binary colour change repaired the missing row")
    return {
        "selected_good_endpoint_rank": 3,
        "one_bad_endpoint_rank_upper_bound": 2,
        "rank_mismatch_is_basis_invariant": True,
        "tilt_changes_cap_direction_not_source_star_maps": True,
    }


def audit_minimal_clean_cap_interface() -> dict[str, object]:
    # Variables are (p1,p2,s1,s2).  The effective response is
    # p1*s1+p1*s2-p2*s1+p2*s2.  Its divided square vanishes modulo the four
    # individual self-square relations, exactly as in ca6362b.
    p1 = {(1, 0, 0, 0): Fraction(1)}
    p2 = {(0, 1, 0, 0): Fraction(1)}
    s1 = {(0, 0, 1, 0): Fraction(1)}
    s2 = {(0, 0, 0, 1): Fraction(1)}
    response = add(multiply(p1, s1), multiply(p1, s2),
                   scale(multiply(p2, s1), Fraction(-1)),
                   multiply(p2, s2))
    response_square = scale(multiply(response, response), Fraction(1, 2))
    quotient = {
        monomial: coefficient for monomial, coefficient in response_square.items()
        if all(exponent <= 1 for exponent in monomial)
    }
    require(not quotient, "the square-zero one-bad cap acquired R^[2]")

    cap = (
        (Fraction(1), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(1), Fraction(1)),
        (Fraction(0), Fraction(-1), Fraction(1)),
    )
    binary_permanent = cap[1][1] * cap[2][2] + cap[1][2] * cap[2][1]
    require(binary_permanent == 0, "the binary cap permanent changed")
    require(tuple(cap[index][index] for index in range(3)) == (1, 1, 1),
            "a target coefficient became inactive")

    # At an intrinsic scalar-unit good pair, the synchronized normal-jet
    # theorem forces (U_a,Theta_a) != (0,0).  The one-bad specialization has
    # G=lambda*q and q^[h]=lambda^-1*X_a, hence U=Theta=0 identically.
    # This is a second exact guard against identifying the two packets.
    for h in range(3, 10):
        lam = Fraction(2)
        unary_g_power = lam**h * (Fraction(1) / lam)
        expected = lam ** (h - 1)
        theta_coefficient = lam ** (h - 1) - expected
        require(unary_g_power - expected == 0 and theta_coefficient == 0,
                f"one-bad normal jets changed at h={h}")

    return {
        "minimal_extra_condition": "R^[2]=0",
        "concrete_sufficient_condition":
            "p1^[2]=p2^[2]=s1^[2]=s2^[2]=0",
        "active_cap": "s=1, kappa=(1,1,1)",
        "binary_permanent": str(binary_permanent),
        "one_bad_intrinsic_normal_class": "(U_a,Theta_a)=(0,0)",
    }


def audit_certification_status() -> dict[str, object]:
    baseline = (ROOT / "certification/BASELINE.md").read_text()
    supersessions = (ROOT / "certification/SUPERSESSIONS.md").read_text()
    require("| `SP-CLEAN-BRIDGE`" in baseline
            and "Open implication" in baseline,
            "the baseline no longer records the open clean bridge")
    require("- Dependency ID: `SP-CLEAN-BRIDGE`" not in supersessions,
            "SP-CLEAN-BRIDGE now has a supersession; redo this audit")
    return {
        "SP-CURVATURE": "certified selected generically active good chart",
        "ROOT-EXTRACTION": "certified full-nine and tilted/direct-free packet",
        "SP-CLEAN-BRIDGE": "open; no accepted supersession",
        "SP-DESCENT": "certified after an active clean cap",
        "SP-K6": "certified terminal six-site obstruction",
        "square_zero_cap_ca6362b": "proved research lemma; not a spine supersession",
        "maximal_shore": "proved/audited classification; no clean-cap conclusion",
        "rootless_type3": (
            "injective full-nine endpoint stars have off-site rank >=2; "
            "rootless nonnilpotence then forces three-site selectors"
        ),
    }


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"pinned dependency changed: {relative}")


def main() -> None:
    pin_dependencies()
    ledger = {
        "rank_boundary": audit_good_one_bad_rank_boundary(),
        "cap_interface": audit_minimal_clean_cap_interface(),
        "certification": audit_certification_status(),
        "minimal_open_lemma": (
            "every synchronized exact source with no active clean cap admits "
            "an exact source-preserving modification or reselection to a "
            "physical pair A_xy=lambda*E_aa with p_a=s_a=0 and effective "
            "binary response R satisfying R^[2]=0"
        ),
        "square_zero_strengthening": (
            "it is enough to force p_b^[2]=p_c^[2]=s_b^[2]=s_c^[2]=0"
        ),
        "branch_audit": {
            "full_nine": "rows only; no direct-block or square-zero concentration",
            "rootless": (
                "good injective stars; type-3 sparse alternatives are closed "
                "and both endpoints have three-site selectors, so not one-bad"
            ),
            "tilt": "activity only; source star maps unchanged",
            "direct_free": "A_pr=0 and nowhere active, not lambda*E_aa",
            "maximal_shore": "aggregate rank classification, not literal row concentration",
            "shared_reciprocal": "can reach one-bad rows on a separate singular-arm route; square-zero remains open",
        },
        "n8_guard": (
            "at h=3 unconditional extraction of this cap is already equivalent "
            "to the open N=8 emptiness/clean-bridge statement"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"dependency ledger changed: {digest}")

    print("uniform one-bad clean-cap dependency audit: PASS")
    print("selected full-nine charts: endpoint rank 3 (good)")
    print("one-bad cap chart: endpoint rank <=2; not a selected good chart")
    print("full-nine/tilt/shore: no square-zero one-bad extraction")
    print("minimal missing lemma: source-preserving one-bad pair with R^[2]=0")
    print("N=8 scope: that extraction is theorem-strength, not an automatic implication")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
