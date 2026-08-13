#!/usr/bin/env python3
"""Test L01 against the full native linear Spencer orbit of the K8 response.

Let R be the hafnian response in the 28 independent edge coefficients.  The
degree-preserving filtered differential operators of order below two are
spanned by R itself and all 28^2 operators x_y partial_x R.  Extend the
primitive twelve-occurrence L01 covector by zero to every nonmatching or
collision degree-four monomial.  It annihilates all 784 first-order outputs
and R, but reads one on the required second-order chart symbol

  2 D q01 partial_D partial_q01
  - p0 s1 partial_p0 partial_s1
  - p1 s0 partial_p1 partial_s0.

Thus no lower-order, including non-diagonal, Spencer correction makes the
desired symbol tangent.  A new source/Tate generator is required.  The
coefficient dual is not yet an accepted augmented terminal because the
physical same-grade map containing such generators has not been constructed
or proved exhaustive.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_uc4_three_cap_l01_terminal_scope.py":
        "dc0aee4c430c35cb9f0deff9b0949e6dede906a444adae2e11302f1e9dcba5b8",
    "notes/h3-uc4-three-cap-l01-terminal-scope.md":
        "7a00c2fe809251a7230fb3cb4ae2e0fd59e0ea60ed419e434e343828c953b7e2",
    "computations/verify_h3_o2_augmented_terminal_cap_cartan_extension_gate.py":
        "8a9bfe47c934658d1b10ad42f283d6a017c27125bcb98615882e4bacd975f1eb",
    "notes/h3-o2-augmented-terminal-cap-cartan-extension-gate.md":
        "e9c0cf3c76cbe4c8061574d2b977bf1189a1fa299ef17ae1d2e463c08a313429",
}
EXPECTED_LEDGER_SHA256 = "995d2fbce55900adfe016058b4db013eefb8049a55e40ab932cba29082a1dfca"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def edge(left: int, right: int) -> tuple[int, int]:
    return min(left, right), max(left, right)


EDGES = tuple((left, right) for left in range(8)
              for right in range(left + 1, 8))
EDGE_INDEX = {value: index for index, value in enumerate(EDGES)}
P, S = 6, 7


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted((edge(first, second),) + tail))


MATCHINGS = tuple(sorted(set(perfect_matchings(range(8)))))
MATCHING_MONOMIALS = tuple(tuple(sorted(EDGE_INDEX[value] for value in matching))
                           for matching in MATCHINGS)
MATCHING_SET = frozenset(MATCHING_MONOMIALS)


def matching(*pairs):
    return tuple(sorted(EDGE_INDEX[edge(left, right)] for left, right in pairs))


def add_to(answer, monomial, coefficient):
    answer[monomial] = answer.get(monomial, Q(0)) + Q(coefficient)
    if answer[monomial] == 0:
        del answer[monomial]


def apply_first_order(y, x):
    answer = {}
    for monomial in MATCHING_MONOMIALS:
        if x not in monomial:
            continue
        result = list(monomial)
        result.remove(x)
        result.append(y)
        add_to(answer, tuple(sorted(result)), 1)
    return answer


def apply_second_order(multiplier, derivatives):
    answer = {}
    left, right = derivatives
    require(left != right, "only distinct squarefree derivatives are used")
    for monomial in MATCHING_MONOMIALS:
        if left not in monomial or right not in monomial:
            continue
        result = list(monomial)
        result.remove(left)
        result.remove(right)
        result.extend(multiplier)
        add_to(answer, tuple(sorted(result)), 1)
    return answer


def scale(coefficient, vector):
    return {monomial: Q(coefficient) * value
            for monomial, value in vector.items() if coefficient * value}


def add(*vectors):
    answer = {}
    for vector in vectors:
        for monomial, coefficient in vector.items():
            add_to(answer, monomial, coefficient)
    return answer


def pairing(dual, vector):
    return sum((dual.get(monomial, Q(0)) * coefficient
                for monomial, coefficient in vector.items()), Q(0))


def l01_dual():
    records = (
        (Q(1, 3), matching((P, S), (0, 1), (2, 3), (4, 5))),
        (Q(-1, 3), matching((P, S), (0, 3), (1, 4), (2, 5))),
        (Q(-1, 3), matching((P, S), (0, 5), (1, 2), (3, 4))),
        (Q(1, 3), matching((P, S), (0, 5), (1, 4), (2, 3))),
        (Q(-1, 3), matching((P, 0), (S, 1), (2, 3), (4, 5))),
        (Q(1, 3), matching((P, 0), (S, 1), (2, 5), (3, 4))),
        (Q(-1, 3), matching((P, 0), (S, 2), (1, 3), (4, 5))),
        (Q(1, 3), matching((P, 0), (S, 3), (1, 2), (4, 5))),
        (Q(-1, 3), matching((P, 1), (S, 0), (2, 3), (4, 5))),
        (Q(1, 3), matching((P, 1), (S, 2), (0, 3), (4, 5))),
        (Q(1, 3), matching((P, 2), (S, 0), (1, 3), (4, 5))),
        (Q(-1, 3), matching((P, 2), (S, 3), (0, 1), (4, 5))),
    )
    answer = {monomial: coefficient for coefficient, monomial in records}
    require(len(answer) == 12 and all(monomial in MATCHING_SET
                                      for monomial in answer),
            "the primitive L01 support changed")
    return answer


def desired_second_order_symbol():
    d = EDGE_INDEX[edge(P, S)]
    q01 = EDGE_INDEX[edge(0, 1)]
    p0 = EDGE_INDEX[edge(P, 0)]
    s1 = EDGE_INDEX[edge(S, 1)]
    p1 = EDGE_INDEX[edge(P, 1)]
    s0 = EDGE_INDEX[edge(S, 0)]
    return add(
        scale(2, apply_second_order((d, q01), (d, q01))),
        scale(-1, apply_second_order((p0, s1), (p0, s1))),
        scale(-1, apply_second_order((p1, s0), (p1, s0))),
    )


def expected_l01():
    answer = {}
    residuals = (((2, 3), (4, 5)),
                 ((2, 4), (3, 5)),
                 ((2, 5), (3, 4)))
    charts = (
        (2, ((P, S), (0, 1))),
        (-1, ((P, 0), (S, 1))),
        (-1, ((P, 1), (S, 0))),
    )
    for coefficient, prefix in charts:
        for tail in residuals:
            add_to(answer, matching(*(prefix + tail)), coefficient)
    return answer


def audit_native_spencer() -> dict[str, object]:
    require(len(EDGES) == 28 and len(MATCHINGS) == 105,
            (len(EDGES), len(MATCHINGS)))
    dual = l01_dual()
    response = {monomial: Q(1) for monomial in MATCHING_MONOMIALS}
    require(pairing(dual, response) == 0,
            "the L01 dual stopped killing the response")

    first_order_nonzero = 0
    first_order_matching_outputs = 0
    pairings = []
    output_support = set()
    for y in range(len(EDGES)):
        for x in range(len(EDGES)):
            vector = apply_first_order(y, x)
            if vector:
                first_order_nonzero += 1
            output_support.update(vector)
            if any(monomial in MATCHING_SET for monomial in vector):
                first_order_matching_outputs += 1
            pairings.append(pairing(dual, vector))
    require(first_order_nonzero == 28 * 28
            and first_order_matching_outputs == 28
            and all(value == 0 for value in pairings),
            (first_order_nonzero, first_order_matching_outputs,
             set(pairings)))

    desired = desired_second_order_symbol()
    l01 = expected_l01()
    require(desired == l01 and len(l01) == 9
            and pairing(dual, desired) == 1,
            "the desired second-order Spencer curvature changed")
    matching_outputs = sum(monomial in MATCHING_SET
                           for monomial in output_support)
    collision_outputs = len(output_support) - matching_outputs
    return {
        "coefficient_variables": len(EDGES),
        "complete_response_occurrences": len(MATCHINGS),
        "native_degree_preserving_first_order_operators": len(pairings),
        "all_first_order_pairings_with_extended_dual": 0,
        "first_order_outputs_in_matching_block": matching_outputs,
        "first_order_nonmatching_or_collision_outputs": collision_outputs,
        "only_diagonal_first_order_operators_return_to_matching_block": (
            first_order_matching_outputs
        ),
        "dual_extension": (
            "psi01 on the 105 perfect-matching monomials and zero on every "
            "nonmatching/collision degree-four monomial"
        ),
        "desired_order_two_operator": (
            "2 D q01 partial_D partial_q01 - p0 s1 partial_p0 partial_s1 "
            "- p1 s0 partial_p1 partial_s0"
        ),
        "desired_output": "L01, nine matching occurrences",
        "dual_value_on_desired_output": str(pairing(dual, desired)),
        "filtered_consequence": (
            "every degree-preserving correction of order below two is in the "
            "tested scalar plus 784-dimensional linear-operator span; it is "
            "annihilated by psi01, so it cannot cancel L01 without changing "
            "the prescribed order-two principal symbol"
        ),
    }


def audit_terminal_scope() -> dict[str, object]:
    return {
        "native_coefficient_Spencer_nonfill": True,
        "accepted_augmented_physical_terminal": False,
        "reason": (
            "the native coefficient Spencer orbit is not the exhaustive "
            "physical source map: arbitrary non-diagonal coefficient moves "
            "lack word/fine/repeated and target/q/anchor/ridge provenance, "
            "while a Tate/collision generator can have nonzero psi01 pairing"
        ),
        "two_exact_completions_of_current_native_map": {
            "nonfill_completion": (
                "retain only the scalar and all 784 first-order native "
                "Spencer outputs; psi01 is a coefficient cokernel dual"
            ),
            "fill_completion": (
                "adjoin one source-labelled column with boundary L01; the "
                "candidate is then in the image"
            ),
            "known_lower_order_data_distinguishes_them": False,
        },
        "conditional_augmented_extension_after_placement": (
            "for the induced cap-corner values mu_j, set q=ainc=Eq=0, "
            "target_j=W_j=-mu_j, ores_j=mu_j, and "
            "ridge=-sum alpha_j mu_j; then exact duality gives protected "
            "filler or augmented terminal"
        ),
        "first_missing_physical_object": (
            "a source-labelled Tate/Spencer generator for the L01 curvature, "
            "equivalently the covariant three-cap/C+ totalization with its "
            "collision, word/fine/repeated and augmented proper faces"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 L01 full linear Spencer dual and terminal gate",
        "pins": PINS,
        "full_native_filtered_order_below_two": audit_native_spencer(),
        "physical_terminal_scope": audit_terminal_scope(),
        "verdict": (
            "The full degree-preserving non-diagonal linear Spencer orbit "
            "does not repair L01.  The twelve-occurrence dual extends by zero "
            "over every nonmatching/collision monomial and annihilates all "
            "784 first-order operators.  The prescribed order-two chart "
            "symbol evaluates exactly to L01 and has dual value one, so no "
            "lower-order Spencer correction makes it tangent.  A new physical "
            "Tate/source generator is necessary.  The dual is a complete "
            "native-coefficient nonfill certificate but not yet an accepted "
            "augmented terminal, because the source-labelled same-grade map "
            "containing possible Tate/collision columns is not exhaustive."
        ),
        "scope": (
            "exact K8 degree-four filtered differential-operator calculation "
            "through order two and exact terminal nonpromotion guard.  It "
            "does not rule out the missing higher source-labelled Tate cell."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("L01 full linear Spencer ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 == "TO_BE_FROZEN":
        print("freeze EXPECTED_LEDGER_SHA256=" + digest)
        return
    print("native non-diagonal first-order Spencer operators: 784")
    print("extended psi01 pairing on every operator: ZERO")
    print("desired order-two chart symbol: L01")
    print("psi01(L01): ONE")
    print("new physical Tate/source generator: REQUIRED")
    print("accepted augmented terminal: NOT YET EXHAUSTIVE")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
