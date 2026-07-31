#!/usr/bin/env python3
"""Audit the complementary scalar-unit pivot and its support ledger.

All arithmetic is exact.  The carrier check keeps the two endpoint orders
``BF`` and ``EC`` separate and verifies a coefficient after restriction away
from the two residual sites, which is the literal physical four-cut layer.
"""

from fractions import Fraction
from itertools import combinations, product


def require(condition, message):
    """Raise explicitly, including under ``python -O``."""

    if not condition:
        raise RuntimeError(message)


def dp_linear_power(left, right, degree):
    """Coefficients of (left*q + right*r)^[degree] in the DP basis."""

    require(degree >= 0, "negative divided-power degree")
    return [left ** (degree - k) * right**k for k in range(degree + 1)]


def audit_divided_power_scaling():
    for h in range(3, 65):
        for alpha in (Fraction(2), Fraction(-3), Fraction(5, 2)):
            g_adjacent = dp_linear_power(alpha, Fraction(1), h - 1)
            pivot_adjacent = dp_linear_power(Fraction(1), 1 / alpha, h - 1)
            scaled_g = [
                coefficient / alpha ** (h - 1) for coefficient in g_adjacent
            ]
            require(scaled_g == pivot_adjacent, f"adjacent scaling failed at h={h}")

            theta_scaled = list(scaled_g)
            theta_scaled[0] -= 1
            require(theta_scaled[0] == 0, "theta must have no pure-q coefficient")
            require(
                all(theta_scaled[k] == alpha ** (-k) for k in range(1, h)),
                f"theta coefficients failed at h={h}",
            )

            g_top = dp_linear_power(alpha, Fraction(1), h)
            pivot_top = dp_linear_power(Fraction(1), 1 / alpha, h)
            require(
                [coefficient / alpha**h for coefficient in g_top] == pivot_top,
                f"top scaling failed at h={h}",
            )


def pivot_row_residuals(h, alpha, unary_error, jets, selected=0):
    """Return transformed-row minus target for the nine physical rows.

    ``jets[(i,j)]`` denotes ``R_ij*Theta``.  Rows meeting the selected
    coordinate are deleted, so only the four complementary jets occur.
    """

    labels = (0, 1, 2)
    scale = alpha ** (1 - h)
    residuals = {}
    for i in labels:
        for j in labels:
            if i == selected and j == selected:
                residuals[i, j] = scale * unary_error
            elif i == selected or j == selected:
                residuals[i, j] = Fraction(0)
            else:
                residuals[i, j] = scale * jets.get((i, j), Fraction(0))
    return residuals


def audit_four_row_reconstruction():
    labels = (0, 1, 2)
    selected = 0
    complementary = {(i, j) for i in (1, 2) for j in (1, 2)}

    for h in range(3, 33):
        alpha = Fraction(-2)
        arbitrary_selected_jets = {
            (i, j): Fraction(10 + 3 * i + j)
            for i in labels
            for j in labels
            if i == selected or j == selected
        }
        residuals = pivot_row_residuals(
            h, alpha, Fraction(0), arbitrary_selected_jets, selected
        )
        require(
            not any(residuals.values()),
            "a deleted selected row survived the pivot",
        )

        used_jet_cells = set()
        for cell in ((i, j) for i in labels for j in labels):
            perturbed = pivot_row_residuals(
                h, alpha, Fraction(0), {cell: Fraction(1)}, selected
            )
            changed = {row for row, value in perturbed.items() if value}
            if changed:
                used_jet_cells.add(cell)
                require(changed == {cell}, "one complementary jet changed another row")
        require(
            used_jet_cells == complementary,
            "the pivot did not use exactly the four complementary jets",
        )

        unary_residual = pivot_row_residuals(
            h, alpha, Fraction(1), {}, selected
        )
        require(
            set(row for row, value in unary_residual.items() if value)
            == {(selected, selected)},
            "the unary error appeared outside the direct selected row",
        )


def rank(vectors):
    rows = [list(map(Fraction, vector)) for vector in vectors]
    if not rows:
        return 0
    row = 0
    columns = len(rows[0])
    for column in range(columns):
        pivot = next((r for r in range(row, len(rows)) if rows[r][column]), None)
        if pivot is None:
            continue
        rows[row], rows[pivot] = rows[pivot], rows[row]
        value = rows[row][column]
        rows[row] = [entry / value for entry in rows[row]]
        for r in range(len(rows)):
            if r != row and rows[r][column]:
                factor = rows[r][column]
                rows[r] = [x - factor * y for x, y in zip(rows[r], rows[row])]
        row += 1
        if row == len(rows):
            break
    return row


def audit_essential_pair():
    # Two injective endpoint stars.  Test every possible selected coordinate.
    stars = (
        [(1, 0, 1, 0), (0, 1, 1, 0), (0, 0, 1, 1)],
        [(1, 1, 0, 0), (0, 1, 0, 1), (0, 0, 1, 1)],
    )
    require(all(rank(star) == 3 for star in stars), "input stars are not good")

    for selected in range(3):
        complementary = [i for i in range(3) if i != selected]
        for star in stars:
            surviving = [star[i] for i in complementary]
            require(rank(surviving) == 2, "pivoted star is not rank two")

        plane = [tuple(int(j == i) for j in range(3)) for i in complementary]
        direct_line = [tuple(int(j == selected) for j in range(3))]
        require(rank(plane) == 2, "wrong complementary endpoint plane")
        require(rank(plane + direct_line) == 3, "direct edge is not essential")


def response_contributions(p_entries, s_entries):
    """Ordered star products grouped by unordered decorated internal cell."""

    output = {}
    for p_atom, p_value in p_entries.items():
        for s_atom, s_value in s_entries.items():
            if p_atom[0] == s_atom[0]:
                continue
            cell = tuple(sorted((p_atom, s_atom)))
            output.setdefault(cell, []).append((p_atom, s_atom, p_value * s_value))
    return output


def response_product(p_entries, s_entries):
    """Square-free product support, retaining orientation cancellation."""

    output = {
        cell: sum((term[2] for term in terms), Fraction(0))
        for cell, terms in response_contributions(p_entries, s_entries).items()
    }
    return {cell: value for cell, value in output.items() if value}


def oriented_cell_products(p_entries, s_entries, cell):
    """Return BF and EC for the site order carried by ``cell``."""

    left, right = cell
    require(left[0] < right[0], "internal cell does not have distinct ordered sites")
    bf = p_entries.get(left, Fraction(0)) * s_entries.get(right, Fraction(0))
    ec = p_entries.get(right, Fraction(0)) * s_entries.get(left, Fraction(0))
    return bf, ec


def pivot_internal(q_entries, response, alpha):
    output = {}
    for cell in set(q_entries) | set(response):
        value = q_entries.get(cell, Fraction(0)) + response.get(
            cell, Fraction(0)
        ) / alpha
        if value:
            output[cell] = value
    return output


def support_ledger(q_entries, pivoted_entries):
    old = set(q_entries)
    new = set(pivoted_entries)
    gained = new - old
    lost = old - new
    return len(gained) - len(lost), gained, lost


def audit_abstract_support_ledger():
    """Exhaust the finite integer ledger behind mn >= m+n and rigidity."""

    feasible = 0
    equality_cases = 0
    for m in range(1, 7):
        for n in range(1, 7):
            for response_size in range(m * n + 1):
                for gained in range(response_size + 1):
                    for lost in range(6):
                        if gained - lost < m + n:
                            continue
                        feasible += 1
                        require(m * n >= m + n, "support ledger missed mn >= m+n")
                        require(m >= 2 and n >= 2, "support ledger admitted a singleton")
                        if m == n == 2:
                            equality_cases += 1
                            require(
                                response_size == gained == 4 and lost == 0,
                                "two-by-two numerical rigidity failed",
                            )
    require(feasible and equality_cases, "support-ledger audit was vacuous")


def audit_two_by_two_rigidity():
    """Exhaust support overlap/cancellation modes for two-by-two packets."""

    atoms = [(site, site % 2) for site in range(4)]
    alpha = Fraction(2)
    admitted = 0
    for p_support in combinations(atoms, 2):
        for s_support in combinations(atoms, 2):
            p_entries = {
                atom: Fraction(2 * atom[0] + 1) for atom in p_support
            }
            s_entries = {
                atom: Fraction(2 * atom[0] + 3) for atom in s_support
            }
            response = response_product(p_entries, s_entries)
            cells = sorted(response)
            for modes in product(range(3), repeat=len(cells)):
                # 0: absent from q; 1: overlaps and survives; 2: cancels in q#.
                q_entries = {}
                for cell, mode in zip(cells, modes):
                    if mode == 1:
                        q_entries[cell] = response[cell]
                    elif mode == 2:
                        q_entries[cell] = -response[cell] / alpha
                pivoted = pivot_internal(q_entries, response, alpha)
                delta, gained, lost = support_ledger(q_entries, pivoted)
                if delta < 4:
                    continue
                admitted += 1
                contributions = response_contributions(p_entries, s_entries)
                require(len(response) == 4, "minimal two-by-two packet lost a cell")
                require(gained == set(response), "not every response cell is new")
                require(not lost, "two-by-two equality packet lost an old q-cell")
                require(not (set(response) & set(q_entries)), "equality packet overlaps q")
                require(
                    sum(len(terms) for terms in contributions.values()) == 4,
                    "an ordered product vanished or merged in the equality packet",
                )
                require(
                    all(len(contributions[cell]) == 1 for cell in response),
                    "an equality cell has two endpoint orientations",
                )
    require(admitted, "two-by-two rigidity audit found no admitted ledger")


def select_new_cell_detection(p_entries, s_entries, q_entries, carrier, alpha):
    """Select a nonzero oriented curvature times a restricted H coefficient."""

    response = response_product(p_entries, s_entries)
    pivoted = pivot_internal(q_entries, response, alpha)
    _, gained, _ = support_ledger(q_entries, pivoted)
    for cell in gained:
        h_coefficient = carrier.get(cell, Fraction(0))
        if not h_coefficient:
            continue
        require(q_entries.get(cell, Fraction(0)) == 0, "new cell has an old q-entry")
        bf, ec = oriented_cell_products(p_entries, s_entries, cell)
        for oriented_star_product in (bf, ec):
            if oriented_star_product:
                curvature = -oriented_star_product
                if curvature * h_coefficient:
                    return cell, curvature * h_coefficient
    return None


def audit_oriented_four_cut_detection():
    # Interleaving the sites forces two BF cells and two EC cells.
    p_two = {(0, 0): Fraction(1), (3, 1): Fraction(2)}
    s_two = {(1, 2): Fraction(3), (2, 0): Fraction(5)}
    response = response_product(p_two, s_two)
    require(len(response) == 4, "two-by-two physical packet is not four cells")

    alpha = Fraction(2)
    q_entries = {((6, 0), (7, 0)): Fraction(11)}
    pivoted = pivot_internal(q_entries, response, alpha)
    delta, gained, lost = support_ledger(q_entries, pivoted)
    require(delta == 4, "wrong two-by-two pivot support change")
    require(gained == set(response) and not lost, "four cells are not all new")

    h = 3
    carrier_monomial = ((8, 1), (9, 2))
    require(
        len(carrier_monomial) == 2 * (h - 2),
        "restricted carrier has the wrong site degree",
    )
    require(
        len({atom[0] for atom in carrier_monomial}) == len(carrier_monomial),
        "restricted carrier repeats a physical site",
    )

    carrier = {
        cell: Fraction(7 + index)
        for index, cell in enumerate(sorted(response))
    }
    forward_cells = 0
    backward_cells = 0
    for cell, response_coefficient in response.items():
        require(
            not ({atom[0] for atom in cell} & {atom[0] for atom in carrier_monomial}),
            "carrier coefficient was not restricted away from the exposed sites",
        )
        bf, ec = oriented_cell_products(p_two, s_two, cell)
        require(bf + ec == response_coefficient, "BF+EC endpoint order is wrong")
        require(bool(bf) != bool(ec), "equality cell is not uniquely oriented")
        forward_cells += int(bool(bf))
        backward_cells += int(bool(ec))

        star_product = bf or ec
        theta_term = response_coefficient * carrier[cell]
        curvature_carrier = (-star_product) * carrier[cell]
        require(theta_term != 0, "chosen Theta coefficient vanished")
        require(curvature_carrier != 0, "oriented four-cut carrier vanished")
        require(
            curvature_carrier == -theta_term,
            "oriented curvature/carrier sign is wrong",
        )

    require(
        forward_cells == backward_cells == 2,
        "the carrier audit did not exercise both endpoint orientations",
    )
    require(
        select_new_cell_detection(p_two, s_two, q_entries, carrier, alpha),
        "Theta did not select a new-cell oriented four-cut coefficient",
    )

    # Outside m=n=2, Theta can be confined to an R-cell already in supp(q).
    p_general = {(0, 0): Fraction(1), (4, 0): Fraction(2)}
    s_general = {
        (1, 1): Fraction(3),
        (2, 1): Fraction(5),
        (3, 1): Fraction(7),
    }
    general_response = response_product(p_general, s_general)
    require(len(general_response) == 6, "general fork packet is not two-by-three")
    overlap = sorted(general_response)[0]
    q_general = {overlap: general_response[overlap]}
    general_pivot = pivot_internal(q_general, general_response, alpha)
    general_delta, general_new, general_lost = support_ledger(
        q_general, general_pivot
    )
    require(
        general_delta == 5 and len(general_new) == 5 and not general_lost,
        "general new-cell support fork has the wrong ledger",
    )

    confined_carrier = {overlap: Fraction(13)}
    require(
        general_response[overlap] * confined_carrier[overlap] != 0,
        "confined Theta guard vanished",
    )
    require(
        select_new_cell_detection(
            p_general, s_general, q_general, confined_carrier, alpha
        )
        is None,
        "support alone falsely moved a confined carrier to a new cell",
    )

    one_new_cell = next(iter(general_new))
    detected_carrier = dict(confined_carrier)
    detected_carrier[one_new_cell] = Fraction(17)
    require(
        select_new_cell_detection(
            p_general, s_general, q_general, detected_carrier, alpha
        ),
        "a nonzero new-cell restriction failed to detect curvature",
    )


def audit_support_bounds():
    atoms = [(site, colour) for site in range(3) for colour in range(2)]
    nonempty = []
    for size in range(1, len(atoms) + 1):
        for subset in combinations(atoms, size):
            entries = {
                atom: Fraction(-1 if (atom[0] + atom[1]) % 2 else 1)
                for atom in subset
            }
            nonempty.append(entries)

    for p_entries in nonempty:
        for s_entries in nonempty:
            response = response_product(p_entries, s_entries)
            contributions = response_contributions(p_entries, s_entries)
            m, n = len(p_entries), len(s_entries)
            require(len(response) <= m * n, "outer-product support bound failed")
            for cell, terms in contributions.items():
                bf, ec = oriented_cell_products(p_entries, s_entries, cell)
                require(
                    bf + ec == sum((term[2] for term in terms), Fraction(0)),
                    "ordered response decomposition failed",
                )
            if len(response) >= m + n:
                require(m >= 2 and n >= 2, "support escalation missed a singleton")

    p_three = {(0, 0): Fraction(1), (1, 0): Fraction(2), (2, 0): Fraction(3)}
    s_three = {(3, 1): Fraction(5), (4, 1): Fraction(7), (5, 1): Fraction(11)}
    nine = response_product(p_three, s_three)
    require(len(nine) == 9, "three-by-three nonmonotone guard is not nine cells")
    require(len(nine) - len(p_three) - len(s_three) == 3, "wrong nine-for-six cost")

    # Same-site loss and an exact two-orientation cancellation are genuine.
    require(
        not response_product({(0, 0): Fraction(1)}, {(0, 1): Fraction(1)}),
        "same-site product survived the square-zero quotient",
    )
    p_cancel = {(0, 0): Fraction(1), (1, 0): Fraction(1)}
    s_cancel = {(0, 0): Fraction(1), (1, 0): Fraction(-1)}
    require(not response_product(p_cancel, s_cancel), "orientation cancellation failed")


def mutation_checks():
    h = 7
    alpha = Fraction(2)
    g_adjacent = dp_linear_power(alpha, Fraction(1), h - 1)
    pivot_adjacent = dp_linear_power(Fraction(1), 1 / alpha, h - 1)
    require(
        [coefficient / alpha**h for coefficient in g_adjacent]
        != pivot_adjacent,
        "mutation accepted alpha^h in the adjacent scaling",
    )

    leaked = pivot_row_residuals(
        h, alpha, Fraction(0), {(1, 2): Fraction(1)}, selected=0
    )
    require(leaked[1, 2] != 0, "mutation dropped a complementary jet condition")

    plane = [(0, 1, 0), (0, 0, 1)]
    wrong_direct_line = [(0, 1, 0)]
    require(
        rank(plane + wrong_direct_line) == 2,
        "mutation made a complementary direct line essential",
    )

    p_entries = {(0, 0): Fraction(1), (3, 1): Fraction(2)}
    s_entries = {(1, 2): Fraction(3), (2, 0): Fraction(5)}
    response = response_product(p_entries, s_entries)
    backward_cell = next(
        cell
        for cell in response
        if oriented_cell_products(p_entries, s_entries, cell)[1]
    )
    bf, ec = oriented_cell_products(p_entries, s_entries, backward_cell)
    require(not bf and ec, "backward-orientation mutation guard is not selective")
    left, right = backward_cell
    wrong_ec = p_entries.get(left, 0) * s_entries.get(right, 0)
    require(wrong_ec != ec, "mutation accepted BF in place of EC")

    carrier = Fraction(19)
    require(
        response[backward_cell] * carrier
        != -response[backward_cell] * carrier,
        "mutation accepted the wrong curvature sign",
    )

    q_overlap = {backward_cell: -response[backward_cell] / alpha}
    pivoted = pivot_internal(q_overlap, response, alpha)
    delta, _, lost = support_ledger(q_overlap, pivoted)
    require(
        delta < 4 and lost == {backward_cell},
        "mutation ignored old-entry cancellation in the support difference",
    )


def main():
    audit_divided_power_scaling()
    audit_four_row_reconstruction()
    audit_essential_pair()
    audit_abstract_support_ledger()
    audit_support_bounds()
    audit_two_by_two_rigidity()
    audit_oriented_four_cut_detection()
    mutation_checks()
    print(
        "scalar-unit complementary pivot / essential-pair audit: PASS; "
        "h=3..64, exact four-row/rank/support/carrier ledgers and "
        "6 adversarial mutations audited"
    )


if __name__ == "__main__":
    main()
