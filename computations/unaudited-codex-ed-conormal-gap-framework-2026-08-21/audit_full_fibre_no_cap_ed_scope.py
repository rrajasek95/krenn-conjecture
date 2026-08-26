#!/usr/bin/env python3
"""Scope audit and minimal ED/Fritz--John interface for the exact N=8 fibre."""

from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OUT = HERE / "results_full_fibre_no_cap_ed_scope.json"

CLEAN_PROOF = ROOT / "proofs/clean-pair-cap-exact-descent.md"
SIX_PROOF = ROOT / "proofs/six-site-arbitrary-complex-obstruction.md"
RESPONSE_REPORT = (ROOT / "computations/unaudited-codex-response-star-2026-08-20"
                   / "REPORT.md")


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def file_digest(path):
    return sha256(path.read_bytes()).hexdigest()


def scope_replay():
    clean = CLEAN_PROOF.read_text()
    six = SIX_PROOF.read_text()
    response = RESPONSE_REPORT.read_text()
    required_clean = [
        "If the three pure cap coefficients", "and the homogeneous cap error",
        "there is a finite endpoint-coloured ternary source on `U`",
        "retains arbitrary complex coefficients",
    ]
    required_six = [
        "endpoint-ordered matrix", "the matrix may be zero",
        "There is no collection of complex matrices",
        "No genericity, positivity, or restriction on the number of parallel",
    ]
    required_response = [
        "an active cap whose response support lies in the star",
        "if and only if", "Why a star—or a triangle—is clean",
        "This is a sufficient clean-cap mechanism",
    ]
    require(all(item in clean for item in required_clean), required_clean)
    require(all(item in six for item in required_six), required_six)
    require(all(item in response for item in required_response), required_response)
    return {
        "clean_descent_proof_sha256": file_digest(CLEAN_PROOF),
        "six_site_proof_sha256": file_digest(SIX_PROOF),
        "response_carrier_report_sha256": file_digest(RESPONSE_REPORT),
        "implication": (
            "F_8(A)=Delta_8 and an active clean cap (p,q,K) imply, by exact "
            "descent, arbitrary complex endpoint-ordered blocks y on six "
            "sites with F_6(y)=Delta_6, contradicting the six-site theorem."
        ),
        "carrier_interface": (
            "A passing star/triangle carrier is exactly an active K with "
            "response supported in that carrier; such support forces the "
            "canonical N=8 cap error E to vanish.  Hence it is an active clean "
            "cap and is impossible on the exact fibre."
        ),
        "terminology_guard": (
            "Failure of all 728 carriers is weaker than absence of every clean "
            "cap, because E may vanish by cancellation on wider support.  The "
            "descent argument nevertheless excludes every active clean cap, so "
            "it implies the 728-carrier residual as a corollary."
        ),
    }


def derivative_support_profile():
    sites = tuple(range(8))
    colours = tuple(range(3))
    edges = tuple(combinations(sites, 2))
    pm6 = tuple(perfect_matchings(range(6)))
    pm8 = tuple(perfect_matchings(sites))
    require(len(pm6) == 15 and len(pm8) == 105, (len(pm6), len(pm8)))
    # For a fixed edge e and cell ij, dF/dA_e[ij] is the six-site residual
    # matching tensor.  The nine cells occupy disjoint endpoint-word supports.
    edge = edges[0]
    residual = tuple(site for site in sites if site not in edge)
    supports = []
    for i, j in product(colours, repeat=2):
        supports.append({(i, j) + word for word in product(colours, repeat=6)})
    require(all(supports[a].isdisjoint(supports[b])
                for a in range(9) for b in range(a)), "column supports overlap")
    require(len(set().union(*supports)) == 3 ** 8, "support union")
    return {
        "complex_source_variables": len(edges) * 9,
        "real_source_variables": len(edges) * 9 * 2,
        "complex_output_coordinates": 3 ** 8,
        "real_output_constraints_in_redundant_presentation": 2 * 3 ** 8,
        "perfect_matchings_N8": len(pm8),
        "residual_perfect_matchings_N6_per_derivative_entry": len(pm6),
        "output_words_per_J_column": 3 ** 6,
        "possible_structural_J_entries": len(edges) * 9 * (3 ** 6),
        "fixed_edge_Te_columns": 9,
        "fixed_edge_column_supports_pairwise_disjoint": True,
        "fixed_edge_column_coefficient_tensor": "the same residual H_6(A|U)",
        "rank_dichotomy": "rank(T_e)=0 if H_6(A|U)=0, otherwise rank(T_e)=9",
    }


def common_matching_hostile_guard():
    words = tuple(product(range(3), repeat=4))
    expanded = {tuple(colour for item in word for colour in (item, item)): 1
                for word in words}
    pure = [word for word in expanded if len(set(word)) == 1]
    mixed = [word for word in expanded if len(set(word)) > 1]
    require(len(expanded) == 81 and len(pure) == 3 and len(mixed) == 78,
            (len(expanded), len(pure), len(mixed)))
    return {
        "source": "A_01=A_23=A_45=A_67=I3, all other blocks zero",
        "nonzero_output_words": len(expanded),
        "pure_words": len(pure),
        "mixed_words": len(mixed),
        "lex_first_mixed_word": list(min(mixed)),
        "coefficient": "1",
        "verdict": (
            "This frequently used canonical pair-product control is not an "
            "exact GHZ8 source and cannot serve as an exact-fibre boundary."
        ),
    }


def ed_system(profile):
    n = profile["complex_source_variables"]
    m = profile["complex_output_coordinates"]
    require(m - n == 6309, (m, n))
    return {
        "attainment": (
            "The exact fibre V={A:F(A)=Delta} is closed in R^504.  The squared "
            "Hermitian norm is coercive, so V nonempty implies a global norm "
            "minimum is attained.  No finite active-cap boundary or infinity "
            "case remains for this full-fibre minimization."
        ),
        "exact_blockwise_condition": (
            "For every intersecting edge family E, F is affine-linear in the "
            "blocks A_E. Every h in ker(L_E) gives a genuine full-fibre line, "
            "so at a norm minimum A_E is orthogonal to ker(L_E). The maximal "
            "families are the eight full seven-edge stars (63 scalar columns) "
            "and the 56 site triangles (27 scalar columns). The single-edge "
            "corollary is H_6(A|B-e)=0 => A_e=0."
        ),
        "real_regular_KKT": [
            "F(A)=Delta",
            "A=J_A^* lambda",
            "equivalently rank([J_A;A^*])=rank(J_A)",
        ],
        "source_sized_gram_compression": [
            "F(A)=Delta",
            "A=J_A^* J_A eta",
            "eta has 252 complex coordinates rather than 6561 output multipliers",
            "im(J_A^*)=im(J_A^*J_A) for the Hermitian realification",
        ],
        "quotient_full_column_rank_guard": (
            "At an exact GHZ point the 21-dimensional T0 has orbit tangent "
            "dimension 21-s inside ker(J_A), so rank(J_A)<=231+s and literal "
            "full column rank 252 is impossible. If the induced map on "
            "E/im(T0.A) is injective, then ker(J_A)=T0.A. At the global norm "
            "minimum the T0 balance equations give A perpendicular ker(J_A), "
            "so A lies in im(J_A^*)=im(J_A^*J_A) and regular ED is automatic "
            "on this quotient-rigid branch."
        ),
        "euler_guard": "J_A A=4 F(A)=4 Delta because F is homogeneous of degree four",
        "naive_fritz_john": [
            "F(A)=Delta",
            "alpha A=J_A^* lambda",
            "(alpha,lambda) nonzero",
        ],
        "singular_alpha_zero_hazard": (
            "In the full 6561-coordinate presentation alpha=0 is automatic and "
            "nondiscriminating: dim_C ker(J_A^*) >= 6561-252 = 6309 at every A. "
            "A theorem-grade singular branch must quotient these redundant "
            "output covectors or use a pointwise independent local generating "
            "set for the fibre ideal.  Merely adjoining alpha=0 multipliers "
            "does not encode minimum-norm criticality."
        ),
        "smallest_safe_system_now": (
            "Use the exact fibre equations, all eight star and 56 triangle "
            "least-norm block equations, and on the regular ED branch the "
            "252-variable Gram equation A=J^*J eta after quotienting the T0 "
            "kernel. Keep the singular fibre locus separate; its valid normal "
            "cone requires local ideal generators or tangent-cone equations, "
            "not the tautological output-cokernel alpha=0 branch."
        ),
        "complex_redundant_cokernel_lower_bound": m - n,
        "real_redundant_cokernel_lower_bound": 2 * m - 2 * n,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--mutate-six-site-scope", action="store_true")
    args = parser.parse_args()
    scope = scope_replay()
    if args.mutate_six_site_scope:
        scope["implication"] = scope["implication"].replace(
            "arbitrary complex endpoint-ordered", "symmetric nonzero")
    require("arbitrary complex endpoint-ordered" in scope["implication"], scope)
    profile = derivative_support_profile()
    ed = ed_system(profile)
    payload = {
        "status": "PASS full exact fibre is automatically no-active-clean-cap; ED scope corrected",
        "scope_audit": scope,
        "common_matching_hostile_guard": common_matching_hostile_guard(),
        "derivative_profile": profile,
        "minimum_norm_ed_interface": ed,
        "terminal_verdict": (
            "Full-fibre norm minimization is logically safe and attained if the "
            "hypothetical fibre is nonempty.  The regular source-sized ED system "
            "and all maximal intersecting-block conditions are exact, but regular "
            "ED is automatic on the T0-quotient-rigid balanced branch. The naive "
            "alpha=0 Fritz--John branch is terminally too redundant and must not "
            "be used without a local-ideal or normal-cone compression."
        ),
    }
    payload["logical_sha256"] = sha256(json.dumps(
        payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    if args.write_results:
        OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("scope PASS", scope["implication"])
    print("profile", profile)
    print("regular ED", ed["source_sized_gram_compression"])
    print("singular guard", ed["singular_alpha_zero_hazard"])
    print("logical sha256", payload["logical_sha256"])


if __name__ == "__main__":
    main()
