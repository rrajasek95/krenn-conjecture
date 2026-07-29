#!/usr/bin/env python3
"""Audit the finite word-incidence step in the three-witness obstruction."""

from itertools import permutations


COLORS = range(3)


def word_for(sigma, tau, p_partner, q_partner, residual_color):
    assert p_partner != q_partner
    remaining = ({0, 1, 2} - {p_partner, q_partner}).pop()
    word = [None, None, None]
    word[p_partner] = sigma[p_partner]
    word[q_partner] = tau[q_partner]
    word[remaining] = residual_color
    return tuple(word), remaining


def main():
    admissible = []
    for sigma in permutations(COLORS):
        sigma_inverse = {color: sigma.index(color) for color in COLORS}
        for tau in permutations(COLORS):
            tau_inverse = {color: tau.index(color) for color in COLORS}
            if any(
                sigma_inverse[color] == tau_inverse[color]
                for color in COLORS
            ):
                continue

            terms = []
            for p_partner in COLORS:
                for q_partner in COLORS:
                    if p_partner == q_partner:
                        continue
                    for residual_color in COLORS:
                        word, remaining = word_for(
                            sigma,
                            tau,
                            p_partner,
                            q_partner,
                            residual_color,
                        )
                        terms.append(
                            (
                                word,
                                p_partner,
                                q_partner,
                                remaining,
                                residual_color,
                            )
                        )

            for color in COLORS:
                i = sigma_inverse[color]
                j = tau_inverse[color]
                assert i != j
                k = ({0, 1, 2} - {i, j}).pop()

                pure_sources = [
                    term for term in terms if term[0] == (color,) * 3
                ]
                assert pure_sources == [((color,) * 3, i, j, k, color)]

                reverse_word, reverse_remaining = word_for(
                    sigma, tau, j, i, color
                )
                assert reverse_remaining == k
                assert len(set(reverse_word)) > 1
                reverse_sources = [
                    term for term in terms if term[0] == reverse_word
                ]
                assert reverse_sources == [
                    (reverse_word, j, i, k, color)
                ]

            admissible.append((sigma, tau))

    # Six choices of sigma and the two derangements relative to it.
    assert len(admissible) == 12
    print(
        "verified the reversed-star contradiction for",
        len(admissible),
        "admissible permutation pairs",
    )


if __name__ == "__main__":
    main()
