#!/usr/bin/env python3
"""Expose the first literal full-row discrepancy in the selected-lower route.

Commit ``6fd2412`` reduces the determinant-dark Gate-I branch to

    J_3(M_v) = A J_col(u_024-u_012).                         (1)

Its pinned left-side theorem reports a physical 360-feature boundary with
all augmented rows typed.  The right side is not yet defined on the complete source rows.  The
nearest committed source-provenant construction is the endpoint-recoloured
order-six Cartan--Spencer cycle.  Its forgotten-grade secondary shadow is the
required ``-delta`` class, but coefficient prolongation produces a private
one-term face

    xi = (4/3) q_01^01 q_27^21 q_34^11 q_35^12 q_67^22.     (2)

This checker gives a direct coordinate proof that (2) is outside the entire
homogeneous direct-free full-row block in its exact fine degree.  Thus it is
the first missing relative Spencer boundary for this construction.  This is
not a no-go for every possible definition of J_col: equation (1) remains
open until a relative cell cancels xi and its transported mate.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    # The one-chain reduction and its exact 360-feature/augmented output.
    "computations/verify_h3_selected_lower_one_chain_comparison_reduction.py":
        "c9fc8c847327d0e119264a3a83cf39d0f4c2ff45b4ddd4e048f42a57cac0e887",
    # The source-provenant endpoint construction and the occurrence of xi.
    "computations/verify_h3_residual_q_order6_endpoint_recolour_composition.py":
        "6ab3f36073cd08c1ccad97ebd6f8ed3c5f39736be82b6063436c161f176cfeb0",
    # The secondary-transfer interface: source=D1=0 and D2=-delta.
    "computations/verify_h3_order6_endpoint_odd_hpl_secondary_transfer.py":
        "5a89d25227562b397d6cf3f16306346ce7d9fd16fb73a0f0a4486355a7cef29e",
    # Literal complete direct-free rows used below.
    "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py":
        "190171b72493e661dedb8e7aa369a9b72f1a71e14487632df2841ca7eeb19bf4",
    # Independent pin on the physical M_v output construction.
    "computations/verify_h3_literal_mv_cap_cartan_composition.py":
        "8e54a161402499c638dcba6177069fc3bb37648fb37c3546955310a56889744e",
}
EXPECTED_LEDGER_SHA256 = (
    "b3468bf713be632852e00c3eea869bf463a97ba2cce9d3e934072abd2f9cbbaf"
)

XI_DIRECTION = (3, 7, 1, 1)
XI_MONOMIAL = (
    (0, 1, 0, 1),
    (2, 7, 2, 1),
    (3, 4, 1, 1),
    (3, 5, 1, 2),
    (6, 7, 2, 2),
)
XI_COEFFICIENT = Q(4, 3)
NORMALIZED_DUAL_COEFFICIENT = Q(3, 4)
EXPECTED_CANDIDATES = (
    ((0, 1, 2, 1, 1, 2, 2, 1), (3, 7, 1, 2)),
    ((0, 1, 2, 1, 1, 2, 2, 2), (3, 7, 1, 1)),
)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def underlying_pair(cell: tuple[int, int, int, int]) -> frozenset[int]:
    return frozenset(cell[:2])


def compatible_full_row_columns(base, target_degree):
    """Enumerate the entire homogeneous quartic-row times linear block."""
    candidates = []
    for left in range(8):
        for right in range(left + 1, 8):
            if frozenset((left, right)) == base.DIRECT_FREE_PAIR:
                continue
            for left_colour in base.COLOURS:
                for right_colour in base.COLOURS:
                    multiplier = (left, right, left_colour, right_colour)
                    remainder = list(target_degree)
                    remainder[3 * left + left_colour] -= 1
                    remainder[3 * right + right_colour] -= 1
                    if any(value < 0 for value in remainder):
                        continue
                    word = []
                    for site in range(8):
                        site_degree = remainder[3 * site:3 * site + 3]
                        if (sum(site_degree) != 1
                                or any(value not in (0, 1)
                                       for value in site_degree)):
                            break
                        word.append(site_degree.index(1))
                    else:
                        candidates.append((tuple(word), multiplier))
    return tuple(sorted(candidates))


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "selected_spencer_base",
    )
    require(tuple(sorted(XI_MONOMIAL)) == XI_MONOMIAL,
            "the primitive monomial is not canonically ordered")
    target_degree = base.fine_degree_of_edge_monomial(XI_MONOMIAL)
    candidates = compatible_full_row_columns(base, target_degree)
    require(candidates == EXPECTED_CANDIDATES,
            ("the exact fine-degree candidate block changed", candidates))

    edge_37 = frozenset((3, 7))
    column_supports = []
    coordinate_values = []
    for word, multiplier in candidates:
        column = tuple(tuple(sorted((multiplier,) + monomial))
                       for monomial in base.full_row(word))
        require(len(column) == len(set(column)) == 90,
                ("a complete candidate column changed", word, multiplier))
        require(underlying_pair(multiplier) == edge_37,
                ("a compatible multiplier is not q_37", multiplier))
        require(all(any(underlying_pair(cell) == edge_37
                        for cell in monomial) for monomial in column),
                "a candidate full-row monomial lost its forced q_37 factor")
        coordinate_value = sum(Q(int(monomial == XI_MONOMIAL))
                               for monomial in column)
        require(coordinate_value == 0,
                "the private xi coordinate entered a full-row column")
        column_supports.append(len(column))
        coordinate_values.append(coordinate_value)

    require(not any(underlying_pair(cell) == edge_37
                    for cell in XI_MONOMIAL),
            "xi unexpectedly acquired a physical q_37 edge")
    normalized_readout = (
        NORMALIZED_DUAL_COEFFICIENT * XI_COEFFICIENT
    )
    require(normalized_readout == 1,
            "the primitive coordinate dual stopped being normalized")

    ledger = {
        "theorem": "first literal Spencer discrepancy on the selected-lower route",
        "pinned_one_chain_commit": "6fd2412",
        "selected_equation": "J_3(M_v)=A J_col(u_024-u_012)",
        "known_physical_left_side": {
            "literal_features": 360,
            "feature_edge_degree": 7,
            "ordinary_residue": [0, 0, 0, 0],
            "D_W_target_ainc": [0, 0, 0, 0],
            "eta_z": "1+delta_(vz)*u_z/t",
            "sigma": "-q_pq^22",
        },
        "closest_complete_input_constructor": {
            "source_provenant": True,
            "source_and_first_transfer": [0, 0],
            "forgotten_grade_secondary_shadow": "-delta=(-1,+1,+1,-1)",
            "fine_components_require_relative_gluing": True,
            "full_J_col_defined": False,
        },
        "first_literal_discrepancy": {
            "direction": list(XI_DIRECTION),
            "coefficient": str(XI_COEFFICIENT),
            "monomial": [list(cell) for cell in XI_MONOMIAL],
            "fine_degree": list(target_degree),
            "compatible_complete_full_row_columns": len(candidates),
            "candidate_words_and_multipliers": [
                [list(word), list(multiplier)]
                for word, multiplier in candidates
            ],
            "candidate_column_supports": column_supports,
            "all_candidates_have_forced_q37": True,
            "xi_has_q37": False,
        },
        "primitive_coordinate_dual": {
            "functional": "lambda_xi=(3/4)e_xi^*",
            "values_on_complete_full_row_columns": [
                str(value) for value in coordinate_values
            ],
            "value_on_first_spencer_face": str(normalized_readout),
        },
        "smallest_missing_cell": (
            "a chart-nondiagonal relative Spencer generator whose boundary "
            "contains -xi in this exact word/fine/repeated grade, together "
            "with the transported mate and the protected augmented rows"
        ),
        "external_repair1_scope": {
            "used_as_dependency": False,
            "grade_forgotten_D2_match_is_consistent": True,
            "raw_39_24_vs_10_10_split_is_not_a_selected_line_separator": True,
            "rank_153_obstruction_applies_to_uniform_operator_module": True,
            "K_freedom_after_committed_coarse_readouts": 7,
            "remaining_left_side_audit": (
                "an independent termwise H_w/private-full-row construction "
                "is still needed to pin the declared physical K half"
            ),
            "reason": (
                "the selected line may use the missing relative gluing; the "
                "literal lambda_xi above instead separates the first direct "
                "coefficient-prolongation face from its complete homogeneous "
                "physical full-row block"
            ),
        },
        "verdict": (
            "the direct committed Cartan-Spencer constructor does not yet "
            "supply J_col(l); it stops at the normalized private face xi.  "
            "This does not rule out a new relative-cell construction of the "
            "selected full-row equation"
        ),
        "scope": (
            "exact direct-free homogeneous full-row nonmembership in the "
            "first coefficient-prolongation grade.  The occurrence of xi "
            "and the outer selected/output theorems are inherited through "
            "byte-pinned committed audits; this checker does not claim that "
            "lambda_xi is a dual on an as-yet-undefined J_col(l)"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("selected-lower Spencer-discrepancy ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("h3 selected lower full row: FIRST SPENCER DISCREPANCY")
    print("selected equation J3(M_v)=A Jcol(l): STILL OPEN")
    print("compatible full-row columns: 2 (both forced q_37)")
    print("lambda_xi=(3/4)e_xi*: columns 0,0; primitive face 1")
    print("external 39/24 split: not a selected-line separator")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
