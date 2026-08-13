#!/usr/bin/env python3
"""Compose the centered base interface with the face-3/5 d_even route.

The clean denominator obstruction is the face augmentation epsilon on Q^5.
The proved centered restriction formulas live in two separate twelve-
occurrence lower modules.  Although each restricted vector has ordinary
coefficient sum 78, it has no proved denominator-face coordinate, so the
extended epsilon still kills it and the common H0 lines.

The proposed promoted centered base G_f would remove the obstruction only
because its *required*, still unconstructed cap face is the primitive

    p_(v,N)=(-Q_(v,N),-ores), epsilon(p)=-1.

Two translates p_3,p_5 cancel the candidate selected projection
y=(e3+e5)/2.  Matching-Bianchi then transports their tails from B0 to B4
and B1.  To obtain the pure labelled section d_even, rather than merely a
tail plus scalar residue, one still needs the invisible cap lift
n_(v,N)=(+Q_(v,N),0) and the physical occurrence-to-label map.  Conditional
on those maps,

    d_even = -1/2[(p_3+n_3)+(p_5+n_5)]

with the two occurrence residues labelled B4 and B1.  The coefficient K4
iota has exactly these labels but is not a physical source map.
"""

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_trace_cartan_even_repair_denominator_tor_gate.py":
        "673b30ac4b68c8a3af42e9c0803b3d5a39796b366b3ac15b5fd8b31b02d8df5d",
    "computations/verify_h3_centered_endpoint_projector_primitive_cap_lift_gate.py":
        "d5c90e6404670c7b666b6aa2b3448f5f16c2aebc7fac47f749fb269250413a28",
    "computations/verify_h3_centered_projector_e14_word_arrow_gate.py":
        "e1b8b17c75292f55439652ac9e5dcb1a24a3e4079c2d378e9fa63544e5491b46",
    "computations/verify_uniform_centered_occurrence_restriction_insertion_gate.py":
        "cb328adc1f23b38f6f9f9305635ddbaef888178633f8db91c205fdfbdca1ff34",
    "computations/verify_h2_lower_delta_plus_iota_target_rank_gate.py":
        "01e36f89b4df4bb020607d2f00871deb96775a7e58b42e85eaef76c20097e5cf",
    "computations/verify_h3_degree4_reset_five_face_aggregate_gate.py":
        "01961c9ae83b91dad31ba859ea2f8a2d5775d73d7ad591aa0a369e7d971f8079",
    "computations/verify_h3_cplus_root_even_koszul_physical_dressing_gate.py":
        "9bd2c9f482dc3277d07bd96a4e2189034e766f97e7800d3864179a75e03cef17",
    "computations/verify_h3_cplus_root_even_labelled_ores_sigma_cartan_gate.py":
        "144d1fd64d8a733f3ec737edd301c540e66d545c9d72adf1abba5f7ed4764ce1",
    "computations/verify_h2_p2_0112_one_endpoint_hasse_placement_gate.py":
        "8ec18f05034b6483512644c49d0009b4b166b0d6b978f6895195321ca9d8417a",
}


def require(condition, detail):
    if not condition:
        raise AssertionError(detail)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def load(relative, name):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def add(*vectors):
    return tuple(sum(entries, Q(0)) for entries in zip(*vectors, strict=True))


def scale(scalar, vector):
    return tuple(Q(scalar) * Q(entry) for entry in vector)


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


def unit(index, width):
    return tuple(Q(int(position == index)) for position in range(width))


def rank(columns):
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    work = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, height)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(height):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def pin_inputs():
    for relative, expected in PINS.items():
        actual = digest(ROOT / relative)
        require(actual == expected, (relative, actual, expected))


def clean_face_and_centered_restriction_audit():
    # Face order 1,...,5.  Existing physical route/Cartan differences span
    # the saturated augmentation-zero lattice.
    face_edges = []
    for index in range(5):
        face_edges.append(add(unit((index + 1) % 5, 5),
                              scale(-1, unit(index, 5))))
    epsilon = (Q(1),) * 5
    y = scale(Q(1, 2), add(unit(2, 5), unit(4, 5)))  # (e3+e5)/2
    require(rank(face_edges) == 4
            and all(dot(epsilon, column) == 0 for column in face_edges)
            and dot(epsilon, y) == 1
            and rank(face_edges + [y]) == 5,
            "the clean face-augmentation obstruction changed")

    # The two marked lower restrictions have 12 occurrence coordinates.
    # R=(15/2)c+(13/2)H0.  Its internal coefficient sum is 78, but this is
    # not epsilon: the two functionals live on different direct summands.
    one12 = (Q(1),) * 12
    c = add(scale(12, unit(0, 12)), scale(-1, one12))
    restricted = add(scale(Q(15, 2), c), scale(Q(13, 2), one12))
    require(sum(c, Q(0)) == 0 and sum(restricted, Q(0)) == 78,
            "the centered restriction augmentation changed")

    zero5, zero12 = (Q(0),) * 5, (Q(0),) * 12
    embed_face = lambda value: value + zero12 + zero12
    embed_23 = lambda value: zero5 + value + zero12
    embed_45 = lambda value: zero5 + zero12 + value
    extended_epsilon = epsilon + zero12 + zero12
    lower_columns = [embed_23(restricted), embed_45(restricted),
                     embed_23(one12), embed_45(one12)]
    require(all(dot(extended_epsilon, column) == 0
                for column in lower_columns)
            and dot(extended_epsilon, embed_face(y)) == 1,
            "a lower H0 coefficient became denominator face augmentation")

    p3 = scale(-1, unit(2, 5))
    p5 = scale(-1, unit(4, 5))
    p_even = scale(Q(1, 2), add(p3, p5))
    require(p_even == scale(-1, y)
            and dot(epsilon, p3) == dot(epsilon, p5) == -1
            and add(y, p_even) == zero5,
            "the primitive cap failed to cancel the selected projection")
    require(rank(face_edges + [p3]) == 5,
            "one primitive cap stopped completing the clean face quotient")
    return {
        "clean_standard_face_image": "ker(epsilon:Q^5->Q)",
        "candidate_selected_projection": "y=(e3+e5)/2",
        "epsilon_y": "1",
        "marked_restriction_each": "(15/2)c_lower+(13/2)H0",
        "internal_occurrence_sum_each": "78",
        "extended_face_epsilon_on_both_restrictions_and_H0": "0",
        "reason": (
            "lower occurrence/H0 rows and denominator face rows are distinct "
            "physical coordinates; numerical coefficient sums cannot be identified"
        ),
        "required_primitive_caps": ["p3=-e3", "p5=-e5"],
        "p_even": "-(e3+e5)/2=-y",
        "conditional_clean_obstruction_cancelled": True,
        "currently_constructed_by_centered_restriction_theorem": False,
    }


def conditional_deven_composition_audit():
    zero6 = (Q(0),) * 6
    b0, b1, b4 = unit(0, 6), unit(1, 6), unit(4, 6)
    v = scale(Q(1, 2), add(b1, b4))

    # Coordinates are tail_B0..B5, scalar ores, labelled ores_B0..B5.
    def vector(*, tail=zero6, scalar_ores=0, labelled_ores=zero6):
        return tail + (Q(scalar_ores),) + labelled_ores

    selected_a3 = vector(tail=scale(-1, b0), scalar_ores=-1)
    selected_a5 = vector(tail=scale(-1, b0), scalar_ores=-1)
    bianchi_4 = vector(tail=add(b4, scale(-1, b0)))
    bianchi_1 = vector(tail=add(b1, scale(-1, b0)))
    a4 = add(selected_a3, scale(-1, bianchi_4))
    a1 = add(selected_a5, scale(-1, bianchi_1))
    require(a4 == vector(tail=scale(-1, b4), scalar_ores=-1)
            and a1 == vector(tail=scale(-1, b1), scalar_ores=-1),
            "matching-Bianchi stopped landing the two fixed tails")
    negative_even_a = scale(Q(-1, 2), add(a4, a1))
    require(negative_even_a == vector(tail=v, scalar_ores=1),
            "the conditional even companion changed")

    # The invisible cap lifts cancel Q but not scalar residue.
    n4 = vector(tail=b4)
    n1 = vector(tail=b1)
    pure_scalar_4 = add(a4, n4)
    pure_scalar_1 = add(a1, n1)
    require(pure_scalar_4 == pure_scalar_1
            == vector(scalar_ores=-1),
            "the p+n pure scalar-residue identity changed")

    # Only after the occurrence-to-label comparison assigns B4/B1 does the
    # same formula become d_even.
    labelled_4 = vector(labelled_ores=scale(-1, b4))
    labelled_1 = vector(labelled_ores=scale(-1, b1))
    d_even = scale(Q(-1, 2), add(labelled_4, labelled_1))
    require(d_even == vector(labelled_ores=v),
            "the labelled d_even composition changed")

    # The coefficient iota knows these two labels, but has no source-chain
    # realization.  Before it is granted, the labelled sector is identically
    # zero on every constructed vector above and d_even raises rank.
    current = (selected_a3, selected_a5, bianchi_4, bianchi_1, n4, n1)
    require(all(column[-6:] == zero6 for column in current)
            and rank(current + (d_even,)) == rank(current) + 1,
            "the labelled residue entered the scalar/tail span")
    chi = tuple(map(Q, (0, 1, -1, 0, 1, -1)))
    labelled_chi = (Q(0),) * 7 + chi
    require(all(dot(labelled_chi, column) == 0 for column in current)
            and dot(labelled_chi, d_even) == 1,
            "the labelled fixed-plane separator changed")
    return {
        "conditional_selected_cells": [
            "A3=(-B0, scalar ores=-1)",
            "A5=(-B0, scalar ores=-1)",
        ],
        "matching_Bianchi_landings": [
            "A3-(B4-B0)=(-B4,-1)",
            "A5-(B1-B0)=(-B1,-1)",
        ],
        "negative_half_sum": "(tail=v, scalar ores=+1)",
        "is_d_even": False,
        "invisible_cap_identity": "p_i+n_i=(tail=0, scalar ores=-1)",
        "labelled_formula": (
            "d_even=-1/2[(p4+n4)_labelled+(p1+n1)_labelled]"
        ),
        "coefficient_labels": ["0112/q23 -> B1", "0121/q45 -> B4"],
        "physical_occurrence_to_label_map_constructed": False,
        "primitive_labelled_dual": [0, 1, -1, 0, 1, -1],
        "dual_on_d_even": "1",
    }


def dependency_scope_audit():
    centered = load(
        "computations/verify_h3_centered_projector_e14_word_arrow_gate.py",
        "deven_centered_base",
    )
    centered_ledger, centered_digest = centered.audit()
    require(centered_digest == centered.EXPECTED_LEDGER_SHA256,
            "the centered/E14 base ledger changed")
    extension = centered_ledger["minimal_extension"]
    require(extension["required_cap_face"]
            == "p=(-Q_(v,N),-ores), epsilon=+/-1"
            and extension["physical_construction"] is False,
            "the promoted base cap scope changed")

    denominator = load(
        "computations/verify_h3_trace_cartan_even_repair_denominator_tor_gate.py",
        "deven_denominator",
    )
    den_ledger, den_digest = denominator.audit()
    require(den_digest == denominator.EXPECTED_LEDGER_SHA256
            and den_ledger["selected_projection_obstruction"]
                ["denominator_kernel_exists_on_clean_C5"] is False,
            "the clean denominator obstruction changed")

    iota = load(
        "computations/verify_h2_lower_delta_plus_iota_target_rank_gate.py",
        "deven_iota",
    )
    iota_ledger, iota_digest = iota.audit()
    require(iota_digest == iota.EXPECTED_LEDGER_SHA256
            and iota_ledger["coefficient_iota"]
                ["physical_source_map_constructed"] is False,
            "the coefficient/physical iota distinction changed")

    p2 = load(
        "computations/verify_h2_p2_0112_one_endpoint_hasse_placement_gate.py",
        "deven_p2_private",
    )
    p2_ledger, p2_digest = p2.audit()
    require(p2_digest == p2.EXPECTED_LEDGER_SHA256
            and p2_ledger["one_endpoint_Hasse_faces"]
                ["rank_complete_rows"] == 8
            and p2_ledger["one_endpoint_Hasse_faces"]
                ["rank_after_faces"] == 16,
            "the P2 one-root private obstruction changed")
    return {
        "centered_base_status": (
            "its restriction coefficients are proved, but the physical cell "
            "is conditional and lists p as a required face"
        ),
        "circularity": (
            "using G_f to supply aggregate-one is valid only after proving "
            "the same primitive p which the clean denominator route lacks"
        ),
        "invisible_n_status": (
            "the degree-four reset constructs a derived filler; physical n "
            "still requires the augmented K_Eq comparison"
        ),
        "label_map_status": (
            "the lower K4 iota assigns B1/B4 coefficientwise but is not a "
            "physical word/fine/repeated-grade chain map"
        ),
        "first_P2_private_face": (
            "the literal 0112 representative has eight nonconstant one-root "
            "Hasse word vectors; rank rises 8 to 16 over complete response "
            "rows, and the target/Eq triangle has zero projection there"
        ),
    }


def audit():
    pin_inputs()
    return {
        "theorem": "centered-base / denominator d_even composition gate",
        "pins": PINS,
        "clean_face_vs_centered_restriction":
            clean_face_and_centered_restriction_audit(),
        "conditional_d_even_composition": conditional_deven_composition_audit(),
        "source_scope": dependency_scope_audit(),
        "sharp_remaining_object": (
            "one sigma-covariant pointed augmented comparison whose two "
            "object restrictions simultaneously supply primitive p_i, "
            "invisible n_i, and the physical B4/B1 labelled residue map; "
            "equivalently construct d_even directly"
        ),
        "smallest_current_duals": [
            "face epsilon detects the unconstructed primitive cap p",
            "wordwise labelled chi detects d_even after scalar/tail composition",
            "one-root occurrence-private lambda detects the first P2 placement face",
        ],
        "terminal_scope": (
            "epsilon and chi are exact projected cokernel covectors, not final "
            "physical terminals until extended across the complete augmented "
            "word/ridge/q/anchor/eta/sigma comparison"
        ),
    }


def main():
    result = audit()
    payload = json.dumps(result, sort_keys=True, separators=(",", ":"))
    ledger = sha256(payload.encode()).hexdigest()
    print("h3 centered base / denominator d_even composition gate: PASS")
    print("proved centered restrictions supply aggregate-one cap: NO")
    print("full promoted G_f would supply it only through required p face")
    print("conditional p+n+label map gives d_even exactly")
    print("ledger sha256:", ledger)


if __name__ == "__main__":
    main()
