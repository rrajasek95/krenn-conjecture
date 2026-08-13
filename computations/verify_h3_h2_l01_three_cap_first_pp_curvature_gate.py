#!/usr/bin/env python3
"""Compute the first PP face of the combined L01 three-cap cell.

Let A=Dq01, B=p0s1, C=p1s0 and let H be the three-term hafnian on
sites 2345.  A covariant family of capped Hasse cells C_A,C_B,C_C would
simultaneously give

    C_R = C_A+C_B+C_C          (the nine-term R01 block),
    C_L = 2C_A-C_B-C_C         (the desired L01 block).

Thus the block projector and capped-C4 pieces are one three-cap family, not
two unrelated source generators.  Its first unavoidable principal-parts
face is the literal Kahler differential dL01.  It has 36 terms: 18 obtained
by differentiating the residual matching tail and 18 by differentiating the
two direction factors.  The tail half is labelwise centered.  The direction
half has six nonzero labelled marginals

    3*(2,2,-1,-1,-1,-1)

on dD,dq01,dp0,ds1,dp1,ds0.  Hence target augmentation zero at degree zero
does not make the capped cell protected at first PP.  The pinned matching
projector exposes only the tail half; the endpoint/direction half is the
first exact proper face of the combined chart cell.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_h2_chart_scalar_capped_c4_augmented_gate.py":
        "18cb73805ffca0a080bc061c88cb42f6c0c83d57efd60c574455b757009785b4",
    "notes/h3-h2-chart-scalar-capped-c4-augmented-gate.md":
        "baee4965bcb9315fc7e9f51693aebcf3cfb6c8a147c76144eb287f7c9c74c998",
    "computations/verify_h3_centered_projector_literal_first_hasse_eq_incidence_gate.py":
        "4e32d14b4d495b4439ed7aba59afedc8de0c1c4f76717989ca9e817444e9cd8f",
    "notes/h3-centered-projector-literal-first-hasse-eq-incidence-gate.md":
        "242a0a148c782c73540f060ef4e685902888f6d0e95da2d050b0e46dec5baf9d",
    "computations/verify_h3_o2_augmented_terminal_cap_cartan_extension_gate.py":
        "8a9bfe47c934658d1b10ad42f283d6a017c27125bcb98615882e4bacd975f1eb",
    "notes/h3-o2-augmented-terminal-cap-cartan-extension-gate.md":
        "e9c0cf3c76cbe4c8061574d2b977bf1189a1fa299ef17ae1d2e463c08a313429",
    "computations/verify_h3_universal_response_ks_augmented_readout_extension_gate.py":
        "4493274dfbda62cec0d6823272762fb01c3a798123a1da206559e91890ba9047",
    "notes/h3-universal-response-ks-augmented-readout-extension-gate.md":
        "f201fd4c4599a27173a824d7475ade679ef2de55e7c91bc3dd9cc917ac16ee37",
}
EXPECTED_LEDGER_SHA256 = (
    "ade1328ac5b627cb5019c9f30f84965e93aad0b342cc1a970097c7b66596e3d4"
)

Edge = tuple[int, int]
Matching = tuple[Edge, ...]
PPLabel = tuple[Matching, Edge]


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted((tuple(sorted((first, second))),) + tail))


def rank(columns: tuple[tuple[Q, ...], ...]) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    work = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[answer], work[pivot] = work[pivot], work[answer]
        value = work[answer][column]
        work[answer] = [entry / value for entry in work[answer]]
        for row in range(height):
            if row == answer or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[answer], strict=True)]
        answer += 1
    return answer


def polynomial_data():
    matchings = tuple(perfect_matchings(tuple(range(8))))
    require(len(matchings) == len(set(matchings)) == 105,
            "the K8 hafnian census changed")
    directions: tuple[tuple[Edge, Edge], ...] = (
        ((6, 7), (0, 1)),  # A=D*q01
        ((0, 6), (1, 7)),  # B=p0*s1
        ((1, 6), (0, 7)),  # C=p1*s0
    )
    tails = tuple(perfect_matchings((2, 3, 4, 5)))
    weights = (Q(2), Q(-1), Q(-1))
    local: dict[Matching, Q] = {}
    local_unweighted: dict[Matching, Q] = {}
    ah: dict[Matching, Q] = {}
    for direction_index, direction in enumerate(directions):
        for tail in tails:
            matching = tuple(sorted(direction + tail))
            local[matching] = weights[direction_index]
            local_unweighted[matching] = Q(1)
            if direction_index == 0:
                ah[matching] = Q(1)
    require(len(local) == len(local_unweighted) == 9 and len(ah) == 3,
            "the local three-cap support changed")
    return matchings, directions, tails, local, local_unweighted, ah


def differential(polynomial: dict[Matching, Q]) -> dict[PPLabel, Q]:
    answer = {}
    for matching, coefficient in polynomial.items():
        for edge in matching:
            answer[(matching, edge)] = coefficient
    return answer


def three_cap_and_first_pp_audit() -> dict[str, object]:
    (matchings, directions, tails, l01, r01, ah) = polynomial_data()
    response = {matching: Q(1) for matching in matchings}
    response_rest = {matching: Q(1) for matching in matchings
                     if matching not in r01}
    require(all(l01[matching] == Q(3) * ah.get(matching, 0)
                - r01[matching] for matching in r01),
            "L01=3AH-R01 changed")

    # A single covariant family C_A,C_B,C_C produces both linear
    # combinations.  This coefficient identity freezes the required signs.
    cap_vectors = []
    local_order = tuple(r01)
    for direction in directions:
        cap_vectors.append(tuple(Q(
            set(direction).issubset(set(matching))
        ) for matching in local_order))
    plus = tuple(sum(entries, Q(0))
                 for entries in zip(*cap_vectors, strict=True))
    odd = tuple(Q(2) * cap_vectors[0][index]
                - cap_vectors[1][index] - cap_vectors[2][index]
                for index in range(len(local_order)))
    require(plus == tuple(r01[matching] for matching in local_order)
            and odd == tuple(l01[matching] for matching in local_order),
            "the three-cap top combinations changed")

    d_response = differential(response)
    d_rest = differential(response_rest)
    d_r01 = differential(r01)
    d_ah = differential(ah)
    d_l01 = differential(l01)
    require(len(d_response) == 420 and len(d_rest) == 384
            and len(d_r01) == len(d_l01) == 36 and len(d_ah) == 12,
            "the first-PP support census changed")
    require(all(d_l01[label] == Q(3) * d_ah.get(label, 0)
                - d_r01[label] for label in d_r01),
            "dL01=3d(AH)-dR01 changed")

    # Embed in the complete 420-coordinate first-PP module and recheck the
    # same rank-three/complement obstruction as at degree zero.
    pp_order = tuple(d_response)
    vector = lambda values: tuple(values.get(label, Q(0)) for label in pp_order)
    columns = tuple(map(vector, (d_response, d_l01, d_ah, d_r01)))
    require(rank(columns[:3]) == 3 and rank(columns) == 3,
            "the complete first-PP rank gate changed")
    residual = tuple(columns[1][index] - Q(3) * columns[2][index]
                     + columns[0][index] for index in range(len(pp_order)))
    require(residual == vector(d_rest),
            "the 384-term first-PP complement changed")

    selected_sites = {0, 1, 6, 7}
    tail_half = {label: value for label, value in d_l01.items()
                 if set(label[1]).isdisjoint(selected_sites)}
    direction_half = {label: value for label, value in d_l01.items()
                      if set(label[1]).issubset(selected_sites)}
    require(len(tail_half) == len(direction_half) == 18
            and set(tail_half).isdisjoint(direction_half),
            "the tail/direction first-PP split changed")

    edge_marginals: dict[Edge, Q] = {}
    for (_matching, edge), coefficient in d_l01.items():
        edge_marginals[edge] = edge_marginals.get(edge, Q(0)) + coefficient
    tail_edges = tuple(sorted(edge for edge in edge_marginals
                              if set(edge).isdisjoint(selected_sites)))
    direction_edges = (
        (6, 7), (0, 1), (0, 6), (1, 7), (1, 6), (0, 7),
    )
    require(len(tail_edges) == 6
            and all(edge_marginals[edge] == 0 for edge in tail_edges),
            (tail_edges, edge_marginals))
    direction_profile = tuple(edge_marginals[edge]
                              for edge in direction_edges)
    require(direction_profile == tuple(map(Q, (6, 6, -3, -3, -3, -3))),
            direction_profile)
    require(sum(direction_profile, Q(0)) == 0,
            "the direction marginal stopped being globally centered")

    # The literal matching face in the pinned endpoint projector is exactly
    # the six tail derivatives in one B fibre.  It is one third of the
    # 18-term tail half and contains no direction-factor derivative.
    b_matchings = tuple(matching for matching in r01
                        if set(directions[1]).issubset(set(matching)))
    b_matching_face = {
        (matching, edge): Q(-1)
        for matching in b_matchings for edge in matching
        if set(edge).isdisjoint(selected_sites)
    }
    require(len(b_matching_face) == 6
            and set(b_matching_face).issubset(tail_half),
            "the pinned six-term matching face changed")

    # A complete-response separator persists at first PP.  Put +1 on one
    # local B direction derivative and -1 on any outside derivative.  It
    # kills dR and d(AH) but detects dL.
    local_label = next(label for label in direction_half
                       if set(directions[1]).issubset(set(label[0])))
    outside_label = next(label for label in d_response if label not in d_r01)
    separator = {local_label: Q(1), outside_label: Q(-1)}
    pairing = lambda values: sum((coefficient * values.get(label, 0)
                                  for label, coefficient in separator.items()),
                                 Q(0))
    require(pairing(d_response) == 0 and pairing(d_ah) == 0
            and pairing(d_l01) == -1,
            "the first-PP separating dual changed")

    return {
        "three_cap_family": {
            "unweighted_sum": "C_A+C_B+C_C has top R01",
            "centered_sum": "2C_A-C_B-C_C has top L01",
            "conclusion": (
                "the block projector and capped C4 are the two projections "
                "of one covariant three-cap family"
            ),
        },
        "degree_zero": {
            "complete_response_occurrences": len(response),
            "local_R01_occurrences": len(r01),
            "outside_occurrences": len(response_rest),
        },
        "first_PP": {
            "complete_response_support": len(d_response),
            "local_dR01_support": len(d_r01),
            "dL01_support": len(d_l01),
            "outside_support": len(d_rest),
            "rank_dR_dL_dAH": rank(columns[:3]),
            "rank_after_dR01": rank(columns),
            "identity": "dL01=3d(Dq01 H2345)-dR01",
            "complete_response_residual": "d(R-R01), support 384",
            "tail_derivative_support": len(tail_half),
            "direction_derivative_support": len(direction_half),
            "pinned_single_fibre_matching_face_support": len(b_matching_face),
        },
        "labelled_marginals": {
            "tail_edge_order": [repr(edge) for edge in tail_edges],
            "tail_values": [str(edge_marginals[edge]) for edge in tail_edges],
            "direction_edge_order": [
                "dD", "dq01", "dp0", "ds1", "dp1", "ds0",
            ],
            "direction_values": [str(value) for value in direction_profile],
            "primitive_direction_profile": [2, 2, -1, -1, -1, -1],
            "global_sum": str(sum(direction_profile, Q(0))),
            "interpretation": (
                "degree-zero target augmentation and every tail-dq marginal "
                "vanish, but the six endpoint/direction PP labels do not"
            ),
        },
        "separating_dual": (
            "+1 on one local B direction derivative and -1 on one outside "
            "derivative; kills dR and d(DqH), detects dL"
        ),
    }


def physical_scope_audit() -> dict[str, object]:
    prior = load(
        "computations/verify_h3_h2_chart_scalar_capped_c4_augmented_gate.py",
        "l01_prior_gate",
    )
    _prior_ledger, prior_digest = prior.audit()
    require(prior_digest == prior.EXPECTED_LEDGER_SHA256,
            "the capped-C4/block-projector gate changed")

    projector = load(
        "computations/verify_h3_centered_projector_literal_first_hasse_eq_incidence_gate.py",
        "l01_projector_face",
    )
    projector_ledger, projector_digest = projector.audit()
    require(projector_digest == projector.EXPECTED_LEDGER_SHA256,
            "the centered-projector face gate changed")
    face = projector_ledger["first_matching_Hasse_face"]
    require(face["first_PP_face_count"] == 6
            and face["target_readout"] == 0
            and face["central_Eq_input_incidence"] == 0,
            "the pinned matching first face changed")

    terminal = load(
        "computations/verify_h3_o2_augmented_terminal_cap_cartan_extension_gate.py",
        "l01_first_pp_terminal",
    )
    terminal_ledger, terminal_digest = terminal.audit()
    require(terminal_digest == terminal.EXPECTED_LEDGER_SHA256,
            "the augmented terminal gate changed")
    fork = terminal_ledger["post_placement_dichotomy"]
    require(fork["third_branch"] is False,
            "the terminal fork acquired a third branch")
    return {
        "pinned_prior_gate": prior_digest,
        "pinned_projector_gate": projector_digest,
        "matching_projector_constructs_formula_not_boundary": True,
        "known_six_term_face": (
            "one endpoint fibre, residual-tail derivatives only, target/Eq zero"
        ),
        "new_first_proper_face": (
            "the 18 endpoint/direction derivatives in dL01, with six labelled "
            "marginals 3*(2,2,-1,-1,-1,-1)"
        ),
        "source_valid_three_cap_family_constructed": False,
        "augmented_readouts_before_placement": {
            "physical_q": "undefined",
            "W": "undefined",
            "labelled_ridge": "undefined",
            "eta_sigma": "unique only after the labelled ridge",
        },
        "post_placement_alternative": fork["exact_alternative"],
        "third_branch": fork["third_branch"],
        "premature_terminalization": False,
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 L01 three-cap first-PP curvature gate",
        "pins": PINS,
        "literal_three_cap_and_first_PP": three_cap_and_first_pp_audit(),
        "physical_scope": physical_scope_audit(),
        "verdict": (
            "A single covariant capped family on the three pairings A,B,C "
            "would construct both the R01 block projector and L01.  Its first "
            "proper face is dL01 with 36 literal terms.  The 18 residual-tail "
            "terms are labelwise centered and contain the pinned six-term "
            "matching face.  The other 18 terms have the nonzero labelled "
            "endpoint/direction marginal 3*(2,2,-1,-1,-1,-1); no pinned "
            "source cell cancels it.  At the complete-response level the "
            "corresponding first-PP complement has support 384.  Physical "
            "q/W/ridge and terminal promotion remain conditional on placing "
            "this full face in the augmented relative map."
        ),
        "shortest_next_cell": (
            "an endpoint-even first-PP Spencer/cobar cell with boundary the "
            "18 direction-factor terms of dL01, simultaneously glued to the "
            "three residual-tail matching faces and the 384-term complement; "
            "it must retain word/fine/repeated, q, W and labelled-ridge data"
        ),
        "scope": (
            "exact canonical h=3 K8 occurrence and first-Kahler modules.  "
            "The checker constructs the formal three-cap combination and its "
            "literal first face, not the missing physical source cells."
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
    print("three capped pairings: R01 and L01 combinations EXACT")
    print("dL01 support: 36 = 18 tail + 18 direction")
    print("tail marginals: ZERO")
    print("direction marginals: 3*(2,2,-1,-1,-1,-1)")
    print("complete first-PP complement: 384 terms")
    print("physical three-cap/endpoint Spencer cell: STILL MISSING")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
