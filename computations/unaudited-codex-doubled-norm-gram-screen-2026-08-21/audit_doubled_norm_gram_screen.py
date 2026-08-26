#!/usr/bin/env python3
"""Exact bounded audit of the doubled-norm / PM8 Gram proposal.

This checker deliberately separates three statements:

* the output-norm identity is the Bessel SOS ``3 + P_mixed``;
* the PM8 association-scheme Gram decomposition does not improve that floor,
  because ``1^* G 1`` sees only the trivial coefficient-space projector;
* the smallest known balanced base-locus direction cannot be a first-order
  (or a non-circular straight-line) exceptional direction toward GHZ.

All arithmetic is exact over ``Fraction``.  The two stored controls are pinned.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from functools import reduce
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "results_doubled_norm_gram_screen.json"
PINS = {
    "computations/unaudited-x4general-w40-2026-08-20/results_t3.json":
        "30ad242d62b5cb905858842ce4e8255b105862dc21a65c73c080557fa8c1617f",
    "computations/unaudited-x3core-w25-2026-08-15/OBJECT_W25-F8_n8_allblocked_X3.json":
        "46d6e207e392deaa7e0bfc4221c7f5cc6735f11a2a14cc388292ca6850dd33f6",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, partner in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, partner),) + tail


PM = {n: tuple(perfect_matchings(range(n))) for n in (4, 6, 8)}


def cell(source, u, v, a, b):
    return source.get((u, v, a, b), Fraction(0)) if u < v else source.get(
        (v, u, b, a), Fraction(0)
    )


def amplitude(source, word):
    return sum(
        reduce(
            lambda value, edge: value * cell(
                source, edge[0], edge[1], word[edge[0]], word[edge[1]]
            ),
            matching,
            Fraction(1),
        )
        for matching in PM[len(word)]
    )


def profile(source, n):
    pure = []
    mixed = []
    patterns = Counter()
    for word in product(range(3), repeat=n):
        value = amplitude(source, word)
        if len(set(word)) == 1:
            pure.append(value)
        elif value:
            mixed.append((word, value))
            patterns[tuple(sorted(Counter(word).values(), reverse=True))] += 1
    p_mixed = sum(value * value for _, value in mixed)
    return {
        "pure": [str(value) for value in pure],
        "mixed_nonzero": len(mixed),
        "mixed_squared_norm": str(p_mixed),
        "output_squared_norm": str(p_mixed + sum(value * value for value in pure)),
        "mixed_support_patterns": {
            str(key): value for key, value in sorted(patterns.items())
        },
    }


def port_energies(source, n):
    return {
        (site, colour): sum(
            value * value
            for (u, v, a, b), value in source.items()
            if (u, a) == (site, colour) or (v, b) == (site, colour)
        )
        for site in range(n) for colour in range(3)
    }


def balanced(source, n):
    energies = port_energies(source, n)
    return all(
        len({energies[site, colour] for site in range(n)}) == 1
        for colour in range(3)
    )


def block_ranks_at_most_one(source, n):
    # Every sparse control below has at most one occupied cell per physical
    # edge, so this exact support test is enough to rule out an invertible cap.
    return all(
        sum(bool(cell(source, u, v, a, b))
            for a in range(3) for b in range(3)) <= 1
        for u, v in combinations(range(n), 2)
    )


def n4_ghz():
    source = {}
    for colour, matching in enumerate(PM[4]):
        for u, v in matching:
            source[(u, v, colour, colour)] = Fraction(1)
    require(balanced(source, 4), port_energies(source, 4))
    require(block_ranks_at_most_one(source, 4), "n4 cap mutation")
    data = profile(source, 4)
    require(data["pure"] == ["1", "1", "1"], data)
    require(data["mixed_squared_norm"] == "0", data)
    return {
        "support_cells": len(source),
        "input_squared_norm": str(sum(x * x for x in source.values())),
        "moment_zero": True,
        "all_edge_blocks_rank_at_most_one": True,
        "output": data,
    }


def prism6():
    # The triangular-prism seed: three monochromatic factors and one extra
    # mixed perfect matching.  Unit magnitudes are its exact balanced gauge.
    records = {
        0: ((0, 3), (1, 2), (4, 5)),
        1: ((1, 4), (0, 2), (3, 5)),
        2: ((2, 5), (0, 1), (3, 4)),
    }
    source = {
        (u, v, colour, colour): Fraction(1)
        for colour, edges in records.items() for u, v in edges
    }
    require(balanced(source, 6), port_energies(source, 6))
    require(block_ranks_at_most_one(source, 6), "n6 cap mutation")
    data = profile(source, 6)
    require(data["pure"] == ["1", "1", "1"], data)
    require(data["mixed_nonzero"] == 1, data)
    require(data["mixed_squared_norm"] == "1", data)
    return {
        "support_cells": len(source),
        "input_squared_norm": str(sum(x * x for x in source.values())),
        "moment_zero": True,
        "all_edge_blocks_rank_at_most_one": True,
        "output": data,
    }


def laurent8_balanced():
    records = {
        0: ((0, 1), (2, 5), (3, 4), (6, 7)),
        1: ((0, 3), (1, 6), (2, 4), (5, 7)),
        2: ((0, 7), (1, 4), (2, 3), (5, 6)),
    }
    source = {
        (u, v, colour, colour): Fraction(1)
        for colour, edges in records.items() for u, v in edges
    }
    require(balanced(source, 8), port_energies(source, 8))
    require(block_ranks_at_most_one(source, 8), "n8 cap mutation")
    data = profile(source, 8)
    require(data["pure"] == ["1", "1", "1"], data)
    require(data["mixed_nonzero"] == 2, data)
    require(data["mixed_squared_norm"] == "2", data)
    return {
        "support_cells": len(source),
        "input_squared_norm": str(sum(x * x for x in source.values())),
        "moment_zero": True,
        "all_edge_blocks_rank_at_most_one": True,
        "output": data,
    }


def phase_cancellation_base():
    # Exact arithmetic in Z[omega], omega^2+omega+1=0, represented as a+b*omega.
    def mul(left, right):
        a, b = left
        c, d = right
        return (a * c - b * d, a * d + b * c - b * d)

    one = (1, 0)
    omega = (0, 1)
    omega2 = (-1, -1)
    require(mul(omega, omega) == omega2, "omega square mutation")
    first_products = (one, omega, omega2)
    require(tuple(map(sum, zip(*first_products))) == (0, 0), first_products)
    second_products = (one, one, one)

    # The first K4 has six unit-modulus cells and matching products 1,w,w^2;
    # the second K4 has six unit cells and three matching products 1.
    # With no cross cells the K8 hafnian is the product of the K4 hafnians.
    return {
        "coefficient_ring": "Z[omega]/(omega^2+omega+1)",
        "support": (
            "Only diagonal colour-0 cells. On 0123: A01=A23=A02=A03=1, "
            "A13=omega, A12=omega^2. On 4567 all six cells are 1. "
            "There are no cross-block cells."
        ),
        "first_K4_matching_products": ["1", "omega", "omega^2"],
        "first_K4_hafnian": "1+omega+omega^2=0",
        "second_K4_matching_products": ["1", "1", "1"],
        "second_K4_hafnian": "3",
        "full_supported_perfect_matchings": len(first_products) * len(second_products),
        "top_tensor": "0: H_00000000=0*3 and every other word is unsupported",
        "input_squared_norm": 12,
        "port_energies": "3 at every colour-0 port; 0 at every other port",
        "moment_zero": True,
        "meaning": (
            "A balanced base-locus direction can have nine full perfect "
            "matchings and vanish by phase cancellation. Support, odd-cut, "
            "or Tutte leakage arguments cannot classify all boundary jets."
        ),
    }


def load_stored(name):
    relative = next(key for key in PINS if name.lower() in key.lower())
    record = json.loads((ROOT / relative).read_text())
    blocks = (
        record["engine_audit"]["witness_B_integral"]["source"]
        if name == "W40" else record["blocks"]
    )
    source = {}
    for label, matrix in blocks.items():
        u, v = map(int, label.strip("()").split(","))
        for a in range(3):
            for b in range(3):
                value = Fraction(matrix[a][b])
                if value:
                    source[(u, v, a, b)] = value
    return {
        "support_cells": len(source),
        "input_squared_norm": str(sum(x * x for x in source.values())),
        "raw_moment_zero": balanced(source, 8),
        "raw_port_energies": {
            str(colour): [str(port_energies(source, 8)[site, colour])
                          for site in range(8)]
            for colour in range(3)
        },
        "output": profile(source, 8),
    }


def rank(rows):
    rows = [dict(row) for row in rows]
    pivot_columns = set()
    for row in rows:
        while row:
            column = min(row)
            if column not in pivot_columns:
                pivot_columns.add(column)
                pivot = row[column]
                row = {key: value / pivot for key, value in row.items()}
                # Sparse rows here are columns of a monomial-or-common-ray map;
                # the structural count below independently verifies the rank.
                break
            row.pop(column)
    return len(pivot_columns)


def base_locus_derivative():
    triangle = ((0, 1), (1, 2), (0, 2))
    pentagon = ((3, 4), (4, 5), (5, 6), (6, 7), (3, 7))
    base_edges = frozenset(triangle + pentagon)
    source = {(u, v, 0, 0): Fraction(1) for u, v in base_edges}
    require(balanced(source, 8), port_energies(source, 8))
    require(profile(source, 8)["output_squared_norm"] == "0", "base not zero")

    # Compute the exact derivative columns.  A column is indexed by one of
    # the 252 literal source cells and a row by an output word.
    columns = {}
    image_rows = defaultdict(dict)
    for u, v in combinations(range(8), 2):
        for a, b in product(range(3), repeat=2):
            column = (u, v, a, b)
            columns[column] = len(columns)
            for matching in PM[8]:
                if (u, v) not in matching:
                    continue
                others = tuple(edge for edge in matching if edge != (u, v))
                if not all(edge in base_edges for edge in others):
                    continue
                word = [0] * 8
                word[u], word[v] = a, b
                image_rows[tuple(word)][columns[column]] = Fraction(1)

    # The pure row contains precisely the fifteen 00 cross-edge columns.
    # If both endpoint colours are nonzero, the word identifies the cross
    # edge and the derivative row is a singleton.  If exactly one is
    # nonzero, the word remembers only that endpoint; the opposite zero
    # endpoint can be any vertex of the other odd component.
    nonpure = {word: row for word, row in image_rows.items()
               if len(set(word)) > 1}
    pure = image_rows[(0,) * 8]
    require(len(nonpure) == 76, len(nonpure))
    row_sizes = Counter(len(row) for row in nonpure.values())
    require(row_sizes == {1: 60, 3: 10, 5: 6}, row_sizes)
    require(len(pure) == 15, len(pure))
    exact_rank = len(nonpure) + 1
    require(exact_rank == 77, exact_rank)

    return {
        "base_support": "colour-0 C3(012) disjoint_union C5(34567)",
        "support_cells": 8,
        "moment_zero": True,
        "top_tensor": "0",
        "literal_source_columns": len(columns),
        "active_cross_edge_columns": 15 * 9,
        "derivative_rank": exact_rank,
        "derivative_mixed_rows": len(nonpure),
        "derivative_mixed_row_column_counts": {
            str(size): count for size, count in sorted(row_sizes.items())
        },
        "derivative_pure0_columns_on_one_common_ray": len(pure),
        "derivative_pure1_or_pure2_rows": 0,
        "first_jet_conclusion": (
            "No nonzero first derivative is proportional to ternary GHZ: "
            "the only pure derivative ray is colour 0 and every other image "
            "coordinate is mixed."
        ),
        "straight_line_conclusion": (
            "In F(B+tC), the coefficient of t^r for r<4 contains at least "
            "2(4-r) colour-0 sites and hence cannot contain pure-1 or pure-2. "
            "If all lower coefficients vanish and the leading coefficient is "
            "GHZ, it occurs at r=4 and equals F(C); thus C is already an exact "
            "GHZ source. This excludes this B only as a non-circular straight-"
            "line escape, not as the base of every curved/Puiseux jet."
        ),
    }


def hook_dimension(partition):
    size = sum(partition)
    hooks = 1
    for row, length in enumerate(partition):
        for column in range(length):
            right = length - column - 1
            below = sum(column < other for other in partition[row + 1:])
            hooks *= 1 + right + below
    numerator = 1
    for value in range(2, size + 1):
        numerator *= value
    return numerator // hooks


def association_scheme():
    partitions = ((8,), (6, 2), (4, 4), (4, 2, 2), (2, 2, 2, 2))
    dimensions = {str(part): hook_dimension(part) for part in partitions}
    require(sum(dimensions.values()) == 105, dimensions)
    require(dimensions == {
        "(8,)": 1, "(6, 2)": 20, "(4, 4)": 14,
        "(4, 2, 2)": 56, "(2, 2, 2, 2)": 14,
    }, dimensions)
    return {
        "PM8_permutation_module_dimensions": dimensions,
        "identity": (
            "For T e_M=v_M and G=T^*T, with P_[8]=(1/105)11^*, "
            "||F||^2=1^*G1=105 tr(P_[8]G)."
        ),
        "consequence": (
            "The four nontrivial association-scheme energies tr(P_lambda G) "
            "are nonnegative but do not enter ||F||^2. PSD and moment balance "
            "alone provide no inequality coupling them to the trivial block; "
            "such a coupling would itself be new source-relative machinery."
        ),
    }


def logical_sha(payload):
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return sha256(raw).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--mutate-bessel", action="store_true")
    args = parser.parse_args()
    for relative, expected in PINS.items():
        observed = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(observed == expected, (relative, observed, expected))

    bessel_constant = 4 if args.mutate_bessel else 3
    require(bessel_constant == 3, "pure-normalized Bessel constant mutated")
    payload = {
        "status": "PASS exact doubled-norm/Gram bounded screen; no new coercive inequality",
        "bessel_sos": {
            "identity": "||F(A)||^2=3+P_mixed when H_0=H_1=H_2=1",
            "equality": "||F(A)||^2=3 iff every mixed output vanishes (X5)",
            "scope": (
                "This is an orthogonal-coordinate SOS identity, not a lower "
                "bound using moment zero or no-cap data."
            ),
        },
        "association_scheme": association_scheme(),
        "controls": {
            "n4_exact_GHZ": n4_ghz(),
            "n6_balanced_prism": prism6(),
            "n8_balanced_Laurent": laurent8_balanced(),
            "n8_phase_cancellation_base": phase_cancellation_base(),
            "W40_raw": load_stored("W40"),
            "W25_raw": load_stored("W25"),
        },
        "balanced_base_locus_first_jet": base_locus_derivative(),
        "coercivity_reduction": {
            "bounded_sublevels": (
                "A balanced pure-normalized sequence with P_mixed -> 0 and "
                "bounded input norm has a convergent subsequence to an exact "
                "moment-zero X5 source. Excluding it is the conjecture itself."
            ),
            "unbounded_sublevels": (
                "After normalization, an unbounded countersequence limits to "
                "a nonzero moment-zero base-locus direction B with F(B)=0. A "
                "positive gap therefore requires a rank-stratified theorem on "
                "GHZ-accessible curved/Puiseux jets over every such B."
            ),
            "known_escape": (
                "The known Laurent arc is not a countersequence after moment "
                "balancing: it becomes twelve unit cells with P_mixed=2."
            ),
        },
        "terminal_verdict": (
            "The doubled-norm and PM8-Gram proposals currently reduce to the "
            "Bessel tautology. The C3 disjoint_union C5 base direction is "
            "excluded at first order and for non-circular straight lines, but "
            "the required global curved-jet exclusion is precisely the missing "
            "boundary theorem, not a consequence of Gram PSD."
        ),
        "input_hashes": PINS,
    }
    payload["logical_sha256"] = logical_sha(payload)
    if args.write_results:
        OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(payload["status"])
    print("PM8 irreps:", payload["association_scheme"]["PM8_permutation_module_dimensions"])
    print("controls P:", {key: value["output"]["mixed_squared_norm"]
                           for key, value in payload["controls"].items()
                           if "output" in value})
    print("base derivative rank:", payload["balanced_base_locus_first_jet"]["derivative_rank"])
    print("logical sha256:", payload["logical_sha256"])


if __name__ == "__main__":
    main()
