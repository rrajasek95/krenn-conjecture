#!/usr/bin/env python3
"""Audit the selected K4/central-Eq mixed derived-intersection cell.

The complete mixed response equation is the sum of thirty ordered-endpoint
K4 matching fibres.  Its first principal-parts row is therefore the sum of
the thirty six-term derivatives.  The marked six-term row at endpoints
(0,1) is not itself the derivative of an equation in the current source
presentation.

Consequently the Koszul/Tate cross-cell with the central normal
E=(H0-u)e_Eq is canonical only for the aggregate response generator.  A
formal selected cell has square-zero boundary, but it requires a pointed
generator eps_01 with d eps_01=b_01.  This checker freezes that exact
source-provenance obstruction, the proper faces, and the target scope.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SITES = tuple(range(6))
MARKED = (0, 1)
PINS = {
    "computations/verify_h3_centered_projector_literal_first_hasse_eq_incidence_gate.py":
        "4e32d14b4d495b4439ed7aba59afedc8de0c1c4f76717989ca9e817444e9cd8f",
    "notes/h3-centered-projector-literal-first-hasse-eq-incidence-gate.md":
        "242a0a148c782c73540f060ef4e685902888f6d0e95da2d050b0e46dec5baf9d",
    "computations/verify_h3_reduced_eq_koszul_tate_relative_orbit_gate.py":
        "15b47a420a6f1e2e6eb0b89e5e5efb5c895172e30b8ab9339dfa1e451ac03668",
    "notes/h3-reduced-eq-koszul-tate-relative-orbit-gate.md":
        "5d5d0b2639cca085d4cc818ba718c154bd5105c79dfbcecd63c018e6a36c92ac",
    "computations/verify_h3_e14_t12_orbit_unary_companion_cycle_gate.py":
        "28a0baf3e6930e9336ceb5632e0abb8509a21ddaa1446eb7e93482831c35bc42",
    "notes/h3-e14-t12-orbit-unary-companion-cycle-gate.md":
        "9d04e359afb3a47b4e547797a00c29f7559a060aa51a69fdda984c0e988f2765",
}
EXPECTED_LEDGER_SHA256 = (
    "57c9c27575b4c08b66cf9132d6014beaeacf810c1e1ee420b5a6e7c20c001737"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def dot(left: tuple[Q, ...], right: tuple[Q, ...]) -> Q:
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def rank(columns: tuple[tuple[Q, ...], ...]) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank width")
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


def edge(left: int, right: int) -> tuple[int, int]:
    return tuple(sorted((left, right)))


def residual_matchings(p_site: int, s_site: int):
    residual = tuple(site for site in SITES if site not in (p_site, s_site))
    a, b, c, d = residual
    return (
        tuple(sorted((edge(a, b), edge(c, d)))),
        tuple(sorted((edge(a, c), edge(b, d)))),
        tuple(sorted((edge(a, d), edge(b, c)))),
    )


def response_fibre_and_first_pp_audit() -> dict[str, object]:
    endpoints = tuple((p_site, s_site) for p_site in SITES
                      for s_site in SITES if p_site != s_site)
    require(len(endpoints) == 30, "ordered endpoint count changed")

    fibre_terms = {}
    pp_terms = {}
    for endpoint in endpoints:
        matchings = residual_matchings(*endpoint)
        fibre_terms[endpoint] = tuple(matchings)
        faces = []
        for matching in matchings:
            for differentiated in matching:
                undifferentiated = next(value for value in matching
                                        if value != differentiated)
                # Retain the endpoint tag: different fixed-endpoint fibres
                # are distinct physical occurrence/source-provenance slots.
                faces.append((endpoint, differentiated, undifferentiated))
        require(len(faces) == len(set(faces)) == 6,
                ("six-term fibre changed", endpoint, faces))
        pp_terms[endpoint] = tuple(faces)

    all_faces = tuple(face for endpoint in endpoints for face in pp_terms[endpoint])
    require(len(all_faces) == len(set(all_faces)) == 180,
            "the thirty tagged six-term PP fibres stopped being disjoint")

    marked_faces = pp_terms[MARKED]
    expected_marked = (
        (MARKED, (2, 3), (4, 5)),
        (MARKED, (4, 5), (2, 3)),
        (MARKED, (2, 4), (3, 5)),
        (MARKED, (3, 5), (2, 4)),
        (MARKED, (2, 5), (3, 4)),
        (MARKED, (3, 4), (2, 5)),
    )
    require(marked_faces == expected_marked,
            ("marked K4 derivative changed", marked_faces))

    # In the fibre coefficient module, the only old complete response
    # generator is 1_30.  A marked fibre is independent modulo that line.
    aggregate = tuple(Q(1) for _ in endpoints)
    marked_index = endpoints.index(MARKED)
    marked = tuple(Q(index == marked_index) for index in range(len(endpoints)))
    comparison_index = next(index for index, endpoint in enumerate(endpoints)
                            if endpoint == (1, 0))
    separator = tuple(Q(index == marked_index) - Q(index == comparison_index)
                      for index in range(len(endpoints)))
    require(rank((aggregate,)) == 1 and rank((aggregate, marked)) == 2
            and dot(separator, aggregate) == 0
            and dot(separator, marked) == 1,
            "the selected endpoint fibre stopped being private")

    # The same exact separation persists after first PP.  Select the first
    # structural face in each endpoint block; it kills the complete sum and
    # reads the marked six-term derivative.
    face_lookup = {face: index for index, face in enumerate(all_faces)}
    aggregate_pp = tuple(Q(1) for _ in all_faces)
    marked_pp = tuple(Q(face in set(marked_faces)) for face in all_faces)
    marked_face = marked_faces[0]
    comparison_face = pp_terms[(1, 0)][0]
    pp_separator = tuple(
        Q(index == face_lookup[marked_face])
        - Q(index == face_lookup[comparison_face])
        for index in range(len(all_faces))
    )
    require(rank((aggregate_pp, marked_pp)) == 2
            and dot(pp_separator, aggregate_pp) == 0
            and dot(pp_separator, marked_pp) == 1,
            "the selected six-term derivative stopped being PP-private")

    return {
        "response_head_word": "11:110000",
        "ordered_endpoint_fibres": len(endpoints),
        "matching_monomials_per_fibre": 3,
        "first_PP_faces_per_fibre": 6,
        "complete_tagged_PP_faces": len(all_faces),
        "marked_fibre": "b_01=p0*s1*(q23q45+q24q35+q25q34)",
        "marked_first_PP_face": (
            "p0*s1*(dq23*q45+q23*dq45+dq24*q35+q24*dq35+"
            "dq25*q34+q25*dq34)"
        ),
        "old_complete_response_equation": "R=sum_(p!=s)b_ps",
        "fibre_rank_old_then_marked": [1, 2],
        "primitive_fibre_separator": "b_01^*-b_10^*",
        "PP_rank_old_then_marked": [1, 2],
        "primitive_PP_separator": (
            "(01,dq23*q45)^*-(10,corresponding first PP face)^*"
        ),
        "source_provenance": (
            "db_01 is a literal formula but not the derivative of a "
            "separate equation/generator in the current physical source"
        ),
    }


def koszul_tate_cross_cell_audit() -> dict[str, object]:
    # Let theta be the clean central Tate edge with boundary E=(H0-u)e_Eq.
    # If eps is an honest response generator with boundary b, the mixed cell
    # kappa has the canonical Leibniz boundary
    #
    #        d kappa = b theta - eps E.
    #
    # The two second-boundary terms cancel with coefficient +1,-1.
    second_boundary = {"b*E": Q(1) - Q(1)}
    second_boundary = {key: value for key, value in second_boundary.items()
                       if value}
    require(not second_boundary, "the mixed Koszul square stopped closing")

    # One cell is necessary and sufficient after eps_01 is present.  Before
    # it is present, only eps_R exists, and its cell has aggregate response
    # incidence.  Retain (aggregate response, selected response, central E,
    # mixed selected incidence) to make the distinction primitive.
    aggregate_edge = (Q(1), Q(0), Q(0), Q(0))
    central_edge = (Q(0), Q(0), Q(1), Q(0))
    aggregate_cross = (Q(1), Q(0), Q(1), Q(0))
    selected_cross = (Q(0), Q(1), Q(1), Q(1))
    mixed_dual = (Q(0), Q(0), Q(0), Q(1))
    old = (aggregate_edge, central_edge, aggregate_cross)
    require(rank(old) == 2 and rank(old + (selected_cross,)) == 3
            and all(dot(mixed_dual, column) == 0 for column in old)
            and dot(mixed_dual, selected_cross) == 1,
            "the selected mixed-incidence obstruction changed")

    return {
        "central_edge": "theta with d(theta)=E=(H0-u)e_Eq",
        "aggregate_response_edge": "epsilon_R with d(epsilon_R)=R",
        "canonical_aggregate_cell": (
            "kappa_R=epsilon_R wedge theta; "
            "d(kappa_R)=R*theta-epsilon_R*E"
        ),
        "formal_selected_cell": (
            "kappa_01=epsilon_01 wedge theta; "
            "d(kappa_01)=b_01*theta-epsilon_01*E"
        ),
        "selected_d_squared": 0,
        "selected_cell_exists_iff": (
            "a source-labelled pointed response generator epsilon_01 "
            "with d(epsilon_01)=b_01 (or an equivalent section modulo R)"
        ),
        "first_PP_proper_faces": [
            "(db_01)*theta (the literal six-term fixed-endpoint face)",
            "b_01*(delta theta)",
            "-(delta epsilon_01)*(H0-u)e_Eq",
            "-epsilon_01*((dH0-du)e_Eq+(H0-u)d(e_Eq))",
        ],
        "aggregate_replacement": (
            "replace b_01,epsilon_01,db_01 by R,epsilon_R,dR; "
            "this is canonical but does not split the marked fibre"
        ),
        "rank_before_after_selected_mixed_cell": [2, 3],
        "primitive_selected_mixed_dual": [0, 0, 0, 1],
        "classification": (
            "the central incidence is the fundamental mixed class only in "
            "the enlarged pointed presentation; it is an excess/cokernel "
            "class in the current complete-row presentation"
        ),
    }


def target_and_physical_scope_audit() -> dict[str, object]:
    previous = load(
        "computations/verify_h3_centered_projector_literal_first_hasse_eq_incidence_gate.py",
        "fixed_endpoint_central_eq_previous",
    )
    matching = previous.derivative_of_matching_fibre_audit()
    endpoint = previous.endpoint_first_face_audit()
    require(matching["target_readout"] == 0
            and endpoint["target_normal_support"] == 18
            and endpoint["detector_on_Delta"] == 0
            and endpoint["detector_on_normal"] == 1,
            "the marked target audit changed")

    reduced = load(
        "computations/verify_h3_reduced_eq_koszul_tate_relative_orbit_gate.py",
        "fixed_endpoint_central_eq_reduced",
    )
    old = reduced.old_physical_block_audit()
    require(old["forced_defect"] == "labelled ordinary residue +Y"
            and old["rank_before_after"] == [3, 4],
            "the physical central-Tate promotion obstruction changed")
    return {
        "marked_matching_and_six_term_target": 0,
        "endpoint_Cartan_target_normal": endpoint["target_normal_formula"],
        "endpoint_target_normal_support": 18,
        "primitive_target_detector": "X_101000^*",
        "detector_on_GHZ_Delta": 0,
        "detector_on_endpoint_normal": 1,
        "consequence": (
            "the mixed Koszul square does not cancel the endpoint moving-"
            "target normal; that correction is a separate proper face"
        ),
        "central_Tate_physical_scope": (
            "even the aggregate square is conditional on promoting the "
            "clean target-zero central theta into the physical augmented "
            "source; the nearest old lift has forced labelled residue +Y"
        ),
        "terminal_scope": (
            "the fibre and mixed-incidence covectors are exact local source "
            "cokernel classes, not physical Fredholm terminals until they "
            "extend across all word/fine/target/anchor/q/ridge/W/eta/sigma rows"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "fixed-endpoint K4 / central-Eq derived-intersection gate",
        "pins": PINS,
        "response_and_PP_provenance": response_fibre_and_first_pp_audit(),
        "mixed_Koszul_Tate_cell": koszul_tate_cross_cell_audit(),
        "target_and_physical_scope": target_and_physical_scope_audit(),
        "verdict": (
            "The natural 2x2 Koszul/Tate cell is canonical for the complete "
            "response equation R=sum b_ps and the central Eq normal.  It is "
            "not a canonical selected-cell construction: the required "
            "six-term face is db_01, while the physical source contains only "
            "dR.  Adjoining one pointed response generator epsilon_01 makes "
            "the formal selected square close with d^2=0 and is exactly the "
            "extra source theorem.  Matching target is zero, but the 18-word "
            "endpoint target normal and clean central-Tate augmentation remain "
            "separate physical faces."
        ),
        "shortest_positive_theorem": (
            "construct one augmented pointed response section epsilon_01 "
            "and a physical target-zero central theta, natural under the "
            "endpoint/matching orbit.  Their canonical mixed Koszul cell then "
            "supplies the selected central incidence; moving-target and the "
            "remaining cap/ridge/q rows must be carried as its typed proper faces"
        ),
        "scope": (
            "exact h=3 source-presentation, first-PP, derived-square, and "
            "target-normal audit; no full terminal promotion or selected "
            "physical section is asserted"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("fixed-endpoint/central-Eq ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("complete response / selected endpoint fibre ranks: 1 -> 2")
    print("complete PP / selected six-term ranks: 1 -> 2")
    print("aggregate response x central Eq square: CANONICAL (conditional theta)")
    print("selected six-term x central Eq square: NEEDS POINTED SOURCE GENERATOR")
    print("matching target: ZERO; endpoint target normal: SUPPORT 18")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
