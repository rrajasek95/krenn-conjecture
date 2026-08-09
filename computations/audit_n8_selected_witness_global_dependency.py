#!/usr/bin/env python3
"""Global dependency audit for the N=8 selected-witness reduction.

This is deliberately a theorem-graph checker, not another source search.  It
pins the exact checkers which close r<=3, the r=4 matching branch, and the
shared-reciprocal low-rank/flat branches.  It then audits the r=0,...,12
decision table and tests the load-bearing promotion from the uniform nonflat
shared-star theorem to a *doubly-good* curved overlap.

The promotion is not currently justified.  Lemma E first makes every
off-diagonal reciprocal unit automatically doubly good.  A literal committed
r=5 shared-endpoint counterguard then has distinct outer colours, independent
shared factors, a nonflat canonical transition, and full-span pair-deletion
budgets 17 and 18, but deleted-star ranks (2,3,3,3); its deficient arm is
diagonal.  It satisfies the selected-witness, endpoint-incidence, and E2
row-shape data, though not the exact GHZ equations or Lemma E's E3 purity.
Thus the only uncovered exact invariant packet is the shared-reciprocal,
nonflat, full-span packet with a diagonal rank-two essential arm and its
forced pure complementary tensor.
"""

from __future__ import annotations

from hashlib import sha256
import importlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "computations"
sys.path.insert(0, str(HERE))


PINS = {
    "computations/verify_n8_rankone_good_curvature_selection.py":
        "f66f3acf359ee24fe96b7bb61c91f5d75f3c76d14075cb818bd8562bc72547ac",
    "computations/verify_n8_oriented_rankone_fullnine_frontier.py":
        "88bb1e8b075f5b8906c80b1b841cdaa0936cff01c20f3449e59dc35afef4e42a",
    "computations/verify_n8_r3_reciprocal_response_obstruction.py":
        "b39419e850e5ff90877921d4c739541fd313506c613e64767ba2c16d23471a38",
    "computations/verify_exact_source_live_split_forcing.py":
        "25e52f3d6dd85a4952cd73fea026c08e19c160f22fff9c993dad39d9ac009ac0",
    "notes/exact-source-live-split-forcing.md":
        "970fda124bf702493205476942d36a3c321502846803f21590a394bbb33cdfc9",
    "computations/verify_n8_rge4_reciprocal_classification.py":
        "55e3c94cbce928b39bb2f41885266549dd5d897ba5493dded520ee13595624e0",
    "computations/verify_n8_r4_flat_good_graph_reduction.py":
        "bd6f513576c5e760232e3af2994db05302cf5f39ac22a9177ed07099947ad867",
    "computations/verify_n8_r4_4k2_three_pure_support_rup.py":
        "b93c9dea6e851a78271c0abd894e4fb272ae965abe87047f9594287221bccff7",
    # This dependency was the pending lower-r4 theorem when this audit was
    # written.  Its own normal checker independently replays all eight frozen
    # proofs; this meta-checker additionally verifies their pinned payloads.
    "computations/verify_n8_r4_lower_matching_three_pure_rup.py":
        "d325559f4bc8ea4b3089ffd28a9b2e848aa1242efdf9c604929cf3e8b4a7c061",
    "computations/verify_shared_reciprocal_fourcover_overlap.py":
        "03c70295b5c72393dda96de0987d88978de768110d0484955e90d983bd1d6851",
    "computations/verify_shared_reciprocal_lowrank_pure_support_closure.py":
        "efb5a88b3571698ef89cd0129e1923940aed5623403e8f23d65db883fcce6c8e",
    "computations/verify_shared_reciprocal_fullspan_budget_frontier.py":
        "f555435b7f6ae19d4023ef1b98bc5753dbe2b475576c2b9c675f23f139a8cdcc",
    "computations/verify_shared_reciprocal_budget13_projective_compatibility.py":
        "ba90af66ea140af93af5ec3e2fc04cbeaffc6c7c2cdc1226fa132e2afdc1ff14",
    "computations/verify_shared_reciprocal_flat_bicase_unit.py":
        "ea7ca9b3de2bc2e7d71d45cfba35fb62d77309819d9b6a910307b91061dd7a18",
}

EXPECTED_DIGEST = "089ad3e94d8bfc4dacbafbb7ebd72074e9b16531b52a70abf06fed2e716bd99c"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies():
    actual = {}
    for relative, expected in PINS.items():
        require(expected != "TO_BE_FILLED_AFTER_COMMIT",
                "the pending lower-r4 theorem has not been pinned")
        digest = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(digest == expected, f"dependency drift: {relative}")
        actual[relative] = digest
    return actual


def load_dependencies():
    names = {
        "oriented": "verify_n8_oriented_rankone_fullnine_frontier",
        "r3": "verify_n8_r3_reciprocal_response_obstruction",
        "rge4": "verify_n8_rge4_reciprocal_classification",
        "r4flat": "verify_n8_r4_flat_good_graph_reduction",
        "r4lower": "verify_n8_r4_lower_matching_three_pure_rup",
        "fullspan": "verify_shared_reciprocal_fullspan_budget_frontier",
        "flatunit": "verify_shared_reciprocal_flat_bicase_unit",
    }
    return {key: importlib.import_module(value) for key, value in names.items()}


def audit_closed_strata(modules):
    oriented = modules["oriented"]
    survivors = oriented.reciprocal_flat_census()
    require(not survivors[0] and not survivors[1] and not survivors[2],
            "an all-flat r<=2 selected-good graph survived")
    require(len(survivors[3]) == 2,
            "the r=3 incidence frontier changed")

    r3 = modules["r3"]
    r3.audit_dependencies()
    normalized, disjoint, overlap_census = r3.audit_overlap_strata()
    zero_terms, _pure_ledger = r3.audit_disjoint_pure_rows(normalized, disjoint)
    require(len(disjoint) == 6 and zero_terms == 54,
            "the exact r=3 response closure changed")

    rge4 = modules["rge4"]
    require(rge4.reciprocal_graph_dichotomy() == 105,
            "the r=4 matching/shared split changed")

    _minimum, r4_survivors, _guards = modules["r4flat"].audit()
    shapes = {row[0] for row in r4_survivors}
    expected_shapes = {
        (("P", 1), ("P", 1), ("P", 1), ("P", 1), ("P", 2), ("P", 2)),
        (("P", 1), ("P", 1), ("P", 2), ("P", 2), ("P", 2)),
        (("P", 2), ("P", 2), ("P", 2), ("P", 2)),
    }
    require(shapes == expected_shapes,
            "the all-flat r=4 matching-component frontier changed")

    lower = modules["r4lower"]
    require(lower.EXPECTED and lower.EXPECTED_LEDGER_SHA256,
            "the lower-r4 proof ledger is not frozen")
    require(len(lower.CERTIFICATE_CASES) == 8,
            "the lower-r4 proof case count changed")
    lower_payloads = {}
    for case in lower.CERTIFICATE_CASES:
        key = lower.certificate_key(*case)
        metadata = lower.EXPECTED[key]
        path = lower.CERTIFICATE_PATHS[case]
        require(path.is_file(), f"missing lower-r4 proof payload: {path}")
        actual = sha256(path.read_bytes()).hexdigest()
        require(actual == metadata["gzip_sha256"],
                f"lower-r4 proof payload drift: {key}")
        lower_payloads[key] = actual

    return {
        "r0_r2_all_flat_survivors": [len(survivors[r]) for r in range(3)],
        "r3_incidence_shapes": len(survivors[3]),
        "r3_disjoint_assignments": len(disjoint),
        "r3_forced_zero_pure_terms": zero_terms,
        "r4_labelled_reciprocal_matchings": 105,
        "r4_all_flat_matching_shapes": sorted(repr(shape) for shape in shapes),
        "r4_lower_frozen_proofs": lower_payloads,
    }


def endpoint_deletion_rank(axes, endpoint, removed_neighbor):
    return len({
        axes[endpoint][neighbor]
        for neighbor in range(8)
        if neighbor not in (endpoint, removed_neighbor)
    })


def pair_chart_profile(axes, removed_pair):
    residual = tuple(site for site in range(8) if site not in removed_pair)
    dimensions = tuple(
        len({axes[site][other] for other in residual if other != site})
        for site in residual
    )
    return residual, dimensions, sum(dimensions)


def audit_goodness_gap(modules):
    rge4 = modules["rge4"]
    out, selected_axes = rge4.MODELS["r5_shared"]
    axes = rge4.complete_counterguard_axes(out, selected_axes)
    rge4.audit_counterguard("r5_shared", out, selected_axes)

    p, q, r = 2, 1, 4
    mutual = {
        rge4.edge(tail, head)
        for tail, heads in out.items() for head in heads
        if tail in out[head]
    }
    require(rge4.edge(p, q) in mutual and rge4.edge(p, r) in mutual,
            "the selected counterguard lost its shared reciprocal arms")

    outer_colours = (axes[q][p], axes[r][p])
    shared_factors = (axes[p][q], axes[p][r])
    require(outer_colours[0] != outer_colours[1],
            "the reciprocal arms lost distinct outgoing colours")
    require(shared_factors[0] != shared_factors[1],
            "the counterguard left the independent shared-factor case")

    ranks = tuple(
        endpoint_deletion_rank(axes, endpoint, removed)
        for endpoint, removed in ((p, q), (q, p), (p, r), (r, p))
    )
    require(ranks == (2, 3, 3, 3),
            f"the direct-arm goodness counterguard changed: {ranks}")

    first = pair_chart_profile(axes, (p, q))
    second = pair_chart_profile(axes, (p, r))
    require(first[1] == (3, 2, 3, 3, 3, 3) and first[2] == 17,
            f"the pq full-span profile changed: {first}")
    require(second[1] == (3, 3, 3, 3, 3, 3) and second[2] == 18,
            f"the pr full-span profile changed: {second}")
    require(3 in first[1] and 3 in second[1],
            "a pair-deletion chart lost its residual full-span site")

    # For independent shared factors, the exact flat-star classification
    # forces both restricted outer stars to vanish.  Every physical block in
    # this committed counterguard is nonzero, so each restricted star has a
    # nonzero entry and the canonical transition is nonflat.  This uses the
    # same bicase tested by f14fa11, without claiming the counterguard is an
    # exact GHZ source.
    common = tuple(site for site in range(8) if site not in (p, q, r))
    restricted_q = tuple(axes[q][site] for site in common)
    restricted_r = tuple(axes[r][site] for site in common)
    require(restricted_q and restricted_r,
            "the independent-case restricted stars vanished")

    fullspan = modules["fullspan"]
    require(fullspan.EXPECTED_LEDGER_SHA256 ==
            "0be34806754fdb6f63a777f9cc57da25984a40489c8156166dcdb2228394a54c",
            "the budget frontier ledger changed")
    flatunit = modules["flatunit"]
    require(flatunit.EXPECTED_LEDGER_SHA256 ==
            "f35f3089eec64c65ccef345ce6b434f79699612257094affad9dcfaf03dcfef6",
            "the uniform flat-unit ledger changed")

    # Lemma E sharpens the exact-source gap.  If a reciprocal coordinate
    # unit E_{b,a} is essential at either endpoint, (E2) says its sole live
    # row must be lambda*e_k with nonzero diagonal (k,k).  Since the unit has
    # only cell (b,a), this is possible exactly when a=b=k.  Thus every
    # off-diagonal reciprocal unit is automatically doubly good.  The chosen
    # structural counterguard uses a diagonal bad arm, so it survives this
    # row-shape necessary condition (but, being non-exact, need not satisfy
    # Lemma E's pure deletion conclusion (E3)).
    lemma_e_admissible = []
    for b in range(3):
        for a in range(3):
            essential_colours = tuple(
                k for k in range(3) if (b, a) == (k, k)
            )
            lemma_e_admissible.append((b, a, essential_colours))
    require(sum(bool(row[2]) for row in lemma_e_admissible) == 3,
            "Lemma-E coordinate-unit diagonal census changed")
    require(all(not colours for b, a, colours in lemma_e_admissible if a != b),
            "an off-diagonal reciprocal unit acquired an essential colour")
    require(axes[p][q] == axes[q][p] and ranks[0] == 2,
            "the counterguard no longer places its defect on a diagonal arm")

    return {
        "representative": "r5_shared",
        "shared_endpoint": p,
        "outer_endpoints": [q, r],
        "outer_colours": list(outer_colours),
        "shared_factors": list(shared_factors),
        "canonical_transition": "nonflat_by_independent_factor_bicase",
        "deleted_endpoint_ranks_pq_pr": list(ranks),
        "pq_chart": {"residual": list(first[0]),
                     "dimensions": list(first[1]), "budget": first[2]},
        "pr_chart": {"residual": list(second[0]),
                     "dimensions": list(second[1]), "budget": second[2]},
        "exact_source": False,
        "lemma_e_coordinate_unit_census": [
            [b, a, list(colours)] for b, a, colours in lemma_e_admissible
        ],
        "exact_gap_sharpening": (
            "a deficient reciprocal arm must be diagonal E_kk and Lemma E "
            "also forces the complementary six-site hafnian to be a nonzero "
            "pure colour-k tensor"
        ),
        "purpose": (
            "structural counterguard: residual full-span and nonflatness do "
            "not imply four deleted-star ranks equal three"
        ),
    }


def decision_table():
    rows = []
    for reciprocal_count in range(13):
        if reciprocal_count <= 2:
            branch = "curved_doubly_good_or_all_flat_count_contradiction"
            status = "closed_to_desired_alternative"
        elif reciprocal_count == 3:
            branch = "curved_doubly_good_or_sharp_response_contradiction"
            status = "closed_to_desired_alternative"
        elif reciprocal_count == 4:
            branch = (
                "matching: curved_doubly_good_or_three_pure_contradiction; "
                "shared: nonflat_but_goodness_unproved"
            )
            status = "open_shared_endpoint_packet"
        else:
            branch = (
                "shared_endpoint: low_rank_contradictory; full_span_and_"
                "nonflat; goodness_unproved"
            )
            status = "open_shared_endpoint_packet"
        rows.append({"r": reciprocal_count, "branch": branch, "status": status})
    require([row["r"] for row in rows] == list(range(13)),
            "the reciprocal-count decision table is incomplete")
    require(sum(row["status"] == "closed_to_desired_alternative"
                for row in rows) == 4,
            "the closed reciprocal-count prefix changed")
    return rows


def main():
    pins = pin_dependencies()
    modules = load_dependencies()
    closed = audit_closed_strata(modules)
    gap = audit_goodness_gap(modules)
    table = decision_table()
    ledger = {
        "dependencies": pins,
        "closed_strata": closed,
        "decision_table": table,
        "goodness_counterguard": gap,
        "verdict": {
            "complete_n8_selected_witness_theorem": False,
            "single_uncovered_packet": (
                "shared reciprocal coordinate arms with distinct outer "
                "colours, a nonflat canonical transition, residual full-span "
                "charts, and at least one diagonal E_kk arm with a rank-two "
                "deleted endpoint star and Lemma-E pure complementary tensor"
            ),
            "missing_implication": (
                "exactness + shared reciprocity + residual full span + "
                "nonflatness => all four direct-arm deleted stars have rank 3, "
                "or contradiction"
            ),
            "f14_scope": (
                "proves nonflatness over the exact source equations; it does "
                "not prove goodness and explicitly records a rank-deficient "
                "alternative"
            ),
        },
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"selected-witness dependency ledger changed: {digest}")
    print("N=8 selected-witness global dependency audit: INCOMPLETE")
    print("r=0..3: curved doubly-good overlap or exact contradiction")
    print("r=4 matching: closed after the frozen lower-matching proofs")
    print("r=4 shared and r=5..12: exact flat branch is contradictory")
    print("UNCOVERED: nonflat shared pair with a diagonal essential arm and pure deletion")
    print("full-span budgets do not supply goodness: counterguard 17/18, ranks 2,3,3,3")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
