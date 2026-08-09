#!/usr/bin/env python3
"""Exact anchor-normal-form cover for the N=8 D1 m=7 support frontier."""

from __future__ import annotations

import importlib
import itertools
import os
import sys
from collections import Counter
from hashlib import sha256
from time import monotonic

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


PINNED_COVER_SHA256 = (
    "77f561ed78d9d2bfbd065541274299cd72d226f6a2a19a2e90faf7d74b4bbcc7"
)
SOURCE = os.path.join(HERE, "verify_n8_d1_minimal_off_sigma_support_cover.py")
with open(SOURCE, "rb") as handle:
    SOURCE_SHA256 = sha256(handle.read()).hexdigest()
require(SOURCE_SHA256 == PINNED_COVER_SHA256,
        "the committed D1 support source changed")
V = importlib.import_module("verify_n8_d1_minimal_off_sigma_support_cover")
D = V.D

EXPECTED_LEDGER_SHA256 = (
    "b6a1e7319e182358e21e196e4d64a33ae3f848b54882e78433d845609a8f5ffd"
)


def triple_states(colour):
    return [(row["extras"], frozenset((row["anchor_factor"],)))
            for row in V.anchor_signatures(colour)]


def special_four_supports(colour):
    """The 4-SR bijections and unions of two residue matchings."""
    all_sr = {
        frozenset(V.cell(site, residue, colour, colour)
                  for site, residue in zip(V.SMALL, image))
        for image in itertools.permutations(V.RESIDUE)
    }
    residue_matchings = list(V.MATCHINGS[V.RESIDUE])
    double_rr = {
        frozenset(V.cell(u, v, colour, colour)
                  for u, v in set(first) | set(second))
        for first, second in itertools.combinations(residue_matchings, 2)
    }
    require(len(all_sr) == 24 and len(double_rr) == 3,
            "the constructive special-four census changed")

    # Independent exhaustive classification among the 22 monochrome cells.
    rr = {V.cell(u, v, colour, colour)
          for u, v in itertools.combinations(V.RESIDUE, 2)}
    sr = {V.cell(u, r, colour, colour)
          for u in V.SMALL for r in V.RESIDUE}
    triples = {row["extras"] for row in V.anchor_signatures(colour)}
    full_traces = []
    for matching in D.C.perfect_matchings(V.SITES):
        trace = frozenset(
            V.cell(u, v, colour, colour) for u, v in matching
            if set((u, v)) & set(V.RESIDUE)
        )
        full_traces.append(trace)
    residue_pms = [frozenset(V.cell(u, v, colour, colour)
                             for u, v in matching)
                   for matching in residue_matchings]
    exhaustive = set()
    for chosen in itertools.combinations(sorted(rr | sr), 4):
        support = frozenset(chosen)
        if not any(trace <= support for trace in full_traces):
            continue
        if any(trace <= support for trace in triples):
            continue
        if sum(matching <= support for matching in residue_pms) == 1:
            continue
        exhaustive.add(support)
    require(exhaustive == all_sr | double_rr,
            "four-cell anchor supports without a 3-trace were omitted")

    small_matchings = list(D.C.perfect_matchings(V.SMALL))
    states = [(support, frozenset()) for support in sorted(all_sr, key=sorted)]
    for support in sorted(double_rr, key=sorted):
        for matching in small_matchings:
            units = frozenset(V.cell(u, v, colour, colour)
                              for u, v in matching)
            states.append((support, units))
    require(len(states) == 33, "special-four branch count changed")
    return states, {"all_SR": len(all_sr), "double_RR": len(double_rr),
                    "unit_branches": len(states)}


def map_set(values, mapping):
    return frozenset(V.map_cell(entry, mapping) for entry in values)


def state_key(state):
    return tuple(sorted(state[0])), tuple(sorted(state[1]))


def state_orbit(state, group):
    extras, units = state
    return {(map_set(extras, mapping), map_set(units, mapping))
            for mapping in group}


def unique_certificate(state, sigma, base_units):
    extras, anchor_units = state
    allowed = sigma | set(extras)
    mandatory = base_units | set(extras) | set(anchor_units)
    for domain in (V.RESIDUE, V.W1, V.W2, V.SITES):
        for matching in V.MATCHINGS[tuple(domain)]:
            choices = []
            for u, v in matching:
                on_edge = [entry for entry in sorted(mandatory)
                           if entry[:2] == (u, v)]
                if not on_edge:
                    break
                choices.append(on_edge)
            else:
                for selected in itertools.product(*choices):
                    word = {}
                    for u, v, i, j in selected:
                        word[u], word[v] = i, j
                    pure = (len(set(word.values())) == 1
                            if domain == V.SITES
                            else set(word.values()) == {2})
                    if pure:
                        continue
                    live = []
                    for other in V.MATCHINGS[tuple(domain)]:
                        cells = tuple(V.cell(u, v, word[u], word[v])
                                      for u, v in other)
                        if all(entry in allowed for entry in cells):
                            live.append(cells)
                    if len(live) == 1 and set(live[0]) <= mandatory:
                        return {"domain": len(domain),
                                "word": [word[site] for site in domain],
                                "matching": [list(entry) for entry in live[0]]}
    return None


def audit():
    started = monotonic()
    _admissible, sigma, off_sigma, _kinds = V.reconstruct_support_domains()
    b3, c3 = triple_states(0), triple_states(1)
    b4, b4_counts = special_four_supports(0)
    c4, c4_counts = special_four_supports(1)

    states = set()
    for b_extra, b_units in b3:
        for c_extra, c_units in c3:
            six = b_extra | c_extra
            for extra in off_sigma - six:
                states.add((frozenset(six | {extra}),
                            frozenset(b_units | c_units)))
    states.update((frozenset(b_extra | c_extra),
                   frozenset(b_units | c_units))
                  for b_extra, b_units in b3
                  for c_extra, c_units in c4)
    states.update((frozenset(b_extra | c_extra),
                   frozenset(b_units | c_units))
                  for b_extra, b_units in b4
                  for c_extra, c_units in c3)
    labelled_states = len(states)
    labelled_supports = len({state[0] for state in states})
    require(labelled_states == 637200 and labelled_supports == 615600,
            "the complete m=7 anchor-state census changed")

    group = V.d1_group()
    orbit_representatives = []
    while states:
        seed = next(iter(states))
        orbit = state_orbit(seed, group)
        states -= orbit
        orbit_representatives.append(min(orbit, key=state_key))
    orbit_representatives.sort(key=state_key)
    require(len(orbit_representatives) == 14120,
            "the m=7 anchor states no longer have 14120 orbits")

    base_units = set(V.BASE_UNITS) | {
        V.cell(0, 2, 2, 2), V.cell(1, 3, 2, 2),
    }
    tally = Counter()
    examples = {}
    survivors = []
    for state in orbit_representatives:
        certificate = unique_certificate(state, sigma, base_units)
        if certificate is None:
            survivors.append(state)
        else:
            tally[certificate["domain"]] += 1
            examples.setdefault(str(certificate["domain"]), certificate)
    require(tally == {4: 3672, 6: 8229, 8: 2193}
            and len(survivors) == 26,
            "the m=7 unique-monomial orbit cover changed")

    support_orbits = {
        min(tuple(sorted(map_set(state[0], mapping))) for mapping in group)
        for state in survivors
    }
    require(len(support_orbits) == 22,
            "the 26 branch survivors no longer project to 22 support orbits")
    survivor_payload = [
        {"extras": [list(entry) for entry in sorted(extras)],
         "anchor_units": [list(entry) for entry in sorted(units)]}
        for extras, units in survivors
    ]
    ledger = {
        "pinned_cover_sha256": SOURCE_SHA256,
        "normal_forms": {"three_trace_per_colour": 72,
                         "special_four_b": b4_counts,
                         "special_four_c": c4_counts},
        "labelled_branch_states": labelled_states,
        "labelled_off_supports": labelled_supports,
        "symmetry_group": len(group),
        "branch_state_orbits": len(orbit_representatives),
        "unique_monomial_kills_by_domain": dict(sorted(tally.items())),
        "certificate_examples": examples,
        "survivor_branch_orbits": len(survivors),
        "survivor_off_support_orbits": len(support_orbits),
        "survivors": survivor_payload,
        "survivor_sha256": D.content_hash(survivor_payload),
        "status": ("exact support certificates reduce m=7 to 26 anchor-unit "
                   "branches over 22 off-support orbits; support-SAT and "
                   "exact ideals remain open"),
    }
    digest = D.content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "the m=7 anchor-normal-form ledger changed")
    return ledger, digest, monotonic() - started


def main():
    ledger, digest, seconds = audit()
    kills = ledger["unique_monomial_kills_by_domain"]
    print("n8 D1 m=7 anchor-normal-form cover: PASS (exact)")
    print("labelled: %d branch states on %d off-supports"
          % (ledger["labelled_branch_states"], ledger["labelled_off_supports"]))
    print("symmetry quotient: %d branch-state orbits"
          % ledger["branch_state_orbits"])
    print("unique-monomial kills: residue %d; six-site %d; full %d"
          % (kills[4], kills[6], kills[8]))
    print("survivors: %d anchor branches over %d off-support orbits"
          % (ledger["survivor_branch_orbits"],
             ledger["survivor_off_support_orbits"]))
    print("survivor sha256:", ledger["survivor_sha256"])
    print("ledger sha256:", digest)
    print("total: %.1f s" % seconds)


if __name__ == "__main__":
    main()
