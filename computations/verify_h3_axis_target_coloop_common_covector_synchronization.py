#!/usr/bin/env python3
"""Synchronize two one-sided minors by one output covector in char zero.

After the proportional branch is removed, fix the selected mixed-word
functional d.  Each endpoint pair defines a nonzero linear functional on
the common output dual,

    f_P(e)=det(P(d),P(e)),  f_S(e)=det(S(d),S(e)).

The union of their two kernels cannot cover a vector space over Q/C.  More
constructively, if e_P and e_S witness the two minors separately, one of
e_P+c e_S for c=0,1,2 witnesses both.  Contracting complete source tensors
with this covector is a literal linear combination of coefficient rows, so
the resulting common two-output Fitting carrier is source-valid.

The checker also freezes the sharp grading caveat: two pairs can have
disjoint literal-word Pluecker supports even though their common covector
exists.  Thus this theorem does not manufacture one matching-grade word.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_axis_target_coloop_proportional_nu_safe_reduction.py":
        "6f27d3585fdc4708026ab6fef6134295dd874f83bb43fd1f480b7314362c56f3",
    "notes/h3-axis-target-coloop-proportional-nu-safe-reduction.md":
        "8e9ba2c477be06a022f1c86f334d45a95b1ff7d9393b7134c6f38aa21d797f14",
    "computations/verify_h3_axis_target_coloop_one_sided_companion_boundary.py":
        "6cb34278cccf9327bdfccdece0b254f3eff95d179e512e80e1c938d4fe0eef62",
    "notes/h3-axis-target-coloop-one-sided-companion-boundary.md":
        "ce93379f949002eaf05f24975b902760d9dcd7095e4150bf132259c73a498393",
    "computations/verify_uniform_five_lock_wedge_or_switch.py":
        "c2541a60db1f8e7a661bc698d2bd1f1a1f396a0f0bfde389ea89bea17fac175e",
    "notes/uniform-five-lock-wedge-or-switch.md":
        "0871d5151a0fdb46fee0c9b15797a864e579a85c360a2638d458583479426914",
}
EXPECTED_LEDGER_SHA256 = (
    "c8ed7d47ea898868ee08211395946d648e5910daef8912e7007e134f1c445c9f"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def add(left, right, scalar=Q(1)):
    return tuple(a + scalar * b for a, b in zip(left, right, strict=True))


def evaluate(covector, vector):
    return sum(a * b for a, b in zip(covector, vector, strict=True))


def minor(first, second, left_covector, right_covector):
    return (evaluate(left_covector, first)
            * evaluate(right_covector, second)
            - evaluate(left_covector, second)
            * evaluate(right_covector, first))


def pluecker(first, second):
    return {
        pair: first[pair[0]] * second[pair[1]]
        - first[pair[1]] * second[pair[0]]
        for pair in combinations(range(len(first)), 2)
    }


def synchronize(first_pair, second_pair, d, e_first, e_second):
    first_functional = lambda e: minor(
        first_pair[0], first_pair[1], d, e)
    second_functional = lambda e: minor(
        second_pair[0], second_pair[1], d, e)
    require(first_functional(e_first) != 0,
            "the first endpoint witness vanished")
    require(second_functional(e_second) != 0,
            "the second endpoint witness vanished")
    candidates = []
    for scalar in map(Q, (0, 1, 2)):
        covector = add(e_first, e_second, scalar)
        values = (first_functional(covector),
                  second_functional(covector))
        candidates.append((scalar, covector, values))
    common = next((candidate for candidate in candidates
                   if candidate[2][0] and candidate[2][1]), None)
    require(common is not None,
            "three characteristic-zero covectors missed two hyperplanes")
    return common, candidates


def audit_separated_literal_words():
    # Coordinates are d,e_P,e_S,r.  P has only Pluecker slot d^e_P and S
    # only d^e_S.  No literal coordinate pair witnesses both.
    p_pair = ((Q(1), Q(1), Q(0), Q(0)),
              (Q(1), Q(0), Q(0), Q(0)))
    s_pair = ((Q(1), Q(0), Q(1), Q(0)),
              (Q(1), Q(0), Q(0), Q(0)))
    d = (Q(1), Q(0), Q(0), Q(0))
    e_p = (Q(0), Q(1), Q(0), Q(0))
    e_s = (Q(0), Q(0), Q(1), Q(0))
    p_pluecker = pluecker(*p_pair)
    s_pluecker = pluecker(*s_pair)
    p_support = {pair for pair, value in p_pluecker.items() if value}
    s_support = {pair for pair, value in s_pluecker.items() if value}
    require(p_support == {(0, 1)} and s_support == {(0, 2)}
            and not p_support & s_support,
            "the separated literal-word minor guard changed")
    common, candidates = synchronize(p_pair, s_pair, d, e_p, e_s)
    scalar, covector, values = common
    require(scalar == 1 and covector == (Q(0), Q(1), Q(1), Q(0))
            and values == (Q(-1), Q(-1)),
            "the canonical common covector changed")
    return {
        "output_basis": ["d", "e_P", "e_S", "r"],
        "P_literal_pluecker_support": [list(pair) for pair in p_support],
        "S_literal_pluecker_support": [list(pair) for pair in s_support],
        "common_literal_word_pair": False,
        "chosen_common_covector": [str(value) for value in covector],
        "chosen_scalar_in_eP+c_eS": str(scalar),
        "common_minor_values": [str(value) for value in values],
        "candidate_values": [
            {"c": str(candidate_scalar),
             "P_minor": str(candidate_values[0]),
             "S_minor": str(candidate_values[1])}
            for candidate_scalar, _candidate_covector, candidate_values
            in candidates
        ],
    }


def audit_characteristic_zero_selection():
    # A finite palette with arbitrary rational affine functionals.  It pins
    # the constructive "at most two bad scalars" proof, including cases in
    # which one witness already works for both endpoints.
    audits = []
    d = (Q(1), Q(0), Q(0), Q(0))
    samples = (
        (((1, 1, 0, 0), (1, 0, 0, 0)),
         ((1, 0, 1, 0), (1, 0, 0, 0)), 1, 2),
        (((2, -1, 3, 0), (1, 2, 0, 1)),
         ((1, 4, -2, 1), (3, 0, 1, -1)), 1, 3),
        (((1, 2, 4, 1), (2, -1, 1, 3)),
         ((3, 1, 2, -2), (1, 0, -1, 4)), 2, 1),
    )
    basis = tuple(tuple(Q(int(index == column)) for index in range(4))
                  for column in range(4))
    for first_pair_raw, second_pair_raw, first_witness, second_witness in samples:
        first_pair = tuple(tuple(map(Q, vector)) for vector in first_pair_raw)
        second_pair = tuple(tuple(map(Q, vector)) for vector in second_pair_raw)
        e_first, e_second = basis[first_witness], basis[second_witness]
        # If the nominated basis vector is accidentally zero, choose the
        # first actual witness; this keeps the palette about the theorem,
        # not a fragile sample coordinate.
        if minor(*first_pair, d, e_first) == 0:
            e_first = next(vector for vector in basis
                           if minor(*first_pair, d, vector))
        if minor(*second_pair, d, e_second) == 0:
            e_second = next(vector for vector in basis
                            if minor(*second_pair, d, vector))
        common, candidates = synchronize(
            first_pair, second_pair, d, e_first, e_second)
        bad = sum(not (values[0] and values[1])
                  for _scalar, _covector, values in candidates)
        require(bad <= 2,
                "two hyperplanes excluded all three rational scalars")
        audits.append({
            "bad_scalars_among_0_1_2": bad,
            "selected_scalar": str(common[0]),
            "selected_minor_values": [str(value) for value in common[2]],
        })
    return audits


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def main():
    pin_dependencies()
    ledger = {
        "pins": PINS,
        "separated_literal_word_guard": audit_separated_literal_words(),
        "characteristic_zero_palette": audit_characteristic_zero_selection(),
        "theorem": (
            "let d be the selected mixed-word covector and suppose the P "
            "and S one-sided pairs each have a nonzero minor involving d. "
            "Their determinant maps f_P,f_S on the common output dual are "
            "nonzero linear functionals.  If e_P,e_S witness them "
            "separately, one of e_P+c*e_S for c=0,1,2 lies outside both "
            "kernels and supplies a common two-output Fitting quotient"
        ),
        "source_validity": (
            "the complete response equations are tensor equalities.  "
            "Contracting them with e_P+c*e_S is an exact linear combination "
            "of literal coefficient rows, so no Ward derivative, division, "
            "or termwise matching cancellation is assumed"
        ),
        "downstream_scope": (
            "a nonzero contraction certifies the corresponding physical "
            "cofactor tensor/activity and is sufficient for a coordinate-"
            "free Fitting carrier.  It does not supply a single matching-"
            "grade word, a distinct-head wedge, deleted-star rank three, "
            "or the missing alternate bright target matching"
        ),
        "remaining_physical_gate": (
            "route the common-covector bistar/Fitting carrier to an actual "
            "rank-restoring crossed response base or show that the full "
            "five-row packet gives an anchor-safe same-star dependence"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"common-covector synchronization ledger changed: {digest}")
    print("h3 target-coloop common-covector synchronization: PASS")
    print("two nonzero determinant maps -> one common output covector")
    print("literal common word can fail; tensor/Fitting carrier still exact")
    print("remaining gate: rank-restoring crossed response provenance")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
