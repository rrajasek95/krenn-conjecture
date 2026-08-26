#!/usr/bin/env python3
"""Exact, no-solve audit of the chart-1 boundary owner shell.

This checker does not repeat modular elimination.  It reads the frozen D12
insertion ledger and the independently replayed literal private-row census,
then classifies the accepted round 6--12 columns by source word and physical
multiplier skeleton.  The private-row result supplies the exact Schur block.
"""

from collections import Counter, defaultdict
from hashlib import sha256
import argparse
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = (ROOT / "computations"
          / "unaudited-codex-n8-chart1-boundary-a0200-2026-08-23")
EXPORT = SOURCE / "export_chart1_boundary.py"
CHECKPOINT = SOURCE / "checkpoint_d12_incremental_cegar.json"
OLD_CHECKPOINT = SOURCE / "checkpoint_d12_lazy_cegar.json"
OWNERSHIP = SOURCE / "results_d12_private_ownership.json"
EXTERNAL_OWNER = SOURCE / "results_d12_first_external_owner.json"
RESULT = HERE / "results_boundary_owner_shell.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def file_sha256(path):
    return sha256(path.read_bytes()).hexdigest()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, f"cannot load {path}")
    spec.loader.exec_module(module)
    return module


E = load(EXPORT, "boundary_owner_shell_export")
D5 = E.D5


def word_profile(code):
    counts = sorted(Counter(D5.decode_word(code)).values(), reverse=True)
    return "".join(str(value) for value in counts)


def physical_skeleton(multiplier):
    edges = []
    degree = Counter()
    adjacency = defaultdict(set)
    for identifier in multiplier:
        i, j, _a, _b = D5.COORDINATES[identifier]
        edges.append((i, j))
        degree[i] += 1
        degree[j] += 1
        adjacency[i].add(j)
        adjacency[j].add(i)
    unseen = set(degree)
    components = 0
    while unseen:
        components += 1
        stack = [unseen.pop()]
        while stack:
            vertex = stack.pop()
            fresh = adjacency[vertex] & unseen
            unseen.difference_update(fresh)
            stack.extend(fresh)
    cyclomatic = len(edges) - len(degree) + components
    degrees = "".join(str(value)
                      for value in sorted(degree.values(), reverse=True))
    return f"v{len(degree)}-d{degrees}-c{components}-mu{cyclomatic}"


def sorted_counter(counter):
    return {str(key): counter[key] for key in sorted(counter, key=str)}


def classify(columns):
    profiles = Counter()
    lengths = Counter()
    off_colours = Counter()
    skeletons = Counter()
    codes = set()
    multipliers = set()
    for code, multiplier in columns:
        codes.add(code)
        multipliers.add(multiplier)
        profiles[word_profile(code)] += 1
        lengths[len(multiplier)] += 1
        off_colours[sum(D5.COORDINATES[value][2]
                        != D5.COORDINATES[value][3]
                        for value in multiplier)] += 1
        skeletons[physical_skeleton(multiplier)] += 1
    return {
        "columns": len(columns),
        "distinct_word_codes": len(codes),
        "distinct_multipliers": len(multipliers),
        "word_profiles": sorted_counter(profiles),
        "multiplier_lengths": sorted_counter(lengths),
        "offdiagonal_colour_factors": sorted_counter(off_colours),
        "physical_skeletons": sorted_counter(skeletons),
    }


EXPECTED = {
    6: {
        "columns": 42, "distinct_word_codes": 1, "distinct_multipliers": 42,
        "word_profiles": {"44": 42},
        "multiplier_lengths": {"2": 24, "3": 18},
        "offdiagonal_colour_factors": {"0": 12, "2": 26, "3": 4},
        "physical_skeletons": {
            "v4-d1111-c2-mu0": 24, "v6-d111111-c3-mu0": 18,
        },
    },
    7: {
        "columns": 523, "distinct_word_codes": 18, "distinct_multipliers": 52,
        "word_profiles": {"422": 238, "44": 123, "62": 162},
        "multiplier_lengths": {"3": 247, "4": 276},
        "offdiagonal_colour_factors": {"0": 51, "2": 432, "3": 40},
        "physical_skeletons": {
            "v6-d111111-c3-mu0": 247, "v8-d11111111-c4-mu0": 276,
        },
    },
    8: {
        "columns": 639, "distinct_word_codes": 18, "distinct_multipliers": 64,
        "word_profiles": {"422": 291, "44": 150, "62": 198},
        "multiplier_lengths": {"3": 441, "4": 198},
        "offdiagonal_colour_factors": {"0": 78, "2": 327, "3": 156, "4": 78},
        "physical_skeletons": {
            "v6-d111111-c3-mu0": 441, "v8-d11111111-c4-mu0": 198,
        },
    },
    9: {
        "columns": 708, "distinct_word_codes": 106, "distinct_multipliers": 60,
        "word_profiles": {
            "332": 12, "422": 259, "431": 20, "44": 156, "521": 20,
            "53": 8, "611": 8, "62": 221, "71": 4,
        },
        "multiplier_lengths": {"2": 88, "4": 620},
        "offdiagonal_colour_factors": {"0": 108, "1": 36, "2": 278, "4": 286},
        "physical_skeletons": {
            "v4-d1111-c2-mu0": 88, "v4-d2222-c1-mu1": 112,
            "v4-d2222-c2-mu2": 508,
        },
    },
    10: {
        "columns": 2025, "distinct_word_codes": 42, "distinct_multipliers": 184,
        "word_profiles": {
            "332": 3, "422": 876, "431": 4, "44": 472, "521": 4,
            "53": 4, "611": 1, "62": 659, "71": 2,
        },
        "multiplier_lengths": {"2": 24, "4": 2001},
        "offdiagonal_colour_factors": {"0": 222, "1": 18, "2": 853, "4": 932},
        "physical_skeletons": {
            "v4-d1111-c2-mu0": 24, "v4-d2222-c1-mu1": 836,
            "v4-d2222-c2-mu2": 112, "v6-d221111-c2-mu0": 1053,
        },
    },
    11: {
        "columns": 969, "distinct_word_codes": 18, "distinct_multipliers": 81,
        "word_profiles": {"422": 411, "44": 234, "62": 324},
        "multiplier_lengths": {"4": 969},
        "offdiagonal_colour_factors": {"0": 150, "2": 464, "4": 355},
        "physical_skeletons": {"v8-d11111111-c4-mu0": 969},
    },
    12: {
        "columns": 39, "distinct_word_codes": 18, "distinct_multipliers": 4,
        "word_profiles": {"422": 18, "44": 9, "62": 12},
        "multiplier_lengths": {"4": 39},
        "offdiagonal_colour_factors": {"0": 39},
        "physical_skeletons": {"v8-d11111111-c4-mu0": 39},
    },
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutate", action="store_true",
                        help="hostile mutation: corrupt the owner coverage")
    arguments = parser.parse_args()

    checkpoint = json.loads(CHECKPOINT.read_text())
    old_checkpoint = json.loads(OLD_CHECKPOINT.read_text())
    ownership = json.loads(OWNERSHIP.read_text())
    external_owner = json.loads(EXTERNAL_OWNER.read_text())
    sequence = [(int(code), bytes.fromhex(multiplier))
                for code, multiplier in checkpoint["column_insertion_sequence"]]
    require(len(sequence) == 7516 and len(set(sequence)) == 7516,
            "insertion sequence changed")

    # The exact historical singleton is frozen only in the old lazy checkpoint.
    require(old_checkpoint["last_dual"] == [["0d55b8ee", 1, 1]],
            "round-6 singleton dual changed")
    singleton = bytes.fromhex("0d55b8ee")
    singleton_factors = [list(D5.COORDINATES[value]) for value in singleton]
    require(singleton_factors == [
        [0, 2, 1, 1], [1, 4, 1, 1], [3, 6, 1, 1], [5, 7, 1, 1],
    ], "round-6 singleton source labels changed")

    rounds = {}
    for record in checkpoint["ledger"]:
        round_number = record["round"]
        if not 6 <= round_number <= 12:
            continue
        start = record["columns"]
        count = record["new_violating_column_orbits"]
        actual = classify(sequence[start:start + count])
        require(actual == EXPECTED[round_number],
                f"round {round_number} classification changed: {actual}")
        rounds[str(round_number)] = actual

    accepted = ownership["accepted_repairs"]
    pending = ownership["round13_pending"]
    coverage = accepted["columns_with_global_private_new_row"]
    if arguments.mutate:
        coverage -= 1
    require(accepted["columns"] == 4903 and coverage == 4903,
            "hostile mutation/private coverage failure")
    require(accepted["all_columns_have_global_private_new_row"],
            "accepted owner shell is not complete")
    require(min(value for value, _count
                in accepted["private_rows_per_column_histogram"]) == 5,
            "private-owner lower bound changed")
    require(pending["violating_unselected_column_orbits"] == 1186
            and pending["columns_with_private_new_row"] == 1186
            and pending["all_columns_have_private_new_row"],
            "round-13 owner shell changed")

    require(external_owner["shell_column"] == [4, "0a52b8ee"]
            and external_owner["shell_private_row"] == "0a12515291c1e5eb"
            and external_owner["shell_coefficient"] == 1
            and external_owner["target_coefficient"] == 0
            and external_owner["external_column"]
            == [4, "0a12515291c1e5eb"]
            and external_owner["external_coefficient"] == 1
            and not external_owner["external_is_selected"]
            and external_owner["incident_count"] == 91,
            "external owner counterguard changed")

    witness = accepted["lex_first_literal_witness"]
    require(witness == {
        "local_column_id": 0,
        "column": [4, "0a51b7ea"],
        "row": "0a12515191b7eaeb",
        "coefficient": 1,
        "literal_hits": [[4, "0a51b7ea", "125191eb", 1]],
    }, "lex-first literal private owner changed")

    # The ledger intentionally freezes only dual sizes after round 6.  This is
    # an archive fact, not a mathematical inference.
    missing_historical_dual_labels = all(
        "dual_rows" not in record and "dual" not in record
        for record in checkpoint["ledger"] if 7 <= record["round"] <= 12
    )
    require(missing_historical_dual_labels,
            "historical dual-label archive interface changed")

    rank_growth = {}
    for record in checkpoint["ledger"]:
        if 7 <= record["round"] <= 12:
            require(record["accepted_rank_increment"]
                    == record["new_violating_column_orbits"]
                    and record["accepted_zero_columns"] == 0,
                    f"round {record['round']} rank ledger changed")
            rank_growth[str(record["round"])] = {
                "accepted_columns": record["new_violating_column_orbits"],
                "rank_increment_mod_1073741827": record["accepted_rank_increment"],
                "dual_support_size": record["dual_support"],
            }

    payload = {
        "format": "n8-chart1-boundary-owner-shell-v1",
        "status": "EXACT_PRIVATE_OWNER_SCHUR_BLOCK_CONSERVES_OLD_COKERNEL",
        "scope": (
            "Exact Q split-injectivity of the accepted r7-r12 attachment shell "
            "relative to the frozen 2613-column interface, plus the analogous "
            "pending r13 shell. Privacy is only within each enumerated shell: "
            "unselected D12 columns are not part of this matrix and may cross its "
            "owner rows. This is not terminal D12 membership, saturation, a full "
            "ideal separator, or an all-round recurrence theorem."
        ),
        "round6_singleton": {
            "row": singleton.hex(),
            "coefficient": [1, 1],
            "source_factors": singleton_factors,
            "accepted_killing_column_orbits": 42,
            "source_replay_guard": (
                "The frozen invariant-orbit representatives are all word profile "
                "44; the 62/422 profiles begin at the next accepted shell."
            ),
        },
        "round_classification": rounds,
        "rank_growth": rank_growth,
        "owner_schur_block": {
            "old_columns": ownership["old_interface"]["columns"],
            "old_rows_including_target": ownership["old_interface"]["rows_including_target"],
            "shell_columns": accepted["columns"],
            "new_rows": accepted["distinct_new_rows"],
            "degree_one_new_rows": accepted["degree_one_new_rows"],
            "columns_with_shell_private_owner": coverage,
            "minimum_shell_private_owners_per_column": 5,
            "lex_first_literal_witness": witness,
            "lemma": (
                "Choose one shell-private beyond-interface row rho(c) for each "
                "enumerated shell column c. Projection of that shell's literal "
                "attachment matrix to "
                "{rho(c)} is diagonal with nonzero integer diagonal, hence is "
                "split-injective over Q. No nonzero combination of these shell "
                "columns lands in the old row interface."
            ),
            "cokernel_consequence": (
                "For the matrix containing exactly the old columns plus the "
                "enumerated r7-r12 shell, the old row-interface cokernel injects "
                "into the enlarged cokernel. This does not survive automatically "
                "after adjoining unenumerated D12 columns that cross owner rows."
            ),
        },
        "round13_counterguard": {
            "pending_columns": pending["violating_unselected_column_orbits"],
            "columns_with_shell_private_owner": pending["columns_with_private_new_row"],
            "new_rows": pending["distinct_new_rows"],
            "degree_one_new_rows": pending["degree_one_new_rows"],
            "lex_first_external_owner": {
                "shell_column": external_owner["shell_column"],
                "shell_private_row": external_owner["shell_private_row"],
                "shell_coefficient": external_owner["shell_coefficient"],
                "target_coefficient": external_owner["target_coefficient"],
                "incident_column_orbits": external_owner["incident_count"],
                "external_column": external_owner["external_column"],
                "external_coefficient": external_owner["external_coefficient"],
                "external_is_selected": external_owner["external_is_selected"],
            },
        },
        "recurrence_verdict": {
            "finite_packet_closed": False,
            "reason": (
                "Rounds 7-8 use only matching multipliers and three word profiles; "
                "rounds 9-10 introduce C4, parallel-double, and P3+P2 skeletons "
                "and all nine mixed profiles; rounds 11-12 return to matching "
                "skeletons, while round 13 opens another private owner shell."
            ),
            "smallest_exact_counterguard": witness,
            "full_d12_counterguard": (
                "Shell-private is not globally private: the full incident owner "
                "census finds previously unselected D12 columns crossing these "
                "rows. Therefore this Schur block cannot be promoted to a full "
                "separator without adjoining the external owner shell."
            ),
        },
        "archive_guard": {
            "historical_dual_labels_rounds7_to12_frozen": False,
            "historical_dual_support_sizes_frozen": True,
            "consequence": (
                "The exact killing-column attachment complex is replayable, but "
                "the r7-r12 dual row labels cannot be reconstructed byte-for-byte "
                "without repeating the rank solve."
            ),
        },
        "checkpoint_sha256": file_sha256(CHECKPOINT),
        "old_checkpoint_sha256": file_sha256(OLD_CHECKPOINT),
        "ownership_sha256": file_sha256(OWNERSHIP),
        "ownership_logical_sha256": ownership["logical_sha256"],
        "external_owner_sha256": file_sha256(EXTERNAL_OWNER),
        "source_sha256": file_sha256(Path(__file__)),
    }
    logical = dict(payload)
    logical.pop("source_sha256")
    payload["logical_sha256"] = sha256(
        json.dumps(logical, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    RESULT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("PASS", payload["logical_sha256"])


if __name__ == "__main__":
    main()
