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

Every check below raises instead of asserting.  A bare ``assert`` is deleted
by ``python3 -O``, and here the whole semantic audit of each refinement, the
DIMACS hash comparisons, and both UNSAT solves used to sit inside assert
tests -- so ``-O`` printed the "hashes agree ... both report UNSAT" line
without having compared a hash or run a solver.
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


def require(condition: object, message: str) -> None:
    """Check a load-bearing condition in a way ``python3 -O`` cannot remove."""

    if not condition:
        raise ValueError(message)


def word_text(word: tuple[int, ...]) -> str:
    return "".join(map(str, word))


def parse_word(text: str) -> tuple[int, ...]:
    word = tuple(map(int, text))
    require(len(word) == 6, f"word {text!r} does not have six sites")
    require(
        all(colour in search.COLORS for colour in word),
        f"word {text!r} uses a colour outside {search.COLORS}",
    )
    return word


def dimacs_bytes(variables: int, clauses: list[list[int]]) -> bytes:
    lines = [f"p cnf {variables} {len(clauses)}\n"]
    lines.extend(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    return "".join(lines).encode()


def subtract(first: tuple[int, ...], second: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(a - b for a, b in zip(first, second, strict=True))


def translated_shape(vectors: list[tuple[int, ...]]) -> tuple[tuple[int, ...], ...]:
    """Canonicalize a nonempty exponent multiset modulo translation."""
    require(vectors, "translated_shape needs a nonempty exponent multiset")
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
    require(first_word != second_word, f"record pairs {first_word} with itself")
    for terms in (first_terms, second_terms):
        require(terms == tuple(sorted(terms)), f"terms {terms} are not sorted")
        require(
            terms and len(set(terms)) == len(terms),
            f"terms {terms} are empty or repeat an index",
        )
        require(
            all(0 <= index < len(search.MATCHINGS) for index in terms),
            f"terms {terms} leave the matching range",
        )

    if kind == "constant_mixed":
        require(len(set(first_word)) == 1, f"{first_word} is not constant")
        require(len(set(second_word)) > 1, f"{second_word} is not mixed")
        require(
            len(first_terms) == len(second_terms),
            f"fibre sizes {len(first_terms)} != {len(second_terms)}",
        )
        first_vectors = [signatures[first_word, index] for index in first_terms]
        second_vectors = [signatures[second_word, index] for index in second_terms]
        require(
            translated_shape(first_vectors) == translated_shape(second_vectors),
            f"{first_word}/{second_word} are not translates of one another",
        )
    else:
        require(kind == "delete_one", f"unknown refinement kind {kind!r}")
        require(
            len(set(first_word)) > 1 and len(set(second_word)) > 1,
            f"delete_one needs two mixed words, got {first_word}/{second_word}",
        )
        omitted = record["omitted"]
        require(
            omitted in first_terms and len(first_terms) >= 3,
            f"omitted term {omitted} is not deletable from {first_terms}",
        )
        retained = tuple(index for index in first_terms if index != omitted)
        require(
            len(retained) == len(second_terms),
            f"retained size {len(retained)} != {len(second_terms)}",
        )
        retained_vectors = [signatures[first_word, index] for index in retained]
        second_vectors = [signatures[second_word, index] for index in second_terms]
        require(
            translated_shape(retained_vectors) == translated_shape(second_vectors),
            f"{first_word} minus {omitted} is not a translate of {second_word}",
        )

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
        satisfiable = solver.solve()
        require(not satisfiable, "cadical195 reports SAT, expected UNSAT")
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
    require(payload["schema"] == SCHEMA, f"schema {payload['schema']!r} != {SCHEMA!r}")
    require(payload["graph"] == "C4+P2", f"graph {payload['graph']!r} != 'C4+P2'")
    require(
        payload["exceptional_edges"]
        == [list(edge) for edge in sorted(search.FIVE_EDGE_GRAPHS["C4+P2"])],
        "certificate is for a different exceptional edge set",
    )
    variables, base_clauses, clauses = build_augmented(payload["refinements"])
    require(
        variables == payload["variables"],
        f"variables {variables} != {payload['variables']}",
    )
    require(
        len(base_clauses) == payload["base_clauses"],
        f"base clauses {len(base_clauses)} != {payload['base_clauses']}",
    )
    require(
        len(clauses) == payload["augmented_clauses"],
        f"augmented clauses {len(clauses)} != {payload['augmented_clauses']}",
    )
    base_digest = hashlib.sha256(dimacs_bytes(variables, base_clauses)).hexdigest()
    require(
        base_digest == payload["base_cnf_sha256"],
        f"base cnf sha256 {base_digest} != {payload['base_cnf_sha256']}",
    )
    augmented_digest = hashlib.sha256(dimacs_bytes(variables, clauses)).hexdigest()
    require(
        augmented_digest == payload["augmented_cnf_sha256"],
        f"augmented cnf sha256 {augmented_digest} != {payload['augmented_cnf_sha256']}",
    )
    for solver_name in ("g4", "cadical195"):
        with Solver(name=solver_name, bootstrap_with=clauses) as solver:
            satisfiable = solver.solve()
            require(
                not satisfiable, f"{solver_name} reports SAT, expected UNSAT"
            )
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
