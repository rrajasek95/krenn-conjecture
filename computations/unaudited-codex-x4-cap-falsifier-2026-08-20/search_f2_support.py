#!/usr/bin/env python3
"""Search characteristic-two support shadows of the N=8 X4 scheme.

This is deliberately a discovery tool, not a characteristic-zero proof.
It emits the raw 4,881 Boolean hafnian equations to z3, enumerates models,
and tests all response-star/triangle carriers over F_2 and Q.  A support hit
must still be lifted (or eliminated) over characteristic zero.
"""

from __future__ import annotations

import argparse
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


def idx(u, v, a, b):
    if u > v:
        u, v, a, b = v, u, b, a
    return INDEX[(u, v, a, b)]


def off_count(word):
    return 8 - max(word.count(c) for c in COLORS)


def monomials(word):
    return tuple(tuple(idx(u, v, word[u], word[v]) for u, v in pm) for pm in PMS)


def bool_term(mon):
    names = [f"x{i}" for i in sorted(set(mon))]
    return names[0] if len(names) == 1 else "(and " + " ".join(names) + ")"


def xor_expr(terms):
    if not terms:
        return "false"
    if len(terms) == 1:
        return terms[0]
    return "(xor " + " ".join(terms) + ")"


def transformed_cell(cell, site_shift, color_perm):
    u, v, a, b = cell
    u = (u + site_shift) % 8
    v = (v + site_shift) % 8
    a, b = color_perm[a], color_perm[b]
    if u > v:
        u, v, a, b = v, u, b, a
    return u, v, a, b


def equivalence_representatives(equivariance):
    if equivariance == "none":
        return tuple(range(len(CELLS)))
    shift, perm = {
        "cyclic": (1, (0, 1, 2)),
        "swap01": (1, (1, 0, 2)),
        "cycle012": (1, (1, 2, 0)),
        "halfturn": (4, (0, 1, 2)),
    }[equivariance]
    answer = []
    for raw in CELLS:
        orbit = []
        cur = raw
        while cur not in orbit:
            orbit.append(cur)
            cur = transformed_cell(cur, shift, perm)
        answer.append(min(INDEX[cell] for cell in orbit))
    return tuple(answer)


def build_smt(min_ones, max_ones, blocks, equivariance):
    lines = ["(set-option :produce-models true)", "(set-logic QF_FD)"]
    lines.extend(f"(declare-const x{i} Bool)" for i in range(len(CELLS)))
    representatives = equivalence_representatives(equivariance)
    if min_ones is not None:
        lines.append(f"(assert ((_ at-least {min_ones}) {' '.join(f'x{i}' for i in range(len(CELLS))) }))")
    if max_ones is not None:
        lines.append(f"(assert ((_ at-most {max_ones}) {' '.join(f'x{i}' for i in range(len(CELLS))) }))")
    if equivariance != "none":
        for i, j in enumerate(representatives):
            if i != j:
                lines.append(f"(assert (= x{i} x{j}))")
    counts = Counter()
    for word in product(COLORS, repeat=8):
        word = tuple(word)
        if off_count(word) > 4:
            continue
        # In the symmetry quotient, identical matching monomials cancel in
        # pairs over F2.  Doing this before SMT emission is decisive: cyclic
        # runs have only 33 effective variables and tiny equations.
        parity = Counter(
            tuple(sorted(set(representatives[i] for i in mon)))
            for mon in monomials(word)
        )
        terms = [bool_term(mon) for mon, count in parity.items() if count & 1]
        target = len(set(word)) == 1
        expr = xor_expr(terms)
        lines.append(f"(assert {expr if target else '(not ' + expr + ')'})")
        counts[off_count(word)] += 1
    for support in blocks:
        lits = [f"x{i}" if i not in support else f"(not x{i})" for i in range(len(CELLS))]
        lines.append("(assert (or " + " ".join(lits) + "))")
    lines.extend(["(check-sat)", "(get-model)"])
    return "\n".join(lines) + "\n", dict(sorted(counts.items()))


def parse_model(text):
    if not text.startswith("sat\n"):
        return None
    values = {}
    lines = text.splitlines()
    for k, line in enumerate(lines):
        line = line.strip()
        if line.startswith("(define-fun x"):
            name = line.split()[1]
            value = lines[k + 1].strip().rstrip(")")
            values[int(name[1:])] = value == "true"
    return frozenset(i for i in range(len(CELLS)) if values.get(i, False))


def rank_mod2(rows):
    packed = []
    for row in rows:
        value = 0
        for j, x in enumerate(row):
            if x & 1:
                value ^= 1 << j
        packed.append(value)
    basis = {}
    for value in packed:
        while value:
            p = value.bit_length() - 1
            if p in basis:
                value ^= basis[p]
            else:
                basis[p] = value
                break
    return len(basis)


def source_from_support(support):
    source = {edge: [[0] * 3 for _ in range(3)] for edge in EDGES}
    for i in support:
        u, v, a, b = CELLS[i]
        source[(u, v)][a][b] = 1
    return source


def cell(source, u, v, a, b):
    return source[(u, v)][a][b] if u < v else source[(v, u)][b][a]


def response_row(source, p, q, a, b, alpha, beta):
    return [
        cell(source, p, a, i, alpha) * cell(source, q, b, j, beta)
        + cell(source, p, b, i, beta) * cell(source, q, a, j, alpha)
        for i in COLORS for j in COLORS
    ]


def carrier_rows(source, p, q, kind, carrier):
    residual = tuple(v for v in SITES if v not in (p, q))
    if kind == "star":
        allowed = {edge for edge in combinations(residual, 2) if carrier in edge}
    else:
        allowed = set(combinations(carrier, 2))
    return [
        response_row(source, p, q, a, b, alpha, beta)
        for a, b in combinations(residual, 2) if (a, b) not in allowed
        for alpha in COLORS for beta in COLORS
    ]


def activity(source, p, q):
    rows = []
    for c in COLORS:
        row = [0] * 9
        row[3 * c + c] = 1
        rows.append(row)
    rows.append([cell(source, p, q, i, j) for i in COLORS for j in COLORS])
    return rows


def profile_mod2(source):
    passing = []
    blockers = Counter()
    for p, q in EDGES:
        residual = tuple(v for v in SITES if v not in (p, q))
        for kind, carriers in (
            ("star", ((v,) for v in residual)),
            ("triangle", combinations(residual, 3)),
        ):
            for raw in carriers:
                carrier = raw[0] if kind == "star" else tuple(raw)
                rows = carrier_rows(source, p, q, kind, carrier)
                base = rank_mod2(rows)
                mask = tuple(rank_mod2(rows + [ell]) == base for ell in activity(source, p, q))
                blockers["".join("1" if x else "0" for x in mask)] += 1
                if not any(mask):
                    passing.append({"pair": [p, q], kind: carrier, "rank": base})
    return passing, dict(sorted(blockers.items()))


def q_word_value(source, word):
    return sum(
        __import__("math").prod(cell(source, u, v, word[u], word[v]) for u, v in pm)
        for pm in PMS
    )


def q_defects(source):
    counts = Counter()
    samples = []
    for word in product(COLORS, repeat=8):
        word = tuple(word)
        if off_count(word) > 4:
            continue
        value = q_word_value(source, word)
        target = int(len(set(word)) == 1)
        if value != target:
            counts[off_count(word)] += 1
            if len(samples) < 12:
                samples.append({"word": list(word), "value": value, "target": target})
    return dict(sorted(counts.items())), samples


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", type=int, default=8)
    parser.add_argument("--min-ones", type=int, default=20)
    parser.add_argument("--max-ones", type=int, default=80)
    parser.add_argument("--timeout-ms", type=int, default=300000)
    parser.add_argument(
        "--equivariance",
        choices=("none", "cyclic", "swap01", "cycle012", "halfturn"),
        default="cyclic",
    )
    args = parser.parse_args()
    records = []
    blocks = []
    word_counts = None
    for number in range(args.models):
        smt, word_counts = build_smt(
            args.min_ones, args.max_ones, blocks, args.equivariance
        )
        smt_path = HERE / f"search_{args.equivariance}.smt2"
        smt_path.write_text(smt)
        proc = subprocess.run(
            ["z3", f"-T:{max(1, args.timeout_ms // 1000)}", str(smt_path)],
            text=True, capture_output=True, timeout=args.timeout_ms / 1000 + 10,
        )
        support = parse_model(proc.stdout)
        if support is None:
            records.append({"solver": proc.stdout.splitlines()[:2], "stderr": proc.stderr[:300]})
            break
        source = source_from_support(support)
        passes, blockers = profile_mod2(source)
        defects, samples = q_defects(source)
        rec = {
            "model": number,
            "ones": len(support),
            "support_indices": sorted(support),
            "support_cells": [list(CELLS[i]) for i in sorted(support)],
            "F2_carrier_passes": len(passes),
            "F2_first_passes": passes[:12],
            "F2_blocker_histogram": blockers,
            "Q_X4_defects_by_offcount": defects,
            "Q_X4_first_defects": samples,
        }
        records.append(rec)
        blocks.append(support)
        print(f"model {number}: ones={len(support)} F2-passes={len(passes)} Q-defects={sum(defects.values())}", flush=True)
        if not passes:
            print("CARRIER-EVASIVE F2 SHADOW", number, flush=True)
            break
    out = {
        "status": "DISCOVERY_ONLY_CHARACTERISTIC_TWO",
        "scope_warning": "F2 support shadows do not prove existence over C/Qbar",
        "word_counts": word_counts,
        "parameters": vars(args),
        "records": records,
    }
    output_path = HERE / f"results_f2_support_{args.equivariance}.json"
    output_path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print("wrote", output_path)


if __name__ == "__main__":
    main()
