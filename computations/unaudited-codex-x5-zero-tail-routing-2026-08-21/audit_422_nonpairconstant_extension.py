#!/usr/bin/env python3
"""Exact sparse classification of the four missing 422 source orbits.

The full 440/2110 extension is treated as frozen input.  This audit derives
one literal Q*X*X polynomial per 422 orbit, proves the 72-row orbit is an
e-row multiple, and gives exact characteristic-zero nonmembership witnesses
for the other three rows in the degree-at-most-four extended-master span.
It also freezes B4 x S3 transport and the X*C cofactor antecedents.

No Groebner basis is used.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
import importlib.util
from itertools import permutations, product
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ROUTING = HERE / "results_x5_zero_tail_routing.json"
FULL440 = HERE / "results_440_2110_extension.json"
FULL440_LABELS = HERE / "extension_440_2110_source_labels.json"
FULL440_SCRIPT = HERE / "audit_440_2110_extension.py"
OUT = HERE / "results_422_nonpairconstant_extension.json"
SUPPORT6_CERT = (ROOT /
    "computations/unaudited-codex-n8-dangerous-chart-bridge-2026-08-20" /
    "results_support6_fixed_left_partner_certificate_audit.json")
SUPPORT8_CERT = (ROOT /
    "computations/unaudited-codex-orbit0-t2-radical-2026-08-20" /
    "results_forced_one_y_mate_unit_identity.json")

TARGETS = (
    "01010202",  # orbit 288
    "00010212",  # orbit 576
    "00001212",  # orbit 72, exact e multiple
    "00010122",  # orbit 288
)
EXPECTED_ORBITS = {
    "01010202": "422_two_edges_to_each_minor_colour",
    "00010212": "422_majority_loop_colour_triangle",
    "00001212": "422_two_majority_loops_two_minor_cross_edges",
    "00010122": "422_majority_loop_minor_loop_two_cross_edges",
}
EXPECTED_SIZES = {
    "01010202": 288, "00010212": 576,
    "00001212": 72, "00010122": 288,
}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    require(spec.loader is not None, f"missing loader for {path}")
    spec.loader.exec_module(module)
    return module


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


EXT = load("x5_422_full440_core", FULL440_SCRIPT)


def file_sha(path):
    return sha256(path.read_bytes()).hexdigest()


def logical_sha(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def vertex_actions():
    actions = set()
    for block_permutation in permutations(range(4)):
        for flips in product((0, 1), repeat=4):
            action = []
            for vertex in range(8):
                block, clone = divmod(vertex, 2)
                action.append(2*block_permutation[block]
                              + (clone ^ flips[block]))
            actions.add(tuple(action))
    require(len(actions) == 384, "B4 action order changed")
    return tuple(sorted(actions))


def act_word(label, vertex_action, colour_permutation):
    old = tuple(map(int, label))
    new = [None]*8
    for vertex, colour in enumerate(old):
        new[vertex_action[vertex]] = colour_permutation[colour]
    return "".join(map(str, new))


def word_orbit(label, actions):
    return frozenset(act_word(label, action, colour_permutation)
                     for action in actions
                     for colour_permutation in permutations(range(3)))


def factor_data(label):
    word = tuple(map(int, label))
    counts = Counter(word)
    majority = next(colour for colour, count in counts.items() if count == 4)
    minors = tuple(sorted(colour for colour, count in counts.items()
                          if count == 2))
    majority_sites = tuple(index for index, colour in enumerate(word)
                           if colour == majority)
    minor_edges = {
        colour: tuple(index for index, value in enumerate(word)
                      if value == colour)
        for colour in minors
    }
    return majority, minors, majority_sites, minor_edges


def cx_word(cofactor_colour, entry_colour, edge):
    word = [cofactor_colour]*8
    for site in edge:
        word[site] = entry_colour
    return "".join(map(str, word))


def forced_cofactor_rows(label, master_labels):
    majority, (minor0, minor1), _sites, edges = factor_data(label)
    edge0, edge1 = edges[minor0], edges[minor1]
    specs = (
        (majority, minor0, edge0),
        (majority, minor1, edge1),
        (minor1, minor0, edge0),
        (minor0, minor1, edge1),
    )
    records = []
    for cofactor_colour, entry_colour, edge in specs:
        source_label = cx_word(cofactor_colour, entry_colour, edge)
        require(source_label in master_labels,
                ("forced X*C row left master", label, source_label))
        records.append({
            "master_source_label": source_label,
            "nonzero_antecedent": f"X_{entry_colour}[{edge[0]}{edge[1]}]",
            "forced_zero": f"C_{cofactor_colour}[{edge[0]}{edge[1]}]",
        })
    return records


def extended_rows():
    rows = EXT.base_macaulay_rows(3, 72)
    for left, right in EXT.combinations(range(3), 2):
        rows.extend(EXT.cross_620_rows(left, right))
        rows.extend(EXT.full_440_rows(left, right))
    require(len(rows) == 49848, "extended degree-four master changed")
    return rows


def incidence_components(rows, targets):
    incidence = defaultdict(list)
    for row_index, row in enumerate(rows):
        for monomial in row:
            incidence[monomial].append(row_index)
    records = {}
    for label, target in targets.items():
        monomials = set(target)
        row_indices = set()
        frontier = list(monomials)
        while frontier:
            monomial = frontier.pop()
            for row_index in incidence.get(monomial, ()):
                if row_index in row_indices:
                    continue
                row_indices.add(row_index)
                for new_monomial in rows[row_index]:
                    if new_monomial not in monomials:
                        monomials.add(new_monomial)
                        frontier.append(new_monomial)
        records[label] = (tuple(sorted(row_indices)),
                          tuple(sorted(monomials,
                                       key=lambda value: (len(value), value))))
    return records


def exact_rank(rows, columns):
    """Integer sparse rank; all pivots in the audited component are +/-1."""
    basis = {}
    for row in rows:
        work = Counter(row)
        while work:
            lead = max(work, key=lambda monomial: (len(monomial), monomial))
            if lead not in basis:
                pivot = work[lead]
                require(abs(pivot) == 1,
                        ("nonunit exact pivot", lead, pivot))
                if pivot == -1:
                    work = Counter({key: -value for key, value in work.items()})
                basis[lead] = work
                break
            factor = work[lead]
            work.subtract({key: factor*value
                           for key, value in basis[lead].items()})
            work = Counter({key: value for key, value in work.items() if value})
    return len(basis)


def name_monomial(names):
    name_to_index = {EXT.variable_name(index): index for index in range(72)}
    return tuple(sorted(name_to_index[name] for name in names))


def main():
    for path in (ROUTING, FULL440, FULL440_LABELS, SUPPORT6_CERT,
                 SUPPORT8_CERT):
        require(path.is_file(), f"missing upstream {path}")
    routing = json.loads(ROUTING.read_text())
    full440 = json.loads(FULL440.read_text())
    full440_labels = json.loads(FULL440_LABELS.read_text())
    support6 = json.loads(SUPPORT6_CERT.read_text())
    support8 = json.loads(SUPPORT8_CERT.read_text())
    require(routing["logical_sha256"] ==
            "85a18c7f6c02678fe9806ca8ab9654643c5f6b0637867d4f2b71d181e3b21171",
            "zero-tail routing changed")
    require(full440["logical_sha256"] ==
            "1f149274216c298e1edf3468f3982f45aaa39ccb9dff45975c7bfb0625c0f04f",
            "full-440 extension changed")
    require(file_sha(FULL440_LABELS) ==
            "e958ec78badfbc6d2b656838dcc8d58eeb08287a349b16299b89080ebab7f643",
            "full-440 source-label export changed")

    route_by_word = {row["canonical_word"]: row
                     for row in routing["routing_table"]}
    actions = vertex_actions()
    master_sectors = load("x5_422_routing_source", HERE /
                          "audit_x5_zero_tail_routing.py").master_packet()
    master_labels = set().union(*master_sectors.values())

    targets = {label: EXT.word_poly(label, colours=3) for label in TARGETS}
    require(all(len(polynomial) == 3 for polynomial in targets.values()),
            "a canonical 422 polynomial ceased to have three terms")
    rows = extended_rows()
    components = incidence_components(rows, targets)

    # Two genuinely tricolour targets occupy coordinates which never occur
    # in the extended degree-four master.  This is exact over Z.
    for label in ("01010202", "00010212"):
        row_indices, monomials = components[label]
        require(not row_indices and set(monomials) == set(targets[label]),
                ("isolated target component changed", label,
                 len(row_indices), len(monomials)))

    # The smallest R*X target meets only a 22-by-69 connected component.
    # An explicit four-coordinate integer dual annihilates the entire 49,848
    # row master, while pairing to one with the target.
    dual_00010122 = {
        name_monomial(("x0_00_10", "x0_01_20", "x1_11_21")): 1,
        name_monomial(("x0_10_20", "x1_00_11", "x1_01_21")): 1,
        name_monomial(("x0_10_20", "x1_11_30", "x1_21_31")): -1,
        name_monomial(("x0_10_30", "x0_20_31", "x1_11_21")): -1,
    }

    def pairing(poly, functional):
        return sum(coefficient*functional.get(monomial, 0)
                   for monomial, coefficient in poly.items())

    require(all(pairing(row, dual_00010122) == 0 for row in rows),
            "four-coordinate exact dual stopped annihilating the master")
    require(pairing(targets["00010122"], dual_00010122) == 1,
            "four-coordinate exact dual stopped detecting the target")
    component_rows, component_monomials = components["00010122"]
    require((len(component_rows), len(component_monomials)) == (22, 69),
            "small R*X incidence component changed")
    component_rank = exact_rank((rows[index] for index in component_rows),
                                component_monomials)
    require(component_rank == 22, "small R*X exact rank changed")

    # Frozen exact redundant orbit.
    e_multiplier = EXT.multiply(EXT.shift(EXT.edge(4, 6), 24),
                                EXT.shift(EXT.edge(5, 7), 48))
    require(targets["00001212"] ==
            EXT.multiply(EXT.CORE.e_pair(0, 1), e_multiplier),
            "00001212 exact e-multiple identity changed")

    records = []
    for label in TARGETS:
        route = route_by_word[label]
        orbit = word_orbit(label, actions)
        require(route["orbit"] == EXPECTED_ORBITS[label]
                and route["literal_row_count"] == EXPECTED_SIZES[label]
                and orbit == frozenset(route["literal_source_labels"]),
                ("B4 x S3 transport changed", label, len(orbit)))
        majority, minors, majority_sites, minor_edges = factor_data(label)
        polynomial = targets[label]
        status = ("REDUNDANT_exact_e_multiple" if label == "00001212"
                  else "GENUINELY_NEW_degree4_source_orbit")
        witness = None
        if label in ("01010202", "00010212"):
            witness = {
                "kind": "isolated_monomial_coordinates",
                "target_monomials_absent_from_all_extended_master_rows": 3,
                "incidence_component_rows": 0,
                "incidence_component_monomials": 3,
            }
        elif label == "00010122":
            witness = {
                "kind": "exact_integer_dual",
                "incidence_component_rows": len(component_rows),
                "incidence_component_monomials": len(component_monomials),
                "component_exact_rank": component_rank,
                "dual_support": [
                    {"coefficient": coefficient,
                     "variables": [EXT.variable_name(index)
                                   for index in monomial]}
                    for monomial, coefficient in sorted(dual_00010122.items())
                ],
                "dual_pairs_with_target": 1,
                "dual_annihilates_all_extended_master_rows": len(rows),
            }
        records.append({
            "orbit": route["orbit"],
            "canonical_word": label,
            "B4_times_S3_orbit_size": len(orbit),
            "B4_times_S3_labels_sha256": route["labels_sha256"],
            "factor_formula": route["canonical_factor_formula"],
            "majority_colour": majority,
            "majority_four_set": list(majority_sites),
            "minor_colours": list(minors),
            "minor_edges": {str(colour): list(edge)
                            for colour, edge in minor_edges.items()},
            "expanded_terms": EXT.serialize(polynomial),
            "expanded_sha256": EXT.poly_sha(polynomial),
            "classification": status,
            "exact_nonmembership_witness": witness,
            "forced_cofactor_zero_antecedents": (
                [] if label == "00001212"
                else forced_cofactor_rows(label, master_labels)),
        })

    require(Counter(record["classification"] for record in records) == {
        "REDUNDANT_exact_e_multiple": 1,
        "GENUINELY_NEW_degree4_source_orbit": 3,
    }, "422 classification census changed")

    result = {
        "status": "PASS exact sparse four-orbit 422 extension theorem",
        "normalization": full440["normalization"],
        "extended_master": {
            "degree_at_most_four_rows": len(rows),
            "includes_full_440": True,
            "full_440_source_labels_sha256": file_sha(FULL440_LABELS),
            "full_440_logical_sha256": full440["logical_sha256"],
        },
        "orbit_records": records,
        "classification_summary": {
            "redundant_orbits": 1,
            "redundant_rows": EXPECTED_SIZES["00001212"],
            "genuinely_new_orbits": 3,
            "genuinely_new_rows": sum(EXPECTED_SIZES[label] for label in
                                        ("01010202", "00010212", "00010122")),
            "new_canonical_words": [
                "01010202", "00010212", "00010122"],
        },
        "support_and_mate_routing": {
            "exact_antecedent": (
                "If Q_c[S]*X_d[T]*X_e[U] is live, four literal master "
                "X*C rows force C_c[T]=C_c[U]=C_e[T]=C_d[U]=0."),
            "support6_certificate_result_sha256": support6["result_sha256"],
            "support8_certificate_result_sha256": support8["result_sha256"],
            "verdict": (
                "A later exact full (X,C,Q,H) match to support6 or the "
                "one-y support8 orbit is terminal by its fixed-left mate "
                "unit. The four-factor antecedent itself does not force "
                "either full signature, so no unconditional existing-unit "
                "route is claimed for the three new source orbits."),
            "remaining_antichain": [
                "01010202", "00010212", "00010122"],
        },
        "B4_times_S3_transport": {
            "B4_order": len(actions),
            "colour_group_order": 6,
            "direct_product_order": len(actions)*6,
            "all_exported_orbits_replayed_literally": True,
        },
        "scope": (
            "The three nonmembership results are exact over Z/Q for the "
            "degree-at-most-four extended-master source span. They prove "
            "that the rows must be added to this source packet; they are "
            "not unrestricted ideal/radical nonmembership claims."),
        "mutation_guards": {
            "old_four_unresolved_422_orbits": True,
            "drop_full_440_before_422_test": True,
            "replace_exact_Q_dual_by_two_prime_only": True,
            "infer_support6_or_support8_from_partial_antecedent": True,
        },
        "source_hashes": {
            str(path.relative_to(ROOT)): file_sha(path)
            for path in (ROUTING, FULL440, FULL440_LABELS,
                         SUPPORT6_CERT, SUPPORT8_CERT)
        },
    }
    result["logical_sha256"] = logical_sha(result)
    text = json.dumps(result, indent=2, sort_keys=True)+"\n"
    if "--write-results" in sys.argv:
        OUT.write_text(text)
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
