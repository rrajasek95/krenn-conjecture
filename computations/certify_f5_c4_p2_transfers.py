#!/usr/bin/env python3
"""Generate or replay the semantic C4+P2 cancellation certificate.

The support-level SAT formula is built by ``search_f5_support_sat.py``.
Every refinement stored here names two exact coefficient fibres and is
checked from scratch to be one of two elementary consequences of the
complex coefficient equations: a constant/mixed translated pair, or a
mixed relation translated onto all but one term of another mixed relation.

Replay does not trust stored clauses.  It validates the named colourings,
matching sets, and Laurent exponent identity, reconstructs every clause,
checks DIMACS hashes, and confirms UNSAT with two SAT engines.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

from pysat.solvers import Solver

import search_f5_support_sat as search


DEFAULT_CERTIFICATE = Path("computations/f5_c4_p2_transfer_certificate.json")
SCHEMA = "f5-c4-p2-laurent-transfer-v1"


def word_text(word: tuple[int, ...]) -> str:
    return "".join(map(str, word))


def parse_word(text: str) -> tuple[int, ...]:
    word = tuple(map(int, text))
    assert len(word) == 6
    assert all(colour in search.COLORS for colour in word)
    return word


def dimacs_bytes(variables: int, clauses: list[list[int]]) -> bytes:
    lines = [f"p cnf {variables} {len(clauses)}\n"]
    lines.extend(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    return "".join(lines).encode()


def subtract(first: tuple[int, ...], second: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(a - b for a, b in zip(first, second, strict=True))


def translated_shape(vectors: list[tuple[int, ...]]) -> tuple[tuple[int, ...], ...]:
    """Canonicalize a nonempty exponent multiset modulo translation."""
    assert vectors
    return min(
        tuple(sorted(subtract(vector, anchor) for vector in vectors))
        for anchor in vectors
    )


def formal_signatures():
    exceptional = search.FIVE_EDGE_GRAPHS["C4+P2"]
    rank_one = set(search.ALL_EDGES) - exceptional
    formal_keys = []
    for edge in sorted(exceptional):
        for i, j in search.CELLS:
            formal_keys.append(("entry", edge, i, j))
    for u, v in sorted(rank_one):
        for colour in search.COLORS:
            formal_keys.extend(
                (
                    ("factor_value", v, u, colour),
                    ("factor_value", u, v, colour),
                )
            )
    formal_keys = sorted(set(formal_keys), key=repr)
    formal_index = {key: index for index, key in enumerate(formal_keys)}

    def signature(colouring, matching):
        vector = [0] * len(formal_keys)
        for edge in matching:
            u, v = edge
            if edge in exceptional:
                keys = (("entry", edge, colouring[u], colouring[v]),)
            else:
                keys = (
                    ("factor_value", v, u, colouring[u]),
                    ("factor_value", u, v, colouring[v]),
                )
            for key in keys:
                vector[formal_index[key]] += 1
        return tuple(vector)

    return {
        (colouring, matching_index): signature(colouring, matching)
        for colouring in search.COLORINGS
        for matching_index, matching in enumerate(search.MATCHINGS)
    }


def exact_fibre_clause(pool, word, terms):
    """Negate the assertion that ``word`` has exactly ``terms`` supported."""
    expected = set(terms)
    return [
        -pool.id(("monomial", word, index))
        if index in expected
        else pool.id(("monomial", word, index))
        for index in range(len(search.MATCHINGS))
    ]


def record_clause(record, pool, signatures):
    """Audit one semantic record and reconstruct its valid blocking clause."""
    kind = record["kind"]
    first = record["first"]
    second = record["second"]
    first_word = parse_word(first["word"])
    second_word = parse_word(second["word"])
    first_terms = tuple(first["terms"])
    second_terms = tuple(second["terms"])
    assert first_word != second_word
    for terms in (first_terms, second_terms):
        assert terms == tuple(sorted(terms))
        assert terms and len(set(terms)) == len(terms)
        assert all(0 <= index < len(search.MATCHINGS) for index in terms)

    if kind == "constant_mixed":
        assert len(set(first_word)) == 1
        assert len(set(second_word)) > 1
        assert len(first_terms) == len(second_terms)
        first_vectors = [signatures[first_word, index] for index in first_terms]
        second_vectors = [signatures[second_word, index] for index in second_terms]
        assert translated_shape(first_vectors) == translated_shape(second_vectors)
    else:
        assert kind == "delete_one"
        assert len(set(first_word)) > 1 and len(set(second_word)) > 1
        omitted = record["omitted"]
        assert omitted in first_terms and len(first_terms) >= 3
        retained = tuple(index for index in first_terms if index != omitted)
        assert len(retained) == len(second_terms)
        retained_vectors = [signatures[first_word, index] for index in retained]
        second_vectors = [signatures[second_word, index] for index in second_terms]
        assert translated_shape(retained_vectors) == translated_shape(second_vectors)

    return exact_fibre_clause(pool, first_word, first_terms) + exact_fibre_clause(
        pool, second_word, second_terms
    )


def supported_fibres(model, pool):
    positive = {literal for literal in model if literal > 0}
    return {
        colouring: tuple(
            index
            for index in range(len(search.MATCHINGS))
            if pool.id(("monomial", colouring, index)) in positive
        )
        for colouring in search.COLORINGS
    }


def find_record(fibres, signatures):
    mixed_by_shape = defaultdict(list)
    constant_by_shape = defaultdict(list)
    for colouring, terms in fibres.items():
        if not terms:
            continue
        vectors = [signatures[colouring, index] for index in terms]
        key = (len(terms), translated_shape(vectors))
        table = constant_by_shape if len(set(colouring)) == 1 else mixed_by_shape
        table[key].append((colouring, terms))

    for key, constant_fibres in constant_by_shape.items():
        if key in mixed_by_shape:
            constant_word, constant_terms = constant_fibres[0]
            mixed_word, mixed_terms = mixed_by_shape[key][0]
            return {
                "kind": "constant_mixed",
                "first": {"word": word_text(constant_word), "terms": list(constant_terms)},
                "second": {"word": word_text(mixed_word), "terms": list(mixed_terms)},
            }

    for colouring, terms in fibres.items():
        if len(set(colouring)) == 1 or len(terms) < 3:
            continue
        for omitted in terms:
            retained = tuple(index for index in terms if index != omitted)
            vectors = [signatures[colouring, index] for index in retained]
            sources = mixed_by_shape.get((len(retained), translated_shape(vectors)))
            if sources:
                source_word, source_terms = sources[0]
                return {
                    "kind": "delete_one",
                    "first": {"word": word_text(colouring), "terms": list(terms)},
                    "second": {"word": word_text(source_word), "terms": list(source_terms)},
                    "omitted": omitted,
                }
    raise AssertionError("support model has no valid Laurent transfer")


def build_augmented(records):
    formula, pool, _ = search.support_formula(search.FIVE_EDGE_GRAPHS["C4+P2"])
    signatures = formal_signatures()
    base_clauses = [list(clause) for clause in formula.clauses]
    clauses = list(base_clauses)
    clauses.extend(record_clause(record, pool, signatures) for record in records)
    return formula.nv, base_clauses, clauses


def generate(path: Path) -> None:
    formula, pool, _ = search.support_formula(search.FIVE_EDGE_GRAPHS["C4+P2"])
    signatures = formal_signatures()
    records = []
    with Solver(name="g4", bootstrap_with=formula.clauses) as solver:
        while solver.solve():
            record = find_record(supported_fibres(solver.get_model(), pool), signatures)
            clause = record_clause(record, pool, signatures)
            solver.add_clause(clause)
            records.append(record)

    variables, base_clauses, clauses = build_augmented(records)
    with Solver(name="cadical195", bootstrap_with=clauses) as solver:
        assert not solver.solve()
    payload = {
        "schema": SCHEMA,
        "graph": "C4+P2",
        "exceptional_edges": [list(edge) for edge in sorted(search.FIVE_EDGE_GRAPHS["C4+P2"])],
        "variables": variables,
        "base_clauses": len(base_clauses),
        "augmented_clauses": len(clauses),
        "base_cnf_sha256": hashlib.sha256(dimacs_bytes(variables, base_clauses)).hexdigest(),
        "augmented_cnf_sha256": hashlib.sha256(dimacs_bytes(variables, clauses)).hexdigest(),
        "refinements": records,
    }
    path.write_text(json.dumps(payload, indent=2) + "\n")
    print(
        f"wrote {path}: {len(records)} audited semantic refinements; "
        f"sha256={payload['augmented_cnf_sha256']}"
    )


def replay(path: Path) -> None:
    payload = json.loads(path.read_text())
    assert payload["schema"] == SCHEMA
    assert payload["graph"] == "C4+P2"
    assert payload["exceptional_edges"] == [
        list(edge) for edge in sorted(search.FIVE_EDGE_GRAPHS["C4+P2"])
    ]
    variables, base_clauses, clauses = build_augmented(payload["refinements"])
    assert variables == payload["variables"]
    assert len(base_clauses) == payload["base_clauses"]
    assert len(clauses) == payload["augmented_clauses"]
    assert hashlib.sha256(dimacs_bytes(variables, base_clauses)).hexdigest() == payload["base_cnf_sha256"]
    assert hashlib.sha256(dimacs_bytes(variables, clauses)).hexdigest() == payload["augmented_cnf_sha256"]
    for solver_name in ("g4", "cadical195"):
        with Solver(name=solver_name, bootstrap_with=clauses) as solver:
            assert not solver.solve(), solver_name
    counts = defaultdict(int)
    for record in payload["refinements"]:
        counts[record["kind"]] += 1
    print(
        f"PASS: replayed {len(payload['refinements'])} semantic refinements "
        f"({dict(sorted(counts.items()))}); hashes agree; "
        "Glucose4 and CaDiCaL195 both report UNSAT"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=DEFAULT_CERTIFICATE)
    parser.add_argument("--generate", action="store_true")
    args = parser.parse_args()
    if args.generate:
        generate(args.certificate)
    else:
        replay(args.certificate)


if __name__ == "__main__":
    main()
