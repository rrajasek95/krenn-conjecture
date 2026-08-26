#!/usr/bin/env python3
"""UNAUDITED RISK PROBE - source (input) side invariants.

Pinned HEAD b63c76c8624996044423a0dde60a2b60c9e8fa3d.  Works only from the
frozen snapshot in ./snap.  Exact rational arithmetic only.

Everything here is computed from the committed objects exposed by
  computations/verify_h3_complete_tangent_lower_protected_phi_reduction.py
  computations/verify_h3_tangent_euler_occurrence_splitter_fredholm.py
  computations/verify_h3_cut_swap_odd_prism_kdu_typing_gate.py
"""
from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
import importlib.util
import json
from pathlib import Path

SNAP = Path(__file__).resolve().parent / "snap"

W = (0, 0, 1, 1, 2, 2)
WP = (0, 2, 1, 1, 0, 2)
RHO = (0, 4, 2, 3, 1, 5)          # site permutation (1 4)
ROOT_SITES = (1, 4)


def load(relative, name):
    spec = importlib.util.spec_from_file_location(name, SNAP / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def permute_edge(edge, permutation):
    return tuple(sorted(permutation[site] for site in edge))


def permute_matching(matching, permutation):
    return tuple(sorted(permute_edge(edge, permutation) for edge in matching))


def rho_word(word, perm=RHO):
    answer = [None] * len(word)
    for old_site, colour in enumerate(word):
        answer[perm[old_site]] = colour
    return tuple(answer)


def weyl_word(word, root_sites=ROOT_SITES):
    answer = list(word)
    sign = 1
    for site in root_sites:
        if answer[site] == 0:
            answer[site] = 2
            sign *= -1
        elif answer[site] == 2:
            answer[site] = 0
    return tuple(answer), sign


def add(*vectors):
    answer = defaultdict(Q)
    for vector in vectors:
        for basis, value in vector.items():
            answer[basis] += Q(value)
    return {b: v for b, v in answer.items() if v}


def scale(value, vector):
    value = Q(value)
    return {b: value * Q(c) for b, c in vector.items() if value * Q(c)}


def multidegree(word, sites=6, colours=3):
    degree = [0] * (sites * colours)
    for site, colour in enumerate(word):
        degree[colours * site + colour] += 1
    return tuple(degree)


def build(perm=RHO, root_sites=ROOT_SITES, alpha_flip=False):
    """Return the full source-side invariant record.

    ``perm``/``root_sites`` are exposed so the mutation controls can feed in
    wrong data and confirm the invariants detect it.
    """
    lower = load(
        "computations/verify_h3_complete_tangent_lower_protected_phi_reduction.py",
        "probe_lower")
    tangent = load(
        "computations/verify_h3_tangent_euler_occurrence_splitter_fredholm.py",
        "probe_tangent")

    base_labels = lower.lower_labels(tangent, (0, 1, 2))
    other_labels = lower.lower_labels(tangent, (0, 2, 4))
    key = lambda label: (label[1], label[2])
    u_labels = frozenset(map(key, base_labels))
    other_keys = frozenset(map(key, other_labels))
    all_labels = tuple(sorted(u_labels | other_keys))
    index = {label: i for i, label in enumerate(all_labels)}

    def rho_label(label):
        matching_index, repeated_edge = label
        matching = permute_matching(tangent.MATCHINGS[matching_index], perm)
        return (tangent.MATCHING_INDEX[matching],
                permute_edge(repeated_edge, perm))

    # --- rho action on the 15 physical collision labels -------------------
    rho_closed = all(rho_label(label) in index for label in all_labels)
    cycles = []
    seen = set()
    for label in all_labels:
        if label in seen or not rho_closed:
            continue
        orbit = [label]
        seen.add(label)
        image = rho_label(label)
        while image != label:
            orbit.append(image)
            seen.add(image)
            image = rho_label(image)
        cycles.append(tuple(orbit))
    cycle_type = Counter(len(c) for c in cycles)

    # rho maps the 012 lower packet onto the 024 lower packet?
    rho_u = frozenset(map(rho_label, u_labels)) if rho_closed else frozenset()
    packets_swapped = (rho_u == other_keys)

    # --- l = (rho-1)u on the 15 labels ------------------------------------
    l = {}
    for label in all_labels:
        value = Q(int(label in rho_u)) - Q(int(label in u_labels))
        if value:
            l[label] = value

    # --- word x label module and the Klein pair (rho, w) ------------------
    def rho_vector(vector):
        return {(rho_word(word, perm), rho_label(label)): value
                for (word, label), value in vector.items()}

    def weyl_vector(vector):
        answer = defaultdict(Q)
        for (word, label), value in vector.items():
            changed, sign = weyl_word(word, root_sites)
            answer[(changed, label)] += sign * value
        return {b: v for b, v in answer.items() if v}

    u_w = {(W, label): Q(1) for label in sorted(u_labels)}
    if alpha_flip:                       # mutation control hook
        first = sorted(u_labels)[0]
        u_w[(W, first)] = Q(-1)

    # B = (1-rho)(w-1) u_W  == d K(u) + K d(u)
    wu = add(weyl_vector(u_w), scale(-1, u_w))
    B = add(wu, scale(-1, rho_vector(wu)))

    # commutation and involutivity of the two operators on this module
    commute = rho_vector(weyl_vector(u_w)) == weyl_vector(rho_vector(u_w))
    rho_involutive = rho_vector(rho_vector(u_w)) == u_w
    w_involutive = weyl_vector(weyl_vector(u_w)) == u_w

    rho_B = rho_vector(B)
    w_B = weyl_vector(B)
    rho_parity = ("odd" if rho_B == scale(-1, B)
                  else "even" if rho_B == B else "mixed")
    w_parity = ("odd" if w_B == scale(-1, B)
                else "even" if w_B == B else "mixed")

    # Klein four isotypic decomposition:  P_{ab} = (1+a rho)(1+b w)/4
    isotypic = {}
    for a in (1, -1):
        for b in (1, -1):
            piece = scale(Q(1, 4), add(
                B, scale(a, rho_vector(B)), scale(b, weyl_vector(B)),
                scale(a * b, rho_vector(weyl_vector(B)))))
            isotypic[f"rho{'+' if a>0 else '-'}_w{'+' if b>0 else '-'}"] = {
                "support": len(piece),
                "coefficients": sorted(Counter(map(str, piece.values())).items()),
            }

    words_present = sorted({word for word, _ in B})
    per_word = defaultdict(list)
    for (word, label), value in B.items():
        per_word[word].append(value)

    return {
        "collision_labels": len(all_labels),
        "u012_labels": len(u_labels),
        "u024_labels": len(other_keys),
        "shared_labels": sorted(map(str, sorted(u_labels & other_keys))),
        "rho_permutation": list(perm),
        "rho_closed_on_15_labels": rho_closed,
        "rho_cycle_type_on_labels": dict(sorted(cycle_type.items())),
        "rho_maps_u012_packet_to_u024_packet": packets_swapped,
        "l_support": len(l),
        "l_coefficient_multiset": sorted(
            Counter(str(v) for v in l.values()).items()),
        "l_zero_labels": sorted(str(x) for x in all_labels if x not in l),
        "rho_operators_commute_with_w": commute,
        "rho_involutive": rho_involutive,
        "w_involutive": w_involutive,
        "B_support": len(B),
        "B_words": [ "".join(map(str, x)) for x in words_present],
        "B_support_per_word": {"".join(map(str, k)): len(v)
                               for k, v in sorted(per_word.items())},
        "B_coefficient_multiset": sorted(
            Counter(str(v) for v in B.values()).items()),
        "B_rho_parity": rho_parity,
        "B_w_parity": w_parity,
        "B_klein_isotypic": isotypic,
        "W_multidegree": list(multidegree(W)),
        "Wprime_multidegree": list(multidegree(WP)),
        "W_equals_Wprime_multidegree": multidegree(W) == multidegree(WP),
        "W_colour_character": [W.count(c) for c in range(3)],
        "Wprime_colour_character": [WP.count(c) for c in range(3)],
        "source_sites": 6,
        "source_colours": 3,
    }, B, all_labels


def main():
    record, _B, _labels = build()
    print(json.dumps(record, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
