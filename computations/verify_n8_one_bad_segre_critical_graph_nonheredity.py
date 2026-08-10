#!/usr/bin/env python3
"""Exact non-heredity counterguard for the Segre critical-pair graph.

The 17 active coordinates of the full six-row transgression have nine
quadratic edges.  Their nontrivial colour-1 component contains one C4.
After setting the diagonal variables to one, the primary functional on this
cycle has a nonzero torus solution, so the edge terms cancel globally.

More sharply, replay the pinned exact source lift for the unit edge
03:10+12:02.  Adjoining the adjacent vertex 14:02 changes the same literal
source rows.  The old lift becomes 2+R with a nonzero, exactly factored
residue R.  Pair-unit certificates are therefore not hereditary under larger
support, and no vertex-cover argument can use them without transition data.
"""

from __future__ import annotations

from collections import Counter, defaultdict, deque
from fractions import Fraction
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import itertools
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
FULL_PATH = (
    "computations/verify_n8_one_bad_segre_"
    "full_deformation_critical_pair.py"
)
FULL_NOTE = "notes/n8-one-bad-segre-full-deformation-critical-pair.md"
PAIR_PATH = (
    "computations/verify_n8_one_bad_segre_cube_critical_two_cell_units.py"
)
PAIR_NOTE = "notes/n8-one-bad-segre-cube-critical-two-cell-units.md"
PINS = {
    FULL_PATH:
        "16b1795fcd25cd4f668e3076d8ad9aa17b98b10289107eb07d83c15f6271a6f3",
    FULL_NOTE:
        "2d873c77bab5e2c722f2bf4e5e4f9df05ecd62b5f52f51abf2279acf2ef2a00b",
    PAIR_PATH:
        "5330151a54bf56fe71690faafeb342fce69932329a66c9e301c65559a5116c1f",
    PAIR_NOTE:
        "44a386f6ff5dffdec2506b2b1286ef137087b40be37aa1a705828c2a4c87b35d",
}
EXPECTED_RESIDUE_SHA256 = "4b822123aa50872777f2d48588da6bfc6ce6aec4ffcf00f93f66e188343504bc"
EXPECTED_DIGEST = "f84285cf54e7693a6efa8353716ddc84fc064c022162325ae14d147591837c68"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_pinned(name, relative):
    path = ROOT / relative
    actual = sha256(path.read_bytes()).hexdigest()
    require(actual == PINS[relative],
            f"pinned dependency changed: {relative}: {actual}")
    spec = spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None,
            f"cannot load {relative}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def graph_components(vertices, edges):
    adjacency = {vertex: set() for vertex in vertices}
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    components = []
    unseen = set(vertices)
    while unseen:
        root = min(unseen)
        queue = deque((root,))
        component = set()
        while queue:
            vertex = queue.popleft()
            if vertex in component:
                continue
            component.add(vertex)
            queue.extend(adjacency[vertex] - component)
        unseen -= component
        component_edges = tuple(
            edge for edge in edges
            if edge[0] in component and edge[1] in component
        )
        components.append((tuple(sorted(component)), component_edges))
    return adjacency, tuple(sorted(components, key=lambda item: item[0]))


def critical_graph_audit(full_module, pair_module):
    first_variation = full_module.load_pinned(
        "segre_first_variation_for_graph", full_module.FIRST_PATH
    )
    inherited = first_variation.audit_first_variation(
        first_variation.load_dependency()
    )
    vertices = {
        label for label, _terms in
        inherited["dangerous_cells_and_term_counts"]
    } | {"12:02"}
    edges = tuple((left, right) for left, right, *_rest in pair_module.CRITICAL)
    require(len(vertices) == 17 and len(edges) == 9,
            "critical graph size changed")
    adjacency, components = graph_components(vertices, edges)
    nontrivial = tuple(component for component in components
                       if component[1])
    isolated = tuple(component[0][0] for component in components
                     if not component[1])
    require(len(nontrivial) == 2 and len(isolated) == 7,
            "critical graph component census changed")

    cycle = ("03:10", "12:02", "05:10", "14:02")
    cycle_edges = {
        tuple(sorted((cycle[index], cycle[(index + 1) % len(cycle)])))
        for index in range(len(cycle))
    }
    undirected_edges = {tuple(sorted(edge)) for edge in edges}
    require(cycle_edges <= undirected_edges,
            "the critical C4 disappeared")
    first_component = next(component for component in nontrivial
                           if "12:02" in component[0])
    cycle_rank = len(first_component[1]) - len(first_component[0]) + 1
    require(cycle_rank == 1,
            "the colour-1 critical component stopped having one cycle")
    second_component = next(component for component in nontrivial
                            if "15:01" in component[0])
    require(len(second_component[0]) == 4
            and len(second_component[1]) == 3
            and len(adjacency["15:01"]) == 3,
            "the colour-2 K1,3 component changed")
    return first_variation, {
        "vertices": len(vertices),
        "edges": len(edges),
        "components": len(components),
        "isolated_vertices": list(isolated),
        "nontrivial_component_shapes": [
            {
                "vertices": list(component_vertices),
                "edges": [list(edge) for edge in component_edges],
                "cycle_rank": len(component_edges) - len(component_vertices) + 1,
            }
            for component_vertices, component_edges in nontrivial
        ],
        "unique_C4": list(cycle),
    }


def primary_cycle_audit(full_module, first_variation):
    _source, _edges, missing, functional = full_module.full_functional(
        first_variation
    )
    labels = {
        45 + index: first_variation.cell_label(cell)
        for index, cell in enumerate(missing)
    }
    cycle = {"03:10", "05:10", "12:02", "14:02"}
    restricted = defaultdict(Fraction)
    for monomial, coefficient in functional.items():
        deformation = tuple(labels[index] for index in monomial
                            if index >= 45)
        if any(label not in cycle for label in deformation):
            continue
        # All 45 diagonal variables are specialized to one.
        restricted[tuple(sorted(deformation))] += coefficient
    restricted = {monomial: coefficient
                  for monomial, coefficient in restricted.items()
                  if coefficient}
    expected = {
        ("03:10",): Fraction(4),
        ("14:02",): Fraction(3),
        ("03:10", "14:02"): Fraction(4),
        ("05:10", "14:02"): Fraction(4),
        ("03:10", "12:02"): Fraction(-2),
        ("05:10", "12:02"): Fraction(-2),
    }
    require(restricted == expected,
            f"critical C4 polynomial changed: {restricted}")

    values = {
        "03:10": Fraction(1),
        "05:10": Fraction(1),
        "14:02": Fraction(1),
        "12:02": Fraction(15, 4),
    }
    evaluation = sum(
        (coefficient
         * product(values[label] for label in monomial)
         for monomial, coefficient in restricted.items()),
        Fraction(0),
    )
    require(evaluation == 0 and all(values.values()),
            "the coefficient-consistent critical C4 point changed")
    return {
        "diagonal_specialization": "d0=...=d44=1",
        "cycle_polynomial": (
            "4*x+3*v+4*x*v+4*z*v-2*x*u-2*z*u"
        ),
        "variables": {
            "x": "03:10", "z": "05:10",
            "u": "12:02", "v": "14:02",
        },
        "nonzero_rational_zero": {
            label: str(value) for label, value in values.items()
        },
    }


def product(values):
    answer = Fraction(1)
    for value in values:
        answer *= value
    return answer


def build_generators(pair_module, first_variation, source, support):
    labels = []
    generators = []
    for word in itertools.product(range(3), repeat=6):
        polynomial = first_variation.coefficient(source, support, word)
        if not polynomial:
            continue
        target = int(word == (0,) * 6)
        expression = pair_module.singular_polynomial(polynomial)
        if target:
            expression = f"({expression})-1"
        labels.append("".join(map(str, word)))
        generators.append(expression)
    return labels, generators


def pair_lift_nonheredity(pair_module):
    first_variation = pair_module.load_dependency()
    first_variation.VARIABLE_COUNT = 48
    first_variation.ZERO_EXPONENT = (0,) * 48
    diagonal_unit = first_variation.load_dependency()
    source, _edges, _variables, base, _multipliers = first_variation.setup(
        diagonal_unit
    )

    pair = ("03:10", "12:02")
    extra = "14:02"
    pair_support = dict(base)
    pair_support[pair_module.parse_cell(pair[0])] = (
        first_variation.poly_variable(45)
    )
    pair_support[pair_module.parse_cell(pair[1])] = (
        first_variation.poly_variable(46)
    )
    expanded_support = dict(pair_support)
    expanded_support[pair_module.parse_cell(extra)] = (
        first_variation.poly_variable(47)
    )

    labels, pair_generators = build_generators(
        pair_module, first_variation, source, pair_support
    )
    expanded_labels, expanded_generators = build_generators(
        pair_module, first_variation, source, expanded_support
    )
    expanded_by_label = dict(zip(expanded_labels, expanded_generators,
                                 strict=True))
    require(all(label in expanded_by_label for label in labels),
            "an old source row disappeared after adjoining the third cell")
    aligned_expanded = [expanded_by_label[label] for label in labels]

    variables = ",".join(f"x{index}" for index in range(48))
    program = f"ring r=0,({variables}),dp; option(redSB);\n"
    program += "ideal I=" + ",".join(pair_generators) + ";\n"
    program += "matrix L; ideal G=liftstd(I,L);\n"
    program += "ideal J=" + ",".join(aligned_expanded) + ";\n"
    program += "matrix R=matrix(J)*L-matrix(G); poly rr=R[1,1];\n"
    program += "poly P=x4*x9+x2*x11+x1*x13; poly Q=rr/(x47*P);\n"
    program += (
        "if(size(G)!=1 || G[1]!=2){ print(\"PAIR_UNIT_FAILED\"); }\n"
        "if(matrix(I)*L-matrix(G)!=0){ print(\"PAIR_LIFT_FAILED\"); }\n"
        "if(rr==0 || rr-x47*P*Q!=0){ print(\"RESIDUE_FACTOR_FAILED\"); }\n"
        "if(size(rr)!=48 || size(P)!=3 || size(Q)!=16){ "
        "print(\"RESIDUE_SIZE_FAILED\"); }\n"
    )
    program += "poly E=rr;\n"
    for index in range(48):
        program += f"E=subst(E,x{index},1);\n"
    program += (
        "if(E!=12){ print(\"RESIDUE_VALUE_FAILED\"); }\n"
        "print(\"RESIDUE\"); print(rr);\n"
        "print(\"QFACTOR\"); print(Q);\n"
        "quit;\n"
    )
    result = subprocess.run(
        ("/usr/local/bin/Singular", "-q"),
        input=program,
        text=True,
        capture_output=True,
        check=False,
        timeout=30,
    )
    require(result.returncode == 0,
            f"Singular pair-transition audit failed: "
            f"{result.stderr or result.stdout}")
    require("FAILED" not in result.stdout,
            f"pair-transition assertion failed: {result.stdout}")
    residue = result.stdout.split("RESIDUE\n", 1)[1].split(
        "\nQFACTOR", 1
    )[0]
    residue_digest = sha256(residue.encode()).hexdigest()
    require(EXPECTED_RESIDUE_SHA256 != "TO_BE_FILLED",
            "pin EXPECTED_RESIDUE_SHA256")
    require(residue_digest == EXPECTED_RESIDUE_SHA256,
            f"pair-lift residue changed: {residue_digest}")
    return {
        "unit_pair": list(pair),
        "adjoined_adjacent_vertex": extra,
        "old_pair_unit": "2",
        "same_lift_after_adjoining": "2+R",
        "residue_terms": 48,
        "residue_factorization": "R=x_14:02*P_3*Q_16",
        "P_3": "d05*d23+d03*d25+d02*d35",
        "Q_16_terms": 16,
        "residue_at_all_variables_one": 12,
        "residue_sha256": residue_digest,
    }


def main():
    full_module = load_pinned("segre_full_deformation", FULL_PATH)
    pair_module = load_pinned("segre_pair_units", PAIR_PATH)
    require(sha256((ROOT / FULL_NOTE).read_bytes()).hexdigest()
            == PINS[FULL_NOTE], "full-deformation note changed")
    require(sha256((ROOT / PAIR_NOTE).read_bytes()).hexdigest()
            == PINS[PAIR_NOTE], "pair-unit note changed")
    first_variation, graph = critical_graph_audit(full_module, pair_module)
    cycle = primary_cycle_audit(full_module, first_variation)
    nonheredity = pair_lift_nonheredity(pair_module)
    ledger = {
        "pins": PINS,
        "critical_graph": graph,
        "coefficient_consistent_C4": cycle,
        "exact_pair_lift_nonheredity": nonheredity,
        "verdict": (
            "the nine exact pair units do not form a hereditary vertex-cover "
            "certificate: the primary graph has a coefficient-consistent C4 "
            "and an adjacent active coordinate gives a nonzero residue in a "
            "pinned pair source lift"
        ),
        "invisible_scope_guard": (
            "59 deformation directions are absent from the primary six-row "
            "functional, but their cross-variation against alternative and "
            "pair unit certificates is not controlled by this graph"
        ),
        "required_global_object": (
            "a source-labelled transition complex for unit certificates, or "
            "a response-compatible S-pair completion; graph occupancy alone "
            "is insufficient"
        ),
        "scope": (
            "exact primary-cycle and one pinned-lift transition counterguard; "
            "not a higher-support feasibility census or one-bad source"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    require(EXPECTED_DIGEST != "TO_BE_FILLED", "pin EXPECTED_DIGEST")
    require(digest == EXPECTED_DIGEST,
            ("critical-graph nonheredity ledger changed", digest))
    print("N=8 Segre critical-graph nonheredity: PASS")
    print("graph: unique C4 plus K1,3 and seven isolated vertices")
    print("primary C4 has a nonzero rational torus cancellation")
    print("pair lift 03:10+12:02 acquires 48-term residue under 14:02")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
