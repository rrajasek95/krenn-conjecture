#!/usr/bin/env python3
"""Audit whether the archive determines a global K14..K24 a*T residual.

This is intentionally an interface audit, not a choice of a new normal form.
It verifies the exact R8' and E-factor profiles and replays the frozen K16
literal stream byte-for-byte.  It then records the first provenance gap that
prevents those data from defining a residual iterator above K14.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
K14_SOURCE = (ROOT / "computations/unaudited-codex-orbit0-k14-interface-audit-2026-08-21"
              / "audit_orbit0_k14_interface.py")
R8_PATH = (ROOT / "computations/unaudited-codex-n8-dangerous-chart-bridge-2026-08-20"
           / "results_orbit0_cutoff9_sparse_r8.json")
K16_SOURCE = (ROOT / "computations/unaudited-codex-orbit0-k16-literal-collection-2026-08-22"
              / "collect_orbit0_k16_literal_residual.py")
K16_PATH = K16_SOURCE.with_name("results_orbit0_k16_literal_residual.json")
DAFSA_SOURCE = (ROOT / "computations/unaudited-codex-orbit0-k16-weighted-dafsa-2026-08-23"
                / "build_k16_weighted_dafsa.py")
DAFSA_RESULT = DAFSA_SOURCE.with_name("results_k16_weighted_dafsa.json")
CYCLE_RESULT = (ROOT / "computations/unaudited-codex-orbit0-k16-cycle-partition-referee-2026-08-23"
                / "results_balanced_cycle_partition_referee.json")
OUT = HERE / "results_global_residual_interface.json"

EXPECTED_K16_FILE_SHA = "28a648a2625d208cc86948b27a06f52f38245fe2ebe130c583e619d1d24b9189"
EXPECTED_K16_STREAM_SHA = "f92c91ad239f112185b29ec53157bfb02931b06bf481d71e3878b2c31e298328"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, path)
    spec.loader.exec_module(module)
    return module


def file_sha256(path):
    digest = sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def convolve(*profiles):
    answer = Counter({0: 1})
    for profile in profiles:
        updated = Counter()
        for left, a in answer.items():
            for right, b in profile.items():
                updated[left + right] += a * b
        answer = updated
    return answer


def main(write_results=False):
    k14 = load("global_residual_k14", K14_SOURCE)
    f = k14.FROZEN
    r8 = json.loads(R8_PATH.read_text())
    require(r8["exact_core_replay"] and r8["exact_reverse_pivot_replay"],
            "R8' replay flags changed")
    require(r8["residual_K_degree"] == 8 and r8["residual_quotient_orbits"] == 120
            and r8["residual_labelled_support"] == 148176,
            "R8' interface changed")
    require(all(f.row_k_degree(bytes.fromhex(row)) == 8
                for row, _num, _den in r8["residual"]),
            "R8' acquired a non-K8 row")

    words = tuple(f.word_from_pair_colours(row) for row in f.PAIR_COLOURS)
    anchors = tuple(f.BASE.term_ids(word, f.M0) for word in words)
    e_profiles = []
    for word, anchor in zip(words, anchors, strict=True):
        profile = Counter(f.row_k_degree(term) for term in f.BASE.word_terms(word)
                          if term != anchor)
        require(profile == {2: 12, 3: 32, 4: 60}, profile)
        e_profiles.append(profile)
    packet_profile = convolve(*e_profiles)
    expected_packet = {6: 1728, 7: 13824, 8: 62784, 9: 171008,
                       10: 313920, 11: 345600, 12: 216000}
    require(packet_profile == expected_packet, packet_profile)

    # Every K0 singleton source has the same complete tail profile.  The
    # frozen collector nevertheless materializes only the K2 part.
    from itertools import product
    singleton_profiles = Counter()
    for colours in product(range(3), repeat=4):
        if len(set(colours)) == 1:
            continue
        word = f.word_from_pair_colours(colours)
        singleton_profiles[tuple(sorted(Counter(
            f.row_k_degree(term) for term in f.BASE.word_terms(word)
        ).items()))] += 1
    require(singleton_profiles == {((0, 1), (2, 12), (3, 32), (4, 60)): 78},
            singleton_profiles)

    k16_sha = file_sha256(K16_PATH)
    require(k16_sha == EXPECTED_K16_FILE_SHA, "frozen K16 JSON changed")
    dafsa = load("global_residual_dafsa", DAFSA_SOURCE)
    stream = sha256()
    count = 0
    for count, (row, numerator, denominator) in enumerate(
            dafsa.literal_records(K16_PATH), 1):
        stream.update(row)
        stream.update(numerator.to_bytes(8, "little", signed=True))
        stream.update(denominator.to_bytes(8, "little", signed=True))
    require(count == 1848174 and stream.hexdigest() == EXPECTED_K16_STREAM_SHA,
            (count, stream.hexdigest()))
    k16 = json.loads(K16_PATH.read_text())
    require(k16["collection"]["reducible_K16_tail_occurrences"] == 75691040,
            "reducible K16 census changed")
    require(k16["source_provenance"]["literal_K2_tails_per_row"] == [12],
            "collector is no longer K2-only")
    require("leading K14 polynomial" in k16["theorem"]["input"],
            "frozen K16 scope wording changed")

    dafsa_result = json.loads(DAFSA_RESULT.read_text())
    require(dafsa_result["input"]["input_file_sha256"] == k16_sha
            and dafsa_result["input"]["literal_stream_sha256"] == stream.hexdigest(),
            "DAFSA no longer pins the frozen K16 stream")
    cycle = json.loads(CYCLE_RESULT.read_text())
    require(cycle["streamed_target"]["target_pairing"] == -311258112,
            "frozen K16 cycle charge changed")

    source_text = K16_SOURCE.read_text()
    require("if pivots(row_signature):" in source_text
            and "reducible_tail_occurrences += 1" in source_text
            and "continue" in source_text,
            "collector's quotient-only branch changed")

    input_occurrences = {
        str(8 + degree): count * r8["residual_labelled_support"]
        for degree, count in sorted(packet_profile.items())
    }
    result = {
        "status": "BLOCKED_MISSING_COMPLETE_RESIDUAL_PROVENANCE",
        "exact_input": {
            "identity": "full pre-reduction residual is -R8prime*E0*E1*E2",
            "R8prime_support": "K8 only",
            "R8prime_labelled_rows": 148176,
            "each_E_K_profile": {str(k): v for k, v in sorted(e_profiles[0].items())},
            "E_product_K_profile": {str(k): v for k, v in sorted(packet_profile.items())},
            "raw_labelled_occurrences_by_total_K": input_occurrences,
            "support_range": "K14..K20 before any singleton reduction",
        },
        "singleton_source": {
            "rows": 78,
            "complete_profile": {"K0": 1, "K2": 12, "K3": 32, "K4": 60},
            "first_K14_rule": (
                "reconstructible: average all valid pivots selected by the frozen "
                "25-signature cover"
            ),
        },
        "frozen_K16_replay": {
            "records": count,
            "json_sha256": k16_sha,
            "literal_stream_sha256": stream.hexdigest(),
            "DAFSA_logical_sha256": dafsa_result["logical_sha256"],
            "cycle_charge": cycle["streamed_target"]["target_pairing"],
            "scope": (
                "quotient of the leading K14 polynomial through K2 pivot tails; "
                "not the K16 slice of the full -R8prime*E0*E1*E2 residual"
            ),
        },
        "first_missing_data": [
            (
                "A source-labelled reduction choice/weight ledger for the genuine "
                "K15 layer of -R8prime*E0*E1*E2.  It is present before the frozen "
                "K16 quotient and was never processed by that collector."
            ),
            (
                "Complete K3/K4 tails of the recorded averaged K14 pivots in the "
                "chosen global residual state.  They are reconstructible from the "
                "rule, but no collected K17/K18 state was frozen."
            ),
            (
                "A pivot choice/weight ledger for the 75,691,040 reducible K16 "
                "tail occurrences.  The collector merely discards them modulo the "
                "K0 initial ideal, so their K18/K19/K20 transfer tails are undefined."
            ),
        ],
        "requested_global_charge": (
            "undefined from the archive: only the frozen leading-term K16 charge "
            "-311258112 is certified; charges at K15 and K17..K24 depend on the "
            "missing reduction choices"
        ),
        "minimal_safe_continuation": (
            "Freeze one H-equivariant ascending-K normal-form policy beginning at "
            "K15, record every literal pivot coefficient and all K2/K3/K4 tails, "
            "then replay K16 against the full input.  Without that ledger, selecting "
            "new pivots would invent a residual rather than reconstruct the archive."
        ),
        "pinned": {
            str(R8_PATH.relative_to(ROOT)): file_sha256(R8_PATH),
            str(K14_SOURCE.relative_to(ROOT)): file_sha256(K14_SOURCE),
            str(K16_SOURCE.relative_to(ROOT)): file_sha256(K16_SOURCE),
            str(K16_PATH.relative_to(ROOT)): k16_sha,
            str(DAFSA_RESULT.relative_to(ROOT)): file_sha256(DAFSA_RESULT),
            str(CYCLE_RESULT.relative_to(ROOT)): file_sha256(CYCLE_RESULT),
        },
    }
    logical = sha256(json.dumps(result, sort_keys=True,
                                separators=(",", ":")).encode()).hexdigest()
    result["logical_sha256"] = logical
    if write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "K16_records": count,
        "K16_stream_sha256": stream.hexdigest(),
        "logical_sha256": logical,
        "first_missing_data": result["first_missing_data"],
    }, indent=2))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    main(args.write_results)
