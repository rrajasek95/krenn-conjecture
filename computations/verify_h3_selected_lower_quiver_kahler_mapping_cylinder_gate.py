#!/usr/bin/env python3
"""Build the minimal pq/xv quiver-valued Kahler mapping cylinder.

The marked clean-C5 chart is D(t), with

    t=q_pq^00,  u=q_xv^00.

In the ordinary N^8 grading the two ridge halves cannot be added.  In the
two-object grade category there is instead a regular arrow

    U=u/t : L_pq -> L_xv

on D(t).  Its first-principal-parts prolongation is the 2-by-2 jet matrix

                    [ U   0 ]
            J1(U) = [ dU  U ].

The dU entry is the unique Leibniz diagonal.  The pinned Cartan/order-six
operator commutes with U and dU, so it supplies no further mixed diagonal.
The complete Hasse/Koszul totalization already realizes the analogous
two-direction square in the derived presentation.  Its projection to the
underived physical source still leaves the pinned monic Eq commutator.

Replacing this cylinder by a flat toric identification is valid only on
D(tu).  The connection d-dlog(U) has logarithmic residue -1 at u=0, and the
contragredient terminal transport uses U^-1=t/u.  The canonical clean-C5
chart assumes only t invertible, so neither operation is globally regular.

Finally, physical q extends across any physically descended cylinder Phi
iff q_xv Phi-q_pq is a protected row.  This is the exact q-cocycle condition;
a nonzero quotient class has a protected-kernel witness once both domains
are physical.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_selected_lower_rees_normal_sign_connection_gate.py":
        "b2776fb92a37188613afd7dc4315297d541ec7232a86812cc550c473aedcbad2",
    "computations/verify_h3_residual_q_order6_ridge_jet_commutation.py":
        "00a0798b4aa1d901b52645cac3f1dbe2854a3d8ce796191f7a4ff9a6e295b28f",
    "computations/verify_h3_shifted_denominator_chart_filler_augmented_commutator.py":
        "7d9e49f34da84772f6e0863a9bfe56cb9a90e0cfd3fceb76da59175ffea36c50",
    "computations/verify_h3_rootless_eta_character_source_interface.py":
        "2357e1a4e1c22c4496d99be12b8bf49deea3838337743ea849da29757508517c",
    "computations/verify_h3_rootless_marked_first_jet_site_euler_correction.py":
        "4c6feb11113fe15dfba45b1dae1bf9e80acd2231b10fee8cb9fe5e4c4d0cd554",
    "computations/verify_h3_rootless_clean_c5_separator_endpoint_kernel_boundary.py":
        "a98c6e0e90127e81e869c68342f3999abbbd8898d2b2eeafbeccbad06575a324",
    "computations/verify_dark_cartan_physical_q_protected_quotient_comparison.py":
        "eb56cdb4ab1915f8ce35ab3acf0398b4f526c52a17c9c8ebafcc7a5ad4f86bcc",
    "computations/verify_h3_tau_plus_full_interface_product_bianchi_extension_gate.py":
        "32be7ef48ad9d35b8863a62889508ccdff0010d8ebff18b366e932aab8b2bf14",
    "computations/verify_h3_generic_cartan_adjacent_target_label_prolongation.py":
        "ef63bd26210802cf300e263da44e178b4dd19abbf0fa5bba059b5d61afb9b782",
    "computations/verify_h3_trapped_carrier_occurrence_graph_hessian_cone_gate.py":
        "ce28ff5d25bf575c280a21c0e35c6dc1ebef54eb039ac94cdc25932a61b95829",
    "computations/verify_h3_selected_lower_relative_weyl_bar_gate.py":
        "7a6f2afebcacc5924110e32a3f7d9c225992f07abae637d4529b5436c64cc294",
}
EXPECTED_LEDGER_SHA256 = (
    "77682303f22772e43968fe70065620639689a0af0b5d33a1451c1a2c643a00ea"
)

# Laurent exponent order is (t,u,a,b).  On the canonical D(t) chart only
# the t exponent may be negative.
T, UCOORD, A, B = range(4)
VARIABLES = ("t", "u", "a", "b")


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def clean(poly):
    return {exponent: Q(value) for exponent, value in poly.items() if value}


def monomial(exponents, coefficient=1):
    return clean({tuple(exponents): Q(coefficient)})


def add(left, right, scale=Q(1)):
    answer = dict(left)
    for exponent, value in right.items():
        answer[exponent] = answer.get(exponent, Q(0)) + scale * value
    return clean(answer)


def multiply(left, right):
    answer = {}
    for left_exp, left_value in left.items():
        for right_exp, right_value in right.items():
            exponent = tuple(a + b for a, b in zip(
                left_exp, right_exp, strict=True
            ))
            answer[exponent] = answer.get(exponent, Q(0)) + (
                left_value * right_value
            )
    return clean(answer)


def scale(value, poly):
    return clean({exponent: Q(value) * coefficient
                  for exponent, coefficient in poly.items()})


def derivative(poly):
    """Universal differential as a dict basis-index -> Laurent polynomial."""
    answer = {index: {} for index in range(4)}
    for exponent, coefficient in poly.items():
        for index, power in enumerate(exponent):
            if not power:
                continue
            next_exponent = list(exponent)
            next_exponent[index] -= 1
            answer[index] = add(answer[index], monomial(
                next_exponent, coefficient * power
            ))
    return {index: poly for index, poly in answer.items() if poly}


def form_add(left, right, scale_value=Q(1)):
    answer = dict(left)
    for basis, coefficient in right.items():
        answer[basis] = add(answer.get(basis, {}), coefficient, scale_value)
        if not answer[basis]:
            del answer[basis]
    return answer


def form_multiply(poly, form):
    return {basis: multiply(poly, coefficient)
            for basis, coefficient in form.items() if coefficient}


def contraction(form, vector):
    answer = {}
    for basis, coefficient in form.items():
        answer = add(answer, multiply(coefficient, vector.get(basis, {})))
    return answer


ONE = monomial((0, 0, 0, 0))
t = monomial((1, 0, 0, 0))
u = monomial((0, 1, 0, 0))
a = monomial((0, 0, 1, 0))
b = monomial((0, 0, 0, 1))
t_inverse = monomial((-1, 0, 0, 0))
u_inverse = monomial((0, -1, 0, 0))
grade_arrow = multiply(u, t_inverse)       # U=u/t, regular on D(t).
inverse_arrow = multiply(t, u_inverse)     # T=t/u, only on D(tu).


def regular_on_Dt(poly):
    return all(exponent[UCOORD] >= 0 for exponent in poly)


def localization_and_jet_audit():
    require(regular_on_Dt(grade_arrow), "u/t stopped being regular on D(t)")
    require(not regular_on_Dt(inverse_arrow),
            "t/u became regular without localizing u")
    require(multiply(grade_arrow, inverse_arrow) == ONE,
            "the two overlap transition functions stopped being inverse")

    f = add(a, t, -1)  # pq ridge potential r_p=a-t.
    left = derivative(multiply(grade_arrow, f))
    right = form_add(
        form_multiply(grade_arrow, derivative(f)),
        form_multiply(f, derivative(grade_arrow)),
    )
    require(left == right, "the first-jet product rule changed")

    diagonal = form_multiply(f, derivative(grade_arrow))
    require(diagonal and diagonal == {
        T: add(scale(-1, multiply(
            a, multiply(u, monomial((-2, 0, 0, 0))))),
            multiply(u, t_inverse)),
        UCOORD: add(multiply(a, t_inverse), ONE, -1),
    }, ("the forced dU diagonal changed", diagonal))

    # The flat connection on the overlap: nabla=d-dlog(U).  Applying it to
    # U*f removes exactly the Leibniz diagonal.
    dlog_u = {UCOORD: u_inverse}
    dlog_t = {T: t_inverse}
    dlog_grade_arrow = form_add(dlog_u, dlog_t, -1)
    covariant = form_add(
        derivative(multiply(grade_arrow, f)),
        form_multiply(multiply(grade_arrow, f), dlog_grade_arrow),
        -1,
    )
    require(covariant == form_multiply(grade_arrow, derivative(f)),
            "the toric connection failed to remove the Leibniz diagonal")
    require(not all(regular_on_Dt(coefficient)
                    for coefficient in dlog_grade_arrow.values()),
            "dlog(u/t) became regular across u=0")

    # Connection form is -dlog(U), so its du/u residue is -1.  This is the
    # normalized dual of Omega^1(log{u=0}) / Omega^1 at the divisor.
    connection_form = {basis: scale(-1, coefficient)
                       for basis, coefficient in dlog_grade_arrow.items()}
    du_coefficient = connection_form[UCOORD]
    residue = du_coefficient.get((0, -1, 0, 0), Q(0))
    require(residue == -1, "the logarithmic residue obstruction changed")

    return {
        "base_chart": "D(t), t=q_pq^00",
        "u_inverted_by_canonical_chart": False,
        "regular_grade_arrow": "U=u/t : L_pq -> L_xv",
        "inverse_grade_arrow": "T=t/u exists only on D(tu)",
        "first_jet_matrix": "[[U,0],[dU,U]]",
        "unique_Leibniz_diagonal": "f*dU for every pq coefficient f",
        "sample_f": "a-t",
        "sample_diagonal_nonzero": True,
        "flat_overlap_connection": "nabla=d-dlog(U)",
        "overlap_curvature": 0,
        "regular_extension_across_u_zero": False,
        "logarithmic_residue_at_u_zero": str(residue),
        "normalized_residue_dual": (
            "Res_(u=0) kills regular one-forms and reads -1 on the "
            "connection form"
        ),
    }


def terminal_transport_audit():
    r_pq = add(a, t, -1)
    r_xv = add(b, u, -1)
    gamma = form_add(derivative(r_pq), derivative(r_xv), -1)
    gamma = {basis: scale(-1, coefficient)
             for basis, coefficient in gamma.items()}
    # The preceding two lines give -d(r_pq-r_xv)=-dr_pq+dr_xv.

    # eta_delta(t)=1, eta_delta(u)=-delta*u/t; a,b are fixed.
    terminal_records = []
    for delta in (0, 1):
        eta = {
            T: ONE,
            UCOORD: scale(-delta, grade_arrow),
        }
        sigma = {A: a}
        original_eta = contraction(gamma, eta)
        original_sigma = contraction(gamma, sigma)
        expected_eta = add(ONE, grade_arrow, delta)
        require(original_eta == expected_eta and original_sigma == scale(-1, a),
                ("the unshifted terminal law changed", delta,
                 original_eta, original_sigma))

        # Collapse the pq half into L_xv by U.  The flat connection makes
        # this covariant, but an ordinary scalar readout sees the U factor.
        shifted = form_add(
            form_multiply(grade_arrow, derivative(r_pq)),
            derivative(r_xv),
            -1,
        )
        shifted = {basis: scale(-1, coefficient)
                   for basis, coefficient in shifted.items()}
        shifted_eta = contraction(shifted, eta)
        shifted_sigma = contraction(shifted, sigma)
        require(shifted_eta == scale(1 + delta, grade_arrow)
                and shifted_sigma == scale(-1, multiply(grade_arrow, a)),
                ("shifted scalar terminal law changed", delta,
                 shifted_eta, shifted_sigma))
        require(shifted_eta != original_eta
                and shifted_sigma != original_sigma,
                "scalar grade collapse unexpectedly preserved terminals")
        terminal_records.append({
            "delta_vz": delta,
            "original_eta": "1+delta*u/t",
            "collapsed_eta": "(1+delta)*u/t",
            "original_sigma": "-a",
            "collapsed_sigma": "-(u/t)*a",
        })

    return {
        "records": terminal_records,
        "failure_on_u_zero": (
            "the collapsed pq contribution vanishes, while eta retains "
            "the constant 1 and sigma retains -a"
        ),
        "contragredient_repair": "multiply the pq terminal covector by U^-1=t/u",
        "contragredient_regular_on_Dt": False,
        "quiver_valued_terminal_solution": (
            "retain pq and xv readouts objectwise in the mapping cylinder; "
            "do not collapse them to one scalar line"
        ),
    }


def cartan_and_physical_descent_audit():
    ridge_source = (ROOT / (
        "computations/verify_h3_residual_q_order6_ridge_jet_commutation.py"
    )).read_text()
    shifted_source = (ROOT / (
        "computations/verify_h3_shifted_denominator_chart_filler_augmented_commutator.py"
    )).read_text()
    require("[Theta_6,M_x]=0 and [Theta_6,d x]=0" in ridge_source,
            "the pinned strict Cartan/ridge commutator changed")
    require("diagonal_projection_commutator\": \"(H_0-u)*eq\""
            in shifted_source,
            "the pinned underived shifted-square residual changed")
    return {
        "horizontal_operator": "endpoint-sign Cartan/order-six connection kappa_xi",
        "vertical_first_jet": "J1(U)=[[U,0],[dU,U]]",
        "known_commutators": ["[Theta_6,U]=0", "[Theta_6,dU]=0"],
        "extra_horizontal_vertical_diagonal": 0,
        "forced_vertical_Leibniz_diagonal": "dU (new PP square entry)",
        "known_Cartan_commutator_supplies_dU": False,
        "derived_presentation": {
            "two_direction_Hasse_Koszul_square": True,
            "target": 0,
            "ordinary_residue": 0,
            "unique_shift_sites": [0, 6, 7],
        },
        "underived_physical_projection": {
            "constructed": False,
            "first_residual": "(H_0-u)*e_Eq at the q-zero top",
            "full_initial_residual_terms": 273,
            "interpretation": (
                "the derived PP cylinder exists, but its comparison to the "
                "literal underived physical source is the new square"
            ),
        },
    }


def shared_reduced_eq_orbit_audit():
    """Compare the odd Gate-I and even Interface-III Eq corrections."""
    # A single raw rho orbit has the regular representation Q{c,rho*c}.
    # Its odd/even projections are independent one-dimensional summands.
    raw_left = (Q(1), Q(0))
    raw_right = (Q(0), Q(1))
    rho = ((Q(0), Q(1)), (Q(1), Q(0)))

    def mat_vec(matrix, vector):
        return tuple(sum(a * b for a, b in zip(row, vector, strict=True))
                     for row in matrix)

    odd = tuple(a - b for a, b in zip(raw_left, raw_right, strict=True))
    even = tuple(a + b for a, b in zip(raw_left, raw_right, strict=True))
    require(mat_vec(rho, odd) == tuple(-value for value in odd)
            and mat_vec(rho, even) == even
            and rank((odd, even)) == 2,
            "the shared reduced-Eq orbit lost its parity splitting")

    # Let e=(H0-u)e_Eq.  The underived Gate-I cylinder leaves +e, so its
    # missing core correction C_- must have dC_-=-e in the odd summand.
    # Interface III's old formal filler is decorated by -2 D tensor v and
    # also leaves -2D*e tensor v.  Decorating the *same sign* core equation
    # dC=-e by -2D tensor v gives +2D*e tensor v, exactly the pinned missing
    # correction.
    root_defect = (Q(-1), Q(1), Q(-1), Q(1))
    v = (Q(0), Q(1, 2), Q(0), Q(0), Q(1, 2), Q(0))
    decoration = tuple(-2 * d * label for d in root_defect for label in v)
    decorated_core_boundary = tuple(-coefficient for coefficient in decoration)
    required_even_eq = tuple(2 * d * label
                             for d in root_defect for label in v)
    require(decorated_core_boundary == required_even_eq
            and sum(value != 0 for value in required_even_eq) == 8,
            "the shared core sign stopped giving Interface III's Eq face")

    # Augmentation rows which factor through the rho-even quotient vanish on
    # C_- and may remain nonzero on C_+.  This is compatible with Gate I's
    # protected-zero target/ores/anchor and Interface III's target-bearing,
    # labelled-ores even packet.  It does not construct those decorations.
    even_functional = (Q(1), Q(1))
    require(sum(a * b for a, b in zip(even_functional, odd, strict=True)) == 0
            and sum(a * b for a, b in zip(even_functional, even,
                                          strict=True)) == 2,
            "an even augmentation stopped distinguishing the two parities")
    return {
        "common_underived_row": "e=(H_0-u)*e_Eq",
        "raw_equivariant_family": "Q{C,rho C}, one rho orbit of dimension two",
        "odd_projection": {
            "generator": "C_-=C-rho C",
            "boundary_needed": "dC_-=-e_-",
            "use": "cancels the +e_- Gate-I quiver-cylinder residual",
            "target_ores_anchor_from_even_rows": 0,
        },
        "even_projection": {
            "generator": "C_+=C+rho C",
            "boundary_needed": "dC_+=-e_+",
            "decoration": "-2D tensor v",
            "resulting_boundary": "+2D(H_0-u)Eq tensor v",
            "matches_Interface_III_exactly": True,
        },
        "minimum_equivariant_source_orbits": 1,
        "minimum_vector_space_dimension": 2,
        "one_parity_line_implies_the_other": False,
        "unification": (
            "one source-valid regular rho-orbit of reduced-Eq mapping-cone "
            "cells would provide both parity projections"
        ),
        "does_not_yet_supply": [
            "Gate-I private boundary and eta/sigma",
            "Interface-III delta_plus full-nine tail",
            "Interface-III mixed target -2D tensor v",
            "Interface-III labelled ordinary residue v",
            "Interface-III W/anchor/ridge/word faces",
        ],
    }


def site_permutation_groupoid_audit():
    """Test whether pq->xv site symmetry supplies the vertical arrow."""
    sites = tuple(range(8))
    pq_sites = frozenset((6, 7))
    repeated_sites = frozenset((3, 7))
    middle = {1: 1, 2: 2, 3: 1, 4: 1, 5: 2}
    profile_preserving = []
    edge_maps = {face: 0 for face in middle}
    commuting_endpoint_sign = 0
    s = {0: 1, 1: 0, **{site: site for site in sites if site not in (0, 1)}}

    for values in permutations(sites):
        image_pq = frozenset((values[6], values[7]))
        face = next((face for face in middle
                     if image_pq == frozenset((0, face))), None)
        if face is None:
            continue
        edge_maps[face] += 1
        image_repeated = frozenset(values[site] for site in repeated_sites)
        if image_repeated != repeated_sites:
            continue
        profile_preserving.append((values, face))
        if all(values[s[site]] == s[values[site]] for site in sites):
            commuting_endpoint_sign += 1
    require(edge_maps == {face: 1440 for face in middle}
            and len(profile_preserving) == 120
            and {face for _values, face in profile_preserving} == {3}
            and commuting_endpoint_sign == 0,
            ("the pq/xv site-permutation census changed", edge_maps,
             len(profile_preserving), commuting_endpoint_sign))

    # Site permutations and one global colour permutation preserve equality
    # of the endpoint colours.  They can send 00->00 (if zero is fixed), but
    # can never send 22 to 0,m_v because m_v is nonzero.  Exhaust S3.
    color_records = []
    for color_perm in permutations((0, 1, 2)):
        t_image = (color_perm[0], color_perm[0])
        a_image = (color_perm[2], color_perm[2])
        for face, m_v in middle.items():
            color_records.append((
                color_perm, face,
                t_image == (0, 0),
                a_image == (0, m_v),
            ))
    require(any(record[2] for record in color_records)
            and not any(record[3] for record in color_records),
            "a global colour relabelling began mapping pq22 to xv0m")

    # A local recolouring can make the two endpoint colours distinct, but
    # then it is not a common colour permutation and moves a pure GHZ word
    # to a mixed word.  Thus it is orbit-relative, not a fixed-fibre map.
    return {
        "GHZ_target_under_site_permutations": "fixed",
        "site_permutations_mapping_pq_to_each_xv_edge": edge_maps,
        "site_permutations_also_preserving_kappa_repeated_profile": len(
            profile_preserving
        ),
        "only_profile_compatible_face": 3,
        "profile_compatible_permutations_commuting_with_endpoint_sign_swap": 0,
        "plain_site_plus_global_colour_maps_t_to_u": True,
        "plain_site_plus_global_colour_maps_a22_to_b0m": False,
        "fine_label_obstruction": (
            "equal decoration 22 remains equal under every global colour "
            "permutation, whereas xv carries the mixed decoration 0,m_v"
        ),
        "local_recolouring_needed": True,
        "local_recolouring_preserves_GHZ_fixed_fibre": False,
        "double_bar_square": (
            "the site permutation does not commute with the endpoint-sign "
            "swap; its group commutator is a new diagonal orbit face"
        ),
        "eta_sigma_transport": (
            "t/u labels transport only on the 00 half; the a/b ridge and "
            "their eta/sigma covectors require the same missing local-root comparison"
        ),
        "physical_q_transport": (
            "not canonical: the permutation exchanges external and C5 "
            "internal roles, so the selected six-matching and ainc rows move"
        ),
        "verdict": (
            "site symmetry supplies an orbit-relative presentation arrow, "
            "not the fixed physical shifted-Kahler arrow"
        ),
    }


def interface_ii_projection_guard():
    source = (ROOT / (
        "computations/verify_h3_trapped_carrier_occurrence_graph_hessian_cone_gate.py"
    )).read_text()
    require("[F_[2](xi)] in coker(A)" in source
            and "cannot be inferred from graph normalization" in source,
            "the Interface-II noncanonicity guard changed")
    return {
        "candidate_occurrence_projection": "[F_[2](xi)] in coker(A)",
        "identification_with_reduced_Eq_orbit_proved": False,
        "reason": (
            "the occurrence graph fixes A, df and its Hessian class but "
            "does not define a map from the output cokernel to the "
            "source-labelled reduced-Eq/six-term complex"
        ),
        "smallest_extra_square": (
            "a physically typed output-to-relative Spencer comparison on "
            "this one Hessian class"
        ),
    }


def rank(rows):
    work = [[Q(value) for value in row] for row in rows]
    if not work:
        return 0
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next((row for row in range(pivot_row, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def q_cocycle_mutation_guard():
    # Exhaust small protected maps and q defects.  A defect is in row(J), or
    # adding it raises rank and a kernel witness exists.  This is the finite
    # shadow of o_q=[q_xv Phi-q_pq] in D^*/row(J).
    cases = in_row = witness_cases = 0
    for height in range(1, 3):
        for width in range(1, 4):
            for entries in product((0, 1), repeat=height * width + width):
                protected = [list(entries[row * width:(row + 1) * width])
                             for row in range(height)]
                defect = list(entries[height * width:])
                old_rank = rank(protected)
                new_rank = rank(protected + [defect])
                if new_rank == old_rank:
                    in_row += 1
                else:
                    # Brute-force a small rational kernel witness.  Since
                    # the matrices are binary of width <=3, {-1,0,1}^n is
                    # sufficient for this mutation census.
                    witness = next((vector for vector in
                                    product((-1, 0, 1), repeat=width)
                                    if any(vector)
                                    and all(sum(a * b for a, b in zip(
                                        row, vector, strict=True)) == 0
                                            for row in protected)
                                    and sum(a * b for a, b in zip(
                                        defect, vector, strict=True)) != 0),
                                   None)
                    require(witness is not None,
                            ("q obstruction lost its kernel witness",
                             protected, defect))
                    witness_cases += 1
                require(new_rank in (old_rank, old_rank + 1),
                        "one q row changed rank by more than one")
                cases += 1
    require(cases == 668 and in_row == 280 and witness_cases == 388,
            ("q cocycle mutation census changed", cases, in_row,
             witness_cases))
    return {
        "complete_maps_checked": cases,
        "cocycle_cases": in_row,
        "obstructed_witness_cases": witness_cases,
        "physical_condition": (
            "o_q(Phi)=[q_xv*Phi-q_pq]=0 in D_pq^*/row(J_pq)"
        ),
        "vanishing_class": (
            "q_xv*Phi-q_pq=lambda*J_pq; this is the augmented cylinder "
            "cochain/homotopy"
        ),
        "nonvanishing_class": (
            "there is x in ker(J_pq) with nonzero q defect; after Phi and "
            "both q rows are physically typed, x or Phi*x is the relative generator"
        ),
        "square_cocycle": (
            "once J1(U) and the horizontal Cartan square are chain maps, "
            "edgewise q homotopies make the two-dimensional cocycle close; "
            "no additional scalar q value is forced by dU alone"
        ),
    }


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    localization = localization_and_jet_audit()
    terminal = terminal_transport_audit()
    descent = cartan_and_physical_descent_audit()
    shared_eq = shared_reduced_eq_orbit_audit()
    site_groupoid = site_permutation_groupoid_audit()
    interface_ii = interface_ii_projection_guard()
    q_gate = q_cocycle_mutation_guard()
    ledger = {
        "theorem": "two-object grade-quiver Kahler mapping-cylinder gate",
        "grade_category": {
            "objects": ["L_pq", "L_xv"],
            "regular_arrow_on_canonical_chart": "U=u/t",
            "horizontal_sign_connection": "kappa_xi",
            "vertical_Kahler_prolongation": "J1(U)",
            "total_bicomplex_vertices": 4,
            "minimal_nonvertex_entry": "one dU diagonal",
        },
        "localization_and_first_jet": localization,
        "terminal_naturality": terminal,
        "Cartan_square_and_physical_descent": descent,
        "shared_GateI_InterfaceIII_reduced_Eq_orbit": shared_eq,
        "site_permutation_groupoid_candidate": site_groupoid,
        "InterfaceII_occurrence_projection": interface_ii,
        "physical_q_cocycle": q_gate,
        "smallest_obstruction_and_dual": {
            "toric_isomorphism_route": (
                "the class of -du/u in Omega^1(log{u=0})/Omega^1, "
                "detected by Res_(u=0)=-1"
            ),
            "mapping_cylinder_route": (
                "the canonical dU diagonal is present in derived PP; its "
                "underived physical descent leaves (H_0-u)e_Eq"
            ),
            "q_route": "[q_xv*Phi-q_pq] modulo protected rows",
            "physical_separator_constructed": False,
        },
        "shortest_positive_lemma": (
            "work in the two-object pq/xv grade category and retain the "
            "principal-parts jet matrix [[U,0],[dU,U]].  The horizontal "
            "Cartan connection commutes with this matrix, and objectwise "
            "eta/sigma retain the exact ridge law.  Construct one physical "
            "regular rho-orbit C,rho C with dC=-(H0-u)e_Eq: its odd "
            "projection cancels Gate I, and its even projection decorated "
            "by -2D tensor v gives Interface III's exact +2D Eq repair.  "
            "The full augmented decorations and q defect must still descend"
        ),
        "verdict": (
            "the quiver formulation gives an exact minimal derived "
            "bicomplex, but not yet an underived physical cell.  A flat "
            "toric identification is only local on D(tu) and cannot preserve "
            "the terminal covectors across u=0.  The known Cartan commutator "
            "is zero; the required diagonal is the new, canonical dU "
            "principal-parts entry.  Gate I and Interface III share the "
            "same underived Eq core with opposite parity projections, so "
            "one two-dimensional regular rho orbit is the sharp unified "
            "source target.  Site permutation alone misses the mixed fine "
            "label and creates a group-commutator diagonal"
        ),
        "scope": (
            "exact Laurent/localization, first-jet, terminal, logarithmic-"
            "residue, Cartan-interchange, and q-quotient statements.  The "
            "derived-to-underived physical comparison and a physical dual "
            "to its Eq residual are not asserted"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("quiver Kahler cylinder ledger changed", digest))
    return ledger, digest


def main():
    ledger, digest = audit()
    print("h3 selected lower quiver/Kahler cylinder: EXACT DERIVED GATE")
    print("canonical D(t) arrow: U=u/t; inverse t/u: overlap only")
    print("minimal PP diagonal: dU; Cartan mixed diagonal: zero")
    print("flat toric descent across u=0: NO (residue -1)")
    print("underived physical residual:", ledger[
        "Cartan_square_and_physical_descent"
    ]["underived_physical_projection"]["first_residual"])
    print("shared Gate-I/III core: one regular rho orbit, odd/even projections")
    print("site-permutation shortcut: NO (mixed label + commutator defect)")
    print("physical q condition: quotient defect zero, or generator witness")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
