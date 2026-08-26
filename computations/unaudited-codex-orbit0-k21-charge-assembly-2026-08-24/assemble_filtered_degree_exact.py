#!/usr/bin/env python3
"""Strict exact-Q charge assembler for one filtered degree K20--K24.

The input manifest contains scalar groups.  A group may cover one lineage via
``id`` or several inseparable lineages via ``ids``; its scalar is added once.
Completeness is checked against the frozen source-faithful recurrence DAG.
"""

from collections import Counter
from fractions import Fraction
from pathlib import Path
import argparse
import hashlib
import json
import re


ROOT = Path(__file__).resolve().parents[2]
DAG_PATH = ROOT / (
    "computations/unaudited-codex-orbit0-k14-k24-recurrence-dag-2026-08-23/"
    "results_recurrence_dag.json"
)
HEX64 = re.compile(r"^[0-9a-f]{64}$")
SUPPORTED_DEGREES = tuple(range(20, 25))


def rational(value):
    if isinstance(value, int):
        return Fraction(value)
    if isinstance(value, str):
        return Fraction(value)
    if isinstance(value, dict):
        return Fraction(int(value["numerator"]), int(value["denominator"]))
    raise TypeError(value)


def render(value):
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "text": str(value),
    }


def entry_ids(entry):
    if ("id" in entry) == ("ids" in entry):
        raise ValueError("exactly one of id/ids is required")
    result = [entry["id"]] if "id" in entry else entry["ids"]
    if (
        not isinstance(result, list)
        or not result
        or not all(isinstance(item, str) for item in result)
        or len(result) != len(set(result))
    ):
        raise ValueError(f"bad IDs {result}")
    return result


def assemble(degree, manifest, allow_partial=False):
    if degree not in SUPPORTED_DEGREES:
        raise ValueError(f"unsupported degree K{degree}")
    dag = json.loads(DAG_PATH.read_text())
    required = dag["required_reachable_lineage_ids_by_degree"][str(degree)]
    if len(required) != len(set(required)):
        raise ValueError(f"frozen K{degree} DAG contains duplicate IDs")
    has_groups = "groups" in manifest
    has_paths = "paths" in manifest
    if has_groups == has_paths:
        raise ValueError("manifest requires exactly one of groups/paths")
    entries = manifest["groups"] if has_groups else manifest["paths"]
    flat = [item for entry in entries for item in entry_ids(entry)]
    counts = Counter(flat)
    duplicate = sorted(item for item, count in counts.items() if count != 1)
    required_set = set(required)
    extra = sorted(set(flat) - required_set)
    present = set(flat)
    missing = [item for item in required if item not in present]
    for entry in entries:
        if not HEX64.fullmatch(entry.get("evidence_sha256", "")):
            raise ValueError(f"bad digest {entry_ids(entry)}")
    if duplicate or extra:
        raise ValueError(f"duplicate={duplicate} extra={extra}")
    if missing and not allow_partial:
        raise ValueError(f"missing {len(missing)} K{degree} IDs: {missing}")
    full = sum((rational(entry["full"]) for entry in entries), Fraction())
    irreducible = sum(
        (rational(entry["irreducible"]) for entry in entries), Fraction()
    )
    manifest_logical = hashlib.sha256(
        json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    complete = not missing
    return {
        "status": (
            f"PASS_COMPLETE_K{degree}_{len(required)}_ID_EXACT_Q"
            if complete
            else f"REJECT_INCOMPLETE_K{degree}_{len(required)}_ID_GATE"
        ),
        "complete_claim": complete,
        "degree": degree,
        "required_paths": len(required),
        "covered_paths": len(flat),
        "scalar_groups": len(entries),
        "missing_paths": missing,
        "duplicate_paths": duplicate,
        "extra_paths": extra,
        "full": render(full),
        "irreducible": render(irreducible),
        "covered_ids": flat,
        "dag_logical_sha256": dag["logical_sha256"],
        "manifest_logical_sha256": manifest_logical,
    }


def self_test():
    dag = json.loads(DAG_PATH.read_text())
    zero_digest = "0" * 64
    tested = {}
    for degree in SUPPORTED_DEGREES:
        required = dag["required_reachable_lineage_ids_by_degree"][str(degree)]
        good = {
            "groups": [
                {
                    "ids": required[:4],
                    "full": "7/3",
                    "irreducible": "11/5",
                    "evidence_sha256": zero_digest,
                },
                *(
                    {
                        "id": item,
                        "full": "0",
                        "irreducible": "0",
                        "evidence_sha256": zero_digest,
                    }
                    for item in required[4:]
                ),
            ]
        }
        result = assemble(degree, good)
        if not result["complete_claim"]:
            raise AssertionError("complete manifest rejected")
        if result["covered_paths"] != len(required):
            raise AssertionError("covered-path count mismatch")
        if result["full"]["text"] != "7/3":
            raise AssertionError("group scalar was not counted exactly once")
        try:
            assemble(degree, {"groups": good["groups"][:-1]})
        except ValueError as error:
            if "missing 1" not in str(error):
                raise
        else:
            raise AssertionError("missing mutation accepted")
        try:
            assemble(degree, {"groups": good["groups"] + [good["groups"][-1]]})
        except ValueError as error:
            if "duplicate" not in str(error):
                raise
        else:
            raise AssertionError("duplicate mutation accepted")
        extra = json.loads(json.dumps(good))
        extra["groups"][-1]["id"] = f"D99:hostile|R:{degree}"
        try:
            assemble(degree, extra)
        except ValueError as error:
            if "extra" not in str(error):
                raise
        else:
            raise AssertionError("extra-path mutation accepted")
        bad_digest = json.loads(json.dumps(good))
        bad_digest["groups"][0]["evidence_sha256"] = "0" * 63
        try:
            assemble(degree, bad_digest)
        except ValueError as error:
            if "bad digest" not in str(error):
                raise
        else:
            raise AssertionError("bad digest accepted")
        try:
            assemble(degree, {"groups": good["groups"], "paths": good["groups"]})
        except ValueError as error:
            if "exactly one" not in str(error):
                raise
        else:
            raise AssertionError("ambiguous manifest schema accepted")
        tested[str(degree)] = len(required)
    print(
        json.dumps(
            {
                "status": "PASS_FILTERED_DEGREE_ASSEMBLER_SELFTEST",
                "tested_required_path_counts": tested,
                "group_scalar_once": True,
                "missing_rejected": True,
                "duplicate_rejected": True,
                "extra_rejected": True,
                "bad_digest_rejected": True,
                "ambiguous_schema_rejected": True,
            },
            sort_keys=True,
        )
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--audit-incomplete", action="store_true")
    parser.add_argument("--degree", type=int)
    parser.add_argument("manifest", nargs="?")
    parser.add_argument("output", nargs="?")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    if args.degree is None or args.manifest is None or args.output is None:
        parser.error("--degree, manifest, and output are required")
    try:
        result = assemble(
            args.degree,
            json.loads(Path(args.manifest).read_text()),
            args.audit_incomplete,
        )
    except ValueError as error:
        print(f"REJECT: {error}")
        raise SystemExit(2)
    output = Path(args.output)
    temporary = Path(str(output) + ".tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    temporary.replace(output)
    print(
        json.dumps(
            {
                key: result[key]
                for key in (
                    "status",
                    "covered_paths",
                    "missing_paths",
                    "full",
                    "irreducible",
                )
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
