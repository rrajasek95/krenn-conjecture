#!/usr/bin/env python3
"""Smallest active curved doubly-good OO full-nine source certificate.

Start from the exact alternating-C8 two-anchor OO packet.  A third diagonal
anchor needs at least three added 11-cells.  There are 30 minimum completions,
19 with both selected arm cofactors support-active.  Every one of those 19
has an ordinary two-row source certificate.

For the canonical completion

    x=A03(1,1), y=A15(1,1), z=A67(1,1),

the pure diagonal row and one mixed row are

    g_diag = x*y*z - 1,
    g_mix  = y*z.

The mixed word 11001111 has endpoint labels pq:10 (off-diagonal) and pr:11
(diagonal).  Thus x*g_mix-g_diag=1 is an ordinary polynomial source unit.
No Ward, Hasse, jet, cap codomain, or solver output enters the proof.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
COMPUTATIONS = ROOT / "computations"
sys.path.insert(0, str(COMPUTATIONS))
PINS = {
    "computations/verify_oo_doubly_good_two_anchor_counterguard.py":
        "b9d986f4e1725082c1101e73729018a6d66296aef628879de50b03508f804699",
    "computations/verify_oo_c8_two_cell_activity_frontier.py":
        "4dc77d50d206fe1eb4f2581cc1310733b5440f18bd0bf6148dd4250cf3c4dd37",
    "computations/verify_oo_c8_minimal_third_anchor_activity.py":
        "16d481c1ed838d96ba58315703cf8e13b71aabc5067e2a8555d85a0ad4b94f38",
    "computations/verify_oo_lambda_conservation_all_order.py":
        "72402e9a3e97e72b1547349f80943950e0c6d521d46adfd6ef4baefb82a4d0b3",
}
EXPECTED_LEDGER_SHA256 = (
    "1d03eb2c35c4a7194ebd5c95383b454d024bc7b7bdcc3830722a2f3ac3b70fe5"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_pinned(name, relative):
    path = ROOT / relative
    actual = sha256(path.read_bytes()).hexdigest()
    require(actual == PINS[relative],
            f"dependency changed: {relative}: {actual}")
    spec = spec_from_file_location(name, path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BASE_PATH = "computations/verify_oo_doubly_good_two_anchor_counterguard.py"
FRONTIER_PATH = "computations/verify_oo_c8_two_cell_activity_frontier.py"
MINIMUM_PATH = "computations/verify_oo_c8_minimal_third_anchor_activity.py"
LAMBDA_PATH = "computations/verify_oo_lambda_conservation_all_order.py"


base = load_pinned("oo_two_anchor", BASE_PATH)
frontier = load_pinned("oo_activity_frontier", FRONTIER_PATH)
minimum = load_pinned("oo_minimum_anchor", MINIMUM_PATH)
# Pin the no-go as an explicit scope guard.  It is deliberately not imported:
# the present proof adds literal physical source rows rather than another
# element of the conserved Ward/Hasse codomain.
require(sha256((ROOT / LAMBDA_PATH).read_bytes()).hexdigest()
        == PINS[LAMBDA_PATH], "the all-order Lambda/Hasse no-go changed")


PURE_ONE = (1,) * 8
MIXED_WORD = (1, 1, 0, 0, 1, 1, 1, 1)
CANONICAL_ADDED = (
    (0, 3, 1, 1),
    (1, 5, 1, 1),
    (6, 7, 1, 1),
)


def add_polynomials(left, right, right_scale=1):
    answer = defaultdict(Fraction)
    for mask, coefficient in left.items():
        answer[mask] += Fraction(coefficient)
    for mask, coefficient in right.items():
        answer[mask] += Fraction(right_scale) * coefficient
    return {mask: coefficient for mask, coefficient in answer.items()
            if coefficient}


def multiply_squarefree(polynomial, factor_mask, scalar=1):
    answer = {}
    for mask, coefficient in polynomial.items():
        require(not (mask & factor_mask),
                "the ordinary certificate acquired a repeated variable")
        answer[mask | factor_mask] = Fraction(scalar) * coefficient
    return answer


def mask_name(mask, variables):
    factors = [variables[index] for index in range(len(variables))
               if mask & (1 << index)]
    return "*".join(factors) if factors else "1"


def minimum_anchor_audit(blocks):
    missing_histogram = Counter()
    for matching in base.perfect_matchings(base.VERTICES):
        missing = sum(base.key(u, v, 1, 1) not in blocks
                      for u, v in matching)
        missing_histogram[missing] += 1
    require(missing_histogram == Counter({3: 30, 4: 75}),
            "the pure-1 minimum completion count changed")
    completions = minimum.minimal_anchor_completions(blocks)
    require(len(completions) == 30
            and all(len(completion) == 3 for completion in completions),
            "the minimum three-cell anchor completions changed")
    return completions, missing_histogram


def certificate_for_completion(blocks, added):
    tensor = frontier.tensor_polynomials(blocks, added)
    residuals = frontier.target_residuals(tensor)
    pure = residuals.get(PURE_ONE)
    require(pure == {0: Fraction(-1), 7: Fraction(1)},
            "a minimum completion changed its pure diagonal row")
    candidates = []
    for word, polynomial in residuals.items():
        if len(set(word)) == 1 or len(polynomial) != 1:
            continue
        mask, coefficient = next(iter(polynomial.items()))
        require(mask and mask & ~7 == 0 and coefficient,
                "a mixed monomial left the three-variable packet")
        candidates.append((-mask.bit_count(), word, mask, coefficient))
    require(candidates, "a minimum completion lost every mixed monomial row")
    _negative_degree, word, mask, coefficient = min(candidates)
    complement = 7 ^ mask
    lifted = multiply_squarefree(
        residuals[word], complement, Fraction(1, coefficient)
    )
    certificate = add_polynomials(lifted, pure, -1)
    require(certificate == {0: Fraction(1)},
            "the two-row ordinary source certificate changed")
    return {
        "added": [f"{u}{v}:{i}{j}" for u, v, i, j in added],
        "mixed_word": list(word),
        "pq_label": f"{word[base.P]}{word[base.Q]}",
        "pr_label": f"{word[base.P]}{word[base.R]}",
        "mixed_mask": mask,
        "mixed_coefficient": str(coefficient),
        "multiplier_mask": complement,
        "certificate": "multiplier*mixed_row-pure_row=1",
    }


def all_minimum_active_certificates(blocks, completions):
    records = []
    activity = Counter()
    best_histogram = Counter()
    for added in completions:
        active = tuple(arm for arm in frontier.ARMS
                       if frontier.is_support_active(blocks, added, arm))
        activity[active] += 1
        if active != frontier.ARMS:
            continue
        record = certificate_for_completion(blocks, added)
        best_histogram[
            int(record["mixed_mask"]).bit_count(),
            int(record["multiplier_mask"]).bit_count(),
            record["pq_label"],
            record["pr_label"],
        ] += 1
        records.append(record)
    require(activity == Counter({
        frontier.ARMS: 19,
        (frontier.ARMS[1],): 8,
        (frontier.ARMS[0],): 3,
    }), "the minimum arm-activity split changed")
    require(len(records) == 19,
            "the minimum doubly-active certificate count changed")
    require(best_histogram == Counter({
        (2, 1, "10", "11"): 5,
        (2, 1, "10", "10"): 5,
        (2, 1, "01", "02"): 3,
        (2, 1, "01", "00"): 3,
        (2, 1, "12", "10"): 2,
        (1, 2, "01", "01"): 1,
    }), f"the minimum source-certificate palette changed: {best_histogram}")
    return records, activity, best_histogram


def matching_terms(blocks, added, target_word):
    added_by_pair = defaultdict(list)
    for index, cell in enumerate(added):
        u, v, i, j = cell
        added_by_pair[u, v].append((i, j, 1 << index))
    terms = []
    for matching in base.perfect_matchings(base.VERTICES):
        choices = []
        for u, v in matching:
            available = [
                (i, j, 0)
                for i in base.COLORS for j in base.COLORS
                if base.entry(blocks, u, v, i, j)
            ] + added_by_pair[u, v]
            if not available:
                choices = []
                break
            choices.append(available)
        for selected in product(*choices) if choices else ():
            word = [None] * 8
            mask = 0
            for (u, v), (i, j, local_mask) in zip(
                    matching, selected, strict=True):
                word[u], word[v] = i, j
                mask |= local_mask
            if tuple(word) == target_word:
                terms.append((tuple(tuple(sorted(edge)) for edge in matching),
                              mask))
    return tuple(terms)


def canonical_packet(blocks):
    added = CANONICAL_ADDED
    tensor = frontier.tensor_polynomials(blocks, added)
    residuals = frontier.target_residuals(tensor)
    require(residuals[PURE_ONE] == {0: Fraction(-1), 7: Fraction(1)}
            and residuals[MIXED_WORD] == {6: Fraction(1)},
            "the canonical diagonal/off-diagonal rows changed")
    lifted = multiply_squarefree(residuals[MIXED_WORD], 1)
    require(add_polynomials(lifted, residuals[PURE_ONE], -1)
            == {0: Fraction(1)},
            "x*g_mix-g_diag stopped being one")

    pure_terms = matching_terms(blocks, added, PURE_ONE)
    mixed_terms = matching_terms(blocks, added, MIXED_WORD)
    require(pure_terms == ((((0, 3), (1, 5), (2, 4), (6, 7)), 7),)
            and mixed_terms == ((((0, 4), (1, 5), (2, 3), (6, 7)), 6),),
            "the canonical source matching provenance changed")

    numeric = dict(blocks)
    for u, v, i, j in added:
        base.add_cell(numeric, u, v, i, j)
    direct_ranks = (
        base.rational_rank(base.direct_matrix(numeric, base.P, base.Q)),
        base.rational_rank(base.direct_matrix(numeric, base.P, base.R)),
    )
    star_ranks = (
        base.star_rank(numeric, base.P, base.Q),
        base.star_rank(numeric, base.Q, base.P),
        base.star_rank(numeric, base.P, base.R),
        base.star_rank(numeric, base.R, base.P),
    )
    curvature = (
        base.entry(numeric, base.P, base.Q, 1, 0)
        * base.entry(numeric, base.R, base.FOURTH, 1, 0)
        - base.entry(numeric, base.P, base.R, 1, 1)
        * base.entry(numeric, base.Q, base.FOURTH, 0, 0)
    )
    require(direct_ranks == (1, 1) and star_ranks == (3, 3, 3, 3)
            and curvature == -1,
            "the canonical curved doubly-good structure changed")
    rulings = (
        base.audit_ruling(numeric, (base.P, base.Q), 0),
        base.audit_ruling(numeric, (base.P, base.R), 1),
    )
    require(rulings == ((3,), (base.Q,)),
            "the active target-2 ruling ledger changed")

    cofactors = {
        "pq": frontier.cofactor_polynomials(
            blocks, added, (base.P, base.Q)
        ),
        "pr": frontier.cofactor_polynomials(
            blocks, added, (base.P, base.R)
        ),
    }
    require(cofactors == {
        "pq": {
            (1, 2, 2, 1, 0, 0): {2: Fraction(1)},
            (1, 2, 2, 1, 1, 1): {6: Fraction(1)},
        },
        "pr": {
            (1, 0, 0, 1, 0, 0): {2: Fraction(1)},
            (1, 0, 0, 1, 1, 1): {6: Fraction(1)},
        },
    }, "the two active cofactor polynomials changed")

    # Audit every full-nine label.  There are 3^6 residual words for each
    # endpoint-colour label in either pair chart.  Zero rows are retained as
    # exact zero equations; the sparse residual dictionary stores only the
    # nine nonzero equations.
    label_census = {}
    residual_label_histograms = {}
    for chart, endpoints in (("pq", (base.P, base.Q)),
                             ("pr", (base.P, base.R))):
        label_census[chart] = {
            f"{i}{j}": 3 ** 6 for i in base.COLORS for j in base.COLORS
        }
        histogram = Counter(
            f"{word[endpoints[0]]}{word[endpoints[1]]}"
            for word in residuals
        )
        residual_label_histograms[chart] = dict(sorted(histogram.items()))
    require(label_census == {
        "pq": {f"{i}{j}": 729 for i in base.COLORS for j in base.COLORS},
        "pr": {f"{i}{j}": 729 for i in base.COLORS for j in base.COLORS},
    }, "the full-nine labelled row census changed")
    require(residual_label_histograms == {
        "pq": {"00": 1, "10": 4, "11": 2, "12": 2},
        "pr": {"00": 1, "10": 2, "11": 4, "12": 2},
    }, "the canonical nonzero full-nine label histogram changed")

    require(not any(polynomial == {0: coefficient}
                    for polynomial in residuals.values()
                    for coefficient in polynomial.values()),
            "a single ordinary source row became a scalar unit")
    return {
        "support_cells": len(blocks) + len(added),
        "variables": ["x=A03_11", "y=A15_11", "z=A67_11"],
        "direct_arm_ranks": list(direct_ranks),
        "good_star_ranks": list(star_ranks),
        "curvature": str(curvature),
        "active_ruling_nonzero_sites": [list(value) for value in rulings],
        "cofactor_polynomials": {
            chart: [
                [list(word), [[mask, str(coefficient)]
                              for mask, coefficient in sorted(poly.items())]]
                for word, poly in sorted(rows.items())
            ] for chart, rows in cofactors.items()
        },
        "full_nine_rows_per_chart": 3 ** 8,
        "full_nine_labels_per_chart": 9,
        "residual_words_per_label": 3 ** 6,
        "nonzero_residual_label_histograms": residual_label_histograms,
        "pure_diagonal_row": "x*y*z-1",
        "mixed_word": list(MIXED_WORD),
        "mixed_labels": {"pq": "10 offdiagonal", "pr": "11 diagonal"},
        "mixed_row": "y*z",
        "ordinary_certificate": "x*(y*z)-(x*y*z-1)=1",
        "certificate_rows": 2,
        "single_row_unit": False,
        "pure_matching": [list(edge) for edge in pure_terms[0][0]],
        "mixed_matching": [list(edge) for edge in mixed_terms[0][0]],
    }


def main():
    blocks = base.build_packet()
    require(len(blocks) == 11,
            "the alternating-C8 two-anchor packet size changed")
    completions, missing_histogram = minimum_anchor_audit(blocks)
    records, activity, palette = all_minimum_active_certificates(
        blocks, completions
    )
    canonical = canonical_packet(blocks)

    ledger = {
        "pins": PINS,
        "lambda_hasse_scope_guard": (
            "the new proof uses two literal physical full-nine source rows; "
            "it does not add a Ward, jet, Hasse, or cap-codomain generator"
        ),
        "pure_one_matching_missing_cell_histogram": dict(sorted(
            missing_histogram.items()
        )),
        "minimum_added_cells": 3,
        "minimum_anchor_completions": len(completions),
        "minimum_activity_histogram": [
            [[list(arm) for arm in arms], count]
            for arms, count in sorted(activity.items(), key=str)
        ],
        "minimum_doubly_active_completions": len(records),
        "minimum_certificate_palette": [
            [list(key), count] for key, count in sorted(palette.items())
        ],
        "minimum_active_certificates": records,
        "canonical_packet": canonical,
        "verdict": (
            "no rational full-row packet exists at the smallest active "
            "curved doubly-good OO completion: all 19 minimum doubly-active "
            "supports have ordinary two-row source certificates, with the "
            "canonical identity x*g_mix-g_diag=1"
        ),
        "scope": (
            "the minimum three-cell completion of the frozen alternating-C8 "
            "two-anchor OO chart; larger active completions and arbitrary "
            "curved OO sources are not classified"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"minimal curved OO full-nine ledger changed: {digest}")

    print("minimal active curved doubly-good OO full-nine unit: PASS")
    print("minimum third-anchor completions / doubly-active: 30 / 19")
    print("all 19 active packets: ordinary two-row source unit")
    print("canonical rows: g_diag=x*y*z-1, g_mix=y*z")
    print("certificate: x*g_mix-g_diag=1")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
