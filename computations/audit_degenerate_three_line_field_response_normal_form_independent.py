#!/usr/bin/env python3
"""Clean-room finite audit of the degenerate three-line-field normal form.

This checker imports no project code.  It uses an ordered-box enumeration,
literal word witnesses, symbolic (rather than sampled) rank contraction,
an explicit selector simulation, and an exhaustive two-layer Hall model.
The arbitrary-vector quotient and response-tensor cancellation steps remain
mathematical arguments and are stated as such in the companion audit note.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from itertools import combinations, permutations, product

import sympy as sp


FIELDS = (2, 0, 1)  # deliberately nonstandard order
TRANSVERSE = 3
SYMBOLS = FIELDS + (TRANSVERSE,)
BIT = {symbol: 1 << symbol for symbol in SYMBOLS}
SUPPORT_MASKS = tuple(range(15, 0, -1))
GOOD_SITES = (4, 2, 0, 3, 1)
GOOD_PAIRS = tuple(combinations(GOOD_SITES, 2))
ALL_SIX_PAIRS = tuple(combinations(range(6), 2))


def supported_symbols(mask):
    return tuple(symbol for symbol in SYMBOLS if mask & BIT[symbol])


@lru_cache(maxsize=None)
def literal_bad_word(sorted_box):
    """Return whether a word outside all three radius-two balls exists."""
    choices = tuple(supported_symbols(mask) for mask in sorted_box)
    return any(
        all(word.count(field) <= 2 for field in FIELDS)
        for word in product(*choices)
    )


def predicted_box_type(box):
    axial = tuple(
        field for field in FIELDS
        if sum(mask == BIT[field] for mask in box) >= 3
    )
    bridges = []
    for r, s in combinations(FIELDS, 2):
        allowed = BIT[r] | BIT[s]
        if all(mask & ~allowed == 0 for mask in box):
            if (sum(mask == BIT[r] for mask in box) <= 2
                    and sum(mask == BIT[s] for mask in box) <= 2):
                bridges.append(frozenset((r, s)))
    return axial, tuple(bridges)


def audit_ordered_boxes():
    counts = Counter()
    valid_multisets = set()
    for box in product(SUPPORT_MASKS, repeat=5):
        key = tuple(sorted(box, reverse=True))
        valid = not literal_bad_word(key)
        axial, bridges = predicted_box_type(box)
        assert valid == bool(axial or bridges), (box, valid, axial, bridges)
        if valid:
            assert len(axial) + len(bridges) == 1
            valid_multisets.add(key)
            counts["valid"] += 1
            counts["axial" if axial else "bridge"] += 1
    assert counts == Counter(valid=6516, axial=6093, bridge=423)
    # All C(15+5-1,5) multisets were encountered through the ordered stream.
    assert literal_bad_word.cache_info().currsize == 11628
    return counts, len(valid_multisets), literal_bad_word.cache_info().currsize


def family_has_sdr(families):
    if any(not family for family in families):
        return False
    return any(len(set(representatives)) == len(families)
               for representatives in product(*families))


def forced_bridge_families(box):
    # Symbols 2 and 0 play r and s.  The pair orientation is irrelevant.
    r, s = 2, 0
    r_sites = frozenset(site for site, mask in zip(GOOD_SITES, box)
                        if mask == BIT[r])
    s_sites = frozenset(site for site, mask in zip(GOOD_SITES, box)
                        if mask == BIT[s])
    mixed = frozenset(GOOD_SITES) - r_sites - s_sites
    r_family = frozenset(
        pair for pair in GOOD_PAIRS
        if s_sites <= frozenset(pair) <= s_sites | mixed
    )
    s_family = frozenset(
        pair for pair in GOOD_PAIRS
        if r_sites <= frozenset(pair) <= r_sites | mixed
    )
    return r_sites, s_sites, mixed, r_family, s_family


def audit_bridge_boundary_and_counts():
    r, s = 2, 0
    masks = (BIT[2], BIT[0], BIT[2] | BIT[0])
    profiles = Counter()
    compatible_profiles = Counter()
    checked = compatible = 0
    for box in product(masks, repeat=5):
        r_sites, s_sites, mixed, r_family, s_family = forced_bridge_families(box)
        if len(r_sites) > 2 or len(s_sites) > 2:
            continue
        checked += 1
        profile = (len(r_sites), len(s_sites), len(mixed))
        profiles[profile] += 1
        assert r_family and s_family
        assert family_has_sdr((r_family, s_family))

        # Independently inspect all ten boundary words rather than trusting
        # the displayed set formula.
        for pair in GOOD_PAIRS:
            r_word_supported = all(
                box[GOOD_SITES.index(site)]
                & BIT[s if site in pair else r]
                for site in GOOD_SITES
            )
            s_word_supported = all(
                box[GOOD_SITES.index(site)]
                & BIT[r if site in pair else s]
                for site in GOOD_SITES
            )
            assert r_word_supported == (pair in r_family)
            assert s_word_supported == (pair in s_family)

        hall_compatible = (
            len(r_family) == 1
            or len(s_family) == 1
            or len(r_family | s_family) <= 2
        )
        assert hall_compatible == (len(r_sites) == 2 or len(s_sites) == 2)
        if hall_compatible:
            compatible += 1
            compatible_profiles[profile] += 1

    assert checked == 141
    assert compatible == 110
    assert profiles == Counter({
        (0, 0, 5): 1, (0, 1, 4): 5, (0, 2, 3): 10,
        (1, 0, 4): 5, (1, 1, 3): 20, (1, 2, 2): 30,
        (2, 0, 3): 10, (2, 1, 2): 30, (2, 2, 1): 30,
    })
    assert compatible_profiles == Counter({
        (0, 2, 3): 10, (1, 2, 2): 30,
        (2, 0, 3): 10, (2, 1, 2): 30, (2, 2, 1): 30,
    })
    return checked, compatible, profiles, compatible_profiles


def matrix_rank(vectors):
    if not vectors:
        return 0
    return sp.Matrix(vectors).rank()


def separable(vectors, killed):
    killed = frozenset(killed)
    base = [vectors[field] for field in killed]
    rank = matrix_rank(base)
    return all(matrix_rank(base + [vectors[field]]) > rank
               for field in range(3) if field not in killed)


def audit_local_matroids():
    models = {
        "circuit": ((1, 2), (2, -1), (3, 1)),
        "coincident": ((1, 2), (2, -1), (-3, -6)),
        "rank1": ((2,), (-3,), (5,)),
    }
    expected = {
        "circuit": {frozenset(k) for k in combinations(range(3), 2)},
        "coincident": {
            frozenset((0,)), frozenset((2,)),
            frozenset((0, 1)), frozenset((1, 2)),
        },
        "rank1": {
            frozenset(k) for size in (1, 2)
            for k in combinations(range(3), size)
        },
    }
    observed = {}
    for name, vectors in models.items():
        nonseparable = set()
        for mask in range(8):
            killed = frozenset(field for field in range(3)
                               if mask & (1 << field))
            if not separable(vectors, killed):
                nonseparable.add(killed)
        assert nonseparable == expected[name]
        observed[name] = nonseparable
    return models, observed


def audit_selector_and_dummy(models):
    checked = Counter()
    for name, vectors in models.items():
        for selected in permutations(ALL_SIX_PAIRS, 3):
            if len(set(selected)) != 3:
                continue
            killed = frozenset(field for field, pair in enumerate(selected)
                               if 0 in pair)
            if not separable(vectors, killed):
                continue
            checked[name] += 1
            for field, chosen in enumerate(selected):
                chosen_good = frozenset(chosen) - {0}
                survivors = []
                for candidate in ALL_SIX_PAIRS:
                    good_filter = chosen_good <= frozenset(candidate)
                    bad_filter = (0 in candidate) or (field not in killed)
                    if good_filter and bad_filter:
                        survivors.append(candidate)
                assert survivors == [chosen]

                # If the bad map kills this field, its selected lift omits
                # site zero.  A nonzero dummy can therefore replace the zero
                # image without altering that lift.
                if field in killed:
                    assert 0 in chosen
    return checked


def audit_incidence_boundary():
    local_masks = tuple(mask for mask in range(7, 0, -1)
                        if mask.bit_count() <= 2)
    survivors = 0
    for assignment in product(local_masks, repeat=6):
        colour_counts = tuple(
            sum(bool(mask & (1 << colour)) for mask in assignment)
            for colour in range(3)
        )
        if min(colour_counts) < 4:
            continue
        survivors += 1
        assert colour_counts == (4, 4, 4)
        assert all(mask.bit_count() == 2 for mask in assignment)
        omitted = tuple(3 - mask.bit_count() for mask in assignment)
        assert omitted == (1,) * 6
    assert survivors == 90
    return survivors


def audit_symbolic_contraction():
    x = sp.symbols("x0:3")
    r = sp.symbols("r0:3")
    c = sp.symbols("c0:3")
    y = sp.symbols("y0:3")
    matrix = sp.Matrix(3, 3, lambda i, j: x[i] * r[j] + c[i] * y[j])
    assert sp.expand(matrix.det()) == 0
    return len(tuple(matrix))


def sdr_k_sets(families, star_elements):
    output = set()
    if any(not family for family in families):
        return output
    for representatives in product(*families):
        if len(set(representatives)) != 3:
            continue
        output.add(frozenset(
            field for field, representative in enumerate(representatives)
            if representative in star_elements
        ))
    return output


def no_sdr(families):
    return not family_has_sdr(families)


def hall_alternatives(families):
    return (
        any(families[r] == families[s] and len(families[r]) == 1
            for r, s in combinations(range(3), 2))
        or len(frozenset().union(*families)) <= 2
    )


def audit_layer_hall(observed_nonseparable):
    good = frozenset(("g0", "g1", "g2"))
    star = frozenset(("i0", "i1", "i2"))
    universe = tuple(sorted(good | star))
    nonempty = tuple(
        frozenset(element for bit, element in enumerate(universe)
                  if mask & (1 << bit))
        for mask in range(1, 1 << len(universe))
    )
    audited = survivors = 0
    bridge_rank2 = bridge_rank1 = 0
    for families in product(nonempty, repeat=3):
        audited += 1
        assert no_sdr(families) == hall_alternatives(families)
        k_sets = sdr_k_sets(families, star)
        equal_singleton = any(
            families[r] == families[s] and len(families[r]) == 1
            for r, s in combinations(range(3), 2)
        )
        if not k_sets and not equal_singleton:
            assert len(frozenset().union(*families)) <= 2

        j = tuple(family & good for family in families)
        i = tuple(family & star for family in families)
        for name, nonseparable in observed_nonseparable.items():
            no_local_selector = all(k in nonseparable for k in k_sets)
            if not no_local_selector:
                continue
            survivors += 1
            if name == "circuit":
                displayed_no_sdr = (
                    no_sdr(j) and no_sdr(i)
                    and all(no_sdr((i[r], j[s], j[t]))
                            for r, s, t in permutations(range(3))
                            if s < t)
                )
                assert displayed_no_sdr
                if k_sets:
                    assert all(len(k) == 2 for k in k_sets)
            elif name == "coincident":
                assert no_sdr((j[0], families[1], j[2]))
                assert no_sdr((i[0], families[1], i[2]))
                if k_sets:
                    assert all((0 in k) != (2 in k) for k in k_sets)
            else:
                assert no_sdr(j) and no_sdr(i)
                if k_sets:
                    assert all(0 < len(k) < 3 for k in k_sets)

        # Corollary 5.2 needs only the abstract facts that J0,J2 have
        # distinct representatives and no locally separable SDR exists.
        if family_has_sdr((j[0], j[2])):
            coincident_forbidden = observed_nonseparable["coincident"]
            if all(k in coincident_forbidden for k in k_sets):
                bridge_rank2 += 1
                assert not i[1]
                assert no_sdr((j[0], families[1], j[2]))
                assert no_sdr((i[0], families[1], i[2]))
                assert (
                    not i[0] or not i[2]
                    or (i[0] == i[2] and len(i[0]) == 1)
                )
                assert hall_alternatives((j[0], families[1], j[2]))

            rank1_forbidden = observed_nonseparable["rank1"]
            if all(k in rank1_forbidden for k in k_sets):
                bridge_rank1 += 1
                assert no_sdr(j) and no_sdr(i)
                if j[1]:
                    assert hall_alternatives(j)

    assert audited == 63 ** 3
    return audited, survivors, bridge_rank2, bridge_rank1


def audit_target_module_separation():
    # Columns are field modules; rows are target tensors.  All-axial is the
    # identity.  In the bridge normal form targets 0,1 are axial on fields
    # 0,1 and target 2 has nonzero boundary components in fields 0,2.
    all_axial = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    bridge = ((1, 0, 0), (0, 1, 0), (1, 0, 1))
    for incidence in (all_axial, bridge):
        columns = tuple(tuple(row[field] for row in incidence)
                        for field in range(3))
        assert len(set(columns)) == 3
        for r, s in combinations(range(3), 2):
            assert any(row[r] != row[s] for row in incidence)
    return all_axial, bridge


def main():
    incidence = audit_incidence_boundary()
    box_counts, valid_multisets, all_multisets = audit_ordered_boxes()
    bridge_count, compatible, profiles, compatible_profiles = (
        audit_bridge_boundary_and_counts()
    )
    models, nonseparable = audit_local_matroids()
    selectors = audit_selector_and_dummy(models)
    contraction_entries = audit_symbolic_contraction()
    hall_systems, hall_survivors, bridge_rank2, bridge_rank1 = (
        audit_layer_hall(nonseparable)
    )
    target_modules = audit_target_module_separation()

    print("independent degenerate three-line-field response audit: PASS")
    print("coordinate-plane incidence assignments", incidence)
    print("ordered support boxes", 15 ** 5, "valid", dict(box_counts),
          "valid multisets", valid_multisets, "all multisets", all_multisets)
    print("fixed-pair bridge boxes", bridge_count, "compatible", compatible)
    print("bridge profiles", dict(sorted(profiles.items())))
    print("compatible profiles", dict(sorted(compatible_profiles.items())))
    print("locally separable selector triples", dict(selectors))
    print("symbolic contraction entries", contraction_entries)
    print("two-layer Hall systems", hall_systems, "classified branches",
          hall_survivors, "bridge rank2", bridge_rank2, "bridge rank1", bridge_rank1)
    print("target-module incidence controls", target_modules)


if __name__ == "__main__":
    main()
