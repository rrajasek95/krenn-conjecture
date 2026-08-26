#!/usr/bin/env python3
"""Exact bounded audit of the 34-column chart-26 degree-eight antichain.

This checker starts after the frozen 146-row first-boundary repair.  It
replays the complete degree-five source exchange incidence, classifies the
34 columns outside that layer, tests degree-six 4--4/4--5/5--5 source legs,
and constructs a finite correction packet for the 34-column complement.

The final correction is local to this complement.  It does not contract the
other 218 second-boundary columns and is not a degree-eight saturation proof.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import importlib.util
import json
import sys
from fractions import Fraction
from itertools import combinations
from pathlib import Path
from time import monotonic

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROLONG = ROOT / "computations/unaudited-codex-n8-degree8-dual-prolongation-2026-08-23/audit_degree8_dual_prolongation.py"
EXTEND = ROOT / "computations/unaudited-codex-n8-normalized-dfs-degree7-2026-08-23/audit_degree8_dual_extension.py"
WEIGHTED = ROOT / "computations/verify_n8_chart26_weighted_degree6_census.py"
OUT = HERE / "results_degree8_antichain_cells.json"
Q = Fraction

ANTICHAIN = (
    ("00000002", "2a6f7eb5"),
    ("00000011", "0788e3f2"),
    ("00000012", "072775a5"), ("00000012", "0775d8e1"),
    ("00002002", "0521b9f0"), ("00002011", "07617eec"),
    ("00002012", "0708d9ef"), ("00002022", "0708d0f2"),
    ("00002102", "0773d0ea"), ("00012101", "055086ea"),
    ("01000000", "2a6e7eb5"),
    ("01000010", "0e4950d5"), ("01000010", "2a6375da"),
    ("01000010", "335a75da"), ("01010010", "0e334abf"),
    ("11000011", "345e9ea6"), ("11000212", "345d95a6"),
    ("11010011", "345d88bf"), ("11012111", "0d4fd2ea"),
    ("11111112", "345d7ebe"),
    ("12000000", "0949dee1"), ("12000000", "88a7eaf4"),
    ("12000002", "1d2240c0"),
    ("12002000", "0949d8e1"), ("12002000", "0951b7ea"),
    ("12011000", "0d4ccdf7"), ("12011010", "0c4c8ad5"),
    ("12012000", "0e4cbaf6"), ("12012111", "0d4cd2ea"),
    ("12111000", "7e80b4ea"), ("12111000", "8084babd"),
    ("12111100", "808dc3f4"),
    ("12111220", "8084abba"), ("12111220", "808dc4e4"),
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def fraction_record(value):
    value = Q(value)
    return [value.numerator, value.denominator]


def histogram(values):
    counter = collections.Counter(values)
    return {str(key): value for key, value in sorted(counter.items(), key=lambda x: str(x[0]))}


def column_record(A, M, column):
    return {
        "word": A.word_label(M, column[0]),
        "word_code": column[0],
        "profile": list(A.word_profile(M, column[0])),
        "multiplier": column[1].hex(),
    }


def decode_columns(M):
    return {
        (M.D5.word_code(tuple(map(int, label))), bytes.fromhex(multiplier))
        for label, multiplier in ANTICHAIN
    }


def exact_extended_functional(A, M):
    target, dual, _rounds = A.reconstruct_dual(M)
    cache = {}
    new_columns = {
        column for column in M.bounded_incident_columns(dual, 8)
        if len(column[1]) == 4
    }
    frequency = collections.Counter(
        row for column in new_columns
        for row in A.column_entries(M, column, cache) if len(row) == 8
    )
    extension = {}
    for column in sorted(new_columns):
        entries = A.column_entries(M, column, cache)
        value = A.pairing(dual, entries)
        if not value:
            continue
        private = min(row for row in entries
                      if len(row) == 8 and frequency[row] == 1)
        extension[private] = -value / entries[private]
    functional = dict(dual)
    functional.update(extension)
    repair_incident = M.bounded_incident_columns(extension, 8)
    candidates = repair_incident | new_columns
    crossings = {
        column for column in candidates
        if A.pairing(functional, A.column_entries(M, column, cache))
    }
    require(len(crossings) == 252, "second-boundary census changed")
    require(A.pairing(functional, target) == -1 and functional.get(b"") == 1,
            "normalized pure-target residual pairing changed")
    return target, functional, crossings, cache


def lower_indices(W):
    originals, degree4, code_to_lead, degree5, words = W.build_leads()
    d4_core3 = collections.defaultdict(set)
    d4_core2 = collections.defaultdict(set)
    for lead in degree4:
        for core in combinations(lead, 3):
            d4_core3[bytes(core)].add(lead)
        for core in combinations(lead, 2):
            d4_core2[bytes(core)].add(lead)
    d5_core3 = collections.defaultdict(set)
    d5_core4 = collections.defaultdict(set)
    d5_by_source = collections.defaultdict(list)
    for lead, (left, right, _distance) in degree5.items():
        for core in combinations(lead, 3):
            d5_core3[bytes(core)].add(lead)
        for core in combinations(lead, 4):
            d5_core4[bytes(core)].add(lead)
        source_lcm = W.monomial_lcm(code_to_lead[left], code_to_lead[right])
        d5_by_source[left].append((lead, W.FIRST.quotient(source_lcm, code_to_lead[left])))
        d5_by_source[right].append((lead, W.FIRST.quotient(source_lcm, code_to_lead[right])))
    return {
        "originals": originals,
        "degree4": degree4,
        "code_to_lead": code_to_lead,
        "degree5": degree5,
        "words": words,
        "d4_core3": d4_core3,
        "d4_core2": d4_core2,
        "d5_core3": d5_core3,
        "d5_core4": d5_core4,
        "d5_by_source": d5_by_source,
    }


def cell_incidence(A, M, W, indices, column, kind):
    """Return literal translated source-leg witnesses of the requested kind."""
    code_to_lead = indices["code_to_lead"]
    witnesses = set()
    for actual_code, multiplier in M.normalized_column_orbit(column):
        lead = code_to_lead[actual_code]
        if kind == "d5":
            for core in combinations(lead, 3):
                for other in indices["d4_core3"][bytes(core)]:
                    if other == lead or len(set(lead) & set(other)) != 3:
                        continue
                    lcm = W.monomial_lcm(lead, other)
                    quotient = W.FIRST.quotient(lcm, lead)
                    translate = W.FIRST.quotient(multiplier, quotient)
                    if translate is not None and len(translate) == 3:
                        witnesses.add((actual_code, indices["degree4"][other], translate))
        elif kind == "44":
            for core in combinations(lead, 2):
                for other in indices["d4_core2"][bytes(core)]:
                    if other == lead or len(set(lead) & set(other)) != 2:
                        continue
                    lcm = W.monomial_lcm(lead, other)
                    quotient = W.FIRST.quotient(lcm, lead)
                    translate = W.FIRST.quotient(multiplier, quotient)
                    if translate is not None and len(translate) == 2:
                        witnesses.add((actual_code, indices["degree4"][other], translate))
        elif kind == "45":
            for core in combinations(lead, 3):
                for other in indices["d5_core3"][bytes(core)]:
                    if len(set(lead) & set(other)) != 3:
                        continue
                    lcm = W.monomial_lcm(lead, other)
                    quotient = W.FIRST.quotient(lcm, lead)
                    translate = W.FIRST.quotient(multiplier, quotient)
                    if translate is not None and len(translate) == 2:
                        witnesses.add((actual_code, other, translate))
        elif kind == "55":
            for first5, inner_multiplier in indices["d5_by_source"][actual_code]:
                for core in combinations(first5, 4):
                    for second5 in indices["d5_core4"][bytes(core)]:
                        if second5 == first5 or len(set(first5) & set(second5)) != 4:
                            continue
                        outer_lcm = W.monomial_lcm(first5, second5)
                        outer_multiplier = W.FIRST.quotient(outer_lcm, first5)
                        required = W.FIRST.multiply(inner_multiplier, outer_multiplier)
                        translate = W.FIRST.quotient(multiplier, required)
                        if translate is not None and len(translate) == 2:
                            witnesses.add((actual_code, first5, second5, translate))
        else:
            raise ValueError(kind)
    return witnesses


def provenance_record(A, M, W, indices, column, coverage):
    multiplier = column[1]
    lead = indices["code_to_lead"][column[0]]
    top = W.FIRST.multiply(multiplier, lead)
    return {
        **column_record(A, M, column),
        "multiplier_skeleton": W.skeleton_type(multiplier),
        "top_skeleton": W.skeleton_type(top),
        "repeated_multiplier_coordinates": W.repeated_coordinates(multiplier),
        "repeated_top_coordinates": W.repeated_coordinates(top),
        "degree5_cell_legs": coverage["d5"],
        "degree6_44_legs": coverage["44"],
        "degree6_45_legs": coverage["45"],
        "degree6_55_legs": coverage["55"],
    }


def private_leaf_packet(A, M, antichain, functional, cache):
    records = []
    hard = set()
    correction = {}
    for column in sorted(antichain):
        entries = A.column_entries(M, column, cache)
        private = []
        for row in entries:
            if len(row) != 8:
                continue
            incident = M.bounded_incident_columns({row: Q(1)}, 8)
            if incident == {column}:
                private.append(row)
        if not private:
            hard.add(column)
            continue
        chosen = min(private)
        value = A.pairing(functional, entries)
        weight = -value / entries[chosen]
        correction[chosen] = weight
        records.append({
            **column_record(A, M, column),
            "global_private_rows": len(private),
            "chosen_row": chosen.hex(),
            "column_coefficient": entries[chosen],
            "repair_weight": fraction_record(weight),
        })
    require(len(records) == 23 and len(hard) == 11,
            "23-leaf/11-hard split changed")
    for row in correction:
        require(len(M.bounded_incident_columns({row: Q(1)}, 8)) == 1,
                "selected leaf stopped being globally private")
    return correction, hard, records


def hard_cell_closure(A, D, M, hard, functional, cache, started):
    rows = {
        row for column in hard
        for row in A.column_entries(M, column, cache) if len(row) == 8
    }
    require(len(rows) == 677, "hard seed row census changed")
    rounds = []
    final_solution = None
    final_columns = None
    for iteration in range(5):
        columns = set()
        row_incidence = {}
        for row in rows:
            incident = M.bounded_incident_columns({row: Q(1)}, 8)
            row_incidence[row] = incident
            columns.update(incident)
        columns = tuple(sorted(columns))
        column_index = {column: index for index, column in enumerate(columns)}
        row_list = tuple(sorted(rows))
        row_vectors = []
        for row in row_list:
            vector = {}
            for column in row_incidence[row]:
                coefficient = A.column_entries(M, column, cache).get(row, 0)
                if coefficient:
                    vector[column_index[column]] = coefficient
            row_vectors.append(vector)
        target = {
            index: -A.pairing(functional, A.column_entries(M, column, cache))
            for index, column in enumerate(columns)
        }
        target = {index: value for index, value in target.items() if value}
        modular_rank, modular_remainder = D.modular_relative_rank(row_vectors, target)
        rank, solution, remainder, separator = D.exact_relative_solve(
            row_list, row_vectors, target, started
        )
        require(rank == modular_rank, "exact/modular hard-cell ranks differ")
        record = {
            "round": iteration,
            "rows": len(rows),
            "columns": len(columns),
            "rank": rank,
            "target_columns": len(target),
            "modular_remainder_terms": len(modular_remainder),
            "exact_remainder_terms": len(remainder),
        }
        if solution:
            for index, column in enumerate(columns):
                value = A.pairing(functional, A.column_entries(M, column, cache))
                value += sum(solution.get(row, Q(0)) * vector.get(index, 0)
                             for row, vector in zip(row_list, row_vectors))
                require(not value, "terminal hard-cell correction misses a column")
            record.update({
                "status": "SOLVED",
                "solution_rows": len(solution),
                "solution_coefficient_histogram": histogram(solution.values()),
            })
            rounds.append(record)
            final_solution = solution
            final_columns = columns
            break
        require(separator and remainder, "hard closure returned no result")
        target_pairing = sum(target.get(index, Q(0)) * value
                             for index, value in separator.items())
        require(target_pairing, "hard-cell separator lost target pairing")
        residual = collections.defaultdict(Q)
        for index, value in separator.items():
            for row, coefficient in A.column_entries(M, columns[index], cache).items():
                residual[row] += value * coefficient
        residual = {row: value for row, value in residual.items() if value}
        require(all(not residual.get(row) for row in rows),
                "hard-cell residual does not vanish on current rows")
        new_top = {row for row in residual if len(row) == 8} - rows
        require(new_top, "hard-cell separator produced no new top row")

        # On the rows already admitted, every displayed separator is a
        # literal gain-graph coboundary: each active row meets exactly two
        # separator columns, and the separator coefficients give a nonzero
        # vertex potential.  This proves the biased-graph theta axiom for
        # these induced graphs, but says nothing about the exterior residual.
        active_edges = []
        adjacency = {index: set() for index in separator}
        entry_coefficients = []
        for row, vector in zip(row_list, row_vectors):
            hits = [(index, vector[index]) for index in separator if index in vector]
            if not hits:
                continue
            require(len(hits) == 2,
                    "hard separator ceased to be a two-incidence gain graph")
            (left, left_coefficient), (right, right_coefficient) = hits
            require(left_coefficient * separator[left]
                    + right_coefficient * separator[right] == 0,
                    "separator potential does not satisfy a gain edge")
            adjacency[left].add(right)
            adjacency[right].add(left)
            entry_coefficients.extend((left_coefficient, right_coefficient))
            active_edges.append(row)
        unseen = set(adjacency)
        components = 0
        while unseen:
            components += 1
            frontier = [unseen.pop()]
            while frontier:
                vertex = frontier.pop()
                for neighbor in adjacency[vertex]:
                    if neighbor in unseen:
                        unseen.remove(neighbor)
                        frontier.append(neighbor)
        cycle_rank = len(active_edges) - len(separator) + components
        record.update({
            "status": "OBSTRUCTED",
            "separator_support": len(separator),
            "separator_target_pairing": fraction_record(target_pairing),
            "separator": [
                {**column_record(A, M, columns[index]),
                 "coefficient": fraction_record(value)}
                for index, value in sorted(separator.items())
            ],
            "residual_support": len(residual),
            "residual_degree_histogram": histogram(map(len, residual)),
            "new_top_rows": len(new_top),
            "residual_sha256": hashlib.sha256(json.dumps(
                [[row.hex(), *fraction_record(value)]
                 for row, value in sorted(residual.items())],
                separators=(",", ":")
            ).encode()).hexdigest(),
            "gain_graph": {
                "vertices": len(separator),
                "edges": len(active_edges),
                "components": components,
                "cycle_rank": cycle_rank,
                "entry_coefficient_histogram": histogram(entry_coefficients),
                "all_edge_gains_are_separator_coboundaries": True,
                "balanced_cycle_theta_axiom": True,
            },
        })
        rounds.append(record)
        rows.update(new_top)
    require(final_solution is not None, "five-round hard-cell gate did not solve")
    return rounds, final_solution, final_columns


def run(mutate=False):
    started = monotonic()
    A = load("degree8_prolong", PROLONG)
    D = load("degree8_extend", EXTEND)
    W = load("weighted_degree6", WEIGHTED)
    M = A.load_checker()
    target, functional, crossings, cache = exact_extended_functional(A, M)
    antichain = decode_columns(M)
    require(len(antichain) == 34 and antichain <= crossings,
            "literal 34-column antichain changed")
    indices = lower_indices(W)

    d5_coverage = {}
    for column in crossings:
        d5_coverage[column] = cell_incidence(A, M, W, indices, column, "d5")
    residual = {column for column in crossings if not d5_coverage[column]}
    require(residual == antichain, "complete degree-five complement changed")

    coverage = {}
    remaining = set(antichain)
    for column in sorted(antichain):
        coverage[column] = {
            "d5": len(d5_coverage[column]),
            "44": len(cell_incidence(A, M, W, indices, column, "44")),
            "45": 0,
            "55": 0,
        }
    touched44 = {column for column in remaining if coverage[column]["44"]}
    remaining -= touched44
    for column in sorted(remaining):
        coverage[column]["45"] = len(cell_incidence(A, M, W, indices, column, "45"))
    touched45 = {column for column in remaining if coverage[column]["45"]}
    remaining -= touched45
    for column in sorted(remaining):
        coverage[column]["55"] = len(cell_incidence(A, M, W, indices, column, "55"))
    touched55 = {column for column in remaining if coverage[column]["55"]}
    remaining -= touched55

    require((len(touched44), sum(coverage[c]["44"] for c in touched44)) == (21, 31),
            "degree-six 4--4 coverage changed")
    require((len(touched45), sum(coverage[c]["45"] for c in touched45)) == (8, 10),
            "degree-six 4--5 coverage changed")
    require(not touched55 and len(remaining) == 5,
            "degree-six 5--5 residual changed")

    leaf_correction, hard, leaf_records = private_leaf_packet(
        A, M, antichain, functional, cache
    )
    functional_after_leaves = dict(functional)
    for row, value in leaf_correction.items():
        functional_after_leaves[row] = functional_after_leaves.get(row, Q(0)) + value
        if not functional_after_leaves[row]:
            functional_after_leaves.pop(row)
    rounds, hard_correction, hard_columns = hard_cell_closure(
        A, D, M, hard, functional_after_leaves, cache, started
    )

    combined = dict(functional_after_leaves)
    for row, value in hard_correction.items():
        combined[row] = combined.get(row, Q(0)) + value
        if not combined[row]:
            combined.pop(row)
    check_columns = set(hard_columns)
    for row in leaf_correction:
        check_columns.update(M.bounded_incident_columns({row: Q(1)}, 8))
    require(antichain <= check_columns, "correction packet lost an antichain column")
    require(all(not A.pairing(combined, A.column_entries(M, column, cache))
                for column in check_columns),
            "combined 34-column packet is not an exact correction")

    if mutate:
        require(len(remaining) == 4, "hostile residual-count mutation survived")

    provenance = [
        provenance_record(A, M, W, indices, column, coverage[column])
        for column in sorted(antichain)
    ]
    result = {
        "verdict": "PASS_EXACT_34_COLUMN_LOCAL_CORRECTION",
        "scope": (
            "normalized chart-26 degree-eight second-boundary complement after "
            "complete degree-five source-cell incidence; not a contraction of "
            "the other 218 columns and not a t^8 saturation decision"
        ),
        "frozen_input": {
            "second_boundary_columns": len(crossings),
            "complete_degree5_touched": len(crossings) - len(antichain),
            "degree5_complement": len(antichain),
            "normalized_full_source_residual_rows": len(target),
            "normalized_residual_pairing": fraction_record(A.pairing(functional, target)),
            "constant_pairing": fraction_record(functional.get(b"", 0)),
        },
        "degree6_source_leg_census": {
            "degree4_degree4_touched": len(touched44),
            "degree4_degree4_incidences": sum(coverage[c]["44"] for c in touched44),
            "degree4_degree5_newly_touched": len(touched45),
            "degree4_degree5_incidences": sum(coverage[c]["45"] for c in touched45),
            "degree5_degree5_newly_touched": len(touched55),
            "degree6_untouched": len(remaining),
            "degree6_untouched_columns": [column_record(A, M, c) for c in sorted(remaining)],
            "guard": "touch is source-leg incidence, not by itself an exact correction",
        },
        "provenance_ledger": provenance,
        "global_private_leaf_packet": {
            "leaf_columns": len(leaf_records),
            "hard_columns": len(hard),
            "records": leaf_records,
            "exact_guard": "each chosen row has exactly one incident degree-eight column globally",
        },
        "hard11_exchange_closure": {
            "hard_columns": [column_record(A, M, c) for c in sorted(hard)],
            "rounds": rounds,
            "terminal_solution": [
                [row.hex(), *fraction_record(value)]
                for row, value in sorted(hard_correction.items())
            ],
            "terminal_columns": len(hard_columns),
            "terminal_solution_rows": len(hard_correction),
        },
        "local_correction_theorem": {
            "leaf_rows": len(leaf_correction),
            "hard_solution_rows": len(hard_correction),
            "checked_incident_columns": len(check_columns),
            "all_checked_columns_annihilated": True,
            "orbit_completion": (
                "columns and rows are canonical support-stabilizer invariants; "
                "normalized column-orbit expansion is used in every coefficient"
            ),
            "conceptual_form": (
                "23 global leaves plus four successive small exchange/Bockstein "
                f"residual cells (supports 4,4,5,22), ending in a "
                f"{len(hard_correction)}-row exact solve"
            ),
            "target_relevance": (
                "each displayed separator pairs nontrivially with the current "
                "degree-eight boundary of the exact normalized residual from "
                "the full-source degree-five pure-product lift"
            ),
            "gain_graph_scope": (
                "the four induced admitted-row graphs are exact coboundary gain "
                "graphs, so their balanced cycles obey theta; this does not give "
                "a universal NBC straightening law because exterior residual rows "
                "create the next graph and two early graphs are trees"
            ),
        },
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = hashlib.sha256(logical.encode()).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    parser.add_argument("--mutate", action="store_true")
    args = parser.parse_args()
    result = run(args.mutate)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_results:
        OUT.write_text(rendered, encoding="utf-8")
    if args.check_results:
        require(OUT.read_text(encoding="utf-8") == rendered,
                "frozen antichain result changed")
    print(json.dumps({
        "verdict": result["verdict"],
        "degree6_untouched": result["degree6_source_leg_census"]["degree6_untouched"],
        "hard_rounds": len(result["hard11_exchange_closure"]["rounds"]),
        "logical_sha256": result["logical_sha256"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
