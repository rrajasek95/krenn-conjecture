#!/usr/bin/env python3
"""Exact referee for the weight-zero support-six Laurent component.

The four supervertices each contain two physical vertices.  The selected
same-colour matching edges are normalized to one.  On every other superedge
we use a 2x2 block.  This file independently evaluates the literal Hafnian,
its 24 block-entry cofactors, the six permanent rows, four triangle rows and
sixteen four-vertex Q contractions over Q(z), z^2+2z-1=0.

It then applies the full anchor stabilizer B4=C2^4 semidirect S4 to the joint
(nonzero-cell, nonzero-cofactor, nonzero-Q) support record.  Two colours can
satisfy the 4+4 and 6+2 core packets only if

  Q_A intersect complement(Q_B) = empty,
  X_B intersect C_A = empty, and X_A intersect C_B = empty.

The audit proves that no ordered pair in this component orbit passes all
three tests.  It does not classify other components of the diagonal ideal.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_support6_component_pairwise_obstruction.json"
SUPER_EDGES = tuple(combinations(range(4), 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(SUPER_EDGES)}
BRANCH_MASK = 51


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


@dataclass(frozen=True)
class K:
    """a+b*z in Q[z]/(z^2+2z-1)."""

    a: Fraction = Fraction(0)
    b: Fraction = Fraction(0)

    def __add__(self, other):
        other = as_k(other)
        return K(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return K(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-as_k(other))

    def __rsub__(self, other):
        return as_k(other) - self

    def __mul__(self, other):
        other = as_k(other)
        # z^2=1-2z.
        return K(self.a * other.a + self.b * other.b,
                 self.a * other.b + self.b * other.a
                 - 2 * self.b * other.b)

    __rmul__ = __mul__

    def __bool__(self):
        return bool(self.a or self.b)

    def encode(self):
        return [[self.a.numerator, self.a.denominator],
                [self.b.numerator, self.b.denominator]]


def as_k(value):
    if isinstance(value, K):
        return value
    return K(Fraction(value), Fraction(0))


ZERO = K()
ONE = K(Fraction(1))
Z = K(Fraction(0), Fraction(1))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
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


PM8 = perfect_matchings(range(8))


def block_entry(blocks, i, j, clone_i, clone_j):
    if i > j:
        i, j = j, i
        clone_i, clone_j = clone_j, clone_i
    return blocks[EDGE_INDEX[(i, j)]][2 * clone_i + clone_j]


def graph_entry(blocks, u, v):
    super_u, clone_u = divmod(u, 2)
    super_v, clone_v = divmod(v, 2)
    if super_u == super_v:
        require(clone_u != clone_v, "repeated physical vertex")
        return ONE
    return block_entry(blocks, super_u, super_v, clone_u, clone_v)


def hafnian_on(blocks, vertices):
    answer = ZERO
    for matching in perfect_matchings(tuple(vertices)):
        term = ONE
        for u, v in matching:
            term *= graph_entry(blocks, u, v)
        answer += term
    return answer


def cofactor(blocks, raw_index):
    edge_index, position = divmod(raw_index, 4)
    i, j = SUPER_EDGES[edge_index]
    clone_i, clone_j = divmod(position, 2)
    removed = {2 * i + clone_i, 2 * j + clone_j}
    return hafnian_on(blocks, tuple(v for v in range(8)
                                    if v not in removed))


def permanent(block):
    return block[0] * block[3] + block[1] * block[2]


def triangle(blocks, i, j, k):
    answer = ZERO
    for clone_i, clone_j, clone_k in product((0, 1), repeat=3):
        answer += (
            block_entry(blocks, i, j, clone_i, clone_j)
            * block_entry(blocks, i, k, 1 - clone_i, clone_k)
            * block_entry(blocks, j, k, 1 - clone_j, 1 - clone_k)
        )
    return answer


def q_value(blocks, value):
    bits = tuple((value >> (3 - site)) & 1 for site in range(4))
    answer = ZERO
    for (i, j), (k, l) in (((0, 1), (2, 3)),
                           ((0, 2), (1, 3)),
                           ((0, 3), (1, 2))):
        answer += (block_entry(blocks, i, j, bits[i], bits[j])
                   * block_entry(blocks, k, l, bits[k], bits[l]))
    return answer


def raw_action_index(raw_index, permutation, flips):
    edge_index, position = divmod(raw_index, 4)
    i, j = SUPER_EDGES[edge_index]
    clone_i, clone_j = divmod(position, 2)
    image = {
        permutation[i]: clone_i ^ flips[permutation[i]],
        permutation[j]: clone_j ^ flips[permutation[j]],
    }
    new_i, new_j = sorted(image)
    new_position = 2 * image[new_i] + image[new_j]
    return 4 * EDGE_INDEX[(new_i, new_j)] + new_position


def q_action_index(value, permutation, flips):
    old = tuple((value >> (3 - site)) & 1 for site in range(4))
    new = [0] * 4
    for site in range(4):
        new[permutation[site]] = old[site] ^ flips[permutation[site]]
    return sum(new[site] << (3 - site) for site in range(4))


def act_support(support, index_action, permutation, flips):
    return frozenset(index_action(value, permutation, flips)
                     for value in support)


def main():
    sigma = -Z - 2
    b = (Z, sigma, ONE, sigma, ONE, ONE)
    c = (sigma, Z, -ONE, Z, -ONE, -ONE)
    require(tuple(b[index] * c[index] for index in range(6))
            == (-ONE,) * 6, "the Laurent block inverse relation changed")
    blocks = tuple((ZERO, b[index], c[index], ZERO)
                   for index in range(6))

    permanent_rows = tuple(ONE + permanent(block) for block in blocks)
    triangle_rows = tuple(
        ONE + permanent(blocks[EDGE_INDEX[(i, j)]])
        + permanent(blocks[EDGE_INDEX[(i, k)]])
        + permanent(blocks[EDGE_INDEX[(j, k)]])
        + triangle(blocks, i, j, k)
        for i, j, k in combinations(range(4), 3)
    )
    h_value = hafnian_on(blocks, range(8))
    cofactors = tuple(cofactor(blocks, raw_index)
                      for raw_index in range(24))
    selected_cofactor_indices = tuple(
        4 * edge + position
        for edge in range(6)
        for position in ((1, 2) if (BRANCH_MASK >> edge) & 1 else (0, 3))
    )
    q_values = tuple(q_value(blocks, value) for value in range(16))

    require(not any(permanent_rows), "a permanent row is nonzero")
    require(not any(triangle_rows), "a triangle row is nonzero")
    require(not any(cofactors[index]
                    for index in selected_cofactor_indices),
            "a selected cofactor is nonzero")
    require(h_value == as_k(4) and h_value != ZERO,
            "the pure Hafnian value changed")

    expected_q = {
        3: -4 - 2 * Z,
        5: 2 * Z,
        6: as_k(2),
        9: as_k(-2),
        10: 4 + 2 * Z,
        12: -2 * Z,
    }
    actual_q = {index: value for index, value in enumerate(q_values) if value}
    require(actual_q == expected_q,
            f"the literal Q values changed: {actual_q!r}")

    x_support = frozenset(index for index in range(24)
                          if blocks[index // 4][index % 4])
    c_support = frozenset(index for index, value in enumerate(cofactors)
                          if value)
    q_support = frozenset(expected_q)
    require(x_support == frozenset(
        4 * edge + position for edge in range(6) for position in (1, 2)),
        "cell support changed")
    require(c_support == frozenset((9, 10, 13, 14)),
            "cofactor support changed")

    actions = tuple((permutation, flips)
                    for permutation in permutations(range(4))
                    for flips in product((0, 1), repeat=4))
    records = frozenset(
        (act_support(x_support, raw_action_index, *action),
         act_support(c_support, raw_action_index, *action),
         act_support(q_support, q_action_index, *action))
        for action in actions
    )
    require(len(actions) == 384 and len(records) == 24,
            "joint orbit census changed")

    def q_ok(left, right):
        return left[2].isdisjoint(frozenset(15 - q for q in right[2]))

    def left_cofactor_ok(left, right):
        return right[0].isdisjoint(left[1])

    def right_cofactor_ok(left, right):
        return left[0].isdisjoint(right[1])

    pairs = tuple(product(records, repeat=2))
    counts = {
        "q_only": sum(q_ok(left, right) for left, right in pairs),
        "left_cofactor_only": sum(left_cofactor_ok(left, right)
                                    for left, right in pairs),
        "right_cofactor_only": sum(right_cofactor_ok(left, right)
                                     for left, right in pairs),
        "q_and_left_cofactor": sum(q_ok(left, right)
                                     and left_cofactor_ok(left, right)
                                     for left, right in pairs),
        "q_and_right_cofactor": sum(q_ok(left, right)
                                      and right_cofactor_ok(left, right)
                                      for left, right in pairs),
        "all_three": sum(q_ok(left, right)
                           and left_cofactor_ok(left, right)
                           and right_cofactor_ok(left, right)
                           for left, right in pairs),
    }
    require(counts["q_only"] == 288,
            "Q-only compatibility census changed")
    require(counts["q_and_left_cofactor"] == 0
            and counts["q_and_right_cofactor"] == 0,
            "a Q-compatible pair passed a one-sided cofactor condition")
    require(counts["all_three"] == 0,
            "a transformed pair passed all diagonal packet conditions")

    # Hostile mutation: dropping the 6+2 cofactor packet leaves all 288
    # Q-compatible ordered pairs alive, while reinstating either direction
    # kills them all.

    result = {
        "status": "UNAUDITED exact support-six component referee",
        "number_field": "Q(z), z^2+2z-1=0",
        "branch_mask": BRANCH_MASK,
        "blocks": "M_e=[[0,b_e],[-1/b_e,0]]",
        "b_01_02_03_12_13_23": [
            value.encode() for value in b
        ],
        "pure_hafnian": h_value.encode(),
        "q_values": {str(index): value.encode()
                     for index, value in expected_q.items()},
        "x_support": sorted(x_support),
        "cofactor_support": sorted(c_support),
        "q_support": sorted(q_support),
        "selected_cofactor_indices": list(selected_cofactor_indices),
        "permanent_rows_zero": len(permanent_rows),
        "triangle_rows_zero": len(triangle_rows),
        "selected_cofactor_rows_zero": len(selected_cofactor_indices),
        "action_count": len(actions),
        "joint_orbit_size": len(records),
        "ordered_pairs_tested": len(pairs),
        "compatibility_counts": counts,
        "pair_conditions": [
            "Q_A intersect complement(Q_B) is empty",
            "X_B intersect C_A is empty",
            "X_A intersect C_B is empty",
        ],
        "scope": (
            "This proves one exact H-live one-colour component and excludes "
            "pairs whose two colours both lie in its full B4 joint-support "
            "orbit. It does not classify every component of the diagonal "
            "packet."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("support-six component pairwise obstruction: PASS")
    print("H / X,C,Q supports:", h_value, len(x_support), len(c_support),
          len(q_support))
    print("actions / joint orbit / pairs:", len(actions), len(records),
          len(pairs))
    print("compatibility counts:", counts)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
