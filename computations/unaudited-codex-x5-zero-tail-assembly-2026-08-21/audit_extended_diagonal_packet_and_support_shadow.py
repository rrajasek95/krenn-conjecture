#!/usr/bin/env python3
"""Assemble the exact e=t=0 diagonal packet and audit its Boolean shadow.

This is deliberately not a polynomial solve.  The first half is an exact
literal-word/orbit replay.  The second half enumerates the inclusion-minimal
support shadow obtained by retaining one permanent monomial in every live
2x2 block and one complementary Q-pair per H-live colour.  It quotients the
survivors by B4 x S3 and records, without overclaiming, which frozen exact
component no-goods can be applied on support data alone.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ROUTING = (ROOT / "computations/unaudited-codex-x5-zero-tail-routing-2026-08-21" /
           "results_x5_zero_tail_routing.json")
EXTENSION_440 = (ROOT / "computations/unaudited-codex-x5-zero-tail-routing-2026-08-21" /
                 "results_440_2110_extension.json")
EXTENSION_422 = (ROOT / "computations/unaudited-codex-x5-zero-tail-routing-2026-08-21" /
                 "results_422_nonpairconstant_extension.json")
CORE_IDENTITY = (ROOT / "computations/unaudited-codex-n8-orbit0-normalized-78-2026-08-20" /
                 "results_polarized_superpair_core_identity.json")
PACKET_OUT = HERE / "extended_diagonal_packet_1566.json"
RESULT_OUT = HERE / "results_extended_diagonal_packet_support_shadow.json"

PAIRING = ((0, 1), (2, 3), (4, 5), (6, 7))
SUPER_EDGES = tuple(combinations(range(4), 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(SUPER_EDGES)}
COMPLEMENTARY_EDGE_PAIRS = (((0, 1), (2, 3)),
                            ((0, 2), (1, 3)),
                            ((0, 3), (1, 2)))

EXPLICIT_ORBITS = (
    "620_three_majority_loops_one_minority_loop",
    "620_two_majority_loops_two_cross_edges",
    "440_two_loops_each",
    "440_four_cross_edges",
    "422_two_majority_loops_two_minority_loops",
    "440_one_loop_each_two_cross_edges",
    "422_two_edges_to_each_minor_colour",
    "422_majority_loop_colour_triangle",
    "422_majority_loop_minor_loop_two_cross_edges",
)
OMITTED_E_ORBIT = "422_two_majority_loops_two_minor_cross_edges"

NO_GOOD_SOURCES = (
    ("support6_arbitrary_mate",
     "computations/unaudited-codex-Q-cross-orbit-pullback-2026-08-21/"
     "results_support6_cross_orbit_pullback_unit.json"),
    ("support8_one_y_arbitrary_mate",
     "computations/unaudited-codex-root-integration-2026-08-20/"
     "results_one_y_forced_mate_unit.json"),
    ("k4_TP_boundary",
     "computations/unaudited-codex-tp-p26-boundary-char0-2026-08-21/"
     "results_tp_p26_base_core_char0_replay_standard.json"),
    ("k4_TP_interior",
     "computations/unaudited-codex-tp-p26-interior-char0-2026-08-21/"
     "results_tp_p26_interior_char0_replay_standard.json"),
    ("cycle_boundary",
     "computations/unaudited-codex-branch0-offdiag-support-strata-2026-08-21/"
     "results_cycle_boundary_family_referee.json"),
    ("A_equals_B_mate_closure",
     "computations/unaudited-codex-generic-cycle-mate-incidence-2026-08-21/"
     "results_AB_component_mate_closure_ledger.json"),
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def file_sha(path):
    return sha256(path.read_bytes()).hexdigest()


def logical_sha(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode("ascii")).hexdigest()


def profile(label):
    counts = sorted(Counter(label).values(), reverse=True)
    return "+".join(map(str, counts + [0] * (3-len(counts))))


def row_formula(label):
    word = tuple(map(int, label))
    factors = []
    for colour in range(3):
        sites = tuple(index for index, value in enumerate(word)
                      if value == colour)
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
            raise RuntimeError("unexpected word profile")
    return "*".join(factors)


def e_multiple_record(label):
    word = tuple(map(int, label))
    majority = next(colour for colour in range(3)
                    if word.count(colour) == 4)
    majority_sites = {index for index, colour in enumerate(word)
                      if colour == majority}
    supervertices = tuple(index for index, pair in enumerate(PAIRING)
                          if set(pair).issubset(majority_sites))
    require(len(supervertices) == 2 and
            majority_sites == set(PAIRING[supervertices[0]] +
                                  PAIRING[supervertices[1]]),
            f"omitted row {label} is not an anchor-union Q=e factor")
    other = [colour for colour in range(3) if colour != majority]
    factors = []
    for colour in other:
        sites = tuple(index for index, value in enumerate(word)
                      if value == colour)
        factors.append(f"X_{colour}[{sites[0]}{sites[1]}]")
    return {
        "label": label,
        "literal_formula": row_formula(label),
        "exact_quotient_factorization": (
            f"e_{majority}[{supervertices[0]}{supervertices[1]}]*" +
            "*".join(factors)),
        "vanishing_generator": f"e_{majority}[{supervertices[0]}{supervertices[1]}]",
    }


def assemble_packet():
    routing = json.loads(ROUTING.read_text())
    extension_440 = json.loads(EXTENSION_440.read_text())
    extension_422 = json.loads(EXTENSION_422.read_text())
    rows = {record["orbit"]: record for record in routing["routing_table"]}
    require(set(EXPLICIT_ORBITS) | {OMITTED_E_ORBIT} == set(rows),
            "routing orbit names changed")
    classification = {record["orbit"]: record["classification"]
                      for record in extension_422["orbit_records"]}
    require(classification == {
        "422_two_edges_to_each_minor_colour": "GENUINELY_NEW_degree4_source_orbit",
        "422_majority_loop_colour_triangle": "GENUINELY_NEW_degree4_source_orbit",
        OMITTED_E_ORBIT: "REDUNDANT_exact_e_multiple",
        "422_majority_loop_minor_loop_two_cross_edges":
            "GENUINELY_NEW_degree4_source_orbit",
    }, "422 extension classification changed")
    require(extension_440["extension_440_2110"]["source_rows"] == 144,
            "440 extension orbit count changed")
    explicit = []
    for orbit in EXPLICIT_ORBITS:
        for label in rows[orbit]["literal_source_labels"]:
            explicit.append({"label": label, "profile": profile(label),
                             "orbit": orbit,
                             "literal_formula": row_formula(label)})
    explicit.sort(key=lambda row: row["label"])
    omitted = [e_multiple_record(label)
               for label in rows[OMITTED_E_ORBIT]["literal_source_labels"]]
    omitted.sort(key=lambda row: row["label"])
    explicit_labels = {row["label"] for row in explicit}
    omitted_labels = {row["label"] for row in omitted}
    all_labels = set().union(*(set(row["literal_source_labels"])
                               for row in rows.values()))
    require(len(explicit) == len(explicit_labels) == 1566,
            "extended packet count/uniqueness changed")
    require(len(omitted) == len(omitted_labels) == 72,
            "e-multiple orbit count changed")
    require(not explicit_labels & omitted_labels and
            explicit_labels | omitted_labels == all_labels and
            len(all_labels) == 1638,
            "1566+72 quotient coverage failed")
    counts = Counter(row["profile"] for row in explicit)
    require(counts == {"6+2+0": 168, "4+4+0": 210, "4+2+2": 1188},
            "explicit profile counts changed")
    packet = {
        "status": "PASS exact extended e=t=0 diagonal packet assembly",
        "ambient": "anchor-normalized X5 zero-tail quotient e=t=0",
        "explicit_generator_count": len(explicit),
        "explicit_profile_counts": dict(counts),
        "explicit_orbits": list(EXPLICIT_ORBITS),
        "explicit_rows": explicit,
        "omitted_exact_e_multiple_orbit": {
            "orbit": OMITTED_E_ORBIT,
            "row_count": len(omitted),
            "rows": omitted,
        },
        "quotient_coverage": {
            "explicit_rows": 1566,
            "rows_zero_in_e_ideal": 72,
            "all_nontrivial_zero_tail_rows": 1638,
            "disjoint_union_verified": True,
        },
        "sources": {
            str(ROUTING.relative_to(ROOT)): file_sha(ROUTING),
            str(EXTENSION_440.relative_to(ROOT)): file_sha(EXTENSION_440),
            str(EXTENSION_422.relative_to(ROOT)): file_sha(EXTENSION_422),
        },
    }
    packet["logical_sha256"] = logical_sha(packet)
    return packet


def cut_mask(bits):
    return sum((((bits >> i) & 1) ^ ((bits >> j) & 1)) << index
               for index, (i, j) in enumerate(SUPER_EDGES))


CUT_MASKS = tuple(sorted({cut_mask(bits) for bits in range(16)}))


def compatible_422(q_cut, left_x, right_x):
    """All six 422 rows for fixed majority-Q and two minor colours."""
    for first, second in COMPLEMENTARY_EDGE_PAIRS:
        i = EDGE_INDEX[first]
        j = EDGE_INDEX[second]
        if ((left_x >> i) & 1) == ((q_cut >> i) & 1) and \
           ((right_x >> j) & 1) == ((q_cut >> j) & 1):
            return False
        if ((left_x >> j) & 1) == ((q_cut >> j) & 1) and \
           ((right_x >> i) & 1) == ((q_cut >> i) & 1):
            return False
    return True


def transform_mask(mask, permutation=(0, 1, 2, 3), flip_mask=0):
    answer = 0
    for index, (left, right) in enumerate(SUPER_EDGES):
        bit = ((mask >> index) & 1) ^ ((flip_mask >> left) & 1) ^ \
              ((flip_mask >> right) & 1)
        image = tuple(sorted((permutation[left], permutation[right])))
        answer |= bit << EDGE_INDEX[image]
    return answer


def generators():
    result = []
    for index in range(3):
        permutation = list(range(4))
        permutation[index], permutation[index+1] = \
            permutation[index+1], permutation[index]
        result.append(("B4", tuple(permutation), 0))
    # A simultaneous flip of all four clones acts trivially on relation masks,
    # so three independent flips generate the faithful (Z2)^3 quotient.
    for index in range(3):
        result.append(("B4", (0, 1, 2, 3), 1 << index))
    result.extend((("S3", 0, 1), ("S3", 1, 2)))
    return tuple(result)


GENERATORS = generators()


def act(state, generator):
    q_cuts, x_relations = state
    if generator[0] == "B4":
        _, permutation, flip_mask = generator
        return (tuple(transform_mask(mask, permutation, flip_mask)
                      for mask in q_cuts),
                tuple(transform_mask(mask, permutation, flip_mask)
                      for mask in x_relations))
    _, left, right = generator
    q_cuts = list(q_cuts)
    x_relations = list(x_relations)
    q_cuts[left], q_cuts[right] = q_cuts[right], q_cuts[left]
    x_relations[left], x_relations[right] = \
        x_relations[right], x_relations[left]
    return tuple(q_cuts), tuple(x_relations)


def support_shadow():
    require(len(CUT_MASKS) == 8, "Q complementary-pair cut census changed")
    allowed = {
        q_cut: [sum(1 << right_x for right_x in range(64)
                    if compatible_422(q_cut, left_x, right_x))
                for left_x in range(64)]
        for q_cut in CUT_MASKS
    }
    survivors = set()
    q_triple_histogram = Counter()
    for q_cuts in permutations(CUT_MASKS, 3):
        count = 0
        for x0 in range(64):
            for x1 in range(64):
                if not compatible_422(q_cuts[2], x0, x1):
                    continue
                possible = allowed[q_cuts[0]][x1] & allowed[q_cuts[1]][x0]
                while possible:
                    low = possible & -possible
                    x2 = low.bit_length() - 1
                    possible -= low
                    survivors.add((q_cuts, (x0, x1, x2)))
                    count += 1
        q_triple_histogram[count] += 1
    require(len(survivors) == 275568 and
            q_triple_histogram == {735: 288, 1331: 48},
            "minimal Boolean survivor census changed")

    remaining = set(survivors)
    orbit_records = []
    while remaining:
        seed = min(remaining)
        remaining.remove(seed)
        queue = [seed]
        for state in queue:
            for generator in GENERATORS:
                image = act(state, generator)
                require(image in survivors, "group action left survivor set")
                if image in remaining:
                    remaining.remove(image)
                    queue.append(image)
        representative = min(queue)
        orbit_records.append({
            "q_pair_cut_masks_e01_e02_e03_e12_e13_e23":
                list(representative[0]),
            "x_relation_masks_e01_e02_e03_e12_e13_e23":
                list(representative[1]),
            "x_relation_weights": [mask.bit_count()
                                   for mask in representative[1]],
            "orbit_size": len(queue),
        })
    orbit_records.sort(key=lambda row: (
        row["q_pair_cut_masks_e01_e02_e03_e12_e13_e23"],
        row["x_relation_masks_e01_e02_e03_e12_e13_e23"]))
    require(len(orbit_records) == 310 and
            sum(row["orbit_size"] for row in orbit_records) == len(survivors),
            "B4 x S3 survivor orbit census changed")
    q_geometry_histogram = Counter(
        tuple(row["q_pair_cut_masks_e01_e02_e03_e12_e13_e23"])
        for row in orbit_records)
    require(set(q_geometry_histogram) == {(0, 7, 25), (0, 30, 45)},
            "minimal Q-pair geometry orbit census changed")

    orbit_size_histogram = Counter(row["orbit_size"]
                                   for row in orbit_records)
    return {
        "encoding": {
            "X": ("Each e=0 block has a live diagonal or antidiagonal pair; "
                  "minimal supports retain exactly one, encoded by one bit."),
            "Q": ("The exact polarized identity on e=t=0 is "
                  "H=sum Q_s*Q_bar(s); minimal H-live support retains one "
                  "complementary transversal Q-pair, encoded by its cut mask."),
            "C": ("All nonanchor cofactor-support bits can be deleted in this "
                  "minimal Boolean shadow; anchor-complement cofactors are t=0."),
            "packet": ("The transverse 440 rows force the three Q-pairs distinct. "
                       "All 422 rows are then checked: only the transverse-majority "
                       "288-row orbit can fire on this minimal Q shadow, and its "
                       "six minor-edge allocations are the complementary-edge tests."),
        },
        "constraint_activity_on_minimal_shadow": {
            "master270_before_new_422_labelled_models": 336 * (64 ** 3),
            "440_2110": "inactive because every nontransversal Q bit is deleted",
            "422_two_edges_to_each_minor_colour":
                "active; cuts 88,080,384 models to 275,568",
            "422_majority_loop_colour_triangle":
                "inactive because every nontransversal Q bit is deleted",
            "422_majority_loop_minor_loop_two_cross_edges":
                "inactive because every nontransversal Q bit is deleted",
            "422_exact_e_multiple": "identically zero in the e=0 quotient",
        },
        "labelled_minimal_survivors": len(survivors),
        "q_triple_local_completion_histogram": {
            str(key): value for key, value in sorted(q_triple_histogram.items())},
        "B4_times_S3_orbits": len(orbit_records),
        "orbit_size_histogram": {
            str(key): value for key, value in sorted(orbit_size_histogram.items())},
        "q_geometry_orbit_refinement_counts": {
            ",".join(map(str, key)): value
            for key, value in sorted(q_geometry_histogram.items())},
        "minimal_surviving_support_signature_antichain": orbit_records,
    }


def no_good_ledger(shadow):
    records = []
    for name, relative in NO_GOOD_SOURCES:
        path = ROOT / relative
        require(path.is_file(), f"missing frozen no-good source {relative}")
        records.append({"name": name, "source": relative,
                        "source_sha256": file_sha(path)})
    # Every minimal shadow record has exactly two live transversal Q values
    # per colour.  The exact support6, support8, cycle, and A=B presentations
    # have respectively 6, >=8, 16, and 6 forced Q values.  TP is a named
    # coefficient chart rather than a support mask.  It would be unsound to
    # broaden any of these exact antecedents to a monotone support clause.
    return {
        "frozen_sources": records,
        "application_rule": (
            "Delete only an exact transported antecedent presentation, not a "
            "support containment or a same-cardinality lookalike."),
        "minimal_antichain_hits": {
            "support6_arbitrary_mate": 0,
            "support8_one_y_arbitrary_mate": 0,
            "k4_TP_boundary_or_interior": 0,
            "cycle_boundary": 0,
            "A_equals_B_mate_closure": 0,
        },
        "why_zero_hits": (
            "The Boolean-minimal antichain has |Q|=2 per colour. The frozen "
            "support6/support8/cycle/A=B antecedents force 6, at least 8, 16, "
            "and 6 Q values respectively, while TP requires coefficient-chart "
            "equalities not encoded by support. Thus the no-goods are present "
            "in the augmented ledger but do not soundly delete a minimal shadow."),
        "coefficient_identity_cases": {
            "q_geometry_0_7_25": (
                "Resolve the 0,7,25 complementary-Q triangle together with its "
                "B4 x S3 X-relation refinements."),
            "q_geometry_0_30_45": (
                "Resolve the exceptional 0,30,45 complementary-Q triangle "
                "together with its B4 x S3 X-relation refinements."),
            "total_exact_support_refinements": shadow["B4_times_S3_orbits"],
            "needed_lemma": (
                "A coefficient identity must show that each shadow is unrealizable "
                "under e=t=0, or route every realization to one of the exact "
                "transported no-good components. Support SAT alone cannot do so."),
        },
    }


def main():
    for path in (ROUTING, EXTENSION_440, EXTENSION_422, CORE_IDENTITY):
        require(path.is_file(), f"missing source {path}")
    packet = assemble_packet()
    shadow = support_shadow()
    result = {
        "status": "PASS exact packet assembly; SAT/support census is discovery-only",
        "packet_logical_sha256": packet["logical_sha256"],
        "packet_counts": packet["quotient_coverage"],
        "support_shadow": shadow,
        "exact_antecedent_no_goods": no_good_ledger(shadow),
        "scope_guard": (
            "The 1566+72 quotient equality is exact. The 310-orbit Boolean "
            "antichain is only the minimal monomial-support shadow: it forgets "
            "coefficient cancellations and does not prove existence or closure "
            "of any polynomial component. No SAT verdict is promoted to a theorem."),
        "source_hashes": {
            str(ROUTING.relative_to(ROOT)): file_sha(ROUTING),
            str(EXTENSION_440.relative_to(ROOT)): file_sha(EXTENSION_440),
            str(EXTENSION_422.relative_to(ROOT)): file_sha(EXTENSION_422),
            str(CORE_IDENTITY.relative_to(ROOT)): file_sha(CORE_IDENTITY),
        },
    }
    result["logical_sha256"] = logical_sha(result)
    packet_text = json.dumps(packet, indent=2, sort_keys=True) + "\n"
    result_text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if "--write-results" in sys.argv:
        PACKET_OUT.write_text(packet_text)
        RESULT_OUT.write_text(result_text)
    if "--check-results" in sys.argv:
        require(PACKET_OUT.read_text() == packet_text, "packet replay mismatch")
        require(RESULT_OUT.read_text() == result_text, "result replay mismatch")
    print(json.dumps({
        "status": result["status"],
        "packet_logical_sha256": packet["logical_sha256"],
        "result_logical_sha256": result["logical_sha256"],
        "explicit_rows": packet["explicit_generator_count"],
        "e_multiple_rows": len(packet["omitted_exact_e_multiple_orbit"]["rows"]),
        "minimal_shadow_survivors": shadow["labelled_minimal_survivors"],
        "minimal_shadow_orbits": shadow["B4_times_S3_orbits"],
        "q_geometry_counts": shadow["q_geometry_orbit_refinement_counts"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
