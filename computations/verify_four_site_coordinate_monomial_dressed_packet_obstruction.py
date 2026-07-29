#!/usr/bin/env python3
"""Exact lightweight audit of the four-site monomial multiplier theorem.

Patterns use -1 for an absent local component and 0, 1, 2 for its target
coordinate.  The unweighted audit exhausts all 255^2 ordered nonzero
pattern pairs.  The symbolic audit keeps parity and four Laurent exponents
for edge gains; it is needed only on the 60^2 colour-surjective pairs.
"""

from itertools import product


ABSENT = -1
COLOURS = range(3)
POWERS = (27, 9, 3, 1)
TARGETS = (0, 40, 80)

# (first Q site, second Q site, first complementary site, second
# complementary site)
PAIR_SPLITS = (
    (0, 1, 2, 3),
    (0, 2, 1, 3),
    (0, 3, 1, 2),
    (1, 2, 0, 3),
    (1, 3, 0, 2),
    (2, 3, 0, 1),
)


def all_patterns():
    patterns = list(product((ABSENT, 0, 1, 2), repeat=4))
    patterns.remove((ABSENT,) * 4)
    assert len(patterns) == 255
    return patterns


def find(parent, parity, vertex):
    if parent[vertex] != vertex:
        old_parent = parent[vertex]
        parent[vertex] = find(parent, parity, old_parent)
        parity[vertex] ^= parity[old_parent]
    return parent[vertex]


def unweighted_profile(left, right):
    """Return which target words lie in the unweighted column span."""

    parent = list(range(81))
    parity = [0] * 81
    killed = [False] * 81

    def pin(vertex):
        killed[find(parent, parity, vertex)] = True

    def add_edge(first, second):
        root_first = find(parent, parity, first)
        root_second = find(parent, parity, second)
        value_first = parity[first]
        value_second = parity[second]
        if root_first == root_second:
            # Every unweighted edge imposes y_second = -y_first.
            if value_first ^ value_second != 1:
                killed[root_first] = True
            return
        parent[root_second] = root_first
        parity[root_second] = value_first ^ value_second ^ 1
        killed[root_first] |= killed[root_second]

    for q_site, q_other, first, second in PAIR_SPLITS:
        forward = left[first] >= 0 and right[second] >= 0
        backward = right[first] >= 0 and left[second] >= 0
        if not (forward or backward):
            continue

        forward_base = (
            left[first] * POWERS[first]
            + right[second] * POWERS[second]
            if forward
            else 0
        )
        backward_base = (
            right[first] * POWERS[first]
            + left[second] * POWERS[second]
            if backward
            else 0
        )

        for q_colour, q_other_colour in product(COLOURS, repeat=2):
            q_base = (
                q_colour * POWERS[q_site]
                + q_other_colour * POWERS[q_other]
            )
            if forward and backward:
                first_word = forward_base + q_base
                second_word = backward_base + q_base
                if first_word == second_word:
                    # Its coefficient is 2 in the unweighted audit.
                    pin(first_word)
                else:
                    add_edge(first_word, second_word)
            else:
                pin((forward_base if forward else backward_base) + q_base)

    return tuple(
        bool(killed[find(parent, parity, target)]) for target in TARGETS
    )


def symbolic_upper_profile(left, right):
    """Upper-bound weighted membership using signed Laurent edge gains."""

    adjacency = [[] for _ in range(81)]
    candidate_pins = 0

    for q_site, q_other, first, second in PAIR_SPLITS:
        forward = left[first] >= 0 and right[second] >= 0
        backward = right[first] >= 0 and left[second] >= 0
        if not (forward or backward):
            continue

        forward_base = (
            left[first] * POWERS[first]
            + right[second] * POWERS[second]
            if forward
            else 0
        )
        backward_base = (
            right[first] * POWERS[first]
            + left[second] * POWERS[second]
            if backward
            else 0
        )
        exponent = tuple(
            int(site == first) - int(site == second) for site in range(4)
        )
        reverse_exponent = tuple(-value for value in exponent)

        for q_colour, q_other_colour in product(COLOURS, repeat=2):
            q_base = (
                q_colour * POWERS[q_site]
                + q_other_colour * POWERS[q_other]
            )
            if forward and backward:
                first_word = forward_base + q_base
                second_word = backward_base + q_base
                if first_word == second_word:
                    # A special weight can cancel this pin.  Retaining it
                    # only enlarges the possible membership profile.
                    candidate_pins |= 1 << first_word
                else:
                    adjacency[first_word].append(
                        (second_word, 1, exponent)
                    )
                    adjacency[second_word].append(
                        (first_word, 1, reverse_exponent)
                    )
            else:
                word = (forward_base if forward else backward_base) + q_base
                candidate_pins |= 1 << word

    profile = []
    zero_exponent = (0, 0, 0, 0)
    for target in TARGETS:
        potentials = {target: (0, zero_exponent)}
        stack = [target]
        potentially_killed = bool((candidate_pins >> target) & 1)

        while stack:
            vertex = stack.pop()
            potentially_killed |= bool((candidate_pins >> vertex) & 1)
            sign, current_exponent = potentials[vertex]
            for neighbour, edge_sign, edge_exponent in adjacency[vertex]:
                expected = (
                    sign ^ edge_sign,
                    tuple(
                        current_exponent[index] + edge_exponent[index]
                        for index in range(4)
                    ),
                )
                if neighbour in potentials:
                    # A different signed Laurent potential is a cycle
                    # which can be inconsistent for some weights.
                    potentially_killed |= potentials[neighbour] != expected
                else:
                    potentials[neighbour] = expected
                    stack.append(neighbour)

        profile.append(potentially_killed)

    return tuple(profile)


def profile_counts(patterns, profile_function, exploit_symmetry=False):
    counts = {}
    if exploit_symmetry:
        # Multiplication by TV is symmetric in T,V.
        for first_index, left in enumerate(patterns):
            for second_index in range(first_index, len(patterns)):
                profile = profile_function(left, patterns[second_index])
                multiplicity = 1 if first_index == second_index else 2
                counts[profile] = counts.get(profile, 0) + multiplicity
    else:
        for left in patterns:
            for right in patterns:
                profile = profile_function(left, right)
                counts[profile] = counts.get(profile, 0) + 1
    return counts


def expected_counts(none_count, singleton_count, pair_count):
    return {
        (False, False, False): none_count,
        (True, False, False): singleton_count,
        (False, True, False): singleton_count,
        (False, False, True): singleton_count,
        (True, True, False): pair_count,
        (True, False, True): pair_count,
        (False, True, True): pair_count,
    }


def main():
    patterns = all_patterns()
    unweighted = profile_counts(
        patterns, unweighted_profile, exploit_symmetry=True
    )
    assert unweighted == expected_counts(14502, 13749, 3092)
    assert sum(unweighted.values()) == 255 * 255
    assert (True, True, True) not in unweighted

    onto_patterns = [
        pattern
        for pattern in patterns
        if {value for value in pattern if value >= 0} == set(COLOURS)
    ]
    assert len(onto_patterns) == 60
    onto_unweighted = profile_counts(
        onto_patterns, unweighted_profile, exploit_symmetry=True
    )
    assert onto_unweighted == expected_counts(432, 768, 288)
    assert sum(onto_unweighted.values()) == 60 * 60
    symbolic = profile_counts(onto_patterns, symbolic_upper_profile)
    assert symbolic == expected_counts(432, 768, 288)
    assert sum(symbolic.values()) == 60 * 60
    assert (True, True, True) not in symbolic

    # The four-cycle sharpness pattern retains colours zero and one.
    cyclic_left = (0, 1, ABSENT, ABSENT)
    cyclic_right = (ABSENT, 0, 1, ABSENT)
    assert unweighted_profile(cyclic_left, cyclic_right) == (
        True,
        True,
        False,
    )

    print("four-site coordinate-monomial dressed obstruction: PASS")
    print(
        "unweighted patterns=65025; profiles="
        "14502/13749x3/3092x3/0; "
        "symbolic onto pairs=3600; binary maximum=2"
    )


if __name__ == "__main__":
    main()
