#!/usr/bin/env python3
"""Apply the symmetric P0 hybrid to the final target-coloop bistar web.

The endpoint-hybrid theorem leaves only cancellation matchings B' with the
same physical ports P0,S1 as the pure-2 target anchor M.  Their P0 cell has
labels 11, while M carries 22.  Use P0:11 with the three pure-2 cells of
M off P0.  The resulting mixed zero row either reselects pure 2 away from
P0 or forces an avoiding matching.  This checker classifies every avoiding
matching and isolates the unique P2,S3 two-edge return.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_axis_target_coloop_endpoint_hybrid_cancellation.py":
        "8187cd44d88ffcc17c532483519aca935824315f7cad9b859d051c58ac10cce9",
    "notes/h3-axis-target-coloop-endpoint-hybrid-cancellation.md":
        "76c8100f9200c52209a98ca785a42f62a1cf410e1150903c2c4f864ba40f0f15",
    "computations/verify_uniform_decorated_anchor_mixed_word_exchange.py":
        "150bf15eb8ac475f866c062afcd7e3002477d02338acdb082c14f9136a3e58b7",
    "notes/uniform-decorated-anchor-mixed-word-exchange.md":
        "0cdc391bebb44150c7941bdbeec853029929f20d46ee813eb2a09bb76c27a5de",
}
EXPECTED_LEDGER_SHA256 = "1e5415e20eaed90c971a6d5b4ec6bfcee50f695ac1bcc874f6f9e388fce50074"

P, S = 6, 7
PURE_TWO = (2,) * 8
SECOND_HYBRID = (1, 2, 2, 2, 2, 2, 1, 2)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(relative, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(spec is not None and spec.loader is not None,
            f"cannot load dependency: {relative}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def decorated_cell(pair, word):
    left, right = pair
    return pair, (word[left], word[right])


def decorated_monomial(matching, word):
    return frozenset(decorated_cell(pair, word) for pair in matching)


def reconstruct_first_residuals(first, routing):
    all_matchings, bright, records = first.residual_records(routing)
    residuals = []
    source_histogram = Counter()
    for record in records:
        M, N, K, L = (record[key] for key in ("M", "N", "K", "L"))
        anchor_union = set(M) | set(K) | set(L)
        for rho3 in range(3):
            first_hybrid = list((1,) * 8)
            first_hybrid[3] = rho3
            first_hybrid[S] = 2
            first_hybrid = tuple(first_hybrid)
            for mate in bright:
                if routing.edge(S, 3) in mate:
                    continue
                external = set(mate) - anchor_union
                if routing.crossed_port(mate):
                    continue
                if any(P in pair or S in pair for pair in external):
                    continue
                if any(first_hybrid[left] != first_hybrid[right]
                       for left, right in external):
                    continue
                require((routing.partner(mate, P),
                         routing.partner(mate, S)) == (0, 1),
                        "a first residual lost M's endpoint ports")
                residuals.append({
                    "source_kind": record["kind"],
                    "rho3": rho3,
                    "M": M, "N": N, "K": K, "L": L,
                    "B": mate,
                })
                source_histogram[(record["kind"], rho3)] += 1
    require(len(residuals) == 618,
            f"the first-hybrid residual count changed: {len(residuals)}")
    require(source_histogram == Counter({
        ("q_only", 0): 58, ("q_only", 1): 144,
        ("q_only", 2): 58,
        ("Hall", 0): 18, ("Hall", 1): 36, ("Hall", 2): 18,
        ("same_skeleton", 0): 68, ("same_skeleton", 1): 150,
        ("same_skeleton", 2): 68,
    }), f"the first residual histogram changed: {source_histogram}")
    return all_matchings, bright, tuple(residuals), source_histogram


def audit_second_hybrid(routing, bright, residuals):
    changed_edge = routing.edge(P, 0)
    categories = Counter()
    by_source = Counter()
    examples = {}
    through_alternates = 0

    for residual in residuals:
        M, N, K, L, B = (
            residual[key] for key in ("M", "N", "K", "L", "B")
        )
        require((routing.partner(B, P), routing.partner(B, S)) == (0, 1)
                and changed_edge in B and changed_edge in M,
                "the second hybrid lost its common P0 edge")
        require(changed_edge not in K and changed_edge not in L,
                "P0 stopped being unique to M among pure anchors")

        # The active B term from the first hybrid supplies P0:11.  All three
        # remaining M cells are selected pure-2 cells.  This is the literal
        # mixed word 12222212.
        b_changed = decorated_cell(changed_edge, SECOND_HYBRID)
        m_pure_changed = decorated_cell(changed_edge, PURE_TWO)
        require(b_changed == (changed_edge, (1, 1))
                and m_pure_changed == (changed_edge, (2, 2)),
                "the P0 decoration pair changed")
        require(decorated_monomial(M, SECOND_HYBRID) - {b_changed}
                == decorated_monomial(M, PURE_TWO) - {m_pure_changed},
                "the selected second-hybrid M tail stopped being pure 2")

        retaining = tuple(matching for matching in bright
                          if changed_edge in matching)
        omitting = tuple(matching for matching in bright
                         if changed_edge not in matching)
        require(len(retaining) == 15 and len(omitting) == 75,
                "the P0 retaining/omitting split changed")
        for matching in retaining:
            if matching == M:
                continue
            require(decorated_monomial(matching, SECOND_HYBRID)
                    - {b_changed}
                    == decorated_monomial(matching, PURE_TWO)
                    - {m_pure_changed},
                    "a through-P0 mate lost pure-2 replacement")
            through_alternates += 1

        anchor_union = set(M) | set(K) | set(L)
        for matching in omitting:
            p_partner = routing.partner(matching, P)
            s_partner = routing.partner(matching, S)
            p_edge = next(pair for pair in matching if P in pair)
            require(p_partner != 0
                    and SECOND_HYBRID[p_partner] == 2
                    and SECOND_HYBRID[P] == 1,
                    "an omitting mate lost its offdiagonal P cell")

            external = set(matching) - anchor_union
            if any(P in pair or S in pair for pair in external):
                category = "external_endpoint_arm"
            elif (p_partner, s_partner) == (2, 1):
                category = "crossed_response_P2_S1"
            elif any(SECOND_HYBRID[left] != SECOND_HYBRID[right]
                     for left, right in external):
                category = "external_offdiagonal_q"
            else:
                require((p_partner, s_partner) == (2, 3),
                        "the endpoint-contained mate was neither crossed nor return")
                require(p_edge == routing.edge(P, 2) and p_edge in L
                        and routing.edge(S, 3) in matching,
                        "the two-edge return left L's endpoint skeleton")
                category = "P2_S3_two_edge_return"
            categories[category] += 1
            by_source[(residual["source_kind"], category)] += 1
            examples.setdefault(category, {
                "source_kind": residual["source_kind"],
                "rho3": residual["rho3"],
                "M": M, "N": N, "K": K, "L": L, "B": B,
                "second_mate": matching,
                "external_edges": tuple(sorted(external)),
                "decorated_cells": tuple(sorted(
                    decorated_cell(pair, SECOND_HYBRID)
                    for pair in matching
                )),
            })

    require(through_alternates == 618 * 14,
            "the through-P0 alternate target count changed")
    require(categories == Counter({
        "external_endpoint_arm": 42642,
        "crossed_response_P2_S1": 1854,
        "external_offdiagonal_q": 1002,
        "P2_S3_two_edge_return": 852,
    }), f"the second-hybrid omitting split changed: {categories}")
    require(by_source == Counter({
        ("q_only", "external_endpoint_arm"): 17940,
        ("q_only", "crossed_response_P2_S1"): 780,
        ("q_only", "external_offdiagonal_q"): 460,
        ("q_only", "P2_S3_two_edge_return"): 320,
        ("Hall", "external_endpoint_arm"): 4968,
        ("Hall", "crossed_response_P2_S1"): 216,
        ("Hall", "external_offdiagonal_q"): 72,
        ("Hall", "P2_S3_two_edge_return"): 144,
        ("same_skeleton", "external_endpoint_arm"): 19734,
        ("same_skeleton", "crossed_response_P2_S1"): 858,
        ("same_skeleton", "external_offdiagonal_q"): 470,
        ("same_skeleton", "P2_S3_two_edge_return"): 388,
    }), f"the second-hybrid source split changed: {by_source}")

    canonical = examples["P2_S3_two_edge_return"]
    require(canonical["M"] == (
        (0, 6), (1, 7), (2, 3), (4, 5)
    ) and canonical["second_mate"] == (
        (0, 1), (2, 6), (3, 7), (4, 5)
    ), "the canonical two-edge return changed")

    return {
        "first_hybrid_residuals": len(residuals),
        "second_hybrid_word": "12222212",
        "changed_edge": [0, P],
        "selected_changed_cell": "P0:11",
        "pure_anchor_cell": "P0:22",
        "retaining_matchings_per_residual": 15,
        "retaining_alternates_checked": through_alternates,
        "omitting_matchings_per_residual": 75,
        "omitting_counts": dict(categories),
        "omitting_counts_by_source_kind": {
            str(key): value for key, value in sorted(by_source.items())
        },
        "canonical_two_edge_return": canonical,
        "factor_dichotomy": (
            "G_12222212=x_(P0;11)*H_(P0)^2+O_(P0).  If O=0, "
            "the mixed zero row forces H=0 and the pure-2 target forces a "
            "pure-2 matching omitting P0; reselecting it makes B's P0 arm "
            "external.  If O!=0, some omitting mate is nonzero and is "
            "external, crossed P2,S1, externally offdiagonal in q, or the "
            "P2,S3 two-edge return"
        ),
    }


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def main():
    pin_dependencies()
    first = load(
        "computations/verify_h3_axis_target_coloop_endpoint_hybrid_cancellation.py",
        "target_coloop_first_hybrid_dependency",
    )
    routing = load(
        "computations/verify_h3_axis_target_coloop_other_bright_matching_routing.py",
        "target_coloop_second_hybrid_routing_dependency",
    )
    _all, bright, residuals, source_histogram = reconstruct_first_residuals(
        first, routing
    )
    audit = audit_second_hybrid(routing, bright, residuals)
    ledger = {
        "pins": PINS,
        "first_residual_histogram": {
            str(key): value for key, value in sorted(source_histogram.items())
        },
        "second_endpoint_hybrid": audit,
        "theorem": (
            "the sole first-hybrid residual has a nonzero P0:11 cell on "
            "the pure-2 M edge P0:22.  Its complete P0 hybrid row forces a "
            "pure-2 reselection away from P0, an external endpoint arm, a "
            "crossed P2,S1 matching, an external offdiagonal q-cell, or "
            "exactly the P2,S3 two-edge return"
        ),
        "remaining_obligation": (
            "the return term has literal endpoint cells P2:12 and S3:22 "
            "on L's two selected arms, with a pure-2 residual tail except "
            "for the single site-0 label.  This is the precise two-edge "
            "companion/recurrence packet; no arbitrary decorated-anchor "
            "mate remains"
        ),
        "scope": (
            "exact matching and word classification of the complete second "
            "hybrid row.  It does not declare the P2,S3 return empty; that "
            "requires the source-typed two-edge companion identity"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"second endpoint hybrid ledger changed: {digest}")
    print("h3 target-coloop second endpoint hybrid: PASS")
    print("first residuals: 618; second word: 12222212")
    print("omitting mates: endpoint 42642 / crossed 1854 / offdiag-q 1002 / return 852")
    print("sole return: P2:12 and S3:22 on L's endpoint skeleton")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
