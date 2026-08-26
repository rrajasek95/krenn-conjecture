#!/usr/bin/env python3
"""Build the exact, metadata-only N=8 attack/obstruction ledger."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


PINS = {
    "six_site_certified_proof": ("proofs/six-site-arbitrary-complex-obstruction.md", "b36b2f9ccb577af0aebf897edfc9fa1f84d01ba0cf4ea49ac11799d992e00713"),
    "full_tail_entry": ("computations/unaudited-codex-full-tail-entry-incidence-2026-08-22/results_full_tail_entry_incidence.json", "3935a4bf729c361c0a78c3295b38c1dbc63be50795b6a575dac6209edad1d10c"),
    "clean_cap_interface": ("computations/unaudited-codex-n8-minlayer-clean-cap-interface-2026-08-23/results_minlayer_clean_cap_interface.json", "16c41cef071f9278fc33ddd2ed5ce8e94bcc65e5eacb6d64e34c9d00c0f6f6d0"),
    "triangle_replacement": ("computations/unaudited-codex-star-tautology-triangle-replacement-2026-08-22/results_star_tautology_triangle_replacement.json", "87ab81d69751c5bd2e805f68f503de95979f7b2d9cecd5e07ccd7ec4c723dcbc"),
    "support_0_through_6": ("computations/unaudited-codex-n8-x5-six-block-support-cap-2026-08-25/MANIFEST.sha256", "fcfc7f972dfb0ed6c7d9cffdc6e2ce552ebad68ae1bc0af121df1455029327b7"),
    "seven_block_boundary": ("computations/unaudited-codex-n8-x5-seven-block-support-boundary-2026-08-25/MANIFEST.sha256", "13bb284c0b400f7227db74f8a135155dd324251147ebf48711b9af8d10adcc85"),
    "rep0_closure_referee": ("computations/unaudited-codex-n8-x5-seven-block-carrier-closure-referee-2026-08-25/FINAL_MANIFEST.sha256", "db5db5ed43e9ab2403d82db0450438f767917d3973067367947fe15bad227ece"),
    "rep1_terminal": ("computations/unaudited-codex-n8-x5-rep1-all162-terminal-promotion-2026-08-26/FINAL_MANIFEST.sha256", "db5cc80c2b443027b60cdb6f514534e890ccc4b9d91979a84dd8bd08897e9ff4"),
    "rep3_terminal": ("computations/unaudited-codex-n8-x5-seven-block-rep3-diagonal-incidence-referee-2026-08-25/FINAL_MANIFEST.sha256", "9ab5890d02f9ab07ec41e2b472b07105842d152dba214b3eaa4c915f19c0ccf2"),
    "rep4_terminal": ("computations/unaudited-codex-n8-x5-rep4-all162-terminal-promotion-2026-08-26/FINAL_MANIFEST.sha256", "91a23cc3e90a45fe0bfc40efd661ce9639ddd84f51e6da411fc2a18ad3e14993"),
    "rectangle12_terminal": ("computations/unaudited-codex-n8-x5-rectangle12-all-ranks-terminal-promotion-audit-2026-08-25/MANIFEST.sha256", "6fb9659c96ee699e3caaf28a23b9f8ec916141cba1afff553d41a037759d3eb0"),
    "anchor4_terminal": ("computations/unaudited-codex-n8-x5-anchor-records12-15-terminal-promotion-audit-2026-08-25/FINAL_MANIFEST.sha256", "00a49e0426cccb020b870055fb4c1aa2c806b5e4aa6543862abee1689ebee315"),
    "rep2_prefix_referee": ("computations/unaudited-codex-n8-x5-rep2-first25-exact-q-terminal-referee-2026-08-26/FINAL_MANIFEST.sha256", "066347c8af9a579b8f09d1c1eebf0197e819753da839f30708616287c4336196"),
    "rep2_closed_t_referee": ("computations/unaudited-codex-n8-x5-rep2-group16-closed-t-exact-q-terminal-referee-2026-08-26/FINAL_MANIFEST.sha256", "429371c829f37109afb425cd48f9b6266045c640e8349cb96063692f42a28d6a"),
    "rep2_torus_cover": ("computations/unaudited-codex-n8-x5-rep2-group16-torus-gauge-decomposition-design-2026-08-26/MANIFEST.sha256", "1492e69373819fda0c50afc4f1366e2d6da90e857c26f73c03c0212ffd879282"),
    "rep2_smallest_unrun": ("computations/unaudited-codex-n8-x5-rep2-group16-Vt1Vt2Dt0-global-unit-gauge-design-2026-08-26/MANIFEST.sha256", "02e228e1f8eaaea3abf063c1c9534a1245b98f50743155c85eae619dc59cfbfe"),
    "rep5_nine_singletons": ("computations/unaudited-codex-n8-x5-rep5-nine-strata-exact-transport-census-2026-08-26/MANIFEST.sha256", "c68dcd0f4524f672d31ff0a94eb923eb7cd5c6a3eeeb706bb9405eb883f6442b"),
    "rep5_rank_strata": ("computations/unaudited-codex-n8-x5-rep5-rank-stratified-guard-pivot-design-v2-2026-08-25/MANIFEST.sha256", "50ed9510e2278f136cbfe28ee0df12a0139e6ef5ad6cfeda9d3b2a589aa16fe1"),
    "rep5_smallest70_cover": ("computations/unaudited-codex-n8-x5-rep5-smallest70-global-three-torus-reduction-design-2026-08-26/MANIFEST.sha256", "65485dd5f8a0994c0512e82a8ac8ef9e188f5b6fab0a1e1bb2cea3dc7aca6914"),
    "rep5_next_symbolic_cover": ("computations/unaudited-codex-n8-x5-rep5-four-subchart-next-symbolic-reduction-design-2026-08-26/MANIFEST.sha256", "d347c3bd4ed99764d103435d25cdaf9b676875d9f90b988ff9cb38073fb585a1"),
    "x5_d10_four_exact": ("computations/unaudited-codex-n8-x5-four-d10-seeded-support-repair-2026-08-25/MANIFEST.sha256", "28ccf2676b9fc98de20971d94e2c54a30d4dbab90eb7121bdb22ad245bda0b5c"),
    "x5_d11_partition": ("computations/unaudited-codex-n8-x5-four-d11-seeded-support-repair-2026-08-25/MANIFEST.sha256", "828fb7ac9f0d745383c734f4ee408219ac38b693b66f59299db4a851b7377116"),
    "x5_d11_triangle_checkpoint": ("computations/unaudited-codex-n8-x5-d11-triangle-partial-batch-production-held-2026-08-25/PRODUCTION_MANIFEST.sha256", "6a392f8f65d9ef921227b57d3fcb560e85f327eeb3b03d5750ee26d9d9bbe88b"),
    "affine_d12_terminal": ("computations/unaudited-codex-n8-affine251-d12-round1641-retry3-support-cap-terminal-audit-2026-08-25/FINAL_MANIFEST.sha256", "9c017349be904334c59e218e791cf17340f0cb8cb520c689fb56487a8777fa09"),
    "pure_chart_coverage": ("computations/unaudited-codex-n8-fh-chart-coverage-audit-2026-08-23/REPORT.md", "44348a70dc2cc47aecbded3272bcf89c68fe46de6c95b1d61b54c47064f0b759"),
    "pacomp_farkas": ("computations/unaudited-codex-n8-pacomp-h3-primitive-hom1-coefficient-ansatz-2026-08-26/MANIFEST.sha256", "a2ba22f8b7af8adad758dee18aa05a5a515f099ddca3eb3fe240868c29a8fa19"),
    "k9_k12_scalar_tail": ("computations/unaudited-codex-orbit0-k9-tail-charge-feasibility-2026-08-24/MANIFEST.sha256", "0523fd24659e4678e4d59514e1f1d3eb7b33f6179e539d5ccf9e472c1bfbf7a8"),
    "k24_conservation_audit": ("computations/unaudited-codex-orbit0-k24-complete35-conservation-audit-2026-08-24/FINAL_MANIFEST.sha256", "33d38fce3104faa547f5413df26a7f0906f4067d249df04003bb8e8e1cacfe8f"),
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def require(condition: bool, detail: object = "validation failure") -> None:
    if not condition:
        raise ValueError(detail)


def node(node_id: str, status: str, title: str, *, depends_on=(), evidence=(), scope="", open_decision=None, independence=()):
    return {
        "id": node_id,
        "status": status,
        "title": title,
        "depends_on": list(depends_on),
        "evidence": list(evidence),
        "scope": scope,
        "open_decision": open_decision,
        "independent_of": list(independence),
    }


def make_ledger() -> dict:
    nodes = [
        node("normalized_x5_interface", "CLOSED_INTERFACE", "Normalized full-X5/clean-cap interface", evidence=("full_tail_entry", "clean_cap_interface", "triangle_replacement", "six_site_certified_proof"), scope="A live active clean cap routes to the certified six-site contradiction; this is an interface, not the remaining global dichotomy."),
        node("support_layers_0_6", "CLOSED", "All support layers with at most six added blocks", depends_on=("normalized_x5_interface",), evidence=("support_0_through_6",), scope="All 38,760 six-block supports and the inherited zero-through-five layers close under the formal guard."),
        node("seven_block_boundary", "CLOSED_REDUCTION", "Seven-block layer reduced to 64 coefficient strata", depends_on=("support_layers_0_6",), evidence=("seven_block_boundary",), scope="7,776 of 7,840 stable strata close structurally; 64 are the exact finite boundary."),
        node("seven_block_nonfull16", "CLOSED", "All 16 non-full-family seven-block records", depends_on=("seven_block_boundary",), evidence=("rectangle12_terminal", "anchor4_terminal"), scope="Twelve rectangle records close in ranks 0,1,2,3 and four anchor/no-rectangle records close over Q."),
        node("seven_rep0", "CLOSED", "Full-family representative 0", depends_on=("seven_block_boundary",), evidence=("rep0_closure_referee",), scope="The exact rank <=1/rank2 incidence certificates and rank3 exclusion close rep0 within its stated source family."),
        node("seven_rep1", "CLOSED", "Full-family representative 1", depends_on=("seven_block_boundary",), evidence=("rep1_terminal",), scope="All 162 canonical exact-Q groups, hence all 972 raw rep1 guard-minor charts, are unit. No cross-representative transport is claimed."),
        node("seven_rep2", "OPEN", "Full-family representative 2", depends_on=("seven_block_boundary",), evidence=("rep2_prefix_referee", "rep2_closed_t_referee", "rep2_torus_cover", "rep2_smallest_unrun"), scope="Canonical groups 0-15 are closed. Group16 is not closed; two members of its exact 60-chart refinement are closed, 58 remain. Groups17-161 are not accepted.", open_decision={"first_blocker": "canonical group16", "smallest_certified_unrun_source": "V(t1,t2) intersect D(t0), torus-gauged exact-Q chart", "variables": 61, "generators": 6568, "global_remaining_after_group16": "groups17-161"}, independence=("seven_rep5",)),
        node("seven_rep3", "CLOSED", "Full-family representative 3", depends_on=("seven_block_boundary",), evidence=("rep3_terminal",), scope="Five color-orbit diagonal-incidence charts close exactly over Q plus the structural zero branch; only rep3 scope."),
        node("seven_rep4", "CLOSED", "Full-family representative 4", depends_on=("seven_block_boundary",), evidence=("rep4_terminal",), scope="All 162 canonical exact-Q groups, hence all 972 raw rep4 charts, are unit. No cross-representative transport is claimed."),
        node("seven_rep5", "OPEN", "Full-family representative 5", depends_on=("seven_block_boundary",), evidence=("rep5_nine_singletons", "rep5_rank_strata", "rep5_smallest70_cover", "rep5_next_symbolic_cover"), scope="The exact rank/pivot cover has nine strata and the transport partition is nine singletons. Existing modular attempts are zero-coverage timeouts; reductions are design-only.", open_decision={"required_representatives": 9, "transport_classes": 9, "selected_stratum": "open84 k2/t1", "smallest_materialized_descendant": "three-torus all-closed source", "variables": 67, "generators": 3645, "warning": "Closing this one descendant does not close its eight-chart parent cover, the selected stratum, or the other eight singleton strata."}, independence=("seven_rep2",)),
        node("seven_block_terminal_assembly", "OPEN_INTEGRATION", "Complete seven-block theorem", depends_on=("seven_block_nonfull16", "seven_rep0", "seven_rep1", "seven_rep2", "seven_rep3", "seven_rep4", "seven_rep5"), scope="Current exact count is 48/64 boundary records locally discharged and 16/64 in rep2/rep5 still open. A final source-labelled 64-record assembly must bind every representative theorem and zero-coefficient boundary; no such terminal promotion is sealed.", open_decision={"open_boundary_records": 16, "open_representative_families": [2, 5]}),
        node("support_layers_8_20", "OPEN_THEOREM", "Support classification/induction for eight through twenty added blocks", depends_on=("seven_block_terminal_assembly",), scope="The seven-block theorem is only a base candidate; no exact monotone carrier extension or exhaustive 8-20 census is sealed.", open_decision={"lemma": "Every guard-preserving support with at least eight added blocks either descends to a smaller closed support or has an active clean triangle/star cap."}),
        node("x5_global_clean_cap_arrow", "OPEN_ROUTE", "Global normalized-X5 clean-cap contradiction", depends_on=("normalized_x5_interface", "support_layers_8_20"), scope="Would close the direct X5 route once all support sizes and formal/source bridges are assembled."),
        node("x5_degree_6_10", "CLOSED_FINITE_DEGREES", "Four blocker ideals: exact Q nonmembership through degree 10", evidence=("x5_d10_four_exact",), scope="Finite-degree dual certificates only; not an all-degree theorem."),
        node("x5_degree_11_coloured", "OPEN", "Degree-11 coloured blocker branches", depends_on=("x5_degree_6_10",), evidence=("x5_d11_partition", "x5_d11_triangle_checkpoint"), scope="Direct D11 transports exactly; triangle/third/cap branches remain unresolved. The triangle has a verified restart checkpoint, not a verdict.", open_decision={"triangle_checkpoint_selected": 1250001, "triangle_checkpoint_support": 1378456, "field": "p=1073741827", "remaining_branches_after_triangle": ["third-colour", "cap-endpoint-colour"], "acceptance_needed": "second prime plus literal characteristic-zero lift/replay"}, independence=("seven_rep2", "seven_rep5")),
        node("x5_all_degree_recurrence", "OPEN_THEOREM", "All-degree blocker obstruction/regularity", depends_on=("x5_degree_11_coloured",), scope="No recurrence transports the four duals to every degree and no finite degree bound is proved."),
        node("affine_d12_search", "OPEN_COMPUTATION", "251-variable affine degree-12 membership search", evidence=("affine_d12_terminal",), scope="Accepted state remains round1640 at 4,069,711 columns/support76,616. Retry3 exposed 223,328 next columns and a 464,887-support candidate but returned SUPPORT_CAP; the hybrid is zero coverage and nonresumable.", open_decision={"smallest_known_next_capacity": {"columns": 4293039, "support_at_least": 464887}, "warning": "Admitting one round is not a convergence theorem."}, independence=("x5_global_clean_cap_arrow", "pacomp_uniform_descent", "k24_relative_route")),
        node("affine_d12_regularity", "OPEN_THEOREM", "Degree/saturation bound making D12 decisive", scope="A D12 member is a valid local affine unit certificate. A D12 nonmember has no affine consequence without a new degree or saturation bound."),
        node("affine_d12_route", "OPEN_ROUTE", "Finite affine-membership route", depends_on=("affine_d12_search", "affine_d12_regularity"), scope="Search termination and the structure theorem are conjunctive, independent obligations."),
        node("pure_chart_globalization", "OPEN_ROUTE", "Pure-chart/orbit globalization", evidence=("pure_chart_coverage",), scope="The pure-product cover has 31 chart orbits and no sealed all-chart certificate/boundary-descent theorem. This is an alternative to the direct normalized-X5 support route.", open_decision={"chart_orbits": 31, "smallest_symbolic_gap": "provenance-preserving C4/boundary descent across entering-cell divisors"}, independence=("affine_d12_route", "pacomp_uniform_descent")),
        node("pacomp_pinned_ansatz", "CLOSED_NO_GO", "PAComp pinned primitive/composite coefficient ansatz", evidence=("pacomp_farkas",), scope="Exact Q Farkas covectors exclude the maximal pinned/formally granted switch/Gamma ansatz before coherence/face checks. This is a no-go for that ansatz, not PAComp or the conjecture."),
        node("pacomp_new_hom1", "OPEN_FINITE_INTERFACE", "New physical primitive Hom^1(response,cap)", depends_on=("pacomp_pinned_ansatz",), scope="A successful constructor must add genuinely new source records carrying both missing quotient signatures; existing 128 primitives/composites cannot.", open_decision={"instances": 4, "required_top_signature": "Lambda01 quotient component eta=2,tB=tC=0 rather than GammaB/GammaC span", "required_retained_signature": "Pi_r,01 correction for each retained row", "after_source_fit": "replay 8 coherence and 5 face checks"}),
        node("pacomp_uniform_descent", "OPEN_ROUTE", "PAComp/uniform-descent proof", depends_on=("pacomp_new_hom1",), scope="Independent proof architecture; current Farkas result narrows its missing primitive but supplies no constructor."),
        node("k9_k12_scalar_tail", "CLOSED_SCALAR", "Omitted K9-K12 scalar tail", evidence=("k9_k12_scalar_tail",), scope="Exact charge -4,564,224 cancels the previously missing +4,564,224. No scalar tail defect remains."),
        node("k24_35_charge", "CLOSED_DIAGNOSTIC", "K24 35/35 charge/conservation audit", depends_on=("k9_k12_scalar_tail",), evidence=("k24_conservation_audit",), scope="The accepted ten-group artifact sum has excess +19,715,328 and therefore rejects the purported source-faithful recurrence completion. It is not a nonmembership or conjecture certificate."),
        node("k24_relative_route", "OPEN_ROUTE", "Orbit-zero source-faithful replay and relative terminal membership", depends_on=("k24_35_charge",), scope="First repair/prove occurrencewise K14-K24 provenance under one policy; then decide B=(L,T), A24_rel=T|ker(L), with lower corrections. Finally globalize beyond orbit-zero/anchors-one.", open_decision={"first_finite_problem": "source-labelled K14-K24 occurrence replay resolving +19715328", "second_finite_problem": "exact relative solve or dual for B*x=(0,0,0,R24)", "global_scope_remaining": "30 other chart orbits plus same-source transport"}, independence=("x5_global_clean_cap_arrow", "affine_d12_route", "pacomp_uniform_descent")),
        node("n8_conjecture", "OPEN", "General bicoloured N=8,d=3 conjecture", scope="No current route supplies a full-scope proof or countercertificate. Any one independently complete global route could settle it; the listed routes are alternatives, not conjunctive prerequisites."),
    ]
    routes = [
        {"id": "direct_x5", "terminal_node": "x5_global_clean_cap_arrow", "status": "OPEN", "blocking_nodes": ["seven_rep2", "seven_rep5", "seven_block_terminal_assembly", "support_layers_8_20"]},
        {"id": "finite_affine_d12", "terminal_node": "affine_d12_route", "status": "OPEN", "blocking_nodes": ["affine_d12_search", "affine_d12_regularity"]},
        {"id": "pure_chart", "terminal_node": "pure_chart_globalization", "status": "OPEN", "blocking_nodes": ["pure_chart_globalization"]},
        {"id": "pacomp_descent", "terminal_node": "pacomp_uniform_descent", "status": "OPEN", "blocking_nodes": ["pacomp_new_hom1"]},
        {"id": "orbit0_relative_k24", "terminal_node": "k24_relative_route", "status": "OPEN_LOCAL_THEN_GLOBAL", "blocking_nodes": ["k24_relative_route"]},
    ]
    return {
        "schema": "KRENN_N8_CURRENT_EXACT_ATTACK_OBSTRUCTION_LEDGER_V1",
        "as_of": "2026-08-26",
        "status": "OPEN_NO_CONJECTURE_VERDICT",
        "headline": "Local seven-block progress is terminal for reps0,1,3,4 and all 16 non-full-family records; reps2 and5 leave 16 seven-block records open, and no route has yet supplied the separate global/regularity/descent arrow.",
        "counts": {
            "seven_block_total_boundary_records": 64,
            "seven_block_closed_records": 48,
            "seven_block_open_records": 16,
            "closed_full_family_representatives": [0, 1, 3, 4],
            "open_full_family_representatives": [2, 5],
            "closed_nonfull_records": 16,
            "rep2_closed_canonical_groups": list(range(16)),
            "rep2_first_open_canonical_group": 16,
            "rep5_exact_transport_classes": 9,
        },
        "logical_nodes": nodes,
        "routes": routes,
        "independence_summary": {
            "genuinely_independent_global_routes": ["direct_x5", "finite_affine_d12", "pure_chart", "pacomp_descent", "orbit0_relative_k24"],
            "independent_local_leaves": [["seven_rep2", "seven_rep5"], ["affine_d12_search", "affine_d12_regularity"]],
            "not_independent": [
                "support_layers_8_20 is downstream of a terminal seven-block base, although its design can proceed in parallel",
                "the K24 relative solve is downstream of source-provenance repair; the scalar tail is already closed",
                "a modular UNIT diagnostic is not independent characteristic-zero coverage",
            ],
        },
        "evidence_pins": {k: {"path": p, "sha256": h} for k, (p, h) in PINS.items()},
        "nonclaims": [
            "No new solver or active production cache was run or read.",
            "Representative closure is not cross-representative transport.",
            "Design-only covers and modular diagnostics add zero characteristic-zero coverage.",
            "The PAComp Farkas certificate excludes only the pinned/formally granted ansatz.",
            "The K24 +19,715,328 value rejects recurrence provenance; it does not separate the conjecture target.",
            "Finite-degree nonmembership is not an all-degree or affine nonmembership theorem.",
        ],
    }


def validate_ledger(data: dict, *, check_files: bool = True) -> None:
    require(data["status"] == "OPEN_NO_CONJECTURE_VERDICT", "false conjecture status")
    nodes = data["logical_nodes"]
    ids = [n["id"] for n in nodes]
    require(len(ids) == len(set(ids)), "duplicate node")
    known = set(ids)
    for n in nodes:
        require(bool(n["status"]), (n["id"], "empty status"))
        require(set(n["depends_on"]) <= known, (n["id"], "unknown dependency"))
        require(set(n["evidence"]) <= set(PINS), (n["id"], "unknown evidence"))
    # Dependency graph must be acyclic.
    deps = {n["id"]: set(n["depends_on"]) for n in nodes}
    remaining = set(deps)
    while remaining:
        ready = {x for x in remaining if not (deps[x] & remaining)}
        require(bool(ready), "dependency cycle")
        remaining -= ready
    c = data["counts"]
    require(c["seven_block_closed_records"] + c["seven_block_open_records"] == c["seven_block_total_boundary_records"] == 64, "boundary count")
    require(c["seven_block_open_records"] == 16, "open boundary count")
    require(c["closed_full_family_representatives"] == [0, 1, 3, 4], "closed reps")
    require(c["open_full_family_representatives"] == [2, 5], "open reps")
    require(c["rep2_closed_canonical_groups"] == list(range(16)), "rep2 prefix")
    require(c["rep5_exact_transport_classes"] == 9, "rep5 transport")
    if check_files:
        for name, (rel, expected) in PINS.items():
            path = ROOT / rel
            require(path.is_file(), (name, rel, "missing"))
            actual = sha256(path)
            require(actual == expected, (name, rel, actual, expected))


def hostile_tests(data: dict) -> list[dict]:
    cases = []
    def rejects(name, mutate):
        clone = json.loads(json.dumps(data))
        mutate(clone)
        try:
            validate_ledger(clone, check_files=False)
        except (AssertionError, KeyError, ValueError):
            cases.append({"name": name, "rejected": True})
        else:
            raise AssertionError(f"hostile accepted: {name}")
    rejects("false_conjecture_pass", lambda x: x.__setitem__("status", "PASS"))
    rejects("duplicate_node", lambda x: x["logical_nodes"].append(x["logical_nodes"][0]))
    rejects("unknown_dependency", lambda x: x["logical_nodes"][0]["depends_on"].append("missing"))
    rejects("cycle", lambda x: x["logical_nodes"][0]["depends_on"].append("normalized_x5_interface"))
    rejects("wrong_open_count", lambda x: x["counts"].__setitem__("seven_block_open_records", 15))
    rejects("wrong_rep2_prefix", lambda x: x["counts"].__setitem__("rep2_closed_canonical_groups", list(range(17))))
    rejects("false_rep5_transport", lambda x: x["counts"].__setitem__("rep5_exact_transport_classes", 1))
    rejects("unknown_evidence", lambda x: x["logical_nodes"][0]["evidence"].append("fabricated"))
    return cases


def atomic_json(path: Path, data: object) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    os.replace(tmp, path)


def main() -> None:
    data = make_ledger()
    validate_ledger(data)
    hostiles = hostile_tests(data)
    atomic_json(HERE / "results_attack_obstruction_ledger.json", data)
    atomic_json(HERE / "results_hostiles.json", {"schema": "KRENN_N8_ATTACK_LEDGER_HOSTILES_V1", "status": "PASS", "cases": hostiles})
    print(json.dumps({"status": "PASS", "nodes": len(data["logical_nodes"]), "pins": len(PINS), "hostiles": len(hostiles)}, sort_keys=True))


if __name__ == "__main__":
    main()
