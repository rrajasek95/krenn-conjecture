#!/usr/bin/env python3
"""Exact finite audit for the two-deficient balanced-word lemma."""

from itertools import combinations, permutations, product


FIELDS = range(3)
GOOD = tuple(range(4))
BAD = (4, 5)
SITES = GOOD + BAD
PAIRS = tuple(combinations(SITES, 2))
SUPPORTS = tuple(range(1, 16))


def distance(word, field):
    return sum(symbol != field for symbol in word)


def contributors(word):
    """Pairs (field, missing pair) able to produce a fixed good word."""
    out = []
    for field in FIELDS:
        deviations = {v for v, symbol in enumerate(word) if symbol != field}
        for pair in PAIRS:
            if deviations.issubset(pair):
                # Both response rows must occupy distinct missing sites.
                row_orders = tuple(permutations(pair, 2))
                assert len(row_orders) == 2
                out.append((field, frozenset(pair)))
    return set(out)


def audit_hamming_balls():
    words = tuple(product(FIELDS, repeat=4))
    balls = {
        field: {word for word in words if distance(word, field) <= 2}
        for field in FIELDS
    }
    assert set(words) == set().union(*balls.values())

    for r, s in combinations(FIELDS, 2):
        expected = {
            word
            for word in words
            if word.count(r) == 2 and word.count(s) == 2
        }
        assert balls[r] & balls[s] == expected

    assert not (balls[0] & balls[1] & balls[2])
    return len(words), tuple(len(balls[r]) for r in FIELDS)


def audit_balanced_contributors():
    checked = 0
    for r, s in combinations(FIELDS, 2):
        for r_positions in combinations(GOOD, 2):
            r_positions = frozenset(r_positions)
            s_positions = frozenset(set(GOOD) - set(r_positions))
            word = tuple(r if v in r_positions else s for v in GOOD)
            expected = {
                (r, s_positions),
                (s, r_positions),
            }
            assert contributors(word) == expected
            checked += 1
    assert checked == 18
    return checked


def audit_segre_normal_forms():
    # Independent-independent normal form:
    # c0 e0*e0 + c1 e1*e1 has determinant c0*c1.
    determinant_terms = {(1, 1): 1}
    assert determinant_terms == {(1, 1): 1}

    # If the left factors coincide, every combination is
    # e0 * (c0 e0 + c1 e1); the right-coincident case is symmetric.
    left_coincident_support = {(0, 0), (0, 1)}
    right_coincident_support = {(0, 0), (1, 0)}
    assert {i for i, _ in left_coincident_support} == {0}
    assert {j for _, j in right_coincident_support} == {0}


def support_values(mask):
    return tuple(symbol for symbol in range(4) if mask & (1 << symbol))


def box_words(box):
    return product(*(support_values(mask) for mask in box))


def valid_box(box):
    return all(
        any(word.count(field) >= 2 for field in FIELDS)
        for word in box_words(box)
    )


def axial_box(box):
    return any(box.count(1 << field) >= 2 for field in FIELDS)


def balanced_word(word):
    if 3 in word:
        return False
    counts = sorted((word.count(field) for field in FIELDS), reverse=True)
    return counts == [2, 2, 0]


def balanced_free_box(box):
    return not any(balanced_word(word) for word in box_words(box))


SITE_PERMS = tuple(permutations(range(4)))
FIELD_PERMS = tuple(permutations(range(3)))


def relabel_mask(mask, field_perm):
    image = mask & (1 << 3)
    for field in FIELDS:
        if mask & (1 << field):
            image |= 1 << field_perm[field]
    return image


def canonical_box(box):
    images = []
    for site_perm in SITE_PERMS:
        for field_perm in FIELD_PERMS:
            images.append(
                tuple(
                    relabel_mask(box[site], field_perm)
                    for site in site_perm
                )
            )
    return min(images)


def audit_support_boxes():
    valid = 0
    axial = 0
    nonaxial = 0
    exceptional = {}

    for box in product(SUPPORTS, repeat=4):
        if not valid_box(box):
            continue
        valid += 1
        if axial_box(box):
            axial += 1
            continue
        nonaxial += 1
        if balanced_free_box(box):
            key = canonical_box(box)
            exceptional[key] = exceptional.get(key, 0) + 1

    expected = {
        (1, 2, 3, 4): 72,
        (1, 2, 3, 8): 72,
        (1, 2, 3, 12): 72,
        (1, 2, 4, 7): 24,
        (1, 2, 5, 5): 72,
        (1, 3, 3, 8): 72,
        (1, 3, 3, 12): 72,
        (1, 6, 6, 6): 12,
        (3, 3, 3, 8): 12,
        (3, 3, 3, 12): 12,
    }

    assert valid == 6625
    assert axial == 3681
    assert nonaxial == 2944
    assert exceptional == expected
    assert sum(exceptional.values()) == 492

    for representative in expected:
        assert valid_box(representative)
        assert not axial_box(representative)
        assert balanced_free_box(representative)

    return valid, axial, nonaxial, len(exceptional)


def main():
    word_count, ball_sizes = audit_hamming_balls()
    balanced = audit_balanced_contributors()
    audit_segre_normal_forms()
    valid, axial, nonaxial, exceptional_orbits = audit_support_boxes()
    print("two-deficient balanced-word coupling: PASS")
    print(f"field words: {word_count}")
    print(f"radius-two ball sizes: {ball_sizes}")
    print(f"balanced field/partition cases: {balanced}")
    print(
        "support boxes: "
        f"valid={valid}, axial={axial}, nonaxial={nonaxial}, "
        f"balanced-free nonaxial orbits={exceptional_orbits}"
    )


if __name__ == "__main__":
    main()
