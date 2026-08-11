#!/usr/bin/env python3
"""Close the crossed-label M branch by its target-augmented private row.

The double-companion transfer can return to the pure-two matching M and
force the literal cell P0:12.  At the frozen carrier support the four
response coefficients over residual word 212222 have profile (0,2,0,2):
the p1s2 and p2s2 rows each have the M and return terms, while the p1s1
and opposite p2s1 rows are empty.  Thus an opposite crossed row is not a
consequence of that fine coefficient.

The new cell P0:12 nevertheless occurs with the pure-two M cofactor in the
target-augmented private word 22222212.  Splitting this complete row into
matchings through and avoiding P0 proves a uniform closure: either the
pure-two target reselects away from P0, or an avoiding term is external,
crossed, or has P2,S3 ports and itself becomes a pure-two matching after
P2:12 is replaced by the already selected P2:22 cell.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_axis_target_coloop_double_companion_transfer.py":
        "94eaf974b2224221d59d05d99ef8cadb03908ee8f3734c28549650c9c026193c",
    "notes/h3-axis-target-coloop-double-companion-transfer.md":
        "914456b7ebe0f58d148b16fbaeb3666bd3fc85e33b2746892523c66ee7b69761",
    "computations/verify_uniform_target_augmented_private_site_active_minor.py":
        "c53ba30dd8b7084cc27e05f11aa6066354fdec45ff2cf72ebdfb85bb8517169b",
    "notes/uniform-target-augmented-private-site-active-minor.md":
        "d7b16ecbb867524615ecf3034e0911e0add34825a7f9088f369f3a11e1c61f0d",
    "computations/verify_uniform_one_bad_nonanchor_offdiagonal_good_pair.py":
        "64e85cd84112b5160efe4f43ce1208da3c49f5e58b3e4a4d6192e6a9c229c306",
    "notes/uniform-one-bad-nonanchor-offdiagonal-good-pair.md":
        "4516c5ff02f130e1ad25b4fde395c81557e58ba0c83f7f98969d95df17fd6409",
    "computations/verify_h3_axis_target_coloop_return_common_q_top_companion.py":
        "6ad4388d645c7bd25fc5359b22798dff953579b2e0923c7317425bb7973e5664",
    "notes/h3-axis-target-coloop-return-common-q-top-companion.md":
        "136e24f8f57cfc14b0b23385bf951e132d3c4f29910ebbf8bdeb91a6ec772847",
}
EXPECTED_LEDGER_SHA256 = (
    "5f916eb3033b77a82328a1fd989d8f56fb77cbbb38c320d7489dc9212e0f85e7"
)

P, S = 6, 7
PURE_ZERO = (0,) * 8
PURE_ONE = (1,) * 8
PURE_TWO = (2,) * 8
RESIDUAL_WORD = (2, 1, 2, 2, 2, 2)
P_PRIVATE_WORD = (2, 2, 2, 2, 2, 2, 1, 2)


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


def same_tail_states(double, second, first, routing):
    all_matchings, bright, residuals, _ = second.reconstruct_first_residuals(
        first, routing
    )
    states = []
    for residual in residuals:
        M, K, L = (residual[key] for key in ("M", "K", "L"))
        union = set(M) | set(K) | set(L)
        internal = {}
        for side, word, changed in (
                ("P", double.P_COMPANION, routing.edge(P, 0)),
                ("S", double.S_COMPANION, routing.edge(S, 1))):
            tails = []
            for matching in all_matchings:
                route = double.candidate_route(
                    routing, matching, word, union, changed
                )
                if route == "return":
                    tails.append(tuple(edge for edge in matching
                                       if P not in edge and S not in edge))
            internal[side] = tuple(tails)
        for tail in set(internal["P"]) & set(internal["S"]):
            transfer = double.transfer_matching(routing, tail)
            states.append((residual, transfer))
    require(len(states) == 812,
            f"the same-tail state count changed: {len(states)}")
    return tuple(all_matchings), tuple(bright), tuple(states)


def selected_support(double, routing, residual, transfer):
    M, K, L, B = (residual[key] for key in ("M", "K", "L", "B"))
    first_word = [1] * 8
    first_word[3] = residual["rho3"]
    first_word[S] = 2
    first_word = tuple(first_word)
    support = set(decorated_monomial(M, PURE_TWO))
    support.update(decorated_monomial(K, PURE_ZERO))
    support.update(decorated_monomial(L, PURE_ONE))
    support.update(decorated_monomial(B, first_word))
    support.update(decorated_monomial(transfer, double.P_COMPANION))
    support.update(decorated_monomial(transfer, double.S_COMPANION))
    support.add(decorated_cell(routing.edge(P, 0), double.RETURN_HYBRID))
    return support


def audit_five_rows(double, second, first, routing):
    all_matchings, bright, states = same_tail_states(
        double, second, first, routing
    )
    profiles = Counter()
    private_initial = Counter()
    examples = {}

    for residual, transfer in states:
        support = selected_support(double, routing, residual, transfer)
        M = residual["M"]
        counts = []
        supported_by_row = {}
        for p_colour, s_colour in ((1, 1), (1, 2), (2, 1), (2, 2)):
            word = RESIDUAL_WORD + (p_colour, s_colour)
            supported = tuple(
                matching for matching in bright
                if decorated_monomial(matching, word) <= support
            )
            counts.append(len(supported))
            supported_by_row[(p_colour, s_colour)] = supported
        profiles[tuple(counts)] += 1
        require(set(supported_by_row[(1, 2)]) == {M, transfer}
                and set(supported_by_row[(2, 2)]) == {M, transfer},
                "the two supported response rows lost their M/return pair")
        require(not supported_by_row[(1, 1)]
                and not supported_by_row[(2, 1)],
                "an opposite-s1 term entered the frozen carrier support")

        private_supported = tuple(
            matching for matching in bright
            if decorated_monomial(matching, P_PRIVATE_WORD) <= support
        )
        private_initial[len(private_supported)] += 1
        require(M in private_supported and len(private_supported) in (1, 2),
                "the private row lost M or acquired more than one old mate")
        if len(private_supported) == 2:
            avoiding = next(matching for matching in private_supported
                            if matching != M)
            require(routing.edge(P, 0) not in avoiding
                    and (routing.partner(avoiding, P),
                         routing.partner(avoiding, S)) == (2, 3),
                    "the old private-row mate stopped being a P2,S3 return")
        examples.setdefault(len(private_supported), {
            "M": M,
            "transfer": transfer,
            "private_supported": private_supported,
        })

    require(profiles == Counter({(0, 2, 0, 2): 812}),
            f"the four-response carrier profile changed: {profiles}")
    require(private_initial == Counter({1: 392, 2: 420}),
            f"the initial private-row profile changed: {private_initial}")
    return all_matchings, bright, states, {
        "same_tail_states": len(states),
        "row_order": ["p1s1", "p1s2", "p2s1", "p2s2"],
        "frozen_carrier_profile": {
            str(key): value for key, value in sorted(profiles.items())
        },
        "p_private_word": "22222212",
        "private_row_old_term_count": dict(sorted(private_initial.items())),
        "examples": examples,
    }


def audit_complete_private_row(routing, bright, states):
    route_counts = Counter()
    retaining_alternates = 0
    examples = {}
    for residual, transfer in states:
        M, K, L = (residual[key] for key in ("M", "K", "L"))
        union = set(M) | set(K) | set(L)
        changed = routing.edge(P, 0)
        require(changed in M and changed not in K and changed not in L,
                "P0 stopped being unique to the pure-two anchor")
        require(decorated_cell(changed, P_PRIVATE_WORD)[1] == (2, 1),
                "the private P0:12 orientation changed")

        retaining = tuple(matching for matching in bright
                          if changed in matching)
        omitting = tuple(matching for matching in bright
                         if changed not in matching)
        require(len(retaining) == 15 and len(omitting) == 75,
                "the private-row retaining/omitting split changed")
        for matching in retaining:
            if matching == M:
                continue
            mixed = decorated_monomial(matching, P_PRIVATE_WORD)
            pure = decorated_monomial(matching, PURE_TWO)
            require(mixed - {decorated_cell(changed, P_PRIVATE_WORD)}
                    == pure - {decorated_cell(changed, PURE_TWO)},
                    "a through-P0 term lost its pure-two replacement")
            retaining_alternates += 1

        for matching in omitting:
            external = set(matching) - union
            ports = (routing.partner(matching, P),
                     routing.partner(matching, S))
            p_edge = routing.edge(P, ports[0])
            s_edge = routing.edge(S, ports[1])
            if p_edge in external:
                route = "external_P_offdiagonal"
            elif ports[0] == 2 and s_edge in external:
                route = "P2_external_S_pure_two_reselection"
            elif ports == (2, 1):
                route = "crossed_P2_S1"
            else:
                require(ports == (2, 3),
                        "an internal avoiding term lost P2,S3 ports")
                route = "pure_two_reselection"
                p2 = routing.edge(P, 2)
                require(decorated_cell(p2, PURE_TWO)
                        in decorated_monomial(
                            transfer, (2, 1, 2, 2, 2, 2, 2, 2)
                        ),
                        "the selected P2:22 cell disappeared")
                mixed = decorated_monomial(matching, P_PRIVATE_WORD)
                pure = decorated_monomial(matching, PURE_TWO)
                require(mixed - {decorated_cell(p2, P_PRIVATE_WORD)}
                        == pure - {decorated_cell(p2, PURE_TWO)},
                        "the P2,S3 return lost its pure-two replacement")
            route_counts[route] += 1
            examples.setdefault(route, {
                "M": M, "K": K, "L": L,
                "candidate": matching,
                "ports": ports,
                "external": tuple(sorted(external)),
            })

    require(retaining_alternates == 812 * 14,
            "the through-P0 alternate count changed")
    require(route_counts == Counter({
        "external_P_offdiagonal": 48720,
        "P2_external_S_pure_two_reselection": 7308,
        "crossed_P2_S1": 2436,
        "pure_two_reselection": 2436,
    }), f"the complete private-row routes changed: {route_counts}")
    return {
        "retaining_alternates": retaining_alternates,
        "omitting_routes": dict(sorted(route_counts.items())),
        "examples": examples,
        "factor_split": (
            "0=P0:12*H_P0^2+O.  If O=0 then H_P0^2=0 and the "
            "pure-two target supplies an avoiding matching.  If O!=0, "
            "an avoiding monomial has an external offdiagonal P arm, is "
            "crossed P2,S1, or has P2 and an external/P3 S arm.  In every "
            "P2 case except the crossed one, replacing active P2:12 by "
            "active P2:22 gives a pure-two matching avoiding P0"
        ),
    }


def audit_four_diagonal_specialization(double, second, first, routing):
    top = load(
        "computations/verify_h3_axis_target_coloop_return_common_q_top_companion.py",
        "return_top_companion_dependency",
    )
    _, returns = top.reconstruct_returns(second, first, routing)
    q_matchings = tuple(routing.perfect_matchings(range(6)))
    bright = tuple(matching for matching in routing.perfect_matchings(range(8))
                   if routing.edge(P, S) not in matching)
    boundary = []
    profiles = Counter()
    private_profiles = Counter()
    direct_reselections = 0
    examples = []

    for residual, candidate in returns:
        first_word, _, q_support = top.selected_q_support(
            second, residual, candidate
        )
        rows = top.supported_top_rows(q_matchings, q_support)
        private = [
            (word, monomials[0])
            for word, monomials in rows.items()
            if word != (0,) * 6 and len(monomials) == 1
        ]
        if not private:
            continue
        diagonal_counts = []
        for word, monomial in private:
            selected = frozenset(edge for edge, _ in monomial)
            diagonal_counts.append(sum(
                1 for matching in q_matchings
                if frozenset(matching) != selected
                and all(word[left] == word[right]
                        for left, right in matching)
            ))
        if not (len(private) == 4 and diagonal_counts == [2, 2, 2, 2]):
            continue

        boundary.append((residual, candidate))
        support = set(decorated_monomial(residual["M"], PURE_TWO))
        support.update(decorated_monomial(residual["K"], PURE_ZERO))
        support.update(decorated_monomial(residual["L"], PURE_ONE))
        support.update(decorated_monomial(residual["B"], first_word))
        support.update(decorated_monomial(residual["N"], first_word))
        support.update(decorated_monomial(candidate, second.SECOND_HYBRID))

        # Specializing the crossed-M branch includes the same physical C
        # matching in the S companion and the newly forced P0:12 cell.
        support.update(decorated_monomial(candidate, double.S_COMPANION))
        support.add(decorated_cell(routing.edge(P, 0),
                                   double.RETURN_HYBRID))
        counts = []
        supported_rows = {}
        for p_colour, s_colour in ((1, 1), (1, 2), (2, 1), (2, 2)):
            word = RESIDUAL_WORD + (p_colour, s_colour)
            supported = tuple(
                matching for matching in bright
                if decorated_monomial(matching, word) <= support
            )
            counts.append(len(supported))
            supported_rows[(p_colour, s_colour)] = supported
        profiles[tuple(counts)] += 1
        require(set(supported_rows[(1, 2)])
                == {residual["M"], candidate}
                and set(supported_rows[(2, 2)])
                == {residual["M"], candidate}
                and not supported_rows[(1, 1)]
                and not supported_rows[(2, 1)],
                "a diagonal packet lost the literal two-row profile")

        private_supported = tuple(
            matching for matching in bright
            if decorated_monomial(matching, P_PRIVATE_WORD) <= support
        )
        private_profiles[len(private_supported)] += 1
        require(set(private_supported) == {residual["M"], candidate},
                "the diagonal packet private row lost its M/C pair")
        p2 = routing.edge(P, 2)
        require(decorated_monomial(candidate, P_PRIVATE_WORD)
                - {decorated_cell(p2, P_PRIVATE_WORD)}
                == decorated_monomial(candidate, PURE_TWO)
                - {decorated_cell(p2, PURE_TWO)}
                and decorated_cell(p2, PURE_TWO) in support,
                "the diagonal C mate stopped giving a pure-two reselection")
        direct_reselections += 1
        examples.append({
            "source_kind": residual["source_kind"],
            "rho3": residual["rho3"],
            "M": residual["M"], "C": candidate,
            "response_profile": tuple(counts),
            "P_private_matchings": private_supported,
        })

    require(len(boundary) == 4,
            f"the sharp diagonal packet count changed: {len(boundary)}")
    require(profiles == Counter({(0, 2, 0, 2): 4})
            and private_profiles == Counter({2: 4})
            and direct_reselections == 4,
            "the four-packet crossed-M specialization changed")
    return {
        "records": len(boundary),
        "response_profile": {str(key): value
                             for key, value in sorted(profiles.items())},
        "opposite_p2s1_terms": 0,
        "P_private_terms_per_record": 2,
        "direct_pure_two_C_reselections": direct_reselections,
        "examples": examples,
        "conclusion": (
            "on every sharp diagonal packet the crossed-M specialization "
            "has M and C in p1s2 and p2s2, no p1s1/p2s1 term, and M/C "
            "again in the private word 22222212.  Replacing C's P2:12 by "
            "its selected S-companion P2:22 makes C itself a pure-two "
            "matching avoiding P0.  Hence no multiplicative relation is "
            "missing from the rank-two deletion lock: this branch leaves "
            "that boundary by direct target reselection"
        ),
    }


def audit_final_alternative_ports(double, routing, all_matchings, states):
    counts = Counter()
    for residual, transfer in states:
        M, K, L = (residual[key] for key in ("M", "K", "L"))
        union = set(M) | set(K) | set(L)
        for mate in all_matchings:
            if mate == transfer or routing.edge(P, S) in mate:
                continue
            external = set(mate) - union
            ports = (routing.partner(mate, P), routing.partner(mate, S))
            if ports in ((2, 1), (0, 3)):
                kind = "crossed"
            elif any(P in edge or S in edge for edge in external):
                kind = "endpoint"
            elif any(double.RETURN_HYBRID[left]
                     != double.RETURN_HYBRID[right]
                     for left, right in external):
                kind = "offdiagonal_q"
            elif mate == M:
                kind = "M"
            elif set(mate) <= union:
                kind = "Hall"
            else:
                kind = "diagonal_q"
            if kind in {"M", "Hall", "diagonal_q"}:
                counts[(kind, ports)] += 1

    require(counts == Counter({
        ("M", (0, 1)): 812,
        ("Hall", (0, 1)): 238,
        ("Hall", (2, 3)): 368,
        ("diagonal_q", (0, 1)): 1386,
        ("diagonal_q", (2, 3)): 68,
    }), f"the final-alternative port split changed: {counts}")
    return {
        "exact_split": {
            str(key): value for key, value in sorted(counts.items())
        },
        "P0_private_row_closes": {
            "M_crossed_label": 812,
            "Hall_P0_S1": 238,
            "diagonal_q_P0_S1": 1386,
            "total_P0_S1_slots": 2436,
        },
        "retained_P2_S3_slots": {
            "Hall": 368,
            "diagonal_q": 68,
            "total": 436,
        },
    }


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def main():
    pin_dependencies()
    double = load(
        "computations/verify_h3_axis_target_coloop_double_companion_transfer.py",
        "double_companion_dependency",
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
    all_matchings, bright, states, rows = audit_five_rows(
        double, second, first, routing
    )
    private = audit_complete_private_row(routing, bright, states)
    alternatives = audit_final_alternative_ports(
        double, routing, all_matchings, states
    )
    diagonal = audit_four_diagonal_specialization(
        double, second, first, routing
    )
    ledger = {
        "pins": PINS,
        "five_row_carrier": rows,
        "complete_P0_private_row": private,
        "final_hybrid_alternatives": alternatives,
        "four_diagonal_packet_specialization": diagonal,
        "theorem": (
            "a nonzero crossed-label M term P0:12*S1:21*Q_M^22 "
            "cannot survive.  The target-augmented private coefficient "
            "22222212 either reselects the pure-two target away from P0, "
            "or produces an external offdiagonal P arm, a crossed P2,S1 "
            "matching, or a P2 term whose P2:22 replacement is such a "
            "pure-two reselection.  The external P arm enters the "
            "nonanchor rank-(3,3) active-minor route; after reselection "
            "P0 does likewise; the crossed case enters the pinned crossed "
            "response route"
        ),
        "opposite_row_guard": (
            "on the exact frozen carrier support the p2s1 coefficient at "
            "residual word 212222 is empty in all 812 states.  Full five-row "
            "exactness does not force a complementary crossed cell or a "
            "five-lock; the first mandatory source row is instead the "
            "target-augmented P-private word 22222212"
        ),
        "scope": (
            "the same private row closes every final-hybrid mate with "
            "P0,S1 ports: 812 M slots, 238 Hall slots, and 1386 diagonal-q "
            "slots.  The 368 Hall plus 68 diagonal-q P2,S3 slots remain the "
            "one-sided active-minor/common-q return recurrence"
        ),
        "diagonal_packet_consequence": (
            "on each of the four sharp diagonal common-q packets, adding "
            "the crossed-M term and the required same-tail S companion "
            "already selects the C physical matching in pure colour two.  "
            "Thus it exits by target reselection and supplies no new "
            "multiplicative p1s2/p2s1 relation to the rank-two five-lock"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"crossed-M private-row ledger changed: {digest}")
    print("h3 target-coloop crossed-M private-site closure: PASS")
    print("frozen five-row profile: (0,2,0,2) x 812; p2s1 empty")
    print("P-private old terms: one 392 / two 420")
    print("P0,S1 final slots closed 2436; P2,S3 slots retained 436")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
