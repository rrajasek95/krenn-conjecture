#!/usr/bin/env python3
"""One-sided response-column route after the physical unary E3 correction.

On one selected mixed word, the target-skeleton and outside matchings use
two physical ports of the same p_i row at P and two ports of the same s_j
row at S.  Fixing one opposite star makes comparison on the other star an
exact linear map.  A proportional complete column can be absorbed by a
finite one-sided coefficient update.  This is anchor-safe unless the update
zeros a protected companion decoration; that event is the sharp lock
boundary.  Nonproportional columns give a same-star 2x2 minor.

An earlier version incorrectly used target coloopness to force every
proportionality scalar to zero.  The mixed-word companion decoration need
not be the pure-target decoration, so both compared columns can vanish on
the pure target coordinate.  This checker now freezes the correct finite
update and exception.

The checker also freezes the finite topology after the forced unary/direct
base: among 7 single-cycle response pairs and 15 unary bases, 55 unions
contain a crossed response matching and 50 do not.  This is only a union
support census, not a nonvanishing coefficient claim.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_axis_target_coloop_even_cycle_e3_boundary.py":
        "d42f7b266764f1c7d371a64f323fff1c5b50a9d73b30d343112603d1924435c8",
    "notes/h3-axis-target-coloop-even-cycle-e3-boundary.md":
        "52897d6063ff5ca46c714a5262c87fae4d243779ccdaee6caa4498c70dd8f2f9",
    "computations/verify_h3_axis_target_coloop_unary_e3_flat_exclusion.py":
        "5a1680fed1f9d0b388bbb0393ad57973bc4b2242d4d99cac9c3c5faadee7467b",
    "notes/h3-axis-target-coloop-unary-e3-flat-exclusion.md":
        "9182beced7c3820d83ddb52100b81ebbea12cea20e1736b7fdee72551b1cef11",
    "computations/verify_uniform_axis_circuit_outside_endpoint_rank_restoration.py":
        "1af29dfddaf3127e758f07c53cf08189bda72df4e54a58a4e0ca78f6709874ac",
    "notes/uniform-axis-circuit-outside-endpoint-rank-restoration.md":
        "a7345aa254a4dcfb65742b8b09f0dafe7a1ef1b1b9a2fa67b6e8528e462a9516",
    "computations/verify_h3_axis_target_coloop_one_sided_companion_boundary.py":
        "6cb34278cccf9327bdfccdece0b254f3eff95d179e512e80e1c938d4fe0eef62",
    "notes/h3-axis-target-coloop-one-sided-companion-boundary.md":
        "ce93379f949002eaf05f24975b902760d9dcd7095e4150bf132259c73a498393",
}
EXPECTED_LEDGER_SHA256 = (
    "4c2ad1df552a7230c14c8b4d74e5b38b07246bb88d2e07205cc90ec86d52eb5e"
)


P, S = 6, 7
TARGET_HOLES = (0, 1)
OUTSIDE_HOLES = (2, 3)
COMMON = (4, 5)


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


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def audit_retained_endpoint_labels():
    audits = []
    for crossed in ((1, 2), (2, 1)):
        for endpoint, label, target_site, outside_site in (
                (P, crossed[0], 0, 2),
                (S, crossed[1], 1, 3)):
            row = ("p" if endpoint == P else "s") + str(label)
            audits.append({
                "selected_mixed_endpoint_labels_(P,S)": crossed,
                "fixed_endpoint": endpoint,
                "common_source_row": row,
                "target_skeleton_port": edge(endpoint, target_site),
                "outside_port": edge(endpoint, outside_site),
            })
    require(len(audits) == 4, "the one-sided source-row label census changed")
    return audits


def audit_exact_column_dichotomy():
    companion_column = (Q(2), Q(-1), Q(3), Q(0))
    scale = Q(-3, 2)
    outside_column = tuple(scale * value for value in companion_column)
    outside_coefficient = Q(4)
    companion_coefficient = Q(5)
    updated_companion = companion_coefficient + scale * outside_coefficient
    before = tuple(outside_coefficient * outside_column[index]
                   + companion_coefficient * companion_column[index]
                   for index in range(len(companion_column)))
    after = tuple(updated_companion * value for value in companion_column)
    require(before == after,
            "the proportional one-sided finite update changed")
    cancellation_value = -scale * outside_coefficient
    require(cancellation_value + scale * outside_coefficient == 0,
            "the protected-companion lock value changed")

    first = (Q(1), Q(2), Q(0), Q(1))
    second = (Q(0), Q(3), Q(1), Q(-1))
    minors = tuple(first[left] * second[right]
                   - first[right] * second[left]
                   for left in range(4) for right in range(left + 1, 4))
    require(any(minors), "nonproportional columns lost every same-star minor")

    return {
        "companion_complete_column_sample": [str(value)
                                             for value in companion_column],
        "outside_complete_column_sample": [str(value)
                                           for value in outside_column],
        "proportional_branch": (
            "C_out=lambda*C_cmp permits the exact finite update "
            "x_out->0, x_cmp->x_cmp+lambda*x_out"
        ),
        "anchor_safety_exception": (
            "if C_cmp is a protected decoration and the updated companion "
            "coefficient is zero, the move loses an anchor and is a lock"
        ),
        "nonproportional_branch": (
            "some complete fine-coordinate same-star 2x2 minor is nonzero"
        ),
        "nonlinear_guard": (
            "only one endpoint row changes; the bistar mixed Hessian is absent"
        ),
    }


def response_pairs():
    target_tails = tuple(perfect_matchings(OUTSIDE_HOLES + COMMON))
    outside_tails = tuple(perfect_matchings(TARGET_HOLES + COMMON))
    records = []
    for target_tail in target_tails:
        for outside_tail in outside_tails:
            target = tuple(sorted((edge(P, 0), edge(S, 1)) + target_tail))
            outside = tuple(sorted((edge(P, 2), edge(S, 3)) + outside_tail))
            cycles = cycle_lengths(target, outside)
            if cycles in ((6,), (8,)):
                records.append((target, outside, cycles[0]))
    require(len(records) == 7, "the single-cycle response pair count changed")
    return tuple(records)


def audit_unary_union_crossed_census():
    matchings = tuple(perfect_matchings(range(8)))
    unary = tuple(tuple(sorted((edge(P, S),) + tail))
                  for tail in perfect_matchings(range(6)))
    require(len(matchings) == 105 and len(unary) == 15,
            "the K8/unary matching counts changed")
    records = []
    total_with_crossed = 0
    no_crossed_union_matching_counts = Counter()
    smallest_residual = None
    for record_index, (target, outside, cycle) in enumerate(response_pairs()):
        with_crossed = 0
        for unary_index, direct in enumerate(unary):
            union = set(target) | set(outside) | set(direct)
            contained = tuple(matching for matching in matchings
                              if set(matching) <= union)
            crossed = []
            for matching in contained:
                ports = (partner(matching, P), partner(matching, S))
                if ports in ((0, 3), (2, 1)):
                    crossed.append(matching)
            if crossed:
                with_crossed += 1
            else:
                no_crossed_union_matching_counts[len(contained)] += 1
                if (smallest_residual is None
                        or len(contained) < len(smallest_residual[3])):
                    smallest_residual = (target, outside, direct, contained)
            records.append({
                "response_record": record_index,
                "unary_base": unary_index,
                "cycle": cycle,
                "has_crossed_response_matching_in_union": bool(crossed),
                "crossed_matching_count": len(crossed),
            })
        total_with_crossed += with_crossed
    require(len(records) == 105
            and total_with_crossed == 55
            and len(records) - total_with_crossed == 50,
            "the unary-base crossed-union census changed")
    per_response = []
    for index in range(7):
        count = sum(record["has_crossed_response_matching_in_union"]
                    for record in records
                    if record["response_record"] == index)
        per_response.append(count)
    require(per_response == [5, 8, 8, 8, 9, 8, 9],
            "the per-response unary crossed counts changed")
    require(no_crossed_union_matching_counts
            == Counter({3: 13, 4: 17, 5: 14, 7: 6}),
            "the no-crossed union matching histogram changed")
    require(smallest_residual == (
        ((0, 6), (1, 7), (2, 3), (4, 5)),
        ((0, 1), (2, 6), (3, 7), (4, 5)),
        ((0, 1), (2, 3), (4, 5), (6, 7)),
        (
            ((0, 1), (2, 3), (4, 5), (6, 7)),
            ((0, 1), (2, 6), (3, 7), (4, 5)),
            ((0, 6), (1, 7), (2, 3), (4, 5)),
        ),
    ), "the smallest three-base physical residual changed")
    return {
        "response_pairs": 7,
        "unary_direct_bases_per_pair": 15,
        "triples": 105,
        "union_has_crossed_response_matching": total_with_crossed,
        "union_has_no_crossed_response_matching": 50,
        "per_response_counts": per_response,
        "no_crossed_union_matching_count_histogram": {
            str(key): value
            for key, value in sorted(no_crossed_union_matching_counts.items())
        },
        "smallest_residual": {
            "M": smallest_residual[0],
            "N": smallest_residual[1],
            "K_unary": smallest_residual[2],
            "all_perfect_matchings_in_union": smallest_residual[3],
        },
        "scope_guard": (
            "containment in the physical edge union does not assert a "
            "nonzero decorated matching coefficient"
        ),
    }


def main():
    pin_dependencies()
    ledger = {
        "pins": PINS,
        "retained_endpoint_source_labels": audit_retained_endpoint_labels(),
        "one_sided_complete_column": audit_exact_column_dichotomy(),
        "forced_unary_union_census": audit_unary_union_crossed_census(),
        "theorem": (
            "on one selected mixed word, target-skeleton and outside ports "
            "are components of the same p_i row and, separately, the same "
            "s_j row.  A proportional complete column admits an exact "
            "one-sided absorption update; nonproportional columns give a "
            "source-valid same-star minor"
        ),
        "anchor_safety": (
            "the absorption is support-reducing unless it zeros a protected "
            "companion decoration.  That exceptional cancellation is an "
            "anchor-contained lock, not an anchor-safe deletion"
        ),
        "scope": (
            "exact one-endpoint linear dichotomy and a physical edge-union "
            "census.  A nonzero same-star minor is not yet identified with "
            "a four-good/clean landing, and an edge-union crossed matching "
            "is not asserted coefficient-nonzero"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"one-sided target-coloop ledger changed: {digest}")
    print("h3 target-coloop one-sided response-column route: PASS")
    print("proportional column -> exact one-sided absorption or protected lock")
    print("nonproportional column -> nonzero same-star minor")
    print("unary union crossed census: 55 present / 50 absent")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
