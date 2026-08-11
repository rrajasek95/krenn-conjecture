#!/usr/bin/env python3
"""Exact one-sided reduction and bistar boundary for the h=3 coloop cycle.

On a selected mixed word, the outside matching N and its forced target-port
companion M use two components of one physical p_i row and two components of
one physical s_j row.  If either pair of *complete tensor columns* is
proportional, bilinearity gives an exact finite modification at that endpoint
only.  The modification is support-reducing unless it zeros a protected
companion decoration; that exceptional event is an anchor-contained lock.

If both endpoint pairs are nonproportional, inspect the four physical port
corners.  For each of the seven single-C6/C8 records, only M and N are
contained in M union N.  Every other diagonal or crossed-corner matching has
a residual q-edge outside that union.  Therefore either an external literal
q-mate occurs, or the selected-word cofactor corner is diagonal with nonzero
determinant.  The latter is the exact bistar/Fitting carrier.  It is not
promoted to a complete-column determinant without a common fine-word minor.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_axis_target_coloop_four_hole_exchange.py":
        "5283fae67a31ea3c9794fc8bbf351f7da5bc8251490dbdffbef04bde1f2a987f",
    "notes/h3-axis-target-coloop-four-hole-exchange.md":
        "9aa3a6e9315cc52769f0124188a17e69b6165fd45c04b21aa7203a4d70d5e341",
    "computations/verify_h3_axis_target_coloop_even_cycle_e3_boundary.py":
        "d42f7b266764f1c7d371a64f323fff1c5b50a9d73b30d343112603d1924435c8",
    "notes/h3-axis-target-coloop-even-cycle-e3-boundary.md":
        "52897d6063ff5ca46c714a5262c87fae4d243779ccdaee6caa4498c70dd8f2f9",
    "computations/verify_uniform_five_lock_wedge_or_switch.py":
        "c2541a60db1f8e7a661bc698d2bd1f1a1f396a0f0bfde389ea89bea17fac175e",
    "notes/uniform-five-lock-wedge-or-switch.md":
        "0871d5151a0fdb46fee0c9b15797a864e579a85c360a2638d458583479426914",
}
EXPECTED_LEDGER_SHA256 = (
    "d9ab3e869fac17f1adf932e3a7aebcc66ac6b62f424c12cfc41aacb69f4b10b4"
)


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


def rank(columns):
    if not columns:
        return 0
    matrix = [[Q(column[row]) for column in columns]
              for row in range(len(columns[0]))]
    pivot_row = 0
    for column in range(len(matrix[0])):
        pivot = next((row for row in range(pivot_row, len(matrix))
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [entry - value * pivot_entry
                           for entry, pivot_entry
                           in zip(matrix[row], matrix[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def audit_one_sided_exact_move():
    # L(z_out)=lambda L(z_cmp).  The displayed coefficient update is the
    # literal finite joint-kernel move, not merely its first variation.
    companion_column = (Q(2), Q(-1), Q(3), Q(0))
    scale = Q(-3, 2)
    outside_column = tuple(scale * value for value in companion_column)
    outside_coefficient = Q(4)
    companion_coefficient = Q(5)
    updated_companion = companion_coefficient + scale * outside_coefficient
    old_response = tuple(
        outside_coefficient * outside_column[index]
        + companion_coefficient * companion_column[index]
        for index in range(len(companion_column))
    )
    new_response = tuple(updated_companion * value
                         for value in companion_column)
    require(old_response == new_response,
            "the exact one-sided joint-kernel update changed")
    require(updated_companion != 0,
            "the anchor-preserving sample accidentally hit the lock")

    # The unique cancellation value is the sharp anchor-safety exception.
    cancellation_coefficient = -scale * outside_coefficient
    cancelled = cancellation_coefficient + scale * outside_coefficient
    require(cancelled == 0,
            "the protected-companion cancellation stratum changed")

    # Nonproportional complete columns are equivalent to a nonzero 2x2
    # complete fine-coordinate minor.  The same statement applies after
    # transposing p and s.
    first = (Q(1), Q(2), Q(0), Q(1))
    second = (Q(0), Q(3), Q(1), Q(-1))
    minors = {
        (left, right): first[left] * second[right]
        - first[right] * second[left]
        for left in range(4) for right in range(left + 1, 4)
    }
    require(rank((first, second)) == 2 and any(minors.values()),
            "complete-column nonproportionality lost its minor")
    proportional = tuple(Q(7) * value for value in first)
    proportional_minors = {
        (left, right): first[left] * proportional[right]
        - first[right] * proportional[left]
        for left in range(4) for right in range(left + 1, 4)
    }
    require(rank((first, proportional)) == 1
            and not any(proportional_minors.values()),
            "the proportional complete-column test changed")

    safety_cases = []
    for protected in (False, True):
        for companion_survives in (False, True):
            if companion_survives or not protected:
                verdict = "anchor-safe support reduction"
            else:
                verdict = "anchor-contained protected-decoration lock"
            safety_cases.append({
                "companion_decoration_protected": protected,
                "updated_companion_nonzero": companion_survives,
                "verdict": verdict,
            })
    require(Counter(case["verdict"] for case in safety_cases) == Counter({
        "anchor-safe support reduction": 3,
        "anchor-contained protected-decoration lock": 1,
    }), "the exact anchor-safety split changed")
    return {
        "affected_side": "P only (and, by transpose, S only)",
        "column_relation": "L_s(z_out)=lambda*L_s(z_cmp)",
        "finite_update": (
            "x_out -> 0; x_cmp -> x_cmp+lambda*x_out"
        ),
        "sample_old_response": [str(value) for value in old_response],
        "sample_new_response": [str(value) for value in new_response],
        "nonproportional_minor_count": sum(bool(value)
                                             for value in minors.values()),
        "anchor_safety_cases": safety_cases,
    }


P, S = 6, 7
TARGET_PORTS = (0, 1)
OUTSIDE_PORTS = (2, 3)
COMMON = (4, 5)


def audit_single_cycle_corners():
    target_tails = tuple(perfect_matchings(OUTSIDE_PORTS + COMMON))
    outside_tails = tuple(perfect_matchings(TARGET_PORTS + COMMON))
    records = []
    external_q_histogram = Counter()
    for target_tail in target_tails:
        for outside_tail in outside_tails:
            target = tuple(sorted((edge(P, 0), edge(S, 1)) + target_tail))
            outside = tuple(sorted((edge(P, 2), edge(S, 3)) + outside_tail))
            cycles = cycle_lengths(target, outside)
            if cycles not in ((6,), (8,)):
                continue
            union = set(target) | set(outside)
            q_union = {pair for pair in union if P not in pair and S not in pair}
            corners = {}
            contained_matrix = []
            for p_port in (0, 2):
                contained_row = []
                for s_port in (1, 3):
                    complement = tuple(site for site in range(6)
                                       if site not in (p_port, s_port))
                    full = tuple(
                        tuple(sorted((edge(P, p_port), edge(S, s_port))
                                     + tail))
                        for tail in perfect_matchings(complement)
                    )
                    contained = tuple(matching for matching in full
                                      if set(matching) <= union)
                    external = tuple(matching for matching in full
                                     if matching not in contained)
                    q_new_counts = []
                    for matching in external:
                        q_edges = {pair for pair in matching
                                   if P not in pair and S not in pair}
                        count = len(q_edges - q_union)
                        require(count >= 1,
                                "an alternate corner matching lacked an external q-edge")
                        q_new_counts.append(count)
                        external_q_histogram[count] += 1
                    corners[f"P{p_port}_S{s_port}"] = {
                        "matching_count": len(full),
                        "contained_in_M_union_N": len(contained),
                        "external_q_matching_count": len(external),
                        "new_q_edge_counts": q_new_counts,
                    }
                    contained_row.append(len(contained))
                contained_matrix.append(contained_row)
            require(contained_matrix == [[1, 0], [0, 1]],
                    f"the single-cycle corner support changed: {contained_matrix}")
            require(sum(entry["external_q_matching_count"]
                        for entry in corners.values()) == 10,
                    "the four-corner external matching count changed")
            records.append({
                "cycle": cycles[0],
                "M": target,
                "N": outside,
                "contained_corner_matrix": contained_matrix,
                "corners": corners,
                "no_external_q_consequence": (
                    "K_d=diag(T_M,T_N), det(K_d)=T_M*T_N!=0"
                ),
            })
    require(len(records) == 7,
            "the single-cycle record count changed")
    require(Counter(record["cycle"] for record in records)
            == Counter({8: 6, 6: 1}),
            "the C6/C8 record histogram changed")
    require(sum(external_q_histogram.values()) == 70,
            "the external corner audit count changed")
    return {
        "single_cycle_records": records,
        "record_count": len(records),
        "corner_matchings_audited": 84,
        "external_q_matchings": 70,
        "external_q_edge_count_histogram": dict(external_q_histogram),
        "uniform_corner_dichotomy": (
            "any supported corner term other than M,N is a literal matching "
            "with a residual q-edge outside M union N; if none occurs, the "
            "selected-word 2x2 cofactor corner is diagonal with localized "
            "nonzero determinant T_M*T_N"
        ),
    }


def partner(matching, site):
    for left, right in matching:
        if left == site:
            return right
        if right == site:
            return left
    raise RuntimeError((matching, site))


def audit_forced_unary_base_landing():
    """Test whether the E3 unary base automatically supplies a cross arm."""
    target_tails = tuple(perfect_matchings(OUTSIDE_PORTS + COMMON))
    outside_tails = tuple(perfect_matchings(TARGET_PORTS + COMMON))
    unary_bases = tuple(
        tuple(sorted((edge(P, S),) + tail))
        for tail in perfect_matchings(range(6))
    )
    all_matchings = tuple(perfect_matchings(range(8)))
    require(len(unary_bases) == 15 and len(all_matchings) == 105,
            "the unary/full K8 matching counts changed")
    audits = []
    for target_tail in target_tails:
        for outside_tail in outside_tails:
            target = tuple(sorted((edge(P, 0), edge(S, 1)) + target_tail))
            outside = tuple(sorted((edge(P, 2), edge(S, 3)) + outside_tail))
            cycles = cycle_lengths(target, outside)
            if cycles not in ((6,), (8,)):
                continue
            for unary in unary_bases:
                union = set(target) | set(outside) | set(unary)
                contained = tuple(matching for matching in all_matchings
                                  if set(matching) <= union)
                crossed = tuple(
                    matching for matching in contained
                    if ((partner(matching, P), partner(matching, S))
                        in ((2, 1), (0, 3)))
                )
                audits.append({
                    "MN_cycle": cycles[0],
                    "unary_base": unary,
                    "contained_matchings": len(contained),
                    "has_crossed_response_skeleton": bool(crossed),
                    "crossed_response_skeleton_count": len(crossed),
                })
    require(len(audits) == 105,
            "the seven-record/unary-base triple count changed")
    landing = Counter((audit["MN_cycle"],
                       audit["has_crossed_response_skeleton"])
                      for audit in audits)
    require(landing == Counter({
        (8, True): 50, (8, False): 40,
        (6, False): 10, (6, True): 5,
    }), f"the unary-base crossed-landing split changed: {landing}")
    no_cross_matching_counts = Counter(
        audit["contained_matchings"] for audit in audits
        if not audit["has_crossed_response_skeleton"]
    )
    require(no_cross_matching_counts == Counter({4: 17, 5: 14,
                                                  3: 13, 7: 6}),
            "the no-cross three-base union profiles changed")
    return {
        "three_base_unions": len(audits),
        "with_crossed_response_skeleton": 55,
        "without_crossed_response_skeleton": 50,
        "cycle_cross_histogram": {
            f"C{cycle}_{'cross' if crossed else 'no_cross'}": count
            for (cycle, crossed), count in sorted(landing.items())
        },
        "no_cross_contained_matching_histogram":
            dict(no_cross_matching_counts),
        "exact_consequence": (
            "the forced unary/direct E3 base does not automatically turn "
            "the selected-word bistar carrier into a crossed response "
            "matching: 50 of 105 physical three-base unions contain none"
        ),
        "first_missing_physical_input": (
            "a complete response companion selecting a crossed matching, "
            "or an alternate bright matching avoiding the target-coloop arm"
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
        "one_sided_complete_column": audit_one_sided_exact_move(),
        "single_cycle_physical_corners": audit_single_cycle_corners(),
        "forced_unary_base_landing": audit_forced_unary_base_landing(),
        "theorem": (
            "for the outside/companion components in one p_i row (or one "
            "s_j row), proportional full tensor columns give an exact "
            "one-endpoint joint-kernel move.  It is a minimum-support "
            "contradiction unless the update zeros a protected companion "
            "decoration, which is an anchor-contained Hall/lock.  If both "
            "endpoint pairs are nonproportional, the four selected-word "
            "physical corners give either a literal external q-mate or a "
            "nonzero diagonal bistar/Fitting carrier"
        ),
        "source_scope": (
            "the proportionality test uses full labelled tensor columns; a "
            "single coefficient never justifies deletion.  The bistar "
            "object is the selected-word physical cofactor corner.  It is "
            "not asserted to be a complete-column determinant unless the "
            "two endpoint minors are witnessed in one common fine degree"
        ),
        "remaining_boundary": (
            "a protected companion-decorated anchor lock, or a nonzero "
            "selected-word bistar carrier whose landing still requires a "
            "compatible full-row/strict-Hall or five-lock hypothesis.  Of "
            "the 105 physical C6/C8 plus unary-base triples, 50 contain no "
            "crossed response skeleton, so the unary base alone cannot "
            "supply that hypothesis"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"one-sided companion ledger changed: {digest}")
    print("h3 target-coloop one-sided companion boundary: PASS")
    print("proportional complete column -> exact one-endpoint kernel move")
    print("anchor safety: one protected-cancellation lock stratum")
    print("seven C6/C8 corners: external q mate or diagonal bistar carrier")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
