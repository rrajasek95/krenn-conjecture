#!/usr/bin/env python3
r"""Uniform second-cofactor tower gate for the one-bad response circuit.

An actual unary-top q is augmented by four top-inactive coloured bridge
cells.  Replace its four response-hole first cofactors by the 9b26452
minimum-response circuit.  Symmetric corrections to the second-cofactor
family then make both Euler layers exact:

    sum_e q_e F_e = h q^[h],
    sum_f q_f G_{e,f} = (h-1) F_e.

The endpoint response rows remain (X1,0,0,X2) and p1,p2 remain non-square.
The hierarchy first fails at

    sum_g q_g H_{e,f,g} = (h-2) G_{e,f}

on four edge pairs.  The corrected G is formal, not the actual second
derivative of q.  Requiring actual G uniquely restores actual F and hence
kills this sharp guard; it does not prove general one-bad concentration.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_one_bad_common_q_euler_hessian_gate.py":
        "99875dd9b500c8ba1e9d33063b4fc69b0710d99f73522f6174679a4b172cdc6d",
    "notes/uniform-one-bad-common-q-euler-hessian-gate.md":
        "6ff05d4d82cc51c3e4567edb4a2a167ab296763e8319f20783b61c68a06a4f96",
    "computations/verify_uniform_one_bad_minimal_response_counterguard.py":
        "57d0a980a26f50bc236f2dcf0b468584a801be049e3cc8cc9418ab0e08ed3b04",
    "computations/verify_uniform_one_bad_square_zero_clean_cap.py":
        "a943fffdc3ce86aa5506e6774ec3a6a8ff10c70491225417152a1298e2754883",
}
EXPECTED_LEDGER_SHA256 = "f38e60434d26fb23ac5c8828d9e894085bd8063c92045a96da754b094a7ccab5"

Edge = tuple[int, int]
Cell = tuple[tuple[int, int], Fraction]


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def load_module(relative: str, name: str):
    path = ROOT / relative
    specification = importlib.util.spec_from_file_location(name, path)
    require(specification is not None and specification.loader is not None,
            f"cannot load {relative}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def normalized_edge(left: int, right: int) -> Edge:
    return (left, right) if left < right else (right, left)


def q_cells(h: int) -> dict[Edge, tuple[Cell, ...]]:
    require(h >= 3, "the tower starts at h=3")
    cells: dict[Edge, list[Cell]] = {}

    def put(edge: Edge, colours: tuple[int, int], coefficient=1) -> None:
        edge = normalized_edge(*edge)
        cells.setdefault(edge, []).append((colours, Fraction(coefficient)))

    # Unary top matching.
    for site in range(0, 2 * h, 2):
        put((site, site + 1), (0, 0))

    # Four coloured bridges.  Each is top-inactive: its two displaced unary
    # partners have no connecting edge.  They expose exactly the colours
    # needed to integrate the four first-cofactor response corrections.
    put((1, 4), (1, 1))
    put((0, 4), (1, 1))
    put((3, 5), (2, 2))
    put((2, 5), (2, 2))
    return {edge: tuple(entries) for edge, entries in cells.items()}


def matching_tensor(h: int, removed: frozenset[int]) -> Counter:
    cells = q_cells(h)
    vertices = tuple(site for site in range(2 * h) if site not in removed)
    order = vertices

    def recurse(remaining: tuple[int, ...]):
        if not remaining:
            yield {}, Fraction(1)
            return
        left = remaining[0]
        remaining_set = set(remaining)
        for right in remaining[1:]:
            edge = normalized_edge(left, right)
            for colours, coefficient in cells.get(edge, ()):
                rest = tuple(site for site in remaining
                             if site not in (left, right))
                for assignment, tail in recurse(rest):
                    updated = dict(assignment)
                    if edge == (left, right):
                        updated[left], updated[right] = colours
                    else:
                        updated[left], updated[right] = colours[::-1]
                    yield updated, coefficient * tail

    output = Counter()
    for assignment, coefficient in recurse(vertices):
        output[tuple(assignment[site] for site in order)] += coefficient
    return Counter({word: coefficient for word, coefficient in output.items()
                    if coefficient})


def all_edges(h: int) -> tuple[Edge, ...]:
    return tuple((left, right) for left in range(2 * h)
                 for right in range(left + 1, 2 * h))


def scale_tensor(tensor: Counter, scalar: Fraction) -> Counter:
    return Counter({word: scalar * coefficient
                    for word, coefficient in tensor.items()
                    if scalar * coefficient})


def subtract_tensors(left: Counter, right: Counter) -> Counter:
    answer = Counter(left)
    answer.subtract(right)
    return Counter({word: coefficient for word, coefficient in answer.items()
                    if coefficient})


def add_tensors(left: Counter, right: Counter) -> Counter:
    answer = Counter(left)
    answer.update(right)
    return Counter({word: coefficient for word, coefficient in answer.items()
                    if coefficient})


def insert_cell(h: int, removed: frozenset[int], edge: Edge,
                colours: tuple[int, int], tensor: Counter) -> Counter:
    ambient = tuple(site for site in range(2 * h) if site not in removed)
    require(edge[0] in ambient and edge[1] in ambient,
            f"cannot insert {edge} after removing {sorted(removed)}")
    remainder = tuple(site for site in ambient if site not in edge)
    output = Counter()
    for word, coefficient in tensor.items():
        require(len(word) == len(remainder), (len(word), len(remainder)))
        assignment = {edge[0]: colours[0], edge[1]: colours[1]}
        assignment.update(dict(zip(remainder, word, strict=True)))
        output[tuple(assignment[site] for site in ambient)] += coefficient
    return Counter({word: coefficient for word, coefficient in output.items()
                    if coefficient})


def divide_by_cell(h: int, removed: frozenset[int], edge: Edge,
                   colours: tuple[int, int], tensor: Counter) -> Counter:
    ambient = tuple(site for site in range(2 * h) if site not in removed)
    positions = {site: index for index, site in enumerate(ambient)}
    require(edge[0] in positions and edge[1] in positions, edge)
    keep = tuple(site for site in ambient if site not in edge)
    output = Counter()
    for word, coefficient in tensor.items():
        observed = (word[positions[edge[0]]], word[positions[edge[1]]])
        require(observed == colours,
                f"tensor is not divisible by q_{edge}:{colours}: {observed}")
        output[tuple(word[positions[site]] for site in keep)] += coefficient
    return Counter({word: coefficient for word, coefficient in output.items()
                    if coefficient})


def pair_key(first: Edge, second: Edge) -> tuple[Edge, Edge]:
    return tuple(sorted((first, second)))  # type: ignore[return-value]


def correction_data():
    # response hole -> top-inactive coloured bridge and its unique q cell
    return {
        (0, 5): ((1, 4), (1, 1)),
        (1, 5): ((0, 4), (1, 1)),
        (2, 4): ((3, 5), (2, 2)),
        (3, 4): ((2, 5), (2, 2)),
    }


def audit_order(h: int, minimal) -> dict[str, object]:
    sites, desired_response_f, words = minimal.build_formal_cofactors(h)
    top = matching_tensor(h, frozenset())
    require(top == Counter({(0,) * (2 * h): Fraction(1)}),
            f"the bridge-augmented q lost unary top at h={h}: {top}")

    edges = all_edges(h)
    actual_f = {edge: matching_tensor(h, frozenset(edge)) for edge in edges}
    formal_f = dict(actual_f)
    for holes, tensor in desired_response_f.items():
        formal_f[tuple(sorted(holes))] = Counter(tensor)

    # The four response rows remain exact, including both crossed zeros.
    cofactor_dict = {frozenset(edge): tensor for edge, tensor in formal_f.items()
                     if tensor}
    p1 = ((0, 1, 1), (1, 1, 1))
    s1 = ((5, 1, 1),)
    p2 = ((2, 2, 1), (3, 2, 1))
    s2 = ((4, 2, 1),)
    rows = {
        "11": minimal.response(sites, cofactor_dict, p1, s1),
        "12": minimal.response(sites, cofactor_dict, p1, s2),
        "21": minimal.response(sites, cofactor_dict, p2, s1),
        "22": minimal.response(sites, cofactor_dict, p2, s2),
    }
    require(rows == {
        "11": Counter({words["X1"]: Fraction(1)}),
        "12": Counter(),
        "21": Counter(),
        "22": Counter({words["X2"]: Fraction(1)}),
    }, f"the second-tower responses changed at h={h}")

    # Genuine second-cofactor background, then one symmetric correction for
    # each response hole.  Since q has no cell on a response hole, symmetry
    # does not feed the correction into the bridge-hole recurrence.
    formal_g: dict[tuple[Edge, Edge], Counter] = {}
    for index, first in enumerate(edges):
        for second in edges[index + 1:]:
            if set(first) & set(second):
                continue
            formal_g[pair_key(first, second)] = matching_tensor(
                h, frozenset(first) | frozenset(second)
            )

    correction_pairs = []
    for response_edge, (bridge_edge, bridge_colours) in correction_data().items():
        delta_f = subtract_tensors(formal_f[response_edge], actual_f[response_edge])
        quotient = divide_by_cell(
            h, frozenset(response_edge), bridge_edge, bridge_colours, delta_f
        )
        key = pair_key(response_edge, bridge_edge)
        delta_g = scale_tensor(quotient, Fraction(h - 1))
        formal_g[key] = add_tensors(formal_g[key], delta_g)
        correction_pairs.append((response_edge, bridge_edge, delta_g))

    # Top Euler with formal F.
    top_euler = Counter()
    for edge, entries in q_cells(h).items():
        for colours, coefficient in entries:
            top_euler.update(scale_tensor(insert_cell(
                h, frozenset(), edge, colours, formal_f[edge]
            ), coefficient))
    require(top_euler == scale_tensor(top, Fraction(h)),
            f"top Euler failed at h={h}")

    # First-cofactor Euler for every physical edge, with one symmetric G.
    for first in edges:
        recurrence = Counter()
        removed = frozenset(first)
        for second, entries in q_cells(h).items():
            if set(first) & set(second):
                continue
            g = formal_g[pair_key(first, second)]
            for colours, coefficient in entries:
                recurrence.update(scale_tensor(insert_cell(
                    h, removed, second, colours, g
                ), coefficient))
        require(recurrence == scale_tensor(formal_f[first], Fraction(h - 1)),
                f"first-cofactor Euler failed at h={h}, edge={first}")

    # If the second cofactors were the genuine ones, their Euler recurrence
    # would return actual F, uniquely.  The nonzero corrections certify that
    # no surviving guard here has actual cofactors through level two.
    require(all(delta_g for _, _, delta_g in correction_pairs),
            "a formal Hessian correction disappeared")

    # Third-cofactor recurrence with the genuine H background.  Its right
    # side equals (h-2)*actual_G, so the residual is exactly
    # (h-2)*delta_G on the four corrected pairs.
    third_failures = {}
    for response_edge, bridge_edge, delta_g in correction_pairs:
        removed = frozenset(response_edge) | frozenset(bridge_edge)
        actual_g = matching_tensor(
            h, removed
        )
        formal = formal_g[pair_key(response_edge, bridge_edge)]
        require(subtract_tensors(formal, actual_g) == delta_g,
                "the Hessian correction lost provenance")

        actual_third_rhs = Counter()
        for third, entries in q_cells(h).items():
            if set(third) & removed:
                continue
            actual_h = matching_tensor(h, removed | frozenset(third))
            for colours, coefficient in entries:
                actual_third_rhs.update(scale_tensor(insert_cell(
                    h, removed, third, colours, actual_h
                ), coefficient))
        require(actual_third_rhs == scale_tensor(actual_g, Fraction(h - 2)),
                f"genuine third-cofactor Euler failed at h={h}, "
                f"pair={response_edge}|{bridge_edge}")

        residual = subtract_tensors(
            scale_tensor(formal, Fraction(h - 2)), actual_third_rhs
        )
        require(residual == scale_tensor(delta_g, Fraction(h - 2)),
                "the third-cofactor residual changed")
        require(residual, f"third recurrence became vacuous at h={h}")
        label = f"{response_edge[0]}{response_edge[1]}|{bridge_edge[0]}{bridge_edge[1]}"
        third_failures[label] = len(residual)

    return {
        "h": h,
        "q_top": "X0",
        "q_bridge_cells": ["14:11", "04:11", "35:22", "25:22"],
        "responses": {"11": "X1", "12": "0", "21": "0", "22": "X2"},
        "top_euler": "exact",
        "first_cofactor_euler": "exact with one symmetric formal G",
        "nonzero_self_squares": ["p1^[2]", "p2^[2]"],
        "third_cofactor_failures": third_failures,
    }


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"pinned dependency changed: {relative}")


def main() -> None:
    pin_dependencies()
    minimal = load_module(
        "computations/verify_uniform_one_bad_minimal_response_counterguard.py",
        "minimal_response",
    )
    audits = [audit_order(h, minimal) for h in range(3, 9)]
    ledger = {
        "pins": PINS,
        "uniform_formula": "every h>=3; representative exact audits h=3..8",
        "q": (
            "unary matching 01|23|45|... plus top-inactive bridges "
            "14:11,04:11,35:22,25:22; q^[h]=X0"
        ),
        "properties": audits,
        "verdict": (
            "top Euler and the complete symmetric first-cofactor Euler/Hessian "
            "recurrence do not formally force square-zero response rows"
        ),
        "actual_cofactor_guard": (
            "if G is required to be the genuine second cofactor of q, the "
            "recurrence uniquely forces F to be the genuine first cofactor; "
            "the four nonzero delta_G corrections are therefore forbidden"
        ),
        "first_failure": (
            "the next recurrence (h-2)G_ef=sum_g q_g H_efg fails on "
            "05|14,15|04,24|35,34|25"
        ),
        "next_theorem": (
            "use the genuine third-cofactor recurrence, not a freely corrected "
            "H, to turn every Hessian correction into a source-preserving "
            "row deletion or another active clean descent"
        ),
        "scope": (
            "uniform formal cofactor-tower counterguard with actual q/top; "
            "F and G corrections are not actual q derivatives, so this is "
            "not a one-bad source or Krenn counterexample"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"second-cofactor tower ledger changed: {digest}")

    print("uniform one-bad second-cofactor tower gate: PASS")
    print("actual q: unary top plus four top-inactive coloured bridges")
    print("top Euler and symmetric first-cofactor Euler: exact")
    print("responses: X1,0,0,X2; non-square rows: p1,p2")
    print("actual-G guard: genuine G would uniquely restore genuine F")
    print("first failure: third-cofactor recurrence on four corrected pairs")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
