#!/usr/bin/env python3
"""Smallest balanced multi-ray no-clean-cap screen on the other P=2 orbit."""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from audit_other_p2_leakage import (
    BASE, BASE_AMPLITUDES, CELLS, EDGE_COLOUR, GONE, PHASES,
    LINEAR, balance_correction, canonical_support, enumerate_feasible,
    existing_mixed_cross, gadd, gconj, gmul, identity_caps,
    identity_response_support, insertion_map, mixed_inner, pcell, pmul,
    polynomial_source, qz_map, require, support_separated,
)


OUT = HERE / "results_other_p2_multiray.json"


def pair_key(left, right):
    return (left, right) if left < right else (right, left)


def phase_value(cells, phases, z_cross):
    words = set().union(*(LINEAR[cell] for cell in cells))
    value = Fraction(0)
    for word in words:
        if len(set(word)) == 1:
            continue
        total = (Fraction(0), Fraction(0))
        for cell, phase in zip(cells, phases):
            coefficient = LINEAR[cell].get(word, 0)
            total = gadd(total, (coefficient * phase[0],
                                 coefficient * phase[1]))
        value += gmul(total, gconj(total))[0]
    value += 2 * z_cross
    for i, j in combinations(range(len(cells)), 2):
        yy = existing_mixed_cross(insertion_map((cells[i], cells[j])))
        value += 2 * yy * gmul(phases[i], phases[j])[0]
    return value


def continuous_triangle_lower_bound(cells, z_cross):
    constant = sum(mixed_inner(LINEAR[cell], LINEAR[cell]) for cell in cells)
    constant += 2 * z_cross
    interaction_l1 = Fraction(0)
    interactions = []
    for i, j in combinations(range(len(cells)), 2):
        hermitian = mixed_inner(LINEAR[cells[i]], LINEAR[cells[j]])
        holomorphic = existing_mixed_cross(insertion_map((cells[i], cells[j])))
        interaction_l1 += abs(hermitian) + abs(holomorphic)
        if hermitian or holomorphic:
            interactions.append((i, j, hermitian, holomorphic))
    return constant - 2 * interaction_l1, interactions


def base_cap_triples():
    row = {"cells": (), "Z": {}}
    return tuple((cap["pair"][0], cap["pair"][1], centre)
                 for cap in identity_caps(row, ())
                 for centre in cap["centres"])


BASE_CAPS = base_cap_triples()


def has_frozen_clean_cap(cells):
    row = {"cells": tuple(cells)}
    return any(support_separated(row, p, q, centre)
               for p, q, centre in BASE_CAPS)


def carrier_class(edges):
    edges = tuple(sorted(set(edges)))
    if not edges:
        return None
    common = set(edges[0])
    for item in edges[1:]:
        common &= set(item)
    if common:
        return ("star", min(common))
    if all(set(left) & set(right) for left, right in combinations(edges, 2)):
        vertices = sorted(set().union(*map(set, edges)))
        if len(vertices) == 3:
            return ("triangle", tuple(vertices))
    return None


def exact_identity_carriers(cells, z, phases):
    row = {"cells": cells, "Z": z}
    source = polynomial_source(row, phases)
    answer = []
    for p, q in sorted(EDGE_COLOUR):
        response = identity_response_support(source, p, q)
        edges = tuple(sorted({item[0] for item in response}))
        kind = carrier_class(edges)
        if kind is not None:
            answer.append({"pair": (p, q), "kind": kind[0],
                           "carrier": kind[1], "edges": edges,
                           "response_cells": len(response)})
    return answer


# Polynomial arithmetic over Q, coefficients stored low degree first.  The
# four-cell terminal candidates have real minimizing phases, so Q(t) suffices.
PZERO = ()
PONE = (Fraction(1),)


def ptrim(poly):
    poly = tuple(poly)
    while poly and poly[-1] == 0:
        poly = poly[:-1]
    return poly


def paddq(left, right):
    return ptrim((left[i] if i < len(left) else 0) +
                 (right[i] if i < len(right) else 0)
                 for i in range(max(len(left), len(right))))


def psubq(left, right):
    return ptrim((left[i] if i < len(left) else 0) -
                 (right[i] if i < len(right) else 0)
                 for i in range(max(len(left), len(right))))


def pmulq(left, right):
    if not left or not right:
        return PZERO
    out = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            out[i + j] += x * y
    return ptrim(out)


def pscale(poly, scalar):
    return ptrim(scalar * value for value in poly)


def pdivmodq(numerator, denominator):
    require(denominator, "zero polynomial divisor")
    remainder = list(numerator)
    quotient = [Fraction(0)] * max(1, len(numerator) - len(denominator) + 1)
    while remainder and len(remainder) >= len(denominator):
        degree = len(remainder) - len(denominator)
        scalar = remainder[-1] / denominator[-1]
        quotient[degree] += scalar
        for index, value in enumerate(denominator):
            remainder[degree + index] -= scalar * value
        remainder = list(ptrim(remainder))
    return ptrim(quotient), ptrim(remainder)


def pgcd(left, right):
    while right:
        _, remainder = pdivmodq(left, right)
        left, right = right, remainder
    return pscale(left, 1 / left[-1]) if left else PZERO


def pexact_div(numerator, denominator):
    quotient, remainder = pdivmodq(numerator, denominator)
    require(not remainder, (numerator, denominator, remainder))
    return quotient


def normalize_poly_row(row):
    row = [ptrim(poly) for poly in row]
    common = PZERO
    for poly in row:
        if poly:
            common = poly if not common else pgcd(common, poly)
            if common == PONE:
                break
    if common and common != PONE:
        row = [pexact_div(poly, common) if poly else PZERO for poly in row]
    first = next((poly for poly in row if poly), PZERO)
    if first:
        row = [pscale(poly, 1 / first[-1]) for poly in row]
    return row


def polynomial_row_basis(rows):
    """Mutually pivot-reduced Q(t) row basis via fraction-free operations."""
    basis = []
    for raw in rows:
        vector = normalize_poly_row(raw)
        for pivot, base in basis:
            if vector[pivot]:
                bp, vp = base[pivot], vector[pivot]
                vector = normalize_poly_row([
                    psubq(pmulq(bp, x), pmulq(vp, y))
                    for x, y in zip(vector, base)])
        if not any(vector):
            continue
        pivot = next(i for i, poly in enumerate(vector) if poly)
        updated = []
        for old_pivot, base in basis:
            if base[pivot]:
                vp, bp = vector[pivot], base[pivot]
                base = normalize_poly_row([
                    psubq(pmulq(vp, x), pmulq(bp, y))
                    for x, y in zip(base, vector)])
            updated.append((old_pivot, base))
        updated.append((pivot, vector))
        basis = sorted(updated)
    return basis


def in_polynomial_rowspan(basis, raw):
    vector = normalize_poly_row(raw)
    for pivot, base in basis:
        if vector[pivot]:
            bp, vp = base[pivot], vector[pivot]
            vector = normalize_poly_row([
                psubq(pmulq(bp, x), pmulq(vp, y))
                for x, y in zip(vector, base)])
    return not any(vector)


def real_poly(polynomial):
    if not polynomial:
        return PZERO
    degree = max(polynomial)
    out = [Fraction(0)] * (degree + 1)
    for index, (real, imaginary) in polynomial.items():
        require(imaginary == 0, (index, imaginary))
        out[index] = real
    return ptrim(out)


def response_row(source, p, q, a, b, alpha, beta):
    answer = []
    for i in range(3):
        for j in range(3):
            polynomial = {}
            for left, right in (
                (pcell(source, p, a, i, alpha),
                 pcell(source, q, b, j, beta)),
                (pcell(source, p, b, i, beta),
                 pcell(source, q, a, j, alpha)),
            ):
                for degree, coefficient in pmul(left, right).items():
                    polynomial[degree] = gadd(
                        polynomial.get(degree, (Fraction(0), Fraction(0))),
                        coefficient)
            answer.append(real_poly(polynomial))
    return answer


def full_carrier_profile(cells, z, phases):
    """All 168 stars + 560 triangles, with four exact blocker memberships."""
    row = {"cells": cells, "Z": z}
    source = polynomial_source(row, phases)
    histogram = Counter()
    passing = []
    for p, q in combinations(range(8), 2):
        residual = tuple(v for v in range(8) if v not in (p, q))
        response_by_edge = {
            edge: [response_row(source, p, q, edge[0], edge[1], alpha, beta)
                   for alpha in range(3) for beta in range(3)]
            for edge in combinations(residual, 2)
        }
        activity = []
        for colour in range(3):
            vector = [PZERO] * 9
            vector[3 * colour + colour] = PONE
            activity.append(vector)
        activity.append([real_poly(pcell(source, p, q, i, j))
                         for i in range(3) for j in range(3)])
        carriers = [("star", centre,
                     {edge for edge in combinations(residual, 2)
                      if centre in edge})
                    for centre in residual]
        carriers += [("triangle", triangle, set(combinations(triangle, 2)))
                     for triangle in combinations(residual, 3)]
        all_edges = set(response_by_edge)
        for kind, carrier, allowed in carriers:
            rows = [vector for edge in sorted(all_edges - allowed)
                    for vector in response_by_edge[edge]]
            basis = polynomial_row_basis(rows)
            membership = tuple(in_polynomial_rowspan(basis, blocker)
                               for blocker in activity)
            mask = "".join("1" if item else "0" for item in membership)
            histogram[(kind, len(basis), mask)] += 1
            if not any(membership):
                passing.append({"pair": (p, q), "kind": kind,
                                "carrier": carrier, "rank": len(basis)})
    require(sum(histogram.values()) == 728, sum(histogram.values()))
    return passing, histogram


def logical_sha(payload):
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return sha256(raw).hexdigest()


def serialize_interactions(interactions):
    return [[i, j, str(h), str(s)] for i, j, h, s in interactions]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--mutate-positivity", action="store_true")
    args = parser.parse_args()

    ray_supports = sorted({tuple(sorted(row["cells"]))
                           for row in enumerate_feasible()})
    require(len(ray_supports) == 72, len(ray_supports))
    require(all(has_frozen_clean_cap(cells) for cells in ray_supports),
            "a single balanced ray already destroys every clean cap")

    literal_candidates = []
    orbit_candidates = {}
    overlap_skips = 0
    for left, right in combinations(ray_supports, 2):
        if set(left) & set(right):
            overlap_skips += 1
            continue
        cells = tuple(sorted(left + right))
        if has_frozen_clean_cap(cells):
            continue
        literal_candidates.append(cells)
        orbit_candidates.setdefault(canonical_support(cells), cells)

    distribution = Counter()
    records = []
    nonpositive_no_carrier = []
    full_audit_queue = []
    lower_bound_failures = []
    for row_index, (canonical, cells) in enumerate(sorted(orbit_candidates.items())):
        z = balance_correction(cells)
        require(z is not None, cells)
        z_cross = existing_mixed_cross(qz_map(z))
        exact_lower_bound, interactions = continuous_triangle_lower_bound(
            cells, z_cross)
        best = None
        minimizers = []
        for phases in product(PHASES, repeat=4):
            value = phase_value(cells, phases, z_cross)
            if best is None or value < best:
                best, minimizers = value, [phases]
            elif value == best:
                minimizers.append(phases)
        if args.mutate_positivity and row_index == 0:
            exact_lower_bound -= 1
        if best != exact_lower_bound:
            lower_bound_failures.append((cells, exact_lower_bound, best))
        distribution[best] += 1

        phase_carriers = []
        no_carrier_phases = []
        for phases in minimizers:
            carriers = exact_identity_carriers(cells, z, phases)
            phase_carriers.append(carriers)
            if not carriers:
                no_carrier_phases.append(phases)
        record = {
            "canonical_support": [list(cell) for cell in canonical],
            "literal_support": [list(cell) for cell in cells],
            "exact_continuous_P2_minimum": str(best),
            "triangle_inequality_lower_bound": str(exact_lower_bound),
            "gaussian_minimizer_count": len(minimizers),
            "interactions_i_j_hermitian_holomorphic": serialize_interactions(
                interactions),
            "every_minimizer_has_identity_star_or_triangle":
                not no_carrier_phases,
            "first_minimizer_carriers": [{
                "pair": list(item["pair"]), "kind": item["kind"],
                "carrier": (list(item["carrier"])
                            if isinstance(item["carrier"], tuple)
                            else item["carrier"]),
                "edges": [list(edge) for edge in item["edges"]],
            } for item in phase_carriers[0]],
        }
        records.append(record)
        if best <= 0 and no_carrier_phases:
            nonpositive_no_carrier.append({
                "record": record,
                "first_no_carrier_phase": [list(map(str, phase))
                                           for phase in no_carrier_phases[0]],
            })
            full_audit_queue.append((record, cells, z, no_carrier_phases[0]))

    print("base clean cap triples", len(BASE_CAPS), BASE_CAPS)
    print("balanced rays", len(ray_supports), "overlap skips", overlap_skips)
    print("literal/orbit minimal no-clean-cap supports",
          len(literal_candidates), len(orbit_candidates))
    print("exact P2 minimum distribution", dict(sorted(distribution.items())))
    print("continuous lower-bound failures", len(lower_bound_failures))
    print("nonpositive no identity carrier", len(nonpositive_no_carrier))
    for item in nonpositive_no_carrier[:10]:
        print("COUNTERCANDIDATE", item)

    require(not lower_bound_failures, lower_bound_failures[:1])
    full_audits = []
    terminal_full_countercandidate = None
    for record, cells, z, phases in full_audit_queue:
        print("full 728-carrier Q(t) audit", cells, flush=True)
        passing, histogram = full_carrier_profile(cells, z, phases)
        audit = {
            "canonical_support": record["canonical_support"],
            "phase": [list(map(str, phase)) for phase in phases],
            "passing_active_carriers": [{
                "pair": list(item["pair"]), "kind": item["kind"],
                "carrier": (list(item["carrier"])
                            if isinstance(item["carrier"], tuple)
                            else item["carrier"]),
                "outside_response_rank": item["rank"],
            } for item in passing],
            "profile_histogram": {
                f"{kind}:rank={rank}:membership={mask}": count
                for (kind, rank, mask), count in sorted(histogram.items())
            },
        }
        full_audits.append(audit)
        print("full carrier passes", len(passing),
              "profile bins", len(histogram), flush=True)
        if not passing:
            terminal_full_countercandidate = audit
            break

    status = ("PASS finite positivity certificate at first cap-destroying support"
              if min(distribution) > 0 else
              "PASS terminal zero-P2 full-carrier-evading candidate"
              if terminal_full_countercandidate else
              "PASS nonpositive candidates retain an active full carrier")
    payload = {
        "status": status,
        "base_support_separated_clean_cap_triples": len(BASE_CAPS),
        "minimality": {
            "all_72_single_balanced_rays_retain_a_clean_cap": True,
            "cells_per_candidate": 4,
            "construction": "union of two disjoint minimal balanced rays",
        },
        "literal_four_cell_no_clean_cap_supports": len(literal_candidates),
        "stabilizer_orbit_count": len(orbit_candidates),
        "orbit_P2_distribution": {str(k): v for k, v in sorted(distribution.items())},
        "minimum_exact_continuous_P2": str(min(distribution)),
        "lower_bound_certificate": (
            "For every orbit, P2 is its constant term plus real Hermitian and "
            "holomorphic pair interactions. The triangle-inequality lower "
            "bound constant-2*sum(abs(interactions)) is attained by an exact "
            "Gaussian phase assignment, hence is the continuous phase minimum."
        ),
        "nonpositive_no_identity_star_triangle_count":
            len(nonpositive_no_carrier),
        "full_728_carrier_audits": full_audits,
        "terminal_full_carrier_evading_candidate": terminal_full_countercandidate,
        "records": records,
        "scope": (
            "First support level in the semigroup generated by disjoint "
            "minimal balanced two-cell rays that destroys every frozen "
            "support-separated K=I clean cap. The carrier census is exact for "
            "all active K=I pair responses and classifies both stars and "
            "triangles. For queued zero candidates the full audit solves all "
            "728 outside-response rowspaces over Q(t) and tests the three "
            "diagonal plus direct-pair blockers. Positivity is local through "
            "second order."
        ),
    }
    payload["logical_sha256"] = logical_sha(payload)
    if args.write_results:
        OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("logical sha256", payload["logical_sha256"])
    require(status.startswith("PASS"), status)


if __name__ == "__main__":
    main()
