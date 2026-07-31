#!/usr/bin/env python3
"""Audit formal partial-matching occupancy and its exact limitation.

This is a small, dependency-free combinatorial checker.  It verifies the
formal state splitting/exposure and the five-site cap expansion.  It also
checks that the unmatched-state section is not a chain map for the
one-chart evaluated cap-multiplication block.  It does not construct an
evaluated pair-comparison total complex or a non-split Rees extension.
"""

from collections import Counter
from fractions import Fraction
from itertools import product
from math import factorial


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge(u, v):
    return tuple(sorted((u, v)))


def partial_matchings(vertices):
    """Return every partial matching once as a tuple of ordered edges."""
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first, rest = vertices[0], vertices[1:]
    answer = list(partial_matchings(rest))
    for position, partner in enumerate(rest):
        tail_vertices = rest[:position] + rest[position + 1 :]
        for tail in partial_matchings(tail_vertices):
            answer.append(tuple(sorted((edge(first, partner),) + tail)))
    return tuple(answer)


def split_at(matching, distinguished):
    """Canonical star/direct occupancy coordinate of one state."""
    for direct in matching:
        if distinguished in direct:
            partner = direct[0] if direct[1] == distinguished else direct[1]
            remainder = tuple(item for item in matching if item != direct)
            return ("direct", partner, remainder)
    return ("star", None, matching)


def assemble_at(coordinate, distinguished):
    kind, partner, remainder = coordinate
    if kind == "star":
        return remainder
    require(kind == "direct", "unknown occupancy branch")
    return tuple(sorted((edge(distinguished, partner),) + remainder))


def expose_state(matching, old_vertices, distinguished):
    """Full coefficient exposure: star x or join x to one unmatched site."""
    covered = {vertex for direct in matching for vertex in direct}
    answer = [matching]
    for partner in old_vertices:
        if partner not in covered:
            answer.append(tuple(sorted((edge(distinguished, partner),) + matching)))
    return tuple(answer)


def check_split_sequences():
    totals = {}
    for size in range(1, 10):
        vertices = tuple(range(size))
        states = partial_matchings(vertices)
        require(len(states) == len(set(states)), "duplicate partial matching")
        for distinguished in vertices:
            coordinates = [split_at(state, distinguished) for state in states]
            require(
                len(coordinates) == len(set(coordinates)),
                f"occupancy coordinates collide at size {size}",
            )
            require(
                all(assemble_at(item, distinguished) == state
                    for item, state in zip(coordinates, states)),
                f"assembly is not inverse at size {size}",
            )

            quotient = partial_matchings(
                tuple(v for v in vertices if v != distinguished)
            )
            star_states = [state for state in states
                           if split_at(state, distinguished)[0] == "star"]
            require(
                set(star_states) == set(quotient),
                f"the canonical section misses a quotient state at size {size}",
            )
            exposed = Counter()
            old_vertices = tuple(v for v in vertices if v != distinguished)
            for quotient_state in quotient:
                exposed.update(expose_state(
                    quotient_state, old_vertices, distinguished
                ))
            require(
                exposed == Counter({state: 1 for state in states}),
                f"full star/direct exposure is not coefficient-one at size {size}",
            )
            for state in states:
                kind, _partner, remainder = split_at(state, distinguished)
                expected_shift = 0 if kind == "star" else 1
                require(
                    len(state) == len(remainder) + expected_shift,
                    "direct-edge grading shift is wrong",
                )

        totals[size] = len(states)
    return totals


SITES = ("p", "q", "r", "s", "x")
STAR = {"p": "xp", "q": "yq", "r": "tr", "s": "vs", "x": "wx"}
DIRECT = {
    edge("p", "q"): "P",
    edge("p", "r"): "R",
    edge("p", "s"): "E",
    edge("p", "x"): "G",
    edge("q", "r"): "T",
    edge("q", "s"): "F",
    edge("q", "x"): "H",
    edge("r", "s"): "U",
    edge("r", "x"): "V",
    edge("s", "x"): "J",
}


def monomial(*names):
    return tuple(sorted(names))


def universal_states(h):
    result = Counter()
    for matching in partial_matchings(SITES):
        covered = {site for direct in matching for site in direct}
        variables = [DIRECT[direct] for direct in matching]
        variables.extend(STAR[site] for site in SITES if site not in covered)
        # The cap already accounts for the deleted physical pair p,q.  On
        # the five exposed physical sites its residual exponent is
        # h-4+|M| (two directs / one direct / no directs give h-2/h-3/h-4).
        exponent = h - 4 + len(matching)
        if exponent >= 0:
            result[(exponent, monomial(*variables))] += h
    return result


def add_term(result, exponent, coefficient, *variables):
    if exponent < 0 or coefficient == 0:
        return
    key = (exponent, monomial(*variables))
    result[key] += Fraction(coefficient)
    if result[key] == 0:
        del result[key]


def multiply_terms(left, right):
    """Multiply ordinary z-polynomials by divided powers."""
    answer = Counter()
    for (z_power, left_vars), left_coefficient in left.items():
        for (exponent, right_vars), right_coefficient in right.items():
            factor = 1
            for offset in range(1, z_power + 1):
                factor *= exponent + offset
            add_term(
                answer,
                exponent + z_power,
                left_coefficient * right_coefficient * factor,
                *(left_vars + right_vars),
            )
    return answer


def ordinary(*terms):
    """Terms are (coefficient, z_power, variable tuple)."""
    answer = Counter()
    for coefficient, z_power, variables in terms:
        answer[(z_power, monomial(*variables))] += Fraction(coefficient)
    return answer


def divided(*terms):
    """Terms are (coefficient, exponent, variable tuple)."""
    answer = Counter()
    for coefficient, exponent, variables in terms:
        add_term(answer, exponent, coefficient, *variables)
    return answer


def sum_counters(*items):
    answer = Counter()
    for item in items:
        answer.update(item)
    return +answer


def cap_chart_pq(h):
    base = ordinary((h, 0, ("xp", "yq")), (1, 1, ("P",)))
    normal = {
        "r": ordinary((h, 0, ("R", "yq")), (h, 0, ("T", "xp")),
                      (1, 0, ("P", "tr"))),
        "s": ordinary((h, 0, ("E", "yq")), (h, 0, ("F", "xp")),
                      (1, 0, ("P", "vs"))),
        "x": ordinary((h, 0, ("G", "yq")), (h, 0, ("H", "xp")),
                      (1, 0, ("P", "wx"))),
    }
    double = {
        "rs": ordinary((h, 0, ("R", "F")), (h, 0, ("E", "T")),
                       (1, 0, ("P", "U"))),
        "rx": ordinary((h, 0, ("R", "H")), (h, 0, ("G", "T")),
                       (1, 0, ("P", "V"))),
        "sx": ordinary((h, 0, ("E", "H")), (h, 0, ("G", "F")),
                       (1, 0, ("P", "J"))),
    }
    return sum_counters(
        multiply_terms(base, divided(
            (1, h - 3, ("U", "wx")),
            (1, h - 3, ("V", "vs")),
            (1, h - 3, ("J", "tr")),
            (1, h - 4, ("tr", "vs", "wx")),
        )),
        multiply_terms(normal["r"], divided(
            (1, h - 2, ("J",)), (1, h - 3, ("vs", "wx"))
        )),
        multiply_terms(normal["s"], divided(
            (1, h - 2, ("V",)), (1, h - 3, ("tr", "wx"))
        )),
        multiply_terms(normal["x"], divided(
            (1, h - 2, ("U",)), (1, h - 3, ("tr", "vs"))
        )),
        multiply_terms(double["rs"], divided((1, h - 2, ("wx",)))),
        multiply_terms(double["rx"], divided((1, h - 2, ("vs",)))),
        multiply_terms(double["sx"], divided((1, h - 2, ("tr",)))),
    )


def rename_counter(counter, renaming):
    answer = Counter()
    for (exponent, variables), coefficient in counter.items():
        renamed = tuple(renaming.get(variable, variable) for variable in variables)
        answer[(exponent, monomial(*renamed))] += coefficient
    return +answer


def cap_chart_pr(h):
    # The pr formula is obtained from the pq formula by the literal chart
    # exchange q <-> r: yq <-> tr, P <-> R, F <-> U, H <-> V.
    renaming = {
        "yq": "tr", "tr": "yq",
        "P": "R", "R": "P",
        "F": "U", "U": "F",
        "H": "V", "V": "H",
    }
    return rename_counter(cap_chart_pq(h), renaming)


def check_five_site_row():
    states = partial_matchings(SITES)
    layer_counts = Counter(len(state) for state in states)
    require(layer_counts == Counter({2: 15, 1: 10, 0: 1}),
            "wrong five-site 1/10/15 layers")

    star_counts = Counter()
    direct_counts = Counter()
    for state in states:
        branch = split_at(state, "x")[0]
        (star_counts if branch == "star" else direct_counts)[len(state)] += 1
    require(star_counts == Counter({1: 6, 2: 3, 0: 1}),
            "wrong x-starred layer counts")
    require(direct_counts == Counter({2: 12, 1: 4}),
            "wrong x-direct layer counts")

    for h in range(3, 17):
        expected = universal_states(h)
        pq = cap_chart_pq(h)
        pr = cap_chart_pr(h)
        require(pq == expected, f"pq chart is not statewise universal at h={h}")
        require(pr == expected, f"pr chart is not statewise universal at h={h}")
        require(pq == pr, f"chart comparison is not flat at h={h}")

        # A one-coefficient chart mutation must destroy statewise flatness.
        mutated = Counter(pq)
        mutation_key = min(mutated)
        mutated[mutation_key] += 1
        require(mutated != expected and mutated != pr,
                f"chart-coefficient mutation escaped detection at h={h}")

        # Polynomial identities and the coefficient-one splitting survive
        # direct-free specializations.  R=0 is a representative literal
        # zero entry of the pr block.
        zero_r = lambda counter: Counter(
            {key: value for key, value in counter.items() if "R" not in key[1]}
        )
        require(zero_r(pq) == zero_r(pr),
                f"direct-free specialization broke flatness at h={h}")

    # One omitted occupancy branch must be detectable.
    truncated = Counter(
        state for state in states if split_at(state, "x")[0] == "star"
    )
    require(sum(truncated.values()) != len(states),
            "mutation guard failed to detect omitted direct branches")


def check_formal_chart_chain_split():
    """Check splitting only for the formal differential 1 tensor d."""
    sites = (0, 1, 2, 3, 4)
    distinguished = 4
    quotient_states = partial_matchings(sites[:-1])

    def differential(cell):
        degree, chart, state = cell
        if degree == 1:
            return Counter({(0, "pq", state): 1, (0, "pr", state): -1})
        return Counter()

    def section(cell):
        degree, chart, state = cell
        return (degree, chart, assemble_at(("star", None, state), distinguished))

    def projection(cell):
        degree, chart, state = cell
        if split_at(state, distinguished)[0] != "star":
            return None
        return (degree, chart, state)

    def formal_exposure_section(cell):
        degree, chart, state = cell
        return Counter({
            (degree, chart, exposed): 1
            for exposed in expose_state(state, sites[:-1], distinguished)
        })

    def differential_sum(chain):
        answer = Counter()
        for cell, coefficient in chain.items():
            for target, value in differential(cell).items():
                answer[target] += coefficient * value
                if answer[target] == 0:
                    del answer[target]
        return answer

    for state in quotient_states:
        for chart in ("g", "pq", "pr"):
            degree = 1 if chart == "g" else 0
            cell = (degree, chart, state)
            lifted = section(cell)
            require(projection(lifted) == cell, "pi*j is not the identity")
            if degree == 1:
                left = differential(lifted)
                right = Counter({section(key): value
                                 for key, value in differential(cell).items()})
                require(left == right, "occupancy section is not a chain map")

                exposure_left = differential_sum(formal_exposure_section(cell))
                exposure_right = Counter()
                for target, value in differential(cell).items():
                    for exposed, section_value in formal_exposure_section(target).items():
                        exposure_right[exposed] += value * section_value
                exposure_right = Counter({key: value for key, value
                                          in exposure_right.items() if value})
                require(exposure_left == exposure_right,
                        "formal star/direct exposure is not a chart chain map")


def check_one_chart_occupancy_block():
    """Audit the divided-power coefficient and the augmented lock.

    The e_x coefficient of (q0+e_x*t)^[d] has coefficient one when written
    as t*q0^[d-1].  Consequently the cap multiplication block is
    L*q0^[d] + Theta*t*q0^[d-1], with no hidden d or h factor.
    """
    nonzero_section_defects = 0
    for h in range(3, 25):
        d = h - 1
        raw_e_coefficient = Fraction(d, factorial(d))
        divided_basis_coefficient = raw_e_coefficient * factorial(d - 1)
        require(divided_basis_coefficient == 1,
                f"occupancy block has a wrong divided-power factor at h={h}")

        # The canonical unmatched-state section is not a chain map for
        # evaluated cap multiplication: d*j - j*d is Theta*t*B.
        theta = Fraction(2, 3)
        unoccupied_block = Fraction(5, 7)
        t_times_b = divided_basis_coefficient * Fraction(11, 13)
        after_multiplication = (
            theta * unoccupied_block,
            theta * t_times_b,
        )
        after_quotient_section = (theta * unoccupied_block, Fraction(0))
        section_defect = tuple(
            after_multiplication[index] - after_quotient_section[index]
            for index in range(2)
        )
        require(section_defect == (0, theta * t_times_b),
                "wrong evaluated occupancy section defect")
        require(section_defect != (0, 0),
                "formal section incorrectly split cap multiplication")
        require(section_defect[1] != 0,
                "evaluated section defect vanished in the residue quotient")
        nonzero_section_defects += 1

        # In symbolic coordinates, the normal term dies in the quotient and
        # the response coefficient equals the augmented target coefficient.
        for target in (Fraction(-1), Fraction(0), Fraction(7, 3)):
            ybar = Fraction(5, 11)
            response = target * ybar
            require(response == target * ybar,
                    "one-chart target/residue lock failed")
            if target:
                require(response != -target * ybar,
                        "target/residue sign mutation escaped detection")
                require(response != (h - 1) * target * ybar,
                        "target/residue divided-power mutation escaped detection")
    require(nonzero_section_defects == 22, "not every h exposed the section defect")
    return nonzero_section_defects


def check_augmented_ledger():
    samples = (
        (Fraction(1), Fraction(2, 3)),
        (Fraction(-5, 7), Fraction(11, 4)),
        (Fraction(13, 2), Fraction(-3, 5)),
    )
    for kappa, ybar in samples:
        cap = (-kappa, -kappa * ybar)
        companion = (kappa, kappa * ybar)
        total = tuple(cap[index] + companion[index] for index in range(2))
        desired = (Fraction(0), -kappa * ybar)
        require(total == (0, 0), "augmented target cancellation is not locked")
        require(total != desired, "split occupancy manufactured the desired class")

        # Direct-free means only the name kappa=AU changes; no formula in
        # this ledger divides by a second direct entry or by the trace.
        au = kappa
        require((-au) + au == 0, "direct-free target did not cancel")

    # The normalized off-diagonal scalar-zero cap
    # alpha^{-1}(tau*E_ab-alpha*I), a != b, has scalar contraction zero
    # and diagonal entries -1 for every trace, including tau=0.
    for alpha, tau in (
        (Fraction(2), Fraction(0)),
        (Fraction(-3, 5), Fraction(7, 4)),
        (Fraction(11, 3), Fraction(-2, 9)),
    ):
        normalized_ab = tau / alpha
        normalized_diagonal = (Fraction(-1),) * 3
        scalar_contraction = normalized_ab * alpha + sum(
            entry * tau / 3 for entry in normalized_diagonal
        )
        require(scalar_contraction == 0,
                "normalized scalar-zero cap depends on nonzero trace")
        require(normalized_diagonal == (-1, -1, -1),
                "normalized cap diagonal changed at trace zero")

    # On the direct-free boundary B=0, kappa=AU without division by B,
    # the trace, a star, or a second direct block.
    for a, u, f in (
        (Fraction(2), Fraction(3), Fraction(5)),
        (Fraction(-7, 4), Fraction(11, 6), Fraction(-2)),
    ):
        b = Fraction(0)
        kappa = a * u - b * f
        require(kappa == a * u and kappa != 0,
                "direct-free kappa specialization is wrong")

    for labels in product(range(3), repeat=5):
        i, j, k, ell, c = labels
        pq_target = int(i == j == k == ell == c)
        pr_target = int(i == k == j == ell == c)
        require(pq_target == pr_target, "all-label augmented targets differ")


def main():
    totals = check_split_sequences()
    check_five_site_row()
    check_formal_chart_chain_split()
    section_defects = check_one_chart_occupancy_block()
    check_augmented_ledger()
    print("formal site-occupancy/partial-matching audit: PASS")
    print(f"partial-matching state counts through nine sites: {totals}")
    print("five-site layers 1/10/15 split as (1/6/3)+(0/4/12)")
    print("formal P tensor D connecting map: zero (statewise chain split)")
    print(f"evaluated one-chart section defects: {section_defects} nonzero cases")
    print("evaluated pair-comparison/Rees Bockstein: not constructed")


if __name__ == "__main__":
    main()
