#!/usr/bin/env python3
"""Test the actual h=4 site/root/Hasse construction of phi01 and phi12.

For the fixed tail T=23|45|67, block transpositions carry the three literal
presentation grades into one another.  On actual decorated coefficient
monomials, however, the two prospective tree edges behave differently.

* p1 and p2 have one identical decorated top monomial.  Their difference is
  the kernel of the two labelled restriction/reinsertion factorizations of
  that monomial.  The Boolean Hasse/Beck--Chevalley source totalization gives
  the coefficient-level phi12 without quotienting coefficient H0.
* p0 and p1 have distinct decorated monomials.  Their block transposition is
  a source-algebra isomorphism to a relabelled object, not a degree-one
  primitive in the fixed pointed object.  Raw folding lowers H0; the
  presentation-safe graph cone retains a new u01 coordinate.

The connected two-root Weyl path maps the first word to the second, but its
GHZ target defect is nonzero.  Across all fifteen tail matchings, every
target-safe linear combination of those root paths has coefficient sum
zero.  The invariant matching-aggregate covector kills that rank-fourteen
subspace and reads one on the desired fixed-tail phi01.  Endpoint-odd Cartan
prisms are contained in this kernel.  Restriction/reinsertion is word
diagonal and cannot change the top quotient.

Thus the existing complete root/Weyl/Hasse operations construct phi12 only
at the source-Hasse level and do not construct phi01.  Consequently no
physical tree or compatible dTau is obtained.  The first missing datum is a
pointed, target-corrected word-changing comparison with nonzero invariant
matching aggregate; a raw site-permutation bar is not a substitute.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction as Q
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h4_collision_ks_three_presentation_connection_grammar_gate.py":
        "6307e4444bae24785206608758590bff3c37432532dfe5c641138edb162b02ff",
    "notes/h4-collision-ks-three-presentation-connection-grammar-gate.md":
        "2bd22746c6dc68f82664cd50111a00162d51f90135be48b3f69adc48fba62761",
    "computations/verify_uniform_physical_cartan_source_prism.py":
        "4f23c4645574d619fac4667eba50567435b2f85ff2583b5b3708a565de400cca",
    "notes/uniform-physical-cartan-source-prism.md":
        "7d1da671c9203c7d6080d988fef662caba6024b65227881e111285ad35ba8067",
    "computations/verify_h3_h2_full_site_chart_swap_pointed_scalar_guard.py":
        "bc35781e0f57bbd1202711e2dc818417d76fa87c69e33d3d4b01540e06865557",
    "notes/h3-h2-full-site-chart-swap-pointed-scalar-guard.md":
        "77771f8eee2a4bbaeb5a9575961efb9c7728833e28bca86d33102806aeffa6c2",
    "computations/verify_h3_hasse_coproduct_cosimplicial_totalization.py":
        "674a7503db43b8ad53d6f4ea9d7fe095f0f26629d92e4b0dd291f14bde82fa3a",
    "notes/h3-hasse-coproduct-cosimplicial-totalization.md":
        "9bb749b3b45a6b0248699bf54364cb304f89e01a4a4ad654963aad3534893ba4",
    "computations/verify_uniform_hyperbolic_collision_pp_augp2_spectator_naturality_gate.py":
        "0eedcb3f03e98ea18b549e2b6e21d7082cf368d8e3bc77fd3f104a178104c25a",
    "notes/uniform-hyperbolic-collision-pp-augp2-spectator-naturality-gate.md":
        "73fd2ff870db0d5344255cee1f2b4008bc19ba5058114f51b312d5a011eb760d",
}
EXPECTED_LEDGER_SHA256 = (
    "9b9a0fecff24117c8f90ace0e9974e61fe0c0b59dc44355c34baa1e4c4babecf"
)

SITE_NAMES = ("P", "S", "0", "1", "2", "3", "4", "5", "6", "7")
TAIL_SITES = (2, 3, 4, 5, 6, 7)
TAIL = ((2, 3), (4, 5), (6, 7))
WORD0 = tuple(map(int, "0121221222"))
WORD1 = tuple(map(int, "0121122222"))
ROOT_SITES = (2, 4)
COMPLEMENT_SITES = (3, 5, 6, 7)

Vector = tuple[Q, ...]
Edge = tuple[int, int]
Matching = tuple[Edge, ...]
Permutation = tuple[int, ...]
DecoratedCell = tuple[int, int, int, int]
DecoratedMonomial = tuple[DecoratedCell, ...]


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def edge(left: int, right: int) -> Edge:
    require(left != right, ("loop", left))
    return tuple(sorted((left, right)))


def matching(*edges: Edge) -> Matching:
    return tuple(sorted(edges))


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield matching(edge(first, second), *tail)


def rank(columns: tuple[Vector, ...]) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    rows = [[columns[column][row] for column in range(len(columns))]
            for row in range(height)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        value = rows[answer][column]
        rows[answer] = [entry / value for entry in rows[answer]]
        for row in range(height):
            if row == answer or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def dot(left: Vector, right: Vector) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def permutation_from_swaps(swaps: tuple[tuple[int, int], ...]) -> Permutation:
    answer = list(range(8))
    for left, right in swaps:
        answer[left], answer[right] = answer[right], answer[left]
    return tuple(answer)


def compose(left: Permutation, right: Permutation) -> Permutation:
    """Composition left after right."""
    return tuple(left[right[site]] for site in range(8))


def act_edge(value: Edge, permutation: Permutation) -> Edge:
    return edge(permutation[value[0]], permutation[value[1]])


def act_matching(value: Matching, permutation: Permutation) -> Matching:
    return matching(*(act_edge(item, permutation) for item in value))


def act_word(word: tuple[int, ...], permutation: Permutation) \
        -> tuple[int, ...]:
    answer = list(word)
    for tail_site in TAIL_SITES:
        answer[tail_site + 2] = word[permutation.index(tail_site) + 2]
    return tuple(answer)


def decorated_monomial(value: Matching, word: tuple[int, ...]) \
        -> DecoratedMonomial:
    return tuple((left, right, word[left + 2], word[right + 2])
                 for left, right in value)


def act_decorated(value: DecoratedMonomial, permutation: Permutation) \
        -> DecoratedMonomial:
    answer = []
    for left, right, colour_left, colour_right in value:
        moved_left, moved_right = permutation[left], permutation[right]
        if moved_left < moved_right:
            answer.append((moved_left, moved_right,
                           colour_left, colour_right))
        else:
            answer.append((moved_right, moved_left,
                           colour_right, colour_left))
    return tuple(sorted(answer))


@dataclass(frozen=True)
class FineLabel:
    removed: Edge
    window: Matching
    reinserted: Edge


def act_fine(value: FineLabel, permutation: Permutation) -> FineLabel:
    return FineLabel(
        act_edge(value.removed, permutation),
        act_matching(value.window, permutation),
        act_edge(value.reinserted, permutation),
    )


PRESENTATION_FINE = (
    FineLabel((2, 3), ((4, 5), (6, 7)), (2, 3)),
    FineLabel((4, 5), ((2, 3), (6, 7)), (4, 5)),
    FineLabel((6, 7), ((2, 3), (4, 5)), (6, 7)),
)

G01 = permutation_from_swaps(((2, 4), (3, 5)))
G12 = permutation_from_swaps(((4, 6), (5, 7)))
G02 = compose(G12, G01)


def literal_site_permutation_audit() -> dict[str, object]:
    require(act_matching(TAIL, G01) == act_matching(TAIL, G12) ==
                act_matching(TAIL, G02) == TAIL,
            "a block permutation left the intrinsic tail")
    require(act_word(WORD0, G01) == WORD1
            and act_word(WORD1, G12) == WORD1
            and act_word(WORD0, G02) == WORD1,
            "the presentation words stopped transporting")
    require(act_fine(PRESENTATION_FINE[0], G01) == PRESENTATION_FINE[1]
            and act_fine(PRESENTATION_FINE[1], G12) == PRESENTATION_FINE[2]
            and act_fine(PRESENTATION_FINE[0], G02) == PRESENTATION_FINE[2],
            "the literal fine labels stopped transporting")

    m0 = decorated_monomial(TAIL, WORD0)
    m1 = decorated_monomial(TAIL, WORD1)
    m2 = decorated_monomial(TAIL, WORD1)
    require(m0 != m1 and m1 == m2,
            ("decorated top distinction changed", m0, m1, m2))
    require(act_decorated(m0, G01) == m1
            and act_decorated(m1, G12) == m2
            and act_decorated(m0, G02) == m2,
            "site permutations stopped acting on actual coefficients")

    all_tail_matchings = tuple(perfect_matchings(TAIL_SITES))
    require(len(all_tail_matchings) == 15, "six-tail matching count")
    for source_word, target_word, group_element in (
            (WORD0, WORD1, G01), (WORD1, WORD1, G12),
            (WORD0, WORD1, G02)):
        actual = Counter(act_decorated(
            decorated_monomial(value, source_word), group_element
        ) for value in all_tail_matchings)
        expected = Counter(decorated_monomial(
            act_matching(value, group_element), target_word
        ) for value in all_tail_matchings)
        require(actual == expected,
                ("complete coefficient row lost covariance", group_element))

    return {
        "site_permutations": {
            "g01": {"cycles": ["(2 4)", "(3 5)"],
                    "maps": "p0 -> p1"},
            "g12": {"cycles": ["(4 6)", "(5 7)"],
                    "maps": "p1 -> p2"},
            "g02": {"definition": "g12*g01", "maps": "p0 -> p2"},
        },
        "strict_composition_g12_g01_equals_g02": True,
        "fixed_intrinsic_tail": ["23", "45", "67"],
        "word_transport": ["0121221222", "0121122222",
                           "0121122222"],
        "fine_transport": [
            "t_23*q_(v,45|67)",
            "t_45*q_(v,23|67)",
            "t_67*q_(v,23|45)",
        ],
        "complete_tail_matchings_checked_per_map": len(all_tail_matchings),
        "actual_decorated_coefficient_top_equalities": {
            "m0_equals_m1": False,
            "m1_equals_m2": True,
        },
        "interpretation": (
            "g01 transports one decorated coefficient monomial to a distinct "
            "relabelled monomial; g12 permutes two equal-colour edge factors "
            "of the same decorated commutative top"
        ),
    }


def restriction_reinsertion_audit() -> dict[str, object]:
    for fine in PRESENTATION_FINE:
        require(matching(*fine.window, fine.reinserted) == TAIL
                and fine.removed == fine.reinserted,
                ("presentation stopped reinserting to T", fine))

    # Presentation-coordinate order p0,p1,p2.  Multiplication/reinsertion
    # lands in the two literal decorated coefficient tops m0,m1=m2.
    mu_columns = (
        tuple(map(Q, (1, 0))),
        tuple(map(Q, (0, 1))),
        tuple(map(Q, (0, 1))),
    )
    phi01 = tuple(map(Q, (-1, 1, 0)))
    phi12 = tuple(map(Q, (0, -1, 1)))

    def apply_mu(vector: Vector) -> Vector:
        return tuple(sum((vector[column] * mu_columns[column][row]
                          for column in range(3)), Q(0))
                     for row in range(2))

    require(rank(mu_columns) == 2
            and apply_mu(phi01) == tuple(map(Q, (-1, 1)))
            and apply_mu(phi12) == (Q(0), Q(0)),
            "the coefficient factorization kernel changed")
    require(len(mu_columns) - rank(mu_columns) == 1,
            "the factorization kernel stopped being one-dimensional")

    # Raw fine folding and presentation-safe graph cones.  At phi12 the
    # unflagged coefficient is already one coordinate, but the two retained
    # fine flags are distinct physical presentation coordinates.
    phi01_raw_h0_before = 2
    phi01_raw_h0_after = 2 - rank((tuple(map(Q, (-1, 1))),))
    phi01_graph_h0 = 3 - rank((tuple(map(Q, (-1, 1, -1))),))
    phi12_fine_h0_before = 2
    phi12_fine_h0_after = 2 - rank((tuple(map(Q, (-1, 1))),))
    phi12_graph_h0 = 3 - rank((tuple(map(Q, (-1, 1, -1))),))
    require((phi01_raw_h0_before, phi01_raw_h0_after, phi01_graph_h0)
            == (2, 1, 2)
            and (phi12_fine_h0_before, phi12_fine_h0_after,
                 phi12_graph_h0) == (2, 1, 2),
            "the pointed graph H0 guard changed")

    return {
        "reinsertion_products": [
            "I_23(45|67)=23|45|67",
            "I_45(23|67)=23|45|67",
            "I_67(23|45)=23|45|67",
        ],
        "presentation_to_decorated_top_matrix_rank": rank(mu_columns),
        "kernel_dimension": len(mu_columns) - rank(mu_columns),
        "kernel_generator": "p2-p1",
        "mu_phi01": ["-m0", "+m1"],
        "mu_phi12": 0,
        "phi12_source_Hasse_status": (
            "the labelled Boolean/Hasse Beck-Chevalley totalization fills "
            "the factorization kernel before physical augmented comparison"
        ),
        "phi12_retained_labels": [
            "t_45*q_(v,23|67); removed/reinserted 45",
            "t_67*q_(v,23|45); removed/reinserted 67",
        ],
        "phi12_unconditional_augmented_cap_status": False,
        "phi12_remaining_comparison": (
            "Hasse source cell -> physical PP/AugP2 protected rows"
        ),
        "raw_fold_H0": {
            "phi01_decorated_coefficients_before_after": [2, 1],
            "phi12_retained_fine_flags_before_after": [2, 1],
        },
        "presentation_safe_graph_H0": {
            "phi01_with_u01": phi01_graph_h0,
            "phi12_with_u12_before_using_source_Hasse_cell": phi12_graph_h0,
        },
        "first_pointed_difference": (
            "restriction/reinsertion places p2-p1 in a genuine coefficient "
            "factorization kernel, but p1-p0 has nonzero coefficient image"
        ),
    }


def signed_weyl_word(word: tuple[int, ...]) -> tuple[tuple[int, ...], int]:
    answer = list(word)
    sign = 1
    for site in ROOT_SITES:
        index = site + 2
        if answer[index] == 1:
            answer[index] = 2
            sign *= -1
        elif answer[index] == 2:
            answer[index] = 1
    return tuple(answer), sign


def permute_full_word(word: tuple[int, ...], permutation: Permutation) \
        -> tuple[int, ...]:
    return act_word(word, permutation)


def root_weyl_target_and_aggregate_audit() -> dict[str, object]:
    changed, sign = signed_weyl_word(WORD0)
    require(changed == WORD1 and sign == -1,
            ("the selected signed two-root word changed", changed, sign))

    delta = Counter({(colour,) * len(SITE_NAMES): 1 for colour in range(3)})
    w_delta = Counter()
    for word, coefficient in delta.items():
        moved, coefficient_sign = signed_weyl_word(word)
        w_delta[moved] += coefficient * coefficient_sign
    defect = Counter(w_delta)
    defect.subtract(delta)
    defect = Counter({word: coefficient for word, coefficient in
                      defect.items() if coefficient})
    require(defect and len(defect) == 4,
            ("the two-root GHZ target defect changed", defect))

    complement_permutations = []
    for moved in permutations(COMPLEMENT_SITES):
        value = list(range(8))
        for old, new in zip(COMPLEMENT_SITES, moved, strict=True):
            value[old] = new
        complement_permutations.append(tuple(value))
    require(len(set(complement_permutations)) == 24,
            "complement S4 changed")
    for group_element in complement_permutations:
        transported = Counter()
        for word, coefficient in defect.items():
            transported[permute_full_word(word, group_element)] += coefficient
        require(transported == defect,
                ("the Weyl defect lost disjoint-site invariance",
                 group_element))

    tails = tuple(perfect_matchings(TAIL_SITES))
    require(len(tails) == 15 and TAIL in tails, "tail census")
    width = len(tails)
    unit = tuple(Q(1) if index == tails.index(TAIL) else Q(0)
                 for index in range(width))
    aggregate = (Q(1),) * width
    target_safe_differences = tuple(
        tuple(Q(1) if row == index else Q(-1) if row == 0 else Q(0)
              for row in range(width))
        for index in range(1, width)
    )
    require(rank(target_safe_differences) == width - 1
            and all(dot(aggregate, column) == 0
                    for column in target_safe_differences)
            and dot(aggregate, unit) == 1,
            "the root matching-aggregate quotient changed")

    # An endpoint-odd Cartan prism has matching coefficient e_M-e_sM, hence
    # lies in the same augmentation-zero kernel.  Check every complement
    # permutation and every matching, including fixed points (zero columns).
    prism_columns = set()
    lookup = {value: index for index, value in enumerate(tails)}
    for group_element in complement_permutations:
        for index, value in enumerate(tails):
            moved_index = lookup[act_matching(value, group_element)]
            column = tuple(Q((1 if row == index else 0)
                             - (1 if row == moved_index else 0))
                           for row in range(width))
            if any(column):
                prism_columns.add(column)
    require(prism_columns
            and all(dot(aggregate, column) == 0 for column in prism_columns)
            and rank(tuple(prism_columns)) <= width - 1,
            "a target-safe Cartan prism acquired invariant aggregate")

    return {
        "root_sites": list(ROOT_SITES),
        "signed_Weyl_on_p0": {"word": "0121122222", "sign": -1},
        "GHZ_target_defect_nonzero": True,
        "GHZ_target_defect_support_size": len(defect),
        "defect_invariant_under_disjoint_tail_S4": True,
        "tail_matching_count": width,
        "root_top_matching_space_dimension": width,
        "target_safe_root_combination_rank": width - 1,
        "target_safe_criterion": "sum of matching coefficients = 0",
        "canonical_dual": "chi_match=sum over all 15 tail matchings",
        "chi_on_every_target_safe_root_combination": 0,
        "chi_on_desired_fixed_tail_phi01": 1,
        "endpoint_odd_Cartan_prisms_killed_by_chi": True,
        "restriction_reinsertion_effect_on_top_quotient": (
            "word diagonal and equivariant; it supplies lower Hasse faces "
            "but no invariant root aggregate"
        ),
        "first_new_source_datum": (
            "a pointed target-corrected word-changing cell with nonzero "
            "matching aggregate, or an augmented terminal accepting chi_match"
        ),
    }


def triangle_consequence_audit() -> dict[str, object]:
    # If raw groupoid arrows were admitted, strict g12*g01=g02 supplies the
    # usual nerve 2-simplex.  Presentation-safe cones instead retain graph
    # coordinates uij.  Their triangle is the next boundary debt.
    edge_boundaries = (
        tuple(map(Q, (-1, 1, 0))),
        tuple(map(Q, (-1, 0, 1))),
        tuple(map(Q, (0, -1, 1))),
    )
    triangle = tuple(map(Q, (1, -1, 1)))
    boundary = tuple(sum((triangle[column] * edge_boundaries[column][row]
                          for column in range(3)), Q(0))
                     for row in range(3))
    require(boundary == (Q(0),) * 3, "triangle incidence")
    return {
        "raw_action_groupoid_relation": "g12*g01=g02",
        "raw_nerve_boundary": "dTau=phi01-phi02+phi12",
        "raw_groupoid_triangle_exact": True,
        "raw_groupoid_is_fixed_pointed_source": False,
        "presentation_safe_edge_boundaries": (
            "d b_ij=(p_j-p_i)-u_ij"
        ),
        "first_graph_coherence_debt": "u01-u02+u12",
        "phi12_source_Hasse_edge_available": True,
        "phi01_physical_edge_available": False,
        "compatible_physical_dTau_available": False,
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    site = literal_site_permutation_audit()
    hasse = restriction_reinsertion_audit()
    root = root_weyl_target_and_aggregate_audit()
    triangle = triangle_consequence_audit()
    require(not site["actual_decorated_coefficient_top_equalities"]
                ["m0_equals_m1"]
            and site["actual_decorated_coefficient_top_equalities"]
                ["m1_equals_m2"]
            and hasse["mu_phi12"] == 0
            and root["chi_on_desired_fixed_tail_phi01"] == 1
            and not triangle["compatible_physical_dTau_available"],
            "the mixed positive/negative verdict changed")
    ledger = {
        "theorem": "h4 physical site/root/Hasse presentation-tree gate",
        "pins": PINS,
        "literal_complete_source_site_action": site,
        "restriction_reinsertion_factorization": hasse,
        "root_Weyl_target_safe_aggregate": root,
        "triangle_consequence": triangle,
        "verdict": (
            "The tail-block permutations transport every literal word, "
            "t_i*q_(v,N_i), window, removal and reinsertion label and obey "
            "g12*g01=g02 on the complete source.  They do not by themselves "
            "give fixed-pointed-source bars.  The distinction is exact: p1 "
            "and p2 reinsert to the same decorated coefficient monomial, so "
            "p2-p1 is the one-dimensional Hasse/Beck-Chevalley "
            "factorization kernel; p0 and p1 are different decorated "
            "monomials, so p1-p0 has nonzero coefficient image and raw site "
            "folding lowers H0.  The two-root Weyl path reaches the right "
            "word but has nonzero GHZ target defect.  All target-safe "
            "combinations over the fifteen tail matchings have sum zero and "
            "are killed by chi_match, whereas the requested fixed-tail "
            "phi01 has chi_match=1.  Hence current complete root/Weyl and "
            "restriction/reinsertion operations do not build the physical "
            "tree or dTau."
        ),
        "scope": (
            "exact complete six-tail matching, ternary-word, decorated-"
            "coefficient, labelled restriction/reinsertion and GHZ-target "
            "audit for the fixed h4 fibre and its full fifteen-matching root "
            "orbit.  The matching-aggregate covector is terminal for the "
            "named root/Weyl/Hasse/site-permutation constructors, not for an "
            "unwritten pointed target-corrected comparison or a larger "
            "augmented source family.  Phi12 is source-Hasse-provenant but "
            "its downstream PP/AugP2 protected-row comparison remains "
            "conditional."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("h4 physical tree ledger changed", digest))
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("all", "site", "hasse", "root",
                                           "triangle"), default="all")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "sha256": digest}, indent=2, sort_keys=True))
    else:
        print(f"h4 physical site/root/Hasse tree ({arguments.mode}): PASS")
        print("phi12: coefficient Hasse/Beck-Chevalley kernel, YES")
        print("phi01: fixed-source physical connector, NO")
        print("chi_match: target-safe root rank 14/15; desired value 1")
        print("compatible physical dTau: NO")
        print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
