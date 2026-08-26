#!/usr/bin/env python3
"""Read-only semantic audit of the recovered hidden-K16 child provider."""

from hashlib import sha256
import json
from pathlib import Path
import struct


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FULL_DIR = ROOT / "computations/unaudited-codex-orbit0-k14-hidden-k16-parent-full-2026-08-23"
FILES = {
    "recovery": FULL_DIR / "results_full_hidden_k16_parent_recovery.json",
    "merge": FULL_DIR / "results_profile_merge.json",
    "provider_source": FULL_DIR / "stream_hidden_k16_children.rs",
    "recovery_source": FULL_DIR / "reconstruct_hidden_k16_parent_runs.rs",
    "dag": ROOT / "computations/unaudited-codex-orbit0-k14-k24-recurrence-dag-2026-08-23/results_recurrence_dag.json",
    "arithmetic": ROOT / "computations/unaudited-codex-orbit0-k19-k24-arithmetic-plan-2026-08-23/results_k19_k24_arithmetic.json",
}
OUT = HERE / "results_hidden_k16_child_stage_audit.json"
U = 400_591_699_200
TAILS = {2: 12, 3: 32, 4: 60}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def read_first_parent():
    path = FULL_DIR / "parents_000_016.bin"
    with path.open("rb") as stream:
        header = stream.read(40)
        record = stream.read(64)
    require(header[:8] == b"H16RUN2\0", header[:8])
    require(int.from_bytes(header[8:24], "little", signed=True) == U,
            header[8:24].hex())
    require(struct.unpack_from("<HHH", header, 24) == (0, 16, 64),
            struct.unpack_from("<HHH", header, 24))
    require(len(record) == 64, len(record))
    return {
        "path": path,
        "row": record[:24],
        "weight": int.from_bytes(record[24:40], "little", signed=True),
        "signature": list(record[40:52]),
        "source_slice": struct.unpack_from("<H", record, 52)[0],
        "source_labels": list(record[54:59]),
        "m1": record[59],
        "m2": record[60],
    }


def audit_guard(degree, parent):
    path = FULL_DIR / f"provider_guard_k{degree}.bin"
    data = path.read_bytes()
    header = data[:64]
    require(header[:8] == b"H16CHD2\0", header[:8])
    require(int.from_bytes(header[8:24], "little", signed=True) == U,
            header[8:24].hex())
    require(header[24] == degree, (header[24], degree))
    require(struct.unpack_from("<H", header, 25)[0] == 0,
            struct.unpack_from("<H", header, 25)[0])
    require(struct.unpack_from("<QQQH", header, 32) ==
            (0, 1, parent["m2"] * TAILS[degree], 52),
            struct.unpack_from("<QQQH", header, 32))
    records = [data[offset:offset + 52] for offset in range(64, len(data), 52)]
    require(all(len(record) == 52 for record in records), len(data))
    expected_weight = -parent["weight"] // parent["m2"]
    require(parent["weight"] % parent["m2"] == 0,
            (parent["weight"], parent["m2"]))
    seen = set()
    for record in records:
        require(int.from_bytes(record[24:40], "little", signed=True) == expected_weight,
                record[24:40].hex())
        require(struct.unpack_from("<Q", record, 40)[0] == 0,
                struct.unpack_from("<Q", record, 40)[0])
        pivot, tail_index, m2, stored_degree = record[48:52]
        require((m2, stored_degree) == (parent["m2"], degree),
                (m2, stored_degree))
        require(tail_index < TAILS[degree], tail_index)
        seen.add((pivot, tail_index))
    require(len(seen) == len(records) == parent["m2"] * TAILS[degree],
            (len(seen), len(records)))
    return {
        "degree": degree,
        "children": len(records),
        "child_weight_scaled": expected_weight,
        "sha256": digest(path),
    }


def build(mutate=False):
    recovery = json.loads(FILES["recovery"].read_text())
    merge = json.loads(FILES["merge"].read_text())
    dag = json.loads(FILES["dag"].read_text())
    arithmetic = json.loads(FILES["arithmetic"].read_text())
    require(recovery["status"] == "PASS_FULL_HIDDEN_K16_PARENT_RECOVERY",
            recovery["status"])
    require(recovery["scope"] ==
            "parents/profiles/providers only; no child-tail charge evaluation",
            recovery["scope"])
    require(recovery["scale"] == U ==
            arithmetic["recommended_single_integer_scale"],
            (recovery["scale"], arithmetic["recommended_single_integer_scale"]))
    require((recovery["hidden_parent_occurrences"],
             recovery["outgoing_second_pivot_uses"],
             recovery["merged_profile_records"],
             recovery["exact_zero_profile_keys"]) ==
            (75_691_040, 511_477_120, 6_229_700, 355_738),
            recovery)

    m1 = {int(key): value for key, value in recovery["first_denominator_hist"].items()}
    m2 = {int(key): value for key, value in recovery["second_denominator_hist"].items()}
    products = {int(key): value for key, value in
                recovery["product_denominator_hist"].items()}
    require(sum(m1.values()) == recovery["heads"], sum(m1.values()))
    require(sum(key * value for key, value in m1.items()) ==
            recovery["first_pivot_uses"], m1)
    require(sum(m2.values()) == recovery["hidden_parent_occurrences"],
            sum(m2.values()))
    require(sum(key * value for key, value in m2.items()) ==
            recovery["outgoing_second_pivot_uses"], m2)
    require(sum(products.values()) == recovery["hidden_parent_occurrences"],
            sum(products.values()))
    require(all(U % product == 0 for product in products), sorted(products))

    node = {row["id"]: row for row in dag["nodes"]}
    immediate = ["D14:222|R:2-2", "D14:222|R:2-3", "D14:222|R:2-4"]
    exact_products = set(node[immediate[0]]["denominator_product_class"]["products"])
    require(all(set(node[lineage]["denominator_product_class"]["products"])
                == exact_products for lineage in immediate), immediate)
    require(set(products) == exact_products, (set(products) ^ exact_products))
    require(node["D14:222|R:2"]["sign_relative_to_unsigned_R8prime"] == 1,
            node["D14:222|R:2"])
    require(all(node[lineage]["sign_relative_to_unsigned_R8prime"] == -1
                for lineage in immediate), immediate)

    parent = read_first_parent()
    guards = {str(degree): audit_guard(degree, parent) for degree in (2, 3, 4)}
    if mutate:
        guards["2"]["children"] -= 1
    require(guards["2"]["children"] == parent["m2"] * 12, guards["2"])
    require(guards["3"]["children"] == parent["m2"] * 32, guards["3"])
    require(guards["4"]["children"] == parent["m2"] * 60, guards["4"])

    outgoing = recovery["outgoing_second_pivot_uses"]
    literal_child_counts = {str(degree): outgoing * tails
                            for degree, tails in TAILS.items()}
    require(literal_child_counts == {
        "2": 6_137_725_440,
        "3": 16_367_267_840,
        "4": 30_688_627_200,
    }, literal_child_counts)
    profile_records = recovery["merged_profile_records"]
    profile_eval_counts = {str(degree): profile_records * tails
                           for degree, tails in TAILS.items()}
    profile_sum = int(recovery["merged_profile_weight_sum_scaled"])
    require(profile_sum == -int(recovery["parent_weight_sum_scaled"]),
            profile_sum)
    child_weight_sums = {str(degree): profile_sum * tails
                         for degree, tails in TAILS.items()}

    merged_path = FULL_DIR / "hidden_k16_second_pivot_profiles_full.bin"
    with merged_path.open("rb") as stream:
        merged_header = stream.read(32)
    require(merged_header[:8] == b"H16MER2\0", merged_header[:8])
    require(int.from_bytes(merged_header[8:24], "little", signed=True) == U,
            merged_header[8:24].hex())
    require(struct.unpack_from("<Q", merged_header, 24)[0] == profile_records,
            struct.unpack_from("<Q", merged_header, 24)[0])
    require(merged_path.stat().st_size == 32 + 59 * profile_records,
            merged_path.stat().st_size)

    result = {
        "status": "PASS_EXACT_HIDDEN_K16_CHILD_STAGE_SEMANTICS_NO_CHILD_RUN",
        "scope": (
            "Read-only audit of the recovered parent/provider and exact immediate-child "
            "execution semantics. No K18/K19/K20 child expansion or charge was run."
        ),
        "source_checkpoint": {
            "parent_occurrence_records": recovery["hidden_parent_occurrences"],
            "parent_bytes": recovery["parent_bytes_total"],
            "outgoing_second_pivot_uses": outgoing,
            "merged_second_pivot_profiles": profile_records,
            "merged_profile_bytes": recovery["merged_profile_bytes"],
            "scale": U,
            "record_semantics": (
                "Each 64-byte parent is an uncollected literal occurrence with scaled "
                "first-response H-slice mass w1, signature, full source labels, m1 and m2."
            ),
        },
        "sign_and_division": {
            "direct_target": "P=-R8prime*E2*E2*E2",
            "K16_hidden_parent": (
                "w1=(R8prime H-slice mass)*U/m1; this is the first response and has DAG sign +"
            ),
            "all_immediate_children": (
                "w2=-w1/m2; K18 [2,2], K19 [2,3], K20 [2,4] all have DAG sign -"
            ),
            "division_checks": [
                "mass*U % m1 == 0",
                "w1 % m2 == 0",
                "m1*m2 is one of the exact 66 DAG products and divides U",
            ],
            "product_count": len(products),
            "maximum_product": max(products),
            "product_lcm": node[immediate[0]]["denominator_product_class"]["product_lcm"],
        },
        "exact_child_counts": {
            "literal_provider": literal_child_counts,
            "total_literal_children": sum(literal_child_counts.values()),
            "merged_profile_tail_evaluations": profile_eval_counts,
            "scaled_child_weight_sum_before_cycle_functional": child_weight_sums,
            "formula": "N_degree = outgoing_second_pivot_uses * (12,32,60)",
        },
        "K2_to_K18_parent_semantics": {
            "lineage": "D14:222|R:2-2",
            "required_source": "the 31 literal parent occurrence files and degree-2 provider",
            "required_pipeline": [
                "stream degree-2 children; do not materialize the 52-byte raw provider packet",
                "canonicalize every 24-byte child under H and add its signed w2 to an external sorted run",
                "merge every run globally, delete exact zeros only after signed addition",
                "for each canonical child compute its H-orbit size O and assert scaled orbit_mass % O == 0",
                "store canonical row, scaled per-labelled coefficient orbit_mass/O, orbit size, lineage and run digest",
                "split zero-pivot rows into the K18 normal 77-profile; retain pivotable rows as the [2,2] parent checkpoint",
                "before its next reduction assert the third denominator product belongs to D14:222|R:2-2-2 and divides U",
            ],
            "why_merged_profile_is_insufficient": (
                "The 29-byte open-cycle key forgets the literal child row and tail index; "
                "it cannot be used as the source-labelled K18 parent checkpoint."
            ),
        },
        "K3_K4_profile_semantics": {
            "lineages": ["D14:222|R:2-3", "D14:222|R:2-4"],
            "immediate_charge_pipeline": (
                "Read the 6,229,700 exact merged open-profile keys once; attach the 32 "
                "K3 and 60 K4 tails in separate lineage accumulators, derive child signature/cycle "
                "partition, and sum exact irreducible-page profiles/scalars with weight w2."
            ),
            "profile_evaluations": {
                "K3": profile_eval_counts["3"],
                "K4": profile_eval_counts["4"],
            },
            "downstream_guard": (
                "A scalar or the existing open profile is sufficient for the immediate K19/K20 "
                "cycle charge only. Any pivotable K19/K20 child still needs either a literal-row "
                "fallback or a separately proved third-pivot profile before emitting terminal descendants."
            ),
        },
        "shared_pass_verdict": {
            "mathematically_safe": True,
            "rule": (
                "One pass over literal parents may compute w2 once per p2, stream K2 children to "
                "the canonical collector, and evaluate K3/K4 scalar profiles in disjoint sinks. "
                "All maps are linear and use the same source labels and w2."
            ),
            "recommended_engineering": (
                "Use two physical consumers: a restartable literal K2 collector and one shared "
                "K3+K4 pass over the already merged 6.23m profile file. This avoids writing "
                "16.37b K3 and 30.69b K4 literal child records."
            ),
            "not_safe": [
                "combining K2/K3/K4 coefficients into one key without a degree/lineage tag",
                "pivoting the K2 branch from the wildcard open-profile file instead of the canonical literal K18 page",
                "claiming K3/K4 descendant completion from an immediate scalar charge alone",
            ],
        },
        "provider_guard": {
            "first_parent": {
                "weight_scaled": parent["weight"],
                "m1": parent["m1"],
                "m2": parent["m2"],
            },
            "degree_guards": guards,
        },
        "stop_replay_assertions": [
            "The 31 parent run intervals cover H slices 0..485 exactly and all hashes match the recovery ledger.",
            "sum m2_hist=75691040 and sum m2*count=511477120.",
            "Provider chunk count equals parent_count-specific SUM(m2)*tail_count, not a universal 36/96/180 per parent.",
            "Each child header pins U, degree, run_start, parent_start/count, child count and 52-byte format.",
            "Every child stores w2=-w1/m2 and exact source ordinal/p2/tail_index/m2/degree.",
            "K2 canonical collection must finish globally before any [2,2] third-pivot reduction begins.",
            "K3 and K4 accumulators have separate lineage IDs and reproduce the exact child weight sums before applying the cycle functional.",
            "Abort on any nondividing U/product, sign, degree, H-orbit division, zero-before-merge, cursor gap/overlap or hash mismatch.",
        ],
        "pinned": {
            str(path.relative_to(ROOT)): digest(path)
            for path in FILES.values()
        } | {
            str(path.relative_to(ROOT)): digest(path)
            for path in [FULL_DIR / f"provider_guard_k{degree}.bin" for degree in (2, 3, 4)]
        },
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode()).hexdigest()
    return result


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--hostile", action="store_true")
    args = parser.parse_args()
    result = build(mutate=args.hostile)
    if args.write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "exact_child_counts": result["exact_child_counts"],
        "shared_pass": result["shared_pass_verdict"],
        "logical_sha256": result["logical_sha256"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

