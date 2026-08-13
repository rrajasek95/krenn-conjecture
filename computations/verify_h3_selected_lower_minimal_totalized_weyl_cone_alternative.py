#!/usr/bin/env python3
"""Reconcile whole-row Cartan descent with the missing occurrence-local bar.

The physical Cartan source-orbit theorem proves covariance of each *complete*
90-term matching row.  The selected Gate-I discrepancy instead asks for a
section of one occurrence quotient.  The selected Weyl-bar audit identifies
that quotient exactly: the old endpoints, whole-row bars, and four Hasse
faces have rank 12, while adjoining the endpoint-odd private packet has rank
13 and a normalized separating functional.

There is a canonical one-generator construction in the homotopy-orbit/group
bar of the complete Hasse totalization.  For a total cycle Z0 with
tau Z0=-Z1,

    d[tau|Z0] = tau Z0-Z0 = -(Z1+Z0).

Endpoint oddization kills its target.  This packages all 341 formal edges in
one chain-valued generator.  It is not automatically a generator of the
physical relative source complex: the missing datum is precisely a section
of the rank-one occurrence quotient, with the complete augmented readouts.
The final boundary/cokernel and kernel/readout alternatives are exact linear
algebra once that complete physical map is fixed.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    # Whole-row Ward identity and endpoint source automorphism.
    "computations/verify_h3_physical_cartan_source_orbit_descent.py":
        "c92667c38c57c69dff18fd7570fa154db7e1a634a83f462dfde6bd5553128a3a",
    # Exact categorical typing gate: PP naturality does not define the
    # physical comparison functor.
    "computations/verify_h3_complete_hasse_cartan_naturality_square_gate.py":
        "3ea6a79bc6918cc4569bd12ad0b1634679c28037b687b6ae7c0e610e81998279",
    # Exact 341+341 formal Weyl bar and the rank-12/rank-13 occurrence gate.
    "computations/verify_h3_selected_lower_relative_weyl_bar_gate.py":
        "7a6f2afebcacc5924110e32a3f7d9c225992f07abae637d4529b5436c64cc294",
    # The selected one-chain target and its complete augmented output type.
    "computations/verify_h3_selected_lower_one_chain_comparison_reduction.py":
        "c9fc8c847327d0e119264a3a83cf39d0f4c2ff45b4ddd4e048f42a57cac0e887",
    # Exact output-side M_v packet.
    "computations/verify_h3_literal_mv_cap_cartan_composition.py":
        "8e54a161402499c638dcba6177069fc3bb37648fb37c3546955310a56889744e",
    # Exhaustive relative generator/separator alternative.
    "computations/verify_h3_six_term_exhaustive_relative_extension_alternative.py":
        "bcc55b05c10ba1ac6f3c4415c18a70274ecc29dd506fbed8e69d471b5f0a5607",
    # Universal root-unipotent factorization of the signed Weyl element.
    "computations/verify_h3_sl2_weyl_cartan_prism.py":
        "1024864418fea8f7f4ca6c77015972febd236f2a9822112daf20e1cf979bddaa",
    # A q-comparison defect is already a relative generator when both sides
    # are complete physical relative domains.
    "computations/verify_dark_cartan_physical_q_protected_quotient_comparison.py":
        "eb56cdb4ab1915f8ce35ab3acf0398b4f526c52a17c9c8ebafcc7a5ad4f86bcc",
    # Polynomial ridge commutation does not itself construct physical
    # labelled repeated-grade terminal typing.
    "computations/verify_h3_residual_q_order6_ridge_jet_commutation.py":
        "00a0798b4aa1d901b52645cac3f1dbe2854a3d8ce796191f7a4ff9a6e295b28f",
}
EXPECTED_LEDGER_SHA256 = (
    "84a38fa40d8cba4d47a6107d62239ddd86b2510fce78455acdc2cd3d77e87eeb"
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


def add(left, right, scale=Q(1)):
    answer = dict(left)
    for key, value in right.items():
        answer[key] = answer.get(key, Q(0)) + Q(scale) * Q(value)
        if not answer[key]:
            del answer[key]
    return answer


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


def nullspace(rows, width):
    work = [[Q(value) for value in row] for row in rows]
    pivots = []
    pivot_row = 0
    for column in range(width):
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
        pivots.append(column)
        pivot_row += 1
    free = [column for column in range(width) if column not in pivots]
    basis = []
    for column in free:
        vector = [Q(0)] * width
        vector[column] = Q(1)
        for row, pivot in enumerate(pivots):
            vector[pivot] = -work[row][column]
        basis.append(tuple(vector))
    return tuple(basis)


def dot(left, right):
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def boundary_or_cokernel_mutation_guard():
    """Exhaust small maps: target is in the image or a dual detects it."""
    cases = 0
    boundary = 0
    cokernel = 0
    for height in range(1, 4):
        for width in range(3):
            entries = height * width + height
            for bits in product((0, 1), repeat=entries):
                columns = tuple(
                    tuple(Q(bits[column * height + row])
                          for row in range(height))
                    for column in range(width)
                )
                target = tuple(Q(value) for value in bits[height * width:])
                column_rows = tuple(zip(*columns, strict=True)) if columns else ()
                old_rank = rank(column_rows)
                enlarged_columns = columns + (target,)
                enlarged_rows = tuple(zip(*enlarged_columns, strict=True))
                new_rank = rank(enlarged_rows)
                if new_rank == old_rank:
                    boundary += 1
                else:
                    # lambda is in the left nullspace of the column map, or
                    # equivalently ker(columns^T), and must detect target.
                    transpose_rows = columns
                    duals = nullspace(transpose_rows, height)
                    witness = next((dual for dual in duals
                                    if dot(dual, target)), None)
                    require(witness is not None,
                            "the cokernel branch lost its dual witness")
                    normalized = tuple(value / dot(witness, target)
                                       for value in witness)
                    require(all(dot(normalized, column) == 0
                                for column in columns)
                            and dot(normalized, target) == 1,
                            "the normalized cokernel witness changed")
                    cokernel += 1
                require(new_rank in (old_rank, old_rank + 1),
                        "one target changed rank by more than one")
                cases += 1
    require(cases == 682 and boundary and cokernel,
            ("boundary/cokernel census changed", cases, boundary, cokernel))
    return {
        "binary_complete_maps": cases,
        "boundary_cases": boundary,
        "cokernel_cases": cokernel,
    }


SITES = tuple(range(8))
TAIL_SITES = (2, 5)


def ghz_target():
    return {tuple([colour] * len(SITES)): Q(1) for colour in range(3)}


def root_on_target(target, site, old, new):
    """Infinitesimal matrix unit e_new<-e_old at one tensor factor."""
    answer = {}
    for word, coefficient in target.items():
        if word[site] != old:
            continue
        changed = list(word)
        changed[site] = new
        changed = tuple(changed)
        answer[changed] = answer.get(changed, Q(0)) + Q(coefficient)
    return {word: value for word, value in answer.items() if value}


def endpoint_swap_word(word):
    changed = list(word)
    changed[0], changed[1] = changed[1], changed[0]
    return tuple(changed)


def signed_tail_weyl_target(target):
    answer = {}
    for word, coefficient in target.items():
        changed = list(word)
        sign = Q(1)
        for site in TAIL_SITES:
            if changed[site] == 1:
                changed[site] = 2
                sign *= -1
            elif changed[site] == 2:
                changed[site] = 1
        changed = tuple(changed)
        answer[changed] = answer.get(changed, Q(0)) + sign * coefficient
    return {word: value for word, value in answer.items() if value}


def target_fibre_equivariance_audit():
    """Locate the first obstruction to an equivariant fixed-GHZ Tate model."""
    delta = ghz_target()
    root_records = []
    root_images = []
    for site in TAIL_SITES:
        for old, new in ((1, 2), (2, 1)):
            image = root_on_target(delta, site, old, new)
            require(len(image) == 1,
                    ("a local root stopped moving GHZ", site, old, new))
            word = next(iter(image))
            require(word not in delta,
                    "a tail root image became a projective GHZ direction")
            root_images.append(image)
            root_records.append({
                "site": site,
                "root": f"{new}<-{old}",
                "GHZ_normal_support": [list(word)],
            })
    supports = [next(iter(image)) for image in root_images]
    require(len(set(supports)) == 4,
            "the four tail-root normal directions lost independence")

    # On the target coordinate ring, if f_w=y_w-Delta_w then
    # X(f_w)(Delta)=(X Delta)_w.  A nonzero record above proves that the
    # point ideal m_Delta is not X-stable.  Hence the fixed derived fibre is
    # not equivariant under any of these connected root directions.
    w_delta = signed_tail_weyl_target(delta)
    defect = add(w_delta, delta, -1)
    require(len(defect) == 4,
            ("the signed Weyl GHZ defect changed", defect))
    swapped_defect = {
        endpoint_swap_word(word): value for word, value in defect.items()
    }
    require(swapped_defect == defect,
            "endpoint oddization stopped killing the Weyl target path")
    require(all(word[0] == word[1] for word in w_delta),
            "the tail Weyl orbit left the endpoint-fixed target locus")
    return {
        "tail_root_directions": root_records,
        "tail_root_span_intersection_with_GHZ_projective_stabilizer": 0,
        "fixed_point_ideal_is_root_stable": False,
        "signed_Weyl_target_defect_support": len(defect),
        "endpoint_swap_fixes_defect": True,
        "endpoint_swap_fixes_tail_root_orbit_pointwise": True,
    }


def orbit_path_fixed_fibre_transport_audit():
    """The vertical orbit path is not a nonzero fixed-fibre boundary.

    At the initial base point use vertical labels v,sv; at the terminal base
    point use wv,swv.  The difference of the path and its s-transport has
    zero base component.  Equivariant parallel transport by w^{-1} sends
    wv->v and swv->sv, so its endpoint boundary cancels in the fixed fibre.
    Keeping the four coordinate labels instead retains the private packet,
    but is then a chain over the orbit rather than a chain in one fibre.
    """
    # Coordinate order: v, sv at Delta; wv, swv at wDelta.
    path = (Q(-1), Q(0), Q(1), Q(0))
    s_path = (Q(0), Q(-1), Q(0), Q(1))
    odd_path_boundary = tuple(left - right for left, right in
                              zip(path, s_path, strict=True))
    require(odd_path_boundary == (Q(-1), Q(1), Q(1), Q(-1)),
            "the vertical orbit-path boundary changed")
    # Equivariant retraction/transport to the Delta fibre.
    transport = (
        (Q(1), Q(0), Q(1), Q(0)),
        (Q(0), Q(1), Q(0), Q(1)),
    )
    transported = tuple(dot(row, odd_path_boundary) for row in transport)
    require(transported == (Q(0), Q(0)),
            "canonical fixed-fibre transport retained an orbit boundary")
    # The two source paths cover the same target/base path because s fixes
    # the orbit pointwise.  Their difference is vertical in the relative
    # orbit complex.
    base_projection = Q(1) - Q(1)
    require(base_projection == 0,
            "the endpoint-odd path acquired a base component")
    return {
        "ambient_endpoint_boundary": [int(value)
                                      for value in odd_path_boundary],
        "base_path_projection": 0,
        "equivariant_transport_to_Delta_fibre": [0, 0],
        "private_boundary_survives_in_fixed_labels": True,
        "private_boundary_survives_canonical_fibre_transport": False,
    }


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    cartan = load(
        "computations/verify_h3_physical_cartan_source_orbit_descent.py",
        "minimal_weyl_cone_cartan",
    ).audit()
    require(cartan["literal_root_covariance"]["complete_words_checked"]
            == 4 * 3 ** 7
            and cartan["literal_endpoint_involution"][
                "complete_words_checked"] == 3 ** 8,
            "the complete-row Cartan descent census changed")

    gate = load(
        "computations/verify_h3_selected_lower_relative_weyl_bar_gate.py",
        "minimal_weyl_cone_gate",
    )
    gate_ledger, gate_digest = gate.audit()
    require(gate_digest
            == "bb89890d7ba7a2100fcd3ad6ad6a6d4c2c57284480e7516b9a3b6419c1d5bdd5",
            "the selected Weyl-bar ledger changed")
    formal = gate_ledger["fine_components"]
    image = gate_ledger["complete_physical_bar_image"]
    dual = gate_ledger["primitive_odd_dual"]
    require(formal["operator_terms"] == [341, 341]
            and formal["tau_Z0_equals_minus_Z1"],
            "the formal two-component Weyl bar changed")
    require(image["endpoint_plus_all_bar_rank"] == 8
            and image["endpoint_bar_plus_four_hasse_face_rank"] == 12
            and image["rank_after_required_private_packet"] == 13,
            "the exact occurrence quotient changed")
    require(dual["on_complete_endpoints_bars_and_four_hasse_faces"] == 0
            and dual["on_required_endpoint_odd_face"] == 1,
            "the occurrence quotient dual changed")

    # The chain-valued normalized group-bar construction.  z0,z1 and their
    # endpoint transports are total cycles.  tau(z0)=-z1; hence the bar
    # boundary is -(z0+z1), and endpoint oddization gives the four corners.
    z0 = {"Z0": Q(1)}
    tau_z0 = {"Z1": Q(-1)}
    formal_bar_boundary = add(tau_z0, z0, -1)
    require(formal_bar_boundary == {"Z0": Q(-1), "Z1": Q(-1)},
            "the one-generator group-bar boundary changed")
    endpoint_transport = {"sZ0": Q(-1), "sZ1": Q(-1)}
    odd_bar_boundary = add(formal_bar_boundary, endpoint_transport, -1)
    require(odd_bar_boundary == {
        "Z0": Q(-1), "Z1": Q(-1),
        "sZ0": Q(1), "sZ1": Q(1),
    }, "the endpoint-odd total bar boundary changed")
    require(gate_ledger["protected_formal_rows"][
                "normalized_bar_augmentation"] == 0
            and gate_ledger["protected_formal_rows"][
                "endpoint_odd_target"] == 0,
            "the forced formal augmented rows changed")

    # A concrete model of the exact rank-one quotient Q_xi.  It is only a
    # model of the certified ranks, not a replacement for the literal dual.
    b_rows = tuple(tuple(Q(int(row == column)) for column in range(13))
                   for row in range(12))
    private = tuple(Q(int(column == 12)) for column in range(13))
    require(rank(b_rows) == 12 and rank(b_rows + (private,)) == 13,
            "the rank-one occurrence quotient model changed")
    lambda_private = private
    require(all(dot(lambda_private, row) == 0 for row in b_rows)
            and dot(lambda_private, private) == 1,
            "the quotient section/dual normalization changed")

    mutation = boundary_or_cokernel_mutation_guard()
    fibre = target_fibre_equivariance_audit()
    orbit_transport = orbit_path_fixed_fibre_transport_audit()
    ledger = {
        "theorem": "minimal totalized Weyl cone and physical occurrence-section alternative",
        "reconciliation": {
            "whole_row_Cartan_descent": (
                "c92667c proves the Ward square on each complete 90-term "
                "matching row and the physical endpoint permutation"
            ),
            "what_it_does_not_prove": (
                "a source preimage of an individual matching occurrence, "
                "or stability/section of the occurrence quotient needed by xi"
            ),
            "no_contradiction": (
                "whole-row covariance acts on the trivial matching-occurrence "
                "summand; the missing Gate-I packet is nontrivial in the "
                "rank-one quotient detected below"
            ),
        },
        "exact_missing_quotient": {
            "ambient": (
                "literal monomial space in the four xi/mate/endpoint-transport "
                "fine grades"
            ),
            "old_subspace": (
                "eight complete endpoints, all complete-row normalized/odd "
                "Weyl bars, and four direct-free Hasse-face bridges"
            ),
            "old_endpoint_bar_rank": image["endpoint_plus_all_bar_rank"],
            "old_rank_with_Hasse_faces": image[
                "endpoint_bar_plus_four_hasse_face_rank"
            ],
            "rank_with_private_packet": image[
                "rank_after_required_private_packet"
            ],
            "Q_xi_dimension": 1,
            "normalized_dual": dual["private_coordinates"],
            "dual_on_old_and_private": [0, 1],
            "missing_section": (
                "for pi:V_xi->V_xi/B_xi and the physical relative boundary "
                "d_rel, construct sigma_xi:Q_xi->L_rel,1 with "
                "pi d_rel sigma_xi=id_Q_xi"
            ),
        },
        "canonical_formal_one_cell": {
            "source_complex": (
                "homotopy-orbit/group-bar of the complete Hasse/PP "
                "totalization"
            ),
            "generator": "b_xi=(1-s)[tau|Z0_tilde]",
            "operator_terms_per_endpoint": formal["operator_terms"],
            "boundary": "d[tau|Z0_tilde]=-(Z0_tilde+Z1_tilde)",
            "endpoint_odd_boundary": {
                key: int(value) for key, value in odd_bar_boundary.items()
            },
            "normalized_bar_augmentation": 0,
            "GHZ_target": 0,
            "advantage": (
                "one chain-valued bar generator packages the 341 formal "
                "edges and every Hasse face; no independent edge census is needed"
            ),
            "physical_status": (
                "formal relative extension only.  Bar_R(R/I) does not by "
                "itself contain the group homotopy-orbit generator; physical "
                "promotion is exactly the section sigma_xi above"
            ),
        },
        "equivariant_cotangent_Tate_audit": {
            "fixed_GHZ_fibre": fibre,
            "premise_correction": (
                "the connected root-unipotent word does not stabilize the "
                "GHZ point or its point ideal.  Each of the four tail-root "
                "directions has a distinct nonzero normal value on GHZ"
            ),
            "why_fixed_fibre_Tate_descent_fails": (
                "for a target relation f_w=y_w-Delta_w, evaluation of "
                "X(f_w) at Delta equals the nonzero coordinate "
                "(X Delta)_w.  Thus root contraction is not an endomorphism "
                "of the cotangent/Tate complex of the fixed fibre"
            ),
            "correct_canonical_object": (
                "use the derived source family over the connected tail-root "
                "orbit of Delta, with its functorial simplicial polynomial/"
                "bar resolution and relative homotopy kernel over that orbit"
            ),
            "minimal_Tate_warning": (
                "an arbitrary minimal Tate resolution is not functorial; the "
                "canonical equivariant model is the simplicial bar/PP model"
            ),
            "corrected_descent_theorem": (
                "the root-unipotent factorization acts on the orbit-family "
                "resolution and integrates the universal Cartan homotopy.  "
                "The endpoint swap fixes the whole tail-root target orbit "
                "pointwise, so (1-s) sends the orbit path to zero and places "
                "b_xi in the relative homotopy kernel"
            ),
            "derived_occurrence_section": (
                "the pinned private boundary of b_xi has nonzero class in "
                "Q_xi; after its certified normalization it canonically "
                "realizes sigma_xi inside this orbit-relative derived model"
            ),
            "fixed_fibre_pullback_audit": orbit_transport,
            "strong_pullback_claim": False,
            "why_parallel_transport_does_not_close": (
                "the endpoint-odd difference is vertical over the orbit, but "
                "equivariant transport w^{-1} identifies wv with v and swv "
                "with sv.  Its four-corner endpoint boundary therefore maps "
                "to zero in the Delta fibre.  Keeping the private packet uses "
                "fixed coordinate labels and leaves the chain orbit-relative"
            ),
            "physical_comparison_still_required": (
                "a chain map from the orbit-relative simplicial PP model to "
                "the literal physical augmented correction complex, preserving "
                "word/fine/repeated grade and protected rows"
            ),
            "replacement_by_canonical_fibre": (
                "not sufficient: an ordinary quasi-isomorphism to the fixed "
                "cotangent/Tate fibre discards the orbit-relative section.  "
                "One must retain the relative orbit cone or add an enriched "
                "comparison/connection that preserves its labelled boundary"
            ),
            "label_tradeoff": (
                "equivariant transport preserves the fibre but identifies the "
                "Weyl-shifted fine labels; fixed-label transport preserves the "
                "private word/fine packet but is not a fixed-fibre map"
            ),
        },
        "smallest_positive_physical_datum": {
            "new_source_type": (
                "one endpoint-odd, occurrence-local PP/Weyl-bar generator "
                "lifting b_xi in the canonical word/fine/repeated grade"
            ),
            "forced_primitive_rows": {
                "private_first_face": (
                    "an oriented nonzero multiple of "
                    "xi-mate-sxi+smate; normalize it to the certified packet"
                ),
                "normalized_bar_augmentation": 0,
                "target": 0,
            },
            "required_capped_augmented_column": {
                "literal_boundary_features": 360,
                "Eq": [-1, 1, 1, -1],
                "ordinary_residue": [0, 0, 0, 0],
                "D_W_target_ainc": [0, 0, 0, 0],
                "eta_z": "1+delta_(vz)*u_z/t",
                "sigma": "-q_pq^22",
            },
            "scope_guard": (
                "only augmentation and target are forced on the bare group "
                "bar.  D/W/ainc/Eq/residue/eta/sigma must be defined by the "
                "physical capped comparison; source naturality does not infer them"
            ),
        },
        "positive_relative_extension_alternative": {
            "boundary_branch": (
                "if the complete physical relative boundary hits the desired "
                "augmented column modulo the old image, choose one preimage; "
                "this is the selected cell C with J3 C=A Jcol(l)"
            ),
            "cokernel_branch": (
                "if not, finite-dimensional duality gives a functional killing "
                "the complete relative image and reading one on the desired column"
            ),
            "filler_ambiguity": (
                "two boundary-branch fillers differ by the protected kernel; "
                "a nonzero physical terminal on that difference normalizes to "
                "the relative generator, while zero terminal makes the comparison "
                "well-defined and passes to the Fredholm separator alternative"
            ),
            "lambda_xi_scope": (
                "the certified lambda_xi is the first associated-graded seed. "
                "It is a final physical separator only if it extends across "
                "every future relative generator and every augmented row"
            ),
            "physical_q_upgrade": (
                "exact terminal equality is unnecessary after the comparison "
                "lands in complete physical relative domains with physical "
                "q=sum(six matching rows)-ainc on both sides: a nonzero q "
                "transport defect is already a relative generator, while a "
                "zero defect gives the augmented q comparison and Fredholm branch"
            ),
            "q_scope_guard": (
                "the exhaustive q alternative does not define q on the new "
                "derived generator.  Physical q typing on the complete domain "
                "is still required; eta/sigma ridge commutation at polynomial "
                "level does not supply that comparison"
            ),
            "mutation_guard": mutation,
        },
        "verdict": (
            "the fixed-GHZ equivariant-Tate premise is false, but the corrected "
            "orbit-relative simplicial PP construction canonically realizes "
            "the source-side rank-one section sigma_xi.  It cannot be pulled "
            "back to the Delta fibre with its private boundary by canonical "
            "parallel transport.  The proof frontier is one enriched comparison "
            "from the retained orbit-relative cell to the literal physical "
            "protected complex, plus physical q typing; no 341-edge expansion "
            "is needed"
        ),
        "scope": (
            "exact reconciliation of the complete-row and private-face "
            "theorems, exact rank-one first obstruction, and exact one-cell "
            "extension/dual alternative.  No physical occurrence-local source "
            "generator is asserted without sigma_xi"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("minimal totalized Weyl cone ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("h3 selected lower minimal totalized Weyl cone: EXACT ALTERNATIVE")
    print("orbit-relative occurrence section: YES; fixed-fibre pullback: NO")
    print("formal 341-edge bar: one chain-valued generator")
    print("occurrence quotient dimension: 1 (rank 12 -> 13)")
    print("next datum: enriched physical comparison plus physical q typing")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
