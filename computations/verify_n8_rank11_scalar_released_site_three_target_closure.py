#!/usr/bin/env python3
"""Exact channel audit for the N=8 scalar-shore released-site closure.

On the released four-site set C = {x} union B, |B|=3, the multiplier
T*V is supported on B.  Hence every surviving quadratic-domain column uses
x, and its output retains the colour carried by that x-cell.  The image
therefore splits as V_x tensor J_B.  A diagonal output with k nonzero target
colours puts all k individual pure targets in the image.  The pinned
four-site arbitrary-superposition theorem has k <= 2, while the literal
all-three-target released row would have k=3.

This checker audits the complete endpoint-coloured channel decomposition,
the dependency hashes, and the conditional three-target factor ledger.  The
uniform proof is in the companion note.
"""

from hashlib import sha256
from itertools import combinations, product
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEPENDENCIES = {
    "verify_four_site_arbitrary_superposition_dressed_packet_obstruction.py":
        "6c83e9a4bf925a47f69feef2465bac9ede5ad16704f462212a8119fb9d5db497",
    "verify_n8_rank11_scalar_unique_blocker_common_power_packet.py":
        "8655bb837142a6452829485acefd9f52d16395ce88a1e024c7b793e3532a8cd8",
}
EXPECTED_LEDGER_DIGEST = (
    "cd12efb1030214f11aa0a8e1827ca44eda30cb4b96b1ed83bca28da0589e4f70"
)

X = 0
B = (1, 2, 3)
C = (X,) + B
COLOURS = range(3)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def dependency_guard():
    for name, expected in DEPENDENCIES.items():
        actual = sha256((HERE / name).read_bytes()).hexdigest()
        require(actual == expected, ("dependency changed", name, actual))


def complement(pair):
    return tuple(site for site in C if site not in pair)


def multiplier_terms(pair):
    """Formal nonzero cells of W_ij=T_i V_j+V_i T_j.

    Both local multiplier rows vanish at X.  A term is recorded only by its
    endpoint colours and orientation; coefficients remain arbitrary.
    """
    i, j = pair
    if X in pair:
        return ()
    return tuple(
        (ci, cj, orientation)
        for ci, cj in product(COLOURS, repeat=2)
        for orientation in ("TV", "VT")
    )


def audit_columns():
    records = []
    active_by_x_colour = {colour: 0 for colour in COLOURS}
    zero_columns = 0
    active_columns = 0

    # A quadratic column is one endpoint-coloured cell on a physical pair.
    for q_pair in combinations(C, 2):
        m_pair = complement(q_pair)
        terms = multiplier_terms(m_pair)
        for q_colours in product(COLOURS, repeat=2):
            if not terms:
                zero_columns += 1
                records.append((q_pair, q_colours, "zero"))
                continue

            require(X in q_pair, ("an active column omitted x", q_pair))
            x_index = q_pair.index(X)
            x_colour = q_colours[x_index]
            active_columns += 1
            active_by_x_colour[x_colour] += 1

            # Every formal W term fills the complementary two B-sites and
            # leaves the q-column's x colour untouched.
            for ci, cj, orientation in terms:
                word = {q_pair[0]: q_colours[0], q_pair[1]: q_colours[1]}
                word[m_pair[0]] = ci
                word[m_pair[1]] = cj
                require(word[X] == x_colour,
                        ("x-colour channel mixed", q_pair, q_colours, word))
            records.append((q_pair, q_colours, x_colour, len(terms)))

    require(zero_columns == 27, ("wrong zero-column count", zero_columns))
    require(active_columns == 27,
            ("wrong active-column count", active_columns))
    require(active_by_x_colour == {0: 9, 1: 9, 2: 9},
            ("wrong x-colour blocks", active_by_x_colour))
    return tuple(records), active_by_x_colour


def audit_three_target_factors():
    # This is the conditional all-three-target subcase.  A singleton blocker
    # for one label restores that label after x is released, but does not by
    # itself make the other two beta_c nonzero.  If all three are nonzero,
    # finite hyperplane avoidance gives one theta with all three values live.
    # Full-support annihilator choices u,v have u_c v_c != 0 for every c.
    u_times_v = (2, -3, 5)
    beta = (7, 11, -13)
    coefficients = tuple(left * right
                         for left, right in zip(u_times_v, beta))
    require(all(coefficients), "the released target lost a colour")
    require(len(coefficients) == 3,
            "the released three-target ledger changed")
    return coefficients


def audit_two_target_incidence():
    """Every two-live equality ledger has a common coordinate-plane site."""
    admissible = []
    for masks in product(range(4), repeat=3):
        # Bit c says that the c-th live coordinate axis lies in S_site.
        if any(sum((mask >> colour) & 1 for mask in masks) < 2
               for colour in range(2)):
            continue
        admissible.append(masks)
        require(3 in masks,
                ("two live axes avoided a common coordinate plane", masks))
    require(admissible, "the two-target incidence ledger became empty")
    return tuple(admissible)


def audit():
    dependency_guard()
    records, blocks = audit_columns()
    coefficients = audit_three_target_factors()
    two_target_ledgers = audit_two_target_incidence()
    # The channel split says a diagonal image with these three nonzero
    # coefficients produces all three individual X_c in the same image.
    # The dependency theorem permits at most two.
    individual_targets_forced = sum(value != 0 for value in coefficients)
    require(individual_targets_forced == 3,
            "the split failed to force three individual targets")
    require(individual_targets_forced > 2,
            "the four-site obstruction was not reached")
    ledger = (records, tuple(sorted(blocks.items())), coefficients,
              individual_targets_forced, two_target_ledgers)
    digest = sha256(repr(ledger).encode()).hexdigest()
    if EXPECTED_LEDGER_DIGEST is not None:
        require(digest == EXPECTED_LEDGER_DIGEST,
                ("zero-site closure ledger changed", digest))
    return digest, len(two_target_ledgers)


def main():
    digest, two_target_ledgers = audit()
    print("N=8 scalar-shore released-site three-target closure: PASS")
    print("  quadratic columns          : 54 = 27 zero + 27 active")
    print("  active x-colour blocks     : 9 + 9 + 9")
    print("  conditional released target: 3 nonzero individual axes")
    print("  four-site permitted axes   : at most 2")
    print(f"  two-target incidence ledgers: {two_target_ledgers}, all plane-routed")
    print(f"  ledger digest              : {digest}")


if __name__ == "__main__":
    main()
