#!/usr/bin/env python3
"""Classify homogeneous spoke restrictions after the rank-two theorem.

Fix x=(q23[00],q24[00],q25[00]).  Every h=3 response occurrence contains
at most one selected spoke.  For a fixed word w, a spoke q2j[00] can occur
only when w2=wj=0.  This gives the complete structural support-mask census
of the 729 words and shows exactly what the ungraded rank-two conclusion of
4f7f104 can, and cannot, promote to a literal word/head block.

The checker also gives a smallest physical restriction counterguard.  Its
target row and two target-zero R21 word rows have total rank three, hence
quotient rank two, but the two transverse directions live in distinct word
blocks and each row contains two cancelling occurrences.  No literal
response coefficient is private.  All q tails in the two rows are pure and
their endpoint holes lie in one closed star, so neither an offdiagonal-q nor
an outside-shore exit follows from the restriction packet alone.

This is a full 729-word/four-head response-map restriction audit, not a full
GHZ source: the other constant-colour target normalizations and augmented
anchor/ridge rows are not imposed by the counterguard.
"""

from __future__ import annotations

import ast
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_active_coloop_spoke_affine_rank_or_deletion_gate.py":
        "cca8b51508756c13f169c6fe079ef9681b645098463d1f64342b0364d0cd4c9c",
    "notes/h3-active-coloop-spoke-affine-rank-or-deletion-gate.md":
        "26a01b0823de811092bb502234eff06d95a13d5545514d4191c552a6dd2143cb",
    "computations/verify_h3_active_coloop_literal_packet_termination_scope.py":
        "ad369a692aa2a7bde3b30a0a4cba5e401b6e61afc62dd752a4f51781a9e6485e",
    "notes/h3-active-coloop-literal-packet-termination-scope.md":
        "1201ea94d8faafefefeaff81a47987e41a817c4775fc98057294ed80fdfe51c5",
    "computations/verify_h3_active_fan_coloop_or_four_good.py":
        "93030f2994e2e6a2052a09a5fefd179c99e0b8fb55cd0c77bee2cb9f8dbc6bb4",
    "computations/verify_h3_active_fan_coloop_saturation_boundary.py":
        "35658ebed521b93387fc00aa7d2600d703f57b3e5e5deca67a11a1ab155d6c56",
}
EXPECTED_LEDGER_SHA256 = (
    "9084ea35b02ebc0eb3e1489642374ebee4d9a6a0612ea2a537b00bae0fdb0f3c"
)

SITES = tuple(range(6))
COLOURS = tuple(range(3))
HEADS = tuple(range(2))
X_EDGES = ((2, 3), (2, 4), (2, 5))
X_LABELS = tuple((left, right, 0, 0) for left, right in X_EDGES)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def edge(left: int, right: int) -> tuple[int, int]:
    return (left, right) if left < right else (right, left)


def q_label(left: int, right: int, left_colour: int, right_colour: int):
    if left > right:
        left, right = right, left
        left_colour, right_colour = right_colour, left_colour
    return (left, right, left_colour, right_colour)


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted((edge(first, second),) + tail))


MATCHINGS6 = tuple(perfect_matchings(SITES))


def product(values):
    answer = Q(1)
    for value in values:
        answer *= value
    return answer


def rank(rows) -> int:
    work = [list(map(Q, row)) for row in rows]
    if not work:
        return 0
    pivot = 0
    for column in range(len(work[0])):
        selected = next((row for row in range(pivot, len(work))
                         if work[row][column]), None)
        if selected is None:
            continue
        work[pivot], work[selected] = work[selected], work[pivot]
        value = work[pivot][column]
        work[pivot] = [entry / value for entry in work[pivot]]
        for row in range(len(work)):
            if row == pivot or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right
                         in zip(work[row], work[pivot], strict=True)]
        pivot += 1
    return pivot


def word_label(word) -> str:
    return "".join(map(str, word))


def structural_block_census() -> dict[str, object]:
    """Classify which selected spokes are allowed by each output word."""
    masks = Counter()
    for word in itertools.product(COLOURS, repeat=6):
        visible = tuple(index for index, (_left, right) in enumerate(X_EDGES)
                        if word[2] == word[right] == 0)
        masks[len(visible)] += 1
    require(masks == Counter({0: 558, 1: 108, 2: 54, 3: 9}), masks)

    # Direct response terms have 15 q^3 occurrences; endpoint response terms
    # have 90 ordered p*s*q^2 occurrences.  No occurrence uses two x spokes.
    direct = MATCHINGS6
    endpoint = []
    for p_site in SITES:
        for s_site in SITES:
            if p_site == s_site:
                continue
            remaining = tuple(site for site in SITES
                              if site not in (p_site, s_site))
            endpoint.extend((p_site, s_site, matching)
                            for matching in perfect_matchings(remaining))
    require(len(direct) == 15 and len(endpoint) == 90,
            (len(direct), len(endpoint)))
    direct_histogram = Counter(
        sum(physical in X_EDGES for physical in matching)
        for matching in direct
    )
    endpoint_histogram = Counter(
        sum(physical in X_EDGES for physical in matching)
        for _p, _s, matching in endpoint
    )
    require(direct_histogram == Counter({0: 6, 1: 9}), direct_histogram)
    require(endpoint_histogram == Counter({0: 54, 1: 36}),
            endpoint_histogram)
    require(max(direct_histogram) == max(endpoint_histogram) == 1,
            "a fine occurrence used two selected spokes")

    return {
        "word_support_mask_histogram": dict(sorted(masks.items())),
        "four_head_block_histogram": {
            str(size): 4 * count for size, count in sorted(masks.items())
        },
        "structural_rule": (
            "q2j[00] can occur in word w iff w2=wj=0; endpoint/head "
            "choices and coefficient cancellation can only shrink this mask"
        ),
        "fine_occurrences_per_response_coefficient": {
            "direct_d_q3": len(direct),
            "ordered_p_s_q2": len(endpoint),
            "total": len(direct) + len(endpoint),
        },
        "selected_spoke_incidence": {
            "direct": dict(sorted(direct_histogram.items())),
            "endpoint": dict(sorted(endpoint_histogram.items())),
        },
        "fine_grade_warning": (
            "each monomial occurrence is spoke-singleton, but the physical "
            "equation is the complete word/head sum; a monomial tag is not "
            "itself a source row"
        ),
    }


def guard_values():
    # A normalized pure-zero coloop with three occupied cofactor tails.
    q_values = {
        q_label(0, 1, 0, 0): Q(1),
        q_label(2, 3, 0, 0): Q(1),
        q_label(2, 4, 0, 0): Q(1),
        q_label(2, 5, 0, 0): Q(-1),
        q_label(4, 5, 0, 0): Q(1),
        q_label(3, 5, 0, 0): Q(1),
        q_label(3, 4, 0, 0): Q(1),
        # Pure mate tails for the two response blocks below.
        q_label(1, 3, 0, 0): Q(-1),
        q_label(1, 4, 0, 0): Q(1),
        q_label(1, 5, 0, 0): Q(1),
    }
    p_values = {
        # Head colour equals the site/output colour: these endpoint cells are
        # diagonal, so the offdiagonal private-site theorem does not fire.
        (1, 5, 1): Q(1),
        (1, 3, 1): Q(1),
    }
    s_values = {(0, 0, 0): Q(1)}
    # The direct d*q^3 response part and the other three response heads vanish.
    d_values = {}
    return p_values, s_values, q_values, d_values


def target_terms(word, q_values):
    answer = []
    for matching in MATCHINGS6:
        cells = tuple(q_label(left, right, word[left], word[right])
                      for left, right in matching)
        value = product(q_values.get(cell, Q(0)) for cell in cells)
        if value:
            answer.append((matching, cells, value))
    return tuple(answer)


def response_terms(head_p, head_s, word, p_values, s_values, q_values,
                   d_values):
    answer = []
    direct_value = d_values.get((head_p, head_s), Q(0))
    if direct_value:
        for matching, cells, q_value in target_terms(word, q_values):
            answer.append(("D", None, None, matching, cells,
                           direct_value * q_value))
    for p_site in SITES:
        p_value = p_values.get((head_p, p_site, word[p_site]), Q(0))
        if not p_value:
            continue
        for s_site in SITES:
            if p_site == s_site:
                continue
            s_value = s_values.get((head_s, s_site, word[s_site]), Q(0))
            if not s_value:
                continue
            residual = tuple(site for site in SITES
                             if site not in (p_site, s_site))
            for matching in perfect_matchings(residual):
                cells = tuple(q_label(left, right, word[left], word[right])
                              for left, right in matching)
                value = p_value * s_value * product(
                    q_values.get(cell, Q(0)) for cell in cells
                )
                if value:
                    answer.append(("PS", p_site, s_site, matching, cells,
                                   value))
    return tuple(answer)


def restriction_from_terms(terms):
    answer = [Q(0), Q(0), Q(0)]
    fine = [[] for _ in X_LABELS]
    for term in terms:
        cells = term[-2]
        value = term[-1]
        used = [index for index, label in enumerate(X_LABELS)
                if label in cells]
        require(len(used) <= 1, (term, used))
        if not used:
            continue
        index = used[0]
        x_value = GUARD_Q[X_LABELS[index]]
        coefficient = value / x_value
        answer[index] += coefficient
        fine[index].append({
            "kind": term[0],
            "p": term[1],
            "s": term[2],
            "matching": repr(term[3]),
            "coefficient": str(coefficient),
        })
    return tuple(answer), tuple(tuple(values) for values in fine)


GUARD_P, GUARD_S, GUARD_Q, GUARD_D = guard_values()


def literal_counterguard() -> dict[str, object]:
    x = tuple(GUARD_Q[label] for label in X_LABELS)
    require(x == (Q(1), Q(1), Q(-1)), x)

    target_rows = {}
    target_nonzero_values = {}
    target_occurrence_histogram = Counter()
    response_rows = {}
    response_nonzero_values = {}
    response_occurrence_histogram = Counter()
    response_fine = {}
    private_response_coefficients = []

    for word in itertools.product(COLOURS, repeat=6):
        label = word_label(word)
        terms = target_terms(word, GUARD_Q)
        target_occurrence_histogram[len(terms)] += 1
        value = sum((term[-1] for term in terms), Q(0))
        row, _fine = restriction_from_terms(
            (("Q", None, None, matching, cells, term_value)
             for matching, cells, term_value in terms)
        )
        if any(row):
            target_rows[label] = row
        if value:
            target_nonzero_values[label] = value

        for head_p in HEADS:
            for head_s in HEADS:
                block = f"R{head_p + 1}{head_s + 1}[{label}]"
                response = response_terms(
                    head_p, head_s, word,
                    GUARD_P, GUARD_S, GUARD_Q, GUARD_D,
                )
                response_occurrence_histogram[len(response)] += 1
                if len(response) == 1:
                    private_response_coefficients.append(block)
                response_value = sum((term[-1] for term in response), Q(0))
                row, fine = restriction_from_terms(response)
                if any(row):
                    response_rows[block] = row
                    response_fine[block] = fine
                if response_value:
                    response_nonzero_values[block] = response_value

    target = (Q(1), Q(1), Q(1))
    expected_response = {
        "R21[000001]": (Q(1), Q(-1), Q(0)),
        "R21[000100]": (Q(0), Q(1), Q(1)),
    }
    require(target_rows == {"000000": target}, target_rows)
    require(target_nonzero_values == {"000000": Q(1)},
            target_nonzero_values)
    require(response_rows == expected_response, response_rows)
    require(not response_nonzero_values, response_nonzero_values)
    require(not private_response_coefficients, private_response_coefficients)
    require(response_occurrence_histogram == Counter({0: 2914, 2: 2}),
            response_occurrence_histogram)
    require(target_occurrence_histogram == Counter({0: 728, 3: 1}),
            target_occurrence_histogram)
    require(rank((target,) + tuple(response_rows.values())) == 3,
            response_rows)
    require(all(sum(value != 0 for value in row) == 2
                for row in response_rows.values()), response_rows)
    require(all(sum(left * right for left, right
                    in zip(row, x, strict=True)) == 0
                for row in response_rows.values()), (response_rows, x))

    # Every nonzero pure-zero target matching retains the coloop 01.
    pure_terms = target_terms((0,) * 6, GUARD_Q)
    require(len(pure_terms) == 3
            and all((0, 1) in matching for matching, _cells, _value
                    in pure_terms), pure_terms)

    # The four fine response occurrences use only pure q cells and holes in
    # the closed star centred at site 0.
    fine_occurrences = []
    holes = set()
    for block, fine_by_spoke in response_fine.items():
        for fine_items in fine_by_spoke:
            for item in fine_items:
                fine_occurrences.append((block, item))
                holes.add(edge(item["p"], item["s"]))
    require(len(fine_occurrences) == 4, fine_occurrences)
    require(holes == {(0, 3), (0, 5)}, holes)
    closed_star = {edge(0, site) for site in range(1, 6)}
    require(holes <= closed_star, (holes, closed_star))
    for block, fine_by_spoke in response_fine.items():
        for fine_items in fine_by_spoke:
            for item in fine_items:
                # All words use mixed endpoint colours, but every q cell in
                # the actual occurrence is [00].
                matching = ast.literal_eval(item["matching"])
                word = tuple(map(int, block.split("[")[1][:-1]))
                cells = tuple(q_label(left, right, word[left], word[right])
                              for left, right in matching)
                require(all(cell[2:] == (0, 0) for cell in cells),
                        (block, cells))

    return {
        "literal_coloop": "alpha=q01[00]=1",
        "occupied_spokes_x": [str(value) for value in x],
        "mate_target_row_y": [str(value) for value in target],
        "cofactor_normalization": "x dot y=1+1-1=1",
        "nonzero_target_restrictions": {
            key: [str(value) for value in row]
            for key, row in target_rows.items()
        },
        "nonzero_response_restrictions": {
            key: [str(value) for value in row]
            for key, row in response_rows.items()
        },
        "response_values_at_x": {
            key: str(sum(left * right for left, right
                         in zip(row, x, strict=True)))
            for key, row in response_rows.items()
        },
        "total_rank_with_target": 3,
        "quotient_rank_mod_target": 2,
        "word_blocks_used": len(response_rows),
        "local_quotient_rank_per_used_block": 1,
        "literal_response_occurrence_histogram":
            dict(sorted(response_occurrence_histogram.items())),
        "literal_private_response_coefficients": 0,
        "fine_spoke_occurrences": len(fine_occurrences),
        "fine_occurrence_packet": fine_occurrences,
        "pure_q_tail_only": True,
        "diagonal_endpoint_cells_only": True,
        "endpoint_holes": [repr(value) for value in sorted(holes)],
        "one_closed_shore_containing_both_holes":
            [repr(value) for value in sorted(closed_star)],
        "scope": (
            "literal full 729-word/four-head restriction of the displayed "
            "h=3 polynomial support.  It satisfies its pure-zero coloop "
            "normalization and all supported mixed response cancellations; "
            "it does not impose the other constant-colour GHZ targets or "
            "the augmented anchor/ridge packet."
        ),
    }


def block_linear_algebra() -> dict[str, object]:
    # If the quotient of the sum of homogeneous block images has dimension
    # two, either one block already has dimension two or two distinct blocks
    # contribute distinct quotient lines.  The literal guard realizes the
    # latter with the least possible number of blocks and nonprivate entries.
    target = (Q(1), Q(1), Q(1))
    left = (Q(1), Q(-1), Q(0))
    right = (Q(0), Q(1), Q(1))
    require(rank((target, left)) == rank((target, right)) == 2,
            (target, left, right))
    require(rank((target, left, right)) == 3, (target, left, right))
    return {
        "exhaustive_block_alternative": (
            "if the total image in k^3/<y> has dimension two, either one "
            "homogeneous block has quotient image dimension two, or at "
            "least two blocks have distinct nonzero quotient lines"
        ),
        "weak_homogeneous_promotion": (
            "some literal word/head block is transverse to the target line; "
            "global rank two cannot be hidden from every block"
        ),
        "private_promotion": "false without another source theorem",
        "sharp_minimality": {
            "blocks": (
                "one scalar word/head row has quotient dimension at most "
                "one, so the split alternative needs at least two blocks"
            ),
            "spoke_occurrence_incidences": (
                "without a singleton/private row, each of the two required "
                "rows has support at least two; four incidences are minimal"
            ),
            "guard_attains_both_bounds": True,
        },
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 active-coloop homogeneous spoke-block split gate",
        "pins": PINS,
        "structural_block_classification": structural_block_census(),
        "block_rank_alternative": block_linear_algebra(),
        "smallest_literal_split_counterguard": literal_counterguard(),
        "effect_on_93cf9ae": {
            "not_supplied": (
                "the three named private target-zero rows R11[110000], "
                "R11[110011], R11[111100]"
            ),
            "why": (
                "a two-occurrence coefficient can vanish by cancellation "
                "inside its own word block and therefore forces no alternate "
                "mate.  Combining the two blocks would mix fine words."
            ),
            "hall_scope": (
                "the counterguard uses pure q tails and endpoint holes 03,05 "
                "inside one closed star, so neither the offdiagonal-q/four-"
                "good route nor strict outside-shore growth is automatic."
            ),
        },
        "shortest_remaining_theorem": (
            "homogeneous private-tail synchronization: for two distinct "
            "target-zero word/head blocks whose spoke restrictions span "
            "k^3/<y>, either one complete coefficient is private modulo the "
            "closed shore (and enters 93cf9ae after the required typed "
            "relabeling), or their cancellation has a source-valid common-"
            "word Hasse/Cartan comparison yielding a typed outside-shore, "
            "four-good, or augmented terminal."
        ),
        "scope": (
            "exact h=3 response-polynomial block classification and literal "
            "restriction counterguard.  It does not claim a complete GHZ "
            "source or contradict the minimum-support theorem of 4f7f104."
        ),
    }
    digest = sha256(json.dumps(ledger, sort_keys=True,
                               separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("word/head spoke masks: 0/1/2/3 CLASSIFIED")
    print("rank two modulo target: HOMOGENEOUS TRANSVERSE BLOCK FORCED")
    print("block-local private row: NOT FORCED")
    print("smallest split guard: TWO WORDS / FOUR FINE OCCURRENCES")
    print("93cf9ae entry: NEEDS PRIVATE-TAIL SYNCHRONIZATION")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
