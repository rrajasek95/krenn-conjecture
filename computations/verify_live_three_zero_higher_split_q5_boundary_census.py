#!/usr/bin/env python3
"""Exact census for the higher-split q=5 truncated-mass boundary."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_live_three_zero_higher_split_collision_frontier as frontier


def require(condition: object, message: str) -> None:
    """Check a load-bearing condition in a way ``python3 -O`` cannot remove."""

    if not condition:
        raise ValueError(message)


@dataclass(frozen=True)
class Selection:
    d: int
    selected_triples: int
    complement: tuple[int, ...]


def formal_selections(
    profile: tuple[int, ...], h: int, p: int
) -> tuple[Selection, ...]:
    """All d=0,1,2 formal selections, including one possible triple."""
    answer = []
    for d in (0, 1, 2):
        singleton_layers = h + 2 - 2 * d
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
            require(
                sum(complement_tuple) == p,
                "sum(complement_tuple) == p",
            )
            answer.append(Selection(d, selected_triples, complement_tuple))
    return tuple(answer)


def applicability_formula(profile: tuple[int, ...], h: int) -> bool:
    n1 = profile.count(1)
    n2 = profile.count(2)
    n3 = profile.count(3)
    return (
        n1 >= h + 2
        or (n1 >= h and (n2 >= 1 or n3 >= 1))
        or (
            n1 >= h - 2
            and (n2 >= 2 or (n2 >= 1 and n3 >= 1))
        )
    )


def high_excess(profile: tuple[int, ...]) -> int:
    return sum(max(0, part - 3) for part in profile)


def capped_mass(profile: tuple[int, ...]) -> int:
    return sum(min(part, 3) for part in profile)


EXPECTED = {
    18: {
        13: (2174, 467, 417, 50),
        14: (3255, 542, 492, 50),
        15: (4836, 612, 562, 50),
        16: (6752, 656, 606, 50),
        17: (9365, 699, 649, 50),
    },
    19: {
        13: (2407, 548, 454, 94),
        14: (3626, 643, 549, 94),
        15: (5446, 737, 643, 94),
        16: (7625, 807, 713, 94),
        17: (10654, 858, 764, 94),
        18: (14247, 901, 807, 94),
    },
}


def symbolic_survivors(h: int, p: int) -> set[tuple[int, ...]]:
    """Profiles allowed by applicability and E <= p-18."""
    total = p + h + 2
    answer = set()
    for profile in frontier.partitions(total):
        if not applicability_formula(profile, h):
            continue
        if high_excess(profile) > p - 18:
            continue
        if profile == (1,) * total:
            continue
        answer.add(profile)
    return answer


def check_tables() -> None:
    for p, rows in EXPECTED.items():
        for h, expected in rows.items():
            k = p - h
            require(
                k >= 1,
                "k >= 1",
            )

            # q=6 is excluded, so the row kernel is four- or
            # five-dimensional.
            q6_gap = 22 - h + max(0, 6 - k)
            require(
                q6_gap > 0,
                "q6_gap > 0",
            )

            _, residual_tuple = frontier.census(h, p)
            residuals = set(residual_tuple)
            applicable = set()
            closed = set()
            survivors = set()

            for profile in residuals:
                selections = formal_selections(profile, h, p)
                require(
                    bool(selections) == applicability_formula(profile, h),
                    "bool(selections) == applicability_formula(profile, h)",
                )
                if not selections:
                    continue
                applicable.add(profile)

                # High parts are untouched by every allowed selection.
                for selection in selections:
                    require(
                        high_excess(selection.complement) == high_excess(
                            profile
                        ),
                        "high_excess(selection.complement) == high_excess( profile )",
                    )
                    require(
                        capped_mass(selection.complement) == (
                            p - high_excess(profile)
                        ),
                        "capped_mass(selection.complement) == ( p - high_excess(pr...",
                    )

                if high_excess(profile) > p - 18:
                    closed.add(profile)
                else:
                    survivors.add(profile)

            observed = (
                len(residuals),
                len(applicable),
                len(closed),
                len(survivors),
            )
            require(
                observed == expected,
                "observed == expected",
            )
            require(
                survivors == symbolic_survivors(h, p),
                "survivors == symbolic_survivors(h, p)",
            )


def check_first_symbolic_families() -> None:
    # p=18: only triples, doubles, and singletons survive.  The translated
    # exponent equation and applicability conditions give 51 profiles
    # including D, hence exactly 50 residual profiles.
    p18_parameters = set()
    for triples in range(20):
        for doubles in range(20):
            u = 20 - 3 * triples - 2 * doubles
            applicable = (
                u >= 2
                or (u >= 0 and triples + doubles >= 1)
                or (
                    u >= -2
                    and (
                        doubles >= 2
                        or (triples >= 1 and doubles >= 1)
                    )
                )
            )
            if applicable:
                p18_parameters.add((triples, doubles, u))
    require(
        len(p18_parameters) == 51,
        "len(p18_parameters) == 51",
    )
    require(
        (0, 0, 20) in p18_parameters,
        "(0, 0, 20) in p18_parameters",
    )

    for h in range(13, 18):
        expected = {
            (3,) * triples + (2,) * doubles + (1,) * (h + u)
            for triples, doubles, u in p18_parameters
            if (triples, doubles, u) != (0, 0, 20)
        }
        require(
            expected == symbolic_survivors(h, 18),
            "expected == symbolic_survivors(h, 18)",
        )

        # Both five-space Wronskians are saturated on p=18.
        k = 18 - h
        for d in (0, 1, 2):
            singletons = h + 2 - 2 * d
            selected_weight = (
                3 * d + 4 * singletons + (5 - k)
            )
            selected_cap = 5 * ((h + 3 - d) + 1 - 5)
            require(
                selected_weight == selected_cap,
                "selected_weight == selected_cap",
            )

        for profile in expected:
            for selection in formal_selections(profile, h, 18):
                complement = selection.complement
                require(
                    max(complement) <= 3,
                    "max(complement) <= 3",
                )
                classes = len(complement)
                dual_weight = (
                    2 * complement.count(1) + complement.count(2)
                )
                dual_cap = 3 * ((classes - 4) + 1 - 3)
                require(
                    dual_weight == dual_cap,
                    "dual_weight == dual_cap",
                )

    # p=19: high excess at most one permits no high part or one four.
    for h in range(13, 19):
        observed = symbolic_survivors(h, 19)
        require(
            all(
                max(profile) <= 4 and profile.count(4) <= 1
                for profile in observed
            ),
            "all( max(profile) <= 4 and profile.count(4) <= 1 for prof...",
        )
        require(
            len(observed) == 94,
            "len(observed) == 94",
        )


def main() -> None:
    check_tables()
    check_first_symbolic_families()
    print("higher-split q=5 boundary census: PASS")
    print("p=18: 50 uniform residual survivors after 417..649 closures")
    print("p=19: 94 uniform residual survivors after 454..807 closures")
    print("q>=6 warning and exact high-excess invariant: audited")


if __name__ == "__main__":
    main()
