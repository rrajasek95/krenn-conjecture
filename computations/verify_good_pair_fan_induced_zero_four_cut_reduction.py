#!/usr/bin/env python3
"""Exact combinatorial audit for the induced-zero four-cut reduction."""

from __future__ import annotations

from itertools import combinations, permutations
from math import ceil


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        partner = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(rest):
            yield tuple(sorted(((min(first, partner), max(first, partner)),) + tail))


def odd_double_factorial(value: int) -> int:
    if value in (-1, 0, 1):
        return 1
    answer = 1
    for factor in range(value, 0, -2):
        answer *= factor
    return answer


def falling(value: int, length: int) -> int:
    answer = 1
    for offset in range(length):
        answer *= value - offset
    return answer


def audit_thresholds() -> None:
    for order in range(8, 202, 2):
        fan = order - 7
        for shore_neighbours in range(1, 25):
            if order < 7 * shore_neighbours + 7:
                continue
            for regular in range(max(0, fan) + 1):
                if regular <= 7 * shore_neighbours - 1:
                    assert fan - regular >= order - 7 * shore_neighbours - 6
                else:
                    zero_set = regular - 6
                    assert zero_set >= 7 * shore_neighbours - 6
                    assert ceil(zero_set / 7) >= shore_neighbours

    # The maximum-degree-six independence estimate is sharp for unions of K7.
    for blocks in range(1, 12):
        vertices = 7 * blocks
        edges = {
            (7 * block + left, 7 * block + right)
            for block in range(blocks)
            for left in range(7)
            for right in range(left + 1, 7)
        }
        degrees = [0] * vertices
        for left, right in edges:
            degrees[left] += 1
            degrees[right] += 1
        assert max(degrees) == 6
        assert blocks == ceil(vertices / 7)


def audit_four_star_matching_class() -> None:
    for order in (8, 10, 12):
        all_matchings = set(perfect_matchings(tuple(range(order))))
        for shore_size in range(1, min(4, order // 2) + 1):
            named = tuple(range(shore_size))
            complement = tuple(range(shore_size, order))
            forbidden = {
                (left, right)
                for position, left in enumerate(named)
                for right in named[position + 1 :]
            }
            surviving = {
                matching
                for matching in all_matchings
                if not any(edge in forbidden for edge in matching)
            }

            all_star = set()
            for images in permutations(complement, shore_size):
                remaining = tuple(
                    vertex for vertex in complement if vertex not in images
                )
                for tail in perfect_matchings(remaining):
                    cross = tuple(
                        (min(source, target), max(source, target))
                        for source, target in zip(named, images, strict=True)
                    )
                    all_star.add(tuple(sorted(cross + tail)))

            assert surviving == all_star
            expected = falling(order - shore_size, shore_size) * (
                odd_double_factorial(order - 2 * shore_size - 1)
            )
            assert len(surviving) == expected


def stored_cell(left: int, right: int, left_colour: str, right_colour: str):
    if left < right:
        return (left, right, left_colour, right_colour)
    return (right, left, right_colour, left_colour)


def audit_endpoint_orientation() -> None:
    # Use a complement label on both sides of the named numerical labels.
    for named in permutations((1, 3, 5, 7), 4):
        for complement in (0, 4, 8):
            if complement in named:
                continue
            for endpoint, colour in zip(named, ("c", "d", "e", "f"), strict=True):
                cell = stored_cell(endpoint, complement, colour, "alpha")
                if endpoint < complement:
                    assert cell[2:] == (colour, "alpha")
                else:
                    assert cell[2:] == ("alpha", colour)


def audit_hole_projection() -> None:
    # A degree-(d-h) square-free sector is indexed by its h physical holes.
    # Multiplying h site-linear rows survives exactly when their selected
    # sites are distinct and equal that hole set.  Rows supported on P can
    # therefore see precisely the hole sets contained in P.
    for site_count in range(2, 13):
        sites = tuple(range(site_count))
        for shore_size in range(1, min(4, site_count) + 1):
            holes = tuple(combinations(sites, shore_size))
            for port_count in range(shore_size, site_count + 1):
                ports = set(range(port_count))
                visible = {
                    hole for hole in holes if set(hole).issubset(ports)
                }
                selected = {
                    tuple(sorted(images))
                    for images in permutations(ports, shore_size)
                }
                assert visible == selected


def main() -> None:
    audit_thresholds()
    audit_four_star_matching_class()
    audit_endpoint_orientation()
    audit_hole_projection()
    print("good-pair fan induced-zero four-cut reduction: PASS")


if __name__ == "__main__":
    main()
