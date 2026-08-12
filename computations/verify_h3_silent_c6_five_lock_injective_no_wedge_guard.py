#!/usr/bin/env python3
"""Exact injective/no-wedge boundary for the silent diagonal C6 lock.

The unary and four response zero fibres frozen by b80b064 do not force a
same-star kernel or a complementary crossed wedge.  A rational common-q
specialization with q13=q04=0 has four natural two-cell attachment windows.
On each window the complete five-tensor finite-difference lock is diagonal:
one direction is detected by the unary pure-zero coefficient and the other
by one diagonal response coefficient.  Both crossed response locks vanish.

This is a source-provenant zero-fibre guard, not a full one-bad point: its
bright X1 and X2 diagonal response tensors are absent.  It pins those bright
rows/star completions as the first additional data needed to close the C6.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SWITCH_PATH = (
    "computations/verify_uniform_diagonal_alternating_cycle_switch_boundary.py"
)
PINS = {
    "computations/verify_h3_four_base_silent_c6_response_lock.py":
        "dc4daa2d200f184b5d00d29c4db175320935a189f5590836afa0c724d3fdac8a",
    "notes/h3-four-base-silent-c6-response-lock.md":
        "54d7278e49e8195ed2262fa37cc89936f718b3bcd192884c6473c736a68354b8",
    "computations/verify_uniform_five_lock_wedge_or_switch.py":
        "c2541a60db1f8e7a661bc698d2bd1f1a1f396a0f0bfde389ea89bea17fac175e",
    "notes/uniform-five-lock-wedge-or-switch.md":
        "0871d5151a0fdb46fee0c9b15797a864e579a85c360a2638d458583479426914",
    SWITCH_PATH:
        "f99c185403bf2e86b7352c555cd02d85bfed0df668b8a87b44a725c3db7edc71",
    "notes/uniform-diagonal-alternating-cycle-switch-boundary.md":
        "1e5b1a530d782ff03805b293ccfc3e6d76db6f046c8d8ffd4224ed3f9725f9e8",
}
EXPECTED_LEDGER_SHA256 = (
    "cf1f90c7da2a5d3122e27d3b5a264e29df859372ef786d485bb423e12ea9c6ad"
)
SITES = tuple(range(6))
PURE_ZERO = (0,) * 6


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_switch():
    spec = spec_from_file_location("silent_c6_switch", ROOT / SWITCH_PATH)
    require(spec is not None and spec.loader is not None,
            "cannot load the same-star switch dependency")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def tensor_add(left, right, scalar=Q(1)):
    answer = Counter(left)
    for key, value in right.items():
        answer[key] += scalar * value
        if not answer[key]:
            del answer[key]
    return answer


def tensor_scale(scalar, tensor):
    return Counter({key: scalar * value for key, value in tensor.items()
                    if scalar * value})


def matrix_rank(columns):
    keys = sorted(set().union(*(set(column) for column in columns)), key=str)
    matrix = [[Q(column.get(key, 0)) for column in columns] for key in keys]
    row = 0
    for column in range(len(columns)):
        pivot = next((index for index in range(row, len(matrix))
                      if matrix[index][column]), None)
        if pivot is None:
            continue
        matrix[row], matrix[pivot] = matrix[pivot], matrix[row]
        value = matrix[row][column]
        matrix[row] = [entry / value for entry in matrix[row]]
        for index in range(len(matrix)):
            if index == row or not matrix[index][column]:
                continue
            value = matrix[index][column]
            matrix[index] = [entry - value * pivot_entry
                             for entry, pivot_entry
                             in zip(matrix[index], matrix[row], strict=True)]
        row += 1
    return row


def labelled_lock_column(switch, q, endpoints, direction):
    column = Counter()
    for word, value in switch.inserted_edge_tensor(q, direction, SITES).items():
        column[("top", word)] += value
    for name, p, s in endpoints:
        response = switch.response_with_inserted_edge(
            q, p, s, direction, SITES
        )
        for word, value in response.items():
            column[(name, word)] += value
    return Counter({key: value for key, value in column.items() if value})


def audit():
    pin_dependencies()
    switch = load_switch()

    # All thirteen displayed cells are nonzero.  The missing physical tables
    # are exactly q04 and q13.  The five base values A,B,K,L,R are nonzero,
    # while the complete pure-zero hafnian is normalized to one.
    weights = {
        (0, 1): Q(-2), (0, 2): Q(1), (0, 3): Q(1), (0, 5): Q(1),
        (1, 2): Q(1), (1, 4): Q(-3), (1, 5): Q(1),
        (2, 3): Q(-1), (2, 4): Q(-1), (2, 5): Q(1),
        (3, 4): Q(2), (3, 5): Q(1), (4, 5): Q(1),
    }
    require((0, 4) not in weights and (1, 3) not in weights,
            "a forbidden C6 chord entered the specialization")
    q = {switch.cell(left, right, 0, 0): value
         for (left, right), value in weights.items()}

    p1 = ((0, 1, Q(1)),)
    s1 = ((1, 1, Q(1)),)
    p2 = ((3, 2, Q(1)),)
    s2 = ((4, 2, Q(1)),)
    endpoints = (
        ("G11", p1, s1), ("G12", p1, s2),
        ("G21", p2, s1), ("G22", p2, s2),
    )

    top = switch.matchings(q, SITES)
    responses = {
        name: switch.response(q, p, s, SITES)
        for name, p, s in endpoints
    }
    require(top == Counter({PURE_ZERO: Q(1)}),
            "the rational specialization lost q^[3]=X0")
    require(all(not tensor for tensor in responses.values()),
            "one of the four frozen response zero fibres became nonzero")

    bases = {
        "A": ((0, 1), (2, 3), (4, 5)),
        "B": ((0, 1), (2, 4), (3, 5)),
        "K": ((0, 2), (1, 5), (3, 4)),
        "L": ((0, 5), (1, 2), (3, 4)),
        "R": ((0, 3), (1, 4), (2, 5)),
    }
    base_values = {
        name: weights[matching[0]] * weights[matching[1]] * weights[matching[2]]
        for name, matching in bases.items()
    }
    require(all(base_values.values()), "one selected base monomial vanished")
    require(base_values == {
        "A": Q(2), "B": Q(2), "K": Q(2), "L": Q(2), "R": Q(-3)
    }, "the selected base values changed")
    o11_value = weights[(2, 5)] * weights[(3, 4)]
    o22_value = weights[(0, 1)] * weights[(2, 5)]
    require((o11_value, o22_value) == (Q(2), Q(-2)),
            "the two diagonal augmented C6 bases stopped being active terms")

    # Each window joins one R edge to one diagonal augmented-response edge
    # at the same physical coordinate.  Every linear combination squares to
    # zero.  The first direction is unary-private; the second is private in
    # G22 (edge 01) or G11 (edge 34).  All crossed lock coordinates vanish.
    windows = {
        "site0": ((0, 3), (0, 1), "G22"),
        "site1": ((1, 4), (0, 1), "G22"),
        "site3": ((0, 3), (3, 4), "G11"),
        "site4": ((1, 4), (3, 4), "G11"),
    }
    window_records = []
    for name, (unary_edge, diagonal_edge, diagonal_row) in windows.items():
        directions = []
        for edge in (unary_edge, diagonal_edge):
            directions.append({switch.cell(*edge, 0, 0): Q(1)})
        common_sites = set(unary_edge) & set(diagonal_edge)
        require(len(common_sites) == 1,
                "an attachment window stopped being same-star")
        require(all(set(next(iter(direction))[:2]) & common_sites
                    for direction in directions),
                "a switch direction left the common physical star")

        columns = [labelled_lock_column(
            switch, q, endpoints, direction
        ) for direction in directions]
        require(matrix_rank(columns) == 2,
                f"{name} acquired a simultaneous five-row kernel")
        require(all(not any(key[0] in {"G12", "G21"} for key in column)
                    for column in columns),
                f"{name} acquired a crossed complementary component")
        expected_first = Counter({("top", PURE_ZERO):
                                  Q(-3 if unary_edge == (0, 3) else 1)})
        diagonal_word = ((1, 1, 0, 0, 0, 0)
                         if diagonal_row == "G11"
                         else (0, 0, 0, 2, 2, 0))
        expected_second = Counter({(diagonal_row, diagonal_word): Q(1)})
        require(columns == [expected_first, expected_second],
                f"{name} lock stopped being the private diagonal matrix")

        # Audit one nontrivial exact finite difference.  Since both inserted
        # cells meet the common site, there are no quadratic terms.
        combined = tensor_add(
            tensor_scale(Q(2, 3), directions[0]),
            tensor_scale(Q(-5, 7), directions[1]),
        )
        q_new = Counter(q)
        q_new.update(combined)
        q_new = Counter({key: value for key, value in q_new.items() if value})
        actual_top = switch.subtract(
            switch.matchings(q_new, SITES), switch.matchings(q, SITES)
        )
        predicted_top = switch.inserted_edge_tensor(q, combined, SITES)
        require(actual_top == predicted_top,
                f"{name} unary finite difference became nonlinear")
        response_checks = 0
        for _row, p, s in endpoints:
            actual = switch.subtract(
                switch.response(q_new, p, s, SITES),
                switch.response(q, p, s, SITES),
            )
            predicted = switch.response_with_inserted_edge(
                q, p, s, combined, SITES
            )
            require(actual == predicted,
                    f"{name} response finite difference became nonlinear")
            response_checks += 1

        window_records.append({
            "window": name,
            "common_site": next(iter(common_sites)),
            "directions": ["q%d%d:00" % edge
                           for edge in (unary_edge, diagonal_edge)],
            "lock_columns": [
                [[key[0], "".join(map(str, key[1])), str(value)]
                 for key, value in sorted(column.items())]
                for column in columns
            ],
            "lock_rank": 2,
            "kernel_dimension": 0,
            "crossed_12_components": 0,
            "crossed_21_components": 0,
            "finite_difference_response_checks": response_checks,
        })

    ledger = {
        "pins": PINS,
        "rational_zero_fibre": {
            "q_weights": {"q%d%d:00" % edge: str(value)
                          for edge, value in sorted(weights.items())},
            "q13": 0,
            "q04": 0,
            "direct_PS": 0,
            "top_tensor": {"000000": "1"},
            "response_zero_tensors": sorted(responses),
            "base_values": {name: str(value)
                            for name, value in base_values.items()},
            "O11_term": str(o11_value),
            "O22_term": str(o22_value),
        },
        "same_star_attachment_windows": window_records,
        "theorem": (
            "the unary plus four frozen response-zero fibres of the silent "
            "chordless C6 do not force a same-star lock kernel or a "
            "complementary crossed wedge: each of its four natural R-to-O "
            "attachment windows can have the injective private lock matrix "
            "diag(nonzero unary, nonzero diagonal response) while both "
            "crossed lock coordinates vanish"
        ),
        "first_missing_input": (
            "the bright X1/X2 diagonal response rows or additional endpoint-"
            "star components must couple the unary-private and diagonal-"
            "private columns; b80b064's four displayed zero fibres alone "
            "cannot supply that coupling"
        ),
        "scope": (
            "exact rational common-q and literal-source five-lock guard, "
            "satisfying q^[3]=X0 and all four displayed response zero "
            "tensors; not a full one-bad point because the bright X1 and X2 "
            "response tensors are absent"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"silent C6 injective guard changed: {digest}")
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("h3 silent C6 five-lock injective/no-wedge guard: PASS (exact)")
    print("four same-star attachment windows: rank 2, kernel 0")
    print("crossed G12/G21 lock components: 0/0")
    print("first missing input: bright diagonal response/star completion")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
