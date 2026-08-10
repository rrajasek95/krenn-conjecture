#!/usr/bin/env python3
"""Exact sparse frontier for the target-free residual-pure branch.

Start from the five-cell Pythagorean common power on five sites and adjoin
at most four nonzero endpoint-coloured cells.  On every support whose old
and new cell characters are independent, the local diagonal torus
normalizes all new coefficients to one.  We exhaust the supports with a
nonzero all-target four-site cofactor.  Exact rational linear algebra then
shows that retaining both old pure images always makes the common-cofactor
map injective, so its target-free residual is zero.

The checker also audits the source-level leading-colour lemma: without an
all-target cofactor the raw pure-target functional separates immediately;
and every target-free cofactor-kernel row is supported on the zero set of
the all-target cofactor vector.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
import itertools
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "computations"))

import search_shared_reciprocal_two_bad_target_free_residual_two_cell as mod


EXPECTED_SEARCH_SHA256 = (
    "e3397dfb7004e1a9ff8d8569ca13c0a50262c7a4536962bcccf451ab47dca38e"
)
EXPECTED_LEDGER_SHA256 = (
    "969f695da1d0bb7baeca303f425594050e6b38186b13d2f32bc5ded456f6054b"
)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def add_cell(cells, u, v, left, right, value):
    if u > v:
        u, v = v, u
        left, right = right, left
    key = ((u, v), left, right)
    cells[key] = cells.get(key, Fraction(0)) + value
    if not cells[key]:
        del cells[key]


def cofactor(cells, hole):
    vertices = tuple(site for site in mod.SITES if site != hole)
    out = defaultdict(Fraction)
    for matching in mod.perfect_matchings(vertices):
        choices = []
        for edge in matching:
            entries = [
                (left, right, value)
                for (candidate, left, right), value in cells.items()
                if candidate == edge
            ]
            if not entries:
                break
            choices.append(entries)
        else:
            for selected in itertools.product(*choices):
                colours = {}
                coefficient = Fraction(1)
                for edge, (left, right, value) in zip(matching, selected):
                    colours[edge[0]] = left
                    colours[edge[1]] = right
                    coefficient *= value
                word = tuple(colours[site] for site in vertices)
                out[word] += coefficient
    return {word: value for word, value in out.items() if value}


def phi_columns(cells):
    columns = []
    cofactors = {hole: cofactor(cells, hole) for hole in mod.SITES}
    for hole, inserted_colour in mod.LABELS:
        vertices = tuple(site for site in mod.SITES if site != hole)
        column = {}
        for word, value in cofactors[hole].items():
            colours = dict(zip(vertices, word))
            colours[hole] = inserted_colour
            row = mod.WORD_INDEX[tuple(colours[site] for site in mod.SITES)]
            column[row] = value
        columns.append(column)
    return columns, cofactors


def reduce_column(column, pivots):
    column = dict(column)
    while column:
        row = min(column)
        if row not in pivots:
            break
        factor = column[row]
        for other_row, value in pivots[row].items():
            updated = column.get(other_row, Fraction(0)) - factor * value
            if updated:
                column[other_row] = updated
            else:
                column.pop(other_row, None)
    return column


def add_to_basis(column, pivots):
    column = reduce_column(column, pivots)
    if not column:
        return False
    row = min(column)
    scalar = Fraction(1, 1) / column[row]
    pivots[row] = {other_row: value * scalar
                   for other_row, value in column.items()}
    return True


def rank_and_pure_images(cells):
    columns, cofactors = phi_columns(cells)
    pivots = {}
    for column in columns:
        add_to_basis(column, pivots)
    pure_images = tuple(
        not reduce_column({mod.WORD_INDEX[(colour,) * 5]: Fraction(1)}, pivots)
        for colour in (0, 1)
    )
    return len(pivots), pure_images, cofactors


def character_rank(keys):
    # Rank is enough over C: a full-row-rank monomial map of algebraic tori
    # is surjective, since all required roots exist.
    pivots = {}
    for edge, left, right in keys:
        column = {
            3 * edge[0] + left: Fraction(1),
            3 * edge[1] + right: Fraction(1),
        }
        add_to_basis(column, pivots)
    return len(pivots)


def base_cells():
    cells = {}
    for u, v, colour, value in (
        (1, 2, 0, Fraction(3, 5)),
        (0, 2, 0, Fraction(4, 5)),
        (3, 4, 0, Fraction(1)),
        (0, 1, 1, Fraction(1)),
        (2, 3, 1, Fraction(1)),
    ):
        add_cell(cells, u, v, colour, colour, value)
    return cells


def all_target_matching(selected):
    edges = {
        key[0] for key in selected
        if key[1:] == (mod.TARGET, mod.TARGET)
    }
    return any(set(left).isdisjoint(right)
               for left, right in itertools.combinations(edges, 2))


def audit_leading_colour_lemma():
    # In Phi(N), where every inserted N_x has zero target coordinate, the
    # word with one non-target colour b at x and target everywhere else has
    # exactly one possible insertion site: x.  Its coefficient is N_x,b*k_x.
    # This combinatorial uniqueness is audited over every x,b and every
    # possible insertion site.
    uniqueness = []
    for x in mod.SITES:
        for b in range(2):
            defect = tuple(b if site == x else mod.TARGET
                           for site in mod.SITES)
            possible = []
            for hole, inserted_colour in mod.LABELS:
                if inserted_colour == mod.TARGET:
                    continue
                if inserted_colour == defect[hole]:
                    possible.append((hole, inserted_colour))
            require(possible == [(x, b)],
                    "one-defect target-free insertion ceased to be unique")
            uniqueness.append((x, b))
    require(len(uniqueness) == 10, "leading-colour audit changed")
    return {
        "all_target_cofactor": "k_x=[t^(C\\x)] H_(C\\x)(q)",
        "raw_separator": (
            "if k=0, raw [t^C] annihilates im(Phi) and every P*N*K*q"
        ),
        "kernel_support": "N in ker(Phi), pi_t(N)=0 => k_x*N_x=0",
        "audited_one_defect_coefficients": len(uniqueness),
    }


def audit_sparse_frontier():
    base = base_cells()
    base_keys = tuple(base)
    all_cells = tuple(
        ((u, v), left, right)
        for u, v in itertools.combinations(mod.SITES, 2)
        for left, right in itertools.product(range(3), repeat=2)
    )
    candidates = tuple(key for key in all_cells if key not in base)
    require(len(candidates) == 85, "candidate-cell census changed")

    ledger = {}
    retained_examples = []
    for added in (2, 3, 4):
        all_target_supports = 0
        dependent_supports = 0
        independent_supports = 0
        pure_retained = 0
        retained_ranks = Counter()
        for selected in itertools.combinations(candidates, added):
            if not all_target_matching(selected):
                continue
            all_target_supports += 1
            if character_rank(base_keys + selected) != len(base_keys) + added:
                dependent_supports += 1
                continue
            independent_supports += 1
            cells = dict(base)
            for edge, left, right in selected:
                add_cell(cells, *edge, left, right, Fraction(1))
            rank, pure_images, cofactors = rank_and_pure_images(cells)
            # The support filter must really produce a nonzero all-target
            # cofactor after exact rational cancellation.
            k = tuple(cofactors[x].get((mod.TARGET,) * 4, Fraction(0))
                      for x in mod.SITES)
            require(any(k), "target matching cancelled from every cofactor")
            if pure_images == (True, True):
                pure_retained += 1
                retained_ranks[rank] += 1
                if len(retained_examples) < 8:
                    retained_examples.append({
                        "added": added,
                        "cells": selected,
                        "rank": rank,
                        "k_support": tuple(i for i, value in enumerate(k)
                                           if value),
                    })
        require(all_target_supports == {2: 15, 3: 1215, 4: 48580}[added],
                f"all-target support census changed at {added}")
        require(dependent_supports == {2: 0, 3: 0, 4: 525}[added],
                f"dependent support census changed at {added}")
        require(pure_retained == {2: 0, 3: 4, 4: 46}[added],
                f"pure-image retention changed at {added}")
        require(retained_ranks == ({15: pure_retained} if pure_retained else {}),
                f"a retained sparse chart ceased to be injective at {added}")
        ledger[str(added)] = {
            "all_target_supports": all_target_supports,
            "torus_independent_supports": independent_supports,
            "excluded_dependent_supports": dependent_supports,
            "retain_X0_X1": pure_retained,
            "retained_phi_ranks": dict(sorted(retained_ranks.items())),
            "residual_pure_hits": 0,
        }
    return {
        "base_cells": len(base),
        "candidate_cells": len(candidates),
        "frontier": ledger,
        "retained_examples": retained_examples,
        "scope": (
            "Pythagorean base plus 2..4 nonzero new cells, with independent "
            "combined site-colour characters and nonzero all-target cofactor"
        ),
        "verdict": (
            "every chart retaining X0,X1 has rank(Phi)=15; hence K=N=R_nt=0"
        ),
        "excluded_scope": (
            "525 character-dependent four-cell supports, five-or-more-cell "
            "deformations, and other binary common-power components"
        ),
    }


def audit_singular_k_guard():
    # Three edge-disjoint four-site matchings, leaving holes 0, 4, and 2,
    # carry colours 0, 1, and t respectively.  The union has no additional
    # matching at holes 0 or 4, so their cofactors are exactly pure.  This
    # is the smallest literal guard showing that nonzero singular k is
    # compatible with both old pure images; the missing ingredient is N.
    cells = {}
    for u, v, colour in (
        (1, 2, 0), (3, 4, 0),
        (0, 1, 1), (2, 3, 1),
        (0, 4, 2), (1, 3, 2),
    ):
        add_cell(cells, u, v, colour, colour, Fraction(1))
    rank, pure_images, cofactors = rank_and_pure_images(cells)
    k = tuple(cofactors[x].get((mod.TARGET,) * 4, Fraction(0))
              for x in mod.SITES)
    require(pure_images == (True, True),
            "singular-k guard lost an old pure image")
    require(k == (0, 0, 1, 0, 0),
            "singular-k guard cofactor vector changed")
    require(rank == 15, "singular-k guard ceased to be injective")

    # The restricted target-free insertion map on Z(k) has two columns per
    # hole.  Full rank shows explicitly that a large zero set of k alone
    # does not produce N.
    columns, _ = phi_columns(cells)
    zero_set = tuple(x for x, value in enumerate(k) if not value)
    restricted = [columns[mod.LABELS.index((x, colour))]
                  for x in zero_set for colour in (0, 1)]
    pivots = {}
    for column in restricted:
        add_to_basis(column, pivots)
    require(len(pivots) == 2 * len(zero_set) == 8,
            "restricted zero-set cofactor map acquired a kernel")
    return {
        "cells": 6,
        "pure_images": ["X0", "X1"],
        "Xt_in_image": False,
        "k": [int(value) for value in k],
        "zero_set_size": len(zero_set),
        "restricted_target_free_columns": len(restricted),
        "restricted_target_free_rank": len(pivots),
        "phi_rank": rank,
        "verdict": (
            "singular nonzero k is compatible with both pure images; "
            "a separate cofactor-syzygy rank defect is load-bearing"
        ),
    }


def main():
    actual = sha256((ROOT / "computations" /
                     "search_shared_reciprocal_two_bad_target_free_residual_two_cell.py").read_bytes()).hexdigest()
    require(EXPECTED_SEARCH_SHA256 == "TO_BE_FILLED" or
            actual == EXPECTED_SEARCH_SHA256,
            f"search dependency changed: {actual}")
    result = {
        "leading_colour": audit_leading_colour_lemma(),
        "sparse_frontier": audit_sparse_frontier(),
        "singular_k_guard": audit_singular_k_guard(),
    }
    payload = json.dumps(result, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("ledger_sha256", digest)
    require(EXPECTED_LEDGER_SHA256 == "TO_BE_FILLED" or
            digest == EXPECTED_LEDGER_SHA256,
            f"ledger changed: {digest}")


if __name__ == "__main__":
    main()
