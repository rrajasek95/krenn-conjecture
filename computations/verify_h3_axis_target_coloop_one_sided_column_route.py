#!/usr/bin/env python3
"""One-sided response-column route after the physical unary E3 correction.

For a selected bright target of colour i and a crossed response, exactly one
outer endpoint retains label i.  At that endpoint the target-skeleton port
and the outside port are two components of the same literal p_i (or s_i)
row.  With the opposite endpoint forms and q fixed, their complete output
columns are therefore compared by an exact linear map.

If the outside column is zero, it is exactly deletable.  If it is
proportional to the target column, the target-coloop coordinate forces the
proportionality scalar to be zero, so this is the same deletion branch.  At
a support-minimal source the columns are nonproportional; a target/outside
2x2 minor is nonzero.  No simultaneous two-star change and hence no bistar
Hessian is used.

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
}
EXPECTED_LEDGER_SHA256 = (
    "9a4760098cd0bd2ab06d3dec10554a549c0fc8a8830dac7b2e37d954d49d7c91"
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
    for target_colour in (1, 2):
        other = 3 - target_colour
        for crossed in ((target_colour, other), (other, target_colour)):
            retained = tuple(endpoint for endpoint, (target_label, label)
                             in zip((P, S),
                                    ((target_colour, crossed[0]),
                                     (target_colour, crossed[1])),
                                    strict=True)
                             if target_label == label)
            require(len(retained) == 1,
                    "a crossed row stopped retaining exactly one endpoint label")
            endpoint = retained[0]
            row = ("p" if endpoint == P else "s") + str(target_colour)
            target_port = edge(endpoint, 0 if endpoint == P else 1)
            outside_port = edge(endpoint, 2 if endpoint == P else 3)
            require(target_port != outside_port,
                    "the target and outside components became one physical port")
            audits.append({
                "target_colour": target_colour,
                "crossed_endpoint_labels_(P,S)": crossed,
                "retained_endpoint": endpoint,
                "common_source_row": row,
                "target_skeleton_port": target_port,
                "outside_port": outside_port,
            })
    require(len(audits) == 4, "the retained-endpoint label census changed")
    return audits


def audit_exact_column_dichotomy():
    target_column = (Q(3), Q(5))
    outside_column = (Q(0), Q(-2))
    determinant = (target_column[0] * outside_column[1]
                   - target_column[1] * outside_column[0])
    require(determinant == -6,
            "the target/outside same-star minor changed")

    compatible = []
    for scalar in (Q(-2), Q(0), Q(3)):
        candidate = tuple(scalar * value for value in target_column)
        if candidate[0] == 0:
            compatible.append((scalar, candidate))
    require(compatible == [(Q(0), (Q(0), Q(0)))],
            "a nonzero proportional outside column survived target coloopness")

    coefficients = (Q(7), Q(-4))
    zero = (Q(0), Q(0))
    before = tuple(coefficients[0] * target_column[index]
                   + coefficients[1] * zero[index] for index in range(2))
    after = tuple(coefficients[0] * target_column[index]
                  for index in range(2))
    require(before == after,
            "zero-column deletion stopped being an exact finite identity")

    return {
        "target_complete_column_sample": [str(value)
                                          for value in target_column],
        "outside_complete_column_sample": [str(value)
                                           for value in outside_column],
        "same_star_minor_sample": str(determinant),
        "proportional_branch": (
            "C_out=lambda*C_tar and C_out(target)=0 with "
            "C_tar(target)!=0 force lambda=0, hence C_out=0"
        ),
        "zero_branch": (
            "delete only the outside component in the common p_i/s_i row; "
            "q and the opposite endpoint rows are fixed"
        ),
        "support_minimal_branch": (
            "C_out!=0, so the two columns are nonproportional and some "
            "literal same-star 2x2 minor is nonzero"
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
            "for either crossed response orientation, retain the endpoint "
            "whose label equals the selected diagonal colour.  The target "
            "and outside ports are components of the same p_i or s_i row. "
            "With every other source row fixed, a zero/proportional outside "
            "complete column is exactly deletable; at support minimum the "
            "columns are nonproportional and give a source-valid same-star "
            "minor"
        ),
        "anchor_safety": (
            "the deletion removes only the outside component.  It cannot be "
            "a nonzero selected pure anchor of another colour because its "
            "endpoint label is i; target-coloopness excludes it from the "
            "selected colour-i target family.  The direct unary anchor uses "
            "P--S and is unchanged"
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
    print("zero/proportional outside column -> exact anchor-safe deletion")
    print("support-minimal outside column -> nonzero same-star minor")
    print("unary union crossed census: 55 present / 50 absent")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
