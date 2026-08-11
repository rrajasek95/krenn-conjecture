#!/usr/bin/env python3
"""The missing p5 Weierstrass row for the global carrier graph.

The literal response coefficient 11@011011 factors as p5 times a series
whose constant coefficient is the localized unit A*s1*z03.  Its two other
terms use only four of the 54 standard-basis carrier variables.  Hence the
row adds the pairwise-coprime initial p5, forces p5=0 in the completed graph,
and removes the unique negative endpoint weight in the Rees boundary.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
import importlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_n8_one_bad_axis_pure_global_killer_weight_order.py":
        "c75d501cdf545080540d8287b04452d7ca57acc87c980f21ec5b7376e74ca287",
    "computations/verify_n8_one_bad_axis_pure_global_killer_rees_lift_boundary.py":
        "12aeddc9720f1612722599860b796eed354cafc9c10aa0c4164e95020950f062",
    "computations/verify_n8_one_bad_endpoint_minor_arbitrary_pure_unary_completion.py":
        "f77b99d56d817689e55f4790e000799bc34c9b6960d2b9f035300d407562f20a",
    "computations/verify_n8_one_bad_endpoint_minor_mixed_rees_first_order.py":
        "afc1029dac43b66a7bc7fa67a12d658d197b0add9b97dfb85cc918014d41dcc3",
}
EXPECTED_LEDGER_SHA256 = "c4bd7c05ea87190d8d5cec9a8545ef0277a8db1035b53a0c910340690296b266"

P5_ROW = ("11", "011011")
P5_COFACTOR_CARRIERS = (
    (0, 2, 0, 1), (3, 4, 0, 1),
    (0, 4, 0, 1), (2, 3, 1, 0),
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency changed: {relative}: {actual}")


def main():
    pin_dependencies()
    global_order = importlib.import_module(
        "verify_n8_one_bad_axis_pure_global_killer_weight_order")
    torus = importlib.import_module(
        "verify_n8_one_bad_axis_pure_chart_torus_accessibility")
    all_pairs = importlib.import_module(
        "verify_n8_one_bad_axis_pure_all_opposing_pair_elimination")
    triples_checker = importlib.import_module(
        "verify_n8_one_bad_axis_pure_all_hilbert_triple_elimination")
    hilbert = importlib.import_module(
        "verify_n8_one_bad_axis_pure_mixed_weight_hilbert_circuits")
    completion = importlib.import_module(
        "verify_n8_one_bad_endpoint_minor_unary_top_completion")
    module = importlib.import_module(
        "verify_n8_one_bad_multisite_permanent_null_defect")

    cells = global_order.mixed_cells()
    basis, _pivots = torus.nullspace(torus.equation_matrix())
    records = global_order.sparse_eliminations(
        all_pairs, triples_checker, completion, module,
        all_pairs.opposing_pairs(torus, basis),
        global_order.primitive_triples(hilbert, torus, basis, cells),
    )
    selected = frozenset(record[3] for record in records)
    survivors = tuple(cell for cell in cells if cell not in selected)
    require(len(selected) == 54 and len(survivors) == 36
            and set(P5_COFACTOR_CARRIERS) <= selected,
            "the 54/36 graph or p5 cofactor carrier class changed")

    top, responses, equations = all_pairs.source_equations(
        completion, module, global_order.full_q(module, cells)
    )
    rows = {(sector, "".join(map(str, word))): polynomial
            for sector, word, polynomial in equations}
    p5_polynomial = responses["11"][tuple(map(int, P5_ROW[1]))]
    expected_p5 = Counter({
        tuple(sorted(("A", "p5", "s1", "z03"))): Fraction(1),
        tuple(sorted(("m0201", "m3401", "p5", "s1"))): Fraction(1),
        tuple(sorted(("m0401", "m2310", "p5", "s1"))): Fraction(1),
    })
    require(rows[P5_ROW] == p5_polynomial == expected_p5,
            "the literal p5 Weierstrass row changed")

    # Recheck the stronger carrier-only order: pure/star factors are treated
    # as arbitrary coefficients, not assigned positive filtration.  Thus the
    # 54 rows form a graph over the entire localized pure coefficient ring.
    carrier_by_name = {
        global_order.carrier_name(cell): cell for cell in cells
    }
    row_leads = defaultdict(set)
    carrier_margins = []
    used_rows = set()
    for family, circuit, stage, selected_cell, step in records:
        key = (step["sector"], step["word"])
        polynomial = rows[key]
        expected_term = tuple(sorted(
            global_order.carrier_name(selected_cell)
            if factor == step["carrier"] else factor
            for factor in step["monomial"].split("*")
        ))
        require(polynomial[expected_term] == Fraction(step["coefficient"]),
                f"a selected graph term changed at {family}/{circuit}/{stage}")
        row_leads[key].add((selected_cell, expected_term))
        used_rows.add(key)
        selected_weight = global_order.CARRIER_WEIGHT_OVERRIDES.get(
            selected_cell, 1
        )
        for term in polynomial:
            if term == expected_term:
                continue
            contaminant_cells = tuple(
                carrier_by_name[factor] for factor in term
                if factor in carrier_by_name
            )
            require(contaminant_cells,
                    f"a carrier-free contaminant entered graph row {key}")
            carrier_margins.append(sum(
                global_order.CARRIER_WEIGHT_OVERRIDES.get(cell, 1)
                for cell in contaminant_cells
            ) - selected_weight)
    require(len(row_leads) == 54
            and all(len(leads) == 1 for leads in row_leads.values())
            and min(carrier_margins) >= 1,
            "the carrier-only formal graph order failed")

    # The p5 term has source weight one; its two tails have weight three.
    # Its leading variable is distinct from all 54 q-carrier leads.
    p5_margins = tuple(
        sum(global_order.CARRIER_WEIGHT_OVERRIDES.get(
            carrier_by_name[factor], 1
        ) for factor in term if factor in carrier_by_name)
        for term in p5_polynomial
        if "A" not in term
    )
    require(p5_margins == (2, 2)
            and all("p5" not in term
                    for leads in row_leads.values()
                    for _cell, term in leads),
            "p5 stopped being a new pairwise-coprime initial variable")

    # Exact target-character homogeneity under the separator.  All 54 graph
    # variables have weight zero, the 36 parameters are positive, and p5 is
    # the only displayed negative endpoint.  The new row sets it to zero.
    separator = global_order.REMAINING_COCHARACTER

    def cell_weight(cell):
        return sum(left * right for left, right in zip(
            torus.quotient_character(cell, basis), separator, strict=True
        ))

    symbol_cells = {
        "A": (2, 4, 1, 1), "B": (3, 5, 1, 1),
        "C": (0, 5, 2, 2), "D": (1, 4, 2, 2),
        "p0": (0, 6, 1, 1), "p5": (5, 6, 1, 1),
        "p2": (2, 6, 2, 2), "s1": (1, 7, 1, 1),
        "s2": (3, 7, 2, 2),
    }
    symbol_cells.update({f"z{left}{right}": (left, right, 0, 0)
                         for left in range(6) for right in range(left + 1, 6)})
    symbol_cells.update(carrier_by_name)

    def term_weight(term):
        return sum(cell_weight(symbol_cells[factor]) for factor in term)

    for key in used_rows | {P5_ROW}:
        require(len({term_weight(term) for term in rows[key]}) == 1,
                f"target homogeneity failed in {key}")
    tensor_polynomials = tuple(top.values()) + tuple(
        polynomial for tensor in responses.values()
        for polynomial in tensor.values()
    )
    require(all(len({term_weight(term) for term in polynomial}) == 1
                for polynomial in tensor_polynomials),
            "full five-tensor target homogeneity failed")
    require(Counter(cell_weight(cell) for cell in selected)
            == Counter({Fraction(0): 54})
            and Counter(cell_weight(cell) for cell in survivors)
            == Counter({Fraction(1): 32, Fraction(2): 4})
            and cell_weight((5, 6, 1, 1)) == -1,
            "the target separator partition changed")

    ledger = {
        "dependencies": PINS,
        "formal_graph": {
            "carrier_rows": len(row_leads),
            "carrier_variables": len(selected),
            "parameters": len(survivors),
            "carrier_only_minimum_margin": min(carrier_margins),
            "pure_star_coefficients_are_base_ring": True,
        },
        "p5_weierstrass_row": {
            "label": "11@011011",
            "polynomial": completion.serial_polynomial(p5_polynomial),
            "unit_constant_factor": "A*s1*z03",
            "tail_carriers": P5_COFACTOR_CARRIERS,
            "tail_source_margins": p5_margins,
            "new_initial": "p5",
        },
        "combined_standard_block": {
            "rows": 55,
            "pairwise_coprime_linear_initials": 55,
            "formal_consequence": "p5=0",
        },
        "target_separator": {
            "selected_zero": 54,
            "survivor_positive": {"1": 32, "2": 4},
            "p5_before_row": -1,
            "p5_after_row": "zero in the completed quotient",
            "all_five_tensors_homogeneous": len(tensor_polynomials),
        },
        "verdict": (
            "the complete literal response rows force p5=0 in the localized "
            "mixed completion, so the negative endpoint obstruction of "
            "aaed0f5 disappears; target-equivariance then lands the formal "
            "graph in the pure chart and the 260bb94 unit lifts by Nakayama"
        ),
        "scope": (
            "all 90 mixed q cells in the established 54-variable formal "
            "graph with the pinned axis-pure endpoint rows; this is a "
            "completed-local Weierstrass statement, not an affine assertion "
            "at distant points where the cofactor bracket may vanish"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the p5 Weierstrass ledger changed: {digest}")

    print("N=8 global killer p5 Weierstrass row: PASS")
    print("literal row: 11@011011 = p5*s1*(A*z03 + two mixed products)")
    print("combined unit-linear initials: 55")
    print("formal consequence: p5=0")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
