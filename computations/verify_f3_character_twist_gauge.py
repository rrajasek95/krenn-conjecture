#!/usr/bin/env python3
"""Verify that all character-twisted F_3 slices are gauge-equivalent.

This checker is deliberately solver-free.  It exhausts all 8^3 character
triples, every edge and ordered colour pair, and independently enumerates the
GL(3,2) x S_3 orbits of character triples.
"""

from __future__ import annotations

from itertools import permutations, product

from search_f3_character_twisted_n8 import character, descriptor
from search_f3_translation_invariant_n8 import N, Q, VERTICES


EXPECTED_CLASSES = {
    (0, 0, 0): 1,
    (0, 0, 1): 21,
    (0, 1, 1): 21,
    (0, 1, 2): 126,
    (1, 1, 1): 7,
    (1, 1, 2): 126,
    (1, 2, 3): 42,
    (1, 2, 4): 168,
}


def invertible_linear_maps():
    """Return the 168 maps in GL(3,2), encoded by basis images."""

    answer = []
    for images in permutations(range(1, N), 3):
        image_set = {apply_linear(images, vector) for vector in VERTICES}
        if len(image_set) == N:
            answer.append(images)
    assert len(answer) == 168
    return tuple(answer)


def apply_linear(images, vector):
    image = 0
    for basis_index, basis_vector in enumerate((1, 2, 4)):
        if vector & basis_vector:
            image ^= images[basis_index]
    return image


def triple_orbit(triple, linear_maps):
    return {
        tuple(apply_linear(linear_map, triple[permutation[index]])
              for index in range(Q))
        for linear_map in linear_maps
        for permutation in permutations(range(Q))
    }


def verify_classification():
    linear_maps = invertible_linear_maps()
    unseen = set(product(VERTICES, repeat=Q))
    observed = {}
    while unseen:
        representative = min(unseen)
        orbit = triple_orbit(representative, linear_maps)
        assert orbit <= unseen
        observed[representative] = len(orbit)
        unseen -= orbit
    assert observed == EXPECTED_CLASSES, observed
    assert sum(observed.values()) == N ** Q


def verify_gauge_identity():
    # A character is multiplicative on the additive group F_2^3.
    for character_vector in VERTICES:
        for left_vertex in VERTICES:
            for right_vertex in VERTICES:
                assert (
                    character(character_vector, left_vertex ^ right_vertex)
                    == character(character_vector, left_vertex)
                    * character(character_vector, right_vertex) % 3
                )

    for characters in product(VERTICES, repeat=Q):
        for u in VERTICES:
            for v in VERTICES:
                if u >= v:
                    continue
                difference = u ^ v
                for left_colour in range(Q):
                    for right_colour in range(Q):
                        # Given a symmetric untwisted entry C_d(i,j), i<=j,
                        # the encoded character-twisted variable is
                        # B_d(i,j)=chi_j(d) C_d(i,j).  Check that the
                        # production descriptor evaluates it as the vertex
                        # gauge chi_a(u) chi_b(v) C_d(a,b).
                        key, descriptor_sign = descriptor(
                            u, v, left_colour, right_colour, characters
                        )
                        encoded_right_colour = key[2]
                        encoded_sign = character(
                            characters[encoded_right_colour], difference
                        )
                        actual_sign = descriptor_sign * encoded_sign % 3
                        gauge_sign = (
                            character(characters[left_colour], u)
                            * character(characters[right_colour], v)
                        ) % 3
                        assert actual_sign == gauge_sign, (
                            characters, u, v, left_colour, right_colour,
                            actual_sign, gauge_sign,
                        )

                        # The production descriptor must also be independent
                        # of which endpoint is used to orient the edge.
                        assert descriptor(
                            u, v, left_colour, right_colour, characters
                        ) == descriptor(
                            v, u, right_colour, left_colour, characters
                        )

    # On a pure colouring the matching-independent gauge factor is one.
    # A nontrivial character is -1 at exactly four of the eight vertices.
    for character_vector in VERTICES:
        pure_factor = 1
        for vertex in VERTICES:
            pure_factor = (
                pure_factor * character(character_vector, vertex)
            ) % 3
        assert pure_factor == 1, (character_vector, pure_factor)


def main():
    verify_classification()
    verify_gauge_identity()
    print(
        "PASS character_triples=512 classes=8 linear_maps=168 "
        "edge_colour_checks=129024 pure_target_checks=8"
    )


if __name__ == "__main__":
    main()
