#!/usr/bin/env python3
"""Exact generic signature of the surviving (B,T,D)=(0,30,12) family."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import combinations, permutations, product
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_face_03012_component_signature.json"
CORE_PATH = (HERE.parent /
             "unaudited-codex-n8-orbit0-normalized-78-2026-08-20" /
             "audit_polarized_superpair_core_identity.py")
EDGES = tuple(combinations(range(4), 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


CORE = load("n8_face_03012_mate_core", CORE_PATH)


def trim(poly):
    values = list(poly)
    while len(values) > 1 and values[-1] == 0:
        values.pop()
    return tuple(values) if values else (Fraction(0),)


def padd(left, right):
    answer = [Fraction(0)] * max(len(left), len(right))
    for index in range(len(left)):
        answer[index] += left[index]
    for index in range(len(right)):
        answer[index] += right[index]
    return trim(answer)


def pneg(poly):
    return trim(tuple(-value for value in poly))


def pmul(left, right):
    answer = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            answer[i + j] += a * b
    return trim(answer)


def pdivmod(numerator, denominator):
    numerator = list(trim(numerator))
    denominator = trim(denominator)
    require(denominator != (0,), "zero polynomial denominator")
    quotient = [Fraction(0)] * max(1, len(numerator) - len(denominator) + 1)
    while len(numerator) >= len(denominator) and any(numerator):
        shift = len(numerator) - len(denominator)
        coefficient = numerator[-1] / denominator[-1]
        quotient[shift] += coefficient
        for index, value in enumerate(denominator):
            numerator[index + shift] -= coefficient * value
        numerator = list(trim(numerator))
    return trim(quotient), trim(numerator)


def pgcd(left, right):
    left, right = trim(left), trim(right)
    while right != (0,):
        _, remainder = pdivmod(left, right)
        left, right = right, remainder
    if left == (0,):
        return (Fraction(1),)
    lead = left[-1]
    return trim(tuple(value / lead for value in left))


def pexact_div(numerator, denominator):
    quotient, remainder = pdivmod(numerator, denominator)
    require(remainder == (0,), "nonexact polynomial division")
    return quotient


@dataclass(frozen=True)
class Rat:
    num: tuple = (Fraction(0),)
    den: tuple = (Fraction(1),)

    def __post_init__(self):
        num, den = trim(self.num), trim(self.den)
        require(den != (0,), "zero rational-function denominator")
        if num == (0,):
            object.__setattr__(self, "num", (Fraction(0),))
            object.__setattr__(self, "den", (Fraction(1),))
            return
        gcd = pgcd(num, den)
        num, den = pexact_div(num, gcd), pexact_div(den, gcd)
        lead = den[-1]
        num = trim(tuple(value / lead for value in num))
        den = trim(tuple(value / lead for value in den))
        object.__setattr__(self, "num", num)
        object.__setattr__(self, "den", den)

    def __add__(self, other):
        other = as_rat(other)
        return Rat(padd(pmul(self.num, other.den),
                        pmul(other.num, self.den)),
                   pmul(self.den, other.den))

    __radd__ = __add__

    def __neg__(self):
        return Rat(pneg(self.num), self.den)

    def __sub__(self, other):
        return self + (-as_rat(other))

    def __rsub__(self, other):
        return as_rat(other) - self

    def __mul__(self, other):
        other = as_rat(other)
        return Rat(pmul(self.num, other.num), pmul(self.den, other.den))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = as_rat(other)
        require(other.num != (0,), "division by zero rational function")
        return Rat(pmul(self.num, other.den), pmul(self.den, other.num))

    def __bool__(self):
        return self.num != (0,)

    def encode(self):
        def encode_poly(poly):
            return [[value.numerator, value.denominator] for value in poly]
        return {"numerator_coefficients_low_to_high": encode_poly(self.num),
                "denominator_coefficients_low_to_high": encode_poly(self.den)}


def as_rat(value):
    if isinstance(value, Rat):
        return value
    return Rat((Fraction(value),))


ZERO, ONE = as_rat(0), as_rat(1)
R = Rat((Fraction(0), Fraction(1)))
Q = R * R - 2 * R - 1


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


def hafnian(blocks, vertices):
    answer = ZERO
    for matching in perfect_matchings(tuple(vertices)):
        term = ONE
        for left, right in matching:
            term *= graph_entry(blocks, left, right)
        answer += term
    return answer


def cofactor(blocks, raw_index):
    edge, position = divmod(raw_index, 4)
    i, j = EDGES[edge]
    ci, cj = divmod(position, 2)
    removed = {2 * i + ci, 2 * j + cj}
    return hafnian(blocks, (vertex for vertex in range(8)
                            if vertex not in removed))


def permanent(block):
    return block[0] * block[3] + block[1] * block[2]


def triangle(blocks, i, j, k):
    answer = ZERO
    for ci, cj, ck in product((0, 1), repeat=3):
        answer += (block_entry(blocks, i, j, ci, cj)
                   * block_entry(blocks, i, k, 1 - ci, ck)
                   * block_entry(blocks, j, k, 1 - cj, 1 - ck))
    return answer


def q_value(blocks, value):
    bits = tuple((value >> (3 - site)) & 1 for site in range(4))
    return sum((block_entry(blocks, i, j, bits[i], bits[j])
                * block_entry(blocks, k, l, bits[k], bits[l])
                for (i, j), (k, l) in (((0, 1), (2, 3)),
                                        ((0, 2), (1, 3)),
                                        ((0, 3), (1, 2)))), ZERO)


def raw_action_index(raw_index, permutation, flips):
    edge, position = divmod(raw_index, 4)
    i, j = EDGES[edge]
    ci, cj = divmod(position, 2)
    image = {permutation[i]: ci ^ flips[permutation[i]],
             permutation[j]: cj ^ flips[permutation[j]]}
    ni, nj = sorted(image)
    return 4 * EDGE_INDEX[(ni, nj)] + 2 * image[ni] + image[nj]


def q_action_index(value, permutation, flips):
    old = tuple((value >> (3 - site)) & 1 for site in range(4))
    new = [0] * 4
    for site in range(4):
        new[permutation[site]] = old[site] ^ flips[permutation[site]]
    return sum(new[site] << (3 - site) for site in range(4))


def act_support(support, action, index_action):
    return frozenset(index_action(value, *action) for value in support)


def main():
    a2 = R * (2 - R)
    blocks = (
        (-R / Q, ZERO, ZERO, Q / R),
        (ZERO, ONE, -ONE, ZERO),
        (a2, ONE, Q, ONE),
        (a2 / Q, ONE, Q, Q),
        (ZERO, ONE / Q, -Q, ZERO),
        (R, ZERO, ZERO, -ONE / R),
    )
    permanent_rows = tuple(ONE + permanent(block) for block in blocks)
    triangle_rows = tuple(
        ONE + permanent(blocks[EDGE_INDEX[(i, j)]])
        + permanent(blocks[EDGE_INDEX[(i, k)]])
        + permanent(blocks[EDGE_INDEX[(j, k)]])
        + triangle(blocks, i, j, k)
        for i, j, k in combinations(range(4), 3)
    )
    cofactors = tuple(cofactor(blocks, index) for index in range(24))
    selected_cofactors = tuple(4 * edge + position
                               for edge in range(6)
                               for position in (0, 3))
    q_values = tuple(q_value(blocks, value) for value in range(16))
    h_value = hafnian(blocks, range(8))
    require(not any(permanent_rows), "a permanent row is nonzero")
    require(not any(triangle_rows), "a triangle row is nonzero")
    require(not any(cofactors[index] for index in selected_cofactors),
            "a selected branch0 cofactor is nonzero")
    expected_h = 4 * R * (R - 2)
    require(h_value == expected_h,
            f"generic H formula changed: {h_value.encode()} != "
            f"{expected_h.encode()}")

    x_support = frozenset(index for index in range(24)
                          if blocks[index // 4][index % 4])
    c_support = frozenset(index for index, value in enumerate(cofactors)
                          if value)
    q_support = frozenset(index for index, value in enumerate(q_values)
                          if value)
    require(q_support == frozenset(range(16)),
            "the survivor no longer has full Q support")

    # Exact arbitrary-mate closure.  Full left Q support makes the packet
    # compatibility condition force every right Q coordinate to zero.  The
    # polarized pure-H identity then kills the mate's H once its literal
    # pair and triangle rows also vanish.
    core_h = CORE.pure_hafnian()
    core_rhs = CORE.add(
        *(CORE.t_triple(*triple) for triple in combinations(range(4), 3)),
        *(CORE.b_self(bits) for bits in CORE.ORIENTATIONS),
        CORE.scale(CORE.add(*(
            CORE.multiply(CORE.e_pair(*left), CORE.e_pair(*right))
            for left, right in CORE.COMPLEMENTARY_EDGE_PAIRS)), -1),
    )
    require(core_h == core_rhs, "polarized mate identity changed")
    actions = tuple((permutation, flips)
                    for permutation in permutations(range(4))
                    for flips in product((0, 1), repeat=4))
    signatures = frozenset(
        (act_support(x_support, action, raw_action_index),
         act_support(c_support, action, raw_action_index),
         act_support(q_support, action, q_action_index))
        for action in actions
    )

    def compatible(left, right):
        return (left[2].isdisjoint(frozenset(15 - q for q in right[2]))
                and right[0].isdisjoint(left[1])
                and left[0].isdisjoint(right[1]))

    compatible_self_pairs = sum(compatible(left, right)
                                for left, right in product(signatures,
                                                           repeat=2))
    result = {
        "status": "UNAUDITED exact generic (0,30,12) component signature",
        "parameter": "r",
        "q": "r^2-2*r-1",
        "open_conditions": ["r!=0", "r!=2", "q!=0"],
        "blocks_edge_order_01_02_03_12_13_23": [
            [value.encode() for value in block] for block in blocks
        ],
        "pure_H": h_value.encode(),
        "pure_H_formula": "4*r*(r-2)",
        "permanent_rows_zero": len(permanent_rows),
        "triangle_rows_zero": len(triangle_rows),
        "selected_branch0_cofactor_rows_zero": len(selected_cofactors),
        "x_support": sorted(x_support),
        "cofactor_support": sorted(c_support),
        "q_support": sorted(q_support),
        "q_values": {str(index): value.encode()
                     for index, value in enumerate(q_values) if value},
        "signature_sizes_X_C_Q": [len(x_support), len(c_support),
                                    len(q_support)],
        "B4_action_count": len(actions),
        "joint_signature_orbit_size": len(signatures),
        "ordered_self_pairs": len(signatures) ** 2,
        "compatible_self_pairs": compatible_self_pairs,
        "arbitrary_mate_obstruction": {
            "forced_zero_Q_indices": list(range(16)),
            "identity": (
                "H=sum_{triples}t + sum_{s0=0}Q_s*Q_bar(s) "
                "- sum_{complementary edges}e_e*e_f"
            ),
            "identity_rebuilt_exactly": True,
            "conclusion": (
                "mate e=t=0 and all Q_s=0 imply mate H=0, contrary to "
                "the H-live source requirement"
            ),
        },
        "scope_guard": (
            "The support calculation is generic on the stated open set. "
            "The arbitrary-mate conclusion uses full Q support plus the "
            "literal polarized H identity; it does not assume a mate branch."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("(0,30,12) exact component signature: PASS")
    print("X/C/Q:", sorted(x_support), sorted(c_support), sorted(q_support))
    print("sizes / orbit / compatible self pairs:",
          result["signature_sizes_X_C_Q"], len(signatures),
          compatible_self_pairs)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
