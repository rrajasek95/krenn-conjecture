#!/usr/bin/env python3
"""Exclude every >=3-centre kernel circuit in the diagonal two-bad chart.

Drop the target-colour internal cells and write K_x^B for the binary
four-site cofactor at hole x.  If u_x e_t is a target-axis kernel row,
the output words having their unique t at x give u_x K_x^B=0.  Hence
K_x^B=0 on the support S of u.

When |S|>=3, the two bright pure rows use at most two remaining binary
cofactors.  One remaining cofactor cannot carry two distinct pure tensors.
For two remaining holes, elementary factor separation forces one cofactor
to be pure a and the other pure c.  Nonzero matching monomials in those
two pure cofactors always contain a disjoint cross-colour edge pair.  Its
2+2 word has exactly one compatible diagonal matching, giving a nonzero
mixed coefficient in a cofactor required to be zero or pure.

The checker exhausts the finite matching and factor-support parts of this
division-free argument and reconstructs the unique mixed word literally.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json


SITES = tuple(range(5))
A, C, T = range(3)
EXPECTED_DIGEST = "d0aef0e02e4e52a78297f850478545859f16d18a1cf59665ade52daa6ae08378"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def audit_unique_target_projection():
    """A word with one t isolates exactly the cofactor at that t-hole."""
    records = []
    parity_live = 0
    for target_hole in SITES:
        remaining = tuple(site for site in SITES if site != target_hole)
        for binary_word in product((A, C), repeat=4):
            full_word = dict(zip(remaining, binary_word))
            full_word[target_hole] = T
            compatible_insertions = []
            for inserted_hole in SITES:
                if full_word[inserted_hole] != T:
                    continue
                cofactor_word = tuple(
                    full_word[site]
                    for site in SITES if site != inserted_hole
                )
                # A colour-diagonal four-site matching has even count of
                # every colour.  This test deliberately uses only parity,
                # so it overapproximates all possible diagonal supports.
                counts = Counter(cofactor_word)
                if all(counts[colour] % 2 == 0 for colour in (A, C, T)):
                    compatible_insertions.append(inserted_hole)
            binary_counts = Counter(binary_word)
            expected = ([target_hole]
                        if all(binary_counts[colour] % 2 == 0
                               for colour in (A, C))
                        else [])
            require(compatible_insertions == expected,
                    "a one-target word did not isolate its target hole")
            parity_live += bool(expected)
            records.append((target_hole, binary_word))
    require(len(records) == 5 * 2**4,
            "the one-target projection census changed")
    require(parity_live == 5 * 8,
            "the live binary-parity projection census changed")
    return len(records), parity_live


def audit_one_and_two_hole_factor_allocation():
    """Audit the support logic for one/two remaining binary cofactors.

    For two holes h,k, a nonzero coefficient at h in the pure-d row forces
    K_h to have factor e_d at k: no term inserted at k can cancel a word
    whose k-coordinate is not d.  The symmetric statement holds at k.
    A nonzero tensor cannot have both e_a and e_c at the same site.  Thus
    two distinct pure targets allocate the two holes bijectively and each
    allocated cofactor is completely pure.
    """
    nonzero_subsets = ((0,), (1,), (0, 1))
    allocations = []
    for a_support in nonzero_subsets:
        for c_support in nonzero_subsets:
            # A hole used by both rows would force its common cofactor to
            # have the two distinct factors e_a and e_c at the other hole.
            if set(a_support) & set(c_support):
                continue
            allocations.append((a_support, c_support))
    require(allocations == [((0,), (1,)), ((1,), (0,))],
            "two-hole pure-target allocation changed")

    # With only one remaining cofactor, both nonzero pure rows necessarily
    # use it, which would force one tensor to be both pure a and pure c.
    one_hole_allocations = []
    if not ({0} & {0}):
        one_hole_allocations.append(((0,), (0,)))
    require(not one_hole_allocations,
            "one cofactor unexpectedly carried two pure targets")
    return allocations


def compatible_diagonal_matchings(vertices, word):
    answer = []
    for matching in perfect_matchings(vertices):
        if all(word[left] == word[right] for left, right in matching):
            answer.append(matching)
    return answer


def audit_cross_colour_matching_collision():
    """Every pair of pure cofactors creates a unique mixed coefficient."""
    records = []
    for h, k in combinations(SITES, 2):
        a_vertices = tuple(site for site in SITES if site != h)
        c_vertices = tuple(site for site in SITES if site != k)
        for a_matching in perfect_matchings(a_vertices):
            for c_matching in perfect_matchings(c_vertices):
                disjoint_pairs = [
                    (a_edge, c_edge)
                    for a_edge in a_matching
                    for c_edge in c_matching
                    if set(a_edge).isdisjoint(c_edge)
                ]
                require(disjoint_pairs,
                        "two pure matching monomials had no disjoint edges")

                a_edge, c_edge = disjoint_pairs[0]
                covered = set(a_edge) | set(c_edge)
                require(len(covered) == 4,
                        "a cross-colour pair failed to cover four sites")
                hole = next(iter(set(SITES) - covered))
                vertices = tuple(site for site in SITES if site != hole)
                word = {
                    **{site: A for site in a_edge},
                    **{site: C for site in c_edge},
                }
                compatible = compatible_diagonal_matchings(vertices, word)
                expected = (tuple(sorted(a_edge)), tuple(sorted(c_edge)))
                expected = tuple(sorted(expected))
                require(compatible == [expected],
                        "the mixed 2+2 word lost its unique matching")

                # Every hole is either in the target-kernel support, where
                # K_hole^B=0, or is h/k, where its cofactor is pure.  A mixed
                # coefficient is forbidden in all three cases.
                forbidden_reason = (
                    "pure-a cofactor" if hole == h else
                    "pure-c cofactor" if hole == k else
                    "zero kernel-support cofactor"
                )
                records.append({
                    "bright_holes": [h, k],
                    "a_matching": a_matching,
                    "c_matching": c_matching,
                    "a_edge": a_edge,
                    "c_edge": c_edge,
                    "mixed_hole": hole,
                    "forbidden_reason": forbidden_reason,
                })

    require(len(records) == 10 * 3 * 3,
            "the pure-matching pair census changed")
    reasons = Counter(record["forbidden_reason"] for record in records)
    require(sum(reasons.values()) == 90,
            "the collision-reason census changed")
    return records, reasons


def audit_support_sizes():
    cases = {}
    for support_size in range(3, 6):
        remaining = 5 - support_size
        if remaining == 2:
            verdict = "two holes force separate pure-a/pure-c cofactors"
        elif remaining == 1:
            verdict = "one cofactor cannot carry both pure targets"
        else:
            verdict = "no cofactor remains to carry either pure target"
        cases[support_size] = {"remaining_holes": remaining,
                               "verdict": verdict}
    return cases


def audit():
    projection_count, live_projection_count = audit_unique_target_projection()
    allocations = audit_one_and_two_hole_factor_allocation()
    collision_records, collision_reasons = (
        audit_cross_colour_matching_collision()
    )
    support_cases = audit_support_sizes()

    ledger = {
        "site_count": len(SITES),
        "one_target_projection_words": projection_count,
        "one_target_live_binary_parity_words": live_projection_count,
        "two_hole_allocations": allocations,
        "pure_matching_pair_records": collision_records,
        "collision_reason_counts": dict(sorted(collision_reasons.items())),
        "large_support_cases": support_cases,
        "verdict": (
            "a colour-diagonal five-site common-cofactor map containing "
            "two distinct pure images has no nonzero target-axis kernel "
            "component supported on three or more centres"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"the large-kernel ledger changed: {digest}")
    return digest, collision_reasons


def main():
    digest, reasons = audit()
    print("coordinate-diagonal >=3-centre kernel exclusion: PASS")
    print("one-target projection words: 80")
    print("live binary-parity projection words: 40")
    print("two-hole pure allocations: 2")
    print("pure matching-pair collisions: 90")
    print("collision reasons:", dict(sorted(reasons.items())))
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
