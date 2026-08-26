#!/usr/bin/env python3
"""Generate the exact full-X5 ideal for canonical seven-block support S*."""

from __future__ import annotations

import itertools
import json
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
FIXED = frozenset(((0, 3), (1, 6), (2, 7), (4, 5)))
ADDED = frozenset(((0, 6), (1, 3), (1, 7), (2, 4), (2, 6), (5, 6), (5, 7)))
VARIABLE = frozenset(((0, 4), (1, 2), (3, 5), (6, 7)))
NONFIXED = tuple(sorted(ADDED | VARIABLE))
SUPPORT = FIXED | set(NONFIXED)


def matchings(vertices):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in matchings(rest):
            yield tuple(sorted(((first, second),) + tail))


PM8 = tuple(sorted(matchings(tuple(range(8)))))
SUPPORTED_MATCHINGS = tuple(matching for matching in PM8 if set(matching) <= SUPPORT)
assert len(PM8) == 105 and len(SUPPORTED_MATCHINGS) == 13

VARIABLE_NAMES = {
    (edge, left, right): f"x{edge[0]}{edge[1]}_{left}{right}"
    for edge in NONFIXED for left, right in itertools.product(range(3), repeat=2)
}


def amplitude_terms(word):
    terms = {}
    for matching in SUPPORTED_MATCHINGS:
        monomial = []
        for edge in matching:
            left, right = word[edge[0]], word[edge[1]]
            if edge in FIXED:
                if left != right:
                    break
            else:
                monomial.append(VARIABLE_NAMES[edge, left, right])
        else:
            monomial = tuple(sorted(monomial))
            terms[monomial] = terms.get(monomial, 0) + 1
    return terms


def polynomial_string(terms):
    pieces = []
    for monomial, coefficient in sorted(terms.items()):
        if not coefficient:
            continue
        body = "*".join(monomial) if monomial else "1"
        if coefficient == 1:
            pieces.append(f"+{body}")
        elif coefficient == -1:
            pieces.append(f"-{body}")
        elif coefficient > 0:
            pieces.append(f"+{coefficient}*{body}")
        else:
            pieces.append(f"{coefficient}*{body}")
    answer = "".join(pieces)
    if answer.startswith("+"):
        answer = answer[1:]
    return answer or "0"


def main():
    equations = []
    pure_count = 0
    mixed_count = 0
    term_census = {}
    for word in itertools.product(range(3), repeat=8):
        terms = amplitude_terms(word)
        if len(set(word)) == 1:
            terms[()] = terms.get((), 0) - 1
            pure_count += 1
        else:
            mixed_count += 1
        terms = {monomial: coefficient for monomial, coefficient in terms.items() if coefficient}
        assert terms
        term_census[str(len(terms))] = term_census.get(str(len(terms)), 0) + 1
        equations.append(polynomial_string(terms))
    assert pure_count == 3 and mixed_count == 6558 and len(equations) == 6561

    variable_list = [
        VARIABLE_NAMES[edge, left, right]
        for edge in NONFIXED for left, right in itertools.product(range(3), repeat=2)
    ]
    assert len(variable_list) == 99 and len(set(variable_list)) == 99
    program = [
        "option(noredefine);",
        f"ring r=0,({','.join(variable_list)}),dp;",
        "ideal I=" + ",\n".join(equations) + ";",
        'print("INPUT_GENERATORS="+string(size(I)));',
        "ideal G=slimgb(I);",
        'print("GROEBNER_SIZE="+string(size(G)));',
        "poly remainder=reduce(1,G);",
        'print("UNIT_REMAINDER="+string(remainder));',
        'if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }',
        "quit;",
    ]
    temporary = HERE / "canonical_full_x5.sing.tmp"
    temporary.write_text("\n".join(program) + "\n")
    temporary.replace(HERE / "canonical_full_x5.sing")
    metadata = {
        "schema": "KRENN_X5_CANONICAL_SEVEN_BLOCK_FULL_IDEAL_GATE_V1",
        "fixed": ["03", "16", "27", "45"],
        "added": ["06", "13", "17", "24", "26", "56", "57"],
        "variable": ["04", "12", "35", "67"],
        "variables": len(variable_list),
        "supported_matchings": ["|".join(f"{a}{b}" for a, b in matching) for matching in SUPPORTED_MATCHINGS],
        "supported_matching_count": len(SUPPORTED_MATCHINGS),
        "equations": len(equations),
        "pure_equations": pure_count,
        "mixed_equations": mixed_count,
        "term_census": term_census,
        "coefficient_ring": "Q",
        "groebner_algorithm": "slimgb",
        "supersedes_failed_algorithm": "std timed out at the 120-second wall with no basis/result",
        "zero_blocks_allowed": True,
    }
    (HERE / "canonical_full_x5_metadata.json").write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n")
    print(json.dumps(metadata, sort_keys=True))


if __name__ == "__main__":
    main()
