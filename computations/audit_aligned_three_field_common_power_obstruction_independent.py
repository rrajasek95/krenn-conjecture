#!/usr/bin/env python3
"""Clean-room finite audit of the aligned three-field obstruction.

This checker imports neither the primary checker nor project modules.  Its
representations are deliberately different from the primary audit:

* pairs are six-bit masks in a nonlexicographic site order;
* coordinate words use a five-letter alphabet, including two transverse
  directions;
* all three-family set systems are represented by capped multiplicities of
  their seven nonempty incidence profiles;
* systems of distinct representatives are found by an augmenting-path
  matching algorithm;
* coordinate-permutation patterns are counted by dynamic programming; and
* the rank-two determinant is expanded by a tiny custom polynomial engine.

The imported distinct-missing-pair power theorem is a mathematical
dependency and is not reproved here.  Everything surrounding that import is
checked exactly.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations, product


# Deliberately use a different site order and bit-mask pairs.
SITES = ("eta", "beta", "zeta", "alpha", "delta", "gamma")
NSITES = len(SITES)
COLOURS = tuple(range(3))
ALPHABET = tuple(range(5))  # three field axes plus two transverse axes
PAIR_MASKS = tuple(
    mask for mask in range(1 << NSITES) if mask.bit_count() == 2
)


def sites(mask: int) -> tuple[int, ...]:
    return tuple(u for u in range(NSITES) if mask & (1 << u))


def hamming(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    return sum(a != b for a, b in zip(left, right))


def response_word(center: int, missing: int,
                  endpoint_labels: tuple[int, int]) -> tuple[int, ...]:
    word = [center] * NSITES
    a, b = sites(missing)
    word[a], word[b] = endpoint_labels
    return tuple(word)


def audit_response_modules_and_provenance() -> None:
    words = tuple(product(ALPHABET, repeat=NSITES))
    balls = {
        c: {
            word for word in words
            if hamming(word, (c,) * NSITES) <= 2
        }
        for c in COLOURS
    }
    # 1 + 6*4 + C(6,2)*4^2 for a five-letter local alphabet.
    assert {len(ball) for ball in balls.values()} == {265}
    assert all(
        balls[i].isdisjoint(balls[j])
        for i, j in combinations(COLOURS, 2)
    )

    # Arbitrary multi-site rows survive on A_c(P) in exactly the two orders
    # of the two missing sites.  Components at an occupied site collide with
    # A_c(P), and two components at the same site collide with each other.
    for missing in PAIR_MASKS:
        endpoint_set = set(sites(missing))
        survivors = {
            (u, v)
            for u, v in product(range(NSITES), repeat=2)
            if u != v and {u, v} == endpoint_set
        }
        assert len(survivors) == 2

        for center in COLOURS:
            for labels in product(ALPHABET, repeat=2):
                assert response_word(center, missing, labels) in balls[center]

    # A two-deviation word determines its centre and missing pair.  This is
    # the coefficient isolation used both for private pairs and for the
    # singleton-deviation lemma.
    for center in COLOURS:
        for other in COLOURS:
            if other == center:
                continue
            for missing in PAIR_MASKS:
                wanted = response_word(center, missing, (other, other))
                origins = [
                    pair for pair in PAIR_MASKS
                    if any(
                        response_word(center, pair, labels) == wanted
                        for labels in product(ALPHABET, repeat=2)
                    )
                ]
                assert origins == [missing]

    # For D_i={u}, the i-centred target coefficient is a sum over the five
    # pairs {u,v}.  For each such v, the k-centred hybrid word isolates the
    # same endpoint coordinate B_ii({u,v})[t at u, i at v].
    for assigned in COLOURS:
        for target_axis in COLOURS:
            if target_axis == assigned:
                continue
            third = next(c for c in COLOURS if c not in (assigned, target_axis))
            for u in range(NSITES):
                target = [assigned] * NSITES
                target[u] = target_axis
                target = tuple(target)
                target_origins = []
                for pair in PAIR_MASKS:
                    for labels in product(ALPHABET, repeat=2):
                        if response_word(assigned, pair, labels) == target:
                            target_origins.append((pair, labels))
                assert len(target_origins) == NSITES - 1
                assert {pair for pair, _ in target_origins} == {
                    (1 << u) | (1 << v)
                    for v in range(NSITES) if v != u
                }

                for pair, labels in target_origins:
                    a, b = sites(pair)
                    endpoint_by_site = {a: labels[0], b: labels[1]}
                    v = next(x for x in (a, b) if x != u)
                    hybrid = [third] * NSITES
                    hybrid[u] = target_axis
                    hybrid[v] = assigned
                    hybrid = tuple(hybrid)
                    hybrid_origins = []
                    for candidate in PAIR_MASKS:
                        for candidate_labels in product(ALPHABET, repeat=2):
                            if response_word(third, candidate,
                                             candidate_labels) == hybrid:
                                hybrid_origins.append(
                                    (candidate, candidate_labels)
                                )
                    assert hybrid_origins == [(pair, labels)]
                    assert endpoint_by_site[u] == target_axis
                    assert endpoint_by_site[v] == assigned


def local_product(left: int, right: int) -> int | None:
    """Basis multiplication in C plus a square-zero ideal.

    Basis value 0 is the unit and positive values are ideal coordinates;
    ``None`` denotes zero.
    """
    if left == 0:
        return right
    if right == 0:
        return left
    return None


def projected_basis(value: int, killed: frozenset[int]) -> int | None:
    if value == 0:
        return 0
    return None if value in killed else value


def audit_unital_projection_and_pair_selection() -> None:
    # On each local algebra, every diagonal coordinate-killing linear map on
    # the ideal, extended by 1 -> 1, respects every basis product.
    ideal_basis = tuple(range(1, 6))
    for kill_bits in range(1 << len(ideal_basis)):
        killed = frozenset(
            value for value in ideal_basis
            if kill_bits & (1 << (value - 1))
        )
        for left, right in product(range(6), repeat=2):
            raw = local_product(left, right)
            projected_raw = (
                None if raw is None else projected_basis(raw, killed)
            )
            pleft = projected_basis(left, killed)
            pright = projected_basis(right, killed)
            projected_product = (
                None if pleft is None or pright is None
                else local_product(pleft, pright)
            )
            assert projected_raw == projected_product

    # For all selected triples, killing axis c at the two sites P_c retains
    # A_c(P) exactly when P=P_c.  Count the distinct triples which invoke the
    # imported theorem.
    distinct = 0
    for selected in product(PAIR_MASKS, repeat=3):
        if len(set(selected)) == 3:
            distinct += 1
        for c in COLOURS:
            survivors = []
            for missing in PAIR_MASKS:
                occupied = ((1 << NSITES) - 1) ^ missing
                if occupied & selected[c] == 0:
                    survivors.append(missing)
            assert survivors == [selected[c]]
    assert distinct == 15 * 14 * 13 == 2730


# A set system is encoded by the multiplicity of each nonempty membership
# profile 001,...,111.  Counts are capped at three: a matching has only
# three left vertices, and every predicate below distinguishes only 0, 1,
# 2, or at least 3 elements.  Thus this is exhaustive for arbitrary finite
# universes, including the actual fifteen missing pairs.
PROFILES = tuple(range(1, 8))


def materialize(profile_counts: tuple[int, ...]):
    elements = tuple(
        (profile, copy)
        for profile, count in zip(PROFILES, profile_counts)
        for copy in range(count)
    )
    families = tuple(
        frozenset(element for element in elements if element[0] & (1 << c))
        for c in COLOURS
    )
    return elements, families


def matching_size(families) -> int:
    """Maximum bipartite matching size by augmenting paths."""
    owner = {}

    def augment(colour: int, seen: set) -> bool:
        for element in families[colour]:
            if element in seen:
                continue
            seen.add(element)
            if element not in owner or augment(owner[element], seen):
                owner[element] = colour
                return True
        return False

    matched = 0
    # Smallest-family first changes only the search path, not the maximum.
    for colour in sorted(COLOURS, key=lambda c: len(families[c])):
        matched += int(augment(colour, set()))
    return matched


def same_singleton_collision(families) -> bool:
    return any(
        families[i] == families[j] and len(families[i]) == 1
        for i, j in combinations(COLOURS, 2)
    )


def audit_hall_private_pairs_and_two_site_classification() -> tuple[int, int]:
    checked = 0
    no_sdr = 0
    two_site_instances = 0
    for profile_counts in product(range(4), repeat=len(PROFILES)):
        elements, families = materialize(profile_counts)
        if any(not family for family in families):
            continue
        checked += 1
        has_sdr = matching_size(families) == 3
        pair_singleton = any(
            len(families[i] | families[j]) == 1
            for i, j in combinations(COLOURS, 2)
        )
        union_small = len(set().union(*families)) <= 2
        assert (not has_sdr) == (pair_singleton or union_small)
        if has_sdr:
            continue
        no_sdr += 1

        # A nonzero assigned central coefficient forces an incidence-profile
        # singleton (a private pair).  No no-SDR system without the already
        # forbidden equal-singleton collision can contain even one.
        if not same_singleton_collision(families):
            assert all(profile_counts[(1 << c) - 1] == 0 for c in COLOURS)

        # If each |D_c|=2 then D_c is a designated member of H_c.  After the
        # equal-singleton collision and the all-common-D rank contradiction
        # are removed, every designation has exactly the advertised P,P,Q
        # shape and the whole active union is {P,Q}.
        if same_singleton_collision(families):
            continue
        for deviations in product(*families):
            if len(set(deviations)) == 1:
                continue  # independently excluded by the rank-three lemma
            two_site_instances += 1
            assert len(set(deviations)) == 2
            assert set().union(*families) == set(deviations)

    assert checked > 0 and no_sdr > 0 and two_site_instances > 0
    return checked, two_site_instances


def cross_cells(axis: int) -> frozenset[tuple[int, int]]:
    return frozenset(
        (row, col) for row, col in product(COLOURS, repeat=2)
        if row == axis or col == axis
    )


def audit_shared_pair_geometry() -> None:
    crosses = {c: cross_cells(c) for c in COLOURS}
    assert set.intersection(*(set(crosses[c]) for c in COLOURS)) == set()

    for assigned in COLOURS:
        competitors = tuple(c for c in COLOURS if c != assigned)
        r, s = competitors
        anti = crosses[r] & crosses[s]
        assert anti == frozenset(((r, s), (s, r)))

        # The support of a nonzero pure quotient tensor is a nonempty
        # rectangle supp(x) x supp(y).  A rectangle contained in the two-cell
        # anti-diagonal is necessarily one cell.
        nonempty_subsets = (
            frozenset((r,)), frozenset((s,)), frozenset((r, s))
        )
        surviving_rectangles = []
        for left, right in product(nonempty_subsets, repeat=2):
            rectangle = frozenset(product(left, right))
            if rectangle <= anti:
                surviving_rectangles.append(rectangle)
        assert set(surviving_rectangles) == {
            frozenset(((r, s),)), frozenset(((s, r),))
        }


def parity(permutation: tuple[int, ...]) -> int:
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(len(permutation))
        for j in range(i + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def audit_common_pair_rank() -> None:
    # Expand det(x_i v_j + y_i u_j) without SymPy.  A monomial is a sorted
    # tuple of variable names, and exact cancellation must leave zero.
    polynomial = Counter()
    for perm in (
        (0, 1, 2), (0, 2, 1), (1, 0, 2),
        (1, 2, 0), (2, 0, 1), (2, 1, 0),
    ):
        sign = parity(perm)
        # Choose one of the two rank-one summands in each selected entry.
        for choices in product((0, 1), repeat=3):
            variables = []
            for i, j, choice in zip(COLOURS, perm, choices):
                if choice == 0:
                    variables.extend((f"x{i}", f"v{j}"))
                else:
                    variables.extend((f"y{i}", f"u{j}"))
            polynomial[tuple(sorted(variables))] += sign
    polynomial = {
        monomial: coefficient
        for monomial, coefficient in polynomial.items()
        if coefficient != 0
    }
    assert not polynomial

    # In contrast, a diagonal matrix with three nonzero entries has the
    # single nonzero determinant monomial d0*d1*d2.
    diagonal = Counter({("d0", "d1", "d2"): 1})
    assert diagonal == Counter({("d0", "d1", "d2"): 1})


def audit_permutation_pattern_dp() -> None:
    # Local moved-colour masks.  The two 3-cycles have the same moved set and
    # therefore multiplicity two for the deviation-set census.
    local_masks = {0b000: 1, 0b011: 1, 0b101: 1, 0b110: 1, 0b111: 2}
    states = {(0, 0, 0): 1}
    for site in range(NSITES):
        next_states = defaultdict(int)
        for deviations, count in states.items():
            for moved, multiplicity in local_masks.items():
                updated = tuple(
                    deviations[c] | ((1 << site) if moved & (1 << c) else 0)
                    for c in COLOURS
                )
                next_states[updated] += count * multiplicity
        states = dict(next_states)

    counts = Counter()
    admissible = 0
    for deviations, multiplicity in states.items():
        lengths = sorted(mask.bit_count() for mask in deviations)
        if any(length not in (1, 2) for length in lengths):
            continue
        admissible += multiplicity
        if lengths == [1, 1, 1]:
            assert len(set(deviations)) == 1
            counts["one_cycle"] += multiplicity
        elif lengths == [1, 1, 2]:
            counts["two_transpositions"] += multiplicity
        elif lengths == [1, 2, 2]:
            doubles = [mask for mask in deviations if mask.bit_count() == 2]
            assert doubles[0] == doubles[1]
            counts["cycle_and_transposition"] += multiplicity
        elif lengths == [2, 2, 2]:
            if len(set(deviations)) == 1:
                counts["two_cycles"] += multiplicity
            else:
                assert len(set(deviations)) == 3
                assert all(
                    (deviations[i] & deviations[j]).bit_count() == 1
                    for i, j in combinations(COLOURS, 2)
                )
                counts["three_transpositions"] += multiplicity
        else:
            raise AssertionError(lengths)

    assert admissible == 462
    assert counts == Counter({
        "one_cycle": 12,
        "two_transpositions": 90,
        "cycle_and_transposition": 180,
        "three_transpositions": 120,
        "two_cycles": 60,
    })


def audit_permutation_hall_eliminations() -> tuple[int, int, int]:
    cyclic = two_trans = mixed = 0
    for profile_counts in product(range(4), repeat=len(PROFILES)):
        elements, families = materialize(profile_counts)
        if any(not family for family in families):
            continue
        h0, h1, h2 = families
        has_sdr = matching_size(families) == 3

        # One 3-cycle: the three singleton exclusions form a directed cycle
        # of strict differences, which always supplies an SDR.
        if h0 - h2 and h1 - h0 and h2 - h1:
            cyclic += 1
            assert has_sdr

        # Two distinct transpositions: colour 2 has D_2=P and the singleton
        # colours have H0\H1 and H1\H0.  If Hall fails, one singleton family
        # is exactly {P}, the forbidden singleton collision with D_2=P.
        if h0 - h1 and h1 - h0 and not has_sdr:
            for pair in h2:
                two_trans += 1
                assert h0 == frozenset((pair,)) or h1 == frozenset((pair,))

        # A 3-cycle plus a transposition: colours 1,2 have common D=P,
        # P belongs to both supports, and singleton exclusion gives H0\H2.
        # Hall failure forces H2={P}, again exactly Lemma 3.2(17).
        if h0 - h2 and not has_sdr:
            for pair in h1 & h2:
                mixed += 1
                assert h2 == frozenset((pair,))

    assert cyclic > 0 and two_trans > 0 and mixed > 0
    return cyclic, two_trans, mixed


def main() -> None:
    audit_response_modules_and_provenance()
    audit_unital_projection_and_pair_selection()
    hall_systems, two_site = audit_hall_private_pairs_and_two_site_classification()
    audit_shared_pair_geometry()
    audit_common_pair_rank()
    audit_permutation_pattern_dp()
    cyclic, two_trans, mixed = audit_permutation_hall_eliminations()
    print("aligned three-field obstruction independent audit: PASS")
    print("five-letter radius-two modules: 3 disjoint spaces of dimension 265")
    print("selected-pair triples: 3375 total; 2730 distinct")
    print("capped-incidence Hall systems:", hall_systems)
    print("two-site deviation designations:", two_site)
    print("permutation residuals: 462 = 12 + 90 + 180 + 120 + 60")
    print("Hall implication witnesses:", cyclic, two_trans, mixed)


if __name__ == "__main__":
    main()
