#!/usr/bin/env python3
"""Cost-three pure-21 path incidence, circuits, and exact Fredholm dual.

Relative to the repaired pure-21 packet, enumerate every single DQ/PS path
requiring exactly three new source cells.  Each path is normalized so its
selected 222222:21 coefficient is +1.  The resulting exact all-word row
difference matrix has rank 29 on 32 columns.  Its three irreducible circuits
are disjoint signed octagons and are all selected-dark.  An explicit eleven-
row integer dual reads +1 on every column.

This is a normalized path-incidence theorem, not a simultaneous nonlinear
source realization: cross terms between cells belonging to different paths
are outside its scope.
"""

import argparse
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


PARENT_PATH = Path(__file__).with_name(
    "verify_n8_f02_ps01_mate_pure_head_migration_gate.py"
)
SPEC = spec_from_file_location("cost3_parent", PARENT_PATH)
require(SPEC is not None and SPEC.loader is not None, "could not load parent audit")
P = module_from_spec(SPEC)
SPEC.loader.exec_module(P)
B = P.B


SELECTED = ((2,) * 6, 2, 1)
OLD_Q2 = {(0, 4), (1, 3)}
BASE_Q = dict(B.Q_EDGE)
BASE_P = dict(B.FIRST)
BASE_S = dict(B.SECOND)
BASE_D = dict(B.DIRECT)


def path_key(path):
    if path[0] == "DQ":
        return ("DQ", path[1])
    return ("PS", path[1], path[2], path[3])


def path_text(path):
    if path[0] == "DQ":
        return "DQ[" + "|".join(f"{x}{y}" for x, y in path[1]) + "]"
    _, p_site, s_site, edges = path
    return (
        f"PS[{p_site},{s_site};"
        + "|".join(f"{x}{y}" for x, y in edges)
        + "]"
    )


def enumerate_paths():
    ps = []
    for p_site in B.SITES:
        for s_site in B.SITES:
            if p_site == s_site:
                continue
            rest = tuple(site for site in B.SITES if site not in (p_site, s_site))
            for matching in B.matchings(rest):
                edges = tuple(sorted(tuple(sorted(edge)) for edge in matching))
                cost = int(p_site != 2) + int(s_site != 5)
                cost += sum(edge not in OLD_Q2 for edge in edges)
                if cost == 3:
                    ps.append(("PS", p_site, s_site, edges))

    dq = []
    for matching in B.matchings(B.SITES):
        edges = tuple(sorted(tuple(sorted(edge)) for edge in matching))
        cost = 1 + sum(edge not in OLD_Q2 for edge in edges)  # new a_21
        if cost == 3:
            dq.append(("DQ", edges))
    require((len(ps), len(dq)) == (28, 4), ("cost-three census moved", ps, dq))
    return tuple(ps + dq)


PATHS = enumerate_paths()
PATH_INDEX = {path_key(path): index for index, path in enumerate(PATHS)}


def reset_tables():
    B.Q_EDGE.clear()
    B.Q_EDGE.update(BASE_Q)
    B.FIRST.clear()
    B.FIRST.update(BASE_P)
    B.SECOND.clear()
    B.SECOND.update(BASE_S)
    B.DIRECT.clear()
    B.DIRECT.update(BASE_D)


def evaluate(polynomial):
    return P.evaluate(polynomial)


def row_ledger():
    answer = {}
    for word in product(B.COLORS, repeat=6):
        for row, column in product(B.COLORS, repeat=2):
            value = evaluate(B.residual(row, column, word))
            if value:
                answer[(word, row, column)] = value
    return answer


def add_path(path):
    additions = []
    if path[0] == "PS":
        _, p_site, s_site, edges = path
        if p_site != 2:
            additions.append(("p", (2, p_site, 2)))
        if s_site != 5:
            additions.append(("s", (1, s_site, 2)))
        for left, right in edges:
            if (left, right) not in OLD_Q2:
                additions.append(("q", (left, right, 2, 2)))
        # The old s_1 coefficient Y is -1.  If it occurs, reverse one new
        # cell so that every selected path has normalized value +1.
        final_sign = -1 if s_site == 5 else 1
    else:
        _, edges = path
        additions.append(("d", (2, 1)))
        for left, right in edges:
            if (left, right) not in OLD_Q2:
                additions.append(("q", (left, right, 2, 2)))
        final_sign = 1
    require(len(additions) == 3, ("path cost is not three", path, additions))
    for position, (kind, key) in enumerate(additions):
        value = final_sign if position == len(additions) - 1 else 1
        table = {"p": B.FIRST, "s": B.SECOND, "q": B.Q_EDGE, "d": B.DIRECT}[kind]
        table[key] = B.constant(value)


def build_columns():
    reset_tables()
    base = row_ledger()
    columns = []
    for path in PATHS:
        reset_tables()
        add_path(path)
        candidate = row_ledger()
        difference = {
            row: candidate.get(row, Q(0)) - base.get(row, Q(0))
            for row in set(candidate) | set(base)
        }
        difference = {row: value for row, value in difference.items() if value}
        require(difference.get(SELECTED) == 1,
                ("selected normalization moved", path, difference.get(SELECTED)))
        columns.append(difference)
    reset_tables()
    return base, tuple(columns)


def rref(matrix):
    work = [list(map(Q, row)) for row in matrix]
    if not work:
        return 0, (), work
    row = 0
    pivots = []
    for column in range(len(work[0])):
        pivot = next((index for index in range(row, len(work)) if work[index][column]), None)
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        scale = work[row][column]
        work[row] = [entry / scale for entry in work[row]]
        for index in range(len(work)):
            if index == row or not work[index][column]:
                continue
            scale = work[index][column]
            work[index] = [
                left - scale * right for left, right in zip(work[index], work[row])
            ]
        pivots.append(column)
        row += 1
        if row == len(work):
            break
    return row, tuple(pivots), work


def linear_combination(columns, weights):
    answer = {}
    for column, weight in zip(columns, weights):
        if not weight:
            continue
        for row, value in column.items():
            answer[row] = answer.get(row, Q(0)) + weight * value
    return {row: value for row, value in answer.items() if value}


def vector(entries):
    answer = [Q(0)] * len(PATHS)
    for path, coefficient in entries:
        answer[PATH_INDEX[path_key(path)]] = Q(coefficient)
    return tuple(answer)


CIRCUITS = (
    vector((
        (("PS", 2, 0, ((1, 4), (3, 5))), 1),
        (("PS", 2, 0, ((1, 5), (3, 4))), -1),
        (("PS", 2, 1, ((0, 3), (4, 5))), -1),
        (("PS", 2, 1, ((0, 5), (3, 4))), 1),
        (("PS", 2, 3, ((0, 1), (4, 5))), 1),
        (("PS", 2, 3, ((0, 5), (1, 4))), -1),
        (("PS", 2, 4, ((0, 1), (3, 5))), -1),
        (("PS", 2, 4, ((0, 3), (1, 5))), 1),
    )),
    vector((
        (("PS", 1, 2, ((0, 4), (3, 5))), 1),
        (("PS", 1, 3, ((0, 4), (2, 5))), -1),
        (("PS", 3, 1, ((0, 4), (2, 5))), 1),
        (("PS", 3, 2, ((0, 4), (1, 5))), -1),
        (("PS", 5, 1, ((0, 4), (2, 3))), -1),
        (("PS", 5, 3, ((0, 4), (1, 2))), 1),
        (("DQ", ((0, 4), (1, 2), (3, 5))), -1),
        (("DQ", ((0, 4), (1, 5), (2, 3))), 1),
    )),
    vector((
        (("PS", 0, 2, ((1, 3), (4, 5))), 1),
        (("PS", 0, 4, ((1, 3), (2, 5))), -1),
        (("PS", 4, 0, ((1, 3), (2, 5))), 1),
        (("PS", 4, 2, ((0, 5), (1, 3))), -1),
        (("PS", 5, 0, ((1, 3), (2, 4))), -1),
        (("PS", 5, 4, ((0, 2), (1, 3))), 1),
        (("DQ", ((0, 2), (1, 3), (4, 5))), -1),
        (("DQ", ((0, 5), (1, 3), (2, 4))), 1),
    )),
)


DUAL = {
    ((0, 0, 0, 0, 2, 2), 2, 0): Q(1),
    ((0, 1, 0, 0, 1, 2), 2, 1): Q(1),
    ((0, 2, 2, 2, 2, 2), 0, 1): Q(-1),
    ((1, 0, 1, 2, 0, 0), 2, 0): Q(1),
    ((1, 1, 1, 1, 1, 2), 2, 1): Q(1),
    ((1, 2, 1, 1, 0, 0), 2, 1): Q(1),
    ((1, 2, 1, 2, 2, 1), 1, 1): Q(1),
    ((1, 2, 1, 2, 2, 2), 0, 1): Q(1),
    ((1, 2, 1, 2, 2, 2), 2, 1): Q(-1),
    ((1, 2, 1, 2, 2, 2), 2, 2): Q(-1),
    ((2, 0, 0, 0, 0, 0), 2, 0): Q(1),
}


def audit_incidence(columns):
    rows = sorted(set().union(*(set(column) for column in columns)) - {SELECTED})
    matrix = [[column.get(row, Q(0)) for column in columns] for row in rows]
    rank, _, _ = rref(matrix)
    require((len(rows), rank, len(columns) - rank) == (62, 29, 3),
            ("cost-three incidence dimensions moved", len(rows), rank))
    return rows, matrix, rank


def audit_circuits(columns, rows):
    supports = []
    for circuit in CIRCUITS:
        support = tuple(index for index, value in enumerate(circuit) if value)
        require(len(support) == 8, ("circuit support size moved", support))
        require(sum(circuit) == 0, ("circuit became selected-bright", circuit))
        require(linear_combination(columns, circuit) == {},
                ("declared circuit is not an exact row relation", circuit))
        restricted = [
            [columns[index].get(row, Q(0)) for index in support]
            for row in rows
        ]
        rank, _, _ = rref(restricted)
        require(rank == 7, ("circuit is not irreducible", support, rank))
        supports.append(frozenset(support))
    require(all(left.isdisjoint(right)
                for position, left in enumerate(supports)
                for right in supports[position + 1:]),
            ("circuit supports overlap", supports))
    require(len(set().union(*supports)) == 24, "circuit union size moved")
    return supports


def audit_dual(columns):
    values = []
    for column in columns:
        value = sum((weight * column.get(row, Q(0)) for row, weight in DUAL.items()), Q(0))
        values.append(value)
    require(values == [Q(1)] * len(columns), ("Fredholm dual moved", values))
    require(SELECTED not in DUAL, "dual illegally used the selected row")
    return values


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=("all", "classification", "incidence", "circuits", "dual"),
        default="all",
    )
    args = parser.parse_args()

    columns = rows = rank = supports = dual_values = None
    if args.mode != "classification":
        _, columns = build_columns()
    if args.mode in ("all", "incidence", "circuits"):
        rows, _, rank = audit_incidence(columns)
    if args.mode in ("all", "circuits"):
        supports = audit_circuits(columns, rows)
    if args.mode in ("all", "dual"):
        dual_values = audit_dual(columns)

    report = {
        "mode": args.mode,
        "cell_cost": 3,
        "ps_paths": sum(path[0] == "PS" for path in PATHS),
        "dq_paths": sum(path[0] == "DQ" for path in PATHS),
        "columns": len(PATHS),
        "off_selected_rows": None if rows is None else len(rows),
        "rank": rank,
        "nullity": None if rank is None else len(PATHS) - rank,
        "irreducible_circuits": None if supports is None else len(supports),
        "circuit_sizes": None if supports is None else [len(support) for support in supports],
        "circuit_selected_sums": None if supports is None else [0, 0, 0],
        "dual_rows": None if dual_values is None else len(DUAL),
        "dual_column_values": None if dual_values is None else sorted(set(map(int, dual_values))),
        "scope": "normalized single-path incidence; simultaneous cross-cell products excluded",
    }
    digest = sha256(
        json.dumps(report, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    print("n=8 pure-21 cost-three multicompanion circuit gate: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
