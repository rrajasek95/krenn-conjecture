#!/usr/bin/env python3
"""Exact degree-nine source-ideal test in characteristic two.

This is the characteristic-two counterpart of
``test_degree9_source_ideal.py``.  Reynolds averaging over ``S_6 x S_3``
is invalid in characteristic two, since that group's order is even.  We
instead average over the odd subgroup

    H = <(012), (345)> x <(012)_colors>,  |H| = 27.

Averaging over H is lossless over GF(2).  The script constructs the complete
H-invariant Macaulay map in the multidegree of

    P = F_000000 F_111111 F_222222

and first applies exact singleton-row elimination.  Thus either a reported
inconsistency proves ``P`` is not in the mixed-coefficient ideal in this
degree, or a fully peeled system gives an explicit GF(2) membership result.
If a nonzero 2-core remains, the script reports its exact dimensions rather
than making an inference.
"""

from __future__ import annotations

import itertools
import gzip
import heapq
import pickle
import time
from array import array
from collections import Counter, deque
from pathlib import Path


N = 6
Q = 3


def perfect_matchings(items):
    items = tuple(items)
    if not items:
        yield ()
        return
    a = items[0]
    for position, b in enumerate(items[1:], 1):
        if a // Q == b // Q:
            continue
        rest = items[1:position] + items[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((a, b),) + tail


VALID_EDGES = tuple(
    (a, b)
    for a in range(N * Q)
    for b in range(a + 1, N * Q)
    if a // Q != b // Q
)
EDGE_INDEX = {edge: index for index, edge in enumerate(VALID_EDGES)}


def matching_code(pairs):
    code = 0
    for a, b in pairs:
        if a > b:
            a, b = b, a
        code |= 1 << EDGE_INDEX[a, b]
    return code


def bit_indices(code):
    while code:
        low = code & -code
        yield low.bit_length() - 1
        code ^= low


VERTEX_PMS = tuple(perfect_matchings(tuple(3 * v for v in range(N))))
assert len(VERTEX_PMS) == 15


def group_actions():
    actions = []
    for left_power, right_power, color_power in itertools.product(range(3), repeat=3):
        vertex_perm = tuple(
            ((v + left_power) % 3 if v < 3 else 3 + (v - 3 + right_power) % 3)
            for v in range(N)
        )
        color_perm = tuple((color + color_power) % 3 for color in range(Q))
        stub_map = tuple(
            3 * vertex_perm[v] + color_perm[color]
            for v in range(N)
            for color in range(Q)
        )
        edge_map = []
        for a, b in VALID_EDGES:
            aa, bb = stub_map[a], stub_map[b]
            if aa > bb:
                aa, bb = bb, aa
            edge_map.append(1 << EDGE_INDEX[aa, bb])
        actions.append((vertex_perm, color_perm, tuple(edge_map)))
    assert len(actions) == 27
    return tuple(actions)


def transform_coloring(coloring, vertex_perm, color_perm):
    result = [None] * N
    for vertex, color in enumerate(coloring):
        result[vertex_perm[vertex]] = color_perm[color]
    return tuple(result)


def transform_code(code, edge_map):
    result = 0
    for index in bit_indices(code):
        result |= edge_map[index]
    return result


def f_matching_code(coloring, vertex_pm):
    return matching_code(
        (u + coloring[u // 3], v + coloring[v // 3]) for u, v in vertex_pm
    )


def complement_matchings(coloring):
    stubs = tuple(
        3 * vertex + color
        for vertex in range(N)
        for color in range(Q)
        if color != coloring[vertex]
    )
    return tuple(matching_code(matching) for matching in perfect_matchings(stubs))


def is_target_monomial(code):
    return all(
        VALID_EDGES[index][0] % Q == VALID_EDGES[index][1] % Q
        for index in bit_indices(code)
    )


def build_matrix(cache_path):
    if cache_path.exists():
        with cache_path.open("rb") as stream:
            data = pickle.load(stream)
        if data.get("version") == 1:
            return data

    actions = group_actions()
    all_colorings = set(itertools.product(range(Q), repeat=N))
    color_reps = []
    while all_colorings:
        coloring = min(all_colorings)
        orbit = {
            transform_coloring(coloring, vertex_perm, color_perm)
            for vertex_perm, color_perm, _ in actions
        }
        all_colorings.difference_update(orbit)
        if len(set(coloring)) > 1:
            color_reps.append(coloring)
    print(f"mixed coloring H-orbits={len(color_reps)}", flush=True)

    row_index = {}
    columns = []

    def canonical_row(code):
        return min(transform_code(code, edge_map) for _, _, edge_map in actions)

    for rep_number, coloring in enumerate(color_reps, 1):
        stabilizer = tuple(
            edge_map
            for vertex_perm, color_perm, edge_map in actions
            if transform_coloring(coloring, vertex_perm, color_perm) == coloring
        )
        unseen = set(complement_matchings(coloring))
        complement_reps = []
        while unseen:
            code = next(iter(unseen))
            orbit = {transform_code(code, edge_map) for edge_map in stabilizer}
            unseen.difference_update(orbit)
            complement_reps.append(min(orbit))

        f_terms = tuple(f_matching_code(coloring, matching) for matching in VERTEX_PMS)
        for complement in complement_reps:
            parity = Counter(canonical_row(complement | term) for term in f_terms)
            row_codes = tuple(sorted(code for code, count in parity.items() if count & 1))
            rows = []
            for code in row_codes:
                if code not in row_index:
                    row_index[code] = len(row_index)
                rows.append(row_index[code])
            columns.append(tuple(rows))
        print(
            f"color orbit {rep_number}/{len(color_reps)}: "
            f"stabilizer={len(stabilizer)} columns={len(columns)} rows={len(row_index)}",
            flush=True,
        )

    row_codes = [None] * len(row_index)
    for code, index in row_index.items():
        row_codes[index] = code
    rhs = bytearray(int(is_target_monomial(code)) for code in row_codes)
    data = {
        "version": 1,
        "columns": columns,
        "row_codes": row_codes,
        "rhs": bytes(rhs),
    }
    with cache_path.open("wb") as stream:
        pickle.dump(data, stream, protocol=pickle.HIGHEST_PROTOCOL)
    return data


def singleton_peel(data):
    columns = data["columns"]
    number_rows = len(data["row_codes"])
    number_columns = len(columns)
    degrees = array("I", [0]) * number_rows
    for column in columns:
        for row in column:
            degrees[row] += 1

    offsets = array("Q", [0]) * (number_rows + 1)
    for row, degree in enumerate(degrees):
        offsets[row + 1] = offsets[row] + degree
    incidence = array("I", [0]) * offsets[-1]
    cursor = array("Q", offsets[:-1])
    for column_index, column in enumerate(columns):
        for row in column:
            incidence[cursor[row]] = column_index
            cursor[row] += 1

    active = bytearray(b"\x01") * number_columns
    assigned = bytearray(number_columns)
    values = bytearray(number_columns)
    rhs = bytearray(data["rhs"])
    queue = deque(row for row, degree in enumerate(degrees) if degree <= 1)
    assignments = 0

    def remaining_column(row):
        for position in range(offsets[row], offsets[row + 1]):
            column = incidence[position]
            if active[column]:
                return column
        return None

    while queue:
        row = queue.popleft()
        if degrees[row] == 0:
            if rhs[row]:
                print(
                    f"INCONSISTENT after {assignments} singleton assignments: "
                    f"row={row} code={data['row_codes'][row]}",
                    flush=True,
                )
                return False
            continue
        if degrees[row] != 1:
            continue
        column = remaining_column(row)
        assert column is not None
        value = rhs[row]
        active[column] = 0
        assigned[column] = 1
        values[column] = value
        assignments += 1
        for touched_row in columns[column]:
            assert degrees[touched_row] > 0
            degrees[touched_row] -= 1
            rhs[touched_row] ^= value
            if degrees[touched_row] <= 1:
                queue.append(touched_row)

    core_rows = sum(degree > 0 for degree in degrees)
    core_columns = sum(active)
    core_rhs = sum(rhs[row] for row, degree in enumerate(degrees) if degree > 0)
    zero_row_rhs = sum(rhs[row] for row, degree in enumerate(degrees) if degree == 0)
    print(
        f"singleton assignments={assignments}; core rows={core_rows}, "
        f"core columns={core_columns}, core rhs weight={core_rhs}, "
        f"zero-row rhs weight={zero_row_rhs}",
        flush=True,
    )
    if zero_row_rhs:
        return False
    if core_rhs == 0:
        print("IN SPAN: singleton assignments plus zero core variables solve A x = P")
        return True
    print("UNRESOLVED: a nonzero exact 2-core remains")
    return None


def minimum_degree_membership(data, certificate_path, dual_path=None):
    """Decide membership by exact sparse elimination of the dual system.

    The equations are ``column dot y = 0`` for every Macaulay column,
    together with ``target dot y = 1``.  If elimination produces ``0=1``,
    provenance of that row is an explicit set of columns whose XOR is the
    target.  If the system is consistent, its solution is a dual witness to
    nonmembership.
    """
    columns = data["columns"]
    number_rows = len(data["row_codes"])
    number_columns = len(columns)
    equations = [set(column) for column in columns]
    equations.append({row for row, value in enumerate(data["rhs"]) if value})
    number_equations = len(equations)
    rhs = bytearray(number_equations)
    rhs[-1] = 1

    adjacency = [set() for _ in range(number_rows)]
    for equation, variables in enumerate(equations):
        for variable in variables:
            adjacency[variable].add(equation)

    active = bytearray(b"\x01") * number_equations
    remaining = number_equations
    heap = [(len(adjacency[v]), v) for v in range(number_rows) if adjacency[v]]
    heapq.heapify(heap)

    # Each current equation is an XOR-expression in the original equations.
    # Leaves 0,...,number_equations-1 are original equations; every update
    # creates one immutable binary XOR node.
    current_node = array("I", range(number_equations))
    left_nodes = array("I")
    right_nodes = array("I")
    records = []
    contradiction_node = None
    updates = 0
    started = time.time()

    while remaining:
        while heap:
            degree, variable = heapq.heappop(heap)
            if degree and degree == len(adjacency[variable]):
                break
        else:
            raise AssertionError(f"{remaining} active equations contain no variables")

        pivot_equation = min(
            adjacency[variable], key=lambda equation: (len(equations[equation]), equation)
        )
        pivot_variables = equations[pivot_equation]
        records.append(
            (
                variable,
                tuple(value for value in pivot_variables if value != variable),
                rhs[pivot_equation],
            )
        )

        for equation in sorted(adjacency[variable] - {pivot_equation}):
            variables = equations[equation]
            for value in pivot_variables:
                if value in variables:
                    variables.remove(value)
                    adjacency[value].remove(equation)
                else:
                    variables.add(value)
                    adjacency[value].add(equation)
                heapq.heappush(heap, (len(adjacency[value]), value))
            rhs[equation] ^= rhs[pivot_equation]
            left_nodes.append(current_node[equation])
            right_nodes.append(current_node[pivot_equation])
            current_node[equation] = number_equations + len(left_nodes) - 1
            updates += 1
            if not variables:
                active[equation] = 0
                remaining -= 1
                if rhs[equation]:
                    contradiction_node = current_node[equation]
                    break
        if contradiction_node is not None:
            break

        active[pivot_equation] = 0
        remaining -= 1
        for value in pivot_variables:
            adjacency[value].remove(pivot_equation)
            heapq.heappush(heap, (len(adjacency[value]), value))

        if len(records) % 10_000 == 0:
            print(
                f"dual pivots={len(records)} remaining={remaining} "
                f"minimum-degree={degree} updates={updates} "
                f"seconds={time.time()-started:.2f}",
                flush=True,
            )

    if contradiction_node is not None:
        total_nodes = number_equations + len(left_nodes)
        marks = bytearray(total_nodes)
        marks[contradiction_node] = 1
        for node in range(total_nodes - 1, number_equations - 1, -1):
            if marks[node]:
                offset = node - number_equations
                marks[left_nodes[offset]] ^= 1
                marks[right_nodes[offset]] ^= 1
        assert marks[number_columns] == 1  # the target equation occurs once
        selected = tuple(index for index in range(number_columns) if marks[index])

        audit = set()
        for column in selected:
            audit.symmetric_difference_update(columns[column])
        target = {row for row, value in enumerate(data["rhs"]) if value}
        assert audit == target

        payload = {
            "version": 1,
            "field": "GF(2)",
            "group_order": 27,
            "shape": (number_rows, number_columns),
            "selected_columns": selected,
        }
        with gzip.open(certificate_path, "wb") as stream:
            pickle.dump(payload, stream, protocol=pickle.HIGHEST_PROTOCOL)
        print(
            f"IN SPAN: exact XOR certificate uses {len(selected)} orbit columns; "
            f"saved {certificate_path}",
            flush=True,
        )
        return True

    assert remaining == 0
    values = bytearray(number_rows)
    for variable, other_variables, value in reversed(records):
        for other in other_variables:
            value ^= values[other]
        values[variable] = value
    assert all(sum(values[row] for row in column) % 2 == 0 for column in columns)
    assert sum(values[row] * value for row, value in enumerate(data["rhs"])) % 2 == 1
    if dual_path is not None:
        support = tuple(row for row, value in enumerate(values) if value)
        with gzip.open(dual_path, "wb") as stream:
            pickle.dump(
                {
                    "version": 1,
                    "field": "GF(2)",
                    "shape": (number_rows, number_columns),
                    "support": support,
                },
                stream,
                protocol=pickle.HIGHEST_PROTOCOL,
            )
        print(f"saved exact dual witness {dual_path}", flush=True)
    print(f"NOT IN SPAN: exact dual witness has support {sum(values)}", flush=True)
    return False


def main():
    cache_path = Path(__file__).with_name("degree9_source_ideal_char2_h27.pkl")
    data = build_matrix(cache_path)
    print(
        f"H-invariant matrix rows={len(data['row_codes'])} "
        f"columns={len(data['columns'])} "
        f"nnz={sum(map(len, data['columns']))} rhs={sum(data['rhs'])}",
        flush=True,
    )
    result = singleton_peel(data)
    certificate_path = Path(__file__).with_name("certificates") / (
        "degree9_char2_h27_membership.pkl.gz"
    )
    certificate_path.parent.mkdir(exist_ok=True)
    result = minimum_degree_membership(data, certificate_path)
    raise SystemExit(0 if result else 1)


if __name__ == "__main__":
    main()
