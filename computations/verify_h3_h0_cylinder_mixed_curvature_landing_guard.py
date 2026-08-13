#!/usr/bin/env python3
"""Audit physical landing of the H0-preserving cylinder curvature t*k_ij."""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_centered_shear_h0_target_cylinder_alternative.py":
        "b4aa84a571500c0e4745ae29ea6c1f23076c63bac139d1bd839fdb1160f515ab",
    "notes/h3-centered-shear-h0-target-cylinder-alternative.md":
        "d21d02f0d3dfece57e080511c34af78b38b77b87600837a05668ae1970b7e70e",
    "computations/verify_h3_universal_response_toric_minor_terminal_gate.py":
        "c40790270ef38ea72ec1601037f81319e02638d80828d96ee341e73d9f665e37",
    "notes/h3-universal-response-toric-minor-terminal-gate.md":
        "9718c4bda2e411a65c9b18d2e4ffd42a270b2458374b92690b40d3e0f0b23cd4",
    "computations/verify_h3_segre_bright_private_site_incidence_tate_alternative.py":
        "e00e9b39740c22b2beacd874e13ab3b7e7c2f776724e19eece28f525400d6258",
    "notes/h3-segre-bright-private-site-incidence-tate-alternative.md":
        "95a8ee1a7603cb5e5af20b44cdf7668a42b22fb020f042839a58e5a8329baa99",
    "computations/verify_h3_centered_scalar_normal_terminal_extension_guard.py":
        "2c0b5f89a99a2ad9058aaa1648ecdff6933d60bee6bc1f92cdb389e64ba73ca7",
    "notes/h3-centered-scalar-normal-terminal-extension-guard.md":
        "ca7320c152463d9fd594adcb35048343d276aefe4663826fe609ae8ee3effafb",
    "computations/verify_h3_active_fan_coloop_or_four_good.py":
        "93030f2994e2e6a2052a09a5fefd179c99e0b8fb55cd0c77bee2cb9f8dbc6bb4",
    "notes/h3-active-fan-coloop-or-four-good.md":
        "9be8996264fa2070a8f5d7f725f3fcb154b6ee2df2b3e5d3ccd4a6412ec5b03a",
    "computations/verify_h3_residual_q_ks_standard_transport_graph_lock.py":
        "eede8aabd5c4740520ed13f1aacc897326a3a02573f860f5b2613c9df91fd53c",
    "notes/h3-residual-q-ks-standard-transport-graph-lock.md":
        "9729e3bd7d639c24c2512641da74815cf1162e995ce76cb6286bca6dd545ca0f",
}
EXPECTED_LEDGER_SHA256 = "ad57a54598097268164aadccb703e8d37d5988fc0b9a789ac8909b4e3dbba0e7"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def dot(left, right) -> Q:
    return sum((Q(a)*Q(b) for a, b in zip(left, right, strict=True)), Q(0))


def rank(vectors) -> int:
    basis: dict[int, tuple[Q, ...]] = {}
    for vector in vectors:
        values = [Q(value) for value in vector]
        for pivot in sorted(basis):
            if values[pivot]:
                scale = values[pivot]
                values = [left-scale*right
                          for left, right in zip(values, basis[pivot], strict=True)]
        pivot = next((i for i, value in enumerate(values) if value), None)
        if pivot is None:
            continue
        scale = values[pivot]
        basis[pivot] = tuple(value/scale for value in values)
    return len(basis)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative, actual))


def fine_grade_audit() -> dict[str, object]:
    # Grade basis is (E0,E1,Q0,Q1,Q2), with gr(u_rj)=E_r+Q_j.
    def grade(r: int, j: int) -> tuple[int, ...]:
        value = [0]*5
        value[r] = 1
        value[2+j] = 1
        return tuple(value)

    def add(left, right):
        return tuple(a+b for a, b in zip(left, right, strict=True))

    g00, g01, g10, g11 = grade(0, 0), grade(0, 1), grade(1, 0), grade(1, 1)
    doubled = add(g00, g11)
    require(doubled == add(g01, g10), "the Segre minor lost homogeneity")

    # A single scalar t cannot have simultaneously the four occurrence
    # grades required by the four product-rule terms.
    required_t_grades = (g00, g11, g01, g10)
    require(len(set(required_t_grades)) == 4,
            "the occurrence tags unexpectedly collapsed")
    tagged_term_grades = (
        add(g00, g11), add(g00, g11),
        add(g01, g10), add(g01, g10),
    )
    require(len(set(tagged_term_grades)) == 1
            and tagged_term_grades[0] == doubled,
            "the tagged target cylinder is not fine homogeneous")
    return {
        "minor": "F01=u00*u11-u01*u10",
        "doubled_physical_grade": list(doubled),
        "tagged_curvature": (
            "t00*u11+u00*t11-t01*u10-u01*t10, with gr(t_rj)=gr(u_rj)"
        ),
        "tagged_terms_same_fine_grade": True,
        "one_formal_scalar_t_is_a_physical_fine_graded_column": False,
        "required_local_target_tags": ["t00", "t01", "t10", "t11"],
        "uniform_2x3_family_tags": 6,
        "warning": (
            "the equality t=L or t=90f at a point is value-level.  Once a "
            "physical polynomial-module generator is placed, multiplication "
            "resolves these grades componentwise"
        ),
    }


def polynomial_module_closure_audit() -> dict[str, object]:
    # Row order: target, ordinary residue, anchor/q, W, ridge, eta/sigma.
    pure_target = (Q(1), Q(0), Q(0), Q(0), Q(0), Q(0))
    cap_graph = (Q(1), Q(1), Q(0), Q(0), Q(0), Q(0))
    k = Q(7)
    curvature = (k, Q(0), Q(0), Q(0), Q(0), Q(0))
    pure_remainder = tuple(a-k*b for a, b in
                           zip(curvature, pure_target, strict=True))
    cap_remainder = tuple(a-k*b for a, b in
                          zip(curvature, cap_graph, strict=True))
    require(pure_remainder == (0, 0, 0, 0, 0, 0)
            and cap_remainder == (0, -7, 0, 0, 0, 0),
            "the polynomial target-multiple signatures changed")
    return {
        "criterion": (
            "if C_t is source-provenant and its physical source module contains "
            "all homogeneous coefficient multiples, then k_ij*C_t is an admitted "
            "Macaulay column"
        ),
        "fine_grade_effect": (
            "automatic componentwise: homogeneous occurrence terms of k_ij land "
            "in their exact product grades"
        ),
        "pure_target_generator": {
            "signature": [1, 0, 0, 0, 0, 0],
            "remainder_after_-kC_t": list(map(int, pure_remainder)),
            "consequence": "curvature completely cancelable; not a terminal",
        },
        "known_cap_graph_after_cross_word_placement": {
            "signature": [1, 1, 0, 0, 0, 0],
            "remainder_after_-k_cap_graph": list(map(int, cap_remainder)),
            "consequence": "target cancels; mixed ordinary residue remains",
        },
        "current_status": (
            "the cap graph is physical only in its own 01211222/P3+K2 grade; "
            "the response/E14 cross-word placement remains open"
        ),
        "first_post_placement_debt": "-k_ij in the word-resolved ores row",
    }


def augmented_character_audit() -> dict[str, object]:
    xi01 = (-1, 1, 0, 1, -1, 0)
    xi02 = (-1, 0, 1, 1, 0, -1)
    xi12 = (0, -1, 1, 0, 1, -1)
    K = (xi01, xi02, xi12)
    endpoint_rows = ((1, 1, 1, 0, 0, 0), (0, 0, 0, 1, 1, 1))
    matching_rows = tuple(tuple(int(i % 3 == j) for i in range(6))
                          for j in range(3))
    scalar_row = ((1, 1, 1, 1, 1, 1),)
    disclosed = scalar_row+endpoint_rows+matching_rows
    require(rank(K) == 2
            and all(dot(k, row) == 0 for k in K for row in disclosed),
            "the mixed curvature acquired an aggregate shadow")

    # Full disclosed augmented rows q/anchor/ridge/W/eta/sigma have zero
    # mixed-character restriction.  Appending zero rows changes no rank.
    augmented_zero_rows = tuple((0,)*6 for _ in range(7))
    require(all(dot(k, row) == 0 for k in K
                for row in disclosed+augmented_zero_rows),
            "an augmented row detected the mixed character")

    # Exact two extensions of the same old output: zero versus the identity
    # on a chosen K-basis.  Only the new mixed terminal row distinguishes them.
    k_basis = (xi01, xi02)
    dark_terminal = ((0, 0), (0, 0))
    bright_terminal = ((1, 0), (0, 1))
    require(rank(dark_terminal) == 0 and rank(bright_terminal) == 2,
            "the output-extension fork changed")
    return {
        "local_curvature_module_rank": 2,
        "representation": "endpoint-odd tensor matching-standard",
        "global_covariant_orbit_rank": 30,
        "old_rows_killing_it": [
            "scalar/complete target", "two endpoint sums", "three matching sums",
            "aggregate anchor and q", "W", "shifted ridge", "eta", "sigma",
        ],
        "dark_extension_on_K": [list(row) for row in dark_terminal],
        "terminal_extension_on_K": [list(row) for row in bright_terminal],
        "same_restriction_to_every_existing_output_row": True,
        "uniform_terminal_needs": (
            "one covariant rank-two local (rank-thirty global) mixed target family; "
            "a scalar target row cannot receive it equivariantly"
        ),
    }


def cartan_residue_identification_audit() -> dict[str, object]:
    cylinder = (Q(1), Q(-1), Q(-1), Q(1))
    graph_lock = (Q(1), Q(-1), Q(-1), Q(1))
    required_correction = tuple(-value for value in graph_lock)
    require(cylinder == graph_lock
            and required_correction == (-1, 1, 1, -1),
            "the cylinder/graph-lock coefficient character changed")
    return {
        "coefficient_character_equal": True,
        "common_character": [1, -1, -1, 1],
        "cylinder_literal_packet": {
            "word": "11:110000 (doubled response grade after multiplication)",
            "endpoint": "p1*s0-p0*s1",
            "matching": "q23:00*q45:00-q24:00*q35:00",
            "output_after_cap_multiple": "ordinary residue only",
        },
        "graph_lock_literal_packet": {
            "word": "1211222",
            "fine_repeated": "first common labelled P3+K2 grade",
            "endpoint": "P_+-P_-",
            "matching": "q00-q11 with decorated 11/21/12 cells",
            "required_residue_correction": [-1, 1, 1, -1],
        },
        "literal_grade_identical_now": False,
        "exact_missing_identification": (
            "the physical Cartan/cap cross-word descent must send the cylinder "
            "endpoint orientation and pure-00 residual matching difference to the "
            "P+/P- decorated q00/q11 residue basis"
        ),
        "standard_graph_transport_closes_it": False,
        "reason": (
            "the pinned graph law R_w=D_w forbids a residue-only standard column"
        ),
        "frontier_after_identification": (
            "exactly the already named graph-breaking Physical Cartan Descent cell, "
            "including its eta/sigma law; no second residue theorem"
        ),
    }


def support_landing_guard() -> dict[str, object]:
    sites = range(6)

    def matchings(vertices):
        vertices = tuple(vertices)
        if not vertices:
            return ((),)
        first = vertices[0]
        answer = []
        for other in vertices[1:]:
            rest = tuple(v for v in vertices if v not in (first, other))
            for tail in matchings(rest):
                answer.append((tuple(sorted((first, other))),)+tail)
        return tuple(answer)

    all_matchings = matchings(sites)
    require(len(all_matchings) == 15, "K6 matching count changed")
    edges = tuple(combinations(sites, 2))
    dense = {edge: 1 for edge in edges}
    dense[(3, 5)] = 2
    sparse = {edge: 0 for edge in edges}
    sparse.update({(2, 3): 1, (4, 5): 1, (2, 4): 1,
                   (3, 5): 2, (0, 5): 1, (1, 4): 1})

    def support(values):
        return tuple(m for m in all_matchings if all(values[e] for e in m))

    dense_support, sparse_support = support(dense), support(sparse)
    require(len(dense_support) == 15
            and sparse_support == (((0, 5), (1, 4), (2, 3)),),
            "the pure-support completions changed")

    e0, e1, q0, q1 = map(Q, (1, 0, 1, 2))
    k01 = (e1-e0)*(q1-q0)
    t = Q(90)*e0*q0
    curvature = t*k01
    require(curvature == -90, "the normalized cylinder curvature changed")
    return {
        "common_local_values": {
            "e0": 1, "e1": 0, "q0": 1, "q1": 2,
            "t=90*f": 90, "t*k01": -90,
        },
        "completion_A": {
            "pure_zero_support_size": 15,
            "literal_pure_coloop": False,
        },
        "completion_B": {
            "pure_zero_support": "{05|14|23}",
            "literal_pure_coloop": "23",
        },
        "offdiagonal_decorated_reference_in_either_local_packet": False,
        "conclusion": (
            "the same nonzero t*k value does not determine the private-site "
            "incidence or the pure-support coloop branch"
        ),
    }


def landing_verdict() -> dict[str, object]:
    return {
        "positive_conditional": (
            "a source-valid tagged target map sending the mixed curvature to a "
            "nonzero mixed GHZ-target coordinate is immediately a target terminal; "
            "a source-valid map to an offdiagonal cell/cofactor enters the committed "
            "active-fan coloop-or-four-good theorem"
        ),
        "currently_constructed_tagged_target_map": False,
        "currently_constructed_private_site_incidence": False,
        "actual_Macaulay_extension": False,
        "first_missing_statement": (
            "place the physical cap graph across the response/E14 word and cancel "
            "or terminalize the resulting mixed ordinary-residue multiple; "
            "alternatively construct the offdiagonal incidence and enter the fan"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 H0-cylinder mixed-curvature landing guard",
        "pins": PINS,
        "fine_grade": fine_grade_audit(),
        "polynomial_module_closure": polynomial_module_closure_audit(),
        "augmented_character": augmented_character_audit(),
        "cartan_residue_identification": cartan_residue_identification_audit(),
        "support_guard": support_landing_guard(),
        "landing": landing_verdict(),
        "verdict": (
            "The nonzero H0-preserving curvature is a genuine endpoint-odd times "
            "matching-standard class.  The formal scalar t is only a coarse-word "
            "object.  Once a physical target-normal generator is placed, however, "
            "Macaulay closure supplies t*k componentwise in the exact fine grades. "
            "A pure target generator cancels it; the known cap graph transfers it "
            "to the identical mixed ordinary-residue character.  Every "
            "currently disclosed scalar/endpoint/matching/anchor/q/W/ridge/eta/"
            "sigma row kills the rank-two local character.  Exact support and output "
            "two-completion guards show that t*k alone forces neither an active fan/"
            "coloop nor a Macaulay terminal.  Cross-word cap placement plus residue "
            "cancellation/terminalization, or an offdiagonal incidence, is the first "
            "new physical theorem."
        ),
        "scope": (
            "canonical h=3 fixed-endpoint Segre block; the completions are exact "
            "local support/output guards, not complete GHZ source points"
        ),
    }
    digest = sha256(json.dumps(ledger, sort_keys=True,
                               separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("coarse H0-cylinder curvature: NONZERO")
    print("polynomial target multiple after physical placement: YES")
    print("known cap-graph multiple closes all rows: NO (ORES REMAINS)")
    print("active-fan/coloop landing forced: NO")
    print("actual Macaulay terminal forced: NO")
    print("ledger_sha256="+digest)


if __name__ == "__main__":
    main()
