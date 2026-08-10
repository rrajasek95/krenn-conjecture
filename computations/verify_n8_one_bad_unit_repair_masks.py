#!/usr/bin/env python3
"""Repair masks and successor units for the eight orbit-1 closures.

For the selected ordinary one-class identity on each minimum orbit-1
closure, reconstruct its exact binomial source footprint.  A repair mask is
an inclusion-minimal set of absent cells which activates a new matching in
one of those source fibres.  The complete census is 12 singleton and 111
double masks.

Every double mask creates fresh singleton debt (propagation, not a proved
descent).  The singleton masks give twelve closed 38-cell successors.  They
have no initial odd character and the canonical first successor has no
literal factorized shared-zero fan, but all twelve are killed by new
one-class units.  Those units have two universal coefficient palettes:
eight trinomials reduce as -M+M+M=M, and four six-term rows cancel one
class and leave +/-2 times the other.  Their own complete repair census is
16 singleton plus 173 double masks.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEPENDENCY = "computations/verify_n8_one_bad_first_closed_exchange_census.py"
DEPENDENCY_SHA256 = (
    "4e61eaa7e669fe6cf78ffbb2ec6746d001854d5bdc14fed1d0b309e0acd189bf"
)
EXPECTED_LEDGER_SHA256 = "3946d0a9a46b2d330913dcd43b1e1bd5c10b358910e15a8884cb4b11e8b9a9d1"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


path = ROOT / DEPENDENCY
require(sha256(path.read_bytes()).hexdigest() == DEPENDENCY_SHA256,
        "the pinned first-closure census changed")
spec = spec_from_file_location("one_bad_first_closed", path)
C = module_from_spec(spec)
spec.loader.exec_module(C)


def reduce_trace(monomial, basis):
    original = Counter(monomial)
    exponent = Counter(monomial)
    coefficient = 1
    used_rows = Counter()
    rebuilt = {}
    character_exponent = Fraction(0)
    for pivot, (basis_row, representation) in sorted(basis.items()):
        multiplier = exponent.get(pivot, 0)
        if not multiplier:
            continue
        row_character = sum(representation.values(), Fraction(0))
        require(row_character.denominator == 1,
                "a repair trace acquired a fractional character")
        character_exponent += multiplier * row_character
        if multiplier * row_character.numerator % 2:
            coefficient = -coefficient
        C.axpy(rebuilt, Fraction(multiplier), basis_row)
        for position, value in representation.items():
            used_rows[position] += multiplier * value
            if not used_rows[position]:
                used_rows.pop(position, None)
        for cell, value in basis_row.items():
            exponent[cell] -= multiplier * int(value)
            if not exponent[cell]:
                exponent.pop(cell, None)

    direct = Counter(original)
    direct.subtract(exponent)
    direct = {cell: Fraction(value) for cell, value in direct.items() if value}
    require(direct == rebuilt,
            "a repair-unit monomial lost exponent provenance")
    require(coefficient == (-1 if character_exponent.numerator % 2 else 1),
            "a repair-unit monomial lost sign provenance")
    return tuple(sorted(exponent.items())), coefficient, dict(used_rows)


def identity_data(support):
    records = []
    for row, word, monomials in C.closure_fibres(1):
        live = tuple(monomial for monomial in monomials
                     if set(monomial) <= support)
        if live:
            records.append({
                "row": row,
                "word": word,
                "live": live,
                "full": monomials,
            })
    binomial_records = [index for index, record in enumerate(records)
                        if len(record["live"]) == 2]
    rows = [C.exponent_difference(
        records[index]["live"][0], records[index]["live"][1]
    ) for index in binomial_records]
    basis, dependencies = C.laurent_basis(rows)
    require(not any(C.character(dependency) == -1
                    for dependency in dependencies),
            "an orbit-1 repair identity acquired an initial odd circuit")

    unit_records = []
    for index, record in enumerate(records):
        reduced = C.reduce_polynomial(record["live"], basis)
        if len(reduced) == 1:
            unit_records.append(index)
    require(unit_records, "a repair state lost every one-class identity")
    target = unit_records[0]

    traces = [reduce_trace(monomial, basis)
              for monomial in records[target]["live"]]
    normal_forms = Counter()
    used_positions = set()
    for normal_form, coefficient, used in traces:
        normal_forms[normal_form] += coefficient
        used_positions.update(used)
    normal_forms = {normal_form: coefficient
                    for normal_form, coefficient in normal_forms.items()
                    if coefficient}
    require(len(normal_forms) == 1,
            "the selected repair identity stopped being one-class")
    source_records = {target} | {
        binomial_records[position] for position in used_positions
    }

    candidates = []
    for source in source_records:
        for monomial in records[source]["full"]:
            missing = frozenset(set(monomial) - support)
            if missing:
                candidates.append((missing, source, monomial))
    minimal = []
    for missing, source, monomial in candidates:
        if not any(other < missing for other, _other_source, _other_monomial
                   in candidates):
            minimal.append((missing, source, monomial))
    masks = {}
    for missing, source, monomial in minimal:
        masks.setdefault(missing, []).append((source, monomial))

    surviving_coefficient = next(iter(normal_forms.values()))
    class_sums = Counter()
    for normal_form, coefficient, _used in traces:
        class_sums[normal_form] += coefficient
    return {
        "records": records,
        "binomial_records": binomial_records,
        "basis": basis,
        "target": target,
        "target_terms": len(records[target]["live"]),
        "target_label": [records[target]["row"], list(records[target]["word"])],
        "source_records": source_records,
        "traces": traces,
        "trace_classes": len(class_sums),
        "trace_class_sums": sorted(class_sums.values()),
        "surviving_coefficient": surviving_coefficient,
        "masks": masks,
    }


def singleton_defects(support):
    defects = []
    for row, word, monomials in C.closure_fibres(1):
        live = tuple(monomial for monomial in monomials
                     if set(monomial) <= support)
        if len(live) == 1:
            defects.append((row, word, live[0]))
    return defects


def fixed_right_colour(site):
    return 0 if site in (2, 4) else 1


def carrier_routes(pair, word, complement=None):
    first, second = pair
    routes = []
    for left_target, right_target in ((first, second), (second, first)):
        route = [
            C.canonical_cell((0, left_target),
                             (word[0], word[left_target])),
            C.canonical_cell((1, right_target),
                             (word[1], word[right_target])),
        ]
        if complement is not None:
            route.append(complement)
        routes.append(tuple(sorted(route)))
    return frozenset(routes)


def literal_factorized_zero_pairs(support):
    """Find raw two-route zero tensors before any Laurent substitution."""
    right = {2, 3, 4, 5}
    exact = []

    # Top equations factored by one complementary right-right cell.
    for pair in itertools.combinations(sorted(right), 2):
        complement_edge = tuple(sorted(right - set(pair)))
        complement = C.canonical_cell(
            complement_edge,
            tuple(fixed_right_colour(site) for site in complement_edge),
        )
        if complement not in support:
            continue
        all_entries = True
        for left_colour, right_colour in itertools.product((0, 1), repeat=2):
            word = [None] * 6
            word[0], word[1] = left_colour, right_colour
            for site in right:
                word[site] = fixed_right_colour(site)
            word = tuple(word)
            live = frozenset(
                C.matching_cells(matching, word)
                for matching in C.BASE.perfect_matchings(C.SITES)
                if set(C.matching_cells(matching, word)) <= support
            )
            if live != carrier_routes(pair, word, complement):
                all_entries = False
        if all_entries:
            exact.append(("top", pair))

    # The two off-diagonal response tensors.
    packet = C.BASE.SHARP_REPRESENTATIVES[1]
    b_holes, c_holes = packet[2], packet[4]
    response_rows = (
        (b_holes[0], 0, c_holes[1], 1),
        (c_holes[0], 1, b_holes[1], 0),
    )
    for left_hole, left_colour, right_hole, right_colour in response_rows:
        residual = tuple(site for site in C.SITES
                         if site not in (left_hole, right_hole))
        pair = tuple(sorted(set(residual) - {0, 1}))
        all_entries = True
        for first_colour, second_colour in itertools.product((0, 1), repeat=2):
            word = [None] * 6
            word[0], word[1] = first_colour, second_colour
            word[left_hole], word[right_hole] = left_colour, right_colour
            for site in pair:
                word[site] = fixed_right_colour(site)
            word = tuple(word)
            live = frozenset(
                C.matching_cells(matching, word)
                for matching in C.BASE.perfect_matchings(residual)
                if set(C.matching_cells(matching, word)) <= support
            )
            if live != carrier_routes(pair, word):
                all_entries = False
        if all_entries:
            exact.append(("response", pair))
    return tuple(exact)


def mask_trace(masks):
    return [
        [sorted(C.cell_name(cell) for cell in mask),
         sorted(source for source, _monomial in sources)]
        for mask, sources in sorted(
            masks.items(),
            key=lambda item: (
                len(item[0]), sorted(C.cell_name(cell) for cell in item[0])
            ),
        )
    ]


def main():
    base_identities = []
    base_masks = []
    singleton_successors = []
    double_propagations = []

    for support_index, support in enumerate(C.sorted_supports(1)):
        identity = identity_data(support)
        base_identities.append({
            "support": support_index,
            "source_records": len(identity["source_records"]),
            "target_label": identity["target_label"],
            "target_terms": identity["target_terms"],
            "masks": len(identity["masks"]),
            "mask_size_histogram": dict(sorted(Counter(
                len(mask) for mask in identity["masks"]
            ).items())),
            "mask_trace_sha256": sha256(json.dumps(
                mask_trace(identity["masks"]), separators=(",", ":")
            ).encode()).hexdigest(),
        })
        for mask in identity["masks"]:
            base_masks.append((support_index, support, mask))
            enlarged = support | mask
            defects = singleton_defects(enlarged)
            if len(mask) == 1:
                require(not defects,
                        "a singleton repair unexpectedly created debt")
                cell = next(iter(mask))
                require(C.cell_name(cell) in {"25:01", "34:10"},
                        "a new singleton repair cell appeared")
                successor = identity_data(enlarged)
                require(not any(C.character(dependency) == -1
                                for dependency in C.laurent_basis([
                                    C.exponent_difference(
                                        successor["records"][index]["live"][0],
                                        successor["records"][index]["live"][1],
                                    )
                                    for index in successor["binomial_records"]
                                ])[1]),
                        "a singleton successor acquired an initial odd circuit")
                singleton_successors.append({
                    "support": support_index,
                    "repair": C.cell_name(cell),
                    "support_cells": len(enlarged),
                    "target_label": successor["target_label"],
                    "target_terms": successor["target_terms"],
                    "trace_classes": successor["trace_classes"],
                    "trace_class_sums": successor["trace_class_sums"],
                    "surviving_coefficient":
                        successor["surviving_coefficient"],
                    "source_records": len(successor["source_records"]),
                    "masks": len(successor["masks"]),
                    "mask_size_histogram": dict(sorted(Counter(
                        len(value) for value in successor["masks"]
                    ).items())),
                    "mask_trace_sha256": sha256(json.dumps(
                        mask_trace(successor["masks"]), separators=(",", ":")
                    ).encode()).hexdigest(),
                })
            else:
                require(len(mask) == 2,
                        "a first repair mask larger than two appeared")
                require(defects and all(set(monomial) & set(mask)
                                        for _row, _word, monomial in defects),
                        "a double repair failed to export fresh singleton debt")
                double_propagations.append({
                    "support": support_index,
                    "repair": sorted(C.cell_name(cell) for cell in mask),
                    "fresh_singletons": len(defects),
                })

    require(Counter(len(mask) for _index, _support, mask in base_masks)
            == Counter({2: 111, 1: 12}),
            "the complete first repair-mask census changed")
    require(len(singleton_successors) == 12
            and len(double_propagations) == 111,
            "the repair split changed")

    palette = Counter(
        (record["target_terms"], record["trace_classes"],
         tuple(record["trace_class_sums"]),
         record["surviving_coefficient"])
        for record in singleton_successors
    )
    require(palette == Counter({
        (3, 1, (1,), 1): 8,
        (6, 2, (-2, 0), -2): 2,
        (6, 2, (0, 2), 2): 2,
    }), f"the successor unit palettes changed: {palette}")
    successor_mask_histogram = Counter()
    for record in singleton_successors:
        successor_mask_histogram.update({
            int(size): count
            for size, count in record["mask_size_histogram"].items()
        })
    require(successor_mask_histogram == Counter({2: 173, 1: 16}),
            "the successor-family repair census changed")

    first_support = C.sorted_supports(1)[0]
    first_repair = C.parse_support("25:01")
    first_escape = first_support | first_repair
    require(not singleton_defects(first_escape),
            "the first singleton escape acquired a support descent")
    require(not literal_factorized_zero_pairs(first_escape),
            "the first singleton escape acquired a literal shared-zero fan")
    first_coefficient = C.coefficient_audit(1, first_escape)
    require(first_coefficient["type"] == "one_class_laurent_unit",
            "the first singleton escape lost its successor unit")

    ledger = {
        "dependency": {"path": DEPENDENCY, "sha256": DEPENDENCY_SHA256},
        "base_unit_identities": base_identities,
        "complete_base_mask_histogram": {"1": 12, "2": 111},
        "double_repairs": {
            "count": len(double_propagations),
            "fresh_singleton_histogram": dict(sorted(Counter(
                record["fresh_singletons"] for record in double_propagations
            ).items())),
            "status": (
                "propagation required; no anchor-preserving descent is "
                "claimed without following later mates"
            ),
        },
        "singleton_successor_units": singleton_successors,
        "successor_palette": [
            [list(key), count] for key, count in sorted(palette.items())
        ],
        "complete_successor_mask_histogram": {"1": 16, "2": 173},
        "first_checked_trichotomy_escape": {
            "base_support": 0,
            "repair": "25:01",
            "support_cells": len(first_escape),
            "singleton_defects": 0,
            "literal_factorized_zero_pairs": [],
            "initial_odd_character": False,
            "replacement_obstruction": first_coefficient,
        },
        "verdict": (
            "the proposed fan/odd/descent trichotomy is not exhaustive at "
            "the literal first-repair level: the first singleton repair "
            "escapes all three checked mechanisms but is killed by a new "
            "one-class unit; the twelve successor units form two exact "
            "translated coefficient palettes"
        ),
        "scope": (
            "repair masks of the eight frozen ordinary one-class identities "
            "and of their twelve singleton successor identities; double-mask "
            "singleton debt is propagation only, and hidden nonliteral tensor "
            "quotients or further mate closures are not excluded"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"one-bad repair-mask ledger changed: {digest}")

    print("N=8 one-bad one-class repair masks: PASS")
    print("base masks: 12 singleton + 111 double")
    print("singleton successors: 8 trinomial + 4 six-term units")
    print("successor masks: 16 singleton + 173 double")
    print("first literal trichotomy escape: support0 + x25_01")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
