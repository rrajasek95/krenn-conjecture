#!/usr/bin/env python3
"""Replay the smallest coordinate dual excluding P0^2 from clean binary J."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPAN_PATH = HERE / "audit_r8prime_p0_binary_packet_span.py"
SPEC = importlib.util.spec_from_file_location("p0_span_dual", SPAN_PATH)
SPAN = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SPAN)
BASE = SPAN.BASE
EXPORT = SPAN.EXPORT
TARGET = HERE / "r8prime_square_pure_anchor_factored_canonical.jsonl"
OUT = HERE / "results_r8prime_p0_square_clean_j_coordinate_dual.json"

WITNESS = bytes.fromhex("0d0d1919555562629797c4c4e0e0e6e6")
WITNESS_COEFFICIENT = 2304


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def alternating_words():
    return tuple(tuple(value for colour in choices
                       for value in (colour, 3 - colour))
                 for choices in product((1, 2), repeat=4))


def divides(row: bytes, term: bytes) -> bool:
    row_counts = Counter(row)
    return all(row_counts[cell] >= multiplicity
               for cell, multiplicity in Counter(term).items())


def matching_from_term(term: bytes):
    return tuple(sorted((BASE.CELLS[cell][0], BASE.CELLS[cell][1])
                        for cell in term))


def main() -> None:
    require(len(WITNESS) == 16, "witness degree changed")
    first_row = None
    with TARGET.open() as stream:
        header = json.loads(next(stream))
        for line in stream:
            record = json.loads(line)
            if record.get("type") == "row":
                first_row = record
                break
    require(header["nonzero_orbits"] == 1_578_292,
            "canonical target orbit count changed")
    require(first_row is not None, "canonical target has no rows")
    require(first_row["index"] == 0, "first target index changed")
    require(bytes.fromhex(first_row["row"]) == WITNESS,
            "lex-first target row changed")
    require(first_row["coefficient"] == [WITNESS_COEFFICIENT, 1],
            "witness target coefficient changed")

    support = Counter(WITNESS)
    require(set(support.values()) == {2}, "witness is not a square")
    square_root = bytes(sorted(support))
    SPAN.audit_p0_row(square_root)
    physical_edges = tuple(sorted((BASE.CELLS[cell][0],
                                   BASE.CELLS[cell][1])
                                  for cell in square_root))
    degrees = Counter(vertex for edge in physical_edges for vertex in edge)
    require(all(degrees[site] == 2 for site in range(BASE.N)),
            "witness physical graph is not 2-regular")

    words = alternating_words()
    require(len(words) == 16, "clean generator count changed")
    dividing_terms = []
    supported_matchings = set()
    checked = 0
    for word in words:
        for term in BASE.word_terms(word):
            checked += 1
            if set(term) <= set(square_root):
                supported_matchings.add(matching_from_term(term))
            if divides(WITNESS, term):
                dividing_terms.append((word, term))
    require(checked == 16 * 105, "clean source term census changed")
    require(not dividing_terms,
            "an alternating-binary generator term divides the witness")

    # Independently enumerate the two uncoloured perfect matchings of the
    # underlying eight-cycle, then show neither has a consistent alternating
    # word.  This is a human-sized replay of the 1,680 literal checks above.
    physical_set = frozenset(physical_edges)
    cycle_matchings = []
    for matching in BASE.PM8:
        if set(matching) <= physical_set:
            cycle_matchings.append(tuple(matching))
    require(len(cycle_matchings) == 2,
            "witness eight-cycle no longer has exactly two perfect matchings")
    compatible_words = {}
    for matching in cycle_matchings:
        compatible = []
        for word in words:
            term = BASE.term_ids(word, matching)
            if set(term) <= set(square_root):
                compatible.append("".join(map(str, word)))
        compatible_words[str(matching)] = compatible
        require(not compatible,
                "an eight-cycle matching acquired an alternating colouring")

    # Covariance: every H_768 transform of the row is still killed because
    # H_768 permutes the 16 alternating words and their 105 terms.
    orbit = SPAN.h_orbit(WITNESS)
    require(min(orbit) == WITNESS, "witness is not its canonical orbit row")
    for transformed in orbit:
        require(not any(divides(transformed, term)
                        for word in words for term in BASE.word_terms(word)),
                "coordinate-dual covariance failed on an orbit member")

    result = {
        "status": "UNAUDITED exact coordinate-dual replay",
        "target_sha256": sha256(TARGET.read_bytes()).hexdigest(),
        "target_nonzero_row_orbits": header["nonzero_orbits"],
        "witness_row": WITNESS.hex(),
        "witness_factorization": [
            {"cell": list(BASE.CELLS[cell]), "exponent": multiplicity}
            for cell, multiplicity in sorted(support.items())
        ],
        "witness_target_quotient_coefficient": [WITNESS_COEFFICIENT, 1],
        "witness_orbit_size": len(orbit),
        "clean_generators": len(words),
        "terms_per_generator": 105,
        "literal_divisibility_checks": checked,
        "dividing_source_terms": 0,
        "physical_graph": "one 8-cycle",
        "physical_cycle_matchings": [list(map(list, matching))
                                     for matching in cycle_matchings],
        "compatible_alternating_words_by_matching": compatible_words,
        "coordinate_dual": (
            "coefficient extraction at the H_768 orbit of witness_row; it "
            "annihilates every degree-16 column Q*H_w in clean J because "
            "some term of H_w must divide the row"
        ),
        "conclusion": "P0^2 is not in the clean alternating-binary ideal J",
        "scope": (
            "This is only a negative result for the positive-sufficient "
            "clean J subproblem. It is not a dual for the full degree-16 "
            "associated-graded source family or the whole cutoff below 17."
        ),
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("R8' P0^2 clean-J coordinate dual: PASS")
    print("witness/orbit/target coefficient:", WITNESS.hex(), len(orbit),
          WITNESS_COEFFICIENT)
    print("literal source terms/divisors:", checked, len(dividing_terms))
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
