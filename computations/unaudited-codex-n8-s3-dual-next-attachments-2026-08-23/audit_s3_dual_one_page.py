#!/usr/bin/env python3
"""One Schur/Bockstein page after the 14 singleton S3-dual killers."""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LOW_PATH = ROOT / "computations/unaudited-codex-n8-s3-source-component-2026-08-23/audit_s3_source_component.py"
HPL_PATH = ROOT / "computations/unaudited-codex-n8-s3-source-hpl-audit-2026-08-23/audit_s3_source_hpl.py"
PURE_REPORT = ROOT / "computations/unaudited-codex-triangle-pure-quotient-collapse-2026-08-22/REPORT.md"
RESULTS = HERE / "results_s3_dual_one_page.json"
REPORT = HERE / "ONE_PAGE_REPORT.md"

EXPECTED = {
    LOW_PATH: "a4d22563904e8dde445067b9e8c466cd048ea471ffdaac566b66202eec1ae189",
    HPL_PATH: "a983e37145dbf480262868a45b91aa42c07d9d72f74e85a395ea099220687479",
    PURE_REPORT: "10537d9ba02cd05a18a7c9a0dad88ca2e2e452747bce7f95a066e3d82306d9f4",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, f"cannot load {path}")
    spec.loader.exec_module(module)
    return module


def modular_rank(rows, columns, prime):
    row_index = {row: index for index, row in enumerate(rows)}
    pivots = {}
    for column in columns:
        vector = {row_index[row]: value % prime for row, value in column.items()
                  if value % prime}
        while vector:
            pivot = min(vector)
            if pivot not in pivots:
                break
            scale = vector[pivot]
            for index, coefficient in pivots[pivot].items():
                value = (vector.get(index, 0) - scale * coefficient) % prime
                if value:
                    vector[index] = value
                else:
                    vector.pop(index, None)
        if vector:
            pivot = min(vector)
            inverse = pow(vector[pivot], prime - 2, prime)
            pivots[pivot] = {index: value * inverse % prime
                             for index, value in vector.items()}
    return len(pivots)


def verify_dual(dual, columns, target):
    require(all(sum(dual.get(row, 0) * value for row, value in column.items()) == 0
                for column in columns), "candidate induced dual does not annihilate columns")
    pairing = sum(dual.get(row, 0) * value for row, value in target.items())
    require(pairing == 1, "candidate induced dual lost unit target pairing")
    return pairing


def main():
    for path, digest in EXPECTED.items():
        require(sha256(path.read_bytes()).hexdigest() == digest, f"source drift: {path}")
    LOW = load("s3_one_page_low", LOW_PATH)
    HPL = load("s3_one_page_hpl", HPL_PATH)
    D5 = LOW.load_normalized().D5
    polynomials = LOW.normalized_polynomials(D5)
    s3 = LOW.parse_kernel("S3")
    h3 = LOW.parse_kernel("H3")
    target = {row: value for row, value in s3.items() if row not in h3}
    rows, old_columns_dict = LOW.build_low_component(target, polynomials)
    old_columns = list(old_columns_dict.values())
    require((len(rows), len(old_columns)) == (1311, 330), "old low component changed")

    tiny = {
        bytes.fromhex("0c4fcc"): 1,
        bytes.fromhex("1557a7"): 1,
        bytes.fromhex("3072a7"): -1,
    }
    degree1_sources = defaultdict(list)
    for code, polynomial in polynomials.items():
        for row in polynomial:
            if len(row) == 1:
                degree1_sources[row].append(code)
    killers = {}
    for target_row in tiny:
        for positions in combinations(range(3), 2):
            multiplier = bytes(sorted(target_row[position] for position in positions))
            base = bytes(target_row[position] for position in range(3)
                         if position not in positions)
            for code in degree1_sources[base]:
                full = Counter()
                for row, value in polynomials[code].items():
                    full[bytes(sorted(multiplier + row))] += value
                low = {row: value for row, value in full.items() if len(row) == 3}
                tail = {row: value for row, value in full.items() if len(row) > 3}
                require(low == {target_row: 1}, "killer low layer changed")
                require(Counter(map(len, tail)) == Counter({4: 6, 5: 30, 6: 68}),
                        "killer tail profile changed")
                killers[(code, multiplier)] = {
                    "hit": target_row, "low": low, "tail": tail,
                }
    require(len(killers) == 14, "killer census changed")
    hit_histogram = Counter(record["hit"].hex() for record in killers.values())
    require(hit_histogram == Counter({"0c4fcc": 4, "1557a7": 6, "3072a7": 4}),
            "killer hit partition changed")

    induced = {
        "0c4fcc": {
            bytes.fromhex("1557a7"): 1,
            bytes.fromhex("2045ae"): 1,
            bytes.fromhex("3072a7"): -1,
        },
        "1557a7": {
            bytes.fromhex("0c4fcc"): 1,
            bytes.fromhex("1e4ea7"): 1,
            bytes.fromhex("3072a7"): -1,
        },
        "3072a7": {
            bytes.fromhex("0c4fcc"): 1,
            bytes.fromhex("1eb7bd"): 1,
            bytes.fromhex("2799b7"): -1,
        },
    }
    group_records = {}
    for hit_hex, dual in induced.items():
        singleton = {bytes.fromhex(hit_hex): 1}
        columns = old_columns + [singleton]
        verify_dual(dual, columns, target)
        rank_profile = {}
        for prime in (1009, 1013):
            rank_profile[str(prime)] = {
                "columns": modular_rank(rows, columns, prime),
                "with_target": modular_rank(rows, columns + [target], prime),
            }
        require(set((item["columns"], item["with_target"])
                    for item in rank_profile.values()) == {(331, 332)},
                "single-killer rank profile changed")
        packets = HPL.internal_response_restrictions(dual)
        expected_packets = 0 if hit_hex == "3072a7" else 1
        require(len(packets) == expected_packets, "induced carrier restriction changed")
        group_records[hit_hex] = {
            "killers": hit_histogram[hit_hex],
            "induced_dual": [[row.hex(), value] for row, value in sorted(dual.items())],
            "rank_profile": rank_profile,
            "internal_response_packets": list(packets.values()),
            "tail_profile_each": {"4": 6, "5": 30, "6": 68},
            "tail_support_each": 104,
            "Schur_tail_status": (
                "UNREACHED: the target remains nonzero in the y<=3 cokernel, so no "
                "choice of old low columns cancels the low layer and defines a higher-y tail"
            ),
        }

    all_singletons = [{record["hit"]: 1} for record in killers.values()]
    all_columns = old_columns + all_singletons
    all_dual = {
        bytes.fromhex("1eb7bd"): 1,
        bytes.fromhex("2045ae"): 1,
        bytes.fromhex("2799b7"): -1,
    }
    verify_dual(all_dual, all_columns, target)
    all_rank_profile = {}
    for prime in (1009, 1013):
        all_rank_profile[str(prime)] = {
            "columns": modular_rank(rows, all_columns, prime),
            "with_target": modular_rank(rows, all_columns + [target], prime),
        }
    require(set((item["columns"], item["with_target"])
                for item in all_rank_profile.values()) == {(333, 334)},
            "all-killer rank profile changed")
    require(not HPL.internal_response_restrictions(all_dual),
            "all-killer induced dual entered a triangle response channel")

    result = {
        "format": "n8-S3-dual-one-Schur-page-v1",
        "status": "EXACT_LOW_CLASS_PERSISTS_NO_TAIL_TRANSFER",
        "old_component": {"rows": len(rows), "columns": len(old_columns), "Q_rank": 330},
        "killers": {
            "columns": len(killers),
            "distinct_low_directions": 3,
            "hit_histogram": dict(sorted(hit_histogram.items())),
            "full_column_profile_each": {"y3": 1, "y4": 6, "y5": 30, "y6": 68},
        },
        "one_killer_by_low_direction": group_records,
        "all_killers": {
            "rank_profile": all_rank_profile,
            "induced_dual": [[row.hex(), value] for row, value in sorted(all_dual.items())],
            "internal_response_packets": [],
        },
        "Schur_verdict": (
            "None of the 14 cells, nor all 14 together, makes residual52 a member of the "
            "complete d5 low image. The low obstruction persists, so a minimized higher-y "
            "tail is not defined on this page."
        ),
        "carrier_referee": {
            "abstract_quotient_fact": (
                "on simultaneous five-set rank9 and H0*H1*H2!=0, blocker equivalence "
                "puts K00 in rowspan(L_T) and annihilates the tiny dual's K00 response restriction"
            ),
            "chain_level_fact": (
                "this annihilates only the carrier restriction. It does not express the full "
                "three-row Macaulay dual as a source boundary; after all first d6 source "
                "attachments an exact nonresponse three-row dual still pairs the target by one"
            ),
            "localized_scope": (
                "a localized filler on the rank9/H-open is not ruled out, but requires an explicit "
                "minor/H-denominator chain certificate. The quotient identity alone is not that certificate."
            ),
            "verdict": (
                "Generic's crossed-response warning is the correct chain-level scope. Tail's "
                "statement is correct only for the abstract carrier-cokernel projection."
            ),
        },
        "scope": "one exact low Schur page only; no broad d6 closure or y10 matrix",
        "source_sha256": {str(path.relative_to(ROOT)): digest for path, digest in EXPECTED.items()},
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    RESULTS.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

    report = """# Minimal S3 dual: one exact Schur page

Each of the 14 new degree-six columns has profile `1,6,30,68` in
`y=3,4,5,6`; its leading layer is a singleton on one of the three tiny-dual
rows.  Adding any one raises the low-column rank from 330 to 331, but adding
the target raises it again to 332 at both audit primes.  Adding all 14 spans
only three new low directions: rank 333, target-augmented rank 334.

Hence cancelling the numerical pairing with the tiny dual is not enough to
start a higher-y Schur transfer.  The target remains nonzero in the y<=3
cokernel, so no minimized higher tail is defined.  After all 14 attachments
the exact induced dual is

`delta_1eb7bd + delta_2045ae - delta_2799b7`,

which has target pairing one and no internal triangle-response restriction.

The five-set/pure quotient theorem does annihilate the original dual's K00
carrier restriction on the rank-nine, H-nonzero open.  It does not by itself
produce a source-chain filler for the full Macaulay class.  Such a localized
claim still needs an explicit minor/H-denominator chain certificate.
"""
    REPORT.write_text(report, encoding="utf-8")
    print("S3 one Schur page: PASS (class persists)")
    print("all-killer ranks:", all_rank_profile)
    print("logical sha256:", result["logical_sha256"])


if __name__ == "__main__":
    main()
