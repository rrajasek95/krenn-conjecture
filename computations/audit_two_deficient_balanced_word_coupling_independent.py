#!/usr/bin/env python3
"""Clean-room audit of the two-deficient balanced-word coupling.

This implementation does not import the primary checker. It represents
formal response-row contributors explicitly, absorbs site permutations by
sorting support multisets, and applies only the six field permutations when
canonicalizing the exceptional boxes.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations, permutations, product

import sympy as sp


FIELDS = (0, 1, 2)
GOOD = (0, 1, 2, 3)
O, T = 4, 5
ALL_SITES = GOOD + (O, T)
TRANSVERSE = 3


def balanced_words():
    """Yield (r,s,R,S,word) with the field pair and partition explicit."""
    for r, s in combinations(FIELDS, 2):
        for r_sites_tuple in combinations(GOOD, 2):
            r_sites = frozenset(r_sites_tuple)
            s_sites = frozenset(set(GOOD) - set(r_sites))
            word = tuple(r if v in r_sites else s for v in GOOD)
            yield r, s, r_sites, s_sites, word


def ordered_formal_contributors(word):
    """All lift/ordered-row terms that can have the selected good word."""
    terms = []
    for h in FIELDS:
        for missing_tuple in combinations(ALL_SITES, 2):
            missing = frozenset(missing_tuple)
            if any(v not in missing and word[v] != h for v in GOOD):
                continue
            x, y = missing_tuple
            for p_site, s_site in ((x, y), (y, x)):
                bad_factors = []
                for bad in (O, T):
                    if bad not in missing:
                        bad_factors.append((bad, f"a{h}"))
                    elif bad == p_site:
                        bad_factors.append((bad, "p"))
                    else:
                        bad_factors.append((bad, "s"))
                terms.append(
                    {
                        "field": h,
                        "missing": missing,
                        "p_site": p_site,
                        "s_site": s_site,
                        "bad_factors": tuple(bad_factors),
                    }
                )
    return terms


def formal_group_coefficient(field, missing):
    """The exact two-endpoint-order coefficient for one forced lift."""
    x, y = sorted(missing)
    lam = sp.Symbol(f"L{field}_{x}{y}")
    p_x = sp.Symbol(f"p{x}")
    p_y = sp.Symbol(f"p{y}")
    s_x = sp.Symbol(f"s{x}")
    s_y = sp.Symbol(f"s{y}")
    return sp.expand(lam * (p_x * s_y + p_y * s_x))


def audit_balanced_extraction():
    cases = 0
    ordered_terms = 0
    for r, s, r_sites, s_sites, word in balanced_words():
        terms = ordered_formal_contributors(word)
        assert len(terms) == 4
        ordered_terms += len(terms)

        grouped = defaultdict(list)
        for term in terms:
            grouped[(term["field"], term["missing"])].append(term)

        assert set(grouped) == {(r, s_sites), (s, r_sites)}
        for (field, missing), pair_terms in grouped.items():
            assert len(pair_terms) == 2
            assert {term["p_site"] for term in pair_terms} == set(missing)
            assert {term["s_site"] for term in pair_terms} == set(missing)
            assert all(
                term["bad_factors"] == ((O, f"a{field}"), (T, f"a{field}"))
                for term in pair_terms
            )
            coefficient = formal_group_coefficient(field, missing)
            assert len(sp.Poly(coefficient).terms()) == 2

        alphas = [
            sp.Symbol(f"alpha_{v}_{word[v]}", nonzero=True) for v in GOOD
        ]
        assert sp.prod(alphas) != 0
        cases += 1

    assert cases == 18
    assert ordered_terms == 72
    return cases, ordered_terms


def audit_hamming_geometry():
    words = set(product(FIELDS, repeat=4))
    balls = {r: {w for w in words if w.count(r) >= 2} for r in FIELDS}
    assert set().union(*balls.values()) == words
    assert tuple(len(balls[r]) for r in FIELDS) == (33, 33, 33)
    for r, s in combinations(FIELDS, 2):
        overlap = balls[r] & balls[s]
        assert len(overlap) == 6
        assert all(w.count(r) == w.count(s) == 2 for w in overlap)
    assert not set.intersection(*balls.values())
    return len(words), tuple(len(balls[r]) for r in FIELDS)


def audit_segre_degeneracies():
    c0, c1 = sp.symbols("c0 c1")
    independent = sp.diag(c0, c1)
    assert sp.factor(independent.det()) == c0 * c1

    left_coincident = sp.Matrix([[c0, c1], [0, 0]])
    right_coincident = sp.Matrix([[c0, 0], [c1, 0]])
    assert left_coincident[1, :] == sp.zeros(1, 2)
    assert right_coincident[:, 1] == sp.zeros(2, 1)

    # If both endpoint pairs coincide, the two generators are proportional.
    generator0 = sp.Matrix([[1, 0], [0, 0]])
    generator1 = sp.Matrix([[2, 0], [0, 0]])
    assert generator1 == 2 * generator0


ALPHABET = frozenset((*FIELDS, TRANSVERSE))
SUPPORTS = tuple(
    frozenset(symbol for symbol in ALPHABET if mask & (1 << symbol))
    for mask in range(1, 16)
)
FIELD_PERMUTATIONS = tuple(permutations(FIELDS))
SITE_PERMUTATIONS = tuple(permutations(GOOD))


def box_words(box):
    return product(*box)


def is_valid(box):
    for word in box_words(box):
        if max(word.count(r) for r in FIELDS) < 2:
            return False
    return True


def is_axial(box):
    return any(
        sum(support == frozenset((r,)) for support in box) >= 2
        for r in FIELDS
    )


def contains_balanced_word(box):
    """Test placements directly, without the primary word-count predicate."""
    for r, s in combinations(FIELDS, 2):
        for r_sites_tuple in combinations(GOOD, 2):
            r_sites = frozenset(r_sites_tuple)
            if all(r in box[v] if v in r_sites else s in box[v] for v in GOOD):
                return True
            if all(s in box[v] if v in r_sites else r in box[v] for v in GOOD):
                return True
    return False


def rename_fields(support, field_permutation):
    renamed = {TRANSVERSE} if TRANSVERSE in support else set()
    renamed.update(field_permutation[r] for r in FIELDS if r in support)
    return frozenset(renamed)


def support_mask(support):
    return sum(1 << symbol for symbol in support)


def multiset_canonical(box):
    """Absorb S4 by sorting, then minimize over only the six field maps."""
    candidates = []
    for field_permutation in FIELD_PERMUTATIONS:
        masks = sorted(
            support_mask(rename_fields(support, field_permutation))
            for support in box
        )
        candidates.append(tuple(masks))
    return min(candidates)


def literal_orbit(box):
    images = set()
    for field_permutation in FIELD_PERMUTATIONS:
        renamed = tuple(rename_fields(support, field_permutation) for support in box)
        for site_permutation in SITE_PERMUTATIONS:
            images.add(tuple(renamed[v] for v in site_permutation))
    return images


def parse_support(label):
    return frozenset(
        TRANSVERSE if symbol == "T" else int(symbol) for symbol in label
    )


REPRESENTATIVES = (
    ("0", "1", "01", "2"),
    ("0", "1", "01", "T"),
    ("0", "1", "01", "2T"),
    ("0", "1", "2", "012"),
    ("0", "1", "02", "02"),
    ("0", "01", "01", "T"),
    ("0", "01", "01", "2T"),
    ("0", "12", "12", "12"),
    ("01", "01", "01", "T"),
    ("01", "01", "01", "2T"),
)
EXPECTED_ORBIT_SIZES = (72, 72, 72, 24, 72, 72, 72, 12, 12, 12)


def audit_boxes():
    counts = Counter()
    exceptional_boxes = set()
    canonical_buckets = Counter()

    labelled_checked = 0
    for box in product(SUPPORTS, repeat=4):
        labelled_checked += 1
        if not is_valid(box):
            continue
        counts["valid"] += 1
        if is_axial(box):
            counts["axial"] += 1
            continue
        counts["nonaxial"] += 1
        if not contains_balanced_word(box):
            counts["exceptional"] += 1
            exceptional_boxes.add(box)
            canonical_buckets[multiset_canonical(box)] += 1

    assert labelled_checked == 15**4 == 50_625
    assert counts == Counter(
        valid=6625, axial=3681, nonaxial=2944, exceptional=492
    )
    assert len(canonical_buckets) == 10

    parsed_representatives = tuple(
        tuple(parse_support(label) for label in representative)
        for representative in REPRESENTATIVES
    )
    expected_keys = {
        multiset_canonical(representative)
        for representative in parsed_representatives
    }
    assert set(canonical_buckets) == expected_keys

    union = set()
    orbit_sizes = []
    for representative, expected_size in zip(
        parsed_representatives, EXPECTED_ORBIT_SIZES, strict=True
    ):
        assert is_valid(representative)
        assert not is_axial(representative)
        assert not contains_balanced_word(representative)
        orbit = literal_orbit(representative)
        assert len(orbit) == expected_size
        assert orbit <= exceptional_boxes
        assert not (union & orbit)
        union |= orbit
        orbit_sizes.append(len(orbit))

    assert union == exceptional_boxes
    assert tuple(orbit_sizes) == EXPECTED_ORBIT_SIZES
    assert tuple(sorted(canonical_buckets.values())) == tuple(
        sorted(EXPECTED_ORBIT_SIZES)
    )
    return labelled_checked, counts, canonical_buckets, exceptional_boxes


EXPECTED_UNIQUE_CENTERS = (
    frozenset((0, 1)),
    frozenset((0, 1)),
    frozenset((0, 1)),
    frozenset((0, 1, 2)),
    frozenset((0, 2)),
    frozenset((0, 1)),
    frozenset((0, 1)),
    frozenset((1, 2)),
    frozenset((0, 1)),
    frozenset((0, 1)),
)


def unique_exact_centers(box):
    """Fields having an exact-distance-two word with no second center."""
    witnesses = defaultdict(list)
    for word in box_words(box):
        centers = tuple(r for r in FIELDS if word.count(r) >= 2)
        if len(centers) == 1 and word.count(centers[0]) == 2:
            witnesses[centers[0]].append(word)
    return witnesses


def audit_unique_center_strengthening(exceptional_boxes):
    """Verify the new one-field extraction on all exceptional boxes."""
    representative_center_sets = []
    representative_witnesses = 0
    for labels, expected in zip(
        REPRESENTATIVES, EXPECTED_UNIQUE_CENTERS, strict=True
    ):
        box = tuple(parse_support(label) for label in labels)
        witnesses = unique_exact_centers(box)
        assert frozenset(witnesses) == expected
        representative_center_sets.append(frozenset(witnesses))
        representative_witnesses += sum(len(words) for words in witnesses.values())

        for center, words in witnesses.items():
            for word in words:
                terms = ordered_formal_contributors(word)
                assert len(terms) == 2
                deviations = frozenset(v for v in GOOD if word[v] != center)
                assert len(deviations) == 2
                assert all(term["field"] == center for term in terms)
                assert all(term["missing"] == deviations for term in terms)
                assert all(
                    term["bad_factors"]
                    == ((O, f"a{center}"), (T, f"a{center}"))
                    for term in terms
                )

    assert representative_witnesses == 47

    # The property is checked directly on all 492 labelled boxes, not merely
    # inferred from invariance of the ten representatives.
    for box in exceptional_boxes:
        witnesses = unique_exact_centers(box)
        assert len(witnesses) >= 2
    return tuple(representative_center_sets), representative_witnesses


def main():
    word_count, ball_sizes = audit_hamming_geometry()
    balanced_cases, ordered_terms = audit_balanced_extraction()
    audit_segre_degeneracies()
    labelled_checked, counts, canonical_buckets, exceptional_boxes = audit_boxes()
    center_sets, center_witnesses = audit_unique_center_strengthening(
        exceptional_boxes
    )
    print("two-deficient balanced-word coupling independent audit: PASS")
    print("field words:", word_count, "ball sizes:", ball_sizes)
    print("balanced cases:", balanced_cases, "ordered formal terms:", ordered_terms)
    print("support boxes checked:", labelled_checked)
    print("box counts:", dict(counts))
    print(
        "exceptional orbit sizes:",
        tuple(sorted(canonical_buckets.values(), reverse=True)),
    )
    print("unique-center sets by representative:", center_sets)
    print("unique-center representative witnesses:", center_witnesses)


if __name__ == "__main__":
    main()
