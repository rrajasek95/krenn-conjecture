#!/usr/bin/env python3
"""Exact characteristic-zero X4 test in small site/color-equivariant families.

The raw 252 endpoint cells are quotiented by one of three explicit finite
symmetries.  All 4,881 hafnian equations are rebuilt and combined over Z,
then Singular decides the resulting ideal over Q.  This is a bounded-family
classification, not a statement about arbitrary X4 sources.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from collections import Counter
from itertools import combinations, product
from pathlib import Path


HERE = Path(__file__).resolve().parent
SITES = tuple(range(8))
COLORS = tuple(range(3))
EDGES = tuple(combinations(SITES, 2))
CELLS = tuple((u, v, a, b) for u, v in EDGES for a in COLORS for b in COLORS)
INDEX = {cell: i for i, cell in enumerate(CELLS)}


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for k in range(1, len(vertices)):
        v = vertices[k]
        rest = vertices[1:k] + vertices[k + 1:]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


PMS = tuple(perfect_matchings(SITES))


def transform(cell, shift, perm):
    u, v, a, b = cell
    u, v, a, b = (u + shift) % 8, (v + shift) % 8, perm[a], perm[b]
    return (u, v, a, b) if u < v else (v, u, b, a)


def quotient(kind):
    shift, perm = {
        "cyclic": (1, (0, 1, 2)),
        "swap01": (1, (1, 0, 2)),
        "cycle012": (1, (1, 2, 0)),
        "halfturn": (4, (0, 1, 2)),
    }[kind]
    raw_rep = []
    for raw in CELLS:
        orbit, cur = [], raw
        while cur not in orbit:
            orbit.append(cur)
            cur = transform(cur, shift, perm)
        raw_rep.append(min(INDEX[x] for x in orbit))
    reps = sorted(set(raw_rep))
    compact = {rep: k for k, rep in enumerate(reps)}
    return tuple(compact[x] for x in raw_rep), reps


def cell_index(u, v, a, b):
    if u > v:
        u, v, a, b = v, u, b, a
    return INDEX[(u, v, a, b)]


def off_count(word):
    return 8 - max(word.count(c) for c in COLORS)


def polynomial(word, qmap, nvars):
    answer = Counter()
    for matching in PMS:
        exponent = [0] * nvars
        for u, v in matching:
            exponent[qmap[cell_index(u, v, word[u], word[v])]] += 1
        answer[tuple(exponent)] += 1
    if len(set(word)) == 1:
        answer[(0,) * nvars] -= 1
    return tuple(sorted((e, c) for e, c in answer.items() if c))


def emit_poly(poly):
    pieces = []
    for exponent, coefficient in poly:
        mon = "*".join(
            f"x{i + 1}" + (f"^{power}" if power != 1 else "")
            for i, power in enumerate(exponent) if power
        )
        if not mon:
            piece = str(coefficient)
        elif coefficient == 1:
            piece = mon
        elif coefficient == -1:
            piece = "-" + mon
        else:
            piece = f"{coefficient}*{mon}"
        pieces.append(piece)
    if not pieces:
        return "0"
    text = pieces[0]
    for piece in pieces[1:]:
        text += piece if piece.startswith("-") else "+" + piece
    return text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("kind", choices=("cyclic", "swap01", "cycle012", "halfturn"))
    parser.add_argument("--timeout", type=int, default=1200)
    parser.add_argument("--algorithm", choices=("std", "slimgb"), default="slimgb")
    args = parser.parse_args()
    qmap, reps = quotient(args.kind)
    polys = {}
    counts = Counter()
    for word in product(COLORS, repeat=8):
        word = tuple(word)
        off = off_count(word)
        if off > 4:
            continue
        poly = polynomial(word, qmap, len(reps))
        counts[off] += 1
        if poly:
            polys.setdefault(poly, word)
    generators = list(polys)
    body = ",\n".join(emit_poly(g) for g in generators)
    variable_names = ",".join(f"x{i + 1}" for i in range(len(reps)))
    script = (
        f"ring R=0,({variable_names}),dp;\n"
        f"ideal I={body};\n"
        f"ideal G={args.algorithm}(I);\n"
        '"UNIT:",(size(G)==1 && G[1]==1);\n'
        '"DIM:",dim(G);\n'
        '"GSIZE:",size(G);\n'
    )
    singular_path = HERE / f"equivariant_{args.kind}.sing"
    singular_path.write_text(script)
    timed_out = False
    try:
        proc = subprocess.run(
            ["Singular", "-q", "--no-warn", str(singular_path)],
            text=True, capture_output=True, timeout=args.timeout,
        )
    except subprocess.TimeoutExpired as error:
        timed_out = True
        proc = subprocess.CompletedProcess(
            error.cmd, -1,
            stdout=(error.stdout or b"").decode() if isinstance(error.stdout, bytes) else (error.stdout or ""),
            stderr=(error.stderr or b"").decode() if isinstance(error.stderr, bytes) else (error.stderr or ""),
        )
    parsed = {}
    for line in proc.stdout.splitlines():
        for key in ("UNIT", "DIM", "GSIZE"):
            if line.startswith(key + ":"):
                parsed[key] = line.split(":", 1)[1]
    output = {
        "status": "UNAUDITED_EXACT_BOUNDED_FAMILY",
        "family": args.kind,
        "algorithm": args.algorithm,
        "symmetry": {
            "cyclic": "site shift +1, colors fixed",
            "swap01": "site shift +1, colors 0 and 1 swapped",
            "cycle012": "site shift +1, colors cycled 0->1->2->0",
            "halfturn": "site shift +4, colors fixed",
        }[args.kind],
        "raw_cells": 252,
        "quotient_variables": len(reps),
        "representative_cells": [list(CELLS[i]) for i in reps],
        "raw_word_counts": dict(sorted(counts.items())),
        "unique_nonzero_generators": len(generators),
        "generator_sha256": hashlib.sha256(body.encode()).hexdigest(),
        "singular_returncode": proc.returncode,
        "singular_timed_out": timed_out,
        "singular_stdout": proc.stdout[-2000:],
        "singular_stderr": proc.stderr[-2000:],
        "decision": parsed if parsed else {"status": "TIMEOUT_NO_VERDICT" if timed_out else "PARSE_FAILURE_NO_VERDICT"},
        "scope_warning": "Only the named equivariant linear family is decided.",
    }
    outpath = HERE / f"results_equivariant_{args.kind}.json"
    outpath.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"family": args.kind, "nvars": len(reps), "ngens": len(generators), **parsed}, sort_keys=True))


if __name__ == "__main__":
    main()
