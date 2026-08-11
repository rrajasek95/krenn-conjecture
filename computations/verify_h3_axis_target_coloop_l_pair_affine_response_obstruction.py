#!/usr/bin/env python3
"""Resolve the two L-edge avoiding sums to one typed affine response row.

The final rainbow mate has word 00112200 and matching

    PS | L_qtail(02,02) | 23:11.

The two off-diagonal cells lie on the two q-tail edges of the pure-one
anchor L.  This checker writes their complete decorated-edge avoiding
rows, then couples both cells in the literal p1s1 companion 00112211.
All but three companion matching types route immediately.  The remaining
row is an affine two-port block; its opposite R21 component is absent
because the literal P2:21 endpoint cell is not selected.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_axis_target_coloop_four_diagonal_switch_five_lock.py":
        "840d86b74a2de2b36b9f8ec5e6a02c9042b0767f040261d887d1c82b64929d7f",
    "notes/h3-axis-target-coloop-four-diagonal-switch-five-lock.md":
        "4e7e9c515384a6464a3a3faa942740790b99551a4e40bf8183e1606b368021f3",
    "computations/verify_uniform_decorated_anchor_mixed_word_exchange.py":
        "150bf15eb8ac475f866c062afcd7e3002477d02338acdb082c14f9136a3e58b7",
    "notes/uniform-decorated-anchor-mixed-word-exchange.md":
        "0cdc391bebb44150c7941bdbeec853029929f20d46ee813eb2a09bb76c27a5de",
    "computations/verify_uniform_five_lock_wedge_or_switch.py":
        "c2541a60db1f8e7a661bc698d2bd1f1a1f396a0f0bfde389ea89bea17fac175e",
    "notes/uniform-five-lock-wedge-or-switch.md":
        "0871d5151a0fdb46fee0c9b15797a864e579a85c360a2638d458583479426914",
}
EXPECTED_LEDGER_SHA256 = (
    "fb44fd739a4a334be410ffe12b578d1cebc175abafb6ef65aade7ffd9c8088d3"
)

P, S = 6, 7
PURE_ONE = (1,) * 8
RAINBOW_WORD = (0, 0, 1, 1, 2, 2)
COMPANION_11 = RAINBOW_WORD + (1, 1)
COMPANION_12 = RAINBOW_WORD + (1, 2)
COMPANION_21 = RAINBOW_WORD + (2, 1)


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


def decorated_monomial(matching, word):
    return frozenset(
        (edge, (word[edge[0]], word[edge[1]])) for edge in matching
    )


def boundary_records(top, second, first, routing):
    _, returns = top.reconstruct_returns(second, first, routing)
    q_matchings = tuple(routing.perfect_matchings(range(6)))
    boundary = []
    for residual, candidate in returns:
        _, _, cells = top.selected_q_support(second, residual, candidate)
        rows = top.supported_top_rows(q_matchings, cells)
        private = [
            (word, monomials[0]) for word, monomials in rows.items()
            if word != (0,) * 6 and len(monomials) == 1
        ]
        if not private:
            continue
        if all(any(
                frozenset(matching)
                != frozenset(edge for edge, _ in monomial)
                and all(word[left] == word[right]
                        for left, right in matching)
                for matching in q_matchings)
                for word, monomial in private):
            boundary.append((residual, candidate))
    require(len(boundary) == 4,
            f"the sharp boundary count changed: {len(boundary)}")
    return tuple(boundary)


def audit():
    top = load(
        "computations/verify_h3_axis_target_coloop_return_common_q_top_companion.py",
        "return_top_companion_dependency",
    )
    four = load(
        "computations/verify_h3_axis_target_coloop_four_diagonal_switch_five_lock.py",
        "four_diagonal_switch_dependency",
    )
    second = load(
        "computations/verify_h3_axis_target_coloop_second_endpoint_hybrid.py",
        "second_endpoint_hybrid_dependency",
    )
    first = load(
        "computations/verify_h3_axis_target_coloop_endpoint_hybrid_cancellation.py",
        "first_endpoint_hybrid_dependency",
    )
    routing = load(
        "computations/verify_h3_axis_target_coloop_other_bright_matching_routing.py",
        "target_coloop_routing_dependency",
    )
    records = boundary_records(top, second, first, routing)
    all_matchings = tuple(routing.perfect_matchings(range(8)))
    bright = tuple(matching for matching in all_matchings
                   if routing.edge(P, S) not in matching)

    exchange_words = Counter()
    exchange_partitions = Counter()
    companion_routes = Counter()
    internal_types = Counter()
    cofactor_terms = Counter()
    endpoint_types = Counter()
    representative = None

    for residual, candidate in records:
        L = residual["L"]
        M = residual["M"]
        K = residual["K"]
        l_tail = tuple(edge for edge in L if P not in edge and S not in edge)
        require(len(l_tail) == 2
                and all((RAINBOW_WORD[left], RAINBOW_WORD[right]) == (0, 2)
                        for left, right in l_tail),
                "the affine residual left the two 02-labelled L edges")

        # Write the two complete decorated-edge rows.  Each selected through
        # term is q_e^02 times the literal pure-one L cofactor.
        exchange_data = []
        for edge in l_tail:
            word = list(PURE_ONE)
            word[edge[0]] = RAINBOW_WORD[edge[0]]
            word[edge[1]] = RAINBOW_WORD[edge[1]]
            word = tuple(word)
            through = tuple(matching for matching in all_matchings
                            if edge in matching)
            avoiding = tuple(matching for matching in all_matchings
                             if edge not in matching)
            require(len(through) == 15 and len(avoiding) == 90,
                    "a decorated-edge through/avoiding split changed")
            require(L in through,
                    "the selected pure-one L cofactor left its through row")
            l_term = decorated_monomial(L, word)
            edge_cell = (edge, (0, 2))
            pure_cofactor = l_term - {edge_cell}
            require(edge_cell in l_term and len(pure_cofactor) == 3,
                    "the selected exchange cofactor changed")
            exchange_words["".join(map(str, word))] += 1
            exchange_partitions[(len(through), len(avoiding))] += 1
            exchange_data.append({
                "edge": edge,
                "word": "".join(map(str, word)),
                "selected_cell": edge_cell,
                "selected_pure_one_cofactor": tuple(sorted(pure_cofactor)),
                "identity": "0=q_e^02*C_e^1+R_e",
            })

        # The common literal companion uses both 02 cells and the selected
        # p1@2,s1@3 endpoint cells on L.
        selected_companion = decorated_monomial(L, COMPANION_11)
        require(all((edge, (0, 2)) in selected_companion for edge in l_tail),
                "the p1s1 companion lost an off-diagonal L-tail cell")
        anchor_union = set(K) | set(L) | set(M)
        internal = []
        for matching in bright:
            if matching == L:
                continue
            external = set(matching) - anchor_union
            offdiagonal = tuple(
                edge for edge in matching
                if COMPANION_11[edge[0]] != COMPANION_11[edge[1]]
            )
            if any(P in edge or S in edge for edge in external):
                route = "external_endpoint"
            elif any(edge not in anchor_union for edge in offdiagonal):
                route = "external_offdiagonal_q"
            else:
                route = "internal_affine_block"
                internal.append(matching)
            companion_routes[route] += 1

        require(len(internal) == 3,
                "the common p1s1 companion stopped having three internal mates")
        l_ports = tuple(sorted((routing.edge(P, 2), routing.edge(S, 3))))
        m_ports = tuple(sorted((routing.edge(P, 0), routing.edge(S, 1))))
        expected_l_affine = tuple(sorted(l_ports + (
            routing.edge(0, 1), routing.edge(4, 5)
        )))
        expected_m_tail = tuple(sorted(m_ports + (
            routing.edge(2, 3), routing.edge(4, 5)
        )))
        for matching in internal:
            if matching == M:
                kind = "M_skeleton_mixed"
            elif matching == expected_l_affine:
                kind = "L_ports_diagonal_affine_tail"
            elif matching == expected_m_tail:
                kind = "M_ports_diagonal_tail"
            else:
                raise RuntimeError(f"unknown internal companion mate: {matching}")
            internal_types[kind] += 1

        # On the L-port block the response coefficient factors through the
        # complete q^[2] cofactor on sites 0,1,4,5.
        hole_matchings = tuple(routing.perfect_matchings((0, 1, 4, 5)))
        require(set(hole_matchings) == {
            ((0, 1), (4, 5)), ((0, 4), (1, 5)), ((0, 5), (1, 4)),
        }, "the four-hole cofactor matching set changed")
        for matching in hole_matchings:
            labels = tuple(
                (edge, (RAINBOW_WORD[edge[0]], RAINBOW_WORD[edge[1]]))
                for edge in matching
            )
            if matching == ((0, 5), (1, 4)):
                kind = "selected_L_tail"
            elif matching == ((0, 4), (1, 5)):
                kind = "external_offdiagonal_tail"
            else:
                kind = "diagonal_affine_tail"
            cofactor_terms[kind] += 1
            require(len(labels) == 2, "a q^[2] cofactor term changed")

        # R11 and R12 share the selected L ports.  R21 would require the
        # absent literal endpoint component P2:21.
        first_word, _, _ = top.selected_q_support(second, residual, candidate)
        p_support, s_support = four.selected_endpoint_support(
            second, residual, candidate, first_word
        )
        require((1, 2, 1) in p_support and (1, 3, 1) in s_support
                and (2, 3, 1) in s_support,
                "the selected R11/R12 L-port factors changed")
        require((2, 2, 1) not in p_support,
                "the missing opposite P2:21 component became selected")
        endpoint_types["R11_selected"] += 1
        endpoint_types["R12_selected"] += 1
        endpoint_types["R21_missing_P2_21"] += 1

        if representative is None:
            representative = {
                "M": M, "K": K, "L": L,
                "rainbow_top_word": "00112200",
                "rainbow_matching": tuple(sorted((routing.edge(P, S),
                                                   *l_tail,
                                                   routing.edge(2, 3)))),
                "exchange_rows": exchange_data,
                "common_companion_word": "00112211",
                "internal_companion_mates": internal,
                "missing_opposite_component": "P2:21",
            }

    require(exchange_partitions == Counter({(15, 90): 8}),
            f"the exchange partitions changed: {exchange_partitions}")
    require(companion_routes == Counter({
        "external_endpoint": 312,
        "external_offdiagonal_q": 32,
        "internal_affine_block": 12,
    }), f"the common companion route split changed: {companion_routes}")
    require(internal_types == Counter({
        "L_ports_diagonal_affine_tail": 4,
        "M_ports_diagonal_tail": 4,
        "M_skeleton_mixed": 4,
    }), f"the internal affine types changed: {internal_types}")
    require(cofactor_terms == Counter({
        "selected_L_tail": 4,
        "external_offdiagonal_tail": 4,
        "diagonal_affine_tail": 4,
    }), f"the L-port cofactor terms changed: {cofactor_terms}")

    ledger = {
        "records": len(records),
        "decorated_edge_exchange_words": dict(sorted(exchange_words.items())),
        "exchange_partition_per_edge": {"through": 15, "avoiding": 90},
        "common_companion_word": "00112211",
        "common_companion_route_counts": dict(sorted(companion_routes.items())),
        "internal_affine_types": dict(sorted(internal_types.items())),
        "L_port_q2_cofactor": {
            "formula": (
                "C23=x01^00*x45^22+x04^02*x15^02+"
                "x05^02*x14^02"
            ),
            "term_types": dict(sorted(cofactor_terms.items())),
        },
        "endpoint_type_obstruction": {
            "R11": "selected on P2,S3",
            "R12": "selected on P2,S3",
            "R21": "missing literal endpoint cell P2:21",
            "five_lock_consequence": (
                "no opposite crossed face on the same L-port q2 cofactor"
            ),
        },
        "representative": representative,
        "conclusion": (
            "The two decorated-edge avoiding aggregates are coupled by the "
            "literal p1s1 companion 00112211.  External terms route, but "
            "three internal port/tail types remain.  On the L-port block "
            "the exact E2 cofactor is selected+external+diagonal-affine. "
            "The external term routes; the diagonal term is a genuine "
            "affine return.  R12 is present but the opposite R21 face needs "
            "the absent P2:21 component, so the five-lock theorem cannot "
            "synchronize the block from the proved inputs."
        ),
    }
    digest = sha256(
        json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return ledger, digest


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def main():
    pin_dependencies()
    ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the frozen L-pair affine ledger changed: {digest}")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")
    print("h3 target-coloop L-pair affine response obstruction: PASS")


if __name__ == "__main__":
    main()
