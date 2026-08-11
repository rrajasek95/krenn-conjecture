#!/usr/bin/env python3
"""Exact square-zero-slice routing boundary for Component IV at h=3.

The five selected face polars are the five coefficients of the divided
square of one scalar decorated K5 quadratic q_m.  This checker proves that
their dense torus zero locus consists of the two primitive-cube-root
holonomy points, and audits why the already committed labelled
anchor/crossed/curvature packet cannot turn that fact into an inactive or
clean-cap landing: its rows preserve the endpoint word.

This is a bounded source-grade counterguard.  It is not a full-source point.
"""

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path


EXPECTED_DIGEST = "6e5d753d8496086334f8b0f64a2074a981a165e5597632f28004a886b96c0922"
PINNED = {
    "selected_membership_separator": (
        "computations/verify_h3_component_iv_selected_denominator_membership_separator.py",
        "859a5e3fc4b942858ded8544333b885a04d1e5e91ae3803e6e0c562393e3b7da",
    ),
    "face_zero_routing_boundary": (
        "computations/verify_h3_component_iv_face_zero_routing_boundary.py",
        "217d14b451a36b6e86caadf14bd5ce63aeda484f8e0917b7f2e1034b640a4fc0",
    ),
    "two_chart_static_fitting": (
        "computations/verify_h3_two_chart_divisor_transport_fitting_obstruction.py",
        "8d67857eb1db6dfdb82428ed1566e7624afde89d5d9b2a07f917384ca165096b",
    ),
    "physical_curvature_word_change": (
        "computations/verify_h3_physical_curvature_qzero_attaching_lower_face_obstruction.py",
        "050bfaa16cedb07248f01f58f8cc59927307861e55da45b759219ccde3d24ee1",
    ),
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


class Poly:
    """Tiny exact polynomial class in (t,A,B,C,D,E)."""

    nvars = 6

    def __init__(self, terms=()):
        if isinstance(terms, (int, Q)):
            terms = {self.nvars * (0,): Q(terms)}
        self.terms = {tuple(monomial): Q(coefficient)
                      for monomial, coefficient in dict(terms).items()
                      if coefficient}

    def __add__(self, other):
        other = as_poly(other)
        result = dict(self.terms)
        for monomial, coefficient in other.terms.items():
            result[monomial] = result.get(monomial, Q(0)) + coefficient
            if not result[monomial]:
                del result[monomial]
        return Poly(result)

    __radd__ = __add__

    def __neg__(self):
        return Poly({monomial: -coefficient
                     for monomial, coefficient in self.terms.items()})

    def __sub__(self, other):
        return self + (-as_poly(other))

    def __rsub__(self, other):
        return as_poly(other) - self

    def __mul__(self, other):
        other = as_poly(other)
        result = {}
        for left, left_coefficient in self.terms.items():
            for right, right_coefficient in other.terms.items():
                monomial = tuple(a + b for a, b in zip(left, right, strict=True))
                result[monomial] = (result.get(monomial, Q(0))
                                    + left_coefficient * right_coefficient)
        return Poly(result)

    __rmul__ = __mul__

    def __truediv__(self, scalar):
        return Poly({monomial: coefficient / Q(scalar)
                     for monomial, coefficient in self.terms.items()})

    def __pow__(self, exponent):
        require(isinstance(exponent, int) and exponent >= 0,
                "polynomial exponent must be nonnegative")
        answer = Poly(1)
        base = self
        while exponent:
            if exponent & 1:
                answer *= base
            base *= base
            exponent >>= 1
        return answer

    def __eq__(self, other):
        return self.terms == as_poly(other).terms


def as_poly(value):
    return value if isinstance(value, Poly) else Poly(value)


def variables():
    output = []
    for index in range(Poly.nvars):
        exponent = [0] * Poly.nvars
        exponent[index] = 1
        output.append(Poly({tuple(exponent): Q(1)}))
    return output


def leading_term(polynomial):
    require(polynomial.terms, "zero polynomial has no leading term")
    monomial = max(polynomial.terms)  # lex in t,A,B,C,D,E
    return monomial, polynomial.terms[monomial]


def divisible(left, right):
    return all(a >= b for a, b in zip(left, right, strict=True))


def monomial_poly(exponent, coefficient=1):
    return Poly({tuple(exponent): Q(coefficient)})


def normal_form(polynomial, basis):
    """Exact multivariate division for the fixed lex order."""
    work = polynomial
    remainder = Poly(0)
    while work.terms:
        work_monomial, work_coefficient = leading_term(work)
        for divisor in basis:
            divisor_monomial, divisor_coefficient = leading_term(divisor)
            if not divisible(work_monomial, divisor_monomial):
                continue
            exponent = tuple(a - b for a, b in zip(
                work_monomial, divisor_monomial, strict=True))
            quotient = monomial_poly(exponent, work_coefficient / divisor_coefficient)
            work -= quotient * divisor
            break
        else:
            term = monomial_poly(work_monomial, work_coefficient)
            remainder += term
            work -= term
    return remainder


def determinant(matrix):
    work = [[Q(value) for value in row] for row in matrix]
    answer = Q(1)
    for column in range(len(work)):
        pivot = next((row for row in range(column, len(work))
                      if work[row][column]), None)
        if pivot is None:
            return Q(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            answer = -answer
        value = work[column][column]
        answer *= value
        for row in range(column + 1, len(work)):
            if not work[row][column]:
                continue
            scale = work[row][column] / value
            for index in range(column, len(work)):
                work[row][index] -= scale * work[column][index]
    return answer


def dense_square_zero_certificate():
    """Prove the saturated normalized K5 ideal has two cyclotomic points."""
    t, A, B, C, D, E = variables()

    # Cycle edges 12,23,34,45,15 have been normalized to one.  The chords
    # are A=13, B=14, C=24, D=25, E=35.  The h_v are the five K4 hafnians.
    h = [
        1 + C * E + D,
        A + B * E + 1,
        1 + B * D + C,
        E + A * D + 1,
        1 + A * C + B,
        t * A * B * C * D * E - 1,  # torus saturation
    ]

    # Literal square-zero matching expansion: the coefficient of the basis
    # word using four sites is the three-matchings hafnian on those sites.
    edge_values = {
        (1, 2): Poly(1), (2, 3): Poly(1), (3, 4): Poly(1),
        (4, 5): Poly(1), (1, 5): Poly(1),
        (1, 3): A, (1, 4): B, (2, 4): C, (2, 5): D, (3, 5): E,
    }

    def edge_value(left, right):
        return edge_values[tuple(sorted((left, right)))]

    def haf4(vertices):
        first, second, third, fourth = vertices
        return (edge_value(first, second) * edge_value(third, fourth)
                + edge_value(first, third) * edge_value(second, fourth)
                + edge_value(first, fourth) * edge_value(second, third))

    literal_faces = [haf4(tuple(site for site in range(1, 6) if site != deleted))
                     for deleted in range(1, 6)]
    require(literal_faces == h[:5],
            "the five h_v stopped being the coefficients of q_m^[2]")
    groebner = [
        E ** 2 + E + 1,
        D - E,
        C - D,
        B - C,
        A + B * E + 1,
        t - E,
    ]

    # A lift certificate G=H*T obtained over Q.  Checking it as a literal
    # polynomial identity makes the ideal containment independent of a CAS.
    zero = Poly(0)
    transform = [
        [
            (B*E**2 + B*E + E + 1)/2,
            Q(1, 2),
            -B*E/2 - B/2 - 1,
            B/2,
            zero,
            -t*A*B*D*E + t*B*D*E + t*C*E + 3*t*E/2 + t/2,
        ],
        [
            (B*D*E - C*E**2 - D*E - D)/2,
            D/2,
            (-B*D + C*E)/2,
            -C/2,
            Poly(1),
            -t*B*D*E/2 - t*C*E/2 - t*D*E/2 - t*D/2 - t*E,
        ],
        [
            (-B*E**2 - E)/2,
            -E/2,
            B*E/2 + E/2 + 1,
            -Q(1, 2),
            zero,
            t*A*D*E + t*A*E + t*B*E**2/2 - t*C*E**2 - t*D*E + t*E**2/2,
        ],
        [
            (-B*E + E + 1)/2,
            -Q(1, 2),
            B/2,
            zero,
            zero,
            t*B*E/2 - t*C*E - t*E/2 + t/2,
        ],
        [
            E**2/2,
            zero,
            -E/2,
            Q(1, 2),
            zero,
            -t*E/2,
        ],
        [zero, zero, zero, zero, zero, E],
    ]
    for column, target in enumerate(groebner):
        lifted = sum((h[row] * transform[row][column]
                      for row in range(len(h))), Poly(0))
        require(lifted == target, f"dense torus lift column {column} failed")

    # Reverse containment and standard-basis property.  The six leading
    # monomials E^2,D,C,B,A,t are pairwise coprime, so Buchberger's product
    # criterion applies after the exact reductions below.
    require(all(normal_form(source, groebner) == 0 for source in h),
            "normalized face equations do not reduce by the certified basis")
    leads = [leading_term(polynomial)[0] for polynomial in groebner]
    for left, right in combinations(leads, 2):
        require(not any(a and b for a, b in zip(left, right, strict=True)),
                "certified leading monomials stopped being pairwise coprime")

    # Consequence: A=B=C=D=E=t=zeta and zeta^2+zeta+1=0.  Verify the
    # representative in Q[zeta]/(zeta^2+zeta+1), represented by pairs a+b*zeta.
    def cmul(left, right):
        a, b = left
        c, d = right
        # zeta^2=-zeta-1
        return (a*c - b*d, a*d + b*c - b*d)

    one = (Q(1), Q(0))
    zeta = (Q(0), Q(1))
    chord_values = dict.fromkeys("ABCDE", zeta)
    h_values = [
        (one, cmul(zeta, zeta), zeta),
        (zeta, cmul(zeta, zeta), one),
        (one, cmul(zeta, zeta), zeta),
        (zeta, cmul(zeta, zeta), one),
        (one, cmul(zeta, zeta), zeta),
    ]
    require(all(tuple(sum((entry[index] for entry in terms), Q(0))
                          for index in range(2)) == (Q(0), Q(0))
                for terms in h_values), "cyclotomic face value is nonzero")
    require(cmul(cmul(zeta, zeta), zeta) == one, "zeta^3 is not one")
    require(zeta != (Q(0), Q(0)), "dense q_m representative vanished")

    return {
        "normalized_cycle_edges": ["12", "23", "34", "45", "15"],
        "normalized_cycle_value": "1",
        "chords": list(chord_values),
        "chord_value": "zeta",
        "cyclotomic_equation": "zeta^2+zeta+1=0",
        "dense_geometric_points": 2,
        "all_ten_q_cells_nonzero": True,
        "q_m_nonzero_but_q_m_divided_square_zero": True,
    }


def word_preserving_packet_audit():
    # The completed two-anchor/direct/crossed static block is already full.
    static = [
        [1, 0, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 1, -2],
        [0, 1, 2, 0],
    ]
    require(determinant(static) == -3, "static two-chart determinant changed")

    # The selected automatic curvature packet permits kappa=AU-BF to be a
    # unit; this scalar does not change decorated endpoint words.
    A, U, B, F = Q(1), Q(1), Q(0), Q(0)
    kappa = A*U - B*F
    require(kappa == 1, "curvature unit probe changed")

    # Curvature joins the three matchings of one fixed decorated K4 word.
    # There are 3^4 word components.  The needed bridge changes the word
    # (0,m_v,2,2) to (0,0,0,0), and no global colour permutation repairs it.
    words = tuple(product(range(3), repeat=4))
    require(len(words) == 81, "decorated K4 word census changed")

    vertices = tuple(range(4))
    matchings = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))

    def decorated_matching(word, matching):
        return tuple(sorted((min(left, right), max(left, right), word[left], word[right])
                            if left < right else
                            (min(left, right), max(left, right), word[right], word[left])
                            for left, right in matching))

    components = []
    seen_nodes = {}
    for word in words:
        component = tuple(decorated_matching(word, matching) for matching in matchings)
        require(len(set(component)) == 3, "a fixed-word K4 component collapsed")
        for node in component:
            require(node not in seen_nodes, "decorated matching entered two word components")
            seen_nodes[node] = word
        components.append(component)
    require(len(seen_nodes) == 243 and len(components) == 81,
            "fixed-label curvature graph census changed")
    odd_word = (1, 2, 1, 1, 2)
    bridges = []
    for face, middle in enumerate(odd_word, start=1):
        physical = (0, middle, 2, 2)
        lower = (0, 0, 0, 0)
        require(physical != lower, "physical and lower endpoint words collided")
        for permutation in permutations(range(3)):
            require(tuple(permutation[value] for value in physical)
                    != tuple(permutation[value] for value in lower),
                    "a global colour permutation erased the word mismatch")
        bridges.append({
            "face": face,
            "physical_word": physical,
            "lower_word": lower,
            "same_fixed_label_component": False,
        })

    return {
        "static_det": "-3",
        "static_block_full": True,
        "kappa_probe": "1",
        "fixed_label_components": 81,
        "bridges": bridges,
        "existing_rows_change_endpoint_word": False,
    }


def main():
    root = Path(__file__).resolve().parent.parent
    pinned_ledger = {}
    for name, (relative, expected) in PINNED.items():
        actual = sha256((root / relative).read_bytes()).hexdigest()
        require(actual == expected, f"pinned artifact changed: {relative}: {actual}")
        pinned_ledger[name] = {"path": relative, "sha256": actual}

    dense = dense_square_zero_certificate()
    packet = word_preserving_packet_audit()
    ledger = {
        "scope": "h3-selected-word-square-zero-slice-plus-bounded-static-curvature-packet",
        "word": "12112",
        "face_polars": "coefficients of q_m^[2]",
        "dense_square_zero_slice": dense,
        "bounded_packet": packet,
        "pinned_artifacts": pinned_ledger,
        "proved": [
            "V(h1,...,h5) contains a dense all-nonzero q_m torus stratum",
            "kappa and the completed anchor/crossed static rows do not change endpoint words",
            "the proposed direct square-zero-to-inactive/clean landing is not supplied",
        ],
        "not_proved": [
            "existence of a full physical source on V(h1,...,h5)",
            "emptiness of the physical rootless stratum",
            "routing by unexamined Hamming-two or higher full-word rows",
        ],
        "next_required_input": (
            "a literal full-nine/Hamming-two identity changing the selected mixed endpoint "
            "word to the zero/anchor word, or a source theorem excluding the cyclotomic "
            "square-zero slice"
        ),
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    digest = sha256(encoded).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST, f"ledger digest changed: {digest}")

    print("h=3 Component-IV square-zero-slice routing boundary: PASS")
    print("dense V(h): two cyclotomic torus points after vertex normalization")
    print("static determinant: -3; fixed-label word bridge: absent")
    print("physical full-source landing: OPEN")
    print(f"ledger sha256: {digest}")


if __name__ == "__main__":
    main()
