#!/usr/bin/env python3
"""Close the 110 target-coloop label residuals by one hybrid anchor row.

The 48 residual-q-only, 50 same-base and 12 residual-C4 records all have
the same endpoint ports for the selected mixed matching N and the other
bright pure matching L: P2 and S3.  Put e=S3.  The selected mixed word has
S-label 2, while L is pure colour 1, so the mixed cell on e and the three
pure L cells off e form a nonzero mixed-row monomial.

Any supported cancellation matching B' either omits e, exposing the
off-diagonal S-endpoint cell 21, or retains e.  In the latter case its tail
is literally a pure-1 matching tail.  If no supported mate omits e, the
whole mixed coefficient factors as x_e^(2,rho_3) H_e^1=0; over a domain
H_e^1=0, and the normalized pure-1 target supplies a matching avoiding e.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_axis_target_coloop_other_bright_anchor_reduction.py":
        "78f8058dd8ede4af69b87bc61a1f14a6b67dfab026fdf55d565ada0919f3e080",
    "notes/h3-axis-target-coloop-other-bright-anchor-reduction.md":
        "d6644fa199c5d6d7602564aeb02a6095086def500016421bb3052bfa013a6344",
    "computations/verify_h3_axis_target_coloop_same_base_hybrid_mate.py":
        "5bcb6953800ec617145fe3be40c52618e362f9cf636d5e9a1fbd9d2257508bec",
    "notes/h3-axis-target-coloop-same-base-hybrid-mate.md":
        "ea9e7e14a60c00f50e33b9141226336510b9470cfdb0118cbdf58adb80bd5f8a",
    "computations/verify_uniform_decorated_anchor_mixed_word_exchange.py":
        "150bf15eb8ac475f866c062afcd7e3002477d02338acdb082c14f9136a3e58b7",
    "notes/uniform-decorated-anchor-mixed-word-exchange.md":
        "0cdc391bebb44150c7941bdbeec853029929f20d46ee813eb2a09bb76c27a5de",
    "computations/verify_uniform_one_bad_nonanchor_offdiagonal_good_pair.py":
        "64e85cd84112b5160efe4f43ce1208da3c49f5e58b3e4a4d6192e6a9c229c306",
    "notes/uniform-one-bad-nonanchor-offdiagonal-good-pair.md":
        "4516c5ff02f130e1ad25b4fde395c81557e58ba0c83f7f98969d95df17fd6409",
}
EXPECTED_LEDGER_SHA256 = (
    "7f3ff8ed4139cd7d3156f2c96e34405beaf0354b899cfe112ff0d1a82aeb38fa"
)


P, S = 6, 7


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge(left, right):
    return tuple(sorted((left, right)))


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remainder):
            yield tuple(sorted((edge(first, second),) + tail))


def partner(matching, site):
    for left, right in matching:
        if left == site:
            return right
        if right == site:
            return left
    raise RuntimeError((matching, site))


def cycle_lengths(first, second):
    common = set(first) & set(second)
    symmetric = (set(first) | set(second)) - common
    adjacency = {}
    for left, right in symmetric:
        adjacency.setdefault(left, set()).add(right)
        adjacency.setdefault(right, set()).add(left)
    lengths = []
    unseen = set(adjacency)
    while unseen:
        start = next(iter(unseen))
        previous = None
        current = start
        length = 0
        while True:
            following = next(site for site in adjacency[current]
                             if site != previous)
            length += 1
            previous, current = current, following
            unseen.discard(previous)
            if current == start:
                break
        lengths.append(length)
    return tuple(sorted(lengths))


def response_pairs():
    records = []
    for target_tail in perfect_matchings((2, 3, 4, 5)):
        for outside_tail in perfect_matchings((0, 1, 4, 5)):
            target = tuple(sorted((edge(P, 0), edge(S, 1)) + target_tail))
            outside = tuple(sorted((edge(P, 2), edge(S, 3)) + outside_tail))
            cycles = cycle_lengths(target, outside)
            if cycles in ((6,), (8,)):
                records.append((target, outside, cycles))
    require(len(records) == 7, "the seven response pairs changed")
    return tuple(records)


def crossed_port(matching):
    return (partner(matching, P), partner(matching, S)) in ((2, 1), (0, 3))


def residual_records():
    """Reconstruct exactly the 48+50+12 records of the pinned reduction."""
    all_matchings = tuple(perfect_matchings(range(8)))
    unary_bases = tuple(tuple(sorted((edge(P, S),) + tail))
                        for tail in perfect_matchings(range(6)))
    bright_bases = tuple(matching for matching in all_matchings
                         if edge(P, S) not in matching)

    no_cross_triples = []
    for target, outside, cycles in response_pairs():
        for unary in unary_bases:
            union = set(target) | set(outside) | set(unary)
            if not any(set(matching) <= union and crossed_port(matching)
                       for matching in all_matchings):
                no_cross_triples.append((target, outside, unary, cycles))
    require(len(no_cross_triples) == 50,
            "the no-cross triple count changed")

    records = []
    all_outcomes = Counter()
    for target, outside, unary, cycles in no_cross_triples:
        for bright in bright_bases:
            anchor_union = set(target) | set(unary) | set(bright)
            external = set(outside) - anchor_union
            endpoint_external = tuple(pair for pair in external
                                      if P in pair or S in pair)
            residual_external = tuple(pair for pair in external
                                      if P not in pair and S not in pair)
            crossed = tuple(matching for matching in all_matchings
                            if set(matching) <= anchor_union
                            and crossed_port(matching))
            if crossed:
                kind = "selected_anchor_crossed"
            elif endpoint_external:
                kind = "external_endpoint_arm"
            elif residual_external:
                kind = "external_residual_q_only"
            elif bright == outside:
                kind = "same_base_word_change"
            else:
                require(cycle_lengths(bright, outside) == (4,),
                        "the last word-change packet stopped being a C4")
                kind = "residual_C4_word_change"
            all_outcomes[kind] += 1
            if kind in {
                "external_residual_q_only",
                "same_base_word_change",
                "residual_C4_word_change",
            }:
                records.append({
                    "kind": kind,
                    "cycles": cycles,
                    "M": target,
                    "N": outside,
                    "K": unary,
                    "L": bright,
                })

    require(all_outcomes == Counter({
        "selected_anchor_crossed": 612,
        "external_endpoint_arm": 3778,
        "external_residual_q_only": 48,
        "same_base_word_change": 50,
        "residual_C4_word_change": 12,
    }), f"the parent partition changed: {all_outcomes}")
    require(len(records) == 110, "the 110 label residuals changed")
    return all_matchings, tuple(records)


def audit_hybrid_escape():
    all_matchings, records = residual_records()
    kinds = Counter(record["kind"] for record in records)
    cycle_kinds = Counter((record["cycles"], record["kind"])
                          for record in records)
    mate_routes = Counter()
    port_pairs = Counter()
    rho_audit = 0

    for record in records:
        target = record["M"]
        outside = record["N"]
        unary = record["K"]
        bright = record["L"]
        require((partner(outside, P), partner(outside, S)) == (2, 3),
                "the selected mixed matching lost ports P2,S3")
        port_pair = (partner(bright, P), partner(bright, S))
        port_pairs[port_pair] += 1
        require(port_pair == (2, 3),
                "a residual other-bright anchor did not share both N ports")

        chosen = edge(S, 3)
        require(chosen in outside and chosen in bright,
                "the shared S3 edge disappeared")
        require(chosen not in target and chosen not in unary,
                "the shared S3 edge entered M or the direct anchor K")
        require(partner(target, S) == 1 and partner(unary, S) == P,
                "the two other selected S arms changed")

        # The selected outside word is rho+(1,2).  Its rho_3 may be any
        # colour.  The hybrid remains mixed because the S label is 2 while
        # every site off chosen is assigned the other bright colour 1.
        for rho_three in range(3):
            word = [1] * 8
            word[S] = 2
            word[3] = rho_three
            word = tuple(word)
            require(len(set(word)) > 1,
                    "the S-head hybrid became a pure target word")
            rho_audit += 1

            for mate in all_matchings:
                if mate == bright:
                    continue
                if chosen in mate:
                    require(all(word[left] == word[right] == 1
                                for left, right in mate if (left, right) != chosen),
                            "a through-e mate tail stopped being pure 1")
                    mate_routes["retains_e_pure_tail"] += 1
                    continue

                new_s_edge = next(pair for pair in mate if S in pair)
                other = (new_s_edge[0] if new_s_edge[1] == S
                         else new_s_edge[1])
                require(other != 3 and word[other] == 1,
                        "an avoiding mate did not send S to a pure-1 site")
                require(word[S] != word[other],
                        "the avoiding S cell stopped being off-diagonal")
                if other == P:
                    # The normalized direct block PS has only its 00 cell,
                    # so a 12/21 decorated term is literally unavailable.
                    mate_routes["direct_PS_label_forbidden"] += 1
                elif new_s_edge in set(target) | set(unary) | set(bright):
                    require(new_s_edge == edge(S, 1),
                            "an avoiding decorated-anchor S edge was not M's S1")
                    mate_routes["decorated_anchor_exchange"] += 1
                else:
                    mate_routes["nonanchor_offdiagonal"] += 1

    require(kinds == Counter({
        "external_residual_q_only": 48,
        "same_base_word_change": 50,
        "residual_C4_word_change": 12,
    }), f"the residual kind histogram changed: {kinds}")
    require(port_pairs == Counter({(2, 3): 110}),
            f"the residual port purification changed: {port_pairs}")
    require(rho_audit == 110 * 3,
            "the arbitrary residual-head-colour audit changed")
    require(mate_routes == Counter({
        "retains_e_pure_tail": 110 * 3 * 14,
        "direct_PS_label_forbidden": 110 * 3 * 15,
        "decorated_anchor_exchange": 110 * 3 * 15,
        "nonanchor_offdiagonal": 110 * 3 * 60,
    }), f"the hybrid mate routing changed: {mate_routes}")

    return {
        "residual_kind_histogram": dict(sorted(kinds.items())),
        "cycle_kind_histogram": {
            str(key): count for key, count in sorted(cycle_kinds.items())
        },
        "shared_port_histogram": {
            str(key): count for key, count in sorted(port_pairs.items())
        },
        "residual_head_colours_audited": rho_audit,
        "candidate_mate_routes": dict(sorted(mate_routes.items())),
        "hybrid_row": (
            "x_(S3)^(2,rho_3) times the three pure-1 L cells off S3; "
            "the output word is (1 off S3, 2 at S, rho_3 at 3)"
        ),
        "aggregate_dichotomy": (
            "a supported avoiding-S3 mate contains a nonzero 21 cell at S; "
            "if none exists, the mixed row is x_(S3)^(2,rho_3) H_(S3)^1=0, "
            "so H_(S3)^1=0 and the normalized pure-1 target supplies an "
            "alternate pure-1 matching omitting S3"
        ),
    }


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def main():
    pin_dependencies()
    ledger = {
        "pins": PINS,
        "hybrid_anchor_escape": audit_hybrid_escape(),
        "routing": (
            "a nonanchor 21 endpoint cell enters the pinned rank-(3,3) "
            "active-minor route.  The only anchor-contained nonzero endpoint "
            "cell is on M's S1 edge and enters the complete decorated-anchor "
            "exchange.  PS is impossible at this word because the normalized "
            "direct block supports only 00.  In the no-avoiding-term branch, "
            "reselecting pure 1 away from S3 makes the already active N arm "
            "S3 external to M,K,L' and restores the rank-three endpoint route"
        ),
        "scope": (
            "exact source-labelled h=3 closure of all 110 residual records, "
            "uniform in the residual partner label rho_3 and over integral "
            "domains.  The graph enumeration only proves the shared-port "
            "landing; the hybrid row and cofactor factorization are literal "
            "full-source identities"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"hybrid anchor-escape ledger changed: {digest}")
    print("h3 target-coloop hybrid anchor escape: PASS")
    print("110/110 residuals share N,L ports P2,S3")
    print("avoiding mate -> nonanchor 21 or decorated M-anchor exchange")
    print("no avoiding mate -> H_S3^1=0 -> pure-1 reselection away from S3")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
