#!/usr/bin/env python3
"""Exact Wick/annihilator projection audit for the N8 one-hot sector."""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "results_bosonic_gaussian_annihilator.json"
PINS = {
    "computations/unaudited-codex-zeon-contraction-hierarchy-2026-08-21/results_zeon_contraction_hierarchy.json":
        "0861f75b1cb729d1550673a8ff9252c0fb756ef455e8a1f4c218bb7dc9aa3cc7",
    "computations/unaudited-codex-graph-connection-hankel-audit-2026-08-21/results_graph_connection_hankel.json":
        "df3aab2562f7b1f92cafe01e0b1d2a93635b9fe6e3a3e4a50fffff0d4d21e8a5",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def perfect_matchings(labels):
    labels = tuple(labels)
    if not labels:
        yield ()
        return
    first = labels[0]
    for position, partner in enumerate(labels[1:], 1):
        rest = labels[1:position] + labels[position + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, partner),) + tail


def make_covariance():
    size = 24
    covariance = [[Fraction(0) for _ in range(size)] for _ in range(size)]
    for left in range(size):
        for right in range(left + 1, size):
            if left // 3 == right // 3:
                continue
            value = Fraction(1 + ((left + 1) * (right + 3)) % 11)
            covariance[left][right] = covariance[right][left] = value
    return covariance


def moment_oracle(covariance):
    @lru_cache(maxsize=None)
    def moment(labels):
        labels = tuple(sorted(labels))
        if not labels:
            return Fraction(1)
        if len(labels) % 2:
            return Fraction(0)
        first = labels[0]
        answer = Fraction(0)
        for position, partner in enumerate(labels[1:], 1):
            rest = labels[1:position] + labels[position + 1:]
            answer += covariance[first][partner] * moment(rest)
        return answer
    return moment


def recurrence_record(name, mu, residual, covariance, moment):
    residual = tuple(sorted(residual))
    lhs = moment(residual + (mu,))
    multiplicities = Counter(residual)
    rhs = Fraction(0)
    terms = []
    for nu, multiplicity in sorted(multiplicities.items()):
        reduced = list(residual)
        reduced.remove(nu)
        value = multiplicity * covariance[mu][nu] * moment(tuple(reduced))
        rhs += value
        terms.append({
            "nu": nu,
            "multiplicity": multiplicity,
            "term": str(value),
        })
    require(lhs == rhs, (name, lhs, rhs, terms))
    return {
        "name": name,
        "mu": mu,
        "residual_modes": list(residual),
        "lhs": str(lhs),
        "rhs": str(rhs),
        "distinct_rhs_terms": len(terms),
        "terms": terms,
    }


def partial_matching_profile(k):
    vertices = tuple(range(k))
    counts = Counter()
    # Select 2j vertices and perfectly match them; all others are live L factors.
    for pairs in range(k // 2 + 1):
        for chosen in combinations(vertices, 2 * pairs):
            counts[pairs] += sum(1 for _ in perfect_matchings(chosen))
    return {str(pairs): counts[pairs] for pairs in sorted(counts)}


def top_partition_counts():
    matchings = tuple(perfect_matchings(range(8)))
    require(len(matchings) == 105, len(matchings))
    output = {}
    for exposed_count in (1, 2, 3):
        exposed = frozenset(range(exposed_count))
        histogram = Counter()
        for matching in matchings:
            internal = sum(u in exposed and v in exposed for u, v in matching)
            crossing = sum((u in exposed) ^ (v in exposed) for u, v in matching)
            histogram[(internal, crossing)] += 1
        output[str(exposed_count)] = {
            f"internal_{internal}_crossing_{crossing}": count
            for (internal, crossing), count in sorted(histogram.items())
        }
    require(output == {
        "1": {"internal_0_crossing_1": 105},
        "2": {"internal_0_crossing_2": 90,
              "internal_1_crossing_0": 15},
        "3": {"internal_0_crossing_3": 60,
              "internal_1_crossing_1": 45},
    }, output)
    return output


def invisible_chord_lower_moments():
    base_edges = {(0, 1), (2, 3), (4, 5), (6, 7)}
    chord_edges = base_edges | {(0, 2)}
    delta = {}
    for degree in range(1, 5):
        base = set()
        chorded = set()
        for vertices in combinations(range(8), 2 * degree):
            for matching in perfect_matchings(vertices):
                normalized = frozenset((min(u, v), max(u, v)) for u, v in matching)
                if normalized <= base_edges:
                    base.add(normalized)
                if normalized <= chord_edges:
                    chorded.add(normalized)
        delta[str(degree)] = len(chorded - base)
    require(delta == {"1": 1, "2": 2, "3": 1, "4": 0}, delta)
    return delta


def logical_sha(payload):
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return sha256(raw).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    for relative, expected in PINS.items():
        observed = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(observed == expected, (relative, observed, expected))

    covariance = make_covariance()
    moment = moment_oracle(covariance)
    recurrences = [
        recurrence_record(
            "one-hole to one-photon-per-site N8",
            0,
            tuple(3 * site + site % 3 for site in range(1, 8)),
            covariance,
            moment,
        ),
        recurrence_record(
            "two-holes plus distinct-colour collision",
            3 * 6 + 2,
            (0, 1) + tuple(3 * site + site % 3 for site in range(1, 6)),
            covariance,
            moment,
        ),
        recurrence_record(
            "two-holes plus repeated-mode collision",
            3 * 6 + 2,
            (0, 0) + tuple(3 * site + site % 3 for site in range(1, 6)),
            covariance,
            moment,
        ),
    ]

    wick_profiles = {str(k): partial_matching_profile(k) for k in range(1, 5)}
    require(wick_profiles == {
        "1": {"0": 1},
        "2": {"0": 1, "1": 1},
        "3": {"0": 1, "1": 3},
        "4": {"0": 1, "1": 6, "2": 3},
    }, wick_profiles)

    payload = {
        "status": "PASS terminal Wick-recurrence no-go",
        "annihilator": "(a_mu - sum_nu A_mu,nu a_nu^dagger)|A>=0",
        "coefficient_recurrence": (
            "M(m+e_mu)=sum_nu m_nu A_mu,nu M(m-e_nu), "
            "where M is the derivative-normalized Gaussian moment."
        ),
        "exact_recurrence_controls": recurrences,
        "normal_order_partial_matching_profiles": wick_profiles,
        "N8_distinct_site_partition_counts": top_partition_counts(),
        "source_crosswalk": {
            "one_annihilator": "literal Laplace/site-down D_p q^[4]=l_p q^[3]",
            "two_annihilators": (
                "A_pr q^[3]+l_p l_r q^[2], the full-nine/carrier layer"
            ),
            "three_annihilators": (
                "three A*l*q^[2] terms plus l_p l_r l_s q, the 45+60 layer"
            ),
            "four_and_higher": (
                "the same Wick partial-matching formula; with all exposed "
                "colours retained, coordinates merely reindex the original rows"
            ),
        },
        "invisible_chord_new_lower_matchings_by_degree": invisible_chord_lower_moments(),
        "purity_scope": (
            "For every symmetric contraction A with analytic norm below one, "
            "the normalized exp(q)|0> is already a pure Gaussian. Covariance "
            "purity is therefore an identity after substituting A, not an "
            "additional constraint. It also uses complex conjugation and "
            "normalizability absent from the holomorphic algebraic source problem."
        ),
        "control_scope": {
            "n4": (
                "The exact GHZ4 matching witness satisfies every annihilator "
                "and commutator identity, so no universal Gaussian identity "
                "can itself contradict GHZ or select a unique bottleneck."
            ),
            "n6": (
                "The unrestricted n6 theorem is an emptiness theorem for the "
                "target coefficient fibre; Gaussian recurrences add no rows "
                "beyond those coefficients and do not independently reproduce it."
            ),
            "n8": (
                "The invisible chord changes q,q^[2],q^[3] by 1,2,1 matching "
                "terms while leaving q^[4] unchanged, and all parent identities "
                "remain valid. Lower hole/collision sectors are not target data."
            ),
        },
        "terminal_verdict": (
            "Projected Bogoliubov equations and their canonical-commutator "
            "closures are exactly Wick/Laplace recurrence. They reproduce the "
            "literal site-down/carrier rows and introduce unconstrained "
            "collision sectors, but no new source-faithful global relation or cap criterion."
        ),
        "input_hashes": PINS,
    }
    payload["logical_sha256"] = logical_sha(payload)
    if args.write_results:
        OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("bosonic Gaussian annihilator audit: PASS terminal Wick no-go")
    print("partial-matching profiles k=1..4:", wick_profiles)
    print("N8 partition counts:", payload["N8_distinct_site_partition_counts"])
    print("invisible chord lower deltas:",
          payload["invisible_chord_new_lower_matchings_by_degree"])
    print("logical sha256:", payload["logical_sha256"])


if __name__ == "__main__":
    main()
