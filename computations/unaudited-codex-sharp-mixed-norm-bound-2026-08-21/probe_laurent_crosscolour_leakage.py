#!/usr/bin/env python3
"""Exact phase-minimized two-cell leakage Hessian at Laurent equality."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from probe_laurent_second_variation import (
    BASE, LAYERS, derivative_coefficients,
)


OUT = HERE / "results_laurent_crosscolour_leakage.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


CELLS = tuple(
    (u, v, a, b)
    for u, v in combinations(range(8), 2)
    for a in range(3) for b in range(3)
    if (u, v, a, b) not in BASE
)


def port_degrees(cells):
    degree = Counter()
    for u, v, a, b in cells:
        degree[u, a] += 1
        degree[v, b] += 1
    return degree


def balance_correction(cells):
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
                (colour, layer, z))
    return z


def mixed_inner(left, right):
    return sum(
        value * right.get(word, 0)
        for word, value in left.items()
        if len(set(word)) > 1
    )


def existing_mixed_cross(base, quadratic):
    return sum(
        base_value * quadratic.get(word, 0)
        for word, base_value in base.items()
        if len(set(word)) > 1
    )


def enumerate_feasible():
    linear = {}
    base = None
    for cell in CELLS:
        y = {cell: Fraction(1)}
        this_base, this_linear, _ = derivative_coefficients(y, {})
        if base is None:
            base = this_base
        else:
            require(this_base == base, "base profile changed")
        linear[cell] = this_linear

    feasible = []
    for left, right in combinations(CELLS, 2):
        if left[2] == left[3] and right[2] == right[3]:
            continue
        z = balance_correction((left, right))
        if z is None:
            continue
        _, _, qz = derivative_coefficients({}, z)
        _, _, qyy = derivative_coefficients(
            {left: Fraction(1), right: Fraction(1)}, {}
        )
        norm_left = mixed_inner(linear[left], linear[left])
        norm_right = mixed_inner(linear[right], linear[right])
        phase_difference = mixed_inner(linear[left], linear[right])
        z_cross = existing_mixed_cross(base, qz)
        phase_sum = existing_mixed_cross(base, qyy)
        constant = norm_left + norm_right + 2 * z_cross
        minimum = constant - 2 * abs(phase_difference) - 2 * abs(phase_sum)
        feasible.append({
            "cells": (left, right),
            "linear_norms": (norm_left, norm_right),
            "linear_overlap": phase_difference,
            "forced_Z_cross": z_cross,
            "YY_existing_cross": phase_sum,
            "phase_minimized_P2": minimum,
            "Z": z,
        })
    return feasible


def edge(u, v):
    return (u, v) if u < v else (v, u)


def transform_matching(matching, site_permutation):
    return tuple(sorted(edge(site_permutation[u], site_permutation[v])
                        for u, v in matching))


def laurent_stabilizer():
    layer_lookup = {tuple(sorted(value)): colour for colour, value in LAYERS.items()}
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
    require(len(answer) == 4, len(answer))
    return tuple(answer)


STABILIZER = laurent_stabilizer()


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


# Gaussian rational helpers, represented by (real, imaginary).
GZERO = (Fraction(0), Fraction(0))
GONE = (Fraction(1), Fraction(0))
GI = (Fraction(0), Fraction(1))
PHASES = (GONE, (-1, 0), GI, (0, -1))


def gadd(left, right):
    return (left[0] + right[0], left[1] + right[1])


def gmul(left, right):
    return (left[0] * right[0] - left[1] * right[1],
            left[0] * right[1] + left[1] * right[0])


def gconj(value):
    return (value[0], -value[1])


def greal(value):
    return value[0]


def phase_minimizer(row):
    best = None
    choices = []
    constant = (sum(row["linear_norms"])
                + 2 * row["forced_Z_cross"])
    for left_phase, right_phase in product(PHASES, repeat=2):
        value = constant
        value += 2 * row["linear_overlap"] * greal(
            gmul(left_phase, gconj(right_phase)))
        value += 2 * row["YY_existing_cross"] * greal(
            gmul(left_phase, right_phase))
        if best is None or value < best:
            best, choices = value, [(left_phase, right_phase)]
        elif value == best:
            choices.append((left_phase, right_phase))
    require(best == row["phase_minimized_P2"], (best, row))
    return choices[0], len(choices)


def padd(target, degree, coefficient):
    target[degree] = gadd(target.get(degree, GZERO), coefficient)
    if target[degree] == GZERO:
        del target[degree]


def pmul(left, right):
    answer = {}
    for left_degree, left_value in left.items():
        for right_degree, right_value in right.items():
            padd(answer, left_degree + right_degree, gmul(left_value, right_value))
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
                    for left, right in (
                        (pcell(source, p, a, colour, alpha),
                         pcell(source, q, b, colour, beta)),
                        (pcell(source, p, b, colour, beta),
                         pcell(source, q, a, colour, alpha)),
                    ):
                        for degree, coefficient in pmul(left, right).items():
                            padd(value, degree, coefficient)
                if value:
                    support.append(((a, b), (alpha, beta), value))
    return support


def identity_cap_screen(row, phases):
    source = polynomial_source(row, phases)
    caps = []
    for p, q in sorted({(u, v) for u, v, _, _ in BASE}):
        response = identity_response_support(source, p, q)
        centres = [site for site in range(8) if site not in (p, q)
                   and response and all(site in item[0] for item in response)]
        if centres:
            caps.append({"pair": (p, q), "centres": tuple(centres),
                         "response_cells": len(response)})
    return caps


def support_separated_identity_cap(row, p, q, centre):
    support = set(BASE) | set(row["cells"])

    def occupied(u, v, a, b):
        if u < v:
            return (u, v, a, b) in support
        return (v, u, b, a) in support

    residual = tuple(site for site in range(8) if site not in (p, q, centre))
    for colour in range(3):
        p_neighbours = [site for site in residual
                        if any(occupied(p, site, colour, alpha)
                               for alpha in range(3))]
        q_neighbours = [site for site in residual
                        if any(occupied(q, site, colour, alpha)
                               for alpha in range(3))]
        if any(left != right for left in p_neighbours for right in q_neighbours):
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
    feasible = enumerate_feasible()

    require(feasible, "no feasible leakage pairs")
    distribution = Counter(row["phase_minimized_P2"] for row in feasible)
    minimum = min(distribution)
    minimizers = [row for row in feasible if row["phase_minimized_P2"] == minimum]
    print("literal off-support cells", len(CELLS))
    print("feasible cross-colour two-cell rays", len(feasible))
    print("phase-minimized P2 distribution", dict(sorted(distribution.items())))
    print("minimum/count", minimum, len(minimizers))
    for row in minimizers[:30]:
        print("minimizer", row)
    nonpositive = [row for row in feasible if row["phase_minimized_P2"] <= 0]
    require(len(nonpositive) == 16, len(nonpositive))
    orbit_groups = defaultdict(list)
    for row in nonpositive:
        orbit_groups[canonical_support(row["cells"])].append(row)
    print("Laurent stabilizer", STABILIZER)
    print("nonpositive support orbits", len(orbit_groups),
          {key: len(value) for key, value in orbit_groups.items()})
    cap_counts = Counter()
    nonpositive_records = []
    for row_index, row in enumerate(nonpositive):
        phases, phase_count = phase_minimizer(row)
        caps = identity_cap_screen(row, phases)
        separated_caps = [cap for cap in caps
                          if any(support_separated_identity_cap(
                              row, cap["pair"][0], cap["pair"][1], centre)
                              for centre in cap["centres"])]
        if args.mutate_cap_ledger and row_index == 0:
            separated_caps = []
        require(separated_caps, ("no support-separated cap", row, caps))
        cap_counts[(row["phase_minimized_P2"], bool(caps))] += 1
        print("nonpositive", row["phase_minimized_P2"], row["cells"],
              "phases", phases, "phase_minimizers", phase_count,
              "identity_caps", caps, "support_separated", separated_caps)
        nonpositive_records.append({
            "P2": str(row["phase_minimized_P2"]),
            "cells": [list(cell) for cell in row["cells"]],
            "canonical_support": [list(cell) for cell in canonical_support(row["cells"])],
            "phase_minimizer_count": phase_count,
            "support_separated_caps": [
                {"pair": list(cap["pair"]), "centres": list(cap["centres"])}
                for cap in separated_caps
            ],
        })
    print("nonpositive cap ledger", dict(cap_counts))
    positive_cap_counts = Counter()
    positive_no_cap = []
    for row in feasible:
        if row["phase_minimized_P2"] <= 0:
            continue
        phases, _ = phase_minimizer(row)
        caps = identity_cap_screen(row, phases)
        separated = any(
            support_separated_identity_cap(
                row, cap["pair"][0], cap["pair"][1], centre)
            for cap in caps for centre in cap["centres"]
        )
        positive_cap_counts[(row["phase_minimized_P2"], separated)] += 1
        if not separated:
            positive_no_cap.append(row)
    print("positive-ray cap control", dict(positive_cap_counts))

    no_cap_orbits = defaultdict(list)
    for row in positive_no_cap:
        no_cap_orbits[canonical_support(row["cells"])].append(row)
    require(len(positive_no_cap) == 4 and len(no_cap_orbits) == 2,
            (len(positive_no_cap), len(no_cap_orbits)))
    require({row["phase_minimized_P2"] for row in positive_no_cap} == {Fraction(5)},
            positive_no_cap)
    payload = {
        "status": "PASS exact Laurent two-cell leakage/cap theorem",
        "literal_offsupport_cells": len(CELLS),
        "feasible_two_cell_extreme_rays": len(feasible),
        "laurent_stabilizer_order": len(STABILIZER),
        "P2_distribution": {str(key): value for key, value in sorted(distribution.items())},
        "nonpositive": {
            "count": len(nonpositive),
            "orbit_count": len(orbit_groups),
            "orbit_sizes": sorted(len(value) for value in orbit_groups.values()),
            "P2_counts": {str(key): value for key, value in sorted(
                Counter(row["phase_minimized_P2"] for row in nonpositive).items())},
            "every_ray_has_support_separated_active_identity_cap": True,
            "records": nonpositive_records,
        },
        "positive_control": {
            "count": len(feasible) - len(nonpositive),
            "cap_ledger": {
                f"P2={value},cap={cap}": count
                for (value, cap), count in sorted(positive_cap_counts.items(), key=str)
            },
        },
        "minimal_support_no_cap": {
            "minimum_number_of_extreme_rays": 1,
            "literal_ray_count": len(positive_no_cap),
            "stabilizer_orbit_count": len(no_cap_orbits),
            "orbit_sizes": sorted(len(value) for value in no_cap_orbits.values()),
            "phase_minimized_P2": "5",
            "phase_independent_reason": (
                "On both representatives linear overlap and YY existing-defect "
                "cross are zero; linear norms sum to 4 and forced Z contributes 1."
            ),
            "representatives": [
                [list(cell) for cell in key] for key in sorted(no_cap_orbits)
            ],
            "scope": (
                "No support-separated K=I Laurent cap survives. This is a "
                "minimal-support local statement, not exclusion of every K."
            ),
        },
        "theorem": (
            "Every nonpositive phase-minimized two-cell leakage ray is in the "
            "active clean-cap branch. The first supports destroying all frozen "
            "support-separated identity caps have strictly positive P2=5."
        ),
    }
    payload["logical_sha256"] = logical_sha(payload)
    if args.write_results:
        OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("minimal no-cap orbits", len(no_cap_orbits),
          {key: len(value) for key, value in no_cap_orbits.items()}, "P2=5")
    print("logical sha256", payload["logical_sha256"])


if __name__ == "__main__":
    main()
