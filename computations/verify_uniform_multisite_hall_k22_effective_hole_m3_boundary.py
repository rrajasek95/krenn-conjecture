#!/usr/bin/env python3
"""Close reverse-hole reselection and isolate the exact M3 lock boundary.

Diagonal Hall families are families of nonzero *complete unordered-hole
aggregates*, not families of individual oriented monomials.  Hence a reverse
orientation which cancels the selected orientation simply makes that hole
ineffective.  The target coefficient one supplies another effective hole;
no source coefficient changes and no termination argument is needed.

For the other Q0-copy outcome, the M3 complete crossed cofactor still has an
exact boundary.  A bridge term leaves the anchor web.  An off-anchor
off-diagonal endpoint mate enters the target-augmented active-minor theorem.
The currently proved full-row machinery leaves only an anchor-contained,
injective five-row lock with no complementary off-anchor wedge.  Minimum
support can delete a blocker only after a simultaneous lock-kernel vector is
known, so entry-minimality alone does not close this last packet.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_multisite_hall_k22_q0_copy_affine_closure.py":
        "d3f2c895f4e487dd53e488f7aba446611b8f1b4ed618aeeb75da07ba4a44107d",
    "notes/uniform-multisite-hall-k22-q0-copy-affine-closure.md":
        "6247c95459492a1cca8908eed03b1a59cac9dba8692be3cdcd47d7879d36bb5b",
    "computations/verify_uniform_multisite_hall_k22_unary_mate_routing.py":
        "543e73ff1ed4eeefb6bbd33a603137f99381c7ad2e7eb28cee5ec55c4ae1956a",
    "notes/uniform-multisite-hall-k22-unary-mate-routing.md":
        "11625211e28d1fd0971f39a05e7da77d66aa4d8c17c357a688b3ec90100c4fec",
    "computations/verify_uniform_target_augmented_private_site_active_minor.py":
        "c53ba30dd8b7084cc27e05f11aa6066354fdec45ff2cf72ebdfb85bb8517169b",
    "notes/uniform-target-augmented-private-site-active-minor.md":
        "d7b16ecbb867524615ecf3034e0911e0add34825a7f9088f369f3a11e1c61f0d",
    "computations/verify_uniform_one_bad_nonanchor_offdiagonal_good_pair.py":
        "64e85cd84112b5160efe4f43ce1208da3c49f5e58b3e4a4d6192e6a9c229c306",
    "notes/uniform-one-bad-nonanchor-offdiagonal-good-pair.md":
        "4516c5ff02f130e1ad25b4fde395c81557e58ba0c83f7f98969d95df17fd6409",
    "computations/verify_uniform_five_lock_wedge_or_switch.py":
        "c2541a60db1f8e7a661bc698d2bd1f1a1f396a0f0bfde389ea89bea17fac175e",
    "notes/uniform-five-lock-wedge-or-switch.md":
        "0871d5151a0fdb46fee0c9b15797a864e579a85c360a2638d458583479426914",
    "computations/verify_uniform_multisite_endpoint_affine_hall_concentration_boundary.py":
        "f24e9bd69ec4baef96104557571c154b399f87f34074edffda27e551f33c2205",
    "notes/uniform-multisite-endpoint-affine-hall-concentration-boundary.md":
        "241b46d9ecede656aa59f2be6d74bc288fbada2aa4843103a950441066763df2",
}
EXPECTED_LEDGER_SHA256 = "ca3131bd96d85dd6ee4a1f8508a6f51bfa915a4ff9b55671698fdc10afce8a6e"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


# Sparse commutative polynomials over Q.
def clean(polynomial):
    return Counter({term: coefficient for term, coefficient
                    in polynomial.items() if coefficient})


def variable(name):
    return Counter({(name,): Q(1)})


def add(*polynomials):
    answer = Counter()
    for polynomial in polynomials:
        answer.update(polynomial)
    return clean(answer)


def multiply(*polynomials):
    answer = Counter({(): Q(1)})
    for polynomial in polynomials:
        updated = Counter()
        for left, left_coefficient in answer.items():
            for right, right_coefficient in polynomial.items():
                updated[tuple(sorted(left + right))] += (
                    left_coefficient * right_coefficient
                )
        answer = clean(updated)
    return answer


def audit_complete_unordered_hole_factorization():
    # Directly regroup the complete ordered-hole response at one pure target
    # word.  The two orientations of {u,v} have the same q cofactor C_uv.
    sites = tuple(range(6))
    p = {site: variable(f"p{site}") for site in sites}
    s = {site: variable(f"s{site}") for site in sites}
    cofactors = {
        (left, right): variable(f"C{left}{right}")
        for left in sites for right in sites if left < right
    }
    ordered = add(*(
        multiply(p[left], s[right], cofactors[tuple(sorted((left, right)))])
        for left in sites for right in sites if left != right
    ))
    unordered = add(*(
        add(multiply(p[left], s[right], cofactors[(left, right)]),
            multiply(p[right], s[left], cofactors[(left, right)]))
        for left in sites for right in sites if left < right
    ))
    require(ordered == unordered and len(unordered) == 30,
            "the complete unordered-hole regrouping changed")

    # A concrete reverse cancellation at 01 removes that physical hole from
    # the effective family while another hole carries the target coefficient.
    values = {
        "p0": Q(1), "s1": Q(1), "p1": Q(1), "s0": Q(-1),
        "C01": Q(7),
        "p2": Q(1), "s3": Q(1), "p3": Q(0), "s2": Q(0),
        "C23": Q(1),
    }
    hole01 = (values["p0"] * values["s1"]
              + values["p1"] * values["s0"]) * values["C01"]
    hole23 = (values["p2"] * values["s3"]
              + values["p3"] * values["s2"]) * values["C23"]
    require((hole01, hole23, hole01 + hole23) == (0, 1, 1),
            "the reverse-axis ineffective-hole guard changed")
    return {
        "ordered_terms": 30,
        "unordered_physical_holes": 15,
        "aggregate_formula":
            "sum_{u<v}(p_u*s_v+p_v*s_u)*C_uv",
        "reverse_axis_sample": {
            "hole01_bracket": "1*1+1*(-1)=0",
            "C01": 7,
            "hole01_complete_contribution": 0,
            "hole23_complete_contribution": 1,
            "target_total": 1,
        },
        "source_step": (
            "none: an ineffective hole is omitted from the effective Hall "
            "family; target total one supplies a different nonzero complete "
            "hole contribution"
        ),
    }


def audit_m3_complete_row_boundary():
    # Exact crossed cofactor from the already pinned unary-mate routing.
    q12, q45, q14, q25, q15, q24 = (
        variable(name) for name in
        ("q12_11", "q45_11", "q14_11", "q25_11",
         "q15_11", "q24_11")
    )
    h03 = add(multiply(q12, q45), multiply(q14, q25),
              multiply(q15, q24))
    require(set(h03) == {
        ("q12_11", "q45_11"),
        ("q14_11", "q25_11"),
        ("q15_11", "q24_11"),
    }, "the M3 complete crossed cofactor changed")
    return {
        "selected_M3_pivot": "q12_11*q45_11",
        "complete_crossed_cofactor":
            "q12_11*q45_11+q14_11*q25_11+q15_11*q24_11",
        "proved_exits": [
            "either bridge product is a free/active anchor-web exit",
            (
                "an off-anchor off-diagonal endpoint mate enters the exact "
                "target-augmented private-site active-minor route"
            ),
            (
                "a nonzero simultaneous five-row lock kernel gives an "
                "anchor-safe entry-minimal deletion"
            ),
            (
                "opposite crossed components at complementary off-anchor "
                "ports give the certified distinct-head four-good wedge"
            ),
        ],
        "unclosed_interface": (
            "the anchor-contained off-axis lock map may remain injective "
            "with no complementary off-anchor wedge"
        ),
        "entry_minimality_boundary": (
            "entry-minimality deletes a blocker only after a nonzero exact "
            "kernel direction is constructed; injectivity supplies no "
            "source modification"
        ),
        "first_missing_global_row": (
            "an opposite crossed companion with common matching provenance, "
            "or an identity forcing a dependence among the five unary/11/"
            "12/21/22 lock columns"
        ),
    }


def main():
    pin_dependencies()
    ledger = {
        "complete_effective_holes":
            audit_complete_unordered_hole_factorization(),
        "M3_boundary": audit_m3_complete_row_boundary(),
        "reverse_axis_theorem": (
            "reverse-axis cancellation closes as a selection issue: the "
            "unordered hole has zero complete contribution and is absent "
            "from the effective Hall family; target coefficient one gives "
            "another effective hole without changing the source"
        ),
        "M3_verdict": (
            "free bridges, off-anchor active mates, lock kernels, and "
            "complementary crossed wedges are closed.  The exact remaining "
            "case is an anchor-contained injective five-row lock with no "
            "complementary off-anchor wedge"
        ),
        "scope": (
            "uniform complete-hole algebra and theorem-dependency audit, "
            "not a matching census.  No physical full-row guard for the "
            "remaining M3 lock is asserted, so that implication is open "
            "rather than refuted"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"Hall K2,2 effective-hole/M3 ledger changed: {digest}")
    print("uniform strict Hall K2,2 effective-hole/M3 boundary: PASS")
    print("reverse-axis: ineffective complete hole; exact witness reselection")
    print("M3: bridge/off-anchor/kernel/complementary-wedge exits certified")
    print("remaining M3 interface: injective anchor-contained five-row lock")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
