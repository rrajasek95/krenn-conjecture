#!/usr/bin/env python3
"""Exact rank-restoration boundary for an outside k=3 endpoint component.

Choose one nonzero pure matching in each target colour.  An endpoint arm
outside their union has selected deleted-star ranks (3,3).  If its complete
two-response column is nonzero, a literal summand makes that arm active.

Pair it with a selected arm of the opposite response colour.  For a deleted
physical pair f, the selected-matching rank at either endpoint is exactly
the number of target colours having a nonzero pure matching which avoids f.
Thus the mate is good iff every colour lost on f has an avoiding matching.
An alternate diagonal target matching supplies the corresponding repair;
for colour zero the ordinary hafnian expansion supplies either an avoiding
unary matching or the exact unary-coloop residual q_f H_f=1.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_hall_k22_outside_endpoint_component_wedge.py":
        "59dd21c4664e8ccd88f771d0191d3db32e5fdb832e2c6de1f169cb197f9a3038",
    "notes/uniform-hall-k22-outside-endpoint-component-wedge.md":
        "cd3807d8f3f4f3d8ccda38e23c5ff291d3f0e3f1a33b69f3d2ef061b117d3347",
    "computations/verify_uniform_multisite_endpoint_affine_hall_concentration_boundary.py":
        "f24e9bd69ec4baef96104557571c154b399f87f34074edffda27e551f33c2205",
    "notes/uniform-multisite-endpoint-affine-hall-concentration-boundary.md":
        "241b46d9ecede656aa59f2be6d74bc288fbada2aa4843103a950441066763df2",
    "computations/verify_uniform_hall_triangle_bridge_dark_unary_reselection.py":
        "ad1c2f890bdf207add20c6524eb5c91f5925aef8aed77f26f290491a4bb937d6",
    "notes/uniform-hall-triangle-bridge-dark-unary-reselection.md":
        "3985d1e9fad83e773fc00acdd71a398cb10698d6a7207f247d561f454f293453",
    "computations/verify_uniform_one_bad_axis_hessian_carrier_circuit_boundary.py":
        "1594dcac16bb77bb929c18edda224e215ea99697bfd36edabc4230a0d341b5c8",
    "notes/uniform-one-bad-axis-hessian-carrier-circuit-boundary.md":
        "d784f8d25461ffcdafcc3fb9a39ccc776f770fb63359f722bead4fe7c965e73e",
}
EXPECTED_LEDGER_SHA256 = (
    "7acbb1bfdc0d59ce4bc79138cb0aff60536304c9c1bb7145292ded123e1990d5"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge(left, right):
    return tuple(sorted((left, right)))


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remainder):
            yield tuple(sorted((edge(first, second),) + tail))


def partner(matching, site):
    for left, right in matching:
        if left == site:
            return right
        if right == site:
            return left
    raise RuntimeError((matching, site))


def rank(matrix):
    matrix = [[Q(value) for value in row] for row in matrix]
    pivot_row = 0
    for column in range(len(matrix[0]) if matrix else 0):
        pivot = next((row for row in range(pivot_row, len(matrix))
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [entry - value * pivot_entry
                           for entry, pivot_entry
                           in zip(matrix[row], matrix[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def avoiding_matching(family, deleted):
    return next((matching for matching in family if deleted not in matching),
                None)


def selected_rank_from_families(families, deleted, endpoint):
    """Rank certified by one avoiding pure matching in each colour."""
    other = deleted[0] if endpoint == deleted[1] else deleted[1]
    columns = []
    for colour, family in enumerate(families):
        matching = avoiding_matching(family, deleted)
        if matching is None:
            continue
        neighbour = partner(matching, endpoint)
        require(neighbour != other,
                "an alleged avoiding matching still used the deleted pair")
        # (neighbour, colour) is a literal coordinate in the deleted star.
        columns.append((neighbour, colour))
    rows = tuple(sorted(set(columns)))
    matrix = [[Q(int(item == row)) for item in columns] for row in rows]
    return rank(matrix), tuple(columns)


def audit_rank_restoration_theorem():
    matchings = tuple(perfect_matchings(range(8)))
    require(len(matchings) == 105, "the K8 matching count changed")

    q0 = ((0, 1), (2, 3), (4, 5), (6, 7))
    q1 = ((0, 2), (1, 3), (4, 6), (5, 7))
    q2 = ((0, 3), (1, 2), (4, 7), (5, 6))
    selected = (q0, q1, q2)
    outer = 6

    # The new occupied arm 06 is outside all three displayed ports at 6.
    outside = edge(outer, 0)
    require(all(outside not in matching for matching in selected),
            "the canonical outside arm entered the selected anchor union")
    singleton_families = tuple((matching,) for matching in selected)
    outside_ranks = tuple(selected_rank_from_families(
        singleton_families, outside, endpoint)[0] for endpoint in outside)
    require(outside_ranks == (3, 3),
            f"the outside arm lost goodness: {outside_ranks}")

    # Pair colour 1 on 06 with the selected colour-2 arm 56.  Q2 loses its
    # column on deletion; the displayed alternate Q2' avoids 56 and repairs
    # it at both endpoints.  Q0,Q1 already avoid 56.
    mate = edge(outer, partner(q2, outer))
    require(mate == (5, 6), "the canonical opposite arm changed")
    q2_alt = ((0, 5), (1, 6), (2, 4), (3, 7))
    require(q2_alt in matchings and mate not in q2_alt,
            "the alternate colour-2 matching stopped repairing the mate")
    repaired_families = ((q0,), (q1,), (q2, q2_alt))
    mate_ranks = tuple(selected_rank_from_families(
        repaired_families, mate, endpoint)[0] for endpoint in mate)
    require(mate_ranks == (3, 3),
            f"the selected opposite arm lost rank restoration: {mate_ranks}")

    # The criterion is exact in the selected-matching coordinate module:
    # distinct target colours occupy disjoint coordinate rows, so its rank
    # is precisely the number of colours with an avoiding matching.
    audits = 0
    for deleted in combinations(range(8), 2):
        deleted = edge(*deleted)
        families = []
        for colour, chosen in enumerate(selected):
            alternate = next((matching for matching in matchings
                              if deleted not in matching
                              and matching != chosen
                              and partner(matching, colour) !=
                              partner(chosen, colour)), None)
            family = ((chosen, alternate) if alternate is not None
                      else (chosen,))
            families.append(tuple(item for item in family if item is not None))
        expected = sum(avoiding_matching(family, deleted) is not None
                       for family in families)
        for endpoint in deleted:
            actual, _columns = selected_rank_from_families(
                tuple(families), deleted, endpoint)
            require(actual == expected,
                    "rank stopped counting repairable target colours")
            audits += 1

    # Removing Q2' gives the sharp rank-two coloop boundary at mate=56.
    coloop_families = ((q0,), (q1,), (q2,))
    coloop_ranks = tuple(selected_rank_from_families(
        coloop_families, mate, endpoint)[0] for endpoint in mate)
    require(coloop_ranks == (2, 2),
            f"the selected-matching coloop boundary changed: {coloop_ranks}")

    return {
        "canonical_outside_arm": outside,
        "outside_deleted_star_ranks": outside_ranks,
        "selected_opposite_arm": mate,
        "alternate_colour_two_matching": q2_alt,
        "repaired_mate_ranks": mate_ranks,
        "endpoint_rank_audits": audits,
        "rank_formula": (
            "rank at either deleted endpoint equals the number of target "
            "colours having a nonzero pure matching which avoids the pair"
        ),
        "unrepaired_coloop_ranks": coloop_ranks,
        "distinct_head_minor_abs": 1,
    }


def audit_complete_column_and_target_recursions():
    # One endpoint component affects exactly its two complete response rows.
    # This pins the finite deletion and the nonzero-literal-summand branch.
    deletion = {
        "zero_complete_column": (
            "delete the occupied component exactly; all five source "
            "tensors remain unchanged"
        ),
        "nonzero_complete_column": (
            "choose a nonzero output coefficient and literal matching "
            "summand; its outside endpoint arm is support-active"
        ),
    }

    # Unary matchings partition by the mate of a chosen site.  This is the
    # coefficient-level Euler recursion.  The audit is combinatorial and
    # holds with arbitrary coefficients after inserting their monomials.
    matchings = tuple(perfect_matchings(range(8)))
    a = 0
    blocks = {
        b: tuple(matching for matching in matchings if edge(a, b) in matching)
        for b in range(1, 8)
    }
    require(sum(len(block) for block in blocks.values()) == len(matchings)
            and all(len(block) == 15 for block in blocks.values()),
            "the unary matching recursion stopped being a disjoint partition")

    # A scalar specialization realizes both outcomes of the exact recursion
    # 1=sum_b U_ab.  An avoiding nonzero block gives an alternate unary
    # matching.  If every avoiding block is zero, the selected edge is a
    # unary coloop and its block is exactly one.
    selected_b = 1
    alternate_values = {b: Q(int(b == 2)) for b in range(1, 8)}
    alternate_values[selected_b] = Q(0)
    require(sum(alternate_values.values()) == 1,
            "the alternate unary specialization changed")
    coloop_values = {b: Q(int(b == selected_b)) for b in range(1, 8)}
    require(sum(coloop_values.values()) == 1
            and all(not value for b, value in coloop_values.items()
                    if b != selected_b),
            "the unary-coloop specialization changed")

    return {
        "complete_column_dichotomy": deletion,
        "unary_expansion": "1=sum_{b!=a} q_ab^00 H_ab^0",
        "unary_matching_blocks": {str(b): len(block)
                                  for b, block in blocks.items()},
        "alternate_unary_outcome": (
            "some avoiding block is nonzero, so choose one of its literal "
            "matching summands to repair colour zero"
        ),
        "unary_coloop_outcome": (
            "all avoiding blocks vanish and q_ab^00 H_ab^0=1"
        ),
        "diagonal_analogue": (
            "the pure diagonal target coefficient partitions by endpoint "
            "port; a nonzero avoiding block supplies an alternate target "
            "matching, while failure is a normalized diagonal port coloop"
        ),
    }


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def main():
    pin_dependencies()
    ledger = {
        "pins": PINS,
        "rank_restoration": audit_rank_restoration_theorem(),
        "source_recursions": audit_complete_column_and_target_recursions(),
        "uniform_lemma": (
            "at a minimum-support k=3 response circuit, an occupied "
            "endpoint component outside the chosen three-colour port union "
            "has nonzero complete column and hence a literal active arm. "
            "Pairing it with a selected opposite-colour arm gives a "
            "distinct-head four-good wedge exactly when every target colour "
            "using the mate edge has a nonzero pure matching avoiding it"
        ),
        "repair_routes": (
            "an alternate diagonal target matching repairs a lost diagonal "
            "colour; unary matching expansion repairs colour zero unless "
            "the mate edge is a unary coloop"
        ),
        "sharp_boundary": (
            "if repair fails, the selected opposite arm is a target-family "
            "coloop and its selected-matching deleted-star rank is at most "
            "two.  Extra source columns may raise that rank; excluding the "
            "coloop or proving such a raise requires a complete crossed-row "
            "identity.  Minimum support and Hessian provenance alone do not"
        ),
        "scope": (
            "uniform complete-column and matching-family rank theorem, not "
            "a proof that every k=3 affine circuit has an outside component "
            "or that the remaining full-five-row coloop packet is empty"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"axis-circuit outside restoration ledger changed: {digest}")
    print("uniform k3 outside endpoint rank restoration: PASS")
    print("outside complete column -> deletion or literal active arm")
    print("mate rank = number of target colours with avoiding pure matching")
    print("failure = normalized target-family coloop; full crossed row remains")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
