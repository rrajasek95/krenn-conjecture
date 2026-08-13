#!/usr/bin/env python3
"""Freeze the exact full-interface type of the last tau_plus orbit.

The two missing tau_plus labels form one rho-orbit.  Its invariant source
line therefore needs only one new equivariant generator.  At the occurrence
level the divided product rule already has coefficient one and its two fixed
resolutions average to

    v = (B1+B4)/2.

This does not yet construct a physical cell.  In the actual omitted-25 grade
the local Bianchi bypass lands on the complementary even average, so the
same generator must carry the augmentation-zero transport

    delta_plus = (-B0+2B1-B2-B3+2B4-B5)/4.

The full interface also forces three other projections of that generator:
the normalized mixed Cartan target -2 D tensor v, the compensating reduced
Eq face +2 D tensor v, and labelled ordinary residue v.  Existing literal
families miss these projections for independent, primitive reasons.  Thus
one *full* nondegenerate relative product-rule/Bianchi orbit is the smallest
formal extension; a bare tail, coarse residue grant, or isolated formal
Hasse top is not it.

The formal third-cofactor totalization has the useful anchor signature but
fails physical descent, retains endpoint ridges, and hits no midpoint word.
Accordingly this checker states a sharp extension interface, not a direct
physical construction.  The beta=0 selected D0 quotient is a different root
summand and remains the independent unit-membership theta(Z) condition.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_trace_cartan_tau_plus_site_collapse_gate.py":
        "f0801bfcd5362f2fc8d9a81bf85a84b2d380fd37cbbe7db2252b352b785d5474",
    "computations/verify_h3_tau_plus_delta_literal_same_grade_gate.py":
        "f5d34986e086055dcba26e347c5a7f7470d9ec62a1346c9c872a8e828ec7b266",
    "computations/verify_h3_cut_swap_shared_loop_hasse_cross_term_gate.py":
        "cc551585391a990060f78b49486c05af6c3b4a301058c855a422ae9d54fe5be5",
    "computations/verify_h3_generic_cartan_adjacent_target_label_prolongation.py":
        "ef63bd26210802cf300e263da44e178b4dd19abbf0fa5bba059b5d61afb9b782",
    "computations/verify_h3_trace_cartan_even_repair_anchor_residue_fibre_gate.py":
        "3012b12ed19c1453e9d14a95beee3542d4385e70c53a553661a5d3cd1bcdb1a9",
    "computations/verify_h3_beta_zero_d0_unary_third_bianchi_membership_gate.py":
        "2b1bead205d5c766ffff6a0ab9a4d39a5d5ba8308bc0e96d70c1bc7974e00677",
}
EXPECTED_LEDGER_SHA256 = (
    "9488629927a079e70d1ac1cc629fca3453f172880b174e5b16e76cee2322bfbe"
)

RHO_B = (5, 1, 3, 2, 4, 0)


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


def add(*vectors):
    return tuple(sum(Q(vector[index]) for vector in vectors)
                 for index in range(len(vectors[0])))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in
                zip(left, right, strict=True)), Q(0))


def tensor(left, right):
    return tuple(Q(a) * Q(b) for a in left for b in right)


def rank(columns):
    if not columns:
        return 0
    height = len(columns[0])
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


def audit_frozen_inputs():
    trace = load(
        "computations/verify_h3_trace_cartan_tau_plus_site_collapse_gate.py",
        "tau_full_trace",
    )
    delta = load(
        "computations/verify_h3_tau_plus_delta_literal_same_grade_gate.py",
        "tau_full_delta",
    )
    cross = load(
        "computations/verify_h3_cut_swap_shared_loop_hasse_cross_term_gate.py",
        "tau_full_cross",
    )
    generic = load(
        "computations/verify_h3_generic_cartan_adjacent_target_label_prolongation.py",
        "tau_full_generic",
    )
    beta = load(
        "computations/verify_h3_beta_zero_d0_unary_third_bianchi_membership_gate.py",
        "tau_full_beta",
    )

    trace_ledger, trace_digest = trace.audit()
    delta_ledger, delta_digest = delta.audit()
    cross_ledger, cross_digest = cross.audit()
    generic_ledger, generic_digest = generic.audit()
    beta_ledger, beta_digest = beta.audit()
    require(trace_digest == trace.EXPECTED_LEDGER_SHA256
            and delta_digest == delta.EXPECTED_LEDGER_SHA256
            and cross_digest == cross.EXPECTED_LEDGER_SHA256
            and generic_digest == generic.EXPECTED_LEDGER_SHA256
            and beta_digest == beta.EXPECTED_LEDGER_SHA256,
            "a frozen interface theorem changed")

    require(trace_ledger["smallest_relative_repair"]
                ["per_omitted_label_image"] == "(B1+B4)/2"
            and trace_ledger["canonical_13_label_landing"]
                ["partial_target"] == [3, 2, 3, 3, 2, 3],
            "the tau_plus missing orbit changed")
    require(delta_ledger["literal_complete_column_gate"]
                ["bounded_literal_dual"]["on_integral_common_tail_bridge"]
            == 12,
            "the complete-column transport dual changed")
    occurrence = cross_ledger["literal_C4_resolution"]
    formal = cross_ledger["formal_totalization"]
    require(occurrence["Hasse_normalized_fixed"]["rho_even_average"]
            == "(B1+B4)/2"
            and occurrence["occurrence_augmentation"] == 1
            and formal["tail_signature_ainc_W_target_ores"]
                == [-1, 0, 0, 0]
            and formal["endpoint_ridge_mismatch_rank"] == 6
            and formal["primitive_Omega_rank"] == 5
            and formal["physical_midpoint_word_hits"] == 0
            and formal["source_valid"] is False,
            "the product-rule occurrence/physical gate changed")
    correction = generic_ledger["formal_filler_and_Rees_guard"] \
        ["known_formal_filler"]["missing_relative_correction"]
    require(correction == "+2D*(H0-u)*Eq",
            "the generic reduced-Eq correction changed")
    require(beta_ledger["exact_membership_or_dual"]["target_map"]
            == "theta:Z -> Q0=S*[D0]",
            "the beta-zero protected quotient changed")
    return {
        "trace": trace_digest,
        "delta": delta_digest,
        "cross": cross_digest,
        "generic": generic_digest,
        "beta_zero": beta_digest,
    }


def audit_even_source_line():
    # The missing labels ell,rho(ell) span a permutation module.  Its even
    # and odd eigenvectors have eigenvalues +1 and -1.  Only the even line
    # occurs in tau_plus, so a single equivariant orbit generator is minimal.
    e_left = (Q(1), Q(0))
    e_right = (Q(0), Q(1))
    e_plus = scale(Q(1, 2), add(e_left, e_right))
    e_minus = scale(Q(1, 2), add(e_left, scale(-1, e_right)))
    rho = lambda pair: (pair[1], pair[0])
    require(rho(e_plus) == e_plus
            and rho(e_minus) == scale(-1, e_minus)
            and rank((e_plus, e_minus)) == 2
            and rank((e_plus,)) == 1,
            "the omitted rho-pair splitting changed")
    return {
        "omitted_source_module": "Q{ell,rho ell}",
        "rho_even_generator": [str(value) for value in e_plus],
        "rho_odd_generator": [str(value) for value in e_minus],
        "tau_plus_consumes": "the one-dimensional rho-even line",
        "minimum_equivariant_generator_orbits": 1,
    }


def audit_full_interface_type():
    v = (Q(0), Q(1, 2), Q(0), Q(0), Q(1, 2), Q(0))
    local = (Q(1, 4), Q(0), Q(1, 4),
             Q(1, 4), Q(0), Q(1, 4))
    delta = add(v, scale(-1, local))
    integral_delta = scale(4, delta)
    expected_integral = (Q(-1), Q(2), Q(-1),
                         Q(-1), Q(2), Q(-1))
    require(delta == scale(Q(1, 4), expected_integral)
            and sum(v) == sum(local) == 1
            and sum(delta) == 0
            and tuple(v[index] for index in RHO_B) == v
            and tuple(local[index] for index in RHO_B) == local
            and tuple(delta[index] for index in RHO_B) == delta,
            "the even landing/transport debt changed")

    # D is the four-corner root defect.  The normalized generic Cartan
    # target is -2D; its missing reduced-Eq face has the opposite +2D
    # coefficient.  Both are coefficientwise decorated by the same v.
    root_defect = (Q(-1), Q(1), Q(-1), Q(1))
    mixed_target = scale(-2, tensor(root_defect, v))
    reduced_eq = scale(2, tensor(root_defect, v))
    require(add(mixed_target, reduced_eq) == (Q(0),) * 24
            and sum(mixed_target) == sum(reduced_eq) == 0
            and sum(value != 0 for value in mixed_target) == 8,
            "the root-decorated target/Eq packet changed")

    # A full candidate is one vector in the direct sum of its forced
    # projections.  This proves one formal generator is enough to *state*
    # the extension.  It says nothing about physical descent/d^2.
    full_candidate = (
        v + delta + mixed_target + reduced_eq + v + (Q(-1),)
    )
    require(rank((full_candidate,)) == 1,
            "the prescribed full-interface generator vanished")
    return {
        "direct_landing_B0_to_B5": [str(value) for value in v],
        "actual_grade_local_Bianchi_average": [str(value) for value in local],
        "same_grade_transport_delta_plus": [str(value) for value in delta],
        "integral_delta_plus": [int(value) for value in integral_delta],
        "root_defect_D": [int(value) for value in root_defect],
        "normalized_mixed_target": "-2 D tensor v",
        "reduced_Eq_face": "+2 D (H0-u)Eq tensor v",
        "labelled_ordinary_residue": "v",
        "formal_anchor_incidence": -1,
        "full_candidate_coordinate_count": len(full_candidate),
        "formal_generator_rank": 1,
    }


def audit_primitive_projection_guards():
    v = (Q(0), Q(1, 2), Q(0), Q(0), Q(1, 2), Q(0))
    d = (Q(-1), Q(2), Q(-1), Q(-1), Q(2), Q(-1))

    # Complete full-nine columns and the projected M_v family tie each
    # private pivot to the same labelled Eq coefficient.  The relative
    # transport wants (D,0).  The primitive dual (D,-D) detects it.
    tied = []
    for index in range(6):
        unit = tuple(Q(int(position == index)) for position in range(6))
        tied.append(unit + unit)
    common_tail = d + (Q(0),) * 6
    private_eq_dual = d + scale(-1, d)
    require(all(dot(private_eq_dual, column) == 0 for column in tied)
            and dot(private_eq_dual, common_tail) == 12
            and rank(tied) == 6 and rank(tied + [common_tail]) == 7,
            "the private/Eq transport obstruction changed")

    # The committed scalar residue lift and the one pinned Cartan residue
    # line miss v.  This is a projection guard, not a claim about an as-yet
    # undefined termwise residue on every complete source column.
    diagonal = (Q(1),) * 6
    cartan_residue = (Q(1), Q(0), Q(1), Q(-1), Q(0), Q(-1))
    residue_dual = (Q(0), Q(1), Q(-1), Q(0), Q(1), Q(-1))
    require(dot(residue_dual, diagonal) == 0
            and dot(residue_dual, cartan_residue) == 0
            and dot(residue_dual, v) == 1
            and rank((diagonal, cartan_residue, v)) == 3,
            "the labelled-residue projection guard changed")

    # In the reduced (Eq,w) plane the old fourth-Hasse face is (1,1),
    # whereas the wanted correction is (1,0).  (1,-1) is primitive.
    old_filler = (Q(1), Q(1))
    eq_correction = (Q(1), Q(0))
    eq_dual = (Q(1), Q(-1))
    require(dot(eq_dual, old_filler) == 0
            and dot(eq_dual, eq_correction) == 1
            and rank((old_filler, eq_correction)) == 2,
            "the reduced-Eq conormal changed")

    # A diagonal cap coordinate has no mixed-word entry.  A nonzero root
    # defect does.  This is why target equality is conditional on iota.
    diagonal_cap = (Q(1), Q(0), Q(-1), Q(0))
    mixed_root = (Q(-1), Q(1), Q(-1), Q(1))
    mixed_coordinate_dual = (Q(0), Q(1), Q(0), Q(0))
    require(dot(mixed_coordinate_dual, diagonal_cap) == 0
            and dot(mixed_coordinate_dual, mixed_root) == 1,
            "the pure-to-mixed word guard changed")
    return {
        "full_nine_transport": {
            "dual": "sum_i D_i(private_i-Eq_i)",
            "value_on_integral_delta_plus": 12,
        },
        "labelled_residue": {
            "dual": [int(value) for value in residue_dual],
            "kills_committed_diagonal_and_pinned_Cartan_lines": True,
            "value_on_v": 1,
            "scope": "projected guard; no bare/coarse residue construction",
        },
        "reduced_Eq": {
            "dual_in_Eq_w_plane": [1, -1],
            "value_on_required_correction": 1,
        },
        "mixed_word": {
            "diagonal_cap_has_mixed_coordinate": False,
            "root_defect_has_mixed_coordinate": True,
        },
        "consequence": (
            "a tail-only, residue-only, Eq-only, or target-only attachment "
            "cannot be promoted to the full interface by the frozen old span"
        ),
    }


def audit_beta_zero_guard():
    # On beta=0 the cap rows span only D2.  The selected D0 quotient is the
    # complementary coordinate, detected by the primitive covector below.
    d0 = (Q(1), Q(0))
    d2 = (Q(0), Q(1))
    d0_dual = (Q(1), Q(0))
    require(dot(d0_dual, d2) == 0
            and dot(d0_dual, d0) == 1
            and rank((d2, d0)) == 2,
            "the beta-zero D0/D2 split changed")

    # J*=-3 alpha beta I.  Any unnormalized polynomial construction from
    # J* vanishes at beta=0; the generic target uses beta^{-1} and therefore
    # has no regular specialization supplying D0.
    samples = []
    alpha = Q(2)
    for beta in (Q(-3), Q(-1), Q(0), Q(2), Q(5)):
        jstar = -3 * alpha * beta
        samples.append((beta, jstar))
    require(next(value for beta, value in samples if beta == 0) == 0
            and all(value != 0 for beta, value in samples if beta != 0),
            "the generic Cartan input stopped vanishing exactly at beta=0")
    return {
        "generic_input": "J*=-3 alpha beta I",
        "normalized_generic_cell_requires": "(alpha beta)^(-1)",
        "regular_beta_zero_specialization": 0,
        "selected_quotient": "Q[D0] modulo the known D2 line",
        "primitive_D0_dual": [1, 0],
        "independent_remaining_condition": "1 in theta(Z)",
        "generic_even_cell_closes_beta_zero": False,
    }


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))
    ledger = {
        "theorem": "tau_plus full-interface product-rule/Bianchi extension gate",
        "pins": PINS,
        "frozen_input_ledgers": audit_frozen_inputs(),
        "rho_even_source_line": audit_even_source_line(),
        "forced_full_interface_type": audit_full_interface_type(),
        "primitive_projection_guards": audit_primitive_projection_guards(),
        "physical_descent_gate": {
            "formal_product_rule_fixed_average": "(B1+B4)/2",
            "formal_tail_signature_ainc_W_target_ores": [-1, 0, 0, 0],
            "source_valid": False,
            "endpoint_ridge_space_rank": 6,
            "Omega_obstruction_rank": 5,
            "selected_midpoint_word_hits": 0,
            "smallest_physical_extension": (
                "one rho-even nondegenerate relative product-rule/Bianchi "
                "orbit in the actual omitted-25 repeated grade, together "
                "with its forced endpoint-ridge and word-changing faces; "
                "its full boundary must realize delta_plus, -2D tensor v, "
                "+2D(H0-u)Eq tensor v, and labelled ores v"
            ),
        },
        "beta_zero_guard": audit_beta_zero_guard(),
        "verdict": (
            "the occurrence coefficient and target average are exact, and "
            "the generic missing domain is only one rho-even source line. "
            "A single fully typed relative orbit is therefore the minimal "
            "formal extension.  It is not present in the old physical "
            "inventory: its complete-column, mixed-word, reduced-Eq, and "
            "labelled-residue projections are all load-bearing, while the "
            "formal Hasse carrier fails descent/ridge/word typing.  Beta=0 "
            "is an independent D0 unit-membership or dual branch"
        ),
        "constructed_physical_cell": False,
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("tau_plus full-interface ledger changed", digest))
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("h3 tau_plus full-interface product/Bianchi: FORMAL ONE-ORBIT GATE")
    print("occurrence landing: (B1+B4)/2 with coefficient one")
    print("required: full-nine delta+, mixed target, reduced Eq, labelled ores")
    print("physical descent: endpoint-ridge/word faces still missing")
    print("beta=0: independent D0 membership or dual")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
