#!/usr/bin/env python3
"""Audit PSQJet_01 as an actual mixed jet versus an absolute source cell.

In the full relative Boolean occurrence DGA the odd graph generator b^-
already exists.  Kähler prolongation and multiplication by q01 therefore
produce the literal element

    J_rel = d(q01 b^-)=dq01 b^-+q01 db^-.

Its presentation differential is the complete 6+6+3 signed product rule,
relative to the equally labelled carrier jet d(q01 u^-).  No new relative
Tate generator is needed.

This is not an absolute physical PSQJet.  Actual divided-Hasse extraction
from complete source rows contains J*eta and all compatible pair faces, not
the selected endpoint fibre.  After granting all six endpoint face pairs,
all termwise carrier graphs, every Hall/coloop exit, and the complete even
rows, the six P4+K2 plus three 4K2 signed pairs retain an exact normalized
endpoint-odd dual.  Thus the next cell must make the relative jet carrier
absolute (equivalently, map it through the two root-labelled cap sections).
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_pf_boolean_odd_graph_db01_section_gate.py":
        "290f2263c5515520fcfa5cd057011690fe24afbd0587af6c84e8c4d4778cd7ac",
    "computations/verify_h3_retained_pair_divided_hasse_min_support_gate.py":
        "28866193002fff5096b8af3db04055fcc786c558a41f084f524d13dec01483cb",
    "computations/verify_h3_selected_lower_quiver_kahler_mapping_cylinder_gate.py":
        "e5deda7162db47f229239dc91b419baaf00c3158249859cbafb03fe3af2cc958",
    "computations/verify_h3_endpoint_odd_cartan_prism_augmentation.py":
        "24ec9e3c1d1f9b689fa5a47faf9900c16724dc215fee0a41a0b653f410427fb3",
    "computations/verify_h3_double_collision_active_fan_hall_prolongation_gate.py":
        "c120ecac81f50b2d418fef91492dd79cb68c5eb5fb65d39dd5e3d7ddce029238",
    "computations/verify_h3_selected_db01_active_coloop_reinsertion_gate.py":
        "a08598e088c100e4b5116fb2b39717ec639116ea1fa7575062ba9a8f8cf9c683",
    "computations/verify_h3_pointed_occurrence_edge_euler_boolean_cube_gate.py":
        "2b720f2a81d047454e224ec6af7ad62680c6ffeae33b6d7275cf995789bc8b8c",
}
EXPECTED_LEDGER_SHA256 = (
    "3d52e6b3b06869766bca889117b053f3eece6a83f898910a407f0ae99e8c0acd"
)


VARIABLES = (
    "p0", "s1", "p1", "s0", "q01",
    "q23", "q45", "q24", "q35", "q25", "q34",
)
TAILS = (("q23", "q45"), ("q24", "q35"), ("q25", "q34"))


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def add(*vectors: tuple[Q, ...]) -> tuple[Q, ...]:
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum(entries, Q(0)) for entries in zip(*vectors, strict=True))


def scale(coefficient: Q, vector: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(Q(coefficient) * Q(entry) for entry in vector)


def dot(left: tuple[Q, ...], right: tuple[Q, ...]) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def unit(width: int, index: int) -> tuple[Q, ...]:
    return tuple(Q(position == index) for position in range(width))


def rank(columns: tuple[tuple[Q, ...], ...] | list[tuple[Q, ...]]) -> int:
    if not columns:
        return 0
    columns = tuple(tuple(map(Q, column)) for column in columns)
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


# A squarefree polynomial is a dict from frozenset(variable names) to Q.
Polynomial = dict[frozenset[str], Q]
Form = dict[str, Polynomial]


def poly_add(left: Polynomial, right: Polynomial,
             coefficient: Q = Q(1)) -> Polynomial:
    answer = dict(left)
    for monomial, value in right.items():
        answer[monomial] = answer.get(monomial, Q(0)) + coefficient * value
        if not answer[monomial]:
            del answer[monomial]
    return answer


def poly_multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    answer: Polynomial = {}
    for left_monomial, left_value in left.items():
        for right_monomial, right_value in right.items():
            require(left_monomial.isdisjoint(right_monomial),
                    ("non-squarefree product", left_monomial, right_monomial))
            monomial = left_monomial | right_monomial
            answer[monomial] = answer.get(monomial, Q(0)) + (
                left_value * right_value
            )
    return {monomial: value for monomial, value in answer.items() if value}


def polynomial_monomial(*variables: str, coefficient: Q = Q(1)) -> Polynomial:
    require(len(variables) == len(set(variables)), variables)
    return {frozenset(variables): Q(coefficient)}


def derivative(polynomial: Polynomial) -> Form:
    answer: Form = {}
    for monomial, coefficient in polynomial.items():
        for variable in monomial:
            term = {monomial - {variable}: coefficient}
            answer[variable] = poly_add(answer.get(variable, {}), term)
    return answer


def form_add(left: Form, right: Form, coefficient: Q = Q(1)) -> Form:
    answer = dict(left)
    for basis, polynomial in right.items():
        answer[basis] = poly_add(answer.get(basis, {}), polynomial, coefficient)
        if not answer[basis]:
            del answer[basis]
    return answer


def form_multiply(polynomial: Polynomial, form: Form) -> Form:
    return {basis: poly_multiply(polynomial, coefficient)
            for basis, coefficient in form.items()}


def physical_psqjet_product_rule_audit() -> dict[str, object]:
    b_minus_c: Polynomial = {}
    h: Polynomial = {}
    for left, right in TAILS:
        b_minus_c = poly_add(
            b_minus_c,
            polynomial_monomial("p0", "s1", left, right),
        )
        b_minus_c = poly_add(
            b_minus_c,
            polynomial_monomial("p1", "s0", left, right),
            Q(-1),
        )
        h = poly_add(h, polynomial_monomial(left, right))
    q = polynomial_monomial("q01")
    top = poly_multiply(q, b_minus_c)
    direct = derivative(top)
    product_rule = form_add(
        form_multiply(q, derivative(b_minus_c)),
        form_multiply(b_minus_c, derivative(q)),
    )
    require(direct == product_rule and len(top) == 6,
            "the PSQJet product rule changed")

    endpoint_bases = ("p0", "s1", "p1", "s0")
    tail_bases = tuple(variable for tail in TAILS for variable in tail)
    endpoint_flags = sum(len(direct[basis]) for basis in endpoint_bases)
    tail_flags = sum(len(direct[basis]) for basis in tail_bases)
    dq_flags = len(direct["q01"])
    require((endpoint_flags, tail_flags, dq_flags) == (12, 12, 6),
            (endpoint_flags, tail_flags, dq_flags))

    # Every monomial remains literal.  The two orientations have opposite
    # coefficients with identical q/tail complements.
    for left, right in TAILS:
        require(top[frozenset(("p0", "s1", "q01", left, right))] == 1
                and top[frozenset(("p1", "s0", "q01", left, right))] == -1,
                (left, right))
    return {
        "top": "(p0*s1-p1*s0)*q01*H2345",
        "top_monomials": len(top),
        "top_type": "endpoint-odd P4+2K2",
        "universal_product_rule_verified": True,
        "literal_first_flags": {
            "endpoint": {"literal": endpoint_flags, "signed_pairs": 6,
                         "type": "P3+2K2"},
            "tail": {"literal": tail_flags, "signed_pairs": 6,
                     "type": "P4+K2"},
            "dq01": {"literal": dq_flags, "signed_pairs": 3,
                     "type": "4K2"},
        },
        "formula": (
            "d((B-C)qH)=(dB-dC)qH+(B-C)dq H+(B-C)q dH"
        ),
        "word": "11110000 = 11:110000",
        "repeated_sites": [0, 1],
        "operation": "PS-over-q01 mixed first jet",
    }


def relative_kahler_totalization_audit() -> dict[str, object]:
    # Fifteen signed product-rule face pairs.  Per pair retain physical B,C
    # and carrier B,C.  The two monic graph rows and one complete-even row
    # have rank three.  The relative jet is their signed graph difference;
    # the absolute physical odd row is the missing fourth direction.
    pairs = 15
    width = 4 * pairs

    def position(block: int, face: int) -> int:
        return block * pairs + face

    def vector(values: dict[int, int]) -> tuple[Q, ...]:
        return tuple(Q(values.get(index, 0)) for index in range(width))

    rows = []
    for face in range(pairs):
        rows.extend((
            vector({position(0, face): -1, position(2, face): 1}),
            vector({position(1, face): -1, position(3, face): 1}),
            vector({position(0, face): 1, position(1, face): 1}),
            vector({position(2, face): 1, position(3, face): 1}),
        ))
    rows = tuple(rows)
    relative_jet = vector({
        **{position(0, face): 1 for face in range(pairs)},
        **{position(1, face): -1 for face in range(pairs)},
        **{position(2, face): -1 for face in range(pairs)},
        **{position(3, face): 1 for face in range(pairs)},
    })
    absolute_jet = vector({
        **{position(0, face): 1 for face in range(pairs)},
        **{position(1, face): -1 for face in range(pairs)},
    })
    require(rank(rows) == 3 * pairs
            and rank((*rows, relative_jet)) == 3 * pairs
            and rank((*rows, absolute_jet)) == 3 * pairs + 1,
            "the relative/absolute PSQJet rank comparison changed")

    # Grant the six endpoint signed pairs absolutely.  The only remaining
    # odd character is supported on the six tail plus three dq01 pairs.
    endpoint_grants = tuple(
        vector({position(0, face): 1, position(1, face): -1})
        for face in range(6)
    )
    routed = (*rows, *endpoint_grants)
    remaining_dual_values = {}
    dual_entries = {}
    for face in range(6, pairs):
        dual_entries.update({
            position(0, face): 1,
            position(1, face): -1,
            position(2, face): 1,
            position(3, face): -1,
        })
    dual = vector(dual_entries)
    require(rank(routed) == 51
            and rank((*routed, absolute_jet)) == 52
            and all(dot(dual, row) == 0 for row in routed)
            and dot(dual, relative_jet) == 0
            and dot(dual, absolute_jet) == 18,
            "the routed nine-pair endpoint-odd dual changed")
    normalized_dual = scale(Q(1, 18), dual)
    remaining_dual_values["relative_jet"] = str(dot(normalized_dual,
                                                      relative_jet))
    remaining_dual_values["absolute_jet"] = str(dot(normalized_dual,
                                                      absolute_jet))
    return {
        "face_pair_order": [
            "6 endpoint P3+2K2", "6 tail P4+K2", "3 dq01 4K2",
        ],
        "coordinates": width,
        "relative_graph_even_rank": rank(rows),
        "rank_after_relative_PSQJet": rank((*rows, relative_jet)),
        "rank_after_absolute_PSQJet": rank((*rows, absolute_jet)),
        "identity": (
            "d(q01*b^-) = dq01*b^- + q01*d(b^-); its presentation "
            "boundary is physical PSQJet - d(q01*u^-)"
        ),
        "new_relative_Tate_generator_required": False,
        "absolute_physical_constructor_present": False,
        "after_granting_all_six_endpoint_pairs": {
            "rank_before_after_absolute_jet": [51, 52],
            "normalized_dual_support": "the 6 P4+K2 and 3 4K2 pairs only",
            "normalized_dual_on_relative_and_absolute":
                remaining_dual_values,
        },
    }


def actual_divided_hasse_scope_audit(retained) -> dict[str, object]:
    ledger, digest = retained.audit()
    require(digest == retained.EXPECTED_LEDGER_SHA256,
            "the actual divided-Hasse dependency changed")
    inventory = ledger["complete_product_rule_inventory"]
    guard = ledger["literal_mixed_two_pair_guard"]
    require(not inventory["isolated_marked_pair_equation"]
            and inventory["pair_shapes"]["PS_response"][
                "literal_complement_count"] == 3
            and guard["marked_retained_pair_value"] == "1"
            and guard["silent_mate_pair_value"] == "-1",
            "the divided-Hasse selected-pair guard changed")
    return {
        "actual_bivariate_formula":
            "[st]F(X)=J_xF(eta)+B_xF(xi,zeta)",
        "PS_pair_C4_complements": 3,
        "selected_pair_isolated": False,
        "mandatory_extra_faces": [
            "J_xF(eta)", "every other compatible ordered pair in a matching",
        ],
        "literal_guard": {
            "marked_pair": 1, "silent_same-grade_mate": -1,
            "complete_target_and_direct_response": 0,
        },
        "conclusion": (
            "PSQJet_01 is not the isolated divided-Hasse coefficient of an "
            "existing absolute complete source row.  Occurrence selection "
            "is supplied only by the relative Boolean cylinders."
        ),
    }


def hall_fan_cartan_route_audit(db01, collision, cartan, kahler) \
        -> dict[str, object]:
    db_ledger, db_digest = db01.audit()
    collision_ledger, collision_digest = collision.audit()
    cartan_ledger, cartan_digest = cartan.audit()
    require(db_digest == db01.EXPECTED_LEDGER_SHA256
            and collision_digest == collision.EXPECTED_LEDGER_SHA256
            and cartan_digest == cartan.EXPECTED_LEDGER_SHA256,
            "a routing dependency changed")
    physical = db_ledger["literal_PP_and_reinsertion_faces"][
        "physical_endpoint_insertion"]
    recurrence = collision_ledger["committed_recurrence_scope"]
    survivor = collision_ledger["finite_endpoint_odd_counterguard"]
    jet = kahler.localization_and_jet_audit()
    require(physical["face_counts"]
                == {"endpoint_dp_ds": 6, "tail_q_db01": 6,
                    "dq01_companion": 3}
            and recurrence["double_collision_face_block"]["live_families"]
                == {"P4+K2": 6, "4K2": 3}
            and survivor["rank_before_after_selected_B_packet"] == [27, 28]
            and "dU" in jet["first_jet_matrix"]
            and "descend H_w" in cartan_ledger["remaining_obligations"][0],
            "the Hall/fan/Cartan route interface changed")
    return {
        "relative_Kahler_route": {
            "status": "complete",
            "mechanism": "the canonical first-jet mapping-cylinder diagonal dU",
            "all_15_signed_pairs_land_in": "d(q01*u^-), with literal labels",
        },
        "endpoint_6_pairs": {
            "grant": "all endpoint dp/ds fan/Cartan exits",
            "effect_on_no_go": "none; the final dual is supported off them",
        },
        "tail_6_P4K2_pairs": {
            "Hall_fan_route": "termwise transport to retained coloop exits",
            "absolute_exit": False,
        },
        "dq01_3_4K2_pairs": {
            "Hall_fan_route": "termwise transport to retained coloop exits",
            "absolute_exit": False,
        },
        "Cartan_scope": {
            "endpoint_even_target_D_W_anchor_Eq": "killed by oddness",
            "ordinary_residue": "retained",
            "physical_source_labelled_descent": "open",
            "operation_block_match_to_P4+2K2": False,
        },
        "strong_exit_counterguard": {
            "rank_before_after_selected_orientation": [27, 28],
            "dual_value": 9,
            "meaning": (
                "even after a B and C recurrence graph and complete even "
                "source/exit row in every remaining fine label, the odd "
                "nine-face packet is not absolute"
            ),
        },
    }


def prior_domain_and_landing_audit(prior) -> dict[str, object]:
    ledger, digest = prior.audit()
    require(digest == prior.EXPECTED_LEDGER_SHA256,
            "the relative odd-domain dependency changed")
    boolean = ledger["Boolean_carrier_comparison"]
    section = ledger["conditional_root_section_gate"]
    require(boolean["full_relative_plus_transpose_presentation"][
                "new_source_generator_required"] is False
            and section["recorded_source_interface_matches"]
            and not section["literal_head_fine_map_constructed"],
            "the relative-domain/cap-section interface changed")
    return {
        "relative_u_minus_and_four_faces_present": True,
        "relative_PSQJet_present_by_DGA_product": True,
        "next_required_absolute_map": (
            "the two root-labelled receiving sections from the PSQJet "
            "carrier jet d(q01*u^-) to the tied r0 cap"
        ),
        "recorded_word_operation_interface_matches": True,
        "literal_head_fine_section_constructed": False,
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    retained = load(
        "computations/verify_h3_retained_pair_divided_hasse_min_support_gate.py",
        "psqjet_retained_pair",
    )
    prior = load(
        "computations/verify_h3_pf_boolean_odd_graph_db01_section_gate.py",
        "psqjet_prior",
    )
    db01 = load(
        "computations/verify_h3_selected_db01_active_coloop_reinsertion_gate.py",
        "psqjet_db01",
    )
    collision = load(
        "computations/verify_h3_double_collision_active_fan_hall_prolongation_gate.py",
        "psqjet_collision",
    )
    cartan = load(
        "computations/verify_h3_endpoint_odd_cartan_prism_augmentation.py",
        "psqjet_cartan",
    )
    kahler = load(
        "computations/verify_h3_selected_lower_quiver_kahler_mapping_cylinder_gate.py",
        "psqjet_kahler",
    )

    ledger = {
        "theorem": "h3 PSQJet_01 divided-Hasse/relative-DGA gate",
        "pins": PINS,
        "literal_physical_product_rule": physical_psqjet_product_rule_audit(),
        "relative_Kahler_totalization": relative_kahler_totalization_audit(),
        "actual_absolute_divided_Hasse":
            actual_divided_hasse_scope_audit(retained),
        "named_Hall_fan_Cartan_routes":
            hall_fan_cartan_route_audit(db01, collision, cartan, kahler),
        "domain_and_next_landing": prior_domain_and_landing_audit(prior),
        "verdict": (
            "PSQJet_01 is a genuine mixed first jet of the existing full "
            "relative Boolean occurrence presentation: it is exactly "
            "d(q01*b^-), so its six endpoint, six P4+K2 tail and three 4K2 "
            "dq01 signed face pairs, together with their carrier mates, "
            "require no new relative Tate generator.  It is not an absolute "
            "divided-Hasse consequence of the complete physical source "
            "rows: actual extraction includes J*eta and every compatible "
            "same-grade pair.  Granting every endpoint exit and every "
            "current Hall/coloop recurrence still leaves a normalized dual "
            "supported on the nine P4+K2/4K2 pairs.  The next physical cell "
            "must make d(q01*u^-) absolute, equivalently construct the two "
            "root-labelled carrier-to-r0 sections with literal head/fine "
            "incidence."
        ),
        "terminal_promotion_input": {
            "normalized_local_dual": (
                "1/18 times (+B-C on source and carrier) on the six P4+K2 "
                "and three 4K2 pairs; zero on endpoint and protected rows"
            ),
            "kills_named_inventory": True,
            "global_augmented_terminal": False,
            "remaining_extension_test": (
                "extend this operation/fine dual across the two root cap "
                "sections, mixed K_Eq square, residue/ridge and all external "
                "complete-source columns"
            ),
        },
        "scope": (
            "exact rational h=3 product-rule, relative cotangent-cylinder, "
            "actual divided-Hasse and named Hall/fan/Cartan audit.  The "
            "local normalized dual is not promoted here to a global source "
            "terminal."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("PSQJet_01 relative mixed first jet: EXISTS AS d(q01*b^-)")
    print("new relative Tate generator required: NO")
    print("absolute divided-Hasse physical constructor: NO")
    print("6 endpoint pairs: GRANTED; 6 P4+K2 + 3 4K2: RETAINED")
    print("normalized nine-pair dual on relative/absolute: 0 / 1")
    print("next physical map: TWO ROOT CARRIER->r0 SECTIONS")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
