#!/usr/bin/env python3
"""Classify the nondense five-site face-zero support strata exactly.

For the scalar decorated K5 slice q_m, h_v is the three-matching hafnian
on the four sites other than v.  This checker classifies every exact support
of q_m on which all five h_v can vanish with every supported edge nonzero.

The theorem is deliberately derived-level.  Full-rank strata admit the same
formal normal-face repair as the dense cyclotomic point.  No physical cap
comparison or source routing is inferred from the q-support classification.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_component_iv_square_zero_slice_routing_boundary.py":
        "6d41acd033a1c5eced5968a8deb780331f2ee93e21f8b85efcba840bf3664e08",
    "notes/h3-component-iv-square-zero-slice-routing-boundary.md":
        "a9c41b0c2a059a2470f7740ff9fff5e1270a11155e76198037c3bdaa6c0546e5",
    "computations/verify_h3_cyclotomic_regularized_shifted_filler_normal_face.py":
        "c409a62957dba0d101d1298ec16695482fce705d3131323a8d3657074f1bf2b0",
    "notes/h3-cyclotomic-regularized-shifted-filler-normal-face.md":
        "33d23d5f30afd8edc8b4e6f5599d027620587b600c87476a1adabf967820ea63",
    "computations/verify_h3_component_iv_cyclotomic_rees_lift_physical_separator.py":
        "12f7edba228a034523c61f10fc7633c7c736516dd3890ab3a89fce376eaa49bb",
    "notes/h3-component-iv-cyclotomic-rees-lift-physical-separator.md":
        "6e5f7b0daa37c19fbdba024f76cf5456e97931caa2c602211a5b02ac65b853e4",
}
EXPECTED_LEDGER_SHA256 = "2df42d8e4a2da409eee136059408dd18d401c62a16480e18822df537fad02585"

VERTICES = tuple(range(5))
EDGES = tuple(combinations(VERTICES, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
FACES = tuple(combinations(VERTICES, 4))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def file_sha256(path):
    return sha256(path.read_bytes()).hexdigest()


def face_matchings(face):
    a, b, c, d = face
    return (((a, b), (c, d)),
            ((a, c), (b, d)),
            ((a, d), (b, c)))


def supported_face_terms(mask, face):
    return tuple(matching for matching in face_matchings(face)
                 if all(mask & (1 << EDGE_INDEX[edge]) for edge in matching))


def permute_mask(mask, permutation):
    answer = 0
    for index, edge in enumerate(EDGES):
        if not mask & (1 << index):
            continue
        image = tuple(sorted((permutation[edge[0]], permutation[edge[1]])))
        answer |= 1 << EDGE_INDEX[image]
    return answer


def canonical_mask(mask):
    return min(permute_mask(mask, permutation)
               for permutation in permutations(VERTICES))


def mask_edges(mask):
    return tuple(edge for index, edge in enumerate(EDGES)
                 if mask & (1 << index))


def degrees(mask):
    edges = mask_edges(mask)
    return tuple(sum(vertex in edge for edge in edges) for vertex in VERTICES)


def has_disjoint_pair(mask):
    edges = mask_edges(mask)
    return any(set(left).isdisjoint(right)
               for left, right in combinations(edges, 2))


def has_triangle(mask):
    edges = set(mask_edges(mask))
    return any(all(tuple(sorted(edge)) in edges for edge in combinations(triple, 2))
               for triple in combinations(VERTICES, 3))


def exponent(matching, support):
    index = {edge: position for position, edge in enumerate(support)}
    answer = [0] * len(support)
    for edge in matching:
        answer[index[edge]] += 1
    return tuple(answer)


def odd_binomial_holonomy(mask):
    """Return a Laurent odd-cycle relation among two-term face equations."""
    support = mask_edges(mask)
    binomials = []
    for face in FACES:
        terms = supported_face_terms(mask, face)
        if len(terms) == 2:
            left, right = (exponent(term, support) for term in terms)
            difference = tuple(a - b for a, b in zip(left, right, strict=True))
            binomials.append((face, difference))
    for coefficients in product((-1, 0, 1), repeat=len(binomials)):
        if not any(coefficients) or sum(coefficients) % 2 == 0:
            continue
        total = tuple(sum(coefficient * binomials[row][1][column]
                          for row, coefficient in enumerate(coefficients))
                      for column in range(len(support)))
        if not any(total):
            return {
                "faces": tuple(binomials[index][0]
                               for index, value in enumerate(coefficients) if value),
                "coefficients": coefficients,
                "laurent_consequence": "1=(-1)^odd=-1, hence 2=0",
            }
    return None


def support_orbit_classification():
    # A face with exactly one supported perfect matching is already a
    # nonzero monomial equation and is impossible on the exact support torus.
    candidates = {}
    for mask in range(1 << len(EDGES)):
        counts = tuple(len(supported_face_terms(mask, face)) for face in FACES)
        if 1 in counts:
            continue
        candidates.setdefault(canonical_mask(mask), []).append(mask)

    require(len(candidates) == 14, "the no-singleton support orbit count changed")
    require(sum(map(len, candidates.values())) == 172,
            "the no-singleton labelled support count changed")
    edge_profile = Counter(mask.bit_count() for mask in candidates)
    require(edge_profile == Counter({0: 1, 1: 1, 2: 1, 3: 2, 4: 2,
                                     5: 1, 6: 2, 7: 1, 8: 1, 9: 1, 10: 1}),
            f"support orbit edge profile changed: {edge_profile}")

    feasible_boundary = []
    impossible_boundary = []
    dense = []
    for mask, orbit in sorted(candidates.items(), key=lambda item: (item[0].bit_count(), item[0])):
        edge_count = mask.bit_count()
        isolated = degrees(mask).count(0)
        record = {
            "edges": mask_edges(mask),
            "edge_count": edge_count,
            "labelled_orbit_size": len(orbit),
            "degree_sequence": tuple(sorted(degrees(mask))),
            "face_term_counts": tuple(len(supported_face_terms(mask, face))
                                      for face in FACES),
        }
        if edge_count == 10:
            record["type"] = "dense_K5"
            dense.append(record)
        elif not has_disjoint_pair(mask):
            record["type"] = "intersecting_triangle" if has_triangle(mask) else "intersecting_star"
            record["reason_feasible"] = "every four-site hafnian is identically zero"
            feasible_boundary.append(record)
        elif isolated and edge_count in (4, 5, 6):
            record["type"] = {4: "isolated_C4", 5: "isolated_K4_minus_edge",
                              6: "isolated_K4"}[edge_count]
            record["reason_feasible"] = "the sole supported K4 hafnian has 2,2,3 terms"
            feasible_boundary.append(record)
        else:
            holonomy = odd_binomial_holonomy(mask)
            require(holonomy is not None,
                    f"an alleged impossible orbit lacks odd holonomy: {record}")
            record["type"] = {
                6: "K2_3", 7: "K2_3_plus_part_edge",
                8: "K5_minus_disjoint_edge_pair", 9: "K5_minus_edge",
            }[edge_count]
            record["odd_binomial_holonomy"] = holonomy
            impossible_boundary.append(record)

    require(len(feasible_boundary) == 9, "feasible boundary orbit count changed")
    require(len(impossible_boundary) == 4, "impossible boundary orbit count changed")
    require(len(dense) == 1, "dense support orbit count changed")
    return {
        "no_singleton_labelled_supports": 172,
        "no_singleton_S5_orbits": 14,
        "feasible_nondense_orbits": feasible_boundary,
        "odd_holonomy_impossible_orbits": impossible_boundary,
        "dense_orbit": dense[0],
        "classification_theorem": (
            "every feasible nondense exact support is intersecting (star/triangle) "
            "or has one isolated vertex and induced support C4, K4-e, or K4"
        ),
    }


def face_values(values):
    output = []
    for face in FACES:
        total = 0
        for matching in face_matchings(face):
            left, right = matching
            total += values.get(left, 0) * values.get(right, 0)
        output.append(total)
    return output


def face_jacobian(values, zero=Q(0)):
    matrix = []
    for face in FACES:
        row = [zero for _ in EDGES]
        for left, right in face_matchings(face):
            row[EDGE_INDEX[left]] = row[EDGE_INDEX[left]] + values.get(right, zero)
            row[EDGE_INDEX[right]] = row[EDGE_INDEX[right]] + values.get(left, zero)
        matrix.append(row)
    return matrix


def matrix_rank(matrix):
    work = [list(row) for row in matrix]
    row = 0
    for column in range(len(work[0])):
        pivot = next((index for index in range(row, len(work))
                      if work[index][column]), None)
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        value = work[row][column]
        work[row] = [entry / value for entry in work[row]]
        for index in range(len(work)):
            if index == row or not work[index][column]:
                continue
            value = work[index][column]
            work[index] = [entry - value * pivot_entry
                           for entry, pivot_entry in zip(work[index], work[row], strict=True)]
        row += 1
    return row


class Laurent:
    """Small exact Laurent ring in a,b,c,d,e for symbolic minors."""

    nvars = 5

    def __init__(self, terms=()):
        if isinstance(terms, (int, Q)):
            terms = {self.nvars * (0,): Q(terms)}
        self.terms = {tuple(exponent): Q(coefficient)
                      for exponent, coefficient in dict(terms).items() if coefficient}

    def __add__(self, other):
        other = as_laurent(other)
        answer = dict(self.terms)
        for exponent, coefficient in other.terms.items():
            answer[exponent] = answer.get(exponent, Q(0)) + coefficient
            if not answer[exponent]:
                del answer[exponent]
        return Laurent(answer)

    __radd__ = __add__

    def __neg__(self):
        return Laurent({exponent: -coefficient for exponent, coefficient in self.terms.items()})

    def __sub__(self, other):
        return self + (-as_laurent(other))

    def __rsub__(self, other):
        return as_laurent(other) - self

    def __mul__(self, other):
        other = as_laurent(other)
        answer = {}
        for left, lc in self.terms.items():
            for right, rc in other.terms.items():
                exponent = tuple(a + b for a, b in zip(left, right, strict=True))
                answer[exponent] = answer.get(exponent, Q(0)) + lc * rc
        return Laurent(answer)

    __rmul__ = __mul__

    def __truediv__(self, other):
        require(isinstance(other, Laurent) and len(other.terms) == 1,
                "only Laurent monomial division is used")
        (exponent, coefficient), = other.terms.items()
        return Laurent({tuple(a - b for a, b in zip(left, exponent, strict=True)): lc / coefficient
                        for left, lc in self.terms.items()})

    def __pow__(self, exponent):
        require(exponent >= 0, "negative Laurent powers are not needed")
        answer = Laurent(1)
        for _ in range(exponent):
            answer *= self
        return answer

    def __eq__(self, other):
        return self.terms == as_laurent(other).terms


def as_laurent(value):
    return value if isinstance(value, Laurent) else Laurent(value)


def laurent_variables():
    answer = []
    for index in range(Laurent.nvars):
        exponent = [0] * Laurent.nvars
        exponent[index] = 1
        answer.append(Laurent({tuple(exponent): Q(1)}))
    return answer


def permutation_sign(permutation):
    inversions = sum(permutation[left] > permutation[right]
                     for left in range(len(permutation))
                     for right in range(left + 1, len(permutation)))
    return -1 if inversions % 2 else 1


def determinant(matrix):
    size = len(matrix)
    answer = 0
    for permutation in permutations(range(size)):
        term = permutation_sign(permutation)
        for row, column in enumerate(permutation):
            term *= matrix[row][column]
        answer += term
    return answer


class QZ:
    """Q[zeta]/(zeta^2+zeta+1)."""

    def __init__(self, a=0, b=0):
        self.a, self.b = Q(a), Q(b)

    def __add__(self, other):
        other = as_qz(other)
        return QZ(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return QZ(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-as_qz(other))

    def __rsub__(self, other):
        return as_qz(other) - self

    def __mul__(self, other):
        other = as_qz(other)
        return QZ(self.a * other.a - self.b * other.b,
                  self.a * other.b + self.b * other.a - self.b * other.b)

    __rmul__ = __mul__

    def inverse(self):
        norm = self.a * self.a - self.a * self.b + self.b * self.b
        require(norm, "attempted to invert zero in Q(zeta)")
        return QZ((self.a - self.b) / norm, -self.b / norm)

    def __truediv__(self, other):
        return self * as_qz(other).inverse()

    def __eq__(self, other):
        other = as_qz(other)
        return self.a == other.a and self.b == other.b

    def __bool__(self):
        return bool(self.a or self.b)

    def text(self):
        return f"{self.a}+({self.b})*zeta"


def as_qz(value):
    return value if isinstance(value, QZ) else QZ(value)


def normal_rank_classification():
    # Intersecting exact supports have h=0 termwise.  Their representative
    # tangent ranks show why they are singular normal faces.
    intersecting = {
        "zero": {},
        "edge": {(0, 1): Q(1)},
        "two_star": {(0, 1): Q(1), (0, 2): Q(1)},
        "three_star": {(0, 1): Q(1), (0, 2): Q(1), (0, 3): Q(1)},
        "triangle": {(0, 1): Q(1), (0, 2): Q(1), (1, 2): Q(1)},
        "four_star": {(0, 1): Q(1), (0, 2): Q(1),
                      (0, 3): Q(1), (0, 4): Q(1)},
    }
    intersecting_ranks = {}
    for name, values in intersecting.items():
        require(face_values(values) == [0] * 5, f"{name} left V(h)")
        intersecting_ranks[name] = matrix_rank(face_jacobian(values))
    require(intersecting_ranks == {
        "zero": 0, "edge": 3, "two_star": 3,
        "three_star": 4, "triangle": 3, "four_star": 4,
    }, f"intersecting ranks changed: {intersecting_ranks}")

    # Canonical isolated four-site supports.  The C4 relation is ad+bc=0.
    a, b, c, d, e = laurent_variables()
    c4 = {(0, 2): a, (0, 3): b, (1, 2): c, (1, 3): -(b * c) / a}
    k4e = dict(c4)
    k4e[(0, 1)] = e
    columns = tuple(EDGE_INDEX[edge] for edge in
                    ((0, 3), (0, 4), (1, 4), (2, 4), (3, 4)))
    expected_binomial_minor = 4 * b ** 2 * c ** 3
    for name, values in (("isolated_C4", c4), ("isolated_K4_minus_edge", k4e)):
        require(face_values(values) == [Laurent(0)] * 5, f"{name} left V(h)")
        jacobian = face_jacobian(values, Laurent(0))
        minor = determinant([[row[column] for column in columns] for row in jacobian])
        require(minor == expected_binomial_minor,
                f"{name} universal rank-five minor changed")

    # On isolated K4, write x02=a,x03=b,x12=c,x13=d,x01=e and
    # x23=-(ad+bc)/e.  One rank-five minor is 4*c*S, S=(ad)^2+adbc+(bc)^2.
    k4 = {(0, 1): e, (0, 2): a, (0, 3): b,
          (1, 2): c, (1, 3): d, (2, 3): -(a * d + b * c) / e}
    require(face_values(k4) == [Laurent(0)] * 5, "isolated K4 left V(h)")
    k4_jacobian = face_jacobian(k4, Laurent(0))
    k4_minor = determinant([[row[column] for column in columns]
                            for row in k4_jacobian])
    S = (a * d) ** 2 + a * b * c * d + (b * c) ** 2
    require(k4_minor == 4 * c * S, "isolated K4 discriminant minor changed")

    # Exact cyclotomic K4 boundary: matching products are zeta^2,zeta,1.
    zeta = QZ(0, 1)
    qz_values = {(0, 1): QZ(1), (0, 2): QZ(1), (0, 3): QZ(1),
                 (1, 2): QZ(1), (1, 3): zeta, (2, 3): zeta * zeta}
    require(face_values(qz_values) == [QZ()] * 5,
            "cyclotomic isolated K4 left V(h)")
    qz_jacobian = face_jacobian(qz_values, QZ())
    require(matrix_rank(qz_jacobian) == 4,
            "cyclotomic isolated K4 normal rank changed")
    covector = (QZ(), QZ(1), zeta, zeta * zeta, QZ(1))
    for column in range(len(EDGES)):
        require(sum((covector[row] * qz_jacobian[row][column]
                     for row in range(5)), QZ()) == QZ(),
                "cyclotomic K4 primitive normal covector stopped annihilating dh")

    return {
        "intersecting_support_ranks": intersecting_ranks,
        "regular_isolated_strata": {
            "C4": {"rank": 5, "universal_minor": "4*b^2*c^3"},
            "K4_minus_edge": {"rank": 5, "universal_minor": "4*b^2*c^3"},
            "K4_generic": {
                "rank": 5,
                "sufficient_minor": "4*c*((a*d)^2+a*b*c*d+(b*c)^2)",
            },
        },
        "first_singular_two_matching_boundary": {
            "support": "isolated K4",
            "matching_products": ["zeta^2", "zeta", "1"],
            "equation": "zeta^2+zeta+1=0",
            "normal_rank": 4,
            "face_order": ["0123", "0124", "0134", "0234", "1234"],
            "primitive_left_covector": [entry.text() for entry in covector],
        },
        "derived_comparison_consequence": (
            "where rank(dh)=5, choose five dual normal directions; quadraticity gives "
            "B(tau)=I+tau*R, so the 827e329 normal Hasse-face repair applies formally"
        ),
        "physical_promotion": False,
    }


def main():
    for relative, expected in PINS.items():
        actual = file_sha256(ROOT / relative)
        require(actual == expected,
                f"dependency changed: {relative}: {actual} != {expected}")
    ledger = {
        "scope": "exact support tori of the five-site q_m square-zero slice",
        "support_classification": support_orbit_classification(),
        "normal_rank": normal_rank_classification(),
        "routing_status": {
            "regular_isolated_four_site_strata": (
                "comparison-compatible in the relative derived normal module"
            ),
            "intersecting_star_triangle_strata": (
                "not routed by the pinned fixed-word packet; require a source theorem "
                "excluding/routing matching-number-at-most-one q_m support"
            ),
            "cyclotomic_isolated_K4": (
                "one primitive normal direction is missing; require an endpoint-word "
                "changing row pairing nontrivially with the displayed covector"
            ),
        },
        "nonclaims": [
            "no physical cap identification",
            "no full-source point on a boundary stratum",
            "no claim that q-support alone implies inactive/rootless routing",
        ],
        "pins": PINS,
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"nondense face-zero strata ledger changed: {digest}")
    print("h3 Component-IV nondense face-zero strata: PASS")
    print("14 no-singleton S5 orbits: 9 feasible boundary, 4 odd-holonomy impossible, 1 dense")
    print("C4/K4-e/generic K4: normal rank 5; cyclotomic isolated K4: rank 4")
    print("physical cap comparison and singular-stratum routing: NOT CLAIMED")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
