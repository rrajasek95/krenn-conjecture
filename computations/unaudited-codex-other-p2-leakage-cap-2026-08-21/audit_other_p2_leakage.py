#!/usr/bin/env python3
"""Exact two-cell leakage/cap audit on the (4+4,8,8) diagonal P=2 orbit.

This checker rebuilds amplitude derivatives from literal matching completions;
it does not import the Laurent-orbit second-variation formulas.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_other_p2_leakage.json"


LAYERS = {
    0: ((0, 1), (2, 3), (4, 5), (6, 7)),
    1: ((0, 2), (1, 3), (4, 6), (5, 7)),
    2: ((0, 3), (1, 4), (2, 7), (5, 6)),
}
BASE = frozenset((u, v, colour, colour)
                 for colour, matching in LAYERS.items()
                 for u, v in matching)
EDGE_COLOUR = {(u, v): colour
               for colour, matching in LAYERS.items()
               for u, v in matching}
CELLS = tuple((u, v, a, b)
              for u, v in combinations(range(8), 2)
              for a in range(3) for b in range(3)
              if (u, v, a, b) not in BASE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    left = vertices[0]
    for index in range(1, len(vertices)):
        right = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield ((left, right),) + tail


MATCHINGS8 = tuple(perfect_matchings(range(8)))


def insertion_map(cells):
    """Amplitude coefficient from prescribed literal source cells.

    Remaining vertices must be completed entirely with the twelve frozen
    diagonal anchor cells. Each physical edge occurs in at most one layer.
    """
    word0 = [None] * 8
    used = set()
    for u, v, a, b in cells:
        if u in used or v in used:
            return Counter()
        used.update((u, v))
        word0[u], word0[v] = a, b
    answer = Counter()
    remaining = tuple(v for v in range(8) if v not in used)
    for matching in perfect_matchings(remaining):
        word = list(word0)
        for u, v in matching:
            e = (u, v) if u < v else (v, u)
            colour = EDGE_COLOUR.get(e)
            if colour is None:
                break
            word[u] = word[v] = colour
        else:
            answer[tuple(word)] += 1
    return answer


def base_amplitudes():
    answer = Counter()
    for matching in MATCHINGS8:
        word = [None] * 8
        for u, v in matching:
            e = (u, v) if u < v else (v, u)
            colour = EDGE_COLOUR.get(e)
            if colour is None:
                break
            word[u] = word[v] = colour
        else:
            answer[tuple(word)] += 1
    return answer


BASE_AMPLITUDES = base_amplitudes()
LINEAR = {cell: insertion_map((cell,)) for cell in CELLS}


def port_degrees(cells):
    degree = Counter()
    for u, v, a, b in cells:
        degree[u, a] += 1
        degree[v, b] += 1
    return degree


def balance_correction(cells):
    """Unique diagonal Z preserving all 24 port norms through order two."""
    degree = port_degrees(cells)
    z = {}
    for colour, layer in LAYERS.items():
        edge_degrees = []
        for u, v in layer:
            if degree[u, colour] != degree[v, colour]:
                return None
            edge_degrees.append(degree[u, colour])
        common = Fraction(sum(edge_degrees), 4)
        for (u, v), value in zip(layer, edge_degrees):
            z[(u, v, colour, colour)] = (common - value) / 2
        require(sum(z[u, v, colour, colour] for u, v in layer) == 0,
                (colour, z))
    return z


def mixed_inner(left, right):
    return sum(value * right.get(word, 0)
               for word, value in left.items() if len(set(word)) > 1)


def existing_mixed_cross(quadratic):
    return sum(value * quadratic.get(word, 0)
               for word, value in BASE_AMPLITUDES.items()
               if len(set(word)) > 1)


def qz_map(z):
    answer = Counter()
    for cell, scalar in z.items():
        for word, value in insertion_map((cell,)).items():
            answer[word] += scalar * value
    return answer


def enumerate_feasible():
    feasible = []
    for left, right in combinations(CELLS, 2):
        # The extreme-ray convention excludes two purely diagonal insertions.
        if left[2] == left[3] and right[2] == right[3]:
            continue
        z = balance_correction((left, right))
        if z is None:
            continue
        yy = insertion_map((left, right))
        nl = mixed_inner(LINEAR[left], LINEAR[left])
        nr = mixed_inner(LINEAR[right], LINEAR[right])
        ld = mixed_inner(LINEAR[left], LINEAR[right])
        zc = existing_mixed_cross(qz_map(z))
        sc = existing_mixed_cross(yy)
        constant = nl + nr + 2 * zc
        minimum = constant - 2 * abs(ld) - 2 * abs(sc)
        feasible.append({
            "cells": (left, right), "linear_norms": (nl, nr),
            "linear_overlap": ld, "forced_Z_cross": zc,
            "YY_existing_cross": sc, "phase_minimized_P2": minimum,
            "Z": z,
        })
    return feasible


def edge(u, v):
    return (u, v) if u < v else (v, u)


def transform_matching(matching, site_permutation):
    return tuple(sorted(edge(site_permutation[u], site_permutation[v])
                        for u, v in matching))


def stabilizer():
    layer_lookup = {tuple(sorted(value)): colour
                    for colour, value in LAYERS.items()}
    answer = []
    for site_permutation in permutations(range(8)):
        colour_permutation = []
        for colour in range(3):
            transformed = transform_matching(LAYERS[colour], site_permutation)
            if transformed not in layer_lookup:
                break
            colour_permutation.append(layer_lookup[transformed])
        else:
            require(len(set(colour_permutation)) == 3, colour_permutation)
            answer.append((site_permutation, tuple(colour_permutation)))
    return tuple(answer)


STABILIZER = stabilizer()


def transform_cell(cell, symmetry):
    site_permutation, colour_permutation = symmetry
    u, v, a, b = cell
    u, v = site_permutation[u], site_permutation[v]
    a, b = colour_permutation[a], colour_permutation[b]
    if u > v:
        u, v, a, b = v, u, b, a
    return (u, v, a, b)


def canonical_support(cells):
    return min(tuple(sorted(transform_cell(cell, symmetry) for cell in cells))
               for symmetry in STABILIZER)


# Exact Gaussian rationals as (real, imaginary).
GZERO = (Fraction(0), Fraction(0))
GONE = (Fraction(1), Fraction(0))
PHASES = (GONE, (-1, 0), (0, 1), (0, -1))


def gadd(left, right):
    return (left[0] + right[0], left[1] + right[1])


def gmul(left, right):
    return (left[0] * right[0] - left[1] * right[1],
            left[0] * right[1] + left[1] * right[0])


def gconj(value):
    return (value[0], -value[1])


def phase_minimizer(row):
    best = None
    choices = []
    constant = sum(row["linear_norms"]) + 2 * row["forced_Z_cross"]
    for lp, rp in product(PHASES, repeat=2):
        value = constant
        value += 2 * row["linear_overlap"] * gmul(lp, gconj(rp))[0]
        value += 2 * row["YY_existing_cross"] * gmul(lp, rp)[0]
        if best is None or value < best:
            best, choices = value, [(lp, rp)]
        elif value == best:
            choices.append((lp, rp))
    require(best == row["phase_minimized_P2"], (best, row))
    return choices[0], len(choices)


def padd(target, degree, coefficient):
    target[degree] = gadd(target.get(degree, GZERO), coefficient)
    if target[degree] == GZERO:
        del target[degree]


def pmul(left, right):
    answer = {}
    for dl, vl in left.items():
        for dr, vr in right.items():
            padd(answer, dl + dr, gmul(vl, vr))
    return answer


def polynomial_source(row, phases):
    source = {cell: {0: GONE} for cell in BASE}
    for cell, phase in zip(row["cells"], phases):
        source[cell] = {1: phase}
    for cell, value in row["Z"].items():
        padd(source[cell], 2, (value, Fraction(0)))
    return source


def pcell(source, u, v, a, b):
    if u < v:
        return source.get((u, v, a, b), {})
    return source.get((v, u, b, a), {})


def identity_response_support(source, p, q):
    residual = tuple(site for site in range(8) if site not in (p, q))
    support = []
    for a, b in combinations(residual, 2):
        for alpha in range(3):
            for beta in range(3):
                value = {}
                for colour in range(3):
                    terms = (
                        (pcell(source, p, a, colour, alpha),
                         pcell(source, q, b, colour, beta)),
                        (pcell(source, p, b, colour, beta),
                         pcell(source, q, a, colour, alpha)),
                    )
                    for left, right in terms:
                        for degree, coefficient in pmul(left, right).items():
                            padd(value, degree, coefficient)
                if value:
                    support.append(((a, b), (alpha, beta), value))
    return support


def identity_caps(row, phases):
    source = polynomial_source(row, phases)
    caps = []
    for p, q in sorted(EDGE_COLOUR):
        trace = {}
        for colour in range(3):
            for degree, coefficient in pcell(source, p, q, colour, colour).items():
                padd(trace, degree, coefficient)
        # The K=I blocker is active: its direct pair scalar has constant one.
        require(trace.get(0) == GONE, ((p, q), trace))
        response = identity_response_support(source, p, q)
        centres = [v for v in range(8) if v not in (p, q)
                   and response and all(v in item[0] for item in response)]
        if centres:
            caps.append({"pair": (p, q), "centres": tuple(centres),
                         "response_cells": len(response),
                         "direct_trace_constant": 1})
    return caps


def support_separated(row, p, q, centre):
    support = set(BASE) | set(row["cells"])

    def occupied(u, v, a, b):
        if u < v:
            return (u, v, a, b) in support
        return (v, u, b, a) in support

    residual = tuple(v for v in range(8) if v not in (p, q, centre))
    for colour in range(3):
        pn = [v for v in residual
              if any(occupied(p, v, colour, alpha) for alpha in range(3))]
        qn = [v for v in residual
              if any(occupied(q, v, colour, alpha) for alpha in range(3))]
        if any(left != right for left in pn for right in qn):
            return False
    return True


def logical_sha(payload):
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return sha256(raw).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--mutate-cap-ledger", action="store_true")
    args = parser.parse_args()

    require(BASE_AMPLITUDES == Counter({
        (0,) * 8: 1, (1,) * 8: 1, (2,) * 8: 1,
        (0, 0, 0, 0, 1, 1, 1, 1): 1,
        (1, 1, 1, 1, 0, 0, 0, 0): 1,
    }), BASE_AMPLITUDES)
    feasible = enumerate_feasible()
    require(feasible, "no balanced rays")
    distribution = Counter(row["phase_minimized_P2"] for row in feasible)
    nonpositive = [row for row in feasible
                   if row["phase_minimized_P2"] <= 0]
    orbit_groups = defaultdict(list)
    for row in nonpositive:
        orbit_groups[canonical_support(row["cells"])].append(row)

    records = []
    failures = []
    for index, row in enumerate(nonpositive):
        phases, phase_count = phase_minimizer(row)
        caps = identity_caps(row, phases)
        separated = [{"pair": cap["pair"], "centres": tuple(
            centre for centre in cap["centres"]
            if support_separated(row, cap["pair"][0], cap["pair"][1], centre))}
                     for cap in caps]
        separated = [cap for cap in separated if cap["centres"]]
        if args.mutate_cap_ledger and index == 0:
            separated = []
        if not separated:
            failures.append((row, caps))
        records.append({
            "P2": str(row["phase_minimized_P2"]),
            "cells": [list(cell) for cell in row["cells"]],
            "canonical_support": [list(cell) for cell in
                                  canonical_support(row["cells"])],
            "phase_minimizer_count": phase_count,
            "support_separated_caps": [
                {"pair": list(cap["pair"]), "centres": list(cap["centres"])}
                for cap in separated],
        })

    print("base amplitudes", BASE_AMPLITUDES)
    print("off-support cells", len(CELLS))
    print("stabilizer order", len(STABILIZER))
    print("feasible rays", len(feasible))
    print("P2 distribution", dict(sorted(distribution.items())))
    print("nonpositive count/orbits", len(nonpositive), len(orbit_groups),
          sorted(len(rows) for rows in orbit_groups.values()))
    print("nonpositive cap failures", len(failures))
    for row, caps in failures[:20]:
        print("FAIL", row, "raw caps", caps)

    payload = {
        "status": ("PASS equality-orbit-wide local energy-to-cap test"
                   if not failures else
                   "FAIL nonpositive balanced ray without separated identity cap"),
        "canonical_layers": {str(c): [list(e) for e in layer]
                             for c, layer in LAYERS.items()},
        "base_amplitudes": {"".join(map(str, w)): value
                            for w, value in sorted(BASE_AMPLITUDES.items())},
        "pair_cycle_types": ["4+4", "8", "8"],
        "union_triangles": 4,
        "literal_offsupport_cells": len(CELLS),
        "stabilizer_order": len(STABILIZER),
        "feasible_two_cell_balanced_rays": len(feasible),
        "P2_distribution": {str(k): v for k, v in sorted(distribution.items())},
        "nonpositive": {
            "count": len(nonpositive), "orbit_count": len(orbit_groups),
            "orbit_sizes": sorted(len(rows) for rows in orbit_groups.values()),
            "P2_counts": {str(k): v for k, v in sorted(Counter(
                row["phase_minimized_P2"] for row in nonpositive).items())},
            "every_ray_has_support_separated_active_identity_cap": not failures,
            "failure_count": len(failures), "records": records,
        },
        "scope": (
            "All minimal two-cell extreme rays admitting the unique diagonal "
            "second-order port-norm correction; phases minimized exactly over "
            "Gaussian representatives, which attain the analytic minimum. "
            "Caps are active K=I pair carriers with star response and the "
            "frozen support-separation guard. This is local through order two."
        ),
    }
    payload["logical_sha256"] = logical_sha(payload)
    if args.write_results:
        OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("logical sha256", payload["logical_sha256"])
    require(not failures, (len(failures), failures[:1]))


if __name__ == "__main__":
    main()
