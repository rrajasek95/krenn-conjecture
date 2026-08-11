#!/usr/bin/env python3
"""Verify the exact 4+4 cut ledger behind a four-site zero-Fitting core.

For S|T with |S|=|T|=4, every K8 perfect matching has 0, 2, or 4
crossing edges.  The three sectors have sizes 9, 72, and 24.  If the three
K4 matching monomials on S are U,V,W and a localized zero-Fitting block
gives U+V=0, then every endpoint-colour coefficient satisfies

    P_w == W*H_T + C2_w + C4_w       modulo (U+V).

Thus the obstruction to the missing third K4 route is exactly the literal
two-cross plus four-cross debt.  The audit is repeated for all 3^8 output
words, retaining endpoint colours on every physical cell.

The checker also records an essential scope boundary.  In product-cap
notation the physical two-cross top sector is [x*C2]_4, not the boundary
tensor C2 itself.  Moreover the compact four-star expansion

    C2_ij = a_(complement ij) L_i L_j

is an additional factorized-signature hypothesis; it is not implied by a
zero-Fitting core relation.  An exact dense rational counterguard satisfies
U+V=0 but violates the three necessary factorization ratios.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import combinations, permutations, product
import json
from pathlib import Path


EXPECTED_DIGEST = "d101d2fa74e708d1ec8d838c72d68e5b2dae25489596389a4bf9898bde218f32"
SITES = tuple(range(8))
LEFT = (0, 1, 2, 3)
RIGHT = (4, 5, 6, 7)
COLOURS = (0, 1, 2)
ROOT = Path(__file__).resolve().parents[1]
ONE_BAD_CHECKER = (
    "computations/verify_n8_multisite_permanent_null_repeated_defect.py"
)
ONE_BAD_CHECKER_SHA256 = (
    "ddc9f38fd5e0044922642f2ecb8f76a6780e6b27dd2aaf60c045974105694d8b"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge(u, v):
    return tuple(sorted((u, v)))


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for second in vertices[1:]:
        rest = tuple(x for x in vertices if x not in (first, second))
        for tail in perfect_matchings(rest):
            answer.append(tuple(sorted((edge(first, second),) + tail)))
    return tuple(answer)


def cell(physical_edge, word):
    u, v = physical_edge
    return (u, v, word[u], word[v])


def monomial(matching, word):
    return tuple(sorted(cell(item, word) for item in matching))


def matching_poly(matchings, word):
    return Counter({monomial(item, word): 1 for item in matchings})


def add(*polys):
    answer = Counter()
    for poly in polys:
        answer.update(poly)
    return +answer


def subtract(left, right):
    answer = Counter(left)
    answer.subtract(right)
    require(all(value >= 0 for value in answer.values()),
            "polynomial subtraction acquired a negative coefficient")
    return +answer


def multiply(left, right):
    answer = Counter()
    for first, first_value in left.items():
        for second, second_value in right.items():
            answer[tuple(sorted(first + second))] += first_value * second_value
    return +answer


def two_cross_matchings():
    answer = []
    for left_internal in combinations(LEFT, 2):
        left_rest = tuple(x for x in LEFT if x not in left_internal)
        for right_internal in combinations(RIGHT, 2):
            right_rest = tuple(x for x in RIGHT if x not in right_internal)
            for image in (right_rest, tuple(reversed(right_rest))):
                answer.append(tuple(sorted((
                    edge(*left_internal),
                    edge(*right_internal),
                    edge(left_rest[0], image[0]),
                    edge(left_rest[1], image[1]),
                ))))
    return tuple(answer)


def four_cross_matchings():
    return tuple(
        tuple(sorted(edge(left, right) for left, right in zip(LEFT, image)))
        for image in permutations(RIGHT)
    )


def matching_ledger():
    all_matchings = perfect_matchings(SITES)
    by_crossing = Counter()
    for matching in all_matchings:
        crossings = sum((u in LEFT) != (v in LEFT) for u, v in matching)
        by_crossing[crossings] += 1
    require(by_crossing == Counter({0: 9, 2: 72, 4: 24}),
            ("4+4 crossing census", by_crossing))

    zero_cross = tuple(
        tuple(sorted(left + right))
        for left in perfect_matchings(LEFT)
        for right in perfect_matchings(RIGHT)
    )
    two_cross = two_cross_matchings()
    four_cross = four_cross_matchings()
    require(len(set(zero_cross)) == 9, "zero-cross list changed")
    require(len(set(two_cross)) == 72, "two-cross list changed")
    require(len(set(four_cross)) == 24, "four-cross list changed")
    require(set(all_matchings) == set(zero_cross + two_cross + four_cross),
            "explicit crossing sectors do not partition all K8 matchings")
    return all_matchings, zero_cross, two_cross, four_cross


def word_audit(sectors):
    all_matchings, zero_cross, two_cross, four_cross = sectors
    left_matchings = perfect_matchings(LEFT)
    right_matchings = perfect_matchings(RIGHT)
    U, V, W = left_matchings
    word_count = 0
    identity_terms = Counter()

    for word in product(COLOURS, repeat=8):
        full = matching_poly(all_matchings, word)
        zero = matching_poly(zero_cross, word)
        cross_two = matching_poly(two_cross, word)
        cross_four = matching_poly(four_cross, word)
        require(full == add(zero, cross_two, cross_four),
                ("decorated 0/2/4 cut decomposition", word))

        left_hafnian = matching_poly(left_matchings, word)
        right_hafnian = matching_poly(right_matchings, word)
        require(zero == multiply(left_hafnian, right_hafnian),
                ("uncrossed sector stopped factoring", word))

        relation = matching_poly((U, V), word)
        missing_route = matching_poly((W,), word)
        relation_times_right = multiply(relation, right_hafnian)
        residual = subtract(full, relation_times_right)
        expected = add(
            multiply(missing_route, right_hafnian),
            cross_two,
            cross_four,
        )
        require(residual == expected,
                ("localized opposite-route/cross-debt identity", word))
        identity_terms["relation_times_spectator"] += sum(
            relation_times_right.values())
        identity_terms["missing_route_times_spectator"] += sum(
            multiply(missing_route, right_hafnian).values())
        identity_terms["two_cross"] += sum(cross_two.values())
        identity_terms["four_cross"] += sum(cross_four.values())
        word_count += 1

    require(word_count == 6561, "endpoint-colour word count changed")
    require(identity_terms == Counter({
        "relation_times_spectator": 6 * 6561,
        "missing_route_times_spectator": 3 * 6561,
        "two_cross": 72 * 6561,
        "four_cross": 24 * 6561,
    }), ("aggregate term ledger", identity_terms))
    return {
        "endpoint_colour_words": word_count,
        "aggregate_terms": dict(sorted(identity_terms.items())),
    }


def normalize_formal_product(atoms):
    """Rewrite L_i^2 as 2 L_i^[2] in the square-free site algebra."""
    counts = Counter(atoms)
    coefficient = Fraction(1)
    output = []
    for atom, count in sorted(counts.items()):
        if atom.startswith("L"):
            require(count <= 2, ("unexpected star multiplicity", atom, count))
            if count == 2:
                coefficient *= 2
                output.append(f"{atom}^[2]")
            else:
                output.append(atom)
        else:
            output.extend((atom,) * count)
    return tuple(sorted(output)), coefficient


def load_committed_one_bad_checker():
    path = ROOT / ONE_BAD_CHECKER
    require(sha256(path.read_bytes()).hexdigest() == ONE_BAD_CHECKER_SHA256,
            "committed one-bad defect checker changed")
    specification = importlib.util.spec_from_file_location(
        "committed_one_bad_repeated_defect", path
    )
    require(specification is not None and specification.loader is not None,
            "cannot load committed one-bad defect checker")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def repeated_endpoint_cumulant_audit():
    # Q_ij is the two-cross response on spectator sites i,j.  Its coefficient
    # is the internal edge on the complementary core pair times L_i L_j.
    components = (
        ("a23", "L0", "L1"),
        ("a13", "L0", "L2"),
        ("a12", "L0", "L3"),
        ("a03", "L1", "L2"),
        ("a02", "L1", "L3"),
        ("a01", "L2", "L3"),
    )
    q_divided_square = Counter()
    for first, left in enumerate(components):
        for second in range(first, len(components)):
            right = components[second]
            scalar = Fraction(1, 2) if first == second else Fraction(1)
            term, normalization = normalize_formal_product(left + right)
            q_divided_square[term] += scalar * normalization

    four_cross = ("L0", "L1", "L2", "L3")
    h_times_four_cross = Counter({
        tuple(sorted(("a01", "a23") + four_cross)): Fraction(1),
        tuple(sorted(("a02", "a13") + four_cross)): Fraction(1),
        tuple(sorted(("a03", "a12") + four_cross)): Fraction(1),
    })
    error = Counter(h_times_four_cross)
    error.subtract(q_divided_square)
    error = Counter({term: coefficient for term, coefficient in error.items()
                     if coefficient})
    require(len(error) == 18, ("repeated-endpoint term count", len(error)))
    require(set(error.values()) == {Fraction(-2)},
            ("repeated-endpoint coefficients", set(error.values())))
    square_histogram = Counter()
    for term in error:
        square_count = sum(atom.endswith("^[2]") for atom in term)
        require(square_count in (1, 2),
                ("cumulant term lacks a star self-square", term))
        square_histogram[square_count] += 1
    require(square_histogram == Counter({1: 12, 2: 6}),
            ("self-square factor census", square_histogram))

    # Setting all four star self-squares to zero annihilates the complete
    # error, exactly the square-zero clean-cap sufficient condition.
    specialized = {
        term: coefficient for term, coefficient in error.items()
        if not any(atom.endswith("^[2]") for atom in term)
    }
    require(not specialized, "square-zero specialization left a cumulant")

    # The permanent-null binary one-bad cap is the h=0 boundary of this
    # same numerator.  Put (L0,L1,L2,L3)=(p0,p1,s0,s1) and specialize the
    # six internal coefficients so that
    #
    #   Q = L0*L2 + L0*L3 - L1*L2 + L1*L3.
    #
    # Equivalently, the binary coefficient matrix is [[1,1],[-1,1]].
    # Its permanent h=a01*a23+a02*a13+a03*a12 is zero.  The specialization
    # of h*C4-Q^[2] must therefore be exactly the negative of the eight
    # repeated-label sectors of Q^[2].
    internal_values = {
        "a23": Fraction(0),
        "a13": Fraction(1),
        "a12": Fraction(1),
        "a03": Fraction(-1),
        "a02": Fraction(1),
        "a01": Fraction(0),
    }
    h_value = (
        internal_values["a01"] * internal_values["a23"]
        + internal_values["a02"] * internal_values["a13"]
        + internal_values["a03"] * internal_values["a12"]
    )
    require(h_value == 0, ("permanent-null specialization", h_value))

    specialized_error = Counter()
    for term, coefficient in error.items():
        value = coefficient
        star_atoms = []
        for atom in term:
            if atom in internal_values:
                value *= internal_values[atom]
            else:
                star_atoms.append(atom)
        if value:
            specialized_error[tuple(sorted(star_atoms))] += value
    specialized_error = Counter({
        term: coefficient
        for term, coefficient in specialized_error.items()
        if coefficient
    })

    q_divided_square_specialized = Counter({
        tuple(sorted(("L0^[2]", "L2^[2]"))): Fraction(2),
        tuple(sorted(("L0^[2]", "L3^[2]"))): Fraction(2),
        tuple(sorted(("L1^[2]", "L2^[2]"))): Fraction(2),
        tuple(sorted(("L1^[2]", "L3^[2]"))): Fraction(2),
        tuple(sorted(("L0^[2]", "L2", "L3"))): Fraction(2),
        tuple(sorted(("L1^[2]", "L2", "L3"))): Fraction(-2),
        tuple(sorted(("L0", "L1", "L2^[2]"))): Fraction(-2),
        tuple(sorted(("L0", "L1", "L3^[2]"))): Fraction(2),
    })

    # Reconstruct the same polynomial from the independent committed
    # row/column-provenance checker.  Its coefficients are on raw products
    # p_i p_k s_j s_l; normalize them into divided powers before comparing.
    one_bad = load_committed_one_bad_checker()
    independent_raw, _ = one_bad.formal_divided_square()
    independent_divided = Counter()
    for ((i, k), (j, l)), coefficient in independent_raw.items():
        term, normalization = normalize_formal_product((
            f"L{i}", f"L{k}", f"L{2 + j}", f"L{2 + l}",
        ))
        independent_divided[term] += coefficient * normalization
    independent_divided = Counter({
        term: coefficient
        for term, coefficient in independent_divided.items()
        if coefficient
    })
    require(independent_divided == q_divided_square_specialized,
            ("independent one-bad divided-power comparison",
             independent_divided))
    require(
        specialized_error
        == Counter({term: -coefficient
                    for term, coefficient
                    in q_divided_square_specialized.items()}),
        ("permanent-null fourth-cumulant boundary", specialized_error),
    )
    sector_histogram = Counter()
    for term in q_divided_square_specialized:
        square_positions = tuple(
            atom[1] for atom in term if atom.endswith("^[2]")
        )
        if len(square_positions) == 2:
            sector_histogram["same_entry"] += 1
        elif square_positions[0] in ("0", "1"):
            sector_histogram["repeated_row"] += 1
        else:
            sector_histogram["repeated_column"] += 1
    require(sector_histogram == Counter({
        "same_entry": 4,
        "repeated_row": 2,
        "repeated_column": 2,
    }), ("permanent-null repeated-label sectors", sector_histogram))

    return {
        "scope": (
            "factorized four-star boundary signature; not implied by the "
            "arbitrary physical 4+4 cut or by U+V=0"
        ),
        "formula": "h*C4-Q^[2]=h^2*L4",
        "nonzero_terms": len(error),
        "coefficient_on_every_term": "-2",
        "star_self_square_factor_histogram": {
            str(key): value for key, value in sorted(square_histogram.items())
        },
        "membership": "h^2*L4 lies in (L0^[2],L1^[2],L2^[2],L3^[2])",
        "square_zero_specialization": "0",
        "permanent_null_specialization": {
            "binary_matrix": "[[1,1],[-1,1]]",
            "h": 0,
            "Q": "L0*L2+L0*L3-L1*L2+L1*L3",
            "identity": "(h*C4-Q^[2])|_(Q=R,h=0) = -R^[2]",
            "surviving_repeated_label_terms": len(specialized_error),
            "sector_histogram": dict(sorted(sector_histogram.items())),
            "independent_checker": ONE_BAD_CHECKER,
            "independent_checker_sha256": ONE_BAD_CHECKER_SHA256,
        },
    }


def permanent(matrix):
    size = len(matrix)
    return sum(
        __import__("math").prod(matrix[row][image[row]]
                                for row in range(size))
        for image in permutations(range(size))
    )


def physical_nonfactorization_counterguard():
    """Build a literal scalar signature outside the four-star ansatz.

    The core has matching products U=1, V=-1, W=6, so U+V=0.  If its
    physical two-boundary signature satisfied

        Q_ij = a_(complement ij) L_i L_j,

    then the three complementary products divided by the corresponding
    core matching products would all equal L0*L1*L2*L3.  Cross
    multiplication shows that none of the three required equalities holds.
    """
    core = {
        (0, 1): 1,
        (2, 3): 1,
        (0, 2): 1,
        (1, 3): -1,
        (0, 3): 2,
        (1, 2): 3,
    }

    def a(u, v):
        return core[tuple(sorted((u, v)))]

    cross = (
        (1, 2, 1, 3),
        (2, 1, 3, 1),
        (1, 3, 2, 4),
        (3, 1, 4, 2),
    )
    U = a(0, 1) * a(2, 3)
    V = a(0, 2) * a(1, 3)
    W = a(0, 3) * a(1, 2)
    require((U, V, W) == (1, -1, 6) and U + V == 0,
            "zero-Fitting core counterguard changed")
    h = U + V + W

    q = {}
    for i, j in combinations(range(4), 2):
        value = 0
        for u, v in permutations(range(4), 2):
            remainder = tuple(x for x in range(4) if x not in (u, v))
            value += cross[i][u] * cross[j][v] * a(*remainder)
        q[i, j] = value
    require(q == {
        (0, 1): 50,
        (0, 2): 64,
        (0, 3): 72,
        (1, 2): 70,
        (1, 3): 36,
        (2, 3): 100,
    }, ("physical C2 signature", q))
    c4 = permanent(cross)
    q2 = (
        q[0, 1] * q[2, 3]
        + q[0, 2] * q[1, 3]
        + q[0, 3] * q[1, 2]
    )
    numerator = h * c4 - q2
    require((h, c4, q2, numerator) == (6, 496, 12344, -9368),
            ("physical cumulant counterguard", h, c4, q2, numerator))

    normalized_products = (
        (q[0, 1] * q[2, 3], a(2, 3) * a(0, 1)),
        (q[0, 2] * q[1, 3], a(1, 3) * a(0, 2)),
        (q[0, 3] * q[1, 2], a(1, 2) * a(0, 3)),
    )
    equalities = []
    for first, second in combinations(normalized_products, 2):
        equalities.append(first[0] * second[1]
                          == second[0] * first[1])
    require(equalities == [False, False, False],
            ("factorized-star counterguard", equalities))
    return {
        "core_matching_products": [U, V, W],
        "zero_Fitting_relation": "U+V=0",
        "dense_cross_matrix": [list(row) for row in cross],
        "physical_C2_entries": {
            f"{i}{j}": value for (i, j), value in sorted(q.items())
        },
        "C0_h": h,
        "C4": c4,
        "C2_divided_square": q2,
        "hC4_minus_C2_divided_square": numerator,
        "factorized_signature_possible_with_same_core_coefficients": False,
        "failed_normalized_product_equalities": len(equalities),
    }


def main():
    sectors = matching_ledger()
    ledger = {
        "cut": {"left": list(LEFT), "right": list(RIGHT)},
        "physical_matching_sectors": {"zero_cross": 9,
                                      "two_cross": 72,
                                      "four_cross": 24},
        "two_cross_grouping": "36 internal-edge pairs times a 2x2 cross permanent",
        "four_cross_grouping": "one 4x4 cross permanent with 24 terms",
        "decorated_audit": word_audit(sectors),
        "fourth_cumulant": repeated_endpoint_cumulant_audit(),
        "physical_nonfactorization_counterguard": (
            physical_nonfactorization_counterguard()
        ),
        "localized_identity": (
            "P_w = W_w*H_T + C2_w + C4_w modulo (U_w+V_w)"
        ),
        "source_interpretation": (
            "for F_w=P_w-delta_w, the missing third K4 route equals "
            "delta_w minus the literal 2/4-cross debt after spectator localization"
        ),
        "scope": (
            "the checker identifies the complete physical contamination module; "
            "the compact 18-term self-square factorization is conditional and "
            "is not implied by the zero-Fitting relation"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST, ("ledger digest", digest))
    print("OO four-site core cross-debt decomposition: PASS")
    print("K8 cut sectors: 9 zero-cross + 72 two-cross + 24 four-cross")
    print("all 6561 endpoint-colour words audited")
    print("sha256:", digest)


if __name__ == "__main__":
    main()
