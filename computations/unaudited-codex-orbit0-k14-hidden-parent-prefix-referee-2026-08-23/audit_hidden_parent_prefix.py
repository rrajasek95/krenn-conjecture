#!/usr/bin/env python3
"""Independent bounded replay of sampled hidden K14->K16 parent records."""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import ast
import importlib.util
import json
from pathlib import Path
import struct


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PACKET = ROOT / "computations/unaudited-codex-orbit0-k14-hidden-k16-parent-prefix-2026-08-23"
SOURCE = PACKET / "reconstruct_hidden_k16_parent_prefix.rs"
PARENTS = PACKET / "hidden_k16_parents_prefix.bin"
PROFILES = PACKET / "hidden_k16_second_pivot_profiles_prefix.bin"
PREFIX_RESULT = PACKET / "results_hidden_k16_parent_prefix.json"
DESIGN = ROOT / "computations/unaudited-codex-orbit0-filtered-k24-reducer-design-2026-08-23/filtered_k24_reducer.py"
COVER = ROOT / "computations/unaudited-codex-orbit0-k14-interface-audit-2026-08-21/results_k16_anchor_cover.json"
FROZEN = ROOT / "computations/unaudited-codex-orbit0-k16-literal-collection-2026-08-22/results_orbit0_k16_literal_residual.json"
OUT = HERE / "results_hidden_parent_prefix_referee.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(path):
    spec = importlib.util.spec_from_file_location("hidden_parent_design", path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, path)
    spec.loader.exec_module(module)
    return module


D = load(DESIGN)


def valid_pivots(signature, cover):
    valid = []
    for pivot in D.CTX.pivots(signature):
        base = tuple(a - b for a, b in
                     zip(signature, D.CTX.vectors[pivot], strict=True))
        survivors = set()
        for tail in D.CTX.tails[pivot][2]:
            counts = Counter(tail)
            child = tuple(a + counts[cell] for a, cell in
                          zip(base, D.CTX.anchor_cells, strict=True))
            if not D.CTX.pivots(child):
                survivors.add(D.CTX.canonical_signature(child))
        if survivors <= cover:
            valid.append(pivot)
    require(valid, signature)
    return tuple(valid)


def subtract(row, anchor):
    value = Counter(row)
    value.subtract(anchor)
    require(all(x >= 0 for x in value.values()), (row.hex(), anchor.hex()))
    return bytes(sorted(cell for cell, count in value.items()
                        for _ in range(count)))


def main():
    prefix = json.loads(PREFIX_RESULT.read_text())
    frozen = json.loads(FROZEN.read_text())
    require(prefix["status"] == "PASS_MEASURED_PREFIX", prefix["status"])
    require(prefix["sample"]["H_slices"] == 31, prefix["sample"])
    require(frozen["collection"]["reducible_K16_tail_occurrences"]
            == 75_691_040, "frozen full count changed")

    cover_raw = json.loads(COVER.read_text())
    cover = frozenset(ast.literal_eval(row) for row in cover_raw
                      ["single_pivot_cover"]["minimum_cover_orbit_representatives"])
    records = D.r8_h_records()
    factor_words = tuple(D.F.word_from_pair_colours(row)
                         for row in D.F.PAIR_COLOURS)
    factor_pivots = tuple(D.CTX.anchor_to_pivot[
        D.F.BASE.term_ids(word, D.F.M0)] for word in factor_words)
    factor_tails = tuple(D.CTX.tails[pivot][2] for pivot in factor_pivots)
    require(tuple(map(len, factor_tails)) == (12, 12, 12), "factor tails")

    raw = PARENTS.read_bytes()
    require(raw[:8] == b"H16PAR1\0", raw[:8])
    scale = int.from_bytes(raw[8:24], "little", signed=True)
    modulus = int.from_bytes(raw[24:28], "little")
    count = int.from_bytes(raw[28:36], "little")
    require(scale == 400_591_699_200, scale)
    require(modulus == 16, modulus)
    require(len(raw) == 36 + 64 * count, (len(raw), count))
    require(count == prefix["hidden_parent_occurrences"], (count, prefix))

    # Deterministic, evenly spread source replay; intentionally not a duplicate
    # of the 4.8-million-record prefix construction.
    sample_indices = sorted({0, count - 1} |
                            {i * (count - 1) // 256 for i in range(257)})
    signs = Counter()
    denominator_pairs = Counter()
    for index in sample_indices:
        start = 36 + 64 * index
        item = raw[start:start + 64]
        row = item[:24]
        weight = int.from_bytes(item[24:40], "little", signed=True)
        signature = tuple(item[40:52])
        ri = int.from_bytes(item[52:54], "little")
        ia, ib, ic, p1, t1, m1, m2, z0, z1, z2 = item[54:64]
        require((z0, z1, z2) == (0, 0, 0), index)
        require(ri % 16 == 0 and ri < len(records), (index, ri))
        require(max(ia, ib, ic) < 12 and p1 < 78 and t1 < 12, index)
        r8, orbit_size, coefficient = records[ri]
        head = bytes(sorted(r8 + factor_tails[0][ia] +
                            factor_tails[1][ib] + factor_tails[2][ic]))
        first = valid_pivots(tuple(Counter(head)[cell]
                                   for cell in D.CTX.anchor_cells), cover)
        require(p1 in first and len(first) == m1, (index, p1, first, m1))
        expected_row = bytes(sorted(subtract(head, D.CTX.anchors[p1]) +
                                    D.CTX.tails[p1][2][t1]))
        require(row == expected_row and row == bytes(sorted(row)), index)
        expected_signature = tuple(Counter(row)[cell]
                                   for cell in D.CTX.anchor_cells)
        second = D.CTX.pivots(expected_signature)
        require(signature == expected_signature and len(second) == m2 and m2,
                (index, signature, expected_signature, second, m2))
        mass = Fraction(orbit_size) * coefficient
        require(mass.denominator == 1, (index, mass))
        expected_weight = mass.numerator * scale // m1
        require(mass.numerator * scale % m1 == 0, (index, mass, m1))
        require(weight == expected_weight, (index, weight, expected_weight))
        signs["positive_transition_formula"] += 1
        denominator_pairs[(m1, m2)] += 1
        for pivot in second:
            quotient = subtract(row, D.CTX.anchors[pivot])
            require(len(quotient) == 20, (index, pivot))
            require(tuple(len(D.CTX.tails[pivot][degree])
                          for degree in (2, 3, 4)) == (12, 32, 60),
                    (index, pivot))

    profile_raw = PROFILES.read_bytes()
    require(profile_raw[:8] == b"H16PRO1\0", profile_raw[:8])
    require(int.from_bytes(profile_raw[8:24], "little", signed=True) == scale,
            "profile scale")
    profile_count = int.from_bytes(profile_raw[28:36], "little")
    require(len(profile_raw) == 36 + 59 * profile_count,
            (len(profile_raw), profile_count))
    require(profile_count == prefix["unique_nonzero_second_pivot_profiles"],
            (profile_count, prefix))
    degree_bytes = Counter(profile_raw[36 + 59 * i + 42]
                           for i in range(profile_count))
    require(degree_bytes == {0: profile_count}, degree_bytes)

    result = {
        "status": "PASS_PREFIX_OCCURRENCE_REPLAY_WITH_FULL_COUNT_SCOPE_GUARD",
        "prefix": {
            "H_slices": 31,
            "hidden_parent_occurrences": count,
            "sampled_occurrence_records_replayed": len(sample_indices),
            "outgoing_second_pivot_uses": prefix["outgoing_second_pivot_uses"],
            "labelled_wildcard_profiles": profile_count,
        },
        "sign": {
            "stored_parent_weight": "+mass*U/m1, correct for P=-R8prime*E2^3",
            "next_transition_weight": "-stored_parent_weight/m2",
        },
        "provenance": (
            "Each 64-byte parent record stores the literal K16 row, exact "
            "U-scaled coefficient, signature, R8 slice, three factor-tail "
            "indices, first pivot/tail, and both denominators. Row+signature "
            "reconstruct every second pivot and its 12/32/60 K2/K3/K4 tails."
        ),
        "aggregation_scope": (
            "The parent stream is labelled H-slice provenance with exact H-orbit "
            "mass. The 59-byte profile stream is an exact labelled wildcard "
            "aggregation, not an H-canonical aggregation."
        ),
        "full_count_scope": (
            "The prefix independently reconstructs only 31/485 H slices. "
            "75,691,040 is pinned from the frozen full collector and copied as "
            "known_full_hidden_occurrences; it is not recovered by this prefix."
        ),
        "sample_denominator_pairs": {
            f"{a}x{b}": n for (a, b), n in sorted(denominator_pairs.items())
        },
        "pinned": {
            str(path.relative_to(ROOT)): sha256(path.read_bytes()).hexdigest()
            for path in (SOURCE, PARENTS, PROFILES, PREFIX_RESULT, DESIGN,
                         COVER, FROZEN)
        },
        "scope": "Bounded evenly spread record replay; no full recovery or child-tail emission.",
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode()).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
