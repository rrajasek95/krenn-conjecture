#!/usr/bin/env python3
"""Common-covector synchronization and the strict-K2,2 scope boundary.

Two nonzero minor forms on the mixed zero-row space always admit a common
rational covector outside both kernels.  Thus different literal witnessing
word pairs do not obstruct a common two-dimensional Fitting quotient.

This does not put the target-coloop residual in the endpoint-support-complete
strict K2,2 chart.  That chart localizes two pure matchings in the selected
bright colour; the second avoids the chosen target arm and is already an
alternate target matching.  The canonical smallest no-cross union has only
M,N and the unary K, so those factors are absent.

The checker also proves that the canonical three-matching union cannot be
the whole physical support.  All three bases contain edge 45, so the full
H8 tensor factors across 45 | complement.  Three literal GHZ coefficients
give a four-row integral unit certificate.  Any physical source over that
selected triple must therefore introduce a fourth matching/new edge.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_axis_target_coloop_one_sided_companion_boundary.py":
        "6cb34278cccf9327bdfccdece0b254f3eff95d179e512e80e1c938d4fe0eef62",
    "notes/h3-axis-target-coloop-one-sided-companion-boundary.md":
        "ce93379f949002eaf05f24975b902760d9dcd7095e4150bf132259c73a498393",
    "computations/verify_uniform_hall_terminal_transfer_bistar_curvature_boundary.py":
        "aa1da69a09c3c34f90024a42b27ab0d0a30b0c1263a6a059d256ff085084c048",
    "notes/uniform-hall-terminal-transfer-bistar-curvature-boundary.md":
        "07523ffcef85b86c0b0808ddec43f1731c99f4426451f0e22171f864e82949aa",
    "computations/verify_uniform_hall_k22_outside_endpoint_component_wedge.py":
        "59dd21c4664e8ccd88f771d0191d3db32e5fdb832e2c6de1f169cb197f9a3038",
    "notes/uniform-hall-k22-outside-endpoint-component-wedge.md":
        "cd3807d8f3f4f3d8ccda38e23c5ff291d3f0e3f1a33b69f3d2ef061b117d3347",
}
EXPECTED_LEDGER_SHA256 = (
    "e77f24f4ea7ee6a5199947dec2fe5a77d9e12756123b33916a90de637eee7bc0"
)


P, S = 6, 7


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge(left, right):
    return tuple(sorted((left, right)))


def dot(form, vector):
    return sum((left * right for left, right in zip(form, vector, strict=True)),
               Q(0))


def audit_common_covector_lemma():
    # Exhaust the nonzero forms with coefficients -1,0,1 on a four-word
    # mixed subspace.  A small rational candidate set meets the complement
    # of both kernels in every case.  The human proof is the usual
    # "an infinite vector space is not the union of two hyperplanes".
    forms = tuple(tuple(Q(value) for value in values)
                  for values in product((-1, 0, 1), repeat=4)
                  if any(values))
    candidates = tuple(tuple(Q(value) for value in values)
                       for values in product((-2, -1, 0, 1, 2), repeat=4)
                       if any(values))
    witness_histogram = {}
    audits = 0
    for first in forms:
        for second in forms:
            witness = next((vector for vector in candidates
                            if dot(first, vector) and dot(second, vector)),
                           None)
            require(witness is not None,
                    "two nonzero rational forms covered the mixed space")
            support = sum(bool(value) for value in witness)
            witness_histogram[support] = witness_histogram.get(support, 0) + 1
            audits += 1
    require(audits == len(forms) ** 2 == 6400,
            "the common-covector audit count changed")
    return {
        "mixed_space_dimension": 4,
        "nonzero_forms": len(forms),
        "ordered_form_pairs": audits,
        "candidate_covectors": len(candidates),
        "witness_support_histogram": witness_histogram,
        "consequence": (
            "if Delta_P(d,-) and Delta_S(d,-) are nonzero on the mixed "
            "zero-row space, one rational mixed coefficient combination "
            "makes both minors nonzero on the common quotient span(d,ell)"
        ),
        "target_coordinate_split": (
            "if either minor form vanishes on every mixed zero row, its "
            "rank-two witness uses a nonzero target coordinate and belongs "
            "to the alternate-target/affine-line branch instead"
        ),
    }


def perfect_matching(*pairs):
    matching = tuple(sorted(edge(*pair) for pair in pairs))
    require(len({site for pair in matching for site in pair})
            == 2 * len(matching), f"not a matching: {matching}")
    return matching


def audit_strict_k22_requires_alternate_target():
    # The endpoint-support-complete opposite-shore chart used by 79907d3.
    unary = perfect_matching((P, S), (0, 1), (2, 4), (3, 5))
    colour1_left = perfect_matching((P, 0), (S, 1), (2, 3), (4, 5))
    colour1_right = perfect_matching((P, 3), (S, 2), (0, 1), (4, 5))
    colour2_left = perfect_matching((P, 2), (S, 0), (1, 3), (4, 5))
    colour2_right = perfect_matching((P, 1), (S, 3), (0, 2), (4, 5))
    families = ((colour1_left, colour1_right),
                (colour2_left, colour2_right))
    for family in families:
        require(not set(family[0]) & {edge(P, 3), edge(S, 2)}
                or family is families[1],
                "the strict family audit changed")
        require(edge(P, 0) not in family[1]
                if family is families[0] else edge(P, 2) not in family[1],
                "the second strict matching stopped avoiding the first P arm")
        require(edge(S, 1) not in family[1]
                if family is families[0] else edge(S, 0) not in family[1],
                "the second strict matching stopped avoiding the first S arm")

    # Normalize the coloop target to the first strict colour.  If both
    # endpoint-support-complete target monomials are localized, the right
    # matching is literally an alternate pure target avoiding either arm.
    require(colour1_left != colour1_right
            and edge(P, 0) not in colour1_right
            and edge(S, 1) not in colour1_right,
            "strict endpoint completion stopped breaking target coloopness")
    return {
        "unary": unary,
        "strict_colour1_family": list(families[0]),
        "strict_colour2_family": list(families[1]),
        "selected_target": colour1_left,
        "alternate_same_colour_target": colour1_right,
        "coloop_consequence": (
            "localizing both same-colour strict core monomials already "
            "supplies a pure target matching avoiding the selected P0/S1 arm"
        ),
        "scope": (
            "the 79907d3 source-unit identities apply after endpoint-support "
            "completion; they cannot be used to manufacture the missing "
            "alternate same-colour matching inside a target-coloop branch"
        ),
    }


# Sparse polynomials over Z for the literal common-edge unit.
def add(*signed):
    answer = {}
    for polynomial, scalar in signed:
        for monomial, coefficient in polynomial.items():
            answer[monomial] = answer.get(monomial, 0) + scalar * coefficient
    return {monomial: coefficient for monomial, coefficient in answer.items()
            if coefficient}


def multiply(*polynomials):
    answer = {(): 1}
    for polynomial in polynomials:
        updated = {}
        for left, left_value in answer.items():
            for right, right_value in polynomial.items():
                monomial = tuple(sorted(left + right))
                updated[monomial] = (updated.get(monomial, 0)
                                     + left_value * right_value)
        answer = updated
    return answer


def variable(name):
    return {(name,): 1}


def constant(value):
    return {(): value} if value else {}


def audit_canonical_three_base_unit():
    target = perfect_matching((P, 0), (S, 1), (2, 3), (4, 5))
    outside = perfect_matching((0, 1), (P, 2), (S, 3), (4, 5))
    unary = perfect_matching((P, S), (0, 1), (2, 3), (4, 5))
    common = set(target) & set(outside) & set(unary)
    require(common == {edge(4, 5)},
            "the canonical three-base common edge changed")

    # If these are all supported matchings, the full tensor is Q45*G on the
    # bipartition {4,5}|{0,1,2,3,P,S}.  Use the pure-zero and pure-one target
    # rows plus one mixed zero row.  The displayed combination is 1.
    q00, q11, g0, g1 = map(variable, ("q00", "q11", "g0", "g1"))
    pure0 = add((multiply(q00, g0), 1), (constant(1), -1))
    pure1 = add((multiply(q11, g1), 1), (constant(1), -1))
    mixed = multiply(q00, g1)
    certificate = add(
        (multiply(g0, q11, mixed), 1),
        (multiply(g0, q00, pure1), -1),
        (pure0, -1),
    )
    require(certificate == constant(1),
            f"the common-edge GHZ unit certificate changed: {certificate}")
    return {
        "M": target,
        "N": outside,
        "K_unary": unary,
        "common_physical_edge": edge(4, 5),
        "factorization_if_support_complete": "H8=Q45 tensor G6",
        "literal_rows": [
            "q00*g0-1 (pure 0^8)",
            "q11*g1-1 (pure 1^8)",
            "q00*g1 (45 coloured 00, complement coloured 1)",
        ],
        "integral_unit_identity": (
            "g0*q11*(q00*g1)-g0*q00*(q11*g1-1)-(q00*g0-1)=1"
        ),
        "consequence": (
            "the canonical three-matching union cannot be the whole physical "
            "support; a support-minimal full source needs a fourth matching "
            "and hence an edge outside M union N union K"
        ),
    }


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def main():
    pin_dependencies()
    ledger = {
        "pins": PINS,
        "common_mixed_covector": audit_common_covector_lemma(),
        "strict_k22_scope": audit_strict_k22_requires_alternate_target(),
        "canonical_smallest_full_support_unit":
            audit_canonical_three_base_unit(),
        "verdict": (
            "different literal minor witnesses can be synchronized on one "
            "rational mixed output covector, so separated word supports are "
            "not an abstract Fitting obstruction.  But the 50 no-cross "
            "residuals are not automatically the endpoint-support-complete "
            "strict K2,2 chart: its missing localized same-colour matching "
            "is already an alternate target.  The canonical smallest union "
            "is itself full-support impossible by a literal common-edge unit"
        ),
        "extra_component_route": (
            "an extra endpoint component is covered by 7114577 when its "
            "complete column is nonzero, and is exactly deletable when zero. "
            "An extra internal q edge must participate in a fourth matching "
            "at support minimum; routing that new base is the remaining gate"
        ),
        "scope": (
            "common-covector/Fitting synchronization, exact 79907d3 "
            "hypothesis audit, and one canonical full-H8 unit.  It does not "
            "claim all 50 unions have a common physical edge or that a "
            "generic fourth internal matching is already crossed/four-good"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"common-covector K2,2 scope ledger changed: {digest}")
    print("h3 target-coloop common-covector / strict-K2,2 scope: PASS")
    print("two nonzero mixed minor forms -> one common rational covector")
    print("strict K2,2 completion -> alternate same-colour target")
    print("canonical 3-base support -> literal common-edge source unit")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
