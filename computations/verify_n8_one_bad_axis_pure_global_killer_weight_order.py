#!/usr/bin/env python3
"""One exact local weight order for every pair/triple killer row.

The 44 pair and 174 primitive-triple killer occurrences collapse to 54
literal source rows with 54 distinct unit-linear carrier initials.  This
checker expands those rows with all 90 mixed q cells present and verifies a
single positive integer valuation which makes every designated carrier term
strictly lighter than every contaminant.  The 36 unselected carrier rays are
then strictly separated by one exact quotient cocharacter, so they support
no positive circuit of any degree.

The statement is an associated-graded/local-standard-basis statement on the
localized pure chart.  It does not assert global ideal membership away from
that chart.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
import importlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_n8_one_bad_axis_pure_all_opposing_pair_elimination.py":
        "2c7ab786a4b0efeb0a4a02e85268d0decef86de0986c1fb0ae567f013676d97c",
    "computations/verify_n8_one_bad_axis_pure_all_hilbert_triple_elimination.py":
        "e6e23172e691cbdc1693101256153eb906151b9b35f19b162f61a9c0c2edb4a7",
    "computations/verify_n8_one_bad_axis_pure_chart_torus_accessibility.py":
        "327dbf6ac8f2d617f78433f25859d8760bec1253d557158425ec8649babd28e9",
    "computations/verify_n8_one_bad_axis_pure_mixed_weight_hilbert_circuits.py":
        "3b1737f02c8746ce8964c3b1b53a713961de7f8ab00f0dd8141e5e7b8647d1c2",
    "computations/verify_n8_one_bad_endpoint_minor_unary_top_completion.py":
        "f0d4c5382cce1ccb8bed5a5ac0afa8cf8662c905bd0c675a56b51f2be7d0b574",
    "computations/verify_n8_one_bad_multisite_permanent_null_defect.py":
        "94946c00fc25cd08eead06148deae85cc2ed80e0cce65c68bc37ad50384f6f53",
}
EXPECTED_LEDGER_SHA256 = "2fe9ca2777a60a55727dba028d9b13611c17b492a5f79c6ecd83f55a9d0c26e1"
SITES = tuple(range(6))
COLOURS = tuple(range(3))

# Every mixed carrier not displayed has weight one.
CARRIER_WEIGHT_OVERRIDES = {
    (0, 1, 1, 0): 3,
    (0, 1, 1, 2): 2,
    (0, 2, 1, 0): 3,
    (0, 3, 1, 0): 2,
    (0, 3, 2, 1): 2,
    (0, 4, 1, 0): 2,
    (0, 4, 1, 2): 3,
    (0, 4, 2, 0): 2,
    (0, 5, 2, 0): 2,
    (1, 2, 2, 1): 2,
    (1, 4, 0, 1): 2,
    (1, 4, 0, 2): 2,
    (1, 4, 2, 0): 2,
    (1, 5, 0, 1): 2,
    (1, 5, 0, 2): 2,
    (1, 5, 2, 0): 2,
    (2, 4, 0, 1): 2,
    (2, 4, 0, 2): 2,
    (2, 4, 1, 0): 2,
    (2, 5, 0, 1): 2,
    (2, 5, 0, 2): 2,
    (2, 5, 1, 0): 2,
    (3, 4, 1, 0): 2,
    (3, 5, 1, 0): 2,
    (4, 5, 1, 2): 2,
    (4, 5, 2, 1): 2,
}

# These are precisely the pure-chart symbols in the expanded rows which are
# not among the localized unit coefficients.  Giving them weight one makes
# the order a genuine positive local valuation on every nonunit source
# coordinate, rather than silently treating p5 or an arbitrary pure z as a
# coefficient.
NONUNIT_PARAMETERS = frozenset(
    {f"z{left}{right}" for left, right in itertools.combinations(SITES, 2)}
    - {"z03", "z12", "z45"}
    | {"p5"}
)
REMAINING_COCHARACTER = (
    0, 0, 0, 0, 0, 0, 0, -1, -1, 0, -1, -1, 0
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency changed: {relative}: {actual}")


def variable(name):
    return Counter({(name,): Fraction(1)})


def carrier_name(cell):
    return "m" + "".join(map(str, cell))


def mixed_cells():
    return tuple(
        (left, right, left_colour, right_colour)
        for left, right in itertools.combinations(SITES, 2)
        for left_colour, right_colour in itertools.product(COLOURS, repeat=2)
        if left_colour != right_colour
    )


def full_q(module, cells):
    result = {
        module.source_cell(2, 4, 1, 1): variable("A"),
        module.source_cell(3, 5, 1, 1): variable("B"),
        module.source_cell(0, 5, 2, 2): variable("C"),
        module.source_cell(1, 4, 2, 2): variable("D"),
    }
    for left, right in itertools.combinations(SITES, 2):
        result[module.source_cell(left, right, 0, 0)] = variable(
            f"z{left}{right}"
        )
    for cell in cells:
        result[module.source_cell(*cell)] = variable(carrier_name(cell))
    return result


def primitive_triples(hilbert, torus, basis, cells):
    rays = {
        cell: torus.primitive(torus.quotient_character(cell, basis))
        for cell in cells
    }
    return tuple(
        triple for triple in itertools.combinations(cells, 3)
        if hilbert.positive_three_dependence(
            *(rays[cell] for cell in triple)
        ) is not None
    )


def sparse_eliminations(all_pairs, triples_checker, completion, module,
                        pairs, triples):
    records = []
    for pair in pairs:
        top, _responses, equations = all_pairs.source_equations(
            completion, module, all_pairs.build_q(module, pair)
        )
        ledger = all_pairs.eliminate_pair(equations, top)
        mapping = dict(zip(("x", "y"), pair, strict=True))
        for stage, step in enumerate(ledger):
            records.append(("pair", pair, stage, mapping[step["carrier"]], step))
    for triple in triples:
        _top, _responses, equations = all_pairs.source_equations(
            completion, module, triples_checker.build_q(module, triple)
        )
        ledger = triples_checker.eliminate_triple(all_pairs, equations)
        mapping = dict(zip(("x", "y", "r"), triple, strict=True))
        for stage, step in enumerate(ledger):
            records.append((
                "triple", triple, stage, mapping[step["carrier"]], step
            ))
    return tuple(records)


def main():
    pin_dependencies()
    hilbert = importlib.import_module(
        "verify_n8_one_bad_axis_pure_mixed_weight_hilbert_circuits")
    torus = importlib.import_module(
        "verify_n8_one_bad_axis_pure_chart_torus_accessibility")
    all_pairs = importlib.import_module(
        "verify_n8_one_bad_axis_pure_all_opposing_pair_elimination")
    triples_checker = importlib.import_module(
        "verify_n8_one_bad_axis_pure_all_hilbert_triple_elimination")
    completion = importlib.import_module(
        "verify_n8_one_bad_endpoint_minor_unary_top_completion")
    module = importlib.import_module(
        "verify_n8_one_bad_multisite_permanent_null_defect")

    cells = mixed_cells()
    basis, _pivots = torus.nullspace(torus.equation_matrix())
    pairs = all_pairs.opposing_pairs(torus, basis)
    triples = primitive_triples(hilbert, torus, basis, cells)
    records = sparse_eliminations(
        all_pairs, triples_checker, completion, module, pairs, triples
    )
    require(len(cells) == 90 and len(pairs) == 22 and len(triples) == 58,
            "the carrier circuit universe changed")
    require(len(records) == 44 + 174,
            "the killer occurrence count changed")

    _top, _responses, equations = all_pairs.source_equations(
        completion, module, full_q(module, cells)
    )
    rows = {(sector, "".join(map(str, word))): polynomial
            for sector, word, polynomial in equations}
    require(len(rows) == len(equations), "duplicate literal source row")
    carrier_by_name = {carrier_name(cell): cell for cell in cells}
    nonunit_symbols = frozenset(carrier_by_name) | NONUNIT_PARAMETERS
    allowed_symbols = nonunit_symbols | all_pairs.KNOWN_UNITS

    constraints = defaultdict(list)
    row_term_histogram = Counter()
    row_leads = defaultdict(set)
    carrier_leads = defaultdict(set)
    for family, circuit, stage, selected_cell, step in records:
        key = (step["sector"], step["word"])
        polynomial = rows[key]
        sparse_factors = step["monomial"].split("*")
        selected_symbol = step["carrier"]
        expected_term = tuple(sorted(
            carrier_name(selected_cell) if factor == selected_symbol else factor
            for factor in sparse_factors
        ))
        require(polynomial[expected_term] == Fraction(step["coefficient"]),
                f"selected literal term changed at {family}/{circuit}/{stage}")
        require(set(expected_term) - {carrier_name(selected_cell)}
                <= all_pairs.KNOWN_UNITS,
                f"the selected coefficient stopped being a chart unit: {key}")
        selected_vector = Counter({carrier_name(selected_cell): 1})
        row_leads[key].add((selected_cell, expected_term))
        carrier_leads[selected_cell].add(key)
        for term in polynomial:
            require(set(term) <= allowed_symbols,
                    f"an unclassified source factor entered {key}: {term}")
            if term == expected_term:
                continue
            vector = Counter(factor for factor in term
                             if factor in nonunit_symbols)
            require(vector, f"constant contaminant in {key}: {term}")
            difference = vector.copy()
            difference.subtract(selected_vector)
            difference = Counter({symbol: value
                                  for symbol, value in difference.items()
                                  if value})
            constraints[tuple(sorted(difference.items()))].append({
                "family": family,
                "circuit": circuit,
                "stage": stage,
                "row": key,
                "selected": selected_cell,
                "selected_term": expected_term,
                "contaminant": term,
            })
        row_term_histogram[len(polynomial)] += 1

    require(len(row_leads) == len(carrier_leads) == 54,
            "the row/carrier lead count changed")
    require(all(len(leads) == 1 for leads in row_leads.values())
            and all(len(rows_for_carrier) == 1
                    for rows_for_carrier in carrier_leads.values()),
            "the literal rows and carrier initials stopped being bijective")

    weights = {carrier_name(cell): CARRIER_WEIGHT_OVERRIDES.get(cell, 1)
               for cell in cells}
    weights.update({parameter: 1 for parameter in NONUNIT_PARAMETERS})
    require(set(weights) == nonunit_symbols and min(weights.values()) == 1,
            "the positive source valuation is incomplete")
    margins = tuple(
        sum(coefficient * weights[symbol] for symbol, coefficient in normal)
        for normal in constraints
    )
    require(margins and min(margins) >= 1,
            f"the common source order failed: minimum margin {min(margins)}")

    selected_cells = frozenset(carrier_leads)
    remaining = tuple(cell for cell in cells if cell not in selected_cells)
    require(len(remaining) == 36, "the surviving carrier count changed")
    pairings = tuple(
        sum(coefficient * value for coefficient, value in zip(
            torus.quotient_character(cell, basis), REMAINING_COCHARACTER
        ))
        for cell in remaining
    )
    require(Counter(pairings) == Counter({Fraction(1): 32, Fraction(2): 4}),
            f"the surviving carrier cone stopped being strict: {pairings}")

    row_lead_ledger = {
        f"{sector}@{word}": {
            "cell": cell,
            "term": "*".join(term),
        }
        for (sector, word), singleton in sorted(row_leads.items())
        for cell, term in singleton
    }
    ledger = {
        "dependencies": PINS,
        "source_universe": {
            "mixed_carriers": len(cells),
            "nonunit_pure_star_parameters": len(NONUNIT_PARAMETERS),
            "pair_circuits": len(pairs),
            "primitive_triple_circuits": len(triples),
            "pair_killer_occurrences": 44,
            "triple_killer_occurrences": 174,
        },
        "common_order": {
            "convention": "lowest positive source weight is initial",
            "carrier_weight_histogram": {
                str(weight): count for weight, count in sorted(Counter(
                    weights[carrier_name(cell)] for cell in cells
                ).items())
            },
            "nonunit_parameter_weight": 1,
            "carrier_weight_overrides": {
                carrier_name(cell): weight
                for cell, weight in sorted(CARRIER_WEIGHT_OVERRIDES.items())
            },
            "raw_comparisons": sum(map(len, constraints.values())),
            "distinct_inequality_normals": len(constraints),
            "margin_histogram": {
                str(margin): count
                for margin, count in sorted(Counter(margins).items())
            },
            "inequality_normals": [
                [[symbol, coefficient] for symbol, coefficient in normal]
                for normal in sorted(constraints)
            ],
        },
        "initial_rows": {
            "literal_rows": len(row_leads),
            "distinct_unit_linear_carriers": len(carrier_leads),
            "row_carrier_bijection": row_lead_ledger,
            "pairwise_coprime_leads": True,
        },
        "surviving_carrier_cone": {
            "carriers": len(remaining),
            "cocharacter": REMAINING_COCHARACTER,
            "pairing_histogram": {
                str(pairing): count
                for pairing, count in sorted(Counter(pairings).items())
            },
            "strictly_separated": True,
        },
        "verdict": (
            "one exact positive local source order selects all 54 distinct "
            "unit-linear pair/triple killer rows simultaneously; the "
            "surviving 36 carrier rays lie in one strict open halfspace"
        ),
        "scope": (
            "localized pure-chart associated graded using the 54 literal "
            "pair/triple rows expanded with all 90 mixed q cells; this "
            "removes the need to enumerate higher carrier Hilbert circuits "
            "in this initial-support argument, but does not assert global "
            "ideal membership away from the chart"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the global killer-order ledger changed: {digest}")

    print("N=8 global pair/triple killer order: PASS")
    print("killer occurrences/rows/carriers: 218/54/54")
    print("raw/distinct comparisons:",
          sum(map(len, constraints.values())), len(constraints))
    print("minimum exact margin:", min(margins))
    print("surviving carrier rays/cocharacter minimum: 36/1")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
