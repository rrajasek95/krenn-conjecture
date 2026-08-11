#!/usr/bin/env python3
"""Audit the endpoint-hybrid cancellation row on the target-coloop boundary.

The 48 residual-q-only, 12 strict-Hall, and 50 same-skeleton records all
have the same endpoint geometry: the selected mixed matching N and the
other-bright pure anchor L use ports P2,S3.  On their common S3 edge the
mixed word has endpoint head 2, whereas the pure-1 word has head 1.

Replace only that pure endpoint cell in L by the selected mixed cell of N.
The resulting hybrid output word has target zero and a nonzero L monomial.
Its complete 90-term direct-free hafnian forces either an alternate pure-1
matching or an omitting-edge mate.  This checker exhausts every possible
omitting-edge matching and identifies the unique unrouted type.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_axis_target_coloop_other_bright_matching_routing.py":
        "132be928909da3a8c8d5362fabe3dd04bc88eeb8428433fc1f8053d5d850c93e",
    "notes/h3-axis-target-coloop-other-bright-matching-routing.md":
        "fd6e8dc71338b3fea8ea1fd9b92e427c187b11152697b861a7c40aa66ff11dd6",
    "computations/verify_uniform_one_bad_nonanchor_offdiagonal_good_pair.py":
        "64e85cd84112b5160efe4f43ce1208da3c49f5e58b3e4a4d6192e6a9c229c306",
    "notes/uniform-one-bad-nonanchor-offdiagonal-good-pair.md":
        "4516c5ff02f130e1ad25b4fde395c81557e58ba0c83f7f98969d95df17fd6409",
    "computations/verify_uniform_hall_terminal_transfer_bistar_curvature_boundary.py":
        "aa1da69a09c3c34f90024a42b27ab0d0a30b0c1263a6a059d256ff085084c048",
    "notes/uniform-hall-terminal-transfer-bistar-curvature-boundary.md":
        "07523ffcef85b86c0b0808ddec43f1731c99f4426451f0e22171f864e82949aa",
}
EXPECTED_LEDGER_SHA256 = "d0f33488f518ed2501bd4a6e7a955bf487e7984b9041870dc36bb67a3aba907a"

P, S = 6, 7
PURE_ONE = (1,) * 8


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_routing():
    relative = (
        "computations/"
        "verify_h3_axis_target_coloop_other_bright_matching_routing.py"
    )
    spec = importlib.util.spec_from_file_location(
        "target_coloop_matching_routing_dependency", ROOT / relative
    )
    require(spec is not None and spec.loader is not None,
            "cannot load the matching-routing dependency")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def decorated_cell(pair, word):
    left, right = pair
    return pair, (word[left], word[right])


def decorated_monomial(matching, word):
    return frozenset(decorated_cell(pair, word) for pair in matching)


def residual_records(module):
    all_matchings = tuple(module.perfect_matchings(range(8)))
    bright = tuple(matching for matching in all_matchings
                   if module.edge(P, S) not in matching)
    records = []
    histogram = Counter()
    for triple_index, (target, outside, direct, cycle) in enumerate(
            module.no_cross_unary_triples(all_matchings)):
        for other_bright in bright:
            anchor_union = set(target) | set(direct) | set(other_bright)
            crossed = any(
                module.crossed_port(matching)
                for matching in all_matchings
                if set(matching) <= anchor_union
            )
            external = set(outside) - anchor_union
            endpoint_external = any(
                P in pair or S in pair for pair in external
            )
            if crossed:
                kind = "crossed"
            elif external and endpoint_external:
                kind = "endpoint"
            elif external:
                kind = "q_only"
            elif other_bright != outside:
                kind = "Hall"
            else:
                kind = "same_skeleton"
            histogram[kind] += 1
            if kind in ("q_only", "Hall", "same_skeleton"):
                records.append({
                    "triple": triple_index,
                    "kind": kind,
                    "cycle": cycle,
                    "M": target,
                    "N": outside,
                    "K": direct,
                    "L": other_bright,
                    "external_N": tuple(sorted(external)),
                })
    require(histogram == Counter({
        "crossed": 612,
        "endpoint": 3778,
        "q_only": 48,
        "Hall": 12,
        "same_skeleton": 50,
    }), f"the residual-record partition changed: {histogram}")
    require(Counter(record["kind"] for record in records) == Counter({
        "q_only": 48, "Hall": 12, "same_skeleton": 50,
    }), "the 110-record hybrid domain changed")
    return all_matchings, bright, tuple(records)


def audit_actual_mixed_word_split(records):
    """Split the 48 q-only records using d=rho+(1,2), literally."""

    histogram = Counter()
    for record in records:
        if record["kind"] != "q_only":
            continue
        external = record["external_N"]
        require(external and all(P not in pair and S not in pair
                                 for pair in external),
                "a q-only record acquired an endpoint edge")
        for rho in product(range(3), repeat=6):
            offdiagonal = any(rho[left] != rho[right]
                              for left, right in external)
            histogram[(record["cycle"], len(external),
                       "offdiagonal" if offdiagonal else "diagonal")] += 1
    expected = Counter({
        (6, 1, "offdiagonal"): 4860,
        (6, 1, "diagonal"): 2430,
        (8, 1, "offdiagonal"): 5832,
        (8, 1, "diagonal"): 2916,
        (8, 2, "offdiagonal"): 16848,
        (8, 2, "diagonal"): 2106,
    })
    require(histogram == expected,
            f"the literal d-word split changed: {histogram}")
    require(sum(value for key, value in histogram.items()
                if key[2] == "offdiagonal") == 27540,
            "the offdiagonal d-word count changed")
    require(sum(value for key, value in histogram.items()
                if key[2] == "diagonal") == 7452,
            "the diagonal d-word count changed")
    return histogram


def audit_endpoint_hybrid(module, all_matchings, bright, records):
    category_counts = Counter()
    by_rho3 = Counter()
    by_record_kind = Counter()
    examples = {}
    retaining_alternates = 0

    for record in records:
        M, N, K, L = (record[key] for key in ("M", "N", "K", "L"))
        n_ports = (module.partner(N, P), module.partner(N, S))
        l_ports = (module.partner(L, P), module.partner(L, S))
        m_ports = (module.partner(M, P), module.partner(M, S))
        require(n_ports == l_ports == (2, 3),
                "N stopped sharing both endpoint ports with L")
        require(m_ports == (0, 1) and n_ports != m_ports,
                "N unexpectedly shared its ports with M")

        changed_edge = module.edge(S, 3)
        require(changed_edge in N and changed_edge in L
                and changed_edge not in M and changed_edge not in K,
                "the mixed/pure changed edge lost uniqueness")
        anchor_union = set(M) | set(K) | set(L)

        retaining = tuple(matching for matching in bright
                          if changed_edge in matching)
        omitting = tuple(matching for matching in bright
                         if changed_edge not in matching)
        require(len(retaining) == 15 and len(omitting) == 75,
                "the retaining/omitting matching split changed")

        for rho3 in range(3):
            hybrid = list(PURE_ONE)
            hybrid[3] = rho3
            hybrid[S] = 2
            hybrid = tuple(hybrid)

            # L supplies a nonzero hybrid monomial: its changed-edge cell is
            # the selected cell of N, while every other factor is selected
            # from the pure-one monomial of L.
            l_hybrid = decorated_monomial(L, hybrid)
            l_pure = decorated_monomial(L, PURE_ONE)
            hybrid_changed = decorated_cell(changed_edge, hybrid)
            pure_changed = decorated_cell(changed_edge, PURE_ONE)
            require(l_hybrid - {hybrid_changed}
                    == l_pure - {pure_changed},
                    "the selected L hybrid tail stopped being pure-one")

            # Any other nonzero term retaining the changed edge gives an
            # alternate pure-one monomial after replacing its one common
            # edge cell by the already selected pure L cell.
            for matching in retaining:
                if matching == L:
                    continue
                require(decorated_monomial(matching, hybrid)
                        - {hybrid_changed}
                        == decorated_monomial(matching, PURE_ONE)
                        - {pure_changed},
                        "a retaining mate lost the pure-target replacement")
                retaining_alternates += 1

            for matching in omitting:
                external = set(matching) - anchor_union
                if module.crossed_port(matching):
                    category = "crossed_response"
                elif any(P in pair or S in pair for pair in external):
                    category = "external_endpoint_arm"
                elif any(hybrid[left] != hybrid[right]
                         for left, right in external):
                    category = "external_offdiagonal_q"
                else:
                    category = "M_port_decorated_anchor_residual"
                    require((module.partner(matching, P),
                             module.partner(matching, S)) == (0, 1),
                            "the residual stopped using M's endpoint ports")
                    s_edge = next(pair for pair in matching if S in pair)
                    require(s_edge == module.edge(S, 1)
                            and s_edge in M,
                            "the residual offdiagonal endpoint cell left M")
                category_counts[category] += 1
                by_rho3[(rho3, category)] += 1
                by_record_kind[(record["kind"], rho3, category)] += 1
                examples.setdefault(category, {
                    "record_kind": record["kind"],
                    "rho3": rho3,
                    "M": M, "N": N, "K": K, "L": L,
                    "mate": matching,
                    "external_edges": tuple(sorted(external)),
                    "decorated_cells": tuple(sorted(
                        decorated_cell(pair, hybrid) for pair in matching
                    )),
                })

    require(retaining_alternates == 110 * 3 * 14,
            "the retaining alternate-pure-target count changed")
    require(category_counts == Counter({
        "external_endpoint_arm": 22770,
        "crossed_response": 990,
        "external_offdiagonal_q": 372,
        "M_port_decorated_anchor_residual": 618,
    }), f"the hybrid omitting-mate split changed: {category_counts}")
    require(by_rho3 == Counter({
        (0, "external_endpoint_arm"): 7590,
        (0, "crossed_response"): 330,
        (0, "external_offdiagonal_q"): 186,
        (0, "M_port_decorated_anchor_residual"): 144,
        (1, "external_endpoint_arm"): 7590,
        (1, "crossed_response"): 330,
        (1, "M_port_decorated_anchor_residual"): 330,
        (2, "external_endpoint_arm"): 7590,
        (2, "crossed_response"): 330,
        (2, "external_offdiagonal_q"): 186,
        (2, "M_port_decorated_anchor_residual"): 144,
    }), f"the rho3 hybrid split changed: {by_rho3}")
    require(Counter({
        (kind, rho3): by_record_kind[
            (kind, rho3, "M_port_decorated_anchor_residual")
        ]
        for kind in ("q_only", "Hall", "same_skeleton")
        for rho3 in range(3)
    }) == Counter({
        ("q_only", 0): 58, ("q_only", 1): 144,
        ("q_only", 2): 58,
        ("Hall", 0): 18, ("Hall", 1): 36, ("Hall", 2): 18,
        ("same_skeleton", 0): 68, ("same_skeleton", 1): 150,
        ("same_skeleton", 2): 68,
    }), "the residual source-category split changed")

    canonical = examples["M_port_decorated_anchor_residual"]
    require(canonical["M"] == (
        (0, 6), (1, 7), (2, 3), (4, 5)
    ) and canonical["N"] == (
        (0, 1), (2, 6), (3, 7), (4, 5)
    ) and canonical["mate"] == canonical["M"],
            "the canonical decorated-anchor residual changed")

    return {
        "records": len(records),
        "record_histogram": dict(Counter(
            record["kind"] for record in records
        )),
        "common_ports": {"N": [2, 3], "L": [2, 3], "M": [0, 1]},
        "changed_edge": [3, S],
        "hybrid_words_by_rho3": [
            "11101112", "11111112", "11121112"
        ],
        "retaining_matchings_per_record": 15,
        "alternate_retaining_matchings_checked": retaining_alternates,
        "omitting_matchings_per_record": 75,
        "omitting_mate_counts": dict(category_counts),
        "omitting_mate_counts_by_rho3": {
            str(key): value for key, value in sorted(by_rho3.items())
        },
        "residual_counts_by_source_kind_and_rho3": {
            str((kind, rho3)): by_record_kind[
                (kind, rho3, "M_port_decorated_anchor_residual")
            ]
            for kind in ("q_only", "Hall", "same_skeleton")
            for rho3 in range(3)
        },
        "canonical_residual": canonical,
        "factor_dichotomy": (
            "G_hybrid=x_(S3;rho3,2)*H_(S3)^1+O_(S3).  If O=0, "
            "the hybrid zero row and the localized changed-edge cell force "
            "H=0; the pure-one target row then forces a pure-one matching "
            "omitting S3.  Reselecting it makes N's S3 arm external.  If "
            "O!=0, some omitting mate is nonzero and has one of the four "
            "exhaustively classified forms"
        ),
    }


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def main():
    pin_dependencies()
    module = load_routing()
    all_matchings, bright, records = residual_records(module)
    word_split = audit_actual_mixed_word_split(records)
    hybrid = audit_endpoint_hybrid(module, all_matchings, bright, records)
    ledger = {
        "pins": PINS,
        "literal_d_word_q_only_split": {
            str(key): value for key, value in sorted(word_split.items())
        },
        "endpoint_hybrid": hybrid,
        "theorem": (
            "on all 110 q-only/Hall/same-skeleton records, N and L share "
            "ports P2,S3 and the selected N cell on S3 changes L's endpoint "
            "head from 1 to 2.  The complete hybrid zero row forces either "
            "a pure-one matching omitting S3, an external endpoint arm, a "
            "crossed response matching, an external offdiagonal q cell, or "
            "the single remaining M-port decorated-anchor web"
        ),
        "proof_consequence": (
            "the first four alternatives are existing source-valid routes. "
            "Thus the 98 label-sensitive packets do not require a general "
            "same-skeleton word-change theorem: their only new coefficient "
            "obligation is the M-port residual, where the omitting mate uses "
            "P0,S1, the offdiagonal S1 cell lies on M itself, and every "
            "external residual q cell is diagonal in the hybrid word"
        ),
        "scope": (
            "the checker proves the literal matching partition and the "
            "factor/replacement identities.  It does not assert the final "
            "M-port decorated-anchor bistar is empty; the pinned bistar "
            "artifact records why a nonlinear source correction is needed"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"endpoint-hybrid cancellation ledger changed: {digest}")
    print("h3 target-coloop endpoint-hybrid cancellation: PASS")
    print("q-only d words: offdiagonal 27540 / diagonal 7452")
    print("hybrid domain: q-only 48 / Hall 12 / same-skeleton 50")
    print("omitting mates: endpoint 22770 / crossed 990 / offdiag-q 372 / residual 618")
    print("sole residual: M-port decorated-anchor bistar web")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
