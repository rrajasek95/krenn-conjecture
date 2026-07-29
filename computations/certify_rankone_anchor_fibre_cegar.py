#!/usr/bin/env python3
"""Record and replay the rank-one six-site fibre CEGAR calculation.

The companion search script is deliberately a discovery tool.  This driver
turns a terminating run into three independently inspectable objects:

* a JSON list of semantic nested/rectangle witnesses;
* the final augmented CNF in DIMACS format; and
* optionally, a DRUP trace from a proof-capable PySAT solver.

Replay does not trust the stored blocking clauses.  It reconstructs every
clause from the named fibres, checks the relevant perfect-matching and
Laurent-exponent identity, and then resolves the resulting CNF.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from pysat.solvers import Solver

import search_rankone_anchor_fibre_cegar as search


def word_text(word):
    return "".join(map(str, word))


def parse_word(value):
    word = tuple(map(int, value))
    assert len(word) == 6 and all(colour in range(3) for colour in word)
    return word


def exact_pattern_clause(compatible, patterns):
    """Negate the conjunction that all named fibres have exact supports."""
    clause = []
    for word, expected_terms in patterns.items():
        expected = set(expected_terms)
        clause.extend(
            -compatible[word, index] if index in expected
            else compatible[word, index]
            for index in range(len(search.MATCHINGS))
        )
    return clause


def encode_nested(witness):
    lower, pair, upper, triple = witness
    return {
        "kind": "nested",
        "lower_word": word_text(lower),
        "pair": list(pair),
        "upper_word": word_text(upper),
        "triple": list(triple),
    }


def encode_rectangle(witness):
    target, triple, pair, b_word, d_word, e_word = witness
    return {
        "kind": "rectangle",
        "target_word": word_text(target),
        "triple": list(triple),
        "pair": list(pair),
        "b_word": word_text(b_word),
        "d_word": word_text(d_word),
        "e_word": word_text(e_word),
    }


def decode_and_audit(record, compatible):
    """Check a semantic witness and return its logically valid block clause."""
    kind = record["kind"]
    if kind == "nested":
        lower = parse_word(record["lower_word"])
        upper = parse_word(record["upper_word"])
        pair = tuple(record["pair"])
        triple = tuple(record["triple"])
        assert len(pair) == 2 and len(set(pair)) == 2
        assert len(triple) == 3 and len(set(triple)) == 3
        assert set(pair) < set(triple)
        assert all(0 <= index < len(search.MATCHINGS)
                   for index in pair + triple)
        changed = {v for v in search.VERTICES if lower[v] != upper[v]}
        common = search.common_vertices(
            search.MATCHINGS[pair[0]], search.MATCHINGS[pair[1]]
        )
        assert changed <= common
        # This is the exact Laurent statement used in the handwritten proof:
        # the ratio of the pair's two monomials is unchanged.
        assert search.difference(lower, *pair) == search.difference(upper, *pair)
        patterns = {lower: pair, upper: triple}
        return exact_pattern_clause(compatible, patterns)

    assert kind == "rectangle"
    target = parse_word(record["target_word"])
    b_word = parse_word(record["b_word"])
    d_word = parse_word(record["d_word"])
    e_word = parse_word(record["e_word"])
    pair = tuple(record["pair"])
    triple = tuple(record["triple"])
    assert len(pair) == 2 and len(set(pair)) == 2
    assert len(triple) == 3 and len(set(triple)) == 3
    assert set(pair) < set(triple)
    assert all(0 <= index < len(search.MATCHINGS)
               for index in pair + triple)
    lhs = tuple(
        a + b for a, b in zip(
            search.difference(target, *pair),
            search.difference(e_word, *pair),
        )
    )
    rhs = tuple(
        a + b for a, b in zip(
            search.difference(b_word, *pair),
            search.difference(d_word, *pair),
        )
    )
    assert lhs == rhs
    patterns = {
        target: triple,
        b_word: pair,
        d_word: pair,
        e_word: pair,
    }
    # Repeated b/d/e words are harmless, but a target word cannot at once
    # have the exact triple and exact pair support.
    assert target not in (b_word, d_word, e_word)
    return exact_pattern_clause(compatible, patterns)


def dimacs_bytes(top, clauses):
    lines = [f"p cnf {top} {len(clauses)}\n"]
    lines.extend(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    return "".join(lines).encode()


def reduce_by_assumption_core(top, base_clauses, records, compatible, solver_name):
    """Discard refinements outside one solver-certified assumption core."""
    clauses = [decode_and_audit(record, compatible) for record in records]
    selectors = list(range(top + 1, top + 1 + len(clauses)))
    with Solver(name=solver_name, bootstrap_with=base_clauses) as solver:
        for selector, clause in zip(selectors, clauses):
            solver.add_clause(clause + [-selector])
        assert not solver.solve(assumptions=selectors)
        core = set(solver.get_core() or ())
    assert core
    reduced = [record for selector, record in zip(selectors, records)
               if selector in core]
    reduced_clauses = list(base_clauses)
    reduced_clauses.extend(
        decode_and_audit(record, compatible) for record in reduced
    )
    with Solver(name=solver_name,
                bootstrap_with=reduced_clauses) as solver:
        assert not solver.solve()
    print(
        f"assumption core: {len(records)} -> {len(reduced)} refinements",
        flush=True,
    )
    return reduced, reduced_clauses


def save_bundle(prefix, top, clauses, records, proof_solver=None):
    prefix = Path(prefix)
    cnf_data = dimacs_bytes(top, clauses)
    cnf_path = prefix.with_suffix(".cnf")
    json_path = prefix.with_suffix(".json")
    cnf_path.write_bytes(cnf_data)
    payload = {
        "variables": top,
        "clauses": len(clauses),
        "refinements": records,
        "cnf_sha256": hashlib.sha256(cnf_data).hexdigest(),
    }
    json_path.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"wrote {json_path} and {cnf_path}", flush=True)
    if proof_solver:
        with Solver(name=proof_solver, with_proof=True,
                    bootstrap_with=clauses) as solver:
            assert not solver.solve(), "proof solver unexpectedly found SAT"
            proof = solver.get_proof()
        assert proof is not None
        # Deletions are optional in DRUP.  Omitting them leaves a larger
        # active formula but preserves reverse-unit-propagation validity and
        # lets the repository's small deletion-free checker audit every line.
        proof = [line for line in proof if not line.startswith("d ")]
        proof_path = prefix.with_suffix(".drup")
        proof_path.write_text("\n".join(proof) + ("\n" if proof else ""))
        print(f"wrote {proof_path} ({len(proof)} proof lines)", flush=True)


def run(args):
    formula, incidence, compatible = search.build_formula()
    base_clauses = list(formula.clauses)
    records = []
    with Solver(name=args.search_solver,
                bootstrap_with=formula.clauses) as solver:
        for round_index in range(args.rounds):
            if not solver.solve():
                print(f"UNSAT after {round_index} refinements", flush=True)
                if not args.no_core:
                    records, clauses = reduce_by_assumption_core(
                        formula.top, base_clauses, records, compatible,
                        args.search_solver,
                    )
                else:
                    clauses = formula.clauses
                save_bundle(
                    args.prefix, formula.top, clauses, records,
                    args.proof_solver,
                )
                return 0
            fibres = search.supported_fibres(solver.get_model(), compatible)
            nested = search.nested_witness(fibres)
            rectangle = None if nested is not None else search.rectangle_witness(fibres)
            if nested is not None:
                record = encode_nested(nested)
            elif rectangle is not None:
                record = encode_rectangle(rectangle)
            else:
                print(f"SURVIVOR after {round_index} refinements", flush=True)
                search.show_support(solver.get_model(), incidence)
                return 2
            clause = decode_and_audit(record, compatible)
            solver.add_clause(clause)
            formula.clauses.append(clause)
            records.append(record)
            if round_index < 10 or (round_index + 1) % 100 == 0:
                print(f"refinement {round_index + 1}: {record['kind']}", flush=True)
        print(f"ROUND LIMIT {args.rounds}", flush=True)
        return 3


def replay(args):
    payload = json.loads(Path(args.replay).read_text())
    formula, _incidence, compatible = search.build_formula()
    for record in payload["refinements"]:
        formula.clauses.append(decode_and_audit(record, compatible))
    data = dimacs_bytes(formula.top, formula.clauses)
    assert formula.top == payload["variables"]
    assert len(formula.clauses) == payload["clauses"]
    assert hashlib.sha256(data).hexdigest() == payload["cnf_sha256"]
    with Solver(name=args.search_solver,
                bootstrap_with=formula.clauses) as solver:
        assert not solver.solve(), "replayed formula is not UNSAT"
    print(
        f"PASS: audited {len(payload['refinements'])} semantic refinements; "
        "hash and UNSAT replay agree",
        flush=True,
    )
    if args.proof_solver:
        prefix = Path(args.replay).with_suffix("")
        save_bundle(prefix, formula.top, formula.clauses,
                    payload["refinements"], args.proof_solver)
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rounds", type=int, default=10000)
    parser.add_argument("--prefix", default="computations/rankone_anchor_fibre")
    parser.add_argument("--search-solver", default="cadical195")
    parser.add_argument(
        "--no-core", action="store_true",
        help="retain all CEGAR clauses instead of extracting an UNSAT core",
    )
    parser.add_argument(
        "--proof-solver", choices=("glucose3", "glucose4", "lingeling")
    )
    parser.add_argument("--replay")
    args = parser.parse_args()
    raise SystemExit(replay(args) if args.replay else run(args))


if __name__ == "__main__":
    main()
