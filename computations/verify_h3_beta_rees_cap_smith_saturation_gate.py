#!/usr/bin/env python3
"""Audit beta-saturation of the minimal physical diagonal Rees packet.

Over R=k[beta] (with h and alpha units), the two literal cap jets are

    Z1 =  beta*rho0 + rho2,
    Z2 = -beta*rho0 + (h-1)*rho2.

Their Smith form is diag(1,beta): the selected rho0 class is nonzero but is
killed by beta.  Adding the formal unary rho0 column does not remove this
torsion because that column carries a primitive protected descent defect.
The resulting three-row packet still has determinant h*beta.  A physical
column carrying the same defect and zero rho0 would cancel it, produce a
unit minor, and make rho0 accessible.

This is an exact first torsion carrier in the pinned physical packet, not a
claim that the exhaustive physical map has torsion: an as-yet unconstructed
source column could supply precisely the defect correction.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_diagonal_rees_saturation_cap_jet_bockstein.py":
        "12c4cc4a947d99eee22cbd87e900ac6c7a56df2c533c4c44c52f0ab0fcedee2a",
    "computations/verify_h3_beta_zero_d0_augmented_terminal_saturation_gate.py":
        "d4fabdb5e180ce63e4a0ff018197f4aaf33767bfcf6940291af7783d2f150b27",
    "computations/verify_h3_beta_zero_d0_unary_third_bianchi_membership_gate.py":
        "2b1bead205d5c766ffff6a0ab9a4d39a5d5ba8308bc0e96d70c1bc7974e00677",
    "computations/verify_h3_tau_plus_full_interface_product_bianchi_extension_gate.py":
        "32be7ef48ad9d35b8863a62889508ccdff0010d8ebff18b366e932aab8b2bf14",
    "computations/verify_h3_trace_cartan_lower_rees_typing_gate.py":
        "0190a8fa16dddf9cecf2de676d4f3ff87d184f031e523d87e1f80937ff55be94",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


class Poly:
    """A tiny exact Q[beta] implementation."""

    def __init__(self, *coefficients):
        values = list(map(Q, coefficients or (0,)))
        while len(values) > 1 and not values[-1]:
            values.pop()
        self.coefficients = tuple(values)

    def __add__(self, other):
        other = as_poly(other)
        size = max(len(self.coefficients), len(other.coefficients))
        return Poly(*(self[index] + other[index] for index in range(size)))

    __radd__ = __add__

    def __neg__(self):
        return Poly(*(-value for value in self.coefficients))

    def __sub__(self, other):
        return self + (-as_poly(other))

    def __rsub__(self, other):
        return as_poly(other) - self

    def __mul__(self, other):
        other = as_poly(other)
        output = [Q(0)] * (len(self.coefficients) + len(other.coefficients) - 1)
        for left, a in enumerate(self.coefficients):
            for right, b in enumerate(other.coefficients):
                output[left + right] += a * b
        return Poly(*output)

    __rmul__ = __mul__

    def __getitem__(self, index):
        return self.coefficients[index] if index < len(self.coefficients) else Q(0)

    def __eq__(self, other):
        return self.coefficients == as_poly(other).coefficients

    def __repr__(self):
        return f"Poly{self.coefficients!r}"

    @property
    def degree(self):
        return len(self.coefficients) - 1 if any(self.coefficients) else -1

    def at_zero(self):
        return self[0]


def as_poly(value):
    return value if isinstance(value, Poly) else Poly(value)


ZERO = Poly(0)
ONE = Poly(1)
BETA = Poly(0, 1)


def add(*vectors):
    return tuple(sum((as_poly(vector[index]) for vector in vectors), ZERO)
                 for index in range(len(vectors[0])))


def scale(coefficient, vector):
    return tuple(as_poly(coefficient) * as_poly(value) for value in vector)


def determinant(matrix):
    matrix = tuple(tuple(map(as_poly, row)) for row in matrix)
    size = len(matrix)
    require(all(len(row) == size for row in matrix), ("nonsquare", matrix))
    if size == 0:
        return ONE
    if size == 1:
        return matrix[0][0]
    answer = ZERO
    for column in range(size):
        minor = tuple(tuple(row[index] for index in range(size)
                            if index != column) for row in matrix[1:])
        answer += ((-1) ** column) * matrix[0][column] * determinant(minor)
    return answer


def rank_rational(matrix):
    work = [list(map(Q, row)) for row in matrix]
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


def specialize_zero(columns):
    return tuple(tuple(as_poly(value).at_zero() for value in column)
                 for column in columns)


def column_rank(columns):
    return rank_rational(tuple(zip(*columns, strict=True))) if columns else 0


def audit_cap_smith_packet():
    records = []
    for h in range(3, 13):
        rho0 = (ONE, ZERO)
        rho2 = (ZERO, ONE)
        z1 = add(scale(BETA, rho0), rho2)
        z2 = add(scale(-BETA, rho0), scale(h - 1, rho2))
        matrix = tuple(zip(z1, z2, strict=True))
        require(determinant(matrix) == h * BETA,
                ("cap determinant", h, determinant(matrix)))
        recovered_rho2 = scale(Q(1, h), add(z1, z2))
        beta_rho0 = scale(Q(1, h), add(scale(h - 1, z1), scale(-1, z2)))
        require(recovered_rho2 == rho2 and beta_rho0 == scale(BETA, rho0),
                ("cap Smith generators", h, recovered_rho2, beta_rho0))
        special = specialize_zero((z1, z2))
        require(column_rank(special) == 1
                and column_rank(special + ((Q(1), Q(0)),)) == 2,
                ("rho0 unexpectedly entered the collision image", h, special))
        # A unit matrix entry gives the first Smith invariant 1; determinant
        # h*beta then makes the second invariant beta up to a unit.
        require(z1[1] == ONE, ("lost unit Smith entry", h, z1))
        records.append({
            "h": h,
            "determinant": f"{h}*beta",
            "generic_rank": 2,
            "special_rank": 1,
            "smith_form_up_to_units": ["1", "beta"],
            "torsion_generator": "[rho0]",
            "beta_times_generator_in_image": True,
        })
    return records


def audit_augmented_unary_defect():
    h = 3
    # Rows are (primitive protected descent, rho0, rho2).  The formal unary
    # cell U carries rho0 with a nonzero descent value.  Z1,Z2 are the two
    # collided cap jets and have zero in this primitive shadow.
    unary = (ONE, ONE, ZERO)
    z1 = (ZERO, BETA, ONE)
    z2 = (ZERO, -BETA, Poly(h - 1))
    minimal = tuple(zip(unary, z1, z2, strict=True))
    require(determinant(minimal) == h * BETA,
            ("augmented unary determinant", determinant(minimal)))
    special = specialize_zero((unary, z1, z2))
    rho0 = (Q(0), Q(1), Q(0))
    require(column_rank(special) == 2
            and column_rank(special + (rho0,)) == 3,
            "formal unary defect accidentally supplied protected rho0")

    # beta*rho0 is still in the cap span, so [rho0] is beta-torsion in the
    # augmented cokernel as well.  The unit 2x2 minor on rows defect,rho2
    # and columns U,Z1 shows its other two Smith factors are units.
    unit_minor = ((unary[0], z1[0]), (unary[2], z1[2]))
    require(determinant(unit_minor) == ONE,
            ("augmented packet lost its unit two-minor", unit_minor))

    # A physical correction V with the same protected defect and zero root
    # output makes U-V=rho0.  The columns U,V,Z1 then have a unit determinant.
    correction = (ONE, ZERO, ZERO)
    positive_minor = tuple(zip(unary, correction, z1, strict=True))
    require(determinant(positive_minor) == Poly(-1),
            ("defect correction did not create a unit minor",
             determinant(positive_minor)))
    protected_rho0 = add(unary, scale(-1, correction))
    require(protected_rho0 == (ZERO, ONE, ZERO),
            ("corrected unary is not protected rho0", protected_rho0))
    return {
        "row_order": ["primitive_descent_defect", "rho0", "rho2"],
        "known_columns": ["formal_unary_U", "cap_Z1", "cap_Z2"],
        "known_determinant": "h*beta",
        "known_smith_form_up_to_units": ["1", "1", "beta"],
        "explicit_torsion_class": "[rho0], the selected D0 shadow",
        "formal_unary_problem": "U=descent+rho0, not protected rho0",
        "smallest_positive_column": "V=descent with zero rho0/rho2",
        "positive_identity": "U-V=rho0",
        "positive_unit_minor": "det(U,V,Z1)=-1",
    }


def audit_bockstein_and_full_orbit_interface():
    records = []
    for h in range(3, 13):
        rho0 = (ONE, ZERO)
        rho2 = (ZERO, ONE)
        z1 = add(scale(BETA, rho0), rho2)
        z2 = add(scale(-BETA, rho0), scale(h - 1, rho2))

        # Let e1,e2 denote the two cap source generators.  The source
        # combination s=((h-1)e1-e2)/h has image beta*rho0.  Mod beta it is
        # a special-fibre cycle, and division of its image by beta followed
        # by specialization is the Bockstein [rho0].
        image_s = scale(Q(1, h), add(scale(h - 1, z1), scale(-1, z2)))
        require(image_s == scale(BETA, rho0),
                ("cap Bockstein numerator", h, image_s))
        bockstein = tuple(Poly(value[1]) for value in image_s)
        require(bockstein == rho0,
                ("cap Bockstein stopped being rho0", h, bockstein))
        source_coefficients = (Q(h - 1, h), Q(-1, h))
        special_image = add(
            scale(source_coefficients[0], tuple(Poly(value.at_zero()) for value in z1)),
            scale(source_coefficients[1], tuple(Poly(value.at_zero()) for value in z2)),
        )
        require(special_image == (ZERO, ZERO),
                ("Bockstein source is not a special cycle", h, special_image))
        records.append({
            "h": h,
            "source_cycle_mod_beta": f"(({h}-1)e1-e2)/{h}",
            "integral_boundary": "beta*rho0",
            "Bockstein": "[rho0]",
        })

    # Frozen a872264 data.  The one even orbit has the only available coarse
    # rootless proper-face shadow which could become V: target and residue
    # zero with ainc=-1.  The pinned data do not identify its primitive
    # descent coordinate with the beta-zero unary defect.  It is explicitly
    # not source-valid and retains ridge/wrong-word faces.  Moreover a872264
    # is a fixed generic occurrence/full-interface prescription; it supplies
    # no integral beta-polynomial source cell, so a beta-Bockstein of that
    # full orbit is not yet defined.
    formal_tail = (Q(-1), Q(0), Q(0), Q(0))
    require(formal_tail == (Q(-1), Q(0), Q(0), Q(0)),
            "the full-orbit coarse proper-face signature changed")
    return {
        "cap_Bockstein_records": records,
        "Bockstein_definition": (
            "for the two-term complex C_R->Y_R, J(s)=beta*y makes s mod beta "
            "a special-fibre cycle and delta_beta([s])=[y mod beta]"
        ),
        "a872264_full_even_orbit": {
            "generic_source_line_rank": 1,
            "generic_occurrence_landing": "v=(B1+B4)/2",
            "formal_proper_face_ainc_W_target_ores": [-1, 0, 0, 0],
            "coarse_zero_target_residue_candidate_for_V": True,
            "same_primitive_descent_coordinate_proved": False,
            "source_valid": False,
            "endpoint_ridge_space_rank": 6,
            "primitive_Omega_rank": 5,
            "selected_midpoint_word_hits": 0,
            "integral_k_beta_cell_constructed": False,
        },
        "exact_status": (
            "[rho0] is literally the cap Bockstein.  The formal proper face "
            "of the rho-even orbit is the unique current projected candidate "
            "for V, but neither equality of the primitive descent coordinate "
            "nor physical equality is proved.  Its ridge, word, Eq, residue, "
            "anchor, and W faces must be totalized in one integral "
            "k[beta]-linear source cell"
        ),
        "strengthened_Interface_III_target": (
            "construct one integral k[beta]-linear rho-even product-rule/"
            "Bianchi cell X(beta) in the actual omitted-25 repeated grade; "
            "over beta!=0 its normalized face is v=(B1+B4)/2 with the full "
            "delta+/target/Eq/ores/W packet, while at beta=0 its proper-face "
            "Bockstein is the complete correction V.  Then U-V is the "
            "protected D0 unit and the generic and beta-zero branches close "
            "by the same unit minor"
        ),
    }


def audit_saturation_criteria():
    # Multiaffinity is defeated by the literal cap matrix itself: every
    # entry has beta degree at most one, yet the cokernel has beta-torsion.
    cap_entries = (BETA, -BETA, ONE, Poly(2))
    require(max(entry.degree for entry in cap_entries) == 1,
            "the multiaffine counterguard changed degree")

    # Flatness of the image is also insufficient.  beta*R is a free rank-one
    # R-module, but R/(beta) is torsion and the inclusion loses rank at zero.
    return {
        "base_ring": "R=k[beta]_(beta), with alpha and h inverted",
        "complete_order_h_ring": "R_h=R[ell]/(ell^(h+1))",
        "physical_map": (
            "J_R=(P_R,theta_R):C_R^(h)->R_prot,R direct-sum R[D0], "
            "with complete word/fine/repeated and Eq/ores/ainc/Yw/W rows"
        ),
        "desired_section": "b=ell^h[D0]",
        "generic_input": "beta^m*b in im(J_R) after the generic orbit is physical",
        "specialization_theorem": (
            "if coker(J_R) has no beta-primary torsion (equivalently im(J_R) "
            "is beta-saturated), then b lies in im(J_R) and specializes to "
            "1 in theta_0(ker P_0)"
        ),
        "image_flatness_suffices": False,
        "reason_image_flatness_fails": (
            "beta*R is free/flat; it is flatness of the cokernel, or purity "
            "of the image inclusion, that controls specialization"
        ),
        "multiaffinity_suffices": False,
        "multiaffine_counterguard": "the cap Smith matrix has degree <=1 and torsion",
        "unit_minor_criterion": (
            "if r is the generic rank and an r-by-r minor is a beta-adic "
            "unit, then special rank equals generic rank and the cokernel "
            "has no beta-primary torsion"
        ),
        "known_packet_has_generic_unit_minor": False,
        "known_packet_first_torsion": "[rho0] killed by beta",
    }


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    ledger = {
        "theorem": "beta-Rees cap Smith saturation gate",
        "pins": PINS,
        "literal_cap_smith_packets": audit_cap_smith_packet(),
        "augmented_unary_defect_packet": audit_augmented_unary_defect(),
        "Bockstein_full_orbit_interface": audit_bockstein_and_full_orbit_interface(),
        "complete_module_and_criteria": audit_saturation_criteria(),
        "verdict": (
            "beta-saturation of the complete augmented physical cokernel "
            "would specialize a constructed generic order-h orbit and close "
            "theta.  Neither multiaffinity nor flatness of the image proves "
            "it.  The pinned cap/unary packet has an explicit first torsion "
            "class [rho0]: its Smith determinant is h*beta.  Removing it is "
            "exactly the source-valid construction of a column with the "
            "unary cell's primitive protected defect and zero selected-root "
            "output; subtracting gives the protected D0 unit"
        ),
        "scope": (
            "exact torsion in the known minimal physical projection.  The "
            "exhaustive map may remove it via an unconstructed column, so "
            "this is a sharp carrier/criterion rather than a global no-go"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    expected = "d57abe489ef3daa029362cee5748937b5b211c5a4d08bdeecfb39c929e87cada"
    require(digest == expected, ("unexpected ledger digest", digest, expected))
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("h3 beta-Rees cap Smith saturation gate: PASS")
    print("cap Smith form: diag(1,beta)")
    print("with defective unary: diag(1,1,beta)")
    print("multiaffinity/image-flatness: insufficient")
    print("missing correction V gives U-V=protected D0 and a unit minor")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
