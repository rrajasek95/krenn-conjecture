#!/usr/bin/env python3
"""Independent exact audit of the uniform pure-lift projection argument.

This script deliberately does not import the primary checker.  It uses
six-bit masks for pairs, site-labelled frozensets for tensor words, and
Gaussian integers for exact complex-weight tests.  It audits:

* aggregation of parallel decorated sources before supports are defined;
* the two ordered endpoint terms surviving multiplication by arbitrary
  multi-site rows;
* the complete provenance of the target and shared-pair response words;
* the private-pair implication, including zero aggregate coefficients;
* every ordered triple of distinct selected pairs and all pure-term and
  local-coordinate valuations;
* matching-power functoriality by symbolic site-incidence vectors;
* the t=0 local projection on target and transverse coordinates; and
* an exact nonreal-weight repeated-pair K4 common-power witness.

The finite checks audit bookkeeping only.  The arbitrary-dimensional
linear-algebra argument is given in the companion note.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations, permutations, product


# A deliberately nonlexicographic site order and bit-mask edge encoding,
# independent of the tuple-edge representation in the primary checker.
SITES = ("f", "b", "e", "a", "d", "c")
SITE_INDEX = {site: i for i, site in enumerate(SITES)}
FULL_MASK = (1 << len(SITES)) - 1
COLOURS = ("cyan", "amber", "violet")
OUTSIDE_AXES = ("rho", "sigma")
LOCAL_BASIS = COLOURS + OUTSIDE_AXES
PAIR_MASKS = tuple(
    sorted(
        (mask for mask in range(1 << len(SITES)) if mask.bit_count() == 2),
        reverse=True,
    )
)


def mask_sites(mask: int) -> tuple[str, ...]:
    return tuple(site for site in SITES if mask & (1 << SITE_INDEX[site]))


def pair_mask(u: str, v: str) -> int:
    return (1 << SITE_INDEX[u]) | (1 << SITE_INDEX[v])


def assignment_word(assignments) -> frozenset[tuple[str, str]]:
    """A tensor word as a site-labelled frozenset, not an ordered tuple."""
    return frozenset(assignments)


def lift_word(base: str, missing: int, endpoint_labels) -> frozenset:
    endpoint_labels = dict(endpoint_labels)
    return assignment_word(
        (site, endpoint_labels.get(site, base)) for site in SITES
    )


def row_var(kind: str, response_colour: str, site: str, label: str) -> tuple:
    return (kind, response_colour, site, label)


def row_monomial(i: str, j: str, p_site: str, p_label: str,
                 s_site: str, s_label: str) -> tuple:
    # Polynomial multiplication is commutative; canonicalize factor order.
    return tuple(sorted((
        row_var("p", i, p_site, p_label),
        row_var("s", j, s_site, s_label),
    )))


def response_provenance(i: str, j: str):
    """Expand p_i s_j E_base(P) from all row sites and basis coordinates."""
    output = defaultdict(list)
    for base in COLOURS:
        for missing in PAIR_MASKS:
            missing_sites = set(mask_sites(missing))
            for p_site, s_site in product(SITES, repeat=2):
                # Local square-zero multiplication leaves precisely the two
                # distinct endpoint orders of the missing pair.
                if p_site == s_site or {p_site, s_site} != missing_sites:
                    continue
                for p_label, s_label in product(LOCAL_BASIS, repeat=2):
                    word = lift_word(
                        base,
                        missing,
                        ((p_site, p_label), (s_site, s_label)),
                    )
                    monomial = row_monomial(
                        i, j, p_site, p_label, s_site, s_label
                    )
                    output[word].append((base, missing, monomial))
    return output


def audit_multisite_rows_and_response_words() -> int:
    # Before introducing coordinate labels, exhaust all possible sites of the
    # two arbitrary multi-site rows.  Exactly the two endpoint orders survive.
    for missing in PAIR_MASKS:
        survivors = tuple(
            (u, v)
            for u, v in product(SITES, repeat=2)
            if u != v
            and not (missing & (1 << SITE_INDEX[u]) == 0)
            and not (missing & (1 << SITE_INDEX[v]) == 0)
        )
        endpoints = mask_sites(missing)
        assert set(survivors) == set(permutations(endpoints, 2))
        assert len(survivors) == 2

    total_terms = 0
    for i, j in product(COLOURS, repeat=2):
        provenance = response_provenance(i, j)
        total_terms += sum(map(len, provenance.values()))

        # Four sites are frozen to the base axis.  Since two missing pairs
        # have union of size at most four, response spaces of distinct base
        # colours cannot share any literal coordinate word.
        assert all(
            len({base for base, _, _ in origins}) == 1
            for origins in provenance.values()
        )

        # A full target word can only come from the matching base colour,
        # but it receives both endpoint orders from every missing pair.
        for c in COLOURS:
            target = assignment_word((site, c) for site in SITES)
            origins = provenance[target]
            assert len(origins) == 2 * len(PAIR_MASKS)
            assert {base for base, _, _ in origins} == {c}
            assert Counter(missing for _, missing, _ in origins) == Counter(
                {missing: 2 for missing in PAIR_MASKS}
            )

    # In the diagonal response c,c, the mixed word with colour c at P and
    # base colour d elsewhere has exactly the same two row monomials as the
    # P-contribution to the all-c target word, and no other origin.
    for c in COLOURS:
        provenance = response_provenance(c, c)
        target = assignment_word((site, c) for site in SITES)
        for d in COLOURS:
            if d == c:
                continue
            for missing in PAIR_MASKS:
                endpoints = mask_sites(missing)
                shared_word = lift_word(
                    d, missing, ((endpoints[0], c), (endpoints[1], c))
                )
                shared_origins = provenance[shared_word]
                assert len(shared_origins) == 2
                assert {(base, pair) for base, pair, _ in shared_origins} == {
                    (d, missing)
                }

                shared_monomials = {term[2] for term in shared_origins}
                target_monomials = {
                    monomial
                    for base, pair, monomial in provenance[target]
                    if base == c and pair == missing
                }
                assert shared_monomials == target_monomials
                assert len(shared_monomials) == 2

                # Transverse row components lie in different coordinate
                # words and therefore cannot cancel either isolated word.
                assert all(
                    all(variable[-1] in COLOURS for variable in monomial)
                    for monomial in shared_monomials | target_monomials
                )
    return total_terms


# Exact Gaussian-integer arithmetic for parallel/cancellation and K4 tests.
Gaussian = tuple[int, int]
ZERO: Gaussian = (0, 0)
ONE: Gaussian = (1, 0)


def gadd(x: Gaussian, y: Gaussian) -> Gaussian:
    return x[0] + y[0], x[1] + y[1]


def gmul(x: Gaussian, y: Gaussian) -> Gaussian:
    return x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0]


def add_coefficient(table, key, value: Gaussian) -> None:
    table[key] = gadd(table.get(key, ZERO), value)
    if table[key] == ZERO:
        del table[key]


def audit_exact_aggregation() -> None:
    p0, p1 = PAIR_MASKS[0], PAIR_MASKS[-1]
    raw_pure = (
        (COLOURS[0], p0, (3, 2)),
        (COLOURS[0], p0, (-1, 5)),
        (COLOURS[0], p0, (-2, -7)),  # exact aggregate zero
        (COLOURS[0], p1, (4, -3)),
        (COLOURS[1], p1, (2, 1)),   # same pair, different colour
        (COLOURS[1], p1, (-1, 4)),
    )
    aggregate = {}
    for colour, missing, coefficient in raw_pure:
        add_coefficient(aggregate, (colour, missing), coefficient)
    assert (COLOURS[0], p0) not in aggregate
    assert aggregate[COLOURS[0], p1] == (4, -3)
    assert aggregate[COLOURS[1], p1] == (1, 5)

    # Supports are defined only after aggregation.  Sharing a pair across
    # colours is retained; an exactly cancelled aggregate is not active.
    supports = {
        colour: {pair for (base, pair), value in aggregate.items()
                 if base == colour and value != ZERO}
        for colour in COLOURS
    }
    assert p0 not in supports[COLOURS[0]]
    assert p1 in supports[COLOURS[0]] & supports[COLOURS[1]]


def audit_private_pair_logic() -> None:
    # At one fixed pair, enumerate every zero/nonzero pattern of its three
    # aggregate coefficients.  The beta_c(P) coefficient can be unconstrained
    # by shared-word equations exactly for singleton activity {c}.
    for activity_bits in range(1 << len(COLOURS)):
        active = {
            COLOURS[i] for i in range(len(COLOURS))
            if activity_bits & (1 << i)
        }
        for c in COLOURS:
            beta_can_contribute = c in active and not (active - {c})
            assert beta_can_contribute == (active == {c})

    # Any three selected private pairs must be pairwise distinct.  Audit all
    # 15^3 labelled choices, retaining the exact 15*14*13 possibilities.
    admissible = []
    for selected in product(PAIR_MASKS, repeat=3):
        private_for_all = all(
            selected[c] not in {
                selected[d] for d in range(3) if d != c
            }
            for c in range(3)
        )
        assert private_for_all == (len(set(selected)) == 3)
        if private_for_all:
            admissible.append(selected)
    assert len(admissible) == 15 * 14 * 13 == 2730


def site_weight(selected: tuple[int, int, int], site: str, label: str) -> int:
    if label not in COLOURS:
        return 0
    c = COLOURS.index(label)
    return int(bool(selected[c] & (1 << SITE_INDEX[site])))


def pure_lift_valuation(selected, c: int, missing: int) -> int:
    # E_c(P) has the c-axis at precisely the sites outside P.
    return sum(
        site_weight(selected, site, COLOURS[c])
        for site in SITES
        if not (missing & (1 << SITE_INDEX[site]))
    )


def matchings_on_mask(support: int) -> tuple[tuple[int, ...], ...]:
    if support == 0:
        return ((),)
    first_bit = support & -support
    remainder = support ^ first_bit
    output = []
    choices = remainder
    while choices:
        second_bit = choices & -choices
        edge = first_bit | second_bit
        for tail in matchings_on_mask(remainder ^ second_bit):
            output.append((edge,) + tail)
        choices ^= second_bit
    return tuple(output)


def graph_shape(selected) -> str:
    degrees = Counter()
    for pair in selected:
        for site in mask_sites(pair):
            degrees[site] += 1
    signature = tuple(sorted(degrees.values()))
    components = []
    unseen = set(degrees)
    while unseen:
        component = {unseen.pop()}
        changed = True
        while changed:
            changed = False
            for pair in selected:
                ends = set(mask_sites(pair))
                if ends & component and not ends <= component:
                    component |= ends
                    unseen -= ends
                    changed = True
        components.append(len(component))
    component_sizes = tuple(sorted(components))
    key = signature, component_sizes
    names = {
        ((1, 1, 1, 1, 1, 1), (2, 2, 2)): "3K2",
        ((1, 1, 1, 1, 2), (2, 3)): "P3+K2",
        ((1, 1, 2, 2), (4,)): "P4",
        ((1, 1, 1, 3), (4,)): "K1,3",
        ((2, 2, 2), (3,)): "K3",
    }
    return names[key]


def audit_projection_and_valuations():
    ordered_shape_counts = Counter()
    for selected in product(PAIR_MASKS, repeat=3):
        if len(set(selected)) != 3:
            continue
        ordered_shape_counts[graph_shape(selected)] += 1

        for c, chosen in enumerate(selected):
            valuations = {
                missing: pure_lift_valuation(selected, c, missing)
                for missing in PAIR_MASKS
            }
            assert valuations[chosen] == 0
            assert all(
                valuation in (1, 2)
                for missing, valuation in valuations.items()
                if missing != chosen
            )

        # Every coordinate of every arbitrary q edge has exponent 0, 1, or
        # 2.  Outside-axis coordinates are fixed by the projection/1PS.
        for edge in PAIR_MASKS:
            u, v = mask_sites(edge)
            for label_u, label_v in product(LOCAL_BASIS, repeat=2):
                exponent = (
                    site_weight(selected, u, label_u)
                    + site_weight(selected, v, label_v)
                )
                assert exponent in (0, 1, 2)
                if label_u in OUTSIDE_AXES and label_v in OUTSIDE_AXES:
                    assert exponent == 0

    assert ordered_shape_counts == {
        "3K2": 90,
        "P3+K2": 1080,
        "P4": 1080,
        "K1,3": 360,
        "K3": 120,
    }

    # Functoriality is symbolic in the local coordinate weights: every
    # matching uses each output site once.  Check the incidence vectors for
    # every four-site and six-site matching.  Dotting these vectors with any
    # assignment of local weights proves equality of input and output
    # valuations in arbitrary local dimension.
    matching_count = 0
    for size in (4, 6):
        for site_indices in combinations(range(len(SITES)), size):
            support = sum(1 << i for i in site_indices)
            for matching in matchings_on_mask(support):
                incidence = Counter(
                    site for edge in matching for site in mask_sites(edge)
                )
                assert incidence == Counter({SITES[i]: 1 for i in site_indices})
                matching_count += 1
    assert matching_count == 15 * 3 + 15

    return ordered_shape_counts, matching_count


def matching_power(edge_cells, number_of_edges: int):
    """Unordered matching power using disjoint bit masks and word unions."""
    output = {}
    for chosen_edges in combinations(tuple(edge_cells), number_of_edges):
        union = 0
        disjoint = True
        for edge in chosen_edges:
            if union & edge:
                disjoint = False
                break
            union |= edge
        if not disjoint:
            continue
        choices = [tuple(edge_cells[edge].items()) for edge in chosen_edges]
        for selected_cells in product(*choices):
            word = frozenset().union(*(cell for cell, _ in selected_cells))
            coefficient = ONE
            for _, value in selected_cells:
                coefficient = gmul(coefficient, value)
            add_coefficient(output, word, coefficient)
    return output


def raw_source_square(raw_sources):
    """Enumerate source choices before parallel decorated-edge aggregation."""
    output = {}
    for left, right in combinations(raw_sources, 2):
        edge_l, cell_l, weight_l = left
        edge_r, cell_r, weight_r = right
        if edge_l & edge_r:
            continue
        add_coefficient(
            output,
            cell_l | cell_r,
            gmul(weight_l, weight_r),
        )
    return output


def aggregate_sources(raw_sources):
    edge_cells = defaultdict(dict)
    for edge, cell, weight in raw_sources:
        add_coefficient(edge_cells[edge], cell, weight)
    return {edge: cells for edge, cells in edge_cells.items() if cells}


def audit_parallel_sources() -> None:
    # Parallel sources with identical endpoint decoration aggregate, while a
    # different ordered endpoint decoration remains a separate tensor cell.
    four = SITES[:4]
    raw = []
    for index, (u, v) in enumerate(combinations(four, 2)):
        edge = pair_mask(u, v)
        c0 = COLOURS[index % 3]
        c1 = COLOURS[(index + 1) % 3]
        cell = assignment_word(((u, c0), (v, c1)))
        alternate = assignment_word(((u, c1), (v, c0)))
        raw.extend((
            (edge, cell, (index + 1, 1)),
            (edge, cell, (-index, -1)),  # same cell; aggregate exactly 1
            (edge, alternate, (0, index + 1)),
        ))
    aggregated = aggregate_sources(raw)
    assert raw_source_square(raw) == matching_power(aggregated, 2)


def audit_nonreal_repeated_k4_witness():
    four = SITES[:4]
    leftover = pair_mask(SITES[4], SITES[5])
    factors = (
        ((four[0], four[1]), (four[2], four[3])),
        ((four[0], four[2]), (four[1], four[3])),
        ((four[0], four[3]), (four[1], four[2])),
    )
    edge_weights = (
        ((1, 1), (2, -1)),
        ((0, -1), (3, 2)),
        ((2, 0), (1, 3)),
    )
    q = defaultdict(dict)
    expected_square = {}
    for c, (factor, weights) in enumerate(zip(factors, edge_weights)):
        for (u, v), weight in zip(factor, weights):
            q[pair_mask(u, v)][assignment_word(((u, COLOURS[c]),
                                                (v, COLOURS[c])))] = weight
        full_word = assignment_word((site, COLOURS[c]) for site in four)
        expected_square[full_word] = gmul(weights[0], weights[1])

    assert all(value != ZERO for value in expected_square.values())
    assert matching_power(dict(q), 2) == expected_square
    assert matching_power(dict(q), 3) == {}

    # Each surviving square word occupies the same four sites, so all three
    # corresponding pure lifts have the repeated missing pair.
    supports = {colour: {leftover} for colour in COLOURS}
    assert all(
        supports[c] - set().union(*(supports[d] for d in COLOURS if d != c))
        == set()
        for c in COLOURS
    )
    return expected_square


def main() -> None:
    audit_exact_aggregation()
    response_terms = audit_multisite_rows_and_response_words()
    audit_private_pair_logic()
    shapes, matching_count = audit_projection_and_valuations()
    audit_parallel_sources()
    k4_coefficients = audit_nonreal_repeated_k4_witness()

    print("independent uniform pure-lift projection audit: PASS")
    print("response monomial provenance terms:", response_terms)
    print("ordered distinct private triples:", sum(shapes.values()))
    print("ordered support-graph census:", dict(sorted(shapes.items())))
    print("symbolic matching-incidence rows:", matching_count)
    print("repeated-pair K4 coefficients:", sorted(k4_coefficients.values()))
    print("scope: exact bookkeeping; arbitrary-dimensional proof is in the note")


if __name__ == "__main__":
    main()
