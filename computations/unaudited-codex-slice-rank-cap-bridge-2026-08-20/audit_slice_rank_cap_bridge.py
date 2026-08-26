#!/usr/bin/env python3
"""Raw audit of the 3xn singleton-packet/rank/cap bridge.

UNAUDITED.  This is independent of the earlier m25 checker: word
polynomials are rebuilt by a recursive subset hafnian, and the m26
counterexample is constructed from the raw endpoint masks over F_13.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import json
import os
import sys


HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "results.json")
COLORS = (0, 1, 2)
SITES = tuple(range(8))
EDGES = tuple(combinations(SITES, 2))
EIDX = {edge: index for index, edge in enumerate(EDGES)}

TEMPLATES = {
    25: (511, 511, 511, 1, 2, 4, 511, 511, 511, 511, 8, 16, 4,
         511, 8, 511, 128, 32, 64, 128, 0, 256, 511, 0, 511, 511, 0,
         511),
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


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def support_of(raw, transpose=False):
    answer = {}
    for edge, mask in zip(EDGES, raw):
        cells = set()
        for a, b in product(COLORS, repeat=2):
            bit = 3 * b + a if transpose else 3 * a + b
            if mask & (1 << bit):
                cells.add((a, b))
        answer[edge] = cells
    return answer


def var_name(edge, a, b):
    return f"x{edge[0]}{edge[1]}_{a}{b}"


def padd(*items):
    answer = Counter()
    for scalar, polynomial in items:
        for monomial, coefficient in polynomial.items():
            answer[monomial] += scalar * coefficient
    return {m: c for m, c in answer.items() if c}


def pmul(left, right):
    answer = Counter()
    for first, a in left.items():
        for second, b in right.items():
            answer[tuple(sorted(first + second))] += a * b
    return {m: c for m, c in answer.items() if c}


def pvar(name):
    return {(name,): 1}


def pdivide(polynomial, name):
    answer = Counter()
    for monomial, coefficient in polynomial.items():
        if name in monomial:
            rest = list(monomial)
            rest.remove(name)
            answer[tuple(rest)] += coefficient
    return dict(answer)


def symbolic_hafnian(word, vertices, support):
    """Recursive subset-DP polynomial; no stored perfect-matching list."""
    memo = {}

    def visit(current):
        if not current:
            return {(): 1}
        if current in memo:
            return memo[current]
        u = current[0]
        answer = {}
        for k in range(1, len(current)):
            v = current[k]
            edge = (u, v)
            a, b = word[u], word[v]
            if (a, b) not in support[edge]:
                continue
            rest = current[1:k] + current[k + 1:]
            cell = pvar(var_name(edge, a, b))
            answer = padd((1, answer), (1, pmul(cell, visit(rest))))
        memo[current] = answer
        return answer

    return visit(tuple(vertices))


def split_packet(words, centre, neighbours, target, support):
    singles = {edge: next(iter(cells)) for edge, cells in support.items()
               if len(cells) == 1}
    target_cell = singles[target]
    target_colour = (target_cell[0] if target[0] == centre
                     else target_cell[1])
    spike_name = var_name(target, *target_cell)
    rows = [symbolic_hafnian(word, SITES, support) for word in words]
    cofactors = []
    spike_cofactors = []
    for t, row in enumerate(rows):
        here = []
        rebuilt = {}
        for neighbour in neighbours:
            edge = tuple(sorted((centre, neighbour)))
            a, b = ((t, word_colour(words[t], neighbour)) if centre < neighbour
                    else (word_colour(words[t], neighbour), t))
            name = var_name(edge, a, b)
            quotient = pdivide(row, name)
            here.append(quotient)
            rebuilt = padd((1, rebuilt), (1, pmul(pvar(name), quotient)))
        spike_q = pdivide(row, spike_name)
        rebuilt = padd((1, rebuilt), (1, pmul(pvar(spike_name), spike_q)))
        require(rebuilt == row, ("packet partition", words[t]))
        cofactors.append(here)
        spike_cofactors.append(spike_q)
    require(all(cofactors[t] == cofactors[0] for t in COLORS),
            "arm cofactor depends on centre colour")
    require(all(not spike_cofactors[t] for t in COLORS if t != target_colour),
            "non-target spike")
    return {
        "rows": rows,
        "Q": cofactors[0],
        "U": pmul(pvar(spike_name), spike_cofactors[target_colour]),
        "spike_colour": target_colour,
        "spike_name": spike_name,
    }


def word_colour(word, site):
    return word[site]


def m25_second_engine_certificate():
    support = support_of(TEMPLATES[25])
    w06 = tuple(tuple(map(int, word)) for word in
                ("00001000", "00001010", "00001020"))
    w26 = tuple(tuple(map(int, word)) for word in
                ("10200000", "10200010", "10200020"))
    require(all(len(set(w)) > 1 and max(w.count(c) for c in COLORS) >= 4
                for w in w06 + w26), "certificate word is not mixed X4")
    first = split_packet(w06, 6, (5, 7), (0, 6), support)
    second = split_packet(w26, 6, (5, 7), (2, 6), support)
    require(first["spike_colour"] == 2 and second["spike_colour"] == 1,
            "spike colours")
    require(len(first["U"]) == len(second["U"]) == 1,
            "spike cofactors are not monomials")

    a = [var_name((5, 6), 0, t) for t in COLORS]
    b = [var_name((6, 7), t, 0) for t in COLORS]
    D = padd((1, pmul(pvar(a[0]), pvar(b[1]))),
             (-1, pmul(pvar(a[1]), pvar(b[0]))))
    alpha = padd((1, pmul(pvar(a[2]), pvar(b[1]))),
                 (-1, pmul(pvar(a[1]), pvar(b[2]))))
    beta = padd((1, pmul(pvar(a[0]), pvar(b[2]))),
                (-1, pmul(pvar(a[2]), pvar(b[0]))))
    cramer = padd(
        (1, pmul(D, first["rows"][2])),
        (-1, pmul(alpha, first["rows"][0])),
        (-1, pmul(beta, first["rows"][1])),
    )
    require(cramer == pmul(D, first["U"]), "second-engine Cramer identity")
    final = padd(
        (1, pmul(pvar(a[0]), second["rows"][1])),
        (-1, pmul(pvar(a[1]), second["rows"][0])),
    )
    require(final == padd((1, pmul(D, second["Q"][1])),
                           (1, pmul(pvar(a[0]), second["U"]))),
            "second-engine final identity")
    right = pmul(first["U"], pmul(pvar(a[0]), second["U"]))
    certificate = padd(
        (1, pmul(first["U"], final)),
        (-1, pmul(second["Q"][1], cramer)),
    )
    require(certificate == right and len(right) == 1,
            "second-engine combined certificate")

    transposed = support_of(TEMPLATES[25], transpose=True)
    singleton = {edge: next(iter(cells)) for edge, cells in support.items()
                 if len(cells) == 1}
    singleton_t = {edge: next(iter(cells)) for edge, cells in transposed.items()
                   if len(cells) == 1}
    mismatches = sum(singleton[e] != singleton_t[e] for e in singleton)
    require(mismatches == 9, "endpoint transpose control")
    return {
        "engine": "recursive subset hafnian with sparse polynomial arithmetic",
        "x4_generators": ["".join(map(str, w)) for w in w06]
                         + ["".join(map(str, w)) for w in w26[:2]],
        "identity_residual_terms": 0,
        "laurent_unit_rhs": "*".join(next(iter(right))),
        "endpoint_transpose_singleton_mismatches": mismatches,
    }


@lru_cache(None)
def matchings(vertices):
    if not vertices:
        return ((),)
    u = vertices[0]
    answer = []
    for k in range(1, len(vertices)):
        v = vertices[k]
        rest = vertices[1:k] + vertices[k + 1:]
        for tail in matchings(rest):
            answer.append(((u, v),) + tail)
    return tuple(answer)


def support_hafnian_count(word, vertices, support):
    return sum(all((word[u], word[v]) in support[(u, v)]
                   for u, v in matching)
               for matching in matchings(tuple(vertices)))


def packet_census(raw):
    support = support_of(raw)
    full = {edge for edge, cells in support.items() if len(cells) == 9}
    singles = {edge: next(iter(cells)) for edge, cells in support.items()
               if len(cells) == 1}
    histogram = Counter()
    by_key = defaultdict(Counter)
    by_target = Counter()
    for centre in SITES:
        full_neighbours = sorted(next(iter(set(edge) - {centre}))
                                 for edge in full if centre in edge)
        other_sites = tuple(site for site in SITES if site != centre)
        for target, cell_ab in singles.items():
            if centre not in target:
                continue
            spike = cell_ab[0] if target[0] == centre else cell_ab[1]
            neighbour = next(iter(set(target) - {centre}))
            neighbour_colour = cell_ab[1] if target[0] == centre else cell_ab[0]
            for fixed in product(COLORS, repeat=7):
                base = [0] * 8
                for site, colour in zip(other_sites, fixed):
                    base[site] = colour
                if base[neighbour] != neighbour_colour:
                    continue
                words = []
                for t in COLORS:
                    base[centre] = t
                    words.append(tuple(base))
                if not all(len(set(word)) > 1
                           and max(word.count(c) for c in COLORS) >= 4
                           for word in words):
                    continue
                good = True
                for t, word in enumerate(words):
                    fired = {edge for edge, ab in singles.items()
                             if centre in edge
                             and (word[edge[0]], word[edge[1]]) == ab}
                    if fired != ({target} if t == spike else set()):
                        good = False
                        break
                if not good:
                    continue
                if support_hafnian_count(
                        words[spike], tuple(v for v in SITES if v not in target),
                        support) != 1:
                    continue
                effective = tuple(n for n in full_neighbours
                                  if support_hafnian_count(
                                      words[0], tuple(v for v in SITES
                                                      if v not in (centre, n)),
                                      support))
                histogram[len(effective)] += 1
                by_target[(centre, target, len(effective))] += 1
                key = (centre, effective, tuple(base[n] for n in effective))
                by_key[key][spike] += 1
    ordered_pairs = sum(
        counts[a] * counts[b]
        for counts in by_key.values() for a in COLORS for b in COLORS if a != b
    )
    return {
        "effective_column_histogram": dict(sorted(histogram.items())),
        "packet_count": sum(histogram.values()),
        "paired_distinct_spike_keys": sum(
            sum(bool(counts[a] and counts[b]) for a in COLORS for b in COLORS
                if a < b) > 0 for counts in by_key.values()),
        "ordered_distinct_spike_pairs": ordered_pairs,
        "target_histogram": {
            f"v{v}|e{e[0]}{e[1]}|n{n}": count
            for (v, e, n), count in sorted(by_target.items())
        },
    }


def det3(rows, modulus):
    return (
        rows[0][0] * (rows[1][1] * rows[2][2] - rows[1][2] * rows[2][1])
        - rows[0][1] * (rows[1][0] * rows[2][2] - rows[1][2] * rows[2][0])
        + rows[0][2] * (rows[1][0] * rows[2][1] - rows[1][1] * rows[2][0])
    ) % modulus


def rref_mod(rows, modulus, width=9):
    matrix = [list(row) for row in rows if any(value % modulus for value in row)]
    rank = 0
    pivots = []
    for column in range(width):
        pivot = next((i for i in range(rank, len(matrix))
                      if matrix[i][column] % modulus), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column] % modulus, -1, modulus)
        matrix[rank] = [value * inverse % modulus for value in matrix[rank]]
        for i in range(len(matrix)):
            if i == rank or not matrix[i][column] % modulus:
                continue
            scale = matrix[i][column] % modulus
            matrix[i] = [(x - scale * y) % modulus
                         for x, y in zip(matrix[i], matrix[rank])]
        pivots.append(column)
        rank += 1
        if rank == width:
            break
    return tuple(tuple(row) for row in matrix[:rank]), tuple(pivots)


def nullspace_mod(rows, modulus, width=9):
    reduced, pivots = rref_mod(rows, modulus, width)
    basis = []
    for free in (j for j in range(width) if j not in pivots):
        vector = [0] * width
        vector[free] = 1
        for row, pivot in zip(reversed(reduced), reversed(pivots)):
            vector[pivot] = -sum(row[j] * vector[j]
                                 for j in range(width) if j != pivot) % modulus
        basis.append(tuple(vector))
    return tuple(basis)


def m26_counterexample():
    modulus = 13
    support = support_of(TEMPLATES[26])
    source = {edge: [[0] * 3 for _ in COLORS] for edge in EDGES}
    for edge_index, edge in enumerate(EDGES):
        for a, b in support[edge]:
            value = (1 + 5 * edge_index + 3 * a + 7 * b) % modulus
            source[edge][a][b] = value or 1

    def cell(u, v, a, b):
        return (source[u, v][a][b] if u < v else source[v, u][b][a])

    def hafnian(word, vertices):
        answer = 0
        for matching in matchings(tuple(vertices)):
            term = 1
            for u, v in matching:
                term = term * cell(u, v, word[u], word[v]) % modulus
            answer = (answer + term) % modulus
        return answer

    w06 = tuple(tuple(map(int, word)) for word in
                ("00001000", "00001010", "00001020"))
    w26 = tuple(tuple(map(int, word)) for word in
                ("10200000", "10200010", "10200020"))
    neighbours = (3, 5, 7)

    def qvector(word):
        return tuple(hafnian(word, tuple(v for v in SITES if v not in (6, n)))
                     for n in neighbours)

    q06, q26 = qvector(w06[0]), qvector(w26[0])
    u06 = (cell(0, 6, 0, 2)
           * hafnian(w06[2], (1, 2, 3, 4, 5, 7))) % modulus
    u26 = (cell(2, 6, 2, 1)
           * hafnian(w26[1], (0, 1, 3, 4, 5, 7))) % modulus
    require(u06 and u26, "counterexample spike unit vanished")

    candidates = []
    for t in COLORS:
        target06 = -u06 % modulus if t == 2 else 0
        target26 = -u26 % modulus if t == 1 else 0
        rows = []
        for row in product(range(1, modulus), repeat=3):
            if (sum(x * y for x, y in zip(row, q06)) % modulus == target06
                    and sum(x * y for x, y in zip(row, q26)) % modulus
                    == target26):
                rows.append(row)
        require(rows, ("no slice row", t))
        candidates.append(rows)
    slice_rows = next((rows for rows in product(*candidates)
                       if det3(rows, modulus)), None)
    require(slice_rows is not None, "no full-rank slice")
    for t, row in enumerate(slice_rows):
        source[3, 6][0][t], source[5, 6][0][t], source[6, 7][t][0] = row
    require(all(source[e][a][b] for e in EDGES for a, b in support[e]),
            "counterexample left open support")
    packet_values = {
        "edge06": [hafnian(word, SITES) for word in w06],
        "edge26": [hafnian(word, SITES) for word in w26],
    }
    require(packet_values == {"edge06": [0, 0, 0], "edge26": [0, 0, 0]},
            packet_values)
    require(det3(slice_rows, modulus) != 0, "slice determinant vanished")

    def response_block(p, q, a, b):
        rows = []
        for alpha, beta in product(COLORS, repeat=2):
            rows.append(tuple(
                (cell(p, a, i, alpha) * cell(q, b, j, beta)
                 + cell(p, b, i, beta) * cell(q, a, j, alpha)) % modulus
                for i, j in product(COLORS, repeat=2)
            ))
        return tuple(rows)

    def carrier(p, q, kind, label):
        residual = tuple(v for v in SITES if v not in (p, q))
        residual_edges = tuple(combinations(residual, 2))
        if kind == "star":
            allowed = {edge for edge in residual_edges if label[0] in edge}
        else:
            allowed = set(combinations(label, 2))
        forbidden = tuple(edge for edge in residual_edges if edge not in allowed)
        rows = [row for edge in forbidden for row in response_block(p, q, *edge)]
        reduced, _ = rref_mod(rows, modulus)
        activities = []
        for colour in COLORS:
            vector = [0] * 9
            vector[4 * colour] = 1
            activities.append(tuple(vector))
        activities.append(tuple(cell(p, q, i, j)
                                for i, j in product(COLORS, repeat=2)))
        blockers = [len(rref_mod(rows + [activity], modulus)[0]) == len(reduced)
                    for activity in activities]
        return {
            "rank": len(reduced),
            "blocked_activity_forms": blockers,
            "active_linear_carrier": not any(blockers),
            "rows": rows,
            "activities": activities,
            "allowed": allowed,
        }

    rank_histogram = Counter()
    active = []
    rank8 = []
    for p, q in EDGES:
        residual = tuple(v for v in SITES if v not in (p, q))
        for centre in residual:
            record = carrier(p, q, "star", (centre,))
            rank_histogram[("star", record["rank"])] += 1
            if record["active_linear_carrier"]:
                active.append((p, q, "star", (centre,)))
        for triangle in combinations(residual, 3):
            record = carrier(p, q, "triangle", triangle)
            rank_histogram[("triangle", record["rank"])] += 1
            if record["active_linear_carrier"]:
                active.append((p, q, "triangle", triangle))
            if record["rank"] == 8:
                rank8.append((p, q, triangle, record))
    require(not active, active[:3])
    natural = carrier(0, 2, "star", (6,))
    require(natural["rank"] == 9 and not natural["active_linear_carrier"],
            "natural star unexpectedly active")
    require(len(rank8) == 2, "rank-8 triangle census")

    # Literal clean-error check on a nonzero kernel vector of one rank-8
    # blocked triangle.  Forbidden responses vanish by matrix multiplication;
    # the full cubic error formula is also evaluated on all 729 residual words.
    p, q, triangle, exceptional = rank8[0]
    kernel = nullspace_mod(exceptional["rows"], modulus)
    require(len(kernel) == 1, "rank-8 kernel")
    K = kernel[0]
    require(all(sum(x * y for x, y in zip(row, K)) % modulus == 0
                for row in exceptional["rows"]), "K left carrier kernel")
    activity_values = [sum(x * y for x, y in zip(row, K)) % modulus
                       for row in exceptional["activities"]]
    require(not all(activity_values), "blocked K became active")
    residual = tuple(v for v in SITES if v not in (p, q))
    responses = {}
    for a, b in combinations(residual, 2):
        block = response_block(p, q, a, b)
        responses[a, b] = tuple(sum(x * y for x, y in zip(row, K)) % modulus
                                  for row in block)
    s_value = activity_values[3]
    error_nonzero = 0
    for values in product(COLORS, repeat=6):
        word = [0] * 8
        for site, colour in zip(residual, values):
            word[site] = colour
        error = 0
        for matching in matchings(residual):
            edges = list(matching)
            R = [responses[e][3 * word[e[0]] + word[e[1]]] for e in edges]
            B = [cell(*e, word[e[0]], word[e[1]]) for e in edges]
            error += s_value * (R[0] * R[1] * B[2]
                                + R[0] * B[1] * R[2]
                                + B[0] * R[1] * R[2]) + R[0] * R[1] * R[2]
        if error % modulus:
            error_nonzero += 1
    require(error_nonzero == 0, "literal cap error did not vanish")

    pure_values = [hafnian((colour,) * 8, SITES) for colour in COLORS]
    x4_failures = 0
    x4_total = 0
    for word in product(COLORS, repeat=8):
        if len(set(word)) == 1 or max(word.count(c) for c in COLORS) < 4:
            continue
        x4_total += 1
        x4_failures += bool(hafnian(word, SITES))
    require(x4_total == 4878 and x4_failures > 0,
            "counterexample scope control")

    return {
        "field": "F_13",
        "support": "m26, all 138 occupied cells nonzero",
        "packet_words": {
            "edge06": ["".join(map(str, word)) for word in w06],
            "edge26": ["".join(map(str, word)) for word in w26],
        },
        "packet_values": packet_values,
        "cofactor_vectors": {"Q06": list(q06), "Q26": list(q26)},
        "spike_units": {"U06": u06, "U26": u26},
        "slice_columns": ["A36[0,t]", "A56[0,t]", "A67[t,0]"],
        "slice_rows": [list(row) for row in slice_rows],
        "slice_determinant": det3(slice_rows, modulus),
        "natural_pair02_star6": {
            "rank": natural["rank"],
            "kernel_dimension": 9 - natural["rank"],
            "blocked_activity_forms": natural["blocked_activity_forms"],
        },
        "all_carriers": {
            "rank_histogram": {
                f"{kind}|rank{rank}": count
                for (kind, rank), count in sorted(rank_histogram.items())
            },
            "active_star_or_triangle_carriers": len(active),
        },
        "rank8_triangle_clean_inactive_control": {
            "pair": [p, q],
            "triangle": list(triangle),
            "kernel_vector": list(K),
            "activity_values_kappa012_s": activity_values,
            "literal_error_nonzero_coefficients": error_nonzero,
        },
        "global_x4_scope_guard": {
            "mixed_x4_rows": x4_total,
            "failed_mixed_x4_rows": x4_failures,
            "pure_amplitudes": pure_values,
            "note": "this refutes the local packet-rank-to-carrier implication, not an X4-coupled theorem",
        },
        "source": {
            f"{u}{v}": source[u, v] for u, v in EDGES
        },
    }


def main():
    certificate = m25_second_engine_certificate()
    censuses = {str(m): packet_census(TEMPLATES[m]) for m in range(25, 29)}
    require(censuses["25"]["effective_column_histogram"].get(2) == 248,
            "m25 two-column calibration")
    require(censuses["26"]["effective_column_histogram"] == {3: 1036, 4: 949},
            "m26 packet census")
    require(censuses["27"]["effective_column_histogram"] == {4: 999},
            "m27 packet census")
    require(censuses["28"]["packet_count"] == 0, "m28 monomial packet census")
    counterexample = m26_counterexample()
    # One vanishing 3x3 minor is not the rank-defect branch when n=4.
    minor_example = ((1, 1, 1, 10), (1, 1, 2, 9), (1, 1, 1, 1))
    minor_values = [det3(tuple(tuple(row[j] for j in columns)
                               for row in minor_example), 13)
                    for columns in combinations(range(4), 3)]
    packet_q = (1, 1, 1, 1)
    packet_pairings = [sum(x * y for x, y in zip(row, packet_q)) % 13
                       for row in minor_example]
    require(minor_values == [0, 0, 4, 4]
            and packet_pairings == [0, 0, 4], "single-minor counterexample")
    core = {
        "status": "PASS",
        "scope": "local matched-packet rank lemma and exact carrier counterexample; no global X4 theorem",
        "independent_m25_reaudit": certificate,
        "abstract_3xn_lemma": {
            "statement": (
                "If S has rows s0,s1,s2, Q is a packet cofactor vector, U is "
                "nonzero, and <sa,Q>=<sb,Q>=0 while <sc,Q>=-U for the third "
                "colour c, then rank_row(S)=3 over the fraction field. Thus "
                "rank<=2 is a unit contradiction; for n>=3 the complementary "
                "branch is full row rank."
            ),
            "proof": (
                "If rank(S)<=2 then sc lies in span(sa,sb); pairing with Q "
                "would give <sc,Q>=0, contradicting U!=0."
            ),
            "missing_map": (
                "Q lives in the n-dimensional neighbour-column space, while "
                "a cap K has nine endpoint-pair coordinates. SLICE-MASTER "
                "Sections 1-4 provide no map Q->K and no implication from "
                "rank(S)=3 to the four carrier row-space nonmembership tests."
            ),
            "single_minor_warning": {
                "field": "F_13",
                "S": [list(row) for row in minor_example],
                "Q": list(packet_q),
                "three_by_three_minors": minor_values,
                "packet_pairings": packet_pairings,
                "conclusion": (
                    "two chosen 3x3 minors vanish while row-rank is 3 and a "
                    "live spike packet is consistent; the contradictory "
                    "branch is all 3x3 minors zero, not one deficient minor"
                ),
            },
        },
        "packet_census": censuses,
        "m26_local_counterexample": counterexample,
        "verdict": {
            "rank_defect_branch": "valid: a live singleton packet excludes row rank <=2",
            "full_rank_to_active_carrier": "false from local packet data alone",
            "smallest_raw_counterexample": (
                "m26/F13 open support, two live singleton packet triples, "
                "3x3 slice determinant 1, but all 728 star/triangle carriers blocked"
            ),
            "remaining_possible_repair": (
                "a theorem may still use additional global X4 equations to "
                "couple the full-rank slice to the nine cap variables; the "
                "counterexample deliberately fails many X4 rows"
            ),
        },
        "controls": {
            "runtime_checks_survive_optimization": True,
            "standard_O_IS_digest_invariant": True,
        },
    }
    digest = sha256(json.dumps(core, sort_keys=True,
                              separators=(",", ":")).encode()).hexdigest()
    output = {
        "mode": {"optimize": sys.flags.optimize,
                 "isolated": sys.flags.isolated,
                 "no_site": sys.flags.no_site},
        "core_digest": digest,
        "core": core,
    }
    with open(OUT, "w", encoding="utf-8") as handle:
        json.dump(output, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(f"CORE_DIGEST={digest}")
    print("M25_SECOND_ENGINE=PASS")
    print("FULL_RANK_TO_CARRIER=REFUTED_LOCALLY")


if __name__ == "__main__":
    main()
