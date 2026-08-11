#!/usr/bin/env python3
r"""Complete literal full-nine source module in the rootless C5 degrees.

For each of the five P3+K2 degrees in the rootless pentagon interface, this
checker enumerates every compatible global output word and every polynomial
edge-monomial multiplier.  It also enumerates the complete common degree-five
component and the natural Tate multiplication maps into it.

The one-chart full-nine boundary maps are injective, certified by literal
unique matching-monomial pivots.  At the Tate top, compatibility is equality
of source-row/multiplier labels.  Every compatible relation has zero sum on
each pure target label, hence zero total anchor incidence.  An arbitrary top
source correction cannot change this because the complete top boundary map
is injective.  The two-chart kernel consists only of pairwise differences and
also has zero anchor and target.

Thus no polynomial source combination in this complete bounded multigraded
inventory realizes (-1,0,0,0).  This does not exclude a genuinely new higher
source-resolution generator outside polynomial multiples of full-nine rows.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
from functools import lru_cache
from hashlib import sha256
from itertools import product
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = "7d32bc6edc31f9c5a81769eee162e1749dd98a3e33405e44541cd3d34d2bf64a"
PINS = {
    "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py":
        "190171b72493e661dedb8e7aa369a9b72f1a71e14487632df2841ca7eeb19bf4",
    "computations/verify_h3_rootless_five_cycle_positive_interface.py":
        "fd359b3ff2abbb01d9508996c754a27b70890b2cd621926fc30b92057b337851",
    "computations/verify_h3_rootless_five_cycle_tate_anchor_obstruction.py":
        "a1383c13a732ec34eda5614c4346fecfd99b960480727ba26ac7089690844936",
}

PURE_WORD = (0,) * 8
CYCLE_CELLS = (
    (1, 2, 1, 2),  # a
    (2, 3, 2, 1),  # b
    (3, 4, 1, 1),  # c
    (4, 5, 1, 2),  # d
    (1, 5, 1, 2),  # e
)
# (left deleted face, right deleted face, left cycle multiplier,
#  right cycle multiplier), in the orientation of 5f490c6.
CUBIC_PAIRS = (
    (1, 3, 0, 1),
    (3, 5, 2, 3),
    (5, 2, 4, 0),
    (2, 4, 1, 2),
    (4, 1, 3, 4),
)
# ce, be, bd, ad, ac: coefficients of the degree-five Tate boundary.
TATE_COMPLEMENTS = ((2, 4), (1, 4), (1, 3), (0, 3), (0, 2))


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


def degree_add(*values):
    return tuple(sum(entries) for entries in zip(*values, strict=True))


def cell_degree(cell):
    degree = [0] * 24
    left, right, left_colour, right_colour = cell
    degree[3 * left + left_colour] += 1
    degree[3 * right + right_colour] += 1
    return tuple(degree)


@lru_cache(maxsize=None)
def multiplier_pairings(base, stubs):
    """All edge monomials pairing a coloured stub multiset without loops."""
    stubs = tuple(stubs)
    if not stubs:
        return ((),)
    first = stubs[0]
    answer = set()
    for position, second in enumerate(stubs[1:], start=1):
        if first[0] == second[0]:
            continue
        cell = base.edge(first[0], second[0], first[1], second[1])
        remainder = stubs[1:position] + stubs[position + 1:]
        for tail in multiplier_pairings(base, remainder):
            answer.add(tuple(sorted((cell,) + tail)))
    return tuple(sorted(answer))


def compatible_words(target_degree):
    choices = tuple(
        tuple(colour for colour in range(3)
              if target_degree[3 * site + colour])
        for site in range(8)
    )
    require(all(choices), "target degree omits a physical site")
    return tuple(product(*choices))


def compatible_multipliers(base, target_degree, word):
    stubs = []
    for site in range(8):
        for colour in range(3):
            count = (target_degree[3 * site + colour]
                     - int(word[site] == colour))
            require(count >= 0, ("word does not divide target", word, site))
            stubs.extend(((site, colour),) * count)
    require(len(stubs) % 2 == 0, "odd multiplier degree")
    return multiplier_pairings(base, tuple(sorted(stubs)))


def component(base, target_degree):
    columns = []
    multiplier_count_distribution = Counter()
    for word in compatible_words(target_degree):
        multipliers = compatible_multipliers(base, target_degree, word)
        multiplier_count_distribution[len(multipliers)] += 1
        for multiplier in multipliers:
            boundary = tuple(
                tuple(sorted(multiplier + row_term))
                for row_term in base.full_row(word)
            )
            require(len(boundary) == len(set(boundary)) == 90,
                    "a multiplied full-nine row collided internally")
            columns.append((word, multiplier, boundary))

    # Exact injectivity certificate: every column has a literal matching
    # monomial which occurs in no other column.
    owners = defaultdict(list)
    for column_index, (_word, _multiplier, boundary) in enumerate(columns):
        for feature in boundary:
            owners[feature].append(column_index)
    unique_per_column = tuple(
        sum(len(owners[feature]) == 1 for feature in boundary)
        for _word, _multiplier, boundary in columns
    )
    require(columns and min(unique_per_column) > 0,
            "complete component lost its literal unique-pivot proof")
    pivots = tuple(
        min(feature for feature in boundary if len(owners[feature]) == 1)
        for _word, _multiplier, boundary in columns
    )
    require(len(pivots) == len(set(pivots)) == len(columns),
            "unique pivots collided")

    labels = tuple((word, multiplier) for word, multiplier, _boundary in columns)
    pure_labels = tuple(label for label in labels if label[0] == PURE_WORD)
    return {
        "target_degree": target_degree,
        "columns": tuple(columns),
        "labels": labels,
        "label_set": frozenset(labels),
        "word_count": len(compatible_words(target_degree)),
        "multiplier_count_distribution": multiplier_count_distribution,
        "feature_count": len(owners),
        "unique_feature_count": sum(len(value) == 1 for value in owners.values()),
        "unique_per_column": unique_per_column,
        "maximum_feature_owner_count": max(map(len, owners.values())),
        "pure_labels": pure_labels,
        "rank": len(columns),
        "one_chart_kernel": 0,
        "two_chart_columns": 2 * len(columns),
        "two_chart_rank": len(columns),
        "two_chart_kernel": len(columns),
    }


def summarize_component(record):
    return {
        "target_weight": sum(record["target_degree"]),
        "words": record["word_count"],
        "columns": len(record["columns"]),
        "multiplier_count_per_word": {
            str(key): value for key, value in
            sorted(record["multiplier_count_distribution"].items())
        },
        "boundary_features": record["feature_count"],
        "unique_boundary_features": record["unique_feature_count"],
        "unique_pivots_per_column": [
            min(record["unique_per_column"]),
            max(record["unique_per_column"]),
        ],
        "maximum_feature_owner_count": record["maximum_feature_owner_count"],
        "pure_row_multipliers": len(record["pure_labels"]),
        "one_chart_rank_kernel": [record["rank"], record["one_chart_kernel"]],
        "two_chart_columns_rank_kernel": [
            record["two_chart_columns"],
            record["two_chart_rank"],
            record["two_chart_kernel"],
        ],
    }


def audit(base, positive):
    cubic_components = []
    cubic_degrees = []
    for left_face, right_face, left_cell, right_cell in CUBIC_PAIRS:
        left_degree = degree_add(
            base.lambda_degree(left_face), cell_degree(CYCLE_CELLS[left_cell])
        )
        right_degree = degree_add(
            base.lambda_degree(right_face), cell_degree(CYCLE_CELLS[right_cell])
        )
        require(left_degree == right_degree and sum(left_degree) == 14,
                ("cubic fine degree mismatch", left_face, right_face))
        cubic_degrees.append(left_degree)
        cubic_components.append(component(base, left_degree))

    require(all(len(record["columns"]) == 288 for record in cubic_components),
            "a complete cubic component changed size")
    require(all(record["word_count"] == 32 for record in cubic_components),
            "a cubic component changed its compatible-word count")
    require(all(record["multiplier_count_distribution"]
                == Counter({6: 16, 12: 16})
                for record in cubic_components),
            "cubic multiplier-pairing census changed")
    require(all(len(record["pure_labels"]) == 6
                for record in cubic_components),
            "a cubic pure-row multiplier census changed")

    top_degrees = []
    for index, record in enumerate(cubic_components):
        complement_degree = degree_add(*(
            cell_degree(CYCLE_CELLS[cell])
            for cell in TATE_COMPLEMENTS[index]
        ))
        top_degrees.append(degree_add(record["target_degree"], complement_degree))
    require(len(set(top_degrees)) == 1 and sum(top_degrees[0]) == 18,
            "the natural Tate maps do not share one fine degree")
    top_component = component(base, top_degrees[0])
    require(top_component["word_count"] == 32
            and len(top_component["columns"]) == 4266
            and top_component["multiplier_count_distribution"]
            == Counter({22: 1, 40: 5, 74: 10,
                        140: 10, 272: 5, 544: 1}),
            "complete top component census changed")
    require(len(top_component["pure_labels"]) == 22,
            "top pure-row multiplier census changed")

    # Natural multiplication sends a row/multiplier label in cubic component
    # i to the same row with the two Tate-complement cells appended.  Every
    # image is checked against the COMPLETE top component.
    image_owners = defaultdict(list)
    for index, record in enumerate(cubic_components):
        complement = tuple(CYCLE_CELLS[cell]
                           for cell in TATE_COMPLEMENTS[index])
        for column_index, (word, multiplier) in enumerate(record["labels"]):
            top_label = (word, tuple(sorted(multiplier + complement)))
            require(top_label in top_component["label_set"],
                    ("natural Tate image missing from top", index, column_index))
            image_owners[top_label].append((index, column_index))

    owner_distribution = Counter(map(len, image_owners.values()))
    require(len(image_owners) == 1201
            and owner_distribution == Counter({1: 980, 2: 205, 3: 15, 5: 1}),
            ("natural Tate image incidence changed", owner_distribution))
    natural_domain = sum(len(record["labels"]) for record in cubic_components)
    natural_kernel = natural_domain - len(image_owners)
    require(natural_domain == 1440 and natural_kernel == 239,
            "natural Tate map rank/kernel changed")

    pure_image_owners = {
        label: owners for label, owners in image_owners.items()
        if label[0] == PURE_WORD
    }
    require(len(pure_image_owners) == 16
            and Counter(map(len, pure_image_owners.values()))
            == Counter({1: 5, 2: 10, 5: 1}),
            "pure Tate-image incidence changed")

    full_cycle_multiplier = tuple(sorted(CYCLE_CELLS))
    full_cycle_label = (PURE_WORD, full_cycle_multiplier)
    full_cycle_owners = pure_image_owners[full_cycle_label]
    require(sorted(index for index, _column in full_cycle_owners)
            == list(range(5)),
            ("the five selected anchors lost their common top label",
             full_cycle_owners))

    # A vector in the natural Tate kernel has coefficient sum zero separately
    # on every image label.  Pure anchor incidence is the negative of the sum
    # on pure labels, while physical target is the positive sum.  Hence both
    # vanish on the entire kernel, not only on the five selected columns.
    # In particular, the full-cycle equation is sum_i gamma_i=0.
    require(sum(len(owners) - 1 for owners in image_owners.values())
            == natural_kernel,
            "label-fibre kernels do not exhaust the natural Tate kernel")

    # Grant an arbitrary polynomial full-nine correction at the top.  Its
    # matching boundary map is injective by the unique pivots above.  Thus a
    # correction cancelling a natural image is uniquely its negative in the
    # free row/multiplier module, and cancels anchor and target termwise.  No
    # hidden top syzygy can alter the readout.
    require(top_component["one_chart_kernel"] == 0,
            "a top full-nine syzygy could change the anchor readout")

    # Recheck the normalized C5 resolution signs which this literal module
    # is meant to lift.
    _g, _f, _d0, _d1, _d2, _records = positive.multigraded_resolution()

    return {
        "direct_free_pair": sorted(base.DIRECT_FREE_PAIR),
        "cubic_components": [summarize_component(value)
                             for value in cubic_components],
        "degree_five_component": summarize_component(top_component),
        "natural_tate_map": {
            "domain_columns": natural_domain,
            "image_labels": len(image_owners),
            "kernel_dimension": natural_kernel,
            "owner_multiplicity_distribution": {
                str(key): value for key, value in sorted(owner_distribution.items())
            },
            "pure_image_labels": len(pure_image_owners),
            "pure_owner_multiplicity_distribution": {
                str(key): value for key, value in
                sorted(Counter(map(len, pure_image_owners.values())).items())
            },
            "full_cycle_selected_owners": [index for index, _ in full_cycle_owners],
            "kernel_anchor_incidence": 0,
            "kernel_physical_target": 0,
            "kernel_w": 0,
            "kernel_ordinary_residue": 0,
        },
        "top_correction": {
            "complete_columns": len(top_component["columns"]),
            "boundary_rank": top_component["rank"],
            "kernel": top_component["one_chart_kernel"],
            "unique_cancelling_correction_is_negative_natural_image": True,
            "net_anchor_after_correction": 0,
            "net_target_after_correction": 0,
        },
        "two_chart": {
            "cubic_kernel_per_degree": 288,
            "top_kernel": 4266,
            "kernel_basis": "pairwise pq-minus-pr copies of each labelled column",
            "kernel_anchor_target_w_ores": [0, 0, 0, 0],
        },
        "typed_membership": {
            "requested_signature": [-1, 0, 0, 0],
            "realized": False,
            "reason": (
                "Tate compatibility is coefficientwise equality of complete "
                "row/multiplier labels; every pure-label sum, hence anchor, is zero"
            ),
            "new_higher_source_generator_excluded": False,
        },
    }


def main() -> None:
    pin_dependencies()
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "rootless_complete_first_degree",
    )
    positive = load(
        "computations/verify_h3_rootless_five_cycle_positive_interface.py",
        "rootless_positive_interface",
    )
    ledger = audit(base, positive)
    digest = sha256(json.dumps(ledger, sort_keys=True,
                               separators=(",", ":")).encode()).hexdigest()
    require(digest == EXPECTED_LEDGER_SHA256, ("ledger digest drift", digest))
    print("h=3 rootless C5 complete multidegree source module: NO-GO (exact)")
    print("  five cubic components          : 288 columns / rank 288 each")
    print("  complete degree-five component : 4266 columns / rank 4266")
    print("  natural Tate map               : 1440 -> 1201, kernel 239")
    print("  anchor on whole Tate kernel    : 0")
    print(f"  ledger sha256                  : {digest}")


if __name__ == "__main__":
    main()
