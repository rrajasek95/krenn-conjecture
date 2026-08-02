#!/usr/bin/env python3
"""Verify the path-forest skeleton of the first chart-26 Groebner layers.

This is a structural audit of already certified polynomials.  It forgets
endpoint colours only after the exact decorated leading monomial has been
computed.  The degree-four leads are perfect matchings, every degree-five
lead is a spanning linear forest of type P4+P2+P2, and the first genuine
degree-six compatibility cell contains 300 simple spanning linear forests
obtained by joining two components.  The certified weighted lead is one of
the P6+P2 terms; the old lexicographic lead repeats a coordinate.

The finite census motivates a uniform forest straightening law.  It does not
prove that all degree-six cells, or any higher-order chart, admit compatible
forest leads.
"""

from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
COMPLETE_PATH = HERE / "verify_n8_chart26_complete_degree5_buchberger.py"
COMPLETE_SPEC = importlib.util.spec_from_file_location(
    "n8_chart26_complete_d5_forest", COMPLETE_PATH
)
COMPLETE = importlib.util.module_from_spec(COMPLETE_SPEC)
COMPLETE_SPEC.loader.exec_module(COMPLETE)

WEIGHT_PATH = HERE / "verify_n8_chart26_feasible_squarefree_weight.py"
WEIGHT_SPEC = importlib.util.spec_from_file_location(
    "n8_chart26_weighted_d6_forest", WEIGHT_PATH
)
WEIGHT = importlib.util.module_from_spec(WEIGHT_SPEC)
WEIGHT_SPEC.loader.exec_module(WEIGHT)

FIRST = COMPLETE.FIRST
D5 = COMPLETE.D5

EXPECTED_LEDGER_SHA256 = (
    "69a673706d95c40e838136743d93ba0a1ba13d3542ae7686e6625c8ca9699475"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def skeleton(row):
    """Return the uncoloured multigraph data of a decorated monomial."""
    edges = tuple(D5.COORDINATES[variable][:2] for variable in row)
    multiplicities = Counter(edges)
    adjacency = {vertex: set() for edge in multiplicities for vertex in edge}
    for left, right in multiplicities:
        adjacency[left].add(right)
        adjacency[right].add(left)

    seen = set()
    component_sizes = []
    for root in adjacency:
        if root in seen:
            continue
        seen.add(root)
        stack = [root]
        size = 0
        while stack:
            vertex = stack.pop()
            size += 1
            for neighbour in adjacency[vertex]:
                if neighbour not in seen:
                    seen.add(neighbour)
                    stack.append(neighbour)
        component_sizes.append(size)

    simple_edges = len(multiplicities)
    vertices = len(adjacency)
    components = len(component_sizes)
    cycle_rank = simple_edges - vertices + components
    return {
        "decorated_squarefree": len(row) == len(set(row)),
        "underlying_simple": len(row) == simple_edges,
        "spanning": set(adjacency) == set(range(8)),
        "maximum_simple_degree": max(map(len, adjacency.values()), default=0),
        "cycle_rank": cycle_rank,
        "component_sizes": tuple(sorted(component_sizes, reverse=True)),
    }


def is_linear_forest(record, component_sizes):
    return (
        record["decorated_squarefree"]
        and record["underlying_simple"]
        and record["spanning"]
        and record["maximum_simple_degree"] <= 2
        and record["cycle_rank"] == 0
        and record["component_sizes"] == component_sizes
    )


def degree6_type(row):
    record = skeleton(row)
    if is_linear_forest(record, (6, 2)):
        return "linear_forest_P6_P2"
    if is_linear_forest(record, (4, 4)):
        return "linear_forest_P4_P4"
    if not record["decorated_squarefree"]:
        return "repeated_decorated_coordinate"
    if not record["underlying_simple"]:
        return "parallel_underlying_edge_distinct_decorations"
    if record["cycle_rank"]:
        return "underlying_cycle"
    return "other"


def audit():
    polynomials, lead_to_code = FIRST.original_basis()
    code_to_lead = {code: lead for lead, code in lead_to_code.items()}

    original_types = Counter()
    for lead in code_to_lead.values():
        record = skeleton(lead)
        require(is_linear_forest(record, (2, 2, 2, 2)),
                "an original lead is not an uncoloured perfect matching")
        original_types[record["component_sizes"]] += 1

    pairs, _cores, _histogram = COMPLETE.build_pairs(code_to_lead)
    degree5_types = Counter()
    decorated_degree5_leads = set()
    for lcm, first_code, second_code in pairs:
        polynomial = COMPLETE.s_polynomial(
            lcm, first_code, second_code, polynomials, code_to_lead
        )
        lead = FIRST.leading_monomial(polynomial)
        record = skeleton(lead)
        require(is_linear_forest(record, (4, 2, 2)),
                "a degree-five lead left the P4+P2+P2 forest stratum")
        degree5_types[record["component_sizes"]] += 1
        decorated_degree5_leads.add(lead)
    require(len(decorated_degree5_leads) == 84005,
            "degree-five decorated leads collided")

    degree6 = WEIGHT.reconstruct_degree6_cell()
    top_degree = max(map(len, degree6))
    require(top_degree == 6, "compatibility cell top degree changed")
    degree6_types = Counter(
        degree6_type(row) for row in degree6 if len(row) == top_degree
    )
    require(degree6_types == Counter({
        "linear_forest_P6_P2": 200,
        "linear_forest_P4_P4": 100,
        "parallel_underlying_edge_distinct_decorations": 44,
        "repeated_decorated_coordinate": 22,
        "underlying_cycle": 6,
    }), "degree-six path/cycle/parallel census changed")

    weighted_lead = WEIGHT.weighted_lead(degree6)
    old_lex_lead = FIRST.leading_monomial(degree6)
    require(weighted_lead.hex() == "0951b4c7ebf5",
            "weighted compatibility lead changed")
    require(degree6_type(weighted_lead) == "linear_forest_P6_P2",
            "weighted lead is not a component-joining path forest")
    require(old_lex_lead.hex() == "0948cfcfebef",
            "old lexicographic compatibility lead changed")
    require(degree6_type(old_lex_lead)
            == "repeated_decorated_coordinate",
            "old lexicographic lead no longer repeats a coordinate")

    ledger = {
        "original_degree4_leads": len(code_to_lead),
        "original_skeleton": "P2+P2+P2+P2",
        "degree5_leads": len(decorated_degree5_leads),
        "degree5_skeleton": "P4+P2+P2",
        "degree6_top_terms": sum(degree6_types.values()),
        "degree6_structural_types": dict(sorted(degree6_types.items())),
        "degree6_simple_component_join_terms": (
            degree6_types["linear_forest_P6_P2"]
            + degree6_types["linear_forest_P4_P4"]
        ),
        "weighted_degree6_lead": weighted_lead.hex(),
        "weighted_degree6_skeleton": "P6+P2",
        "old_lex_degree6_lead": old_lex_lead.hex(),
        "old_lex_degree6_type": degree6_type(old_lex_lead),
        "conclusion": (
            "the completed d4/d5 leads and the repaired first d6 lead "
            "follow a spanning path-forest component-joining skeleton"
        ),
        "scope_guard": (
            "this is a finite structural census, not a completed d6 "
            "Groebner basis or a uniform straightening theorem"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return ledger, digest


def main():
    ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                "frozen path-forest ledger changed")
    print(
        "n=8 chart26 path-forest skeleton: PASS; "
        "d4/d5=6558/84005, d6 forest/nonforest=300/72"
    )
    print(json.dumps(ledger, sort_keys=True))
    print("sha256:", digest)


if __name__ == "__main__":
    main()
