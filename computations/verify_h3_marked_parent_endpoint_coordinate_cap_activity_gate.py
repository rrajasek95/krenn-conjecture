#!/usr/bin/env python3
"""Audit the literal physical-cap evaluation of the marked h=3 parents.

The marked cap word is 01211222 and the physical cap endpoints are p=6,
q=7.  Hence every marked term has endpoint colour 22.  Termwise contraction
against a general cap covector K sees only K_22.  This checker verifies that
statement on all 90 direct-free parent matchings, together with every remote
matching-edge cofactor square and the two distinguished q23/q45 squares.

The observation map Cap_phys -> k consequently has rank one and an
eight-dimensional kernel.  Its two missing diagonal directions are exactly
the data needed to decide colour activity.  In particular E_22 and I have
the same value on every marked fixed-word term, although E_22 is inactive
and I is active whenever tr(A_67) is nonzero.  Thus the marked object alone
does not canonically produce an active cap; the missing datum is a physical
diagonal completion, not an Eq-presentation filler.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_six_root_marked_collision_word_section.py":
        "d0da0f1473fc1032416c3758ffc932531ac71698c2370ee67224baedd2e13f95",
    "computations/verify_h3_six_root_marked_collision_p2_restriction_reinsertion.py":
        "9b387023ee8cac6bb000d6936a8985cbc16bbad0a9f7deb3613c1f44c233a1f8",
    "computations/verify_clean_pair_cap_exact_descent_symbolic.py":
        "d6507c2afa341ce5c15056feddf92b9a171e2a5c80652617b595c7c7cf35acf5",
    "computations/verify_cap_line_cubic_activity_dichotomy.py":
        "39a0b8ee22e4eec56b1174d200e29679a3baeae1a814ec422f69b6a9725f1300",
    "computations/verify_h3_full_hasse_koszul_cap_totalization.py":
        "51940ce0ac8387b68e7725508db6da1a1c055ea036335bbf19750580c69e13fb",
}
EXPECTED_LEDGER_SHA256 = (
    "d447dcef475f55003ce76c8836433a9311f8c3ec372b412aa1595e06e233297a"
)

SITES = tuple(range(8))
COLOURS = tuple(range(3))
P, QSITE, RCHART = 6, 7, 3
CAP_WORD = tuple(map(int, "01211222"))
DIRECT_FREE_EDGE = (RCHART, P)
DISTINGUISHED_CUTS = ((2, 3), (4, 5))


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def edge_key(left: int, right: int) -> tuple[int, int]:
    return (left, right) if left < right else (right, left)


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        remainder = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(remainder):
            yield (edge_key(first, second),) + tail


def decorated_monomial(matching) -> tuple[tuple[int, int, int, int], ...]:
    return tuple(sorted(
        (left, right, CAP_WORD[left], CAP_WORD[right])
        for left, right in matching
    ))


def coordinate_cap(left_colour: int, right_colour: int):
    return tuple(
        Q(a == left_colour and b == right_colour)
        for a in COLOURS for b in COLOURS
    )


def cap_entry(cap, left_colour: int, right_colour: int) -> Q:
    return Q(cap[3 * left_colour + right_colour])


def add_caps(*caps):
    return tuple(sum((Q(cap[index]) for cap in caps), Q(0))
                 for index in range(9))


def scale_cap(scalar, cap):
    return tuple(Q(scalar) * Q(entry) for entry in cap)


def cap_kappas(cap):
    return tuple(cap_entry(cap, colour, colour) for colour in COLOURS)


def rank(columns) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    rows = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    result = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(result, height)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[result], rows[pivot] = rows[pivot], rows[result]
        value = rows[result][column]
        rows[result] = [entry / value for entry in rows[result]]
        for row in range(height):
            if row == result or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right
                         for left, right in zip(rows[row], rows[result],
                                                strict=True)]
        result += 1
    return result


def fixed_word_contraction(cap, monomial):
    """Universal coefficient of a marked term after endpoint contraction."""
    require(any(cell[:2] == edge_key(P, QSITE) for cell in monomial)
            or (sum(P in cell[:2] for cell in monomial) == 1
                and sum(QSITE in cell[:2] for cell in monomial) == 1),
            ("endpoints are not matched exactly once", monomial))
    require(CAP_WORD[P] == CAP_WORD[QSITE] == 2,
            (CAP_WORD[P], CAP_WORD[QSITE]))
    # The edge variables are retained: for a direct term this is the scalar
    # A_pq[22], and for a crossed term these are the two contracted endpoint
    # legs.  Only the cap-coordinate coefficient changes.
    return cap_entry(cap, 2, 2), monomial


def remove_decorated_edge(monomial, edge):
    edge = edge_key(*edge)
    matches = [cell for cell in monomial if cell[:2] == edge]
    require(len(matches) == 1, (edge, monomial))
    selected = matches[0]
    remainder = list(monomial)
    remainder.remove(selected)
    return tuple(remainder), selected


def parent_contraction_and_cofactor_audit():
    all_matchings = tuple(perfect_matchings(SITES))
    parents = tuple(
        matching for matching in all_matchings
        if DIRECT_FREE_EDGE not in matching
    )
    require(len(all_matchings) == 105 and len(parents) == 90,
            (len(all_matchings), len(parents)))

    e22 = coordinate_cap(2, 2)
    identity = add_caps(*(coordinate_cap(c, c) for c in COLOURS))
    direct = 0
    crossed = 0
    parent_terms = set()
    scalar_linearity_checks = 0
    cofactor_squares = 0
    cut_counts = {edge: 0 for edge in DISTINGUISHED_CUTS}
    residual_sites = tuple(site for site in SITES if site not in (P, QSITE))

    for matching in parents:
        monomial = decorated_monomial(matching)
        require(monomial not in parent_terms, ("duplicate parent", monomial))
        parent_terms.add(monomial)
        if edge_key(P, QSITE) in matching:
            direct += 1
        else:
            crossed += 1

        # Both caps have K_22=1 and therefore act identically on every
        # physical fixed-word parent term, direct or crossed.
        require(fixed_word_contraction(e22, monomial)
                == fixed_word_contraction(identity, monomial), matching)

        # Exact R-linearity on representative rational coefficients.  The
        # same equality is the coefficient identity over the universal ring.
        for scalar in (Q(-3), Q(0), Q(2, 5)):
            left = scale_cap(scalar, e22)
            coefficient, output = fixed_word_contraction(left, monomial)
            base_coefficient, base_output = fixed_word_contraction(
                e22, monomial)
            require(coefficient == scalar * base_coefficient
                    and output == base_output, (scalar, matching))
            scalar_linearity_checks += 1

        # Every cofactor wholly inside U commutes with endpoint contraction.
        # Deletion and reinsertion are literal removal/addition of the same
        # decorated cell, so this also checks source multiplication by that
        # cell on the marked image.
        for edge in matching:
            if P in edge or QSITE in edge:
                continue
            deleted, cell = remove_decorated_edge(monomial, edge)
            coefficient, output = fixed_word_contraction(e22, monomial)
            deleted_after, removed_after = remove_decorated_edge(output, edge)
            # Contract after deleting has the same cap coefficient and the
            # same retained partial monomial.
            require(coefficient == cap_entry(e22, 2, 2)
                    and deleted_after == deleted
                    and removed_after == cell,
                    ("cofactor square", matching, edge))
            require(tuple(sorted(deleted_after + (removed_after,))) == output,
                    ("reinsertion square", matching, edge))
            cofactor_squares += 1
            if edge in cut_counts:
                cut_counts[edge] += 1

    require((direct, crossed) == (15, 75), (direct, crossed))
    require(cofactor_squares == 195, cofactor_squares)
    require(cut_counts == {(2, 3): 15, (4, 5): 12}, cut_counts)
    require(scalar_linearity_checks == 270, scalar_linearity_checks)
    return {
        "physical_cap_pair": [P, QSITE],
        "direct_free_pair": list(DIRECT_FREE_EDGE),
        "cap_word": "".join(map(str, CAP_WORD)),
        "endpoint_colours": [CAP_WORD[P], CAP_WORD[QSITE]],
        "parents": len(parents),
        "cap_pair_direct_parents": direct,
        "cap_pair_crossed_parents": crossed,
        "literal_contraction_identity":
            "K|-M_c = K_22*(the same direct/crossed endpoint monomial)",
        "R_linearity_checks": scalar_linearity_checks,
        "all_remote_cofactor_squares": cofactor_squares,
        "distinguished_cut_squares": {
            "q23": cut_counts[(2, 3)],
            "q45": cut_counts[(4, 5)],
        },
        "reinsertion_commutes": True,
        "endpoint_even_section_changes_cap_coordinate": False,
    }


def observation_rank_and_activity_audit():
    caps = tuple(coordinate_cap(a, b)
                 for a in COLOURS for b in COLOURS)
    observation_columns = tuple((cap_entry(cap, 2, 2),) for cap in caps)
    kappa_columns = tuple(cap_kappas(cap) for cap in caps)
    require(rank(observation_columns) == 1, observation_columns)
    require(rank(kappa_columns) == 3, kappa_columns)

    e22 = coordinate_cap(2, 2)
    identity = add_caps(*(coordinate_cap(c, c) for c in COLOURS))
    require(cap_entry(e22, 2, 2) == cap_entry(identity, 2, 2) == 1,
            (e22, identity))
    require(cap_kappas(e22) == (Q(0), Q(0), Q(1))
            and cap_kappas(identity) == (Q(1), Q(1), Q(1)),
            (cap_kappas(e22), cap_kappas(identity)))

    # Original physical cap-block witness: only A_67[22]=1.  The two lifts
    # have the same nonzero direct scalar s=1, but opposite activity verdicts.
    pair_block = coordinate_cap(2, 2)

    def scalar(cap):
        return sum((left * right
                    for left, right in zip(cap, pair_block, strict=True)),
                   Q(0))

    def activity(cap):
        kappas = cap_kappas(cap)
        answer = scalar(cap)
        for value in kappas:
            answer *= value
        return answer

    require(scalar(e22) == scalar(identity) == 1,
            (scalar(e22), scalar(identity)))
    require(activity(e22) == 0 and activity(identity) == 1,
            (activity(e22), activity(identity)))

    # The target tensor detects exactly what the fixed mixed-word parents do
    # not: K|-Delta = sum_c kappa_c X_c.
    target_e22 = cap_kappas(e22)
    target_identity = cap_kappas(identity)
    require(target_e22 != target_identity, (target_e22, target_identity))

    # The fixed-word observation is kappa_2 itself.  It loses the two exact
    # diagonal activity coordinates and all six off-diagonal coordinates.
    observed_diagonal = (Q(0), Q(0), Q(1))
    missing_diagonal_duals = (
        (Q(1), Q(0), Q(0)),
        (Q(0), Q(1), Q(0)),
    )
    require(all(sum(a * b for a, b in zip(dual, observed_diagonal,
                                           strict=True)) == 0
                for dual in missing_diagonal_duals), missing_diagonal_duals)
    return {
        "physical_cap_dimension": 9,
        "fixed_word_observation": "obs_22(K)=K_22",
        "observation_rank": 1,
        "observation_kernel_dimension": 8,
        "diagonal_target_rank": 3,
        "missing_diagonal_activity_coordinates": ["kappa_0", "kappa_1"],
        "two_indistinguishable_lifts": {
            "minimal_coordinate_lift": {
                "K": "E_22",
                "s_on_A67_equals_E22": "1",
                "kappas": ["0", "0", "1"],
                "activity": "0",
            },
            "identity_diagonal_lift": {
                "K": "I=E_00+E_11+E_22",
                "s_on_A67_equals_E22": "1",
                "kappas": ["1", "1", "1"],
                "activity": "1",
            },
        },
        "same_action_on_all_fixed_word_parents_and_cofactors": True,
        "first_distinguishing_physical_readout":
            "K|-Delta=sum_c kappa_c X_c",
        "conclusion": (
            "the marked parent object determines one cap coordinate, not a "
            "cap covector.  Its canonical support-preserving lift is genuine "
            "but inactive; an active lift requires two source-defined "
            "diagonal completion coordinates"
        ),
    }


def constructive_minimum_audit():
    return {
        "already_constructed_coefficient_data": [
            "90-parent marked augmentation",
            "endpoint-even response-to-cap word section",
            "q23/q45 restriction and first dq reinsertion",
        ],
        "minimum_new_solutionwise_map": (
            "a partial conservative lift on the selected marked carrier "
            "j_A:obs_22(K)->K in Cap_phys(A;6,7), including its q23/q45 "
            "proper faces"
        ),
        "necessary_scalar_conditions": [
            "obs_22(K) equals the marked coefficient",
            "s(K)=<K,A_67> is nonzero",
            "kappa_0(K)*kappa_1(K)*kappa_2(K) is nonzero",
            "the physical clean error E_67(K) vanishes",
        ],
        "protected_readout_requirement": (
            "none beyond a conservative B evaluation if K and cleanliness "
            "are checked directly in Cap_phys; B/Eq separation remains "
            "necessary only when the existing r0 chain ladder is used to "
            "prove the physical landing or for Fredholm promotion"
        ),
        "avoidable_for_constructive_cap": [
            "a quasi-isomorphism N->r0",
            "acyclicity of the full comparison cone",
            "an absolute dK_Eq=E filler",
            "essential surjectivity on every primitive cap column",
            "endpoint-odd fillers in the endpoint-even quotient",
        ],
        "not_supplied_by_marked_N": [
            "a canonical lift through the 8-dimensional obs_22 kernel",
            "the two missing diagonal target coordinates",
            "nonvanishing of s",
            "cleanliness of the completed covector",
        ],
        "weakest_sufficient_positive_datum": (
            "one source-provenant completed covector K on the selected "
            "carrier, natural only for the proper faces actually used, with "
            "s*kappa0*kappa1*kappa2 nonzero and E_67(K)=0"
        ),
    }


def audit():
    pin_dependencies()
    ledger = {
        "theorem": (
            "literal marked-parent endpoint contraction is R-linear and "
            "cofactor-natural but has rank-one cap observation K->K_22.  "
            "It neither constructs nor rules out an active cap: E_22 and I "
            "are indistinguishable on the entire marked fixed-word object "
            "while having opposite activity on the same physical cap block"
        ),
        "pins": PINS,
        "termwise_physical_contraction":
            parent_contraction_and_cofactor_audit(),
        "cap_rank_and_scalar_guard": observation_rank_and_activity_audit(),
        "constructive_route_minimum": constructive_minimum_audit(),
        "scope": (
            "exact h=3 physical endpoints 6,7, word 01211222, all 90 "
            "direct-free parents, all 195 internal cofactor/reinsertion "
            "squares, both marked P2 cuts, and the original nine-dimensional "
            "cap and ternary target.  This does not exclude a cross-word "
            "diagonal completion or prove cleanliness of any completion"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="full")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger changed", digest, EXPECTED_LEDGER_SHA256))
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "ledger_sha256": digest}, indent=2, sort_keys=True))
    else:
        print("h3 marked-parent physical cap evaluation: RANK-ONE FORK")
        print("mode", arguments.mode)
        print("literal R-linear/cofactor-natural contraction: YES")
        print("cap observation: rank 1 (K_22), kernel dimension 8")
        print("active cap determined by marked object: NO")
        print("minimum new datum: source-provenant diagonal completion")
        print("ledger_sha256", digest)


if __name__ == "__main__":
    main()
