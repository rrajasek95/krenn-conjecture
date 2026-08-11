#!/usr/bin/env python3
r"""First higher anchor-relevant S-pair beyond the rootless C5 Tate audit.

The degree-five Tate label relations of 189791f are not a Schreyer-complete
set for the full polynomial source module.  In the nearest C5 word sector,
the first new anchor-relevant syzygy is the ordinary Koszul relation between
the pure row F0=H0-u and a Hamming-one mixed row Fw=Hw.

This checker constructs the complete 181-column fine component, proves its
rank is 180 and its kernel is exactly the displayed Koszul vector.  Its pure
coefficient is Hw, so its typed readout is (-Hw,0,Hw,0): it retains the old
anchor-target lock and cannot supply the primitive invisible anchor.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = "700bd61256d2f43f41c924732ccbde512130d9b741e56556fd6ff76f6b2cd5e2"
PINS = {
    "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py":
        "190171b72493e661dedb8e7aa369a9b72f1a71e14487632df2841ca7eeb19bf4",
    "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py":
        "719e48963faac5cd1dc5e7348de41e86f690f3046fefba88dddfa60bae532899",
}

PURE_WORD = (0,) * 8
MIXED_WORD = (0, 1, 0, 0, 0, 0, 0, 0)
ZERO = Q(0)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"pinned dependency changed: {relative}")


def load(relative: str, name: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, ("cannot import", path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def degree_add(left, right):
    return tuple(a + b for a, b in zip(left, right, strict=True))


def word_degree(word):
    degree = [0] * 24
    for site, colour in enumerate(word):
        degree[3 * site + colour] += 1
    return tuple(degree)


# Polynomial monomials are (u exponent, sorted tuple of decorated edge cells).
def monomial_multiply(left, right):
    return left[0] + right[0], tuple(sorted(left[1] + right[1]))


def polynomial_multiply(left, right):
    answer = Counter()
    for left_term, left_value in left.items():
        for right_term, right_value in right.items():
            answer[monomial_multiply(left_term, right_term)] += (
                left_value * right_value
            )
    return Counter({term: value for term, value in answer.items() if value})


def polynomial_add(*values):
    answer = Counter()
    for value in values:
        answer.update(value)
    return Counter({term: coefficient for term, coefficient in answer.items()
                    if coefficient})


def scale(value, scalar):
    return Counter({term: scalar * coefficient for term, coefficient in
                    value.items() if scalar * coefficient})


def sparse_rank(columns):
    pivots = {}
    for source in columns:
        column = {row: Q(value) for row, value in source.items() if value}
        while column:
            pivot = min(column, key=repr)
            value = column[pivot]
            if pivot not in pivots:
                column = {row: coefficient / value
                          for row, coefficient in column.items()}
                pivots[pivot] = column
                break
            factor = value
            for row, coefficient in pivots[pivot].items():
                new_value = column.get(row, ZERO) - factor * coefficient
                if new_value:
                    column[row] = new_value
                else:
                    column.pop(row, None)
    return len(pivots), len(set().union(*(set(column) for column in columns)))


def audit(base):
    h0 = Counter({(0, monomial): Q(1)
                  for monomial in base.full_row(PURE_WORD)})
    hw = Counter({(0, monomial): Q(1)
                  for monomial in base.full_row(MIXED_WORD)})
    u = Counter({(1, ()): Q(1)})
    f0 = polynomial_add(h0, scale(u, Q(-1)))
    fw = hw
    require(len(h0) == len(hw) == 90 and len(f0) == 91,
            "direct-free row support changed")

    target_degree = degree_add(word_degree(PURE_WORD), word_degree(MIXED_WORD))
    require(sum(target_degree) == 16,
            "first pure/mixed Koszul fine weight changed")
    word_choices = tuple(
        tuple(colour for colour in range(3)
              if target_degree[3 * site + colour])
        for site in range(8)
    )
    compatible_words = tuple(product(*word_choices))
    require(compatible_words == (PURE_WORD, MIXED_WORD),
            "nearest binary fine degree gained another output row")

    # Complete monomial multiplier census in this fine degree:
    # - on r0, every term of Hw (90 direct-free perfect matchings);
    # - on rw, every term of H0 plus the pure homogenizer u (91).
    columns = []
    labels = []
    for multiplier in sorted(hw, key=repr):
        columns.append(polynomial_multiply(Counter({multiplier: Q(1)}), f0))
        labels.append(("r0", multiplier))
    for multiplier in sorted(h0, key=repr):
        columns.append(polynomial_multiply(Counter({multiplier: Q(1)}), fw))
        labels.append(("rw", multiplier))
    columns.append(polynomial_multiply(u, fw))
    labels.append(("rw", (1, ())))
    require(len(columns) == len(labels) == 181,
            "complete first higher component changed size")

    rank, row_count = sparse_rank(columns)
    require(rank == 180 and row_count == 7200,
            ("first higher component rank changed", rank, row_count))

    # H_w*r0 - H_0*r_w + u*r_w.  This is exactly
    # H_w*(H_0-u) - (H_0-u)*H_w = 0.
    kernel = [Q(1)] * 90 + [Q(-1)] * 90 + [Q(1)]
    boundary = Counter()
    for coefficient, column in zip(kernel, columns, strict=True):
        for term, value in column.items():
            boundary[term] += coefficient * value
    require(not any(boundary.values()), "Koszul vector is not a source syzygy")
    require(len(columns) - rank == 1,
            "Koszul vector does not span the complete kernel")

    # Fine homogeneity of both terms in the free source module.
    require(degree_add(word_degree(MIXED_WORD), word_degree(PURE_WORD))
            == target_degree,
            "H_w*r0 lost fine degree")
    require(degree_add(word_degree(PURE_WORD), word_degree(MIXED_WORD))
            == target_degree,
            "(H0-u)*rw lost fine degree")

    # Anchor-relevant minimality: below multiplier degree four, a coefficient
    # cannot contain u.  In a syzygy, the coefficient of u in F0 then forces
    # the pure-row coefficient to vanish.  At degree four the displayed u*rw
    # term first permits cancellation, and the Koszul vector realizes it.
    multiplier_edge_degree = 4
    require(all(len(term[1]) == multiplier_edge_degree and term[0] == 0
                for term in hw), "H_w multiplier degree changed")
    require(all(len(term[1]) == multiplier_edge_degree and term[0] == 0
                for term in h0), "H_0 multiplier degree changed")

    # The pure-row coefficient is H_w.  A pure generator coefficient A has
    # typed readout A*(-1,0,1,0); mixed generators have no anchor or target.
    # Hence the new syzygy is still detected by the old conormal separator.
    typed_readout = ("-H_w", 0, "H_w", 0)

    # With two identical chart copies, the boundary rank remains 180.  Its
    # 182-dimensional kernel is generated by 181 pairwise chart differences
    # plus one Koszul vector.  Differences have zero typed readout; target
    # zero kills the Koszul coefficient and therefore its anchor as well.
    two_chart_columns = 2 * len(columns)
    two_chart_kernel = two_chart_columns - rank
    require(two_chart_kernel == 182,
            "two-chart higher-component kernel changed")

    return {
        "words": {
            "pure": "".join(map(str, PURE_WORD)),
            "hamming_one": "".join(map(str, MIXED_WORD)),
        },
        "fine_degree": {
            "weight": sum(target_degree),
            "nonzero_slots": [
                [index // 3, index % 3, value]
                for index, value in enumerate(target_degree) if value
            ],
            "compatible_rows": 2,
        },
        "complete_component": {
            "r0_edge_multipliers": 90,
            "rw_edge_multipliers": 90,
            "rw_u_multiplier": 1,
            "columns": len(columns),
            "polynomial_rows": row_count,
            "rank": rank,
            "kernel_dimension": len(columns) - rank,
        },
        "kernel_generator": {
            "formula": "H_w*r0-(H_0-u)*r_w",
            "support": len(kernel),
            "boundary": 0,
            "multiplier_edge_degree": multiplier_edge_degree,
            "typed_readout_ainc_w_tgt_ores": list(typed_readout),
        },
        "minimality": {
            "anchor_relevant_syzygy_below_multiplier_degree_4": False,
            "reason": "without a u multiplier, the u coefficient forces the pure-row coefficient to zero",
            "first_new_multiplier_degree": 4,
            "first_new_fine_weight": 16,
        },
        "schreyer_promotion": {
            "tate_critical_pairs_complete": False,
            "reason": "the new weight-16 u-Koszul class is below and outside the edge-only weight-18 Tate top",
            "all_degree_anchor_zero_from_tate_pairs": False,
            "all_degree_polynomial_target_zero_implies_anchor_zero": True,
            "all_degree_reason": "pure-row coefficient is simultaneously minus anchor incidence and physical target",
        },
        "two_chart": {
            "columns": two_chart_columns,
            "rank": rank,
            "kernel_dimension": two_chart_kernel,
            "generators": "181 chart differences plus one Koszul class",
            "target_zero_kernel_anchor": 0,
        },
        "proof_impact": {
            "primitive_anchor_constructed": False,
            "new_higher_relative_generator_still_required": True,
        },
    }


def main() -> None:
    pin_dependencies()
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "rootless_complete_first_degree",
    )
    ledger = audit(base)
    digest = sha256(json.dumps(ledger, sort_keys=True,
                               separators=(",", ":")).encode()).hexdigest()
    require(digest == EXPECTED_LEDGER_SHA256, ("ledger digest drift", digest))
    print("h=3 rootless C5 first higher anchor S-pair: exact counterguard")
    print("  complete component             : 181 columns / rank 180")
    print("  first new anchor S-pair        : multiplier degree 4, fine weight 16")
    print("  typed readout                  : (-H_w,0,H_w,0)")
    print("  Tate critical pairs complete   : NO")
    print(f"  ledger sha256                  : {digest}")


if __name__ == "__main__":
    main()
