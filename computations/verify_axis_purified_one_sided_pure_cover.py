#!/usr/bin/env python3
"""Audit the axis-purified one-sided-essential pure-cover obstruction.

At eight sites give each endpoint a distinguished target-axis label.  If a
physical edge can carry a pure-c cell only when at least one endpoint has
label c, then a supported pure-c perfect matching needs at least four
c-labelled vertices.  Three colours would need at least twelve vertices.

The script independently enumerates all 3^8 labelings and all 105 perfect
matchings.  It also freezes the sharp two-colour boundary, where a 4+4
labelling does admit pure matchings for both labels.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json


N = 8
COLOURS = 3


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in matchings(rest):
            yield ((first, second),) + tail


def pure_compatible(matching, labels, colour):
    """Every edge has a colour-labelled endpoint."""

    return all(labels[left] == colour or labels[right] == colour
               for left, right in matching)


def base_three_digits(value):
    digits = []
    for _ in range(N):
        digits.append(value % COLOURS)
        value //= COLOURS
    return tuple(digits)


def audit_three_colour_obstruction(all_matchings):
    profile_census = Counter()
    compatible_labelings = 0
    maximum_colours_realized = 0

    for code in range(COLOURS ** N):
        labels = base_three_digits(code)
        profile = tuple(sorted(Counter(labels).values(), reverse=True))
        profile_census[profile] += 1
        realized = sum(
            any(pure_compatible(matching, labels, colour)
                for matching in all_matchings)
            for colour in range(COLOURS)
        )
        maximum_colours_realized = max(maximum_colours_realized, realized)
        if realized == COLOURS:
            compatible_labelings += 1

    require(compatible_labelings == 0,
            "a three-colour pure-cover labelling survived")
    require(maximum_colours_realized == 2,
            "the sharp number of simultaneously realizable colours changed")
    require(sum(profile_census.values()) == COLOURS ** N,
            "the labelling profile census is incomplete")
    return profile_census, maximum_colours_realized


def audit_two_colour_sharpness(all_matchings):
    labels = (0, 0, 0, 0, 1, 1, 1, 1)
    counts = tuple(
        sum(pure_compatible(matching, labels, colour)
            for matching in all_matchings)
        for colour in range(2)
    )
    # In either colour every matching edge must cross the 4+4 partition.
    require(counts == (24, 24),
            f"the two-colour 4+4 sharp boundary changed: {counts}")
    return counts


def main():
    all_matchings = tuple(matchings(range(N)))
    require(len(all_matchings) == 105,
            "the eight-site perfect-matching count changed")
    profiles, maximum = audit_three_colour_obstruction(all_matchings)
    sharp = audit_two_colour_sharpness(all_matchings)
    ledger = {
        "sites": N,
        "colours": COLOURS,
        "perfect_matchings": len(all_matchings),
        "axis_labelings": COLOURS ** N,
        "three_colour_survivors": 0,
        "maximum_colours_realized": maximum,
        "two_colour_4_plus_4_matching_counts": list(sharp),
        "profile_census": {
            ",".join(map(str, key)): value
            for key, value in sorted(profiles.items())
        },
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    expected = "c09de6ed69c29aa07f35a2cd8e3de4ded3cf9121cf2bf7321f83e334b9d5e08f"
    require(digest == expected,
            f"axis-pure cover ledger changed: {digest}")
    print("axis-purified one-sided pure-cover obstruction: PASS")
    print("three-colour survivors: 0 / 6561")
    print(f"two-colour sharp matching counts: {sharp}")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
