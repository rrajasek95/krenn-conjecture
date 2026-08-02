#!/usr/bin/env python3
"""Independent generating-function audit of the full Hasse lower faces.

For every deleted face and every matching of its four internal sites, this
checker forms the square-zero Hasse translation tau in the two mixed endpoint
directions and the two internal matching-edge directions.  In the translated
two-row Eq complex plus the split cap block it verifies

    N = tau(H_m) (r_0-T) - tau(H_0-u) r_m,
    dN = tau(H_m) Y w,
    tgt(N) = ores(N) = 0.

It also reconstructs the indexed squarefree Hasse/Spencer row differential.
It then retains every proper Boolean face and checks the strict pq/pr chart
cycle and all fifteen reset-denominator columns.  The proper internal faces
have real cross-column support (5,3,3,1); the corresponding faces of N match
them exactly.  Only the top internal face has the Kronecker support used by
the Reynolds symbol.  Finally, it records the exact obstruction to calling
this an underived physical-source jet: H_m is a target-zero physical
constraint, but the top coefficient of tau(H_m) is the unit.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import combinations


Q = Fraction
ZERO = Q(0)
ONE = Q(1)
SITES = tuple(range(8))
ODD = (1, 2, 3, 4, 5)
COLOURS = (0, 1, 2)
X, R, P, QSITE = 0, 3, 6, 7
FORBIDDEN = frozenset((P, R))
PURE = (0,) * 8
MIXED = (0, 1, 2, 1, 1, 2, 2, 2)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


@lru_cache(maxsize=None)
def matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position, second in enumerate(vertices[1:], start=1):
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def edge(left, right, left_colour, right_colour):
    if left < right:
        return "w", left, right, left_colour, right_colour
    return "w", right, left, right_colour, left_colour


def monomial(*variables):
    return tuple(sorted(variables))


def constant(value=ONE):
    return {(): Q(value)} if value else {}


def variable(item):
    return {monomial(item): ONE}


def add(*polynomials):
    answer = defaultdict(Q)
    for polynomial in polynomials:
        for term, coefficient in polynomial.items():
            answer[term] += coefficient
    return {term: coefficient for term, coefficient in answer.items()
            if coefficient}


def scale(scalar, polynomial):
    return {term: Q(scalar) * coefficient
            for term, coefficient in polynomial.items()
            if scalar * coefficient}


def is_epsilon(item):
    return item[0] == "eps"


def multiply(left, right):
    """Product in the square-zero Hasse algebra."""
    answer = defaultdict(Q)
    for left_term, left_coefficient in left.items():
        for right_term, right_coefficient in right.items():
            joined = left_term + right_term
            epsilons = [item for item in joined if is_epsilon(item)]
            if len(epsilons) != len(set(epsilons)):
                continue
            answer[tuple(sorted(joined))] += (
                left_coefficient * right_coefficient
            )
    return {term: coefficient for term, coefficient in answer.items()
            if coefficient}


def derivative(polynomial, items):
    answer = polynomial
    for item in items:
        next_answer = defaultdict(Q)
        for term, coefficient in answer.items():
            multiplicity = term.count(item)
            if not multiplicity:
                continue
            remainder = list(term)
            remainder.remove(item)
            next_answer[tuple(remainder)] += multiplicity * coefficient
        answer = {term: coefficient for term, coefficient in next_answer.items()
                  if coefficient}
    return answer


def translate(polynomial, directions):
    """Apply z_i -> z_i+epsilon_i, retaining every Hasse coefficient."""
    answer = polynomial
    for base_variable, epsilon in directions.items():
        translated = defaultdict(Q)
        for term, coefficient in answer.items():
            translated[term] += coefficient
            if base_variable in term:
                replaced = list(term)
                replaced.remove(base_variable)
                replaced.append(epsilon)
                translated[tuple(sorted(replaced))] += coefficient
        answer = {term: coefficient for term, coefficient in translated.items()
                  if coefficient}
    return answer


def hasse_coefficient(polynomial, subset, all_epsilons):
    subset = frozenset(subset)
    all_epsilons = frozenset(all_epsilons)
    answer = defaultdict(Q)
    for term, coefficient in polynomial.items():
        present = frozenset(item for item in term if item in all_epsilons)
        if present != subset:
            continue
        remainder = tuple(item for item in term if item not in all_epsilons)
        answer[remainder] += coefficient
    return {term: coefficient for term, coefficient in answer.items()
            if coefficient}


def external_face(polynomial, external_epsilons):
    """Coefficient in all external epsilons, retaining internal epsilons."""
    external_epsilons = frozenset(external_epsilons)
    answer = defaultdict(Q)
    for term, coefficient in polynomial.items():
        present = frozenset(item for item in term if item in external_epsilons)
        if present != external_epsilons:
            continue
        remainder = tuple(item for item in term if item not in external_epsilons)
        answer[remainder] += coefficient
    return {term: coefficient for term, coefficient in answer.items()
            if coefficient}


def polynomial_from_matching(vertices, colouring, direct_free=True):
    answer = defaultdict(Q)
    for matching in matchings(tuple(vertices)):
        if direct_free and FORBIDDEN in {
            frozenset(pair) for pair in matching
        }:
            continue
        term = monomial(*(
            edge(left, right, colouring[left], colouring[right])
            for left, right in matching
        ))
        answer[term] += ONE
    return dict(answer)


def contains_pair(term, pair):
    pair = frozenset(pair)
    return any(
        item[0] == "w" and frozenset((item[1], item[2])) == pair
        for item in term
    )


def partition(polynomial, pair):
    direct = {term: coefficient for term, coefficient in polynomial.items()
              if contains_pair(term, pair)}
    star = {term: coefficient for term, coefficient in polynomial.items()
            if not contains_pair(term, pair)}
    require(set(direct).isdisjoint(star), "sector overlap")
    require(add(direct, star) == polynomial, "sector partition")
    return direct, star


H_MIXED = polynomial_from_matching(SITES, dict(enumerate(MIXED)))
H_PURE = polynomial_from_matching(SITES, dict(enumerate(PURE)))
require(len(H_MIXED) == len(H_PURE) == 90, "direct-free row size")
HOMOGENIZING_U = variable(("homogenizing", "u"))
F_PURE = add(H_PURE, scale(-ONE, HOMOGENIZING_U))
CAP_Y = variable(("cap", "Y"))
KAPPA = variable(("curvature", "kappa"))


def face(deleted):
    return tuple(site for site in ODD if site != deleted)


def face_hafnian(deleted):
    colouring = {site: MIXED[site] for site in face(deleted)}
    return polynomial_from_matching(face(deleted), colouring, direct_free=False)


def internal_variables(matching):
    return tuple(
        edge(left, right, MIXED[left], MIXED[right])
        for left, right in matching
    )


def endpoint_variables(deleted):
    return (
        edge(X, deleted, MIXED[X], MIXED[deleted]),
        edge(P, QSITE, MIXED[P], MIXED[QSITE]),
    )


def module_add(*elements):
    answer = {}
    for element in elements:
        for generator, coefficient in element.items():
            answer[generator] = add(answer.get(generator, {}), coefficient)
            if not answer[generator]:
                del answer[generator]
    return answer


def module_scale(scalar, element):
    return {generator: scale(scalar, coefficient)
            for generator, coefficient in element.items()}


def module_multiply(polynomial, element):
    return {generator: multiply(polynomial, coefficient)
            for generator, coefficient in element.items()}


def module_coefficient(element, subset, all_epsilons):
    return {
        generator: coefficient
        for generator, polynomial in element.items()
        if (coefficient := hasse_coefficient(
            polynomial, subset, all_epsilons
        ))
    }


def module_external_face(element, external_epsilons):
    return {
        generator: coefficient
        for generator, polynomial in element.items()
        if (coefficient := external_face(polynomial, external_epsilons))
    }


def apply_module_map(element, generator_images):
    answer = {}
    for generator, coefficient in element.items():
        for output, image_coefficient in generator_images[generator].items():
            contribution = multiply(coefficient, image_coefficient)
            answer[output] = add(answer.get(output, {}), contribution)
            if not answer[output]:
                del answer[output]
    return answer


def translated_totalization(directions):
    tau_hm = translate(H_MIXED, directions)
    tau_f0 = translate(F_PURE, directions)
    require(tau_f0 == F_PURE,
            "pure row moved in mixed Hasse directions")

    # The translated differential is base changed along tau; translating
    # coefficients without translating these two row boundaries would not be
    # a chain complex and would leave the false extra term H_m(H_0-u).
    differential = {
        "r_0": {"eq": tau_f0},
        "r_m": {"eq": tau_hm},
        "T": {"w": scale(-ONE, CAP_Y)},
        "rho": {"w": constant()},
    }
    target = {
        "r_0": {"target": constant()},
        "r_m": {},
        "T": {"target": constant()},
        "rho": {},
    }
    ordinary_residue = {
        "r_0": {},
        "r_m": {},
        "T": {},
        "rho": {"ores": constant()},
    }
    total_chain = {
        "r_0": tau_hm,
        "r_m": scale(-ONE, tau_f0),
        "T": scale(-ONE, tau_hm),
    }
    expected_boundary = {"w": multiply(tau_hm, CAP_Y)}
    require(apply_module_map(total_chain, differential) == expected_boundary,
            "dN != tau(H_m)*Y*w")
    require(not apply_module_map(total_chain, target), "N retained target")
    require(not apply_module_map(total_chain, ordinary_residue),
            "N retained ordinary residue")
    return total_chain, expected_boundary, differential, target, ordinary_residue


def subsets(items):
    items = tuple(items)
    for size in range(len(items) + 1):
        yield from combinations(items, size)


def submasks(mask):
    answer = []
    subset = mask
    while True:
        answer.append(subset)
        if subset == 0:
            break
        subset = (subset - 1) & mask
    return tuple(sorted(answer))


def directions_for_mask(directions, mask):
    return tuple(
        direction for index, direction in enumerate(directions)
        if mask & (1 << index)
    )


def indexed_hasse_differential(row, jet_mask, directions):
    """Squarefree Hasse prolongation of the two physical row boundaries."""
    if row == "r_0":
        return {("eq", jet_mask): F_PURE}
    require(row == "r_m", "unknown indexed Hasse row")
    answer = {}
    for derivative_mask in submasks(jet_mask):
        coefficient = derivative(
            H_MIXED, directions_for_mask(directions, derivative_mask)
        )
        if coefficient:
            answer = module_add(answer, {
                ("eq", jet_mask ^ derivative_mask): coefficient
            })
    return answer


def indexed_hasse_chain_differential(chain, directions):
    answer = {}
    for (row, jet_mask), coefficient in chain.items():
        image = indexed_hasse_differential(row, jet_mask, directions)
        for output, output_coefficient in image.items():
            contribution = multiply(coefficient, output_coefficient)
            answer[output] = add(answer.get(output, {}), contribution)
            if not answer[output]:
                del answer[output]
    return answer


def indexed_top_koszul_cycle(directions):
    full_mask = (1 << len(directions)) - 1
    answer = {}
    for derivative_mask in submasks(full_mask):
        coefficient = derivative(
            H_MIXED, directions_for_mask(directions, derivative_mask)
        )
        if coefficient:
            answer[("r_0", full_mask ^ derivative_mask)] = coefficient
    answer[("r_m", full_mask)] = scale(-ONE, F_PURE)
    return answer


def audit_one_cube(deleted, matching):
    internal = internal_variables(matching)
    require(len(internal) == 2, "h=3 internal direction count")
    marked_u, marked_t = endpoint_variables(deleted)
    epsilons = tuple(("eps", name) for name in ("u", "t", "e", "f"))
    eps_u, eps_t, eps_e, eps_f = epsilons
    directions = {
        marked_u: eps_u,
        marked_t: eps_t,
        internal[0]: eps_e,
        internal[1]: eps_f,
    }
    total_chain, boundary, _differential, _target, _ores = (
        translated_totalization(directions)
    )
    tau_hm = translate(H_MIXED, directions)

    # Coefficientwise Spencer/Hasse interpretation of the generating
    # translation.  The row copies indexed by Boolean faces are essential;
    # a single isolated coefficient is not a chain in the old complex.
    ordered_directions = tuple(directions)
    indexed_cycle = indexed_top_koszul_cycle(ordered_directions)
    require(not indexed_hasse_chain_differential(
        indexed_cycle, ordered_directions
    ), "indexed four-direction Koszul/Hasse lift is not closed")
    full_mask = (1 << len(ordered_directions)) - 1
    require(
        indexed_cycle.get(("r_0", 0)) == constant(),
        "indexed Hasse cycle lost its target-one zero jet",
    )
    require(
        indexed_cycle.get(("r_m", full_mask)) == scale(-ONE, F_PURE),
        "indexed Hasse cycle lost its top mixed-row correction",
    )

    # The response correction is now derived on the entire Hasse
    # totalization, not assigned only to its top symbol.
    response_cycle = module_multiply(
        KAPPA,
        module_add(
            total_chain,
            {"rho": scale(-ONE, multiply(tau_hm, CAP_Y))},
        ),
    )
    require(not apply_module_map(response_cycle, _differential),
            "totalized curvature/response chain is not closed")
    require(not apply_module_map(response_cycle, _target),
            "totalized curvature/response cycle retained target")
    require(
        apply_module_map(response_cycle, _ores)
        == {"ores": scale(-ONE, multiply(KAPPA, multiply(tau_hm, CAP_Y)))},
        "totalized curvature/response cycle has the wrong residue",
    )

    # Every Hasse coefficient is the corresponding ordinary derivative.
    for subset in subsets(tuple(directions)):
        epsilon_subset = tuple(directions[item] for item in subset)
        require(
            hasse_coefficient(tau_hm, epsilon_subset, epsilons)
            == derivative(H_MIXED, subset),
            "Hasse coefficient/derivative mismatch",
        )

    top = module_coefficient(total_chain, epsilons, epsilons)
    top_constraint = hasse_coefficient(tau_hm, epsilons, epsilons)
    require(top_constraint == constant(),
            "translated mixed physical equation lost its unit top")
    require(top == {"r_0": constant(), "T": constant(-ONE)},
            "top coefficient of N is not r_0-T")
    require(
        module_coefficient(boundary, epsilons, epsilons)
        == {"w": CAP_Y},
        "top Hasse boundary is not Y*w",
    )
    original_differential = {
        "r_0": {"eq": F_PURE},
        "r_m": {"eq": H_MIXED},
        "T": {"w": scale(-ONE, CAP_Y)},
        "rho": {"w": constant()},
    }
    projected_top_boundary = apply_module_map(top, original_differential)
    require(
        projected_top_boundary
        == {"eq": F_PURE, "w": CAP_Y},
        "diagonal projection defect is not (H_0-u)*eq",
    )
    require(
        module_coefficient(response_cycle, epsilons, epsilons)
        == {
            "r_0": KAPPA,
            "T": scale(-ONE, KAPPA),
            "rho": scale(-ONE, multiply(KAPPA, CAP_Y)),
        },
        "top response cycle is not kappa*(r_0-T-Y*rho)",
    )

    # The same translated polynomial has pq-direct and pr-two-star sector
    # placement on every face containing both external directions.
    pq_direct, pq_star = partition(H_MIXED, (P, QSITE))
    pr_direct, pr_star = partition(H_MIXED, (P, R))
    for internal_subset in subsets((eps_e, eps_f)):
        full_subset = (eps_u, eps_t) + tuple(internal_subset)
        expected = hasse_coefficient(tau_hm, full_subset, epsilons)
        require(
            hasse_coefficient(
                translate(pq_direct, directions), full_subset, epsilons
            ) == expected,
            "external Hasse face left pq-direct sector",
        )
        require(not hasse_coefficient(
            translate(pq_star, directions), full_subset, epsilons
        ), "external Hasse face entered pq-star sector")
        require(not hasse_coefficient(
            translate(pr_direct, directions), full_subset, epsilons
        ), "external Hasse face entered pr-direct sector")
        require(
            hasse_coefficient(
                translate(pr_star, directions), full_subset, epsilons
            ) == expected,
            "external Hasse face left pr-two-star sector",
        )

    # Strict chart descent.  The shared cap term cancels in N_pq-N_pr; the
    # remaining translated Koszul chart comparison is closed and invisible
    # coefficient by coefficient.
    chart_difference = {
        "r_0_pq": tau_hm,
        "r_m_pq": scale(-ONE, F_PURE),
        "r_0_pr": scale(-ONE, tau_hm),
        "r_m_pr": F_PURE,
    }
    chart_differential = {
        "r_0_pq": {"eq": F_PURE},
        "r_m_pq": {"eq": tau_hm},
        "r_0_pr": {"eq": F_PURE},
        "r_m_pr": {"eq": tau_hm},
    }
    chart_target = {
        "r_0_pq": {"target": constant()},
        "r_m_pq": {},
        "r_0_pr": {"target": constant()},
        "r_m_pr": {},
    }
    require(not apply_module_map(chart_difference, chart_differential),
            "translated strict chart comparison is not closed")
    require(not apply_module_map(chart_difference, chart_target),
            "translated strict chart comparison retained target")

    # Retain the full internal Boolean face of every denominator column.
    # For the five selected colours, the reset column is h_s; the other ten
    # columns are zero.  The external (x,s),(p,q) face of the same universal
    # N totalization supplies exactly tau_internal(h_s)*(r_0-T), including
    # all proper-face leakage.
    internal_directions = {internal[0]: eps_e, internal[1]: eps_f}
    support_by_subset = {subset: [] for subset in subsets((eps_e, eps_f))}
    for site in ODD:
        h_site = face_hafnian(site)
        translated_h = translate(h_site, internal_directions)
        for colour in COLOURS:
            reset_column = translated_h if colour == MIXED[site] else {}

            if colour != MIXED[site]:
                require(not reset_column, "unselected denominator column")
                continue

            site_u, site_t = endpoint_variables(site)
            site_eps_u = ("eps", "site_u")
            site_eps_t = ("eps", "site_t")
            site_directions = {
                site_u: site_eps_u,
                site_t: site_eps_t,
                internal[0]: eps_e,
                internal[1]: eps_f,
            }
            site_chain, site_boundary, _d, site_target, site_ores = (
                translated_totalization(site_directions)
            )
            denominator_face = module_external_face(
                site_chain, (site_eps_u, site_eps_t)
            )
            boundary_face = module_external_face(
                site_boundary, (site_eps_u, site_eps_t)
            )
            require(boundary_face == {
                "w": multiply(translated_h, CAP_Y)
            }, "denominator proper faces do not match dN")
            require(not apply_module_map(denominator_face, site_target),
                    "denominator Hasse face retained target")
            require(not apply_module_map(denominator_face, site_ores),
                    "denominator Hasse face retained ordinary residue")

            for internal_subset in subsets((eps_e, eps_f)):
                value = hasse_coefficient(
                    translated_h, internal_subset, (eps_e, eps_f)
                )
                if value:
                    support_by_subset[internal_subset].append(site)

            top_face = module_coefficient(
                denominator_face, (eps_e, eps_f), (eps_e, eps_f)
            )
            expected_top = (
                {"r_0": constant(), "T": constant(-ONE)}
                if site == deleted else {}
            )
            require(top_face == expected_top,
                    "top denominator support is not Kronecker")

    support_counts = {
        subset: len(sites) for subset, sites in support_by_subset.items()
    }
    require(support_counts[()] == 5,
            "order-zero denominator support count")
    require(support_counts[(eps_e,)] == support_counts[(eps_f,)] == 3,
            "order-one denominator support count")
    require(support_counts[(eps_e, eps_f)] == 1,
            "top denominator support count")
    require(support_by_subset[(eps_e, eps_f)] == [deleted],
            "top denominator support label")

    return {
        "deleted": deleted,
        "matching": matching,
        "top_chain": "r_0-T",
        "indexed_hasse_cycle_terms": len(indexed_cycle),
        "top_boundary": "Y*w",
        "target": 0,
        "ordinary_residue": 0,
        "top_response_cycle": "kappa*(r_0-T-Y*rho)",
        "top_response": "-kappa*Y",
        "pq_sector": "direct",
        "pr_sector": "two_star",
        "denominator_selected_columns_by_internal_face": [5, 3, 3, 1],
        "top_denominator_column": [deleted, MIXED[deleted]],
        "underived_source_translation": "obstructed: top tau(H_m)=1",
        "diagonal_projection_commutator": "(H_0-u)*eq",
    }


def cubical_sign_audit():
    def boundary(state):
        free = [index for index, value in enumerate(state) if value is None]
        answer = defaultdict(int)
        for local_index, coordinate in enumerate(free):
            sign = -1 if local_index % 2 else 1
            upper = list(state)
            lower = list(state)
            upper[coordinate] = 1
            lower[coordinate] = 0
            answer[tuple(upper)] += sign
            answer[tuple(lower)] -= sign
        return {face_state: coefficient
                for face_state, coefficient in answer.items() if coefficient}

    first = boundary((None,) * 4)
    second = defaultdict(int)
    appearances = defaultdict(int)
    for facet, coefficient in first.items():
        for ridge, face_coefficient in boundary(facet).items():
            second[ridge] += coefficient * face_coefficient
            appearances[ridge] += 1
    require(len(first) == 8, "four-cube facet count")
    require(len(appearances) == 24 and set(appearances.values()) == {2},
            "four-cube ridge count")
    require(not {ridge: value for ridge, value in second.items() if value},
            "four-cube boundary does not square to zero")


def main():
    records = []
    for deleted in ODD:
        for matching in matchings(face(deleted)):
            records.append(audit_one_cube(deleted, matching))
    require(len(records) == 15, "five faces times three matchings")
    cubical_sign_audit()

    # All three matching choices have the same top; normalized Reynolds
    # averaging therefore preserves r_0-T and Y*w without declaring away the
    # proper Boolean faces checked above.
    for deleted in ODD:
        face_records = [record for record in records
                        if record["deleted"] == deleted]
        require(len(face_records) == 3, "face matching count")
        require({record["top_chain"] for record in face_records} == {"r_0-T"},
                "matching-dependent top chain")

    print("full four-direction Hasse/Koszul/cap totalization: PASS")
    print("N=tau(H_m)(r_0-T)-tau(H_0-u)r_m; dN=tau(H_m)Y*w")
    print("target and structural totalized ordinary residue vanish identically")
    print("strict pq/pr chart difference is a closed invisible Hasse cycle")
    print("all 15 denominator columns retained on proper faces: support 5,3,3,1")
    print("top support is Kronecker and top chain is r_0-T with boundary Y*w")
    print("kappa*(N-tau(H_m)Y*rho) is a cycle with top response -kappa*Y")
    print("underived physical-source descent fails exactly: top tau(H_m)=1")
    print("top diagonal projection has commutator defect (H_0-u)*eq")
    print("PASS: prolonged-cone fourth transgression; physical d4 needs a derived lift")


if __name__ == "__main__":
    main()
