#!/usr/bin/env python3
"""Generate and replay named Laurent certificates for nontriangle |F|<=3.

Each stored refinement names exact coefficient fibres.  Replay independently
checks either a translated-zero cover, an integral binomial-lattice reduction
of one fibre, or the special translated-trinomial contradiction.  It then
reconstructs a canonical CNF, verifies its SHA-256 digest, and confirms UNSAT
with CaDiCaL 1.9.5 and Kissat 4.0.4.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp
from pysat.solvers import Solver

import search_f5_support_sat as base
import verify_f3_toric_obstruction as laurent
import verify_f4_support_obstruction as transfers


def require(condition, message):
    """Check a load-bearing condition in a way ``python3 -O`` cannot remove."""

    if not condition:
        raise RuntimeError(message)


SCHEMA = "low-rank-graph-laurent-v1"
DEFAULT_CERTIFICATE = Path("computations/low_rank_graph_laurent_certificate.json")
CASES = {
    "3P2": base.THREE_EDGE_GRAPHS["3P2"],
    "P3+P2+P1": base.THREE_EDGE_GRAPHS["P3+P2+P1"],
    "P4+2P1": base.THREE_EDGE_GRAPHS["P4+2P1"],
    "2P2+2P1": laurent.LOWER_EDGE_GRAPHS["2P2+2P1"],
    "P3+3P1": laurent.LOWER_EDGE_GRAPHS["P3+3P1"],
    "P2+4P1": laurent.LOWER_EDGE_GRAPHS["P2+4P1"],
    "6P1": laurent.LOWER_EDGE_GRAPHS["6P1"],
}


def dimacs_bytes(variables, clauses):
    lines = [f"p cnf {variables} {len(clauses)}\n"]
    lines.extend(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    return "".join(lines).encode()


def parse_fiber(raw):
    word = tuple(raw[0])
    supported = tuple(raw[1])
    require(
        len(word) == 6 and all(colour in base.COLORS for colour in word),
        f"fiber word {word} is not a six-site colouring",
    )
    require(
        supported == tuple(sorted(supported)) and supported,
        f"fiber {word} has an unsorted or empty support {supported}",
    )
    require(
        len(set(supported)) == len(supported),
        f"fiber {word} repeats a matching index",
    )
    require(
        all(0 <= index < len(base.MATCHINGS) for index in supported),
        f"fiber {word} names a matching outside 0..{len(base.MATCHINGS) - 1}",
    )
    return word, supported


def difference(first, second):
    return tuple(a - b for a, b in zip(first, second, strict=True))


def integer_coordinates(rows, target):
    """Return the unique integral row coordinates, or ``None``.

    Certificate records contain subsets of the independent relation basis
    actually used in a contradiction.  Therefore rational coordinates are
    unique; accepting them only when every denominator is one is a direct
    integer-combination check and needs no saturation inference.
    """
    if not rows:
        return () if not any(target) else None
    matrix = sp.Matrix(rows)
    _rref, columns = matrix.rref()
    columns = tuple(columns)
    # The pivot columns count the rank, so this is the row-independence check
    # that makes the rational coordinates below unique.
    require(
        len(columns) == len(rows),
        f"relation rows are dependent: rank {len(columns)} < {len(rows)}",
    )
    minor = matrix[:, list(columns)]
    target_row = sp.Matrix(1, len(target), target)
    coordinates = target_row[:, list(columns)] * minor.inv()
    if coordinates * matrix != target_row:
        return None
    if any(value.q != 1 for value in coordinates):
        return None
    return tuple(int(value) for value in coordinates)


def relation(signatures, word, supported):
    # A binomial relation x^a = -x^b comes from a *zero* two-term fiber, so
    # its coloring has to be mixed.
    require(len(set(word)) > 1, f"binomial fiber {word} is a constant coloring")
    require(len(supported) == 2, f"fiber {word} has {len(supported)} terms, not 2")
    first, second = supported
    return difference(signatures[word, first], signatures[word, second])


def audit_transfer(record, pool, signatures):
    require(record["kind"] == "transfer", f"not a transfer: {record['kind']}")
    target_word, target_terms = parse_fiber(record["target"])
    target_kind = record["target_kind"]
    require(
        (len(set(target_word)) == 1) == (target_kind == "constant"),
        f"transfer target {target_word} disagrees with kind {target_kind}",
    )
    if target_kind != "constant":
        require(
            target_kind == "mixed" and len(set(target_word)) > 1,
            f"transfer target {target_word} is not a mixed fiber",
        )
    leftover = tuple(record["leftover"])
    require(
        len(leftover) == (0 if target_kind == "constant" else 1),
        f"transfer leftover {leftover} is wrong for a {target_kind} target",
    )
    require(
        set(leftover) <= set(target_terms),
        f"transfer leftover {leftover} is not inside the target support",
    )

    covered = []
    source_fibers = []
    for raw_source, raw_subset in record["sources"]:
        source_word, source_terms = parse_fiber(raw_source)
        subset = tuple(raw_subset)
        require(
            len(set(source_word)) > 1,
            f"transfer source {source_word} is a constant coloring",
        )
        require(
            subset == tuple(
                index for index in target_terms if index in set(subset)
            ),
            f"transfer subset {subset} is not an ordered part of the target",
        )
        require(
            len(subset) == len(source_terms) and len(subset) >= 2,
            f"transfer subset {subset} does not match source {source_terms}",
        )
        target_vectors = [signatures[target_word, index] for index in subset]
        source_vectors = [signatures[source_word, index] for index in source_terms]
        require(
            transfers.translated_shape(target_vectors)
            == transfers.translated_shape(source_vectors),
            f"source {source_word} is not a translate of the target block",
        )
        covered.extend(subset)
        source_fibers.append((source_word, source_terms))
    require(
        len(covered) == len(set(covered)),
        "the transfer sources are not pairwise disjoint",
    )
    require(
        set(covered) | set(leftover) == set(target_terms),
        "the transfer sources plus leftover do not cover the target",
    )
    require(
        not (set(covered) & set(leftover)),
        "a transfer source overlaps the leftover term",
    )

    clause = transfers.exact_support_block(pool, target_word, set(target_terms))
    for source_word, source_terms in source_fibers:
        clause.extend(transfers.exact_support_block(pool, source_word, set(source_terms)))
    return clause


def named_fibers(record):
    parsed = [parse_fiber(raw) for raw in record["fibers"]]
    require(
        len({word for word, _supported in parsed}) == len(parsed),
        "a record names the same colouring twice",
    )
    return dict(parsed)


def audit_single_fiber(record, signatures):
    require(
        record["kind"] == "single_fiber", f"not a single fiber: {record['kind']}"
    )
    fibers = named_fibers(record)
    target = tuple(record["target"])
    require(target in fibers, f"target {target} is not among the named fibers")
    target_terms = fibers[target]
    # Both conflicts below need the target coefficient to be *zero*.  That is
    # exactly what a mixed coloring supplies; a constant coloring has target
    # coefficient one and neither argument survives.
    require(
        len(set(target)) > 1,
        f"single-fiber target {target} is a constant coloring",
    )
    kind = record["conflict_kind"]

    if kind == "odd-binomial":
        require(
            len(target_terms) == 2,
            f"odd-binomial target {target} has {len(target_terms)} terms",
        )
        basis_fibers = [(word, terms) for word, terms in fibers.items() if word != target]
        rows = [relation(signatures, word, terms) for word, terms in basis_fibers]
        coordinates = integer_coordinates(rows, relation(signatures, target, target_terms))
        require(
            coordinates is not None,
            f"target {target} is not an integer combination of the basis",
        )
        # Every named binomial has character -1.  The target character must
        # disagree with the value predicted from the basis equations.
        require(
            (-1 if sum(coordinates) % 2 else 1) != -1,
            f"target {target} has the character its basis predicts",
        )
        return

    require(
        kind == "single-laurent-class", f"unknown conflict kind {kind}"
    )
    require(
        len(target_terms) >= 3,
        f"single-laurent-class target {target} has {len(target_terms)} terms",
    )
    basis_fibers = [(word, terms) for word, terms in fibers.items() if word != target]
    rows = [relation(signatures, word, terms) for word, terms in basis_fibers]
    exponents = [signatures[target, index] for index in target_terms]
    classes = []
    class_sums = []
    for exponent in exponents:
        for class_index, representative in enumerate(classes):
            coordinates = integer_coordinates(rows, difference(exponent, representative))
            if coordinates is not None:
                class_sums[class_index] += -1 if sum(coordinates) % 2 else 1
                break
        else:
            classes.append(exponent)
            class_sums.append(1)
    require(
        all(isinstance(value, int) for value in class_sums),
        f"non-integer class sums {class_sums}",
    )
    require(
        len([value for value in class_sums if value]) == 1,
        f"target {target} has class sums {class_sums}, not one live class",
    )


def audit_translated_trinomial(record, signatures):
    require(
        record["kind"] == "translated_trinomial",
        f"not a translated trinomial: {record['kind']}",
    )
    fibers = named_fibers(record)
    first = tuple(record["first"])
    second = tuple(record["second"])
    require(
        first != second and len(fibers[first]) == len(fibers[second]) == 3,
        f"{first} and {second} are not two distinct trinomial fibers",
    )
    # Both trinomials must be zero fibers, so both colorings must be mixed.
    for word in (first, second):
        require(
            len(set(word)) > 1,
            f"translated-trinomial fiber {word} is a constant coloring",
        )
    basis_fibers = [
        (word, terms)
        for word, terms in fibers.items()
        if word not in (first, second)
    ]
    rows = [relation(signatures, word, terms) for word, terms in basis_fibers]
    first_terms = fibers[first]
    second_terms = fibers[second]
    first_exponents = [signatures[first, index] for index in first_terms]
    expected_parities = tuple(record["parities"])
    require(
        len(expected_parities) == 2 and any(expected_parities),
        f"recorded parities {expected_parities} carry no sign change",
    )

    found = False
    for permutation in itertools.permutations(range(3)):
        second_exponents = [
            signatures[second, second_terms[index]] for index in permutation
        ]
        parities = []
        for position in (1, 2):
            first_relative = difference(first_exponents[position], first_exponents[0])
            second_relative = difference(second_exponents[position], second_exponents[0])
            coordinates = integer_coordinates(rows, difference(first_relative, second_relative))
            if coordinates is None:
                break
            parities.append(int(sum(coordinates) % 2 != 0))
        if len(parities) == 2 and tuple(parities) == expected_parities:
            found = True
            break
    require(
        found,
        f"no matching of {first} onto {second} reproduces {expected_parities}",
    )


class NullSolver:
    def add_clause(self, _clause):
        pass


def add_named_fiber_block(clauses, pool, cache, fibers):
    indicators = []
    for word, supported in sorted(fibers.items()):
        key = (word, supported)
        if key not in cache:
            indicator = pool.id(("exact_fiber", word, supported))
            cache[key] = indicator
            pattern = [
                pool.id(("monomial", word, index))
                if index in supported
                else -pool.id(("monomial", word, index))
                for index in range(len(base.MATCHINGS))
            ]
            clauses.extend([[-indicator, literal] for literal in pattern])
            clauses.append([indicator] + [-literal for literal in pattern])
        indicators.append(cache[key])
    clauses.append(sorted(-indicator for indicator in indicators))


def build_case(name, records):
    exceptional = set(CASES[name])
    formula, pool, active = base.support_formula(exceptional)
    laurent.add_minor_witnesses(formula, pool, exceptional, active)
    automorphisms = laurent.graph_automorphisms(exceptional)
    comparisons = laurent.add_support_lex_leaders(
        formula, pool, exceptional, automorphisms
    )
    clauses = [list(clause) for clause in formula.clauses]
    base_clauses = list(clauses)
    signatures = transfers.formal_signatures(exceptional, pool)
    indicator_cache = {}

    for record in records:
        kind = record["kind"]
        if kind == "transfer":
            clauses.append(audit_transfer(record, pool, signatures))
            continue
        if kind == "single_fiber":
            audit_single_fiber(record, signatures)
        else:
            require(
                kind == "translated_trinomial", f"unknown record kind {kind}"
            )
            audit_translated_trinomial(record, signatures)
        add_named_fiber_block(clauses, pool, indicator_cache, named_fibers(record))
    return pool.top, comparisons, base_clauses, clauses


def solve_twice(clauses):
    for solver_name in ("cadical195", "kissat404"):
        with Solver(name=solver_name, bootstrap_with=clauses) as solver:
            require(not solver.solve(), f"{solver_name} found a model")


def generate_case(name):
    artifact = {}
    closed = laurent.audit_graph(
        name,
        CASES[name],
        solver_name="cadical195",
        use_symmetry_orbit=False,
        static_rebuild_interval=0,
        use_lex_leaders=True,
        artifact_sink=artifact,
        use_support_cuts=False,
    )
    require(closed, f"{name}: audit_graph did not close")
    counts = artifact["counts"]
    for unused in ("toric_rank_cuts", "odd_cuts", "generalized_cuts", "support_cuts"):
        require(counts[unused] == 0, f"{name}: {unused} is nonzero in {counts}")
    require(
        len(artifact["records"])
        == (
            counts["transfers"]
            + counts["single_fiber_cuts"]
            + counts["translated_trinomial_cuts"]
        ),
        f"{name}: {len(artifact['records'])} records do not match {counts}",
    )
    variables, comparisons, base_clauses, clauses = build_case(name, artifact["records"])
    solve_twice(clauses)
    return {
        "exceptional_edges": [list(edge) for edge in sorted(CASES[name])],
        "lex_comparisons": comparisons,
        "counts": counts,
        "variables": variables,
        "base_clauses": len(base_clauses),
        "augmented_clauses": len(clauses),
        "base_cnf_sha256": hashlib.sha256(dimacs_bytes(variables, base_clauses)).hexdigest(),
        "augmented_cnf_sha256": hashlib.sha256(dimacs_bytes(variables, clauses)).hexdigest(),
        "records": artifact["records"],
    }


def replay_case(name, payload):
    require(
        payload["exceptional_edges"]
        == [list(edge) for edge in sorted(CASES[name])],
        f"{name}: certificate names different exceptional edges",
    )
    variables, comparisons, base_clauses, clauses = build_case(name, payload["records"])
    require(
        comparisons == payload["lex_comparisons"],
        f"{name}: lex comparison count changed",
    )
    require(variables == payload["variables"], f"{name}: variable count changed")
    require(
        len(base_clauses) == payload["base_clauses"],
        f"{name}: base clause count changed",
    )
    require(
        len(clauses) == payload["augmented_clauses"],
        f"{name}: augmented clause count changed",
    )
    require(
        hashlib.sha256(dimacs_bytes(variables, base_clauses)).hexdigest()
        == payload["base_cnf_sha256"],
        f"{name}: base CNF digest mismatch",
    )
    require(
        hashlib.sha256(dimacs_bytes(variables, clauses)).hexdigest()
        == payload["augmented_cnf_sha256"],
        f"{name}: augmented CNF digest mismatch",
    )
    solve_twice(clauses)
    print(
        f"PASS {name}: {len(payload['records'])} named semantic records; "
        f"sha256={payload['augmented_cnf_sha256']}"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=DEFAULT_CERTIFICATE)
    parser.add_argument("--generate", action="store_true")
    parser.add_argument("--only", action="append", choices=tuple(CASES))
    parser.add_argument("--merge-from", type=Path, action="append")
    args = parser.parse_args()
    selected = tuple(dict.fromkeys(args.only or CASES))
    if args.merge_from:
        bundle = json.loads(args.certificate.read_text())
        require(bundle["schema"] == SCHEMA, "unexpected bundle schema")
        for source_path in args.merge_from:
            source = json.loads(source_path.read_text())
            require(source["schema"] == SCHEMA, "unexpected source schema")
            bundle["cases"].update(source["cases"])
        temporary = args.certificate.with_suffix(args.certificate.suffix + ".tmp")
        temporary.write_text(json.dumps(bundle, indent=2) + "\n")
        temporary.replace(args.certificate)
        print(f"merged {len(args.merge_from)} bundle(s) into {args.certificate}")
        return
    if args.generate:
        if args.certificate.exists():
            bundle = json.loads(args.certificate.read_text())
            require(bundle["schema"] == SCHEMA, "unexpected bundle schema")
        else:
            bundle = {"schema": SCHEMA, "cases": {}}
        for name in selected:
            bundle["cases"][name] = generate_case(name)
            temporary = args.certificate.with_suffix(args.certificate.suffix + ".tmp")
            temporary.write_text(json.dumps(bundle, indent=2) + "\n")
            temporary.replace(args.certificate)
            print(f"wrote {name} to {args.certificate}")
        return

    bundle = json.loads(args.certificate.read_text())
    require(bundle["schema"] == SCHEMA, "unexpected bundle schema")
    for name in selected:
        require(name in bundle["cases"], f"certificate missing case {name}")
        replay_case(name, bundle["cases"][name])


if __name__ == "__main__":
    main()
