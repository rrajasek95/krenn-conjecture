#!/usr/bin/env python3
"""Exact all-order census for the h=8 mixed-role pair-drop theorem."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_collision_frontier as frontier


H = 8


@dataclass(frozen=True)
class Selection:
    d: int
    selected_triples: int
    complement: tuple[int, ...]

    @property
    def singleton_layers(self) -> int:
        return 10 - 2 * self.d

    @property
    def classes(self) -> int:
        return len(self.complement)

    @property
    def simple_roots(self) -> int:
        return self.complement.count(1)


def formal_selections(profile: tuple[int, ...], k: int) -> tuple[Selection, ...]:
    """All multiplicity types allowed by the all-order theorem."""
    answer = []
    for d in range(5):
        singleton_layers = 10 - 2 * d
        for selected_triples in (0, 1):
            selected_doubles = d - selected_triples
            if selected_doubles < 0:
                continue
            if profile.count(3) < selected_triples:
                continue
            if profile.count(2) < selected_doubles:
                continue
            if profile.count(1) < singleton_layers:
                continue

            complement = list(profile)
            for _ in range(selected_triples):
                complement.remove(3)
                complement.append(1)
            for _ in range(selected_doubles):
                complement.remove(2)
            for _ in range(singleton_layers):
                complement.remove(1)
            complement_tuple = tuple(sorted(complement, reverse=True))

            # Literal construction versus the closed formulas (3).
            assert sum(complement_tuple) == k + 8
            assert len(complement_tuple) == (
                len(profile) + d + selected_triples - 10
            )
            assert complement_tuple.count(1) == (
                profile.count(1)
                - 10
                + 2 * d
                + selected_triples
            )
            answer.append(Selection(d, selected_triples, complement_tuple))
    return tuple(answer)


def audit_legal_pair_graph(
    profile: tuple[int, ...], selection: Selection
) -> int:
    """Audit every zero orbit and the theorem's sole allowed missing edge."""
    d = selection.d
    selected_triples = selection.selected_triples
    selected_doubles = d - selected_triples
    singleton_layers = selection.singleton_layers
    unselected_singletons = profile.count(1) - singleton_layers

    layers = (
        tuple(("T", index) for index in range(selected_triples))
        + tuple(("D", index) for index in range(selected_doubles))
        + tuple(("S", index) for index in range(singleton_layers))
    )
    assert len(layers) == 10 - d

    zero_orbits = [None]
    zero_orbits.extend(layer for layer in layers if layer[0] == "S")
    if unselected_singletons:
        zero_orbits.append(("U", 0))

    for zero in zero_orbits:
        illegal_edges = set()
        for left, right in combinations(layers, 2):
            lowered = {left, right}
            nonzero_guards = unselected_singletons
            if zero is not None and zero[0] == "U":
                nonzero_guards -= 1
            nonzero_guards += sum(
                layer[0] == "T" and layer not in lowered for layer in layers
            )
            nonzero_guards += sum(
                layer[0] == "D" and layer in lowered for layer in layers
            )
            nonzero_guards += sum(
                layer[0] == "S" and layer in lowered and layer != zero
                for layer in layers
            )
            if not nonzero_guards:
                illegal_edges.add(frozenset((left, right)))

        assert len(illegal_edges) <= 1
        if illegal_edges:
            assert selected_triples == 1
            assert zero is not None and zero[0] == "S"
            triple = next(layer for layer in layers if layer[0] == "T")
            assert illegal_edges == {frozenset((triple, zero))}
    return len(zero_orbits)


ROUTES = ("B", "L", "W", "X4", "X3", "I", "D5")


def route_flags(
    profile: tuple[int, ...], k: int
) -> tuple[set[str], tuple[Selection, ...]]:
    selections = formal_selections(profile, k)
    flags: set[str] = set()
    doubles = profile.count(2)
    for selection in selections:
        c = selection.classes
        simple = selection.simple_roots
        if c < 5:
            flags.add("B")
        if c == 5 and simple > 0:
            flags.add("L")
        if c >= 6 and simple > 2 * c - 10:
            flags.add("W")
        double_swap = (
            selection.selected_triples == 0
            and selection.d >= 1
            and c == 5
            and simple == 0
            and selection.complement.count(2) >= 2
        )
        if double_swap and doubles >= 4:
            flags.add("X4")
        if double_swap and doubles == 3:
            # Complement count >=2 and d>=1 force d=1 here.
            assert selection.d == 1
            flags.add("X3")
        if selection.d <= 4:
            flags.add("I")
    if (
        len(profile) == 11
        and doubles >= 8
        and profile.count(1) >= 1
    ):
        flags.add("D5")
    return flags, selections


EXPECTED = {
    # R, A, B, L, W, X4, X3, I, D5, closed, A-open, N-open.  Labels are
    # sequential in the displayed order, so overlaps receive one label.
    1: (35, 24, 12, 7, 5, 0, 0, 0, 0, 24, 0, 11),
    2: (42, 32, 13, 6, 4, 4, 0, 5, 0, 32, 0, 10),
    3: (46, 34, 5, 10, 2, 3, 0, 14, 1, 35, 0, 11),
    4: (46, 35, 5, 5, 1, 3, 0, 21, 1, 36, 0, 10),
    5: (44, 38, 0, 9, 0, 2, 1, 26, 1, 39, 0, 5),
    6: (44, 38, 0, 0, 0, 0, 0, 38, 0, 38, 0, 6),
    7: (40, 37, 0, 0, 0, 0, 0, 37, 0, 37, 0, 3),
    8: (39, 37, 0, 0, 0, 0, 0, 37, 0, 37, 0, 2),
    9: (39, 37, 0, 0, 0, 0, 0, 37, 0, 37, 0, 2),
    10: (39, 38, 0, 0, 0, 0, 0, 38, 0, 38, 0, 1),
}

FORMER_A_OPEN_COUNTS = (0, 0, 1, 1, 1, 3, 2, 1, 1, 1)
assert sum(FORMER_A_OPEN_COUNTS) == 11
assert all(row[-2] == 0 for row in EXPECTED.values())


def profile(triples=0, doubles=0, singletons=0):
    return (3,) * triples + (2,) * doubles + (1,) * singletons


def check_finite_census() -> None:
    fifth_order_sequential = None
    zero_orbits = 0
    for k, expected in EXPECTED.items():
        _, residual_tuple = frontier.census(H, H + k)
        residual = set(residual_tuple)
        applicable = set()
        raw_routes = {route: set() for route in ROUTES}

        for candidate in residual:
            flags, selections = route_flags(candidate, k)
            if selections:
                applicable.add(candidate)
            for selection in selections:
                zero_orbits += audit_legal_pair_graph(candidate, selection)
            for route in flags:
                raw_routes[route].add(candidate)

        used = set()
        sequential = {}
        for route in ROUTES:
            sequential[route] = raw_routes[route] - used
            used |= raw_routes[route]
        observed = (
            len(residual),
            len(applicable),
            *(len(sequential[route]) for route in ROUTES),
            len(used),
            len(applicable - used),
            len(residual - used - applicable),
        )
        assert observed == expected
        if k == 5:
            fifth_order_sequential = sequential

    assert fifth_order_sequential is not None
    expected_linear = {
        profile(5, 3, 2),
        profile(5, 2, 4),
        profile(5, 1, 6),
        profile(5, 0, 8),
        profile(4, 4, 3),
        profile(4, 3, 5),
        profile(4, 2, 7),
        profile(4, 1, 9),
        profile(4, 0, 11),
    }
    assert fifth_order_sequential["L"] == expected_linear
    assert fifth_order_sequential["X4"] == {
        profile(3, 6, 2),
        profile(3, 4, 6),
    }
    assert fifth_order_sequential["X3"] == {profile(3, 3, 8)}
    assert len(fifth_order_sequential["I"]) == 26
    assert fifth_order_sequential["D5"] == {profile(2, 8, 1)}

    boundary = profile(3, 2, 10)
    flags, selections = route_flags(boundary, 5)
    assert selections and flags == {"I"}
    assert any(
        selection.d == 0
        and selection.selected_triples == 0
        and selection.complement == profile(3, 2, 0)
        for selection in selections
    )

    fifth_residual = set(frontier.census(H, H + 5)[1])
    fifth_closed = set().union(
        *(fifth_order_sequential[route] for route in ROUTES)
    )
    expected_survivors = {
        (4, 4) + (3,) * 5,
        profile(5, 4, 0),
        profile(4, 5, 1),
        profile(3, 7, 0),
        profile(0, 11, 1),
    }
    assert fifth_residual - fifth_closed == expected_survivors

    # This was the sole fifth-order member of the former d=4 formal tail.
    former_tail_member = profile(0, 10, 3)
    former_tail_flags, former_tail_selections = route_flags(
        former_tail_member, 5
    )
    assert former_tail_flags == {"I"}
    assert any(selection.d == 4 for selection in former_tail_selections)
    assert zero_orbits > 0


def repeated_degree_cap(repeated_classes: int) -> int:
    """Maximum repeated-label contribution under lambda_1+lambda_2<=7."""
    if repeated_classes == 0:
        return 0
    if repeated_classes == 1:
        return 6
    return 3 * repeated_classes + 1


def check_uniform_tail_bounds() -> None:
    # Abstractly exhaust the integer invariants occurring in (2)--(3).
    maxima = {"B": 0, "L": 0, "W": 0}
    for d in range(5):
        singleton_layers = 10 - 2 * d
        for selected_triples in (0, 1):
            if selected_triples > d:
                continue
            for singletons in range(singleton_layers, 101):
                for repeated in range(max(1, d), 101):
                    classes = singletons + repeated
                    c = classes + d + selected_triples - 10
                    simple = (
                        singletons - 10 + 2 * d + selected_triples
                    )
                    total_cap = singletons + repeated_degree_cap(repeated)
                    if c < 5:
                        maxima["B"] = max(maxima["B"], total_cap)
                    if c == 5 and simple > 0:
                        maxima["L"] = max(maxima["L"], total_cap)
                    if c >= 6 and simple > 2 * c - 10:
                        maxima["W"] = max(maxima["W"], total_cap)
    assert maxima == {"B": 27, "L": 28, "W": 27}

    # On a swap profile, c=5 and j=0 give n1=10-2d and rho=5+d.
    # At least d+2 classes are doubles, leaving at most three higher
    # repeated classes.  Audit the sharp contribution of those classes.
    swap_cap = 0
    for d in range(1, 5):
        singletons = 10 - 2 * d
        repeated = 5 + d
        for doubles in range(d + 2, repeated + 1):
            if doubles < 3:
                continue
            higher = repeated - doubles
            if higher == 0:
                higher_cap = 0
            elif higher == 1:
                higher_cap = 5
            else:
                higher_cap = 3 * higher + 1
            total_cap = singletons + 2 * doubles + higher_cap
            swap_cap = max(swap_cap, total_cap)
    assert swap_cap == 24

    # Consequently no Section-3 criterion can occur once M=k+18>28.
    assert 10 + 18 == 28
    assert 11 + 18 > max(*maxima.values(), swap_cap)


def check_infinite_applicable_incidence_family() -> None:
    for k in range(1, 41):
        candidate = (2,) + (1,) * (k + 16)
        assert sum(candidate) == k + 18
        assert frontier.classify(candidate, H, H + k) == "R"
        flags, selections = route_flags(candidate, k)
        assert selections
        d_zero = next(
            selection
            for selection in selections
            if selection.d == 0 and selection.selected_triples == 0
        )
        assert d_zero.classes == k + 7
        assert d_zero.simple_roots == k + 6
        assert "I" in flags
        assert ("W" in flags) == (k == 1)
        if k >= 2:
            assert flags == {"I"}


def check_closed_form_incidence_and_tail() -> None:
    """Audit the all-d incidence formula and vanished d=4 tail."""
    for singletons in range(31):
        for doubles in range(16):
            for triples in range(8):
                selection_types = []
                for d in range(5):
                    singleton_layers = 10 - 2 * d
                    for selected_triples in (0, 1):
                        selected_doubles = d - selected_triples
                        if selected_doubles < 0:
                            continue
                        if (
                            singletons >= singleton_layers
                            and doubles >= selected_doubles
                            and triples >= selected_triples
                        ):
                            selection_types.append((d, selected_triples))

                incidence_formula = (
                    singletons >= 10
                    or (
                        singletons >= 8
                        and (doubles >= 1 or triples >= 1)
                    )
                    or (
                        singletons >= 6
                        and (
                            doubles >= 2
                            or (doubles >= 1 and triples >= 1)
                        )
                    )
                    or (
                        singletons >= 4
                        and (
                            doubles >= 3
                            or (doubles >= 2 and triples >= 1)
                        )
                    )
                    or (
                        singletons >= 2
                        and (
                            doubles >= 4
                            or (doubles >= 3 and triples >= 1)
                        )
                    )
                )
                observed_incidence = bool(selection_types)
                assert incidence_formula == observed_incidence

                former_tail_formula = singletons in (2, 3) and (
                    doubles >= 4
                    or (doubles >= 3 and triples >= 1)
                )
                observed_former_tail = bool(selection_types) and not any(
                    d <= 3 for d, _ in selection_types
                )
                assert former_tail_formula == observed_former_tail
                assert not (bool(selection_types) and not observed_incidence)

                if singletons < 2:
                    no_selection_formula = True
                elif singletons < 4:
                    no_selection_formula = (
                        doubles <= 2
                        or (doubles == 3 and triples == 0)
                    )
                elif singletons < 6:
                    no_selection_formula = (
                        doubles <= 1
                        or (doubles == 2 and triples == 0)
                    )
                elif singletons < 8:
                    no_selection_formula = (
                        doubles == 0
                        or (doubles == 1 and triples == 0)
                    )
                elif singletons < 10:
                    no_selection_formula = doubles == 0 and triples == 0
                else:
                    no_selection_formula = False
                assert no_selection_formula == (not selection_types)

    # The algebraic M caps prove that no B/L/W/X route reaches k>=11.
    # Check the first ten tail slices as a separate census sanity test.
    for k in range(11, 21):
        _, residuals = frontier.census(H, H + k)
        for candidate in residuals:
            flags, _ = route_flags(candidate, k)
            assert not (flags & {"B", "L", "W", "X4", "X3", "D5"})


def main() -> None:
    check_finite_census()
    check_uniform_tail_bounds()
    check_infinite_applicable_incidence_family()
    check_closed_form_incidence_and_tail()
    print("h=8 all-order mixed-role collision census: PASS")
    print("complementary closure window: k=1..5")
    print("d=0..4 incidence, D5 endpoint, and no-selection tail: exact")


if __name__ == "__main__":
    main()
