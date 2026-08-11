#!/usr/bin/env python3
"""Full-five typed linear boundary of the k=3 target-port coloop.

The five aggregate tensor equations do not, as row equations alone, force
an avoiding pure target matching.  This checker builds two exact three-
column response circuits.  Each diagonal/crossed pair sums to (X_i,0), all
three complete columns are independent, and the pure target coordinate
occurs in only the first port.  The unary row is exact in its own grade.

This is deliberately not a common-q physical source.  It proves that the
next positive lemma must use a source relation coupling literal matching
tails across the rows, rather than another linear combination of the five
aggregate equations.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_axis_circuit_outside_endpoint_rank_restoration.py":
        "1af29dfddaf3127e758f07c53cf08189bda72df4e54a58a4e0ca78f6709874ac",
    "notes/uniform-axis-circuit-outside-endpoint-rank-restoration.md":
        "a7345aa254a4dcfb65742b8b09f0dafe7a1ef1b1b9a2fa67b6e8528e462a9516",
    "computations/verify_uniform_one_bad_axis_hessian_carrier_circuit_boundary.py":
        "1594dcac16bb77bb929c18edda224e215ea99697bfd36edabc4230a0d341b5c8",
    "notes/uniform-one-bad-axis-hessian-carrier-circuit-boundary.md":
        "d784f8d25461ffcdafcc3fb9a39ccc776f770fb63359f722bead4fe7c965e73e",
}
EXPECTED_LEDGER_SHA256 = (
    "14ae260e94c71d1cc99a1063a66ece6cd599cec7496948fce486e34179ce6dba"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def rank(columns):
    if not columns:
        return 0
    matrix = [[Q(column[row]) for column in columns]
              for row in range(len(columns[0]))]
    pivot_row = 0
    for column in range(len(matrix[0])):
        pivot = next((row for row in range(pivot_row, len(matrix))
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [entry - value * pivot_entry
                           for entry, pivot_entry
                           in zip(matrix[row], matrix[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def add(*vectors):
    return tuple(sum(entries) for entries in zip(*vectors, strict=True))


def pair_circuit(target_index, diagonal_debts, crossed_debts, dimension):
    """Three complete columns in one diagonal/crossed response pair."""
    x, a, b = target_index, *diagonal_debts
    u, v = crossed_debts
    columns = []
    for entries in (
        {x: 1, a: 1, u: 1},
        {a: -1, b: 1, u: -1, v: 1},
        {b: -1, v: -1},
    ):
        columns.append(tuple(Q(entries.get(index, 0))
                             for index in range(dimension)))
    target = tuple(Q(int(index == x)) for index in range(dimension))
    require(add(*columns) == target,
            "the diagonal/crossed circuit stopped summing to its target")
    require(rank(columns) == 3,
            "the three complete response columns stopped being minimum")
    require(tuple(column[x] for column in columns) == (1, 0, 0),
            "the pure target coordinate stopped being a port coloop")
    return columns, target


def audit_full_five_boundary():
    # Coordinate blocks:
    #   0  top X0
    #   1  response-11 target X1
    #   2,3 response-11 mixed debts A,B
    #   4,5 response-12 crossed debts U,V
    #   6  response-22 target X2
    #   7,8 response-22 mixed debts C,D
    #   9,10 response-21 crossed debts W,Z.
    dimension = 11
    top = tuple(Q(int(index == 0)) for index in range(dimension))
    p1_columns, target1 = pair_circuit(1, (2, 3), (4, 5), dimension)
    p2_columns, target2 = pair_circuit(6, (7, 8), (9, 10), dimension)

    total = add(top, *p1_columns, *p2_columns)
    expected = tuple(Q(int(index in (0, 1, 6)))
                     for index in range(dimension))
    require(total == expected,
            "the five typed target rows stopped being exact")

    # Separating port functionals.  They prove that neither target can be
    # moved to an avoiding port through a joint-kernel translation: each
    # complete three-column map is injective and the target coordinate is
    # carried only by its first column.
    for columns, target, target_index in (
            (p1_columns, target1, 1), (p2_columns, target2, 6)):
        require(rank(columns) == rank(columns + [target]) == 3,
                "the target left the complete-column image")
        require(all(column[target_index] == 0 for column in columns[1:]),
                "an avoiding port acquired a pure target coefficient")
        require(rank(columns[1:]) == 2,
                "the two avoiding complete columns became deletable")

    # Pair an active avoiding p1 component (column 1) with the selected p2
    # target port (column 0).  Both are nonzero and their endpoint heads can
    # be e1,e2, but the latter is a target-family coloop.  The aggregate
    # crossed row is nevertheless exactly zero because coordinates 9,10
    # cancel across all three p2 columns.
    require(any(p1_columns[1]) and any(p2_columns[0]),
            "the outside/opposite pair lost activity")
    require(all(sum(column[index] for column in p1_columns) == 0
                for index in (4, 5)),
            "the first crossed row stopped vanishing")
    require(all(sum(column[index] for column in p2_columns) == 0
                for index in (9, 10)),
            "the second crossed row stopped vanishing")

    return {
        "feature_basis": [
            "top:X0", "11:X1", "11:A", "11:B", "12:U", "12:V",
            "22:X2", "22:C", "22:D", "21:W", "21:Z",
        ],
        "p1_complete_columns": [[str(value) for value in column]
                                for column in p1_columns],
        "p2_complete_columns": [[str(value) for value in column]
                                for column in p2_columns],
        "column_ranks": [rank(p1_columns), rank(p2_columns)],
        "typed_row_sums": ["top=X0", "11=X1", "12=0", "21=0", "22=X2"],
        "pure_target_port_supports": {"X1": [0], "X2": [0]},
        "outside_active_component": "p1 column 1",
        "selected_opposite_coloop": "p2 column 0",
        "joint_kernel_dimensions": [0, 0],
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
        "full_five_typed_boundary": audit_full_five_boundary(),
        "negative_theorem": (
            "the unary target and four complete response sums, treated as "
            "aggregate tensor rows, do not force an avoiding target "
            "matching, a joint-kernel deletion, or a target-line point in "
            "a minimum k3 complete-column circuit"
        ),
        "first_missing_source_relation": (
            "a genuine common-q matching-exchange relation coupling a "
            "literal tail in the outside column to the coloop diagonal tail; "
            "equivalently a four-hole Hessian/Pluecker coefficient before "
            "the matching terms are summed into their five tensor rows"
        ),
        "scope": (
            "exact rational full-five row module and primitive coloop "
            "separator, not a physical common-q source or a counterexample "
            "to any theorem using literal cofactor provenance"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"target-coloop full-five ledger changed: {digest}")
    print("uniform target-coloop full-five typed boundary: PASS")
    print("two k3 complete-column ranks: 3,3; joint kernels: 0,0")
    print("five row sums exact; both pure targets remain single-port coloops")
    print("missing input: literal common-q four-hole matching exchange")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
