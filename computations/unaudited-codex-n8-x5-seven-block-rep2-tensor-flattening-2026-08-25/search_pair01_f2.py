#!/usr/bin/env python3
"""Exact F2 countermodel search for the rep2 rank-one pair01 system.

This is deliberately independent of the sealed Groebner inputs.  It rebuilds
the 13 source-labelled perfect-matching terms and writes a Boolean SMT model,
where xor/and are exactly addition/multiplication in F2.
"""

from __future__ import annotations

import itertools
import json
import os
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
COLORS = range(3)
FIXED = frozenset(((0, 3), (1, 6), (2, 7), (4, 5)))
ADDED = frozenset(((0, 6), (1, 4), (1, 7), (2, 3), (2, 6), (5, 6), (5, 7)))
VARIABLE = frozenset(((0, 4), (1, 2), (3, 5), (6, 7)))
ELIMINATED = frozenset(((5, 6), (5, 7)))
RETAINED = tuple(sorted((ADDED | VARIABLE) - ELIMINATED))
SUPPORT = FIXED | ADDED | VARIABLE


def matchings(vertices):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in matchings(rest):
            yield tuple(sorted(((first, second),) + tail))


SUPPORTED = tuple(
    matching for matching in matchings(tuple(range(8))) if set(matching) <= SUPPORT
)
assert len(SUPPORTED) == 13
SOURCE = {
    (edge, i, j): f"a{edge[0]}{edge[1]}_{i}{j}"
    for edge in RETAINED
    for i, j in itertools.product(COLORS, repeat=2)
}
U = tuple(f"u{i}" for i in COLORS)
V = tuple(f"v{i}" for i in COLORS)
DUAL = {name: tuple(f"{name}{i}" for i in COLORS) for name in "xyz"}
RHO = tuple(f"rho{i}" for i in COLORS)
SIGMA = tuple(f"sigma{i}" for i in COLORS)
TAU = "tau"


def xor(*terms):
    terms = tuple(term for term in terms if term != "false")
    if not terms:
        return "false"
    if len(terms) == 1:
        return terms[0]
    return f"(xor {' '.join(terms)})"


def land(*terms):
    if "false" in terms:
        return "false"
    terms = tuple(term for term in terms if term != "true")
    if not terms:
        return "true"
    if len(terms) == 1:
        return terms[0]
    return f"(and {' '.join(terms)})"


def retained(edge, i, j):
    return SOURCE[edge, i, j]


def a26v(row):
    return xor(*(land(retained((2, 6), row, k), V[k]) for k in COLORS))


def entry(edge, i, j):
    if edge in FIXED:
        return "true" if i == j else "false"
    if edge == (5, 7):
        return land(U[i], V[j])
    if edge == (5, 6):
        # Minus equals plus over F2.
        return land(U[i], a26v(j))
    return retained(edge, i, j)


def amplitude(word):
    terms = []
    for matching in SUPPORTED:
        terms.append(land(*(entry(edge, word[edge[0]], word[edge[1]]) for edge in matching)))
    return xor(*terms)


def constraints():
    result = []
    labels = []
    for word in itertools.product((0, 1), repeat=8):
        result.append(amplitude(word))
        labels.append("amp_" + "".join(map(str, word)))
        if len(set(word)) == 1:
            result[-1] = xor(result[-1], "true")
    word = (2,) * 8
    result.append(xor(amplitude(word), "true"))
    labels.append("amp_22222222")

    # Guard: A06*v=0 and (I-A17*A26)*v=0.
    for i in COLORS:
        result.append(xor(*(land(retained((0, 6), i, j), V[j]) for j in COLORS)))
        labels.append(f"guard06_{i}")
    for i in COLORS:
        correction = xor(*(
            land(retained((1, 7), i, j), retained((2, 6), j, k), V[k])
            for j, k in itertools.product(COLORS, repeat=2)
        ))
        result.append(xor(V[i], correction))
        labels.append(f"guard1726_{i}")

    # Cap67 adjoint failure graph.
    for i, j in itertools.product(COLORS, repeat=2):
        gi = xor(
            *(land(retained((0, 6), k, i), DUAL["x"][k]) for k in COLORS),
            DUAL["y"][i],
            *(land(retained((2, 6), k, i), DUAL["z"][k]) for k in COLORS),
        )
        hj = xor(
            *(land(retained((1, 7), k, j), DUAL["y"][k]) for k in COLORS),
            DUAL["z"][j],
        )
        rhs = xor(land(gi, V[j]), land(a26v(i), hj))
        result.append(xor(retained((6, 7), i, j), rhs))
        labels.append(f"adj67_{i}{j}")

    # Cap45/star1 failure incidence.
    for j in COLORS:
        value = xor(*(land(retained((0, 4), i, j), RHO[i]) for i in COLORS))
        result.append(xor(value, "true" if j == 0 else "false"))
        labels.append(f"inc04_{j}")
    for j in COLORS:
        value = xor(
            *(land(retained((3, 5), i, j), SIGMA[i]) for i in COLORS),
            land(U[j], TAU),
        )
        result.append(xor(value, "true" if j == 0 else "false"))
        labels.append(f"inc35u_{j}")

    assert len(result) == 278 == len(labels)
    return result, labels


def main():
    equations, labels = constraints()
    variables = (
        list(SOURCE.values())
        + list(U)
        + list(V)
        + [item for name in "xyz" for item in DUAL[name]]
        + list(RHO)
        + list(SIGMA)
        + [TAU]
    )
    assert len(variables) == 103 == len(set(variables))
    lines = [
        "(set-option :produce-unsat-cores true)",
        "(set-option :smt.core.minimize true)",
    ]
    lines.extend(f"(declare-const {variable} Bool)" for variable in variables)
    lines.extend(
        f"(assert (! (not {equation}) :named c_{index}_{label}))"
        for index, (equation, label) in enumerate(zip(equations, labels))
    )
    # Exact rank one rather than the rank-zero closure.
    lines.append(f"(assert (! (or {' '.join(U)}) :named rank_u))")
    lines.append(f"(assert (! (or {' '.join(V)}) :named rank_v))")
    lines.extend(("(check-sat)", "(get-unsat-core)"))
    smt = HERE / "rep2_pair01_rank1_f2.smt2"
    temporary = smt.with_suffix(".smt2.tmp")
    temporary.write_text("\n".join(lines) + "\n")
    os.replace(temporary, smt)
    process = subprocess.run(
        ["z3", "-T:60", str(smt)], capture_output=True, text=True, timeout=65
    )
    output = process.stdout + process.stderr
    (HERE / "rep2_pair01_rank1_f2.stdout").write_text(output)
    status = next((line for line in output.splitlines() if line in {"sat", "unsat", "unknown"}), "NO_STATUS")
    result = {
        "schema": "KRENN_X5_REP2_PAIR01_F2_COUNTERMODEL_SEARCH_V1",
        "field": 2,
        "variables": len(variables),
        "equations": len(equations),
        "rank_one_nonzero_assertions": 2,
        "supported_matching_count": len(SUPPORTED),
        "status": status,
        "solver_returncode": process.returncode,
    }
    (HERE / "results_pair01_f2_search.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
