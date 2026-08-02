#!/usr/bin/env python3
"""Audit the terminal Hamilton-path readout in normalized chart 26.

There are two different objects which can have the same uncoloured
Hamilton-path skeleton:

* a top term produced by mixed-source path-forest straightening; and
* a monomial of the physical pure product H_0 H_1 H_2.

This checker compares them without forgetting endpoint colours.  It also
tests the clean-cap error on one physical pure-target Hamilton row.  The
selected row has a unique pure matching triple and an active support edge
between its endpoints, but adding one off-path spoke changes its clean-cap
error.  Thus a terminal leading monomial does not by itself give a
lift-independent physical cap readout.
"""

from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load_module(name, filename):
    path = HERE / filename
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


NORMALIZED = load_module(
    "n8_chart26_terminal_normalized",
    "verify_n8_chart26_normalized_degree7_closure.py",
)
WEIGHTED = load_module(
    "n8_chart26_terminal_weighted",
    "verify_n8_chart26_feasible_squarefree_weight.py",
)
D5 = NORMALIZED.D5

EXPECTED_LEDGER_SHA256 = (
    "2ecee35a9284d8bcbc8955122ec3b2c7ca65a2b5002d800dbea2616db6967824"
)
SELECTED_ROW = bytes.fromhex("04237475b8cfea")
SELECTED_ENDPOINTS = (2, 5)
SELECTED_CAP = (
    (-1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
)
PERTURBING_SPOKE = (0, 2, 0, 0)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def path_data(row):
    """Return components, degrees, and endpoints for a simple forest."""
    multiplicities = Counter()
    adjacency = {vertex: set() for vertex in range(8)}
    for variable in row:
        left, right, _left_colour, _right_colour = D5.COORDINATES[variable]
        multiplicities[left, right] += 1
        adjacency[left].add(right)
        adjacency[right].add(left)
    if len(row) != len(set(row)) or len(multiplicities) != len(row):
        return None
    if max(map(len, adjacency.values())) > 2:
        return None

    seen = set()
    components = []
    for root in range(8):
        if root in seen:
            continue
        seen.add(root)
        stack = [root]
        component = []
        while stack:
            vertex = stack.pop()
            component.append(vertex)
            for neighbour in adjacency[vertex]:
                if neighbour not in seen:
                    seen.add(neighbour)
                    stack.append(neighbour)
        components.append(tuple(sorted(component)))
    if len(multiplicities) - 8 + len(components):
        return None
    endpoints = tuple(
        vertex for vertex in range(8) if len(adjacency[vertex]) == 1
    )
    return components, adjacency, endpoints


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position, second in enumerate(vertices[1:]):
        remaining = vertices[1:position + 1] + vertices[position + 2:]
        edge = (min(first, second), max(first, second))
        for tail in perfect_matchings(remaining):
            answer.append((edge,) + tail)
    return tuple(answer)


def pure_target_audit():
    """Enumerate the physical target after exact support normalization."""
    pure_terms = []
    pure_full_lifts = []
    for colour in range(3):
        normalized_to_full = {}
        code = D5.word_code((colour,) * 8)
        for full in D5.iter_word_terms(code):
            normalized = bytes(
                variable for variable in full
                if variable not in D5.SUPPORT_IDS
            )
            require(normalized not in normalized_to_full,
                    "one pure hafnian acquired a normalized term collision")
            normalized_to_full[normalized] = full
        require(len(normalized_to_full) == 105,
                "pure matching census changed")
        pure_terms.append(tuple(normalized_to_full))
        pure_full_lifts.append(normalized_to_full)

    target_rows = set()
    degree_histogram = Counter()
    hamilton_rows = []
    endpoint_histogram = Counter()
    support_endpoint_rows = 0
    support_pairs = {
        (left, right)
        for left, right, _left_colour, _right_colour
        in D5.SOURCE.SUPPORT_PRODUCT
    }
    selected_factor = None

    for first in pure_terms[0]:
        for second in pure_terms[1]:
            partial = bytes(sorted(first + second))
            for third in pure_terms[2]:
                row = bytes(sorted(partial + third))
                require(row not in target_rows,
                        "two pure matching triples collided after normalization")
                target_rows.add(row)
                degree_histogram[len(row)] += 1
                if len(row) != 7:
                    continue
                record = path_data(row)
                if record is None:
                    continue
                components, _adjacency, endpoints = record
                if tuple(sorted(map(len, components), reverse=True)) != (8,):
                    continue
                hamilton_rows.append(row)
                endpoint_histogram[endpoints] += 1
                if endpoints in support_pairs:
                    support_endpoint_rows += 1
                if row == SELECTED_ROW:
                    selected_factor = (
                        pure_full_lifts[0][first],
                        pure_full_lifts[1][second],
                        pure_full_lifts[2][third],
                    )

    require(len(target_rows) == 105 ** 3,
            "normalized pure product lost unique source provenance")
    require(degree_histogram == Counter({
        0: 1, 2: 36, 3: 96, 4: 612, 5: 2304, 6: 9120,
        7: 25344, 8: 73584, 9: 171008, 10: 313920,
        11: 345600, 12: 216000,
    }), "normalized pure-target degree histogram changed")
    require(len(hamilton_rows) == 5596,
            "pure-target Hamilton-row census changed")
    require(support_endpoint_rows == 5388,
            "support-active Hamilton endpoint census changed")
    require(selected_factor is not None,
            "selected physical Hamilton target row disappeared")
    require(tuple(item.hex() for item in selected_factor)
            == ("0075cfea", "0482b8ee", "23747de9"),
            "selected pure matching triple changed")

    return {
        "rows": target_rows,
        "degree_histogram": degree_histogram,
        "hamilton_rows": tuple(hamilton_rows),
        "endpoint_histogram": endpoint_histogram,
        "support_endpoint_rows": support_endpoint_rows,
        "selected_factor": selected_factor,
    }


def first_cell_terminal_extensions(target_rows):
    """Compare the first mixed-source forest cell with the physical target."""
    polynomial = WEIGHTED.reconstruct_degree6_cell()
    path_terms = []
    extensions = set()
    support_join_occurrences = 0
    for row in polynomial:
        if len(row) != 6:
            continue
        record = path_data(row)
        if record is None:
            continue
        components, adjacency, _endpoints = record
        component_sizes = tuple(sorted(map(len, components), reverse=True))
        if component_sizes not in ((6, 2), (4, 4)):
            continue
        path_terms.append(row)
        require(any(
            D5.COORDINATES[variable][2]
            != D5.COORDINATES[variable][3]
            for variable in row
        ), "a first-cell path term unexpectedly became target-diagonal")

        component_endpoints = [
            tuple(vertex for vertex in component
                  if len(adjacency[vertex]) == 1)
            for component in components
        ]
        require(len(component_endpoints) == 2
                and all(len(item) == 2 for item in component_endpoints),
                "degree-six path components lost two endpoints")
        for left in component_endpoints[0]:
            for right in component_endpoints[1]:
                for left_colour in range(3):
                    for right_colour in range(3):
                        coordinate = D5.SOURCE.edge(
                            left, right, left_colour, right_colour
                        )
                        variable = D5.COORDINATE_ID[coordinate]
                        if variable in D5.SUPPORT_IDS:
                            support_join_occurrences += 1
                            continue
                        extensions.add(bytes(sorted(row + bytes((variable,)))))

    require(len(path_terms) == 300,
            "first compatibility cell path-term census changed")
    require(len(extensions) == 10173,
            "normalized legal terminal-extension census changed")
    require(support_join_occurrences == 627,
            "support-unit join occurrence census changed")
    intersection = extensions.intersection(target_rows)
    require(not intersection,
            "a first-cell terminal extension entered the physical target")
    return {
        "path_terms": tuple(path_terms),
        "extensions": extensions,
        "support_join_occurrences": support_join_occurrences,
    }


def cap_error(extra_coordinates=()):
    """Compute the N=8 clean-cap error on the selected coordinate lift.

    In the site-square-zero algebra the coefficient of a word on the six
    residual sites in

        s r^2 x / 2 + r^3 / 6

    is the sum over perfect matchings with either one x-edge and two
    r-edges, or three r-edges.  This avoids any division and is exact over
    the integers.
    """
    blocks = {edge: {} for edge in combinations(range(8), 2)}

    def add_coordinate(coordinate):
        left, right, left_colour, right_colour = coordinate
        matrix = blocks[left, right]
        key = (left_colour, right_colour)
        matrix[key] = matrix.get(key, 0) + 1

    for coordinate in D5.SOURCE.SUPPORT_PRODUCT:
        add_coordinate(coordinate)
    for variable in SELECTED_ROW:
        add_coordinate(D5.COORDINATES[variable])
    for coordinate in extra_coordinates:
        add_coordinate(coordinate)

    def matrix(left, right):
        if left < right:
            return blocks[left, right]
        return {
            (right_colour, left_colour): value
            for (left_colour, right_colour), value
            in blocks[right, left].items()
        }

    p, q = SELECTED_ENDPOINTS
    residual = tuple(vertex for vertex in range(8) if vertex not in (p, q))
    scalar = sum(
        SELECTED_CAP[left_colour][right_colour] * value
        for (left_colour, right_colour), value in matrix(p, q).items()
    )
    kappa = tuple(SELECTED_CAP[colour][colour] for colour in range(3))

    direct = {}
    response = {}
    for position, left in enumerate(residual):
        for right in residual[position + 1:]:
            direct[left, right] = matrix(left, right)
            output = {}
            for (p_colour, left_colour), first in matrix(p, left).items():
                for (q_colour, right_colour), second in matrix(q, right).items():
                    key = (left_colour, right_colour)
                    output[key] = output.get(key, 0) + (
                        first * second * SELECTED_CAP[p_colour][q_colour]
                    )
            for (p_colour, right_colour), first in matrix(p, right).items():
                for (q_colour, left_colour), second in matrix(q, left).items():
                    key = (left_colour, right_colour)
                    output[key] = output.get(key, 0) + (
                        first * second * SELECTED_CAP[p_colour][q_colour]
                    )
            response[left, right] = {
                key: value for key, value in output.items() if value
            }

    error = {}
    matchings = perfect_matchings(residual)
    for word in product(range(3), repeat=6):
        colour = dict(zip(residual, word))
        coefficient = 0
        for matching in matchings:
            all_response = 1
            for edge in matching:
                left, right = edge
                all_response *= response[edge].get(
                    (colour[left], colour[right]), 0
                )
            coefficient += all_response

            for direct_edge in matching:
                left, right = direct_edge
                term = direct[direct_edge].get(
                    (colour[left], colour[right]), 0
                )
                for edge in matching:
                    if edge == direct_edge:
                        continue
                    first, second = edge
                    term *= response[edge].get(
                        (colour[first], colour[second]), 0
                    )
                coefficient += scalar * term
        if coefficient:
            error[word] = coefficient
    return scalar, kappa, error


def audit():
    target = pure_target_audit()
    first_cell = first_cell_terminal_extensions(target["rows"])

    selected_record = path_data(SELECTED_ROW)
    require(selected_record is not None,
            "selected target row stopped being a Hamilton path")
    selected_components, _selected_adjacency, selected_endpoints = selected_record
    require(tuple(map(len, selected_components)) == (8,)
            and selected_endpoints == SELECTED_ENDPOINTS,
            "selected target endpoints changed")
    require((2, 5, 0, 0) in D5.SOURCE.SUPPORT_PRODUCT,
            "selected endpoint direct support coordinate disappeared")
    require(PERTURBING_SPOKE not in D5.SOURCE.SUPPORT_PRODUCT,
            "perturbing spoke entered the chart support")
    require(D5.COORDINATE_ID[PERTURBING_SPOKE] not in SELECTED_ROW,
            "perturbing spoke entered the terminal row")

    scalar, kappa, base_error = cap_error()
    require((scalar, kappa, base_error) == (-1, (-1, 1, 1), {}),
            "selected coordinate-face cap stopped being clean and active")
    perturbed_scalar, perturbed_kappa, perturbed_error = cap_error(
        (PERTURBING_SPOKE,)
    )
    require(perturbed_scalar == scalar and perturbed_kappa == kappa,
            "off-path spoke changed cap activity")
    require(perturbed_error == {
        (0, 2, 0, 2, 2, 0): 2,
        (0, 2, 0, 2, 2, 1): 2,
        (0, 2, 2, 2, 2, 0): 2,
        (0, 2, 2, 2, 2, 1): 2,
    }, "off-path lift-indeterminacy witness changed")

    ledger = {
        "normalized_pure_target_rows": len(target["rows"]),
        "normalized_pure_target_degree_histogram": dict(sorted(
            target["degree_histogram"].items()
        )),
        "degree7_pure_target_rows": target["degree_histogram"][7],
        "degree7_pure_target_hamilton_rows": len(target["hamilton_rows"]),
        "hamilton_rows_with_support_endpoint_pair": (
            target["support_endpoint_rows"]
        ),
        "hamilton_rows_without_support_endpoint_pair": (
            len(target["hamilton_rows"]) - target["support_endpoint_rows"]
        ),
        "selected_target_row": SELECTED_ROW.hex(),
        "selected_target_endpoints": list(SELECTED_ENDPOINTS),
        "selected_unique_pure_matching_triple": [
            item.hex() for item in target["selected_factor"]
        ],
        "first_degree6_path_terms": len(first_cell["path_terms"]),
        "first_cell_normalized_terminal_extensions": len(
            first_cell["extensions"]
        ),
        "first_cell_support_unit_join_occurrences": (
            first_cell["support_join_occurrences"]
        ),
        "first_cell_terminal_target_intersection": 0,
        "selected_cap": [list(row) for row in SELECTED_CAP],
        "selected_cap_scalar": scalar,
        "selected_cap_kappa": list(kappa),
        "selected_coordinate_face_error_support": len(base_error),
        "perturbing_spoke": list(PERTURBING_SPOKE),
        "perturbed_cap_scalar": perturbed_scalar,
        "perturbed_cap_kappa": list(perturbed_kappa),
        "perturbed_error": [
            [list(word), coefficient]
            for word, coefficient in sorted(perturbed_error.items())
        ],
        "conclusion": (
            "chart 26 contains uniquely sourced physical Hamilton target "
            "rows with active clean coordinate-face caps, but the first "
            "mixed forest cell does not reach them and one invisible "
            "off-path spoke changes the terminal clean-cap error"
        ),
        "scope_guard": (
            "this is an exact chart-local terminal counterexample to a "
            "monomial-only readout, not a uniform clean-pair existence "
            "theorem or a proof about an exact ternary source"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return ledger, digest


def main():
    ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                "frozen terminal Hamilton-readout ledger changed")
    print(
        "n=8 chart26 terminal Hamilton readout: PASS; "
        "target paths=5596, first-cell intersection=0, "
        "lift error 0->4"
    )
    print(json.dumps(ledger, sort_keys=True))
    print("sha256:", digest)


if __name__ == "__main__":
    main()
