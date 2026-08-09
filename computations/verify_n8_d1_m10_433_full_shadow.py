#!/usr/bin/env python3
"""Exact complete-shadow closure of the N=8 D1 m=10 4+3+3 family."""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import os
import subprocess
import sys
from time import monotonic

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


PINNED_343_SHA256 = (
    "fcf3cf65d3c1588a70292ae4d35ad84a5e81adeb7ddc1e43c48a0b5f4c9ba831"
)
SOURCE = os.path.join(HERE, "verify_n8_d1_m10_343_full_shadow.py")
with open(SOURCE, "rb") as handle:
    require(hashlib.sha256(handle.read()).hexdigest() == PINNED_343_SHA256,
            "the committed 3+4+3 closure source changed")
H = importlib.import_module("verify_n8_d1_m10_343_full_shadow")
F, I, A, D = H.F, H.I, H.A, H.D

PALETTE_PATH = os.path.join(
    HERE, "certificates", "n8_d1_m10_433_rup_palettes.json"
)
EXPECTED_PALETTE_SHA256 = (
    "989e74059eb626a588e810c339f87ae3b5269f0909fc7d2003e72102c9810dbc"
)
EXPECTED_LEDGER_SHA256 = (
    "731316a9b6a0758b70c4bfafcf14b1dbeaf450e38ee1088ca4199c78fc258f8f"
)


def family_branches():
    branches, admissible, sigma, off_sigma = I.surviving_branches()
    rows = [(index, state) for family, index, state in branches
            if family == "433" and index not in (46, 47, 48)]
    require(len(rows) == 54, "the 4+3+3 symbolic frontier changed")
    return rows, admissible, sigma, off_sigma


def check_branch(index, palettes, discover=False):
    branches, admissible, sigma, off_sigma = family_branches()
    state = dict(branches)[index]
    supports, stats = H.dynamic_residuals(
        state, admissible, sigma, off_sigma
    )
    union = frozenset().union(*palettes) if palettes else frozenset()
    hits, direct = 0, 0
    for support in supports:
        certificate = F.direct_complete_support_certificate(
            (support, state[1]), admissible, sigma
        )
        if certificate is not None:
            direct += 1
            continue
        if union:
            compact = F.build_fixed_full_shadow(
                support, state[1], admissible, sigma, off_sigma, union
            )
            if A.M8.unit_refutation(compact.clauses) is not None:
                hits += 1
                continue
        require(discover,
                "branch 433:%d has a complete-shadow survivor" % index)
        full = F.build_fixed_full_shadow(
            support, state[1], admissible, sigma, off_sigma
        )
        core = F.unit_refutation_core_fibres(full)
        require(core is not None,
                "branch 433:%d has a complete-shadow SAT support" % index)
        palette = core["fibres"]
        compact = F.build_fixed_full_shadow(
            support, state[1], admissible, sigma, off_sigma, palette
        )
        require(A.M8.unit_refutation(compact.clauses) is not None,
                "an extracted 4+3+3 RUP palette failed its check")
        palettes.append(palette)
        union = frozenset(set(union) | set(palette))
        hits += 1
    require(direct + hits == len(supports),
            "a 4+3+3 complete support was not closed")
    return {
        "branch": index,
        "dynamic_nodes": stats["nodes"],
        "dynamic_unique_closures": stats["dynamic_unique_closures"],
        "repair_DNF_nodes": stats["repair_DNF_nodes"],
        "free_extension_nodes": stats["free_extension_nodes"],
        "complete_support_residuals": len(supports),
        "direct_complete_support_closures": direct,
        "palette_RUP_closures": hits,
    }, palettes


def worker_command(index, discover):
    command = [sys.executable]
    if sys.flags.optimize:
        command.append("-O")
    command.extend([os.path.abspath(__file__), "--worker", str(index)])
    if discover:
        command.append("--discover")
    return command


def run_worker(index, palettes, discover=False):
    payload = json.dumps(H.encode_palettes(palettes), separators=(",", ":"))
    result = subprocess.run(
        worker_command(index, discover), input=payload, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        cwd=HERE,
    )
    require(result.returncode == 0,
            "433:%d worker failed: %s" % (index, result.stderr.strip()))
    output = json.loads(result.stdout)
    return output["row"], H.decode_palettes(output["palettes"])


def audit(rows):
    started = monotonic()
    with open(PALETTE_PATH, "rb") as handle:
        raw = handle.read()
    require(hashlib.sha256(raw).hexdigest() == EXPECTED_PALETTE_SHA256,
            "the frozen 4+3+3 RUP palettes changed")
    palettes = H.decode_palettes(json.loads(raw.decode("ascii")))
    require(len(rows) == 54,
            "the complete 4+3+3 batch census changed")
    ledger = {
        "pinned_343_sha256": PINNED_343_SHA256,
        "palette_sha256": hashlib.sha256(raw).hexdigest(),
        "inherited_343_palettes": 19,
        "total_root_RUP_palettes": len(palettes),
        "palette_sizes": [len(palette) for palette in palettes],
        "symbolic_branches_closed": len(rows),
        "dynamic_nodes": sum(row["dynamic_nodes"] for row in rows),
        "dynamic_unique_closures": sum(
            row["dynamic_unique_closures"] for row in rows
        ),
        "complete_support_residuals": sum(
            row["complete_support_residuals"] for row in rows
        ),
        "direct_complete_support_closures": sum(
            row["direct_complete_support_closures"] for row in rows
        ),
        "palette_RUP_closures": sum(
            row["palette_RUP_closures"] for row in rows
        ),
        "branch_rows": rows,
        "remaining_m10_symbolic_branches": 131,
        "status": ("the complete m=10 4+3+3 support-shadow family is "
                   "empty; only 3+3+4 remains"),
    }
    digest = D.content_hash(ledger)
    require(digest == EXPECTED_LEDGER_SHA256,
            "the complete 4+3+3 shadow ledger changed")
    return ledger, digest, monotonic() - started


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", type=int)
    parser.add_argument("--discover", action="store_true")
    parser.add_argument("--batch-start", type=int)
    parser.add_argument("--batch-end", type=int)
    parser.add_argument("--batch-output")
    parser.add_argument("--aggregate-dir")
    args = parser.parse_args()
    if args.worker is not None:
        palettes = H.decode_palettes(json.loads(sys.stdin.read()))
        row, palettes = check_branch(args.worker, palettes, args.discover)
        print(json.dumps({"row": row,
                          "palettes": H.encode_palettes(palettes)},
                         sort_keys=True, separators=(",", ":")))
        return
    if args.batch_start is not None:
        require(args.batch_end is not None,
                "a batch end is required with a batch start")
        with open(PALETTE_PATH, "rb") as handle:
            palettes = H.decode_palettes(json.loads(handle.read()))
        branches, _admissible, _sigma, _off_sigma = family_branches()
        rows = []
        for index, _state in branches[args.batch_start:args.batch_end]:
            row, returned = check_branch(index, list(palettes), False)
            require(returned == palettes,
                    "a checking worker mutated the frozen palettes")
            rows.append(row)
        payload = json.dumps(rows, sort_keys=True, separators=(",", ":"))
        if args.batch_output:
            with open(args.batch_output, "w") as handle:
                handle.write(payload)
        else:
            print(payload)
        return
    require(args.aggregate_dir is not None,
            "use --aggregate-dir after checking isolated batches")
    rows = []
    for filename in sorted(os.listdir(args.aggregate_dir),
                           key=lambda value: int(value.split(".")[0])):
        with open(os.path.join(args.aggregate_dir, filename), "r") as handle:
            rows.extend(json.load(handle))
    ledger, digest, seconds = audit(rows)
    print("n8 D1 m=10 complete 4+3+3 shadow: PASS (exact)")
    print("branches closed:", ledger["symbolic_branches_closed"])
    print("dynamic nodes:", ledger["dynamic_nodes"])
    print("complete supports:", ledger["complete_support_residuals"])
    print("RUP palettes:", ledger["total_root_RUP_palettes"])
    print("remaining m=10 symbolic branches: 131")
    print("ledger sha256:", digest)
    print("total: %.1f s" % seconds)


if __name__ == "__main__":
    main()
