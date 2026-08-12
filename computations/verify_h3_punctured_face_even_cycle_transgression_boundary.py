#!/usr/bin/env python3
"""Exact boundary for extending the punctured-C4 source certificate.

For two alternating matching products M,N and a two-site Hamming face,
the punctured functional

  D_Q = M_z Q_t - M_y Q_x + N_x Q_y - N_t Q_z

annihilates M+N.  Applied to complete target-augmented response rows it
therefore detects every other matching base Q.  The C4 proof succeeds when
all mixed faces of one third base vanish, leaving D_Q=M_z Q_t.

For the canonical C6 and C8 shortening base K=03|12|45|..., D_K has four
distinct signed monomials, not one.  Thus the same certificate does not isolate
the shortening chord without one further mixed-face routing/vanishing
input.  This checker freezes that exact obstruction and the topology census.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_c4_punctured_cube_alternate_target_lift.py":
        "15494dbdcf5d019d6fc858d2bad016a48dc966f63c672e739491a3692842c503",
    "notes/h3-c4-punctured-cube-alternate-target-lift.md":
        "fd6ae2e7be7c9f46ec3c8ff225dca54535daad24736b540a7aecd0ac4605cedf",
    "computations/verify_uniform_axis_k3_unequal_tail_reduction.py":
        "ef4c7bc9554fbf6fc5a65aef754d35359c46e0bb67014bd20060114a34cd1843",
    "notes/uniform-axis-k3-unequal-tail-reduction.md":
        "352e02a73da833fb159b24d581e7a91653fe195a76fbe3cc5aa531fd3e141993",
    "computations/verify_c4_base_exchange_connected_flat_propagation.py":
        "1e1b6ff1ae607b860330a6117f61045640b73f546275c36d4d62daff9ab6e383",
    "notes/c4-base-exchange-connected-flat-propagation.md":
        "9cf4b98c6ca5f9492c854aaf3c726b7eeb48a1294cfa7609a1b521b0df3e2eef",
}
EXPECTED_LEDGER_SHA256 = (
    "ca97e92948392f236fbf99f699f2210e5b94287b3a59f34968033bd755de3370"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge(left, right):
    return tuple(sorted((left, right)))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        remainder = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remainder):
            yield tuple(sorted(((first, second),) + tail))


def cycle_matchings(order):
    first = tuple(edge(site, site + 1) for site in range(0, order, 2))
    second = tuple(sorted(
        edge(site, (site + 1) % order) for site in range(1, order, 2)
    ))
    shortening = tuple(sorted(
        (edge(0, 3), edge(1, 2))
        + tuple(edge(site, site + 1) for site in range(4, order, 2))
    ))
    return first, second, shortening


def face_words(order):
    target = [1] * order
    x = target.copy()
    y = target.copy()
    z = target.copy()
    x[0] = z[0] = 0
    y[2] = z[2] = 2
    return tuple(map(tuple, (target, x, y, z)))


def variable(name):
    return Counter({(name,): 1})


def add(*scaled):
    result = Counter()
    for coefficient, value in scaled:
        for monomial, old in value.items():
            result[monomial] += coefficient * old
    return Counter({term: coefficient for term, coefficient in result.items()
                    if coefficient})


def multiply(left, right):
    result = Counter()
    for left_term, left_value in left.items():
        for right_term, right_value in right.items():
            result[tuple(sorted(left_term + right_term))] += (
                left_value * right_value
            )
    return Counter({term: coefficient for term, coefficient in result.items()
                    if coefficient})


def matching_product(matching, word):
    result = Counter({(): 1})
    for left, right in matching:
        result = multiply(result, variable(
            f"q{left}{right}_{word[left]}{word[right]}"
        ))
    return result


def transgression(first, second, candidate, words):
    target, x, y, z = words
    return add(
        (1, multiply(matching_product(first, z),
                     matching_product(candidate, target))),
        (-1, multiply(matching_product(first, y),
                      matching_product(candidate, x))),
        (1, multiply(matching_product(second, x),
                     matching_product(candidate, y))),
        (-1, multiply(matching_product(second, target),
                      matching_product(candidate, z))),
    )


def alternating_components(first, second):
    difference = set(first) ^ set(second)
    adjacency = {}
    for left, right in difference:
        adjacency.setdefault(left, []).append(right)
        adjacency.setdefault(right, []).append(left)
    unseen = set(adjacency)
    lengths = []
    while unseen:
        start = next(iter(unseen))
        previous = None
        current = start
        length = 0
        while True:
            unseen.discard(current)
            length += 1
            neighbours = adjacency[current]
            require(len(neighbours) == 2,
                    "a matching difference stopped being cycles")
            following = (neighbours[0] if neighbours[0] != previous
                         else neighbours[1])
            previous, current = current, following
            if current == start:
                break
        lengths.append(length)
    return tuple(sorted(lengths))


def monomial_text(polynomial):
    return [
        {"coefficient": coefficient, "variables": list(monomial)}
        for monomial, coefficient in sorted(polynomial.items())
    ]


def evaluate(polynomial, values):
    return sum(
        coefficient
        * product(values.get(variable_name, 1)
                  for variable_name in monomial)
        for monomial, coefficient in polynomial.items()
    )


def product(values):
    answer = 1
    for value in values:
        answer *= value
    return answer


def audit_order(order):
    first, second, shortening = cycle_matchings(order)
    words = face_words(order)
    trans_first = transgression(first, second, first, words)
    trans_second = transgression(first, second, second, words)
    require(not add((1, trans_first), (1, trans_second)),
            f"the punctured functional stopped annihilating M+N on C{order}")

    matchings = tuple(perfect_matchings(range(order)))
    topology = Counter()
    term_counts = Counter()
    no_c4_side = 0
    for candidate in matchings:
        if candidate in (first, second):
            continue
        left_type = alternating_components(first, candidate)
        right_type = alternating_components(candidate, second)
        topology[(left_type, right_type)] += 1
        if (4,) not in (left_type, right_type):
            no_c4_side += 1
        value = transgression(first, second, candidate, words)
        require(value, f"a C{order} third-base transgression vanished identically")
        term_counts[len(value)] += 1

    shortening_value = transgression(
        first, second, shortening, words
    )
    require(len(shortening_value) == 4,
            f"the C{order} shortening transgression stopped having four terms")
    target, _x, _y, _z = words
    pure_shortening = matching_product(shortening, target)
    require(evaluate(pure_shortening, {}) == 1,
            "the pure shortening monomial test changed")

    # Sharp local algebra guard: every displayed coefficient, both bridge
    # pivots, and the pure shortening monomial may be units while the signed
    # four-term shortening transgression cancels already at the all-one point.
    guard_values = {}
    require(evaluate(shortening_value, guard_values) == 0
            and evaluate(pure_shortening, guard_values) == 1,
            f"the C{order} two-term cancellation guard changed")

    return {
        "order": order,
        "third_matching_bases": len(matchings) - 2,
        "transgression_term_histogram": dict(sorted(term_counts.items())),
        "bases_with_no_C4_side": no_c4_side,
        "topology_histogram": {
            f"{left}|{right}": count
            for (left, right), count in sorted(topology.items())
        },
        "shortening_matching": shortening,
        "shortening_transgression": monomial_text(shortening_value),
        "shortening_terms": len(shortening_value),
        "cancellation_guard": {
            "D_K": 0,
            "K_target": 1,
            "all_displayed_variables": 1,
        },
    }


def audit_abstract_source_formula():
    # The complete response-row combination has the exact form
    # U*sum_Q D_Q = a2*M_z.  If one D_K=V*K_t survives with U,V,M_z,a2
    # localized, the pure K target monomial is forced.  This records the
    # sufficient theorem independently of the failed generic hypothesis.
    U, V, Kt, a2, Mz = map(
        variable, ("U", "V", "K_t", "a2", "M_z")
    )
    source = add((1, multiply(multiply(U, V), Kt)),
                 (-1, multiply(a2, Mz)))
    require(len(source) == 2,
            "the localized single-survivor source formula changed")
    return {
        "complete_row_formula": "U*sum_{Q!=M,N} D_Q=a2*M_z",
        "sufficient_hypotheses": [
            "one common endpoint-response block on t,x,y,z",
            "selected bridge words make M_z and the required face pivots units",
            "every D_Q except one shortening base K vanishes or enters a proved route",
            "D_K=V*K_t with V a localized unit (all mixed K faces vanish or route)",
        ],
        "conclusion": (
            "K_t is forced; if M triangle K is C4 it joins the flat base "
            "components, and otherwise K shortens the alternating cycle"
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
        "C6": audit_order(6),
        "C8": audit_order(8),
        "single_survivor_theorem": audit_abstract_source_formula(),
        "universal_identity": (
            "for every two matching products M,N, the two-site punctured "
            "functional annihilates M+N coefficientwise"
        ),
        "negative_verdict": (
            "the target-coloop certificate does not generically force a "
            "distance-three shortening chord: already on C6 the desired "
            "base has a four-term transgression, and four third bases have "
            "no C4 side to either input matching"
        ),
        "exact_next_input": (
            "route or kill the extra mixed face of the shortening base and "
            "all competing D_Q in the same endpoint grade; equivalently, "
            "prove a first-transgression selection theorem from the unary "
            "and companion rows"
        ),
        "scope": (
            "exact source-row functional and C6/C8 matching-base boundary; "
            "the cancellation assignment is a local coefficient guard, "
            "not a full unary/four-response source packet"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the even-cycle transgression ledger changed: {digest}")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")
    print("h3 punctured-face even-cycle transgression boundary: PASS")


if __name__ == "__main__":
    main()
