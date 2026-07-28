#!/usr/bin/env python3
"""Round 1 of the four-extra-cell varied-q exact search at the polarized seed.

Region.  In the eight-site ternary square-zero algebra fix the recorded seed

    q = 23_00+45_00+67_00 + 01_11+36_11+57_11 + 02_22+14_22+56_22,
    z = 01_00 + 24_11 + 37_22,

with z*q^[3] = Delta_{8,3}.  This round searches the first sanctioned open
sparse region beyond the recorded exclusions: quadruples e1<e2<e3<e4 of
distinct endpoint-colour cells outside supp(q), coefficients
t1,t2,t3,t4 in C^*, and the varied internal quadratic

    Q = q + t1*e1 + t2*e2 + t3*e3 + t4*e4.

The census decides exactly, for every one of the C(243,4) = 141,722,460
quadruples, whether the polarized target identity  z*Q^[3] = Delta_{8,3}
has a solution with all four coefficients nonzero.

Method.  Multilinearity in the square-zero algebra gives the exact
Laurent-debt expansion (no t1*t2*t3*t4 term can occur in a cubic power):

  z*Q^[3] - Delta = sum_i t_i D_i + sum_{i<j} t_i t_j D_ij
                    + sum_{i<j<k} t_i t_j t_k D_ijk,

  D_i = z e_i q^[2],  D_ij = z e_i e_j q,  D_ijk = z e_i e_j e_k.

Every nonzero debt coefficient equals one (asserted).  If a top word is hit
by exactly one of the fourteen Laurent monomials, the identity fails on the
whole torus.  The census therefore classifies quadruples into:

  * compatible          -- all fourteen debts vanish; identity holds for all t.
  * singleton_rejection -- some top word has exactly one Laurent hit.
  * support survivors   -- every hit word is hit at least twice; the exact
                           polynomial system in t1..t4 is then decided by a
                           saturated Groebner basis over Q (torus variable h,
                           h*t1*t2*t3*t4 = 1): a unit ideal is
                           torus-inconsistent, a non-unit ideal is a
                           cancellation family (Nullstellensatz over C).

Completeness of the survivor enumeration (anchor lemma).  Every survivor
with at least one visible cell (nonzero D_i) contains a visible cell e_i
whose debt word w must be hit by a second Laurent monomial, i.e. by the
single debt of another chosen cell, by the cross debt of a chosen pair, or
by the triple debt of a chosen triple.  The cells of that second object all
lie in the quadruple, so the quadruple is an extension of {e_i} union
cells(object) by free cells.  Enumerating every visible cell, every matching
object with the same word, and all free completions therefore reaches every
survivor with a visible cell.  Survivors without visible cells are quadruples
of invisible cells and are covered by the direct scan of all C(99,4)
invisible quadruples.  An independent exhaustive C scan of all C(243,4)
quadruples (search_n8_varied_q_round_1_exhaustive_scan.c) confirms the
classification counts and the survivor list.

Outputs (small): a JSON summary next to this script and the identically
compatible quadruple ledger digest.  The full compatible list is written to
--scratch-dir for the pair-cap closure driver, not to the repository.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
from itertools import combinations, product
import json
import os
import shutil
import subprocess

SITES = tuple(range(8))
COLOURS = (0, 1, 2)
EDGES = tuple(combinations(SITES, 2))
ALL_CELLS = tuple(
    (left, right, left_colour, right_colour)
    for left, right in EDGES
    for left_colour, right_colour in product(COLOURS, repeat=2)
)
BASE_Q = (
    (2, 3, 0, 0), (4, 5, 0, 0), (6, 7, 0, 0),
    (0, 1, 1, 1), (3, 6, 1, 1), (5, 7, 1, 1),
    (0, 2, 2, 2), (1, 4, 2, 2), (5, 6, 2, 2),
)
DISPLAYED_Z = ((0, 1, 0, 0), (2, 4, 1, 1), (3, 7, 2, 2))
PURE_WORDS = tuple((colour,) * 8 for colour in COLOURS)

TOTAL_QUADRUPLES = 141_722_460
EXPECTED_TRIANGLES = 87_027

MASK_MONOMIAL = {
    1: "t1", 2: "t2", 4: "t3", 8: "t4",
    3: "t1*t2", 5: "t1*t3", 9: "t1*t4",
    6: "t2*t3", 10: "t2*t4", 12: "t3*t4",
    7: "t1*t2*t3", 11: "t1*t2*t4", 13: "t1*t3*t4", 14: "t2*t3*t4",
}


def cells_are_disjoint(cells):
    endpoints = tuple(site for cell in cells for site in cell[:2])
    return len(endpoints) == len(set(endpoints))


def partial_word(cells):
    word = [-1] * 8
    for left, right, left_colour, right_colour in cells:
        assert word[left] == word[right] == -1
        word[left] = left_colour
        word[right] = right_colour
    return tuple(word)


def word_id(word):
    value = 0
    for colour in word:
        assert colour in COLOURS
        value = 3 * value + colour
    return value


def single_debt(extra):
    result = Counter()
    for z_cell in DISPLAYED_Z:
        for pair in combinations(BASE_Q, 2):
            cells = (z_cell, extra) + pair
            if cells_are_disjoint(cells):
                result[partial_word(cells)] += 1
    return result


def cross_debt(left, right):
    result = Counter()
    for z_cell in DISPLAYED_Z:
        for q_cell in BASE_Q:
            cells = (z_cell, left, right, q_cell)
            if cells_are_disjoint(cells):
                result[partial_word(cells)] += 1
    return result


def triple_debt(first, second, third):
    result = Counter()
    for z_cell in DISPLAYED_Z:
        cells = (z_cell, first, second, third)
        if cells_are_disjoint(cells):
            result[partial_word(cells)] += 1
    return result


def build_debts(extras):
    singles = []
    for cell in extras:
        debt = single_debt(cell)
        assert all(coefficient == 1 for coefficient in debt.values())
        singles.append(tuple(sorted(word_id(word) for word in debt)))
    assert Counter(map(len, singles)) == Counter({0: 99, 1: 135, 2: 9})

    crosses = {}
    pair_count = 0
    for i, j in combinations(range(len(extras)), 2):
        pair_count += 1
        debt = cross_debt(extras[i], extras[j])
        assert len(debt) <= 1
        assert all(coefficient == 1 for coefficient in debt.values())
        if debt:
            crosses[i, j] = word_id(next(iter(debt)))
    assert pair_count == 29_403 and len(crosses) == 3_573

    triples = {}
    for i, j, k in combinations(range(len(extras)), 3):
        debt = triple_debt(extras[i], extras[j], extras[k])
        assert len(debt) <= 1
        assert all(coefficient == 1 for coefficient in debt.values())
        if debt:
            triples[i, j, k] = word_id(next(iter(debt)))
    assert len(triples) == 29_076
    return singles, crosses, triples


def quadruple_rows(quad, singles, crosses, triples):
    """Map word-id -> tuple of Laurent monomial masks hitting it."""
    rows = defaultdict(list)
    for position, index in enumerate(quad):
        for word in singles[index]:
            rows[word].append(1 << position)
    for (a, b) in combinations(range(4), 2):
        word = crosses.get((quad[a], quad[b]))
        if word is not None:
            rows[word].append((1 << a) | (1 << b))
    for (a, b, c) in combinations(range(4), 3):
        word = triples.get((quad[a], quad[b], quad[c]))
        if word is not None:
            rows[word].append((1 << a) | (1 << b) | (1 << c))
    return rows


def classify_quadruple(quad, singles, crosses, triples):
    rows = quadruple_rows(quad, singles, crosses, triples)
    if not rows:
        return "compatible", ()
    if any(len(masks) == 1 for masks in rows.values()):
        return "singleton_rejection", ()
    system = tuple(sorted(
        (word, tuple(sorted(masks))) for word, masks in rows.items()
    ))
    return "support_survivor", system


def enumerate_k4s(invisible, crosses):
    """All quadruples of pairwise-compatible invisible cells, via bitsets."""
    adjacency = defaultdict(int)
    members = sorted(invisible)
    for i, j in combinations(members, 2):
        if (i, j) not in crosses:
            adjacency[i] |= 1 << j
            adjacency[j] |= 1 << i
    triangles = 0
    quads = []
    for i in members:
        above_i = adjacency[i] >> (i + 1) << (i + 1)
        mask_j = above_i
        while mask_j:
            j = (mask_j & -mask_j).bit_length() - 1
            mask_j &= mask_j - 1
            common_ij = above_i & adjacency[j]
            mask_k = common_ij >> (j + 1) << (j + 1)
            while mask_k:
                k = (mask_k & -mask_k).bit_length() - 1
                mask_k &= mask_k - 1
                triangles += 1
                mask_l = common_ij & adjacency[k]
                mask_l = mask_l >> (k + 1) << (k + 1)
                while mask_l:
                    l = (mask_l & -mask_l).bit_length() - 1
                    mask_l &= mask_l - 1
                    quads.append((i, j, k, l))
    return triangles, quads


def survivor_candidates(singles, crosses, triples, invisible):
    """Complete candidate set per the anchor lemma plus the invisible scan."""
    n = len(singles)
    word_singles = defaultdict(list)
    for index, words in enumerate(singles):
        for word in words:
            word_singles[word].append(index)
    word_crosses = defaultdict(list)
    for pair, word in crosses.items():
        word_crosses[word].append(pair)
    word_triples = defaultdict(list)
    for triple, word in triples.items():
        word_triples[word].append(triple)

    candidates = set()

    def complete(base_cells):
        base = tuple(sorted(set(base_cells)))
        free = 4 - len(base)
        assert 0 <= free <= 2
        others = [index for index in range(n) if index not in base]
        if free == 0:
            candidates.add(base)
        elif free == 1:
            for extra in others:
                candidates.add(tuple(sorted(base + (extra,))))
        else:
            for extra_pair in combinations(others, 2):
                candidates.add(tuple(sorted(base + extra_pair)))

    for word, anchors in word_singles.items():
        for anchor in anchors:
            for other in anchors:
                if other != anchor:
                    complete((anchor, other))
            for pair in word_crosses.get(word, ()):
                if anchor not in pair:
                    complete((anchor,) + pair)
                else:
                    complete(pair)
            for triple in word_triples.get(word, ()):
                if anchor in triple:
                    complete(triple)
                else:
                    complete((anchor,) + triple)

    invisible_set = sorted(invisible)
    for quad in combinations(invisible_set, 4):
        candidates.add(quad)
    return candidates


def singular_torus_status(systems, executable):
    """Batch-decide torus solvability of the survivor systems over Q."""
    lines = ["ring r=0,(t1,t2,t3,t4,h),dp;"]
    for label, system in systems:
        polys = []
        for _word, masks in system:
            polys.append("+".join(MASK_MONOMIAL[mask] for mask in masks))
        polys.append("h*t1*t2*t3*t4-1")
        lines.append(f"ideal I{label}={','.join(polys)};")
        lines.append(f"ideal G{label}=std(I{label});")
        lines.append(f'print("RESULT {label}");')
        lines.append(f"print(size(G{label}));")
        lines.append(f"print(G{label}[1]);")
    program = "\n".join(lines) + "\n"
    result = subprocess.run(
        [executable, "-q"], input=program, text=True, capture_output=True,
        check=True, timeout=3600,
    )
    assert not result.stderr.strip(), result.stderr
    outputs = {}
    stream = iter(result.stdout.splitlines())
    for line in stream:
        line = line.strip()
        if line.startswith("RESULT "):
            label = int(line.split()[1])
            size = next(stream).strip()
            first = next(stream).strip()
            outputs[label] = (size == "1" and first == "1")
    return outputs


def torus_witness(system):
    """Search a small exact rational witness of the cancellation system."""
    values = (Fraction(1), Fraction(-1), Fraction(2), Fraction(-2),
              Fraction(1, 2), Fraction(-1, 2))
    monomials = {}
    for mask in MASK_MONOMIAL:
        monomials[mask] = [position for position in range(4) if mask >> position & 1]
    for assignment in product(values, repeat=4):
        good = True
        for _word, masks in system:
            total = Fraction(0)
            for mask in masks:
                term = Fraction(1)
                for position in monomials[mask]:
                    term *= assignment[position]
                total += term
            if total:
                good = False
                break
        if good:
            return tuple(str(value) for value in assignment)
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scratch-dir",
        default=os.environ.get("N8_ROUND1_SCRATCH", "/tmp"),
        help="directory for the large compatible-quadruple ledger",
    )
    parser.add_argument("--skip-singular", action="store_true")
    args = parser.parse_args()

    assert len(ALL_CELLS) == 252
    extras = tuple(cell for cell in ALL_CELLS if cell not in BASE_Q)
    assert len(extras) == 243

    base_expansion = Counter()
    for z_cell in DISPLAYED_Z:
        for triple in combinations(BASE_Q, 3):
            cells = (z_cell,) + triple
            if cells_are_disjoint(cells):
                base_expansion[partial_word(cells)] += 1
    assert base_expansion == Counter({word: 1 for word in PURE_WORDS})

    singles, crosses, triples = build_debts(extras)
    invisible = tuple(index for index, words in enumerate(singles) if not words)
    assert len(invisible) == 99
    invisible_pairs = {cell[:2] for index in invisible for cell in (extras[index],)}
    assert invisible_pairs == {
        (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (1, 2),
        (1, 3), (1, 5), (1, 7), (2, 5), (3, 4),
    }

    # No triple of pairwise-compatible invisible cells has nonzero triple
    # debt, so every K4 of the compatibility graph is fully compatible.
    invisible_set = set(invisible)
    for (i, j, k) in triples:
        if i in invisible_set and j in invisible_set and k in invisible_set:
            assert (i, j) in crosses or (i, k) in crosses or (j, k) in crosses

    triangles, compatible_quads = enumerate_k4s(invisible, crosses)
    assert triangles == EXPECTED_TRIANGLES
    compatible_quads.sort()

    candidates = survivor_candidates(singles, crosses, triples, invisible)
    survivors = []
    candidate_compatible = 0
    for quad in sorted(candidates):
        kind, system = classify_quadruple(quad, singles, crosses, triples)
        if kind == "support_survivor":
            survivors.append((quad, system))
        elif kind == "compatible":
            candidate_compatible += 1
    # The invisible scan sees every compatible quadruple exactly once.
    assert candidate_compatible == len(compatible_quads)

    # Cross-check the graph enumeration against the direct invisible scan.
    direct_compatible = sum(
        1 for quad in compatible_quads
        if classify_quadruple(quad, singles, crosses, triples)[0] == "compatible"
    )
    assert direct_compatible == len(compatible_quads)

    survivor_digest = hashlib.sha256()
    for quad, system in survivors:
        survivor_digest.update(repr((quad, system)).encode())
        survivor_digest.update(b"\n")

    compatible_digest = hashlib.sha256()
    for quad in compatible_quads:
        compatible_digest.update(repr(quad).encode())
        compatible_digest.update(b"\n")

    executable = shutil.which("Singular")
    torus_results = {}
    if not args.skip_singular:
        assert executable is not None, "Singular is required for torus decisions"
        labelled = [(index, system) for index, (_quad, system) in enumerate(survivors)]
        for start in range(0, len(labelled), 200):
            torus_results.update(
                singular_torus_status(labelled[start:start + 200], executable)
            )

    def equation_shape(masks):
        degrees = tuple(sorted(bin(mask).count("1") for mask in masks))
        if len(masks) == 2:
            low, high = sorted(masks, key=lambda mask: bin(mask).count("1"))
            if low & high == low:
                return degrees, "nested"
            return degrees, "disjoint" if low & high == 0 else "overlap"
        return degrees, "other"

    records = []
    status_counter = Counter()
    relation_counter = Counter()
    for index, (quad, system) in enumerate(survivors):
        if args.skip_singular:
            status = "undecided"
            witness = None
        else:
            unit = torus_results[index]
            status = "torus_inconsistent" if unit else "cancellation_family"
            witness = None if unit else torus_witness(system)
            assert unit or witness is not None
        status_counter[status] += 1
        if status == "cancellation_family":
            relation_counter[
                tuple(sorted(equation_shape(masks) for _word, masks in system))
            ] += 1
        records.append({
            "cells": [list(extras[index_]) for index_ in quad],
            "indices": list(quad),
            "system": [
                {"word": word, "masks": list(masks)} for word, masks in system
            ],
            "status": status,
            "witness": witness,
        })

    singleton_count = (
        TOTAL_QUADRUPLES - len(compatible_quads) - len(survivors)
    )
    summary = {
        "region": "Q = q + t1*e1 + t2*e2 + t3*e3 + t4*e4, distinct cells outside supp(q), t in (C^*)^4",
        "seed_q": [list(cell) for cell in BASE_Q],
        "seed_z": [list(cell) for cell in DISPLAYED_Z],
        "total_quadruples": TOTAL_QUADRUPLES,
        "compatible_quadruples": len(compatible_quads),
        "compatibility_triangles": triangles,
        "singleton_rejections": singleton_count,
        "support_survivors": len(survivors),
        "survivor_status_counts": dict(status_counter),
        "cancellation_relation_histogram": {
            repr(shape): count for shape, count in sorted(relation_counter.items())
        },
        "survivor_sha256": survivor_digest.hexdigest(),
        "compatible_sha256": compatible_digest.hexdigest(),
        "torus_inconsistent_quadruples": [
            record["cells"] for record in records
            if record["status"] == "torus_inconsistent"
        ],
        "representative_survivors": records[:3],
    }

    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "search_n8_varied_q_round_1_survivors.json"), "w") as handle:
        json.dump(summary, handle, indent=1)
        handle.write("\n")

    os.makedirs(args.scratch_dir, exist_ok=True)
    ledger_path = os.path.join(args.scratch_dir, "n8_round1_compatible_quads.txt")
    with open(ledger_path, "w") as handle:
        for quad in compatible_quads:
            handle.write("%d %d %d %d\n" % quad)
    full_path = os.path.join(args.scratch_dir, "n8_round1_survivors_full.json")
    with open(full_path, "w") as handle:
        json.dump(records, handle)
        handle.write("\n")

    print("four-extra-cell varied-q census: PASS")
    print("total quadruples:", TOTAL_QUADRUPLES)
    print("compatible quadruples (K4):", len(compatible_quads))
    print("compatibility triangles:", triangles)
    print("support survivors:", len(survivors))
    print("survivor statuses:", dict(status_counter))
    print("singleton rejections (derived):", singleton_count)
    print("cancellation relation histogram:")
    for shape, count in sorted(relation_counter.items()):
        print("  ", shape, count)
    print("survivor sha256:", survivor_digest.hexdigest())
    print("compatible sha256:", compatible_digest.hexdigest())
    print("compatible ledger written to:", ledger_path)
    print("full survivor ledger written to:", full_path)


if __name__ == "__main__":
    main()
