#!/usr/bin/env python3
"""Exact referee for the weight-zero diagonal branch and its 4+4 blocker.

The arithmetic is in Q(r,g), r^2=2 and g^2=65.  We instantiate the
four-parameter family at u=v=w=t=1, replay the literal normalized Hafnian
polynomials, and then scan the complete B4 orbit of its Q support.

The last scan is purely combinatorial but theorem-bearing: a two-colour
4+4 packet requires supp(Q_c) to be disjoint from the bitwise complement of
supp(Q_d).  Thus the absence of a compatible ordered pair rules out every
pair of symmetry-transformed copies of this family.  It is not a statement
about other components of the cofactor branch.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_weight0_char0_family_and_packet.json"
EDGES = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
TRIPLES = ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3))
BRANCH_MASK = 51  # bits 1,1,0,0,1,1 in edge order above


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


@dataclass(frozen=True)
class NF:
    """Element a+b*r+c*g+d*r*g of Q(r,g), r^2=2, g^2=65."""

    coefficients: tuple[Fraction, Fraction, Fraction, Fraction]

    @staticmethod
    def coerce(value):
        if isinstance(value, NF):
            return value
        return NF((Fraction(value), Fraction(0), Fraction(0), Fraction(0)))

    def __add__(self, other):
        other = NF.coerce(other)
        return NF(tuple(a + b for a, b in zip(self.coefficients,
                                               other.coefficients)))

    __radd__ = __add__

    def __neg__(self):
        return NF(tuple(-value for value in self.coefficients))

    def __sub__(self, other):
        return self + (-NF.coerce(other))

    def __rsub__(self, other):
        return NF.coerce(other) - self

    def __mul__(self, other):
        other = NF.coerce(other)
        answer = [Fraction(0) for _ in range(4)]
        # Basis indices are bit pairs (power of r, power of g).
        for left, a in enumerate(self.coefficients):
            for right, b in enumerate(other.coefficients):
                r_power = (left & 1) + (right & 1)
                g_power = (left >> 1) + (right >> 1)
                coefficient = a * b
                if r_power == 2:
                    coefficient *= 2
                    r_power = 0
                if g_power == 2:
                    coefficient *= 65
                    g_power = 0
                answer[r_power + 2 * g_power] += coefficient
        return NF(tuple(answer))

    __rmul__ = __mul__

    def inverse(self):
        require(self != ZERO, "division by zero in Q(r,g)")
        # Columns of multiplication by self in the fixed basis.
        basis = (ONE, R, G, R * G)
        matrix = [list((self * vector).coefficients) +
                  [Fraction(1 if row == 0 else 0)]
                  for row, vector in enumerate(basis)]
        # The construction above stores basis images as rows.  Transpose the
        # coefficient square before rational Gaussian elimination.
        matrix = [[matrix[column][row] for column in range(4)] +
                  [Fraction(1 if row == 0 else 0)]
                  for row in range(4)]
        for column in range(4):
            pivot = next(row for row in range(column, 4)
                         if matrix[row][column])
            matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
            scale = matrix[column][column]
            matrix[column] = [value / scale for value in matrix[column]]
            for row in range(4):
                if row == column or not matrix[row][column]:
                    continue
                scale = matrix[row][column]
                matrix[row] = [a - scale * b
                               for a, b in zip(matrix[row], matrix[column])]
        answer = NF(tuple(matrix[row][4] for row in range(4)))
        require(self * answer == ONE, "number-field inverse replay failed")
        return answer

    def __truediv__(self, other):
        return self * NF.coerce(other).inverse()

    def __rtruediv__(self, other):
        return NF.coerce(other) / self

    def json_value(self):
        def encode(value):
            return (str(value.numerator) if value.denominator == 1
                    else f"{value.numerator}/{value.denominator}")
        return [encode(value) for value in self.coefficients]


ZERO = NF((Fraction(0),) * 4)
ONE = NF.coerce(1)
R = NF((Fraction(0), Fraction(1), Fraction(0), Fraction(0)))
G = NF((Fraction(0), Fraction(0), Fraction(1), Fraction(0)))
require(R * R == NF.coerce(2) and G * G == NF.coerce(65),
        "number-field relations changed")


def perfect_matchings(vertices):
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        answer.extend((((first, second),) + tail)
                      for tail in perfect_matchings(rest))
    return tuple(answer)


def variable_for_sites(u, v):
    if u > v:
        u, v = v, u
    i, x = divmod(u, 2)
    j, y = divmod(v, 2)
    if i == j:
        return None
    return 4 * EDGE_INDEX[(i, j)] + 2 * x + y


def matching_value(vertices, values):
    answer = ZERO
    for matching in perfect_matchings(tuple(vertices)):
        term = ONE
        for u, v in matching:
            variable = variable_for_sites(u, v)
            if variable is not None:
                term *= values[variable]
        answer += term
    return answer


def permanent_value(edge, values):
    start = 4 * edge
    return values[start] * values[start + 3] + values[start + 1] * values[start + 2]


def triangle_value(i, j, k, values):
    ij = EDGE_INDEX[(i, j)]
    ik = EDGE_INDEX[(i, k)]
    jk = EDGE_INDEX[(j, k)]
    answer = ZERO
    for x, y, z in product((0, 1), repeat=3):
        answer += (values[4 * ij + 2 * x + y]
                   * values[4 * ik + 2 * (1 - x) + z]
                   * values[4 * jk + 2 * (1 - y) + (1 - z)])
    return answer


def q_value(index, values):
    bits = tuple((index >> (3 - site)) & 1 for site in range(4))
    answer = ZERO
    for (i, j), (k, l) in (((0, 1), (2, 3)),
                           ((0, 2), (1, 3)),
                           ((0, 3), (1, 2))):
        answer += (values[4 * EDGE_INDEX[(i, j)] + 2 * bits[i] + bits[j]]
                   * values[4 * EDGE_INDEX[(k, l)] + 2 * bits[k] + bits[l]])
    return answer


def family_point():
    rho = R - 1
    sigma = -R - 1
    eta = (-5 * rho - 12 + G * (rho + 2)) / (6 * rho)
    u = v = w = t = ONE
    b = (rho * u / v, sigma * u / w, u,
         sigma * v / w, v, w)
    a5 = t
    a4 = eta * t * v / w
    a3 = t * v * (rho * eta + sigma)
    a2 = (u * t / w * ((-3 * rho - 7) * eta + 5 * rho + 13)
          / (rho + 5))
    a1 = (u * t * ((7 * rho + 3) * eta - 2 * rho - 4)
          / (rho + 5))
    a0 = sigma * (v * a2 + u * a4)
    a = (a0, a1, a2, a3, a4, a5)
    values = []
    for edge in range(6):
        values.extend((a[edge], b[edge], -ONE / b[edge], ZERO))
    return tuple(values), a, b, eta


def transform_q_index(index, switches, permutation):
    bits = tuple((index >> (3 - site)) & 1 for site in range(4))
    transformed = [0] * 4
    for site in range(4):
        transformed[permutation[site]] = bits[site] ^ switches[site]
    return sum(transformed[site] << (3 - site) for site in range(4))


def transform_branch_mask(mask, switches, permutation):
    answer = 0
    for edge, (i, j) in enumerate(EDGES):
        bit = ((mask >> edge) & 1) ^ switches[i] ^ switches[j]
        target = EDGE_INDEX[tuple(sorted((permutation[i], permutation[j])))]
        answer |= bit << target
    return answer


def transform_support(support, switches, permutation):
    return tuple(sorted(transform_q_index(index, switches, permutation)
                        for index in support))


def transform_cell_index(index, switches, permutation):
    edge, entry = divmod(index, 4)
    i, j = EDGES[edge]
    x, y = divmod(entry, 2)
    pi, pj = permutation[i], permutation[j]
    x ^= switches[i]
    y ^= switches[j]
    if pi < pj:
        return 4 * EDGE_INDEX[(pi, pj)] + 2 * x + y
    return 4 * EDGE_INDEX[(pj, pi)] + 2 * y + x


def transform_cell_mask(mask, switches, permutation):
    answer = 0
    for index in range(24):
        if mask >> index & 1:
            answer |= 1 << transform_cell_index(index, switches, permutation)
    return answer


def indices(mask):
    return [index for index in range(mask.bit_length()) if mask >> index & 1]


def main():
    values, a, b, eta = family_point()
    permanents = [permanent_value(edge, values) for edge in range(6)]
    triangles = [triangle_value(*triple, values) for triple in TRIPLES]
    cofactor_rows = []
    for edge, (i, j) in enumerate(EDGES):
        entries = (((0, 1), (1, 0)) if BRANCH_MASK >> edge & 1
                   else ((0, 0), (1, 1)))
        for x, y in entries:
            cofactor_rows.append((edge, x, y,
                                  matching_value(tuple(site for site in range(8)
                                                       if site not in
                                                       (2 * i + x, 2 * j + y)),
                                                 values)))
    q_values = tuple(q_value(index, values) for index in range(16))
    q_zero = tuple(index for index, value in enumerate(q_values)
                   if value == ZERO)
    q_live = tuple(index for index, value in enumerate(q_values)
                   if value != ZERO)
    hafnian = matching_value(tuple(range(8)), values)

    require(permanents == [-ONE] * 6, "a block permanent changed")
    require(triangles == [NF.coerce(2)] * 4, "a triangle contraction changed")
    require(all(value == ZERO for *_, value in cofactor_rows),
            "a selected cofactor is nonzero")
    require(hafnian == NF.coerce(4), "family Hafnian changed")
    require(q_zero == (0, 2, 7, 8, 11, 13, 14, 15),
            "family Q-zero set changed")
    require(len(q_live) == 8, "family Q support changed")

    # Keep the global clone flip.  It is trivial on the six branch-orientation
    # bits but sends Q_s to Q_{15-s}, so quotienting it out would miss 24
    # support masks and would be unsound for the 4+4 comparison.
    group = tuple((switches, permutation)
                  for switches in product((0, 1), repeat=4)
                  for permutation in permutations(range(4)))
    require(len(group) == 384, "full B4 size changed")
    zero_orbit = sorted({
        tuple(sorted(transform_q_index(index, switches, permutation)
                     for index in q_zero))
        for switches, permutation in group
    })
    require(len(zero_orbit) == 96, "Q-zero support orbit changed")
    universe = set(range(16))
    intersection_histogram = Counter()
    minimum = 17
    minimum_pair = None
    compatible = []
    for left_zero in zero_orbit:
        left_live = universe - set(left_zero)
        for right_zero in zero_orbit:
            right_live = universe - set(right_zero)
            offending = sorted(left_live & {15 - index for index in right_live})
            intersection_histogram[len(offending)] += 1
            if len(offending) < minimum:
                minimum = len(offending)
                minimum_pair = (left_zero, right_zero, tuple(offending))
            if not offending:
                compatible.append((left_zero, right_zero))
    require(not compatible and minimum == 2,
            "a pair of transformed family supports passed the 4+4 packet")

    self_offending = sorted(set(q_live) & {15 - index for index in q_live})
    require(self_offending == [3, 5, 6, 9, 10, 12],
            "self-pair 4+4 control changed")

    # Earlier exact-Q NONUNIT tests used two allowed seven-coordinate sets,
    # obtained by deleting Q_1 or Q_4 from the live support above.  The exact
    # support-six point below lies in both, so these are containment/support
    # data, not exact-support-seven components.
    k7_left = tuple(index for index in q_live if index != 1)
    k7_other = tuple(index for index in q_live if index != 4)

    def joint_orbit(branch, support):
        return {(transform_branch_mask(branch, switches, permutation),
                 transform_support(support, switches, permutation))
                for switches, permutation in group}

    k7_orbit = joint_orbit(BRANCH_MASK, k7_left)
    k7_other_orbit = joint_orbit(BRANCH_MASK, k7_other)
    k8_joint_orbit = joint_orbit(BRANCH_MASK, q_live)
    require(k7_orbit == k7_other_orbit and len(k7_orbit) == 192,
            "the two k7 components left their common joint orbit")
    require(len(k8_joint_orbit) == 192, "k8 joint orbit size changed")

    def support_compatible(left, right):
        return not (set(left) & {15 - index for index in right})

    joint_compatibility = {}
    for left_name, left_orbit in (("k7", k7_orbit),
                                  ("k8", k8_joint_orbit)):
        for right_name, right_orbit in (("k7", k7_orbit),
                                        ("k8", k8_joint_orbit)):
            joint_compatibility[f"{left_name}_to_{right_name}"] = sum(
                support_compatible(left_support, right_support)
                for _, left_support in left_orbit
                for _, right_support in right_orbit)
    require(joint_compatibility == {
        "k7_to_k7": 1152, "k7_to_k8": 0,
        "k8_to_k7": 0, "k8_to_k8": 0,
    }, "joint k7/k8 support compatibility changed")

    fixed_left = (BRANCH_MASK, tuple(sorted(k7_left)))
    left_stabilizer = tuple(
        (switches, permutation) for switches, permutation in group
        if (transform_branch_mask(BRANCH_MASK, switches, permutation),
            transform_support(k7_left, switches, permutation)) == fixed_left)
    require(len(left_stabilizer) == 2, "fixed k7 component stabilizer changed")
    fixed_mates = sorted(
        (branch, support) for branch, support in k7_orbit
        if support_compatible(fixed_left[1], support))
    require(len(fixed_mates) == 6, "fixed k7 mate census changed")
    unseen_mates = set(fixed_mates)
    mate_orbits = []
    while unseen_mates:
        representative = min(unseen_mates)
        orbit = {
            (transform_branch_mask(representative[0], switches, permutation),
             transform_support(representative[1], switches, permutation))
            for switches, permutation in left_stabilizer}
        unseen_mates -= orbit
        mate_orbits.append(tuple(sorted(orbit)))
    mate_orbits.sort()
    require(sorted(map(len, mate_orbits)) == [1, 1, 2, 2],
            "fixed k7 mate orbit sizes changed")

    # The exact d=0 normal form sharpens the NONUNIT handoff.  Its fixed live
    # set is F={3,5,6,9,10,12}; the quotient coordinates are
    # (Q1,Q2,Q4,Q8), while Q0 is a nondegenerate quadratic.  Thus its
    # support-eight strata have either one quotient coordinate together with
    # Q0, or two quotient coordinates with Q0=0.  The four one-coordinate
    # representatives form one joint B4 orbit.  Only that orbit has any
    # support-level mate; after fixing Q1 the mate support is forced and only
    # three cofactor branch masks remain.
    fixed_live = {3, 5, 6, 9, 10, 12}
    quotient_indices = (1, 2, 4, 8)
    one_y_supports = {
        index: tuple(sorted(fixed_live | {0, index}))
        for index in quotient_indices
    }
    one_y_orbits = {index: joint_orbit(BRANCH_MASK, support)
                    for index, support in one_y_supports.items()}
    require(all(orbit == one_y_orbits[1]
                for orbit in one_y_orbits.values())
            and len(one_y_orbits[1]) == 192,
            "one-y support-eight joint orbit changed")
    one_y_orbit = one_y_orbits[1]
    normalized_one_y = (BRANCH_MASK, one_y_supports[1])
    forced_mate_support = tuple(sorted(
        universe - {15 - index for index in normalized_one_y[1]}))
    one_y_mates = sorted(
        item for item in one_y_orbit
        if support_compatible(normalized_one_y[1], item[1]))
    require(one_y_mates == [
        (7, forced_mate_support),
        (25, forced_mate_support),
        (42, forced_mate_support),
    ] and forced_mate_support == (0, 1, 2, 4, 7, 8, 11, 13),
            "one-y forced mate census changed")
    one_y_stabilizer = tuple(
        action for action in group
        if (transform_branch_mask(BRANCH_MASK, *action),
            transform_support(normalized_one_y[1], *action)) ==
        normalized_one_y)
    require(len(one_y_stabilizer) == 2,
            "normalized one-y stabilizer changed")
    remaining = set(one_y_mates)
    one_y_mate_orbits = []
    while remaining:
        representative = min(remaining)
        orbit = {
            (transform_branch_mask(representative[0], *action),
             transform_support(representative[1], *action))
            for action in one_y_stabilizer
        }
        remaining -= orbit
        one_y_mate_orbits.append(tuple(sorted(orbit)))
    one_y_mate_orbits.sort()
    require(sorted(map(len, one_y_mate_orbits)) == [1, 2],
            "one-y mate stabilizer orbits changed")

    two_y_orbits = []
    two_y_representatives = {}
    for pair in combinations(quotient_indices, 2):
        support = tuple(sorted(fixed_live | set(pair)))
        orbit = joint_orbit(BRANCH_MASK, support)
        orbit_class = next((index for index, old in enumerate(two_y_orbits)
                            if old == orbit), None)
        if orbit_class is None:
            orbit_class = len(two_y_orbits)
            two_y_orbits.append(orbit)
        two_y_representatives[str(pair)] = {
            "support": list(support),
            "orbit_class": orbit_class,
            "orbit_size": len(orbit),
        }
    require(sorted(map(len, two_y_orbits)) == [96, 192],
            "two-y support-eight orbit classes changed")
    orbit_classes = [one_y_orbit] + two_y_orbits
    compatibility_matrix = [[
        sum(support_compatible(left[1], right[1])
            for left in left_orbit for right in right_orbit)
        for right_orbit in orbit_classes]
        for left_orbit in orbit_classes]
    require(compatibility_matrix == [
        [576, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
    ], "normal-form support-eight compatibility changed")

    # A smaller exact component exists over Q(r), r^2=2.  Put z=r-1,
    # a_e=d_e=0 and c_e=-1/b_e for the displayed b tuple.  This point is
    # independently rebuilt here from the literal 105 matchings.
    zeta = R - 1
    support6_b = (zeta, -zeta - 2, ONE, -zeta - 2, ONE, ONE)
    support6_values = []
    for edge in range(6):
        support6_values.extend((ZERO, support6_b[edge],
                                -ONE / support6_b[edge], ZERO))
    support6_values = tuple(support6_values)
    support6_permanents = tuple(permanent_value(edge, support6_values)
                                for edge in range(6))
    support6_triangles = tuple(triangle_value(*triple, support6_values)
                               for triple in TRIPLES)
    support6_q = tuple(q_value(index, support6_values)
                       for index in range(16))
    support6_q_live = tuple(index for index, value in enumerate(support6_q)
                            if value != ZERO)
    support6_h = matching_value(tuple(range(8)), support6_values)
    support6_cofactors = []
    for edge, (i, j) in enumerate(EDGES):
        for x, y in product((0, 1), repeat=2):
            support6_cofactors.append(matching_value(
                tuple(site for site in range(8)
                      if site not in (2 * i + x, 2 * j + y)),
                support6_values))
    support6_x_live_mask = sum(1 << index for index, value
                               in enumerate(support6_values) if value != ZERO)
    support6_c_live_mask = sum(1 << index for index, value
                               in enumerate(support6_cofactors) if value != ZERO)
    require(support6_permanents == (-ONE,) * 6
            and support6_triangles == (NF.coerce(2),) * 4,
            "support-six base equations changed")
    require(support6_h == NF.coerce(4)
            and support6_q_live == (3, 5, 6, 9, 10, 12),
            "support-six H/Q data changed")
    require(indices(support6_x_live_mask) ==
            [4 * edge + entry for edge in range(6) for entry in (1, 2)],
            "support-six X support changed")
    require(indices(support6_c_live_mask) == [9, 10, 13, 14],
            "support-six cofactor support changed")
    mutated_support6_values = list(support6_values)
    mutated_support6_values[1] += ONE
    require(permanent_value(0, tuple(mutated_support6_values)) != -ONE,
            "support-six coefficient mutation did not fire")
    # In particular the twelve cofactors selected by mask 51 vanish.
    for edge in range(6):
        selected = ((1, 2) if BRANCH_MASK >> edge & 1 else (0, 3))
        require(all(support6_cofactors[4 * edge + entry] == ZERO
                    for entry in selected),
                "support-six selected cofactor changed")

    support6_orbit = set()
    for switches, permutation in group:
        support6_orbit.add((
            transform_branch_mask(BRANCH_MASK, switches, permutation),
            transform_support(support6_q_live, switches, permutation),
            transform_cell_mask(support6_x_live_mask, switches, permutation),
            transform_cell_mask(support6_c_live_mask, switches, permutation),
        ))
    require(len(support6_orbit) == 24,
            "support-six enriched B4 orbit size changed")
    q_compatible6 = 0
    left_cross_failures6 = 0
    right_cross_failures6 = 0
    full_compatible6 = []
    for left in support6_orbit:
        for right in support6_orbit:
            if not support_compatible(left[1], right[1]):
                continue
            q_compatible6 += 1
            left_fails = bool(left[2] & right[3])
            right_fails = bool(right[2] & left[3])
            left_cross_failures6 += left_fails
            right_cross_failures6 += right_fails
            if not left_fails and not right_fails:
                full_compatible6.append((left, right))
    require(q_compatible6 == 288
            and left_cross_failures6 == right_cross_failures6 == 288
            and not full_compatible6,
            "support-six pairwise obstruction changed")

    result = {
        "status": "UNAUDITED exact characteristic-zero family referee",
        "field": "Q(r,g), r^2=2, g^2=65",
        "parameter_specialization": "u=v=w=t=1",
        "branch_mask": BRANCH_MASK,
        "branch_bits_01_02_03_12_13_23": [
            (BRANCH_MASK >> edge) & 1 for edge in range(6)],
        "eta_basis_1_r_g_rg": eta.json_value(),
        "a_basis_1_r_g_rg": [value.json_value() for value in a],
        "b_basis_1_r_g_rg": [value.json_value() for value in b],
        "permanents": [value.json_value() for value in permanents],
        "triangles": [value.json_value() for value in triangles],
        "selected_cofactor_count": len(cofactor_rows),
        "selected_cofactors_all_zero": True,
        "H_basis_1_r_g_rg": hafnian.json_value(),
        "Q_zero_indices": list(q_zero),
        "Q_live_indices": list(q_live),
        "Q_values_basis_1_r_g_rg": [value.json_value() for value in q_values],
        "full_B4_elements": len(group),
        "distinct_transformed_Q_zero_sets": len(zero_orbit),
        "ordered_support_pairs": len(zero_orbit) ** 2,
        "four_plus_four_offending_coordinate_histogram": {
            str(key): value for key, value in sorted(intersection_histogram.items())},
        "compatible_ordered_support_pairs": len(compatible),
        "minimum_offending_coordinates": minimum,
        "first_minimum_pair": {
            "left_Q_zero": list(minimum_pair[0]),
            "right_Q_zero": list(minimum_pair[1]),
            "offending_left_indices_s_with_Qc_s_Qd_15_minus_s_nonzero":
                list(minimum_pair[2]),
        },
        "self_pair_offending_indices": self_offending,
        "exact_Q_nonunit_k7_support_handoff": {
            "input_scope": (
                "The two exact-Q NONUNIT allowed-support ideals do not "
                "certify exact support seven: both contain the explicit "
                "support-six point checked below. This subsection certifies "
                "only their joint orbit and support compatibility."
            ),
            "two_reported_live_supports": [list(k7_left), list(k7_other)],
            "same_full_joint_B4_orbit": True,
            "joint_orbit_size": len(k7_orbit),
            "k8_joint_orbit_size": len(k8_joint_orbit),
            "ordered_joint_support_compatibility": joint_compatibility,
            "fixed_left": {
                "branch_mask": fixed_left[0],
                "live_support": list(fixed_left[1]),
            },
            "fixed_left_stabilizer_size": len(left_stabilizer),
            "fixed_left_Q_compatible_mates": [
                {"branch_mask": branch, "live_support": list(support)}
                for branch, support in fixed_mates],
            "fixed_left_mate_orbits": [[
                {"branch_mask": branch, "live_support": list(support)}
                for branch, support in orbit] for orbit in mate_orbits],
        },
        "exact_support6_component": {
            "field": "Q(r), r^2=2; z=r-1 satisfies z^2+2z-1=0",
            "a_entries": [ZERO.json_value()] * 6,
            "b_entries_basis_1_r_g_rg": [value.json_value()
                                           for value in support6_b],
            "d_entries": [ZERO.json_value()] * 6,
            "H_basis_1_r_g_rg": support6_h.json_value(),
            "Q_live_indices": list(support6_q_live),
            "Q_values_basis_1_r_g_rg": [value.json_value()
                                          for value in support6_q],
            "X_live_cell_indices": indices(support6_x_live_mask),
            "cofactor_live_cell_indices": indices(support6_c_live_mask),
            "enriched_joint_B4_orbit_size": len(support6_orbit),
            "Q_compatible_ordered_pairs": q_compatible6,
            "left_X_times_right_cofactor_failures": left_cross_failures6,
            "right_X_times_left_cofactor_failures": right_cross_failures6,
            "fully_compatible_ordered_pairs": len(full_compatible6),
            "coefficient_mutation_fired": True,
            "conclusion": (
                "The size-six component has many Q-compatible pairings, but "
                "every one violates X_left*C_right and X_right*C_left."
            ),
        },
        "exact_d0_normal_form_support_handoff": {
            "input": (
                "base quotient coordinates y=(Q1,Q2,Q4,Q8), fixed live "
                "F={3,5,6,9,10,12}, with Q0 one nondegenerate quadratic"
            ),
            "one_y_representatives": {
                str(index): list(support)
                for index, support in one_y_supports.items()
            },
            "one_y_joint_orbit_size": len(one_y_orbit),
            "normalized_left": {
                "branch_mask": normalized_one_y[0],
                "Q_live_support": list(normalized_one_y[1]),
            },
            "forced_mate_Q_live_support": list(forced_mate_support),
            "forced_mate_branch_masks": [item[0] for item in one_y_mates],
            "left_stabilizer_size": len(one_y_stabilizer),
            "mate_stabilizer_orbit_sizes": sorted(
                map(len, one_y_mate_orbits)),
            "two_y_representatives": two_y_representatives,
            "orbit_order": ["one_y", "two_y_class_0", "two_y_class_1"],
            "ordered_support_compatibility_matrix": compatibility_matrix,
            "conclusion": (
                "The two-y support-eight strata have no support-compatible "
                "mate. For the only live case, normalized one-y, Q support "
                "forces the mate support and leaves branch masks 7,25,42 "
                "in two left-stabilizer orbits."
            ),
        },
        "conclusion": (
            "One-colour Q-support lower bounds of eight or seven are false: "
            "the checker exhibits exact H=4 components of support eight and "
            "six. The support-eight B4 orbit has no 4+4-compatible ordered "
            "pair. The support-six enriched B4 orbit has 288 Q-compatible "
            "ordered pairs, but all 288 fail each direction of the 6+2 "
            "X/cofactor packet, so it has no fully compatible ordered pair. "
            "The remaining global task is to classify any other H-live "
            "components; the reported k7 NONUNIT ideals contain the support-"
            "six point and are not separate exact-support-seven evidence."
        ),
        "smallest_detecting_packet": (
            "the 16 compressed 4+4 coordinates Q_c(s)Q_d(15-s); the "
            "pairconstant and selected 6+2/cofactor equations already vanish"
        ),
        "scope": (
            "This excludes pairings within the exact support-eight family "
            "and within the exact support-six component, including all full-"
            "B4 transforms. It does not classify every component of the "
            "three cofactor-orientation branch ideals or exclude cross-"
            "pairings with an as-yet-unclassified component."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("weight-zero characteristic-zero family: PASS")
    print("H / Q zero / live:", hafnian.json_value(), q_zero, q_live)
    print("support orbit / ordered pairs:", len(zero_orbit), len(zero_orbit) ** 2)
    print("compatible / minimum offending:", len(compatible), minimum)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
