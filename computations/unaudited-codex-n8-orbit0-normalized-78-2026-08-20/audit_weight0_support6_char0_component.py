#!/usr/bin/env python3
"""Exact support-six char-zero component and its full B4 packet orbit.

This supplies a literal point on both apparent seven-support deletion ideals
from ``analyze_weight0_dzero_lowq_chart.py``.  It also checks that support-only
Q compatibility is misleading: every Q-compatible transformed pair violates
both directions of the 6+2 entry/cofactor packet.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import permutations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SCREEN_PATH = HERE / "screen_lowq_joint_branch_orbits.py"
OUT = HERE / "results_weight0_support6_char0_component.json"
Q = Fraction
ZERO = (Q(0), Q(0))
ONE = (Q(1), Q(0))
Z = (Q(0), Q(1))
PERFECT_MATCHINGS_4 = (
    ((0, 1), (2, 3)),
    ((0, 2), (1, 3)),
    ((0, 3), (1, 2)),
)


def load_screen():
    spec = importlib.util.spec_from_file_location("n8_support6_screen",
                                                  SCREEN_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SCREEN = load_screen()


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def k_add(*values):
    return (sum(value[0] for value in values),
            sum(value[1] for value in values))


def k_neg(value):
    return (-value[0], -value[1])


def k_mul(left, right):
    # z^2 = 1-2z.
    return (left[0] * right[0] + left[1] * right[1],
            left[0] * right[1] + left[1] * right[0]
            - 2 * left[1] * right[1])


def k_string(value):
    return f"({value[0]})+({value[1]})*z"


def evaluate(poly, entries):
    answer = ZERO
    for monomial, integer_coefficient in poly.items():
        term = (Q(integer_coefficient), Q(0))
        for variable in monomial:
            term = k_mul(term, entries[variable])
        answer = k_add(answer, term)
    return answer


def derivative(poly, variable):
    answer = {}
    for monomial, coefficient in poly.items():
        multiplicity = monomial.count(variable)
        if not multiplicity:
            continue
        reduced = list(monomial)
        reduced.remove(variable)
        reduced = tuple(reduced)
        answer[reduced] = answer.get(reduced, 0) + coefficient * multiplicity
    return {monomial: coefficient for monomial, coefficient in answer.items()
            if coefficient}


def raw_entries():
    minus_one = (Q(-1), Q(0))
    minus_z_minus_two = (Q(-2), Q(-1))
    b_values = (Z, minus_z_minus_two, ONE, minus_z_minus_two, ONE, ONE)
    # -1/b values, reduced using z(z+2)=1.
    c_values = (minus_z_minus_two, Z, minus_one, Z, minus_one, minus_one)
    entries = []
    for b_value, c_value in zip(b_values, c_values):
        require(k_mul(b_value, c_value) == minus_one,
                "block anti-product ceased to be -1")
        entries.extend((ZERO, b_value, c_value, ZERO))
    return tuple(entries)


def entry_action(raw_variable, permutation, flips):
    edge_index, block_entry = divmod(raw_variable, 4)
    left, right = SCREEN.EDGES[edge_index]
    left_clone, right_clone = divmod(block_entry, 2)
    new_left, new_right = permutation[left], permutation[right]
    new_left_clone = left_clone ^ flips[new_left]
    new_right_clone = right_clone ^ flips[new_right]
    if new_left < new_right:
        new_edge = (new_left, new_right)
        new_entry = 2 * new_left_clone + new_right_clone
    else:
        new_edge = (new_right, new_left)
        new_entry = 2 * new_right_clone + new_left_clone
    return 4 * SCREEN.EDGE_INDEX[new_edge] + new_entry


def act_mask(mask, count, action_function, action):
    return sum(1 << action_function(index, *action)
               for index in range(count) if mask & (1 << index))


def q_complement_mask(mask):
    return sum(1 << (15 - index) for index in range(16)
               if mask & (1 << index))


def main():
    entries = raw_entries()
    base_polys, hafnian_poly = SCREEN.PROBE.equations(
        SCREEN.branch_bits(51))
    base_values = tuple(evaluate(poly, entries) for poly in base_polys)
    require(all(value == ZERO for value in base_values),
            "a raw base equation failed")

    q_values = tuple(evaluate(SCREEN.q_poly(index), entries)
                     for index in range(16))
    hafnian = evaluate(hafnian_poly, entries)
    expected_hafnian = (Q(4), Q(0))
    require(hafnian == expected_hafnian and hafnian != ZERO,
            "pure Hafnian changed")
    q_support = frozenset(index for index, value in enumerate(q_values)
                          if value != ZERO)
    require(q_support == {3, 5, 6, 9, 10, 12},
            "support-six pattern changed")

    cofactors = tuple(evaluate(derivative(hafnian_poly, variable), entries)
                      for variable in range(24))
    entry_mask = sum((value != ZERO) << index
                     for index, value in enumerate(entries))
    cofactor_mask = sum((value != ZERO) << index
                        for index, value in enumerate(cofactors))
    q_mask = sum((value != ZERO) << index
                 for index, value in enumerate(q_values))
    require(entry_mask == 6710886 and cofactor_mask == 26112
            and q_mask == 5736, "literal support masks changed")

    actions = tuple((permutation, flips)
                    for permutation in permutations(range(4))
                    for flips in product((0, 1), repeat=4))
    joint_orbit = frozenset((
        act_mask(entry_mask, 24, entry_action, action),
        act_mask(cofactor_mask, 24, entry_action, action),
        act_mask(q_mask, 16, SCREEN.act_index, action),
    ) for action in actions)
    support_orbit = frozenset(record[2] for record in joint_orbit)
    require(len(joint_orbit) == 24 and len(support_orbit) == 8,
            "B4 orbit sizes changed")
    support8_seed = sum(1 << index
                        for index in (1, 3, 4, 5, 6, 9, 10, 12))
    support8_orbit = frozenset(
        act_mask(support8_seed, 16, SCREEN.act_index, action)
        for action in actions
    )
    require(len(support8_orbit) == 96,
            "support-eight control orbit changed")

    support_only_compatible = 0
    joint_q_compatible = 0
    full_packet_compatible = 0
    q_compatible_both_cofactor_fail = 0
    for left in joint_orbit:
        for right in joint_orbit:
            q_ok = not (left[2] & q_complement_mask(right[2]))
            left_entry_right_cofactor = not (left[0] & right[1])
            right_entry_left_cofactor = not (right[0] & left[1])
            joint_q_compatible += q_ok
            full_packet_compatible += (
                q_ok and left_entry_right_cofactor
                and right_entry_left_cofactor
            )
            q_compatible_both_cofactor_fail += (
                q_ok and not left_entry_right_cofactor
                and not right_entry_left_cofactor
            )
    for left in support_orbit:
        for right in support_orbit:
            support_only_compatible += not (
                left & q_complement_mask(right))
    support6_to_support8_compatible = sum(
        not (left & q_complement_mask(right))
        for left in support_orbit for right in support8_orbit
    )
    support8_to_support6_compatible = sum(
        not (left & q_complement_mask(right))
        for left in support8_orbit for right in support_orbit
    )

    require(support_only_compatible == 32,
            "support-only must-fire control changed")
    require(support6_to_support8_compatible == 0
            and support8_to_support6_compatible == 0,
            "support-six/eight cross-orbit obstruction changed")
    require(joint_q_compatible == 288
            and q_compatible_both_cofactor_fail == 288,
            "joint Q/cofactor census changed")
    require(full_packet_compatible == 0,
            "a full packet-compatible pair unexpectedly appeared")

    # Human-size explanation of the 0/576 result.  The support-six mask is
    # exactly the weight-two layer of F_2^4.  Relative endpoint flips delta
    # make two such masks disjoint exactly when wt(delta) is odd.  But for an
    # odd cut every perfect matching of four vertices has exactly one crossing
    # edge, never two.  A two-edge cofactor matching therefore necessarily
    # shares one block orientation with the other graph's all-edge X support.
    middle_layer = frozenset(index for index in range(16)
                             if index.bit_count() == 2)
    require(q_mask == sum(1 << index for index in middle_layer),
            "support-six mask ceased to be the middle Boolean layer")
    relative_flip_rows = []
    for delta in range(16):
        translated = frozenset(index ^ delta for index in middle_layer)
        disjoint = middle_layer.isdisjoint(translated)
        odd = delta.bit_count() % 2 == 1
        require(disjoint == odd,
                "middle-layer relative-flip criterion changed")
        crossing_histogram = []
        for matching in PERFECT_MATCHINGS_4:
            crossing = sum(((delta >> (3 - left)) & 1)
                           != ((delta >> (3 - right)) & 1)
                           for left, right in matching)
            crossing_histogram.append(crossing)
            if odd:
                require(crossing == 1,
                        "odd cut ceased to cross exactly one matching edge")
        relative_flip_rows.append({
            "delta": delta,
            "weight": delta.bit_count(),
            "Q_supports_disjoint": disjoint,
            "crossing_edges_in_three_matchings": crossing_histogram,
        })

    result = {
        "status": "UNAUDITED exact characteristic-zero component/orbit referee",
        "number_field": "Q[z]/(z^2+2z-1)",
        "blocks": (
            "M_e=[[0,b_e],[-1/b_e,0]], "
            "b=(z,-z-2,1,-z-2,1,1)"
        ),
        "base_equation_count": len(base_polys),
        "base_values": [k_string(value) for value in base_values],
        "H": k_string(hafnian),
        "Q_values": [k_string(value) for value in q_values],
        "Q_support": sorted(q_support),
        "entry_nonzero_indices": [index for index in range(24)
                                  if entry_mask & (1 << index)],
        "cofactor_nonzero_indices": [index for index in range(24)
                                     if cofactor_mask & (1 << index)],
        "B4_action_count": len(actions),
        "support_orbit_size": len(support_orbit),
        "joint_X_C_Q_orbit_size": len(joint_orbit),
        "support_orbit_ordered_Q_compatible": support_only_compatible,
        "support8_control_orbit_size": len(support8_orbit),
        "support6_to_support8_ordered_Q_compatible": (
            support6_to_support8_compatible
        ),
        "support8_to_support6_ordered_Q_compatible": (
            support8_to_support6_compatible
        ),
        "joint_orbit_ordered_Q_compatible": joint_q_compatible,
        "joint_Q_compatible_pairs_failing_both_cofactor_directions": (
            q_compatible_both_cofactor_fail
        ),
        "joint_orbit_ordered_full_packet_compatible": full_packet_compatible,
        "relative_flip_packet_explanation": {
            "support_description": "all four-bit words of Hamming weight two",
            "Q_compatibility": "relative endpoint flip has odd Hamming weight",
            "cofactor_obstruction": (
                "an odd 1|3 cut crosses exactly one edge of every perfect "
                "matching, so one cofactor block orientation always meets X"
            ),
            "sixteen_relative_flip_checks": relative_flip_rows,
        },
        "scope": (
            "This refutes a one-colour support>=8 lemma, but its own B4 "
            "orbit supplies no two-colour 78+48+144 diagonal packet point."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("weight0 support-six char0 component: PASS")
    print("H / Q support:", k_string(hafnian), sorted(q_support))
    print("support / joint orbit:", len(support_orbit), len(joint_orbit))
    print("Q-compatible / full packet-compatible:", joint_q_compatible,
          full_packet_compatible)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
