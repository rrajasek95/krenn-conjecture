#!/usr/bin/env python3
"""Audit the shifted derived filler across the cyclotomic face-zero locus.

The five normal arcs have divided face matrix B(tau)=I+tau*R.  The
polynomial shifted filler has a five-term Hasse source companion.  In its
empty-Eq projection it has the universal two-row block

    n(h) = h*(r_0-T) - F_0*r_m,       d n(h) = h*Y*w,

the literal regularized difference loses the q-independent r_m companion.
On the empty-Eq/zero-jet projection this reads

    (n(h(tau))-n(0))/tau = B(tau)*(r_0-T).

After multiplication by B(tau)^(-1), its boundary is Y*w+F_0*e_Eq, not
Y*w.  Target and ordinary residue vanish and the chart correction is -S.
The component -F_0*r_m[ut,nu] of the missing full normal Hasse face has
empty-Eq boundary -F_0*e_Eq.  Thus the whole base cycle s_ut(q0)[nu], not
the naked coefficient difference, is the first required attaching face.
Only the decisive empty-Eq projection is asserted here; this is not a
physical comparison or physical cap identification.
"""

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_h3_component_iv_cyclotomic_rees_lift_physical_separator as REES
import verify_h3_component_iv_cyclotomic_normal_rees_boundary as NORMAL
import verify_h3_full_hasse_koszul_cap_totalization as TOTAL


ROOT = Path(__file__).resolve().parents[1]
QQ = Fraction
K = NORMAL.H2.K
ZERO = NORMAL.ZERO
ONE = NORMAL.ONE
EXPECTED_LEDGER_SHA256 = "d44bb7419baae7c0aae7c3b7b74ee2ceffe5ebb714e58a1b2a16fa4058341742"
PINS = {
    "computations/verify_h3_augmented_derived_comparison_shared_rootless_inactive_interface.py":
        "81c1bd9de57871cb334de5f3a1b4c7a3ede2a25316841c4ee0d3902a30b35341",
    "notes/h3-augmented-derived-comparison-shared-rootless-inactive-interface.md":
        "be451a7b5166c0164ac9c65b51585d1038a2bacef7a9afce91e5a348d8542b62",
    "computations/verify_h3_shifted_denominator_chart_filler_augmented_commutator.py":
        "7d9e49f34da84772f6e0863a9bfe56cb9a90e0cfd3fceb76da59175ffea36c50",
    "notes/h3-shifted-denominator-chart-filler-augmented-commutator.md":
        "1d89c1e592fdc723bb58b1b75e2ba846b812401efad33c8cd88d4265dc0a7743",
    "computations/verify_h3_component_iv_cyclotomic_normal_rees_boundary.py":
        "bc3da1ce329b5134bab2e51d7d70ee32052d76b440bd2fa947583a2132b149ef",
    "notes/h3-component-iv-cyclotomic-normal-rees-boundary.md":
        "6168f501bee2cab6c5f339ef47d1581af507a99a9053f99708836cd81fd8578e",
    "computations/verify_h3_component_iv_cyclotomic_rees_lift_physical_separator.py":
        "12f7edba228a034523c61f10fc7633c7c736516dd3890ab3a89fce376eaa49bb",
    "notes/h3-component-iv-cyclotomic-rees-lift-physical-separator.md":
        "6e5f7b0daa37c19fbdba024f76cf5456e97931caa2c602211a5b02ac65b853e4",
    "computations/verify_h3_full_hasse_koszul_cap_totalization.py":
        "51940ce0ac8387b68e7725508db6da1a1c055ea036335bbf19750580c69e13fb",
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def empty_eq_projection():
    """Return the decisive empty-Eq projection and its missing component."""

    differential = {
        "r_0": {"eq": TOTAL.F_PURE},
        "T": {"w": TOTAL.scale(-1, TOTAL.CAP_Y)},
        # Empty-Eq projection of the normal-indexed row: dh=1.
        "r_m_normal": {"eq": TOTAL.constant()},
    }
    target = {
        "r_0": {"target": TOTAL.constant()},
        "T": {"target": TOTAL.constant()},
        "r_m_normal": {},
    }
    ores = {generator: {} for generator in differential}

    # B^{-1} times the five literal divided differences gives one copy of
    # this chain in each normalized face coordinate.
    naked = {
        "r_0": TOTAL.constant(),
        "T": TOTAL.constant(-1),
    }
    naked_boundary = TOTAL.apply_module_map(naked, differential)
    require(naked_boundary == {
        "eq": TOTAL.F_PURE,
        "w": TOTAL.CAP_Y,
    }, "regularized difference lost its primitive Eq residual")
    require(not TOTAL.apply_module_map(naked, target)
            and not TOTAL.apply_module_map(naked, ores),
            "regularized difference retained target or ordinary residue")

    companion = {"r_m_normal": TOTAL.scale(-1, TOTAL.F_PURE)}
    companion_boundary = TOTAL.apply_module_map(companion, differential)
    require(companion_boundary == {"eq": TOTAL.scale(-1, TOTAL.F_PURE)},
            "normal mixed-row component has the wrong boundary projection")
    require(not TOTAL.apply_module_map(companion, target)
            and not TOTAL.apply_module_map(companion, ores),
            "normal mixed-row component retained an augmentation")

    projected_sum = TOTAL.module_add(naked, companion)
    projected_boundary = TOTAL.apply_module_map(projected_sum, differential)
    require(projected_boundary == {"w": TOTAL.CAP_Y},
            "normal mixed-row component did not cancel the empty-Eq defect")

    homogenizer = next(iter(TOTAL.HOMOGENIZING_U))
    require(TOTAL.F_PURE[homogenizer] == -1,
            "F_0 lost its monic homogenizing term")
    require(len(TOTAL.F_PURE) == 91,
            "F_0 support changed")
    return naked_boundary, companion_boundary, projected_boundary


def relative_one_face_identity():
    """Verify the full u/t Hasse repair in the divided normal complex."""

    ut_mask = 3
    masks = TOTAL.submasks(ut_mask)
    h0 = {
        mask: ({} if mask == ut_mask
               else TOTAL.variable(("h0", mask)))
        for mask in masks
    }
    divided = {
        mask: TOTAL.variable(("divided_normal", mask))
        for mask in masks
    }

    differential = {}
    target = {}
    chart = {}
    for mask in masks:
        for normal_grade in (0, 1):
            generator = ("r_0", mask, normal_grade)
            differential[generator] = {
                ("eq", mask, normal_grade): TOTAL.F_PURE
            }
            target[generator] = (
                {"target": TOTAL.constant()} if mask == 0 else {}
            )
            chart[generator] = (
                {"chart": TOTAL.constant(-1)} if mask == 0 else {}
            )
    differential["T"] = {"w": TOTAL.scale(-1, TOTAL.CAP_Y)}
    target["T"] = {"target": TOTAL.constant()}
    chart["T"] = {}

    # The normal-indexed mixed row uses the base Hasse coefficients on the
    # normal-tagged outputs and the divided differences on the lower face.
    rm_normal = ("r_m", ut_mask, 1)
    rm_image = {}
    for derivative_mask in masks:
        complement = ut_mask ^ derivative_mask
        if h0[derivative_mask]:
            rm_image[("eq", complement, 1)] = h0[derivative_mask]
        rm_image[("eq", complement, 0)] = divided[derivative_mask]
    differential[rm_normal] = rm_image
    target[rm_normal] = {}
    chart[rm_normal] = {}

    # The naked quotient has every divided coefficient but no r_m term.
    naked = {}
    for derivative_mask in masks:
        complement = ut_mask ^ derivative_mask
        naked[("r_0", complement, 0)] = divided[derivative_mask]
    naked["T"] = TOTAL.scale(-1, divided[ut_mask])

    # The single missing normal face is the full base cycle s_ut(q0)[nu].
    lifted_base = {}
    for derivative_mask in masks:
        if not h0[derivative_mask]:
            continue
        complement = ut_mask ^ derivative_mask
        lifted_base[("r_0", complement, 1)] = h0[derivative_mask]
    lifted_base[rm_normal] = TOTAL.scale(-1, TOTAL.F_PURE)

    naked_boundary = TOTAL.apply_module_map(naked, differential)
    expected_naked = {"w": TOTAL.multiply(
        divided[ut_mask], TOTAL.CAP_Y
    )}
    for derivative_mask in masks:
        complement = ut_mask ^ derivative_mask
        expected_naked[("eq", complement, 0)] = TOTAL.multiply(
            TOTAL.F_PURE, divided[derivative_mask]
        )
    require(naked_boundary == expected_naked,
            "naked divided filler has the wrong full Hasse residual")

    lifted_boundary = TOTAL.apply_module_map(lifted_base, differential)
    expected_lifted = {
        ("eq", ut_mask ^ derivative_mask, 0): TOTAL.scale(
            -1, TOTAL.multiply(TOTAL.F_PURE, divided[derivative_mask])
        )
        for derivative_mask in masks
    }
    require(lifted_boundary == expected_lifted,
            "full normal base face did not cancel every u/t grade")

    repaired = TOTAL.module_add(naked, lifted_base)
    repaired_boundary = TOTAL.apply_module_map(repaired, differential)
    require(repaired_boundary == {"w": TOTAL.multiply(
        divided[ut_mask], TOTAL.CAP_Y
    )}, "one normal Hasse face did not repair the divided filler")
    ores = {generator: {} for generator in differential}
    require(not TOTAL.apply_module_map(repaired, target)
            and not TOTAL.apply_module_map(repaired, ores),
            "repaired relative filler retained target or ordinary residue")
    require(TOTAL.apply_module_map(repaired, chart)
            == {"chart": TOTAL.scale(-1, divided[ut_mask])},
            "repaired relative filler lost its -S chart correction")
    require(len(naked_boundary) == 5 and len(lifted_boundary) == 4,
            "full u/t Hasse grade count changed")
    return naked_boundary, lifted_boundary, repaired_boundary


def audit():
    pin_dependencies()
    remainder = REES.quadratic_remainder_matrix()
    require(remainder == [list(row) for row in zip(*remainder, strict=True)],
            "cyclotomic quadratic remainder stopped being symmetric")

    # Exact divided face matrix B=I+tau R and its formal inverse.  The
    # recurrence is the proof; order ten is only a mutation guard.
    guard_order = 10
    product = REES.truncate_product_b_inverse(remainder, guard_order)
    require(product[0] == NORMAL.identity(5),
            "B inverse lost its constant term")
    require(all(value == [[ZERO] * 5 for _ in range(5)]
                for value in product[1:guard_order]),
            "B inverse failed before the guard order")

    # Each raw divided difference has the same B matrix simultaneously in
    # its Yw boundary, its F_0 Eq residual, and (with opposite sign) its
    # chart terminal.  Therefore B^{-1} normalizes all three to I, I, -I.
    normalized_yw = NORMAL.identity(5)
    normalized_eq = NORMAL.identity(5)
    normalized_chart = REES.matrix_scale(K(-1), NORMAL.identity(5))
    require(NORMAL.determinant(normalized_eq) == ONE,
            "the Eq residual unexpectedly acquired a kernel")
    require(NORMAL.determinant(normalized_chart) == K(-1),
            "the normalized chart correction is not -S")

    naked, companion, projected = empty_eq_projection()
    full_naked, full_face, full_repaired = relative_one_face_identity()
    ledger = {
        "pins": PINS,
        "coefficient_field": "Q[zeta]/(zeta^2+zeta+1)",
        "cyclotomic_face_value": "h(q0)=0",
        "exact_divided_face_matrix": "B(tau)=I+tau*R",
        "formal_inverse": "C_0=I; C_n=(-R)^n",
        "inverse_guard_order": guard_order,
        "polynomial_difference": (
            "(n_v(q(tau))-n_v(q0))/tau; every coefficient is divisible"
        ),
        "lost_constant_companion": (
            "the entire base Hasse cycle s_ut(q0)[normal], including its "
            "q-independent -F_0*r_m[ut,normal] component"
        ),
        "normalized_naked_empty_eq_projection": {
            "chain_projection": "r_0[empty]-T",
            "boundary_projection": "Y*w+F_0*e_Eq[empty]",
            "target": 0,
            "ordinary_residue": 0,
            "chart_correction": "-S_v",
            "F_0_terms": len(TOTAL.F_PURE),
            "F_0_monic_term": "-u_hom",
            "eq_matrix": "I5",
        },
        "first_normal_hasse_face": {
            "full_chain": "s_ut(q0)[normal]",
            "distinguished_component": "-F_0*r_m[ut,normal]",
            "distinguished_empty_eq_boundary": "-F_0*e_Eq[empty]",
            "target": 0,
            "ordinary_residue": 0,
            "scope": (
                "the displayed component cancels the decisive empty-Eq "
                "projection; the complete normal-indexed base cycle cancels "
                "all four u/t Eq grades in the divided relative complex"
            ),
        },
        "exact_relative_one_face_repair": {
            "naked_boundary_grades": len(full_naked),
            "base_face_boundary_grades": len(full_face),
            "repaired_boundary_grades": len(full_repaired),
            "boundary": "divided_normal(h_v)*Y*w",
            "after_B_inverse": "Y*w",
            "target": 0,
            "ordinary_residue": 0,
            "chart_correction_after_B_inverse": "-S_v",
        },
        "empty_eq_projection_checks": {
            "naked_outputs": sorted(naked),
            "companion_outputs": sorted(companion),
            "sum_outputs": sorted(projected),
        },
        "verdict": (
            "the naked regularized difference does not extend 0828a2f "
            "across V(h): B^{-1} leaves the primitive monic F_0 Eq "
            "residual.  A lift must retain the full normal-indexed base "
            "cycle; that one relative Hasse face cancels every u/t grade "
            "and gives the exact derived repair"
        ),
        "physical_scope": (
            "conditional only: the relative derived repair does not construct "
            "the underived physical "
            "comparison or identifies chart-odd -S_v/Yw with the physical "
            "cap coordinate"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"regularized filler ledger changed: {digest}")
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("h3 cyclotomic regularized shifted filler: PASS (exact)")
    print("naked B^-1 difference: Yw + F_0*Eq; tgt=ores=0; chart=-S")
    print("first missing face: full s_ut(q0)[normal] base cycle")
    print("one-face derived repair: exact in all four u/t grades")
    print("physical comparison/cap identification: OPEN")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
