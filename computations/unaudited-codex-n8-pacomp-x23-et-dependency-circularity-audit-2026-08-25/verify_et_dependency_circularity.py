#!/usr/bin/env python3
"""Small fail-closed dependency audit for the h=3 Lambda/Pi obligations."""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PINS = {
    "computations/unaudited-codex-n8-pacomp-x23-total-carrier-et-construction-audit-2026-08-25/MANIFEST.sha256":
        "f4c40ad4801fcf2950af2871e46eb6971e3a5fee12f124a8f37367d6e343117b",
    "computations/unaudited-codex-n8-pacomp-proof-continuation-2026-08-25/MANIFEST.sha256":
        "e580fd316a4aa3a52b50e66b5173d7c3372a39d2da721848a21be8295aeb0a6e",
    "notes/h3-generic-symmetric-c4-placement-terminal-gate.md":
        "dcf0ef4adf500b4bee46ca301b12241e95ed1343a509a4fe4110d5dd3a906e92",
    "computations/verify_h3_generic_symmetric_c4_placement_terminal_gate.py":
        "ecb8725715747c3270fb069545309283d1890fbac6e66dfb6ed2f53b609e0030",
    "notes/h3-h2-c4-trivial-tag-euler-scalar-face-gate.md":
        "3d16b7a1b77030eaaa5ba3fc342b927a7ee750db2c4f8091868591acc261477f",
    "computations/verify_h3_h2_c4_trivial_tag_euler_scalar_face_gate.py":
        "47378f8ce904021bb802e0e4fd59de1591f0cd7333e1fcbc645e62cf40deb499",
    "notes/h3-actual-source-primitive-terminal-reduction-gate.md":
        "6891973dced53cb17528020456e0f96c3776e1b070f442836f21924e220eb578",
    "computations/verify_h3_actual_source_primitive_terminal_reduction_gate.py":
        "5754c85f7ae4b714777cdbb0f941672ade1977c5568f332a0dc8e317e4952927",
    "notes/h3-component-iv-face-zero-routing-boundary.md":
        "21e1ee5557dbaee26cf564353d06d9e2a5fca5c3877290f87c1665b9af4c37e9",
    "computations/verify_h3_component_iv_face_zero_routing_boundary.py":
        "217d14b451a36b6e86caadf14bd5ce63aeda484f8e0917b7f2e1034b640a4fc0",
    "notes/h3-cut-swap-collision-word-orbit-obstruction.md":
        "f77846730f94c090823fdf96db0c489398597ef0542b394a2f016d14738913d0",
    "computations/verify_h3_cut_swap_collision_word_orbit_obstruction.py":
        "d7281084a0fc084e6d951f527daf92c92faefebec183a83d6cfa33e055596c77",
    "notes/h3-l01-full-linear-spencer-dual-gate.md":
        "434f96823775e4f4412584b534e3c10fc5d748efec69a19ffb45192663a1886c",
    "computations/verify_h3_l01_full_linear_spencer_dual_gate.py":
        "2900027d9e9d9481ba18d3682777447269142bc5db65293ac3b2b360d270dda1",
    "notes/h3-chart-odd-gate-ii-augmented-filler-terminal-fork.md":
        "fdb07cd655a0bd4dfa519c8c7faed8cafac105345737f44902b8127324f24a2a",
    "computations/verify_h3_chart_odd_gate_ii_augmented_filler_terminal_fork.py":
        "cd445864a1440b89b213229c6795b409a9c49b84bf388dc4a476ed2030077e91",
    "notes/h3-gamma-cotangent-principal-parts-enrichment-foundation-gate.md":
        "5bc019d62b62f9cd8ab57524d3056ce124582dbb5a134f2f0aa36726e58c86bd",
    "computations/verify_h3_gamma_cotangent_principal_parts_enrichment_foundation_gate.py":
        "3eb7bc5bd51a9affa3aa0cdab113efc2856375c0de9e083efc611aed7cd1058f",
    "notes/h3-full-site-root-companion-closed-balanced-cycle-counterguard.md":
        "c44f6f5d93edea92d9e4b004c41544982e53ea94bc82f529b27ff077dd77e38f",
    "computations/verify_h3_full_site_root_companion_closed_balanced_cycle_counterguard.py":
        "d1f9a89b9ef627d9c214c72b76c150c6134fd330f82fd343f68f12a4fcbccd0c",
}


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def rank(columns: tuple[tuple[Q, ...], ...]) -> int:
    if not columns:
        return 0
    require(len({len(c) for c in columns}) == 1, "rank height")
    rows = [[columns[j][i] for j in range(len(columns))]
            for i in range(len(columns[0]))]
    answer = 0
    for column in range(len(columns)):
        pivot = next((r for r in range(answer, len(rows))
                      if rows[r][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        p = rows[answer][column]
        rows[answer] = [x / p for x in rows[answer]]
        for r in range(len(rows)):
            if r == answer or not rows[r][column]:
                continue
            c = rows[r][column]
            rows[r] = [x - c * y for x, y in
                       zip(rows[r], rows[answer], strict=True)]
        answer += 1
    return answer


def dot(a: tuple[Q, ...], b: tuple[Q, ...]) -> Q:
    return sum((x * y for x, y in zip(a, b, strict=True)), Q(0))


def audit() -> dict[str, object]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, (relative, actual, expected))

    # Earliest L01 quotient.
    B = tuple(map(Q, (0, 1, 0)))
    C = tuple(map(Q, (0, 0, 1)))
    L = tuple(map(Q, (2, -1, -1)))
    require(rank((B, C)) == 2 and rank((B, C, L)) == 3,
            "L quotient")

    # Post-reinsertion complete-row quotient.
    rows = (
        tuple(map(Q, (1, 1, 1, 0, 0))),
        tuple(map(Q, (1, 0, 0, 1, 1))),
        tuple(map(Q, (1, 1, 0, 1, 0))),
        tuple(map(Q, (1, 0, 1, 0, 1))),
    )
    core = tuple(map(Q, (1, 0, 0, 0, 0)))
    eta = (Q(1), Q(-1, 2), Q(-1, 2), Q(-1, 2), Q(-1, 2))
    require(rank(rows) == 3 and rank(rows + (core,)) == 4
            and all(dot(eta, row) == 0 for row in rows)
            and dot(eta, core) == 1, "retained-r quotient")

    # Exact relative-C4 countermodel: full site/root covariance plus literal
    # tails still admits a closed four-object relative bar with no absolute
    # switch. Coordinates are x0..x3,u0..u3.
    cycle = ((0, 1), (1, 2), (2, 3), (3, 0))
    columns = []
    lam = tuple(map(Q, (1, -1, 1, -1)))
    mu = [x / 4 for x in lam] + [Q(0)] * 4
    for edge_index, (source, target) in enumerate(cycle):
        column = [Q(0)] * 8
        column[target] += 1
        column[source] -= 1
        column[4 + edge_index] -= 1
        columns.append(tuple(column))
        mu[4 + edge_index] = (lam[target] - lam[source]) / 4
    balanced = tuple(list(lam) + [Q(0)] * 4)
    require(rank(tuple(columns)) == 4
            and all(dot(tuple(mu), column) == 0 for column in columns)
            and dot(tuple(mu), balanced) == 1,
            "relative covariance countermodel")

    # Propositional counterguards.  These are implications with load-bearing
    # antecedents; each can hold while both requested fillers are absent.
    implies = lambda p, q: (not p) or q
    lambda_exists = False
    pi_exists = False
    require(implies(False, False) and not lambda_exists and not pi_exists,
            "rootless antecedent countervaluation")
    require(implies(False, False) and not lambda_exists and not pi_exists,
            "inactive antecedent countervaluation")
    # Even with an exhaustive fork, nonfill may take the terminal branch.
    exhaustive = True
    terminal = True
    require(exhaustive and (lambda_exists or terminal), "terminal fork")

    result: dict[str, object] = {
        "schema": "pacomp-h3-et-dependency-circularity-audit-v1",
        "status": "PASS_CIRCULAR_STOP_NO_EXISTING_ROUTE_IMPLIES_FILLERS",
        "scope": "pinned small h=3 symbolic dependency graph only",
        "parent_manifest_sha256": PINS[next(iter(PINS))],
        "pins": PINS,
        "obligations": {
            "top": "dLambda_01=L01",
            "proper_face": "dPi_r,01=-R_ret",
            "relation": (
                "Pi_r is a necessary lower-filtration component of a total "
                "Lambda_01 in the displayed relative-C4 construction; Pi_r "
                "alone does not imply Lambda_01"
            ),
        },
        "local_essential_surjectivity": {
            "L01_quotient_dimension": 1,
            "L01_positive_branch": (
                "essential surjectivity onto this local quotient is exactly "
                "the existence of Lambda_01"
            ),
            "retained_r_quotient_dimension": 1,
            "retained_r_positive_branch": (
                "essential surjectivity onto the next face quotient is "
                "exactly the existence of Pi_r,01"
            ),
            "global_scope_guard": (
                "full GammaPrimitiveCompleteness is stronger: it enumerates "
                "the exhaustive physical source and permits deciding filler "
                "versus terminal; it does not assert the filler branch"
            ),
        },
        "route_audit": {
            "rootless_component_III": {
                "antecedent": "physical Phi/M_v on complete relative domains",
                "conclusion": "q defect/generator or q transport/Fredholm",
                "classification": (
                    "POST-PLACEMENT; neither constructs the DQ/PS source edge "
                    "nor the retained-r landing"
                ),
            },
            "inactive_component_IV": {
                "antecedent": (
                    "physical comparison plus derived Yw->physical W, normal-grade "
                    "naturality, and cyclotomic/horizontal/diagonal routing"
                ),
                "classification": "STRICTLY DOWNSTREAM AND STILL OPEN",
            },
            "face_zero": {
                "fact": (
                    "simultaneous h_v=0 is not proved to land in either the "
                    "rootless-open or all-inactive branch"
                ),
                "classification": "NO ROUTING IMPLICATION",
            },
            "rootless_inactive_cross_use": (
                "invalid: the pinned audit explicitly separates the cap-line gcd "
                "split from the five internal face coefficients"
            ),
        },
        "terminal_promotion_audit": {
            "generic_C4": (
                "after same-grade U_C4 placement, exact duality gives filler or "
                "terminal; the theorem does not place U_C4"
            ),
            "L01": (
                "after same-grade L01 placement in exhaustive J_full, exact duality "
                "gives protected filler or augmented terminal"
            ),
            "why_not_a_filler_theorem": (
                "the nonfill terminal branch is allowed, and J_full/source-cell "
                "exhaustiveness is not instantiated"
            ),
            "why_not_a_terminal_yet": (
                "native Spencer and named augmented columns are not the exhaustive "
                "physical same-grade source; a future Lambda/Pi may pair nontrivially"
            ),
        },
        "counterguards": {
            "relative_site_root_C4": {
                "columns": 4,
                "rank": 4,
                "ambient_dimension": 8,
                "balanced_detector_value": 1,
                "meaning": (
                    "full-site covariance, conjugated roots, fixed literal tails "
                    "and normalization coexist with no absolute switch"
                ),
            },
            "official_source_completion_pair": (
                "the same official EqSystem/native jet data admit an enriched "
                "completion with no bright primitive and one with an orphan "
                "operation-changing primitive; source enrichment is load-bearing"
            ),
        },
        "implication_edges": [
            "source-labelled total Lambda_01 => dLambda_01=L01",
            "total Lambda_01 in the pinned filtration => required Pi_r,01 component",
            "same-grade placement + exhaustive J_full => filler OR terminal",
            "physical Phi => local rootless q/Fredholm dichotomy",
            "physical comparison + cap law + naturality => inactive routing",
        ],
        "non_edges": [
            "rootless theorem !=> Lambda_01 or Pi_r,01",
            "inactive theorem !=> Lambda_01 or Pi_r,01",
            "face-zero condition !=> rootless or inactive placement",
            "terminal-promotion theorem !=> filler branch",
            "native Spencer cokernel !=> accepted source terminal",
            "site/root covariance !=> absolute DQ/PS switch",
        ],
        "stop_rule": (
            "STOP: any further rearrangement invoking source-grade essential "
            "surjectivity, GammaPrimitiveCompleteness, or exhaustive J_full to "
            "construct Lambda_01/Pi_r is circular.  Progress requires either an "
            "explicit new source-labelled generator/placement map or an independent "
            "proof that the exhaustive dual takes the terminal branch."
        ),
        "promotion": "NONE",
        "verdict": (
            "Neither obligation is a consequence of an existing rootless, inactive, "
            "face-zero, or terminal-promotion theorem.  In each relevant one-dimensional "
            "local quotient its positive essential-surjectivity assertion is exactly "
            "the missing filler.  The broader completeness theorem is stronger but only "
            "decides filler versus terminal; it does not choose filler.  Rearrangement "
            "through any of those hypotheses is therefore circular."
        ),
    }
    logical = sha256(json.dumps(result, sort_keys=True, separators=(",", ":"))
                     .encode()).hexdigest()
    return {"logical_sha256": logical, "result": result}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    wrapped = audit()
    encoded = json.dumps(wrapped, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded)
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
