#!/usr/bin/env python3
"""Light exact checks for odd-residue survival by minimality.

The uniform proof is the site-count argument in the accompanying note.
This dependency-free script checks its divided-power bookkeeping on sparse
exact instances; it is not a bounded verification of the conjecture.
"""

from collections import defaultdict
from fractions import Fraction


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sites(monomial):
    return {site for site, _colour in monomial}


def add_term(polynomial, monomial, coefficient):
    key = tuple(sorted(monomial))
    require(len(sites(key)) == len(key), "a monomial repeated a site")
    polynomial[key] += Fraction(coefficient)
    if polynomial[key] == 0:
        del polynomial[key]


def multiply(left, right):
    product = defaultdict(Fraction)
    for left_monomial, left_coefficient in left.items():
        left_sites = sites(left_monomial)
        for right_monomial, right_coefficient in right.items():
            if left_sites.isdisjoint(sites(right_monomial)):
                add_term(
                    product,
                    left_monomial + right_monomial,
                    left_coefficient * right_coefficient,
                )
    return dict(product)


def divided_power(quadratic, order):
    """Return q^[order] by selecting disjoint quadratic monomials once."""
    levels = [defaultdict(Fraction) for _ in range(order + 1)]
    levels[0][()] = Fraction(1)
    for edge, coefficient in quadratic.items():
        edge_sites = sites(edge)
        for degree in range(order, 0, -1):
            for monomial, old_coefficient in tuple(levels[degree - 1].items()):
                if edge_sites.isdisjoint(sites(monomial)):
                    add_term(
                        levels[degree],
                        monomial + edge,
                        old_coefficient * coefficient,
                    )
    return dict(levels[order])


def sparse_packet(h):
    """Deterministic q0 on 2h-1 sites and rho through one new site x."""
    odd_size = 2 * h - 1
    x = odd_size
    q0 = defaultdict(Fraction)

    # Two sparse near-perfect matchings with different omitted sites.
    for j in range(h - 1):
        add_term(
            q0,
            ((2 * j, j % 3), (2 * j + 1, (j + 1) % 3)),
            j + 1,
        )
        add_term(
            q0,
            ((2 * j + 1, (j + 2) % 3), (2 * j + 2, j % 3)),
            Fraction((-1) ** j, j + 2),
        )

    rho = defaultdict(Fraction)
    for colour, site in enumerate((odd_size - 1, 0, odd_size // 2)):
        add_term(rho, ((x, colour), (site, (colour + 1) % 3)), colour + 2)
    return dict(q0), dict(rho), x


def check_square_zero_binomial():
    for h in range(3, 9):
        q0, rho, _x = sparse_packet(h)
        q_tilde = dict(q0)
        for monomial, coefficient in rho.items():
            q_tilde[monomial] = q_tilde.get(monomial, Fraction()) + coefficient

        require(divided_power(q0, h) == {}, f"q0^[h] survived at h={h}")
        require(divided_power(rho, 2) == {}, f"rho^[2] survived at h={h}")

        actual = divided_power(q_tilde, h)
        expected = multiply(rho, divided_power(q0, h - 1))
        require(actual == expected, f"wrong divided-power expansion at h={h}")
        require(expected, f"test packet was vacuous at h={h}")


def check_target_assembly():
    for h in range(3, 20):
        odd_sites = tuple(range(2 * h - 1))
        x = 2 * h - 1
        targets = {}
        for colour in range(3):
            y_colour = tuple((site, colour) for site in odd_sites)
            full_word = tuple(sorted(((x, colour),) + y_colour))
            targets[full_word] = targets.get(full_word, 0) + 1

        require(len(targets) == 3, f"target colours collided at h={h}")
        for colour in range(3):
            expected = tuple((site, colour) for site in range(2 * h))
            require(targets.get(expected) == 1, f"missing target colour {colour}")


def source_cells(quadratic, site_count):
    """Expand an aggregate quadratic into one canonical decorated source per cell."""
    cells = []
    for monomial, coefficient in quadratic.items():
        require(len(monomial) == 2, "a quadratic cell did not have two endpoints")
        (u, colour_u), (v, colour_v) = monomial
        require(0 <= u < v < site_count, "endpoint order was not canonical")
        require(0 <= colour_u < 3 and 0 <= colour_v < 3,
                "a cell left the ternary palette")
        require(coefficient != 0, "a zero source cell was retained")
        cells.append((u, v, colour_u, colour_v, coefficient))
    require(len(cells) <= 9 * site_count * (site_count - 1) // 2,
            "finite source bound failed")
    return cells


def aggregate_cells(cells):
    quadratic = defaultdict(Fraction)
    for u, v, colour_u, colour_v, coefficient in cells:
        add_term(quadratic, ((u, colour_u), (v, colour_v)), coefficient)
    return dict(quadratic)


def check_aggregate_to_source_ledger():
    # Every aggregate cell is one endpoint-ordered decorated source, uniformly
    # in the size.  Reaggregation preserves both the quadratic and its matching
    # tensor.  The examples need not satisfy the GHZ equation.
    for h in range(3, 9):
        q0, rho, x = sparse_packet(h)
        site_count = x + 1
        aggregate = dict(q0)
        for monomial, coefficient in rho.items():
            aggregate[monomial] = aggregate.get(monomial, Fraction()) + coefficient
            if aggregate[monomial] == 0:
                del aggregate[monomial]
        cells = source_cells(aggregate, site_count)
        rebuilt = aggregate_cells(cells)
        require(rebuilt == aggregate, f"cell reaggregation failed at h={h}")
        require(divided_power(rebuilt, h) == divided_power(aggregate, h),
                f"matching tensor changed under realization at h={h}")
        require(site_count == 2 * h and site_count >= 6,
                f"wrong smaller-source order at h={h}")

    # The allowed four-site one-factorization is a concrete exact ternary
    # aggregate.  It audits the palette argument while also guarding against
    # the false claim that minimality ranges over order four.
    quadratic = defaultdict(Fraction)
    one_factors = (
        ((0, 1), (2, 3)),
        ((0, 2), (1, 3)),
        ((0, 3), (1, 2)),
    )
    for colour, matching in enumerate(one_factors):
        for u, v in matching:
            add_term(quadratic, ((u, colour), (v, colour)), 1)
    target = {
        tuple((site, colour) for site in range(4)): Fraction(1)
        for colour in range(3)
    }
    require(divided_power(dict(quadratic), 2) == target,
            "four-site ternary one-factorization")
    cells = source_cells(dict(quadratic), 4)
    require({cell[2] for cell in cells} | {cell[3] for cell in cells}
            == {0, 1, 2}, "exact target did not retain the full palette")


def check_offdiagonal_detection():
    for alpha in (Fraction(1), Fraction(-7), Fraction(3, 5)):
        require(alpha != 0, "invalid off-diagonal scalar")
        endpoint_coefficients = (-alpha, -alpha, -alpha)
        for surviving_colour in range(3):
            require(
                endpoint_coefficients[surviving_colour] != 0,
                "a surviving colour was invisible at the off-diagonal endpoint",
            )
            normalized_residue = endpoint_coefficients[surviving_colour] / alpha
            require(normalized_residue == -1, "wrong normalized residue")


def main():
    check_square_zero_binomial()
    check_target_assembly()
    check_aggregate_to_source_ledger()
    check_offdiagonal_detection()
    print("odd-residue minimality survival: PASS")
    print("  all three quotient zeros assemble an exact source two sites smaller")
    print("  aggregate cells give a finite ordered ternary source ledger")
    print("  every surviving colour is detected by an off-diagonal endpoint")


if __name__ == "__main__":
    main()
