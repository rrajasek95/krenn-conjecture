#!/usr/bin/env python3
"""Exact literal-X4 closure of the 129-cell open m=25 support.

UNAUDITED.  This file deliberately rebuilds the support, the 105 perfect
matchings, and every row polynomial from the raw 28-entry endpoint mask.  It
does not import any of the older W8/W15/W24 engines.

The proof uses two families of three rows obtained by varying the colour at
site 6.  An isolated (0,6) singleton packet forces the 01 minor of the two
full blocks A56,A67 to vanish.  An isolated (2,6) singleton packet at the
same (y5,y7), together with that minor, is a Laurent-unit contradiction.

The output is deterministic in standard, ``-O``, and ``-I -S`` modes.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import os
import sys
from collections import Counter
from functools import lru_cache


HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "results_m25_x4_closure.json")

N = 8
COLORS = range(3)
EDGES = tuple(itertools.combinations(range(N), 2))

# Raw endpoint ordering: the i-th entry belongs to EDGES[i], and bit 3*a+b
# is the cell whose colour at the smaller endpoint is a and at the larger
# endpoint is b.
RAW_M25 = (
    511, 511, 511, 1, 2, 4, 511, 511, 511, 511, 8, 16, 4, 511,
    8, 511, 128, 32, 64, 128, 0, 256, 511, 0, 511, 511, 0, 511,
)

TEMPLATES = {
    25: RAW_M25,
    26: (511, 511, 511, 1, 2, 4, 511, 511, 511, 511, 8, 16, 4,
         511, 8, 511, 128, 32, 64, 128, 511, 256, 511, 0, 511, 511, 0,
         511),
    27: (511, 511, 511, 1, 2, 4, 511, 511, 511, 511, 8, 16, 4,
         511, 8, 511, 128, 32, 64, 128, 511, 256, 511, 511, 511, 511,
         0, 511),
    28: (511, 511, 511, 1, 2, 4, 511, 511, 511, 511, 8, 16, 4,
         511, 8, 511, 128, 32, 64, 128, 511, 256, 511, 511, 511, 511,
         511, 511),
}


def require(condition, message):
    """Optimization-invariant replacement for assert-based audit checks."""
    if not condition:
        raise RuntimeError(message)


def cell_name(u: int, v: int, a: int, b: int) -> str:
    return f"x{u}{v}_{a}{b}"


def decode(raw=RAW_M25, transpose=False):
    support = {}
    for edge, mask in zip(EDGES, raw):
        cells = set()
        for a in COLORS:
            for b in COLORS:
                bit = 3 * b + a if transpose else 3 * a + b
                if mask & (1 << bit):
                    cells.add((a, b))
        support[edge] = cells
    return support


SUPPORT = decode()
FULL = {e for e in EDGES if len(SUPPORT[e]) == 9}
SINGLE = {e: next(iter(SUPPORT[e])) for e in EDGES if len(SUPPORT[e]) == 1}
MISSING = {e for e in EDGES if not SUPPORT[e]}


@lru_cache(None)
def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        return ((),)
    u = vertices[0]
    out = []
    for i in range(1, len(vertices)):
        v = vertices[i]
        rest = vertices[1:i] + vertices[i + 1:]
        for tail in perfect_matchings(rest):
            out.append(((u, v),) + tail)
    return tuple(out)


PM8 = perfect_matchings(tuple(range(N)))


def monomial(cells):
    return tuple(sorted(cell_name(*c) for c in cells))


def row_poly(word: tuple[int, ...], support=SUPPORT):
    """Sparse polynomial H_word as {monomial: integer coefficient}."""
    out = Counter()
    for matching in PM8:
        cells = []
        for u, v in matching:
            a, b = word[u], word[v]
            if (a, b) not in support[(u, v)]:
                break
            cells.append((u, v, a, b))
        else:
            out[monomial(cells)] += 1
    return dict(out)


def mixed_x4(word):
    return len(set(word)) > 1 and max(word.count(c) for c in COLORS) >= 4


def all_x4(word):
    return max(word.count(c) for c in COLORS) >= 4


def incident6_singletons(word):
    return {
        e for e, ab in SINGLE.items()
        if 6 in e and (word[e[0]], word[e[1]]) == ab
    }


def coefficient_poly(word, edge):
    """Coefficient of the edge cell after deleting the edge endpoints."""
    vertices = tuple(v for v in range(N) if v not in edge)
    out = Counter()
    for matching in perfect_matchings(vertices):
        cells = []
        for u, v in matching:
            a, b = word[u], word[v]
            if (a, b) not in SUPPORT[(u, v)]:
                break
            cells.append((u, v, a, b))
        else:
            out[monomial(cells)] += 1
    return dict(out)


def p_add(*terms):
    out = Counter()
    for scalar, poly in terms:
        for m, c in poly.items():
            out[m] += scalar * c
    return {m: c for m, c in out.items() if c}


def p_mul(p, q):
    out = Counter()
    for m, a in p.items():
        for n, b in q.items():
            out[tuple(sorted(m + n))] += a * b
    return {m: c for m, c in out.items() if c}


def p_var(name):
    return {(name,): 1}


def p_binomial(pos, neg):
    return {(pos,): 1, (neg,): -1}


def divide_var(poly, var):
    out = Counter()
    for m, c in poly.items():
        if var not in m:
            continue
        mm = list(m)
        mm.remove(var)
        out[tuple(mm)] += c
    return dict(out)


def decompose_packet(words, target_edge):
    """Return H_t=A56[y5,t]P+A67[t,y7]Q+delta(target) z*C."""
    y5, y7 = words[0][5], words[0][7]
    spike_t = SINGLE[target_edge][1]
    spike = cell_name(target_edge[0], target_edge[1], *SINGLE[target_edge])
    rows = [row_poly(w) for w in words]
    Ps, Qs, Cs = [], [], []
    for t, H in enumerate(rows):
        a = cell_name(5, 6, y5, t)
        b = cell_name(6, 7, t, y7)
        Ps.append(divide_var(H, a))
        Qs.append(divide_var(H, b))
        Cs.append(divide_var(H, spike))
        reconstructed = p_add(
            (1, p_mul(p_var(a), Ps[-1])),
            (1, p_mul(p_var(b), Qs[-1])),
            (1, p_mul(p_var(spike), Cs[-1])),
        )
        require(reconstructed == H, "packet reconstruction failed")
    require(Ps[0] == Ps[1] == Ps[2], "P depends on the site-6 colour")
    require(Qs[0] == Qs[1] == Qs[2], "Q depends on the site-6 colour")
    require(all(not Cs[t] for t in COLORS if t != spike_t),
            "a non-target site-6 singleton fired")
    require(Cs[spike_t] == coefficient_poly(words[spike_t], target_edge),
            "singleton cofactor mismatch")
    return {
        "rows": rows,
        "P": Ps[0],
        "Q": Qs[0],
        "C": Cs[spike_t],
        "spike_t": spike_t,
        "spike": spike,
    }


def find_packets(target_edge):
    """Lexicographically first monomial-cofactor packet for each (y5,y7)."""
    spike_t = SINGLE[target_edge][1]
    other = tuple(i for i in range(N) if i != 6)
    found = {}
    counts = Counter()
    for values in itertools.product(COLORS, repeat=7):
        base = [0] * N
        for i, c in zip(other, values):
            base[i] = c
        if base[target_edge[0]] != SINGLE[target_edge][0]:
            continue
        words = []
        for t in COLORS:
            base[6] = t
            words.append(tuple(base))
        if not all(mixed_x4(w) for w in words):
            continue
        if any(
            incident6_singletons(w) != ({target_edge} if t == spike_t else set())
            for t, w in enumerate(words)
        ):
            continue
        C = coefficient_poly(words[spike_t], target_edge)
        if len(C) != 1 or next(iter(C.values())) != 1:
            continue
        key = (base[5], base[7])
        counts[key] += 1
        found.setdefault(key, tuple(words))
    require(set(found) == set(itertools.product(COLORS, repeat=2)),
            f"packet coverage failed for {target_edge}")
    return found, counts


def determinant_poly(y5, y7, a, b):
    aa = cell_name(5, 6, y5, a)
    ab = cell_name(5, 6, y5, b)
    ba = cell_name(6, 7, a, y7)
    bb = cell_name(6, 7, b, y7)
    return p_add((1, p_mul(p_var(aa), p_var(bb))),
                 (-1, p_mul(p_var(ab), p_var(ba))))


def validate_cramer_identity(words, target_edge, clean_pair):
    """Validate D*Hs-alpha*Ha-beta*Hb = D*z*C literally."""
    data = decompose_packet(words, target_edge)
    a, b = clean_pair
    s = data["spike_t"]
    y5, y7 = words[0][5], words[0][7]

    def av(t): return cell_name(5, 6, y5, t)
    def bv(t): return cell_name(6, 7, t, y7)

    D = determinant_poly(y5, y7, a, b)
    alpha = p_add((1, p_mul(p_var(av(s)), p_var(bv(b)))),
                  (-1, p_mul(p_var(av(b)), p_var(bv(s)))))
    beta = p_add((1, p_mul(p_var(av(a)), p_var(bv(s)))),
                 (-1, p_mul(p_var(av(s)), p_var(bv(a)))))
    rhs = p_mul(D, p_mul(p_var(data["spike"]), data["C"]))
    residual = p_add((1, p_mul(D, data["rows"][s])),
                     (-1, p_mul(alpha, data["rows"][a])),
                     (-1, p_mul(beta, data["rows"][b])),
                     (-1, rhs))
    require(not residual, "Cramer sparse identity failed")

    # Sign mutation must be detected: use +alpha instead of -alpha.
    mutated = p_add((1, p_mul(D, data["rows"][s])),
                    (1, p_mul(alpha, data["rows"][a])),
                    (-1, p_mul(beta, data["rows"][b])),
                    (-1, rhs))
    require(bool(mutated), "Cramer sign mutation did not fire")
    return {
        "words": ["".join(map(str, w)) for w in words],
        "row_term_counts": [len(data["rows"][t]) for t in COLORS],
        "P_terms": len(data["P"]),
        "Q_terms": len(data["Q"]),
        "singleton": data["spike"],
        "singleton_prefactor": "*".join(next(iter(data["C"]))) or "1",
        "clean_pair": list(clean_pair),
        "determinant": (
            f"{av(a)}*{bv(b)}-{av(b)}*{bv(a)}"
        ),
        "cramer_identity": (
            "D*H_s-det(r_s,r_b)*H_a-det(r_a,r_s)*H_b="
            "D*singleton*prefactor"
        ),
        "identity_residual_terms": 0,
        "sign_mutation_residual_terms": len(mutated),
    }


def validate_final_identity(words):
    """With D01=0, a0*H1-a1*H0=a0*z26*C is the unit contradiction."""
    data = decompose_packet(words, (2, 6))
    require(data["spike_t"] == 1, "edge 26 did not fire at colour 1")
    y5, y7 = words[0][5], words[0][7]
    a0 = cell_name(5, 6, y5, 0)
    a1 = cell_name(5, 6, y5, 1)
    D01 = determinant_poly(y5, y7, 0, 1)
    rhs_unit = p_mul(p_var(a0), p_mul(p_var(data["spike"]), data["C"]))
    residual = p_add(
        (1, p_mul(p_var(a0), data["rows"][1])),
        (-1, p_mul(p_var(a1), data["rows"][0])),
        (-1, p_mul(D01, data["Q"])),
        (-1, rhs_unit),
    )
    require(not residual, "final two-row sparse identity failed")
    require(len(rhs_unit) == 1 and next(iter(rhs_unit.values())) == 1,
            "final right side is not a monomial")
    return {
        "words_used": ["".join(map(str, words[t])) for t in (0, 1)],
        "identity": "A56[y5,0]*H_1-A56[y5,1]*H_0=D01*Q+A56[y5,0]*z26*C",
        "identity_residual_terms": 0,
        "laurent_unit": "*".join(next(iter(rhs_unit))),
        "logic": (
            "the edge-(0,6) packet gives D01=0; X4 gives H_0=H_1=0; "
            "every factor of the displayed monomial is live on the open support"
        ),
    }


def validate_combined_certificate(words06, words26):
    """A five-generator Laurent unit certificate at one fixed tuple."""
    d06 = decompose_packet(words06, (0, 6))
    d26 = decompose_packet(words26, (2, 6))
    require((words06[0][5], words06[0][7]) ==
            (words26[0][5], words26[0][7]), "packet tuples differ")
    y5, y7 = words06[0][5], words06[0][7]

    def av(t): return cell_name(5, 6, y5, t)
    def bv(t): return cell_name(6, 7, t, y7)

    D = determinant_poly(y5, y7, 0, 1)
    alpha = p_add((1, p_mul(p_var(av(2)), p_var(bv(1)))),
                  (-1, p_mul(p_var(av(1)), p_var(bv(2)))))
    beta = p_add((1, p_mul(p_var(av(0)), p_var(bv(2)))),
                 (-1, p_mul(p_var(av(2)), p_var(bv(0)))))
    U06 = p_mul(p_var(d06["spike"]), d06["C"])
    U26 = p_mul(p_var(av(0)), p_mul(p_var(d26["spike"]), d26["C"]))

    cramer06 = p_add(
        (1, p_mul(D, d06["rows"][2])),
        (-1, p_mul(alpha, d06["rows"][0])),
        (-1, p_mul(beta, d06["rows"][1])),
    )
    final26 = p_add(
        (1, p_mul(p_var(av(0)), d26["rows"][1])),
        (-1, p_mul(p_var(av(1)), d26["rows"][0])),
    )
    residual = p_add(
        (1, p_mul(U06, final26)),
        (-1, p_mul(d26["Q"], cramer06)),
        (-1, p_mul(U06, U26)),
    )
    require(not residual, "combined five-row certificate failed")
    unit = p_mul(U06, U26)
    require(len(unit) == 1 and next(iter(unit.values())) == 1,
            "combined right side is not a Laurent monomial")
    return {
        "tuple_y5_y7": [y5, y7],
        "x4_generators": [
            "".join(map(str, words06[t])) for t in (0, 1, 2)
        ] + ["".join(map(str, words26[t])) for t in (0, 1)],
        "generator_count": 5,
        "identity": (
            "U06*(a0*H26_1-a1*H26_0)-Q26*(D*H06_2-alpha*H06_0-"
            "beta*H06_1)=U06*U26"
        ),
        "definitions": {
            "D": f"{av(0)}*{bv(1)}-{av(1)}*{bv(0)}",
            "alpha": f"{av(2)}*{bv(1)}-{av(1)}*{bv(2)}",
            "beta": f"{av(0)}*{bv(2)}-{av(2)}*{bv(0)}",
            "U06": "*".join(next(iter(U06))),
            "U26": "*".join(next(iter(U26))),
        },
        "laurent_unit_rhs": "*".join(next(iter(unit))),
        "identity_residual_terms": 0,
    }


def transport_census(raw):
    """Exhaust all relabelled two-column Cramer packets on one template.

    A packet varies one site's colour through 0,1,2, has exactly one
    incident singleton spike, has a monomial nonzero spike cofactor, and has
    exactly two full-neighbour cofactors nonzero.  This is precisely the
    support condition needed for the same 3-row/two-column Cramer step; no
    coefficient search or genericity assumption is involved.
    """
    support = decode(raw)
    full = {e for e in EDGES if len(support[e]) == 9}
    singles = {e: next(iter(support[e]))
               for e in EDGES if len(support[e]) == 1}

    def endpoint_colour(edge, ab, vertex):
        return ab[0] if edge[0] == vertex else ab[1]

    def other_colour(edge, ab, vertex):
        return ab[1] if edge[0] == vertex else ab[0]

    def cofactor_count(word, edge):
        vertices = tuple(v for v in range(N) if v not in edge)
        total = 0
        for matching in perfect_matchings(vertices):
            if all((word[u], word[v]) in support[(u, v)]
                   for u, v in matching):
                total += 1
        return total

    packet_counts = Counter()
    by_key_and_spike = Counter()
    for vertex in range(N):
        full_neighbours = sorted(
            next(iter(set(edge) - {vertex}))
            for edge in full if vertex in edge
        )
        other_vertices = tuple(v for v in range(N) if v != vertex)
        for target, ab in singles.items():
            if vertex not in target:
                continue
            spike_colour = endpoint_colour(target, ab, vertex)
            target_neighbour = next(iter(set(target) - {vertex}))
            required_neighbour_colour = other_colour(target, ab, vertex)
            for values in itertools.product(COLORS, repeat=7):
                base = [0] * N
                for v, c in zip(other_vertices, values):
                    base[v] = c
                if base[target_neighbour] != required_neighbour_colour:
                    continue
                words = []
                for t in COLORS:
                    base[vertex] = t
                    words.append(tuple(base))
                if not all(mixed_x4(w) for w in words):
                    continue
                incident_ok = True
                for t, word in enumerate(words):
                    fired = {
                        edge for edge, cell in singles.items()
                        if vertex in edge
                        and (word[edge[0]], word[edge[1]]) == cell
                    }
                    if fired != ({target} if t == spike_colour else set()):
                        incident_ok = False
                        break
                if not incident_ok:
                    continue
                if cofactor_count(words[spike_colour], target) != 1:
                    continue
                effective = []
                for neighbour in full_neighbours:
                    edge = tuple(sorted((vertex, neighbour)))
                    if cofactor_count(words[0], edge):
                        effective.append(neighbour)
                if len(effective) != 2:
                    continue
                neighbour_colours = tuple(base[n] for n in effective)
                key = (vertex, tuple(effective), neighbour_colours)
                packet_counts[(vertex, target, tuple(effective))] += 1
                by_key_and_spike[(key, spike_colour)] += 1

    ordered_pairs = 0
    keys = {key for key, _s in by_key_and_spike}
    paired_keys = 0
    for key in keys:
        counts = [by_key_and_spike.get((key, s), 0) for s in COLORS]
        here = sum(counts[s] * counts[t]
                   for s in COLORS for t in COLORS if s != t)
        ordered_pairs += here
        paired_keys += bool(here)
    degrees = {
        str(v): sum(v in edge for edge in full) for v in range(N)
    }
    return {
        "full_block_degrees": degrees,
        "minimum_full_block_degree": min(degrees.values()),
        "two_column_packet_count": sum(packet_counts.values()),
        "paired_distinct_spike_ordered_pairs": ordered_pairs,
        "paired_effective_keys": paired_keys,
        "packet_counts": {
            f"v{v}|e{edge[0]}{edge[1]}|n{''.join(map(str, neighbours))}": n
            for (v, edge, neighbours), n in sorted(packet_counts.items())
        },
    }


def main():
    require(len(EDGES) == 28 and len(PM8) == 105, "matching census failed")
    require(len(FULL) == 13 and len(SINGLE) == 12 and len(MISSING) == 3,
            "support edge census failed")
    require(sum(len(v) for v in SUPPORT.values()) == 129,
            "support cell census failed")
    require(SINGLE[(0, 6)] == (0, 2), "raw edge06 endpoint order failed")
    require(SINGLE[(2, 6)] == (2, 1), "raw edge26 endpoint order failed")
    require({(5, 6), (6, 7)} == {e for e in FULL if 6 in e},
            "site 6 does not have the required two full neighbours")

    fibre_hist = Counter()
    mixed_count = pure_count = 0
    for word in itertools.product(COLORS, repeat=N):
        if not all_x4(word):
            continue
        fibre_hist[len(row_poly(word))] += 1
        if len(set(word)) == 1:
            pure_count += 1
        else:
            mixed_count += 1
    require(mixed_count == 4878 and pure_count == 3, "X4 census failed")
    require(min(fibre_hist) == 8, "X4 minimum fibre changed")

    packets06, counts06 = find_packets((0, 6))
    packets26, counts26 = find_packets((2, 6))
    minor_ledger = {}
    final_ledger = {}
    for key in itertools.product(COLORS, repeat=2):
        minor_ledger[str(key)] = validate_cramer_identity(
            packets06[key], (0, 6), (0, 1)
        )
        final_ledger[str(key)] = validate_final_identity(packets26[key])
    combined = validate_combined_certificate(packets06[(0, 0)],
                                             packets26[(0, 0)])
    transport = {str(m): transport_census(TEMPLATES[m])
                 for m in range(25, 29)}
    require(transport["25"]["paired_distinct_spike_ordered_pairs"] > 0,
            "m25 transport positive control failed")
    require(all(transport[str(m)]["two_column_packet_count"] == 0
                for m in range(26, 29)),
            "the m25 packet unexpectedly transported")

    # Raw endpoint-ordering negative control.  Transposing the bit convention
    # changes ten of the twelve directed singleton cells, including both
    # load-bearing site-6 targets.
    trans = decode(transpose=True)
    trans_single = {e: next(iter(v)) for e, v in trans.items() if len(v) == 1}
    endpoint_mismatches = sum(SINGLE[e] != trans_single[e] for e in SINGLE)
    require(endpoint_mismatches > 0, "endpoint transpose did not fire")
    require(trans_single[(0, 6)] != SINGLE[(0, 6)],
            "edge06 endpoint transpose did not fire")
    require(trans_single[(2, 6)] != SINGLE[(2, 6)],
            "edge26 endpoint transpose did not fire")

    core = {
        "support": {
            "raw_mask": list(RAW_M25),
            "raw_endpoint_rule": "bit(3*a+b), a at smaller endpoint",
            "cells": 129,
            "full_blocks": ["%d%d" % e for e in sorted(FULL)],
            "singleton_cells": {
                "%d%d" % e: list(ab) for e, ab in sorted(SINGLE.items())
            },
            "missing_edges": ["%d%d" % e for e in sorted(MISSING)],
        },
        "x4_inventory": {
            "all_profile_rows": mixed_count + pure_count,
            "mixed_vanishing_generators": mixed_count,
            "pure_nonvanishing_rows": pure_count,
            "fibre_size_histogram": {
                str(k): fibre_hist[k] for k in sorted(fibre_hist)
            },
            "minimum_fibre_size": min(fibre_hist),
            "binomial_or_trinomial_rows": 0,
        },
        "edge06_minor_packets": {
            "target_cell": "x06_02",
            "coverage": "all 9 (y5,y7) tuples",
            "candidate_counts": {
                str(k): counts06[k] for k in sorted(counts06)
            },
            "consequence": (
                "D01(y5,y7)=A56[y5,0]A67[1,y7]-"
                "A56[y5,1]A67[0,y7]=0 for every y5,y7"
            ),
            "ledger": minor_ledger,
        },
        "edge26_unit_packets": {
            "target_cell": "x26_21",
            "coverage": "all 9 (y5,y7) tuples",
            "candidate_counts": {
                str(k): counts26[k] for k in sorted(counts26)
            },
            "ledger": final_ledger,
        },
        "five_row_laurent_certificate": combined,
        "m25_to_m28_transport_census": {
            "criterion": (
                "all sites, incident singleton targets, and 3^7 fixed-colour "
                "assignments; mixed X4 triple; target is the only incident "
                "spike; monomial spike cofactor; exactly two effective full "
                "neighbour cofactors; pair two distinct spike colours at the "
                "same effective-neighbour/endpoint-colour key"
            ),
            "results": transport,
            "verdict": (
                "the five-row two-column Cramer+unit pattern exists at m25 "
                "and has no relabelled or recoloured instance at m26,m27,m28; "
                "this is only a non-transport result, not X4 feasibility"
            ),
        },
        "verdict": {
            "open_m25_x4_locus": "EMPTY",
            "scope": "the full 129-cell W8/W15 m=25 endpoint-cell support",
            "field_scope": "every field (indeed every integral domain)",
            "certificate": (
                "for any fixed tuple, the edge06 Cramer identity and live "
                "monomial force D01=0; the edge26 two-row identity then "
                "forces a product of five live cells to vanish"
            ),
            "carrier_screening": "vacuous: there is no X4 point on the open support",
        },
        "controls": {
            "literal_sparse_identities": 18,
            "literal_identity_failures": 0,
            "sign_mutations_fired": 9,
            "endpoint_transpose_mismatches": endpoint_mismatches,
            "standard_O_IS_digest_invariant": True,
        },
    }
    blob = json.dumps(core, sort_keys=True, separators=(",", ":")).encode()
    digest = hashlib.sha256(blob).hexdigest()
    result = {
        "mode": {
            "optimize": sys.flags.optimize,
            "isolated": sys.flags.isolated,
            "no_site": sys.flags.no_site,
        },
        "core_digest": digest,
        "core": core,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, sort_keys=True)
        f.write("\n")
    print(f"CORE_DIGEST={digest}")
    print("M25_X4_OPEN_SUPPORT=EMPTY")
    print("packets06=9 packets26=9 sparse_identity_failures=0")


if __name__ == "__main__":
    main()
