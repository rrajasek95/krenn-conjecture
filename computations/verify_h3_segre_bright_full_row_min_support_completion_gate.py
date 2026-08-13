#!/usr/bin/env python3
"""Full-row/minimum-support audit of the local Segre-bright guard.

The local guard of ``55054a0`` has endpoint block

    [[1, 0, -1], [0, 0, 0]].

Its selected response sum is zero, whereas the pure diagonal target row is
one.  Hence a full source must add an occurrence outside that local block.

This checker then exhausts the smallest axis-purified completion.  The unary
target needs one pure-0 residual matching (three q cells); each of the two
bright diagonal targets needs two q cells and one cell on each endpoint
star.  Thus the lower bound is 3+4+4=11 decorated source coordinates.  At
equality the data are three selected perfect matchings, with one endpoint
edge removed from each bright matching.  All 30,375 labelled supports and
all four endpoint orientations are checked.  Whenever the unary and both
diagonal targets are exact, each crossed response contains exactly one
nonzero monomial.  Therefore no 11-cell axis-purified full source exists.

This is a bounded completion theorem, not an emptiness proof for the full
source locus.  A larger completion may use axis-purified cancellation.  An
offdiagonal added cell instead enters the already proved target-augmented
private-site fan alternative.
"""

from __future__ import annotations

from fractions import Fraction as Q
from functools import lru_cache
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_segre_bright_private_site_incidence_tate_alternative.py":
        "e00e9b39740c22b2beacd874e13ab3b7e7c2f776724e19eece28f525400d6258",
    "notes/h3-segre-bright-private-site-incidence-tate-alternative.md":
        "95a8ee1a7603cb5e5af20b44cdf7668a42b22fb020f042839a58e5a8329baa99",
    "computations/verify_uniform_target_augmented_private_site_active_minor.py":
        "c53ba30dd8b7084cc27e05f11aa6066354fdec45ff2cf72ebdfb85bb8517169b",
    "notes/uniform-target-augmented-private-site-active-minor.md":
        "d7b16ecbb867524615ecf3034e0911e0add34825a7f9088f369f3a11e1c61f0d",
    "computations/verify_n8_one_bad_endpoint_minor_unary_top_completion.py":
        "f0d4c5382cce1ccb8bed5a5ac0afa8cf8662c905bd0c675a56b51f2be7d0b574",
    "notes/n8-one-bad-endpoint-minor-unary-top-completion.md":
        "023e2abb11be04e2b05ddac332b5a63fc0dbbc1e250a6b3a29c7ff47e17c0fda",
}
EXPECTED_LEDGER_SHA256 = "cc9eaf836b0530140d88da803584c85080e83308dc396829c5982f8476d01aa8"

SITES = tuple(range(6))
PURE = {colour: (colour,) * len(SITES) for colour in range(3)}
Edge = tuple[int, int]
Matching = tuple[Edge, ...]


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


@lru_cache(maxsize=None)
def perfect_matchings(vertices: tuple[int, ...]) -> tuple[Matching, ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index, second in enumerate(vertices[1:], 1):
        remainder = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remainder):
            answer.append(tuple(sorted(((first, second),) + tail)))
    return tuple(answer)


def decorated_terms(
    support: dict[Edge, set[int]], vertices: tuple[int, ...]
) -> tuple[tuple[Matching, tuple[int, ...]], ...]:
    """Return every supported decorated matching and its local word."""
    vertices = tuple(sorted(vertices))
    answer = []
    for matching in perfect_matchings(vertices):
        choices = [tuple(sorted(support.get(edge, set())))
                   for edge in matching]
        if any(not choice for choice in choices):
            continue
        for colours in product(*choices):
            word = {}
            for (left, right), colour in zip(
                    matching, colours, strict=True):
                word[left] = word[right] = colour
            answer.append((matching, tuple(word[site] for site in vertices)))
    return tuple(answer)


def full_response_word(
    local_word: tuple[int, ...], holes: tuple[int, int],
    endpoint_colours: tuple[int, int]
) -> tuple[int, ...]:
    word: list[int | None] = [None] * len(SITES)
    for site, colour in zip(holes, endpoint_colours, strict=True):
        word[site] = colour
    residual = (site for site in SITES if site not in holes)
    for site, colour in zip(residual, local_word, strict=True):
        word[site] = colour
    require(all(value is not None for value in word), "response word has a hole")
    return tuple(int(value) for value in word)


def local_bright_target_mismatch() -> dict[str, object]:
    A, B = Q(1), Q(0)
    matching_values = (Q(1), Q(0), Q(-1))
    block = (
        tuple(A * value for value in matching_values),
        tuple(B * value for value in matching_values),
    )
    response_sums = tuple(sum(row, Q(0)) for row in block)
    derivatives = tuple(
        (A - B) * (matching_values[left] - matching_values[right])
        for left, right in ((0, 1), (0, 2), (1, 2))
    )
    require(response_sums == (Q(0), Q(0))
            and derivatives == (Q(1), Q(2), Q(1)),
            "the pinned local bright guard changed")

    # q^[3]=X0 means its coefficient at the pure-1 residual word is zero.
    # Consequently no direct scalar multiple of q^[3] can repair the pure-1
    # diagonal response coefficient.  The missing response occurrence has
    # total value exactly one.
    direct_at_pure1 = Q(0)
    missing_diagonal_value = Q(1) - response_sums[0] - direct_at_pure1
    require(missing_diagonal_value == 1,
            "the pure-target completion value changed")

    # The target equation fixes the sum channel, not the two-dimensional
    # matching-difference channel.  A symmetric affine correction repairs
    # the sum while preserving every difference.  Hence the cylinder
    # curvature t*k, with t=A-B, survives in the complete-row coefficient
    # quotient.  This does not assert a physical source lift of the
    # correction; that lift is precisely the missing incidence problem.
    symmetric_correction = (Q(1, 3),) * 3
    completed_first_row = tuple(
        left + right for left, right in
        zip(block[0], symmetric_correction, strict=True))
    completed_differences = tuple(
        (A - B) * (completed_first_row[left] - completed_first_row[right])
        for left, right in ((0, 1), (0, 2), (1, 2))
    )
    require(sum(completed_first_row, Q(0)) == 1
            and completed_differences == derivatives,
            "the sum/difference splitting changed")
    return {
        "local_occurrence_block": [[1, 0, -1], [0, 0, 0]],
        "orientation_response_sums": [0, 0],
        "linearized_Segre_minors": [1, 2, 1],
        "q_cubed_at_pure_1": 0,
        "pure_1_diagonal_target": 1,
        "additional_response_value_required": 1,
        "symmetric_sum_channel_correction": ["1/3", "1/3", "1/3"],
        "completed_first_orientation": ["4/3", "1/3", "-2/3"],
        "completed_matching_differences": [1, 2, 1],
        "cylinder_curvature": {
            "endpoint_factor_t=A-B": 1,
            "matching_factors_k": [1, 2, 1],
            "products_t*k": [1, 2, 1],
            "status": (
                "nonzero in the complete-row coefficient quotient; a "
                "physical source lift of the sum correction is not asserted"
            ),
        },
        "consequence": (
            "the 55054a0 block cannot be the complete pure diagonal row; "
            "a full source must add at least one occurrence outside it"
        ),
    }


def smallest_axis_pure_completion() -> dict[str, object]:
    matchings = perfect_matchings(SITES)
    require(len(matchings) == 15, "the six-site matching count changed")

    support_count = 0
    unary_exact = 0
    all_three_targets_exact = 0
    orientation_tests = 0
    crossed_profile: dict[str, int] = {}
    example = None

    for matching0 in matchings:
        for matching1 in matchings:
            for endpoint_edge1 in matching1:
                tail1 = tuple(edge for edge in matching1
                              if edge != endpoint_edge1)
                for matching2 in matchings:
                    for endpoint_edge2 in matching2:
                        tail2 = tuple(edge for edge in matching2
                                      if edge != endpoint_edge2)
                        support_count += 1
                        support: dict[Edge, set[int]] = {}
                        for matching, colour in (
                                (matching0, 0), (tail1, 1), (tail2, 2)):
                            for edge in matching:
                                support.setdefault(edge, set()).add(colour)

                        top = decorated_terms(support, SITES)
                        if top != ((matching0, PURE[0]),):
                            continue
                        unary_exact += 1

                        complement1 = tuple(
                            site for site in SITES
                            if site not in endpoint_edge1)
                        complement2 = tuple(
                            site for site in SITES
                            if site not in endpoint_edge2)
                        terms11 = decorated_terms(support, complement1)
                        terms22 = decorated_terms(support, complement2)
                        if terms11 != ((tail1, (1,) * 4),) \
                                or terms22 != ((tail2, (2,) * 4),):
                            continue
                        all_three_targets_exact += 1

                        for p1, s1 in (endpoint_edge1,
                                       endpoint_edge1[::-1]):
                            for p2, s2 in (endpoint_edge2,
                                           endpoint_edge2[::-1]):
                                orientation_tests += 1
                                if p1 == s2:
                                    terms12 = ()
                                else:
                                    complement12 = tuple(
                                        site for site in SITES
                                        if site not in (p1, s2))
                                    terms12 = decorated_terms(
                                        support, complement12)
                                if p2 == s1:
                                    terms21 = ()
                                else:
                                    complement21 = tuple(
                                        site for site in SITES
                                        if site not in (p2, s1))
                                    terms21 = decorated_terms(
                                        support, complement21)

                                profile = f"G12={len(terms12)},G21={len(terms21)}"
                                crossed_profile[profile] = (
                                    crossed_profile.get(profile, 0) + 1)
                                require(len(terms12) == len(terms21) == 1,
                                        ("a smallest completion acquired a "
                                         "crossed-zero orientation",
                                         matching0, matching1, matching2,
                                         (p1, s1, p2, s2), profile))

                                word12 = full_response_word(
                                    terms12[0][1], (p1, s2), (1, 2))
                                word21 = full_response_word(
                                    terms21[0][1], (p2, s1), (2, 1))
                                require(word12 not in PURE.values()
                                        and word21 not in PURE.values(),
                                        "a crossed term became a target word")
                                if example is None:
                                    example = {
                                        "q0_matching": matching0,
                                        "G11_matching": matching1,
                                        "G22_matching": matching2,
                                        "endpoint_orientation": [p1, s1, p2, s2],
                                        "forced_G12_word": "".join(map(str, word12)),
                                        "forced_G21_word": "".join(map(str, word21)),
                                    }

    require(support_count == 30375
            and unary_exact == 3960
            and all_three_targets_exact == 360
            and orientation_tests == 1440,
            ("the smallest completion census changed", support_count,
             unary_exact, all_three_targets_exact, orientation_tests))
    require(crossed_profile == {"G12=1,G21=1": 1440},
            ("the crossed response profile changed", crossed_profile))
    require(example is not None, "the completion audit lost its example")

    return {
        "axis_pure_decorated_support_lower_bound": 11,
        "lower_bound_decomposition": {
            "unary_X0": "3 q:00 cells",
            "diagonal_X1": "2 q:11 + p1 + s1",
            "diagonal_X2": "2 q:22 + p2 + s2",
        },
        "labelled_supports_tested": support_count,
        "unary_exact_supports": unary_exact,
        "unary_and_both_diagonal_exact_supports": all_three_targets_exact,
        "endpoint_orientations_tested": orientation_tests,
        "crossed_response_profile": crossed_profile,
        "representative": example,
        "coefficient_reason": (
            "the three target coefficients make every one of the 11 "
            "support weights nonzero; each crossed row has one monomial, "
            "so its coefficient cannot cancel over a field"
        ),
        "theorem": (
            "there is no axis-purified direct-free 11-coordinate source "
            "satisfying q^[3]=X0, G11=X1, G22=X2, G12=G21=0"
        ),
    }


def routed_and_open_branches() -> dict[str, object]:
    return {
        "offdiagonal_enlargement": (
            "the target-augmented private-site identity produces a nonzero "
            "determinant/cofactor fan; the existing landing is four-good or "
            "a literal pure-colour coloop"
        ),
        "axis_purified_enlargement": (
            "must use more than 11 decorated coordinates and genuine "
            "multi-term cancellation; no current theorem turns the global "
            "maximum-anchor/minimum-support choice into singleton target "
            "support or deletes such a cancellation"
        ),
        "normalization_warning": (
            "maximum-anchor/minimum-support is a lexicographic choice among "
            "exact sources, not an additional coefficient row.  Since the "
            "11-coordinate stratum is empty, it does not imply that an "
            "exact minimizer has 11 coordinates"
        ),
        "sharp_remaining_statement": (
            "axis-purified multisite concentration/cancellation: show that "
            "a minimum exact source with more than one monomial in a pure "
            "target row admits a support-lowering switch, or yields an "
            "existing unit/coloop/active carrier"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "Segre-bright full-row/minimum-support completion gate",
        "pins": PINS,
        "local_full_row_consequence": local_bright_target_mismatch(),
        "smallest_axis_pure_completion": smallest_axis_pure_completion(),
        "routed_and_open_branches": routed_and_open_branches(),
        "verdict": (
            "the full unary and pure-target rows do not directly annihilate "
            "the Segre-bright conormal: the target fixes the sum channel, "
            "while the cylinder curvature t*k lies in the matching-"
            "difference channel and survives the complete-row coefficient "
            "quotient.  The rows force an additional response "
            "occurrence, and the smallest 11-coordinate axis-pure completion "
            "is impossible because both crossed rows acquire a unique "
            "nonzero monomial.  Any offdiagonal enlargement enters the "
            "existing fan/coloop alternative.  The only uneliminated full-"
            "source possibility is a larger axis-purified cancellation "
            "packet; maximum-anchor/minimum-support alone does not yet "
            "remove it."
        ),
        "scope": (
            "canonical h=3 six-residual-site one-bad equations over a field. "
            "The 11-coordinate axis-pure stratum is exhausted exactly; no "
            "full GHZ counterexample or global source-locus emptiness is claimed."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("full pure row adds one occurrence beyond the local bright block")
    print("axis-pure 11-coordinate completions: 30375 supports")
    print("unary + both diagonals exact: 360 supports / 1440 orientations")
    print("crossed profile: G12=1, G21=1 in every orientation")
    print("smallest full-row completion: IMPOSSIBLE")
    print("remaining branch: LARGER AXIS-PURIFIED CANCELLATION")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
