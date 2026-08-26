#!/usr/bin/env python3
"""Exact orbit and diagonal-torus counterguard for the 22-row extension."""

from collections import Counter
from hashlib import sha256
from itertools import permutations, product
from pathlib import Path
import argparse
import json
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PREVIOUS = (
    ROOT
    / "computations/unaudited-codex-triangle-rankdrop-prerequisite-2026-08-23"
    / "results_triangle_rankdrop_prerequisite.json"
)
SOURCE = (
    ROOT
    / "computations/unaudited-codex-rootless-fine-macaulay-2026-08-22"
    / "results_closure22_plus_full_profile71_joint_cegar_rust_p32003.json"
)
OUT = HERE / "results_triangle_rank9_22row_cegar.json"
U_EDGES = {(0, 6), (3, 7)}


def edge(u, v):
    return (u, v) if u < v else (v, u)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted((edge(first, second),) + tail))


MATCHINGS = tuple(perfect_matchings(range(8)))


def matching_count(vertices, allowed):
    vertices = tuple(sorted(vertices))
    if len(vertices) % 2:
        return 0
    return sum(
        all(pair in allowed for pair in matching)
        for matching in perfect_matchings(vertices)
    )


def amplitude_count(word, colour_matchings):
    value = 1
    for colour, matching in enumerate(colour_matchings):
        vertices = [site for site, symbol in enumerate(word) if int(symbol) == colour]
        value *= matching_count(vertices, set(matching) | U_EDGES)
    return value


def profile(word):
    return "+".join(str(value) for value in sorted(Counter(word).values(), reverse=True))


def minor_divisor_stabilizer():
    # Stabilize cap pair {6,7}, triangle {0,1,2}, outside {3,4,5}, and
    # distinguished response edge {0,3}.  Hence 0 and 3 are fixed, while
    # 1<->2, 4<->5, 6<->7 are independent.  S3 relabels colours.
    answer = []
    for swap12, swap45, swap67 in product(range(2), repeat=3):
        site = list(range(8))
        if swap12:
            site[1], site[2] = site[2], site[1]
        if swap45:
            site[4], site[5] = site[5], site[4]
        if swap67:
            site[6], site[7] = site[7], site[6]
        for colour in permutations(range(3)):
            answer.append((tuple(site), colour))
    assert len(answer) == 48
    return tuple(answer)


def act_word(word, group_element):
    site, colour = group_element
    answer = [None] * 8
    for old_site, symbol in enumerate(word):
        answer[site[old_site]] = str(colour[int(symbol)])
    return "".join(answer)


def orbit_census(words):
    group = minor_divisor_stabilizer()
    words = set(words)
    seen = set()
    census = []
    for representative in sorted(words):
        if representative in seen:
            continue
        ambient_orbit = {act_word(representative, element) for element in group}
        intersection = sorted(words & ambient_orbit)
        seen.update(intersection)
        census.append({
            "representative": representative,
            "profile": profile(representative),
            "ambient_orbit_size": len(ambient_orbit),
            "intersection_size": len(intersection),
            "intersection": intersection,
        })
    assert seen == words
    assert len(census) == 11
    return census


def support_automorphism_count(colour_matchings):
    edge_sets = [set(matching) | U_EDGES for matching in colour_matchings]
    count = 0
    for site, colour in minor_divisor_stabilizer():
        okay = True
        for old_colour, edges in enumerate(edge_sets):
            image = {edge(site[u], site[v]) for u, v in edges}
            if image != edge_sets[colour[old_colour]]:
                okay = False
                break
        count += int(okay)
    return count


def find_extended_guard(words):
    candidates = []
    for matching in MATCHINGS:
        allowed = set(matching) | U_EDGES
        if matching_count(range(8), allowed) != 1:
            continue
        masks = []
        for colour in range(3):
            mask = 0
            for index, word in enumerate(words):
                vertices = [site for site, symbol in enumerate(word) if int(symbol) == colour]
                if matching_count(vertices, allowed):
                    mask |= 1 << index
            masks.append(mask)
        candidates.append((matching, masks))
    assert len(candidates) == 99

    chosen = None
    for matching0, masks0 in candidates:
        for matching1, masks1 in candidates:
            partial = masks0[0] & masks1[1]
            for matching2, masks2 in candidates:
                if partial & masks2[2] == 0:
                    chosen = (matching0, matching1, matching2)
                    break
            if chosen:
                break
        if chosen:
            break
    assert chosen == (
        ((0, 1), (2, 3), (4, 5), (6, 7)),
        ((0, 2), (1, 4), (3, 7), (5, 6)),
        ((0, 2), (1, 4), (3, 6), (5, 7)),
    )
    assert all(amplitude_count(word, chosen) == 0 for word in words)
    pure = {
        str(colour): matching_count(range(8), set(chosen[colour]) | U_EDGES)
        for colour in range(3)
    }
    assert pure == {"0": 1, "1": 1, "2": 1}

    full_nonzero = {}
    for symbols in product(range(3), repeat=8):
        if len(set(symbols)) == 1:
            continue
        word = "".join(str(symbol) for symbol in symbols)
        value = amplitude_count(word, chosen)
        if value:
            full_nonzero[word] = value
    assert len(full_nonzero) == 20
    profile_census = Counter(profile(word) for word in full_nonzero)
    assert profile_census == {"6+2": 8, "4+2+2": 7, "4+4": 5}

    # There are 6,5,6 diagonal cells in the three colour supports.  The
    # mixed packet restricts identically to zero; the three pure equations
    # are independent monomial=1 equations.  Hence their torus has dim 14.
    active_cell_count = sum(len(set(matching) | U_EDGES) for matching in chosen)
    assert active_cell_count == 17
    torus_dimension = active_cell_count - 3

    # U supplies P_0=I and Q_3=I.  No support edge is 07, hence Q_0=0;
    # therefore R_03 is the identity even though colour 2 also has edge 36.
    assert all((0, 6) in (set(matching) | U_EDGES) for matching in chosen)
    assert all((3, 7) in (set(matching) | U_EDGES) for matching in chosen)
    assert all((0, 7) not in (set(matching) | U_EDGES) for matching in chosen)

    return {
        "candidate_matching_count": len(candidates),
        "colour_matchings": [[list(pair) for pair in matching] for matching in chosen],
        "selected_packet_word_count": len(words),
        "selected_packet_nonzero_amplitudes": {},
        "pure_amplitudes": pure,
        "active_diagonal_cell_count": active_cell_count,
        "pure_torus_dimension": torus_dimension,
        "R_03_operator": "identity on Mat_3",
        "Delta_03": 1,
        "L_triangle_rank": 9,
        "full_X5_nonzero_mixed_amplitudes": full_nonzero,
        "full_X5_nonzero_profile_census": dict(sorted(profile_census.items())),
        "minor_divisor_support_stabilizer_size": support_automorphism_count(chosen),
    }


def audit():
    source_payload = json.loads(SOURCE.read_text())
    previous_payload = json.loads(PREVIOUS.read_text())
    base_words = tuple(source_payload["source_words"])
    violating22 = tuple(
        previous_payload["literal_diagonal_counterguard"]
        ["full_X5_nonzero_mixed_amplitudes"]
    )
    assert len(base_words) == 62 and len(violating22) == 22
    assert not set(base_words) & set(violating22)
    assert Counter(profile(word) for word in violating22) == {
        "6+2": 8, "4+4": 6, "4+2+2": 8,
    }
    selected = base_words + violating22
    guard = find_extended_guard(selected)
    result = {
        "status": "PASS 84-row extension still admits a rank-nine diagonal torus",
        "minor": {
            "name": "Delta_03",
            "definition": "det(K -> P_0^T K Q_3 + Q_0^T K^T P_3)",
            "degree": 18,
            "minor_divisor_stabilizer_size": 48,
            "ordered_cap_stabilizer_size": 24,
        },
        "violating22_profile_census": dict(
            sorted(Counter(profile(word) for word in violating22).items())
        ),
        "violating22_minor_stabilizer_orbits": orbit_census(violating22),
        "first_guard_support_stabilizer_size": support_automorphism_count((
            ((0, 1), (2, 3), (4, 5), (6, 7)),
            ((0, 1), (2, 3), (4, 6), (5, 7)),
            ((0, 2), (1, 3), (4, 5), (6, 7)),
        )),
        "extended_guard": guard,
        "membership_verdict": {
            "over": "Z, Q, and every finite field",
            "statement": (
                "For every m>=1, Delta_03^m is not in the ideal generated by "
                "the 62 frozen rows, the 22 extension rows, and the three pure "
                "normalizations."
            ),
            "proof": (
                "Evaluation at the extended guard sends every ideal generator "
                "to zero and sends Delta_03^m to one."
            ),
            "radical_membership": False,
            "modular_run_needed": False,
        },
        "lowest_order_verdict": (
            "On the first guard each of the 22 added rows has nonzero order-zero "
            "value, so its completed local ideal is the unit ideal.  This is "
            "witness-specific.  On the extended 17-cell support, all 84 mixed "
            "rows vanish identically, their support-tangent derivatives vanish "
            "to every order, and the normalized common-zero torus has dimension "
            "14 with Delta_03 invertible."
        ),
        "smallest_next_packet": {
            "row_count": len(guard["full_X5_nonzero_mixed_amplitudes"]),
            "profile_census": guard["full_X5_nonzero_profile_census"],
            "words": list(guard["full_X5_nonzero_mixed_amplitudes"]),
        },
        "source_digests": {
            "closure62": sha256(SOURCE.read_bytes()).hexdigest(),
            "previous_guard": sha256(PREVIOUS.read_bytes()).hexdigest(),
        },
        "scope": (
            "Exact literal diagonal-source counterguard for the selected 84 rows. "
            "It is not a full X5 point; its 20 named mixed rows are nonzero."
        ),
    }
    assert result["first_guard_support_stabilizer_size"] == 1
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(canonical.encode()).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-results", action="store_true")
    args = parser.parse_args()
    result = audit()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.check_results:
        if not OUT.exists() or OUT.read_text() != rendered:
            print("frozen result mismatch", file=sys.stderr)
            return 1
        print(result["status"], result["logical_sha256"])
        return 0
    OUT.write_text(rendered)
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
