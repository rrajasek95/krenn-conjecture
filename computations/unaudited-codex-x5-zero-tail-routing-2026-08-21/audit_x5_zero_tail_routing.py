#!/usr/bin/env python3
"""Exact routing audit for the 1,638 nontrivial X5 zero-tail rows.

No polynomial elimination is used.  The checker enumerates the literal
three-colour words, verifies their tail-zero matching factorization, takes
orbits under the anchor-pair wreath group B4 and colour permutations, and
compares them with the frozen 78+48+144 diagonal master packet.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "results_x5_zero_tail_routing.json"
PAIRING = ((0, 1), (2, 3), (4, 5), (6, 7))
PAIR_TYPES = ((0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2))
MASTER_SOURCE = (ROOT / "computations/unaudited-codex-k4-cycle-quadratic-mate-2026-08-21" /
                 "audit_quadratic_component_mates.py")
TAIL_RESULT = (ROOT / "computations/unaudited-codex-tail-filtered-lift-obstruction-2026-08-21" /
               "results_tail_filtered_lift_obstruction.json")
PROOF_REVIEW = (ROOT / "computations/unaudited-codex-proof-spine-review-2026-08-21" /
                "REPORT.md")
DANGER_REPORT = (ROOT / "computations/unaudited-codex-n8-dangerous-chart-bridge-2026-08-20" /
                 "REPORT.md")
SUPPORT6 = (ROOT / "computations/unaudited-codex-n8-dangerous-chart-bridge-2026-08-20" /
            "results_support6_component_pairwise_obstruction.json")
SUPPORT8 = (ROOT / "computations/unaudited-codex-orbit0-t2-radical-2026-08-20" /
            "results_weight0_char0_family_and_packet.json")


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def file_sha(path):
    return sha256(path.read_bytes()).hexdigest()


def logical_sha(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode("ascii")).hexdigest()


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index+1:]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


PM8 = tuple(perfect_matchings(range(8)))


def profile(word):
    counts = sorted(Counter(word).values(), reverse=True)
    return tuple(counts + [0]*(3-len(counts)))


def word_label(word):
    return "".join(map(str, word))


def pair_multigraph_signature(word):
    """Canonical loop/edge multiplicities modulo S3 colour relabelling."""
    raw = Counter(tuple(sorted((word[left], word[right])))
                  for left, right in PAIRING)
    candidates = []
    for permutation in permutations(range(3)):
        relabelled = Counter()
        for edge, count in raw.items():
            relabelled[tuple(sorted((permutation[edge[0]],
                                     permutation[edge[1]])))] += count
        candidates.append(tuple(relabelled[edge] for edge in PAIR_TYPES))
    return min(candidates)


def row_formula(word):
    factors = []
    for colour in range(3):
        sites = tuple(index for index, value in enumerate(word) if value == colour)
        if not sites:
            continue
        if len(sites) == 2:
            factors.append(f"X_{colour}[{sites[0]}{sites[1]}]")
        elif len(sites) == 4:
            factors.append(f"Q_{colour}[{''.join(map(str, sites))}]")
        elif len(sites) == 6:
            omitted = tuple(index for index in range(8) if index not in sites)
            factors.append(f"C_{colour}[{omitted[0]}{omitted[1]}]")
        else:
            raise RuntimeError(f"unexpected even class size {len(sites)}")
    return "*".join(factors)


def master_packet():
    pairconstant = {
        word_label(tuple(values[site//2] for site in range(8)))
        for values in product(range(3), repeat=4) if len(set(values)) > 1
    }
    four_four = set()
    for left, right in combinations(range(3), 2):
        for orientation in range(16):
            values = []
            for site in range(4):
                bit = (orientation >> (3-site)) & 1
                values.extend((right, left) if bit else (left, right))
            four_four.add(word_label(values))
    six_two = set()
    super_edges = tuple(combinations(range(4), 2))
    for majority, minority in permutations(range(3), 2):
        for edge in super_edges:
            for clone_left, clone_right in product(range(2), repeat=2):
                values = [majority]*8
                values[2*edge[0]+clone_left] = minority
                values[2*edge[1]+clone_right] = minority
                six_two.add(word_label(values))
    require((len(pairconstant), len(four_four), len(six_two)) == (78, 48, 144),
            "master 78+48+144 sector census changed")
    require(not (pairconstant & four_four or pairconstant & six_two
                 or four_four & six_two), "master sectors ceased to be disjoint")
    return {"pairconstant_78": pairconstant,
            "four_plus_four_48": four_four,
            "six_plus_two_144": six_two}


ORBIT_NAMES = {
    ((6, 2, 0), "00000011"): "620_three_majority_loops_one_minority_loop",
    ((6, 2, 0), "00000101"): "620_two_majority_loops_two_cross_edges",
    ((4, 4, 0), "00001111"): "440_two_loops_each",
    ((4, 4, 0), "00010111"): "440_one_loop_each_two_cross_edges",
    ((4, 4, 0), "01010101"): "440_four_cross_edges",
    ((4, 2, 2), "00001122"): "422_two_majority_loops_two_minority_loops",
    ((4, 2, 2), "00001212"): "422_two_majority_loops_two_minor_cross_edges",
    ((4, 2, 2), "00010122"): "422_majority_loop_minor_loop_two_cross_edges",
    ((4, 2, 2), "00010212"): "422_majority_loop_colour_triangle",
    ((4, 2, 2), "01010202"): "422_two_edges_to_each_minor_colour",
}


def main():
    require(len(PM8) == 105, "perfect-matching census changed")
    for path in (MASTER_SOURCE, TAIL_RESULT, PROOF_REVIEW, DANGER_REPORT,
                 SUPPORT6, SUPPORT8):
        require(path.is_file(), f"missing upstream {path}")
    tail = json.loads(TAIL_RESULT.read_text())
    require(tail["terminal_zero_tail_quotient"]["nontrivial_diagonal_packet_rows"]
            == 1638, "upstream zero-tail count changed")

    sectors = master_packet()
    master_union = set().union(*sectors.values())
    require(len(master_union) == 270, "master packet union changed")

    records = defaultdict(lambda: {"labels": [], "representative": None,
                                   "signature": None, "matching_terms": None})
    automatic = 0
    pure = 0
    for word in product(range(3), repeat=8):
        counts = profile(word)
        if counts == (8, 0, 0):
            pure += 1
            continue
        if any(count % 2 for count in counts):
            automatic += 1
            # No perfect matching stays inside every odd colour class.
            require(not any(all(word[left] == word[right]
                                for left, right in matching)
                            for matching in PM8),
                    "odd-profile row retained a tail-zero matching")
            continue
        require(counts in ((6, 2, 0), (4, 4, 0), (4, 2, 2)),
                f"unexpected even mixed profile {counts}")
        diagonal_matchings = sum(
            all(word[left] == word[right] for left, right in matching)
            for matching in PM8)
        expected_terms = {(6, 2, 0): 15, (4, 4, 0): 9,
                          (4, 2, 2): 3}[counts]
        require(diagonal_matchings == expected_terms,
                "literal tail-zero factor term count changed")
        signature = pair_multigraph_signature(word)
        key = (counts, signature)
        label = word_label(word)
        row = records[key]
        row["labels"].append(label)
        row["signature"] = signature
        row["matching_terms"] = diagonal_matchings
        if row["representative"] is None or label < row["representative"]:
            row["representative"] = label

    require((pure, automatic, sum(len(row["labels"]) for row in records.values()))
            == (3, 4920, 1638), "pure/automatic/nontrivial census changed")
    require(len(records) == 10, "B4 x S3 signature orbit count changed")

    routing = []
    profile_counts = Counter()
    master_profile_counts = Counter()
    missing_profile_counts = Counter()
    master_sector_counts = Counter()
    for (counts, signature), row in sorted(records.items()):
        representative = row["representative"]
        orbit_name = ORBIT_NAMES.get((counts, representative))
        require(orbit_name is not None, f"unnamed orbit {(counts, representative)}")
        labels = sorted(row["labels"])
        sector_hits = {name: sorted(set(labels) & sector)
                       for name, sector in sectors.items()}
        active_sectors = [name for name, hits in sector_hits.items() if hits]
        master_labels = sorted(set(labels) & master_union)
        missing_labels = sorted(set(labels) - master_union)
        # Every signature orbit is either wholly selected or wholly absent.
        require(not (master_labels and missing_labels),
                f"master packet cuts signature orbit {orbit_name}")
        profile_name = "+".join(map(str, counts))
        profile_counts[profile_name] += len(labels)
        master_profile_counts[profile_name] += len(master_labels)
        missing_profile_counts[profile_name] += len(missing_labels)
        for sector, hits in sector_hits.items():
            master_sector_counts[sector] += len(hits)
        routing.append({
            "orbit": orbit_name,
            "profile": profile_name,
            "canonical_word": representative,
            "pair_multigraph_signature_l0_l1_l2_e01_e02_e12": list(signature),
            "literal_row_count": len(labels),
            "tail_zero_matching_terms": row["matching_terms"],
            "canonical_factor_formula": row_formula(tuple(map(int, representative))),
            "master_270_sector": active_sectors[0] if active_sectors else None,
            "master_270_covered": bool(master_labels),
            "literal_source_labels": labels,
            "labels_sha256": sha256("\n".join(labels).encode("ascii")).hexdigest(),
        })

    require(profile_counts == {"6+2+0": 168, "4+4+0": 210,
                               "4+2+2": 1260}, "profile counts changed")
    require(master_sector_counts == {"pairconstant_78": 78,
                                     "four_plus_four_48": 48,
                                     "six_plus_two_144": 144},
            "master sector routing changed")
    require(master_profile_counts == {"6+2+0": 168,
                                      "4+4+0": 66,
                                      "4+2+2": 36},
            "master profile routing changed")
    require(+missing_profile_counts == {"4+4+0": 144,
                                        "4+2+2": 1224},
            "missing profile routing changed")

    missing_orbits = [row["orbit"] for row in routing
                      if not row["master_270_covered"]]
    require(missing_orbits == [
        "422_two_edges_to_each_minor_colour",
        "422_majority_loop_colour_triangle",
        "422_two_majority_loops_two_minor_cross_edges",
        "422_majority_loop_minor_loop_two_cross_edges",
        "440_one_loop_each_two_cross_edges",
    ], "missing orbit list changed")

    payload = {
        "status": "PASS exact X5 zero-tail diagonal routing audit",
        "ambient": {
            "sites": 8, "colours": 3,
            "anchor_pairing": [list(pair) for pair in PAIRING],
            "zero_tail_variables": {
                "X_c[ij]": "two-site Hafnian g^c_ij",
                "C_c[ij]": "six-site Hafnian on V\\{i,j}, the ij cofactor",
                "Q_c[S]": "four-site Hafnian on S",
            },
            "row_map": {
                "6+2+0": "C_c[ij]*X_d[ij]",
                "4+4+0": "Q_c[S]*Q_d[V\\S]",
                "4+2+2": "Q_c[S]*X_d[T]*X_e[U]",
            },
        },
        "literal_census": {
            "pure_rows": pure,
            "automatic_odd_class_rows": automatic,
            "nontrivial_even_class_rows": sum(profile_counts.values()),
            "profile_counts": dict(profile_counts),
            "signature_orbits_B4_times_S3": len(routing),
        },
        "master_270_replay": {
            "sector_counts": dict(master_sector_counts),
            "profile_counts": dict(master_profile_counts),
            "total": sum(master_profile_counts.values()),
            "source": str(MASTER_SOURCE.relative_to(ROOT)),
            "source_sha256": file_sha(MASTER_SOURCE),
            "meaning": (
                "The selected master packet contains every 6+2+0 row, the "
                "pair-constant and fully split 4+4+0 orbits, and only the "
                "pair-constant 4+2+2 orbit."),
        },
        "routing_table": routing,
        "missing_from_master_270": {
            "row_count": sum(missing_profile_counts.values()),
            "profile_counts": dict(+missing_profile_counts),
            "signature_orbits": missing_orbits,
            "smallest_orbit": "440_one_loop_each_two_cross_edges",
            "smallest_orbit_count": 144,
        },
        "closure_scope_audit": {
            "frozen_k4_cycle_and_TP": (
                "These are exact closures of named one-colour cofactor/support "
                "charts inside the normalized master packet; no frozen ledger "
                "routes all diagonal charts or the five missing word signatures "
                "to those two graph types."),
            "frozen_support6_and_support8": (
                "These are real H-live one-colour components on the localized "
                "weight-zero d=0 chart, closed by arbitrary-mate obstructions. "
                "Their audits explicitly do not classify every H-live component."),
            "exhaust_zero_tail_scheme": False,
            "exact_blocker": (
                "The existing artifacts contain neither a complete e=0 diagonal "
                "chart census nor a derivation making the 144 mixed-pair 4+4 "
                "rows and four non-pairconstant 4+2+2 signature orbits redundant."
            ),
        },
        "lemma_status": {
            "requested": "e=0 implies active cap or an existing mate-closed component",
            "proved_by_frozen_artifacts": False,
            "theorem_grade_conditional_form": (
                "If every H-live e=0 diagonal chart is routed to k4-cycle, TP, "
                "support6, support8, uniform/aligned mate-closed families, or an "
                "active carrier, then the requested implication follows. The "
                "routing antecedent is the missing diagonal classification theorem."
            ),
            "smallest_next_exact_target": (
                "On the e=t=0 normalized anchor chart, reduce the 144-row "
                "440_one_loop_each_two_cross_edges orbit against the literal "
                "78+48+144 packet. Either prove exact containment/redundancy or "
                "add it as a new diagonal chart signature before treating the "
                "four missing 4+2+2 orbits."
            ),
        },
        "source_hashes": {
            str(path.relative_to(ROOT)): file_sha(path)
            for path in (TAIL_RESULT, PROOF_REVIEW, DANGER_REPORT, SUPPORT6, SUPPORT8)
        },
        "mutation_guards": {
            "drop_440_2110_orbit": True,
            "declare_master270_equal_to_full1638": True,
            "route_nonpairconstant_422_to_pairconstant": True,
            "declare_localized_support8_family_global_exhaustion": True,
        },
    }
    payload["logical_sha256"] = logical_sha(payload)
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if "--write-results" in sys.argv:
        OUT.write_text(text)
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
