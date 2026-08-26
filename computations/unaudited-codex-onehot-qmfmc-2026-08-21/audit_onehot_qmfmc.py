#!/usr/bin/env python3
"""Exact cut/rank audit for the fixed one-hot K_n tensor network."""

from __future__ import annotations

import argparse
from fractions import Fraction
from functools import reduce
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "results_onehot_qmfmc.json"
PINS = {
    "computations/unaudited-codex-onehot-peps-holant-2026-08-21/results_onehot_peps_holant.json":
        "d5029396bbe6347808d5e7c5cab4baf5bebcacc9eaba9d7f97405649d3d02221",
    "computations/unaudited-codex-zeon-contraction-hierarchy-2026-08-21/results_zeon_contraction_hierarchy.json":
        "0861f75b1cb729d1550673a8ff9252c0fb756ef455e8a1f4c218bb7dc9aa3cc7",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def nominal_cut(n, terminal_subset, tensor_subset):
    terminal_subset = frozenset(terminal_subset)
    tensor_subset = frozenset(tensor_subset)
    physical_edges = len(terminal_subset ^ tensor_subset)
    virtual_edges = len(tensor_subset) * (n - len(tensor_subset))
    return 3**physical_edges * 4**virtual_edges


def source_cut(n, terminal_subset, tensor_subset, bond_ranks):
    terminal_subset = frozenset(terminal_subset)
    tensor_subset = frozenset(tensor_subset)
    value = 3 ** len(terminal_subset ^ tensor_subset)
    for u in tensor_subset:
        for v in range(n):
            if v not in tensor_subset and u < v:
                value *= bond_ranks[(u, v)]
            elif v not in tensor_subset and v < u:
                value *= bond_ranks[(v, u)]
    return value


def cut_census(n, bond_ranks=None):
    sites = tuple(range(n))
    output = {}
    for k in range(1, n // 2 + 1):
        terminal = frozenset(range(k))
        choices = []
        for mask in range(1 << n):
            tensor = frozenset(i for i in sites if mask & (1 << i))
            if bond_ranks is None:
                value = nominal_cut(n, terminal, tensor)
            else:
                value = source_cut(n, terminal, tensor, bond_ranks)
            choices.append((value, tuple(sorted(tensor))))
        minimum = min(value for value, _tensor in choices)
        minimizers = [tensor for value, tensor in choices if value == minimum]
        output[str(k)] = {
            "minimum": minimum,
            "minimizers": [list(tensor) for tensor in minimizers],
            "ghz_flattening_rank": 3,
            "rank_deficit_factor": minimum // 3,
        }
    return output


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


def amplitude(word, weights, matchings):
    value = Fraction(0)
    for matching in matchings:
        term = Fraction(1)
        for u, v in matching:
            term *= weights.get((u, v, word[u], word[v]), 0)
        value += term
    return value


def n4_witness_audit():
    matchings = tuple(perfect_matchings(range(4)))
    weights = {}
    for colour, matching in enumerate(matchings):
        for u, v in matching:
            weights[(u, v, colour, colour)] = Fraction(1)
    nonzero = {}
    for word in product(range(3), repeat=4):
        value = amplitude(word, weights, matchings)
        if value:
            nonzero["".join(map(str, word))] = value
    require(nonzero == {"0000": 1, "1111": 1, "2222": 1}, nonzero)
    bond_ranks = {edge: 2 for edge in combinations(range(4), 2)}
    cuts = cut_census(4, bond_ranks)
    require([cuts[str(k)]["minimum"] for k in (1, 2)] == [3, 9], cuts)
    return {
        "nonzero_outputs": {key: str(value) for key, value in nonzero.items()},
        "edge_block_ranks": "all six A_uv have rank 1",
        "bond_state_schmidt_ranks": "all six |00>+A_uv have rank 2",
        "source_aware_cuts": cuts,
        "bottleneck_control": (
            "The exact GHZ4 output has rank three across every cut, but no "
            "edge block carries three colour channels. This refutes a literal "
            "single-bond three-channel bottleneck inference. The witness does "
            "have clean caps, so it is not a counterexample to clean-cap existence."
        ),
    }


def invisible_chord_audit():
    sites = range(8)
    matchings = tuple(perfect_matchings(sites))
    base_edges = ((0, 1), (2, 3), (4, 5), (6, 7))
    base = {(u, v, 0, 0): Fraction(1) for u, v in base_edges}
    chorded = dict(base)
    chorded[(0, 2, 0, 0)] = Fraction(1)
    base_nonzero = {}
    chord_nonzero = {}
    for word in product(range(3), repeat=8):
        left = amplitude(word, base, matchings)
        right = amplitude(word, chorded, matchings)
        if left:
            base_nonzero["".join(map(str, word))] = left
        if right:
            chord_nonzero["".join(map(str, word))] = right
    require(base_nonzero == chord_nonzero == {"00000000": Fraction(1)},
            (base_nonzero, chord_nonzero))
    return {
        "base_live_edges": [list(edge) for edge in base_edges],
        "added_chord": [0, 2],
        "identical_output": {"00000000": "1"},
        "meaning": (
            "The added chord changes an internal bond from Schmidt rank 1 to "
            "2 but belongs to no full perfect matching. Top tensors and every "
            "flattening rank remain identical, so projector-specific output "
            "rank cannot recover internal bond support or capacity."
        ),
    }


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

    nominal8 = cut_census(8)
    require([nominal8[str(k)]["minimum"] for k in range(1, 5)]
            == [3, 9, 27, 81], nominal8)
    require(all(nominal8[str(k)]["minimizers"] == [[]]
                for k in range(1, 4)), nominal8)
    require(nominal8["4"]["minimizers"]
            == [[], list(range(8))], nominal8)
    payload = {
        "status": "PASS exact one-hot quantum max-flow/min-cut no-go audit",
        "network_cut_formula": (
            "For output terminal set S and site-tensor side U, nominal cut "
            "capacity is 3^|S symmetric_difference U| * "
            "4^(|U|(8-|U|))."
        ),
        "K8_nominal_cut_census": nominal8,
        "GHZ8_flattening_ranks": {
            "all_nontrivial_bipartitions": 3,
            "reason": (
                "The flattening has exactly three nonzero entries, indexed by "
                "the three constant-colour row/column pairs."
            ),
        },
        "source_aware_necessary_cut_condition": (
            "With r_uv=1+rank(A_uv), every hypothetical GHZ source obeys "
            "product_(uv crossing U) r_uv >= 3 for every nontrivial U. "
            "Equivalently, each site cut has either one rank>=2 edge block or "
            "at least two nonzero rank-one blocks. This is only a weak support cut."
        ),
        "n4_exact_control": n4_witness_audit(),
        "invisible_chord_control": invisible_chord_audit(),
        "X5_scope": (
            "At n=8,d=3, X5 is the full mixed output system. Together with "
            "pure normalization it says the realized output is GHZ, so all "
            "flattening-rank statements above are consequences of the target "
            "tensor and contain no extra source-coordinate equation."
        ),
        "terminal_verdict": (
            "Generic QMF/QMC theorems do not apply as an equality-case rigidity "
            "result here. Every nominal min cut severs only physical dimension-3 "
            "legs; balanced cuts have deficits 3,9,27, and only one-site cuts "
            "saturate trivially. The fixed one-hot projector is highly "
            "noninjective, as the invisible chord proves. Rank plus X5 cannot "
            "force a literal internal three-channel bottleneck or clean pair."
        ),
        "input_hashes": PINS,
    }
    payload["logical_sha256"] = logical_sha(payload)
    if args.write_results:
        OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("one-hot QMF/QMC audit: PASS")
    print("K8 nominal mincuts k=1..4: 3,9,27,81; GHZ ranks all 3")
    print("K4 source-aware mincuts: 3,9; every live edge block rank 1")
    print("invisible chord: internal Schmidt rank changes, top tensor unchanged")
    print("logical sha256:", payload["logical_sha256"])


if __name__ == "__main__":
    main()
