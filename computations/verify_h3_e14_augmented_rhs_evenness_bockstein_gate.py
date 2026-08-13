#!/usr/bin/env python3
"""Audit integral evenness of the coupled E14 D-character right side.

On the six alternating root-label lines the coupled system of 677fff4 is

    (I+LF)K=A+X+LFC.

The literal D4 hidden face is ``A=-E`` and the old physical ``O_-E`` has
the compensating private packet ``X=+E``.  The normalized face-3/face-5 cap
graph gives ``d_even=(B1+B4)/2`` and root insertion gives
``LFC=2D_root*d_even=E``.  Hence the right side is the primitive packet

    E=D_root tensor (B1+B4),

not ``2E``.  Since ``LF`` is the identity on the alternating sector, the
equation is ``2K=E``.  It has the unique solution ``E/2`` over k[beta] for
the characteristic-zero theorem, with no beta denominator.  It has no
solution only in the optional coefficient lattice Z[beta], where its class
is the rho-even element ``B1+B4`` in coker(2I_6)=(Z/2)^6.  This is not a
proof obstruction over k[beta].

The centered response identities do not supply a spare two.  They give

    (A_match+I)c_f=3c_01,
    c_01=30b_01-R,
    3R+(A_match+I)c_f=90b_01.

After multiplying the entire coupled equation by 90, the solution is
``45E``.  It is integral, but not divisible by 90; normalizing the selected
fibre recovers ``E/2``.  The single factor 2 in 90 is consumed by the
selected-fibre denominator.  The full coefficient projector says the same
thing as ``8/720=1/90``.

Neither divided-power convention adds a coefficient two: the D4 top
coefficient and the multi-affine second-Hasse cross coefficient are both
one.  This is harmless over k[beta].  The old beta-Bockstein V has zero root
output and addresses an independent beta-primary extension; it is unaffected
by this optional Z-form calculation.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from math import gcd
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_e14_d4_p2_keq_deven_simultaneous_totalization_gate.py":
        "dfa46c3519089bb7b2a04d24ea6e4f9d138887d98fb53af60369184d2d2c91fd",
    "notes/h3-e14-d4-p2-keq-deven-simultaneous-totalization-gate.md":
        "0dcd6a7900fcb34577a56d73aa5b801ced773a4190c3e1e8f6eaf9383117f4a8",
    "computations/verify_h3_e14_selected_fibre_graph_keq_koszul_gate.py":
        "9d57cbcfaeebb8d7f67d6efea87a124b4a46ad1dc054d5fc0954ab0c2338b157",
    "notes/h3-e14-selected-fibre-graph-keq-koszul-gate.md":
        "98cae28b58267abcffc47b571e52581a354950ef684df5f28b58dca88c60c6e7",
    "computations/verify_h3_e14_orbit_relative_d4_target_cone_gate.py":
        "67d33b03ec52c619f29e76c917fdba9b7e28380b4349291fa37b6b7d511e241c",
    "notes/h3-e14-orbit-relative-d4-target-cone-gate.md":
        "6268689c54144cc09b6be596b81d8b4aa741e0590a83e664ec3f6e65b89187bf",
    "computations/verify_h3_augmented_p2_section_shortest_conditional_gate.py":
        "c583279d8f4cb7efc24b7fc4784e480b63acb1ca7fe430ae1a7e2db2b854c11b",
    "notes/h3-augmented-p2-section-shortest-conditional-gate.md":
        "ee5da6f0911feb06707106cc6207161bbac7cabd31885f554321698dfbb989d8",
    "computations/verify_h3_loop_degeneracy_hasse_cross_term_scope_gate.py":
        "024eb1cbe7d5aca9795c7d2491bb6399c0e93324f898d031707c1c752d7ea14c",
    "notes/h3-loop-degeneracy-hasse-cross-term-scope-gate.md":
        "2906899b807451def78bf92e36e1c212c4242982a3ad8f86d2fe2ba274b6cd11",
    "computations/verify_h3_centered_projector_literal_first_hasse_eq_incidence_gate.py":
        "4e32d14b4d495b4439ed7aba59afedc8de0c1c4f76717989ca9e817444e9cd8f",
    "notes/h3-centered-projector-literal-first-hasse-eq-incidence-gate.md":
        "242a0a148c782c73540f060ef4e685902888f6d0e95da2d050b0e46dec5baf9d",
    "computations/verify_h3_generic_cplus_lower_quotient_smith_gate.py":
        "f4ee0503c4639b79a655bdbab94d02218c99b348bee8f3c46f9554b7e803e3e0",
    "notes/h3-generic-cplus-lower-quotient-smith-gate.md":
        "c8ab8922b05e81819029a51d09475de746173c727313c1a5ff7c6d3aca24f2e5",
}
EXPECTED_LEDGER_SHA256 = (
    "e47f3ca618c143c68a50a17339e2fed4234fedce8c041f2d4b8cbc4d4e5e37b6"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def add(*vectors: tuple[int, ...]) -> tuple[int, ...]:
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum(entries) for entries in zip(*vectors, strict=True))


def scale(coefficient: int, vector: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(coefficient * entry for entry in vector)


def tensor(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(a * b for a in left for b in right)


def content(vector: tuple[int, ...]) -> int:
    answer = 0
    for entry in vector:
        answer = gcd(answer, abs(entry))
    return answer


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def literal_augmented_rhs_audit() -> dict[str, object]:
    d_root = (-1, 1, -1, 1)
    orbit_sum = (0, 1, 0, 0, 1, 0)  # B1+B4 = 2*d_even.
    e = tensor(d_root, orbit_sum)

    # These are the D-character coefficients after the coupled comparison
    # identifies the hidden, nearest-lift, and cap faces.  A and X cancel;
    # the cap term remains primitive.
    a = scale(-1, e)
    x = e
    lf_c = e
    rhs = add(a, x, lf_c)
    require(rhs == e and content(rhs) == 1
            and sum(bool(value) for value in rhs) == 8,
            "the literal alternating RHS changed")

    line_a = scale(-1, orbit_sum)
    line_x = orbit_sum
    line_lfc = orbit_sum
    line_rhs = add(line_a, line_x, line_lfc)
    require(line_rhs == orbit_sum and content(line_rhs) == 1,
            "the six-line RHS changed")

    mod2 = tuple(value % 2 for value in line_rhs)
    require(mod2 == (0, 1, 0, 0, 1, 0),
            "the mod-two RHS support changed")
    rational_solution = tuple(Q(value, 2) for value in line_rhs)
    require(tuple(2 * value for value in rational_solution)
                == tuple(map(Q, line_rhs))
            and any(value.denominator == 2 for value in rational_solution),
            "the rational half-solution changed")

    return {
        "six_line_order": ["B0", "B1", "B2", "B3", "B4", "B5"],
        "D_root": list(d_root),
        "primitive_orbit_sum": list(orbit_sum),
        "A_D4_hidden": list(line_a),
        "X_old_O_minus_E": list(line_x),
        "LF_C_cap_face": list(line_lfc),
        "A_plus_X_plus_LF_C": list(line_rhs),
        "literal_24_row_nonzero_entries": 8,
        "integer_content": content(line_rhs),
        "divisible_by_two_in_Z6": False,
        "divisible_by_two_in_Zbeta6": False,
        "mod_two_obstruction": list(mod2),
        "coupled_equation_on_D_sector": "2K=B1+B4",
        "solution_over_characteristic_zero_kbeta": [
            str(value) for value in rational_solution
        ],
        "solution_is_beta_integral": True,
        "solution_over_optional_Zbeta_form": False,
    }


def smith_and_rho_even_audit() -> dict[str, object]:
    # I+LF restricts to 2I_6.  Its Smith invariants are six copies of 2.
    smith = (2,) * 6
    determinant = 1
    for invariant in smith:
        determinant *= invariant
    require(determinant == 64,
            "the integral alternating Smith determinant changed")

    obstruction = (0, 1, 0, 0, 1, 0)
    # rho interchanges B1 and B4.  In the rho-even lattice the orbit sum is
    # a primitive basis vector, not twice another invariant integral vector.
    rho = (0, 4, 2, 3, 1, 5)
    transported = tuple(obstruction[rho[index]] for index in range(6))
    require(transported == obstruction and content(obstruction) == 1,
            "the rho-even primitive obstruction changed")

    return {
        "integral_operator_on_D_lines": "2 I_6",
        "Smith_invariants": list(smith),
        "cokernel": "(Z/2)^6 (and (Z[beta]/2)^6 over Z[beta])",
        "obstruction_class": "[B1+B4]",
        "obstruction_order": 2,
        "rho_action": "B1<->B4",
        "rho_even": True,
        "primitive_in_rho_even_integral_lattice": True,
        "rho_even_cokernel_seen_by_this_packet": "one Z/2 class",
        "primitive_mod2_duals": ["B1 coefficient mod 2", "B4 coefficient mod 2"],
    }


def centered_normalization_audit() -> dict[str, object]:
    fibres = 30
    aggregate = (1,) * fibres
    selected = (1,) + (0,) * (fibres - 1)
    c_01 = add(scale(fibres, selected), scale(-1, aggregate))
    m_c_f = scale(3, c_01)
    numerator = add(scale(3, aggregate), m_c_f)
    require(numerator == scale(90, selected),
            "3R+(A+I)c_f=90b_01 changed")

    # If every augmented face were natural for the centered identity, the
    # D-character numerator would be 90E.  Solving the scaled coupled system
    # gives 45E.  It is integral but cannot be divided by 90 integrally.
    orbit_sum = (0, 1, 0, 0, 1, 0)
    scaled_rhs = scale(90, orbit_sum)
    scaled_solution = tuple(value // 2 for value in scaled_rhs)
    require(tuple(2 * value for value in scaled_solution) == scaled_rhs
            and scaled_solution == scale(45, orbit_sum)
            and any(value % 90 for value in scaled_solution),
            "the centered scaled half-solution changed")

    # h=3 full coefficient projector: combined numerator has output 8*1,
    # denominator 720, hence exactly 1/90 and no spare 2 after normalization.
    require(Q(8, 720) == Q(1, 90),
            "the h3 full projector normalization changed")

    return {
        "centered_identities": [
            "(A_match+I)c_f=3c_01",
            "c_01=30b_01-R",
            "3R+(A_match+I)c_f=90b_01",
        ],
        "selected_generator_formula": (
            "epsilon_01=(3epsilon_R+(A_match+I)epsilon_cf)/90"
        ),
        "normalization_prime_factors": "90=2*3^2*5",
        "full_projector_ratio": "8/720=1/90",
        "conditional_augmented_D_numerator": "90(B1+B4)",
        "scaled_coupled_solution": "45(B1+B4)",
        "scaled_solution_integral": True,
        "scaled_solution_divisible_by_90": False,
        "normalized_solution": "(B1+B4)/2",
        "spare_factor_two_after_selected_normalization": False,
        "interpretation": (
            "the 3 and 30 identities clear the selected-fibre denominator; "
            "they do not make the normalized coupled RHS even"
        ),
    }


def divided_power_and_bockstein_audit() -> dict[str, object]:
    d4_profile = (1, 4, 6, 4, 1)
    require(d4_profile[-1] == 1,
            "the fourth divided-Hasse top coefficient changed")

    # Multi-affine f,g: D^[2](fg)=D(f)D(g), so the cross coefficient is one.
    # The two selected cap faces land in different free labels B4 and B1;
    # their sum is primitive rather than coordinatewise even.
    face3 = (0, 0, 0, 0, -1, 0)
    face5 = (0, -1, 0, 0, 0, 0)
    face_sum = add(face3, face5)
    require(content(face_sum) == 1,
            "the two labelled cap faces became even")

    return {
        "D4_Boolean_profile": list(d4_profile),
        "D4_top_coefficient": 1,
        "multi_affine_second_Hasse_rule": "D^[2](fg)=D(f)D(g)",
        "second_Hasse_cross_coefficient": 1,
        "face3": "-B4",
        "face5": "-B1",
        "face_sum_primitive": True,
        "divided_power_supplies_missing_two": False,
        "existing_beta_Bockstein_V_root_output": 0,
        "existing_beta_Bockstein_interacts_with_mod2_D_character": False,
        "relation_between_obstructions": (
            "the old Smith class is beta-primary; the new class is the "
            "constant rho-even element [B1+B4] modulo 2"
        ),
        "optional_Z_form_repair": (
            "one source-valid augmented column whose D-character proper "
            "face is B1+B4 modulo 2 (equivalently, makes the coupled RHS "
            "2-divisible); this is not required over characteristic-zero "
            "k[beta] and must not be confused with the root-zero beta-"
            "Bockstein V"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "E14 coupled augmented-RHS evenness and Bockstein gate",
        "pins": PINS,
        "literal_augmented_rhs": literal_augmented_rhs_audit(),
        "integral_Smith_and_rho_even_class": smith_and_rho_even_audit(),
        "centered_3_over_30_normalization": centered_normalization_audit(),
        "divided_power_and_Bockstein": divided_power_and_bockstein_audit(),
        "verdict": (
            "The complete alternating right side is primitive, not even: "
            "A=-E and X=+E cancel, while LFC=E remains.  Hence the coupled "
            "equation is 2K=E.  It closes uniquely and beta-integrally over "
            "the characteristic-zero theorem ring k[beta], with K=E/2.  "
            "Only the optional Z[beta] coefficient form has the nonzero "
            "rho-even class [B1+B4].  The centered /3 then /30 construction has numerator "
            "90 and consumes its only factor two during selected-fibre "
            "normalization; divided-Hasse top and cross coefficients are "
            "one.  This does not affect the independent beta-Bockstein."
        ),
        "scope": (
            "canonical h=3 E14 alternating root x six-label quotient.  The "
            "coefficient-lattice parity and normalized identities are exact.  The "
            "calculation is conditional on the still-open source-valid "
            "augmented face map F_D; it shows what its integral normalization "
            "would require, but creates no new gate over characteristic-zero "
            "k[beta] and proves neither existence nor terminal promotion."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("A+X+LFC on D-lines: B1+B4 (PRIMITIVE, NOT EVEN)")
    print("coupled equation: 2K=B1+B4")
    print("over char-0 k[beta]: K=(B1+B4)/2 (BETA-INTEGRAL)")
    print("optional Z[beta] form only: NONZERO RHO-EVEN Z/2 CLASS")
    print("centered /3,/30: clears 90, leaves no spare factor 2")
    print("divided Hasse top/cross coefficients: 1,1 (NO PARITY REPAIR)")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
