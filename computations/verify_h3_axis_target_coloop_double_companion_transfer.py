#!/usr/bin/env python3
"""Reduce the M-port residual by its two pure-2 endpoint companions.

The first hybrid leaves an active P0:11,S1:21 matching on M's physical
ports.  Comparing each cell with the selected pure-2 M anchor gives two
literal complete rows:

    P companion 12222212,       S companion 21222222.

After the usual complete-cofactor/pure-target split, every avoiding mate is
endpoint-external, crossed, externally offdiagonal in q, or has the old
P2,S3 ports.  This checker classifies both companions simultaneously and
freezes the finite same-tail/C4 return boundary.  It also audits the first
mixed row coupling the two same-tail return decorations.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_axis_target_coloop_second_endpoint_hybrid.py":
        "9a6d826940b76fcb1edf33fb44eba6bfabdeb3797ec08850bd5ac944aafa232f",
    "notes/h3-axis-target-coloop-second-endpoint-hybrid.md":
        "af2dd864b0286bc2fed0aa4c39975d813395910669b3ab0ef308c4e686659745",
    "computations/verify_uniform_one_bad_nonanchor_offdiagonal_good_pair.py":
        "64e85cd84112b5160efe4f43ce1208da3c49f5e58b3e4a4d6192e6a9c229c306",
    "notes/uniform-one-bad-nonanchor-offdiagonal-good-pair.md":
        "4516c5ff02f130e1ad25b4fde395c81557e58ba0c83f7f98969d95df17fd6409",
}
EXPECTED_LEDGER_SHA256 = (
    "17e6f900b44bbbdcaeb46a26d34669ee9d2ec920bb824931aa44340f95bbe6cb"
)

P, S = 6, 7
PURE_TWO = (2,) * 8
P_COMPANION = (1, 2, 2, 2, 2, 2, 1, 2)
S_COMPANION = (2, 1, 2, 2, 2, 2, 2, 2)
RETURN_HYBRID = (2, 1, 2, 2, 2, 2, 1, 2)


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


def offdiagonal_edges(matching, word):
    return tuple(pair for pair in matching
                 if word[pair[0]] != word[pair[1]])


def transfer_matching(routing, tail):
    return tuple(sorted((routing.edge(P, 2), routing.edge(S, 3)) + tail))


def candidate_route(routing, candidate, word, union, through_edge):
    if routing.edge(P, S) in candidate:
        return "direct_PS_forbidden"
    if through_edge in candidate:
        return "through"
    external = set(candidate) - union
    ports = (routing.partner(candidate, P), routing.partner(candidate, S))
    if ports in ((2, 1), (0, 3)):
        return "crossed"
    if any(P in pair or S in pair for pair in external):
        return "endpoint"
    if any(word[left] != word[right] for left, right in external):
        return "offdiagonal_q"
    require(ports == (2, 3),
            "an internal companion return lost ports P2,S3")
    return "return"


def audit_double_companion():
    second = load(
        "computations/verify_h3_axis_target_coloop_second_endpoint_hybrid.py",
        "target_coloop_second_hybrid_dependency",
    )
    first = load(
        "computations/verify_h3_axis_target_coloop_endpoint_hybrid_cancellation.py",
        "target_coloop_first_hybrid_dependency",
    )
    routing = load(
        "computations/verify_h3_axis_target_coloop_other_bright_matching_routing.py",
        "target_coloop_matching_routing_dependency",
    )
    all_matchings, _bright, residuals, source_histogram = (
        second.reconstruct_first_residuals(first, routing)
    )
    require(len(residuals) == 618, "the first M-port residual count changed")

    residual_tails = tuple(routing.perfect_matchings((0, 1, 4, 5)))
    route_counts = Counter()
    return_counts = Counter()
    pair_counts = Counter()
    same_identity = Counter()
    hybrid_mate_counts = Counter()
    canonical = None

    for residual in residuals:
        M, K, L, B = (residual[key] for key in ("M", "K", "L", "B"))
        union = set(M) | set(K) | set(L)
        p_edge = routing.edge(P, 0)
        s_edge = routing.edge(S, 1)
        require(p_edge in M and s_edge in M and p_edge in B and s_edge in B,
                "the first residual lost M's two physical endpoint edges")

        # B supplies P0:11 and S1:21.  Off the selected endpoint edge, the
        # corresponding companion monomial uses only selected pure-2 M cells.
        for side, word, changed in (
                ("P", P_COMPANION, p_edge),
                ("S", S_COMPANION, s_edge)):
            active_cell = decorated_cell(changed, word)
            pure_cell = decorated_cell(changed, PURE_TWO)
            require(decorated_monomial(M, word) - {active_cell}
                    == decorated_monomial(M, PURE_TWO) - {pure_cell},
                    f"the {side} companion tail stopped being pure 2")
            if side == "P":
                require(active_cell[1] == (1, 1),
                        "the P0 companion lost cell 11")
            else:
                require(active_cell[1] == (1, 2),
                        "the S1 companion lost the oriented 21 cell")

        internal = {}
        for side, word, changed in (
                ("P", P_COMPANION, p_edge),
                ("S", S_COMPANION, s_edge)):
            internal[side] = []
            for candidate in all_matchings:
                route = candidate_route(
                    routing, candidate, word, union, changed
                )
                if route in {"through", "direct_PS_forbidden"}:
                    continue
                route_counts[(side, route)] += 1
                if route == "return":
                    require((routing.partner(candidate, P),
                             routing.partner(candidate, S)) == (2, 3),
                            "a return lost L's endpoint ports")
                    tail = tuple(pair for pair in candidate
                                 if P not in pair and S not in pair)
                    require(tail in residual_tails,
                            "a return tail stopped being a K4 matching")
                    internal[side].append(tail)
            return_counts[(residual["source_kind"], residual["rho3"],
                           side, len(internal[side]))] += 1

        for p_tail in internal["P"]:
            for s_tail in internal["S"]:
                form = "same_tail" if p_tail == s_tail else "residual_C4"
                if form == "residual_C4":
                    require(routing.cycle_lengths(p_tail, s_tail) == (4,),
                            "two distinct K4 return tails stopped being one C4")
                pair_counts[(residual["source_kind"], residual["rho3"],
                             form)] += 1
                if form != "same_tail":
                    continue

                transfer = transfer_matching(routing, p_tail)
                same_identity["equals_L" if transfer == L
                              else "distinct_same_tail"] += 1

                # Use P2:12 from the P return and every other edge from the
                # S return.  Disjoint matching edges make this the literal
                # word 21222212 on the same physical skeleton.
                p_changed = decorated_cell(routing.edge(P, 2), P_COMPANION)
                hybrid = (decorated_monomial(transfer, S_COMPANION)
                          - {decorated_cell(routing.edge(P, 2), S_COMPANION)})
                hybrid = hybrid | {p_changed}
                require(hybrid == decorated_monomial(transfer, RETURN_HYBRID),
                        "the two returns stopped forming one literal hybrid")

                for mate in all_matchings:
                    if mate == transfer or routing.edge(P, S) in mate:
                        continue
                    external = set(mate) - union
                    ports = (routing.partner(mate, P),
                             routing.partner(mate, S))
                    if ports in ((2, 1), (0, 3)):
                        kind = "crossed"
                    elif any(P in pair or S in pair for pair in external):
                        kind = "endpoint"
                    elif any(RETURN_HYBRID[left] != RETURN_HYBRID[right]
                             for left, right in external):
                        kind = "offdiagonal_q"
                    elif mate == M:
                        kind = "M_crossed_label"
                        m_cells = decorated_monomial(M, RETURN_HYBRID)
                        missing = m_cells - decorated_monomial(M, S_COMPANION)
                        require(missing == {
                            decorated_cell(p_edge, RETURN_HYBRID)
                        }, "the M mate needs more than the P0:12 cell")
                    elif set(mate) <= union:
                        kind = "Hall"
                    else:
                        kind = "diagonal_q"
                    hybrid_mate_counts[kind] += 1

                if canonical is None and transfer == L:
                    canonical = {
                        "source_kind": residual["source_kind"],
                        "rho3": residual["rho3"],
                        "M": M, "K": K, "L": L, "first_mate_B": B,
                        "P_return": transfer, "S_return": transfer,
                        "return_hybrid_word": "21222212",
                        "M_mate_new_cell": decorated_cell(
                            p_edge, RETURN_HYBRID
                        ),
                    }

    require(route_counts == Counter({
        ("P", "endpoint"): 42642,
        ("P", "crossed"): 1854,
        ("P", "offdiagonal_q"): 1002,
        ("P", "return"): 852,
        ("S", "endpoint"): 42642,
        ("S", "crossed"): 1854,
        ("S", "offdiagonal_q"): 994,
        ("S", "return"): 860,
    }), f"the double-companion route counts changed: {route_counts}")
    require(sum(pair_counts.values()) == 1288,
            "the simultaneous return-pair count changed")
    require(sum(value for key, value in pair_counts.items()
                if key[-1] == "same_tail") == 812,
            "the same-tail return count changed")
    require(sum(value for key, value in pair_counts.items()
                if key[-1] == "residual_C4") == 476,
            "the residual-C4 return count changed")
    require(same_identity == Counter({
        "equals_L": 618, "distinct_same_tail": 194,
    }), f"the same-tail identity split changed: {same_identity}")
    require(hybrid_mate_counts == Counter({
        "endpoint": 63336,
        "crossed": 4872,
        "offdiagonal_q": 1188,
        "M_crossed_label": 812,
        "Hall": 606,
        "diagonal_q": 1454,
    }), f"the return-hybrid mate split changed: {hybrid_mate_counts}")

    return {
        "first_M_port_residuals": len(residuals),
        "source_histogram": {
            str(key): value for key, value in sorted(source_histogram.items())
        },
        "companion_words": {
            "P0_11_vs_22": "12222212",
            "S1_21_vs_22": "21222222",
        },
        "avoiding_route_counts": {
            str(key): value for key, value in sorted(route_counts.items())
        },
        "return_profile_counts": {
            str(key): value for key, value in sorted(return_counts.items())
        },
        "simultaneous_return_pairs": {
            "total": sum(pair_counts.values()),
            "same_tail": 812,
            "residual_C4": 476,
            "by_source_and_rho": {
                str(key): value for key, value in sorted(pair_counts.items())
            },
        },
        "same_tail_identity": dict(sorted(same_identity.items())),
        "return_hybrid": {
            "word": "21222212",
            "mate_routes": dict(sorted(hybrid_mate_counts.items())),
            "canonical": canonical,
        },
    }


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def main():
    pin_dependencies()
    audit = audit_double_companion()
    ledger = {
        "pins": PINS,
        "double_companion_transfer": audit,
        "theorem": (
            "the P0:11 and S1:21 cells in every M-port residual have two "
            "literal pure-2 companion rows.  Unless a pure-2 anchor "
            "reselects away from the relevant M edge, each row routes to "
            "an external endpoint, crossed matching, external offdiagonal "
            "q cell, or a P2,S3 return.  Simultaneous internal returns have "
            "only the same-tail or one-C4 forms"
        ),
        "progress_guard": (
            "618 same-tail return pairs use exactly the old L skeleton, so "
            "physical-edge support does not strictly increase.  The mixed "
            "hybrid of the two return decorations is the literal zero word "
            "21222212 and forces a distinct mate.  If that mate is M, its "
            "only new factor is P0:12, completing the crossed-label "
            "P0:12,S1:21 M monomial"
        ),
        "scope": (
            "exact full-row/matching classification.  The 606 Hall and "
            "1454 diagonal-q alternatives in the final hybrid are retained; "
            "this theorem narrows but does not declare the affine return empty"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"double-companion ledger changed: {digest}")
    print("h3 target-coloop double companion transfer: PASS")
    print("P return 852 / S return 860")
    print("simultaneous returns: same-tail 812 / residual-C4 476")
    print("same-tail old-L self-return: 618")
    print("next literal hybrid 21222212; M mate needs only P0:12")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
