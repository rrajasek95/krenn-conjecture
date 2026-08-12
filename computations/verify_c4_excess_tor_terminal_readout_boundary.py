#!/usr/bin/env python3
"""Exact terminal-readout boundary for the flat C4 excess Tor.

At the normalized ternary Segre point, decompose each one-site function
space as constants plus zero-sum contrasts.  The checker identifies all 56
excess conormal/Tor_1 modes of the two balanced C4 flattenings, verifies that
site-gauge quotient removes none of them, and constructs a quadratic excess
class detected by a single marked-word readout.  This is a geometric
counterguard only; it does not identify the excess class with physical
hafnian-source H_1.
"""

from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_torus_c4_segre_derived_diagonal_interface.py":
        "89c63c525595e8ab090b6055ba40f5a6d98b20846f8eefadd63b83754a52da5d",
    "notes/torus-c4-segre-derived-diagonal-interface.md":
        "a73da619de52890b86f5ac0a70a15ac7eeb6a5e3ff916a4d39807c1522c10d57",
    "computations/verify_local_c4_relative_coherence_curvature_square.py":
        "9753c669db38b29e55706d4d8865c3beb46dcb0835298a90061babcda6483744",
    "notes/local-c4-coherence-curvature-relative-square.md":
        "5ed2232758948b993826d69158f6cdb57a06c077ad3a37af7db3a5005d9b9b43",
    "computations/verify_h3_rootless_non_euler_diagonal_stabilizer_jet.py":
        "0bbed406d393543b6badf222ff0665dc1b12445a2360a015e5398bd538bd5e5c",
    "notes/h3-rootless-non-euler-diagonal-stabilizer-jet.md":
        "0a2321191cdd29dc21aed0c988e76d710e09a993303780527ca1502f4d833dc4",
    "computations/verify_n8_chart26_c4_primitive_colon.py":
        "549d66f4405fe0492893b42d235baecade27d04d882eda583b65b646f38a078b",
}
EXPECTED_LEDGER_SHA256 = (
    "7c3e8e99d74e41a344564b0dc064c6391a9bb5e30e55e2beb86b377aebe9f0c1"
)


SITES = (0, 1, 4, 5)
A_BLOCKS = (frozenset((0, 1)), frozenset((4, 5)))
B_BLOCKS = (frozenset((0, 5)), frozenset((1, 4)))
COLOURS = range(3)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def file_sha256(path):
    return sha256(path.read_bytes()).hexdigest()


def rank(matrix):
    work = [[Q(entry) for entry in row] for row in matrix]
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next((row for row in range(pivot_row, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [entry / pivot_value
                           for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            multiplier = work[row][column]
            work[row] = [entry - multiplier * pivot_entry
                         for entry, pivot_entry
                         in zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def table_incidence(blocks):
    words = tuple(product(COLOURS, repeat=4))
    rows = []
    for block in blocks:
        positions = tuple(SITES.index(site) for site in sorted(block))
        for values in product(COLOURS, repeat=len(positions)):
            rows.append(tuple(
                int(tuple(word[position] for position in positions) == values)
                for word in words
            ))
    return rows


def site_incidence():
    words = tuple(product(COLOURS, repeat=4))
    rows = []
    for position in range(4):
        for colour in COLOURS:
            rows.append(tuple(int(word[position] == colour) for word in words))
    return rows


def qualifying_support(subset):
    """A contrast support is conormal to both balanced Segre tangents."""
    return (all(not subset <= block for block in A_BLOCKS)
            and all(not subset <= block for block in B_BLOCKS))


def audit_decomposition():
    sectors = []
    dimensions = {}
    for mask in range(1 << len(SITES)):
        subset = frozenset(
            site for index, site in enumerate(SITES) if mask & (1 << index)
        )
        if not qualifying_support(subset):
            continue
        dimension = 2 ** len(subset)  # dim zero-sum contrasts = 2 per site
        dimensions[len(subset)] = dimensions.get(len(subset), 0) + dimension
        sectors.append({
            "sites": sorted(subset),
            "degree": len(subset),
            "dimension": dimension,
        })
    require(dimensions == {2: 8, 3: 32, 4: 16},
            f"the C4 excess-sector decomposition changed: {dimensions}")
    require(sum(dimensions.values()) == 56,
            "the excess sectors stopped summing to rank 56")

    tangent_a = table_incidence(A_BLOCKS)
    tangent_b = table_incidence(B_BLOCKS)
    gauge = site_incidence()
    rank_a = rank(tangent_a)
    rank_b = rank(tangent_b)
    rank_gauge = rank(gauge)
    rank_sum = rank(tangent_a + tangent_b)
    require((rank_a, rank_b, rank_gauge, rank_sum) == (17, 17, 9, 25),
            "the tangent/site-gauge ranks changed")
    require(81 - rank_sum == 56,
            "the excess conormal stopped having rank 56")
    require(rank(tangent_a + gauge) == rank_a
            and rank(tangent_b + gauge) == rank_b,
            "site gauge left a balanced Segre tangent")
    return {
        "site_gauge_rank": rank_gauge,
        "balanced_tangent_ranks": [rank_a, rank_b],
        "balanced_tangent_sum_rank": rank_sum,
        "excess_rank_after_site_gauge_quotient": 56,
        "sectors": sectors,
        "degree_dimensions": dimensions,
    }


def audit_detected_class():
    # theta=(1,-1,0)_0 tensor 1_1 tensor (1,-1,0)_4 tensor 1_5.
    # It is the smallest {0,4} third-matching excess sector.
    contrast = (1, -1, 0)
    theta = {}
    for i, j, k, ell in product(COLOURS, repeat=4):
        theta[(i, j, k, ell)] = contrast[i] * contrast[k]

    def marginal(fixed_positions, fixed_values):
        return sum(value for word, value in theta.items()
                   if all(word[position] == colour
                          for position, colour
                          in zip(fixed_positions, fixed_values, strict=True)))

    # Orthogonality to the (01)|(45) and (05)|(14) tangent tables.
    for positions in ((0, 1), (2, 3), (0, 3), (1, 2)):
        for values in product(COLOURS, repeat=2):
            require(marginal(positions, values) == 0,
                    "the quadratic excess class acquired a balanced marginal")

    # Site gauge is contained in either tangent; verify directly as well.
    for position in range(4):
        for colour in COLOURS:
            require(marginal((position,), (colour,)) == 0,
                    "the excess class stopped annihilating site gauge")

    total_augmentation = sum(theta.values())
    marked_word = (0, 0, 0, 0)
    marked_readout = theta[marked_word]
    require(total_augmentation == 0,
            "the scalar/full-word augmentation stopped killing excess")
    require(marked_readout == 1,
            "the marked coordinate stopped detecting excess")
    return {
        "class": "(e0-e1)_0 tensor 1_1 tensor (e0-e1)_4 tensor 1_5",
        "sector": [0, 4],
        "balanced_pair_marginals": 0,
        "site_gauge_marginals": 0,
        "full_scalar_augmentation": total_augmentation,
        "marked_word": list(marked_word),
        "marked_word_readout": marked_readout,
    }


def main():
    for relative, expected in PINS.items():
        actual = file_sha256(ROOT / relative)
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")

    ledger = {
        "excess_decomposition": audit_decomposition(),
        "detected_quadratic_class": audit_detected_class(),
        "invisibility_criterion": (
            "a linear terminal readout kills geometric excess iff its "
            "representative lies in the sum of the two balanced tangents"
        ),
        "positive_special_case": (
            "the full scalar/all-word augmentation is balanced-additive "
            "and kills all geometric excess classes"
        ),
        "negative_general_case": (
            "site-gauge quotient alone does not kill excess, and a marked "
            "word readout detects an explicit quadratic class"
        ),
        "source_scope": (
            "geometric Segre Tor only: no canonical map to physical "
            "hafnian-source H1 or the rootless pentagon h_v is asserted"
        ),
        "rootless_consequence": (
            "the non-Euler marked h_v descent still needs a source-labelled "
            "terminal map proving epsilon(H1_source)=0; vertex gauge cannot "
            "supply zero indeterminacy automatically"
        ),
        "primitive_source_guard": (
            "the pinned chart26 primitive-colon H1 remains separate; its "
            "terminal pairing is not computed by this geometric model"
        ),
        "pins": PINS,
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"C4 excess/readout ledger changed: {digest}")
    print("C4 excess Tor terminal-readout boundary: PASS")
    print(json.dumps(ledger, sort_keys=True))
    print("sha256:", digest)


if __name__ == "__main__":
    main()
